"""Independent D3 Drekkana holdout validator (Gate 5 of ADR-0009).

Validates the production D3 classification (generic framework +
registered Parashara rule) against a reference built INDEPENDENTLY
inside this file: a 36-cell lookup table typed by sign NAME from the
classical statement (first drekkana the sign itself, second the 5th,
third the 9th). Nothing is imported from engine/astrology/varga_d3.

Run:  python validate_d3_holdout.py
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

#: Independent reference table, typed from the classical rule by name.
REFERENCE = {
    "Aries": ("Aries", "Leo", "Sagittarius"),
    "Taurus": ("Taurus", "Virgo", "Capricorn"),
    "Gemini": ("Gemini", "Libra", "Aquarius"),
    "Cancer": ("Cancer", "Scorpio", "Pisces"),
    "Leo": ("Leo", "Sagittarius", "Aries"),
    "Virgo": ("Virgo", "Capricorn", "Taurus"),
    "Libra": ("Libra", "Aquarius", "Gemini"),
    "Scorpio": ("Scorpio", "Pisces", "Cancer"),
    "Sagittarius": ("Sagittarius", "Aries", "Leo"),
    "Capricorn": ("Capricorn", "Taurus", "Virgo"),
    "Aquarius": ("Aquarius", "Gemini", "Libra"),
    "Pisces": ("Pisces", "Cancer", "Scorpio"),
}


def reference_d3(longitude: float):
    longitude = longitude % 360.0
    source = int(longitude // 30.0)
    division = int((longitude - source * 30.0) // 10.0)
    if division > 2:
        division = 2
    return SIGNS.index(REFERENCE[SIGNS[source]][division]), division


def main() -> int:
    rule = get_varga_rule(3, "parashara")
    failures = []

    dense = 0
    step = 360.0 / 51429
    for i in range(51429):
        longitude = i * step
        result = classify(longitude, rule)
        expected_sign, expected_division = reference_d3(longitude)
        if (result.d_sign, result.division_index) != (expected_sign, expected_division):
            failures.append(("dense", longitude))
        dense += 1

    # Boundary battery: exact boundaries plus ULP neighbors ABOVE
    # (below-boundary dust follows the locked promote-up/sign-split
    # convention, covered by the repository tests; this validator's
    # naive reference carries no tolerance by construction).
    boundary = 0
    for k in range(36):
        base = k * 10.0
        points = [base]
        up = base
        for _ in range(3):
            up = math.nextafter(up, math.inf)
            points.append(up)
        for longitude in points:
            result = classify(longitude, rule)
            expected_sign, expected_division = reference_d3(longitude)
            if (result.d_sign, result.division_index) != (expected_sign, expected_division):
                failures.append(("boundary", longitude))
            boundary += 1

    print("=" * 60)
    print("INDEPENDENT D3 DREKKANA VALIDATION")
    print("=" * 60)
    print(f"Dense cases    : {dense}")
    print(f"Boundary cases : {boundary}")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:5]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT D3 CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
