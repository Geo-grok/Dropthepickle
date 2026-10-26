-- Optional one-time backfill: copy the v2 labels from go_clicks_classified onto the stored rows.
-- Run after migrations/0004. Only rows the new rules flag are touched; nothing is deleted.
UPDATE go_clicks
SET is_bot = 1,
    bot_reason = (SELECT c.bot_reason_v2 FROM go_clicks_classified c WHERE c.id = go_clicks.id)
WHERE id IN (SELECT id FROM go_clicks_classified WHERE is_bot_v2 = 1 AND (is_bot = 0 OR bot_reason IS NULL));
