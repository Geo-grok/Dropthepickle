"""Check internal links/assets in dist/ and that external links resolve."""
import pathlib,re,sys,requests,concurrent.futures as cf
from bs4 import BeautifulSoup
D=pathlib.Path(__file__).parent.parent/"dist"; bad=[]; ext=set()
for f in D.rglob("*.html"):
    s=BeautifulSoup(f.read_text(),"html.parser")
    for t,a in [("a","href"),("link","href"),("script","src"),("iframe","src"),("form","action")]:
        for el in s.find_all(t):
            u=el.get(a)
            if not u: continue
            if u.startswith(("http://","https://")):
                if "dropthepickle.com" not in u and u.rstrip("/") not in ("https://fonts.googleapis.com","https://fonts.gstatic.com"): ext.add(u)  # skip preconnect hosts  # own domain not live yet (canonical tags)
                continue
            if u.startswith(("mailto:","#","/api/")): continue
            p=u.split("#")[0]
            if not p: continue
            target = (D / p.lstrip("/")) if p.startswith("/") else (f.parent / p).resolve()
            try: target.relative_to(D.resolve())
            except ValueError: bad.append((f.name,u)); continue
            if not target.exists() and not target.with_name(target.name+".html").exists(): bad.append((f.name,u))  # Cloudflare assets serve /x as x.html
print("internal broken:",bad)
H={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
def chk(u):
    if "youtube.com/watch" in u: u0,u="",u; u="https://www.youtube.com/oembed?format=json&url="+u
    try:
        r=requests.get(u,headers=H,timeout=20,allow_redirects=True,stream=True); r.close(); return u.split('url=')[-1],r.status_code
    except Exception as ex: return u,str(ex)[:60]
res=list(cf.ThreadPoolExecutor(16).map(chk,sorted(ext)))
fail=[(u,c) for u,c in res if c!=200]
print(f"external: {len(res)} checked, {len(fail)} non-200")
for u,c in fail: print("  ",c,u)
sys.exit(1 if bad else 0)
