"""
Chart Builder
"""

from engine.astrology.chart_house_builder import build_chart_house
from engine.astrology.chart_lagna_builder import build_chart_lagna
from engine.astrology.chart_nakshatra_builder import build_chart_nakshatra
from engine.astrology.chart_pada_builder import build_chart_pada
from engine.astrology.chart_planet_builder import build_chart_planet
from engine.astrology.chart_sign_builder import build_chart_sign
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.chart import Chart


def build_chart(snapshot: AstronomySnapshot) -> Chart:
    """
    Build a D1 chart from an astronomy snapshot.
    """

    ascendant = snapshot.houses.ascendant

    lagna = build_chart_lagna(ascendant)

    house_map = {
        house_number: build_chart_house(house_number, cusp)
        for house_number, cusp in enumerate(snapshot.houses.houses, start=1)
    }

    sign_map = {
        sign_number: build_chart_sign(sign_number)
        for sign_number in range(1, 13)
    }

    nakshatra_map = {
        nakshatra_number: build_chart_nakshatra(nakshatra_number)
        for nakshatra_number in range(1, 28)
    }

    pada_map = {
        pada_number: build_chart_pada(pada_number)
        for pada_number in range(1, 109)
    }

    planets = {
        name: build_chart_planet(
            name=name,
            planet=planet,
            ascendant=ascendant,
        )
        for name, planet in snapshot.sidereal_planets.items()
    }

    return Chart(
        chart_type="D1",
        ascendant=ascendant,
        lagna=lagna,
        house_map=house_map,
        sign_map=sign_map,
        nakshatra_map=nakshatra_map,
        pada_map=pada_map,
        ayanamsa=snapshot.ayanamsa.value,
        houses=snapshot.houses,
        planets=planets,
    )