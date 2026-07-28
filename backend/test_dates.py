from app.agents.date_utils import parse_flexible_date

test_cases = ["15/01/2026", "20th July 2026", "2026-01-15", "January 15, 2026", "not a date"]
for t in test_cases:
    print(f"{t!r:30} -> {parse_flexible_date(t)}")