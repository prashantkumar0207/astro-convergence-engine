"""
Sign-convention declaration registry (SIGN_CONVENTION_V1,
ADR-0012, Decision SC-C).

This module is the SINGLE SOURCE OF TRUTH for which convention every
sign-typed field on every public model uses. It exists so the
project's convention split is machine-checked rather than merely
documented: a collected gate walks the live models, requires every
sign-typed field to appear here, and verifies each declaration
against values observed on real charts. A new sign-typed field added
without a declaration FAILS the gate, which is the point.

Declaring a convention here does not change any value. The
certified varga outputs (0-based) and the rashi-level outputs
(1-based) keep their exact locked semantics; see engine.astrology.sign.
"""

#: Convention tags.
ZERO_BASED = "zero_based"      # Aries = 0 ... Pisces = 11
ONE_BASED = "one_based"        # Aries = 1 ... Pisces = 12
NOT_AN_INDEX = "not_an_index"  # names, lords, and object containers

#: Value shapes, so the gate knows how to read a field.
SCALAR = "scalar"
TUPLE_OF_INDEXES = "tuple_of_indexes"
DICT_VALUES = "dict_values"
DICT_KEYS = "dict_keys"

#: Declarations keyed by "Model.field", each mapping to
#: (convention, value shape, accessor prefix or None). The accessor
#: prefix names the additive Sign accessor pair added in this phase
#: (for example "sign" means ``sign_object`` plus the opposite-
#: convention scalar), so the gate verifies declarations exactly
#: instead of guessing names.
#:
#: VARGA outputs are 0-based; RASHI-level outputs are 1-based. Both
#: are certified and locked. Every entry below was established by
#: execution against real charts, not by inspection.
SIGN_FIELD_CONVENTIONS = {
    # --- rashi level (1-based) -------------------------------------
    "ChartPlanet.sign": (ONE_BASED, SCALAR, "sign"),
    "ChartLagna.sign": (ONE_BASED, SCALAR, "sign"),
    "ChartHouse.sign": (ONE_BASED, SCALAR, "sign"),
    "ChartSign.number": (ONE_BASED, SCALAR, None),
    "Chart.sign_map": (ONE_BASED, DICT_KEYS, None),
    "KpChain.sign_number": (ONE_BASED, SCALAR, "sign"),
    "DrishtiChart.ascendant_sign": (ONE_BASED, SCALAR, "ascendant_sign"),
    "DrishtiChart.planet_signs": (ONE_BASED, DICT_VALUES, None),
    "PlanetDrishti.sign_number": (ONE_BASED, SCALAR, "sign"),
    "PlanetDrishti.aspected_signs": (ONE_BASED, TUPLE_OF_INDEXES, None),

    # --- varga level (0-based, certified and locked) ---------------
    "NavamsaPlanet.sign": (ZERO_BASED, SCALAR, "sign"),
    "NavamsaChart.ascendant_sign": (ZERO_BASED, SCALAR, "ascendant_sign"),
    "ChartNavamsa.sign": (ZERO_BASED, SCALAR, "sign"),
    "DashamsaPlanet.sign": (ZERO_BASED, SCALAR, "sign"),
    "DashamsaChart.ascendant_sign": (ZERO_BASED, SCALAR, "ascendant_sign"),
    "VargaPosition.sign": (ZERO_BASED, SCALAR, "sign"),
    "VargaPlanet.sign": (ZERO_BASED, SCALAR, "sign"),

    # --- not sign indexes at all ----------------------------------
    "KpChain.sign_name": (NOT_AN_INDEX, SCALAR, None),
    "KpChain.sign_lord": (NOT_AN_INDEX, SCALAR, None),
    # KpSignificatorJudgment.signification_set is a tuple of HOUSE numbers
    # (1-12, KP_SIGNIFICATOR_V1, ADR-0078), not zodiac sign numbers - it
    # matches this gate's own naming heuristic ("sign" is a substring of
    # "signification") by coincidence, not because it is sign-typed.
    "KpSignificatorJudgment.signification_set": (NOT_AN_INDEX, TUPLE_OF_INDEXES, None),
}

#: Sign-producing functions and the convention of their return value.
SIGN_FUNCTION_CONVENTIONS = {
    "engine.astrology.signs.zodiac_sign": ONE_BASED,
    "engine.kp.chain.kp_chain.sign_number": ONE_BASED,
    "engine.parashari.drishti.aspected_signs": ONE_BASED,
    "engine.astrology.navamsa_chart.navamsa_sign": ZERO_BASED,
    "engine.astrology.dashamsa_chart.dashamsa_sign": ZERO_BASED,
    "engine.astrology.varga_classifier.classify.d_sign": ZERO_BASED,
}


def declared(model_name: str, field_name: str):
    """Return (convention, shape, accessor) for a field, or None."""

    return SIGN_FIELD_CONVENTIONS.get(f"{model_name}.{field_name}")


def is_index(convention: str) -> bool:
    """True when the declaration describes an actual sign index."""

    return convention in (ZERO_BASED, ONE_BASED)
