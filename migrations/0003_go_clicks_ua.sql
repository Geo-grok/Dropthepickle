-- /go/<slug> bot filtering (see handleGo in src/worker.js).
-- user_agent: raw User-Agent header (truncated to 512 chars by the worker), NULL if absent.
-- is_bot: 1 when the worker flags the hit as a crawler, link checker, preview fetcher or script.
-- Rows written before this migration keep is_bot = 0 and user_agent = NULL.
-- Real browser clicks: SELECT slug, COUNT(*) FROM go_clicks WHERE is_bot = 0 GROUP BY slug;
-- Not idempotent (SQLite has no ADD COLUMN IF NOT EXISTS): apply once via `wrangler d1 migrations apply`.
ALTER TABLE go_clicks ADD COLUMN user_agent TEXT;
ALTER TABLE go_clicks ADD COLUMN is_bot INTEGER DEFAULT 0;
