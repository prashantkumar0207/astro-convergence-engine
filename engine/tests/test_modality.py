from engine.astrology.modality import modality


def test_modality():
    assert modality(1) == "Cardinal"
    assert modality(2) == "Fixed"
    assert modality(3) == "Dual"