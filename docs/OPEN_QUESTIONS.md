<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACTIVE REGISTER. Fourteen questions: twelve open, two with candidate resolutions awaiting ratification. Nothing in this register is ratified, because Q1 is itself open. |
| Version | 0.4.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# Open Questions Register

Ambiguities are decided by the owner, never by silent assumption. Each question blocks the
artifacts listed against it. Resolution = decision log entry + this register updated.

| ID | Question | Why it matters | Blocks | Status |
|---|---|---|---|---|
| Q1 | Who are the named owners/maintainers (docs owner, engine owner, release owner)? | Accountability for a 10+ year artifact | All status headers | OPEN |
| Q2 | Branch/review model (trunk-based vs GitFlow; required reviewers; protection rules)? | Merge discipline | CONTRIBUTING.md | OPEN |
| Q3 | Versioning and release policy (repo-wide semver vs per-component; tagging; changelog scope)? | Long-term compatibility management | CHANGELOG.md, engine releases | OPEN |
| Q4 | Authoritative expansion, scope and mutual boundary of **HLKG** and **AKG**? | Two specification skeletons cannot be filled without inventing meaning | HLKG_SPEC.md, AKG_SPEC.md, knowledge/ layout | OPEN |
| Q5 | One-paragraph ratified project mission (what the system is and is not)? | Anchors MASTER_ARCHITECTURE section 1 | MASTER_ARCHITECTURE.md | OPEN |
| Q6 | May `engine/` ever read `knowledge/` at runtime, or is knowledge strictly an app-layer concern? | Hard dependency rule | MASTER_ARCHITECTURE.md section 4 | **RESOLVED PENDING RATIFICATION** (ADR-0024) |
| Q7 | Repository license, given upstream dual-licensed dependencies (e.g. AGPL-3.0 Swiss Ephemeris) and possible commercial deployment? | Legal viability of the whole repo | LICENSE (intentionally absent until decided) | OPEN |
| Q8 | Ratified roadmap phases with entry/exit criteria? | Prevents narrative-driven "done" | PROJECT_ROADMAP.md | **OPEN.** Resolution DRAFTED, not closed (ADR-0026) |
| Q9 | Should the existing certified calculation kernel (astro_kernel v1.3, Tier-0 portably certified) be imported into `engine/` as-is as the first component, and under what module name? | Avoids re-implementation; preserves certification lineage | engine/ population | **RESOLVED PENDING RATIFICATION** (ADR-0025) |
| Q10 | CI provider and mandatory pipeline stages (validation standard is CI-ready but no provider is chosen)? | Automation of the gates | tools/, repository settings | OPEN |
| Q11 | Should a direct value-comparison test assert that `legacy/kp.py` and `engine/kp/tables.py` hold identical Vimshottari lord and year tables? | ADR-0023 D3 permits the three-way duplication on condition it is tested rather than removed. `engine/tests/test_vimshottari_consistency.py` compares `engine/dasha/tables.py` against `engine/kp/tables.py` only. The legacy-to-engine leg is covered behaviourally by the equivalence sweep and not by direct table comparison, so a divergence introduced in one table could in principle survive until a behavioural case happened to exercise it. | Completeness of the ADR-0023 D3 condition | OPEN, raised 2026-08-11 |
| Q12 | Is `LOCK_MANIFEST.json` a live register that must be kept current, or frozen historical evidence of the Tier-0 lock? | It records `tier1_kp_significator` as SPECIFICATION_PENDING and describes a tier structure that later work did not follow. If it is live it is stale and misleading; if it is frozen evidence it must say so, because a reader cannot currently tell which, and editing frozen certification evidence would be a governance violation while leaving a live register stale would be a documentation defect. ADR-0027 D5 declined to edit it for exactly this reason. | LOCK_MANIFEST.json, certification status reporting | OPEN, raised 2026-08-11 |
| Q13 | Were ADR-0001 and ADR-0002, both dated 2026-07-11 and both carrying `Status: Accepted`, ratified by the owner, or were they marked Accepted by the authoring agent before the register adopted its current status vocabulary? | They are the only two entries in the register claiming Accepted status, and they fix the canonical top-level folder set that ADR-0003 then reconciled against. If they were owner acts, they bind and ADR-0003 needs owner supersession. If they were not, the register contains two entries claiming an authority no one exercised, which is the exact failure mode ADR-0022 exists to prevent. The repository evidences neither reading, and both retroactively demoting them and retroactively confirming them would falsify the record. | Precedence of ADR-0001/0002 over ADR-0003; integrity of the Accepted status | OPEN, raised 2026-08-11. ADR-0028 finding C-06. **Only the owner can answer this one.** |
| Q14 | Should the ADR numbering gate in `.github/workflows/ci.yml` carry a committed negative control, as the identifier gate does? | The identifier gate plants a retired identifier on every CI run and fails the build if the gate does not catch it, so its PASS is evidence. The numbering gate has no such control, so a PASS proves only that the gate ran, not that it can still fail. ADR-0029 corrected a real numbering defect and the gate now passes; without a negative control there is nothing to detect the gate silently breaking later, which is exactly the circularity the project charter section 11 warns against. | Evidential value of the governance job's numbering step | OPEN, raised 2026-08-11. ADR-0029 consequences. Adding it is a workflow change and was not authorised in the pass that raised it. |

## Status vocabulary used in this register

| Status | Meaning |
|---|---|
| OPEN | No decision exists. |
| RESOLUTION DRAFTED, PENDING RATIFICATION | A candidate answer exists in a document, it is explicitly unratified, and it does not bind. The question is still OPEN for every purpose that depends on a ratified answer. |
| RESOLVED PENDING RATIFICATION | An ADR records a decision that answers the question. The ADR itself is PROPOSED, because Q1 is open and `PROJECT_CONSTITUTION.md` section 11 reserves ratification to the owner. Nothing here is Accepted. |
| RESOLVED | An owner-ratified decision exists. **No question in this register currently holds this status.** |

The distinction matters and is not bookkeeping. Q1, the named owners, is itself open, so there is at
present **no authority in the repository that can Accept anything**. Every ADR in
`docs/DECISION_LOG.md`, including ADR-0022 through ADR-0030 which were written to resolve the
ADR-0013 conflicts, to disposition the earlier register, and to correct the numbering gate, is
PROPOSED. A reader must not treat any entry below as settled.

The two entries that carry `Status: Accepted`, ADR-0001 and ADR-0002, are the subject of Q13 and are
not evidence that ratification has ever occurred.

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
| Q13 | The owner states whether ADR-0001 and ADR-0002 were ratified. If yes, they stand and ADR-0003 requires owner supersession. If no, their status is corrected by a superseding entry that records the correction rather than by editing them. | **Owner only.** No evidence in the repository can settle this, and inferring either answer would falsify the record. |
| Q14 | The governance job plants an invalid ADR heading on every run and fails the build if the numbering gate does not reject it, mirroring the identifier gate's existing control. | Engineering, on owner authorisation. Adding it is a workflow change. |

## Q8 closure criteria (ADR-0021 D2)

Q8 remains **OPEN**. ADR-0026 addresses roadmap reconciliation and drafts a resolution; it does not
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

No row in this table may be filled until an owner ratifies the decision that resolves the question.
Entries recorded as RESOLVED PENDING RATIFICATION above are deliberately **absent** from this log,
because the log is the record of settled matters and nothing is settled while Q1 is open.

| ID | Resolved by | Date | Decision link |
|---|---|---|---|
| - | - | - | - |

### Awaiting ratification (not yet resolutions)

| ID | Candidate resolution | Drafted | Ratification blocker |
|---|---|---|---|
| Q6 | ADR-0024, strengthened by ADR-0030 clause 1 | 2026-08-11 | Q1 open; both ADRs are PROPOSED |
| Q9 | ADR-0025, strengthened by ADR-0030 clause 2 | 2026-08-11 | Q1 open; both ADRs are PROPOSED |
| Q8 | ADR-0026 plus `docs/Q8_CLOSURE_MATRIX.md` | 2026-08-11 | Closure criteria not met; matrix unratified; prior CEO direction to keep Q8 open |
