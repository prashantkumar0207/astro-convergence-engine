# Knowledge Standards

## Purpose

This document defines the standards governing every knowledge asset used by the Astro Convergence Engine.

Knowledge assets contain canonical astrological facts only. They must remain independent from calculations, interpretations, and prediction logic.

---

# Core Principles

## Single Source of Truth

A fact shall exist in only one knowledge asset.

Example:

- Planet dignity belongs only in `dignities.json`
- Natural relationships belong only in `natural_relationships.json`

Facts must never be duplicated.

---

## Facts vs Interpretation

Knowledge files contain facts.

They do not contain:

- Predictions
- Explanations
- Probabilities
- Remedies
- Interpretations

Example:

Correct:

Sun element = Fire

Incorrect:

Sun gives leadership.

---

## Stable Identifiers

Every entity has a permanent identifier.

Examples:

PLANET_SUN

SIGN_ARIES

HOUSE_10

NAKSHATRA_ASHWINI

Identifiers never change once released.

---

## Versioning

Every knowledge file begins with:

{
    "schema_version": "1.0"
}

Schema changes require a version increment.

---

## Naming Convention

Identifiers:

UPPER_SNAKE_CASE

JSON keys:

snake_case

Display names:

Title Case

Examples:

english_name

sanskrit_name

moolatrikona

weekday

---

## Units

Angles:

Decimal degrees

Example:

10.0

Coordinates:

Degrees only

Time:

ISO 8601 where applicable.

---

## Enumerations

Enumerations shall be finite wherever possible.

Examples:

gender

element

modality

nature

guna

direction

Validation shall reject unknown values.

---

## Nullable Fields

Use null only when information is genuinely unavailable.

Never use empty strings.

---

## References

Knowledge files remain source-agnostic.

Supporting references are maintained separately in the research directory.

---

## Backward Compatibility

Knowledge schema changes should preserve compatibility whenever practical.

Breaking changes require a schema version update.

---

## Validation

Every knowledge asset must pass validation before being accepted into the repository.

Validation includes:

- Required fields
- Identifier uniqueness
- Enum validation
- Cross-reference validation
- Schema version validation

---

## Future Extensions

The schema shall support future additions without breaking existing data.

Examples:

KP

Jaimini

Nadi

BNN

Tajik

shall extend the engine through additional knowledge and rule layers rather than modifying canonical facts.