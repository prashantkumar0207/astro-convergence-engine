"""
Astronomy Pipeline

Builds a complete deterministic astronomy result from the
already-computed deterministic engines.

No astrological interpretation is performed here.
"""

from engine.models.astronomy_result import AstronomyResult
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.aspect import Aspect


def astronomy_pipeline(
    snapshot: AstronomySnapshot,
    aspects: tuple[Aspect, ...],
) -> AstronomyResult:
    """
    Combine deterministic astronomy outputs into one object.
    """

    return AstronomyResult(
        snapshot=snapshot,
        aspects=aspects,
    )