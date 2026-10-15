import sys
from playwright.sync_api import sync_playwright
pages=sys.argv[1:] or ["index","paddles","reviews"]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":390,"height":844},device_scale_factor=2,is_mobile=True)
    errs=[];pg.on("pageerror",lambda e:errs.append(str(e)))
    for n in ["deals","vs-joola-perseus-pro-v-vs-joola-hyperion-pro-v","compare","pro-paddles","index","tournaments","reviews","news","pros","creators","podcasts","paddles","shop","community","about","disclosure","privacy"]:
        r=pg.goto(f"http://localhost:8765/{n}.html",wait_until="domcontentloaded");pg.wait_for_timeout(800)
        print(n,r.status,pg.title(),"overflowX" if pg.evaluate("document.documentElement.scrollWidth>390") else "")
        if n in pages: pg.screenshot(path=f"screenshots/{n}-390.png",full_page=False if n!="index" else True)
    print("js errors:",errs);b.close()
