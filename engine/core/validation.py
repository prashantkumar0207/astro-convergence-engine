from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from models.birth_data import BirthData


class ValidationError(Exception):
    """Raised when birth data is invalid."""


def validate_birth_data(data: BirthData) -> None:
    """
    Validate all birth input before any calculations begin.
    Raises ValidationError if anything is invalid.
    """

    # -------------------------------
    # Validate date & time
    # -------------------------------
    try:
        datetime(
            year=data.year,
            month=data.month,
            day=data.day,
            hour=data.hour,
            minute=data.minute,
            second=int(data.second),
        )
    except ValueError as exc:
        raise ValidationError(str(exc))

    # -------------------------------
    # Validate latitude
    # -------------------------------
    if not (-90.0 <= data.latitude <= 90.0):
        raise ValidationError(
            f"Latitude out of range: {data.latitude}"
        )

    # -------------------------------
    # Validate longitude
    # -------------------------------
    if not (-180.0 <= data.longitude <= 180.0):
        raise ValidationError(
            f"Longitude out of range: {data.longitude}"
        )

    # -------------------------------
    # Validate timezone
    # -------------------------------
    try:
        ZoneInfo(data.timezone)
    except ZoneInfoNotFoundError:
        raise ValidationError(
            f"Unknown timezone: {data.timezone}"
        )