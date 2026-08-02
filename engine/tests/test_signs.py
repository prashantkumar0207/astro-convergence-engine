from engine.astrology.signs import zodiac_sign


def test_zodiac_signs():
    assert zodiac_sign(0.0) == 1
    assert zodiac_sign(29.99) == 1
    assert zodiac_sign(30.0) == 2
    assert zodiac_sign(89.99) == 3
    assert zodiac_sign(180.0) == 7
    assert zodiac_sign(359.99) == 12