from engine.astrology.chart_factory import build_all_charts
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.planet_collection import PlanetCollection
from engine.models.house_position import HousePosition
from engine.models.ayanamsa import Ayanamsa
from engine.models.navamsa_chart import NavamsaChart
from engine.models.dashamsa_chart import DashamsaChart
from engine.models.chart import Chart


def test_chart_factory_builds_supported_charts():
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
        planets=PlanetCollection(planets={}),
        houses=houses,
        ayanamsa=Ayanamsa(value=24.0, mode=1),
        sidereal_planets={},
    )

    charts = build_all_charts(snapshot)

    # Supported chart keys
    assert "D1" in charts
    assert "D9" in charts
    assert "D10" in charts

    # D1 is now the real Rashi chart (audit section 5: the
    # factory previously routed D1 to a placeholder that echoed
    # the snapshot).
    assert isinstance(charts["D1"], Chart)
    assert charts["D1"].chart_type == "D1"
    assert charts["D1"] != snapshot

    # D9 is a dedicated Navamsa representation
    assert isinstance(charts["D9"], NavamsaChart)
    assert charts["D9"] != snapshot

    # D10 is a dedicated Dashamsa representation
    assert isinstance(charts["D10"], DashamsaChart)
    assert charts["D10"] != snapshot