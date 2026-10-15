#!/usr/bin/env python3
"""Refresh feeds (news, YouTube reviews, podcasts, tournaments) into data/*.json, then rebuild the site.
Usage: python3 update.py [--no-fetch]   (daily cron: 0 6 * * * cd /path && python3 update.py)"""
import json, re, sys, html, datetime, time, subprocess, pathlib
import feedparser, requests
ROOT = pathlib.Path(__file__).parent
DATA = ROOT / "data"; DATA.mkdir(exist_ok=True)
CFG = json.loads((ROOT / "config.json").read_text())
UA = {"User-Agent": "Mozilla/5.0 (compatible; DropThePickleBot/1.0; feed reader)"}
# Review filter: a title is kept if it names gear (paddle/shoe/ball/brand/spec) AND reads like a review/test/comparison.
BRANDS=r"selkirk|joola|crbn|six ?zero|engage|gearbox|paddletek|vatic|bread ?(?:&|and) ?butter|bnb|franklin|onix|electrum|diadem|11six24|prokennex|volair|ronbus|proton|holbrook|babolat|wilson|pickleball apes|pb apes|luzz|gamma|recess|enhance|honolulu|spartus|rpm|thrive|neonic|cpx|arronax|pakle|gherkin|mehau|pickle poppers|legacy|vulcan|head|adidas|asics|k-swiss|acacia|skechers|fila|apl|hexgrit|armorgrit"
STRONG=re.compile(r"\breview(?:ed|s)?\b|first (?:look|impressions?|hits)|impressions|\bvs\.?\b|versus|tier list|unbox|quick ?take|play test|drill test|lab (?:test|result)|retest", re.I)
GEAR=re.compile(rf"paddles?\b|shoes?\b|sneakers?|pickleballs?\b|\bballs?\b|\bbags?\b|overgrip|grips?\b|grit\b|lead tape|edge guard|\bcore\b|foam|carbon|kevlar|thermoform|\d+ ?mm\b|swing ?weight|twist ?weight|\b(?:{BRANDS})\b", re.I)
WEAK=re.compile(r"tested|testing|\btests?\b|compar|honest|worth|hype|best|top \d+|rank|spin|power|control|rpm|specs?|budget|upgrade|\bnew\b|release|durab|update|value|tier|elite|choosing|until you watch|should you buy|buyer'?s guide|breakdown|explained|data|roundup|picks", re.I)
NO=re.compile(r"livestream|full match|highlights?\b|crashouts?|recap|giveaway winner|\bdrills? to\b|how to (?:hit|serve|play|dink)", re.I)
def is_review(title):
    if NO.search(title): return False
    if STRONG.search(title) and GEAR.search(title): return True
    if STRONG.search(title) and re.search(r"\breview\b|first (?:look|impressions?)", title, re.I): return True
    return bool(GEAR.search(title) and WEAK.search(title) and re.search(rf"paddles?\b|shoes?\b|pickleballs?\b|balls?\b|\b(?:{BRANDS})\b", title, re.I))

SOURCES_FILE = DATA / "sources.json"
def registry():
    try: return json.loads(SOURCES_FILE.read_text())["sources"]
    except Exception: return []
def pipeline(kind):
    """Merge config lists with every registry source flagged in_pipeline (the registry is the living list)."""
    out = {}
    if kind == "youtube":
        out.update(CFG["YOUTUBE_CHANNELS"])
        for s in registry():
            if s["type"] == "youtube" and s.get("in_pipeline") and s.get("channel_id"): out.setdefault(s["name"], s["channel_id"])
        # de-dupe by channel id
        seen, res = set(), {}
        for k, v in out.items():
            if v not in seen: seen.add(v); res[k] = v
        return res
    if kind == "news":
        out.update(CFG["NEWS_FEEDS"])
        for s in registry():
            if s["type"] not in ("youtube","podcast","x","instagram","forum") and s.get("in_pipeline") and s["feed"].get("rss") and "events.xml" not in s["feed"]["rss"]:
                if not any(s["feed"]["rss"].split("//")[1].split("/")[0].replace("www.","") in u for u in out.values()): out[s["name"]] = s["feed"]["rss"]
        return out
    if kind == "podcast":
        out.update(CFG.get("PODCAST_FEEDS", {}))
        for s in registry():
            if s["type"] == "podcast" and s.get("in_pipeline"): out.setdefault(s["name"], s["feed"]["rss"])
        return out
STOP = set("the a an and or of to in on for with at by from is are was be this that it its as your you how why what new".split())

def get(url):
    r = requests.get(url, headers=UA, timeout=25); r.raise_for_status(); return r.content

def iso(entry):
    t = entry.get("published_parsed") or entry.get("updated_parsed")
    return time.strftime("%Y-%m-%d", t) if t else ""

def save(name, obj):
    obj["updated"] = datetime.datetime.now().isoformat(timespec="minutes")
    (DATA / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False))

def keep_old(name, err):
    print(f"  ! {name}: {err} (keeping previous data)")

def summary(source, title, tags, date):
    # One line in our own words: who published it, when, and what it's filed under. No copied body text.
    tags = [t for t in tags if t and t.lower() not in ("uncategorized", "news", "pickleball")][:3]
    s = f"{source} story from {date}" if date else f"{source} story"
    return s + (f", filed under {', '.join(tags)}." if tags else ". Read the full piece at the source.")

def news():
    items, status = [], {}
    for src, url in pipeline("news").items():
        try:
            f = feedparser.parse(get(url)); n = 0
            for e in f.entries[:8]:
                if not e.get("link"): continue
                d = iso(e)
                items.append(dict(source=src, title=html.unescape(e.title), link=e.link, date=d,
                    summary=summary(src, e.title, [t.get("term", "") for t in e.get("tags", [])], d)))
                n += 1
            status[src] = f"ok ({n})"
        except Exception as ex:
            status[src] = f"failed: {ex}"
    items.sort(key=lambda x: x["date"], reverse=True)
    print("news:", status)
    if items: save("news.json", dict(items=items, sources=status))
    else: keep_old("news.json", "no items")

def reviews():
    vids, status = [], {}
    for ch, cid in pipeline("youtube").items():
        try:
            f = feedparser.parse(get(f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}")); n = 0
            for e in f.entries:
                if "/shorts/" in e.link or not is_review(e.title): continue
                vids.append(dict(channel=ch, channel_url=f"https://www.youtube.com/channel/{cid}",
                    title=html.unescape(e.title), link=e.link, video_id=e.get("yt_videoid", ""), date=iso(e)))
                n += 1
            status[ch] = f"ok ({n})"
        except Exception as ex:
            status[ch] = f"failed: {ex}"
    vids.sort(key=lambda x: x["date"], reverse=True)
    allv = list(vids)  # uncapped list, used to match videos to paddle pages
    per = {}; capped = []
    for v in vids:  # max 6 per channel so one prolific reviewer can't crowd out the rest
        per[v["channel"]] = per.get(v["channel"], 0) + 1
        if per[v["channel"]] <= 6: capped.append(v)
    vids = capped
    print("reviews:", status)
    if vids: save("reviews.json", dict(items=vids[:60], all_items=allv, sources=status))
    else: keep_old("reviews.json", "no items")

def podcasts():
    eps, status = [], {}
    for src, url in pipeline("podcast").items():
        try:
            f = feedparser.parse(get(url)); n = 0
            for e in f.entries[:3]:
                link = e.get("link") or ""
                if not link.startswith("http") or link.endswith((".xml", ".rss")):
                    link = next((s["url"] for s in registry() if s["name"] == src), "")
                    if not link: continue
                eps.append(dict(show=src, title=html.unescape(e.title), link=link, date=iso(e))); n += 1
            status[src] = f"ok ({n})"
        except Exception as ex:
            status[src] = f"failed: {ex}"
    eps.sort(key=lambda x: x["date"], reverse=True)
    print("podcasts:", status)
    if eps: save("podcasts.json", dict(items=eps, sources=status))
    else: keep_old("podcasts.json", "no items")

def tournaments():
    evs, status = [], {}
    today = datetime.date.today().isoformat()
    for src, url in CFG["TOURNAMENT_FEEDS"].items():
        try:
            raw = get(url).decode("utf-8", "replace")
            for item in re.findall(r"<item>(.*?)</item>", raw, re.S):
                g = lambda tag: html.unescape((re.search(rf"<{tag}>(.*?)</{tag}>", item, re.S) or [None, ""])[1]).strip()
                end = g("ev:enddate") or g("ev:startdate")
                if end and end < today: continue
                tickets = re.search(r"Tickets: (https://\S+)", g("description"))
                evs.append(dict(source=src, name=g("title"), link=g("link"), start=g("ev:startdate"), end=g("ev:enddate"),
                    location=g("ev:location"), tickets=tickets.group(1) if tickets else ""))
            status[src] = f"ok ({len(evs)})"
        except Exception as ex:
            status[src] = f"failed: {ex}"
    evs.sort(key=lambda x: x["start"])
    print("tournaments:", status)
    if evs: save("tournaments.json", dict(items=evs, sources=status))
    else: keep_old("tournaments.json", "no items")

if __name__ == "__main__":
    if "--no-fetch" not in sys.argv:
        for fn in (news, reviews, podcasts, tournaments):
            try: fn()
            except Exception as ex: print("error in", fn.__name__, ex)
        try: subprocess.call([sys.executable, str(ROOT / "scripts/track_prices.py")])
        except Exception as ex: print("error in track_prices", ex)
    sys.exit(subprocess.call([sys.executable, str(ROOT / "build.py")]))
