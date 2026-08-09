| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | CAREER_DOMAIN_MODEL.md v0.1.0 s.8 (source taxonomy), docs/QUESTION_REGISTRY_SPEC.md s.7 (Answer Contract), CAREER_EVENT_REGISTRY.md v0.1.0 (complementary anchoring), CAREER_QUESTION_LIBRARY.md v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_OUTCOME_REGISTRY.md |
| Machine verification | 21 outcomes, 6 groups: unique IDs/names, valid polarity values, classes from the closed registry, all linked slugs exist, all 7 opposition pairs resolve to registered outcomes. Three-way anchoring computed: event+outcome union covers 55/61 questions; 6 residual questions entity/market-state anchored; 3 dual-anchored questions listed. ALL CHECKS PASS. |

# Career Outcome Registry

Formalises the Domain Model's Outcome taxonomy (s.8): the states and trajectories a
complete answer may assert. **Outcomes are answer vocabulary, not Questions, not events
and not predictions** - they are what QUALITY ratings rate, what DESCRIPTION narratives
characterise, and what CAUSAL explanations explain. Includes the outcomes named in the
brief: growth, delay, stability, recognition (as `recognition_attained`), leadership (as
`leadership_attained`) and decline.

## 1. ID Scheme and Record Shape

`OC-CAR-NNN` - domain-local, zero-padded, monotone, immutable, never reused; the
domain-local-vs-HLKG-wide question is shared with events (EVR-1; ruling applies to both
families - OCR-1 mirrors it). Each outcome: ID | name | group | definition | polarity |
applicable classes | linked Questions | scale-dependency.

**Polarity** is descriptive default valence (favourable / adverse / neutral) for
vocabulary organisation only - it is subject-relative in reality (early retirement is
adverse to one person, favourable to another) and MUST NOT be consumed as an evaluation
rule by any engine. Recorded because a registry without valence invites inconsistent ad-hoc
labelling later.

## 2. Anchoring Doctrine (complementary to the Event Registry)

Questions anchor three ways, and the two registries are designed as complements:
- **Event-anchored** (44/61): TIMING/OCCURRENCE of happenings -> CAREER_EVENT_REGISTRY.
- **Outcome-anchored** (14/61): QUALITY/DESCRIPTION/CAUSAL and state-transition questions
  whose answers are expressed in this registry's vocabulary.
- **Entity/market-state anchored** (6/61, s.5): questions about states of Entities (Model
  s.6) that are neither events nor career outcomes (e.g., workplace environment, skill
  demand).
Dual anchoring is permitted only where a CAUSAL/QUALITY question sits on a state-entry
event; the 3 such cases are listed in s.6 - anything else claiming both anchors is a
modelling error.


## 3.1 Group: Trajectory (5)

| ID | Outcome | Definition | Polarity | Classes | Linked Questions | Scale needed |
|---|---|---|---|---|---|---|
| OC-CAR-001 | `growth` | Working life is expanding in scope, level or venture scale. | favourable | QUALITY, DESCRIPTION | `advancement.trajectory_description`<br>`business.venture_viability` | YES |
| OC-CAR-002 | `decline` | Working life is contracting in level, scope or standing. | adverse | QUALITY, DESCRIPTION, CAUSAL | `advancement.trajectory_description`<br>`performance.setback_cause` | YES |
| OC-CAR-003 | `stability` | Working life holds its level without material movement. | neutral | QUALITY, DESCRIPTION | `advancement.trajectory_description`<br>`business.venture_viability` | YES |
| OC-CAR-004 | `stagnation` | Expected movement is absent; advancement has stalled. | adverse | QUALITY, CAUSAL | `advancement.trajectory_description`<br>`advancement.stagnation_cause` | YES |
| OC-CAR-005 | `reinvention` | Working life changes form substantially (new career shape). | neutral | DESCRIPTION | `advancement.trajectory_description` | no |

## 3.2 Group: Attainment (4)

| ID | Outcome | Definition | Polarity | Classes | Linked Questions | Scale needed |
|---|---|---|---|---|---|---|
| OC-CAR-006 | `success` | A declared career goal is achieved. | favourable | QUALITY, OCCURRENCE | *(vocabulary only in v0.1.0)* | YES |
| OC-CAR-007 | `leadership_attained` | Authority/leadership standing is reached. | favourable | OCCURRENCE, TIMING | *(vocabulary only in v0.1.0)* | no |
| OC-CAR-008 | `recognition_attained` | Professional acknowledgement within the field is secured. | favourable | QUALITY, OCCURRENCE | `performance.field_standing_quality`<br>`performance.appraisal_quality` | YES |
| OC-CAR-009 | `seniority_attained` | A higher formal grade or rank is reached. | favourable | OCCURRENCE, TIMING | *(vocabulary only in v0.1.0)* | no |

## 3.3 Group: Timing-flavoured (3)

| ID | Outcome | Definition | Polarity | Classes | Linked Questions | Scale needed |
|---|---|---|---|---|---|---|
| OC-CAR-010 | `delay` | An expected career event realises later than its expected point. | adverse | TIMING, OCCURRENCE | *(vocabulary only in v0.1.0)* | no |
| OC-CAR-011 | `acceleration` | An expected career event realises earlier than its expected point. | favourable | TIMING, OCCURRENCE | *(vocabulary only in v0.1.0)* | no |
| OC-CAR-012 | `prematurity` | An exit-type event realises before its natural point. | neutral | OCCURRENCE | *(vocabulary only in v0.1.0)* | no |

## 3.4 Group: Security (3)

| ID | Outcome | Definition | Polarity | Classes | Linked Questions | Scale needed |
|---|---|---|---|---|---|---|
| OC-CAR-013 | `security` | Employment/venture continuity is well protected. | favourable | QUALITY | `employment.job_security` | YES |
| OC-CAR-014 | `insecurity` | Continuity is materially threatened. | adverse | QUALITY | `employment.job_security` | YES |
| OC-CAR-015 | `precarity` | Working life is structurally unstable across engagements. | adverse | QUALITY, DESCRIPTION | *(vocabulary only in v0.1.0)* | YES |

## 3.5 Group: Fit (4)

| ID | Outcome | Definition | Polarity | Classes | Linked Questions | Scale needed |
|---|---|---|---|---|---|---|
| OC-CAR-016 | `fit` | The line of work matches the subject's makeup and aims. | favourable | QUALITY, SELECTION | `profession.fit_quality`<br>`profession.vocation_direction` | YES |
| OC-CAR-017 | `misfit` | The line of work conflicts with the subject's makeup or aims. | adverse | QUALITY | `profession.fit_quality` | YES |
| OC-CAR-018 | `satisfaction` | Working life is experienced as fulfilling (career appraisal, not wellbeing). | favourable | QUALITY, TIMING | `satisfaction.career_quality`<br>`satisfaction.improvement_timing` | YES |
| OC-CAR-019 | `dissatisfaction` | Working life is experienced as unfulfilling (career appraisal). | adverse | QUALITY, CAUSAL | `satisfaction.career_quality`<br>`satisfaction.dissatisfaction_cause` | YES |

## 3.6 Group: Economic (2)

| ID | Outcome | Definition | Polarity | Classes | Linked Questions | Scale needed |
|---|---|---|---|---|---|---|
| OC-CAR-020 | `income_growth` | Compensation attached to work rises over the scope (career facet; wealth is finance). | favourable | QUALITY | `compensation.income_growth_quality` | YES |
| OC-CAR-021 | `income_stagnation` | Compensation attached to work fails to rise. | adverse | QUALITY, CAUSAL | `compensation.income_growth_quality`<br>`compensation.stagnation_cause` | YES |

## 4. Opposition Pairs (vocabulary structure - NOT `EXCLUDES` edges)

Antonym structure aids scale design and intake disambiguation. These pairs are
vocabulary-level opposites; they are NOT node relationships and never imply the EXCLUDES
edge type (a career can hold growth and decline in different periods):

- `growth` <-> `decline`
- `stability` <-> `stagnation`
- `security` <-> `insecurity`
- `fit` <-> `misfit`
- `satisfaction` <-> `dissatisfaction`
- `income_growth` <-> `income_stagnation`
- `acceleration` <-> `delay`

Unpaired by design: `reinvention`, `success`, `leadership_attained`, `seniority_attained`,
`recognition_attained`, `precarity`, `prematurity` - their negations are absences, not
outcomes.

## 5. Residual: Entity/Market-State Anchored Questions (6)

Correctly linked to neither registry; they anchor on Entity states (Model s.6):

- `workplace.environment_quality`
- `workplace.relations_quality`
- `skill.adequacy_quality`
- `skill.demand_description`
- `skill.upskilling_direction`
- `compensation.level_quantity`

## 6. Dual-Anchored Questions (3 - the only permitted overlaps)

| Question | Event anchor | Outcome anchor |
|---|---|---|
| `advancement.stagnation_cause` | stagnation_onset (EV) | stagnation (OC) |
| `compensation.stagnation_cause` | pay_raise (absence pattern) | income_stagnation (OC) |
| `performance.appraisal_quality` | appraisal_outcome (EV) | recognition_attained (OC) |

## 7. Scale Requirements Ledger (feeds CDQ-5 ratification)

15 outcomes require declared Rating scales before any linked QUALITY question can
reach CANONICAL. Proposed consolidation: the 15 scale-needing outcomes reduce to **7 scale
artifacts** by pairing opposites on bipolar scales (security<->insecurity; fit<->misfit;
satisfaction<->dissatisfaction; income growth<->stagnation; growth/decline/stability/
stagnation on one trajectory scale) plus success-against-goal, recognition-standing and
venture-viability scales. Consolidation is a proposal for the CDQ-5 decision, not a
ratified design.

## 8. OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| OCR-1 | Domain-local vs HLKG-wide outcome ID family (mirror of EVR-1; one ruling should cover both) | ID permanence |
| OCR-2 | Ratification of the s.7 scale consolidation (7 bipolar/unipolar artifacts) as the CDQ-5 work list | QUALITY questions -> CANONICAL |
| OCR-3 | Is `delay` an outcome nodes may anchor on, or purely an answer-facet (a property OF Timeline answers vs expectation)? Current v0.1.0 links no question to it; the ruling shapes future "will X be delayed" intake | Timing-flavoured group usage |
| OCR-4 | Polarity metadata retention: keep as descriptive vocabulary aid, or drop as evaluative risk? | s.1 polarity column |
| Inherited | CDQ-5 (scales), EVR-1 (ID family), QQ-2 (annotations) | as recorded |

## 9. Self-Audit Record

1. Coverage closure achieved and machine-verified: event(44) + outcome(14) - dual(3) +
   entity-state(6) = 61/61 questions accounted for under exactly one doctrine each (plus
   3 permitted duals). The complementarity claim between the two registries is computed,
   not asserted.
2. `delay` and `acceleration` were nearly linked to every TIMING question in drafting -
   rejected: they are properties of answers relative to expectations, not what those
   questions ask; the honest state is vocabulary-only with OCR-3 recording the open
   semantics.
3. Polarity was almost omitted as evaluative; retained as descriptive-only with an
   explicit no-engine-consumption rule and OCR-4 offering the owner the deletion option -
   the risk is recorded either way.
4. Name-collision sweep vs event names and subdomain names: `stagnation` (outcome) vs
   `stagnation_onset` (event) is the deliberate state-vs-state-entry pair, documented in
   s.6; zero accidental collisions.
5. The scale ledger converts CDQ-5 from an abstract blocker into a concrete 7-artifact
   work list - proposed, clearly, not ratified.
