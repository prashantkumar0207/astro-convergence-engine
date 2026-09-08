<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ADDRESSED by `ADR-0092`** (2026-09-05): the owner accepted Option 2 - `certification/ENGINE_CAPABILITY_INVENTORY.json` is frozen dated historical evidence, not a live current-state register, is not a current source of truth, and must not be used by any future capability-consistency gate as a live-state authority. Option 2's in-file label was expressly NOT authorized ("Do not modify `ENGINE_CAPABILITY_INVENTORY.json`"), so `ADR-0092` is currently the only record of the classification. `Q12`/`LOCK_MANIFEST.json` deliberately not resolved or altered; Option 4 not adopted. The paper below remains unedited as the options record. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-05 (status only: Option 2 accepted, `ADR-0092`) |
| Review cadence | TBD |

# DP-034. Classification of `certification/ENGINE_CAPABILITY_INVENTORY.json`: live current-state register, or frozen dated historical evidence?

## 0. Authorization and scope

Written under the owner's "CEO AUTHORIZATION - BEGIN DP-034" instruction: "Proceed with DP-034 as an
options/decision paper only. Scope is strictly the classification of
`certification/ENGINE_CAPABILITY_INVENTORY.json` as either: 1. a live current-state register that must
be regenerated/enforced, or 2. frozen dated historical evidence that must be explicitly labelled and
excluded from current-state enforcement. Examine its relationship to the existing
`Q12`/`LOCK_MANIFEST.json` classification question and present the available options, consequences,
recommendation, and exact decision required from the CEO."

This paper decides nothing. Per `docs/decisions/README.md`, a paper that resolves its own question has
failed. It presents the question, the honest case for each option including the option the builder does
not recommend, the consequences, and a separately labelled recommendation with a confidence level.

**Out of scope, explicitly:** reconciling `ENGINE_STATUS.md`, `README.md`, or
`VARGA_CERTIFICATION_ROADMAP.md`; regenerating any artifact; implementing or designing a reconciliation
gate; CI wiring; D16/D4 production work; D20/D27/D60 work; resolving `DP-024`; resolving `Q12` itself.

## 1. The question

`certification/ENGINE_CAPABILITY_INVENTORY.json` is a structured, per-capability status map covering
fourteen capability domains under an explicit five-value classification scale
(`CERTIFIED`/`PARTIALLY_CERTIFIED`/`IMPLEMENTED`/`SPECIFIED`/`PLANNED`, plus `ABSENT`). It is dated
`2026-08-11` and names the commit it was compiled against (`c5a2712f`).

Since that date the engine has certified ten further capabilities. The file has not been updated. **The
question this paper exists to put to the owner is not "should it be updated" - that presupposes the
answer. The question is what kind of file it is**, because the two readings imply opposite correct
actions, and acting on the wrong reading is a governance violation in either direction.

## 2. Established facts, from the repository

### 2.1 What the file says about itself

| Field | Value |
|---|---|
| `status` | `PROPOSED - pending owner ratification (docs/OPEN_QUESTIONS.md Q1)` |
| `date` | `2026-08-11` |
| `commit` | `c5a2712ff4a3c5c3145730bfc1e4e5bc9f41c260` |
| `method` | "Compiled by reading the repository, not by reading its documents. A capability is IMPLEMENTED only if code executes it; CERTIFIED only if a regenerable artifact and a reproducible runner exist and were executed; PARTIALLY CERTIFIED where the artifact exists but **the audit of 2026-08-11** found the gate proves less than claimed." |
| `audit_reference` | `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` |
| `counts_note` | "Counts are deliberately omitted. A tally invites the impression that certified capabilities are comparable units, which they are not." |

It does **not** anywhere declare itself a live register, and it does not carry a regeneration
instruction. It names a date, a commit, and the specific audit that produced it.

### 2.2 How divergent it now is, measured

Using the file's own classification scale, at least **eleven capability statuses are now wrong**:

| Inventory entry | Recorded status | Actual state |
|---|---|---|
| `strength_and_yogas.yogas` | `ABSENT` | `PARASHARI_YOGA_V1` PASS, `ADR-0081`, production |
| `kp.significators_four_step_ruling_planets_horary` | `ABSENT` | `KP_SIGNIFICATOR_V1` PASS, `ADR-0078`/`ADR-0079`, production |
| `panchanga.tithi` / `.vara` / `.yoga` / `.karana` | `ABSENT` (x4) | `PANCHANGA_V1` PASS, `ADR-0055` |
| `rising_and_setting.sunrise_sunset` | `ABSENT` | `RISE_SET_V1` PASS, `ADR-0054` |
| `rising_and_setting.rahu_kalam` / `.yamaganda` / `.gulika` | `ABSENT` (x3) | `TRIKALAM_V1` PASS, `ADR-0060` |
| `divisional_charts` | eight entries, ending D30 | D24, D40, D45 production-registered and absent from the file; D16 and D4 certified standalone and absent |

`strength_and_yogas.shadbala: ABSENT` remains **correct** - `engine/astrology/planet_strength.py` still
raises `NotImplementedError`. The file is not uniformly wrong, which matters: a reader cannot tell the
correct entries from the incorrect ones without independently re-deriving all of them.

### 2.3 Its position relative to the gates

- `scripts/check_artifact_drift.py` globs `certification/*.json` and `reports/certification/*`. The
  inventory **is inside that gate's scope** and is counted among the 67 evidence files it reports PASS on.
- That gate compares each file **to its own committed version**. A file that is never regenerated
  therefore passes permanently. The gate's PASS says nothing about whether the file is true.
- **No script reads, regenerates, or references the inventory** - confirmed by direct search across
  `scripts/` and `engine/`. No certifier produces it.

So the file currently occupies a contradictory position: it sits inside the certification-evidence gate,
which implies live evidence, while nothing regenerates it, which implies frozen evidence.

### 2.4 The dated-evidence pattern it shares

Three files in `certification/` carry `status: PROPOSED - pending owner ratification (Q1)` plus a date
and no regenerating runner: `ENGINE_CAPABILITY_INVENTORY.json` (2026-08-11),
`G6_REMOTE_CI_VALIDATION.json` (2026-08-11), and `ORACLE_ENVIRONMENT.json` (2026-08-10). The other
twenty-one `certification/*.json` files are regenerated from scratch by a named runner on every
invocation. The inventory belongs, by shape, to the first group, not the second.

**Disanalogy worth stating:** `ORACLE_ENVIRONMENT.json` is read and enforced by
`scripts/check_oracle_environment.py`, which asserts the running environment matches it. So membership
in the dated group does not by itself imply "inert". The inventory, unlike `ORACLE_ENVIRONMENT.json`,
is read by nothing.

## 3. Relationship to `Q12` / `LOCK_MANIFEST.json`

`Q12` (`docs/OPEN_QUESTIONS.md`, **OPEN**, raised 2026-08-11) asks: "Is `LOCK_MANIFEST.json` a live
register that must be kept current, or frozen historical evidence?" Its stated reasoning is the same
one this paper faces: "If it is live it is stale and misleading; if it is frozen evidence it must say
so, because a reader cannot currently tell which, and editing frozen certification evidence would be a
governance violation while leaving a live register stale would be a documentation defect."

The precedent the project set for that file is directly relevant:

- **`ADR-0027` D5:** "`LOCK_MANIFEST.json` tier entries are **not** edited by this entry. Whether that
  file is a live register or frozen evidence is unresolved."
- **Finding C-04:** "Whether the file is a live register or frozen evidence is unresolved, which is
  exactly `Q12`. **Editing it under either reading risks a governance violation.** Left OPEN."
- **`certification/CURRENT_ENGINE_LOCK.json`, `lock_scope_note`:** "`LOCK_MANIFEST.json` is deliberately
  left untouched: it describes the LEGACY kernel exclusively, and keeping the two separate is the
  substance of audit finding F-17."

So the repository has already met this exact class of question once, and its answer was to **decline to
edit, record the question, and leave it open** - deliberately, twice, in a ratified entry and in a
certification artifact.

### 3.1 Where the two files differ, and why it matters

| | `LOCK_MANIFEST.json` | `ENGINE_CAPABILITY_INVENTORY.json` |
|---|---|---|
| Location | repository root | `certification/` |
| Inside `check_artifact_drift.py` scope | **No** | **Yes** |
| Self-declared status/date/commit | **None** (keys: `schema_version`, `project`, `source_of_truth`, `tiers`) | **Yes** - status, date, source commit, method, audit reference |
| Contains a key asserting authority | **Yes** - `source_of_truth` | No |
| Subject | the LEGACY kernel exclusively (finding F-17) | the CURRENT engine's whole capability surface |
| Known-wrong entries | `tier1_kp_significator: SPECIFICATION_PENDING`; no KP_CHAIN entry (`ADR-0006` consequence undischarged, finding C-04) | at least eleven (section 2.2) |

**These differences cut both ways, and the paper does not resolve them.** The inventory is *better*
self-documented than `LOCK_MANIFEST.json` - it names its own date, commit and originating audit, which
is what a frozen snapshot looks like. But it is *inside* the evidence gate and describes the *current*
engine, which is what a live register looks like. `LOCK_MANIFEST.json` has the opposite profile: it
asserts `source_of_truth` but sits outside the gate and describes a frozen legacy artifact.

A reader cannot settle this from the artifacts. That is precisely why it is an owner decision.

## 4. Options

### Option 1 - Live current-state register: regenerate and enforce

Declare the inventory a live register. It must be brought current, and thereafter kept current -
ideally by generating it from the same sources the capability-claim audit used
(`CERTIFIED_PRODUCTION_VARGAS`, the `certification/*.json` result fields, the certifier/validator
registrations) rather than by hand.

**Honest case for:** it is the only file in the repository that maps the *whole* capability surface at
one place under an explicit, defensible classification scale, including the `PARTIALLY_CERTIFIED`
distinction no other document expresses. Its `method` field - "compiled by reading the repository, not
by reading its documents" - is exactly the discipline the project wants. Made live and generated, it
becomes the natural source of truth for any future reconciliation gate, and the reconciliation problem
found in the 2026-09-05 audit largely dissolves: documents would be checked against a machine-generated
inventory rather than against ad-hoc greps.

**Consequences:** requires building a generator and a negative control (a gate that cannot fail is not
evidence). Its `status: PROPOSED - pending owner ratification` must be resolved, since a live register
in `certification/` that is "pending ratification" indefinitely is the same defect in a new place. The
`counts_note` position ("counts are deliberately omitted") must be preserved or explicitly overridden.
Its eleven wrong entries would be corrected by regeneration, not by hand-editing - but the first
regeneration necessarily discards the 2026-08-11 snapshot, which is itself the audit evidence for
`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`. That evidence would need to be preserved elsewhere first,
or the audit's own citation target is destroyed.

**Risk:** this is the option that most increases scope. It creates a new generated artifact, a new gate,
and a new maintenance obligation, in exchange for solving a documentation problem.

### Option 2 - Frozen dated historical evidence: label explicitly and exclude

Declare the inventory a dated snapshot: the machine-readable companion to
`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`. Add an explicit, unambiguous self-label saying so, and
name it in the exclusion list of any future current-state enforcement.

**Honest case for:** this is what the file already looks like. It names a date, a source commit, and the
audit that produced it; it says "the audit of 2026-08-11 found..."; and it shares that shape with the
other two dated evidence files. Under this reading the file is not stale at all - it is a correct record
of what was true on 2026-08-11, and its eleven "wrong" entries are not wrong, they are historical. This
option follows the `ADR-0027` D5 / finding C-04 precedent exactly, is the smallest change that removes
the ambiguity, and destroys no evidence.

**Consequences:** the repository then has no live capability inventory at all, and the 2026-09-05 audit's
finding that no single document states current capability correctly remains fully open - to be solved,
if at all, by fixing `ENGINE_STATUS.md` and `README.md` instead. The label must be added *to the file*,
which is an edit to a file inside the certification-evidence gate; that edit is small but must be
authorized explicitly, and will move the artifact-drift gate's baseline (expected, one-time, and
understood - the same pattern already seen whenever an evidence file legitimately changes).

**Risk:** a future reader may still consult it as current, because it is titled "capability inventory"
and lives in `certification/`. A label mitigates but does not eliminate that. Renaming or relocating it
would be stronger, but renaming committed certification evidence is itself a governance question this
paper does not open.

### Option 3 - Leave open, record the question only (the `Q12` treatment; **the builder does not recommend this**)

Do neither. Record that the classification is undetermined, exactly as `ADR-0027` D5 did for
`LOCK_MANIFEST.json`, and leave the file untouched.

**Honest case for:** it is the established precedent for this exact question class, it is the only
option that cannot be wrong, and it costs nothing. `ADR-0027` D5 reasoned that editing under either
reading risks a governance violation; that reasoning has not been shown false. There is a real argument
that both files should be classified together, in one decision, rather than one now and one later - and
that decision may want evidence this paper does not have.

**Consequences:** the ambiguity persists in a second file, and the count of undetermined-classification
files rises from one to two. The 2026-09-05 audit's discrepancy D-12 stays unresolved and continues to
block any reconciliation gate's exclusion list, because a gate cannot correctly exclude a file whose
classification nobody has decided.

**Why the builder does not recommend it:** `Q12` has been open since 2026-08-11 and has already caused
one documented consequence - `ADR-0006`'s KP_CHAIN entry requirement remains undischarged (finding C-04)
purely because nobody can say what the file is. Repeating that outcome for a second file, when this
file's own `status`/`date`/`commit`/`audit_reference` fields make its character *substantially clearer*
than `LOCK_MANIFEST.json`'s, would defer a question that the evidence is already adequate to answer.

### Option 4 - Resolve both files together, as one classification rule

Answer the general question - what is a dated, non-regenerated file in an evidence directory? - and
apply the resulting rule to `ENGINE_CAPABILITY_INVENTORY.json`, `LOCK_MANIFEST.json`, and any future
file of the same shape, closing `Q12` in the same act.

**Honest case for:** it is the only option that stops the class of question recurring. Both files exist;
a third could appear; a rule decided once is cheaper than three case-by-case decisions, and the project
already prefers standing rules to ad-hoc dispositions (`ADR-0040` for identifier families is the
precedent).

**Consequences:** materially larger scope than the owner authorized for this paper. `LOCK_MANIFEST.json`
carries its own live complication - the undischarged `ADR-0006` KP_CHAIN consequence and the F-17
legacy/current separation - which this paper has not investigated and should not resolve blind. It would
also make one decision depend on evidence about a file outside this paper's authorized scope.

**Note on scope:** this option is presented for completeness because it is genuinely available and
arguably the most durable. It is **outside** the scope the owner set for DP-034, and adopting it would
require a separate, wider authorization.

## 5. Recommendation

**Recommended: Option 2 - frozen dated historical evidence, explicitly labelled and excluded.**

**Confidence: MEDIUM-HIGH.**

Reasoning, stated as evidence rather than preference:

1. **The file already self-identifies as a snapshot.** It names its date, its source commit, its
   compiling method in the past tense, and the specific audit that produced it. Nothing in it claims
   currency or asks to be regenerated. Classifying it as what it says it is requires the least
   invention.
2. **It is read by nothing.** Unlike `ORACLE_ENVIRONMENT.json`, which a gate enforces, the inventory has
   no consumer. A live register with no consumer and no generator is a maintenance liability with no
   compensating benefit.
3. **Option 1's benefit is achievable without it.** If the project later wants a machine-generated
   capability inventory, it can build one from `CERTIFIED_PRODUCTION_VARGAS` and the artifact set
   directly. Nothing about that work requires reusing this file, and reusing it costs the 2026-08-11
   audit evidence.
4. **It preserves evidence.** Option 1's first regeneration overwrites the snapshot that
   `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` cites. The project's standing rule is that stored
   artifacts are history; destroying a history record to make it current inverts that rule.

**Why the confidence is not HIGH:** the file sits inside `check_artifact_drift.py`'s scope, which is a
genuine argument that the repository has been treating it as live evidence all along. That placement was
never a decision anyone recorded - it follows from a glob - but it is a fact, and a reasonable owner
could read it as the repository's own implicit prior classification. This paper does not treat a glob
pattern as a decision, but it does not pretend the ambiguity is absent either.

## 6. The exact decision required from the CEO

One classification, stated explicitly. The owner is asked to choose exactly one:

1. **Option 1 (live register):** "`certification/ENGINE_CAPABILITY_INVENTORY.json` is a live
   current-state register. Authorize the work to make it generated, current, and enforced." - which
   additionally requires deciding how the 2026-08-11 snapshot is preserved before first regeneration,
   and resolving its `PROPOSED - pending owner ratification` status.
2. **Option 2 (frozen evidence, recommended):** "`certification/ENGINE_CAPABILITY_INVENTORY.json` is
   frozen dated historical evidence of the 2026-08-11 audit. Authorize adding an explicit label saying
   so, and exclude it from all current-state enforcement." - which additionally requires authorizing
   that one small edit to a file inside the certification-evidence gate, and accepting the resulting
   one-time artifact-drift baseline move.
3. **Option 3 (leave open):** "Record the question; change nothing." - `Q12`-style, no further action.
4. **Option 4 (joint rule, out of this paper's scope):** "Resolve this together with `Q12` under one
   standing rule." - requires a separate, wider authorization.

Whichever is chosen, the decision belongs in `docs/DECISION_LOG.md` as an ADR, per
`.claude/rules/governance.md`. **This paper records no choice and makes none.**

## 7. What this paper does not do

Does not edit, label, regenerate, relocate or rename `certification/ENGINE_CAPABILITY_INVENTORY.json`.
Does not resolve `Q12` or touch `LOCK_MANIFEST.json`. Does not reconcile `ENGINE_STATUS.md`,
`README.md`, `docs/VARGA_CERTIFICATION_ROADMAP.md` or `docs/OPEN_QUESTIONS.md`. Does not design or
implement any gate, or define any exclusion list. Does not wire CI. Does not authorize D16/D4 production
work, D20/D27/D60 work, or resolve `DP-024`. Does not push, open a PR, or merge.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-09-05 | **Status header only** - Option 2 accepted by the owner and recorded as `ADR-0092`. Sections 0-7 and the 1.0.0 change-history row below are unedited, confirmed by diff: the paper remains the options record exactly as drafted, per the `DP-015`-`DP-020` convention. |
| 1.0.0 | 2026-09-05 | Created under the owner's "CEO AUTHORIZATION - BEGIN DP-034" instruction. Presents four options for classifying `certification/ENGINE_CAPABILITY_INVENTORY.json` (live register / frozen dated evidence / leave open / joint rule with `Q12`), the measured divergence (eleven wrong capability statuses against the file's own scale), its self-declared snapshot fields, its contradictory position inside `check_artifact_drift.py`'s scope with no regenerating runner, and the `Q12`/`LOCK_MANIFEST.json` precedent including `ADR-0027` D5 and finding C-04. Recommends Option 2 at MEDIUM-HIGH confidence, with the counter-argument stated. Decides nothing. |
