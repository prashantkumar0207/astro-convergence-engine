"""Step 1: dependency/environment validation + ephemeris checksum validation. Fails loudly."""
import sys, hashlib
from pathlib import Path
ROOT = Path(__file__).resolve().parent

def fail(msg):
    print("PREFLIGHT FAIL:", msg); sys.exit(2)

def main():
    if sys.version_info < (3, 9):
        fail(f"Python >= 3.9 required, found {sys.version.split()[0]}")
    try:
        import swisseph as swe
    except ImportError:
        fail("pyswisseph not installed (pip install -r requirements.lock)")
    try:
        import pytest  # noqa
    except ImportError:
        fail("pytest not installed (pip install -r requirements.lock)")
    ephe = ROOT / "ephe"
    manifest = ephe / "CHECKSUMS.sha256"
    if not manifest.exists():
        fail(f"missing checksum manifest {manifest}")
    n = 0
    for line in manifest.read_text().splitlines():
        if not line.strip():
            continue
        want, fname = line.split()
        f = ephe / fname
        if not f.exists():
            fail(f"required ephemeris file absent: {f}")
        got = hashlib.sha256(f.read_bytes()).hexdigest()
        if got != want:
            fail(f"checksum mismatch for {fname}: expected {want}, got {got}")
        n += 1
    if n < 2:
        fail("manifest must pin at least sepl_18.se1 and semo_18.se1")
    print(f"PREFLIGHT OK: python {sys.version.split()[0]}, pyswisseph {swe.version}, "
          f"{n} ephemeris files checksum-verified")
if __name__ == "__main__":
    main()
