"""
Certification precondition gate (ADR-0014 proposed).

docs/VALIDATION_STANDARD.md s2 rule 4 requires checksummed data assets
to be verified before any certification run, and s2 rule 6 requires an
automated anti-fitting scan to be PART OF THE GATE. This test enforces
both on every default pytest run, and additionally requires that every
certification artifact carry the preconditions it was produced under,
so a claim cannot be published without them.
"""

import hashlib
import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))

import certification_support as support  # noqa: E402

#: Every artifact that must carry preconditions. The Tier-0 artifact was
#: exempt until its runner was wired; Q16 wired it, so the exemption is
#: withdrawn and it is now held to the same standard as the rest.
ARTIFACTS = (
    "current_engine_certification.json",
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
    assert result["modules_scanned"] >= 180


def test_anti_fitting_scan_covers_every_declared_certification_source():
    """M-03: additions or removals from the certification surface are explicit."""

    assert len(support.CERTIFIER_SOURCES) == 18
    assert len(support.VALIDATOR_SOURCES) == 17
    assert support.FIXTURE_SOURCES == ("brihat_fixtures.py",)
    discovered_certifiers = {
        str(path.relative_to(ROOT)).replace("\\", "/")
        for path in (ROOT / "scripts").glob("certify_*.py")
    }
    assert discovered_certifiers == set(support.CERTIFIER_SOURCES)
    discovered_validators = {
        path.name for path in ROOT.glob("validate_*_holdout.py")
    }
    assert discovered_validators == set(support.VALIDATOR_SOURCES)


def test_checksum_manifest_covers_every_required_ephemeris_file():
    """Q16 coverage proof: the manifest guards the data actually read.

    Verifying the swetest binary's version proves the ORACLE is the pinned
    one. It proves nothing about the ephemeris DATA. This test asserts that
    the manifest covers exactly the files
    `engine.astronomy.ephemeris.REQUIRED_FILES` declares, resolved at the
    path the engine configures, so that coverage cannot silently rot if
    either list changes.
    """

    from engine.astronomy.ephemeris import REQUIRED_FILES, default_ephemeris_path

    manifest_names = {
        line.split()[-1]
        for line in support.CHECKSUM_MANIFEST.read_text().splitlines()
        if line.strip()
    }
    missing = set(REQUIRED_FILES) - manifest_names
    assert not missing, (
        f"ephemeris files required by the engine but absent from "
        f"CHECKSUMS.sha256: {sorted(missing)}. Their integrity is unverified."
    )
    # The manifest is relative to the repository root, which is also where
    # the engine points Swiss Ephemeris and where the runner points swetest.
    assert default_ephemeris_path() == ROOT
    for name in REQUIRED_FILES:
        assert (ROOT / name).is_file()


def test_checksum_verification_detects_a_corrupted_asset(tmp_path):
    """Ephemeris-integrity negative control. Copy-based; real data untouched.

    A gate that cannot fail is not a gate. This corrupts a COPY and proves
    the verification refuses it.
    """

    import certification_support as module

    from engine.astronomy.ephemeris import REQUIRED_FILES

    for name in REQUIRED_FILES:
        shutil.copy2(ROOT / name, tmp_path / name)
    manifest = tmp_path / "CHECKSUMS.sha256"
    manifest.write_text(
        "".join(
            f"{hashlib.sha256((tmp_path / n).read_bytes()).hexdigest()}  {n}\n"
            for n in REQUIRED_FILES
        )
    )

    original_root, original_manifest = module.ROOT, module.CHECKSUM_MANIFEST
    try:
        module.ROOT, module.CHECKSUM_MANIFEST = tmp_path, manifest
        # Positive: the copies verify, so the control is meaningful.
        assert module.verify_data_assets()["assets_verified"] == len(REQUIRED_FILES)

        # Corrupt one byte of one copy.
        victim = tmp_path / REQUIRED_FILES[0]
        data = bytearray(victim.read_bytes())
        data[len(data) // 2] ^= 0xFF
        victim.write_bytes(bytes(data))

        with pytest.raises(module.CertificationFailure) as caught:
            module.verify_data_assets()
        assert "checksum mismatch" in str(caught.value)
    finally:
        module.ROOT, module.CHECKSUM_MANIFEST = original_root, original_manifest

    # The real bundled data was never touched.
    assert support.verify_data_assets()["assets_verified"] >= 3


def test_checksum_verification_detects_a_missing_asset(tmp_path):
    """The other half of the failure mode: absent, not merely altered."""

    import certification_support as module

    from engine.astronomy.ephemeris import REQUIRED_FILES

    name = REQUIRED_FILES[0]
    shutil.copy2(ROOT / name, tmp_path / name)
    manifest = tmp_path / "CHECKSUMS.sha256"
    manifest.write_text(
        f"{hashlib.sha256((tmp_path / name).read_bytes()).hexdigest()}  {name}\n"
    )

    original_root, original_manifest = module.ROOT, module.CHECKSUM_MANIFEST
    try:
        module.ROOT, module.CHECKSUM_MANIFEST = tmp_path, manifest
        assert module.verify_data_assets()["assets_verified"] == 1
        (tmp_path / name).unlink()
        with pytest.raises(module.CertificationFailure) as caught:
            module.verify_data_assets()
        assert "missing" in str(caught.value)
    finally:
        module.ROOT, module.CHECKSUM_MANIFEST = original_root, original_manifest


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


def test_anti_fitting_scan_rejects_a_certifier_named_adjustment(tmp_path):
    """M-03 negative control: verification code is no longer outside the gate."""

    offender = tmp_path / "certify_probe.py"
    offender.write_text("oracle_adjust_for_case = 0.5\n")
    import certification_support as module

    original_root = module.ROOT
    try:
        module.ROOT = tmp_path
        with pytest.raises(module.CertificationFailure) as caught:
            module.scan_for_fitting(targets=("certify_probe.py",))
        assert "suspicious_identifier" in str(caught.value)
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
    # Stored artifacts are history, not proof: pre-M-03 artifacts correctly
    # record their older scan surface. New runs use the strengthened 170-file
    # gate asserted above; do not rewrite unrelated evidence by hand.
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
    # The Tier-0 runner records its verdict inside `summary` alongside the
    # failure list that produced it; the others set it at top level. Read
    # both through the shared helper rather than duplicating the verdict
    # into the artifact purely so this assertion can find it.
    verdict = support._result_of(report)
    assert verdict != "n/a", f"{slug} declares no verdict anywhere"
    assert verdict in rendered.read_text()
    assert verdict in transcript.read_text()
