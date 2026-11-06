"""M-09 (G1 audit; ADR-0112 s3): every varga layer takes its parent sign by D1's rule.

The defect: inside the 1e-10 window below a sign boundary, D1 (zodiac_sign) promoted the value to
the next sign, while classify(), D9 and D10 took the source sign by plain floor. Two facts that
should share a parent sign did not. The certified sweeps stepped around this by probing at
+0.0007. These tests probe the window exactly: at, just inside and just outside every boundary.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from engine.astrology.dashamsa_chart import dashamsa_longitude, dashamsa_sign  # noqa: E402
from engine.astrology.longitude_utils import BOUNDARY_TOLERANCE  # noqa: E402
from engine.astrology.navamsa_chart import navamsa_longitude, navamsa_number, navamsa_sign  # noqa: E402
from engine.astrology.signs import zodiac_sign  # noqa: E402
from engine.astrology.varga_classifier import classify  # noqa: E402
from engine.astrology.varga_registry import get_varga_rule, registered_vargas  # noqa: E402

BOUNDARIES = [30.0 * k for k in range(1, 12)]
RULES = {division: get_varga_rule(division, school) for division, school in registered_vargas()}


def inside(boundary):
    """Points the convention promotes: within the tolerance below the boundary."""

    return [math.nextafter(boundary, -math.inf), boundary - 5e-11, boundary - 0.9 * BOUNDARY_TOLERANCE]


def outside(boundary):
    """Points just below the window, which must stay in the previous sign."""

    return [boundary - 1.01 * BOUNDARY_TOLERANCE, boundary - 2e-10, boundary - 1e-9]


def d1_parent(longitude):
    return zodiac_sign(longitude) - 1


def layers_agree_with_d1(parent_of) -> bool:
    """True if ``parent_of`` gives D1's parent sign at every boundary, inside and outside the window."""

    for boundary in BOUNDARIES:
        for longitude in [boundary, *inside(boundary), *outside(boundary)]:
            if parent_of(longitude) != d1_parent(longitude):
                return False
    return True


def test_parent_sign_is_d1s_rule():
    from engine.astrology.longitude_utils import parent_sign

    assert layers_agree_with_d1(parent_sign)


@pytest.mark.parametrize("boundary", BOUNDARIES)
@pytest.mark.parametrize("division", sorted(RULES))
def test_a_window_value_classifies_as_the_boundary_itself(boundary, division):
    """Promoted to the next sign at degree 0: the same output as the exact boundary."""

    rule = RULES[division]
    at = classify(boundary, rule)
    for longitude in inside(boundary):
        assert classify(longitude, rule) == at, (division, longitude)


@pytest.mark.parametrize("boundary", BOUNDARIES)
def test_d9_and_d10_promote_with_d1(boundary):
    for longitude in inside(boundary):
        assert navamsa_sign(longitude) == navamsa_sign(boundary)
        assert navamsa_longitude(longitude) == navamsa_longitude(boundary)
        assert navamsa_number(longitude) == navamsa_number(boundary) == 1
        assert dashamsa_sign(longitude) == dashamsa_sign(boundary)
        assert dashamsa_longitude(longitude) == dashamsa_longitude(boundary)


@pytest.mark.parametrize("boundary", BOUNDARIES)
def test_values_outside_the_window_keep_their_sign(boundary):
    for longitude in outside(boundary):
        assert d1_parent(longitude) == int(longitude // 30.0)
        assert navamsa_number(longitude) == 9


@pytest.mark.parametrize("longitude", [b for boundary in BOUNDARIES for b in (boundary, *inside(boundary),
                                                                              *outside(boundary))]
                         + [0.0, 1e-12, 359.99999999995, math.nextafter(360.0, -math.inf), 123.456])
def test_d9_and_d10_sign_and_longitude_agree(longitude):
    assert int(navamsa_longitude(longitude) // 30.0) == navamsa_sign(longitude)
    assert int(dashamsa_longitude(longitude) // 30.0) == dashamsa_sign(longitude)


def test_the_top_edge_clamps_to_pisces_as_d1_does():
    from engine.astrology.longitude_utils import parent_sign

    for longitude in (359.99999999995, math.nextafter(360.0, -math.inf)):
        assert zodiac_sign(longitude) == 12 and parent_sign(longitude) == 11


@pytest.mark.parametrize("full_turn", [360.0, 720.0, -360.0])
def test_exactly_360_degrees_is_aries_in_every_layer(full_turn):
    """Regression: a full turn normalizes to 0 degrees, Aries, in D1 and every varga layer alike."""

    from engine.astrology.longitude_utils import parent_sign

    assert zodiac_sign(full_turn) == 1 and parent_sign(full_turn) == 0
    assert navamsa_sign(full_turn) == navamsa_sign(0.0) and navamsa_longitude(full_turn) == navamsa_longitude(0.0)
    assert dashamsa_sign(full_turn) == dashamsa_sign(0.0) and dashamsa_longitude(full_turn) == dashamsa_longitude(0.0)
    for rule in RULES.values():
        assert classify(full_turn, rule) == classify(0.0, rule)


@pytest.mark.parametrize("longitude", [math.nextafter(360.0, -math.inf), 360.0 - 5e-11, 360.0 - 2e-10])
def test_values_immediately_below_360_stay_in_pisces(longitude):
    from engine.astrology.longitude_utils import parent_sign

    assert zodiac_sign(longitude) == 12 and parent_sign(longitude) == 11
    for rule in RULES.values():
        result, pisces = classify(longitude, rule), classify(359.9999, rule)
        assert (result.d_sign, result.division_index) == (pisces.d_sign, pisces.division_index)
        assert (result.d_sign, result.division_index) != (classify(0.0, rule).d_sign, 0)


def test_the_check_rejects_the_superseded_floor_rule():
    """The historical source-sign floor is exactly what this suite must refuse."""

    assert not layers_agree_with_d1(lambda longitude: int(longitude // 30.0))
    assert not layers_agree_with_d1(lambda longitude: d1_parent(longitude) + (1 if longitude % 30 > 29.9 else 0))
