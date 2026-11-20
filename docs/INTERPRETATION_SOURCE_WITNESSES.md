<!--
Document status header - keep current on every edit.
-->
| Field | Value |
|---|---|
| Status | **PROPOSED. A record of candidate source witnesses only (`ADR-0130` s3).** Nothing here authorizes publication of any rule. |
| Version | 0.2.0 |
| Owner | Project Owner (`ADR-0051` D4) |
| Last updated | 2026-11-20 |
| Review cadence | On any change to a witness, a locator or a rights decision |

# INTERPRETATION source witnesses

This records where source material for the first genuine rules comes from, what has and has not been checked, and what blocks
publication. It holds provenance, locators and hashes only. **It copies no source text, Sanskrit or English.**

Everything marked "read by Claude" below was read directly from the pinned file. Claude's reading is not independent
verification (`ADR-0130` s2.1; B4).

## 1. Witness W1: the Sharma edition, Volume I

| Field | Recorded | How established |
|---|---|---|
| Title page (PDF page 1) | *Maharshi Parasara's Brihat Parasara Hora Sastra*, Vol. I. Translation, commentary and annotation by Girish Chand Sharma. Sagar Publications, New Delhi | Read by Claude |
| Imprint (PDF page 2) | "© Publishers". First published 1994; reprinted 1995; reprint 1999. Published by Narinder Sagar for Sagar Publications | Read by Claude. This corrects the earlier "1994 (reprint 1998)". |
| The owner's copy | A PDF in the owner's Google Drive Books folder (`Brihat.pdf`), 20,110,607 bytes, 657 PDF pages. Its Drive link is deliberately not recorded here: this repository is public, and the link opens a copyrighted book. | Downloaded through the owner's link on 2026-11-20 |
| **Witness SHA-256** | `3c63c1a22d5fec46624dd0f865e4cf35c2ac63e61b84485622f81b4a8175c3af` | Computed from the download |
| Other digests | MD5 `2d37b3221c64b27251628644ff7664bd`; SHA-1 `58b8beb331e72a411cdc61ac7f6934c24b3103f1` | Computed |
| Provenance of the copy | Byte-identical to Internet Archive item `brihatparasarahorasastrawithenglishtranslationgirishchandsharmavolume1_547_G` (collections `digitallibraryindia`, `JaiGyan`), whose published MD5 and SHA-1 match. The PDF's own metadata names Internet Archive as its producer (2025-08-26) | Both files hashed and compared byte for byte |
| Chapter | **Chapter 26**, "Effects of the Bhava Lords" (Sanskrit colophon heading numbered 26), opening on printed page 275 (PDF page 283) | Read by Claude on the chapter's opening page. The contents page swaps the titles of chapters 26 and 27; its descriptions and page numbers are right. |
| Page offset | PDF page = printed page + 8 | Checked at printed pages 275, 325, 326, 327, 329 and 341 |
| Layers on each page | (a) the Sanskrit verse with its number; (b) Sharma's English translation; (c) Sharma's notes, for most verses, including example charts of named real people (printed page 327) | Read by Claude. Layer (c) is never used: ACE records are synthetic. |

### 1.1 Verified locators: the lord of the 10th house in houses 1 to 5

| Verse | The 10th lord placed in | Printed page | PDF page | Locator, in the registry's format |
|---|---|---|---|---|
| 109 | the 1st house | 325 | 333 | `chapter 26, verse 109, page 325` |
| 110 | the 2nd house | 325 (its translation ends, and its notes run, on 326) | 333 | `chapter 26, verse 110, page 325` |
| 111 | the 3rd house | 326 | 334 | `chapter 26, verse 111, page 326` |
| 112 | the 4th house | 326 | 334 | `chapter 26, verse 112, page 326` |
| 113 | the 5th house | 326 (its notes run on to 327) | 334 | `chapter 26, verse 113, page 326` |

Read by Claude, verse number and house in each. Verses 118 to 120 (the 10th lord in the 10th to 12th houses) were read on printed page
329, so the whole sequence of verses 109 to 120 lies on printed pages 325 to 329 (PDF pages 333 to 337), as the CEO reported. Verses 114
to 117 were not read and are outside the authorized five.

## 2. Other witnesses

| Witness | What was checked | Limit |
|---|---|---|
| X1: enjoylearningsanskrit.com, BPHS chapter 24 | The Sanskrit of verses 109 to 113, one house per verse | Numbers this chapter 24; W1 numbers it 26. The verse numbers agree. No edition named; "All rights reserved". A cross-check only. |
| X2: Brihat Jataka of Varahamihira, tr. N. Chidambaram Iyer, Madras, 1885 (Wellcome Collection `afmgm695`) | Title, imprint and rights read from the record | Public Domain Mark. It is not BPHS. |
| W1 Volume II and the Books folder, in the owner's Drive | **Not accessible.** Both redirect to Google sign-in, and the Drive connected to this session (another account) reports them not found | An account-permission restriction. Not needed for verses 109 to 113. |
| Earlier printed Sanskrit editions on the Internet Archive, including Bombay 1899 (Subodhini) and Khemraj 1923 | Listed by the archive's search only | Not opened, and not assessed for rights. Possible independent Sanskrit witnesses. |

Chapter and verse numbering differs between editions, so every locator names its edition.

## 3. Rights: what each layer is

| Layer | Status as recorded | Consequence for the repository |
|---|---|---|
| (a) The Sanskrit verses | A classical text, not the work of a modern author. Whether this edition's setting of it carries any edition right is not established here. | The owner decides (B1). |
| (b) Sharma's English translation | A modern translation; the imprint reads "© Publishers" (Sagar Publications), first published 1994 | Never reproduced or closely paraphrased in the repository. |
| (c) Sharma's notes | Modern commentary, same imprint | Never reproduced, and never a rule source. |
| The Internet Archive item's CC0 label | Applied by the uploader | **Not a rights basis.** It is not a licence from the rights holder. |

## 4. Blockers to publishing any genuine rule

| # | Blocker | State | Who resolves it |
|---|---|---|---|
| B1 | The rights basis: for example, rules stated in ACE's own words from the Sanskrit, citing W1 by locator and quoting nothing; or a licence from Sagar Publications; or a public-domain Sanskrit witness instead | **Open** | The owner |
| B2 | A witness pinned by its SHA-256 | **Hash recorded** (s1). The owner confirms W1, with this hash, as the witness | The owner |
| B3 | The locators of the passage read directly in W1 | **Read by Claude** for verses 109 to 113 (s1.1). Independent confirmation is part of B4. | Claude (done); the verifier |
| B4 | A named independent verifier, who is not Claude, who reads the verses at these locators and checks each rule's statement, locator, condition, domain and polarity, with their own transcription | **Open** | The owner |
| B5 | The rule count | **Five** (verses 109 to 113), as the owner's Stage 2 preparation authorization sets | Settled for preparation |
| B6 | Verse 109 states both favourable and adverse effects; a rule carries one polarity, with no mixed value | **Open**: one rule with one polarity, or one rule per effect | The owner, with the verifier |
| B7 | The criteria S2-1 to S2-3 cited in the owner's authorization are not defined in the repository | **Open**: their text is needed before the rules can be checked against them | The owner or the CEO |
