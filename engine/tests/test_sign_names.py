from engine.astrology.sign_names import sign_name


def test_sign_name():
    assert sign_name(1) == "Aries"
    assert sign_name(12) == "Pisces"