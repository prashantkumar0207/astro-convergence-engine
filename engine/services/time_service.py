from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from models.birth_data import BirthData


def local_datetime(data: BirthData) -> datetime:
    """
    Return timezone-aware local datetime.
    """

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
    Convert local birth time to UTC.
    """

    return local_datetime(data).astimezone(timezone.utc)