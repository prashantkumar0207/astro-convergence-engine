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

# H7. Birth-Time Rectification

## 1. Purpose and the failure mode this document exists to prevent

BTR assesses whether supplied birth data is consistent with confirmed history, and where the birth
time is genuinely uncertain, searches a declared candidate interval.

The failure mode it exists to prevent is simple and common: prediction failed, therefore the birth
time must be wrong. That reasoning makes a system unfalsifiable. It is prohibited here, structurally
rather than by exhortation.

## 2. Two modes

**Mode A, background consistency assessment.** Runs for every user with a stated birth time. Asks
whether confirmed events are consistent with the supplied data. Produces a consistency assessment,
never a replacement time.

**Mode B, dedicated rectification.** Runs only when the user declares their birth time uncertain and
supplies a candidate interval. Produces ranked candidates with evidence and confidence, never a
single answer presented as certain.

## 3. The mandatory failure-attribution order

Before birth-time uncertainty may be offered as an explanation for a failed historical fit, the
system MUST evaluate and record, in this order:

1. Astronomical and calculation correctness.
2. Calculation profile correctness.
3. Rule correctness.
4. Whether the selected system actually claims to predict this event class at all.
5. Conflicting methodologies.
6. Event data quality and date uncertainty.
7. Only then, birth-time uncertainty.

Each step MUST be recorded with its result. A BTR output that cannot show the first six were
evaluated is not a valid BTR output.

Step 4 deserves emphasis because it is the one most often skipped. Many failures are not failures:
the system was asked to explain an event class that the selected method makes no claim about.

## 4. The required conclusion

BTR MUST be capable of concluding **"birth details appear sufficiently consistent"** as a first-class
reportable outcome, not as a fallback or an absence of a result. A system that can only ever say the
birth time might be wrong is a system that will always say it.

Equally, BTR MUST be able to conclude that a failed prediction is more likely methodological or
evidential than birth-data related, and to say so.

## 5. Anti-overfitting

**Candidate birth times MUST NOT be selected solely by optimising future prediction success.** Future
success is unobservable at selection time; using it is either impossible or circular.

**Where candidate selection consumes historical events, an independent holdout of confirmed events
MUST remain unused by selection and available for validation.** The holdout is protected in the
ledger, per H2 section 5, not in this layer, so the protection cannot be bypassed by a consumer.

A candidate that fits every known event with nothing held back is indistinguishable from curve
fitting, and the specification must make that impossible by construction.

The rectification search space, the scoring function and the number of candidates evaluated MUST all
be recorded. A search that tries ten thousand candidates and reports the best one is doing something
statistically very different from a search that tries five, and the record must show which.

## 6. Immutability of user data

Original user-entered birth data is immutable. Candidates are separate objects, each carrying its own
evidence, confidence and the search that produced it. Nothing in the system may silently substitute a
candidate for the original.

This has a concrete prerequisite the audit surfaced: dasha timelines currently record only a float
Julian Day and no civil birth data, IANA zone or fold, so a timeline cannot today be attributed to
the birth record that produced it. That must be fixed before BTR can distinguish candidates.

## 7. Sensitivity, and why this layer is delicate

Moon longitude error propagates to dasha dates at 164 to 548 days per degree depending on the seed
lord. A one-hour birth-time ambiguity was measured to move the first mahadasha boundary by 101 days.
BTR is therefore both unusually powerful and unusually able to manufacture agreement. The
holdout requirement is what separates the two.

## 8. Open questions requiring an owner decision

How wide a candidate interval may be before rectification is refused as unconstrained. The minimum
number of confirmed events before Mode B may run at all. Whether candidates are ever shown to the
user or only used to qualify confidence. How consistency is reported when events are too few to
conclude anything, which must be distinguishable from consistency confirmed.

## 9. Verification strategy

A negative test proving BTR cannot be invoked as an explanation without the six prior steps recorded.
A holdout-leakage test that fails if selection reads a protected event. Immutability enforcement on
original birth data. A test that the sufficiently-consistent conclusion is reachable, using synthetic
data where it is the correct answer. A test that search-space size is recorded.

## 11. Multi-domain amendment (2026-08-11, additive)

BTR is **not universally applicable**, and treating it as such would reintroduce the failure this
document exists to prevent.

Applicability by entity shape, per `docs/H0_ENTITY_MODEL_SPEC.md` section 3:

**Shape A, origin moment.** Applicable, and only where origin certainty is `uncertain` or `reported`.
**Shape B, derived moment (Varshaphal).** Not independently applicable. Uncertainty is inherited from
the parent natal chart, so rectification happens on the parent or not at all.
**Shape C, query moment (Prashna).** Never applicable. The moment is known by construction, because
it is the moment the question was asked. There is no origin-time uncertainty to resolve.
**Shape D, no entity (General Muhurta).** Not applicable; there is no subject.

**BTR MUST refuse where origin certainty is `documented`.** A company incorporation timestamped by a
registry, or a treaty signed at a recorded hour, is documented fact. Rectifying against it would be
the prohibited reasoning of section 1 wearing a different hat: prediction failed, therefore the
documented time must be wrong. The refusal must be structural, gated on the entity field, not left to
the judgment of whoever invokes it.

**Search honesty.** Section 5 requires recording the search space and the number of candidates
evaluated. `docs/PLATFORM_DOMAIN_ARCHITECTURE.md` section 8 records that General Muhurta has the same
statistical shape, evaluating many candidates and reporting the best, and is therefore bound by the
same discipline. Neither may present "best of ten thousand" as "strongly indicated" without its
denominator.

## 12. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
| 1.1.0 | 2026-08-11 | Additive section 11: applicability by entity shape, the documented-origin refusal, and shared search honesty with Muhurta. Sections 1 to 10 unmodified. |
