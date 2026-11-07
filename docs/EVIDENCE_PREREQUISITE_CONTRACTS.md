<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | IMPLEMENTED AND DECIDED: M-04, M-05 and M-09 are merged (PRs #44, #45 and #46), and every s4 item is resolved by `ADR-0111`, `ADR-0112` or `ADR-0113`. Kept as the record of the contracts. |
| Version | 1.2.0 |
| Owner | Project Owner (`ADR-0051` D4) |
| Last updated | 2026-11-06 |
| Review cadence | On each authorization below |

# EVIDENCE prerequisite closure: implementation contracts

This document serves `Q8_CLOSURE_MATRIX.md` s6. It covers M-04, M-05 and M-09, and the specification decisions that
remain. Baseline: `main` `6c93a1405d3c1e3c9e15ecac09883e90c0308a19`. Each defect below was confirmed live by a read-only
runtime probe. **Nothing here changes a calculation, and nothing here may be implemented without authorization.**

Three rules apply to every contract:
- each fix lands in its own PR, with the affected artifacts regenerated and reconciled;
- a committed negative control must reject the original defect;
- CI must pass on all four jobs.

## 1. M-04: DrishtiChart house convention (`DP-025` A2 Option 1, selected by `ADR-0111`)

**Defect.** `DrishtiChart.provenance.house_system == 'P'`, which is Placidus, while `PlanetDrishti.aspected_houses` are
whole-sign (`engine/models/drishti.py:15`). No field states the convention.

**Contract.**
- Add one field to `DrishtiChart`: `houses_convention: str = "whole_sign"`. It is additive, defaulted and immutable.
- Leave `provenance`, signs, houses and every other value unchanged.

**Certification impact.**
- Regenerate `PARASHARI_DRISHTI_V1`. The new field is the only expected difference; anything else is a failure.
- `SIGN_CONVENTION_V1` Gate C walks model fields. It must still pass, because the field is not a sign index.
- C2, C3 and C4 should not change.

**Negative control.** A test fails if the field is absent or differs from the convention that `aspected_houses` uses.

**Not covered.** `DP-025` A1, the polar-Placidus gap, stays open.

## 2. M-05: Transit provenance (not waiting for `DP-040`, per `ADR-0111`)

**Defect.**
- `TransitEvent` has a bare `profile_name`, and no provenance (`engine/transits/crossing.py:172` and `:190`).
- `TransitView.provenance` is the transit moment's. The natal provenance is checked at `engine/transits/view.py:59`, then
  dropped.

**Contract.**
1. **Shared builder.** Factor `Provenance` construction out of `engine/astronomy/astronomy_snapshot.py:77` into one
   function of the profile, so events and snapshots cannot diverge.
2. **`TransitEvent`.** Add `provenance: Provenance`, built from `find_crossings`' own `profile`. Keep `profile_name` and
   `declared_division`, so existing consumers do not break.
3. **`TransitView`.** Add `natal_provenance: Provenance`, carrying the provenance that `transit_view` already validates.
4. **No behaviour change.** Leave every computed value alone: crossing times, directions, residuals, longitudes and contacts.

**Certification impact.**
- Regenerate `TRANSIT_V1`. The added provenance blocks are the only expected difference.
- `VIMSHOTTARI_V1` uses `find_crossings` only for near-boundary times. Its drift gate must stay clean.
- **The three `TRANSIT_V1` overclaims must stay `OPEN_SCOPE_OVERCLAIM`,** and no `DP-040` option is implied. `returns()`,
  `natal_conjunctions()` and `transit_view()` change only by the added fields.

**Negative controls.** A test rejects an event without provenance, and one whose provenance differs from the profile that
produced it. A test rejects a view whose `natal_provenance` is not the natal snapshot's.

**Not covered.** G1's M-06 (profile guarding on the event API) is not a §6 prerequisite, and is not added here.

## 3. M-09: The source sign inside the 1e-10 boundary window (decision required)

**Defect.** At longitude `29.99999999995`:
- D1 promotes the value to Taurus, because `zodiac_sign` applies the `BOUNDARY_TOLERANCE` convention at sign level.
- D3 and D9 derive from source sign Aries, because `classify` takes `int(lon // 30)` at
  `engine/astrology/varga_classifier.py:62`, and `navamsa_sign` does the same at `engine/astrology/navamsa_chart.py:60`.
  They then clamp to Aries's last division.
- So two facts that should share a parent sign do not. The certified sweeps step around this by probing at `+0.0007`
  (`scripts/certify_sign_convention.py:219`).
- **Corrected (`ADR-0112` s5):** version 1.0.0 said D9 and D10 disagree with themselves inside the window. They do not.
  At `29.99999999995`, `navamsa_longitude` is `269.99999999954997` (sign 8), consistent with `navamsa_sign`. D10 is
  consistent too. The earlier figure came from a probe that rounded to nine decimals.

**Affected only by inputs in `[30k - 1e-10, 30k)`.** That window is 0.36 micro-arcseconds wide, six orders of magnitude
below the certified ephemeris tolerance.

### Options

- **A. Promote the parent everywhere (recommended).** Varga layers take the source sign by the same tolerance rule as D1,
  and the degree is clamped at 0 at the start of the new sign. This applies `engine/astrology/longitude_utils.py`'s own
  stated convention hierarchically: a value within tolerance below a boundary belongs to the next division, and the sign is
  a division.
  - D1 does not change.
  - The varga, D9 and D10 outputs change, inside the window only.
- **B. Floor the parent everywhere.** D1 drops promotion at sign level.
  - This reverses the F-04 and A-3 remediation that the tolerance exists for: exact classical boundaries that floats
    undershoot would be misplaced again.
  - It changes D1, KP chain signs, drishti and yoga inputs, which is the largest certified blast radius.
- **C. Keep both conventions and declare the seam.**
  - No calculation changes. Each layer publishes its convention, and a gate pins the disagreement at the exact boundary.
  - The evidence layer would have to reconcile parents on every join, which is the very problem
    `EVIDENCE_INDEPENDENCE_DESIGN.md` s10 names.

**Recommendation: A.** It is the only option that removes the seam without reversing a remediation. Under
`Q8_CLOSURE_MATRIX.md` §14 it needs its own ADR and recertification.

### Certification impact of A

- **Code paths:** `classify` (registry vargas D2, D3, D7, D12, D20, D24, D30, D40 and D45, and standalone D4 and D16),
  `navamsa_sign` and `navamsa_longitude` (D9), `dashamsa_sign` and `dashamsa_longitude` (D10), and the chart builders over
  them.
- **Artifacts to regenerate:**
  - `current_engine` (its D9 and D10 validators)
  - `SIGN_CONVENTION_V1` (Gate A's ULP-adversarial sweep hashes, and Gate D)
  - all eleven `VARGA_*` artifacts
- **Constraint:** the independent validators and static references must be updated to the same rule independently, not
  copied from production.
- **Measurement:** the implementation must first count how many certified sweep, holdout and oracle points lie in the
  window. Any changed value outside the window is a failure.
- **PyJHora:** its behaviour at these points must be recorded as observed, not assumed.

**Negative controls.**
- A gate at the exact window, replacing the `+0.0007` avoidance, fails if D1 and any varga disagree on the parent.
- A test fails if a value outside the window changes.

## 4. Specification decisions still open (H0, H1, H2, H4, H5)

**Resolved, 2026-11-07.** Every item below is resolved, as `ADR-0113` s3 records item by item, and H0, H1, H2, H4 and H5
are promoted to `ACCEPTED` by `ADR-0113` s4. The text below is the record as it stood before that.

No specification is promoted here. Each stays `PROPOSED, C0 RESEARCH` until the owner ratifies it. Several items that
the specs record as "decided" rest on `ADR-0020` and `ADR-0021`, which stay `PROPOSED` and were not blanket-ratified.

| Spec | Open item | Current state | Owner action |
|---|---|---|---|
| H0 | Identifier family | Decided: `ADR-0111` (`ENT-00000001`) | None |
| H0 | Subject shape: specialised subject types | `ADR-0020` D1, `PROPOSED` | Ratify or replace |
| H0 | Competing charts: no silent selection | `ADR-0020` D3, `PROPOSED` | Ratify or replace |
| H0 | Entity vocabulary: five provisional kinds | `ADR-0021` D3, `PROPOSED` | Ratify or replace |
| H0 | Relationships as links | `ADR-0021` D4, `PROPOSED` | Ratify or replace |
| H1 | Identifier for event records | Open. Event *entities* are covered by `ENT`; life-event *records* are not stated | Decide |
| H1 | Event-class vocabulary | Open | Decide |
| H1 | Stored per person or per birth record | Open | Decide |
| H1 | Retention and privacy posture | Open, and a legal question | Decide, with advice |
| H2 | How the protected holdout is chosen | Open | Decide |
| H2 | Minimum sample size before confidence is reported | Open | Decide |
| H2 | Whether rejected hypotheses are shown to the user | Open | Decide |
| H4 | Identifier family for evidence items | Open | Decide |
| H4 | Strength: rule property, system property or both | Open | Decide |
| H4 | Evidence persisted or recomputed | Open. `DP-005` D-1 option C bears on it | Decide |
| H5 | Identifier family for rules | Open | Decide |
| H5 | Rules as data or code | `DP-005` D-3 | Decide in `DP-005` |
| H5 | Runtime variant selection, and dual-variant analysis | Open | Decide |

Every specification also carries a stale status header ("pending owner ratification (Q1)", though Q1 is ratified). That
should be corrected when each is ratified, and not before.

## 5. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-11-06 | Created under `ADR-0111`. Contracts and one recommendation; no implementation. |
| 1.2.0 | 2026-11-07 | Status updated: the contracts are implemented and s4 is resolved (`ADR-0113`). |
| 1.1.0 | 2026-11-06 | M-09's D9/D10 self-inconsistency claim corrected (`ADR-0112` s5). The owner selected M-09 option A and authorized all three contracts (`ADR-0112`). |
