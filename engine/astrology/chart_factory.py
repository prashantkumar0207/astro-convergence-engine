from engine.astrology.chart_builder import build_chart
from engine.astrology.dashamsa_chart import dashamsa_chart
from engine.astrology.navamsa_chart import navamsa_chart
from engine.astrology.rashi_chart import rashi_chart
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.chart import Chart


def build_all_charts(snapshot: AstronomySnapshot) -> dict:
    return {
        "D1": rashi_chart(snapshot),
        "D9": navamsa_chart(snapshot),
        "D10": dashamsa_chart(snapshot),
    }


def build_master_chart(snapshot: AstronomySnapshot) -> Chart:
    return build_chart(snapshot)
