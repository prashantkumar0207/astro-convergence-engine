"""Shared certification support (ADR-0014 proposed).

Closes four requirements of docs/VALIDATION_STANDARD.md that the
per-layer certification runners did not previously meet:

  s2 rule 4  checksummed data assets verified BEFORE any certification
             run (preflight);
  s2 rule 6  an automated anti-fitting scan is PART OF THE GATE, with
             findings cleared by written justification (scan_for_fitting);
  s1         a "certified/locked" claim requires machine-readable results
             AND a human-readable report generated in the SAME run, with
             console/report agreement (emit);
  s3         the machine-readable results, and the exact console
             transcript, are retained alongside the claim (emit).

Every runner calls preflight() early and emit() last. emit() derives the
human-readable report FROM THE SAME dict it serialises, so the two cannot
disagree by construction.
"""

from __future__ import annotations

import atexit
import hashlib
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: Files whose integrity must hold before any certification claim.
CHECKSUM_MANIFEST = ROOT / "CHECKSUMS.sha256"

#: Q24 / B-2. The numerical authority's own integrity, VERIFIED at runtime
#: rather than merely recorded. Before this, `ORACLE_ENVIRONMENT.json`'s
#: `reference_binary_sha256` and `manifest_sha256` were read by nothing: what
#: the gate actually checked was a version string, which any binary can print.
ORACLE_ENVIRONMENT = ROOT / "certification" / "ORACLE_ENVIRONMENT.json"
REFERENCE_BINARY = ROOT / "swetest"

#: Git blob identity of `CHECKSUMS.sha256`, pinned to the commit that ratified
#: it. The current file must hash to THIS constant; the constant is never
#: recomputed from the current file, so the check cannot degrade into a
#: self-comparison (CEO execution control 7). A pinned constant also survives
#: the shallow clones CI checkouts produce, where the historical git object
#: itself may be absent.
MANIFEST_ANCHOR_COMMIT = "a62a2c8f9e021575deeac7dee61f53aaae1bc265"
MANIFEST_ANCHOR_BLOB = "0885f0446ba4306c7afa78eef06a0be2e7b6c5a7"

#: RESIDUAL LIMITATION, recorded rather than papered over. All three trust
#: records for the manifest - its SHA-256 in `ORACLE_ENVIRONMENT.json`, the
#: blob constant above, and the per-file digest duplication between the
#: manifest and `ORACLE_ENVIRONMENT.json` - live inside this repository. They
#: make a SINGLE-file edit fail. A coordinated edit of all of them, in one
#: commit, cannot be cryptographically prevented by any in-repository anchor.
#: The only genuine anchor is upstream provenance (`BUILD_INFO.txt` records the
#: binary as built from aloistr/swisseph v2.10.03), which requires network
#: access and is deliberately out of M1's scope. The committed control
#: `test_trust_record_integrity.py` demonstrates this limitation rather than
#: merely describing it.
TRUST_ANCHOR_RESIDUAL = (
    "coordinated edits to every repository-held trust record cannot be "
    "cryptographically prevented by an in-repository trust anchor; only "
    "upstream provenance would anchor this, and it is out of M1 scope"
)

#: Identifier fragments that would indicate per-case fudging.
_SUSPICIOUS_NAMES = (
    "fudge", "calibrat", "magic_", "hack_", "tweak",
    "correction_for", "offset_for", "adjust_for", "per_case",
)

#: Holdout case identifiers; production code must never mention them.
_HOLDOUT_IDS = re.compile(r"\bH(?:1[01]|[1-9])_[a-z]", re.IGNORECASE)

#: Production code must never import verification-only material.
_FORBIDDEN_IMPORTS = re.compile(
    r"^\s*(?:from|import)\s+(?:jhora|brihat_fixtures|legacy|engine\.tests)\b", re.MULTILINE
)

# M-03: all source locations that can shape a certification claim are scanned,
# not merely the production package. The historical audit named eleven
# certifiers; the current tree contains the later current-engine runner too.
# ADR-0054 added a thirteenth (rise/set); ADR-0055 adds a fourteenth
# (panchanga).
CERTIFIER_SOURCES = (
    "scripts/certify_current_engine.py", "scripts/certify_d12.py",
    "scripts/certify_d16.py",
    "scripts/certify_d2.py", "scripts/certify_d20.py", "scripts/certify_d24.py", "scripts/certify_d3.py",
    "scripts/certify_d30.py", "scripts/certify_d4.py", "scripts/certify_d40.py",
    "scripts/certify_d45.py", "scripts/certify_d7.py", "scripts/certify_kp_chain.py",
    "scripts/certify_kp_significator.py",
    "scripts/certify_panchanga.py", "scripts/certify_parashari_drishti.py",
    "scripts/certify_parashari_yoga.py",
    "scripts/certify_rise_set.py", "scripts/certify_sign_convention.py",
    "scripts/certify_transits.py",
    "scripts/certify_trikalam.py", "scripts/certify_vimshottari.py",
)
VALIDATOR_SOURCES = (
    "validate_d10_holdout.py", "validate_d12_holdout.py",
    "validate_d16_holdout.py", "validate_d24_holdout.py",
    "validate_d20_holdout.py", "validate_d2_holdout.py", "validate_d3_holdout.py",
    "validate_d30_holdout.py", "validate_d4_holdout.py", "validate_d40_holdout.py",
    "validate_d45_holdout.py", "validate_d7_holdout.py",
    "validate_d9_holdout.py", "validate_kp_holdout.py",
    "validate_kp_significator_holdout.py",
    "validate_panchanga_holdout.py", "validate_parashari_drishti_holdout.py",
    "validate_parashari_yoga_holdout.py",
    "validate_rise_set_holdout.py", "validate_transits_holdout.py",
    "validate_trikalam_holdout.py", "validate_vimshottari_holdout.py",
)
FIXTURE_SOURCES = ("brihat_fixtures.py",)
SCAN_TARGETS = ("engine", *CERTIFIER_SOURCES, *VALIDATOR_SOURCES, *FIXTURE_SOURCES)


class CertificationFailure(RuntimeError):
    """Raised when a certification precondition or scan fails."""


def manifest_bytes() -> bytes:
    """`CHECKSUMS.sha256` with line endings normalised to LF.

    The committed blob is LF (234 bytes). A Windows checkout materialises CRLF
    (237 bytes), which changes the file's SHA-256 without changing a single
    digest it records - so a naive hash-the-file check would fail on Windows
    and pass on Linux. Normalisation is applied ONLY to this text manifest; the
    ephemeris assets and the reference binary are hashed as raw bytes and are
    never normalised.
    """

    return CHECKSUM_MANIFEST.read_bytes().replace(b"\r\n", b"\n")


def _git_blob_id(data: bytes) -> str:
    """Git's own blob object id for `data`, computed locally."""

    header = b"blob " + str(len(data)).encode() + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def _parse_manifest(data: bytes) -> dict:
    entries = {}
    for line in data.decode("utf-8").split("\n"):
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        entries[parts[-1]] = parts[0]
    return entries


def verify_trust_records() -> dict:
    """Q24 / B-2: verify the numerical authority itself, not a version string.

    Four checks, each of which fails certification:

    1. the reference binary's bytes hash to the digest `ORACLE_ENVIRONMENT.json`
       records - a check that did not previously exist at all;
    2. the manifest's own bytes hash to the digest that file records;
    3. the manifest's git blob identity equals the pinned constant;
    4. the manifest's per-file digests and `ORACLE_ENVIRONMENT.json`'s duplicate
       list agree, in BOTH directions, so editing either one alone fails.

    Check 4 is what makes single-file tampering detectable. See
    TRUST_ANCHOR_RESIDUAL for what none of this achieves.
    """

    if not ORACLE_ENVIRONMENT.exists():
        raise CertificationFailure(
            "ORACLE_ENVIRONMENT.json absent; trust records unverifiable")
    env = json.loads(ORACLE_ENVIRONMENT.read_text(encoding="utf-8"))

    # 1. The reference binary - the D-001 numerical authority.
    if not REFERENCE_BINARY.exists():
        raise CertificationFailure("reference binary `swetest` absent; cannot certify")
    recorded_binary = env["swiss_ephemeris"]["reference_binary_sha256"]
    binary_bytes = REFERENCE_BINARY.read_bytes()
    actual_binary = hashlib.sha256(binary_bytes).hexdigest()
    if actual_binary != recorded_binary:
        raise CertificationFailure(
            f"reference binary sha256 mismatch: ORACLE_ENVIRONMENT.json records "
            f"{recorded_binary}, the file on disk is {actual_binary}. The D-001 "
            f"numerical authority is not the pinned build."
        )

    # 2. The manifest's own digest.
    data = manifest_bytes()
    recorded_manifest = env["ephemeris_assets"]["manifest_sha256"]
    actual_manifest = hashlib.sha256(data).hexdigest()
    if actual_manifest != recorded_manifest:
        raise CertificationFailure(
            f"CHECKSUMS.sha256 sha256 mismatch: ORACLE_ENVIRONMENT.json records "
            f"{recorded_manifest}, the normalised file is {actual_manifest}"
        )

    # 3. Git blob identity against the pinned constant.
    actual_blob = _git_blob_id(data)
    if actual_blob != MANIFEST_ANCHOR_BLOB:
        raise CertificationFailure(
            f"CHECKSUMS.sha256 blob identity {actual_blob} does not match the "
            f"constant pinned at {MANIFEST_ANCHOR_COMMIT} ({MANIFEST_ANCHOR_BLOB})"
        )

    # 4. Cross-record agreement, both directions.
    manifest_entries = _parse_manifest(data)
    env_entries = env["ephemeris_assets"]["files"]
    if set(manifest_entries) != set(env_entries):
        raise CertificationFailure(
            f"trust records disagree on WHICH assets are covered: manifest "
            f"{sorted(manifest_entries)}, ORACLE_ENVIRONMENT.json {sorted(env_entries)}"
        )
    for name, digest in manifest_entries.items():
        if env_entries[name] != digest:
            raise CertificationFailure(
                f"trust records disagree on {name}: manifest {digest}, "
                f"ORACLE_ENVIRONMENT.json {env_entries[name]}"
            )

    return {
        "reference_binary": REFERENCE_BINARY.name,
        "reference_binary_sha256_verified": actual_binary,
        "reference_binary_bytes": len(binary_bytes),
        "manifest_sha256_verified": actual_manifest,
        "manifest_blob_id_verified": actual_blob,
        "manifest_anchor_commit": MANIFEST_ANCHOR_COMMIT,
        "cross_record_assets_agreed": len(manifest_entries),
        "residual_limitation": TRUST_ANCHOR_RESIDUAL,
    }


def verify_data_assets() -> dict:
    """VALIDATION_STANDARD s2 rule 4: verify checksummed assets."""

    if not CHECKSUM_MANIFEST.exists():
        raise CertificationFailure("CHECKSUMS.sha256 absent; cannot certify")
    verified = {}
    for line in CHECKSUM_MANIFEST.read_text().split("\n"):
        line = line.strip()
        if not line:
            continue
        expected, name = line.split()[0], line.split()[-1]
        target = ROOT / name
        if not target.exists():
            raise CertificationFailure(f"checksummed asset missing: {name}")
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        if digest != expected:
            raise CertificationFailure(
                f"checksum mismatch for {name}: expected {expected}, got {digest}"
            )
        verified[name] = digest
    if not verified:
        raise CertificationFailure("checksum manifest empty")
    return {"assets_verified": len(verified), "sha256": verified}


def _source_files(targets: tuple[str, ...]) -> list[Path]:
    """Resolve the declared scan surface, failing closed on any omission."""

    paths: list[Path] = []
    for target in targets:
        path = ROOT / target
        if path.is_dir():
            paths.extend(
                candidate for candidate in sorted(path.rglob("*.py"))
                if "tests" not in candidate.parts and not candidate.name.startswith("test_")
            )
        elif path.is_file() and path.suffix == ".py":
            paths.append(path)
        else:
            raise CertificationFailure(f"anti-fitting scan target missing or not Python: {target}")
    return paths


def scan_for_fitting(targets: tuple[str, ...] = SCAN_TARGETS) -> dict:
    """
    VALIDATION_STANDARD s2 rule 6: automated anti-fitting scan.

    Flags suspicious identifier fragments in every certification subject. The
    production engine has the stronger policy: no frozen holdout references or
    verification-only imports. Certifiers necessarily declare the holdouts and
    external oracle they execute, so treating those declarations as findings
    would make the gate permanently fail rather than detect fitting.
    """

    findings = []
    scanned = 0
    for path in _source_files(targets):
        text = path.read_text()
        scanned += 1
        relative = path.relative_to(ROOT)
        lowered = text.lower()
        for fragment in _SUSPICIOUS_NAMES:
            if fragment in lowered:
                findings.append({"file": str(relative), "kind": "suspicious_identifier",
                                 "detail": fragment})
        if relative.parts[0] == "engine":
            for match in _HOLDOUT_IDS.finditer(text):
                line = text[: match.start()].count("\n") + 1
                findings.append({"file": f"{relative}:{line}", "kind": "holdout_reference",
                                 "detail": match.group(0)})
            for match in _FORBIDDEN_IMPORTS.finditer(text):
                line = text[: match.start()].count("\n") + 1
                findings.append({"file": f"{relative}:{line}", "kind": "verification_import",
                                 "detail": match.group(0).strip()})
    if findings:
        raise CertificationFailure(
            f"anti-fitting scan produced {len(findings)} finding(s), none justified: {findings}"
        )
    return {
        "modules_scanned": scanned,
        "findings": [],
        "justified_exceptions": [
            "Frozen holdout declarations and oracle imports are permitted only outside engine/; "
            "all scanned sources remain subject to suspicious-identifier detection."
        ],
    }


def _scalar(value) -> str:
    """Render one value for the human-readable report, without truncation.

    Lists become comma-separated text, and an empty list renders as ``none``
    rather than as an empty string, so that "zero failures" is stated rather
    than merely implied by an absent line.
    """

    if isinstance(value, list):
        return ", ".join(str(item) for item in value) if value else "none"
    return str(value)


def _result_of(report: dict) -> str:
    """The run's PASS/FAIL verdict, wherever the runner records it.

    Most runners set a top-level ``result``. The Tier-0 runner records its
    verdict inside ``summary`` alongside the failure list that produced it.
    Reading both avoids duplicating the verdict in the artifact purely so
    that the report can render it, which would create two places for it to
    be wrong.
    """

    if report.get("result"):
        return str(report["result"])
    summary = report.get("summary")
    if isinstance(summary, dict) and summary.get("result"):
        return str(summary["result"])
    return "n/a"


def _render(report: dict) -> str:
    """Human-readable report derived from the machine-readable dict."""

    lines = [
        f"# {report.get('schema', 'certification')} - HUMAN-READABLE REPORT",
        "",
        "Generated by the same run that produced the machine-readable results, per",
        "docs/VALIDATION_STANDARD.md s1. Do not edit: regenerate.",
        "",
        f"- Decision entry: {report.get('adr', 'n/a')}",
    ]
    # ADR-0014: traceability for the retired provisional identifiers. Emitted only
    # when the runner declares one, so artifacts that never carried a provisional
    # identifier render byte-identically to before.
    if report.get("supersedes_provisional_id"):
        lines.append(
            f"- Supersedes provisional identifier: {report['supersedes_provisional_id']}"
        )
    lines += [
        f"- Date: {report.get('date', 'n/a')}",
        f"- Scope: {report.get('scope', 'n/a')}",
    ]
    # C-03: the Tier-0 runner declares its frozen tolerance at top level rather
    # than inside a gate block. Rendered when present so the human-readable
    # evidence states the tolerance the run was judged against. Inert for every
    # artifact that does not declare one.
    if "tolerance_arcsec" in report:
        lines.append(f"- Tolerance: {report['tolerance_arcsec']} arcsec")
    lines += [
        f"- Result: **{_result_of(report)}**",
        "",
    ]
    # C-03: run metadata (source revision, engine version, execution stamp).
    # Inert for artifacts that do not declare a run block.
    run = report.get("run")
    if isinstance(run, dict) and run:
        lines += ["## Run metadata", ""]
        lines += [f"- {key}: {_scalar(value)}" for key, value in run.items()]
        lines.append("")
    preconditions = report.get("preconditions")
    if preconditions:
        lines += ["## Preconditions", ""]
        assets = preconditions.get("data_assets", {})
        scan = preconditions.get("anti_fitting", {})
        lines += [
            f"- Data assets verified against CHECKSUMS.sha256: {assets.get('assets_verified')}",
            f"- Anti-fitting scan: {scan.get('modules_scanned')} production modules, "
            f"{len(scan.get('findings', []))} findings",
            "",
        ]
    gates = report.get("gates", {})
    if gates:
        lines += ["## Gates", ""]
        for name, value in gates.items():
            if isinstance(value, dict):
                summary = ", ".join(
                    f"{k}={v}" for k, v in value.items()
                    if isinstance(v, (int, float, str, bool)) and len(str(v)) <= 80
                )
            else:
                summary = str(value)
            lines.append(f"- **{name}**: {summary or 'see machine-readable results'}")
        lines.append("")
    # C-03: the summary block carries the numbers a reader needs in order to
    # check the claim: comparison counts, numerical maxima, fallback count,
    # failures and result. Rendered from the SAME dict that is serialised, so
    # the two evidence files cannot disagree. Inert for artifacts with no
    # summary block, which is every artifact predating this change.
    summary = report.get("summary")
    if isinstance(summary, dict) and summary:
        lines += ["## Summary", ""]
        lines += [f"- **{key}**: {_scalar(value)}" for key, value in summary.items()]
        lines.append("")
    non_claims = report.get("explicit_non_claims")
    if non_claims:
        lines += ["## Explicit non-claims", ""] + [f"- {item}" for item in non_claims] + [""]
    lines += [
        "## Evidence files",
        "",
        f"- machine-readable: `certification/{report.get('_artifact_name', '')}`",
        f"- console transcript: `reports/certification/{report.get('_slug', '')}.console.txt`",
        "",
    ]
    return "\n".join(lines)


class _Tee(io.TextIOBase):
    """Capture stdout while still printing it."""

    def __init__(self, stream):
        self.stream = stream
        self.buffer_text = io.StringIO()

    def write(self, text):
        self.buffer_text.write(text)
        return self.stream.write(text)

    def flush(self):
        self.stream.flush()


def start_transcript() -> _Tee:
    """Begin capturing the console transcript (s3 retention)."""

    tee = _Tee(sys.stdout)
    sys.stdout = tee
    return tee


def preflight() -> dict:
    """Run both mandatory preconditions and return them for the report."""

    return {
        "data_assets": verify_data_assets(),
        "trust_records": verify_trust_records(),
        "anti_fitting": scan_for_fitting(),
    }


def emit(report: dict, artifact_name: str, slug: str, tee=None) -> Path:
    """
    Write the machine-readable artifact, the human-readable report
    derived from the same dict, and the console transcript.
    """

    report["_artifact_name"] = artifact_name
    report["_slug"] = slug
    artifact = ROOT / "certification" / artifact_name
    # Inert where the directory is tracked, which is every current case. Kept
    # so that routing a runner through emit() cannot lose the directory
    # creation that runner did for itself.
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(json.dumps(report, indent=1) + "\n")

    reports_dir = ROOT / "reports" / "certification"
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / f"{slug}.report.md").write_text(_render(report))

    if tee is not None:
        # Flush at interpreter exit, not here: emit() is called before a
        # runner prints its console summary, and s3 requires the EXACT
        # transcript, which therefore is only complete at exit.
        target = reports_dir / f"{slug}.console.txt"

        def _flush_transcript():
            sys.stdout = tee.stream
            target.write_text(tee.buffer_text.getvalue())

        atexit.register(_flush_transcript)
    return artifact
