"""Independent D45 Akshavedamsa holdout validator (ADR-0077).

Validates the frozen D45 rule (imported from scripts/certify_d45.py, which owns the
one frozen definition under certification - this rule is NOT registered in
engine.astrology.varga_registry and engine/astrology/varga_d45.py does not exist)
against a reference built INDEPENDENTLY inside this file: a per-sign lookup table
constructed by direct sign-name enumeration (movable/fixed/dual triads), not the
framework's own modular-arithmetic offsets.

Run:  python validate_d45_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent / "scripts"))

from engine.astrology.varga_classifier import classify  # framework (SUBJECT)

from certify_d45 import D45_PARASHARA  # the one frozen rule under certification

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independent reference, built by direct enumeration (not offset arithmetic):
#: for a movable-sign source, the 45-part sequence starts at Aries and repeats
#: the twelve signs in zodiacal order; fixed starts at Leo; dual starts at
#: Sagittarius. Materialized as an explicit 45-entry table per source sign.
_MOVABLE_START, _FIXED_START, _DUAL_START = "Aries", "Leo", "Sagittarius"
_MOVABLE, _FIXED, _DUAL = (
    {"Aries", "Cancer", "Libra", "Capricorn"},
    {"Taurus", "Leo", "Scorpio", "Aquarius"},
    {"Gemini", "Virgo", "Sagittarius", "Pisces"},
)

REFERENCE_TABLE = {}
for _source_name in SIGNS:
    if _source_name in _MOVABLE:
        _start = SIGNS.index(_MOVABLE_START)
    elif _source_name in _FIXED:
        _start = SIGNS.index(_FIXED_START)
    else:
        _start = SIGNS.index(_DUAL_START)
    REFERENCE_TABLE[_source_name] = tuple(
        SIGNS[(_start + _k) % 12] for _k in range(45)
    )


#: Independently re-derived from the engine's own documented, already-locked
#: boundary rule (engine/astrology/longitude_utils.py's own docstring: "a degree
#: within BOUNDARY_TOLERANCE below a division's edge promotes to the next
#: division"), not imported from that module - this validator applies the SAME
#: documented convention on its own terms, so it checks whether classify()
#: correctly IMPLEMENTS the documented rule, not whether it matches a naive,
#: unpromoted floor (which would spuriously "fail" at every one of D45's own
#: non-exact 2/3-degree boundaries, per ADR-0077 section 3).
_BOUNDARY_TOLERANCE = 1e-10


def reference_d45(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    degree = longitude - source * 30.0
    width = 30.0 / 45.0
    division = int((degree + _BOUNDARY_TOLERANCE) / width)
    if division > 44:
        division = 44
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


def main() -> int:
    rule = D45_PARASHARA
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        expected_sign, expected_division = reference_d45(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            failures.append(("dense", longitude))
        dense += 1

    boundary = 0
    for k in range(540):  # 45 divisions x 12 signs
        base = k * (30.0 / 45.0)
        points = [base]
        up = base
        import math
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            result = classify(longitude, rule)
            expected_sign, expected_division = reference_d45(longitude)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                failures.append(("boundary", longitude))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT D45 AKSHAVEDAMSA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D45 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
