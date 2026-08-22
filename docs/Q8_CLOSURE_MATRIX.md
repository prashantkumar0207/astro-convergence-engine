<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED. Owner-ratified 2026-08-17 (ADR-0048). Q8 is CLOSED.** Ratification approves this matrix as the roadmap-governance framework; it is not implementation authorisation for any phase. Phase entry remains gated by each phase's own prerequisites, entry criteria, and CEO approval per the sections below, none of which are weakened or waived by ratification. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# Q8 Closure Matrix

## 1. What this is and is not

Open question Q8 asks for ratified roadmap phases **with entry and exit criteria**. ADR-0020 D6 gave
the domain order. ADR-0021 D2 confirmed that the order alone does not close Q8, and that closure
requires, per phase: prerequisites, entry criteria, implementation scope, certification gates, exit
criteria, and CEO approval requirement.

This document proposed that matrix so the owner would have something concrete to amend or reject.

**Q8 is CLOSED (ADR-0048, 2026-08-17).** The owner ratified this matrix as written; the register
(`docs/OPEN_QUESTIONS.md`) is updated accordingly. Ratification closes the *governance question* -
that ratified per-phase criteria now exist. **It still authorises no implementation of anything.**
Every phase below remains gated by its own prerequisites, entry criteria and CEO approval, and phase
entry does not imply authorisation of every capability inside that phase - each says so individually.
`ADR-0048` additionally records that Phase G's own exit criteria (section 3) are not independently
confirmed met as of ratification - see that entry for detail. Ratification does not assert they are.

## 2. Conventions used

**Certification gates** cite the existing vocabulary where one exists and the charter's C0 to C5 levels
where the mapping is still unresolved, which is itself pending ADR-0017.

**CEO approval requirement** distinguishes three levels: *phase entry*, approval to begin;
*intra-phase*, approval at named checkpoints inside the phase; *phase exit*, approval that the phase is
complete. A phase requiring only entry and exit approval is one the builder may work through
continuously, which is the throughput model already in use.

**Prerequisites** are things that must be true before entry and are not part of the phase's own work.

## 3. Phase G, governance and certification (in progress)

| Field | Content |
|---|---|
| Prerequisites | None. Entered from the 2026-08-10 project state report. |
| Entry criteria | Met: baseline `1f861f6` reconstructed and audited. |
| Implementation scope | G6 oracle reproducibility and CI (done, `a460ba2`, remote-validated). G1 identifier reconciliation (done, `c18150b`). G2 charter commit, G3 precedence hierarchy, G4 decision papers, G5 certification taxonomy, G7 stale documentation. Architecture and specification preparation (done). |
| Certification gates | Default gate green; all validators; all certification runners regenerate PASS; identifier governance gate with negative control; zero-calculation-impact fingerprint proof on every commit. |
| Exit criteria | G2, G3, G4, G5, G7 complete. DP-001 answered so ADR entries can leave PROPOSED. The three BLOCKER findings B-01, B-02, B-03 either resolved or explicitly deferred by decision. |
| CEO approval | Per commit, currently. Recommend relaxing to entry and exit plus named checkpoints once DP-001 lands. |

## 4. FOUNDATION

| Field | Content |
|---|---|
| Prerequisites | Phase G exit. ADR-0017 certification taxonomy ratified, since this phase's gates are stated in it. DP-009 answered, because the tier classification determines the certification methodology. |
| Entry criteria | The gate-integrity work recommended in the G1 report is complete: B-01 rule/division validation, B-02 rule-content pinning, B-03 live recomputation, H-04 depth-3 oracle gate, and anti-fitting scan coverage. Rationale: everything built afterwards is certified by these gates. |
| Implementation scope | Rise and set with declared conventions. Panchanga: tithi, vara, nakshatra as a panchanga element, yoga, karana. Rahu Kalam, Yamaganda, Gulika with variant tables recorded. Civil-date rendering for dasha boundaries. Resolution of H-01 true-node completeness and H-02 the ingress classification seam. Boundary-proximity indicators where sensitivity warrants. |
| Certification gates | Per capability: declared conventions in a calculation profile; independent external reference for the astronomical parts; the varga template of frozen rule, second transcription, dense sweep, ULP battery, external oracle and independent validator for the classification parts; protected holdout; regenerable artifact; collected pinning test; ADR. |
| Exit criteria | Every capability above at the level ADR-0017 defines as production certified. H-01 and H-02 resolved and certified, or explicitly deferred by decision with the dependent domains blocked accordingly. |
| CEO approval | Entry, per-capability checkpoint, exit. Per-capability because each is a new Tier-0 or Tier-1 claim. |

## 5. JATAKA

| Field | Content |
|---|---|
| Prerequisites | FOUNDATION exit. |
| Entry criteria | The Dasha roadmap's steps 1 to 6 complete: depth-3 gate, frozen dasha baseline, profile allow-list, the H-08 convention decision, near-boundary Moon cases, boundary-proximity indicator. |
| Implementation scope | Remaining production vargas in the roadmap's risk order. Vimshottari depth and convention extensions if decided. Aspect coverage beyond full graha drishti if decided. Planet strength if decided. Each is a separate ADR and none is implied by phase entry. |
| Certification gates | The per-varga template in `docs/NEW_VARGA_IMPLEMENTATION_TEMPLATE.md`. For dashas, the requirements in `docs/DASHA_CERTIFICATION_ROADMAP.md` section 4. |
| Exit criteria | Every capability declared a production analytical input is individually certified. No capability is in use that a certification artifact does not cover. |
| CEO approval | Entry, per capability, exit. A varga or dasha extension is never entered on the strength of phase entry alone. |

## 6. EVIDENCE

| Field | Content |
|---|---|
| Prerequisites | JATAKA exit. DP-005 answered, since H3, H4 and H5 depend on the knowledge boundary. DP-008 answered, since entities need identifiers. Provenance completeness: findings M-04, M-05 and M-09 resolved, because `docs/EVIDENCE_INDEPENDENCE_DESIGN.md` section 10 shows the evidence layer is unbuildable without it. |
| Entry criteria | H0, H1, H2, H4 and H5 promoted from C0 research to ratified specifications. |
| Implementation scope | Entity model with specialised subject types. Event model. Historical event ledger with protected holdout support in the store. Evidence model with the five relationship classes. Interpretation rule registry. Provenance graph recording. No scoring, no weighting, no fitting. |
| Certification gates | Schema round-trip. Immutability enforcement. Holdout-leakage detection. A negative test proving analytical content cannot be stored on an entity or an event. Provenance-mismatch detection across joined evidence. Decomposability of every aggregate. |
| Exit criteria | Evidence can be produced, stored, retrieved and decomposed, with provenance sufficient to build the graph in the independence design. No claim can exist without a rule identifier and full provenance. |
| CEO approval | Entry, checkpoint at the evidence model since it is the hub, exit. |

## 7. INTERPRETATION

| Field | Content |
|---|---|
| Prerequisites | EVIDENCE exit. The rule registry populated with at least one school's rules, each source-cited. |
| Entry criteria | H5 ratified. The LLM boundary implemented as a refusal, not a guideline. |
| Implementation scope | Rule application producing evidence items. Explanation generation traceable to rule identifiers. Strictly no prediction. |
| Certification gates | Refusal of unregistered rules. A negative test proving generated text cannot introduce a rule. Source-citation completeness. Variant coverage where a rule has recorded variants. |
| Exit criteria | Every interpretive claim traces to a registered, versioned, source-cited rule. Deterministic fact, interpretation and prediction are separated in the output, not only in the design. |
| CEO approval | Entry, checkpoint at the LLM boundary, exit. |

## 8. CONVERGENCE

| Field | Content |
|---|---|
| Prerequisites | INTERPRETATION exit. At least two independently certified analytical systems. `docs/EVIDENCE_INDEPENDENCE_DESIGN.md` section 11 decisions taken. The provenance graph populated and complete. |
| Entry criteria | H8 ratified. The independence design approved. The cut level decided and the unknown-relationship policy decided. |
| Implementation scope | Dependency-aware convergence. Bound-pair reporting with the cut. Minimum-cut explanation. Disagreement preservation. Reporting vocabulary including conflict and insufficient evidence. |
| Certification gates | Isolation enforcement so one system's output cannot reach another's input. The independence test battery in the design's section 12. A test that a measured null correlation does not raise the count. A test that conflicts are never netted against agreement. Explanation completeness. |
| Exit criteria | Convergence reports a bound pair, names its cut, names its minimum cut set, and can state whether agreeing sources could have disagreed. It produces a result with BTR absent. |
| CEO approval | Entry, checkpoint at the independence computation, exit. |

## 9. VARSHAPHAL

| Field | Content |
|---|---|
| Prerequisites | CONVERGENCE exit. Solar return certified, since `returns()` exists but is in no certification artifact. |
| Entry criteria | A Varshaphal specification at the depth H1 through H8 reached, with classical sources named and variants recorded. |
| Implementation scope | Varsha Lagna, Muntha, Varshesh, Tajika aspects in a school-isolated module, Sahams, Mudda dasha as a new dasha system. |
| Certification gates | Solar return against an external reference. Tajika aspects certified independently of Parashari drishti and never routed through it. Mudda dasha against the full dasha requirements. Derived-relationship edges to the parent natal chart present in the provenance graph. |
| Exit criteria | Each component individually certified. Derived relationships correctly reduce the independent path count, demonstrated by test. |
| CEO approval | Entry, per component, exit. |

## 10. MUHURTA

| Field | Content |
|---|---|
| Prerequisites | VARSHAPHAL exit. **H-02 independently reproduced per ADR-0020 D5, and repaired and certified if confirmed.** Panchanga and rise/set certified in FOUNDATION. Tara Bala and Chandra Bala specified. |
| Entry criteria | H-02 closed. A Muhurta specification including the search methodology and the purpose-specific rule sets. |
| Implementation scope | General Muhurta as search and ranking over candidate moments. Personalised Muhurta adding natal compatibility. Search window, candidate space and selection methodology exposed. |
| Certification gates | Panchanga correctness at candidate instants, which is the H-02 seam and must be a gate rather than an assumption. Search-space and candidate-count recording, with a test that a result cannot be emitted without them. Reproducibility of a ranking given identical inputs. |
| Exit criteria | Recommendations carry their reasons, their avoided factors, their search space and their confidence. The system cannot present "best of N" without N. |
| CEO approval | Entry, checkpoint at the search methodology, exit. |

## 11. PRASHNA

| Field | Content |
|---|---|
| Prerequisites | MUHURTA exit. H3 unblocked, meaning DP-005 answered. Panchanga certified. |
| Entry criteria | A Prashna specification with its classical source and rule set. The question entity type implemented. |
| Implementation scope | Question as entity, Prashna context and chart, applicable rules, qualified answer. No birth data required anywhere in the path. |
| Certification gates | A test that no birth data is required. A test that BTR refuses on a query-moment subject. Rule provenance completeness. |
| Exit criteria | A question yields a qualified answer traceable to registered rules, with no birth data involved. |
| CEO approval | Entry, exit. |

## 12. MUNDANE

| Field | Content |
|---|---|
| Prerequisites | PRASHNA exit. The multiple-comparison methodology decided per ADR-0021 D1. Competing-chart support implemented per ADR-0020 D3. |
| Entry criteria | A pre-registered validation protocol per `docs/VALIDATION_STANDARD.md` section 4, registered before any protected run. |
| Implementation scope | Non-personal entity charts. Competing chart sets with independent analysis and explicit disagreement. Mundane rule sets. Pre-registered validation. |
| Certification gates | A test that a protected holdout cannot be read by any selection or tuning process. Negative controls against permuted data. A test that a result cannot be emitted without its hypothesis and event counts. A test that competing charts produce separately attributed analyses. |
| Exit criteria | Mundane analysis is attributable to a specific candidate chart, disagreement between candidate charts is surfaced rather than resolved silently, and every validation claim carries its protocol, its counts and its effect sizes. |
| CEO approval | Entry, checkpoint at the validation protocol before the first protected run, exit. |

## 13. BTR, orthogonal to the phases

BTR is not a phase and is never a prerequisite for convergence. It becomes possible once EVIDENCE
exits, since it consumes evidence and the ledger, and it may be entered at any later point by its own
decision. Its gates are in `docs/H7_BTR_SPEC.md` section 9, plus the shape scoping and the
documented-origin refusal in section 11. Approval: entry and exit, with a checkpoint at the candidate
selection method, because that is where the anti-overfitting rules bite.

## 14. Cross-phase invariants

These hold in every phase and are not restated per phase. No phase may weaken a certification gate to
pass. No phase may modify certified calculation behaviour without its own ADR and recertification. No
phase may introduce a second convention for anything that already has one. Protected holdouts are never
used for selection or tuning. Statistical significance is never represented as scientific proof of
astrology. C4 is never represented as C5. Every phase's completion report states what it could not
verify.

## 15. What the owner decided for Q8 to close (historical framing, resolved 2026-08-17)

This section originally posed the questions the owner needed to settle: whether this matrix is the
right shape; whether the entry criteria are correct, particularly the recommendation that
gate-integrity work precede FOUNDATION and that H-02 gate MUHURTA; whether the approval levels are
right; whether BTR's orthogonal treatment is acceptable; and whether phases may overlap, which this
matrix assumes they may not.

**Resolved 2026-08-17 (`ADR-0048`): the owner ratified the matrix as written**, meaning as posed above,
with no amendment to any of the questions this section raised. The original question text is preserved
above unedited, per this repository's practice of not rewriting historical record; only this
introductory sentence and the closing line below are updated to state the outcome.

**Q8 is CLOSED. No phase is thereby authorised** - phase authorisation remains a separate, per-phase,
per-capability owner act, exactly as sections 3 through 14 and the cross-phase invariants (section 14)
already state.

## 16. Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-17 | Owner-ratified as written (`ADR-0048`). Q8 CLOSED. Status header, section 1 and section 15 updated to reflect ratification; sections 3-14 (the phase definitions) unchanged. No phase authorised by this change. |
| 1.0.0 | 2026-08-11 | Drafted on CEO direction as a candidate matrix. Q8 remains OPEN. |
