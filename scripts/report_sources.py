#!/usr/bin/env python3
"""Render data/sources.json -> reports/sources_ranked.md (ranked by audience; 'unknown' stays unknown)."""
import json, pathlib, re, collections
R = pathlib.Path(__file__).parent.parent
d = json.loads((R / "data/sources.json").read_text()); S = d["sources"]
def num(v):
    m = re.match(r"([\d.,]+)\s*([KM]?)", str(v or "").replace(",", ""))
    if not m: return None
    return float(m.group(1)) * {"K": 1e3, "M": 1e6, "": 1}[m.group(2)]
L = [f"# Pickleball sources ranked by audience\n", f"Registry: `data/sources.json` (updated {d['updated']}). {len(S)} sources.\n",
     "Audience numbers are public figures with their source. Different metrics are not comparable, so each type gets its own ranking. 'unknown' means no verifiable public number.\n",
     "## Counts by type\n", "| Type | Count | In site pipeline |", "|---|---|---|"]
c = collections.Counter(s["type"] for s in S); p = collections.Counter(s["type"] for s in S if s.get("in_pipeline"))
L += [f"| {t} | {n} | {p.get(t,0)} |" for t, n in c.most_common()]
L += ["", "## Top by followers/subscribers (YouTube, X, Instagram, Reddit)\n", "| # | Name | Platform | Audience | Source |", "|---|---|---|---|---|"]
soc = sorted([s for s in S if num(s["audience"]["value"]) and s["type"] in ("youtube","x","instagram","forum")], key=lambda s: -num(s["audience"]["value"]))
L += [f"| {i} | [{s['name']}]({s['url']}) | {s['type']} | {s['audience']['value']} | {s['audience']['source']} |" for i, s in enumerate(soc, 1)]
def section(title, typ, cols):
    rows = [s for s in S if s["type"] in typ]
    rows.sort(key=lambda s: (num(str(s["audience"]["value"]).replace("Tranco rank #","")) or 9e9) if "tranco" in s["audience"].get("metric","") else 9e9+ -(s["audience"].get("episodes") or 0))
    out = ["", f"## {title}\n", "| Name | Type | Audience | Feed/API | Robots / ToS | In pipeline |", "|---|---|---|---|---|---|"]
    for s in rows:
        a = s["audience"]; extra = f"; 3rd-party est. {a['third_party_estimate']['value']} ({a['third_party_estimate']['source']})" if a.get("third_party_estimate") else ""
        if s["type"] == "podcast": extra = f"; {a.get('episodes')} episodes"
        out.append(f"| [{s['name']}]({s['url']}) | {s['type']} | {a['value']} ({a['source']}){extra} | {s['feed'].get('rss') or '-'} / {s['feed'].get('api') or '-'} | {s['scraping']['robots']}; {s['scraping']['tos']} | {'yes' if s.get('in_pipeline') else 'no'} |")
    return out
L += section("Websites, tours, leagues, stats and retailers (ranked by Tranco)", [t for t in c if t not in ("youtube","x","instagram","podcast","forum")], None)
L += section("Podcasts (no public listener counts; by episode count)", ["podcast"], None)
new = [s for s in S if s.get("flag") == "new"]
L += ["", f"## New candidates from discover_sources.py ({len(new)})\n"] + [f"- [{s['name']}]({s['url']}) ({s['type']}, {s['audience']['value']}), found {s.get('added')}: {s.get('note','')}" for s in new]
(R / "reports").mkdir(exist_ok=True); (R / "reports/sources_ranked.md").write_text("\n".join(L) + "\n")
print("wrote reports/sources_ranked.md", len(S))
