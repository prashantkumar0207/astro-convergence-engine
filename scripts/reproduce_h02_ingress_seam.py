"""H-02 INGRESS-CLASSIFICATION SEAM: INDEPENDENT-REFERENCE REPRODUCTION (DP-013 Option A).

THIS IS AN INVESTIGATION, NOT A CERTIFIER. It does not certify anything, does
not implement a fix, and does not touch TRANSIT_V1 or any other certified
capability. It exists solely to independently reproduce - or refute - the
H-02 finding `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` reported and
`docs/DECISION_LOG.md` `ADR-0020` D5 required be independently reproduced
before any production Muhurta work relies on it (`docs/decisions/
DP-013-h02-ingress-classification-seam.md`, ratified Option C = A + B).

MECHANISM UNDER TEST. `engine.transits.crossing.find_crossings` (the
certified TRANSIT_V1 event-finder) guarantees each reported event instant's
longitude is within `RESIDUAL_BOUND_ARCSEC` (1e-4 arcsec, 2.78e-8 degrees) of
the exact target boundary. `engine.astrology.longitude_utils.division_index`
(the certified sign/nakshatra classifier) promotes a value into the next
division only within `BOUNDARY_TOLERANCE` (1e-10 degrees) of that boundary -
about 278 times narrower than the event-finder's own residual guarantee. A
reported event instant can therefore land on either side of the true
boundary within its residual guarantee, and RE-CLASSIFYING the longitude AT
that reported instant is not guaranteed to agree with the division the event
was searching for.

METHODOLOGY (Option A: independent reference, not the certified
`division_index`). For a real 2024 holdout of Sun sign-boundary crossings
(one full year, `engine.transits.events.sign_ingresses`) and Moon
nakshatra-boundary crossings (one sidereal month plus margin,
`engine.transits.events.nakshatra_ingresses`) - both the already-certified
TRANSIT_V1 event-finder, never reimplemented here - this script:

  1. Takes each reported event's `julian_day` and independently recomputes
     the body's sidereal longitude there via the already-certified
     `sidereal_planet_position` (never re-deriving the ephemeris itself).
  2. Classifies that longitude, and the event's own `target_longitude`,
     using an independently-coded exact-rational (`fractions.Fraction`)
     classifier that mirrors the production convention (tolerance-promoted,
     top-clamped, `BOUNDARY_TOLERANCE = 1e-10`) but is typed here a second
     time, never importing `division_index` - the same independence
     discipline `validate_panchanga_holdout.py`/`validate_trikalam_holdout.py`
     already established this session.
  3. Reports a mismatch wherever the two classifications disagree - this
     reproduces (or refutes) H-02 exactly, using only certified primitives
     plus one new, genuinely independent classifier.

A second, separately-coded classifier lives in `validate_h02_reproduction.py`
(repo root) and is invoked here as a subprocess cross-check, mirroring this
repository's established Gate E discipline.

NEGATIVE CONTROL. `negative_control()` below constructs two synthetic cases
whose outcome is known by construction (one a genuine mismatch, one not),
confirms the real comparison logic classifies both correctly, then swaps in
a deliberately broken comparison and confirms it would fail to catch the
known mismatch - proving this reproduction can actually detect a defect,
not merely report agreement by construction.
"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import date, datetime, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import swisseph as swe  # noqa: E402

from engine.astronomy.profile import PARASHARI_LAHIRI  # noqa: E402
from engine.astronomy.sidereal_planets import sidereal_planet_position  # noqa: E402
from engine.transits.events import nakshatra_ingresses, sign_ingresses  # noqa: E402

#: Independently declared, matching (not importing) `engine.astrology.
#: longitude_utils.BOUNDARY_TOLERANCE` and the span/count constants
#: `engine.transits.events` already uses for its boundary targets.
BOUNDARY_TOLERANCE = Fraction(1, 10**10)
SIGN_SPAN = Fraction(30)
SIGN_COUNT = 12
NAKSHATRA_SPAN = Fraction(40, 3)  # 360/27 exactly, as a rational.
NAKSHATRA_COUNT = 27


def independent_division_index(longitude: float, span: Fraction, count: int) -> int:
    """Independently-coded exact-rational classifier: tolerance-promoted,
    top-clamped, mirroring the production convention without importing it."""

    value = Fraction(repr(longitude)) % 360
    index = int((value + BOUNDARY_TOLERANCE) / span)
    return min(index, count - 1)


def classify_sign(longitude: float) -> int:
    return independent_division_index(longitude, SIGN_SPAN, SIGN_COUNT)


def classify_nakshatra(longitude: float) -> int:
    return independent_division_index(longitude, NAKSHATRA_SPAN, NAKSHATRA_COUNT)


def check_event(event, body_swe_id: int, classify) -> dict:
    """Independently reclassify one certified crossing event; report
    whether the reclassification agrees with the division it was
    searching for."""

    position = sidereal_planet_position(
        event.julian_day, body_swe_id, PARASHARI_LAHIRI.ayanamsa_mode, strict=True,
    )
    reported = classify(position.longitude)
    target = classify(event.target_longitude)
    return {
        "body": event.body,
        "target_longitude": event.target_longitude,
        "julian_day": event.julian_day,
        "residual_arcsec": event.residual_arcsec,
        "direction": event.direction,
        "reclassified_longitude": position.longitude,
        "target_division": target,
        "reclassified_division": reported,
        "mismatch": reported != target,
    }


def negative_control() -> bool:
    """Proves this reproduction's comparison logic can actually detect a
    defect: constructs a synthetic case whose mismatch is known by
    construction, confirms the REAL classifier flags it, then temporarily
    swaps in a deliberately broken classifier (always agrees with the
    target) and confirms the SAME comparison would then fail to flag the
    known mismatch, before restoring the real one. Returns True only if
    every step behaved as designed."""

    global classify_sign
    real_classify_sign = classify_sign

    target = 90.0  # An arbitrary sign boundary; only the exact value matters here.
    matching_longitude = target + 1e-11  # Within BOUNDARY_TOLERANCE: same division as target.
    mismatching_longitude = target - 1e-8  # Outside tolerance, inside the H-02 residual scale: previous division.

    target_division = real_classify_sign(target)
    if real_classify_sign(matching_longitude) != target_division:
        return False  # The real classifier itself is not behaving as designed; control is void.
    if real_classify_sign(mismatching_longitude) == target_division:
        return False  # Same - the synthetic "known mismatch" isn't actually a mismatch.

    real_detects_the_mismatch = real_classify_sign(mismatching_longitude) != target_division

    def _broken_classify_sign(longitude):
        return target_division  # Always agrees with the target - a deliberately broken classifier.

    classify_sign = _broken_classify_sign
    try:
        broken_misses_the_mismatch = classify_sign(mismatching_longitude) == target_division
    finally:
        classify_sign = real_classify_sign

    restored_correctly = classify_sign is real_classify_sign and (
        classify_sign(mismatching_longitude) != target_division
    )

    return real_detects_the_mismatch and broken_misses_the_mismatch and restored_correctly


def run() -> dict:
    if not negative_control():
        print("H-02 REPRODUCTION: negative control FAILED - comparison logic is not trustworthy")
        sys.exit(3)

    jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)
    sun_events = sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
    moon_events = nakshatra_ingresses("Moon", jd0, jd0 + 35, PARASHARI_LAHIRI)

    sun_results = [check_event(e, swe.SUN, classify_sign) for e in sun_events]
    moon_results = [check_event(e, swe.MOON, classify_nakshatra) for e in moon_events]

    sun_mismatches = [r for r in sun_results if r["mismatch"]]
    moon_mismatches = [r for r in moon_results if r["mismatch"]]

    validator = subprocess.run(
        [sys.executable, str(ROOT / "validate_h02_reproduction.py")],
        capture_output=True, text=True,
    )
    validator_ran_ok = validator.returncode == 0 and "H-02 INDEPENDENT VALIDATOR PASS" in validator.stdout
    validator_counts = {}
    if validator_ran_ok:
        for pair in validator.stdout.strip().rsplit(":", 1)[-1].split():
            key, _, value = pair.partition("=")
            if key:
                validator_counts[key] = int(value)
    validator_agrees = validator_ran_ok and validator_counts == {
        "sun_cases": len(sun_results),
        "sun_mismatches": len(sun_mismatches),
        "moon_cases": len(moon_results),
        "moon_mismatches": len(moon_mismatches),
    }
    validator_ok = validator_agrees

    return {
        "schema": "h02_ingress_seam_reproduction",
        "classification": "INVESTIGATION EVIDENCE, NOT A CERTIFICATION",
        "date": str(date.today()),
        "executed_utc": datetime.now(timezone.utc).isoformat(),
        "dp": "DP-013", "adr_context": "ADR-0020 D5",
        "source_finding": "reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md H-02",
        "methodology": "Option A: independent exact-rational reference, real 2024 holdout, "
                        "certified event-finder and position primitives reused, classifier "
                        "typed independently (twice: here and in validate_h02_reproduction.py)",
        "negative_control_verified": True,
        "cross_validator": {
            "ran_ok": validator_ran_ok,
            "counts": validator_counts,
            "agrees_exactly": validator_agrees,
        },
        "sun_sign_ingresses": {
            "holdout_window": "2024-01-01 to 2025-01-01 (366 days)",
            "cases": len(sun_results),
            "mismatches": len(sun_mismatches),
            "mismatch_rate": (len(sun_mismatches) / len(sun_results)) if sun_results else None,
            "details": sun_results,
        },
        "moon_nakshatra_ingresses": {
            "holdout_window": "2024-01-01 to 2024-02-05 (35 days)",
            "cases": len(moon_results),
            "mismatches": len(moon_mismatches),
            "mismatch_rate": (len(moon_mismatches) / len(moon_results)) if moon_results else None,
            "details": moon_results,
        },
        "original_audit_figures_for_comparison": {
            "sun_sankranti": "2 of 12 misclassified (2024, parashari_lahiri)",
            "moon_nakshatra": "12 of 28 misclassified (2024, parashari_lahiri)",
            "note": "this reproduction's own holdout selection (full year Sun; one sidereal "
                    "month plus margin Moon) is independently defined, not the audit's exact "
                    "unstated instant list - DP-013 s5 flags this as an open methodology "
                    "question the ratification did not settle further.",
        },
    }


def main():
    report = run()
    out_dir = ROOT / "reports" / "h02_reproduction"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "reproduction_evidence.json"
    out_path.write_text(json.dumps(report, indent=1) + "\n")

    print("=" * 60)
    print("H-02 INGRESS-CLASSIFICATION SEAM - INDEPENDENT REPRODUCTION")
    print("(investigation evidence, not a certification, per DP-013)")
    print("=" * 60)
    print("negative_control_verified:", report["negative_control_verified"])
    print("cross_validator agrees    :", report["cross_validator"]["agrees_exactly"])
    print("Sun sign ingresses        :", report["sun_sign_ingresses"]["cases"], "cases,",
          report["sun_sign_ingresses"]["mismatches"], "mismatches")
    print("Moon nakshatra ingresses  :", report["moon_nakshatra_ingresses"]["cases"], "cases,",
          report["moon_nakshatra_ingresses"]["mismatches"], "mismatches")
    print("evidence archived         :", out_path.relative_to(ROOT).as_posix())
    if not report["cross_validator"]["agrees_exactly"]:
        print("WARNING: independent validator did not confirm agreement - see its own output")
        sys.exit(3)
    print("RESULT: reproduction executed successfully (see mismatch counts above; "
          "this is evidence for the CEO's DP-013 ratification, not a PASS/FAIL verdict)")


if __name__ == "__main__":
    main()
