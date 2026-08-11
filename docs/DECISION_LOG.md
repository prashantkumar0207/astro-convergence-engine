<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - contains accepted entries ADR-0001..0002 and proposed entries ADR-0003..0014, ADR-0018, ADR-0019, ADR-0020 (plus the ADR-0018 remote-CI evidence addendum, 2026-08-11) |
| Version | 0.6.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# Decision Log (ADR register)

Append-only. Entries are never edited after acceptance; they are superseded by later entries.
Template at the bottom. Numbering: ADR-XXXX, monotonically increasing.

RESERVED NUMBERS. ADR-0015 through ADR-0017 are reserved for the remaining Phase G commits
(0015 charter adoption, 0016 precedence hierarchy and agent workflow, 0017 certification
taxonomy). ADR-0014 was issued 2026-08-11 with Phase G commit 3. Phase G commit 1 delivered
G6 first by CEO sequencing decision, so ADR-0018 exists before ADR-0015..0017. The gap is a
reservation, not a lost entry. Numbers are obtained from this register BEFORE implementation, per ADR-0004.

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


## ADR-0018 - CI tiering and oracle environment reproducibility

- **Date:** 2026-08-10
- **Status:** PROPOSED - pending owner ratification (Q1). Per PROJECT_CONSTITUTION.md s11,
  AI output is proposal, not authority.
- **Context:** Two conditions violated `docs/VALIDATION_STANDARD.md` s2. (a) CI ran the
  default gate and two of the eleven independent holdout validators; nine validators, the
  legacy kernel gate and all eleven certification runners never ran in CI, and three of the
  four installed dependencies were unpinned, contravening s2 rule 4. (b) More seriously, the
  oracle environment was not reproducible from the repository. `PyJHora` 4.8.7 declares an
  EMPTY `Requires-Dist`, so its runtime imports fail one at a time on a clean machine and pip
  cannot resolve them. The certification artifacts recorded the package version and the Python
  version and nothing else, so an engineer holding only this repository could not recreate the
  environment that produced the eight oracle certifications. A certification whose environment
  cannot be recreated is a report, not proof.
- **Decision:**
  1. SPLIT CI into two jobs by external-oracle dependence, verified by inspection that no file
     under `engine/tests/` and no `validate_*.py` imports `jhora`. `hermetic` runs the default
     gate, ALL ELEVEN validators, the legacy kernel gate and the three non-oracle certification
     runners on Python 3.11 and 3.12. `oracle` runs the eight PyJHora runners on Python 3.11.
     The split is for reproducibility and outage isolation, never for speed: this change ADDED
     nine validators, the legacy gate and three certification runners to CI and removed
     nothing. `continue-on-error` is prohibited and absent; no step converts a failure into a
     warning; no validator or runner is skipped.
  2. RECORD the oracle environment identity in `certification/ORACLE_ENVIRONMENT.json`: OS and
     architecture, Python version and implementation, the CPython 3.11 linux x86_64 ABI
     constraint, PyJHora version with the explicit statement that it declares no dependencies,
     the six undeclared runtime dependencies (`numpy`, `geocoder`, `pytz`, `timezonefinder`,
     `geopy`, `python-dateutil`) and the iterative import-failure method by which they were
     discovered, the Swiss Ephemeris binding and reported library version, the `swetest`
     reference binary SHA-256 and build provenance, the ephemeris asset checksums, the lock
     file with its own SHA-256 and full 35-package closure, and the per-runner oracle
     invocation method including the D-007 Moon-injection methodology for Vimshottari and the
     per-event derived tolerances for transits with the ~20.5 arcsec oracle Sun divergence
     recorded NOT VERIFIED.
  3. PIN the oracle environment in `requirements-oracle.lock`: 35 packages, every one carrying
     a SHA-256, installed with `--require-hashes`. Self-contained by design so one file plus a
     clean interpreter reproduces the environment. A different Python minor version or platform
     requires its own lock and its own recorded identity and MUST NOT be obtained by relaxing
     hashes.
  4. ASSERT the identity at run time via `scripts/check_oracle_environment.py`, which fails
     loudly on any divergence in Python minor version, architecture, PyJHora version, any
     locked package version, or any ephemeris checksum.
  5. PROVE hermeticity rather than assert it. `scripts/ci_no_network.py` blocks outbound
     connection paths in-process without replacing the `socket.socket` class, because `ssl`
     subclasses it at import time and swapping the class yields a false failure. A negative
     control step proves the guard still blocks, so a guard that silently stopped working is
     caught rather than trusted. The guarantee is process-scoped and is documented as such.
  6. ADD `jsonschema==4.25.0` to `requirements.lock`. It is imported by
     `engine/knowledge/validator.py` and collected by `engine/tests/test_schema_validator.py`,
     so the default gate cannot run without it, yet it was absent from this file while
     `pyproject.toml` and `engine/requirements-lock.txt` both declared it. The three
     pre-existing pins are unchanged.
- **Consequences:** The oracle tier is bound to CPython 3.11 linux x86_64 until a second lock
  exists; the hermetic tier still runs 3.12. Hash pinning protects integrity, not availability:
  if an index removes a version the job fails loudly rather than installing something else,
  which is intended. The `governance` job specified in the Phase G plan is deliberately NOT
  added by this commit, because its primary check is the retired-identifier search that cannot
  pass until Phase G commit 2 (G1); adding it now would either break CI or require disabling
  its real checks. `scripts/certify_tier0.py` remains broken and untouched; its disposition is
  Phase G commit 6 (G7). NO calculation, varga, dasha, interpretation, BTR, validation,
  convergence, prediction, UI or ML work is included, and no certified logic was refactored.
- **Evidence:** Executed 2026-08-10 on the baseline tree at `1f861f6` in virtual environments
  created with no system site-packages. Oracle tier: hash-pinned install from
  `requirements-oracle.lock` alone, 35 packages, all hashes satisfied; all eight oracle
  certification runners PASS; regenerated artifacts differ from the committed artifacts in the
  `date` field ONLY, every gate value byte-identical. Hermetic tier: install from
  `requirements.lock` alone, 395 tests pass, all eleven validators pass, legacy gate 5 of 5,
  all three non-oracle certifiers PASS; the same set re-run under the network guard produces
  identical results; the negative control fails with `NoNetworkError` and exit code 1.
  `scripts/check_oracle_environment.py` returns 0 in the reproduced environment and 1 in a
  non-matching one. Specification: `docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md`.

---

## ADR-0018 EVIDENCE ADDENDUM - remote CI validation (2026-08-11)

- **Status:** ADDITIVE EVIDENCE. This addendum does NOT edit ADR-0018 above; that entry and its
  original evidence paragraph stand unmodified as dated record. ADR-0018 remains PROPOSED.
- **Context:** ADR-0018's original evidence was entirely local: clean-environment reproduction
  inside the container that authored the lock. The stated purpose of G6 was to prove the oracle
  environment reproducible OUTSIDE that sandbox, so the decision was not fully evidenced until the
  workflow ran on foreign hardware.
- **New evidence:** The `engine-ci` workflow executed on GitHub-hosted runners for commit
  `a460ba2b7e4eac55f8ac2f51b9e9eb9a35607fda` on branch `phase-g-governance`. Reported results:
  `hermetic` PASS on Python 3.11; `hermetic` PASS on Python 3.12; `oracle` PASS; overall workflow
  SUCCESS; `oracle-certification-evidence` artifact produced. `requirements-oracle.lock` therefore
  installed under `--require-hashes` on foreign hardware, the environment identity assertion passed
  there, and all eight oracle certification runners passed there. The predicted wheel-hash
  portability risk did not materialize. No hash was relaxed, no dependency version changed, and the
  lock was not regenerated.
- **Evidence class, stated exactly:** CEO_REPORTED. These remote results were observed by the
  CEO/technical auditor and reported to the builder. The builder has no network access to the
  Actions API and did NOT independently observe them. Run URL, run id, runner image and pip version
  were not supplied and are recorded as null rather than guessed. Per this register's own
  anti-circularity discipline, a PASS without a resolvable run identifier is weaker evidence than
  the project standard requires, and completing it by additive amendment remains an open item.
- **Determination:** G6 = PASS, on CEO authority, 2026-08-11. This is a REPRODUCIBILITY and
  INFRASTRUCTURE determination only. It certifies no calculation, promotes no component's
  certification level, and is not a C4 or C5 claim about any astrological method.
- **Technical debt recorded, not fixed:** TD-CI-001 GitHub Actions Node.js 20 deprecation warnings
  (non-blocking; the G6 commit must not be altered merely to silence them); TD-CI-002 oracle tier
  bound to CPython 3.11 linux x86_64, never to be resolved by relaxing hashes; TD-CI-003
  `scripts/certify_tier0.py` still broken, disposition belongs to Phase G commit 6 (G7).
- **Machine-readable record:** `certification/G6_REMOTE_CI_VALIDATION.json`. Human-readable record:
  `reports/G6_COMPLETION_RECORD.md`. Specification update: `docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md`
  section 7.1, version 1.1.0.
- **State:** `phase-g-governance` is NOT merged into `main`. `main` remains at `1f861f6`. Phase G
  commit 2 (G1) has not started and awaits CEO approval.

---

## ADR-0014 - Completion of the ADR-0004 identifier rewrite; varga pinning parity

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1). Per PROJECT_CONSTITUTION.md s11, an
  AI-written entry cannot be Accepted by its author.
- **Context:** ADR-0004 retired ten provisional plan identifiers and stated that module
  docstrings, certification runners, certification artifacts and pinning tests were updated to
  the compliant `ADR-\d{4}` numbers. Commit `8a5d56e` claimed the rewrite covered "every
  reference ... across 61 files" and that "all eleven certification artifacts were regenerated
  by their own runners". `reports/ALIGNMENT_REVIEW.md` s8 repeated the completeness claim.
  Independent audit on 2026-08-10 found the claim false for the varga family. `git log --all
  -S "ADR-0009" -- engine/astrology/varga_d3.py` returns no commits: the compliant number was
  never written into those modules at all. **38 tracked files carried retired identifiers in 70
  occurrences**: `ADR-VARGA-D3-001` 14, `ADR-VARGA-D12-001` 12, `ADR-VARGA-D7-001` 11,
  `ADR-VARGA-D30-001` 10, `ADR-VARGA-D2-001` 10, `ADR-CONVENTION-001` 4, `ADR-KP-001` 3,
  `ADR-DASHA-001` 2, `ADR-TRANSIT-001` 2, `ADR-ASPECT-PAR-001` 2. Meanwhile README.md and this
  register cited ADR-0009 through ADR-0012 for the same artifacts, so documentation and
  artifacts disagreed. Recorded as audit finding B-3, severity MEDIUM: zero calculation impact,
  but a traceability defect inside the very phase whose purpose was traceability.
- **Decision:**
  1. COMPLETE the rewrite. Replacement map: `ADR-VARGA-D3-001` to ADR-0009;
     `ADR-VARGA-D12-001` to ADR-0010; `ADR-VARGA-D7-001`, `ADR-VARGA-D30-001` and
     `ADR-VARGA-D2-001` to ADR-0011; `ADR-CONVENTION-001` to ADR-0012.
  2. RECORD supersession in STRUCTURED FIELDS ONLY, not in free text. Each of the five varga
     runners emits `"supersedes_provisional_id"` beside `"adr"`, and
     `scripts/certification_support.py` renders a matching line into the human-readable report
     when and only when that key is present. Writing the supersession inline in docstrings was
     considered and REJECTED: it would reintroduce the retired strings across the tree and make
     the zero-unauthorised-occurrence requirement unverifiable. Traceability is stronger as a
     queryable field than as prose.
  3. PRESERVE the two legitimate citations. `docs/DECISION_LOG.md` (this register, 10
     occurrences in the ADR-0004 retirement list and the ADR-0006/0009/0010/0011/0012 titles)
     and `reports/ALIGNMENT_REVIEW.md` (1 occurrence in its dated body) cite the retired
     identifiers AS retired and are unchanged.
  4. CLOSE the pinning asymmetry. Only D3 and D12 asserted `report["adr"]`, while KP,
     Vimshottari, transits, drishti and sign convention all did. D2, D7 and D30 had no
     certification pinning test at all, which is why the batch commit's identifiers went
     uncaught. Add `test_varga_d2_certification.py`, `test_varga_d7_certification.py` and
     `test_varga_d30_certification.py`; every varga pinning test now asserts both `adr` and
     `supersedes_provisional_id`, plus that varga's defining behaviour (D2's two-sign output
     space, D7's full-zodiac coverage, D30's exclusion of the luminary signs).
  5. ENFORCE it mechanically. The `governance` CI job deferred by ADR-0018 lands here, running
     `scripts/check_retired_identifiers.py`: an exact-string search for all ten retired
     identifiers and a family-regex search for any `ADR-` token not followed by exactly four
     digits, against a declared allowlist. The family regex is the operative one, because the
     defect class is an unauthorised identifier family, not these ten strings.
  6. CORRECT the false completeness claim WITHOUT rewriting evidence.
     `reports/ALIGNMENT_REVIEW.md` receives a dated superseding note at its head, in the exact
     pattern already used by FINDINGS_MATRIX.md; its body is untouched. Commit `8a5d56e`'s
     message is wrong and cannot be corrected: rewriting published history is forbidden, so
     this entry is the corrective record.
- **Consequences:** Zero calculation impact, proven rather than asserted (see Evidence).
  Artifacts for the six non-varga certifications were deliberately NOT committed: regenerating
  them changed only their run date, and committing date churn for artifacts this ADR did not
  touch would obscure the diff. That restoration also PROVES the shared `_render` change is
  inert where the new key is absent. Future phases obtain an ADR number from this register
  BEFORE implementation, per ADR-0004, and the governance job now fails the build if a
  non-compliant identifier family appears again.
  **Corrected count:** an earlier report of this finding said 37 files. The verified figure is
  38; the occurrence total of 70 was correct. The discrepancy was an arithmetic error in the
  report, not a change in the tree.
- **Evidence:** Before-state inventory of 38 files and 70 occurrences reproduced by `git grep`
  over `git ls-files`. After remediation both searches return zero occurrences outside the
  declared allowlist. All eleven certification runners regenerate PASS. The five varga
  artifacts differ from their prior versions in exactly three fields (`adr`,
  `supersedes_provisional_id`, `date`) and five lines each; every gate value is byte-identical,
  including the gate D `d9_sweep_sha256` = `ca444f10...` and `d10_sweep_sha256` = `78cd000f...`
  present before and after. Default gate rises from 395 to 404 tests, the increase being
  exactly the nine new test functions added by decision 4 (three per artifact gate). Legacy gate 5 of 5. Eleven
  independent validators PASS. Calculation-impact fingerprints over a 51,429-point dense sweep
  plus 1e-9 boundary neighbourhoods are identical to a pristine worktree of `1f861f6` for D9
  sign and longitude, D10 sign and longitude, and all five registry vargas.

---

## ADR-0019 - Product identity: multi-domain Jyotisha platform, not a natal application

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** The repository's specifications, including H1 through H8 written earlier the same day,
  assumed the subject of analysis is a person with a birth chart. The owner clarified that the
  long-term product is a multi-domain Jyotisha intelligence platform spanning Jataka, Varshaphal,
  Muhurta, Prashna and Mundane astrology. Four of those five domains violate the person-plus-birth-
  chart assumption. Left unrecorded, that assumption would harden into the entity model, the evidence
  model and the convergence layer, where it would be expensive to remove.
- **Decision:**
  1. RECORD the product identity: a transparent, evidence-driven, multi-domain Jyotisha intelligence
     platform that evaluates analytical methods against historical evidence, measures consistency and
     confidence, and provides qualified future-oriented analysis through convergence of multiple
     systems. The USP is unchanged: PAST to TEST to LEARN to CONFIDENCE to FUTURE.
  2. GENERALISE the core subject from person to **astrological entity**, specified in
     `docs/H0_ENTITY_MODEL_SPEC.md`, numbered zero because H1 through H8 depend on it.
  3. RECORD that entities are NOT uniform. Four structurally different shapes exist: origin moment
     (person, country, company), derived moment (Varshaphal, from a parent chart), query moment
     (Prashna, where the moment is known by construction), and no entity at all (General Muhurta,
     which evaluates a candidate moment for a purpose). Generalising "person" to "entity" is necessary
     but not sufficient, because these differ in which operations are valid.
  4. RECORD that General Muhurta **inverts the pipeline**: every other domain takes a moment and
     produces analysis, while General Muhurta takes a purpose and a window and searches for moments.
     It is the only domain requiring an optimiser, and its output is a ranked set with reasons.
  5. SCOPE BTR by entity shape and gate it on origin certainty. BTR MUST refuse where the origin
     moment is `documented`. Rectifying against a registry-timestamped incorporation would be the
     prohibited reasoning "prediction failed, therefore the time is wrong" in another form.
  6. ADD entity, domain and chart reference to the evidence model. The chart reference exists to make
     **shared-origin detection** possible: Varshaphal derives from the natal chart, so natal and
     Varshaphal agreeing is one source agreeing with itself through a transformation. Without it,
     convergence would systematically overstate confidence in exactly the combination the product most
     wants to present.
  7. ADD the cross-domain axis to convergence, with the requirement that it be able to state whether
     agreeing sources **could have disagreed**, and with an explicit multiple-comparison discipline for
     mundane validation, where large samples of publicly dated events make chance agreement likely.
  8. DECLARE domain isolation as a second axis orthogonal to school isolation. Tajika aspects are not a
     variant of Parashari drishti; Mudda dasha is not a variant of Vimshottari; Prashna rules are not
     natal rules. Terminological overlap is not methodological identity.
- **Consequences:** No code, no calculation change, no new domain implementation. `docs/H0_ENTITY_MODEL_
  SPEC.md` and `docs/PLATFORM_DOMAIN_ARCHITECTURE.md` are added; H1, H4, H7 and H8 receive additive
  amendment sections with their prior content unmodified. Two capability gaps are recorded that were
  not previously visible: **panchanga** (tithi, vara, nakshatra, yoga, karana) is a calculation-layer
  capability that does not exist, and **rising and setting** does not exist either, which blocks Rahu
  Kalam, Yamaganda and Gulika and is genuine Tier-0 astronomical work with its own high-latitude edge
  cases. Verified: `engine/` contains zero occurrences of tithi, vara, karana, panchanga, rahu kalam,
  yamaganda, gulika, muhurta, varshaphal, muntha, varshesh, saham, tajika, prashna or mundane.
  Audit finding H-02 is elevated in priority: transit event instants are misclassified by the engine's
  own classifier at 17 percent of sign ingresses and 43 percent of nakshatra ingresses, and Muhurta is
  precisely the question "which tithi and nakshatra hold at this candidate moment", evaluated over many
  candidates of which the marginal ones sit near boundaries. `engine/transits/events.py` `returns()`
  already implements longitude return and would serve solar return, but appears in no certification
  artifact. Mudda dasha inherits the whole depth requirement in `docs/DASHA_CERTIFICATION_ROADMAP.md`.
  Development priority is unchanged: governance and certification, then calculation confidence, then
  evidence, interpretation, convergence, and domain modules last.
- **Evidence:** `docs/PLATFORM_DOMAIN_ARCHITECTURE.md`, `docs/H0_ENTITY_MODEL_SPEC.md`, additive
  sections in H1 s9, H4 s8, H7 s11 and H8 s10, and the capability-absence search recorded above.

---

## ADR-0020 - Multi-domain platform: ten ratified architecture decisions

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1). Recorded on CEO direction following
  review of ADR-0019. Supersedes no entry; resolves several questions ADR-0019 left open.
- **Context:** ADR-0019 recorded the multi-domain product identity and deliberately left the
  consequent architecture questions open. The CEO reviewed the findings and issued ten decisions.
  This entry records them, records what they resolve, and records the conflicts and residues they
  create, per PROJECT_CONSTITUTION.md s3.2 which forbids resolving ambiguity silently.
- **Decision:**

  **D1. Entity architecture: a common abstraction with specialised subject types.** NOT one
  undifferentiated generic entity. A shared `AstrologicalSubject` and domain abstraction, with
  specialised types where semantics differ: Person, Organisation/Company, Geographic/National
  entity, Event, Question. Shared infrastructure without pretending all subject types have
  identical chart semantics. RESOLVES the open question in `docs/H0_ENTITY_MODEL_SPEC.md` s7,
  "whether shapes are one type or four", in favour of a common abstraction plus specialisation.

  **D2. Panchanga and rise/set are Tier-0 foundational calculation capabilities.** Not ad-hoc
  logic inside Muhurta. They will support Muhurta, Prashna, Mundane, panchanga functionality,
  Rahu Kalam, Yamaganda, Gulika and related time-window calculations. They require INDEPENDENT
  CERTIFICATION before any dependent production module relies on them.

  **D3. Mundane multi-chart model: no silent chart selection.** Where multiple historically
  defensible origin charts exist for a country, company or institution, the architecture must
  permit entity to candidate chart set, with provenance per chart, independent analysis per
  chart, comparison, and explicit disagreement. The system must be capable of stating that
  different defensible charts produce different conclusions. RESOLVES the second open question in
  `docs/H0_ENTITY_MODEL_SPEC.md` s7 in favour of analysing across candidates and surfacing
  disagreement.

  **D4. Convergence dependency model: five evidence relationship classes.** Convergence MUST NOT
  treat every agreeing output as independent. The evidence model must preserve dependency and
  provenance relationships, and the convergence engine must distinguish and explain to the user:
  INDEPENDENT, DERIVED, SHARED-ORIGIN, CORRELATED, and CONFLICTING evidence. Natal to Varshaphal
  is a derived relationship and cannot automatically count as two confirmations. EXTENDS
  `docs/H4_EVIDENCE_MODEL_SPEC.md` s8 and `docs/H8_CONVERGENCE_SPEC.md` s10, which specified
  shared-origin detection only.

  **D5. H-02 is a potential blocker for Muhurta and must be independently reproduced.** Before
  any production Muhurta implementation, the reported transit ingress and nakshatra boundary
  classification defect must be independently reproduced, NOT assumed correct because it appears
  in an audit. If confirmed, the underlying calculation is repaired and certified before
  dependent Muhurta work.

  **D6. Preferred domain roadmap**, subject to future CEO review:
  FOUNDATION, JATAKA, EVIDENCE, INTERPRETATION, CONVERGENCE, VARSHAPHAL, MUHURTA, PRASHNA,
  MUNDANE. BTR remains an independent evidence-driven capability and MUST NOT become a
  prerequisite for convergence or a universal explanation for prediction failure.

  **D7. Muhurta: both modes reserved.** General Muhurta may operate without birth details.
  Personalised Muhurta may incorporate natal chart, relevant vargas, dashas, transits, Moon
  factors, Tara Bala, Chandra Bala, purpose-specific rules and historical evidence where
  appropriate. Muhurta is fundamentally a SEARCH AND RANKING problem over candidate moments and
  MUST expose its search window, candidate space and selection methodology.

  **D8. Varshaphal is a distinct annual-analysis domain**, not another natal interpretation
  layer: solar return, Varsha Lagna, Muntha, Varshesh, Tajika aspects, Sahams, Mudda Dasha, each
  subject to later certification.

  **D9. Prashna is a question-driven domain** requiring no birth details: question plus timestamp
  plus location to Prashna context and chart, applicable rules, analysis, evidence, qualified
  answer.

  **D10. The repository is the permanent record.** These decisions are recorded here rather than
  relied upon from conversation.

- **Consequences and residues, stated rather than smoothed:**

  1. **The Tier-0 lock scope is NOT retroactively widened by D2.** ADR-0005 fixes the lock scope
     as the astronomical kernel, ephemeris handling, frame, calculation profiles, houses,
     sidereal positions, the JD/time pipeline, and the certified D9/D10 mathematics. Panchanga
     and rise/set are new capabilities that will require certification at Tier-0 depth; the
     existing lock covers neither and MUST NOT be read as if it did.
  2. **A layering nuance worth recording.** Rise/set is astronomy proper: ephemeris plus horizon
     geometry, with genuine high-latitude edge cases where the concept degrades or fails.
     Panchanga elements are deterministic CLASSIFICATION over astronomical outputs, structurally
     closer to a varga than to the kernel. Both are foundational and both need independent
     certification, which is the substance of D2 and is not in question. Whether they occupy the
     same tier label is a precision question for the eventual taxonomy work, and it is recorded
     here rather than decided.
  3. **Vara depends on rise/set.** The Jyotisha weekday runs sunrise to sunrise, not midnight to
     midnight, so vara cannot be computed from the civil calendar and inherits every rise/set
     edge case. Rahu Kalam, Yamaganda and Gulika are eighth-part divisions of the day and night
     and carry variant assignment tables across traditions. Each variant is a decision to be
     recorded, never chosen silently, exactly as the varga variants are.
  4. **Four of D4's five classes are structurally derivable; one is not.** INDEPENDENT, DERIVED,
     SHARED-ORIGIN and CONFLICTING follow from provenance and chart references recorded at
     evidence-creation time. CORRELATED is a MEASURED property: knowing that two rules or systems
     tend to agree beyond their structural relationship requires evidence accumulated in the
     historical ledger. The taxonomy therefore has two different epistemic sources, and the
     measured class cannot be populated until the ledger exists and has a defensible sample.
  5. **D6 partially answers Q8 and does not close it.** Open question Q8 asks for ratified
     roadmap phases WITH entry and exit criteria. D6 supplies the order; it supplies no criteria.
     It also supersedes in practice the sequencing in `docs/PROJECT_BACKLOG.md` that placed Phase
     1 Core Intelligence before Phase 2 Astrology Systems, which is ADR-0013 conflict 7. Whether
     Q8 is now closed, or remains open pending criteria, is an owner decision.
  6. **D5's evidence class, stated plainly.** The H-02 percentages, two of twelve Sun sankranti
     instants and twelve of twenty-eight Moon nakshatra ingress instants, were produced by a
     delegated read-only audit and relayed in
     `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`. The builder did not personally re-execute
     that measurement. The CEO's instruction to reproduce independently is therefore correct on
     the evidence as it stands, and this entry records the gap rather than defending the figure.
  7. **D7's search-methodology exposure aligns Muhurta with BTR.** Both evaluate many candidates
     and report the best, so both are bound by the discipline in `docs/H7_BTR_SPEC.md` s11 and
     `docs/PLATFORM_DOMAIN_ARCHITECTURE.md` s8: record the search space and the candidate count,
     and never present "best of ten thousand" as "strongly indicated" without its denominator.
  8. **D3 has no supporting model today.** Nothing in `engine/models/` represents a subject, let
     alone a subject with competing charts. D3 is a requirement on a layer that does not exist.
  9. **NO IMPLEMENTATION IS AUTHORISED.** Not panchanga, rise/set, Muhurta, Varshaphal, Prashna,
     Mundane, BTR, interpretation or convergence. Development priority is unchanged: governance
     and certification, calculation confidence, evidence, interpretation, convergence, domains.

- **Evidence:** `docs/PLATFORM_DOMAIN_ARCHITECTURE.md` s13, `docs/H0_ENTITY_MODEL_SPEC.md` s10,
  `docs/H4_EVIDENCE_MODEL_SPEC.md` s10, `docs/H8_CONVERGENCE_SPEC.md` s12, and
  `certification/ENGINE_CAPABILITY_INVENTORY.json`. Default gate 404 passed and the identifier
  governance gate PASS at the time of recording, with zero changes under `engine/`, `legacy/`,
  `scripts/`, any validator or any certification artifact.

---

## ADR template (copy, do not edit above the line)

## ADR-XXXX - <title>
- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-YYYY
- **Context:** <forces, constraints, problem>
- **Decision:** <the binding choice, stated imperatively>
- **Consequences:** <positive, negative, follow-up obligations>
- **Evidence:** <links to validation runs where applicable>
