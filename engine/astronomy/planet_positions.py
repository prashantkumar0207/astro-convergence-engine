"""
Planet Position Engine

Computes deterministic tropical planetary positions using the
Swiss Ephemeris.

No astrological interpretation is performed here.
"""

from __future__ import annotations

import swisseph as swe

from engine.models.planet_position import PlanetPosition


def planet_position(julian_day: float, body: int) -> PlanetPosition:
    """
    Compute the tropical position of a celestial body.
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    if not isinstance(body, int):
        raise TypeError("body must be a Swiss Ephemeris planet constant.")

    result = swe.calc_ut(
        julian_day,
        body,
        swe.FLG_SWIEPH | swe.FLG_SPEED,
    )

    position = result[0] if isinstance(result[0], (list, tuple)) else result

    return PlanetPosition(
        longitude=position[0],
        latitude=position[1],
        distance=position[2],
        speed_longitude=position[3],
        speed_latitude=position[4],
        speed_distance=position[5],
    )