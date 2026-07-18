"""
House Position Engine

Computes deterministic house cusps and angles using
the Swiss Ephemeris.

No astrological interpretation is performed here.
"""

from __future__ import annotations

import swisseph as swe

from engine.models.house_position import HousePosition


def house_positions(
    julian_day: float,
    latitude: float,
    longitude: float,
    house_system: bytes = b"P",
) -> HousePosition:
    """
    Compute deterministic house cusps and major angles.

    Parameters
    ----------
    julian_day
        Julian Day in UTC.

    latitude
        Geographic latitude in degrees.

    longitude
        Geographic longitude in degrees.

    house_system
        Swiss Ephemeris house system code.

    Returns
    -------
    HousePosition
        Deterministic house geometry.

    Raises
    ------
    TypeError
        If any argument has an invalid type.
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    if not isinstance(latitude, (int, float)):
        raise TypeError("latitude must be numeric.")

    if not isinstance(longitude, (int, float)):
        raise TypeError("longitude must be numeric.")

    if not isinstance(house_system, bytes):
        raise TypeError("house_system must be bytes.")

    cusps, ascmc = swe.houses_ex(
        julian_day,
        latitude,
        longitude,
        house_system,
    )

    return HousePosition(
        ascendant=ascmc[0],
        mc=ascmc[1],
        armc=ascmc[2],
        vertex=ascmc[3],
        equatorial_ascendant=ascmc[4],
        co_ascendant=ascmc[5],
        polar_ascendant=ascmc[7],
        houses=tuple(cusps[1:]),
    )