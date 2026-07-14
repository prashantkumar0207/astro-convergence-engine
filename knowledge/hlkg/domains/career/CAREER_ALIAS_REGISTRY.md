| Field | Value |
|---|---|
| Status | DRAFT - PROPOSED alias batch, pending import gates |
| Version | 0.1.0 |
| Owner | TBD (Q1 / DQ-4) |
| Last updated | 2026-07-11 |
| Governed by | docs/HLKG_CONSTITUTION.md s.7/s.16, docs/QUESTION_REGISTRY_SPEC.md s.14/s.15, docs/CANONICAL_QUESTION_SCHEMA.md, CAREER_QUESTION_LIBRARY.md v0.1.0 |
| Repository path | knowledge/hlkg/domains/career/CAREER_ALIAS_REGISTRY.md |
| Machine verification | 399 aliases over all 61 nodes (en 203, hi 61, hi-Latn 135). Per-locale normalised uniqueness across the entire batch: PASS (zero collisions). No alias collides with any canonical label. Every alias maps to exactly one node. |

# Career Alias Registry

Surface forms mapping natural user language to the 61 career Questions of
CAREER_QUESTION_LIBRARY.md v0.1.0. Aliases never own identity, never carry relationships,
and are Gate-1 material at import (HLKG Constitution s.7). Locales used: `en` (English),
`hi` (Hindi, Devanagari), `hi-Latn` (romanised Hindi / Hinglish - locale tag pending
CQL-3/HQ-5 ratification).

## Conventions

- **Kinds** (provenance tags, not structure): *phrasing* (natural question forms),
  *spelling-variant* (common misspellings/romanisation variants, stored verbatim so Gate-1
  exact matching catches them), *search-phrase* (keyword-style fragments users type into
  search boxes; not grammatical questions).
- **Normalisation** for matching: constitutional function (NFKC, lowercase, whitespace
  collapse, terminal-punctuation strip incl. Devanagari danda). Stored text preserves
  author form.
- Parameter values (years, countries, company names) never appear in aliases - such
  phrases parameterise at query time (QRS s.8).
- One alias -> exactly one node, per locale, registry-wide. Machine-checked for this batch.


## `employment`

### HLKG-N-000401 - `career.employment.first_job_timing` - When is first employment likely to begin?
| Locale | Alias |
|---|---|
| en | When will I get my first job? |
| en | When will I start earning for the first time? |
| en | When will my career start? |
| en | first job timing *(search)* |
| hi | पहली नौकरी कब लगेगी? |
| hi-Latn | first job kab milegi |
| hi-Latn | pehli naukri kab lagegi |
| hi-Latn | pahli nokri kab lagegi *(sp)* |

### HLKG-N-000402 - `career.employment.job_occurrence` - Will employment be obtained within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I be employed soon? |
| en | Will I find work this year? |
| en | Will I get a job? |
| en | job yes or no *(search)* |
| en | will i get a jobb *(sp)* |
| hi | क्या मुझे नौकरी मिलेगी? |
| hi-Latn | kya mujhe job milegi |
| hi-Latn | naukri milegi ya nahi |
| hi-Latn | nokri milegi ya nahi *(sp)* |

### HLKG-N-000403 - `career.employment.job_loss_occurrence` - Will loss of employment occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Am I getting laid off? |
| en | Is my job at risk? |
| en | Will I lose my job? |
| en | job loss risk *(search)* |
| en | will i loose my job *(sp)* |
| hi | क्या मेरी नौकरी जाएगी? |
| hi-Latn | kya meri job chali jayegi |
| hi-Latn | naukri jayegi kya |
| hi-Latn | layoff hoga kya *(search)* |

### HLKG-N-000404 - `career.employment.reemployment_timing` - When is re-employment after a loss of employment likely to occur?
| Locale | Alias |
|---|---|
| en | When will I be re-employed after losing my job? |
| en | When will I get a job again? |
| en | new job after layoff when *(search)* |
| hi | दोबारा नौकरी कब मिलेगी? |
| hi-Latn | dobara naukri kab milegi |
| hi-Latn | job jane ke baad nayi job kab |

### HLKG-N-000405 - `career.employment.job_security` - How secure is the current employment?
| Locale | Alias |
|---|---|
| en | How safe is my job? |
| en | How stable is my current job? |
| en | Is my job secure? |
| en | job security level *(search)* |
| en | job securtiy *(sp)* |
| hi | मेरी नौकरी कितनी सुरक्षित है? |
| hi-Latn | job pakki hai kya |
| hi-Latn | meri naukri kitni secure hai |

### HLKG-N-000406 - `career.employment.government_job_occurrence` - Will government employment be obtained within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get a government job? |
| en | Will I get into public service? |
| en | goverment job will i get *(sp)* |
| hi | क्या सरकारी नौकरी मिलेगी? |
| hi-Latn | govt job milegi ya nahi |
| hi-Latn | sarkari naukri milegi kya |
| hi-Latn | sarkari job chance *(search)* |
| hi-Latn | sarkari nokri milegi *(sp)* |

### HLKG-N-000407 - `career.employment.offer_occurrence` - Will an employment offer be received within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get the offer? |
| en | Will the offer letter come? |
| en | job offer yes no *(search)* |
| hi | क्या ऑफर मिलेगा? |
| hi-Latn | offer letter aayega kya |
| hi-Latn | offer milega ya nahi |


## `profession`

### HLKG-N-000408 - `career.profession.vocation_direction` - Which of the declared vocational directions fits best?
| Locale | Alias |
|---|---|
| en | Which career field suits me among these? |
| en | Which of these professions should I choose? |
| en | career field selection *(search)* |
| en | which carrer suits me among these *(sp)* |
| hi | इनमें से कौन सा करियर मेरे लिए सही है? |
| hi-Latn | in options me se kaunsa career sahi hai |
| hi-Latn | kaunsa field choose karun in me se |

### HLKG-N-000409 - `career.profession.change_occurrence` - Will a change of profession occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I change my field? |
| en | Will I switch professions? |
| en | profession change yes no *(search)* |
| hi | क्या मैं अपना पेशा बदलूँगा? |
| hi-Latn | field change hoga kya |
| hi-Latn | kya main apna profession badlunga |

### HLKG-N-000410 - `career.profession.change_timing` - When is a change of profession likely to occur?
| Locale | Alias |
|---|---|
| en | When will I change my line of work? |
| en | When will I switch careers? |
| en | career switch timing *(search)* |
| hi | पेशा कब बदलेगा? |
| hi-Latn | career switch kab hoga |
| hi-Latn | profession kab badlega |

### HLKG-N-000411 - `career.profession.fit_quality` - How well does the current profession fit the subject?
| Locale | Alias |
|---|---|
| en | Am I in the right profession? |
| en | Does my current profession suit me? |
| en | profession fit check *(search)* |
| hi | क्या मैं सही पेशे में हूँ? |
| hi-Latn | kya main sahi profession me hun |
| hi-Latn | yeh field mere liye sahi hai kya |

### HLKG-N-000412 - `career.profession.practice_establishment_timing` - When is an independent professional practice likely to be established?
| Locale | Alias |
|---|---|
| en | When can I start my own practice? |
| en | When will my independent practice begin? |
| en | own practice start when *(search)* |
| hi | अपनी प्रैक्टिस कब शुरू होगी? |
| hi-Latn | apni practice kab shuru hogi |
| hi-Latn | khud ki practice kab start hogi |


## `business`

### HLKG-N-000413 - `career.business.start_timing` - When is a business venture likely to start?
| Locale | Alias |
|---|---|
| en | When can I start my own business? |
| en | When will my business begin? |
| en | business start timing *(search)* |
| hi | अपना व्यवसाय कब शुरू होगा? |
| hi-Latn | apna kaam kab start hoga |
| hi-Latn | business kab shuru hoga |
| hi-Latn | bussiness kab shuru hoga *(sp)* |

### HLKG-N-000414 - `career.business.start_occurrence` - Will a business venture start within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I become an entrepreneur? |
| en | Will I start a business? |
| en | entrepreneurship yes no *(search)* |
| en | will i start a bussiness *(sp)* |
| hi | क्या मैं व्यवसाय शुरू करूँगा? |
| hi-Latn | apna business hoga ya nahi |
| hi-Latn | kya main business karunga |

### HLKG-N-000415 - `career.business.venture_viability` - How viable is the stated business venture as a working enterprise?
| Locale | Alias |
|---|---|
| en | How healthy will my venture be as a business? |
| en | Will my business do well? |
| en | business viability *(search)* |
| hi | क्या मेरा व्यवसाय अच्छा चलेगा? |
| hi-Latn | business acha chalega ya nahi |
| hi-Latn | mera business chalega kya |

### HLKG-N-000416 - `career.business.closure_occurrence` - Will closure of the stated business occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Is my business going to close? |
| en | Will my business shut down? |
| en | business closure risk *(search)* |
| hi | क्या मेरा व्यवसाय बंद होगा? |
| hi-Latn | business band hoga kya |
| hi-Latn | kya mera kaam band ho jayega |

### HLKG-N-000417 - `career.business.expansion_timing` - When is expansion of the stated business likely to occur?
| Locale | Alias |
|---|---|
| en | When will my business expand? |
| en | When will my business grow? |
| en | business expansion when *(search)* |
| hi | व्यवसाय कब बढ़ेगा? |
| hi-Latn | business expand kab hoga |
| hi-Latn | business kab badhega |

### HLKG-N-000418 - `career.business.sale_occurrence` - Will a sale or exit of the stated business occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I exit my business? |
| en | Will I sell my company? |
| en | business sale exit *(search)* |
| hi | क्या मैं अपनी कंपनी बेचूँगा? |
| hi-Latn | business exit hoga kya |
| hi-Latn | kya main apni company bechunga |

### HLKG-N-000419 - `career.business.partnership_occurrence` - Will a business partnership form within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get a business partner? |
| en | Will a partnership form in my business? |
| en | business partner yes no *(search)* |
| hi | क्या व्यवसाय में साझेदार मिलेगा? |
| hi-Latn | business me partner milega kya |
| hi-Latn | partnership hogi ya nahi business me |


## `advancement`

### HLKG-N-000420 - `career.advancement.promotion_timing` - When is a promotion likely to occur?
| Locale | Alias |
|---|---|
| en | When is my promotion due? |
| en | When will I get promoted? |
| en | promotion timing *(search)* |
| en | when will i get promtion *(sp)* |
| hi | प्रमोशन कब होगा? |
| hi-Latn | promotion kab hoga |
| hi-Latn | promotion kab milega |
| hi-Latn | promosan kab hoga *(sp)* |

### HLKG-N-000421 - `career.advancement.promotion_occurrence` - Will a promotion occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get promoted this year? |
| en | Will my promotion happen within this period? |
| en | promotion yes no *(search)* |
| hi | क्या इस अवधि में प्रमोशन होगा? |
| hi-Latn | is saal promotion hoga kya |
| hi-Latn | promotion milega ya nahi |

### HLKG-N-000422 - `career.advancement.leadership_occurrence` - Will a leadership role be attained within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I become a manager? |
| en | Will I lead a team someday? |
| en | Will I reach a leadership position? |
| en | leadership role chance *(search)* |
| hi | क्या मैं लीडर बनूँगा? |
| hi-Latn | kya main manager banunga |
| hi-Latn | leadership role milega kya |

### HLKG-N-000423 - `career.advancement.leadership_timing` - When is a leadership role likely to be attained?
| Locale | Alias |
|---|---|
| en | When will I lead a team? |
| en | When will I reach a leadership role? |
| en | leadership timing *(search)* |
| hi | नेतृत्व की भूमिका कब मिलेगी? |
| hi-Latn | leadership kab milegi |
| hi-Latn | team lead kab banunga |

### HLKG-N-000424 - `career.advancement.trajectory_description` - What is the likely trajectory of career advancement?
| Locale | Alias |
|---|---|
| en | How will my career progress? |
| en | What will my career growth look like? |
| en | career trajectory *(search)* |
| en | how will my carrer progress *(sp)* |
| hi | मेरा करियर कैसे आगे बढ़ेगा? |
| hi-Latn | career growth kaisi rahegi |
| hi-Latn | mera career kaise aage badhega |

### HLKG-N-000425 - `career.advancement.stagnation_cause` - What factors underlie stagnation in career advancement?
| Locale | Alias |
|---|---|
| en | Why am I not getting promoted? |
| en | Why is my career stuck? |
| en | career stuck reasons *(search)* |
| hi | मेरा करियर क्यों रुका हुआ है? |
| hi-Latn | career kyu ruka hua hai |
| hi-Latn | promotion kyu nahi ho raha |


## `transition`

### HLKG-N-000426 - `career.transition.job_change_timing` - When is a change of job likely to occur?
| Locale | Alias |
|---|---|
| en | When will I change my job? |
| en | When will I move to a new company? |
| en | job change timing *(search)* |
| hi | नौकरी कब बदलेगी? |
| hi-Latn | job kab change hogi |
| hi-Latn | naukri kab badlegi |
| hi-Latn | job kab chenge hogi *(sp)* |

### HLKG-N-000427 - `career.transition.job_change_occurrence` - Will a change of job occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I change my company within this period? |
| en | Will I switch jobs? |
| en | job switch yes no *(search)* |
| hi | क्या मैं नौकरी बदलूँगा? |
| hi-Latn | job switch hoga kya |
| hi-Latn | kya main company change karunga |

### HLKG-N-000428 - `career.transition.job_change_count` - How many changes of employer are indicated within the stated horizon?
| Locale | Alias |
|---|---|
| en | How many employers will I have in this period? |
| en | How many times will I change jobs? |
| en | job change count *(search)* |
| hi | कितनी बार नौकरी बदलेगी? |
| hi-Latn | kitni baar job change hogi |
| hi-Latn | kitni companiya badlunga |

### HLKG-N-000429 - `career.transition.career_change_occurrence` - Will a change of career occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I change my career completely? |
| en | Will I move into a different career altogether? |
| en | complete career change *(search)* |
| hi | क्या मैं पूरी तरह करियर बदलूँगा? |
| hi-Latn | kya main career hi badal dunga |
| hi-Latn | poora career change hoga kya |

### HLKG-N-000430 - `career.transition.career_break_occurrence` - Will a career break occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I take a break from work? |
| en | Will there be a gap in my career? |
| en | career break chance *(search)* |
| hi | क्या करियर में विराम आएगा? |
| hi-Latn | career break hoga kya |
| hi-Latn | kaam se break lunga kya |

### HLKG-N-000431 - `career.transition.reentry_timing` - When is re-entry into working life after a career break likely?
| Locale | Alias |
|---|---|
| en | When will I return to work after my break? |
| en | When will my career restart after the gap? |
| en | return to work after break *(search)* |
| hi | ब्रेक के बाद काम पर कब लौटूँगा? |
| hi-Latn | break ke baad job kab milegi |
| hi-Latn | gap ke baad career kab restart hoga |

### HLKG-N-000432 - `career.transition.second_career_occurrence` - Will a second career begin within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I start a new career later in life? |
| en | Will there be a second career for me? |
| en | second career chance *(search)* |
| hi | क्या दूसरा करियर शुरू होगा? |
| hi-Latn | dusra career shuru hoga kya |
| hi-Latn | life me second career hoga kya |


## `workplace`

### HLKG-N-000433 - `career.workplace.environment_quality` - How favourable is the working environment expected to be?
| Locale | Alias |
|---|---|
| en | How good will my workplace be? |
| en | Is my work environment good? |
| en | work enviroment good or bad *(sp)* |
| en | workplace environment quality *(search)* |
| hi | काम का माहौल कैसा रहेगा? |
| hi-Latn | office ka mahaul kaisa rahega |
| hi-Latn | work environment acha hoga kya |

### HLKG-N-000434 - `career.workplace.conflict_occurrence` - Will workplace conflict occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I have problems with my boss? |
| en | Will there be conflict at my workplace? |
| en | office conflict chance *(search)* |
| hi | क्या दफ्तर में विवाद होगा? |
| hi-Latn | boss se problem hogi kya |
| hi-Latn | office me jhagda hoga kya |

### HLKG-N-000435 - `career.workplace.conflict_resolution_timing` - When is resolution of the stated workplace conflict likely?
| Locale | Alias |
|---|---|
| en | When will my office problems end? |
| en | When will this workplace conflict get resolved? |
| en | office problem resolution when *(search)* |
| hi | दफ्तर की समस्याएँ कब खत्म होंगी? |
| hi-Latn | boss se jhagda kab suljhega |
| hi-Latn | office ki problem kab khatam hogi |

### HLKG-N-000436 - `career.workplace.relations_quality` - How favourable are working relations with colleagues and superiors expected to be?
| Locale | Alias |
|---|---|
| en | How will my relations with colleagues be? |
| en | Will my boss support me? |
| en | boss support colleagues relations *(search)* |
| hi | सहकर्मियों से संबंध कैसे रहेंगे? |
| hi-Latn | boss support karega kya |
| hi-Latn | colleagues se relation kaisa rahega |


## `performance`

### HLKG-N-000437 - `career.performance.recognition_occurrence` - Will professional recognition be received within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get an award at work? |
| en | Will my work be recognised? |
| en | will my work be recognized *(sp)* |
| en | work recognition chance *(search)* |
| hi | क्या मेरे काम की पहचान होगी? |
| hi-Latn | award milega kya office me |
| hi-Latn | kaam ki pehchan hogi kya |

### HLKG-N-000438 - `career.performance.recognition_timing` - When is professional recognition likely to be received?
| Locale | Alias |
|---|---|
| en | When will I get credit for my work? |
| en | When will my work be recognised? |
| en | recognition timing *(search)* |
| hi | काम की सराहना कब होगी? |
| hi-Latn | kaam ka credit kab milega |
| hi-Latn | pehchan kab milegi |

### HLKG-N-000439 - `career.performance.appraisal_quality` - How favourable is the upcoming appraisal outcome expected to be?
| Locale | Alias |
|---|---|
| en | How favourable will my rating be this cycle? |
| en | Will my appraisal go well? |
| en | appraisal outcome *(search)* |
| en | will my apprisal go well *(sp)* |
| hi | मेरा अप्रेज़ल कैसा रहेगा? |
| hi-Latn | appraisal acha hoga kya |
| hi-Latn | rating kaisi milegi is baar |
| hi-Latn | apprisal acha hoga kya *(sp)* |

### HLKG-N-000440 - `career.performance.field_standing_quality` - How strong is professional standing within the subject's field expected to be?
| Locale | Alias |
|---|---|
| en | How strong will my professional standing be? |
| en | Will I be respected in my field? |
| en | professional standing field *(search)* |
| hi | अपने क्षेत्र में मेरी प्रतिष्ठा कैसी होगी? |
| hi-Latn | apne field me izzat milegi kya |
| hi-Latn | professional standing kaisi hogi |

### HLKG-N-000441 - `career.performance.setback_cause` - What factors underlie repeated professional setbacks?
| Locale | Alias |
|---|---|
| en | Why do I keep failing at work? |
| en | Why do professional setbacks keep happening to me? |
| en | repeated work failure reasons *(search)* |
| hi | काम में बार-बार असफलता क्यों? |
| hi-Latn | kaam me baar baar failure kyu |
| hi-Latn | professional setbacks kyu ho rahe hain |


## `skill`

### HLKG-N-000442 - `career.skill.adequacy_quality` - How adequate are current skills for the stated career goal?
| Locale | Alias |
|---|---|
| en | Are my skills enough for this role? |
| en | Do I have the skills for my career goal? |
| en | skill gap check *(search)* |
| hi | क्या मेरे कौशल इस लक्ष्य के लिए पर्याप्त हैं? |
| hi-Latn | meri skills kaafi hain kya is role ke liye |
| hi-Latn | skills enough hain ya nahi goal ke liye |

### HLKG-N-000443 - `career.skill.demand_description` - What is the demand outlook for the declared skill set in professional application?
| Locale | Alias |
|---|---|
| en | Are my skills in demand? |
| en | What is the demand outlook for my skill set? |
| en | skill demand outlook *(search)* |
| hi | मेरे कौशल की माँग कैसी है? |
| hi-Latn | market me meri skills chalengi kya |
| hi-Latn | meri skills ki demand kaisi hai |

### HLKG-N-000444 - `career.skill.upskilling_direction` - Which of the declared upskilling paths best serves the stated career goal?
| Locale | Alias |
|---|---|
| en | Which course should I do for my career among these? |
| en | Which of these skill paths should I pick? |
| en | upskilling path selection *(search)* |
| hi | इनमें से कौन सा कोर्स करियर के लिए सही है? |
| hi-Latn | in me se kaunsa course karun career ke liye |
| hi-Latn | kaunsi skill seekhun in options me se |


## `assignment`

### HLKG-N-000445 - `career.assignment.foreign_posting_occurrence` - Will a work posting abroad occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get a foreign posting? |
| en | Will I go abroad for work? |
| en | Will I go onsite? |
| en | onsite chance *(search)* |
| en | will i get a foriegn posting *(sp)* |
| hi | क्या विदेश में पोस्टिंग होगी? |
| hi-Latn | abroad ka chance hai kya job me |
| hi-Latn | onsite jaunga kya |
| hi-Latn | videsh me posting hogi kya |
| hi-Latn | foreign posting hoga kya *(search)* |

### HLKG-N-000446 - `career.assignment.foreign_posting_timing` - When is a work posting abroad likely to occur?
| Locale | Alias |
|---|---|
| en | When will I go abroad for work? |
| en | When will my onsite happen? |
| en | onsite timing *(search)* |
| hi | विदेश में पोस्टिंग कब होगी? |
| hi-Latn | onsite kab jaunga |
| hi-Latn | videsh kab jaunga kaam ke liye |

### HLKG-N-000447 - `career.assignment.transfer_occurrence` - Will a transfer of work location occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get transferred? |
| en | Will my work location change? |
| en | transfer chance *(search)* |
| hi | क्या मेरा तबादला होगा? |
| hi-Latn | posting change hogi kya |
| hi-Latn | transfer hoga kya |
| hi-Latn | tranfer hoga kya *(sp)* |

### HLKG-N-000448 - `career.assignment.transfer_timing` - When is a transfer of work location likely to occur?
| Locale | Alias |
|---|---|
| en | When is my transfer due? |
| en | When will I be transferred? |
| en | transfer timing *(search)* |
| hi | तबादला कब होगा? |
| hi-Latn | posting kab badlegi |
| hi-Latn | transfer kab hoga |

### HLKG-N-000449 - `career.assignment.posting_return_timing` - When is return from the current work posting likely?
| Locale | Alias |
|---|---|
| en | When will I come back from onsite? |
| en | When will I return from this posting? |
| en | onsite return timing *(search)* |
| hi | पोस्टिंग से वापसी कब होगी? |
| hi-Latn | onsite se wapas kab aunga |
| hi-Latn | posting se wapsi kab hogi |


## `compensation`

### HLKG-N-000450 - `career.compensation.raise_occurrence` - Will a salary increase occur within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I get a raise? |
| en | Will my salary increase this cycle? |
| en | salary hike yes no *(search)* |
| en | will i get a rise in salary *(sp)* |
| hi | क्या वेतन बढ़ेगा? |
| hi-Latn | increment milega kya |
| hi-Latn | salary badhegi kya |
| hi-Latn | incriment milega kya *(sp)* |

### HLKG-N-000451 - `career.compensation.raise_timing` - When is a salary increase likely to occur?
| Locale | Alias |
|---|---|
| en | When is my next raise? |
| en | When will my salary increase? |
| en | salary hike timing *(search)* |
| hi | वेतन कब बढ़ेगा? |
| hi-Latn | increment kab milega |
| hi-Latn | salary kab badhegi |

### HLKG-N-000452 - `career.compensation.income_growth_quality` - How strong is professional income growth expected to be?
| Locale | Alias |
|---|---|
| en | How strong will my professional income growth be? |
| en | Will my earnings from work grow well? |
| en | income growth from job *(search)* |
| hi | काम से कमाई कितनी अच्छी बढ़ेगी? |
| hi-Latn | kaam se kamai kitni achi badhegi |
| hi-Latn | professional income growth kaisi hogi |

### HLKG-N-000453 - `career.compensation.level_quantity` - What level of professional income is indicated for the stated period?
| Locale | Alias |
|---|---|
| en | How much will I earn from my job? |
| en | What will my professional income level be in this period? |
| en | expected salary level *(search)* |
| hi | नौकरी से कितनी कमाई होगी? |
| hi-Latn | job se kitna kamaunga |
| hi-Latn | salary kitni hogi is period me |

### HLKG-N-000454 - `career.compensation.stagnation_cause` - What factors underlie stagnation of professional income?
| Locale | Alias |
|---|---|
| en | Why is my professional income stuck? |
| en | Why is my salary not increasing? |
| en | salary stuck reasons *(search)* |
| hi | वेतन क्यों नहीं बढ़ रहा? |
| hi-Latn | increment kyu nahi mil raha |
| hi-Latn | salary kyu nahi badh rahi |


## `satisfaction`

### HLKG-N-000455 - `career.satisfaction.career_quality` - How satisfying is the subject's working life expected to be?
| Locale | Alias |
|---|---|
| en | How satisfying will my working life be? |
| en | Will I be happy in my career? |
| en | career satisfaction outlook *(search)* |
| en | will i be happy in my carrer *(sp)* |
| hi | क्या मैं अपने करियर में खुश रहूँगा? |
| hi-Latn | career me khush rahunga kya |
| hi-Latn | kaam me santushti milegi kya |

### HLKG-N-000456 - `career.satisfaction.dissatisfaction_cause` - What factors underlie dissatisfaction with the subject's working life?
| Locale | Alias |
|---|---|
| en | Why am I unhappy at work? |
| en | Why does my working life feel unsatisfying? |
| en | work unhappiness reasons *(search)* |
| hi | काम में असंतोष क्यों है? |
| hi-Latn | job se satisfaction kyu nahi mil raha |
| hi-Latn | kaam me khushi kyu nahi hai |

### HLKG-N-000457 - `career.satisfaction.improvement_timing` - When is satisfaction with working life likely to improve?
| Locale | Alias |
|---|---|
| en | When will my working life improve? |
| en | When will things get better at work? |
| en | work situation improvement when *(search)* |
| hi | काम में हालात कब सुधरेंगे? |
| hi-Latn | job me cheezein kab theek hongi |
| hi-Latn | kaam me halaat kab sudhrenge |


## `exit`

### HLKG-N-000458 - `career.exit.retirement_timing` - When is retirement from working life likely to occur?
| Locale | Alias |
|---|---|
| en | When will I retire? |
| en | When will my working life end? |
| en | retirement timing *(search)* |
| en | when will i retier *(sp)* |
| hi | सेवानिवृत्ति कब होगी? |
| hi-Latn | kaam se kab retire hounga |
| hi-Latn | retirement kab hoga |

### HLKG-N-000459 - `career.exit.early_retirement_occurrence` - Will retirement occur earlier than the stated expected point?
| Locale | Alias |
|---|---|
| en | Will I retire early? |
| en | Will I stop working before the usual age? |
| en | early retirement chance *(search)* |
| hi | क्या जल्दी सेवानिवृत्ति होगी? |
| hi-Latn | early retirement hoga kya |
| hi-Latn | jaldi retire ho jaunga kya |

### HLKG-N-000460 - `career.exit.postretirement_work_occurrence` - Will professional activity resume after retirement within the stated horizon?
| Locale | Alias |
|---|---|
| en | Will I stay professionally active after retiring? |
| en | Will I work after retirement? |
| en | work after retirement *(search)* |
| hi | क्या सेवानिवृत्ति के बाद काम करूँगा? |
| hi-Latn | retire hone ke baad bhi job karunga kya |
| hi-Latn | retirement ke baad kaam karunga kya |

### HLKG-N-000461 - `career.exit.career_end_description` - What is the likely character of the final phase of working life?
| Locale | Alias |
|---|---|
| en | How will my career end? |
| en | What will the last phase of my working life look like? |
| en | career final phase *(search)* |
| hi | करियर का अंतिम दौर कैसा होगा? |
| hi-Latn | career ka aakhri daur kaisa hoga |
| hi-Latn | career ka end kaisa hoga |

## Ambiguous Phrases - deliberately NOT aliases

These common phrasings match multiple nodes and therefore violate the one-alias-one-node
law; intake must disambiguate them (or route via decomposition), never map them:

| Phrase (locale) | Candidate nodes | Disambiguation needed |
|---|---|---|
| "When will I get a job?" / "naukri kab milegi" (en/hi-Latn) | employment.first_job_timing vs employment.reemployment_timing | Is this the first job, or re-employment? (See ALR-1 - a general job-timing node may be the right fix.) |
| "Will my career be good?" (en) | advancement.trajectory_description vs satisfaction.career_quality | Trajectory or satisfaction? |
| "Will I go abroad?" (en) / "videsh jaunga kya" (hi-Latn) | assignment.foreign_posting_occurrence vs travel/residence-domain questions | Work posting, trip, or settlement? (Domain Model boundary 4.3.) |
| "Will I be successful?" (en) | multiple QUALITY/DESCRIPTION nodes | Against which declared goal? |
| "Job or business?" (en/hi-Latn) | profession.vocation_direction (with options bound) | SELECTION requires the option_set bound - phrase admits it, so route to intake with options prompt, not a bare alias. |

## Batch Validation Summary

- 399 aliases across 61/61 nodes (min 5, max 9 per node); en 203, hi 61, hi-Latn 135.
- Per-locale normalised uniqueness: PASS across the whole batch; zero collisions between
  aliases and canonical labels.
- Devanagari normalisation note: terminal danda (।) treated as terminal punctuation.
- Spelling variants intentionally include high-frequency errors (promtion/promosan,
  goverment, foriegn, loose-for-lose, enviroment, carrer, apprisal, bussiness,
  nokri/naukari, incriment, tranfer, retier) stored verbatim for exact Gate-1 capture.
- Search phrases are locale-tagged like any alias and obey the same uniqueness law.

## OPEN QUESTIONS (assumptions refused)

| ID | Question | Blocks |
|---|---|---|
| ALR-1 | Library gap exposed by alias work: no general `employment.job_timing` node exists (only first-job and re-employment). Add it via extension policy, or keep disambiguation-only? Owner call - NOT silently added here. | The most common single phrase in the domain |
| ALR-2 | `hi-Latn` as the ratified tag for Hinglish (vs treating romanised Hindi as `hi` variants) - instance of CQL-3/HQ-5 | All 135 hi-Latn rows |
| ALR-3 | Native-speaker review of the 61 Devanagari aliases (drafted by a non-native process; translation provenance rules HQ-5 require review before supported-locale status) | `hi` locale support claim |
| ALR-4 | Should search-phrases be a separate surface-form class with different matching (prefix/keyword) rather than plain aliases? Current law treats them as aliases; ranking implications belong to QQ-7. | search-phrase matching semantics |

## Self-Audit Record

1. Uniqueness engineered, not hoped: the entire 399-row batch was machine-checked for
   per-locale normalised collisions and against all 61 canonical labels - PASS. During
   drafting, three collisions were caught and rewritten ("naukri kab milegi" originally
   attached to two nodes; "career kaisa rahega" clashed between trajectory and
   satisfaction; "salary badhegi kya" duplicated across raise nodes) - all resolved by
   reassignment to the ambiguity table or rephrasing.
2. The single most common user phrase in this domain proved unmappable under current
   nodes - recorded as ALR-1 rather than force-fitted, and the ambiguity table routes it
   meanwhile.
3. Devanagari content flagged for native review (ALR-3) instead of being asserted correct.
4. No alias embeds a parameter value; verified by inspection sweep for years, place names
   and brand names.
5. Coverage floor enforced: every node has >= 1 alias in each of en and hi-Latn and >= 1
   Devanagari form, satisfying the library's resolvability quality bar in three surfaces.
