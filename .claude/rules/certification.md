# Certification and gate rules

Full detail: `docs/VALIDATION_STANDARD.md` (`Status: DRAFT` - cite accordingly), `specs/VALIDATION_PROTOCOL.md`,
`docs/CI_AND_ORACLE_REPRODUCIBILITY_SPEC.md`, `docs/PROJECT_CONSTITUTION.md` s12 ("Definition of Locked").

- **A stored certification artifact is history, not proof.** `certification/*.json` and
  `reports/certification/*` are regenerated evidence from a specific past run. Never hand-edit them.
  Never treat their presence as current proof of anything - regenerate to verify.
- **Never weaken a gate to make it pass.** If a gate fails and the failure looks wrong, the default
  hypothesis is that the gate is right and something else is broken. Only conclude the gate itself is
  defective after independent reproduction (see `ADR-0043` for a worked example: reproduce the failure
  locally first, then fix the gate's actual defect - narrowly - not the thing it's supposed to catch).
- **A gate that cannot fail is not evidence.** Any new or repaired gate needs a committed negative
  control proving it actually rejects a real violation.
- **Windows/Linux gate parity gap, known and permanent for now:** `swetest`-dependent certifiers
  (`certify_current_engine.py` and the oracle-tier `certify_*.py` scripts that need PyJHora) cannot run
  on this Windows host - the bundled reference binary is a Linux ELF binary. A failure to *run* one of
  these locally is a platform limitation, not a regression. The four governance/drift gate scripts
  (`check_adr_numbering.py`, `check_retired_identifiers.py`, `check_identifier_families.py`,
  `check_artifact_drift.py`) and the default `pytest` gate are pure Python and do run on this host -
  use them for local verification; rely on CI (`.github/workflows/ci.yml`) for the rest.
- **`VOLATILE` fields are the only precedent for "this difference doesn't matter."** Only run metadata
  (date, timestamp, source revision, working-tree-dirty flag, interpreter version) may be treated as
  non-substantive. Never extend that reasoning to a calculated value, tolerance, count, or verdict
  without an explicit decision entry.
- **Locked means all four of `PROJECT_CONSTITUTION.md` s12's conditions, not some.** Do not describe
  anything as "Locked" unless a decision entry records it as such per that section.
