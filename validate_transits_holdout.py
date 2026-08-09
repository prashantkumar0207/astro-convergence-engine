"""Independent transit-event holdout validator (Gate 4 of ADR-TRANSIT-001).

Validates engine/transits against an event finder built INDEPENDENTLY
inside this file: dense fixed-step scanning with inverse quadratic
interpolation (Brent-style refinement), a different construction from
the production station-aware bisection. Nothing is imported from
engine/transits. The certified position pipeline is the shared
authority for positions (D-001); what this validator independently
re-derives is the EVENT FINDING.

Run:  python validate_transits_holdout.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import swisseph as swe

from engine.astronomy.profile import PARASHARI_LAHIRI
from engine.astronomy.sidereal_planets import sidereal_planet_position
from engine.transits.crossing import find_crossings  # SUBJECT
from engine.transits.events import nakshatra_ingresses, sign_ingresses  # SUBJECT

MODE = PARASHARI_LAHIRI.ayanamsa_mode
TIME_AGREEMENT_DAYS = 1e-5  # ~0.86 s


def longitude(body_id, julian_day):
    return sidereal_planet_position(julian_day, body_id, MODE).longitude


def wrap(delta):
    return -((-delta + 180.0) % 360.0 - 180.0)


def reference_events(body_id, target, jd0, jd1, step):
    """Scan + inverse-quadratic refinement, independent of production."""

    def diff(julian_day):
        return wrap(longitude(body_id, julian_day) - target)

    events = []
    previous_jd, previous = jd0, diff(jd0)
    cursor = jd0 + step
    while cursor <= jd1 + 1e-12:
        current = diff(cursor)
        if previous * current < 0 and abs(previous - current) < 180.0:
            a, fa, b, fb = previous_jd, previous, cursor, current
            for _ in range(200):
                mid = 0.5 * (a + b)
                fm = diff(mid)
                # inverse quadratic estimate when values are distinct
                if fa != fm and fb != fm and fa != fb:
                    est = (
                        a * fb * fm / ((fa - fb) * (fa - fm))
                        + b * fa * fm / ((fb - fa) * (fb - fm))
                        + mid * fa * fb / ((fm - fa) * (fm - fb))
                    )
                else:
                    est = mid
                if not (a < est < b):
                    est = mid
                fe = diff(est)
                if fa * fe <= 0:
                    b, fb = est, fe
                else:
                    a, fa = est, fe
                if b - a < 1e-10:
                    break
            events.append(0.5 * (a + b))
        previous_jd, previous = cursor, current
        cursor += step
    return events


def compare(label, subject_events, body_id, target, jd0, jd1, step, failures):
    subject_times = [event.julian_day for event in subject_events
                     if event.direction != 0 and abs(wrap(event.target_longitude - target)) < 1e-12]
    reference_times = reference_events(body_id, target, jd0, jd1, step)
    if len(subject_times) != len(reference_times):
        failures.append((label, "count", len(subject_times), len(reference_times)))
        return 0
    for ours, theirs in zip(subject_times, reference_times):
        if abs(ours - theirs) > TIME_AGREEMENT_DAYS:
            failures.append((label, "time", ours, theirs))
    return len(reference_times)


def main() -> int:
    failures = []
    checked = 0

    jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)

    # 1. Sun sign ingresses, two years, all 12 boundaries.
    sun_events = sign_ingresses("Sun", jd0, jd0 + 731, PARASHARI_LAHIRI)
    for k in range(12):
        checked += compare(f"sun_ingress_{k*30}", 
                           [e for e in sun_events if e.target_longitude == 30.0 * k],
                           swe.SUN, 30.0 * k, jd0, jd0 + 731, 1.0, failures)

    # 2. Moon nakshatra ingresses, 60 days, all 27 boundaries.
    moon_events = nakshatra_ingresses("Moon", jd0, jd0 + 60, PARASHARI_LAHIRI)
    for k in range(27):
        target = float(k * (40.0 / 3.0))
        checked += compare(f"moon_nak_{k}",
                           [e for e in moon_events if abs(e.target_longitude - target) < 1e-9],
                           swe.MOON, target, jd0, jd0 + 60, 0.02, failures)

    # 3. Mercury through its 2024 retrograde loop (triple crossing).
    jd_retro = swe.julday(2024, 3, 1, 0.0, swe.GREG_CAL)
    mercury = find_crossings("Mercury", 355.0, jd_retro, jd_retro + 106, PARASHARI_LAHIRI)
    checked += compare("mercury_retro_355", mercury, swe.MERCURY, 355.0,
                       jd_retro, jd_retro + 106, 0.05, failures)

    # 4. Mars slow crossing.
    mars = find_crossings("Mars", 150.0, jd0, jd0 + 500, PARASHARI_LAHIRI)
    checked += compare("mars_150", mars, swe.MARS, 150.0, jd0, jd0 + 500, 0.25, failures)

    print("=" * 60)
    print("INDEPENDENT TRANSIT EVENT VALIDATION")
    print("=" * 60)
    print(f"Events cross-checked : {checked}")
    print(f"Time agreement bound : {TIME_AGREEMENT_DAYS} days")
    if failures:
        print(f"FAILURES: {len(failures)}; first: {failures[:4]}")
        print("RESULT: FAIL")
        return 1
    print()
    print("RESULT: ALL INDEPENDENT TRANSIT CASES PASSED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
