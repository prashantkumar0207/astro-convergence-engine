from engine.astrology.chart_json import chart_json
from engine.models.chart import Chart


def test_chart_json():
    text = chart_json(Chart(planets=()))

    assert isinstance(text, str)