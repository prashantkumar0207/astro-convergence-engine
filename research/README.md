# engine/

Deterministic calculation kernel(s). **No domain/business logic is implemented at skeleton
stage** (foundation rule 5/6).

Rules for this folder:
- MUST be importable in isolation: no imports from `app/`, `knowledge/`, `research/`.
- Every kernel ships with: frozen calculation/configuration profile, pinned dependencies,
  its own test suite, and certification evidence per `docs/VALIDATION_STANDARD.md`.
- Frozen profiles are immutable per version; behavioural change = new version + ADR.

Population note: importing the existing Tier-0 certified kernel is pending owner decision
(docs/OPEN_QUESTIONS.md Q9). Do not re-implement it here in the meantime.
