"""
Project-wide longitude normalization and division classification.

Remediates audit findings F-04 and A-3: the engine previously used
four different boundary conventions (D9 tolerance-promoted, D10
floor, nakshatra/pada naive floor, signs naive floor), and only
D9 guarded the float-modulo artifact where x % 360.0 returns
exactly 360.0 for tiny negative x.

CONVENTION (single, project-wide):

  A longitude exactly at a division boundary, or within
  BOUNDARY_TOLERANCE below it, belongs to the NEXT division, and
  the top edge is clamped so indices never exceed their range.

WHY 1e-10 DEGREES IS THE RIGHT TOLERANCE:

  - Upstream float arithmetic (modulo, subtraction, scaling) on
    degree values accumulates errors of at most a few times
    1e-13 degrees; 1e-10 absorbs that with almost three orders of
    magnitude of margin, so exact classical boundaries such as
    10 deg 00' 00" are classified deterministically even when the
    binary double undershoots the exact rational (for example
    360/27 > 40/3 in IEEE-754, which previously misclassified 74
    of 107 exact pada boundaries).
  - 1e-10 degrees is 0.36 microarcseconds. The certified
    ephemeris tolerance of this project is 0.5 arcseconds, six
    orders of magnitude larger, so the tolerance can never
    reclassify a value that is astronomically distinguishable
    from the boundary.

This is the same convention the certified D9 module introduced in
commit 16ccea2; it is now shared by every division computation.
"""

BOUNDARY_TOLERANCE = 1e-10


def normalize_longitude(longitude: float) -> float:
    """
    Normalize a longitude to the canonical [0, 360) range.

    Guards the IEEE-754 artifact where Python's float modulo
    returns exactly 360.0 for tiny negative inputs (for example
    -1e-16 % 360.0 == 360.0), which would otherwise leak
    out-of-range indices such as sign 13 into consumers.
    """
    longitude = longitude % 360.0

    if longitude >= 360.0:
        return 0.0

    return longitude


def division_index(value: float, size: float, count: int) -> int:
    """
    Return the zero-based division index of `value` within `count`
    consecutive divisions of width `size`, applying the project
    boundary convention (tolerance-promoted, top-clamped).
    """
    index = int((value + BOUNDARY_TOLERANCE) / size)

    if index >= count:
        index = count - 1

    return index
