from engine.astronomy.astronomy_pipeline import astronomy_pipeline
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.planet_collection import PlanetCollection
from engine.models.house_position import HousePosition
from engine.models.ayanamsa import Ayanamsa


def test_pipeline_returns_model():

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

    planets = PlanetCollection(planets=())
    sidereal_planets = ()

    ayanamsa = Ayanamsa(
        value=24.0,
        mode=1,
    )

    snapshot = AstronomySnapshot(
    julian_day=2447719.968055556,
    planets=planets,
    houses=houses,
    ayanamsa=ayanamsa,
    sidereal_planets=sidereal_planets,
    )

    result = astronomy_pipeline(
        snapshot=snapshot,
        aspects=(),
    )

    assert result.snapshot == snapshot
    assert result.aspects == ()