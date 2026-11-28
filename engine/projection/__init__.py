"""Projection of INTERPRETATION's application records into evidence (ADR-0134 WP-I2).

The one bounded exception to WP-I1's interpretation import allowlist (ADR-0133 I7; ADR-0134 s2): this package alone
writes untimed synthetic natal evidence, and it supplies the evidence store's natal verifier. engine/interpretation/ is
unchanged and still imports no evidence store.
"""
