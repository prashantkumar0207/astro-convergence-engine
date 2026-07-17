# Repository Architecture
**Project:** Astro Convergence Engine

Version: 1.0  
Status: LOCKED  
Last Updated: 17 July 2026

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