from engine.astrology.house import house_from_longitude


def test_house_from_longitude():
    assert house_from_longitude(15.0, 15.0) == 1
    assert house_from_longitude(45.0, 15.0) == 2
    assert house_from_longitude(75.0, 15.0) == 3
    assert house_from_longitude(345.0, 15.0) == 12