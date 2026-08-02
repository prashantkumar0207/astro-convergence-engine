from engine.astrology.nakshatra_names import nakshatra_name


def test_nakshatra_name():
    assert nakshatra_name(1) == "Ashwini"
    assert nakshatra_name(27) == "Revati"