"""Seasonal shopping pages: guides/pickleball-gift-guide-2026.html.

Facts only: every price comes from data/paddles.json + data/price_history.json (maker-page checks, date shown next to it),
codes from data/discount-codes.json and config.json OWN_CODES. No invented items, prices, sales or dates. Budget tiers
that the data can't fill say so instead of padding. Not a playtest ranking.
"""
import json, pathlib, re
import own_codes
from paddle_pages import slug, cores, money, price_checked

GIFT_FN = "guides/pickleball-gift-guide-2026.html"

def _slugb(b): return re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")

def make(page, e, fmt, PP, cur, ph, buy, OWN, item_list, absu):
    DC = json.loads((pathlib.Path(__file__).parent / "data/discount-codes.json").read_text())
    codes = DC.get("codes", [])
    usd = [p for p in PP if p["currency"] == "USD" and ph(p).get("available") is not False]
    usd.sort(key=lambda p: (cur(p), p["brand"], p["model"]))
    aud = [p for p in PP if p["currency"] != "USD"]
    def chk(p): return ph(p).get("checked") or ""
    def stamp(p, pre=""): return price_checked(chk(p), fmt, e, label="Checked")
    def row(p, pre=""):
        h = ph(p); was = f' <s class="meta">{money(p, h["compare_at"])}</s>' if h.get("sale") and h.get("compare_at") else ""
        spec = " · ".join(x for x in [p["core"], p["shape"]] if x) or "specs not published"
        return (f'<tr><td><a href="{pre}{slug(p)}"><b>{e(p["brand"])}</b> {e(p["model"])}</a><br><span class="meta">{e(spec)}</span></td>'
                f'<td><b>{money(p, cur(p))}</b>{was}<br><span class="meta">{stamp(p)}</span></td><td>{buy(p)}</td></tr>')
    def table(ps, pre=""):
        return ('<div class="tbl"><table><tr><th>Gift</th><th>Maker price</th><th>Where to buy</th></tr>'
                + "".join(row(p, pre) for p in ps) + "</table></div>")
    t1 = [p for p in usd if cur(p) < 25]
    t2 = [p for p in usd if 25 <= cur(p) < 75]
    t3 = [p for p in usd if 75 <= cur(p) <= 100]
    t4 = [p for p in usd if cur(p) > 100]
    beg = [p for p in usd if cur(p) <= 200 and (16.0 in cores(p) or any(w in (p.get("shape") or "").lower() for w in ("widebody", "hybrid", "max")))][:6]
    last = max((chk(p) for p in usd), default="")
    lo = usd[0] if usd else None
    vol = OWN.get("Volair")
    # brand code pages for brands in the guide with tracked codes
    gb = sorted({p["brand"] for p in usd}, key=str.lower)
    def best_disc(b):
        cs = [c for c in codes if c["brand"] == b]
        if not cs: return None
        pct = [int(m.group(1)) for c in cs for m in [re.search(r"(\d+)%", c["discount"])] if m]
        return len(cs), (f"up to {max(pct)}% off" if pct else cs[0]["discount"]), max(c.get("verified") or "" for c in cs)
    code_lis = ""
    for b in gb:
        if b in OWN:
            oc = OWN[b]; code_lis += f'<li><a href="/discount-codes/{_slugb(b)}"><b>{e(b)} promo code</b></a>: our own code {e(oc["code"])} takes {e(oc["discount"])} at checkout.</li>'
            continue
        d = best_disc(b)
        if d: code_lis += f'<li><a href="/discount-codes/{_slugb(b)}"><b>{e(b)} codes</b></a>: {d[0]} tracked code{"s" if d[0] != 1 else ""}, {e(d[1])}, last checked {fmt(d[2])}.</li>'
        else: code_lis += f'<li><a href="/discount-codes/{_slugb(b)}"><b>{e(b)}</b></a>: no working code at our last check.</li>'
    vcall = own_codes.callout(e, vol, "../disclosure.html", js=True, details=True) if vol else ""
    DISC = '<p class="disc">Some links are affiliate links. We may earn a commission at no extra cost to you. <a href="../disclosure.html">Learn more</a>.</p>'

    # ---------------- Gift guide ----------------
    if t1: s1 = table(t1, "../")
    else: s1 = ('<p>None yet. No paddle or item in our price data is under $25 right now, and we don\'t list prices we haven\'t checked. '
                'The cheapest thing we have confirmed on a retailer page is a 2-paddle beginner set in our <a href="pickleball-paddles-under-30.html">paddles under $30</a> guide. '
                'A gift that costs nothing extra: send them our <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a> with a card.</p>')
    thin3 = f'<p class="meta">Only {len(t3)} paddle{"s" if len(t3) != 1 else ""} in our data sit in this range, so it\'s a short list.</p>' if len(t3) < 3 else ""
    picks = [("../best-paddles-for-beginners.html", "Best paddles for beginners"), ("../best-paddles-for-power.html", "Best paddles for power"),
             ("../best-paddles-for-control.html", "Best paddles for control"), ("../best-paddles-for-tennis-players.html", "Best paddles for tennis players"),
             ("../best-16mm-paddles.html", "Best 16mm paddles"), ("../best-elongated-paddles.html", "Best elongated paddles"),
             ("best-volair-paddles.html", "Best Volair paddle by player type"), ("best-paddles-under-100.html", "Best paddles under $100"),
             ("pickleball-paddles-under-30.html", "Pickleball paddles under $30")]
    pick_lis = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in picks)
    gqa = [
        ("What is a good pickleball gift under $25?", "We don't have a verified price on any item under $25 right now, so we don't recommend one. The cheapest item we've confirmed is a 2-paddle beginner set in our paddles under $30 guide."),
        ("What is a good pickleball gift for a beginner?", "A paddle that fits our beginner rule: $200 or less with a 16mm core option or a wider face." + (f" The lowest-priced one in our data is the {lo['brand']} {lo['model']} at {money(lo, cur(lo))} (checked {fmt(chk(lo))})." if lo else "")),
        ("How much should I spend on a pickleball paddle gift?", f"The paddles we track run {money(usd[0], cur(usd[0]))} to {money(usd[-1], cur(usd[-1]))} at the maker's site. {len(t2) + len(t3)} of them are $100 or less." if usd else "See our paddle database for current prices."),
        ("Are these prices current?", f"Each price was read on the maker's own product page on the date shown next to it (latest check {fmt(last)}). Prices change, so confirm at checkout."),
        ("Is there a discount code I can use?", (f"Yes for Volair: our code {vol['code']} takes {vol['discount']} at checkout on volair.com. " if vol else "") + "Other brands' codes are on our discount codes page, re-checked daily."),
        ("Should I wait for Black Friday?", f"Black Friday is November 27, 2026 and Cyber Monday is November 30. Compare any sale price with our price tracker before you buy, so you can tell if it is really lower."),
    ]
    def faq(qa, h="Gift guide FAQ"): return f"<h2>{e(h)}</h2>" + "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qa)
    def faq_ld(qa): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    listed = t1 + t2 + t3 + t4
    gbody = (f'<h1>Pickleball Gift Guide 2026</h1>{DISC}'
             f'<p class="meta">Gifts sorted by budget, using only prices we checked on each maker\'s own site. {price_checked(last, fmt, e)} We have not playtested these paddles and this is not a ranking.</p>'
             f'<p class="meta"><a href="../deals.html"><b>Paddle deals →</b></a> · <a href="/discount-codes"><b>Discount codes →</b></a></p>'
             f'<h2>Under $25</h2>{s1}'
             f'<h2>$25 to $75</h2>{table(t2, "../") if t2 else "<p>No items in our price data in this range right now.</p>"}'
             f'<h2>$75 to $100</h2>{thin3}{table(t3, "../") if t3 else "<p>No items in our price data in this range right now.</p>"}'
             f'<h2>$100 and up</h2><p class="meta">{len(t4)} paddles, lowest price first.' + (f' Six Zero ({len(aud)} paddles) prices in AUD only, so they are on the <a href="../price-index.html">price index</a> instead.' if aud else "") + f'</p>{table(t4, "../")}'
             f'<h2>Beginner gifts</h2><p>Our beginner rule: $200 or less, plus a 16mm core option or a wider or hybrid face. These are the {len(beg)} lowest-priced paddles that pass it. New players will also like <a href="pickleball-rules-for-beginners.html">rules for beginners</a> and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a>.</p>{table(beg, "../")}'
             f'<h2>Paddle picks by player</h2><p>Know how they play? These spec-filter lists narrow it down.</p><ul>{pick_lis}</ul>'
             f'<h2>Save with codes</h2><p>Codes can stack on a gift budget. See every code on our <a href="/discount-codes">pickleball discount codes</a> page, re-checked daily. For the brands in this guide:</p><ul>{code_lis}</ul>{vcall}'
             f'{faq(gqa)}'
             f'<p class="meta">More: <a href="../deals.html">Deals</a> · <a href="../price-tracker.html">Price tracker</a> · <a href="../price-index.html">Price index</a> · <a href="../paddle-quiz.html">Paddle quiz</a> · <a href="../disclosure.html">Disclosure</a></p>')
    gdesc = f"Pickleball gifts by budget for 2026: $25-75, $75-100 and $100+ paddles with dated maker prices, beginner picks, and verified discount codes."
    page(GIFT_FN, "Pickleball Gift Guide 2026: Gifts by Budget", gbody, gdesc[:155],
         fresh={"items": [(p["brand"], p["model"], cur(p), chk(p)) for p in listed + beg], "faq": gqa},
         schema=[{**item_list(listed), "name": "Pickleball Gift Guide 2026"}, faq_ld(gqa)], raw_title=True)
