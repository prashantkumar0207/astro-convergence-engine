<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents evidence and unresolved semantic choices for `ADR-0099` s4. **DECIDES NOTHING.** Requires owner adjudication. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-22 |
| Review cadence | TBD |

# DP-039. Executable semantics for `ADR-0099` s4 SCOPE OVERCLAIM, the prerequisite for the C3 gate

Written under the owner's "CEO AUTHORIZATION - NEXT GOVERNANCE PREREQUISITE" instruction, which
directed governance analysis and drafting only and expressly forbade implementing `C2`-`C5`.
`DP-039`'s identifier was allocated in `docs/decisions/README.md` before this paper's substantive
content was written, per `ADR-0040`. **That ordering is not independently proven by the commit
graph:** the index row and this paper were committed together, so the repository evidences only that
both exist, not the sequence in which they were produced. Measured against `main` at
`f8f1360716885955130fb78bba6cfe3f3302a8b9`.

**Nothing in this paper resolves any ambiguity by inference.** It states what the repository
evidences, separates what follows from that evidence from what does not, and for every genuine
semantic choice it presents the options and their consequences without selecting one.

**A note on the referring instruction.** The authorization refers to "the trigger terms / executable
semantics in `DP-038` s4". `DP-038` s4 is the `N1`-`N7` unresolved-questions register and contains no
trigger terms. The terms that gate `C3` are in **`ADR-0099` s4** (`docs/DECISION_LOG.md` L8768-L8790),
the ratified SCOPE OVERCLAIM obligation. This paper addresses `ADR-0099` s4. The discrepancy is
recorded rather than silently reinterpreted.

---

## 1. The wording under examination

`ADR-0099` s4, ACCEPTED, `docs/DECISION_LOG.md` L8770-L8774, verbatim:

> A capability named in a certification artifact's `scope` but exercised by **no gate** in that artifact
> is a **SCOPE OVERCLAIM**. Every such capability must either:
>
> - **(a)** be exercised by at least one gate in that artifact; or
> - **(b)** appear in a declared `scope_not_gated` array in that artifact, with a per-item reason.

`ADR-0099` s7 (L8820-L8823) describes the gate that would enforce it:

> **C3.** Add a scope-coverage gate asserting that every capability named in an artifact's `scope` is
> either exercised by a gate or listed in `scope_not_gated` with a reason. Modelled on
> `SIGN_CONVENTION_V1`'s existing `declaration_registry` / `function_registry` completeness pattern,
> which this repository has already ratified and operated.

`ADR-0100` s1 (ACCEPTED) qualifies only s4's **authority**, not its terms: the obligation is
established by `ADR-0099` itself, with `docs/VALIDATION_STANDARD.md` a subject-matter reference only.
Neither entry defines the trigger terms. **Neither is edited by this paper.**

---

## 2. Measured state of the certification corpus

Every figure below was measured against `main` at `f8f1360716885955130fb78bba6cfe3f3302a8b9`.

| Measurement | Value |
|---|---|
| Certification artifacts in `certification/` | 26 |
| Artifacts carrying a non-empty `scope` | **22** |
| Artifacts carrying a `scope_not_gated` array | **0** |
| Distinct `schema` values across the 26 artifacts | **26** - every artifact has its own bespoke schema |
| Distinct gate-block keys across the corpus | 167 |
| Gate-block keys recording which code objects a gate exercised | **none that is universal** |
| Artifacts carrying `explicit_non_claims` | 22 |

**`scope` is free prose.** `TRANSIT_V1`'s reads: *"longitude-crossing primitive; sign/nakshatra
ingresses (with declared_division, H-02 fix Option 1, ADR-0065); returns; natal conjunctions;
natal-relative view"*. It contains no identifiers, no delimiter contract, and no mapping to code.

**Gate blocks record measurements, not coverage.** `TRANSIT_V1`'s four gates carry
`events` / `max_residual_arcsec` / `bound_arcsec`, `anchors` / `worst_delta_over_tolerance` /
`worst_astronomy_delta_arcsec` / `worst_aberration_residual_arcsec`, `result`, and
`cases_checked` / `negative_control_verified`. **No gate in any artifact carries a list of the
callables it exercised.**

**The four per-gate identifier keys that do exist are mutually inconsistent**, which is itself
evidence that no convention exists:

| Artifact | Gate | Key | Value |
|---|---|---|---|
| `KP_SIGNIFICATOR_V1` | `D_non_invasiveness` | `production_module` | `engine.kp.significators` - dotted module path |
| `PARASHARI_YOGA_V1` | `D_non_invasiveness` | `production_module` | `engine/parashari/mahapurusha_yoga.py` - **file path, same key name** |
| `VARGA_D16_V1` | `C_oracle` | `function` | `shodasamsa_chart(chart_method=1, Traditional Parasara)` - prose, and it names the **external PyJHora** function, not the engine's |
| `KP_SIGNIFICATOR_V1` | `G_node_aspect_cases` | `levels_exercised` | `['conjunction', 'aspect', 'sign_lord_fallback', ...]` - domain labels, not code identifiers |

---

## 3. What follows from the evidence

**Finding 3.1 - neither limb of s4's trigger is presently evaluable.**

- *"a capability **named** in a certification artifact's `scope`"* - `scope` is prose. Deciding which
  substrings denote capabilities requires a rule that does not exist. A word-level proxy run over the
  corpus flags **all 22** scope-bearing artifacts, including on ordinary English words such as
  "given" and "first", which demonstrates that an unbounded trigger matches indiscriminately rather
  than that 22 overclaims exist.
- *"exercised by **no gate** in that artifact"* - no artifact records what its gates exercised, so
  non-exercise cannot be read from the artifact at all.

**Finding 3.2 - s4's own worked example was decided by human reading.** The three `TRANSIT_V1`
instances were identified (L8782-L8785) because the four gate names and blocks *"mention none of
'return', 'conjunction', 'natal-relative' or 'view'"*. That is absence-of-words in prose. It reached
the correct answer; it is not a procedure a gate can execute, and it is not stated as a rule.

**Finding 3.3 - `C3` cannot be specified against the current artifact schema.** `C3` is described as
an assertion over "every capability named in an artifact's `scope`". Given 3.1, there is no
deterministic input to assert over. **This is a prerequisite, not an implementation difficulty:** no
amount of care in writing `C3` supplies the missing substrate.

**Finding 3.4 - the repository already holds one rigorous precedent, and one weaker one.**

- **Rigorous.** `SIGN_CONVENTION_V1` carries `declaration_registry` (20 entries) and
  `function_registry` (6 entries), both **dicts keyed by stable dotted identifiers** -
  `engine.astrology.signs.zodiac_sign`, `Chart.sign_map`. This is the pattern `ADR-0099` s7 names for
  `C3`, and it is enumerated and machine-checkable. **It should be reused, not duplicated.**
- **Weaker.** `explicit_non_claims`, present in 22 artifacts, is the repository's declared-exclusion
  precedent and is the closest existing analogue to s4's `scope_not_gated`. But its values are prose
  strings - *"Four Step Theory (Gondhalekar) - out of scope (ADR-0027 Decision 3)"* - so it supplies
  the **form** of a declared exclusion with a reason, and not machine-checkable membership.

**Finding 3.5 - `docs/NAMING_STANDARD.md` s2's ID-family table has no family for code capabilities.**
Its families cover questions, domains, events, outcomes, test scenarios, `ADR` and `DP`. Its s3 slug
convention is for the HLKG knowledge layer, not for callables. There is therefore no naming rule to
inherit, only the `function_registry` shape.

**Finding 3.6 - `docs/VALIDATION_STANDARD.md` supplies no definition either.** Its s2 eight
non-negotiable rules cover independence, holdouts, fallback, reproducibility, skips, anti-fitting,
boundary testing and stored results. None defines capability identity or gate coverage. Consistent
with `ADR-0100` s1, it is a subject-matter reference here and not a source of authority.

---

## 4. The genuine semantic choices requiring owner adjudication

Three. None can be derived from repository evidence; each has materially different consequences.
**This paper selects none of them, and deliberately offers no recommendation**, following the owner's
standing instruction not to select definitions on their behalf.

### Choice 1 - how a capability is identified for s4's purposes

| Option | Definition | Consequences |
|---|---|---|
| **1-A. Declared enumeration** | Each artifact gains a machine-readable array of capability identifiers - the `function_registry` shape, dotted paths - authored alongside its `scope` prose. `scope` stays prose and becomes non-normative for s4. | Directly reuses the ratified precedent `ADR-0099` s7 names. Requires an enumeration for each of the 22 artifacts, authored by someone. The enumeration's own completeness is not itself checkable against prose. |
| **1-B. Parse the `scope` string** | Define a delimiter and token grammar for `scope`, making the existing prose the normative source. | No new per-artifact authoring. But requires rewriting 22 free-text `scope` strings to conform, and any grammar will mis-parse parentheticals such as `TRANSIT_V1`'s "(with declared_division, H-02 fix Option 1, ADR-0065)". |
| **1-C. Code-anchored** | A capability is a public callable of the module(s) the artifact certifies; `scope` prose is disregarded entirely. | Fully mechanical, no authoring. But it decides coverage for callables the artifact never claimed, and it has no way to express a claim such as "natal-relative view" that spans several callables. |

### Choice 2 - how "exercised by a gate" is evidenced

| Option | Definition | Consequences |
|---|---|---|
| **2-A. Gates declare what they exercise** | Every gate block gains an `exercises` array of capability identifiers, written by the certifier that produced it. | Evidence is produced by the run that exercised the code, which matches this repository's "evidence over narrative" rule. Touches the gate schema of all 26 artifacts and regenerates every one of them. |
| **2-B. Artifact-level coverage map** | One `scope_coverage` object per artifact mapping each capability identifier to the gate name(s) covering it. | Smaller schema change; one block per artifact rather than a key in every gate. But the mapping is authored, not observed, so it can drift from what the gates actually do. |
| **2-C. Observed coverage** | Coverage is measured at certification time by instrumenting the run. | Cannot drift - it records what executed. Heaviest to build, and it measures execution, which is not the same claim as "this gate tests this capability". |

### Choice 3 - retrospective scope

| Option | Definition | Consequences |
|---|---|---|
| **3-A. Immediate and universal** | `C3` applies to all 22 scope-bearing artifacts as soon as it exists. | One consistent rule. Every artifact must be enumerated and regenerated before `C3` can pass; until then the gate fails the whole corpus. |
| **3-B. Forward-only** | `C3` applies to artifacts certified or regenerated after its introduction; existing artifacts are grandfathered until they are next regenerated. | `C3` can land without a corpus-wide migration. Leaves a period in which the obligation is in force but unenforced for most artifacts, which is the state that exists today. |
| **3-C. Declared backlog** | `C3` applies universally, but artifacts not yet enumerated are listed in a committed backlog with a per-item reason, in the `explicit_non_claims` idiom. | Makes the gap explicit and countable rather than silent, and reuses an existing precedent. Adds a second exclusion mechanism alongside `scope_not_gated`, which risks confusion between "not gated" and "not yet enumerated". |

---

## 5. Normative versus executable, stated separately

The owner's instruction requires these be distinguished. As of `f8f13607`:

- **Normative, and already in force.** `ADR-0099` s4 as ratified: a capability named in an artifact's
  `scope` but exercised by no gate is a SCOPE OVERCLAIM and must be gated or declared in
  `scope_not_gated` with a per-item reason. This obligation binds today. **Nothing in this paper
  changes it.**
- **Executable, and not yet established.** No procedure exists by which a gate can decide either limb
  of that trigger. Choices 1, 2 and 3 are exactly what is missing.
- **Unresolved.** Choices 1, 2 and 3, and consequently the specification of `C3`.
- **Not authorized by this paper.** `C2`, `C3`, `C4`, `C5`; any change to a certification artifact,
  schema, registry, gate, test or CI job; disposition of the three `TRANSIT_V1` scope overclaims; any
  JATAKA phase-exit work.

---

## 6. Relationship to the three open `TRANSIT_V1` overclaims

`returns()` (`engine/transits/events.py` L65), `natal_conjunctions()` (L79) and `transit_view()`
(`engine/transits/view.py` L47) remain **open SCOPE OVERCLAIMS, separately tracked**, as recorded in
`DP-038` s2. Their disposition under `ADR-0099` s4 (a) or (b) is undecided, is not decided here, and
was expressly excluded from this work package. `TRANSIT_V1` is unchanged, still records
`verdict: PASS`, and still carries no `scope_not_gated` array.

Note the ordering consequence: option **1-A** or **1-B** would make those three identifiable by rule
rather than by reading, whereas **1-C** would decide their status as a side effect of the definition.
That is a reason to settle Choice 1 before disposing of them, not a reason to dispose of them here.

---

## 7. What this paper does not do

It decides nothing. It does not edit `ADR-0099` or `ADR-0100`, and creates no permission to edit any
recorded decision entry. It does not amend `docs/Q8_CLOSURE_MATRIX.md`,
`docs/VALIDATION_STANDARD.md`, `docs/ENGINE_STATUS.md` or `docs/OPEN_QUESTIONS.md`. It does not
resolve, narrow or reinterpret `N1`, `N2`, `N5`, `N6` or `N7`, all of which remain open. It does not
declare, perform or recommend JATAKA phase exit, which **remains on HOLD**. It changes no production
code, test, CI job, registry, certification artifact or holdout datum. **It authorizes no part of the
`C2`-`C5` programme**, which remains unauthorized under `ADR-0099` s7's own terms.

---

## Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-09-22 | Created under the owner's "CEO AUTHORIZATION - NEXT GOVERNANCE PREREQUISITE" instruction. Records the measured state of the 26-artifact certification corpus, establishes that neither limb of `ADR-0099` s4's trigger is presently evaluable and that `C3` therefore cannot be specified, identifies `SIGN_CONVENTION_V1`'s `declaration_registry`/`function_registry` as the precedent to reuse and `explicit_non_claims` as the weaker declared-exclusion analogue, and presents the three semantic choices requiring owner adjudication with options and consequences. Selects none. Declares no phase exit and authorizes no implementation. |
