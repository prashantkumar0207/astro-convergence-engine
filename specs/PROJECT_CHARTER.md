<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED - adopted as the ACE Project Charter, `ADR-0015`/`ADR-0051` (owner-ratified 2026-08-17); its "Natal product contract" section owner-ratified under `ADR-0117` (2026-11-10).** Subordinate to, and does not replace or supersede, `docs/PROJECT_CONSTITUTION.md`, which remains the governing constitution. The four sections adopted in 2026-08 (Product motive, Analytical systems, Isolation protocol, Scientific limitation) are unedited, and the contract's text is unedited by its ratification. **The "Complete product contract" section is PROPOSED under the `ADR-0117` addendum**: pending the owner's separate approval, and not binding until then. |
| Version | 1.3.1 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-11-10 |
| Review cadence | TBD |

# Project Charter

## Product motive

Build a deterministic backend that accepts birth inputs, calculates reproducible chart data, runs multiple astrology methodologies as isolated evidence engines, verifies past events before future prediction, and lets an LLM explain deterministic evidence without inventing chart mathematics.

## Analytical systems

Parashari, DOB-based Pythagorean Numerology, R. G. Rao-style BNN, Umang Taneja-style Nakshatra Nadi, KP with Four-Step refinement, and CIL when its exact framework is reproducibly specified. Additional systems require their own specification and isolation rules.

## Isolation protocol

Each methodology starts from the same validated raw data but must derive its result independently. A result from one system must not become a target date, weighting signal, or interpretation hint for another system. Cross-system comparison occurs only after each applicable system result is frozen.

## Scientific limitation

Astrology and numerology are interpretive systems and are not scientifically validated predictive methods. Engineering certification in this repository refers to reproducibility and correctness against a frozen calculation specification, not proof of predictive validity.

## Natal product contract (v1.2.0; ACCEPTED, owner-ratified under `ADR-0117`)

This section states what the natal (Jataka) product must do. It adds to the sections above and removes or
narrows none of them.

### The mandatory natal flow

1. **Birth details.** The user supplies birth date, time and place, with their stated precision. Nothing
   else is required to begin.
2. **Blind historical prediction.** From the birth details alone, each applicable system independently
   predicts events in the user's past, each with an event class, a timing window, and the system and rule
   that produced it. The user is not asked for any historical life event before this, and none is used.
3. **Issuance before disclosure.** The predictions are frozen and recorded before any of them is shown to
   the user and before the user discloses any event. An issued prediction is never edited. Regenerating
   produces a new issuance beside the original, never a replacement.
4. **User verification.** The user confirms, partially confirms or rejects each prediction, or leaves it
   unanswered. Each answer is linked to the frozen prediction it answers. Events the user volunteers are
   recorded as volunteered, apart from answers.
5. **Evaluation.** Successes and failures are both kept and counted. Historical fit is evaluated against
   protected evidence, under a protocol registered before the protected data is read, with negative
   controls.
6. **Justified confidence only.** ACE states confidence only as far as step 5 supports it, and otherwise
   says that confidence is not established. Confidence is never manufactured.
7. **Explainable future predictions.** Each future prediction states its system, rule provenance,
   evidence, agreement and disagreement between systems, uncertainty, and the conditions under which it
   would be judged wrong.
8. **Prospective outcome tracking.** Each future prediction is issued before its window opens. Its actual
   outcome is appended later, and the prediction itself is never edited.

### Two kinds of prediction, two different guarantees

- A **historical prediction** concerns a period that has already happened, so it cannot be issued before
  its outcome. Its guarantee is that it was issued **before the user disclosed anything** about that
  period. Agreement with the user's answers is evidence of historical fit only.
- A **future prediction** is issued **before its window opens and before its outcome exists**. Only these
  predictions, tracked to their outcomes, can show predictive accuracy.

### Rules

- Users MUST NOT be required to provide historical life events before ACE issues its initial historical
  predictions. Volunteered events may be recorded, but they are never inputs to that first issuance.
- Historical confirmations alone MUST NOT be represented as proven future predictive accuracy.
- Preserved, not changed: the systems and qualifiers in "Analytical systems" (`ADR-0106` OR-2); the
  "Isolation protocol"; system and rule provenance on every result; disagreement between systems reported,
  never hidden; uncertainty carried through to every output; birth-time rectification optional, never
  required, and never the automatic explanation for a failed prediction; and the "Scientific limitation"
  section, unchanged.
- **Five domains.** The platform's scope is Jataka (natal), Varshaphal, Muhurta, Prashna and Mundane. The
  flow above is the natal contract. Varshaphal, Muhurta, Prashna and Mundane keep their own distinct
  workflows and are not forced into it. Their detailed design in `docs/PLATFORM_DOMAIN_ARCHITECTURE.md`
  stays `PROPOSED`; this Charter does not ratify it.

### Acceptance tests owed by future work

None is implemented by this amendment. Any work package that implements part of the natal flow must fix
the applicable tests among its exit criteria before coding, and must not narrow them.

| ID | Test | Required behaviour |
|---|---|---|
| AT1 | Blind historical prediction | For a person with no recorded events, historical predictions are issued from birth details alone. Adding, changing or answering any recorded event for that person does not change an issued set, and the issuing path reads no event, answer or ledger record. No system's prediction is an input to another system's prediction. |
| AT2 | Immutable issuance | Every prediction carries its event class, timing window, observable outcome, the conditions under which it is judged wrong, its system and rule references, and the engine and rule versions; one missing any is refused. A set is sealed by content hash, with its issuance recorded, before any part is shown; showing an unsealed set is refused; editing an issued prediction is refused; reissuing creates a new set and keeps the original. |
| AT3 | Reproducibility | The same birth details, engine version and rule versions reproduce a byte-identical prediction set. |
| AT4 | Prediction-to-answer linkage and failure preservation | Every answer references exactly one frozen prediction. Unanswered predictions are recorded as unanswered. Volunteered events are recorded apart from answers. Rejections and misses are retained and counted, and no interface removes or hides them. |
| AT5 | Feedback isolation | After users have answered, regenerating at the same versions yields the identical set. Answers cannot reach the issuing path. A rule changed in response to answers is a new rule version, evaluated only on evidence it has not seen. |
| AT6 | Protected validation and justified confidence | Confidence is derived only from a pre-registered protocol over a protected holdout, with negative controls such as shuffled dates or random windows, and is refused below the protocol's minimum sample. Protected answers are never readable for selection, tuning, rectification or development. Historical fit is never labelled future accuracy. |
| AT7 | Prospective prediction tracking | A future prediction's issuance precedes its window. Its outcome is appended afterwards; editing the prediction is refused. Predictive accuracy is reported only from these records, and separately from historical fit. |

### Charter compliance in reviews

Every future product review, architecture review, work-package definition, specification ratification
and decision paper that touches the natal flow, prediction, evidence, validation, birth-time
rectification, convergence or the user journey MUST state, with citations, how it complies with this
contract, or name each conflict for the owner to decide. A review without that statement is incomplete.
A reviewer does not resolve a conflict with this Charter; the Charter governs until the owner amends it
through a decision entry.

## Complete product contract (v1.3.0; PROPOSED under the `ADR-0117` addendum, pending separate owner approval)

This section completes the product contract across the whole user experience and all five domains. It is not binding
until the owner approves it. It does not edit the ratified "Natal product contract" above: where it adds detail to a
natal step, it adds and never narrows, and if the two ever appear to differ, the ratified section governs until the
owner decides. s10 proposes the two wording changes that reconcile them.

### 1. The question comes first, and is kept

1. The user asks a question or requests a general reading. ACE preserves the request verbatim, unchanged for the life
   of the record.
2. ACE identifies the request's intent, subject, domain, timeframe and required inputs, and records anything it could
   not resolve.
3. An ambiguous request is clarified with the user. An unsupported one is refused, with what was missing. Neither is
   answered by invention.

### 2. Each domain has its own workflow

- **Jataka (natal):** the natal contract above, completed by s3 to s8 below.
- **Varshaphal:** derived from the parent natal chart and the year. It needs the natal birth details by construction
  and inherits their uncertainty. It is not a second natal verification cycle.
- **Muhurta, general:** a purpose, a window and a place. It needs no birth details. It searches candidate moments and
  returns options with their reasons, the factors avoided, the search space and the number of candidates evaluated.
- **Muhurta, personalised:** general Muhurta plus the person's relevant chart factors, inheriting their uncertainty.
- **Prashna:** the question's own moment and place. It needs no birth details, and birth-time rectification never
  applies.
- **Mundane:** countries, companies, governments, institutions and dated public events. Competing charts for one
  entity are held separately with their sources, and disagreement between them is shown, never silently resolved.

Natal inputs are required only where a domain structurally depends on the natal chart: Varshaphal and personalised
Muhurta. No non-natal domain requires the natal verification cycle. Each domain follows the past-before-future
discipline through its own evidence and validation.

### 3. What "blind" means for natal historical predictions

1. Historical predictions are generated from birth data and registered, versioned rules only. The question is not an
   input to generation, so the same birth details and versions produce the identical set whatever the user asked (AT3).
2. After the generated set is frozen, the question selects which of its predictions are relevant to present and to
   answer from. The selection is recorded, and it selects by topic, never by a prediction's content or likely success.
3. Each issuance records what had been disclosed before it: historical facts in the opening question, earlier answers,
   volunteered events and stored event records. That record is made by a step separate from generation. None of these
   is an input to generation, and generation reads none of them (AT1).
4. A prediction counts as a blind success only if its event was not disclosed, by any of those routes, before the
   prediction was issued.
5. The whole generated set is frozen and versioned before any of it is presented, and before any answer is requested.

### 4. Every answer, and every non-answer, is kept

Confirmations, partial confirmations, rejections and reported non-events are answers. Each is kept as its own kind of
record and linked, immutably, to the one frozen prediction it answers. A presented prediction left unanswered is
recorded as unanswered against that prediction, and is never counted as a success or a failure. Volunteered events are
kept as their own records. They are not answers, and they need no prediction link.

### 5. Evaluation, independence and uncertainty

1. Historical fit is evaluated only under a protocol registered before the protected data is read, against protected
   holdouts, with negative controls, versioned rules and every recorded failure.
2. Each system's result keeps its system and rule provenance, and systems stay isolated.
3. Relationships between sources carry their class, with an explicit UNKNOWN state that is never treated as
   independence (`ADR-0113` s2 A; `ADR-0106` OR-4). The number of agreeing systems is only an upper bound on genuinely
   independent evidence.
4. Disagreement is reported, never netted away, and uncertainty is carried to every output.
5. Agreement is never presented as independent evidence. Historical fit is never presented as proven future accuracy.

### 6. Learning

1. Any change to rules or methods in response to evidence is versioned, recorded with the evidence that prompted it,
   and evaluated only on evidence it has not seen.
2. Protected holdouts are never used for tuning or selection.
3. Confidence is never manufactured.
4. Birth-time rectification is never invoked automatically to explain a failed prediction. Alternative causes come
   first. A birth time is never selected solely because it improves future prediction, and rectification must be able
   to conclude that the supplied time is sufficiently consistent.

### 7. ACE answers the original question

ACE returns to the user's preserved question, or to the scope of the general reading. It gives:

- the answer the evidence supports;
- timing, only where it is justified;
- the explanatory evidence, with system and rule provenance;
- uncertainty and limitations.

Where a reliable answer cannot be established, ACE says so and says why. The LLM explains this evidence and never
adds a claim, rule or calculation the evidence does not contain.

### 8. Future predictions and their outcomes

Future predictions are frozen before their outcome windows open. Actual outcomes are recorded afterwards, against the
frozen predictions. Prospective predictive performance is evaluated and reported separately from historical fit.

### 9. What stays fixed

- The calculation-certification requirements.
- The "Scientific limitation" section.
- The LLM's role as explainer of deterministic evidence, never inventor of chart mathematics ("Product motive").

No certified calculation is altered and no certification gate is weakened by this contract.

### 10. Proposed changes to the ratified natal wording (pending separate owner approval)

Starting from a question means the user may disclose historical facts before ACE issues anything, which two ratified
passages above do not allow for. Until the owner approves the replacements below, the ratified text stands unchanged.

**Natal flow, step 3.** Ratified text:

> 3. **Issuance before disclosure.** The predictions are frozen and recorded before any of them is shown to
>    the user and before the user discloses any event. An issued prediction is never edited. Regenerating
>    produces a new issuance beside the original, never a replacement.

Proposed replacement:

> 3. **Issuance blind to disclosure, before verification.** The predictions are generated without reference to
>    anything the user has disclosed, and are frozen and recorded before any of them is shown to the user and before
>    the user is asked to verify any of them. Historical facts the user disclosed before issuance, including any in
>    the opening question, are recorded as disclosed and never counted as blind successes. An issued prediction is
>    never edited. Regenerating produces a new issuance beside the original, never a replacement.

**Two kinds of prediction, the historical bullet.** Ratified text:

> - A **historical prediction** concerns a period that has already happened, so it cannot be issued before
>   its outcome. Its guarantee is that it was issued **before the user disclosed anything** about that
>   period. Agreement with the user's answers is evidence of historical fit only.

Proposed replacement:

> - A **historical prediction** concerns a period that has already happened, so it cannot be issued before
>   its outcome. Its guarantee is that it was **generated blind to anything the user disclosed and frozen before the
>   user verified it**. It counts as a blind success only for an event the user had not disclosed before it was
>   issued. Agreement with the user's answers is evidence of historical fit only.

### Further acceptance tests owed by future work

These add to AT1 to AT7 above. None is implemented by this amendment. Any work package that implements part of the
contract must fix the applicable tests among its exit criteria before coding, and must not narrow them.

| ID | Test | Required behaviour |
|---|---|---|
| AT8 | Question intake and routing | The request is stored verbatim and never altered. Intent, subject, domain, timeframe and required inputs are recorded, with anything unresolved. A request routed to an unregistered domain, or missing a required input, is refused or returned for clarification; no answer content is produced for it. |
| AT9 | Disclosure isolation | Each issuance records the disclosure state before it, through a step separate from generation, including historical facts in the opening question. Disclosed facts, earlier answers, volunteered events and stored event records are never inputs to generation. The question selects among frozen predictions by topic, the selection is recorded, and it never alters the generated set: the same birth details and versions yield the identical set whatever the question. A prediction whose event was disclosed before issuance is never counted as a blind success. |
| AT10 | Verification records | Every answer (a confirmation, partial confirmation, rejection or reported non-event) is stored as its own kind and linked immutably to exactly the one frozen prediction it answers. A presented prediction left unanswered is recorded as unanswered against that prediction and counted as neither success nor failure. Volunteered events are distinct records: they need no prediction link and are never counted as answers. |
| AT11 | System independence | No system's output reaches another system's input. Every result carries its system and rule provenance. An UNKNOWN relationship is never counted as independent, and agreeing systems never raise the independent-evidence count above the number of genuinely independent paths. Disagreement is reported, never netted. |
| AT12 | Feedback and learning protection | A rule changed in response to evidence is a new version, linked to that evidence, and evaluated only on evidence it has not seen. Protected holdouts are unreadable for tuning or selection. Rectification is never invoked automatically after a failed prediction, and never selects a birth time solely because it improves future prediction. |
| AT13 | Answering the original question | Every output references the preserved question or reading scope. It carries the supported answer, timing only where justified, its evidence, provenance, uncertainty and limitations, or an explicit statement that a reliable answer cannot be established and why. Text the LLM generates cannot introduce a claim, rule or calculation absent from the evidence. |
| AT14 | Domain boundaries | Varshaphal requires the parent natal record and inherits its uncertainty. General Muhurta and Prashna run with no birth details anywhere in the path. Personalised Muhurta inherits the personal chart's uncertainty. Muhurta cannot emit a result without its search space and candidate count. Prashna refuses rectification. Mundane analyses competing charts separately and surfaces their disagreement. No non-natal domain requires the natal verification cycle. |
| AT15 | End-to-end natal experience | One synthetic journey: question, routing, blind issuance, frozen presentation, verification, evaluation under protocol, answer to the original question, future prediction, and recorded outcome. Each stage leaves its record, and the final answer is reproducible from those records and versions. |
| AT16 | Certification preserved | Every certified calculation artifact is unchanged outside volatile fields, and every certification gate keeps its negative control. |

The "Charter compliance in reviews" obligation applies to this section as well, including question intake, domain
routing and answering the original question.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.3.1 | 2026-11-10 | `ADR-0117` addendum, revised after the CEO completeness HOLD (PROPOSED): s3, s4, AT9 and AT10 reconciled; s10 proposes two changes to ratified natal wording, pending separate owner approval. Ratified text unedited. |
| 1.3.0 | 2026-11-10 | `ADR-0117` addendum (PROPOSED): added the "Complete product contract" section and acceptance tests AT8 to AT16 on the owner's directive. Every earlier section is unedited. |
| 1.2.1 | 2026-11-10 | `ADR-0117` ratified by the owner: the "Natal product contract" section is ACCEPTED. Status text only; no section's content changed. |
| 1.2.0 | 2026-11-10 | `ADR-0117` (PROPOSED): added the "Natal product contract" section on the owner's directive. The four adopted sections are unedited. |
| 1.1.0 | 2026-08-17 | `ADR-0051`: owner-adopted as the ACE Project Charter, subordinate to `docs/PROJECT_CONSTITUTION.md`. Sections above unedited. |
| 1.0.0 | 2026-08-17 | `ADR-0015` (PROPOSED): added the mandatory status header, absent since the bootstrap era. Sections above unedited. |
