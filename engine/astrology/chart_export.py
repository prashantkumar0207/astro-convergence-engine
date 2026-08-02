"""
Chart Export
"""

from dataclasses import asdict

from engine.models.chart import Chart


def export_chart(chart: Chart) -> dict:
    return asdict(chart)