"""390px and 1280px screenshots of key pages -> screenshots/redesign-<page>-<w>.png (needs a server on :8765 serving dist/)."""
from playwright.sync_api import sync_playwright
PAGES = {"home": "index", "deals": "deals", "paddle": "paddle-joola-perseus-pro-v", "compare": "vs-joola-perseus-pro-v-vs-joola-hyperion-pro-v"}
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    for w, h in [(390, 844), (1280, 800)]:
        pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=2 if w == 390 else 1, is_mobile=w == 390)
        errs = []; pg.on("pageerror", lambda x: errs.append(str(x)))
        for k, n in PAGES.items():
            pg.goto(f"http://localhost:8765/{n}.html", wait_until="networkidle"); pg.wait_for_timeout(500)
            pg.evaluate("document.querySelectorAll('.rv').forEach(x=>x.classList.add('in'))"); pg.wait_for_timeout(800)
            ov = pg.evaluate(f"document.documentElement.scrollWidth>{w}")
            pg.screenshot(path=f"screenshots/redesign-{k}-{w}.png", full_page=True)
            print(k, w, "overflowX" if ov else "ok")
        print("js errors:", errs); pg.close()
    b.close()
