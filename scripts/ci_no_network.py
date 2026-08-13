"""Hermeticity harness (ADR-0018).

Runs a script or module with all socket creation disabled, so a gate that
silently depends on the network FAILS instead of passing quietly.

Scope of the guarantee, stated exactly: this blocks socket creation inside
this Python process, which is the path every Python HTTP, DNS, and database
client takes. It does not sandbox child processes. The certification runners
launch no network child processes; the only external binary used anywhere in
the gate is the bundled local `swetest`.

Usage:
    python scripts/ci_no_network.py <script.py> [args...]
    python scripts/ci_no_network.py -m <module> [args...]

Exit code is the exit code of the wrapped target. A blocked connection
attempt raises NoNetworkError, which surfaces as a normal failure.
"""

import runpy
import socket
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class NoNetworkError(RuntimeError):
    """Raised when a hermetic gate attempts to use the network."""


def _blocked(*args, **kwargs):
    raise NoNetworkError(
        "network access attempted inside a hermetic gate; the hermetic tier "
        "must run with no network. Do not relax this check: find the caller."
    )


def _install_guard() -> None:
    """Block outbound connections without replacing the socket class.

    The class itself is left intact on purpose: `ssl` subclasses
    `socket.socket` at import time, so swapping the class out breaks
    stdlib imports and produces a false failure rather than a real one.
    Only the operations that actually reach the network are blocked.
    """
    socket.socket.connect = _blocked      # type: ignore[assignment]
    socket.socket.connect_ex = _blocked   # type: ignore[assignment]
    socket.create_connection = _blocked   # type: ignore[assignment]
    socket.getaddrinfo = _blocked         # type: ignore[assignment]
    socket.gethostbyname = _blocked       # type: ignore[assignment]


def main() -> int:
    argv = sys.argv[1:]
    if not argv:
        print(__doc__)
        return 2

    sys.path.insert(0, str(ROOT))
    _install_guard()

    if argv[0] == "-m":
        if len(argv) < 2:
            print("ci_no_network: -m requires a module name", file=sys.stderr)
            return 2
        module, rest = argv[1], argv[2:]
        sys.argv = [module] + rest
        try:
            runpy.run_module(module, run_name="__main__", alter_sys=True)
        except SystemExit as exc:
            return int(exc.code or 0)
        return 0

    target = argv[0]
    sys.argv = [target] + argv[1:]
    try:
        runpy.run_path(str(ROOT / target), run_name="__main__")
    except SystemExit as exc:
        return int(exc.code or 0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
