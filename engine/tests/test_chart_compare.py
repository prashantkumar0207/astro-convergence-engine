from engine.astrology.chart_compare import same_chart
from engine.models.chart import Chart


def test_same_chart():
    chart = Chart(planets=())

    assert same_chart(chart, chart)