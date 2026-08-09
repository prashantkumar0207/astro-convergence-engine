| Field | Value |
|---|---|
| Status | DRAFT - pending owner ratification |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | docs/HLKG_CONSTITUTION.md, docs/DOMAIN_REGISTRY_SPEC.md, docs/QUESTION_REGISTRY_SPEC.md, docs/CANONICAL_QUESTION_SCHEMA.md |
| Registry position | The `career` domain is **not yet ratified** (DQ-1). This model doubles as the DRAFT-state domain definition input required by Domain Registry lifecycle s.5/s.7: its Scope, Out-of-Scope and Boundary sections are written to be lifted verbatim into the domain record at ratification. |
| Repository path | knowledge/hlkg/domains/career/CAREER_DOMAIN_MODEL.md |

# Career Domain Knowledge Model

The authoritative conceptual model of the Career domain: what it means, what it contains,
where its edges are, and how its knowledge is organised - complete enough that a future
engineer can generate canonical Questions without ambiguity, without this document ever
generating them itself. No questions, no astrology, no prediction logic, no JSON.

---

## 1. Purpose

Within HLKG, **Career** is the domain of a person's productive working life: the sequence
of employments, ventures, professional practices, roles and work-derived standing through
which a person earns, contributes, advances and eventually exits working life.

The domain answers to one locus test (Domain Registry s.4): a Question belongs to Career
iff its **complete answer is about the subject's working life itself** - an employment,
venture, role, professional trajectory, work event or work-derived state - rather than
about the money, relationships, health, learning or places that surround it.

Career is expected to be among the highest-traffic domains; this model is therefore
deliberately over-explicit about boundaries.

## 2. Scope

Territories inside Career (positive enumeration; each bullet is testable against a sample
question):

- **Employment**: obtaining, holding, changing and losing jobs; first employment; re-employment.
- **Profession & vocation**: choice, fit and identity of one's line of work; professional practice (independent professionals included).
- **Business as venture**: starting, running, growing, pivoting, closing or selling a business the subject operates - the venture's fate as work.
- **Advancement**: promotion, seniority, grade, scope expansion, leadership attainment, authority.
- **Transitions**: job change, employer change, career change, industry change, career breaks and re-entry, second careers.
- **Workplace**: work environment, workplace relations, conflict with colleagues/superiors *as work matters*, organisational culture fit.
- **Performance & professional recognition**: appraisal outcomes, awards at/for work, professional reputation inside one's field.
- **Skills in professional application**: adequacy, use and demand of skills for work; upskilling driven by and evaluated against career outcomes.
- **Mobility & assignments**: transfers, deputations, secondments, foreign postings, onsite assignments - work-purposed relocation events.
- **Professional income as career outcome**: salary/compensation level, raises, earning growth *attached to employment or venture performance* (see boundary 4.1).
- **Career satisfaction**: contentment with one's working life as an appraisal of the career itself (see boundary 4.5).
- **Exit**: retirement timing and manner, career end, post-exit professional activity.

## 3. Out of Scope

Reciprocal pointers (Domain Registry s.3 requires the receiving domain to claim these at
its own ratification; reciprocity closure is tracked in CDQ-2):

| Excluded territory | Owning domain |
|---|---|
| Marriage, partnerships, romance (including workplace romance as a relationship) | `relationship` |
| Physical/mental health, burnout as a clinical state, stress disorders | `health` |
| Wealth, assets, investments, savings, debts, pensions as money matters, returns from business as invested capital | `finance` |
| Property acquisition/disposal (including office premises as assets) | `property` |
| Children, family duties, family members' own careers (subject-scope note: CDQ-4) | `family` |
| Learning outcomes: admission, study completion, examinations, degrees as attainment | `education` |
| Litigation, disputes as legal proceedings (including employment lawsuits as proceedings) | `legal` |
| Public fame and standing outside one's professional field | `reputation` |
| The journey/stay logistics of travel; permanent settlement decisions | `travel` / `residence` |
| Meaning-of-life, calling as spiritual matter | `inner_life` (boundary 4.6) |

## 4. Domain Boundaries (hard cases, written as binding boundary-note candidates)

**4.1 Business vs Finance.** The venture's operational fate - will it start, grow, survive,
close - is Career (the venture is the subject's work). Money outcomes of the venture -
profit level, wealth created, recovery of invested capital, funding - are Finance. Test:
if the complete answer describes the *venture as an activity*, Career; if it describes
*money*, Finance. "Will my business succeed?" is Career (QUALITY of the venture); "Will my
business make me wealthy?" is Finance.

**4.2 Education vs Career.** Acquiring the qualification (admission, completion, exam
result) is Education. The *career consequence* of a qualification - whether it yields the
job, the promotion, the professional standing - is Career. Test: answer about learning
attainment -> Education; answer about working-life effect -> Career.

**4.3 Foreign travel vs Foreign posting vs Emigration.** A work-purposed assignment
(posting, deputation, onsite) is Career - the event is an employment event. The trip/stay
as an experience with duration-bounded logistics is Travel. Open-ended settlement abroad
is Residence, even when triggered by work; the *posting* remains Career while the
*settlement* is Residence. (Consistent with the Domain Registry s.13 illustration.)

**4.4 Career failure vs Financial loss.** Losing the job, the venture folding, demotion:
Career. The monetary damage that follows: Finance. One user story, two Questions, linked
at node level - never one dual-domain node.

**4.5 Job satisfaction vs Mental health.** Satisfaction/dissatisfaction as an appraisal of
one's working life is Career (QUALITY class). Distress, anxiety, burnout as conditions of
the person are Health, even when work-caused. Test: is the answer about the career or
about the person's wellbeing? Causation does not transfer ownership (answer-locus rule:
motivation/cause never decides domain).

**4.6 Vocation vs Calling.** Vocational direction and professional identity ("which line
of work fits") is Career (SELECTION/DESCRIPTION). The spiritual/meaning dimension of a
calling is `inner_life`. Where a single user utterance mixes both, it is composite and
decomposes.

**4.7 Professional recognition vs Public reputation.** Standing *within one's field or
workplace* (awards, professional respect, appraisal) is Career; fame and standing in the
*general public* is Reputation. Test: who is the audience in a complete answer?

**4.8 Government/military rank and service matters.** Rank progression, postings,
disciplinary career effects are Career; court-martial or litigation as a proceeding is
Legal; pension corpus is Finance.

## 5. Subdomains

**Registry note:** per Domain Registry s.2.2 the classification space is FLAT - these
subdomains are *knowledge organisation only*. They are the controlled vocabulary from
which Question slug **topic segments** (segment 2) will be drawn, ensuring 50,000-scale
slug consistency; they are not registry domains and never classify nodes by themselves.

| Subdomain (slug topic) | Covers |
|---|---|
| `employment` | Jobs held/sought/lost; hiring; re-entry |
| `profession` | Line-of-work identity, professional practice, vocation fit |
| `business` | Owned/operated ventures as work (start, run, pivot, close, sell) |
| `advancement` | Promotion, seniority, grade, scope, leadership |
| `transition` | Job/career/industry change; breaks; second careers |
| `workplace` | Environment, relations, conflict-as-work-matter, culture fit |
| `performance` | Appraisals, targets, professional recognition and awards |
| `skill` | Professional adequacy, application and demand of skills |
| `assignment` | Transfers, deputations, secondments, foreign postings |
| `compensation` | Professional income as career outcome (boundary 4.1 applies) |
| `satisfaction` | Career contentment and fit (boundary 4.5 applies) |
| `exit` | Retirement, career end, post-exit professional activity |

Twelve topics; additions follow s.13. Aspect segments (segment 3) come from the Event and
Outcome taxonomies below plus the class-typical aspects (`timing`, `occurrence`,
`stability`, `direction`, ...).

## 6. Entity Model

Entities the domain's knowledge speaks about (conceptual, technology-free):

- **Person (Subject)** - whose career it is; always a query parameter, never data (QRS s.3).
- **Employment** - the relation Person<->Employer in a Role over time; the central unit of employed careers.
- **Employer / Organization** - party providing employment (company, government, institution, family enterprise).
- **Role / Position** - the function held; carries Title/Grade.
- **Business (Venture)** - an enterprise the subject owns/operates as work.
- **Profession** - the recognised line of work independent of any single employer.
- **Industry / Sector** - the field the work happens in.
- **Skill** - a capability in professional application.
- **Contract / Engagement** - the terms binding work (permanent, fixed, freelance, gig).
- **Compensation** - pay attached to Employment/Venture (career-outcome facet only; 4.1).
- **Assignment / Posting** - a bounded work-purposed placement (incl. foreign).
- **Workplace** - the working environment and its relations.
- **Recognition** - professional acknowledgement (award, appraisal outcome, field standing).
- **Career Path** - the ordered sequence of Employments/Ventures/Roles of one Person.
- **Career Break** - a bounded absence from working life.
- **Retirement** - the terminal transition out of working life (possibly reversible: 12.1).

Entity notes: Employment vs Role separation matters (role change without employer change
is a distinct event class); Business is an entity, not a subdomain synonym - one person
may hold several (12.2).

## 7. Event Taxonomy

Career events (things that happen), grouped; each is a candidate *aspect* vocabulary item.
No prediction semantics attach to any of them.

- **Entry**: first employment; workforce re-entry (after break/retirement).
- **Progression**: promotion; grade/seniority rise; scope expansion; leadership appointment; pay raise (as employment event).
- **Lateral**: role change (same employer); employer change (same profession); transfer; secondment; foreign posting; return from posting.
- **Reorientation**: profession change; industry change; employed<->self-employed switch.
- **Separation**: resignation; termination; layoff/retrenchment; contract end/non-renewal.
- **Venture**: business start; expansion; pivot; partnership formation/dissolution *in the venture*; closure; sale/exit.
- **Interruption**: career break start/end; sabbatical; suspension.
- **Recognition**: award; milestone; appraisal outcome; professional honour.
- **Adversity**: demotion; disciplinary action (as employment event); stagnation onset (state-entry treated as event for taxonomy completeness).
- **Exit**: retirement; voluntary early exit; career end; post-retirement engagement start.

## 8. Outcome Taxonomy

Career outcomes (states/trajectories a complete answer may assert), the vocabulary behind
QUALITY/DESCRIPTION answers and outcome-flavoured aspects:

- **Trajectory**: growth; decline; stability; stagnation; reinvention/change.
- **Attainment**: success/achievement (against declared goal); leadership/authority attained; recognition attained; seniority attained.
- **Timing-flavoured**: delay (of an expected event); acceleration; prematurity (e.g., early exit).
- **Security**: job security; insecurity; precarity.
- **Fit**: satisfaction; dissatisfaction; vocational fit/misfit.
- **Economic (career facet)**: income growth; income stagnation - always as compensation attached to work (4.1).

Outcomes are declared-scale material: any QUALITY Question over these MUST reference a
declared Rating scale (Answer Contract, QRS s.7); scale ratification is CDQ-5.

## 9. Question Categories

The seven constitutional classes applied to Career (categories only - zero inventory):

| Class | Career meaning | Shape reminder |
|---|---|---|
| TIMING | when a career event occurs (promotion, job change, business start, retirement...) | Timeline Object |
| OCCURRENCE | whether a career event occurs within a horizon (job loss, posting, re-employment...) | value+horizon |
| QUALITY | graded state of a career facet (stability, satisfaction, venture health, security...) | Rating vs declared scale |
| SELECTION | which of declared options fits (vocational direction, offer A vs B, employed vs venture...) | selection among bound options |
| QUANTITY | counts/magnitudes (number of employer changes, span of career break...) | number+unit+basis |
| DESCRIPTION | characterisation (nature of career path, style of professional life...) | Structured Narrative |
| CAUSAL | factors behind a career state (stagnation, repeated separations...) | factors+explanation |

Class discipline inherited: one class per Question; "will I get promoted and when?" is two
Questions (OCCURRENCE + TIMING), typically `RELATES_TO`/`REFINES`-linked.

## 10. Relationships

**Knowledge-level relations (this model, descriptive):**
- Entity-Entity: Person *holds* Employment; Employment *at* Employer *in* Role; Person *operates* Business; Role *requires* Skills; Employment *governed by* Contract.
- Event-Entity: every event *applies to* exactly one central entity (Promotion->Employment; Business start->Business; Posting->Assignment).
- Event-Event (characteristic ordering, not law): Entry precedes Progression; Separation precedes Re-entry; Venture start precedes Venture outcomes; Break start precedes Break end.
- Event-Outcome: events *evidence* outcomes (promotion evidences growth; repeated separation evidences precarity) - descriptive association only, never inference rules.
- Subdomain adjacency (indexes shared boundary notes): compensation<->`finance`; satisfaction<->`health`; skill<->`education`; assignment<->`travel`/`residence`; performance<->`reputation`; business<->`finance`/`legal`.

**Question-level mapping (when Questions are later generated):** knowledge orderings
surface only through the constitutional edge registry - e.g., first-employment-timing
`PRECEDES` promotion-timing; promotion-timing `DEPENDS_ON` employment-occurrence;
narrow foreign-posting-occurrence `REFINES` assignment-occurrence. No new edge types are
introduced or implied by this model.

## 11. Common User Language (intent evidence only - nothing canonicalised)

Natural phrasings future intake must resolve (en + illustrative hi-latin), grouped by the
category they signal:

- Timing: "When will I get a job?" - "When will I get promoted?" - "Naukri kab lagegi?" - "Promotion kab hoga?" - "When can I start my own business?" - "When will I retire?"
- Occurrence: "Will I lose my job?" - "Will I get the offer?" - "Is a foreign posting in my future?" - "Will my startup survive?" - "Will I get government job?"
- Quality: "How stable is my job?" - "Is my career going well?" - "Will my business do well?"
- Selection: "Should I take job A or B?" - "Job or business?" - "Should I change my career?" - "Which field suits me?"
- Quantity: "How many times will I change jobs?"
- Description: "What kind of career will I have?" - "What does my professional future look like?"
- Causal: "Why am I not getting promoted?" - "Why do I keep losing jobs?"

Note the traps this evidences: "Should I change my career?" is SELECTION over declared
options, not advice; "Will I settle abroad through my job?" is composite
(posting-occurrence + settlement) per boundary 4.3.

## 12. Edge Cases (rulings this model commits to; genuinely open items go to s.15)

1. **Career after retirement / second career**: Retirement is an Exit event, not domain
   exit; post-retirement professional activity is a new Career Path segment (Entry:
   re-entry). No special subdomain needed.
2. **Multiple businesses / multiple jobs / portfolio careers**: Business and Employment
   are entities, so plurality is a parameter/target matter at question time, never new
   concepts. QUANTITY class covers "how many".
3. **Freelancing / gig economy**: Contract kinds (freelance, gig) on Engagement; freelance
   practice is `profession` (practice) with engagements, not a new subdomain.
4. **Government service**: Employer kind = government; security semantics differ but the
   model is unchanged; exam-based selection *into* service is Education->Career boundary 4.2
   (exam = education; appointment = career).
5. **Military**: rank system maps to Advancement; postings to Assignment; discharge to
   Separation/Exit; proceedings to Legal (4.8).
6. **Political career**: elections-as-contests are career-entry/progression events for the
   politician-subject (office = Role; electorate = employer-analogue); public standing
   beyond the field is Reputation (4.7). Adopted: political office IS Career.
7. **Influencer/creator career**: venture-or-profession depending on structure; audience
   fame is Reputation; platform income is compensation (career facet) vs wealth (finance).
8. **Sports career**: profession with early typical Exit; the model's Exit/second-career
   machinery covers it without special cases.
9. **Religious profession**: clergy-as-occupation is Career (`profession`); personal faith
   is `inner_life` (4.6).
10. **Family business**: the venture is Career; intra-family succession disputes are
    Family/Legal boundary matters; the subject's role in the family firm is Employment/
    Business per their position.
11. **Career break for caregiving**: the break is Career (Interruption); the caregiving
    itself is Family.
12. **Academic career**: studying is Education; the academic *as professional*
    (appointments, tenure, publications-as-recognition) is Career.
13. **Unpaid/volunteer leadership**: NOT ruled here - whether unpaid productive roles
    (homemaker, volunteer office) fall inside "working life" is a genuine scope decision
    -> CDQ-3.

## 13. Future Expansion

- **New work forms** (e.g., new engagement kinds, AI-era occupations) enter as Contract
  kinds, Professions or Industries - vocabulary additions to s.6/s.7 lists (MINOR to this
  model), never structural change.
- **New subdomains** only when a territory demonstrably fits no existing topic *and*
  passes the necessity/orthogonality tests of Domain Registry s.7 in miniature; expected
  rate: rare (the 12 topics were stress-tested against s.12's edge cases).
- **New events/outcomes** append to taxonomies with a boundary check against neighbours.
- The model version follows document semver; question generation pins the model version it
  was generated against, so growth never invalidates existing Questions.
- Splitting Career (e.g., Business into its own domain) is a Domain Registry merge/split
  event (s.6) - possible, governed, and requiring migration maps; this model's subdomain
  separation of `business` was designed to make such a split clean if ever ratified.

## 14. Validation Checklist (before any question generation from this model)

- [ ] Domain `career` ratified in the Domain Registry with Scope/Out-of-Scope lifted from
      s.2/s.3 and reciprocity closed with `finance`, `education`, `health`, `travel`,
      `residence`, `reputation`, `legal`, `family`, `relationship`, `inner_life` (CDQ-2).
- [ ] Every s.4 boundary case entered as a boundary note on BOTH affected domains.
- [ ] Subdomain topic vocabulary (s.5) frozen as the slug segment-2 controlled list.
- [ ] Every s.7 event and s.8 outcome term checked unique against entity/subdomain names
      (no synonym duplicates) - one term, one meaning.
- [ ] Each s.11 phrasing resolvable in principle to (class, subdomain, aspect) without
      ambiguity by two independent reviewers (sample adjudication recorded).
- [ ] Each s.12 ruling reviewed and countersigned by the domain owner.
- [ ] All CDQ items resolved or explicitly deferred with recorded rationale.
- [ ] QUALITY scale artifacts for s.8 outcomes ratified (CDQ-5) or generation restricted
      to non-QUALITY classes.
- [ ] Model version tagged; question-generation batches record it.

## 15. OPEN QUESTIONS (assumptions refused)

CDQ-numbered; mirrored into docs/OPEN_QUESTIONS.md on adoption.

| ID | Question | Blocks |
|---|---|---|
| CDQ-1 | Ratification of `career` as a registry domain (instance of DQ-1) with this model's s.2/s.3 as its record content | Everything downstream |
| CDQ-2 | Reciprocity closure: the ten receiving domains must claim s.3's territories - cannot be closed unilaterally from inside Career | Domain LOCK |
| CDQ-3 | Are unpaid productive roles (homemaker, long-term volunteer office) inside "working life"? Scope decision with cultural weight - owner call | s.2 scope edge; intake rules |
| CDQ-4 | Subject-scope: are career questions about specified others (spouse's career, child's career) Career-domain nodes with subject parameter, or Family-domain? (instance of HQ-6) | s.6 Person entity; intake routing |
| CDQ-5 | Declared Rating scales for career QUALITY outcomes (stability, satisfaction, venture health): who authors, where they live, how versioned | s.8/s.9 QUALITY generation |
| CDQ-6 | Does `compensation` remain a Career topic long-term, or migrate to `finance` at ratification? This model argues career-facet placement (4.1) but the finance domain owner must concur | s.5 topic list stability |

---

## Self-Audit Record (independent-architect pass performed before finalisation)

Issues found and fixed: (1) *Income* initially scoped wholesale into Career - split into
compensation-as-career-outcome vs wealth-as-finance (4.1), residual concurrence flagged
CDQ-6 rather than assumed. (2) *Skills* duplicated Education's territory - resolved by
acquisition-vs-application locus (4.2, `skill` topic narrowed). (3) *Recognition*
collided with the `reputation` domain - resolved by audience test (4.7). (4) *Workplace
conflict* risked overlap with `legal` and `relationship` - scoped to conflict-as-work-
matter with proceedings->Legal, romance->Relationship. (5) Subdomain list initially 15
with `leadership`, `entrepreneurship`, `retirement` as separate topics - merged into
`advancement`, `business`, `exit` to remove synonym duplication and keep slug vocabulary
tight. (6) Edge case "unpaid roles" was initially ruled in-scope by assumption - reverted
to CDQ-3 as a genuine owner decision. (7) Verified no s.7 event name collides with an s.5
topic name except by deliberate containment. Remaining known limitation: reciprocity
(CDQ-2) is structurally unclosable from this side - correctly deferred, not papered over.
