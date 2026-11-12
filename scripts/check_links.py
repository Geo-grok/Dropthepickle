"""Check internal links/assets in dist/, URL/canonical/index hygiene, and (optionally) the live site.

  python3 scripts/check_links.py                 dist checks + external link check (slow, network)
  python3 scripts/check_links.py --no-external   dist checks only
  python3 scripts/check_links.py --live [BASE]   also check the deployed site (default https://dropthepickle.com):
                                                 every sitemap URL answers 200 with no redirect, a self canonical and no
                                                 noindex (meta or X-Robots-Tag); sample .html / trailing-slash URLs answer
                                                 one 301 to the clean URL.

Dist checks (fail the run):
  * broken internal links and assets
  * no internal link points at a .html URL or at www./http:// dropthepickle.com (each would be a redirect hop)
  * every indexable page's canonical is its own final URL (dir/x.html -> https://dropthepickle.com/dir/x)
  * every sitemap URL is a built page whose canonical is that exact URL and which carries no noindex
  * no noindex page is in the sitemap
"""
import pathlib, re, sys, json, requests, concurrent.futures as cf
from xml.etree import ElementTree as ET
from bs4 import BeautifulSoup
import sitemap_util
ROOT = pathlib.Path(__file__).resolve().parent.parent
D = (ROOT / "dist").resolve(); bad = []; ext = set()
BASE = "https://dropthepickle.com"
GO = json.loads((ROOT / "src" / "go-links.json").read_text()).get("links", {})  # /go/<slug> is served by the Worker, not dist/
args = sys.argv[1:]
def final_url(rel):
    if rel == "index.html": return BASE + "/"
    if rel.endswith("/index.html"): return f"{BASE}/{rel[:-len('index.html')]}"
    return f"{BASE}/{rel[:-5]}"
def is_noindex(s):
    return any("noindex" in (m.get("content") or "").lower() for m in s.find_all("meta", attrs={"name": re.compile(r"^(robots|googlebot)$", re.I)}))
pages = {}
for f in D.rglob("*.html"):
    rel = f.relative_to(D).as_posix()
    s = BeautifulSoup(f.read_text(), "html.parser"); pages[rel] = s
    for t, a in [("a", "href"), ("link", "href"), ("script", "src"), ("iframe", "src"), ("form", "action")]:
        for el in s.find_all(t):
            u = el.get(a)
            if not u: continue
            if t == "a" and re.match(r"^(https?:)?//(www\.)?dropthepickle\.com", u) and (u.startswith("http://") or "//www." in u):
                bad.append((rel, f"internal link via http/www: {u}"))
            if u.startswith(("http://", "https://")):
                if t == "a" and "dropthepickle.com" in u and "/go/" not in u and re.search(r"\.html([#?]|$)", u): bad.append((rel, f"internal link to .html: {u}"))
                if "dropthepickle.com" not in u and u.rstrip("/") not in ("https://fonts.googleapis.com", "https://fonts.gstatic.com"): ext.add(u)
                continue
            if u.startswith(("mailto:", "#", "/api/")): continue
            p = u.split("#")[0].split("?")[0]
            if not p: continue
            if t == "a" and p.endswith(".html") and not p.startswith("/go/"): bad.append((rel, f"internal link to .html: {u}"))
            if p.startswith("/go/"):
                if p[4:].strip("/") not in GO: bad.append((rel, u))
                continue
            target = (D / p.lstrip("/")) if p.startswith("/") else (f.parent / p).resolve()
            try: target.relative_to(D)
            except ValueError: bad.append((rel, u)); continue
            if not target.exists() and not target.with_name(target.name + ".html").exists() and not (target / "index.html").exists(): bad.append((rel, u))  # Cloudflare assets serve /x as x.html
# canonical == final URL for every indexable page
for rel, s in pages.items():
    if rel == "404.html" or is_noindex(s): continue
    c = s.find("link", rel="canonical"); cv = (c.get("href") or "").strip() if c else ""
    if cv != final_url(rel): bad.append((rel, f"canonical {cv!r} is not the page's final URL {final_url(rel)}"))
# sitemap: built, self-canonical, indexable (index + per-template children)
try:
    locs, children = sitemap_util.page_locs_from_dist(D, BASE)
except Exception as ex:
    bad.append(("sitemap.xml", str(ex)))
    locs, children = [], []
if not children:
    bad.append(("sitemap.xml", "not a sitemap index with child sitemaps"))
by_url = {final_url(rel): rel for rel in pages}
for loc in locs:
    rel = by_url.get(loc)
    if not rel: bad.append(("sitemap.xml", f"no built page for {loc}")); continue
    s = pages[rel]; c = s.find("link", rel="canonical")
    if not c or c.get("href") != loc: bad.append(("sitemap.xml", f"{loc}: canonical is {c.get('href') if c else None}"))
    if is_noindex(s): bad.append(("sitemap.xml", f"{loc}: noindex page is in the sitemap"))
print(f"dist: {len(pages)} pages, {len(locs)} sitemap URLs, {sum(1 for s in pages.values() if is_noindex(s))} noindex pages")
print("internal problems:", len(bad))
for x in bad[:50]: print("  ", x)
H = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
if "--live" in args:
    i = args.index("--live"); live = (args[i + 1] if len(args) > i + 1 and args[i + 1].startswith("http") else BASE).rstrip("/")
    lbad = []
    sm = requests.get(live + "/sitemap.xml", headers=H, timeout=30)
    def resolve_live_child(loc):
        url = loc.replace(BASE, live, 1) if loc.startswith(BASE) else loc
        r = requests.get(url, headers=H, timeout=30)
        r.raise_for_status()
        return ET.fromstring(r.content)
    try:
        llocs, _lchildren = sitemap_util.page_locs_from_xml_text(sm.text, resolve_live_child)
    except Exception as ex:
        lbad.append(f"sitemap index: {ex}")
        llocs = []
    def chk_live(u):
        u2 = u.replace(BASE, live, 1)
        r = requests.get(u2, headers=H, timeout=30, allow_redirects=False)
        out = []
        if r.status_code != 200: out.append(f"{u}: status {r.status_code} {r.headers.get('location', '')}")
        else:
            s = BeautifulSoup(r.text, "html.parser"); c = s.find("link", rel="canonical")
            if not c or c.get("href") != u: out.append(f"{u}: canonical {c.get('href') if c else None}")
            if is_noindex(s) or "noindex" in (r.headers.get("x-robots-tag") or "").lower(): out.append(f"{u}: noindex")
        return out
    with cf.ThreadPoolExecutor(8) as ex:
        for o in ex.map(chk_live, llocs): lbad += o
    for u in [x for x in llocs if not x.endswith("/")][:15]:
        for variant in (u + ".html", u + "/"):
            r = requests.get(variant.replace(BASE, live, 1) + "?q=1", headers=H, timeout=30, allow_redirects=False)
            want = u.replace(BASE, live, 1) + "?q=1"
            if r.status_code != 301 or r.headers.get("location") != want: lbad.append(f"{variant}?q=1: {r.status_code} -> {r.headers.get('location')} (want 301 -> {want})")
            else:
                r2 = requests.get(want, headers=H, timeout=30, allow_redirects=False)
                if r2.status_code != 200: lbad.append(f"{want}: second hop answered {r2.status_code}")
    print(f"live: {len(llocs)} sitemap URLs checked, {len(lbad)} problems")
    for x in lbad[:50]: print("  ", x)
    bad += [("live", x) for x in lbad]
if "--no-external" not in args and "--live" not in args:
    def chk(u):
        if "youtube.com/watch" in u: u = "https://www.youtube.com/oembed?format=json&url=" + u
        try:
            r = requests.get(u, headers=H, timeout=20, allow_redirects=True, stream=True); r.close(); return u.split('url=')[-1], r.status_code
        except Exception as ex: return u, str(ex)[:60]
    res = list(cf.ThreadPoolExecutor(16).map(chk, sorted(ext)))
    fail = [(u, c) for u, c in res if c != 200]
    print(f"external: {len(res)} checked, {len(fail)} non-200 (informational)")
    for u, c in fail: print("  ", c, u)
sys.exit(1 if bad else 0)
