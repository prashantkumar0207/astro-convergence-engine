import swisseph as swe

from engine.astronomy.ayanamsa import ayanamsa


def test_ayanamsa_returns_model():
    result = ayanamsa(
        2447719.968055556,
        swe.SIDM_LAHIRI,
    )

    assert result.value > 0
    assert isinstance(result.mode, int)