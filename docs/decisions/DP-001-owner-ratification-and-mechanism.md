<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-17 |
| Review cadence | TBD |

# DP-001. Named owners and the ratification mechanism

## 1. The question

`docs/decisions/README.md`'s index describes this paper's question as "Q1 named owners and the
ratification mechanism," blocking "every status header; ratification of all PROPOSED ADRs." It has
carried the status **RESERVED, not drafted** since the paper series was created.

Two distinct things are bundled under that one heading, and this paper's first job is to separate
them, because they have different answers:

1. **Named owners.** Who holds the docs-owner, engine-owner and release-owner roles named in Q1
   (`docs/OPEN_QUESTIONS.md`)?
2. **The ratification mechanism.** What, formally, counts as a valid owner ratification of a
   `DECISION_LOG.md` entry - what evidentiary form must it take for a builder to record an entry as
   Accepted?

**This paper decides neither.** It presents what has already happened, in fact, against each
question, and the options for closing the gap between fact and formal record.

## 2. What has already happened, stated as fact

**`ADR-0033` Decision 1 (2026-08-13, ACCEPTED)** named:

| Role | Holder |
|---|---|
| Project Owner, final ratifying authority | Prashant Kumar |
| Builder, researcher, executor | Claude |
| Independent CEO and technical auditor | ChatGPT |

It also ratified, as text: "the repository is the authoritative permanent project record"; "conversation
is input material only and is never permanent authority... it becomes authority only because it is
written here"; and "significant phase work MUST NOT be merged to main without CEO audit and owner
authorisation."

**`docs/OPEN_QUESTIONS.md` Q1's own row records this as "RATIFIED IN PART"**: the Project Owner, Builder
and Independent auditor roles are named; the **docs owner, engine owner and release owner roles were
not designated and remain OPEN** - Q1's own text is explicit that these "are not invented."

**The ratification mechanism has not been separately, formally defined anywhere**, but a consistent
practice has accumulated since `ADR-0033`: an entry is recorded Accepted when the owner supplies an
explicit ratification instruction in conversation, which becomes authority only by being written into
`docs/DECISION_LOG.md` (`ADR-0033`'s own self-referential statement of the rule). Twenty-five entries
have since been Accepted this way (`ADR-0001`, `ADR-0002`, `ADR-0005` through `ADR-0012`, `ADR-0033`
through `ADR-0037`, `ADR-0039` through `ADR-0042`, `ADR-0044`, `ADR-0045`, `ADR-0046`, `ADR-0048`,
`ADR-0049`, `ADR-0050`), each citing the specific ratification instruction that authorised it.

**`docs/decisions/README.md`'s own index row for DP-001 says its answer blocks "ratification of all
PROPOSED ADRs."** That has not been literally true since `ADR-0033`: ratifications have proceeded
using the accumulated-practice mechanism above, without DP-001 ever being drafted or its question
formally closed. This is the central tension this paper exists to name.

## 3. Options

**Option A. Declare DP-001 fully answered by `ADR-0033` Decision 1 and the practice it established;
no further work needed.** Simplest. Its cost: it treats an *accumulated, undocumented practice* as
equivalent to a *formally defined mechanism*, which is exactly the "silently treat related documents
as equivalent to an ADR" failure mode this repository's own governance discipline exists to prevent.
It also does not close the still-open docs/engine/release-owner roles, which Q1's own row states
plainly remain open.

**Option B. Declare DP-001 answered IN PART: the "ratification mechanism" half is closed by citing
`ADR-0033` Decision 1 and the twenty-five-entry practice it produced as the operative precedent; the
"named owners" half stays explicitly open for the three undesignated roles.** Matches the actual
state of the repository exactly: one half has a ratified, cited, working answer; the other half does
not. Its cost: DP-001 remains formally open (not closed), which some readers may find unsatisfying
given how much has already happened under its shadow.

**Option C. Draft and ratify a dedicated, explicit "ratification mechanism" ADR** describing precisely
what evidentiary form a valid ratification instruction must take (e.g., must name the specific entry
or decision by identifier; must be attributable to the named Project Owner; must be written into the
register before it binds), rather than relying on an accumulated, never-written-down pattern. This
would resolve the discomfort felt in `docs/OPEN_QUESTIONS.md` Q13 (whether `ADR-0001`/`ADR-0002`'s
original "Accepted" status meant anything) from recurring for a future entry. Its cost: it is new
policy authorship, not a recording of what already exists, and risks re-litigating twenty-five already
-settled ratifications under a new test they were not measured against.

**Option D. Leave DP-001 fully RESERVED, undrafted in substance; treat this paper as a first pass only,
deferring every question to a later round.** Costs nothing now. Its risk: the gap between
`docs/decisions/README.md`'s literal text ("blocks ratification of all PROPOSED ADRs") and the
twenty-five ratifications that have already happened without it stays unexplained indefinitely.

## 4. Recommendation

**Option B, confidence MEDIUM.** It is the option that states what is actually true rather than either
manufacturing closure (Option A) or authoring new policy on the builder's own initiative (Option C,
which the owner may still want, but as its own decision, not a default). It also surfaces, rather than
buries, the one substantive remaining gap: the docs/engine/release-owner roles.

For that remaining gap, `docs/OPEN_QUESTIONS.md`'s own consolidated-batch item 1 (line 214) already
offers a builder recommendation, restated here rather than re-derived: name a docs owner, an engine
owner and a release owner, **or** state explicitly that the Project Owner holds all three for now -
"the second is a real answer and closes the question" (op. cit.). This paper does not choose between
them; it notes the existing recommendation is still on the table and unactioned.

## 5. What the decision must also settle, whichever option is chosen

Whether `docs/decisions/README.md`'s DP-001 index row is edited to match whichever disposition is
chosen (its "Blocks" column currently overstates the paper's practical effect, per Section 2 above).
Whether Option C's dedicated mechanism ADR, if wanted, should be scoped now or deferred as its own
future item. Whether the docs/engine/release-owner roles are named individually or collapsed onto the
Project Owner, and if named individually, who holds each.

## 6. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-17 | Drafted on owner direction ("CEO GOVERNANCE AUTHORIZATION - COMPLETE REMAINING PHASE G EXIT WORK"). Presents options; decides nothing. |
