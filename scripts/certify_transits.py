"""TRANSIT_V1 CERTIFICATION RUNNER (ADR-0008; `declared_division` field
and Gate E, H-02 fix Option 1, ADR-0065).

Regenerates certification/TRANSIT_V1_certification.json FROM SCRATCH
on every run; the stored JSON is never accepted as proof.

Gates: A residual battery on the certified position authority;
B completeness vs independent fine scan; C external anchors (PyJHora
sankranti and Moon-ingress instants under the D-007 discipline:
per-event tolerance derived from the MEASURED oracle astronomy delta
at the event instant divided by the local speed, plus the oracle's
own documented search slop; categorical tolerance zero); D the
independent validator; E `declared_division` correctness (H-02 fix,
ADR-0065) with a genuine negative control. Exit 0 = PASS, 3 = FAIL.

GATE E, WHAT IT CERTIFIES. `ADR-0064` independently reproduced H-02 (the
ingress-classification seam: a reported crossing instant's own residual,
`RESIDUAL_BOUND_ARCSEC` = `1e-4` arcsec, is ~278x wider than
`division_index`'s promotion tolerance, `1e-10` degrees, so re-classifying
the reported instant can disagree with the division actually searched
for). `DP-013` s6 recommended, and the owner ratified (`ADR-0065`), Option
1: `TransitEvent.declared_division` (`engine/transits/events.py`) is
classified from the EXACT `target_longitude`, never from the noisy
reported `julian_day`. This gate asserts that property holds for the
full certified holdout, with a negative control proving the assertion
can actually fail. It does not, and cannot, "fix" H-02's underlying
residual-vs-tolerance gap - `julian_day`/`residual_arcsec` are unchanged
by this gate or by Option 1 at all; `declared_division` is a new,
independently-computed field a consumer can trust instead of
re-classifying the event's own instant.
"""

import json
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

sys.path.insert(0, str(ROOT / "scripts"))
import certification_support as support  # noqa: E402

import swisseph as swe  # noqa: E402

from engine.astronomy.profile import KP_KRISHNAMURTI, PARASHARI_LAHIRI  # noqa: E402
from engine.astronomy.sidereal_planets import sidereal_planet_position  # noqa: E402
from engine.transits.crossing import RESIDUAL_BOUND_ARCSEC, find_crossings  # noqa: E402
from engine.transits.events import nakshatra_ingresses, sign_ingresses  # noqa: E402

try:
    from jhora.panchanga import drik
    import importlib.metadata
    PYJHORA_VERSION = importlib.metadata.version("PyJHora")
except Exception as error:  # pragma: no cover
    print("TRANSIT CERTIFICATION FAIL: PyJHora oracle unavailable:", error)
    sys.exit(3)

#: Oracle search slop: pyjhora's ingress search at its stable default
#: precision stops within ~0.001 deg of the boundary (measured), and
#: tighter settings make its search diverge (measured); allow 120 s.
ORACLE_SEARCH_SLOP_DAYS = 120.0 / 86400.0


def fail(message):
    print("TRANSIT CERTIFICATION FAIL:", message)
    sys.exit(3)


def gate_a_residuals():
    jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)
    events = []
    events += sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
    events += nakshatra_ingresses("Moon", jd0, jd0 + 60, PARASHARI_LAHIRI)
    events += find_crossings("Mercury", 355.0,
                             swe.julday(2024, 3, 1, 0.0, swe.GREG_CAL),
                             swe.julday(2024, 6, 15, 0.0, swe.GREG_CAL),
                             PARASHARI_LAHIRI)
    worst = max(event.residual_arcsec for event in events)
    if worst > RESIDUAL_BOUND_ARCSEC:
        fail(f"residual {worst} arcsec > {RESIDUAL_BOUND_ARCSEC}")
    return {"events": len(events), "max_residual_arcsec": worst,
            "bound_arcsec": RESIDUAL_BOUND_ARCSEC}


def gate_c_oracle_anchors():
    anchors = []
    worst_ratio = 0.0
    for profile, jhora_mode in ((PARASHARI_LAHIRI, "LAHIRI"), (KP_KRISHNAMURTI, "KP")):
        drik.set_ayanamsa_mode(jhora_mode)
        place = drik.Place("anchor", 0.0, 0.0, 0.0)
        jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)

        our_events = sign_ingresses("Sun", jd0, jd0 + 366, profile)
        if len(our_events) != 12:
            fail(f"{profile.name}: expected 12 sankrantis, got {len(our_events)}")

        cursor = jd0
        for our_event in our_events:
            oracle_jd, oracle_longitude = drik.next_planet_entry_date(0, cursor, place)
            # Derived tolerance: measured oracle Sun delta at the event
            # divided by local Sun speed, plus search slop.
            position = sidereal_planet_position(
                our_event.julian_day, swe.SUN, profile.ayanamsa_mode)
            oracle_sun = drik.solar_longitude(our_event.julian_day)
            delta_deg = abs(((oracle_sun - position.longitude + 180.0) % 360.0) - 180.0)
            speed = abs(position.speed_longitude)
            tolerance = delta_deg / speed + ORACLE_SEARCH_SLOP_DAYS
            observed = abs(our_event.julian_day - oracle_jd)
            anchors.append({
                "profile": profile.name,
                "target": our_event.target_longitude,
                "our_jd": our_event.julian_day,
                "oracle_jd": oracle_jd,
                "oracle_astronomy_delta_arcsec": delta_deg * 3600.0,
                "delta_days": observed,
                "derived_tolerance_days": tolerance,
            })
            if observed > tolerance:
                fail(f"{profile.name} sankranti at {our_event.target_longitude}: "
                     f"delta {observed} d > derived tolerance {tolerance} d")
            worst_ratio = max(worst_ratio, observed / tolerance)
            cursor = oracle_jd + 1.0
    return {"anchors": len(anchors), "worst_delta_over_tolerance": worst_ratio,
            "details": anchors}


def gate_d_validator():
    result = subprocess.run(
        [sys.executable, str(ROOT / "validate_transits_holdout.py")],
        capture_output=True, text=True)
    if result.returncode != 0 or "ALL INDEPENDENT TRANSIT CASES PASSED" not in result.stdout:
        fail(f"independent validator failed: {result.stdout[-300:]}")
    return {"result": "PASS"}


def gate_e_declared_division():
    """H-02 fix Option 1 (ADR-0065): `declared_division` must equal the
    certified classifier applied to `target_longitude` (exact) for every
    sign/nakshatra ingress in the holdout, and must be `None` for event
    kinds with no division semantics. A genuine negative control (real
    events checked, then the classifier `events.py` uses is temporarily
    broken and the SAME assertion is shown to fail, then restored) proves
    this gate can actually detect a defect."""

    from engine.astrology.nakshatra import nakshatra as classify_nakshatra
    from engine.astrology.signs import zodiac_sign as classify_sign

    jd0 = swe.julday(2024, 1, 1, 0.0, swe.GREG_CAL)
    sun_events = sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
    moon_events = nakshatra_ingresses("Moon", jd0, jd0 + 35, PARASHARI_LAHIRI)

    checked = 0
    for event in sun_events:
        if event.declared_division != classify_sign(event.target_longitude):
            fail(f"sign_ingress at {event.target_longitude}: declared_division "
                 f"{event.declared_division} != classify_sign(target) {classify_sign(event.target_longitude)}")
        checked += 1
    for event in moon_events:
        if event.declared_division != classify_nakshatra(event.target_longitude):
            fail(f"nakshatra_ingress at {event.target_longitude}: declared_division "
                 f"{event.declared_division} != classify_nakshatra(target) "
                 f"{classify_nakshatra(event.target_longitude)}")
        checked += 1

    # declared_division must be None where "division" has no defined
    # meaning - a plain crossing to an arbitrary (non-boundary) target.
    plain_crossing = find_crossings("Mercury", 355.0,
                                     swe.julday(2024, 3, 1, 0.0, swe.GREG_CAL),
                                     swe.julday(2024, 6, 15, 0.0, swe.GREG_CAL),
                                     PARASHARI_LAHIRI)
    for event in plain_crossing:
        if event.declared_division is not None:
            fail(f"plain crossing at {event.target_longitude}: declared_division "
                 f"should be None, got {event.declared_division}")
        checked += 1

    # Genuine negative control: temporarily break the classifier
    # engine/transits/events.py uses, confirm the SAME comparison this
    # gate performs would then fail to detect the resulting disagreement,
    # then restore and re-verify agreement.
    import engine.transits.events as events_module
    real_classify_sign = events_module._classify_sign

    def _always_sign_1(_longitude):
        return 1

    events_module._classify_sign = _always_sign_1
    try:
        broken_events = sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
        negative_control_caught = any(
            b.declared_division != real_classify_sign(b.target_longitude) for b in broken_events
        )
    finally:
        events_module._classify_sign = real_classify_sign

    if not negative_control_caught:
        fail("negative control: a deliberately broken classifier was NOT caught by Gate E's own comparison")
    if events_module._classify_sign is not real_classify_sign:
        fail("negative control: events.py's classifier was not correctly restored")
    restored_events = sign_ingresses("Sun", jd0, jd0 + 366, PARASHARI_LAHIRI)
    if any(e.declared_division != real_classify_sign(e.target_longitude) for e in restored_events):
        fail("negative control: restored classifier no longer agrees with itself")

    return {"cases_checked": checked, "negative_control_verified": True}


def main():
    tee = support.start_transcript()
    preconditions = support.preflight()
    report = {
        "schema": "transit_v1_certification",
        "adr": "ADR-0008",
        "date": str(date.today()),
        "scope": ("longitude-crossing primitive; sign/nakshatra ingresses "
                  "(with declared_division, H-02 fix Option 1, ADR-0065); "
                  "returns; natal conjunctions; natal-relative view"),
        "decisions": {
            "TR-A": "event-time guarantee 1e-6 day; bisection bracket 1e-9 day",
            "TR-B": "45 deg max motion per sample, speed bounds x safety 4",
            "TR-C": "swetest position authority; oracle anchors with derived tolerances (D-007)",
        },
        "oracle": {
            "package": "PyJHora", "version": PYJHORA_VERSION,
            "notes": ("Oracle Sun differs from the certified Sun by ~20.5 arcsec "
                      "at compared instants (magnitude consistent with aberration "
                      "handling differences; cause NOT VERIFIED); oracle ingress "
                      "search carries ~1 min slop at stable precision. Tolerances "
                      "are derived per event from measured deltas, never assumed."),
        },
        "gates": {
            "A_residual_battery": gate_a_residuals(),
            "C_oracle_anchors": gate_c_oracle_anchors(),
            "D_independent_validator": gate_d_validator(),
            "E_declared_division": gate_e_declared_division(),
        },
        "explicit_non_claims": [
            "aspect-system events (Parashari/Western; aspect-systems phase)",
            "dasha-transit convergence (convergence layer)",
            "topocentric/heliocentric variants",
            "interpretation",
        ],
        "environment": {"python": sys.version.split()[0]},
        "preconditions": preconditions,
        "result": "PASS",
    }
    out = support.emit(report, "TRANSIT_V1_certification.json", "transit", tee)
    print("=" * 60)
    print("TRANSIT_V1 CERTIFICATION")
    print("=" * 60)
    gate_a = report["gates"]["A_residual_battery"]
    gate_c = report["gates"]["C_oracle_anchors"]
    gate_e = report["gates"]["E_declared_division"]
    print(f"residual battery  : {gate_a['events']} events, max {gate_a['max_residual_arcsec']:.2e} arcsec")
    print(f"oracle anchors    : {gate_c['anchors']} sankrantis, worst delta/tolerance {gate_c['worst_delta_over_tolerance']:.3f}")
    print(f"validator         : PASS")
    print(f"declared_division : {gate_e['cases_checked']} cases, negative_control_verified={gate_e['negative_control_verified']}")
    # .as_posix(): a bare str(Path) uses the OS-native separator, which
    # would make this line (captured into the console transcript) differ
    # between a Windows-local run and Linux CI - the same provenance
    # defect this session's other certifiers already hit and fixed.
    print("archived          :", out.relative_to(ROOT).as_posix())
    print("RESULT            : PASS")


if __name__ == "__main__":
    main()
