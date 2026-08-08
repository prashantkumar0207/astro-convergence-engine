"""
Nakshatra Pada Utilities

Each nakshatra divides into 4 padas of 360/108 degrees
(3 deg 20 min) each. The pada is computed relative to the SAME
nakshatra that engine.astrology.nakshatra assigns, so the two
classifications can never disagree near a boundary: a longitude
promoted into the next nakshatra by the boundary tolerance gets
pada 1 of that nakshatra, not pada 4 of the previous one
(audit finding F-04).
"""

from engine.astrology.longitude_utils import (
    division_index,
    normalize_longitude,
)
from engine.astrology.nakshatra import NAKSHATRA_SPAN

PADA_SPAN = 360.0 / 108.0


def pada(longitude: float) -> int:
    """
    Returns nakshatra pada number (1-4).
    """
    longitude = normalize_longitude(longitude)

    nakshatra_index = division_index(longitude, NAKSHATRA_SPAN, 27)

    within = longitude - nakshatra_index * NAKSHATRA_SPAN

    if within < 0.0:
        # Tolerance promoted the longitude into the next
        # nakshatra; it sits at that nakshatra's first pada.
        within = 0.0

    return division_index(within, PADA_SPAN, 4) + 1
