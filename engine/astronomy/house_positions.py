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
    flags: int = 0,
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

    flags
        Swiss Ephemeris calculation flags. Pass swe.FLG_SIDEREAL
        (with the sidereal mode already set via set_sid_mode) to
        obtain sidereal cusps and angles; the default 0 yields the
        tropical frame. The produced HousePosition records which
        frame was used (audit finding F-01).

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
        flags,
    )

    # Defend against the C-style 13-element cusp tuple used by some
    # library versions (house 1 at index 1). pyswisseph 2.10 returns
    # 12 elements with house 1 at index 0; normalize to that.
    cusps = tuple(cusps)
    if len(cusps) == 13:
        cusps = cusps[1:]

    frame = "sidereal" if flags & swe.FLG_SIDEREAL else "tropical"

    return HousePosition(
        ascendant=ascmc[0],
        mc=ascmc[1],
        armc=ascmc[2],
        vertex=ascmc[3],
        equatorial_ascendant=ascmc[4],
        co_ascendant=ascmc[5],
        polar_ascendant=ascmc[7],
        houses=cusps,
        house_system=house_system.decode("ascii"),
        frame=frame,
    )