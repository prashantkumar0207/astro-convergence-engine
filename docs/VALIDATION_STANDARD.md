<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - sections 1 to 3 as distilled 2026-07-11; sections 5 and 6 added 2026-08-11 per ADR-0021 |
| Version | 0.2.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# Validation Standard

Defines what counts as proof in this project. Applies to all folders.

## 1. Claim classes and required evidence
| Claim | Required evidence |
|---|---|
| "Works" | Automated test in `tests/`, passing in CI, reproducible locally by one documented command |
| "Accurate / within tolerance" | Absolute-error comparison against an independent authoritative reference, with pinned inputs, versions and checksums; tolerance stated in absolute units, never percentages, unless a decision entry justifies otherwise |
| "Certified / locked" | A dedicated reproducible certification harness: fresh-environment one-command run, machine-readable results + human-readable report generated in the same run, console/report agreement |
| "Faster / better" | Benchmark with fixed seed/inputs, environment recorded, baseline committed |

## 2. Non-negotiable rules
1. **Independence:** the reference used to certify must not be derived from the code under test.
2. **Holdout discipline:** cases used to tune or debug can never alone certify; a genuinely
   untouched holdout set is mandatory.
3. **No silent fallback:** degraded modes must fail loudly in certification contexts.
4. **Reproducibility:** zero machine-specific absolute paths; pinned dependencies; checksummed
   data assets verified before any certification run.
5. **Skips are failures** in certification suites: a missing mandatory dependency fails the run.
6. **Anti-fitting:** automated scans for hard-coded per-case corrections are part of the gate;
   findings must be cleared with written justification.
7. **Boundary testing:** interval/threshold logic is tested below/at/above every boundary with
   exact arithmetic where representable.
8. **Stored results are history, not proof:** every certification re-executes calculations.

## 3. Evidence retention
Machine-readable results, raw reference outputs, and the exact console transcript are
committed or released alongside the claim. Historical artifacts live under a clearly marked
path and are never read by live pipelines.

## 4. Empirical validation of astrological methods (ADR-0021 D1, normative)

Sections 1 to 3 govern whether software computes what it claims. This section governs a different
and harder claim: whether a specified astrological method, under a specified protocol, performed as
described against historical evidence. The two must never be conflated.

**Pre-registration is mandatory.** Before any protected testing run, the protocol MUST define: the
event classes; the hypotheses and rules under test; the development or training historical set; the
protected holdout historical set; the number of hypotheses tested; the number of events tested; the
multiple-comparison methodology; the effect-size measures; negative controls where feasible; and
replication requirements where feasible.

Whether a protocol was registered before the protected run is a checkable fact, not a judgment, and
it MUST be recorded as such.

**Rules MUST NOT be selected, modified or tuned using protected holdout results.** This extends s2
rule 2 from calculation certification to empirical validation, where the temptation is greater
because the search space is larger.

**Statistical significance MUST NEVER be represented as scientific proof of astrology.** It is
evidence about the measured performance of a specified method under a specified protocol, and it MUST
be stated in those terms wherever it appears, including in any user-facing surface.

**Reporting the selected result without the search is prohibited.** The number of hypotheses tested
and the number of events tested are part of the result, not context for it. A finding reported
without its denominator is not a finding.

**Negative controls.** Where a true control group does not exist, a permuted-data control usually
does: run the same rules against entity charts randomly reassigned, or events shifted to random
dates, to obtain an empirical null. A rule that scores as well against shuffled data as against real
data has demonstrated a property of the protocol, not of the rule.

## 5. The independence principle (ADR-0021 D5, normative)

> **Absence of measured correlation is not evidence of independence.**

Four non-equivalences follow, each stated because each has been assumed somewhere in practice:
an unknown relationship is not independent; a derived relationship is not independent; a
shared-origin relationship is not independent; a correlated relationship is not independent.

This governs any aggregation of evidence anywhere in the system, not only convergence. Wherever
agreement is counted, weighted or scored, the dependency structure between the agreeing sources MUST
be established or explicitly recorded as unknown, and unknown MUST NOT be treated as independent.

The count of agreeing sources is an **upper bound** on the number of genuinely independent evidence
paths, never an estimate of it.

## 6. Change history
| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Initial standard distilled from Tier-0 certification practice |
| 0.2.0 | 2026-08-11 | Additive sections 5 and 6: pre-registered empirical validation of astrological methods, and the independence principle, per ADR-0021. Sections 1 to 3 unmodified. |
