<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACTIVE REGISTER. Twenty-five questions. **Owner ratifications of 2026-08-13: Q13 resolved; Q1 and Q8 ratified in part (ADR-0033); ADR-0005 ratified, making Tier-0 FORMALLY LOCKED (ADR-0034); ADR-0009/0010/0011 ratified, making the registry vargas owner-ratified CERTIFIED but NOT Locked (ADR-0035); ADR-0012 ratified, closing the varga sign-convention asymmetry (ADR-0036).** **Eleven fully open** (Q2, Q3, Q4, Q5, Q7, Q10, Q12, Q22, Q23, Q24, Q25), **six with candidate resolutions awaiting a ratification decision** (Q6, Q9, Q11, Q14, Q15, Q16), two ratified in part (Q1, Q8), one resolved (Q13). **Nineteen** register entries are now Accepted; ratification is per-entry and the rest are not. |
| Version | 2.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-14 |
| Review cadence | TBD |

# Open Questions Register

Ambiguities are decided by the owner, never by silent assumption. Each question blocks the
artifacts listed against it. Resolution = decision log entry + this register updated.

| ID | Question | Why it matters | Blocks | Status |
|---|---|---|---|---|
| Q1 | Who are the named owners/maintainers (docs owner, engine owner, release owner)? | Accountability for a 10+ year artifact | All status headers | **RATIFIED IN PART, 2026-08-13** (ADR-0033 D1). Project Owner: Prashant Kumar. Builder: Claude. Independent auditor: ChatGPT. **STILL OPEN:** the docs owner, engine owner and release owner were not designated and are not invented. |
| Q2 | Branch/review model (trunk-based vs GitFlow; required reviewers; protection rules)? | Merge discipline | CONTRIBUTING.md | OPEN |
| Q3 | Versioning and release policy (repo-wide semver vs per-component; tagging; changelog scope)? | Long-term compatibility management | CHANGELOG.md, engine releases | OPEN |
| Q4 | Authoritative expansion, scope and mutual boundary of **HLKG** and **AKG**? | Two specification skeletons cannot be filled without inventing meaning | HLKG_SPEC.md, AKG_SPEC.md, knowledge/ layout | OPEN |
| Q5 | One-paragraph ratified project mission (what the system is and is not)? | Anchors MASTER_ARCHITECTURE section 1 | MASTER_ARCHITECTURE.md | OPEN |
| Q6 | May `engine/` ever read `knowledge/` at runtime, or is knowledge strictly an app-layer concern? | Hard dependency rule | MASTER_ARCHITECTURE.md section 4 | **RESOLVED PENDING RATIFICATION** (ADR-0024) |
| Q7 | Repository license, given upstream dual-licensed dependencies (e.g. AGPL-3.0 Swiss Ephemeris) and possible commercial deployment? | Legal viability of the whole repo | LICENSE (intentionally absent until decided) | OPEN |
| Q8 | Ratified roadmap phases with entry/exit criteria? | Prevents narrative-driven "done" | PROJECT_ROADMAP.md | **OWNER-RATIFIED DIRECTION, 2026-08-13; FULL RESOLUTION STILL OPEN** (ADR-0033 D3). The dependency ordering is ratified. Per-phase criteria are not. |
| Q9 | Should the existing certified calculation kernel (astro_kernel v1.3, Tier-0 portably certified) be imported into `engine/` as-is as the first component, and under what module name? | Avoids re-implementation; preserves certification lineage | engine/ population | **RESOLVED PENDING RATIFICATION** (ADR-0025) |
| Q10 | CI provider and mandatory pipeline stages (validation standard is CI-ready but no provider is chosen)? | Automation of the gates | tools/, repository settings | OPEN |
| Q11 | Should a direct value-comparison test assert that `legacy/kp.py` and `engine/kp/tables.py` hold identical Vimshottari lord and year tables? | ADR-0023 D3 permits the three-way duplication on condition it is tested rather than removed. `engine/tests/test_vimshottari_consistency.py` compares `engine/dasha/tables.py` against `engine/kp/tables.py` only. The legacy-to-engine leg is covered behaviourally by the equivalence sweep and not by direct table comparison, so a divergence introduced in one table could in principle survive until a behavioural case happened to exercise it. | Completeness of the ADR-0023 D3 condition | **RESOLVED PENDING RATIFICATION, 2026-08-13** (ADR-0037 D3). `engine/tests/test_vimshottari_table_identity.py`: all three pairs compared directly, no cross-import, 7 perturbation controls, plus comparison against an independently transcribed classical sequence. |
| Q12 | Is `LOCK_MANIFEST.json` a live register that must be kept current, or frozen historical evidence of the Tier-0 lock? | It records `tier1_kp_significator` as SPECIFICATION_PENDING and describes a tier structure that later work did not follow. If it is live it is stale and misleading; if it is frozen evidence it must say so, because a reader cannot currently tell which, and editing frozen certification evidence would be a governance violation while leaving a live register stale would be a documentation defect. ADR-0027 D5 declined to edit it for exactly this reason. | LOCK_MANIFEST.json, certification status reporting | OPEN, raised 2026-08-11. **New evidence 2026-08-13** (ADR-0034 consequences): `certification/CURRENT_ENGINE_LOCK.json` states that `LOCK_MANIFEST.json` describes the LEGACY kernel exclusively and is deliberately left untouched, per audit finding F-17. That narrows the question but does not answer what the file is FOR or whether it is live; it stays OPEN and unedited. |
| Q13 | Were ADR-0001 and ADR-0002, both dated 2026-07-11 and both carrying `Status: Accepted`, ratified by the owner, or were they marked Accepted by the authoring agent before the register adopted its current status vocabulary? | They are the only two entries in the register claiming Accepted status, and they fix the canonical top-level folder set that ADR-0003 then reconciled against. If they were owner acts, they bind and ADR-0003 needs owner supersession. If they were not, the register contains two entries claiming an authority no one exercised, which is the exact failure mode ADR-0022 exists to prevent. The repository evidences neither reading, and both retroactively demoting them and retroactively confirming them would falsify the record. | Precedence of ADR-0001/0002 over ADR-0003; integrity of the Accepted status | **RESOLVED, 2026-08-13** (ADR-0033 D2). The owner ratified both entries as written, prospectively. The historical question of what the 2026-07-11 status meant is deliberately left unanswered and unneeded. |
| Q14 | Should the ADR numbering gate in `.github/workflows/ci.yml` carry a committed negative control, as the identifier gate does? | The identifier gate plants a retired identifier on every CI run and fails the build if the gate does not catch it, so its PASS is evidence. The numbering gate has no such control, so a PASS proves only that the gate ran, not that it can still fail. ADR-0029 corrected a real numbering defect and the gate now passes; without a negative control there is nothing to detect the gate silently breaking later, which is exactly the circularity the project charter section 11 warns against. | Evidential value of the governance job's numbering step | **RESOLVED PENDING RATIFICATION, 2026-08-13** (ADR-0037 D3). Check extracted to `scripts/check_adr_numbering.py` so gate and control run the same code; CI control plants a duplicate and an out-of-order entry; 15 committed tests. |
| Q15 | Should `certification/current_engine_certification.json` be made byte-reproducible by recording the swetest invocation without the run's temporary directory and the checkout's absolute path? | Two runs of identical code over identical data currently produce different bytes, because each case records `swetest_cmd` containing `/tmp/swetest_<random>/` and the absolute checkout path. Root D-005 removed exactly this class of environment-specific absolute-path dependency from the legacy Tier-0 package, and it has reappeared here. It does not affect Constitution s12 condition 3, since both evidence files regenerate together and agree, but it means the artifact cannot be diffed across runs to show that nothing changed. | Byte-level reproducibility claims about Tier-0 evidence | **RESOLVED PENDING RATIFICATION, 2026-08-13** (ADR-0037 D3). Recorded command normalised to `<bundled>/swetest` and `-edir<repo-root>`; two consecutive runs now differ only in `run.executed_utc`; every number identical to the pre-change artifact. |
| Q16 | Should `scripts/certify_current_engine.py` call `certification_support.preflight()`, as the other certifiers do? | It verifies the swetest binary version at runtime but does NOT verify the ephemeris checksums against `CHECKSUMS.sha256`, and no anti-fitting scan forms part of this gate. That is VALIDATION_STANDARD s2 rules 4 and 6. The legacy Tier-0 runner did verify ephemeris checksums per root D-005, so this is a capability the current runner lost. Wiring it changes what the gate can reject, which is a scope decision rather than a repair. | VALIDATION_STANDARD s2 rules 4 and 6 for Tier-0 | **RESOLVED PENDING RATIFICATION** (ADR-0032). Implemented: preflight wired, coverage asserted, three committed negative controls. |
| Q17 | Does `PROJECT_CONSTITUTION.md` s12 condition 4 require a **ratified** decision entry, or merely that an entry exists? | ADR-0033 D4 had to decide this in order to evaluate Tier-0's status, and adopted the ratified reading. The textual reading, that an entry merely records the lock, would let the builder satisfy all four Locked conditions with no human act at all, since conditions 1, 2 and 3 are machine-verifiable. That would make the constitution's strongest status its easiest to claim. The reading adopted is therefore the stricter one, but it is a builder interpretation of the owner's constitution and should be confirmed or corrected rather than left as precedent by default. | Governs every FUTURE lock. **No longer blocks Tier-0**: ADR-0005 was ratified on 2026-08-13, so condition 4 is met under either reading (ADR-0034). | **RESOLVED, 2026-08-14 (ADR-0039).** Condition 4 requires an owner-ratified decision entry; mere existence is insufficient. |
| Q18 | When a ratified decision entry contains lock language of its own, does that make its subject a Constitution s12 Locked artifact? | ADR-0012 decision (b) says of the sign conventions "Both are locked", and it is now ratified. Conditions 1, 2 and 3 are met for them. ADR-0036 D3 declined to declare s12 Locked status for two independent reasons: no lock authorisation was given, and ADR-0012 records no version, which condition 4 requires. ADR-0012 is unlikely to be the only ratified entry containing lock language, so the rule should be decided once rather than case by case. | Whether s12 Locked status can arise from ratification alone, and how many artifacts currently hold it | **RESOLVED, 2026-08-14 (ADR-0039).** Lock language does not itself create s12 Locked status; formal s12 conditions and explicit lock authorisation remain required. |
| Q19 | The `DP-NNN` decision-paper family is in use (`docs/decisions/DP-008`, `DP-009`, `README.md`) but is not declared in `docs/NAMING_STANDARD.md` s2's ID-Families table, has no decision-log entry and has no uniqueness check. Should it be registered, renamed into the `ADR-` family, or retired? | `NAMING_STANDARD.md` requires a governing section, a decision-log entry and a uniqueness check **before first use**. None of the three exists and the family is already in use. This is the identical defect class ADR-0004 retired, recreated on 2026-08-11, and it passes CI only because the identifier gate's family regex matches `ADR-` tokens alone. ADR-0014 D5's claim that the family regex catches "the eleventh invention" is therefore false about the repository's actual exposure. | Integrity of the identifier-family rule; whether the gate can be extended to enforce family declaration at all | **RESOLVED, 2026-08-14 (ADR-0040).** Registered as `DP-\d{3}`, issued by `docs/decisions/README.md`, with a standing tracked-file gate and duplicate-allocation control. |
| Q20 | `.github/` is a tracked top-level folder holding the entire CI apparatus, and it appears in no ADR's declared top-level set. Should a superseding entry declare it? | **Ratified** ADR-0001 fixes the set with the word "exactly" and requires a superseding ADR for any addition; ADR-0003 repeats it. So the repository is currently in violation of a ratified decision. ADR-0028's consistency audit additionally asserted the tree matches ADR-0003's consequences "exactly", which it does not: those consequences also omit `schemas/`, which exists. | Conformance with ratified ADR-0001; accuracy of ADR-0028's audit row | **RESOLVED, 2026-08-14 (ADR-0041).** ADR-0001's top-level list is superseded by the explicit current canonical set, including `.github/` and `schemas/` and excluding `app/` and top-level `tests/`. |
| Q21 | ADR-0023 asserts that `engineering/ENGINEERING_CONSTITUTION.md` Principle 3 and `docs/KNOWLEDGE_STANDARDS.md` "are narrowed", while changing neither. Does an ADR outrank the engineering constitution, and if so should the narrowing be written into those documents? | Both files contain **zero** references to ADR-0023 or to any ADR; the unqualified prohibition still stands in both, so a reader of either cannot discover the narrowing. And `engineering/ENGINEERING_CONSTITUTION.md` is **not placed anywhere** in ADR-0022's hierarchy, which names "PROJECT CONSTITUTION", so it is not established that an ADR can narrow it. A fourth document, `docs/ARCHITECTURE.md`, states the same prohibition and is covered by no narrowing at all. ADR-0023 is itself PROPOSED. | Whether the certified rule tables comply with the governing standards; C-01, C-02, C-05 | **RESOLVED, 2026-08-14 (ADR-0042).** ADRs do not silently narrow higher-level constitutions or standards; the four-part executable normative rule-data exception is now written into the governing documents. |
| Q22 | The evidence-agreement gate compares each report against the same `certification_support._render` that produced it. Should an independent check exist? | It proves `report == _render(artifact)`, which is real and catches hand-editing and stale regeneration. It cannot detect a defect **inside** `_render`, where both evidence files would agree on a wrong number. Under the charter's anti-circularity rule this is the analogue of Q14 for that gate. | Evidential strength of Constitution s12 condition 3 | OPEN, raised 2026-08-13. Audit L-12. Closing it needs new verification design, not remediation. |
| Q23 | Should `requirements.lock` be hash-pinned, and should `pip` itself be pinned? | Only `requirements-oracle.lock` carries hashes and is installed with `--require-hashes`. `requirements.lock`, used by two of the three CI jobs, is version-pinned only. All three jobs run `pip install --upgrade pip` unpinned, so even the oracle environment is lock-plus-unpinned-pip, which the spec's "one file plus a clean interpreter reproduces the oracle environment" does not describe. | Strength of the hermetic tier's integrity guarantee; accuracy of the reproducibility spec | OPEN, raised 2026-08-13. Audit L-5. Hash-pinning changes the dependency contract. |
| Q24 | Should the `swetest` reference binary and `CHECKSUMS.sha256` itself be integrity-verified? | The binary's SHA-256 is recorded in `certification/ORACLE_ENVIRONMENT.json` and **read by nothing**; what is checked is a version string, which any binary can print. `CHECKSUMS.sha256` is itself unverified, so a coordinated edit of manifest plus assets passes both mechanisms. **The D-001 numerical authority is the one asset in the gate with recorded-but-unverified integrity.** | Integrity of the independent numerical authority; ADR-0032's phrasing that a version check "proves the ORACLE is the pinned build" | OPEN, raised 2026-08-13. Audit L-7, L-6. Touches the D-001 verification path. |
| Q25 | The only remote-CI evidence in the repository attests the **two-job** workflow at `a460ba2`. No run record exists for the three-job workflow, and this batch changed the workflow again. Should a fresh remote CI run be recorded before any further ratification of ADR-0018? | ADR-0018's addendum is self-labelled `CEO_REPORTED` with `run_url`, `run_id`, `runner_image` and `pip_version` all null, which the repository commendably flags. What is not flagged is that the attested workflow file no longer exists. **The repository cannot prove CI passes at HEAD, and nothing in this batch claims it does.** | Evidential basis of ADR-0018; whether the governance job has ever run green remotely | OPEN, raised 2026-08-13. Audit NOT-DETERMINABLE section. **Only the owner can produce this evidence: it requires a run on GitHub.** |

## Status vocabulary used in this register

| Status | Meaning |
|---|---|
| OPEN | No decision exists. |
| RESOLUTION DRAFTED, PENDING RATIFICATION | A candidate answer exists in a document, it is explicitly unratified, and it does not bind. The question is still OPEN for every purpose that depends on a ratified answer. |
| RESOLVED PENDING RATIFICATION | An ADR records a decision that answers the question. The ADR itself is PROPOSED, because Q1 is open and `PROJECT_CONSTITUTION.md` section 11 reserves ratification to the owner. Nothing here is Accepted. |
| RESOLVED | An owner-ratified decision exists. **Q13 and, in part, Q1 and Q8 now hold this status; nothing else does.** |
| RATIFIED IN PART | The owner has decided some of what the question asked and explicitly left the rest undecided. The undecided part is still OPEN and is named. |

**This paragraph changed on 2026-08-13 and the change matters.** Q1 previously left the repository
with no authority that could Accept anything. The owner is now named, so ratification is possible.

**Possible is not done.** Ratification is per-entry. **Eleven** entries in `docs/DECISION_LOG.md` are
Accepted, all ratified by Prashant Kumar on 2026-08-13: **ADR-0001, ADR-0002, ADR-0005, ADR-0009,
ADR-0010, ADR-0011, ADR-0012, ADR-0033, ADR-0034, ADR-0035 and ADR-0036**.

**ADR-0003, ADR-0004, ADR-0006, ADR-0007, ADR-0008, ADR-0013, ADR-0014 and ADR-0018 through ADR-0032
all remain PROPOSED**, including every entry written to resolve the ADR-0013 conflicts, to disposition
the earlier register, to correct the numbering gate, and to repair and complete the Tier-0
certification evidence. A reader must not read "an owner exists" as "the register is ratified".

**One asymmetry produced by per-entry ratification has been closed and one remains.** Closed: the
ratified registry vargas emitted a sign convention defined by then-unratified ADR-0012, which is now
ratified (ADR-0035 D4, closed by ADR-0036 D2). Remaining: ratified ADR-0001 fixes a top-level folder
set that unratified ADR-0003 reconciled away (ADR-0033 D2). Also outstanding, though not an
asymmetry: ADR-0006, ADR-0007 and ADR-0008 are the three certified production layers still
unratified.

## Q6 resolution (ADR-0024, strengthened by ADR-0030 clause 1)

The two claims below are different in kind and are stated separately on purpose. Collapsing them is
the error the strengthening exists to prevent.

**Empirical fact, as at commit `2a4ac9f`.** `engine/` contains zero runtime imports of top-level
`knowledge/` and zero references to `knowledge/hlkg`. This is an observation of the current tree. It
could change with any commit and it binds nothing.

**Normative architectural rule, which binds.**

> **`engine/` MUST NOT have an uncontrolled runtime dependency on top-level `knowledge/`.**
> Such a dependency is PROHIBITED unless and until a future explicit architectural decision
> authorises a specific controlled interface, defining at minimum its version pinning, its schema
> validation, its failure behaviour, and its effect on certification.

ADR-0030 **withdraws** ADR-0024 D1's narrowing to "certification-critical calculation", which left
non-critical runtime dependency implicitly permitted. The prohibition is unqualified. **No
controlled interface is introduced, specified or authorised**, and none may be built on the strength
of this text.

`engine/knowledge/` is implementation-owned rule data, a different thing from top-level `knowledge/`
despite the name collision, and remains permitted under the ADR-0023 four-part test. One live
dependency is declared on the record: `engine/astrology/dignity.py` loads
`engine/knowledge/data/dignities.json` via `engine/knowledge/repository.py`, which sits outside the
current Tier-0 lock scope.

## Q9 resolution (ADR-0025, strengthened by ADR-0030 clause 2)

> (a) `engine/` **is** the production calculation foundation. It is authoritative and is not
> reimplemented for architectural aesthetics. Its Tier-0 lock lineage at `bfae088` is preserved.
>
> (b) `legacy/` **remains** a historical and equivalence reference: the KP equivalence oracle for
> ADR-0006 and the historical Tier-0 record.
>
> (c) **Retirement of `legacy/` REQUIRES an explicit future decision AND completion of the migration
> and certification requirements of `docs/LEGACY_KERNEL_MIGRATION.md`.** Both are necessary; neither
> alone is sufficient. ADR-0025 D3 stated only the migration condition and omitted the decision
> requirement; ADR-0030 supplies it.
>
> (d) **No retirement is implied, scheduled or foreshadowed by the current state.** In particular,
> the empirical finding that `legacy/` is imported by five test modules and no production module
> MUST NOT be read as evidence that retirement is close at hand or appropriate. A low dependency
> count is not a retirement criterion.

Verified rather than asserted: the five importers are test modules, and the one reference inside
`engine/kp/intervals.py` is a docstring, not an import.

## Resolution criteria for the questions raised during the governance pass

A question closes when its criterion is met **and** an owner ratifies the closing decision. Neither
alone is sufficient, for the same reason recorded in the status vocabulary above.

| ID | Resolution criterion | Who can answer |
|---|---|---|
| Q11 | A committed test asserts value-identity between the Vimshottari lord and year tables in `legacy/kp.py` and `engine/kp/tables.py`, without cross-import, and it fails when either table is perturbed. That last clause is the criterion that matters: an assertion with no demonstrated failure mode is not coverage. | Engineering, on owner authorisation. The work is a test addition, currently unauthorised. |
| Q12 | `LOCK_MANIFEST.json` carries an explicit self-description as either a live register or frozen historical evidence. If live, its tier entries are reconciled with the actual programme and a KP_CHAIN entry is added per ADR-0006. If frozen, it says so and the live status moves to `certification/ENGINE_CAPABILITY_INVENTORY.json`, which already serves that purpose. | **Owner.** The question is what the artifact is for, which is not discoverable from the repository. |
| Q13 | **MET, 2026-08-13.** The owner ratified both entries as written. They stand, and ADR-0003 accordingly requires owner supersession before either folder list is treated as settled; ADR-0033 D2 records that tension. | **Owner only.** Answered. |
| Q14 | The governance job plants an invalid ADR heading on every run and fails the build if the numbering gate does not reject it, mirroring the identifier gate's existing control. | Engineering, on owner authorisation. Adding it is a workflow change. |
| Q15 | `swetest_cmd` records the invocation without the run's temporary directory and without the checkout's absolute path, so two runs over identical data produce identical bytes. **NOT addressed in the ADR-0032 pass, by instruction.** | Engineering, on owner authorisation. |
| Q16 | RESOLVED PENDING RATIFICATION by ADR-0032: `preflight()` wired, coverage of `REQUIRED_FILES` asserted, corrupted-asset and missing-asset negative controls committed. | Done, pending ratification. |
| Q17 | The owner states whether s12 condition 4 requires a ratified decision entry or merely an existing one. Tier-0 no longer depends on the answer, since ADR-0005 is now ratified and satisfies it either way; the answer governs every future lock. | **Owner only.** It is an interpretation of the owner's own constitution. |
| Q18 | The owner states whether ratifying an entry containing lock language confers s12 Locked status, or whether a separate lock authorisation is always required. If the latter, ADR-0036 D3's refusal stands as the pattern. | **Owner only.** Same character as Q17. |

## Q8 closure criteria (ADR-0021 D2)

**Status as at 2026-08-13: OWNER-RATIFIED DIRECTION, FULL RESOLUTION STILL OPEN** (ADR-0033 D3).

The owner has ratified the dependency ordering, and the ratification carries five qualifications
that bind: the ordering is **guidance, not implementation authorisation**; existing certified
astrology foundation work remains valid historical foundation work; astrology systems remain
independently implemented and independently evaluated; convergence MUST preserve provenance,
dependency, correlation and uncertainty; and structurally different domains MUST NOT be forced
through one natal pipeline. The ratified ordering is recorded in `docs/PROJECT_ROADMAP.md` section 3.

**What is still open is the harder half.** The criteria below are unchanged and unmet: no phase has
ratified prerequisites, entry criteria, scope, certification gates, exit criteria or approval
requirements. Direction without criteria still cannot tell anyone when a phase has been entered or
finished, which is the failure mode Q8 exists to prevent.

The remainder of this section is the original text, unchanged.

ADR-0026 addresses roadmap reconciliation and drafts a resolution; it does not
close the question, and the reason is recorded in ADR-0026's consequences: the closure criteria below
require per-phase prerequisites, entry criteria, scope, certification gates, exit criteria and
approval requirements, those exist only as an unratified candidate matrix in
`docs/Q8_CLOSURE_MATRIX.md`, and closing the question on that basis would be manufacturing approval.

Q8 status is therefore **RESOLUTION DRAFTED, PENDING RATIFICATION**, which is a form of OPEN.

The original criteria follow unchanged.

ADR-0020 D6 supplies a preferred domain order (FOUNDATION, JATAKA, EVIDENCE,
INTERPRETATION, CONVERGENCE, VARSHAPHAL, MUHURTA, PRASHNA, MUNDANE) and that order is explicitly
**not** authorisation to begin implementation.

Q8 closes only when the roadmap defines, for every implementation phase: prerequisites, entry
criteria, implementation scope, certification gates, exit criteria, and CEO approval requirements.

No roadmap document in this repository authorises implementation. `docs/PROJECT_ROADMAP.md`,
`docs/VARGA_CERTIFICATION_ROADMAP.md`, `docs/DASHA_CERTIFICATION_ROADMAP.md` and
`docs/PLATFORM_DOMAIN_ARCHITECTURE.md` each state orders or sequences and each says so; this note
records it at register level so the point survives reading any one of them in isolation.

## Decision papers and design proposals drafted (2026-08-11)

Drafted on CEO direction. Each presents options; none decides. All four matters remain OPEN.

| Matter | Document | Status |
|---|---|---|
| Entity identifier family and pattern | `docs/decisions/DP-008-entity-identifier-family.md` | OPEN, options presented, recommendation labelled |
| Tier classification for panchanga and rise/set | `docs/decisions/DP-009-panchanga-riseset-tier.md` | OPEN, options presented, recommendation labelled |
| Independent evidence-path representation and computation | `docs/EVIDENCE_INDEPENDENCE_DESIGN.md` | OPEN, design proposal; convergence must not be implemented on it |
| Q8 phase criteria | `docs/Q8_CLOSURE_MATRIX.md` | **Q8 REMAINS OPEN**; candidate matrix for ratification |

`docs/decisions/README.md` indexes the paper series and records that DP-001 through DP-007 are
reserved for the Phase G governance round and are not yet drafted.

## CONSOLIDATED OWNER-DECISION BATCH, prepared 2026-08-13

Prepared on the owner's direction so that these can be decided together rather
than one interruption at a time. **Every proposal below is the builder's
recommendation and binds nothing.** Where a recommendation would create authority
the builder does not have, that is said instead of a recommendation being made.

Confidence labels: HIGH means the repository determines the answer and the
decision is essentially recording it; MEDIUM means the proposal is defensible and
alternatives are real; LOW means the owner's judgement is doing the work.

| # | Question | Proposed decision | Confidence | If deferred |
|---|---|---|---|---|
| 1 | **Q1**, remaining maintainer roles | Name a docs owner, an engine owner and a release owner, or state explicitly that the project owner holds all three for now. The second is a real answer and closes the question. | HIGH that a decision is cheap; LOW as to who | 42 document status headers keep reading `Owner: TBD`, and the status-header gate keeps passing on a placeholder |
| 2 | **Q2**, branch and review model | Adopt what is already practised: short-lived governance branches off `main`, CEO audit then owner merge by pull request, no direct pushes to `main`. That is what PR #1 did. | HIGH | `CONTRIBUTING.md` stays unwritten and the practice stays undocumented |
| 3 | **Q3**, versioning and release policy | Per-component semver, since `engine/version.py` already carries 0.3.0 independently of document versions; tag on lock events, as `v0.1.0-kernel-stable` already does. | MEDIUM | No changelog discipline; the existing tag is unexplained |
| 4 | **Q4**, HLKG and AKG scope | **No proposal offered.** This is product ontology, not engineering, and inventing a scope is exactly what the register forbids. It blocks two specification skeletons and nothing certified. | n/a | Two skeletons stay unfillable; Q21's knowledge-layer question stays partly abstract |
| 5 | **Q5**, project mission paragraph | Adopt the charter's own USP sentence, PAST BEFORE FUTURE, as the ratified mission: a deterministic, auditable, multi-method astrology evidence engine that demonstrates historical evidence before offering future-oriented analysis. | MEDIUM | `MASTER_ARCHITECTURE.md` section 1 stays unanchored |
| 6 | **Q7**, repository licence | **No proposal offered; obtain legal advice.** Swiss Ephemeris is AGPL-3.0 or commercial, and the answer determines whether commercial deployment is viable at all. The builder is not competent to decide it and neither is a confident guess. | n/a | `LICENSE` stays absent, which is the safe state, but commercial viability stays undetermined |
| 7 | **Q8**, per-phase criteria | Ratify `docs/Q8_CLOSURE_MATRIX.md` as the criteria set, or amend it. The direction is already ratified; only the criteria remain. | MEDIUM | No phase can be declared entered or exited by criteria |
| 8 | **Q10**, CI provider | Record GitHub Actions, which is already in use, and record the three jobs as the mandatory pipeline. This is recording reality. | HIGH | The pipeline exists with no decision behind it |
| 9 | **Q12**, `LOCK_MANIFEST.json` purpose | Declare it **frozen historical evidence of the legacy kernel**, which is what `CURRENT_ENGINE_LOCK.json` already says it is, and move live status reporting to `ENGINE_CAPABILITY_INVENTORY.json`, which already serves that purpose. Add one self-describing field; edit nothing else. | HIGH | A reader cannot tell whether its `SPECIFICATION_PENDING` tier entries are current |
| 10 | **Q17**, s12 condition 4 | Confirm the stricter reading: condition 4 requires a **ratified** entry. Otherwise the builder could satisfy all four Locked conditions with no human act, since 1, 2 and 3 are machine-verifiable. | HIGH | ADR-0033 D4's reading stands as unconfirmed precedent |
| 11 | **Q18**, lock language in ratified entries | Confirm that ratifying an entry containing the word "locked" does **not** by itself confer s12 Locked status, and that a separate lock authorisation is always required. This preserves the distinction Tier-0's lock relied on. | HIGH | Each future case is argued from scratch |
| 12 | **Q19**, the `DP-NNN` family | Register `DP-NNN` in `NAMING_STANDARD.md` s2 as a **non-normative decision-paper** family, explicitly outside the ADR decision family, with a uniqueness check; then extend the identifier gate to require that every family in use is declared. Renaming the two papers into the ADR family is the alternative and is worse, because they are proposals and would occupy issued ADR numbers. | MEDIUM | An unauthorised identifier family stays in use, and the gate stays structurally unable to see it |
| 13 | **Q20**, `.github/` undeclared | Issue a superseding entry declaring `.github/` sanctioned, describing it as CI and repository automation, and correct the top-level set to include `schemas/`. **The builder will not draft this unasked**: ADR-0001 is ratified and amending it is an owner act. | HIGH that it needs doing | The repository stays in violation of a ratified decision |
| 14 | **Q21**, the narrowed standards | Place `engineering/ENGINEERING_CONSTITUTION.md` explicitly in the ADR-0022 hierarchy, then either write the ADR-0023 narrowing into it, `KNOWLEDGE_STANDARDS.md` and `docs/ARCHITECTURE.md`, or reject the narrowing and require the rule tables to move. **Do not leave it as an assertion in an unratified ADR that three standards do not mention.** | MEDIUM | Certified rule tables remain in unresolved tension with three standards; C-01, C-02, C-05 stay stale |
| 15 | **Q22**, agreement-gate circularity | Authorise a schema-level or independently written second renderer for the human-readable report, so the agreement gate does not rely on the function under test. Lower priority than Q19 and Q20. | MEDIUM | Condition 3's evidence stays one function away from circular |
| 16 | **Q23**, hash-pinning | Hash-pin `requirements.lock` and pin `pip` in all three jobs, then correct the reproducibility spec's "one file plus a clean interpreter" claim. | MEDIUM | Two of three jobs install without hash verification |
| 17 | **Q24**, unverified oracle assets | Add the `swetest` binary SHA-256 to `CHECKSUMS.sha256` and verify the manifest's own digest, so the D-001 numerical authority is integrity-checked rather than version-string-checked. | HIGH that it should be done | The independent numerical authority stays the one unverified asset in the gate |
| 18 | **Q25**, remote CI evidence | Run the three-job workflow on GitHub and record the run URL, run id, runner image and pip version, superseding the `CEO_REPORTED` addendum. **Only the owner can do this.** | HIGH | ADR-0018 cannot be ratified on evidence that attests a workflow file which no longer exists |

**Recommended ratification batch, in dependency order.** Q17 and Q18 first, because they are
interpretive and every later lock decision depends on them. Then Q20 and Q19, the two live
conformance violations. Then Q21, which unblocks C-01, C-02 and C-05. Then Q24 and Q25, which are
the two real evidential weaknesses. Then the housekeeping set, Q1, Q2, Q3, Q10 and Q12, which are
mostly recording what already happens. Q4, Q5, Q7 and Q8 last, since they are product and legal
decisions that block no certified work.

**Also awaiting a ratification decision, not new questions:** ADR-0003, ADR-0004, ADR-0013,
ADR-0014 and ADR-0018 through ADR-0032 are all still PROPOSED. ADR-0003 is the most consequential,
because ratified ADR-0001 and unratified ADR-0003 disagree about the top-level folder set, which is
the oldest open asymmetry in the register.

## Resolution log

No row may be filled until the owner ratifies the decision that resolves the question. Entries
recorded as RESOLVED PENDING RATIFICATION are deliberately **absent** from this log, because the log
records settled matters and a PROPOSED entry settles nothing.

| ID | Resolved by | Date | Decision link |
|---|---|---|---|
| Q13 | Prashant Kumar (owner) | 2026-08-13 | ADR-0033 D2; ADR-0001 and ADR-0002 ratified as written |
| Q1, in part | Prashant Kumar (owner) | 2026-08-13 | ADR-0033 D1. Owner, builder and auditor roles named. Docs, engine and release owners NOT designated and remain OPEN. |
| Q8, direction only | Prashant Kumar (owner) | 2026-08-13 | ADR-0033 D3. Dependency ordering ratified with five qualifications. Per-phase criteria remain OPEN. |
| (not a question) Tier-0 formal lock | Prashant Kumar (owner) | 2026-08-13 | ADR-0005 ratified as written; ADR-0034 verifies all four Constitution s12 conditions. **Tier-0 is FORMALLY LOCKED.** Recorded here because it is the first artifact in the repository to meet the constitution's definition. |
| (not a question) Registry varga ratification | Prashant Kumar (owner) | 2026-08-13 | ADR-0009, ADR-0010 and ADR-0011 ratified as written (ADR-0035). D2, D3, D7, D12 and D30 are owner-ratified CERTIFIED. **NOT Locked**: s12 condition 4 fails because no entry declares a varga lock, and ratifying a certification does not create one. |
| (not a question) Drishti and sign-convention ratification | Prashant Kumar (owner) | 2026-08-13 | ADR-0012 ratified as written (ADR-0036). **Closes the ADR-0035 D4 asymmetry**: the convention the ratified vargas emit is now itself ratified. Sign conventions are owner-ratified and locked in behaviour, but **NOT an s12 Locked artifact**; see Q18. |

### Awaiting ratification (not yet resolutions)

| ID | Candidate resolution | Drafted | Ratification blocker |
|---|---|---|---|
| Q6 | ADR-0024, strengthened by ADR-0030 clause 1 | 2026-08-11 | Both ADRs PROPOSED. **The blocker changed on 2026-08-13: an owner now exists, so this awaits a ratification decision rather than the absence of an authority.** |
| Q9 | ADR-0025, strengthened by ADR-0030 clause 2 | 2026-08-11 | Both ADRs PROPOSED. Same changed blocker as Q6. |
| Q16 | ADR-0032, implemented and gated | 2026-08-13 | ADR is PROPOSED. Same changed blocker as Q6. |
| Q8, per-phase criteria | ADR-0026 plus `docs/Q8_CLOSURE_MATRIX.md` | 2026-08-11 | Closure criteria not met; matrix unratified. The DIRECTION half is now ratified; this row covers only the criteria half. |
