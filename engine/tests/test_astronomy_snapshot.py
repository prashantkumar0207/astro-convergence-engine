from engine.astronomy.astronomy_snapshot import astronomy_snapshot


def test_astronomy_snapshot_returns_model():

    result = astronomy_snapshot(
        julian_day=2447719.968055556,
        latitude=25.5941,
        longitude=85.1376,
    )

    assert result.julian_day > 0

    assert len(result.planets.planets) == 12

    assert len(result.sidereal_planets) == 12

    assert result.ayanamsa.value > 0

    assert len(result.houses.houses) == 12