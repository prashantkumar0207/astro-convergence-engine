"""Q24 / B-2 negative controls: the trust-record verification must FAIL.

`certification_support.verify_trust_records()` was added because
`ORACLE_ENVIRONMENT.json` recorded the reference binary's SHA-256 and the
checksum manifest's own SHA-256 and **nothing read either of them**. What the
gate actually checked was a version string, which any binary can print.

A gate that cannot fail is not evidence (`.claude/rules/certification.md`), so
every check added there has a control here that plants a real violation and
demands rejection. One control deliberately demonstrates what the design does
NOT achieve - see `test_coordinated_edit_of_every_trust_record_is_NOT_caught`.

Every control operates on copies under `tmp_path`. The real manifest, binary
and environment record are never written to, and the final test asserts that.
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

#: Captured at import, BEFORE any monkeypatch. Staging reads the real records
#: through these, so staging twice in one test cannot copy a patched path onto
#: itself.
REAL_MANIFEST = support.CHECKSUM_MANIFEST
REAL_ENVIRONMENT = support.ORACLE_ENVIRONMENT
REAL_BINARY = support.REFERENCE_BINARY


def _real_manifest_bytes() -> bytes:
    return REAL_MANIFEST.read_bytes().replace(b"\r\n", b"\n")


def _stage(tmp_path, manifest_bytes=None, env=None, binary_bytes=None):
    """Copy the three trust records into tmp_path, optionally perturbed, and
    point the module's constants at the copies."""

    manifest = tmp_path / "CHECKSUMS.sha256"
    manifest.write_bytes(
        REAL_MANIFEST.read_bytes() if manifest_bytes is None else manifest_bytes
    )

    env_path = tmp_path / "ORACLE_ENVIRONMENT.json"
    real_env = json.loads(REAL_ENVIRONMENT.read_text(encoding="utf-8"))
    env_path.write_text(json.dumps(real_env if env is None else env), encoding="utf-8")

    binary = tmp_path / "swetest"
    if binary_bytes is None:
        shutil.copy(REAL_BINARY, binary)
    else:
        binary.write_bytes(binary_bytes)

    return manifest, env_path, binary


@pytest.fixture
def staged(tmp_path, monkeypatch):
    def _apply(**kwargs):
        manifest, env_path, binary = _stage(tmp_path, **kwargs)
        monkeypatch.setattr(support, "CHECKSUM_MANIFEST", manifest)
        monkeypatch.setattr(support, "ORACLE_ENVIRONMENT", env_path)
        monkeypatch.setattr(support, "REFERENCE_BINARY", binary)
        return manifest, env_path, binary
    return _apply


def test_unperturbed_copies_verify(staged):
    """Baseline. Without this, a control that fails proves nothing."""

    staged()
    result = support.verify_trust_records()
    assert result["cross_record_assets_agreed"] == 3
    assert result["manifest_blob_id_verified"] == support.MANIFEST_ANCHOR_BLOB


def test_tampered_reference_binary_is_caught(staged):
    """The D-001 numerical authority replaced by a different build."""

    staged(binary_bytes=b"#!/bin/sh\necho 'SWISS EPHEMERIS  2.10.03'\n")
    with pytest.raises(support.CertificationFailure, match="reference binary sha256 mismatch"):
        support.verify_trust_records()


def test_manifest_edited_alone_is_caught(staged):
    """A single-file edit of the manifest, leaving every other record intact.

    This is the case the cross-record duplication exists to catch.
    """

    tampered = _real_manifest_bytes().replace(b"a2cd8fc", b"deadbee")
    staged(manifest_bytes=tampered)
    with pytest.raises(support.CertificationFailure):
        support.verify_trust_records()


def test_environment_record_edited_alone_is_caught(staged):
    """The mirror case: ORACLE_ENVIRONMENT.json edited, manifest untouched."""

    env = json.loads(REAL_ENVIRONMENT.read_text(encoding="utf-8"))
    env["ephemeris_assets"]["files"]["seas_18.se1"] = "0" * 64
    staged(env=env)
    with pytest.raises(support.CertificationFailure, match="trust records disagree on seas_18.se1"):
        support.verify_trust_records()


def test_manifest_blob_identity_is_pinned_not_recomputed(staged):
    """Control for CEO execution control 7.

    Adding a line changes the blob identity. If the constant were recomputed
    from the current file this would pass, which is exactly the self-comparison
    the control forbids.
    """

    env = json.loads(REAL_ENVIRONMENT.read_text(encoding="utf-8"))
    extended = _real_manifest_bytes() + b"0" * 64 + b"  extra_asset.se1\n"
    # Keep the OTHER two records consistent with the edit, so the only check
    # that can still fail is the pinned blob identity.
    env["ephemeris_assets"]["manifest_sha256"] = hashlib.sha256(extended).hexdigest()
    env["ephemeris_assets"]["files"]["extra_asset.se1"] = "0" * 64
    staged(manifest_bytes=extended, env=env)
    with pytest.raises(support.CertificationFailure, match="blob identity"):
        support.verify_trust_records()


def test_crlf_and_lf_manifests_verify_identically(staged):
    """Platform independence, the defect that would have broken this on Windows.

    The committed blob is LF; a Windows checkout materialises CRLF. That changes
    the file's raw SHA-256 without changing a single digest it records.
    """

    lf = _real_manifest_bytes()
    crlf = lf.replace(b"\n", b"\r\n")
    assert hashlib.sha256(crlf).hexdigest() != hashlib.sha256(lf).hexdigest()

    staged(manifest_bytes=crlf)
    from_crlf = support.verify_trust_records()
    staged(manifest_bytes=lf)
    from_lf = support.verify_trust_records()
    assert from_crlf["manifest_sha256_verified"] == from_lf["manifest_sha256_verified"]
    assert from_crlf["manifest_blob_id_verified"] == from_lf["manifest_blob_id_verified"]


def test_coordinated_edit_of_every_trust_record_is_NOT_caught(staged):
    """THE RESIDUAL, demonstrated rather than described.

    An attacker who edits the ephemeris asset, the manifest, the environment
    record AND the pinned constant together passes every check. No
    in-repository anchor can prevent this; only upstream provenance could, and
    that is out of M1's scope by the CEO's own exclusion.

    This test asserts the limitation so that it cannot quietly disappear: if a
    future change genuinely closes it, this test fails and must be rewritten
    deliberately rather than the claim being silently strengthened.
    """

    forged_digest = "1" * 64
    lines = _real_manifest_bytes().decode().strip().split("\n")
    lines[0] = f"{forged_digest}  seas_18.se1"
    forged_manifest = ("\n".join(lines) + "\n").encode()

    env = json.loads(REAL_ENVIRONMENT.read_text(encoding="utf-8"))
    env["ephemeris_assets"]["files"]["seas_18.se1"] = forged_digest
    env["ephemeris_assets"]["manifest_sha256"] = hashlib.sha256(forged_manifest).hexdigest()

    manifest, env_path, binary = staged(manifest_bytes=forged_manifest, env=env)
    # The fourth record, the pinned constant, moved in the same act.
    import pytest as _pytest  # noqa: F401
    original_blob = support.MANIFEST_ANCHOR_BLOB
    try:
        support.MANIFEST_ANCHOR_BLOB = support._git_blob_id(forged_manifest)
        result = support.verify_trust_records()
    finally:
        support.MANIFEST_ANCHOR_BLOB = original_blob

    assert result["cross_record_assets_agreed"] == 3, (
        "the coordinated-edit control no longer demonstrates the residual; if "
        "the limitation has genuinely been closed, rewrite this test "
        "deliberately and update TRUST_ANCHOR_RESIDUAL"
    )
    assert "coordinated edits" in support.TRUST_ANCHOR_RESIDUAL
    assert support.MANIFEST_ANCHOR_BLOB == original_blob


def test_controls_left_the_real_trust_records_untouched():
    """Every control above ran on copies. Prove the originals are intact."""

    env = json.loads(REAL_ENVIRONMENT.read_text(encoding="utf-8"))
    assert hashlib.sha256(REAL_BINARY.read_bytes()).hexdigest() == (
        env["swiss_ephemeris"]["reference_binary_sha256"]
    )
    assert hashlib.sha256(_real_manifest_bytes()).hexdigest() == (
        env["ephemeris_assets"]["manifest_sha256"]
    )
    assert support._git_blob_id(_real_manifest_bytes()) == support.MANIFEST_ANCHOR_BLOB
    # And the real verification still passes against the real files.
    support.verify_trust_records()
