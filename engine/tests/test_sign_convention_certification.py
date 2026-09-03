"""
SIGN_CONVENTION_V1 certification artifact gate (collected by default
pytest).
"""

import json
import sys
from pathlib import Path

import pytest

from engine.astrology.sign import Sign
from engine.astrology.sign_conventions import SIGN_FIELD_CONVENTIONS

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "certification" / "SIGN_CONVENTION_V1_certification.json"

sys.path.insert(0, str(ROOT / "scripts"))
import certify_sign_convention as certifier  # noqa: E402

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
    "D24_parashara": "b377e5df545c9fdc595ead2b2c448715914832e39c4622244a6d13f105ce55cb",
    "D30_parashara": "8b10c2f7b1d8bd8c76406e2290b19f37e55899e78653b520896e9e662606f5a4",
    "D45_parashara": "56a88127eb983a832e4016e0961c929b3accadcaf007def5210af2ab94818cce",
}


def test_artifact_exists_and_claims_pass():
    assert ARTIFACT.exists(), "run scripts/certify_sign_convention.py"
    report = json.loads(ARTIFACT.read_text())
    assert report["schema"] == "sign_convention_v1_certification"
    assert report["adr"] == "ADR-0012"
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
    """
    B-03 (`reports/G1_ARCHITECTURE_AUDIT_2026-08-11.md`): this gate used
    to compare the stored artifact against these same constants, which
    proves the artifact matches itself, not that the certified
    functions still produce these values. It now RECOMPUTES the sweep
    live, via the certifier's own `gate_a_non_invasiveness()` (the same
    code `scripts/certify_sign_convention.py` uses to produce the
    artifact in the first place), and compares the fresh result
    directly against the pinned constants. The stored artifact is not
    read by this test at all; `docs/VALIDATION_STANDARD.md` s2 rule 8:
    stored results are history, not proof - recompute.
    """

    gate = certifier.gate_a_non_invasiveness()
    assert gate["d9_sweep_sha256"] == CERTIFIED_SWEEP_HASHES["d9"]
    assert gate["d10_sweep_sha256"] == CERTIFIED_SWEEP_HASHES["d10"]
    for key, digest in gate["registry_varga_sweep_sha256"].items():
        assert digest == CERTIFIED_SWEEP_HASHES[key], key


def test_negative_control_a_mutated_certified_function_is_detected(monkeypatch):
    """
    Prove the recomputing gate above can actually fail (B-03's second
    requirement). Temporarily mutates the certified `navamsa_sign`
    (D9) as the certifier module sees it, re-derives the sweep, and
    confirms the D9 hash no longer matches. Uses pytest's `monkeypatch`
    so the substitution is automatically undone at the end of this
    test regardless of outcome - nothing in `engine/astrology/` is
    touched, and no certification artifact is read or written by this
    test, so there is nothing here for the mutation to contaminate.
    """

    real_navamsa_sign = certifier.navamsa_sign

    def wrong_navamsa_sign(longitude):
        # Off-by-one sign for every input: certainly different from
        # the certified function for at least one certified swept
        # point, which is all the negative control needs to prove.
        return (real_navamsa_sign(longitude) + 1) % 12

    monkeypatch.setattr(certifier, "navamsa_sign", wrong_navamsa_sign)

    mutated = certifier.gate_a_non_invasiveness()
    assert mutated["d9_sweep_sha256"] != CERTIFIED_SWEEP_HASHES["d9"], (
        "mutating the certified D9 sign function did not change the "
        "recomputed hash; the gate cannot fail and is not evidence"
    )

    # monkeypatch only restores at test teardown, not mid-test - undo
    # explicitly here so this test can itself verify the mutation was
    # fully reversible rather than merely asserting it will be later.
    monkeypatch.undo()
    restored = certifier.gate_a_non_invasiveness()
    assert restored["d9_sweep_sha256"] == CERTIFIED_SWEEP_HASHES["d9"]


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
