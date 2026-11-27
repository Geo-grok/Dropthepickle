#!/usr/bin/env python3
"""Trim the self-hosted Inter variable fonts to the weight range the site uses (400-800).

assets/fonts/fonts.css declares Inter only at 400, 600, 700 and 800 (each face points at the same
variable file), so the browser never renders Inter outside wght 400-800. The Google Fonts files carry
the full 100-900 axis; cutting it to 400-800 keeps every glyph, every OpenType feature and the same
unicode ranges, and makes the files ~23-29% smaller (inter-latin is preloaded on every page).
Outlines at 400/600/700/800 match the originals to within ~1.5/2048 em (sub-pixel).

Run once (idempotent: a file already at 400-800 is skipped). Needs: pip install fonttools brotli
"""
import pathlib
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT_DIR = pathlib.Path(__file__).resolve().parent.parent / "assets" / "fonts"
WGHT = (400, 800)

for name in ("inter-latin.woff2", "inter-latin-ext.woff2"):
    p = FONT_DIR / name
    f = TTFont(p)
    ax = next(a for a in f["fvar"].axes if a.axisTag == "wght")
    if (ax.minValue, ax.maxValue) == WGHT:
        print(f"{name}: already {WGHT}, skipped"); continue
    before = p.stat().st_size
    g = instancer.instantiateVariableFont(f, {"wght": WGHT}, updateFontNames=False)
    g.flavor = "woff2"
    g.save(p)
    print(f"{name}: wght {ax.minValue:g}-{ax.maxValue:g} -> {WGHT[0]}-{WGHT[1]}, {before} -> {p.stat().st_size} bytes")
