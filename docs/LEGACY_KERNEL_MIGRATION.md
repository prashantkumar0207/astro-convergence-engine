| Field | Value |
|---|---|
| Status | DRAFT |
| Version | 0.1.0 |
| Owner | TBD |
| Last Updated | 2026-07-18 |

# Legacy Kernel Migration

## Purpose

This document records the engineering strategy for migrating the original certified Tier-0 astronomical kernel into the new modular engine architecture.

It is an engineering migration document only.

It is **not** an Architecture Decision Record (ADR).

---

# Current Repository State

The repository currently contains two implementations.

## Legacy Certified Kernel

Repository root:

- engine.py
- kp.py
- certify_tier0.py
- preflight.py
- finalize_report.py
- regression scripts
- certification assets

This implementation produced the Tier-0 Numerical Core certification recorded in CERTIFICATION_REPORT.md.

---

## New Modular Engine

Location:

```
engine/
```

Current modules include:

```
core/
models/
services/
calculations/
tests/
```

This implementation is under active development.

---

# Migration Principle

The certified kernel remains the reference implementation until equivalent functionality has been implemented, tested and validated inside the modular engine.

No functionality will be removed from the legacy kernel before equivalent behaviour exists in the modular architecture.

---

# Migration Strategy

Migration occurs incrementally.

Each migration follows this sequence:

1. Select one deterministic module.
2. Create specification.
3. Implement inside engine/.
4. Write unit tests.
5. Validate against the certified legacy implementation.
6. Record evidence.
7. Freeze behaviour.

Only after all certified functionality has been migrated may the legacy implementation be retired.

---

# Scope

This document governs migration only.

Architecture decisions remain in:

```
docs/DECISION_LOG.md
```

Repository architecture remains defined in:

```
docs/MASTER_ARCHITECTURE.md
```

---

END