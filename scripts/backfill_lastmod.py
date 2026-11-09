#!/usr/bin/env python3
"""One-time backfill of real content-change dates into data/page_dates.json (run once, before the first FRESH_V=2 build).

Why: until Nov 2026 the per-brand discount-code payload included the daily "verified" stamp, so ~100 code pages showed
lastmod = build day every day, and ~80 pages had no lastmod at all. This script records an honest date per page from git:

* discount-codes/<brand>: the last commit (America/Chicago date) where that brand's codes changed in
  data/discount-codes.json, ignoring the daily "verified" field.
* pages with no recorded date: the commit date when the page's current content hash first appeared in
  data/page_dates.json (the hash has not changed since, so neither has the content).
* stub pages that had no freshness payload: the last commit that changed their source text (listed in STUBS).

Entries are written without "v", so build.py keeps these dates and re-baselines the hashes under the new payload format.
"""
import json, subprocess, pathlib, collections
ROOT = pathlib.Path(__file__).resolve().parent.parent
def git(*a): return subprocess.check_output(["git", "-C", str(ROOT), *a], text=True, env={"TZ": "America/Chicago", "PATH": "/usr/bin:/bin"})
def commits(path):  # oldest first: (sha, CT date)
    out = git("log", "--reverse", "--date=format-local:%Y-%m-%d", "--format=%H %ad", "--", path)
    return [tuple(l.split()) for l in out.splitlines() if l.strip()]
def at(sha, path):
    try: return json.loads(git("show", f"{sha}:{path}"))
    except Exception: return None
def slugb(b):
    import re; return re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")
STUBS = {  # fn -> source snippets; date = newest commit that added/removed any of them (git log -S)
    "shop.html": ["Coming soon 👕"],
    "community.html": ["Used-paddle marketplace"],
    "guides.html": ['page("guides.html"'],
    "disclosure.html": ["Sponsored placements are clearly labeled", "OWN_CODES"],
}
def main():
    store = json.loads((ROOT / "data/page_dates.json").read_text())
    log = []
    # 1) brand code pages from discount-codes.json history
    last = {}; prev = {}
    for sha, day in commits("data/discount-codes.json"):
        d = at(sha, "data/discount-codes.json") or {}
        cur = collections.defaultdict(list)
        for c in d.get("codes", []): cur[c["brand"]].append((c.get("code"), c.get("discount"), c.get("conditions"), c.get("source_url")))
        for b in set(cur) | set(prev):
            v = sorted(cur.get(b, []))
            if prev.get(b) != v: last[b] = day
            prev[b] = v
    hist = [(day, at(sha, "data/page_dates.json") or {}) for sha, day in commits("data/page_dates.json")]
    born = {}
    for day, snap in hist:
        for fn in snap: born.setdefault(fn, day)
    own = {}
    for o in (json.loads((ROOT / "config.json").read_text()).get("OWN_CODES") or []):
        if isinstance(o, dict) and o.get("brand") and o.get("approved"): own[o["brand"]] = o["approved"][:10]
    for b in own: last[b] = max(last.get(b, ""), own[b])
    for b, day in list(last.items()):
        fn = f"discount-codes/{slugb(b)}.html"
        day = max(day, born.get(fn, day))  # never earlier than the page itself
        if fn in store and store[fn].get("updated") != day:
            log.append((fn, store[fn].get("updated"), day)); store[fn] = {"hash": store[fn]["hash"], "updated": day}
    # 2) pages without a date: first commit where the current hash appeared
    for fn, ent in store.items():
        if ent.get("updated"): continue
        since = None
        for day, snap in hist:
            h = (snap.get(fn) or {}).get("hash")
            if h == ent["hash"]:
                if since is None: since = day
            else: since = None
        if since: log.append((fn, None, since)); ent["updated"] = since
    # 3) stub pages with no payload before
    for fn, snippets in STUBS.items():
        days = []
        for sn in snippets:
            out = git("log", "-1", "--date=format-local:%Y-%m-%d", "--format=%ad", "-S", sn, "--", "build.py", "content_pages.py", "config.json").strip()
            if out: days.append(out)
        if days and not (store.get(fn) or {}).get("updated"):
            store[fn] = {"hash": "", "updated": max(days)}; log.append((fn, None, max(days)))
    (ROOT / "data/page_dates.json").write_text(json.dumps(store, indent=1, sort_keys=True) + "\n")
    for fn, a, b in sorted(log): print(f"{fn}: {a} -> {b}")
    print(f"{len(log)} dates backfilled")
if __name__ == "__main__": main()
