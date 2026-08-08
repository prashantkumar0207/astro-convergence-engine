"""
Chart Sorting Utilities
"""

from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def sort_chart(chart: Chart) -> tuple[ChartPlanet, ...]:
    """
    Planets sorted by longitude.

    Returns a tuple rather than a Chart: the previous version
    constructed an invalid Chart that dropped every non-planet
    field and violated the planets type contract (audit F-08).
    """
    return tuple(
        sorted(
            chart.planets.values(),
            key=lambda p: p.longitude,
        )
    )
