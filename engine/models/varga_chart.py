from dataclasses import dataclass

from .provenance import Provenance
from .varga_planet import VargaPlanet, VargaPosition


@dataclass(frozen=True)
class VargaChart:
    """
    Generic divisional chart (Phase A model).

    Self-describing per the ADR: the varga number, the RESOLVED
    school (never implicit), and the astronomy Provenance the chart
    was computed from, so a future convergence layer can verify that
    joined facts share a calculation profile.
    """

    varga: int
    school: str
    ascendant: VargaPosition
    planets: dict[str, VargaPlanet]
    provenance: Provenance | None = None
