"""
KP legacy equivalence gate (Gate 1 of ADR-KP-001).

The certified legacy kernel (legacy/kp.py) is the equivalence ORACLE:
engine/kp must reproduce its (SL, NL, SB, SS) classification exactly,
with zero categorical tolerance (DECISION_LOG D-003). legacy/ is
imported here as an oracle only; production code never imports it.
"""

import math
from fractions import Fraction

from engine.kp.chain import kp_chain
from engine.kp.intervals import all_boundaries

from legacy import kp as legacy_kp


def _tuples_match(longitude) -> bool:
    ours = kp_chain(longitude)
    theirs = legacy_kp.chain(longitude)
    return (
        ours.sign_lord,
        ours.nakshatra_lord,
        ours.sub_lord,
        ours.sub_sub_lord,
        ours.sign_number - 1,
        ours.nakshatra_number - 1,
    ) == (
        theirs["SL"],
        theirs["NL"],
        theirs["SB"],
        theirs["SS"],
        legacy_kp.SIGNS.index(theirs["sign"]),
        legacy_kp.NAKS.index(theirs["nakshatra"]),
    )


def test_dense_sweep_exact_equivalence_51429():
    step = 360.0 / 51429
    mismatches = [i for i in range(51429) if not _tuples_match(i * step)]
    assert mismatches == [], f"{len(mismatches)} mismatches, first at {mismatches[:3]}"


def test_every_boundary_at_above_below_exact():
    eps = Fraction(1, 10**9)
    for boundary in all_boundaries():
        assert _tuples_match(boundary), f"exact boundary {boundary}"
        assert _tuples_match(boundary + eps), f"above boundary {boundary}"
        if boundary > 0:
            assert _tuples_match(boundary - eps), f"below boundary {boundary}"


def test_every_boundary_float_ulp_neighbors():
    for boundary in all_boundaries():
        base = float(boundary)
        points = [base]
        down = base
        up = base
        for _ in range(3):
            down = math.nextafter(down, -math.inf)
            up = math.nextafter(up, math.inf)
            points.extend((down, up))
        for point in points:
            if 0.0 <= point < 360.0:
                assert _tuples_match(point), f"ULP neighbor {point!r} of {boundary}"


def test_adversarial_decimal_spellings():
    cases = [
        0.0, 359.9999999999999, 1e-13, 30.000000000000004,
        13.333333333333332, 13.333333333333334, 13.333333333333336,
        120.00000000000001, 359.99999999999994, 179.99999999999997,
        6.666666666666667, 46.66666666666667, 359.0000000001,
    ]
    for value in cases:
        assert _tuples_match(value), f"spelling {value!r}"
    # Negative and >360 normalization parity with the oracle.
    for value in (-0.1, -359.9999999, 360.0, 720.5, -720.5):
        assert _tuples_match(value), f"normalization {value!r}"


def test_nearest_boundary_arcsec_matches_oracle():
    step = 360.0 / 997
    for i in range(997):
        lon = i * step
        assert kp_chain(lon).nearest_boundary_arcsec == legacy_kp.chain(lon)[
            "nearest_boundary_arcsec"
        ]
