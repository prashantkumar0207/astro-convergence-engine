"""
Planet Collection Engine

Computes deterministic tropical positions for all supported
celestial bodies.

Canonical planet identity (remediates audit finding F-14 / A-5):

- The nine classical Vedic grahas are Sun, Moon, Mars, Mercury,
  Jupiter, Venus, Saturn, Rahu, Ketu.
- Rahu is the lunar node selected by the node policy ("mean" by
  default, matching the certified legacy profile; "true" is
  available). Ketu is ALWAYS derived as Rahu + 180 degrees, with
  Rahu's speed (the mean node's actual retrograde rate; the legacy
  kernel's hard-coded -1.0 placeholder speed is not reproduced).
- The raw nodes (MeanNode, TrueNode) and the outer planets
  (Uranus, Neptune, Pluto) are additionally exposed for
  astronomical completeness; Vedic layers should consume the
  canonical names.
"""

from __future__ import annotations

import swisseph as swe

from engine.astronomy.planet_positions import planet_position
from engine.models.planet_collection import PlanetCollection
from engine.models.planet_position import PlanetPosition


#: Direct Swiss Ephemeris bodies (no derivation involved).
PLANET_BODIES = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mercury": swe.MERCURY,
    "Venus": swe.VENUS,
    "Mars": swe.MARS,
    "Jupiter": swe.JUPITER,
    "Saturn": swe.SATURN,
    "Uranus": swe.URANUS,
    "Neptune": swe.NEPTUNE,
    "Pluto": swe.PLUTO,
    "MeanNode": swe.MEAN_NODE,
    "TrueNode": swe.TRUE_NODE,
}

#: The nine classical grahas every Vedic layer should consume.
CANONICAL_GRAHAS = (
    "Sun",
    "Moon",
    "Mars",
    "Mercury",
    "Jupiter",
    "Venus",
    "Saturn",
    "Rahu",
    "Ketu",
)


def derive_ketu(rahu: PlanetPosition) -> PlanetPosition:
    """Ketu is the point opposite Rahu on the ecliptic."""
    return PlanetPosition(
        longitude=(rahu.longitude + 180.0) % 360.0,
        latitude=-rahu.latitude,
        distance=rahu.distance,
        speed_longitude=rahu.speed_longitude,
        speed_latitude=-rahu.speed_latitude,
        speed_distance=rahu.speed_distance,
    )


def planet_collection(
    julian_day: float,
    node_policy: str = "mean",
) -> PlanetCollection:
    """
    Compute deterministic tropical positions for all supported
    planets, including the canonical Rahu/Ketu pair.
    """

    if not isinstance(julian_day, (int, float)):
        raise TypeError("julian_day must be numeric.")

    if node_policy not in ("mean", "true"):
        raise ValueError("node_policy must be 'mean' or 'true'.")

    planets = {
        name: planet_position(julian_day, body)
        for name, body in PLANET_BODIES.items()
    }

    rahu_source = "MeanNode" if node_policy == "mean" else "TrueNode"

    planets["Rahu"] = planets[rahu_source]
    planets["Ketu"] = derive_ketu(planets[rahu_source])

    return PlanetCollection(planets=planets)
