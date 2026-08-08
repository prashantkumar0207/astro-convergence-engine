from fractions import Fraction

from engine.astrology.navamsa_chart import (
    navamsa_longitude,
    navamsa_pada,
    navamsa_sign,
)

MOVABLE = {0, 3, 6, 9}
FIXED = {1, 4, 7, 10}

NAVAMSA_SIZE = Fraction(10, 3)
EPS = 1e-7


def reference_start_sign(sign):
    # Independent reference implementation:
    # movable -> same sign
    # fixed   -> 9th from sign
    # dual    -> 5th from sign
    if sign in MOVABLE:
        return sign
    if sign in FIXED:
        return (sign + 8) % 12
    return (sign + 4) % 12


def reference(longitude):
    x = Fraction(str(longitude)) % 360
    sign = int(x // 30)

    degree = x - sign * 30

    navamsa_index = int(degree / NAVAMSA_SIZE)
    if navamsa_index > 8:
        navamsa_index = 8

    d9_sign = (
        reference_start_sign(sign) + navamsa_index
    ) % 12

    navamsa_start = NAVAMSA_SIZE * navamsa_index
    fraction = (degree - navamsa_start) / NAVAMSA_SIZE

    d9_longitude = (
        Fraction(d9_sign * 30)
        + fraction * 30
    )

    return (
        float(d9_longitude),
        d9_sign,
        navamsa_index + 1,
    )


def check(label, longitude):
    expected_longitude, expected_sign, expected_pada = reference(longitude)

    actual_longitude = navamsa_longitude(longitude)
    actual_sign = navamsa_sign(longitude)
    actual_pada = navamsa_pada(longitude)

    if actual_sign != expected_sign:
        raise AssertionError(
            f"{label}: SIGN mismatch at {longitude}: "
            f"expected {expected_sign}, got {actual_sign}"
        )

    if actual_pada != expected_pada:
        raise AssertionError(
            f"{label}: PADA mismatch at {longitude}: "
            f"expected {expected_pada}, got {actual_pada}"
        )

    if abs(actual_longitude - expected_longitude) > 1e-9:
        raise AssertionError(
            f"{label}: LONGITUDE mismatch at {longitude}: "
            f"expected {expected_longitude}, got {actual_longitude}"
        )


# ------------------------------------------------------------
# 1. 108 midpoint holdout cases
# ------------------------------------------------------------

midpoint_cases = 0

for sign in range(12):
    for pada in range(9):
        longitude = (
            sign * 30
            + float((Fraction(pada) + Fraction(1, 2)) * NAVAMSA_SIZE)
        )

        check(
            f"MIDPOINT sign={sign} pada={pada + 1}",
            longitude,
        )

        midpoint_cases += 1


# ------------------------------------------------------------
# 2. Exact boundaries + just below + just above
# ------------------------------------------------------------

boundary_cases = 0

for sign in range(12):
    for boundary in range(9):
        boundary_degree = boundary * NAVAMSA_SIZE

        longitude = sign * 30 + boundary_degree

        # Exact boundary
        check(
            f"EXACT sign={sign} boundary={boundary}",
            longitude,
        )
        boundary_cases += 1

        # Just below, except 0° where previous Navamsa wraps
        if boundary > 0:
            below = longitude - EPS

            check(
                f"BELOW sign={sign} boundary={boundary}",
                below,
            )
            boundary_cases += 1

        # Just above
        if boundary < 9:
            above = longitude + EPS

            check(
                f"ABOVE sign={sign} boundary={boundary}",
                above,
            )
            boundary_cases += 1


print()
print("=" * 60)
print("INDEPENDENT NAVAMSA HOLDOUT VALIDATION")
print("=" * 60)
print(f"108 midpoint cases : {midpoint_cases} PASSED")
print(f"Boundary cases     : {boundary_cases} PASSED")
print()
print("RESULT: ALL INDEPENDENT NAVAMSA CASES PASSED")
print("=" * 60)
