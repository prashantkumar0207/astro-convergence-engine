"""
Birth Data Validation

Remediates audit finding F-12: this module previously had a broken
import (top-level `models` instead of `engine.models`), was dead
code, and its test file was empty, so no latitude, longitude,
timezone, or date validation was reachable anywhere in the engine.

It is now wired into the live calculation pipeline
(engine.calculations.calculations.calculate).
"""

import math
from datetime import datetime, timezone as _tz
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from engine.models.birth_data import BirthData


class ValidationError(Exception):
    """Raised when birth data is invalid."""


def validate_birth_data(data: BirthData) -> None:
    """
    Validate all birth input before any calculations begin.
    Raises ValidationError if anything is invalid.
    """

    if not isinstance(data, BirthData):
        raise ValidationError("data must be a BirthData instance.")

    # Date & time fields form a real calendar datetime.
    try:
        naive = datetime(
            year=data.year,
            month=data.month,
            day=data.day,
            hour=data.hour,
            minute=data.minute,
            second=int(data.second),
        )
    except (ValueError, TypeError) as exc:
        raise ValidationError(str(exc))

    if not isinstance(data.second, (int, float)) or not (
        0.0 <= float(data.second) < 60.0
    ):
        raise ValidationError(f"Second out of range: {data.second}")

    if data.fold not in (0, 1):
        raise ValidationError(f"fold must be 0 or 1, got {data.fold}")

    # Latitude / longitude ranges (geographic degrees).
    if not isinstance(data.latitude, (int, float)) or not (
        -90.0 <= data.latitude <= 90.0
    ):
        raise ValidationError(f"Latitude out of range: {data.latitude}")

    if not isinstance(data.longitude, (int, float)) or not (
        -180.0 <= data.longitude <= 180.0
    ):
        raise ValidationError(f"Longitude out of range: {data.longitude}")

    # ADR-0054: no arbitrary bound is imposed (real locations range from
    # below-sea-level basins to high mountains); only finiteness is
    # checked, matching this repository's practice of not inventing
    # limits the record does not justify.
    if not isinstance(data.elevation_m, (int, float)) or not math.isfinite(
        float(data.elevation_m)
    ):
        raise ValidationError(f"elevation_m must be a finite number: {data.elevation_m}")

    # Timezone must be a real IANA zone.
    try:
        zone = ZoneInfo(data.timezone)
    except (ZoneInfoNotFoundError, TypeError, ValueError):
        raise ValidationError(f"Unknown timezone: {data.timezone}")

    # Nonexistent local times (DST spring-forward gap): a local
    # time inside the gap does not round-trip through UTC.
    aware = naive.replace(tzinfo=zone, fold=data.fold)

    round_trip = aware.astimezone(_tz.utc).astimezone(zone)

    if round_trip.replace(tzinfo=None, fold=0) != naive:
        raise ValidationError(
            f"Nonexistent local time (DST gap): {naive} in {data.timezone}"
        )
