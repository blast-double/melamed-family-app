"""Tests for date resolver (copied from Itero — smoke tests)."""
from datetime import date
from execution.taskops.date_resolver import resolve_deadline


class TestDateResolver:
    def test_tomorrow(self):
        ref = date(2026, 3, 27)
        assert resolve_deadline("tomorrow", ref) == "2026-03-28"

    def test_today(self):
        ref = date(2026, 3, 27)
        assert resolve_deadline("today", ref) == "2026-03-27"

    def test_next_week(self):
        ref = date(2026, 3, 27)  # Friday
        assert resolve_deadline("next week", ref) == "2026-03-30"  # Monday

    def test_by_friday(self):
        ref = date(2026, 3, 23)  # Monday
        assert resolve_deadline("by Friday", ref) == "2026-03-27"

    def test_relative_days(self):
        ref = date(2026, 3, 27)
        assert resolve_deadline("3 days", ref) == "2026-03-30"

    def test_none_input(self):
        assert resolve_deadline(None) is None

    def test_empty_string(self):
        assert resolve_deadline("") is None

    def test_unrecognized(self):
        assert resolve_deadline("whenever") is None
