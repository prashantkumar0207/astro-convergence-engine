"""
Independent validator for panchanga classification (ADR-0055, Gate E).

A THIRD, differently-coded reference for the arithmetic
`engine.astrology.panchanga` performs, mirroring the discipline already
established by `validate_rise_set_holdout.py` (never import the module
under test's own classification logic):

  - Tithi/Yoga/Karana: exact rational (`fractions.Fraction`) boundary
    classification, independently re-derived here rather than calling
    `engine.astrology.longitude_utils.division_index`. Same style as
    `scripts/certify_current_engine.py`'s `exact_nakshatra_reference`
    (already an established, certified pattern for this repository),
    applied to elongation/sum instead of raw longitude.
  - Vara: an independently-coded classical Julian-Day-to-Gregorian-date
    algorithm (Fliegel & Van Flandern, 1968, "A Machine Algorithm for
    Processing Calendar Dates", Communications of the ACM 11(10):657),
    never calling `swisseph.revjul`. The already-certified Tier-0
    `engine.astronomy.rise_set.sunrise` IS reused here (not
    re-independently-derived a second time - `validate_rise_set_holdout.py`
    already independently certifies it); this validator checks only the
    NEW logic `engine.astrology.panchanga.vara` adds on top: which civil
    day anchors the sunrise-to-sunrise interval, and that day's weekday.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine.astronomy.profile import CalculationProfile, DEFAULT_PROFILE  # noqa: E402
from engine.astronomy.rise_set import RiseSetStatus, sunrise  # noqa: E402

_TOLERANCE = Fraction(1, 10**10)


def _exact_index(value: Fraction, span: Fraction, count: int) -> int:
    value = value % 360
    idx = int((value + _TOLERANCE) / span)
    if idx >= count:
        idx = count - 1
    return idx + 1


def exact_tithi(sun_longitude: float, moon_longitude: float) -> int:
    elongation = (Fraction(repr(moon_longitude)) - Fraction(repr(sun_longitude))) % 360
    return _exact_index(elongation, Fraction(12), 30)


def exact_yoga(sun_longitude: float, moon_longitude: float) -> int:
    total = (Fraction(repr(sun_longitude)) + Fraction(repr(moon_longitude))) % 360
    return _exact_index(total, Fraction(360, 27), 27)


def exact_karana(sun_longitude: float, moon_longitude: float) -> int:
    elongation = (Fraction(repr(moon_longitude)) - Fraction(repr(sun_longitude))) % 360
    return _exact_index(elongation, Fraction(6), 60)


def jdn_to_gregorian(jdn: int) -> tuple[int, int, int]:
    """
    Fliegel & Van Flandern (1968). `jdn` is the integer Julian Day
    Number (noon-referenced). Independently coded from the published
    algorithm, never calling `swisseph.revjul`.
    """

    l = jdn + 68569
    n = (4 * l) // 146097
    l = l - (146097 * n + 3) // 4
    i = (4000 * (l + 1)) // 1461001
    l = l - (1461 * i) // 4 + 31
    j = (80 * l) // 2447
    day = l - (2447 * j) // 80
    l = j // 11
    month = j + 2 - 12 * l
    year = 100 * (n - 49) + i + l
    return year, month, day


def exact_weekday_index(jdn: int) -> int:
    """0 (Sunday) .. 6 (Saturday), from an independently-coded
    calendar-date derivation plus Python's standard-library
    `datetime.date.weekday()` (itself an independent implementation of
    the Gregorian calendar, not part of this repository's own code)."""

    from datetime import date

    year, month, day = jdn_to_gregorian(jdn)
    python_weekday = date(year, month, day).weekday()  # Monday=0..Sunday=6
    return (python_weekday + 1) % 7


@dataclass(frozen=True)
class ExactVaraResult:
    determinate: bool
    index: int | None


def exact_vara(
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> ExactVaraResult:
    """
    Independently re-derives the day-selection and weekday-labelling
    logic `engine.astrology.panchanga.vara` adds. Reuses (does not
    re-derive) the already Tier-0-certified `rise_set.sunrise` itself -
    `validate_rise_set_holdout.py` is where that gets independently
    checked.
    """

    import math

    midnight = math.floor(julian_day_ut - 0.5) + 0.5
    today_sunrise = sunrise(midnight, latitude, longitude, elevation_m, profile, strict)

    if today_sunrise.status != RiseSetStatus.OK:
        return ExactVaraResult(determinate=False, index=None)

    anchor_midnight = midnight if julian_day_ut >= today_sunrise.julian_day_ut else midnight - 1.0
    jdn = int(anchor_midnight + 0.5)
    return ExactVaraResult(determinate=True, index=exact_weekday_index(jdn))


#: Same real-world holdout `scripts/certify_rise_set.py` already uses,
#: reused rather than reinvented. Times are set to local mid-morning
#: (a fixed UT hour) so tithi/yoga/karana are evaluated at a real
#: instant, not merely a bare civil date.
_HOLDOUT_DATES = [
    ("H1_london_1823", (1823, 4, 17), 51.5074, -0.1278),
    ("H2_newyork_1900", (1900, 1, 1), 40.7128, -74.0060),
    ("H3_sydney_1946", (1946, 6, 14), -33.8688, 151.2093),
    ("H4_delhi_1979", (1979, 11, 11), 28.6667, 77.2167),
    ("H5_reykjavik_1992", (1992, 2, 29), 64.1466, -21.9426),
    ("H6_quito_2010", (2010, 7, 21), -0.1807, -78.4678),
    ("H7_tokyo_2033", (2033, 9, 3), 35.6762, 139.6503),
    ("H8_mumbai_2077", (2077, 12, 3), 19.0760, 72.8777),
    ("H9_paris_2350", (2350, 1, 15), 48.8566, 2.3522),
    ("H10_boundary_moon_a", (2025, 3, 1), 28.6667, 77.2167),
    ("H11_boundary_moon_b", (2025, 3, 2), 28.6667, 77.2167),
]

_CIRCUMPOLAR_HOLDOUT = [
    ("P1_svalbard_midnight_sun", (2024, 6, 21), 78.2232, 15.6267),
    ("P2_svalbard_polar_night", (2024, 12, 21), 78.2232, 15.6267),
]


def _run(fail_fast: bool = True) -> dict:
    import swisseph as swe

    from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI
    from engine.astronomy.sidereal_planets import sidereal_planet_position
    from engine.astrology.panchanga import (
        karana_index,
        panchanga,
        tithi_index,
        yoga_index,
    )

    mismatches = []
    comparisons = 0

    for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
        for holdout_id, (y, m, d), lat, lon in _HOLDOUT_DATES:
            jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
            sun = sidereal_planet_position(jd, swe.SUN, profile.ayanamsa_mode, True)
            moon = sidereal_planet_position(jd, swe.MOON, profile.ayanamsa_mode, True)

            engine_tithi = tithi_index(sun.longitude, moon.longitude)
            engine_yoga = yoga_index(sun.longitude, moon.longitude)
            engine_karana = karana_index(sun.longitude, moon.longitude)
            ref_tithi = exact_tithi(sun.longitude, moon.longitude)
            ref_yoga = exact_yoga(sun.longitude, moon.longitude)
            ref_karana = exact_karana(sun.longitude, moon.longitude)

            comparisons += 3
            if engine_tithi != ref_tithi:
                mismatches.append(f"{profile.name}/{holdout_id}: tithi {engine_tithi} != {ref_tithi}")
            if engine_yoga != ref_yoga:
                mismatches.append(f"{profile.name}/{holdout_id}: yoga {engine_yoga} != {ref_yoga}")
            if engine_karana != ref_karana:
                mismatches.append(f"{profile.name}/{holdout_id}: karana {engine_karana} != {ref_karana}")

            p = panchanga(jd, lat, lon, 0.0, profile, True)
            comparisons += 1
            ev = exact_vara(jd, lat, lon, 0.0, profile, True)
            if not ev.determinate:
                mismatches.append(f"{profile.name}/{holdout_id}: vara expected determinate, reference says indeterminate")
            elif p.vara.status.value != "ok" or p.vara.index != ev.index:
                mismatches.append(
                    f"{profile.name}/{holdout_id}: vara {p.vara.status.value}/{p.vara.index} != ok/{ev.index}"
                )

            if fail_fast and mismatches:
                break

    for holdout_id, (y, m, d), lat, lon in _CIRCUMPOLAR_HOLDOUT:
        jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
        p = panchanga(jd, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        comparisons += 1
        ev = exact_vara(jd, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        if ev.determinate != (p.vara.status.value == "ok"):
            mismatches.append(f"{holdout_id}: circumpolar determinacy mismatch: engine ok={p.vara.status.value == 'ok'}, reference determinate={ev.determinate}")

    return {
        "holdout_cases": len(_HOLDOUT_DATES) * 2 + len(_CIRCUMPOLAR_HOLDOUT),
        "comparisons": comparisons,
        "mismatches": mismatches,
    }


def main() -> int:
    result = _run()
    if result["mismatches"]:
        print("PANCHANGA HOLDOUT VALIDATION FAIL:")
        for m in result["mismatches"]:
            print(" -", m)
        return 3
    print(
        f"PANCHANGA HOLDOUT VALIDATION PASS: {result['holdout_cases']} cases, "
        f"{result['comparisons']} comparisons, 0 mismatches"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
