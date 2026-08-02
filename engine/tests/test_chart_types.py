from engine.astrology.chart_types import ChartType


def test_chart_types_exist():
    assert ChartType.D1.value == "D1"
    assert ChartType.D9.value == "D9"
    assert ChartType.D10.value == "D10"
    assert ChartType.D60.value == "D60"