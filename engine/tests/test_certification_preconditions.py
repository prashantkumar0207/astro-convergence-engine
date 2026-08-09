"""
Certification precondition gate (ADR-0014 proposed).

docs/VALIDATION_STANDARD.md s2 rule 4 requires checksummed data assets
to be verified before any certification run, and s2 rule 6 requires an
automated anti-fitting scan to be PART OF THE GATE. This test enforces
both on every default pytest run, and additionally requires that every
certification artifact carry the preconditions it was produced under,
so a claim cannot be published without them.
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import certification_support as support  # noqa: E402

#: Every artifact that must carry preconditions. The Tier-0 artifact
#: predates this requirement and is exempt until its runner is wired.
ARTIFACTS = (
    "KP_CHAIN_V1_certification.json",
    "VIMSHOTTARI_V1_certification.json",
    "TRANSIT_V1_certification.json",
    "VARGA_D3_V1_certification.json",
    "VARGA_D12_V1_certification.json",
    "VARGA_D7_V1_certification.json",
    "VARGA_D30_V1_certification.json",
    "VARGA_D2_V1_certification.json",
    "PARASHARI_DRISHTI_V1_certification.json",
    "SIGN_CONVENTION_V1_certification.json",
)


def test_data_assets_verify_against_the_manifest():
    result = support.verify_data_assets()
    assert result["assets_verified"] >= 3
    assert all(len(digest) == 64 for digest in result["sha256"].values())


def test_anti_fitting_scan_is_clean():
    result = support.scan_for_fitting()
    assert result["findings"] == [], result["findings"]
    assert result["modules_scanned"] > 100


def test_anti_fitting_scan_actually_detects_violations(tmp_path):
    # A gate that cannot fail is not a gate. Prove it bites.
    package = tmp_path / "fake_engine"
    package.mkdir()
    (package / "offender.py").write_text(
        "# calibration for H4_delhi_1979\nfudge_factor = 0.5\n"
    )
    import certification_support as module

    original_root = module.ROOT
    try:
        module.ROOT = tmp_path
        with pytest.raises(module.CertificationFailure):
            module.scan_for_fitting(targets=("fake_engine",))
    finally:
        module.ROOT = original_root


@pytest.mark.parametrize("name", ARTIFACTS)
def test_artifact_carries_its_preconditions(name):
    artifact = ROOT / "certification" / name
    assert artifact.exists(), f"missing artifact {name}"
    report = json.loads(artifact.read_text())
    preconditions = report.get("preconditions")
    assert preconditions, f"{name} carries no preconditions block"
    assert preconditions["data_assets"]["assets_verified"] >= 3
    assert preconditions["anti_fitting"]["findings"] == []
    assert preconditions["anti_fitting"]["modules_scanned"] > 100


@pytest.mark.parametrize("name", ARTIFACTS)
def test_human_readable_report_and_transcript_retained(name):
    report = json.loads((ROOT / "certification" / name).read_text())
    slug = report["_slug"]
    reports_dir = ROOT / "reports" / "certification"
    rendered = reports_dir / f"{slug}.report.md"
    transcript = reports_dir / f"{slug}.console.txt"
    assert rendered.exists(), f"no human-readable report for {slug}"
    assert transcript.exists(), f"no console transcript for {slug}"
    # console/report agreement: the report states the same verdict the
    # console printed, because both derive from one dict.
    assert report["result"] in rendered.read_text()
    assert report["result"] in transcript.read_text()
