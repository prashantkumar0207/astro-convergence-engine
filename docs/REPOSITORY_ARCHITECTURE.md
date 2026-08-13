# Repository Architecture
**Project:** Astro Convergence Engine

Version: 1.0  
Status: HISTORICAL (superseded in part). Previously marked LOCKED; that lock is corrected below.  
Last Updated: 17 July 2026 (content). 2026-08-11 (status correction only).

---

# Status correction (ADR-0023 decision 4, PROPOSED, pending owner ratification)

This document was marked `LOCKED`. That status is **corrected to HISTORICAL** for two reasons, and
the correction is purely documentary. **No architectural rule in this document is rewritten, and no
code, test, certification artifact or calculated value changes because of it.**

**Reason 1: the lock was never recorded.** `PROJECT_CONSTITUTION.md` section 12 condition 4 requires
that a locked artifact be recorded by a decision entry. No entry in either decision register records
a lock on this document. A LOCKED marker that no decision supports is a claim the constitution does
not support, so it is withdrawn rather than retroactively justified.

**Reason 2: it conflicts with every other architecture document on one point.** This is the only
architecture document that places prediction and interpretation **inside** the knowledge layer.
`docs/MASTER_ARCHITECTURE.md`, `docs/ASTROLOGY_ARCHITECTURE.md` and
`docs/PLATFORM_DOMAIN_ARCHITECTURE.md` each separate them. Under the CALCULATION / RULE /
INTERPRETATION / EVIDENCE separation that the project charter treats as non-negotiable, that
placement is wrong, and leaving it LOCKED would give the wrong statement the strongest status in the
repository.

**What is authoritative for layering.** `docs/DECISION_LOG.md` ADR-0023 and ADR-0024, together with
`docs/PLATFORM_DOMAIN_ARCHITECTURE.md`. Where this document and those disagree about the position of
the knowledge, interpretation or prediction layers, **those govern**.

**What in this document remains useful and is not superseded.** The repository layout, the five
design principles, the module responsibility rules, the naming and commit conventions, and the
directory responsibilities. Those are unaffected by the correction and continue to describe the
repository accurately.

The section titled "Architecture Lock" below is read subject to this correction: it describes an
intent to keep the structure stable, which stands, and not a ratified lock, which never existed.

---

# Purpose

This document defines the architectural rules of the repository.

Every module, package, test, script and future contribution MUST follow this document.

Changing these rules requires an architectural decision and should not happen casually.

---

# Design Principles

The repository is built around five principles:

1. Deterministic calculations
2. Strict separation of responsibilities
3. Modular design
4. Test-driven engineering
5. Reproducible results

No module should perform work outside its responsibility.

---

# Repository Layout

```
astro-convergence-engine/

docs/
engine/

README.md
.gitignore
```

---

# Engine Layout

```
engine/

api/
astronomy/
calculations/
core/
ephemeris/
knowledge/
models/
services/
tests/
tools/
```

---

# Folder Responsibilities

## api/

Purpose

Application interfaces only.

Contains:

- FastAPI
- REST endpoints
- Request validation
- Response serialization

Must NOT contain:

- Business logic
- Mathematical calculations
- Astrology logic

---

## astronomy/

Purpose

Pure astronomical algorithms.

Examples

- Planet positions
- Coordinate transforms
- House systems
- Sidereal calculations
- Nutation
- Obliquity

---

## calculations/

Purpose

High-level astrology calculations.

Examples

- Natal chart
- Vargas
- Yogas
- Shadbala
- Ashtakavarga
- Dasha
- Transit

This package orchestrates lower-level engines.

---

## core/

Purpose

Deterministic mathematical foundation.

Contains only:

- Julian Day
- Timezone engine
- Validation
- Mathematical primitives

Rules

Must be deterministic.

Must have no business logic.

Must be independently testable.

---

## ephemeris/

Purpose

Swiss Ephemeris wrapper layer.

Responsibilities

- Ephemeris access
- Planet retrieval
- House retrieval
- Ayanamsha retrieval

No astrology logic.

---

## knowledge/

Purpose

Prediction engine.

Contains

- Rule engines
- Knowledge base
- Prediction logic
- Interpretation

---

## models/

Purpose

Data models.

Contains

- Pydantic models
- Immutable structures
- DTOs

No calculations.

---

## services/

Purpose

Infrastructure services.

Examples

- Timezone resolution
- File loading
- Configuration
- Utilities

No astrology.

---

## tests/

Purpose

Validation.

Every public engine must have tests.

---

## tools/

Purpose

Developer utilities.

Examples

- Code generation
- Scaffolding
- Maintenance scripts

Never imported by production code.

---

# Dependency Rules

Allowed direction

api
↓

calculations
↓

astronomy
↓

ephemeris
↓

core

models and services may be used where appropriate.

Forbidden:

- core importing knowledge
- core importing api
- core importing calculations
- ephemeris importing calculations
- tests imported by production code

---

# Naming Rules

Modules

snake_case.py

Classes

PascalCase

Functions

snake_case

Constants

UPPER_CASE

Private helpers

_prefix

---

# Testing Rules

Every deterministic module requires:

- unit tests
- regression tests
- reproducible inputs
- reproducible outputs

---

# Documentation Rules

Every public module must contain:

- purpose
- inputs
- outputs
- exceptions
- examples (where appropriate)

---

# Git Rules

Every commit should represent one logical change.

Recommended commit style:

feat:
fix:
refactor:
docs:
test:
chore:

---

# Architecture Lock

The repository structure defined in this document is considered the canonical architecture.

New folders should not be introduced unless there is a clear architectural need.

Existing responsibilities should not be mixed.

---

END OF DOCUMENT