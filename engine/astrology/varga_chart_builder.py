"""
Generic Varga Chart Builder (Phase A infrastructure)

Builds a VargaChart from an AstronomySnapshot and a rule. Not used
by any production varga in Phase A (the registry is empty); it
exists so Phase D vargas plug in without new plumbing, and so the
provenance-propagation contract is testable now.
"""

from engine.astrology.varga_classifier import classify
from engine.models.astronomy_snapshot import AstronomySnapshot
from engine.models.varga_chart import VargaChart
from engine.models.varga_planet import VargaPlanet, VargaPosition


def build_varga_chart(
    snapshot: AstronomySnapshot,
    division: int,
    rule,
    school: str,
) -> VargaChart:
    """
    Classify the ascendant and every sidereal planet under `rule`.

    The snapshot's Provenance is passed through unchanged so the
    chart is traceable to its calculation profile.
    """
    asc = classify(snapshot.houses.ascendant, rule)

    ascendant = VargaPosition(
        source_longitude=snapshot.houses.ascendant,
        sign=asc.d_sign,
        division_number=asc.division_number,
        fraction=asc.fraction,
    )

    planets: dict[str, VargaPlanet] = {}

    for name, planet in snapshot.sidereal_planets.items():
        c = classify(planet.longitude, rule)
        planets[name] = VargaPlanet(
            name=name,
            source_longitude=planet.longitude,
            sign=c.d_sign,
            division_number=c.division_number,
            fraction=c.fraction,
        )

    return VargaChart(
        varga=division,
        school=school,
        ascendant=ascendant,
        planets=planets,
        provenance=snapshot.provenance,
    )
