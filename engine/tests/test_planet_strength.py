import pytest

from engine.astrology.planet_strength import planet_strength


def test_planet_strength_is_explicitly_unimplemented():
    # Spec-correct replacement (audit Phase 12): the old test
    # locked in a placeholder 0.0 as if it were a real strength.
    with pytest.raises(NotImplementedError):
        planet_strength()
