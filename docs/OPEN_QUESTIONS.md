<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACTIVE REGISTER. Thirteen questions: eleven open, two with candidate resolutions awaiting ratification. Nothing in this register is ratified, because Q1 is itself open. |
| Version | 0.3.0 |
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

## Status vocabulary used in this register

| Status | Meaning |
|---|---|
| OPEN | No decision exists. |
| RESOLUTION DRAFTED, PENDING RATIFICATION | A candidate answer exists in a document, it is explicitly unratified, and it does not bind. The question is still OPEN for every purpose that depends on a ratified answer. |
| RESOLVED PENDING RATIFICATION | An ADR records a decision that answers the question. The ADR itself is PROPOSED, because Q1 is open and `PROJECT_CONSTITUTION.md` section 11 reserves ratification to the owner. Nothing here is Accepted. |
| RESOLVED | An owner-ratified decision exists. **No question in this register currently holds this status.** |

The distinction matters and is not bookkeeping. Q1, the named owners, is itself open, so there is at
present **no authority in the repository that can Accept anything**. Every ADR in
`docs/DECISION_LOG.md`, including ADR-0022 through ADR-0028 which were written to resolve the
ADR-0013 conflicts and to disposition the earlier register, is PROPOSED. A reader must not treat any
entry below as settled.

The two entries that carry `Status: Accepted`, ADR-0001 and ADR-0002, are the subject of Q13 and are
not evidence that ratification has ever occurred.

## Q6 resolution (ADR-0024)

`engine/` MUST NOT depend on top-level `knowledge/` at runtime for certification-critical
calculation. `engine/knowledge/` is implementation-owned rule data, a different thing despite the
name collision, and is permitted under the ADR-0023 four-part test.

Verified rather than asserted: `engine/` contains zero runtime imports of top-level `knowledge/`.
The decision protects an existing property; no code must change to comply. One live dependency is
declared on the record, `engine/astrology/dignity.py` loading `engine/knowledge/data/dignities.json`
via `engine/knowledge/repository.py`, which sits outside the current Tier-0 lock scope.

## Q9 resolution (ADR-0025)

The kernel under `engine/` is the authoritative production calculation foundation, its Tier-0 lock
lineage at `bfae088` is preserved, and `legacy/` remains a historical and equivalence reference that
is **NOT retired**. `docs/LEGACY_KERNEL_MIGRATION.md` forbids retirement before all certified
functionality has migrated, and that condition is not met.

Verified rather than asserted: `legacy/` is imported by five test modules and by no production
module. The one reference inside `engine/kp/intervals.py` is a docstring, not an import.

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
| Q6 | ADR-0024 | 2026-08-11 | Q1 open; ADR is PROPOSED |
| Q9 | ADR-0025 | 2026-08-11 | Q1 open; ADR is PROPOSED |
| Q8 | ADR-0026 plus `docs/Q8_CLOSURE_MATRIX.md` | 2026-08-11 | Closure criteria not met; matrix unratified; prior CEO direction to keep Q8 open |
