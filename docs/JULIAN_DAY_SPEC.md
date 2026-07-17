# Julian Day Engine Specification

Version: 1.0

Status: Draft

---

## Purpose

Convert a timezone-aware UTC datetime into a deterministic Julian Day Number (JD).

This module is the mathematical foundation for all subsequent astronomical calculations.

---

## Inputs

UTC datetime

Requirements:

- timezone-aware
- valid datetime
- Gregorian calendar

---

## Outputs

Julian Day

Type:

float

Example:

2447719.968055556

---

## Responsibilities

The Julian Day Engine SHALL:

- Accept only UTC datetimes.
- Reject naive datetimes.
- Produce deterministic output.
- Delegate astronomical constants to Swiss Ephemeris where appropriate.

---

## Non-Responsibilities

The engine SHALL NOT:

- Calculate planetary positions.
- Calculate houses.
- Calculate ayanamsha.
- Perform timezone conversion.

Timezone conversion belongs exclusively to Time Service.

---

## Public API

```python
julian_day(datetime_utc) -> float
```

---

## Error Conditions

Raise ValueError if:

- datetime has no timezone
- datetime is not UTC

Raise TypeError if:

- input is not datetime

---

## Determinism

The same UTC datetime SHALL always produce the same Julian Day.

No external state.

No randomness.

---

## Unit Tests

Required:

- Valid UTC conversion
- Leap year
- Gregorian transition
- Invalid timezone
- Naive datetime
- Invalid type

---

## Validation

Compare output against Swiss Ephemeris reference values.

Maximum allowed error:

1e-9 day

---

END