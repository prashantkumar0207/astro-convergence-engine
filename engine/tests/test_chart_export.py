from engine.astrology.chart_export import export_chart
from engine.models.chart import Chart


def test_chart_export():
    chart = Chart(planets=())

    result = export_chart(chart)

    assert isinstance(result, dict)