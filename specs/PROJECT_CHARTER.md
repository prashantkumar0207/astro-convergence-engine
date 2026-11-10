<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED - adopted as the ACE Project Charter, `ADR-0015`/`ADR-0051` (owner-ratified 2026-08-17).** Subordinate to, and does not replace or supersede, `docs/PROJECT_CONSTITUTION.md`, which remains the governing constitution. The four adopted sections (Product motive, Analytical systems, Isolation protocol, Scientific limitation) are unedited. **The "Natal product contract" section is PROPOSED under `ADR-0117`**: owner-directed, pending independent CEO review and the owner's final ratification, and not binding until then. |
| Version | 1.2.0 |
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

## Natal product contract (v1.2.0; PROPOSED under `ADR-0117`, pending the owner's final ratification)

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

## Change history

| Version | Date | Change |
|---|---|---|
| 1.2.0 | 2026-11-10 | `ADR-0117` (PROPOSED): added the "Natal product contract" section on the owner's directive. The four adopted sections are unedited. |
| 1.1.0 | 2026-08-17 | `ADR-0051`: owner-adopted as the ACE Project Charter, subordinate to `docs/PROJECT_CONSTITUTION.md`. Sections above unedited. |
| 1.0.0 | 2026-08-17 | `ADR-0015` (PROPOSED): added the mandatory status header, absent since the bootstrap era. Sections above unedited. |
