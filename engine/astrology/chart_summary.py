"""
Chart Summary
"""

from engine.models.chart import Chart


def chart_summary(chart: Chart) -> dict:
    return {
        "planet_count": len(chart.planets),
    }