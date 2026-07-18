"""
Astronomy Result Model

Container for the complete deterministic astronomical computation.
"""

from dataclasses import dataclass

from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.aspect import Aspect


@dataclass(frozen=True)
class AstronomyResult:
    """
    Complete deterministic astronomical output.
    """

    snapshot: AstronomySnapshot
    aspects: tuple[Aspect, ...]