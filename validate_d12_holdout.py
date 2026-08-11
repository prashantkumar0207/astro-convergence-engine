"""Independent D12 Dwadasamsa holdout validator (ADR-0010).

Validates the production D12 classification against a reference built
INDEPENDENTLY inside this file: target sign computed by counting
onward from the source sign by name order (a lookup construction, not
the framework's modular arithmetic). Nothing is imported from
engine/astrology/varga_d12.

Run:  python validate_d12_holdout.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.astrology.varga_classifier import classify  # framework (SUBJECT)
from engine.astrology.varga_registry import get_varga_rule

import engine.astrology  # noqa: F401  (registers production vargas)

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independent reference: full 144-cell target table built by name
#: counting ("first part the sign itself, then the next sign in
#: order"), materialized once and used as a lookup.
REFERENCE_TABLE = {}
for _source_name in SIGNS:
    _start = SIGNS.index(_source_name)
    REFERENCE_TABLE[_source_name] = tuple(
        SIGNS[(_start + _k) % 12] for _k in range(12)
    )


def reference_d12(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    division = int((longitude - source * 30.0) // 2.5)
    if division > 11:
        division = 11
    return SIGNS.index(REFERENCE_TABLE[SIGNS[source]][division]), division


def main() -> int:
    rule = get_varga_rule(12, "parashara")
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        expected_sign, expected_division = reference_d12(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            failures.append(("dense", longitude))
        dense += 1

    boundary = 0
    for k in range(144):
        base = k * 2.5
        points = [base]
        up = base
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            result = classify(longitude, rule)
            expected_sign, expected_division = reference_d12(longitude)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                failures.append(("boundary", longitude))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT D12 DWADASAMSA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D12 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
