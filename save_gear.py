"""Thumb-friendly "Save on gear" CTA row for pages social visitors land on (Buzz, news, guides, how-to-watch,
event and newsroom pages). Links to the three money-saving pages: brand discount codes, paddle deals, price tracker.

Counts come straight from data/discount-codes.json (distinct brands) and data/price-tracker.json (rows), so the
labels never claim more than the data holds. Absolute extensionless hrefs work at any directory depth.
Buzz story pages (buzz/*), best-X buying guides, head-to-head comparison pages and the pros, podcasts, reviews and science pages get it too.
Paddle pages get their own brand-specific row (paddle_pages.py), and the codes, deals and tracker pages already link these, so both are skipped.
The paddle database, pro paddles, compare, guides hub, creator and 404 pages get it too, plus Merch, Marketplace, the price index and the home page (under Top 5).
"""
import json, pathlib, re

_D = pathlib.Path(__file__).parent / "data"
def _load(n):
    try: return json.loads((_D / n).read_text())
    except (OSError, ValueError): return {}

CSS = (".savegear{background:var(--navy);border-radius:16px;padding:12px;margin:16px 0 18px;box-shadow:inset 0 0 0 2px var(--neon)}"
       ".savegear p{margin:0 0 10px;color:#fff;font:800 18px/1.3 Inter,system-ui,sans-serif}.savegear p span{color:var(--neon)}"
       ".savegear .sgr{display:flex;flex-wrap:wrap;gap:8px}"
       ".savegear a{flex:1 1 140px;display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:56px;padding:10px 8px;border-radius:12px;"
       "background:#16264a;color:#fff;font:800 17px/1.2 Inter,system-ui,sans-serif;text-decoration:none;text-align:center;box-shadow:inset 0 0 0 2px rgba(198,244,50,.55)}"
       ".savegear a small{display:block;margin-top:3px;font:700 16px/1.2 Inter,system-ui,sans-serif;color:#d5deeb}"
       ".savegear a.hot{flex-basis:100%;background:var(--neon);color:var(--navy);box-shadow:none}.savegear a.hot small{color:var(--navy)}"
       ".savegear a:hover{background:#1f3360}.savegear a.hot:hover{background:#d6ff4a}"
       ".savegear.sgplus a{flex-basis:120px}.savegear.sgplus a.hot{flex-basis:100%}"
       ".topwrap .savegear{margin:6px 16px 0}")  # home: line up with the Top 5 cards (16px side margins)

SKIP = {"guides/pickleball-gift-guide-2026.html"}  # already a shopping page full of these links
def wants(fn):
    if fn in SKIP: return False
    if fn in ("buzz.html", "news.html", "tournaments.html") or fn.startswith(("guides/", "events/", "articles/")): return True
    # Buzz story pages are what social posts link to; the row lands after the story, right before Sources.
    if fn.startswith("buzz/"): return True
    # Buying-intent pages (best-X paddle guides, head-to-head comparisons) and pro/podcast/review/science pages
    # social and search visitors land on; they only linked codes and the tracker from the menu and footer.
    if "/" not in fn and fn.startswith(("best-", "vs-")) and fn.endswith(".html"): return True
    if fn in ("pros.html", "podcasts.html", "reviews.html", "science.html"): return True
    # Nov 16, 2026: paddle-shopping hubs (paddle database, pro paddles, compare), the guides hub, creator pages and the
    # 404 page had no codes/deals/tracker link above the footer, so phone visitors had to dig through the menu.
    # Nov 19, 2026: the Merch and Marketplace menu pages are "coming soon" dead ends, and the price index is a paddle-price page
    # with no deals/tracker link above the footer. (The home page gets the row under its Top 5 deals in paddle_pages.py.)
    if fn in ("shop.html", "community.html", "price-index.html"): return True
    return fn in ("paddles.html", "pro-paddles.html", "compare.html", "guides.html", "creators.html", "404.html") or fn.startswith("creators/")

# Tournament-traffic pages (Worlds week) also get gift guide, Black Friday hub and Top 5 buttons.
# Scoped by filename so event pages (events/*) keep their exact built HTML.
PLUS = {"buzz.html", "tournaments.html", "guides/how-to-watch-pro-pickleball.html"}
EARLY = {"tournaments.html", "guides.html"}  # intro paragraphs (tournaments) or an all-card list (guides hub, else the row lands at the very end) push it below the fold at 320px, so put it right after the header
def html(plus=False):
    brands = len({c.get("brand") for c in _load("discount-codes.json").get("codes", []) if c.get("brand")})
    tracked = len(_load("price-tracker.json").get("rows", []))
    codes = f"<small>{brands} brands</small>" if brands else ""
    track = f"<small>{tracked} paddles</small>" if tracked else ""
    more = ('<a href="/guides/pickleball-gift-guide-2026">🎁 Gift guide</a>'
            '<a href="/deals/black-friday-pickleball-deals-2026">🖤 Black Friday deals</a>'
            '<a href="/#top5">🏆 Top 5 paddles</a>') if plus else ""
    return (f'<nav class="savegear{" sgplus" if plus else ""}" aria-label="Save on pickleball gear"><p>🥒 <span>Save on gear:</span> codes, deals and price drops</p><div class="sgr">'
            f'<a class="hot" href="/discount-codes">🏷️ Discount codes{codes}</a>'
            '<a href="/deals">🔥 Paddle deals<small>Price drops</small></a>'
            f'<a href="/price-tracker">📉 Price tracker{track}</a>{more}</div></nav>')

# First block-level section after the page header: an <h2>, a <section>/<aside>/<nav>, or a card grid.
_NEXT = re.compile(r'<(?:h2|section|aside|nav|div class="(?:grid|tbl)")[\s>]')
def insert(fn, body):
    """Put the row right before the first section that follows the intro; append if the page has none."""
    if not wants(fn): return body
    row = html(fn in PLUS)
    if fn in EARLY and body.startswith('<section class="pagehead">'):
        k = body.index('</section>') + len('</section>')
        return body[:k] + row + body[k:]
    m = re.search(r'</section>', body) if body.startswith('<section class="pagehead">') else re.search(r'</h1>', body)
    start = m.end() if m else 0
    n = _NEXT.search(body, start)
    if n: return body[:n.start()] + row + body[n.start():]
    if body.endswith("</article>"): return body[:-len("</article>")] + row + "</article>"
    return body + row
