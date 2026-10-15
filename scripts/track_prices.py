#!/usr/bin/env python3
"""Daily price tracker: reads each paddle's price from its maker's own product page (Shopify product JSON at <url>.js),
only where robots.txt allows. Appends to data/price_history.json and flags drops.
 - drop: today's price is lower than the last different price we recorded
 - sale: maker shows a compare-at (was) price higher than today's price
Usage: python3 scripts/track_prices.py   (update.py runs it daily)"""
import json, pathlib, datetime, urllib.parse as up, urllib.robotparser as rp
import requests
R = pathlib.Path(__file__).parent.parent
UA = "DropThePickleBot"; H = {"User-Agent": f"Mozilla/5.0 (compatible; {UA}/1.0; daily price check; +https://dropthepickle.com/about.html)"}
TODAY = datetime.date.today().isoformat()
PD = json.loads((R / "data/paddles.json").read_text())
HF = R / "data/price_history.json"
hist = json.loads(HF.read_text()) if HF.exists() else {"paddles": {}}
robots = {}
def allowed(url):
    p = up.urlparse(url); base = f"{p.scheme}://{p.netloc}"
    if base not in robots:
        r = rp.RobotFileParser()
        try: r.parse(requests.get(base + "/robots.txt", headers=H, timeout=15).text.splitlines())
        except Exception: r = None
        robots[base] = r
    return bool(robots[base]) and robots[base].can_fetch(UA, url)
ok = skipped = failed = 0
for p in PD["paddles"]:
    key = f'{p["brand"]} {p["model"]}'
    rec = hist["paddles"].setdefault(key, {"source_url": p["source_url"], "currency": p["currency"], "history": []})
    js = p["source_url"].split("?")[0] + ".js"
    if not (allowed(js) and allowed(p["source_url"])):
        rec["status"] = "skipped: robots.txt disallows"; skipped += 1; continue
    try:
        j = requests.get(js, headers=H, timeout=20).json()
        price = round(j["price"] / 100, 2); was = j.get("compare_at_price")
        was = round(was / 100, 2) if was else None
        h = rec["history"]
        prev = next((x["price"] for x in reversed(h) if x["date"] != TODAY), None)
        h[:] = [x for x in h if x["date"] != TODAY] + [{"date": TODAY, "price": price, "compare_at": was, "available": j.get("available")}]
        img = j.get("featured_image") or ""
        img = ("https:" + img) if img.startswith("//") else img
        rec.update(image=img, current=price, compare_at=was, available=j.get("available"), checked=TODAY, status="ok",
                   previous=prev, drop=bool(prev and price < prev), sale=bool(was and was > price),
                   low=min(x["price"] for x in h))
        ok += 1
    except Exception as ex:
        rec["status"] = f"failed: {str(ex)[:80]}"; failed += 1
hist["updated"] = TODAY
HF.write_text(json.dumps(hist, indent=1, ensure_ascii=False))
print(f"prices: {ok} ok, {skipped} skipped by robots, {failed} failed; drops: {sum(v.get('drop',False) for v in hist['paddles'].values())}, on sale: {sum(v.get('sale',False) for v in hist['paddles'].values())}")
