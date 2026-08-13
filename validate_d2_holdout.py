"""Independent D2 Hora holdout validator (ADR-0011).

Validates the production D2 Hora classification against a reference
built INDEPENDENTLY inside this file (by-name lookup construction).
Nothing is imported from engine/astrology/varga_d2.

Run:  python validate_d2_holdout.py
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

#: Independent reference: odd signs Sun hora (Leo) then Moon hora
#: (Cancer); even signs reversed. Output space is two signs only.


def reference(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    half = 0 if (longitude - source * 30.0) + 1e-10 < 15.0 else 1
    if (longitude - source * 30.0) >= 29.9999999999:
        half = 1
    leo, cancer = SIGNS.index("Leo"), SIGNS.index("Cancer")
    if source % 2 == 0:
        return (leo, 0) if half == 0 else (cancer, 1)
    return (cancer, 0) if half == 0 else (leo, 1)


def boundaries():
    return [s * 30.0 + h * 15.0 for s in range(12) for h in range(2)]


def main() -> int:
    rule = get_varga_rule(2, "parashara")
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
    print("INDEPENDENT D2 VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D2 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
