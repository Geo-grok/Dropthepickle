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
]


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

    def more(current):
        links = "".join(f'<li><a href="../{fn}">{e(title)}</a></li>' for fn, title in GUIDES if fn != current)
        links += '<li><a href="../price-index.html">Paddle price index</a></li><li><a href="../tournaments.html">Pro events</a></li><li><a href="../creators/ryan-morneau.html">Ryan Morneau spotlight</a></li>'
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
<p>Pickleball Breakdowns is Ryan Morneau's channel. On the channel he says he watches how the best players in the world make decisions, then breaks that down so you can use it in your next match. <a href="{JMU}" target="_blank" rel="noopener">James Madison University</a> reported that he was the No. 1-ranked collegiate pickleball player in the United States, held that ranking for more than a year, and became the first collegiate singles national champion.</p>
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
         "No. These pages filter published specs and today's maker prices. They are not a playtest and not a rating."),
        ("Where are the prices from?",
         "Each price is the maker's own price from our daily check, in the currency on that maker's page. We do not invent a street price."),
    ]
    faq_html, faq_ld = faq(choose_faq)
    choose = f'''<h1>How to choose a pickleball paddle</h1>
<p class="meta">A beginner and intermediate walkthrough using the specs and maker prices already in our database. Not a ranking.</p>
<p>You do not need a pro's paddle to start. You do need to know which published number you are buying. Work through budget, shape, core, and weight, then open the paddle page and read the maker's specs.</p>
<h2>1. Set a budget</h2>
<p>In our database the lowest USD maker price today is {money(lo, cur(lo))} for the {alink(lo)}, and the highest is {money(hi, cur(hi))} for the {alink(hi)}. Six Zero models are listed in AUD, so they are not in that dollar range. The <a href="../price-index.html">price index</a> tracks every recorded maker price. If you want to stay at $100, use the <a href="best-paddles-under-100.html">under-$100 guide</a>, which only includes paddles whose current maker price is actually at or under $100.</p>
<h2>2. Pick a shape</h2>
<p>An elongated face is longer and usually narrower. On our spec pages we describe that as extra reach, with less room on the sides when you miss the middle. A wider face, including shapes makers call Max, Widebody, or Hybrid, gives more side-to-side area. The <a href="../best-elongated-paddles.html">elongated filter</a> lists every paddle whose shape field includes elongated. Two real examples: the {alink(perseus)} is listed as elongated, and the {alink(halo)} is listed as Max or XL.</p>
<h2>3. Pick a core thickness</h2>
<p>Core thickness is the millimetre number in the core field, such as 13mm, 14mm, 16mm, or 19mm. Thicker cores are generally described as softer. Thinner cores are generally described as crisper. That is a description of the spec, not a test result from us. The <a href="paddle-weight-and-core.html">weight and core guide</a> shows which thicknesses our paddles actually publish, with a link to each example.</p>
<h2>4. Check the weight</h2>
<p>Makers that publish a weight in our files land between {light[0]:.1f} oz ({alink(light[2])}) and {heavy[1]:.1f} oz ({alink(heavy[2])}{", maker price in AUD" if heavy[2]["currency"] != "USD" else ""}). Lighter published weights are easier to swing at the kitchen. Heavier published weights put more mass behind the ball and can feel slower in a fast exchange. Some makers leave weight blank. If it is blank on the paddle page, we do not guess it.</p>
<h2>5. Read one spec page before you buy</h2>
<p>Open the <a href="../paddles.html">paddle database</a> or <a href="../compare.html">compare two paddles</a> from the same brand. Each paddle page repeats the maker's core, shape, weight, and today's price, and links to the maker's product page.</p>
{faq_html}
{more("guides/how-to-choose-a-paddle.html")}'''
    page("guides/how-to-choose-a-paddle.html", "How to choose a pickleball paddle", choose,
         "How to choose a pickleball paddle from published shape, core, weight, and maker price. Not a scored ranking.",
         fresh={"low": [lo["brand"], lo["model"], cur(lo)], "high": [hi["brand"], hi["model"], cur(hi)],
                "weight": [light[0], heavy[1]], "faq": choose_faq},
         schema=[faq_ld])

    # ----- under $100 -----
    def row(p, note):
        h = ph(p)
        sale = f' Sale, down from the maker\'s compare-at of {money(p, h["compare_at"])}.' if h.get("sale") and h.get("compare_at") else ""
        spec = " · ".join(x for x in [p.get("core"), p.get("shape"), p.get("weight")] if x)
        return f'<li>{alink(p)} — {money(p, cur(p))} today.{e(sale)} Published specs: {e(spec) or "the maker page does not list core, shape, and weight clearly"}. {note}</li>'

    if u100:
        under_items = "".join(row(p, "This is the only USD paddle in our database at $100 or less right now." if len(u100) == 1 else "At or under $100 at today's maker price.") for p in u100)
        under_lead = f"{len(u100)} USD paddle{'s' if len(u100) != 1 else ''} in our database {'are' if len(u100) != 1 else 'is'} at $100 or less at today's maker price."
    else:
        under_items = "<li>None. No USD paddle in our database is at or under $100 at today's maker price.</li>"
        under_lead = "No USD paddle in our database is at or under $100 at today's maker price."
    near_items = "".join(row(p, "Over $100. Listed here only so you can see the next prices in the file, not because it made a $100 cutoff.") for p in near) or "<li>None at $150 or under either.</li>"
    names = ", ".join(f"{p['brand']} {p['model']}" for p in u100) or "none"
    u100_faq = [
        ("Which paddles are under $100?",
         f"{under_lead} {names}. The list is alphabetical only when prices tie. It is not ordered by how the paddles play."),
        ("Are the paddles between $100 and $150 included?",
         "They are shown in a separate list and labeled as over $100. They are not called under-$100 paddles."),
        ("Why is the list so short?",
         "Our database is a small set of major-brand models with specs copied from the maker's page. It is not a catalog of every budget paddle for sale."),
    ]
    faq_html, faq_ld = faq(u100_faq)
    under = f'''<h1>Best paddles under $100</h1>
<p class="meta">From our paddle file only. Today's maker price, not a playtest and not a ranking.</p>
<p>{under_lead} "Best" on this page means "matches the price filter," the same rule as the <a href="../best-paddles-under-100.html">under-$100 spec list</a>. We do not score power, control, or spin.</p>
<h2>At or under $100</h2>
<ul>{under_items}</ul>
<h2>Just over $100, up to $150</h2>
<p>These are still USD maker prices from the same file. They cost more than $100.</p>
<ul>{near_items}</ul>
<p>Six Zero prices are in AUD on the maker's site, so a Six Zero paddle is not converted into this dollar list. Check the <a href="../price-index.html">price index</a> if you want every recorded price, including AUD.</p>
{faq_html}
{more("guides/best-paddles-under-100.html")}'''
    page("guides/best-paddles-under-100.html", "Best paddles under $100", under,
         "Which paddles in the DropThePickle database are at or under $100 at today's maker price, plus the next prices up to $150. Not a playtest ranking.",
         fresh={"under": [(p["brand"], p["model"], cur(p)) for p in u100],
                "near": [(p["brand"], p["model"], cur(p)) for p in near], "faq": u100_faq},
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
