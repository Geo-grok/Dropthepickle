#!/usr/bin/env python3
"""Render data/*.json + config.json into a static site in dist/."""
import json, pathlib, shutil, html, urllib.parse, datetime, re, hashlib
ROOT = pathlib.Path(__file__).parent; DIST = ROOT / "dist"
C = json.loads((ROOT / "config.json").read_text())
def D(n):
    p = ROOT / "data" / n
    return json.loads(p.read_text()) if p.exists() else {"items": []}
e = lambda s: html.escape(str(s or ""), quote=True)
NAV = [("index.html","Home"),("tournaments.html","Tournaments"),("reviews.html","Reviews"),("buzz.html","Buzz"),
       ("pros.html","Pros"),("pro-paddles.html","Pro paddles"),("creators.html","Creators"),("podcasts.html","Podcasts"),("compare.html","Compare"),("shop.html","Merch"),("community.html","Marketplace")]
CSS = r"""
:root{--navy:#0b1630;--navy2:#111d36;--navy3:#16264a;--neon:#c6f432;--neon2:#a8d61c;--warm:#ff7a45;--ink:#0d1526;--mut:#4a5878;--bg:#f4f6fa;--card:#fff;--line:#e3e8f0;--r:18px;--sh:0 1px 2px rgba(11,20,38,.06),0 8px 24px rgba(11,20,38,.08);--sh2:0 2px 4px rgba(11,20,38,.08),0 18px 40px rgba(11,20,38,.16)}
*{box-sizing:border-box}html{scroll-behavior:smooth;overflow-x:hidden;max-width:100%}
body{margin:0;font:16px/1.6 Inter,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:var(--ink);background:var(--bg);-webkit-font-smoothing:antialiased;overflow-x:hidden;max-width:100%}
a{color:#2453c7;text-underline-offset:3px}img{max-width:100%;height:auto;display:block}
h1,h2,h3,.display{font-family:Oswald,"Bebas Neue",Impact,sans-serif;letter-spacing:.01em;line-height:1.1;text-transform:uppercase}
h1{font-size:clamp(2rem,5vw,3.2rem);margin:.4rem 0 .6rem;font-weight:700}
h2{font-size:clamp(1.4rem,3vw,1.9rem);margin:2.4rem 0 1rem;font-weight:700;display:flex;align-items:center;flex-wrap:wrap;gap:.6rem;scroll-margin-top:5rem}
h2::before{content:"";width:6px;height:1.1em;background:var(--neon);border-radius:3px;box-shadow:0 0 0 2px var(--navy) inset}
h3{font-size:1.15rem;margin:.2rem 0 .4rem;font-weight:600;text-transform:none;font-family:Inter,system-ui,sans-serif;letter-spacing:-.01em;line-height:1.3}
h3 a{color:inherit;text-decoration:none}h3 a:hover{color:#2453c7}
.meta{color:var(--mut);font-size:.94rem}.note{font-size:.94rem;color:var(--mut)}
/* header */
header{position:sticky;top:0;z-index:50;background:#0b1630;border-bottom:1px solid rgba(255,255,255,.06)}
.bar{display:flex;align-items:center;flex-wrap:nowrap;gap:.75rem;max-width:1200px;margin:auto;padding:.4rem 1.1rem}
.logo{display:flex;align-items:center;gap:.45rem;text-decoration:none;line-height:1;flex:none;min-width:0;color:#fff}
.logo picture{display:block;line-height:0;flex:none}
.logo img{width:60px;height:60px;max-width:none;border-radius:50%;object-fit:cover;flex:none}
.logo b{font-family:Anton,Impact,sans-serif;font-weight:400;font-size:32px;letter-spacing:.02em;color:#fff;white-space:nowrap;line-height:1}
.logo b span{color:#7cff4f}
.nav{display:flex;gap:.1rem;margin-left:auto;align-items:center;min-width:0;overflow-x:auto;scrollbar-width:none}.nav::-webkit-scrollbar{display:none}
.nav a{color:#c9d3e6;text-decoration:none;padding:.45rem .55rem;border-radius:10px;font-size:.94rem;font-weight:600;white-space:nowrap;transition:.2s}
.nav a:hover{color:#fff;background:rgba(255,255,255,.07)}.nav a.on{color:var(--navy);background:var(--neon)}
.join{margin-left:.4rem}
.burger{display:none;margin-left:auto;background:none;border:0;width:42px;height:42px;border-radius:10px;cursor:pointer;color:#fff}
.burger span{display:block;width:22px;height:2px;background:#fff;margin:5px auto;border-radius:2px;transition:.3s}
.navopen .burger span:nth-child(1){transform:translateY(7px) rotate(45deg)}.navopen .burger span:nth-child(2){opacity:0}.navopen .burger span:nth-child(3){transform:translateY(-7px) rotate(-45deg)}
@media(max-width:1320px){.burger{display:block;flex:none}.join{display:inline-flex;flex:none;white-space:nowrap}
 .nav{position:fixed;inset:80px 0 auto 0;flex-direction:column;align-items:stretch;background:var(--navy);padding:.8rem 1rem 1.4rem;gap:.2rem;transform:translateY(-120%);transition:transform .35s cubic-bezier(.2,.8,.2,1);box-shadow:0 20px 40px rgba(0,0,0,.35);max-height:calc(100vh - 80px);overflow:auto}
 .nav a{font-size:1.05rem;padding:.75rem 1rem}.navopen .nav{transform:none}}
/* always-visible primary tabs (pills) */
.bar{min-height:60px;padding-top:0;padding-bottom:0}.logo img{width:40px;height:40px}
.btn.join{white-space:nowrap;font-size:16px;font-weight:800;padding:10px 14px;flex:none}
.tabs{display:flex;gap:8px;max-width:1200px;margin:auto;padding:4px 16px 12px;overflow-x:auto;scrollbar-width:none;background:#0b1630}.tabs::-webkit-scrollbar{display:none}
.tabs a{flex:none;display:flex;align-items:center;min-height:44px;padding:10px 16px;border-radius:999px;font:700 16px/1 Inter,system-ui,sans-serif;color:#e6ecf5;text-decoration:none;background:#16264a;white-space:nowrap}
.tabs a:hover{background:#1f3360}.tabs a.on{background:#c6f432;color:#0b1630}
/* homepage: navy frame, hero strip, Top 5 */
.topwrap{background:#0b1630;padding:16px 0 20px}.topwrap .in{max-width:760px;margin:auto}
.hstrip{display:flex;gap:14px;align-items:center;margin:0 16px 16px;padding:16px;border-radius:16px;background:#16264a;max-height:150px;box-sizing:border-box;overflow:hidden}
.hstrip .dill{flex:none;width:76px;height:76px;border-radius:50%;background:#c6f432;display:grid;place-items:center;overflow:hidden}.hstrip .dill img{width:68px;height:68px;border-radius:50%}
.hstrip h1{margin:0;font:800 22px/1.15 Inter,system-ui,sans-serif;color:#fff;letter-spacing:0;text-transform:none}.hstrip h1 em{font-style:normal;color:#c6f432}
.hstrip p{margin:4px 0 0;color:#d5deeb;font-size:15px;line-height:1.3}.hstrip .eyebrow,.hstrip .updated{display:none}
.topwrap h2{color:#fff;margin:0 16px 12px;font-size:22px}.topwrap h2::before{display:none}.topwrap .seemore{color:#c6f432;font-size:16px}
.top5{list-style:none;margin:0;padding:0}
.top5 li{display:flex;gap:14px;padding:14px;margin:0 16px 12px;background:#fff;border-radius:16px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
.top5 .th{flex:none;position:relative;width:84px;height:84px;border-radius:12px;background:#e8edf6;overflow:hidden;display:grid;place-items:center}.top5 .th img,.top5 .th svg{width:100%;height:100%;object-fit:cover}
.top5 .rk{position:absolute;top:4px;left:4px;min-width:26px;height:26px;border-radius:999px;background:#0b1630;color:#c6f432;display:grid;place-items:center;font:800 15px/1 Inter,sans-serif}
.top5 .bd{min-width:0;flex:1}.top5 h3{margin:0 0 4px;font:800 18px/1.25 Inter,system-ui,sans-serif;color:#0b1630}.top5 h3 a{color:#0b1630;text-decoration:none}
.top5 .fr{font-size:15px;color:#4a5878;margin:0 0 6px}
.top5 .px{font-size:20px;font-weight:800;color:#0b1630;display:flex;flex-wrap:wrap;align-items:center;gap:6px}.top5 .px s{color:#6b7a99;font-weight:600;font-size:16px}
.top5 .off{background:#c6f432;color:#0b1630;font-size:14px;font-weight:800;padding:3px 8px;border-radius:6px}
.top5 .go{display:inline-flex;margin-top:8px;min-height:44px;padding:10px 16px;font-size:16px}
.topwrap .more{margin:4px 16px 0;color:#d5deeb;font-size:15px}.topwrap .more a{color:#c6f432;font-weight:700}
/* buttons, badges */
.btn{display:inline-flex;align-items:center;gap:.45rem;background:var(--neon);color:var(--navy);font-weight:800;padding:.8rem 1.25rem;border-radius:12px;text-decoration:none;border:0;cursor:pointer;font-size:.98rem;transition:transform .15s,box-shadow .2s,background .2s;box-shadow:0 6px 18px rgba(198,244,50,.28)}
.btn:hover{transform:translateY(-2px);background:#d4ff45;box-shadow:0 10px 26px rgba(198,244,50,.4)}
.btn.ghost{background:transparent;color:#fff;box-shadow:inset 0 0 0 2px rgba(255,255,255,.35)}.btn.ghost:hover{box-shadow:inset 0 0 0 2px var(--neon);color:var(--neon)}
.btn.sm{padding:.45rem .85rem;font-size:.94rem;border-radius:10px}.btn.warm{background:var(--warm);color:#fff;box-shadow:0 6px 18px rgba(255,122,69,.3)}
.tag,.badge{display:inline-flex;align-items:center;gap:.25rem;font-size:.94rem;font-weight:800;letter-spacing:0;text-transform:uppercase;padding:.22rem .55rem;border-radius:6px;background:#eef2f8;color:var(--navy3);vertical-align:middle}
.b-sale{background:var(--warm);color:#fff}.b-drop{background:var(--neon);color:var(--navy)}.b-power{background:#ffe1d3;color:#b23d0c}.b-control{background:#dde8ff;color:#1d3f9a}.b-out{background:#eee;color:#777}.b-pub{background:var(--navy);color:var(--neon)}
/* layout */
main{max-width:1200px;margin:auto;padding:1.4rem 1.1rem 3rem}
.grid{display:grid;gap:1.1rem;grid-template-columns:repeat(auto-fill,minmax(min(270px,100%),1fr));min-width:0}
.card{position:relative;background:var(--card);border-radius:var(--r);padding:1.15rem;box-shadow:var(--sh);border:1px solid var(--line);transition:transform .25s cubic-bezier(.2,.8,.2,1),box-shadow .25s;overflow:hidden}
.card:hover{transform:translateY(-4px);box-shadow:var(--sh2)}
.card ul{padding-left:1.1rem;margin:.4rem 0}.card li{margin:.25rem 0}
.disc{background:linear-gradient(90deg,#fff7e6,#fffdf5);border:1px solid #ffe0a8;padding:.7rem .9rem;border-radius:12px;font-size:.94rem;margin:.6rem 0}
/* video cards */
.vid{position:relative;padding-top:56.25%;border-radius:12px;overflow:hidden;background:#000;margin:-.2rem -.2rem .7rem}.vid iframe{position:absolute;inset:0;width:100%;height:100%;border:0}
.thumb{position:relative;display:block;margin:-1.15rem -1.15rem .85rem;aspect-ratio:16/9;background:var(--navy) center/cover no-repeat;overflow:hidden}
.thumb img{width:100%;height:100%;object-fit:cover;transition:transform .5s}.card:hover .thumb img{transform:scale(1.05)}
.thumb::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 50%,rgba(11,20,38,.55))}
.play{position:absolute;z-index:2;left:50%;top:50%;width:58px;height:58px;margin:-29px;border-radius:50%;background:rgba(198,244,50,.95);display:grid;place-items:center;box-shadow:0 8px 24px rgba(0,0,0,.35);transition:transform .2s}.card:hover .play{transform:scale(1.1)}
.play::before{content:"";border-left:16px solid var(--navy);border-top:10px solid transparent;border-bottom:10px solid transparent;margin-left:4px}
.chan{position:absolute;z-index:2;left:.7rem;bottom:.6rem;color:#fff;font-size:.94rem;font-weight:700}
/* hero */
.hero{position:relative;overflow:hidden;background:radial-gradient(1200px 500px at 85% -10%,rgba(198,244,50,.18),transparent 60%),radial-gradient(800px 400px at -10% 110%,rgba(255,122,69,.22),transparent 60%),linear-gradient(160deg,#0b1426 0%,#132550 100%);color:#fff;margin:0 0 0}
.hero .court{position:absolute;inset:0;width:100%;height:100%;opacity:.16}
.hero .in{position:relative;max-width:1200px;margin:auto;padding:clamp(3rem,9vw,6.5rem) 1.1rem clamp(3rem,8vw,5.5rem);display:grid;gap:2rem;grid-template-columns:1.25fr .9fr;align-items:center}
.hero h1{font-size:clamp(2.7rem,8vw,5.6rem);line-height:.95;margin:.6rem 0 1rem;font-family:"Bebas Neue",Oswald,Impact,sans-serif;font-weight:400;letter-spacing:.01em}
.hero h1 em{font-style:normal;color:var(--neon);text-shadow:0 0 40px rgba(198,244,50,.35)}
.hero p{color:#c9d3e6;font-size:clamp(1rem,2vw,1.18rem);max-width:560px;margin:0 0 1.6rem}
.eyebrow{display:inline-flex;gap:.5rem;align-items:center;font-size:.94rem;font-weight:800;letter-spacing:0;text-transform:uppercase;color:var(--neon);background:rgba(198,244,50,.1);border:1px solid rgba(198,244,50,.3);padding:.35rem .7rem;border-radius:99px}
.eyebrow i{width:8px;height:8px;border-radius:50%;background:var(--neon);box-shadow:0 0 0 0 rgba(198,244,50,.6);animation:pulse 2s infinite}
@keyframes pulse{70%{box-shadow:0 0 0 10px rgba(198,244,50,0)}100%{box-shadow:0 0 0 0 rgba(198,244,50,0)}}
.ctas{display:flex;flex-wrap:wrap;gap:.7rem}
.stats{display:flex;gap:1.6rem;margin-top:2rem;flex-wrap:wrap}.stats b{display:block;font-family:Oswald,sans-serif;font-size:1.9rem;color:#fff;line-height:1}.stats span{font-size:.94rem;color:#d5deeb;text-transform:uppercase;letter-spacing:0}
.heroart{position:relative;justify-self:center;width:min(380px,80vw);aspect-ratio:1;animation:float 6s ease-in-out infinite}
@keyframes float{50%{transform:translateY(-12px) rotate(2deg)}}
@media(max-width:820px){.hero .in{grid-template-columns:1fr}.heroart{display:none}}
.phero{background:linear-gradient(160deg,#0b1426,#162a57);color:#fff;border-radius:24px;padding:clamp(1.2rem,4vw,2.4rem);display:grid;grid-template-columns:minmax(0,.9fr) minmax(0,1.1fr);gap:clamp(1rem,4vw,2.5rem);align-items:center;position:relative;overflow:hidden;box-shadow:var(--sh2);margin:.4rem 0 1.4rem}
.phero h1{color:#fff;margin-top:.3rem}.phero .meta{color:#a9b6cf}.phero .meta a{color:var(--neon)}
.phero .img{background:radial-gradient(circle at 50% 40%,#fff,#e9eef7);border-radius:20px;aspect-ratio:1;display:grid;place-items:center;padding:1rem;overflow:hidden;min-width:0;max-width:100%}
.phero .img img{width:100%;height:100%;max-width:100%;max-height:100%;min-width:0;min-height:0;object-fit:contain;transform:none;filter:drop-shadow(0 18px 24px rgba(0,0,0,.25))}
.price{font-family:Oswald,sans-serif;font-size:2.4rem;font-weight:700;line-height:1;color:var(--neon)}.price s{font-size:1.1rem;color:#8796b3;margin-left:.4rem;font-weight:400}
@media(max-width:720px){.phero{grid-template-columns:1fr}}
.pagehead{background:linear-gradient(160deg,#0b1426,#162a57);color:#fff;border-radius:24px;padding:clamp(1.4rem,4vw,2.6rem);margin:.4rem 0 1.2rem;position:relative;overflow:hidden;box-shadow:var(--sh2)}
.pagehead h1{color:#fff;margin:0 0 .5rem}.pagehead p,.pagehead .meta{color:#b5c1d8;margin:.3rem 0;max-width:820px}.pagehead a{color:var(--neon)}
.pagehead::after{content:"";position:absolute;right:-60px;top:-60px;width:220px;height:220px;border-radius:50%;background:radial-gradient(circle,rgba(198,244,50,.35),transparent 70%)}
/* paddle cards */
.pcard{display:flex;flex-direction:column;padding:0;min-width:0;max-width:100%}.pcard .pimg{background:radial-gradient(circle at 50% 35%,#fff,#eef2f8);aspect-ratio:4/3;display:grid;place-items:center;padding:1rem;position:relative;overflow:hidden;min-width:0;max-width:100%}
.pcard .pimg img{width:100%;height:100%;max-width:100%;max-height:100%;min-width:0;min-height:0;object-fit:contain;transform:none;filter:drop-shadow(0 10px 14px rgba(0,0,0,.15))}
.pcard .badges{position:absolute;top:.7rem;left:.7rem;display:flex;gap:.3rem;flex-wrap:wrap}
.pcard .body{padding:1rem 1.1rem 1.15rem;display:flex;flex-direction:column;gap:.35rem;flex:1}
.pcard .pp{font-family:Oswald,sans-serif;font-size:1.5rem;font-weight:700}.pcard .pp s{font-size:.95rem;color:var(--mut);font-weight:400;margin-left:.3rem}
.pcard .brand{font-size:.94rem;font-weight:800;letter-spacing:0;text-transform:uppercase;color:var(--mut)}
.credit{font-size:.94rem;color:#94a0b5;position:absolute;right:.6rem;bottom:.4rem}
.rail{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(250px,1fr);gap:1.1rem;overflow-x:auto;scroll-snap-type:x mandatory;padding:.3rem .2rem 1rem;scrollbar-width:thin}
.rail>*{scroll-snap-align:start}
@media(min-width:1100px){.rail{grid-auto-columns:calc(25% - .83rem)}}
/* tables */
.tbl{overflow-x:auto;border-radius:16px;border:1px solid var(--line);box-shadow:var(--sh);background:#fff}
table{width:100%;border-collapse:collapse;font-size:.94rem}th,td{padding:.75rem .9rem;border-bottom:1px solid var(--line);text-align:left;vertical-align:top}
tr:last-child td,tr:last-child th{border-bottom:0}thead th,tr:first-child th:not([scope]){background:var(--navy);color:#fff;font-family:Oswald,sans-serif;text-transform:uppercase;letter-spacing:0;font-weight:500}
tr:first-child th a{color:var(--neon)}tbody tr:hover{background:#f8faff}
.vs td.win{background:linear-gradient(90deg,rgba(198,244,50,.25),rgba(198,244,50,.08));font-weight:700;position:relative}
.vs td.win::after{content:"✓ edge";margin-left:.4rem;font-size:.94rem;font-weight:800;color:var(--navy);background:var(--neon);padding:.08rem .4rem;border-radius:5px;text-transform:uppercase}
.vs th[scope=row]{background:#f4f6fa;color:var(--navy3);width:22%}
.vshead{display:grid;grid-template-columns:minmax(0,1fr) auto minmax(0,1fr);gap:1rem;align-items:center;text-align:center}
.vshead .vsimg{background:#fff;border-radius:18px;aspect-ratio:1;display:grid;place-items:center;padding:.8rem;max-width:min(220px,100%);margin:auto;overflow:hidden;min-width:0}
.vshead .vsimg img{width:100%;height:100%;max-width:100%;max-height:100%;min-width:0;min-height:0;object-fit:contain;transform:none}
.vsbadge{font-family:"Bebas Neue",Oswald,sans-serif;font-size:2.4rem;width:68px;height:68px;border-radius:50%;background:var(--neon);color:var(--navy);display:grid;place-items:center;box-shadow:0 0 0 6px rgba(198,244,50,.2)}
.vshead h3{color:#fff;margin-top:.6rem}
/* tournaments strip, news, sections */
.strip{display:grid;grid-auto-flow:column;grid-auto-columns:minmax(260px,1fr);gap:1rem;overflow-x:auto;padding-bottom:.6rem}
.tcard{background:var(--navy2);color:#fff;border:1px solid rgba(255,255,255,.08)}.tcard h3{color:#fff}.tcard .meta{color:#a9b6cf}.tcard a{color:var(--neon)}
.date{display:inline-flex;flex-direction:column;align-items:center;justify-content:center;width:58px;height:62px;border-radius:12px;background:var(--neon);color:var(--navy);font-family:Oswald,sans-serif;line-height:1;float:right;margin:0 0 .4rem .6rem}.date b{font-size:1.5rem}.date small{font-size:.94rem;font-weight:700;text-transform:uppercase}
.band{background:var(--navy);color:#fff;border-radius:26px;padding:clamp(1.4rem,4vw,2.6rem);margin:2.6rem 0 0;position:relative;overflow:hidden}
.band h2{color:#fff;margin-top:0}.band p{color:#b5c1d8}.band .meta{color:#d5deeb}
.dark{background:var(--navy);color:#fff;margin:2.4rem -1.1rem 0;padding:1rem 1.1rem 2.6rem}
.dark h2{color:#fff}.dark .meta{color:#a9b6cf}
.dark .in{max-width:1200px;margin:auto;padding:0 1.1rem}
.newscard .pub{margin-bottom:.5rem}
.seemore{font-weight:700;text-decoration:none;font-size:.94rem;margin-left:auto;font-family:Inter,sans-serif;text-transform:none;letter-spacing:0;color:#2453c7}.dark .seemore{color:var(--neon)}
.pros{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:.8rem}
.pro{display:flex;gap:.8rem;align-items:center;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:.8rem;box-shadow:var(--sh);transition:.2s}.pro:hover{transform:translateY(-3px)}
.pro .av{width:44px;height:44px;flex:none;border-radius:50%;background:var(--navy);color:var(--neon);display:grid;place-items:center;font-family:Oswald,sans-serif;font-weight:700}
.grid.proscons{grid-template-columns:repeat(auto-fit,minmax(270px,1fr))}.proscons .card:first-child{border-top:4px solid var(--neon)}.proscons .card:last-child{border-top:4px solid var(--warm)}
/* forms */
form{display:flex;flex-wrap:wrap;gap:.6rem;margin:.6rem 0;position:relative}.hp{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
input[type=email]{padding:.85rem 1rem;border-radius:12px;border:1px solid rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff;font-size:1rem;flex:1;min-width:min(220px,100%);max-width:380px}
main input[type=email]{border-color:var(--line);background:#fff;color:var(--ink)}.band input[type=email]{border-color:rgba(255,255,255,.2);background:rgba(255,255,255,.08);color:#fff}
input::placeholder{color:#d5deeb}
/* footer */
footer{background:#070d1a;color:#d5deeb;padding:3rem 1.1rem 2rem;font-size:.94rem}
.fin{max-width:1200px;margin:auto;display:grid;grid-template-columns:minmax(0,1.3fr) repeat(4,minmax(0,1fr));gap:1.4rem}
footer h4{color:#fff;font-family:Oswald,sans-serif;text-transform:uppercase;letter-spacing:0;margin:0 0 .7rem;font-size:.95rem}
footer a{color:#c9d3e6;text-decoration:none;display:block;margin:.3rem 0}footer a:hover{color:var(--neon)}
.legal{max-width:1200px;margin:2rem auto 0;padding-top:1.2rem;border-top:1px solid rgba(255,255,255,.08);font-size:.94rem}
@media(max-width:980px){.fin{grid-template-columns:1fr 1fr}.fin>div:first-child{grid-column:1/-1}}
@media(max-width:700px){.logo{gap:.32rem}.logo img{width:52px;height:52px}.logo b{font-size:26px}}
@media(max-width:520px){.tcard .date{float:none;margin:0 0 .6rem}.stats{gap:.75rem 1rem}.stats b{font-size:1.45rem}.hero h1{font-size:2.35rem}.bar{padding:.3rem .5rem;gap:.35rem}.burger{width:36px}.btn.join{margin-left:.15rem}.nav{inset:66px 0 auto 0;max-height:calc(100vh - 66px)}}
.faq{background:#fff;border:1px solid var(--line);border-radius:14px;padding:.85rem 1rem;margin:.45rem 0;box-shadow:var(--sh)}.faq summary{font-weight:800;cursor:pointer}.faq p{margin:.45rem 0 0}
.vgrid{display:grid;gap:1rem;grid-template-columns:repeat(auto-fill,minmax(min(240px,100%),1fr))}
.vgrid .vid.short{padding-top:177.78%;margin:0 0 .7rem}
.socials{display:flex;flex-wrap:wrap;gap:.5rem;margin:.8rem 0 1.2rem}
.spot{display:grid;gap:1rem;grid-template-columns:minmax(0,220px) minmax(0,1fr);align-items:center}
@media(max-width:640px){.spot{grid-template-columns:1fr}}
.spot img{width:100%;border-radius:14px;background:#0b1426}
.dill{display:flex;gap:1rem;align-items:center;background:#fff;border:1px solid var(--line);border-radius:18px;padding:1rem 1.15rem;box-shadow:var(--sh);margin:1.2rem 0}
.dill picture{flex:none;line-height:0}
.dill img{width:88px;height:88px;max-width:none;border-radius:50%;object-fit:cover;background:#0b1426}
.dill h2{margin:0 0 .35rem;font-size:1.35rem}
.dill p{margin:0}
@media(max-width:520px){.dill{align-items:flex-start}.dill img{width:72px;height:72px}}
/* reveal */
.rv{opacity:0;transform:translateY(16px);transition:opacity .6s,transform .6s cubic-bezier(.2,.8,.2,1)}.rv.in{opacity:1;transform:none}
@media(prefers-reduced-motion:reduce){*{animation:none!important;transition:none!important}.rv{opacity:1;transform:none}}
.secs{grid-template-columns:repeat(auto-fill,minmax(200px,1fr))}.secs a{text-decoration:none;color:inherit}
.tbl table td a{font-weight:600}
.codes-best{display:flex;flex-wrap:wrap;gap:.5rem;margin:.6rem 0 1rem}.codes-best a{background:var(--navy);color:var(--neon);text-decoration:none;font-weight:800;padding:.5rem .8rem;border-radius:99px;font-size:.94rem}
.cbrand{margin-top:1.8rem}.ccard{display:flex;flex-direction:column;gap:.55rem}.ccard .cdisc{font-family:Anton,Impact,sans-serif;font-size:2rem;line-height:1;color:var(--navy);letter-spacing:.01em}
.ccard .ccond{color:var(--mut);font-size:.95rem;margin:0}.crow{display:flex;gap:.5rem;align-items:stretch}
.ccode{flex:1;min-width:0;font-family:ui-monospace,Menlo,Consolas,monospace;font-size:1.35rem;font-weight:800;letter-spacing:0;background:var(--navy);color:var(--neon);border:2px dashed var(--neon);border-radius:12px;padding:.85rem .7rem;cursor:pointer;text-align:center;overflow-wrap:anywhere;min-height:56px}
.ccopy{min-width:88px;min-height:56px;font-size:1rem}.ccopy.ok{background:#fff;color:var(--navy);box-shadow:inset 0 0 0 2px var(--navy)}
.ccard .cshop{font-weight:800;color:var(--navy);font-size:1rem;padding:.35rem 0}.ccard .cmeta{font-size:.94rem;color:var(--mut)}.ccard .cmeta a{color:var(--mut)}
.codewarn{background:#fff8e6;border:1px solid #f3d27a;border-radius:12px;padding:.8rem 1rem;color:#5a4300;font-size:.95rem}
.b-unconf{background:#ffe1d3;color:#b23d0c;border:1px solid #ff7a45}.b-conf{background:#e6f9c2;color:#3b5a00}
.buzzcard .srcs{font-size:.94rem;margin:.5rem 0 0}.buzzcard .srcs a{margin-right:.6rem}
.buzzx{margin:.6rem 0}.buzzx .twitter-tweet{margin:.5rem 0!important}

"""
# Always-visible primary tabs (mobile-first). Codes uses the clean /discount-codes URL.
TABS = [("deals.html","Deals"),("/discount-codes","Codes"),("paddles.html","Paddles"),("guides.html","Guides"),("news.html","News")]
TAB_ON = {"/discount-codes": ("discount-codes.html",), "guides.html": ("guides.html", "guides/"), "paddles.html": ("paddles.html", "paddle-")}
# Central outbound map for /go/<slug>. build() fills it; write_go_map() saves src/go-links.json for the Worker.
GO = {}
GO_FILE = pathlib.Path(__file__).parent / "src" / "go-links.json"
def go_slug(url):
    for s, v in GO.items():
        if v["url"] == url: return s
    u = urllib.parse.urlparse(url)
    host = u.netloc.replace("www.", "").split(".")[0]
    last = [x for x in u.path.split("/") if x][-1:] or ["home"]
    base = re.sub(r"[^a-z0-9]+", "-", f"{host}-{last[0]}".lower()).strip("-")[:60].strip("-")
    s, i = base, 2
    while s in GO: s, i = f"{base}-{i}", i + 1
    GO[s] = {"url": url}
    return s
GO_A = re.compile(r'<a ([^>]*?)href="(https?://[^"]+)"([^>]*)>')
def golinks(doc):
    """Route outbound deal and shop links (rel=sponsored, or the Shop-brand links on codes) through /go/<slug>."""
    def sub(m):
        attrs = m.group(1) + m.group(3)
        if 'rel="sponsored' not in attrs and 'class="cshop"' not in attrs: return m.group(0)
        url = html.unescape(m.group(2))
        if "dropthepickle.com" in url: return m.group(0)
        return f'<a {m.group(1)}href="/go/{go_slug(url)}"{m.group(3)}>'
    return GO_A.sub(sub, doc)
def write_go_map():
    old = {}
    if GO_FILE.exists():
        try: old = json.loads(GO_FILE.read_text()).get("links", {})
        except Exception: old = {}
    links = {s: {"url": v["url"], "affiliate_tag": (old.get(s) or {}).get("affiliate_tag", "")} for s, v in sorted(GO.items())}
    GO_FILE.write_text(json.dumps({"_note": "slug -> destination. affiliate_tag is an optional query string (e.g. ref=dtp) the Worker appends. Leave empty until joined.", "links": links}, indent=1) + "\n")
def logo_html(rel):
    """Round Mic Drop avatar plus a live text wordmark. The wide logo image stays out of the header."""
    return (f'<picture><source srcset="{rel("avatar.webp")}" type="image/webp">'
            f'<img src="{rel("avatar.png")}" alt="Big Dill, the DropThePickle mascot" width="60" height="60"></picture>'
            f'<b>DROPTHE<span>PICKLE</span></b>')
PADDLE_SVG = '''<svg viewBox="0 0 200 260" width="70%" aria-label="Paddle illustration"><defs><linearGradient id="pg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#18284a"/><stop offset="1" stop-color="#0b1426"/></linearGradient></defs><rect x="40" y="10" width="120" height="160" rx="52" fill="url(#pg)"/><rect x="48" y="18" width="104" height="144" rx="46" fill="none" stroke="#c6f432" stroke-width="3" opacity=".7"/><path d="M60 120 L140 60" stroke="#ff7a45" stroke-width="6" stroke-linecap="round" opacity=".85"/><rect x="88" y="168" width="24" height="80" rx="8" fill="#0b1426"/><rect x="88" y="190" width="24" height="6" fill="#c6f432"/><rect x="88" y="208" width="24" height="6" fill="#c6f432"/><circle cx="150" cy="40" r="16" fill="#c6f432"/></svg>'''
COURT = '''<svg class="court" viewBox="0 0 1200 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true"><g fill="none" stroke="#c6f432" stroke-width="3"><rect x="120" y="70" width="960" height="460"/><line x1="600" y1="70" x2="600" y2="530"/><line x1="460" y1="70" x2="460" y2="530"/><line x1="740" y1="70" x2="740" y2="530"/><line x1="120" y1="300" x2="460" y2="300"/><line x1="740" y1="300" x2="1080" y2="300"/></g><g stroke="#fff" stroke-width="2" stroke-dasharray="6 10" opacity=".6"><line x1="600" y1="40" x2="600" y2="560"/></g></svg>'''
HEROART = '''<svg class="heroart" viewBox="0 0 400 400" aria-hidden="true"><defs><radialGradient id="ballg" cx=".35" cy=".3"><stop offset="0" stop-color="#eaff8a"/><stop offset=".6" stop-color="#c6f432"/><stop offset="1" stop-color="#8db511"/></radialGradient><linearGradient id="pad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff9a6b"/><stop offset="1" stop-color="#ff5f2e"/></linearGradient></defs><g transform="rotate(-24 200 200)"><rect x="110" y="40" width="170" height="220" rx="76" fill="url(#pad)"/><rect x="122" y="52" width="146" height="196" rx="66" fill="none" stroke="#fff" stroke-width="3" opacity=".45"/><rect x="178" y="252" width="34" height="110" rx="12" fill="#0b1426"/><rect x="178" y="280" width="34" height="8" fill="#c6f432"/><rect x="178" y="304" width="34" height="8" fill="#c6f432"/></g><circle cx="300" cy="110" r="62" fill="url(#ballg)"/><g fill="#0b1426" opacity=".85"><circle cx="280" cy="85" r="7"/><circle cx="315" cy="78" r="6"/><circle cx="335" cy="110" r="7"/><circle cx="300" cy="112" r="7.5"/><circle cx="270" cy="120" r="6"/><circle cx="292" cy="145" r="6.5"/><circle cx="325" cy="140" r="5.5"/></g><g stroke="#c6f432" stroke-width="4" stroke-linecap="round" opacity=".5"><line x1="210" y1="150" x2="150" y2="170"/><line x1="220" y1="120" x2="170" y2="125"/></g></svg>'''

FOOTCOLS = [("Explore",[("tournaments.html","Tournaments"),("reviews.html","Paddle reviews"),("news.html","News"),("buzz.html","Buzz"),("podcasts.html","Podcasts"),("creators.html","Creators"),("creators/ryan-morneau.html","Ryan Morneau")]),
            ("Learn",[("guides/how-to-choose-a-paddle.html","Choose a paddle"),("guides/best-paddles-under-100.html","Under $100 guide"),("guides/pickleball-rules-for-beginners.html","Rules"),("guides/how-to-dink.html","How to dink"),("guides/paddle-weight-and-core.html","Weight and core")]),
            ("Gear",[("paddles.html","Paddle database"),("compare.html","Compare paddles"),("deals.html","Deals"),("discount-codes.html","Discount codes"),("price-index.html","Price index"),("pro-paddles.html","Pro paddles"),("best-paddles-under-100.html","Under $100")]),
            ("Company",[("about.html","About"),("disclosure.html","Affiliate disclosure"),("privacy.html","Privacy"),("community.html","Join the community")])]
# Last content-change date per page. A date is recorded only when `fresh` differs from the hash stored in data/page_dates.json.
_PREV, _NEXT, CATALOG = {}, {}, {}
def canon(fn):
    base = C["BASE_URL"].rstrip("/")
    return base + "/" if fn == "index.html" else f"{base}/{fn}"
def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()
def note_fresh(fn, payload):
    """Return an ISO date only when this page's data changed since the last build. The first time we see a payload is a baseline, not a change."""
    if payload is None: return None
    h = fingerprint(payload); _NEXT[fn] = h
    prev = _PREV.get(fn)
    if prev and prev.get("hash") == h: return prev.get("updated")
    if prev: return datetime.date.today().isoformat()
    return None
def save_fresh():
    store = {}
    for fn, h in sorted(_NEXT.items()):
        prev = _PREV.get(fn)
        if prev and prev.get("hash") == h: updated = prev.get("updated")
        elif prev: updated = datetime.date.today().isoformat()
        else: updated = None
        store[fn] = {"hash": h, "updated": updated}
    (ROOT / "data" / "page_dates.json").write_text(json.dumps(store, indent=1, sort_keys=True) + "\n")
def publish_brand():
    """Copy Mic Drop files into dist. Header logo and favicons are the generated sizes; originals stay under /brand/."""
    brand = ROOT / "assets" / "brand"
    web = ROOT / "assets"
    (DIST / "brand").mkdir(parents=True, exist_ok=True)
    for p in brand.iterdir():
        if p.is_file(): shutil.copyfile(p, DIST / "brand" / p.name)
    for name in ("icon-512.png", "og-1200x630.png", "dtp-avatar.png"):
        shutil.copyfile(brand / name, DIST / name)
    for name in ("logo-full.png", "logo-full.webp", "avatar.png", "avatar.webp", "favicon.ico", "favicon-32.png", "apple-touch-icon.png"):
        shutil.copyfile(web / name, DIST / name)
def publish_media():
    """Public video files. Not linked from any page."""
    src = ROOT / "media"
    if not src.is_dir(): return
    dest = DIST / "media"
    dest.mkdir(parents=True, exist_ok=True)
    for p in src.iterdir():
        if p.is_file(): shutil.copyfile(p, dest / p.name)
def crumbs_for(fn, title, url):
    base = C["BASE_URL"].rstrip("/") + "/"
    home = {"name": "Home", "url": base}
    if fn == "index.html": return [home]
    crumbs = [home]
    if fn.startswith("events/"): crumbs.append({"name": "Tournaments", "url": base + "tournaments.html"})
    elif fn.startswith("guides/"): crumbs.append({"name": "Guides", "url": base + "guides/how-to-choose-a-paddle.html"})
    elif fn.startswith("creators/"): crumbs.append({"name": "Creators", "url": base + "creators.html"})
    elif fn.startswith("paddle-") or fn == "price-index.html": crumbs.append({"name": "Paddles", "url": base + "paddles.html"})
    elif fn.startswith(("vs-", "best-")): crumbs.append({"name": "Compare", "url": base + "compare.html"})
    crumbs.append({"name": title, "url": url})
    return crumbs
def ld_graph(title, desc, url, crumbs, updated, extra):
    base = C["BASE_URL"].rstrip("/")
    org, site = base + "/#organization", base + "/#website"
    web = {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": title, "description": desc,
           "isPartOf": {"@id": site}, "publisher": {"@id": org}, "breadcrumb": {"@id": url + "#breadcrumb"}, "inLanguage": "en"}
    if updated: web["dateModified"] = updated
    graph = [
        {"@type": "Organization", "@id": org, "name": C["SITE_NAME"], "url": base + "/", "email": C["CONTACT_EMAIL"],
         "description": C["TAGLINE"], "logo": {"@type": "ImageObject", "url": base + "/brand/logo-full.png", "width": 2000, "height": 800}},
        {"@type": "WebSite", "@id": site, "name": C["SITE_NAME"], "url": base + "/", "description": C["TAGLINE"],
         "publisher": {"@id": org}, "inLanguage": "en"},
        web,
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i, "name": c["name"], "item": c["url"]} for i, c in enumerate(crumbs, 1)]},
    ]
    graph.extend(n for n in (extra or []) if n)
    return {"@context": "https://schema.org", "@graph": graph}
def emit_crawl_files():
    base = C["BASE_URL"].rstrip("/")
    save_fresh()
    pages = [CATALOG[fn] for fn in CATALOG if fn != "404.html"]
    pages.sort(key=lambda p: (p["fn"] != "index.html", p["fn"]))
    urls = []
    for p in pages:
        last = f"\n    <lastmod>{p['updated']}</lastmod>" if p.get("updated") else ""
        urls.append(f"  <url>\n    <loc>{html.escape(canon(p['fn']))}</loc>{last}\n  </url>")
    (DIST / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(urls) + "\n</urlset>\n")
    bots = ["*", "GPTBot", "ChatGPT-User", "OAI-SearchBot", "Google-Extended", "GoogleOther", "anthropic-ai", "ClaudeBot",
            "Claude-SearchBot", "PerplexityBot", "Perplexity-User", "CCBot", "Bytespider", "Applebot-Extended", "Amazonbot",
            "meta-externalagent", "FacebookBot", "cohere-ai", "Diffbot", "AI2Bot", "DuckAssistBot", "MistralAI-User"]
    (DIST / "robots.txt").write_text("\n".join(f"User-agent: {b}\nAllow: /\nDisallow: /go/\n" for b in bots) + f"\nSitemap: {base}/sitemap.xml\n")
    def bullet(p): return f"- [{p['title']}]({canon(p['fn'])}): {p['desc']}"
    main_names = {"index.html", "tournaments.html", "reviews.html", "news.html", "buzz.html", "pros.html", "pro-paddles.html", "creators.html", "podcasts.html", "paddles.html", "compare.html", "deals.html", "discount-codes.html"}
    mains = [p for p in pages if p["fn"] in main_names]
    guides = [p for p in pages if p["fn"].startswith(("guides/", "creators/"))]
    paddles = [p for p in pages if p["fn"].startswith(("paddle-", "vs-", "best-"))]
    rest = [p for p in pages if p not in mains and p not in paddles and p not in guides]
    llms = [f"# {C['SITE_NAME']}", "", f"> {C['TAGLINE']}", "",
            f"{C['SITE_NAME']} is all things pickleball, free for everyone: news, paddles, prices, pros, tournaments, videos and guides, all in one place. It lists pro tournament dates, manufacturer paddle specs, maker prices, news headlines, beginner guides, and links to creator videos and podcasts. Specs and prices come from the makers. This site does not publish its own ratings or reviews.",
            "", "## Main", *[bullet(p) for p in mains], "", "## Guides", *[bullet(p) for p in guides], "", "## Paddles", *[bullet(p) for p in paddles], "", "## Optional", *[bullet(p) for p in rest], ""]
    (DIST / "llms.txt").write_text("\n".join(llms))
def pagehead(body):
    m = re.match(r'(<h1>.*?</h1>)((?:<p class="(?:meta|disc)">.*?</p>)*)', body, re.S)
    if not m: return body
    parts = re.findall(r'<p class="(meta|disc)">(.*?)</p>', m.group(2), re.S)
    head = m.group(1) + "".join(f'<p>{t}</p>' for k, t in parts if k == "meta")
    disc = "".join(f'<p class="disc">{t}</p>' for k, t in parts if k == "disc")
    return f'<section class="pagehead">{head}</section>{disc}' + body[m.end():]
def page(fn, title, body, desc="", full=False, *, fresh=None, schema=None, crumbs=None, image=None):
    prefix = "../" * fn.count("/")
    rel = lambda h: h if h.startswith(("http://", "https://", "mailto:", "#", "/")) else prefix + h
    nav = "".join(f'<a href="{rel(h)}" class="{"on" if h==fn else ""}">{t}</a>' for h, t in NAV)
    tabs = "".join(f'<a href="{rel(h)}"{" class=" + chr(34) + "on" + chr(34) + " aria-current=" + chr(34) + "page" + chr(34) if any(fn.startswith(x) for x in TAB_ON.get(h, (h,))) else ""}>{t}</a>' for h, t in TABS)
    n = C["SITE_NAME"]
    mark = logo_html(rel)
    doc_title = f"{title} · {n}"
    if not desc: desc = f"{title} on {n}: {C['TAGLINE']}."
    url = canon(fn)
    updated = note_fresh(fn, fresh)
    img = C["BASE_URL"].rstrip("/") + "/og-1200x630.png"
    stamp = f'<p class="meta updated">Updated {fmt(updated)}</p>' if updated else ""
    if not full: body = f"<main>{pagehead(body)}{stamp}</main>"
    elif stamp: body = body.replace('<span class="eyebrow"><i></i>Updated daily</span>', f'<span class="eyebrow"><i></i>Updated daily</span>{stamp}', 1)
    ld = json.dumps(ld_graph(doc_title, desc, url, crumbs or crumbs_for(fn, title, url), updated, schema), ensure_ascii=False).replace("<", "\\u003c")
    cols = "".join(f'<div><h4>{h}</h4>{"".join(f"<a href={chr(34)}{rel(u)}{chr(34)}>{t}</a>" for u, t in ls)}</div>' for h, ls in FOOTCOLS)
    doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(doc_title)}</title><meta name="description" content="{e(desc)}"><meta name="theme-color" content="#0b1426">
<meta property="og:type" content="website"><meta property="og:site_name" content="{e(n)}"><meta property="og:title" content="{e(doc_title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}"><meta property="og:image" content="{e(img)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Drop the Pickle">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(doc_title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{e(img)}">
<link rel="icon" href="{rel("favicon.ico")}" sizes="48x48"><link rel="icon" type="image/png" href="{rel("favicon-32.png")}" sizes="32x32"><link rel="apple-touch-icon" href="{rel("apple-touch-icon.png")}" sizes="180x180"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bebas+Neue&family=Inter:wght@400;600;700;800&family=Oswald:wght@500;700&display=swap">
<link rel="stylesheet" href="{rel("style.css")}"><link rel="canonical" href="{e(url)}"><link rel="sitemap" type="application/xml" title="Sitemap" href="{rel("sitemap.xml")}">
<script type="application/ld+json">{ld}</script></head>
<body><header><div class="bar"><a class="logo" href="{rel("index.html")}" aria-label="{e(n)} home">{mark}</a>
<button class="burger" aria-label="Menu" aria-expanded="false"><span></span><span></span><span></span></button><nav class="nav">{nav}</nav><a class="btn sm join" href="{rel("community.html")}#signup">Join free</a></div><nav class="tabs" aria-label="Main sections">{tabs}</nav></header>
{body}
<footer><div class="fin"><div><a class="logo" href="{rel("index.html")}" aria-label="{e(n)} home">{mark}</a><p>The all-in-one pickleball hub: tournaments, paddle reviews, deals, news and pro gear, refreshed daily from public sources.</p></div>{cols}</div>
<div class="legal">© {datetime.date.today().year} {e(n)}. Headlines, videos, product images and event info belong to their publishers and makers and link to the original source. Some links are affiliate links; as an Amazon Associate we may earn from qualifying purchases.</div></footer>
<script>
(()=>{{const b=document.querySelector('.burger');b.addEventListener('click',()=>{{const o=document.body.classList.toggle('navopen');b.setAttribute('aria-expanded',o)}});
if('IntersectionObserver'in window){{const io=new IntersectionObserver(es=>es.forEach(x=>{{if(x.isIntersecting){{x.target.classList.add('in');io.unobserve(x.target)}}}}),{{rootMargin:'0px 0px -40px 0px'}});
document.querySelectorAll('main .card,main .pro,.band').forEach(el=>{{el.classList.add('rv');io.observe(el)}})}}
document.querySelectorAll('form[action$="/api/signup"]').forEach(f=>f.addEventListener('submit',async ev=>{{ev.preventDefault();const btn=f.querySelector('button');if(btn)btn.disabled=true;let ok=false,msg="Thanks! You're on the list.";try{{const res=await fetch(f.action,{{method:'POST',body:new FormData(f),headers:{{Accept:'application/json'}}}});const data=await res.json().catch(()=>null);ok=!!(res.ok&&data&&data.ok);if(data&&data.message)msg=data.message;else if(!res.ok)msg='Something went wrong. Please try again.'}}catch(err){{msg='Could not reach the signup service. Please try again.'}}if(ok){{const p=document.createElement('p');p.textContent=msg;f.replaceWith(p)}}else{{if(btn)btn.disabled=false;let p=f.querySelector('.signup-msg');if(!p){{p=document.createElement('p');p.className='signup-msg meta';f.append(p)}}p.textContent=msg}}}}))}})()
</script>
<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{{"token": "8b857a29f29446008d526b7021a0eaa1"}}'></script>
</body></html>"""
    dest = DIST / fn
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(golinks(doc))
    CATALOG[fn] = {"fn": fn, "title": doc_title, "desc": desc, "updated": updated}

def buy(p):
    dom = urllib.parse.urlparse(p["buy_url"]).netloc.replace("www.", "")
    prm = C["BRAND_AFFILIATE_PARAMS"].get(dom, "")
    url = p["buy_url"] + (("&" if "?" in p["buy_url"] else "?") + prm if prm else "")
    out = f'<a href="{e(url)}" rel="sponsored nofollow noopener" target="_blank">{e(p["brand"])} store</a>'
    tag = C.get("AMAZON_ASSOCIATES_TAG") or C.get("AFFILIATE_TAG")
    if tag:
        q = urllib.parse.quote_plus(f'{p["brand"]} {p["model"]} pickleball paddle')
        out += f' · <a href="https://www.amazon.com/s?k={q}&tag={e(tag)}" rel="sponsored nofollow noopener" target="_blank">Amazon</a>'
    return out

def signup(src):
    ep = C.get("SIGNUP_ENDPOINT") or "/api/signup"
    return f'<form id="signup" action="{e(ep)}" method="post"><input type="hidden" name="source" value="{e(src)}"><input class="hp" type="text" name="website" tabindex="-1" autocomplete="off" aria-hidden="true"><input type="email" name="email" required maxlength="254" placeholder="you@email.com" aria-label="Email"><button class="btn">Notify me</button></form><p class="note">We\'ll only email DropThePickle updates. See our <a href="privacy.html">privacy policy</a>.</p>'

def fmt(d):
    try: return datetime.date.fromisoformat(d).strftime("%b %d, %Y")
    except Exception: return e(d)

def build():
    global _PREV, _NEXT, CATALOG
    _NEXT, CATALOG = {}, {}
    try: _PREV = json.loads((ROOT / "data" / "page_dates.json").read_text())
    except Exception: _PREV = {}
    if DIST.exists(): shutil.rmtree(DIST)
    DIST.mkdir(); (DIST / "style.css").write_text(CSS); publish_brand(); publish_media()
    T, R, N, P = D("tournaments.json"), D("reviews.json"), D("news.json"), D("pros.json")
    PD = json.loads((ROOT / "data/paddles.json").read_text())
    def dbadge(d):
        try: x = datetime.date.fromisoformat(d); return f'<span class="date"><b>{x.day}</b><small>{x:%b}</small></span>'
        except Exception: return ""
    def event_fn(t):
        return "events/" + re.sub(r"[^a-z0-9]+", "-", t["name"].lower()).strip("-") + ".html"
    def sports_event(t):
        """SportsEvent using only fields present on the tournament record."""
        ev = {"@type": "SportsEvent"}
        if t.get("name"): ev["name"] = t["name"]
        if t.get("start"): ev["startDate"] = t["start"]
        if t.get("end"): ev["endDate"] = t["end"]
        if t.get("link"): ev["url"] = t["link"]
        if t.get("location"): ev["location"] = {"@type": "Place", "name": t["location"]}
        if t.get("source"): ev["organizer"] = {"@type": "Organization", "name": t["source"]}
        if t.get("tickets"): ev["offers"] = {"@type": "Offer", "url": t["tickets"]}
        return ev
    tcard = lambda t: f'<div class="card tcard">{dbadge(t["start"]) if t.get("start") else ""}<span class="tag b-pub">{e(t["source"])}</span><h3><a href="{event_fn(t)}">{e(t["name"])}</a></h3><div class="meta">{(fmt(t["start"]) + " – " + fmt(t["end"])) if t.get("start") and t.get("end") else ""}{(" · " + e(t["location"])) if t.get("location") else ""}</div><p><a href="{e(t["link"])}" target="_blank" rel="noopener">Official event page</a>{(" · <a href="+chr(34)+e(t["tickets"])+chr(34)+" target=_blank rel=noopener>Tickets</a>") if t.get("tickets") else ""}</p></div>'
    ncard = lambda n: f'<div class="card newscard"><div class="pub"><span class="tag b-pub">{e(n["source"])}</span></div><h3><a href="{e(n["link"])}" target="_blank" rel="noopener">{e(n["title"])}</a></h3><div class="meta">{e(n["summary"])}</div></div>'
    def rcard(v, embed=True):
        if not embed and v.get("video_id"):
            return f'<div class="card"><a class="thumb" href="{e(v["link"])}" target="_blank" rel="noopener" aria-label="Watch on YouTube"><img loading="lazy" src="https://i.ytimg.com/vi/{e(v["video_id"])}/hqdefault.jpg" alt=""><span class="play"></span><span class="chan">{e(v["channel"])}</span></a><h3><a href="{e(v["link"])}" target="_blank" rel="noopener">{e(v["title"])}</a></h3><div class="meta">{fmt(v["date"])} · <a href="{e(v["channel_url"])}" target="_blank" rel="noopener">{e(v["channel"])}</a></div></div>'
        em = f'<div class="vid"><iframe loading="lazy" src="https://www.youtube-nocookie.com/embed/{e(v["video_id"])}" title="{e(v["title"])}" allowfullscreen></iframe></div>' if embed and v.get("video_id") else ""
        return f'<div class="card">{em}<h3><a href="{e(v["link"])}" target="_blank" rel="noopener">{e(v["title"])}</a></h3><div class="meta"><a href="{e(v["channel_url"])}" target="_blank" rel="noopener">{e(v["channel"])}</a> · {fmt(v["date"])}</div></div>'
    page("tournaments.html", "Tournaments", f'''<h1>Upcoming tournaments</h1><p class="meta">Pro events from the official <a href="https://www.ppatour.com/events/" target="_blank" rel="noopener">Carvana PPA Tour</a> event feed. Always confirm dates and sign up on the official page. Each card links to our event page, which only repeats fields from that feed.</p>
<div class="grid">{"".join(tcard(t) for t in T["items"]) or "<p>No events right now.</p>"}</div>
<h2>Find amateur tournaments near you</h2><p>These directories host signups for local and regional events (including West Texas). We link to them instead of copying their listings:</p>
<ul><li><a href="https://pickleballtournaments.com/" target="_blank" rel="noopener">PickleballTournaments.com</a></li><li><a href="https://www.pickleballbrackets.com/" target="_blank" rel="noopener">PickleballBrackets.com</a></li><li><a href="https://usapickleball.org/" target="_blank" rel="noopener">USA Pickleball</a> (sanctioned events)</li></ul>''',
         "Upcoming Carvana PPA Tour pro pickleball events with dates, cities and links to the official event pages.",
         fresh=[{k: t.get(k) for k in ("name", "start", "end", "location", "link", "tickets", "source")} for t in T["items"]],
         schema=[sports_event(t) for t in T["items"]])
    for t in T["items"]:
        bits = []
        if t.get("source"): bits.append(f'<p class="meta">{e(t["source"])}</p>')
        when = " – ".join(fmt(t[k]) for k in ("start", "end") if t.get(k))
        where = e(t["location"]) if t.get("location") else ""
        if when or where: bits.append(f'<p>{when}{(" · " + where) if where else ""}</p>')
        if t.get("link"): bits.append(f'<p><a class="btn" href="{e(t["link"])}" target="_blank" rel="noopener">Official event page</a></p>')
        if t.get("tickets"): bits.append(f'<p><a href="{e(t["tickets"])}" target="_blank" rel="noopener">Tickets</a></p>')
        bits.append('<p><a href="../tournaments.html">All tournaments</a></p>')
        loc = t.get("location") or ""
        when_desc = " – ".join(t[k] for k in ("start", "end") if t.get(k))
        desc_bits = [t["name"]]
        if t.get("source"): desc_bits.append(t["source"])
        if when_desc: desc_bits.append(when_desc)
        if loc: desc_bits.append(loc)
        page(event_fn(t), t["name"], f'<h1>{e(t["name"])}</h1>' + "".join(bits),
             ". ".join(desc_bits) + ".",
             fresh={k: t.get(k) for k in ("name", "start", "end", "location", "link", "tickets", "source")},
             schema=[sports_event(t)])
    page("reviews.html", "Paddle review roundup", f'<h1>Paddle review roundup</h1><p class="meta">The newest paddle videos from leading independent reviewers, pulled from their public YouTube feeds. All videos play on YouTube and belong to their creators. Go subscribe!</p><div class="grid">{"".join(rcard(v, False) for v in R["items"])}</div>',
         "Newest pickleball paddle videos from independent YouTube reviewers, with a link back to each creator's channel.",
         fresh=[{k: v.get(k) for k in ("channel", "title", "link", "date", "video_id")} for v in R["items"]])
    page("news.html", "Pickleball news", f'<h1>Pickleball news</h1><p class="meta">Headlines from public RSS feeds: {", ".join(e(s) for s in C["NEWS_FEEDS"])}. Click through to read on the publisher\'s site.</p><div class="grid">{"".join(ncard(n) for n in N["items"])}</div>',
         "Pickleball headlines from The Dink, Pickleball Union, Major League Pickleball, The Kitchen Pickle and Pickleball Kitchen.",
         fresh=[{k: n.get(k) for k in ("source", "title", "link", "date")} for n in N["items"]])
    # Pickleball Buzz (hand-curated data/buzz.json; update.py never writes it)
    B = D("buzz.json")
    def sbadge(b): return '<span class="tag b-unconf">⚠ Unconfirmed</span>' if b.get("status") != "confirmed" else '<span class="tag b-conf">Confirmed</span>'
    def bcard(b, full=True):
        srcs = " ".join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["label"])}</a>' for s in b.get("sources", []))
        emb = "".join(f'<blockquote class="twitter-tweet" data-dnt="true"><a href="{e(u)}">View post on X</a></blockquote>' for u in b.get("embeds", [])) if full else ""
        tags = " ".join(f'<span class="tag">{e(t)}</span>' for t in b.get("tags", [])) if full else ""
        return (f'<div class="card buzzcard"><div class="pub">{sbadge(b)} {tags}</div><h3>{e(b["title"])}</h3><div class="meta">{fmt(b.get("date"))}</div><p>{e(b["summary"])}</p>'
                f'<p class="srcs"><b>Sources:</b> {srcs}</p>{f"<div class={chr(34)}buzzx{chr(34)}>{emb}</div>" if emb else ""}</div>')
    BUZZ_TEASER = (f'<h2>Pickleball Buzz <a class="seemore" href="buzz.html">All buzz →</a></h2><div class="grid">{"".join(bcard(b, False) for b in B.get("items", [])[:3])}</div>') if B.get("items") else ""
    page("buzz.html", "Pickleball Buzz", f'<h1>Pickleball Buzz</h1><p class="meta">What the pickleball world is talking about (updated {e(B.get("updated",""))}). Items marked <b>Unconfirmed</b> are rumors or chatter with no official confirmation. Every item links to its sources; X posts are shown with X\'s official embeds.</p><div class="grid">{"".join(bcard(b) for b in B.get("items", [])) or "<p>No buzz right now.</p>"}</div><script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>',
         "Pickleball Buzz: what the pickleball world is talking about, with confirmed stories and clearly labeled rumors, each linked to its sources.",
         fresh={"updated": B.get("updated"), "items": [(b.get("title"), b.get("status"), b.get("date")) for b in B.get("items", [])]})
    rows = "".join(f'<tr><td><a href="{e(p["profile"])}" target="_blank" rel="noopener"><b>{e(p["name"])}</b></a></td><td>{e(p["country"])}</td><td>{e(p["paddle"])}</td><td>{" ".join(f"<a href={chr(34)}{e(u)}{chr(34)} target=_blank rel=noopener>{k}</a>" for k,u in p["socials"].items())}</td></tr>' for p in P.get("pros", []))
    page("pros.html", "Pro players", f'<h1>Top pro players</h1><p class="meta">Facts from each player\'s official PPA Tour profile (retrieved {e(P.get("retrieved"))}). Blank means the profile didn\'t list it.</p><div class="tbl"><table><tr><th>Player</th><th>Country</th><th>Paddle (per profile)</th><th>Socials</th></tr>{rows}</table></div>',
         "Country, paddle and social links for top pros, taken from each player's official PPA Tour profile.",
         fresh=[{k: p.get(k) for k in ("name", "country", "paddle", "profile", "socials")} for p in P.get("pros", [])])
    page("shop.html", "Merch", f'<h1>Merch shop</h1><div class="card"><h3>Coming soon 👕</h3><p>Shirts, hats and gear for dinkers. Get notified when we launch.</p>{signup("merch")}</div>',
         "DropThePickle merch is coming soon. Join the list to hear when shirts, hats and gear go on sale.")
    page("community.html", "Marketplace & forum", f'<h1>Marketplace & forum</h1><div class="grid"><div class="card"><h3>Used-paddle marketplace</h3><p>Buy and sell paddles and gear. Coming soon.</p></div><div class="card"><h3>Community forum</h3><p>Find partners, talk gear and swap tips. Coming soon.</p></div></div><h2>Be first in line</h2>{signup("community")}',
         "A used-paddle marketplace and community forum are on the way. Join the list to get in first.")
    page("about.html", "About", f'<h1>About {e(C["SITE_NAME"])}</h1><p>{e(C["SITE_NAME"])} is an independent pickleball hub started by a player and fitness fan in Midland, Texas. We gather tournaments, reviews, news and gear specs from public sources into one fast page, and always link back to the original.</p><p>We aren\'t affiliated with the PPA Tour, MLP, USA Pickleball or any brand listed. Every headline, video and event belongs to its publisher. The site is refreshed automatically each day. Spot an error? Email <a href="mailto:{e(C["CONTACT_EMAIL"])}">{e(C["CONTACT_EMAIL"])}</a>.</p><section class="dill"><picture><source srcset="avatar.webp" type="image/webp"><img src="avatar.png" alt="Big Dill, the DropThePickle mascot" width="88" height="88"></picture><div><h2>Meet Big Dill</h2><p>Big Dill is the Mic Drop pickle on the logo. He hangs around the deals, then gets out of the way. The site is still All Things Pickleball.</p></div></section>',
         "DropThePickle is an independent pickleball hub from Midland, Texas, linking tournaments, news and gear specs back to their sources.",
         fresh={"email": C["CONTACT_EMAIL"]})
    page("disclosure.html", "Affiliate disclosure", f'<h1>Affiliate disclosure</h1><p>{e(C["SITE_NAME"])} is reader-supported. Some links on this site, especially "where to buy" links in the paddle database, are <b>affiliate links</b>. If you click an affiliate link and buy something, we may earn a commission <b>at no extra cost to you</b>.</p><p>As an Amazon Associate, {e(C["SITE_NAME"])} earns from qualifying purchases. We may also take part in affiliate programs run by paddle brands and retailers.</p><p>Sponsored placements are clearly labeled <b>Sponsored</b>.</p><p>Editorial specs are never paid. Commissions and sponsorships do not change which products we list or the manufacturer specs we show. Specs come from the maker pages recorded in our data. We don\'t accept payment to add or alter a spec. Affiliate links are marked <code>rel="sponsored"</code>, and pages with them carry a notice near the top, in line with the U.S. FTC Endorsement Guides (16 CFR Part 255).</p>',
         "Affiliate links may earn a commission. Sponsored placements are labeled Sponsored. Editorial specs are never paid.")
    page("privacy.html", "Privacy policy", f'<h1>Privacy policy</h1><p class="meta">Effective October 15, 2026</p><h2>What we collect</h2><p>If you join the email list, your email is stored securely and used only for DropThePickle updates. We also store the page you signed up from, the time you signed up, and the country our host reports for that request. Unsubscribe on request at <a href="mailto:{e(C["CONTACT_EMAIL"])}">{e(C["CONTACT_EMAIL"])}</a>.</p><h2>Third parties</h2><p>Embedded YouTube videos use youtube-nocookie.com, but YouTube may still set cookies once you press play. Affiliate partners (such as Amazon) may use cookies to track referrals after you click a link. Our host may keep standard server logs.</p><p>We use Cloudflare Web Analytics, which is privacy-friendly and cookieless.</p><h2>Not sold</h2><p>We do not sell your personal information.</p><h2>Contact</h2><p>To ask about or delete your data, email <a href="mailto:{e(C["CONTACT_EMAIL"])}">{e(C["CONTACT_EMAIL"])}</a>.</p>',
         "Emails on the DropThePickle list are stored securely and used only for site updates. Unsubscribe on request at geolobo@mail.grokbot.com.",
         fresh={"email": C["CONTACT_EMAIL"], "effective": "2026-10-15", "list": "stored securely, DropThePickle updates only, unsubscribe on request", "analytics": "Cloudflare Web Analytics, cookieless"})
    # Creators & Podcasts directories from the living source registry (links only)
    SR = D("sources.json").get("sources", [])
    groups = [("Gear & paddle reviewers", lambda s: "review" in s.get("subtype","")), ("Coaches & instruction", lambda s: "instruction" in s.get("subtype","")),
              ("Pros", lambda s: s.get("subtype","").startswith("pro")), ("Media & entertainment", lambda s: s.get("subtype","") in ("media","entertainment","highlights","broadcast","podcast")),
              ("Health, fitness & PT", lambda s: "health" in s.get("subtype","")), ("Tours, leagues & orgs", lambda s: s.get("subtype","") in ("tour","league","governing body","ratings","brand"))]
    yts = [s for s in SR if s["type"] == "youtube" and s.get("flag") != "new"]
    def ccard(s):
        return f'<div class="card"><h3><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}</a></h3><div class="meta">YouTube · {e(s["audience"]["value"])} subscribers</div></div>'
    used, csecs = set(), ""
    for title, fn in groups:
        items = [s for s in yts if fn(s) and s["id"] not in used]
        used.update(s["id"] for s in items)
        if items: csecs += f'<h2>{title}</h2><div class="grid">{"".join(ccard(s) for s in items)}</div>'
    socials = [s for s in SR if s["type"] in ("x","instagram")]
    srow = "".join(f'<li><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}</a> on {"X" if s["type"]=="x" else "Instagram"} ({e(s["audience"]["value"])} followers)</li>' for s in socials)
    page("creators.html", "Pickleball creators directory", f'<h1>Pickleball creators</h1><p class="meta">The pickleball YouTubers, coaches, reviewers and pros worth following. Subscriber counts come from each public channel page (checked {e(D("sources.json").get("updated",""))}). We only link out, so go support them on their own channels.</p><div class="card spot"><a href="creators/ryan-morneau.html"><img src="https://i.ytimg.com/vi/Q7zUZLXK_gE/hqdefault.jpg" alt="The Most Important Singles Shots, a Pickleball Breakdowns clip"></a><div><span class="tag b-pub">Spotlight</span><h3><a href="creators/ryan-morneau.html">Ryan Morneau · Pickleball Breakdowns</a></h3><p>Match breakdowns and strategy tips. James Madison University reported him as the No. 1-ranked collegiate singles player. Six of his latest clips are embedded on his page.</p><p><a href="creators/ryan-morneau.html">Open the spotlight</a></p></div></div>{csecs}<h2>On X and Instagram</h2><ul>{srow}</ul>',
         "A directory of pickleball YouTubers, coaches, reviewers and pros, with a spotlight on Ryan Morneau's Pickleball Breakdowns channel.",
         fresh={"youtube": [(s["name"], s["url"], (s.get("audience") or {}).get("value")) for s in yts],
                "social": [(s["name"], s["url"], (s.get("audience") or {}).get("value")) for s in socials],
                "spotlight": "creators/ryan-morneau.html"})
    PC = D("podcasts.json")
    shows = [s for s in SR if s["type"] == "podcast" and s.get("flag") != "new"]
    latest = {}
    for ep in PC.get("items", []): latest.setdefault(ep["show"], []).append(ep)
    def pcard(s):
        eps = "".join(f'<li><a href="{e(x["link"])}" target="_blank" rel="noopener">{e(x["title"])}</a> <span class="meta">{fmt(x["date"])}</span></li>' for x in latest.get(s["name"], [])[:2])
        return f'<div class="card"><h3><a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}</a></h3><div class="meta">{e(s["audience"].get("episodes",""))} episodes · <a href="{e(s["feed"]["rss"])}" target="_blank" rel="noopener">RSS</a></div>{f"<ul>{eps}</ul>" if eps else ""}</div>'
    page("podcasts.html", "Pickleball podcasts", f'<h1>Pickleball podcasts</h1><p class="meta">Shows ordered by episode count, with their newest episodes pulled from each public podcast feed. Listen on the show\'s own page.</p><div class="grid">{"".join(pcard(s) for s in sorted(shows, key=lambda s: -(s["audience"].get("episodes") or 0)))}</div>',
         "Pickleball podcasts ordered by episode count, with the newest episodes pulled from each public show feed.",
         fresh={"shows": [(s["name"], s["url"], (s.get("audience") or {}).get("episodes")) for s in shows],
                "episodes": [(ep.get("show"), ep.get("title"), ep.get("date"), ep.get("link")) for ep in PC.get("items", [])]})

    # discount codes (data/discount-codes.json, refreshed by scripts/refresh-codes)
    DC = D("discount-codes.json"); codes = DC.get("codes", [])
    def slugb(b): return re.sub(r"[^a-z0-9]+", "-", b.lower()).strip("-")
    def score(c):
        m = re.search(r"(\d+)%", c["discount"]); n = re.search(r"\$(\d+)", c["discount"])
        return int(m.group(1)) if m else (int(n.group(1)) / 2 if n else 1)
    def ccard(c):
        cd = e(c["code"])
        exp = f' · Expires {fmt(c["expiry"])}' if c.get("expiry") else ""
        sd = f' (page dated {e(c["source_date"])})' if c.get("source_date") else ""
        return (f'<div class="card ccard"><div class="cdisc">{e(c["discount"])}</div><p class="ccond">{e(c["conditions"])}</p>'
                f'<div class="crow"><button class="ccode" data-code="{cd}" aria-label="Copy code {cd}">{cd}</button><button class="btn ccopy" data-code="{cd}">Copy</button></div>'
                f'<a class="cshop" href="{e(c["shop_url"])}" target="_blank" rel="noopener">Shop {e(c["brand"])} →</a>'
                f'<div class="cmeta">Last checked {fmt(c.get("verified"))}{exp} · Source: <a href="{e(c["source_url"])}" target="_blank" rel="noopener">{e(c["source"])}</a>{sd}</div></div>')
    brands = sorted({c["brand"] for c in codes}, key=str.lower)
    best = {}
    for c in codes:
        if c["brand"] not in best or score(c) > score(best[c["brand"]]): best[c["brand"]] = c
    jump = "".join(f'<a href="#{slugb(b)}">{e(b)} · {e(best[b]["discount"])}</a>' for b in brands)
    secs = "".join(f'<section class="cbrand" id="{slugb(b)}"><h2>{e(b)} codes</h2><div class="grid">{"".join(ccard(c) for c in sorted([c for c in codes if c["brand"]==b], key=lambda c: -score(c)))}</div></section>' for b in brands)
    nocode = "".join(f'<li><b>{e(b)}:</b> {e(t)}</li>' for b, t in DC.get("no_code", {}).items())
    copyjs = """<script>document.addEventListener('click',ev=>{const b=ev.target.closest('[data-code]');if(!b)return;const c=b.dataset.code,done=()=>{const k=b.parentNode.querySelector('.ccopy');if(k){k.textContent='Copied!';k.classList.add('ok');setTimeout(()=>{k.textContent='Copy';k.classList.remove('ok')},1800)}};if(navigator.clipboard)navigator.clipboard.writeText(c).then(done,done);else{const t=document.createElement('textarea');t.value=c;document.body.appendChild(t);t.select();document.execCommand('copy');t.remove();done()}});</script>"""
    page("discount-codes.html", "Pickleball Discount Codes & Paddle Coupons (Updated Daily)",
         f'<h1>Pickleball discount codes</h1><p class="meta">{len(codes)} working codes for {len(brands)} paddle brands and retailers. Every code is re-checked each day on the creator or brand page that publishes it. Codes that disappear get removed. Last checked: {fmt(DC.get("updated"))}.</p>'
         f'<p class="codewarn"><b>Heads up:</b> codes can expire or change without notice, and most brands allow one code per order (sale prices often beat a code). Check your cart total before you pay. We don\'t make up codes or post leaked ones.</p>'
         f'<p class="meta">Looking for price drops instead? See <a href="deals.html">Big Dill\'s paddle deals</a>.</p><h2>Best code per brand</h2><div class="codes-best">{jump}</div>{secs}'
         f'{f"<h2>No working code right now</h2><ul>{nocode}</ul>" if nocode else ""}<p class="disc">Codes are published by the creators and brands linked on each card. Many are affiliate codes, so the creator may earn a commission. DropThePickle doesn\'t earn anything from these codes. <a href="disclosure.html">Disclosure</a>.</p>{copyjs}',
         f"{len(codes)} pickleball discount codes and paddle coupons for {', '.join(brands[:8])} and more, re-checked daily. Tap to copy.",
         fresh={"codes": [(c["brand"], c["code"], c["discount"]) for c in codes]})
    import paddle_pages; paddle_pages.make(page, e, fmt, buy, D, C, PD, R, P, X=dict(tcard=tcard, ncard=ncard, rcard=rcard, signup=signup, T=T, N=N, BUZZ_TEASER=BUZZ_TEASER, COURT=COURT, HEROART=HEROART, PADDLE_SVG=PADDLE_SVG))
    page("404.html", "Page not found", f'''<h1>Out of bounds</h1><p class="meta">That page isn't on the court. The point is over.</p>
<p><a class="btn" href="index.html">Back to {e(C["SITE_NAME"])}</a></p>''', "That page isn't on the court. Head back to the DropThePickle hub.")
    emit_crawl_files()
    print("built", len(list(DIST.rglob("*.html"))), "pages ->", DIST)
build()
write_go_map()
