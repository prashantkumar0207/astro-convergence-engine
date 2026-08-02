from engine.astrology.pada import pada


def test_pada():
    assert pada(0.0) == 1
    assert pada(3.3333) == 1
    assert pada(3.3334) == 2
    assert pada(12.0) == 4