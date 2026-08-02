from engine.astrology.chart_statistics import planet_count
from engine.models.chart import Chart


def test_planet_count():
    assert planet_count(Chart(planets=())) == 0