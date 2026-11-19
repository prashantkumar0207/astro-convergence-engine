<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED by the owner as evidence within its stated scope (`ADR-0129`).** This record declares nothing: `ADR-0129` records the exit decision. |
| Version | 0.4.0 |
| Owner | Project Owner (`ADR-0051` D4; `ADR-0107` Q-C) |
| Last updated | 2026-11-19 |
| Review cadence | Regenerate at the exact `main` SHA of any exit decision |

# EVIDENCE phase-exit evidence and checklist

This record tests the EVIDENCE phase against the requirements already accepted in `docs/Q8_CLOSURE_MATRIX.md` s6, and the
cross-phase invariants in s14 (`ADR-0048`). It adds no criterion. A stored artifact is history, not proof, so the runs are
listed in s3. Version 0.3.0 evaluates `ad4d5f7`, after findings F1 and F2 and limit L1 were corrected. Version 0.1.0 evaluated
`689fd36`, and 0.2.0 evaluated `f24771f`.

## 1. Result for the reviewer

| Status | Rows | Which |
|---|---|---|
| Met | 28 | Prerequisites, entry, scope, certification gates, two approvals, six invariants |
| Met with a stated qualification | 4 | X1, X2, X3, I4 |
| Open finding | 0 | F1, F2 and L1 are corrected and merged (s5) |
| Pending | 1 | A3, the exit approval this checkpoint would give |

**The decision needed is the exit itself.** The only residual limit is L2: a complete forgery, identical to what `persist()`
would write, by someone with direct write access to the database. The CEO accepted L2 as a documented external-tampering limit
(`ADR-0127` s1). Every inconsistent forgery tried is refused.

## 2. What was evaluated

- **Evaluated `main` SHA:** `ad4d5f7383ba2a0c4f53464132198831b77be72a`, the merge of PR #63. Parents
  `f24771fb7405bfd4adfb0a44ce13c322f0319d76` and `584fcb097c8ad8c746f9d24873cfd7d029586de4`. Tree `a6780f489f22b23fcebf361f9b68cd79f496735c`, identical to the PR head.
- **EVIDENCE entry baseline:** `90cd0cae777f6e7e67b78b109be68b714fa8cf91` (`ADR-0114`).
- **Later commits:** the commits that carry this record are later SHAs, and are not the one evaluated here. They change
  documentation only.

## 3. Regenerated evidence at `ad4d5f7`

| Run | Result |
|---|---|
| Post-merge CI `44498742069` (push to `main`, `ubuntu-24.04`) | Success on all four jobs. 2,348 tests on Python 3.11 and 3.12. Drift clean on 76 files in the 3.11, 3.12 and oracle jobs. |
| Clean native Linux regeneration from an archive of the tree | 24 of 24 certifiers pass. Drift clean on 76 files. All governance steps pass. 2,348 tests passed, 0 skipped. No tree changes. |
| C3 scope coverage | 24 artifacts, 56 capabilities, 276 members, 176 gates; 3 open tracked overclaims, 2 `scope_not_gated`. |
| C4 reachability | 188 in use and covered, 143 not in use; 0 uncovered, 0 material `UNKNOWN`. |

`EVIDENCE_FOUNDATIONS_V1` (result PASS; committed SHA-256 `c287b5358430c95ce66348496a710bcd5f4928cf00573020bd16bf8698a0209a`):

| Gate | Classification | Result |
|---|---|---|
| A entity integrity | structural | 0 mismatches |
| B entity refusals | negative control | 22 refusals |
| C event integrity | structural | 0 mismatches |
| D event refusals | negative control | 60 refusals |
| E event-class registry | conformance | 0 mismatches |
| F comparator controls | negative control | 8 controls |
| G ledger integrity | structural | 0 mismatches |
| H ledger refusals | negative control | 64 refusals |
| I holdout leakage | negative control | 10 controls |
| J evidence integrity | structural | 0 mismatches, 2 controls |
| K evidence refusals | negative control | 55 refusals |
| L relationships and provenance | negative control | 12 controls |
| M registry integrity | structural | 0 mismatches, 14 controls |
| N registry refusals | negative control | 50 refusals |
| O snapshot fails closed | negative control | 13 controls |
| P graph integrity | structural | 0 mismatches, 2 controls |
| Q graph refusals | negative control | 71 refusals |
| R graph agreement | structural | 0 mismatches, 16 controls |
| S evidence read integrity | negative control | 10 forgeries, 101 refusals, 12 legitimate read paths preserved, 6 controls |
| T relationship integrity | negative control | 42 forgeries, 89 refusals, 6 legitimate read paths preserved, 6 controls |
| U historical rule integrity | negative control | 6 forgeries, 60 refusals, 7 legitimate read paths preserved, 5 controls |

## 4. Checklist against `Q8_CLOSURE_MATRIX.md`

### 4.1 Prerequisites (s6)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| P1 | JATAKA exit | Met | `ADR-0110`, owner-ratified |
| P2 | DP-005 answered | Met | `ADR-0112` s2 (C, A, C, with conditions) |
| P3 | DP-008 answered | Met | `ADR-0111` (Option B) |
| P4 | Finding M-04 resolved | Met | PR #44, merged; recorded in `ADR-0113` |
| P5 | Finding M-05 resolved | Met | PR #45, merged; recorded in `ADR-0113`. The three `TRANSIT_V1` overclaims stay open, as `ADR-0112` requires |
| P6 | Finding M-09 resolved | Met | PR #46, merged at `46536da`; recorded in `ADR-0113` |

### 4.2 Entry criterion (s6)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| E1 | H0, H1, H2, H4 and H5 promoted to ratified specifications | Met | `ADR-0113`. Each specification's status header reads `ACCEPTED` |

### 4.3 Implementation scope (s6)

| # | Requirement | Status | Delivered by | Merge | Post-merge CI |
|---|---|---|---|---|---|
| S1 | Entity model with specialised subject types | Met | WP-E1 (`ADR-0114`), PR #48 | `06267f1` | `42581789417` |
| S2 | Event model | Met | WP-E2 (`ADR-0115`), PR #49 | `dfdfadb` | `42589414966` |
| S3 | Historical event ledger with protected holdout support | Met | WP-E3 (`ADR-0116`), PR #50 | `0f50bc8` | `42771214588` |
| S4 | Evidence model with the five relationship classes | Met | WP-E4 (`ADR-0119`), PR #54; corrected by PR #62 (`ADR-0125`) | `9bf782d`; `f24771f` | `43213469895`; `44302736571` |
| S5 | Interpretation rule registry | Met | WP-E5 (`ADR-0120`, `ADR-0121`), PR #56; historical reads corrected by PR #63 (`ADR-0127`) | `69730bf`; `ad4d5f7` | `44047429370`; `44498742069` |
| S6 | Provenance graph recording | Met | WP-E6 (`ADR-0122`), PR #59; reads corrected by PR #61 (`ADR-0124`) | `689fd36`; `16e3e7f` | `44273894275`; `44292709114` |
| S7 | No scoring, no weighting, no fitting | Met | A scan of `engine/evidence/` finds two names containing "fit". `historical_fit` is a confidence component carried as supplied or absent and never computed (`ADR-0119` AC7). `_require_fit` checks that a rule's school and strength match an item. Neither fits anything. Structural tests refuse division and multiplication in the evidence model, store, identifier and graph modules. | | |

### 4.4 Certification gates (s6)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| G1 | Schema round-trip | Met | Gates A, C, G, J, M and P |
| G2 | Immutability enforcement | Met | All 19 tables in the shared database carry UPDATE and DELETE triggers. The three issuer tables may only advance. Direct-SQL refusals in gates B, D, H, K and Q |
| G3 | Holdout-leakage detection | Met | Gate I, 10 controls, including protected entries served for selection, tuning, development and rectification |
| G4 | Negative test: analytical content cannot be stored on an entity or an event | Met | Gate B (4 analytical keys on an entity); gate D (26 on an event and its parts) |
| G5 | Provenance-mismatch detection across joined evidence | Met | Gate K (a join differing in each of the 7 provenance fields); gate L (a planted comparator ignoring each field is rejected); gate T (a relationship joining items of differing provenance is refused) |
| G6 | Decomposability of every aggregate | Met | The three aggregates each return their members: `EvidenceStore.counts` (gate J), `HistoricalLedger.counts` (gate G) and `EvidenceStore.relationship_counts` (gate T). `issued_count` is an issuer's high-water mark, not an aggregate of records |

### 4.5 Exit criteria (s6)

| # | Requirement | Status | Evidence and qualification |
|---|---|---|---|
| X1 | Evidence can be produced, stored, retrieved and decomposed | **Met, qualified** | Gates J, K, R, S and U. **Qualification:** items are synthetic records built by a caller. No rule is applied to a chart, because rule application belongs to INTERPRETATION (s7) |
| X2 | Provenance sufficient to build the graph in the independence design | **Met, qualified** | Gates P, Q and R: all six node kinds of the design's s3, recorded at creation, each item reproduced from its graph alone. **Qualifications** are in s6 |
| X3 | No claim can exist without a rule identifier and full provenance | **Met, qualified** | Through the API, every attempt is refused (gates K and N). Rows written by direct SQL that break the requirements are refused by every evidence read (gates S and U) and every relationship read (gate T). **Qualification:** the residual limit L2 in s5, which the CEO accepted |

### 4.6 CEO approval (s6)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| A1 | Entry | Met | `ADR-0114`. The owner states the CEO PASS came first |
| A2 | Checkpoint at the evidence model | Met | `ADR-0119`, revision 1 and its ratification. The CEO's bounded HOLD is quoted there; the owner states the PASS |
| A3 | Exit | **Pending** | The final exit audit of this record |

### 4.7 Cross-phase invariants (s14)

| # | Invariant | Status | Evidence |
|---|---|---|---|
| I1 | No phase weakens a certification gate to pass | Met | No gate function has been deleted from the evidence certifier since entry. Each correction added a gate and left earlier gates identical. `SUPPORT_PATHS_V1` gates A to G are identical to entry. The only lines removed from CI are the three `runs-on` values pinned by PR #57 |
| I2 | No change to certified calculation behaviour without an ADR and recertification | Met | `engine/` outside `engine/evidence/` and the tests has **no diff** since entry. 26 of 28 artifacts differ only in volatile fields and `modules_scanned`. The other two are `EVIDENCE_FOUNDATIONS_V1` and `SUPPORT_PATHS_V1`, which gained gates H and I in WP-E1 |
| I3 | No second convention for anything that has one | Met | `ENT`, `EVR`, `EVD` and `RUL` are registered families (`ADR-0111`, `ADR-0113`), checked in CI. The graph issues no new family (`ADR-0122` D3) |
| I4 | Protected holdouts are never used for selection or tuning | **Met, qualified** | Gates H and I. **Qualification:** the ledger's purpose check covers reads through the ledger only, as the certificate's non-claims state |
| I5 | Statistical significance is never represented as proof | Met | Nothing in EVIDENCE computes a statistic |
| I6 | C4 is never represented as C5 | Met | `EVIDENCE_FOUNDATIONS_V1` states that it is structural certification only |
| I7 | The completion report states what it could not verify | Met | s7 of this record |

## 5. Findings and residual limits

### 5.1 Findings and limits corrected since version 0.1.0

| Finding | What was demonstrated | Correction | Merge | Post-merge CI | Result at `ad4d5f7` |
|---|---|---|---|---|---|
| **F1** | A row written by direct SQL, naming a rule never registered, was accepted by `load`, `evidence_ids`, `join`, `counts`, `classify` and `relate` | PR #61 (`ADR-0124`), gate S | `16e3e7f` | `44292709114` | Refused by every read |
| **F2** | A forged relationship record claiming `independent`, where `classify()` said `shared_origin`, was returned by `relationships()` and `relationship_counts()` | PR #62 (`ADR-0125`), gate T | `f24771f` | `44302736571` | Refused by both reads |
| **L1** | A forged rule row claiming another snapshot, naming a `RUL` number never issued, with an evidence row and matching graph rows, was accepted by `load` and `evidence_ids` | PR #63 (`ADR-0127`), gate U | `ad4d5f7` | `44498742069` | Refused: a historical rule version must be an issued `RUL`, under its school, and a version still published unchanged |

### 5.2 The residual limit on X3, demonstrated at `ad4d5f7`

| Limit | What is accepted | Why it remains | Disposition |
|---|---|---|---|
| **L2** | A complete forgery of a published rule's evidence: exactly the rows `persist()` would have written | Such rows cannot be told apart from real ones by any check inside the store | Accepted by the CEO as a documented external-tampering limit (`ADR-0127` s1) |

A historical rule version now has to be what the governed records prove, so a forged row claiming another snapshot is refused unless it
copies a genuine publication exactly. Such a copy is an L2 forgery.

## 6. Qualifications carried forward

**On X2, what the recorded graph does not contain:**
- **Timing nodes** have no upstream edge, because an item does not record how its timing context was computed.
- **Vargas:** a chart node is recorded by label and varga, with no separate edge from D1 to the varga.
- **Question and candidate moments** are absent. No question engine exists.
- **`CORRELATED_WITH`** is not recorded, because nothing in EVIDENCE measures correlation.
- **The independence design** stays `PROPOSED`. Only its s3 recording schema is adopted (`ADR-0122` D1).

**Carried from earlier decisions, none closed here:**
- The registry holds synthetic rules only. A populated registry is an INTERPRETATION prerequisite (s7).
- The three `TRANSIT_V1` scope overclaims stay open.
- Prediction issuance has no roadmap placement (`ADR-0117` addendum).
- Retiring `SUPPORT_PATHS_V1` gates H and I needs separate approval.
- Every non-claim in `EVIDENCE_FOUNDATIONS_V1` stands.

## 7. What could not be verified

- **The CEO's PASS decisions.** Their text is not in the repository. A1, A2 and the merges rest on the owner's statements.
- **Producer honesty.** The store cannot show that a producer's inputs or completeness statements are true.
- **Reads outside the APIs.** Direct database access to protected events cannot be detected.
- **Forged but consistent records.** See L2 in s5.
- **Independence in fact.** A relationship record is checked against the recorded items. That shows agreement with the recorded
  structure, not that two items are independent in fact.
- **Future classifier changes.** Stored relationships are checked by re-classifying them, so a later change to the classifier would make
  older records fail until a decision addresses it.
- **Real data.** Every record exercised is synthetic, so behaviour on real rules, charts or people is untested.
- **Fitness for INTERPRETATION.** Nothing here shows the evidence model suits rule application, which has not been built.

## 8. Charter compliance (`specs/PROJECT_CHARTER.md` v1.4.0)

- **s5 (provenance):** each item records its provenance when produced, and reads refuse rows that break it, subject to L2.
- **s6 (learning):** nothing in EVIDENCE learns, measures or fits.
- **s7 (the LLM as explainer):** no LLM path exists, and generated text cannot introduce a rule.
- **s9 (what stays fixed):** certified calculations are unchanged since entry (I2).
- **The Q8 disposition:** no prediction is issued.
- No conflict with the Charter was found.
