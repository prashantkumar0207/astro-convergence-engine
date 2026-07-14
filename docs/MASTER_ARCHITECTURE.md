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

# Master Architecture

## 1. Purpose and scope
TBD - one page maximum: what the system is, for whom, and what it will never be.
(Placeholder intentionally not filled: see docs/OPEN_QUESTIONS.md Q5.)

## 2. System context (C4 level 1)
TBD - context diagram: external actors, external systems, trust boundaries.

## 3. Container view (C4 level 2)
Established structural containers (skeleton stage):

| Container | Repository path | Responsibility (one line) | May depend on |
|---|---|---|---|
| Calculation engine | `engine/` | Deterministic domain-independent computation kernel(s) | nothing internal |
| Knowledge layer | `knowledge/` | Versioned, validated knowledge assets and their access contracts | TBD (Q6) |
| Application layer | `app/` | User-facing product(s) | engine, knowledge (via contracts) |
| Research | `research/` | Non-normative exploration | read-only on all |
| Tests | `tests/` | Cross-cutting verification and certification harnesses | all (test scope) |
| Tools | `tools/` | Build, validation, release tooling | all (dev scope) |

## 4. Dependency and boundary rules
- Runtime dependency direction: `app -> engine`; `app -> knowledge` via versioned contract only.
- `engine/` must remain importable in isolation (no knowledge/app imports).
- `research/` output enters production only by promotion through a decision log entry
  plus validation per VALIDATION_STANDARD.md.
- Frozen profiles/configurations are immutable per version; changes create a new version.

## 5. Cross-cutting concerns
TBD: determinism policy, error-handling policy, versioning policy (Q3), configuration
management, reproducibility requirements, licensing constraints (Q7).

## 6. Architecture decision index
This section indexes structural decisions; the binding text lives in DECISION_LOG.md.

| ADR | Title | Status |
|---|---|---|
| ADR-0001 | Canonical repository structure (this skeleton) | Accepted 2026-07-11 |

## 7. Change history
| Version | Date | Change |
|---|---|---|
| 0.1.0 | 2026-07-11 | Skeleton created |
