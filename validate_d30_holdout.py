"""Independent D30 Trimsamsa holdout validator (ADR-VARGA-D30-001).

Validates the production D30 Trimsamsa classification against a reference
built INDEPENDENTLY inside this file (by-name lookup construction).
Nothing is imported from engine/astrology/varga_d30.

Run:  python validate_d30_holdout.py
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

#: Independent reference: the classical trimsamsa segment tables by
#: planet and sign name; even signs reverse the odd order.
ODD = ((5.0, "Aries"), (5.0, "Aquarius"), (8.0, "Sagittarius"),
       (7.0, "Gemini"), (5.0, "Libra"))
EVEN = ((5.0, "Taurus"), (7.0, "Virgo"), (8.0, "Pisces"),
        (5.0, "Capricorn"), (5.0, "Scorpio"))


def reference(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    within = longitude - source * 30.0
    table = ODD if source % 2 == 0 else EVEN
    cumulative = 0.0
    for division, (width, target_name) in enumerate(table):
        cumulative += width
        if within + 1e-10 < cumulative or division == 4:
            return SIGNS.index(target_name), division
    raise AssertionError


def boundaries():
    out = []
    for s in range(12):
        table = ODD if s % 2 == 0 else EVEN
        cumulative = 0.0
        for width, _ in table:
            out.append(s * 30.0 + cumulative)
            cumulative += width
    return out


def main() -> int:
    rule = get_varga_rule(30, "parashara")
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
    print("INDEPENDENT D30 VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D30 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
