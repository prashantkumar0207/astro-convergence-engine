"""
Chart Serializer
"""

from dataclasses import asdict

from engine.models.astronomy_snapshot import AstronomySnapshot


def serialize_chart(snapshot: AstronomySnapshot) -> dict:
    return asdict(snapshot)