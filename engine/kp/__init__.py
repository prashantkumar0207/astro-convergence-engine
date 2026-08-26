"""
KP (Krishnamurti Paddhati) layer.

Isolated per the school-separation rule: nothing here is imported by
Parashari, Varga, or Tier-0 modules, and nothing here mutates them.
The KP layer consumes AstronomySnapshot facts computed EXPLICITLY
under the ratified KP_KRISHNAMURTI profile.

Scope: KP_CHAIN_V1 (ADR-0006) - the exact-rational lordship chain
(sign lord SL, nakshatra/star lord NL, sub lord SB, sub-sub lord SS)
and KP chart assembly. KP_SIGNIFICATOR_V1 (ADR-0078) - a single,
narrow, frozen judgment (does the 7th cusp's own sub-lord signify the
marriage-promise houses 2/7/11 or the marriage-denial houses
1/6/10/12) - is also in scope, per its own certification-execution
record in docs/DECISION_LOG.md. Four-step theory, ruling planets,
horary judgment, general significators beyond that one frozen
judgment, and dashas remain OUT of scope and do not exist here.
"""
