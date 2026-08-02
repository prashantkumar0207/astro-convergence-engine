"""
Chart JSON
"""

import json
from dataclasses import asdict

from engine.models.chart import Chart


def chart_json(chart: Chart) -> str:
    return json.dumps(asdict(chart))