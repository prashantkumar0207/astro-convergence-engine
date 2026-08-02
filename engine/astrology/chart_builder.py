"""
Chart Builder
"""

from engine.astrology.chart_lagna_builder import build_chart_lagna
from engine.astrology.chart_planet_builder import build_chart_planet
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.chart import Chart
from engine.astrology.chart_house_builder import build_chart_house
from engine.astrology.chart_sign_builder import build_chart_sign
from engine.astrology.chart_nakshatra_builder import build_chart_nakshatra
from engine.astrology.chart_pada_builder import build_chart_pada


def build_chart(snapshot: AstronomySnapshot) -> Chart:
    ascendant = snapshot.houses.ascendant

    lagna = build_chart_lagna(ascendant)
    house_map = {
    i + 1: build_chart_house(i + 1, cusp)
    for i, cusp in enumerate(snapshot.houses.houses)
}
    sign_map = {
    i: build_chart_sign(i)
    for i in range(1, 13)
}
    nakshatra_map = {
    i: build_chart_nakshatra(i)
    for i in range(1, 28)
}
    pada_map = {
    i: build_chart_pada(i)
    for i in range(1, 109)
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