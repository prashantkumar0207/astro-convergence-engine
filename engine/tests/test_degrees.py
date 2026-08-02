from pytest import approx

from engine.astrology.degrees import degree_in_sign


def test_degree_in_sign():
    assert degree_in_sign(0.0) == approx(0.0)
    assert degree_in_sign(29.99) == approx(29.99)
    assert degree_in_sign(30.0) == approx(0.0)
    assert degree_in_sign(35.5) == approx(5.5)
    assert degree_in_sign(182.25) == approx(2.25)
    assert degree_in_sign(359.99) == approx(29.99)