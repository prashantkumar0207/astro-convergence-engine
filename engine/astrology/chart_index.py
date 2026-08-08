from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def chart_index(chart: Chart) -> dict[str, ChartPlanet]:
    """
    Name -> planet mapping. Chart.planets is already keyed by
    name (audit finding F-08: this previously iterated the dict
    keys as if they were planet objects and crashed on real
    charts).
    """
    return dict(chart.planets)
