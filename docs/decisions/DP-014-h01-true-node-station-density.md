<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-21 |
| Review cadence | TBD |

# DP-014. H-01 true-node station-density gap in `find_crossings()`

## 1. The question

`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-01, "`node_policy=\"true\"` produces silently
incomplete transit results," has no governing decision paper or ADR anywhere in the repository. Unlike
H-02 (`ADR-0020` D5), no prior decision-log entry contains H-01-specific analysis to extract - the only
existing analysis is the original audit finding itself, plus (new in this paper) a live re-verification
of that finding's numbers and a blast-radius trace across every `node_policy` consumer in the
repository. This paper extracts the audit's own finding and its own two proposed solutions into a
citable decision paper. It decides nothing, recommends nothing beyond the audit's own proposed
solutions, and is not implementation-authorized.

## 2. What is already established, and what is not - stated separately

**Established (by the original audit, re-verified live in this paper, not re-derived or altered):**
`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-01: `engine/transits/speeds.py` sizes the
transit-event search grid from a bound on **speed** (`grid_step_days(body) = MAX_MOTION_PER_STEP_DEG /
(MAX_SPEED_DEG_PER_DAY[body] * SAFETY_FACTOR)`), but `engine/transits/crossing.py`'s `find_crossings()`
correctness requires at most one station (speed-sign change / turning point) per grid interval - a
bound on **station spacing**, which nothing in the repository computes or enforces. Measured for the
true node: maximum speed 0.233 deg/day (within the declared 0.3 deg/day bound), but roughly sixteen
speed-sign changes per hundred days (~one station every 6.25 days) against a grid step of 37.5 days for
that body. A sixty-target, four-hundred-day sweep found four targets where production reported fewer
crossings than a fine scan, worst case one reported where three exist. `NODE_POLICY_TRUE` is defined
(`engine/astronomy/profile.py:29`) and reachable (`engine/transits/crossing.py`'s body resolution), so
this is a live, supported code path, not dead code - but no shipped profile selects it and no test
exercises it.

**Re-verified live for this paper (2026-08-21), against the current `e7adeb0` tree, unchanged since the
audit:**

- `engine/transits/speeds.py`: `MAX_SPEED_DEG_PER_DAY["TrueNode"] = 0.3`, `SAFETY_FACTOR = 4.0`,
  `MAX_MOTION_PER_STEP_DEG = 45.0`, giving `grid_step_days("TrueNode") = 45.0 / (0.3 * 4.0) = 37.5`
  days - identical to the audit's own figure. The defect is present in the live codebase today, not
  already fixed.
- `git log --oneline -- engine/transits/speeds.py` shows no commits since `8a5d56e` (a decision-log
  renumbering migration, not a substantive change) - the file predates and is untouched by this
  session's H-02 work.
- A repository-wide grep of `docs/DECISION_LOG.md` for "H-01" finds no ratified or proposed ADR item
  specific to H-01 (only the `Q8_CLOSURE_MATRIX.md` scope citation and two "does not extend to H-01"
  disclaimers in `ADR-0059`/`ADR-0061`'s consequence sections). Unlike H-02, there is no existing
  "D5-equivalent" written analysis anywhere in the ratified-or-proposed register to extract from - this
  paper's technical content is therefore drawn directly from the original audit and from fresh code
  inspection, not from a prior decision-log item.
- A repository-wide grep of `engine/tests/` for `NODE_POLICY_TRUE`, `node_policy.*true`, or `TrueNode`
  finds zero matches - no test anywhere exercises the true-node path. This re-confirms the audit's own
  "no test exercises it" claim is still accurate today.

**Not established (explicitly not decided by this paper):** which of the audit's two proposed
solutions, if either, should be implemented; any station-spacing bound for the true node or any other
body; whether TRANSIT_V1's completeness claim should be narrowed, or the true-node path repaired to
match it.

## A. Exact H-01 problem statement

`find_crossings()`'s correctness invariant is "at most one station per grid interval, so every
remaining piece is monotone" (per `engine/transits/crossing.py`'s own docstring). The grid is sized only
from a speed bound, which guarantees no more than 45 degrees of motion per sample - it does not, and by
construction cannot, guarantee no more than one turning point per sample. For bodies whose direction
changes frequently relative to their grid step (measured: true node, ~one station per 6.25 days against
a 37.5-day step), a single grid interval can contain multiple stations that the single speed-sign
bisection inside that interval cannot fully isolate, so some crossing events within that interval are
never found. The failure is silent: no error, no warning, no flag on the returned event list - the
function simply returns a materially incomplete answer for the affected profile/body combination.

## B. Why the issue exists

The grid-sizing logic (`engine/transits/speeds.py`) was designed around a speed bound because that is
what keeps the longitude-difference function well-behaved for bisection *within* a monotone piece. It
does not address how a monotone piece is identified in the first place: `find_crossings()` isolates
"at most one station per interval" by construction of that same grid, i.e. it treats grid interval
boundaries as station boundaries without ever verifying that assumption against actual station density.
The bound needed for that step - maximum station frequency, not maximum speed - was never derived or
encoded for any body. It happens not to matter for the two shipped profiles' bodies in practice (see
section E), which is presumably why it was not caught before this audit.

## C. Current implementation status

Live and unmodified since the audit. `NODE_POLICY_TRUE` is a defined, reachable enum value
(`engine/astronomy/profile.py:29`); `engine/transits/crossing.py` resolves it to the `TrueNode`
ephemeris body without any additional safeguard. No refusal, warning, or completeness caveat exists
anywhere on this path today. No decision paper or ADR has ever addressed it.

## D. Existing certified/locked scope affected

None of the FORMALLY LOCKED Tier-0 scope (`ADR-0005`/`ADR-0034`: the astronomical calculation kernel -
ephemeris handling, frame, calculation profiles, houses, sidereal positions, JD/time pipeline - and the
certified D9/D10 divisional mathematics) is implicated by H-01's specific defect mechanism. `node_policy`
is a field on `CalculationProfile` (Locked-adjacent), and the mean/true node ephemeris *position lookup*
itself (`engine/astronomy/sidereal_planets.py`) is part of Locked-scope "sidereal positions" - but that
lookup is a direct dictionary read with no search algorithm, and it already returns the correct
instantaneous position regardless of node policy (confirmed in section F). H-01's defect lives entirely
in `engine/transits/crossing.py`/`speeds.py`, which is TRANSIT_V1 territory (`ADR-0008`), not Tier-0
Locked scope. Fixing or gating H-01 under any option in section H would not require reopening the Locked
scope.

`TRANSIT_V1`'s own completeness claim is affected in the sense the audit states: "TRANSIT_V1's
completeness claim is scoped to mean-node bodies in practice while the code advertises a broader
contract." No certified numeric value changes merely by virtue of this gap existing - see section L.

## E. Existing evidence and tests

The only evidence is the original audit's sweep (sixty targets, four hundred days, four mismatches,
worst case one reported where three exist) and its measured true-node station rate (~sixteen per
hundred days) versus grid step (37.5 days), both re-confirmed live for this paper (section 2). No test
file in `engine/tests/` exercises `node_policy="true"` in any form - confirmed by direct grep, not
assumption. The audit's own hundred-target randomised sweep over the two shipped profiles (mean-node
only) found zero mismatches, which is the basis for "no published result is affected" in section F.
This paper does not re-run the sixty-target sweep itself: the audit's own reproduction is treated as
sufficient evidence for a decision-readiness paper, and re-running it would duplicate rather than
strengthen the existing measurement (the grid-step and speed-bound numbers that drive it are
independently re-verified in section 2 instead).

## F. Exact calculation paths affected

Traced live, not assumed, across every `node_policy` consumer in the repository (eight files):

- **Affected (search/root-finding, the actual defect mechanism):** `engine/transits/crossing.py`
  `find_crossings()`, and everything built on it - `engine/transits/events.py`'s `sign_ingresses()`,
  `nakshatra_ingresses()`, `returns()`, `natal_conjunctions()` - when invoked for a true-node body
  (Rahu/Ketu) under a hypothetical `node_policy="true"` profile.
- **Not affected (direct ephemeris lookup, no search):**
  `engine/astronomy/sidereal_planets.py`'s `sidereal_planet_collection()` does
  `sidereal["MeanNode" if node_policy == "mean" else "TrueNode"]` - a plain dict read, no grid or
  bisection involved. `engine/astronomy/planet_collection.py`'s `planet_collection()` similarly does
  `planets["Rahu"] = planets[rahu_source]` where `rahu_source` is chosen by a string comparison, again
  no search. Ordinary chart/position calculation (natal Rahu/Ketu longitude, houses) is unaffected by
  H-01's mechanism regardless of node policy.
- **Not affected (metadata/provenance only):** `engine/astronomy/astronomy_snapshot.py` passes
  `node_policy` through to the two lookups above and records it on `Provenance`; `engine/models/
  provenance.py`'s `Provenance.node_policy: str` is a plain metadata field; `scripts/
  certify_current_engine.py` records it in provenance output only.
- **Explicitly refused already:** `engine/kp/chart.py:51` raises `KpProfileError("KP requires the mean
  node (Decision KP-B)")` whenever `provenance.node_policy != NODE_POLICY_MEAN` - the KP module already
  hard-gates true-node out entirely, independent of anything this paper decides.
- **Shipped profiles:** both `PARASHARI_LAHIRI` and `KP_KRISHNAMURTI` (`engine/astronomy/profile.py`)
  select `NODE_POLICY_MEAN` only. No shipped profile reaches the affected path today.

## G. Classification

A **calculation defect** in `find_crossings()`'s implicit assumption (station spacing not bounded,
though the code's docstring asserts it is handled), combined with a **certification gap** (TRANSIT_V1's
completeness claim is not scoped to exclude the true-node path it does not actually support). It is not
a missing implementation (`NODE_POLICY_TRUE` is fully implemented and reachable) and not a convention
decision (no naming/labelling ambiguity is involved, unlike H-02).

## H. Options

The audit itself proposes exactly two solutions and explicitly warns against a third ("do not simply
shrink the step: the correct invariant needs stating, not tightening by guess"). This paper adds one
further option (defer) consistent with `DP-012`'s precedent, given no shipped profile currently reaches
the affected path. No other option is presented, per the task's explicit "do not invent a convention."

### Option 1 - Bound station spacing per body explicitly, and re-size the grid from that bound (audit's first proposed solution)

Derive a genuine, defensible maximum station-frequency bound for the true node (and confirm/derive one
for every other body sharing the grid-sizing path), then re-derive `grid_step_days()` so it also
satisfies "at most one station per interval," not only "under 45 degrees of motion per interval." This
would make true-node event-finding actually match TRANSIT_V1's advertised contract.

- **Advantages:** the only option that produces a genuinely complete, certifiable true-node transit
  search; closes the gap TRANSIT_V1 currently advertises but does not deliver.
- **Disadvantages:** requires real astronomical/algorithmic research to establish a station-frequency
  bound with the same rigor `MAX_SPEED_DEG_PER_DAY` itself required (that bound is presumed
  empirically-derived-with-margin, not a closed-form constant) - the audit's own measured "sixteen per
  hundred days" is one observed window, not yet a proven worst case. An under-justified bound would
  itself be a new, unaudited claim. Highest implementation cost of the three options.
- **Certification implications:** requires a TRANSIT_V1 recertification addendum - a new completeness
  gate for the true-node path (station-density test per body, completeness comparison against a fine
  scan), per the audit's own "tests required."
- **Blast radius:** `engine/transits/speeds.py`'s grid-step formula for `TrueNode` specifically (and any
  other body found to need a station-spacing bound); `MeanNode` and all currently-exercised bodies
  unaffected if their existing speed bounds already happen to satisfy a station-spacing bound (not yet
  verified either way for bodies other than TrueNode).
- **Certified-value impact:** none for any currently-shipped profile (neither selects true-node); would
  newly define TrueNode transit-search behavior that does not exist in certified form today.

### Option 2 - Gate the true-node path behind an explicit refusal until certified (audit's second proposed solution)

Have `find_crossings()` (or its callers) raise an explicit, structured error when invoked with a
true-node body, converting today's silent incompleteness into a loud refusal - consistent with this
repository's existing "never silently wrong, structured refusal" pattern (e.g. `RiseSetStatus.NO_RISE`/
`NO_SET`, `TrikalamStatus.INDETERMINATE`).

- **Advantages:** small, low-risk change; requires no new astronomical research or station-frequency
  bound; converts a real defect into an honest, documented limitation immediately; matches the KP
  module's own precedent (`engine/kp/chart.py:51` already refuses true node outright).
- **Disadvantages:** does not make true-node transit search actually work; a future consumer that
  legitimately needs true-node transits would still need Option 1's work eventually.
- **Certification implications:** smallest of the three - a narrow TRANSIT_V1 addendum (a refusal test,
  per the audit's own "tests required... a refusal test if the path is gated"), arguably not even
  requiring a new Gate, just a documented behavior change plus a test.
- **Blast radius:** `engine/transits/crossing.py`'s body-resolution step only; a guard clause, not an
  algorithm change.
- **Certified-value impact:** none. No currently-shipped profile reaches this path, so no existing
  result changes; the change only affects a currently-silent-wrong path, converting it to an explicit
  error.

### Option 3 - Defer entirely; document the gap, no code change

Leave the code as-is. Optionally update TRANSIT_V1's own `explicit_non_claims` (or equivalent
documentation) to state plainly that true-node completeness is not certified, mirroring how the gap is
already documented in the audit and in `Q8_CLOSURE_MATRIX.md`. No shipped profile reaches the affected
path today, so nothing currently certified is incomplete in practice.

- **Advantages:** zero implementation cost, zero regression risk; consistent with `DP-012`'s own
  precedent (Option C, "deferred entirely until a consuming feature needs it").
- **Disadvantages:** the reachable, silently-incomplete code path (`NODE_POLICY_TRUE`) remains exactly
  as it is today - callable and silently wrong if any future code ever does select it, with nothing in
  the code itself to stop that.
- **Certification implications:** none required beyond an optional documentation note.
- **Blast radius:** none - no code touched.
- **Certified-value impact:** none.

## I / J / K / L

Advantages/disadvantages, certification implications, blast radius, and certified-value impact are
stated inline under each option in section H, per the audit's own level of analysis - this paper does
not add speculative detail beyond what the audit and the fresh code trace in sections D-F support.

## M. Recommendation

No option is unambiguously compelled by the evidence the way, for example, H-02's fix Option 1 was
(additive-only, zero consumers, zero risk). Between the three:

Option 2 (explicit refusal) is the most tractable near-term step: it requires no new astronomical
research, carries the lowest implementation and certification cost of the two audit-proposed solutions,
and follows a pattern this repository already applies elsewhere (KP's own existing true-node refusal,
`RiseSetStatus`/`TrikalamStatus`'s structured-refusal precedent) rather than inventing a new one. It
converts a real, reachable, silent defect into an honest, tested limitation without requiring an
under-justified station-frequency bound. Option 1 remains the eventual complete fix if and when a
consuming feature genuinely needs true-node transit search, but should not be attempted until that
bound can be derived with real rigor, not guessed. Option 3 is a legitimate zero-cost alternative if the
owner judges even Option 2's small change unnecessary while nothing consumes the path.

**Confidence: medium.** This is a closer call than most recent fix-option recommendations in this
project's history: unlike H-02 (where the fix was additive and risk-free), all three options here carry
a real trade-off, and reasonable owners could prefer Option 3 (true zero-cost deferral, matching
`DP-012`'s precedent) over Option 2 (a small but real code change to a path nothing currently uses).

## N. What is NOT being decided by this paper

This paper does not decide: which option (1, 2, or 3) is adopted; any station-spacing bound for any
body; any change to `engine/transits/crossing.py`, `engine/transits/speeds.py`, or any test file; any
change to TRANSIT_V1's certification artifacts or documented claims; whether H-01 blocks or does not
block any future Jataka/engine work. It does not ratify `ADR-0020`, `Q8_CLOSURE_MATRIX.md`, or any other
document it cites. It is not implementation-authorization for any option, including the one it
recommends.

## O. Exact CEO/owner decision required

The owner must select one of: Option 1 (derive a station-spacing bound and repair `find_crossings()` for
the true node), Option 2 (gate the true-node path behind an explicit refusal), or Option 3 (defer,
optionally with a documentation-only note). That selection, recorded as a new, numbered decision-log
entry citing this paper, is what would authorize any subsequent implementation work - this paper alone
does not.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-21 | Created. Extracts `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` finding H-01, re-verifies its figures live against `e7adeb0`, and traces the exact blast radius across all eight `node_policy` consumers. Options only; decides nothing; not implementation-authorized. |
