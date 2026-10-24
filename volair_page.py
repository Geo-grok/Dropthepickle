"""Dedicated Volair promo-code page at /discount-codes/volair (dist/discount-codes/volair.html).

Replaces the generic per-brand code page for Volair only: leads with our own code (config.json OWN_CODES via
own_codes.callout), then a short lineup from data/paddles.json, an honest how-to FAQ, and the creator codes we track.
Stacking: Volair doesn't publish whether codes combine with sales or other codes, so we never claim they do.
Exclusions: Volair's ambassador page says licensed paddles are excluded; the V.1F isn't tagged as included in discounts.
"""
import own_codes

AMBASSADOR = "https://volair.com/pages/ambassador"
NOAPPLY = "Volair doesn't tag the V.1F paddle as included in its discounts, so the code may not apply to it. Check the total before you pay."

CSS = (".vhero{background:var(--navy);color:#fff;border-radius:var(--r);padding:20px 18px;margin:0 0 14px;box-shadow:var(--sh2)}"
       ".vhero h1{color:#fff;font-size:clamp(1.9rem,8vw,2.8rem);line-height:1.1;margin:.2rem 0 .6rem}.vhero h1 em{color:var(--neon);font-style:normal}"
       ".vhero>p{font-size:1.15rem;margin:.3rem 0;color:#dfe6f3}.vhero .owncode p,.vhero .owncode .ownhead{color:var(--navy)}.vhero .owncode .owndisc{color:#3d4a63}.vhero .owncode .owntag{color:var(--neon)}.vhero .owncode{margin-top:14px}"
       ".vline{display:grid;gap:12px;grid-template-columns:1fr;margin:10px 0}@media(min-width:720px){.vline{grid-template-columns:1fr 1fr}}"
       ".vrow{background:#fff;border:2px solid var(--line);border-left:8px solid var(--neon);border-radius:16px;padding:14px 16px}"
       ".vrow h3{font-size:1.3rem;margin:0 0 .2rem}.vrow h3 a{color:var(--navy)}.vrow .vp{font-size:1.35rem;font-weight:900;color:var(--navy);margin:.2rem 0}"
       ".vrow .vp s{font-weight:600;color:var(--mut);font-size:1rem;margin-left:.4rem}.vrow ul{margin:.3rem 0 .5rem;padding-left:1.1rem;font-size:1.05rem}"
       ".vrow .vnote{font-size:1rem;background:#fff3c4;border-radius:10px;padding:6px 10px;margin:.3rem 0}"
       ".vrow .vlinks{display:flex;flex-wrap:wrap;gap:8px;margin-top:.4rem}.vrow .vlinks a{font-weight:800;font-size:1.05rem}"
       ".vnext{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}")

def make(page, e, fmt, C, OWN, PD, H, go_slug, paddle_slug, cards, copyjs, crumbs, crumb_html, canon, fresh):
    oc = OWN.get("Volair")
    fn = "discount-codes/volair.html"
    pp = [p for p in PD["paddles"] if p["brand"] == "Volair"]
    def cur(p): return H.get(f'{p["brand"]} {p["model"]}', {})
    def usd(x): return f"${x:,.2f}"
    def row(p):
        h = cur(p); now = h.get("current", p["price"])
        was = f'<s>{usd(h["compare_at"])}</s>' if h.get("sale") and h.get("compare_at") else ""
        specs = [(k, p.get(f)) for k, f in (("Shape", "shape"), ("Core", "core"), ("Weight", "weight"), ("Face", "face"))]
        li = "".join(f"<li><b>{k}:</b> {e(v)}</li>" for k, v in specs if v)
        note = f'<p class="vnote">{e(p["note"])}</p>' if p.get("note") else ""
        if p.get("code_excluded"): note += f'<p class="vnote"><b>Heads up:</b> the code may not apply to this paddle. Check the total before you pay.</p>'
        go = "/go/" + go_slug(p["buy_url"])
        return (f'<div class="vrow"><h3><a href="../{paddle_slug(p)}">{e(p["model"])}</a></h3><div class="vp">{usd(now)}{was}</div><ul>{li}</ul>{note}'
                f'<div class="vlinks"><a href="../{paddle_slug(p)}">Full specs →</a><a href="{e(go)}" target="_blank" rel="sponsored nofollow noopener">Check price at Volair →</a></div></div>')
    checked = max([p.get("checked", "") for p in pp] or [""])
    lineup = (f'<h2>The Volair lineup</h2><p class="meta">Prices and specs from volair.com{", checked " + fmt(checked) if checked else ""}. Prices change, so confirm on Volair before you buy.</p>'
              f'<div class="vline">{"".join(row(p) for p in sorted(pp, key=lambda p: (p["price"], p["model"])))}</div>') if pp else ""
    how = (oc or {}).get("how") or "Type the code in the discount code box at checkout on volair.com and tap Apply."
    faq = [
        ("How do I use the Volair promo code?", f"Add your paddle to the cart on volair.com and go to checkout. {how}"),
        ("How much is the Volair paddle discount?", f"{oc['code']} takes {oc['discount']} at checkout on volair.com." if oc else "See the codes on this page."),
        ("Does the code work on every Volair paddle?", "Not always. Volair's ambassador program page says licensed paddles are excluded. Volair also doesn't tag the V.1F as included in its discounts, so the code may not apply to it. If the discount doesn't show at checkout, that item is excluded."),
        ("Can I combine it with a sale price or another code?", "Volair doesn't publish whether codes combine with sale prices or with each other. Check your cart total at checkout before you pay."),
        ("Does DropThePickle earn money from this code?", own_codes.earn_line(oc) if oc else "Some codes on this page are affiliate codes."),
    ]
    faq_html = "<h2>Volair promo code FAQ</h2>" + "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in faq)
    lead = own_codes.callout(e, oc, "../disclosure.html", note=NOAPPLY) if oc else ""
    body = (f'{crumb_html}<section class="vhero"><h1>Volair promo code &amp; paddle discount: <em>10% off</em></h1>'
            f'<p>Use our code at checkout on volair.com. Here\'s how it works, what it may not cover, and the current Volair paddles.</p>{lead}</section>'
            f'<p class="meta">Exclusions: per <a href="{AMBASSADOR}" target="_blank" rel="noopener">Volair\'s ambassador page</a>, licensed paddles are excluded. Volair doesn\'t publish whether codes stack.</p>'
            f'<div class="vnext"><a class="btn" href="../paddle-quiz.html">Not sure which Volair? Take the paddle quiz →</a><a class="btn ghost" href="/discount-codes">All discount codes →</a></div>'
            f'{lineup}{faq_html}'
            + (f'<h2>Other Volair codes we track</h2><p class="meta">Published by creators; each card links to its source. Many are affiliate codes, so the creator may earn a commission.</p><div class="grid">{cards}</div>' if cards else "")
            + f'<p class="meta"><a href="/discount-codes">All pickleball discount codes</a> · <a href="../paddle-quiz.html">Paddle quiz</a> · <a href="../deals.html">Paddle deals</a> · <a href="../disclosure.html">Disclosure</a></p>'
            + copyjs + own_codes.COPY_JS)
    title = "Volair Promo Code & Paddle Discount: 10% Off (DROPTHEPICKLE)" if oc else "Volair promo codes & paddle discounts"
    desc = ("Volair promo code DROPTHEPICKLE takes 10% off at checkout on volair.com. Volair paddle discount details, exclusions, "
            "how to apply it, and current Volair paddles with prices and specs.")
    schema = [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]
    page(fn, title, body, desc, fresh=fresh, schema=schema, crumbs=crumbs)
