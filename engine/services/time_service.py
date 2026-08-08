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
        microsecond=int((data.second % 1) * 1_000_000),
        tzinfo=ZoneInfo(data.timezone),
    )


def utc_datetime(data: BirthData) -> datetime:
    """
    Convert BirthData local birth time to UTC.
    """

    return local_datetime(data).astimezone(timezone.utc)