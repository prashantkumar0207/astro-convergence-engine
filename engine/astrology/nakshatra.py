"""
Nakshatra Utilities

Each of the 27 nakshatras spans 360/27 degrees (13 deg 20 min).
Boundary handling follows the project convention in
engine.astrology.longitude_utils (audit finding F-04: exact
boundaries such as 40.0 degrees, the start of Rohini, were
previously misclassified into the preceding nakshatra because the
binary double 360/27 exceeds the exact rational 40/3).
"""

from engine.astrology.longitude_utils import (
    division_index,
    normalize_longitude,
)

NAKSHATRA_SPAN = 360.0 / 27.0


def nakshatra(longitude: float) -> int:
    """
    Returns Nakshatra number (1-27).
    """
    longitude = normalize_longitude(longitude)

    return division_index(longitude, NAKSHATRA_SPAN, 27) + 1
