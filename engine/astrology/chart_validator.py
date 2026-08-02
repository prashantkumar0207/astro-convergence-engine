"""
Chart Validator
"""

from engine.models.astronomy_snapshot import AstronomySnapshot


def validate_chart(snapshot: AstronomySnapshot) -> bool:
    return snapshot is not None