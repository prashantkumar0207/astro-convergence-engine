"""
KP transcribed-fixture regression (Gate 4 of ADR-0006).

The 50-item Brihat fixture set (brihat_fixtures.py, COMPARISON
FIXTURES transcribed from screenshots, not astronomical ground truth)
was certified in the legacy era as a pure-math structural check: run
the KP chain on the FIXTURE longitudes themselves and require every
SL/NL/SB/SS field to match the transcription exactly
(v1_1_engineering_decision.json: 200/200 exact fields). This test
pins that result onto engine/kp permanently.
"""

from fractions import Fraction

import brihat_fixtures

from engine.kp.chain import kp_chain

CASES = (brihat_fixtures.CASE_C, brihat_fixtures.CASE_D)


def _dms_to_exact(dms: str) -> Fraction:
    degrees, minutes, seconds = (int(part) for part in dms.split(":"))
    return Fraction(degrees) + Fraction(minutes, 60) + Fraction(seconds, 3600)


def _check(items):
    failures = []
    fields = 0
    for name, (dms, sl, nl, sb, ss) in items.items():
        chain = kp_chain(_dms_to_exact(dms))
        got = (chain.sign_lord, chain.nakshatra_lord, chain.sub_lord, chain.sub_sub_lord)
        expected = (sl, nl, sb, ss)
        fields += 4
        if got != expected:
            failures.append((name, dms, expected, got))
    return fields, failures


def test_structural_check_on_all_fixture_longitudes_200_fields():
    total_fields = 0
    all_failures = []
    for case in CASES:
        for items in (case["planets"], case["cusps"]):
            fields, failures = _check(items)
            total_fields += fields
            all_failures.extend((case["label"], *failure) for failure in failures)
    assert total_fields == 200
    assert all_failures == [], all_failures
