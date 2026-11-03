"""Porcelain v2 status parsing and exact allow-list classification (WP-RD-B, R1 s5.3).

The status output is captured as raw bytes and is never stripped: porcelain v2 with -z
terminates every record with NUL and needs no whitespace handling. Every record is
validated field by field. Anything malformed, truncated or unrecognised raises
StatusParseError, and a failed git invocation raises GitStatusError. Neither may ever
be read as an empty, clean status.

The parser is deliberately split into small functions (split_records, parse_records,
classify) so that each can be mutation-tested independently
(tests/test_gitstatus_mutants.py applies exact-once source mutations to this file).
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass

#: The harness status command. Every behaviour-relevant option is explicit, so user or
#: repository configuration (status.renames, status.showUntrackedFiles, diff.renames)
#: cannot change the output shape.
STATUS_ARGS = (
    "status",
    "--porcelain=v2",
    "-z",
    "--untracked-files=all",
    "--ignored=matching",
    "--no-renames",
)

#: `git status --no-renames` and porcelain v2 both require at least this version.
MIN_GIT_VERSION = (2, 18)

_XY = re.compile(rb"[.MTADRCU]{2}\Z")
_SUB = re.compile(rb"(N\.\.\.|S[C.][M.][U.])\Z")
_MODE = re.compile(rb"[0-7]{6}\Z")
_OID = re.compile(rb"([0-9a-f]{40}|[0-9a-f]{64})\Z")
_SCORE = re.compile(rb"[RC][0-9]{1,3}\Z")


class StatusParseError(Exception):
    """Status output was malformed, truncated or of an unrecognised shape."""


class GitStatusError(Exception):
    """git could not be run, or exited non-zero."""


@dataclass(frozen=True)
class Record:
    """One porcelain v2 record. `kind` is the record-type token: 1, 2, u, ? or !."""

    kind: str
    path: str
    xy: str | None = None
    orig_path: str | None = None
    fields: tuple[str, ...] = ()

    def describe(self) -> str:
        parts = [self.kind]
        if self.xy is not None:
            parts.append(self.xy)
        parts.append(self.path)
        if self.orig_path is not None:
            parts.append(f"<- {self.orig_path}")
        return " ".join(parts)


@dataclass(frozen=True)
class Verdict:
    """Classification of a parsed status against an exact allow-list."""

    clean: bool
    allowed: tuple[str, ...]
    outside: tuple[str, ...]
    ignored_new: tuple[str, ...]


def _decode(raw: bytes) -> str:
    return os.fsdecode(raw)


def _check(pattern: re.Pattern, value: bytes, what: str) -> None:
    if not pattern.match(value):
        raise StatusParseError(f"invalid {what}: {value!r}")


def git_version(git: str = "git", runner=subprocess.run) -> tuple[int, int]:
    done = runner([git, "--version"], capture_output=True)
    if done.returncode != 0:
        raise GitStatusError(f"git --version exited {done.returncode}")
    match = re.search(rb"(\d+)\.(\d+)", done.stdout)
    if match is None:
        raise GitStatusError(f"unrecognised git version output: {done.stdout!r}")
    return int(match.group(1)), int(match.group(2))


def run_git_status(worktree, git: str = "git", runner=subprocess.run, renames: bool = False) -> bytes:
    """Return the raw status bytes. `renames=True` exists only for the rename-matrix tests."""

    args = list(STATUS_ARGS)
    if renames:
        args[args.index("--no-renames")] = "--renames"
    try:
        done = runner([git, "-C", str(worktree), *args], capture_output=True)
    except OSError as exc:
        raise GitStatusError(f"git could not be executed: {exc}") from exc
    if done.returncode != 0:
        raise GitStatusError(f"git status exited {done.returncode}: {done.stderr!r}")
    if not isinstance(done.stdout, bytes):
        raise GitStatusError("git status output was not captured as bytes")
    return done.stdout


def split_records(raw: bytes) -> list[bytes]:
    """Split NUL-terminated output into record tokens. Truncation is an error."""

    if not isinstance(raw, bytes):
        raise StatusParseError("status output must be bytes")
    if raw == b"":
        return []
    if not raw.endswith(b"\0"):
        raise StatusParseError("status output is not NUL-terminated (truncated)")
    tokens = raw[:-1].split(b"\0")
    if any(token == b"" for token in tokens):
        raise StatusParseError("empty record inside status output")
    return tokens


def _parse_ordinary(token: bytes) -> Record:
    parts = token.split(b" ", 8)
    if len(parts) != 9:
        raise StatusParseError(f"ordinary record has {len(parts)} fields, expected 9: {token!r}")
    path = parts[8]
    if path == b"":
        raise StatusParseError(f"ordinary record has an empty path: {token!r}")
    _, xy, sub, mode_head, mode_index, mode_worktree, oid_head, oid_index = parts[:8]
    _check(_XY, xy, "XY")
    _check(_SUB, sub, "submodule state")
    for mode in (mode_head, mode_index, mode_worktree):
        _check(_MODE, mode, "mode")
    for oid in (oid_head, oid_index):
        _check(_OID, oid, "object name")
    fields = tuple(part.decode("ascii") for part in parts[1:8])
    return Record("1", _decode(path), xy.decode("ascii"), None, fields)


def _parse_rename(token: bytes, orig: bytes | None) -> Record:
    parts = token.split(b" ", 9)
    if len(parts) != 10:
        raise StatusParseError(f"rename record has {len(parts)} fields, expected 10: {token!r}")
    path = parts[9]
    if path == b"":
        raise StatusParseError(f"rename record has an empty path: {token!r}")
    _, xy, sub, mode_head, mode_index, mode_worktree, oid_head, oid_index, score = parts[:9]
    _check(_XY, xy, "XY")
    _check(_SUB, sub, "submodule state")
    for mode in (mode_head, mode_index, mode_worktree):
        _check(_MODE, mode, "mode")
    for oid in (oid_head, oid_index):
        _check(_OID, oid, "object name")
    _check(_SCORE, score, "rename score")
    if orig is None:
        raise StatusParseError(f"rename record has no original-path token: {token!r}")
    fields = tuple(part.decode("ascii") for part in parts[1:9])
    return Record("2", _decode(path), xy.decode("ascii"), _decode(orig), fields)


def _parse_unmerged(token: bytes) -> Record:
    parts = token.split(b" ", 10)
    if len(parts) != 11:
        raise StatusParseError(f"unmerged record has {len(parts)} fields, expected 11: {token!r}")
    path = parts[10]
    if path == b"":
        raise StatusParseError(f"unmerged record has an empty path: {token!r}")
    _, xy, sub, mode_1, mode_2, mode_3, mode_worktree, oid_1, oid_2, oid_3 = parts[:10]
    _check(_XY, xy, "XY")
    _check(_SUB, sub, "submodule state")
    for mode in (mode_1, mode_2, mode_3, mode_worktree):
        _check(_MODE, mode, "mode")
    for oid in (oid_1, oid_2, oid_3):
        _check(_OID, oid, "object name")
    fields = tuple(part.decode("ascii") for part in parts[1:10])
    return Record("u", _decode(path), xy.decode("ascii"), None, fields)


def _parse_untracked(token: bytes) -> Record:
    path = token[2:]
    if path == b"":
        raise StatusParseError("untracked record has an empty path")
    return Record("?", _decode(path))


def _parse_ignored(token: bytes) -> Record:
    path = token[2:]
    if path == b"":
        raise StatusParseError("ignored record has an empty path")
    return Record("!", _decode(path))


def parse_records(tokens: list[bytes]) -> list[Record]:
    """Parse record tokens. An unrecognised record type is an error, never skipped."""

    records: list[Record] = []
    index = 0
    while index < len(tokens):
        token = tokens[index]
        head = token[:2]
        step = 1
        if head == b"1 ":
            records.append(_parse_ordinary(token))
        elif head == b"2 ":
            orig = tokens[index + 1] if index + 1 < len(tokens) else None
            records.append(_parse_rename(token, orig))
            step = 2
        elif head == b"u ":
            records.append(_parse_unmerged(token))
        elif head == b"? ":
            records.append(_parse_untracked(token))
        elif head == b"! ":
            records.append(_parse_ignored(token))
        else:
            raise StatusParseError(f"unrecognised status record type: {token[:32]!r}")
        index += step
    return records


def _is_allowed(record: Record, allow_list: frozenset) -> bool:
    return record.kind == "1" and record.xy == ".M" and record.path in allow_list


def classify(records: list[Record], allow_list, pre_ignored=frozenset()) -> Verdict:
    """Exact allow-list classification. Only a type-1 `.M` record on an allow-listed path
    is allowed; ignored paths absent from `pre_ignored` are reported as new."""

    allow = frozenset(allow_list)
    pre = frozenset(pre_ignored)
    allowed: list[str] = []
    outside: list[str] = []
    ignored_new: list[str] = []
    for record in records:
        if record.kind == "!":
            if record.path not in pre:
                ignored_new.append(record.path)
            continue
        if _is_allowed(record, allow):
            allowed.append(record.path)
        else:
            outside.append(record.describe())
    return Verdict(
        clean=not outside and not ignored_new,
        allowed=tuple(allowed),
        outside=tuple(outside),
        ignored_new=tuple(ignored_new),
    )


def status_verdict(worktree, allow_list, pre_ignored=frozenset(), git: str = "git",
                   runner=subprocess.run) -> Verdict:
    """Run, parse and classify. Raises GitStatusError or StatusParseError; never a
    clean verdict on failure."""

    return classify(parse_records(split_records(run_git_status(worktree, git, runner))),
                    allow_list, pre_ignored)


def ignored_paths(worktree, git: str = "git", runner=subprocess.run) -> frozenset:
    """The current set of ignored paths, for the pre-run ignored baseline."""

    records = parse_records(split_records(run_git_status(worktree, git, runner)))
    return frozenset(record.path for record in records if record.kind == "!")
