"""Deterministic Navamsa (D9) calculations."""

from collections.abc import Mapping

from engine.models.astronomy_snapshot import AstronomySnapshot


_MOVABLE_SIGNS = {0, 3, 6, 9}
_FIXED_SIGNS = {1, 4, 7, 10}
_NAVAMSA_SIZE = 30.0 / 9.0

# Small tolerance so values immediately below an exact Navamsa
# boundary are classified into the next Navamsa, matching the
# convention that an exact boundary belongs to the next division.
_BOUNDARY_TOLERANCE = 1e-10


def _normalize_longitude(longitude: float) -> float:
    """
    Normalize a longitude to the canonical [0, 360) range.

    Python's float modulo can return exactly 360.0 for tiny
    negative inputs (for example -1e-16 % 360.0 == 360.0),
    which would produce an out-of-range sign index of 12.
    Guard against that explicitly.
    """
    longitude = longitude % 360.0

    if longitude >= 360.0:
        return 0.0

    return longitude


def _navamsa_index(degree: float) -> int:
    """
    Return the zero-based Navamsa index (0-8) for a degree
    within a sign, applying the boundary tolerance and
    clamping against floating-point spillover at the top edge.
    """
    return min(
        8,
        int((degree + _BOUNDARY_TOLERANCE) / _NAVAMSA_SIZE),
    )


def _navamsa_start_sign(sign: int) -> int:
    """Return the first D9 sign for a source zodiac sign (0-based)."""
    if sign in _MOVABLE_SIGNS:
        return sign
    if sign in _FIXED_SIGNS:
        return (sign + 8) % 12
    return (sign + 4) % 12


def navamsa_sign(longitude: float) -> int:
    """Return the D9 sign index (0-11) for a sidereal longitude."""
    longitude = _normalize_longitude(longitude)

    sign = int(longitude // 30.0)
    degree = longitude % 30.0

    navamsa_index = _navamsa_index(degree)

    return (_navamsa_start_sign(sign) + navamsa_index) % 12


def navamsa_longitude(longitude: float) -> float:
    """Map a sidereal longitude to its continuous D9 longitude."""
    longitude = _normalize_longitude(longitude)

    sign = int(longitude // 30.0)
    degree = longitude % 30.0

    navamsa_index = _navamsa_index(degree)

    fraction = (degree - navamsa_index * _NAVAMSA_SIZE) / _NAVAMSA_SIZE

    # When the boundary tolerance promotes a value sitting
    # immediately below a Navamsa boundary into the next
    # Navamsa, the raw fraction is a tiny negative number.
    # Clamp it so the returned longitude stays inside the
    # same D9 sign that navamsa_sign() reports.
    if fraction < 0.0:
        fraction = 0.0

    d9_sign = (_navamsa_start_sign(sign) + navamsa_index) % 12

    return d9_sign * 30.0 + fraction * 30.0


def navamsa_number(longitude: float) -> int:
    """
    Return the navamsa number (1-9) for a sidereal longitude.

    Canonical name per audit A-6; this is the 1-9 division within
    a sign, a distinct concept from the 1-4 nakshatra pada.
    """
    longitude = _normalize_longitude(longitude)

    sign_degree = longitude % 30.0

    # Each Navamsa = 10/3 degrees.
    # The shared helper applies the boundary tolerance so exact
    # boundaries such as 10°00'00" are classified into the next
    # Navamsa, and clamps the index so the result never exceeds 9.
    return _navamsa_index(sign_degree) + 1


#: Backward-compatible alias (pre-A-6 name). The 1-9 value is a
#: navamsa number, not a nakshatra pada; prefer navamsa_number.
navamsa_pada = navamsa_number


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
            navamsa_number=navamsa_number(planet.longitude),
        )

    return NavamsaChart(
        ascendant=ascendant,
        ascendant_sign=navamsa_sign(snapshot.houses.ascendant),
        planets=planets,
    )
