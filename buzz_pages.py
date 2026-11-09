"""Pickleball Buzz: one page per story at /buzz/<date>-<slug>, plus the /buzz hub that links to them.

Data: data/buzz.json (hand-curated; update.py never writes it). Story URLs must not move when a headline is edited, so
the first slug issued for a story is kept in data/buzz_slugs.json, keyed by date + first source URL (falling back to the
title). That file only grows. Unknown /buzz/<x> URLs are sent to the hub by the Worker.
Stories whose summary is shorter than MIN_WORDS still get a page (the hub links to it) but are noindex and stay out of
the sitemap, as are items not marked confirmed.
"""
import json, re, pathlib
ROOT = pathlib.Path(__file__).parent
SLUGS = ROOT / "data" / "buzz_slugs.json"
MIN_WORDS = 60

def _key(b):
    src = next((s.get("url") for s in b.get("sources", []) if s.get("url")), "") or b.get("title", "")
    return f'{b.get("date", "")}|{src}'

def _slugify(b):
    words = re.sub(r"[^a-z0-9]+", " ", b["title"].lower().replace("'", "")).split()
    stop = {"a", "an", "the", "and", "of", "to", "in", "on", "for", "at", "is", "as", "with", "by", "from"}
    keep = [w for w in words if w not in stop][:8] or words[:8]
    return f'{b.get("date", "undated")}-' + "-".join(keep)

def assign_slugs(items):
    try: reg = json.loads(SLUGS.read_text())
    except Exception: reg = {}
    used = set(reg.values()); out = []
    for b in items:
        k = _key(b); s = reg.get(k)
        if not s:
            base = _slugify(b); s = base; n = 2
            while s in used: s = f"{base}-{n}"; n += 1
            reg[k] = s; used.add(s)
        out.append(s)
    if len(set(out)) != len(out):  # two items sharing a key: give the later ones their own slug
        seen = set()
        for i, s in enumerate(out):
            if s in seen:
                base = _slugify(items[i]); s2 = base; n = 2
                while s2 in used: s2 = f"{base}-{n}"; n += 1
                out[i] = s2; used.add(s2)
            seen.add(out[i])
    SLUGS.write_text(json.dumps(reg, indent=1, sort_keys=True, ensure_ascii=False) + "\n")
    return out

def excerpt(text, limit=220):
    first = re.split(r"(?<=[.!?])\s+", text.strip(), maxsplit=1)[0]
    if len(first) <= limit: return first
    return text[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "…"

def describe(text, limit=155):
    t = re.sub(r"\s+", " ", text).strip()
    return t if len(t) <= limit else t[:limit].rsplit(" ", 1)[0].rstrip(",;:.") + "…"

def make(page, e, fmt, C, B, *, nudge, NUDGEJS, XLAZY, SIGNUP_TITLE, SIGNUP_BLURB, holiday_note, canon):
    items = B.get("items", [])
    slugs = assign_slugs(items)
    base = C["BASE_URL"].rstrip("/")
    def fn_of(s): return f"buzz/{s}.html"
    def sbadge(b): return '<span class="tag b-unconf">⚠ Unconfirmed</span>' if b.get("status") != "confirmed" else '<span class="tag b-conf">Confirmed</span>'
    def indexable(b): return b.get("status") == "confirmed" and len(b.get("summary", "").split()) >= MIN_WORDS
    def tcard(b, s, *, rel=""):
        """Hub/teaser card: headline links to the story page; no embeds, no source list (those live on the story page)."""
        return (f'<div class="card buzzcard"><div class="pub">{sbadge(b)}</div><h3><a href="{rel}buzz/{s}">{e(b["title"])}</a></h3>'
                f'<div class="meta"><time datetime="{e(b.get("date", ""))}">{fmt(b.get("date"))}</time></div><p>{e(excerpt(b["summary"]))}</p>'
                f'<p class="watch"><a href="{rel}buzz/{s}">Read the story and sources →</a></p></div>')
    teaser = (f'<h2>Pickleball Buzz <a class="seemore" href="buzz.html">All buzz →</a></h2><div class="grid">'
              + "".join(tcard(b, s) for b, s in list(zip(items, slugs))[:3]) + '</div>') if items else ""
    # story pages
    for i, (b, s) in enumerate(zip(items, slugs)):
        fn = fn_of(s); url = canon(fn)
        srcs = "".join(f'<li><a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["label"])}</a></li>' for x in b.get("sources", []))
        emb = "".join(f'<blockquote class="twitter-tweet" data-dnt="true"><a href="{e(u)}">View post on X</a></blockquote>' for u in b.get("embeds", []))
        if b.get("video_id"): emb += f'<div class="vid"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{e(b["video_id"])}" title="{e(b["title"])}" allowfullscreen></iframe></div>'
        tags = " ".join(f'<span class="tag">{e(t)}</span>' for t in b.get("tags", []))
        links = "".join(f'<p class="watch"><a href="{e(l["href"])}">{e(l["label"])} →</a></p>' for l in b.get("links", []))
        mine = set(b.get("tags", []))
        rel = [(x, xs) for x, xs in zip(items, slugs) if xs != s and mine & set(x.get("tags", []))][:4]
        if len(rel) < 4: rel += [(x, xs) for x, xs in zip(items, slugs) if xs != s and (x, xs) not in rel][:4 - len(rel)]
        more = "".join(f'<li><a href="{e(xs)}">{e(x["title"])}</a> <span class="meta">({fmt(x.get("date"))})</span></li>' for x, xs in rel)
        paras = "".join(f"<p>{e(p)}</p>" for p in re.split(r"\n\s*\n", b["summary"].strip()) if p.strip())
        body = (f'<article><nav class="crumbs" aria-label="Breadcrumb"><a href="../index.html">Home</a> › <a href="../buzz.html">Buzz</a> › <span>Story</span></nav>'
                f'<h1>{e(b["title"])}</h1><p class="meta">Pickleball Buzz · <time datetime="{e(b.get("date", ""))}">{fmt(b.get("date"))}</time> · {sbadge(b)} {tags}</p>'
                f'{paras}{links}<h2>Sources</h2><ul class="srcs">{srcs or "<li>No source recorded.</li>"}</ul>'
                f'{f"<div class={chr(34)}buzzx{chr(34)}>{emb}</div>" if emb else ""}'
                f'<p class="meta">DropThePickle summarizes what the linked sources report. Items marked Unconfirmed have no official confirmation.</p>'
                f'<h2>More from Pickleball Buzz</h2><ul>{more}</ul><p><a href="../buzz.html">All Pickleball Buzz stories →</a></p></article>'
                f'{XLAZY if b.get("embeds") else ""}')
        art = {"@type": "NewsArticle", "headline": b["title"][:110], "datePublished": b.get("date"), "description": describe(b["summary"]),
               "url": url, "mainEntityOfPage": url, "image": [base + "/og-1200x630.png"],
               "author": {"@type": "Organization", "name": C["SITE_NAME"], "url": base + "/"},
               "publisher": {"@id": base + "/#organization"},
               "isBasedOn": [x["url"] for x in b.get("sources", []) if x.get("url")]}
        if b.get("tags"): art["keywords"] = ", ".join(b["tags"])
        crumbs = [{"name": "Home", "url": base + "/"}, {"name": "Pickleball Buzz", "url": canon("buzz.html")}, {"name": b["title"], "url": url}]
        page(fn, b["title"], body, describe(b["summary"]),
             fresh={k: b.get(k) for k in ("title", "summary", "status", "date", "sources", "embeds", "links", "tags", "video_id")},
             schema=[art], crumbs=crumbs, noindex=not indexable(b))
    # hub
    il = {"@type": "ItemList", "name": "Pickleball Buzz stories", "numberOfItems": len(items), "itemListElement": [
        {"@type": "ListItem", "position": i, "url": canon(fn_of(s)), "name": b["title"]} for i, (b, s) in enumerate(zip(items, slugs), 1)]}
    page("buzz.html", B.get("seo_title") or "Pickleball Buzz",
         f'<h1>Pickleball Buzz</h1><p class="meta">What the pickleball world is talking about (updated {e(B.get("updated", ""))}). Each story has its own page with its sources and any official posts. Items marked <b>Unconfirmed</b> are rumors or chatter with no official confirmation.</p>'
         f'{nudge("buzz", "buzz", SIGNUP_TITLE, SIGNUP_BLURB)}{holiday_note("buzz")}<div class="grid">{"".join(tcard(b, s) for b, s in zip(items, slugs)) or "<p>No buzz right now.</p>"}</div>'
         f'{nudge("buzz-bottom", "buzzb", "Like the buzz? Get codes by email", SIGNUP_BLURB)}{NUDGEJS}',
         B.get("seo_desc") or "Pickleball Buzz: what the pickleball world is talking about, with confirmed stories and clearly labeled rumors, each linked to its sources.",
         raw_title=bool(B.get("seo_title")), schema=[il],
         fresh={"items": [(b.get("title"), b.get("status"), b.get("date"), s) for b, s in zip(items, slugs)]})
    return teaser, {"stories": len(items), "indexed": sum(1 for b in items if indexable(b))}
