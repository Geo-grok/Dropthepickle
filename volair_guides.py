"""Volair gap pages: guides/best-volair-paddles.html (by player type) and vs-volair-mach-2-forza-vs-volair-pro-1.html.

Facts only: model, shape, core, weight, face and price come from data/paddles.json (+ price_history.json current price).
Extra Mach 2 Forza / Pro 1 specs (length, width, swing/twist weight) are copied from volair.com product pages (SPEC_SRC).
Player-type groupings are spec rules or Volair's own product copy, never hands-on testing. No reviews, no ratings.
"""
import own_codes

CHECKED = "2026-10-25"  # date the volair.com specs below were read
SPEC_SRC = {
    "Mach 2 Forza": ("https://volair.com/products/mach-2-forza-pickleball-paddle", {
        "14mm": {"Average weight": "7.7 oz", "Length": "15.88 in", "Width": "8.12 in", "Handle length": "5.5 in", "Grip circumference": "4.15 in", "Swing weight": "108", "Twist weight": "6.99"},
        "16mm": {"Average weight": "8 oz", "Length": "15.88 in", "Width": "8.12 in", "Handle length": "5.5 in", "Grip circumference": "4.15 in", "Swing weight": "112", "Twist weight": "7.37"}},
        "Polypropylene honeycomb, foam walls", "T700 carbon fiber"),
    "Pro 1": ("https://volair.com/products/pro-1", {
        "14mm": {"Average weight": "7.8 oz", "Length": "16.35 in", "Width": "7.5 in", "Handle length": "5.5 in", "Grip circumference": "4.25 in", "Swing weight": "114", "Twist weight": "5.82"},
        "16mm": {"Average weight": "8.1 oz", "Length": "16.35 in", "Width": "7.5 in", "Handle length": "5.5 in", "Grip circumference": "4.3 in", "Swing weight": "120", "Twist weight": "6.09"}},
        "Polypropylene honeycomb", "Fiberglass"),
}

def _faq(qa): return [{"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]}]
def _faq_html(e, qa, h): return f"<h2>{e(h)}</h2>" + "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in qa)

def make(page, e, fmt, OWN, PD, H, paddle_slug):
    oc = OWN.get("Volair")
    pp = {p["model"]: p for p in PD["paddles"] if p["brand"] == "Volair"}
    if not pp: return
    def now(p): return H.get(f'Volair {p["model"]}', {}).get("current", p["price"])
    def usd(x): return f"${x:,.2f}"
    checked = max(p.get("checked", "") for p in pp.values())
    code_line = (f'<p class="meta vlink">Buying one? Our <a href="/discount-codes/volair"><b>Volair promo code</b></a> {e(oc["code"])} takes {e(oc["discount"])} at checkout on volair.com. '
                 f'<a href="/discount-codes/volair">How to use it and what it excludes →</a></p>') if oc else ""
    callout = own_codes.callout(e, oc, "../disclosure.html" , js=True, details=True) if oc else ""
    ex = [m for m, p in pp.items() if p.get("code_excluded")]

    # ---------- best Volair paddle guide ----------
    def pick(models): return [pp[m] for m in models if m in pp]
    groups = [
        ("Power", "Volair markets the Mach 2 Forza as \"engineered for commanding power\". The Mach Forzas use a T700 carbon fiber face; the 14mm option is the thinner, livelier core Volair describes as letting you \"all-out let it fly\".",
         pick(["Mach 2 Forza", "Mach 1 Forza"])),
        ("Control", "Volair's CTRL Forzas use an aramid fiber face that Volair describes as \"flexible and forgiving\" for control, on a 16mm core. Thicker cores are generally described as softer.",
         pick(["CTRL 2 Forza", "CTRL 1 Forza"])),
        ("All-court (hybrid shape)", "Hybrid shapes sit between widebody and elongated. These are the Volair models whose shape field reads hybrid.",
         [p for p in pp.values() if "hybrid" in (p.get("shape") or "").lower()]),
        ("Beginner and budget", "Our beginner rule: $200 or less with a 16mm option or a wider face. These are the lowest-priced Volair models that pass it. Volair's own Pro 1 copy says it's for players looking to upgrade their starter paddle.",
         sorted([p for p in pp.values() if now(p) <= 100 and "16mm" in p["core"]], key=lambda p: (now(p), p["model"]))),
    ]
    def row(p):
        note = f' <span class="meta">({e(p["note"])})</span>' if p.get("note") else ""
        exn = ' <span class="meta">(code may not apply)</span>' if p.get("code_excluded") else ""
        return (f'<tr><td><a href="../{paddle_slug(p)}">{e(p["model"])}</a>{note}{exn}</td><td>{e(p.get("shape") or "not listed")}</td><td>{e(p["core"])}</td>'
                f'<td>{e(p["weight"])}</td><td>{e(p["face"])}</td><td>{usd(now(p))}</td></tr>')
    thead = "<tr><th>Paddle</th><th>Shape</th><th>Core</th><th>Weight</th><th>Face</th><th>Price</th></tr>"
    secs = "".join(f'<h2>Best Volair paddle for {e(t.lower()) if not t.startswith("All") else "all-court play"}</h2><p>{e(why)}</p><div class="tbl"><table>{thead}{"".join(row(p) for p in ps)}</table></div>' for t, why, ps in groups if ps)
    lo, hi = min(map(now, pp.values())), max(map(now, pp.values()))
    gqa = [
        ("What is the best Volair paddle?", "It depends on how you play. Volair itself says it recommends the Mach 2 Forza 16mm for most players. For control, Volair markets the aramid-face CTRL Forzas. For a lower price, the Pro 1, Pro 2 and Mach 2 start at " + usd(min(now(p) for p in pick(["Pro 1", "Pro 2", "Mach 2"]) or pp.values())) + ". We group them by published specs, not by playtesting."),
        ("Which Volair paddle has the most power?", "Volair markets the Mach 2 Forza for power. Its 14mm version is the thinner core option. We haven't tested power ourselves."),
        ("Which Volair paddle is best for control?", "Volair markets the CTRL 1 and CTRL 2 Forza for control. Both use an aramid fiber face on a 16mm core."),
        ("Which Volair paddle is best for beginners?", "By our spec rule, the lower-priced 16mm options such as the Pro 1, Pro 2 and Mach 2 fit. Volair describes the Pro 1 as an upgrade from a starter paddle."),
        ("How much do Volair paddles cost?", f"The Volair paddles we track run {usd(lo)} to {usd(hi)} at our last check of volair.com ({fmt(checked)}), before any code."),
        ("Is there a Volair discount code?", f"Yes. Our code {oc['code']} takes {oc['discount']} at checkout on volair.com. Some licensed and excluded paddles don't take codes." if oc else "See our Volair discount codes page."),
    ]
    gbody = (f'<h1>Best Volair Paddle by Player Type ({CHECKED[:4]})</h1>'
             f'<p>Volair makes {len(pp)} paddles in our database. This guide sorts them by how you play: power, control, all-court and beginner. Every spec and price comes from volair.com (prices checked {fmt(checked)}). We group by published specs and Volair\'s own product descriptions. We have not playtested these paddles and this is not a ranking.</p>'
             f'{code_line}{secs}'
             f'<h2>Head to head</h2><p><a href="../vs-volair-mach-2-forza-vs-volair-pro-1.html">Volair Mach 2 Forza vs Pro 1: specs side by side →</a></p>'
             f'<h2>Volair promo code</h2>{callout}'
             f'{_faq_html(e, gqa, "Best Volair paddle FAQ")}'
             f'<p class="meta">More: <a href="/discount-codes/volair">Volair promo code</a> · <a href="../paddle-quiz.html">Paddle quiz</a> · <a href="../best-paddles-for-power.html">Best paddles for power</a> · <a href="../best-paddles-for-control.html">Best paddles for control</a> · <a href="../best-paddles-for-beginners.html">Best paddles for beginners</a> · <a href="../disclosure.html">Disclosure</a></p>')
    page("guides/best-volair-paddles.html", "Best Volair Paddle for Power, Control & Beginners (2026)", gbody,
         f"Best Volair paddle by player type: power, control, all-court, beginner. Real volair.com specs and prices ({usd(lo)}-{usd(hi)}), plus code {oc['code'] if oc else ''}."[:155],
         fresh={"volair": [(p["model"], now(p)) for p in pp.values()]}, schema=_faq(gqa), raw_title=True)

    # ---------- Mach 2 Forza vs Pro 1 ----------
    A, B = pp.get("Mach 2 Forza"), pp.get("Pro 1")
    if not (A and B): return
    ua, sa, ca, fa = SPEC_SRC["Mach 2 Forza"]; ub, sb, cb, fb = SPEC_SRC["Pro 1"]
    rows = [("Price (volair.com)", usd(now(A)), usd(now(B))), ("Shape", A["shape"], B["shape"]), ("Thickness options", A["core"], B["core"]),
            ("Face", fa, fb), ("Core", ca, cb)]
    for t in ("16mm", "14mm"):
        for k in sa[t]: rows.append((f"{k} ({t})", sa[t][k], sb[t][k]))
    tbl = ("<div class=\"tbl vs\"><table><tr><th></th>"
           f'<th><a href="{paddle_slug(A)}">Mach 2 Forza</a></th><th><a href="{paddle_slug(B)}">Pro 1</a></th></tr>'
           + "".join(f"<tr><td>{e(k)}</td><td>{e(a)}</td><td>{e(b)}</td></tr>" for k, a, b in rows) + "</table></div>")
    gap = now(A) - now(B)
    diffs = [f"The Mach 2 Forza costs {usd(gap)} more at our last check ({usd(now(A))} vs {usd(now(B))})." if gap > 0 else f"Both are {usd(now(A))} at our last check.",
             f"Face: the Mach 2 Forza uses {fa}; the Pro 1 uses {fb}.",
             f"Shape: the Mach 2 Forza is a widebody ({sa['16mm']['Width']} wide, {sa['16mm']['Length']} long); the Pro 1 is a hybrid ({sb['16mm']['Width']} wide, {sb['16mm']['Length']} long).",
             f"Volair lists a lower swing weight and a higher twist weight for the Mach 2 Forza (16mm: {sa['16mm']['Swing weight']} / {sa['16mm']['Twist weight']}) than the Pro 1 (16mm: {sb['16mm']['Swing weight']} / {sb['16mm']['Twist weight']}).",
             "Volair says it recommends the Mach 2 Forza 16mm for most players, and describes the Pro 1 as an upgrade from a starter paddle, with an elongated handle for two-handed backhands."]
    vqa = [
        ("What is the difference between the Volair Mach 2 Forza and Pro 1?", " ".join(diffs[:3])),
        ("Which is cheaper, the Mach 2 Forza or the Pro 1?", diffs[0]),
        ("Which has the bigger sweet spot?", f"We don't measure sweet spots. Volair lists a twist weight of {sa['16mm']['Twist weight']} for the Mach 2 Forza 16mm and {sb['16mm']['Twist weight']} for the Pro 1 16mm; a higher twist weight is generally described as more stable on off-center hits. Volair markets the Mach 2 Forza's wider shape for fewer mishits."),
        ("Do both come in 14mm and 16mm?", f"Yes. Volair lists both in 14mm and 16mm. Weights: Mach 2 Forza {A['weight']}; Pro 1 {B['weight']}."),
        ("Does the Volair promo code work on both?", f"Our code {oc['code']} takes {oc['discount']} at checkout on volair.com. Volair doesn't flag either paddle as excluded, but licensed art editions say codes don't apply. Check your total before you pay." if oc else "See our Volair discount codes page."),
    ]
    vbody = (f'<h1>Volair Mach 2 Forza vs Pro 1</h1>'
             f'<p>Volair\'s widebody Mach 2 Forza and hybrid Pro 1, side by side. Every number below is copied from volair.com (specs read {fmt(CHECKED)}, prices checked {fmt(checked)}). '
             f'This is a spec comparison, not a playtest, and we don\'t score either paddle. Sources: <a href="{ua}" target="_blank" rel="noopener">Mach 2 Forza on volair.com</a>, <a href="{ub}" target="_blank" rel="noopener">Pro 1 on volair.com</a>.</p>'
             f'{code_line}<h2>Specs side by side</h2>{tbl}<h2>Differences in the published specs</h2><ul>{"".join(f"<li>{e(d)}</li>" for d in diffs)}</ul>'
             f'<p><a class="btn" href="{paddle_slug(A)}">Mach 2 Forza full specs →</a> <a class="btn ghost" href="{paddle_slug(B)}">Pro 1 full specs →</a></p>'
             f'<h2>Volair promo code</h2>{own_codes.callout(e, oc, "disclosure.html", js=True, details=True) if oc else ""}'
             f'{_faq_html(e, vqa, "Mach 2 Forza vs Pro 1 FAQ")}'
             f'<p class="meta">More: <a href="guides/best-volair-paddles.html">Best Volair paddle by player type</a> · <a href="/discount-codes/volair">Volair promo code</a> · <a href="compare.html">Compare paddles</a> · <a href="disclosure.html">Disclosure</a></p>')
    page("vs-volair-mach-2-forza-vs-volair-pro-1.html", "Volair Mach 2 Forza vs Pro 1: Specs & Price Compared", vbody,
         f"Volair Mach 2 Forza vs Pro 1: shape, face, weight, swing and twist weight, and price ({usd(now(A))} vs {usd(now(B))}) from volair.com. Code {oc['code'] if oc else ''} for {oc['discount'] if oc else ''}."[:155],
         fresh={"vs": [(A["model"], now(A)), (B["model"], now(B))]}, schema=_faq(vqa), raw_title=True)
