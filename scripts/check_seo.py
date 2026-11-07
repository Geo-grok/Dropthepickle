#!/usr/bin/env python3
"""Source/rendered SEO checks for dist/. Stdlib plus BeautifulSoup (already required).

Fails on missing titles, descriptions, canonicals or H1s, unparseable JSON-LD,
sitemap URLs that are not real built pages, broken internal links, and the
specific contradictions fixed on 2026-11-07. Does not claim rich-result eligibility.
"""
import json, re, sys, pathlib
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup

ROOT = pathlib.Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
BASE = "https://dropthepickle.com"
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
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

sm = ET.parse(DIST / "sitemap.xml")
locs = [el.text.strip() for el in sm.getroot().findall("sm:url/sm:loc", NS)]
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

u100 = text_of("best-paddles-under-100.html")
if u100.find("<h2>At or under $100</h2>") > u100.find("<h2>Closest picks, $100 to $150</h2>"):
    fail("under-$100 page lists the over-$100 group first")
graph = json.loads(BeautifulSoup(u100, "html.parser").find("script", attrs={"type": "application/ld+json"}).string)
lists = [n for n in graph["@graph"] if n.get("@type") == "ItemList"]
names = [n.get("name") for n in lists]
if names[:1] != ["At or under $100"]:
    fail(f"under-$100 primary ItemList name is {names[:1]}")
primary = lists[0]
for item in primary["itemListElement"]:
    price = float(item["item"]["offers"]["price"])
    if price > 100: fail(f"under-$100 ItemList includes {item['name']} at {price}")
if any(n.get("name") == "Closest picks, $100 to $150" and any(float(i["item"]["offers"]["price"]) <= 100 for i in n["itemListElement"]) for n in lists):
    fail("the $100 to $150 ItemList includes an at-or-under-$100 paddle")

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
event = next(n for n in wgraph["@graph"] if n.get("@type") == "SportsEvent")
if event.get("startDate") != "2026-11-02T08:00:00-06:00":
    fail(f"Worlds startDate is {event.get('startDate')}")
if "11:00 a.m." not in event.get("description", "") and "11:00" not in event.get("description", ""):
    fail("Worlds schema description dropped the PPA 11 a.m. disagreement")
if 'id="this-weekend"' not in worlds:
    fail("Worlds page is missing the weekend answer")
if "November 7, 2026" not in worlds:
    fail("Worlds page does not record the November 7 recheck")

home = text_of("index.html")
if "<h1>Pickleball news, paddle prices and codes</h1>" not in home:
    fail("homepage H1 was not updated")
if "yours either way" in home:
    fail("homepage still says the discount is yours either way")

about = text_of("about.html")
if "No person is named as editor" not in about:
    fail("about page does not state that there is no named editor")

if "yours either way" in "\n".join(p.read_text() for p in pages):
    fail("a built page still says the discount is yours either way")

print(f"checked {len(pages)} HTML pages, {len(locs)} sitemap URLs")
if bad:
    print(f"{len(bad)} problems:")
    for msg in bad: print(" -", msg)
    sys.exit(1)
print("seo checks passed")
