<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | ACCEPTED (`ADR-0113`, 2026-11-07). Specification only: no implementation is authorised by this document, and EVIDENCE entry needs CEO approval and the owner's explicit authorization. |
| Version | 2.0.0 |
| Owner | Project Owner (`ADR-0051` D4) |
| Last updated | 2026-11-07 |
| Review cadence | On amendment |

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

## 9. Mundane validation protocol (ADR-0021 D1, additive)

Section 5 requires protected holdout support in the store. Mundane validation adds a protocol
requirement on top, because its sample sizes make chance agreement likely in a way personal event
histories do not.

Every mundane validation run MUST be pre-registered per `docs/VALIDATION_STANDARD.md` section 5, and
the ledger MUST retain the registration alongside the results, so that the protocol as run can be
compared against the protocol as declared. A registration retained only outside the ledger is not
retained.

The ledger MUST record, per validation run: the hypotheses tested and their count, the events tested
and their count, the multiple-comparison method applied, the effect sizes observed, the negative
control results, and whether the run used the development set or the protected holdout.

**Rules must not be selected, modified or tuned using protected holdout results.** The store-level
protection in section 5 makes this enforceable rather than aspirational, which is why the protection
lives in the store.

Results reported without their hypothesis and event counts are incomplete, and the ledger should be
unable to emit them that way.

## 10. Ratified decisions and superseded wording (ADR-0113)

This section controls. Where earlier text differs from it, this section governs, and the earlier sentence stays only as
history.

**Ratified.** `ADR-0021` D1, pre-registration (s9).

**Decided.**
- **Holdout selection:** a protected holdout is selected before any protected validation, by a recorded, reproducible random
  procedure over a frozen eligible set. It is then locked against tuning, leakage and automated clearing.
- **Minimum N:** each pre-registered protocol fixes its minimum N before testing.
- **Rejected hypotheses:** they are retained and counted. Disclosure respects the protected-holdout access controls.

**Superseded, for the EVIDENCE phase.**
- **s2's CONFIDENCE and FUTURE steps, and s8's "class-partitioned scoring correctness".** In EVIDENCE the ledger records
  performance fields and their counts, and computes no confidence, score or weight (`Q8_CLOSURE_MATRIX.md` s6). Deriving
  confidence belongs to a later phase, under its own decision.
- **s9's reliance on `docs/VALIDATION_STANDARD.md` s5.** That document is `DRAFT`. The registration's contents are governed by
  `ADR-0021` D1 as ratified, and the reference is informative.

## 11. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
| 1.1.0 | 2026-08-11 | Additive section 9: the pre-registered mundane validation protocol per ADR-0021 D1. Sections 1 to 9 unmodified. |
| 2.0.0 | 2026-11-07 | **Promoted to ACCEPTED by `ADR-0113`.** Additive decisions section; superseded wording named, not deleted. |
