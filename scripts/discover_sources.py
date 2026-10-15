#!/usr/bin/env python3
"""Weekly discovery of new/rising pickleball sources. Appends candidates to data/sources.json with flag "new"
(never auto-wired into the site: a human sets in_pipeline=true after review).

Sanctioned inputs only:
  - YouTube Data API v3 search + channel stats, if YT_API_KEY is set (official API, gives real subscriber counts)
  - YouTube links shared in r/Pickleball via the Arctic Shift archive API, resolved with YouTube oEmbed (official)
  - Google News RSS mentions ("pickleball ...") -> publisher domains, then probe each for its own RSS feed
  - Apple Podcasts / iTunes Search API (public) for new pickleball shows
Audience is 'unknown' unless an official API returns a number.
Cron: 0 7 * * 1 cd /path/pickleball-hub && python3 scripts/discover_sources.py && python3 scripts/report_sources.py
"""
import json, os, re, time, datetime, pathlib, collections, urllib.parse
import requests, feedparser
R = pathlib.Path(__file__).parent.parent; F = R / "data/sources.json"
UA = {"User-Agent": "Mozilla/5.0 (compatible; DropThePickleBot/1.0; +discovery)"}
TODAY = datetime.date.today().isoformat()
reg = json.loads(F.read_text()); S = reg["sources"]
known_ids = {s.get("channel_id") for s in S if s.get("channel_id")}
known_urls = {re.sub(r"^https?://(www\.)?", "", s["url"]).rstrip("/").lower() for s in S}
known_dom = {u.split("/")[0] for u in known_urls}
known_feeds = {(s.get("feed") or {}).get("rss") for s in S}
added = []
def add(entry):
    entry.update(flag="new", added=TODAY, in_pipeline=False, status="candidate")
    entry["id"] = f"{entry['type']}:{entry.get('channel_id') or entry['url']}"
    S.append(entry); added.append(entry)
def get(u, **kw):
    r = requests.get(u, headers=UA, timeout=25, **kw); r.raise_for_status(); return r

def youtube_api(key):
    ids = collections.Counter()
    for q in ["pickleball paddle review", "pickleball", "pickleball coaching", "pickleball gear"]:
        j = get("https://www.googleapis.com/youtube/v3/search", params=dict(part="snippet", q=q, type="video", order="date",
                publishedAfter=(datetime.datetime.utcnow() - datetime.timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ"), maxResults=50, key=key)).json()
        for it in j.get("items", []): ids[it["snippet"]["channelId"]] += 1
    new = [c for c, n in ids.most_common(100) if c not in known_ids]
    for i in range(0, len(new), 50):
        j = get("https://www.googleapis.com/youtube/v3/channels", params=dict(part="snippet,statistics", id=",".join(new[i:i+50]), key=key)).json()
        for ch in j.get("items", []):
            subs = int(ch["statistics"].get("subscriberCount", 0) or 0)
            if subs < 1000 or ch["statistics"].get("hiddenSubscriberCount"): continue
            cid = ch["id"]; known_ids.add(cid)
            add(dict(name=ch["snippet"]["title"], type="youtube", subtype="unclassified", channel_id=cid, url=f"https://www.youtube.com/channel/{cid}",
                     audience=dict(value=f"{subs:,}", metric="youtube_subscribers", source="YouTube Data API v3 channels.statistics", as_of=TODAY),
                     feed=dict(rss=f"https://www.youtube.com/feeds/videos.xml?channel_id={cid}", api="YouTube Data API v3"),
                     scraping=dict(robots="n/a (RSS used)", tos="RSS + embed only", allowed_method="rss+embed"),
                     note=f"{ids[cid]} recent pickleball videos in API search"))

def youtube_from_reddit():
    after = int(time.time() - 30 * 86400); seen = collections.Counter(); meta = {}
    try:
        j = get("https://arctic-shift.photon-reddit.com/api/posts/search", params=dict(subreddit="Pickleball", after=after, limit=100, fields="url,title")).json()
    except Exception as ex:
        print("reddit archive failed:", ex); return
    for p in j.get("data", []):
        u = p.get("url") or ""
        if "youtu" not in u: continue
        try: o = get("https://www.youtube.com/oembed", params=dict(url=u, format="json")).json()
        except Exception: continue
        au = o.get("author_url", ""); seen[au] += 1; meta[au] = o.get("author_name", au)
    for au, n in seen.most_common():
        key = re.sub(r"^https?://(www\.)?", "", au).rstrip("/").lower()
        if not au or key in known_urls: continue
        # resolve channel id via the channel's public RSS link is not possible from a handle without the page; keep URL only
        known_urls.add(key)
        add(dict(name=meta[au], type="youtube", subtype="unclassified", url=au, audience=dict(value="unknown", metric="", source="no official count fetched (set YT_API_KEY)", as_of=TODAY),
                 feed=dict(rss=None, api="YouTube Data API v3"), scraping=dict(robots="n/a", tos="RSS + embed only", allowed_method="rss+embed"),
                 note=f"shared {n}x in r/Pickleball in the last 30 days (Arctic Shift archive, resolved via YouTube oEmbed)"))

def news_mentions():
    doms = collections.Counter(); names = {}
    for q in ["pickleball", "pickleball paddle", "pickleball tournament", "pickleball league"]:
        try: f = feedparser.parse(get("https://news.google.com/rss/search?" + urllib.parse.urlencode(dict(q=q, hl="en-US", gl="US", ceid="US:en"))).content)
        except Exception as ex: print("google news failed:", ex); continue
        for e in f.entries:
            src = e.get("source") or {}
            href = src.get("href", "")
            if not href: continue
            d = re.sub(r"^https?://(www\.)?", "", href).split("/")[0].lower()
            title = src.get("title", d)
            if "pickle" in d or "pickle" in title.lower() or "dink" in d: doms[d] += 2   # pickleball-native outlets weigh more
            else: doms[d] += 0  # general outlets are tracked but not added
            names[d] = title
    for d, n in doms.most_common():
        if n < 2 or d in known_dom: continue
        feed = None
        for path in ("/feed", "/rss", "/feed.xml", "/rss.xml", "/blogs/news.atom"):
            try:
                r = requests.get(f"https://{d}{path}", headers=UA, timeout=12)
                if r.status_code == 200 and re.search(r"<(rss|feed)[\s>]", r.text[:3000]): feed = f"https://{d}{path}"; break
            except Exception: pass
        robots = "unknown"
        try:
            import urllib.robotparser as rp
            p = rp.RobotFileParser(); p.parse(requests.get(f"https://{d}/robots.txt", headers=UA, timeout=10).text.splitlines())
            robots = "allowed for /" if p.can_fetch("DropThePickleBot", f"https://{d}/") else "disallowed for /"
        except Exception: pass
        known_dom.add(d)
        add(dict(name=names[d], type="news", url=f"https://{d}/", audience=dict(value="unknown", metric="", source="not measured by discovery job (check Tranco)", as_of=TODAY),
                 feed=dict(rss=feed, api=None), scraping=dict(robots=robots, tos="not reviewed: headlines + links only", allowed_method="rss" if feed else "link only"),
                 note=f"appeared in Google News RSS pickleball results (score {n})"))

def podcasts():
    for term in ["pickleball", "pickleball podcast"]:
        try: res = get("https://itunes.apple.com/search", params=dict(media="podcast", term=term, limit=50)).json()["results"]
        except Exception as ex: print("itunes failed:", ex); continue
        for r in res:
            fu = r.get("feedUrl")
            if not fu or fu in known_feeds or (r.get("trackCount") or 0) < 10: continue
            known_feeds.add(fu)
            add(dict(name=r["collectionName"], type="podcast", url=r.get("collectionViewUrl", "").split("?")[0],
                     audience=dict(value="unknown", metric="", source="podcast platforms do not publish listener counts", episodes=r.get("trackCount"), as_of=TODAY),
                     feed=dict(rss=fu, api="iTunes Search API"), scraping=dict(robots="n/a", tos="public podcast RSS; link to episodes only", allowed_method="rss"),
                     note=f"by {r.get('artistName')}; last release {str(r.get('releaseDate',''))[:10]}"))

if __name__ == "__main__":
    key = os.environ.get("YT_API_KEY")
    steps = ([lambda: youtube_api(key)] if key else []) + [youtube_from_reddit, news_mentions, podcasts]
    for fn in steps:
        try: fn()
        except Exception as ex: print("step failed:", getattr(fn, "__name__", "youtube_api"), ex)
    reg["updated"] = TODAY
    F.write_text(json.dumps(reg, indent=1, ensure_ascii=False))
    print(f"added {len(added)} new candidates:"); [print(" -", a["type"], a["name"], a["url"]) for a in added]
