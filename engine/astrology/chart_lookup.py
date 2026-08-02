"""
Chart Lookup
"""

from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def planet(chart: Chart, name: str) -> ChartPlanet:
    for p in chart.planets:
        if p.name == name:
            return p

    raise KeyError(name)