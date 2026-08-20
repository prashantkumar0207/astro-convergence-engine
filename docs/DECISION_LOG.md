<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACTIVE REGISTER. **ACCEPTED (38): ADR-0001, ADR-0002, ADR-0005 through ADR-0012, ADR-0015, ADR-0016, ADR-0017, ADR-0033 through ADR-0037, ADR-0039 through ADR-0042, ADR-0044, ADR-0045, ADR-0046, ADR-0048 through ADR-0060**, owner-ratified across 2026-08-13, 2026-08-14, 2026-08-17, 2026-08-18, 2026-08-19 and 2026-08-20. **`ADR-0060` ratifies `DP-011` Option C seeded by Option B: Rahu Kalam/Yamaganda/Gulika become named, profile-selectable variants; the PyJHora 4.8.7 `trikalam()` convention is independently inspected, transcribed and frozen as the seed variant `PYJHORA_TRIKALAM_V1`. Authorizes only that one variant's implementation/certification work - does not itself certify it, does not authorize a second variant, and does not authorize Muhurta-specific consumption.** **`ADR-0056` formalizes the four-role AI collaboration model (USER/CLAUDE/CHATGPT/CODEX); Codex is explicitly excluded from the ACE workflow. `ADR-0057` (CEO-audit HOLD remediation) adds ACE interaction mode and mandatory session-start audit to `specs/CLAUDE_WORKFLOW.md`. `ADR-0058` adds an execution-continuity rule (do not stop prematurely; five terminal stop conditions) to the same document; its `specs/CLAUDE_WORKFLOW.md` edit is committed (`20a9589e3d567bbf86e36b13bf2d61ca734e728e`). `ADR-0059` records the CEO-approved `PANCHANGA_V1` Gate F (genuine PyJHora external-oracle comparison for tithi/yoga/karana, nakshatra explicitly excluded): implemented, committed (`4177d6108236e64d07f6b23499307001f0d7c421`), pushed, and **CI-confirmed green** (run `32242462766`, all four jobs, oracle job genuinely executing Gate F: 66 comparisons, 0 mismatches, negative control verified) under the hash-pinned oracle environment. A 2026-08-19 evidence addendum to `ADR-0059` records the owner's acceptance of Panchanga's FOUNDATION per-capability checkpoint (`Q8_CLOSURE_MATRIX.md` s4); this does not close FOUNDATION's own phase-exit criteria, which still require Rahu Kalam/Yamaganda/Gulika, H-01, and H-02.** Tier-0 is **FORMALLY LOCKED** (ADR-0034), the only s12 Locked artifact. The registry vargas and the sign conventions are **owner-ratified but NOT s12 Locked** (ADR-0035 D3, ADR-0036 D3). **Q8 is now CLOSED** (ADR-0048); **Phase G exited and FOUNDATION entry criteria were independently confirmed satisfied** (this session's evidence reports). **FOUNDATION's first work package, rise/set, is CERTIFIED (`ADR-0054`, `RISE_SET_V1`)**: five owner-ratified conventions (upper-limb disc, standard -50' refraction, elevation accounted for, structured NO_RISE/NO_SET, conventions in `CalculationProfile`/`BirthData`), zero calculation impact on any existing certified capability, two genuine defects found and fixed during its own construction (recorded in the entry). **Panchanga classification-only work (tithi/vara/nakshatra/yoga/karana at a given instant) is now authorised (`ADR-0055`)**: engine-wide 1e-10 promote-up boundary convention, vara consumes the certified rise/set layer, element transition-timing deferred. **Rahu Kalam/Yamaganda/Gulika remain NOT authorised pending a future DP-NNN variant-table ratification (`ADR-0055` item 2).** No later phase (Muhurta, Varshaphal, Prashna, Mundane, BTR, Interpretation, Convergence, UI, ML) is thereby authorised - `docs/Q8_CLOSURE_MATRIX.md` s4 requires its own per-capability checkpoint for each. **Still PROPOSED: ADR-0003, ADR-0004, ADR-0013, ADR-0014, ADR-0018 through ADR-0032, ADR-0038, and ADR-0047.** `ADR-0047`'s originally-reported G5 sample accounting (22/22 complete, 16 independent, 4 ADB_MATCH, 2 unresolved, 14 events) was briefly, and **erroneously**, corrected to "12/22 attempted" by a 2026-08-18 addendum that has since been found (owner-directed forensic reconciliation) to rest on a conflation of the 22-person sample with an unrelated 5-person bridging pilot; a second, later 2026-08-18 addendum **restores 22/22 as the authoritative state** (16 independent, 4 ADB_MATCH: Fichera/Aimar/Serantoni/Bobet, 2 unresolved: Veen/Perquier, 14 independent events) and marks the "12/22" addendum SUPERSEDED/RETRACTED, preserved unedited. `ADR-0047` remains PROPOSED, not ratified, throughout. Ratification is per-entry; an owner existing is not the register being ratified. Includes the ADR-0018 remote-CI evidence addendum (2026-08-11), the ADR-0047 "12/22" addendum (2026-08-18, now retracted), and the ADR-0047 restoration addendum (2026-08-18). |
| Version | 3.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-20 (ADR-0060: DP-011 ratified, Option C seeded by Option B; PyJHora trikalam convention transcribed and frozen) |
| Review cadence | TBD |

# Decision Log (ADR register)

Append-only. Entries are never edited after acceptance; they are superseded by later entries.
Template at the bottom. Numbering: ADR-XXXX, monotonically increasing.

ORDERING. Per ADR-0029, this register is ordered by IDENTIFIER, not by append time. A new entry is
inserted at its numeric position. "Append-only" governs CONTENT: no entry is edited, renumbered or
deleted after it is written. It does not govern position. An addendum is NOT an entry and uses a
level-three heading, `### Evidence addendum to ADR-XXXX - <subject>`, so the numbering gate counts
decisions and only decisions.

RESERVED NUMBERS. ADR-0015 through ADR-0017 are reserved for the remaining Phase G commits
(0015 charter adoption, 0016 precedence hierarchy and agent workflow, 0017 certification
taxonomy). ADR-0014 was issued 2026-08-11 with Phase G commit 3. Phase G commit 1 delivered
G6 first by CEO sequencing decision, so ADR-0018 was ISSUED before ADR-0014 and before the
reserved 0015..0017. It is nevertheless FILED after ADR-0014, per the ordering rule above. The gap
at 0015..0017 is a reservation, not a lost entry, and a gap is not a monotonicity failure. Numbers are obtained from this register BEFORE implementation, per ADR-0004.

---

## ADR-0001 - Canonical repository structure
- **Date:** 2026-07-11
- **Status:** Accepted. **RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the
  ratification instruction recorded in ADR-0033. The ratification is of this entry EXACTLY AS
  WRITTEN: no word of its context, decision or consequences is changed, and no earlier
  conversation is claimed retrospectively as the ratification. Resolves Q13 for this entry.
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
- **Status:** Accepted. **RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the
  ratification instruction recorded in ADR-0033. The ratification is of this entry EXACTLY AS
  WRITTEN: no word of its context, decision or consequences is changed, and no earlier
  conversation is claimed retrospectively as the ratification. Resolves Q13 for this entry.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the lock
  authorisation recorded in ADR-0034. Ratified EXACTLY AS WRITTEN: the lock's scope, version,
  ratified profiles, frozen tolerances and evidence are unchanged, and no numerical value is
  restated or revised. **This ratification is what satisfies PROJECT_CONSTITUTION.md s12
  condition 4**, and with it Tier-0 is formally LOCKED. See ADR-0034 for the four-condition
  verification.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0037. Ratified EXACTLY AS WRITTEN: every scope boundary, numeric contract,
  boundary convention, profile restriction, non-claim and certification figure stands unaltered.
  **Ratification of a certification is not a lock**; this layer is NOT a Constitution s12 Locked
  artifact. See ADR-0037.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0037. Ratified EXACTLY AS WRITTEN: every scope boundary, numeric contract,
  boundary convention, profile restriction, non-claim and certification figure stands unaltered.
  **Ratification of a certification is not a lock**; this layer is NOT a Constitution s12 Locked
  artifact. See ADR-0037.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0037. Ratified EXACTLY AS WRITTEN: every scope boundary, numeric contract,
  boundary convention, profile restriction, non-claim and certification figure stands unaltered.
  **Ratification of a certification is not a lock**; this layer is NOT a Constitution s12 Locked
  artifact. See ADR-0037.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0035. Ratified EXACTLY AS WRITTEN: every rule table, boundary convention,
  school key, non-claim, recorded numerical finding and certification figure stands unaltered.
  **Ratification of a certification is not a lock**; no varga is Locked, and this entry does not
  claim otherwise. See ADR-0035.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0035. Ratified EXACTLY AS WRITTEN: every rule table, boundary convention,
  school key, non-claim, recorded numerical finding and certification figure stands unaltered.
  **Ratification of a certification is not a lock**; no varga is Locked, and this entry does not
  claim otherwise. See ADR-0035.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0035. Ratified EXACTLY AS WRITTEN: every rule table, boundary convention,
  school key, non-claim, recorded numerical finding and certification figure stands unaltered.
  **Ratification of a certification is not a lock**; no varga is Locked, and this entry does not
  claim otherwise. See ADR-0035.
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
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13**, on the ratification
  recorded in ADR-0036. Ratified EXACTLY AS WRITTEN: both decisions, the locked sign conventions,
  the declaration gate, the recorded non-claims and the explicit substitution of
  ARCHITECTURE_STATUS.md item 5 all stand unaltered. **This ratification closes the asymmetry
  ADR-0035 D4 recorded**, since the convention the ratified registry vargas emit is now itself
  owner-ratified. **It does NOT declare a Constitution s12 Locked artifact**; see ADR-0036 D3.
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

## ADR-0015 - Candidate Project Charter identified for adoption; disposition of ambiguous "charter section 11" references

- **Date:** 2026-08-17
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-17**, on the ratification instruction recorded in `ADR-0051` Decision 1. `specs/PROJECT_CHARTER.md` is adopted as the ACE Project Charter, unchanged, and explicitly does not replace or supersede `docs/PROJECT_CONSTITUTION.md`. The Decision items below stand as originally drafted and are not rewritten; see `ADR-0051` for the ratification record.
- **Context:** `docs/DECISION_LOG.md`'s reserved-numbers note (line 23) and `docs/Q8_CLOSURE_MATRIX.md` s3 both name "G2, charter commit / charter adoption" as an unmet Phase G exit item, held under the reserved, unissued `ADR-0015`. A prior forensic pass this session found `specs/PROJECT_CHARTER.md` as the only candidate document, unchanged since the repository's bootstrap commits (`485b6aa`, `716141e`, both 2026-07-11) and never previously drafted toward an ADR.
- **Decision:**
  1. **Identify `specs/PROJECT_CHARTER.md` as the candidate Project Charter**, per explicit owner instruction not to silently substitute `docs/PROJECT_CONSTITUTION.md` for it. Its current content (Product motive, Analytical systems, Isolation protocol, Scientific limitation) is reproduced here as the exact text under consideration; this entry changes none of it.
  2. **Verification against governing documents and history, performed and recorded:** `specs/PROJECT_CHARTER.md` carries no status header, version, or owner field, contrary to `docs/DOCUMENTATION_STANDARD.md` s2's mandatory structure for governing documents - it predates that standard and was never brought into conformance. `git log --follow -- specs/PROJECT_CHARTER.md` shows exactly two commits, both from the bootstrap era, and `git log --all -S"ADR-0015"` / `-S"charter adoption"` (this session) confirm no historical draft, section, or note toward `ADR-0015` exists anywhere in the tracked history. The document's content does not conflict with any ratified ADR found: its four sections (methodology isolation, no-cross-contamination, scientific-limitation disclaimer) are consistent with `docs/PROJECT_CONSTITUTION.md` ss 4-5 and 10 and with `docs/VALIDATION_STANDARD.md`'s empirical-validation section, though none of those cross-references is itself ratified charter content - each stands on its own document's own status.
  3. **`specs/PROJECT_CHARTER.md` gains a status header** (Status: PROPOSED - candidate Project Charter under this entry, not yet owner-adopted; Version 1.0.0, treating the header addition as the first versioned instance since none existed before; Owner: TBD per Q1) via this same governance pass. This is a mechanical/administrative addition only - it asserts no ratification and changes no existing sentence of the charter's substantive text.
  4. **Explicit disposition of every repository reference found that refers, ambiguously or incorrectly, to "the charter['s] section 11"** (a repository-wide search, this session, for "charter" co-occurring with "section"): `specs/PROJECT_CHARTER.md` has **no numbered sections at all**, so no reference to a "charter section" can be to it. Three occurrences were found, and each names content that in fact belongs to `docs/PROJECT_CONSTITUTION.md` s11 (the AI Collaboration Model / anti-circularity rule):
     - `docs/OPEN_QUESTIONS.md` row Q14 ("...the circularity the project charter section 11 warns against"): a **live, routinely-amended register**, not frozen evidence. **Disposed of by annotation in the same pass as this entry** (see `docs/OPEN_QUESTIONS.md` Q14's updated row): the phrase is clarified in place to name `docs/PROJECT_CONSTITUTION.md` s11 explicitly, without altering the row's resolution status or history.
     - `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md` line 23 ("...the circularity the project charter section 11 exists to prevent"): a **dated audit report**, frozen evidence of that date. **Disposed of by citation here, left untouched on the page** - correcting a dated report's prose would alter historical evidence for a defect that does not change what the report found or concluded.
     - `docs/DECISION_LOG.md`, `ADR-0033` Decision 4 ("...contradicts `PROJECT_CONSTITUTION.md` section 11, contradicts the charter's anti-circularity rule..."): an **already-ratified (ACCEPTED) decision entry**. **Disposed of by citation here, left untouched** - per governance rule, an already-recorded decision entry's substance is never edited; the sentence's own juxtaposition (naming `PROJECT_CONSTITUTION.md` s11 and then "the charter's anti-circularity rule" as the same thing, one clause apart) is itself the clearest evidence that this repository's own established informal usage treats "the charter" as shorthand for `PROJECT_CONSTITUTION.md` in governance prose, not as a reference to `specs/PROJECT_CHARTER.md`.
     - **Finding, stated plainly:** every located "charter section 11" reference is an imprecision of language, not a claim about `specs/PROJECT_CHARTER.md`. None requires a substantive correction to what it asserts; each has now been explicitly identified and dispositioned per this decision, satisfying the instruction that ambiguous references not be left unaddressed.
  5. **This entry does not adopt the charter.** Adoption is the owner's act. On adoption, this entry's Status line is updated to Accepted with the ratification evidence, per the pattern already used for `ADR-0001`/`ADR-0002` (`ADR-0033` Decision 2) - the body above is not rewritten.
- **Consequences:** No certified calculation behaviour, certification artifact, or ratified decision entry is touched. `specs/PROJECT_CHARTER.md` gains only a status header; its substantive text is byte-identical to before. `docs/OPEN_QUESTIONS.md` Q14 gains a clarifying annotation, not a status change. G2 remains **NOT complete** until the owner acts on this entry - preparing it does not itself satisfy `docs/Q8_CLOSURE_MATRIX.md` s3's "charter commit" criterion.
- **Evidence:** `specs/PROJECT_CHARTER.md` (full text, this session); `git log --follow -- specs/PROJECT_CHARTER.md`; `git log --all -S"ADR-0015" -S"charter adoption"`; repository-wide search for "charter" near "section" (three occurrences found, all cited above); `docs/DOCUMENTATION_STANDARD.md` s2; `docs/OPEN_QUESTIONS.md` Q14 (pre- and post-annotation); `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md` line 23; `docs/DECISION_LOG.md` `ADR-0033` Decision 4 (line ~1620, unedited); this session's own forensic report (prior turn) confirming `ADR-0015` unissued via `scripts/check_adr_numbering.py`.

---

## ADR-0016 - Precedence-hierarchy component recorded as satisfied by ADR-0042; agent-workflow component proposed; dangling ADR-0022 dispositioned

- **Date:** 2026-08-17
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-17**, on the ratification instruction recorded in `ADR-0051` Decision 2. The precedence-hierarchy component is closed by reference to already-ratified `ADR-0042`; the agent-workflow component is ratified by adopting `specs/CLAUDE_WORKFLOW.md` as written, subordinate to the `ADR-0042` hierarchy and not an independent source of authority. The Decision items below stand as originally drafted and are not rewritten; see `ADR-0051` for the ratification record.
- **Context:** `docs/DECISION_LOG.md` line 24 reserves this number for "precedence hierarchy and agent workflow" as one combined Phase G commit. Owner instruction this session directed evaluating these as two separate components, evaluating `ADR-0042` as the already-ratified precedence hierarchy without duplicating or rewriting it, and dispositioning dangling `ADR-0022`.
- **Decision:**
  1. **Precedence-hierarchy component: satisfied by `ADR-0042`, already ACCEPTED (2026-08-14).** `ADR-0042` Decision 1 states, as ratified fact: **OWNER -> PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> DECISION LOG / ADR -> STANDARDS -> SPECIFICATIONS -> CODE -> CONVERSATION**. This entry records, and does not restate or amend, that `ADR-0042` already answers the "precedence hierarchy" half of this reserved slot's original scope. No new hierarchy text is authored here.
  2. **Disposition of dangling `ADR-0022` ("Governance authority hierarchy; disposition of the root D-00x decision family"), PROPOSED, 2026-08-11, never ratified.** `ADR-0022` Decision 1 proposed an earlier, three-level-top hierarchy (`OWNER -> PROJECT CONSTITUTION -> DECISION LOG/ADR -> ...`) that does not include `ENGINEERING CONSTITUTION` as its own rung. That specific decision item is **superseded in substance by `ADR-0042`**, which is later and ratified. `ADR-0022`'s remaining decision items (2 through 4: the root `DECISION_LOG.md` D-00x family's subordinate classification, conflict resolution favouring the ADR register, and no-deletion/no-renumbering) are **a separate question, not addressed by `ADR-0042` and not addressed here**, and remain PROPOSED, unresolved, and unaffected by this entry. `ADR-0022` itself is **not edited** - per governance rule, a recorded entry's substance is never altered; this decision item is the corrective record, in the same pattern `ADR-0014` used to correct a false claim in commit `8a5d56e` without rewriting it.
  3. **Agent-workflow component, proposed policy, not ratified here.** `specs/CLAUDE_WORKFLOW.md` was inspected against current ratified governance (`docs/PROJECT_CONSTITUTION.md` s11, `ADR-0042`) and the `.claude/` tooling (`CLAUDE.md`, `.claude/rules/governance.md`, `.claude/rules/certification.md`, `.claude/rules/git-safety.md`, `.claude/rules/validation.md`, ratified by `ADR-0044`). Finding: its content (Claude as implementation engineer, not methodology or certification authority; the handoff-package pattern; "two AI systems agreeing is not evidence of correctness") is **consistent with, and strictly narrower than**, both - no contradiction was found. It remains `Status: DRAFT` (a header was added for accuracy in this session's prior governance pass, `ADR-0050`; its substantive text is unchanged and still unratified). `ADR-0044` Decision 7 explicitly declined to ratify or modify it. **Proposed option, labelled as a recommendation only, confidence MEDIUM:** ratify `specs/CLAUDE_WORKFLOW.md` as written as the agent-workflow half of this entry's scope, since its content already matches ratified practice and no revision was found necessary. **Alternative, stated because it is real:** the owner may instead direct specific amendments first (for example, explicitly restating the owner-ratifies-all-decisions and ChatGPT-auditor rules from `docs/PROJECT_CONSTITUTION.md` s11, which `specs/CLAUDE_WORKFLOW.md` does not currently repeat) before ratification. **This entry does not choose between these; the owner does.**
- **Consequences:** No certified calculation behaviour touched. `ADR-0022` and `ADR-0042` are both unedited. `specs/CLAUDE_WORKFLOW.md` is unedited by this entry (its status header was already added under `ADR-0050`). G3 remains **NOT complete**: the precedence-hierarchy half is factually answered by cross-reference to already-ratified material, but this entry itself is PROPOSED, and the agent-workflow half still requires an owner ratification act this entry does not perform.
- **Evidence:** `docs/DECISION_LOG.md` `ADR-0022` (full text) and `ADR-0042` (full text); `specs/CLAUDE_WORKFLOW.md` (full text, post-`ADR-0050` header); `CLAUDE.md` and `.claude/rules/*.md` (current tracked content); `ADR-0044` Decision 7; this session's prior forensic report confirming `ADR-0016` unissued and `ADR-0022` dangling.

---

## ADR-0017 - Proposed C0-C5 certification taxonomy: facts, gaps, and proposed policy, separated

- **Date:** 2026-08-17
- **Status:** **ACCEPTED. RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-17**, on the ratification instruction recorded in `ADR-0051` Decision 3, as a claim/evidence classification framework (not a confidence score). The final, binding C0-C5 definitions are tabulated in `ADR-0051`, which governs where its wording differs from this entry's own Section 3 "proposed policy" draft below; Sections 1-4 here stand unedited as the historical record of what was proposed and are not rewritten.
- **Context:** `docs/Q8_CLOSURE_MATRIX.md` s2 cites "the charter's C0 to C5 levels" as certification-gate vocabulary "where the mapping is still unresolved," reserved as `ADR-0017`. `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` (lines 461-465) independently recommended this taxonomy "land sooner rather than later." A repository-wide search this session found no draft anywhere.
- **Section 1 - Existing repository facts (attested, cited, not invented):**
  - `Status: PROPOSED, C0 RESEARCH` is used verbatim as a status-header value on nine specifications: `docs/EVIDENCE_INDEPENDENCE_DESIGN.md`, `docs/H0_ENTITY_MODEL_SPEC.md` through `H5`, `H7_BTR_SPEC.md`, `H8_CONVERGENCE_SPEC.md`, and `docs/PLATFORM_DOMAIN_ARCHITECTURE.md`. Meaning, by consistent usage: specification/design proposal only, no implementation authorised.
  - `docs/Q8_CLOSURE_MATRIX.md` s6 (EVIDENCE phase) entry criteria: "H0, H1, H2, H4 and H5 promoted from C0 research to ratified specifications" - names a next step above C0 without giving it a number.
  - `docs/PROJECT_ROADMAP.md` line 38: "certified to C2 or C4 in several places" - two distinct certified levels used side by side, with no stated ranking between them.
  - `docs/H6_PREDICTION_LEDGER_SPEC.md` s5, "The C5 gate": **C4 is explicitly defined as "a claim about software correctness."** **C5 is explicitly defined as "a claim about the world," earned only through the prediction ledger, over a protected population, with pre-registered falsification criteria and a stated sample size.** "C4 MUST NEVER be represented as C5" is stated as a standing rule, repeated verbatim in `docs/PROJECT_ROADMAP.md` line 178 and `docs/Q8_CLOSURE_MATRIX.md` s14.
  - `docs/DECISION_LOG.md` (`ADR-0018` evidence block, "G6" determination) and `reports/G6_COMPLETION_RECORD.md` line 178 both state a reproducibility/infrastructure determination "certifies no calculation, promotes no component's certification level, and is not a C4 or C5 claim about any astrological method" - i.e., some determinations are **explicitly outside the C-scale entirely**, a fact this proposal preserves rather than resolves away.
  - The varga six-gate certification template, as implemented identically in every `scripts/certify_d*.py`, runs in this fixed order: Gate A (rule-table integrity, second transcription), Gate B (dense mathematical sweep against an independently-coded rule), Gate C (external oracle comparison), Gate D (framework non-invasiveness), Gate E (independent validator). Internal validation (A/B) is structurally complete before external-oracle validation (C) begins, in every certifier inspected.
  - `docs/PROJECT_CONSTITUTION.md` s12 defines "Locked" as the conjunction of four conditions (written spec/profile; a passing reproducible verification run; machine- and human-readable evidence agreeing from that same run; a decision-log entry recording the lock, version and evidence) - the single strongest attested status in the repository, held only by Tier-0 (`ADR-0034`). No document anywhere maps "Locked" onto a C-number.
  - `docs/VALIDATION_STANDARD.md` s1 defines a **separate, disjoint** claim-class vocabulary: "Works," "Accurate / within tolerance," "Certified / locked," "Faster / better" - with **no stated mapping** to C0-C5 anywhere in the tracked tree.
- **Section 2 - Contradictions and gaps identified (not resolved by this entry):**
  - **`C1` and `C3` have zero attested usage anywhere in the tracked repository** (verified by word-boundary search this session) - no document, spec, report, or ADR ever writes "C1" or "C3" with any meaning. This is the single largest gap: two of six levels in the "C0-C5" name are pure placeholders.
  - No document states whether `C2` or `C4` is the higher/stronger claim, despite both being used (`docs/PROJECT_ROADMAP.md` line 38) as if the reader already knows.
  - No mapping exists between `docs/VALIDATION_STANDARD.md`'s claim-class vocabulary and C0-C5, despite `docs/Q8_CLOSURE_MATRIX.md` s2 citing both as if interchangeable ("cite the existing vocabulary where one exists and the charter's C0 to C5 levels").
  - No mapping exists between `PROJECT_CONSTITUTION.md` s12 "Locked" and any C-number.
  - `docs/MASTER_ARCHITECTURE.md` lines 18 and 21 use "C4" for the **unrelated C4 architecture-modelling standard** ("System context (C4 level 1)," "Container view (C4 level 2)") - a token collision with certification-C4 that predates this proposal and will confuse readers once `ADR-0017` is ratified under either name.
  - It is never stated whether "C0 RESEARCH" (always written as one compound phrase) is part of the same numeric scale as C2/C4/C5, or a separate prefix notation that happens to share a digit.
- **Section 3 - Proposed policy (builder recommendation, confidence MEDIUM overall, explicitly NOT ratified by this entry):**
  A six-level scale is proposed, anchored to the attested facts in Section 1 wherever one exists, and explicitly flagged as invented where none does:
  1. **C0 - Research.** Specification/design proposal only; no implementation authorised. *(Attested, high confidence - matches existing usage exactly.)*
  2. **C1 - Ratified specification.** The specification has been owner-ratified; no certified implementation exists yet. *(Proposed - fills the gap `Q8_CLOSURE_MATRIX.md` s6 names ["promoted from C0 research to ratified specifications"] without a number. No prior attested usage of "C1" itself.)*
  3. **C2 - Implemented, internally validated.** Code exists, passes the "Works" claim class (`VALIDATION_STANDARD.md` s1), and passes internal dense-sweep/ULP-battery validation (varga template Gates A/B) - no independent external reference yet. *(Proposed mapping - consistent with `PROJECT_ROADMAP.md`'s informal "C2" usage and the gate template's actual internal ordering, but the mapping itself is new.)*
  4. **C3 - Externally cross-checked, not yet locked.** Passed independent-oracle comparison (varga template Gate C) but no `PROJECT_CONSTITUTION.md` s12 decision-log lock yet. **Flagged explicitly: this is the weakest part of this proposal** - "C3" has zero prior attested usage anywhere, and this level is invented whole to fill the structural gap between "internally validated" and "certified/locked," not extracted from existing evidence.
  5. **C4 - Certified / Locked.** *(Attested - matches `H6_PREDICTION_LEDGER_SPEC.md` s5's "software correctness" claim and `VALIDATION_STANDARD.md`'s "Certified/locked" claim class.)* **Proposed, not attested:** that this corresponds exactly to `PROJECT_CONSTITUTION.md` s12's four-condition "Locked" definition - no document currently states this equivalence.
  6. **C5 - Empirically validated.** *(Attested, verbatim from `H6_PREDICTION_LEDGER_SPEC.md` s5: prediction validated over a protected population, pre-registered falsification criteria, stated sample size. A claim about the world, never C4.)*
  - **Explicitly out of scale, proposed as a standing note rather than a level:** reproducibility/infrastructure determinations (the G6 pattern) are recorded as certifying "no calculation" and claiming no C-level at all, per Section 1's evidence - this proposal recommends the taxonomy say so explicitly, to prevent a future determination being miscited as a C-level by omission.
- **Section 4 - Owner decision points (this entry decides none of them):**
  1. Whether a six-level `C0-C5` scale is wanted at all, given `C1` and `C3` have no existing usage to anchor them, versus a smaller or differently-shaped scale.
  2. Whether the proposed `C1`/`C2`/`C3` definitions in Section 3 (the three levels with the weakest or no attested precedent) are acceptable, or should be redefined.
  3. Whether `PROJECT_CONSTITUTION.md` s12 "Locked" should be explicitly mapped onto this scale, or kept deliberately separate and stronger.
  4. Whether `VALIDATION_STANDARD.md`'s claim-class vocabulary should be cross-referenced to, superseded by, or kept independent of the C-scale.
  5. Whether `docs/MASTER_ARCHITECTURE.md`'s unrelated "C4 architecture-model" usage should be renamed to remove the token collision once certification-C4 is ratified.
  6. Whether the "explicitly out of scale" note for reproducibility/infrastructure determinations (Section 3) should be adopted as written.
- **Consequences:** No certified calculation behaviour, certification artifact, or ratified decision entry is touched. No document in the repository is modified by this entry's substance (Sections 1-4 are new text in this entry only). G5 remains **NOT complete**: this is a proposal awaiting the six decisions in Section 4, not a ratified taxonomy.
- **Evidence:** Repository-wide searches this session for "C0" through "C5" (word-boundary, all `.md` files, `.ace_q17_q21_prechange/` excluded) and their zero-result counterparts for `C1`/`C3`; `docs/Q8_CLOSURE_MATRIX.md` ss 2, 6, 14; `docs/PROJECT_ROADMAP.md` lines 38, 178; `docs/H6_PREDICTION_LEDGER_SPEC.md` s5; `docs/VALIDATION_STANDARD.md` s1; `docs/PROJECT_CONSTITUTION.md` s12; `docs/MASTER_ARCHITECTURE.md` lines 18, 21; `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` lines 461-465; `reports/G6_COMPLETION_RECORD.md` line 178; every `scripts/certify_d*.py` (gate ordering, direct inspection); this session's prior forensic report.

---

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

### Evidence addendum to ADR-0018 - remote CI validation (2026-08-11)

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

## ADR-0021 - Mundane validation discipline, Q8 status, entity vocabulary and relationships, and the independence principle

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1). Recorded on CEO direction following
  approval of ADR-0020 as the current architectural baseline.
- **Context:** ADR-0020 was approved and four of its recorded residues were referred back for
  decision: the multiple-comparison discipline for mundane validation, the status of Q8, the entity
  vocabulary, and entity relationships. A fifth item elevates the independence rule from a
  consequence noted in a specification to a permanent normative principle.
- **Decision:**

  **D1. Mundane validation is pre-registered, not mined.** Mundane historical validation MUST NOT
  become a large-scale pattern-mining exercise in which many hypotheses are tested and only the
  successful-looking results are reported. Before any protected testing, a mundane validation
  protocol MUST define: event classes; hypotheses and rules; the development or training historical
  set; the protected holdout historical set; the number of hypotheses tested; the number of events
  tested; the applicable multiple-comparison methodology; effect-size measures; negative controls
  where feasible; and replication requirements where feasible.

  Rules MUST NOT be selected, modified or tuned using protected holdout results.

  **Statistical significance MUST NEVER be represented as scientific proof of astrology.** It is
  evidence about the measured performance of a specified astrological method under a specified
  validation protocol, and it is to be stated in exactly those terms.

  This is a permanent governance and validation requirement, recorded normatively in
  `docs/VALIDATION_STANDARD.md` s4 and in `docs/H2_HISTORICAL_EVENT_LEDGER_SPEC.md` s9.

  **D2. Q8 REMAINS OPEN.** ADR-0020 D6 supplies a preferred domain order and does not close Q8. Q8
  remains open until the roadmap defines, for every implementation phase: prerequisites, entry
  criteria, implementation scope, certification gates, exit criteria, and CEO approval requirements.
  **The domain order is NOT authorisation to begin implementation.**

  **D3. The entity vocabulary is provisional and extensible.** Current kinds: Person,
  Organisation/Company, Geographic/National Entity, Event, Question. The ontology is deliberately NOT
  frozen at this stage. A new entity kind requires an explicit architectural decision.

  **D4. Relationships are modelled as explicit links, not as entities.** Entity A, relationship,
  Entity B. For example Person LEADS Organisation, Person CANDIDATE_IN Election, Company OPERATES_IN
  Country, Event OCCURS_IN GeographicEntity. A relationship MAY later be promoted to an entity only
  if it requires its own lifecycle, identity, evidence, provenance, temporal state and independent
  analysis. RESOLVES the third open question in `docs/H0_ENTITY_MODEL_SPEC.md` s7.

  **D5. The independence principle is permanent and normative:**

  > **Absence of measured correlation is not evidence of independence.**

  Therefore, and stated as non-equivalences because each has been assumed in practice elsewhere:
  unknown relationship is not independent; derived relationship is not independent; shared-origin
  relationship is not independent; correlated relationship is not independent.

  The convergence architecture must eventually determine AND EXPLAIN the dependency structure
  between evidence sources, and must answer not "how many systems agree" but **"how many genuinely
  independent evidence paths support this conclusion"**.

- **Consequences and analysis:**

  1. **D1 is pre-registration, and naming it that is useful.** The list of things to define before
     testing is the established practice of pre-registration as used in empirical research. Naming
     it gives the eventual implementation a body of existing method to draw on rather than
     inventing a protocol from first principles, and it makes the discipline auditable: a protocol
     either was registered before the protected run or it was not, and that is a checkable fact
     rather than a judgment.
  2. **A concrete negative control exists for this domain and should be recorded now.** Running the
     same rules against permuted data, for example entity charts randomly reassigned to entities,
     or events shifted to random dates, gives an empirical null distribution. If a rule scores as
     well against shuffled data as against real data, the apparent performance is an artifact of
     the protocol rather than a property of the rule. This is cheap, and it is one of the few
     controls available in a domain where a true control group does not exist.
  3. **The count of agreeing systems is an upper bound, never the answer.** D5's question implies
     the dependency structure is a graph, and the honest measure is the number of genuinely
     independent paths through it, which is at most the number of agreeing sources and typically
     fewer. A convergence layer that reports the raw count is reporting the upper bound as though
     it were the estimate. How the effective independent count is computed is an open design
     question; that it must not be the raw count is now decided.
  4. **D5 makes an existing specification passage normative.** `docs/H8_CONVERGENCE_SPEC.md` s12
     already stated that unmeasured relationships must not default to independent, as a consequence
     of ADR-0020 D4. It is now a named principle in its own right, which matters because it applies
     beyond convergence: it governs how evidence is aggregated anywhere, including any future
     scoring, weighting or confidence computation.
  5. **D2 has an immediate consequence for how this project reads its own roadmaps.**
     `docs/VARGA_CERTIFICATION_ROADMAP.md`, `docs/DASHA_CERTIFICATION_ROADMAP.md` and
     `docs/PLATFORM_DOMAIN_ARCHITECTURE.md` all state orders and sequences. None of them
     authorises implementation, all of them say so, and D2 makes that explicit at the register
     level so the point cannot be lost by reading one document in isolation.
  6. **D4 defers a real cost rather than avoiding it.** Links are cheaper than entities and are the
     right starting point. The promotion criteria matter because relationships in this domain
     genuinely can acquire their own lifecycle: a marriage has a start, an end, its own events and
     arguably its own chart. The criteria are recorded so promotion is a decision rather than a
     drift.
  7. **D3's extensibility is not a licence for silent growth.** A new entity kind changes which
     rules are applicable and therefore what the system may claim, so it takes an architectural
     decision, exactly as a new varga or a new identifier family does.
  8. **NO IMPLEMENTATION IS AUTHORISED** by this entry: not panchanga, rise/set, Muhurta,
     Varshaphal, Prashna, Mundane, BTR, interpretation or convergence.

- **Evidence:** `docs/VALIDATION_STANDARD.md` s4 and s5, `docs/H2_HISTORICAL_EVENT_LEDGER_SPEC.md`
  s9, `docs/H0_ENTITY_MODEL_SPEC.md` s9.1, `docs/H8_CONVERGENCE_SPEC.md` s14,
  `docs/OPEN_QUESTIONS.md` Q8 closure criteria. Default gate 404 passed and the identifier
  governance gate PASS at the time of recording, with zero changes under `engine/`, `legacy/`,
  `scripts/`, any validator or any certification artifact.

---

## ADR-0022 - Governance authority hierarchy; disposition of the root D-00x decision family

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1). Recorded on CEO direction. Per
  PROJECT_CONSTITUTION.md s11 an AI-written entry cannot be Accepted by its author, and Q1 (named
  owners) is open, so **no entry in this register can currently be Accepted by anyone**. That is
  stated here once and applies to every entry below.
- **Context:** ADR-0013 conflict 5 records that root `DECISION_LOG.md` (D-001..D-008) and this
  register (ADR-000x) coexist with no stated precedence. Separately, the repository has never had a
  single written authority hierarchy, which is what allowed out-of-repository plan documents to
  govern in-repository code during the 2026-08-08/09 work.
- **Decision:**
  1. **NORMATIVE AUTHORITY HIERARCHY**, highest first:
     `OWNER -> PROJECT CONSTITUTION -> DECISION LOG / ADR -> STANDARDS -> SPECIFICATIONS -> CODE ->
     CONVERSATION`.
     The owner is the final ratifying authority. The repository is the permanent project record.
     Conversation is input material and never permanent authority.
  2. **D-00x disposition: option A, subordinate classification, not migration.** The root
     `DECISION_LOG.md` family is classified as **ROOT TECHNICAL DECISIONS**: operative, subordinate
     to this register in precedence, and **closed to new entries**. All future decisions are issued
     as ADR-000x from this register only.
  3. Where a root D-00x entry and an ADR conflict, **the ADR governs**, and the conflict must be
     recorded rather than resolved silently.
  4. No root decision is deleted, renumbered or rewritten. Provenance is preserved intact.
- **Consequences:**
  - **Correction to the framing in the CEO instruction, made deliberately.** The instruction offered
    "explicitly classified as historical/root technical decisions". D-001 through D-007 are **not
    historical**: they are live and actively cited. D-001 fixes swetest as the numerical authority
    and is cited by the certifiers; D-002 fixes the 0.5 arcsec tolerance; D-003 fixes zero
    categorical tolerance for the KP hierarchy; D-004 is the anti-fitting rule; D-007 governs how
    external-oracle divergence is handled and is cited by the transit and Vimshottari certifiers.
    Labelling them historical would imply they no longer bind, which would be a substantive and
    unintended weakening. They are therefore recorded as **operative but subordinate and closed**.
  - Option A was chosen over migration because migration would either renumber operative decisions,
    breaking every citation in the certifiers, or duplicate them, creating exactly the two-source
    ambiguity the conflict exists to remove. Option A is the smaller change and preserves provenance
    completely, which is what the instruction asked for.
  - D-008 alone carries a sequencing claim rather than a technical constraint and is dealt with
    separately in ADR-0027.
  - Root `DECISION_LOG.md` gains a header note recording this classification. Its entries are
    untouched.
- **Evidence:** Root `DECISION_LOG.md` D-001..D-008 read in full; D-001, D-002, D-003, D-007 cited
  live in `scripts/certify_*.py` and in ADR-0006, ADR-0007 and ADR-0008 evidence blocks.

---

## ADR-0023 - Executable normative rule data versus governed knowledge; the Vimshottari duplication; architecture-document precedence

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** ADR-0013 conflicts 1, 2 and 3 are one problem seen from three angles.
  Conflict 1: `engineering/ENGINEERING_CONSTITUTION.md` Principle 3 says knowledge belongs in
  structured knowledge files and business logic in engine modules, while every certified rule table
  is a Python literal. Conflict 2: `docs/KNOWLEDGE_STANDARDS.md` says a fact shall exist in only one
  knowledge asset and must never be duplicated, while the Vimshottari lord and year tables exist in
  three places by deliberate choice. Conflict 3: three architecture documents place the knowledge
  layer in three incompatible positions, and the only one marked LOCKED is the only one that places
  prediction and interpretation inside knowledge, which every other document forbids.
- **Decision:**

  **1. A precise test distinguishing the two categories.** Data is **EXECUTABLE NORMATIVE RULE DATA**
  if and only if ALL FOUR hold:

  (a) a deterministic certified calculation cannot produce its output without it;
  (b) changing it changes certified numerical or categorical output;
  (c) it is covered by that calculation's certification artifact;
  (d) it is school-scoped, and its classical source and provenance are recorded at the point of use.

  Data failing any of the four is **GOVERNED KNOWLEDGE**.

  Executable normative rule data MAY be colocated with the implementation as frozen literals.
  Governed knowledge belongs in `knowledge/`, research material in `research/`, and product or
  application state never becomes calculation truth.

  **2. Principle 3 is narrowed, explicitly, not violated.** A frozen classical rule table is neither
  knowledge-for-reasoning nor business logic: it is part of the deterministic specification of an
  algorithm, and it is verified cell by cell as such. Principle 3 therefore **yields for data meeting
  the four-part test**, and governs everything else unchanged. This is a narrowing recorded by
  decision rather than a wording rule quietly ignored, which is what conflict 1 objects to.

  The engineering rationale is stated because it is the substance: moving a certified varga table
  into a loadable asset would make certified output depend on file loading, path resolution and
  schema validation at runtime. That converts a proven deterministic property into an operational
  one, weakens certification, and is precisely what the instruction warns against.

  **3. The Vimshottari duplication is PERMITTED, with its reason and its test stated.** The lord and
  year tables exist in `legacy/kp.py`, `engine/kp/tables.py` and `engine/dasha/tables.py`. Each
  serves a different school-scoped consumer, each is independently certified, and a cross-import
  would create a dependency in which a change made for one school silently alters another. School
  isolation is a charter non-negotiable; single-source-of-truth is a standard. **Where they conflict
  for executable normative rule data, isolation wins**, and the duplication is tested rather than
  removed. `KNOWLEDGE_STANDARDS.md` is therefore narrowed to governed knowledge, its proper subject.

  **A gap in the current cross-consistency net is recorded rather than glossed.**
  `engine/tests/test_vimshottari_consistency.py` asserts `engine/dasha/tables.py` equals
  `engine/kp/tables.py` without cross-import. **No test compares `engine/kp/tables.py` against
  `legacy/kp.py` directly.** That leg is covered only behaviourally, by the equivalence sweep. Closing
  it is required follow-up work, recorded as new question Q11.

  **4. Architecture-document precedence.** `docs/REPOSITORY_ARCHITECTURE.md` is marked `LOCKED`, and
  that lock fails PROJECT_CONSTITUTION.md s12 condition 4 because no decision entry records it. It is
  also the only architecture document placing prediction and interpretation inside the knowledge
  layer. Its LOCKED status is therefore **corrected to a historical status with a superseding note**,
  as a purely documentary correction of a claim the constitution never supported. Its content is not
  rewritten. For layering, the authoritative statement is this ADR together with
  `docs/PLATFORM_DOMAIN_ARCHITECTURE.md`.
- **Consequences:** No file moves. No calculated value changes. `engine/knowledge/data/` remains
  implementation-owned rule data under the four-part test, distinct from top-level `knowledge/`, which
  is governed knowledge; ADR-0024 draws that boundary. New question Q11 records the missing
  legacy-to-engine table comparison.
- **Evidence:** Principle 3 text at `engineering/ENGINEERING_CONSTITUTION.md:46-50`;
  `docs/KNOWLEDGE_STANDARDS.md:13-22`; `docs/REPOSITORY_ARCHITECTURE.md:5` LOCKED status;
  the three table locations verified present and value-identical; `test_vimshottari_consistency.py`
  read and its coverage boundary confirmed by inspection.

---

## ADR-0024 - Engine to knowledge boundary (resolves Q6)

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** Q6 asks whether `engine/` may read `knowledge/` at runtime. ADR-0013 conflict 4
  records that it was answered in practice rather than by decision.
- **Decision:**
  1. **`engine/` MUST NOT depend on top-level `knowledge/` at runtime for certification-critical
     calculation.** The certified calculation path executes against pinned, versioned,
     implementation-owned rule contracts only.
  2. `engine/knowledge/` is **implementation-owned rule and reference data**, not the governed
     knowledge layer, and is permitted as a runtime dependency of engine code under the ADR-0023
     four-part test. The name collision with top-level `knowledge/` is unfortunate and is recorded
     rather than renamed, because renaming a package touches import paths across certified modules
     for a cosmetic gain.
  3. Dependency direction: `research / authoritative sources -> governed specifications and knowledge
     -> implementation -> certification evidence`.
  4. Future inference, question and convergence layers MAY consume governed knowledge. The
     calculation engine MUST NOT load arbitrary knowledge assets dynamically. Any future controlled
     adapter MUST be specified explicitly, with its version pinning and failure behaviour, before use.
- **Consequences:**
  - **Empirically verified, and the decision matches reality.** `engine/` contains **zero** runtime
    imports of top-level `knowledge/`, and zero references to `knowledge/hlkg`. Nothing must change
    to comply; the decision records and protects an existing property.
  - **One live dependency is declared rather than discovered later.**
    `engine/astrology/dignity.py` loads `engine/knowledge/data/dignities.json` through
    `engine/knowledge/repository.py`. Under the four-part test that is implementation-owned rule data
    and is permitted. It is named here so the dependency is on the record. Note that dignity data
    sits **outside** the current Tier-0 lock scope, which covers the kernel and D9/D10 only.
  - Q6 is recorded as resolved pending ratification; see `docs/OPEN_QUESTIONS.md`.
- **Evidence:** Repository-wide search: 0 runtime imports of top-level `knowledge/` from `engine/`;
  `engine/knowledge/repository.py:16,28` and `engine/astrology/dignity.py:5` for the declared
  dependency.

---

## ADR-0025 - Certified kernel lineage (resolves Q9)

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** Q9 asks whether the certified kernel should be imported into `engine/` and under what
  name. It has been open while `engine/` was heavily populated and certified.
- **Decision:**
  1. The calculation kernel under `engine/` is the **authoritative production calculation
     foundation**. It is not reimplemented for architectural aesthetics.
  2. Its certification lineage is preserved: Tier-0 lock at `bfae088` recorded by ADR-0005, evidenced
     by `certification/current_engine_certification.json` and
     `certification/CURRENT_ENGINE_LOCK.json`, with 528 comparisons against the bundled swetest
     2.10.03 binary under both ratified profiles at a maximum error of 0.000180 arcsec.
  3. `legacy/` remains a **historical and equivalence reference**. It is NOT retired.
     `docs/LEGACY_KERNEL_MIGRATION.md` forbids retirement before all certified functionality has
     migrated, and that condition is not met.
  4. Any change inside certified scope requires a formal change decision, regression, independent
     validation, and recertification where applicable.
- **Consequences:**
  - **Empirically verified.** `legacy/` is imported by **five test modules only** and by no production
    module. The single reference inside `engine/kp/intervals.py` is a docstring recording that the
    mathematics was migrated verbatim; it is not an import. The dependency posture is therefore
    already correct.
  - **No retirement is claimed.** `legacy/` continues to serve as the KP equivalence oracle for
    ADR-0006 and as the historical Tier-0 record described by `LOCK_MANIFEST.json`.
  - Q9 is recorded as resolved pending ratification.
- **Evidence:** `grep` over `engine/` for legacy imports returns `test_kp_chart.py:22`,
  `test_kp_legacy_equivalence.py:16`, `test_kp_certification.py:16`,
  `test_reference_astronomy.py:120`, and a docstring at `engine/kp/intervals.py:24`.

---

## ADR-0026 - Roadmap reconciliation and the Phase-2-ahead-of-Phase-1 history (ADR-0013 conflict 7; addresses Q8)

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1). **Q8 is NOT closed by this entry**; see
  consequences.
- **Context:** `docs/PROJECT_BACKLOG.md` places Phase 1 Core Intelligence before Phase 2 Astrology
  Systems. The astrology systems were built first, and all nineteen Phase 1 items remain not started.
  ADR-0020 D6 later recorded a preferred domain order, and ADR-0021 D2 confirmed that an order alone
  does not close Q8.
- **Decision:**
  1. **The history is recorded, not rewritten.** Certified astrology foundation layers were developed
     ahead of the originally proposed Phase 1 intelligence layer. That work is valid, certified, and
     is treated as **completed prerequisite foundation work**. It is not undone and not re-sequenced
     retrospectively.
  2. **Certified does not mean ready.** That the calculation layers are certified does NOT imply the
     intelligence or convergence product is ready. Nineteen Phase 1 items remain not started, and no
     evidence, interpretation, convergence, validation, API or UI capability exists.
  3. **Future sequencing is dependency-driven, not historical.** The forward order is: governance
     baseline; canonical question and input model; knowledge and domain registry; inference and
     dependency planning; evidence model; system-specific interpretation layers; convergence;
     historical validation and learning; API; UI; production.
  4. Astrology system implementation remains modular and school-isolated. **Muhurta, Varshaphal,
     Prashna and Mundane remain separate domain architectures and are not forced through a natal
     pipeline** (ADR-0019, ADR-0020).
  5. `docs/PROJECT_ROADMAP.md` becomes the document distinguishing completed historical work,
     currently authorised work, future work, and prerequisites. No phase is marked complete without
     evidence.
- **Consequences:**
  - **Q8 remains OPEN, and this is a deliberate conflict with the instruction's step 5 heading.** The
    instruction asks to resolve Q8. The immediately preceding CEO direction stated "Q8 remains OPEN.
    Do not close it", and Q8's own closure criteria per ADR-0021 D2 require per-phase prerequisites,
    entry criteria, scope, certification gates, exit criteria and approval requirements. Those exist
    as a **candidate matrix** in `docs/Q8_CLOSURE_MATRIX.md`, which is explicitly unratified.
    Closing Q8 here would be manufacturing approval, which the instruction also forbids. The two
    directions conflict and the conflict is recorded rather than resolved by picking one silently.
    Q8 status becomes RESOLUTION DRAFTED, PENDING RATIFICATION.
  - This entry supersedes the *sequencing implication* of `docs/PROJECT_BACKLOG.md`, not its content.
    The backlog remains the enumerated item list.
- **Evidence:** `docs/PROJECT_BACKLOG.md` Phase 1 contains 19 unchecked items, verified by count;
  `docs/Q8_CLOSURE_MATRIX.md` present in this branch; ADR-0020 D6 and ADR-0021 D2.

---

## ADR-0027 - KP significator scope; clarification of root D-008 (ADR-0013 conflict 6)

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** Root D-008 names KP_SIGNIFICATOR_V1 as the next engineering tier and requires its
  methodology specification to be frozen before implementation. It was never superseded, while the
  2026-08-08/09 work spanned a much wider programme. `LOCK_MANIFEST.json` still records
  `tier1_kp_significator` as SPECIFICATION_PENDING.
- **Decision:**
  1. **D-008 is CLARIFIED, not superseded, and the two halves are separated.** Its **methodology
     requirement stands in full and is generalised**: a frozen, independently audited specification
     precedes implementation. Its **sequencing claim**, that KP significators are necessarily the
     next tier, is superseded by the dependency-driven order in ADR-0026. Nothing about D-008 implies
     authorisation to implement.
  2. **KP significators are NOT authorised for implementation.**
  3. **Four separately scoped items, never one feature.** KP significators; four-step; ruling
     planets; horary. Each requires its own specification, its own ADR and its own certification.
     Combining them into one vague feature is prohibited.
  4. A KP_SIGNIFICATOR specification MUST define, at minimum: exact methodology; source authority;
     houses considered; star, sub and sub-sub logic; four-step interpretation if applicable; ruling
     planets if included; cusp handling; retrograde treatment; node treatment; boundary behaviour;
     school and profile requirements; independent validation protocol; protected holdout; negative
     controls; acceptance criteria; and explicit non-claims.
  5. `LOCK_MANIFEST.json` tier entries are **not** edited by this entry. Whether that file is a live
     register or frozen legacy evidence is unresolved and is recorded as new question Q12.
- **Consequences:** The KP layer's certified scope remains chains and fact charts only. The boundary
  convention finding H-07, where the boundary-proximity indicator is blind to the sign boundary, is
  a prerequisite consideration for any significator work, since significators consume the chain.
- **Evidence:** Root `DECISION_LOG.md` D-008; `LOCK_MANIFEST.json` tier table;
  `docs/KP_CHAIN_SPEC.md` non-claims; `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-07.

---

## ADR-0028 - Disposition of ADR-0003 through ADR-0013, and the repository-wide consistency audit

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** The governance ratification pass requires an individual disposition for every
  entry from ADR-0003 to ADR-0013, and a repository-wide consistency audit against the reconciled
  position. Both are recorded here so that the disposition is a decision record rather than a
  conversational assertion.

### Decision 1. The available dispositions, and the one that is not available

`PROJECT_CONSTITUTION.md` section 11 reserves ratification to the named owner, and Q1, which names
the owner, is open. **No entry in this register can currently be Accepted by anyone**, including by
the author of this entry. "Accept as written" is therefore **not an available disposition**, and
recording one would be manufacturing approval.

The dispositions used below are:

| Disposition | Meaning |
|---|---|
| RETAIN | The entry stands as written. It remains PROPOSED. |
| RETAIN WITH RECORDED DEFECT | The entry stands, and a specific defect inside it is recorded here rather than corrected, because correcting a committed entry would falsify the append-only record. |
| SUPERSEDED IN PART | A later entry governs part of its subject. The entry is not withdrawn. |
| WITHDRAW | Not used. No entry below merits withdrawal. |

No entry is edited, renumbered or deleted by this decision.

### Decision 2. Per-entry disposition

| ADR | Subject | Disposition | Basis |
|---|---|---|---|
| 0003 | Structural reconciliation | RETAIN WITH RECORDED DEFECT | Decision 1 and 3 are reflected in the working tree, verified: the top-level set is `assets certification docs engine engineering examples knowledge legacy reports research schemas scripts specs tools`, which matches the entry's consequences exactly, with `app/` and `tests/` absent as decided. **Defect: the entry's own follow-up obligation was never discharged.** It flagged `NAMING_STANDARD.md` section 5 and `VALIDATION_STANDARD.md` section 1 for correction and required the naming conformance sweep to be re-run. Neither was done. See the audit below, findings C-01 and C-02. |
| 0004 | Identifier family correction | RETAIN | Completed by ADR-0014 and now mechanically enforced by `scripts/check_retired_identifiers.py` with a negative control. Nothing outstanding. |
| 0005 | Current-engine Tier-0 lock | RETAIN WITH RECORDED DEFECT | The lock, its scope, its version and its evidence stand. **Two defects.** First, its closing sentence states that the unmet `PROJECT_CONSTITUTION.md` section 12 condition 3 is addressed by ADR-0012; ADR-0012 is graha drishti and sign conventions and does not address certification reporting. The cross-reference is wrong. Second, and materially, **condition 3 is still unmet**: `scripts/certify_current_engine.py` writes only the machine-readable artifact and does not call `scripts/certification_support.emit`, so no human-readable report is generated from the same run. Nine of the eleven certifiers do call it; the two that do not are `certify_current_engine.py` and the superseded `certify_tier0.py`. **The one certifier covering the locked Tier-0 kernel is the one that does not meet the condition.** See finding C-03. |
| 0006 | KP lordship chain layer | SUPERSEDED IN PART | The layer, its scope and its evidence stand. Its reference to root D-008 is now governed by ADR-0027, which clarifies D-008 rather than superseding it and confirms that significators, four-step, ruling planets and horary remain unauthorised. Its stated consequence that `LOCK_MANIFEST.json` requires a KP_CHAIN entry is **not discharged**: that file records only `tier0_numerical_core`, `tier1_kp_significator`, `tier2_four_step` and `tier3_cil`. Whether it should be edited at all is Q12, so the gap is recorded and left open rather than closed by editing possible frozen evidence. See finding C-04. |
| 0007 | Vimshottari dasha layer | SUPERSEDED IN PART | The layer and its evidence stand. Its recorded three-way table duplication, referred to ADR-0013 conflict 2, is now dispositioned by ADR-0023 D3, which permits the duplication on the stated condition that it is tested rather than removed. The condition is only partly met; the missing legacy-to-engine comparison is new question Q11. |
| 0008 | Transit event layer | RETAIN | Nothing outstanding at governance level. The layer carries audit findings M-04 and M-05 on provenance, which are engineering findings recorded in `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` and are not authorised for remediation. |
| 0009 | Generic Varga framework; D3 | RETAIN | The framework/production distinction it draws is exactly the distinction the charter requires, and it holds. Note that `certification/ENGINE_CAPABILITY_INVENTORY.json` classifies the framework itself PARTIALLY CERTIFIED while D3 is CERTIFIED; that is consistent with this entry, not in tension with it. |
| 0010 | D12; certified-registry constant | RETAIN | Nothing outstanding. |
| 0011 | D7, D30, D2 | RETAIN | Nothing outstanding. The entry itself records that registering three vargas in one commit strained ENGINEERING_CONSTITUTION Principle 10. Self-recorded, not concealed, and no remedy is proposed for a completed commit. |
| 0012 | Parashari drishti; sign conventions | RETAIN | Both locked conventions stand and are enforced by a declaration gate. The entry's explicit substitution of `ARCHITECTURE_STATUS.md` item 5, which said "unify", is reaffirmed: renumbering would reopen locked behaviour. |
| 0013 | Open standards conflicts recorded | SUPERSEDED IN PART, and REMAINS OPEN | Each of its seven conflicts now has a disposition entry: 1, 2 and 3 by ADR-0023; 4 by ADR-0024 (Q6) and ADR-0025 (Q9); 5 by ADR-0022; 6 by ADR-0027; 7 by ADR-0026. **ADR-0013 is not closed**, because every disposing entry is itself PROPOSED. It remains the live record of the conflicts until the disposing entries are ratified, and it is the correct thing to read if the ratification does not happen. |

### Decision 3. Repository-wide consistency audit

Findings are recorded, **not corrected**. Each is a documentary or traceability defect. None of them
changes a calculated value, and none is authorised for remediation by the current task.

| ID | Finding | Verified by | Why it is not corrected here |
|---|---|---|---|
| C-01 | `docs/NAMING_STANDARD.md` section 5 states the closed top-level set as `docs/ engine/ knowledge/ research/ tests/ tools/ app/ examples/ assets/ schemas/`, citing ADR-0001..0003. That list contains `tests/` and `app/`, which ADR-0003 decisions 4 and 2 removed, and omits the six folders ADR-0003 decision 3 sanctioned. It is stale against both the tree and the decision it cites. | Line 86-87 of the file read directly; tree listed | NAMING_STANDARD is a STANDARD, above SPECIFICATIONS in the ADR-0022 hierarchy. Editing a standard to match an unratified ADR would give ADR-0003 effect it does not have. Left OPEN. |
| C-02 | `docs/VALIDATION_STANDARD.md` line 19 defines "Works" as an automated test in `tests/`. No top-level `tests/` exists; `pytest.ini` testpaths point at `engine/tests/`. ADR-0003 flagged this text for correction and it was not corrected. | File read; `pytest.ini` read | Same reason as C-01. Left OPEN. |
| C-03 | `scripts/certify_current_engine.py`, the certifier for the ADR-0005 Tier-0 lock, does not generate a human-readable report from the same run, so `PROJECT_CONSTITUTION.md` section 12 condition 3 remains unmet for the locked kernel. ADR-0005's claim that ADR-0012 addresses this is incorrect. | `grep` for `certification_support` across all eleven certifiers: 9 hit, `certify_current_engine.py` and `certify_tier0.py` do not; `reports/certification/` contains ten report pairs and none for the current engine | This is a code change to a certification runner inside locked scope. Not authorised, and not a documentation fix. Recommended as the highest-value next remediation. |
| C-04 | `LOCK_MANIFEST.json` records no KP_CHAIN entry despite ADR-0006 requiring one, and records `tier1_kp_significator` as SPECIFICATION_PENDING under a tier structure later work did not follow. | File read in full | Whether the file is a live register or frozen evidence is unresolved, which is exactly Q12. Editing it under either reading risks a governance violation. Left OPEN. |
| C-05 | `docs/MASTER_ARCHITECTURE.md` lines 28 and 30 still describe `app/` and top-level `tests/` as layers of the architecture. | File read | Same reason as C-01, and it is the same underlying staleness. Left OPEN. |
| C-06 | This register's own status header described ADR-0001 and ADR-0002 as "accepted entries". Both do carry `Status: Accepted`, dated 2026-07-11, before Q1 was raised. ADR-0022 states that nothing can currently be Accepted. The two statements are reconcilable only if the 2026-07-11 acceptances were owner acts recorded before the register adopted its current status vocabulary, which the repository does not evidence either way. | Entries and header read | **Recorded as a genuine ambiguity, not resolved.** Retroactively demoting two Accepted entries would rewrite the record; asserting they were owner-ratified would manufacture provenance. The header is updated below to state the ambiguity rather than to assert either reading. |
| C-07 | The register's numbering is non-monotonic: ADR-0018 appears between ADR-0013 and ADR-0014, and 0015 to 0017 are reserved and unissued. The `governance` CI job fails on this, and the remote branch is RED. | Remote CI run; header note lines 17-21 read | Under standing CEO HOLD. A remediation proposal exists and is **not approved**. Not touched. |

### Decision 4. What this entry does not do

It does not close ADR-0013. It does not ratify anything. It does not correct C-01 through C-07. It
makes no change to any calculation, test, certification artifact or gate.

- **Consequences:** Seven documentary defects are now on the record with their verification and with
  a stated reason for non-correction, which converts them from unknown risk into tracked risk. C-03
  is the one finding of the seven with substantive weight, because it means the constitution's own
  four-condition definition of Locked is not satisfied for the kernel that everything else depends
  on. That is recorded plainly rather than softened.
- **Evidence:** Every claim in the tables above was checked against the working tree at
  `c5bdd81` during this pass, by reading the cited file or running the cited search. No claim is
  carried over from an earlier report.

---

## ADR-0029 - Register ordering rule, and correction of the ADR numbering gate failure

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** The `governance` CI job's numbering step failed on the remote with two errors:
  `duplicate ADR numbers: [18]` and `ADR numbers not monotonic`, the observed sequence being
  `1..13, 18, 18, 14, 19..28`. Investigation found two distinct causes, and neither is a numbering
  error in the sense the gate was written to catch.

  **Cause of the duplicate.** The remote-CI evidence addendum was written with the heading
  `## ADR-0018 EVIDENCE ADDENDUM - remote CI validation (2026-08-11)`. The gate's regex,
  `^## ADR-(\d{4}) `, cannot distinguish an addendum from an entry, so it counted ADR-0018 twice.
  There was never a duplicate decision. An addendum is a child of its entry, and its heading level
  was wrong.

  **Cause of the non-monotonic order.** ADR-0018 was issued at Phase G commit 1 and ADR-0014 at
  Phase G commit 3, because the owner sequenced G6 first. Each was appended to the end of the file
  as it was written. **That is correct append-only behaviour, and it produced a file the gate
  rejects.** The register's stated rule "Append-only" and the gate's rule "numbers ascend in file
  order" are in direct conflict whenever a lower number is issued later. The register never stated
  which governs. That unstated conflict, not carelessness, is what turned the branch red.
- **Decision:**
  1. **The register is ordered by IDENTIFIER, not by append time.** A new entry is inserted at its
     numeric position. "Append-only" governs **content**: no entry is edited, renumbered or deleted
     after it is written. It does not govern **position**. This resolves the conflict by decision
     rather than by weakening either rule, and it is stated here because the register was silent.
  2. **An addendum is not an entry.** Evidence addenda, corrections of fact, and any other material
     attaching to an existing entry use a level-three heading of the form
     `### Evidence addendum to ADR-XXXX - <subject>`, so that the numbering gate counts decisions
     and only decisions.
  3. **Corrections applied, both purely positional or structural.** The addendum heading was demoted
     from `##` to `###`, and the ADR-0018 block together with that addendum was relocated to sit
     after ADR-0014. **No entry was renumbered, edited, deleted, split or merged.**
  4. **The gate is NOT weakened.** Its regex, its uniqueness assertion and its monotonicity
     assertion are unchanged. `.github/workflows/ci.yml` is not modified by this entry. The
     repository was corrected to satisfy the gate; the gate was not adjusted to tolerate the
     repository.
  5. The reserved-numbers note stands: ADR-0015 through ADR-0017 remain reserved and unissued for
     the remaining Phase G commits, and a gap in the sequence is not a monotonicity failure.
- **Consequences:**
  - **Byte-identity of the moved content is proven, not asserted.** SHA-256 over the extracted
    ADR-0014 block is `4af3498012250daa5dd91b4b6a7d6b2aa464a5241c02bfaad9e82e4bf60d51c7` before and
    after the move; over the ADR-0018 block including its addendum,
    `10cebd50fdefc4080398cdbb8e553f8560b8ca4a336b4005eb3dc8940673df53` before and after. Total line
    count is 1171 before and after. The only textual change in the file beyond this entry is the one
    heading level.
  - The gate now reports `PASS: 25 ADR entries, unique and monotonic: ADR-0001..ADR-0028`, sequence
    `1..14, 18..28`.
  - **ADR-0028 finding C-07 is thereby resolved**, and it is the only one of the seven consistency
    findings this pass closes. C-01 through C-06 remain open.
  - **A gap in the gate itself is recorded rather than fixed.** The identifier gate has a committed
    negative control in `.github/workflows/ci.yml`; the **numbering gate does not**. Its PASS is
    therefore weaker evidence than the identifier gate's PASS. A negative control was executed
    manually during this pass and behaved correctly, but a manual run is not a standing gate. Adding
    one is a workflow change and is not authorised here. Recorded as new question Q14.
- **Evidence:** Local reproduction of the original failure before correction, exit 1 with both
  errors; local execution after correction, exit 0; the two block hashes above; a manual negative
  control planting `## ADR-0018 - duplicate probe`, which the gate rejected with exit 1.

---

## ADR-0030 - Normative strengthening of the Q6 and Q9 decisions, and the complete ADR-0013 mapping

- **Date:** 2026-08-11
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** The CEO correction pass required that the Q6 and Q9 decisions read as architectural
  rules rather than as observations of current behaviour. On re-reading, ADR-0024 and ADR-0025 were
  found to be **weaker than intended in three specific respects**, recorded below. Because the
  register is append-only in content, those entries are not edited; this entry states the governing
  wording and takes precedence over them where they differ.
- **Decision:**

  **1. Q6, the engine-to-knowledge boundary. The two claims are separated explicitly.**

  *Empirical fact, as at commit `2a4ac9f`:* `engine/` contains **zero** runtime imports of top-level
  `knowledge/` and zero references to `knowledge/hlkg`. This is an observation. It could change with
  any commit and it binds nothing.

  *Normative architectural rule, which binds:*
  > **`engine/` MUST NOT have an uncontrolled runtime dependency on top-level `knowledge/`.**
  > Such a dependency is PROHIBITED unless and until a future explicit architectural decision
  > authorises a specific controlled interface, defining at minimum its version pinning, its schema
  > validation, its failure behaviour, and its effect on certification.

  **The narrowing "for certification-critical calculation" in ADR-0024 D1 is WITHDRAWN.** It left
  non-certification-critical runtime dependency implicitly permitted, which is not what was
  intended: a dependency that is harmless today becomes load-bearing the moment anything downstream
  consumes it, and the boundary would then have been crossed without a decision. The prohibition is
  unqualified.

  **No such controlled interface is introduced, specified or authorised by this entry.** The
  permitted case remains exactly what ADR-0024 D2 records: `engine/knowledge/`, which is
  implementation-owned rule data and a different thing from top-level `knowledge/` despite the name
  collision.

  **2. Q9, the kernel and the legacy reference. Four clauses, stated normatively.**

  > (a) `engine/` **is** the production calculation foundation. It is authoritative and is not
  > reimplemented for architectural aesthetics.
  >
  > (b) `legacy/` **remains** a historical and equivalence reference. It is the KP equivalence oracle
  > for ADR-0006 and the historical Tier-0 record.
  >
  > (c) **Retirement of `legacy/` REQUIRES an explicit future decision AND the completion of the
  > migration and certification requirements of `docs/LEGACY_KERNEL_MIGRATION.md`.** Both are
  > necessary. Neither alone is sufficient. This clause was missing from ADR-0025 D3, which stated
  > only that the migration condition is unmet; it did not state that a decision is also required.
  >
  > (d) **No retirement is implied, scheduled or foreshadowed by the current state**, and in
  > particular the empirical finding that `legacy/` is imported by five test modules and no
  > production module MUST NOT be read as evidence that retirement is close at hand or appropriate. A low
  > dependency count is not a retirement criterion.

  **3. The complete ADR-0013 conflict-to-disposition mapping**, recorded here as a single table
  because it was previously distributed across six entries and one summary row.

  | ADR-0013 conflict | Subject | Disposing entry |
  |---|---|---|
  | 1 | ENGINEERING_CONSTITUTION Principle 3 versus rule tables as Python literals | ADR-0023 |
  | 2 | KNOWLEDGE_STANDARDS single-source-of-truth versus the three-way Vimshottari duplication | ADR-0023 |
  | 3 | Three architecture documents placing the knowledge layer differently; the unsupported LOCKED status | ADR-0023 |
  | 4 | Q6 and Q9 answered in practice rather than by decision | ADR-0024 (Q6) and ADR-0025 (Q9), both strengthened by this entry |
  | 5 | Root D-00x and ADR-000x coexisting with no stated precedence | ADR-0022 |
  | 6 | Root D-008 naming KP_SIGNIFICATOR_V1 as the next tier | ADR-0027 |
  | 7 | PROJECT_BACKLOG Phase 1 before Phase 2 versus what was actually built | ADR-0026 |

  Every conflict maps to exactly one disposing entry, except conflict 4, which maps to two because
  it recorded two distinct questions in one item. ADR-0023 disposes of three conflicts because
  conflicts 1, 2 and 3 are one problem seen from three angles, which ADR-0023's context states.

  **4. No feature decision is contained in ADR-0022 through ADR-0030.** Verified by reading every
  decision clause in the seven prior entries and this one: each is a rule, a classification, a
  prohibition, a disposition or a documentation obligation. The only clauses that mention
  implementation do so to **withhold** authorisation: ADR-0027 D2 states that KP significators are
  not authorised, ADR-0026 D5 states that no phase is marked complete without evidence, and
  ADR-0024 D4 and this entry's clause 1 both prohibit rather than permit.
- **Consequences:**
  - Where ADR-0024 D1 and this entry's clause 1 differ, **this entry governs**, and the difference
    is a deliberate strengthening rather than a correction of an error of fact.
  - Where ADR-0025 D3 and this entry's clause 2 differ, **this entry governs**.
  - Nothing in `engine/`, `legacy/`, `knowledge/` or any test is changed by this entry. The
    prohibition it states is already satisfied.
- **Evidence:** Repository-wide search for runtime imports of top-level `knowledge/` from `engine/`,
  zero results, re-run this pass; the five `legacy/` importers re-confirmed as test modules;
  every decision clause of ADR-0022 through ADR-0028 re-read for feature content.

---

## ADR-0031 - Tier-0 same-run certification evidence repaired (ADR-0028 finding C-03)

- **Date:** 2026-08-13
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** ADR-0028 finding C-03 recorded that `scripts/certify_current_engine.py`, the certifier
  behind the ADR-0005 Tier-0 lock, wrote only the machine-readable artifact. Nine of the eleven
  certifiers already routed their output through `certification_support.emit`, which derives the
  human-readable report from the same dict it serialises; this one and the superseded
  `certify_tier0.py` did not. `PROJECT_CONSTITUTION.md` section 12 condition 3 was therefore unmet
  for the locked kernel that every other layer depends on.
- **Decision:**
  1. **Route the Tier-0 runner through the existing emitter.** `emit()` now writes the artifact, the
     human-readable report and the console transcript from THE SAME run and THE SAME result object.
     No second calculation is performed to produce the report, and no value is copied by hand.
  2. **The evidence contract is stated and rendered, not implied.** Both files now carry: source
     revision and working-tree cleanliness, engine version, execution timestamp, Python version,
     holdout case identity, reference binary, profile set, comparison counts, the three numerical
     maxima, the frozen tolerance, the Moshier fallback count, the failure list and the PASS/FAIL
     verdict.
  3. **Three additive, inert extensions to the shared emitter**, being the smallest change that
     renders the contract: an optional tolerance line, an optional run-metadata section, and an
     optional summary section, plus a verdict lookup that reads `summary.result` when no top-level
     `result` exists. **All four are no-ops for every artifact that predates this change**, which is
     proven rather than assumed: all ten existing reports re-render byte-identically.
     The verdict lookup exists specifically so the verdict is NOT duplicated into the artifact
     merely so the report can display it, which would create two places for it to be wrong.
  4. **A standing agreement gate with a real negative control**,
     `engine/tests/test_certification_evidence_agreement.py`. It re-derives every report from its
     artifact and demands byte equality across all eleven pairs, names the Tier-0 pair explicitly so
     discovery cannot silently drop it, asserts a floor of eleven pairs so a discovery bug cannot
     turn the gate into a no-op, and asserts that the Tier-0 report actually contains the contract
     fields, because agreement with an empty report would be worthless agreement. Six parametrised
     negative controls corrupt an in-memory copy and require the comparison to fail.
  5. **`source_revision` is observed, never asserted.** Where git is unavailable the fields read
     `unavailable` rather than being guessed. `working_tree_dirty` is recorded because a run over a
     modified tree is evidence about that tree and not about the named commit.
- **Consequences:**
  - **Constitution section 12 condition 3 is now satisfied technically. Formal Locked status is NOT
    thereby established.** Condition 4 requires a decision entry recording the lock, and ADR-0005 is
    PROPOSED because Q1 is open. **The correct description of Tier-0 remains "reported", not
    "Locked"**, and this entry does not change ADR-0005's status.
  - **Zero numerical change, proven three ways.** The committed pre-change artifact, a re-run in the
    repository, and a run in a fresh extracted tree with the evidence deleted first all produce
    identical per-case values, identical summaries, identical tolerance and an identical ayanamsa
    profile check. Comparisons 264 planets and 264 cusps per the two profiles combined; maximum
    planet error 0.00017942695649253437 arcsec; maximum ascendant error 0.00017634032474234118;
    maximum cusp error 0.0001795366415535682; Moshier fallbacks 0; result PASS.
  - **The artifact's serialisation changed from two-space to one-space indent**, because `emit()`
    writes at indent 1 as it does for the other ten artifacts, and it gained the `_artifact_name`
    and `_slug` keys the emitter records. No value changed. The artifact is regenerated current
    evidence by its own declared contract, not immutable historical evidence, so regenerating it is
    correct rather than a rewrite of protected material.
  - **A separate defect is recorded, not fixed: the artifact is not byte-reproducible.** Each case
    records `swetest_cmd` containing the run's temporary directory and the checkout's absolute path,
    so two runs of identical code on identical data produce different bytes. That is the same class
    of defect root D-005 removed from the legacy Tier-0 package. It does not affect condition 3,
    because both evidence files regenerate together and agree. Recorded as new question Q15.
  - **A second gap is recorded, not fixed:** this runner still does not call `preflight()`, so it
    verifies the swetest binary version but not the ephemeris checksums, and no anti-fitting scan
    forms part of this gate. That is VALIDATION_STANDARD section 2 rules 4 and 6, not section 12
    condition 3, and wiring it changes what the gate can reject. Recorded as new question Q16.
- **Evidence:** Live negative controls executed against the real on-disk evidence, not only in
  memory: hand-editing the report produced 3 test failures, altering the artifact produced 4, and
  after restoration both files hashed identically to their pre-control values, with the two source
  files unchanged. Default gate 415 passed, up from 404 by the 11 new agreement tests. Fresh
  extracted-tree run reproduced the certification from one command with all three evidence files
  regenerated from nothing.

---

## ADR-0032 - Tier-0 ephemeris integrity (resolves Q16), and the certification evidence provenance protocol

- **Date:** 2026-08-13
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** Two matters arising from the C-03 repair recorded in ADR-0031. First, the evidence
  committed at `7582407` records `source_revision: 4c14c05` and `working_tree_dirty: True`, which is
  not the commit that carries it, and the CEO required this be proven rather than explained away.
  Second, Q16 recorded that the Tier-0 runner verified the swetest binary's version but not the
  integrity of the ephemeris data.

### Decision 1. Evidence provenance: case A, proven, and a protocol so it stops recurring

**The evidence was NOT stale.** It represents the working tree that became `7582407`, and the
proof is a chain of three checked facts rather than a recollection:

  1. The certification run stamped `2026-08-13T08:03:44Z`. The commit `7582407` is timestamped
     `2026-08-13T08:04:39Z`, fifty-five seconds later.
  2. Every source file the certification depends on has a filesystem mtime EARLIER than the run:
     the runner at 07:59:45, the shared emitter at 08:02:40, and every engine module, the swetest
     binary and all three ephemeris files at 2026-08-10. **No source was modified after the run.**
  3. The working tree was clean at `7582407`, so the on-disk files equal the committed blobs.

  From (3) the committed blobs equal the on-disk files; from (2) the on-disk files at commit time
  equal those at run time; therefore **the committed tree contains exactly the implementation that
  was certified**. `working_tree_dirty: True` was truthful: at run time the tree differed from
  `4c14c05`, which is precisely what that field exists to say.

**Why this is nevertheless unsatisfactory, and the protocol that fixes it.** A reader should not
have to reconstruct mtimes to learn which commit was certified. The cause is structural: a run
must precede the commit that carries its output, so `HEAD` at run time is always the PREVIOUS
commit.

  **PROTOCOL, from this entry onward. Certification evidence is committed in two steps.**
  **Step 1** commits the implementation. **Step 2** re-runs the certifier against that clean
  committed tree and commits ONLY the regenerated evidence files. The evidence then records a real
  commit SHA with `working_tree_dirty: false`, and that SHA names the commit holding the certified
  implementation. The step-2 commit MUST change no implementation file, which is verifiable by
  diffing the two commits.

  This is bookkeeping discipline, not a redesign. Nothing in the runner changes to support it.

### Decision 2. Q16: ephemeris integrity is verified, using the existing mechanism

**The finding, stated precisely because the distinction is the whole point.** `resolve_swetest()`
executes the bundled binary and asserts the string `version 2.10.03`. That proves the ORACLE is the
pinned build. **It proves nothing whatsoever about the ephemeris DATA**, which is what both the
oracle and the engine actually read, and which is where a silent corruption would move every
number in the run while every version check still passed.

  1. **The runner calls `certification_support.preflight()` before anything else**, and records its
     result as `report["preconditions"]`, which the emitter already renders. No checksum logic is
     duplicated: this is the same `verify_data_assets()` the other nine certifiers use, and the same
     `CHECKSUMS.sha256` manifest.
  2. **Coverage is exact and is now asserted, not assumed.** `CHECKSUMS.sha256` lists
     `seas_18.se1`, `semo_18.se1` and `sepl_18.se1`. `engine.astronomy.ephemeris.REQUIRED_FILES`
     declares those same three, and `default_ephemeris_path()` resolves to the repository root,
     which is also the `-edir` the runner passes to swetest. **The engine and the independent oracle
     read the same three verified files.** A test asserts this correspondence so it cannot rot if
     either list changes.
  3. A precondition failure routes through `fail()`, exiting 3 with a legible message, matching the
     runner's existing convention rather than raising a traceback.
  4. The anti-fitting scan arrives with `preflight()` as a consequence, closing VALIDATION_STANDARD
     section 2 rule 6 for this runner at the same time as rule 4. 146 production modules scanned,
     zero findings.
  5. **The Tier-0 exemption in `engine/tests/test_certification_preconditions.py` is withdrawn.**
     That list carried the comment that Tier-0 "predates this requirement and is exempt until its
     runner is wired". It is wired, so the artifact is now held to the same standard as the other
     ten.
- **Negative controls.** Three committed, plus two demonstrated end to end.
  Committed: a copy-based control that corrupts one byte of a COPY of an ephemeris file and requires
  `CertificationFailure`; a control that deletes a copied asset and requires the same; and the
  coverage assertion above. Each verifies the copies PASS first, so the control cannot pass
  vacuously. Demonstrated: corrupting one byte of `semo_18.se1` in a full extracted copy made the
  certifier exit 3 with the expected and actual digests printed, and deleting `sepl_18.se1` made it
  exit 3 reporting the missing asset. **The real bundled reference data was never modified**, proven
  by a combined SHA-256 over the three ephemeris files and the manifest, identical before and after.
- **Consequences:**
  - **Zero numerical change.** Summary, tolerance, ayanamsa profile check and every per-case value
    are identical to the pre-C-03 committed artifact at `4c14c05`. 264 planet and 264 cusp
    comparisons; maxima 0.00017942695649253437, 0.00017634032474234118 and 0.0001795366415535682
    arcsec; zero Moshier fallbacks; PASS. Tolerance still 0.5 arcsec. The 11-case holdout, both
    profiles, and every calculation path are untouched.
  - Default gate 420 passed, from 415: three new precondition tests and two parametrised cases
    gained by withdrawing the Tier-0 exemption.
  - **Constitution section 12 is unaffected by this entry.** Condition 3 was repaired by ADR-0031;
    this closes a VALIDATION_STANDARD section 2 gap. **Condition 4 remains unmet and Tier-0 remains
    correctly described as "reported", not "Locked"**, because ADR-0005 is PROPOSED while Q1 is open.
    ADR-0005's status is not changed by this entry.
  - **Q15 remains OPEN and is deliberately not addressed.** The artifact is still not
    byte-reproducible, because each case records `swetest_cmd` containing the run's temporary
    directory and the checkout's absolute path.
- **Evidence:** mtime and commit-timestamp chain above; `CHECKSUMS.sha256` compared against
  `REQUIRED_FILES`; end-to-end controls exiting 3 with correct diagnostics; combined ephemeris
  hash unchanged; full gate 420 passed.

---

## ADR-0033 - Owner ratification: governance roles (Q1), ADR-0001 and ADR-0002 (Q13), and roadmap direction (Q8)

- **Date:** 2026-08-13
- **Status:** **ACCEPTED. This is the first owner-ratified entry issued by this register**, and it is
  the entry that makes ratification possible at all. It is accepted because the owner supplied the
  decisions below as an explicit ratification instruction, not because its author judged it correct.
- **Context:** Q1 asked who the named owners are. It has been open since 2026-07-11 and has blocked
  every other ratification: `PROJECT_CONSTITUTION.md` section 11 reserves ratification to the owner,
  so with no owner named, **no entry in this register could be Accepted by anyone**, and ADR-0022
  recorded that plainly. The owner has now supplied a ratification package covering Q1, Q13 and the
  direction half of Q8.

### Decision 1. Governance roles (Q1, ratified in part)

| Role | Holder |
|---|---|
| Project Owner, final ratifying authority | **Prashant Kumar** |
| Builder, researcher, executor | **Claude** |
| Independent CEO and technical auditor | **ChatGPT** |

Also ratified:

- The **repository** is the authoritative permanent project record for implementation, governance,
  specifications, certification and decision history.
- **Conversation is input material only and is never permanent authority.** This ratification is
  itself an instance of the rule: it was given in conversation, and it becomes authority only
  because it is written here.
- **Significant phase work MUST NOT be merged to main without CEO audit and owner authorisation.**

**Q1 is ratified IN PART and REMAINS OPEN in part.** Q1 asked for a docs owner, an engine owner and
a release owner. The package designated none of the three, and the instruction was explicit that a
required maintainer who has not been designated is left OPEN rather than guessed. **No additional
maintainer is invented.** Consequently the `| Owner | TBD (see Q1) |` field in all 42 document
status headers is left unchanged: those fields name a document maintainer, which is one of the three
undesignated roles, and filling them with the project owner's name would assert a delegation that
was not made.

**How this ratification is evidenced, stated rather than glossed.** It reached the repository through
a working session, and the repository has no mechanism to authenticate who issued it. That is a
real limitation of the current process, not a defect in this record. If the owner wants ratification
to be independently verifiable later, the durable forms are a signed commit or an owner-signed file
in the repository; neither is created here, because neither was requested.

### Decision 2. ADR-0001 and ADR-0002 ratified as written (Q13, resolved)

The owner ratifies **ADR-0001** and **ADR-0002** exactly as currently recorded. Their status lines
now record the ratification date, the ratifying owner, and that no substantive content changed. Not
one word of their context, decision or consequences is altered.

**No earlier conversation is claimed as the ratification.** Q13 asked whether their pre-existing
`Accepted` status was an owner act or an authoring artifact. That question is **not** answered by
this entry and does not need to be: the status is now legitimate prospectively, from 2026-08-13,
whatever its earlier provenance was. Q13 is resolved on that basis and the historical ambiguity is
left recorded rather than retrospectively decided.

A consequence worth naming: ADR-0001 fixes the canonical top-level folder set, and **ADR-0003
reconciled the tree against it and is still PROPOSED**. Ratifying ADR-0001 as written therefore
leaves a live tension, because the tree currently on disk is ADR-0003's, not ADR-0001's. This does
not require action now; it requires that ADR-0003 be ratified or rejected before anyone treats
either folder list as settled. Recorded so it is not discovered later.

### Decision 3. Roadmap direction ratified; Q8 NOT closed

The owner ratifies this dependency ordering:

> Foundation and Certification -> Question and Input Architecture -> Knowledge and Rule Architecture
> -> Dependency and Inference Architecture -> Evidence Architecture -> System-specific Interpretation
> -> Convergence -> Historical Validation and Learning -> API -> UI and Production

With five ratified qualifications:

1. **The ordering is dependency guidance, NOT automatic implementation authorisation.** Nothing in it
   authorises work to begin.
2. Existing certified astrology foundation work remains **valid historical foundation work**.
3. Astrology systems remain **independently implemented and independently evaluated**.
4. Convergence MUST preserve **provenance, dependency, correlation and uncertainty**.
5. **Structurally different domains MUST NOT be forced through one natal pipeline.**

**Q8 becomes OWNER-RATIFIED DIRECTION, FULL RESOLUTION STILL OPEN.** Full closure continues to
require, for every phase: prerequisites, entry criteria, scope, certification gates, exit criteria
and CEO approval requirements. Those exist only as the unratified candidate matrix in
`docs/Q8_CLOSURE_MATRIX.md`.

### Decision 4. PROJECT_CONSTITUTION section 12 condition 4, evaluated explicitly for ADR-0005

The instruction required this be evaluated rather than assumed, so the reasoning is set out in full.

Condition 4 reads: *"A decision log entry records the lock, its version, and its evidence."*
**ADR-0005 does record all three**: scope, engine 0.3.0, the two ratified profiles, and the 528
comparisons at a maximum error of 0.000180 arcsec. On a purely textual reading, condition 4 is met
by the entry's existence.

**That reading is rejected, and deliberately.** If a PROPOSED entry satisfied condition 4, then the
AI builder could satisfy every condition of "Locked" without any human act, since conditions 1, 2
and 3 are all machine-verifiable. "Locked" would become self-certifiable, which contradicts
`PROJECT_CONSTITUTION.md` section 11, contradicts the charter's anti-circularity rule, and would make
the constitution's own strongest status the easiest to claim. The governing reading is therefore that
condition 4 requires a **ratified** entry.

**Applying that reading: ADR-0005 was NOT included in this ratification package.** The owner ratified
ADR-0001, ADR-0002 and the Q8 direction. ADR-0005 remains PROPOSED.

**Therefore Tier-0 is NOT Locked, and MUST continue to be described as "reported".** The status is
unchanged by this entry.

What HAS changed is the nature of the blocker, and the change is substantial. Before this entry the
obstacle was that no ratifying authority existed. Now one does, and the remaining conditions stand
as follows: condition 1 met, a frozen profile and specification exist; condition 2 met, a fresh
extracted tree reproduces the certification from one command with zero skips; condition 3 met by
ADR-0031, machine-readable and human-readable evidence generated by the same run and agreeing
byte-for-byte, defended by a gate with working negative controls; condition 4 **unmet, and now
unmet for exactly one reason: ADR-0005 has not been ratified.**

**Tier-0 is one owner decision away from Locked.** That decision is not taken here and MUST NOT be
inferred from this entry.

The textual ambiguity in condition 4 is recorded as new question Q17, because the reading adopted
above is a governing interpretation made by the builder and should be confirmed or corrected by the
owner rather than left as precedent by default.

- **Consequences:**
  - **ADR-0022's statement that no entry can currently be Accepted by anyone is superseded from this
    date.** An authority now exists. **Every other entry in this register nevertheless remains
    PROPOSED**, because ratification is per-entry and only ADR-0001, ADR-0002 and this entry have
    received it. A reader must not read "an owner exists" as "the register is ratified".
  - Q1 resolved in part, Q13 resolved, Q8 direction ratified with full closure still open, Q17 raised.
  - Nothing else changes. No code, no calculation, no certification artifact, no gate, no workflow.
  - Explicitly NOT addressed, by instruction: Q11, Q12, Q14, Q15, and consistency findings C-01,
    C-02, C-04, C-05, C-06.
- **Evidence:** The owner's ratification instruction of 2026-08-13; `PROJECT_CONSTITUTION.md`
  sections 11 and 12 read in full; ADR-0005 re-read for what it does and does not record;
  `certification/current_engine_certification.json` and
  `reports/certification/current_engine.report.md` at `d951caf` for the condition 1, 2 and 3
  assessment.

---

## ADR-0034 - Tier-0 formally LOCKED: owner ratification of ADR-0005 and verification of all four Constitution s12 conditions

- **Date:** 2026-08-13
- **Status:** **ACCEPTED**, on the owner's lock authorisation of 2026-08-13.
- **Context:** ADR-0033 D4 evaluated `PROJECT_CONSTITUTION.md` section 12 for Tier-0 and found
  conditions 1, 2 and 3 met and condition 4 unmet for exactly one reason: ADR-0005 had not been
  ratified. It recorded that Tier-0 was one owner decision away from Locked, and that the decision
  must not be inferred. The owner has now taken it.

### Decision 1. ADR-0005 is ratified, and Tier-0 is formally LOCKED

The owner ratifies **ADR-0005 exactly as written**. Its scope, version, ratified profiles, frozen
tolerances and evidence are unchanged. **No numerical value is restated, revised or re-derived by
this entry.**

**TIER-0 IS FORMALLY LOCKED as of 2026-08-13.**

### Decision 2. The four conditions, verified individually

The constitution requires ALL four. Each is stated with what actually satisfies it, because a lock
asserted without this table is the defect ADR-0005 was written to correct in the first place.

| # | Condition | Status | What satisfies it |
|---|---|---|---|
| 1 | A written specification or frozen profile exists | **MET** | Two frozen `CalculationProfile` definitions, `parashari_lahiri` (SIDM 1) and `kp_krishnamurti` (SIDM 5), owner-signed 2026-08-08; frozen numerical authority and tolerances at root D-001 to D-004; `certification/CURRENT_ENGINE_LOCK.json` |
| 2 | A reproducible verification run passes per VALIDATION_STANDARD: fresh environment, one command, zero skips, independent reference | **MET** | `python3 scripts/certify_current_engine.py` reproduced from a freshly extracted tree with all evidence deleted first, exit 0; default gate 420 passed, **zero skipped**; independent reference is the bundled Astrodienst swetest 2.10.03 C binary, version-asserted at runtime; ephemeris integrity verified against `CHECKSUMS.sha256` per ADR-0032 |
| 3 | Machine-readable results and a human-readable report generated by that same run, agreeing exactly | **MET** | Repaired by ADR-0031. `certification_support.emit()` writes `certification/current_engine_certification.json`, `reports/certification/current_engine.report.md` and the console transcript from one run and one dict. Defended by `engine/tests/test_certification_evidence_agreement.py`, which re-derives every report from its artifact and demands byte equality, with six in-memory and two live negative controls proven to fail on disagreement |
| 4 | A decision log entry records the lock, its version and its evidence | **MET, AS OF THIS ENTRY** | ADR-0005 records the lock, engine version 0.3.0, scope and evidence, and is now **owner-ratified**. Decision 1 above is what changed |

**Condition 4 and the Q17 interpretation.** ADR-0033 D4 had to decide whether condition 4 requires a
*ratified* entry or merely an *existing* one, and adopted the stricter reading so that "Locked" could
not be self-certified by the builder. **That question is now moot for Tier-0: under either reading,
condition 4 is met**, because ADR-0005 both exists and is ratified. **Q17 nevertheless remains OPEN**
as a general interpretive question, since it will govern every future lock, and the stricter reading
should be confirmed by the owner rather than inherited as precedent from this case.

### Decision 3. The certified tree, identified exactly

The evidence in the repository was produced by a run against commit
`d951caf941d832aca17d77e8807c8cbf7a72a049` with a clean working tree, per the ADR-0032 provenance
protocol. Two commits have followed. **Neither touched a single implementation file**, and that is
proven by git tree hashes rather than asserted:

| Path | `d951caf` | `e203320` |
|---|---|---|
| `engine/` | `0790a968aaa9ed0f8691efb498cbae1d0bec3861` | identical |
| `scripts/` | `cf098034318e74beba15cef1653eccb0cf621eda` | identical |
| `legacy/` | `7b9fc652cdb03e0c09294c49611a3964041ecd75` | identical |
| `CHECKSUMS.sha256` | `0885f0446ba4306c7afa78eef06a0be2e7b6c5a7` | identical |
| `seas_18.se1` | `8f900cab7e557e4c41f758a6bf3a3c3967e7e3db` | identical |
| `semo_18.se1` | `5427d9f885fd6cb9489584ade37e52c6abb4d407` | identical |
| `sepl_18.se1` | `786702cd04506371ee6223af1ebac02d54c848b8` | identical |
| `swetest` | `1829dd062a09dde15711a9ae5f4fb070952e02c1` | identical |

The five files changed since `d951caf` are three governance documents and the two evidence files
regenerated by the protocol's own second step.

Per that protocol a confirming run is executed against the clean tree at the commit carrying this
entry, and its evidence is committed immediately after, so the locked commit and the evidence's
recorded `source_revision` are the same SHA. **That run confirms; it does not re-derive.** If it had
produced any different number the lock would not have been recorded, and the divergence would have
been reported instead.

### Decision 4. The locked numbers, restated for the record and unchanged

Frozen tolerance 0.5 arcsec (root D-002), categorical tolerance zero (root D-003). 11-case holdout
across both ratified profiles: 264 planet comparisons and 264 cusp comparisons, 528 in total.
Maximum planet error 0.00017942695649253437 arcsec, maximum ascendant error
0.00017634032474234118 arcsec, maximum cusp error 0.0001795366415535682 arcsec. Ayanamsa separation
between the two profiles 5.811157757093781 arcmin. Zero Moshier fallback events, zero failures,
result PASS.

These are the values already in the artifact. **Nothing here recomputes or rounds them.**

- **Consequences:**
  - **Change control tightens immediately.** Any change inside the locked scope, being the
    astronomical calculation kernel and the certified D9/D10 divisional mathematics, now requires a
    formal change decision, regression, independent validation and recertification, plus a further
    ADR. The lock is not a badge; it is a constraint on future edits.
  - **Three statements in committed entries are superseded from this date, and are NOT edited**,
    because the register is append-only in content: ADR-0031's and ADR-0032's consequence blocks and
    ADR-0033 D4 each state that Tier-0 remains "reported", not "Locked". Each was true when written.
    **This entry supersedes all three**, and a reader encountering them must read them as dated
    record. `docs/PROJECT_ROADMAP.md`, being a living summary rather than a dated decision, is
    updated in place.
  - **What is NOT locked, restated because a lock invites over-reading.** The lock covers the
    astronomical kernel and the certified D9/D10 mathematics **only**. It does not cover the registry
    vargas D2, D3, D7, D12 and D30, which have their own certifications; nor the KP, dasha, transit
    or drishti layers, which have theirs; nor dignity data, which sits outside lock scope; nor
    polar-circle house behaviour beyond 64.1 degrees north, which remains NOT VERIFIED; nor any of
    the absent capabilities listed in `certification/ENGINE_CAPABILITY_INVENTORY.json`. Panchanga and
    rise/set are Tier-0 by ADR-0020 D2 and are **not** retroactively brought inside this lock.
  - **C4 is not C5.** Tier-0 being Locked means the calculations are certified against an independent
    numerical authority. It says nothing about astrological validity, and MUST NEVER be represented
    as prediction validation.
  - **Q15 is unaffected and remains OPEN.** The artifact is still not byte-reproducible across runs,
    because `swetest_cmd` records the run's temporary directory and the checkout's absolute path.
    That is a reproducibility annoyance, not a condition-2 failure: condition 2 requires the run to
    reproduce, and it does, with every number identical.
  - **A finding bearing on Q12, recorded but not resolving it.**
    `certification/CURRENT_ENGINE_LOCK.json` states that `LOCK_MANIFEST.json` is deliberately left
    untouched because it describes the LEGACY kernel exclusively, per audit finding F-17. That is
    material evidence for Q12 and was not visible when Q12 was raised. Q12 asks what the file is FOR
    and whether it is live or frozen, which this does not answer, so **Q12 stays OPEN** and
    `LOCK_MANIFEST.json` is not edited.
- **Evidence:** Owner's lock authorisation of 2026-08-13; `PROJECT_CONSTITUTION.md` section 12 read
  in full and evaluated condition by condition; git tree hashes above; ADR-0031 and ADR-0032 for
  conditions 3 and 2; `certification/current_engine_certification.json` and
  `reports/certification/current_engine.report.md`, same-run and byte-agreeing.

---

## ADR-0035 - Owner ratification of ADR-0009, ADR-0010 and ADR-0011: the registry vargas

- **Date:** 2026-08-13
- **Status:** **ACCEPTED**, on the owner's ratification of 2026-08-13.
- **Context:** ADR-0009, ADR-0010 and ADR-0011 record the Generic Varga framework entering production
  use and the five registry vargas built on it. All three had been PROPOSED since 2026-08-09, blocked
  first by Q1 and then simply by not having been put to the owner. The owner has now ratified all
  three exactly as written.

### Decision 1. What is ratified

| Entry | Subject ratified |
|---|---|
| **ADR-0009** | The Generic Varga framework enters production use. **D3 Drekkana**, Parashara variant (the sign itself, the 5th, the 9th), under the `parashara` school key, expressed as frozen `SegmentVargaRule` literals because `CyclicVargaRule` cannot express the drekkana's four-sign jumps. D9 and D10 are **NOT** migrated and the registry continues to refuse those divisions by contract |
| **ADR-0010** | **D12 Dwadasamsa**, twelve 2.5-degree parts from the sign itself forward, as frozen `CyclicVargaRule` literals; and `engine.astrology.CERTIFIED_PRODUCTION_VARGAS` as the single source of truth for sanctioned registry state |
| **ADR-0011** | **D7 Saptamsa** (odd signs from the sign itself, even from the seventh, forward), **D30 Trimsamsa** (unequal tara-graha segments 5/5/8/7/5 odd and reversed even, no luminaries), **D2 Hora** (two 15-degree halves with a deliberately two-sign Leo/Cancer output space) |

Ratified **as written**. Every rule table, boundary convention, school key, non-claim and
certification figure stands unaltered. **No implementation, calculation, rule table, tolerance or
certification artifact is touched by this entry**, and no certification is re-run or re-derived.

### Decision 2. Three things the owner is accepting that are easy to miss

Stated explicitly because ratifying "as written" means ratifying the caveats the entries recorded
about themselves, and those caveats should not pass silently into an approval.

**1. The D7 ULP finding.** ADR-0011 records that D7's 30/7-degree segment widths are not
binary-representable, that six points of the 51,429-point sweep land one ULP below a boundary, and
that the locked promote-up convention governs there, with the independent references carrying that
tolerance explicitly. **That numerical caveat is now owner-accepted**, not resolved. It is the
correct treatment, and it remains a documented edge in the D7 rule rather than an absence of one.

**2. ADR-0011's self-recorded process exception.** That entry registered three vargas in a single
commit and says so, noting it strains `engineering/ENGINEERING_CONSTITUTION.md` Principle 10, one
logical change per commit, and the README's own "one at a time" rule. Ratifying as written accepts
that exception for that historical commit. **It sets no precedent**: future vargas follow
`docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md` and Principle 10.

**3. Framework certification is still not per-varga certification.** ADR-0009's central constraint is
ratified along with the rest: the framework is infrastructure. `ENGINE_CAPABILITY_INVENTORY.json`
classifies the framework itself PARTIALLY CERTIFIED while each registered varga is CERTIFIED
individually, and those two statements are consistent rather than in tension.

### Decision 3. Constitution s12 evaluated for the registry vargas. They are NOT Locked

Evaluated explicitly rather than assumed, because Tier-0's lock followed a ratification and the
pattern invites the inference that this one does too. **It does not.**

| # | Condition | State for D2, D3, D7, D12, D30 |
|---|---|---|
| 1 | Written specification or frozen profile | **MET.** Frozen rule literals plus `docs/VARGA_REGISTRY_SPEC.md` |
| 2 | Reproducible verification run | **MET.** Each certifier reproduces from one command; each calls `preflight()`, so ephemeris integrity and the anti-fitting scan are part of every gate |
| 3 | Same-run machine and human evidence, agreeing | **MET.** All five certifiers route through `certification_support.emit()`, and `engine/tests/test_certification_evidence_agreement.py` re-derives each report from its artifact and demands byte equality |
| 4 | A decision log entry records **the lock**, its version and its evidence | **NOT MET.** |

**Condition 4 fails for a reason that ratification cannot fix.** ADR-0009, ADR-0010 and ADR-0011
record **certifications**, not locks. No entry in this register declares a lock over any registry
varga, so there is no lock for a decision entry to record. Ratifying a certification entry makes the
certification owner-endorsed; it does not manufacture a lock that was never declared.

**Therefore no registry varga is Locked, and none may be described as such.** D2, D3, D7, D12 and D30
are **owner-ratified CERTIFIED**, which is a real and useful status and is not the same status
Tier-0 now holds. Locking any of them would require a fresh decision entry declaring the lock, its
scope and its evidence, and a separate owner authorisation. Neither exists and neither is implied
here.

### Decision 4. A dependency tension, recorded rather than left to be discovered

**ADR-0012 is NOT in this ratification package and remains PROPOSED**, and it is the entry that fixes
the sign convention these vargas emit: "every varga sign output is 0-based, including certified
D9/D10 and all registry vargas", enforced by the `SIGN_FIELD_CONVENTIONS` declaration gate.

So the five vargas ratified here produce outputs whose **interpretation convention is defined by an
unratified entry**. Nothing is wrong in the code, and the certifications are unaffected: the
convention is locked in behaviour and mechanically enforced. But the governance record is
asymmetric, and a reader could reasonably ask by what authority a ratified varga's output index is
read 0-based. **The clean resolution is to put ADR-0012 to the owner**; it is recommended and not
assumed.

This is the same class of tension ADR-0033 D2 recorded between ratified ADR-0001 and unratified
ADR-0003, and it is recorded for the same reason: ratification proceeding entry by entry will keep
producing these until the register is either fully ratified or the gaps are deliberate and known.

- **Consequences:**
  - Accepted entries in this register become **eight**: ADR-0001, ADR-0002, ADR-0005, ADR-0009,
    ADR-0010, ADR-0011, ADR-0033, ADR-0034, and this entry makes nine. Everything else remains
    PROPOSED, and in particular ADR-0003, ADR-0004, ADR-0006, ADR-0007, ADR-0008, ADR-0012,
    ADR-0013, ADR-0014 and ADR-0018 through ADR-0032 are not ratified by this entry.
  - **The Tier-0 lock is untouched.** ADR-0005, ADR-0034 and
    `certification/CURRENT_ENGINE_LOCK.json` are not modified, and the certified numerical evidence
    for Tier-0 is not regenerated. The registry vargas sit **outside** the Tier-0 lock scope, which
    ADR-0034 restated as the kernel and the certified D9/D10 mathematics only.
  - **C4 is not C5**, restated because ratification of five certifications in one act is exactly
    where that slippage would start. These vargas are certified as calculations against independent
    references. Nothing here says any varga predicts anything.
  - The vargas that remain **ABSENT** are unaffected and unchanged: D4, D16, D20, D24, D27, D40, D45
    and D60 do not exist, and ratifying the framework does not bring them any closer to existing.
  - **Recommended next ratification, not taken here: ADR-0012**, for the reason in Decision 4, and
    then ADR-0006, ADR-0007 and ADR-0008, which are the remaining certified production layers.
- **Evidence:** ADR-0009, ADR-0010 and ADR-0011 re-read in full before ratification;
  `certification/VARGA_D2_V1_certification.json`, `VARGA_D3_V1_certification.json`,
  `VARGA_D7_V1_certification.json`, `VARGA_D12_V1_certification.json` and
  `VARGA_D30_V1_certification.json` confirmed present, each PASS, each citing a compliant decision
  identifier; all five certifiers confirmed to call both `preflight()` and `emit()`; register
  searched for any varga lock declaration, none found.

---

## ADR-0036 - Owner ratification of ADR-0012: Parashari graha drishti and the locked sign conventions

- **Date:** 2026-08-13
- **Status:** **ACCEPTED**, on the owner's ratification of 2026-08-13.
- **Context:** ADR-0035 D4 recorded an asymmetry created by per-entry ratification: the five registry
  vargas had been ratified, while ADR-0012, the entry that fixes the sign convention their outputs
  are read under, remained PROPOSED. The recommendation was to put ADR-0012 to the owner. The owner
  has now ratified it exactly as written.

### Decision 1. What is ratified

**Decision (a), aspects.** `engine/parashari/` as the first school layer above the shared primitives,
implementing full (purna) graha drishti facts only: every graha aspects the seventh, Mars
additionally the fourth and eighth, Jupiter the fifth and ninth, Saturn the third and tenth, by
inclusive whole-sign counting. **Node-cast aspects remain excluded from certified behaviour because
traditions genuinely disagree**, and the variant is recorded rather than chosen silently. Fractional
sputa drishti, Jaimini rashi drishti, Western aspects, yogas, strengths and interpretation remain
non-claims.

**Decision (b), sign conventions.** Do NOT renumber. **Every varga sign output is 0-based, including
certified D9/D10 and all registry vargas; every rashi-level output is 1-based. Both are locked.** The
inert `Sign` value type, the additive opposite-convention accessors, and the
`engine.astrology.sign_conventions` declaration with a collected gate that fails on any undeclared
field are all ratified.

Ratified **as written**. No rule, convention, gate, non-claim or certification figure is altered, and
**no calculation code or certification artifact is touched by this entry**.

### Decision 2. The asymmetry ADR-0035 D4 recorded is CLOSED

The registry vargas D2, D3, D7, D12 and D30 are owner-ratified, and the convention under which their
sign outputs are read is now owner-ratified too. **A reader can now answer "by what authority is a
ratified varga's output index read 0-based" by pointing at a ratified entry.**

Two things this does NOT close, stated so the closure is not over-read:

- **ADR-0006, ADR-0007 and ADR-0008 remain PROPOSED**, so the KP chain, Vimshottari and transit
  layers are certified but not owner-ratified. They are the remaining certified production layers.
- **The ADR-0001 versus ADR-0003 tension recorded in ADR-0033 D2 is untouched.** Ratified ADR-0001
  still fixes a top-level folder set that unratified ADR-0003 reconciled away.

### Decision 3. Constitution s12 evaluated. NOT declared Locked, and the reason is deliberate

This entry needs a more careful evaluation than ADR-0035 did, because **ADR-0012 decision (b)
actually contains the words "Both are locked"**. Unlike the varga certification entries, there is a
lock claim here for a decision entry to record. So the question is live rather than trivially
answered, and it is answered as follows.

| # | Condition | State for the sign conventions |
|---|---|---|
| 1 | Written specification or frozen profile | **MET.** `docs/SIGN_CONVENTION_SPEC.md` |
| 2 | Reproducible verification run | **MET.** `scripts/certify_sign_convention.py` runs from one command and calls `preflight()`, so ephemeris integrity and the anti-fitting scan gate it |
| 3 | Same-run machine and human evidence, agreeing | **MET.** Routes through `certification_support.emit()`; covered by the byte-equality agreement gate |
| 4 | A decision log entry records the lock, **its version** and its evidence | **ARGUABLY MET, NOT DECLARED** |

**Condition 4 is not asserted, for two independent reasons, either of which is sufficient.**

**First, no lock authorisation was given.** When Tier-0 was locked the owner supplied a separate,
explicit instruction: "I approve formally locking Tier-0." The present instruction ratifies ADR-0012
and says nothing about locking. Ratification and lock authorisation have been kept as distinct owner
acts throughout, and inferring the second from the first would be manufacturing an owner act. That is
the one thing this register exists to prevent.

**Second, ADR-0012 does not state a version.** Condition 4 requires the entry to record the lock,
**its version**, and its evidence. ADR-0005 recorded engine 0.3.0. ADR-0012 records the lock and the
evidence but no version for the locked convention. On a strict reading condition 4 is therefore not
satisfied on its own terms, independently of the authorisation point.

**Consequently the sign conventions are OWNER-RATIFIED and LOCKED IN BEHAVIOUR, but are NOT a
Constitution s12 Locked artifact, and MUST NOT be described as one.** The distinction is not
pedantry: "locked" in ADR-0012 means the numbering will not be changed and a gate enforces it, which
is true and mechanically verified. "Locked" in section 12 is a formal status with four conditions and
a change-control consequence. Tier-0 holds the second. The sign conventions hold the first.

Recorded as new question **Q18**, because ADR-0012 is unlikely to be the only ratified entry
containing lock language, and whether such entries become s12 Locked artifacts should be decided once
rather than case by case.

### Decision 4. What the ratification accepts that is easy to miss

**The explicit substitution of ARCHITECTURE_STATUS.md item 5.** That document required the sign
conventions be *unified*. ADR-0012 declined, on the grounds that renumbering would reopen locked
behaviour, and said so openly. **Ratifying as written accepts the substitution**: the requirement to
unify is superseded, and dual conventions with a declaration gate are the ratified design.
`ARCHITECTURE_STATUS.md` is not edited by this entry; its item 5 stands as dated record, superseded
by ratified ADR-0012.

**Node-cast aspects are excluded by decision, not by omission.** Ratifying decision (a) ratifies that
exclusion. Any future node-aspect work is a new decision with its own school attribution, not a gap
to be quietly filled.

- **Consequences:**
  - Accepted entries become **eleven**: ADR-0001, ADR-0002, ADR-0005, ADR-0009, ADR-0010, ADR-0011,
    ADR-0012, ADR-0033, ADR-0034, ADR-0035 and this entry. Still PROPOSED: ADR-0003, ADR-0004,
    ADR-0006, ADR-0007, ADR-0008, ADR-0013, ADR-0014 and ADR-0018 through ADR-0032.
  - **Every certified varga layer and its governing convention are now owner-ratified together.**
    That is the substantive gain: the varga stack no longer rests on an unratified foundation.
  - The Tier-0 lock, ADR-0005, ADR-0034 and `certification/CURRENT_ENGINE_LOCK.json` are untouched,
    and no certified numerical evidence is regenerated.
  - **C4 is not C5.** Ratifying a drishti certification says the aspect facts are computed correctly
    by the stated rule. It says nothing about what an aspect means or predicts.
  - **Recommended next ratifications, not taken here:** ADR-0006, ADR-0007 and ADR-0008, the three
    remaining certified production layers, and then ADR-0003, whose tension with ratified ADR-0001 is
    the oldest unresolved governance asymmetry in the register.
- **Evidence:** ADR-0012 re-read in full before ratification; `docs/SIGN_CONVENTION_SPEC.md` and
  `docs/PARASHARI_DRISHTI_SPEC.md` confirmed present;
  `certification/PARASHARI_DRISHTI_V1_certification.json` and
  `certification/SIGN_CONVENTION_V1_certification.json` confirmed present and PASS; both certifiers
  confirmed to call `preflight()` and `emit()`; `ARCHITECTURE_STATUS.md` confirmed present at the
  repository root, so the substitution ADR-0012 records is a substitution of a live document.

---

## ADR-0037 - Owner ratification of ADR-0006, ADR-0007 and ADR-0008; Phase G audit; authorised remediation

- **Date:** 2026-08-13
- **Status:** **ACCEPTED as to Decision 1**, on the owner's ratification of 2026-08-13.
  **PROPOSED as to Decisions 2 through 5**, which are the builder's audit findings and remediation.
- **Context:** The owner ratified ADR-0006, ADR-0007 and ADR-0008 and directed a single end-to-end
  audit of the remaining Phase G governance and certification state, with remediation of whatever
  existing decisions already authorise, so that the same ground is not re-covered repeatedly.

### Decision 1. ADR-0006, ADR-0007 and ADR-0008 ratified as written

| Entry | Subject ratified |
|---|---|
| **ADR-0006** | The isolated `engine/kp/` package: exact-rational lordship chains and KP fact charts under the `kp_krishnamurti` profile **only**; the legacy `Decimal(str(x))` conversion rule and `[start, end)` interval ownership preserved verbatim as the KP layer's documented numeric contract, deliberately differing from the engine-wide 1e-10 promote-up convention; mean node asserted; nothing retired from `legacy/` |
| **ADR-0007** | The isolated `engine/dasha/` package: Vimshottari maha, antar and pratyantar in exact rational arithmetic; **year length an EXPLICIT field with no hidden default**, certified against the mean sidereal year 91314091/250000 days exactly; school-explicit seeding recorded in provenance; depths 1 to 3 only |
| **ADR-0008** | The isolated `engine/transits/` package: longitude-crossing events by station-aware bisection on the certified position pipeline; sign and nakshatra ingresses, returns and natal conjunctions; retrograde multiplicity reported and direction flagged; a natal-relative view that **refuses mixed-profile comparison**; event-time guarantee 1e-6 day, residual bound 1e-4 arcsec |

Ratified as written. Every scope boundary, numeric contract, boundary convention, profile
restriction and non-claim stands unaltered.

**Two caveats the ratification carries, named so they do not pass silently.** ADR-0007 ratifies a
genuinely contested classical convention: dasha year length has five defensible values and the
choice moves period boundaries by days to months over a lifetime. What is ratified is that the
choice is **explicit and certified**, not that it is the only right one; other conventions remain
non-claims each needing its own entry. ADR-0008 ratifies an evidence position that records its own
limit: the 24 sankranti anchors were compared under per-event tolerances derived from a measured
~20.5 arcsec oracle Sun divergence **whose cause is recorded NOT VERIFIED**, per root D-007. That
divergence is accepted as handled, not as explained.

**These layers are NOT Constitution s12 Locked**, for the same reason ADR-0035 D3 gave: they record
certifications, not locks, so condition 4 has no lock to record. `certification/` carries no lock
artifact for KP, dasha or transits. Ratified CERTIFIED is a real status and is not the status
Tier-0 holds.

### Decision 2. The audit, and where its findings live

Two independent read-only audits were run by separate agents, one over the CI workflow and one over
every entry from ADR-0013 to ADR-0036, both instructed to find over-claiming rather than to confirm.
The full record is `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md`.

**Verdict: no BLOCKER.** No calculation, tolerance, holdout, certified artifact or gate produces a
wrong result. Every finding is governance, traceability or evidence scope.

**The finding that matters most is where the defects clustered.** They are concentrated in the
*evidence citations of the governance entries*, ADR-0022 through ADR-0028, and in three CI step
names. They are not in the certification entries. **Governance prose was written to a lower
evidential standard than the certification work it governs**, which is the wrong way round, and it
was not found by re-reading those entries: it took independent agents checking every citation
against the tree.

**Corrections to committed entries, recorded here and NOT edited into them**, because the register
is append-only in content:

- **ADR-0022's evidence is wrong in part.** "D-001, D-002, D-003, D-007 cited live in
  `scripts/certify_*.py`": `D-003` and `D-004` appear **zero** times under `scripts/`. D-003 is cited
  live, but in `engine/kp/intervals.py`, `engine/kp/tables.py` and two KP tests. The substantive
  claim, that D-001 to D-007 are operative rather than historical, stands. The cited proof does not.
- **ADR-0025 and ADR-0030's `legacy/` importer claim is wrong as worded.** The set is **seven**, not
  five: the four `engine/tests/` modules named, plus root-level `test_tier0_certification.py`, plus
  **`scripts/certify_kp_chain.py`, which is a certification runner and not a test module**. The claim
  was phrased repo-wide and evidenced `engine/`-scoped. What survives, and it is the part that
  matters, is that **no production module imports `legacy/`**.
- **ADR-0028's row for ADR-0003 is wrong.** It asserts the tree "matches the entry's consequences
  exactly". It does not: the consequences omit `schemas/`, which exists, and nothing declares
  `.github/`, which exists and holds the entire CI apparatus. See Q20.
- **ADR-0014's preserved-citation counts are wrong.** `reports/ALIGNMENT_REVIEW.md` has three
  occurrences on one line, not one; the entry switched from counting occurrences to counting lines
  mid-paragraph. The register's own count has grown from 10 to 36 and the allowlist bounds nothing.
- **ADR-0032 counts three committed ephemeris negative controls; two exist.** The third is a
  positive coverage assertion. Both real controls are properly constructed.
- **ADR-0035 D2.1 ratifies a D7 caveat that is not in the D7 artifact.** The "six sweep points, one
  ULP" finding lives in the varga registry spec, the roadmap and a test comment, not in
  `certification/VARGA_D7_V1_certification.json`.

### Decision 3. Remediation executed, because existing decisions already authorise it

| Item | What was done | Verification |
|---|---|---|
| **Q11** | Direct value-identity of all three Vimshottari tables, `legacy/kp.py`, `engine/kp/tables.py`, `engine/dasha/tables.py`, with **no cross-import**, closing the leg ADR-0023 D3's permission depends on. Each table is additionally compared against an **independently transcribed classical sequence**, because three identical wrong tables would pass a mutual comparison | 24 tests, including 7 perturbation controls that each assert the mutation is real before requiring detection, plus a control proving a one-year drift breaks the 120-year total |
| **Q14** | The numbering check moved out of inline YAML into `scripts/check_adr_numbering.py`, so **the gate and its negative control run the same code** rather than the control duplicating the rule. CI plants a duplicate and an out-of-order entry into a copy and requires both to be rejected | 15 committed tests including 4 negative controls, one of which is the exact defect ADR-0029 corrected, an addendum promoted to a level-two heading. CI control simulated locally: duplicate exit 1, out-of-order exit 1, register untouched |
| **Q15** | The recorded swetest invocation is normalised to `<bundled>/swetest` and `-edir<repo-root>`. The command **executed** is unchanged; only the recorded string is normalised, and every argument affecting the computation is recorded verbatim | Two consecutive runs are now identical except `run.executed_utc`. Zero absolute paths remain in the artifact. **Every number identical to the pre-change committed artifact**: summary, tolerance, ayanamsa check, preconditions and all per-case values |
| **H-2**, the gate hole | `SUPERSESSION_FIELD_RE` now validates the value against the ten retired strings, and where a division can be read off the path it must be the identifier ADR-0014 D1's map assigns to that division. The division map is **derived from `RETIRED`** rather than written out, so it cannot drift | 5 probes in an isolated copy: invented family CAUGHT, wrong division CAUGHT, wrong layer CAUGHT, correct division PASSES, unauthorised position CAUGHT. 18 committed tests |
| **H-4**, the CI loophole | `scripts/check_artifact_drift.py` replaces a `git diff` that always exited 0 under a step name asserting a byte-level invariant. Difference is permitted **only** in `date`, `run.executed_utc`, `run.source_revision`, `run.working_tree_dirty` | 13 negative controls, each verified to be detected, plus 4 asserting the volatile fields do **not** trip it, plus a test pinning the volatile list against silent widening |
| **M-1**, false CI claims | The job renamed from "hermetic (no oracle, no network)" and the header now states the real scope: full egress, a five-symbol in-process guard on six of fifteen invocations, child processes not sandboxed, `requirements.lock` version-pinned but not hash-pinned, `pip` upgraded unpinned | Documentation. YAML re-parsed, three jobs, no `continue-on-error` |
| **M-2**, weak network control | The control now runs the probe **unguarded first and requires success**, proving egress exists, then requires the guarded run to fail **with `NoNetworkError` named in the output**. It previously asserted only a nonzero exit, which a missing probe, a renamed guard or a runner with no egress all satisfy | Both halves executed locally: unguarded reached pypi, guarded exited 1 with `NoNetworkError` |
| **M-3**, evidence destroyed | Drift is now checked **before** `git checkout -- certification/ reports/` restores them, and the immutability path list extends to `docs/`, root `*.py`, `CHECKSUMS.sha256`, both lock files, `.github/`, the ephemeris files and the `swetest` binary | The step no longer swallows `git status`'s own exit status |
| **M-8**, stale lock record | `CURRENT_ENGINE_LOCK.json` `certified_tree` now points at the artifact's `run.source_revision` as the single source of truth instead of duplicating a SHA maintained by hand, which had already gone stale one commit after the provenance protocol was adopted. A note records that the block's rounded maxima are superseded in precision by the artifact | No numerical value changed; the trees were already hash-identical |

**Nothing was weakened to obtain a PASS.** Every change above either adds a check, narrows an
exemption, or corrects a claim. Where a check could not be strengthened without an owner decision it
was left and recorded.

### Decision 4. What was NOT done, and the exact blocker for each

| Finding | Blocker |
|---|---|
| **H-1**, the `DP-NNN` family | Registering an identifier family changes `docs/NAMING_STANDARD.md`, a STANDARD, which sits above SPECIFICATIONS in ADR-0022's hierarchy. Extending the gate to flag `DP-` would turn CI red immediately. **Q19** |
| **H-3**, `.github/` undeclared | **Ratified** ADR-0001 fixes the top-level set with the word "exactly". A ratified decision cannot be amended by the builder, and inventing a superseding entry would be manufacturing authority. **Q20** |
| **M-5 and M-6**, the narrowed standards | This is precisely what the directive's item H.4 anticipated: an **unratified** ADR must not silently override a higher-level standard. ADR-0023 is PROPOSED, and `engineering/ENGINEERING_CONSTITUTION.md` is not even placed in ADR-0022's hierarchy, so it is not established that an ADR can narrow it. **Q21** |
| **L-12**, agreement-gate circularity | The gate compares each report against the function that produced it. Closing this needs an independent renderer or a schema-level check, which is new verification design rather than remediation. **Q22** |
| **L-5**, hermetic lock not hash-pinned | Hash-pinning `requirements.lock` changes the dependency contract for two jobs. Documented in the workflow header; the decision is the owner's. **Q23** |
| **L-6, L-7**, unverified oracle assets | The `swetest` binary's recorded SHA-256 is read by nothing, and `CHECKSUMS.sha256` is itself unverified, so a coordinated edit passes both mechanisms. Adding these checks touches the D-001 numerical authority's verification path. **Q24** |
| **C-01, C-02, C-05**, stale standards | Unchanged from ADR-0028. Same blocker as M-5. Additionally, ADR-0003's obligation to re-run the naming conformance sweep **cannot be discharged**: no sweep script exists, and `NAMING_STANDARD.md` NS-2 still proposes creating one |
| **C-04**, `LOCK_MANIFEST.json` | Q12, unchanged. New evidence recorded in ADR-0034 narrowed it |
| **C-06**, ADR-0001/0002 acceptance | Resolved by ADR-0033 D2 |
| **L-4**, `certify_tier0.py` broken | Its disposition was assigned to G7 and G7 has not been authorised |
| **Remote CI evidence staleness** | The only remote-CI record in the repository attests the **two-job** workflow at `a460ba2`. No run record exists for the three-job workflow, and this batch changed the workflow again. **The repository cannot prove CI passes at HEAD**, and this entry does not claim it does. **Q25** |

### Decision 5. Domain and architecture separation re-verified (directive item F)

Re-checked against the tree, not against the entries: **Panchanga and rise/set remain Tier-0-scoped
and ABSENT**, and are **not** inside the ADR-0005 lock, which ADR-0034 restated as the kernel and the
certified D9/D10 mathematics only. **Muhurta, Varshaphal, Prashna and Mundane remain PLANNED, each a
separate domain architecture**, with no implementation and no natal pipeline reuse. The absence sweep
across all fifteen domain terms returns zero hits in `engine/`. **No product feature is authorised
by anything in this batch**, and the four ratified layers gain no new scope from being ratified.

- **Consequences:**
  - Accepted entries become **fourteen**: ADR-0001, ADR-0002, ADR-0005, ADR-0006, ADR-0007,
    ADR-0008, ADR-0009, ADR-0010, ADR-0011, ADR-0012, ADR-0033, ADR-0034, ADR-0035, ADR-0036, plus
    Decision 1 of this entry. Still PROPOSED: ADR-0003, ADR-0004, ADR-0013, ADR-0014, ADR-0018
    through ADR-0032, and Decisions 2 to 5 of this entry.
  - **Every certified production layer is now owner-ratified**: Tier-0, KP chains, Vimshottari,
    transits, the five registry vargas, drishti and the sign conventions. That was the point of the
    batch, and it is the first time the certification stack rests entirely on ratified decisions.
  - Seven new questions, Q19 to Q25, all owner-answerable, prepared as one batch in
    `docs/OPEN_QUESTIONS.md`.
  - Default gate rises from **420 to 496**, seventy-six new tests across four modules, of
    which **thirty-four are negative controls** that each require a deliberate corruption to be
    detected. Nothing existing was removed or relaxed.
  - **The Tier-0 lock is untouched.** No tolerance, profile, holdout case, kernel calculation or
    D9/D10 mathematics changed. Q15 changed a recorded string and no computed value, proven against
    the pre-change artifact field by field.
- **Evidence:** `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md`; the four new test modules;
  `scripts/check_adr_numbering.py`, `scripts/check_artifact_drift.py`, and the corrected
  `scripts/check_retired_identifiers.py`; the probe matrices executed in isolated copies; the
  regenerated Tier-0 evidence compared field by field against its pre-change committed version.

---

## ADR-0038 - The ADR-0037 batch broke the default gate; second-round audit and repair

- **Date:** 2026-08-13
- **Status:** PROPOSED - pending owner ratification (Q1).
- **Context:** A verification audit was run against the tree ADR-0037 produced, by an independent
  agent instructed not to assume the fixes worked. It found a **BLOCKER caused by the remediation
  itself**, plus five weaknesses in the new controls. This entry records the failure plainly and the
  repair.

### Decision 1. The self-inflicted blocker, recorded without softening

`engine/tests/test_retired_identifier_gate_scope.py`, added by ADR-0037 to prove the identifier
gate's exemption had been narrowed, **wrote the ten retired identifiers as literal strings in a
tracked file that was not on the gate's allowlist**. The result:

- `scripts/check_retired_identifiers.py` reported 19 Pattern A and 19 Pattern B violations;
- the `governance` job would have died at its first step;
- the default gate failed, on the module's own self-check that the real tree still passes.

**Three things about this are worth stating rather than burying.**

First, **it passed pre-commit and failed post-commit**, because the gate reads `git ls-files`. While
the file was untracked it was invisible to the gate. The commit that tracked it is what broke it.
Any gate scoped to tracked files has this property, and the batch's own validation did not account
for it.

Second, **`.github/workflows/ci.yml` already records this exact lesson**, in the comment explaining
why its probe string is assembled at run time: "A literal here would be a real violation inside a
tracked file, and the gate would flag this workflow itself. Found the hard way." The lesson was
applied to the YAML and not to the test module written in the same batch.

Third, **ADR-0037 asserted "Nothing was weakened to obtain a PASS" and reported the gate count
rising to 496, without noticing that one of the 496 was failing.** The count was right and the
conclusion was wrong. That is the sharpest illustration available of the finding ADR-0037 D2 itself
recorded: governance prose written to a lower evidential standard than the work it governs.

**Repair.** The module now assembles every identifier at run time from `gate.RETIRED`, the single
source of truth, and carries a self-enforcing test asserting that no retired identifier literal
appears in its own text.

### Decision 2. Five weaknesses in the ADR-0037 controls, all repaired

| Finding | What was wrong | Repair, and how it was verified |
|---|---|---|
| **Unmapped divisions failed open** | `authorised_supersession()` returned the same permissive answer for "no division in the path" and "division present but not in the replacement map". **D9 and D10 are in the second class**, so a D9 or D10 file could have claimed to supersede any retired identifier at all. They are the two flagship certified vargas | Two distinct sentinels, `ANY_RETIRED` and `NOTHING_AUTHORISED`. An unmapped division now authorises nothing. Probed both directions |
| **Look-alike keys inherited the exemption** | The key was matched as a substring, so `xyzsupersedes_provisional_id` was exempt | A left boundary on the key. Three prefix probes committed |
| **Rendered evidence was unenforced** | The drift gate covered `certification/*.json` only, while the CI step diffed `reports/certification/` and the next step uploaded it as certification evidence. Flipping every PASS to FAIL in a report passed | The gate now compares reports and console transcripts line by line, ignoring only the text renderings of the four volatile fields. Verified by corrupting three real evidence files and restoring them |
| **A vacuous PASS** | With nothing modified, the gate compared zero files and printed a PASS that read as "regenerated and identical" | It now compares **every tracked evidence file** regardless of git status, reports the count, and **fails** if it finds none to check. Verified in an empty repository |
| **The numbering control proved neither rule** | Both probes used already-issued numbers, so the out-of-order probe tripped the uniqueness rule too. Deleting **either** assertion left the control passing | The ordering probe now uses **ADR-0016**, which is reserved and unissued, so it is out of order without being a duplicate. Mutation-tested: with uniqueness deleted the ordering probe still fires, and with ordering deleted the duplicate probe still fires |
| **The network control proved one patch of five** | One probe exercising three calls short-circuits on whichever patched symbol it reaches first. With two patches deleted it still raised `NoNetworkError` and still passed | **Five separate probes, each run twice**: unguarded it must succeed, guarded it must fail with `NoNetworkError`. Mutation matrix run: removing `socket.socket.connect`, `connect_ex`, `getaddrinfo` or `gethostbyname` now each fails its own probe |
| **The immutability message over-claimed** | The pathspec omitted `LOCK_MANIFEST.json`, `schemas/`, `knowledge/`, `pyproject.toml`, `pytest.ini` and root documents, while the step printed "no tracked source file was modified" | The step now checks the **whole tree** after restoring `certification/` and `reports/`. Any pathspec, however long, omits something |

**One residual is recorded rather than fixed, because it cannot be fixed.** `create_connection`
cannot be isolated by any probe: it delegates to `getaddrinfo` internally, so removing its patch
alone leaves the call blocked by the `getaddrinfo` patch. It is defence in depth over a path already
covered. Four of the guard's five symbols are individually detected; the fifth is stated in
`.github/workflows/ci.yml` rather than claimed.

### Decision 3. `docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` corrected

It still said "No external oracle, no network" and "defines two jobs", and its status header read
version 1.0.0 while its own change history recorded 1.1.0. All three corrected. **No procedure
changed**; the document now describes the workflow that exists, including the `governance` job and
the two gates added under ADR-0037.

- **Consequences:**
  - Default gate **496 to 521**. The 496 included one failure; the 521 do not.
  - **The lesson generalises and is worth carrying forward: a gate scoped to tracked files cannot be
    validated before the files are tracked.** Any future gate of this shape should be exercised
    against a staged tree, not a working tree.
  - Every ADR-0037 remediation now has a control that has been mutation-tested rather than merely
    executed. That distinction is the whole difference between a gate and a decoration, and ADR-0037
    did not draw it consistently.
  - Findings NOT repaired remain as ADR-0037 D4 recorded them, and Q19 to Q25 are unchanged.
  - **Tier-0 untouched.** No tolerance, profile, holdout case, kernel calculation or D9/D10
    mathematics changed by this entry.
- **Evidence:** The independent verification audit; the mutation matrices for the numbering control,
  the network guard and the retired-identifier scope; corruption and restoration of three real
  rendered evidence files; the empty-repository probe; `git diff --check` clean; 521 passed, zero
  skipped.

---

## ADR-0039 - Owner resolutions of Q17 and Q18: Constitution s12 lock semantics

- **Date:** 2026-08-14
- **Status:** **ACCEPTED**, on the owner's explicit approval of the Q17-Q21 decision batch.
- **Context:** Q17 asks whether Constitution s12 condition 4 requires a ratified decision entry or merely an entry that records the lock. Q18 asks whether lock language inside a ratified decision entry itself creates s12 Locked status.
- **Decision:**
  1. **Q17 — a Constitution s12 Locked artifact requires condition 4 to be satisfied by a decision entry that is itself owner-ratified.** Mere existence of an ADR is insufficient.
  2. **Q18 — lock language inside a ratified decision does not by itself create s12 Locked status.** The four s12 conditions remain conjunctive; formal lock status requires the complete s12 record, including version/evidence and the required owner authorisation.
  3. **Ratification and lock authorisation remain distinct owner acts.** They may be combined only when the owner explicitly authorises both.
- **Consequences:** Q17 and Q18 are resolved for future locks. Tier-0 remains formally Locked under ADR-0034. The sign conventions remain owner-ratified but not s12 Locked under ADR-0036.
- **Evidence:** Owner approval of the Q17-Q21 decision batch on 2026-08-14; ADR-0034 and ADR-0036 re-read against Constitution s12.

---

## ADR-0040 - Owner resolution of Q19: DP-NNN decision-paper identifier family

- **Date:** 2026-08-14
- **Status:** **ACCEPTED**, on the owner's explicit approval of the Q17-Q21 decision batch.
- **Context:** `DP-NNN` is already used by `docs/decisions/DP-008`, `DP-009` and the decision-paper index, but it was absent from the Naming Standard's ID-Families table and had no mechanical family check.
- **Decision:** Register `DP-NNN` as a repository decision-paper identifier family:
  - Pattern: `DP-\d{3}`.
  - Width: 3.
  - Scope: repository-wide decision papers.
  - Issuer: `docs/decisions/README.md`.
  - Source of law: `docs/NAMING_STANDARD.md` section 2 and this ADR.
  - Existing IDs `DP-008` and `DP-009` remain valid; `DP-001` through `DP-007` remain reserved.
  - New decision papers MUST be allocated in the index before drafting.
  - The governance gate MUST scan tracked files for `DP-\d{3}` tokens, reject unregistered tokens, and reject duplicate index allocation.
- **Consequences:** Q19 is resolved. Decision papers remain proposals; decisions still live only in the ADR register.
- **Evidence:** `docs/decisions/README.md`; `docs/NAMING_STANDARD.md`; `scripts/check_identifier_families.py`; committed governance negative controls.

---

## ADR-0041 - Owner resolution of Q20: canonical repository top-level structure

- **Date:** 2026-08-14
- **Status:** **ACCEPTED**, on the owner's explicit approval of the Q17-Q21 decision batch.
- **Context:** Ratified ADR-0001 says the top-level folder set is exact, while the actual repository contains `.github/`, `schemas/`, and later-sanctioned governance/certification folders.
- **Decision:** **Supersede ADR-0001's top-level-folder list** with the actual governed repository structure:
  `.github/`, `assets/`, `certification/`, `docs/`, `engine/`, `engineering/`, `examples/`, `knowledge/`, `legacy/`, `reports/`, `research/`, `schemas/`, `scripts/`, `specs/`, `tools/`.
  `app/` and top-level `tests/` are not part of the current set; tests remain under `engine/tests/`. `.github/` is the repository governance/CI layer and `schemas/` is the normative schema layer.
  Any future top-level folder addition, removal or semantic repurposing requires a superseding ADR.
- **Consequences:** Q20 is resolved. ADR-0003 remains a dated proposed reconciliation record; this entry governs the canonical set where it conflicts with ADR-0003's proposed consequences.
- **Evidence:** Repository tree at `98cc2bd`; ADR-0001; ADR-0002; ADR-0003; current CI and schema paths.

---

## ADR-0042 - Owner resolution of Q21: authority hierarchy and executable normative rule data

- **Date:** 2026-08-14
- **Status:** **ACCEPTED**, on the owner's explicit approval of the Q17-Q21 decision batch.
- **Context:** ADR-0023 is PROPOSED and claims to narrow `engineering/ENGINEERING_CONSTITUTION.md` Principle 3 and `docs/KNOWLEDGE_STANDARDS.md`, while those documents do not delegate that authority. `docs/ARCHITECTURE.md` also independently prohibits duplication.
- **Decision:**
  1. The authority hierarchy is explicitly: **OWNER -> PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> DECISION LOG / ADR -> STANDARDS -> SPECIFICATIONS -> CODE -> CONVERSATION**.
  2. **An ADR does not itself narrow a higher-level constitution or standard.** Any exception MUST first be written into that governing document through its own change-control/ratification process, then may be referenced by an ADR.
  3. The project explicitly permits **executable normative rule data** to be colocated with certified implementation when all four ADR-0023 criteria are met: deterministic necessity, output-changing effect, certification coverage, and school-scoped provenance.
  4. `docs/KNOWLEDGE_STANDARDS.md` is narrowed to governed knowledge; its single-source-of-truth rule does not prohibit separately school-scoped executable normative rule data when the four-part test is met.
  5. `engineering/ENGINEERING_CONSTITUTION.md` Principle 3 is clarified to preserve its general rule while explicitly permitting the same four-part exception.
  6. `docs/ARCHITECTURE.md` is clarified consistently: governed knowledge belongs in `knowledge/`; executable normative rule data may remain with certified implementation when the four-part test is met; interpretation and prediction logic remain outside the knowledge layer.
  7. ADR-0023 remains a dated proposed record. Its exception is authoritative because the governing documents now explicitly state it, not because ADR-0023 silently overrode them.
- **Consequences:** Q21 is resolved. Future standards conflicts cannot be silently resolved by an ADR. The Vimshottari three-way table isolation remains subject to direct identity testing and school-specific certification.
- **Evidence:** ADR-0022; ADR-0023; `engineering/ENGINEERING_CONSTITUTION.md`; `docs/KNOWLEDGE_STANDARDS.md`; `docs/ARCHITECTURE.md`; owner approval of Q17-Q21.

---

## ADR-0043 - Repair a false-positive in the certification artifact drift gate: interpreter identity is volatile

- **Date:** 2026-08-14
- **Status:** PROPOSED. The builder cannot self-ratify (`PROJECT_CONSTITUTION.md` s11); recorded so the fix is not undocumented code.
- **Context:** CI run `31796327555` on branch `phase-g-q17-q21` (PR "Phase G governance Q17-Q21 remediation — CEO review") failed at the `hermetic` job's Python 3.12 leg, in the step "Assert regenerated artifacts did not drift, then that no source changed". `scripts/check_artifact_drift.py` reported genuine-looking drift in `certification/KP_CHAIN_V1_certification.json` (`environment.python`), `certification/SIGN_CONVENTION_V1_certification.json` (`environment.python`), `certification/current_engine_certification.json` (`run.python`) and `reports/certification/current_engine.report.md` (the rendered `- python:` line): each `'3.11.15' -> '3.12.13'`. `docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` s5 runs the three non-oracle certifiers (`certify_current_engine.py`, `certify_kp_chain.py`, `certify_sign_convention.py`) on **both** Python 3.11 and 3.12 by design, and the committed artifacts were last regenerated and archived by whichever leg ran last, so the interpreter-identity field the certifier records as run metadata now legitimately differs from the other leg's interpreter without any calculated value changing. The drift gate's `VOLATILE` list (added by ADR-0037, extended by ADR-0038) did not yet include this field, so it was treated as a substantive drift, correctly by the gate's existing rules but incorrectly given the spec's own dual-interpreter design. An uncommitted, unauthored working-tree edit to `.github/workflows/ci.yml` found at the start of this session had attempted to route around the failure by gating the non-oracle certification runners and the drift-assertion step to the 3.11 leg only. That would have silently dropped 3.12 coverage of three certification runners and the drift gate itself, which `CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` s2 explicitly prohibits ("MUST NOT be used to reduce coverage") and which the project charter's rule against weakening gates to obtain green CI forbids outright. That edit was discarded, not committed, and is not part of this entry.
- **Decision:** `run.python` and `environment.python` are added to `scripts/check_artifact_drift.py`'s `VOLATILE` tuple, and the rendered-report line prefix `- python:` is added to `VOLATILE_LINE_PREFIXES`, following the same reasoning already applied to `date`, `run.executed_utc`, `run.source_revision` and `run.working_tree_dirty`: the interpreter patch version a run executed under is run metadata, not a certified numerical claim, and both interpreter legs are required to produce byte-identical **calculated content** (every comparison count, numerical maximum, tolerance, case identifier and PASS/FAIL verdict remain strictly compared; only the interpreter-version field is exempted). `.github/workflows/ci.yml` is left unchanged: both Python 3.11 and 3.12 continue to run the full non-oracle certification and drift-assertion steps, preserving the coverage the spec requires.
- **Consequences:** The `hermetic` job's 3.12 leg can now regenerate and archive a non-oracle certification artifact without a false-positive drift failure on the interpreter-version field alone. No certified tolerance, holdout case, gate value or PASS/FAIL verdict changed. `engine/tests/test_artifact_drift_gate.py`'s closed-list guard tests (`test_the_volatile_list_is_exactly_what_is_documented`, `test_the_volatile_line_prefixes_are_exactly_what_is_documented`) were updated in the same commit, so a future silent widening of either list is still caught. A companion positive test (`test_environment_python_is_volatile`) and two new parametrized cases prove the widening does what it claims rather than merely existing.
- **Evidence:** CI run `31796327555` (failed, before this fix) and its predecessor `31796101445` (failed on the unrelated DP identifier self-reference bug, repaired separately by commit `190612a`). Locally reproduced on CPython 3.12.10: regenerating `certify_kp_chain.py` and `certify_sign_convention.py` and running `scripts/check_artifact_drift.py` reproduced the identical `environment.python` drift reported by CI; after the fix, `python scripts/check_artifact_drift.py <the four affected files>` returns `PASS: 4 evidence file(s) identical to the committed version outside the volatile fields`; the regenerated artifacts were then restored via `git checkout` and the working tree left clean. `certify_current_engine.py` could not be run locally (the bundled `swetest` reference binary is a Linux ELF binary; this machine is Windows), so the `run.python` / current-engine leg of the fix is verified by code symmetry with the `environment.python` leg and by the CI log's identical failure shape, not by local re-execution; CI on the actual Linux runners is the pending confirmation. Full local default gate: 527 passed (524 baseline plus 3 new tests), zero skipped, zero failed.

---

## ADR-0044 - In-repo AI collaboration scaffolding: CLAUDE.md, .claude/rules/, bounded permissions, hooks, and AI_HANDOFF_CURRENT.md

- **Date:** 2026-08-17
- **Status:** ACCEPTED, on the owner's explicit direction in the session that reviewed `reports/AI_COLLABORATION_INSPECTION.md` and instructed implementation of a specific minimum architecture.
- **Context:** `reports/AI_COLLABORATION_INSPECTION.md` (2026-08-17) found no `CLAUDE.md`, no `.claude/rules/`, no hooks, and no `reports/AI_HANDOFF_CURRENT.md` anywhere in the repository or this machine's Claude Code configuration; `.claude/settings.json` and `.claude/settings.local.json` existed but were entirely untracked, and the latter contained one-off literal permission rules rather than an authored policy. The same inspection found `docs/decisions/DP-010-ai-collaboration-scaffolding.md` (drafted the prior session, unratified, committed alongside this entry) analysing this exact question in options form. The owner reviewed that inspection and directed implementation of a specific architecture, narrower in one respect than DP-010's own recommendation: no skills, agents, or MCP servers, and no repair of the stale/inconsistent documents the inspection found (`docs/PROJECT_CONSTITUTION.md` s11's DRAFT status versus `engineering/ENGINEERING_CONSTITUTION.md`'s ACTIVE status; `specs/CLAUDE_WORKFLOW.md`'s missing status header; `docs/PROJECT_MASTER.md`'s stale, unflagged contradiction of ADR-0041) - the owner's explicit instruction was to record those as open issues rather than silently rewrite existing authoritative documents in the same pass.
- **Decision:**
  1. Add a root `CLAUDE.md` that operationalizes `docs/PROJECT_CONSTITUTION.md` s11 for tooling, citing rather than restating the constitution, `docs/DECISION_LOG.md`, and `docs/OPEN_QUESTIONS.md` as the actual authority, and stating plainly that `docs/PROJECT_CONSTITUTION.md` is itself `Status: DRAFT`.
  2. Add `.claude/rules/governance.md`, `.claude/rules/certification.md`, `.claude/rules/git-safety.md`, `.claude/rules/validation.md`, imported into `CLAUDE.md` via explicit `@` references (Claude Code does not auto-scan an arbitrary `rules/` directory).
  3. Replace the untracked, ad hoc `.claude/settings.local.json` one-off rules with a curated, **tracked** `.claude/settings.json` carrying a bounded allow-list (safe reads, test/gate execution, `git add`/`commit`/`checkout -- `/`restore --staged`) that deliberately excludes `git push` and all destructive git verbs, so those continue to prompt. No `permissions.mode` override is set; `bypassPermissions` is not used. `.claude/settings.local.json` is cleared to an empty allow-list and added to `.gitignore` as the personal/local override layer.
  4. Add two hooks, wired in `.claude/settings.json`: `.claude/hooks/git_safety_guard.py` (`PreToolUse` on `Bash`) blocks force-push, `reset --hard`, `clean -f` (any variant), `branch -D`, direct push/merge to `main`, and `--no-verify`/`--no-gpg-sign`; `.claude/hooks/governance_gate_check.py` (`PostToolUse` on `Edit`/`Write`) re-runs the existing `check_adr_numbering.py` / `check_retired_identifiers.py` / `check_identifier_families.py` / `check_artifact_drift.py` gates immediately after an edit to the files they cover, reusing those scripts rather than reimplementing their logic, and scoped away from the `swetest`-dependent certifiers that cannot run on this Windows host.
  5. Add `reports/AI_HANDOFF_CURRENT.md`, explicitly headed "INDEX ONLY - navigation aid, not evidence", pointing to `docs/DECISION_LOG.md` / `docs/OPEN_QUESTIONS.md` / `README.md` rather than restating their content as fact.
  6. State the Claude auto-memory boundary (convenience only; never authoritative; never citable as evidence) as one line in `CLAUDE.md`, since the memory mechanism already exists (confirmed empty for this project at inspection time) and needed a written boundary, not a new file.
  7. `docs/PROJECT_CONSTITUTION.md`, `engineering/ENGINEERING_CONSTITUTION.md`, `specs/CLAUDE_WORKFLOW.md`, and `docs/PROJECT_MASTER.md` are **not modified** by this entry. Their staleness and inconsistency, recorded in `reports/AI_COLLABORATION_INSPECTION.md` s2.8 and s4, remain open and are cited as such (DRAFT status, missing header, stale content) rather than silently repaired.
  8. This entry closes `docs/decisions/DP-010-ai-collaboration-scaffolding.md`'s question. The decision taken is narrower than DP-010's own recommendation (no skills/agents/MCP); that narrowing is the owner's choice, not a correction of the paper.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file was touched. `main` still carries no GitHub branch-protection rule and the new `PreToolUse` hook is a session-local, Bash-tool-only control - both limitations are stated in `.claude/rules/git-safety.md` rather than implied away. `docs/decisions/DP-010-ai-collaboration-scaffolding.md` remains on disk as the record of the options considered; it is superseded in effect by this entry, not deleted. The three stale/inconsistent documents named above remain exactly as stale as `reports/AI_COLLABORATION_INSPECTION.md` found them, by explicit instruction, and are not to be read as repaired by this entry.
- **Evidence:** `reports/AI_COLLABORATION_INSPECTION.md`; `docs/decisions/DP-010-ai-collaboration-scaffolding.md`; the owner's explicit implementation instruction in the session of 2026-08-17. Verification performed before this entry was written: `python -m pytest -q` - 527 passed, 0 failed, 0 skipped; `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` - all PASS; `git diff --check` - clean; both hooks smoke-tested directly against the documented stdin/exit-code contract - `git_safety_guard.py` correctly blocked six destructive-command cases (force-push, `reset --hard`, `clean -fd`, `branch -D`, push to `main`, `--no-verify`) and correctly allowed six safe ones (push to the current feature branch, `git status`, a normal commit, a non-`Bash` tool call, a command containing a bare `-f`-free filename, a `pytest -k` filter string containing the word "git"); `governance_gate_check.py` correctly passed on the current (valid) `docs/DECISION_LOG.md` and `docs/decisions/README.md`, correctly no-op'd on an unrelated file and on a non-`PostToolUse` event, and, as a negative control, correctly detected (exit 2) a deliberately duplicated ADR heading number, temporarily injected into a working copy of `docs/DECISION_LOG.md`, which was then restored and re-verified clean (`check_adr_numbering.py` PASS, `git diff --stat` empty) before this entry was written. **A real defect was found and fixed during implementation, not merely during isolated smoke-testing:** the first actual commit attempt of this batch was itself blocked by `git_safety_guard.py`, because the commit message's own descriptive prose (naming `--no-verify` and `--no-gpg-sign` as things the hook blocks) was pattern-matched as if those were live flags - the same self-reference defect class this repository has hit before (the retired-identifier gate's literal-string self-reference, `docs/DECISION_LOG.md`, prior sessions). The hook was corrected to strip heredoc bodies and quoted-string contents before scanning for dangerous flags, re-verified against all eleven original smoke-test cases plus three new cases targeting the fixed defect specifically (a heredoc commit message mentioning both blocked flags in prose: allowed; the same flag passed for real outside quotes: still blocked; a quoted message mentioning `--force` in prose: allowed), then the actual commit succeeded. Full detail in `reports/AI_COLLABORATION_IMPLEMENTATION.md`.

---

## ADR-0045 - Post-merge correction of three continuity/control defects in the AI-collaboration architecture

- **Date:** 2026-08-17
- **Status:** ACCEPTED, on the owner's explicit direction in the CEO post-merge audit that identified the three defects below and specified the fix scope narrowly.
- **Context:** `ADR-0044`'s implementation (commit `a866ba0`, report commit `990cd60`) was pushed to `origin/phase-g-q17-q21` and merged into `phase-g-governance` via PR #2 at merge commit `d53787e75048dbadc1a2e3559cf42405c1d56661`; GitHub CI run `32007363289` succeeded on that exact merge commit. A CEO audit of the resulting state, confirmed against the repository before any change was made, found three defects: (1) `reports/AI_COLLABORATION_IMPLEMENTATION.md` still described the implementation as unpushed and on `phase-g-q17-q21`, stale since the push and merge; (2) `reports/AI_HANDOFF_CURRENT.md`'s snapshot named `ADR-0043` as the highest issued decision, stale since `ADR-0044` (ACCEPTED) was added in the same batch that file itself documents; (3) `.claude/settings.json` allows `Bash(git commit*)` broadly and `.claude/hooks/git_safety_guard.py` blocked direct push and direct merge to `main` but had no check for a direct `git commit` while checked out on `main`, even though `.claude/rules/git-safety.md` already stated the rule ("never push to, merge into, or commit directly on `main`") - the mechanical control did not match the documented rule for one of its three verbs.
- **Decision:**
  1. `reports/AI_COLLABORATION_IMPLEMENTATION.md` gets a new "Post-merge update" section recording the push, the PR #2 merge, and the green CI run, and explicitly distinguishes the original implementation commit (`a866ba0`) from the later merge commit (`d53787e`) - one created the files, the other only merged an already-complete branch. The original "Exact HEAD SHA", "Working tree / branch state", and "Next authorized step" sections are **preserved unedited** as the historical record of what was true when the report was written, with a note pointing to the new section rather than the historical text being rewritten.
  2. `reports/AI_HANDOFF_CURRENT.md`'s snapshot section is updated directly (not layered, since the document's own stated purpose is to be refreshed): branch `phase-g-governance`, the PR #2 merge and CI run, and `ADR-0044` as the highest issued and ACCEPTED decision. Its "INDEX ONLY - navigation aid, not evidence" status header and all "trust git over this file" language are unchanged.
  3. `.claude/hooks/git_safety_guard.py` gains one narrow check: a `git commit` (or `--amend`) while `current_branch() == "main"` is blocked with the same unconditional treatment already used for push-to-main and merge-on-main (a hook cannot verify an in-conversation human confirmation, so it blocks outright rather than trying to). `.claude/rules/git-safety.md`'s one-line description of what the hook covers is corrected to say "push/merge/commit" instead of "push/merge". `.claude/settings.json`'s allow-list is **not narrowed** - Claude Code's permission globs are not branch-aware, so the enforcement correctly belongs in the hook, not in a static pattern; narrowing the pattern would not have closed the gap and was not attempted.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file was touched by this entry - confirmed by diffing the changed-file list against those paths before committing. `docs/PROJECT_CONSTITUTION.md` and the other three documents `ADR-0044` left unrepaired remain exactly as they were; this entry does not touch them. `main` remains untouched (this entry's commit lands on `phase-g-governance`, not `main`, and is not a merge). The existing force-push/`reset --hard`/`clean -f`/`branch -D`/`--no-verify` protections in `git_safety_guard.py` are unchanged; only one new check was added, and it does not fire for commits on any branch other than `main`.
- **Evidence:** Verified before any change: `git fetch origin`; `git rev-parse origin/phase-g-governance` matched local HEAD (`d53787e75048dbadc1a2e3559cf42405c1d56661`) exactly; `git merge-base --is-ancestor d53787e... origin/main` returned false (not an ancestor, confirming `main` untouched); `gh run view 32007363289` showed all four jobs green; the three defects were each read directly from the affected files before being described as confirmed, per the instruction to fix "only if the repository confirms them". Post-fix: `python -m pytest -q` - 527 passed, 0 failed, 0 skipped; `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` - all PASS; `git diff --check` - clean. Hook negative control for the new rule, run via direct module import with `current_branch` monkeypatched to `"main"` (chosen over actually checking out `main`, to avoid touching that branch at all during verification): a plain `git commit` and a `git commit --amend` were both correctly blocked, while `git status` and `git diff` were correctly allowed; with `current_branch` monkeypatched back to `"phase-g-governance"`, both commit forms were correctly allowed. The full original eleven-case smoke-test battery from `ADR-0044` was re-run against the current environment and passed unchanged (five blocked, six allowed, including the heredoc/quoted-string regression case). Full detail in `reports/AI_COLLABORATION_IMPLEMENTATION.md`'s post-merge update.

---

## ADR-0046 - Repair a second false-positive in git_safety_guard.py: per-statement scanning

- **Date:** 2026-08-17
- **Status:** ACCEPTED, on the owner's explicit direction that authorized `ADR-0045`'s post-merge correction, of which this is a directly-discovered continuation.
- **Context:** While pushing `ADR-0045`'s correction commit (`83acf44`), the verification command itself - `git status --short`, then two unrelated diagnostic lines including `git rev-parse origin/main` and `git merge-base --is-ancestor ... origin/main`, then `git push origin phase-g-governance` - was blocked by `git_safety_guard.py`'s "direct push targeting `main`" rule, even though the actual push targeted `phase-g-governance`, not `main`. The rule matched `\bgit\b.*\bpush\b` and `\bmain\b` **anywhere in the whole multi-line command string**, so the unrelated `origin/main` diagnostic lines earlier in the same Bash call satisfied the "mentions main" half of the check for the unrelated push later in the same call. This is the same defect class as `ADR-0045`'s evidence paragraph and `ADR-0044`'s heredoc/quote finding: the hook scanning a wider span of text than the thing it is actually supposed to be checking.
- **Decision:** `git_safety_guard.py` now splits the sanitized command into individual shell statements (on `&&`, `||`, `;`, `|`, and newline) and evaluates every rule against **one statement at a time**, never against the whole multi-statement command. A word appearing only in an unrelated statement in the same Bash call can no longer satisfy a check meant for a different statement. This is strictly more precise, not weaker: a genuine violation in any one statement of a chained command is still caught (verified below), and the existing rules and their triggering patterns are otherwise unchanged.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file touched. No existing protection was removed or narrowed. `.claude/rules/git-safety.md` needed no further wording change - it already described the hook's coverage by verb, not by scanning method.
- **Evidence:** The exact failing command was reproduced via direct `blocked_reason()` calls (not through the CI/subprocess path, to keep the reproduction deterministic) and confirmed to false-block before the fix and pass cleanly after it. Nineteen cases verified post-fix: the regression repro; a genuine push-to-`main` mixed into an otherwise unrelated multi-statement chain (still correctly blocked); a genuine force-push on one line among unrelated lines (still correctly blocked); the full eleven-case battery from `ADR-0044`/`ADR-0045` (five blocked, six allowed, unchanged); and the five/two-case commit-on-`main` monkeypatched negative control from `ADR-0045` (still blocked on simulated `main`, still allowed on the real current branch). `python -m py_compile` - compiles. Full verification suite re-run clean: `python -m pytest -q` - 527 passed; `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` - all PASS; `git diff --check` - clean.

---

## ADR-0047 - G5 Historical Validation Corpus — Supplement Only

- **Date:** 2026-08-17
- **Status:** PROPOSED. Not owner-ratified. This entry records a research decision reported to the builder for persistence into repository governance records; it is not self-ratifying and does not become binding by being written down. Per `docs/PROJECT_CONSTITUTION.md` s11, owner ratification is a separate, required act.
- **Context:** ACE's historical-validation programme (`docs/VALIDATION_STANDARD.md`, `docs/H2_HISTORICAL_EVENT_LEDGER_SPEC.md`) requires a protected corpus of independently-verifiable, exact-day historical events to serve as a primary validation benchmark. The publicly accessible **G5 dataset** was investigated as a candidate. Investigation was necessary because public accessibility alone does not establish independence from any other reference database (here, **ADB**, a comparison/reference database checked for overlap) - a record's presence on a different website is not evidence of independent lineage, and G5/ADB agreement is not independent confirmation of either. This required a person-by-person and event-by-event lineage assessment rather than a bulk assumption in either direction. **Naming note:** "G5" here is unrelated to "G5, certification taxonomy" in `docs/Q8_CLOSURE_MATRIX.md`'s Phase G work breakdown; the collision is coincidental and both usages stand as they are. Full detail: `research/G5_DATASET_VALIDATION_CLOSEOUT.md`.
- **Evidence:** A fixed, pre-registered 22-person sample was evaluated (pre-registration before evaluation is what makes the completion count meaningful). Result, **as reported to the builder and not independently reproduced from primary records** (no per-person worksheet is currently committed to this repository - see `research/G5_DATASET_VALIDATION_CLOSEOUT.md` s8 for the evidence-class statement in full): 22/22 sample completed; 16 people classified independent of ADB; 4 matched ADB; 2 identities remained unresolved (lineage UNKNOWN, counted as neither independent nor matched); 14 genuinely independent exact-day events identified across the 16 independent people; event-domain coverage limited to academic appointment/honor, military/combat events, political detention, family events, and career/administrative/publication events. This evidence class matches the precedent already established in `docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md` s7.1's `CEO_REPORTED` class: reported by the requester, not independently observed by the builder, and recorded as such rather than silently presented as builder-verified.
- **Decision:**
  1. **G5 is SUPPLEMENT ONLY.** Fourteen independent exact-day events across five domain categories, from a 22-person sample, does not establish sufficient independent, multi-domain, exact-day event density for G5 to serve as ACE's **primary** historical-validation benchmark.
  2. **Permitted role.** G5 may be used for: (a) entity-resolution / reference population; (b) birth-time-quality / reference support; (c) supplementary independent historical events; (d) selected career/military/academic/family exact-day evidence where provenance qualifies per the lineage rule in decision 4.
  3. **Prohibited role.** G5 must NOT be treated as: (a) ACE's primary historical-validation corpus; (b) a general protected validation benchmark; (c) a protected holdout by default; (d) evidence of predictive accuracy; (e) automatically independent of ADB; (f) independent merely because a record appears on a different website; (g) a basis for extrapolating the 22-person sample's findings to the full G5 population.
  4. **Lineage requirement.** Every G5 person/event used as independent evidence anywhere in ACE requires explicit lineage and ADB-overlap assessment at the point of use, following `docs/H4_EVIDENCE_MODEL_SPEC.md` s10's existing rule for evidence relationships: an unmeasured or unknown relationship must never default to independent. **UNKNOWN lineage remains UNKNOWN** and is never counted as INDEPENDENT. G5/ADB agreement must never be treated as independent confirmation.
  5. This entry does not authorise, and is not to be read as authorising, any implementation work (calculation engine, certification, or product-domain code) on the strength of it. It is a corpus-suitability and evidentiary-role decision only.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file is touched by this entry. No protected validation data or holdout is created, modified, or designated by this entry. `research/G5_DATASET_VALIDATION_CLOSEOUT.md` is the supporting research record; this entry is the normative decision text if the two ever disagree, per this register's usual precedence. This entry remains PROPOSED until an owner ratifies it; until then, G5's role in ACE is undecided in the binding sense, and decision 1-4 above states the builder's recorded position, not a ratified constraint.
- **Limitations:** The 22-person sample must not be extrapolated to the full G5 population (`research/G5_DATASET_VALIDATION_CLOSEOUT.md` s7). The underlying per-person worksheet is not currently in this repository; reproducibility of the counts in "Evidence" above is therefore not yet independently verifiable from repository contents alone.

### Evidence addendum to ADR-0047 - corrected G5 sample accounting (2026-08-18)

- **Status:** CORRECTIVE EVIDENCE. This addendum does NOT edit `ADR-0047`'s Context/Evidence/Decision/Consequences/Limitations text above; that text stands unmodified as the dated record of what was originally reported on 2026-08-17. `ADR-0047` **remains PROPOSED** - this addendum does not ratify it, does not mark it ACCEPTED, and does not convert it into a certification decision. It corrects the evidentiary basis only.
- **Context:** The completion accounting reported to the builder and recorded in `ADR-0047`'s own Evidence paragraph - "22/22 sample completed; 16 people classified independent of ADB; 4 matched ADB; 2 identities remained unresolved; 14 genuinely independent exact-day events" - was subsequently identified as an incorrect completion count. **It must not be relied upon as verified evidence and is superseded by the corrected accounting below.** `research/G5_DATASET_VALIDATION_CLOSEOUT.md` is corrected in the same governance pass as this addendum, per its own "Change history."
- **Corrected executed state, as reported (still not independently reproduced by the builder from primary records - no per-person worksheet is present in this repository, per `ADR-0047`'s own Limitations and s8 of the research record):**
  - **Attempted: 12 / 22.** Fifteen of the twenty-two pre-registered people were never attempted; the sample is NOT 22/22 complete and must never again be described as such.
  - **Confirmed independent of ADB (4):** Impanis, Del Prete, Painleve, Esclangon.
  - **ADB_MATCH, not independent (2):** Maldini, Bobet.
  - **NO_MATCH (1):** Mounicq.
  - **AMBIGUOUS (1):** Charpentier.
  - **Identity-resolved but never ADB-checked (4):** Scaroni, Bacchelli, Prinzhorn, Ellinger. **These four are NOT counted as independent** - an unchecked lineage is UNKNOWN, not independent, per `ADR-0047` Decision 4's own rule, which this addendum applies to itself rather than exempting itself from.
  - **Unattempted (15).**
  - The prior "16 independent people" and "14 genuinely independent exact-day events" figures do not survive this correction: 16 was double the corrected confirmed-independent count of 4, and the 14-event figure was derived from those same 16 people. **No corrected event-level count is supplied by this addendum** - none was given to the builder as part of this correction, and none is invented here. Section 5 ("Event-domain coverage observed") of the research record is therefore also superseded, not merely section 4; both are marked as such in the corrected document.
- **What this addendum does not do:** it does not supply a corrected event list; it does not re-examine or resolve `Mounicq`, `Charpentier`, or the four unchecked identities; it does not independently reproduce any of the corrected counts from primary records (the same evidence-class limitation `ADR-0047` itself already stated applies unchanged); it does not assert a population-level G5 independence rate; it does not assert or imply any predictive-accuracy claim.
- **Effect on `ADR-0047`'s Decision 1 (G5 = SUPPLEMENT ONLY):** the substantive conclusion is unaffected and, if anything, further supported - a corrected, smaller confirmed-independent count (4 of 22 attempted, not 16) is weaker evidence for primary-benchmark suitability than the original incorrect figure, not stronger. `ADR-0047` Decision 1-4's text is not edited by this addendum; a reader relying on `ADR-0047`'s own Evidence paragraph for the underlying counts must use this addendum's corrected figures instead.
- **Evidence:** Owner correction instruction, 2026-08-18: "ACE GOVERNANCE CORRECTION - G5 / ADR-0047 ONLY," naming the corrected counts and the four named categories with the specific people listed above. `research/G5_DATASET_VALIDATION_CLOSEOUT.md` (corrected in the same pass, version 2.0.0). No calculation-engine, certification-artifact, locked Tier-0, protected validation data, or unrelated-ADR file is touched by this addendum.

### Evidence addendum to ADR-0047 - restoration of authoritative G5 sample accounting; retraction of the 2026-08-18 "12/22" addendum above (2026-08-18)

- **Status:** CORRECTIVE EVIDENCE. This addendum does NOT edit or delete the "corrected G5 sample accounting" addendum immediately above; that addendum's text stands unmodified as the dated record of what was reported and briefly relied upon. **That addendum is itself now SUPERSEDED / RETRACTED** for the reason given below. This addendum does not ratify `ADR-0047`; it **remains PROPOSED**.
- **Context:** Owner-directed forensic reconciliation, performed read-only against primary source files supplied outside this repository (`FINAL_CLOSEOUT_22_SAMPLE.md`, `BRIDGING_MISSION_FINAL_REPORT_v2.md`, `NEXT_CORPUS_REPORT.md`, and the `G5_CENSUS_REPORT.md` checkpoint series), established that the "12/22 attempted" figure recorded in the addendum immediately above was **itself incorrect**. Its source, `NEXT_CORPUS_REPORT.md`, conflated the pre-registered 22-person G5 sample with an unrelated, separately-run **five-person bridging pilot** (Maldini, Impanis, Mounicq, Del Prete, Charpentier) - two of that pilot's names (Impanis, Del Prete) were counted into the "12 attempted" figure, and it further mischaracterized four of the 22-sample's people (Scaroni, Bacchelli, Prinzhorn, Ellinger) as "never ADB-checked" when the primary 22-person closeout record shows all four as ADB-checked with a NONMATCH result. `NEXT_CORPUS_REPORT.md`'s timestamp postdates both the 22-person closeout and the bridging-pilot report it draws from, and its account contradicts both rather than correcting either.
- **Restored authoritative state, G5 original 22-person sample (supersedes the "12/22" figures above):**
  - **Attempted: 22 / 22.** The sample is complete as originally reported on 2026-08-17, not 12/22 as the intervening (now-retracted) addendum stated.
  - **Independent of ADB (16).**
  - **ADB_MATCH, not independent (4):** Fichera, Aimar, Serantoni, Bobet.
  - **Unresolved identity (2):** Veen, Perquier.
  - **Independent, exact-day events (14)**, across the 16 independent people.
- **Separate five-person bridging pilot (explicitly excluded from the counts above, per the primary record's own statement that it is "not merged into any count"):** Maldini, Impanis, Mounicq, Del Prete, Charpentier. This pilot is a distinct piece of research with its own separate result and was never part of the pre-registered 22-person G5 sample.
- **Disposition of the retracted "12/22" addendum:** preserved unedited above, marked SUPERSEDED/RETRACTED by this entry, not deleted, per this register's append-only convention - the audit trail shows (a) the original 22/22 report (2026-08-17), (b) the erroneous 12/22 correction (2026-08-18, first addendum), and (c) this restoration (2026-08-18, this addendum), in that order.
- **Effect on `ADR-0047`'s Decision 1 (G5 = SUPPLEMENT ONLY):** unchanged. Fourteen independent, exact-day events from a 22-person sample was, and remains, the evidentiary basis already found insufficient for a primary historical-validation benchmark in `ADR-0047`'s own Decision 1; restoring the correct count does not newly authorize any different role for G5 than decisions 1-4 already state.
- **Evidence class, unchanged:** as with both prior accountings, these counts are **reported, not independently reproduced by the builder from primary records within this repository** - `FINAL_CLOSEOUT_22_SAMPLE.md` and the other files reconciled above are external files supplied for this reconciliation, not committed to this repository. This addendum records the reconciliation result; it does not import those files into the repository.
- **Evidence:** Owner instruction, 2026-08-18: "READ-ONLY G5 EVIDENCE RECONCILIATION - NO RESEARCH," followed by "ACE GOVERNANCE REPAIR - RESTORE AUTHORITATIVE G5 22-PERSON RECORD." No calculation-engine, certification-artifact, locked Tier-0, protected validation data, or unrelated-ADR file is touched by this addendum.

---

## ADR-0048 - Owner ratification of the Q8 Closure Matrix: Q8 CLOSED

- **Date:** 2026-08-17
- **Status:** **ACCEPTED.** It is accepted because the owner supplied explicit ratification of `docs/Q8_CLOSURE_MATRIX.md` as a ratification instruction, following the same evidentiary pattern already used in `ADR-0033` (Q1, Q13, Q8 direction), `ADR-0034` (Tier-0 lock), `ADR-0035` (registry vargas) and `ADR-0036` (drishti/sign-convention): the ratification reached the repository through a working session, and this entry is what makes it authoritative, per `docs/PROJECT_CONSTITUTION.md` s7 and s11.
- **Context:** `ADR-0033` Decision 3 ratified Q8's **dependency ordering** on 2026-08-13, explicitly leaving the harder half open: "no phase has ratified prerequisites, entry criteria, scope, certification gates, exit criteria or approval requirements." `docs/Q8_CLOSURE_MATRIX.md` (drafted 2026-08-11, `Status: PROPOSED`) is the candidate matrix meeting that closure test, covering Phase G, FOUNDATION, JATAKA, EVIDENCE, INTERPRETATION, CONVERGENCE, VARSHAPHAL, MUHURTA, PRASHNA, BTR (treated orthogonally), and the cross-phase invariants. The owner has now reviewed and approved it.
- **Independent audit performed before ratification, per instruction.** The matrix's structure was checked against current repository state rather than ratified sight-unseen:
  - `ADR-0017` (the charter's C0-C5 certification taxonomy, which the matrix's "Conventions used" section cites as "still pending") remains unissued - confirmed via `scripts/check_adr_numbering.py`, which reports `ADR-0015` through `ADR-0017` as a legal reservation gap. The matrix's citation is accurate, not stale.
  - `DP-008` and `DP-009` (cited as prerequisites for JATAKA/EVIDENCE and FOUNDATION respectively) remain `OPEN, drafted` in `docs/decisions/README.md`. Accurate, not stale.
  - **One substantive gap was found, and it is reported rather than silently repaired or silently ignored:** Phase G's own stated exit criterion includes "the three BLOCKER findings B-01, B-02, B-03 either resolved or explicitly deferred by decision." Direct inspection of `engine/astrology/varga_registry.py`'s `register_varga_rule` (2026-08-17) shows no check that a registered rule's division count matches the division it is registered under - this is exactly finding B-01 as stated in `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` s"B-01". No entry in `docs/DECISION_LOG.md` explicitly defers B-01 (searched; no match), and `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md`, the later and more thorough audit, does not mention it at all. **B-02 and B-03 were not independently re-verified in this pass** and are flagged for the same treatment, not assumed resolved. This is not a defect in the matrix's wording - the matrix correctly states the criterion - it is a finding that the criterion's current satisfaction is unconfirmed. It does not block this ratification (see Decision 6) but is recorded so it is not later mistaken for a cleared gate.
  - No other substantive contradiction between the matrix and current ADRs/`docs/OPEN_QUESTIONS.md` was found. The matrix's ten phase entries, BTR's orthogonal treatment, and the cross-phase invariants are internally consistent with `ADR-0019`, `ADR-0020`, `ADR-0021`, `ADR-0026` and `ADR-0033` as currently recorded.
- **Decision:**
  1. **The owner ratifies `docs/Q8_CLOSURE_MATRIX.md` as written.** No word of its phase definitions (sections 3 through 14) is altered by this entry. Its status header and self-referential "Q8 remains OPEN" statements (section 1, section 15) are updated in the same commit to reflect ratification, which is a synchronization of the document's own status claim, not a substantive change - the same treatment `ADR-0033` Decision 2 applied to `ADR-0001`/`ADR-0002`.
  2. **Q8 is CLOSED.** `docs/OPEN_QUESTIONS.md` Q8 moves from "OWNER-RATIFIED DIRECTION, FULL RESOLUTION STILL OPEN" to **RESOLVED**, and a resolution-log row is added citing this entry.
  3. **The phase ordering and per-phase matrix are now the authorized roadmap governance**, per `docs/Q8_CLOSURE_MATRIX.md` sections 3-14 and `docs/PROJECT_ROADMAP.md` section 3's dependency ordering (already ratified, `ADR-0033` D3).
  4. **Phase entry does NOT automatically authorise every future capability within that phase.** Each phase's matrix entry itself says so (for example FOUNDATION: "CEO approval: entry, per-capability checkpoint, exit... each is a new Tier-0 or Tier-1 claim"; JATAKA: "Each is a separate ADR and none is implied by phase entry"). This entry does not weaken that; it ratifies it.
  5. **Binding, unweakened by this entry:** every phase's stated prerequisites and entry criteria; every phase's stated certification gates (per-capability template requirements, external-reference/oracle requirements, negative controls); every phase's stated CEO approval checkpoints (entry, intra-phase, exit, as each phase specifies); the cross-phase invariants in section 14 verbatim, including "no phase may weaken a certification gate to pass" and "protected holdouts are never used for selection or tuning"; `docs/VALIDATION_STANDARD.md`'s protected-holdout rules generally, unaffected by this entry.
  6. **No implementation authorisation is inferred beyond the matrix, and specifically none is created by this entry.** Ratifying Q8 ratifies the *governance framework*, not a certification that any phase's entry criteria are currently met. In particular, the audit finding above (B-01 unresolved, B-02/B-03 unverified) means **Phase G's own exit criteria are NOT confirmed met by this entry**, and consequently FOUNDATION's prerequisite ("Phase G exit") is likewise not confirmed satisfied. This entry does not declare Phase G exited and does not authorise FOUNDATION entry. Whether B-01/B-02/B-03 are to be resolved, explicitly deferred, or otherwise dispositioned is a separate decision, not made here.
- **Consequences:** `docs/Q8_CLOSURE_MATRIX.md` status header changes from PROPOSED to ACCEPTED/RATIFIED. `docs/OPEN_QUESTIONS.md` Q8 changes from open-in-part to RESOLVED. `docs/PROJECT_ROADMAP.md` is synchronized (status header, section 3's "Q8 is not closed by this ratification" language, section 4's Q8 prerequisite-gate row) to reflect closure, with no change to section 3's already-ratified ordering or to any completed-work row. No calculation-engine, certification-artifact, locked Tier-0, or product-domain file is touched. No certification gate is weakened. No protected holdout is created, read, or exposed. No product-domain implementation (FOUNDATION, Panchanga, sunrise/sunset, Muhurta, Varshaphal, Prashna, Mundane, BTR, Interpretation, Convergence, UI, ML) is begun, authorised, or inferred as authorised by this entry.
- **Evidence:** `docs/Q8_CLOSURE_MATRIX.md` (the ratified document); `ADR-0033` D3 (the prior direction-only ratification this entry completes); `ADR-0021` D2 (the closure-criteria requirement this entry satisfies); `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` (source of the B-01 finding independently re-confirmed here); `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md` (checked and found silent on B-01); `engine/astrology/varga_registry.py` (direct code inspection, 2026-08-17); `scripts/check_adr_numbering.py` output (ADR-0017 reservation-gap confirmation); `docs/decisions/README.md` (DP-008/DP-009 status confirmation). Post-change verification: `python -m pytest -q`, `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py`, `git diff --check` - exact results cited in this commit's message, consistent with `ADR-0043`'s pattern of citing exact command output rather than a summary.

---

## ADR-0049 - B-01, B-02 and B-03 remediated: varga registry division invariant, rule identity/content pinning, live sign-convention recomputation

- **Date:** 2026-08-17
- **Status:** ACCEPTED, on the owner's explicit authorization ("APPROVE B-01 B-02 B-03 REMEDIATION") of the specific remediation forensically audited and classified Class C in the immediately preceding session, and reported before any change was made.
- **Context:** `ADR-0048` ratified `docs/Q8_CLOSURE_MATRIX.md`, whose Phase G exit criterion requires "the three BLOCKER findings B-01, B-02, B-03 either resolved or explicitly deferred by decision." A forensic audit (prior session, same day) independently re-confirmed all three unresolved in current code and git history, with `docs/PROJECT_ROADMAP.md` section 2 recording them, by name, as "discussed and not approved" - classified Class C, remediation requiring owner decision. The owner then explicitly authorized remediation of exactly these three findings, no more.
- **B-01: the varga registry never checked that a rule matches the division it is registered under.**
  - **Original finding** (`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` "B-01"): `register_varga_rule` validated rule type, the D1/D9/D10 refusal, a non-empty school string, and duplicate keys - never `division` against the rule's own content. Registering `D12_PARASHARA` under division 4, 13, 0 or -5 was accepted.
  - **A material correction to the audit's own proposed fix, made during implementation and recorded here rather than silently applied:** the audit proposed, for `SegmentVargaRule`, that every source sign have the same segment count *and that count equal the registered division*. Direct inspection of the certified `D30_PARASHARA` (`engine/astrology/varga_d30.py`) shows this is **factually wrong for the already-certified D30 registration**: Trimsamsa's practical, certified rule has five unequal segments per sign (one per ruling planet: Mars/Saturn/Jupiter/Mercury/Venus), registered under division 30. Implementing the audit's literal text would have rejected the legitimate, already-ratified (`ADR-0011`, `ADR-0035`) D30 registration. The corrected design gives `SegmentVargaRule` its own self-declared `division: int` field (mirroring `CyclicVargaRule.divisions`, which is not tied to segment count) rather than inferring division identity from segment count, and separately enforces segment-count *uniformity across the 12 signs* (a genuine, independent structural invariant D30 also satisfies: 5 segments on every sign) without requiring that count to equal the division number. This is stricter and more correct than the audit's text, not weaker: it protects `CyclicVargaRule` and `SegmentVargaRule` symmetrically and does not special-case D30.
  - **Implementation:** `engine/astrology/varga_rules.py` - `SegmentVargaRule` gains `division: int` (validated: integer, >= 2) and a per-sign segment-count-uniformity check in `__post_init__`. `engine/astrology/varga_registry.py` - `register_varga_rule` now validates `division` is a non-bool int >= 2 other than 1/9/10, and cross-checks `rule.divisions == division` (Cyclic) or `rule.division == division` (Segment) before storing. **No upper bound on `division` is enforced**: no document in this repository specifies an authoritative maximum (the highest classical varga named anywhere here is D60), and inventing one would itself be an unauthorised limit.
  - **Production rules updated:** `varga_d2.py`, `varga_d3.py`, `varga_d30.py` gain `division=2`, `division=3`, `division=30` respectively (their already-correct values; `varga_d7.py` and `varga_d12.py` needed no change, being `CyclicVargaRule` with `divisions` already matching). Four existing test call sites in `engine/tests/test_varga_framework.py` that registered a 5-division synthetic rule under key `9999` (never checked before) now use key `5`, matching the rule's actual content, or a purpose-built synthetic 9999-division rule where the dispatcher-routing test needed the original arbitrary key preserved without affecting any other test's arithmetic.
- **B-02: a certified rule could be swapped at runtime while every non-invasiveness gate stayed green.**
  - **Original finding:** `unregister_varga_rule` is unguarded and `_REGISTRY` is plain mutable state; every existing gate compared registry keys, never rule identity or content.
  - **Implementation:** `engine/astrology/varga_rules.py` gains `rule_content_sha256(rule)`, a deterministic SHA-256 fingerprint of a rule's own table data (divisions/start_sign/direction for Cyclic; division/segments for Segment) - content, not object identity. Each varga's Gate-4 test section (`test_varga_d3.py`, `test_varga_d12.py`, `test_varga_batch_d7_d30_d2.py`) gains an identity assertion (`get_varga_rule(N, school) is DN_PARASHARA`) and a content-hash pinning assertion against a hardcoded expected digest. Each certifier's `gate_d_non_invasiveness()` (`scripts/certify_d2.py`, `certify_d3.py`, `certify_d7.py`, `certify_d12.py`, `certify_d30.py`) gains the same identity check (failing the certification run if it does not hold) and records `rule_content_sha256` in its Gate D output, alongside the existing D9/D10 sweep hashes.
  - **Emergent relationship to B-01, recorded rather than left implicit:** the audit's own B-02 reproduction (unregister D3, re-register D30's rule under key 3) is now *also* caught by B-01's division cross-check, since `D30_PARASHARA.division` (30) does not equal 3. B-01 and B-02 are complementary, not redundant: verified directly, a *same-division* content tamper (one cell of `D3_PARASHARA` changed, `division` left at 3) passes B-01's check and is caught only by B-02's identity/content checks - the negative controls below prove this specific case.
- **B-03: the sign-convention certification gate read a stored artifact instead of recomputing, contrary to `docs/VALIDATION_STANDARD.md` s2 rule 8.**
  - **Original finding:** `engine/tests/test_sign_convention_certification.py`'s `test_non_invasiveness_hashes_match_published_main` compared `certification/SIGN_CONVENTION_V1_certification.json`'s recorded hashes against hardcoded constants - proving the artifact matches itself, never that the certified functions still produce those values.
  - **Implementation:** the test now imports `scripts/certify_sign_convention.py` as a module and calls its own `gate_a_non_invasiveness()` directly - the exact code that produces the artifact in the first place - comparing the **freshly recomputed** sweep hashes against the same pinned constants. The stored artifact is not read by this test at all. Measured cost: 0.67 seconds for 54,697 points across D9, D10 and all five registry vargas, confirmed affordable in the default gate. A companion negative control (`test_negative_control_a_mutated_certified_function_is_detected`) monkeypatches `navamsa_sign` inside the certifier module, confirms the recomputed D9 hash changes, then explicitly undoes the patch (`monkeypatch.undo()`, not merely relying on teardown) and re-confirms the hash is restored - proving the gate can both fail and recover cleanly.
- **Negative controls, all genuine (planted violation, confirmed rejection/detection, state fully restored, confirmed restored):** B-01 - the audit's exact repro (D12 rule under divisions 4/13/0/-5) rejected with the specific new error; a same-division-mismatched `CyclicVargaRule` and `SegmentVargaRule` each rejected; non-integer/boolean/out-of-range `division` rejected; all five current certified registrations proven to remain valid (re-registering under their own key correctly fails for the *duplicate* reason, not a division-mismatch reason, proving the new check does not misfire on legitimate content). B-02 - a single-cell-tampered copy of `D3_PARASHARA` and `D12_PARASHARA`, and of each of D7/D30/D2, registered under its own correct (unchanged) division: identity check fails, content hash differs, state restored and re-verified after. B-03 - `navamsa_sign` mutated inside the certifier module: recomputed hash changes; unmutated: hash matches again.
- **Consequences:** No certified numeric or categorical output changed for any of the five production vargas or the sign-convention layer - proven by the full existing dense-sweep, ULP-boundary and cross-layer test suites passing unchanged (558 total, up from 527 baseline), and by `gate_d_non_invasiveness()` and `gate_a_non_invasiveness()` independently reproducing the exact same content hashes and sweep hashes as before this change. `certification/VARGA_D2_V1_certification.json`, `..._D3_V1...`, `..._D7_V1...`, `..._D12_V1...`, `..._D30_V1...` are **not regenerated by this entry**: the five varga certifiers require the PyJHora external oracle (`scripts/certify_d*.py` Gate C), unavailable on this Windows development host - a genuine environment limitation, not a defect, matching the same class of limitation already documented for `certify_current_engine.py` (`ADR-0043`). `certification/SIGN_CONVENTION_V1_certification.json` was regenerated locally as a real, successful run (no PyJHora dependency) and found byte-identical outside the already-volatile `date`/`environment.python` fields; that no-op regeneration was discarded (`git checkout --`) rather than committed, per this repository's standing practice of not committing an audit-run regeneration that changes nothing certified. Full end-to-end re-certification of the five varga artifacts, including the genuine PyJHora oracle comparison, is deferred to the next CI run on the Linux oracle-tier runner (`docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md`), where it will be independently confirmed or, if it fails, investigated before being treated as resolved.
- **Phase G exit status: NOT a candidate for exit, notwithstanding this remediation.** B-01/B-02/B-03 are now resolved, but `docs/Q8_CLOSURE_MATRIX.md` section 3's Phase G exit criteria list several further items, at least two of which remain independently unmet and were verified, not assumed: **G5 "certification taxonomy"** (the charter's C0-C5 levels) requires `ADR-0017`, confirmed still unissued (`scripts/check_adr_numbering.py` reports it inside the reserved-and-unissued 0015-0017 gap); **G7 "stale documentation"** was explicitly left unrepaired by owner instruction in `ADR-0044` D7 (`docs/PROJECT_CONSTITUTION.md`/`engineering/ENGINEERING_CONSTITUTION.md` status inconsistency, `specs/CLAUDE_WORKFLOW.md`'s missing status header, `docs/PROJECT_MASTER.md`'s uncorrected staleness). G2/G3/G4 status was not exhaustively re-verified in this pass and is not claimed either way. This entry does not authorise, and must not be read as authorising, FOUNDATION or any product-domain work.
- **Evidence:** `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` (original findings); the forensic audit of the immediately preceding session (B-01/B-02/B-03 classification, Class C, and the exact original-repro evidence cited there, independently re-confirmed against current code in this entry); direct code inspection of `engine/astrology/varga_registry.py`, `varga_rules.py`, `varga_d2.py`, `varga_d3.py`, `varga_d30.py`, and the five `scripts/certify_d*.py`; `python -m pytest -q` - 558 passed, 0 failed, 0 skipped (up from 527 at baseline); `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` - all PASS; `git diff --check` - clean; `gate_d_non_invasiveness()` invoked directly (via an in-process import stub for the PyJHora module-level guard only - Gate C itself was never invoked, trusted, or claimed to have passed) for all five certifiers, each returning the same content hash independently computed from the production rule object directly; the exact original B-01 and B-02 repro scenarios re-run against current code and confirmed rejected/detected, cited above.

---

## ADR-0050 - G7 stale documentation repaired; G5 certification taxonomy found not ready to ratify

- **Date:** 2026-08-17
- **Status:** ACCEPTED, on the owner's explicit authorization ("APPROVE G5 RATIFICATION AND G7 REPAIR") of exactly the two named Phase G exit items, `docs/Q8_CLOSURE_MATRIX.md` s3.
- **Context:** `ADR-0049` left G5 and G7 as the two independently-verified-unmet Phase G exit items alongside B-01/B-02/B-03 (since resolved). The owner authorized remediation of exactly these two, no more, with G5 conditioned on `ADR-0017` actually being ready to ratify and G7 bounded to documentation repair, not new decisions.
- **G5: `ADR-0017` (the charter's C0-C5 certification taxonomy) is not ready to ratify - no such taxonomy exists anywhere in the repository to inspect, verify, or ratify.**
  - **Verification performed:** `scripts/check_adr_numbering.py` confirms `ADR-0015` through `ADR-0017` remain a reserved, unissued gap. Searched `specs/PROJECT_CHARTER.md` (the document the taxonomy is repeatedly cited as belonging to, e.g. `docs/decisions/DP-009-panchanga-riseset-tier.md` line 75, `docs/Q8_CLOSURE_MATRIX.md` s2) for any C0-C5 tier definition: none exists: the charter's only certification-adjacent sentence is the single disclaimer that "engineering certification... refers to reproducibility and correctness... not proof of predictive validity." Searched `docs/decisions/` for a drafted paper defining the taxonomy: none exists (`docs/decisions/README.md`'s index has no such entry; DP-001 through DP-007 are reserved for an unrelated governance round). No draft ADR-0017 file, section, or note was found anywhere in the tracked tree.
  - **Decision:** G5 is **not resolved this session.** Drafting a C0-C5 certification taxonomy from nothing is authoring new certification policy, not ratifying an existing, reviewable proposal - exactly the "genuine owner decision... cannot be inferred from an existing ratified decision" boundary this session's own authorization instructs stopping at, and the G5 instruction itself was explicitly conditional ("If `ADR-0017` is ready, formally ratify it"). No taxonomy was invented, no certification requirement was weakened or bypassed to manufacture a ratifiable document, and no certified calculation behaviour was touched.
  - **What G5 requires before it can be attempted again:** a drafted taxonomy (as a `DP-NNN` paper per `docs/decisions/README.md`'s own registration-before-drafting rule, or a direct owner-authored proposal) mapping the charter's intended C0-C5 levels against the existing certification vocabulary (`docs/VALIDATION_STANDARD.md`, the varga six-gate template, Tier-0 lock criteria) - none of which currently exists to review.
- **G7: the three named stale-documentation findings from `ADR-0044` D7 / `reports/AI_COLLABORATION_INSPECTION.md` s2.8 are repaired.**
  - **Finding 1 - `docs/PROJECT_CONSTITUTION.md` s11 `DRAFT` status read as less authoritative than the subordinate `engineering/ENGINEERING_CONSTITUTION.md`'s `ACTIVE` status.** Repaired by adding a cross-reference note to `docs/PROJECT_CONSTITUTION.md` s11 and a matching note to `engineering/ENGINEERING_CONSTITUTION.md`'s header, both citing `ADR-0042`'s ratified authority hierarchy (**OWNER -> PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> ...**) so a reader is not misled by either document's own status label. Neither document's substantive content, ratification status, or version meaning changed - `docs/PROJECT_CONSTITUTION.md` remains `DRAFT` (still pending Q5), `engineering/ENGINEERING_CONSTITUTION.md` remains `ACTIVE` (still describes its own in-force operational status, not precedence). Both bumped PATCH (0.1.0 -> 0.1.1; 1.1.0 -> 1.1.1) with change-history entries recording exactly this.
  - **Finding 2 - `specs/CLAUDE_WORKFLOW.md` carried no status header at all**, contrary to `docs/DOCUMENTATION_STANDARD.md` s2's mandatory structure. Repaired by adding the mandatory status header (`Status: DRAFT` - honestly stated as not yet run through the `DRAFT -> REVIEW -> RATIFIED -> SUPERSEDED` lifecycle `docs/DOCUMENTATION_STANDARD.md` s4 defines, `Owner: TBD` matching the same convention used elsewhere pending Q1's remaining scope) and a change-history section. Substantive workflow content unchanged, per `reports/AI_COLLABORATION_INSPECTION.md` s3's own assessment that the content is sound and only its governance framing was missing.
  - **Finding 3 - `docs/PROJECT_MASTER.md` stale, unflagged contradiction of `ADR-0041`** (lists `app/` and top-level `tests/` as canonical structure; `ADR-0041` explicitly excludes both). Repaired by adding a superseded/historical-record banner at the top pointing to `README.md`'s "Current state" section and `docs/PROJECT_BACKLOG.md` as the current authoritative sources, and to `ADR-0041` for the canonical structure. The historical body (Flutter-era milestones, repository structure, progress checklist) is preserved unedited below the banner, per this repository's practice of not rewriting history - only the banner and a new change-history entry are additions.
  - **Scope discipline:** the wider "42 document status headers keep reading `Owner: TBD`" observation (`docs/OPEN_QUESTIONS.md` Q1, line 214) and any other staleness not named in `ADR-0044` D7's specific three-item list were left untouched - out of this session's authorized G7 scope, and DP-001 (which would resolve the underlying `Owner: TBD` question generally) remains unanswered.
- **Validation:** `python -m pytest -q` - 558 passed, 0 failed, 0 skipped (unchanged from `ADR-0049`'s baseline, as expected for a documentation-only change). `scripts/check_identifier_families.py`, `scripts/check_retired_identifiers.py`, `scripts/check_adr_numbering.py` - all PASS. `scripts/check_artifact_drift.py` - PASS, 37 evidence files identical outside volatile fields, confirming zero certification impact from this entry. `git diff --check` - clean. No negative control was constructed for this entry: no gate logic, invariant, or certified behaviour changed - the existing governance gates' own established negative-control precedent (`ADR-0043`, `ADR-0049`) remains the evidence they can still fail; nothing here altered that evidence.
- **Consequences:** No certified calculation behaviour, certification artifact, or gate script changed. `docs/PROJECT_CONSTITUTION.md`, `engineering/ENGINEERING_CONSTITUTION.md`, `specs/CLAUDE_WORKFLOW.md`, and `docs/PROJECT_MASTER.md` are the only files modified, all documentation-only. **Phase G exit status: still NOT a candidate for exit.** G7 is now satisfied; G5 remains unmet, for the reason recorded above rather than by omission. Independently re-verified against `docs/Q8_CLOSURE_MATRIX.md` s3 in this same session: **G2** (`ADR-0015` charter adoption) is unissued - `specs/PROJECT_CHARTER.md` carries no status header or ratification record at all; **G3** (`ADR-0016` precedence hierarchy and agent workflow) is unissued as its own reserved entry, though its precedence-hierarchy substance was separately ratified under `ADR-0042` (a different number), following the same reserved-item-superseded-by-a-differently-numbered-entry pattern already established for `DP-003`/`ADR-0020` D6 - its "agent workflow" half has no corresponding ratified decision found; **G4** (decision-paper mechanism) is satisfied - `ADR-0040` (ACCEPTED) established the numbering/registration process and it is in active use (`DP-008`, `DP-009`, `DP-010`); **DP-001** remains `RESERVED, not drafted` (`docs/decisions/README.md`). This entry does not authorise, and must not be read as authorising, FOUNDATION or any product-domain work, and does not itself resolve G2, G3, or DP-001, none of which were in this session's authorized scope.
- **Evidence:** `docs/Q8_CLOSURE_MATRIX.md` s3 (the exit criteria being audited); `ADR-0044` D7 and `reports/AI_COLLABORATION_INSPECTION.md` s2.8/s3/s4 (the exact three G7 findings and their recommended minimal repair, s4 item 10); `ADR-0049`'s own Phase-G-exit-status paragraph (source of the "G5/G7 unmet" framing this entry updates); `scripts/check_adr_numbering.py` output (`ADR-0015`-`ADR-0017` reservation-gap confirmation, unchanged by this entry); direct inspection of `specs/PROJECT_CHARTER.md`, `docs/decisions/README.md`, `docs/OPEN_QUESTIONS.md` Q1 (owner ratified in part, `ADR-0033` D1); `git diff` of the four modified files; `python -m pytest -q`, `scripts/check_identifier_families.py`, `scripts/check_retired_identifiers.py`, `scripts/check_adr_numbering.py`, `scripts/check_artifact_drift.py`, `git diff --check` output cited above.

---

## ADR-0051 - Owner ratification of ADR-0015 (charter), ADR-0016 (precedence hierarchy and agent workflow), ADR-0017 (C0-C5 taxonomy), and DP-001 Option B

- **Date:** 2026-08-17
- **Status:** **ACCEPTED.** It is accepted because the owner supplied the decisions below as an explicit ratification instruction ("CEO AUDITED OWNER AUTHORIZATION - PHASE G REMAINING GOVERNANCE DECISIONS"), following the same evidentiary pattern already used in `ADR-0033`, `ADR-0035`, `ADR-0036`, `ADR-0048` and `ADR-0049`: the instruction reached the repository through a working session, and this entry is what makes it authoritative, per `docs/PROJECT_CONSTITUTION.md` s7 and s11. No historical conversation transcript is manufactured; only the decisions themselves, as given, are recorded, dated to this entry's own date.
- **Context:** `ADR-0015`, `ADR-0016` and `ADR-0017` were drafted PROPOSED in the immediately preceding session (commit `02eb45e`), each explicitly awaiting owner ratification and none self-ratified. `docs/decisions/DP-001-owner-ratification-and-mechanism.md` was drafted the same session, presenting Options A-D and recommending Option B without deciding. The owner has now reviewed all four and supplied explicit decisions for each, which this entry records.

### Decision 1. ADR-0015 ratified: `specs/PROJECT_CHARTER.md` adopted as the ACE Project Charter

`ADR-0015` is ratified **as written**. `specs/PROJECT_CHARTER.md`'s existing substantive content (Product motive, Analytical systems, Isolation protocol, Scientific limitation) is accepted **unchanged** - this entry does not rewrite it. The owner explicitly confirms the distinction `ADR-0015` itself already drew and does not weaken it: **the Project Charter does not replace or supersede `docs/PROJECT_CONSTITUTION.md`.** `docs/PROJECT_CONSTITUTION.md` remains the governing constitutional authority (per `ADR-0042`'s ratified hierarchy: OWNER -> PROJECT CONSTITUTION -> ...); `specs/PROJECT_CHARTER.md` is the project/product/methodology charter, one rung below it. `ADR-0015`'s disposition of the three ambiguous "charter section 11" references (`docs/OPEN_QUESTIONS.md` Q14, `reports/PHASE_G_GOVERNANCE_AUDIT_2026-08-13.md`, `ADR-0033` Decision 4) is ratified as already correctly performed; no further action on those references is required.

### Decision 2. ADR-0016 ratified: precedence-hierarchy component closed by reference; agent-workflow component ratified

**Precedence-hierarchy component:** the owner accepts that `ADR-0042` already satisfies this component in full. No hierarchy text is duplicated or rewritten here; the governing hierarchy remains exactly as `ADR-0042` Decision 1 states it: **OWNER -> PROJECT CONSTITUTION -> ENGINEERING CONSTITUTION -> DECISION LOG / ADR -> STANDARDS -> SPECIFICATIONS -> CODE -> CONVERSATION.** `ADR-0016`'s Decision 1 (recording this same satisfaction-by-reference) is ratified as written.

**Agent-workflow component:** `specs/CLAUDE_WORKFLOW.md` is ratified **as written** as the ACE agent-workflow specification, per `ADR-0016`'s Decision 3 recommended option. It is not rewritten by this entry, and no constitutional text is duplicated into it. **Explicit constraint, binding:** ratification does not change its position in the `ADR-0042` hierarchy - it remains at the SPECIFICATIONS rung, subordinate to `PROJECT CONSTITUTION`, `ENGINEERING CONSTITUTION`, and `DECISION LOG / ADR`. `specs/CLAUDE_WORKFLOW.md` MUST NOT be read, cited, or extended as an independent source of authority capable of overriding `docs/PROJECT_CONSTITUTION.md` or any accepted ADR. Its own status header is updated (this entry) from `DRAFT` to `ACCEPTED`, citing this ratification; its substantive text (the handoff-package pattern, "two AI systems agreeing is not evidence of correctness," Claude's implementation-engineer role) is unchanged.

**`ADR-0022` disposition:** confirmed exactly as `ADR-0016` Decision 2 already recorded it, and not expanded. `ADR-0022` is **not edited, rewritten, or deleted**. Its Decision 1 (the earlier, three-level-top hierarchy proposal) is superseded in substance by `ADR-0042`, recorded here and in `ADR-0016` as a cross-reference, never as an edit to `ADR-0022` itself. `ADR-0022` Decisions 2-4 (the root `DECISION_LOG.md` D-00x family's disposition) are **left untouched and unresolved** - no existing repository governance rule was found requiring more than the documentary cross-reference `ADR-0016` already supplies, so none is added.

### Decision 3. ADR-0017 ratified: C0-C5 claim/evidence classification framework adopted

`ADR-0017` is ratified as a **claim/evidence classification framework**, not a confidence score. The owner supplies the following as the **final, binding definitions**, superseding `ADR-0017`'s own Section 3 "proposed policy" language in effect (that original section is not edited - it stands as the historical record of what was proposed; this entry's text governs going forward):

| Level | Definition |
|---|---|
| **C0** | Research. Proposed research/specification/design. No implementation is thereby authorized. |
| **C1** | Ratified specification. The specification has been owner-ratified. No certified implementation is implied. |
| **C2** | Implemented and internally validated. Implementation exists and satisfies the applicable internal validation requirements. |
| **C3** | Independently externally cross-checked. The implementation has passed appropriate independent external/reference comparison, but this alone does not constitute a C4 software-correctness certification. |
| **C4** | Certified software correctness. A claim concerning correctness of the software implementation against its specified calculation/validation requirements. |
| **C5** | Protected empirical/world claim. A claim about the real-world predictive performance of a method/system, supported through the protected empirical validation/prediction-ledger framework and its pre-registered falsification criteria, protected population, and stated sample size. |

**Critical distinction, restated as binding, not advisory:** C0-C5 are not a simplistic confidence score. **C4 MUST NOT be represented as C5.** Correct software implementation does not establish real-world predictive validity. This restates, and does not weaken, `docs/H6_PREDICTION_LEDGER_SPEC.md` s5 and the standing invariant already present in `docs/PROJECT_ROADMAP.md` line 178 and `docs/Q8_CLOSURE_MATRIX.md` s14.

**Locked status, decided: orthogonal.** `docs/PROJECT_CONSTITUTION.md` s12 "Locked" remains a separate constitutional status requiring the section-12 conditions (written spec/profile; passing reproducible verification; same-run machine- and human-readable evidence agreement; a decision-log entry recording the lock). **`C4` is explicitly NOT auto-defined as `Locked`.** `C4` concerns software correctness; `Locked` is the constitutional status. A component may hold a C-level classification and, separately, Locked status where s12's conditions are independently satisfied - this resolves `ADR-0017` Section 4 decision point 3 as "kept deliberately separate," not "mapped."

**`docs/VALIDATION_STANDARD.md`, decided: not replaced.** Its existing claim-class vocabulary ("Works," "Accurate / within tolerance," "Certified / locked," "Faster / better") is **not deleted or replaced**. No equivalence between it and C0-C5 is manufactured by this entry, because none is supported by existing documents (`ADR-0017` Section 2's own finding, confirmed here). If a precise cross-reference is wanted later, it is a separate future item, not decided now. This resolves `ADR-0017` Section 4 decision point 4 as "kept independent for now."

**`docs/MASTER_ARCHITECTURE.md`'s unrelated C4 architecture-model terminology, decided: documentation follow-up, NOT a Phase G blocker.** The token collision (`ADR-0017` Section 2's finding) is real and must not be allowed to create certification-terminology ambiguity going forward, but resolving it is explicitly **not** made a condition of G5 or of Phase G exit, and no change to `docs/MASTER_ARCHITECTURE.md` is made by this entry. Recorded here as an open documentation follow-up item, unscheduled. This resolves `ADR-0017` Section 4 decision point 5 as "flagged, deferred, not a blocker."

**G6-class reproducibility/infrastructure determinations, decided: remain outside the C0-C5 scale**, exactly as `ADR-0017` Section 3's own proposed note stated and Section 1's evidence already showed (the G6/`ADR-0018` determination "certifies no calculation... is not a C4 or C5 claim"). This resolves `ADR-0017` Section 4 decision point 6 as adopted.

`ADR-0017` Section 4 decision point 1 (whether a six-level scale is wanted at all) and decision point 2 (whether the C1/C2/C3 definitions are acceptable) are resolved by this entry's adoption of the table above: yes, six levels, with the definitions as tabulated - which are compatible with, and in the case of C3 nearly identical in substance to, `ADR-0017`'s own "weakest, explicitly flagged" C3 proposal.

### Decision 4. DP-001 Option B accepted; interim ownership decided

`docs/decisions/DP-001-owner-ratification-and-mechanism.md` Option B is accepted:

1. **The ratification-mechanism half is answered IN PART** by `ADR-0033` Decision 1 and the subsequent twenty-five-entry owner-ratification precedent it established. This is the operative mechanism; it is not retrospectively replaced or invalidated, and none of the twenty-five previously-Accepted ADRs (`ADR-0001`, `ADR-0002`, `ADR-0005` through `ADR-0012`, `ADR-0033` through `ADR-0037`, `ADR-0039` through `ADR-0042`, `ADR-0044`, `ADR-0045`, `ADR-0046`, `ADR-0048`, `ADR-0049`, `ADR-0050`) is reopened, re-tested, or invalidated by this entry.
2. **The named-owner half is resolved: until explicitly delegated, the Project Owner (Prashant Kumar) holds the docs-owner, engine-owner and release-owner responsibilities**, in addition to the Project Owner role already named in `ADR-0033` Decision 1. No additional person or role holder is invented. This is stated as an **interim arrangement**, explicitly reversible by future, explicit owner delegation - it does not foreclose naming separate individuals later.

`docs/decisions/README.md`'s DP-001 index row, `docs/decisions/DP-001-owner-ratification-and-mechanism.md`'s own status header, and `docs/OPEN_QUESTIONS.md` Q1's row are updated (this same pass) to record this disposition, so the repository stops describing DP-001 as blocking "ratification of all PROPOSED ADRs" when the twenty-five-entry precedent already demonstrates the operative mechanism, and stops describing the docs/engine/release-owner roles as undesignated when this entry designates them, interim, to the Project Owner.

- **Consequences:** `ADR-0015`, `ADR-0016` and `ADR-0017`'s own Status lines are updated (mechanical field only, per the `ADR-0009`/`ADR-0001`/`ADR-0002` pattern - their Context/Decision/Consequences/Evidence bodies are **not** edited) to ACCEPTED, citing this entry. `specs/PROJECT_CHARTER.md` and `specs/CLAUDE_WORKFLOW.md` status headers are updated to reflect adoption/ratification; neither document's substantive text changes. No certified calculation behaviour, certification artifact, or already-Accepted decision entry (other than the mechanical Status-line updates named above, which this entry's own governance explicitly authorizes) is touched. **Phase G exit status: independently re-audited below, not assumed.**
  - **G2 (charter adoption): now satisfied.** `ADR-0015` is ACCEPTED; `specs/PROJECT_CHARTER.md` is the adopted charter.
  - **G3 (precedence hierarchy and agent workflow): now satisfied.** `ADR-0016` is ACCEPTED; the precedence-hierarchy component is closed by reference to `ADR-0042`, and the agent-workflow component is closed by ratification of `specs/CLAUDE_WORKFLOW.md`.
  - **G5 (certification taxonomy): now satisfied.** `ADR-0017` is ACCEPTED with the binding C0-C5 table above.
  - **G4 (decision papers): remains satisfied**, as recorded in `ADR-0050` (`ADR-0040` mechanism, in active use).
  - **G7 (stale documentation): remains satisfied**, as recorded in `ADR-0050`.
  - **B-01/B-02/B-03: remain RESOLVED**, as recorded in `ADR-0049`; unaffected by this entry.
  - **DP-001: now OPEN, dispositioned per Decision 4 above** - not formally CLOSED as a paper (it remains an options paper on record, per `docs/decisions/README.md`'s own convention that a paper decides nothing), but its practical question is answered by this entry.
  - `docs/Q8_CLOSURE_MATRIX.md` s3's Phase G exit criteria are: "G2, G3, G4, G5, G7 complete. DP-001 answered so ADR entries can leave PROPOSED. The three BLOCKER findings B-01, B-02, B-03 either resolved or explicitly deferred by decision." **Every named item is now satisfied or resolved**, verified individually above rather than assumed. Per `docs/Q8_CLOSURE_MATRIX.md` s1's own caution, this entry states that fact but does **not** itself constitute the separate CEO-approval act the matrix's own "CEO approval" row for Phase G requires for exit to be declared complete - that determination is made in this session's evidence report, citing this entry as the basis.
- **Evidence:** `ADR-0015`, `ADR-0016`, `ADR-0017` (full prior text, commit `02eb45e`); `docs/decisions/DP-001-owner-ratification-and-mechanism.md` (full prior text, commit `02eb45e`); `ADR-0042` (hierarchy); `ADR-0022` (unedited); `docs/H6_PREDICTION_LEDGER_SPEC.md` s5; `docs/PROJECT_CONSTITUTION.md` s12; `docs/VALIDATION_STANDARD.md` s1; `docs/MASTER_ARCHITECTURE.md`; `docs/Q8_CLOSURE_MATRIX.md` s3; the owner's explicit ratification instruction, this session, 2026-08-17 ("CEO AUDITED OWNER AUTHORIZATION - PHASE G REMAINING GOVERNANCE DECISIONS"); post-change `python -m pytest -q`, `scripts/check_adr_numbering.py`, `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py`, `scripts/check_artifact_drift.py`, `git diff --check` results cited in this entry's own commit.

---

## ADR-0052 - Owner ratification of DP-009 Option B: rise/set Tier-0, panchanga Tier-1

- **Date:** 2026-08-17
- **Status:** **ACCEPTED.** The owner explicitly approved DP-009 Option B and authorised only the associated governance recording plus H-04/M-03 gate remediation. This entry records the owner decision; it does not manufacture a historical transcript or expand that authorization.
- **Context:** `docs/Q8_CLOSURE_MATRIX.md` section 4 makes DP-009 an explicit FOUNDATION prerequisite because the tier classification determines the certification methodology. `docs/decisions/DP-009-panchanga-riseset-tier.md` presents options but correctly decides nothing itself. Its Option B is the recommended methodological distinction: rise/set is convention-parameterized astronomical calculation, while most panchanga elements are deterministic classification over astronomical values. Vara depends on sunrise and therefore cannot honestly be placed wholly on either side.
- **Decision:** Accept DP-009 **Option B**. **Rise/set is Tier-0. Panchanga is Tier-1. Vara is explicitly documented as straddling the boundary** because its sunrise-to-sunrise definition depends on the Tier-0 rise/set calculation. Tier classification distinguishes validation methodology; it does not diminish the requirement for rigorous certification or permit a dependent capability to use an uncertified input.
- **Consequences:** No FOUNDATION, panchanga, rise/set, Muhurta, or other product-domain capability is implemented or authorised by this entry. Before any dependent production use, rise/set retains the required Tier-0 profile/convention declaration and independent astronomical-reference gates; panchanga retains the Tier-1 frozen-rule, independent-transcription, dense-sweep, ULP-boundary, external-reference, validator, holdout and regenerable-artifact gates stated in the ratified roadmap. Vara must declare and certify its rise/set dependency and high-latitude behavior rather than treating it as a pure longitude classification. `docs/decisions/README.md` and the DP-009 row in `docs/OPEN_QUESTIONS.md` are updated to mark the paper's question addressed; the paper itself remains unedited as the historical options record.
- **Evidence:** Owner instruction, 2026-08-17: "APPROVE DP-009 OPTION B. Rise/set Tier-0; Panchanga Tier-1; Vara explicitly documented as straddling the boundary." `docs/decisions/DP-009-panchanga-riseset-tier.md`; `docs/Q8_CLOSURE_MATRIX.md` section 4; `ADR-0017` / `ADR-0051` Decision 3 classification framework. Post-change governance and certification-gate verification is recorded in this remediation commit and must not be confused with FOUNDATION entry or CEO approval.

---

## ADR-0053 - H-04 (Vimshottari depth-3 oracle gate) and M-03 (anti-fitting scan coverage) remediated

- **Date:** 2026-08-17
- **Status:** ACCEPTED, on the owner's explicit authorization of H-04 and M-03 remediation as scoped FOUNDATION entry-criteria gate-integrity work (`docs/Q8_CLOSURE_MATRIX.md` s4), following the same pattern as `ADR-0049`'s B-01/B-02/B-03 authorization: implementation, forensic re-verification, negative controls, and certification evidence, recorded here rather than trusted from the implementing commit's own claim.
- **Context:** `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` "H-04": `scripts/certify_vimshottari.py` passed `depth=2` to the oracle comparison while `ADR-0007` and `docs/ENGINE_STATUS.md` claimed depths 1-3 certified - a documentation-versus-evidence conflict, not a calculation defect (the audit ran the missing comparison in memory and it passed). "M-03": `scripts/certification_support.py`'s anti-fitting scan defaulted to `targets=("engine",)`, so none of the eleven certifiers, eleven root validators, or the fixture module were ever scanned for fitting patterns, making the gate evadable outside `engine/`.
- **H-04, implementation (commit `37aca59`, author Prashant Kumar):** `scripts/certify_vimshottari.py` changed `depth=2` to `depth=3`, `timeline.antardashas()` to `timeline.pratyantardashas()`, the expected row count from 81 to 729 per case (matching the G1 audit's in-memory result exactly), and the PyJHora oracle call to request `dhasa_level_index=... .PRATHYANTARA` at pratyantar depth. `engine/dasha/vimshottari.py` required **no change**: `depth: int = 3` was already its default and `pratyantardashas()` already existed - the engine has certified depth-3 mathematics since before this entry; only the certifier script was undershooting it.
- **H-04, defect found and fixed during this entry's forensic verification, not assumed correct from the commit:** pushing `37aca59` and inspecting CI run `32048557295` showed the oracle-tier job failing with `AttributeError: PRATHYANTARA. Did you mean: 'PRATYANTARA'?` - the PyJHora enum member is spelled `PRATYANTARA`; the implementing commit had it as `PRATHYANTARA` (transposed), so **the depth-3 oracle comparison had never actually executed successfully**. Corrected to `jhora_const.MAHA_DHASA_DEPTH.PRATYANTARA` in this entry's own commit. This is exactly the class of error independent verification exists to catch: the certifier code read as correct and the commit message claimed the remediation, but the gate had never actually run.
- **M-03, implementation (commit `37aca59`):** `scripts/certification_support.py` gained `CERTIFIER_SOURCES` (the twelve `scripts/certify_*.py` files present in the tree - the G1 audit's "eleven" plus `certify_current_engine.py`, which postdates the audit), `VALIDATOR_SOURCES` (the eleven root `validate_*_holdout.py` files), and `FIXTURE_SOURCES` (`brihat_fixtures.py`); `scan_for_fitting`'s default `targets` changed from `("engine",)` to the union of all of these. `_source_files()` fails closed: a declared target that is missing or not a `.py` file raises `CertificationFailure` rather than silently scanning less than declared. The holdout-reference and forbidden-import checks remain scoped to `engine/` only (certifiers and validators legitimately declare holdout IDs and import the oracle/fixtures/legacy kernel by design; applying that rule to them would make the gate permanently fail rather than detect fitting); the suspicious-identifier-fragment check applies to every scanned file without exception.
- **M-03, independently re-verified in this entry, not merely trusted from the commit's tests:** direct invocation of `scan_for_fitting()` with no arguments (i.e., the real default, not a mocked target) scanned **170 modules with zero findings**, up from the pre-fix ~146 (`engine/` alone). A manually constructed clean file passed; a manually constructed file containing `magic_number = 42` (a `_SUSPICIOUS_NAMES` fragment) at an arbitrary `targets=(...)` location correctly raised `CertificationFailure` citing `suspicious_identifier`. `discovered_certifiers` (globbed from `scripts/certify_*.py`) and `discovered_validators` (globbed from `validate_*_holdout.py`) were independently recomputed and found to equal `CERTIFIER_SOURCES`/`VALIDATOR_SOURCES` exactly - the declared scan surface does not silently omit or duplicate anything currently on disk.
- **Tests (commit `37aca59`):** `engine/tests/test_certification_preconditions.py` gained `test_anti_fitting_scan_covers_every_declared_certification_source` (cross-checks the declared source lists against what is actually discoverable on disk, so a future certifier or validator added without updating the declaration fails this test rather than silently going unscanned) and `test_anti_fitting_scan_rejects_a_certifier_named_adjustment` (negative control: a synthetic `certify_probe.py` containing an `adjust_for`-fragment pattern, scanned via `scan_for_fitting`, must raise `CertificationFailure` - proving the expanded scan surface can actually detect a violation outside `engine/`, not merely count files). `test_anti_fitting_scan_is_clean`'s module-count assertion was raised from `> 100` to `>= 170`. `test_artifact_carries_its_preconditions`'s assertion is deliberately left at `> 100`, not raised to match the new count, because it reads the **committed, not-yet-regenerated** artifacts, which correctly still record their pre-M-03 scan surface - raising it would assert a number those stored artifacts do not contain, and VALIDATION_STANDARD s2 rule 8 forbids treating a stored artifact as anything but history.
- **Certification-artifact impact, consequence of M-03 working as intended:** all eleven certification artifacts legitimately report `preconditions.anti_fitting.modules_scanned: 170` (was 146) and a non-empty `justified_exceptions` list once regenerated, because the scan surface itself changed; `VIMSHOTTARI_V1` additionally reports the H-04 schema change (`oracle_bhukti_rows_compared` -> `oracle_pratyantar_rows_compared`, 1782 -> 16038 rows, `oracle_max_start_delta_days` 1.86e-09 days, `oracle_lord_mismatches: 0`). This is **expected drift caused directly by this entry**, not an unexplained change; `scripts/check_artifact_drift.py` correctly flagging it as non-volatile is the drift gate performing its job, not a defect in it.
  - **Eight oracle-tier artifacts (`D2`, `D3`, `D7`, `D12`, `D30`, `VIMSHOTTARI`, `TRANSIT`, `PARASHARI_DRISHTI`) regenerated for real on CI's Linux oracle-tier runner** (`.github/workflows/ci.yml` `oracle` job, real PyJHora, hash-pinned) after the `PRATHYANTARA` typo fix, CI run `32051145458`: the "Oracle certification runners (all eight)" step **passed**, downloaded via `oracle-certification-evidence`, and drift-checked locally: every non-VIMSHOTTARI artifact differs from the previously-committed version in exactly the two M-03 fields; VIMSHOTTARI additionally differs in exactly the H-04 fields described above; nothing else changed in any of the eight - no calculation, gate count, tolerance or verdict moved. Committed in this entry's own commit.
  - **`current_engine`, `KP_CHAIN_V1`, `SIGN_CONVENTION_V1`: gap diagnosed, then closed within this same entry.** `current_engine` cannot run on this Windows host at all: `certify_current_engine.py` shells out to the repository's bundled `swetest`, confirmed by direct inspection (`file ./swetest`) to be an `ELF 64-bit LSB pie executable ... for GNU/Linux` - `[WinError 193] %1 is not a valid Win32 application` is Windows correctly refusing to execute a Linux binary, the same documented platform limitation as `ADR-0043`. The CI oracle job's own upload step (`path: certification/*.json`) was checked directly and confirmed to upload whatever is in that directory at upload time, not to regenerate `current_engine`/`KP_CHAIN`/`SIGN_CONVENTION` - its "Oracle certification runners" step runs exactly the eight scripts named above and no others, so its bundle's copies of these three were confirmed (direct field comparison) to be the unregenerated, already-committed 146-scan versions, not fresh evidence, and were discarded rather than mistaken for real regeneration. A local Windows regeneration of `KP_CHAIN`/`SIGN_CONVENTION` (`pyswisseph`, no `swetest`/PyJHora dependency) produced the correct M-03 drift with zero other change, but its console transcript recorded the archived path with a Windows backslash where every other artifact records a POSIX forward slash - a genuine cross-platform provenance difference, declined (not committed, not hand-edited).
  - **Closure:** `.github/workflows/ci.yml`'s `hermetic` job gained an `actions/upload-artifact@v4` step (`hermetic-certification-evidence-${{ matrix.python-version }}`), mirroring the `oracle` job's existing one exactly, placed after the network-guard re-run and before the drift assertion so a legitimate drift failure still preserves the artifacts, with `if: always()` affecting only whether the upload step itself runs, never the job's pass/fail verdict, and no `continue-on-error` anywhere. `check_artifact_drift.py` was not moved, weakened, or bypassed. Pushed as its own commit; CI run `32053467926` confirms the upload step succeeded on both matrix legs while the (expected, unchanged) drift-assertion failure persisted. Both `hermetic-certification-evidence-3.11` and `-3.12` bundles were downloaded and independently compared field-by-field, ignoring only the same six volatile fields `check_artifact_drift.py` itself permits: identical. All three artifacts record `preconditions.anti_fitting.modules_scanned: 170`, `justified_exceptions` length 1, `result`/`summary.result: PASS`, and archived paths with POSIX forward slashes (confirming genuine Linux/CI provenance, not the Windows-path artifact discarded above). Overlaid into the working tree and drift-checked against the previously-committed (146-scan) versions: **every one of the three differs in exactly the two M-03 preconditions fields and nothing else** - the identical pattern already established for the eight oracle-tier artifacts. Committed in this entry's own follow-up commit. All eleven certification artifacts are now current with the M-03 scan surface; H-04's depth-3 evidence (`VIMSHOTTARI_V1`) was already committed above.
- **Consequences:** No certified numeric or categorical calculation output changes: H-04 exercises mathematics the engine already computed by default: M-03 changes what is scanned for fitting, not any calculation. `docs/Q8_CLOSURE_MATRIX.md` s4 entry criteria E4 (H-04) and E5 (anti-fitting scan coverage) are satisfied by code and test, pending the CI-sourced artifact regeneration this entry's evidence completes. FOUNDATION is **not thereby entered**: DP-009 (`ADR-0052`) and gate-integrity (this entry) being satisfied are FOUNDATION *prerequisites and entry criteria*, not an owner authorization to begin FOUNDATION implementation, which remains a separate, explicit, not-yet-given act.
- **Evidence:** `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md` H-04 and M-03 sections; commit `37aca59` full diff; CI run `32048557295` (failure, both defects diagnosed above, before the typo fix); CI run `32051145458` (commit `4985f16`, after the typo fix: governance gate PASS; oracle job's "Oracle certification runners (all eight)" step PASS with real PyJHora, confirming H-04's depth-3 comparison actually executes - `oracle_pratyantar_rows_compared: 16038` (2 profiles x 11 cases x 729 rows), `oracle_lord_mismatches: 0`, `oracle_max_start_delta_days: 1.862645149230957e-09` against a `1e-05`-day tolerance, matching the G1 audit's in-memory prediction ("729 rows per case... zero lord mismatches, maximum start delta 1.86e-09 days") exactly; the job's overall drift-assertion step correctly failed on the expected, understood schema/scan-surface change, not an unexpected one); direct inspection of `engine/dasha/vimshottari.py` (depth-3 default and `pratyantardashas()` pre-existing) and `engine/models/dasha.py`; direct inspection of `.github/workflows/ci.yml`'s `oracle` job (exact eight scripts run; upload step's actual scope) to diagnose why `current_engine`/`KP_CHAIN`/`SIGN_CONVENTION` are not obtainable from it; manual independent invocation of `scan_for_fitting()` (170 modules, 0 findings) and of the clean-file/dirty-file negative-control pair, this session; local regeneration of `KP_CHAIN_V1`/`SIGN_CONVENTION_V1` (both PASS, correct M-03-only drift, discarded for the Windows-path-separator provenance reason stated above); `python -m pytest -q` - 560 passed, 0 failed, 0 skipped, including the corrected `test_vimshottari_certification.py` pinning assertions against the real regenerated artifact; `scripts/check_adr_numbering.py`, `scripts/check_identifier_families.py`, `scripts/check_artifact_drift.py` (confirms the eight committed artifacts differ from pre-entry HEAD in exactly the fields described above and nothing else) - all PASS; `file ./swetest` output (ELF, Linux) as the Windows-limitation diagnosis.

---

## ADR-0054 - FOUNDATION first work package: sunrise/sunset (rise/set), five owner-ratified conventions

- **Date:** 2026-08-18
- **Status:** ACCEPTED, on the owner's explicit authorization ("CEO OWNER AUTHORIZATION - FOUNDATION RISE/SET") ratifying five specific conventions and the complete rise/set workstream, following the prior session's explicit stop-and-report (this same register, no separate entry: no rise/set spec, ADR, or `CalculationProfile`/`BirthData` field existed anywhere in the tracked tree before this entry, confirmed by direct search before implementation began).
- **Context:** `docs/Q8_CLOSURE_MATRIX.md` s4 lists "Rise and set with declared conventions" first in FOUNDATION's implementation scope; `docs/decisions/DP-009-panchanga-riseset-tier.md` s6 named the convention set required but never decided it ("must not be resolved by implementation convenience"). `ADR-0020` D2 established rise/set as Tier-0, requiring independent certification before any dependent capability (panchanga's `vara`, Rahu Kalam/Yamaganda/Gulika) relies on it. None of those dependent capabilities is touched by this entry.
- **Decision - the five ratified conventions, binding, none inferred:**
  1. **Upper-limb solar disc.**
  2. **Standard atmospheric refraction, -50' standard altitude** (34' refraction + 16' mean solar semi-diameter, the classical almanac convention).
  3. **Observer elevation accounted for.**
  4. **Explicit structured `NO_RISE`/`NO_SET`** result when the event does not occur that day (circumpolar), never an exception, never a silently-wrong timestamp.
  5. **Conventions represented in the existing `CalculationProfile`; elevation represented in the existing location input model (`BirthData`).**
- **Implementation:**
  - `engine/astronomy/profile.py`: `CalculationProfile` gains `rise_set_disc_reference` (default `RISE_SET_DISC_UPPER_LIMB`) and `rise_set_refraction` (default `RISE_SET_REFRACTION_STANDARD`) fields. `PARASHARI_LAHIRI`/`KP_KRISHNAMURTI` are unmodified in substance - both instances gain the two new fields only via the dataclass defaults, since both are constructed with keyword arguments. **Zero calculation impact, proven, not assumed:** full `pytest` suite (560 tests, pre-existing baseline) re-passed unchanged; `certify_kp_chain.py`/`certify_sign_convention.py` (the two non-oracle certifiers runnable on this host) re-executed locally and drift-checked against committed evidence - the only difference was `anti_fitting.modules_scanned` incrementing by exactly one (the new `rise_set.py` file being scanned), nothing else; `ayanamsa_mode`/`house_system` values asserted unchanged directly in `scripts/certify_rise_set.py`'s own Gate D.
  - `engine/models/birth_data.py`: `elevation_m: float = 0.0` added (last field, so no existing positional or keyword call site breaks). `engine/core/validation.py` validates only finiteness - **no arbitrary range is imposed** (real locations range from the Dead Sea shore, ~-430m, to high mountain settlements): the same "do not invent unjustified limits" discipline `ADR-0049` applied to varga division bounds.
  - `engine/astronomy/rise_set.py` (new): `sunrise()`/`sunset()`, thin wrappers over `swe.rise_trans_true_hor`. Three findings from direct empirical investigation before any code was written, all recorded because the investigation is part of the evidence, not just its conclusion:
    - Plain `swe.rise_trans` with `geopos` altitude and `atpress=attemp=0.0` handles ONLY the atmospheric-pressure/refraction half of elevation. Verified directly: a 4000m-elevation sunrise computed this way was 62.5 seconds **later** than sea level - the physically wrong direction (higher elevation must see the sun earlier). `swe.rise_trans_true_hor`'s explicit `horhgt` parameter (the geometric dip of the horizon) is used instead: `horizon_dip_degrees(h) = 0.0293 * sqrt(h)` degrees (Meeus, *Astronomical Algorithms* ch. 15; equivalent to `arccos(R_earth/(R_earth+h))` for small `h/R`). Re-verified after the fix: the same 4000m case now rises ~487 seconds **earlier**, the correct direction.
    - `swe.rise_trans_true_hor` reports no fallback-mode flag of its own (unlike `swe.calc_ut`). Verified directly: a year-3000 date (outside the bundled 1800-2399 CE ephemeris range) returned a silent, unflagged result with `FLG_SWIEPH` requested. `strict=True` (the default) now calls the existing, already-certified `calc_ut_checked(jd, swe.SUN, swe.FLG_SWIEPH)` first, reusing rather than re-deriving the Tier-0 fallback guard (`engine/astronomy/ephemeris.py`), so the same silent degradation is caught for rise/set too.
    - Circumpolar days (`res == -2`) were verified, for both a permanent-daylight case (Svalbard, June) and a permanent-night case (Svalbard, December), to return `-2` for **both** the rise and the set query on the same day - `RiseSetResult(status=NO_RISE|NO_SET, julian_day_ut=None)` reflects this rather than assuming only one of the two is ever absent.
  - An unratified `rise_set_disc_reference`/`rise_set_refraction` on a profile raises `UnsupportedRiseSetConventionError` rather than being silently applied - only the five ratified conventions above are implemented.
- **Tests:** `engine/tests/test_rise_set.py`, 39 tests: headline sanity, circumpolar (both directions, both events), boundary latitudes (-90 to 90, antimeridian longitudes), elevation (dip formula, monotonic direction in both events, below-sea-level, non-finite rejection), declared-convention enforcement (both fields), strict-mode ephemeris fallback (raises strict, succeeds non-strict, and a dedicated test proving the same call's behaviour genuinely differs by mode, not vacuously), input validation. One genuine negative control: `horizon_dip_degrees` is monkeypatched to always return `0.0` (the exact real defect found and fixed during design, reintroduced deliberately), and the resulting sunrise is confirmed to fall **outside** `validate_rise_set_holdout.py`'s own tolerance against its independent reference - proving that check can actually fail, not merely that it currently passes - then explicitly un-monkeypatched and re-verified restored.
- **Certification (`scripts/certify_rise_set.py`, `RISE_SET_V1`, mirrors the varga A-E gate lettering):**
  - **A (convention integrity):** both certified profiles carry the ratified values; the unratified-convention guard is exercised and confirmed to raise; `BirthData.elevation_m`'s default is asserted `0.0`.
  - **B (dense/boundary sweep):** the same H1-H11 real-world holdout this repository's other certifiers already use (`scripts/certify_vimshottari.py` etc.) - reused, not reinvented - both events, 22 comparisons, against an independently-coded closed-form reference (below), 60-second tolerance.
  - **C (independent reference):** two frozen circumpolar cases (Svalbard summer/winter) checked for the correct `NO_RISE`/`NO_SET` classification; two frozen elevation cases (La Paz, Bolivia, 3640m; Dead Sea shore, -430m) checked against the same closed-form reference, 150-second tolerance.
  - **Why C is a closed-form reference, not the bundled `swetest` binary:** `swetest` cannot run on this Windows host at all (Linux ELF binary, `ADR-0043`/`ADR-0053`), and its command-line rise/set flag support was not established with the same confidence as its already-proven `-house`/`-fPl` position flags (`certify_current_engine.py`). Rather than commit an unverified binary invocation, `certify_rise_set.py` independently re-derives sunrise/sunset from `swe.calc_ut` (apparent equatorial position - the already-Tier-0-certified ephemeris input, never `swe.rise_trans*`) plus `swe.sidtime` (Greenwich sidereal time) plus the classical hour-angle/altitude transform plus an explicit bisection search that never calls `swe.rise_trans_true_hor`. This checks something materially different from an ephemeris cross-check (already settled): whether this module correctly turned that ephemeris data, the ratified conventions and the observer's location into a rise/set time.
  - **Tolerances are derived, not tuned.** Measured directly, before being hardcoded: the closed-form reference disagrees with `swe.rise_trans_true_hor` by 11-25 seconds across the real H1-H11 holdout (worst case Reykjavik, the highest latitude in the set) and by up to ~53 seconds at 4000m elevation. 60s/150s leave comfortable margin. The residual itself has an identified, non-defect cause: the closed-form model applies a flat -50' threshold, while Swiss Ephemeris applies a more realistic altitude-dependent refraction curve near the horizon - the same *class* of external-reference divergence `D-007` already established a precedent for documenting and bounding rather than hiding.
  - **D (non-invasiveness):** ayanamsa modes and house systems for both certified profiles asserted unchanged; the strict-mode fallback guard re-exercised.
  - **E (independent validator):** `validate_rise_set_holdout.py`, a **third, differently-coded** reference (single/double-iteration direct closed-form transit + arccos solve, not the certifier's own sampling-bisection method), against the same holdout plus an equinox day-length property check (11.9-12.3h at five latitudes, honestly wider than exactly 12h to allow for real refraction).
  - **Two genuine defects were found and fixed in this validator during its own construction, before being committed - recorded because independent verification exists to catch exactly this class of error:**
    1. An earlier version's two-pass transit refinement re-sampled Greenwich Sidereal Time at the *moving* transit estimate on the second pass instead of keeping the first pass's fixed-epoch value, silently discarding almost a full day; caught because it produced e.g. a 23:59 UT "transit" for London that visibly could not be right, not merely because a number didn't match.
    2. The initial single-transit ± H0 formula assumed rise always precedes set within a UT-midnight-to-midnight window; false wherever local time is already past sunrise at UT midnight (e.g. Sydney, UTC+10) - a query for "next set" then correctly finds the same afternoon's, while "next rise" needs the *following* day's transit. Caught by an 86,400-second (24-hour scale) discrepancy on the Sydney (`H3`) holdout case alone, fixed by searching both the current and the following day's transit per event and taking the earliest forward result - the same forward-search semantics `swe.rise_trans_true_hor` implements internally.
  - `scripts/certification_support.py`'s M-03 `CERTIFIER_SOURCES`/`VALIDATOR_SOURCES` updated (12->13, 11->12) to include the two new files, keeping the anti-fitting scan's declared surface synchronized with what is actually on disk; `engine/tests/test_certification_preconditions.py`'s matching count assertions updated identically, and its `modules_scanned` floor raised from 170 to 173 (171 for the new `engine/astronomy/rise_set.py`, +1 each for the new certifier and validator).
- **CI:** `.github/workflows/ci.yml` `hermetic` job: `certify_rise_set.py` added to "Non-oracle certification runners" (needs only `pyswisseph`, no `swetest`/PyJHora) and to the network-guard re-run; `validate_rise_set_holdout.py` added to "Independent holdout validators," renamed from "all eleven" to "all twelve." No gate weakened, moved, or bypassed; no `continue-on-error`.
- **Consequences:** No product-domain capability (Panchanga, Muhurta, or any other) is implemented, wired, or authorised by this entry - `engine/astronomy/rise_set.py` is called by nothing yet. No certified numeric or categorical output of any existing capability changes (proven above, not assumed). FOUNDATION's rise/set work package now has a declared-convention profile, a certified implementation, a protected real-world holdout, an independent reference (two independently-coded methods, neither importing the other), meaningful negative controls, and CI integration. This does **not** itself authorise any further FOUNDATION capability (panchanga, Rahu Kalam/Yamaganda/Gulika, H-01, H-02): `docs/Q8_CLOSURE_MATRIX.md` s4's own "CEO approval: entry, per-capability checkpoint, exit" row requires a separate checkpoint for each.
- **Evidence:** `docs/Q8_CLOSURE_MATRIX.md` s4; `docs/decisions/DP-009-panchanga-riseset-tier.md` s6; `ADR-0020` D2; direct empirical investigation of `swe.rise_trans`/`swe.rise_trans_true_hor`/`swe.calc_ut`/`swe.sidtime` behaviour, this session (elevation-direction bug, silent-fallback behaviour, circumpolar both-events behaviour); `python -m pytest -q` - 599 passed (up from 560), 0 failed, 0 skipped; `python scripts/certify_rise_set.py` - PASS, all gates; `python validate_rise_set_holdout.py` - PASS, both independently-fixed defects re-verified fixed; `python scripts/ci_no_network.py scripts/certify_rise_set.py` - PASS under the hermeticity guard; `scripts/check_adr_numbering.py`, `scripts/check_identifier_families.py`, `scripts/check_retired_identifiers.py`, `scripts/check_artifact_drift.py` - all PASS; local re-execution of `certify_kp_chain.py`/`certify_sign_convention.py` confirming zero calculation-value impact from the `CalculationProfile` change. **CI run `32111976327`** (commit `aaa6aba`): governance gate PASS; oracle job's "Oracle certification runners (all eight)" step PASS (rise/set's addition of `engine/astronomy/rise_set.py` did not break any of the eight); both `hermetic` (3.11, 3.12) jobs' full test/validator/certifier steps PASS, including `certify_rise_set.py` itself and `validate_rise_set_holdout.py` under the network guard; all four jobs' drift-assertion steps failed on exactly, and only, `preconditions.anti_fitting.modules_scanned: 170 -> 173` across all eleven previously-existing certification artifacts - the expected, understood consequence of `rise_set.py` (plus the new certifier and validator) joining the M-03 scan surface, not an unexpected change. Regenerated evidence for all eleven downloaded (`oracle-certification-evidence`, `hermetic-certification-evidence-3.11`, `-3.12`; the two hermetic bundles cross-compared and confirmed identical outside the same volatile fields `check_artifact_drift.py` permits), overlaid, and drift-checked locally: confirmed to differ from pre-entry HEAD in exactly that one field per artifact and nothing else. Committed in this entry's own follow-up commit alongside the `RISE_SET_V1` artifact itself.

---

## ADR-0055 - Owner ratification of Panchanga methodology conventions (DP-009 s6); Rahu Kalam/Yamaganda/Gulika deferred

- **Date:** 2026-08-18
- **Status:** **ACCEPTED.** The owner authorized this entry's four decisions with the single word "authorized," given in direct reply to a bundled, explicitly-labelled "OWNER ACTION REQUIRED... Recommended decision, bundled: 1 = ...; 2 = ...; 3 = ...; 4 = ..." report in the same session. This entry records that reply as ratifying exactly the four items as stated in that report, quoted verbatim in Decision below, rather than inferring a broader or narrower scope. Per `docs/PROJECT_CONSTITUTION.md` s11, this recording act is what makes the reply authoritative, matching the precedent already used for `ADR-0052`'s "APPROVE DP-009 OPTION B."
- **Context:** `docs/decisions/DP-009-panchanga-riseset-tier.md` s6 ("What the decision must also settle, whichever option is chosen") lists specific Panchanga methodology questions and states they "must not be resolved by implementation convenience." `ADR-0052` ratified DP-009's tier classification only (rise/set Tier-0, panchanga Tier-1) and explicitly left s6 unresolved. Before any Panchanga implementation began this session, a read-only inspection of the repository (`docs/Q8_CLOSURE_MATRIX.md` s4, `DP-009` s6, `ADR-0052`, `engine/astrology/nakshatra.py`, `engine/astrology/longitude_utils.py`, `engine/kp/README.md`, `scripts/certify_current_engine.py`) confirmed none of s6's items are settled by any existing ratified entry, and that two live, deliberately-different boundary conventions already coexist in this repository (the engine-wide 1e-10 promote-up `[start, end)` convention used by `division_index`/vargas/signs/nakshatra, and the KP package's exact-Decimal/rational interval convention, deliberately divergent per `ADR-0006`/`engine/kp/README.md`) with nothing declaring which governs tithi/yoga/karana. No source table for Rahu Kalam/Yamaganda/Gulika variants exists anywhere in this repository.
- **Decision - the four items, as presented for authorization and accepted verbatim:**
  1. **Tithi/Yoga/Karana boundary convention:** the existing engine-wide 1e-10 promote-up, `[start, end)` convention (the same convention `engine/astrology/nakshatra.py`'s `division_index` already uses, Tier-0 certified in `certify_current_engine.py`), applied uniformly under both the `parashari_lahiri` and `kp_krishnamurti` profiles. The KP package's distinct exact-interval convention is NOT extended to panchanga by this entry.
  2. **Rahu Kalam/Yamaganda/Gulika variant-table selection is explicitly NOT decided by this entry.** No source was named by the owner; per DP-009's own warning that "each variant is a decision to record, never a silent choice," this entry authorizes drafting a short `DP-NNN` options paper naming candidate source tables for separate, later owner ratification. **Implementation of Rahu Kalam, Yamaganda, or Gulika remains NOT authorized** until that table is ratified by a future decision entry.
  3. **Panchanga's first FOUNDATION work package is scoped to classification at a given instant**: which tithi, nakshatra, yoga, karana and vara currently obtain, reusing already-certified primitives (`engine.astrology.nakshatra`, `engine.astronomy.rise_set`) where they exist. **Element start/end transition-timing (the civil-day boundaries of each element) is explicitly deferred to a later, separately-checkpointed work package**, since it requires new certified event-finding/root-finding infrastructure comparable in kind to rise/set's independent bisection solver, not merely classification.
  4. **Vara is computed by consuming the already-certified Tier-0 `engine.astronomy.rise_set` layer** (`sunrise()`), not by reimplementing sunrise logic inside the panchanga module, consistent with `ADR-0052`'s description of vara as depending on, not duplicating, the Tier-0 layer.
- **Consequences:** This entry authorizes implementation of the classification-only first Panchanga work package - tithi, vara, nakshatra (as a panchanga element), yoga, karana at a given instant - each still subject to `docs/Q8_CLOSURE_MATRIX.md` s4's "CEO approval: entry, per-capability checkpoint, exit" and its Tier-1 certification gates (`ADR-0052`). This entry does **not** authorize: Rahu Kalam, Yamaganda, Gulika (pending item 2's future table ratification); element start/end transition timing; H-01, H-02; or any later phase (Muhurta, Varshaphal, Prashna, Mundane, BTR, Interpretation, Convergence, UI, ML). The five owner-ratified rise/set conventions (`ADR-0054`) are unchanged and not reopened by this entry.
- **Evidence:** This session's "ACE CONTINUOUS CEO EXECUTION DIRECTIVE - PANCHANGA FOUNDATION" instruction; this session's read-only inspection findings and "OWNER ACTION REQUIRED" report (the four numbered items and their bundled recommendation, quoted in Decision above); owner reply, verbatim: "authorized." `docs/decisions/DP-009-panchanga-riseset-tier.md` s6; `docs/Q8_CLOSURE_MATRIX.md` s4; `ADR-0052`; `ADR-0054`; direct inspection of `engine/astrology/nakshatra.py`, `engine/astrology/longitude_utils.py`, `engine/kp/README.md`, `scripts/certify_current_engine.py`.

---

## ADR-0056 - Formal four-role AI collaboration model (USER/CLAUDE/CHATGPT/CODEX); Codex excluded from the ACE workflow

- **Date:** 2026-08-18
- **Status:** **ACCEPTED**, on the owner's explicit, self-contained governance instruction: "ACE GOVERNANCE CHANGE - PERMANENT LLM ROLE SEPARATION," given directly in this session, specifying the four roles, their responsibilities, the Git-as-source-of-truth principle, the canonical-handoff discipline, and the explicit Codex exclusion verbatim.
- **Context:** `docs/PROJECT_CONSTITUTION.md` s11 ("AI Collaboration Model") described a two-AI prose model (builder/executor Claude, reviewer/auditor ChatGPT) since the constitution's original drafting, and `ADR-0044` built the tooling scaffolding (`CLAUDE.md`, `.claude/rules/`, `reports/AI_HANDOFF_CURRENT.md`) around that same informal model without ever formalizing a third party's status. Untracked `.codex/` and `AGENTS.md` artifacts present in this working tree (unrelated to this entry; not created or touched by it) indicate Codex has been used informally in or around this repository, which is the direct motivation for making its exclusion explicit rather than assumed. The owner directed a formal, four-role structure - naming Codex out of the ACE workflow specifically - and a concrete, repeatable discipline for how Claude's work reaches ChatGPT for audit, so the user is not needed as a manual message courier between the two AI collaborators.
- **Decision:**
  1. **USER - product owner, final ratifying authority.** Significant architectural, certification, phase, and governance decisions require the user's approval wherever this constitution or `docs/DECISION_LOG.md` requires it.
  2. **CLAUDE - the primary and sole ACE builder/executor.** All ACE coding, repository editing, test execution, certification execution, and commits are performed by Claude. Claude updates `reports/AI_HANDOFF_CURRENT.md` (the canonical Claude -> ChatGPT handoff) after every meaningful implementation task, and must not create a competing handoff mechanism.
  3. **CHATGPT - independent ACE CEO / technical auditor.** Reviews Claude's work independently: audits architecture, specifications, governance, code, tests, certification evidence, provenance, and claims; determines PASS / HOLD / FAIL; provides the exact next action/instruction for Claude when remediation is required. Not an ACE implementation/builder; does not commit to this repository; must not require the user to manually relay Claude's terminal output when the evidence already exists in Git or the canonical handoff.
  4. **CODEX - not part of the ACE workflow.** ACE implementation is Claude's; ACE auditing is ChatGPT's. No third AI worker is introduced into ACE building or auditing under this section, unless the user explicitly changes the ACE workflow in a future decision entry.
  5. **Git is the source of truth** for all of the above: conversation text with any AI collaborator is input material, never authoritative project memory; `reports/AI_HANDOFF_CURRENT.md` is an evidence/index record, not a substitute for Git evidence (restates `docs/PROJECT_CONSTITUTION.md` s7, applied explicitly to the three-AI context).
  6. `docs/PROJECT_CONSTITUTION.md` s11 is amended in place to state roles 1-5 above, replacing its prior two-AI prose while explicitly retaining rules (a)-(d) unchanged (owner ratifies all decisions; audit findings are verified against the artifact, not trusted; each iteration is narrow, evidenced, and recorded; neither AI may weaken targets or redefine "done") - the roles operationalize those rules, they do not replace them. `CLAUDE.md`'s "Your role here" section is updated to match. `reports/AI_HANDOFF_CURRENT.md` gains a structured, repeatable "Task handoff log" section (branch, commit SHA, previous approved commit, task, relevant ADR/specification, files changed, implementation summary, tests executed and results, certification executed and results, known issues, unresolved questions, CEO decision required, next authorized action) so future updates follow one template rather than free-form prose, and its stale 2026-08-17 snapshot is refreshed.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file is touched by this entry - confirmed by diffing the changed-file list before committing. `docs/PROJECT_CONSTITUTION.md` remains `Status: DRAFT` overall (unchanged by this entry; only s11's content and the version/change-history footer are edited, per the same "amend in place, cite the decision entry" pattern `ADR-0042`'s hierarchy ratification and this repair both already use). No prior ADR is edited. `main` is untouched; this entry's commit lands on `phase-g-governance`. The untracked `.codex/`/`AGENTS.md` artifacts already present in the working tree are neither deleted nor incorporated by this entry - their disposition (retain, relocate, or remove) is a separate matter this entry does not decide.
- **Evidence:** Owner instruction, 2026-08-18, verbatim title "ACE GOVERNANCE CHANGE - PERMANENT LLM ROLE SEPARATION," specifying all five decision points above; existing `reports/AI_HANDOFF_CURRENT.md` located and confirmed as the sole existing handoff mechanism (no competing file found: `find . -iname "*HANDOFF*"` returned exactly one match) before it was extended, not replaced. Post-change verification: `python -m pytest -q`; `scripts/check_adr_numbering.py`; `scripts/check_retired_identifiers.py`; `scripts/check_identifier_families.py`; `git diff --check` - exact results cited in this entry's commit message.

---

## ADR-0057 - CEO-audit remediation: ACE interaction mode and mandatory session-start audit permanently encoded

- **Date:** 2026-08-18
- **Status:** **ACCEPTED**, on the owner's explicit relay of a CEO (ChatGPT) audit result: "ACE CEO AUDIT RESULT: HOLD... the existing AI collaboration architecture is substantially correct, but three required protections are not yet permanently encoded," followed by six required permanent rules and an explicit instruction to use the existing `specs/CLAUDE_WORKFLOW.md` / `CLAUDE.md` / `reports/AI_HANDOFF_CURRENT.md` / ADR governance rather than create a new competing workflow.
- **Context:** `ADR-0056` (this same session, immediately prior) already formalized four of the six required rules: Claude as sole ACE builder/executor, ChatGPT as independent auditor with PASS/HOLD/FAIL authority, Codex's exclusion from the ACE workflow, and `reports/AI_HANDOFF_CURRENT.md` as the canonical, disciplined Claude->ChatGPT handoff (`docs/PROJECT_CONSTITUTION.md` s11, `CLAUDE.md`, and the handoff file's own "Task handoff log" template). Inspection before this entry confirmed those four were already in place, unedited. Two rules genuinely had no permanent home anywhere in the repository: (a) an explicit ACE interaction/response mode governing ChatGPT's own default behaviour (execution/audit-first, not generic explanation, unless the owner asks for one) - `ADR-0056` addressed roles and responsibilities, not response style; (b) a mandatory session-start audit checklist (branch, HEAD, working tree, relevant spec/ADR, handoff index, last approved decision, unresolved questions) stated as a rule binding **both** AI collaborators - `CLAUDE.md`'s "Before modifying anything" section already covered similar ground for Claude's own tooling behaviour, but `CLAUDE.md` is explicitly "operationalizes... for tooling" (its own header) and is not something ChatGPT reads as its own operating procedure. `specs/CLAUDE_WORKFLOW.md` (`ADR-0016`/`ADR-0051`, `ACCEPTED`) is the ratified, shared agent-workflow specification governing procedural *how/when* for both collaborators - the correct, smallest, already-existing home for these two rules, distinct from `docs/PROJECT_CONSTITUTION.md` s11's *who* content, which this entry does not reopen.
- **Decision:**
  1. **ACE interaction mode**, added to `specs/CLAUDE_WORKFLOW.md`: ChatGPT's default ACE response mode is execution/audit first - an audit request results in an audit, a review request in a review, "what should Claude do" in the exact instruction; lengthy generic explanation is given only when the owner explicitly asks for it; existing Git/handoff evidence is used directly rather than requiring the owner to manually relay Claude's output; a genuine capability/permission blocker is stated briefly with the exact next action, not substituted with explanation.
  2. **Mandatory session-start audit**, added to `specs/CLAUDE_WORKFLOW.md`: before any significant ACE audit, review, or implementation task, establish current branch, current HEAD SHA, working-tree state, the relevant specification/ADR, `reports/AI_HANDOFF_CURRENT.md`, the last approved decision, and unresolved questions bearing on the task - never infer approval from a prior session's conclusion or a stale handoff snapshot.
  3. Items already permanently encoded by `ADR-0056` (Claude as sole builder/executor; ChatGPT as independent auditor with PASS/HOLD/FAIL authority and exact-next-action obligation; Codex's exclusion; `reports/AI_HANDOFF_CURRENT.md` as the canonical, non-competing handoff with its INDEX-ONLY status preserved) are **not re-encoded or restated in substance by this entry** - `specs/CLAUDE_WORKFLOW.md`'s new section cross-references `docs/PROJECT_CONSTITUTION.md` s11 for the role model rather than duplicating it, so the two documents do not drift against each other over time.
  4. No new file is created. No competing workflow document is introduced. `docs/PROJECT_CONSTITUTION.md` s11 (`ADR-0056`) and `CLAUDE.md`'s "Your role here" are **not reopened** by this entry - only `specs/CLAUDE_WORKFLOW.md` gains the two missing sections, and `reports/AI_HANDOFF_CURRENT.md` gains this task's own "Task handoff log" entry, applying the discipline `ADR-0056` already established to itself.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file is touched by this entry - confirmed by diffing the changed-file list before committing. `specs/CLAUDE_WORKFLOW.md`'s original six-step per-tier workflow and its "two AI systems agreeing is not evidence" line are unedited; only two new sections and the version/change-history footer are added, matching the same amend-in-place-cite-the-decision pattern `ADR-0056`, `ADR-0042`'s hierarchy ratification, and the earlier G7 repair already use. No prior ADR entry is edited. `main` is untouched; this entry's commit lands on `phase-g-governance`. No certification gate is weakened, narrowed, or bypassed - none is touched.
- **Evidence:** Owner-relayed CEO audit result, 2026-08-18, verbatim title "ACE CEO AUDIT RESULT: HOLD," specifying the six required permanent rules and the explicit "do not create a new competing AI workflow; use the existing specs/CLAUDE_WORKFLOW.md / CLAUDE.md / reports/AI_HANDOFF_CURRENT.md / ADR governance" instruction. Pre-change inspection confirmed `ADR-0056`, `CLAUDE.md`, and `reports/AI_HANDOFF_CURRENT.md`'s existing content against the six required rules before deciding what was genuinely missing, rather than assuming the audit's premise. Post-change verification: `python -m pytest -q`; `scripts/check_adr_numbering.py`; `scripts/check_retired_identifiers.py`; `scripts/check_identifier_families.py`; `scripts/check_artifact_drift.py`; `git diff --check` - exact results cited in this entry's commit message.

---

## ADR-0058 - Execution continuity rule: do not stop prematurely on authorized ACE work

- **Date:** 2026-08-19
- **Status:** **ACCEPTED**, on the owner's explicit, self-contained instruction: "ACE EXECUTION - PERSIST EXECUTION CONTINUITY GOVERNANCE," given directly in this session, specifying the five terminal stop conditions and the "convert 'you should do X' into the next executable instruction" rule verbatim. **Commit confirmed:** the owner committed this entry and its accompanying `specs/CLAUDE_WORKFLOW.md`/`reports/AI_HANDOFF_CURRENT.md` edits directly, commit `20a9589e3d567bbf86e36b13bf2d61ca734e728e` ("Formalize ACE execution continuity rule"), confirmed present at `HEAD` during the session-start audit of the following task ("ACE EXECUTION CONTINUITY - PANCHANGA PRODUCTION-CERTIFICATION CHECKPOINT", 2026-08-19). The "recorded but not committed pending authorization" language originally here (and in `reports/AI_HANDOFF_CURRENT.md`'s matching entry) described the state at drafting time and is corrected by this mechanical status update only - Decision/Context/Evidence below are unedited.
- **Context:** `ADR-0056` (four-role model) and `ADR-0057` (ACE interaction mode; mandatory session-start audit) formalized *who* does what and *when* to check state, but neither addressed a related, distinct failure mode: an AI collaborator stopping mid-task to offer analysis, a recommendation, or a menu of possible next steps when the authorized workflow could instead simply continue. The owner's instruction names this precisely and gives five exhaustive conditions under which stopping is actually correct, plus the explicit prohibition on ending with "you should do X" when X is directly executable instead.
- **Decision:**
  1. `specs/CLAUDE_WORKFLOW.md` (1.2.0 -> 1.3.0) gains a new "Execution continuity (do not stop prematurely)" section, placed after "Session-start audit (mandatory)" (`ADR-0057`) and before "Change history" - the same document, for the same reason `ADR-0057` chose it: procedural *how/when*, not the *who* (`docs/PROJECT_CONSTITUTION.md` s11 stays untouched).
  2. The five terminal stop conditions, verbatim in substance: **USER INPUT REQUIRED** (a genuine decision/approval/credential/file/output only the user can supply); **CLAUDE INPUT REQUIRED** (ChatGPT cannot itself execute the next step - issue Claude the complete next instruction: context, objective, constraints, required checks, expected output, handoff-update requirement; if the step is already obvious from governance and the current milestone, issue it without first asking "what next?"); **BLOCKED** (a genuine external/environmental limitation - state the precise blocker and exact unblock action once, not repeatedly); **CEO APPROVAL REQUIRED** (an existing governance/certification checkpoint under `docs/PROJECT_CONSTITUTION.md` s11 rule (a) or `.claude/rules/*.md`); **TASK COMPLETE** (authorized work and its required verification actually finished).
  3. Outside those five, do not stop: no ending on "you should do X" when X is directly executable; no re-asking confirmation for an already-authorized routine step; no re-explaining completed work absent an actual contradiction to resolve.
  4. **Explicit non-override, stated in the new section itself:** this rule governs response *behaviour*, not authorization. It does not authorize any work repository governance has not already authorized, and it does not weaken `docs/PROJECT_CONSTITUTION.md` s11 rule (a) - the owner still ratifies all decisions, and condition 4 (CEO approval required) is not overridden by the general "keep going" instruction. A continuity rule that could be read as license to skip an approval checkpoint would itself be a governance weakening, which this decision does not make.
- **Consequences:** No calculation-engine, certification-artifact, locked Tier-0, or product-domain file is touched by this entry - confirmed by diffing the changed-file list before any commit. No certification gate, threshold, or existing evidence is altered. `docs/PROJECT_CONSTITUTION.md` s11 and `ADR-0056`/`ADR-0057` are not reopened. `reports/AI_HANDOFF_CURRENT.md` gains this task's own "Task handoff log" entry recording the change and its provenance, per the same discipline `ADR-0056` established. **Commit now confirmed** (see Status line above, `20a9589e3d567bbf86e36b13bf2d61ca734e728e`) - the commit-authorization condition this paragraph originally described as pending is satisfied.
- **Evidence:** Owner instruction, 2026-08-19, verbatim title "ACE EXECUTION - PERSIST EXECUTION CONTINUITY GOVERNANCE," specifying the five conditions, the token-efficiency rule, and the explicit "do not commit or push unless explicitly authorized" constraint. Pre-change inspection: branch `phase-g-governance`, HEAD `300e6267a2738b160e140e502a8765ec1711935a`, working tree clean of tracked changes, `scripts/check_adr_numbering.py` confirmed next free number `ADR-0058` before this entry was drafted.

---

## ADR-0059 - CEO-approved PANCHANGA_V1 external-oracle gate (Gate F): implemented and CI-confirmed

- **Date:** 2026-08-19
- **Status:** **ACCEPTED**, on the owner's explicit CEO-relayed instruction: "ACE EXECUTION CONTINUITY -
  PANCHANGA PYJHORA EXTERNAL-ORACLE GATE... CEO DECISION: APPROVED. The CEO has explicitly approved
  Option (b): implement and CI-verify a genuine PyJHora external-oracle gate for Panchanga
  classification," given directly in this session in response to the immediately preceding
  "PANCHANGA PRODUCTION-CERTIFICATION CHECKPOINT" audit's finding (recorded in
  `reports/AI_HANDOFF_CURRENT.md`'s 2026-08-19 checkpoint entry, not a separate ADR, per that audit's
  own no-commit scope) that `PANCHANGA_V1` lacked the external-oracle gate `DP-009` s5 / `ADR-0052` /
  `Q8_CLOSURE_MATRIX.md` s4 name for panchanga's classification parts. **CI verification is explicitly
  NOT yet part of this ACCEPTED status** - see Evidence below; this entry records the CEO's decision and
  its local implementation, not a claim that CI has confirmed it.
- **Context:** The checkpoint audit offered two remedies: (a) ratify the existing independently-coded
  reference as an accepted substitution, mirroring `ADR-0054`'s explicit rise/set precedent, or (b)
  build a real PyJHora oracle gate. The CEO chose (b). `certify_d2.py`, `certify_vimshottari.py` and
  `certify_transits.py` already establish the mechanism this entry reuses: a module-level
  `try/except ImportError` around `jhora`, hard `sys.exit(3)` if unavailable, and (for the latter two)
  `drik.set_ayanamsa_mode("LAHIRI"|"KP")` to align PyJHora's ayanamsa with each certified profile before
  comparison. `jhora.panchanga.drik` was located and its `tithi(jd, place)`, `yogam(jd, place)`,
  `karana(jd, place)` functions inspected and empirically cross-checked this session (an isolated,
  throwaway venv, PyJHora 4.8.7 installed unpinned for exploration only, distinct from the hash-pinned
  `requirements-oracle.lock` CI uses) - confirmed 1-based indices identical in convention to this
  module's own `tithi_index`/`yoga_index`/`karana_index`, and confirmed empirically that `place.timezone`
  does not affect the result at a fixed UT `jd` for the values this gate uses (one arbitrary large offset
  was observed to change the result in exploratory testing; `timezone=0.0` is used deliberately and
  uniformly, not left implicit).
- **Decision:**
  1. `scripts/certify_panchanga.py` gains **Gate F, `F_external_oracle`**: a genuine comparison of
     `jhora.panchanga.drik.tithi/yogam/karana` against this module's `tithi_index`/`yoga_index`/
     `karana_index`, run across the same H1-H11 holdout Gate B uses and both certified profiles (66
     comparisons, matching Gate B's own scale), plus a genuine negative control (temporarily replacing
     the real `tithi_index` with a function guaranteed to disagree with the real oracle value, confirming
     the SAME comparison logic flags it, then restoring and re-verifying agreement) - mirroring
     `engine/tests/test_panchanga.py`'s own established negative-control pattern for the Fraction-exact
     reference. Gates A-E are **unedited in behaviour and result**.
  2. **Nakshatra is deliberately excluded from Gate F**, recorded in the gate's own
     `nakshatra_excluded_reason` field: `nakshatra_index` is a thin reuse of the already Tier-0-certified
     `nakshatra()` (proven identical in Gate D), not new code this work package introduced, and the
     checkpoint audit that authorized this gate scoped the gap to tithi/yoga/karana specifically. Adding
     a nakshatra oracle comparison was judged to silently broaden the certified claim beyond what was
     authorized, per the CEO instruction's own explicit prohibition on that.
  3. **`certify_panchanga.py` moves from the `hermetic` job's "Non-oracle certification runners" to the
     `oracle` job's runners** (`.github/workflows/ci.yml`, now nine), because its module-level PyJHora
     import is now unconditional - identical in kind to all eight existing oracle certifiers, not a new
     CI mechanism. This was a deliberate design choice, not the only possible one: `scripts/
     check_artifact_drift.py` compares exactly one committed artifact per file against whatever
     regenerated it, with no per-job exception for "oracle executed" vs "not executed"; running Gate F
     conditionally in two CI jobs would make the canonical artifact legitimately differ by job, which is
     exactly the calculated-content drift `.claude/rules/certification.md` forbids adding to the
     volatile-fields list without its own separate decision. Refusing to certify at all without PyJHora
     (the unconditional import guard) satisfies the CEO instruction's "the final production certification
     must not claim an external-oracle gate unless it has actually executed" as strongly as possible:
     there is no degraded/faked PASS state, only PASS-with-Gate-F-executed or an immediate FAIL at
     import. `validate_panchanga_holdout.py` (Gate E) needs no PyJHora and **stays** in the `hermetic`
     job's independent-holdout-validator list, unchanged.
  4. `certification/PANCHANGA_V1_certification.json` (and its `reports/certification/panchanga.*`
     companions) are regenerated to reflect Gate F - **this session, locally, via the unpinned
     exploration venv described in Context**, genuinely executing PyJHora, not backfilled or faked: 66
     comparisons, 0 mismatches, negative control verified. This is explicitly **not** the hash-pinned CI
     oracle-environment evidence `RISE_SET_V1`/`ADR-0054`-class entries use as their canonical source -
     see Evidence below for exactly what is and is not yet confirmed.
- **Consequences:** No calculation logic in `engine/astrology/panchanga.py` or `panchanga_names.py` is
  touched by this entry - `tithi_index`/`yoga_index`/`karana_index`/`nakshatra_index`/`vara` are
  unchanged; Gate F only adds an external comparison against them. Gates A-E's own evidence is unchanged
  (confirmed identical in this session's regenerated artifact). `python -m pytest -q` (778 passed) and
  `validate_panchanga_holdout.py` (24 cases, 90 comparisons, 0 mismatches) both re-run unaffected, since
  neither imports `jhora`. **CI now confirmed:** committed `4177d6108236e64d07f6b23499307001f0d7c421`,
  pushed, CI run `32242462766` green on all four jobs; the `oracle` job's own execution of
  `certify_panchanga.py` (ninth runner) printed `F_external_oracle` with 66 comparisons, 0 mismatches,
  negative control verified, under the hash-pinned environment (`PyJHora 4.8.7`, identity-verified
  against `requirements-oracle.lock`); the drift-assertion step passed (43 evidence files identical
  outside volatile fields). The canonical `certification/PANCHANGA_V1_certification.json` and its
  `reports/certification/panchanga.*` companions were subsequently overlaid with the CI-sourced versions
  (differing from this entry's original local-venv-sourced commit only in the volatile
  `environment.python` field), matching the `ADR-0053`/`ADR-0054` precedent of preferring CI-sourced
  canonical evidence. The prior checkpoint's open item (`reports/AI_HANDOFF_CURRENT.md`'s 2026-08-19
  checkpoint entry) is now resolved **with CI evidence**, the same evidence class `RISE_SET_V1`/
  `current_engine`/the varga oracle
  certifiers already rely on for their own committed claims.
- **Evidence:** Owner/CEO instruction, 2026-08-19, verbatim title "ACE EXECUTION CONTINUITY - PANCHANGA
  PYJHORA EXTERNAL-ORACLE GATE," "CEO DECISION: APPROVED... Option (b)." Session-start audit: branch
  `phase-g-governance`, HEAD `20a9589e3d567bbf86e36b13bf2d61ca734e728e`, working tree carrying only the
  prior checkpoint's two documentation edits before this task began. `scripts/certify_d2.py`,
  `scripts/certify_vimshottari.py`, `scripts/certify_transits.py` (existing oracle-gate mechanism,
  inspected before reuse); `jhora.panchanga.drik` (module located, functions inspected and empirically
  cross-checked, 66/66 comparisons agreeing with this session's own probe run, in an isolated,
  throwaway, unpinned venv distinct from `requirements-oracle.lock`). `python -m pytest -q` - 778 passed,
  0 failed. `python validate_panchanga_holdout.py` - PASS, 24 cases, 90 comparisons. `python
  scripts/certify_panchanga.py` in the main (no-PyJHora) environment - correctly `exit(3)`, matching
  every other oracle-tier certifier's behaviour without PyJHora. `python scripts/certify_panchanga.py`
  via the isolated exploration venv - PASS, all gates including `F_external_oracle` (66 comparisons, 0
  mismatches, negative control verified); regenerated `certification/PANCHANGA_V1_certification.json`
  and its report/console companions. `scripts/check_adr_numbering.py` - PASS, 58 -> 59 entries.
  `scripts/check_retired_identifiers.py`, `scripts/check_identifier_families.py` - PASS.
  `git diff --check` - clean (CRLF-normalization warnings only). **CI run `32242462766`**
  (commit `4177d6108236e64d07f6b23499307001f0d7c421`,
  `https://github.com/prashantkumar0207/astro-convergence-engine/actions/runs/32242462766`) - all four
  jobs green: governance (10s), no-oracle 3.11 (2m14s, `certify_panchanga.py` correctly absent,
  `validate_panchanga_holdout.py` PASS), no-oracle 3.12 (2m41s, same shape), oracle (52s, environment
  identity verified - python 3.11, PyJHora 4.8.7, 35 packages matching the lock, 3 ephemeris assets
  matching checksums - `certify_panchanga.py` ran ninth and last, `F_external_oracle` genuinely executed
  with 66 comparisons/0 mismatches/negative control verified, drift-assertion PASS on 43 evidence files).
  Directly observed via `gh run view`/`gh run download`, not inferred.

### Evidence addendum to ADR-0059 - owner acceptance of the Panchanga per-capability FOUNDATION checkpoint (2026-08-19)

- **Status:** ACCEPTED. The owner, in direct reply to this session's "ACE - FOUNDATION CHECKPOINT AUDIT"
  (recorded in `reports/AI_HANDOFF_CURRENT.md`'s 2026-08-19 "FOUNDATION checkpoint audit" entry),
  instructed: "Use the existing governance mechanism to record this narrow checkpoint acceptance as an
  ADR-0059 addendum, refresh reports/AI_HANDOFF_CURRENT.md, run the required governance checks, and
  commit it if the repository workflow permits." This instruction is itself the act of ratification per
  `docs/PROJECT_CONSTITUTION.md` s11 - this entry records it, matching the precedent already used for
  `ADR-0052`'s "APPROVE DP-009 OPTION B" and `ADR-0055`'s "authorized."
- **Decision:** `docs/Q8_CLOSURE_MATRIX.md` s4's "CEO approval: Entry, per-capability checkpoint, exit"
  requirement is now **satisfied for Panchanga classification** (tithi, nakshatra-reuse, yoga, karana,
  vara at a given instant), on the strength of the evidence `ADR-0059`'s own body already presents (six
  gates, a genuine PyJHora external-oracle Gate F, CI-confirmed green under the hash-pinned oracle
  environment, run `32242462766`) and this session's independent re-verification (the FOUNDATION
  checkpoint audit above) that none of that evidence has since regressed.
- **Scope - explicitly bounded:** this addendum accepts only the classification-only capability
  `ADR-0055` authorized. It does **not** extend to: element start/end transition timing (`ADR-0055` item
  3); Rahu Kalam, Yamaganda, Gulika (`ADR-0055` item 2, still pending a `DP-NNN` variant-table paper);
  H-01, H-02; or any later phase. It does not by itself close FOUNDATION's own phase-exit criteria,
  which additionally require those still-outstanding capabilities per `Q8_CLOSURE_MATRIX.md` s4's exit
  row.
- **Evidence:** this session's "ACE - FOUNDATION CHECKPOINT AUDIT" task and its
  `reports/AI_HANDOFF_CURRENT.md` 2026-08-19 findings; the owner instruction quoted above; `ADR-0059`'s
  own Evidence section (CI run `32242462766`).

---

## ADR-0060 - Owner ratification of DP-011: Rahu Kalam/Yamaganda/Gulika as named, profile-selectable variants; PyJHora convention transcribed and frozen as the seed variant

- **Date:** 2026-08-20
- **Status:** **ACCEPTED**, on the owner's explicit instruction: "CEO DECISION - DP-011. RATIFIED: OPTION
  C, SEEDED BY OPTION B. Adopt multiple named, profile-selectable Rahu Kalam / Yamaganda / Gulika
  variants as the architectural model. For the initial certified variant, use the PyJHora convention as
  the seed/default variant, but only after" the seven numbered conditions quoted verbatim in Decision
  below. Per `docs/PROJECT_CONSTITUTION.md` s11, this instruction is the ratifying act; this entry
  records it, matching the precedent already used for `ADR-0052`/`ADR-0055`/`ADR-0059`.
- **Context:** `docs/decisions/DP-011-rahu-kalam-yamaganda-gulika-variant-tables.md` presented four
  options and recommended Option C (named, profile-selectable variants) seeded by Option B (adopt
  PyJHora's own convention as the first variant, since this repository already treats PyJHora as its
  designated Panchanga oracle, `ADR-0059`), explicitly not yet backed by any inspection of PyJHora's
  actual source. This entry closes that gap: PyJHora 4.8.7 was installed in an isolated, throwaway,
  unpinned exploration venv (distinct from the hash-pinned `requirements-oracle.lock` CI uses, same
  discipline `ADR-0059`'s own implementation entry used), and its
  `jhora/panchanga/drik.py` source was read directly (not executed blind, not guessed) to locate and
  transcribe the governing function.
- **Decision - the owner's seven conditions, and how each is satisfied by this entry:**
  1. **"the exact PyJHora convention/table is independently inspected"** - done. Function `trikalam(jd,
     place, option)` in `jhora/panchanga/drik.py` (PyJHora 4.8.7), lines ~1433-1464, governs all three
     periods via one shared implementation. Verbatim transcription of the offset table (the only
     tradition-specific content):
     ```
     # value in each array is for given weekday (0 = sunday, etc.)
     offsets = { 'raahu kaalam': [0.875, 0.125, 0.75, 0.5, 0.625, 0.375, 0.25],
                 'gulikai':      [0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0.0],
                 'yamagandam':   [0.5, 0.375, 0.25, 0.125, 0.0, 0.75, 0.625] }
     start_time = srise + day_dur * offsets[option][weekday]
     end_time = start_time + 0.125 * day_dur
     ```
     where `srise = sunrise(jd, place)[0]`, `day_dur = day_length(jd, place)` (`sunset - sunrise`, both
     in **local decimal hours**, not Julian Day), and `weekday = vaara(jd, place)` (0=Sunday..6=Saturday,
     PyJHora's default `show_vedic_day=True` - sunrise-to-sunrise Vedic weekday, computed by
     `vedic_weekday()`: civil weekday of `jd`, rolled back by one if `jd`'s own local clock hour is
     before that same day's sunrise local hour). Each period's window is always exactly 1/8 of that
     day's sunrise-to-sunset span - **day-only division; PyJHora 4.8.7's `trikalam` has no separate
     night-time branch for any of the three**, which resolves `DP-011` s2 item 2's open question for
     this specific variant: this seed variant is day-only by construction, not by omission.
  2. **"its rule/table is explicitly transcribed and frozen"** - the table above is frozen as
     `PYJHORA_TRIKALAM_V1` (Decision item 4). Any future PyJHora version that changes these seven-element
     arrays would require a new variant identity, never a silent edit to this one, per this repository's
     existing "a variant is a decision to record, never a silent choice" discipline (`DP-009`).
  3. **"provenance/source is recorded"** - PyPI package `PyJHora`, version `4.8.7` (the same version
     `ADR-0059` already cites and CI's `requirements-oracle.lock` pins), module `jhora.panchanga.drik`,
     function `trikalam` (and its three convenience lambdas `raahu_kaalam`/`yamaganda_kaalam`/
     `gulikai_kaalam`). Inspected via direct source read of the installed package file, not via
     documentation, a webpage, or memory of the convention.
  4. **"the variant is given an explicit identity/name"** - `PYJHORA_TRIKALAM_V1`.
  5. **"the implementation is isolated from other variants"** - satisfied by construction: exactly one
     variant exists after this entry; the implementation (see Consequences) keys all tables by variant
     identity from the start, so a second variant is additive, not a rewrite.
  6. **"the required tests, boundary cases, negative control, independent validation and certification
     evidence are defined"** - addressed by the implementation this entry authorizes (see Consequences);
     this entry alone does not constitute that evidence, per the owner's own "does NOT automatically
     certify the resulting implementation."
  7. **"any uncertainty or ambiguity in the PyJHora convention is explicitly recorded rather than
     guessed"** - two genuine representational differences are recorded, not silently resolved:
     (a) PyJHora expresses `sunrise`/`sunset`/the resulting windows in **local decimal hours** (subject
     to its `place.timezone` field); this repository's own `rise_set.sunrise`/`sunset` return **Julian
     Day, UT**. The frozen rule transcribed above is the *proportional offset arithmetic*
     (`start = sunrise + offset * day_length`; `duration = day_length / 8`), which is representation-
     independent; the seed variant's implementation performs this arithmetic in JD-UT terms (consistent
     with how `vara`, `ADR-0055` item 4, already consumes `rise_set` in JD-UT rather than reimplementing
     PyJHora's local-hour pipeline), and Gate F must convert PyJHora's local-hour output (with
     `place.timezone` fixed at `0.0`, the same convention `ADR-0059` already established) to JD-UT before
     comparing, not assume the raw numbers are already comparable. (b) PyJHora's `trikalam` computes the
     time window from **the sunrise of `jd`'s own calendar day** (via `sunrise(jd, place)` called
     directly on the query instant) but selects the **offset using `vaara`'s sunrise-anchored, possibly
     rolled-back weekday** - these two are not always the same calendar day for an instant before that
     day's sunrise. This is PyJHora's actual behaviour, not a defect this entry is correcting; the seed
     variant's implementation must mirror it exactly (today's-calendar-day sunrise/sunset for the
     window, `panchanga.vara`'s already-certified rolled-back weekday for the offset lookup) rather than
     "improving" it into a more internally-consistent rule PyJHora itself does not implement.
- **Consequences:** This entry authorizes **only** the variant-definition and certification work for
  `PYJHORA_TRIKALAM_V1` - a new `engine.astrology.trikalam` module (Rahu Kalam, Yamaganda, Gulika
  window computation, consuming certified `rise_set.sunrise`/`sunset` and `panchanga.vara`, never
  reimplementing either), its tests, a certifier following the established template (frozen-rule
  integrity, dense sweep, boundary/circumpolar battery, non-invasiveness, independent validator, and a
  genuine Gate F re-comparing against live PyJHora - the same discipline `ADR-0059` established), an
  independent validator, and CI wiring. It does **not** by itself certify that implementation - certified
  status requires the gates to actually run and pass, CI-confirmed, exactly as `ADR-0059` required for
  Panchanga. It does **not** authorize: a second or later variant (explicitly reserved, per the owner's
  "do not implement additional variants unless separately authorized"); any Muhurta-specific consumption
  of these periods (search, ranking, or otherwise); or any change to `panchanga.py`, `rise_set.py`, or
  any already-certified module. System/profile provenance (which variant identity produced a given
  result) must be carried in the result type, not left implicit.
- **Evidence:** `docs/decisions/DP-011-rahu-kalam-yamaganda-gulika-variant-tables.md`; the owner's
  "CEO DECISION - DP-011" instruction, quoted above; direct inspection of `jhora/panchanga/drik.py`
  (PyJHora 4.8.7, installed via `pip install PyJHora` into an isolated venv at
  `dp011_explore_venv`, not the main environment or CI's hash-pinned lock).

---

## ADR template (copy, do not edit above the line)

## ADR-XXXX - <title>
- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-YYYY
- **Context:** <forces, constraints, problem>
- **Decision:** <the binding choice, stated imperatively>
- **Consequences:** <positive, negative, follow-up obligations>
- **Evidence:** <links to validation runs where applicable>
