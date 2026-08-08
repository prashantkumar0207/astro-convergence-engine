from engine.astrology.divisional_chart import divisional_chart
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.planet_collection import PlanetCollection
from engine.models.house_position import HousePosition
from engine.models.ayanamsa import Ayanamsa
from engine.models.navamsa_chart import NavamsaChart
from engine.models.dashamsa_chart import DashamsaChart


def make_snapshot() -> AstronomySnapshot:
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

    return AstronomySnapshot(
        julian_day=2447719.968055556,
        planets=PlanetCollection(planets={}),
        houses=houses,
        ayanamsa=Ayanamsa(value=24.0, mode=1),
        sidereal_planets={},
    )


def test_divisional_chart_dispatches_d9_to_navamsa():
    snapshot = make_snapshot()

    result = divisional_chart(snapshot, division=9)

    assert isinstance(result, NavamsaChart)
    assert result.ascendant == 180.0
    assert result.ascendant_sign == 6
    assert result.planets == {}


def test_divisional_chart_dispatches_d10_to_dashamsa():
    snapshot = make_snapshot()

    result = divisional_chart(snapshot, division=10)

    assert isinstance(result, DashamsaChart)
    assert result.ascendant == 70.0
    assert result.ascendant_sign == 2
    assert result.planets == {}


def test_divisional_chart_rejects_unsupported_divisions():
    # Spec-correct replacement (audit F-15): the old test locked
    # in the silent D1 passthrough for unimplemented vargas.
    import pytest

    from engine.astrology.divisional_chart import UnsupportedVargaError

    snapshot = make_snapshot()

    for division in (2, 7, 12, 60):
        with pytest.raises(UnsupportedVargaError):
            divisional_chart(snapshot, division=division)

    with pytest.raises(UnsupportedVargaError):
        divisional_chart(snapshot, division=13)  # not a varga at all


def test_divisional_chart_dispatches_d1_to_real_chart():
    from engine.models.chart import Chart

    snapshot = make_snapshot()

    result = divisional_chart(snapshot, division=1)

    assert isinstance(result, Chart)
    assert result.chart_type == "D1"