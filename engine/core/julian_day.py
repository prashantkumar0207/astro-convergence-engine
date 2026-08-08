"""
Julian Day Engine

Purpose
-------
Convert a timezone-aware UTC datetime into a deterministic Julian Day
using the Swiss Ephemeris implementation.

This module performs no timezone conversion. The caller is responsible
for supplying a UTC-aware datetime.

Calendar policy (audit finding F-10): Python datetimes are proleptic
Gregorian BY DEFINITION, so the Gregorian calendar flag is passed to
the Swiss Ephemeris explicitly. Historical dates recorded in the
Julian calendar (before 1582-10-15 in most of Europe, later
elsewhere) must be converted to proleptic Gregorian by the caller
BEFORE constructing the datetime; passing a Julian-calendar date
unconverted shifts the result by about 10 days near 1582.

Time basis: the result is a Julian Day in UT, passed to Swiss
Ephemeris *_ut functions. UTC is treated as UT1; the difference is
bounded by 0.9 s (about 0.5 arcsec of Moon motion) and accepted as
within tolerance. This is recorded in snapshot Provenance.
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
        swe.GREG_CAL,
    )