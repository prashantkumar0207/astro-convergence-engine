"""Capability enumeration and per-gate coverage declarations (ADR-0101 s2-s3, ADR-0107).

`certification_support.emit()` applies this table, so every certifier writes its
own `capabilities`, `scope_not_gated` and per-gate `exercises` from the run that
produced the artifact. The two-segment capability slug, the callable-path members
and the member-level dispositions are the owner's selections (2-B, 3-C). The rest
of the shape is a builder specification awaiting ratification: see ADR-0108.

These are declarations, not observations (ADR-0101 s3). `scripts/check_scope_coverage.py`
checks them against the source by a separate static method, and a declaration
it cannot support fails the gate.

Member dispositions:
  GATED                    at least one gate in this artifact exercises the member.
  SCOPE_NOT_GATED          named in `scope_not_gated` with a reason. Not coverage.
  OPEN_SCOPE_OVERCLAIM     an ADR-0099 s4 overclaim, open and tracked in the backlog.
                           Not coverage, and no DP-040 option is selected by it.
  INHERITED_NEUTRALITY_PROVEN
                           ADR-0099 s5: a delegator whose neutrality a committed test
                           proves. Must name that test. No member claims this today.
"""

from __future__ import annotations

GATED = "GATED"
SCOPE_NOT_GATED = "SCOPE_NOT_GATED"
OPEN_SCOPE_OVERCLAIM = "OPEN_SCOPE_OVERCLAIM"
INHERITED = "INHERITED_NEUTRALITY_PROVEN"

CAPABILITY_SCHEMA = "ace-capability-enumeration-v1"

CLASSIFY = "engine.astrology.varga_classifier.classify"
DIVISIONAL = "engine.astrology.divisional_chart.divisional_chart"
BUILDER = "engine.astrology.varga_chart_builder.build_varga_chart"
RULE_HASH = "engine.astrology.varga_rules.rule_content_sha256"
CALCULATE = "engine.calculations.calculations.calculate"

_NO_PRODUCTION_REACH = ("the validator recomputes from its own embedded reference and calls no "
                        "production code, so it exercises no production callable")


def _fn(path, *gates):
    return {"callable": path, "kind": "callable", "disposition": GATED, "exercised_by": list(gates)}


def _data(path, *gates):
    return {"callable": path, "kind": "data", "disposition": GATED, "exercised_by": list(gates)}


def _ungated(path, reason):
    return {"callable": path, "kind": "callable", "disposition": SCOPE_NOT_GATED, "exercised_by": [],
            "reason": reason}


def _overclaim(path, entry):
    return {"callable": path, "kind": "callable", "disposition": OPEN_SCOPE_OVERCLAIM, "exercised_by": [],
            "backlog_entry": entry}


def _cap(capability_id, *members):
    return {"id": capability_id, "members": list(members)}


def _varga_five(number, rule):
    """D2, D3, D7, D12 and D30: five gates, each with a validator that reaches production."""

    return {
        "capabilities": [_cap(
            f"vargas.d{number}",
            _data(rule, "A_table_integrity", "B_dense_sweep", "C_oracle", "D_non_invasiveness"),
            _fn(CLASSIFY, "B_dense_sweep", "C_oracle", "E_independent_validator"),
            _fn(f"engine.astrology.varga_d{number}.ensure_registered", "D_non_invasiveness"),
            _fn(DIVISIONAL, "D_non_invasiveness"),
        )],
    }


def _varga_nine_registered(number, rule, last_gate="I_static_reference_regression", composed=True):
    """D20, D24, D40 and D45: production-registered, with the post-ADR-0083 battery."""

    rule_gates = ["A_table_integrity", "B_dense_sweep", "C_oracle", "D_non_invasiveness", "F_boundary_cases",
                  "G_protected_holdout", "H_negative_controls"]
    classify_gates = ["B_dense_sweep", "C_oracle", "F_boundary_cases", "G_protected_holdout", "H_negative_controls"]
    empty = {}
    if last_gate == "I_static_reference_regression":
        rule_gates.append(last_gate)
        classify_gates.append(last_gate)
        empty["E_independent_validator"] = _NO_PRODUCTION_REACH
    members = [
        _data(rule, *rule_gates),
        _fn(CLASSIFY, *classify_gates),
        _fn(RULE_HASH, "A_table_integrity", "D_non_invasiveness", "H_negative_controls"),
        _fn(f"engine.astrology.varga_d{number}.ensure_registered", "D_non_invasiveness"),
    ]
    if composed:
        members.append(_fn(DIVISIONAL, "D_non_invasiveness"))
    declaration = {"capabilities": [_cap(f"vargas.d{number}", *members)]}
    if empty:
        declaration["empty_exercises"] = empty
    return declaration


def _varga_nine_standalone(number):
    """D4 and D16: certified, deliberately unregistered, rule embedded in the certifier."""

    return {
        "capabilities": [_cap(
            f"vargas.d{number}",
            _fn(CLASSIFY, "B_dense_sweep", "C_oracle", "F_boundary_cases", "G_protected_holdout",
                "H_negative_controls", "I_static_reference_regression"),
            _fn(RULE_HASH, "A_table_integrity", "D_isolation", "H_negative_controls"),
        )],
        "empty_exercises": {"E_independent_validator": _NO_PRODUCTION_REACH},
    }


_D45 = _varga_nine_registered(45, "engine.astrology.varga_d45.D45_PARASHARA", last_gate="I_composition_verification")
for _member in _D45["capabilities"][0]["members"]:
    if _member["callable"] == RULE_HASH:
        _member["exercised_by"].remove("A_table_integrity")  # D45's Gate A checks the table cell by cell.
    if _member["callable"] == CLASSIFY:
        _member["exercised_by"] += ["E_independent_validator", "I_composition_verification"]
    if _member["callable"] == DIVISIONAL:
        _member["exercised_by"] += ["E_independent_validator", "I_composition_verification"]
_D45["capabilities"][0]["members"].append(_fn(BUILDER, "E_independent_validator", "I_composition_verification"))

_SIGNIFICATORS = "engine.kp.significators"
_YOGA = "engine.parashari.mahapurusha_yoga"
_PANCHANGA = "engine.astrology.panchanga"
_RISE_SET = "engine.astronomy.rise_set"
_EVENTS = "engine.transits.events"
_NAVAMSA = "engine.astrology.navamsa_chart"
_DASHAMSA = "engine.astrology.dashamsa_chart"
_DASHA = "engine.dasha.vimshottari"
_CONVENTIONS = "engine.astrology.sign_conventions"

_DASHA_GATES = ("oracle_pratyantar_rows_compared", "oracle_lord_mismatches", "oracle_max_start_delta_days",
                "independent_validator", "cases", "near_boundary_coverage", "boundary_proximity_indicator")
_DASHA_WRAPPER_REASON = ("a public wrapper over the gated vimshottari_from_moon. No certification gate calls it. "
                         "Test coverage is not gate coverage, and no inherited certification is claimed")

ARTIFACT_DECLARATIONS = {
    "current_engine_certification.json": {
        "capabilities": [
            _cap("kernel.sidereal_longitudes", _fn(CALCULATE, "A_holdout_comparison")),
            _cap("kernel.ascendant_and_cusps", _fn(CALCULATE, "A_holdout_comparison")),
            _cap("kernel.ayanamsa_profiles", _fn(CALCULATE, "B_ayanamsa_profile_check")),
            _cap("vargas.d9", _fn(f"{_NAVAMSA}.navamsa_sign", "C_d9_independent_validator"),
                 _fn(f"{_NAVAMSA}.navamsa_longitude", "C_d9_independent_validator")),
            _cap("vargas.d10", _fn(f"{_DASHAMSA}.dashamsa_sign", "D_d10_independent_validator"),
                 _fn(f"{_DASHAMSA}.dashamsa_longitude", "D_d10_independent_validator")),
        ],
    },
    "KP_CHAIN_V1_certification.json": {
        "capabilities": [
            _cap("kp.lordship_chain",
                 _fn("engine.kp.chain.kp_chain", "A_legacy_oracle_equivalence", "C_fixture_structural_200",
                     "D_independent_validator"),
                 _fn("engine.kp.intervals.all_boundaries", "A_legacy_oracle_equivalence")),
            _cap("kp.fact_chart", _fn("engine.kp.chart.kp_chart", "B_holdout_chart_equivalence")),
        ],
    },
    "KP_SIGNIFICATOR_V1_certification.json": {
        "capabilities": [_cap(
            "kp.marriage_judgment",
            _fn(f"{_SIGNIFICATORS}.judge_marriage", "D_non_invasiveness", "F_retrograde_cases", "G_node_aspect_cases",
                "I_protected_holdout"),
            _fn(f"{_SIGNIFICATORS}.signification_set", "D_non_invasiveness", "G_node_aspect_cases",
                "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.node_substitute", "D_non_invasiveness", "G_node_aspect_cases",
                "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.is_aspecting", "D_non_invasiveness", "G_node_aspect_cases", "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.is_conjunct", "D_non_invasiveness", "G_node_aspect_cases", "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.aspected_signs", "D_non_invasiveness", "G_node_aspect_cases"),
            _fn(f"{_SIGNIFICATORS}.house_of_placidus", "D_non_invasiveness", "H_strength_order_cases",
                "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.sign_of", "D_non_invasiveness", "E_boundary_cases", "G_node_aspect_cases",
                "H_strength_order_cases", "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.full_name", "F_retrograde_cases", "G_node_aspect_cases", "H_strength_order_cases",
                "J_negative_controls"),
            _fn(f"{_SIGNIFICATORS}.rule_content_sha256", "A_table_integrity", "D_non_invasiveness",
                "J_negative_controls"),
            _fn("engine.kp.chain.kp_chain", "B_dense_sweep", "C_independent_validator", "D_non_invasiveness",
                "E_boundary_cases", "F_retrograde_cases", "G_node_aspect_cases", "H_strength_order_cases",
                "J_negative_controls"),
            _fn("engine.kp.chart.kp_chart", "C_independent_validator", "I_protected_holdout"),
            _data(f"{_SIGNIFICATORS}.PROMISE_HOUSES", "A_table_integrity", "J_negative_controls"),
            _data(f"{_SIGNIFICATORS}.DENY_HOUSES", "A_table_integrity", "J_negative_controls"),
            _data(f"{_SIGNIFICATORS}.SPECIAL_ASPECTS", "A_table_integrity", "G_node_aspect_cases"),
        )],
    },
    "PANCHANGA_V1_certification.json": {
        "capabilities": [
            _cap("panchanga.tithi", _fn(f"{_PANCHANGA}.tithi_index", "A_convention_integrity", "B_dense_sweep",
                                        "C_boundary_and_vara_edge_cases", "E_independent_validator",
                                        "F_external_oracle")),
            _cap("panchanga.yoga", _fn(f"{_PANCHANGA}.yoga_index", "A_convention_integrity", "B_dense_sweep",
                                       "E_independent_validator", "F_external_oracle")),
            _cap("panchanga.karana",
                 _fn(f"{_PANCHANGA}.karana_index", "A_convention_integrity", "B_dense_sweep",
                     "C_boundary_and_vara_edge_cases", "E_independent_validator", "F_external_oracle"),
                 _fn("engine.astrology.panchanga_names.karana_name", "C_boundary_and_vara_edge_cases")),
            _cap("panchanga.nakshatra",
                 _fn(f"{_PANCHANGA}.nakshatra_index", "D_non_invasiveness"),
                 _fn("engine.astrology.nakshatra.nakshatra", "D_non_invasiveness")),
            _cap("panchanga.vara", _fn(f"{_PANCHANGA}.vara", "C_boundary_and_vara_edge_cases")),
            _cap("panchanga.at_instant", _fn(f"{_PANCHANGA}.panchanga", "E_independent_validator")),
        ],
    },
    "PARASHARI_DRISHTI_V1_certification.json": {
        "capabilities": [_cap(
            "drishti.graha_full",
            _data("engine.parashari.drishti.DRISHTI_OFFSETS", "A_table_integrity", "B_combinatorial_12x12"),
            _fn("engine.parashari.drishti.aspected_signs", "B_combinatorial_12x12", "D_independent_validator"),
            _fn("engine.parashari.drishti.parashari_drishti", "C_oracle"),
            _fn("engine.parashari.drishti.graha_drishti_from_snapshot", "C_oracle"),
        )],
    },
    "PARASHARI_YOGA_V1_certification.json": {
        "capabilities": [_cap(
            "yogas.panch_mahapurusha",
            _fn(f"{_YOGA}.mahapurusha_yoga", "C_independent_validator", "D_non_invasiveness",
                "G_retrograde_disclosure", "H_static_reference_regression", "J_composition_verification"),
            _fn(f"{_YOGA}.graha_mahapurusha_from_snapshot", "C_independent_validator", "D_non_invasiveness",
                "J_composition_verification"),
            _fn(f"{_YOGA}.yoga_present", "D_non_invasiveness", "F_multi_yoga_cases", "G_retrograde_disclosure"),
            _fn(f"{_YOGA}._yoga_predicate_from_sign_and_house", "B_logical_enumeration", "C_independent_validator",
                "D_non_invasiveness", "I_negative_controls"),
            _fn("engine.astrology.house.whole_sign_house", "B2_longitude_plumbing", "C_independent_validator",
                "D_non_invasiveness", "E_boundary_cases", "J_composition_verification"),
            _fn("engine.astrology.signs.zodiac_sign", "B2_longitude_plumbing", "C_independent_validator",
                "D_non_invasiveness", "E_boundary_cases", "J_composition_verification"),
            _fn("engine.astrology.dignity.is_exalted", "A_table_integrity", "D_non_invasiveness"),
            _fn("engine.astrology.dignity.is_own_sign", "A_table_integrity", "D_non_invasiveness"),
            _fn(f"{_YOGA}.rule_content_sha256", "D_non_invasiveness", "I_negative_controls"),
            _data(f"{_YOGA}.YOGA_GRAHAS", "A_table_integrity", "B_logical_enumeration", "D_non_invasiveness",
                  "F_multi_yoga_cases", "G_retrograde_disclosure", "I_negative_controls"),
            _data(f"{_YOGA}.KENDRA_HOUSES", "A_table_integrity", "B_logical_enumeration", "D_non_invasiveness",
                  "I_negative_controls"),
        )],
    },
    "RISE_SET_V1_certification.json": {
        "capabilities": [
            _cap("rise_set.sunrise", _fn(f"{_RISE_SET}.sunrise", "A_convention_integrity", "B_dense_sweep",
                                         "C_independent_reference", "D_non_invasiveness",
                                         "E_independent_validator")),
            _cap("rise_set.sunset", _fn(f"{_RISE_SET}.sunset", "B_dense_sweep", "C_independent_reference",
                                        "E_independent_validator")),
            _cap("rise_set.horizon_dip", _fn(f"{_RISE_SET}.horizon_dip_degrees", "B_dense_sweep",
                                             "C_independent_reference")),
        ],
    },
    "SIGN_CONVENTION_V1_certification.json": {
        "capabilities": [
            _cap("conventions.sign_type",
                 _fn("engine.astrology.sign.Sign.from_one_based", "B_sign_type", "D_cross_layer_agreement"),
                 _fn("engine.astrology.sign.Sign.from_zero_based", "B_sign_type", "D_cross_layer_agreement"),
                 _data("engine.astrology.sign.SIGN_COUNT", "B_sign_type")),
            _cap("conventions.declarations",
                 _fn(f"{_CONVENTIONS}.declared", "C_declaration_coverage"),
                 _fn(f"{_CONVENTIONS}.is_index", "C_declaration_coverage"),
                 _data(f"{_CONVENTIONS}.SIGN_FIELD_CONVENTIONS", "C_declaration_coverage"),
                 _data(f"{_CONVENTIONS}.SIGN_FUNCTION_CONVENTIONS", "D_cross_layer_agreement")),
            _cap("conventions.cross_layer",
                 _fn("engine.astrology.signs.zodiac_sign", "D_cross_layer_agreement"),
                 _fn(f"{_NAVAMSA}.navamsa_sign", "A_non_invasiveness", "D_cross_layer_agreement"),
                 _fn(f"{_DASHAMSA}.dashamsa_sign", "A_non_invasiveness", "D_cross_layer_agreement"),
                 _fn(CLASSIFY, "A_non_invasiveness", "D_cross_layer_agreement"),
                 _fn("engine.kp.chain.kp_chain", "D_cross_layer_agreement"),
                 _fn("engine.parashari.drishti.aspected_signs", "D_cross_layer_agreement")),
            _cap("conventions.chart_fields",
                 _fn(f"{_NAVAMSA}.navamsa_chart", "C_declaration_coverage"),
                 _fn(f"{_DASHAMSA}.dashamsa_chart", "C_declaration_coverage"),
                 _fn("engine.astrology.chart_factory.build_master_chart", "C_declaration_coverage"),
                 _fn("engine.kp.chart.kp_chart", "C_declaration_coverage"),
                 _fn("engine.parashari.drishti.parashari_drishti", "C_declaration_coverage")),
            _cap("vargas.d1",
                 _fn(DIVISIONAL, "C_declaration_coverage"),
                 _fn("engine.astrology.chart_builder.build_chart", "C_declaration_coverage")),
        ],
    },
    "TRANSIT_V1_certification.json": {
        "capabilities": [
            _cap("transits.crossing", _fn("engine.transits.crossing.find_crossings", "A_residual_battery",
                                          "D_independent_validator", "E_declared_division")),
            _cap("transits.sign_ingress", _fn(f"{_EVENTS}.sign_ingresses", "A_residual_battery", "C_oracle_anchors",
                                              "D_independent_validator", "E_declared_division")),
            _cap("transits.nakshatra_ingress", _fn(f"{_EVENTS}.nakshatra_ingresses", "A_residual_battery",
                                                   "D_independent_validator", "E_declared_division")),
            _cap("transits.returns", _overclaim(f"{_EVENTS}.returns", "OVERCLAIM-TRANSIT-RETURNS")),
            _cap("transits.natal_conjunctions",
                 _overclaim(f"{_EVENTS}.natal_conjunctions", "OVERCLAIM-TRANSIT-NATAL-CONJUNCTIONS")),
            _cap("transits.natal_view",
                 _overclaim("engine.transits.view.transit_view", "OVERCLAIM-TRANSIT-NATAL-VIEW")),
        ],
    },
    "TRIKALAM_V1_certification.json": {
        "capabilities": [_cap(
            "trikalam.periods",
            _fn("engine.astrology.trikalam.trikalam_period", "B_dense_sweep", "C_boundary_ulp_and_circumpolar",
                "E_independent_validator", "F_external_oracle"),
            _fn(f"{_PANCHANGA}.vara", "B_dense_sweep", "C_boundary_ulp_and_circumpolar", "D_non_invasiveness",
                "E_independent_validator"),
            _data("engine.astrology.trikalam.PYJHORA_TRIKALAM_V1", "A_convention_integrity", "B_dense_sweep",
                  "C_boundary_ulp_and_circumpolar", "E_independent_validator", "F_external_oracle"),
            _data("engine.astrology.trikalam.PERIOD_FRACTION", "A_convention_integrity", "B_dense_sweep"),
        )],
    },
    "VARGA_D2_V1_certification.json": _varga_five(2, "engine.astrology.varga_d2.D2_PARASHARA"),
    "VARGA_D3_V1_certification.json": _varga_five(3, "engine.astrology.varga_d3.D3_PARASHARA"),
    "VARGA_D4_V1_certification.json": _varga_nine_standalone(4),
    "VARGA_D7_V1_certification.json": _varga_five(7, "engine.astrology.varga_d7.D7_PARASHARA"),
    "VARGA_D12_V1_certification.json": _varga_five(12, "engine.astrology.varga_d12.D12_PARASHARA"),
    "VARGA_D16_V1_certification.json": _varga_nine_standalone(16),
    "VARGA_D20_V1_certification.json": _varga_nine_registered(20, "engine.astrology.varga_d20.D20_VIMSAMSA",
                                                              composed=False),
    "VARGA_D24_V1_certification.json": _varga_nine_registered(24, "engine.astrology.varga_d24.D24_SIDDHAMSA"),
    "VARGA_D30_V1_certification.json": _varga_five(30, "engine.astrology.varga_d30.D30_PARASHARA"),
    "VARGA_D40_V1_certification.json": _varga_nine_registered(40, "engine.astrology.varga_d40.D40_KHAVEDAMSA"),
    "VARGA_D45_V1_certification.json": _D45,
    "VIMSHOTTARI_V1_certification.json": {
        "capabilities": [_cap(
            "dasha.vimshottari",
            _fn(f"{_DASHA}.vimshottari_from_moon", *_DASHA_GATES),
            _fn(CALCULATE, "oracle_pratyantar_rows_compared", "cases", "near_boundary_coverage"),
            _ungated(f"{_DASHA}.vimshottari_from_snapshot", _DASHA_WRAPPER_REASON),
            _ungated(f"{_DASHA}.vimshottari_parashari", _DASHA_WRAPPER_REASON),
            _ungated(f"{_DASHA}.vimshottari_kp", _DASHA_WRAPPER_REASON),
        )],
        "empty_exercises": {"start_tolerance_days": "a declared tolerance value, not an execution of any callable"},
    },
}


class DeclarationError(RuntimeError):
    """A certifier's report and its declaration disagree. Certification must stop."""


def _gate_exercises(declaration: dict) -> dict:
    exercises: dict = {}
    for capability in declaration["capabilities"]:
        for member in capability["members"]:
            for gate in member["exercised_by"]:
                exercises.setdefault(gate, set()).add(capability["id"])
    return {gate: sorted(ids) for gate, ids in exercises.items()}


def apply(report: dict, artifact_name: str) -> None:
    """Write the declarations into `report`, failing closed on any disagreement."""

    if artifact_name not in ARTIFACT_DECLARATIONS:
        raise DeclarationError(
            f"{artifact_name} has no capability declaration, so ADR-0101 s2-s3 cannot be met; "
            f"add it to scripts/capability_declarations.py")
    declaration = ARTIFACT_DECLARATIONS[artifact_name]
    gates = report.get("gates")
    if not isinstance(gates, dict) or not gates:
        raise DeclarationError(f"{artifact_name}: the report has no gates to attach `exercises` to")
    exercises = _gate_exercises(declaration)
    empty = declaration.get("empty_exercises", {})
    declared = set(exercises) | set(empty)
    missing = sorted(set(gates) - declared)
    unknown = sorted(declared - set(gates))
    if missing:
        raise DeclarationError(f"{artifact_name}: gates with no declaration: {missing}")
    if unknown:
        raise DeclarationError(f"{artifact_name}: declarations for gates the report lacks: {unknown}")

    scalar_gates = {}
    for name, block in gates.items():
        ids = exercises.get(name, [])
        if isinstance(block, dict):
            # A copy: some certifiers also publish a gate's dict under another key
            # (`oracle`), and that record must not change.
            gates[name] = dict(block, exercises=ids)
            if name in empty:
                gates[name]["exercises_note"] = empty[name]
        else:
            scalar_gates[name] = {"exercises": ids}
            if name in empty:
                scalar_gates[name]["exercises_note"] = empty[name]

    report["capability_schema"] = CAPABILITY_SCHEMA
    report["capabilities"] = [
        {"id": capability["id"], "members": [dict(member) for member in capability["members"]]}
        for capability in declaration["capabilities"]
    ]
    report["scope_not_gated"] = [
        {"id": member["callable"], "capability": capability["id"], "reason": member["reason"]}
        for capability in declaration["capabilities"]
        for member in capability["members"]
        if member["disposition"] == SCOPE_NOT_GATED
    ]
    if scalar_gates:
        report["scalar_gate_exercises"] = scalar_gates
