| Field | Value |
|---|---|
| Status | DRAFT - PROPOSED batch, pending ratification gates (see Lifecycle Position) |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | docs/HLKG_CONSTITUTION.md, docs/DOMAIN_REGISTRY_SPEC.md, docs/QUESTION_REGISTRY_SPEC.md, docs/CANONICAL_QUESTION_SCHEMA.md, knowledge/hlkg/domains/career/CAREER_DOMAIN_MODEL.md v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_QUESTION_LIBRARY.md |
| Machine verification | 61 records: slug regex + 3-segment + aspect<=30 + label rules + ID/slug uniqueness + one-class-per-question: PASS. 10 relationship edges: targets exist, RELATES_TO rationale present, REFINES/PRECEDES/DEPENDS_ON acyclic: PASS. One defect (32-char aspect) caught and fixed pre-release. |

# Career Question Library

61 candidate canonical Questions for the `career` domain, generated strictly from the
Career Domain Model's frozen topic vocabulary. This is the human-readable source library;
it contains no astrology and no prediction logic.

## Lifecycle Position (read first)

Per the locked specifications these records are a **PROPOSED batch**, not CANONICAL:
CANONICAL requires domain ratification (CDQ-1/DQ-1), duplicate Gates 1-2, adjudication and
- for QUALITY records - ratified scales (CDQ-5). Per M2.4 Import Rules, canonical IDs are
issued only by the registry at import; the IDs below are a **proposed reserved block
(HLKG-N-000401..000461)** to be confirmed or reissued by the registry issuer. Nothing in
this document may be cited as canonical until those gates pass.

## Batch Conventions (defaults; per-record entries list only deltas)

- **Domain:** all records `career` (HLKG-D-001 placeholder pending ratification).
- **Slug:** `career.<subdomain>.<aspect>`; subdomain from the frozen 12-topic vocabulary.
- **Parameters:** every record declares `subject` (kind subject, required). Every
  OCCURRENCE record additionally declares `horizon` (required). Every TIMING record
  declares `horizon` (optional). SELECTION records declare `option_set` (required).
  Extra parameters are listed per record.
- **Answer Contract:** determined by class per QUESTION_REGISTRY_SPEC s.7:

  - TIMING: Timeline Object (intervals + declared precision; empty = not indicated within scope)
  - OCCURRENCE: {value: yes/no/not_established, horizon (mandatory), qualifier?}
  - QUALITY: Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
  - SELECTION: Selection among options bound at query time (option_set parameter)
  - QUANTITY: {value/range, unit, basis_note}
  - DESCRIPTION: Structured Narrative (facets + summary)
  - CAUSAL: {factors[], explanation, counterfactual_note?}
- **Aliases:** listed forms are locale `en` unless tagged; all illustrative intake
  evidence, normalised at import (Gate 1 applies).
- **Validation notes:** boundary references cite CAREER_DOMAIN_MODEL.md s.4.
- **Composites:** never nodes; see Composite Decomposition Patterns section.


## Subdomain `employment` (7 questions)

### 1. HLKG-N-000401 - `career.employment.first_job_timing`
- **Human Question:** When is first employment likely to begin?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I get my first job?" | "Naukri kab lagegi? (hi-Latn)"
- **Relationships:** `PRECEDES` -> HLKG-N-000420 (`career.advancement.promotion_timing`)

### 2. HLKG-N-000402 - `career.employment.job_occurrence`
- **Human Question:** Will employment be obtained within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get a job?" | "Will I find work this year?"
- **Relationships:** target of `REFINES` from HLKG-N-000406 (`career.employment.government_job_occurrence`); target of `PRECEDES` from HLKG-N-000407 (`career.employment.offer_occurrence`)

### 3. HLKG-N-000403 - `career.employment.job_loss_occurrence`
- **Human Question:** Will loss of employment occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I lose my job?" | "Is my job at risk?"
- **Relationships:** target of `DEPENDS_ON` from HLKG-N-000404 (`career.employment.reemployment_timing`)

### 4. HLKG-N-000404 - `career.employment.reemployment_timing`
- **Human Question:** When is re-employment after a loss of employment likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I get a job again?"
- **Relationships:** `DEPENDS_ON` -> HLKG-N-000403 (`career.employment.job_loss_occurrence`)

### 5. HLKG-N-000405 - `career.employment.job_security`
- **Human Question:** How secure is the current employment?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "How safe is my job?"

### 6. HLKG-N-000406 - `career.employment.government_job_occurrence`
- **Human Question:** Will government employment be obtained within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get a government job?" | "Sarkari naukri milegi? (hi-Latn)"
- **Relationships:** `REFINES` -> HLKG-N-000402 (`career.employment.job_occurrence`)
- **Validation Notes:** Appointment is Career; the qualifying examination itself is Education (boundary 4.2).

### 7. HLKG-N-000407 - `career.employment.offer_occurrence`
- **Human Question:** Will an employment offer be received within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get the offer?"
- **Relationships:** `PRECEDES` -> HLKG-N-000402 (`career.employment.job_occurrence`)


## Subdomain `profession` (5 questions)

### 8. HLKG-N-000408 - `career.profession.vocation_direction`
- **Human Question:** Which of the declared vocational directions fits best?
- **Class / Contract:** SELECTION -> Selection among options bound at query time (option_set parameter)
- **Parameters:** subject (required), option_set (required)
- **Aliases:** "Which career field suits me?" | "What line of work should I choose among these?"

### 9. HLKG-N-000409 - `career.profession.change_occurrence`
- **Human Question:** Will a change of profession occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I change my field?"

### 10. HLKG-N-000410 - `career.profession.change_timing`
- **Human Question:** When is a change of profession likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I switch careers?"

### 11. HLKG-N-000411 - `career.profession.fit_quality`
- **Human Question:** How well does the current profession fit the subject?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Am I in the right profession?"

### 12. HLKG-N-000412 - `career.profession.practice_establishment_timing`
- **Human Question:** When is an independent professional practice likely to be established?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When can I start my own practice?"


## Subdomain `business` (7 questions)

### 13. HLKG-N-000413 - `career.business.start_timing`
- **Human Question:** When is a business venture likely to start?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When can I start my own business?" | "Business kab shuru hoga? (hi-Latn)"
- **Relationships:** `PRECEDES` -> HLKG-N-000417 (`career.business.expansion_timing`)

### 14. HLKG-N-000414 - `career.business.start_occurrence`
- **Human Question:** Will a business venture start within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I start a business?"

### 15. HLKG-N-000415 - `career.business.venture_viability`
- **Human Question:** How viable is the stated business venture as a working enterprise?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Will my business do well?"
- **Validation Notes:** Venture-as-activity only; wealth outcomes belong to finance (boundary 4.1).

### 16. HLKG-N-000416 - `career.business.closure_occurrence`
- **Human Question:** Will closure of the stated business occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will my business shut down?"

### 17. HLKG-N-000417 - `career.business.expansion_timing`
- **Human Question:** When is expansion of the stated business likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will my business grow?"
- **Relationships:** target of `PRECEDES` from HLKG-N-000413 (`career.business.start_timing`)

### 18. HLKG-N-000418 - `career.business.sale_occurrence`
- **Human Question:** Will a sale or exit of the stated business occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I sell my company?"

### 19. HLKG-N-000419 - `career.business.partnership_occurrence`
- **Human Question:** Will a business partnership form within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get a business partner?"
- **Validation Notes:** Partnership in the venture; personal partnerships belong to relationship.


## Subdomain `advancement` (6 questions)

### 20. HLKG-N-000420 - `career.advancement.promotion_timing`
- **Human Question:** When is a promotion likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I get promoted?" | "Promotion kab hoga? (hi-Latn)"
- **Relationships:** target of `PRECEDES` from HLKG-N-000401 (`career.employment.first_job_timing`)

### 21. HLKG-N-000421 - `career.advancement.promotion_occurrence`
- **Human Question:** Will a promotion occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get promoted this year?"
- **Relationships:** target of `RELATES_TO` from HLKG-N-000422 (`career.advancement.leadership_occurrence`)

### 22. HLKG-N-000422 - `career.advancement.leadership_occurrence`
- **Human Question:** Will a leadership role be attained within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I become a manager?" | "Will I reach a leadership position?"
- **Relationships:** `RELATES_TO` -> HLKG-N-000421 (`career.advancement.promotion_occurrence`) - rationale: Leadership attainment often but not necessarily arrives via promotion; neither refines the other.

### 23. HLKG-N-000423 - `career.advancement.leadership_timing`
- **Human Question:** When is a leadership role likely to be attained?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I lead a team?"

### 24. HLKG-N-000424 - `career.advancement.trajectory_description`
- **Human Question:** What is the likely trajectory of career advancement?
- **Class / Contract:** DESCRIPTION -> Structured Narrative (facets + summary)
- **Parameters:** subject (required)
- **Aliases:** "How will my career progress?"

### 25. HLKG-N-000425 - `career.advancement.stagnation_cause`
- **Human Question:** What factors underlie stagnation in career advancement?
- **Class / Contract:** CAUSAL -> {factors[], explanation, counterfactual_note?}
- **Parameters:** subject (required)
- **Aliases:** "Why am I not getting promoted?"


## Subdomain `transition` (7 questions)

### 26. HLKG-N-000426 - `career.transition.job_change_timing`
- **Human Question:** When is a change of job likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I change my job?"

### 27. HLKG-N-000427 - `career.transition.job_change_occurrence`
- **Human Question:** Will a change of job occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I switch jobs?"

### 28. HLKG-N-000428 - `career.transition.job_change_count`
- **Human Question:** How many changes of employer are indicated within the stated horizon?
- **Class / Contract:** QUANTITY -> {value/range, unit, basis_note}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "How many times will I change jobs?"

### 29. HLKG-N-000429 - `career.transition.career_change_occurrence`
- **Human Question:** Will a change of career occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I change my career completely?"

### 30. HLKG-N-000430 - `career.transition.career_break_occurrence`
- **Human Question:** Will a career break occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I take a break from work?"
- **Relationships:** target of `DEPENDS_ON` from HLKG-N-000431 (`career.transition.reentry_timing`)

### 31. HLKG-N-000431 - `career.transition.reentry_timing`
- **Human Question:** When is re-entry into working life after a career break likely?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I return to work after my break?"
- **Relationships:** `DEPENDS_ON` -> HLKG-N-000430 (`career.transition.career_break_occurrence`)

### 32. HLKG-N-000432 - `career.transition.second_career_occurrence`
- **Human Question:** Will a second career begin within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I start a new career later in life?"


## Subdomain `workplace` (4 questions)

### 33. HLKG-N-000433 - `career.workplace.environment_quality`
- **Human Question:** How favourable is the working environment expected to be?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Is my work environment good?"
- **Relationships:** target of `RELATES_TO` from HLKG-N-000455 (`career.satisfaction.career_quality`)

### 34. HLKG-N-000434 - `career.workplace.conflict_occurrence`
- **Human Question:** Will workplace conflict occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I have problems with my boss?"
- **Validation Notes:** Conflict as a work matter; legal proceedings belong to legal, romance to relationship.

### 35. HLKG-N-000435 - `career.workplace.conflict_resolution_timing`
- **Human Question:** When is resolution of the stated workplace conflict likely?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will my office problems end?"

### 36. HLKG-N-000436 - `career.workplace.relations_quality`
- **Human Question:** How favourable are working relations with colleagues and superiors expected to be?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Will my boss support me?"


## Subdomain `performance` (5 questions)

### 37. HLKG-N-000437 - `career.performance.recognition_occurrence`
- **Human Question:** Will professional recognition be received within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get an award at work?" | "Will my work be recognised?"

### 38. HLKG-N-000438 - `career.performance.recognition_timing`
- **Human Question:** When is professional recognition likely to be received?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I get credit for my work?"

### 39. HLKG-N-000439 - `career.performance.appraisal_quality`
- **Human Question:** How favourable is the upcoming appraisal outcome expected to be?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Will my appraisal go well?"

### 40. HLKG-N-000440 - `career.performance.field_standing_quality`
- **Human Question:** How strong is professional standing within the subject's field expected to be?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Will I be respected in my field?"
- **Validation Notes:** Audience test (boundary 4.7): within-field standing is Career; public fame is reputation.

### 41. HLKG-N-000441 - `career.performance.setback_cause`
- **Human Question:** What factors underlie repeated professional setbacks?
- **Class / Contract:** CAUSAL -> {factors[], explanation, counterfactual_note?}
- **Parameters:** subject (required)
- **Aliases:** "Why do I keep failing at work?"


## Subdomain `skill` (3 questions)

### 42. HLKG-N-000442 - `career.skill.adequacy_quality`
- **Human Question:** How adequate are current skills for the stated career goal?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Are my skills enough for this role?"

### 43. HLKG-N-000443 - `career.skill.demand_description`
- **Human Question:** What is the demand outlook for the declared skill set in professional application?
- **Class / Contract:** DESCRIPTION -> Structured Narrative (facets + summary)
- **Parameters:** subject (required)
- **Aliases:** "Are my skills in demand?"

### 44. HLKG-N-000444 - `career.skill.upskilling_direction`
- **Human Question:** Which of the declared upskilling paths best serves the stated career goal?
- **Class / Contract:** SELECTION -> Selection among options bound at query time (option_set parameter)
- **Parameters:** subject (required), option_set (required)
- **Aliases:** "Which course should I do for my career among these?"
- **Validation Notes:** Career use of learning; the study/qualification itself is Education (boundary 4.2).


## Subdomain `assignment` (5 questions)

### 45. HLKG-N-000445 - `career.assignment.foreign_posting_occurrence`
- **Human Question:** Will a work posting abroad occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I go onsite?" | "Will I get a foreign posting?"
- **Relationships:** target of `DEPENDS_ON` from HLKG-N-000449 (`career.assignment.posting_return_timing`)

### 46. HLKG-N-000446 - `career.assignment.foreign_posting_timing`
- **Human Question:** When is a work posting abroad likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I go abroad for work?"

### 47. HLKG-N-000447 - `career.assignment.transfer_occurrence`
- **Human Question:** Will a transfer of work location occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get transferred?"

### 48. HLKG-N-000448 - `career.assignment.transfer_timing`
- **Human Question:** When is a transfer of work location likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When is my transfer due?"

### 49. HLKG-N-000449 - `career.assignment.posting_return_timing`
- **Human Question:** When is return from the current work posting likely?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I come back from onsite?"
- **Relationships:** `DEPENDS_ON` -> HLKG-N-000445 (`career.assignment.foreign_posting_occurrence`)


## Subdomain `compensation` (5 questions)

### 50. HLKG-N-000450 - `career.compensation.raise_occurrence`
- **Human Question:** Will a salary increase occur within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I get a raise?" | "Increment milega? (hi-Latn)"

### 51. HLKG-N-000451 - `career.compensation.raise_timing`
- **Human Question:** When is a salary increase likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will my salary increase?"

### 52. HLKG-N-000452 - `career.compensation.income_growth_quality`
- **Human Question:** How strong is professional income growth expected to be?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Will my earnings from work grow well?"
- **Validation Notes:** Compensation attached to work only; wealth belongs to finance (boundary 4.1, CDQ-6).

### 53. HLKG-N-000453 - `career.compensation.level_quantity`
- **Human Question:** What level of professional income is indicated for the stated period?
- **Class / Contract:** QUANTITY -> {value/range, unit, basis_note}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "How much will I earn from my job?"
- **Validation Notes:** Answer carries unit and basis note per QUANTITY contract.

### 54. HLKG-N-000454 - `career.compensation.stagnation_cause`
- **Human Question:** What factors underlie stagnation of professional income?
- **Class / Contract:** CAUSAL -> {factors[], explanation, counterfactual_note?}
- **Parameters:** subject (required)
- **Aliases:** "Why is my salary not increasing?"


## Subdomain `satisfaction` (3 questions)

### 55. HLKG-N-000455 - `career.satisfaction.career_quality`
- **Human Question:** How satisfying is the subject's working life expected to be?
- **Class / Contract:** QUALITY -> Rating Object vs a DECLARED scale (scale artifacts pending CDQ-5)
- **Parameters:** subject (required); scale: DECLARED (pending CDQ-5)
- **Aliases:** "Will I be happy in my career?"
- **Relationships:** `RELATES_TO` -> HLKG-N-000433 (`career.workplace.environment_quality`) - rationale: Frequent co-signal in user intent; recorded for intake routing analytics only.
- **Validation Notes:** Career appraisal only; wellbeing states belong to health (boundary 4.5).

### 56. HLKG-N-000456 - `career.satisfaction.dissatisfaction_cause`
- **Human Question:** What factors underlie dissatisfaction with the subject's working life?
- **Class / Contract:** CAUSAL -> {factors[], explanation, counterfactual_note?}
- **Parameters:** subject (required)
- **Aliases:** "Why am I unhappy at work?"

### 57. HLKG-N-000457 - `career.satisfaction.improvement_timing`
- **Human Question:** When is satisfaction with working life likely to improve?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will things get better at work?"


## Subdomain `exit` (4 questions)

### 58. HLKG-N-000458 - `career.exit.retirement_timing`
- **Human Question:** When is retirement from working life likely to occur?
- **Class / Contract:** TIMING -> Timeline Object (intervals + declared precision; empty = not indicated within scope)
- **Parameters:** subject (required), horizon (optional)
- **Aliases:** "When will I retire?"
- **Relationships:** target of `DEPENDS_ON` from HLKG-N-000460 (`career.exit.postretirement_work_occurrence`)

### 59. HLKG-N-000459 - `career.exit.early_retirement_occurrence`
- **Human Question:** Will retirement occur earlier than the stated expected point?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I retire early?"
- **Validation Notes:** Horizon binds the 'expected point'; pension adequacy belongs to finance.

### 60. HLKG-N-000460 - `career.exit.postretirement_work_occurrence`
- **Human Question:** Will professional activity resume after retirement within the stated horizon?
- **Class / Contract:** OCCURRENCE -> {value: yes/no/not_established, horizon (mandatory), qualifier?}
- **Parameters:** subject (required), horizon (required)
- **Aliases:** "Will I work after retirement?"
- **Relationships:** `DEPENDS_ON` -> HLKG-N-000458 (`career.exit.retirement_timing`)

### 61. HLKG-N-000461 - `career.exit.career_end_description`
- **Human Question:** What is the likely character of the final phase of working life?
- **Class / Contract:** DESCRIPTION -> Structured Narrative (facets + summary)
- **Parameters:** subject (required)
- **Aliases:** "How will my career end?"

## Composite Decomposition Patterns (patterns own no identity)

Recurring compound user utterances and their decompositions - each resolves to multiple
Query targets, never to a node:

| Composite phrasing (evidence) | Decomposes to |
|---|---|
| "Will I get promoted, and when?" | advancement.promotion_occurrence + advancement.promotion_timing |
| "Will I go abroad for work and settle there?" | assignment.foreign_posting_occurrence + (residence settlement Question - other domain) |
| "Should I quit and start a business, and will it work?" | profession.vocation_direction (options bound) + business.venture_viability |
| "When will I change jobs and will my salary grow?" | transition.job_change_timing + compensation.income_growth_quality |
| "Will I lose my job, and when will I find a new one?" | employment.job_loss_occurrence + employment.reemployment_timing |
| "When will I retire and will I work afterwards?" | exit.retirement_timing + exit.postretirement_work_occurrence |

## Batch Validation Summary

- Class distribution: TIMING 18, OCCURRENCE 22, QUALITY 10, SELECTION 2, QUANTITY 2,
  DESCRIPTION 3, CAUSAL 4 (total 61 - within the 50-75 mandate).
- Every subdomain of the frozen 12-topic vocabulary is populated (min 3, max 7).
- TIMING/OCCURRENCE siblings are deliberately distinct nodes (QRS s.8 rule 4) and are
  NOT auto-linked; only adjudicated edges are recorded.
- All 10 QUALITY records are **CANONICAL-blocked until CDQ-5 scales ratify** (Domain
  Model checklist); they may progress to REVIEW meanwhile.
- No EXCLUDES edges: none justified; EXCLUDES is never forced (constitutional note).
- Duplicate Gate 1 pre-check within batch: all normalised labels/aliases unique (machine-
  verified); graph-wide Gate 1/2 runs at import against the live registry.

## OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| CQL-1 | Confirmation or reissue of the reserved ID block HLKG-N-000401..000461 by the registry issuer | Citable IDs |
| CQL-2 | Adjudication of the two RELATES_TO edges (routing-analytics rationale acceptable?) | Edges at REVIEW |
| CQL-3 | hi-Latn alias treatment: locale tag for romanised Hindi (`hi-Latn` proposed, unratified against HQ-5) | Alias import |
| CQL-4 | Whether `compensation.level_quantity` survives the CDQ-6 (career vs finance) concurrence | Record 53's domain placement |
| Inherited | CDQ-1..6, DQ-1, HQ-5, QQ-2 | as recorded previously |

## Self-Audit Record (performed before finalisation)

1. **Machine checks executed, not assumed:** slug regex/3-segment/aspect-length, ID and
   slug uniqueness, label form (<=120, ends '?'), one class per record, relationship
   target existence, RELATES_TO rationale presence, acyclicity of REFINES/PRECEDES/
   DEPENDS_ON - ALL PASS. One genuine defect found and fixed: aspect
   `partnership_formation_occurrence` (32 chars) violated the 30-char rule -> renamed
   `partnership_occurrence`.
2. **Boundary sweep:** every record touching a Domain Model hard boundary (4.1 money,
   4.2 education, 4.5 health, 4.7 reputation) carries an explicit validation note; no
   record answers in another domain's locus.
3. **Granularity sweep:** no record's honest answer spans two classes; compound intents
   found during drafting were pushed into the Composite Patterns table instead of nodes.
4. **Restraint check:** leadership_occurrence was initially drafted as REFINES
   promotion_occurrence - rejected on review (leadership is not a strict subset of
   promotion) and downgraded to RELATES_TO with rationale; recorded here as precedent.
5. **Known limitations left open, not papered over:** IDs provisional (CQL-1); QUALITY
   scales absent (CDQ-5); reciprocity with neighbour domains unclosed (CDQ-2); the batch
   is PROPOSED and says so at the top.
