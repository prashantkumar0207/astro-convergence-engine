from engine.astrology.chart_sort import sort_chart
from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def test_chart_sort():
    moon = ChartPlanet("Moon", 100, 4, 10, 1, 8, 2)
    sun = ChartPlanet("Sun", 50, 2, 20, 11, 4, 1)

    chart = Chart(planets={"Moon": moon, "Sun": sun})

    result = sort_chart(chart)

    assert [p.name for p in result] == ["Sun", "Moon"]
