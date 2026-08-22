# Validation rules

Full detail: `docs/VALIDATION_STANDARD.md` (`Status: DRAFT` - cite accordingly, not as ratified).

- **A skip is a failure, not a pass.** A certification or validation suite that skips a case has not
  verified that case.
- **Independent references and untouched holdouts are what make a validation real.** A test that
  compares a function's output to itself, or to data the same code produced, proves internal
  consistency, not correctness. Prefer an external reference (an oracle, a second transcription, a
  closed-form check) wherever one exists.
- **Anti-fitting**: do not tune thresholds, tolerances, or logic against the specific holdout cases
  meant to validate them. If a holdout fails, the fix is in the implementation or a recorded,
  independently-justified change to the specification - never a tolerance widened until the case
  passes.
- **Every claim in a report needs a run behind it.** "This should work" or "this looks right" is not a
  validation result. Run it, then say what happened.
