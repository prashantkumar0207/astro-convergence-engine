<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED - adopted as the ACE Project Charter, `ADR-0015`/`ADR-0051` (owner-ratified 2026-08-17).** Subordinate to, and does not replace or supersede, `docs/PROJECT_CONSTITUTION.md`, which remains the governing constitution. Substantive text below is unedited by adoption. |
| Version | 1.1.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# Project Charter

## Product motive

Build a deterministic backend that accepts birth inputs, calculates reproducible chart data, runs multiple astrology methodologies as isolated evidence engines, verifies past events before future prediction, and lets an LLM explain deterministic evidence without inventing chart mathematics.

## Analytical systems

Parashari, DOB-based Pythagorean Numerology, R. G. Rao-style BNN, Umang Taneja-style Nakshatra Nadi, KP with Four-Step refinement, and CIL when its exact framework is reproducibly specified. Additional systems require their own specification and isolation rules.

## Isolation protocol

Each methodology starts from the same validated raw data but must derive its result independently. A result from one system must not become a target date, weighting signal, or interpretation hint for another system. Cross-system comparison occurs only after each applicable system result is frozen.

## Scientific limitation

Astrology and numerology are interpretive systems and are not scientifically validated predictive methods. Engineering certification in this repository refers to reproducibility and correctness against a frozen calculation specification, not proof of predictive validity.

## Change history

| Version | Date | Change |
|---|---|---|
| 1.1.0 | 2026-08-17 | `ADR-0051`: owner-adopted as the ACE Project Charter, subordinate to `docs/PROJECT_CONSTITUTION.md`. Sections above unedited. |
| 1.0.0 | 2026-08-17 | `ADR-0015` (PROPOSED): added the mandatory status header, absent since the bootstrap era. Sections above unedited. |
