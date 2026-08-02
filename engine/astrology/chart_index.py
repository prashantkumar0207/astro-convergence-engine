from engine.models.chart import Chart


def chart_index(chart: Chart):
    return {
        p.name: p
        for p in chart.planets
    }