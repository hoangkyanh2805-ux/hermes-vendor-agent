#!/usr/bin/env python3
"""
rank_engine.py — Hermes Vendor Rank State Machine

Pure function: mutates registry dict in-place, no file I/O, no Telegram.
Importable standalone (no vendor_bot dependency).

STATE MACHINE DIAGRAM
=====================

         first_post_date set
  new ────────────────────────► active
   ▲                              │  ▲
   │                 30d joins≥20 │  │ cold→active:
   │                              ▼  │ last_post==today
   │                            top ─┤
   │                           ▲  │  │
   │         30d joins≥50 AND  │  │  │
   │         senior_streak≥3   │  │  │ top→active:
   │                           │  │  │ 30d joins<10
   │                       senior  │
   │                           │   │
   │    senior→top:            │   │
   │    30d joins<30           ▼   │
   │                        (top)  │
   │                               │
   │   any→cold: last_activity     │
   └── >14d AND status not in      │
       (inactive, cold) ───────────┘
                                cold

TRANSITIONS (7 total)
─────────────────────
1. new     → active  : first_post_date is set
2. active  → top     : 30day_valid_joins >= 20
3. top     → senior  : 30day_valid_joins >= 50 AND senior_streak >= 3
4. top     → active  : 30day_valid_joins < 10  (demotion)
5. senior  → top     : 30day_valid_joins < 30  (demotion)
6. any     → cold    : last_activity > 14d ago (status not inactive/cold)
7. cold    → active  : last_post_date == today

Optional fields added (additive, no breaking change):
  prev_rank          — rank saved before cold-flag, restored on re-activation
  senior_streak      — int, months consecutively meeting >=50 joins
  last_streak_month  — "YYYY-MM", idempotency guard for streak increment
"""

import datetime
import logging
from typing import Dict, List, Tuple

log = logging.getLogger("rank-engine")

# ─── Date helpers ──────────────────────────────────────────────────────────────

def _to_date(value):
    # type: (object) -> datetime.date | None
    """
    Parse a date value into datetime.date.

    Args:
        value: A string "YYYY-MM-DD" or a datetime.date instance.

    Returns:
        datetime.date on success, None on failure.
    """
    if value is None:
        return None
    if isinstance(value, datetime.date):
        return value
    if isinstance(value, str):
        try:
            parts = value.strip().split("-")
            if len(parts) == 3:
                return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
        except (ValueError, TypeError):
            pass
    return None


def _activity_date(v):
    # type: (dict) -> datetime.date | None
    """
    Return the most recent activity date for a vendor record.

    Checks last_post_date, then first_post_date, then join_date (fallback).

    Args:
        v: Vendor dict from registry.

    Returns:
        Most recent activity as datetime.date, or None if no parseable date found.
    """
    for field in ("last_post_date", "first_post_date", "join_date"):
        d = _to_date(v.get(field))
        if d is not None:
            return d
    return None


# ─── Streak helpers ─────────────────────────────────────────────────────────

def _current_month_str(today):
    # type: (datetime.date) -> str
    """Return "YYYY-MM" for the given date."""
    return today.strftime("%Y-%m")


def _maybe_increment_streak(v, today):
    # type: (dict, datetime.date) -> None
    """
    Increment senior_streak if this month has not already been counted.

    Idempotency guard: last_streak_month == current month prevents
    double-counting if the cron runs more than once in a calendar month.

    Args:
        v:     Vendor dict (mutated in place).
        today: Reference date (datetime.date).
    """
    month_str = _current_month_str(today)
    if v.get("last_streak_month") == month_str:
        return  # Already counted this month
    v["senior_streak"] = int(v.get("senior_streak", 0)) + 1
    v["last_streak_month"] = month_str


# ─── Transition helpers ─────────────────────────────────────────────────────

def _safe_joins(v):
    # type: (dict) -> int
    """
    Return 30day_valid_joins as int (0 on missing/invalid).

    Args:
        v: Vendor dict.

    Returns:
        Integer join count.
    """
    try:
        return int(v.get("30day_valid_joins", v.get("joins", 0)))
    except (TypeError, ValueError):
        return 0


# ─── Core state machine ─────────────────────────────────────────────────────

def run_transitions(registry, today):
    # type: (dict, datetime.date) -> List[Tuple[str, str]]
    """
    Run all rank state machine transitions over the vendor registry.

    Evaluates each vendor against the 7 defined transitions in priority order:

      1. new     → active  (first_post_date present)
      2. any     → cold    (last_activity > 14 days ago; skips inactive/cold)
      3. cold    → active  (last_post_date == today)
      4. active  → top     (30day_valid_joins >= 20)
      5. top     → senior  (30day_valid_joins >= 50 AND senior_streak >= 3)
      6. top     → active  (30day_valid_joins < 10; demotion)
      7. senior  → top     (30day_valid_joins < 30; demotion)

    Priority notes:
      - cold-flag (T2) is checked BEFORE cold→active (T3) so that a vendor
        who posts exactly today after a long silence is promoted in the same
        run rather than being stuck cold until the next cron.
      - Streak increment happens inside T5 only when the transition fires,
        guarded by last_streak_month.

    Args:
        registry: Full registry dict as loaded from vendor-registry.json.
                  Mutated in place — callers must save the file themselves.
        today:    Reference date for all age calculations (datetime.date).

    Returns:
        List of (vendor_name, transition_str) tuples for every transition
        that fired, in the order vendors were processed.
        Example: [("hiephoang47", "new->active"), ("tuananh99", "active->top")]
    """
    events = []  # type: List[Tuple[str, str]]
    vendors = registry.get("vendors", {})

    for name, v in vendors.items():
        status = v.get("status", "active")
        rank = v.get("rank", "new")

        # Skip fully deactivated vendors — they are managed manually.
        if status == "inactive":
            continue

        joins = _safe_joins(v)
        activity = _activity_date(v)

        # ── T1: new → active ─────────────────────────────────────────────────
        # Guard: rank == "new"
        # Trigger: first_post_date is set (vendor has made their first post)
        if rank == "new" and v.get("first_post_date"):
            v["rank"] = "active"
            v["status"] = "active"
            log.info("rank T1 new->active: %s", name)
            events.append((name, "new->active"))
            rank = "active"  # carry forward for subsequent checks in this pass
            status = "active"

        # ── T2: any → cold ───────────────────────────────────────────────────
        # Guard: status not in (inactive, cold)
        # Trigger: last_activity > 14 days ago
        # Saves prev_rank so T3 can restore it.
        if status not in ("inactive", "cold"):
            if activity is None or (today - activity).days > 14:
                prev_rank = rank
                v["prev_rank"] = prev_rank
                v["rank"] = "cold"
                v["status"] = "cold"
                log.info(
                    "rank T2 %s->cold: %s (last_activity=%s)",
                    prev_rank, name, activity
                )
                events.append((name, "{0}->cold".format(prev_rank)))
                rank = "cold"
                status = "cold"

        # ── T3: cold → active ────────────────────────────────────────────────
        # Guard: status == "cold"
        # Trigger: last_post_date == today (vendor posted again today)
        # Restores prev_rank when available.
        if status == "cold":
            last_post = _to_date(v.get("last_post_date"))
            if last_post == today:
                restored_rank = v.get("prev_rank", "active")
                # prev_rank could itself be "cold" if data is inconsistent;
                # clamp to "active" as the floor.
                if restored_rank not in ("new", "active", "top", "senior"):
                    restored_rank = "active"
                v["rank"] = restored_rank
                v["status"] = "active"
                v.pop("prev_rank", None)
                log.info("rank T3 cold->%s (restored): %s", restored_rank, name)
                events.append((name, "cold->{0}".format(restored_rank)))
                rank = restored_rank
                status = "active"

        # ── T4: active → top ─────────────────────────────────────────────────
        # Guard: rank == "active"
        # Trigger: 30day_valid_joins >= 20
        if rank == "active" and joins >= 20:
            v["rank"] = "top"
            log.info("rank T4 active->top: %s (joins=%d)", name, joins)
            events.append((name, "active->top"))
            rank = "top"

        # ── T5: top → senior ─────────────────────────────────────────────────
        # Guard: rank == "top"
        # Trigger: 30day_valid_joins >= 50 AND senior_streak >= 3
        # Streak is incremented here (once per month, idempotency-guarded).
        elif rank == "top" and joins >= 50:
            _maybe_increment_streak(v, today)
            streak = int(v.get("senior_streak", 0))
            if streak >= 3:
                v["rank"] = "senior"
                log.info(
                    "rank T5 top->senior: %s (joins=%d, streak=%d)",
                    name, joins, streak
                )
                events.append((name, "top->senior"))
                rank = "senior"

        # ── T6: top → active (demotion) ──────────────────────────────────────
        # Guard: rank == "top"
        # Trigger: 30day_valid_joins < 10
        elif rank == "top" and joins < 10:
            v["rank"] = "active"
            log.info("rank T6 top->active (demotion): %s (joins=%d)", name, joins)
            events.append((name, "top->active"))
            rank = "active"

        # ── T7: senior → top (demotion) ──────────────────────────────────────
        # Guard: rank == "senior"
        # Trigger: 30day_valid_joins < 30
        if rank == "senior" and joins < 30:
            v["rank"] = "top"
            log.info("rank T7 senior->top (demotion): %s (joins=%d)", name, joins)
            events.append((name, "senior->top"))
            # rank = "top"  # no further checks after this

    return events


# ─── Smoke test ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    two_weeks_ago = today - datetime.timedelta(days=15)
    one_month_ago = today - datetime.timedelta(days=32)

    mock_registry = {
        "vendors": {
            # T1: new → active (has first_post_date)
            "alice_new": {
                "vendor": "Alice",
                "rank": "new",
                "status": "new",
                "join_date": yesterday.isoformat(),
                "first_post_date": yesterday.isoformat(),
                "last_post_date": yesterday.isoformat(),
                "30day_valid_joins": 0,
            },
            # T2: any → cold (last activity 15 days ago)
            "bob_goes_cold": {
                "vendor": "Bob",
                "rank": "active",
                "status": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": two_weeks_ago.isoformat(),
                "30day_valid_joins": 5,
            },
            # T3: cold → active (posted today, was cold)
            "carol_returns": {
                "vendor": "Carol",
                "rank": "cold",
                "status": "cold",
                "prev_rank": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": today.isoformat(),
                "30day_valid_joins": 3,
            },
            # T4: active → top (>=20 joins)
            "dave_to_top": {
                "vendor": "Dave",
                "rank": "active",
                "status": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": today.isoformat(),
                "30day_valid_joins": 25,
            },
            # T5: top → senior (>=50 joins, streak already 3)
            "eve_to_senior": {
                "vendor": "Eve",
                "rank": "top",
                "status": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": today.isoformat(),
                "30day_valid_joins": 55,
                "senior_streak": 2,            # will be incremented to 3 → fires
                "last_streak_month": "2026-04", # old month — increment allowed
            },
            # T6: top → active demotion (<10 joins)
            "frank_demoted": {
                "vendor": "Frank",
                "rank": "top",
                "status": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": today.isoformat(),
                "30day_valid_joins": 7,
            },
            # T7: senior → top demotion (<30 joins)
            "grace_demoted": {
                "vendor": "Grace",
                "rank": "senior",
                "status": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": today.isoformat(),
                "30day_valid_joins": 20,
            },
            # No transition: inactive vendor — must be skipped entirely
            "henry_inactive": {
                "vendor": "Henry",
                "rank": "active",
                "status": "inactive",
                "join_date": one_month_ago.isoformat(),
                "30day_valid_joins": 0,
            },
            # No transition: idempotency guard — streak already counted this month
            "iris_streak_guard": {
                "vendor": "Iris",
                "rank": "top",
                "status": "active",
                "join_date": one_month_ago.isoformat(),
                "first_post_date": one_month_ago.isoformat(),
                "last_post_date": today.isoformat(),
                "30day_valid_joins": 55,
                "senior_streak": 2,
                "last_streak_month": today.strftime("%Y-%m"),  # already counted
            },
        }
    }

    print("=" * 60)
    print("rank_engine.py — smoke test")
    print("Today:", today.isoformat())
    print("=" * 60)

    events = run_transitions(mock_registry, today)

    print("\nFired transitions:")
    if events:
        for vendor_name, transition in events:
            print("  {0:20s}  {1}".format(vendor_name, transition))
    else:
        print("  (none)")

    print("\nFinal ranks:")
    for vname, v in mock_registry["vendors"].items():
        print("  {0:20s}  rank={1:8s}  status={2}".format(
            vname,
            v.get("rank", "?"),
            v.get("status", "?")
        ))

    # Assertions
    vendors = mock_registry["vendors"]
    assert vendors["alice_new"]["rank"] == "active",        "T1 failed"
    assert vendors["bob_goes_cold"]["rank"] == "cold",      "T2 failed"
    assert vendors["carol_returns"]["rank"] == "active",    "T3 failed"
    assert vendors["dave_to_top"]["rank"] == "top",         "T4 failed"
    assert vendors["eve_to_senior"]["rank"] == "senior",    "T5 failed"
    assert vendors["frank_demoted"]["rank"] == "active",    "T6 failed"
    assert vendors["grace_demoted"]["rank"] == "top",       "T7 failed"
    assert vendors["henry_inactive"]["rank"] == "active",   "inactive skip failed"
    assert vendors["iris_streak_guard"]["rank"] == "top",   "streak idempotency failed"
    assert vendors["iris_streak_guard"]["senior_streak"] == 2, "streak should not increment"

    print("\nAll assertions passed.")
    print("=" * 60)
