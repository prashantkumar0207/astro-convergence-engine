<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - contains accepted entries ADR-0001..0002 and proposed entries ADR-0003..0012 |
| Version | 0.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-09 |
| Review cadence | TBD |

# Decision Log (ADR register)

Append-only. Entries are never edited after acceptance; they are superseded by later entries.
Template at the bottom. Numbering: ADR-XXXX, monotonically increasing.

---

## ADR-0001 - Canonical repository structure
- **Date:** 2026-07-11
- **Status:** Accepted
- **Context:** A long-term project needs a stable, minimal top-level layout that separates
  normative documents, deterministic engine code, governed knowledge, non-normative research,
  verification, tooling and product code.
- **Decision:** Adopt exactly these top-level folders: `docs/ engine/ knowledge/ research/
  tests/ tools/ app/`, with dependency rules as recorded in MASTER_ARCHITECTURE.md section 4.
- **Consequences:** New top-level folders require a superseding ADR. All ambiguous
  foundational items are tracked in OPEN_QUESTIONS.md rather than assumed.

---

## ADR-0002 - Foundation additions per M1 repository audit
- **Date:** 2026-07-11
- **Status:** Accepted
- **Context:** External M1 audit (reviewer: ChatGPT) required five additions before M1
  lock: PROJECT_CONSTITUTION.md, /examples, /assets, LICENSE placeholder, SECURITY.md.
  ADR-0001 requires a superseding ADR for any new top-level folder.
- **Decision:** Add top-level `examples/` and `assets/` (illustrative and media layers -
  neither may be a runtime dependency of engine/knowledge/app), add the constitution as
  the highest governing document, add a no-grant LICENSE placeholder pending Q7, and add
  SECURITY.md with contact pending Q1. No existing folder, specification or standard is
  modified.
- **Consequences:** Canonical top-level set is now: docs, engine, knowledge, research,
  tests, tools, app, examples, assets. README layout table extended accordingly.
- **Evidence:** M1_REPOSITORY_AUDIT_FIXES.md (audit input, retained with project records).

---

## ADR-0003 - Structural reconciliation: restoration, deletions, and undeclared folders

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1). Per PROJECT_CONSTITUTION.md s11,
  AI output is proposal, not authority; this entry is written by the AI builder and is not
  Accepted until the named owner ratifies it.
- **Context:** The working tree has diverged from the top-level set frozen by ADR-0001 and
  amended by ADR-0002, in both directions, with no superseding ADR. Specifically: (a) commit
  c50178f removed `knowledge/`, `schemas/`, `examples/`, `tools/`, `research/`, `assets/`;
  (b) commit 5ae8ee7 removed `app/`; (c) `tests/` never existed at top level, its content
  living at `engine/tests/`; (d) six undeclared top-level folders exist -- `certification/`,
  `engineering/`, `legacy/`, `reports/`, `scripts/`, `specs/`; (e) `knowledge/` and `tools/`
  names are additionally used *inside* `engine/`. ADR-0001 governs addition explicitly and is
  silent on removal; the safe reading, given the word "exactly" and ADR-0002's "No existing
  folder ... is modified", is that removal also requires a superseding ADR.
- **Decision:**
  1. RESTORE `knowledge/`, `schemas/`, `examples/`, `tools/`, `research/`, `assets/` to their
     exact pre-deletion contents. Done: 22 files, every blob hash identical to c50178f^.
     Rationale: these are the substrate of PROJECT_BACKLOG.md Phase 1, not product remnants;
     `schemas/question.schema.json` is the declared normative artifact of
     CANONICAL_QUESTION_SCHEMA.md; three surviving governing documents reference these paths.
  2. CONFIRM the removal of `app/` as deliberate, and record the consequent disposition
     change to audit finding F-22. F-22 was recorded as DEFERRED WITH JUSTIFICATION on the
     grounds that replacement required the API layer. The actual resolution was deletion,
     because the stub displayed horoscope values not produced by the engine, which F-22
     itself called release-blocking. A frontend is rebuilt at PROJECT_BACKLOG.md Phase 5 on
     the API layer. FINDINGS_MATRIX.md F-22 is amended accordingly.
  3. DECLARE the six existing undeclared top-level folders as sanctioned, describing what
     each is for, rather than leaving the tree silently non-compliant: `certification/`
     machine-readable certification artifacts; `engineering/` the engineering constitution;
     `legacy/` the certified legacy kernel retained as migration reference per
     LEGACY_KERNEL_MIGRATION.md; `reports/` historical certification reports and raw
     reference outputs; `scripts/` certification runners and the legacy pipeline; `specs/`
     validation protocol and charter documents.
  4. RECORD that `tests/` as a top-level folder is superseded in practice by `engine/tests/`
     (pytest.ini testpaths), and that VALIDATION_STANDARD.md s1 and NAMING_STANDARD.md s5
     text referring to `tests/` is therefore stale and flagged for correction.
- **Consequences:** The top-level set becomes: `docs/ engine/ knowledge/ research/ tools/
  examples/ assets/ certification/ engineering/ legacy/ reports/ scripts/ specs/`. `app/` is
  absent by decision and returns at Phase 5. `tests/` is absent by supersession. Any further
  structural change still requires a superseding ADR. NAMING_STANDARD.md s5's closed list and
  its conformance-sweep claim require updating, and the sweep needs re-running.
- **Evidence:** Restoration commit on branch `reconcile-v1`; blob-level diff showing zero
  differences against c50178f^; `python3 tools/career_validate.py` -> 61 records, 0 findings,
  exit 0; default gate 372 passed, unchanged.

---

## ADR-0004 - Identifier family correction: provisional plan identifiers superseded

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** Eight development phases carried out on 2026-08-08/09 cited decision
  identifiers of the form `ADR-KP-001`, `ADR-DASHA-001`, `ADR-TRANSIT-001`,
  `ADR-VARGA-D3-001`, `ADR-VARGA-D12-001`, `ADR-VARGA-D7-001`, `ADR-VARGA-D30-001`,
  `ADR-VARGA-D2-001`, `ADR-ASPECT-PAR-001`, `ADR-CONVENTION-001`. These appear in module
  docstrings and in every certification artifact. None exists in this register or in the root
  engineering register. NAMING_STANDARD.md s2 fixes the decision family as `ADR-\d{4}`,
  width 4, issuer `DECISION_LOG.md`, and requires that any new ID family have a governing
  section, a decision-log entry and a uniqueness check. None of those three steps was taken,
  so the identifiers constitute an unauthorised parallel family.
- **Decision:** Treat those ten strings as PROVISIONAL PLAN IDENTIFIERS, not members of the
  ADR family. Issue compliant entries ADR-0005..ADR-0012 below, each recording the
  provisional identifier it supersedes. Update module docstrings, certification runners,
  certification artifacts and pinning tests to cite the compliant identifier. The provisional
  strings are retired and MUST NOT be reused.
- **Consequences:** Documentation-only churn across engine modules, scripts and artifacts; no
  calculated value changes, which is proven by cross-commit SHA-256 output sweeps. Future
  phases obtain an ADR number from this register BEFORE implementation, per s14
  ("specifications first, code second, claims last").

---

## ADR-0005 - Current-engine Tier-0 lock

- **Date:** 2026-08-09 (recording a lock established 2026-08-08 at commit bfae088)
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** PROJECT_CONSTITUTION.md s12 defines Locked as requiring all four of: a written
  spec or frozen profile; a reproducible verification run per VALIDATION_STANDARD; machine-
  readable results and a human-readable report from that same run, agreeing; and a decision
  log entry recording the lock, its version and its evidence. The current engine's Tier-0 lock
  was declared in CURRENT_ENGINE_CERTIFICATION_STATUS.md and
  certification/CURRENT_ENGINE_LOCK.json with no entry in either decision register, so
  condition 4 was unmet and the lock was, in s12's words, "at most, 'reported'".
- **Decision:** Record the lock. Scope: the astronomical calculation kernel (ephemeris
  handling, frame, calculation profiles, houses, sidereal positions, JD/time pipeline) and the
  certified D9/D10 divisional mathematics. Version: engine 0.3.0. Ratified profiles:
  `parashari_lahiri` (SIDM 1) and `kp_krishnamurti` (SIDM 5), per the owner sign-off recorded
  2026-08-08. Frozen numerical authority and tolerances per root D-001..D-004.
- **Consequences:** Changes inside the lock scope require the same discipline that established
  it and a further ADR. Note the still-open gap: condition 3 is only partly met, because the
  human-readable report is hand-authored rather than generated by the same run. ADR-0012
  addresses that.
- **Evidence:** `scripts/certify_current_engine.py`, regenerated from scratch:
  528 comparisons across the frozen 11-case holdout under both profiles, max planet error
  0.000179 arcsec, max ascendant error 0.000176, max cusp error 0.000180, zero Moshier
  fallbacks; `certification/current_engine_certification.json`; default gate 372 passed;
  legacy gate 5/5.

---

## ADR-0006 - KP lordship chain layer (supersedes provisional ADR-KP-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** legacy/kp.py held the certified KP interval mathematics. LEGACY_KERNEL_
  MIGRATION.md requires per-module migration with validation against the certified legacy
  implementation before any retirement, and root D-003 sets zero categorical tolerance for
  SL/NL/SB/SS.
- **Decision:** Add an isolated `engine/kp/` package providing exact-rational lordship chains
  and KP fact charts under the `kp_krishnamurti` profile only. Preserve the legacy
  `Decimal(str(x))` conversion rule and `[start, end)` interval ownership verbatim as the KP
  layer's documented numeric contract, which deliberately differs from the engine-wide
  1e-10 promote-up convention. Assert the mean node. Retire nothing from `legacy/`.
- **Consequences:** KP significators, four-step, ruling planets and horary remain out of
  scope; root D-008 continues to require a frozen, independently audited specification for
  KP_SIGNIFICATOR_V1 before that tier. LOCK_MANIFEST.json requires a KP_CHAIN entry.
- **Evidence:** `certification/KP_CHAIN_V1_certification.json`; equivalence against
  legacy/kp.py over a 51,429-point dense sweep plus 19,679 boundary and ULP points with zero
  mismatches; 11-case chart holdout, 275 chain comparisons, max longitude delta 0.0 arcsec;
  200/200 transcribed fixture fields; independent validator with an in-file flat-table
  reference. legacy/ verified unmodified by diff.

---

## ADR-0007 - Vimshottari dasha layer (supersedes provisional ADR-DASHA-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** Dasha year length is a genuinely open classical convention (mean sidereal,
  true sidereal, tropical, savana, lunar), and the choice moves period boundaries by days to
  months over a lifetime. No in-repository oracle exists for dashas.
- **Decision:** Add an isolated `engine/dasha/` package computing Vimshottari maha, antar and
  pratyantar periods in exact rational arithmetic. Make year length an EXPLICIT field on a
  DashaProfile with no hidden default; certify V1 against the mean sidereal year
  (91314091/250000 days exactly) as documented by the external oracle. Seed school-explicitly
  from a `parashari_lahiri` or `kp_krishnamurti` snapshot and record which in provenance.
  Certify depths 1-3 only.
- **Consequences:** Other dasha systems, deeper levels and other year conventions are
  non-claims, each requiring its own ADR. The Vimshottari lord and year tables now exist in
  `legacy/kp.py`, `engine/kp/tables.py` and `engine/dasha/tables.py`; that duplication is a
  deliberate choice of school isolation over KNOWLEDGE_STANDARDS.md single-source-of-truth,
  enforced by a cross-consistency test rather than a cross-import, and is recorded as an open
  standards conflict for owner adjudication (see ADR-0013).
- **Evidence:** `certification/VIMSHOTTARI_V1_certification.json`; 1,782 dasha-bhukti rows
  across 11 cases and both profiles with zero lord mismatches and max start delta 1.4e-9 days,
  using the oracle's own Moon to isolate timeline mathematics from oracle astronomy per root
  D-007; independent closed-form validator over 1,081 Moon cases.

---

## ADR-0008 - Transit event layer (supersedes provisional ADR-TRANSIT-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Decision:** Add an isolated `engine/transits/` package finding longitude-crossing events
  by station-aware bisection on the certified position pipeline, so event instants inherit the
  Tier-0 certification. Cover sign and nakshatra ingresses, returns and natal conjunctions,
  with retrograde multiplicity reported and direction flagged, plus a documented tangent rule
  for station contacts. Provide a natal-relative view that refuses mixed-profile comparison.
  Event-time guarantee 1e-6 day; residual bound 1e-4 arcsec; sampling bounded by documented
  per-body maximum speeds times a safety factor of four.
- **Consequences:** Aspect-system events, dasha-transit convergence and topocentric variants
  are non-claims.
- **Evidence:** `certification/TRANSIT_V1_certification.json`; residual battery 74 events at
  max 2.1e-5 arcsec; completeness equal to independent fine-grid scans including a retrograde
  Mercury triple crossing with direction sequence +1/-1/+1; 24 sankranti anchors against the
  external oracle under per-event tolerances derived from the measured ~20.5 arcsec oracle Sun
  divergence, whose cause is recorded NOT VERIFIED, per root D-007; independent
  scan-plus-interpolation validator over 86 events.

---

## ADR-0009 - Generic Varga framework enters production use; D3 Drekkana (supersedes provisional ADR-VARGA-D3-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** The Generic Varga framework existed as certified infrastructure with an empty
  registry. The governing constraint is that it must not replace the certified D9/D10
  production modules without an explicit architectural decision, a full equivalence proof and
  regression certification.
- **Decision:** Register the first production varga, D3 Drekkana (Parashara variant: the
  sign itself, the 5th, the 9th), under the `parashara` school key. Do NOT migrate D9 or D10;
  they remain hard-wired to their certified modules and the registry continues to refuse those
  divisions by contract. Express the rule as frozen `SegmentVargaRule` literals, because the
  framework's `CyclicVargaRule` steps one sign per division and cannot express the drekkana's
  four-sign jumps.
- **Consequences:** Other drekkana variants are non-claims. Four Phase A/B tests that asserted
  an empty registry were replaced, with the reason documented inline.
- **Evidence:** `certification/VARGA_D3_V1_certification.json`; 36-cell table verified against
  a second independent transcription and a trine re-derivation; 51,429-point sweep with zero
  mismatches; full ULP boundary battery; external oracle 3,600/3,600; registration proven
  non-invasive by 53,019-point SHA-256 sweeps of D9/D10 identical before and after;
  independent by-name validator.

---

## ADR-0010 - D12 Dwadasamsa; certified-registry constant (supersedes provisional ADR-VARGA-D12-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Decision:** Register D12 Dwadasamsa (twelve 2.5-degree parts from the sign itself,
  forward) as frozen `CyclicVargaRule` literals, putting the framework's second and last rule
  contract into production use. Introduce
  `engine.astrology.CERTIFIED_PRODUCTION_VARGAS` as the single source of truth for the
  sanctioned registry state, and reconcile every registry-state assertion to it.
- **Consequences:** Every future varga updates one constant; registry-state tests follow it
  automatically.
- **Evidence:** `certification/VARGA_D12_V1_certification.json`; 24-cell table against a
  second transcription plus a full 144-cell target re-derivation; 51,429-point sweep, zero
  mismatches; ULP battery at all 144 boundaries; oracle 3,600/3,600; D9/D10 hashes unchanged;
  independent validator.

---

## ADR-0011 - D7 Saptamsa, D30 Trimsamsa, D2 Hora (supersedes provisional ADR-VARGA-D7-001, ADR-VARGA-D30-001, ADR-VARGA-D2-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Decision:** Register three further Parashara vargas: D7 Saptamsa (odd signs from the sign
  itself, even from the seventh, forward), D30 Trimsamsa (unequal tara-graha segments
  5/5/8/7/5 odd and reversed even, no luminaries), and D2 Hora (two 15-degree halves with a
  deliberately two-sign Leo/Cancer output space).
- **Consequences:** Named alternative variants for all three are non-claims. This commit
  registered three vargas together, which strains ENGINEERING_CONSTITUTION Principle 10
  (one logical change per commit) and the README's own "one at a time" rule; recorded here
  rather than left unstated.
- **Evidence:** Three certification artifacts; per varga a dual-transcribed table, a
  51,429-point sweep with zero mismatches, a ULP boundary battery, external oracle
  3,600/3,600, and an independent by-name validator; D30 additionally verified by a
  rulership-and-gender re-derivation; D2's two-sign output space pinned by test. A recorded
  numerical finding: D7's 30/7-degree widths are not binary-representable and six sweep points
  land one ULP below a boundary, where the locked promote-up convention governs; the
  independent references carry that tolerance explicitly.

---

## ADR-0012 - Parashari graha drishti; sign-convention enforcement (supersedes provisional ADR-ASPECT-PAR-001, ADR-CONVENTION-001)

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Decision (a), aspects:** Open `engine/parashari/` as the first school layer above the
  shared primitives and implement full (purna) graha drishti facts only: every graha aspects
  the seventh, Mars additionally the fourth and eighth, Jupiter the fifth and ninth, Saturn
  the third and tenth, by inclusive whole-sign counting. Exclude node-cast aspects from
  certified behaviour because traditions genuinely disagree, and record the variant rather
  than choosing silently. Fractional sputa drishti, Jaimini rashi drishti, Western aspects,
  yogas, strengths and interpretation are non-claims.
- **Decision (b), sign conventions:** Do NOT renumber. Every varga sign output is 0-based,
  including certified D9/D10 and all registry vargas; every rashi-level output is 1-based.
  Both are locked. Introduce an inert `Sign` value type with named constructors and accessors
  and no arithmetic, add opposite-convention accessors additively to every sign-carrying
  model, and declare every sign-typed field in `engine.astrology.sign_conventions` with a
  collected gate that fails on any undeclared field. Note that ARCHITECTURE_STATUS.md item 5
  said "unify"; this is an explicit substitution of that requirement, on the grounds that
  renumbering would reopen locked behaviour.
- **Consequences:** The convergence-layer prerequisite is satisfied in substance. The
  declaration gate prevents the convention debt from growing.
- **Evidence:** `certification/PARASHARI_DRISHTI_V1_certification.json` (84-pair exhaustive
  combinatorics, oracle 154 comparisons over the 11-case holdout with zero mismatches,
  independent name-counting validator) and
  `certification/SIGN_CONVENTION_V1_certification.json` (17 fields proven by discriminating
  witness across 192 real charts, 59,988 cross-layer checks, and non-invasiveness sweeps over
  54,697 points showing D9, D10 and all five registry vargas byte-identical to the prior
  commit).

---

## ADR-0013 - Open standards conflicts recorded for owner adjudication

- **Date:** 2026-08-09
- **Status:** PROPOSED - pending owner ratification (Q1). This entry RECORDS conflicts; it
  does not resolve them.
- **Context:** The 2026-08-08/09 work surfaced conflicts between governing documents that
  were, in practice, resolved in code without an ADR. PROJECT_CONSTITUTION.md s3.2 forbids
  resolving ambiguity silently, so each is registered here for decision.
- **Conflicts recorded:**
  1. `engineering/ENGINEERING_CONSTITUTION.md` Principle 3 (the only ACTIVE, non-DRAFT
     governing document, self-declared higher priority than implementation prompts) states
     knowledge must never be hardcoded into algorithms. Every new rule table is a Python
     literal, while `engine/knowledge/data/` exists and was not used. Either the principle
     yields for frozen classical rule tables, or the tables must move to knowledge assets.
  2. `docs/KNOWLEDGE_STANDARDS.md` single-source-of-truth versus school isolation: the
     Vimshottari tables exist in three places by deliberate choice.
  3. Three architecture documents place the knowledge layer in three incompatible positions,
     and the only one marked LOCKED (`docs/REPOSITORY_ARCHITECTURE.md`) is the only one that
     places prediction logic and interpretation inside knowledge, which every other document
     forbids. That lock also fails s12 condition 4.
  4. Open questions Q6 (may `engine/` read `knowledge/` at runtime) and Q9 (should the
     certified kernel be imported into `engine/`) were answered in practice, not by decision.
  5. Root `DECISION_LOG.md` (D-00x) and this register (ADR-000x) coexist with no stated
     precedence.
  6. Root D-008 names KP_SIGNIFICATOR_V1 as the next tier and was never superseded, while the
     2026-08-08/09 work spanned a much wider programme.
  7. `docs/PROJECT_BACKLOG.md` places Phase 1 Core Intelligence before Phase 2 Astrology
     Systems; the astrology systems were built first while all nineteen Phase 1 items remain
     not started.
- **Consequences:** None of these is resolved by this entry. Each requires an owner decision,
  and several require a superseding ADR once decided.


## ADR template (copy, do not edit above the line)

## ADR-XXXX - <title>
- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-YYYY
- **Context:** <forces, constraints, problem>
- **Decision:** <the binding choice, stated imperatively>
- **Consequences:** <positive, negative, follow-up obligations>
- **Evidence:** <links to validation runs where applicable>
