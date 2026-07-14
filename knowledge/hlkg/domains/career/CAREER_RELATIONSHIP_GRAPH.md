| Field | Value |
|---|---|
| Status | DRAFT - proposed adjudication set; edges are semantic changes requiring adjudication before entering records |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | docs/HLKG_CONSTITUTION.md s.10, docs/QUESTION_REGISTRY_SPEC.md s.10, CAREER_QUESTION_LIBRARY.md v0.1.0, career.questions.json v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_RELATIONSHIP_GRAPH.md |
| Machine verification | 17 edges over 61 nodes: endpoints exist, no self-edges, no duplicate triples, no pair double-typed DEPENDS_ON+PRECEDES, RELATES_TO rationale present on all 4, REFINES/PRECEDES/DEPENDS_ON each acyclic - ALL PASS |

# Career Relationship Graph

The adjudication source for typed edges among the 61 career Questions. Ten edges already
ship in career.questions.json v0.1.0; seven are newly proposed here and enter the records
only after adjudication (edge changes are semantic changes, QRS s.18).

## 1. Vocabulary Mapping (no new types - constitutional registry is closed)

The requested relationship names map onto the locked registry as follows; inventing new
edge types would be a constitutional amendment and is refused:

| Requested name | Constitutional type | Direction convention |
|---|---|---|
| Parent | `REFINES` target | the broader Question |
| Child | `REFINES` source | the strictly narrower Question |
| Refines | `REFINES` | child -> parent |
| Depends On | `DEPENDS_ON` | dependent -> presupposed |
| Related | `RELATES_TO` | symmetric in meaning; stored on the record where adjudicated; rationale mandatory |
| Mutually Exclusive | `EXCLUDES` | symmetric |
| Predecessor | `PRECEDES` source | the concept realised earlier |
| Successor | `PRECEDES` target | the concept realised later |

**Important distinction:** "Successor/Predecessor" here means *life-sequence*
(`PRECEDES`). The registry's other successor notion - `SUPERSEDED_BY` - is *lifecycle
machinery* for DEPRECATED nodes and has, correctly, **zero instances** in this batch
(no career node is deprecated).

## 2. Edge Semantics and House Rules

- `REFINES`: child is strictly narrower; every complete answer to the child bears on the
  parent's scope. Single hierarchy per pair; acyclic.
- `PRECEDES`: when both concepts realise, the source characteristically or necessarily
  realises first. Acyclic. Never used for mere correlation.
- `DEPENDS_ON`: a complete answer to the source presupposes an (affirmative) answer to the
  target. Acyclic. **House convention:** where DEPENDS_ON holds, the implied sequence is
  NOT duplicated as PRECEDES - presupposition subsumes sequence (machine-checked).
- `RELATES_TO`: last resort; written rationale mandatory; carries no hierarchy, no
  sequence, no inference license.
- `EXCLUDES`: affirmative resolutions conceptually incompatible; symmetric; never forced.
- TIMING/OCCURRENCE sibling pairs (promotion, job change, foreign posting, raise,
  business start, profession change) are deliberately **unlinked**: their kinship is
  already structural via shared topic+event (QRS s.8 rule 4); edges would add noise, not
  meaning.

## 3. The Edge Set (17 edges)

### 3.1 REFINES - Parent/Child hierarchy (3)

| Child (source) | Parent (target) | Justification | Status |
|---|---|---|---|
| HLKG-N-000406 `employment.government_job_occurrence` | HLKG-N-000402 `employment.job_occurrence` | Government employment is strictly a kind of employment; every complete answer to the child is a partial answer to the parent scope. | in records v0.1.0 |
| HLKG-N-000445 `assignment.foreign_posting_occurrence` | HLKG-N-000447 `assignment.transfer_occurrence` | A work posting abroad is strictly a transfer of work location whose destination is foreign. | proposed |
| HLKG-N-000446 `assignment.foreign_posting_timing` | HLKG-N-000448 `assignment.transfer_timing` | Timing counterpart of the same strict-subset relation. | proposed |

### 3.2 PRECEDES - Predecessor/Successor sequences (5)

| Predecessor (source) | Successor (target) | Justification | Status |
|---|---|---|---|
| HLKG-N-000401 `employment.first_job_timing` | HLKG-N-000420 `advancement.promotion_timing` | First employment characteristically precedes any promotion. | in records v0.1.0 |
| HLKG-N-000407 `employment.offer_occurrence` | HLKG-N-000402 `employment.job_occurrence` | An offer characteristically precedes the employment it enables. | in records v0.1.0 |
| HLKG-N-000402 `employment.job_occurrence` | HLKG-N-000403 `employment.job_loss_occurrence` | Employment necessarily precedes any loss of it; order fixed when both realise. | proposed |
| HLKG-N-000413 `business.start_timing` | HLKG-N-000417 `business.expansion_timing` | Venture start characteristically precedes its expansion. | in records v0.1.0 |
| HLKG-N-000414 `business.start_occurrence` | HLKG-N-000418 `business.sale_occurrence` | Venture start necessarily precedes its sale/exit. | proposed |

### 3.3 DEPENDS_ON - presupposition (5)

| Dependent (source) | Presupposed (target) | Justification | Status |
|---|---|---|---|
| HLKG-N-000404 `employment.reemployment_timing` | HLKG-N-000403 `employment.job_loss_occurrence` | Re-employment presupposes a prior loss of employment; the child's complete answer presupposes an affirmative answer to the target. | in records v0.1.0 |
| HLKG-N-000431 `transition.reentry_timing` | HLKG-N-000430 `transition.career_break_occurrence` | Re-entry presupposes a career break. | in records v0.1.0 |
| HLKG-N-000449 `assignment.posting_return_timing` | HLKG-N-000445 `assignment.foreign_posting_occurrence` | Return presupposes a posting. | in records v0.1.0 |
| HLKG-N-000460 `exit.postretirement_work_occurrence` | HLKG-N-000458 `exit.retirement_timing` | Post-retirement activity presupposes retirement. | in records v0.1.0 |
| HLKG-N-000435 `workplace.conflict_resolution_timing` | HLKG-N-000434 `workplace.conflict_occurrence` | Resolution presupposes the conflict. | proposed |

### 3.4 RELATES_TO - adjudicated adjacency (4, rationale mandatory)

| A (record holder) | B | Rationale | Status |
|---|---|---|---|
| HLKG-N-000455 `satisfaction.career_quality` | HLKG-N-000433 `workplace.environment_quality` | Frequent co-signal in user intent; recorded for intake routing analytics only. | in records v0.1.0 |
| HLKG-N-000422 `advancement.leadership_occurrence` | HLKG-N-000421 `advancement.promotion_occurrence` | Leadership attainment often but not necessarily arrives via promotion; neither refines the other. | in records v0.1.0 |
| HLKG-N-000450 `compensation.raise_occurrence` | HLKG-N-000421 `advancement.promotion_occurrence` | Raises frequently accompany promotions yet occur independently; adjacency aids intake disambiguation, no hierarchy exists. | proposed |
| HLKG-N-000442 `skill.adequacy_quality` | HLKG-N-000444 `skill.upskilling_direction` | An adequacy gap typically motivates the upskilling selection; answers inform each other without presupposition. | proposed |

### 3.5 EXCLUDES - mutually exclusive (0, with justification)

No pair of career Questions is conceptually incompatible in the EXCLUDES sense: career
lives legitimately contain apparent opposites over time (early retirement AND
post-retirement work; business closure AND a later venture; job loss AND leadership
attainment). Candidates examined and rejected: early_retirement vs postretirement_work
(sequential, not exclusive); business closure vs expansion (both can occur across a
venture's life); employed vs self-employed direction (a SELECTION binding, not two
occurrence nodes). EXCLUDES is never forced (constitutional note); zero is the honest count.

### 3.6 SUPERSEDED_BY - lifecycle successors (0)

No DEPRECATED nodes exist in career v0.1.0; this section exists so future deprecations
have their designated home and so "successor" is never conflated with PRECEDES.

## 4. Derived Views

**Hierarchy (Parent <- children):**
- employment.job_occurrence <- employment.government_job_occurrence
- assignment.transfer_occurrence <- assignment.foreign_posting_occurrence
- assignment.transfer_timing <- assignment.foreign_posting_timing

**Sequence chains (Predecessor -> Successor):**
- offer_occurrence -> job_occurrence -> job_loss_occurrence; job_loss_occurrence ~(DEPENDS_ON)~ reemployment_timing
- first_job_timing -> promotion_timing
- business.start_timing -> expansion_timing; start_occurrence -> sale_occurrence
- career_break_occurrence ~(DEPENDS_ON)~ reentry_timing; foreign_posting_occurrence ~(DEPENDS_ON)~ posting_return_timing; retirement_timing ~(DEPENDS_ON)~ postretirement_work_occurrence

## 5. Deliberate Non-Edges (rejected candidates - precedent record)

| Candidate | Rejected because |
|---|---|
| leadership_occurrence REFINES promotion_occurrence | Leadership is not a strict subset of promotion (lateral hires, founder roles); downgraded to RELATES_TO in v0.1.0 - retained precedent. |
| reemployment_timing PRECEDES anything / job_loss PRECEDES reemployment_timing | Pair already carries DEPENDS_ON; house convention forbids double-typing. |
| business.closure_occurrence DEPENDS_ON start_occurrence | "The stated business" is bound as a query parameter; existence is context, not an answer to the start Question - presupposition test fails. |
| satisfaction.improvement_timing DEPENDS_ON dissatisfaction_cause | Improvement presupposes a state, not an answer to a CAUSAL Question. |
| trajectory_description RELATES_TO every advancement node | Blanket adjacency adds no routing value; RELATES_TO is last resort, not decoration. |
| Any TIMING <-> OCCURRENCE sibling edge | Structural kinship already explicit (s.2 house rule). |

## 6. Pending Edges (blocked on open questions)

If ALR-1 ratifies a general `employment.job_timing` node: first_job_timing REFINES
job_timing; reemployment_timing REFINES job_timing (both strict narrowings). Recorded now
so the decision lands with its consequences visible.

## 7. Validation

Machine checks executed on the full 17-edge set (results in header): endpoint existence
against career.questions.json; no self-edges; no duplicate (type, source, target); no
DEPENDS_ON+PRECEDES double-typed pair; RELATES_TO rationale present (4/4); per-type
acyclicity via depth-first search for REFINES, PRECEDES, DEPENDS_ON. At import, edges
additionally face the registry-level checks (endpoint lifecycle states, graph-wide
acyclicity with other domains' edges).

## 8. OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| CRG-1 | Adjudication of the 7 proposed edges (3 REFINES-assignment, 2 PRECEDES, 1 DEPENDS_ON, 2 RELATES_TO) | Records v0.2.0 edge update |
| CRG-2 | Is the house convention "DEPENDS_ON subsumes PRECEDES on the same pair" ratified project-wide, or career-local? | Cross-domain consistency |
| CRG-3 | ALR-1 outcome (general job_timing node) and its two pending REFINES edges | s.6 |
| Inherited | CQL-2 (original RELATES_TO adjudication) | as recorded |

## 9. Self-Audit Record

1. Every edge machine-verified (header); one candidate class of error - double-typing a
   pair with both DEPENDS_ON and PRECEDES - was made structurally impossible by an
   explicit convention plus a check, after the reemployment pair initially carried both
   in drafting.
2. The rejected-candidates table preserves adjudication precedent, including the
   leadership/promotion REFINES rejection inherited from the library's audit.
3. EXCLUDES=0 and SUPERSEDED_BY=0 are argued, not omitted - each has a section stating why
   zero is correct, so absence is auditable.
4. Restraint check: 17 edges over 61 nodes (0.28/node) - the graph carries only
   adjudicable meaning; density was reviewed against the "RELATES_TO is not decoration"
   rule and two drafted RELATES_TO edges were cut (job_change<->job_loss; stagnation_cause
   <->promotion_occurrence) as adding routing noise without disambiguation value.
5. Directionality spot-checked: all REFINES point child->parent, all DEPENDS_ON point
   dependent->presupposed, matching QRS s.10 conventions exactly.
