#!/usr/bin/env python3
"""
Mutation-detection gate (proposed; see DP-030).

A certification gate proves nothing unless it can FAIL. This script
verifies that claim mechanically instead of by reading the code: it
deliberately corrupts a certified computation and requires the
certifier's own correctness gates to detect the corruption.

Motivation (2026-08-26 forensic experiment, KP_SIGNIFICATOR_V1):
every one of that certifier's runnable gates reported PASS while
every sub-lord it computed was wrong. The defect was structural -
each gate sourced its expected value from the same runtime that
produced the actual value, so both sides moved together and the
comparison reduced to `x != x`. No amount of added cases fixes
that; 12,960 tautologies are as empty as one.

This gate is the standing guard against that defect class. It is
deliberately mechanical: it does not read code, trust a docstring,
or rely on a reviewer noticing circularity. It corrupts and looks.

The corruption disguises itself as legitimate source-level code
(`__module__`/`__name__` preserved), because a tamper-detector that
only catches monkeypatching - as KP_SIGNIFICATOR_V1's gate D does,
via `kp_chain.__module__ != "engine.kp.chain"` - would not catch a
wrong implementation actually written into the module. The realistic
defect is a developer writing incorrect logic, not an attacker
patching at runtime.

Exit code 0 = the certifier's gates DETECTED the corruption (good).
Exit code 1 = at least one gate passed while the computation was
              wrong: that gate is not load-bearing (bad).
Exit code 2 = harness error (the corruption did not take effect, or
              the target could not be driven); never reported as PASS.

Read-only with respect to the repository: imports the certifier and
calls its gate functions directly, deliberately bypassing main() so
that no transcript, artifact, or report file is written.
"""

import argparse
import contextlib
import dataclasses
import importlib
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))


class HarnessError(RuntimeError):
    """The experiment could not be performed - never a PASS."""


def _corrupt_kp_chain():
    """
    Return a kp_chain replacement that rotates sub_lord one step along
    the KP lord cycle - wrong at every longitude, structurally valid,
    and indistinguishable from genuine source code by metadata.
    """
    from engine.kp.tables import KP_LORDS
    import engine.kp.chain as chain_module

    pristine = chain_module.kp_chain

    def corrupted(longitude):
        real = pristine(longitude)
        index = KP_LORDS.index(real.sub_lord)
        return dataclasses.replace(real, sub_lord=KP_LORDS[(index + 1) % len(KP_LORDS)])

    # Disguise as source-level code: a wrong implementation written into
    # engine/kp/chain.py would carry exactly this metadata.
    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)

    # Prove the corruption is total before trusting any PASS below.
    changed = sum(
        1 for step in range(0, 3600)
        if pristine(step / 10).sub_lord != corrupted(step / 10).sub_lord
    )
    if changed != 3600:
        raise HarnessError(
            f"corruption did not take effect at every sampled longitude "
            f"({changed}/3600); a PASS below would be meaningless"
        )
    return pristine, corrupted, changed


#: Gates whose stated purpose is detecting an incorrect significator
#: result. At least one MUST fail when the computation is corrupted.
#: Gate D is deliberately excluded: it is a module-identity tamper
#: check, not a correctness check, and it cannot see a wrong value
#: written into the module itself. Gate C is deliberately excluded: it
#: runs in a separate subprocess that does not observe this in-process
#: kp_chain patch (proven by the literal on-disk file-edit-run-revert
#: experiment instead - see the certification-repair report). Gate I is
#: INCLUDED as of the 2026-08-27 repair: since it now compares production
#: against STATIC frozen expected values (rather than a live "independent"
#: re-derivation that shared the same corrupted kp_chain), it correctly
#: detects this substrate-level corruption too - verified directly: before
#: the repair gate I passed blind under this same corruption despite a
#: different verdict distribution; after the repair it fails with an
#: explicit per-case mismatch.
KP_SIGNIFICATOR_CORRECTNESS_GATES = (
    "gate_b_dense_sweep",
    "gate_e_boundary_cases",
    "gate_f_retrograde_cases",
    "gate_g_node_aspect_cases",
    "gate_h_strength_order_cases",
    "gate_i_protected_holdout",
    "gate_j_negative_controls",
)


def run_kp_significator(verbose=True):
    import engine.kp.chain as chain_module
    import engine.kp.chart as chart_module

    pristine, corrupted, changed = _corrupt_kp_chain()
    chain_module.kp_chain = corrupted
    # engine.kp.chart does `from engine.kp.chain import kp_chain` at its own
    # module level, binding its own separate name - patching chain_module's
    # attribute above does not reach it. gate_i_protected_holdout builds its
    # charts via kp_chart(), so without this second patch the corruption
    # would silently miss gate I's own real-chart construction.
    chart_module.kp_chain = corrupted

    certifier = importlib.import_module("certify_kp_significator")
    certifier.kp_chain = corrupted

    if verbose:
        print(f"corruption verified: sub_lord wrong at {changed}/3600 sampled longitudes")
        print("running the certifier's own correctness gates against it\n")

    detected, passed_blind = [], []
    for name in KP_SIGNIFICATOR_CORRECTNESS_GATES:
        gate = getattr(certifier, name, None)
        if gate is None:
            raise HarnessError(f"{name} not found in certify_kp_significator")
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                gate()
        except SystemExit:
            detected.append(name)
            if verbose:
                print(f"  {name:30s} FAILED - detected the wrong value (good)")
            continue
        except Exception as error:            # noqa: BLE001
            raise HarnessError(f"{name} raised {type(error).__name__}: {error}") from error
        passed_blind.append(name)
        if verbose:
            print(f"  {name:30s} PASSED - blind to the wrong value (BAD)")

    return detected, passed_blind


def _corrupt_signifies():
    """
    Return a _signifies replacement that drops the 'planet_name ==
    owner_name' clause - a realistic wrong-implementation mistake (an
    engineer forgetting the owner category) that changes neither
    PROMISE_HOUSES/DENY_HOUSES/SPECIAL_ASPECTS/KP_GRAHAS (so gate A's
    content-hash pin does not see it) nor kp_chain (so this corrupts the
    SIGNIFICATOR layer specifically, unlike _corrupt_kp_chain above, which
    corrupts the shared, separately-certified KP_CHAIN_V1 substrate).
    """
    import engine.kp.significators as sig_module

    pristine = sig_module._signifies

    def corrupted(planet_name, house, chart, cusp_lons):
        occupant_names = {
            body.name for body in chart.bodies
            if body.name in sig_module.KP_GRAHAS
            and sig_module.house_of_placidus(body.longitude, cusp_lons) == house
        }
        owner_name = sig_module.full_name(chart.cusps[house - 1].chain.sign_lord)
        nl = sig_module.full_name(sig_module._body(chart, planet_name).chain.nakshatra_lord)
        return (
            planet_name in occupant_names
            # deliberately dropped: `or planet_name == owner_name`
            or nl in occupant_names
            or nl == owner_name
        )

    corrupted.__module__ = pristine.__module__
    corrupted.__name__ = pristine.__name__
    corrupted.__qualname__ = getattr(pristine, "__qualname__", pristine.__name__)
    return pristine, corrupted


#: Gates run against a _signifies corruption - the full correctness-relevant
#: set, including gate I (now the static-holdout comparison) and the
#: negative controls, since this corruption targets the significator layer
#: itself rather than the shared kp_chain substrate. Gate D is excluded for
#: the same reason as above (module-identity check, not correctness). Gate
#: C is excluded because it runs in a separate subprocess that does not see
#: this in-process patch - proving that requires the literal on-disk
#: file-edit-run-revert experiment (see the CEO directive's own item 7,
#: performed separately and recorded in the certification-repair report).
KP_SIGNIFICATOR_LOGIC_CORRECTNESS_GATES = (
    "gate_b_dense_sweep",
    "gate_e_boundary_cases",
    "gate_f_retrograde_cases",
    "gate_g_node_aspect_cases",
    "gate_h_strength_order_cases",
    "gate_i_protected_holdout",
    "gate_j_negative_controls",
)


def run_kp_significator_logic(verbose=True):
    import engine.kp.significators as sig_module

    pristine, corrupted = _corrupt_signifies()
    sig_module._signifies = corrupted

    # certify_kp_significator.py never binds _signifies at module level -
    # every gate that needs it does `from engine.kp.significators import
    # _signifies` freshly inside its own function body, and judge_marriage/
    # signification_set call it via engine.kp.significators' own module
    # globals - so patching the attribute above is sufficient; no separate
    # patch on the certifier module is needed or meaningful.
    certifier = importlib.import_module("certify_kp_significator")

    if verbose:
        print("corruption: engine.kp.significators._signifies() with the owner-membership "
              "clause dropped (content hash and kp_chain both untouched)")
        print("running the certifier's own correctness gates against it\n")

    detected, passed_blind = [], []
    for name in KP_SIGNIFICATOR_LOGIC_CORRECTNESS_GATES:
        gate = getattr(certifier, name, None)
        if gate is None:
            raise HarnessError(f"{name} not found in certify_kp_significator")
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                gate()
        except SystemExit:
            detected.append(name)
            if verbose:
                print(f"  {name:30s} FAILED - detected the wrong value (good)")
            continue
        except Exception as error:            # noqa: BLE001
            raise HarnessError(f"{name} raised {type(error).__name__}: {error}") from error
        passed_blind.append(name)
        if verbose:
            print(f"  {name:30s} PASSED - blind to the wrong value (BAD)")

    sig_module._signifies = pristine
    certifier._signifies = pristine

    return detected, passed_blind


TARGETS = {
    "kp_significator": run_kp_significator,
    "kp_significator_logic": run_kp_significator_logic,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=sorted(TARGETS), nargs="?", default="kp_significator")
    args = parser.parse_args()

    print(f"MUTATION DETECTION GATE: {args.target}")
    print("=" * 62)
    try:
        detected, passed_blind = TARGETS[args.target]()
    except HarnessError as error:
        print(f"\nHARNESS ERROR: {error}")
        print("RESULT: INCONCLUSIVE (exit 2) - not a pass.")
        return 2

    print()
    if not detected:
        print("RESULT: FAIL (exit 1)")
        print(f"  {len(passed_blind)} correctness gate(s) passed while every computed")
        print("  sub_lord was wrong, and none detected it. These gates are not")
        print("  load-bearing: they compare the implementation against itself.")
        print(f"  Blind gates: {', '.join(passed_blind)}")
        return 1

    print("RESULT: PASS (exit 0)")
    print(f"  Detected by: {', '.join(detected)}")
    if passed_blind:
        print(f"  Note - blind to the corruption (informational): {', '.join(passed_blind)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
