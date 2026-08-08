"""
Divisional Chart Dispatcher
"""

from typing import Any

from engine.models.astronomy_snapshot import AstronomySnapshot


def divisional_chart(
    snapshot: AstronomySnapshot,
    division: int,
) -> Any:
    """
    Build a supported divisional chart.

    D1 remains represented by the original AstronomySnapshot.
    D9 delegates to the deterministic Navamsa implementation.

    Unsupported divisions currently return the original snapshot
    unchanged until their dedicated calculations are implemented.
    """
    if division == 9:
        from engine.astrology.navamsa_chart import navamsa_chart

        return navamsa_chart(snapshot)

    return snapshot