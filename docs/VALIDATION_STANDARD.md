<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | DRAFT - placeholder skeleton, content pending |
| Version | 0.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-07-11 |
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

## 4. Change history
| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Initial standard distilled from Tier-0 certification practice |
