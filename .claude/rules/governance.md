# Governance rules

Full detail: `docs/PROJECT_CONSTITUTION.md`, `docs/DECISION_LOG.md`, `docs/OPEN_QUESTIONS.md`,
`docs/decisions/README.md`, `docs/NAMING_STANDARD.md` s2, `docs/DOCUMENTATION_STANDARD.md`.

- **Decisions live in `docs/DECISION_LOG.md` as four-digit, zero-padded `ADR` entries (for example
  `ADR-0044`), issued by the owner.** A decision paper (`docs/decisions/DP-NNN-*.md`) presents options
  and a labelled recommendation; it decides nothing, however confident the recommendation. Do not act
  on a `DP-NNN` paper's recommendation as if it were approved - wait for a decision entry or explicit
  owner instruction, and then record that instruction as a decision entry yourself if none exists yet.
- **Status vocabulary matters.** `DRAFT` / `PROPOSED` / `OPEN` = not binding. `ACCEPTED` = owner-ratified.
  Never present a `DRAFT` document's content as settled; cite its actual status.
- **Ratification is per-entry, not per-register.** An owner existing, or having ratified some entries,
  does not mean the whole register is ratified. Check the specific entry.
- **Before editing `docs/DECISION_LOG.md`**: get the next free ADR number from
  `python scripts/check_adr_numbering.py` (gaps are legal - some numbers are reserved). Append the new
  entry in ascending numeric order (ADR-0029 established the register is ordered by identifier, not by
  append time). Give it a status header matching `docs/DOCUMENTATION_STANDARD.md` s2 and cite real
  evidence (commit SHAs, CI run IDs, command output), not assertions.
- **Before introducing a new decision-paper (`DP-NNN`)**: register it in `docs/decisions/README.md`'s
  index first (before drafting), per ADR-0040. `python scripts/check_identifier_families.py` verifies
  every `DP-\d{3}` token in the tracked tree is registered.
- **Never edit an existing, already-recorded decision entry to change its substance.** If a prior entry
  is wrong or stale, record that in a new entry - the append-only history is the evidence trail.
- **Never invent an ADR number, a ratification, or an owner decision.** If something looks decided but
  you cannot find the decision entry recording it, treat it as undecided and say so.
