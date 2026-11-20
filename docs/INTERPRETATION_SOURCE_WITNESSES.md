<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **PROPOSED. A record of candidate source witnesses only (`ADR-0130` s3).** Nothing here authorizes publication of any rule. |
| Version | 0.1.0 |
| Owner | Project Owner (`ADR-0051` D4) |
| Last updated | 2026-11-19 |
| Review cadence | On any change to a witness, a locator or a rights decision |

# INTERPRETATION source witnesses

This records where candidate source material for the first genuine rules might come from, what has and has not been checked, and
what blocks publication. It holds provenance and locators only. **It copies no source text.**

## 1. Candidate witness W1

| Field | Recorded |
|---|---|
| Work | Brihat Parashara Hora Shastra (BPHS), Volume I |
| Edition | Girish Chand Sharma, Sagar Publications, 1994 (reprint 1998) |
| Passage | The placements of the lord of the 10th house in each of the 12 houses, verses 109 to 120 |
| Locator, as reported | Printed pages 325 to 329; PDF pages 333 to 337 of the owner's copy |
| School and domain it would serve | `ProducingSystem.PARASHARI`, `Domain.JATAKA` |
| Verified by Claude | **No.** The copy is in the owner's Google Drive Books folder. The Drive connected to this session is a different account, and neither a title nor a full-text search found it. The locator above is the CEO's report, not checked. |

## 2. Cross-witnesses consulted, and what they showed

| Witness | What was checked | Limit |
|---|---|---|
| X1: enjoylearningsanskrit.com, BPHS chapter 24 | The Sanskrit of verses 109 to 113 (the 10th lord in houses 1 to 5) was read verse by verse, one house per verse | The site names no edition, states "All rights reserved", and verses 114 to 120 were not read. Usable as a cross-check only. |
| X2: Brihat Jataka of Varahamihira, tr. N. Chidambaram Iyer, Madras, Foster Press, 1885 (Wellcome Collection `afmgm695`) | Title, imprint and rights read from the record | Public Domain Mark. It is not BPHS. |

Chapter and verse numbering differs between BPHS editions, so every locator must name its edition.

## 3. Blockers to publishing any genuine rule

| # | Blocker | Who resolves it |
|---|---|---|
| B1 | The rights basis for the chosen edition. W1 is a modern translation, presumed in copyright: verbatim quotation needs a licence, or the rule must cite it without quoting. | The owner |
| B2 | A witness scan pinned by its SHA-256, as an authorized source requires. | The owner, who holds the copy |
| B3 | The locators of verses 109 to 120 read directly in W1. | Claude, once the copy is reachable |
| B4 | A named independent verifier, who is not Claude, and their transcription. | The owner |
| B5 | The rule count: 5 rules (verses 109 to 113) or 12 (verses 109 to 120). | The owner |
