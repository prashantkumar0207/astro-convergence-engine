"""
Divisional Chart Dispatcher (school-aware since Phase A)

Audit finding F-15: unsupported divisions previously returned the
original D1 snapshot silently. Unsupported divisions and schools
raise UnsupportedVargaError.

Phase A of the Generic Varga Architecture ADR adds the explicit
`school` parameter and routes unknown (division, school) pairs
through the varga registry. D1, D9 and D10 remain hard-wired to
their certified implementations, byte-for-byte unchanged; the
registry is empty in Phase A, so behavior for every division is
exactly as before, with the school dimension now explicit.
"""

from typing import Any

from engine.astrology.varga_registry import (
    DEFAULT_SCHOOL,
    UnsupportedVargaError,
    get_varga_rule,
)
from engine.models.astronomy_snapshot import AstronomySnapshot


#: Divisions served by certified, independently verified modules.
IMPLEMENTED_VARGAS = (1, 9, 10)


def divisional_chart(
    snapshot: AstronomySnapshot,
    division: int,
    school: str | None = None,
) -> Any:
    """
    Build a supported divisional chart.

    D1 builds the real Rashi chart. D9 and D10 delegate to their
    certified implementations. Any other (division, school) is
    looked up in the varga registry and raises
    UnsupportedVargaError until a rule is registered under the full
    ADR certification protocol.

    `school` is explicit; None resolves to the varga's documented
    default ("parashara"). The certified D1/D9/D10 implementations
    ARE the Parashara school; requesting any other school for them
    raises rather than silently substituting.
    """
    resolved_school = school if school is not None else DEFAULT_SCHOOL

    if division in IMPLEMENTED_VARGAS:
        if resolved_school != DEFAULT_SCHOOL:
            raise UnsupportedVargaError(
                f"D{division} is implemented only for the "
                f"'{DEFAULT_SCHOOL}' school; got '{resolved_school}'."
            )

        if division == 1:
            from engine.astrology.chart_builder import build_chart

            return build_chart(snapshot)

        if division == 9:
            from engine.astrology.navamsa_chart import navamsa_chart

            return navamsa_chart(snapshot)

        from engine.astrology.dashamsa_chart import dashamsa_chart

        return dashamsa_chart(snapshot)

    # Future vargas (ADR Phase D) resolve through the registry;
    # empty in Phase A, so this raises with the registered list.
    rule = get_varga_rule(division, resolved_school)

    from engine.astrology.varga_chart_builder import build_varga_chart

    return build_varga_chart(snapshot, division, rule, resolved_school)
