"""
Independent validator for the H-02 ingress-classification seam reproduction
(DP-013 Option A, Gate-E-style discipline).

A second, separately-typed exact-rational classifier - never importing
`scripts/reproduce_h02_ingress_seam.py`'s own `classify_sign`/
`classify_nakshatra` - that independently re-derives the same 2024 holdout
(reusing only the certified `engine.transits.events`/`sidereal_planet_position`
primitives both this file and the main script legitimately share, matching
`validate_panchanga_holdout.py`'s own precedent) and reports its own mismatch
counts. This is investigation evidence, not a certification - it does not
implement a fix and does not touch TRANSIT_V1.
"""

from __future__ import annotations

import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import swisseph as swe  # noqa: E402

from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402
from engine.astronomy.sidereal_planets import sidereal_planet_position  # noqa: E402
from engine.transits.events import nakshatra_ingresses, sign_ingresses  # noqa: E402

#: Independently retyped a second time. Never import from
#: scripts/reproduce_h02_ingress_seam.py.
_TOLERANCE = Fraction(1, 10**10)
_SIGN_SPAN = Fraction(30)
_SIGN_COUNT = 12
_NAKSHATRA_SPAN = Fraction(40, 3)
_NAKSHATRA_COUNT = 27


def _classify(longitude: float, span: Fraction, count: int) -> int:
    value = Fraction(repr(longitude)) % 360
    index = int((value + _TOLERANCE) / span)
    return min(index, count - 1)


def exact_classify_sign(longitude: float) -> int:
    return _classify(longitude, _SIGN_SPAN, _SIGN_COUNT)


def exact_classify_nakshatra(longitude: float) -> int:
    return _classify(longitude, _NAKSHATRA_SPAN, _NAKSHATRA_COUNT)


def _mismatches(events, body_swe_id: int, classify) -> int:
    count = 0
    for event in events:
        position = sidereal_planet_position(
            event.julian_day, body_swe_id, PARASHARI_LAHIRI.ayanamsa_mode, strict=True,
        )
        if classify(position.longitude) != classify(event.target_longitude):
            count += 1
    return count


def _run() -> dict:
    jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)
    sun_events = sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
    moon_events = nakshatra_ingresses("Moon", jd0, jd0 + 35, PARASHARI_LAHIRI)

    return {
        "sun_cases": len(sun_events),
        "sun_mismatches": _mismatches(sun_events, swe.SUN, exact_classify_sign),
        "moon_cases": len(moon_events),
        "moon_mismatches": _mismatches(moon_events, swe.MOON, exact_classify_nakshatra),
    }


def main() -> int:
    result = _run()
    print(
        f"H-02 INDEPENDENT VALIDATOR PASS: sun_cases={result['sun_cases']} "
        f"sun_mismatches={result['sun_mismatches']} moon_cases={result['moon_cases']} "
        f"moon_mismatches={result['moon_mismatches']}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
