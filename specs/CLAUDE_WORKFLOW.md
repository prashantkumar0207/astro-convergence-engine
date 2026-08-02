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
