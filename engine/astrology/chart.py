"""
Birth Chart Builder
"""

from engine.models.astronomy_snapshot import AstronomySnapshot


def birth_chart(snapshot: AstronomySnapshot) -> AstronomySnapshot:
    """
    Initial chart builder.

    For now it simply returns the astronomy snapshot.
    Higher-level astrology layers will build on this.
    """
    return snapshot