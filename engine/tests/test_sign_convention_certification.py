"""
SIGN_CONVENTION_V1 certification artifact gate (collected by default
pytest).
"""

import json
from pathlib import Path

from engine.astrology.sign import Sign
from engine.astrology.sign_conventions import SIGN_FIELD_CONVENTIONS

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "SIGN_CONVENTION_V1_certification.json"

#: Certified sweep hashes, verified EQUAL at published main 7d170f8 and
#: at the commit introducing this phase, proving no certified value
#: changed (Gate A, Decision SC-B).
CERTIFIED_SWEEP_HASHES = {
    "d9": "58b133367fba404976f3e562fd46ed50bd332006b8c7107415e9d3a3a9263c5e",
    "d10": "5678aecfe9576ca81ecf818566b9a9302ffb62eeb5a7cfcce8cc2f86504ab9e3",
    "D2_parashara": "41c2cb733f3bdb18e63cab9f9d837f013977c6d171229f4e865b85056c4b5436",
    "D3_parashara": "71672e052fc5877fce4e6b8bc0ab1160f9e776e4b6e85a8e2f16386024e673a0",
    "D7_parashara": "51f7acf701b1978990accbfcbedfbac6001446f2e31789077752e44c54c3b73c",
    "D12_parashara": "81b14663c6d66a8680e3697a25b9bd53c72897768e233b82f1dfcbc3eb1306ac",
    "D30_parashara": "8b10c2f7b1d8bd8c76406e2290b19f37e55899e78653b520896e9e662606f5a4",
}


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_sign_convention.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "sign_convention_v1_certification"
    assert report["adr"] == "ADR-CONVENTION-001"
    assert report["result"] == "PASS"
    gates = report["gates"]
    assert gates["B_sign_type"] == {"signs": 12, "mismatches": 0, "inert": True}
    assert gates["C_declaration_coverage"]["mismatches"] == 0
    assert gates["C_declaration_coverage"]["fields_proven"] >= 17
    assert gates["D_cross_layer_agreement"]["mismatches"] == 0
    assert "no renumbering of any certified sign value" in report["explicit_non_claims"]


def test_artifact_records_the_declaration_registry_as_evidence():
    report = json.loads(ARTIFACT.read_text())
    recorded = report["declaration_registry"]
    assert set(recorded) == set(SIGN_FIELD_CONVENTIONS)
    for key, (convention, shape, accessor) in SIGN_FIELD_CONVENTIONS.items():
        assert recorded[key] == {"convention": convention, "shape": shape,
                                 "accessor": accessor}


def test_non_invasiveness_hashes_match_published_main():
    report = json.loads(ARTIFACT.read_text())
    gate = report["gates"]["A_non_invasiveness"]
    assert gate["d9_sweep_sha256"] == CERTIFIED_SWEEP_HASHES["d9"]
    assert gate["d10_sweep_sha256"] == CERTIFIED_SWEEP_HASHES["d10"]
    for key, digest in gate["registry_varga_sweep_sha256"].items():
        assert digest == CERTIFIED_SWEEP_HASHES[key], key


def test_every_declared_field_proven_by_discriminating_witness():
    report = json.loads(ARTIFACT.read_text())
    fields = report["gates"]["C_declaration_coverage"]["fields"]
    for key, record in fields.items():
        expected_witness = 0 if record["convention"] == "zero_based" else 12
        assert record["discriminating_witness"] == expected_witness, key
        assert record["min"] <= expected_witness <= record["max"], key


def test_headline_behavior_reproduces_on_sample():
    assert Sign.from_zero_based(4).name == "Leo"
    assert Sign.from_one_based(5).name == "Leo"
    assert Sign.from_zero_based(4) == Sign.from_one_based(5)
