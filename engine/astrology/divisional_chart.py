"""
Divisional Chart Base
"""

from engine.models.astronomy_snapshot import AstronomySnapshot


def divisional_chart(
    snapshot: AstronomySnapshot,
    division: int,
) -> AstronomySnapshot:
    """
    Base implementation for all Vargas.

    Actual Vargas mathematics will be implemented later.
    """
    _ = division

    return snapshot