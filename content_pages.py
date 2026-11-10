"""Beginner guides and the Ryan Morneau spotlight.

Prices, specs, and video IDs come from data files or his public YouTube feed.
Rule statements follow the USA Pickleball rulebook. Nothing here is a playtest ranking.
"""
from paddle_pages import slug, weights, cores, money
import gift_pages

# Newest uploads on https://www.youtube.com/@pickleball_breakdowns as of 2026-10-16.
# A post titled "Test V44" from that same feed is left out.
VIDEOS = [
    ("Q7zUZLXK_gE", "The Most Important Singles Shots", "2026-10-15"),
    ("XvMXZBd6QM0", "Break Ankles like Jorja", "2026-10-14"),
    ("zaoPkv7HNB4", "Fast Hands = More Footwork", "2026-10-12"),
    ("27EpGzlVMS4", "Forehand Takes Middle = Fake News", "2026-10-11"),
    ("9ddM0uj-07Q", "Biggest Upset in PPA History?", "2026-10-09"),
    ("26DRfs221zo", "How to Beat Tall People", "2026-10-06"),
]
DINK_VIDEO = ("wjjT2aJeLeQ", "The Secret to Never Missing Dinks", "2026-09-29")
YT = "https://www.youtube.com/@pickleball_breakdowns"
IG = "https://instagram.com/pickleball_breakdowns"
TT = "https://tiktok.com/@pickleball_breakdowns"
FB = "https://www.facebook.com/pickleballbreakdowns"
JMU = "https://www.jmu.edu/news/2026/05/11-ryan-morneau-feature.shtml"
RULES = "https://usapickleball.org/docs/rules/USAP-Official-Rulebook.pdf"
RULES_SUM = "https://usapickleball.org/docs/rules/USAP-Rules-Summary.pdf"

GUIDES = [
    ("guides/how-to-choose-a-paddle.html", "How to choose a paddle"),
    ("guides/best-paddles-under-100.html", "Best paddles under $100"),
    ("guides/pickleball-rules-for-beginners.html", "Pickleball rules for beginners"),
    ("guides/how-to-dink.html", "How to dink"),
    ("guides/paddle-weight-and-core.html", "Paddle weight and core"),
    ("guides/is-my-paddle-dead.html", "Is my paddle dead? Core crush signs"),
    ("guides/pickleball-rules-cheat-sheet-2026.html", "Pickleball rules cheat sheet 2026"),
    ("guides/how-to-read-dupr-ratings.html", "How to read DUPR ratings"),
    ("guides/pickleball-paddles-under-30.html", "Pickleball paddles under $30"),
    ("guides/six-zero-paddle-review.html", "Six Zero paddle lineup and prices"),
    ("guides/indoor-vs-outdoor-pickleball-balls.html", "Indoor vs outdoor pickleball balls"),
    ("guides/how-to-choose-pickleball-shoes.html", "How to choose pickleball shoes"),
    ("guides/pickleball-court-dimensions.html", "Pickleball court dimensions"),
    ("guides/pickleball-grip-size.html", "Pickleball grip size chart"),
    ("guides/pickleball-drills.html", "Pickleball drills"),
    ("guides/pickleball-kitchen-rules.html", "Pickleball kitchen rules"),
    ("guides/third-shot-drop.html", "Third shot drop"),
    ("guides/pickleball-stacking.html", "Pickleball stacking"),
    ("guides/how-to-watch-pro-pickleball.html", "How to watch pro pickleball"),
    ("guides/pickleball-gift-guide-2026.html", "Pickleball gift guide 2026"),
]
RULES_CHANGES = "https://usapickleball.org/docs/rules/USAP-Rulebook-Change-Document.pdf"
RULES_CHANGES_VIEW = "https://rules.usapickleball.org/view/rule-changes-view-all/"
RULES_HUB = "https://usapickleball.org/rules/"


def make(page, e, fmt, PP, cur, ph):
    by = {p["model"]: p for p in PP}

    def P(model):
        return by[model]

    def href(p):
        return "../" + slug(p)

    def alink(p, label=None):
        return f'<a href="{href(p)}">{e(label or (p["brand"] + " " + p["model"]))}</a>'

    def faq(pairs):
        body = "".join(f'<details class="faq"><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q, a in pairs)
        schema = {"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pairs]}
        return f'<h2>Questions</h2>{body}', schema

    def sources(items):
        lis = "".join(f'<li><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>{(" — " + e(n)) if n else ""}</li>' for t, u, n in items)
        return f'<h2>Sources</h2><ul>{lis}</ul>'

    def money_links():
        return ('<p>Shopping for gear? Check today\'s <a href="../discount-codes.html">pickleball discount codes</a> '
                'and the <a href="../deals.html">paddle deals</a> before you pay full price.</p>')

    def more(current):
        links = "".join(f'<li><a href="../{fn}">{e(title)}</a></li>' for fn, title in GUIDES if fn != current)
        links += '<li><a href="../price-index.html">Paddle price index</a></li><li><a href="../tournaments.html">Pro events</a></li><li><a href="../events/opendoor-pickleball-world-championships.html">PPA Worlds 2026 guide</a></li><li><a href="../events/mlp-nations-cup-2026.html">MLP Nations Cup 2026: how to watch</a></li><li><a href="../events/usa-pickleball-nationals-2026.html">USA Pickleball Nationals 2026: schedule and how to watch</a></li><li><a href="../creators/ryan-morneau.html">Ryan Morneau spotlight</a></li>'
        return f'<h2>Keep going</h2><ul>{links}</ul>'

    def embed(vid, title, short=True):
        klass = "vid short" if short else "vid"
        return (f'<div class="card"><div class="{klass}"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{e(vid)}" '
                f'title="{e(title)}" allowfullscreen></iframe></div><h3><a href="https://www.youtube.com/watch?v={e(vid)}" '
                f'target="_blank" rel="noopener">{e(title)}</a></h3></div>')

    usd = [p for p in PP if p["currency"] == "USD"]
    u100 = sorted([p for p in usd if cur(p) <= 100], key=cur)
    near = sorted([p for p in usd if 100 < cur(p) <= 150], key=cur)
    priced = sorted(usd, key=cur)
    weighted = [(min(weights(p)), max(weights(p)), p) for p in PP if weights(p)]
    light = min(weighted, key=lambda t: (t[0], t[2]["brand"], t[2]["model"]))
    heavy = max(weighted, key=lambda t: (t[1], t[2]["brand"], t[2]["model"]))
    heavy_ties = [t for t in weighted if t[1] == heavy[1]]

    halo, luxx, perseus, bantam = P("SLK HALO Power"), P("LUXX Control Air (InfiniGrit)"), P("Perseus Pro V"), P("Bantam TKO-C")
    boom = P("LABS Project Boomstik")

    # ----- spotlight -----
    clips = "".join(embed(vid, title) for vid, title, _d in VIDEOS)
    social = (f'<a class="btn sm" href="{YT}" target="_blank" rel="noopener">YouTube</a>'
              f'<a class="btn sm" href="{IG}" target="_blank" rel="noopener">Instagram</a>'
              f'<a class="btn sm" href="{TT}" target="_blank" rel="noopener">TikTok</a>'
              f'<a class="btn sm" href="{FB}" target="_blank" rel="noopener">Facebook</a>')
    spot = f'''<h1>Ryan Morneau</h1>
<p class="meta">Pickleball Breakdowns · match breakdowns and strategy tips</p>
<p>Pickleball Breakdowns is Ryan Morneau's channel. On the channel he says he watches how the best players in the world make decisions, then breaks that down so you can use it in your next match. In his own channel bio, he calls himself the No. 1 collegiate singles player in the country when he graduated from James Madison University, and says he won a college national title along the way. <a href="{JMU}" target="_blank" rel="noopener">James Madison University</a> reported that he was the No. 1-ranked collegiate pickleball player in the United States, held that ranking for more than a year, and became the first collegiate singles national champion.</p>
<p>The clips below are six of his latest uploads from the channel's public feed on October 16, 2026. A post from that feed titled "Test V44" is not included. The videos are his. We embed them here and link each one back to YouTube.</p>
<div class="socials">{social}</div>
<div class="vgrid">{clips}</div>
<p class="note">Credit: Ryan Morneau, Pickleball Breakdowns. <a href="{YT}" target="_blank" rel="noopener">youtube.com/@pickleball_breakdowns</a></p>
<h2>Use this with the guides</h2>
<ul>
<li><a href="../guides/how-to-dink.html">How to dink</a> — his September 29, 2026 clip "The Secret to Never Missing Dinks" is embedded there.</li>
<li><a href="../guides/pickleball-rules-for-beginners.html">Pickleball rules for beginners</a></li>
<li><a href="../guides/how-to-choose-a-paddle.html">How to choose a paddle</a></li>
<li><a href="../guides/paddle-weight-and-core.html">Paddle weight and core</a></li>
</ul>'''
    videos_ld = [{
        "@type": "VideoObject", "name": title,
        "url": f"https://www.youtube.com/watch?v={vid}",
        "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}",
        "thumbnailUrl": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
        "uploadDate": date,
        "creator": {"@type": "Person", "name": "Ryan Morneau", "url": YT},
    } for vid, title, date in VIDEOS]
    person = {"@type": "Person", "name": "Ryan Morneau", "url": YT,
              "sameAs": [YT, IG, TT, FB],
              "alumniOf": {"@type": "CollegeOrUniversity", "name": "James Madison University", "url": JMU}}
    page("creators/ryan-morneau.html", "Ryan Morneau, Pickleball Breakdowns", spot,
         "Ryan Morneau's Pickleball Breakdowns channel: match breakdowns and strategy tips, with six of his latest YouTube clips embedded.",
         fresh={"videos": VIDEOS, "links": [YT, IG, TT, FB, JMU]},
         schema=[person, *videos_ld])

    # ----- how to choose -----
    lo, hi = priced[0], priced[-1]
    choose_faq = [
        ("What should a beginner decide first?",
         "Start with budget, then shape, then core thickness, then weight. Those are the fields the makers publish on the paddles in our database."),
        ("Does DropThePickle rank the best paddle?",
         "No. These pages filter published specs and the latest checked maker prices. They are not a playtest and not a rating."),
        ("Where are the prices from?",
         "Each price is the maker's own price from our latest check of the maker page, in the currency on that maker's page. We do not invent a street price."),
    ]
    faq_html, faq_ld = faq(choose_faq)
    choose = f'''<h1>How to choose a pickleball paddle</h1>
<p class="meta">A beginner and intermediate walkthrough using the specs and maker prices already in our database. Not a ranking.</p>
<p>You do not need a pro's paddle to start. You do need to know which published number you are buying. Work through budget, shape, core, and weight, then open the paddle page and read the maker's specs.</p>
<h2>1. Set a budget</h2>
<p>In our database the lowest USD maker price at our latest check is {money(lo, cur(lo))} for the {alink(lo)}, and the highest is {money(hi, cur(hi))} for the {alink(hi)}. Six Zero models are listed in AUD, so they are not in that dollar range. The <a href="../price-index.html">price index</a> tracks every recorded maker price. If you want to stay at $100, use the <a href="best-paddles-under-100.html">under-$100 guide</a>, which only includes paddles whose current maker price is actually at or under $100.</p>
<h2>2. Pick a shape</h2>
<p>An elongated face is longer and usually narrower. On our spec pages we describe that as extra reach, with less room on the sides when you miss the middle. A wider face, including shapes makers call Max, Widebody, or Hybrid, gives more side-to-side area. The <a href="../best-elongated-paddles.html">elongated filter</a> lists every paddle whose shape field includes elongated. Two real examples: the {alink(perseus)} is listed as elongated, and the {alink(halo)} is listed as Max or XL.</p>
<h2>3. Pick a core thickness</h2>
<p>Core thickness is the millimetre number in the core field, such as 13mm, 14mm, 16mm, or 19mm. Thicker cores are generally described as softer. Thinner cores are generally described as crisper. That is a description of the spec, not a test result from us. The <a href="paddle-weight-and-core.html">weight and core guide</a> shows which thicknesses our paddles actually publish, with a link to each example.</p>
<h2>4. Check the weight</h2>
<p>Makers that publish a weight in our files land between {light[0]:.1f} oz ({alink(light[2])}) and {heavy[1]:.1f} oz ({alink(heavy[2])}{", maker price in AUD" if heavy[2]["currency"] != "USD" else ""}). Lighter published weights are easier to swing at the kitchen. Heavier published weights put more mass behind the ball and can feel slower in a fast exchange. Some makers leave weight blank. If it is blank on the paddle page, we do not guess it.</p>
<h2>5. Read one spec page before you buy</h2>
<p>Open the <a href="../paddles.html">paddle database</a> or <a href="../compare.html">compare two paddles</a> from the same brand. Each paddle page repeats the maker's core, shape, weight, and latest checked price, and links to the maker's product page. Before you buy, measure your hand with our <a href="pickleball-grip-size.html">grip size guide</a>.</p>
{faq_html}
{more("guides/how-to-choose-a-paddle.html")}'''
    page("guides/how-to-choose-a-paddle.html", "How to choose a pickleball paddle", choose,
         "How to choose a pickleball paddle from published shape, core, weight, and maker price. Not a scored ranking.",
         fresh={"low": [lo["brand"], lo["model"], cur(lo)], "high": [hi["brand"], hi["model"], cur(hi)],
                "weight": [light[0], heavy[1]], "faq": choose_faq},
         schema=[faq_ld])

    # ----- under $100 -----
    def verified(p):
        h = ph(p)
        return (p["currency"] == "USD" and h.get("status") == "ok" and h.get("available") is True
                and isinstance(h.get("current"), (int, float)) and bool(h.get("checked")))
    ok_under = sorted([p for p in PP if verified(p) and ph(p)["current"] < 100], key=lambda p: (ph(p)["current"], p["brand"], p["model"]))
    ok_near = sorted([p for p in PP if verified(p) and 100 <= ph(p)["current"] <= 150], key=lambda p: (ph(p)["current"], p["brand"], p["model"]))
    aud = [p for p in PP if p["currency"] != "USD"]
    unverified = [p for p in PP if p["currency"] == "USD" and not verified(p)]

    def row(p):
        h = ph(p)
        spec = " · ".join(x for x in [p.get("core"), p.get("shape"), p.get("weight")] if x) or "not published by the maker"
        sale = f' (maker compare-at {money(p, h["compare_at"])})' if h.get("sale") and h.get("compare_at") else ""
        return f'<tr><th scope="row">{alink(p)}</th><td>{money(p, h["current"])}{e(sale)}</td><td>{e(fmt(h["checked"]))}</td><td>{e(spec)}</td></tr>'

    def table(rows):
        return ('<div class="tbl"><table><thead><tr><th>Paddle</th><th>Maker price</th><th>Price checked</th><th>Published specs</th></tr></thead><tbody>'
                + "".join(row(p) for p in rows) + '</tbody></table></div>')

    if ok_under:
        under_table = table(ok_under)
        under_lead = f"{len(ok_under)} paddle{'s' if len(ok_under) != 1 else ''} in our database {'have' if len(ok_under) != 1 else 'has'} a verified current maker price under $100."
    else:
        under_table = "<p><b>None right now.</b> No paddle in our database has a verified current maker price under $100.</p>"
        under_lead = "No paddle in our database has a verified current maker price under $100 right now."
    near_table = table(ok_near) if ok_near else "<p>None.</p>"
    at100 = [p for p in ok_near if ph(p)["current"] == 100]
    at100_txt = "".join(f" The {p['brand']} {p['model']} is exactly {money(p, 100)}, which is not under $100, so it is excluded." for p in at100)
    excl = [f"{p['brand']} {p['model']}: exactly {money(p, 100)} at the last check, not under $100." for p in at100]
    if aud:
        excl.append(f"{len(aud)} Six Zero paddle{'s are' if len(aud) != 1 else ' is'} priced in AUD on the maker's site. We do not convert currencies, so {'they are' if len(aud) != 1 else 'it is'} left out.")
    if unverified:
        excl.append(f"{len(unverified)} USD paddle{'s' if len(unverified) != 1 else ''} had no successful, in-stock price check, so {'they are' if len(unverified) != 1 else 'it is'} left out.")
    names = ", ".join(f"{p['brand']} {p['model']}" for p in ok_under)
    checked_dates = sorted({ph(p)["checked"] for p in PP if verified(p)})
    last_check = fmt(checked_dates[-1]) if checked_dates else "not recorded"
    cheapest = ok_under[0] if ok_under else None
    cheapest_txt = (
        f"At our latest check, the lowest verified maker price under $100 is {money(cheapest, ph(cheapest)['current'])} "
        f"for the {cheapest['brand']} {cheapest['model']} (checked {fmt(ph(cheapest)['checked'])})."
        if cheapest else
        "None right now. See the $100 to $150 table for the closest verified prices."
    )
    u100_faq = [
        ("Which pickleball paddles are under $100?",
         under_lead + (f" They are: {names}." if ok_under else " The cheapest verified prices in our file are $100 or more, and they are shown in a separate table.")),
        ("What is the cheapest paddle under $100 on this page?",
         cheapest_txt),
        ("Where do these prices come from?",
         f"Each price is the maker's own price from our latest check of the maker page, saved with the date it was checked. The latest check date on this page is {last_check}. We do not invent street or coupon prices."),
        ("Why is a $100.00 paddle not on the list?",
         "This list only includes paddles priced under $100. A paddle at exactly $100.00 does not meet that rule, so it is shown in the $100 to $150 table instead."),
        ("Is this a ranking of the best paddles?",
         "No. Here, best means the paddle passed the price rule. We do not playtest or score power, control, or spin."),
        ("Are under-$100 paddles good for beginners?",
         "A low price does not automatically mean a beginner paddle. Use this page for the budget filter, then check published shape and weight on how to choose a paddle and the beginners paddles filter."),
    ]
    faq_html, faq_ld = faq(u100_faq)
    _OWN = __import__("own_codes").own_codes(__import__("json").load(open(__import__("pathlib").Path(__file__).with_name("config.json"))))
    _voc = _OWN.get("Volair")
    vol_under = [p for p in ok_under if p["brand"] == "Volair"]

    def vrow(p):
        h = ph(p)
        ex = " Volair doesn't tag this paddle as included in its discounts, so the code may not apply. Check the total before you pay." if p.get("code_excluded") else ""
        spec = ", ".join(x for x in [p.get("shape"), p.get("core"), p.get("face")] if x)
        return (f'<li><b>{alink(p)}</b>: {money(p, h["current"])} on volair.com (checked {e(fmt(h["checked"]))}). {e(spec)}.{e(ex)} '
                f'<a href="{e(p["buy_url"])}" rel="sponsored noopener" target="_blank">Shop at Volair →</a></li>')
    vol_html = ""
    if vol_under and _voc:
        vol_html = (f'<h2>Volair paddles under $100 with code {e(_voc["code"])}</h2>'
                    f'<p>{"Every paddle" if len(vol_under) == len(ok_under) else f"{len(vol_under)} of the {len(ok_under)} paddles"} that passed our under-$100 rule {"is a Volair" if len(vol_under) == len(ok_under) else "are Volairs"}. Our code <b>{e(_voc["code"])}</b> takes {e(_voc["discount"])} at checkout on volair.com. '
                    f'Volair doesn\'t publish whether the code stacks with sale prices, so check your cart total. {e(__import__("own_codes").earn_line(_voc))}</p>'
                    f'<ul>{"".join(vrow(p) for p in vol_under)}</ul>'
                    f'<p class="meta">Full code details: <a href="../discount-codes/volair.html">Volair promo code</a> · <a href="best-volair-paddles.html">Best Volair paddle by player type</a></p>')
    u100_faq += [
        ("Is there a discount code for paddles under $100?",
         (f"Yes for Volair: our code {_voc['code']} takes {_voc['discount']} at checkout on volair.com. " if _voc else "") + "Some paddles may be excluded from discounts (including some sale models). Every code we track is on our discount codes page."),
        ("Will these paddles be cheaper on Black Friday 2026?",
         "We can't say yet. We only report a Black Friday sale once the brand publishes it. Our Black Friday hub tracks which brands have announced 2026 sales, and our price tracker shows if a price really dropped."),
    ]
    faq_html, faq_ld = faq(u100_faq)
    # SERP polish (approved P1): at-a-glance criteria, buyer FAQs, internal links.
    # Keep Web Dev's short title stem; build.py appends " · DropThePickle". Prices stay
    # data-driven from price_history checks — no invented scores or codes.
    under = f'''<h1>Best Pickleball Paddles Under $100 (2026)</h1>
<p class="meta">Verified maker prices from our own paddle file (latest check {e(last_check)}). Not a playtest and not a ranking. Built for the 2026 shopping season.</p>
{__import__("own_codes").volair_link(__import__("own_codes").own_codes(__import__("json").load(open(__import__("pathlib").Path(__file__).with_name("config.json")))), "Shopping Volair?")}
<p>{under_lead} The rule is strict: the paddle needs a successful, in-stock price check on the maker's own page, in US dollars, and the current price must be below $100. Every price on this page shows the date it was checked.</p>
<h2>How this under-$100 list works</h2>
<ul>
<li><b>Strict under-$100 rule:</b> current maker price must be below $100 (a paddle at exactly $100.00 goes in the near table).</li>
<li><b>Verified only:</b> USD, in stock, with a check date on the maker's own page. We do not invent street or coupon prices.</li>
<li><b>"Best" means the filter:</b> we do not playtest or score power, control, or spin.</li>
<li><b>Near $100:</b> verified prices from $100 to $150 sit in a separate table so you can see the next step up.</li>
<li><b>Codes:</b> when a Volair under-$100 paddle is eligible, our code applies at checkout; some models are excluded. Full list on <a href="/discount-codes">discount codes</a>.</li>
</ul>
<h2>Under $100 right now (verified maker prices)</h2>
{under_table}
{vol_html}
<h2>Near $100: verified prices $100 to $150</h2>
<p>These paddles cost $100 or more, so they are <b>not</b> under-$100 picks. They are here so you can see where the cheapest verified prices actually sit.{e(at100_txt)}</p>
{near_table}
<h2>What we left out</h2>
<ul>{"".join(f"<li>{e(x)}</li>" for x in excl) or "<li>Nothing else.</li>"}</ul>
<p>Our database is a short list of major-brand models with specs copied from the maker. It is not a catalog of every budget paddle on the market. See every recorded price on the <a href="../price-index.html">price index</a>. New to buying? Start with <a href="how-to-choose-a-paddle.html">how to choose a paddle</a> or the <a href="../best-paddles-for-beginners.html">best paddles for beginners</a> filter.</p>
<p class="meta">Shopping now? <a href="/discount-codes"><b>Discount codes →</b></a> · <a href="../discount-codes/volair.html"><b>Volair code →</b></a> · <a href="../deals.html"><b>Paddle deals →</b></a> · <a href="pickleball-gift-guide-2026.html"><b>Gift guide 2026 →</b></a> · <a href="../deals/black-friday-pickleball-deals-2026.html"><b>Black Friday 2026 hub →</b></a> · <a href="../best-paddles-for-beginners.html">Beginners paddles</a> · <a href="pickleball-paddles-under-30.html">Paddles under $30</a></p>
{money_links()}
{faq_html}
{sources([(f"{p['brand']} {p['model']} (maker product page)", p["source_url"], f"price checked {fmt(ph(p)['checked'])}") for p in ok_under + ok_near])}
{more("guides/best-paddles-under-100.html")}'''
    def item_list_u100(ps, name):
        # Product/ItemList ported from the dropped /best-paddles-under-100 spec-filter page, using this guide's lists.
        if not ps:
            return None
        import urls
        base = __import__("json").load(open(__import__("pathlib").Path(__file__).with_name("config.json")))["BASE_URL"]
        els = []
        for i, p in enumerate(ps, 1):
            h = ph(p)
            offer = {"@type": "Offer", "url": p["buy_url"], "priceCurrency": p["currency"], "price": f"{h['current']:.2f}",
                     "itemCondition": "https://schema.org/NewCondition"}
            if h.get("available") is True:
                offer["availability"] = "https://schema.org/InStock"
            elif h.get("available") is False:
                offer["availability"] = "https://schema.org/OutOfStock"
            node = {"@type": "Product", "name": f'{p["brand"]} {p["model"]}', "brand": {"@type": "Brand", "name": p["brand"]},
                    "category": "Pickleball paddle", "url": urls.canon(base, slug(p)), "offers": offer}
            if h.get("image"):
                node["image"] = h["image"]
            els.append({"@type": "ListItem", "position": i, "name": node["name"], "url": node["url"], "item": node})
        return {"@type": "ItemList", "name": name, "numberOfItems": len(ps), "itemListElement": els}
    u100_lists = [x for x in (item_list_u100(ok_under, "Under $100 (verified)"),
                              item_list_u100(ok_near, "Closest verified prices, $100 to $150")) if x]
    page("guides/best-paddles-under-100.html", "Best Pickleball Paddles Under $100 (2026)", under,
         "Best pickleball paddles under $100 with verified maker prices, our Volair code DROPTHEPICKLE where it applies, and the closest $100–$150 picks. Strict under-$100 filter. No playtest scores.",
         fresh={"under": [(p["brand"], p["model"], ph(p)["current"]) for p in ok_under],  # no daily "checked" stamp
                "near": [(p["brand"], p["model"], ph(p)["current"]) for p in ok_near], "faq": u100_faq},
         schema=[faq_ld, *u100_lists], raw_title=True)

    # ----- rules -----
    # Beginner hub (SEO target approved 2026-11-05): keep the short rec-game reading, strengthen
    # title/meta, add an at-a-glance + next-steps hub to cheat sheet / drills / court / dink.
    # Facts stay paraphrases of the USA Pickleball Official Rulebook; no invented rule numbers.
    rules_faq = [
        ("Who can score a point?",
         "In standard scoring, a point is scored by serving the ball and winning the rally. If the receiving side wins the rally, it does not get a point. Rally scoring, where either side can score, is a separate option in the rulebook."),
        ("What is the kitchen?",
         "The non-volley zone, called the kitchen, is the 7-foot area on each side of the net. You may not volley the ball while you, or anything you are wearing or carrying, are touching that zone, including its lines. Your momentum after a volley counts too."),
        ("What is the two-bounce rule?",
         "The receiver must let the serve bounce, and the serving side must let the return bounce. After those two bounces, either side may volley or play a groundstroke. Hitting the ball before the required bounce is a fault."),
        ("How do you call the score in doubles?",
         "Call three numbers: serving team's score, receiving team's score, then the server number (1 or 2). A doubles game starts at zero-zero-two, because the first server of the game is treated as the second server. In singles, call only two numbers: server's score, then receiver's score."),
        ("What happens if the serve clips the net?",
         "Under the USA Pickleball rulebook, the serve must clear the kitchen and land in the correct service court, with or without touching the net. A serve that lands in the kitchen is a fault. A pro tour can publish its own deviations, so check that event's sheet before you play it."),
    ]
    faq_html, faq_ld = faq(rules_faq)
    rules = f'''<h1>Pickleball rules for beginners: court, serve, kitchen and scoring (2026)</h1>
<p class="meta">A short reading of the 2026 USA Pickleball Official Rulebook, in our words. The rulebook wins if we ever disagree. No named reviewer; send corrections from the <a href="../about.html">about page</a>.</p>
<p>The official text is the <a href="{RULES}" target="_blank" rel="noopener">USA Pickleball Official Rulebook</a> (PDF). The <a href="{RULES_SUM}" target="_blank" rel="noopener">basic rules summary</a> is the short version of the same organization. This page is the handful of rules that decide a rec game. For a one-page quick reference, use the <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a>.</p>
<h2>At a glance</h2>
<ul>
<li><b>Court:</b> 20 by 44 feet for singles and doubles; kitchen 7 feet deep; net 36 inches at the sidelines and 34 at the center.</li>
<li><b>Serve:</b> diagonal into the opposite service court; must clear the kitchen; legal volley serve or drop serve.</li>
<li><b>Two-bounce rule:</b> the serve and the return must each bounce before anyone can volley.</li>
<li><b>Kitchen:</b> you may stand in it; you may not volley while touching it, including its lines.</li>
<li><b>Scoring:</b> in standard scoring, only the serving side scores; a typical game is to 11, win by 2.</li>
</ul>
<h2>The court and the net</h2>
<p>A standard court is 20 feet wide and 44 feet long for singles and doubles. The net is 36 inches high at the sidelines and 34 inches high at the center. Each end has a non-volley zone 7 feet deep. All lines that bound that zone are part of the zone. Full measurements, space needed and layout tips: <a href="pickleball-court-dimensions.html">pickleball court dimensions</a>.</p>
<h2>The serve</h2>
<p>You serve diagonally into the opposite service court. The ball has to clear the kitchen and land in the correct box. On a volley serve, the paddle has to be moving upward, the paddle head must not be above your wrist, and the ball must not be above your waist when you hit it. A drop serve is the other legal motion: you drop the ball and hit it after it bounces, without propelling the ball on the way down. In singles, you start on the right when your score is even, and on the left when it is odd. Solo practice for this: <a href="pickleball-drills.html">Serving From a Basket</a> in our drills guide.</p>
<h2>Two bounces, then anything</h2>
<p>The receiver has to let the serve bounce. The serving side then has to let that return bounce. After those two bounces, either side may volley or play a groundstroke. Hitting the ball before the required bounce is a fault. Letting the ball bounce twice on your side is a fault.</p>
<h2>The kitchen</h2>
<p>You can stand in the kitchen. You cannot hit a volley while touching it. If you volley from behind the line and your momentum carries you, your paddle, or your hat into the zone, that is still a fault, even if the ball is already dead. A ball that lands on a line is in, except a serve that lands on the kitchen line, which is short. Full NVZ faults walk-through: <a href="pickleball-kitchen-rules.html">pickleball kitchen rules</a>. The <a href="how-to-dink.html">dink guide</a> is the soft shot people hit into this zone once the two bounces are done.</p>
<h2>Scoring</h2>
<p>Standard scoring gives a point only to the serving side, and only if that side wins the rally. A typical game in the rulebook's introduction is the first to 11, with a lead of at least 2. Tournament sections also list games to 15 or 21, still win by two. Call two numbers in singles: server's score, then receiver's score. The game starts at zero-zero. Call three numbers in doubles: serving team's score, receiving team's score, then the server number. A doubles game starts at zero-zero-two, because the first server of the game is treated as the second server. When in doubt, ask before the serve. The rulebook says a player may ask who the correct server or receiver is before the ball is hit. Rally scoring and other 2026 updates are summarized on the <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a>.</p>
<h2>What to practice next</h2>
<ul>
<li><a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a> — one-page quick reference, including confirmed 2026 changes.</li>
<li><a href="pickleball-kitchen-rules.html">Pickleball kitchen rules</a> — NVZ faults, paddle-touch, momentum and the kitchen line.</li>
<li><a href="pickleball-stacking.html">How to stack in pickleball</a> — legal doubles positioning on the serve and return.</li>
<li><a href="pickleball-drills.html">Pickleball drills</a> — USA Pickleball's four beginner drills, plus partner and solo wall work.</li>
<li><a href="pickleball-court-dimensions.html">Pickleball court dimensions</a> — court size, kitchen depth, net height and layout tolerances.</li>
<li><a href="how-to-dink.html">How to dink</a> — the soft kitchen shot after the two bounces.</li>
<li><a href="how-to-choose-a-paddle.html">How to choose a paddle</a> — specs from our database once the rules make sense. Or browse <a href="../best-paddles-for-beginners.html">best paddles for beginners</a>.</li>
</ul>
<p>Want the calendar after that? See <a href="../tournaments.html">which pro events are upcoming</a>.</p>
{money_links()}
{faq_html}
{more("guides/pickleball-rules-for-beginners.html")}'''
    page("guides/pickleball-rules-for-beginners.html", "Pickleball Rules for Beginners: Serve, Kitchen and Scoring (2026)", rules,
         "Pickleball rules for beginners from the 2026 USA Pickleball rulebook: court, serve, two-bounce rule, kitchen, and how scoring works. Not a substitute for the official book.",
         fresh={"source": RULES, "faq": rules_faq, "reviewer": "none named"},
         schema=[faq_ld])

    # ----- dink -----
    # SERP polish (approved P2, 2026-11-05): stronger title/meta for "how to dink in
    # pickleball", snippet-friendly at-a-glance, FAQs from facts already on this page,
    # kitchen-rules + beginners + drills links. Retain video embed and drill cross-links.
    vid, vtitle, vdate = DINK_VIDEO
    dink_faq = [
        ("What is a dink?",
         "A dink is a soft shot that drops into the opponent's non-volley zone. It is not a winner. It keeps the rally going until someone gives you a ball you can attack."),
        ("Can I step into the kitchen to dink?",
         "Yes, if the ball bounces first. The kitchen fault is for a volley, not for standing there. If you swing before the bounce, or your momentum from a volley carries you in, it is a fault."),
        ("Where should a beginner aim a dink?",
         "Crosscourt. The kitchen is 20 feet wide and 7 feet deep, so the diagonal gives you a longer landing area than a straight-ahead dink."),
        ("Why do my dinks float or pop up?",
         "Two habits on this page cause that: a big backswing (it turns a dink into a pop-up) and standing up as you hit (the usual way a dink floats). Keep the swing short and stay down."),
        ("When should I dink in a point?",
         "After the serve and the return have bounced. Most intermediate points are then decided at the kitchen, and a dink is the soft ball that lands in the opponent's kitchen so they cannot attack it."),
    ]
    faq_html, faq_ld = faq(dink_faq)
    dink = f'''<h1>How to dink in pickleball: soft kitchen shot, technique and drills</h1>
<p class="meta">How to dink in pickleball after the two-bounce rule: short-swing technique, crosscourt aim, kitchen/NVZ fault to avoid, a Ryan Morneau clip, and drills. Not a certified coaching lesson and not a claim about what wins matches.</p>
<h2>Dink at a glance</h2>
<ul>
<li><b>What it is:</b> a soft, unhurried shot that lands in the opponent's kitchen (non-volley zone) so they cannot attack it.</li>
<li><b>When:</b> after the serve and the return have bounced. Then most intermediate points are decided at the kitchen.</li>
<li><b>Motion:</b> paddle in front, short swing, meet the ball out front, aim crosscourt when you can, stay down.</li>
<li><b>Kitchen / NVZ:</b> you may step in after a bounce; volleying while touching the zone (or letting volley momentum carry you in) is a fault.</li>
<li><b>Practice:</b> watch the clip below, then run the Down the Link Dink Game in our drills guide.</li>
</ul>
<p>After the serve and the return have bounced, most intermediate points are decided at the kitchen. A dink is the unhurried ball that lands in the opponent's kitchen so they cannot attack it. The <a href="pickleball-rules-for-beginners.html">rules for beginners</a> guide covers why you cannot volley that ball if you are touching the zone; the full NVZ walk-through is <a href="pickleball-kitchen-rules.html">pickleball kitchen rules</a>. The kitchen is 7 feet deep and 20 feet wide; see <a href="pickleball-court-dimensions.html">pickleball court dimensions</a> for the full layout.</p>
<h2>The motion</h2>
<ul>
<li>Hold the paddle in front of you, not beside your hip. Meet the ball out in front of your body.</li>
<li>Use a short swing. Lift the ball just over the net. A big backswing turns a dink into a pop-up.</li>
<li>Aim crosscourt when you can. You have more court on the diagonal than straight ahead.</li>
<li>If the ball is dropping at your feet, let it bounce and then lift it. Reaching in and taking it out of the air is the kitchen fault.</li>
<li>Stay down. Standing up as you hit is the usual way a dink floats.</li>
</ul>
<h2>What to watch</h2>
<p>Ryan Morneau posted "{e(vtitle)}" on his Pickleball Breakdowns channel on {fmt(vdate)}. It is his clip, embedded here so you can watch the idea from a player who breaks down pro points. More of his recent clips are on the <a href="../creators/ryan-morneau.html">spotlight page</a>.</p>
{embed(vid, vtitle)}
<p>To build the habit, run the dink drills in our <a href="pickleball-drills.html">pickleball drills guide</a>, starting with the Down the Link Dink Game.</p>
<h2>The paddle is the smaller part</h2>
<p>A published light weight is easier to reset in a fast exchange. In our file the lightest listed number is {light[0]:.1f} oz, on the {alink(light[2])}. That is a spec, not a promise that the paddle dinks better. Read <a href="paddle-weight-and-core.html">weight and core</a> before you buy a new face to fix a swing.</p>
{faq_html}
{more("guides/how-to-dink.html")}'''
    page("guides/how-to-dink.html", "How to Dink in Pickleball: Soft Kitchen Shot, Technique and Drills", dink,
         "How to dink in pickleball: the soft kitchen shot after the two-bounce rule, short-swing technique, common pop-up mistakes, kitchen/NVZ fault, plus a Ryan Morneau clip and drills.",
         fresh={"video": DINK_VIDEO, "light": [light[2]["brand"], light[2]["model"], light[0]], "faq": dink_faq},
         schema=[faq_ld, {"@type": "VideoObject", "name": vtitle, "uploadDate": vdate,
                          "url": f"https://www.youtube.com/watch?v={vid}",
                          "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}",
                          "thumbnailUrl": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                          "creator": {"@type": "Person", "name": "Ryan Morneau", "url": YT}}])

    # ----- weight and core -----
    thick = {}
    for p in PP:
        for mm in cores(p):
            thick.setdefault(mm, []).append(p)
    thick_bits = []
    for mm in sorted(thick):
        sample = sorted(thick[mm], key=lambda p: (p["brand"].lower(), p["model"].lower()))[0]
        n = len(thick[mm])
        thick_bits.append(f'<li>{mm:g} mm, for example the {alink(sample)}. {n} paddle{"s" if n != 1 else ""} in the file {"list" if n != 1 else "lists"} this thickness.</li>')
    def heavy_label(t):
        aud = ", maker price in AUD" if t[2]["currency"] != "USD" else ""
        return alink(t[2]) + f" (up to {t[1]:.1f} oz{aud})"
    heavy_names = " and ".join(heavy_label(t) for t in sorted(heavy_ties, key=lambda t: (t[2]["brand"], t[2]["model"])))
    wt_faq = [
        ("What weights are actually published?",
         f"Among paddles that publish a weight, the lowest number in our file is {light[0]:.1f} oz and the highest is {heavy[1]:.1f} oz. If a maker leaves weight blank, the paddle page says so. We do not fill it in."),
        ("Is 16mm the control core?",
         "We do not rank cores. A 16mm or thicker option is generally described as softer than a thinner core in the same family. The paddle page tells you which thicknesses that model lists."),
        ("Should I add lead tape?",
         "The USA Pickleball rulebook allows weighted tape inside the stated limits. We do not tell you how much to add. Change one thing at a time and write down the published stock weight first."),
    ]
    faq_html, faq_ld = faq(wt_faq)
    weight = f'''<h1>Paddle weight and core, explained</h1>
<p class="meta">What the ounce and millimetre numbers on a spec page mean, using only paddles in our database.</p>
<p>Two numbers do most of the work when you compare paddles on this site: weight in ounces, and core thickness in millimetres. Both come from the maker's page. A blank field means the maker did not state it clearly when we copied the spec.</p>
<h2>Weight</h2>
<p>The lowest published weight in our file is {light[0]:.1f} oz, on the {alink(light[2])} ({e(light[2]["weight"])}). The high end of a published range reaches {heavy[1]:.1f} oz on {heavy_names}. A lighter paddle is easier to move at the kitchen. A heavier paddle carries more mass into the ball and can feel slower when the rally gets fast. Those are the usual descriptions of the number, not a lab test we ran.</p>
<p>Some listings are a range because the maker sells more than one shape. The {alink(P("SLK ERA Power"))} publishes {e(P("SLK ERA Power")["weight"])}. Read the shape that matches the paddle you are holding.</p>
<h2>Core thickness</h2>
<p>The core is the layer in the middle of the face. Makers list it in millimetres. Thicker cores are generally described as softer and more control-friendly. Thinner cores are generally described as crisper and poppier. A model can list more than one thickness. The {alink(halo)} lists {e(halo["core"])}. The {alink(perseus)} lists {e(perseus["core"])}. The {alink(luxx)} lists {e(luxx["core"])}, the thickest single number in our file. The {alink(bantam)} lists {e(bantam["core"])}.</p>
<ul>{"".join(thick_bits)}</ul>
<p>The <a href="../best-16mm-paddles.html">16mm filter</a> is every paddle whose core field includes 16mm. It is not an ordered list of the softest paddles.</p>
<h2>What to do with the numbers</h2>
<p>If you mishit on the sides, look at a wider shape before you look at a heavier weight. If the ball feels too lively, look at a thicker published core before you add tape. Then open <a href="how-to-choose-a-paddle.html">how to choose a paddle</a> and the <a href="../compare.html">comparison pages</a>, which put two spec sheets side by side. The third number to check is grip circumference: see the <a href="pickleball-grip-size.html">pickleball grip size chart</a>.</p>
{faq_html}
{more("guides/paddle-weight-and-core.html")}'''
    page("guides/paddle-weight-and-core.html", "Paddle weight and core explained", weight,
         "What pickleball paddle weight and core thickness mean, using the ounce and millimetre figures makers publish in our database.",
         fresh={"light": [light[2]["brand"], light[2]["model"], light[2]["weight"]],
                "heavy": [(t[2]["brand"], t[2]["model"], t[2]["weight"]) for t in heavy_ties],
                "cores": sorted(thick), "faq": wt_faq},
         schema=[faq_ld])

    # ----- is my paddle dead -----
    SELKIRK = "https://www.selkirk.com/blogs/paddles-and-product-education/what-is-core-crushing-in-pickleball-everything-you-need-to-know"
    SLABS = "https://www.selkirklabs.com/blogs/news/the-anatomy-of-pickleball-paddle-core-crushing-what-happens-beneath-the-surface"
    PBSCI = "https://pickleballscience.org/thermoformed-paddle-delamination-revisited/"
    DINK_CC = "https://www.thedinkpickleball.com/how-to-check-your-pickleball-paddle-for-core-crushing/"
    USAP_FIELD = "https://usapickleball.org/usap-news/equipment-news/usa-pickleball-and-pickleball-instruments-to-launch-paddle-field-testing-program-at-golden-ticket-events/"
    USAP_EQ = "https://equipment.usapickleball.org/"
    dead_faq = [
        ("What is core crush?",
         "Core crush is when the honeycomb core inside a paddle collapses or breaks down, so the face no longer stays rigid. Selkirk says it can come from a manufacturing problem or from gradual wear after many hard hits."),
        ("How do I test my paddle for core crush at home?",
         "Use three quick checks. Tap the face with a knuckle or a hard plastic handle and listen for a dull thud instead of a crisp, even sound. Drop a ball on different spots and look for spots where it barely bounces. Press firmly with your thumbs in the center and listen for a crackle or crunch. Do not press near the edge guard, where foam can crunch on its own."),
        ("Does a dead paddle hit softer or harder?",
         "It can feel either way. Selkirk describes dead spots and lost power. The Dink says a crushed core can also get a stronger trampoline effect, which can push a paddle out of spec for sanctioned play."),
        ("When should I replace my paddle?",
         "Replace it when the tap, bounce, or crunch test finds a problem in the hitting area, or when you see cracks or face separation. As a rough guide, Selkirk says heavy competitive players often replace paddles every 3 to 6 months and recreational players can often go a year or longer."),
        ("Is core crush covered by warranty?",
         "Sometimes. Coverage depends on the maker's warranty terms. Record a short video of the tap and press tests before you contact the maker."),
    ]
    faq_html, faq_ld = faq(dead_faq)
    dead = f'''<h1>Is my paddle dead? Core crush signs</h1>
<p class="meta">Symptoms, three quick tests, and when to replace a pickleball paddle. Based on maker and USA Pickleball sources, not our own lab.</p>
<p>A paddle that feels "dead" usually has a problem in the core, the honeycomb layer between the two faces. <a href="{SELKIRK}" target="_blank" rel="noopener">Selkirk</a> describes core crushing as the core collapsing so it no longer stays rigid, either from a manufacturing problem or from wear after many hard hits. It is different from delamination, where the face separates from the core, but the two can show similar signs.</p>
<h2>Symptoms</h2>
<ul>
<li><b>Dull sound.</b> Hits sound flat or hollow, especially in the sweet spot.</li>
<li><b>Dead spots.</b> The ball comes off some parts of the face with much less pop than others.</li>
<li><b>Less power or more effort.</b> You swing harder for the same depth.</li>
<li><b>A sudden "hot" feel.</b> <a href="{DINK_CC}" target="_blank" rel="noopener">The Dink</a> reports that a crushed core can also give a stronger trampoline effect, so a paddle can feel livelier as it fails.</li>
<li><b>Visible wear.</b> Cracks near the edge, discoloration, or shiny worn patches, per Selkirk.</li>
</ul>
<h2>How to test it</h2>
<ol>
<li><b>Tap test.</b> Tap across the face with a knuckle or the hard plastic end of a screwdriver handle. <a href="{PBSCI}" target="_blank" rel="noopener">Pickleball Science</a> found that undamaged areas give a high "ping" and damaged areas give a low "thud."</li>
<li><b>Bounce test.</b> Hold the paddle flat and drop a ball on different spots. A spot where the ball barely rebounds is likely a dead zone, per <a href="{SLABS}" target="_blank" rel="noopener">Selkirk LABS</a>.</li>
<li><b>Press test.</b> Press firmly with your thumbs in the center or just above it. A crackle, crunch, or a face that gives inward points to a weakened core. Stay away from the edge guard, where foam can crunch normally.</li>
</ol>
<p>These are field checks, not a lab result. USA Pickleball runs its own <a href="{USAP_FIELD}" target="_blank" rel="noopener">paddle field-testing program at Golden Ticket events</a>, and approved models are listed in the <a href="{USAP_EQ}" target="_blank" rel="noopener">USA Pickleball equipment database</a>. If you play sanctioned events, a worn paddle could fail testing even if the model is approved.</p>
<h2>When to replace it</h2>
<ul>
<li>Any of the three tests finds a problem in the hitting area.</li>
<li>You see cracks, a split edge guard, or the face lifting.</li>
<li>It has been heavy use for a long time. Selkirk's rough guide is every 3 to 6 months for heavy competitive players and a year or longer for recreational players.</li>
</ul>
<p>To make a paddle last longer, Selkirk advises keeping it out of hot cars and off wet courts. Before you buy a new one, read <a href="paddle-weight-and-core.html">paddle weight and core</a>, then compare <a href="best-paddles-under-100.html">paddles under $100</a>.</p>
{money_links()}
{faq_html}
{sources([("Selkirk: What is core crushing in pickleball?", SELKIRK, "manufacturer"),
          ("Selkirk LABS: The anatomy of paddle core crushing", SLABS, "manufacturer"),
          ("USA Pickleball: paddle field-testing program at Golden Ticket events", USAP_FIELD, "governing body"),
          ("USA Pickleball approved equipment database", USAP_EQ, "governing body"),
          ("Pickleball Science: Thermoformed paddle delamination revisited", PBSCI, "independent testing"),
          ("The Dink: How to check your paddle for core crushing", DINK_CC, "")])}
{more("guides/is-my-paddle-dead.html")}'''
    page("guides/is-my-paddle-dead.html", "Is my pickleball paddle dead? Core crush signs and tests", dead,
         "Core crush signs in a pickleball paddle: dull sound, dead spots, the tap, bounce and press tests, and when to replace it. Cited to Selkirk and USA Pickleball.",
         fresh={"faq": dead_faq, "links": [SELKIRK, SLABS, USAP_FIELD, USAP_EQ, PBSCI, DINK_CC]},
         schema=[faq_ld])

    # ----- rules cheat sheet 2026 -----
    cheat_faq = [
        ("What rulebook is this cheat sheet based on?",
         "The 2026 USA Pickleball Official Rulebook, plus the USA Pickleball 2026 Rulebook Change Document, published December 17, 2025. The rulebook wins if this page ever disagrees."),
        ("Did rally scoring change in 2026?",
         "Yes. Rally scoring is still a provisional option. In 2026 a point is scored by whoever wins each rally, including when the receiving side has game point. Under the 2025 rule, a receiver could not win the game on a rally."),
        ("Can I put spin on the serve in 2026?",
         "You may not manipulate the ball to add spin when you release it, except letting it roll off the paddle face. The 2026 rule adds that spin may be applied when the paddle contacts the ball."),
        ("Is the two-bounce rule the same in 2026?",
         "Yes. The serve and the return of serve must each bounce before being hit."),
    ]
    faq_html, faq_ld = faq(cheat_faq)
    cheat = f'''<h1>Pickleball rules cheat sheet 2026</h1>
<p class="meta">One-page summary of the 2026 USA Pickleball Official Rulebook, in our words, with the confirmed 2026 changes. The rulebook wins if we ever disagree. No named reviewer; send corrections from the <a href="../about.html">about page</a>.</p>
<p>Source: the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball Official Rulebook</a> (PDF) and the <a href="{RULES_CHANGES}" target="_blank" rel="noopener">2026 Rulebook Change Document</a> (PDF, published December 17, 2025). The 2026 book was renumbered, so rule numbers below are the 2026 numbers.</p>
<h2>The basics</h2>
<ul>
<li><b>Court:</b> 20 by 44 feet for singles and doubles, with a non-volley zone (the kitchen) on each side of the net. Full measurements: <a href="pickleball-court-dimensions.html">pickleball court dimensions</a>.</li>
<li><b>Serve:</b> diagonal, into the opposite service court, using a legal volley serve or drop serve.</li>
<li><b>Two-bounce rule (10.A):</b> the serve and the return of serve must each bounce before being hit.</li>
<li><b>Double bounce (10.B):</b> you must return the ball before its second bounce.</li>
<li><b>Kitchen:</b> you may stand in it, but you may not volley while touching it. See the <a href="pickleball-rules-for-beginners.html">beginner rules guide</a> for the full kitchen walk-through.</li>
<li><b>Standard scoring (4.A):</b> a point is scored by serving and winning the rally. A typical game is to 11, win by 2.</li>
</ul>
<h2>Volley serve (7.C)</h2>
<ul>
<li>The paddle must move in a <b>clear</b> upward arc when it contacts the ball (7.C.1).</li>
<li>The highest point of the paddle head must <b>clearly</b> not be above the server's wrist joint at contact (7.C.2).</li>
<li>The ball must <b>clearly</b> be no higher than the server's waist at contact (7.C.3).</li>
</ul>
<h2>Confirmed 2026 changes</h2>
<p>Each item below is listed in the USA Pickleball 2026 Rulebook Change Document.</p>
<ul>
<li><b>Rally scoring game point (14.A.2, 15.C.2).</b> Rally scoring stays a provisional option. A point now goes to whoever wins each rally, including when the receiving side has game point. Tournament directors may not use rally scoring in double-elimination doubles events, 2026 Golden Ticket events, or the 2026 National Championships.</li>
<li><b>"Clearly" added to the volley serve (7.C).</b> USA Pickleball says the word makes the rule stronger and more enforceable.</li>
<li><b>Serve spin (7.B.2).</b> You still may not add spin when releasing the ball, except by letting it roll off the paddle face. The 2026 text adds that spin may be applied on contact with the paddle.</li>
<li><b>Double hit (10.D).</b> A ball may be hit more than once in one continuous, single-direction stroke by one player. A non-continuous stroke, or both partners hitting the ball, is a fault.</li>
<li><b>Out calls (8.F, 8.F.3).</b> Signal "out" by voice, hand signal, or both. If you return the ball, call it before the opponent hits it or before the ball becomes dead.</li>
<li><b>Wrong score (6.F).</b> A player may stop a rally to fix the score before the return of serve. Stopping play to challenge a correct score is a fault.</li>
<li><b>Spectators (8.J).</b> Spectators must not be consulted on any call. The old wording was "should not."</li>
</ul>
<p>The change document also lists other updates, including adaptive standing play, timeouts, ejections, and wheelchair rules. Read the full <a href="{RULES_CHANGES}" target="_blank" rel="noopener">change document</a> or USA Pickleball's <a href="{RULES_CHANGES_VIEW}" target="_blank" rel="noopener">rule change list</a> for every entry. Pro tours can publish their own deviations, so check the event's rules before you play it.</p>
<p>Once the rules click, see <a href="how-to-dink.html">how to dink</a>, <a href="pickleball-stacking.html">how to stack in doubles</a> (legal under the position rules in Section 5) and <a href="how-to-read-dupr-ratings.html">how to read DUPR ratings</a>.</p>
{money_links()}
{faq_html}
{sources([("USA Pickleball 2026 Official Rulebook (PDF)", RULES, ""),
          ("USA Pickleball 2026 Rulebook Change Document (PDF)", RULES_CHANGES, "published December 17, 2025"),
          ("USA Pickleball rule changes, all entries", RULES_CHANGES_VIEW, ""),
          ("USA Pickleball rules hub", RULES_HUB, "")])}
{more("guides/pickleball-rules-cheat-sheet-2026.html")}'''
    page("guides/pickleball-rules-cheat-sheet-2026.html", "Pickleball rules cheat sheet 2026 (USA Pickleball rulebook)", cheat,
         "A one-page 2026 pickleball rules cheat sheet from the USA Pickleball Official Rulebook, with the confirmed 2026 changes to rally scoring, serves, double hits and out calls.",
         fresh={"source": [RULES, RULES_CHANGES], "faq": cheat_faq, "reviewer": "none named"},
         schema=[faq_ld])

    # ----- DUPR -----
    # SERP polish (approved P1, 2026-11-05): stronger title/meta for "how to read DUPR /
    # DUPR scale / DUPR explained", snippet-friendly at-a-glance, club-facing FAQs.
    # Percentiles and scale numbers stay from DUPR + The Dink sources already on this page.
    DUPR_HOW = "https://www.dupr.com/how-it-works"
    DUPR_CALC = "https://www.dupr.com/post/how-your-dupr-rating-is-calculated"
    DUPR_ALGO = "https://www.dupr.com/post/dupr-algo-update-win-or-lose-your-rating-can-go-up"
    DUPR_PCT = "https://www.dupr.com/post/dupr-rating-percentiles-see-how-your-rating-stacks-up-2"
    DINK_PCT = "https://www.thedinkpickleball.com/dupr-rating-percentiles-where-does-your-rating-rank/"
    PCT = [("3.0", "31st", "Top 69%"), ("3.5", "60th", "Top 40%"), ("4.0", "84th", "Top 16%"), ("4.5", "95th", "Top 5%"), ("5.0", "99th", "Top 1%")]
    DIST_ROWS = [("2.000 to 2.499", "11%"), ("2.500 to 2.999", "20%"), ("3.000 to 3.499", "29%"), ("3.500 to 3.999", "24%"), ("4.000 to 4.499", "11%"), ("4.500 to 4.999", "4%"), ("5.000+", "1%")]
    dupr_faq = [
        ("What is the DUPR scale?",
         "DUPR ratings run from 2.000 to 8.000. New players start as NR, meaning not rated, until they have enough results."),
        ("Can my DUPR go up if I lose?",
         "Yes. Since July 8, 2025, DUPR moves your rating on performance against the expected score. If you score more points than expected, your rating can go up even in a loss. If you score fewer, it can go down even in a win."),
        ("What percentile is a 4.0 DUPR?",
         "About the 84th percentile, so roughly the top 16% of active DUPR doubles players. That comes from a DUPR snapshot dated September 22, 2026, reported by DUPR and The Dink."),
        ("What is the DUPR reliability score?",
         "It is a 1 to 100% number on your profile that shows how much recent match data your rating is based on. A low score means the rating rests on old or thin data."),
        ("What is a typical or average DUPR rating?",
         "There is no single average published as a mean. In the September 22, 2026 doubles snapshot from DUPR and The Dink, the biggest band is 3.000 to 3.499 (29% of active doubles players), and 53% of active doubles players are somewhere in the 3s."),
        ("Are singles and doubles DUPR ratings the same?",
         "No. DUPR gives separate ratings for singles, gender doubles, and mixed doubles. Players in the 50 to 65+ bracket can also have an age-group rating. Compare like with like."),
    ]
    faq_html, faq_ld = faq(dupr_faq)
    pct_rows = "".join(f'<tr><th scope="row">{r}</th><td>{p}</td><td>{t}</td></tr>' for r, p, t in PCT)
    dist_rows = "".join(f'<tr><th scope="row">{r}</th><td>{s_}</td></tr>' for r, s_ in DIST_ROWS)
    dupr = f'''<h1>How to read DUPR ratings: scale explained, calculation and percentiles</h1>
<p class="meta">DUPR explained without the app: the 2.000 to 8.000 scale, how a rating moves, the reliability score, and 2026 doubles percentiles. Sourced from DUPR and The Dink.</p>
<h2>DUPR at a glance</h2>
<ul>
<li><b>Scale:</b> 2.000 to 8.000. New players start as <b>NR</b> (not rated) until they have enough results.</li>
<li><b>Separate numbers:</b> singles, gender doubles, and mixed doubles each get their own rating; 50 to 65+ players can also get an age-group rating.</li>
<li><b>Reliability score:</b> 1 to 100% on your profile. Higher means the rating rests on fresher, thicker match data.</li>
<li><b>Four factors:</b> performance vs. expectation, type of match, recency, and volume.</li>
<li><b>Quick percentile:</b> a 4.0 doubles rating is about the 84th percentile (top 16%) in the September 22, 2026 snapshot.</li>
</ul>
<h2>The scale</h2>
<p>According to <a href="{DUPR_HOW}" target="_blank" rel="noopener">DUPR</a>, every new player starts as <b>NR</b> (not rated), then gets a rating on a scale from <b>2.000 to 8.000</b>. You get separate ratings for singles, gender doubles, and mixed doubles, and players in the 50 to 65+ bracket also get an age-group rating.</p>
<p>Your profile shows two numbers: the <b>DUPR rating</b> and a <b>reliability score</b> from 1 to 100%. A higher reliability score means the rating is more likely to reflect your current level. A low one means it rests on old or thin match data.</p>
<h2>How a rating is calculated</h2>
<p>DUPR lists four factors on its <a href="{DUPR_HOW}" target="_blank" rel="noopener">How it works</a> page and in its post <a href="{DUPR_CALC}" target="_blank" rel="noopener">How your DUPR rating is calculated</a>:</p>
<ol>
<li><b>Performance vs. expectation.</b> Every match has an expected score based on everyone's rating. Beat it and your rating can rise. Fall short and it can drop.</li>
<li><b>Type of match.</b> Verified club, league, and tournament matches count more than self-posted rec games.</li>
<li><b>Recency.</b> Recent matches count the most.</li>
<li><b>Volume.</b> More matches make your rating more stable, so one result moves it less.</li>
</ol>
<p>In doubles, the team rating is the average of both players' ratings, and that drives the expected score. Since <a href="{DUPR_ALGO}" target="_blank" rel="noopener">DUPR's July 8, 2025 update</a>, a win does not guarantee a rise. DUPR's own example: a 3.5 expected to lose 5-11 to a 4.0 who instead loses 9-11 will see the rating go up.</p>
<h2>What percentile is your DUPR?</h2>
<p>DUPR shared a snapshot of doubles ratings dated September 22, 2026, covering players worldwide with at least one result in the previous 12 months. <a href="{DINK_PCT}" target="_blank" rel="noopener">The Dink</a> reported it on October 7, 2026, and DUPR published the same figures in <a href="{DUPR_PCT}" target="_blank" rel="noopener">its own post</a>. Percentages are rounded, so percentiles are approximate.</p>
<div class="tbl"><table><thead><tr><th>DUPR rating</th><th>Percentile</th><th>Where that puts you</th></tr></thead><tbody>{pct_rows}</tbody></table></div>
<div class="tbl"><table><thead><tr><th>Rating range</th><th>Share of active doubles players</th></tr></thead><tbody>{dist_rows}</tbody></table></div>
<p>The biggest band is 3.000 to 3.499, and 53% of active players are somewhere in the 3s. The data covers active DUPR doubles players only, not singles and not everyone who plays.</p>
<h2>Reading your own number</h2>
<ul>
<li>Check the reliability score first. A low score means the rating may not match how you play today.</li>
<li>Compare like with like. Your singles and doubles ratings are separate.</li>
<li>Log verified matches. Club, league, and tournament results count more than self-posted games.</li>
</ul>
<p>For clubs and captains: the same three checks are the useful ones before you place someone in a bracket. This page does not invent a bracket formula; it restates how DUPR describes the rating itself.</p>
<p>Need a rules refresher before a rated match? Use the <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a>, <a href="pickleball-rules-for-beginners.html">rules for beginners</a>, or <a href="pickleball-kitchen-rules.html">kitchen / NVZ rules</a>.</p>
{money_links()}
{faq_html}
{sources([("DUPR: How it works", DUPR_HOW, ""),
          ("DUPR: How your DUPR rating is calculated", DUPR_CALC, ""),
          ("DUPR: Algo update, win or lose your rating can go up", DUPR_ALGO, "July 8, 2025"),
          ("DUPR: DUPR rating percentiles", DUPR_PCT, "snapshot September 22, 2026"),
          ("The Dink: DUPR rating percentiles, where does your rating rank?", DINK_PCT, "Thomas Shields, October 7, 2026")])}
{more("guides/how-to-read-dupr-ratings.html")}'''
    page("guides/how-to-read-dupr-ratings.html", "How to Read DUPR Ratings: Scale Explained and Percentiles", dupr,
         "How to read DUPR ratings (DUPR explained): the 2.000 to 8.000 scale, four calculation factors, reliability score, and 2026 doubles percentiles from DUPR and The Dink.",
         fresh={"pct": PCT, "dist": DIST_ROWS, "faq": dupr_faq},
         schema=[faq_ld])

    # ----- Keyword pages, Oct 23, 2026 -----
    # Every price, date and venue fact below was read on the linked page on CHECKED.
    # Nothing here claims hands-on testing.
    import json as _json, pathlib as _pl, datetime as _dt
    CHECKED = "2026-10-23"
    checked = _dt.date.fromisoformat(CHECKED).strftime("%B %-d, %Y")
    ext = lambda u, t: f'<a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a>'

    # ----- Paddles under $30 -----
    SW_AMZ = "https://www.amazon.com/dp/B0GLYWT2VN"
    SW_INV = "https://theinventory.com/smartway-pickleball-paddles-set-of-2-usapa-approved-fiberglass-rackets-56ce1dfb"
    SW_INV_AUG = "https://theinventory.com/smartway-two-paddle-pickleball-set-deal"
    usd_prices = sorted(cur(p) for p in usd)
    cheapest = priced[0] if priced else None
    u30_faq = [
        ("Can you get a decent pickleball paddle for under $30?",
         f"We found one listing we could confirm under $30 on {checked}: a Smartway set of 2 fiberglass paddles with 4 balls and a carry bag at $29.99 on Amazon, list price $36.99. That is a beginner set, not a performance paddle. We have not played with it."),
        ("Is the Smartway 2-pack really $29.99?",
         f"It was on {checked}, for the Frost Nova blue and white color on Amazon, sold by SMARTWAY SPORT and shipped by Amazon. The Inventory also reported it at $29.99, and at $29.96 on August 31, 2026. Amazon prices change often and can differ by color, so check the price before you buy."),
        ("Why are there so few paddles on this page?",
         "Because we only list prices we could confirm on the retailer's own page, with the date we checked. Plenty of cheap paddles exist, but we did not find other sub-$30 prices we could verify for this page."),
        ("What is the cheapest paddle in the DropThePickle paddle list?",
         (f"The cheapest US-dollar price in our paddle list is ${usd_prices[0]:,.2f}, so nothing in that list is under $30." if usd_prices else "Our paddle list has no US-dollar prices right now.")),
    ]
    u30_faq_html, u30_faq_ld = faq(u30_faq)
    u30 = f'''<h1>Pickleball paddles under $30</h1>
<p class="meta">Only prices we confirmed on the retailer's page, with the date. Checked {checked}. The evidence is thin: we confirmed one listing.</p>
<h2>The short answer</h2>
<p>Under $30 you are buying a <b>beginner set</b>, usually two fiberglass paddles with balls and a bag. On {checked} we could confirm one listing at that price on the retailer's own page. We have not played with it, and this is not a ranking.</p>
<div class="tbl"><table><thead><tr><th>Listing</th><th>Price seen</th><th>What's included</th><th>Checked</th></tr></thead><tbody>
<tr><th scope="row">{ext(SW_AMZ, "Smartway Pickleball Paddles Set of 2 (Amazon)")}</th><td>$29.99 (list $36.99), Frost Nova blue/white</td><td>2 fiberglass paddles, 4 balls, 1 carry bag</td><td>{checked}</td></tr>
</tbody></table></div>
<h2>What the listing says</h2>
<ul>
<li>Sold by SMARTWAY SPORT, ships from Amazon, 30-day returns.</li>
<li>Fiberglass face and polypropylene honeycomb core, 16.53 x 7.67 inches, 4 1/4 inch grip.</li>
<li>Weight: the listing says 8 oz in its bullet points and 7.5 oz in its spec table, so treat weight as approximate.</li>
<li>Marketed as USAPA approved. Check the <a href="https://equipment.usapickleball.org/paddle-list/" target="_blank" rel="noopener">USA Pickleball approved paddle list</a> before using it in a sanctioned event.</li>
<li>4.6 out of 5 stars from 29 ratings on Amazon on {checked}.</li>
</ul>
<p>The deal was reported by {ext(SW_INV, "The Inventory")} at $29.99. It also covered the same set at $29.96 on {ext(SW_INV_AUG, "August 31, 2026")}. Amazon prices move daily and can differ by color, so the price you see may not match.</p>
<h2>Where the evidence is thin</h2>
<p>One confirmed listing is not a market survey. We did not find other sub-$30 prices we could confirm on a retailer page for this update, so we left them out instead of guessing. {"Our own paddle list starts at $" + format(usd_prices[0], ",.2f") + " in US dollars" if usd_prices else "Our own paddle list has no US-dollar prices"}, so none of the paddles we track are under $30.</p>
<p>If you can stretch your budget, the <a href="best-paddles-under-100.html">best paddles under $100</a> guide lists verified maker prices, and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a> explains what you give up at the low end.</p>
{money_links()}
{u30_faq_html}
{sources([("Amazon: Smartway Pickleball Paddles Set of 2 (ASIN B0GLYWT2VN)", SW_AMZ, f"$29.99, list $36.99, checked {checked}"),
          ("The Inventory: 2-Pack USAPA Pickleball Paddles Just $30 on Amazon", SW_INV, f"$29.99, seen {checked}"),
          ("The Inventory: This $30 Two-Paddle Pickleball Set Is Perfect for Beginners", SW_INV_AUG, "$29.96, August 31, 2026"),
          ("USA Pickleball approved paddle list", "https://equipment.usapickleball.org/paddle-list/", "")])}
{more("guides/pickleball-paddles-under-30.html")}'''
    page("guides/pickleball-paddles-under-30.html", "Pickleball paddles under $30: verified prices (Oct 2026)", u30,
         f"Pickleball paddles under $30, with only retailer-confirmed prices: a Smartway 2-paddle set at $29.99 on Amazon, checked {checked}. What it includes and where the evidence is thin.",
         fresh={"checked": CHECKED, "faq": u30_faq},
         schema=[u30_faq_ld])

    # ----- Six Zero lineup -----
    SZ_US = "https://us.sixzeropickleball.com/collections/paddles"
    SZ_LINEUP = [  # (model, US price as shown, note) from SZ_US on CHECKED
        ("Coral 16mm", "$200.00", ""), ("Coral 16mm Lightweight", "$200.00", ""), ("Coral Pro 16mm", "from $220.00", ""),
        ("Coral 'Rainbow' Edition 16mm", "$200.00", "edition"), ("Black Opal 14mm", "$220.00", ""),
        ("Black Opal 14mm Elongated", "$180.00", ""), ("Black Opal 'Year of the Horse' Edition 14mm", "$220.00", "edition"),
        ("Boulder Opal 14mm", "$220.00", ""), ("Ruby Pro 14mm", "$220.00", ""),
        ("Ruby Pro 'Dick's Sporting Goods' Edition 14mm", "$225.00", "edition"),
        ("Double Black Diamond \"Gold\" Limited Edition", "$180.00", "limited edition"),
        ("Double Black Diamond Control", "no price shown", ""), ("Quartz", "out of stock", ""),
    ]
    sz_ours = [p for p in PP if p["brand"] == "Six Zero"]
    try:
        _dc = _json.loads((_pl.Path(__file__).parent / "data/discount-codes.json").read_text())
        sz_codes = [c for c in _dc.get("codes", []) if c.get("brand") == "Six Zero"]
    except Exception:
        sz_codes = []
    sz_last = max((c.get("verified") or "" for c in sz_codes), default="")
    sz_code_line = (f"Our code tracker lists {len(sz_codes)} Six Zero code{'s' if len(sz_codes) != 1 else ''}, last checked {fmt(sz_last)}."
                    if sz_codes else "Our code tracker has no working Six Zero code right now.")
    def sz_row(p):
        pr = money(p) if p.get("price") else "not listed"
        return (f'<tr><th scope="row">{alink(p, p["model"])}</th><td>{e(p["core"]) or "not published"}</td>'
                f'<td>{e(p["weight"]) or "not published"}</td><td>{e(p["shape"]) or "not published"}</td><td>{e(pr)}</td></tr>')
    lineup_rows = "".join(f'<tr><th scope="row">{e(m)}</th><td>{e(pr)}</td><td>{e(n)}</td></tr>' for m, pr, n in SZ_LINEUP)
    sz_faq = [
        ("Did DropThePickle test Six Zero paddles?",
         "No. This page is a lineup overview built from Six Zero's own US site and the specs in our paddle list. We have not playtested these paddles, so there are no performance scores here."),
        ("How much do Six Zero paddles cost?",
         f"On Six Zero's US site on {checked}, regular models were listed from $180.00 to $220.00, and a Dick's Sporting Goods edition of the Ruby Pro was $225.00. Prices can change."),
        ("Which Six Zero paddles come in 14mm and 16mm?",
         "On the US site, the Black Opal, Boulder Opal and Ruby Pro models are listed as 14mm, and the Coral models as 16mm."),
        ("Is there a Six Zero discount code?", sz_code_line + " Codes are on our discount codes page with the date each was checked."),
    ]
    sz_faq_html, sz_faq_ld = faq(sz_faq)
    sz = f'''<h1>Six Zero paddle review: the 2026 lineup, specs and prices</h1>
<p class="meta">A lineup overview from Six Zero's US site and our paddle data, checked {checked}. Not a hands-on review: we have not playtested these paddles.</p>
<h2>What this page is</h2>
<p>People searching for a Six Zero paddle review usually want to know which models exist, how they differ, and what they cost. This page answers that from the maker's own listings. For opinions on how they play, watch the independent reviewers in our <a href="../reviews.html">paddle review roundup</a>.</p>
<h2>The US lineup on {checked}</h2>
<p>Prices as shown on {ext(SZ_US, "Six Zero's US paddle page")}, in US dollars.</p>
<div class="tbl"><table><thead><tr><th>Model</th><th>US price shown</th><th>Note</th></tr></thead><tbody>{lineup_rows}</tbody></table></div>
<p>The names carry the core thickness: the Coral models are 16mm, and the Black Opal, Boulder Opal and Ruby Pro are 14mm. Thicker cores are usually softer and more controlled, thinner cores more poppy; see <a href="paddle-weight-and-core.html">paddle weight and core</a>.</p>
<h2>What Six Zero says about its build</h2>
<ul>
<li>Six Zero says its paddles use its own Carbon Fusion Edge Technology: foam injection, then a lightweight carbon seam that fuses the top and bottom faces.</li>
<li>It describes the Ruby as having a 100% aramid fiber face with a textured 3K weave surface.</li>
<li>It offers a 12-month structural warranty.</li>
</ul>
<p>Those are the maker's claims, not our measurements.</p>
<h2>Specs in our paddle list</h2>
<p>These four Six Zero paddles are in our paddle list, with specs and prices from Six Zero's Australian site, so the prices are in Australian dollars.</p>
<div class="tbl"><table><thead><tr><th>Paddle</th><th>Core</th><th>Weight</th><th>Shape</th><th>Price</th></tr></thead><tbody>{"".join(sz_row(p) for p in sz_ours)}</tbody></table></div>
<p>Compare them with other brands on <a href="../best-six-zero-paddles.html">best Six Zero paddles</a> or the <a href="../compare.html">compare page</a>.</p>
<h2>Codes and deals</h2>
<p>{e(sz_code_line)} See the <a href="../discount-codes.html">discount codes page</a> and current <a href="../deals.html">paddle deals</a>.</p>
{sz_faq_html}
{sources([("Six Zero US: Pickleball Paddles", SZ_US, f"prices and model names, checked {checked}")] +
         [(f"Six Zero: {p['model']}", p["source_url"], "AUD specs in our paddle list") for p in sz_ours])}
{more("guides/six-zero-paddle-review.html")}'''
    page("guides/six-zero-paddle-review.html", "Six Zero paddle review 2026: lineup, specs and prices", sz,
         f"Six Zero paddle lineup for 2026: every model on Six Zero's US site with prices ($180 to $225) checked {checked}, specs from our paddle list, and Six Zero codes. Not a hands-on test.",
         fresh={"checked": CHECKED, "lineup": SZ_LINEUP, "ours": [(p["model"], p.get("price"), p["currency"]) for p in sz_ours], "codes": len(sz_codes), "faq": sz_faq},
         schema=[sz_faq_ld])

    # ----- Indoor vs outdoor pickleball balls (Oct 28, 2026) -----
    # Every spec below was read on the linked page on Oct 28, 2026. No prices, no playtest claims.
    B_ESM = "https://equipment.usapickleball.org/docs/Equipment-Standards-Manual.pdf"
    B_LIST = "https://equipment.usapickleball.org/view/ball-list/"
    B_X40 = "https://franklinsports.com/x-40-outdoor-pickleball-packs"
    B_X26 = "https://franklinsports.com/x-26-indoor-pickleball-packs"
    B_LT_PPA = "https://www.ppatour.com/lt-pro-48-pickleball-named-official-ball-of-carvana-ppa-tour/"
    B_LT_MLP = "https://www.prnewswire.com/news-releases/life-times-lt-pro-48-pickleball-named-official-ball-of-major-league-pickleball-2026-season-kicks-off-in-dallas-may-22-302757035.html"
    B_LT_SPEC = "https://pickleballcentral.com/life-time-lt-pro-48-pickleball/"
    B_APP = "https://stories.franklinsports.com/franklin-x40-named-official-ball-of-app-tour"
    B_PPA_BLOG = "https://www.ppatour.com/ppa-blog/how-to-pick-the-perfect-pickleball/"
    BALL_SPEC = [
        ("Diameter", "2.87 to 2.97 in (7.29 to 7.54 cm), out-of-round no more than +/-0.020 in", "2.D.3"),
        ("Weight", "0.78 to 0.935 oz (22.1 to 26.5 g)", "2.D.4"),
        ("Bounce", "30 to 34 in (76.2 to 86.4 cm) to the top of the ball, dropped from 78 in (198.1 cm) onto a granite plate at 70°F +/- 5°F", "2.D.5"),
        ("Compression", "Average under 43 lbf (ASTM F1888-09 test)", "2.D.6"),
        ("Hardness", "40 to 50 Durometer D, recorded for data only and no longer a pass/fail requirement", "2.D.7"),
        ("Holes", "26 to 40 circular holes", "2.D.8"),
        ("Surface", "Smooth, no texturing, one uniform color; a slight seam ridge is allowed", "2.D.1"),
    ]
    BALLS = [
        ("Franklin X-26", "26", "Two-piece", "Indoor", "Franklin: approved for indoor tournament play by USA Pickleball", B_X26),
        ("Franklin X-40", "40", "One-piece polyethylene, machine-drilled holes", "Outdoor", "Franklin: official ball of the US Open Pickleball Championships and of USA Pickleball", B_X40),
        ("Life Time LT Pro 48", "48", "Two-piece, injection molded; 26 g, 2.9 in", "Indoor and outdoor (seller)", "Official ball of the PPA Tour (since Aug. 2025) and MLP (2026 season)", B_LT_SPEC),
    ]
    ball_faq = [
        ("What is the difference between indoor and outdoor pickleball balls?",
         "Hole size and count. The 2026 USA Pickleball rulebook says the ball with larger holes is customarily used indoors and the ball with smaller holes is customarily used outdoors. Franklin's X-26 indoor ball has 26 holes and its X-40 outdoor ball has 40."),
        ("Can you use an outdoor pickleball indoors?",
         "Yes. Rule 3.C.1 of the 2026 USA Pickleball rulebook says all approved balls are acceptable for indoor or outdoor play. Indoor and outdoor are customary uses, not a rule."),
        ("How many holes does a pickleball have?",
         "USA Pickleball's Equipment Standards Manual (Rev. 3.0, January 2025) calls for 26 to 40 circular holes. Franklin's X-26 has 26 and its X-40 has 40. Life Time's LT Pro 48, the PPA Tour and MLP ball, has 48."),
        ("What ball do the pros use?",
         "The PPA Tour named the Life Time LT Pro 48 its exclusive ball on August 1, 2025, and Major League Pickleball named it its official ball on April 29, 2026. Franklin says its X-40 is the official ball of the US Open Pickleball Championships, and the APP Tour named the X-40 its exclusive ball in March 2024."),
        ("What are the official pickleball ball size and weight?",
         "USA Pickleball's Equipment Standards Manual sets a diameter of 2.87 to 2.97 inches, a weight of 0.78 to 0.935 ounces (22.1 to 26.5 grams), and a bounce of 30 to 34 inches when dropped from 78 inches onto granite."),
        ("Which ball do I need for a USA Pickleball sanctioned tournament?",
         "Whatever the tournament director picks. Under the Equipment Standards Manual (2.D.2), the director chooses the tournament ball, and it must be on USA Pickleball's approved ball list."),
    ]
    ball_faq_html, ball_faq_ld = faq(ball_faq)
    spec_rows = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td><td>{e(r)}</td></tr>' for k, v, r in BALL_SPEC)
    ball_rows = "".join(f'<tr><th scope="row"><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></th><td>{e(h)}</td><td>{e(c)}</td><td>{e(use)}</td><td>{e(note)}</td></tr>' for n, h, c, use, note, u in BALLS)
    balls = f'''<h1>Indoor vs outdoor pickleball balls</h1>
<p class="meta">What actually separates an indoor ball from an outdoor ball, the official USA Pickleball specs, and which balls the pro tours use. From the 2026 USA Pickleball rulebook, the Equipment Standards Manual and the makers' own pages, read October 28, 2026.</p>
<h2>The short answer</h2>
<ul>
<li><b>Indoor balls have fewer, larger holes.</b> Franklin's <a href="{B_X26}" target="_blank" rel="noopener">X-26</a> indoor ball has 26.</li>
<li><b>Outdoor balls have more, smaller holes.</b> Franklin's <a href="{B_X40}" target="_blank" rel="noopener">X-40</a> outdoor ball has 40.</li>
<li><b>Either one is legal on either surface.</b> Rule 3.C.1 of the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball rulebook</a> says all approved balls are acceptable for indoor or outdoor play. The rulebook's Figure 3-2 only says the larger-hole ball is <i>customarily</i> used indoors and the smaller-hole ball outdoors.</li>
</ul>
<h2>Official ball specs</h2>
<p>The 2026 rulebook (Rule 3.C) covers the basics: one uniform color, a maker's name or logo on the ball, and a smooth, untextured surface. The numbers live in USA Pickleball's <a href="{B_ESM}" target="_blank" rel="noopener">Equipment Standards Manual</a> (Revision 3.0, January 2025), section 2.D:</p>
<div class="tbl"><table><thead><tr><th>Spec</th><th>Requirement</th><th>ESM rule</th></tr></thead><tbody>{spec_rows}</tbody></table></div>
<p>Under 2.D.2, the tournament director chooses the ball for a sanctioned event, and it must be on USA Pickleball's <a href="{B_LIST}" target="_blank" rel="noopener">approved ball list</a>. That list labels each ball <b>Out</b> (outdoor), <b>Ind</b> (indoor) or <b>I/O</b> (both). The newest listings we saw on October 28, 2026 were dated October 22, 2026, including the AMP Easy Rally 40 and Drip (Out) and the GUNICA G-Pro1 and MINGLR MX40 (I/O).</p>
<h2>Three balls, side by side</h2>
<p>Facts as each maker or seller publishes them. We have not lab-tested or play-tested these balls.</p>
<div class="tbl"><table><thead><tr><th>Ball</th><th>Holes</th><th>Construction</th><th>Made for</th><th>Notable</th></tr></thead><tbody>{ball_rows}</tbody></table></div>
<p>The LT Pro 48 has more holes than the 26-to-40 range in the Equipment Standards Manual's ball section. If you are entering a USA Pickleball sanctioned tournament, use the ball the tournament director names from the approved list.</p>
<h2>What ball do the pros use?</h2>
<ul>
<li><b>PPA Tour:</b> the <a href="{B_LT_PPA}" target="_blank" rel="noopener">PPA announced on August 1, 2025</a> that the Life Time LT Pro 48 would be the exclusive ball of all its tournaments and events, starting in Bristol, Tenn. The announcement says the ball has symmetrically spaced holes with chamfered edges to reduce cracking.</li>
<li><b>Major League Pickleball:</b> <a href="{B_LT_MLP}" target="_blank" rel="noopener">Life Time and MLP named the LT Pro 48 MLP's official ball on April 29, 2026</a>, ahead of the 2026 season.</li>
<li><b>US Open and USA Pickleball:</b> <a href="{B_X40}" target="_blank" rel="noopener">Franklin says</a> the X-40 was chosen as the official ball of the US Open Pickleball Championships and of USA Pickleball.</li>
<li><b>APP Tour:</b> the APP named the Franklin X-40 the <a href="{B_APP}" target="_blank" rel="noopener">exclusive ball of the APP Tour and APP Next Gen Series</a> in March 2024.</li>
</ul>
<p>Watching the pros this fall? See the <a href="../events/opendoor-pickleball-world-championships.html">PPA Worlds 2026 guide</a> and <a href="../events/usa-pickleball-nationals-2026.html">USA Pickleball Nationals 2026</a>.</p>
<h2>How to pick one</h2>
<ul>
<li><b>Gym floor or indoor court:</b> a larger-hole indoor ball is the customary choice. The PPA Tour's <a href="{B_PPA_BLOG}" target="_blank" rel="noopener">ball guide</a> (January 2024) says the Jugs indoor ball's wider holes mean less skipping on a gym floor, but notes that ball is not USA Pickleball approved; it points indoor tournament players to the approved Onix Pure 2.</li>
<li><b>Concrete or asphalt outdoors:</b> a 40-hole outdoor ball is the customary choice. Franklin describes the X-40's one-piece polyethylene build as made to resist denting and cracking on outdoor courts.</li>
<li><b>Want to practice with the tour ball:</b> the PPA Tour and MLP use the LT Pro 48.</li>
<li><b>Playing a sanctioned event:</b> check the event's named ball, then confirm it on the <a href="{B_LIST}" target="_blank" rel="noopener">USA Pickleball ball list</a>.</li>
<li><b>New player:</b> the same PPA guide calls the Onix Dura Fast 40 a "fast" ball that is not ideal for beginners or indoor surfaces.</li>
</ul>
<p>Buying balls with a new paddle? Check <a href="../discount-codes/franklin.html">Franklin discount codes</a> and <a href="../discount-codes/onix.html">Onix discount codes</a>.</p>
{money_links()}
{ball_faq_html}
{sources([("USA Pickleball: 2026 Official Rulebook", RULES, "Rule 3.C and Figure 3-2"),
          ("USA Pickleball: Equipment Standards Manual", B_ESM, "Revision 3.0, January 2025, section 2.D"),
          ("USA Pickleball: Approved ball list", B_LIST, "read October 28, 2026"),
          ("Franklin Sports: X-40 Outdoor Pickleballs", B_X40, "read October 28, 2026"),
          ("Franklin Sports: X-26 Indoor Pickleballs", B_X26, "read October 28, 2026"),
          ("PPA Tour: LT Pro 48 named official ball of the Carvana PPA Tour", B_LT_PPA, "August 1, 2025"),
          ("Life Time via PR Newswire: LT Pro 48 named official ball of Major League Pickleball", B_LT_MLP, "April 29, 2026"),
          ("Pickleball Central: Life Time LT Pro 48 specifications", B_LT_SPEC, "read October 28, 2026"),
          ("Franklin Sports: X-40 named official ball of APP Tour", B_APP, "March 19, 2024"),
          ("PPA Tour: How to pick the perfect pickleball", B_PPA_BLOG, "Andrew Gilman, January 25, 2024")])}
{more("guides/indoor-vs-outdoor-pickleball-balls.html")}'''
    page("guides/indoor-vs-outdoor-pickleball-balls.html", "Indoor vs outdoor pickleball balls: holes, specs and pro balls (2026)", balls,
         "Indoor vs outdoor pickleball balls: 26 vs 40 holes, official USA Pickleball size, weight and bounce specs, and the balls the PPA Tour, MLP and US Open use.",
         fresh={"spec": BALL_SPEC, "balls": BALLS, "faq": ball_faq},
         schema=[ball_faq_ld])

    # ----- How to choose pickleball shoes (Nov 2, 2026) -----
    # Evergreen. Every claim is paraphrased or quoted from a source read on SH_CHECKED. No shoe rankings, prices or codes are invented;
    # the brand list below is built from data/discount-codes.json at build time (brands whose tracked code conditions mention shoes).
    SH_CHECKED = "2026-11-02"
    sh_checked = _dt.date.fromisoformat(SH_CHECKED).strftime("%B %-d, %Y")
    SH_AAOS = "https://www.orthoinfo.org/staying-healthy/athletic-shoes/"
    SH_AAPSM = "https://www.aapsm.org/sport-shoes.html"
    SH_AMA = "https://www.ama-assn.org/public-health/prevention-wellness/what-doctors-want-patients-know-about-preventing-pickleball"
    SH_CSMR = "https://pubmed.ncbi.nlm.nih.gov/33031206/"
    SH_ASICS = "https://www.asics.com/us/en-us/blog/a-guide-to-pickleball-shoes/"
    SH_SELKIRK = "https://www.selkirk.com/blogs/paddles-and-product-education/pickleball-shoe-faq"
    import json as _json, pathlib as _pl, re as _re
    try:
        _dc = _json.loads((_pl.Path(__file__).parent / "data" / "discount-codes.json").read_text())
    except Exception:
        _dc = {}
    shoe_brands = sorted({c["brand"] for c in _dc.get("codes", []) if "shoe" in (c.get("conditions") or "").lower()}, key=str.lower)
    _sb = lambda b: _re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")
    shoe_links = ", ".join(f'<a href="../discount-codes/{_sb(b)}.html">{e(b)}</a>' for b in shoe_brands)
    SH_CMP = [
        ("Built for", "Quick cuts, side-to-side movement and sudden stops (AAPSM, AAOS)", "Forward, heel-to-toe motion (AAPSM)"),
        ("Sides and upper", "Built up on the inside and outside edges for stability; firmer sides (AAPSM, AMA)", "Less lateral support (AMA, ASICS)"),
        ("Sole", "Solid tread (AAOS), wider soles that flare past the upper (AAPSM), firmer outsoles (AMA)", "Softer, more cushioned (AMA)"),
        ("Main job", "Help keep the foot from rolling during lateral moves (AAPSM)", "Absorb repeated impact when running (AAPSM)"),
    ]
    shoe_faq = [
        ("Can you wear running shoes for pickleball?",
         "It is not recommended. The American Academy of Podiatric Sports Medicine says running shoes are designed for heel-to-toe movement and not for side-to-side movement, pivoting or spinning. A 2020 review in Current Sports Medicine Reports says proper court shoes are a must and that running sneakers, built for linear movement, do not give enough support for other directions."),
        ("Can I wear tennis shoes for pickleball?",
         "Yes. Selkirk's shoe FAQ says that if you do not wear a pickleball-specific shoe, tennis shoes are the best option because both sports use similar side-to-side movement. In an American Medical Association Q&A, sports medicine physician Christopher Wu, MD, also suggests a tennis shoe with firm sides and grip."),
        ("What is the difference between indoor and outdoor pickleball shoes?",
         "The rubber. Selkirk says indoor pickleball shoes use softer materials such as gum rubber to protect the floor, while outdoor shoes use harder rubber to stand up to surfaces such as asphalt and concrete. ASICS says the tough rubber of outdoor shoes can scuff hardwood, and that soft indoor soles wear down faster on asphalt."),
        ("Do I really need pickleball-specific shoes?",
         "Not necessarily, but you do want a court shoe. The AAOS says that if you play one sport more than two times a week, you should buy a shoe designed for that sport, and the AAPSM says regular pickleball players should consider a sport-specific shoe. Any court shoe built for lateral movement, including a tennis shoe, fits that advice."),
        ("How long do pickleball shoes last?",
         "There is no fixed number. Selkirk says it depends on how often and how long you play, your style and whether you play indoors or outdoors, and that pickleball shoes can last anywhere from a few months to a few years."),
        ("How should pickleball shoes fit?",
         "The AAOS suggests trying shoes on at the end of the day in the socks you play in, leaving at least a half inch between your longest toe and the tip of the shoe, making sure the heel counter grips your heel, and lacing them up fully before you judge the fit."),
    ]
    shoe_faq_html, shoe_faq_ld = faq(shoe_faq)
    cmp_rows = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(a)}</td><td>{e(b)}</td></tr>' for k, a, b in SH_CMP)
    shoes = f'''<h1>How to choose pickleball shoes: court shoes vs running shoes</h1>
<p class="meta">Can you play pickleball in running shoes? What separates a court shoe, and do you need separate indoor and outdoor pairs? Answers from sports medicine groups and shoe makers, read {sh_checked}. We have not wear-tested or ranked any shoe.</p>
<h2>The short answer</h2>
<ul>
<li><b>Wear a court shoe, not a running shoe.</b> The <a href="{SH_AAPSM}" target="_blank" rel="noopener">American Academy of Podiatric Sports Medicine</a> (AAPSM) says running shoes are built for heel-to-toe movement and are not designed for side-to-side movement, pivoting or spinning. A <a href="{SH_CSMR}" target="_blank" rel="noopener">2020 review in <i>Current Sports Medicine Reports</i></a> says proper court shoes are a must for pickleball.</li>
<li><b>A pickleball shoe or a tennis shoe both work.</b> <a href="{SH_SELKIRK}" target="_blank" rel="noopener">Selkirk</a> calls tennis shoes the best option if you skip pickleball-specific shoes, because the movements are similar.</li>
<li><b>Match the sole to the court.</b> Softer gum-rubber soles for indoor floors, harder rubber for outdoor asphalt and concrete (Selkirk, ASICS).</li>
</ul>
<h2>Court shoes vs running shoes</h2>
<p>Pickleball is played in short bursts: shuffles along the kitchen line, lunges for dinks and quick stops. The AAPSM lists the features that make court shoes different. The <a href="{SH_AAOS}" target="_blank" rel="noopener">American Academy of Orthopaedic Surgeons</a> (AAOS) adds that court shoes have a solid tread and are designed to provide stability in all directions.</p>
<div class="tbl"><table><thead><tr><th></th><th>Court shoe (pickleball, tennis)</th><th>Running shoe</th></tr></thead><tbody>{cmp_rows}</tbody></table></div>
<p>In an <a href="{SH_AMA}" target="_blank" rel="noopener">American Medical Association Q&amp;A</a>, Atlantic Health sports medicine physician Christopher Wu, MD, says tennis shoes have firmer outsoles for cutting and pivoting, while a running shoe "likely will have more cushioning, but not as much support, especially when you're making lateral movements." He also says that "most importantly, a shoe should be comfortable."</p>
<p>The <i>Current Sports Medicine Reports</i> review (Vitale and Liu, 2020) notes there are no evidence-based equipment studies for pickleball yet, so its advice comes from the authors' clinical experience. It still recommends court shoes, not running sneakers, for all players because of injury risk.</p>
<h2>Indoor vs outdoor pickleball shoes</h2>
<ul>
<li><b>Indoor (gym floors, hardwood):</b> Selkirk says indoor shoes use softer materials such as gum rubber, which grips while protecting the floor. <a href="{SH_ASICS}" target="_blank" rel="noopener">ASICS</a> says the tough rubber on outdoor shoes is likely to leave scuff marks on hardwood.</li>
<li><b>Outdoor (asphalt, concrete):</b> both makers say outdoor shoes use harder, stronger rubber to handle gritty court surfaces.</li>
<li><b>One pair for both?</b> ASICS says you can wear indoor shoes outside, but the soft rubber wears down faster on asphalt. Selkirk says two pairs are worth considering depending on how much you play, but a pickleball-specific shoe can handle both.</li>
</ul>
<p>Balls change indoors and outdoors too. See <a href="indoor-vs-outdoor-pickleball-balls.html">indoor vs outdoor pickleball balls</a>.</p>
<h2>What to look for</h2>
<ul>
<li><b>Lateral support:</b> a supportive upper or reinforced side walls (ASICS); sides built up on the inside and outside of the shoe (AAPSM).</li>
<li><b>Traction that fits your court:</b> see indoor vs outdoor above.</li>
<li><b>Cushioning:</b> ASICS points to shock absorption for the running, jumping and turning in a match.</li>
<li><b>A heel that stays put:</b> the AAOS says the heel counter, the back of the shoe, should grip your heel.</li>
<li><b>Fit and comfort:</b> Selkirk's checklist covers toe room, heel fit, width and weight.</li>
</ul>
<h2>How to try them on</h2>
<p>From the AAOS shoe-buying tips:</p>
<ul>
<li>Shop at the end of the day or after a workout, because feet swell during the day.</li>
<li>Wear the socks you play in.</li>
<li>Leave at least a half inch between your longest toe and the tip of the shoe, with room to wiggle your toes.</li>
<li>Lace them up fully, try on both shoes and walk on more than one surface.</li>
<li>If you play one sport more than two times a week, buy a shoe made for that sport.</li>
</ul>
<h2>When to replace them</h2>
<p>Selkirk says there is no single answer: it depends on how often and how long you play, your playing style and whether you play indoors or outdoors, so pickleball shoes can last from a few months to a few years. The AAOS adds that cushioning can become less effective over time, even in shoes that have sat unused on a shelf.</p>
<h2>Shoe discount codes</h2>
<p>{f"These brands have a tracked discount code whose terms mention shoes: {shoe_links}. Each brand page shows the code, its source and the terms." if shoe_links else "Check the brand pages on our discount code list for codes that cover shoes."} Check the terms before you buy.</p>
<p>New player? Start with <a href="pickleball-rules-for-beginners.html">pickleball rules for beginners</a>, <a href="how-to-dink.html">how to dink</a> and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a>.</p>
{money_links()}
{shoe_faq_html}
{sources([("AAPSM: Footwear – Court Sport Shoes", SH_AAPSM, f"American Academy of Podiatric Sports Medicine, read {sh_checked}"),
          ("AAOS OrthoInfo: Athletic Shoes", SH_AAOS, f"American Academy of Orthopaedic Surgeons, read {sh_checked}"),
          ("AMA: What doctors want patients to know about preventing pickleball injuries", SH_AMA, "Sara Berg, with Christopher Wu, MD"),
          ("Vitale K, Liu S. Pickleball: Review and Clinical Recommendations for this Fast-growing Sport", SH_CSMR, "Current Sports Medicine Reports, 2020;19(10):406-413"),
          ("ASICS: A Guide to Pickleball Shoes", SH_ASICS, "August 15, 2024"),
          ("Selkirk: Pickleball shoe FAQ", SH_SELKIRK, "Jaclyn Brandt, August 6, 2024")])}
{more("guides/how-to-choose-pickleball-shoes.html")}'''
    page("guides/how-to-choose-pickleball-shoes.html", "How to choose pickleball shoes: court vs running shoes", shoes,
         "Can you play pickleball in running shoes? Court shoes vs running shoes, indoor vs outdoor soles, and fit tips, from the AAOS, AAPSM, AMA and shoe makers.",
         fresh={"cmp": SH_CMP, "faq": shoe_faq, "brands": shoe_brands},
         schema=[shoe_faq_ld])

    # ----- Pickleball court dimensions (Nov 3, 2026) -----
    # Evergreen. Measurements come from the 2026 USA Pickleball Official Rulebook (Section 3), USA Pickleball's
    # court construction page and its court layout diagram, and the ITF 2026 Rules of Tennis, all read on CD_CHECKED.
    # Square-foot totals and the tennis comparison are our own arithmetic from those numbers.
    CD_CHECKED = "2026-11-03"
    cd_checked = _dt.date.fromisoformat(CD_CHECKED).strftime("%B %-d, %Y")
    CD_CONSTR = "https://usapickleball.org/construction/"
    CD_DIAGRAM = "https://usapickleball.org/wp-content/uploads/2025/09/court-construction-layout-diagram.jpg"
    CD_MANUAL = "https://usapickleball.org/construction/manual/"
    CD_ITF = "https://www.itftennis.com/media/7221/2026-rules-of-tennis-english.pdf"
    CD_SPEC = [
        ("Court (singles and doubles)", "20 ft x 44 ft", "6.10 m x 13.41 m", "Rule 3.A.1"),
        ("Non-volley zone (kitchen), each side", "7 ft deep x 20 ft wide", "2.13 m deep", "Rule 3.A.4.c"),
        ("Service court, each", "10 ft wide x 15 ft deep", "", "USA Pickleball court diagram"),
        ("Line width", "2 in", "5.08 cm", "Rule 3.A.4.e"),
        ("Net height at the sidelines", "36 in (+/- 1/4 in)", "91.44 cm", "Rule 3.B.6"),
        ("Net height at the center", "34 in (+/- 1/4 in)", "86.36 cm", "Rule 3.B.7"),
        ("Net post spacing (inside to inside)", "22 ft (+/- 1 in)", "6.71 m", "Rule 3.B.2"),
        ("Net post diameter (max)", "3 in", "7.62 cm", "Rule 3.B.2"),
        ("Net length (min)", "21 ft 9 in", "6.63 m", "Rule 3.B.3"),
        ("Net height, bottom edge to top (min)", "30 in", "76.2 cm", "Rule 3.B.3"),
        ("Corner-to-corner diagonal", "48 ft 4 in (+/- 3/4 in)", "", "USA Pickleball court diagram"),
    ]
    CD_AREA = [
        ("The court itself", "20 x 44 ft", "6.10 x 13.41 m", "880"),
        ("Minimum playing surface", "30 x 60 ft", "9.14 x 18.29 m", "1,800"),
        ("New construction (recommended)", "34 x 64 ft", "10.36 x 19.5 m", "2,176"),
        ("Tournament play (recommended)", "34 x 64 ft", "10.36 x 19.5 m", "2,176"),
        ("Stadium court (recommended)", "50 x 80 ft", "15.24 x 24.38 m", "4,000"),
    ]
    CD_TOL = [
        ("Net line to outside of the kitchen line", "7 ft", "+/- 1/8 in"),
        ("Net line to outside of the baseline", "22 ft", "+/- 1/4 in"),
        ("Outside sideline to outside sideline", "20 ft", "+/- 1/4 in"),
        ("Outside sideline to the centerline", "10 ft", "+/- 1/8 in"),
        ("Diagonal, to the outside of the lines", "48 ft 4 in", "+/- 3/4 in"),
    ]
    CD_TENNIS = [
        ("Court length", "44 ft", "78 ft"),
        ("Court width", "20 ft (singles and doubles)", "27 ft singles, 36 ft doubles"),
        ("Net height at center", "34 in", "3 ft (36 in)"),
        ("Net height at the posts/sidelines", "36 in at the sidelines", "3 1/2 ft (42 in) at the posts"),
        ("Front zone", "7 ft non-volley zone (kitchen)", "No volley restriction"),
    ]
    cd_faq = [
        ("What are the dimensions of a pickleball court?",
         "A pickleball court is 20 feet wide and 44 feet long (6.10 m by 13.41 m) for both singles and doubles, per Rule 3.A.1 of the 2026 USA Pickleball Official Rulebook. Measurements are taken to the outside edge of the lines."),
        ("How big is the kitchen on a pickleball court?",
         "The non-volley zone, or kitchen, is 7 feet deep and 20 feet wide on each side of the net (Rule 3.A.4.c). All lines that bound it are part of the zone, so a foot on the kitchen line counts as being in the kitchen."),
        ("How much space do you need for a pickleball court?",
         "The 2026 rulebook sets the minimum playing surface at 30 by 60 feet (about 1,800 square feet). It recommends 34 by 64 feet for new construction and tournament play, and 50 by 80 feet for a stadium court."),
        ("How high is a pickleball net?",
         "36 inches at the sidelines and 34 inches at the center, each within a quarter inch, per Rules 3.B.6 and 3.B.7. If the net has a center strap, the 34-inch measurement includes the strap."),
        ("Are singles and doubles pickleball courts the same size?",
         "Yes. Unlike tennis, pickleball uses the same 20 by 44 foot court for singles and doubles. Mini-singles is also played on a standard court, with only one half of each end in play during a rally."),
        ("How do I check that a court I taped out is square?",
         "Measure the diagonal. USA Pickleball's court layout diagram gives the corner-to-corner diagonal as 48 feet 4 inches, plus or minus 3/4 inch, measured to the outside of the lines. If both diagonals match that, the rectangle is square."),
        ("How does a pickleball court compare to a tennis court?",
         "A tennis court is 78 feet long and 36 feet wide for doubles, per the ITF Rules of Tennis, versus 20 by 44 feet for pickleball. The tennis net is 3 feet high at the center, 2 inches higher than a pickleball net's 34 inches."),
    ]
    cd_faq_html, cd_faq_ld = faq(cd_faq)
    cd_spec_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c) or "—"}</td><td>{e(d)}</td></tr>' for a, b, c, d in CD_SPEC)
    cd_area_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in CD_AREA)
    cd_tol_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in CD_TOL)
    cd_ten_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in CD_TENNIS)
    court = f'''<h1>Pickleball court dimensions: size, kitchen, net height and layout (2026)</h1>
<p class="meta">Every measurement on this page is from the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball Official Rulebook</a> (Section 3, Court and Equipment) and USA Pickleball's <a href="{CD_CONSTR}" target="_blank" rel="noopener">court construction page</a> and layout diagram, read {cd_checked}. Square-foot totals are our own math. If you are building a permanent court, use a professional court builder.</p>
<h2>The short answer</h2>
<ul>
<li><b>Court:</b> 20 feet wide by 44 feet long, the same for singles and doubles (Rule 3.A.1).</li>
<li><b>Kitchen:</b> 7 feet deep on each side of the net, the full 20-foot width (Rule 3.A.4.c).</li>
<li><b>Net:</b> 36 inches high at the sidelines, 34 inches at the center (Rules 3.B.6 and 3.B.7).</li>
<li><b>Space you need:</b> at least 30 by 60 feet of playing surface; 34 by 64 feet is recommended for new courts (Rule 3.A.3).</li>
</ul>
<h2>Court measurements</h2>
<p>All measurements are made to the <b>outside edge</b> of the perimeter and kitchen lines (Rule 3.A.2), so the lines are part of the 20 by 44 foot court. The <a href="{CD_DIAGRAM}" target="_blank" rel="noopener">USA Pickleball court diagram</a> shows each service court as 10 feet wide and 15 feet deep: the 22 feet from the net to the baseline, minus the 7-foot kitchen.</p>
<div class="tbl"><table><thead><tr><th>Part</th><th>Imperial</th><th>Metric</th><th>Source</th></tr></thead><tbody>{cd_spec_rows}</tbody></table></div>
<h2>The lines and areas</h2>
<ul>
<li><b>Baselines</b> run parallel to the net at each end. <b>Sidelines</b> run the length of the court (Rules 3.A.4.a and b).</li>
<li><b>The kitchen (non-volley zone)</b> is the 7 by 20 foot area next to the net on each side. All lines that bound it are part of the zone, and the rulebook says it is two-dimensional: it does not extend above the playing surface (Rule 3.A.4.c).</li>
<li><b>The centerline</b> runs from the kitchen line to the baseline and splits the right and left service courts (Rule 3.A.4.d). It does not run through the kitchen.</li>
<li><b>Service courts</b> include their baseline, sideline and the centerline, so a serve landing on any of those lines is in. Because the kitchen line belongs to the kitchen, a serve that lands on it is short (see our <a href="pickleball-rules-for-beginners.html">rules for beginners</a>).</li>
<li><b>Lines</b> should be 2 inches wide and all one color that clearly contrasts with the court (Rule 3.A.4.e).</li>
</ul>
<h2>The net</h2>
<p>The net sits 2 inches lower in the middle than at the sidelines: <b>36 inches</b> where it crosses the outer edge of the sidelines and <b>34 inches</b> at the center, each within a quarter inch. A center strap, placed 10 feet from the outside edge of the sidelines, may be used to pull it down to 34 inches, and the center measurement includes the strap (Rules 3.B.5 to 3.B.7).</p>
<p>The posts should be 22 feet apart, inside to inside, within an inch, and no more than 3 inches in diameter. The net itself should be at least 21 feet 9 inches long and at least 30 inches from bottom edge to top, with a 2-inch white tape binding over a cord or cable along the top (Rules 3.B.2 to 3.B.4). USA Pickleball's diagram recommends the posts sit 12 inches outside each sideline.</p>
<h2>How much space you need</h2>
<p>The court is 880 square feet, but players need room to run behind the baseline and outside the sidelines. Rule 3.A.3 sets the minimum playing surface and lists recommended sizes:</p>
<div class="tbl"><table><thead><tr><th>Purpose</th><th>Feet</th><th>Meters</th><th>Square feet (our math)</th></tr></thead><tbody>{cd_area_rows}</tbody></table></div>
<p>By our math, the minimum 30 by 60 foot area leaves 5 feet on each side of the court and 8 feet behind each baseline. For orientation, USA Pickleball's <a href="{CD_CONSTR}" target="_blank" rel="noopener">construction page</a> says outdoor courts should run north to south so players don't look straight into the sun in the morning or late afternoon.</p>
<h2>Laying out a court: check your measurements</h2>
<p>Taping a temporary court in a gym or driveway? Use the tolerances from USA Pickleball's <a href="{CD_DIAGRAM}" target="_blank" rel="noopener">court layout diagram</a>, all measured to the outside of the lines:</p>
<div class="tbl"><table><thead><tr><th>Measure</th><th>Target</th><th>Tolerance</th></tr></thead><tbody>{cd_tol_rows}</tbody></table></div>
<p>The diagonal is the quick way to check the court is square: if both corner-to-corner measurements come out at 48 feet 4 inches, the corners are right angles. Tape or paint 2-inch lines, then measure the net at the sidelines and the center before you play.</p>
<h2>Pickleball court vs tennis court</h2>
<p>Tennis numbers are from the <a href="{CD_ITF}" target="_blank" rel="noopener">ITF 2026 Rules of Tennis</a>.</p>
<div class="tbl"><table><thead><tr><th></th><th>Pickleball</th><th>Tennis</th></tr></thead><tbody>{cd_ten_rows}</tbody></table></div>
<p>By our math, a pickleball court (880 square feet) is under a third of a doubles tennis court (78 by 36 feet, 2,808 square feet). Planning to convert tennis courts? USA Pickleball and the American Sports Builders Association publish a <a href="{CD_MANUAL}" target="_blank" rel="noopener">court construction and maintenance manual</a> with a section on tennis conversions.</p>
<h2>Gear for your court</h2>
<p>Court surface changes the ball you should use: see <a href="indoor-vs-outdoor-pickleball-balls.html">indoor vs outdoor pickleball balls</a>. Gym floor or asphalt also changes your shoes: see <a href="how-to-choose-pickleball-shoes.html">how to choose pickleball shoes</a>. Then learn the shot that lives in that 7-foot zone in <a href="how-to-dink.html">how to dink</a>, and check the <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a>.</p>
{money_links()}
{cd_faq_html}
{sources([("USA Pickleball: 2026 Official Rulebook", RULES, f"Section 3, Court and Equipment (Rules 3.A and 3.B), read {cd_checked}"),
          ("USA Pickleball: Pickleball court construction, lighting and shading", CD_CONSTR, f"court dimensions and north-south orientation, read {cd_checked}"),
          ("USA Pickleball: Court construction layout diagram", CD_DIAGRAM, "service court size, line tolerances, diagonal and net post placement"),
          ("USA Pickleball: Court construction and maintenance manual", CD_MANUAL, "USA Pickleball and ASBA manual, 2023 edition"),
          ("ITF: 2026 Rules of Tennis", CD_ITF, f"Rule 1, The Court, read {cd_checked}")])}
{more("guides/pickleball-court-dimensions.html")}'''
    page("guides/pickleball-court-dimensions.html", "Pickleball Court Dimensions: Size, Kitchen and Net Height (2026)", court,
         "Pickleball court dimensions from the 2026 USA Pickleball rulebook: 20 x 44 ft court, 7 ft kitchen, 36/34 in net, 30 x 60 ft minimum space, layout tolerances and tennis comparison.",
         fresh={"checked": CD_CHECKED, "spec": CD_SPEC, "area": CD_AREA, "tol": CD_TOL, "tennis": CD_TENNIS, "faq": cd_faq},
         schema=[cd_faq_ld])

    # ----- Pickleball grip size (Nov 4, 2026) -----
    # Evergreen. Sizing methods and grip options are from Selkirk's grip-size article and grip guide and ARTI's grip-size guide;
    # the grip-alteration rules are from the 2026 USA Pickleball Official Rulebook (Rule 3.D); the Volair table is built from
    # data/paddles.json (maker specs, re-read on volair.com on GR_CHECKED). Nothing here is a playtest or our own sizing chart.
    GR_CHECKED = "2026-11-04"
    gr_checked = _dt.date.fromisoformat(GR_CHECKED).strftime("%B %-d, %Y")
    GR_SLK = "https://www.selkirk.com/blogs/pickleball-education/how-do-i-know-my-pickleball-grip-size"
    GR_SLK_GUIDE = "https://www.selkirk.com/pages/selkirk-grip-guide"
    GR_ARTI = "https://www.playwitharti.com/blogs/news/pickleball-paddle-grip-size-guide-circumference"
    GR_HEIGHT = [("Below 5 ft 3 in (160 cm)", "4 in (10.2 cm)"), ("5 ft 3 in to 5 ft 8 in (160-173 cm)", "4.25 in (10.8 cm)"), ("Above 5 ft 8 in (173 cm)", "4.5 in (11.4 cm)")]
    GR_ARTI_CHART = [("Under 4 in", "4 1/8 in"), ("4 to 4 1/4 in", "4 1/4 in"), ("4 1/4 to 4 1/2 in", "4 3/8 in")]
    GR_SLK_GRIPS = [("Thin Grip", "4 in", "Small hands; about 0.2 oz lighter than the Comfort Grip"),
                    ("Comfort Grip", "4.25 in", "Selkirk's standard grip, \"preferred by most people\""),
                    ("Contour Grip", "4.25 in", "Same size as Comfort, with ridges; recommended for beginners"),
                    ("Double Grip", "4.5 in", "Very large hands; a Comfort Grip over another Comfort Grip, about 0.4 oz heavier on average")]
    gr_vol = [p for p in PP if p["brand"] == "Volair" and p.get("grip")]
    gr_vol.sort(key=lambda p: (p["grip"], p["model"]))
    gr_faq = [
        ("How do I measure my pickleball grip size?",
         "Hold your playing hand palm up with the fingers extended and together. Measure from the middle of the three palm creases to the tip of your ring finger. Selkirk and ARTI both say that number, in inches, is about your grip circumference."),
        ("What is the most common pickleball grip size?",
         "4 1/4 inches. Selkirk's standard Comfort Grip is 4.25 inches and \"preferred by most people\", and ARTI calls 4 1/4 inches the most widely used size."),
        ("Should I size up or down if I'm between grip sizes?",
         "Go smaller. ARTI says to choose the smaller grip and add overgrip, because overgrip can only make a handle bigger. There is no practical way to shrink a grip that is too large."),
        ("How much does an overgrip add?",
         "ARTI says one layer of standard overgrip adds about 1/16 inch to the circumference. Selkirk's Double Grip, a full Comfort Grip wrapped over another, takes its 4.25-inch grip to 4.5 inches."),
        ("Does the index finger test work for pickleball?",
         "Selkirk calls it a myth for pickleball. It says the tennis rule of thumb, fitting an index finger between your fingertips and palm, tends to push players into a bigger grip than is most comfortable."),
        ("Can I change my grip size and still play in sanctioned events?",
         "Yes. The 2026 USA Pickleball rulebook lists changing grip size with inserts, adding or replacing grip wrap, and replacing OEM interchangeable grips as allowed alterations (Rule 3.D.6). The altered paddle must still meet all specifications."),
        ("Can I use my height to pick a grip size?",
         "Selkirk publishes a height chart: under 5 ft 3 in, a 4-inch grip; 5 ft 3 in to 5 ft 8 in, 4.25 inches; over 5 ft 8 in, 4.5 inches. It says this is less accurate than measuring your hand."),
    ]
    gr_faq_html, gr_faq_ld = faq(gr_faq)
    gr_h_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in GR_HEIGHT)
    gr_a_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in GR_ARTI_CHART)
    gr_s_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in GR_SLK_GRIPS)
    gr_v_rows = "".join(f'<tr><th scope="row">{alink(p, p["model"])}</th><td>{e(p["grip"])}</td><td>{e(p.get("handle") or "not published")}</td><td>{e(p.get("shape") or "")}</td></tr>' for p in gr_vol)
    _gr_own = __import__("own_codes").own_codes(__import__("json").load(open(__import__("pathlib").Path(__file__).with_name("config.json")))).get("Volair")
    gr_code = (f'<p>Our own Volair code <b>{e(_gr_own["code"])}</b> takes {e(_gr_own["discount"])} at checkout on volair.com. '
               f'{e(__import__("own_codes").earn_line(_gr_own))} Details: <a href="../discount-codes/volair.html">Volair promo code</a>.</p>') if _gr_own else ""
    gr_vol_html = (f'''<h2>Grip sizes on Volair paddles</h2>
<p>Most makers list a single stock grip size, so check the spec before you buy. Volair publishes grip circumference and handle length for each paddle. These are the paddles in our database, with the numbers from each paddle's page on volair.com (re-read {gr_checked}):</p>
<div class="tbl"><table><thead><tr><th>Volair paddle</th><th>Grip circumference</th><th>Handle length</th><th>Shape</th></tr></thead><tbody>{gr_v_rows}</tbody></table></div>
<p>By that list, the Forza paddles and the V.1F/ XL-W list 4.15 inches and the CMD paddles 4.125, just under the common 4 1/4. Smaller grips like these can be built up with overgrip. The Pro and Mach 2 paddles list 4.25 inches in 14mm and 4.3 inches in 16mm.</p>
{gr_code}''') if gr_vol else ""
    grip = f'''<h1>Pickleball grip size: how to measure your hand and pick a paddle grip (2026)</h1>
<p class="meta">Sizing methods and charts are from paddle makers <a href="{GR_SLK}" target="_blank" rel="noopener">Selkirk</a> and <a href="{GR_ARTI}" target="_blank" rel="noopener">ARTI</a>. Grip alteration rules are from the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball Official Rulebook</a>. All read {gr_checked}. This is not medical advice. If you have arm pain, see a doctor.</p>
<h2>The short answer</h2>
<ul>
<li><b>Measure:</b> palm up, fingers together. Measure from the middle palm crease to the tip of your ring finger. That number, in inches, is about your grip circumference (Selkirk, ARTI).</li>
<li><b>Most players:</b> 4 1/4 inches is the common starting size.</li>
<li><b>Between sizes:</b> go smaller and add overgrip (ARTI).</li>
<li><b>Legal:</b> grip wrap and grip-size inserts are allowed alterations under the 2026 rulebook (Rule 3.D.6).</li>
</ul>
<h2>Why grip size matters</h2>
<p>Grip size is the <b>circumference</b> of the handle, measured around it in inches. Selkirk says a grip that is too small makes you squeeze the paddle harder than you need to, and one that is too big makes you strain for control. Over time, either one can tire your hand and arm. ARTI adds that an oversized grip limits the wrist movement you use for spin and soft shots at the kitchen.</p>
<h2>How to measure your grip size (the ruler test)</h2>
<ol>
<li>Hold your playing hand palm up, fingers extended and pressed together.</li>
<li>Find the <b>middle</b> of the three palm creases. Selkirk calls it the bottom lateral crease. ARTI calls it the horizontal line across the center of your palm, <i>not</i> the crease just below your fingers.</li>
<li>Measure from that crease to the tip of your <b>ring finger</b> with a ruler marked in inches.</li>
</ol>
<p>Selkirk says the result "will be somewhere between 4 and 5 inches" and should be your grip circumference. ARTI turns it into a size with this chart:</p>
<div class="tbl"><table><thead><tr><th>Your measurement</th><th>ARTI's suggested grip</th></tr></thead><tbody>{gr_a_rows}</tbody></table></div>
<p>ARTI calls its chart "a starting point, not a verdict." Selkirk says the best check is court time with the paddle.</p>
<h2>No ruler? Selkirk's height chart</h2>
<div class="tbl"><table><thead><tr><th>Height</th><th>Grip size</th></tr></thead><tbody>{gr_h_rows}</tbody></table></div>
<p>Selkirk says height is less accurate than measuring your hand.</p>
<h2>Skip the index finger test</h2>
<p>Tennis players are often told to fit their other index finger between the fingertips and palm while holding the handle. Selkirk calls this a myth for pickleball: it tends to push players into a bigger grip than is most comfortable. Coming from tennis, a slightly bigger grip may still feel right to you.</p>
<h2>Grip size names: small, medium, large</h2>
<p>Size names aren't standard, so go by the number. Selkirk's grip options:</p>
<div class="tbl"><table><thead><tr><th>Selkirk grip</th><th>Circumference</th><th>Notes</th></tr></thead><tbody>{gr_s_rows}</tbody></table></div>
<p>ARTI lists 4 1/8 inches as small, 4 1/4 as medium and 4 3/8 as large. It says a 4 1/2-inch grip is uncommon in pickleball.</p>
<h2>Overgrips: the easy way to size up</h2>
<p>ARTI says one layer of standard overgrip adds about 1/16 inch to the circumference. It also absorbs sweat and is cheap to replace. That only works in one direction: you can build a small grip up, but you can't make a big grip smaller. That's why ARTI says to go smaller when you're between sizes. Selkirk adds that grips change size over time as they wear down or swell with moisture, so check yours now and then.</p>
<p>Under the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball rulebook</a>, adding or replacing grip wrap (Rule 3.D.6.h), changing grip size with inserts (3.D.6.g) and replacing OEM interchangeable grips (3.D.6.d) are allowed alterations. The altered paddle still has to meet all specifications. The rulebook also says decals and tape on the paddle face can't extend more than 1 inch above the top of the grip (Rule 3.D.7).</p>
<h2>Handle length is a separate number</h2>
<p>Circumference is how thick the handle is. Handle length is how long it is. Selkirk says handles are usually around 4.5 inches long, and a longer handle helps if you hit two-handed shots. The paddle as a whole is capped by Rule 3.D.2: length plus width can't exceed 24 inches, and length can't exceed 17 inches, so a longer handle means less face. For the rest of the spec sheet, see <a href="paddle-weight-and-core.html">paddle weight and core</a> and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a>.</p>
{gr_vol_html}
<h2>Next steps</h2>
<p>Still choosing a paddle? Try the <a href="../paddle-quiz.html">paddle quiz</a> or the <a href="best-paddles-under-100.html">best paddles under $100</a>. If your paddle feels different than it used to, check <a href="is-my-paddle-dead.html">core crush signs</a>.</p>
{money_links()}
{gr_faq_html}
{sources([("Selkirk: How do I find my pickleball paddle grip size?", GR_SLK, f"ruler test, height chart, sizing effects, handle length, read {gr_checked}"),
          ("Selkirk: Grip guide", GR_SLK_GUIDE, f"Thin, Comfort, Contour and Double Grip sizes and weights, index finger test, read {gr_checked}"),
          ("ARTI Pickleball: Pickleball paddle grip size guide", GR_ARTI, f"measurement chart, size names, overgrip adds about 1/16 inch, read {gr_checked}"),
          ("USA Pickleball: 2026 Official Rulebook", RULES, f"Rules 3.D.2 (dimensions), 3.D.6 (allowable alterations) and 3.D.7, read {gr_checked}"),
          ("Volair product pages (one per paddle, linked from each paddle page)", "https://volair.com/", f"grip circumference and handle length for each paddle listed, re-read {gr_checked}")])}
{more("guides/pickleball-grip-size.html")}'''
    page("guides/pickleball-grip-size.html", "Pickleball Grip Size Chart: How to Measure Your Paddle Grip (2026)", grip,
         "Find your pickleball grip size: the ruler test, Selkirk's height chart, ARTI's sizing chart, overgrip tips, the 2026 rulebook on grip changes, and Volair grip specs.",
         fresh={"checked": GR_CHECKED, "height": GR_HEIGHT, "arti": GR_ARTI_CHART, "selkirk": GR_SLK_GRIPS,
                "volair": [[p["model"], p["grip"], p.get("handle")] for p in gr_vol], "faq": gr_faq},
         schema=[gr_faq_ld])

    # ----- Pickleball drills (Nov 5, 2026) -----
    # Evergreen. Every drill below is described from the linked source page, read on DR_CHECKED: USA Pickleball's
    # "Top Four Pickleball Drills Anyone Can Do" and third-shot article, PlayPickleball's 2-person drills (Barrett and Danea Bass),
    # and pickleball.com's wall-drill piece with pro Ava Ignatowich. Wall tape heights come from the 2026 rulebook (our court guide).
    # No invented rep targets: counts appear only where the source gives them.
    DR_CHECKED = "2026-11-05"
    dr_checked = _dt.date.fromisoformat(DR_CHECKED).strftime("%B %-d, %Y")
    DR_USAP = "https://usapickleball.org/pickleball-skills/level-one/top-four-pickleball-drills/"
    DR_USAP3 = "https://usapickleball.org/pickleball-skills/level-three/mastering-the-third-shot-in-pickleball/"
    DR_PP = "https://playpickleball.com/pickleball-drills-2-people/"
    DR_WALL = "https://pickleball.com/learn/the-best-pickleball-wall-drills-with-ava-ignatowich"
    DR_TABLE = [
        ("Down the Link Dink Game", "2", "Dink control, patience, when to attack", "USA Pickleball"),
        ("Two Tap Drill", "2", "Soft hands, volley control", "USA Pickleball"),
        ("Cross Court Drops", "2", "Third shot drop from the baseline", "USA Pickleball"),
        ("Serving From a Basket", "1", "Serve consistency and depth", "USA Pickleball"),
        ("Dink Dink Bang", "2", "Dinks, speed-ups, resets", "PlayPickleball"),
        ("Fast Hands", "2", "Hand speed at the net", "PlayPickleball"),
        ("Slinky", "2", "Shots from every part of the transition zone", "PlayPickleball"),
        ("Work-Up", "2", "Getting from the baseline to the kitchen", "PlayPickleball"),
        ("Skinny Singles", "2", "Game play on half the court", "PlayPickleball"),
        ("Wall dinks, fast hands and drives", "1", "Feel, reflexes, cardio", "Ava Ignatowich via pickleball.com"),
    ]
    dr_faq = [
        ("What are the best pickleball drills for beginners?",
         "USA Pickleball's four drills \"anyone can do\" are the Down the Link Dink Game, the Two Tap Drill, Cross Court Drops and Serving From a Basket. Together they cover dinking, soft hands, the third shot drop and the serve."),
        ("How do you do the Two Tap Drill?",
         "Stand at the kitchen line across from a partner and volley back and forth. Each time the ball comes to you, tap it up to yourself once, then hit it back. USA Pickleball says it builds soft hands, ball control, reaction time and volley consistency."),
        ("How many drop shots should I hit in a row?",
         "In USA Pickleball's Cross Court Drops drill, the goal is 10 to 20 successful drops in a row from behind the baseline before you switch sides with your partner. Don't move forward after the drop during the drill."),
        ("Can I practice pickleball alone?",
         "Yes. USA Pickleball's Serving From a Basket drill needs only you and a basket of balls. A wall works too: pro Ava Ignatowich told pickleball.com she gets far more reps at a wall and spends most of that time on fast hands, alternating forehands and backhands."),
        ("What is the Skinny Singles drill?",
         "It's singles played on half of each side of the court, scored like a regular game to 11. PlayPickleball calls it the drill that's most like a real game when you only have two people."),
        ("How high should the net line be for wall practice?",
         "The 2026 USA Pickleball rulebook sets the net at 36 inches at the sidelines and 34 inches at the center, so a strip of tape at 34 to 36 inches is a fair stand-in. See our court dimensions guide for the full layout."),
    ]
    dr_faq_html, dr_faq_ld = faq(dr_faq)
    dr_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td><td>{e(d)}</td></tr>' for a, b, c, d in DR_TABLE)
    drills = f'''<h1>Pickleball drills: 10 drills for beginners, partners and solo practice (2026)</h1>
<p class="meta">Each drill is described from its source: <a href="{DR_USAP}" target="_blank" rel="noopener">USA Pickleball</a>, <a href="{DR_PP}" target="_blank" rel="noopener">PlayPickleball</a> (Barrett and Danea Bass) and <a href="{DR_WALL}" target="_blank" rel="noopener">pickleball.com</a> (pro Ava Ignatowich). All read {dr_checked}. Rep targets appear only where the source gives one.</p>
<h2>The short answer</h2>
<ul>
<li><b>New to drilling:</b> start with USA Pickleball's four basics: a dink game, the Two Tap Drill, cross-court drops and serving from a basket.</li>
<li><b>Two players, more pace:</b> add Dink Dink Bang, Fast Hands, Slinky, Work-Up and Skinny Singles.</li>
<li><b>No partner:</b> serve from a basket, or hit against a wall.</li>
</ul>
<p>USA Pickleball says drilling is "the fastest and most effective way to improve," and that even a few minutes of drills before games can make a noticeable difference.</p>
<h2>All 10 drills at a glance</h2>
<div class="tbl"><table><thead><tr><th>Drill</th><th>Players</th><th>What it works on</th><th>Source</th></tr></thead><tbody>{dr_rows}</tbody></table></div>
<h2>USA Pickleball's four drills anyone can do</h2>
<h3>1. Down the Link Dink Game</h3>
<p>Stand at the kitchen line directly across from your partner and play on half the court only. One player feeds a dink, and the return must also be a dink. After that, anything goes: speed-ups, lobs, volleys or more dinks, as long as the ball stays on your half. USA Pickleball suggests playing best two out of three games to 5 points, then switching sides. It builds dink control and teaches when to attack. New to the shot? Read <a href="how-to-dink.html">how to dink</a> first.</p>
<h3>2. Two Tap Drill</h3>
<p>From the kitchen line, volley back and forth with your partner. When the ball comes to you, tap it up to yourself once before you send it back. The goal is a steady rally at a pace you control. USA Pickleball lists soft hands, ball control, reaction time and volley consistency as what it improves.</p>
<h3>3. Cross Court Drops</h3>
<p>Your partner stands at the kitchen line. You stand behind the baseline, cross-court. Hit drop shots to your partner, who returns the ball deep to your baseline. The key rule: don't move forward after your shot. Stay back and keep hitting drops. Aim for 10 to 20 good drops in a row, then switch. In a game, the drop is the soft third shot that buys you time to move up. USA Pickleball's <a href="{DR_USAP3}" target="_blank" rel="noopener">third shot guide</a> suggests going cross-court because that path crosses the lowest part of the net. Full technique, drop vs drive and more drills: <a href="third-shot-drop.html">third shot drop guide</a>.</p>
<h3>4. Serving From a Basket</h3>
<p>Take a basket of balls and serve from one side until it's empty, focusing on consistency and placement. Collect the balls and repeat from the other side. This is the one you can do alone. Need a refresher on where a legal serve has to land? See the <a href="pickleball-rules-for-beginners.html">rules for beginners</a>.</p>
<h2>Five 2-person drills from PlayPickleball</h2>
<h3>5. Dink Dink Bang</h3>
<p>Both players at the kitchen line. Hit three dinks, then the fourth shot is a speed-up and the fifth is a reset, then go back to dinking. The pattern is "dink, dink, dink, bang, reset," and PlayPickleball says it covers almost every kitchen-line shot.</p>
<h3>6. Fast Hands</h3>
<p>Volley back and forth from the kitchen line, aiming at each other's hips. Both players then step one step into the kitchen and keep volleying, adding a step at a time until someone faults. It's a drill, not a game: in a real point, you can't volley while you're touching the kitchen. PlayPickleball says the ball seems much slower once you're back at the line.</p>
<h3>7. Slinky</h3>
<p>Your partner stays put at the kitchen line. You hit three dinks, step back, hit three more shots, and keep stepping back three shots at a time until you reach the baseline. Then work your way forward the same way. The point is to hit from every part of the transition zone.</p>
<h3>8. Work-Up</h3>
<p>One player at the kitchen line feeds to the other at the baseline. The baseline player tries to work up to the kitchen while the net player tries to keep them back, then they play out the point. Start over after each fault. PlayPickleball says it works your drives, drops and speed-ups.</p>
<h3>9. Skinny Singles</h3>
<p>Play singles using only half of each side of the court, scored like a regular game to 11. PlayPickleball calls it the drill that's most like a real game when there are just two of you.</p>
<h2>10. Solo: wall drills from a pro</h2>
<p>Pro Ava Ignatowich told pickleball.com that at a wall she gets far more reps than in practice play, where she feels she hits "only about 25% of the shots." Her routine, as pickleball.com describes it:</p>
<ul>
<li><b>Dinks first.</b> Hit low, soft shots to warm up, watching the ball hit the sweet spot. You can't see where the balls would land, so this is about feel.</li>
<li><b>Speed-ups and resets.</b> In the middle of a dink rally, speed up into the wall, then block the return so it comes back soft.</li>
<li><b>Fast hands.</b> Most of her wall time goes here: alternate forehand and backhand. Step closer to make it faster, or back to make it easier.</li>
<li><b>Drives for cardio.</b> Get low and hit through the ball, aiming slightly left or right so you have to move sideways.</li>
</ul>
<p>For a net line, put tape on the wall between 34 and 36 inches high. The 2026 rulebook sets the net at 36 inches at the sidelines and 34 at the center (see <a href="pickleball-court-dimensions.html">pickleball court dimensions</a>).</p>
<h2>Gear for practice</h2>
<p>A handful of balls is all most drills need, but match them to your court: <a href="indoor-vs-outdoor-pickleball-balls.html">indoor vs outdoor balls</a>. Court shoes matter more when you're moving side to side for an hour: see <a href="how-to-choose-pickleball-shoes.html">how to choose pickleball shoes</a>. If your hand tires fast, check your <a href="pickleball-grip-size.html">grip size</a>.</p>
{money_links()}
{dr_faq_html}
{sources([("USA Pickleball: Top Four Pickleball Drills Anyone Can Do", DR_USAP, f"Down the Link Dink Game, Two Tap Drill, Cross Court Drops, Serving From a Basket, read {dr_checked}"),
          ("USA Pickleball: Mastering the Third Shot in Pickleball", DR_USAP3, f"drop vs drive, cross-court drops over the lowest part of the net, read {dr_checked}"),
          ("PlayPickleball: 5 simple pickleball drills for 2 people (Barrett and Danea Bass)", DR_PP, f"Dink Dink Bang, Fast Hands, Slinky, Work-Up, Skinny Singles, read {dr_checked}"),
          ("pickleball.com: The best pickleball wall drills with Ava Ignatowich", DR_WALL, f"wall dinks, speed-ups and resets, fast hands, drives, read {dr_checked}"),
          ("USA Pickleball: 2026 Official Rulebook", RULES, f"net height and the non-volley zone (kitchen) volley rule, read {dr_checked}")])}
{more("guides/pickleball-drills.html")}'''
    page("guides/pickleball-drills.html", "Pickleball Drills: 10 Drills for Beginners, Partners and Solo (2026)", drills,
         "10 pickleball drills from USA Pickleball, PlayPickleball and pro Ava Ignatowich: dinking, Two Tap, cross-court drops, serving, Skinny Singles and solo wall drills.",
         fresh={"checked": DR_CHECKED, "table": DR_TABLE, "faq": dr_faq},
         schema=[dr_faq_ld])

    # ----- Pickleball kitchen / NVZ rules (Nov 6, 2026) -----
    # Evergreen deep-dive for the approved P3 target. Every rule number and paraphrase below was read from the
    # 2026 USA Pickleball Official Rulebook PDF, the Basic Rules Summary PDF, and USA Pickleball's rules-summary
    # and how-to-play pages on KV_CHECKED. Court size cross-checks our court-dimensions guide (Rule 3.A.4.c).
    KV_CHECKED = "2026-11-06"
    kv_checked = _dt.date.fromisoformat(KV_CHECKED).strftime("%B %-d, %Y")
    KV_SUM_PAGE = "https://usapickleball.org/rules/summary/"
    KV_HOW = "https://usapickleball.org/pickleball-skills/level-one/how-to-play-pickleball/"
    KV_FAULTS = [
        ("Contact while volleying", "11.A.1", "You, your paddle, clothing, or anything else touching you (including your partner) touches the NVZ during the volley"),
        ("Momentum after a volley", "11.A.2", "The volley's momentum carries you into contact with the NVZ, or into something already touching it, even after the ball is dead"),
        ("Volley before exiting", "11.A.3", "After you touched the NVZ, you volley again before both feet are completely outside it on the playing surface"),
        ("Serve into the kitchen", "7.E.2 / 8.C", "A serve that lands in the NVZ, or on the NVZ line, is short and a fault"),
    ]
    kv_faq = [
        ("What are the pickleball kitchen rules?",
         "The kitchen is the non-volley zone: 7 feet deep by 20 feet wide on each side of the net (Rule 3.A.4.c). You may stand in it. You may not volley while you, or anything in contact with you, are touching it. Momentum from a volley that carries you into the zone is also a fault (Section 11)."),
        ("Can you stand in the kitchen in pickleball?",
         "Yes. USA Pickleball's rules summary says a player may legally be in the non-volley zone any time other than when volleying a ball. After a bounce, you can step in to play the ball. Standing there while not volleying is legal; volleying while touching it is not."),
        ("Is the kitchen line part of the kitchen?",
         "Yes. Rule 3.A.4.c says all lines that bound the non-volley zone are part of the zone. A toe on the kitchen line counts as being in the kitchen for a volley."),
        ("Is a paddle touch in the kitchen a fault?",
         "Yes, if it happens during the act of volleying. Rule 11.A.1 faults a volleying player when anything that has contact with that player — paddle, clothing, hat, or partner — contacts the non-volley zone."),
        ("Does momentum into the kitchen count after the ball is dead?",
         "Yes. Rule 11.A.2 says a volleying player's momentum that causes contact with the non-volley zone is a fault even after the ball becomes dead. Rule 9.B.1 calls out this momentum exception to the usual live-ball-only fault rule."),
        ("Is a serve that lands on the kitchen line in or out?",
         "Out. The rules summary and Rule 8.C say a serve that contacts the non-volley zone line is short and a fault. Other balls that touch a line are in."),
        ("Do I have to leave the kitchen before I can volley again?",
         "Yes. Rule 11.A.3: after contacting the non-volley zone, you may not volley until both feet have contacted the playing surface completely outside the zone."),
    ]
    kv_faq_html, kv_faq_ld = faq(kv_faq)
    kv_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in KV_FAULTS)
    kitchen = f'''<h1>Pickleball kitchen rules: NVZ faults, paddle touch and momentum (2026)</h1>
<p class="meta">Paraphrased from the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball Official Rulebook</a>, the <a href="{RULES_SUM}" target="_blank" rel="noopener">Basic Rules Summary</a>, and USA Pickleball's <a href="{KV_SUM_PAGE}" target="_blank" rel="noopener">rules summary</a> and <a href="{KV_HOW}" target="_blank" rel="noopener">how to play</a> pages, all read {kv_checked}. The rulebook wins if we ever disagree.</p>
<h2>The short answer</h2>
<ul>
<li><b>What it is:</b> the non-volley zone (NVZ), nicknamed the kitchen — 7 feet deep by 20 feet wide on each side of the net (Rule 3.A.4.c).</li>
<li><b>The real rule:</b> you may stand in it. You may not volley while touching it, including its lines.</li>
<li><b>Connected contact counts:</b> paddle, clothing, hat, or partner contact during a volley is the same fault (Rule 11.A.1).</li>
<li><b>Momentum counts:</b> if a volley carries you into the kitchen, it is a fault even after the ball is dead (Rule 11.A.2).</li>
<li><b>Serve short:</b> a serve that lands in the kitchen or on the kitchen line is a fault (Rules 7.E.2 and 8.C).</li>
</ul>
<h2>What the kitchen is</h2>
<p>Rule 3.A.4.c defines each non-volley zone as the 7-foot by 20-foot (2.13 m by 6.08 m) area next to the net. The NVZ lines run parallel to the net, 7 feet out, between the sidelines. <b>All lines that bound the zone are part of the zone</b>, so a foot or paddle on the kitchen line is contact with the kitchen. The rulebook also says the zone is two-dimensional: it does not extend above the playing surface. Full court layout: <a href="pickleball-court-dimensions.html">pickleball court dimensions</a>.</p>
<p>USA Pickleball's how-to-play page calls the NVZ the 14-foot area around the net (7 feet on each side) and notes the nickname "Kitchen." Beginner overview: <a href="pickleball-rules-for-beginners.html">pickleball rules for beginners</a>.</p>
<h2>When standing in the kitchen is legal</h2>
<p>The Basic Rules Summary is blunt: a player may legally be in the non-volley zone any time other than when volleying a ball. After the ball has bounced on your side, you can step in (or stay in) to hit it. That is how dinks and erases work at the net — see <a href="how-to-dink.html">how to dink</a>. Standing idle in the kitchen is legal; it is just usually bad position because you cannot take the next ball out of the air until you re-establish outside.</p>
<h2>The three NVZ faults in Section 11</h2>
<p>Section 11 opens with Rule 11.A: all volleys must be initiated outside the non-volley zone. A player, or anything in contact with the player, may contact the zone at any time <b>except during the act of volleying</b>.</p>
<div class="tbl"><table><thead><tr><th>Fault</th><th>Rule</th><th>What triggers it</th></tr></thead><tbody>{kv_rows}</tbody></table></div>
<h3>Paddle touch and anything connected to you</h3>
<p>Rule 11.A.1 faults a volleying player when that player, or anything that has contact with the volleying player — including the player's partner — contacts the non-volley zone. The Basic Rules Summary says the same in plain language: it is a fault if, when volleying, the player steps on the NVZ, including the line, or when the player's momentum causes them or anything they are wearing or carrying to touch the zone. So a paddle tip, a hat brim, a sleeve, or leaning on a partner who is in the kitchen can all finish the fault.</p>
<h3>Momentum after the volley</h3>
<p>The rulebook defines momentum as the property that keeps a player moving after contacting the ball. The act of volleying produces momentum that ends when the player regains balance and control, or stops moving toward the non-volley zone. Rule 11.A.2: when a volleying player's momentum causes the player to contact anything (including the player's partner) that is in contact with the NVZ, <b>even after the ball becomes dead</b>, it is a fault. Rule 9.B.1 makes the same point: faults normally require a live ball, except for non-volley zone violations involving momentum.</p>
<p>Practical read: if you volley a winner and then stumble onto the kitchen line, you still lose the rally. Stopping yourself by grabbing a partner who is standing in the kitchen is the same problem.</p>
<h3>Re-establishing both feet outside before the next volley</h3>
<p>Rule 11.A.3: after contacting the non-volley zone, when a player volleys a ball before both feet contact the playing surface completely outside the zone, it is a fault. You cannot hop from inside the kitchen and volley in the air without first planting both feet outside. Once both feet are clear, you may volley again from outside the line.</p>
<h2>Serve: kitchen and kitchen line are short</h2>
<p>Rule 7.E says the served ball must clear the opponent's non-volley zone and land in the correct service court. Rule 7.E.2: a served ball that lands in the non-volley zone is a fault against the server. Rule 8.C and the rules summary add the line call: a serve that contacts the non-volley zone line is "out" — short and a fault. Other balls that touch a line are in. One-page reminder: <a href="pickleball-rules-cheat-sheet-2026.html">pickleball rules cheat sheet 2026</a>.</p>
<h2>Common kitchen arguments, settled</h2>
<ul>
<li><b>"My paddle only brushed the line after I hit."</b> If it was part of the act of volleying or the momentum from that volley, Rules 11.A.1 and 11.A.2 still apply.</li>
<li><b>"The ball was already dead."</b> Momentum into the kitchen is the exception; the fault still counts (Rules 11.A.2 and 9.B.1).</li>
<li><b>"I was just standing there."</b> Standing is fine. Volleying while touching the zone is not. Hitting a ball that has bounced first is fine.</li>
<li><b>"The kitchen line is in for a serve."</b> No. For a serve, the kitchen line is short. For other shots, a ball on the kitchen line is in — but your foot on that line during a volley is still NVZ contact.</li>
</ul>
<h2>Practice the line without the fault</h2>
<p>Soft hands at the kitchen are a skill, not a loophole. Use the dink and Two Tap work in our <a href="pickleball-drills.html">pickleball drills</a> guide, and keep your toes behind the line until the bounce. When you do step in after a bounce, remember Rule 11.A.3 before the next volley: both feet outside first.</p>
{money_links()}
{kv_faq_html}
{sources([("USA Pickleball: 2026 Official Rulebook", RULES, f"Rules 3.A.4.c, 7.E.2, 8.C, 9.B.1, Section 11 (11.A–11.A.3), Momentum and Non-Volley Zone definitions, read {kv_checked}"),
          ("USA Pickleball: Basic Rules Summary (PDF)", RULES_SUM, f"Non-Volley Zone and Line Calls summary, Rev. 1/1/2026, read {kv_checked}"),
          ("USA Pickleball: Essential Pickleball Rules Summary", KV_SUM_PAGE, f"NVZ, kitchen nickname, momentum and line-call bullets, read {kv_checked}"),
          ("USA Pickleball: How to Play Pickleball", KV_HOW, f"Kitchen rule overview, standing vs volleying, serve must clear the kitchen, read {kv_checked}")])}
{more("guides/pickleball-kitchen-rules.html")}'''
    page("guides/pickleball-kitchen-rules.html", "Pickleball Kitchen Rules: NVZ Faults, Paddle Touch and Momentum (2026)", kitchen,
         "Pickleball kitchen rules from the 2026 USA Pickleball rulebook: NVZ size, paddle-touch and momentum faults, standing after a bounce, kitchen line on the serve, and FAQ.",
         fresh={"checked": KV_CHECKED, "faults": KV_FAULTS, "faq": kv_faq},
         schema=[kv_faq_ld])

    # ----- Third shot drop (Nov 9, 2026) -----
    # Evergreen technique page for the approved P3 target. Every tip below paraphrases the linked USA Pickleball
    # and Pickleball.com pages read on TS_CHECKED. No invented stats, heights or percentages beyond what they say.
    TS_CHECKED = "2026-11-09"
    ts_checked = _dt.date.fromisoformat(TS_CHECKED).strftime("%B %-d, %Y")
    TS_USAP_DD = "https://usapickleball.org/pickleball-skills/level-three/mastering-the-third-shot-in-pickleball/"
    TS_USAP_BASICS = "https://usapickleball.org/pickleball-skills/level-three/basics-of-the-third-shot-drop/"
    TS_USAP_L3 = "https://usapickleball.org/skill-level/level-three/"
    TS_PBCOM = "https://pickleball.com/learn/drop-or-drive-mastering-the-third-shot-decision"
    TS_CHOICE = [
        ("Low return that is hard to attack", "Drop", "USA Pickleball"),
        ("Deep return that pushes you back", "Drop", "USA Pickleball, Pickleball.com"),
        ("Short return that bounces high", "Drive", "USA Pickleball, Pickleball.com"),
        ("You are balanced and stepping in", "Drive", "Pickleball.com"),
        ("Off balance and need a simpler ball", "Drive (then drop on the fifth)", "USA Pickleball"),
    ]
    ts_faq = [
        ("What is a third shot drop in pickleball?",
         "It is a soft, controlled shot hit by the serving team on the third shot of the rally, after the serve and return, that lands in the opponent's kitchen. USA Pickleball describes it as like a longer dink hit from the baseline. Because it lands low in the kitchen, the net team has to let it bounce or hit up, which gives the serving team time to move forward."),
        ("Why is it called the third shot?",
         "The serve is shot one and the return is shot two. Under the two-bounce rule the serving team must let the return bounce, so they usually start the third shot from the baseline while the receivers are already at the kitchen line. The third shot is the serving team's first chance to get to the net."),
        ("Should I drop or drive the third shot?",
         "USA Pickleball's level-three tip is simple: drop low balls, drive high balls, and follow your shot in. Drop when the return is low or deep and pushes you back. Drive when the return is short with a high bounce and you are balanced. A drive can also set up an easier drop on the fifth shot."),
        ("How hard should I grip the paddle for a third shot drop?",
         "Loosely. USA Pickleball suggests about a three on a one-to-ten grip pressure scale. A tighter grip sends the ball farther."),
        ("Where should I aim a third shot drop?",
         "Into the opponent's kitchen. USA Pickleball suggests crosscourt because that path crosses the lowest part of the net, and also lists the opponent's backhand, the middle of the court, and the returner as smart targets. Pickleball.com suggests a soft arc that clears the net by no more than about a foot."),
        ("Should I run to the net after a third shot drop?",
         "Only after a good one. Both USA Pickleball and Pickleball.com say to move up once you know the drop is quality. If it is high or short, hold back, defend, and try to get in on the fifth shot."),
    ]
    ts_faq_html, ts_faq_ld = faq(ts_faq)
    ts_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in TS_CHOICE)
    tsd = f'''<h1>Third shot drop: how to hit it, when to drop vs drive, and drills</h1>
<p class="meta">Built from USA Pickleball's <a href="{TS_USAP_BASICS}" target="_blank" rel="noopener">third shot drop basics</a> and <a href="{TS_USAP_DD}" target="_blank" rel="noopener">drop vs drive</a> lessons, its <a href="{TS_USAP_L3}" target="_blank" rel="noopener">level three skills page</a>, and <a href="{TS_PBCOM}" target="_blank" rel="noopener">Pickleball.com's third-shot decision guide</a>, all read {ts_checked}. No coaching stats are made up here.</p>
<h2>The short answer</h2>
<ul>
<li><b>What it is:</b> a soft shot the serving team hits on shot three that lands in the opponent's kitchen, like a long dink from the baseline.</li>
<li><b>Why it matters:</b> the two-bounce rule keeps the serving team back while the receivers reach the kitchen line. A good drop lets you move up without eating a hard volley.</li>
<li><b>How to hit it:</b> semi-open stance, paddle in front of you, grip pressure around 3 out of 10, gentle low-to-high lift with your legs, short follow-through.</li>
<li><b>Where:</b> into the kitchen, often crosscourt over the lowest part of the net.</li>
<li><b>Drop or drive:</b> drop low or deep returns; drive short, high ones when you are balanced.</li>
</ul>
<h2>Why the third shot is the hard one</h2>
<p>A rally starts with the serve and the return, and both must bounce (<a href="pickleball-rules-for-beginners.html">two-bounce rule</a>). That means the returning team can walk up to the <a href="pickleball-kitchen-rules.html">kitchen line</a> while the serving team waits at the baseline. USA Pickleball calls the third shot one of the most important and toughest shots in the game because it is the serving team's bridge from the baseline to the kitchen, where most points are won. Court layout and kitchen depth: <a href="pickleball-court-dimensions.html">pickleball court dimensions</a>.</p>
<h2>How to hit a third shot drop</h2>
<ol>
<li><b>Stay back and get set.</b> Wait behind the baseline for the return, then take small steps so you hit the ball out in front of you (USA Pickleball).</li>
<li><b>Semi-open stance.</b> Halfway between facing the net and facing the sideline. USA Pickleball says it keeps the stroke compact and stops an oversized backswing.</li>
<li><b>Paddle in front.</b> USA Pickleball's picture: a brick wall right behind your legs, and the paddle never swings past it.</li>
<li><b>Soft grip.</b> About a 3 on a 1 to 10 pressure scale. Squeeze harder and the ball flies farther.</li>
<li><b>Lift, don't slap.</b> Pickleball.com: a gentle low-to-high motion, paddle face slightly open, legs doing the work instead of the wrist.</li>
<li><b>Soft arc.</b> Pickleball.com suggests the ball clear the net by no more than about a foot and land in the kitchen so opponents have to hit up.</li>
<li><b>Earn the walk forward.</b> Move up only after a quality drop. If it floats high or lands short, hold your ground and look for the fifth shot.</li>
</ol>
<p>Same soft hands as a dink, just from farther back. If dinks still feel stiff, start with <a href="how-to-dink.html">how to dink</a>. For why a high, soft arc lands short and slows down, watch our Big Dill Science short on <a href="../science.html">the physics of the third shot drop</a>.</p>
<h2>Drop or drive: a quick read</h2>
<p>USA Pickleball's level-three rule of thumb is "drop low balls, drive high balls, and follow your shot in." The table puts the sources' cues side by side.</p>
<div class="tbl"><table><thead><tr><th>What the return gives you</th><th>Usual choice</th><th>Source</th></tr></thead><tbody>{ts_rows}</tbody></table></div>
<p>A drive does not need to win the point. Pickleball.com says a heavy drive can force pop-ups and set up the fifth shot, and suggests aiming at the hip area rather than the shoulders.</p>
<h2>Where to aim</h2>
<ul>
<li><b>Crosscourt:</b> USA Pickleball notes the crosscourt path takes the ball over the lowest part of the net and gives you more room.</li>
<li><b>The backhand:</b> usually the weaker side.</li>
<li><b>The middle:</b> more margin for error, and it can cause confusion between partners.</li>
<li><b>The returner:</b> often still moving forward after the return.</li>
</ul>
<h2>Common third shot drop mistakes</h2>
<ul>
<li><b>Too much backswing.</b> The brick-wall cue fixes it.</li>
<li><b>Death grip.</b> Tension adds distance; relax toward a 3 out of 10.</li>
<li><b>Wristy flick.</b> Lift with the legs instead.</li>
<li><b>Running in behind a bad drop.</b> A high drop plus a rushing serving team is how points get lost. Stay back and reset.</li>
<li><b>Only one shot.</b> USA Pickleball says to practice both the drop and the drive and learn when to use each.</li>
</ul>
<h2>Third shot drop drills</h2>
<p>USA Pickleball's "Cross Court Drops" drill is in our <a href="pickleball-drills.html">pickleball drills</a> guide: your partner stands at the kitchen line, you hit drops crosscourt from the baseline, they feed it back deep, and you stay back until you string 10 to 20 good drops together. Two easy add-ons, both following the sources' tips:</p>
<ul>
<li><b>Drop and step.</b> Hit a drop, take a few steps forward only if it landed in the kitchen, then split-step and reset back to the baseline.</li>
<li><b>Call it.</b> Your partner feeds a random mix of low, deep and short, high balls. Call "drop" or "drive" before you hit, then hit that shot.</li>
</ul>
<p>USA Pickleball's level-three page suggests tracking one focus number each game, for example the share of your drops that were quality ones. A paddle with a softer, more controlled feel can help this shot; see <a href="paddle-weight-and-core.html">paddle weight and core</a> and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a>.</p>
{money_links()}
{ts_faq_html}
{sources([("USA Pickleball: Basics of the Third Shot Drop", TS_USAP_BASICS, f"definition, semi-open stance, paddle in front, grip pressure about 3 of 10, read {ts_checked}"),
          ("USA Pickleball: Mastering the Third Shot, Drop vs. Drive", TS_USAP_DD, f"when to drop vs drive, keys to the third shot, placement and crosscourt tip, read {ts_checked}"),
          ("USA Pickleball: Skill Level Three", TS_USAP_L3, f"third-shot rule of thumb and one-focus-metric tip, read {ts_checked}"),
          ("Pickleball.com: Drop or drive? Mastering the third shot decision", TS_PBCOM, f"low-to-high lift, net clearance, drive cues and targets, read {ts_checked}")])}
{more("guides/third-shot-drop.html")}'''
    page("guides/third-shot-drop.html", "Third Shot Drop in Pickleball: How to Hit It, Drop vs Drive and Drills", tsd,
         "How to hit a pickleball third shot drop: stance, grip pressure, low-to-high lift, where to aim, when to drop vs drive, common mistakes and drills, from USA Pickleball tips.",
         fresh={"checked": TS_CHECKED, "choice": TS_CHOICE, "faq": ts_faq},
         schema=[ts_faq_ld])

    # ----- Pickleball stacking (Nov 10, 2026) -----
    # Evergreen doubles-tactics page for the approved P3 target. Rule numbers are from the 2026 USA Pickleball
    # Official Rulebook PDF (Section 5, 6.D.2, 7.A, 7.E.4, 14.A, 18.C), read on SK_CHECKED. Tactics paraphrase the
    # linked Pickleheads, The Kitchen and USA Pickleball pages read the same day. No invented stats or rule numbers.
    SK_CHECKED = "2026-11-10"
    sk_checked = _dt.date.fromisoformat(SK_CHECKED).strftime("%B %-d, %Y")
    SK_USAP_SKILL = "https://usapickleball.org/skill-level/"
    SK_USAP_STRAT = "https://usapickleball.org/pickleball-skills/level-three/how-to-develop-a-strategy-to-identify-a-players-strengths-or-weaknesses/"
    SK_PH = "https://www.pickleheads.com/guides/what-is-stacking-in-pickleball"
    SK_KITCHEN = "https://thekitchenpickle.com/blogs/tips/stacking-in-pickleball-basics-how-to-stack/"
    SK_RULES = [
        ("5.B.1", "The correct server must serve from the correct serving area, and the correct receiver must receive the serve."),
        ("5.B.2", "After each side out, the first server is the player correctly positioned on the right side for the team's score."),
        ("5.B.3", "The starting server's correct position is the right side when the team's score is zero or even, the left when it is odd. The partner is on the opposite side."),
        ("5.B.4", "Except while serving and receiving, there is no restriction on where players stand, on or off the court, as long as they are on their own end of the net."),
        ("5.C", "Before the serve, you may ask your opponent who the correct server or receiver is, or whether players are in the correct positions. They must answer."),
        ("5.C.1.c", "If positions are correct and the wrong player returns the serve, it is a fault against that player, even if the rally is finished. It must be called before the next serve."),
        ("7.E.4", "A serve that hits the server or the server's partner is a fault against the server."),
    ]
    sk_faq = [
        ("What is stacking in pickleball?",
         "Stacking is a doubles tactic where both partners line up on the same side of the court before the serve or the return, then move to their preferred sides once the ball is in play. The serving and receiving rules still decide who serves, who receives and from which side. Stacking only changes where the other partner waits and where each player ends up."),
        ("Is stacking legal in pickleball?",
         "Yes. In the 2026 USA Pickleball rulebook, the correct server must serve from the correct serving area and the correct receiver must receive the serve (rule 5.B.1). Except while serving and receiving, rule 5.B.4 puts no restriction on where players stand, on or off the court, as long as they stay on their own end of the net."),
        ("What is the difference between a half stack and a full stack?",
         "Pickleheads calls stacking only when your team is serving a half stack, because it is easier than stacking on the return. Stacking on both your serve and your return is what players usually call a full stack. The return stack takes more movement and usually a hand signal."),
        ("Why do righty and lefty teams stack?",
         "When a right-handed and a left-handed player line up the traditional way, one arrangement puts both backhands in the middle. Stacking lets the team switch sides only on the points where the score puts them in that alignment, so both forehands cover the middle, as The Kitchen and Pickleheads both explain."),
        ("What are the hand signals for stacking?",
         "Pickleheads describes the common system: the partner at the kitchen line signals behind their back so the other team cannot see. An open hand means switch, a closed fist means stay, and some teams add a signal for a fake switch."),
        ("What happens if we end up in the wrong position while stacking?",
         "Under the 2026 USA Pickleball rulebook, if the correct server or receiver is out of position when the score is called and someone stops the rally to point it out correctly, the rally is replayed (5.C.1.a). If the rally is completed first, the result stands (5.C.2). If positions are correct but the wrong player returns the serve, that is a fault (5.C.1.c). Stopping play with an incorrect claim is a fault against the player who stopped it (5.C.1.b)."),
    ]
    sk_faq_html, sk_faq_ld = faq(sk_faq)
    sk_rows = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td></tr>' for a, b in SK_RULES)
    stk = f'''<h1>How to stack in pickleball: serve and return stacking explained</h1>
<p class="meta">Rules from the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball Official Rulebook</a> (PDF). Tactics from <a href="{SK_PH}" target="_blank" rel="noopener">Pickleheads</a>, <a href="{SK_KITCHEN}" target="_blank" rel="noopener">The Kitchen</a> and USA Pickleball's <a href="{SK_USAP_SKILL}" target="_blank" rel="noopener">skill levels</a>, all read {sk_checked}. The rulebook wins if we ever disagree. No coaching stats are made up here.</p>
<h2>The short answer</h2>
<ul>
<li><b>What it is:</b> both partners line up on the same side before the serve or return, then slide to their preferred sides once the ball is in play.</li>
<li><b>Why:</b> keep both forehands in the middle (especially righty/lefty teams), or keep the stronger player on the side they play best.</li>
<li><b>Is it legal:</b> yes. The correct server serves from the correct side and the correct receiver receives. The other two players can stand anywhere on their own end, on or off the court (rule 5.B.4).</li>
<li><b>Half stack:</b> stack only when your team serves. <b>Full stack:</b> stack on the return too, usually with a hand signal.</li>
<li><b>What it never changes:</b> who serves, who receives, or the score.</li>
</ul>
<h2>What stacking is</h2>
<p>In traditional doubles, partners split the court: each player starts on one side of the centerline and stays roughly there. The score decides those starting sides. The Kitchen puts the key idea simply: the rules decide where you start, not where you play. Stacking means the partner who is not serving or receiving waits on the same side as the server or receiver, often near or beyond the sideline. After the serve or return, the team slides so each player ends up on the side they want.</p>
<p>New to how the score sets your side? In doubles, the starting server is on the right when the team's score is zero or even and on the left when it is odd, and the partner is on the other side (rule 5.B.3). Pickleheads calls these each player's "even side" and "odd side." Serving and scoring basics: <a href="pickleball-rules-for-beginners.html">pickleball rules for beginners</a>.</p>
<h2>Why teams stack</h2>
<ul>
<li><b>Forehands in the middle.</b> The middle is a favorite target because it can cause confusion and force a backhand. For a right-handed and a left-handed partner, one traditional alignment puts both backhands in the middle. Stacking fixes it on those points (The Kitchen, Pickleheads).</li>
<li><b>A stronger player on one side.</b> For two righties or two lefties, someone's forehand is already in the middle, so stacking is optional. It still helps when one player has a much stronger forehand or prefers one side (The Kitchen, Pickleheads).</li>
<li><b>Hiding a weakness.</b> USA Pickleball's strategy tips list stacking or switching to get more forehands on the ball as one way to adjust when opponents keep attacking a weak shot.</li>
<li><b>Changing the picture.</b> Pickleheads also lists keeping momentum and unsettling opponents who are not adapting to your movement.</li>
</ul>
<p>USA Pickleball's <a href="{SK_USAP_SKILL}" target="_blank" rel="noopener">skill level descriptions</a> treat stacking as an intermediate strategy: basic knowledge of it at one level, a solid understanding of when and how to use it at the next, and partners who "easily stack" court positions above that.</p>
<h2>How to stack on the serve</h2>
<ol>
<li><b>Server goes where the score says.</b> The correct server stands in the correct serving area for the score, with at least one foot touching that serving area behind the baseline and neither foot on the court (rules 7.A.1 to 7.A.3).</li>
<li><b>Partner lines up on the same side.</b> If the score already puts you both on your preferred sides, line up normally. If it does not, the partner waits beside the server, toward the sideline, instead of crossing to the other half.</li>
<li><b>Stay out of the serve's way.</b> A serve that hits the server's partner is a fault against the server (rule 7.E.4). Pickleheads stresses standing where you do not impede the serve.</li>
<li><b>Slide after the serve.</b> Once the ball is served, both players move to their preferred sides and play the point from there.</li>
</ol>
<p>The serve stack is the easier half because the serving team stays back for the return anyway (the two-bounce rule), so there is time to move. The Kitchen suggests starting with serve-only stacking in rec games.</p>
<h2>How to stack on the return</h2>
<ol>
<li><b>Receiver goes where the score says.</b> The correct receiver stands in the service court for the score and must be the one to return the serve (rules 5.B.1, 5.C.1.c).</li>
<li><b>Partner waits at the kitchen line on the same side.</b> Pickleheads describes the non-receiver standing at the kitchen line, often just outside the sideline on the receiver's side.</li>
<li><b>Return deep with some arc.</b> Pickleheads suggests a deep return with less pace and a little arc, and The Kitchen a deep return with some loft. Both buy time for the switch. Pickleheads also suggests returning to the opponent straight across rather than crosscourt, for a little more time.</li>
<li><b>Switch on contact.</b> After the return, the partner slides across to their side of the kitchen line, covering the middle on the way, while the returner moves up to the kitchen line on the side the partner left.</li>
</ol>
<p>Because the receiving team switches during a live ball, the return stack is the one that needs communication, and the one where a slow move costs points.</p>
<h2>Half stack vs full stack</h2>
<p>Pickleheads calls stacking only when serving a "half stack," since stacking on the return is harder. Stacking on both serve and return is often called a full stack. Many teams also mix in "switch or stay" on the return point by point instead of switching every time, which The Kitchen notes as an option.</p>
<h2>The position rules that matter</h2>
<p>From the 2026 USA Pickleball Official Rulebook (rule numbers are the 2026 numbering):</p>
<div class="tbl"><table><thead><tr><th>Rule</th><th>What it says, in our words</th></tr></thead><tbody>{sk_rows}</tbody></table></div>
<p>A few more that come up when stacking:</p>
<ul>
<li><b>Out of position, rally stopped (5.C.1.a):</b> if the correct server or receiver was not in the correct position when the score was called and a player correctly stops the rally, the rally is replayed.</li>
<li><b>Out of position, rally finished (5.C.2):</b> if nobody stopped it, the result of the rally stands.</li>
<li><b>Wrong claim (5.C.1.b):</b> stopping a rally with an incorrect position claim is a fault against the player who stopped it.</li>
<li><b>Changing serving areas after the score call (6.D.2):</b> the server must let all players reposition, then re-call the score to restart the 10-second count.</li>
<li><b>Tournaments (18.C):</b> starting servers in doubles must wear the identification the Tournament Director requires, which helps everyone track who belongs where.</li>
<li><b>Rally scoring (14.A):</b> in the provisional rally-scoring option, only one player serves per side out, and service still begins with the player correctly positioned on the right for the team's score (14.A.4, 14.A.5).</li>
</ul>
<p>Kitchen rules do not change when you stack: <a href="pickleball-kitchen-rules.html">pickleball kitchen rules</a>. One-page rule summary: <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a>.</p>
<h2>How to signal</h2>
<p>The serve stack needs no signal. On the return, Pickleheads describes the common system: the partner at the kitchen line signals behind their back so the other team cannot see it.</p>
<ul>
<li><b>Open hand:</b> switch.</li>
<li><b>Closed fist:</b> stay.</li>
<li><b>Fake:</b> some teams add a signal for a fake switch to keep opponents guessing (Pickleheads, The Kitchen).</li>
</ul>
<p>You can also just talk to your partner, but Pickleheads points out that the other team hears it too. Agree on the signals before the game.</p>
<h2>Common stacking mistakes</h2>
<ul>
<li><b>Losing track of the score or server.</b> Stacking never changes who serves or the score, so The Kitchen suggests one partner tracks positions. If unsure, ask before the serve (rule 5.C).</li>
<li><b>The wrong player returns.</b> When positions are correct, a return by the wrong player is a fault (5.C.1.c).</li>
<li><b>Standing in the serve's path.</b> A serve that hits the server's partner is a fault against the server (7.E.4).</li>
<li><b>A lazy or late switch.</b> The Kitchen warns that a slow switch can leave a gap worse than not stacking at all. Pickleheads warns that strong drivers will hit into any open space while you move.</li>
<li><b>A fast, low return.</b> It gives you no time to switch. Go deep with some arc.</li>
<li><b>Running through your shot.</b> Pickleheads: be ready to stop and split step to hit, then keep moving into position.</li>
<li><b>Both reaching for the middle.</b> Once you are set, agree who takes the middle ball (The Kitchen).</li>
</ul>
<h2>When not to stack</h2>
<ul>
<li><b>When it puts a weak backhand in the middle,</b> or both backhands, unless that is your strength (Pickleheads).</li>
<li><b>When it takes a strong forehand away</b> by forcing that player to a side where they hit more backhands (Pickleheads).</li>
<li><b>When it causes more errors than it saves.</b> Pickleheads calls stacking an advanced concept: work on fundamentals and practice it before relying on it.</li>
<li><b>When opponents keep punishing the switch.</b> The Kitchen suggests signaling to stay put for a while.</li>
</ul>
<h2>How to practice it</h2>
<p>Start with the serve stack in casual games, expect a few mix-ups, and fix them before the next serve (The Kitchen). Then add the return stack with a deep, lofted return, which is the same soft control you build with <a href="third-shot-drop.html">third shot drops</a> and <a href="how-to-dink.html">dinks</a>. Partner warm-ups: <a href="pickleball-drills.html">pickleball drills</a>. Court layout and where the sidelines are: <a href="pickleball-court-dimensions.html">pickleball court dimensions</a>.</p>
{money_links()}
{sk_faq_html}
{sources([("USA Pickleball 2026 Official Rulebook (PDF)", RULES, f"rules 5.B.1 to 5.B.4, 5.C, 5.C.1.a to 5.C.1.c, 5.C.2, 6.D.2, 7.A, 7.E.4, 14.A.4, 14.A.5, 18.C, read {sk_checked}"),
          ("USA Pickleball: Skill levels", SK_USAP_SKILL, f"where stacking sits in the skill descriptions, read {sk_checked}"),
          ("USA Pickleball: How to develop a strategy to identify a player's strengths or weaknesses", SK_USAP_STRAT, f"stacking or switching to get more forehands on the ball, read {sk_checked}"),
          ("Pickleheads: What is stacking in pickleball?", SK_PH, f"serve and return setups, half stacking, hand signals, when not to stack, read {sk_checked}"),
          ("The Kitchen: How stacking in pickleball helps you own the middle", SK_KITCHEN, f"righty/lefty teams, switch/stay/fake, easing into it, read {sk_checked}")])}
{more("guides/pickleball-stacking.html")}'''
    page("guides/pickleball-stacking.html", "How to Stack in Pickleball: Serve and Return Stacking Explained", stk,
         "How to stack in pickleball doubles: half stack vs full stack, serve and return setups, hand signals, the USA Pickleball position rules, common faults and when not to stack.",
         fresh={"checked": SK_CHECKED, "rules": SK_RULES, "faq": sk_faq},
         schema=[sk_faq_ld])

    # ----- How to watch pro pickleball (Oct 29, 2026) -----
    # Every fact below was read on the linked official page on WT_CHECKED. Broadcast windows move; no invented times.
    WT_CHECKED = "2026-10-29"
    wt_checked = _dt.date.fromisoformat(WT_CHECKED).strftime("%B %-d, %Y")
    WT_PPA = "https://www.ppatour.com/watch/"
    WT_PPA_TV = "https://www.ppatour.com/watch/tv/"
    WT_PBTV = "https://pickleballtv.com/"
    WT_IOS = "https://apps.apple.com/us/app/pickleballtv/id6739588861"
    WT_PLAY = "https://play.google.com/store/apps/details?id=com.apppickleballtv"
    WT_UP_PRO = "https://worlds.unitedpickleball.com/ppa-tour"
    WT_MLP = "https://majorleaguepickleball.co/news/houston-hammers-to-join-major-league-pickleball-as-21st-team-for-2027-season/"
    WT_CBS = "https://pickleball.com/news/carvana-masters-broadcast-schedule-features-national-coverage-on-championship-sunday"
    WT_APP_CAL = "https://www.theapp.global/news/2026-app-tour-evolution-bigger-impact-more-scale-enhanced-pro-player-platform"
    WT_APP_DET = "https://www.theapp.global/news/detroit-preview-2026"
    WT_APP_OP = "https://www.theapp.global/news/sunday-broadcast-overland-park-2026"
    WT_UN_LIVE = "https://usapickleballnationals.com/livestream/"
    WT_NC_MLP = "https://majorleaguepickleball.co/news/match-schedule-for-mlp-nations-cup-released/"
    WT_NC_UP = "https://worlds.unitedpickleball.com/nations-cup"
    WT_WHO = [
        ("PPA Tour", "PickleballTV streams every round of every event", "Select rounds on Tennis Channel, FS1 and FS2 in the PPA's 2026 schedule; CBS carried Championship Sunday at the Carvana Masters in January", WT_PPA_TV),
        ("Major League Pickleball (MLP)", "PickleballTV", "MLP reports 2026 records on CBS (733K viewers, NYC Finals, Aug. 30) and FS1 (146K, Orlando, Aug. 1)", WT_MLP),
        ("APP Tour", "APPTV on YouTube (Players Court) and ESPN+ (Championship Court)", "National windows on ESPN2 and CBS Sports Network at some 2026 events", WT_APP_DET),
        ("USA Pickleball Nationals", "VS Sports livestreams and records every match", "None listed", WT_UN_LIVE),
    ]
    WT_WEEK = [
        ("Fri Oct 30", "MLP Nations Cup, pool play", "PickleballTV", "10 AM – 7 PM"),
        ("Sat Oct 31", "MLP Nations Cup, pool play", "PickleballTV", "10 AM – 7 PM"),
        ("Sun Nov 1", "MLP Nations Cup, semifinals", "PickleballTV", "10 AM – 1 PM"),
        ("Sun Nov 1", "MLP Nations Cup, finals", "PickleballTV", "2 – 3:30 PM"),
        ("Oct 31 – Nov 8", "USA Pickleball Nationals, San Diego", "VS Sports livestream", "Every match; match times posted closer to play"),
        ("Tue Nov 3", "PPA Worlds, round of 64", "PickleballTV", "11 AM – 7 PM"),
        ("Wed Nov 4", "PPA Worlds, round of 32", "PickleballTV", "11 AM – 7 PM"),
        ("Thu Nov 5", "PPA Worlds, round of 16", "PickleballTV", "11 AM – 6 PM"),
        ("Thu Nov 5", "PPA Worlds, Celebrity Pro-Am", "Tennis Channel and PickleballTV", "7 – 9 PM"),
        ("Fri Nov 6", "PPA Worlds, quarterfinals", "PickleballTV", "11 AM – 7 PM"),
        ("Sat Nov 7", "PPA Worlds, semifinals", "PickleballTV", "11 AM – 7 PM"),
        ("Sun Nov 8", "PPA Worlds, Championship Sunday", "PickleballTV", "10 AM – 4 PM"),
    ]
    WT_NEXT = [
        ("Nov 12–15", "APP Arizona Open, Mesa, AZ", "On the APP's 2026 nationally televised calendar; channels on the APP's event posts"),
        ("Nov 19–22", "PPA Proton Daytona Beach Open, Daytona Beach, FL", "PickleballTV, round of 16 through Championship Sunday"),
        ("Dec 3–6", "APP Tour Championships, Fort Lauderdale, FL", "On the APP's 2026 nationally televised calendar"),
        ("Dec 17–20", "PPA Veolia Malibu Showcase, Malibu, CA", "PickleballTV every day, plus Tennis Channel all four days"),
    ]
    wt_who_rows = "".join(f'<tr><th scope="row">{e(t)}</th><td>{e(s)}</td><td>{e(n)}</td><td><a href="{e(u)}" target="_blank" rel="noopener">source</a></td></tr>' for t, s, n, u in WT_WHO)
    wt_week_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(c)}</td><td>{e(t)}</td></tr>' for d, w, c, t in WT_WEEK)
    wt_next_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(c)}</td></tr>' for d, w, c in WT_NEXT)
    wt_faq = [
        ("What time is the MLP Nations Cup final?",
         "The MLP Nations Cup final was Sunday, November 1, 2026 at 2 p.m. CT at Brookhaven Country Club in Farmers Branch, Texas. Team USA beat Latin America 3-0. The semifinals were at 10 a.m. and 11:30 a.m. CT. Matches streamed on PickleballTV and the PickleballTV app. Results are on our MLP Nations Cup page."),
        ("Is PickleballTV free?",
         "Partly. PickleballTV runs a free 24/7 channel with selected matches and original shows, offered on Fubo, Samsung TV Plus, Roku, Fire TV and Plex. Every court, full replays and DVR features need a paid PickleballTV app subscription."),
        ("How much does the PickleballTV app cost?",
         "The App Store and Google Play listings say full access costs $5.99 a month or $59.99 a year, with a 30-day free trial. The app streams up to six courts live per event, plus on-demand replays."),
        ("What channel is pro pickleball on?",
         "Most pro pickleball streams on PickleballTV. In 2026 the PPA Tour also put select rounds on Tennis Channel, FS1 and FS2, and CBS aired Championship Sunday at the Carvana Masters. MLP matches aired on CBS and FS1. The APP Tour uses ESPN+, APPTV on YouTube, and national windows on ESPN2 and CBS Sports Network."),
        ("Is Pickleball Worlds 2026 on TV?",
         "The Celebrity Pro-Am is on Tennis Channel on Thursday, November 5, 7 to 9 p.m. CT. The pro main draw, November 3 to 8, streams on PickleballTV, per United Pickleball and the PPA Tour."),
        ("How can I watch PPA Worlds 2026?",
         "United Pickleball says every day of the main draw, from the round of 64 on Tuesday, November 3 through Championship Sunday on November 8, is live on PickleballTV. The Celebrity Pro-Am is on Tennis Channel and PickleballTV on Thursday, November 5, from 7 to 9 p.m. CT."),
        ("How do I watch the APP Tour?",
         "At 2026 APP events, Championship Court has aired on ESPN+ and the Players Court on APPTV on YouTube, per the APP. Some Championship Sundays also had national windows on ESPN2 or CBS Sports Network."),
        ("How can I watch USA Pickleball Nationals 2026?",
         "The official Nationals site says every match at the 2026 Oceanview USA Pickleball National Championships, October 31 to November 8 in San Diego, is livestreamed and recorded by VS Sports."),
    ]
    wt_faq_html, wt_faq_ld = faq(wt_faq)
    import os as _os
    from zoneinfo import ZoneInfo as _ZI
    _bd = _os.environ.get("DTP_BUILD_DATE")
    build_day = _dt.date.fromisoformat(_bd) if _bd else _dt.datetime.now(_ZI("America/Chicago")).date()
    _sat, _sun = _dt.date(2026, 11, 7), _dt.date(2026, 11, 8)
    _built = build_day.strftime("%B %-d, %Y")
    _wt_link = '<a href="../events/opendoor-pickleball-world-championships.html#this-weekend">Worlds weekend schedule</a>'
    if build_day == _sat:
        wt_weekend = (f'<p><b>Page built {_built}.</b> The published schedule has semifinals that day on <b>PickleballTV</b> from 11 AM to 7 PM CT, '
                      f'and Championship Sunday on November 8, first serve 10 AM CT, PickleballTV 10 AM to 4 PM CT. The 4 PM time is the broadcast window, not an event-end clock. '
                      f'A November 7 reading of United Pickleball marked Monday through Friday completed. Full table: {_wt_link}.</p>')
        wt_week_note = f'This page was built {_built}. PPA Worlds semifinals are on the published Saturday schedule, and Championship Sunday is November 8.'
    elif build_day == _sun:
        wt_weekend = (f'<p><b>Page built {_built}.</b> Semifinals were Saturday, November 7 (PickleballTV 11 AM to 7 PM CT). '
                      f'Championship Sunday is November 8: first serve 10 AM CT, PickleballTV 10 AM to 4 PM CT. The 4 PM time is the broadcast window. Full table: {_wt_link}.</p>')
        wt_week_note = f'This page was built {_built}. Championship Sunday is the remaining published PPA Worlds day. Semifinals were Saturday, November 7.'
    elif build_day > _sun:
        wt_weekend = (f'<p><b>Page built {_built}, after Championship Sunday.</b> Published windows were semifinals on Saturday, November 7, on <b>PickleballTV</b> from 11 AM to 7 PM CT, '
                      f'and Championship Sunday on November 8, first serve 10 AM CT, PickleballTV 10 AM to 4 PM CT. The 4 PM time is the broadcast window, not an event-end clock. Full table: {_wt_link}.</p>')
        wt_week_note = f'This page was built {_built}. The published PPA Worlds windows were semifinals on November 7 and Championship Sunday on November 8.'
    else:
        wt_weekend = (f'<p><b>Page built {_built}.</b> Published windows: semifinals Saturday, November 7, on <b>PickleballTV</b> from 11 AM to 7 PM CT, '
                      f'and Championship Sunday November 8, first serve 10 AM CT, PickleballTV 10 AM to 4 PM CT. The 4 PM time is the broadcast window. Full table: {_wt_link}.</p>')
        wt_week_note = f'This page was built {_built}. The published PPA Worlds windows are semifinals on November 7 and Championship Sunday on November 8.'
    watch = f'''<h1>How to watch pro pickleball on TV and streaming (2026)</h1>
<p class="meta">Where the PPA Tour, Major League Pickleball, the APP Tour and USA Pickleball Nationals stream and air, from the tours' own pages and the PickleballTV app listings, read {wt_checked}. Broadcast windows move, so confirm on the linked schedule before you tune in. Times are Central (CT) unless noted.</p>
<h2>The short answer</h2>
<ul>
<li><b>PPA Tour and MLP:</b> stream on <b>PickleballTV</b>. The {ext(WT_PPA, "PPA Tour")} says PickleballTV streams every round of every Carvana PPA Tour event, with marquee rounds on national TV.</li>
<li><b>APP Tour:</b> <b>ESPN+</b> for Championship Court and <b>APPTV on YouTube</b> for the Players Court, per the {ext(WT_APP_DET, "APP")}.</li>
<li><b>USA Pickleball Nationals:</b> every match is livestreamed and recorded by <b>VS Sports</b>, per the {ext(WT_UN_LIVE, "official Nationals site")}.</li>
</ul>
<h2 id="nations-cup-final">MLP Nations Cup final: result (Sunday Nov 1)</h2>
<p>The inaugural MLP Nations Cup final was <b>Sunday, November 1, 2026</b> at Brookhaven Country Club in Farmers Branch, Texas. <b>Team USA beat Latin America 3-0.</b> Scores and the published watch windows are on our <a href="../events/mlp-nations-cup-2026.html">MLP Nations Cup 2026 page</a>. The schedule {ext(WT_NC_MLP, "MLP published")} before the event, all on Championship Court, was:</p>
<ul><li><b>Semifinal 1:</b> 10:00 AM CT (Group A No. 2 vs Group B No. 1). Result: Latin America def. Asia Domestic 3-1.</li><li><b>Semifinal 2:</b> 11:30 AM CT (Group A No. 1 vs Group B No. 2). Result: USA def. Europe East 3-1.</li><li><b>Final:</b> 2:00 PM CT. Result: USA def. Latin America 3-0.</li></ul>
<p><b>Where it streamed:</b> <b>PickleballTV</b> and the PickleballTV app. MLP said all Nations Cup matches were available there, and {ext(WT_NC_UP, "United Pickleball")} listed PickleballTV windows of 10 AM to 1 PM CT for the semifinals and 2 to 3:30 PM CT for the final.</p>
<h2 id="ppa-worlds">How to watch PPA Worlds 2026 (published windows)</h2>
{wt_weekend}
<ul><li><b>Mon Nov 2 (completed):</b> pro qualifying in all five pro events; no stream window listed. First serve was recorded as 8 AM CT per United Pickleball and the PPA's Oct 28 X post; the PPA event page still listed 11 AM on a November 7 recheck. Details: <a href="../events/opendoor-pickleball-world-championships.html#qualifying">Worlds qualifying Monday</a>.</li><li><b>Tue Nov 3 to Fri Nov 6 (completed):</b> round of 64 through quarterfinals on <b>PickleballTV</b>, 11 AM to 7 PM CT (6 PM on Thursday).</li><li><b>Thu Nov 5 (completed):</b> Celebrity Pro-Am on <b>Tennis Channel</b> and PickleballTV, 7 to 9 PM CT.</li><li><b>Sat Nov 7:</b> semifinals on <b>PickleballTV</b>, 11 AM to 7 PM CT.</li><li><b>Sun Nov 8:</b> Championship Sunday on PickleballTV, 10 AM to 4 PM CT. The 4 PM time is the broadcast window.</li></ul>
<p>The PPA released the seeded draws on October 31. Full day-by-day table, draws and FAQs: <a href="../events/opendoor-pickleball-world-championships.html#how-to-watch">how to watch Pickleball Worlds 2026</a>.</p>
<p><b>Gear up for Worlds:</b> <a href="../paddle-volair-mach-1-forza.html">Volair Mach 1 Forza</a> · <a href="../paddle-volair-mach-2-forza.html">Volair Mach 2 Forza</a> · <a href="../paddle-volair-cmd-el-16mm.html">Volair CMD EL 16mm</a> · <a href="../guides/pickleball-gift-guide-2026.html">2026 gift guide</a> · <a href="../discount-codes.html">discount codes</a></p>
<h2>Who streams what</h2>
<div class="tbl"><table><thead><tr><th>Tour or event</th><th>Streaming</th><th>National TV</th><th>Source</th></tr></thead><tbody>{wt_who_rows}</tbody></table></div>
<p>The CBS window at the Carvana Masters ran 12 to 2 p.m. ET on Championship Sunday in January 2026, per {ext(WT_CBS, "Pickleball.com")}. MLP's viewer numbers are from its {ext(WT_MLP, "October 28, 2026 release")}.</p>
<h2>PickleballTV: free channel vs the app</h2>
<p><b>The free channel.</b> {ext(WT_PBTV, "PickleballTV")} runs 24/7 and says it is offered on <b>Fubo, Samsung TV Plus, Roku, Fire TV and Plex</b>. The app listings describe this free FAST channel as carrying selected matches and original shows.</p>
<p><b>The paid app.</b> The {ext(WT_IOS, "App Store")} (iPhone, iPad, Apple TV) and {ext(WT_PLAY, "Google Play")} listings say the app is a free download, and full access costs <b>$5.99 a month or $59.99 a year</b>, with a 30-day free trial. Paid access adds up to six live courts per event, full replays on demand, and pause and rewind. The listings say it covers more than 3,000 live hours from 32 PPA and MLP tournaments a year.</p>
<p>So if you only want the feature court, the free channel may be enough. If you want to follow one player on an outer court, or rewatch a match, you need the app.</p>
<h2>This week: Nations Cup, Nationals and PPA Worlds</h2>
<p>The table is the published week of windows, not a live board. The Nations Cup ended November 1 (Team USA won; <a href="../events/mlp-nations-cup-2026.html">results</a>). {wt_week_note} Nations Cup times are converted from the {ext(WT_PPA, "PPA's watch page")} (listed in ET). PPA Worlds times are from {ext(WT_UP_PRO, "United Pickleball")} (listed in CT), which says windows can move. All times CT.</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>Event</th><th>Where to watch</th><th>Window (CT)</th></tr></thead><tbody>{wt_week_rows}</tbody></table></div>
<p>PPA pro qualifying on Monday, November 2 had no stream window on the PPA's schedule when we checked. For tickets, parking and rosters, see our <a href="../events/mlp-nations-cup-2026.html">MLP Nations Cup 2026</a>, <a href="../events/usa-pickleball-nationals-2026.html">USA Pickleball Nationals 2026</a> and <a href="../events/opendoor-pickleball-world-championships.html">PPA Worlds 2026</a> guides.</p>
<p>For the full Worlds day-by-day schedule, ticket prices and entrants, see <a href="../events/opendoor-pickleball-world-championships.html">Pickleball World Championships 2026: schedule, TV and tickets</a>.</p>
<h2>Coming up after Worlds</h2>
<div class="tbl"><table><thead><tr><th>Dates</th><th>Event</th><th>Coverage listed</th></tr></thead><tbody>{wt_next_rows}</tbody></table></div>
<p>PPA rows are from the {ext(WT_PPA_TV, "PPA TV schedule")}. APP rows are from the APP's {ext(WT_APP_CAL, "2026 nationally televised calendar")}. The APP posts exact channels and times in a broadcast post during each event, like its {ext(WT_APP_OP, "Overland Park Championship Sunday post")} (APPTV, ESPN+ and ESPN2). Full pro calendar: <a href="../tournaments.html">upcoming tournaments</a>.</p>
<h2>Tips</h2>
<ul>
<li><b>Check the time zone.</b> The PPA lists ET. United Pickleball's Worlds pages list CT.</li>
<li><b>Look for the official schedule on the day.</b> Order of play and court assignments come out shortly before each day, so a match you want may land on an outer court that only the paid app carries.</li>
<li><b>Replays:</b> the PickleballTV app has on-demand replays, and VS Sports records every Nationals match.</li>
</ul>
<h2>Gear while you watch</h2>
<p>Seen a paddle you like on the broadcast? Our <a href="../pro-paddles.html">pro paddles page</a> lists what the pros use. Then check the <a href="/discount-codes">pickleball discount codes</a> and today's <a href="../deals.html">paddle deals</a> before you pay full price.</p>
{wt_faq_html}
{sources([("Major League Pickleball: Nations Cup match schedule", WT_NC_MLP, f"semifinal and final times (CT) and PickleballTV, read October 31, 2026"),
          ("United Pickleball: MLP Nations Cup", WT_NC_UP, "PickleballTV windows for Sunday semifinals and final (CT), read October 31, 2026"),
          ("PPA Tour: Watch pro pickleball", WT_PPA, f"PickleballTV coverage, Nations Cup and Worlds windows (ET), read {wt_checked}"),
          ("PPA Tour: TV schedule", WT_PPA_TV, f"2026 broadcast and streaming windows, read {wt_checked}"),
          ("United Pickleball: Worlds pro play", WT_UP_PRO, f"Worlds windows in CT, read {wt_checked}"),
          ("PickleballTV", WT_PBTV, "free 24/7 channel and platforms"),
          ("PickleballTV on the App Store", WT_IOS, f"app prices and features, read {wt_checked}"),
          ("PickleballTV on Google Play", WT_PLAY, "app prices and features"),
          ("Pickleball.com: Carvana Masters broadcast schedule", WT_CBS, "CBS window, January 13, 2026"),
          ("Major League Pickleball: Houston Hammers release", WT_MLP, "2026 CBS and FS1 viewership, October 28, 2026"),
          ("APP: 2026 APP Tour evolution", WT_APP_CAL, "2026 nationally televised calendar, December 23, 2025"),
          ("APP: Detroit Open preview", WT_APP_DET, "ESPN+, APPTV on YouTube, ESPN2 and CBS Sports Network, August 19, 2026"),
          ("APP: Championship Sunday from Overland Park", WT_APP_OP, "APPTV, ESPN+ and ESPN2, September 20, 2026"),
          ("USA Pickleball Nationals: Livestream", WT_UN_LIVE, "VS Sports livestream and recordings")])}
{gift_pages.holiday_note("watch")}
{more("guides/how-to-watch-pro-pickleball.html")}'''
    page("guides/how-to-watch-pro-pickleball.html", "How to watch pro pickleball: TV channels, PickleballTV and streaming (2026)", watch,
         "How to watch pro pickleball in 2026: PickleballTV free channel vs $5.99 app, PPA and MLP on Tennis Channel, FS1 and CBS, APP on ESPN+, plus PPA Worlds windows.",
         fresh={"checked": WT_CHECKED, "who": WT_WHO, "week": WT_WEEK, "next": WT_NEXT, "faq": wt_faq, "weekend_bucket": ("sat" if build_day == _sat else "sun" if build_day == _sun else "after" if build_day > _sun else "before")},
         schema=[wt_faq_ld])

    # ----- PPA Worlds 2026 -----
    PPA_EV = "https://www.ppatour.com/events/2026/pickleball-world-championships/"
    PPA_TODAY = "https://www.ppatour.com/events/2026/pickleball-world-championships/today/"
    UP_HOME = "https://worlds.unitedpickleball.com/"
    UP_SCHED = "https://worlds.unitedpickleball.com/schedule"
    UP_TIX = "https://worlds.unitedpickleball.com/tickets"
    FB_CITY = "https://discoverfarmersbranch.com/pickleball/"
    # /events/ppa-worlds-2026 merged into OW_FN; 301 in src/worker.js (WORLDS_301).
    # ----- Opendoor Pickleball World Championships 2026: full search-answer page (refresh of the event card) -----
    # Every fact read on the linked official pages (plus the cited Kitchen schedule) on OW_CHECKED. Times CT (UTC-6 after DST ends Nov 1).
    from urls import clean_path as _cp
    OW_CHECKED = "2026-11-01"
    ow_checked = _dt.date.fromisoformat(OW_CHECKED).strftime("%B %-d, %Y")
    OW_FN = "events/opendoor-pickleball-world-championships.html"
    PPA_WATCH, PPA_TV = "https://www.ppatour.com/watch/", "https://www.ppatour.com/watch/tv/"
    UP_PRO = "https://worlds.unitedpickleball.com/ppa-tour"
    PPA_CELEB = "https://www.ppatour.com/municipal-celebrity-pickleball-showdown-wahlberg/"
    KITCHEN = "https://thekitchenpickle.com/blogs/news/2026-pickleball-world-championships-schedule-events-dallas/"
    PBTV, PBTV_IOS = "https://pickleballtv.com/", "https://apps.apple.com/us/app/pickleballtv/id6739588861"
    OW_DAYS = [
        ("Fri Oct 30", "MLP Nations Cup: round-robin play (8 international teams)", "Pool play on PickleballTV 10 AM – 7 PM"),
        ("Sat Oct 31", "MLP Nations Cup: round-robin play", "Pool play on PickleballTV 10 AM – 7 PM"),
        ("Sun Nov 1", "MLP Nations Cup: single-elimination semifinals and final", "Semis 10 AM – 1 PM, finals 2 – 3:30 PM on PickleballTV"),
        ("Mon Nov 2", "PPA pro qualifying, all five pro events", "First serve 8 AM CT per United Pickleball and the PPA's Oct 28 X post (PPA event page still lists 11 AM); no stream window listed"),
        ("Tue Nov 3", "Main draw: round of 64", "First serve 11 AM; PickleballTV 11 AM – 7 PM"),
        ("Wed Nov 4", "Main draw: round of 32", "First serve 11 AM; PickleballTV 11 AM – 7 PM"),
        ("Thu Nov 5", "Main draw: round of 16. PPA Challenger Showdown singles pool play. Celebrity Pickleball Showdown at 7 PM", "PickleballTV 11 AM – 6 PM; Pro-Am 7 – 9 PM on Tennis Channel and PickleballTV"),
        ("Fri Nov 6", "Quarterfinals: singles and mixed (morning session), men's and women's doubles (evening session). Challenger Showdown doubles and mixed pool play", "First serve 11 AM; PickleballTV 11 AM – 7 PM"),
        ("Sat Nov 7", "Semifinals (men's and women's doubles in the evening session). Challenger Showdown semifinals and finals", "First serve 11 AM; PickleballTV 11 AM – 7 PM"),
        ("Sun Nov 8", "Championship Sunday: finals in all five pro events", "First serve 10 AM; PickleballTV 10 AM – 4 PM"),
    ]
    OW_TIX = [("Grounds Pass, any day", "$30.42"), ("Courtside Bleacher", "$46.66 – $92.03"), ("Courtside Chair", "$113.69 – $221.99"),
              ("VIP", "$276.13 – $438.58"), ("Box Suite, daily", "$3,254.23 – $9,751.90"), ("Weeklong Grounds Pass", "$113.69"),
              ("Weeklong Courtside, Chair, VIP and Box Suite", "Sold out")]
    OW_CHAMPS = [("Men's singles", "Federico Staksrud"), ("Women's singles", "Anna Leigh Waters"),
                 ("Men's doubles", "Hayden Patriquin and Federico Staksrud"), ("Women's doubles", "Anna Leigh Waters and Anna Bright"),
                 ("Mixed doubles", "Anna Leigh Waters and Ben Johns")]
    OW_WATCH = [  # United Pickleball pro page (CT) and PPA watch page / event page (ET, one hour later), read 2026-10-31
        ("Mon Nov 2", "Pro qualifying, all five pro events", "No stream window listed", "First serve 8 AM CT per United Pickleball and the PPA's Oct 28 X post (PPA event page still lists 11 AM)"),
        ("Tue Nov 3", "Main draw: round of 64", "PickleballTV", "11 AM – 7 PM"),
        ("Wed Nov 4", "Main draw: round of 32", "PickleballTV", "11 AM – 7 PM"),
        ("Thu Nov 5", "Main draw: round of 16", "PickleballTV", "11 AM – 6 PM"),
        ("Thu Nov 5", "Celebrity Pro-Am (MUNICIPAL Celebrity Pickleball Showdown)", "Tennis Channel and PickleballTV", "7 – 9 PM"),
        ("Fri Nov 6", "Quarterfinals", "PickleballTV", "11 AM – 7 PM"),
        ("Sat Nov 7", "Semifinals", "PickleballTV", "11 AM – 7 PM"),
        ("Sun Nov 8", "Championship Sunday: finals in all five pro events", "PickleballTV", "10 AM – 4 PM"),
    ]
    ow_watch_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(c)}</td><td>{e(t)}</td></tr>' for d, w, c, t in OW_WATCH)
    ow_day_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(t)}</td></tr>' for d, w, t in OW_DAYS)
    ow_tix_rows = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in OW_TIX)
    ow_champ_rows = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in OW_CHAMPS)
    ow_faq = [
        ("When is the 2026 Pickleball World Championships?",
         "The PPA Tour's Opendoor Pickleball World Championships run November 2 to 8, 2026, at Brookhaven Country Club, 3333 Golfing Green Dr, Farmers Branch, Texas. The published schedule puts semifinals on Saturday, November 7 (PickleballTV 11 a.m. to 7 p.m. CT) and Championship Sunday on November 8 (first serve 10 a.m. CT; PickleballTV lists coverage until 4 p.m. CT, which is a broadcast window, not a published event-end time). A November 7, 2026 reading of United Pickleball marked Monday through Friday completed. That reading is not a live board. United Pickleball bills the full Worlds week as October 30 to November 8 because the MLP Nations Cup opened it."),
        ("When are the PPA Worlds qualifiers?",
         "PPA Worlds qualifiers are on Monday, November 2, 2026, the first day of the PPA event, and Championship Sunday is November 8, per United Pickleball's week schedule. First serve is 8 a.m. CT per United Pickleball and the PPA's October 28 post on X; the PPA event page still lists 11 a.m. Check the Order of Play in the MATCHDAY app."),
        ("When does PPA Worlds qualifying start?",
         "Pro qualifying for all five pro events was Monday, November 2, 2026, and United Pickleball's pro page marked that day completed on a November 7, 2026 recheck. The first-serve time on the record is 8 a.m. CT per an earlier reading of United Pickleball and the PPA's October 28 post on X. The PPA event page still listed 11 a.m. on that November 7 recheck. This page does not drop either source."),
        ("Is Worlds qualifying streamed?",
         "No stream window is listed for Monday qualifying. The PPA event page shows no live channel for Monday, November 2, and United Pickleball's PickleballTV schedule starts with the round of 64 on Tuesday, November 3. The PPA's MATCHDAY app lists live scores, brackets and order of play."),
        ("Is the main draw November 2 to 8 or November 3 to 8?",
         "Both dates appear because they describe different things. November 2 to 8 is the whole PPA event, including Monday qualifying. The main draw starts with the round of 64 on Tuesday, November 3 and ends November 8."),
        ("Where is PPA Worlds 2026?",
         "Brookhaven Country Club, 3333 Golfing Green Dr, Farmers Branch, TX 75234. That is the address on the club's own contact page (invitedclubs.com, read November 7, 2026) and on the PPA at-the-event page. United Pickleball's Nations Cup page prints 3334 Golfing Green Drive for the same club; this page uses the club's number. Brookhaven is the club and Farmers Branch is the city. General parking is at Dallas College Brookhaven Campus, Lot P3, 3939 Valley View Lane, with free shuttles to the venue."),
        ("How can I watch Pickleball Worlds 2026?",
         "Every day of the main draw is live on PickleballTV, Tuesday, November 3 through Sunday, November 8. The Celebrity Pro-Am is on Tennis Channel and PickleballTV on Thursday, November 5 from 7 to 9 p.m. CT. PickleballTV's free 24/7 channel carries selected matches; every court and replays need the paid PickleballTV app."),
        ("Is Pickleball Worlds on TV?",
         "Yes, for one night. The Celebrity Pro-Am is on Tennis Channel on Thursday, November 5, from 7 to 9 p.m. CT, per the PPA Tour and United Pickleball. The pro main draw, Tuesday, November 3 through Championship Sunday, November 8, streams on PickleballTV; neither official schedule lists another TV channel for it."),
        ("What time does Worlds start each day?",
         "The published pattern is Monday qualifying at 8 a.m. CT per United Pickleball and the PPA's October 28 post on X, while the PPA event page still listed 11 a.m. on a November 7, 2026 recheck. Tuesday through Saturday are listed at 11 a.m. CT and Championship Sunday at 10 a.m. CT. PickleballTV coverage runs 11 a.m. to 7 p.m. CT Tuesday to Saturday (to 6 p.m. Thursday) and 10 a.m. to 4 p.m. CT Sunday, per United Pickleball. On November 7, United Pickleball's court board showed semifinals with Championship Court first up at 11:00 a.m. CT and court SC1 first up at 8:45 a.m. CT. Those are the times on the board at that reading, not a promise they stay put. Gate times had not been posted when we checked."),
        ("Are the PPA Worlds 2026 draws and seeds out?",
         "Yes. The PPA released the draws on October 31 with a draw reveal show on PPA Tour YouTube. The full seeded main draws are on the PPA event page and United Pickleball's pro page, which fill in scores as matches finish."),
        ("How much are tickets to the Pickleball World Championships in Dallas?",
         "These figures are not a live checkout price. United Pickleball's ticket page, re-read November 7, 2026, still prints a Grounds Pass at $30.42, Courtside Bleacher seats from $46.66 to $92.03, and a Weeklong Grounds Pass at $113.69, and it says those numbers are Tixr data from October 11, 2026, fees included. Prices vary by day and demand. Confirm the current total on Tixr before you pay."),
        ("How much prize money is at PPA Worlds 2026?",
         "The PPA Tour lists a total payout of $1,648,641 across the five pro divisions, including appearance fees. It is a PPA Major, worth 3,000 ranking points per division title."),
        ("Who is playing at PPA Worlds 2026?",
         "The PPA says every No. 1 seed is entered and highlights Anna Leigh Waters, Len Yang and Rachel Rohrabacher in the draw. The defending champions are Federico Staksrud (men's singles), Anna Leigh Waters (women's singles), Hayden Patriquin and Federico Staksrud (men's doubles), Anna Leigh Waters and Anna Bright (women's doubles), and Anna Leigh Waters and Ben Johns (mixed)."),
    ]
    ow_faq_html, ow_faq_ld = faq(ow_faq)
    BH_CONTACT = "https://www.invitedclubs.com/clubs/brookhaven-country-club/contact-us/"
    ow_event = {"@type": "SportsEvent", "name": "Opendoor Pickleball World Championships 2026",
                "description": "PPA pro event November 2 to 8, 2026 at Brookhaven Country Club, 3333 Golfing Green Dr, Farmers Branch, Texas, the address on the club's contact page. Qualifying first serve on this page is 8:00 a.m. CT from United Pickleball and the PPA's October 28 X post; the PPA event page listed 11:00 a.m. on a November 7, 2026 recheck. endDate is the published last day, November 8, with no clock time. PickleballTV's 4:00 p.m. CT Sunday window is a broadcast end, not a published event-end time.",
                "sport": "Pickleball", "startDate": "2026-11-02T08:00:00-06:00", "endDate": "2026-11-08",
                "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "url": PPA_EV, "organizer": {"@type": "Organization", "name": "Carvana PPA Tour", "url": "https://www.ppatour.com/"},
                "location": {"@type": "Place", "name": "Brookhaven Country Club",
                             "address": {"@type": "PostalAddress", "streetAddress": "3333 Golfing Green Dr", "addressLocality": "Farmers Branch",
                                         "addressRegion": "TX", "postalCode": "75234", "addressCountry": "US"}}}
    ow_go = [(_cp("events/mlp-nations-cup-2026.html"), "MLP Nations Cup 2026: teams and how to watch"),
             (_cp("guides/how-to-watch-pro-pickleball.html"), "How to watch pro pickleball: PickleballTV free vs app"),
             (_cp("pro-paddles.html"), "What paddles the pros use"),
             (_cp("discount-codes.html"), "Pickleball discount codes"),
             (_cp("guides/pickleball-gift-guide-2026.html"), "2026 pickleball gift guide"),
             (_cp("deals/black-friday-pickleball-deals-2026.html"), "Black Friday paddle deals hub")]
    ow_links = '<aside class="holi" aria-label="Related guides"><p><b>Plan the rest of Worlds week</b></p>' + "".join(f'<a class="holia" href="/{u}">{e(t)} →</a>' for u, t in ow_go) + "</aside>"
    OW_GEAR = [(_cp("paddle-volair-mach-1-forza.html"), "Volair Mach 1 Forza review"),
               (_cp("paddle-volair-mach-2-forza.html"), "Volair Mach 2 Forza review"),
               (_cp("paddle-volair-cmd-el-16mm.html"), "Volair CMD EL 16mm review"),
               (_cp("guides/pickleball-gift-guide-2026.html"), "2026 pickleball gift guide"),
               (_cp("discount-codes.html"), "Pickleball discount codes")]
    ow_gear = '<aside class="holi" aria-label="Gear up for Worlds"><p><b>Gear up for Worlds</b></p>' + "".join(f'<a class="holia" href="/{u}">{e(t)} →</a>' for u, t in OW_GEAR) + "</aside>"
    _sched = ("Saturday, November 7 is semifinals on the published schedule: PickleballTV 11 AM to 7 PM CT, and the PPA event page lists a first serve of 11:00 AM. "
              "Sunday, November 8 is Championship Sunday: first serve 10:00 AM CT, PickleballTV 10 AM to 4 PM CT. "
              "The 4 PM time is the published broadcast window, not an event-end clock.")
    if build_day == _sat:
        ow_h2 = "Built November 7, 2026: semifinals, then Championship Sunday"
        ow_lead = (f"<p id=\"ow-weekend-lead\"><b>This page was built on November 7, 2026.</b> {_sched} "
                   f"{ext(UP_PRO, 'United Pickleball')} that day marked Monday, November 2 through Friday, November 6 completed.</p>")
    elif build_day == _sun:
        ow_h2 = "Built November 8, 2026: Championship Sunday"
        ow_lead = ("<p id=\"ow-weekend-lead\"><b>This page was built on November 8, 2026.</b> Semifinals were Saturday, November 7. "
                   "Championship Sunday is November 8: first serve 10:00 AM CT, PickleballTV 10 AM to 4 PM CT. "
                   "The 4 PM time is the broadcast window, not an event-end clock. Semifinal winners are not listed on this build.</p>")
    elif build_day > _sun:
        ow_h2 = "PPA Worlds weekend: the published schedule"
        ow_lead = (f"<p id=\"ow-weekend-lead\"><b>This page was built on {_built}, after Championship Sunday.</b> "
                   "The event dates were November 2 to 8, 2026. The published windows were semifinals on Saturday, November 7 "
                   "(PickleballTV 11 AM to 7 PM CT) and Championship Sunday on November 8 (first serve 10:00 AM CT, PickleballTV 10 AM to 4 PM CT). "
                   "The 4 PM time is the broadcast window, not an event-end clock. This build does not list semifinal or final match winners.</p>")
    else:
        ow_h2 = "Weekend schedule: semifinals Saturday and Championship Sunday"
        ow_lead = f"<p id=\"ow-weekend-lead\"><b>Published schedule, not a live board.</b> This copy was built on {_built}. {_sched}</p>"
    ow_snapshot = (f'<p><b>Court board snapshot, read November 7, 2026:</b> {ext(UP_PRO, "United Pickleball\'s pro page")} showed semifinals with '
                   'Championship Court first up at 11:00 AM CT and court SC1 first up at 8:45 AM CT. That board is the reading from that date, not the order of play on a later day. '
                   f'The same reading did not include a final semifinal winner list, and the {ext(PPA_EV, "PPA event page")} labeled semifinals "Live · auto-updating." '
                   'This page does not list semifinal winners.</p>')
    ow_weekend_js = """<script>(function(){var h=document.getElementById("this-weekend"),p=document.getElementById("ow-weekend-lead");if(!h||!p)return;var n=Date.now();
if(n>=Date.UTC(2026,10,9,6)){h.textContent="PPA Worlds weekend: the published schedule";p.textContent="The event dates were November 2 to 8, 2026. Published windows: semifinals Saturday November 7, PickleballTV 11 AM to 7 PM CT. Championship Sunday November 8, first serve 10 AM CT, PickleballTV 10 AM to 4 PM CT. The 4 PM time is the broadcast window, not an event-end clock. Semifinal winners are not listed on this page.";}
else if(n>=Date.UTC(2026,10,8,6)){h.textContent="Championship Sunday, November 8, 2026";p.textContent="Semifinals were Saturday, November 7. Championship Sunday is November 8: first serve 10:00 AM CT, PickleballTV 10 AM to 4 PM CT. The 4 PM time is the broadcast window, not an event-end clock. Semifinal winners are not listed here.";}
})();</script>"""
    ow = f'''<h1>Pickleball World Championships 2026: schedule, how to watch and tickets</h1>
<p class="meta">The Carvana PPA Tour's Opendoor Pickleball World Championships ("PPA Worlds"), Farmers Branch, Texas (Dallas area). Schedule rechecked November 7, 2026 on the PPA event page and United Pickleball's pro page. The weekend lead below follows the date this page was built, so a later rebuild does not keep calling November 7 current. Earlier facts keep the date they were read. All times Central (CT). Times can move, so confirm on the official pages.</p>
<h2 id="this-weekend">{ow_h2}</h2>
{ow_lead}
{ow_snapshot}
{ow_weekend_js}
<h2 id="qualifying">Worlds qualifying Monday, Nov 2: schedule and how to follow</h2>
<p><b>What it is:</b> Monday, November 2 is pro qualifying for all five pro events (men's and women's singles, men's and women's doubles, and mixed), per the {ext(PPA_EV, "PPA event page")}. Qualifying is the day before the seeded main draw starts with the round of 64 on Tuesday.</p>
<ul>
<li><b>First serve on the record:</b> 8 AM CT per an earlier reading of {ext(UP_PRO, "United Pickleball's pro schedule")} and the PPA's <a href="https://x.com/PPAtour/status/2115563515494924594" target="_blank" rel="noopener">Oct 28 X post</a>. The {ext(PPA_EV, "PPA event page")} still listed 11 AM on November 7, 2026. United Pickleball marked Monday completed that day. Both times stay on this page.</li>
<li><b>Streaming:</b> no stream window is listed for Monday. The PPA event page shows no live channel for qualifying day, and United Pickleball's PickleballTV schedule starts Tuesday.</li>
<li><b>Where to follow:</b> the PPA's MATCHDAY app (iOS and Android) lists live scores, brackets, order of play and match alerts, per the {ext(PPA_WATCH, "PPA watch page")}. The PPA event page lists Grounds Pass tickets for Monday if you want to go.</li>
</ul>
<p><b>Then the main draw, November 3 to 8:</b> the round of 64 starts Tuesday at 11 AM CT, with PickleballTV every day through Championship Sunday. See <a href="#how-to-watch">how to watch Pickleball Worlds 2026</a> for the full day-by-day windows.</p>
{ow_gear}
<h2>Pickleball Worlds 2026 schedule: Worlds week vs the main draw</h2>
<ul>
<li><b>Worlds week: October 30 to November 8, 2026.</b> {ext(UP_HOME, "United Pickleball")} bills ten days of Worlds, opened by the MLP Nations Cup on October 30 to November 1.</li>
<li><b>PPA pro event: November 2 to 8.</b> The {ext(PPA_EV, "PPA Tour event page")} lists these dates. Monday, November 2 is pro qualifying.</li>
<li><b>Main draw: November 3 to 8.</b> The round of 64 starts Tuesday, November 3, and Championship Sunday is November 8, per the {ext(UP_PRO, "United Pickleball pro page")}.</li>
</ul>
<p>So "November 2 to 8" and "November 3 to 8" are both right: the first includes Monday qualifying, the second is the main draw only.</p>
<h2>Venue and parking</h2>
<p><b>Brookhaven Country Club</b>, 3333 Golfing Green Dr, <b>Farmers Branch, TX 75234</b>. That street address is on the {ext(BH_CONTACT, "club's own contact page")} (read November 7, 2026) and on the {ext(PPA_TODAY, "PPA's at-the-event page")}. {ext("https://worlds.unitedpickleball.com/nations-cup", "United Pickleball's Nations Cup page")} prints 3334 Golfing Green Drive for the same club; this page uses the club's number. General parking is at <b>Dallas College Brookhaven Campus, Lot P3</b>, 3939 Valley View Lane, with free shuttles from about 6:30 AM to 11 PM daily, October 30 to November 8. Rideshare drop-off is on Brookhaven Drive, just past Golfing Green Drive. Box Suite ticket holders get on-site parking. Overnight and RV parking is not allowed.</p>
<p>Brookhaven or Farmers Branch? Both names are right: Brookhaven is the club, Farmers Branch is the city. The {ext(FB_CITY, "City of Farmers Branch")} gives the same address and has a resident-only parking permit rule on streets near the club from October 30 to November 8, so use Lot P3.</p>
<h2>Day-by-day schedule (CT): PPA Worlds qualifiers to Championship Sunday</h2>
<div class="tbl"><table><thead><tr><th>Day</th><th>Pro events and divisions</th><th>Start and stream (CT)</th></tr></thead><tbody>{ow_day_rows}</tbody></table></div>
<p>Pro rounds and first-serve times are from the {ext(PPA_EV, "PPA event page")}; morning and evening session splits are from {ext(UP_TIX, "United Pickleball's ticket page")}; stream windows are from the {ext(UP_PRO, "United Pickleball pro page")} (CT) and match the {ext(PPA_WATCH, "PPA watch page")} (ET, one hour later). Nations Cup windows are converted from the PPA watch page's ET listing. The five pro events are men's and women's singles, men's and women's doubles, and mixed doubles. Amateur divisions run all week; your times are on your bracket at pickleballtournaments.com.</p>
<p><b>Monday start time, kept on the record:</b> 8 AM CT per an earlier reading of United Pickleball and the PPA's <a href="https://x.com/PPAtour/status/2115563515494924594" target="_blank" rel="noopener">Oct 28 X post</a>. The PPA event page still listed 11 AM on November 7, 2026, and United Pickleball marked Monday completed. Tuesday to Saturday are listed at 11 AM CT and Championship Sunday at 10 AM CT. More on <a href="#qualifying">Monday qualifying</a> and <a href="#this-weekend">this weekend</a>.</p>
<p>Off the pro courts: live music runs on the Pickleball Boulevard Stage every day from November 1 to 7, with Clayton Mullen on Friday, November 6 from 6:30 to 8 PM, per {ext(UP_SCHED, "United Pickleball's schedule")}. {ext(KITCHEN, "The Kitchen")} has the full daily list of clinics and socials.</p>
<h2 id="how-to-watch">How to watch Pickleball Worlds 2026</h2>
<p>The short answer: <b>PickleballTV every day of the main draw</b> (Tuesday, November 3 to Sunday, November 8), plus the <b>Celebrity Pro-Am on Tennis Channel</b> on Thursday, November 5 at 7 PM CT. All times Central (CT), from the {ext(UP_PRO, "United Pickleball pro page")}; the {ext(PPA_WATCH, "PPA watch page")} lists the same windows in ET, one hour later. Windows can move.</p>
<div class="tbl"><table><thead><tr><th>Date</th><th>What's on</th><th>Where to watch</th><th>Time (CT)</th></tr></thead><tbody>{ow_watch_rows}</tbody></table></div>
<p><b>Draws and seeds:</b> the PPA released the draws on October 31 (see the PPA's {ext("https://www.youtube.com/watch?v=DtWX52IoO2c", "draw reveal show")}). Seeded main draws, from 64-player singles to 32-team doubles and mixed, are on the {ext(PPA_EV, "PPA event page")} and {ext(UP_PRO, "United Pickleball")}. We don't list seeds here until we can read them from an official seed list.</p>
<ul>
<li><b>PickleballTV, every day of the main draw:</b> Tue Nov 3 to Sat Nov 7 from 11 AM, ending 7 PM (6 PM on Thursday), and Championship Sunday 10 AM – 4 PM CT, per {ext(UP_PRO, "United Pickleball")} and the {ext(PPA_TV, "PPA TV schedule")}.</li>
<li><b>Celebrity Pro-Am on Tennis Channel:</b> the MUNICIPAL Celebrity Pickleball Showdown, headlined by Mark Wahlberg, is <b>Thursday, November 5, 7 – 9 PM CT</b> on Tennis Channel and PickleballTV, per the {ext(PPA_CELEB, "PPA announcement")} and the PPA watch page (8 – 10 PM ET).</li>
<li><b>Free channel vs the app:</b> {ext(PBTV, "PickleballTV")}'s free 24/7 channel is on Fubo, Samsung TV Plus, Roku, Fire TV and Plex and carries selected matches. Every court, replays and DVR need the paid app; the {ext(PBTV_IOS, "App Store listing")} lists $5.99 a month or $59.99 a year with a 30-day free trial.</li>
</ul>
<p>Our <a href="../guides/how-to-watch-pro-pickleball.html">how to watch pro pickleball guide</a> has the full week of windows, including the Nations Cup and USA Pickleball Nationals.</p>
<h2>Tickets</h2>
<p><b>Not a live checkout price.</b> {ext(UP_TIX, "United Pickleball's ticket page")}, re-read November 7, 2026, still prints the figures below and says they are Tixr data from <b>October 11, 2026</b>, fees included. The page also says prices vary by day and demand. The ranges in this table are that October 11 snapshot, not a cart total we checked on November 7. Confirm the current price on Tixr before you pay.</p>
<div class="tbl"><table><thead><tr><th>Ticket</th><th>October 11, 2026 Tixr figure</th></tr></thead><tbody>{ow_tix_rows}</tbody></table></div>
<p>A Grounds Pass covers the outer courts, including select pro matches; Courtside, Chair and VIP add reserved seats on Championship Court. Nations Cup tickets (October 30 to November 1) are sold separately; see our <a href="mlp-nations-cup-2026.html">Nations Cup guide</a>.</p>
<h2>Format, prize money and points</h2>
<p>The {ext(PPA_EV, "PPA Tour")} lists Worlds as a <b>PPA Major worth 3,000 ranking points</b> per division title, with a <b>total payout of $1,648,641</b> across five pro divisions, including appearance fees. {ext(UP_PRO, "United Pickleball")} lists single-elimination main draws: 64 players in men's and women's singles, 32 teams in men's and women's doubles, and 32 teams in mixed. The PPA Challenger Showdown runs alongside it from Thursday to Saturday, with eight 2027 PPA Tour contracts on the line.</p>
<h2>Notable entrants and defending champions</h2>
<p>The PPA says every No. 1 seed is entered, and its event page highlights <b>Anna Leigh Waters</b>, <b>Len Yang</b> and <b>Rachel Rohrabacher</b> in the draw. Full seeded draws are on the {ext(UP_PRO, "United Pickleball pro page")}. Defending champions, per the PPA:</p>
<div class="tbl"><table><thead><tr><th>Event</th><th>2025 champion</th></tr></thead><tbody>{ow_champ_rows}</tbody></table></div>
{ow_links}
{ow_faq_html}
{sources([("PPA Tour: Opendoor Pickleball World Championships 2026", PPA_EV, f"dates, points, payout, schedule, entrants, champions, checked {ow_checked}"),
          ("PPA Tour: At the event", PPA_TODAY, f"address, parking, first serve, checked {ow_checked}"),
          ("PPA Tour: Watch", PPA_WATCH, f"PickleballTV and Tennis Channel windows (ET), checked {ow_checked}"),
          ("PPA Tour: TV schedule", PPA_TV, f"Worlds windows (ET), checked {ow_checked}"),
          ("PPA Tour: MUNICIPAL Celebrity Pickleball Showdown", PPA_CELEB, "Nov 5, 7 p.m. CT, Tennis Channel"),
          ("United Pickleball: Pickleball Worlds 2026", UP_HOME, f"Oct 30 to Nov 8 week, checked {ow_checked}"),
          ("United Pickleball: Pro play", UP_PRO, f"draw sizes, CT windows, checked {ow_checked}"),
          ("United Pickleball: Week schedule", UP_SCHED, f"qualifiers Mon Nov 2 to Championship Sunday Nov 8, music, Nations Cup, checked October 31, 2026"),
          ("United Pickleball: Tickets", UP_TIX, "Tixr snapshot dated October 11, 2026, still printed when re-read November 7, 2026; not a live cart price"),
          ("Brookhaven Country Club: contact", BH_CONTACT, "club address 3333 Golfing Green Dr, read November 7, 2026"),
          ("City of Farmers Branch: Pickleball", FB_CITY, "venue address, neighborhood parking"),
          ("PickleballTV", PBTV, "free channel platforms"),
          ("PickleballTV on the App Store", PBTV_IOS, "app price and trial"),
          ("The Kitchen: 2026 Worlds schedule of events", KITCHEN, "daily programming, updated Oct 29, 2026")])}
<p><a href="../tournaments.html">All tournaments</a></p>'''
    page(OW_FN, "Pickleball Worlds 2026: Schedule & TV", ow,
         "Pickleball Worlds 2026 in CT: semifinals Sat Nov 7 (PickleballTV 11 AM–7 PM), Championship Sunday Nov 8 (first serve 10 AM; 4 PM is the broadcast window). Qualifying Mon Nov 2 is on record at 8 AM CT; the PPA page lists 11 AM.",
         fresh={"checked": OW_CHECKED, "days": OW_DAYS, "tix": OW_TIX, "champs": OW_CHAMPS, "faq": ow_faq, "event": ow_event, "weekend_bucket": ("sat" if build_day == _sat else "sun" if build_day == _sun else "after" if build_day > _sun else "before")},
         schema=[ow_event, ow_faq_ld], raw_title=True)
    # MLP Nations Cup page. Every fact below was read on the linked official pages (and the cited preview) on NC_CHECKED.
    # Results are listed only once official MLP / United Pickleball pages post them as final.
    NC_CHECKED = "2026-11-01"
    nc_checked = _dt.date.fromisoformat(NC_CHECKED).strftime("%B %-d, %Y")
    NC_UP = "https://worlds.unitedpickleball.com/nations-cup"
    NC_MLP = "https://www.majorleaguepickleball.co/"
    NC_MLP_ROSTERS = "https://majorleaguepickleball.co/news/groups-rosters-and-captains-announced-for-inaugural-mlp-nations-cup-hosted-at-brookhaven-country-club-oct-30-nov-1/"
    NC_MLP_SCHED = "https://majorleaguepickleball.co/news/match-schedule-for-mlp-nations-cup-released/"
    NC_PPA_WATCH = "https://www.ppatour.com/watch/"
    NC_YAHOO = "https://sports.yahoo.com/articles/inaugural-major-league-nations-cup-124924340.html"
    NC_X_USA = "https://x.com/MajorLeaguePB/status/2115883868964196757"
    NC_X_COSTUME = "https://x.com/MajorLeaguePB/status/2115858704926908872"
    NC_X_TIX = "https://x.com/MajorLeaguePB/status/2115843605742977322"
    NC_X_RAIN = "https://x.com/MajorLeaguePB/status/2116184782254334407"
    NC_TEAMS = [  # MLP roster announcement, September 24, 2026; Asia International swap per MLP / United Pickleball / Yahoo Sports
        ("A", "USA", "Johnny Goldberg", "Tyra Black, Anna Bright, Kate Fahey, Ben Johns, CJ Klinger, Will Howells"),
        ("A", "Canada", "Steve Deakin", "Victoria DiMuzio, Blaine Hovenier, Armaan Jiwa Mawji, Layne Sleeth, Ryan Torresin, Angie Walker"),
        ("A", "Europe - West", "Chris Cantino", "Judit Castillo, Helena Jansen, Will MacKinnon, Theo Platel, Estee Widdershoven, DJ Young"),
        ("A", "Asia Domestic", "Geoffrey Nguyen and Jeff Tsao", "Augie Ge, Milan Rane, Jonathan Truong, Zoey Wang, Jamie Wei, Len Yang"),
        ("B", "Asia International", "Madeleine Lim", "Rika Fujiwara, Lingwei Kong, Jimmy Liong, Tama Shimabukuro, Jack Wong, Macy Ybañez"),
        ("B", "Australia", "Sange Carter", "Sarah Burr, Chris Crouch, Sahra Dennehy, Mitch Hargreaves, Danni-Elle Townsend, George Wall"),
        ("B", "Europe - East", "Caleb Garrard", "Andrei Daescu, Arwid Dahlin, Ivan Jakovljevic, Lina Padegimaite, Tina Pisnik, Daria Walczak"),
        ("B", "Latin America", "Juan Manuel Benitez", "Nico Acevedo, Mari Humberg, Rafa Lenhard, Eric Oncins, Alexa Schull, Charlie Trevino"),
    ]
    # Match order: MLP schedule release (Sep 29). Start times: United Pickleball match list (CT), read NC_CHECKED.
    NC_SCHED = [
        ("Fri Oct 30", "10:00 AM", "Group B", "Australia vs Asia International"),
        ("Fri Oct 30", "11:30 AM", "Group B", "Europe - East vs Latin America"),
        ("Fri Oct 30", "1:00 PM", "Group A", "Europe - West vs Asia Domestic"),
        ("Fri Oct 30", "2:30 PM", "Group A", "Canada vs USA"),
        ("Fri Oct 30", "4:00 PM", "Group B", "Australia vs Europe - East"),
        ("Fri Oct 30", "5:30 PM", "Group A", "Asia Domestic vs Canada"),
        ("Sat Oct 31", "10:00 AM", "Group B", "Latin America vs Asia International"),
        ("Sat Oct 31", "11:30 AM", "Group A", "USA vs Europe - West"),
        ("Sat Oct 31", "1:00 PM", "Group B", "Asia International vs Europe - East"),
        ("Sat Oct 31", "2:30 PM", "Group B", "Latin America vs Australia"),
        ("Sat Oct 31", "4:00 PM", "Group A", "USA vs Asia Domestic"),
        ("Sat Oct 31", "5:30 PM", "Group A", "Europe - West vs Canada"),
        ("Sun Nov 1", "10:00 AM", "Semifinal 1", "Asia Domestic (Group A No. 2) vs Latin America (Group B No. 1)"),
        ("Sun Nov 1", "11:30 AM", "Semifinal 2", "USA (Group A No. 1) vs Europe East (Group B No. 2)"),
        ("Sun Nov 1", "2:00 PM", "Final", "Semifinal winners"),
    ]
    # Results: only matches marked Final on the United Pickleball match list (official MLP results) are listed. Winner listed first; game scores winner-first.
    NC_RESULTS_AS_OF = "5:03 PM"
    NC_X_FINAL = "https://x.com/MajorLeaguePB/status/2117008397656863145"
    NC_X_SF2 = "https://x.com/MajorLeaguePB/status/2116984380857999747"
    NC_RESULTS = [  # (day, group, winner, loser, [(game, winner pts, loser pts), ...], games won-lost)
        ("Fri Oct 30", "Group B", "Australia", "Asia International", [("W", 11, 9), ("M", 12, 14), ("MX1", 11, 3), ("MX2", 11, 7)], "3-1"),
        ("Fri Oct 30", "Group B", "Europe East", "Latin America", [("W", 11, 6), ("M", 11, 7), ("MX1", 11, 8)], "3-0"),
        ("Fri Oct 30", "Group A", "Asia Domestic", "Europe West", [("W", 4, 11), ("M", 11, 9), ("MX1", 11, 1), ("MX2", 11, 9)], "3-1"),
        ("Fri Oct 30", "Group A", "USA", "Canada", [("W", 5, 11), ("M", 11, 4), ("MX1", 11, 0), ("MX2", 11, 1)], "3-1"),
        ("Fri Oct 30", "Group B", "Australia", "Europe East", [("W", 11, 9), ("M", 11, 2), ("MX1", 7, 11), ("MX2", 11, 4)], "3-1"),
        ("Fri Oct 30", "Group A", "Asia Domestic", "Canada", [("W", 12, 10), ("M", 11, 7), ("MX1", 11, 2)], "3-0"),
        ("Sat Oct 31", "Group B", "Latin America", "Asia International", [("W", 11, 8), ("M", 11, 5), ("MX1", 11, 4)], "3-0"),
        ("Sat Oct 31", "Group A", "USA", "Europe West", [("W", 11, 5), ("M", 11, 1), ("MX1", 11, 2)], "3-0"),
        ("Sat Oct 31", "Group B", "Europe East", "Asia International", [("W", 11, 2), ("M", 7, 11), ("MX1", 11, 4), ("MX2", 11, 7)], "3-1"),
        ("Sat Oct 31", "Group B", "Latin America", "Australia", [("W", 12, 10), ("M", 11, 2), ("MX1", 11, 5)], "3-0"),
        ("Sat Oct 31", "Group A", "USA", "Asia Domestic", [("W", 13, 11), ("M", 6, 11), ("MX1", 12, 14), ("MX2", 11, 4), ("DB", 21, 18)], "3-2"),
        ("Sat Oct 31", "Group A", "Europe West", "Canada", [("W", 11, 3), ("M", 2, 11), ("MX1", 12, 10), ("MX2", 11, 6)], "3-1"),
        ("Sun Nov 1", "Semifinal 1", "Latin America", "Asia Domestic", [("W", 11, 3), ("M", 9, 11), ("MX1", 11, 3), ("MX2", 11, 3)], "3-1"),
        ("Sun Nov 1", "Semifinal 2", "USA", "Europe East", [("W", 11, 3), ("M", 11, 6), ("MX1", 12, 14), ("MX2", 11, 7)], "3-1"),
        ("Sun Nov 1", "Final", "USA", "Latin America", [("W", 11, 9), ("M", 11, 1), ("MX1", 11, 6)], "3-0"),
    ]
    # Not final at NC_RESULTS_AS_OF (United Pickleball match list): (start CT, group, match, status)
    NC_PENDING = []  # all 12 group matches, both semifinals and the final marked Final (checked Nov 1, 5:03 PM CT)
    # Standings: United Pickleball "Two pools of four" tables (official MLP results), copied in the order shown, read Oct 31, 8:40 PM CT; unchanged on recheck Nov 1 at NC_RESULTS_AS_OF CT. Pool 1 = Group A, Pool 2 = Group B.
    NC_STAND = {"Pool 1 (Group A)": [("USA", 3, 0, "+6", "+52"), ("Asia Domestic", 2, 1, "+4", "+17"), ("Europe West", 1, 2, "−3", "−26"), ("Canada", 0, 3, "−7", "−43")],
                "Pool 2 (Group B)": [("Latin America", 2, 1, "+3", "+21"), ("Europe East", 2, 1, "+3", "+14"), ("Australia", 2, 1, "+1", "+9"), ("Asia International", 0, 3, "−7", "−44")]}
    NC_TV = [("Fri Oct 30", "Pool play", "10 AM – 7 PM CT", "11 AM – 8 PM ET"),
             ("Sat Oct 31", "Pool play", "10 AM – 7 PM CT", "11 AM – 8 PM ET"),
             ("Sun Nov 1", "Semifinals", "10 AM – 1 PM CT", "11 AM – 2 PM ET"),
             ("Sun Nov 1", "Final", "2 – 3:30 PM CT", "3 – 4:30 PM ET")]
    nc_team_rows = "".join(f'<tr><td>{e(g)}</td><th scope="row">{e(t)}</th><td>{e(c)}</td><td>{e(r)}</td></tr>' for g, t, c, r in NC_TEAMS)
    nc_sched_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(t)}</td><td>{e(s)}</td><td>{"<b>" + e(m) + "</b>" if "USA" in m else e(m)}</td></tr>' for d, t, s, m in NC_SCHED)
    nc_tv_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(ct)}</td><td>{e(et)}</td></tr>' for d, w, ct, et in NC_TV)
    def nc_res_rows(day):
        return "".join(f'<tr><td>{e(g)}</td><th scope="row">{e(w)} def. {e(l)}, {e(gs)}</th><td>{e(", ".join(f"{n} {x}-{y}" for n, x, y in games))}</td></tr>' for d, g, w, l, games, gs in NC_RESULTS if d == day)
    nc_pending_rows = "".join(f'<li>{e(t)} CT ({e(g)}): {"<b>" + e(m) + "</b>" if "USA" in m else e(m)}, {e(st)} when we checked</li>' for t, g, m, st in NC_PENDING)
    nc_stand_html = "".join(f'<h3>{e(p)}</h3><div class="tbl"><table><thead><tr><th>Team</th><th>W</th><th>L</th><th>Game diff.</th><th>Point diff.</th></tr></thead><tbody>' + "".join(f'<tr><th scope="row">{e(t)}</th><td>{w}</td><td>{l}</td><td>{e(gd)}</td><td>{e(pd)}</td></tr>' for t, w, l, gd, pd in rows) + "</tbody></table></div>" for p, rows in NC_STAND.items())
    nc_faq = [
        ("When is the MLP Nations Cup 2026?",
         "Friday, October 30 to Sunday, November 1, 2026, at Brookhaven Country Club, 3333 Golfing Green Dr, Farmers Branch, Texas, the address on the club's contact page. United Pickleball's Nations Cup page prints 3334 Golfing Green Drive. Play started at 10 a.m. CT each day, and the final was Sunday, November 1 at 2 p.m. CT."),
        ("How can I watch the MLP Nations Cup 2026?",
         "MLP says all matches are available on PickleballTV and the PickleballTV app, and United Pickleball says Championship Court matches are livestreamed on PickleballTV. Coverage runs 10 a.m. to 7 p.m. CT on Friday and Saturday, with semifinals 10 a.m. to 1 p.m. CT and the final 2 to 3:30 p.m. CT on Sunday."),
        ("Who is on Team USA at the MLP Nations Cup?",
         "MLP lists Tyra Black, Anna Bright, Kate Fahey, Ben Johns, CJ Klinger and Will Howells, with captain Johnny Goldberg. Anna Leigh Waters is not on the roster."),
        ("When does Team USA play?",
         "Team USA won Group A at 3-0, beating Canada 3-1, Europe - West 3-0 and Asia Domestic 3-2 in a DreamBreaker. On Sunday, November 1 it beat Europe East 3-1 in the semifinal and Latin America 3-0 in the final. Champion: USA."),
        ("How does the MLP Nations Cup format work?",
         "Eight teams of six pros, 48 players in all, play MLP's coed team format in two groups of four. Each team plays the other three in its group on Friday and Saturday. The top two in each group reach Sunday's semifinals, where each group winner plays the other group's runner-up, and the winners meet in the final."),
        ("Are Nations Cup tickets the same as PPA Worlds tickets?",
         "No. United Pickleball says Nations Cup tickets are sold separately from Worlds week, on Tixr. MLP said on October 29 that last-minute tickets start at $25. Doors open one hour before the first matches."),
        ("Who won the MLP Nations Cup 2026?",
         "Team USA. USA beat Latin America 3-0 in the final on Sunday, November 1, 2026 (11-9, 11-1, 11-6), per the official MLP results on United Pickleball. In the semifinals, Latin America beat Asia Domestic 3-1 and USA beat Europe East 3-1."),
        ("Who was in the Nations Cup semifinals?",
         "USA, Asia Domestic, Latin America and Europe East. Pool play finished Saturday night: the official final tables show USA (3-0) and Asia Domestic (2-1) as the top two in Pool 1 (Group A), and Latin America and Europe East (both 2-1, ahead of Australia, also 2-1, on game and point differential) as the top two in Pool 2 (Group B). Semifinal 1 was Asia Domestic vs Latin America on Sunday, November 1 at 10 a.m. CT (Latin America won 3-1). Semifinal 2 was USA vs Europe East at 11:30 a.m. CT (USA won 3-1). The final was at 2 p.m. CT (USA beat Latin America 3-0), all on PickleballTV."),
        ("Where can I see Nations Cup results?",
         "United Pickleball's Nations Cup page posts the match list and pool standings from the official MLP results, and live scores and standings are on majorleaguepickleball.co during the event. Our standings and results section is dated with the time we last read them."),
    ]
    nc_faq_html, nc_faq_ld = faq(nc_faq)
    nc_place = {"@type": "Place", "name": "Brookhaven Country Club",
                "address": {"@type": "PostalAddress", "streetAddress": "3333 Golfing Green Dr", "addressLocality": "Farmers Branch",
                            "addressRegion": "TX", "postalCode": "75234", "addressCountry": "US"}}
    nc_event = {"@type": "SportsEvent", "name": "MLP Nations Cup 2026", "startDate": "2026-10-30T10:00:00-05:00", "endDate": "2026-11-01",
                "description": "The inaugural MLP Nations Cup, October 30 to November 1, 2026, at Brookhaven Country Club, 3333 Golfing Green Dr, Farmers Branch, Texas. Eight regional pro teams played Major League Pickleball's coed format. Team USA won the final, beating Latin America 3-0 on November 1. endDate is the last published day, with no clock time for the final ball.",
                "eventStatus": "https://schema.org/EventScheduled", "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
                "sport": "Pickleball", "url": NC_UP, "location": nc_place,
                "organizer": {"@type": "SportsOrganization", "name": "Major League Pickleball", "url": NC_MLP},
                "competitor": [{"@type": "SportsTeam", "name": f"Team {t}"} for _, t, _, _ in NC_TEAMS],
                "offers": {"@type": "Offer", "url": NC_UP}}
    nations = f'''<h1>MLP Nations Cup 2026: standings, results, schedule and how to watch</h1>
<p class="meta">Facts checked {nc_checked} against MLP's official roster and schedule announcements, the United Pickleball Nations Cup page and the PPA Tour watch page. All times Central (CT) unless noted. Times and rosters can change, so confirm on the official pages.</p>
<h2>The basics</h2>
<p>The inaugural <b>MLP Nations Cup</b> was <b>Friday, October 30 to Sunday, November 1, 2026</b> at <b>Brookhaven Country Club</b>, 3333 Golfing Green Dr, <b>Farmers Branch, Texas</b>. That is the address on the {ext(BH_CONTACT, "club's contact page")} (read November 7, 2026). {ext(NC_UP, "United Pickleball's Nations Cup page")} prints 3334 Golfing Green Drive; this page uses the club's number. United Pickleball called the event the official kickoff to the Opendoor Pickleball World Championships. Eight regional teams of six pros, <b>48 players</b> in all, played Major League Pickleball's coed team format. <b>Team USA won</b>, beating Latin America 3-0 in the final on Sunday, November 1 at 2 PM CT.</p>
<h2>MLP Nations Cup standings and results</h2>
<p class="meta">Final results. Standings and results are from the official MLP results on the {ext(NC_UP, "United Pickleball Nations Cup page")}; only matches marked Final are listed. For anything newer, see live scores on {ext(NC_MLP, "majorleaguepickleball.co")}.</p>
<p>Pool play is complete: all 12 group matches are marked Final. The top two in each pool reached Sunday's semifinals: <b>USA</b> and <b>Asia Domestic</b> from Pool 1, <b>Latin America</b> and <b>Europe East</b> from Pool 2. Standings are copied in the order the official table shows them; Pool 2's three 2-1 teams are separated by game and point differential, which knocked out Australia. USA then won the tournament.</p>
{nc_stand_html}
<p>Game key: W women's doubles, M men's doubles, MX mixed doubles, DB DreamBreaker. Game scores are listed winner first, from the official match list.</p>
<h3>Nations Cup pickleball results: Championship Sunday (November 1)</h3>
<div class="tbl"><table><thead><tr><th>Round</th><th>Result</th><th>Game scores</th></tr></thead><tbody>{nc_res_rows("Sun Nov 1")}</tbody></table></div>
<p><b>Team USA won the first MLP Nations Cup</b>, beating Latin America 3-0 in the final (11-9, 11-1, 11-6), per the official match list and {ext(NC_X_FINAL, "MLP")}.</p>
<h3>Nations Cup pickleball results: day 2 (Saturday, October 31)</h3>
<div class="tbl"><table><thead><tr><th>Group</th><th>Result</th><th>Game scores</th></tr></thead><tbody>{nc_res_rows("Sat Oct 31")}</tbody></table></div>
<p>Team USA beat Asia Domestic 3-2 in a DreamBreaker (21-18) to finish 3-0 and top Pool 1.</p>
<h3>Nations Cup pickleball results: day 1 (Friday, October 30)</h3>
<div class="tbl"><table><thead><tr><th>Group</th><th>Result</th><th>Game scores</th></tr></thead><tbody>{nc_res_rows("Fri Oct 30")}</tbody></table></div>
<p>Rain moved Friday's opener indoors with a {ext(NC_X_RAIN, "10:30 AM CT target start")}.</p>
<h2>Sunday, November 1: Nations Cup semifinals and final</h2>
<ul><li><b>Semifinal 1</b> (10:00 AM CT): Latin America def. Asia Domestic 3-1 (W 11-3, M 9-11, MX1 11-3, MX2 11-3)</li><li><b>Semifinal 2</b> (11:30 AM CT): <b>USA def. Europe East 3-1</b> (W 11-3, M 11-6, MX1 12-14, MX2 11-7), per the official match list and {ext(NC_X_SF2, "MLP")}</li><li><b>Final</b> (2:00 PM CT): <b>USA def. Latin America 3-0</b> (W 11-9, M 11-1, MX1 11-6). <b>Champion: USA.</b></li></ul>
<p>All three Sunday matches are marked Final on the {ext(NC_UP, "United Pickleball match list")} (official MLP results).</p>
<h2>Schedule</h2>
<p>Every match is on Championship Court. Match order is from {ext(NC_MLP_SCHED, "MLP's schedule release")}, and start times are from the {ext(NC_UP, "United Pickleball match list")}. Team USA matches are in bold.</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>Start (CT)</th><th>Round</th><th>Match</th></tr></thead><tbody>{nc_sched_rows}</tbody></table></div>
<h2>How to watch Nations Cup pickleball</h2>
<p>MLP says <b>all matches are available on PickleballTV and the PickleballTV app</b>. United Pickleball says Championship Court matches are livestreamed on PickleballTV. These are the coverage windows from {ext(NC_UP, "United Pickleball")} (CT) and the {ext(NC_PPA_WATCH, "PPA Tour watch page")} (ET):</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>Coverage</th><th>Central</th><th>Eastern</th></tr></thead><tbody>{nc_tv_rows}</tbody></table></div>
<p>Neither page lists any other TV broadcast, such as Tennis Channel, for the Nations Cup. For PickleballTV free vs paid and the rest of Worlds week, see <a href="../guides/how-to-watch-pro-pickleball.html">how to watch pro pickleball</a>.</p>
<h2>Team USA</h2>
<p>Team USA plays in Group A, with captain <b>Johnny Goldberg</b>. MLP's roster: <b>Ben Johns, CJ Klinger, Will Howells, Tyra Black, Anna Bright and Kate Fahey</b>. {ext(NC_X_USA, "MLP notes")} that St. Louis Shock teammates Bright and Fahey reunite on the USA squad. {ext(NC_YAHOO, "Yahoo Sports")} points out that <b>Anna Leigh Waters</b> is not on the team.</p>
<ul><li>Fri Oct 30, 2:30 PM CT: USA def. Canada 3-1</li><li>Sat Oct 31, 11:30 AM CT: USA def. Europe - West 3-0</li><li>Sat Oct 31, 4:00 PM CT: USA def. Asia Domestic 3-2 (DreamBreaker 21-18)</li><li>Sun Nov 1, 11:30 AM CT: USA def. Europe East 3-1 (semifinal)</li><li>Sun Nov 1, 2:00 PM CT: USA def. Latin America 3-0 (final), Nations Cup champions</li></ul>
<h2>Format</h2>
<p>The eight teams were split into two groups of four. Each team played the other three in its group across Friday and Saturday. The top two in each group advanced to Sunday's single-elimination bracket. Semifinal 1 was the Group A runner-up against the Group B winner, and Semifinal 2 was the Group A winner against the Group B runner-up. The two winners met in the final. USA won.</p>
<h2>Teams and rosters</h2>
<p>Groups, captains and players are from {ext(NC_MLP_ROSTERS, "MLP's September 24 roster announcement")}. Tama Shimabukuro has since replaced Hien Truong on Asia International, per the United Pickleball team list and Yahoo Sports. United Pickleball's team list (read {nc_checked}) also omits Ryan Torresin for Canada and Sarah Burr and Mitch Hargreaves for Australia. MLP hasn't announced a change, so check the official pages before match day.</p>
<div class="tbl"><table><thead><tr><th>Group</th><th>Team</th><th>Captain</th><th>Players</th></tr></thead><tbody>{nc_team_rows}</tbody></table></div>
<p>Want to see what the pros play? The <a href="../pro-paddles.html">pro paddles page</a> lists each player's paddle from their official PPA profile.</p>
<h2>Going in person</h2>
<p>Nations Cup tickets are sold separately from Worlds week, on Tixr. {ext(NC_X_TIX, "MLP said on October 29")} that last-minute tickets start at $25. United Pickleball lists a Courtside Pass (bleacher seating, first come, first served) and a VIP Pass. Doors open one hour before the first matches. Outside food and drink aren't allowed, and filming matches isn't permitted without MLP's written approval. On Saturday, October 31, {ext(NC_X_COSTUME, "MLP is holding a Halloween costume contest")} for fans, with prizes for the top 3 from DoorDash and VIP ticket upgrades for 10 more fans.</p>
<h2>Next up: PPA Worlds, November 2 to 8</h2>
<p>The PPA Tour's Opendoor Pickleball World Championships follow at the same venue from <b>November 2 to 8</b>, per United Pickleball. See our <a href="opendoor-pickleball-world-championships.html#this-weekend">Pickleball World Championships 2026 page</a> for the published weekend windows (semifinals November 7, Championship Sunday November 8; the lead there follows the build date), plus parking and the day-by-day schedule in CT. PPA pro qualifying was <b>Monday, November 2</b>. The first-serve time on the record is 8 AM CT from an earlier United Pickleball reading and the PPA's Oct 28 X post; the PPA event page still listed 11 AM on November 7, 2026.</p>
<p class="watch"><a href="opendoor-pickleball-world-championships.html#how-to-watch">Next up: Pickleball Worlds 2026 — how to watch →</a></p>
<h2>Gear before you go</h2>
{money_links()}
{nc_faq_html}
{sources([("Major League Pickleball: Groups, rosters and captains announced", NC_MLP_ROSTERS, "groups, captains, rosters, format; September 24, 2026"),
          ("Major League Pickleball: Match schedule released", NC_MLP_SCHED, "match order, Sunday times, PickleballTV; September 29, 2026"),
          ("United Pickleball: MLP Nations Cup", NC_UP, f"venue, match times, coverage windows, team list, tickets; read {nc_checked}"),
          ("PPA Tour: Watch pro pickleball", NC_PPA_WATCH, f"PickleballTV windows in ET; read {nc_checked}"),
          ("Yahoo Sports (Forbes): Inaugural Major League Nations Cup kicks off Worlds week", NC_YAHOO, "rosters, roster changes, Anna Leigh Waters not playing; by Todd Boss, October 28, 2026"),
          ("@MajorLeaguePB on X: Bright and Fahey reunite for USA", NC_X_USA, "October 29, 2026"),
          ("@MajorLeaguePB on X: tickets from $25", NC_X_TIX, "October 29, 2026"),
          ("@MajorLeaguePB on X: Halloween costume contest", NC_X_COSTUME, "October 29, 2026"),
          ("@MajorLeaguePB on X: rain moves first match indoors", NC_X_RAIN, "October 30, 2026"),
          ("United Pickleball: Nations Cup match list and pool standings (official MLP results)", NC_UP, f"pool standings, semifinal and final results; read November 1, 2026, {NC_RESULTS_AS_OF} CT"),
          ("@MajorLeaguePB on X: USA beats Europe East 3-1 to reach the final", NC_X_SF2, "November 1, 2026"),
          ("@MajorLeaguePB on X: USA are the 2026 Nations Cup champions", NC_X_FINAL, "November 1, 2026"),
          ("Major League Pickleball", NC_MLP, "live scores and standings")])}
<p><a href="../tournaments.html">All tournaments</a> · <a href="opendoor-pickleball-world-championships.html">PPA Worlds 2026</a> · <a href="../guides/how-to-watch-pro-pickleball.html">How to watch pro pickleball</a></p>'''
    page("events/mlp-nations-cup-2026.html", "MLP Nations Cup 2026 Standings & Results", nations,
         "MLP Nations Cup 2026 final results: USA beat Latin America 3-0 to win the first Nations Cup. Semifinal scores, final pool standings and every group result.",
         fresh={"checked": NC_CHECKED, "teams": NC_TEAMS, "sched": NC_SCHED, "tv": NC_TV, "results": NC_RESULTS, "pending": NC_PENDING, "stand": NC_STAND, "faq": nc_faq, "address": "3333 Golfing Green Dr"},
         schema=[nc_event, nc_faq_ld], raw_title=True)
    # USA Pickleball Nationals page. Every fact below was read on the official Nationals pages on UN_CHECKED.
    UN_CHECKED = "2026-10-27"
    un_checked = _dt.date.fromisoformat(UN_CHECKED).strftime("%B %-d, %Y")
    UN_HOME = "https://usapickleballnationals.com/"
    UN_TIX = "https://usapickleballnationals.com/tickets/"
    UN_SCHED = "https://usapickleballnationals.com/schedule/"
    UN_LIVE = "https://usapickleballnationals.com/livestream/"
    UN_FAQ = "https://usapickleballnationals.com/faqs/"
    UN_NEWS = "https://usapickleball.org/usap-news/nationals/usa-pickleball-national-championships-return-to-barnes-tennis-center-in-2026/"
    UN_DAYS = [
        ("Sat Oct 31", "Junior boys' and girls' doubles, APP Selkirk U.S. Collegiate Series Championships, wheelchair coed doubles, mixed doubles 65-85+"),
        ("Sun Nov 1", "Junior mixed doubles and singles, Collegiate Series Championships, wheelchair coed singles, men's doubles 65-80+, women's singles 65-80+"),
        ("Mon Nov 2", "Wheelchair hybrid doubles, men's singles 65-80+, women's doubles 65-80+"),
        ("Tue Nov 3", "Mixed doubles 50-64; Concert on the Court, 4:30 to 7:30 PM (separate ticket)"),
        ("Wed Nov 4", "Men's doubles 50-64, women's singles 50-64; pro mixed doubles, men's doubles and men's singles round of 32"),
        ("Thu Nov 5", "Men's singles 50-64, women's doubles 50-64; pro round of 16 in all five pro events"),
        ("Fri Nov 6", "Mixed doubles 19-49"),
        ("Sat Nov 7", "Women's singles 19-49, men's doubles 19-49; Champion and Masters pro doubles; pro men's doubles and men's singles semifinals"),
        ("Sun Nov 8", "Women's doubles 19-49, men's singles 19-49; Masters pro singles; gold and bronze medal matches in all five pro events"),
    ]
    UN_TIX_ROWS = [
        ("General Admission", "Free", "Every day, Oct 31 to Nov 8. Open Championship Court seating through Nov 3, then bleachers only from Nov 4."),
        ("Championship Court presented by QVC", "$20 Wednesday, $49 Thursday to Sunday", "Reserved Championship Court seating, Nov 4 to Nov 8"),
        ("VIP", "$139", "Reserved VIP seating on Championship Court, VIP Lounge, lite bites, four drink tickets"),
        ("Concert on the Court (Tue Nov 3)", "$10 GA, $60 VIP Experience", "Event entry only, not full-day Nationals admission"),
        ("On-site parking", "$50 per day", "Limited, no reentry, no RVs"),
        ("Off-site shuttle", "Free parking, $10 per group per day", "Lot just east of SeaWorld; shuttles about every 15 minutes from 6 AM"),
    ]
    un_day_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td></tr>' for d, w in UN_DAYS)
    un_tix_rows = "".join(f'<tr><th scope="row">{e(t)}</th><td>{e(p)}</td><td>{e(n)}</td></tr>' for t, p, n in UN_TIX_ROWS)
    un_faq = [
        ("When and where are the 2026 USA Pickleball National Championships?",
         "October 31 to November 8, 2026, at Barnes Tennis Center, 4490 West Point Loma Blvd., San Diego, California. USA Pickleball calls it the 2026 Oceanview USA Pickleball National Championships."),
        ("How can I watch USA Pickleball Nationals 2026 online?",
         "The official Nationals site says every match is livestreamed and recorded by VS Sports, so you can watch live or rewatch match recordings."),
        ("Is it free to watch Nationals in person?",
         "Yes. General Admission is free every day, but every non-player needs a single-day ticket for each day. Reserved Championship Court seats cost $20 on Wednesday and $49 Thursday to Sunday, and VIP is $139."),
        ("When are the pro medal matches at Nationals 2026?",
         "The official schedule lists pro men's doubles and men's singles semifinals on Saturday, November 7, and gold and bronze medal matches in pro mixed, men's and women's doubles and singles on Sunday, November 8."),
        ("Where do I park for Nationals?",
         "On-site parking at Barnes Tennis Center is $50 per day with no reentry. Or park free at the off-site lot just east of SeaWorld and ride the shuttle for $10 per group per day. All point-of-sale locations at the event are cashless."),
    ]
    un_faq_html, un_faq_ld = faq(un_faq)
    un_event = {"@type": "SportsEvent", "name": "2026 Oceanview USA Pickleball National Championships",
                "startDate": "2026-10-31", "endDate": "2026-11-08", "url": UN_HOME,
                "eventAttendanceMode": "https://schema.org/MixedEventAttendanceMode", "eventStatus": "https://schema.org/EventScheduled",
                "organizer": {"@type": "Organization", "name": "USA Pickleball", "url": "https://usapickleball.org/"},
                "location": {"@type": "Place", "name": "Barnes Tennis Center",
                             "address": {"@type": "PostalAddress", "streetAddress": "4490 W Point Loma Blvd", "addressLocality": "San Diego", "addressRegion": "CA", "postalCode": "92107", "addressCountry": "US"}},
                "offers": {"@type": "Offer", "url": UN_TIX, "price": "0", "priceCurrency": "USD", "name": "General Admission"}}
    nationals = f'''<h1>USA Pickleball Nationals 2026: schedule, tickets and how to watch</h1>
<p class="meta">From the official USA Pickleball Nationals site. Checked {un_checked}. Match times, courts and brackets come out closer to play, so confirm on the official pages.</p>
<h2>The basics</h2>
<p>The <b>2026 Oceanview USA Pickleball National Championships</b> run <b>Saturday, October 31 to Sunday, November 8</b> at <b>Barnes Tennis Center in San Diego</b>, the second straight year there, per {ext(UN_NEWS, "USA Pickleball")}. Play is spread across 54 courts, with junior, collegiate, amateur, wheelchair and pro divisions. Amateur players qualify through Golden Ticket tournaments and USA Pickleball's Tiered Point System.</p>
<h2>How to watch online</h2>
<p>The {ext(UN_LIVE, "official livestream page")} says every match is livestreamed and recorded by <b>VS Sports</b>, so you can follow players live or catch up on recordings later. Individual match times are posted through Pickleball Den closer to play, per the {ext(UN_FAQ, "Nationals FAQ")}.</p>
<p>Same week, different event: the Opendoor Pickleball World Championships run November 2 to 8 in Farmers Branch, Texas. See our <a href="opendoor-pickleball-world-championships.html">PPA Worlds 2026 guide</a> and <a href="mlp-nations-cup-2026.html">MLP Nations Cup 2026 how to watch</a>.</p>
<h2>Day-by-day schedule</h2>
<p>Divisions by day from the {ext(UN_SCHED, "official schedule")}:</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>Who plays</th></tr></thead><tbody>{un_day_rows}</tbody></table></div>
<h2>Tickets and parking</h2>
<p>Prices from the {ext(UN_TIX, "official tickets page")}. Every non-player needs a single-day ticket for each day, children 5 and under get in free, all sales are final, and no outside food or drink is allowed except water. Players get venue access on the days they compete.</p>
<div class="tbl"><table><thead><tr><th>Ticket</th><th>Price</th><th>What you get</th></tr></thead><tbody>{un_tix_rows}</tbody></table></div>
<p>The event is cashless, including parking, the box office and concessions. Groups of 30 or more and military visitors can email tickets@usapickleball.org about discounts.</p>
<h2>Gear before you go</h2>
{money_links()}
{un_faq_html}
{sources([("USA Pickleball Nationals", UN_HOME, f"dates, venue, qualifying, checked {un_checked}"),
          ("Nationals schedule", UN_SCHED, f"divisions by day, checked {un_checked}"),
          ("Nationals tickets", UN_TIX, f"ticket prices, parking, shuttle, checked {un_checked}"),
          ("Nationals livestream", UN_LIVE, "VS Sports livestream and recordings"),
          ("Nationals FAQs", UN_FAQ, "courts, match times, cashless venue"),
          ("USA Pickleball: Nationals return to Barnes Tennis Center in 2026", UN_NEWS, "venue announcement")])}
<p><a href="../tournaments.html">All tournaments</a> · <a href="opendoor-pickleball-world-championships.html">PPA Worlds 2026</a> · <a href="mlp-nations-cup-2026.html">MLP Nations Cup 2026</a></p>'''
    page("events/usa-pickleball-nationals-2026.html", "USA Pickleball Nationals 2026: schedule, tickets and how to watch", nationals,
         "USA Pickleball Nationals 2026 runs Oct 31 to Nov 8 at Barnes Tennis Center, San Diego: VS Sports livestream, day-by-day schedule, pro medal matches, free GA tickets and parking.",
         fresh={"checked": UN_CHECKED, "days": UN_DAYS, "tix": UN_TIX_ROWS, "faq": un_faq},
         schema=[un_event, un_faq_ld])
