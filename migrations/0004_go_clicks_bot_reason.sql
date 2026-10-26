-- /go/<slug> bot labelling v2 (see botReasons/logClick in src/worker.js). Labels only; clicks are never blocked.
-- bot_reason: comma-joined labels written by the worker, NULL for clean clicks:
--   ua_bot (crawler/script UA), no_ua, ua_not_browser, ios13 (iPhone/iPad OS 13_x UA), no_referer,
--   burst (>= 3 clicks in 10 min from SG/BR/IN/GB, or >= 10 in 10 min from any other single country).
-- Not idempotent (ALTER TABLE ADD COLUMN): run once.
ALTER TABLE go_clicks ADD COLUMN bot_reason TEXT;
CREATE INDEX IF NOT EXISTS go_clicks_country_time ON go_clicks (country, created_at);

-- Reclassifies every row (old and new) with the v2 rules without modifying data.
-- burst here looks +/- 10 minutes around each click, so the first clicks of a burst are caught too
-- (the worker only sees earlier clicks at write time, so it labels from the 3rd/10th click on).
-- user_agent IS NULL is not treated as a bot here, because rows from before 0003 never stored a UA.
DROP VIEW IF EXISTS go_clicks_classified;
CREATE VIEW go_clicks_classified AS
WITH b AS (
  SELECT g.*,
    CASE WHEN g.country IS NULL THEN 0 ELSE (
      SELECT COUNT(*) FROM go_clicks h
      WHERE h.country = g.country
        AND julianday(h.created_at) BETWEEN julianday(g.created_at) - 10.0/1440 AND julianday(g.created_at) + 10.0/1440
    ) END AS burst_n
  FROM go_clicks g
), r AS (
  SELECT b.*,
    (b.user_agent LIKE '%OS 13\_%like Mac OS X%' ESCAPE '\'
       AND (b.user_agent LIKE '%iPhone%' OR b.user_agent LIKE '%iPad%' OR b.user_agent LIKE '%iPod%')) AS r_ios13,
    (b.referer_path IS NULL) AS r_no_referer,
    (b.burst_n >= CASE WHEN b.country IN ('SG','BR','IN','GB') THEN 3 ELSE 10 END) AS r_burst
  FROM b
)
SELECT id, slug, referer_path, country, created_at, user_agent, is_bot, bot_reason, burst_n,
  r_ios13, r_no_referer, r_burst,
  CASE WHEN is_bot = 1 OR r_ios13 OR r_no_referer OR r_burst THEN 1 ELSE 0 END AS is_bot_v2,
  NULLIF(trim(
    COALESCE(CASE WHEN is_bot = 1 THEN COALESCE(bot_reason, 'ua_bot') END, '')
    || CASE WHEN r_ios13 AND instr(COALESCE(bot_reason,''),'ios13') = 0 THEN ',ios13' ELSE '' END
    || CASE WHEN r_no_referer AND instr(COALESCE(bot_reason,''),'no_referer') = 0 THEN ',no_referer' ELSE '' END
    || CASE WHEN r_burst AND instr(COALESCE(bot_reason,''),'burst') = 0 THEN ',burst' ELSE '' END, ','), '') AS bot_reason_v2
FROM r;
