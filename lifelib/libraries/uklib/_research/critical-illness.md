# Critical Illness Cover (accelerated with term assurance, and standalone) — research notes (UK)

All sources accessed 2026-08-03. Facts are tagged [S#]/[R#] where extracted from a document actually
fetched and read; facts from general knowledge are tagged [unverified]. Where a fetch failed the
source is retained as a known reference with `fetched_ok = false` and nothing is cited to it as verified.

---

## Primary sources

### S1 — Legal & General, "Life Insurance / Critical Illness Cover — Policy Terms and Conditions" (QGI14872 — 2026/07)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy conditions (combined booklet: Life Insurance PB QGI12849 + Critical Illness Cover PB)
- URL: https://www.legalandgeneral.com/asset/499546/globalassets/personal/life-cover/_resources/documents/qgi14872.pdf
- Fetched: YES (PDF, 47 pp., full text extracted)
- Current direct (D2C) retail product. Critical Illness Cover is sold alongside Life Insurance as a
  separate policy ("Additional or Independent Critical Illness Cover") [S1]. Key facts extracted below.

### S2 — Legal & General, adviser Critical Illness Cover product page
- Publisher: Legal & General
- Doc type: technical guide / adviser product page
- URL: https://www.legalandgeneral.com/adviser/protection/products/personal-protection/critical-illness-cover/
- Fetched: YES (HTML, summarised by fetch tool — product limits below)

### S3 — Legal & General, "Critical Illness Cover and Critical Illness Extra with Life Insurance — Policy Booklet" (QGI14162)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy conditions (intermediary "My Life" variant; reviewable premiums)
- URL: https://am.landg.com/asset/4a07ae/globalassets/adviser/files/protection/my-life/landg/policy-booklet/cic-two/cic-two-policybooklet08.pdf
- Fetched: YES (PDF, 42 pp., full text extracted)

### S4 — Aviva, "Critical Illness+ — Policy Conditions" (AL51002, 04/2025)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: policy conditions
- URL: https://static.aviva.io/content/dam/document-library/adviser/individualprotection/al51002c.pdf
- Fetched: YES (PDF, 47 pp., full text extracted; WebFetch was 403 — retrieved via direct HTTPS GET)

### S5 — Aviva, "Policy Summary of Critical Illness+" (AL51001, 04/2025)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: key features document / policy summary
- URL: https://static.aviva.io/content/dam/document-library/adviser/individualprotection/al51001c.pdf
- Fetched: YES (PDF, 28 pp., full text extracted)

### S6 — Royal London, "Critical Illness Cover at a glance" (SAP8P10029/14, June 2025)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: adviser sales aid / product summary
- URL: https://adviser.royallondon.com/globalassets/docs/protection/SAP8P10029-critical-illness-cover-at-a-glance.pdf
- Fetched: YES (PDF, 2 pp., full text extracted)

### S7 — Royal London, adviser page "Details of Critical Illness Cover"
- Publisher: Royal London
- Doc type: adviser product page
- URL: https://adviser.royallondon.com/protection/personal-protection/critical-illness-cover/detail/
- Fetched: YES (HTML, summarised by fetch tool)

### S8 — Royal London, "Personal Menu Plan — Life or Critical Illness Cover — Plan details" (PCP8P10010, July 2025)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions (plan details, 84 pp.)
- URL: https://adviser.royallondon.com/globalassets/docs/protection/pcp8p10010-plan-details-for-the-personal-menu-plan-life-or-critical-illness-cover.pdf
- Fetched: YES (PDF, 84 pp., full text extracted)

### S9 — Vitality, "Serious Illness Cover" public product page
- Publisher: Vitality (VitalityLife)
- Doc type: product page (marketing but with concrete plan facts)
- URL: https://www.vitality.co.uk/life-insurance/serious-illness-cover/
- Fetched: YES (via browser; vitality.co.uk blocks non-browser fetches)

### S10 — VitalityLife, "VitalityLife Essentials Plan Summary" (mirror hosted by LifeQuote)
- Publisher: VitalityLife (document); mirror host: LifeQuote (lifequote.co.uk)
- Doc type: key features document / plan summary
- URL: https://www.lifequote.co.uk/cdrom/KFDocsProps/VitalityLife/VitalityLife%20KFD.pdf
- Fetched: YES (PDF, 16 pp., full text extracted). CAUTION: third-party mirror, undated — describes an
  earlier generation of the product (Primary/Comprehensive severity structure) than the current
  1X/2X/3X presentation on S9. Both recorded; treat S10 as the design reference for the severity mechanics.

### S11 — Zurich, "Key features of the Zurich Life Protection policy" (NP720500009, 02/2025)
- Publisher: Zurich Assurance Ltd
- Doc type: key features document
- URL: https://www.zurich.co.uk/-/media/documents/life-insurance/720500.pdf
- Fetched: YES (PDF, 16 pp., full text extracted)

---

## Regulatory and actuarial references

### R1 — ABI, "Guide to Minimum Standards for Critical Illness Cover" (16 September 2022; April 2023 clarifications)
- Publisher: Association of British Insurers
- URL: https://www.abi.org.uk/globalassets/files/publications/public/protection/abi-guide-to-minimum-standards-for-critical-illness-cover-2023.pdf
- Fetched: NO (abi.org.uk sits behind a Cloudflare challenge that blocked all fetch routes tried).
  Retained as the load-bearing known reference. Its content is triangulated from R2, R3 and from
  insurer documents that visibly implement it (S1 cancer/heart-attack/stroke wordings; S11 states the
  KFD "follows the Association of British Insurers Statement of Best Practice for Critical Illness
  Cover, March 2023" [S11]).

### R2 — Unum, "Definition changes for ABI minimum standards 2023"
- Publisher: Unum Limited
- URL: https://www.unum.co.uk/docs/Definition-changes-critical-illness-cover.pdf
- Fetched: YES (PDF, 3 pp., full text extracted)
- Confirms: the ABI guide "sets out the minimum standards that insurers must meet to call their
  product Critical Illness Cover"; latest full review 2021/22 changed 3 conditions (Alzheimer's →
  broadened to all dementia with MCI exclusion; Cancer clarifications; Heart Attack — myocardial
  injury excluded); April 2023 clarifications; insurers must comply for new policies by 31 January 2024 [R2].

### R3 — SCOR, "Revision of the Minimum Standards for Critical Illness Review 2022"
- Publisher: SCOR (UK)
- URL: https://www.scor.com/en/article/news-uk/revision-minimum-standards-critical-illness-review-2022
- Fetched: YES (HTML)
- Confirms 2022 cancer exclusion changes (NET "WHO Grade 2 or above"; GIST "AFIP/Miettinen and
  Lasota moderate or high risk" or "UICC/TNM8 stage II or above"; prostate "Gleason score of 7 or
  above" / clinical TNM staging), heart-attack clarification, adoption recommended by 31 January 2024;
  prior reviews 2011, 2014, 2018 [R3].

### R4 — FSMA 2000 (Regulated Activities) Order 2001, Schedule 1 (SI 2001/544)
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Fetched: YES
- Part II long-term classes: Class I life and annuity; Class III linked long term; Class IV permanent
  health (contracts providing defined benefits for incapacity from accident or sickness, of indefinite
  duration or running to retirement age, with restricted insurer cancellation rights). Part I general
  classes 1 (accident) and 2 (sickness) [R4].

### R5 — FCA Handbook, ICOBS 1.1 (general application rule)
- Publisher: FCA (handbook.fca.org.uk)
- URL: https://www.handbook.fca.org.uk/handbook/ICOBS/1/1.html
- Fetched: YES (via browser; page as of 03/08/2026)
- ICOBS 1.1.1 R: the sourcebook applies to a firm "with respect to the following activities carried on
  in relation to a non-investment insurance contract … (1) an insurance distribution activity; (2)
  effecting and carrying out contracts of insurance; … (4) communicating or approving a financial
  promotion" [R5]. (Pure protection contracts such as term assurance and CIC are non-investment
  insurance contracts, so conduct rules sit in ICOBS rather than COBS [unverified — FCA Glossary not fetched].)

### R6 — FCA, Consumer Duty firms page
- Publisher: FCA
- URL: https://www.fca.org.uk/firms/consumer-duty
- Fetched: YES (HTML; landing page only)
- The Duty "sets high standards of consumer protection across financial services, and requires firms
  to put their customers' needs first"; final rules in PS22/9 [R6]. In-force dates 31 July 2023
  (open products) / 31 July 2024 (closed products) [unverified].

### R7 — PRA Rulebook, Technical Provisions Part (Solvency UK)
- Publisher: PRA (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Fetched: YES (via browser; Rulebook "in the present" on 03/08/2026)
- Key content extracted (see BEL section below). Confirms the post-reform ("Solvency UK") state:
  risk-margin rules 4A/4B effective 31/12/2024 with cost-of-capital 4% and risk-tapering factor;
  former matching-adjustment chapters 6–7 deleted 30/06/2024 (MA now in its own Part) [R7].

### R8 — IFoA/CMI, "Critical illness investigation" page
- Publisher: Institute and Faculty of Actuaries — Continuous Mortality Investigation
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/critical-illness-investigation
- Fetched: YES (HTML)
- The investigation covers "the morbidity experience of critical illness policyholders" — both
  standalone CI and full accelerated (death + CI) business. Outputs: WP14 (original methodology),
  WP33 (July 2008, "adjusted results" methodology), WP43 (insured-lives accelerated CI diagnosis
  rates 1999–2004), WP50 (AC04 diagnosis-rate tables from 2003–2006 experience), WP52
  (cause-specific diagnosis rates 2003–2006), WP58 (supplementary AC04 analyses), WP75 (2012
  initiative for 2007–2011 data). CIBT93 is the population-based comparison table. Data collection
  from 1998–99 claims onwards [R8].

### R9 — CMI Working Paper 167, "Accelerated critical illness experience by cause of claim, 2017–2020"
- Publisher: IFoA/CMI
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-working-papers/assurances/cmi-working-paper-167
- Fetched: YES (HTML)
- Published January 2023; analyses accelerated CI claims on non-rated term assurance policies
  2017–2020 by cause; tests the fit of the cause-specific diagnosis rates derived in Working Paper
  151; WP167 itself and accompanying chart data are downloadable from the page [R9]. Full CMI
  tables/datasets are generally restricted to authorised users (CMI subscribers) [unverified — access
  limits not stated on the fetched pages].

### R10 — FRC, TAS 100 (General Actuarial Standards) v2.0
- Publisher: Financial Reporting Council
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- Fetched: YES (HTML)
- TAS 100 v2.0 published 3 March 2023, effective 1 July 2023; applies to all technical actuarial work
  within geographic scope and must be applied by IFoA members [R10]. TAS 200 covers technical
  actuarial work in insurance [unverified — separate FRC page not fetched].

### R11 — Bank of England, Solvency II implementation / Solvency UK page
- Publisher: Bank of England / PRA
- URL: https://www.bankofengland.co.uk/prudential-regulation/key-initiatives/solvency-ii-implementation
- Fetched: NO (403 to all fetch routes tried). Retained as known reference. The reformed rule state is
  evidenced directly from the Rulebook text in R7 instead.

---

## Extracted specifications

### 1. Product structure

- **Accelerated vs standalone.** UK CIC is sold (a) combined with life cover so the sum assured pays on
  the earlier of death/terminal illness/critical illness ("Life Cover and Critical Illness" — Zurich
  [S11]; "Life or Critical Illness Cover" — Royal London [S8]; joint life first event basis [S11]), or
  (b) as standalone CI with no death benefit (Zurich "Critical Illness Cover" pays only on a defined
  critical illness [S11]; Aviva Critical Illness+ is a standalone CI contract [S4]); L&G sells CIC
  "alongside your Life Insurance as a separate policy (also referred to as Additional or Independent
  Critical Illness Cover)" — i.e. contractually separate but distributed with life cover [S1].
- **Benefit shape.** Lump sum on level or decreasing basis; Aviva also offers "family income cover"
  paying equal monthly instalments to the end of term [S4]. Royal London offers lump sum or regular
  payments (decreasing cover lump-sum only) [S7].
- **Policy ends** when the full (main) CI benefit is paid [S1][S4][S11]. Additional-payment
  (partial) claims and children's claims do NOT reduce the sum assured or end the policy
  [S1][S3][S4][S8][S11].
- **Vitality outlier.** Serious Illness Cover is severity-based: each condition is graded and the claim
  pays a percentage of the cover amount by severity — historically 5% (Severity G) to 100% (Severity A),
  with "Primary Cover" spanning severities A–E and "Comprehensive Cover" A–G [S10]; the current
  proposition pays 25%–100% per claim on the standard plan (114 conditions) and can be upgraded to
  cover up to 174 conditions with total claims up to 3× the cover amount [S9]. Payments reduce the
  remaining "plan account" unless a Protected Cover option is chosen, which reinstates cover [S10].

### 2. Eligibility, ages and terms

| Parameter | L&G | Aviva CI+ | Zurich | Vitality |
|---|---|---|---|---|
| Min entry age | 18 [S2] | 18 [S5] | 18 [S11] | not stated in fetched docs |
| Max entry age | 67 (life+CIC level) / 64 (other options) [S2] | 64 [S5] | 69 [S11] | — |
| Max age at policy end | policy must end by 75th birthday [S2] | 75 (guaranteed premiums) / 90 (reviewable) [S5] | 74 [S11] | — |
| Min term | 2 yrs (life level/increasing with CIC), 5 yrs others [S2] | 5 yrs (guaranteed) / 6 yrs (reviewable) [S5] | 5 yrs [S11] | — |
| Max term | 50 yrs [S2] | 50 yrs [S5] | 40 yrs [S11] | — |
| Residency to apply | UK resident, ≥183 days in last tax year [S1] | — | — | — |

Ancillary-benefit age limits (Aviva): TPD max entry 64, benefit ends at 70; waiver of premium entry ≤64,
ends 70 (option only available until eldest life turns 71 per conditions [S4]); fracture cover entry
18–59, ends 70; global treatment entry ≤64, ends 84; life change/separation benefit ≤54 [S5].
L&G TPD ends at the policy end date or 70th birthday of the oldest life, whichever earlier, with the
premium reduced when TPD drops off [S1]. Zurich Multi-Fracture Cover entry 18–64, ends 69 [S11].

### 3. Sum assured / cover amounts

- L&G: no minimum sum assured (minimum-premium driven); maxima reported on the adviser page:
  £3m where TPD on Specified Work Tasks basis / £2m own-occupation TPD; Family & Personal Income
  Plan max £4,000 per month [S2 — as summarised by the fetched page].
- Vitality: overall maximum ever paid per person across Serious Illness Cover, Disability Cover,
  Family Income Cover (SIC element) and Education Cover (Severity A) is £3,000,000, raised to
  £4,000,000 with Serious Illness Cover Booster [S10]. Child SIC up to £100,000 per child [S9][S10].
- Royal London: free cover (pre-commencement) up to £500,000, to age 60 [S7].
- Aviva/Zurich: no explicit sum assured caps in the fetched KFD/conditions [gap].

### 4. Survival period

- L&G: pay "if you're diagnosed with a condition or undergo a medical procedure listed … and survive
  for 14 days from diagnosis, even if this is after the policy end date" [S1]. Children: 14 days [S1]
  (10 days in the QGI14162 intermediary variant for children [S3]).
- Aviva: survive at least **10 days** (main, additional, upgraded and children's benefits) [S4][S5].
- Royal London: additional-conditions and children's claims are not paid if the person/child dies
  within **10 days** of meeting the definition [S8]. (On the combined Life or CIC plan the main benefit
  needs no survival period because death itself is insured [S8].)
- Vitality: no payment "if you do not survive for at least **14 days** after the date of the
  life-changing event" (also 14 days for child SIC) [S10].
- ABI-typical survival period is 14 days [unverified — R1 not fetched].

### 5. Conditions covered — counts and structure

| Insurer | Full-payment conditions | Additional/partial-payment conditions |
|---|---|---|
| L&G CIC (retail) | ~37 listed definitions incl. TPD (aorta graft surgery; aplastic anaemia; bacterial meningitis; benign brain tumour; blindness; cancer; cardiac arrest; cardiomyopathy; coma; coronary artery bypass grafts; CJD; deafness; dementia incl. Alzheimer's; encephalitis; heart attack; heart valve replacement/repair; kidney failure; liver failure; loss of hand or foot; loss of speech; major organ transplant; motor neurone disease; multiple sclerosis; multiple system atrophy; open heart surgery; paralysis of limb; Parkinson's; primary pulmonary hypertension; progressive supranuclear palsy; removal of an eyeball; respiratory failure; spinal stroke; stroke; SLE; third-degree burns 20%; TPD; traumatic brain injury) [S1] | 2 conditions at lower of 25% / £25,000 (carcinoma in situ of the breast treated by surgery; low-grade prostate cancer Gleason 2–6, ≥T1N0M0) [S1] |
| L&G CIC Extra (intermediary) | CIC list + ~17 extra full-payment definitions (benign spinal cord tumour; cauda equina syndrome; heart failure — EF ≤39% and NYHA Class 3; intensive care — 7 days' ventilation; interstitial lung disease — DLCO <40%; myasthenia gravis; necrotising fasciitis; neuromyelitis optica; Parkinson plus syndromes; peripheral vascular disease; primary sclerosing cholangitis; pulmonary artery surgery; removal of an entire lung; removal of an eyeball; severe Crohn's disease; syringomyelia/syringobulbia; ulcerative colitis) [S3] | ~22 conditions at lower of £30,000 / 50% of cover (incl. aortic aneurysm with endovascular repair; severe aplastic anaemia; brain abscess; carotid artery stenosis ≥50% with surgery; central retinal artery/vein occlusion; cerebral/spinal aneurysm and AVM; coronary angioplasty of 2+ arteries; Crohn's — one resection; desmoid-type fibromatosis; type 1 diabetes; drug-resistant epilepsy; Guillain-Barré ≥6 months' symptoms; less advanced cancer of named sites; non-invasive GIST; other cancer in situ/NET with surgery; pituitary gland tumour; removal of lung lobe(s); removal of urinary bladder; significant visual loss 6/24 or field ≤45°; third-degree burns 10%) [S3] |
| Aviva CI+ (standard) | 33 conditions incl. terminal illness [S5] | 2 conditions (less advanced cancer of breast / of prostate) at lower of £25,000 / 25% [S4][S5] |
| Aviva CI+ (upgraded) | +15 further full-payment conditions (benign spinal cord tumour; brain abscess; intensive care; neuromyelitis optica; Parkinson's plus syndromes; syringomyelia/syringobulbia; heart failure; peripheral vascular disease; Crohn's — 2 resections; interstitial lung disease; necrotising fasciitis; pneumonectomy; ulcerative colitis; rheumatoid arthritis; psychosis and bipolar affective disorder) [S5] | 26 upgraded additional conditions at lower of £30,000 / 100% of cover [S4][S5] |
| Royal London | 46 full-payment definitions (incl. 13 advanced-surgery-benefit conditions paid on joining an NHS waiting list) [S6] | 32 additional conditions at 50% of cover up to £35,000, incl. 17 early forms of cancer [S6][S8] |
| Zurich | 39 Full Payment conditions incl. terminal illness [S11] | 2 Additional Payment conditions (less advanced cancer of breast / of prostate) at lower of £25,000 / 25%, one claim per condition per life [S11] |
| Vitality | severity-graded: standard plan 114 conditions (payouts 25%–100%); upgraded plans up to 174 conditions (historically payouts from 5% at Severity G) [S9][S10] | n/a — partial payment is intrinsic to the severity scale [S9][S10] |

Market context: "On average, critical illness insurance policies only cover 75 conditions (Defaqto, 2026)" [S9].

### 6. Headline (ABI-aligned) definitions — key parameters from L&G wording

- **Cancer** — malignant tumour, positive histological diagnosis, uncontrolled growth + tissue invasion;
  excludes pre-malignant / in-situ / borderline / low malignant potential; prostate covered only if
  Gleason ≥7 or ≥ cT2bN0M0 (or pT2N0M0 post-prostatectomy); urothelial only ≥ T1N0M0; thyroid only
  ≥ T2N0M0; melanoma confined to epidermis excluded; NETs without nodal/distant spread only if WHO
  Grade ≥2; GIST only if AFIP/Miettinen-Lasota moderate/high risk or UICC/TNM8 stage ≥II [S1].
  (These are the 2022/23 ABI minimum-standard parameters [R2][R3].)
- **Heart attack** — definite acute MI: new ECG or imaging changes AND characteristic rise of cardiac
  markers (troponins/enzymes); myocardial injury without infarction and angina excluded [S1].
- **Stroke** — death of brain tissue (blood supply/haemorrhage) with neurological deficit and clinical
  symptoms lasting ≥24 hours; TIA and eye/optic-nerve stroke excluded [S1].
- **Dementia incl. Alzheimer's** — "of specified severity", diagnosis by specified consultants supported
  by neuropsychometric testing; MCI excluded [S1] (2022 ABI change broadened Alzheimer's to all
  dementia and added the MCI exclusion [R2]).
- **TPD** — two definitions: "Own occupation … unable to do your own occupation ever again before your
  70th birthday" or "Specified Work Tasks" (unable ever again to do 3 of 6 tasks: walking 200 m,
  climbing 12 stairs, lifting 2 kg for 60 s, bending, getting in/out of a car, writing/typing); disabilities
  without a clear prognosis are not covered [S1]. Aviva mirrors this ("own occupation" / "activities of
  daily work", before age 71, 3 of 6 tasks) [S4].

### 7. Children's cover

| Feature | L&G (retail) | Aviva (standard / upgraded) | Royal London (standard / enhanced) | Zurich (optional add-on) |
|---|---|---|---|---|
| Inclusion | automatic with CIC [S1] | automatic / paid upgrade [S4] | included options [S7][S8] | optional, flexible add/remove [S11] |
| Ages | 30 days–18th birthday (21 if in full-time education) [S1] | 30 days–18 (21 FTE) / birth–22nd birthday [S4] | to age 22 (23 if FTE) [S7][S8] | to 22nd birthday; death benefit after 30 days old [S11] |
| Amount | lower of 50% of cover or £25,000 per child; max 2 children per policy; £50,000 max per child across policies [S1] | lower of £25,000 or 50% / flat £25,000 upgraded [S4] | 50% capped £30,000 standard / capped £50,000 enhanced (full conditions; additional conditions capped £35,000) [S6][S8] | lower of £25,000 or 50% (full-payment); lower of £25,000 or 25% (additional-payment) [S11] |
| Death of child | Child Funeral Benefit £4,000 (max 2 children) [S1] | £5,000 / £10,000 upgraded, incl. stillbirth from 24th week [S4] | £5,000 standard / £10,000 enhanced [S6][S8] | £5,000 [S11] |
| Pregnancy complications | — | £5,000 per pregnancy (6 listed complications, upgraded benefit) [S4] | 8 complications, £5,000 per pregnancy; £5,000 per foetus (death in utero); £10,000 stillbirth [S6][S8] | — |
| Extras | accident hospitalisation £5,000; family accommodation £100/night to £1,000; childcare up to £1,000 [S1] | hospital £100/night from 8th night, ≤30 nights; child extra care £50,000; advanced illness £10,000 [S4] | conversion option: child can take own CIC ≤£50,000 within 6 months of children's cover ending, no underwriting [S6] | conversion benefit age 18–22, up to lower of £25,000 or 50% [S11] |
| Exclusions | condition present at birth; symptoms pre-start; death within survival period; TPD [S1] | congenital/pre-start symptoms; parental awareness of risk (upgraded) [S4] | pre-existing risk awareness (pregnancy complications) [S8] | one full-payment claim per child [S11] |
| Vitality | Child Serious Illness Cover: standalone add-on up to £100,000 per child, multiple claims, covers birth-diagnosed conditions, £5,000 funeral contribution; pre-existing conditions excluded [S9][S10] | | | |

### 8. Premiums

- Payment monthly or annually; 60-day grace period then cancellation without refund [S1][S4]
  (30 days in the L&G intermediary variant [S3]).
- **Guaranteed vs reviewable**: L&G retail CIC — guaranteed [S1] (choice of guaranteed or reviewable
  by cover type on the adviser menu [S2]); Aviva — both offered; reviews every 5 years from the 5th
  anniversary; "There are no limits on how much your premium can change"; changes <2% or 50p ignored;
  policyholder may instead reduce cover [S4][S5]. Royal London — guaranteed or reviewable [S7][S8].
  L&G QGI14162 variant — reviewable: no change for first 5 years, then 5-yearly reviews on claims
  experience/industry experience/medical advances/law, ±5% tolerance, individual health not a factor [S3].
- **Indexation (increasing cover)**: L&G — cover up by RPI (no increase if RPI <1%, capped 10% p.a.);
  premium up by RPI × 1.5 capped 15% p.a.; declining 3 years in a row removes the option [S1].
  Aviva — RPI-linked (cover max 10%, premium ×1.5 max 15%) or fixed 3% / 5%; decline 3 in a row →
  option removed; family income basis: 3%/5% with no premium increase [S4]. Royal London — increasing
  2–5% fixed or RPI 2–10% [S7]. Vitality — RPI rounded up to next 0.25%, increases capped at 10%,
  tiered premium loadings (RPI+1.5% / +2.5% / +3.5% by RPI band; RPI+5% above age 80) [S10].
- **Waiver of premium**: L&G — optional; starts after 26 consecutive weeks of incapacity (own
  occupation, or 3+ specified work tasks if not in paid employment) [S1]. Aviva — optional; own
  occupation or 2 of 6 work tasks; deferred period applies; stops at age 71 [S4].

### 9. Guaranteed insurability / options

- L&G "Increasing your cover" (life events): marriage/civil partnership, divorce/dissolution, birth,
  adoption, pay rise on promotion/new job, mortgage increase on move/improvements; policy must have
  started before 55th birthday; notify within 6 months; increase capped at the lower of 100% of
  original cover or £200,000 (and % pay rise / mortgage increase where relevant), implemented as an
  additional policy ending at the 65th birthday or 1 year after original expiry [S1].
- Aviva "Life change benefit": included when accepted on standard terms, eldest life <55, 8 events
  (incl. rent increases and switching rental→mortgage); new policy within 180 days; total additional
  cover capped at the lower of £200,000 or the original cover amount (family income: the equivalent
  of £8,000 a year); new policy must end before age 70 [S4].
- Zurich "Milestone benefit": within 90 days of a life event, age ≤54, increase capped at the lower of
  the original sum assured or £200,000 [S11].
- Joint-life separation options: L&G — separate on divorce/dissolution/mortgage change; new single
  policies at current rates, cover ≤ min(£1m, original), ending by 75th birthday (CIC) / 70th (life)
  or original expiry + 1 year [S1]. Aviva "Separation benefit" — once only, new policy before age 55,
  ends before 70 [S4]. Zurich — separation option on joint policies [S11].
- Replacement cover after a joint-life claim: L&G — the non-claiming life may take a new single
  policy within 6 months (not after additional-cover-only claims) [S1].

### 10. Exclusions and standard provisions

- CI policies carry few blanket exclusions; exclusions are embedded per definition (e.g. cancers
  below staging thresholds, drug/alcohol-secondary conditions, self-inflicted injury for eyeball
  removal) [S1][S3]. Any case-specific exclusions appear in the policy schedule [S1].
- Claims can be declined for misrepresentation; proportionate remedy reduces cover by the formula
  `new cover = premium charged × original cover / higher premium` [S1].
- Residence/claim-validity: L&G covers claims where the life insured resides in the EU, Australia,
  Canada, Channel Islands, Isle of Man, New Zealand, UK or USA (discretion elsewhere) [S1][S3];
  Aviva restricts waiver-of-premium if living >13 consecutive weeks outside a listed country group [S4].
- Diagnosis must be by a (UK) consultant of appropriate specialism [S1][S4].
- First-year suicide/self-inflicted-death clause applies to the life insurance element [S1][S3].
- Cooling-off: 30 days with full premium refund; thereafter no refund on monthly premiums
  (pro-rata refund of annual premiums on cancellation at L&G) [S1][S4][S5].
- **Surrender/paid-up**: these are pure protection contracts; the fetched documents describe
  cancellation with no payment other than the cooling-off refund [S1][S4][S5] — no surrender or
  paid-up value exists [unverified as an explicit statement; consistent with all fetched terms].
- Tax/trusts: the L&G retail policy is written to remain a qualifying policy compatible with
  para 19(3) Schedule 15 ICTA 1988 and "cannot be issued or assigned into a trust" [S1] (other
  insurers' plans commonly are placed in trust [unverified]).
- FSCS: 100% of the claim value protected, with continuity preferred [S1].

### 11. Aviva-specific riders (design variations worth modelling)

- **Extra care cover**: pays the cover amount + £50,000 where a CI claim is accompanied by severe
  permanent disability (unable to perform 3+ of 6 ADLs), or the life covered is under 55 when meeting
  specified degenerative-condition definitions (dementia, kidney/liver failure, Parkinson's, MND,
  respiratory failure, heart failure/Parkinson's-plus if upgraded); a follow-on £50,000 is payable if
  permanent loss of independence emerges within 18 months of a trigger claim [S4].
- **Fracture cover**: schedule of fixed benefits £2,000–£6,000, one claim per policy year, sport
  exclusions [S4]. (Zurich Multi-Fracture Cover: £2,000/£4,000/£6,000, max £6,000 per policy year [S11].)
- **Global treatment**: overseas-treatment benefit administered by a third party, renewing every
  3 years (premium may change at renewal) [S4][S5].
- **Hospital benefit**: £100/night from the 8th consecutive night, max 30 nights (upgraded benefit)
  [S4].

### 12. Vitality Serious Illness Cover mechanics (severity-tiered variation)

- Severity scale: payout is a percentage of cover by severity — 5% (Severity G) up to 100%
  (Severity A); Primary Cover = severities A–E; Comprehensive Cover = A–G [S10]. Current standard
  plan: 114 conditions, each claim pays 25%–100%, further claims allowed up to 100% of cover;
  upgraded ("boosted") plans: up to 174 conditions, claims up to 3× the cover amount, minimum
  payouts down to 5% (3X plan) [S9] [counts 114/143/174 by 1X/2X/3X tier: only 114 and 174 confirmed
  on the fetched page; the 2X tier at 143 conditions 15%–100% is [unverified]].
- Multiple claims: subsequent claims classified as "progressive" or "unrelated", affecting the
  incremental amount payable [S10]. Claims reduce the plan account; Protected Life and Serious
  Illness Cover reinstates cover after a claim [S10].
- Cancer Relapse Benefit (Comprehensive): pays again for the same cancer recurring at the same or
  lower severity after ≥1 year's remission, with the lump sum increased by 50% [S10].
- Dementia and FrailCare Cover: at SIC expiry remaining cover converts to later-life cover paying
  25% (Severity D) to 100% (Severity A); requires SIC plus Vitality/Wellness Optimiser; no new
  underwriting [S9][S10].
- Family Benefit: automatic £5,000 lump sum for specified conditions [S10].
- Serious Illness Cover Booster: increases payments for certain conditions depending on age and
  dependent children; raises the overall per-person maximum to £4,000,000 [S10].
- Premium engagement mechanics (Vitality Optimiser — premium discounts linked to the Vitality health
  programme) exist but were not detailed in the fetched documents [unverified].

### 13. Prudential valuation frame (Solvency UK) for CI business

- Technical provisions = best estimate + risk margin (Technical Provisions 2.4); value equals the
  current transfer amount to another UK Solvency II firm (2.2) [R7].
- Best estimate: probability-weighted average of future cash flows, discounted on the relevant
  risk-free term structure, gross of reinsurance (3.1), including all cash in- and out-flows required
  to settle obligations over their lifetime (3.2) [R7].
- Risk margin (rules effective 31/12/2024): cost-of-capital method with CoC = 4% (per reg 7B(b) IRPR
  Regulations); formula RM = CoC · Σt SCR(t)·max(λ^t, λ_floor)/(1+r(t+1))^(t+1) with risk-tapering
  factor λ = 0.9 for long-term business and floor 0.25 [R7]. (This is the reformed "Solvency UK" risk
  margin — materially lower than the pre-reform 6% no-taper version [unverified comparison].)
- Expense, inflation, and policyholder-option assumptions must be allowed for; lapse/surrender
  assumptions must be realistic and reflect dependence on future conditions (9.1–9.2); obligations
  segmented into homogeneous risk groups by line of business (10.1) [R7].
- The former matching-adjustment chapters of the Part were deleted 30/06/2024 (MA now regulated in a
  dedicated Part) [R7]; MA is in practice irrelevant to CI term business [unverified].
- Conduct: ICOBS applies to these non-investment insurance contracts [R5]; the Consumer Duty requires
  firms to deliver good outcomes incl. fair value [R6].
- Authorisation classes: accelerated CI written with life cover falls in long-term Class I (life and
  annuity); standalone CI is typically written as long-term Class IV (permanent health — "contracts
  providing defined benefits for incapacity from accidents or illness, requiring either indefinite
  duration or coverage through retirement age") or general classes 1–2 for short-term forms
  [R4 for the class definitions; the mapping of CI products to classes is [unverified]].

### 14. Actuarial/morbidity basis

- CMI CI investigation: covers standalone and full accelerated CI business; diagnosis-rate approach —
  "AC04" insured-lives accelerated CI diagnosis-rate tables (WP50, 2003–2006 experience), cause-specific
  diagnosis rates (WP52; updated in WP151), adjusted-results methodology matching settled claims to
  exposure (WP33) [R8][R9].
- CIBT93: population-based CI diagnosis table used as a comparison basis (originating from the 2000
  SIAS paper "A Critical Review") [R8; provenance detail from search snippet — treat the SIAS
  attribution as [unverified]].
- Latest public output: WP167 (Jan 2023) — accelerated CI experience by cause of claim 2017–2020 on
  non-rated term assurances; notes WP151 cause-specific diagnosis rates still fit; 2020 experience
  affected by COVID-19 [R9].
- Modelling implication for accelerated CI: the decrement is "death or CI diagnosis, whichever first";
  the CMI's accelerated investigation measures combined claim incidence with cause-of-claim splits
  [R8][R9]. The classical independent-rates formulation (ix diagnosis rates plus mortality net of
  overlap) is standard actuarial practice [unverified].
- Standards: TAS 100 v2.0 applies to all technical actuarial work from 1 July 2023 [R10]; TAS 200
  applies to insurance work [unverified].

---

## Variations across insurers

1. **Payment architecture.** The dominant design (L&G, Aviva, Zurich, Royal London) is: one lump-sum
   full payment on a defined-conditions list (33–46 conditions), which ends the policy, plus a set of
   lower-severity "additional payment" conditions paying a capped percentage without reducing cover.
   Vitality replaces this with a graded severity scale (A–G, 100% down to 5%/25%) and multiple claims
   against a depletable (or protected) account — the key structural outlier [S9][S10][S1][S4][S11][S6].
2. **Additional-payment calibration** varies: 25% capped £25,000 (L&G retail, Aviva standard, Zurich)
   → 50% capped £30,000–£35,000 (L&G CIC Extra, Royal London) → 100% capped £30,000 (Aviva upgraded)
   [S1][S3][S4][S8][S11].
3. **Two-tier menu**: most insurers now sell a core product plus an enhanced tier (L&G CIC vs CIC
   Extra; Aviva standard vs upgraded; Zurich "three levels" of CI per its 2024 relaunch [unverified —
   media page not fetched]; Vitality 1X/2X/3X). Enhanced tiers add ~15–20 full-payment conditions and
   expand partial payments [S3][S4][S5].
4. **Survival period**: 14 days (L&G retail, Vitality) vs 10 days (Aviva, Royal London, L&G
   intermediary children's) [S1][S4][S8][S10][S3].
5. **Children's cover**: always a capped percentage (50%) with per-child and per-policy limits;
   caps range £25,000–£50,000; enhanced tiers add child-specific congenital-onset conditions,
   pregnancy complications and conversion options [S1][S3][S4][S6][S8][S11]. Zurich makes children's
   cover optional; L&G/Aviva/RL include a standard level automatically [S11][S1][S4][S7].
6. **Premium guarantee**: retail CIC premiums are now typically guaranteed; reviewable variants
   persist (Aviva, Royal London menus; L&G intermediary QGI14162 with 5-yearly reviews and no cap on
   review changes at Aviva) [S1][S3][S4][S5][S7].
7. **Representative design for a reference implementation**: an accelerated level-term + CI contract
   (single or joint life first event), guaranteed premiums, ~40 ABI-aligned full-payment conditions
   incl. TPD, 2–3 additional-payment conditions at 25%/£25,000, children's cover at 50%/£25,000
   (2-claim limit), 14-day survival period, entry 18–64, expiry ≤75, term 5–50 years — this matches
   the L&G/Aviva/Zurich mainstream closely [S1][S4][S5][S11]. A standalone variant is identical minus
   the death benefit (premium refund/no payment on death within survival period) [S4][S11]. The
   Vitality severity-tiered account is the documented alternative design [S9][S10].

---

## Gaps and caveats

- **ABI Guide (R1) not directly fetched** — abi.org.uk is behind a Cloudflare human-verification
  challenge for all routes tried (direct fetch, scripted download, text proxy). Its requirements are
  reconstructed from Unum's compliance note [R2], SCOR's review [R3], and insurer wordings that
  implement the model definitions [S1][S11]. The exact list of required model wordings/exclusions and
  the guide's precise survival-period language remain unverified.
- **Vitality current plan provisions not retrievable** — vitality.co.uk/adviser.vitality.co.uk block
  non-browser downloads, and the in-browser PDF link triggers a native download dialog. Severity
  mechanics were taken from an older official plan summary hosted by LifeQuote [S10] (mirror,
  undated) and the live product page [S9]. The current 1X/2X/3X condition counts other than 114/174,
  per-severity percentage tables by condition, and Vitality Optimiser premium mechanics are not verified.
- **Royal London entry ages/term/sum limits** not found in the fetched plan details (the 84-page plan
  details is definitions-focused); the adviser "at a glance" and detail pages give benefit amounts but
  not underwriting limits.
- **Zurich full policy terms** not fetched (KFD only); Zurich's survival period and its 2024 "three
  levels" CI proposition are unverified.
- **Premium rates**: no insurer publishes CI rate cards; premium levels can only be sampled from
  quote engines (not done). Aviva reviewable-premium reviews explicitly have "no limits" on changes [S4].
- **L&G adviser-page numbers** (max sums assured £2m/£3m, FPIP £4,000/month, min term 2 years) come
  from a fetch-tool summary of a JS-heavy page (S2); they are plausible but were not verified against
  a second document.
- **CMI data access**: working papers (incl. WP167) are publicly downloadable [R9], but full CMI
  tables/datasets are believed restricted to authorised users/subscribers [unverified]; AC04 table
  values were not obtained.
- **Consumer Duty dates** (31 July 2023 / 31 July 2024) and the ICOBS "pure protection" glossary
  mapping are stated from general knowledge [unverified]; the FCA landing pages fetched carried
  little substantive text.
- The two L&G booklets differ (retail QGI14872 2026/07 guaranteed-premium vs intermediary QGI14162
  reviewable-premium, 10- vs 14-day child survival), so L&G facts must be cited to the correct variant.
