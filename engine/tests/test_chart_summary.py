from engine.astrology.chart_summary import chart_summary
from engine.models.chart import Chart


def test_chart_summary():
    summary = chart_summary(Chart(planets=()))

    assert summary["planet_count"] == 0