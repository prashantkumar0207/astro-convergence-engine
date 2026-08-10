"""Assert the running environment matches certification/ORACLE_ENVIRONMENT.json.

The oracle certification runners are only meaningful if the environment that
produced them is the one the repository claims. This check fails loudly on any
divergence rather than certifying against an environment nobody recorded.

Run:  python scripts/check_oracle_environment.py
Exit: 0 on match, 1 on any mismatch.
"""

import json
import platform
import sys
from pathlib import Path

import importlib.metadata as md

ROOT = Path(__file__).resolve().parent.parent
IDENTITY = ROOT / "certification" / "ORACLE_ENVIRONMENT.json"


def main() -> int:
    if not IDENTITY.exists():
        print(f"FAIL: {IDENTITY} absent; cannot verify oracle environment")
        return 1

    env = json.loads(IDENTITY.read_text())
    errors: list[str] = []

    want_minor = ".".join(env["runtime"]["python"].split(".")[:2])
    got_minor = ".".join(platform.python_version().split(".")[:2])
    if got_minor != want_minor:
        errors.append(f"python {got_minor} does not match recorded {want_minor}")

    if platform.machine() != "x86_64":
        errors.append(f"machine {platform.machine()} does not match recorded x86_64")

    try:
        pyjhora = md.version("PyJHora")
        if pyjhora != env["oracle"]["version"]:
            errors.append(f"PyJHora {pyjhora} does not match recorded {env['oracle']['version']}")
    except md.PackageNotFoundError:
        errors.append("PyJHora absent")

    for line in env["dependency_lock"]["closure"]:
        name, version = line.split("==")
        try:
            actual = md.version(name)
        except md.PackageNotFoundError:
            errors.append(f"{name} absent")
            continue
        if actual != version:
            errors.append(f"{name} {actual} does not match locked {version}")

    for filename, digest in env["ephemeris_assets"]["files"].items():
        import hashlib

        path = ROOT / filename
        if not path.exists():
            errors.append(f"{filename} absent")
            continue
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != digest:
            errors.append(f"{filename} checksum does not match recorded value")

    if errors:
        print("ENVIRONMENT IDENTITY MISMATCH:")
        for item in errors:
            print(f"  - {item}")
        print("\nDo not relax this check. Either restore the recorded environment or")
        print("record a new identity with its own lock file and decision entry.")
        return 1

    count = len(env["dependency_lock"]["closure"])
    print(f"environment identity verified: python {got_minor}, PyJHora "
          f"{env['oracle']['version']}, {count} packages match the lock, "
          f"{len(env['ephemeris_assets']['files'])} ephemeris assets match checksums")
    return 0


if __name__ == "__main__":
    sys.exit(main())
