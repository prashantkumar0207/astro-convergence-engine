"""
House Utilities

Two distinct planet-to-house assignment rules are provided, and
they are NOT interchangeable (audit findings F-05 / A-2):

- equal_house_from_ascendant: twelve equal 30-degree houses
  measured from the exact Ascendant degree.
- whole_sign_house: the classical whole-sign (Rashi = Bhava)
  rule, where the sign containing the Ascendant is the 1st house
  and each subsequent sign is one house.

The two coincide only when the Ascendant is at 0 degrees of its
sign. The Parashari D1 chart builder uses WHOLE SIGN (the
documented project decision for Rashi charts); Placidus cusp data
remains available separately on HousePosition for cusp-based
techniques and never silently mixes with these rules.
"""

from engine.astrology.longitude_utils import (
    division_index,
    normalize_longitude,
)
from engine.astrology.signs import zodiac_sign


def equal_house_from_ascendant(
    longitude: float,
    ascendant: float,
) -> int:
    """
    Equal-house number (1-12) measured from the exact Ascendant
    degree. This is the rule the pre-remediation code implemented
    under a misleading whole-sign docstring.
    """
    diff = normalize_longitude(longitude - ascendant)

    return division_index(diff, 30.0, 12) + 1


def whole_sign_house(
    longitude: float,
    ascendant: float,
) -> int:
    """
    Whole-sign house number (1-12): the sign holding the
    Ascendant is house 1.
    """
    return (zodiac_sign(longitude) - zodiac_sign(ascendant)) % 12 + 1


def house_from_longitude(
    longitude: float,
    ascendant: float,
) -> int:
    """
    Backward-compatible alias for equal_house_from_ascendant.

    Deprecated: callers should choose equal_house_from_ascendant
    or whole_sign_house explicitly.
    """
    return equal_house_from_ascendant(longitude, ascendant)
