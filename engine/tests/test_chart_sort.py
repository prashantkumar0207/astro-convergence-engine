from engine.astrology.chart_sort import sort_chart
from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def test_chart_sort():
    chart = Chart(
        planets=(
            ChartPlanet("Moon", 100, 4, 10, 1, 8, 2),
            ChartPlanet("Sun", 50, 2, 20, 11, 4, 1),
        )
    )

    result = sort_chart(chart)

    assert result.planets[0].name == "Sun"