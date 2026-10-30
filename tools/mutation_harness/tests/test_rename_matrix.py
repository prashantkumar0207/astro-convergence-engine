"""Rename matrix RN-1 to RN-6b (R1 s5.4.2, corrected by RD-C3).

Real git, in disposable temporary repositories only. Records are compared as a
multiset, because porcelain v2 emits changed entries before untracked and ignored ones.
"""

import os
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

HARNESS_DIR = Path(__file__).resolve().parents[1]
if str(HARNESS_DIR) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR))

import gitstatus  # noqa: E402

ZERO_MODE = "000000"
ZERO_OID = "0" * 40
AL = frozenset({"certification/A.json"})


@pytest.fixture(autouse=True)
def isolated_git_config(monkeypatch):
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")


def git(repo, *args):
    return subprocess.run(
        ["git", "-C", str(repo), "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
         *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q")
    (root / "a.txt").write_text("rename matrix fixture line\n" * 20)
    (root / "engine_x.txt").write_text("engine fixture line\n" * 20)
    git(root, "add", "a.txt", "engine_x.txt")
    git(root, "commit", "-q", "-m", "fixture")
    return root


def records(repo, renames):
    return gitstatus.parse_records(gitstatus.split_records(gitstatus.run_git_status(repo, renames=renames)))


def shape(recs):
    return Counter((r.kind, r.xy, r.path, r.orig_path) for r in recs)


def by_path(recs):
    return {r.path: r for r in recs}


def test_RN1_staged_rename_detection_enabled(repo):
    git(repo, "mv", "a.txt", "b.txt")
    recs = records(repo, renames=True)
    assert shape(recs) == Counter({("2", "R.", "b.txt", "a.txt"): 1})
    assert recs[0].fields[-1] == "R100"
    assert not gitstatus.classify(recs, AL).clean


def test_RN2_staged_rename_detection_disabled(repo):
    git(repo, "mv", "a.txt", "b.txt")
    recs = records(repo, renames=False)
    assert shape(recs) == Counter({("1", "D.", "a.txt", None): 1, ("1", "A.", "b.txt", None): 1})
    deleted, added = by_path(recs)["a.txt"], by_path(recs)["b.txt"]
    # fields = (XY, sub, mH, mI, mW, hH, hI)
    assert deleted.fields[3] == ZERO_MODE and deleted.fields[4] == ZERO_MODE and deleted.fields[6] == ZERO_OID
    assert added.fields[2] == ZERO_MODE and added.fields[5] == ZERO_OID
    assert not gitstatus.classify(recs, AL).clean


@pytest.mark.parametrize("renames", [True, False], ids=["RN3_enabled", "RN4_disabled"])
def test_RN3_RN4_unstaged_filesystem_rename(repo, renames):
    os.rename(repo / "a.txt", repo / "b.txt")
    recs = records(repo, renames=renames)
    assert shape(recs) == Counter({("1", ".D", "a.txt", None): 1, ("?", None, "b.txt", None): 1})
    assert by_path(recs)["a.txt"].fields[4] == ZERO_MODE
    assert not gitstatus.classify(recs, AL).clean


@pytest.mark.parametrize("renames", [True, False], ids=["enabled", "disabled"])
def test_RN5_intent_to_add_rename_classification_only(repo, renames, capsys):
    """Record shapes are observed and printed, not asserted (R1: not verified on the
    target git version); only the fail-closed classification is asserted."""

    os.rename(repo / "a.txt", repo / "b.txt")
    git(repo, "add", "-N", "b.txt")
    recs = records(repo, renames=renames)
    print("RN-5", "renames" if renames else "no-renames", sorted(shape(recs).items(), key=repr))
    assert recs
    assert not gitstatus.classify(recs, AL | {"b.txt", "a.txt"}).clean


def test_RN6_rename_into_allow_listed_path_enabled(repo):
    (repo / "certification").mkdir()
    git(repo, "mv", "engine_x.txt", "certification/A.json")
    recs = records(repo, renames=True)
    assert shape(recs) == Counter({("2", "R.", "certification/A.json", "engine_x.txt"): 1})
    verdict = gitstatus.classify(recs, AL)
    assert not verdict.clean and verdict.allowed == ()


def test_RN6b_rename_into_allow_listed_path_disabled(repo):
    (repo / "certification").mkdir()
    git(repo, "mv", "engine_x.txt", "certification/A.json")
    recs = records(repo, renames=False)
    assert shape(recs) == Counter({("1", "D.", "engine_x.txt", None): 1,
                                   ("1", "A.", "certification/A.json", None): 1})
    verdict = gitstatus.classify(recs, AL)
    assert not verdict.clean and verdict.allowed == ()


def test_worktree_modification_of_allow_listed_artifact_is_clean(repo):
    """Positive control on real git: an unstaged modification of an exact allow-listed
    tracked file is the one allowed shape."""

    (repo / "certification").mkdir()
    (repo / "certification" / "A.json").write_text("{}\n")
    git(repo, "add", "certification/A.json")
    git(repo, "commit", "-q", "-m", "artifact")
    (repo / "certification" / "A.json").write_text('{"changed": true}\n')
    verdict = gitstatus.status_verdict(repo, AL)
    assert verdict.clean and verdict.allowed == ("certification/A.json",)


def test_ignored_entries_are_listed_for_the_hygiene_baseline(repo):
    """`--ignored=matching` reports a wholly ignored directory as ONE collapsed entry
    (`__pycache__/`), not per file (observed on git 2.43; the first version of this test
    expected per-file entries and was corrected, see IMPLEMENTATION_EVIDENCE.md). The
    harness therefore requires an EMPTY ignored set at S0 (hygiene), so any ignored entry
    that appears later - directory or file - is new."""

    (repo / ".gitignore").write_text("__pycache__/\n")
    git(repo, "add", ".gitignore")
    git(repo, "commit", "-q", "-m", "ignore")
    assert gitstatus.ignored_paths(repo) == frozenset()
    (repo / "__pycache__").mkdir()
    (repo / "__pycache__" / "m.cpython-311.pyc").write_bytes(b"x")
    assert gitstatus.ignored_paths(repo) == frozenset({"__pycache__/"})
    verdict = gitstatus.status_verdict(repo, AL)
    assert not verdict.clean and verdict.ignored_new == ("__pycache__/",)


def test_ignored_reporting_is_directory_granular_limitation(repo):
    """Documented limitation: a NEW file inside an ALREADY-ignored directory produces no
    new entry under `--ignored=matching`. This is why S0 refuses any pre-existing ignored
    entry (state-machine test C7d) and why the harness separately scans for .pyc files."""

    (repo / ".gitignore").write_text("__pycache__/\n")
    git(repo, "add", ".gitignore")
    git(repo, "commit", "-q", "-m", "ignore")
    (repo / "__pycache__").mkdir()
    (repo / "__pycache__" / "old.pyc").write_bytes(b"x")
    before = gitstatus.ignored_paths(repo)
    (repo / "__pycache__" / "new.pyc").write_bytes(b"y")
    assert gitstatus.ignored_paths(repo) == before == frozenset({"__pycache__/"})
