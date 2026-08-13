<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACTIVE REGISTER. Seventeen questions. **Owner ratifications of 2026-08-13: Q13 resolved; Q1 and Q8 ratified in part (ADR-0033); ADR-0005 ratified, making Tier-0 FORMALLY LOCKED (ADR-0034).** Twelve fully open, three with candidate resolutions awaiting a ratification decision, two ratified in part. An owner now exists, so ratification is possible; it is per-entry and has been given three times only. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-13 |
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
| Q11 | Should a direct value-comparison test assert that `legacy/kp.py` and `engine/kp/tables.py` hold identical Vimshottari lord and year tables? | ADR-0023 D3 permits the three-way duplication on condition it is tested rather than removed. `engine/tests/test_vimshottari_consistency.py` compares `engine/dasha/tables.py` against `engine/kp/tables.py` only. The legacy-to-engine leg is covered behaviourally by the equivalence sweep and not by direct table comparison, so a divergence introduced in one table could in principle survive until a behavioural case happened to exercise it. | Completeness of the ADR-0023 D3 condition | OPEN, raised 2026-08-11 |
| Q12 | Is `LOCK_MANIFEST.json` a live register that must be kept current, or frozen historical evidence of the Tier-0 lock? | It records `tier1_kp_significator` as SPECIFICATION_PENDING and describes a tier structure that later work did not follow. If it is live it is stale and misleading; if it is frozen evidence it must say so, because a reader cannot currently tell which, and editing frozen certification evidence would be a governance violation while leaving a live register stale would be a documentation defect. ADR-0027 D5 declined to edit it for exactly this reason. | LOCK_MANIFEST.json, certification status reporting | OPEN, raised 2026-08-11. **New evidence 2026-08-13** (ADR-0034 consequences): `certification/CURRENT_ENGINE_LOCK.json` states that `LOCK_MANIFEST.json` describes the LEGACY kernel exclusively and is deliberately left untouched, per audit finding F-17. That narrows the question but does not answer what the file is FOR or whether it is live; it stays OPEN and unedited. |
| Q13 | Were ADR-0001 and ADR-0002, both dated 2026-07-11 and both carrying `Status: Accepted`, ratified by the owner, or were they marked Accepted by the authoring agent before the register adopted its current status vocabulary? | They are the only two entries in the register claiming Accepted status, and they fix the canonical top-level folder set that ADR-0003 then reconciled against. If they were owner acts, they bind and ADR-0003 needs owner supersession. If they were not, the register contains two entries claiming an authority no one exercised, which is the exact failure mode ADR-0022 exists to prevent. The repository evidences neither reading, and both retroactively demoting them and retroactively confirming them would falsify the record. | Precedence of ADR-0001/0002 over ADR-0003; integrity of the Accepted status | **RESOLVED, 2026-08-13** (ADR-0033 D2). The owner ratified both entries as written, prospectively. The historical question of what the 2026-07-11 status meant is deliberately left unanswered and unneeded. |
| Q14 | Should the ADR numbering gate in `.github/workflows/ci.yml` carry a committed negative control, as the identifier gate does? | The identifier gate plants a retired identifier on every CI run and fails the build if the gate does not catch it, so its PASS is evidence. The numbering gate has no such control, so a PASS proves only that the gate ran, not that it can still fail. ADR-0029 corrected a real numbering defect and the gate now passes; without a negative control there is nothing to detect the gate silently breaking later, which is exactly the circularity the project charter section 11 warns against. | Evidential value of the governance job's numbering step | OPEN, raised 2026-08-11. ADR-0029 consequences. Adding it is a workflow change and was not authorised in the pass that raised it. |
| Q15 | Should `certification/current_engine_certification.json` be made byte-reproducible by recording the swetest invocation without the run's temporary directory and the checkout's absolute path? | Two runs of identical code over identical data currently produce different bytes, because each case records `swetest_cmd` containing `/tmp/swetest_<random>/` and the absolute checkout path. Root D-005 removed exactly this class of environment-specific absolute-path dependency from the legacy Tier-0 package, and it has reappeared here. It does not affect Constitution s12 condition 3, since both evidence files regenerate together and agree, but it means the artifact cannot be diffed across runs to show that nothing changed. | Byte-level reproducibility claims about Tier-0 evidence | OPEN, raised 2026-08-13. ADR-0031 consequences. |
| Q17 | Does `PROJECT_CONSTITUTION.md` s12 condition 4 require a **ratified** decision entry, or merely that an entry exists? | ADR-0033 D4 had to decide this in order to evaluate Tier-0's status, and adopted the ratified reading. The textual reading, that an entry merely records the lock, would let the builder satisfy all four Locked conditions with no human act at all, since conditions 1, 2 and 3 are machine-verifiable. That would make the constitution's strongest status its easiest to claim. The reading adopted is therefore the stricter one, but it is a builder interpretation of the owner's constitution and should be confirmed or corrected rather than left as precedent by default. | Governs every FUTURE lock. **No longer blocks Tier-0**: ADR-0005 was ratified on 2026-08-13, so condition 4 is met under either reading (ADR-0034). | OPEN, raised 2026-08-13. ADR-0033 D4; moot for Tier-0 per ADR-0034. **Owner-answerable in one line.** |
| Q16 | Should `scripts/certify_current_engine.py` call `certification_support.preflight()`, as the other certifiers do? | It verifies the swetest binary version at runtime but does NOT verify the ephemeris checksums against `CHECKSUMS.sha256`, and no anti-fitting scan forms part of this gate. That is VALIDATION_STANDARD s2 rules 4 and 6. The legacy Tier-0 runner did verify ephemeris checksums per root D-005, so this is a capability the current runner lost. Wiring it changes what the gate can reject, which is a scope decision rather than a repair. | VALIDATION_STANDARD s2 rules 4 and 6 for Tier-0 | **RESOLVED PENDING RATIFICATION** (ADR-0032). Implemented: preflight wired, coverage asserted, three committed negative controls. |

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

**Possible is not done.** Ratification is per-entry. Exactly three entries in `docs/DECISION_LOG.md`
are Accepted: **ADR-0001, ADR-0002 and ADR-0033**, all ratified by Prashant Kumar on 2026-08-13.
**ADR-0003 through ADR-0014 and ADR-0018 through ADR-0032 all remain PROPOSED**, including every
entry written to resolve the ADR-0013 conflicts, to disposition the earlier register, to correct the
numbering gate, and to repair and complete the Tier-0 certification evidence. A reader must not read
"an owner exists" as "the register is ratified".

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

### Awaiting ratification (not yet resolutions)

| ID | Candidate resolution | Drafted | Ratification blocker |
|---|---|---|---|
| Q6 | ADR-0024, strengthened by ADR-0030 clause 1 | 2026-08-11 | Both ADRs PROPOSED. **The blocker changed on 2026-08-13: an owner now exists, so this awaits a ratification decision rather than the absence of an authority.** |
| Q9 | ADR-0025, strengthened by ADR-0030 clause 2 | 2026-08-11 | Both ADRs PROPOSED. Same changed blocker as Q6. |
| Q16 | ADR-0032, implemented and gated | 2026-08-13 | ADR is PROPOSED. Same changed blocker as Q6. |
| Q8, per-phase criteria | ADR-0026 plus `docs/Q8_CLOSURE_MATRIX.md` | 2026-08-11 | Closure criteria not met; matrix unratified. The DIRECTION half is now ratified; this row covers only the criteria half. |
