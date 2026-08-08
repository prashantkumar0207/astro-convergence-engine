"""
Deterministic Dashamsa (D10) calculations.

Parashari Dashamsa rule:

- Each Rashi is divided into 10 equal parts of 3 degrees.
- Odd signs start counting from the source sign.
- Even signs start counting from the 9th sign from the source sign.

Sign indices:

0 = Aries
1 = Taurus
2 = Gemini
3 = Cancer
4 = Leo
5 = Virgo
6 = Libra
7 = Scorpio
8 = Sagittarius
9 = Capricorn
10 = Aquarius
11 = Pisces
"""

from collections.abc import Mapping

from engine.models.astronomy_snapshot import AstronomySnapshot


DASHAMSA_SIZE = 3.0


def _normalize_longitude(longitude: float) -> float:
    """Normalize longitude to [0, 360)."""
    return longitude % 360.0


def _start_sign(source_sign: int) -> int:
    """
    Return the starting D10 sign for a source Rashi.

    Parashari rule:

    - Odd sign  -> start from the source sign.
    - Even sign -> start from the 9th sign from the source sign.
    """
    if source_sign % 2 == 0:
        return source_sign

    return (source_sign + 8) % 12


def _segment(longitude: float) -> tuple[int, int, float]:
    """
    Return:

    - source sign
    - Dashamsa segment index (0-9)
    - degree within the source Rashi
    """
    longitude = _normalize_longitude(longitude)

    source_sign = int(longitude // 30.0)

    degree = longitude - source_sign * 30.0

    segment = int(degree // DASHAMSA_SIZE)

    # Protect the upper edge from floating-point spillover.
    if segment >= 10:
        segment = 9

    return source_sign, segment, degree


def dashamsa_sign(longitude: float) -> int:
    """
    Return the D10 sign index for a sidereal longitude.

    Sign indices:

    0 = Aries
    1 = Taurus
    ...
    11 = Pisces
    """
    source_sign, segment, _ = _segment(longitude)

    return (_start_sign(source_sign) + segment) % 12


def dashamsa_longitude(longitude: float) -> float:
    """
    Return the transformed D10 sidereal longitude.

    Each 3-degree Dashamsa segment is expanded into
    a full 30-degree D10 sign.
    """
    source_sign, segment, degree = _segment(longitude)

    d10_sign = (_start_sign(source_sign) + segment) % 12

    segment_start = segment * DASHAMSA_SIZE

    fraction = (
        degree - segment_start
    ) / DASHAMSA_SIZE

    result = (
        d10_sign * 30.0
        + fraction * 30.0
    )

    # Do not round here. Fixed-decimal rounding can move a value
    # immediately below a D10 boundary onto that boundary.
    #
    # Modulo guarantees the canonical [0, 360) range.
    return result % 360.0


def dashamsa_chart(snapshot: AstronomySnapshot):
    """
    Build the deterministic D10 representation from a D1 snapshot.
    """
    from engine.models.dashamsa_chart import DashamsaChart
    from engine.models.dashamsa_planet import DashamsaPlanet

    ascendant = dashamsa_longitude(snapshot.houses.ascendant)

    planets: dict[str, DashamsaPlanet] = {}

    source = snapshot.sidereal_planets

    if isinstance(source, Mapping):
        planet_items = source.items()
    else:
        planet_items = iter(source)

    for name, planet in planet_items:
        longitude = dashamsa_longitude(planet.longitude)

        _, segment, _ = _segment(planet.longitude)

        planets[name] = DashamsaPlanet(
            name=name,
            longitude=longitude,
            sign=dashamsa_sign(planet.longitude),
            degree=longitude % 30.0,
            segment=segment + 1,
        )

    return DashamsaChart(
        ascendant=ascendant,
        ascendant_sign=dashamsa_sign(snapshot.houses.ascendant),
        planets=planets,
    )