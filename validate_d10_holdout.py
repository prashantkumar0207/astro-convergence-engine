from fractions import Fraction

from engine.astrology.dashamsa_chart import (
    dashamsa_longitude,
    dashamsa_sign,
)


DASHAMSA_SIZE = Fraction(3, 1)

MOVABLE = {0, 3, 6, 9}
FIXED = {1, 4, 7, 10}


def reference_start_sign(sign: int) -> int:
    """Independent Dashamsa starting-sign rule."""
    if sign in MOVABLE:
        return sign

    if sign in FIXED:
        return (sign + 8) % 12

    return (sign + 4) % 12


def reference(longitude: float):
    """Independent D10 reference calculation."""
    x = Fraction(str(longitude)) % 360

    source_sign = int(x // 30)
    degree = x - source_sign * 30

    segment = int(degree / DASHAMSA_SIZE)

    if segment >= 10:
        segment = 9

    d10_sign = (
        reference_start_sign(source_sign) + segment
    ) % 12

    segment_start = segment * DASHAMSA_SIZE

    fraction = (
        degree - segment_start
    ) / DASHAMSA_SIZE

    d10_longitude = (
        Fraction(d10_sign * 30)
        + fraction * 30
    )

    return float(d10_longitude), d10_sign


def check(label: str, longitude: float):
    expected_longitude, expected_sign = reference(longitude)

    actual_sign = dashamsa_sign(longitude)
    actual_longitude = dashamsa_longitude(longitude)

    if actual_sign != expected_sign:
        raise AssertionError(
            f"{label}: SIGN mismatch at {longitude}: "
            f"expected {expected_sign}, got {actual_sign}"
        )

    if abs(actual_longitude - expected_longitude) > 1e-9:
        raise AssertionError(
            f"{label}: LONGITUDE mismatch at {longitude}: "
            f"expected {expected_longitude}, got {actual_longitude}"
        )


# ------------------------------------------------------------
# 1. Midpoint holdout
# 12 signs × 10 Dashamsas = 120 cases
# ------------------------------------------------------------

midpoint_cases = 0

for sign in range(12):
    for segment in range(10):
        longitude = (
            sign * 30
            + segment * 3
            + 1.5
        )

        check(
            f"MIDPOINT sign={sign} segment={segment + 1}",
            longitude,
        )

        midpoint_cases += 1


# ------------------------------------------------------------
# 2. Exact internal boundaries
# 12 signs × 9 boundaries = 108 cases
# ------------------------------------------------------------

exact_boundary_cases = 0

for sign in range(12):
    for boundary in range(1, 10):
        longitude = sign * 30 + boundary * 3

        check(
            f"EXACT sign={sign} boundary={boundary}",
            longitude,
        )

        exact_boundary_cases += 1


# ------------------------------------------------------------
# 3. Just below + just above boundaries
# 108 × 2 = 216 cases
# ------------------------------------------------------------

epsilon = 1e-9

near_boundary_cases = 0

for sign in range(12):
    for boundary in range(1, 10):
        longitude = sign * 30 + boundary * 3

        below = longitude - epsilon
        above = longitude + epsilon

        check(
            f"BELOW sign={sign} boundary={boundary}",
            below,
        )

        check(
            f"ABOVE sign={sign} boundary={boundary}",
            above,
        )

        near_boundary_cases += 2


# ------------------------------------------------------------
# 4. Normalization cases
# ------------------------------------------------------------

check("NORMALIZATION 360", 360.0)
check("NORMALIZATION 720", 720.0)
check("NORMALIZATION -0.001", -0.001)
check("NORMALIZATION -30", -30.0)

normalization_cases = 4


print()
print("=" * 60)
print("INDEPENDENT DASHAMSA D10 HOLDOUT VALIDATION")
print("=" * 60)
print(f"Midpoint cases       : {midpoint_cases} PASSED")
print(f"Exact boundary cases : {exact_boundary_cases} PASSED")
print(f"Near-boundary cases  : {near_boundary_cases} PASSED")
print(f"Normalization cases  : {normalization_cases} PASSED")
print()
print(
    "TOTAL CASES          : "
    f"{midpoint_cases + exact_boundary_cases + near_boundary_cases + normalization_cases}"
)
print()
print("RESULT: ALL INDEPENDENT DASHAMSA CASES PASSED")
print("=" * 60)