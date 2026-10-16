-- Outbound click counter for /go/<slug> redirects (see src/worker.js and src/go-links.json).
CREATE TABLE IF NOT EXISTS go_clicks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  slug TEXT NOT NULL,
  referer_path TEXT,
  country TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
CREATE INDEX IF NOT EXISTS go_clicks_slug_time ON go_clicks (slug, created_at);
