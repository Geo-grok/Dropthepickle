"""/paddle-quiz: 'Find your paddle'. Three questions -> three picks, scored at build time from site data only:
data/paddles.json + data/price_history.json (the paddle data paddle_pages.py uses), data/price-tracker.json (verified
prices with checked dates), src/go-links.json (via the build's /go map) and data/discount-codes.json.
All 27 answer combos are precomputed here; the page's inline JS only reads the answers from the URL and renders."""
import json, re, datetime, itertools
SKILLS = [("beginner", "Beginner", "New or still learning the kitchen"), ("intermediate", "Intermediate", "Rallies, drops and dinks are coming"), ("advanced", "Advanced", "Tournament or 4.0+ level")]
BUDGETS = [("u100", "Under $100", "Keep it cheap"), ("100-200", "$100 to $200", "The sweet spot"), ("200plus", "$200+", "Show me the best")]
STYLES = [("control", "Control", "Soft hands, dinks and resets"), ("power", "Power", "Drives, put-aways, big serves"), ("all-court", "All-court", "A bit of everything")]
POWER_MODELS = ("Pressure X 8E", "LABS Project Boomstik", "Cannon XPP M1")  # same list paddle_pages.py uses for its Power badge

def cores(p): return [float(x) for x in re.findall(r"(\d+(?:\.\d+)?)\s*mm", p["core"])]
def norm(u): return (u or "").split("?")[0].rstrip("/").replace("://www.", "://")
def code_score(c):
    m = re.search(r"(\d+)%", c["discount"]); n = re.search(r"\$(\d+)", c["discount"])
    return int(m.group(1)) if m else (int(n.group(1)) / 2 if n else 1)

def bucket(v):
    return "u100" if v <= 100 else "100-200" if v <= 200 else "200plus"

def make(page, e, fmt, D, PD, go_slug, paddle_slug):
    PT = D("price-tracker.json"); DC = D("discount-codes.json"); H = D("price_history.json").get("paddles", {})
    tracker = {norm(r["url"]): r for r in PT.get("rows", [])}
    tracker.update({r["go"].rsplit("/", 1)[-1]: r for r in PT.get("rows", []) if r.get("go")})
    best = {}
    for c in DC.get("codes", []):
        if c["brand"] not in best or code_score(c) > code_score(best[c["brand"]]): best[c["brand"]] = c
    no_code = DC.get("no_code", {})
    paddles, skipped = [], []
    for p in PD["paddles"]:
        h = H.get(f'{p["brand"]} {p["model"]}', {})
        slug = go_slug(p["buy_url"])
        r = tracker.get(slug) or tracker.get(norm(p["buy_url"]))
        if h.get("available") is False and not r:
            skipped.append(f'{p["brand"]} {p["model"]}'); continue
        c = cores(p); s = (p.get("shape") or "").lower(); m = p["model"].lower()
        usd = r["current_price"] if r and r["currency"] == "USD" else (p["price"] if p["currency"] == "USD" else None)
        code = best.get(p["brand"])
        paddles.append({
            "brand": p["brand"], "model": p["model"], "go": f"/go/{slug}", "page": paddle_slug(p),
            "price": r["current_price"] if r else None, "cur": r["currency"] if r else p["currency"], "checked": r["checked"] if r else None,
            "list": p["price"], "list_cur": p["currency"], "usd": usd,
            "core": p["core"], "shape": p["shape"], "weight": p["weight"],
            "power": "power" in m or p["model"] in POWER_MODELS, "control": "control" in m,
            "c": c, "s": s, "m": m,
            "code": {k: code[k] for k in ("code", "discount", "conditions", "verified")} if code else None,
            "nocode": no_code.get(p["brand"], ""),
        })

    def score(x, skill, budget, style):
        c, s, pr = x["c"], x["s"], x["usd"]; mx = max(c) if c else 0; mn = min(c) if c else 0
        wide = any(k in s for k in ("hybrid", "widebody", "max", "xl"))
        elong_only = "elongated" in s and not wide
        pts = 0.0
        # budget
        if pr is None: pts -= 9 if budget == "u100" else 1  # non-USD maker price (Six Zero, AUD): no exchange-rate guessing
        else:
            b, want = bucket(pr), budget
            order = ["u100", "100-200", "200plus"]
            if b == want: pts += 4
            elif order.index(b) < order.index(want): pts += 1
            else: pts -= 6 + (pr - {"u100": 100, "100-200": 200}.get(want, pr)) / 25
        # skill
        if skill == "beginner":
            pts += 2 * (mx >= 16) + 2 * wide + (pr is not None and pr <= 150) - 2 * elong_only - (pr is not None and pr > 250)
        elif skill == "intermediate":
            pts += (16 in c) + (len(set(c)) > 1) + (pr is not None and 120 <= pr <= 230)
        else:
            pts += 2 * ("elongated" in s) + (bool(c) and mn <= 14.3) + (pr is not None and pr >= 199) + (" pro" in " " + x["m"] or "labs" in x["m"])
        # play style
        if style == "control":
            pts += 4 * x["control"] + 2 * (mx >= 16) + (mx >= 19) + ("hybrid" in s) - 3 * x["power"]
        elif style == "power":
            pts += 4 * x["power"] + 2 * ("elongated" in s) + (bool(c) and mn <= 14.3) - 3 * x["control"]
        else:
            pts += 3 * ("hybrid" in s) + 2 * (len(set(c)) > 1) + (16 in c) - x["power"] - x["control"]
        pts += 0.5 * (x["price"] is not None) + 0.5 * (x["code"] is not None)
        return pts

    def why(x, skill, budget, style):
        out, pr = [], x["usd"]
        if pr is None: out.append(f'Priced in {x["list_cur"]} on the maker site, so it may not fit a US budget exactly.')
        elif x["price"] is None:
            fit = "fits your budget" if bucket(pr) == budget else "is under your budget" if ["u100", "100-200", "200plus"].index(bucket(pr)) < ["u100", "100-200", "200plus"].index(budget) else "is over your budget"
            out.append(f'Maker list price ${pr:,.2f} (retrieved {PD.get("retrieved", "")}, not re-checked) {fit}.')
        elif bucket(pr) == budget: out.append("Fits your budget.")
        elif ["u100", "100-200", "200plus"].index(bucket(pr)) < ["u100", "100-200", "200plus"].index(budget): out.append("Comes in under your budget.")
        else: out.append(f"Closest fit, but over your budget.")
        if x["power"]: out.append("The maker markets it for power.")
        if x["control"]: out.append("The maker markets it for control.")
        specs = ", ".join(t for t in [x["core"] and f'{x["core"]} core', x["shape"] and f'{x["shape"]} shape', x["weight"]] if t)
        if specs: out.append(f"Maker specs: {specs}.")
        return out

    results = {}
    for (sk, _, _), (bu, _, _), (st, _, _) in itertools.product(SKILLS, BUDGETS, STYLES):
        ranked = sorted(range(len(paddles)), key=lambda i: (-score(paddles[i], sk, bu, st), paddles[i]["usd"] or 9999, paddles[i]["model"]))
        picks, brands = [], {}
        while len(picks) < 3:
            i = max((i for i in ranked if i not in picks), key=lambda i: (score(paddles[i], sk, bu, st) - 4 * brands.get(paddles[i]["brand"], 0), -ranked.index(i)))
            picks.append(i); brands[paddles[i]["brand"]] = brands.get(paddles[i]["brand"], 0) + 1
        results[f"{sk}|{bu}|{st}"] = [[i, why(paddles[i], sk, bu, st)] for i in picks]
    used = sorted({i for v in results.values() for i, _ in v})
    data = {"p": [{k: x[k] for k in ("brand", "model", "go", "page", "price", "cur", "checked", "list", "list_cur", "code", "nocode")} for x in paddles],
            "r": results, "retrieved": PD.get("retrieved", "")}
    blob = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")

    def qgroup(key, title, opts):
        btns = "".join(f'<button type="button" class="qopt" data-q="{key}" data-v="{v}" aria-pressed="false"><b>{e(t)}</b><small>{e(sub)}</small></button>' for v, t, sub in opts)
        return f'<fieldset class="qq" id="q-{key}"><legend>{title}</legend><div class="qopts">{btns}</div></fieldset>'
    css = """<style>
.qintro{display:flex;gap:14px;align-items:center;background:#0b1630;color:#fff;border-radius:18px;padding:16px;margin:0 0 18px}.qintro img{width:72px;height:72px;object-fit:cover;border-radius:50%;background:#c6f432;flex:none}.qintro p{margin:0;font-size:18px;font-weight:700;line-height:1.35}
.qq{border:0;margin:0 0 22px;padding:0}.qq legend{font:800 22px/1.2 Inter,system-ui,sans-serif;color:#0b1630;margin:0 0 10px;padding:0}
.qopts{display:grid;gap:10px;grid-template-columns:1fr}@media(min-width:720px){.qopts{grid-template-columns:repeat(3,1fr)}}
.qopt{display:block;width:100%;min-height:68px;text-align:left;padding:14px 18px;border-radius:16px;border:3px solid #16264a;background:#fff;color:#0b1630;font:inherit;cursor:pointer}
.qopt b{display:block;font-size:20px;font-weight:800}.qopt small{display:block;font-size:16px;color:#4a5878;margin-top:2px}
.qopt[aria-pressed=true]{background:#c6f432;border-color:#0b1630;box-shadow:0 0 0 3px #0b1630 inset}.qopt[aria-pressed=true] small{color:#16264a}
.qopt:focus-visible{outline:4px solid #2453c7;outline-offset:2px}
#qres{scroll-margin-top:130px}#qres[hidden]{display:none}.qhead{background:#0b1630;color:#fff;border-radius:18px;padding:16px 18px;margin:8px 0 14px}.qhead h2{color:#fff;margin:0 0 4px}.qhead p{margin:0;font-size:17px;color:#d5deeb}
.qpick{background:#fff;border-radius:18px;border:2px solid #e3e8f0;border-left:10px solid #c6f432;padding:16px 16px 18px;margin:0 0 14px;box-shadow:0 2px 10px rgba(11,20,38,.08)}
.qpick .rk{display:inline-block;background:#0b1630;color:#c6f432;font-weight:900;font-size:15px;padding:4px 10px;border-radius:999px;margin-bottom:6px}
.qpick h3{font:800 22px/1.2 Inter,system-ui,sans-serif;margin:2px 0 8px;color:#0b1630}.qpick h3 small{display:block;font-size:15px;font-weight:800;color:#4a5878;text-transform:uppercase}
.qprice{font-family:Anton,Impact,sans-serif;font-size:36px;line-height:1.05;color:#0b1630}.qprice.see{font-family:Inter,system-ui,sans-serif;font-size:24px;font-weight:900}
.qstamp{font-size:16px;font-weight:700;color:#16264a;margin:2px 0 8px}.qpick ul{margin:6px 0 10px;padding-left:20px;font-size:16px}.qpick li{margin:3px 0}
.qcode{display:flex;gap:8px;align-items:stretch;margin:10px 0}.qcode .ccode{font-size:20px}.qcmeta{font-size:15px;color:#4a5878;margin:0 0 10px}
.qgo{display:flex;justify-content:center;width:100%;min-height:58px;font-size:19px;margin-top:6px}.qspec{display:inline-block;margin-top:10px;font-weight:700;font-size:16px;padding:8px 0}
.qshare{display:grid;gap:10px;grid-template-columns:1fr 1fr;margin:16px 0}.qshare .btn{justify-content:center;min-height:56px;font-size:18px}.qshare .btn.alt{background:#0b1630;color:#fff;box-shadow:none}.qshare .btn[hidden]{display:none}.qshare .only{grid-column:1/-1}
.qmsg{font-weight:800;color:#3b5a00;min-height:1.4em;margin:0}
</style>"""
    shares = '<div class="qshare"><button type="button" class="btn" id="qcopy">🔗 Copy link</button><button type="button" class="btn alt" id="qnative" hidden>📤 Share</button></div><p class="qmsg" id="qmsg" role="status" aria-live="polite"></p><p><button type="button" class="btn ghost" id="qreset" style="color:#0b1630;box-shadow:inset 0 0 0 2px #0b1630;min-height:52px;font-size:17px">↺ Start over</button></p>'
    js = r"""<script>(()=>{const D=JSON.parse(document.getElementById('qdata').textContent),K=['skill','budget','style'],A={},L={skill:%s,budget:%s,style:%s};
const M=(v,c)=>(c==='AUD'?'A$':'$')+Number(v).toLocaleString('en-US',{minimumFractionDigits:2,maximumFractionDigits:2});
const day=d=>{try{return new Date(d+'T12:00:00').toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}catch(e){return d}};
const esc=s=>String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const res=document.getElementById('qres'),list=document.getElementById('qlist'),sum=document.getElementById('qsum'),msg=document.getElementById('qmsg');
function link(){return location.origin+location.pathname+'#'+K.map(k=>k+'='+A[k]).join('&')}
function mark(){document.querySelectorAll('.qopt').forEach(b=>b.setAttribute('aria-pressed',A[b.dataset.q]===b.dataset.v?'true':'false'))}
function card(i,why,n){const p=D.p[i];let price=p.price!=null?'<div class="qprice">'+M(p.price,p.cur)+'</div><div class="qstamp">✓ Checked '+day(p.checked)+' on '+esc(p.brand)+"'s site"+(p.cur==='AUD'?' · AUD':'')+'</div>':'<div class="qprice see">See price</div><div class="qstamp">Not in our price tracker yet. Tap through for today\'s price.</div>';
let code=p.code?'<div class="qcode"><button class="ccode" data-code="'+esc(p.code.code)+'" aria-label="Copy code '+esc(p.code.code)+'">'+esc(p.code.code)+'</button><button class="btn ccopy" data-code="'+esc(p.code.code)+'">Copy</button></div><p class="qcmeta"><b>'+esc(p.code.discount)+'</b> · '+esc(p.code.conditions)+' · code checked '+day(p.code.verified)+'</p>':'<p class="qcmeta">No working '+esc(p.brand)+' code right now. <a href="/discount-codes">See all codes</a></p>';
return '<article class="qpick"><span class="rk">Pick #'+n+'</span><h3><small>'+esc(p.brand)+'</small>'+esc(p.model)+'</h3>'+price+'<ul>'+why.map(w=>'<li>'+esc(w)+'</li>').join('')+'</ul>'+code+'<a class="btn qgo" href="'+esc(p.go)+'" rel="sponsored nofollow noopener" target="_blank">Shop '+esc(p.brand)+' →</a><a class="qspec" href="/'+esc(p.page.replace(/\.html$/,''))+'">Specs and reviews →</a></article>'}
function show(scroll){mark();if(!K.every(k=>A[k])){res.hidden=true;return}const r=D.r[K.map(k=>A[k]).join('|')];if(!r)return;
sum.textContent=L.skill[A.skill]+' · '+L.budget[A.budget]+' · '+L.style[A.style];list.innerHTML=r.map((x,j)=>card(x[0],x[1],j+1)).join('');res.hidden=false;
history.replaceState(null,'',link());if(scroll)res.scrollIntoView({behavior:'smooth',block:'start'})}
function next(k){const i=K.indexOf(k);for(let j=i+1;j<K.length;j++)if(!A[K[j]])return document.getElementById('q-'+K[j]).scrollIntoView({behavior:'smooth',block:'center'})}
document.addEventListener('click',ev=>{const b=ev.target.closest('.qopt');if(b){A[b.dataset.q]=b.dataset.v;const done=K.every(k=>A[k]);show(done);if(!done)next(b.dataset.q);return}
const c=ev.target.closest('[data-code]');if(c){const t=c.dataset.code,k=c.parentNode.querySelector('.ccopy'),ok=()=>{if(k){k.textContent='Copied!';k.classList.add('ok');setTimeout(()=>{k.textContent='Copy';k.classList.remove('ok')},1800)}};if(navigator.clipboard)navigator.clipboard.writeText(t).then(ok,ok);else ok()}});
document.getElementById('qcopy').addEventListener('click',()=>{const u=link(),ok=()=>{msg.textContent='Link copied. Paste it anywhere.'};if(navigator.clipboard)navigator.clipboard.writeText(u).then(ok,()=>prompt('Copy this link',u));else prompt('Copy this link',u)});
const nb=document.getElementById('qnative');if(navigator.share){nb.hidden=false}else{document.getElementById('qcopy').classList.add('only')}
nb.addEventListener('click',()=>navigator.share({title:'My paddle picks from Big Dill',text:'My 3 paddle picks ('+sum.textContent+'):',url:link()}).catch(()=>{}));
document.getElementById('qreset').addEventListener('click',()=>{K.forEach(k=>delete A[k]);res.hidden=true;msg.textContent='';history.replaceState(null,'',location.pathname+location.search);mark();document.getElementById('q-skill').scrollIntoView({behavior:'smooth'})});
function load(){const h=new URLSearchParams(location.hash.slice(1)),q=new URLSearchParams(location.search);K.forEach(k=>{const v=h.get(k)||q.get(k);if(v&&L[k][v])A[k]=v});show(false)}
window.addEventListener('hashchange',load);load()})()</script>""" % tuple(json.dumps({v: t for v, t, _ in o}) for o in (SKILLS, BUDGETS, STYLES))
    n_tracked = sum(1 for x in paddles if x["price"] is not None)
    body = (f'<h1>Find your paddle</h1><p class="meta">Three taps, three paddle picks. Prices come from our <a href="price-tracker.html">Paddle Price Tracker</a> with the date we checked. Codes come from our <a href="discount-codes.html">daily-checked discount codes</a>.</p>'
            f'{css}<div class="qintro"><picture><source srcset="avatar.webp" type="image/webp"><img src="avatar.png" alt="Big Dill, the DropThePickle mascot" width="72" height="72"></picture><p>Big Dill picks from {len(paddles)} paddles in our database. Answer 3 questions.</p></div>'
            + qgroup("skill", "1. What's your level?", SKILLS) + qgroup("budget", "2. What's your budget?", BUDGETS) + qgroup("style", "3. How do you like to play?", STYLES)
            + f'<section id="qres" hidden aria-live="polite"><div class="qhead"><h2>Your 3 picks</h2><p id="qsum"></p></div><div id="qlist"></div>{shares}</section>'
            f'<p class="disc">Picks are a spec match from maker data (core, shape, weight, how the maker markets it) and price. They are not lab or on-court test results. {n_tracked} of {len(paddles)} paddles have a verified tracker price; the rest say "See price". Budget fit uses the tracker price, or the maker list price (retrieved {e(PD.get("retrieved", ""))}) when we have no tracker price. Shop buttons may be affiliate links. <a href="disclosure.html">Disclosure</a>.</p>'
            f'<p class="meta">Want to dig in? <a href="paddles.html">Paddle database</a> · <a href="compare.html">Compare paddles</a> · <a href="best-paddles-for-beginners.html">Best for beginners</a></p>'
            f'<script type="application/json" id="qdata">{blob}</script>{js}')
    page("paddle-quiz.html", "Find your paddle: 3-question pickleball paddle quiz", body,
         "Answer 3 quick questions (level, budget, play style) and Big Dill picks 3 pickleball paddles with checked prices and working discount codes.",
         fresh={"r": results, "p": data["p"]})
    return {"paddles": len(paddles), "recommendable": len(used), "tracked": n_tracked, "skipped": skipped,
            "no_code": sorted({x["brand"] for x in paddles if not x["code"]}),
            "no_price": [f'{x["brand"]} {x["model"]}' for x in paddles if x["price"] is None],
            "used": [f'{paddles[i]["brand"]} {paddles[i]["model"]}' for i in used]}
