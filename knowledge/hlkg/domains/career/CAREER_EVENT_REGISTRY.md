| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification; 5 events are PROPOSED-ADDITIONS to the Domain Model taxonomy (Model s.13 vocabulary append) |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | CAREER_DOMAIN_MODEL.md v0.1.0 s.7 (source taxonomy), docs/HLKG_CONSTITUTION.md, docs/QUESTION_REGISTRY_SPEC.md, CAREER_QUESTION_LIBRARY.md v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_EVENT_REGISTRY.md |
| Machine verification | 47 events, 10 groups: unique IDs and names, all classes from the closed 7-class registry, every linked question slug exists in career.questions.json. Coverage computed both directions: 44/61 questions event-anchored; 17 legitimately state/outcome-anchored; 16 events currently have zero questions (coverage gap ledger, s.5). ALL CHECKS PASS. |

# Career Event Registry

Formalises the Domain Model's event taxonomy (s.7) into an identified, linkable registry.
**Events are knowledge vocabulary, not Questions and not nodes**: they name the happenings
that TIMING/OCCURRENCE aspects are built from, anchor the aspect segment vocabulary, and
serve as the coverage ledger for future question generation. No prediction semantics
attach to any event.

## 1. ID Scheme

`EV-CAR-NNN`, zero-padded, monotone, immutable, never reused - **domain-local** identifiers.
Whether event IDs become an HLKG-wide registry family (HLKG-EV-...) shared across domains
(e.g., relocation events appearing in residence and career) is deliberately unratified
(EVR-1); domain-local IDs migrate cleanly under either outcome.

## 2. Record Shape

Each event: ID | name (snake_case, unique, collision-checked against subdomain and outcome
vocabularies) | group (one of the 10 Domain Model groups) | one-line description |
applicable question classes (from the closed 7-class registry - which classes can
meaningfully anchor on this event) | linked existing Questions | origin (MODEL = Domain
Model s.7 verbatim; PROPOSED-ADDITION = appended by this registry, pending Model v0.2.0
ratification).


## 3.1 Group: Entry (4 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-001 | `first_employment` | Subject begins their first employment. | TIMING, OCCURRENCE | `employment.first_job_timing` | MODEL |
| EV-CAR-002 | `workforce_reentry` | Subject returns to working life after a break or loss. | TIMING, OCCURRENCE | `employment.reemployment_timing`<br>`transition.reentry_timing` | MODEL |
| EV-CAR-043 | `employment_obtained` | Subject obtains employment (general hiring event, any ordinal). | TIMING, OCCURRENCE | `employment.job_occurrence`<br>`employment.government_job_occurrence` | PROPOSED-ADDITION |
| EV-CAR-044 | `offer_received` | A formal employment offer is received. | OCCURRENCE | `employment.offer_occurrence` | PROPOSED-ADDITION |

## 3.2 Group: Progression (5 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-003 | `promotion` | Subject is elevated to a higher role or grade with the same employer. | TIMING, OCCURRENCE, CAUSAL | `advancement.promotion_timing`<br>`advancement.promotion_occurrence`<br>`advancement.stagnation_cause` | MODEL |
| EV-CAR-004 | `grade_rise` | Formal seniority/grade increase without a role change. | TIMING, OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-005 | `scope_expansion` | Responsibilities broaden materially within the current role. | OCCURRENCE, DESCRIPTION | *(none yet - gap)* | MODEL |
| EV-CAR-006 | `leadership_appointment` | Subject is appointed to a leadership role. | TIMING, OCCURRENCE | `advancement.leadership_timing`<br>`advancement.leadership_occurrence` | MODEL |
| EV-CAR-007 | `pay_raise` | Compensation attached to current work increases. | TIMING, OCCURRENCE, CAUSAL | `compensation.raise_timing`<br>`compensation.raise_occurrence`<br>`compensation.stagnation_cause` | MODEL |

## 3.3 Group: Lateral (6 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-008 | `role_change` | Role changes within the same employer, no elevation implied. | TIMING, OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-009 | `employer_change` | Subject moves to a different employer in the same profession. | TIMING, OCCURRENCE, QUANTITY | `transition.job_change_timing`<br>`transition.job_change_occurrence`<br>`transition.job_change_count` | MODEL |
| EV-CAR-010 | `transfer` | Work location changes within the same employer. | TIMING, OCCURRENCE | `assignment.transfer_timing`<br>`assignment.transfer_occurrence` | MODEL |
| EV-CAR-011 | `secondment` | Temporary placement with another unit or organisation. | TIMING, OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-012 | `foreign_posting` | Work-purposed placement abroad. | TIMING, OCCURRENCE | `assignment.foreign_posting_timing`<br>`assignment.foreign_posting_occurrence` | MODEL |
| EV-CAR-013 | `posting_return` | Return from a work posting to the base location. | TIMING | `assignment.posting_return_timing` | MODEL |

## 3.4 Group: Reorientation (4 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-014 | `profession_change` | Subject changes their line of work. | TIMING, OCCURRENCE | `profession.change_timing`<br>`profession.change_occurrence`<br>`transition.career_change_occurrence` | MODEL |
| EV-CAR-015 | `industry_change` | Subject changes the sector they work in, profession retained. | TIMING, OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-016 | `employment_mode_switch` | Switch between employed and self-employed/practice modes. | TIMING, OCCURRENCE | `profession.practice_establishment_timing` | MODEL |
| EV-CAR-045 | `second_career_start` | A distinct later-life career commences. | OCCURRENCE, TIMING | `transition.second_career_occurrence` | PROPOSED-ADDITION |

## 3.5 Group: Separation (4 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-017 | `resignation` | Subject voluntarily ends an employment. | TIMING, OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-018 | `termination` | Employer ends the employment for cause. | OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-019 | `layoff` | Employment ends through retrenchment/redundancy. | OCCURRENCE | `employment.job_loss_occurrence` | MODEL |
| EV-CAR-020 | `contract_end` | Fixed engagement concludes or is not renewed. | TIMING, OCCURRENCE | *(none yet - gap)* | MODEL |

## 3.6 Group: Venture (7 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-021 | `business_start` | Subject's venture commences operation. | TIMING, OCCURRENCE | `business.start_timing`<br>`business.start_occurrence` | MODEL |
| EV-CAR-022 | `business_expansion` | Venture grows materially in scale or footprint. | TIMING, OCCURRENCE | `business.expansion_timing` | MODEL |
| EV-CAR-023 | `business_pivot` | Venture changes its core activity. | OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-024 | `venture_partnership_formation` | A partnership forms within the venture. | OCCURRENCE | `business.partnership_occurrence` | MODEL |
| EV-CAR-025 | `venture_partnership_dissolution` | A venture partnership dissolves. | OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-026 | `business_closure` | Venture ceases operation. | OCCURRENCE | `business.closure_occurrence` | MODEL |
| EV-CAR-027 | `business_sale` | Venture is sold or exited. | OCCURRENCE | `business.sale_occurrence` | MODEL |

## 3.7 Group: Interruption (4 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-028 | `career_break_start` | A deliberate pause in working life begins. | OCCURRENCE | `transition.career_break_occurrence` | MODEL |
| EV-CAR-029 | `career_break_end` | The pause ends and working life resumes. | TIMING | `transition.reentry_timing` | MODEL |
| EV-CAR-030 | `sabbatical` | Sanctioned extended leave with return rights. | OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-031 | `suspension` | Employment is suspended pending process. | OCCURRENCE | *(none yet - gap)* | MODEL |

## 3.8 Group: Recognition (4 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-032 | `award` | Formal professional award or honour is conferred. | TIMING, OCCURRENCE | `performance.recognition_timing`<br>`performance.recognition_occurrence` | MODEL |
| EV-CAR-033 | `milestone` | A notable professional milestone is reached. | OCCURRENCE, DESCRIPTION | *(none yet - gap)* | MODEL |
| EV-CAR-034 | `appraisal_outcome` | Periodic appraisal concludes with a rating. | QUALITY | `performance.appraisal_quality` | MODEL |
| EV-CAR-035 | `professional_honour` | Field-level honour or fellowship is conferred. | OCCURRENCE | *(none yet - gap)* | MODEL |

## 3.9 Group: Adversity (5 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-036 | `demotion` | Subject is moved to a lower role or grade. | OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-037 | `disciplinary_action` | Formal disciplinary measure as an employment event. | OCCURRENCE | *(none yet - gap)* | MODEL |
| EV-CAR-038 | `stagnation_onset` | Advancement measurably stalls (state-entry treated as event). | CAUSAL, OCCURRENCE | `advancement.stagnation_cause` | MODEL |
| EV-CAR-046 | `workplace_conflict_onset` | A workplace conflict begins as a work matter. | OCCURRENCE | `workplace.conflict_occurrence` | PROPOSED-ADDITION |
| EV-CAR-047 | `workplace_conflict_resolution` | A workplace conflict is resolved. | TIMING | `workplace.conflict_resolution_timing` | PROPOSED-ADDITION |

## 3.10 Group: Exit (4 events)

| ID | Event | Description | Classes | Linked Questions | Origin |
|---|---|---|---|---|---|
| EV-CAR-039 | `retirement` | Subject leaves working life at or after the customary point. | TIMING | `exit.retirement_timing` | MODEL |
| EV-CAR-040 | `early_exit` | Working life ends before the expected point. | OCCURRENCE | `exit.early_retirement_occurrence` | MODEL |
| EV-CAR-041 | `career_end` | The final conclusion of working life. | DESCRIPTION | `exit.career_end_description` | MODEL |
| EV-CAR-042 | `postretirement_engagement` | Professional activity resumes after retirement. | TIMING, OCCURRENCE | `exit.postretirement_work_occurrence` | MODEL |

## 4. State/Outcome-Anchored Questions (17 - correctly NOT event-linked)

These Questions anchor on states, qualities, selections or causal patterns rather than on
events; forcing an event link would corrupt the taxonomy. They anchor instead on the
Domain Model's Outcome taxonomy (s.8) and Entity model (s.6):

- `employment.job_security` (QUALITY)
- `profession.vocation_direction` (SELECTION)
- `profession.fit_quality` (QUALITY)
- `business.venture_viability` (QUALITY)
- `advancement.trajectory_description` (DESCRIPTION)
- `workplace.environment_quality` (QUALITY)
- `workplace.relations_quality` (QUALITY)
- `performance.field_standing_quality` (QUALITY)
- `performance.setback_cause` (CAUSAL)
- `skill.adequacy_quality` (QUALITY)
- `skill.demand_description` (DESCRIPTION)
- `skill.upskilling_direction` (SELECTION)
- `compensation.income_growth_quality` (QUALITY)
- `compensation.level_quantity` (QUANTITY)
- `satisfaction.career_quality` (QUALITY)
- `satisfaction.dissatisfaction_cause` (CAUSAL)
- `satisfaction.improvement_timing` (TIMING)

## 5. Coverage Gap Ledger (16 events with zero Questions)

The generation backlog for library v0.2.0 - each gap event supports the classes listed in
s.3 and awaits owner prioritisation (no questions are generated here):


| ID | Event | Group |
|---|---|---|
| EV-CAR-004 | `grade_rise` | Progression |
| EV-CAR-005 | `scope_expansion` | Progression |
| EV-CAR-008 | `role_change` | Lateral |
| EV-CAR-011 | `secondment` | Lateral |
| EV-CAR-015 | `industry_change` | Reorientation |
| EV-CAR-017 | `resignation` | Separation |
| EV-CAR-018 | `termination` | Separation |
| EV-CAR-020 | `contract_end` | Separation |
| EV-CAR-023 | `business_pivot` | Venture |
| EV-CAR-025 | `venture_partnership_dissolution` | Venture |
| EV-CAR-030 | `sabbatical` | Interruption |
| EV-CAR-031 | `suspension` | Interruption |
| EV-CAR-033 | `milestone` | Recognition |
| EV-CAR-035 | `professional_honour` | Recognition |
| EV-CAR-036 | `demotion` | Adversity |
| EV-CAR-037 | `disciplinary_action` | Adversity |

## 6. OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| EVR-1 | Domain-local (EV-CAR-) vs HLKG-wide (HLKG-EV-) event ID family; cross-domain event sharing policy | ID permanence |
| EVR-2 | Ratification of the 5 PROPOSED-ADDITION events into Domain Model v0.2.0 (notably `employment_obtained`, which is the event-side twin of the ALR-1 general-job-node gap) | Origin column closure |
| EVR-3 | Whether the Coverage Gap Ledger (s.5) mandates generation priority or remains informational | Library v0.2.0 scope |
| Inherited | ALR-1 (general job timing node), CDQ-1 (domain ratification) | as recorded |

## 7. Self-Audit Record

1. Built from a machine sweep in both directions - and the sweep produced this registry's
   most valuable finding: five event-anchored Questions had NO event in the Model s.7
   taxonomy (general hiring, offer receipt, second-career start, conflict onset/
   resolution). They were added as flagged PROPOSED-ADDITIONS under the Model's own
   append policy rather than silently, and `employment_obtained` is explicitly recorded
   as the event-side twin of ALR-1 - two independent artifacts now point at the same
   library gap, which is exactly what a registry system is for.
2. Name-collision sweep run against subdomain names (12) and outcome terms (Model s.8):
   zero collisions; `career_break_start/end` deliberately distinct from the subdomain
   `transition` and outcome vocabulary.
3. The 23 unanchored Questions were individually reviewed: all are state/outcome/selection
   /causal-anchored; none is a missed event link. `stagnation_onset` was the borderline
   case - kept as an event (Model s.7 lists it as state-entry-as-event) and linked to the
   CAUSAL question.
4. Restraint: zero questions generated despite 16 inviting gaps; the ledger records them
   for owner prioritisation instead (EVR-3).
5. Known limitation: event descriptions are one-liners by design; boundary nuance lives in
   the Domain Model and is not duplicated here (single source of truth).
