"""
Timezone Engine

Converts a timezone-aware local datetime to UTC.
"""

from __future__ import annotations

from datetime import datetime, timezone


def to_utc(local_datetime: datetime) -> datetime:
    """
    Convert a timezone-aware datetime to UTC.
    """

    if not isinstance(local_datetime, datetime):
        raise TypeError("local_datetime must be a datetime object.")

    if local_datetime.tzinfo is None:
        raise ValueError("local_datetime must be timezone-aware.")

    return local_datetime.astimezone(timezone.utc)