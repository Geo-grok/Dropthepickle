#!/usr/bin/env python3
"""Unit tests for the go_clicks_classified pair_burst rule (migration 0005).

Rebuilds the go_clicks schema in an in-memory SQLite database, inserts sample
clicks, and checks that the same slug from two different countries within 5
seconds is flagged on both sides, while longer gaps, same-country pairs, and
different slugs are not. Also checks that src/worker.js stays in sync
(PAIR_WINDOW_SEC = 5, pair_burst label) and that handleGo still returns a 302.
"""
from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WINDOW_SEC = 5
fail = 0


def ok(msg: str) -> None:
    print("ok  ", msg)


def bad(msg: str) -> None:
    global fail
    fail += 1
    print("FAIL", msg)


def exec_script(db: sqlite3.Connection, path: Path) -> None:
    db.executescript(path.read_text())


def schema() -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    # 0002-0005 only (0001 is subscribers).
    for name in (
        "0002_go_clicks.sql",
        "0003_go_clicks_ua.sql",
        "0004_go_clicks_bot_reason.sql",
        "0005_go_clicks_pair_burst.sql",
    ):
        exec_script(db, ROOT / "migrations" / name)
    return db


def insert(
    db: sqlite3.Connection,
    slug: str,
    country: str | None,
    created_at: str,
    *,
    referer_path: str | None = "/",
    user_agent: str | None = "Mozilla/5.0 (Macintosh) AppleWebKit/605.1.15 Safari/605.1",
    is_bot: int = 0,
    bot_reason: str | None = None,
) -> int:
    cur = db.execute(
        "INSERT INTO go_clicks (slug, referer_path, country, created_at, user_agent, is_bot, bot_reason) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (slug, referer_path, country, created_at, user_agent, is_bot, bot_reason),
    )
    return int(cur.lastrowid)


def classified(db: sqlite3.Connection, row_id: int) -> sqlite3.Row:
    row = db.execute("SELECT * FROM go_clicks_classified WHERE id = ?", (row_id,)).fetchone()
    if row is None:
        raise AssertionError(f"no classified row for id={row_id}")
    return row


def expect_pair(db: sqlite3.Connection, row_id: int, label: str) -> None:
    row = classified(db, row_id)
    if row["r_pair_burst"] and row["is_bot_v2"] == 1 and "pair_burst" in (row["bot_reason_v2"] or ""):
        ok(label)
    else:
        bad(
            f"{label}: r_pair_burst={row['r_pair_burst']} is_bot_v2={row['is_bot_v2']} "
            f"reason={row['bot_reason_v2']!r}"
        )


def expect_not_pair(db: sqlite3.Connection, row_id: int, label: str) -> None:
    row = classified(db, row_id)
    if row["r_pair_burst"]:
        bad(f"{label}: unexpectedly pair_burst reason={row['bot_reason_v2']!r}")
    else:
        ok(label)


def test_source_sync() -> None:
    worker = (ROOT / "src" / "worker.js").read_text()
    mig = (ROOT / "migrations" / "0005_go_clicks_pair_burst.sql").read_text()
    if f"const PAIR_WINDOW_SEC = {WINDOW_SEC};" in worker:
        ok("worker.js PAIR_WINDOW_SEC = 5")
    else:
        bad("worker.js missing `const PAIR_WINDOW_SEC = 5;`")
    if 'reasons.push("pair_burst")' in worker:
        ok("worker.js labels later click as pair_burst")
    else:
        bad("worker.js does not push pair_burst")
    if "pair_burst backflag" in worker or "pair_burst') > 0" in worker:
        ok("worker.js back-flags the earlier click")
    else:
        bad("worker.js has no earlier-click backflag")
    # Redirect behaviour must stay a 302 to the same destination.
    if "status: 302" in worker and "return new Response(null, {" in worker:
        ok("worker.js handleGo still returns 302")
    else:
        bad("worker.js handleGo 302 response missing")
    if "never blocks or alters the redirect" in worker or "Labelling never blocks or alters the redirect" in worker:
        ok("worker.js still documents that labelling does not change the redirect")
    else:
        bad("worker.js lost the 'labelling does not change the redirect' note")
    if "5.0/86400" in mig and "pair_burst" in mig and "DROP VIEW IF EXISTS go_clicks_classified" in mig:
        ok("migration 0005 view uses +/- 5s and pair_burst")
    else:
        bad("migration 0005 missing 5.0/86400, pair_burst, or DROP VIEW")


def test_pairs() -> None:
    db = schema()
    slug = "selkirk-labs-project-boomstik"

    # 1. Classic sweep: same slug, SG then BR 2 seconds later. Both sides flagged.
    a = insert(db, slug, "SG", "2026-11-20T12:00:00.000Z")
    b = insert(db, slug, "BR", "2026-11-20T12:00:02.000Z")
    expect_pair(db, a, "SG click of a 2s SG/BR pair is flagged")
    expect_pair(db, b, "BR click of a 2s SG/BR pair is flagged")

    # 2. Inclusive 5-second boundary.
    c = insert(db, "paddle-boundary", "SG", "2026-11-20T13:00:00.000Z")
    d = insert(db, "paddle-boundary", "IN", "2026-11-20T13:00:05.000Z")
    expect_pair(db, c, "pair at exactly 5s is flagged (first)")
    expect_pair(db, d, "pair at exactly 5s is flagged (second)")

    # 3. Just outside the window: 6 seconds.
    e = insert(db, "paddle-gap", "SG", "2026-11-20T14:00:00.000Z")
    f = insert(db, "paddle-gap", "BR", "2026-11-20T14:00:06.000Z")
    expect_not_pair(db, e, "6s gap is not a pair (first)")
    expect_not_pair(db, f, "6s gap is not a pair (second)")

    # 4. Same slug, same country, 2s apart: not pair_burst (same-country burst is a different rule).
    g = insert(db, "paddle-same-country", "US", "2026-11-20T15:00:00.000Z")
    h = insert(db, "paddle-same-country", "US", "2026-11-20T15:00:02.000Z")
    expect_not_pair(db, g, "same-country pair is not pair_burst (first)")
    expect_not_pair(db, h, "same-country pair is not pair_burst (second)")
    row = classified(db, g)
    if row["is_bot_v2"] == 0:
        ok("two US clicks in 2s stay is_bot_v2=0 (under the any-country burst of 10)")
    else:
        bad(f"two US clicks unexpectedly flagged is_bot_v2={row['is_bot_v2']} reason={row['bot_reason_v2']!r}")

    # 5. Different slugs, SG and BR 2s apart: not a pair.
    i = insert(db, "paddle-alpha", "SG", "2026-11-20T16:00:00.000Z")
    j = insert(db, "paddle-beta", "BR", "2026-11-20T16:00:02.000Z")
    expect_not_pair(db, i, "different slugs are not a pair (SG)")
    expect_not_pair(db, j, "different slugs are not a pair (BR)")

    # 6. Lone click.
    k = insert(db, "paddle-lone", "SG", "2026-11-20T17:00:00.000Z")
    expect_not_pair(db, k, "a single click is not a pair")
    if classified(db, k)["is_bot_v2"] == 0:
        ok("lone browser click stays is_bot_v2=0")
    else:
        bad("lone browser click was flagged")

    # 7. Null country does not form a pair with a real country.
    m = insert(db, "paddle-null", None, "2026-11-20T18:00:00.000Z")
    n = insert(db, "paddle-null", "SG", "2026-11-20T18:00:02.000Z")
    expect_not_pair(db, m, "null-country click is not a pair")
    expect_not_pair(db, n, "click next to a null-country row is not a pair")

    # 8. Three countries on the same slug within 5s: all flagged.
    o = insert(db, "paddle-triple", "SG", "2026-11-20T19:00:00.000Z")
    p = insert(db, "paddle-triple", "BR", "2026-11-20T19:00:02.000Z")
    q = insert(db, "paddle-triple", "IN", "2026-11-20T19:00:04.000Z")
    expect_pair(db, o, "triple pair SG")
    expect_pair(db, p, "triple pair BR")
    expect_pair(db, q, "triple pair IN")

    # 9. Same-country burst rule still works (3 SG clicks in 10 minutes, even on different slugs).
    r1 = insert(db, "burst-one", "SG", "2026-11-20T20:00:00.000Z")
    r2 = insert(db, "burst-two", "SG", "2026-11-20T20:01:00.000Z")
    r3 = insert(db, "burst-three", "SG", "2026-11-20T20:02:00.000Z")
    for rid, name in ((r1, "first"), (r2, "second"), (r3, "third")):
        row = classified(db, rid)
        if row["r_burst"] and row["is_bot_v2"] == 1 and "burst" in (row["bot_reason_v2"] or ""):
            ok(f"same-country SG burst still flags the {name} click")
        else:
            bad(f"SG burst missed the {name} click: r_burst={row['r_burst']} reason={row['bot_reason_v2']!r}")
        if row["r_pair_burst"]:
            bad(f"SG burst click {name} should not also be pair_burst")

    # 10. Optional reclassify backfill copies pair_burst onto stored is_bot / bot_reason.
    before = db.execute("SELECT is_bot, bot_reason FROM go_clicks WHERE id = ?", (a,)).fetchone()
    db.executescript((ROOT / "scripts" / "reclassify_go_clicks.sql").read_text())
    after = db.execute("SELECT is_bot, bot_reason FROM go_clicks WHERE id = ?", (a,)).fetchone()
    if before["is_bot"] == 0 and after["is_bot"] == 1 and "pair_burst" in (after["bot_reason"] or ""):
        ok("reclassify_go_clicks.sql backfills pair_burst onto stored rows")
    else:
        bad(f"reclassify did not backfill pair: before={tuple(before)} after={tuple(after)}")

    db.close()


def main() -> int:
    test_source_sync()
    test_pairs()
    if fail:
        print(f"{fail} pair_burst check(s) failed")
        return 1
    print("pair_burst checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
