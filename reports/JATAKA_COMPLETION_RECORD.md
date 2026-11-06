<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **ACCEPTED by the owner as evidence within its stated scope (`ADR-0110`).** This record declares nothing: `ADR-0110` records the exit decision. |
| Version | 0.3.0 |
| Owner | Project Owner (`ADR-0051` D4; `ADR-0107` Q-C) |
| Last updated | 2026-11-06 |
| Review cadence | Regenerate at the exact `main` SHA of any exit decision |

# JATAKA completion record (N5) and qualification reconciliation (N1)

This is the concise record `ADR-0107` requires for `N5`, with `N1`'s reconciliation in s4. Every count below was generated
from the artifacts at the evaluated `main` SHA. A stored artifact is history, not proof, so the runs are listed in s3.

## 1. What was evaluated

- **Evaluated `main` SHA:** `7ffe60bd702a8ee36f1bea8d42a19b685e341df0`, the merge of PR #40. Parents `8d59d6ddfefd38a94799b14fd80b4fab922316b8` and
  `147b19b73b68b3c0684c84f2b0380706443817df`. Tree `63af0b0a890e607a71f3f6853a084224918837a6`, identical to the PR head.
- **CI at that SHA:** run `42039426497`, push event, success on all four jobs.
- **Later commits:** committing this record creates a later SHA. That SHA is not the one evaluated here, and differs from it
  by this file alone only if its own diff shows that.

## 2. Exit criterion (`Q8_CLOSURE_MATRIX.md` s5, under `ADR-0099`)

**Clause 1, every declared capability individually certified: met at `7ffe60b`, by C2.** The declaring lists did not
change. 23 inputs are declared:

| Declared input | Artifact | Capability | Verdict | Gates | Decision entry |
|---|---|---|---|---|---|
| D1 | SIGN_CONVENTION_V1 | vargas.d1 | PASS | 1 | ADR-0012 |
| D2 | VARGA_D2_V1 | vargas.d2 | PASS | 5 | ADR-0011 |
| D3 | VARGA_D3_V1 | vargas.d3 | PASS | 5 | ADR-0009 |
| D7 | VARGA_D7_V1 | vargas.d7 | PASS | 5 | ADR-0011 |
| D9 | current_engine | vargas.d9 | PASS | 1 | ADR-0005 |
| D10 | current_engine | vargas.d10 | PASS | 1 | ADR-0005 |
| D12 | VARGA_D12_V1 | vargas.d12 | PASS | 5 | ADR-0010 |
| D20 | VARGA_D20_V1 | vargas.d20 | PASS | 8 | ADR-0095 |
| D24 | VARGA_D24_V1 | vargas.d24 | PASS | 8 | ADR-0083 |
| D30 | VARGA_D30_V1 | vargas.d30 | PASS | 5 | ADR-0011 |
| D40 | VARGA_D40_V1 | vargas.d40 | PASS | 8 | ADR-0087 |
| D45 | VARGA_D45_V1 | vargas.d45 | PASS | 9 | ADR-0077 |
| current_engine | current_engine | (all) | PASS | 4 | ADR-0005 |
| KP_CHAIN_V1 | KP_CHAIN_V1 | (all) | PASS | 4 | ADR-0006 |
| KP_SIGNIFICATOR_V1 | KP_SIGNIFICATOR_V1 | (all) | PASS | 10 | ADR-0078 |
| PANCHANGA_V1 | PANCHANGA_V1 | (all) | PASS | 6 | ADR-0055 |
| PARASHARI_DRISHTI_V1 | PARASHARI_DRISHTI_V1 | (all) | PASS | 4 | ADR-0012 |
| PARASHARI_YOGA_V1 | PARASHARI_YOGA_V1 | (all) | PASS | 11 | ADR-0081 |
| RISE_SET_V1 | RISE_SET_V1 | (all) | PASS | 5 | ADR-0054 |
| SIGN_CONVENTION_V1 | SIGN_CONVENTION_V1 | (all) | PASS | 4 | ADR-0012 |
| TRANSIT_V1 | TRANSIT_V1 | (all) | PASS | 4 | ADR-0008 |
| TRIKALAM_V1 | TRIKALAM_V1 | (all) | PASS | 6 | ADR-0060 |
| VIMSHOTTARI_V1 | VIMSHOTTARI_V1 | (all) | PASS | 8 | ADR-0007 |

**Clause 2, nothing in use without certification coverage: met at `7ffe60b`, by C4, subject to s5 and s6.** Of
211 public functions: 109 are in use and covered, 102 are not in use,
0 are live uncovered, 0 are dead-path uncovered, and 0 are `UNKNOWN`. Appendix A gives the artifact and
gate covering each.

**C3:** implemented and passing, so exit is not being proposed without it. Open backlog entries: `OVERCLAIM-TRANSIT-RETURNS`, `OVERCLAIM-TRANSIT-NATAL-CONJUNCTIONS`, `OVERCLAIM-TRANSIT-NATAL-VIEW`.
These three scope overclaims do not gate exit (`ADR-0099` s4), remain required remediation, and no `DP-040` option is selected.

## 3. Regenerated evidence

CI is run `42039426497`. "Local" is a clean native Linux copy from `git archive` of that SHA, on Python 3.11.17, executed
2026-11-05 after the merge. A stored artifact is history, so both regenerated it.

| Check | CI at `7ffe60b` | Local at `7ffe60b` |
|---|---|---|
| Certifiers | All PASS: 41 result lines across three certifier jobs, including `SUPPORT_PATHS_V1` | 23 of 23 PASS |
| Evidence drift | PASS, 73 files, in all three certifier jobs | PASS, 73 files |
| C2, C3, C4 | PASS. C3: 23 artifacts, 48 capabilities, 148 members, 153 gates | PASS, same counts |
| C4 clause 2 | Coverage established; clause 2 satisfied. Clause 2 alone | Gate PASS |
| C2, C3, C4 negative controls | Each exits 1 on its planted violation | Same, as written in `ci.yml` |
| Default `pytest` | 1,254 passed on both runs, on Python 3.11 and on 3.12 | 1,254 passed, 0 skipped |
| Governance job | Success | All 12 steps passed |
| Default `pytest`, Windows host | Not applicable | 1,254 passed (Python 3.12), on the identical tree |

**Reconciliation against `8d59d6d`:** no calculated value changed. All 22 pre-existing scope-bearing artifacts differ only by module count and volatile fields, plus the intended `SIGN_CONVENTION_V1` and `VIMSHOTTARI_V1` changes, and the 4 frozen artifacts are identical. `engine/` production code, `validate_*.py` and `engine/knowledge/data/` have zero diff.

## 4. N1: qualifications reconciled to demonstrated scope

No remediation was repeated. Each accepted qualification stands unchanged, and the later evidence is linked to it. Per
the CEO's reading in `ADR-0107` s3 item 2, which the owner has not separately adopted, this counts only what is
demonstrated and currently covered. It is not blanket certification of all possible behaviour.

| Qualification | Later evidence | Regenerated at `7ffe60b` | Still not claimed |
|---|---|---|---|
| `ADR-0083`, as ratified: "Local certification: PASS. 8/9 failable gates independently verified. Gate C/oracle corroboration: PENDING." Gate C then had no failure path | Registered production Gate C, CI `41798264558` | Gate C: 5,400 comparisons, 0 mismatches | Deity or label payloads, non-default PyJHora chart methods, non-Parashara variants |
| `ADR-0085` (D45 composition layer had no D45-specific exact-value check) | Gate I, commit `1f7bc79bb0833d57deeea9cb120a63de480d8ef3`, PR #36, merge `62baacc704adcfca62973a5d359d4698b9aaf1c3`, CI `41626489663` | Gate I: PASS | The excluded Parivritti and Somanatha methods. `ADR-0077`'s A-H result alone remains no proof of composition |
| `ADR-0086` (Yoga composition had no independent house or sign evidence) | Gate J, commit `06f69d54d0bc65b2988924a3d2756935cb32c185`, PR #37, merge `7c653297495ea51b2133427ccbb660405d3ce3ba`, CI `41798264558` | Gate J: PASS | Bhanga or cancellation logic and combustion gating. Retrograde is a disclosed qualifier, not a gate. `ADR-0081`'s A-I result alone remains no proof of composition |

The owner accepted this scoped reconciliation, preserving those qualifications and non-claims (`ADR-0109`, ratification
sub-entry).

## 5. Exceptions, qualifications and non-claims

- **"Covered" is a reachability statement.** It means a GATED member of a PASS artifact reaches the function. It does not
  mean a gate asserts every behaviour of it (`ADR-0108` s4 item 4; C3 S10).
- **`SUPPORT_PATHS_V1` Gate D proves access-path fidelity only.** `planets`, `signs`, `houses` and `nakshatras` are covered
  in that sense alone. The classical correctness of their data is not certified by it.
- **A GATED member is not thereby in use.** `KnowledgeRegistry.clear` is gated by `SUPPORT_PATHS_V1` and is `NOT_IN_USE`.
- **`rashi_chart`** is certified as neutral over `build_chart`. That adds nothing to what is certified about D1 charts.
- **`natural_relationship`** agrees with one external source, PyJHora. **`to_utc`**'s named-zone cases use literal instants
  and do not validate the timezone database against a second source.
- **Dead callers remain uncertified:** `house_from_longitude`, `map_chart`, `build_all_charts`, `calculate_from_datetime`
  and `KnowledgeResolver.resolve` have no outside caller, and are `NOT_IN_USE`. Nothing was removed.
- **Universe limits (`ADR-0108` s4):** public functions and methods only. Classes, constants and dunder methods are not
  rows, `engine/main.py` handlers and `engine/tools/` are excluded, and implicit dispatch such as `Sign.__str__` is not a row.
- **`ADR-0109` is `ACCEPTED` only in part:** s1 item 4, s3A items 1 to 3 and the `N1` reconciliation. Its s1 items 1 to 3 and
  s3 item 5 are in force as merged code, but the ratification does not name them.
- **`ADR-0103`, `ADR-0004`, `ADR-0018`** stay `PROPOSED`. `Q2`, `Q5`, `Q12`, `Q26` and `Q27` keep their recorded statuses.

## 6. What could not be verified

- **The local certifier runs were on Python 3.11 only.** CI's certifier jobs are the evidence for the rest of its matrix.
- **`N2` stays an unresolved, unverified property.** The roughly fourteen unaudited negative-control gates are neither tested
  nor cleared. `ADR-0107` s2 defers it as nonblocking on present evidence: it reopens for a demonstrated escaped defect or a
  future decision that relies on the unverified property. The new gates' controls are self-authored, and no independent
  mutation harness has run against them.
- **Static analysis has limits.** Dynamic dispatch in engine modules: {"engine.knowledge.registry": ["getattr"]}. Only the `getattr` on an engine
  class is modelled. `import_module`-style reach into a contained class would not be seen, and none was found by search.
- **Containment has per-method evidence and real-tree controls** (`engine/tests/test_stage_c_containment_evidence.py`), all
  written by the builder, and the owner has ratified the rule. The 415 `KnowledgeCache.get` call sites outside `engine/` are
  not individually typed: they rest on no importer and no constructor. Its runtime test covers executed paths only, and
  does not execute the FastAPI routes, because `fastapi` is not in the gate environment.
- **The CEO's technical PASS on PR #40** is stated in the owner's merge authorization. Its text is not a repository file.
- **The owner's Stage A and ADR-0108 text** exists as session input, per `ADR-0107`'s provenance limit.

## 7. Outstanding before any exit decision

Resolved, as `ADR-0110` records. The owner states that the CEO's independent technical PASS came first; its text is not a
repository file. The owner then ratified JATAKA exit, and this record merged with PR #41 at `main` `7e5265b`. Entry into
EVIDENCE or any other phase is a separate decision. **This record declares nothing.**

No material blocker to that review is known. The three `TRANSIT_V1` overclaims remain open (`ADR-0099` s4: they do not gate
exit), and PR #33 and `ADR-0103` stay unmerged and `PROPOSED`.

**Approval status: CEO technical PASS, as the owner states. Owner exit ratified (`ADR-0110`), with this record accepted as
evidence within its stated scope. The evaluated engine SHA above is unchanged.**

## Appendix A: coverage of each in-use function

Generated from `reports/c4_reachability.json` and the artifacts' capability blocks.

### Directly GATED (67)

| Function | Artifact | Gates |
|---|---|---|
| `astrology.chart_builder.build_chart` | SIGN_CONVENTION_V1 | C_declaration_coverage |
| `astrology.dashamsa_chart.dashamsa_chart` | SIGN_CONVENTION_V1 | C_declaration_coverage |
| `astrology.dashamsa_chart.dashamsa_longitude` | current_engine | D_d10_independent_validator |
| `astrology.dashamsa_chart.dashamsa_sign` | SIGN_CONVENTION_V1, current_engine | A_non_invasiveness, D_cross_layer_agreement, D_d10_independent_validator |
| `astrology.dignity.is_exalted` | PARASHARI_YOGA_V1 | A_table_integrity, D_non_invasiveness |
| `astrology.dignity.is_own_sign` | PARASHARI_YOGA_V1 | A_table_integrity, D_non_invasiveness |
| `astrology.house.equal_house_from_ascendant` | SUPPORT_PATHS_V1 | A_equal_house_closed_form |
| `astrology.house.whole_sign_house` | PARASHARI_YOGA_V1 | B2_longitude_plumbing, C_independent_validator, D_non_invasiveness +2 |
| `astrology.nakshatra.nakshatra` | PANCHANGA_V1 | D_non_invasiveness |
| `astrology.navamsa_chart.navamsa_chart` | SIGN_CONVENTION_V1 | C_declaration_coverage |
| `astrology.navamsa_chart.navamsa_longitude` | current_engine | C_d9_independent_validator |
| `astrology.navamsa_chart.navamsa_sign` | SIGN_CONVENTION_V1, current_engine | A_non_invasiveness, C_d9_independent_validator, D_cross_layer_agreement |
| `astrology.panchanga.karana_index` | PANCHANGA_V1 | A_convention_integrity, B_dense_sweep, C_boundary_and_vara_edge_cases +2 |
| `astrology.panchanga.nakshatra_index` | PANCHANGA_V1 | D_non_invasiveness |
| `astrology.panchanga.tithi_index` | PANCHANGA_V1 | A_convention_integrity, B_dense_sweep, C_boundary_and_vara_edge_cases +2 |
| `astrology.panchanga.vara` | PANCHANGA_V1, TRIKALAM_V1 | B_dense_sweep, C_boundary_and_vara_edge_cases, C_boundary_ulp_and_circumpolar +2 |
| `astrology.panchanga.yoga_index` | PANCHANGA_V1 | A_convention_integrity, B_dense_sweep, E_independent_validator +1 |
| `astrology.planet_mapper.map_planet` | SUPPORT_PATHS_V1 | B_map_planet_closed_form |
| `astrology.rashi_chart.rashi_chart` | SUPPORT_PATHS_V1 | F_rashi_chart_neutrality |
| `astrology.sign.Sign.from_one_based` | SIGN_CONVENTION_V1 | B_sign_type, D_cross_layer_agreement |
| `astrology.sign.Sign.from_zero_based` | SIGN_CONVENTION_V1 | B_sign_type, D_cross_layer_agreement |
| `astrology.sign.Sign.name` | SIGN_CONVENTION_V1 | B_sign_type |
| `astrology.sign.Sign.one_based` | SIGN_CONVENTION_V1 | B_sign_type, D_cross_layer_agreement |
| `astrology.signs.zodiac_sign` | PARASHARI_YOGA_V1, SIGN_CONVENTION_V1 | B2_longitude_plumbing, C_independent_validator, D_cross_layer_agreement +3 |
| `astrology.varga_chart_builder.build_varga_chart` | VARGA_D45_V1 | E_independent_validator, I_composition_verification |
| `astrology.varga_classifier.classify` | SIGN_CONVENTION_V1, VARGA_D12_V1, VARGA_D16_V1, VARGA_D20_V1, VARGA_D24_V1, VARGA_D2_V1, VARGA_D30_V1, VARGA_D3_V1, VARGA_D40_V1, VARGA_D45_V1, VARGA_D4_V1, VARGA_D7_V1 | A_non_invasiveness, B_dense_sweep, C_oracle +7 |
| `astrology.varga_d12.ensure_registered` | VARGA_D12_V1 | D_non_invasiveness |
| `astrology.varga_d2.ensure_registered` | VARGA_D2_V1 | D_non_invasiveness |
| `astrology.varga_d20.ensure_registered` | VARGA_D20_V1 | D_non_invasiveness |
| `astrology.varga_d24.ensure_registered` | VARGA_D24_V1 | D_non_invasiveness |
| `astrology.varga_d3.ensure_registered` | VARGA_D3_V1 | D_non_invasiveness |
| `astrology.varga_d30.ensure_registered` | VARGA_D30_V1 | D_non_invasiveness |
| `astrology.varga_d40.ensure_registered` | VARGA_D40_V1 | D_non_invasiveness |
| `astrology.varga_d45.ensure_registered` | VARGA_D45_V1 | D_non_invasiveness |
| `astrology.varga_d7.ensure_registered` | VARGA_D7_V1 | D_non_invasiveness |
| `astronomy.rise_set.horizon_dip_degrees` | RISE_SET_V1 | B_dense_sweep, C_independent_reference |
| `astronomy.rise_set.sunrise` | RISE_SET_V1 | A_convention_integrity, B_dense_sweep, C_independent_reference +2 |
| `astronomy.rise_set.sunset` | RISE_SET_V1 | B_dense_sweep, C_independent_reference, E_independent_validator |
| `calculations.calculations.calculate` | VIMSHOTTARI_V1, current_engine | A_holdout_comparison, B_ayanamsa_profile_check, cases +2 |
| `core.timezone_engine.to_utc` | SUPPORT_PATHS_V1 | C_to_utc_reference |
| `dasha.vimshottari.vimshottari_from_moon` | VIMSHOTTARI_V1 | boundary_proximity_indicator, cases, independent_validator +4 |
| `dasha.vimshottari.vimshottari_from_snapshot` | VIMSHOTTARI_V1 | snapshot_wrapper_neutrality |
| `knowledge.loader.KnowledgeLoader.load` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.registry.KnowledgeRegistry.get` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.repository.KnowledgeRepository.dignities` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.repository.KnowledgeRepository.houses` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.repository.KnowledgeRepository.load_json` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.repository.KnowledgeRepository.nakshatras` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.repository.KnowledgeRepository.natural_relationships` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity, E_natural_relationship_oracle |
| `knowledge.repository.KnowledgeRepository.planets` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.repository.KnowledgeRepository.signs` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `knowledge.validator.SchemaValidator.load_json` | SUPPORT_PATHS_V1 | D_knowledge_access_fidelity |
| `kp.chain.kp_chain` | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, SIGN_CONVENTION_V1 | A_legacy_oracle_equivalence, B_dense_sweep, C_fixture_structural_200 +9 |
| `kp.significators.aspected_signs` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, G_node_aspect_cases |
| `kp.significators.full_name` | KP_SIGNIFICATOR_V1 | F_retrograde_cases, G_node_aspect_cases, H_strength_order_cases +1 |
| `kp.significators.house_of_placidus` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, H_strength_order_cases, J_negative_controls |
| `kp.significators.is_aspecting` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, G_node_aspect_cases, J_negative_controls |
| `kp.significators.is_conjunct` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, G_node_aspect_cases, J_negative_controls |
| `kp.significators.node_substitute` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, G_node_aspect_cases, J_negative_controls |
| `kp.significators.sign_of` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, E_boundary_cases, G_node_aspect_cases +2 |
| `kp.significators.signification_set` | KP_SIGNIFICATOR_V1 | D_non_invasiveness, G_node_aspect_cases, J_negative_controls |
| `parashari.drishti.aspected_signs` | PARASHARI_DRISHTI_V1, SIGN_CONVENTION_V1 | B_combinatorial_12x12, D_cross_layer_agreement, D_independent_validator |
| `parashari.drishti.graha_drishti_from_snapshot` | PARASHARI_DRISHTI_V1 | C_oracle |
| `parashari.mahapurusha_yoga.graha_mahapurusha_from_snapshot` | PARASHARI_YOGA_V1 | C_independent_validator, D_non_invasiveness, J_composition_verification |
| `transits.crossing.find_crossings` | TRANSIT_V1 | A_residual_battery, D_independent_validator, E_declared_division |
| `transits.events.nakshatra_ingresses` | TRANSIT_V1 | A_residual_battery, D_independent_validator, E_declared_division |
| `transits.events.sign_ingresses` | TRANSIT_V1 | A_residual_battery, C_oracle_anchors, D_independent_validator +1 |

### Covered through a GATED caller (42)

| Function | Reached from | Artifacts |
|---|---|---|
| `astrology.chart_house_builder.build_chart_house` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.chart_lagna_builder.build_chart_lagna` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.chart_nakshatra_builder.build_chart_nakshatra` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.chart_navamsa_builder.build_chart_navamsa` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.chart_pada_builder.build_chart_pada` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.chart_planet_builder.build_chart_planet` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.chart_sign_builder.build_chart_sign` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.degrees.degree_in_sign` | `astrology.chart_builder.build_chart` +4 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.dignity.dignity` | `astrology.dignity.is_exalted` +5 | PARASHARI_YOGA_V1 |
| `astrology.longitude_utils.division_index` | `astrology.chart_builder.build_chart` +22 | PANCHANGA_V1, PARASHARI_DRISHTI_V1, PARASHARI_YOGA_V1 +14 |
| `astrology.longitude_utils.normalize_longitude` | `astrology.chart_builder.build_chart` +22 | PANCHANGA_V1, PARASHARI_DRISHTI_V1, PARASHARI_YOGA_V1 +14 |
| `astrology.nakshatra_names.nakshatra_name` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.navamsa_chart.navamsa_number` | `astrology.chart_builder.build_chart` +6 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +8 |
| `astrology.pada.pada` | `astrology.chart_builder.build_chart` +3 | SIGN_CONVENTION_V1, SUPPORT_PATHS_V1, VARGA_D12_V1 +7 |
| `astrology.varga_classifier.VargaClassification.division_number` | `astrology.divisional_chart.divisional_chart` +1 | SIGN_CONVENTION_V1, VARGA_D12_V1, VARGA_D24_V1 +6 |
| `astrology.varga_classifier.math_nextafter_below_one` | `astrology.divisional_chart.divisional_chart` +2 | SIGN_CONVENTION_V1, VARGA_D12_V1, VARGA_D16_V1 +9 |
| `astrology.varga_registry.get_varga_rule` | `astrology.divisional_chart.divisional_chart` | SIGN_CONVENTION_V1, VARGA_D12_V1, VARGA_D24_V1 +6 |
| `astrology.varga_registry.register_varga_rule` | `astrology.varga_d12.D12_PARASHARA` +17 | VARGA_D12_V1, VARGA_D20_V1, VARGA_D24_V1 +6 |
| `astrology.varga_registry.registered_vargas` | `astrology.varga_d12.D12_PARASHARA` +17 | VARGA_D12_V1, VARGA_D20_V1, VARGA_D24_V1 +6 |
| `astronomy.astronomy_snapshot.astronomy_snapshot` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.ayanamsa.ayanamsa` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.ephemeris.calc_ut_checked` | `astrology.panchanga.panchanga` +11 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PANCHANGA_V1 +8 |
| `astronomy.ephemeris.default_ephemeris_path` | `astrology.panchanga.panchanga` +11 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PANCHANGA_V1 +8 |
| `astronomy.ephemeris.ephemeris_mode_from_flags` | `astrology.panchanga.panchanga` +11 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PANCHANGA_V1 +8 |
| `astronomy.ephemeris.initialize_ephemeris` | `astrology.panchanga.panchanga` +11 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PANCHANGA_V1 +8 |
| `astronomy.house_positions.house_positions` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.planet_collection.derive_ketu` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.planet_collection.planet_collection` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.planet_positions.planet_position` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.sidereal_planets.sidereal_planet_collection` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `astronomy.sidereal_planets.sidereal_planet_position` | `astrology.panchanga.panchanga` +7 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PANCHANGA_V1 +6 |
| `core.julian_day.julian_day` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `core.validation.validate_birth_data` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `dasha.profile.validate_dasha_profile` | `dasha.vimshottari.vimshottari_from_moon` +1 | VIMSHOTTARI_V1 |
| `kp.chart.kp_chart_from_snapshot` | `kp.chart.kp_chart` | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, SIGN_CONVENTION_V1 |
| `kp.intervals.to_exact` | `kp.chain.kp_chain` +1 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, SIGN_CONVENTION_V1 |
| `kp.intervals.walk` | `kp.chain.kp_chain` +1 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, SIGN_CONVENTION_V1 |
| `models.dasha.DashaPeriod.duration_years` | `dasha.vimshottari.vimshottari_from_moon` +1 | VIMSHOTTARI_V1 |
| `models.dasha.DashaPeriod.lord` | `dasha.vimshottari.vimshottari_from_moon` +1 | VIMSHOTTARI_V1 |
| `services.time_service.local_datetime` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `services.time_service.utc_datetime` | `calculations.calculations.calculate` +3 | KP_CHAIN_V1, KP_SIGNIFICATOR_V1, PARASHARI_DRISHTI_V1 +4 |
| `transits.speeds.grid_step_days` | `transits.crossing.find_crossings` +2 | TRANSIT_V1 |
