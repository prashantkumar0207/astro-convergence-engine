"""
Independent validator for engine.astrology.trikalam (ADR-0060, Gate E).

A second, independently-coded reference for `PYJHORA_TRIKALAM_V1`'s
arithmetic: the offset table below is retyped directly from ADR-0060's
transcription, never imported from `engine.astrology.trikalam._OFFSETS`,
so a corruption of the module's own table is not self-confirming. Reuses
(does not re-derive) the already Tier-0-certified `rise_set.sunrise`/
`sunset` and the already-certified `panchanga.vara`, matching
`validate_panchanga_holdout.py`'s own precedent of reusing certified
primitives rather than re-independently-certifying them a second time.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from engine.astrology.panchanga import VaraStatus, vara  # noqa: E402
from engine.astronomy.profile import CalculationProfile, DEFAULT_PROFILE  # noqa: E402
from engine.astronomy.rise_set import RiseSetStatus, sunrise, sunset  # noqa: E402

#: Independently retyped from ADR-0060's transcription of PyJHora 4.8.7's
#: `trikalam()`. Never import from `engine.astrology.trikalam`.
_INDEPENDENT_OFFSETS = {
    "rahu_kalam": (0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25),
    "gulika": (0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0),
    "yamaganda": (0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625),
}
_PERIOD_FRACTION = 0.125


@dataclass(frozen=True)
class ExactTrikalamResult:
    determinate: bool
    start_julian_day_ut: float | None
    end_julian_day_ut: float | None


def exact_trikalam(
    element: str,
    julian_day_ut: float,
    latitude: float,
    longitude: float,
    elevation_m: float = 0.0,
    profile: CalculationProfile = DEFAULT_PROFILE,
    strict: bool = True,
) -> ExactTrikalamResult:
    """Independently re-derives `PYJHORA_TRIKALAM_V1`'s window."""

    import math

    midnight = math.floor(julian_day_ut - 0.5) + 0.5
    today_sunrise = sunrise(midnight, latitude, longitude, elevation_m, profile, strict)
    today_sunset = sunset(midnight, latitude, longitude, elevation_m, profile, strict)
    weekday = vara(julian_day_ut, latitude, longitude, elevation_m, profile, strict)

    if (
        today_sunrise.status != RiseSetStatus.OK
        or today_sunset.status != RiseSetStatus.OK
        or weekday.status != VaraStatus.OK
    ):
        return ExactTrikalamResult(determinate=False, start_julian_day_ut=None, end_julian_day_ut=None)

    day_duration = today_sunset.julian_day_ut - today_sunrise.julian_day_ut
    offset = _INDEPENDENT_OFFSETS[element][weekday.index]
    start = today_sunrise.julian_day_ut + day_duration * offset
    end = start + _PERIOD_FRACTION * day_duration
    return ExactTrikalamResult(determinate=True, start_julian_day_ut=start, end_julian_day_ut=end)


#: Same real-world holdout `certify_rise_set.py`/`certify_panchanga.py`
#: already use, reused rather than reinvented.
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

_ELEMENTS = ("rahu_kalam", "yamaganda", "gulika")


def _run(fail_fast: bool = True) -> dict:
    import swisseph as swe

    from engine.astrology.trikalam import PYJHORA_TRIKALAM_V1, TrikalamElement, trikalam_period
    from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI

    mismatches = []
    comparisons = 0

    for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
        for holdout_id, (y, m, d), lat, lon in _HOLDOUT_DATES:
            jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
            for element_name in _ELEMENTS:
                element = TrikalamElement(element_name)
                engine_result = trikalam_period(element, jd, lat, lon, 0.0, profile, True, PYJHORA_TRIKALAM_V1)
                ref = exact_trikalam(element_name, jd, lat, lon, 0.0, profile, True)

                comparisons += 1
                if not ref.determinate:
                    mismatches.append(f"{profile.name}/{holdout_id}/{element_name}: expected determinate, reference says indeterminate")
                elif engine_result.status.value != "ok" or engine_result.start_julian_day_ut != ref.start_julian_day_ut or engine_result.end_julian_day_ut != ref.end_julian_day_ut:
                    mismatches.append(
                        f"{profile.name}/{holdout_id}/{element_name}: "
                        f"{engine_result.status.value}/{engine_result.start_julian_day_ut}/{engine_result.end_julian_day_ut} "
                        f"!= ok/{ref.start_julian_day_ut}/{ref.end_julian_day_ut}"
                    )

            if fail_fast and mismatches:
                break

    for holdout_id, (y, m, d), lat, lon in _CIRCUMPOLAR_HOLDOUT:
        jd = swe.julday(y, m, d, 12.0, swe.GREG_CAL)
        for element_name in _ELEMENTS:
            element = TrikalamElement(element_name)
            engine_result = trikalam_period(element, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
            ref = exact_trikalam(element_name, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True)
            comparisons += 1
            if ref.determinate != (engine_result.status.value == "ok"):
                mismatches.append(
                    f"{holdout_id}/{element_name}: circumpolar determinacy mismatch: "
                    f"engine ok={engine_result.status.value == 'ok'}, reference determinate={ref.determinate}"
                )

    return {
        "holdout_cases": len(_HOLDOUT_DATES) * 2 + len(_CIRCUMPOLAR_HOLDOUT),
        "comparisons": comparisons,
        "mismatches": mismatches,
    }


def main() -> int:
    result = _run()
    if result["mismatches"]:
        print("TRIKALAM HOLDOUT VALIDATION FAIL:")
        for m in result["mismatches"]:
            print(" -", m)
        return 3
    print(
        f"TRIKALAM HOLDOUT VALIDATION PASS: {result['holdout_cases']} cases, "
        f"{result['comparisons']} comparisons, 0 mismatches"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
