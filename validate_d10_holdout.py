from fractions import Fraction

from engine.astrology.dashamsa_chart import (
    dashamsa_longitude,
    dashamsa_sign,
)


DASHAMSA_SIZE = Fraction(3, 1)


def reference_start_sign(sign: int) -> int:
    """
    Independent Parashari Dashamsa starting-sign rule.

    Odd zodiac signs:
        Start from the source sign.

    Even zodiac signs:
        Start from the 9th sign from the source sign.

    Zero-based sign indices:
        0 Aries
        1 Taurus
        2 Gemini
        3 Cancer
        4 Leo
        5 Virgo
        6 Libra
        7 Scorpio
        8 Sagittarius
        9 Capricorn
        10 Aquarius
        11 Pisces
    """
    if sign % 2 == 0:
        return sign

    return (sign + 8) % 12


def reference(longitude: float):
    """
    Independent exact-reference calculation for Parashari D10.

    This function intentionally does not call any production
    Dashamsa helper.
    """
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
            f"expected {expected_longitude}, "
            f"got {actual_longitude}"
        )


# ------------------------------------------------------------
# 1. All 120 segment midpoints
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
# 3. Just below and just above every boundary
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
# 4. Normalization
# ------------------------------------------------------------

normalization_cases = 0

normalization_inputs = (
    360.0,
    720.0,
    -0.001,
    -30.0,
    -360.0,
    361.5,
)

for longitude in normalization_inputs:
    check(
        f"NORMALIZATION longitude={longitude}",
        longitude,
    )

    normalization_cases += 1


# ------------------------------------------------------------
# 5. Explicit classical anchor cases
# ------------------------------------------------------------

anchor_cases = {
    # longitude : expected D10 sign index
    1.5: 0,      # Aries 1°30' -> Aries
    34.5: 10,    # Taurus 4°30' -> Aquarius
    67.5: 4,     # Gemini 7°30' -> Leo
    100.5: 2,    # Cancer 10°30' -> Gemini
    133.5: 8,    # Leo 13°30' -> Sagittarius
    166.5: 6,    # Virgo 16°30' -> Libra
    199.5: 0,    # Libra 19°30' -> Aries
    232.5: 10,   # Scorpio 22°30' -> Aquarius
    265.5: 4,    # Sagittarius 25°30' -> Leo
    298.5: 2,    # Capricorn 28°30' -> Gemini
    301.5: 10,   # Aquarius 1°30' -> Aquarius
    334.5: 8,    # Pisces 4°30' -> Sagittarius
}

anchor_cases_count = 0

for longitude, expected_sign in anchor_cases.items():
    actual_sign = dashamsa_sign(longitude)

    if actual_sign != expected_sign:
        raise AssertionError(
            f"CLASSICAL ANCHOR mismatch at {longitude}: "
            f"expected sign {expected_sign}, "
            f"got {actual_sign}"
        )

    anchor_cases_count += 1


# ------------------------------------------------------------
# Report
# ------------------------------------------------------------

total_cases = (
    midpoint_cases
    + exact_boundary_cases
    + near_boundary_cases
    + normalization_cases
    + anchor_cases_count
)

print()
print("=" * 60)
print("INDEPENDENT PARASHARI DASHAMSA D10 VALIDATION")
print("=" * 60)
print(f"Midpoint cases        : {midpoint_cases} PASSED")
print(f"Exact boundary cases  : {exact_boundary_cases} PASSED")
print(f"Near-boundary cases   : {near_boundary_cases} PASSED")
print(f"Normalization cases   : {normalization_cases} PASSED")
print(f"Classical anchors     : {anchor_cases_count} PASSED")
print()
print(f"TOTAL CASES           : {total_cases}")
print()
print("RESULT: ALL INDEPENDENT PARASHARI D10 CASES PASSED")
print("=" * 60)