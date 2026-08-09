"""Independent Parashari drishti validator (ADR-0012).

Validates production graha drishti against an in-file reference built
by NAME-COUNTING (walk the zodiac by sign name from the planet's sign
and pick the named ordinals), a different construction from the
production modular arithmetic. Nothing imported from engine/parashari.

Run:  python validate_parashari_drishti_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from engine.parashari.drishti import aspected_signs  # SUBJECT

SIGNS = ("Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
         "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces")

#: Independent reference: classical ordinals by graha name.
REFERENCE_ORDINALS = {
    "Sun": (7,), "Moon": (7,), "Mercury": (7,), "Venus": (7,),
    "Mars": (4, 7, 8), "Jupiter": (5, 7, 9), "Saturn": (3, 7, 10),
}


def reference_aspected(planet: str, sign_number: int):
    # Walk the zodiac by name, counting the planet's own sign as 1.
    walk = [SIGNS[(sign_number - 1 + step) % 12] for step in range(12)]
    return tuple(SIGNS.index(walk[ordinal - 1]) + 1
                 for ordinal in REFERENCE_ORDINALS[planet])


def main() -> int:
    failures = []
    checked = 0
    for planet in REFERENCE_ORDINALS:
        for sign in range(1, 13):
            if aspected_signs(planet, sign) != reference_aspected(planet, sign):
                failures.append((planet, sign))
            checked += 1

    print("=" * 60)
    print("INDEPENDENT PARASHARI DRISHTI VALIDATION")
    print("=" * 60)
    print(f"Planet-sign cases : {checked}")
    if failures:
        print(f"FAILURES: {failures}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT DRISHTI CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
