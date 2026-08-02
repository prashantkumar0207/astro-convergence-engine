from engine.astrology.divisional_chart import divisional_chart
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.planet_collection import PlanetCollection
from engine.models.house_position import HousePosition
from engine.models.ayanamsa import Ayanamsa


def test_divisional_chart_returns_snapshot():
    houses = HousePosition(
        ascendant=100.0,
        mc=190.0,
        armc=180.0,
        vertex=200.0,
        equatorial_ascendant=100.0,
        co_ascendant=110.0,
        polar_ascendant=120.0,
        houses=(
            0.0,
            30.0,
            60.0,
            90.0,
            120.0,
            150.0,
            180.0,
            210.0,
            240.0,
            270.0,
            300.0,
            330.0,
        ),
    )

    snapshot = AstronomySnapshot(
        julian_day=2447719.968055556,
        planets=PlanetCollection(planets=()),
        houses=houses,
        ayanamsa=Ayanamsa(value=24.0, mode=1),
        sidereal_planets=(),
    )

    result = divisional_chart(snapshot, division=9)

    assert result == snapshot