<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACTIVE. **Section 3's dependency ordering is OWNER-RATIFIED (2026-08-13, ADR-0033 D3), and Tier-0 is FORMALLY LOCKED (2026-08-13, ADR-0034); every other section remains unratified.** This document distinguishes completed historical work, currently authorised work, future work and prerequisites, per ADR-0026 D5. It does NOT authorise implementation, and Q8's per-phase criteria remain OPEN. |
| Version | 0.5.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-13 |
| Review cadence | TBD |

# Project Roadmap

> Rule: every phase has explicit ENTRY and EXIT criteria; a phase is never "done" by
> narrative - only by evidence per VALIDATION_STANDARD.md.

## 0. What this document is, and what it is not

**It is** the single place that separates four different things which the repository previously
conflated: work that is finished and certified, work that is currently authorised, work that is
planned, and the prerequisites that gate each of them.

**It is not** an authorisation to implement anything. No item below may be started on the strength
of appearing here. Authorisation is a separate act by the owner, per `PROJECT_CONSTITUTION.md`
section 11.

**Q8's direction is ratified; its criteria are not.** On 2026-08-13 the owner ratified the
dependency ordering now recorded in section 3 (ADR-0033 D3), so that ordering binds. ADR-0021 D2's
closure criteria are untouched by it: prerequisites, entry criteria, implementation scope,
certification gates, exit criteria and approval requirements, for every implementation phase. A
candidate matrix meeting those criteria exists at `docs/Q8_CLOSURE_MATRIX.md` and is explicitly
unratified. **Until it is, no phase can be declared entered or exited by criteria**, and the ratified
ordering remains guidance rather than authorisation.

**Certified does not mean ready.** ADR-0026 D2. The calculation layers are certified to C2 or C4 in
several places. No evidence, interpretation, convergence, historical-validation, BTR, API or UI
capability exists at all. A reader who takes the certification badges as a measure of product
completeness will be badly wrong.

## 1. Completed historical work

Recorded as history, not as a plan that was followed. ADR-0026 D1: the certified astrology
foundation layers were developed **ahead of** the originally proposed Phase 1 intelligence layer in
`docs/PROJECT_BACKLOG.md`. That work is valid and certified. It is not undone and not re-sequenced
retrospectively. The sequencing implication of the backlog is superseded; its enumerated item list
is not.

The authoritative statement of what exists and at what level is
`certification/ENGINE_CAPABILITY_INVENTORY.json`, which was compiled by reading the repository
rather than its documents. The table below summarises it and does not replace it. Where the two
disagree, the inventory governs and the disagreement is a defect to be reported.

| Area | State | Evidence |
|---|---|---|
| Repository foundation and governing skeletons | DONE 2026-07-11 | Phase 0 commit |
| Tier-0 astronomical kernel, both ratified profiles | **FORMALLY LOCKED, 2026-08-13.** All four Constitution s12 conditions verified individually in ADR-0034. Scope is the kernel and the certified D9/D10 mathematics ONLY. Changes inside that scope now require a formal change decision, regression, independent validation, recertification and a further ADR | ADR-0005, **owner-ratified**; ADR-0034 (four-condition verification); ADR-0031 (same-run evidence); ADR-0032 (ephemeris integrity); `certification/CURRENT_ENGINE_LOCK.json`; `certification/current_engine_certification.json` and `reports/certification/current_engine.report.md`, same-run and byte-agreeing; 528 comparisons against bundled swetest 2.10.03, max error 0.000180 arcsec |
| D1, D9, D10 | CERTIFIED. D9 and D10 by dedicated modules, never via the registry | Inside the ADR-0005 Tier-0 lock scope, which covers the kernel and D9/D10 only |
| KP lordship chain and fact charts | CERTIFIED, chains and fact charts only | ADR-0006; `certification/KP_CHAIN_V1_certification.json`; `docs/KP_CHAIN_SPEC.md` non-claims |
| Vimshottari maha and antar | CERTIFIED. Pratyantar PARTIALLY CERTIFIED | ADR-0007; `certification/VIMSHOTTARI_V1_certification.json` |
| Transit longitude-crossing primitive | CERTIFIED. Ingresses PARTIALLY CERTIFIED | ADR-0008; `certification/TRANSIT_V1_certification.json` |
| Generic varga framework and D3 | Framework PARTIALLY CERTIFIED; D3 CERTIFIED. **ADR-0009 owner-ratified 2026-08-13** | ADR-0009, **owner-ratified** (ADR-0035); `certification/VARGA_D3_V1_certification.json`. Infrastructure is not certification of any individual varga |
| D12 | CERTIFIED. **ADR-0010 owner-ratified 2026-08-13** | ADR-0010, **owner-ratified** (ADR-0035); `certification/VARGA_D12_V1_certification.json` |
| D7, D30, D2 | CERTIFIED. **ADR-0011 owner-ratified 2026-08-13.** D7 carries an owner-accepted ULP finding: its 30/7-degree widths are not binary-representable | ADR-0011, **owner-ratified** (ADR-0035); the three matching `certification/VARGA_*_V1_certification.json` artifacts |
| Parashari graha drishti and sign-convention enforcement | CERTIFIED | ADR-0012; `certification/PARASHARI_DRISHTI_V1_certification.json`; `certification/SIGN_CONVENTION_V1_certification.json` |
| Oracle reproducibility and CI tiering (G6) | Oracle reproducibility CERTIFIED; CI jobs IMPLEMENTED | ADR-0018 and its evidence addendum; `certification/ORACLE_ENVIRONMENT.json`; `certification/G6_REMOTE_CI_VALIDATION.json` |
| Retired-identifier enforcement (B-3) | CLOSED, mechanically enforced with a negative control | ADR-0014; `scripts/check_retired_identifiers.py` |
| Governance reconciliation of the ADR-0013 conflicts | DRAFTED, unratified | ADR-0022 through ADR-0027, all PROPOSED |
| Owner ratification checkpoint | **ACCEPTED 2026-08-13** | ADR-0033: governance roles (Q1, in part), ADR-0001 and ADR-0002 ratified as written (Q13), roadmap direction ratified (Q8, direction only) |
| Tier-0 formal lock | **ACCEPTED 2026-08-13** | ADR-0034: ADR-0005 ratified; all four s12 conditions verified; Tier-0 is the first artifact in the repository to satisfy the constitution's definition of Locked |
| Registry varga ratification | **ACCEPTED 2026-08-13** | ADR-0035: ADR-0009, ADR-0010 and ADR-0011 ratified as written. D2, D3, D7, D12, D30 owner-ratified CERTIFIED. **Not Locked**, and ADR-0012, which fixes their sign convention, is still PROPOSED |

**Not complete, despite adjacent certification.** D4, D16, D20, D24, D27, D40, D45 and D60 are
ABSENT, not merely uncertified. Deeper dasha levels and every other dasha system are absent. KP
significators, four-step, ruling planets and horary are absent. Jaimini, BNN/Nadi, CIL, Umang Taneja
Nakshatra Nadi, numerology and Lal Kitab are absent. Shadbala and yogas are absent. Panchanga is
absent except for nakshatra. Sunrise, sunset and the derived inauspicious periods are absent, and
ADR-0020 D2 places them at Tier-0, **not** covered by the existing ADR-0005 lock, which is not
retroactively widened. Placidus houses are exercised only to 64.1 degrees north, so polar behaviour
is undefined. Every product layer from the event model through convergence is SPECIFIED only.

## 2. Currently authorised work

| Item | Authorised by | Boundary |
|---|---|---|
| Governance and documentation reconciliation | Current CEO direction | No new product, astrology, convergence, evidence, API, UI, ML or calculation functionality. No weakening of validation gates. No change to certified numerical behaviour. |

**Nothing else is authorised.** In particular, and stated because each has been discussed and none
has been approved: the ADR numbering CI fix; audit findings B-01, B-02, B-03, H-02, H-03 and H-04;
KP significators, four-step, ruling planets and horary (ADR-0027 D2); panchanga and rise/set
(DP-009 is a decision paper, not a decision); the convergence algorithm
(`docs/EVIDENCE_INDEPENDENCE_DESIGN.md` prohibits implementation on its strength); BTR; and any
Muhurta, Varshaphal, Prashna or Mundane capability.

## 3. Future work, in the OWNER-RATIFIED dependency order

**RATIFIED BY THE OWNER, Prashant Kumar, 2026-08-13 (ADR-0033 D3).** This is the first
owner-ratified content in this document, and it is the ordering only.

> Foundation and Certification -> Question and Input Architecture -> Knowledge and Rule Architecture
> -> Dependency and Inference Architecture -> Evidence Architecture -> System-specific
> Interpretation -> Convergence -> Historical Validation and Learning -> API -> UI and Production

**Five ratified qualifications, which bind as strongly as the ordering itself:**

1. **The ordering is dependency guidance, NOT automatic implementation authorisation.** Nothing here
   permits work to begin. Authorisation remains a separate owner act, per section 0.
2. Existing certified astrology foundation work remains **valid historical foundation work**.
3. Astrology systems remain **independently implemented and independently evaluated**.
4. Convergence MUST preserve **provenance, dependency, correlation and uncertainty**.
5. **Structurally different domains MUST NOT be forced through one natal pipeline.**

The table below maps that ordering to the prerequisites each phase actually has. The prerequisites
are engineering fact and are **not** part of the ratification.

| # | Ratified phase | Principal prerequisite |
|---|---|---|
| 1 | Foundation and Certification | In progress. Q1 named an owner on 2026-08-13, so ratification is now possible; per-entry ratification is almost entirely outstanding |
| 2 | Question and Input Architecture | Entity model H0; entity identifier family, still open per DP-008 |
| 3 | Knowledge and Rule Architecture | Q4 HLKG/AKG scope, open |
| 4 | Dependency and Inference Architecture | Items 2 and 3 |
| 5 | Evidence Architecture | H4; provenance completeness, which audit findings M-04, M-05 and M-09 currently block |
| 6 | System-specific Interpretation | H5 rule registry; per-system rule sourcing |
| 7 | Convergence | Item 5 complete; the independence design ratified; provenance graph recorded at evidence-creation time; qualification 4 above |
| 8 | Historical Validation and Learning | H2 ledger; protected holdouts; multiple-comparison discipline |
| 9 | API | Everything it would expose being certified |
| 10 | UI and Production | Item 9 |

**Q8 is not closed by this ratification.** The direction is ratified; the per-phase prerequisites,
entry criteria, scope, certification gates, exit criteria and approval requirements are not. Until
those exist and are ratified, no phase can be declared entered or exited by criteria. Q8's status is
**OWNER-RATIFIED DIRECTION, FULL RESOLUTION STILL OPEN.**

Astrology system implementation remains modular and school-isolated throughout. Muhurta,
Varshaphal, Prashna and Mundane remain separate domain architectures and are **not** forced through
a natal pipeline (ADR-0019, ADR-0020, ADR-0026 D4).

Certification-track work runs alongside rather than inside this order:
`docs/VARGA_CERTIFICATION_ROADMAP.md` and `docs/DASHA_CERTIFICATION_ROADMAP.md`. Both state orders
and neither authorises implementation.

## 4. Prerequisites that currently gate almost everything

| Gate | Effect while unmet |
|---|---|
| Q1, named owners | **PARTLY CLEARED 2026-08-13.** An owner exists, so ratification is possible. Three entries are Accepted: ADR-0001, ADR-0002, ADR-0033. Everything else remains PROPOSED, and the docs, engine and release owner roles are still undesignated. |
| Q7, repository license | Legal viability of commercial deployment is undetermined, given AGPL-3.0 upstream dependencies |
| Q8 closure criteria | No phase can be declared entered or exited by criteria, because no ratified criteria exist |
| Provenance completeness | Blocks the evidence model, and therefore convergence. G1 audit M-04, M-05, M-09 |
| Three BLOCKER and eight HIGH audit findings | Recorded in `reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`, unfixed by instruction |
| CI governance job RED on remote | The gate itself is failing on ADR numbering. Fix proposed, not approved |

## 5. Horizon overview

The table below is a *structural template*, not a committed plan. Phase names and sequence await Q8.

| Phase | Name | Entry criteria | Exit criteria (evidence) | Status |
|---|---|---|---|---|
| 0 | Repository foundation | - | Structure + governing skeletons merged | DONE 2026-07-11 |
| 1 | TBD (see section 3, dependency order) | TBD, awaiting Q8 | TBD, awaiting Q8 | NOT STARTED |
| 2 | TBD | TBD | TBD | NOT STARTED |

## 6. Milestone register
| ID | Milestone | Target | Depends on | Evidence link |
|---|---|---|---|---|
| M-000 | Foundation skeleton | 2026-07-11 | - | Phase 0 commit |

## 7. Out of scope (standing)

TBD - explicit non-goals to protect the 10-year maintenance budget. One standing non-goal is already
recorded elsewhere and is repeated here because it is the most important: the project does not claim
and will not claim that astrology itself has been scientifically validated because software
calculations are correct. C4 production certification MUST NEVER be represented as C5 prediction
validation.

## 8. Risk register (top items only)
| ID | Risk | Impact | Mitigation | Owner |
|---|---|---|---|---|
| R-001 | Foundational ambiguities resolved by assumption instead of decision | Architecture drift | OPEN_QUESTIONS.md discipline; PR checklist | TBD |
| R-002 | Certification badges read as product readiness | Premature confidence; unsupported external claims | Section 0 of this document; ADR-0026 D2 | TBD |
| R-003 | Q1 unresolved indefinitely, so the ADR register accumulates PROPOSED entries that are followed in practice as if ratified | Governance becomes decorative | Status vocabulary in OPEN_QUESTIONS.md; this row | TBD |

## 9. Change history
| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Skeleton created |
| 0.2.0 | 2026-08-11 | ADR-0026 D5: separated completed historical work, currently authorised work, future dependency order and prerequisite gates. Original horizon, milestone, out-of-scope and risk sections retained and renumbered to 5 through 8. No phase marked complete without evidence. Does not close Q8. |
| 0.3.0 | 2026-08-13 | ADR-0033 D3: section 3 replaced by the owner-ratified dependency ordering and its five binding qualifications. Q1 gate row updated to reflect partial clearance. Q8 remains open as to per-phase criteria. No other section is ratified. |
| 0.4.0 | 2026-08-13 | ADR-0034: Tier-0 row corrected from "reported" to FORMALLY LOCKED after owner ratification of ADR-0005 satisfied s12 condition 4. Lock scope restated as kernel plus certified D9/D10 only. No numerical value changed. |
| 0.5.0 | 2026-08-13 | ADR-0035: varga rows annotated as owner-ratified. Recorded that they are CERTIFIED, not Locked, and that ADR-0012, which defines their sign convention, remains PROPOSED. No numerical value changed. |
