<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | PROPOSED, C0 RESEARCH. Specification only. No implementation is authorised by this document. Pending owner ratification (docs/OPEN_QUESTIONS.md Q1). |
| Version | 1.0.0 |
| Owner | TBD (see docs/OPEN_QUESTIONS.md Q1) |
| Last updated | 2026-08-11 |
| Review cadence | TBD |

# H3. Question Engine

## 1. Purpose

The question engine turns what a user asks into a structured, resolvable object that names the
domain, the timeframe, the question type, and what evidence would answer it. It is the entry point
of the analytical pipeline.

## 2. Relationship to the existing HLKG substrate

The repository already contains substantial drafted material for this layer: a canonical question
schema, question and domain registry specifications, and a career-domain corpus with a question
library, alias registry, event and outcome registries, a relationship graph and a conformance
dataset. It was drafted, removed, and restored blob-identical, and it has never been consumed by any
code.

This specification does not replace that work. It cannot responsibly reconcile with it either, until
DP-005 settles where knowledge lives and whether `engine/` may read it at runtime. Three architecture
documents currently place the knowledge layer in three incompatible positions, and the only one
marked LOCKED is the only one that puts prediction and interpretation inside knowledge, which every
other document forbids.

**H3 is therefore blocked on DP-005 and should not proceed past this document until it is answered.**

## 3. What a resolved question must carry

The raw text as asked, preserved verbatim. The resolved domain. The question type: whether a thing
will happen, when it will happen, whether a past thing did happen, or a comparison between options.
The timeframe, which may be open. The subject and the birth record it resolves against. The
evidence classes that would answer it, which is what lets the inference layer plan. And an explicit
record of anything the engine could not resolve, because a question the system half-understood is
more dangerous than one it refused.

## 4. Boundaries

The question engine MUST NOT answer. It resolves and structures. Any drift toward answering
collapses the layer separation the charter requires.

It MUST NOT invent a domain. An unrecognised question is an unresolved question, and the honest
output is a refusal plus what was missing.

The eventual LLM role here is parsing and disambiguation against a registry, never rule invention.

## 5. Open questions requiring an owner decision

DP-005 in full. The relationship between the drafted HLKG question identifiers and any new family.
Whether the career corpus is the pilot domain or whether a smaller domain is a better first target.

## 6. Verification strategy

Round-trip on the existing conformance dataset once its status is settled. Refusal coverage for
unresolvable questions. A negative test proving the engine produces no answer content.

## 7. Change history

| Version | Date | Change |
|---|---|---|
| 1.0.0 | 2026-08-11 | Created in the G1 work package as Phase H preparation. Blocked on DP-005. |
