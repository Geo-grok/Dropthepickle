#!/usr/bin/env python3
"""Source/rendered SEO checks for dist/. Stdlib plus BeautifulSoup (already required).

Fails on missing titles, descriptions, canonicals or H1s, unparseable JSON-LD,
sitemap URLs that are not real built pages, broken internal links, and the
specific contradictions fixed on 2026-11-07. Does not claim rich-result eligibility.
"""
import json, re, sys, pathlib
from bs4 import BeautifulSoup
import sitemap_util

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BASE = "https://dropthepickle.com"
bad = []

def fail(msg):
    bad.append(msg)

def soup(path):
    return BeautifulSoup(path.read_text(), "html.parser")

pages = sorted(p for p in DIST.rglob("*.html"))
if not pages:
    fail("dist/ has no HTML; run python3 build.py first")

for path in pages:
    rel = path.relative_to(DIST).as_posix()
    doc = soup(path)
    title = (doc.title.string or "").strip() if doc.title and doc.title.string else ""
    desc = doc.find("meta", attrs={"name": "description"})
    desc_v = (desc.get("content") or "").strip() if desc else ""
    canon = doc.find("link", rel="canonical")
    canon_v = (canon.get("href") or "").strip() if canon else ""
    h1s = doc.find_all("h1")
    if rel != "404.html":
        if not title: fail(f"{rel}: missing title")
        if not desc_v: fail(f"{rel}: missing meta description")
        if "paddles.json" in desc_v or "price_history.json" in desc_v:
            fail(f"{rel}: meta description names an internal data file")
        if not canon_v.startswith(BASE + "/") and canon_v != BASE + "/":
            fail(f"{rel}: canonical is not on {BASE}: {canon_v}")
        if ".html" in canon_v: fail(f"{rel}: canonical still has .html: {canon_v}")
        if len(h1s) != 1: fail(f"{rel}: expected 1 h1, found {len(h1s)}")
    for block in doc.find_all("script", attrs={"type": "application/ld+json"}):
        try:
            json.loads(block.string or "")
        except Exception as ex:
            fail(f"{rel}: JSON-LD did not parse: {ex}")
    for a in doc.find_all("a", href=True):
        href = a["href"].split("#", 1)[0].split("?", 1)[0]
        if not href or href.startswith(("mailto:", "http://", "https://", "/go/", "/api/")): continue
        target = (DIST / href.lstrip("/")) if href.startswith("/") else (path.parent / href).resolve()
        try:
            target.relative_to(DIST.resolve())
        except ValueError:
            fail(f"{rel}: internal link escapes dist: {a['href']}")
            continue
        if target.is_file(): continue
        html = target.with_name(target.name + ".html") if target.suffix == "" else None
        index = target / "index.html"
        if (html and html.is_file()) or index.is_file(): continue
        fail(f"{rel}: broken internal link {a['href']}")

robots = (DIST / "robots.txt").read_text() if (DIST / "robots.txt").is_file() else ""
if "Sitemap: https://dropthepickle.com/sitemap.xml" not in robots:
    fail("robots.txt does not declare the sitemap")
if "Disallow: /go/" not in robots:
    fail("robots.txt does not disallow /go/")

try:
    locs, children = sitemap_util.page_locs_from_dist(DIST, BASE)
except Exception as ex:
    fail(f"sitemap index: {ex}")
    locs, children = [], []
if children:
    child_names = []
    for cloc in children:
        try:
            child_names.append(sitemap_util.child_filename(cloc, BASE))
        except ValueError as ex:
            fail(str(ex))
    for name in sitemap_util.EXPECTED_CHILDREN:
        if name not in child_names:
            fail(f"sitemap index missing {name}")
    extra = [n for n in child_names if n not in sitemap_util.EXPECTED_CHILDREN]
    if extra:
        fail(f"unexpected child sitemaps: {extra}")
else:
    fail("sitemap.xml is not a sitemap index with child sitemaps")
seen = set()
for loc in locs:
    if loc in seen: fail(f"duplicate sitemap URL {loc}")
    seen.add(loc)
    if not loc.startswith(BASE): fail(f"sitemap URL off-host: {loc}")
    if ".html" in loc: fail(f"sitemap URL has .html: {loc}")
    path = loc[len(BASE):] or "/"
    if path == "/":
        fn = DIST / "index.html"
    elif path.endswith("/"):
        fn = DIST / path.lstrip("/") / "index.html"
    else:
        fn = DIST / (path.lstrip("/") + ".html")
    if not fn.is_file(): fail(f"sitemap URL has no built page: {loc}")

def text_of(rel):
    return (DIST / rel).read_text()

u100 = text_of("guides/best-paddles-under-100.html")
if u100.find("<h2>Under $100 (verified)</h2>") > u100.find("<h2>Closest verified prices, $100 to $150</h2>"):
    fail("under-$100 page lists the over-$100 group first")
graph = json.loads(BeautifulSoup(u100, "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
lists = [n for n in graph["@graph"] if n.get("@type") == "ItemList"]
names = [n.get("name") for n in lists]
if names[:1] != ["Under $100 (verified)"]:
    fail(f"under-$100 primary ItemList name is {names[:1]}")
primary = lists[0]
for item in primary["itemListElement"]:
    price = float(item["item"]["offers"]["price"])
    if price >= 100: fail(f"under-$100 ItemList includes {item['name']} at {price}")
if any(n.get("name") == "Closest verified prices, $100 to $150" and any(float(i["item"]["offers"]["price"]) < 100 for i in n["itemListElement"]) for n in lists):
    fail("the $100 to $150 ItemList includes an under-$100 paddle")

vol = text_of("paddle-volair-v-1f-xl-w-16mm.html")
if "doesn't publish a weight" in vol:
    fail("V.1F page still says the maker does not publish a weight")
if "8 oz" not in vol:
    fail("V.1F page no longer shows the published 8 oz weight")
if "yours either way" in vol:
    fail("V.1F page still promises the discount either way")
if "<h1>Volair V.1F/ XL-W 16mm</h1>" not in vol:
    fail("V.1F H1 does not include the brand")

worlds = text_of("events/opendoor-pickleball-world-championships.html")
wgraph = json.loads(BeautifulSoup(worlds, "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
event = next(n for n in wgraph["@graph"] if n.get("@type") == "SportsEvent" and "World" in n.get("name", ""))
if event.get("startDate") != "2026-11-02T08:00:00-06:00":
    fail(f"Worlds startDate is {event.get('startDate')}")
if event.get("endDate") != "2026-11-08":
    fail(f"Worlds endDate should be the published last day with no clock, got {event.get('endDate')}")
if "offers" in event:
    fail("Worlds SportsEvent still carries an offer, and the ticket figures are an October 11 snapshot")
if "11:00 a.m." not in event.get("description", ""):
    fail("Worlds schema description dropped the PPA 11 a.m. disagreement")
if "broadcast end" not in event.get("description", ""):
    fail("Worlds schema description does not say the 4 p.m. window is a broadcast end")
if event["location"]["address"]["streetAddress"] != "3333 Golfing Green Dr":
    fail("Worlds schema address is not the club's 3333 Golfing Green Dr")
if 'id="this-weekend"' not in worlds:
    fail("Worlds page is missing the weekend answer")
if "Court board snapshot, read November 7, 2026" not in worlds:
    fail("Worlds page does not date the court-board snapshot")
if "What's left:" in worlds or "Short answer for November 7" in worlds:
    fail("Worlds lead still presents November 7 as the current status")
if "Not a live checkout price" not in worlds:
    fail("Worlds ticket section does not mark the October 11 figures as historical")
if "October 11, 2026 Tixr figure" not in worlds:
    fail("Worlds ticket table header does not name the Tixr snapshot")
import os
from datetime import date
from zoneinfo import ZoneInfo
_bd = os.environ.get("DTP_BUILD_DATE")
built = date.fromisoformat(_bd) if _bd else __import__("datetime").datetime.now(ZoneInfo("America/Chicago")).date()
h2 = BeautifulSoup(worlds, "html.parser").find(id="this-weekend")
h2_text = h2.get_text(" ", strip=True) if h2 else ""
if built == date(2026, 11, 7) and h2_text != "Built November 7, 2026: semifinals, then Championship Sunday":
    fail(f"Nov 7 build lead heading is {h2_text!r}")
elif built == date(2026, 11, 8) and "November 8, 2026" not in h2_text:
    fail(f"Nov 8 build lead heading is {h2_text!r}")
elif built > date(2026, 11, 8) and h2_text != "PPA Worlds weekend: the published schedule":
    fail(f"post-event build lead heading is {h2_text!r}")
elif built < date(2026, 11, 7) and "November 7, 2026" in h2_text and "Built November 7" in h2_text:
    fail("a pre-November 7 build is using the November 7 current-status heading")

nations = text_of("events/mlp-nations-cup-2026.html")
ngraph = json.loads(BeautifulSoup(nations, "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
nc = next(n for n in ngraph["@graph"] if n.get("@type") == "SportsEvent")
if nc["location"]["address"]["streetAddress"] != "3333 Golfing Green Dr":
    fail(f"Nations Cup schema address is {nc['location']['address']['streetAddress']}")
if nc.get("endDate") != "2026-11-01":
    fail(f"Nations Cup endDate should be the last day with no clock, got {nc.get('endDate')}")
if "3334 Golfing Green Drive" not in nations:
    fail("Nations Cup page dropped the United Pickleball 3334 disagreement")

home = text_of("index.html")
if "<h1>Pickleball news, paddle prices and codes</h1>" not in home:
    fail("homepage H1 was not updated")
if "yours either way" in home:
    fail("homepage still says the discount is yours either way")
if built == date(2026, 11, 7) and "Built Nov 7:" not in home:
    fail("homepage Worlds card does not date the November 7 build")
if built > date(2026, 11, 8) and 'id="wmd"' in home:
    fail("homepage Worlds card is still rendered after November 8")

about = text_of("about.html")
about_desc = about and BeautifulSoup(about, "html.parser").find("meta", attrs={"name": "description"})["content"]
if "No named editor" in about_desc or "No person is named" in about_desc:
    fail(f"about meta description centers a missing editor: {about_desc}")
if "maker pages" not in about_desc or "geolobo@mail.grokbot.com" not in about_desc:
    fail(f"about meta description does not describe sourcing and corrections: {about_desc}")

if "yours either way" in "\n".join(p.read_text() for p in pages):
    fail("a built page still says the discount is yours either way")

guide = json.loads(BeautifulSoup(text_of("guides/how-to-dink.html"), "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
crumbs = next(n for n in guide["@graph"] if n.get("@type") == "BreadcrumbList")
guides_url = next(i["item"] for i in crumbs["itemListElement"] if i["name"] == "Guides")
if guides_url != "https://dropthepickle.com/guides":
    fail(f"Guides breadcrumb points at {guides_url}")
deal = json.loads(BeautifulSoup(text_of("deals/black-friday-pickleball-deals-2026.html"), "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
deal_crumbs = next(n for n in deal["@graph"] if n.get("@type") == "BreadcrumbList")
deals_url = next((i["item"] for i in deal_crumbs["itemListElement"] if i["name"] == "Deals"), None)
if deals_url != "https://dropthepickle.com/deals":
    fail(f"Deals breadcrumb is {deals_url}")

def product_offer(fn):
    g = json.loads(BeautifulSoup(text_of(fn), "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
    return next(n for n in g["@graph"] if n.get("@type") == "Product")["offers"]
# Honeyfoam TKO-X: schema availability must follow the latest recorded price check, not a hardcoded state.
_tko = json.loads((ROOT / "data" / "price_history.json").read_text())["paddles"]["Paddletek Honeyfoam TKO-X"]["history"][-1].get("available")
_tko_want = {True: "https://schema.org/InStock", False: "https://schema.org/OutOfStock"}.get(_tko)
if product_offer("paddle-paddletek-honeyfoam-tko-x.html").get("availability") != _tko_want:
    fail(f"Honeyfoam TKO-X availability should match latest price check ({_tko_want or 'none recorded'})")
if "availability" in product_offer("paddle-paddletek-tempest-veyra.html"):
    fail("Tempest Veyra has no recorded availability and should not claim InStock")
if product_offer("paddle-volair-v-1f-xl-w-16mm.html").get("availability") != "https://schema.org/InStock":
    fail("V.1F should stay InStock")
cmp_ = json.loads(BeautifulSoup(text_of("compare.html"), "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
cmp_list = next(n for n in cmp_["@graph"] if n.get("@type") == "ItemList")
if cmp_list.get("name") != "All paddles":
    fail("compare ItemList is not named for the All paddles section")
if "Compare pickleball paddles" not in text_of("compare.html"):
    fail("compare H1 was not clarified")
if "<h1>Upcoming pro pickleball tournaments</h1>" not in text_of("tournaments.html"):
    fail("tournaments H1 was not clarified")
feed_events = [p for p in pages if p.parent.name == "events" and p.name not in ("opendoor-pickleball-world-championships.html", "mlp-nations-cup-2026.html", "usa-pickleball-nationals-2026.html")]
if not feed_events or not all("What the official feed lists" in p.read_text() and "does not call the ticket link registration" in p.read_text() and "A ticket link, when the feed has one, is only a ticket link." in p.read_text() for p in feed_events):
    fail("a feed event page is missing the official-feed facts or mislabels tickets as registration")
if any("Drop the Pickle" in p.read_text() for p in pages):
    fail("a page still says Drop the Pickle")
for p in pages:
    rel = p.relative_to(DIST).as_posix()
    if rel == "404.html":
        continue
    if "DropThe<span>Pickle</span>" not in p.read_text():
        fail(f"{rel} wordmark is not DropThePickle")
    if 'property="og:image:alt" content="DropThePickle"' not in p.read_text() and rel not in ("links.html", "links/tiktok.html", "links/instagram.html"):
        fail(f"{rel} og:image:alt is not DropThePickle")
home_html = text_of("index.html")
if "We do not claim to have playtested the paddles." not in home_html:
    fail("homepage identity sentence missing")
if "avantlink.com/affiliate_app_confirm.php" in home_html:
    fail("AvantLink homepage verification script is still present")
if "Price checked" not in text_of("guides/best-paddles-under-100.html"):
    fail("under-100 guide comparison table missing")
if "DropThePickle has not playtested this paddle." not in text_of("paddle-volair-v-1f-xl-w-16mm.html"):
    fail("V.1F still lacks the specs-vs-playtest line")
if " · DropThePickle" not in BeautifulSoup(text_of("events/opendoor-pickleball-world-championships.html"), "html.parser").title.string:
    fail("Worlds title is missing the DropThePickle publisher token")
if " · DropThePickle" not in BeautifulSoup(text_of("discount-codes/bodhi.html"), "html.parser").title.string:
    fail("Bodhi coupon title is missing the separate DropThePickle token")
if "DROPTHEPICKLE" not in text_of("discount-codes/volair.html"):
    fail("Volair coupon spelling changed")
volair_title = BeautifulSoup(text_of("discount-codes/volair.html"), "html.parser").title.string
if volair_title.count("DropThePickle") != 1 or "DROPTHEPICKLE" not in volair_title or not volair_title.endswith(" · DropThePickle"):
    fail(f"Volair title must keep the coupon and add one exact publisher suffix: {volair_title}")
cmp_html = text_of("compare.html")
if "Maker specs side by side" not in cmp_html or "Price checked" not in cmp_html or "Not a playtest." not in cmp_html:
    fail("compare hub is missing the maker-facts table")
if "Side-by-side maker specs. Not a playtest." not in text_of("best-paddles-for-power.html"):
    fail("power best-of hub is missing the spec table")
vs_html = text_of("vs-selkirk-omni-vs-selkirk-slk-era-power.html")
if "Price checked" not in vs_html or "Maker spec page" not in vs_html or "not a playtest result" not in vs_html:
    fail("head-to-head page is missing price date, source, or fact/opinion line")
volair_vs = text_of("vs-volair-mach-2-forza-vs-volair-pro-1.html")
if "specs read" not in volair_vs or "prices checked" not in volair_vs or "not a playtest" not in volair_vs:
    fail("Volair Mach 2 vs Pro 1 no longer states source dates and the not-a-playtest line")
volair_best = text_of("guides/best-volair-paddles.html")
if "Price checked" not in volair_best or ">volair.com</a>" not in volair_best or "have not playtested" not in volair_best:
    fail("Volair player-type guide is missing per-row price date, source, or the not-a-playtest line")
under_guide = text_of("guides/best-paddles-under-100.html")
if "Price checked" not in under_guide or "maker product page" not in under_guide or "Not a playtest" not in under_guide:
    fail("under-$100 guide is missing price date, maker source, or the not-a-playtest line")

# Phase 0 retired-URL 301s: map is in src/page-redirects.json; the Worker issues the 301s.
REDIRECTS_EXPECTED = {
    "/events/mojo-energy-pouches-virginia-beach-open": "/articles/virginia-beach-open-2026-first-time-champions",
    "/vs-selkirk-labs-project-boomstik-vs-six-zero-coral-16mm": "/paddle-selkirk-labs-project-boomstik",
    "/vs-gearbox-gbx-power-elongated-gen-3-vs-six-zero-coral-16mm": "/paddle-gearbox-gbx-power-elongated-gen-3",
    "/vs-joola-hyperion-pro-v-vs-six-zero-coral-16mm": "/paddle-joola-hyperion-pro-v",
    "/vs-gearbox-gbx-power-elongated-gen-3-vs-joola-hyperion-pro-v": "/paddle-gearbox-gbx-power-elongated-gen-3",
}
redir_path = ROOT / "src" / "page-redirects.json"
if not redir_path.is_file():
    fail("src/page-redirects.json is missing")
    redirs = {}
else:
    redirs = json.loads(redir_path.read_text()).get("redirects") or {}
if redirs != REDIRECTS_EXPECTED:
    fail(f"page-redirects.json does not match the five retired 301s: {redirs}")
for src, dest in REDIRECTS_EXPECTED.items():
    src_fn = DIST / (src.lstrip("/") + ".html")
    if src_fn.is_file():
        fail(f"retired URL still has a built page (should 301): {src}")
    dest_fn = DIST / "index.html" if dest == "/" else DIST / (dest.lstrip("/") + ".html")
    if not dest_fn.is_file():
        fail(f"301 target has no built page: {src} -> {dest}")
    if (BASE + dest) not in seen:
        fail(f"301 target is not in the sitemap: {dest}")

print(f"checked {len(pages)} HTML pages, {len(locs)} sitemap URLs")
if bad:
    print(f"{len(bad)} problems:")
    for msg in bad: print(" -", msg)
    sys.exit(1)
print("seo checks passed")
