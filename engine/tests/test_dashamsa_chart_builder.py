from engine.astrology.dashamsa_chart import dashamsa_chart
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.ayanamsa import Ayanamsa
from engine.models.dashamsa_chart import DashamsaChart
from engine.models.dashamsa_planet import DashamsaPlanet
from engine.models.house_position import HousePosition
from engine.models.planet_collection import PlanetCollection
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def make_snapshot():
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

    sidereal_planets = {
        "Sun": SiderealPlanetPosition(
            longitude=0.0,
            latitude=0.0,
            distance=1.0,
            speed_longitude=1.0,
            speed_latitude=0.0,
            speed_distance=0.0,
        ),
        "Moon": SiderealPlanetPosition(
            longitude=31.5,
            latitude=0.0,
            distance=1.0,
            speed_longitude=13.0,
            speed_latitude=0.0,
            speed_distance=0.0,
        ),
        "Mars": SiderealPlanetPosition(
            longitude=61.5,
            latitude=0.0,
            distance=1.0,
            speed_longitude=0.5,
            speed_latitude=0.0,
            speed_distance=0.0,
        ),
    }

    return AstronomySnapshot(
        julian_day=2447719.968055556,
        planets=PlanetCollection(planets=()),
        houses=houses,
        ayanamsa=Ayanamsa(value=24.0, mode=1),
        sidereal_planets=sidereal_planets,
    )


def test_dashamsa_chart_returns_dashamsa_chart():
    snapshot = make_snapshot()

    result = dashamsa_chart(snapshot)

    assert isinstance(result, DashamsaChart)
    assert result.ascendant == 190.0
    assert result.ascendant_sign == 6
    assert set(result.planets) == {"Sun", "Moon", "Mars"}


def test_dashamsa_chart_builds_planet_models():
    snapshot = make_snapshot()

    result = dashamsa_chart(snapshot)

    sun = result.planets["Sun"]
    moon = result.planets["Moon"]
    mars = result.planets["Mars"]

    assert isinstance(sun, DashamsaPlanet)
    assert isinstance(moon, DashamsaPlanet)
    assert isinstance(mars, DashamsaPlanet)

    assert sun.name == "Sun"
    assert sun.longitude == 0.0
    assert sun.sign == 0
    assert sun.degree == 0.0
    assert sun.segment == 1

    assert moon.name == "Moon"
    assert moon.longitude == 285.0
    assert moon.sign == 9
    assert moon.degree == 15.0
    assert moon.segment == 1

    assert mars.name == "Mars"
    assert mars.longitude == 195.0
    assert mars.sign == 6
    assert mars.degree == 15.0
    assert mars.segment == 1


def test_dashamsa_chart_preserves_planet_names():
    snapshot = make_snapshot()

    result = dashamsa_chart(snapshot)

    assert list(result.planets) == ["Sun", "Moon", "Mars"]