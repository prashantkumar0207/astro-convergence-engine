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

# H6. Prediction Ledger

## 1. Purpose

The prediction ledger records what the system said would happen, before it happened, in a form that
can later be scored against what did. It closes the feedback loop and is the only route to a C5
claim.

## 2. The falsifiability requirement

A prediction that cannot fail is not a prediction. Every record MUST carry a stated window, a stated
observable outcome, and stated conditions under which it would be judged wrong. Vague predictions are
the mechanism by which astrology software appears accurate, and a system whose stated purpose is
demonstrable honesty cannot use it.

## 3. Required fields

Identity and version. The question it answers. The predicted outcome and its window. The evidence set
that produced it, by reference, so the prediction can be re-derived. Confidence, decomposed as in H4.
Engine version, rule versions, calculation profile. The falsification criteria. The timestamp of
issue, which must precede the window. And, once known, the outcome, its linked ledger event, and the
scoring.

Recording the engine and rule versions is what makes a five-year-old prediction interpretable. Without
them, a later scoring run cannot tell whether the system was wrong or merely different.

## 4. Immutability

A prediction is immutable once issued. Its outcome is appended. A prediction that can be edited after
the fact is worthless as evidence and worse than worthless as a trust mechanism.

## 5. The C5 gate

C5, prediction validated, is earned only through this ledger, over a protected population, with
pre-registered falsification criteria and a stated sample size. C4 is a claim about software
correctness. C5 is a claim about the world. **C4 MUST NEVER be represented as C5**, and no amount of
calculation certification constitutes scientific validation of astrology.

## 6. Open questions requiring an owner decision

The identifier family. Whether predictions are issued automatically or only on request. The minimum
sample before any aggregate accuracy is shown to a user. Whether users see their own scoring history,
which is a trust decision with arguments on both sides.

## 7. Verification strategy

Immutability enforcement. Issue-before-window ordering. Re-derivability of a prediction from its
recorded evidence set and versions. A negative test rejecting a prediction with no falsification
criteria.

## 8. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
