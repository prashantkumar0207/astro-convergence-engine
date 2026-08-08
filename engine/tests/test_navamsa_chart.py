from engine.astrology.navamsa_chart import (
    navamsa_chart,
    navamsa_longitude,
    navamsa_pada,
    navamsa_sign,
)
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.planet_collection import PlanetCollection
from engine.models.house_position import HousePosition
from engine.models.ayanamsa import Ayanamsa
from engine.models.navamsa_chart import NavamsaChart
from engine.models.sidereal_planet_position import SiderealPlanetPosition


def make_snapshot(ascendant=100.0, sidereal_planets=None):
    houses = HousePosition(
        ascendant=ascendant,
        mc=190.0,
        armc=180.0,
        vertex=200.0,
        equatorial_ascendant=100.0,
        co_ascendant=110.0,
        polar_ascendant=120.0,
        houses=(
            0.0, 30.0, 60.0, 90.0, 120.0, 150.0,
            180.0, 210.0, 240.0, 270.0, 300.0, 330.0,
        ),
    )

    return AstronomySnapshot(
        julian_day=2447719.968055556,
        planets=PlanetCollection(planets={}),
        houses=houses,
        ayanamsa=Ayanamsa(value=24.0, mode=1),
        sidereal_planets=sidereal_planets or {},
    )


def test_navamsa_chart_builds_d9_chart():
    result = navamsa_chart(make_snapshot())

    assert isinstance(result, NavamsaChart)
    assert result.ascendant == 180.0
    assert result.ascendant_sign == 6
    assert result.planets == {}


def test_navamsa_longitude_uses_movable_fixed_and_dual_rules():
    assert navamsa_longitude(0.0) == 0.0
    assert navamsa_longitude(30.0) == 270.0
    assert navamsa_longitude(60.0) == 180
    assert navamsa_longitude(90.0) == 90.0


def test_navamsa_sign_and_pada_are_consistent():
    assert navamsa_sign(100.0) == 6
    assert navamsa_longitude(100.0) == 180.0
    assert navamsa_pada(100.0) == 4


def test_navamsa_chart_maps_sidereal_planets():
    sun = SiderealPlanetPosition(
        longitude=180.0,
        latitude=0.0,
        distance=1.0,
        speed_longitude=1.0,
        speed_latitude=0.0,
        speed_distance=0.0,
    )

    result = navamsa_chart(make_snapshot(sidereal_planets={"Sun": sun}))

    assert result.planets["Sun"].name == "Sun"
    assert result.planets["Sun"].longitude == 180.0
    assert result.planets["Sun"].sign == 6
    assert result.planets["Sun"].degree == 0.0
    assert result.planets["Sun"].pada == 1

def test_navamsa_exact_boundaries():
    # Each Navamsa is exactly 3°20' = 10/3 degrees.
    #
    # 100° = Cancer 10° exactly.
    # Cancer is movable, so its Navamsas start from Cancer:
    # Cancer, Leo, Virgo, Libra, ...
    #
    # Therefore Cancer 10° belongs to Libra D9.

    assert navamsa_pada(100.0) == 4
    assert navamsa_sign(100.0) == 6
    assert navamsa_longitude(100.0) == 180.0

    # Cancer 20° = beginning of the 7th Navamsa.
    assert navamsa_pada(110.0) == 7
    assert navamsa_sign(110.0) == 9
    assert navamsa_longitude(110.0) == 270.0

    # Taurus 10°.
    # Taurus is fixed and its Navamsas start from Capricorn:
    # Capricorn, Aquarius, Pisces, Aries, ...
    assert navamsa_pada(40.0) == 4
    assert navamsa_sign(40.0) == 0
    assert navamsa_longitude(40.0) == 0.0

    # Gemini 10°.
    # Gemini is dual and its Navamsas start from Libra:
    # Libra, Scorpio, Sagittarius, Capricorn, ...
    assert navamsa_pada(70.0) == 4
    assert navamsa_sign(70.0) == 9
    assert navamsa_longitude(70.0) == 270.0

def test_navamsa_longitude_stays_in_canonical_range():
    """
    D9 longitude must always be in [0, 360).
    """
    test_longitudes = [
        0.0,
        1.5,
        29.99999999999,
        29.99999999999999,
        30.0,
        359.99999999999994,
        360.0,
        720.0,
        -360.0,
        -720.0,
        -0.001,
        -1e-16,
        -1e-15,
        -1e-14,
        -1e-12,
        -1e-10,
        1e-16,
        1e-12,
    ]

    for longitude in test_longitudes:
        result = navamsa_longitude(longitude)

        assert 0.0 <= result < 360.0


def test_navamsa_tiny_negative_longitudes_normalize_to_aries():
    """
    A tiny negative longitude represents the 0 Aries boundary
    and must not leak an out-of-range sign index through
    float-modulo returning exactly 360.0.
    """
    for longitude in (-1e-16, -1e-15, -1e-14):
        assert navamsa_sign(longitude) == 0
        assert navamsa_longitude(longitude) == 0.0
        assert navamsa_pada(longitude) == 1


def test_navamsa_pada_always_in_range():
    """
    Navamsa pada must always be within 1..9.
    """
    step = 30.0 / 9.0

    test_longitudes = [
        0.0,
        29.99999999999,
        29.99999999999999,
        30.0,
        -1e-16,
        -1e-12,
        -1e-10,
        -0.001,
    ]

    for sign in range(12):
        for boundary in range(10):
            edge = sign * 30.0 + boundary * step

            for offset in (
                -1e-9, -1e-11, -1e-12, -1e-15,
                0.0,
                1e-15, 1e-12, 1e-11, 1e-9,
            ):
                test_longitudes.append(edge + offset)

    for longitude in test_longitudes:
        pada = navamsa_pada(longitude)

        assert 1 <= pada <= 9


def test_navamsa_sign_and_longitude_remain_consistent_near_boundaries():
    """
    The continuous D9 longitude and the D9 sign must describe
    the same zodiac sign, including for values immediately
    below a Navamsa boundary where the boundary tolerance
    promotes the value into the next Navamsa.
    """
    step = 30.0 / 9.0

    for sign in range(12):
        for boundary in range(1, 9):
            edge = sign * 30.0 + boundary * step

            for offset in (
                -1e-9, -1e-11, -1e-12, -1e-13,
                0.0,
                1e-13, 1e-12, 1e-11, 1e-9,
            ):
                longitude = edge + offset

                transformed = navamsa_longitude(longitude)
                d9_sign = navamsa_sign(longitude)

                assert 0.0 <= transformed < 360.0
                assert int(transformed // 30.0) % 12 == d9_sign
