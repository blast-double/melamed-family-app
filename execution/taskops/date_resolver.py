#!/usr/bin/env python3
"""
Resolves relative deadline phrases from meeting transcripts to ISO dates.


Examples:
  "by Friday"     → next Friday from reference_date
  "next week"     → following Monday
  "end of month"  → last business day of reference month
  "tomorrow"      → reference_date + 1
  null / ""       → None
"""
from __future__ import annotations

import re
from datetime import date, timedelta


# Day name → weekday number (Monday=0 ... Sunday=6)
_DAY_MAP = {
    "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
    "friday": 4, "saturday": 5, "sunday": 6,
    "mon": 0, "tue": 1, "wed": 2, "thu": 3, "fri": 4, "sat": 5, "sun": 6,
}


def resolve_deadline(phrase: str | None, reference_date: date | None = None) -> str | None:
    """
    Convert a relative deadline phrase to an ISO date string (YYYY-MM-DD).
    Returns None if the phrase is empty, null, or unrecognizable.

    Args:
        phrase: Natural language deadline from transcript (e.g., "by Friday").
        reference_date: The date to resolve relative phrases against (typically
                       the meeting date). Defaults to today.
    """
    if not phrase or not phrase.strip():
        return None

    ref = reference_date or date.today()
    text = phrase.lower().strip()

    # Strip common prefixes
    text = re.sub(r"^(by|before|on|this coming|this)\s+", "", text)

    # "tomorrow"
    if "tomorrow" in text:
        return (ref + timedelta(days=1)).isoformat()

    # "today"
    if text in ("today", "now", "asap", "immediately"):
        return ref.isoformat()

    # "end of week" / "eow"
    if text in ("end of week", "eow", "end of the week"):
        days_until_friday = (4 - ref.weekday()) % 7
        if days_until_friday == 0 and ref.weekday() > 4:
            days_until_friday = 7
        return (ref + timedelta(days=days_until_friday or 7)).isoformat()

    # "next week" → following Monday
    if "next week" in text:
        days_until_monday = (7 - ref.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        return (ref + timedelta(days=days_until_monday)).isoformat()

    # "end of month" / "eom"
    if text in ("end of month", "eom", "end of the month"):
        if ref.month == 12:
            last_day = date(ref.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(ref.year, ref.month + 1, 1) - timedelta(days=1)
        # Back up to last business day
        while last_day.weekday() > 4:
            last_day -= timedelta(days=1)
        return last_day.isoformat()

    # Day name: "friday", "by wednesday", etc.
    for day_name, day_num in _DAY_MAP.items():
        if day_name in text:
            days_ahead = (day_num - ref.weekday()) % 7
            if days_ahead == 0:
                days_ahead = 7  # Always next occurrence, not today
            return (ref + timedelta(days=days_ahead)).isoformat()

    # "X days" / "X weeks"
    m = re.search(r"(\d+)\s*(day|week)s?", text)
    if m:
        n = int(m.group(1))
        unit = m.group(2)
        delta = timedelta(days=n) if unit == "day" else timedelta(weeks=n)
        return (ref + delta).isoformat()

    # Unrecognized → None (no due date rather than wrong date)
    return None
