from engine.astrology.chart_index import chart_index
from engine.models.chart import Chart


def test_chart_index():
    assert chart_index(Chart(planets=())) == {}