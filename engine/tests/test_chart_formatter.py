from engine.astrology.chart_formatter import format_chart
from engine.models.chart import Chart


def test_chart_formatter():
    assert format_chart(Chart(planets=())) == "Chart(0 planets)"