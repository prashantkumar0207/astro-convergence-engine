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

# H2. Historical Event Ledger

## 1. Purpose

The ledger is the append-only record of what the user says actually happened, and of how the system
performed against it. It is the substrate of the product's USP, and the place where
PAST to TEST to LEARN to CONFIDENCE to FUTURE becomes a data structure rather than a slogan.

## 2. The chain, stated as obligations

**PAST.** The ledger holds confirmed events from H1. Nothing else counts as past.

**TEST.** For each event, the system records what each analytical system said, or would have said,
about that period, before knowing the outcome. The ordering matters: a test recorded after the
outcome is known is not a test.

**LEARN.** The ledger accumulates measured performance. In this phase LEARN means **measurement and
recorded performance only**. No statistical fitting, no weight learning, no parameter tuning, no
model training. That prohibition is not a scheduling convenience; moving from measurement to fitting
engages the anti-overfitting constitution directly and requires its own charter-level decision.

**CONFIDENCE.** Confidence is derived from measured performance and is always reported with the
sample size and the classes it was measured over. A confidence figure without its denominator is
prohibited.

**FUTURE.** Future-oriented output may cite ledger-derived confidence. It may never cite confidence
that was not measured.

## 3. Performance must be measured by class, not globally

A single accuracy number across all events is close to meaningless and actively misleading. Two
systems with identical global accuracy can be opposite in usefulness. Performance MUST be recorded
along at least: event class, timing context, producing system, rule, prediction type, and evidence
strength.

The practical consequence is that a system strong at career timing and weak at health timing is
visible as exactly that, which is the honest thing to tell a user and also the thing that makes
convergence weighting defensible later.

## 4. The anti-confirmation-bias rule

The system MUST NOT solicit only events that would support its own prior output. This is the
easiest way to build something that looks impressive and proves nothing.

Concretely: event elicitation MUST be capable of asking about periods where the system predicts
nothing notable, and the ledger MUST record which events were volunteered by the user versus
prompted by the system, because those two populations have different evidential weight and mixing
them destroys the distinction.

A hypothesis that the user rejects is evidence. It MUST be retained with the same permanence as a
confirmation. A ledger that keeps only its hits is a marketing artifact.

## 5. Holdout discipline

The ledger MUST support marking a subset of confirmed events as **protected**, unavailable to any
process that selects, tunes or rectifies. This is what makes BTR honest, and it is specified here
rather than in H7 because the protection has to exist in the store, not in the consumer.

Protected status is set once and cannot be cleared by any automated process. A holdout that can be
un-protected on demand is not a holdout.

## 6. Correction without destruction

Users misremember and then correct themselves. A correction appends a superseding record carrying
the reason, and every score computed from the superseded version remains in the ledger with a
pointer to what changed. Otherwise the system's own history of being wrong disappears, which is
exactly the history the USP depends on being able to show.

## 7. Open questions requiring an owner decision

Whether a protected holdout is chosen by the user, chosen randomly at ledger creation, or defined by
recency. The minimum sample size below which confidence is reported as insufficient rather than
computed. Whether rejected hypotheses are shown back to the user, which is a product and trust
decision as much as an engineering one.

## 8. Verification strategy

Append-only enforcement, including an attempt to overwrite. Holdout leakage detection: a test that
fails if any selection or rectification process reads a protected record. Class-partitioned scoring
correctness against hand-computed fixtures. A test that a rejected hypothesis is retained and
counted.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
