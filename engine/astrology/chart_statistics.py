"""
Chart Statistics
"""

from engine.models.chart import Chart


def planet_count(chart: Chart) -> int:
    return len(chart.planets)