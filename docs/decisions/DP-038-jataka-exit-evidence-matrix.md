<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents an evidence matrix and unresolved questions. **DECIDES NOTHING.** Requires owner approval. **This paper does NOT declare, perform, or recommend JATAKA phase exit**, which remains on hold pending a separate owner decision. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-18 |
| Review cadence | TBD |

# DP-038. JATAKA phase-exit evidence matrix and M2 record reconciliation

Written under the owner's "CEO AUTHORIZATION — PROCEED WITH M2" and "CEO DECISION —
M2 SCOPE CONFIRMED" instructions. `DP-038`'s identifier was allocated in `docs/decisions/README.md` before this paper's substantive
content was written, per `ADR-0040`. **That ordering is not independently proven by the commit
graph:** the index row and this paper were committed together in `5be71a2`, so the repository
evidences only that both exist, not the sequence in which they were produced. `DP-037`, by
contrast, was allocated in `d47ad63` and drafted in `f9bf3c2`, where the graph does prove it. Reconstructed against `main` at
`b92cd5ff422cebecb395b5846614c96a7c23a5e0`.

**Nothing in this paper resolves any ambiguity by inference.** For every open item
it states the evidence, the competing interpretations, the consequence for JATAKA
exit, and the decision still required.

---

## 1. The exit criterion, verbatim

`docs/Q8_CLOSURE_MATRIX.md` s5:

> | Exit criteria | Every capability declared a production analytical input is individually certified. No capability is in use that a certification artifact does not cover. |

s14, applying to every phase:

> Every phase's completion report states what it could not verify.

s5's approval row: **"Entry, per capability, exit."**

---

## 2. Evidence matrix

### Clause 1 - "every capability declared a production analytical input is individually certified"

| Declared input | Artifact | Verdict at `b92cd5ff` |
|---|---|---|
| 9 registry vargas `[2,3,7,12,20,24,30,40,45]` | `VARGA_D*_V1_certification.json` | 9/9 **PASS** |
| D1 / D9 / D10, dedicated modules | `current_engine` + varga artifacts | **PASS** |
| 11 `certified_capabilities` in the machine-checked block | their own artifacts | 11/11 **PASS** |

**Every declared input holds a PASS artifact.** Clause 1 is met *on the face of the
artifacts*, and is qualified by sections 3.2 and 3.3 below.

### Clause 2 - "no capability is in use that a certification artifact does not cover"

| Item | Finding | Status |
|---|---|---|
| `returns()` | see 3.1 | **AMBIGUOUS** |
| D16 / D4 | certified, unregistered, dispatcher raises `UnsupportedVargaError` - not in use | not a clause-2 item |
| `planet_strength()` | raises `NotImplementedError` by design - not in use | not a clause-2 item |
| `engine/api/`, `engine/main.py` | empty package; 60-line demo that "performs no astrology itself" | not analytical inputs |

### s14 completion report

See 3.5. **No JATAKA completion report exists.**

---

## 3. The seven open items

None of the following is treated as resolved merely because it is documented.

### 3.1 `returns()` coverage

**Evidence.** `engine/transits/events.py` L65 defines `returns()` as a thin
delegator: it calls `find_crossings(body, natal_longitude, jd_start, jd_end,
profile, kind="return")` and adds no arithmetic of its own. `kind` does not branch
the search - `engine/transits/crossing.py` uses it only at L178, passing it into
the emitted event, and at L196 for `kind="tangent"`. `returns()` has **zero
production callers**: the only references are in `engine/tests/test_transit_events.py`
(L66, L129). `engine/transits/__init__.py` is docstring-only and exports nothing.
`TRANSIT_V1`'s `scope` string names "returns", but no gate block exercises it - the
gates are `A_residual_battery` (74 events, max residual 2.11e-05 arcsec),
`C_oracle_anchors`, `D_independent_validator`, `E_declared_division` - and
`validate_transits_holdout.py` contains **zero** occurrences of the word.
`Q8_CLOSURE_MATRIX.md` s9 states verbatim: *"Solar return certified, since
`returns()` exists but is in no certification artifact."*

**Competing interpretations.**
*(a) Covered.* The computation is `find_crossings`, which gates A/C/D/E exercise
directly. `kind="return"` is a label, not an algorithm. A wrapper that adds nothing
inherits the certification of what it wraps.
*(b) Not covered.* No gate exercises the natal-longitude-as-target usage or the
`kind="return"` labelling path, no validator mentions it, and the roadmap's own
text says it is in no artifact. "Covered" under reading (a) is an inference about
delegation, not an executed check.

**Consequence for JATAKA exit.** Under (a), clause 2 is met. Under (b), clause 2 is
**unmet** and exit requires either a gate covering `returns()`, or an explicit
owner finding that a zero-caller wrapper is not "in use".

**Decision required.** Which reading governs; and if (b), whether to gate
`returns()` or to record it as not-in-use. Either path is its own authorization.

### 3.2 The ADR-0083 / ADR-0085 / ADR-0086 certification-integrity qualifications

**Evidence.** Three **ACCEPTED** entries qualify capabilities that hold PASS
artifacts. `ADR-0086` (`PARASHARI_YOGA_V1`) states that `ADR-0081`'s "PASS on all
ten gates (A-I)" *"must not be represented, or relied upon, as proof that
`graha_mahapurusha_from_snapshot()`'s own composition/plumbing is independently
verified for `house_number`/`sign_number` - it is not"*, and records that this
*"mirror[s] exactly the qualification `ADR-0085` established for `VARGA_D45_V1` and
`ADR-0083` established for D24's Gate C"*. `ADR-0086` also carries a remediation
design that is **design only**: ratifying it *"does NOT authorize its
implementation."*

**Competing interpretations.**
*(a) Still certified.* Each capability has a PASS artifact from a real run. The
qualification narrows what the artifact proves; it does not withdraw certification.
Clause 1 asks whether each is "individually certified", and each is.
*(b) Not fully certified.* A ratified entry saying a named layer is **not**
independently verified means that capability's certification does not cover part of
what it serves in production. Exiting a phase on artifacts carrying standing,
owner-ratified qualifications asserts more than the evidence supports.

**Consequence for JATAKA exit.** Under (a), no effect. Under (b), at least three
production capabilities - `PARASHARI_YOGA_V1`, `VARGA_D45_V1` and D24 - fail clause
1 until their qualifications are discharged, each requiring its own authorization.

**Decision required.** Whether a ratified integrity qualification is compatible with
"individually certified" for phase-exit purposes. **This is `N1`.**

### 3.3 ADR-0086 s2's unaudited negative-control residual

**Evidence.** `ADR-0086` s2 records, as an explicitly out-of-scope residual: the
same structural pattern - *"an in-process synthetic negative-control gate that never
monkeypatches the real production function"* - is present in **every other certified
capability's own negative-control gate**, naming D2/D3/D7/D12/D30, `TRANSIT_V1`,
`VIMSHOTTARI_V1`, `PANCHANGA_V1`, `TRIKALAM_V1`, `PARASHARI_DRISHTI_V1`,
`RISE_SET_V1`, `SIGN_CONVENTION_V1`, `KP_CHAIN_V1` and Tier-0/`current_engine`,
*"none of which this entry, the prior investigation, or `ADR-0085` examined"*, and
which is *"neither confirmed defective nor cleared"*.

**Relevance.** This is the same defect class M1 addressed for H-03 (a tolerance
derived from the quantity it bounded) and Q22/H-7a (a gate comparing a function's
output to itself). M1's own controls deliberately mutated the real production
function - `_render` in a worktree, an injected longitude bias through the real
position pipeline - because in-process synthetic controls cannot reach that class.
M1 did **not** audit the fourteen gates named above.

**Competing interpretations.**
*(a) Does not bear on exit.* It is unquantified and unconfirmed. Treating an
unexamined risk as a blocker would make phase exit unreachable in principle.
*(b) Bears directly on clause 1.* "Individually certified" is weakened if a
capability's negative control cannot fail for the defect it exists to catch, and the
register already records that this may be true of essentially the whole certified
surface.

**Consequence for JATAKA exit.** Under (a), none. Under (b), clause 1 cannot be
assessed for any capability until the residual is audited - a substantial
investigation in its own right.

**Decision required.** Whether to commission that audit before or after exit, or to
accept the residual explicitly. **This is `N2`.**

### 3.4 "declared" and "in use" are undefined

**Evidence.** The phrase "production analytical input" occurs three times across all
governing documents - `Q8_CLOSURE_MATRIX.md` s5, `VARGA_CERTIFICATION_ROADMAP.md`
L25, and `DECISION_LOG.md` L8156 (D20's consequences) - and is **defined nowhere**.
Neither "declared" nor "in use" is defined in `PROJECT_CONSTITUTION.md`,
`VALIDATION_STANDARD.md`, `ADR-0017` or elsewhere.

**Competing interpretations.** *"Declared"* could mean: the `ENGINE_STATUS.md`
capability block (machine-checked, but it postdates `Q8` and no document ties the
two); or `CERTIFIED_PRODUCTION_VARGAS` plus the certified-capability list; or any
capability an ADR calls a production analytical input. *"In use"* could mean:
importable and exercised anywhere; reachable from a production entry point; or
reachable from a consumer outside `engine/`. The three readings of "in use" give
different answers for `returns()` (3.1).

**Consequence for JATAKA exit.** The criterion cannot be evaluated deterministically
without a definition. Any exit finding would rest on a builder's reading of an
undefined term.

**Decision required.** Adopt operational definitions and name their normative
authority - most plausibly a new ADR, since `Q8_CLOSURE_MATRIX.md` is itself
ratified and should not be silently reinterpreted.

### 3.5 Does s14 require a JATAKA completion report?

**Evidence.** s14: *"Every phase's completion report states what it could not
verify."* No JATAKA completion report exists. The only `*COMPLETION*` artifact in
`reports/` is `G6_COMPLETION_RECORD.md`, a Phase-G item. **FOUNDATION exited via
`ADR-0068`, a readiness-audit ADR, not a completion report.** `ADR-0068` does state
deferrals and non-certifications - *"deferred, not certified"*, *"explicitly not
certified"* - so it arguably discharges s14 in substance.

**Competing interpretations.**
*(a) No separate artifact required.* FOUNDATION's precedent is a readiness-audit
ADR that names what was deferred; JATAKA can follow it.
*(b) A completion report is required.* s14 says "completion report", not "readiness
audit", and the two are different artifacts serving different purposes: one records
readiness to leave, the other records what the phase could not verify.

**Consequence for JATAKA exit.** Under (b), a completion report is a prerequisite
that does not yet exist.

**Decision required.** Whether the FOUNDATION precedent governs, or whether s14
requires a distinct artifact.

### 3.6 ADR-0004: procedural or normative?

**Evidence.** `ADR-0004` is PROPOSED. `NEW_VARGA_IMPLEMENTATION_TEMPLATE.md` - which
`Q8` s5 names as JATAKA's certification gate - cites it exactly once, at L24:
*"Obtain the ADR number from `docs/DECISION_LOG.md` before implementation, per
ADR-0004."*

**Competing interpretations.**
*(a) Procedural.* It governs identifier allocation. No certification result depends
on it; a varga certified under a correctly-allocated number is unaffected by its
ratification status.
*(b) Normative and load-bearing.* It is cited by a document `Q8` designates as the
phase's certification gate, so an unratified dependency sits inside the gate chain.

**Consequence for JATAKA exit.** Under (a), none. Under (b), the gate chain contains
an unratified normative dependency.

**Decision required.** Its bucket placement, and whether ratification is a
precondition for exit.

### 3.7 ADR-0018 and evidential standing

**Evidence.** `ADR-0018` (CI tiering and oracle environment reproducibility) has been
PROPOSED since 2026-08-10, *"pending owner ratification (Q1)"*, and is cited 21
times in the register. Every current certification claim - including every genuine
oracle result M1 produced - rests on CI evidence the entry governs. `Q25` already
annotates its `CEO_REPORTED` addendum with null `run_url`/`run_id`. The JATAKA exit
criterion cites no ADR.

**Competing interpretations.**
*(a) Does not block exit.* The criterion speaks only of capabilities and artifacts.
The CI apparatus demonstrably works; its governing entry being unratified is
governance debt, not an evidence defect.
*(b) Affects evidential standing.* If the decision governing how certification
evidence is produced is not owner-ratified, then the standing of every artifact
produced under it is, strictly, proposed rather than accepted.

**Consequence for JATAKA exit.** Under (a), none. Under (b), exit would rest on
evidence whose governing decision the owner has never accepted.

**Decision required.** Whether `ADR-0018` belongs in the blocking bucket.

---

## 4. Unresolved questions bearing on exit

| # | Question |
|---|---|
| N1 | Is a capability carrying a ratified certification-integrity qualification (`ADR-0083`/`0085`/`0086`) "individually certified" for exit purposes? |
| N2 | Does `ADR-0086` s2's unaudited negative-control residual across ~14 capabilities bear on clause 1, and must it be audited before exit? |
| N3 | Which reading of `returns()` governs (3.1)? |
| N4 | What are the operational definitions of "declared" and "in use", and under whose authority (3.4)? |
| N5 | Does s14 require a distinct JATAKA completion report (3.5)? |
| N6 | Is `ADR-0004` a blocking dependency (3.6)? |
| N7 | Does `ADR-0018` block exit, or is it governance debt (3.7)? |

`Q26` and `Q27`, created by the M2 Option-C split, are tracked in
`docs/OPEN_QUESTIONS.md` and are **not** JATAKA-exit blockers: both concern
evidence-presentation and trust-anchoring limitations that are explicitly recorded
and controlled.

---

## 5. What M2 corrected in the record

Five factually false statements, and nothing else:

| # | File | Correction |
|---|---|---|
| M1 | `ENGINE_STATUS.md` s2 | D16/D4 "neither is wired into CI" - false since `ADR-0096`; both are wired and hold genuine oracle agreement |
| M2 | `ENGINE_STATUS.md` s3 | "eleven served / eight registered" -> twelve / nine |
| M3 | `ENGINE_STATUS.md` s1 | "21 registered validator sources" -> 22. The adjacent certifier count was **not** touched: it became correct when M-4 took 23 -> 22 |
| M4 | `OPEN_QUESTIONS.md` `Q24` | premise "read by nothing" superseded by `12d3b5c`; status -> RESOLVED IN PART; residual split to `Q27` |
| M5 | `OPEN_QUESTIONS.md` `Q22` | status -> RESOLVED IN PART, H-7a recorded with its negative-control evidence; H-7b split to `Q26` |

One further correction was made and is disclosed as a deviation: the
`OPEN_QUESTIONS.md` status header read *"Twenty-five questions"*, which the
authorized creation of `Q26`/`Q27` made false. It now reads twenty-seven.

*Superseded, appended 2026-09-18:* the sentence "No other header field was altered" was true
of commit `5be71a2`, which this section described. It was superseded by `ab26e084`, a separately
authorized metadata correction that updated the `Version` and `Last updated` fields of both
`docs/ENGINE_STATUS.md` and `docs/OPEN_QUESTIONS.md`. The original sentence is preserved above
rather than rewritten, so the record shows what was claimed and when it ceased to be true.

---

## 6. What this paper does not do

It does not decide. **It does not declare, perform, or recommend JATAKA phase exit**,
which remains on hold. It resolves none of N1-N7 by inference. It changes no
production code, certification logic, holdout datum, artifact, registry, CI gate or
test, and ratifies no ADR.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-18 | Created under the owner's "CEO AUTHORIZATION — PROCEED WITH M2" and "CEO DECISION — M2 SCOPE CONFIRMED" instructions. Identifier allocated before the paper's substantive content was written, per `ADR-0040`; index row and paper committed together in `5be71a2`, so the commit graph does not independently prove that ordering. Carries the JATAKA-exit evidence matrix, the seven commissioned investigation findings each with evidence, competing interpretations, exit consequence and the decision still required, and unresolved questions N1-N7. Records the M2 record corrections. Declares no phase exit. |
