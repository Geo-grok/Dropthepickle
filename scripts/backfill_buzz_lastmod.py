#!/usr/bin/env python3
"""One-time backfill of real content-change dates for the /buzz/<slug> story pages in data/page_dates.json.

Why: the story pages were split out of /buzz on 2026-11-09, so every story counted as a brand-new page and got
lastmod = 2026-11-09, even stories from October. A story page's content is its data/buzz.json item, so its real
lastmod is the last commit (America/Chicago date) that changed that item's page fields, found from git history.

Items are matched across commits by the same key buzz_pages.py uses for slugs (date + first source URL, with the
duplicate-key rule). Entries are written without "v", so build.py keeps these dates and re-baselines the hashes.
Run once, then build: python3 scripts/backfill_buzz_lastmod.py && python3 build.py
"""
import json, subprocess, pathlib, hashlib, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from buzz_pages import _key, _dup_key
FIELDS = ("title", "summary", "status", "date", "sources", "embeds", "links", "tags", "video_id")  # = buzz_pages fresh
def git(*a): return subprocess.check_output(["git", "-C", str(ROOT), *a], text=True, env={"TZ": "America/Chicago", "PATH": "/usr/bin:/bin"})
def keys(items):
    out, seen_base, ks = [], set(), []
    for b in items:
        base = _key(b); k = base if base not in seen_base else _dup_key(b); n = 2
        while k in ks: k = f"{_dup_key(b)}|{n}"; n += 1
        seen_base.add(base); ks.append(k); out.append((k, b))
    return out
def main():
    store = json.loads((ROOT / "data/page_dates.json").read_text())
    slugs = json.loads((ROOT / "data/buzz_slugs.json").read_text())
    log = git("log", "--reverse", "--date=format-local:%Y-%m-%d", "--format=%H %ad", "--", "data/buzz.json")
    last, prev = {}, {}
    for line in log.splitlines():
        sha, day = line.split()
        try: items = json.loads(git("show", f"{sha}:data/buzz.json")).get("items", [])
        except Exception: continue
        for k, b in keys(items):
            h = hashlib.sha256(json.dumps({f: b.get(f) for f in FIELDS}, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
            if prev.get(k) != h: last[k] = day; prev[k] = h
    n = 0
    for k, day in sorted(last.items()):
        fn = f"buzz/{slugs[k]}.html" if k in slugs else None
        if fn in store and store[fn].get("updated") != day:
            print(f"{fn}: {store[fn].get('updated')} -> {day}")
            store[fn] = {"hash": store[fn]["hash"], "updated": day}; n += 1
    (ROOT / "data/page_dates.json").write_text(json.dumps(store, indent=1, sort_keys=True) + "\n")
    print(f"{n} buzz story dates restored")
if __name__ == "__main__": main()
