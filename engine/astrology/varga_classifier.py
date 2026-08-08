"""
Generic Varga Classifier (Phase A)

The single algorithm of the generic framework. Its AUTHORITATIVE
output is the classification triple:

    d_sign          0-based sign in the divisional chart
    division_index  0-based division within the source sign
    fraction        position within the division, in [0, 1)

Expanded D-space longitude is deliberately NOT produced here: it is
a derived convention, canonical only where a certified module defines
it (D9/D10). Consumers that need a projected longitude must derive it
explicitly and own that decision (ADR refinement; structural outliers
such as D30 and D2 must never have longitude semantics silently
imposed on them).

Boundary policy: reuses engine.astrology.longitude_utils verbatim
(the Tier-0-locked convention). There is exactly one boundary policy
in this codebase; this module adds none.
"""

from dataclasses import dataclass

from engine.astrology.longitude_utils import (
    BOUNDARY_TOLERANCE,
    division_index as _uniform_division_index,
    normalize_longitude,
)
from engine.astrology.varga_rules import (
    CyclicVargaRule,
    SegmentVargaRule,
)


@dataclass(frozen=True)
class VargaClassification:
    """Authoritative classification of a longitude under a rule."""

    d_sign: int
    division_index: int
    fraction: float

    @property
    def division_number(self) -> int:
        """1-based division number (canonical A-6 style naming)."""
        return self.division_index + 1


def classify(longitude: float, rule) -> VargaClassification:
    """
    Classify a sidereal longitude under a varga rule.

    Normalization and the promote-up boundary tolerance come from
    the locked longitude utilities; the top edge is clamped; a
    tolerance-promoted value sits at fraction 0.0 of its new
    division (the same convention the certified D9/D10 modules
    implement).
    """
    longitude = normalize_longitude(longitude)

    source_sign = int(longitude // 30.0)
    degree = longitude - source_sign * 30.0

    if isinstance(rule, CyclicVargaRule):
        return _classify_cyclic(source_sign, degree, rule)

    if isinstance(rule, SegmentVargaRule):
        return _classify_segments(source_sign, degree, rule)

    raise TypeError(f"Unknown varga rule type: {type(rule)!r}")


def _classify_cyclic(
    source_sign: int,
    degree: float,
    rule: CyclicVargaRule,
) -> VargaClassification:
    width = 30.0 / rule.divisions

    index = _uniform_division_index(degree, width, rule.divisions)

    fraction = (degree - index * width) / width
    if fraction < 0.0:
        # Tolerance promoted the value into the next division; it
        # sits at that division's start (locked convention).
        fraction = 0.0

    start = rule.start_sign[source_sign]
    step = rule.direction[source_sign]

    d_sign = (start + step * index) % 12

    return VargaClassification(
        d_sign=d_sign,
        division_index=index,
        fraction=fraction,
    )


def _classify_segments(
    source_sign: int,
    degree: float,
    rule: SegmentVargaRule,
) -> VargaClassification:
    sign_segments = rule.segments[source_sign]

    cumulative = 0.0
    last = len(sign_segments) - 1

    for index, (width, target) in enumerate(sign_segments):
        cumulative += width

        # Promote-up convention: a degree within BOUNDARY_TOLERANCE
        # below a segment's upper edge belongs to the NEXT segment.
        if degree + BOUNDARY_TOLERANCE < cumulative or index == last:
            segment_start = cumulative - width

            fraction = (degree - segment_start) / width
            if fraction < 0.0:
                fraction = 0.0
            if fraction >= 1.0:
                # Top-edge clamp on the final segment (float
                # spillover at exactly 30 degrees is prevented by
                # normalization, so this only guards ULP dust).
                fraction = math_nextafter_below_one()

            return VargaClassification(
                d_sign=target,
                division_index=index,
                fraction=fraction,
            )

    raise AssertionError("unreachable: segment loop always returns")


def math_nextafter_below_one() -> float:
    import math

    return math.nextafter(1.0, 0.0)
