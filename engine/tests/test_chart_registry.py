from engine.astrology.chart_registry import supported_charts


def test_supported_charts():
    assert 9 in supported_charts()