# Planet Position Engine Specification

## Purpose

The Planet Position Engine computes deterministic tropical geocentric planetary positions
from a Julian Day using the Swiss Ephemeris.

This module performs no:

- timezone conversion
- Julian Day calculation
- sidereal conversion
- interpretation
- prediction

It is purely an astronomical calculation module.

---

## Input

Julian Day (UTC)

Example

2457711.968055556

---

## Output

One immutable result for every supported body.

Each body contains:

- longitude
- latitude
- distance
- speed_longitude
- speed_latitude
- speed_distance

---

## Supported Bodies

Sun

Moon

Mercury

Venus

Mars

Jupiter

Saturn

Rahu (Mean Node)

Ketu (Derived)

Uranus

Neptune

Pluto

---

## Determinism

Same Julian Day

↓

Same Swiss Ephemeris Version

↓

Same Configuration

↓

Identical Output

---

## Responsibility

Input:

Julian Day

Output:

Raw Tropical Planet Positions

Nothing Else.