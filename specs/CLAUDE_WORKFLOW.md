| Field | Value |
|---|---|
| Status | **ACCEPTED - ratified as the ACE agent-workflow specification, `ADR-0016`/`ADR-0051` (owner-ratified 2026-08-17).** Subordinate to the `ADR-0042` authority hierarchy (`PROJECT CONSTITUTION` -> `ENGINEERING CONSTITUTION` -> `DECISION LOG / ADR` -> ... -> `SPECIFICATIONS`); MUST NOT be read as an independent source of authority capable of overriding the Constitution or an accepted ADR. Substantive content below is unedited by ratification. |
| Version | 1.1.0 |
| Owner | TBD (docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# Claude Implementation Workflow

Claude is an implementation engineer, not the methodology authority or final certification authority.

For each derived tier:

1. ChatGPT/architecture workflow freezes the methodology specification and output schema.
2. Create a handoff package containing the specification, allowed dependencies, frozen upstream interfaces, fixtures, and explicit prohibited shortcuts.
3. Claude implements code, unit tests, and a manifest without modifying locked upstream tiers.
4. Returned code is audited against the specification.
5. Independent adversarial and untouched holdout tests are run.
6. If evidence passes, version and lock the tier. If it fails, record the defect and run a narrow correction iteration.

Two AI systems agreeing is not evidence of correctness. Executable evidence and independent validation are the judge.

## Change history
| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-17 | `ADR-0051`: owner-ratified as the ACE agent-workflow specification, subordinate to the `ADR-0042` hierarchy. Substantive content unchanged. |
| 1.0.0 | 2026-08-17 | G7 documentation repair (`docs/Q8_CLOSURE_MATRIX.md` s3): added the mandatory status header required by `docs/DOCUMENTATION_STANDARD.md` s2, previously missing entirely. Substantive content unchanged. |
