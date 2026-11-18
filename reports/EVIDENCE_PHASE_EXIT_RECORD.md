<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **PROPOSED, for independent CEO review.** This record presents evidence and declares nothing. EVIDENCE exit is **not** declared. |
| Version | 0.1.0 |
| Owner | Project Owner (`ADR-0051` D4; `ADR-0107` Q-C) |
| Last updated | 2026-11-18 |
| Review cadence | Regenerate at the exact `main` SHA of any exit decision |

# EVIDENCE phase-exit evidence and checklist

This record tests the EVIDENCE phase against the requirements already accepted in `docs/Q8_CLOSURE_MATRIX.md` s6, and the
cross-phase invariants in s14 (`ADR-0048`). It adds no criterion. A stored artifact is history, not proof, so the runs are
listed in s3.

## 1. Result for the reviewer

| Status | Rows | Which |
|---|---|---|
| Met | 28 | Prerequisites, entry, scope, certification gates, two approvals, six invariants |
| Met with a stated qualification | 3 | X1, X2, I4 |
| **Open finding, needs a CEO determination** | **1** | **X3 (finding F1, s5)** |
| Pending | 1 | A3, the exit approval this review would give |

**The decision needed is on F1.** An evidence row written by direct SQL can name a rule that was never registered, and six
store reads accept it. Whether that blocks exit depends on how the X3 clause is read, so this record does not settle it.

## 2. What was evaluated

- **Evaluated `main` SHA:** `689fd369e6f871a2e21b1afa20911ed305c973e7`, the merge of PR #59. Parents
  `e63f93edd4aacf3e692abb5a899ecbc7e10d8103` and `b4e5f516f64ee8b5db2d7dbb007639d8670ad3aa`. Tree `b10309ac7329e9332e6b7656ef43609f4f1bce73`, identical to the PR head.
- **EVIDENCE entry baseline:** `90cd0cae777f6e7e67b78b109be68b714fa8cf91` (`ADR-0114`).
- **Later commits:** committing this record creates a later SHA, which is not the one evaluated here.

## 3. Regenerated evidence at `689fd36`

| Run | Result |
|---|---|
| Post-merge CI `44273894275` (push to `main`, `ubuntu-24.04`) | Success on all four jobs. 2,084 tests on Python 3.11 and 3.12. Drift clean on 76 files in the 3.11, 3.12 and oracle jobs. |
| Clean native Linux regeneration from an archive of the tree | 24 of 24 certifiers pass. Drift clean on 76 files. All governance steps pass. 2,084 tests passed, 0 skipped. No tree changes. |
| C3 scope coverage | 24 artifacts, 56 capabilities, 276 members, 173 gates; 3 open tracked overclaims, 2 `scope_not_gated`. |
| C4 reachability | 188 in use and covered, 143 not in use; 0 uncovered, 0 material `UNKNOWN`. |

`EVIDENCE_FOUNDATIONS_V1` (result PASS; committed SHA-256 `287f24f9e304b2fe85383f5b6eace0961bb3937e0558d5db7c71089c8f4aff51`):

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
| S4 | Evidence model with the five relationship classes | Met | WP-E4 (`ADR-0119`), PR #54 | `9bf782d` | `43213469895` |
| S5 | Interpretation rule registry | Met | WP-E5 (`ADR-0120`, `ADR-0121`), PR #56 | `69730bf` | `44047429370` |
| S6 | Provenance graph recording | Met | WP-E6 (`ADR-0122`), PR #59 | `689fd36` | `44273894275` |
| S7 | No scoring, no weighting, no fitting | Met | A scan of `engine/evidence/` finds no such function, class or typed field, except `historical_fit`, a confidence component carried as supplied or absent and never computed (`ADR-0119` AC7). Structural tests refuse division and multiplication in the evidence model, store, identifier and graph modules. | | |

### 4.4 Certification gates (s6)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| G1 | Schema round-trip | Met | Gates A, C, G, J, M and P |
| G2 | Immutability enforcement | Met | All 19 tables in the shared database carry UPDATE and DELETE triggers. The three issuer tables may only advance. Direct-SQL refusals in gates B, D, H, K and Q |
| G3 | Holdout-leakage detection | Met | Gate I, 10 controls, including protected entries served for selection, tuning, development and rectification |
| G4 | Negative test: analytical content cannot be stored on an entity or an event | Met | Gate B (4 analytical keys on an entity); gate D (26 on an event and its parts) |
| G5 | Provenance-mismatch detection across joined evidence | Met | Gate K (a join differing in each provenance field); gate L (a planted comparator ignoring each of the 7 fields is rejected) |
| G6 | Decomposability of every aggregate | Met | The three aggregates each return their members: `EvidenceStore.counts` (gate J), `HistoricalLedger.counts` (gate G) and `EvidenceStore.relationship_counts` (tests). `issued_count` is an issuer's high-water mark, not an aggregate of records |

### 4.5 Exit criteria (s6)

| # | Requirement | Status | Evidence and qualification |
|---|---|---|---|
| X1 | Evidence can be produced, stored, retrieved and decomposed | **Met, qualified** | Gates J, K and R. **Qualification:** items are synthetic records built by a caller. No rule is applied to a chart, because rule application belongs to INTERPRETATION (s7) |
| X2 | Provenance sufficient to build the graph in the independence design | **Met, qualified** | Gates P, Q and R: all six node kinds of the design's s3, recorded at creation, each item reproduced from its graph alone. **Qualifications** are in s6 |
| X3 | No claim can exist without a rule identifier and full provenance | **Open finding** | Through the API, every attempt is refused (gates K and N). A row stripped of provenance is refused on read. **Finding F1 (s5) is open** |

### 4.6 CEO approval (s6)

| # | Requirement | Status | Evidence |
|---|---|---|---|
| A1 | Entry | Met | `ADR-0114`. The owner states the CEO PASS came first |
| A2 | Checkpoint at the evidence model | Met | `ADR-0119`, revision 1 and its ratification. The CEO's bounded HOLD is quoted there; the owner states the PASS |
| A3 | Exit | **Pending** | This review |

### 4.7 Cross-phase invariants (s14)

| # | Invariant | Status | Evidence |
|---|---|---|---|
| I1 | No phase weakens a certification gate to pass | Met | No gate function has been deleted from the evidence certifier since entry. `SUPPORT_PATHS_V1` gates A to G are identical to entry. The only lines removed from CI are the three `runs-on` values pinned by PR #57 |
| I2 | No change to certified calculation behaviour without an ADR and recertification | Met | `engine/` outside `engine/evidence/` and the tests has **no diff** since entry. 26 of 28 artifacts differ only in volatile fields and `modules_scanned`. The other two are `EVIDENCE_FOUNDATIONS_V1` and `SUPPORT_PATHS_V1`, which gained gates H and I in WP-E1 |
| I3 | No second convention for anything that has one | Met | `ENT`, `EVR`, `EVD` and `RUL` are registered families (`ADR-0111`, `ADR-0113`), checked in CI. The graph issues no new family (`ADR-0122` D3) |
| I4 | Protected holdouts are never used for selection or tuning | **Met, qualified** | Gates H and I. **Qualification:** the ledger's purpose check covers reads through the ledger only, as the certificate's non-claims state |
| I5 | Statistical significance is never represented as proof | Met | Nothing in EVIDENCE computes a statistic |
| I6 | C4 is never represented as C5 | Met | `EVIDENCE_FOUNDATIONS_V1` states that it is structural certification only |
| I7 | The completion report states what it could not verify | Met | s7 of this record |

## 5. Finding F1: an unregistered rule named by a row written directly to the database

**What was demonstrated at `689fd36`.** A synthetic `evidence_items` row was inserted by direct SQL. It was well formed, carried
full calculation provenance, and named a `RUL` number that was never issued or registered.

| Read | Result |
|---|---|
| `load`, `evidence_ids`, `join`, `counts`, `classify`, `relate` | **Accepted** |
| `item_graph`, `reproduce`, `recorded_graph` | Refused |
| `persist` of the same item through the API | Refused |
| `load` of a row stripped of its provenance | Refused |

**Why it needs a determination.** Read literally, X3 holds: the row carries a rule identifier and full provenance. But H4 s4
says only registered rules produce evidence, and the CEO's HOLDs on PR #56 and PR #59 both treated rows written by direct SQL
as in scope.

| Option | Effect |
|---|---|
| **A. Treat F1 as blocking.** Authorize one bounded correction: every evidence read refuses a row whose rule version is not registered or whose graph is not recorded, with regressions and gate coverage. | Closes the inconsistency. **Recommended**, because it matches the two earlier HOLDs and needs no new criterion. |
| **B. Accept F1 as a stated limitation,** recorded as a certificate non-claim. | No code change. The certificate already states that direct SQLite access to the ledger cannot be detected. |

Neither option has been acted on. Under either one, someone with write access to the database could still forge a row and every
record that justifies it, which no check inside the store can detect.

**To reproduce:** build a store with one registered rule and one entity, then insert `item_to_record(EvidenceId.from_number(500),
item)` into `evidence_items`, where `item.rule` names `RuleId.from_number(999999)`. Then call the reads above.

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
- **Forged but consistent records.** A forged item whose justifying records were forged to agree with it is not detectable.
- **Real data.** Every record exercised is synthetic, so behaviour on real rules, charts or people is untested.
- **Fitness for INTERPRETATION.** Nothing here shows the evidence model suits rule application, which has not been built.

## 8. Charter compliance (`specs/PROJECT_CHARTER.md` v1.4.0)

- **s5 (provenance):** each item records its provenance when produced, subject to F1.
- **s6 (learning):** nothing in EVIDENCE learns, measures or fits.
- **s7 (the LLM as explainer):** no LLM path exists, and generated text cannot introduce a rule.
- **s9 (what stays fixed):** certified calculations are unchanged since entry (I2).
- **The Q8 disposition:** no prediction is issued.
- No conflict with the Charter was found. F1 is reported for the CEO's determination.
