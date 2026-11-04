"""Black Friday entry point card for the homepage and /deals, pointing to the Black Friday paddle deals page.
Date-gated at build time in Central Time through END (Tue Dec 1, 2026), like worlds_card.py (DTP_BUILD_DATE
override for testing, YYYY-MM-DD). Pages only rebuild on deploy, so an inline script also hides it once Dec 1 is
over in CT (Dec 2 00:00 CST = 06:00 UTC); it runs before first paint, so there is no layout shift.
Plain facts only: no countdowns or "ends soon" wording, and never says codes stack."""
import datetime, os
from zoneinfo import ZoneInfo
from gift_pages import BF_URL, BF_DAY, CM_DAY
END = datetime.date(2026, 12, 1)

CSS = (".bfe{background:#0b1426;border-radius:18px;padding:14px;margin:14px 0;box-shadow:inset 0 0 0 2px #c6f432;color:#fff;contain:layout}"
       ".bfe[hidden]{display:none}.bfe h2::before{display:none}"
       ".bfe h2{margin:0 0 4px;font:800 22px/28px Inter,system-ui,sans-serif;color:#c6f432;letter-spacing:0;text-transform:none}"
       ".bfe p{margin:0 0 12px;font:700 17px/24px Inter,system-ui,sans-serif;color:#fff}"
       ".bfe .bfe-r{display:flex;flex-wrap:wrap;gap:8px}"
       ".bfe a{flex:1 1 200px;display:flex;align-items:center;justify-content:center;min-height:52px;padding:8px 12px;border-radius:12px;"
       "font:800 18px/22px Inter,system-ui,sans-serif;text-decoration:none;text-align:center}"
       ".bfe a.b1{background:#c6f432;color:#0b1426}.bfe a.b2{background:#16264a;color:#fff;box-shadow:inset 0 0 0 2px rgba(198,244,50,.55)}"
       ".bfe a:focus-visible{outline:3px solid #fff;outline-offset:2px}")

def build_date():  # same rule as build.py evwk_build_date()
    v = os.environ.get("DTP_BUILD_DATE")
    return datetime.date.fromisoformat(v) if v else datetime.datetime.now(ZoneInfo("America/Chicago")).date()

def _md(s):
    d = datetime.date.fromisoformat(s)
    return f"{d:%a} {d:%b} {d.day}"

def html(where="home", OWN=None, today=None):
    """Card HTML, or "" after END (CT). where: "home" or "deals" (sets the second button)."""
    today = today or build_date()
    if today > END: return ""
    vol = (OWN or {}).get("Volair")
    code = f' Our Volair code {vol["code"]} takes {vol["discount"]} at checkout.' if vol else ""
    second = ('<a class="b2" href="/discount-codes">💸 All discount codes</a>' if where == "home"
              else '<a class="b2" href="/price-tracker">📈 Is it a real deal? Price tracker</a>')
    cid = f"bfe-{where}"
    return (f'<aside class="bfe" id="{cid}" aria-label="Black Friday paddle deals"><h2>🛒 Black Friday paddle deals</h2>'
            f'<p>Black Friday is {_md(BF_DAY)}, Cyber Monday {_md(CM_DAY)}. Dated maker prices and brand sales we\'ve confirmed.{code}</p>'
            f'<div class="bfe-r"><a class="b1" href="{BF_URL}">🔥 See Black Friday paddle deals</a>{second}</div></aside>'
            f'<script>if(Date.now()>=Date.UTC(2026,11,2,6))document.getElementById("{cid}").hidden=true</script>')
