"""
KP_SIGNIFICATOR_V1 result model (ADR-0078).

A single, narrow judgment: does the 7th house cusp's KP cuspal sub-lord
signify the marriage-promise house group (2, 7, 11) or the marriage-denial
group (1, 6, 10, 12), for a natal chart under the KP_KRISHNAMURTI profile.
Facts and their own disclosed provenance only; no interpretation, timing,
convergence, or predictive narrative exists here.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KpSignificatorJudgment:
    """
    Result of the KP_SIGNIFICATOR_V1 7th-cusp marriage promise/denial
    judgment (ADR-0078).

    Attributes
    ----------
    sub_lord
        The 7th cusp's own KP cuspal sub-lord (engine canonical planet
        name - Rahu/Ketu already resolved through node substitution
        where the sub-lord itself is a node, per ADR-0078 section 6).
    signification_set
        Every house (1-12) `sub_lord` signifies, via Ordering A's own
        union of its four categories (star of occupant, occupant, star
        of owner, owner - ADR-0078 section 4).
    verdict
        One of "PROMISED" (signifies only the promise group, 2/7/11),
        "DENIED" (signifies only the denial group, 1/6/10/12), "MIXED"
        (signifies houses in both groups), or "UNDETERMINED" (signifies
        houses in neither group). Never silently forced into a binary
        result (ADR-0078 section 7).
    retrograde_qualifier
        True if `sub_lord`'s own planet is retrograde at the chart's
        epoch - the promise/denial verdict above is then conditional,
        not equivalent to a direct-motion verdict (ADR-0078 section 5).
    aspect_convention_disclosure
        Provenance note: the KP-scoped aspect/conjunction convention is
        an ACE-defined inference from K.S. Krishnamurti's own
        demonstrated usage, not a single verbatim primary citation
        (ADR-0078 section 3).
    horary_to_natal_disclosure
        Provenance note: the promise/deny house-group rule was
        demonstrated in Krishnamurti's own text via a horary
        illustration; its application to a natal chart here is a
        disclosed ACE-defined inference, not a direct primary citation
        for the natal case (ADR-0078 section 1).
    """

    sub_lord: str
    signification_set: tuple
    verdict: str
    retrograde_qualifier: bool
    aspect_convention_disclosure: str
    horary_to_natal_disclosure: str
