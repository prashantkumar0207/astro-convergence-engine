from engine.astrology.chart_validator import validate_chart


def test_chart_validator():
    assert validate_chart(object()) is True