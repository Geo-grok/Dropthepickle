"""Seasonal shopping pages: guides/pickleball-gift-guide-2026.html and deals/black-friday-pickleball-deals-2026.html.

Facts only: every price comes from data/paddles.json + data/price_history.json (maker-page checks, date shown next to it),
codes from data/discount-codes.json and config.json OWN_CODES. No invented items, prices, sales or dates. Budget tiers
that the data can't fill say so instead of padding. Not a playtest ranking.
"""
import json, pathlib, re
import own_codes
from paddle_pages import slug, cores, money, price_checked

GIFT_FN = "guides/pickleball-gift-guide-2026.html"
BF_FN = "deals/black-friday-pickleball-deals-2026.html"
BF_DAY, CM_DAY = "2026-11-27", "2026-11-30"
# Brand pages checked 2026-10-29 for officially published Black Friday 2026 details. None carried a 2026 date.
BF_CHECKED = "2026-10-29"
BF_WATCH = [("Selkirk", "https://www.selkirk.com/collections/black-friday-deals", "Selkirk runs a Black Friday collection page. It shows no 2026 dates, so we don't treat its prices as this year's sale."),
            ("Volair", "https://volair.com/collections/sale", "Volair's sale page shows no Black Friday dates."),
            ("CRBN", "https://crbnpickleball.com/", "CRBN's most recent Black Friday page we found is for 2025. No 2026 sale published.")]

# Contextual holiday callout for high-traffic pages (paddle reviews, code pages, Buzz, how-to-watch).
# Absolute extensionless hrefs (urls.clean_path), so it works at any directory depth. Max two holiday links per box.
from urls import clean_path
GIFT_URL, BF_URL = "/" + clean_path(GIFT_FN), "/" + clean_path(BF_FN)
CSS = (".holi{background:#fff;border:2px solid var(--line);border-left:8px solid var(--neon);border-radius:16px;padding:12px 14px;margin:14px 0}"
       ".holi p{margin:0 0 .4rem;font-size:1.02rem}.holi .holia{display:inline-flex;align-items:center;min-height:44px;padding:.5rem .2rem;margin-right:1rem;font-weight:800;color:var(--navy)}")
HOLI = {
    "paddle": ("Buying a paddle as a gift?", [(GIFT_URL, "See our 2026 gift guide by budget →"), (BF_URL, "Tracking Black Friday paddle sales →")]),
    "codes": ("Waiting for Black Friday paddle sales?", [(BF_URL, "Our hub tracks which paddle brands have announced 2026 sales →")]),
    "buzz": ("Shopping for a pickleball player?", [(GIFT_URL, "Paddle gifts by budget: 2026 gift guide →"), (BF_URL, "Black Friday paddle deals hub →")]),
    "watch": ("Got a pickleball fan on your gift list?", [(GIFT_URL, "See our 2026 paddle gift guide by budget →")]),
}
def holiday_note(kind):
    lead, links = HOLI[kind]
    return f'<aside class="holi" aria-label="Holiday paddle deals"><p><b>{lead}</b></p>' + "".join(f'<a class="holia" href="{u}">{t}</a>' for u, t in links) + "</aside>"

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
    # Under-$25 non-paddle gifts: data/gift-under-25.json (each price read on the brand's own product page, date per item).
    G25 = json.loads((pathlib.Path(__file__).parent / "data/gift-under-25.json").read_text())["items"]
    G25 = sorted(G25, key=lambda g: (g["price_usd"], g["brand"], g["name"]))
    def g25row(g):
        own = g["brand"] in OWN and g.get("dtp_code")
        rel = "sponsored noopener" if own else "noopener"
        note = f'<br><span class="meta">{e(g["price_note"])}</span>' if g.get("price_note") else ""
        code = f'<br><span class="meta">Code {e(OWN[g["brand"]]["code"])}: {e(OWN[g["brand"]]["discount"])}</span>' if own else ""
        return (f'<tr><td><b>{e(g["name"])}</b><br><span class="meta">{e(g["brand"])} · {e(g["category"])}. {e(g["blurb"])}</span></td>'
                f'<td><b>${g["price_usd"]:.2f}</b>{note}<br><span class="meta">{price_checked(g["date_checked"], fmt, e, label="Checked")}</span>{code}</td>'
                f'<td><a href="{e(g["product_url"])}" target="_blank" rel="{rel}">{e(g["brand"])} store</a></td></tr>')
    s1 = ('<p>Small gifts and stocking stuffers, each priced on the brand\'s own store on the date shown (before shipping and tax). '
          + (f'The Volair items take our code {e(vol["code"])} for {e(vol["discount"])}. ' if vol else "")
          + 'Want a paddle near this price? See our <a href="pickleball-paddles-under-30.html">paddles under $30</a> guide.</p>'
          '<div class="tbl"><table><tr><th>Gift</th><th>Brand price</th><th>Where to buy</th></tr>' + "".join(g25row(g) for g in G25) + "</table></div>")
    thin3 = f'<p class="meta">Only {len(t3)} paddle{"s" if len(t3) != 1 else ""} in our data sit in this range, so it\'s a short list.</p>' if len(t3) < 3 else ""
    picks = [("../best-paddles-for-beginners.html", "Best paddles for beginners"), ("../best-paddles-for-power.html", "Best paddles for power"),
             ("../best-paddles-for-control.html", "Best paddles for control"), ("../best-paddles-for-tennis-players.html", "Best paddles for tennis players"),
             ("../best-16mm-paddles.html", "Best 16mm paddles"), ("../best-elongated-paddles.html", "Best elongated paddles"),
             ("best-volair-paddles.html", "Best Volair paddle by player type"), ("best-paddles-under-100.html", "Best paddles under $100"),
             ("pickleball-paddles-under-30.html", "Pickleball paddles under $30")]
    pick_lis = "".join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in picks)
    gqa = [
        ("What is a good pickleball gift under $25?", f"Accessories: we list {len(G25)} items from ${G25[0]['price_usd']:.2f} to ${G25[-1]['price_usd']:.2f}, including overgrips, edge guard tape, paddle covers, balls and a CRBN eGift card, each priced on the brand's own store (checked {fmt(max(g['date_checked'] for g in G25))})."),
        ("What is a good pickleball gift for a beginner?", "A paddle that fits our beginner rule: $200 or less with a 16mm core option or a wider face." + (f" The lowest-priced one in our data is the {lo['brand']} {lo['model']} at {money(lo, cur(lo))} (checked {fmt(chk(lo))})." if lo else "")),
        ("How much should I spend on a pickleball paddle gift?", f"The paddles we track run {money(usd[0], cur(usd[0]))} to {money(usd[-1], cur(usd[-1]))} at the maker's site. {len(t2) + len(t3)} of them are $100 or less." if usd else "See our paddle database for current prices."),
        ("Are these prices current?", f"Each price was read on the maker's own product page on the date shown next to it (latest check {fmt(last)}). Prices change, so confirm at checkout."),
        ("Is there a discount code I can use?", (f"Yes for Volair: our code {vol['code']} takes {vol['discount']} at checkout on volair.com. " if vol else "") + "Other brands' codes are on our discount codes page, re-checked daily."),
        ("Should I wait for Black Friday?", f"Black Friday is November 27, 2026 and Cyber Monday is November 30. Our Black Friday hub tracks current prices so you can tell if a sale price is really lower."),
    ]
    def faq(qa, h="Gift guide FAQ"): return f"<h2>{e(h)}</h2>" + "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qa)
    def faq_ld(qa): return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}
    listed = t1 + t2 + t3 + t4
    gbody = (f'<h1>Pickleball Gift Guide 2026</h1>{DISC}'
             f'<p class="meta">Gifts sorted by budget, using only prices we checked on each maker\'s own site. {price_checked(last, fmt, e)} We have not playtested these paddles and this is not a ranking.</p>'
             f'<p class="meta"><a href="../deals.html"><b>Paddle deals →</b></a> · <a href="../{BF_FN}"><b>Black Friday pickleball deals 2026 →</b></a> · <a href="/discount-codes"><b>Discount codes →</b></a></p>'
             f'<h2>Under $25</h2>{s1}'
             f'<h2>$25 to $75</h2>{table(t2, "../") if t2 else "<p>No items in our price data in this range right now.</p>"}'
             f'<h2>$75 to $100</h2>{thin3}{table(t3, "../") if t3 else "<p>No items in our price data in this range right now.</p>"}'
             f'<h2>$100 and up</h2><p class="meta">{len(t4)} paddles, lowest price first.' + (f' Six Zero ({len(aud)} paddles) prices in AUD only, so they are on the <a href="../price-index.html">price index</a> instead.' if aud else "") + f'</p>{table(t4, "../")}'
             f'<h2>Beginner gifts</h2><p>Our beginner rule: $200 or less, plus a 16mm core option or a wider or hybrid face. These are the {len(beg)} lowest-priced paddles that pass it. New players will also like <a href="pickleball-rules-for-beginners.html">rules for beginners</a> and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a>.</p>{table(beg, "../")}'
             f'<h2>Paddle picks by player</h2><p>Know how they play? These spec-filter lists narrow it down.</p><ul>{pick_lis}</ul>'
             f'<h2>Save with codes</h2><p>Codes can stack on a gift budget. See every code on our <a href="/discount-codes">pickleball discount codes</a> page, re-checked daily. For the brands in this guide:</p><ul>{code_lis}</ul>{vcall}'
             f'{faq(gqa)}'
             f'<p class="meta">More: <a href="../deals.html">Deals</a> · <a href="../price-tracker.html">Price tracker</a> · <a href="../price-index.html">Price index</a> · <a href="../paddle-quiz.html">Paddle quiz</a> · <a href="../disclosure.html">Disclosure</a></p>')
    gdesc = "Pickleball gifts by budget for 2026: stocking stuffers under $25, paddles from $49.99 to $100+, beginner picks, dated prices and verified codes."
    def item_list(ps, _il=item_list):  # gift-guide list also carries the under-$25 accessories
        d = _il(ps)
        if ps is listed:
            extra = [{"@type": "ListItem", "position": 0, "name": g["name"], "url": g["product_url"], "item": {"@type": "Product", "name": g["name"], "brand": {"@type": "Brand", "name": g["brand"]},
                      "offers": {"@type": "Offer", "price": f'{g["price_usd"]:.2f}', "priceCurrency": "USD", "url": g["product_url"]}}} for g in G25]
            els = extra + d["itemListElement"]
            for i, x in enumerate(els, 1): x["position"] = i
            d = {**d, "numberOfItems": len(els), "itemListElement": els}
        return d
    page(GIFT_FN, "Pickleball Gift Guide 2026: Gifts by Budget", gbody, gdesc[:155],
         fresh={"items": [(p["brand"], p["model"], cur(p), chk(p)) for p in listed + beg], "faq": gqa},
         schema=[{**item_list(listed), "name": "Pickleball Gift Guide 2026"}, faq_ld(gqa)], raw_title=True)

    # ---------------- Black Friday hub ----------------
    sale = [p for p in usd if ph(p).get("sale") or ph(p).get("drop")]
    def lowrow(p):
        h = ph(p); low = h.get("low")
        return (f'<tr><td><a href="../{slug(p)}"><b>{e(p["brand"])}</b> {e(p["model"])}</a></td><td><b>{money(p, cur(p))}</b>'
                + (f' <s class="meta">{money(p, h["compare_at"])}</s>' if h.get("sale") and h.get("compare_at") else "")
                + f'<br><span class="meta">{stamp(p)}</span></td><td>{money(p, low) if low else "not recorded"}</td><td>{buy(p)}</td></tr>')
    lowtbl = ('<div class="tbl"><table><tr><th>Paddle</th><th>Price now</th><th>Lowest we\'ve recorded</th><th>Where to buy</th></tr>'
              + "".join(lowrow(p) for p in sale) + "</table></div>") if sale else "<p>No paddles were below the maker's compare-at price or our last recorded price at our latest check.</p>"
    watch = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(b)}</a>: {e(t)}</li>' for b, u, t in BF_WATCH)
    bqa = [
        ("When is Black Friday 2026?", "Black Friday is Friday, November 27, 2026. Cyber Monday is Monday, November 30, 2026."),
        ("Have pickleball brands announced Black Friday 2026 sales?", f"Not that we could confirm as of {fmt(BF_CHECKED)}. None of the brand pages we checked shows a dated 2026 Black Friday sale. We'll update this page as brands publish details."),
        ("How do I know if a Black Friday paddle deal is real?", "Compare the sale price with our price tracker and price index. Each paddle page shows the lowest price we've recorded on the maker's site, so you can see if a 'deal' is really lower."),
        ("Which paddles are on sale right now?", f"At our latest check, {len(sale)} paddle{'s were' if len(sale) != 1 else ' was'} below the maker's compare-at price or our last recorded price. They're listed on this page with the date we checked."),
        ("Is there a pickleball discount code for Black Friday?", (f"Our Volair code {vol['code']} takes {vol['discount']} at checkout on volair.com today. " if vol else "") + "Brands often limit codes on sale items, so check your cart total. All tracked codes are on our discount codes page."),
        ("Should I buy now or wait?", "If a paddle is already at the lowest price we've recorded, waiting may not save more. Brands haven't published 2026 Black Friday prices yet, so nobody can promise a deeper cut."),
    ]
    under100 = t2 + t3
    bbody = (f'<h1>Black Friday Pickleball Deals 2026</h1>{DISC}'
             f'<p class="meta">Black Friday is {fmt(BF_DAY)} and Cyber Monday is {fmt(CM_DAY)}. This is our hub for both: current verified prices and codes now, and we\'ll update it as brands announce sales. {price_checked(last, fmt, e)}</p>'
             f'<h2>Has any brand announced its 2026 sale?</h2><p>Not yet, as far as we could confirm on {fmt(BF_CHECKED)}. We only list a sale once the brand publishes it. Pages we\'re watching:</p><ul>{watch}</ul>'
             f'<h2>Is that deal real? Check before you buy</h2><p>Brands raise and cut prices all year. Before you trust a "Black Friday" price, compare it with our numbers:</p>'
             f'<ul><li><a href="../price-tracker.html"><b>Paddle Price Tracker</b></a>: popular paddles with "% off list", checked on each brand\'s own page.</li>'
             f'<li><a href="../price-index.html"><b>Paddle Price Index</b></a>: every maker price we\'ve recorded.</li>'
             f'<li>Each paddle page shows the lowest price we\'ve seen.</li></ul>'
             f'<h2>On sale at our last check</h2>{lowtbl}'
             f'<h2>Paddles $100 and under right now</h2>{table(under100, "../") if under100 else "<p>None at our last check.</p>"}'
             f'<h2>Codes you can use now</h2><p>Most brands allow one code per order and may exclude sale items, so check the total before you pay. Every tracked code is on <a href="/discount-codes">pickleball discount codes</a>.</p>{vcall}'
             f'<h2>Shopping for someone else?</h2><p>See our <a href="../{GIFT_FN}">Pickleball Gift Guide 2026</a>, sorted by budget.</p>'
             f'{faq(bqa, "Black Friday FAQ")}'
             f'<p class="meta">More: <a href="../deals.html">All paddle deals</a> · <a href="../guides/best-volair-paddles.html">Best Volair paddles</a> · <a href="../guides/best-paddles-under-100.html">Best paddles under $100</a> · <a href="../disclosure.html">Disclosure</a></p>')
    bdesc = "Black Friday (Nov 27) and Cyber Monday (Nov 30) 2026 pickleball deals hub: dated paddle prices, working codes, and a price tracker to spot fake sales."
    blist = sale + [p for p in under100 if p not in sale]
    base = absu("index.html")
    page(BF_FN, "Black Friday Pickleball Deals 2026: Prices & Codes", bbody, bdesc[:155],
         fresh={"sale": [(p["brand"], p["model"], cur(p), chk(p)) for p in blist], "faq": bqa, "watch": BF_WATCH},
         schema=[{**item_list(blist), "name": "Black Friday pickleball deals 2026"}, faq_ld(bqa)], raw_title=True,
         crumbs=[{"name": "Home", "url": base}, {"name": "Deals", "url": absu("deals.html")}, {"name": "Black Friday Pickleball Deals 2026", "url": absu(BF_FN)}])
