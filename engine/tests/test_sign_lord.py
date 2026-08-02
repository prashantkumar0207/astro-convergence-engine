from engine.astrology.sign_lord import sign_lord


def test_sign_lord():
    assert sign_lord(1) == "Mars"
    assert sign_lord(5) == "Sun"
    assert sign_lord(12) == "Jupiter"