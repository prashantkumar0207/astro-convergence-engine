"""
Real-birth end-to-end integration tests (audit CRITICAL missing
test 4): the full pipeline BirthData -> validated time -> JD ->
sidereal snapshot -> D1 chart, with every assertion derived
INDEPENDENTLY of the engine:

- Sidereal longitudes from the bundled swetest 2.10.03 binary
  (-b12.7.1989 -ut11:14:00 -eswe -sid1 -house85.1376,25.5941,P):
  Sun 86.3688406, Moon 192.3040141, Ascendant 239.0275081.
- Sign / nakshatra / pada / navamsa classifications derived by
  hand from the classical definitions in the comments below.
"""

from engine.astrology.chart_builder import build_chart
from engine.astrology.chart_factory import build_all_charts
from engine.astrology.navamsa_chart import navamsa_chart
from engine.calculations.calculations import calculate
from engine.models.birth_data import BirthData
from engine.models.chart import Chart


BIRTH = BirthData(
    year=1989,
    month=7,
    day=12,
    hour=16,
    minute=44,
    second=0.0,
    latitude=25.5941,
    longitude=85.1376,
    timezone="Asia/Kolkata",
)


def build():
    snapshot = calculate(BIRTH).snapshot
    return snapshot, build_chart(snapshot)


def test_lagna_independently_derived():
    # Ascendant 239.0275 -> floor(239.03/30)+1 = sign 8 Scorpio.
    # Nakshatra: 239.0275 / (360/27) = 17.93 -> 18 Jyeshtha.
    # Pada: within-nakshatra 12.36 deg / (360/108) = 3.7 -> pada 4.
    _, chart = build()

    assert chart.lagna.sign == 8
    assert chart.lagna.nakshatra == 18
    assert chart.lagna.nakshatra_pada == 4
    assert abs(chart.ascendant - 239.0275081) * 3600 < 0.5


def test_sun_independently_derived():
    # Sun 86.36884 -> sign 3 Gemini, degree 26.3688.
    # Whole-sign house from Scorpio lagna: (3-8) mod 12 + 1 = 8.
    # Nakshatra: 86.3688/13.3333 = 6.48 -> 7 Punarvasu.
    # Pada: within 6.3688 / 3.3333 = 1.91 -> pada 2.
    # Navamsa: 26.3688/3.3333 = 7.91 -> navamsa number 8;
    #   Gemini is dual -> D9 count starts Libra(6); (6+7)%12 = 1
    #   -> Taurus.
    _, chart = build()

    sun = chart.planets["Sun"]

    assert abs(sun.longitude - 86.3688406) * 3600 < 0.5
    assert sun.sign == 3
    assert abs(sun.degree - 26.3688406) < 0.001
    assert sun.house == 8
    assert sun.nakshatra == 7
    assert sun.nakshatra_pada == 2
    assert sun.navamsa.navamsa_number == 8
    assert sun.navamsa.sign == 1
    assert sun.retrograde is False


def test_moon_independently_derived():
    # Moon 192.30401 -> sign 7 Libra, degree 12.304.
    # Whole-sign house: (7-8) mod 12 + 1 = 12.
    # Nakshatra: 192.304/13.3333 = 14.42 -> 15 Swati.
    # Pada: within 5.637 / 3.3333 = 1.69 -> pada 2.
    # Navamsa: 12.304/3.3333 = 3.69 -> number 4; Libra movable ->
    #   starts Libra(6); (6+3)%12 = 9 -> Capricorn.
    _, chart = build()

    moon = chart.planets["Moon"]

    assert abs(moon.longitude - 192.3040141) * 3600 < 0.5
    assert moon.sign == 7
    assert moon.house == 12
    assert moon.nakshatra == 15
    assert moon.nakshatra_pada == 2
    assert moon.navamsa.navamsa_number == 4
    assert moon.navamsa.sign == 9


def test_rahu_ketu_opposition_preserved_end_to_end():
    _, chart = build()

    rahu = chart.planets["Rahu"]
    ketu = chart.planets["Ketu"]

    assert abs((ketu.longitude - rahu.longitude) % 360.0 - 180.0) < 1e-9
    assert rahu.retrograde and ketu.retrograde


def test_nakshatra_map_is_complete_and_self_consistent():
    # Regression for audit F-03 (all 27 entries collapsed to 1-3).
    _, chart = build()

    assert sorted(chart.nakshatra_map.keys()) == list(range(1, 28))

    for number, entry in chart.nakshatra_map.items():
        assert entry.number == number
        assert abs(entry.end - entry.start - 360.0 / 27.0) < 1e-9

    assert chart.nakshatra_map[4].name == "Rohini"
    assert chart.nakshatra_map[27].name == "Revati"


def test_embedded_navamsa_agrees_with_standalone_d9_chart():
    # Regression for audit F-09: the D1-embedded navamsa summary
    # and the standalone D9 chart must agree for every planet.
    snapshot, chart = build()

    d9 = navamsa_chart(snapshot)

    for name, planet in chart.planets.items():
        assert planet.navamsa.sign == d9.planets[name].sign, name
        assert (
            planet.navamsa.navamsa_number
            == d9.planets[name].navamsa_number
        ), name


def test_factory_returns_real_charts_for_all_supported_keys():
    snapshot, _ = build()

    charts = build_all_charts(snapshot)

    assert isinstance(charts["D1"], Chart)
    assert charts["D1"].planets["Sun"].sign == 3
    assert charts["D9"].planets["Sun"].sign == 1
    assert type(charts["D10"]).__name__ == "DashamsaChart"


def test_chart_utilities_work_on_real_chart():
    # Regression for audit F-08 (AttributeError on real charts).
    from engine.astrology.chart_index import chart_index
    from engine.astrology.chart_json import chart_json
    from engine.astrology.chart_lookup import planet as lookup
    from engine.astrology.chart_mapper import map_chart
    from engine.astrology.chart_sort import sort_chart

    snapshot, chart = build()

    assert chart_index(chart)["Sun"].sign == 3
    assert lookup(chart, "Moon").nakshatra == 15

    ordered = sort_chart(chart)
    longitudes = [p.longitude for p in ordered]
    assert longitudes == sorted(longitudes)

    mapped = map_chart(snapshot)
    assert len(mapped) == 14

    assert isinstance(chart_json(chart), str)
