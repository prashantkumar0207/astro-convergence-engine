"""
Divisional Chart Dispatcher

Audit finding F-15: unsupported divisions previously returned the
original D1 snapshot silently, so a caller asking for D60 received
D1 data disguised as a D60 result. Unsupported divisions now raise
UnsupportedVargaError.
"""

from typing import Any

from engine.astrology.chart_constants import SUPPORTED_VARGAS
from engine.models.astronomy_snapshot import AstronomySnapshot


#: Divisions with a real, independently verified implementation.
IMPLEMENTED_VARGAS = (1, 9, 10)


class UnsupportedVargaError(NotImplementedError):
    """Raised when a divisional chart is not implemented."""


def divisional_chart(
    snapshot: AstronomySnapshot,
    division: int,
) -> Any:
    """
    Build a supported divisional chart.

    D1 builds the real Rashi chart.
    D9 delegates to the certified Navamsa implementation.
    D10 delegates to the certified Dashamsa implementation.

    Any other division raises UnsupportedVargaError; a varga is
    only added once its classical rule is independently
    established and testable (audit Phase 9 requirement).
    """
    if division == 1:
        from engine.astrology.chart_builder import build_chart

        return build_chart(snapshot)

    if division == 9:
        from engine.astrology.navamsa_chart import navamsa_chart

        return navamsa_chart(snapshot)

    if division == 10:
        from engine.astrology.dashamsa_chart import dashamsa_chart

        return dashamsa_chart(snapshot)

    if division in SUPPORTED_VARGAS:
        raise UnsupportedVargaError(
            f"D{division} is a recognized varga but its rule is "
            f"not implemented yet. Implemented: "
            f"{IMPLEMENTED_VARGAS}."
        )

    raise UnsupportedVargaError(
        f"D{division} is not a recognized varga. Implemented: "
        f"{IMPLEMENTED_VARGAS}."
    )
