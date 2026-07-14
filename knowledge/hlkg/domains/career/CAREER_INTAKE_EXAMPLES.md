| Field | Value |
|---|---|
| Status | DRAFT - illustrative examples; regenerated, never hand-edited (examples/ charter applies) |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Produced against | career.questions.json v0.1.0 · CAREER_ALIAS_REGISTRY.md v0.1.0 · CAREER_PARAMETER_REGISTRY.md v0.1.0 · schemas/question.schema.json 1.0.0 · career.test.dataset.json v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_INTAKE_EXAMPLES.md |
| Machine verification | 18 worked examples. Every plain-RESOLVED utterance exact-match-verified against the alias registry to the exact expected node (RESOLVED_WITH_PARAMETERS resolves via alias stem + extraction, so exact-match assertion deliberately does not apply there). All slugs verified against records; 13 examples trace to test-dataset scenario IDs. ALL PASS - after one caught-and-fixed defect (see Self-Audit 2). |

# Career Intake Examples

Worked, end-to-end mappings from natural user language to canonical Questions, bound
parameters and answer-contract shapes. **Illustrative, not normative** - tests and
specifications govern behaviour; these examples exist so humans can see the machinery run.
No astrology, no prediction content: answer contracts are shown as empty structural
skeletons.

## The Intake Pipeline (recap)

1. **Normalise** (NFKC, lowercase, whitespace collapse, terminal punctuation incl. danda)
2. **Exact resolve** - Gate-1 lookup against per-locale aliases + labels -> one node or nothing
3. **Ambiguity check** - phrases in the Ambiguity table demand disambiguation, never mapping
4. **Composite check** - multi-concept utterances decompose to multiple Query targets
5. **Parameter extraction** - years/durations/options/subject become bindings, never aliases
6. **Binding validation** - required parameters present, kinds registered, policy gates (VC-C/D)
7. **Answer contract** - the class fixes the payload shape; `not_established` is always a lawful outcome


## Example 1: Simple exact resolution (English)
**Utterance** (`en`): "When will I get promoted?"
**Normalised:** `when will i get promoted`
**Outcome:** `RESOLVED`
**Canonical Question:** HLKG-N-000420 `career.advancement.promotion_timing` (TIMING) - "When is a promotion likely to occur?"
**Answer contract skeleton:** `{"payload": {"intervals": [{"interval_start":"...","interval_end":"...","precision_declared":"month","strength_label":"..."}]}}  # empty list = not indicated within scope`
**Bound parameters:** `{"subject": {"relation": "self"}}`
**Notes:** Horizon optional and unbound: answer scope = engine's declared maximum scope, which the answer MUST state.

## Example 2: Hinglish resolution
**Utterance** (`hi-Latn`): "promotion kab hoga"
**Normalised:** `promotion kab hoga`
**Outcome:** `RESOLVED`
**Canonical Question:** HLKG-N-000420 `career.advancement.promotion_timing` (TIMING) - "When is a promotion likely to occur?"
**Answer contract skeleton:** `{"payload": {"intervals": [{"interval_start":"...","interval_end":"...","precision_declared":"month","strength_label":"..."}]}}  # empty list = not indicated within scope`
**Bound parameters:** `{"subject": {"relation": "self"}}`
**Notes:** Same node as the English form - aliases converge on one identity; locale hi-Latn pending CQL-3/ALR-2.

## Example 3: Devanagari resolution
**Utterance** (`hi`): "क्या सरकारी नौकरी मिलेगी?" · traces to `TC-CAR-039`
**Normalised:** `क्या सरकारी नौकरी मिलेगी`
**Outcome:** `RESOLVED`
**Canonical Question:** HLKG-N-000406 `career.employment.government_job_occurrence` (OCCURRENCE) - "Will government employment be obtained within the stated horizon?"
**Answer contract skeleton:** `{"payload": {"value":"yes|no|not_established","horizon":{"start":"...","end":"..."},"qualifier":"..."}}  # horizon mandatory`
**Bound parameters:** `{"subject": {"relation": "self"}, "horizon": "REQUIRED - must be elicited before answering"}`
**Notes:** OCCURRENCE without a horizon is malformed: intake must elicit the window, not assume one. Danda/question-mark stripped by normalisation.

## Example 4: Spelling-variant capture
**Utterance** (`en`): "when will i get promtion" · traces to `TC-CAR-032`
**Normalised:** `when will i get promtion`
**Outcome:** `RESOLVED`
**Canonical Question:** HLKG-N-000420 `career.advancement.promotion_timing` (TIMING) - "When is a promotion likely to occur?"
**Answer contract skeleton:** `{"payload": {"intervals": [{"interval_start":"...","interval_end":"...","precision_declared":"month","strength_label":"..."}]}}  # empty list = not indicated within scope`
**Bound parameters:** `{"subject": {"relation": "self"}}`
**Notes:** Stored-verbatim misspelling ('promtion') hits Gate-1 exact match after normalisation - variants resolve only if registered, which is the design: unregistered misspellings fall to NO_MATCH/Gate-2.

## Example 5: Horizon extraction - absolute
**Utterance** (`en`): "Will I get promoted before 2028?" · traces to `TC-CAR-092`
**Normalised:** `will i get promoted before 2028`
**Outcome:** `RESOLVED_WITH_PARAMETERS`
**Canonical Question:** HLKG-N-000421 `career.advancement.promotion_occurrence` (OCCURRENCE) - "Will a promotion occur within the stated horizon?"
**Answer contract skeleton:** `{"payload": {"value":"yes|no|not_established","horizon":{"start":"...","end":"..."},"qualifier":"..."}}  # horizon mandatory`
**Bound parameters:** `{"subject": {"relation": "self"}, "horizon": {"start": "QUERY_DATE", "end": "2028-01-01"}}`
**Notes:** 'before 2028' is a parameter, never an alias (VC-E3). Note the class shift vs example 1: 'when' asks TIMING; 'will..before X' asks OCCURRENCE - two different nodes (QRS s.8.4). Resolution here is via the alias stem + extraction, so exact-match verification deliberately does not apply to RESOLVED_WITH_PARAMETERS.

## Example 6: Horizon extraction - relative
**Utterance** (`en`): "Will I change jobs in the next two years?" · traces to `TC-CAR-093`
**Normalised:** `will i change jobs in the next two years`
**Outcome:** `RESOLVED_WITH_PARAMETERS`
**Canonical Question:** HLKG-N-000427 `career.transition.job_change_occurrence` (OCCURRENCE) - "Will a change of job occur within the stated horizon?"
**Answer contract skeleton:** `{"payload": {"value":"yes|no|not_established","horizon":{"start":"...","end":"..."},"qualifier":"..."}}  # horizon mandatory`
**Bound parameters:** `{"subject": {"relation": "self"}, "horizon": {"from": "QUERY_TIME", "duration": "P2Y"}}`
**Notes:** Whether relative windows normalise to absolute at binding (reproducibility) is CPR-4 - both forms shown pending that ruling.

## Example 7: QUANTITY with required horizon
**Utterance** (`en`): "How many times will I change jobs in the next ten years?" · traces to `TC-CAR-094`
**Normalised:** `how many times will i change jobs in the next ten years`
**Outcome:** `RESOLVED_WITH_PARAMETERS`
**Canonical Question:** HLKG-N-000428 `career.transition.job_change_count` (QUANTITY) - "How many changes of employer are indicated within the stated horizon?"
**Answer contract skeleton:** `{"payload": {"value_or_range":"...","unit":"employer changes","basis_note":"..."}}`
**Bound parameters:** `{"subject": {"relation": "self"}, "horizon": {"from": "QUERY_TIME", "duration": "P10Y"}}`
**Notes:** Windowed QUANTITY: horizon required by declaration.

## Example 8: SELECTION with options bound
**Utterance** (`en`): "Should I take job A or job B?"
**Normalised:** `should i take job a or job b`
**Outcome:** `RESOLVED_WITH_PARAMETERS`
**Canonical Question:** HLKG-N-000408 `career.profession.vocation_direction` (SELECTION) - "Which of the declared vocational directions fits best?"
**Answer contract skeleton:** `{"payload": {"options_declared":[...],"selected":["opt-.."],"ranking":[...],"abstained":false}}`
**Bound parameters:** `{"subject": {"relation": "self"}, "option_set": [{"option_id": "opt-1", "label": "Job A"}, {"option_id": "opt-2", "label": "Job B"}]}`
**Notes:** Options bound at query time; answers reference option_ids only; registry never stores option content.

## Example 9: SELECTION without options
**Utterance** (`en`): "Should I change my career?" · traces to `TC-CAR-098`
**Normalised:** `should i change my career`
**Outcome:** `OPTIONS_REQUIRED`
**Canonical Question:** HLKG-N-000408 `career.profession.vocation_direction` (SELECTION) - "Which of the declared vocational directions fits best?"
**Answer contract skeleton:** `{"payload": {"options_declared":[...],"selected":["opt-.."],"ranking":[...],"abstained":false}}`
**Notes:** SELECTION is malformed without option_set - intake prompts for the choices instead of guessing them.

## Example 10: QUALITY (scale-gated)
**Utterance** (`en`): "How safe is my job?"
**Normalised:** `how safe is my job`
**Outcome:** `RESOLVED`
**Canonical Question:** HLKG-N-000405 `career.employment.job_security` (QUALITY) - "How secure is the current employment?"
**Answer contract skeleton:** `{"payload": {"scale_id":"<pending CDQ-5>","scale_definition_ref":"...","value":"...","band":"...","caveats":[]}}`
**Bound parameters:** `{"subject": {"relation": "self"}}`
**Notes:** Resolves cleanly, but the QUALITY answer contract requires a declared scale - blocked until CDQ-5/OCR-2 scales ratify; honest interim outcome is a refusal citing the missing scale, not an unscaled rating (CIE-2).

## Example 11: CAUSAL
**Utterance** (`en`): "Why am I not getting promoted?"
**Normalised:** `why am i not getting promoted`
**Outcome:** `RESOLVED`
**Canonical Question:** HLKG-N-000425 `career.advancement.stagnation_cause` (CAUSAL) - "What factors underlie stagnation in career advancement?"
**Answer contract skeleton:** `{"payload": {"factors":[{"factor":"...","direction":"...","weight_label":"..."}],"explanation":"...","counterfactual_note":"..."}}`
**Bound parameters:** `{"subject": {"relation": "self"}}`
**Notes:** Dual-anchored (stagnation_onset event + stagnation outcome) - one of only three permitted duals.

## Example 12: Ambiguity - mandatory disambiguation
**Utterance** (`en`): "When will I get a job?" · traces to `TC-CAR-070`
**Normalised:** `when will i get a job`
**Outcome:** `DISAMBIGUATION_REQUIRED`
**Candidate/target Questions:**
- HLKG-N-000401 `career.employment.first_job_timing` (TIMING) - "When is first employment likely to begin?"
- HLKG-N-000404 `career.employment.reemployment_timing` (TIMING) - "When is re-employment after a loss of employment likely to occur?"
**Disambiguation dialogue:** Intake asks: 'Is this your first job, or a return to work after a previous job ended?' - then routes.
**Notes:** Deliberately NOT an alias (one-alias-one-node law). The most common phrase in the domain has no general node - ALR-1/EVR-2 gap; this example is the user-facing cost of that open decision.

## Example 13: Composite - decomposition
**Utterance** (`en`): "Will I get promoted, and when?" · traces to `TC-CAR-076`
**Normalised:** `will i get promoted, and when`
**Outcome:** `DECOMPOSITION`
**Candidate/target Questions:**
- HLKG-N-000421 `career.advancement.promotion_occurrence` (OCCURRENCE) - "Will a promotion occur within the stated horizon?"
- HLKG-N-000420 `career.advancement.promotion_timing` (TIMING) - "When is a promotion likely to occur?"
**Notes:** Two Query targets, two answer envelopes; any packaging of the pair is a consumer concern. The composite never becomes a node.

## Example 14: Boundary routing - money vs venture
**Utterance** (`en`): "Will my business make me wealthy?" · traces to `TC-CAR-084`
**Normalised:** `will my business make me wealthy`
**Outcome:** `OUT_OF_DOMAIN`
**Notes:** Model boundary 4.1: wealth outcome -> finance domain. Contrast: 'Will my business do well?' resolves in-career to business.venture_viability.

## Example 15: Boundary routing - exam vs appointment
**Utterance** (`en`): "Will I pass the civil services exam?" · traces to `TC-CAR-086`
**Normalised:** `will i pass the civil services exam`
**Outcome:** `OUT_OF_DOMAIN`
**Notes:** Boundary 4.2: the examination is education; the appointment ('क्या सरकारी नौकरी मिलेगी?', example 3) is career - one user journey, two domains, cleanly split.

## Example 16: Policy refusal - other subject
**Utterance** (`en`): "Will my son get a government job?" · traces to `TC-CAR-097`
**Normalised:** `will my son get a government job`
**Outcome:** `NOT_YET_SUPPORTED`
**Candidate/target Questions:**
- HLKG-N-000406 `career.employment.government_job_occurrence` (OCCURRENCE) - "Will government employment be obtained within the stated horizon?"
**Bound parameters:** `{"subject": {"relation": "other", "relation_label": "child"}}`
**Notes:** Datatype supports other-subject; ACCEPTANCE is blocked pending CDQ-4. Explicit refusal, never a silent remap to self.

## Example 17: Novel paraphrase - honest NO_MATCH
**Utterance** (`en`): "Is a promotion on the cards for me" · traces to `TC-CAR-060`
**Normalised:** `is a promotion on the cards for me`
**Outcome:** `NO_MATCH_EXACT`
**Candidate/target Questions:**
- HLKG-N-000421 `career.advancement.promotion_occurrence` (OCCURRENCE) - "Will a promotion occur within the stated horizon?"
**Notes:** Exact resolution returns NO_MATCH (correct: resolution never guesses); Gate-2-style similarity surfaces the candidate as an ADVISORY for human-confirmed routing or alias-proposal.

## Example 18: Malformed input
**Utterance** (`en`): "xkqz vprt mlln" · traces to `TC-CAR-100`
**Normalised:** `xkqz vprt mlln`
**Outcome:** `NO_MATCH`
**Notes:** Non-language input; NO_MATCH is a first-class contract outcome, not an error.

## Cross-Example Observations

- Examples 1 vs 5 are the parameter rule in action: "when will I get promoted" (TIMING) and
  "will I get promoted before 2028" (OCCURRENCE + horizon) are DIFFERENT Questions - a
  binding never changes class (QRS s.8.4).
- Examples 3 vs 15 show one user journey split across two domains at the exam/appointment
  boundary - intake gets this right only because the boundary is written (Model 4.2).
- Example 12 is the live user-facing cost of the ALR-1/EVR-2 gap; ratifying a general
  job-timing node converts a disambiguation dialogue into a direct resolution.
- Every refusal outcome (OPTIONS_REQUIRED, NOT_YET_SUPPORTED, NO_MATCH) is a designed
  contract outcome with a next step - the pipeline never guesses.

## OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| CIE-1 | Disambiguation dialogue wording/locale strategy (example 12's prompt is illustrative, not ratified UX) | Intake UX layer |
| CIE-2 | Interim behaviour for scale-gated QUALITY questions (example 10 proposes refusal-citing-missing-scale; alternative: DESCRIPTION-class fallback) - owner call | QUALITY intake pre-CDQ-5 |
| Inherited | CPR-4 (relative horizon canonicalisation), CDQ-4, CDQ-5, ALR-1/EVR-2, CQL-3/ALR-2 | as recorded |

## Self-Audit Record

1. Consistency engineered: every plain-RESOLVED example machine-verified to exact-match a
   registered alias to the exact expected node; all slugs verified against records; 12
   examples trace to test-dataset scenario IDs - aliases, test dataset and examples are
   provably in sync at v0.1.0.
2. The verification loop caught a real defect in the first draft: the spelling-variant
   example used "will i get promtion", which is NOT a registered alias (the registry's
   variant is "when will i get promtion"). Fixed to the registered form and re-verified -
   and the correction sharpened the example's own lesson: variants resolve only if
   registered; unregistered misspellings correctly fall to NO_MATCH/Gate-2.
3. Verification scope stated honestly: RESOLVED_WITH_PARAMETERS utterances resolve via
   alias stem + extraction and are deliberately outside the exact-match assertion (their
   behaviour is asserted by the test dataset's parameter_binding scenarios instead).
4. QUALITY example 10 nearly showed a fabricated 1-5 rating - replaced with the honest
   scale-gated refusal and CIE-2 opened for the owner's interim-behaviour ruling.
5. Answer skeletons contain no methodology, no values, no confidence semantics (QQ-3
   untouched); `not_established` appears as a lawful outcome by design.
6. Known limitation: 18 examples cannot exercise every path (no DEPRECATED forwarding, no
   translation fallback); those await live-registry states and are claimed nowhere as
   covered.
