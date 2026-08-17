"""PreToolUse hook: blocks the clearest destructive/unsafe git operations.

Bounded, session-local backstop for .claude/rules/git-safety.md. It only sees Bash commands run
through this Claude Code session's Bash tool - it is not a substitute for GitHub branch protection
(main currently has none) or for human judgment.

Contract: reads the PreToolUse JSON payload on stdin. Exit 0 = allow. Exit 2 with a message on stderr =
block, and Claude is shown the message. Any other exception is swallowed and treated as allow, so a bug
here fails open rather than blocking all Bash use.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

# Matches a heredoc body: `<<'EOF' ... \nEOF` / `<<EOF ... \nEOF` / `<<-EOF ... \nEOF`, DOTALL so it
# spans lines. Strips the body text (e.g. a commit message) so words like "--no-verify" *mentioned*
# in a message don't look like a flag *passed* on the command line.
_HEREDOC_RE = re.compile(r"<<-?\s*['\"]?(\w+)['\"]?.*?\n\1\b", re.DOTALL)
# Matches a double- or single-quoted string body (non-greedy, allows escaped quotes), so flag-shaped
# text inside `-m "..."` or similar is stripped the same way.
_DQUOTE_RE = re.compile(r'"(?:[^"\\]|\\.)*"')
_SQUOTE_RE = re.compile(r"'(?:[^'\\]|\\.)*'")


def _sanitize(command: str) -> str:
    """Strip heredoc bodies and quoted-string contents so only real shell tokens are scanned."""

    sanitized = _HEREDOC_RE.sub(" ", command)
    sanitized = _DQUOTE_RE.sub('""', sanitized)
    sanitized = _SQUOTE_RE.sub("''", sanitized)
    return sanitized


def current_branch() -> str:
    try:
        result = subprocess.run(
            ["git", "branch", "--show-current"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def blocked_reason(raw_command: str) -> str | None:
    if "git" not in raw_command:
        return None

    command = _sanitize(raw_command)
    if "git" not in command:
        # Every "git" mention was inside a heredoc/quoted string (e.g. a commit message
        # describing a git command) - nothing was actually invoked.
        return None

    if re.search(r"--no-verify|--no-gpg-sign", command):
        return "--no-verify / --no-gpg-sign bypasses hooks or commit signing."

    if re.search(r"\bgit\b.*\bpush\b.*(--force-with-lease\b|--force\b|(?<!\S)-f(?!\S))", command):
        return "force-push (--force / -f / --force-with-lease) can overwrite remote history."

    if re.search(r"\bgit\b.*\breset\b.*--hard\b", command):
        return "git reset --hard discards uncommitted work irreversibly."

    if re.search(r"\bgit\b.*\bclean\b.*-[a-zA-Z]*f", command):
        return "git clean -f (any variant) irreversibly deletes untracked files."

    if re.search(r"\bgit\b.*\bbranch\b.*(-D\b|--delete\s+--force\b)", command):
        return "git branch -D force-deletes a branch, discarding unmerged commits."

    if re.search(r"\bgit\b.*\bpush\b", command):
        if re.search(r"\bmain\b", command):
            return "direct push targeting 'main' requires explicit owner authorization."
        if current_branch() == "main" and not re.search(r":\s*\S+\s*$", command.strip()):
            return "pushing while checked out on 'main' with no explicit non-main refspec."

    if re.search(r"\bgit\b.*\bmerge\b", command) and current_branch() == "main":
        return "merging while checked out on 'main' requires explicit owner authorization."

    if re.search(r"\bgit\b.*\bcommit\b", command) and current_branch() == "main":
        return "committing directly on 'main' requires explicit owner authorization."

    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0

    if payload.get("hook_event_name") != "PreToolUse":
        return 0
    if payload.get("tool_name") != "Bash":
        return 0

    command = (payload.get("tool_input") or {}).get("command") or ""
    if not command.strip():
        return 0

    try:
        reason = blocked_reason(command)
    except Exception:
        return 0

    if reason:
        sys.stderr.write(
            "BLOCKED by .claude/hooks/git_safety_guard.py (see .claude/rules/git-safety.md):\n"
            f"  {reason}\n"
            f"  command: {command}\n"
            "If this is genuinely intended, ask the user to confirm explicitly, then run it "
            "outside this guard's blocked patterns or have the user run it directly.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
