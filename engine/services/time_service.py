"""
Time Service

Converts BirthData local civil time to UTC using the IANA timezone
database (zoneinfo + tzdata), which correctly handles DST and
historical UTC-offset changes.

Remediates audit finding F-11: this module was previously dead
code while the live pipeline accepted fixed offsets that silently
ignore DST and history. It is now the live path
(engine.calculations.calculations.calculate).

Ambiguous local times (DST fall-back, occurring twice) are
disambiguated by BirthData.fold per PEP 495. Nonexistent local
times (DST gap) are rejected by engine.core.validation before this
service runs.
"""

from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from engine.models.birth_data import BirthData


def local_datetime(data: BirthData) -> datetime:
    """
    Build a timezone-aware local datetime from BirthData.
    """

    if not isinstance(data, BirthData):
        raise TypeError("data must be a BirthData instance.")

    return datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=data.hour,
        minute=data.minute,
        second=int(data.second),
        microsecond=int(round((data.second % 1) * 1_000_000)),
        tzinfo=ZoneInfo(data.timezone),
        fold=data.fold,
    )


def utc_datetime(data: BirthData) -> datetime:
    """
    Convert BirthData local birth time to UTC.
    """

    return local_datetime(data).astimezone(timezone.utc)
