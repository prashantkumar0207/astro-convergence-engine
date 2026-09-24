<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Design research for `ADR-0101` s6's unresolved specification questions. **DECIDES NOTHING.** Requires owner adjudication on the items listed in section 10. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-09-23 |
| Review cadence | TBD |

# DP-041. Capability enumeration, identifier grammar and the remediation backlog: resolving `ADR-0101` s6

Written under the owner's "CONTINUE AUTONOMOUSLY" instruction following the merge of `DP-040` at
`8ebf71bb3b78aea0655eb1ca7171d1c660b3113d`. `DP-041`'s identifier was allocated in
`docs/decisions/README.md` before this paper's substantive content was written, per `ADR-0040`. **That
ordering is not independently proven by the commit graph:** the index row and this paper were
committed together. All evidence was measured against `main` at
`8ebf71bb3b78aea0655eb1ca7171d1c660b3113d`.

**The design is not invented here.** Every candidate below is traced to an existing repository
precedent, and sections 10 and 11 separate what follows from existing authority from what genuinely
requires the owner. **This paper decides nothing and selects no option.**

---

## 1. Governing authority

| Instrument | Status | What it fixes |
|---|---|---|
| `ADR-0099` s4 | ACCEPTED | The SCOPE OVERCLAIM obligation itself: gate it, or declare it in `scope_not_gated` with a per-item reason |
| `ADR-0100` s1 | ACCEPTED | That obligation's authority is `ADR-0099` itself; `docs/VALIDATION_STANDARD.md` is a subject-matter reference only |
| `ADR-0101` s2 | ACCEPTED | Artifacts **must** enumerate production capabilities using **stable machine-readable capability identifiers**; `scope` prose is explanatory evidence, not authoritative identity; no word-match inference |
| `ADR-0101` s3 | ACCEPTED | Each gate **must** declare an **`exercises`** array of the identifiers it covers; `C3` evaluated from explicit declarations only |
| `ADR-0101` s4 | ACCEPTED | Universal application; **no silent or permanent grandfathering**; a declared remediation backlog carrying **artifact identity, deficiency, required remediation, status, disposition/owner**; **no unsafe all-at-once migration** |
| `ADR-0101` s6 | ACCEPTED | Lists precisely the questions this paper researches as **unresolved** |
| `ADR-0092` | ACCEPTED | **`ENGINE_CAPABILITY_INVENTORY.json` only**: frozen dated historical evidence, **"must not be used by the future capability-consistency gate as a live-state authority"**, and **"Do not modify"** it. It exempts **one file** from **one enforcement surface**; it says nothing about `ADR-0101` |
| `ADR-0042` decision 1 | ACCEPTED | Authority hierarchy: DECISION LOG / ADR sits above STANDARDS |
| `.claude/rules/certification.md` | project rule | Stored artifacts are **never hand-edited**; regenerate to verify; **"a gate that cannot fail is not evidence"** - any new or repaired gate needs a committed negative control |
| `docs/NAMING_STANDARD.md` s2 | DRAFT | ID-family table: `ADR-\d{4}`, `DP-\d{3}`, `EV-CAR-\d{3}`, `TC-CAR-\d{3}`, etc. **Has no family for code capabilities** |

**The word `exercises` is the only identifier fixed by ratified text.** Every other key name, shape and
location below is open.

---

## 2. Repository evidence: the corpus, and three universes that must not be conflated

Measured at `8ebf71bb`:

| Measurement | Value |
|---|---|
| Files in `certification/*.json` | **26** |
| Declared **FROZEN_EVIDENCE** in `scripts/check_capability_state.py` L84-L89 | **4** - `ENGINE_CAPABILITY_INVENTORY.json`, `ORACLE_ENVIRONMENT.json`, `G6_REMOTE_CI_VALIDATION.json`, `CURRENT_ENGINE_LOCK.json` |
| Carrying a non-empty `scope` | **22** |
| Carrying `gates` | 21 |
| Carrying `_slug` / `_artifact_name` | **22** |
| Carrying `explicit_non_claims` | 22 |
| Carrying `scope_not_gated` | **0** |
| Carrying any per-gate `exercises` | **0** |
| Distinct `schema` values | **26** - one per artifact; there is no shared schema to extend |
| Distinct top-level keys across the corpus | **67** |

### 2.1 Three universes, distinguished

An earlier draft of this paper (v1.0.0) concluded that the `ADR-0101` obligation universe is 22 rather
than 26, and presented that as derived from ratified authority. **The CEO audit of PR #28 found that
conclusion insufficiently established, and it is withdrawn here.** It conflated three distinct things:

| Universe | What it is | Authority | Size |
|---|---|---|---|
| **U1. Measured corpus** | Files matching `certification/*.json` | Direct measurement | **26** |
| **U2. `check_capability_state.py` live-source universe** | U1 minus the four names in that script's `FROZEN_EVIDENCE` constant | The script itself, at one call site | **22** |
| **U3. `ADR-0101` obligation universe** | The artifacts to which s2 and s3's requirements apply | `ADR-0101` s4, ratified | **not established** |

**What `ADR-0101` s4 actually says**, at `docs/DECISION_LOG.md` L9145 and L9159-L9163:

> The requirements in sections 2 and 3 apply **universally to the certification corpus.**

> **Measured starting position at `f8f13607`** ... **26** certification artifacts, of which **22** carry
> a non-empty `scope` ...

The ratified text says *universally to the certification corpus* and records that corpus as **26**. It
does not carve out an exemption, and it does not equate the corpus with the scope-bearing subset.

**What `ADR-0092` actually exempts.** It names **one file**, `ENGINE_CAPABILITY_INVENTORY.json`, and
exempts it from being used **"by the future capability-consistency gate as a live-state authority"**,
while separately forbidding its modification. That is an exemption from **one enforcement surface**.
`ADR-0101` s2/s3/s4 is a different surface, and `ADR-0092` does not address it.

**What the other three frozen files rest on.** `scripts/check_capability_state.py` L81-L83 states it in
its own words:

> Dated evidence, never a live source. **`ADR-0092` decides this for the capability inventory
> specifically; the other three share its shape** (a date, a source commit or environment, and no runner
> that regenerates them).

Measured: `ORACLE_ENVIRONMENT.json` and `G6_REMOTE_CI_VALIDATION.json` are named in **zero** `ADR`
entries that call them frozen or historical; `CURRENT_ENGINE_LOCK.json`'s single near-match is about
frozen `CalculationProfile` definitions, not about the artifact's status. **Three of the four are frozen
by a builder's shape-based inference recorded in a code comment, not by any ratified decision.**

**How narrowly `FROZEN_EVIDENCE` is actually used.** The constant appears at exactly **one** call site,
`check_capability_state.py` L199, where it `continue`s past those four names while building the verdict
map for that gate's own completeness universe. It is a parameter of one script's reading, not a
repository-wide exemption.

### 2.2 The consequence, stated as a question rather than an answer

**Whether U3 equals U1 (26), U2 (22), or something else is not established by any ratified text**, and
this paper does not decide it. It is carried to section 10 as **Q-E**. Three readings are live:

- **U3 = 26.** The plain reading of "universally to the certification corpus" together with s4's own
  measurement. Consequence: the four frozen artifacts are in scope for s2/s3, yet three have no runner
  to write an enumeration and `ADR-0092` forbids modifying the fourth - so they could only ever enter
  compliance **through the backlog**, which is arguably exactly what s4's no-silent-grandfathering rule
  intends.
- **U3 = 22.** The reading v1.0.0 asserted. It is *coherent* - only 22 carry `scope`, and a SCOPE
  OVERCLAIM cannot arise without one - but it requires either an interpretation of `ADR-0101` or an
  extension of `ADR-0092` to three files it never named.
- **U3 = 22 for s2/s3, 26 for s4.** The obligations apply where they can be satisfied; the backlog
  records the remainder. This is the only reading under which nothing is silently exempt **and** nothing
  is required of an artifact that cannot produce it.

**The measured facts in the table above are not in question. Only the mapping from those facts to
`ADR-0101`'s universe is unresolved.**

---

## 3. Precedent A - stable artifact identity already exists (`_slug`)

22 artifacts carry `_artifact_name` and `_slug`, written **mechanically** by
`scripts/certification_support.py` L477-L478 - never hand-authored:

```
current_engine   kp_chain   kp_significator   panchanga   parashari_drishti
parashari_yoga   rise_set   sign_convention   transit     trikalam
varga_d2  varga_d3  varga_d7  varga_d12  varga_d16  varga_d20
varga_d24  varga_d30  varga_d40  varga_d45  varga_d4
```

Grammar in practice: lowercase, `[a-z0-9_]`, no leading/trailing underscore. **`ADR-0101` s4's
"artifact identity" field has an existing, mechanically-generated answer.** No new convention is
needed for that field.

## 4. Precedent B - a machine-readable backlog already exists

`certification/G6_REMOTE_CI_VALIDATION.json` carries `technical_debt`, a list of objects whose field
union is:

```
id / title / observed / evidence_class / severity / blocking / detail / decision
```

with, for example:

```json
{
  "id": "TD-CI-002",
  "title": "Oracle tier bound to CPython 3.11 linux x86_64",
  "severity": "LOW",
  "blocking": false,
  "detail": "requirements-oracle.lock carries cp311 linux x86_64 wheel hashes, so the oracle job
             cannot run on 3.12 until a second lock and a second recorded identity exist.",
  "decision": "Recorded, not fixed. Must never be resolved by relaxing hashes."
}
```

The same artifact carries a top-level **`evidence_classes`** vocabulary - `EXECUTED_LOCAL`
("run by the builder in this container and directly observed") and `CEO_REPORTED` ("observed by the
CEO/technical auditor ... NOT independently observed by the builder"). It also carries
`open_items_not_closed_by_g6` and `deviations_from_plan`, both prose lists.

**Mapped against `ADR-0101` s4's five required fields:**

| `ADR-0101` s4 requires | `technical_debt` supplies | Gap |
|---|---|---|
| artifact identity | *(implied by containment)* | **yes** - a corpus-wide backlog cannot rely on containment |
| deficiency | `title` + `detail` | no |
| required remediation | partly `decision` | **partial** - `decision` mixes disposition and remediation |
| status | `blocking` + `severity` | **partial** - no explicit lifecycle status |
| disposition / owner | `decision`; **no `owner` field** | **yes** for owner |

**Governance gap, reported not resolved:** `TD-CI-\d{3}` appears in four tracked files
(`G6_REMOTE_CI_VALIDATION.json`, `docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md`,
`docs/DECISION_LOG.md`, `reports/G6_COMPLETION_RECORD.md`) but **`TD-` is absent from
`docs/NAMING_STANDARD.md` s2's ID-family table and is not covered by
`scripts/check_retired_identifiers.py`.** An established identifier family is in use, unregistered.

## 5. Precedent C - a hierarchical capability vocabulary already exists, and cannot be reused as authority

`certification/ENGINE_CAPABILITY_INVENTORY.json` holds **91 leaf capability entries** under 14 domains,
addressed by dotted path - `astronomical_kernel.ephemeris_strict_swieph`,
`divisional_charts.D9_navamsa`, `transits.longitude_crossing_primitive` - each with a `status` drawn
from a declared `classification_scale`:

```
CERTIFIED / PARTIALLY_CERTIFIED / IMPLEMENTED / SPECIFIED / ABSENT
```

**This is the repository's only existing example of naming capabilities rather than callables**, and it
demonstrates multi-callable grouping directly: `divisional_charts.D4_D16_D20_D24_D27_D40_D45_D60` is
one entry spanning eight divisions.

**Two constraints on reusing it, both from ratified authority.** `ADR-0092` classifies the file as
frozen dated historical evidence, states it **"must not be used by the future capability-consistency
gate as a live-state authority"**, and instructs **"Do not modify"** it. So its *vocabulary shape* is
citable precedent; its *content* is not a source of truth and its file is not editable.

**And it is directly material to `DP-040`.** The inventory's transit entries are:

```
transits.longitude_crossing_primitive        CERTIFIED
transits.sign_and_nakshatra_ingresses        PARTIALLY_CERTIFIED
transits.returns_and_natal_conjunctions      IMPLEMENTED  "in no certified artifact"
transits.true_node_path                      IMPLEMENTED
transits.aspect_system_events                ABSENT
transits.dasha_transit_convergence           ABSENT
```

**`transits.returns_and_natal_conjunctions` collapses two of `DP-040`'s three callables into a single
capability.** `DP-040` established that `returns()` is a pure delegator while `natal_conjunctions()`
is not, and that their dispositions therefore differ. **A capability vocabulary at this granularity
cannot express two different dispositions for one identifier.** That is the sharpest concrete
consequence of question 3, and it is evidence, not opinion.

Note also that `transit_view()` has **no** entry in the inventory's `transits` domain at all; the
nearest is `domains.varshaphal_annual.components.solar_return`, which names `returns()`.

## 6. Precedent D - the live sanctioned capability source, and the gate over it

`docs/ENGINE_STATUS.md` carries a `<!-- CAPABILITY-BLOCK:BEGIN ... -->` / `<!-- CAPABILITY-BLOCK:END -->`
fenced JSON block, parsed by `scripts/check_capability_state.py` L73-L79 and enforced by a numbered
failure-condition vocabulary **F1 ... F14**. `ADR-0092` points here, not at the inventory, for live
state. `ADR-0101` s7's `C2` is described as extending exactly this gate.

**Consequence for question 1:** the repository already has two distinct homes for machine-readable
capability data - a fenced block in a governed Markdown document (live, gated, hand-maintained but
machine-checked) and top-level keys in certifier-written JSON artifacts (regenerated, never
hand-edited). `ADR-0101` s2 says *artifacts* enumerate, which points at the second.

## 7. Precedent E - `declaration_registry` / `function_registry`, and `explicit_non_claims`

`SIGN_CONVENTION_V1_certification.json` carries `declaration_registry` (20 entries) and
`function_registry` (6 entries), both dicts keyed by **dotted Python identifiers**:

```
"engine.astrology.signs.zodiac_sign": "one_based"
"engine.astrology.navamsa_chart.navamsa_sign": "zero_based"
"Chart.sign_map": {"convention": "one_based", "shape": "dict_keys", "accessor": null}
```

`ADR-0101` s2 names this as the precedent to reuse. Note it is **code-anchored**: keys are import
paths, not capability names. It is the opposite granularity choice from precedent C.

`explicit_non_claims` (22 artifacts) is a **prose list**, e.g. *"Four Step Theory (Gondhalekar) - out
of scope (ADR-0027 Decision 3)"*. It supplies the **form** of a declared exclusion with a reason -
**one shape `scope_not_gated` could take** - but is not machine-checkable against code.

---

## 8. Candidate designs

### 8.1 Question 1 - capability-enumeration key and shape

| Option | Design | Advantages | Disadvantages |
|---|---|---|---|
| **1-A. Top-level `capabilities` array of objects** in each artifact, written by the certifier | `[{"id": ..., "callables": [...], "note": ...}]` | Carries per-capability metadata; mirrors `technical_debt`'s object-list shape; extensible | A new top-level key across 22 bespoke schemas |
| **1-B. Top-level `capability_registry` dict**, id -> metadata | Mirrors `declaration_registry`/`function_registry` exactly - the precedent `ADR-0101` s7 names | Closest to the cited precedent; natural key uniqueness | Dict ordering carries no meaning; slightly awkward for capabilities with no metadata |
| **1-C. Reuse the `rule` key's nesting**, adding `rule.capabilities` | No new top-level key | `rule` exists on only 13 of 26 artifacts; wrong home for non-varga capabilities |

**Derivable regardless of option:** the enumeration must be **written by the certifier, not
hand-edited** (`.claude/rules/certification.md`), and must live in the artifact rather than in
`ENGINE_STATUS.md`, because `ADR-0101` s2 says *artifacts* enumerate.

### 8.2 Question 2 - identifier grammar

| Option | Grammar | Precedent | Advantages | Disadvantages |
|---|---|---|---|---|
| **2-A. Dotted Python import path** | `engine.transits.events.returns` | `function_registry` | Mechanically verifiable against the tree; zero ambiguity; an identifier that cannot silently drift from code | Cannot name a capability spanning several callables without inventing a synthetic path; couples the register to module layout, so a refactor renames capabilities |
| **2-B. Dotted capability slug** | `transits.returns` | `ENGINE_CAPABILITY_INVENTORY` domains; `_slug` charset | Survives refactoring; expresses capabilities, which is what `ADR-0101` s2 says to enumerate | Needs its own mapping to code, and that mapping is the thing a gate would have to trust |
| **2-C. Artifact-scoped slug** | `transit/returns` using the existing `_slug` as the scope | Reuses `_slug`, already mechanically generated | Scope is unambiguous and already exists | Two capabilities of the same name in different artifacts are distinct, which may be right or wrong |
| **2-D. Registered ID family** | `CAP-TRN-001` | `NAMING_STANDARD` s2 table; `TD-CI-\d{3}` | Fits the repository's existing ID-family machinery and could be gated by `check_retired_identifiers` | Opaque; needs a registry mapping ids to meaning; `NAMING_STANDARD.md` is DRAFT |

### 8.3 Question 3 - a capability spanning several callables

This is the question precedent C makes concrete.

| Option | Design | Consequence for `DP-040` |
|---|---|---|
| **3-A. One identifier, explicit `callables` list** | `{"id": "transits.natal_relative_view", "callables": ["engine.transits.view.transit_view"]}` | Expresses "natal-relative view" naturally. A capability's disposition is then **uniform across its callables** - so `returns()` and `natal_conjunctions()` **must not** share one identifier, contradicting the inventory's `returns_and_natal_conjunctions` |
| **3-B. One identifier per callable; composite capabilities are not expressible** | `engine.transits.view.transit_view` | Maximum precision, per-callable dispositions trivially expressible | `scope` strings name *capabilities* ("natal-relative view"), so the enumeration stops corresponding to the prose it replaces |
| **3-C. Two-level: capability with member callables, dispositions at member level** | `{"id": ..., "members": [{"callable": ..., "disposition": ...}]}` | Expresses both, at the cost of the most complex schema of the three |

### 8.4 Questions 4 and 5 - backlog location, schema, and status/disposition/owner

| Option | Location | Advantages | Disadvantages |
|---|---|---|---|
| **4-A. A committed register**, e.g. `certification/REMEDIATION_BACKLOG.json` | One corpus-wide view; countable; reviewable in one diff | **Hand-maintained**, so it can drift from the artifacts unless a gate binds them; a new artifact-directory file that is not certifier-generated |
| **4-B. Per-artifact key** `remediation_backlog`, written by each certifier | Mirrors `technical_debt` exactly; regenerated, so it cannot drift | No single corpus-wide view without an aggregator; cannot hold entries for the 4 frozen artifacts, which have no runner |
| **4-C. A governed Markdown register** with a fenced JSON block, like `CAPABILITY-BLOCK` | Reuses precedent D's machinery, including its gate pattern | Hand-maintained like 4-A; puts certification state in a docs file |

**Schema: the five fields are required by s4; the surrounding shape is a candidate.** `ADR-0101` s4's
five fields map onto `technical_debt`'s eight with two genuine gaps - explicit `status` and `owner`.
The field list below adds `observed` and `evidence_class` from that precedent; **those two are
suggestions, not requirements**:

```
id / artifact / capability / deficiency / required_remediation / status / disposition / owner / observed / evidence_class
```

`evidence_class` is offered because `G6_REMOTE_CI_VALIDATION.json` already declares that vocabulary and
an audit-time observation is not the same evidence class as a gate result.

**`owner` cannot be specified here.** `docs/OPEN_QUESTIONS.md` **Q1 (named owners) is OPEN**, and every
governing document in the repository carries `Owner | TBD (see docs/OPEN_QUESTIONS.md Q1)`. Any
`owner` vocabulary invented now would either contradict Q1 or be a placeholder. **This is a hard
dependency, not a design preference.**

**Status vocabulary candidates**, both from existing repository vocabularies: `classification_scale`
(`CERTIFIED`/`PARTIALLY_CERTIFIED`/`IMPLEMENTED`/`SPECIFIED`/`ABSENT`) or a lifecycle set
(`OPEN`/`IN_PROGRESS`/`CLOSED`/`ACCEPTED_DEBT`) modelled on `technical_debt`'s
`severity`+`blocking`+`decision`.

### 8.5 Question 6 - does backlog completeness itself need a gate?

**Unresolved. An earlier draft (v1.0.0) called the existence of such a gate derivable; the CEO audit of
PR #28 found that too strong, and it is withdrawn.**

What **is** supported by ratified text: `ADR-0101` s4 requires a **declared remediation backlog** with
five named fields, and forbids silent and permanent grandfathering. **The backlog's existence and its
schema are therefore requirements.**

What is **not** supported: `ADR-0101` contains no sentence requiring that **backlog completeness be
mechanically gated**. `.claude/rules/certification.md`'s *"a gate that cannot fail is not evidence"* is a
rule about **gates** - it constrains gates that exist, and says nothing about which obligations must be
gated. Deriving a mandatory completeness gate from it would be manufacturing a requirement from a
general principle, and this paper does not do so.

**Whether backlog completeness is enforced by a gate at all is therefore an open design question**,
carried to section 10 as **Q-F**. If the owner decides it should be, the candidate forms are:

| Option | Design | Notes |
|---|---|---|
| **6-A. Extend `check_capability_state.py`** with new F-conditions | Reuses the F1-F14 vocabulary and an already-CI-wired gate; `ADR-0101` s7 already describes `C2` as extending this script | Concentrates more responsibility in one gate |
| **6-B. A new `check_remediation_backlog.py`** | Separable, independently negative-controllable | A fifth governance gate to wire and maintain |
| **6-C. Fold it into `C3`** | Fewest moving parts | Couples backlog completeness to scope coverage; a `C3` failure would then have two unrelated causes |

**Negative-control implication, if any gate is built:** each of the three changes what a gate can
reject, so each would require its own committed negative control proving it rejects a real violation -
`ADR-0101` s7 and `.claude/rules/certification.md`. CI already has four such controls (`ci.yml` L140,
L397, L421, L550) to model on. **This applies to a gate that is built; it is not an argument that one
must be.**

### 8.6 Question 7 - representing the existing corpus without grandfathering

**Not derivable.** This question cannot be answered before **Q-E** (section 2.2) settles which universe
`ADR-0101` s4 governs. v1.0.0 answered it by asserting U3 = 22; that assertion is withdrawn.

What survives unchanged is the measured position: **26** files, **4** named in `FROZEN_EVIDENCE`, **22**
scope-bearing and runner-regenerated, **0** carrying an enumeration, `exercises` or `scope_not_gated`.

The migration options below are written for "the artifacts in the obligation universe", whichever Q-E
determines that to be. **Under U3 = 26 they additionally require a way for the four frozen artifacts to
be represented** - and since three have no runner and the fourth may not be modified per `ADR-0092`,
**the backlog is the only mechanism available to them**, which is a point in favour of the U3 = 26 or
mixed readings rather than against them.

The open part is **how the obligation universe enters compliance**:

| Option | Design | Migration implication |
|---|---|---|
| **7-A. Backlog-first** - land the backlog with every artifact in the universe enumerated as non-compliant, then remediate | Satisfies s4's "no silent grandfathering" from day one; nothing is hidden | The backlog is 22 entries long on day one and shrinks |
| **7-B. Gate-first with the backlog as the escape hatch** | `C3` lands and every artifact either complies or is in the backlog | Requires backlog and gate to land together, a larger single step |
| **7-C. Per-artifact, one regeneration at a time** | Smallest steps, each independently reviewable | Longest period in which the obligation is in force and partially unenforced |

**All three regenerate artifacts** for the runner-regenerated members of the universe. On this Windows host the oracle-tier certifiers cannot run, so any
regeneration touching them must be **CI-sourced**, captured with an explicit per-tier file list - the
pattern `ADR-0096`'s recovery commit established after the D20 copy-order defect.

### 8.7 Question 8 - where the three `TRANSIT_V1` overclaims sit

**Structurally derivable; substantively blocked on `DP-040`.** `TRANSIT_V1` is scope-bearing and
runner-regenerated, so it sits inside the obligation universe under **every** reading of **Q-E**. Under
any backlog location in 8.4 the three become entries under artifact `transit` (its existing `_slug`), each with its own deficiency and its
own `required_remediation`. `DP-040` established that the required remediation **differs per callable
within that one artifact**, which is direct evidence for keying the backlog at **capability**
granularity rather than artifact granularity, and against option 3-A's grouping if
`returns_and_natal_conjunctions` were adopted as the identifier.

**The backlog can hold all three as `OPEN` without prejudging `DP-040`.** Recording a deficiency is
not disposing of it. Nothing in this paper disposes of them.

---

## 9. Interaction with `C2`-`C5` and with `DP-040`

**`C2`** (`ADR-0101` s7) extends `check_capability_state.py` with a
`declared_production_analytical_inputs` key in `ENGINE_STATUS.md` s6. It is **independent of every
question in this paper** - it concerns the *declaring* union under `ADR-0099` s2, not per-artifact
capability enumeration. **`C2` is not blocked by anything here.**

**`C3`** is blocked by questions 1, 2 and 3: it cannot be specified until the enumeration key, the
identifier grammar and the multi-callable representation exist. It is additionally shaped by 6 and 7.

**`C4`** (reachability, implementing `ADR-0099` s3) is independent of this paper, with one caveat: if
2-A (dotted import paths) is chosen, `C4` and the enumeration would share an identifier space, which
is an advantage worth weighing.

**`C5`** (delegator neutrality tests) is independent, and `DP-040` established it is applicable to
`returns()` only.

**`DP-040`** interacts in two directions. Its four `scope_not_gated`-dependent options - 1-B, 1-C, 2-B
and 3-B - **cannot be implemented until question 1's shape is settled**, since `scope_not_gated` is a
sibling of the enumeration key. And its finding that remediation differs per callable is the strongest
single piece of evidence for question 3 and for backlog granularity.

**CI implications, common to all options:** any new gate needs a CI step and a negative-control step;
any artifact-schema change regenerates artifacts and therefore exercises the drift gates at `ci.yml`
L231 and L345; the governance job (L391-L550) is where a backlog-completeness gate would most
naturally sit alongside the existing four.

---

## 10. What genuinely requires CEO adjudication

**Six items. None is derivable from repository authority.**

- **Q-A. Identifier granularity and grammar** (questions 2 and 3 together). Code-anchored dotted import
  paths, capability slugs, artifact-scoped slugs, or a registered ID family - and whether a capability
  may span several callables. **These two cannot be decided separately:** 2-A largely forces 3-B, while
  2-B or 2-D permits 3-A or 3-C. Precedent points both ways (`function_registry` is code-anchored;
  `ENGINE_CAPABILITY_INVENTORY` is capability-anchored), and `ADR-0092` blocks the latter from being
  authority.
- **Q-B. Backlog location** (question 4): a committed register, a per-artifact certifier-written key,
  or a governed Markdown block. The trade is **corpus-wide visibility versus immunity from drift**. If
  **Q-E** puts the four frozen artifacts inside the obligation universe, note that **4-B cannot
  represent them at all** - three have no runner to write the key and `ADR-0092` forbids modifying the
  fourth.
- **Q-C. `owner` semantics** (question 5). **Hard-blocked on `Q1`**, which is OPEN. Either `Q1` is
  resolved first, or the owner directs that `owner` be recorded with a placeholder vocabulary and
  states which - it should not be invented.
- **Q-D. Migration sequence** (question 7): backlog-first, gate-first, or per-artifact. This decides
  how long the ratified obligation stays in force while partially unenforced. **Depends on Q-E**,
  since it cannot be sequenced over an unknown universe.
- **Q-E. The `ADR-0101` obligation universe** (section 2.2), raised by the CEO audit of PR #28 and
  **not present in v1.0.0**, which asserted an answer instead. Does `ADR-0101` s4's "universally to
  the certification corpus" mean **26**, **22**, or **26 for s4 with 22 for s2/s3**? `ADR-0101` s4
  says *universally* and measures the corpus at **26**; `ADR-0092` exempts **one** file from **one**
  enforcement surface that is not `ADR-0101`'s; and three of the four frozen files rest on a code
  comment rather than any ratified decision. **Resolving this may require an interpretation of
  `ADR-0101`, an extension of `ADR-0092`, or a new entry** - which is an owner decision, not a
  builder reading. **Q-D, question 7 and the practical shape of Q-B all wait on it.**
- **Q-F. Whether backlog completeness is mechanically gated** (section 8.5), also raised by the CEO
  audit and **not present in v1.0.0**, which called the gate's existence derivable. `ADR-0101` s4
  requires the backlog to exist and names its fields; **no ratified text requires that its
  completeness be gated.** If the owner wants one, forms 6-A, 6-B and 6-C are set out above; if not,
  the backlog is a declared record maintained without mechanical enforcement, which is what s4
  literally requires.

Secondary, and only if the owner wants it settled now rather than at implementation: the **status
vocabulary** (8.4), and - **if** Q-F is answered yes - the **gate form** (8.5). Both have defensible
precedent either way.

## 11. What does NOT require CEO adjudication

These follow from ratified authority or existing mechanical precedent and can be settled by
implementation precedent when the work is authorized:

1. **"Artifact identity" needs no new convention for the 22 that carry one** - `_slug` is
   machine-generated at `certification_support.py` L477-L478. The four `FROZEN_EVIDENCE` files carry
   no `_slug`, so if **Q-E** places them in the universe their identity field needs one decision, most
   obviously the filename.
2. **The measured corpus facts are settled and are not in question** - **26** files, **4** named in
   `FROZEN_EVIDENCE`, **22** scope-bearing and runner-regenerated, **0** carrying an enumeration,
   `exercises` or `scope_not_gated`. *(v1.0.0 listed here a claim that the obligation universe is 22
   rather than 26. **That claim is withdrawn** and is now **Q-E** in section 10. The measurement
   stands; the mapping from it to `ADR-0101`'s universe does not.)*
3. **The enumeration lives in the artifact, not in `ENGINE_STATUS.md`** - `ADR-0101` s2 says artifacts
   enumerate.
4. **The enumeration is certifier-written, never hand-edited** - `.claude/rules/certification.md`.
5. **`exercises` is the fixed key name for the per-gate declaration** - `ADR-0101` s3.
6. **The backlog must exist and must carry `ADR-0101` s4's five named fields** - stated in s4's own
   text. *(v1.0.0 listed here a claim that backlog completeness requires a gate, derived from "a gate
   that cannot fail is not evidence". **That claim is withdrawn**: that rule constrains gates that
   exist and does not make any obligation gateable-by-necessity. Whether completeness is enforced by
   a gate is now **Q-F** in section 10.)*
7. **Every new or extended gate that is built requires its own committed negative control** -
   `ADR-0101` s7 and `.claude/rules/certification.md`; four CI precedents exist. This constrains gates
   that are built; it does not require that any be built.
8. **Artifact regeneration touching oracle-tier certifiers must be CI-sourced** with an explicit
   per-tier file list - the `ADR-0096` recovery pattern, on the documented Windows parity gap.
9. **The three `TRANSIT_V1` overclaims can be recorded as `OPEN` backlog entries without prejudging
   `DP-040`** - recording a deficiency is not disposing of it.
10. **The backlog schema's non-`owner` fields can follow `technical_debt`** - `id`, `title`/`deficiency`,
    `detail`, `observed`, `evidence_class`, plus the `required_remediation` and `status` fields
    `ADR-0101` s4 names.

**One governance gap reported, not resolved:** the `TD-CI-\d{3}` identifier family is in live use in
four tracked files but is absent from `docs/NAMING_STANDARD.md` s2's ID-family table and is not covered
by `scripts/check_retired_identifiers.py`. If a new capability or backlog ID family is introduced, the
same omission should not be repeated.

---

## 12. What this paper does not do

It decides nothing and selects no option. **It does not resolve `Q-E` or `Q-F`**, the two questions
the CEO audit of PR #28 restored to unresolved; it neither interprets `ADR-0101` s4's universe nor
extends `ADR-0092` beyond the single file it names. It does not modify `engine/`, `certification/`,
`scripts/`, `.github/`, `docs/ENGINE_STATUS.md`, `docs/Q8_CLOSURE_MATRIX.md`,
`docs/OPEN_QUESTIONS.md`, `docs/DECISION_LOG.md`, `docs/VALIDATION_STANDARD.md`, any existing `ADR`
body, `DP-039` or `DP-040`. It does not implement `C2`, `C3`, `C4` or `C5`. It does not
create any capability enumeration, `exercises` array, `scope_not_gated` array or remediation backlog.
It does not dispose of the three `TRANSIT_V1` SCOPE OVERCLAIMS, which remain open. It does not resolve
`N1`, `N2`, `N5`, `N6` or `N7`, nor `Q1` or `Q12`. It does not declare, perform or recommend JATAKA
phase exit, which **remains on HOLD**.

---

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-09-24 | **Corrections required by the CEO audit of PR #28, which returned HOLD.** **Material:** v1.0.0 stated that the `ADR-0101` obligation universe is 22 artifacts rather than 26 and presented that as derived from ratified authority. **That conclusion is withdrawn.** It conflated three universes, now distinguished in a new section 2.1: the measured corpus (26), `check_capability_state.py`'s live-source universe (22, set by that script's own `FROZEN_EVIDENCE` constant at one call site, L199), and `ADR-0101`'s obligation universe, which **no ratified text establishes**. `ADR-0101` s4 L9145 says the requirements apply *"universally to the certification corpus"* and L9159-L9163 measures that corpus at 26; `ADR-0092` exempts **one** file from **one** enforcement surface - use as a live-state authority by the capability-consistency gate - which is not `ADR-0101`'s surface; and `ORACLE_ENVIRONMENT.json`, `G6_REMOTE_CI_VALIDATION.json` and `CURRENT_ENGINE_LOCK.json` are frozen on a builder's shape-based inference recorded in a code comment at `check_capability_state.py` L81-L83, backed by **no** `ADR`. The question is restored as unresolved **Q-E**, with three live readings and a note that resolving it may require an interpretation of `ADR-0101`, an extension of `ADR-0092`, or a new entry - an owner decision. Section 8.6 no longer answers question 7 and now waits on Q-E. **Secondary:** v1.0.0 listed "backlog completeness requires a gate" as not requiring adjudication, deriving it from *"a gate that cannot fail is not evidence"*. **That is withdrawn too**: `ADR-0101` s4 requires the backlog to exist and names its fields but contains no sentence requiring mechanical enforcement of its completeness, and that rule constrains gates that exist rather than making an obligation gateable-by-necessity. Backlog existence and schema remain derived; enforcement becomes unresolved **Q-F**, with candidate forms 6-A/6-B/6-C retained. Also corrected, per audit item E: the introduction pointed at "section 9" for the derived-versus-adjudicated split, which lives in sections 10 and 11; section 1's `ADR-0092` row now states the exemption's exact scope; section 10's count goes four to six; section 11 items 1, 2, 6 and 7 are re-scoped, with the two withdrawals marked in place rather than deleted. The measured corpus facts are unchanged throughout. Still decides nothing, selects no option, authorizes no `C2`-`C5` work, creates no enumeration, `exercises` array, `scope_not_gated` or backlog, disposes of none of the three `TRANSIT_V1` scope overclaims, and declares no phase exit. |
| 1.0.0 | 2026-09-23 | Created under the owner's "CONTINUE AUTONOMOUSLY" instruction after `DP-040` merged at `8ebf71bb`. Researches `ADR-0101` s6's eight unresolved specification questions against existing repository precedent rather than inventing a design. Records five precedents: `_slug`/`_artifact_name` as mechanically-generated artifact identity on 22 artifacts; `technical_debt` in `G6_REMOTE_CI_VALIDATION.json` as an existing machine-readable backlog with an eight-field schema and an `evidence_classes` vocabulary; `ENGINE_CAPABILITY_INVENTORY.json`'s 91-entry hierarchical capability vocabulary, which `ADR-0092` forbids using as live authority and whose `transits.returns_and_natal_conjunctions` entry would collapse two callables `DP-040` showed need different dispositions; the `CAPABILITY-BLOCK` plus `check_capability_state.py` F1-F14 gate as the live sanctioned source; and `declaration_registry`/`function_registry`/`explicit_non_claims`. Establishes from `ADR-0092` and the measured `FROZEN_EVIDENCE` set that the obligation universe is **22 artifacts, not 26**. Presents candidate designs for each question with advantages, disadvantages, migration, negative-control and CI implications, and **selects none**. Separates four items genuinely requiring CEO adjudication - identifier granularity and grammar, backlog location, `owner` semantics (hard-blocked on `Q1`), migration sequence - from ten that follow from existing authority. Reports that the `TD-CI-\d{3}` family is in use but unregistered in `NAMING_STANDARD.md` s2. Decides nothing; authorizes no implementation; declares no phase exit. |
