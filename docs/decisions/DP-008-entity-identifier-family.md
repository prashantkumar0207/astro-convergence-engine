<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | OPEN - decision paper. Presents options and recommends one. DECIDES NOTHING. Requires owner approval before any identifier format is used. |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# DP-008. Entity identifier family and pattern

## 1. The question

`docs/H0_ENTITY_MODEL_SPEC.md` requires every astrological entity to carry a stable identifier from a
declared family. The family and its pattern are undecided, and ADR-0021 D3 keeps the entity-kind
vocabulary deliberately extensible, which interacts with the choice.

**This paper decides nothing.** The format must not be invented or locked without owner approval.

## 2. Why it cannot be deferred much longer

`docs/NAMING_STANDARD.md` s2 requires that any new identifier family have a governing section, a
decision-log entry, and a uniqueness check **before first use**. ADR-0004 exists because ten
identifiers were minted without those three steps, and ADR-0014 exists because completing that
correction was itself left half-done. The entity family is the next identifier family the project
will need, and it is the first opportunity to follow the rule rather than repair it afterwards.

## 3. A constraint that eliminates one otherwise attractive option

`docs/NAMING_STANDARD.md` s2 states, for all families with no exceptions, that identifiers are
**zero-padded, monotone, immutable, never reused**.

A UUID or ULID satisfies immutable and never-reused but **violates monotone and zero-padded**. UUIDv4
is not ordered at all; ULID is time-ordered but not zero-padded decimal. Choosing either therefore
requires amending NAMING_STANDARD s2, which is a decision in its own right and should be made
knowingly rather than discovered during implementation.

## 4. A constraint that eliminates the most readable option

A kind-prefixed identifier, for example `PER-000001` for a person and `ORG-000001` for an
organisation, reads well and sorts usefully. It has two defects that interact badly with decisions
already taken.

**It conflicts with immutability.** If an entity's kind is corrected, say a body first recorded as an
Organisation is properly a Geographic entity, its identifier must either change, violating
immutability, or lie permanently. Misclassification at intake is not hypothetical for mundane
entities.

**It conflicts with D3's extensibility.** Every new entity kind needs a new prefix, so the prefix set
is a second vocabulary to govern alongside the kind vocabulary, and the two can drift.

Encoding a mutable attribute into an immutable identifier is the general defect here, and kind is
mutable by correction even if it is stable in practice.

## 5. Options

**Option A. Flat sequential, kind-neutral.** `ENT-000001`, six digits, issued by a declared issuer.
Satisfies NAMING_STANDARD s2 exactly as written. Kind lives in a field, not in the identifier, so
correction is a field update. Requires a single issuer, which is trivial while the system is
centralised and becomes a coordination point if it ever is not. Six digits caps at one million
entities, which is ample for persons and organisations and worth a second thought only if market or
event entities are ever ingested in bulk.

**Option B. Flat sequential, wider.** `ENT-00000001`, eight digits. Identical to A with more headroom.
The cost is purely cosmetic. Worth stating because widening later is not possible without violating
zero-padding consistency.

**Option C. Kind-prefixed sequential.** `PER-000001`, `ORG-000001`, `GEO-000001`, `EVT-000001`,
`QST-000001`. Most readable, and defective for the two reasons in section 4. Presented because
readability in logs and support conversations is a real benefit and the owner may weigh it
differently.

**Option D. Opaque identifier, ULID or UUIDv7.** No issuer, no coordination, safe under any future
distribution, and time-sortable in the v7 and ULID cases. Requires amending NAMING_STANDARD s2.
Unreadable in conversation, which matters more than it sounds for a system whose outputs are meant to
be explained to users.

**Option E. Defer.** Legitimate only while nothing needs an identifier. Since H0 is specification-only
and no implementation is authorised, deferral costs nothing today. It costs a great deal on the first
day of implementation, because that is exactly when the pressure to invent one arrives.

## 6. Recommendation

**Option B, `ENT-00000001`, eight digits, kind-neutral.** Confidence: medium-high.

It satisfies NAMING_STANDARD s2 as written with no amendment. It keeps the mutable attribute out of
the immutable identifier. It gives headroom that costs nothing now and cannot be added later. Readability
is adequate: `ENT-00000042` is speakable, and the kind is one field lookup away.

I recommend against Option D despite its engineering appeal, because the readability loss is real for a
product whose value proposition is explanation, and because amending a standard to fit an implementation
choice is the pattern this project has spent Phase G correcting.

## 7. What the decision must also settle

The issuer, meaning which component allocates the next number and where the counter lives. Whether
identifiers are allocated at intake or at first persistence. Whether a test or fixture range is
reserved, which is cheap now and awkward later. And whether the same family covers all five entity
kinds or whether questions, being ephemeral in Prashna, get their own family.

## 8. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Drafted on CEO direction. Presents options; decides nothing. |
