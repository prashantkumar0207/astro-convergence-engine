from engine.models.planet_position import PlanetPosition
from engine.models.ayanamsa import Ayanamsa
from engine.astronomy.sidereal_planets import sidereal_planet


def test_sidereal_planet_returns_model():
    tropical = PlanetPosition(
        longitude=100.0,
        latitude=1.0,
        distance=1.0,
        speed_longitude=0.98,
        speed_latitude=0.0,
        speed_distance=0.0,
    )

    ayanamsa = Ayanamsa(
        value=24.0,
        mode=1,
    )

    result = sidereal_planet(
        tropical,
        ayanamsa,
    )

    assert result.longitude == 76.0
    assert result.latitude == 1.0