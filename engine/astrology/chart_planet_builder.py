"""
Chart Planet Builder
"""

from engine.astrology.chart_navamsa_builder import build_chart_navamsa
from engine.astrology.degrees import degree_in_sign
from engine.astrology.house import house_from_longitude
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
    pada_value = pada(planet.longitude)

    return ChartPlanet(
        name=name,
        longitude=planet.longitude,
        latitude=planet.latitude,
        speed=planet.speed_longitude,
        distance=planet.distance,
        retrograde=planet.speed_longitude < 0,
        sign=zodiac_sign(planet.longitude),
        degree=degree_in_sign(planet.longitude),
        house=house_from_longitude(
            planet.longitude,
            ascendant,
        ),
        nakshatra=nakshatra(planet.longitude),
        pada=pada_value,
        navamsa=build_chart_navamsa(
            longitude=planet.longitude,
            pada=pada_value,
        ),
    )