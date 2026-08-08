
"""Navamsa (D9) Chart."""

from engine.models.astronomy_snapshot import AstronomySnapshot


def navamsa_sign(longitude: float) -> int:
    """Return Navamsa sign index (0-11)."""
    longitude %= 360.0
    sign = int(longitude // 30.0)
    degree = longitude % 30.0
    navamsa = int(degree // (30.0 / 9.0))

    if sign in {0, 3, 6, 9}:          # movable
        start = sign
    elif sign in {1, 4, 7, 10}:       # fixed
        start = (sign + 8) % 12
    else:                              # dual
        start = (sign + 4) % 12

    return (start + navamsa) % 12


def navamsa_longitude(longitude: float) -> float:
    """Convert a sidereal longitude to its D9 longitude."""
    longitude %= 360.0

    sign = int(longitude // 30.0)
    degree = longitude % 30.0
    navamsa_size = 30.0 / 9.0
    navamsa = int(degree // navamsa_size)

    fraction = (degree - navamsa * navamsa_size) / navamsa_size

    if sign in {0, 3, 6, 9}:
        start = sign
    elif sign in {1, 4, 7, 10}:
        start = (sign + 8) % 12
    else:
        start = (sign + 4) % 12

    return ((start + navamsa) % 12) * 30.0 + fraction * 30.0


def navamsa_pada(longitude: float) -> int:
    """Return D9 pada number 1-108."""
    longitude %= 360.0
    return int(longitude / (360.0 / 108.0)) + 1


def navamsa_chart(snapshot: AstronomySnapshot):
    """Build deterministic D9 representation."""

    from engine.models.navamsa_chart import NavamsaChart
    from engine.models.navamsa_planet import NavamsaPlanet

    ascendant = navamsa_longitude(snapshot.houses.ascendant)

    source = snapshot.sidereal_planets

    if hasattr(source, "items"):
        iterator = source.items()
    else:
        iterator = source

    planets = {}

    for name, planet in iterator:
        lon = navamsa_longitude(planet.longitude)

        planets[name] = NavamsaPlanet(
            name=name,
            longitude=lon,
            sign=navamsa_sign(planet.longitude),
            degree=lon % 30.0,
            pada=navamsa_pada(planet.longitude),
        )

    return NavamsaChart(
        ascendant=ascendant,
        ascendant_sign=navamsa_sign(snapshot.houses.ascendant),
        planets=planets,
    )
