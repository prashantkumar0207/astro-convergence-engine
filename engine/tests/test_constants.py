from engine.astrology.constants import (
    TOTAL_HOUSES,
    TOTAL_NAKSHATRAS,
    TOTAL_PADAS,
    TOTAL_SIGNS,
)


def test_constants():
    assert TOTAL_SIGNS == 12
    assert TOTAL_HOUSES == 12
    assert TOTAL_NAKSHATRAS == 27
    assert TOTAL_PADAS == 108