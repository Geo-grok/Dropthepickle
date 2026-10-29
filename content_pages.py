"""Beginner guides and the Ryan Morneau spotlight.

Prices, specs, and video IDs come from data files or his public YouTube feed.
Rule statements follow the USA Pickleball rulebook. Nothing here is a playtest ranking.
"""
from paddle_pages import slug, weights, cores, money

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
    ("guides/how-to-watch-pro-pickleball.html", "How to watch pro pickleball"),
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
        links += '<li><a href="../price-index.html">Paddle price index</a></li><li><a href="../tournaments.html">Pro events</a></li><li><a href="../events/ppa-worlds-2026.html">PPA Worlds 2026 guide</a></li><li><a href="../events/mlp-nations-cup-2026.html">MLP Nations Cup 2026: how to watch</a></li><li><a href="../events/usa-pickleball-nationals-2026.html">USA Pickleball Nationals 2026: schedule and how to watch</a></li><li><a href="../creators/ryan-morneau.html">Ryan Morneau spotlight</a></li>'
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
<p>Open the <a href="../paddles.html">paddle database</a> or <a href="../compare.html">compare two paddles</a> from the same brand. Each paddle page repeats the maker's core, shape, weight, and latest checked price, and links to the maker's product page.</p>
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
    u100_faq = [
        ("Which pickleball paddles are under $100?",
         under_lead + (f" They are: {names}." if ok_under else " The cheapest verified prices in our file are $100 or more, and they are shown in a separate table.")),
        ("Where do these prices come from?",
         f"Each price is the maker's own price from our latest check of the maker page, saved with the date it was checked. The latest check date on this page is {last_check}. We do not invent street or coupon prices."),
        ("Why is a $100.00 paddle not on the list?",
         "This list only includes paddles priced under $100. A paddle at exactly $100.00 does not meet that rule, so it is shown in the $100 to $150 table instead."),
        ("Is this a ranking of the best paddles?",
         "No. Here, best means the paddle passed the price rule. We do not playtest or score power, control, or spin."),
    ]
    faq_html, faq_ld = faq(u100_faq)
    under = f'''<h1>Best pickleball paddles under $100</h1>
<p class="meta">Built from our own paddle file and dated maker price checks. Not a playtest and not a ranking.</p>
{__import__("own_codes").volair_link(__import__("own_codes").own_codes(__import__("json").load(open(__import__("pathlib").Path(__file__).with_name("config.json")))), "Shopping Volair?")}
<p>{under_lead} The rule is strict: the paddle needs a successful, in-stock price check on the maker's own page, in US dollars, and the current price must be below $100. Every price on this page shows the date it was checked.</p>
<h2>Under $100 (verified)</h2>
{under_table}
<h2>Closest verified prices, $100 to $150</h2>
<p>These paddles cost $100 or more, so they are <b>not</b> under-$100 picks. They are here so you can see where the cheapest verified prices actually sit.{e(at100_txt)}</p>
{near_table}
<h2>What we left out</h2>
<ul>{"".join(f"<li>{e(x)}</li>" for x in excl) or "<li>Nothing else.</li>"}</ul>
<p>Our database is a short list of major-brand models with specs copied from the maker. It is not a catalog of every budget paddle on the market. See every recorded price on the <a href="../price-index.html">price index</a>, or use the <a href="../best-paddles-under-100.html">under-$100 spec filter</a>. New to buying? Start with <a href="how-to-choose-a-paddle.html">how to choose a paddle</a>.</p>
{money_links()}
{faq_html}
{sources([(f"{p['brand']} {p['model']} (maker product page)", p["source_url"], f"price checked {fmt(ph(p)['checked'])}") for p in ok_under + ok_near])}
{more("guides/best-paddles-under-100.html")}'''
    page("guides/best-paddles-under-100.html", "Best pickleball paddles under $100 (dated price checks)", under,
         "Pickleball paddles with a verified maker price under $100, with the date of each price check. No invented prices and no playtest scores.",
         fresh={"under": [(p["brand"], p["model"], ph(p)["current"], ph(p)["checked"]) for p in ok_under],
                "near": [(p["brand"], p["model"], ph(p)["current"], ph(p)["checked"]) for p in ok_near], "faq": u100_faq},
         schema=[faq_ld])

    # ----- rules -----
    rules_faq = [
        ("Who can score a point?",
         "In standard scoring, a point is scored by serving the ball and winning the rally. If the receiving side wins the rally, it does not get a point. Rally scoring, where either side can score, is a separate option in the rulebook."),
        ("What is the kitchen?",
         "The non-volley zone, called the kitchen, is the 7-foot area on each side of the net. You may not volley the ball while you, or anything you are wearing or carrying, are touching that zone, including its lines. Your momentum after a volley counts too."),
        ("What happens if the serve clips the net?",
         "Under the USA Pickleball rulebook, the serve must clear the kitchen and land in the correct service court, with or without touching the net. A serve that lands in the kitchen is a fault. A pro tour can publish its own deviations, so check that event's sheet before you play it."),
    ]
    faq_html, faq_ld = faq(rules_faq)
    rules = f'''<h1>Pickleball rules for beginners</h1>
<p class="meta">A short reading of the USA Pickleball rulebook, in our words. The rulebook wins if we ever disagree.</p>
<p>The official text is the <a href="{RULES}" target="_blank" rel="noopener">USA Pickleball Official Rulebook</a> (PDF). The <a href="{RULES_SUM}" target="_blank" rel="noopener">basic rules summary</a> is the short version of the same organization. This page is the handful of rules that decide a rec game.</p>
<h2>The court and the net</h2>
<p>A standard court is 20 feet wide and 44 feet long for singles and doubles. The net is 36 inches high at the sidelines and 34 inches high at the center. Each end has a non-volley zone 7 feet deep. All lines that bound that zone are part of the zone.</p>
<h2>The serve</h2>
<p>You serve diagonally into the opposite service court. The ball has to clear the kitchen and land in the correct box. On a volley serve, the paddle has to be moving upward, the paddle head must not be above your wrist, and the ball must not be above your waist when you hit it. A drop serve is the other legal motion: you drop the ball and hit it after it bounces, without propelling the ball on the way down. In singles, you start on the right when your score is even, and on the left when it is odd.</p>
<h2>Two bounces, then anything</h2>
<p>The receiver has to let the serve bounce. The serving side then has to let that return bounce. After those two bounces, either side may volley or play a groundstroke. Hitting the ball before the required bounce is a fault. Letting the ball bounce twice on your side is a fault.</p>
<h2>The kitchen</h2>
<p>You can stand in the kitchen. You cannot hit a volley while touching it. If you volley from behind the line and your momentum carries you, your paddle, or your hat into the zone, that is still a fault, even if the ball is already dead. A ball that lands on a line is in, except a serve that lands on the kitchen line, which is short. The <a href="how-to-dink.html">dink guide</a> is the soft shot people hit into this zone once the two bounces are done.</p>
<h2>Scoring</h2>
<p>Standard scoring gives a point only to the serving side, and only if that side wins the rally. A typical game in the rulebook's introduction is the first to 11, with a lead of at least 2. Tournament sections also list games to 15 or 21, still win by two. Call two numbers in singles: server's score, then receiver's score. The game starts at zero-zero. Call three numbers in doubles: serving team's score, receiving team's score, then the server number. A doubles game starts at zero-zero-two, because the first server of the game is treated as the second server. When in doubt, ask before the serve. The rulebook says a player may ask who the correct server or receiver is before the ball is hit.</p>
<p>Ready to look at gear after the rules make sense? <a href="how-to-choose-a-paddle.html">Choose a paddle</a> from the specs we have, or see <a href="../tournaments.html">which pro events are on the calendar</a>.</p>
{faq_html}
{more("guides/pickleball-rules-for-beginners.html")}'''
    page("guides/pickleball-rules-for-beginners.html", "Pickleball rules for beginners", rules,
         "Beginner pickleball rules from the USA Pickleball rulebook: court, serve, two-bounce rule, kitchen, and scoring. Not a substitute for the official book.",
         fresh={"source": RULES, "faq": rules_faq},
         schema=[faq_ld])

    # ----- dink -----
    vid, vtitle, vdate = DINK_VIDEO
    dink_faq = [
        ("What is a dink?",
         "A dink is a soft shot that drops into the opponent's non-volley zone. It is not a winner. It keeps the rally going until someone gives you a ball you can attack."),
        ("Can I step into the kitchen to dink?",
         "Yes, if the ball bounces first. The kitchen fault is for a volley, not for standing there. If you swing before the bounce, or your momentum from a volley carries you in, it is a fault."),
        ("Where should a beginner aim a dink?",
         "Crosscourt. The kitchen is 20 feet wide and 7 feet deep, so the diagonal gives you a longer landing area than a straight-ahead dink."),
    ]
    faq_html, faq_ld = faq(dink_faq)
    dink = f'''<h1>How to dink</h1>
<p class="meta">The soft shot into the kitchen, for players who already know the two-bounce rule. Not a lesson from a certified coach and not a claim about what wins matches.</p>
<p>After the serve and the return have bounced, most intermediate points are decided at the kitchen. A dink is the unhurried ball that lands in the opponent's kitchen so they cannot attack it. The <a href="pickleball-rules-for-beginners.html">rules guide</a> covers why you cannot volley that ball if you are touching the zone.</p>
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
<h2>The paddle is the smaller part</h2>
<p>A published light weight is easier to reset in a fast exchange. In our file the lightest listed number is {light[0]:.1f} oz, on the {alink(light[2])}. That is a spec, not a promise that the paddle dinks better. Read <a href="paddle-weight-and-core.html">weight and core</a> before you buy a new face to fix a swing.</p>
{faq_html}
{more("guides/how-to-dink.html")}'''
    page("guides/how-to-dink.html", "How to dink", dink,
         "How to dink in pickleball: a soft kitchen shot, the non-volley fault to avoid, and one real clip from Ryan Morneau.",
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
<p>If you mishit on the sides, look at a wider shape before you look at a heavier weight. If the ball feels too lively, look at a thicker published core before you add tape. Then open <a href="how-to-choose-a-paddle.html">how to choose a paddle</a> and the <a href="../compare.html">comparison pages</a>, which put two spec sheets side by side.</p>
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
<p>To make a paddle last longer, Selkirk advises keeping it out of hot cars and off wet courts. Before you buy a new one, read <a href="paddle-weight-and-core.html">paddle weight and core</a>, then compare <a href="best-paddles-under-100.html">dated prices under $100</a>.</p>
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
<p class="meta">One-page summary of the 2026 USA Pickleball Official Rulebook, in our words, with the confirmed 2026 changes. The rulebook wins if we ever disagree.</p>
<p>Source: the <a href="{RULES}" target="_blank" rel="noopener">2026 USA Pickleball Official Rulebook</a> (PDF) and the <a href="{RULES_CHANGES}" target="_blank" rel="noopener">2026 Rulebook Change Document</a> (PDF, published December 17, 2025). The 2026 book was renumbered, so rule numbers below are the 2026 numbers.</p>
<h2>The basics</h2>
<ul>
<li><b>Court:</b> 20 by 44 feet for singles and doubles, with a non-volley zone (the kitchen) on each side of the net.</li>
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
<p>Once the rules click, see <a href="how-to-dink.html">how to dink</a> and <a href="how-to-read-dupr-ratings.html">how to read DUPR ratings</a>.</p>
{money_links()}
{faq_html}
{sources([("USA Pickleball 2026 Official Rulebook (PDF)", RULES, ""),
          ("USA Pickleball 2026 Rulebook Change Document (PDF)", RULES_CHANGES, "published December 17, 2025"),
          ("USA Pickleball rule changes, all entries", RULES_CHANGES_VIEW, ""),
          ("USA Pickleball rules hub", RULES_HUB, "")])}
{more("guides/pickleball-rules-cheat-sheet-2026.html")}'''
    page("guides/pickleball-rules-cheat-sheet-2026.html", "Pickleball rules cheat sheet 2026 (USA Pickleball rulebook)", cheat,
         "A one-page 2026 pickleball rules cheat sheet from the USA Pickleball Official Rulebook, with the confirmed 2026 changes to rally scoring, serves, double hits and out calls.",
         fresh={"source": [RULES, RULES_CHANGES], "faq": cheat_faq},
         schema=[faq_ld])

    # ----- DUPR -----
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
    ]
    faq_html, faq_ld = faq(dupr_faq)
    pct_rows = "".join(f'<tr><th scope="row">{r}</th><td>{p}</td><td>{t}</td></tr>' for r, p, t in PCT)
    dist_rows = "".join(f'<tr><th scope="row">{r}</th><td>{s_}</td></tr>' for r, s_ in DIST_ROWS)
    dupr = f'''<h1>How to read DUPR ratings</h1>
<p class="meta">The DUPR scale, how a rating is calculated, and what percentile your number puts you in. From DUPR's own pages and The Dink.</p>
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
<p>Need a rules refresher before a rated match? Use the <a href="pickleball-rules-cheat-sheet-2026.html">2026 rules cheat sheet</a>.</p>
{money_links()}
{faq_html}
{sources([("DUPR: How it works", DUPR_HOW, ""),
          ("DUPR: How your DUPR rating is calculated", DUPR_CALC, ""),
          ("DUPR: Algo update, win or lose your rating can go up", DUPR_ALGO, "July 8, 2025"),
          ("DUPR: DUPR rating percentiles", DUPR_PCT, "snapshot September 22, 2026"),
          ("The Dink: DUPR rating percentiles, where does your rating rank?", DINK_PCT, "Thomas Shields, October 7, 2026")])}
{more("guides/how-to-read-dupr-ratings.html")}'''
    page("guides/how-to-read-dupr-ratings.html", "How to read DUPR ratings: scale, calculation and percentiles", dupr,
         "How to read a DUPR rating: the 2.000 to 8.000 scale, the four factors in the calculation, the reliability score, and 2026 percentiles from DUPR and The Dink.",
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
<p>If you can stretch your budget, the <a href="best-paddles-under-100.html">best paddles under $100</a> guide lists dated maker prices, and <a href="how-to-choose-a-paddle.html">how to choose a paddle</a> explains what you give up at the low end.</p>
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
<p>Watching the pros this fall? See the <a href="../events/ppa-worlds-2026.html">PPA Worlds 2026 guide</a> and <a href="../events/usa-pickleball-nationals-2026.html">USA Pickleball Nationals 2026</a>.</p>
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
        ("Is PickleballTV free?",
         "Partly. PickleballTV runs a free 24/7 channel with selected matches and original shows, offered on Fubo, Samsung TV Plus, Roku, Fire TV and Plex. Every court, full replays and DVR features need a paid PickleballTV app subscription."),
        ("How much does the PickleballTV app cost?",
         "The App Store and Google Play listings say full access costs $5.99 a month or $59.99 a year, with a 30-day free trial. The app streams up to six courts live per event, plus on-demand replays."),
        ("What channel is pro pickleball on?",
         "Most pro pickleball streams on PickleballTV. In 2026 the PPA Tour also put select rounds on Tennis Channel, FS1 and FS2, and CBS aired Championship Sunday at the Carvana Masters. MLP matches aired on CBS and FS1. The APP Tour uses ESPN+, APPTV on YouTube, and national windows on ESPN2 and CBS Sports Network."),
        ("How can I watch PPA Worlds 2026?",
         "United Pickleball says every day of the main draw, from the round of 64 on Tuesday, November 3 through Championship Sunday on November 8, is live on PickleballTV. The Celebrity Pro-Am is on Tennis Channel and PickleballTV on Thursday, November 5, from 7 to 9 p.m. CT."),
        ("How do I watch the APP Tour?",
         "At 2026 APP events, Championship Court has aired on ESPN+ and the Players Court on APPTV on YouTube, per the APP. Some Championship Sundays also had national windows on ESPN2 or CBS Sports Network."),
        ("How can I watch USA Pickleball Nationals 2026?",
         "The official Nationals site says every match at the 2026 Oceanview USA Pickleball National Championships, October 31 to November 8 in San Diego, is livestreamed and recorded by VS Sports."),
    ]
    wt_faq_html, wt_faq_ld = faq(wt_faq)
    watch = f'''<h1>How to watch pro pickleball on TV and streaming (2026)</h1>
<p class="meta">Where the PPA Tour, Major League Pickleball, the APP Tour and USA Pickleball Nationals stream and air, from the tours' own pages and the PickleballTV app listings, read {wt_checked}. Broadcast windows move, so confirm on the linked schedule before you tune in. Times are Central (CT) unless noted.</p>
<h2>The short answer</h2>
<ul>
<li><b>PPA Tour and MLP:</b> stream on <b>PickleballTV</b>. The {ext(WT_PPA, "PPA Tour")} says PickleballTV streams every round of every Carvana PPA Tour event, with marquee rounds on national TV.</li>
<li><b>APP Tour:</b> <b>ESPN+</b> for Championship Court and <b>APPTV on YouTube</b> for the Players Court, per the {ext(WT_APP_DET, "APP")}.</li>
<li><b>USA Pickleball Nationals:</b> every match is livestreamed and recorded by <b>VS Sports</b>, per the {ext(WT_UN_LIVE, "official Nationals site")}.</li>
</ul>
<h2>Who streams what</h2>
<div class="tbl"><table><thead><tr><th>Tour or event</th><th>Streaming</th><th>National TV</th><th>Source</th></tr></thead><tbody>{wt_who_rows}</tbody></table></div>
<p>The CBS window at the Carvana Masters ran 12 to 2 p.m. ET on Championship Sunday in January 2026, per {ext(WT_CBS, "Pickleball.com")}. MLP's viewer numbers are from its {ext(WT_MLP, "October 28, 2026 release")}.</p>
<h2>PickleballTV: free channel vs the app</h2>
<p><b>The free channel.</b> {ext(WT_PBTV, "PickleballTV")} runs 24/7 and says it is offered on <b>Fubo, Samsung TV Plus, Roku, Fire TV and Plex</b>. The app listings describe this free FAST channel as carrying selected matches and original shows.</p>
<p><b>The paid app.</b> The {ext(WT_IOS, "App Store")} (iPhone, iPad, Apple TV) and {ext(WT_PLAY, "Google Play")} listings say the app is a free download, and full access costs <b>$5.99 a month or $59.99 a year</b>, with a 30-day free trial. Paid access adds up to six live courts per event, full replays on demand, and pause and rewind. The listings say it covers more than 3,000 live hours from 32 PPA and MLP tournaments a year.</p>
<p>So if you only want the feature court, the free channel may be enough. If you want to follow one player on an outer court, or rewatch a match, you need the app.</p>
<h2>This week: Nations Cup, Nationals and PPA Worlds</h2>
<p>Three big events overlap. Nations Cup times are converted from the {ext(WT_PPA, "PPA's watch page")} (listed in ET). PPA Worlds times are from {ext(WT_UP_PRO, "United Pickleball")} (listed in CT), which says windows can move. All times CT.</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>Event</th><th>Where to watch</th><th>Window (CT)</th></tr></thead><tbody>{wt_week_rows}</tbody></table></div>
<p>PPA pro qualifying on Monday, November 2 had no stream window on the PPA's schedule when we checked. For tickets, parking and rosters, see our <a href="../events/mlp-nations-cup-2026.html">MLP Nations Cup 2026</a>, <a href="../events/usa-pickleball-nationals-2026.html">USA Pickleball Nationals 2026</a> and <a href="../events/ppa-worlds-2026.html">PPA Worlds 2026</a> guides.</p>
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
{sources([("PPA Tour: Watch pro pickleball", WT_PPA, f"PickleballTV coverage, Nations Cup and Worlds windows (ET), read {wt_checked}"),
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
{more("guides/how-to-watch-pro-pickleball.html")}'''
    page("guides/how-to-watch-pro-pickleball.html", "How to watch pro pickleball: TV channels, PickleballTV and streaming (2026)", watch,
         "How to watch pro pickleball in 2026: PickleballTV free channel vs $5.99 app, PPA and MLP on Tennis Channel, FS1 and CBS, APP on ESPN+, plus PPA Worlds windows.",
         fresh={"checked": WT_CHECKED, "who": WT_WHO, "week": WT_WEEK, "next": WT_NEXT, "faq": wt_faq},
         schema=[wt_faq_ld])

    # ----- PPA Worlds 2026 -----
    PPA_EV = "https://www.ppatour.com/events/2026/pickleball-world-championships/"
    PPA_TODAY = "https://www.ppatour.com/events/2026/pickleball-world-championships/today/"
    UP_HOME = "https://worlds.unitedpickleball.com/"
    UP_SCHED = "https://worlds.unitedpickleball.com/schedule"
    UP_TIX = "https://worlds.unitedpickleball.com/tickets"
    FB_CITY = "https://discoverfarmersbranch.com/pickleball/"
    WEEK = [("Fri Oct 30 – Sun Nov 1", "MLP Nations Cup, the official kickoff (eight international teams)", ""),
            ("Mon Nov 2", "PPA pro qualifying", "11:00 AM"), ("Tue Nov 3", "Main draw, round of 64", "11:00 AM"),
            ("Wed Nov 4", "Main draw, round of 32", "11:00 AM"), ("Thu Nov 5", "Main draw, round of 16", "11:00 AM"),
            ("Fri Nov 6", "Quarterfinals", "11:00 AM"), ("Sat Nov 7", "Semifinals", "11:00 AM"),
            ("Sun Nov 8", "Championship Sunday, finals", "10:00 AM")]
    TIX = [("Grounds Pass (any day)", "$30.42"), ("Courtside Bleacher", "$46.66 – $92.03"), ("Courtside Chair", "$113.69 – $221.99"),
           ("VIP", "$276.13 – $438.58"), ("Box Suite (daily)", "$3,254.23 – $9,751.90"), ("Weeklong Grounds Pass", "$113.69"),
           ("MLP Nations Cup courtside", "$25.00 – $35.83"), ("MLP Nations Cup 3-day courtside", "$70.37")]
    week_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(t) or "see schedule"}</td></tr>' for d, w, t in WEEK)
    tix_rows = "".join(f'<tr><th scope="row">{e(k)}</th><td>{e(v)}</td></tr>' for k, v in TIX)
    w_faq = [
        ("When is PPA Worlds 2026?",
         "The PPA Tour event, the Opendoor Pickleball World Championships, runs November 2 to 8, 2026. The wider Worlds week starts October 30 with the MLP Nations Cup, so United Pickleball lists Worlds as October 30 to November 8."),
        ("Is PPA Worlds 2026 in Brookhaven or Farmers Branch?",
         "Both are correct. The venue is Brookhaven Country Club, 3333 Golfing Green Drive, and it is in the city of Farmers Branch, Texas, in the Dallas area. Brookhaven is the club, not a separate city."),
        ("How much are PPA Worlds 2026 tickets?",
         "United Pickleball's ticket page, using Tixr data from October 11, 2026, lists a Grounds Pass at $30.42 any day, courtside bleachers from $46.66 to $92.03, and a weeklong grounds pass at $113.69, fees included. Tickets are sold on Tixr and prices change by day and demand."),
        ("Where do I park for PPA Worlds 2026?",
         "The PPA says all general parking is at Dallas College Brookhaven Campus, Lot P3, 3939 Valley View Lane, with free shuttles to the venue from October 30 to November 8. Overnight and RV parking is not allowed."),
    ]
    w_faq_html, w_faq_ld = faq(w_faq)
    w_event = {"@type": "SportsEvent", "name": "Opendoor Pickleball World Championships 2026", "startDate": "2026-11-02", "endDate": "2026-11-08",
               "url": PPA_EV, "organizer": {"@type": "Organization", "name": "Carvana PPA Tour"},
               "location": {"@type": "Place", "name": "Brookhaven Country Club",
                            "address": {"@type": "PostalAddress", "streetAddress": "3333 Golfing Green Dr", "addressLocality": "Farmers Branch",
                                        "addressRegion": "TX", "postalCode": "75234", "addressCountry": "US"}},
               "offers": {"@type": "Offer", "url": UP_TIX}}
    worlds = f'''<h1>PPA Worlds 2026: dates, venue and tickets</h1>
<p class="meta">The Opendoor Pickleball World Championships, from the official PPA Tour and United Pickleball pages. Checked {checked}. Confirm on the official pages before you travel.</p>
<h2>Dates</h2>
<p>The {ext(PPA_EV, "PPA Tour event page")} lists the <b>Opendoor Pickleball World Championships</b> for <b>November 2 to 8, 2026</b>. It is a PPA Major worth 3,000 ranking points, with a listed total payout of $1,648,641.</p>
<p>The reported <b>October 30 to November 8</b> dates are for the whole Worlds week. {ext(UP_SCHED, "United Pickleball's schedule")} starts the week with the <b>MLP Nations Cup</b> on October 30 to November 1, the official kickoff, at the same venue. The PPA pro event itself starts November 2.</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>What's on</th><th>First serve</th></tr></thead><tbody>{week_rows}</tbody></table></div>
<p>First-serve times are from the PPA's {ext(PPA_TODAY, "at the event page")}. Gate times had not been posted on {checked}.</p>
<h2>Venue: Brookhaven Country Club, Farmers Branch</h2>
<p>Both names are right. The venue is <b>Brookhaven Country Club</b>, 3333 Golfing Green Dr, <b>Farmers Branch, TX 75234</b>, in the Dallas area. Brookhaven is the club. Farmers Branch is the city. The PPA and the {ext(FB_CITY, "City of Farmers Branch")} both give that address.</p>
<h2>Parking and getting there</h2>
<ul>
<li>All general parking is at <b>Dallas College Brookhaven Campus, Lot P3</b>, 3939 Valley View Lane, Farmers Branch, TX 75244. Free shuttles run to the venue from October 30 to November 8, about 6:30 AM to 11:00 PM.</li>
<li>Rideshare pickup and drop-off is on Brookhaven Drive, just past Golfing Green Drive.</li>
<li>Box Suite ticket holders get on-site parking. Overnight and RV parking is not allowed.</li>
<li>The city has a resident-only parking permit rule on streets near the club from October 30 to November 8.</li>
</ul>
<h2>Tickets</h2>
<p>Tickets are sold through Tixr. {ext(UP_TIX, "United Pickleball's ticket page")} lists these prices, including fees, using Tixr data from October 11, 2026. Prices vary by day and demand.</p>
<div class="tbl"><table><thead><tr><th>Ticket</th><th>Price listed</th></tr></thead><tbody>{tix_rows}</tbody></table></div>
<p>On that page, the weeklong courtside, chair, VIP and box suite passes were marked sold out. Our <a href="opendoor-pickleball-world-championships.html">event card</a> links to the official Tixr page.</p>
<h2>Gear before you go</h2>
{money_links()}
{w_faq_html}
{sources([("PPA Tour: Opendoor Pickleball World Championships 2026", PPA_EV, f"dates, payout, points, checked {checked}"),
          ("PPA Tour: At the event", PPA_TODAY, f"schedule, address, parking, checked {checked}"),
          ("United Pickleball: Pickleball Worlds 2026", UP_HOME, f"checked {checked}"),
          ("United Pickleball: Week schedule", UP_SCHED, "October 30 to November 8"),
          ("United Pickleball: Tickets", UP_TIX, "Tixr data from October 11, 2026"),
          ("City of Farmers Branch: Pickleball", FB_CITY, "venue address, neighborhood parking")])}
<p>Watching the kickoff? See the <a href="mlp-nations-cup-2026.html">MLP Nations Cup 2026 teams and how to watch</a>.</p>
<p>Watching from home? Worlds is on PickleballTV every day of the main draw, with the Celebrity Pro-Am on Tennis Channel. See <a href="../guides/how-to-watch-pro-pickleball.html">how to watch pro pickleball</a> for windows and PickleballTV free vs paid.</p>
<p><a href="../tournaments.html">All tournaments</a></p>'''
    page("events/ppa-worlds-2026.html", "PPA Worlds 2026: dates, venue and tickets (Farmers Branch, TX)", worlds,
         "PPA Worlds 2026: the Opendoor Pickleball World Championships run Nov 2 to 8 at Brookhaven Country Club, Farmers Branch, TX, after the Oct 30 MLP Nations Cup kickoff. Schedule, parking and ticket prices.",
         fresh={"checked": CHECKED, "week": WEEK, "tix": TIX, "faq": w_faq},
         schema=[w_event, w_faq_ld])
    # MLP Nations Cup page. Every fact below was read on the two linked pages on NC_CHECKED.
    NC_CHECKED = "2026-10-26"
    nc_checked = _dt.date.fromisoformat(NC_CHECKED).strftime("%B %-d, %Y")
    NC_UP = "https://worlds.unitedpickleball.com/nations-cup"
    NC_DINK = "https://www.thedinkpickleball.com/mlp-nations-cup-2026-tournament-preview-everything-you-need-to-know/"
    NC_MLP = "https://www.majorleaguepickleball.co/"
    NC_TEAMS = [
        ("A", "Team USA", "Johnny Goldberg", "Anna Bright, Tyra Black, Kate Fahey, Ben Johns, CJ Klinger, Will Howells"),
        ("A", "Team Canada", "Steve Deakin", "Victoria DiMuzio, Blaine Hovenier, Armaan Jiwa Mawji, Layne Sleeth, Ryan Torresin, Angie Walker"),
        ("A", "Team Europe - West", "Chris Cantino", "Judit Castillo, Helena Jansen, Will MacKinnon, Theo Platel, Estee Widdershoven, DJ Young"),
        ("A", "Team Asia Domestic", "Geoffrey Nguyen and Jeff Tsao (co-captains)", "Augie Ge, Milan Rane, Jonathan Truong, Zoey Wang, Jamie Wei, Len Yang"),
        ("B", "Team Australia", "Sange Carter", "Sarah Burr, Chris Crouch, Sahra Dennehy, Mitch Hargreaves, Danni-Elle Townsend, George Wall"),
        ("B", "Team Latin America", "Juan Benitez", "Nico Acevedo, Mari Humberg, Rafa Lenhard, Eric Oncins, Alexa Schull, Charlie Trevino"),
        ("B", "Team Europe - East", "Caleb Garrard", "Andrei Daescu, Arwid Dahlin, Ivan Jakovljevic, Lina Padegimaite, Tina Pisnik, Daria Walczak"),
        ("B", "Team Asia International", "Madeleine Lim", "Rika Fujiwara, Lingwei Kong, Jimmy Liong, Tama Shimabukuro, Jack Wong, Macy Ybañez"),
    ]
    NC_TV = [("Fri Oct 30", "Round robin (six matches)", "10 AM CT / 11 AM ET"),
             ("Sat Oct 31", "Round robin (six matches)", "10 AM CT / 11 AM ET"),
             ("Sun Nov 1", "Semifinals", "10 AM CT / 11 AM ET"),
             ("Sun Nov 1", "Championship match", "2 PM CT / 3 PM ET")]
    nc_team_rows = "".join(f'<tr><td>{e(g)}</td><th scope="row">{e(t)}</th><td>{e(c)}</td><td>{e(r)}</td></tr>' for g, t, c, r in NC_TEAMS)
    nc_tv_rows = "".join(f'<tr><th scope="row">{e(d)}</th><td>{e(w)}</td><td>{e(t)}</td></tr>' for d, w, t in NC_TV)
    nc_faq = [
        ("How can I watch the MLP Nations Cup 2026?",
         "United Pickleball says every match is available on PickleballTV and the PickleballTV app. Championship Court matches are livestreamed on PickleballTV, and Grandstand Court matches are on the PickleballTV app."),
        ("What time does MLP Nations Cup coverage start?",
         "The Dink lists coverage starting at 10 a.m. CT (11 a.m. ET) on Friday, Saturday and Sunday, with the championship match at 2 p.m. CT (3 p.m. ET) on Sunday, November 1."),
        ("Who is on Team USA at the MLP Nations Cup?",
         "The Dink lists captain Johnny Goldberg with Anna Bright, Tyra Black, Kate Fahey, Ben Johns, CJ Klinger and Will Howells."),
        ("How does the MLP Nations Cup format work?",
         "Eight teams play the MLP coed team format in two groups of four. Each team plays three round-robin matches on Friday and Saturday. The top two in each group reach Sunday's semifinals, where each group winner plays the other group's runner-up, and the winners meet in the final."),
        ("Are Nations Cup tickets the same as PPA Worlds tickets?",
         "No. United Pickleball says Nations Cup tickets are sold separately from Worlds week, with sessions and current prices on Tixr. Doors open one hour before the first matches."),
    ]
    nc_faq_html, nc_faq_ld = faq(nc_faq)
    nc_event = {"@type": "SportsEvent", "name": "MLP Nations Cup 2026", "startDate": "2026-10-30", "endDate": "2026-11-01",
                "url": NC_UP, "organizer": {"@type": "Organization", "name": "Major League Pickleball"},
                "location": {"@type": "Place", "name": "Brookhaven Country Club",
                             "address": {"@type": "PostalAddress", "addressLocality": "Farmers Branch", "addressRegion": "TX", "postalCode": "75234", "addressCountry": "US"}},
                "offers": {"@type": "Offer", "url": NC_UP}}
    nations = f'''<h1>MLP Nations Cup 2026: teams, format and how to watch</h1>
<p class="meta">From the official United Pickleball Nations Cup page and The Dink's October 26 preview. Checked {nc_checked}. Rosters and times can change, so confirm on the official pages.</p>
<h2>The basics</h2>
<p>The inaugural <b>MLP Nations Cup</b> runs <b>Friday, October 30 to Sunday, November 1, 2026</b> at <b>Brookhaven Country Club in Farmers Branch, Texas</b>, in the Dallas area. {ext(NC_UP, "United Pickleball")} calls it the official kickoff to the Opendoor Pickleball World Championships, which start November 2 at the same venue. Eight regional teams and 48 pros play Major League Pickleball's coed team format.</p>
<h2>How to watch</h2>
<p>Every match is available on <b>PickleballTV</b> and the <b>PickleballTV app</b>, per United Pickleball. Championship Court is livestreamed on PickleballTV, and Grandstand Court matches are on the app. These are the coverage start times listed by {ext(NC_DINK, "The Dink")}:</p>
<div class="tbl"><table><thead><tr><th>Day</th><th>What's on</th><th>Coverage starts</th></tr></thead><tbody>{nc_tv_rows}</tbody></table></div>
<p>Live scores and standings are posted on {ext(NC_MLP, "majorleaguepickleball.co")} during the event. United Pickleball says more broadcast details are still to be announced.</p>
<h2>Format</h2>
<p>The eight teams are split into two groups of four. Each team plays three round-robin matches across Friday and Saturday. The top two in each group advance to Sunday's single-elimination bracket: the Group A winner plays the Group B runner-up, the Group B winner plays the Group A runner-up, and the two winners meet in the final for the first Nations Cup title.</p>
<h2>Teams and rosters</h2>
<p>Rosters as listed by The Dink on {nc_checked}. It notes that Tama Shimabukuro replaced Hien Truong on Asia International in an October 20 update.</p>
<div class="tbl"><table><thead><tr><th>Group</th><th>Team</th><th>Captain</th><th>Players</th></tr></thead><tbody>{nc_team_rows}</tbody></table></div>
<p>Want to see what the pros play? The <a href="../pro-paddles.html">pro paddles page</a> lists each player's paddle from their official PPA profile.</p>
<h2>Going in person</h2>
<p>Nations Cup tickets are sold separately from Worlds week, with sessions and current prices on Tixr. United Pickleball lists a Courtside Pass (bleacher seating, first come first served) and a VIP Pass. Doors open one hour before the first matches, outside food and drink are not allowed, and filming matches is not permitted without MLP's written approval. For parking, shuttles and the rest of the week, see our <a href="ppa-worlds-2026.html">PPA Worlds 2026 guide</a>.</p>
<h2>Gear before you go</h2>
{money_links()}
{nc_faq_html}
{sources([("United Pickleball: MLP Nations Cup", NC_UP, f"dates, teams, streaming, tickets, checked {nc_checked}"),
          ("The Dink: MLP Nations Cup 2026 preview", NC_DINK, "rosters, groups, format, broadcast times; by Erik Tice, October 26, 2026"),
          ("Major League Pickleball", NC_MLP, "live scores and standings")])}
<p><a href="../tournaments.html">All tournaments</a> · <a href="ppa-worlds-2026.html">PPA Worlds 2026</a></p>'''
    page("events/mlp-nations-cup-2026.html", "MLP Nations Cup 2026: teams, rosters, format and how to watch", nations,
         "How to watch the MLP Nations Cup 2026 (Oct 30 to Nov 1, Farmers Branch, TX): PickleballTV times in CT and ET, all 8 team rosters including Team USA, groups and format.",
         fresh={"checked": NC_CHECKED, "teams": NC_TEAMS, "tv": NC_TV, "faq": nc_faq},
         schema=[nc_event, nc_faq_ld])
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
<p>Same week, different event: the Opendoor Pickleball World Championships run November 2 to 8 in Farmers Branch, Texas. See our <a href="ppa-worlds-2026.html">PPA Worlds 2026 guide</a> and <a href="mlp-nations-cup-2026.html">MLP Nations Cup 2026 how to watch</a>.</p>
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
<p><a href="../tournaments.html">All tournaments</a> · <a href="ppa-worlds-2026.html">PPA Worlds 2026</a> · <a href="mlp-nations-cup-2026.html">MLP Nations Cup 2026</a></p>'''
    page("events/usa-pickleball-nationals-2026.html", "USA Pickleball Nationals 2026: schedule, tickets and how to watch", nationals,
         "USA Pickleball Nationals 2026 runs Oct 31 to Nov 8 at Barnes Tennis Center, San Diego: VS Sports livestream, day-by-day schedule, pro medal matches, free GA tickets and parking.",
         fresh={"checked": UN_CHECKED, "days": UN_DAYS, "tix": UN_TIX_ROWS, "faq": un_faq},
         schema=[un_event, un_faq_ld])
