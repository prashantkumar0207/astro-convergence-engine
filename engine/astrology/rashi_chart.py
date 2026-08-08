"""
Rashi (D1) Chart Builder

Audit finding (section 5): this was previously a placeholder that
returned the snapshot unchanged, and the factory routed D1 to it,
leaving the real builder dead. It now delegates to the real D1
builder.
"""

from engine.astrology.chart_builder import build_chart
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.chart import Chart


def rashi_chart(snapshot: AstronomySnapshot) -> Chart:
    """
    Build the Rashi (D1) chart.
    """
    return build_chart(snapshot)
