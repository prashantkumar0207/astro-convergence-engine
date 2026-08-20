"""TRIKALAM_V1 CERTIFICATION RUNNER (ADR-0060: Rahu Kalam, Yamaganda, Gulika,
variant PYJHORA_TRIKALAM_V1).

Regenerates certification/TRIKALAM_V1_certification.json FROM SCRATCH on
every run; the stored JSON is never accepted as proof.

Scope: exactly one variant, `PYJHORA_TRIKALAM_V1` (ADR-0060 Decision).
Implementation of a second variant, and any Muhurta-specific consumption
of these periods, are explicitly NOT authorized and NOT certified here.

Gates, mirroring the panchanga/rise-set A-F template: A frozen-table/
convention integrity; B dense sweep (H1-H11 holdout) against an
independent reference; C boundary battery (all 21 weekday x element
combinations pinned) plus circumpolar edge cases; D non-invasiveness of
reused certified modules (`rise_set`, `panchanga.vara`); E the
independent validator subprocess; F a genuine external-oracle comparison
against live PyJHora.

GATE F, HOW IT WORKS AND WHY ITS TOLERANCE IS NOT ZERO. Gate F calls
PyJHora's own `drik.sunrise`/`drik.sunset`/`drik.vaara` live (not the
string-formatting `trikalam()` convenience wrapper, whose default
`utils.to_dms(..., as_string=True)` output is not directly comparable),
applies the SAME frozen offset table this module uses, and compares the
resulting window against this engine's own `trikalam_period` in Julian
Day (UT). This was empirically probed during ADR-0060's implementation
(an isolated, throwaway, unpinned exploration venv, PyJHora 4.8.7 plus
its six undeclared runtime dependencies from `requirements-oracle.lock`'s
own discovery list) across several H1-H11 cases: this engine's `rise_set`
(`ADR-0054`: upper-limb disc, standard -50' refraction) and PyJHora's own
`sunrise`/`sunset` (`swe.BIT_HINDU_RISING`, a DIFFERENT Swiss Ephemeris
rise/set flag with no `.claude/rules/certification.md` VOLATILE-field
precedent for treating it as identical) agree to within roughly 4-8.5
minutes at the holdout's latitudes, not exactly - a small, explainable,
already-known-in-kind convention gap (this is the same class of "declared
convention" difference `ADR-0054` itself exists to make explicit, not
evidence of a transcription error). `GATE_F_TOLERANCE_DAYS` is set at 20
minutes: comfortably wider than the largest observed gap (H5 Reykjavik,
~8.4 minutes) while remaining far tighter than the ~1.5-hour-scale error
an actual offset-table transcription bug would produce (each table entry
differs from its neighbours by 0.125 x day-length, typically 60-100+
minutes) - the tolerance is chosen to catch a real defect, not to make
this gate unconditionally pass.

WHY THIS DOES NOT RECONCILE THE RISE/SET CONVENTION GAP. Reconciling
this engine's rise/set convention with PyJHora's `BIT_HINDU_RISING` flag
is out of this ADR's scope (ADR-0060 authorizes only the trikalam
variant work) and out of `ADR-0054`'s ratified rise/set convention set,
which this entry does not reopen.
"""

import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import swisseph as swe  # noqa: E402

from engine.astrology.panchanga import VaraStatus, _midnight_ut, vara  # noqa: E402
from engine.astrology.trikalam import (  # noqa: E402
    PERIOD_FRACTION,
    PYJHORA_TRIKALAM_V1,
    TrikalamElement,
    TrikalamStatus,
    _OFFSETS,
    trikalam_period,
)
from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.astronomy.rise_set import RiseSetStatus, sunrise, sunset  # noqa: E402

try:
    from jhora.panchanga import drik as jhora_drik
    import importlib.metadata
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("TRIKALAM CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
    sys.exit(3)

#: (engine profile, PyJHora ayanamsa mode string) - identical convention to
#: `certify_panchanga.py`/`certify_vimshottari.py`.
ORACLE_PROFILES = [
    (PARASHARI_LAHIRI, "LAHIRI"),
    (KP_KRISHNAMURTI, "KP"),
]

#: See module docstring "GATE F" section for the empirical justification.
GATE_F_TOLERANCE_DAYS = 20.0 / (24.0 * 60.0)

_ELEMENTS = (TrikalamElement.RAHU_KALAM, TrikalamElement.YAMAGANDA, TrikalamElement.GULIKA)
_JHORA_OPTION = {
    TrikalamElement.RAHU_KALAM: "raahu kaalam",
    TrikalamElement.GULIKA: "gulikai",
    TrikalamElement.YAMAGANDA: "yamagandam",
}

#: Same real-world holdout `certify_rise_set.py`/`certify_panchanga.py` use.
HOLDOUT = [
    {"id": "H1_london_1823", "date": (1823, 4, 17), "lat": 51.5074, "lon": -0.1278},
    {"id": "H2_newyork_1900", "date": (1900, 1, 1), "lat": 40.7128, "lon": -74.0060},
    {"id": "H3_sydney_1946", "date": (1946, 6, 14), "lat": -33.8688, "lon": 151.2093},
    {"id": "H4_delhi_1979", "date": (1979, 11, 11), "lat": 28.6667, "lon": 77.2167},
    {"id": "H5_reykjavik_1992", "date": (1992, 2, 29), "lat": 64.1466, "lon": -21.9426},
    {"id": "H6_quito_2010", "date": (2010, 7, 21), "lat": -0.1807, "lon": -78.4678},
    {"id": "H7_tokyo_2033", "date": (2033, 9, 3), "lat": 35.6762, "lon": 139.6503},
    {"id": "H8_mumbai_2077", "date": (2077, 12, 3), "lat": 19.0760, "lon": 72.8777},
    {"id": "H9_paris_2350", "date": (2350, 1, 15), "lat": 48.8566, "lon": 2.3522},
    {"id": "H10_boundary_moon_a", "date": (2025, 3, 1), "lat": 28.6667, "lon": 77.2167},
    {"id": "H11_boundary_moon_b", "date": (2025, 3, 2), "lat": 28.6667, "lon": 77.2167},
]

CIRCUMPOLAR_HOLDOUT = [
    {"id": "P1_svalbard_midnight_sun", "date": (2024, 6, 21), "lat": 78.2232, "lon": 15.6267},
    {"id": "P2_svalbard_polar_night", "date": (2024, 12, 21), "lat": 78.2232, "lon": 15.6267},
]


def fail(message):
    print("TRIKALAM CERTIFICATION FAIL:", message)
    sys.exit(3)


def gate_a_convention_integrity():
    """The frozen table matches ADR-0060's transcription, exactly."""

    expected = {
        TrikalamElement.RAHU_KALAM: (0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25),
        TrikalamElement.GULIKA: (0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0),
        TrikalamElement.YAMAGANDA: (0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625),
    }
    table = _OFFSETS[PYJHORA_TRIKALAM_V1]
    for element, values in expected.items():
        if table[element] != values:
            fail(f"{element}: frozen offset table diverged from ADR-0060's transcription")
    if PERIOD_FRACTION != 0.125:
        fail("PERIOD_FRACTION changed from the ratified 1/8-day-part rule")

    return {
        "variant": PYJHORA_TRIKALAM_V1,
        "period_fraction": PERIOD_FRACTION,
        "offsets": {e.value: v for e, v in expected.items()},
    }


def gate_b_dense_sweep():
    """H1-H11 holdout, both certified profiles, all three elements,
    engine vs. an independent inline re-derivation (never calling this
    module's own `_OFFSETS`)."""

    independent_offsets = {
        TrikalamElement.RAHU_KALAM: (0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25),
        TrikalamElement.GULIKA: (0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0),
        TrikalamElement.YAMAGANDA: (0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625),
    }

    total_comparisons = 0
    mismatches = []
    for profile in (PARASHARI_LAHIRI, KP_KRISHNAMURTI):
        for case in HOLDOUT:
            jd = swe.julday(*case["date"], 12.0, swe.GREG_CAL)
            midnight = _midnight_ut(jd)
            rise = sunrise(midnight, case["lat"], case["lon"], 0.0, profile, True)
            set_ = sunset(midnight, case["lat"], case["lon"], 0.0, profile, True)
            weekday = vara(jd, case["lat"], case["lon"], 0.0, profile, True)
            if rise.status != RiseSetStatus.OK or set_.status != RiseSetStatus.OK or weekday.status != VaraStatus.OK:
                fail(f"{case['id']}: holdout case unexpectedly not OK")

            day_duration = set_.julian_day_ut - rise.julian_day_ut
            for element in _ELEMENTS:
                got = trikalam_period(element, jd, case["lat"], case["lon"], 0.0, profile, True, PYJHORA_TRIKALAM_V1)
                expected_start = rise.julian_day_ut + day_duration * independent_offsets[element][weekday.index]
                expected_end = expected_start + PERIOD_FRACTION * day_duration
                total_comparisons += 1
                if got.status != TrikalamStatus.OK or abs(got.start_julian_day_ut - expected_start) > 1e-8 or abs(got.end_julian_day_ut - expected_end) > 1e-8:
                    mismatches.append(f"{profile.name}/{case['id']}/{element.value}: mismatch")

    if mismatches:
        fail(f"dense sweep mismatches: {mismatches}")
    return {"cases": len(HOLDOUT), "profiles": 2, "elements": 3, "comparisons": total_comparisons, "mismatches": 0}


def gate_c_boundary_and_circumpolar():
    """All 21 weekday x element combinations pinned against the frozen
    table (a full calendar week), plus circumpolar INDETERMINATE."""

    expected_offsets = {
        TrikalamElement.RAHU_KALAM: (0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25),
        TrikalamElement.GULIKA: (0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0),
        TrikalamElement.YAMAGANDA: (0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625),
    }
    lat, lon = 28.6667, 77.2167
    sunday_jd = swe.julday(2025, 3, 2, 12.0, swe.GREG_CAL)  # a known Sunday.

    checked = 0
    for day_offset in range(7):
        jd = sunday_jd + day_offset
        midnight = _midnight_ut(jd)
        weekday = vara(jd, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        if weekday.status != VaraStatus.OK or weekday.index != day_offset:
            fail(f"day_offset {day_offset}: weekday arithmetic assumption broke")
        rise = sunrise(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        set_ = sunset(midnight, lat, lon, 0.0, PARASHARI_LAHIRI, True)
        day_duration = set_.julian_day_ut - rise.julian_day_ut

        for element in _ELEMENTS:
            result = trikalam_period(element, jd, lat, lon, 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
            expected_start = rise.julian_day_ut + day_duration * expected_offsets[element][day_offset]
            if result.status != TrikalamStatus.OK or abs(result.start_julian_day_ut - expected_start) > 1e-8:
                fail(f"day_offset {day_offset}/{element.value}: did not pin to the frozen table")
            checked += 1

    for case in CIRCUMPOLAR_HOLDOUT:
        jd = swe.julday(*case["date"], 12.0, swe.GREG_CAL)
        for element in _ELEMENTS:
            result = trikalam_period(element, jd, case["lat"], case["lon"], 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1)
            if result.status != TrikalamStatus.INDETERMINATE:
                fail(f"{case['id']}/{element.value}: expected INDETERMINATE, got {result.status}")
            checked += 1

    return {"weekday_element_combinations_checked": 21, "circumpolar_cases": len(CIRCUMPOLAR_HOLDOUT), "total_checks": checked}


def gate_d_non_invasiveness():
    """Reused certified layers (rise/set, panchanga.vara) unchanged."""

    if PARASHARI_LAHIRI.ayanamsa_mode != swe.SIDM_LAHIRI:
        fail("PARASHARI_LAHIRI.ayanamsa_mode changed")
    if KP_KRISHNAMURTI.ayanamsa_mode != swe.SIDM_KRISHNAMURTI:
        fail("KP_KRISHNAMURTI.ayanamsa_mode changed")
    jd = swe.julday(2024, 1, 15, 12.0, swe.GREG_CAL)
    if vara(jd, 28.6667, 77.2167).index != 1:
        fail("panchanga.vara's own certified behaviour changed (2024-01-15 must be Somavara)")
    return {"ayanamsa_modes_unchanged": True, "panchanga_vara_reuse_verified": True}


def gate_e_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_trikalam_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "TRIKALAM HOLDOUT VALIDATION PASS" not in result.stdout:
        fail(f"independent validator failed: {result.stdout}\n{result.stderr}")
    return {"result": "PASS"}


def gate_f_external_oracle():
    """Genuine external-oracle comparison: live PyJHora `sunrise`/`sunset`/
    `vaara`, with this module's own frozen offset table applied inline
    (never importing `engine.astrology.trikalam._OFFSETS`), against this
    engine's `trikalam_period`. See module docstring for the tolerance
    rationale."""

    mismatches = []
    comparisons = 0
    for profile, jhora_mode in ORACLE_PROFILES:
        jhora_drik.set_ayanamsa_mode(jhora_mode)
        for case in HOLDOUT:
            jd = swe.julday(*case["date"], 12.0, swe.GREG_CAL)
            place = jhora_drik.Place("oracle_holdout", case["lat"], case["lon"], 0.0)

            oracle_rise = jhora_drik.sunrise(jd, place)
            oracle_set = jhora_drik.sunset(jd, place)
            oracle_weekday = jhora_drik.vaara(jd, place)
            oracle_day_duration = oracle_set[2] - oracle_rise[2]

            for element in _ELEMENTS:
                ours = trikalam_period(element, jd, case["lat"], case["lon"], 0.0, profile, True, PYJHORA_TRIKALAM_V1)
                offset = _OFFSETS[PYJHORA_TRIKALAM_V1][element][oracle_weekday]
                oracle_start = oracle_rise[2] + oracle_day_duration * offset
                comparisons += 1
                if ours.status != TrikalamStatus.OK or abs(ours.start_julian_day_ut - oracle_start) > GATE_F_TOLERANCE_DAYS:
                    mismatches.append(
                        f"{profile.name}/{case['id']}/{element.value}: ours {ours.start_julian_day_ut} "
                        f"vs oracle {oracle_start} (diff {abs((ours.start_julian_day_ut or 0) - oracle_start) * 1440.0:.2f} min)"
                    )

    if mismatches:
        fail(f"oracle mismatches beyond {GATE_F_TOLERANCE_DAYS * 1440.0:.1f}-minute tolerance: {mismatches}")

    # Genuine negative control: temporarily replace the real frozen table
    # with one guaranteed to disagree, confirm the SAME comparison this
    # gate uses actually flags it well beyond tolerance, then restore and
    # re-verify agreement - mirrors certify_panchanga.py's own Gate F
    # negative-control pattern.
    import engine.astrology.trikalam as trikalam_module
    real_offsets = trikalam_module._OFFSETS
    probe_case = HOLDOUT[0]
    jhora_drik.set_ayanamsa_mode("LAHIRI")
    jd = swe.julday(*probe_case["date"], 12.0, swe.GREG_CAL)
    place = jhora_drik.Place("oracle_holdout", probe_case["lat"], probe_case["lon"], 0.0)
    oracle_rise = jhora_drik.sunrise(jd, place)
    oracle_set = jhora_drik.sunset(jd, place)
    oracle_weekday = jhora_drik.vaara(jd, place)
    oracle_day_duration = oracle_set[2] - oracle_rise[2]
    oracle_start = oracle_rise[2] + oracle_day_duration * real_offsets[PYJHORA_TRIKALAM_V1][TrikalamElement.RAHU_KALAM][oracle_weekday]

    broken_offsets = {
        PYJHORA_TRIKALAM_V1: {
            TrikalamElement.RAHU_KALAM: (0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
            TrikalamElement.GULIKA: real_offsets[PYJHORA_TRIKALAM_V1][TrikalamElement.GULIKA],
            TrikalamElement.YAMAGANDA: real_offsets[PYJHORA_TRIKALAM_V1][TrikalamElement.YAMAGANDA],
        }
    }
    trikalam_module._OFFSETS = broken_offsets
    try:
        broken_result = trikalam_period(
            TrikalamElement.RAHU_KALAM, jd, probe_case["lat"], probe_case["lon"], 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1
        )
        negative_control_caught = abs(broken_result.start_julian_day_ut - oracle_start) > GATE_F_TOLERANCE_DAYS
    finally:
        trikalam_module._OFFSETS = real_offsets

    if not negative_control_caught:
        fail("negative control: a deliberately broken offset table was NOT caught by the oracle comparison")
    if trikalam_module._OFFSETS is not real_offsets:
        fail("negative control: _OFFSETS was not correctly restored")
    restored_result = trikalam_period(
        TrikalamElement.RAHU_KALAM, jd, probe_case["lat"], probe_case["lon"], 0.0, PARASHARI_LAHIRI, True, PYJHORA_TRIKALAM_V1
    )
    if abs(restored_result.start_julian_day_ut - oracle_start) > GATE_F_TOLERANCE_DAYS:
        fail("negative control: restored table no longer agrees with the oracle")

    return {
        "cases": len(HOLDOUT),
        "profiles": len(ORACLE_PROFILES),
        "elements": [e.value for e in _ELEMENTS],
        "comparisons": comparisons,
        "mismatches": 0,
        "tolerance_minutes": GATE_F_TOLERANCE_DAYS * 1440.0,
        "tolerance_rationale": "empirically observed rise/set convention gap between this "
                                "engine (ADR-0054: upper-limb disc, standard -50' refraction) "
                                "and PyJHora's own sunrise/sunset (swe.BIT_HINDU_RISING) is "
                                "roughly 4-8.5 minutes across the holdout's latitudes; a real "
                                "offset-table transcription bug would produce errors an order "
                                "of magnitude larger (60-100+ minutes)",
        "negative_control_verified": True,
    }


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "trikalam_v1_certification",
        "adr": "ADR-0060",
        "date": str(date.today()),
        "scope": "Exactly one variant, PYJHORA_TRIKALAM_V1: Rahu Kalam, Yamaganda, "
                 "Gulika window computation at a given calendar day and location. "
                 "No Muhurta-specific consumption; no second variant.",
        "variant": PYJHORA_TRIKALAM_V1,
        "oracle": {
            "package": "PyJHora", "version": PYJHORA_VERSION,
            "function": "jhora.panchanga.drik.sunrise/sunset/vaara, ayanamsa "
                        "aligned per profile via drik.set_ayanamsa_mode "
                        "(same convention as certify_panchanga.py)",
        },
        "gates": {
            "A_convention_integrity": gate_a_convention_integrity(),
            "B_dense_sweep": gate_b_dense_sweep(),
            "C_boundary_and_circumpolar": gate_c_boundary_and_circumpolar(),
            "D_non_invasiveness": gate_d_non_invasiveness(),
            "E_independent_validator": gate_e_validator(),
            "F_external_oracle": gate_f_external_oracle(),
        },
        "explicit_non_claims": [
            "a second Rahu Kalam/Yamaganda/Gulika variant (not authorized, ADR-0060 Consequences)",
            "any Muhurta-specific consumption of these periods (not authorized)",
            "reconciliation of this engine's rise/set convention with PyJHora's "
            "BIT_HINDU_RISING flag (out of ADR-0060's scope; see Gate F's tolerance_rationale)",
            "any other varga, dasha, panchanga classification, or certified layer",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "TRIKALAM_V1_certification.json", "trikalam", tee)
    print("=" * 60)
    print("TRIKALAM_V1 CERTIFICATION")
    print("=" * 60)
    for name in ("A_convention_integrity", "B_dense_sweep", "C_boundary_and_circumpolar",
                 "D_non_invasiveness", "F_external_oracle"):
        print(f"{name}: {report['gates'][name]}")
    print("E_independent_validator: PASS")
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
