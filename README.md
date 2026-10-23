# DropThePickle: static pickleball hub

- `python3 update.py`: pulls news RSS, YouTube review RSS and the PPA events feed into `data/`, then runs `build.py` → `dist/`. If a source fails, the previous data is kept.
- `python3 update.py --no-fetch`: rebuild only.
- `python3 scripts/fetch_pros.py`: refresh pro facts from official PPA profiles (run weekly or monthly).
- `data/paddles.json`: hand-verified manufacturer specs. Edit it to add paddles (and include the source URL).
- `python3 scripts/check_links.py`: checks internal and external links. `scripts/screenshots.py`: takes 390px screenshots (needs a server on :8765 and `pip install playwright`).
- `scripts/track_prices.py`: maker-price check (robots-respecting) → `data/price_history.json`; run by `update.py`. Its `updated` date only moves when at least one price was verified.
- Daily refresh: the `daily` GitHub Action (`.github/workflows/daily.yml`, ~6 AM CT) runs `update.py` and commits the refreshed `data/` files to `main`. It does **not** publish the site: there is no deploy on push. The live site changes only when someone deploys `main` by hand with `npx wrangler deploy` (currently a daily publish around 9 AM CT). The push needs Actions "Read and write" workflow permissions; if it can't push, the job fails with an `::error` saying so.
- Price freshness wording: pages say "Prices last checked <date>" (paddle pages: "Maker price checked <date>") from `price_history.json`, never "today". The build adds "(checked recently)" only when the date is 2 or fewer days old, and "Prices may have changed since then." when it is more than 7. A small inline script (`FRESHJS` in `paddle_pages.py`) re-checks both in the visitor's browser against the real date, so pages that are not rebuilt or redeployed stop claiming freshness on their own. Without JS, the text is just the plain date plus the build-time note.
- `config.json`: SITE_NAME, AFFILIATE_TAG / AMAZON_ASSOCIATES_TAG, BRAND_AFFILIATE_PARAMS, SIGNUP_ENDPOINT, feed lists.

Setup: `pip install -r requirements.txt`. Cron: `0 6 * * * cd /path/pickleball-hub && python3 update.py >> update.log 2>&1`
Deploy (manual; nothing deploys on push): `npx wrangler deploy` from an up-to-date `main` publishes `src/worker.js` with `dist/` as static assets (`wrangler.jsonc`; missing paths serve `dist/404.html`). `POST /api/signup` stores the address in the D1 database `dtp-subscribers` (binding `DB`, id `fddb64c4-6f12-4af0-b6ec-aeaf902a70f0`). The `subscribers` table already exists. `migrations/0001_init.sql` matches it for a fresh database. Build command: `pip install -r requirements.txt && python3 update.py`.

## Link in bio (`links_page.py`)
- Bio URLs: TikTok `https://dropthepickle.com/links/tiktok`, Instagram `https://dropthepickle.com/links/instagram`. Generic: `https://dropthepickle.com/links` (utm_source=bio).
- Every button carries `utm_source=<platform>&utm_medium=social&utm_campaign=bio`. The hrefs are baked in per page, and a tiny inline script swaps the source when the URL has `?src=tiktok|instagram` (or `?utm_source=`). So `/links?src=tiktok` works too.
- "Latest video" is the newest `media/*.mp4` by git add date (falls back to `LATEST_VIDEO_FALLBACK` in a shallow checkout). Build fails if a bio page goes over 30KB. `/links` is in the sitemap and not in the nav; the platform copies are `noindex` with a canonical to `/links`.

## Paddle quiz (`paddle_quiz.py`)
- `/paddle-quiz`: 3 questions (level, budget, play style) → 3 picks. All 27 answer combos are scored at build time from `data/paddles.json` + `data/price_history.json`, `data/price-tracker.json`, `data/discount-codes.json` and the `/go/` map. The JSON is embedded in the page, and inline JS renders it. Answers live in the hash (`#skill=beginner&budget=100-200&style=all-court`) and also work as a query string.
- Prices are shown only when the tracker has one (with its checked date). Everything else says "See price". Six Zero (AUD) is never converted. Paddles marked unavailable and not in the tracker are left out.

## Sources, discovery & sponsors (added 2026-10-14)
- `data/sources.json`: living registry of sources (audience + where the number came from, RSS/API, robots/ToS). Entries with `in_pipeline: true` are pulled by `update.py` on top of the config lists (YouTube review channels, news RSS, podcast RSS → `data/podcasts.json`).
- `scripts/discover_sources.py` (weekly): appends candidates flagged `"new"` (YouTube via API if `YT_API_KEY` is set, else r/Pickleball links via Arctic Shift + oEmbed; Google News RSS; iTunes podcast search). Review them, then set `in_pipeline`. Cron: `0 7 * * 1 cd /path && python3 scripts/discover_sources.py && python3 scripts/report_sources.py`
- `scripts/report_sources.py` → `reports/sources_ranked.md`. `data/sponsors.json` + `reports/sponsors.md`: sponsor/advertiser prospects and ad-network thresholds.
- New pages: `creators.html`, `podcasts.html` (links/titles only).
