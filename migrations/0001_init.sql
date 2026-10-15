-- Subscribers for POST /api/signup. Apply with:
-- npx wrangler d1 migrations apply dtp-subscribers
-- Do not apply until the D1 database dtp-subscribers exists and database_id is set.

CREATE TABLE subscribers (
  email TEXT NOT NULL UNIQUE,
  source TEXT,
  created_at TEXT NOT NULL,
  country TEXT
);
