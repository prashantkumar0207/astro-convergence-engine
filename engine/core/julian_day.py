"""
Julian Day Engine

Purpose
-------
Convert a timezone-aware UTC datetime into a deterministic Julian Day
using the Swiss Ephemeris implementation.

This module performs no timezone conversion. The caller is responsible
for supplying a UTC-aware datetime.
"""

from __future__ import annotations

from datetime import datetime, timezone

import swisseph as swe


def julian_day(datetime_utc: datetime) -> float:
    """
    Compute the Julian Day for a UTC datetime.

    Parameters
    ----------
    datetime_utc
        A timezone-aware datetime in UTC.

    Returns
    -------
    float
        Julian Day.

    Raises
    ------
    TypeError
        If the input is not a datetime.
    ValueError
        If the datetime is naive or not UTC.
    """

    if not isinstance(datetime_utc, datetime):
        raise TypeError("datetime_utc must be a datetime object.")

    if datetime_utc.tzinfo is None:
        raise ValueError("datetime_utc must be timezone-aware.")

    if datetime_utc.utcoffset() != timezone.utc.utcoffset(datetime_utc):
        raise ValueError("datetime_utc must be in UTC.")

    return swe.julday(
        datetime_utc.year,
        datetime_utc.month,
        datetime_utc.day,
        (
            datetime_utc.hour
            + datetime_utc.minute / 60
            + datetime_utc.second / 3600
            + datetime_utc.microsecond / 3_600_000_000
        ),
    )