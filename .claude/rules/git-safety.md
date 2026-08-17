# Git safety rules

- **Never force-push** (`--force`, `-f`, or `--force-with-lease`) without the user explicitly
  confirming it in this conversation for that specific push.
- **Never run `git reset --hard`, `git clean -f` (any variant), or `git branch -D`** without explicit
  confirmation - each discards work that may not be recoverable.
- **Never push to, merge into, or commit directly on `main`** without explicit owner authorization for
  that specific action. Work happens on branches; `main` is CEO/owner territory.
- **Never use `--no-verify` or `--no-gpg-sign`** - these bypass hooks and signing, which exist for a
  reason.
- **Always create new commits rather than amending**, unless explicitly asked to amend. Amending after
  a failed pre-commit hook rewrites the wrong commit.
- **Run `git status` before any command that could discard uncommitted work**
  (`checkout`/`restore`/`reset`/`clean`), and check whether what's there is deliberate in-progress work
  before touching it.
- **A `PreToolUse` hook (`.claude/hooks/git_safety_guard.py`) mechanically blocks the clearest cases of
  the above** (force-push, `reset --hard`, `clean -f`, `branch -D`, direct push/merge to `main`,
  `--no-verify`/`--no-gpg-sign`) for `Bash` commands in this session. Treat it as a backstop, not the
  actual control - it only covers this tool, this session, this host. `main` currently has **no**
  GitHub branch-protection rule (confirmed in `reports/AI_COLLABORATION_INSPECTION.md` s2.7); nothing
  server-side stops a force-push or direct push by any other client.
- **Pushing is a shared-visibility action.** Even for a non-`main` branch, confirm with the user before
  pushing unless they've already asked for it in this conversation.
