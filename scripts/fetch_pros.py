"""Build data/pros.json from official PPA Tour athlete profiles (facts only)."""
import json,re,requests,datetime
from bs4 import BeautifulSoup
SLUGS="ben-johns anna-leigh-waters federico-staksrud anna-bright hayden-patriquin catherine-parenteau christian-alshon jorja-johnson gabe-tardio parris-todd jw-johnson kate-fahey andrei-daescu jackie-kawamoto collin-johns tyra-black connor-garnett lea-jansen hunter-johnson jade-kawamoto tyson-mcguffin".split()
UA={"User-Agent":"Mozilla/5.0 (PickleHub bot)"}
out=[]
for s in SLUGS:
    url=f"https://www.ppatour.com/athletes/{s}/"
    r=requests.get(url,headers=UA,timeout=20)
    if r.status_code!=200: print("skip",s,r.status_code); continue
    soup=BeautifulSoup(r.text,"html.parser")
    p={}
    for sc in soup.find_all("script",type="application/ld+json"):
        try: j=json.loads(sc.string)
        except Exception: continue
        for it in (j.get("@graph",[j]) if isinstance(j,dict) else j):
            if isinstance(it,dict) and it.get("@type")=="Person": p=it
    for x in soup(["script","style"]): x.decompose()
    t=soup.get_text(" ",strip=True)
    m=re.search(r"plays the ([^.]{3,80}?)\.",t)
    socials={}
    for a in soup.find_all("a",href=True):
        h=a["href"]
        for k,dom in [("instagram","instagram.com"),("x","x.com/"),("youtube","youtube.com")]:
            if dom in h and k not in socials and "ppatour" not in h.lower(): socials[k]=h
    out.append(dict(name=p.get("name") or s.replace("-"," ").title(),country=p.get("nationality",""),
        paddle=m.group(1).strip() if m else "",profile=url,image=p.get("image",""),socials=socials))
    print(out[-1]["name"],"|",out[-1]["country"],"|",out[-1]["paddle"])
json.dump(dict(retrieved=str(datetime.date.today()),source="ppatour.com athlete profiles",pros=out),open("data/pros.json","w"),indent=1,ensure_ascii=False)
