<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED, C0 RESEARCH. Specification only. No implementation is authorised by this document. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# H4. Evidence Model, the central hub

## 1. Why this document matters more than its siblings

BTR, prediction and convergence are all sibling consumers of evidence. Historical validation scores
evidence. Every claim the product will ever make is an evidence item or an aggregate of them. A
wrong field here does not cause a local bug; it propagates into four layers and is expensive to
change once any of them exists.

The architecture is:

```
CALCULATION -> RULES -> INTERPRETATION -> EVIDENCE
                                            |
                        +-------------------+-------------------+
                        |                   |                   |
              HISTORICAL VALIDATION       BTR      PREDICTION      CONVERGENCE
```

Convergence is a sibling of BTR, not downstream of it. That is deliberate and is restated in H8.

## 2. The four-way separation this model enforces

**CALCULATION** is what the astronomy and the certified layers computed. Deterministic, certified,
reproducible.

**RULE** is what a named astrological system says a configuration means. Sourced, versioned,
attributable.

**INTERPRETATION** is a rule applied to a specific chart and question. Derived, traceable.

**EVIDENCE** is an interpretation with its historical performance and provenance attached, in a form
that can be counted, compared and disagreed with.

These MUST NOT collapse. The commonest way they collapse is an evidence item that carries a
conclusion but not the rule that produced it, at which point the system can no longer explain itself
and convergence degrades into an opaque score.

## 3. Required fields

**Identity and versioning.** A stable identifier and a schema version.

**Domain and question linkage.** Which question this bears on.

**Producing system.** Parashari, KP, Jaimini, BNN, CIL, Nakshatra Nadi, numerology, or a future
approved system. This field is mandatory and MUST survive every aggregation. Evidence normalisation
that erases which system produced a claim destroys the entire convergence design, and it is the
easiest mistake to make when building a scoring layer.

**Rule identity.** The rule identifier and version. An evidence item whose rule cannot be named is
not evidence; it is an assertion.

**Calculation provenance.** The full provenance of every calculated input, not a profile name. Two
facts computed under different ayanamsas must never be silently joined, and the only way to prevent
that is to carry enough provenance to detect it. The audit of 2026-08-11 found transit events carry
only a profile-name string and no provenance object, and that drishti provenance mislabels its own
house convention. Both must be fixed before either feeds evidence.

**Chart context.** Which chart or varga, which planets, houses, signs, significators.

**Timing context.** Which dasha period, which transit, which window. Timing is not decoration: the
historical-validation design scores by timing context, so it must be a field rather than prose.

**Polarity.** Positive, negative, neutral, contradictory, or insufficient. All five are required.
A model with only positive and negative forces contradictory evidence to be discarded or misfiled,
and preserved disagreement is the point of the whole system.

**Strength.** The rule's own claimed weight, separate from confidence.

**Confidence, decomposed.** Never a single number. At minimum: calculation confidence, rule
confidence, historical fit, cross-method convergence, timing convergence, birth-data consistency,
contradictory evidence present, and data completeness. A single unexplained confidence number is
prohibited by the charter and would be the first thing to erode trust when it is wrong.

**Historical performance.** The measured performance of this rule and system for this event class and
timing context, with its sample size. Absent when never measured, and absent must be distinguishable
from zero.

## 4. Prohibitions

Evidence MUST NOT be produced by an LLM inventing a rule. Only registered rules from H5 produce
evidence.

Evidence MUST NOT modify calculation. The dependency is one-directional and should be enforced
structurally, not by convention.

Evidence MUST NOT be aggregated into a score that cannot be decomposed back into its items.

## 5. Open questions requiring an owner decision

The identifier family. Whether strength is a rule property, a system property, or both. Whether
evidence is persisted or recomputed on demand, which is a reproducibility question: persisted
evidence can be audited against the engine version that produced it, recomputed evidence cannot be
audited at all after an engine change.

## 6. Verification strategy

A negative test proving an evidence item cannot be constructed without a rule identifier and full
provenance. Decomposability: every aggregate reproduces its inputs. Provenance-mismatch detection
across joined items. Coverage of all five polarities. A test that historical performance absent and
historical performance zero are distinguishable.

## 8. Multi-domain amendment (2026-08-11, additive)

Three fields are added, and one is added for a reason that is easy to miss.

**Entity.** Which entity this evidence concerns, per `docs/H0_ENTITY_MODEL_SPEC.md`.

**Domain.** Jataka, Varshaphal, Muhurta, Prashna or Mundane. Domain is orthogonal to producing
system: natal-Parashari and Varshaphal-Tajika are different pairs and MUST NOT be merged. The
mandatory-and-must-survive-aggregation rule stated for producing system applies identically to
domain.

**Chart reference.** Which chart produced this evidence, since an entity may carry several competing
charts.

The chart reference is not bookkeeping. It is what makes **shared-origin detection** possible.
Varshaphal derives from the natal chart by construction, so natal and Varshaphal agreeing is not two
independent confirmations; they share an origin and could hardly have disagreed. Without a chart
reference a convergence layer cannot tell that combination apart from two genuinely independent
sources, and it would systematically overstate confidence in precisely the combination the product
most wants to present. This is the same trap section 2 of `docs/H8_CONVERGENCE_SPEC.md` records for
two systems sharing a Moon position, in a sharper form.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
| 1.1.0 | 2026-08-11 | Additive section 8: entity, domain and chart reference, and the shared-origin rationale. Sections 1 to 7 unmodified. |
