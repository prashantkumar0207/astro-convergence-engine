from engine.astrology.chart_index import chart_index
from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def test_chart_index_empty():
    assert chart_index(Chart(planets={})) == {}


def test_chart_index_real_chart():
    sun = ChartPlanet("Sun", 50, 2, 20, 11, 4, 1)
    result = chart_index(Chart(planets={"Sun": sun}))

    assert result["Sun"] is sun
