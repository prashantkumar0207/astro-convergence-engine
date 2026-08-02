from engine.models.chart import Chart


def test_chart():
    chart = Chart(planets=())

    assert chart.planets == ()