<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND CERTIFIED - decision entry ADR-0008 PROPOSED pending owner ratification (Q1) |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD (see docs/OPEN_QUESTIONS.md Q1) |

# Transit event layer specification

> **Provenance and normative status.** This specification was authored as a plan,
> approved by the owner conversationally, and implemented before being lifted into
> `docs/`. `docs/PROJECT_CONSTITUTION.md` s7 states that anything not in the repository
> is input material and not truth, so the out-of-repository original carried no
> authority; this file is the resident specification. The governing decision is recorded
> in `docs/DECISION_LOG.md` at ADR-0008, whose status is PROPOSED pending owner
> ratification (Q1). The text below is DESCRIPTIVE of the certified implementation and
> of the decisions actually taken; the ADR is the normative record. Sections retain the
> numbering of the original plan, including its implementation and publication records,
> which are preserved as dated evidence.

Date: 2026-08-09
Status: PROPOSED. Implementation starts only after explicit approval.
Base: origin/main 7394441 (VIMSHOTTARI_V1 certified and published).

## 1. Objective and scope

Build TRANSIT_V1: deterministic transit computation on top of the certified astronomy, as a new isolated engine/transits/ package. Two capabilities, both facts-only:

First, transit snapshots: the certified AstronomySnapshot already computes any moment; the transit layer adds the natal-relative view (transiting positions annotated with the natal chart's reference points) under an explicit profile, provenance-stamped.

Second, transit events by root-finding: the times at which a transiting body's sidereal longitude crosses a target longitude. This one primitive covers sign ingresses, nakshatra ingresses (and their padas), returns (body crossing its own natal longitude), and transit-to-natal conjunctions. V1 certifies exactly this crossing primitive and the event types built from it.

Explicit non-goals of V1: no aspect-system events (Parashari special aspects and Western angular aspects are school-layer work gated on the aspect-systems phase), no interpretation, no dasha-transit convergence (that belongs to the convergence layer), no topocentric or heliocentric variants.

## 2. The mathematics

A crossing event is a root of f(t) = wrapped_difference(longitude(t), target) on a time interval. The engine finds all roots in a requested window by: sampling f on a step grid sized to the body's maximum angular speed (so no crossing can hide between samples, including retrograde reversals), bracketing sign changes, and refining each bracket by bisection on the certified sidereal longitude function until the time bracket is below tolerance. Bisection is chosen over faster methods deliberately: it is unconditionally convergent and every step is an evaluation of the already-certified position pipeline, so the event time inherits Tier-0's certification. Retrograde motion yields multiple events for the same target; all are reported, each flagged with the motion direction at crossing.

## 3. Decisions that need your explicit sign-off

Decision TR-A, time tolerance: refine brackets to 1e-6 day (about 0.086 s). At the Moon's maximum speed this is about 0.006 arcsec of longitude, far inside the certified 0.5 arcsec envelope; tighter serves nothing physical (UTC-as-UT1 is itself bounded by 0.9 s, already documented).

Decision TR-B, sampling safety margin: grid step = 0.5 x (360 / max_speed_deg_per_day) per body, with documented per-body maximum speeds taken from Swiss Ephemeris extremes and a safety factor of 4. Slower sampling risks missed double crossings near stations; this makes misses mathematically impossible rather than unlikely.

Decision TR-C, verification strategy: swetest remains the position authority (D-001). Event times are verified three ways: (1) residual check, the certified longitude at the found time must be within 1e-4 arcsec of the target; (2) an independent in-validator event finder using dense scanning plus inverse quadratic interpolation, built differently from the production bisection, must find the same event set with matching times; (3) an external anchor set: published sidereal Sun ingress instants (Makara Sankranti and the other sankrantis, which pyjhora's panchanga module computes independently) compared within a documented tolerance, with categorical (event existence and ordering) tolerance zero.

## 4. Certification gates

Gate 1, primitive invariants: every reported event's residual under the certified position function is within tolerance; events are complete (the independent scanner finds nothing the production finder missed, over dense test windows including Mercury retrograde loops and Moon perigee speeds); direction flags match the sign of the speed at the event.

Gate 2, cross-layer consistency: sign and nakshatra ingress events land exactly on the certified boundary longitudes; the classification of a point epsilon after an ingress agrees with the certified sign/nakshatra/KP-chain primitives.

Gate 3, external anchors: sankranti (sidereal Sun ingress) instants versus pyjhora's independently computed panchanga values across multiple years and both ayanamsa profiles, plus a Moon nakshatra-ingress spot set; categorical agreement exact, time agreement within a tolerance derived from the recorded oracle astronomy delta (the same D-007 discipline used for VIMSHOTTARI_V1).

Gate 4, independent validator: root-level validate_transits_holdout.py, in-file scan-based finder, no imports from engine/transits.

Gate 5, certification artifact and full-battery regression proof, same pattern as the previous phases (runner script, regenerated JSON, collected artifact-pinning test, additive README update).

## 5. Implementation order

Step 1: crossing primitive plus per-body speed table, Gates 1 and 2. Step 2: event types (sign/nakshatra ingress, return, natal-point conjunction) and the natal-relative snapshot view. Step 3: oracle anchors and independent validator, Gates 3 and 4. Step 4: certification runner, artifact, docs, Gate 5. Publication by bundle relay or PAT, then fresh-clone verification. Full battery after every commit.

## 6. Risks

Stations (speed near zero) make crossings tangent rather than transversal; the bracketing logic must treat grazing contacts explicitly (report if the extremum actually touches the target, with a documented rule). Long windows over centuries multiply ephemeris calls; the step grid is per-body, so cost stays proportional. pyjhora anchor times carry that oracle's ~1 arcsec astronomy, which for the Sun (about 1 deg/day) means up to ~24 s of event-time difference; the tolerance will be derived and recorded per body, never silently widened.

## 7. What I need from you

Approve or amend: the overall plan, TR-A (1e-6 day event tolerance), TR-B (speed-bounded sampling with 4x safety), TR-C (three-way verification with swetest authority and pyjhora anchors under D-007). One word, approved, covers all.

## Implementation record (2026-08-09) - BUILT AND VERIFIED, PENDING PUBLICATION

Built on branch transit-v1 (two commits on top of published main 7394441; tip b6a9d2cca7728c95937c6445b3ee28074f8c9435). Provably additive; only README.md modified (including reconciling its non-claims line with the certified dasha and transit layers).

Approved decisions executed: TR-A event-time guarantee 1e-6 day, with the actual bisection bracket tightened to 1e-9 day so residuals meet the 1e-4 arcsec bound at lunar maximum speed; TR-B 45 degree max motion per sample with generous speed bounds x safety 4; TR-C three-way verification.

Oracle findings recorded per D-001/D-007: PyJHora's Sun differs from the certified Sun by ~20.5 arcsec at compared instants (magnitude consistent with aberration handling differences, cause NOT VERIFIED) and its ingress search diverges at tight precision settings, so anchor tolerances are derived per event (measured delta / local speed + 120 s slop). All 24 sankranti anchors pass, worst at 81% of derived tolerance, categorical agreement exact. Gate results: residual battery 74 events max 2.1e-5 arcsec; completeness equal to independent fine scans (Sun, Moon, Mars, retrograde Mercury); Mercury 2024 retrograde triple crossing with direction sequence +1/-1/+1; independent validator 86 events within 1e-5 day, zero failures. Full battery: 303 tests, five independent validators, legacy gate 5/5, four certification runners regenerate PASS.

## Publication record (2026-08-09)

Published via owner bundle relay: origin/transit-v1 pushed, main fast-forwarded 7394441 -> b6a9d2cca7728c95937c6445b3ee28074f8c9435. Fresh-clone post-publication verification (EXECUTED): 303 tests, five independent validators PASS, legacy gate 5/5, four certification runners regenerate PASS, tree clean. TRANSIT_V1 is CERTIFIED and PUBLISHED.
## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-09 | Lifted into docs/ from the out-of-repository plan document(s): TRANSIT_ENGINE_PLAN.md. Content preserved; header, provenance note and change history added per docs/DOCUMENTATION_STANDARD.md s2. |
