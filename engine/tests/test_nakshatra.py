from engine.astrology.nakshatra import nakshatra


def test_nakshatra():
    assert nakshatra(0.0) == 1
    assert nakshatra(13.3333) == 1
    assert nakshatra(13.3334) == 2
    assert nakshatra(359.99) == 27