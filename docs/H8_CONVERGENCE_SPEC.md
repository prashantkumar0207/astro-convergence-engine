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

# H8. Convergence

## 1. Purpose

Convergence combines independently produced evidence from isolated analytical systems, preserves
their agreement and disagreement, and explains why they agree or disagree.

## 2. Convergence is not a confidence score

This is the central design constraint. A number that says 73 percent tells the user nothing they can
check, nothing they can argue with, and nothing that would let them notice the system is wrong.

Every convergent claim MUST retain and expose: the producing system, the rule, the calculation
provenance, where systems agree, where they disagree, evidence strength, the historical performance
of each contributing system for this event class and timing context, uncertainty, timing context,
and source provenance.

**The output MUST be able to explain WHY systems agree or disagree.** Not merely report that they
did. Two systems agreeing because they both derive from the same Moon position is a materially
weaker signal than two systems agreeing from independent significators, and a design that cannot
tell those apart is producing a number that means different things at different times.

## 3. Isolation before combination

Each system produces its evidence independently, with no visibility of any other system's output. A
result from one system MUST NOT become an input, a target, a weight or a hint for another. Cross-system
comparison happens only after each applicable system's result is frozen.

This is enforced today in the calculation layers by profile guarding, and the audit found that
enforcement inconsistent: drishti checks profile name and ayanamsa, the transit view checks name
only, and the primary transit event API checks nothing. Convergence will magnify any such leak,
because it is the layer that joins facts across systems.

## 4. Disagreement is a result, not a problem

The reporting vocabulary MUST include: strong convergence, moderate convergence, conflict,
insufficient evidence, and unresolved birth-data uncertainty. Conflict is a legitimate final answer
and must be presentable as one.

Suppressing disagreement to produce a cleaner answer is the single most damaging thing this layer
could do, because the disagreement is the honest signal.

## 5. Relationship to BTR

```
                     EVIDENCE
                        |
        +---------------+---------------+
        |               |               |
       BTR          PREDICTION      CONVERGENCE
```

Convergence MAY consume birth-data consistency information from BTR as one input among several. It
MUST NOT depend on BTR, and MUST produce a result when BTR has not run or is inconclusive. Making
convergence downstream of BTR would let a birth-time hypothesis silently gate all cross-system
analysis, which is precisely the failure the charter's BTR prohibition exists to prevent.

## 6. Prerequisites already satisfied, and one not

Satisfied: the sign-index conventions are explicit and machine-enforced, which was the documented
prerequisite for joining facts across layers, and school isolation is enforced in code at the
profile level.

Not satisfied, and recorded in the 2026-08-11 audit: D1 and the varga layers disagree about the
source sign inside the boundary-tolerance window, and both sign-convention gates step around that
seam by construction. Transit events carry no provenance object. Drishti provenance mislabels its own
house convention. Every one of these is a seam, and convergence is made entirely of seams. They
should be closed before convergence is implemented, not after.

## 7. Open questions requiring an owner decision

How weights are derived from measured historical performance, and whether weighting is permitted at
all before a defensible sample exists. Whether an unmeasured system contributes at all. How
convergence is reported when systems disagree and none has a track record. Whether the user sees
per-system detail by default.

## 8. Verification strategy

Isolation enforcement: a test that fails if one system's output can reach another's input.
Explanation completeness: every convergent claim decomposes into its contributing evidence.
Disagreement preservation across aggregation. A test that convergence produces a result with BTR
absent. Vocabulary coverage including conflict and insufficient evidence.

## 9. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. |
