from engine.astrology.chart_planet_builder import build_chart_planet
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def test_chart_planet_builder():
    planet = SiderealPlanetPosition(
        longitude=125.5,
        latitude=0.0,
        distance=1.0,
        speed_longitude=1.0,
        speed_latitude=0.0,
        speed_distance=0.0,
    )

    result = build_chart_planet(
        name="Sun",
        planet=planet,
        ascendant=95.0,
    )

    assert result.name == "Sun"
    assert result.sign == 5
    assert result.house == 2