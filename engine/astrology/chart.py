"""
Birth Chart Entry Point
"""

from engine.astrology.chart_builder import build_chart
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.chart import Chart


def birth_chart(snapshot: AstronomySnapshot) -> Chart:
    """
    Build the D1 birth chart for a snapshot.
    """
    return build_chart(snapshot)
