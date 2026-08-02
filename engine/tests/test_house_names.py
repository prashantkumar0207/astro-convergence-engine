from engine.astrology.house_names import house_name


def test_house_name():
    assert house_name(1) == "House 1"
    assert house_name(12) == "House 12"