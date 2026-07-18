import swisseph as swe

from engine.astronomy.aspects import aspect


def test_aspect_returns_model():

    result = aspect(
        swe.SUN,
        100.0,
        swe.MOON,
        190.0,
    )

    assert result.body1 == swe.SUN
    assert result.body2 == swe.MOON
    assert result.angle == 90.0