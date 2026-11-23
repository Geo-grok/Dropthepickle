-- /go/<slug> bot labelling v3: cross-country same-slug pairs (see logClick in src/worker.js).
-- pair_burst: the same slug clicked from two different countries within +/- 5 seconds.
-- Growth saw this as a homepage sweep (Nov 16-22): same paddle slug twice, ~2s apart,
-- Singapore plus another country (often Brazil), stored as is_bot = 0 because the
-- existing same-country burst rule did not catch it.
-- Labels only; clicks are never blocked or redirected differently.
-- The worker labels the later click at write time and best-effort back-flags the earlier
-- row. This view looks both ways, so the first click of a pair, simultaneous inserts,
-- and historical rows are flagged too. Keep 5 seconds in sync with PAIR_WINDOW_SEC
-- in src/worker.js.
-- Replaces the go_clicks_classified view from 0004 (same columns, plus r_pair_burst
-- folded into is_bot_v2 / bot_reason_v2). Not idempotent past the DROP/CREATE VIEW.
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
    (b.burst_n >= CASE WHEN b.country IN ('SG','BR','IN','GB') THEN 3 ELSE 10 END) AS r_burst,
    (b.country IS NOT NULL AND EXISTS (
      SELECT 1 FROM go_clicks p
      WHERE p.slug = b.slug
        AND p.id != b.id
        AND p.country IS NOT NULL
        AND p.country != b.country
        AND julianday(p.created_at) BETWEEN julianday(b.created_at) - 5.0/86400 AND julianday(b.created_at) + 5.0/86400
    )) AS r_pair_burst
  FROM b
)
SELECT id, slug, referer_path, country, created_at, user_agent, is_bot, bot_reason, burst_n,
  r_ios13, r_no_referer, r_burst, r_pair_burst,
  CASE WHEN is_bot = 1 OR r_ios13 OR r_no_referer OR r_burst OR r_pair_burst THEN 1 ELSE 0 END AS is_bot_v2,
  NULLIF(trim(
    COALESCE(CASE WHEN is_bot = 1 THEN COALESCE(bot_reason, 'ua_bot') END, '')
    || CASE WHEN r_ios13 AND instr(COALESCE(bot_reason,''),'ios13') = 0 THEN ',ios13' ELSE '' END
    || CASE WHEN r_no_referer AND instr(COALESCE(bot_reason,''),'no_referer') = 0 THEN ',no_referer' ELSE '' END
    || CASE WHEN r_burst AND instr(COALESCE(bot_reason,''),'burst') = 0 THEN ',burst' ELSE '' END
    || CASE WHEN r_pair_burst AND instr(COALESCE(bot_reason,''),'pair_burst') = 0 THEN ',pair_burst' ELSE '' END, ','), '') AS bot_reason_v2
FROM r;
