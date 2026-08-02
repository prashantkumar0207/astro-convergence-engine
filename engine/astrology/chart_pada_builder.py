from engine.models.chart_pada import ChartPada


PADA_SPAN = (360.0 / 27.0) / 4.0


def build_chart_pada(number: int) -> ChartPada:
    nakshatra = ((number - 1) // 4) + 1

    start = (number - 1) * PADA_SPAN

    return ChartPada(
        number=number,
        nakshatra=nakshatra,
        start=start,
        end=start + PADA_SPAN,
    )