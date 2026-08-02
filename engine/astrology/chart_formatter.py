from engine.models.chart import Chart


def format_chart(chart: Chart) -> str:
    return f"Chart({len(chart.planets)} planets)"