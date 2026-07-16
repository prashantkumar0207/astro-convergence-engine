# Astro Convergence Engine

Version: 0.1.0

Status: Active Development

---

# Vision

Astro Convergence Engine is a deterministic astrology platform that produces reproducible astrological calculations and predictions.

The system is designed as an engineering platform rather than a traditional astrology application.

Every prediction must originate from deterministic astronomical calculations.

---

# Core Principles

1. Flutter never performs astrology calculations.
2. Python Engine is the single source of truth.
3. Every calculation must be deterministic.
4. Same inputs always produce identical outputs.
5. Every module must be independently testable.
6. Every calculation must be validated.
7. Every prediction must reference calculation evidence.
8. No external astrology API will ever be used.

---

# Repository Structure

docs/
app/
engine/
tests/
datasets/
research/
scripts/

---

# Current Architecture

Flutter App

↓

Service Layer

↓

Python Engine

↓

Swiss Ephemeris

↓

Calculation Pipeline

↓

Prediction Engine

↓

Flutter UI

---

# Current Progress

✅ Git Repository

✅ Documentation Structure

✅ Flutter Setup

✅ Android Build

✅ Navigation

✅ Forms

✅ Validation

✅ Loading Screen

✅ Result Screen

✅ Service Layer

❌ Swiss Ephemeris

❌ Geocoding

❌ Timezone Resolution

❌ Planet Calculation

❌ Ascendant

❌ Houses

❌ D-Charts

❌ KP

❌ BNN

❌ Prediction Engine

---

# Coding Rules

- UI contains no astrology calculations.
- Every module must have unit tests.
- Engine code is pure Python.
- Flutter communicates through services.
- Every public class requires documentation.

---

# Current Milestone

Milestone 1

Working Flutter Application

Status:

Completed

---

Next Milestone

Real Horoscope Calculation

Status:

In Progress