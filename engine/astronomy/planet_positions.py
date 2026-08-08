"""
Planet Position Engine

Computes deterministic tropical planetary positions using the
Swiss Ephemeris.

No astrological interpretation is performed here.
"""

from __future__ import annotations

import swisseph as swe

from engine.astronomy.ephemeris import calc_ut_checked
from engine.models.planet_position import PlanetPosition


def planet_position(
    julian_day: float,
    body: int,
    strict: bool = True,
) -> PlanetPosition:
    """
    Compute the tropical position of a celestial body.

    Uses the Swiss Ephemeris (SWIEPH) with the bundled data files.
    In strict mode (default) a silent fallback to the Moshier
    ephemeris raises EphemerisFallbackError instead of returning
    mislabelled data (audit finding F-02).
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    if not isinstance(body, int):
        raise TypeError("body must be a Swiss Ephemeris planet constant.")

    position, _mode = calc_ut_checked(
        julian_day,
        body,
        swe.FLG_SWIEPH | swe.FLG_SPEED,
        strict=strict,
    )

    return PlanetPosition(
        longitude=position[0],
        latitude=position[1],
        distance=position[2],
        speed_longitude=position[3],
        speed_latitude=position[4],
        speed_distance=position[5],
    )