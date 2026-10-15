# DropThePickle: static pickleball hub

- `python3 update.py`: pulls news RSS, YouTube review RSS and the PPA events feed into `data/`, then runs `build.py` → `dist/`. If a source fails, the previous data is kept.
- `python3 update.py --no-fetch`: rebuild only.
- `python3 scripts/fetch_pros.py`: refresh pro facts from official PPA profiles (run weekly or monthly).
- `data/paddles.json`: hand-verified manufacturer specs. Edit it to add paddles (and include the source URL).
- `python3 scripts/check_links.py`: checks internal and external links. `scripts/screenshots.py`: takes 390px screenshots (needs a server on :8765 and `pip install playwright`).
- `scripts/track_prices.py`: daily maker-price check (robots-respecting) → `data/price_history.json`; run by `update.py`.
- `config.json`: SITE_NAME, AFFILIATE_TAG / AMAZON_ASSOCIATES_TAG, BRAND_AFFILIATE_PARAMS, SIGNUP_ENDPOINT, feed lists.

Setup: `pip install -r requirements.txt`. Cron: `0 6 * * * cd /path/pickleball-hub && python3 update.py >> update.log 2>&1`
Deploy: `npx wrangler deploy` publishes `dist/` as a Workers static-assets site (`wrangler.jsonc`; missing paths serve `dist/404.html`). Build command: `pip install -r requirements.txt && python3 update.py`.

## Sources, discovery & sponsors (added 2026-10-14)
- `data/sources.json`: living registry of sources (audience + where the number came from, RSS/API, robots/ToS). Entries with `in_pipeline: true` are pulled by `update.py` on top of the config lists (YouTube review channels, news RSS, podcast RSS → `data/podcasts.json`).
- `scripts/discover_sources.py` (weekly): appends candidates flagged `"new"` (YouTube via API if `YT_API_KEY` is set, else r/Pickleball links via Arctic Shift + oEmbed; Google News RSS; iTunes podcast search). Review them, then set `in_pipeline`. Cron: `0 7 * * 1 cd /path && python3 scripts/discover_sources.py && python3 scripts/report_sources.py`
- `scripts/report_sources.py` → `reports/sources_ranked.md`. `data/sponsors.json` + `reports/sponsors.md`: sponsor/advertiser prospects and ad-network thresholds.
- New pages: `creators.html`, `podcasts.html` (links/titles only).
