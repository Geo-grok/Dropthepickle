-- Matches the live dtp-subscribers.subscribers table.
-- id is assigned by SQLite. email is unique. created_at defaults to UTC if omitted.

CREATE TABLE IF NOT EXISTS subscribers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT NOT NULL UNIQUE,
  source TEXT,
  country TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
