"""
Chart Lookup
"""

from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def planet(chart: Chart, name: str) -> ChartPlanet:
    return chart.planets[name]
