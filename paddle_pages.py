"""Paddle detail, comparison, best-of, deals and pro-paddle pages. Specs/prices come only from data/paddles.json
(maker pages) and data/price_history.json (maker-page price checks). Pros/cons are our own spec-based notes, never test results."""
import re, json, pathlib
ROOT = pathlib.Path(__file__).parent
def slug(p): return "paddle-" + re.sub(r"[^a-z0-9]+", "-", f'{p["brand"]} {p["model"]}'.lower().replace("¹","1").replace("³","3")).strip("-") + ".html"
def cores(p): return [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*mm", p["core"])]
def weights(p): return [float(x) for x in re.findall(r"(\d\.\d+)", p["weight"])]
GENERIC = {"pro","v","elongated","power","control","hybrid","series","air","edition","dual","the","slk","labs","project","gen-3","(gen-3)","m1","2026","14mm","16mm","(infinigrit)","(durable","grit)","3s","crbn¹","crbn³","x","x2","8e","c","era","omni","ruby"}
KEYS = {"X2 Elongated": [r"engage x2\b"], "OMNI": [r"selkirk omni|\bomni\b"], "SLK ERA Power": [r"\bera power\b|slk era"], "Ruby": [r"six ?zero ruby|\bruby\b"], "Pressure X 8E": [r"pressure ?x"],
        "CRBN¹ X Series": [r"crbn ?1? ?x series|crbn x\b"], "GX2 Power Hybrid": [r"gx2"], "GBX Power Elongated (Gen-3)": [r"gbx"]}
def keys(p):
    if p["model"] in KEYS: return KEYS[p["model"]]
    words = [w for w in re.split(r"\s+", p["model"]) if w.lower() not in GENERIC and len(w) > 2]
    return [re.escape(" ".join(words[:2])).replace(r"\ ", r"\s*")] if words else []
def videos(p, R):
    ks = keys(p); out = []
    for v in R.get("all_items") or R.get("items", []):
        if ks and any(re.search(k, v["title"], re.I) for k in ks): out.append(v)
    return out[:6]
def money(p, amt=None):
    a = p["price"] if amt is None else amt
    return ("$" if p["currency"] == "USD" else "A$") + f"{a:,.2f}"
FRESH_DAYS = 2   # "(checked recently)" only while the newest price check is this many calendar days old or less
STALE_DAYS = 7   # past this, add "Prices may have changed since then."
STALE_NOTE = " Prices may have changed since then."
# Runs in the visitor's browser against the real current date, so a page that never gets rebuilt or redeployed stops
# claiming freshness on its own. Every price-date stamp is <span class="pchk" data-checked="YYYY-MM-DD">.
# Age = whole calendar days between the check date and the visitor's local today.
# Without JS the static text is just the plain date (plus "(checked recently)" only if fresh at build time).
FRESHJS = ("<script>(function(){var n=new Date(),t=Date.UTC(n.getFullYear(),n.getMonth(),n.getDate());"
           "document.querySelectorAll('.pchk[data-checked]').forEach(function(el){"
           "var m=/^(\\d{4})-(\\d{2})-(\\d{2})$/.exec(el.getAttribute('data-checked')||''),"
           "a=m?Math.round((t-Date.UTC(+m[1],m[2]-1,+m[3]))/864e5):NaN;"
           "if(!(a>=0&&a<=%d))el.querySelectorAll('.pfresh').forEach(function(x){x.remove()});"
           "if(a>%d&&!el.querySelector('.pstale')){var s=document.createElement('span');s.className='pstale';s.textContent=%s;el.appendChild(s)}"
           "})})()</script>") % (FRESH_DAYS, STALE_DAYS, json.dumps(STALE_NOTE))
def price_age(iso):
    import datetime
    try: return (datetime.date.today() - datetime.date.fromisoformat(str(iso)[:10])).days
    except Exception: return None
def price_checked(iso, fmt, e, html=True, label="Prices last checked"):
    """'<label> <date>.' Build adds ' (checked recently)' only when the date is <= FRESH_DAYS old and
    ' Prices may have changed since then.' when it is > STALE_DAYS old. FRESHJS re-checks both in the browser.
    Never says 'today'."""
    if not iso: return "Price check date not recorded."
    d = str(iso)[:10]; age = price_age(d)
    if not html: return f"{label} {fmt(d)}." + (STALE_NOTE if age is not None and age > STALE_DAYS else "")
    soft = '<span class="pfresh"> (checked recently)</span>' if age is not None and 0 <= age <= FRESH_DAYS else ""
    stale = f'<span class="pstale">{STALE_NOTE}</span>' if age is not None and age > STALE_DAYS else ""
    return f'<span class="pchk" data-checked="{e(d)}">{label} <time datetime="{e(d)}">{fmt(d)}</time>{soft}.{stale}</span>'
def notes(p, ph):
    """Spec-based pros/cons in our own words. General characteristics only; no performance claims."""
    pro, con = [], []
    c, w, s, m = cores(p), weights(p), p["shape"].lower(), p["model"].lower()
    if len(set(c)) > 1: pro.append(f"Comes in more than one core thickness ({p['core']}), so you can pick the feel you prefer.")
    if c and max(c) >= 16: pro.append("A 16mm+ core option. Thicker cores are generally described as softer and more control-friendly.")
    if c and min(c) <= 14.3: pro.append("A thinner core option. Thinner cores are generally associated with a crisper, poppier response.")
    if "elongated" in s: pro.append("Elongated shape gives extra reach and leverage on serves and drives."); con.append("Elongated faces are narrower, so off-center hits on the sides are less forgiving.")
    if "widebody" in s or "hybrid" in s or "max" in s: pro.append("Wider or hybrid face options give a larger hitting area side to side.")
    if w and max(w) >= 8.2: pro.append("Heavier spec (up to %.1f oz) adds mass behind the ball." % max(w)); con.append("The heavier end of the range can feel slower in fast hand battles.")
    if w and min(w) <= 7.8: pro.append("Lighter spec (from %.1f oz) favors quick hands at the kitchen." % min(w))
    if not w: con.append("The maker doesn't publish a weight on its product page.")
    if not p["shape"]: con.append("The maker doesn't clearly state the shape on its product page.")
    if "power" in m: pro.append("The maker positions this model for power.")
    if "control" in m: pro.append("The maker positions this model for control.")
    if p["currency"] != "USD": con.append("Priced in AUD on the maker's site. Shipping and exchange costs for US buyers vary.")
    if p["currency"] == "USD" and p["price"] <= 130: pro.append(f"Budget-friendly list price ({money(p)}).")
    if p["currency"] == "USD" and p["price"] >= 280: con.append(f"Premium list price ({money(p)}).")
    if ph.get("sale"): pro.append(f"At our last check, below the maker's compare-at price ({money(p, ph['compare_at'])}).")
    if ph.get("available") is False: con.append("Shown as unavailable on the maker's site at our last check.")
    return pro or ["Nothing stands out from the published specs alone."], con or ["No obvious spec drawbacks. Watch the linked reviews for on-court impressions."]
def badge(ph, p=None):
    b = ""
    if ph.get("drop"): b += '<span class="tag b-drop">⬇ Price drop</span> '
    if ph.get("sale"): b += '<span class="tag b-sale">Sale</span> '
    if p is not None:
        if "power" in p["model"].lower() or p["model"] in ("Pressure X 8E", "LABS Project Boomstik", "Cannon XPP M1"): b += '<span class="tag b-power">Power</span> '
        if "control" in p["model"].lower(): b += '<span class="tag b-control">Control</span> '
    if ph.get("available") is False: b += '<span class="tag b-out">Unavailable</span>'
    return b
def make(page, e, fmt, buy, D, C, PD, R, P, X=None):
    X = X or {}
    import own_codes; OWN = own_codes.own_codes(C)  # our own affiliate codes (config.json OWN_CODES)
    NOAPPLY = "Volair doesn't tag this paddle as included in its discounts, so the code may not apply to it. Check the total before you pay."
    def owncall(p, js=True): return own_codes.callout(e, OWN[p["brand"]], js=js, note=NOAPPLY if p.get("code_excluded") else "") if p["brand"] in OWN else ""
    H = D("price_history.json").get("paddles", {})
    ph = lambda p: H.get(f'{p["brand"]} {p["model"]}', {})
    cur = lambda p: ph(p).get("current", p["price"])
    pros = P.get("pros", [])
    def img(p, cls="", w=600, eager=False, hi=False):
        # w: pixel width asked from the maker's Shopify CDN (sized to the slot, ~2.4x for phones).
        # eager/hi: for above-the-fold images, skip lazy-loading so the main picture paints sooner (LCP).
        u = ph(p).get("image")
        load = ('fetchpriority="high" ' if hi else "") + ("" if eager else 'loading="lazy" decoding="async" ')
        if u: return f'<img {load}src="{e(u + ("&" if "?" in u else "?") + f"width={w}")}" alt="{e(p["brand"])} {e(p["model"])} (image: {e(p["brand"])})">'
        return X.get("PADDLE_SVG", "")
    def credit(p): return f'<span class="credit">Image: {e(p["brand"])}</span>' if ph(p).get("image") else ""
    def pcard(p, why="", own=False):
        h = ph(p); was = f'<s>{money(p, h["compare_at"])}</s>' if h.get("sale") else ""
        return f'<div class="card pcard"><a class="pimg" href="{slug(p)}">{img(p)}<span class="badges">{badge(h, p)}</span>{credit(p)}</a><div class="body"><span class="brand">{e(p["brand"])}</span><h3><a href="{slug(p)}">{e(p["model"])}</a></h3><div class="meta">{" · ".join(x for x in [p["core"], p["shape"], p["weight"]] if x)}</div><div class="pp">{money(p, cur(p))}{was}</div>{f"<p class={chr(34)}meta{chr(34)}>{e(why)}</p>" if why else ""}{owncall(p, js=False) if own else ""}<div class="meta" style="margin-top:auto">{buy(p)}</div></div></div>' 
    PP = PD["paddles"]; by = {p["model"]: p for p in PP}
    base = C["BASE_URL"].rstrip("/")
    def absu(fn): return base + "/" if fn == "index.html" else base + "/" + fn
    def fresh_p(p):
        h = ph(p)
        return {"brand": p["brand"], "model": p["model"], "weight": p["weight"], "core": p["core"], "shape": p["shape"],
                "list": p["price"], "currency": p["currency"], "current": h.get("current"), "compare_at": h.get("compare_at"),
                "available": h.get("available"), "sale": h.get("sale"), "drop": h.get("drop"), "low": h.get("low"),
                "previous": h.get("previous"), "image": h.get("image") or ""}
    def product_node(p):
        h = ph(p)
        node = {"@type": "Product", "name": f'{p["brand"]} {p["model"]}', "brand": {"@type": "Brand", "name": p["brand"]},
                "category": "Pickleball paddle", "sku": slug(p)[:-5], "url": absu(slug(p)),
                "description": f'{p["brand"]} {p["model"]} pickleball paddle. Maker-listed weight: {p["weight"] or "not published"}. Core: {p["core"] or "not published"}. Shape: {p["shape"] or "not published"}.',
                "offers": {"@type": "Offer", "url": p["buy_url"], "priceCurrency": p["currency"], "price": f"{cur(p):.2f}",
                           "availability": "https://schema.org/OutOfStock" if h.get("available") is False else "https://schema.org/InStock",
                           "itemCondition": "https://schema.org/NewCondition"}}
        if h.get("image"): node["image"] = h["image"]
        return node
    def item_list(ps):
        return {"@type": "ItemList", "numberOfItems": len(ps), "itemListElement": [
            {"@type": "ListItem", "position": i, "name": f'{p["brand"]} {p["model"]}', "url": absu(slug(p)), "item": product_node(p)}
            for i, p in enumerate(ps, 1)]}
    DISC = '<p class="disc">Some links are affiliate links. We may earn a commission at no extra cost to you. <a href="disclosure.html">Learn more</a>.</p>'
    SRC = f'<p class="meta">Specs and list prices come from the maker\'s own product page (retrieved {e(PD["retrieved"])}). The current price comes from our latest check of the maker page (date shown above). Pros and cons are our own notes based on published specs. They are not lab or on-court test results.</p>'
    def pro_users(p):
        ks = keys(p); return [x for x in pros if x.get("paddle") and x["paddle"].lower().startswith(p["brand"].lower().split()[0]) and ks and any(re.search(k, x["paddle"], re.I) for k in ks)]
    def pricecell(p):
        h = ph(p); s = f'<b>{money(p, cur(p))}</b>'
        if h.get("compare_at") and h.get("sale"): s += f' <s class="meta">{money(p, h["compare_at"])}</s>'
        return s + " " + badge(h)
    def vlist(p):
        vs = videos(p, R)
        if not vs: return '<p class="meta">No matching reviewer videos in our feeds yet. They refresh daily.</p>'
        return "<ul>" + "".join(f'<li><a href="{e(v["link"])}" target="_blank" rel="noopener">{e(v["title"])}</a> <span class="meta">({e(v["channel"])}, {fmt(v["date"])})</span></li>' for v in vs) + "</ul>"
    EXTRA = [("face", "Face"), ("core_material", "Core material"), ("length", "Length"), ("width", "Width"), ("handle", "Handle"), ("grip", "Grip circumference"), ("swing_weight", "Swing weight"), ("twist_weight", "Twist weight"), ("note", "Note")]
    def specs(p): return f'<table><tr><th scope="row">Weight</th><td>{e(p["weight"]) or "not published"}</td></tr><tr><th scope="row">Core</th><td>{e(p["core"]) or "not published"}</td></tr><tr><th scope="row">Shape</th><td>{e(p["shape"]) or "not published"}</td></tr>{"".join(f'<tr><th scope="row">{lab}</th><td>{e(p[k])}</td></tr>' for k, lab in EXTRA if p.get(k))}<tr><th scope="row">List price</th><td>{money(p)}</td></tr><tr><th scope="row">Latest price</th><td>{pricecell(p)}</td></tr></table>'
    def pc(p):
        a, b = notes(p, ph(p)); return f'<div class="grid proscons"><div class="card"><h3>👍 Pros</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in a)}</ul></div><div class="card"><h3>👎 Cons</h3><ul>{"".join(f"<li>{e(x)}</li>" for x in b)}</ul></div></div>'
    # paddle detail pages
    for p in PP:
        users = pro_users(p)
        pu = ("<h2>Pros who use it</h2><ul>" + "".join(f'<li><a href="{e(x["profile"])}" target="_blank" rel="noopener">{e(x["name"])}</a> ({e(x["paddle"])}, per PPA profile)</li>' for x in users) + "</ul>") if users else ""
        h = ph(p); was = f'<s>{money(p, h["compare_at"])}</s>' if h.get("sale") else ""
        hero = f'<section class="phero"><div class="img" style="position:relative">{img(p, eager=True, hi=True)}{credit(p)}</div><div><span class="eyebrow"><i></i>{e(p["brand"])}</span><h1>{e(p["model"])}</h1><p>{badge(h, p)}</p><div class="price">{money(p, cur(p))}{was}</div><p class="meta">{price_checked(h.get("checked",""), fmt, e, label="Maker price checked")} Lowest we\'ve seen: {money(p, h.get("low", cur(p)))}.</p><div class="ctas"><a class="btn" href="{e(p["buy_url"])}" rel="sponsored nofollow noopener" target="_blank">Check price at {e(p["brand"])} →</a><a class="btn ghost" href="compare.html">Compare</a></div>{owncall(p)}<p class="meta">Where to buy: {buy(p)} · <a href="{e(p["source_url"])}" target="_blank" rel="noopener">Maker spec page</a></p></div></section>'
        page(slug(p), f'{p["brand"]} {p["model"]}', f'{hero}{DISC}{SRC}<h2>Specs</h2><div class="tbl">{specs(p)}</div><h2>Pros & cons (from the specs)</h2>{pc(p)}{pu}<h2>Reviewer videos</h2>{vlist(p)}<p><a href="compare.html">Compare paddles →</a></p>',
             f'{p["brand"]} {p["model"]} specs, maker price and links to independent reviewer videos. No DropThePickle rating.',
             fresh=fresh_p(p), schema=[product_node(p)], image=ph(p).get("image") or None)
    # comparisons: same brand, plus one cross-brand pair per brand combo that shares an elongated shape
    def shape_bucket(p):
        s = (p.get("shape") or "").lower()
        if "elongated" in s: return "elongated"
        if "hybrid" in s: return "hybrid"
        if "widebody" in s or "max" in s: return "wide"
        return ""
    def pair_key(a, b):
        x, y = sorted((a, b), key=lambda p: (p["brand"].lower(), p["model"].lower()))
        return (x["brand"], x["model"], y["brand"], y["model"])
    vs_pairs, seen_pairs = [], set()
    def add_pair(a, b):
        if a is b: return
        k = pair_key(a, b)
        if k in seen_pairs: return
        seen_pairs.add(k)
        left, right = (a, b) if (a["brand"], a["model"]) == (k[0], k[1]) else (b, a)
        vs_pairs.append((left, right))
    by_brand = {}
    for p in PP: by_brand.setdefault(p["brand"], []).append(p)
    for brand in sorted(by_brand):
        group = sorted(by_brand[brand], key=lambda p: p["model"].lower())
        for i in range(len(group)):
            for j in range(i + 1, len(group)): add_pair(group[i], group[j])
    elong = {}
    for p in PP:
        if shape_bucket(p) == "elongated": elong.setdefault(p["brand"], []).append(p)
    elong_brands = sorted(elong)
    for i in range(len(elong_brands)):
        for j in range(i + 1, len(elong_brands)):
            a = sorted(elong[elong_brands[i]], key=lambda p: p["model"].lower())[0]
            b = sorted(elong[elong_brands[j]], key=lambda p: p["model"].lower())[0]
            add_pair(a, b)
    if len(vs_pairs) > 70: vs_pairs = vs_pairs[:70]
    vs_links = []
    for A, B in vs_pairs:
        fn = "vs-" + slug(A)[7:-5] + "-vs-" + slug(B)[7:-5] + ".html"; t = f'{A["brand"]} {A["model"]} vs {B["brand"]} {B["model"]}'
        def win(k, A=A, B=B):
            if k == "Latest price" and A["currency"] == B["currency"] and cur(A) != cur(B): return "A" if cur(A) < cur(B) else "B"
            if k == "List price" and A["currency"] == B["currency"] and A["price"] != B["price"]: return "A" if A["price"] < B["price"] else "B"
            if k == "Core" and len(cores(A)) != len(cores(B)) and cores(A) and cores(B): return "A" if len(set(cores(A))) > len(set(cores(B))) else "B"
            return ""
        rows = "".join(f'<tr><th scope="row">{k}</th><td class="{"win" if win(k)=="A" else ""}">{f(A)}</td><td class="{"win" if win(k)=="B" else ""}">{f(B)}</td></tr>' for k, f in [("Weight", lambda p: e(p["weight"]) or "not published"), ("Core", lambda p: e(p["core"]) or "not published"), ("Shape", lambda p: e(p["shape"]) or "not published"), ("List price", money), ("Latest price", pricecell), ("Buy", buy)])
        diff = []
        ca, cb = cores(A), cores(B)
        if ca and cb and set(ca) != set(cb): diff.append(f'Core options differ: {A["model"]} lists {A["core"]}; {B["model"]} lists {B["core"]}.')
        if (A.get("shape") or "") != (B.get("shape") or ""): diff.append(f'Shape field: {A["model"]} is {A["shape"] or "not stated"}; {B["model"]} is {B["shape"] or "not stated"}.')
        if A["currency"] == B["currency"] and cur(A) != cur(B): lo, hi = (A, B) if cur(A) < cur(B) else (B, A); diff.append(f'{lo["model"]} is {money(lo, abs(cur(A) - cur(B)))} lower at the latest checked maker price than {hi["model"]}.')
        if A["weight"] == B["weight"] and A["weight"]: diff.append("The published weight text is identical.")
        same = []
        if A["brand"] == B["brand"]: same.append(f'same brand ({A["brand"]})')
        if shape_bucket(A) and shape_bucket(A) == shape_bucket(B): same.append(f'shape field includes {shape_bucket(A)}')
        vh = f'<section class="pagehead"><span class="eyebrow"><i></i>Head to head</span><h1 style="margin-top:.7rem">{e(t)}</h1><div class="vshead"><div><a class="vsimg" href="{slug(A)}">{img(A)}</a><h3>{e(A["model"])}</h3><div class="price" style="font-size:1.6rem">{money(A, cur(A))}</div></div><div class="vsbadge">VS</div><div><a class="vsimg" href="{slug(B)}">{img(B)}</a><h3>{e(B["model"])}</h3><div class="price" style="font-size:1.6rem">{money(B, cur(B))}</div></div></div></section>'
        body = f'{vh}{DISC}{SRC}<p class="meta">Same-category pair ({"; ".join(same) or "shared spec fields"}). Highlighted cells are the lower maker price or more listed core thicknesses. That is not a performance ranking.</p><h2>Specs side by side</h2><div class="tbl vs"><table><tr><th></th><th><a href="{slug(A)}">{e(A["model"])}</a></th><th><a href="{slug(B)}">{e(B["model"])}</a></th></tr>{rows}</table></div><h2>Differences in the published specs</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in diff) or "<li>The published spec fields shown here match.</li>"}</ul>'
        for p in (A, B): body += f'<h2>{e(p["model"])}: notes from the specs</h2>{pc(p)}<h3>Reviewer videos</h3>{vlist(p)}'
        body += '<p class="meta">These notes restate published specs. They are not lab or on-court test results.</p>'
        page(fn, t, body, f"{t}: maker specs and latest checked prices for a same-category pair. No score or rating from us.",
             fresh=[fresh_p(A), fresh_p(B)], schema=[item_list([A, B])]); vs_links.append((fn, t))
    # best-of lists
    usd = [p for p in PP if p["currency"] == "USD"]
    list_links = []
    def lst(title, fn, intro, items, why):
        ordered = sorted(items, key=lambda p: (p["brand"].lower(), p["model"].lower()))
        cards = "".join(pcard(p, why(p)) for p in ordered)
        page(fn, title, f'<h1>{e(title)}</h1>{DISC}<p>{intro}</p>{SRC}<p class="meta">Alphabetical by brand and model. Not a performance ranking.</p><div class="grid">{cards or "<p>No paddles in our database match this filter.</p>"}</div>',
             f"{title}. Spec filter only, from paddles.json. Not a scored ranking.",
             fresh=[fresh_p(p) for p in ordered], schema=[item_list(ordered)] if ordered else None); list_links.append((fn, title))
    u100 = sorted([p for p in usd if cur(p) <= 100], key=cur); near = sorted([p for p in usd if 100 < cur(p) <= 150], key=cur)
    lst("Best paddles under $100", "best-paddles-under-100.html", f'Paddles in our database at <b>$100 or less</b> at the latest checked maker price ({len(u100)} at that check), followed by the closest picks up to $150. Our database is small and focused on major brands, so check back as we add budget models. The <a href="guides/best-paddles-under-100.html">under-$100 guide</a> explains this filter in plain language.', u100 + near,
        lambda p: ("At or under $100 at our last check." if cur(p) <= 100 else "Just over $100 at our last check.") + " " + notes(p, ph(p))[0][0])
    beg = sorted([p for p in usd if cur(p) <= 200 and (cores(p) and max(cores(p)) >= 16 or re.search("hybrid|widebody|max", p["shape"], re.I))], key=cur)[:8]
    lst("Best pickleball paddles for beginners", "best-paddles-for-beginners.html", "Our beginner shortlist uses three spec rules: a price of $200 or less, plus a 16mm core option or a wider or hybrid face. Both are generally considered more forgiving. It's a starting point based on specs, not a test ranking.", beg,
        lambda p: "Budget-friendly with a forgiving spec profile: " + ", ".join(x for x in [p["core"], p["shape"]] if x) + ".")
    pw = [p for p in PP if "power" in p["model"].lower() or p["model"] in ("Pressure X 8E", "LABS Project Boomstik", "Cannon XPP M1")]
    lst("Best pickleball paddles for power", "best-paddles-for-power.html", "These are paddles their makers market for power, or that the reviewers in our feeds cover as power paddles. We sort by the latest checked price. Elongated shapes add leverage on drives and serves.", sorted(pw, key=cur),
        lambda p: "Marketed for power" + (" · elongated option for extra leverage" if "elongated" in p["shape"].lower() else "") + ".")
    ct = [p for p in PP if "control" in p["model"].lower() or (cores(p) and max(cores(p)) >= 16 and re.search("hybrid", p["shape"], re.I))]
    lst("Best pickleball paddles for control", "best-paddles-for-control.html", "These are paddles their makers market for control, plus 16mm+ hybrids. Thicker cores are generally described as softer and more controlled. We sort by the latest checked price.", sorted(ct, key=cur),
        lambda p: "Control-leaning spec: " + ", ".join(x for x in [p["core"], p["shape"]] if x) + ".")
    def listed(p):
        bits = []
        if p.get("core"): bits.append(f"{p['core']} core")
        if p.get("shape"): bits.append(f"{p['shape']} shape")
        if p.get("weight"): bits.append(f"weight {p['weight']}")
        return f"{p['brand']} lists " + ", ".join(bits) + "." if bits else f"{p['brand']} does not publish core, shape, or weight."
    mm16 = [p for p in PP if 16.0 in cores(p)]
    lst("Best 16mm paddles", "best-16mm-paddles.html", f"Filter: the core field lists 16mm ({len(mm16)} paddles). Models that also list other thicknesses stay in. This is not a ranking of how those paddles play.", mm16, listed)
    elongated = [p for p in PP if "elongated" in (p.get("shape") or "").lower()]
    lst("Best elongated paddles", "best-elongated-paddles.html", f"Filter: the shape field includes elongated ({len(elongated)} paddles). A blank shape is left out, even if another field mentions an elongated option. Not a ranking.", elongated, listed)
    tennis = [p for p in elongated if 16.0 in cores(p)]
    lst("Best for tennis players", "best-paddles-for-tennis-players.html", f"Filter only: the shape field includes elongated and the core field lists 16mm ({len(tennis)} paddles). paddles.json has no tennis-player field, so this is not a playtest ranking and not a claim about who should buy them.", tennis, listed)
    for brand in ("CRBN", "Engage", "Gearbox", "JOOLA", "Luzz", "Paddletek", "Selkirk", "Six Zero"):
        items = [p for p in PP if p["brand"] == brand]
        slugb = re.sub(r"[^a-z0-9]+", "-", brand.lower()).strip("-")
        aud = " Maker prices for this brand are in AUD." if items and items[0]["currency"] != "USD" else ""
        lst(f"Best {brand} paddles", f"best-{slugb}-paddles.html", f"Filter: brand is {brand} ({len(items)} paddles in paddles.json).{aud} Not a ranking of {brand} models.", items, listed)
    # hub
    page("compare.html", "Compare paddles", f'<h1>Compare paddles</h1><p class="meta">Head-to-head pages pair paddles that share a brand, or one elongated paddle from each of two brands. Best-of lists are spec filters. None of these pages is a performance ranking.</p><h2>Head to head</h2><ul>{"".join(f"<li><a href={chr(34)}{f}{chr(34)}>{e(t)}</a></li>" for f, t in vs_links)}</ul><h2>Best-of lists</h2><ul>{"".join(f"<li><a href={chr(34)}{f}{chr(34)}>{e(t)}</a></li>" for f, t in list_links)}</ul><h2>All paddles</h2><ul>{"".join(f"<li><a href={chr(34)}{slug(p)}{chr(34)}>{e(p[chr(98)+chr(114)+chr(97)+chr(110)+chr(100)])} {e(p[chr(109)+chr(111)+chr(100)+chr(101)+chr(108)])}</a></li>" for p in PP)}</ul>',
         "Same-category paddle comparisons and spec-filter lists from manufacturer specs and the latest checked maker prices. No performance ranking.",
         fresh={"vs": [fn for fn, _t in vs_links], "lists": [fn for fn, _t in list_links]}, schema=[item_list(PP)])
    # deals
    deals = sorted([p for p in PP if ph(p).get("drop") or ph(p).get("sale")], key=lambda p: -(1 - cur(p) / (ph(p).get("compare_at") or ph(p).get("previous") or cur(p))))
    def dcard(p):
        h = ph(p); ref = h.get("compare_at") if h.get("sale") else h.get("previous"); pct = round(100 * (1 - cur(p) / ref)) if ref else 0
        return pcard(p, f"-{pct}% · " + ("Down from our last recorded price" if h.get("drop") else "vs. the maker's compare-at price") + f" · lowest we've seen {money(p, h.get('low', cur(p)))}", own=True)
    upd = D("price_history.json").get("updated", "")
    # Our own codes (stacking with sales is unconfirmed); one copy handler for the strip and any own-code brand cards.
    OWNSTRIP = (("<h2>Our own code</h2>" + "".join(own_codes.callout(e, oc) for _b, oc in sorted(OWN.items()))) + own_codes.COPY_JS) if OWN else ""
    page("deals.html", "Pickleball paddle deals & price drops", f'<h1>Paddle deals</h1>{DISC}{OWNSTRIP}<p class="meta">{price_checked(upd, fmt, e)} We check each paddle\'s price on its maker\'s own site (only where robots.txt allows). A <b>price drop</b> means the price fell since our last check. <b>On sale</b> means the maker shows a higher compare-at price. Prices can change at any time, so confirm at checkout.</p><p class="meta"><a href="discount-codes.html"><b>Stack a coupon: see current discount codes →</b></a> · <a href="price-tracker.html"><b>Paddle Price Tracker →</b></a> · Shopping for touch? See <a href="best-paddles-for-control.html"><b>best paddles for control</b></a>.</p><div class="grid">{"".join(dcard(p) for p in deals) or "<p>No deals at our last check. Check back later.</p>"}</div>',
         f"Pickleball paddle price drops and maker-site sales, checked on each brand's own page. {price_checked(upd, fmt, e, html=False)}",
         fresh=[fresh_p(p) for p in deals], schema=[item_list(deals)] if deals else None)
    # paddle database (re-rendered with links + badges)
    prow = "".join(f'<tr><td><a href="{slug(p)}"><b>{e(p["brand"])}</b><br>{e(p["model"])}</a> {badge(ph(p), p)}</td><td>{e(p["weight"])}</td><td>{e(p["core"])}</td><td>{e(p["shape"])}</td><td>{pricecell(p)}</td><td>{buy(p)}</td></tr>' for p in PP)
    page("paddles.html", "Paddle database", f'<h1>Paddle database</h1>{DISC}<p><a class="btn" href="paddle-quiz.html" style="min-height:56px;font-size:1.1rem">🎯 Not sure? Take the 3-question paddle quiz →</a></p><p class="meta">Specs and list prices come from each manufacturer\'s own product page (retrieved {e(PD["retrieved"])}). {price_checked(upd, fmt, e)} Blank means the maker doesn\'t clearly publish it. Six Zero prices are in AUD. See <a href="deals.html">current deals</a>, <a href="compare.html">compare paddles</a>, or the <a href="price-index.html">price index</a>.</p><div class="tbl"><table><tr><th>Paddle</th><th>Weight</th><th>Core</th><th>Shape</th><th>Latest price</th><th>Where to buy</th></tr>{prow}</table></div>',
         f"Pickleball paddle specs, core thickness, shape and the latest maker price, sourced from each brand's product page. {price_checked(upd, fmt, e, html=False)}",
         fresh=[fresh_p(p) for p in PP], schema=[item_list(PP)])
    import csv, io
    hist = D("price_history.json"); rows_h = hist.get("paddles", {})
    by_name = {f'{p["brand"]} {p["model"]}': p for p in PP}
    buf = io.StringIO(); writer = csv.writer(buf)
    writer.writerow(["paddle", "currency", "date", "price", "compare_at", "available", "source_url"])
    for name in sorted(rows_h):
        rec = rows_h[name]
        for hrow in rec.get("history") or []:
            writer.writerow([name, rec.get("currency", ""), hrow.get("date", ""), hrow.get("price", ""), hrow.get("compare_at", ""), hrow.get("available", ""), rec.get("source_url", "")])
    (ROOT / "dist" / "price-index.csv").write_text(buf.getvalue())
    def mean(vals): return sum(vals) / len(vals) if vals else None
    def money_n(curcy, amt):
        if not isinstance(amt, (int, float)): return ""
        return ("$" if curcy == "USD" else "A$" if curcy == "AUD" else "") + f"{amt:,.2f}"
    usd_cur = [rec["current"] for rec in rows_h.values() if rec.get("currency") == "USD" and isinstance(rec.get("current"), (int, float))]
    aud_cur = [rec["current"] for rec in rows_h.values() if rec.get("currency") == "AUD" and isinstance(rec.get("current"), (int, float))]
    trs = []
    for name in sorted(rows_h):
        rec = rows_h[name]; p = by_name.get(name); curcy = rec.get("currency") or ""
        label = f'<a href="{slug(p)}">{e(name)}</a>' if p else e(name)
        current, previous = rec.get("current"), rec.get("previous")
        delta = ""
        if isinstance(current, (int, float)) and isinstance(previous, (int, float)):
            delta = money_n(curcy, current - previous)
        avail = "yes" if rec.get("available") is True else "no" if rec.get("available") is False else ""
        src = f'<a href="{e(rec["source_url"])}" target="_blank" rel="noopener">Maker page</a>' if rec.get("source_url") else ""
        trs.append(f'<tr><td>{label}</td><td>{e(curcy)}</td><td>{money_n(curcy, current)}</td><td>{money_n(curcy, previous)}</td><td>{delta}</td><td>{money_n(curcy, rec.get("low"))}</td><td>{avail}</td><td>{e(rec.get("checked") or "")}</td><td>{src}</td></tr>')
    usd_avg, aud_avg = mean(usd_cur), mean(aud_cur)
    page("price-index.html", "Paddle Price Index", f'''<h1>Paddle Price Index</h1><p class="meta">Every paddle recorded in price_history.json (file updated {e(hist.get("updated", ""))}). The USD number is the unweighted mean of {len(usd_cur)} current USD maker prices ({money_n("USD", usd_avg)}). The AUD number is the unweighted mean of {len(aud_cur)} current AUD maker prices ({money_n("AUD", aud_avg)}). The two currencies are not converted. Change is current minus previous from that file.</p>
<p><a class="btn" href="price-index.csv">Download CSV</a></p>
<div class="tbl"><table><tr><th>Paddle</th><th>Currency</th><th>Current</th><th>Previous</th><th>Change</th><th>Low</th><th>Available</th><th>Checked</th><th>Source</th></tr>{"".join(trs)}</table></div>''',
         "Unweighted means of current USD and AUD maker prices from price_history.json, plus each recorded price and a CSV of the history rows.",
         fresh={name: {k: rows_h[name].get(k) for k in ("currency", "current", "previous", "low", "compare_at", "available", "checked")} for name in sorted(rows_h)})
    # pros' paddles
    def match(x):
        for p in PP:
            if x.get("paddle") and x["paddle"].lower().startswith(p["brand"].lower().split()[0]) and keys(p) and any(re.search(k, x["paddle"], re.I) for k in keys(p)): return p
    rows = ""; cnt = {}
    for x in pros:
        if not x.get("paddle"): continue
        p = match(x); cnt[x["paddle"].split()[0].upper()] = cnt.get(x["paddle"].split()[0].upper(), 0) + 1
        cell = f'<a href="{slug(p)}">{e(x["paddle"])}</a> {badge(ph(p), p)}<br><span class="meta">{pricecell(p)}</span>' if p else e(x["paddle"]) + '<br><span class="meta">not in our database yet</span>'
        rows += f'<tr><td><a href="{e(x["profile"])}" target="_blank" rel="noopener"><b>{e(x["name"])}</b></a></td><td>{cell}</td><td>{buy(p) if p else "-"}</td></tr>'
    brands = ", ".join(f"{k.title()} ({v})" for k, v in sorted(cnt.items(), key=lambda kv: -kv[1]))
    matched, seen = [], set()
    for x in pros:
        mp = match(x)
        if mp and slug(mp) not in seen:
            seen.add(slug(mp)); matched.append(mp)
    page("pro-paddles.html", "What paddle do the pros use?", f'<h1>What paddle do the pros use?</h1>{DISC}<p class="meta">From each player\'s official PPA Tour profile (retrieved {e(P.get("retrieved"))}). Pros often play custom or pre-release versions, and sponsorships change. Brands among these players: {e(brands)}.</p><div class="tbl"><table><tr><th>Player</th><th>Paddle (per profile)</th><th>Buy</th></tr>{rows}</table></div><p class="meta">Players whose profile lists no paddle are left out.</p>',
         "Which paddles top PPA pros list on their official profiles, linked to maker specs and latest checked prices.",
         fresh=[{"name": x.get("name"), "paddle": x.get("paddle")} for x in pros if x.get("paddle")],
         schema=[item_list(matched)] if matched else None)

    # ---------- home ----------
    T, N, tcard, ncard, rcard, signup = X["T"], X["N"], X["tcard"], X["ncard"], X["rcard"], X["signup"]
    teaser = [x for x in pros if x.get("paddle")][:8]
    def av(n): return "".join(w[0] for w in n.split()[:2]).upper()
    pt = "".join(f'<a class="pro" href="pro-paddles.html" style="text-decoration:none;color:inherit"><span class="av">{e(av(x["name"]))}</span><span><b>{e(x["name"])}</b><br><span class="meta">{e(x["paddle"])}</span></span></a>' for x in teaser)
    dl = deals or sorted(PP, key=cur)[:6]
    def top5row(i, p):
        h = ph(p); ref = h.get("compare_at") if h.get("sale") else h.get("previous"); pct = round(100 * (1 - cur(p) / ref)) if ref else 0
        was = f'<s>{money(p, ref)}</s>' if ref and ref > cur(p) else ""
        why = "price drop" if h.get("drop") else "on sale"
        return (f'<li><a class="th" href="{slug(p)}" aria-label="{e(p["brand"])} {e(p["model"])}">{img(p, w=200, eager=i <= 3)}<span class="rk">{i}</span></a><div class="bd">'
                f'<h3><a href="{slug(p)}">{e(p["brand"])} {e(p["model"])}</a></h3>'
                f'<p class="fr">{e(p["brand"])} store · {why} · checked {fmt(h.get("checked"))}</p>'
                f'<div class="px">{money(p, cur(p))}{was}{f"<span class={chr(34)}off{chr(34)}>-{pct}%</span>" if pct > 0 else ""}</div>'
                f'<a class="btn go" href="{e(p["buy_url"])}" rel="sponsored nofollow noopener" target="_blank">Get deal →</a></div></li>')
    top5 = (f'<h2 id="top5">Top 5 paddle deals <a class="seemore" href="deals.html">All →</a></h2><ol class="top5">{"".join(top5row(i, p) for i, p in enumerate(deals[:5], 1))}</ol><p class="more">Prices from makers\' own sites. {price_checked(upd, fmt, e)} Confirm at checkout. <a href="/discount-codes">Stack a discount code →</a></p>') if deals else ""
    home = f'''<section class="topwrap"><div class="in"><div class="hstrip"><span class="dill"><picture><source srcset="avatar.webp" type="image/webp"><img src="avatar.png" alt="Big Dill, the DropThePickle mascot" width="68" height="68"></picture></span><div><span class="eyebrow"><i></i>Updated daily</span><h1>ALL THINGS <em>PICKLEBALL</em></h1><p>Free for everyone. {len(deals)} paddle deals, prices checked {fmt(upd)}.</p></div></div>
{top5}</div></section>
<main>
{X.get("BUZZ_TEASER","")}
<h2 id="start">Start here</h2>
<p class="meta">New to the sport, or shopping for a paddle? These guides use the USA Pickleball rulebook and the maker specs already on this site. No invented prices.</p>
<div class="grid secs">
<a class="card" href="guides/pickleball-rules-for-beginners.html"><h3>Rules for beginners</h3><div class="meta">Serve, kitchen, scoring →</div></a>
<a class="card" href="guides/how-to-dink.html"><h3>How to dink</h3><div class="meta">The soft kitchen shot →</div></a>
<a class="card" href="guides/how-to-choose-a-paddle.html"><h3>Choose a paddle</h3><div class="meta">Budget, shape, core, weight →</div></a>
<a class="card" href="guides/paddle-weight-and-core.html"><h3>Weight and core</h3><div class="meta">Ounces and millimetres →</div></a>
<a class="card" href="guides/best-paddles-under-100.html"><h3>Under $100</h3><div class="meta">Only checked maker prices →</div></a>
<a class="card" href="price-index.html"><h3>Price index</h3><div class="meta">Every recorded maker price →</div></a>
<a class="card" href="tournaments.html"><h3>Pro events</h3><div class="meta">Dates from the PPA feed →</div></a>
</div>
<div class="card spot"><a href="creators/ryan-morneau.html"><img src="https://i.ytimg.com/vi/Q7zUZLXK_gE/hqdefault.jpg" alt="The Most Important Singles Shots, a Pickleball Breakdowns clip"></a><div><span class="tag b-pub">Creator spotlight</span><h3><a href="creators/ryan-morneau.html">Ryan Morneau · Pickleball Breakdowns</a></h3><p>Match breakdowns and strategy tips. James Madison University reported him as the No. 1-ranked collegiate singles player.</p><p><a href="creators/ryan-morneau.html">Watch his latest clips</a></p></div></div>
<h2>Big Dill's Picks <a class="seemore" href="deals.html">All deals →</a></h2><p class="meta"><a href="discount-codes.html"><b>Pickleball discount codes →</b></a> Working coupon codes for Selkirk, CRBN, Six Zero, Gearbox and more, checked daily.</p><div class="rail">{"".join(pcard(p) for p in dl[:8])}</div>
<h2>Latest reviews <a class="seemore" href="reviews.html">All reviews →</a></h2><div class="grid">{"".join(rcard(v, False) for v in R.get("items", [])[:6])}</div>
<section class="dark"><div class="in"><h2>Up next on tour <a class="seemore" href="tournaments.html">Full schedule →</a></h2><div class="strip">{"".join(tcard(t) for t in T.get("items", [])[:6])}</div></div></section>
<h2>Headlines <a class="seemore" href="news.html">All news →</a></h2><div class="grid">{"".join(ncard(n) for n in N.get("items", [])[:6])}</div>
<h2>What the pros play <a class="seemore" href="pro-paddles.html">See all →</a></h2><div class="pros">{pt}</div>
<h2>Find your paddle</h2><div class="grid secs"><a class="card" href="paddle-quiz.html"><h3>🎯 Take the paddle quiz</h3><div class="meta">3 questions, 3 picks →</div></a>{"".join(f'<a class="card" href="{f}"><h3>{e(t)}</h3><div class="meta">Spec filter →</div></a>' for f, t in list_links)}</div>
<section class="band"><h2>Get the weekly drop</h2><p>The best paddle deals, new reviews and tournament news, once a week. No spam.</p>{signup("home")}</section>
</main>'''
    page("index.html", "Pickleball news, paddle deals & prices", home,
         "Daily pickleball news, verified paddle discount codes and dated price checks. All things pickleball, free for everyone.",
         full=True,
         fresh={"deals": [fresh_p(p) for p in dl[:8]],
                "buzz": [(b.get("title"), b.get("status")) for b in D("buzz.json").get("items", [])[:3]],
                "start": ["guides/pickleball-rules-for-beginners.html", "guides/how-to-dink.html", "guides/how-to-choose-a-paddle.html", "guides/paddle-weight-and-core.html", "guides/best-paddles-under-100.html", "price-index.html", "tournaments.html", "creators/ryan-morneau.html"],
                "reviews": [(v.get("title"), v.get("date"), v.get("link")) for v in R.get("items", [])[:6]],
                "news": [(n.get("title"), n.get("date"), n.get("link")) for n in N.get("items", [])[:6]],
                "events": [(t.get("name"), t.get("start"), t.get("end"), t.get("location")) for t in T.get("items", [])[:6]],
                "pros": [(x.get("name"), x.get("paddle")) for x in teaser]},
         schema=[item_list(dl[:8])] if dl else None)
    gl = [("guides/how-to-choose-a-paddle.html","How to choose a paddle","Budget, shape, core, weight"),("guides/pickleball-paddles-under-30.html","Pickleball paddles under $30","Retailer-confirmed prices only"),("guides/six-zero-paddle-review.html","Six Zero paddle lineup","Models, specs and US prices"),("events/ppa-worlds-2026.html","PPA Worlds 2026","Dates, venue, parking, tickets"),("guides/best-paddles-under-100.html","Best pickleball paddles under $100","Verified maker prices, dated"),("guides/pickleball-rules-for-beginners.html","Rules for beginners","Serve, kitchen, scoring"),("guides/how-to-dink.html","How to dink","The soft kitchen shot"),("guides/paddle-weight-and-core.html","Paddle weight and core","Ounces and millimetres"),("guides/is-my-paddle-dead.html","Is my paddle dead? Core crush signs","Symptoms, tests, when to replace"),("guides/pickleball-rules-cheat-sheet-2026.html","Pickleball rules cheat sheet 2026","USA Pickleball 2026 rulebook"),("guides/how-to-read-dupr-ratings.html","How to read DUPR ratings","Scale, calculation, percentiles"),("best-paddles-for-beginners.html","Best paddles for beginners","Spec filter"),("price-index.html","Paddle Price Index","Every recorded maker price")]
    page("guides.html", "Pickleball guides", '<h1>Pickleball guides</h1><p class="meta">Plain-language guides for new players and paddle shoppers.</p><div class="grid secs">' + "".join(f'<a class="card" href="{f}"><h3>{e(t)}</h3><div class="meta">{e(d)} →</div></a>' for f, t, d in gl) + '</div>',
         "Pickleball guides: choosing a paddle, paddles under $30 and $100, the Six Zero lineup, PPA Worlds 2026, the 2026 rules cheat sheet, DUPR ratings, core crush signs, how to dink, and paddle weight and core.",
         schema=[{"@type": "ItemList", "name": "Pickleball guides", "numberOfItems": len(gl), "itemListElement": [
             {"@type": "ListItem", "position": i, "name": t, "url": absu(f)} for i, (f, t, d) in enumerate(gl, 1)]}])
    import content_pages
    content_pages.make(page, e, fmt, PP, cur, ph)
