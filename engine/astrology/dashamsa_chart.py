"""
Deterministic Dashamsa (D10) calculations.
"""
from engine.models.astronomy_snapshot import AstronomySnapshot

MOVABLE_SIGNS = {0, 3, 6, 9}
FIXED_SIGNS = {1, 4, 7, 10}

DASHAMSA_SIZE = 3.0


def _normalize_longitude(longitude: float) -> float:
    """Normalize longitude to [0, 360)."""
    return longitude % 360.0


def _start_sign(source_sign: int) -> int:
    """
    Return the starting D10 sign for a source Rashi.

    Movable -> same sign
    Fixed   -> 9th sign from source
    Dual    -> 5th sign from source
    """
    if source_sign in MOVABLE_SIGNS:
        return source_sign

    if source_sign in FIXED_SIGNS:
        return (source_sign + 8) % 12

    return (source_sign + 4) % 12


def _segment(longitude: float) -> tuple[int, int, float]:
    """
    Return source sign, Dashamsa segment index and degree within
    the source Rashi.
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
    """
    source_sign, segment, degree = _segment(longitude)

    d10_sign = (_start_sign(source_sign) + segment) % 12

    segment_start = segment * DASHAMSA_SIZE
    fraction = (degree - segment_start) / DASHAMSA_SIZE

    result = d10_sign * 30.0 + fraction * 30.0

    return round(result % 360.0, 12)

def dashamsa_chart(snapshot: AstronomySnapshot):
    """Build the deterministic D10 representation from a D1 snapshot."""
    from collections.abc import Mapping

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
        source_sign, segment, _ = _segment(planet.longitude)

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