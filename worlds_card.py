"""Homepage card for PPA Worlds main-draw week (Tue Nov 3 to Sun Nov 8, 2026). Static HTML, date-gated at build
time in Central Time like the event-week strip (build.py evwk_build_date, DTP_BUILD_DATE override for testing).
Copy stays true for the whole window: semifinals Sat Nov 7 and Championship Sunday Nov 8, from the published
United Pickleball / PPA windows. No live scores."""
import datetime, os
from zoneinfo import ZoneInfo
START, END = datetime.date(2026, 11, 3), datetime.date(2026, 11, 8)

CSS = (".wmd{background:#0b1426;border-radius:18px;padding:14px;margin:12px max(12px,calc((100% - 1100px)/2)) 4px;box-shadow:inset 0 0 0 2px #c6f432;color:#fff;contain:layout}"
       ".wmd[hidden]{display:none}.wmd h2::before{display:none}"
       ".wmd h2{margin:0 0 4px;font:800 22px/28px Inter,system-ui,sans-serif;color:#c6f432;letter-spacing:0;text-transform:none}"
       ".wmd p{margin:0 0 12px;font:700 17px/24px Inter,system-ui,sans-serif;color:#fff}"
       ".wmd .wmd-r{display:flex;flex-wrap:wrap;gap:8px}"
       ".wmd a{flex:1 1 200px;display:flex;align-items:center;justify-content:center;min-height:52px;padding:8px 12px;border-radius:12px;"
       "font:800 18px/22px Inter,system-ui,sans-serif;text-decoration:none;text-align:center}"
       ".wmd a.w1{background:#c6f432;color:#0b1426}.wmd a.w2{background:#16264a;color:#fff;box-shadow:inset 0 0 0 2px rgba(198,244,50,.55)}"
       ".wmd a:focus-visible{outline:3px solid #fff;outline-offset:2px}")

def build_date():  # same rule as build.py evwk_build_date()
    v = os.environ.get("DTP_BUILD_DATE")
    return datetime.date.fromisoformat(v) if v else datetime.datetime.now(ZoneInfo("America/Chicago")).date()
def html(today=None):
    today = today or build_date()
    if not (START <= today <= END): return ""
    return ('<aside class="wmd" id="wmd" aria-label="PPA Worlds main draw"><h2>🏆 PPA Worlds main draw</h2>'
            '<p>Semifinals are Sat Nov 7 (PickleballTV 11 AM–7 PM CT). Championship Sunday is Nov 8 (first serve 10 AM CT, PickleballTV 10 AM–4 PM).</p><div class="wmd-r">'
            '<a class="w1" href="/events/opendoor-pickleball-world-championships#this-weekend">📺 Worlds schedule this weekend</a>'
            '<a class="w2" href="/buzz">🔥 Worlds coverage on Buzz</a></div></aside>'
            # Pages only rebuild daily, so also hide once Nov 8 is over in CT (Nov 9 00:00 CST = 06:00 UTC); runs before first paint.
            '<script>if(Date.now()>=Date.UTC(2026,10,9,6))document.getElementById("wmd").hidden=true</script>')
