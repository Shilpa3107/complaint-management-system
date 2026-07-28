from datetime import date
from typing import Optional
from dateutil import parser as dateutil_parser


def parse_flexible_date(raw: Optional[str]) -> Optional[date]:
    """Attempt to parse a date string in various formats using dateutil.
    Returns None if parsing fails (caller should treat as missing/needs review)."""
    if not raw:
        return None
    try:
        return dateutil_parser.parse(raw, fuzzy=True).date()
    except (ValueError, OverflowError):
        return None