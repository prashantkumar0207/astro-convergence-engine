"""INTERPRETATION, work package WP-I1 (ADR-0133; PROPOSED, not ratified).

Rule application on synthetic charts only, producing in-memory application records, never evidence (ADR-0133 D6):

- conditions.py   closed evaluation of a rule's conditions from PARASHARI_HOUSE_LORD_V1's certified facts (I2);
- application.py  every variant of one published synthetic Parashari rule version applied to one synthetic chart,
                  with refusals and a content hash on every record (I3, I4, I6, I7, I8, I9);
- explanation.py  deterministic sentences rendered from a record verified against the chart it came from and the
                  pinned registry, with no text input of any kind (I5).

Nothing here persists anything, reads the ledger, an event, an answer or the evidence store, issues a prediction,
computes confidence, or contains an LLM client. Every genuine rule is refused (ADR-0132 s4; ADR-0133 D2 inactive).
"""
