from engine.models.chart_sign import ChartSign


def build_chart_sign(number: int) -> ChartSign:
    start = (number - 1) * 30.0

    return ChartSign(
        number=number,
        start=start,
        end=start + 30.0,
    )