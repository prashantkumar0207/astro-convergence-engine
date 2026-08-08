"""
Exhaustive boundary, ULP-adversarial, and normalization tests for
the D1 division primitives (audit findings F-04, F-05, A-3).

Expected values come from exact rational arithmetic (fractions),
NOT from the production formulas: for a longitude expressed as an
exact Fraction, the division index is floor(value / span) with
span an exact rational, and a value within the documented 1e-10
tolerance below a boundary belongs to the next division.
"""

import math
from fractions import Fraction

import pytest

from engine.astrology.house import (
    equal_house_from_ascendant,
    whole_sign_house,
)
from engine.astrology.longitude_utils import (
    BOUNDARY_TOLERANCE,
    normalize_longitude,
)
from engine.astrology.nakshatra import nakshatra
from engine.astrology.pada import pada
from engine.astrology.signs import zodiac_sign

NAK_SPAN = Fraction(360, 27)  # exact 13 deg 20 min
PADA_SPAN = Fraction(360, 108)  # exact 3 deg 20 min
TOL = Fraction(1, 10**10)


def exact_index(value: float, span: Fraction, count: int) -> int:
    """Independent exact-arithmetic reference classification."""
    x = Fraction(repr(value)) % 360
    idx = int((x + TOL) / span)
    return min(idx, count - 1)


def offsets():
    return (-1e-9, -5e-11, -1e-11, -1e-12, -1e-13, 0.0,
            1e-13, 1e-12, 1e-11, 5e-11, 1e-9)


def test_every_nakshatra_boundary():
    for k in range(27):
        edge = float(k * NAK_SPAN)
        for d in offsets():
            x = edge + d
            expected = exact_index(x, NAK_SPAN, 27) + 1
            assert nakshatra(x) == expected, (x, k, d)


def test_every_pada_boundary():
    for k in range(108):
        edge = float(k * PADA_SPAN)
        for d in offsets():
            x = edge + d
            p = pada(x)
            assert 1 <= p <= 4
            # pada relative to the exactly-classified nakshatra
            nak_idx = exact_index(x, NAK_SPAN, 27)
            within = (Fraction(repr(x)) % 360) - nak_idx * NAK_SPAN
            if within < 0:
                within = Fraction(0)
            expected = min(int((within + TOL) / PADA_SPAN), 3) + 1
            assert p == expected, (x, k, d)


def test_classical_nakshatra_anchor_rohini_start():
    """40.0 degrees is the exact start of Rohini (nakshatra 4,
    pada 1). The pre-remediation code returned nakshatra 3,
    pada 4."""
    assert nakshatra(40.0) == 4
    assert pada(40.0) == 1


def test_every_sign_boundary():
    for k in range(12):
        edge = k * 30.0
        for d in offsets():
            x = edge + d
            expected = exact_index(x, Fraction(30), 12) + 1
            assert zodiac_sign(x) == expected, (x, k, d)


def test_ulp_adversarial_all_division_boundaries():
    violations = 0
    for k in range(1, 108):
        edge = float(k * PADA_SPAN)
        for direction in (0.0, 720.0):
            x = edge
            for _ in range(25):
                x = math.nextafter(x, direction)
                if not (1 <= nakshatra(x) <= 27):
                    violations += 1
                if not (1 <= pada(x) <= 4):
                    violations += 1
                if not (1 <= zodiac_sign(x) <= 12):
                    violations += 1
    assert violations == 0


@pytest.mark.parametrize(
    "value", [0.0, 360.0, 720.0, -360.0, -720.0, -1e-16, -1e-14,
              -1e-12, -0.001, 359.99999999999994]
)
def test_normalization_inputs_stay_in_range(value):
    normalized = normalize_longitude(value)
    assert 0.0 <= normalized < 360.0

    assert 1 <= zodiac_sign(value) <= 12
    assert 1 <= nakshatra(value) <= 27
    assert 1 <= pada(value) <= 4


def test_tiny_negative_classifies_as_zero_aries_ashwini():
    """Regression for zodiac_sign(-1e-16) == 13 and
    nakshatra(-1e-16) == 27 (audit finding F-04)."""
    for x in (-1e-16, -1e-15, -1e-14):
        assert zodiac_sign(x) == 1
        assert nakshatra(x) == 1
        assert pada(x) == 1


def test_equal_house_vs_whole_sign_are_distinct_rules():
    """Audit finding F-05 divergence case: asc 100.0 (Cancer 10),
    planet 95.0 (Cancer 5). Whole sign: same sign, house 1.
    Equal house: 355 degrees behind the ascendant, house 12."""
    assert whole_sign_house(95.0, 100.0) == 1
    assert equal_house_from_ascendant(95.0, 100.0) == 12


def test_whole_sign_house_all_offsets():
    for asc_sign in range(12):
        asc = asc_sign * 30.0 + 17.3
        for planet_sign in range(12):
            lon = planet_sign * 30.0 + 4.9
            expected = (planet_sign - asc_sign) % 12 + 1
            assert whole_sign_house(lon, asc) == expected


def test_equal_house_boundary_artifact_guarded():
    """(longitude - ascendant) % 360.0 can float to exactly 360.0;
    the house index must stay in 1..12."""
    asc = 100.0
    for x in (asc - 1e-16, asc - 1e-14, asc, asc + 1e-14):
        h = equal_house_from_ascendant(x, asc)
        assert 1 <= h <= 12


def test_aspect_normalizes_unnormalized_inputs():
    from engine.astronomy.aspects import aspect

    assert aspect(0, 730.0, 1, 10.0).angle == 0.0
    assert aspect(0, -10.0, 1, 10.0).angle == 20.0
    assert aspect(0, 370.0, 1, 190.0).angle == 180.0
    assert 0.0 <= aspect(0, -1234.5, 1, 987.6).angle <= 180.0


def test_boundary_tolerance_value_documented_and_sane():
    # Below ephemeris meaning (0.5 arcsec = 1.39e-4 deg), above
    # float noise (~1e-13 deg).
    assert 1e-13 < BOUNDARY_TOLERANCE < 1.39e-4
