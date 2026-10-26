"""Link-in-bio page for TikTok and Instagram: /links, /links/tiktok, /links/instagram.
Minimal on purpose: no site nav, no web fonts, one small avatar, inline CSS, a few lines of vanilla JS.
Every internal link gets utm_source=<platform>&utm_medium=social&utm_campaign=bio. The hrefs are baked in at
build time (so they work without JS), and the inline script swaps utm_source when the page URL has ?src= or ?utm_source=."""
import json, pathlib, re, subprocess, urllib.parse
ROOT = pathlib.Path(__file__).parent
# Used only when git history can't tell which video is newest (for example a depth-1 CI checkout where every file shares one commit).
LATEST_VIDEO_FALLBACK = "drill-triangle-combo"
PLATFORMS = ("tiktok", "instagram")
ALIASES = {"tt": "tiktok", "tiktok": "tiktok", "ig": "instagram", "insta": "instagram", "instagram": "instagram"}

def latest_video():
    """Newest published video in media/: the .mp4 whose first commit is the most recent."""
    vids = {p.stem for p in (ROOT / "media").glob("*.mp4")}
    if not vids: return None
    added = {}
    try:
        out = subprocess.run(["git", "log", "--diff-filter=A", "--name-only", "--format=@%ct", "--", "media/"],
                             cwd=ROOT, capture_output=True, text=True, timeout=20).stdout
        ts = 0
        for line in out.splitlines():
            if line.startswith("@"): ts = int(line[1:])
            elif line.startswith("media/") and line.endswith(".mp4"):
                stem = pathlib.Path(line).stem
                if stem in vids and stem not in added: added[stem] = ts
    except Exception:
        added = {}
    if added and len(set(added.values())) > 1:
        return max(added, key=lambda s: (added[s], s))
    return LATEST_VIDEO_FALLBACK if LATEST_VIDEO_FALLBACK in vids else sorted(vids)[-1]

def nice(stem):
    words = stem.replace("-", " ").split()
    return " ".join(w.upper() if w in ("dtp", "vs") else w.capitalize() for w in words)

def utm(href, src):
    u = urllib.parse.urlsplit(href)
    q = [(k, v) for k, v in urllib.parse.parse_qsl(u.query) if not k.startswith("utm_")]
    q += [("utm_source", src), ("utm_medium", "social"), ("utm_campaign", "bio")]
    return urllib.parse.urlunsplit((u.scheme, u.netloc, u.path, urllib.parse.urlencode(q), u.fragment))

CSS = """*{box-sizing:border-box}html,body{margin:0;background:#0b1630;color:#fff}
body{font:17px/1.4 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-font-smoothing:antialiased;min-height:100vh}
.w{max-width:480px;margin:0 auto;padding:28px 18px 40px}
.hd{text-align:center;margin-bottom:22px}
.av{display:inline-grid;place-items:center;width:112px;height:112px;border-radius:50%;background:#c6f432;box-shadow:0 0 0 6px rgba(198,244,50,.18)}
.av img{width:100px;height:100px;border-radius:50%;display:block;background:#0b1630}
.wm{display:block;margin:14px 0 4px;font:400 38px/1 Anton,Impact,"Arial Narrow Bold",sans-serif;letter-spacing:.02em;color:#fff;text-decoration:none}.wm span{color:#7cff4f}
.tg{margin:0;font-size:18px;font-weight:700;color:#c9d3e6}
.bt{display:flex;align-items:center;gap:14px;min-height:72px;margin:0 0 14px;padding:14px 18px;border-radius:18px;background:#16264a;color:#fff;text-decoration:none;font-size:20px;font-weight:800;line-height:1.2;border:2px solid #22386a}
.bt:active{transform:scale(.98)}.bt:focus-visible{outline:4px solid #c6f432;outline-offset:3px}
.bt i{flex:none;font-style:normal;font-size:28px;width:36px;text-align:center}
.bt b{display:block}.bt small{display:block;font-size:15px;font-weight:600;color:#c9d3e6;margin-top:3px}
.bt.hot{background:#c6f432;color:#0b1630;border-color:#c6f432}.bt.hot small{color:#16264a}
.bt::after{content:"\\2192";margin-left:auto;font-size:24px;opacity:.8}
.ft{text-align:center;margin-top:22px;font-size:16px;color:#c9d3e6}.ft a{color:#c6f432;font-weight:700}"""

JS = """<script>(()=>{const A=%s,q=new URLSearchParams(location.search),r=(q.get('src')||q.get('utm_source')||'').toLowerCase();const s=A[r]||(r==='bio'?'bio':document.body.dataset.src||'bio');document.body.dataset.src=s;document.querySelectorAll('a[data-utm]').forEach(a=>{const u=new URL(a.getAttribute('href'),location.href);u.searchParams.set('utm_source',s);u.searchParams.set('utm_medium','social');u.searchParams.set('utm_campaign','bio');a.href=u.pathname+u.search+u.hash})})()</script>"""

def make(C, e, canon, CATALOG, DIST, extra=None):
    vid = latest_video()
    buttons = []
    if vid: buttons.append(("hot", "▶", "Latest video", nice(vid), f"/media/{vid}.mp4"))
    buttons += [("", "🏷", "Discount codes", "Working paddle codes, checked daily", "/discount-codes"),
                ("", "🔥", "Pickleball Buzz", "What everyone is talking about", "/buzz"),
                ("", "💸", "Top deals", "Paddle price drops", "/deals"),
                ("", "📉", "Price tracker", "Real prices with the date we checked", "/price-tracker")]
    for b in (extra or []): buttons.insert(b.pop("at", len(buttons)), (b["cls"], b["icon"], b["title"], b["sub"], b["href"]))
    n = C["SITE_NAME"]; base = C["BASE_URL"].rstrip("/")
    desc = "Big Dill's links: the latest video, pickleball discount codes, buzz, top paddle deals and the price tracker."
    url = canon("links.html"); img = base + "/og-1200x630.png"
    alias_js = json.dumps(ALIASES)
    def render(fn, src, robots):
        pre = "../" * fn.count("/")
        btns = "".join(f'<a class="bt{" " + c if c else ""}" href="{e(utm(h, src))}" data-utm><i aria-hidden="true">{ic}</i><span><b>{e(t)}</b><small>{e(s)}</small></span></a>' for c, ic, t, s, h in buttons)
        title = f"{n} links · Big Dill"
        doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#0b1630">{robots}
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(n)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(img)}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{pre}favicon.ico" sizes="48x48"><link rel="apple-touch-icon" href="{pre}apple-touch-icon.png"><link rel="canonical" href="{e(url)}">
<style>{CSS}</style>
<script async src="https://aromatic-caribou-889.convex.site/api/a/am_WGwXq9YSwrdbKKse"></script></head>
<body data-src="{src}"><main class="w"><header class="hd"><a class="av" href="{e(utm('/', src))}" data-utm aria-label="{e(n)} home"><picture><source srcset="{pre}avatar.webp" type="image/webp"><img src="{pre}avatar.png" alt="Big Dill, the DropThePickle mascot" width="100" height="100"></picture></a>
<a class="wm" href="{e(utm('/', src))}" data-utm>DROPTHE<span>PICKLE</span></a><p class="tg">All things pickleball. Free.</p></header>
<nav aria-label="Links">{btns}</nav>
<p class="ft">Big Dill's home: <a href="{e(utm('/', src))}" data-utm>dropthepickle.com</a></p></main>
{JS % alias_js}
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8b857a29f29446008d526b7021a0eaa1"}}'></script>
</body></html>"""
        out = DIST / fn; out.parent.mkdir(parents=True, exist_ok=True); out.write_text(doc)
        return len(doc.encode())
    sizes = {"links.html": render("links.html", "bio", "")}
    for p in PLATFORMS:
        sizes[f"links/{p}.html"] = render(f"links/{p}.html", p, '<meta name="robots" content="noindex,follow">')
    # Only the main /links page goes in the sitemap; the platform copies are noindex with a canonical to it.
    CATALOG["links.html"] = {"fn": "links.html", "title": f"{n} links · Big Dill", "desc": desc, "updated": None}
    for fn, size in sizes.items():
        if size > 30_000: raise SystemExit(f"{fn} is {size} bytes; keep the link-in-bio page under 30KB")
    return sizes
