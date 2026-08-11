"""Independent D7 Saptamsa holdout validator (ADR-0011).

Validates the production D7 Saptamsa classification against a reference
built INDEPENDENTLY inside this file (by-name lookup construction).
Nothing is imported from engine/astrology/varga_d7.

Run:  python validate_d7_holdout.py
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

#: Independent reference: odd signs count the seven parts from the
#: sign itself, even signs from the seventh sign, forward; the
#: locked convention promotes values within 1e-10 below a boundary.
WIDTH = 30.0 / 7.0


def reference(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    division = int(((longitude - source * 30.0) + 1e-10) / WIDTH)
    if division > 6:
        division = 6
    start_name = SIGNS[source] if source % 2 == 0 else SIGNS[(source + 6) % 12]
    return (SIGNS.index(start_name) + division) % 12, division


def boundaries():
    return [s * 30.0 + d * WIDTH for s in range(12) for d in range(7)]


def main() -> int:
    rule = get_varga_rule(7, "parashara")
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        expected = reference(longitude)
        if (result.d_sign, result.division_index) != expected:
            failures.append(("dense", longitude))
        dense += 1

    boundary = 0
    for base in boundaries():
        points = [base]
        up = base
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            if longitude >= 360.0:
                continue
            result = classify(longitude, rule)
            expected = reference(longitude)
            if (result.d_sign, result.division_index) != expected:
                failures.append(("boundary", longitude))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT D7 VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D7 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
