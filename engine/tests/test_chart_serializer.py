from engine.models.ayanamsa import Ayanamsa
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.house_position import HousePosition
from engine.models.planet_collection import PlanetCollection

from engine.astrology.chart_serializer import serialize_chart


def test_chart_serializer():
    houses = HousePosition(
        ascendant=100,
        mc=190,
        armc=180,
        vertex=200,
        equatorial_ascendant=100,
        co_ascendant=110,
        polar_ascendant=120,
        houses=(0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330),
    )

    snapshot = AstronomySnapshot(
        julian_day=1,
        planets=PlanetCollection(planets=()),
        houses=houses,
        ayanamsa=Ayanamsa(value=24, mode=1),
        sidereal_planets=(),
    )

    assert isinstance(serialize_chart(snapshot), dict)