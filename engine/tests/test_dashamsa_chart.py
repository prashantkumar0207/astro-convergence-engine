from fractions import Fraction

from engine.astrology.dashamsa_chart import (
    dashamsa_longitude,
    dashamsa_sign,
)


DASHAMSA_SIZE = Fraction(3, 1)

ODD_SIGNS = {
    0,  # Aries
    2,  # Gemini
    4,  # Leo
    6,  # Libra
    8,  # Sagittarius
    10,  # Aquarius
}

EVEN_SIGNS = {
    1,  # Taurus
    3,  # Cancer
    5,  # Virgo
    7,  # Scorpio
    9,  # Capricorn
    11,  # Pisces
}


def reference_start_sign(sign: int) -> int:
    """
    Independent Parashari Dashamsa rule.

    Odd sign:
        Start from the source sign.

    Even sign:
        Start from the 9th sign from the source sign.
    """
    if sign in ODD_SIGNS:
        return sign

    if sign in EVEN_SIGNS:
        return (sign + 8) % 12

    raise AssertionError(f"Invalid zodiac sign: {sign}")


def reference(longitude: float):
    """
    Independent reference calculation for Parashari D10.
    """
    x = Fraction(str(longitude)) % 360

    source_sign = int(x // 30)
    degree = x - source_sign * 30

    segment = int(degree / DASHAMSA_SIZE)

    if segment >= 10:
        segment = 9

    d10_sign = (
        reference_start_sign(source_sign) + segment
    ) % 12

    segment_start = segment * DASHAMSA_SIZE

    fraction = (
        degree - segment_start
    ) / DASHAMSA_SIZE

    d10_longitude = (
        Fraction(d10_sign * 30)
        + fraction * 30
    )

    return float(d10_longitude), d10_sign


def test_dashamsa_zero_degree_all_signs():
    for sign in range(12):
        longitude = sign * 30.0

        expected_longitude, expected_sign = reference(longitude)

        assert dashamsa_sign(longitude) == expected_sign
        assert abs(
            dashamsa_longitude(longitude)
            - expected_longitude
        ) < 1e-9


def test_dashamsa_all_120_segments():
    for sign in range(12):
        for segment in range(10):
            longitude = (
                sign * 30.0
                + segment * 3.0
                + 1.5
            )

            expected_longitude, expected_sign = reference(longitude)

            assert dashamsa_sign(longitude) == expected_sign
            assert abs(
                dashamsa_longitude(longitude)
                - expected_longitude
            ) < 1e-9


def test_dashamsa_exact_boundaries():
    for sign in range(12):
        for boundary in range(1, 10):
            longitude = sign * 30.0 + boundary * 3.0

            expected_longitude, expected_sign = reference(longitude)

            assert dashamsa_sign(longitude) == expected_sign
            assert abs(
                dashamsa_longitude(longitude)
                - expected_longitude
            ) < 1e-9


def test_dashamsa_just_below_and_above_boundaries():
    epsilon = 1e-9

    for sign in range(12):
        for boundary in range(1, 10):
            longitude = sign * 30.0 + boundary * 3.0

            below = longitude - epsilon
            above = longitude + epsilon

            expected_below = reference(below)
            expected_above = reference(above)

            assert dashamsa_sign(below) == expected_below[1]
            assert dashamsa_sign(above) == expected_above[1]

            assert abs(
                dashamsa_longitude(below)
                - expected_below[0]
            ) < 1e-8

            assert abs(
                dashamsa_longitude(above)
                - expected_above[0]
            ) < 1e-8


def test_dashamsa_full_circle_normalization():
    assert dashamsa_sign(360.0) == dashamsa_sign(0.0)
    assert dashamsa_longitude(360.0) == dashamsa_longitude(0.0)


def test_dashamsa_negative_longitude_normalization():
    expected_longitude, expected_sign = reference(-0.001)

    assert dashamsa_sign(-0.001) == expected_sign
    assert abs(
        dashamsa_longitude(-0.001)
        - expected_longitude
    ) < 1e-9


def test_dashamsa_parashari_odd_even_start_rules():
    # Odd signs start from themselves.
    assert dashamsa_sign(0.0) == 0       # Aries
    assert dashamsa_sign(60.0) == 2      # Gemini
    assert dashamsa_sign(120.0) == 4    # Leo
    assert dashamsa_sign(180.0) == 6    # Libra
    assert dashamsa_sign(240.0) == 8    # Sagittarius
    assert dashamsa_sign(300.0) == 10   # Aquarius

    # Even signs start from the 9th sign.
    assert dashamsa_sign(30.0) == 9     # Taurus -> Capricorn
    assert dashamsa_sign(90.0) == 11    # Cancer -> Pisces
    assert dashamsa_sign(150.0) == 1    # Virgo -> Taurus
    assert dashamsa_sign(210.0) == 3    # Scorpio -> Cancer
    assert dashamsa_sign(270.0) == 5    # Capricorn -> Virgo
    assert dashamsa_sign(330.0) == 7    # Pisces -> Scorpio


def test_dashamsa_odd_sign_progressions():
    expected = {
        0: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        2: [2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
        4: [4, 5, 6, 7, 8, 9, 10, 11, 0, 1],
        6: [6, 7, 8, 9, 10, 11, 0, 1, 2, 3],
        8: [8, 9, 10, 11, 0, 1, 2, 3, 4, 5],
        10: [10, 11, 0, 1, 2, 3, 4, 5, 6, 7],
    }

    for source_sign, expected_signs in expected.items():
        actual = [
            dashamsa_sign(
                source_sign * 30.0 + segment * 3.0
            )
            for segment in range(10)
        ]

        assert actual == expected_signs


def test_dashamsa_even_sign_progressions():
    expected = {
        1: [9, 10, 11, 0, 1, 2, 3, 4, 5, 6],
        3: [11, 0, 1, 2, 3, 4, 5, 6, 7, 8],
        5: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        7: [3, 4, 5, 6, 7, 8, 9, 10, 11, 0],
        9: [5, 6, 7, 8, 9, 10, 11, 0, 1, 2],
        11: [7, 8, 9, 10, 11, 0, 1, 2, 3, 4],
    }

    for source_sign, expected_signs in expected.items():
        actual = [
            dashamsa_sign(
                source_sign * 30.0 + segment * 3.0
            )
            for segment in range(10)
        ]

        assert actual == expected_signs


def test_dashamsa_classical_midpoint_anchors():
    cases = {
        1.5: 0,      # Aries 1°30' -> Aries
        34.5: 10,    # Taurus 4°30' -> Aquarius
        67.5: 4,     # Gemini 7°30' -> Leo
        100.5: 2,    # Cancer 10°30' -> Gemini
        133.5: 8,    # Leo 13°30' -> Sagittarius
        166.5: 6,    # Virgo 16°30' -> Libra
        199.5: 0,    # Libra 19°30' -> Aries
        232.5: 10,   # Scorpio 22°30' -> Aquarius
        265.5: 4,    # Sagittarius 25°30' -> Leo
        298.5: 2,    # Capricorn 28°30' -> Gemini
        301.5: 10,   # Aquarius 1°30' -> Aquarius
        334.5: 8,    # Pisces 4°30' -> Sagittarius
    }

    for longitude, expected_sign in cases.items():
        assert dashamsa_sign(longitude) == expected_sign