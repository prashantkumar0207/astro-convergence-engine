# Astro Convergence Engine Architecture

Version: 1.0

---

# Vision

Astro Convergence Engine is designed as a deterministic, extensible and
professional astrology platform.

The architecture must remain understandable even after thousands of source files
and many independent astrology systems.

The primary goals are:

- correctness
- determinism
- extensibility
- maintainability
- testability
- performance

---

# Layered Architecture

Dependency direction is strictly one-way.

API
↓
Calculations
↓
Astrology
↓
Knowledge
↓
Astronomy
↓
Models

No layer may depend on a higher layer.

Circular imports are prohibited.

---

# Models

Models represent immutable domain objects.

Models contain:

- data
- validation only when appropriate

Models never contain:

- business logic
- prediction logic
- calculations

---

# Astronomy

Astronomy is purely deterministic mathematics.

Responsibilities:

- Swiss Ephemeris
- Julian Day
- House Cusps
- Ayanamsa
- Planet Positions
- Sidereal Conversion

Astronomy never performs astrological interpretation.

---

# Knowledge

Knowledge is the single source of truth.

All static astrological knowledge belongs here.

Examples:

- Signs
- Planets
- Nakshatras
- Yogas
- Karakas
- Relationships
- Exaltation
- Debilitation
- Moolatrikona
- Dasha metadata
- KP metadata
- Jaimini metadata

Python modules must never duplicate knowledge data.

---

# Astrology

Astrology transforms deterministic astronomical data into
astrological meaning.

Astrology contains:

- Chart Construction
- Vargas
- Houses
- Lords
- Yogas
- Dashas
- Strengths
- KP
- Jaimini
- Nadi
- Interpretation

---

# Calculations

Calculations orchestrate engines.

Calculations never implement astrology rules.

---

# API

API exposes engine functionality.

API never contains astrology calculations.

---

# Testing

Every public function requires tests.

Regression tests are mandatory for every bug fix.

All commits must pass the complete test suite.

---

# File Creation Policy

Every file must earn its existence.

Create a new file only when:

- it represents a complete domain concept
- it improves maintainability
- it significantly reduces complexity

Avoid creating tiny one-function wrapper files.

---

# Metadata Policy

Static data belongs in Knowledge.

Algorithms belong in Astrology.

Mathematics belongs in Astronomy.

Never duplicate metadata.

---

# Package Size

Target:

10–20 files per package.

If a package grows significantly beyond this,
create subpackages grouped by domain.

---

# Refactoring Policy

Known architectural debt must not cross milestone boundaries.

Every milestone ends with:

- Architecture Review
- Refactoring
- Test Suite
- Git Tag

before the next milestone begins.

---

# Engineering Principles

Correctness over convenience.

Clarity over cleverness.

Composition over duplication.

Explicit over implicit.

Small cohesive modules over large monoliths.

Performance only after correctness.

Architecture before features.