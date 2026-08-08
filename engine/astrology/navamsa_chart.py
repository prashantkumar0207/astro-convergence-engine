"""Deterministic Navamsa (D9) calculations."""

from collections.abc import Mapping

from engine.models.astronomy_snapshot import AstronomySnapshot


_MOVABLE_SIGNS = {0, 3, 6, 9}
_FIXED_SIGNS = {1, 4, 7, 10}
_NAVAMSA_SIZE = 30.0 / 9.0


def _navamsa_start_sign(sign: int) -> int:
    """Return the first D9 sign for a source zodiac sign (0-based)."""
    if sign in _MOVABLE_SIGNS:
        return sign
    if sign in _FIXED_SIGNS:
        return (sign + 8) % 12
    return (sign + 4) % 12


def navamsa_sign(longitude: float) -> int:
    """Return the D9 sign index (0-11) for a sidereal longitude."""
    longitude %= 360.0
    sign = int(longitude // 30.0)
    degree = longitude % 30.0
    navamsa_index = min(
    8,
    int((degree + 1e-10) / _NAVAMSA_SIZE),
)
    return (_navamsa_start_sign(sign) + navamsa_index) % 12


def navamsa_longitude(longitude: float) -> float:
    """Map a sidereal longitude to its continuous D9 longitude."""
    longitude %= 360.0

    sign = int(longitude // 30.0)
    degree = longitude % 30.0
    navamsa_index = min(
    8,
    int((degree + 1e-10) / _NAVAMSA_SIZE),
)
    fraction = (degree - navamsa_index * _NAVAMSA_SIZE) / _NAVAMSA_SIZE

    d9_sign = (_navamsa_start_sign(sign) + navamsa_index) % 12
    return d9_sign * 30.0 + fraction * 30.0


def navamsa_pada(longitude: float) -> int:
    """Return Navamsa pada number (1-9) for a sidereal longitude."""
    longitude = longitude % 360.0

    sign_degree = longitude % 30.0

    # Each Navamsa = 10/3 degrees.
    # Use a small tolerance so exact boundaries such as
    # 10°00'00" are classified into the next Navamsa.
    navamsa_index = int((sign_degree + 1e-10) / (10.0 / 3.0))

    return navamsa_index + 1


def _iter_sidereal_planets(snapshot: AstronomySnapshot):
    """Yield (name, planet) pairs from supported planet containers."""
    source = snapshot.sidereal_planets
    if isinstance(source, Mapping):
        return source.items()
    return iter(source)


def navamsa_chart(snapshot: AstronomySnapshot):
    """Build the deterministic D9 representation from a D1 snapshot."""
    from engine.models.navamsa_chart import NavamsaChart
    from engine.models.navamsa_planet import NavamsaPlanet

    ascendant = navamsa_longitude(snapshot.houses.ascendant)

    planets: dict[str, NavamsaPlanet] = {}
    for name, planet in _iter_sidereal_planets(snapshot):
        longitude = navamsa_longitude(planet.longitude)
        planets[name] = NavamsaPlanet(
            name=name,
            longitude=longitude,
            sign=navamsa_sign(planet.longitude),
            degree=longitude % 30.0,
            pada=navamsa_pada(planet.longitude),
        )

    return NavamsaChart(
        ascendant=ascendant,
        ascendant_sign=navamsa_sign(snapshot.houses.ascendant),
        planets=planets,
    )
