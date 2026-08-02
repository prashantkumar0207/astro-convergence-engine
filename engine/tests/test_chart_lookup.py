from engine.astrology.chart_lookup import planet
from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def test_chart_lookup():
    chart = Chart(
        planets=(
            ChartPlanet("Sun", 50, 2, 20, 11, 4, 1),
        )
    )

    assert planet(chart, "Sun").sign == 2