"""
Exact-rational KP interval mathematics (KP_CHAIN_V1, ADR-KP-001).

Numeric contract (Decision KP-A, approved 2026-08-09)
-----------------------------------------------------
The KP layer classifies EXACT RATIONAL longitudes with [start, end)
interval ownership: a longitude exactly on a boundary belongs to the
interval that STARTS there. There is NO float promotion tolerance in
this layer. Float inputs are converted through Decimal(str(x)), which
preserves the decimal spelling of ephemeris output rather than the
raw IEEE-754 binary expansion (Fraction(float) would).

Relationship to the engine-wide float convention: the engine's
longitude_utils promotes floats within 1e-10 degrees below a division
boundary up to it. The two conventions agree everywhere except floats
lying within 1e-10 below an exact KP boundary, where this layer keeps
the certified legacy classification. This is a deliberate, documented,
school-specific policy, NOT a hidden second convention: it preserves
bit-exact equivalence with the certified legacy kernel (legacy/kp.py)
under the zero-categorical-mismatch rule (DECISION_LOG D-003). Every
chain result carries nearest_boundary_arcsec so consumers can flag
boundary-critical outputs.

The mathematics below is migrated verbatim from legacy/kp.py and is
covered by an exact equivalence gate against it.
"""

from decimal import Decimal
from fractions import Fraction

from engine.kp.tables import KP_YEARS, NAK_SPAN


def to_exact(value) -> Fraction:
    """
    Convert a longitude-like value to an exact Fraction.

    Floats are converted via Decimal(str(value)) to preserve their
    decimal spelling (the certified legacy conversion rule).
    """

    if isinstance(value, Fraction):
        return value
    if isinstance(value, Decimal):
        return Fraction(value)
    if isinstance(value, int):
        return Fraction(value)
    if isinstance(value, float):
        return Fraction(Decimal(str(value)))
    return Fraction(Decimal(str(value)))


def walk(position: Fraction, start_index: int, span: Fraction):
    """
    Walk the 9-lord Vimshottari cycle across ``span`` starting at
    ``start_index`` and return (lord_index, offset_into_interval,
    interval_width) for the interval owning ``position`` under the
    [start, end) rule.
    """

    accumulated = Fraction(0)
    for step in range(9):
        index = (start_index + step) % 9
        width = span * KP_YEARS[index] / 120
        if position < accumulated + width:
            return index, position - accumulated, width
        accumulated += width
    raise ArithmeticError("interval walk fell through")


def all_boundaries() -> list:
    """
    Every nakshatra, sub, and sub-sub start boundary in [0, 360),
    as exact Fractions, sorted ascending. Verification helper for
    tests and validators; not used by production classification.
    """

    bounds = set()
    for nak in range(27):
        base = nak * NAK_SPAN
        bounds.add(base)
        star_index = nak % 9
        accumulated = Fraction(0)
        for step in range(9):
            index = (star_index + step) % 9
            width = NAK_SPAN * KP_YEARS[index] / 120
            sub_start = base + accumulated
            bounds.add(sub_start)
            inner = Fraction(0)
            for step2 in range(9):
                inner_index = (index + step2) % 9
                inner_width = width * KP_YEARS[inner_index] / 120
                bounds.add(sub_start + inner)
                inner += inner_width
            accumulated += width
    return sorted(bounds)
