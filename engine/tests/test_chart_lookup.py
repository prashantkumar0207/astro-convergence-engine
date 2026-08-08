import pytest

from engine.astrology.chart_lookup import planet
from engine.models.chart import Chart
from engine.models.chart_planet import ChartPlanet


def test_chart_lookup():
    sun = ChartPlanet("Sun", 50, 2, 20, 11, 4, 1)
    chart = Chart(planets={"Sun": sun})

    assert planet(chart, "Sun").sign == 2


def test_chart_lookup_missing_raises():
    with pytest.raises(KeyError):
        planet(Chart(planets={}), "Moon")
