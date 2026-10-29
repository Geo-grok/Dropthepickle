#!/usr/bin/env python3
"""Keep data/price-tracker.json in sync with data/price_history.json (the maker-page checks track_prices.py records).

For each tracker row (matched to price_history by product URL), take the newest history entry. That entry only
exists because track_prices.py read the price that day, so it is a verified price. Rules:
 - Only rows with a newer verified entry change: current_price, list_price (compare-at, or current when none),
   pct_off and checked (= the history entry's date). A row with no newer check keeps its old price and date.
 - An entry marked unavailable (out of stock) is not used: the tracker lists in-stock prices only.
 - Currency comes from price_history (Six Zero stays AUD). A currency mismatch is never synced; it is reported.
 - The file's "updated" date = the OLDEST row "checked" date, so the page never claims a check that didn't happen.
 - Big moves (>= 40% below the previous tracker price) are synced, since the maker page says so, but are printed
   as warnings (and ::warning in GitHub Actions) for a human to eyeball.
Usage: python3 scripts/sync_tracker.py [--check]   (--check: report only, write nothing; exit 1 if out of sync)
track_prices.py runs this after every price check, so the daily refresh updates both files in the same step."""
import json, os, pathlib, sys
R = pathlib.Path(__file__).parent.parent
TF, HF = R / "data/price-tracker.json", R / "data/price_history.json"
BIG = 0.40

def pct(cur, lst): return int((lst - cur) / lst * 100 + 0.5) if lst and lst > cur else 0
def norm(u): return (u or "").split("?")[0].rstrip("/").lower()

def sync(tracker, hist):
    """Mutates tracker; returns (changes, warnings)."""
    by = {norm(v.get("source_url")): v for v in hist.get("paddles", {}).values()}
    changes, warns = [], []
    for r in tracker["rows"]:
        v = by.get(norm(r["url"]))
        if not v: warns.append(f"{r['paddle']}: no price_history entry, row left as is"); continue
        if v.get("currency") != r["currency"]:
            warns.append(f"{r['paddle']}: currency {r['currency']} vs history {v.get('currency')}, not synced"); continue
        ok = [x for x in v.get("history", []) if isinstance(x.get("price"), (int, float)) and x.get("available") is not False]
        if not ok: continue
        last = ok[-1]
        if last["date"] <= r["checked"]: continue  # nothing newer was verified
        lst = last["compare_at"] if last.get("compare_at") and last["compare_at"] > last["price"] else last["price"]
        old = (r["current_price"], r["list_price"], r["checked"])
        if last["price"] != r["current_price"]:
            changes.append(f"{r['paddle']}: {r['currency']} {r['current_price']:.2f} -> {last['price']:.2f} (list {lst:.2f}, checked {last['date']})")
            if r["current_price"] and last["price"] <= r["current_price"] * (1 - BIG):
                warns.append(f"BIG DROP {r['paddle']}: {r['current_price']:.2f} -> {last['price']:.2f} ({pct(last['price'], r['current_price'])}% below the last tracker price). Eyeball {r['url']}")
        r.update(current_price=last["price"], list_price=lst, pct_off=pct(last["price"], lst), checked=last["date"])
    if tracker["rows"]: tracker["updated"] = min(r["checked"] for r in tracker["rows"])
    return changes, warns

def main():
    check = "--check" in sys.argv
    t, h = json.loads(TF.read_text()), json.loads(HF.read_text())
    before = json.dumps(t, sort_keys=True)
    changes, warns = sync(t, h)
    gh = os.environ.get("GITHUB_ACTIONS") == "true"
    for w in warns: print(("::warning title=Price tracker::" if gh else "WARNING tracker: ") + w)
    for c in changes: print("tracker price change: " + c)
    dirty = json.dumps(t, sort_keys=True) != before
    if check:
        print("price-tracker.json is " + ("OUT OF SYNC with price_history.json (run scripts/sync_tracker.py)" if dirty else "in sync"))
        return 1 if dirty else 0
    if dirty:
        t["note"] = ("Each row's price comes from the newest check of the brand's own product page recorded in price_history.json "
                     "(Shopify product data on the retailer's domain); 'checked' is that check's date and 'updated' is the oldest row's date. "
                     "Lowest in-stock variant price. list_price = the page's compare-at price, or the current price when none is shown. "
                     "Six Zero prices are AUD.")
        TF.write_text(json.dumps(t, indent=1, ensure_ascii=False) + "\n")
    print(f"tracker: {len(changes)} price changes, updated {t['updated']}")
    return 0

if __name__ == "__main__": sys.exit(main())
