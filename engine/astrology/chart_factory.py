"""
Chart Factory
"""

from engine.astrology.rashi_chart import rashi_chart
from engine.astrology.navamsa_chart import navamsa_chart
from engine.models.astronomy_snapshot import AstronomySnapshot


def build_all_charts(snapshot: AstronomySnapshot) -> dict:
    """
    Build all currently supported charts.
    """

    return {
        "D1": rashi_chart(snapshot),
        "D9": navamsa_chart(snapshot),
    }