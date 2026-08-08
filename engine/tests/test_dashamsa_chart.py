from fractions import Fraction

from engine.astrology.dashamsa_chart import (
    dashamsa_longitude,
    dashamsa_sign,
)


DASHAMSA_SIZE = Fraction(3, 1)

MOVABLE = {0, 3, 6, 9}
FIXED = {1, 4, 7, 10}


def reference_start_sign(sign: int) -> int:
    if sign in MOVABLE:
        return sign

    if sign in FIXED:
        return (sign + 8) % 12

    return (sign + 4) % 12


def reference(longitude: float):
    x = Fraction(str(longitude)) % 360

    sign = int(x // 30)
    degree = x - sign * 30

    segment = int(degree / DASHAMSA_SIZE)

    start_sign = reference_start_sign(sign)
    d10_sign = (start_sign + segment) % 12

    segment_start = segment * DASHAMSA_SIZE
    fraction = (degree - segment_start) / DASHAMSA_SIZE

    d10_longitude = Fraction(d10_sign * 30) + fraction * 30

    return float(d10_longitude), d10_sign


def test_dashamsa_zero_degree_all_signs():
    for sign in range(12):
        longitude = sign * 30.0

        expected_longitude, expected_sign = reference(longitude)

        assert dashamsa_sign(longitude) == expected_sign
        assert dashamsa_longitude(longitude) == expected_longitude


def test_dashamsa_all_120_segments():
    for sign in range(12):
        for segment in range(10):
            longitude = sign * 30.0 + segment * 3.0 + 1.5

            expected_longitude, expected_sign = reference(longitude)

            assert dashamsa_sign(longitude) == expected_sign
            assert dashamsa_longitude(longitude) == expected_longitude


def test_dashamsa_exact_boundaries():
    for sign in range(12):
        for boundary in range(1, 10):
            longitude = sign * 30.0 + boundary * 3.0

            expected_longitude, expected_sign = reference(longitude)

            assert dashamsa_sign(longitude) == expected_sign
            assert dashamsa_longitude(longitude) == expected_longitude


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


def test_dashamsa_full_circle_normalization():
    assert dashamsa_sign(360.0) == dashamsa_sign(0.0)
    assert dashamsa_longitude(360.0) == dashamsa_longitude(0.0)


def test_dashamsa_negative_longitude_normalization():
    expected_longitude, expected_sign = reference(-0.001)

    assert dashamsa_sign(-0.001) == expected_sign
    assert dashamsa_longitude(-0.001) == expected_longitude


def test_dashamsa_modality_start_rules():
    # Movable signs: start from themselves.
    assert dashamsa_sign(0.0) == 0
    assert dashamsa_sign(90.0) == 3

    # Fixed signs: start from the 9th sign.
    assert dashamsa_sign(30.0) == 9
    assert dashamsa_sign(120.0) == 0

    # Dual signs: start from the 5th sign.
    assert dashamsa_sign(60.0) == 6
    assert dashamsa_sign(150.0) == 9


def test_dashamsa_movable_progression():
    expected = list(range(10))

    actual = [
        dashamsa_sign(segment * 3.0)
        for segment in range(10)
    ]

    assert actual == expected


def test_dashamsa_fixed_progression():
    expected = [9, 10, 11, 0, 1, 2, 3, 4, 5, 6]

    actual = [
        dashamsa_sign(30.0 + segment * 3.0)
        for segment in range(10)
    ]

    assert actual == expected


def test_dashamsa_dual_progression():
    expected = [6, 7, 8, 9, 10, 11, 0, 1, 2, 3]

    actual = [
        dashamsa_sign(60.0 + segment * 3.0)
        for segment in range(10)
    ]

    assert actual == expected
