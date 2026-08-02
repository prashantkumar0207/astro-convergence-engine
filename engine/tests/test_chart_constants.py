from engine.astrology.chart_constants import SUPPORTED_VARGAS


def test_supported_vargas():
    assert 1 in SUPPORTED_VARGAS
    assert 9 in SUPPORTED_VARGAS
    assert 60 in SUPPORTED_VARGAS