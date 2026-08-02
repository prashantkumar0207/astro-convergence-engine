from engine.models.chart_planet import ChartPlanet


def test_chart_planet():
    planet = ChartPlanet(
        name="Sun",
        longitude=125.5,
        sign=5,
        degree=5.5,
        house=2,
        nakshatra=10,
        pada=2,
    )

    assert planet.name == "Sun"
    assert planet.sign == 5