"""
Chart Sorting Utilities
"""

from engine.models.chart import Chart


def sort_chart(chart: Chart) -> Chart:
    return Chart(
        planets=tuple(
            sorted(
                chart.planets,
                key=lambda p: p.longitude,
            )
        )
    )