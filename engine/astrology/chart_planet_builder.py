"""
Chart Planet Builder

House rule: WHOLE SIGN (the documented project decision for the
Parashari D1 chart; audit A-2). Equal-house and Placidus cusp
data remain available separately and are never mixed in here.
"""

from engine.astrology.chart_navamsa_builder import build_chart_navamsa
from engine.astrology.degrees import degree_in_sign
from engine.astrology.house import whole_sign_house
from engine.astrology.nakshatra import nakshatra
from engine.astrology.pada import pada
from engine.astrology.signs import zodiac_sign
from engine.models.chart_planet import ChartPlanet
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def build_chart_planet(
    name: str,
    planet: SiderealPlanetPosition,
    ascendant: float,
) -> ChartPlanet:
    return ChartPlanet(
        name=name,
        longitude=planet.longitude,
        latitude=planet.latitude,
        speed=planet.speed_longitude,
        distance=planet.distance,
        retrograde=planet.speed_longitude < 0,
        sign=zodiac_sign(planet.longitude),
        degree=degree_in_sign(planet.longitude),
        house=whole_sign_house(
            planet.longitude,
            ascendant,
        ),
        nakshatra=nakshatra(planet.longitude),
        nakshatra_pada=pada(planet.longitude),
        navamsa=build_chart_navamsa(planet.longitude),
    )
