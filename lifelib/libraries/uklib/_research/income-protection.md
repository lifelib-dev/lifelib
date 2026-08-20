# Individual Income Protection Insurance — research notes (UK)

Research notes for UK individual income protection (IP) insurance — long-term "permanent
health insurance" paying a regular monthly benefit while the insured is incapacitated by
illness or injury, after a chosen deferred/waiting period, until recovery, expiry or the end
of a limited payment term. These notes are the citation ground truth for the UK
income-protection product documents: source ids S1..S12 and R1..R10 below are **frozen** —
never renumber.

access date: 2026-08-03.

Citation discipline: every extracted fact is tagged `[S#]` or `[R#]` pointing at a document
that was actually fetched and read. `[unverified]` marks statements from general knowledge or
from secondary summaries of documents that could not be retrieved. Where a fetch failed the
failure is recorded and the item is kept only as a known reference (fetched_ok = false).
Cross-references of the form `[regulatory-actuarial.md R#]` point at the shared UK regulatory
reference library in this directory, whose entries were verified in the same working session.

---

## Primary sources

### S1 — Aviva, "Income Protection+ Policy Conditions" (AL52002 10/2024)
- Publisher: Aviva Life & Pensions UK Limited (FRN 185896)
- Doc type: policy conditions, 29 pp. Internal code AV1113426_AL52002_1024.
- URL: https://static.aviva.io/content/dam/document-library/adviser/individualprotection/al52002c.pdf
- Retrieved: YES (server returns HTTP 403 to plain fetch; PDF downloaded via curl with
  browser user-agent, full text extracted and read).
- Content: full contract for Aviva's flagship individual IP product. Core benefits (main,
  restricted, back to work, waiver of premium), cover types (full cover to term / limited
  payment term), benefit calculation (maximum yearly amount, benefit guarantee, income
  offsets), additional benefits (hospital, trauma, NHS special arrangements, life change),
  optional benefits (fracture cover, global treatment, increasing cover), claims, linked
  claims, alterations, premiums (guaranteed/reviewable), eligibility, definitions.

### S2 — Aviva, "Policy Summary of Income Protection+" (AL52001 10/2024)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: policy summary (customer-facing summary; the product's KFD-successor
  disclosure document), 24 pp. Internal code AV1129714_AL52001_1024.
- URL: https://static.aviva.io/content/dam/document-library/adviser/individualprotection/al52001c.pdf
- Retrieved: YES (curl, full text extracted).
- Content: policy term limits (5–52 years; end between age 50 and 71st birthday), deferred
  period menu (4/8/13/26/52/104 weeks, dual deferred), eligibility (18–59), benefit maxima
  and worked examples of the benefit guarantee, increasing-cover mechanics, protection
  promise (free accidental-injury cover during underwriting).

### S3 — LV=, "Income Protection — Guaranteed Premiums — Policy Conditions" (MIMIIP16G, 34552-2021 01/24)
- Publisher: Liverpool Victoria Financial Services Limited (register no. 110035)
- Doc type: policy conditions, 32 pp.
- URL: https://www.lvadviser.com/lifeassets/assets/documents/income-protection-policy-conditions-guaranteed-premiums.pdf
- Retrieved: YES (curl; full text extracted). Edition 01/24.
- Content: own occupation cover (A1) and homemaker cover (A2); claims and payments (B1–B16
  incl. benefit calculation, £1,500 benefit guarantee, back-to-work and proportionate
  payments, linked claims, fracture cover, death benefit, unemployment premium waiver,
  parent & child cover); policy management (C1–C16 incl. inflation-linked cover, guaranteed
  increase options, premium terms); appendices for doctors/surgeons, NHS and teachers sick
  pay guarantees; definitions.

### S4 — LV=, "Income Protection and Budget Income Protection — Key features of the Flexible Protection Plan" (27746-2019 05/19)
- Publisher: LV= (document names Liverpool Victoria Friendly Society Limited as provider —
  older entity; see Gaps)
- Doc type: Key Features Document, 8 pp. Edition 05/19 (older than S3).
- URL: https://www.lifequote.co.uk/cdrom/KFDocsProps/Liverpool%20Victoria/Liverpool%20Victoria%20IP%20KFD.pdf
  (intermediary-hosted mirror of the LV= document; original lvadviser.com copy returns 403)
- Retrieved: YES (curl, full text extracted).
- Content: KFD for the Flexible Protection Plan IP menu: IP vs Budget IP (12/24-month claim
  limits), waiting periods (1, 2, 3, 6, 12 months), maximum cover 60% of earnings, maximum
  benefit £20,833/month level (£14,583 inflation-linked), minimum premium £5/month, £3
  admin charge, minimum 5-year term ending before age 70, guaranteed vs reviewable premium
  terms, sick pay guarantees, homemaker treatment.

### S5 — Royal London, "Personal Menu Plan — Income Protection — Plan details" (July 2026, PCP8P10012/13)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions booklet ("plan details" = full terms and conditions), 56 pp.
- URL: https://adviser.royallondon.com/globalassets/docs/protection/pcp8p10012-plan-details-for-the-personal-menu-plan-income-protection.pdf
- Retrieved: YES (curl; full text extracted). July 2026 edition.
- Content: full T&Cs of the IP cover in Royal London's Personal Menu Plan: claims (incl.
  connected claims, cover payment period), how much is paid (maximum annual benefit, £1,750
  and £3,500 minimum guarantees, offsets, 90% tolerance), additional benefits (Fracture
  Cover, Hospitalisation Payment, Additional Payment on Death, Back to Work Payment, Child
  Illness & Loss, Child Hospitalisation), premiums (level/increasing, payment pause),
  changing cover (increasing cover, Cover Increase Options, Lifestyle/Job Flexibility),
  general conditions, and the three-tier incapacity definitions (Own Occupation / Serious
  Illness / Everyday Tasks), NHS deferred-period tables, terminal illness, definitions.

### S6 — Royal London, "Personal Menu Plan — Our covers and options at a glance" (GP8P10007)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: adviser product-options table, 2-page PDF (4 extracted pages).
- URL: https://adviser.royallondon.com/globalassets/docs/protection/GP8P10007.personal-menu-plan-our-covers-and-options-at-a-glance.pdf
- Retrieved: YES (curl; full text extracted).
- Content: cross-cover parameter table for the Personal Menu Plan: term ranges, minimum
  cover £100/month, minimum premium £5/month (£60/year), entry ages 18–59, IP maximum end
  age 70, deferred periods 4/8/13/26/52 weeks, cover payment periods (whole term/1/2/5
  years), level vs increasing income (fixed 2–5% or RPI min 2% max 10%), guaranteed vs
  reviewable-after-5-years premiums, own occupation vs working-tasks definitions.

### S7 — The Exeter, "Income First — Policy Document" (MKTG585, March 2026)
- Publisher: Exeter Friendly Society Limited (trading as The Exeter; register no. 205309;
  Friendly Societies Act 1992 reg. 91F)
- Doc type: policy conditions ("policy document"), 36 pp.
- URL: https://dyn.the-exeter.com/download/brochure?code=IF-PD
- Retrieved: YES (curl; full text extracted). March 2026 edition.
- Content: full T&Cs for The Exeter's Income First IP: benefit £500–£10,000/month, waiting
  periods Day 1–52 weeks, flexible waiting periods for NHS staff and teachers (tables),
  employer change promise, claim periods (full term / 2-year / 5-year), finishing age
  50–70, guaranteed insurability option, waiver of premium, fixed benefit option, financial
  assessment (65%/45% of £60,000 band), houseperson/unemployed treatment, first job
  promise, rehabilitation and proportionate benefit formula, indexation (CPIH), premium
  options (level guaranteed / age-costed guaranteed / age-costed reviewable), policy
  breaks, redundancy premium holiday, no standard exclusions, territorial limits.

### S8 — The Exeter, "Income First — Policy Summary" (MKTG577, March 2026)
- Publisher: Exeter Friendly Society Limited
- Doc type: policy summary, 8 pp.
- URL: https://dyn.the-exeter.com/download/brochure?code=IF-PS
- Retrieved: YES (curl; full text extracted).
- Content: summary confirming Income First is a long-term IP product paying a regular
  benefit on total inability to work in the own occupation; used to corroborate S7.

### S9 — The Exeter, "Guide to Income Protection — Pure Protection Plus / Income One Plus" (040219/866, Feb 2019)
- Publisher: Exeter Friendly Society Limited
- Doc type: adviser product guide, 20 pp.
- URL: https://lifequote.co.uk/cdrom/KFDocsProps/The%20Exeter/The%20Exeter%20IP%20Guide.pdf
  (intermediary-hosted mirror; document is The Exeter's own adviser guide)
- Retrieved: YES (curl; full text extracted). 2019 edition — records the adviser-sold
  Income One Plus / Pure Protection Plus generation of the product.
- Content: eligibility (18–59, UK resident + NHS GP 3 years, ≥15 h/week, finishing age
  50–70, minimum 5-year term), benefit £500–£10,000/month, replacement formula 60% of
  first £100,000 + 40% above, Fixed Benefit Option (75%) and Minimum Benefit Guarantee
  (£1,000/month, 2-year limited claim period only), three premium options, indexation (RPI
  max 10%), guaranteed insurability option (20% or £500/month), no standard exclusions.

### S10 — Vitality, "Personal Protection Plan Provisions" (VLTD174857WF_J3779_02/2025)
- Publisher: Vitality Life Limited
- Doc type: plan provisions (full T&Cs for the Personal Protection Plan menu — Life,
  Serious Illness and Income Protection Cover), 159 pp.
- URL: https://www.vitality.co.uk/media-online/advisers/literature/life/personal-protection/policy-documents/personal-protection-plan-provisions.pdf
- Retrieved: YES (curl; full text extracted; IP sections B4.1–B4.11 and premium provisions
  D2/D3/E2 read in full). Edition 02/2025.
- Content: Income Protection Cover section B4: incapacity definitions (own occupation /
  activities of daily living), deferred periods 7 days–60 months (dual deferred), benefit
  formula (60%/50% with £5,000/month bands; verified vs unverified earnings; Earnings
  Guarantee), Income Boost by Vitality Status, hospitalisation benefit, Recovery Benefit,
  short payment terms 12/24/60 months, houseperson claims, rehabilitation/proportionate
  benefit, linked claims, public sector deferred periods, waiver of premium; plan-level
  premium provisions (guaranteed / reviewable / Optimiser).

### S11 — Cirencester Friendly, "Income Assured Enhanced — Key Features Document" (V7, May 2026)
- Publisher: Cirencester Friendly Society Limited (register no. 109987; Friendly Societies
  Act 1992 reg. 149F)
- Doc type: Key Features Document, 28 pp.
- URL: https://cirencester-friendly.co.uk/documents/Adviser/004_Income_Assured_Enhanced/Key-Features.pdf
- Retrieved: YES (curl; full text extracted). V7 (MAY 2026).
- Content: KFD for a Holloway-style friendly society IP contract: unit-based benefit
  (£10.50/week per unit; 5–75 units), 60% of earnings ceiling, age-costed guaranteed
  premium rates, deferred periods 1–52 weeks plus Day One Accident Protection, optional
  capital sum (surplus share scheme with early-closure penalties), CPI indexation, end age
  50–70 (or state retirement age if higher), standard exclusions list, incapacity
  definitions (Own Occupation with benefit tapering, Own/Own Suited, Houseperson), £1,500
  minimum benefit guarantee, terminal illness benefit, career break, claim mechanics.

### S12 — Cirencester Friendly, "Schedule 5 — Rules of the Income Assured Enhanced Contract" (V3a, July 2024)
- Publisher: Cirencester Friendly Society Limited
- Doc type: registered contract rules (the legal terms; the KFD S11 is the plain-English
  guide to this document), 28 pp.
- URL: https://cirencester-friendly.co.uk/documents/Adviser/004_Income_Assured_Enhanced/Schedule-5-Rules.pdf
- Retrieved: YES (curl; full text extracted). V3a (JUL 2024).
- Content: Parts A–Q: definitions (Own Occupation Disabling Illness, Houseperson Disabling
  Illness, Member's Credit), membership terms (60% of Earnings limit), premiums, benefits
  of sick members (claim notice and evidence rules, no work of any kind while claiming),
  accident protection, indexation, rehabilitation benefit, proportionate benefit, terminal
  illness benefit, career break, bonuses (Surplus Allocation, Bonus Allocation, Commuted
  Bonus capped at 100% of premiums, discretionary Terminal Bonus on With-Profits Actuary
  advice) — the Holloway capital-account machinery.

---

## Regulatory and actuarial references

### R1 — CMI, "'IP11' Series claim inception and termination rates — Briefing note" (September 2020, note added April 2021)
- Publisher: Continuous Mortality Investigation Limited (wholly owned by the IFoA)
- Doc type: public briefing note, 5 pp.
- URL: https://www.actuaries.org.uk/system/files/field/document/Final-IP11-Series-claim-inception-and-termination-rates-Briefing-note-v02-2021-04-28.pdf
- Retrieved: YES (curl; full text extracted and read).
- Content: authoritative public summary of the current UK individual-IP experience rates.
  Key facts extracted in the specifications section: dataset 2007–2016; rates split by
  sex, deferred period and CMI occupation class; naming convention
  IP11 {M/F} DP{d} OC{n} {Inc/Rec/Dth}; two-dimensional recovery and claimant-mortality
  rates; run-in periods; the April-2021 data-issue note (inception rates understated).
  Explicitly public — not subject to CMI subscriber terms.

### R2 — IFoA/CMI, "Income protection investigation" (web page)
- Publisher: Institute and Faculty of Actuaries (actuaries.org.uk)
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/income-protection-investigation
- Retrieved: YES (fetched and read).
- Content: the investigation tracks claim inceptions and terminations (recovery or death)
  since 1975, with occupation-class data from 1991. IP11 (finalised September 2020,
  2007–2016 data) is the most recent completed graduation. Data issues affecting the claim
  inception rates were subsequently discovered; adjustment spreadsheets accompany Working
  Paper 136. Also references WP203 (2021–2023 results), WP149 (data issues), WP120 (IP06)
  and WP72/96 (cause-of-sickness analyses). Most outputs are restricted to CMI Authorised
  Users.

### R3 — CMI Working Paper 136, "Final 'IP11' claim inception and termination rates for individual income protection experience" (landing page)
- Publisher: Institute and Faculty of Actuaries
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-working-papers/income-protection/cmi-working-paper-136
- Retrieved: YES (landing page fetched and read; the working paper itself is restricted to
  CMI Authorised Users — not retrieved).
- Content: WP136 (September 2020, updated March/April 2021) presents the final IP11 Series
  rates from 2007–2016 data, summarises feedback on the WP131 proposals, and is
  accompanied by a spreadsheet of indicative adjustments for the inception-rate data issue
  (terminations unaffected) and the CMI IP Rate Table Tool. The public briefing note (R1)
  is the only unrestricted output.

### R4 — CMI Working Papers 5, 6, 7, 46, 47 and 48 — IPM 1991-98 graduations (landing page)
- Publisher: Institute and Faculty of Actuaries
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-working-papers/income-protection/cmi-5-6-7-46-47-48
- Retrieved: YES (landing page fetched and read).
- Content: confirms the CMI produced graduations of individual IP sickness inception and
  termination experience "using the multiple state model approach described in CMIR 12",
  based on male occupation-class-1 lives, 1991–98 ("IPM 1991-98"). WP5 (2004) covers claim
  recovery and mortality intensity graduations; WP6 date-related features 1975–1998; WP7
  terminations for other occupations/females/group; WP46/47/48 (2010) the inception-rate
  graduations and overview. CMIR 12 is the CMI report "The Analysis of Permanent Health
  Insurance Data" (1991/92) that introduced the healthy–sick–dead multiple-state model for
  UK PHI [the CMIR 12 report itself was not retrieved — title and date per search-result
  summaries, [unverified]]. Historically, before CMIR 12, UK sickness experience was
  analysed on the Manchester Unity (friendly society sickness-rate) basis, and IP reserving
  contrasted inception-rate/disabled-annuity methods with the multi-state approach
  [unverified — textbook general knowledge, no public IFoA source retrieved].

### R5 — IFoA/CMI, "CMI Income Protection Rate Table Tool" (web page)
- Publisher: Institute and Faculty of Actuaries
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/income-protection-investigation/cmi-income-protection-rate-table-tool
- Retrieved: YES (fetched and read).
- Content: spreadsheet tool for deriving claim inception and termination rates and "other
  factors required for" profit testing, valuations and experience analysis — including
  decrement rates, continuance probabilities and claim annuity values — incorporating the
  IP11 rates and earlier graduations published as formulae. Subscriber access; the page
  repeats the IP11 inception-rate data-issue warning (WP136/WP149).

### R6 — FSMA 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1 Part II
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Retrieved: YES (fetched and read).
- Content: Class IV "Permanent health": "contracts of insurance providing specified
  benefits against risks of persons becoming incapacitated in consequence of sustaining
  injury as a result of an accident or of an accident of a specified class or of sickness
  or infirmity, being contracts that — (a) are expressed to be in effect for a period of
  not less than five years, or until the normal retirement age for the persons concerned,
  or without limit of time; and (b) either are not expressed to be terminable by the
  insurer, or are expressed to be so terminable only in special circumstances mentioned in
  the contract." This is why UK individual IP is long-term insurance business (minimum
  5-year terms and non-cancellable by the insurer) rather than general/annually-renewable
  accident & sickness business.

### R7 — PRA Rulebook — Technical Provisions Part
- Publisher: Prudential Regulation Authority (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Retrieved: YES (page payload downloaded via curl; rule text read from the embedded
  content — the site blocks plain fetches).
- Content: verified rule 3.1 wording that the best estimate "corresponds to the
  probability-weighted average of future cash-flows, taking into account the time value of
  money (expected present value of future cash-flows) using the relevant risk-free interest
  rate term structure"; technical provisions = best estimate + risk margin. For an IP cash
  flow model this defines the target output: BEL cash flows for both active lives
  (premiums, future claim incidence) and claims in payment (disabled-life annuity
  projections of benefit outgo with recovery/death terminations). Fuller annotation in the
  shared library [regulatory-actuarial.md R1].

### R8 — PRA Rulebook — Matching Adjustment Part (definition of "eligible element")
- Publisher: Prudential Regulation Authority (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/matching-adjustment
- Retrieved: YES (page payload downloaded via curl; definitions text read from the
  embedded content).
- Content: verified the definition: "eligible element means a portion of insurance or
  reinsurance obligations forming part of a wider contract of insurance or reinsurance
  contract and which: (1) comprises: (a) the guaranteed element of a with-profits policy
  that is either an immediate annuity or a deferred annuity; or (b) the in-payment element
  of a group death in service dependants' annuity or an income protection policy, in each
  case, where the element can be organised and managed separately in accordance with
  regulation 4(6) of the IRPR regulations...". I.e. under Solvency UK the claims-in-payment
  element of IP business can qualify for a Matching Adjustment portfolio even though the
  whole contract does not. See also [regulatory-actuarial.md R2].

### R9 — FCA Handbook, ICOBS — Insurance: Conduct of Business sourcebook
- Publisher: Financial Conduct Authority (handbook.fca.org.uk)
- URL: https://handbook.fca.org.uk/handbook/ICOBS/1/1.html
- Retrieved: NO in this pass (the handbook site is JavaScript-rendered; direct fetch and
  PDF-export URLs returned navigation shells only). fetched_ok = false here.
- Content (via the shared library, where ICOBS 1.1 was read via browser in the same
  session [regulatory-actuarial.md R11]): ICOBS applies to the distribution, effecting and
  carrying out of non-investment insurance contracts; a "pure protection contract"
  (term assurance, standalone CI, income protection) is conducted under ICOBS rather than
  COBS even though IP is long-term (Class IV) insurance business prudentially.

### R10 — FRC, Technical Actuarial Standards TAS 100 (v2.0) and TAS 200: Insurance (v2.0)
- Publisher: Financial Reporting Council (frc.org.uk)
- URLs: https://www.frc.org.uk/library/standards-codes-policy/actuarial-policy-technical-actuarial-standards/
- Retrieved: NO in this pass. fetched_ok = false here; both standards were fetched and
  verified in the shared library [regulatory-actuarial.md R33, R34].
- Content (per shared library): TAS 100 sets principles for all UK technical actuarial
  work; TAS 200 adds insurance-specific provisions (assumptions, models, communication)
  that apply to IP pricing, reserving and experience analysis performed by UK actuaries.

---

## Extracted specifications

### 1. Product architecture

- UK individual IP is written as long-term insurance (RAO Class IV "Permanent health"):
  contracts must run at least five years or to normal retirement age and be non-cancellable
  by the insurer except in contract-specified special circumstances [R6]. All six sampled
  products satisfy this: minimum 5-year terms are explicit at Aviva [S2], LV= [S4], The
  Exeter [S9], Cirencester [S11], Royal London (5–52 year IP term band) [S6].
- Distribution/conduct is under FCA ICOBS as a pure protection contract [R9,
  fetched_ok=false — see note]; prudential valuation under Solvency UK technical provisions
  [R7]; the in-payment claims element is MA-eligible [R8].
- Two structural families in the sample:
  - **Proprietary/mutual insurer products** (Aviva Income Protection+ [S1], LV= Income
    Protection / Budget IP [S3][S4], Royal London Personal Menu Plan IP [S5], Vitality
    Personal Protection Plan IP Cover [S10], The Exeter Income First [S7]) — monthly benefit
    chosen in £, financially underwritten at claim against a banded percentage of pre-tax
    earnings.
  - **Holloway-style friendly society contract** (Cirencester Friendly Income Assured
    Enhanced [S11][S12]) — benefit bought in units (£10.50/week per unit), age-costed
    premium table, optional participation in society surpluses accumulating a capital sum
    ("Member's Credit" with Surplus Allocation / Bonus Allocation / discretionary Terminal
    Bonus on the advice of the With-Profits Actuary) [S11][S12].
- All products include waiver of premium during claim as a standard feature (mechanics
  vary; see §13) [S1][S3][S5][S7][S10][S11].
- No product in the sample has a cash-in/surrender value ([S4] "no cash in value at any
  time"; [S5] cash-in value section: none; [S7] "no cash-in value"), except the Cirencester
  capital-sum option, which returns the accumulated Member's Credit (less early-closure
  penalty) [S11].

### 2. Eligibility and issue ages

- Aviva: ages 18–59 at acceptance; working (employed or self-employed) for the past 12
  months with earnings evidence; resident and entitled to live/work in UK, Channel Islands,
  Isle of Man or Gibraltar; registered with a UK/CI/IoM/Gibraltar doctor for 2 years (or 2
  years' medical history available) [S1][S2].
- LV=: ages 17–59; permanently living in the UK; UK resident for the last 2 years;
  registered with a UK doctor for 2 years; cover not offered to Jobseeker's Allowance
  claimants [S3 App][S4].
- Royal London: minimum age 18, maximum age at start 59 (IP); person covered [S6].
- The Exeter (Income One Plus era): 18–59 inclusive; UK resident and registered with a UK
  NHS GP for the last 3 years; working ≥15 hours/week employed or self-employed; policy
  must start ≥5 years before the chosen finishing age [S9].
- Vitality: entry-age limits for IP Cover are not stated in the plan provisions extract
  (they sit in adviser literature) — gap; houseperson category exists for
  students/retired/under-16-hours workers at claim [S10].
- Cirencester Friendly: age 16 to before the 60th birthday; at least 5 years between start
  and end date; UK resident; 3 years' medical history from a UK doctor; employed or
  self-employed earning ≥£4,550/year or working ≥16 hours/week (or bona fide houseperson);
  earnings taxable in the UK; not awaiting medical tests [S11].

### 3. Policy term and expiry ages

- Aviva: term 5–52 years; cannot end before age 50 nor continue past the 71st birthday
  [S2].
- LV=: minimum 5 years; must end before age 70 [S4].
- Royal London: IP term band 5–52 years; maximum age when cover ends 70 (IP; higher bands
  in the table apply to other menu covers) [S6]. Incapacity definitions apply "before age
  70"; a living-tasks definition applies if cover goes past 70 [S5][S6].
- The Exeter: finishing date is a selected age between 50 and 70 [S7][S9].
- Vitality: cover ends at the schedule "date of expiry" less the deferred period (e.g. a
  3-month deferred ends cover 3 months before expiry) [S10 B4.11]. Numeric expiry-age
  limits not in the provisions (gap).
- Cirencester: end date = selected retirement age 50 to 70, "or state retirement age,
  whichever is higher"; may be amended (≥5 years remaining) and extended by up to one year
  twice [S11]. This is the only sampled product with an explicit State Pension age link.

### 4. Benefit amounts and earnings-replacement formulas

Chosen monthly benefit, capped at claim by a "maximum benefit" formula applied to pre-tax,
pre-incapacity earnings (last 12 months; 3-year averaging for volatile earnings at Royal
London [S5]):

| Insurer | Replacement formula | Absolute cap |
|---|---|---|
| Aviva | 65% of first £60,000 of gross yearly earnings + 45% above | £20,000/month = £240,000/year (can exceed via increasing cover) [S1][S2] |
| LV= | 60% of income (flat) | £20,833/month level; £14,583/month inflation-linked [S3 B5][S4] |
| Royal London | 65% of first £60,000 + 50% above | £250,000/year incl. all other IP [S5][S6] |
| The Exeter Income First | 65% of first £60,000 of personal taxable income + 45% above | benefit range £500–£10,000/month [S7] |
| The Exeter Income One Plus (2019) | 60% of first £100,000 + 40% above | £500–£10,000/month [S9] |
| Vitality | 60% of first £5,000/month (=£60,000/yr) + 50% of £5,000–£15,000/month | £16,666/month; verified earnings capped £15,000/month → £8,000/month benefit without further evidence [S10 B4.2] |
| Cirencester | 60% of gross earnings (salary+P11D, or pre-tax profits; directors' dividends includable) | 75 initial units = £40,950/year; minimum 5 units = £2,730/year [S11] |

- Minimum cover: Royal London £100/month [S6]; The Exeter £500/month [S7][S9]; Cirencester
  5 units (£52.50/week) [S11].
- Earnings definitions consistently: employed = pre-tax PAYE earnings incl. P11D benefits
  in kind (Aviva caps BIK at £10,000 taxable value: company car, accommodation, PMI [S1]),
  regular bonus/commission; self-employed = pre-tax profit share; directors of private
  limited companies may count dividends subject to conditions (Aviva [S1]; Royal London —
  company with ≤3 other shareholders employed as full-time working directors [S5];
  Cirencester — same ≤3-shareholder test [S11]; LV= — dividends from current-year profits
  related to work activities [S4][S3]).
- Royal London "Fixed Costs Flexibility": self-employed pre-incapacity earnings may include
  the insured's share of continuing fixed business costs (regulatory/contractual payments,
  loans on business assets), while the insured remains liable for them [S5].
- Benefit-fixing options: The Exeter fixed benefit option — fix up to £7,500/month (Income
  First, no extra cost, evidence within 6 months of start; claim criteria: under 55,
  working ≥30 h/week) [S7]; Income One Plus generation: fix 75% of initial benefit
  (evidence within 12 months) or optional Minimum Benefit Guarantee £1,000/month on
  2-year limited claim period (extra cost) [S9]; Vitality earnings verification in first 6
  months (employed: salary + bonus capped at 20%; self-employed: lesser of 3-year average
  and 120% of lowest year) [S10 B4.2].

### 5. Deferred / waiting periods

| Insurer | Menu | Notes |
|---|---|---|
| Aviva | 4, 8, 13, 26, 52, 104 weeks | dual deferred period available (partial benefit after first, full after second); not with reviewable premiums [S1][S2] |
| LV= | 1, 2, 3, 6, 12 months (1–2 months occupation-dependent) | "waiting period" terminology [S4] |
| Royal London | 4, 8, 13, 26, 52 weeks | NHS medical professionals with 52-week deferred: benefit starts when sick pay halves, per service table [S5][S6] |
| The Exeter | Day 1 (payable after 3 consecutive days, backdated), 1, 4, 8, 13, 26, 52 weeks | level guaranteed premiums only for ≥4 weeks; flexible waiting periods for NHS staff and teachers with 52-week choice [S7][S9] |
| Vitality | 7 days (self-employed only), 1, 2, 3, 6, 12, 24, 60 months | dual deferred available; public-sector deferred aligns with NHS/council/teacher sick pay if 12-month deferred chosen [S10 B4.1, B4.10] |
| Cirencester | 1, 4, 8, 13, 26, 52 weeks | plus optional Day One Accident Protection (accident claims from day 1) [S11] |

- Benefit is paid monthly in arrears from the end of the deferred period (first payment ~1
  month later), with daily pro-rating of partial months (Aviva [S1], LV= worked example
  [S3 B3], Vitality day-count formula [S10 B4.2]); Cirencester pays fortnightly on the 8th
  and 23rd [S11].
- Claim notification deadlines scale with the deferred period: Aviva — before 8 weeks of
  incapacity or before the deferred period ends if shorter [S1] (summary: two months, or
  one month for the 4-week deferred [S2]); LV= — 2 weeks (waiting period ≤2 months) or 8
  weeks (≥3 months), late notice restarts the waiting period [S3 B1]; The Exeter — 2 weeks
  (Day 1–4 weeks), 4 weeks (8–13 weeks), 8 weeks (26–52 weeks) [S7]; Vitality — immediate
  (7-day), 2 weeks (1–2 months), 1 month (3 months), 2 months (6–60 months); notice >90
  days after deferred-period end may be declined [S10 B4.1]; Cirencester — 7 days' notice
  (Day One/≤4-week deferred) or within 1 calendar month (longer deferred) [S12 D2].
- NHS sick pay structure (context for deferred choice): builds to 6 months' full pay + 6
  months' half pay after 5 years' service [S2]; full service tables reproduced at Royal
  London [S5], The Exeter [S7] and Vitality (incl. teachers England/Wales/NI in working
  days, teachers Scotland, council employees under the Green Book) [S10 B4.10].

### 6. Incapacity definitions

- **Own occupation is the standard primary definition at all six insurers**:
  - Aviva: inability, caused by illness or injury, to perform the duties of each and every
    occupation followed in the 12 months before the illness/injury (occupations <10 h/week
    ignored); "duties" = material and substantial activities that cannot reasonably be
    omitted or modified [S1 defs].
  - LV=: unable to carry out the "main tasks" of your occupation and not doing any other
    paid or unpaid work [S3 A1].
  - Royal London: loss of physical or mental ability, before age 70, to do the material and
    substantial duties of the own occupation [S5].
  - The Exeter: total inability to work in the own occupation; claims always assessed
    against own occupation regardless of occupation class [S7][S9].
  - Vitality: unable to perform the material and substantial duties of the own occupation
    and not working in any other occupation [S10 B4.1].
  - Cirencester: "Own Occupation Disabling Illness" — unable to perform the Material and
    Substantial Duties of the Occupation(s), not following any other occupation or activity
    whatsoever [S12 Part A]. The KFD also offers an **Own/Own Suited** variant (own
    occupation for the first 52 weeks of claim, then any occupation suited by training,
    education or experience) and states that under the pure Own Occupation choice the
    regular benefit reduces to 75% of initial entitlement after 52 weeks and 50% after 104
    weeks [S11 §9] (not present in the older Schedule V3a — see Gaps).
- **Fallback definitions for those not in (full) work**:
  - LV= homemaker cover: unable to prepare a meal or do basic housework [S3 A2]; applied
    when out of work >30 days at claim (2024 conditions [S3]; the 2019 KFD said 12 months
    [S4] — edition difference).
  - Royal London three-tier: not in full-time work (>16 h/week) → "Serious Illness"
    definition (blindness 3/60, cancer on chemo/radiotherapy within 3 months, complete
    dependency, deafness >95dB, dialysis, organic brain disease — payable while unable to
    work in any capacity); not in paid occupation at all → "Everyday Tasks" (failing 3 of
    9: sitting 30 min, standing 5 min, walking 200 m, climbing 12 stairs, lifting 2 kg,
    bending, getting in/out of a car, holding an ordinary UK driving licence on medical
    grounds, writing/typing) [S5]. Own occupation preserved for 3 months after redundancy /
    between jobs [S5].
  - Vitality: houseperson category (houseperson, student, retired, working <16 h/week,
    unemployed >1 month) assessed on failing 3 of 6 activities of daily living; benefit
    capped £1,500/month plus £100/child (max £300 or 20% of benefit) [S10 B4.6].
  - The Exeter: unemployed (>3 months) assessed on ability to go outdoors unassisted and
    seek employment; houseperson on inability to perform normal household duties, and must
    evidence increased household costs [S7].
  - Aviva restricted benefit: not working before incapacity → benefit for a maximum of 12
    months over the policy term, assessed on the occupation of the 12 months before work
    stopped [S1].
  - Cirencester Houseperson Disabling Illness: confined to home or hospital and totally
    unable to perform houseperson functions; benefit capped £2,730/year [S11].
- **Terminal illness**: Royal London pays without the deferred period if death is expected
  within 12 months (first unequivocal diagnosis, confirmed by chief medical officer)
  [S5]; Cirencester pays a one-off Terminal Illness Benefit of six months' benefit as a
  lump sum, plus benefit continuing normally [S11][S12 Part I].

### 7. Benefit payment terms (full term vs limited)

- Aviva: "full cover to term" or "limited payment term" of 24 months per incapacity; after
  a full 24 months, a claim for the same illness requires 6 consecutive months back at
  work; with dual deferred, max 24 monthly payments per claim; unlimited number of claims
  either way [S1][S2].
- LV=: full-term product, or **Budget Income Protection** with claim limit 12 or 24 months
  per claim (guaranteed premiums; reviewable premiums only 24 months); same-cause re-claim
  requires 6 months back at work; a homemaker who exhausts the claim limit has the policy
  cancelled [S4].
- Royal London: cover payment period options — throughout the term, or 1, 2 or 5 years
  [S6]; connected-claim interaction: remaining balance of the payment period can be used if
  return to work occurred before it ended; after a fully-used payment period, 26 continuous
  weeks back at work are needed before a connected claim [S5].
- The Exeter: standard full term to finishing date, or limited claim period of 2 or 5 years
  per individual claim (multiple claims for different causes allowed; limited claim periods
  run from the end of each claim's waiting period and may overlap) [S7][S9].
- Vitality: full payment term, or Short Payment Term of 12, 24 or 60 months; four
  enumerated subsequent-claim scenarios (linked within 6 months → deferred waived, shared
  payment-term budget; same condition after 6 months without 6 months back at work →
  deferred applies, shared budget; same condition after 6 months back at work → fresh
  payment term; unrelated condition → deferred applies, fresh payment term) [S10 B4.4].
- Cirencester: full term only (no limited payment option), but under the KFD's Own
  Occupation definition the benefit itself tapers to 75% after 52 weeks and 50% after 104
  weeks of claim [S11].
- Payments stop on: recovery/ceasing to meet the definition, no further loss of earnings,
  end of limited payment term, policy end date, death (all products) [S1][S3][S5][S7][S10];
  also non-compliance with medical advice/treatment (LV= [S3], The Exeter [S7], Vitality
  [S10]), custody/imprisonment (Aviva — retrospective payment if acquitted [S1]), starting
  any work incl. voluntary (Cirencester [S12 D5.5]).

### 8. Minimum benefit guarantees

Protection against earnings having fallen since outset (all conditional on working a
minimum number of hours at incapacity):

- Aviva benefit guarantee: pay the chosen benefit up to £1,500/month in full; above that,
  pay in full if the maximum yearly amount ≥90% of the benefit amount; else pay the higher
  of £1,500/month and the maximum yearly amount. Requires ≥16 h/week work [S1][S2].
- LV=: £1,500/month guarantee (less other insurance payments and 60% of continuing
  income); requires ≥16 h/week (self-employed) or ≥25 h/week (employed); doctors and
  surgeons £3,000/month [S3 B5/B7][S4]. Plus a 10%-of-cover over-insurance tolerance
  [S3 B5][S4].
- Royal London: minimum £1,750/month (non-doctors) or £3,500/month (doctors/surgeons) in
  the benefit formula; 90% tolerance (pay full cover if maximum benefit ≥90% of cover)
  [S5].
- Vitality Earnings Guarantee: lesser of £1,500/month (doctors/surgeons £3,000) and the
  benefit amount, if employed ≥30 h/week or self-employed ≥20 h/week; indexed if
  indexation chosen [S10 B4.2].
- The Exeter: fixed benefit option (S7, §4 above) plays this role; Income One Plus offered
  an explicit £1,000/month Minimum Benefit Guarantee on the 2-year limited claim period
  [S9].
- Cirencester: Minimum Benefit Guarantee of up to £1,500/month where evidenced earnings
  cannot support the chosen benefit [S11].

### 9. Offsets — continuing income deducted at claim

- Aviva deducts from the maximum yearly amount: continuing business income (incl. earned
  dividends), continuing employer income (incl. sick pay and benefits in kind), pensions
  paid due to incapacity (excl. lump sums), any income received because of the
  illness/injury (excluding state benefits), and regular payments from other insurance
  (income protection/PHI, mortgage/credit/loan/pension premium protection) where they
  exceed £50/month in total; taxable income is deducted net [S1].
- LV= deducts: 100% of other accident & sickness insurance payments; 60% of sickness
  benefit or ill-health retirement payments; 60% of continuing income or pension payments
  [S3 B5].
- Royal London deducts other replacement insurance and continuing
  employment/self-employment income, to bring total income down to the maximum annual
  benefit (subject to the £1,750/£3,500 floors and 90% rule) [S5].
- The Exeter deducts: taxable employer payments (company sick pay but not SSP), continuing
  business income/dividends, pension payments (unless already received before the policy
  started), and similar insurance benefits [S7].
- Vitality deducts: benefits under other incapacity insurance (incl. MPPI); 60% of
  continuing salary/wages/fees/dividends/commission from employment or business; ill-health
  early-retirement pension net of tax/NI. Explicitly NOT deducted: state benefits,
  non-employment dividends, rental income, waiver-of-premium benefits [S10 B4.2].
- Cirencester deducts continuing income from paid work, other providers' IP/insurance
  payments, and ill-health early-retirement pensions; investment income is not deducted
  unless earned in the course of the occupation [S11].
- State benefits: universally not deducted ([S3 B6][S4][S7 "State benefits"][S9][S10]),
  but insurer payments can reduce means-tested Universal Credit — LV= offers a "Pay my
  mortgage" facility paying the lender directly so the benefit is not means-tested
  [S3 B6][S4]; Royal London repeats the UC warning [S5].

### 10. Proportionate and rehabilitation benefits (partial return to work)

All six products pay a reduced benefit on partial return to work, on the common formula
reduced benefit = (pre-claim income − new income) / pre-claim income × benefit in payment:

- LV= B9 (part-time return to own occupation: return <30 h/week having worked ≥30 h/week)
  and B10 (different occupation because unable to do the original); 52-week window to
  restart payments if new-job income later falls for the same medical cause [S3].
- Royal London: same formula and 30-hour conditions; separately a **Back to Work Payment**
  after the claim ends — 25% of the last monthly amount one month after return and 10% two
  months after (covers with a payment period), or 50%/25% (full-term covers); only for
  deferred periods 13/26/52 weeks [S5].
- The Exeter: "rehabilitation benefit" (same occupation part-time) and "proportionate
  benefit" (different occupation), formula (A−B)/A × C on financially-assessed amounts;
  worked example pays £500/month on 50% earnings loss from a £1,000 benefit [S7].
- Vitality: rehabilitation benefit (own occupation, reduced extent) and proportionate
  benefit (different occupation, lower earnings), same three-step formula on
  verified/pre-incapacity earnings [S10 B4.7]; Income Boost also applies to these [S10].
- Aviva: "back to work benefit" — percentage of full benefit equal to the percentage
  reduction in earnings, RPI-adjusted between incapacity start and payment [S1].
- Cirencester: "Recovery Benefit" on phased return or alternative occupation, calculated on
  the new earnings (Parts G/H of the Schedule) [S11][S12].

### 11. Linked / recurring claims

Recurrence of the same cause within a window restarts payment without a new deferred
period:

- Aviva: 12 months from end of the previous claim (full cover to term); detailed
  limited-payment-term rules (remaining months usable; fresh 24-month term after 6 months
  back at work) [S1].
- LV=: 6 months from return to work, same illness and same occupation, notified within 2
  weeks [S3 B11][S4].
- Royal London: "connected claims" — 52 weeks from payments stopping, same cause, same
  occupation, not having returned against doctor's advice [S5].
- The Exeter: 6 months, same illness/injury (both full-term "linking claims" and limited
  claim period variants); returning against medical advice voids it [S7].
- Vitality: 6 months from benefit payments ending, same condition [S10 B4.8].
- Cirencester: 52 weeks from return to work, same condition → benefit paid immediately
  [S11].

### 12. Escalation (indexation) — pre-claim and in-claim

- Aviva increasing cover (optional, at outset): RPI (12-month change, capped 10%/yr), or
  fixed 3% or 5%; premium rises by 1.5× the benefit increase (so RPI-linked premium
  increases cap at 15%; 4.5%/7.5% for the fixed options); no change if RPI ≤0; increases
  continue during claim [S1][S2].
- LV= inflation-linked cover: RPI (12 months to 3 months before anniversary); premium
  increases at inflation ×1.5; in-claim increases capped at 12%/yr; insurer may stop
  increases once cover exceeds 3× the initial amount (not while in claim) [S3 C1]
  (index = RPI per definitions [S3 defs]).
- Royal London increasing cover: fixed rate 2–5% or RPI with minimum 2% and maximum 10%;
  premium increases at the escalation rate ×1.2; two consecutive cancelled increases end
  the option; cover stops increasing at £250,000/yr [S5][S6].
- The Exeter Income First: indexation on CPIH (rate 4 months before anniversary), benefit
  increase capped 10%/yr, applies in claim; with level guaranteed premiums the premium
  rises at CPIH ×1.5 capped 15%/yr; with age-costed options premiums rise by CPIH on top
  of age-related increases [S7]. (Income One Plus 2019 guide quoted RPI max 10% [S9].)
- Vitality: RPI rounded up to next 0.25%, min 0% max 10%; premium increase is RPI +1.5%
  (RPI ≤1.75%), RPI +2.5% (2–7.75%) or capped-RPI +3.5% (≥8%); increases continue in
  claim (applied on claim anniversaries using RPI five months prior) with post-claim
  catch-up [S10 B4.2].
- Cirencester: indexation option on CPI, capped 10%/yr; applies in claim (increase takes
  effect after the review date plus deferred period); the Society may reduce cover and
  premiums if the index falls; declining 3 consecutive increases removes the option
  [S11][S12 Part F].

### 13. Premium structures and guarantees

- Payment: monthly Direct Debit universally (Aviva monthly-only [S1]; LV= DD-only, premiums
  payable to one month before end date less the waiting period [S3 C5][S4]; Royal London
  monthly or yearly [S5]; Cirencester monthly, collected 6th/18th [S11]).
- Grace periods / lapse: Aviva 60 days then cancellation (unpaid premium deducted from any
  claim) [S1]; LV= 60 days, reinstatement possible within 6 months of first missed payment
  with health questionnaire and arrears [S3 C6–C7]; Royal London 5 weeks overdue → plan
  cancelled; formal payment pause option up to 3 months (once, repayable over 6/12/24
  months, outstanding amounts deducted from claims) [S5]; The Exeter: 2 months missed →
  cancelled [S7]; Cirencester: 4 months in arrears → contract closed [S11].
- **Guaranteed premiums**: Aviva — level unless policy changed / increasing cover / global
  treatment [S1]; LV= — guaranteed; changeable only for tax/legislation/court-decision
  reasons, with 60 days' notice and the option to hold premium and cut cover [S3 C8];
  Royal London — level cover premiums "won't change" [S5]; The Exeter level guaranteed
  [S7]; Vitality guaranteed (but see Optimiser below) [S10 D2].
- **Reviewable premiums**: Aviva — 5-yearly reviews, assumption-based (medical trends,
  industry experience, legislation/tax, claims costs), no limit on changes, <2%-or-50p
  changes ignored, option to hold premium and reduce benefit [S1]; LV= — no change in the
  first 5 years, then annual reviews (KFD) [S4]; Royal London — "reviewable after 5 years"
  option [S6]; Vitality — first review at the 5th anniversary, then annually, but a changed
  premium is then fixed for 5 years; no limit on the size of change [S10 D3.3].
- **Age-costed premiums** (recalculated each year with attained age from a schedule fixed
  at outset): The Exeter age-costed guaranteed (rates guaranteed; schedule of future
  premiums provided) and age-costed reviewable (rates reviewable after policy year 3, any
  amount, 30 days' notice) [S7][S9]; Cirencester premiums are age-costed by design
  ("based on your age when you join or the age you attain each year") with guaranteed
  rates [S11].
- **Vitality health-linked pricing**: with Optimiser the initial premium starts lower and
  is adjusted every anniversary by Vitality Status — Bronze +2.5%, Silver +1.5%, Gold
  +0.5%, Platinum no change — on top of indexation/review changes [S10 E2]; guaranteed
  premiums can still vary via Vitality Status [S10 D2.1].
- Minimum premiums / charges: LV= minimum £5/month including a £3/month administration
  charge (reducible for multi-policy plans) [S4]; Royal London minimum £5/month or
  £60/year for the plan, including the plan charge [S6]. Cirencester underwriting quirk: a
  5% base-premium discount per applied exclusion for back disorders or mental illness (max
  10%) [S11].
- **Waiver of premium** (of the IP premium itself): Aviva — premiums paid by insurer from
  the earlier of deferred-period end and 13 weeks of incapacity [S1]; Royal London /
  The Exeter / Vitality / Cirencester — premiums waived while benefit is paid (Exeter and
  Cirencester: premiums payable only during the waiting/deferred period)
  [S5][S7][S10 B4.9][S11]; Vitality also waives during the deferred period for up to 3
  months while a Recovery Benefit pathway is used [S10]; LV= is the outlier — premiums
  remain payable during claim, with waiver available as a separate Waiver of Premium
  policy in the Flexible Protection Plan [S3 C5][S4]; LV= instead pays up to 6 months of
  premiums during involuntary unemployment (90-day initial exclusion) [S3 B15]; The Exeter
  similarly offers a redundancy premium holiday of up to 3 months (after 6 months in
  force; 12-month gap between uses) [S7].

### 14. Guaranteed insurability / increase options (no further medical underwriting)

- Aviva "life change benefit" (standard-terms policies only): events — marriage/civil
  partnership, divorce/dissolution, separation, becoming a parent, mortgage
  increase/house purchase/home improvements, rent increase or new rental, change of
  employer or promotion; per event max = lower of 50% of original benefit and £9,000/yr,
  via a new policy; salary increase ≥20% since outset → one-off increase up to £20,000/yr
  (employed only); take-up before age 55, new policy must end before 71, within 90 days of
  the event, not within 5 years of the end date, not while claiming [S1].
- LV= Guaranteed Increase Options: rental increase, mortgage increase (move/improvement),
  marriage/civil partnership, childbirth/adoption, basic salary increase ≥10%
  (promotion/qualification/job change; employed only) — each up to 50% of original cover,
  max £10,000/yr, age ≤54, within 3 months; "significant career progression" (salary
  +≥20%): once, up to £20,000/yr; lifetime GIO total £35,000/yr; if not working, cover
  capped £18,000/yr (£1,500/month) [S3 C2].
- Royal London Cover Increase Options (standard terms): marriage/divorce, first mortgage,
  rent increase, mortgage increase, birth/adoption, salary increase; within 6 months,
  person covered under 60; per event max = lowest of half original cover, maximum annual
  benefit less current cover, £12,000/yr (rent event also capped at 12× the monthly rent
  increase); lifetime total £24,000/yr; not available while claiming or within 12 months
  of a claim ending [S5].
- The Exeter guaranteed insurability option: Income First — up to 50% of original benefit
  or £833.33/month per event (marriage, birth/adoption, new/increased mortgage,
  divorce/dissolution/separation, rent increase, earnings increase); within 3 months;
  policy ≥6 months old; age <55; working ≥15 h/week; total ≤£10,000/yr or 50% [S7];
  Income One Plus generation: 20% or £500/month, also exercisable on every 3rd policy
  anniversary [S9].
- Cirencester: increase up to 10% of current benefit per lifestyle event
  (marriage/civil partnership, birth/adoption, earnings increase, new/increased mortgage),
  within 60% of income, plus an increase option on every 5th anniversary [S11]; the
  Schedule caps event increases at 20% of current Sick Pay within 60% of Earnings
  [S12 B] (edition difference — see Gaps).
- Vitality: no GIO extracted from the plan provisions IP section (not part of B4) — any
  such option sits elsewhere in adviser literature (gap).

### 15. Additional / ancillary benefits

- Fracture cover:
  - Aviva (optional): 18-bone schedule £2,000–£6,000 (e.g. skull/pelvis/leg/knee/ankle
    £6,000; arm/wrist/vertebra £4,000; jaw £3,000; others £2,000); one claim per policy
    year; excludes stress/hairline/avulsion/chip/micro fractures and listed sports
    (mountain biking/BMX, boxing/cage fighting/martial arts, rugby/Gaelic football, horse
    riding, motorcycle sport/off-road) [S1].
  - LV= (built in): schedule £650–£2,200 (open skull/upper leg/knee £2,200; closed
    skull/pelvis/lower leg/arm/ankle £1,250; most others £1,000; ribs/collar bone £650);
    one fracture per 12-month period; longer excluded-sports list incl. skiing/
    snowboarding, climbing, flying sports [S3 B13].
  - Royal London (built in): schedule £1,000–£4,000 (open skull/upper leg/knee £4,000);
    max two claims over the term; multiple simultaneous fractures capped £4,000 [S5].
- Hospitalisation benefit (during the deferred period): £100/night after 6 consecutive
  nights, max 90 nights — Aviva (per policy term) [S1], Royal London [S5], Vitality (from
  the 7th night; cash cap £9,000) [S10]. Royal London adds Child Hospitalisation on the
  same terms per child [S5].
- Death benefits: LV= £5,000 if death within 4 years of start, £10,000 after 4 years (max
  £10,000/person; in-claim overpayments deducted) [S3 B14][S4]; Royal London Additional
  Payment on Death £10,000 [S5].
- Trauma/serious-injury lump sums: Aviva trauma benefit — 6× monthly benefit capped
  £40,000, once per term, on blindness, deafness, loss of hand/foot, loss of speech,
  paralysis of limb, or loss of independence (3 of 6 ADLs) [S1].
- Children's benefits: LV= parent & child cover — 6× monthly cover capped £25,000 per
  child per policy on ~specified child illnesses [S3 B16][S4]; Royal London Child Illness
  (6× monthly benefit capped £25,000; per-child, per person covered; £50,000 overall for
  two covered parents) & Child Loss £5,000 [S5]; Vitality pays £100/month per dependent
  child (max £300 or 20%) during houseperson claims [S10 B4.6]; separate Child Serious
  Illness Cover exists in the Vitality menu [S10 C1].
- Occupation-specific sick-pay guarantees: Aviva NHS special arrangements (52-week
  deferred; benefit from when NHS sick pay reduces; no benefit if incapacity <4 weeks)
  [S1]; LV= appendices for NHS dentists/doctors/surgeons and teachers (Burgundy Book /
  NI terms / SNCT) with 12-month waiting period [S3][S4]; Royal London NHS medical
  professionals [S5]; The Exeter NHS + teachers flexible waiting periods and an employer
  change promise (sick pay restricted in first year with a new employer → benefit can be
  paid from 4 weeks of illness; policy ≥3 years old) [S7]; Vitality public-sector deferred
  (NHS, councils, teachers) with linked deferred aggregation of broken sickness periods
  [S10 B4.10].
- Rehabilitation support services: LV= — up to 3× the amount of cover per claim on
  treatment/services (physio, psychological, return-to-work) [S3 B8]; Vitality Recovery
  Benefit — four clinical pathways (MSK, mental health, cancer, neuro/stroke), no monetary
  cap [S10]; Aviva Global Treatment (optional) — overseas treatment of six serious
  illness/procedure groups, £1m per 12 months / £2m lifetime, 3-year renewable, ends at 71
  [S1].
- Aviva "protection promise": free accidental-injury cover while underwriting is prolonged
  [S2]. Vitality Income Boost: benefit uplift for the first 6 months of claim by Vitality
  Status (Platinum 20%, Gold 15%, Silver 10%, Bronze 0%) [S10].

### 16. Exclusions

- Aviva, Royal London, The Exeter and LV= have **no standard illness exclusions** — only
  person-specific exclusions applied at underwriting and shown on the schedule
  ([S1] — exclusions only via policy schedule; [S5] — cover-summary exclusions plus
  intentional self-inflicted injury; [S7] "no standard exclusions on Income First";
  [S9]; [S3 A1] "no restrictions on the type of sickness or accident... unless we have
  told you"). Common non-covered situations (not illness exclusions): unemployment/
  redundancy, normal pregnancy/childbirth, lockdown/quarantine/suspension/custody
  restrictions on access to work (LV= [S3]), remand/custodial sentence (Aviva [S1]).
- Cirencester is the exception with a standard exclusion list: solvent/substance misuse,
  illegal drugs, alcohol misuse, pregnancy/childbirth, sterilisation (unless medically
  necessary), medically unnecessary operations incl. cosmetic surgery, criminal conduct,
  and motor-sports accidents [S11].
- Intentional self-inflicted injury excluded at Royal London [S5]; The Exeter excludes
  incapacity from self-elected, non-medically-required treatment [S7].

### 17. Alterations, breaks, cancellation, surrender

- Cooling-off: 30 days with full premium refund at all sampled insurers
  [S1][S4][S5][S7][S11]; thereafter cancellation any time, no refund, no cash-in value
  [S1][S4][S5][S7] (Cirencester: capital-sum option balance paid less penalty [S11]).
- Alterations menus: Aviva — decreases of benefit/term and deferred-period increases
  without underwriting; increases/decreased deferred/occupation change with underwriting;
  benefit increases issued as a new policy at current rates [S1]. LV= — change cover,
  waiting period, term or occupation via special application [S3 C3]; out-of-work cover
  reduction with 24-month restoration right [S3 C4]. Royal London — Lifestyle Flexibility
  (review of ratings/exclusions on improved lifestyle) and Job Flexibility (occupation /
  deferred-period changes); no duty to notify deteriorations after outset [S5]. The
  Exeter — change benefit, finishing date, waiting period, claim period, indexation; fixed
  benefit addable within 6 months [S7].
- Career breaks: Royal London — sabbatical/career break up to 12 months treated as still
  in work (job to return to; employed only; break starts ≥12 months into the policy)
  [S5]; The Exeter — short-term policy break (reduce benefit to as low as £500/month for
  up to 52 weeks, once, after year 4) and long-term policy break (cover suspended up to 3
  years at 10% of premium, reinstatement at attained-age premium) [S7]; Cirencester —
  premium suspension up to 12 months per break, 24 months lifetime, after 12 months'
  premiums; no cover while suspended but bonus interest continues on any Member's Credit
  [S11]; LV= doctors/surgeons sabbatical option [S3 App A].
- Assignment: Aviva policy not assignable [S1]; Royal London plans can be assigned or
  placed in trust (payment mechanics follow the deed) [S5]; Cirencester death benefit /
  contract not assignable [S3 B14 for LV=; S11].

### 18. Territorial limits

- Cover while abroad follows a permitted-country list with a payment limit outside it:
  Aviva — 37-country list (UK, EEA states, CI/IoM/Gibraltar, Australia, Canada, Hong
  Kong, NZ, Norway, Switzerland, USA); outside it, max 3 months' benefit after the
  deferred period [S1]. LV= — similar list (adds Iceland, Japan, Liechtenstein); max 26
  weeks outside; claims stop after 2-week visits to non-listed countries [S3 A1]. Royal
  London — assessment-country list; may require return to a listed country [S5]. The
  Exeter — UK-based product; EU + 10 listed countries, max 3 months, then must return to
  the UK [S7]. Vitality — full benefit in UK/permitted countries; elsewhere capped at 183
  days per 365 and 365 days in total [S10 B4.5]. Cirencester — UK contract; ends if the
  member habitually lives and works outside the UK; >8 weeks/year working abroad must be
  notified [S11].

### 19. Holloway friendly society variation (Cirencester)

- Unit pricing: 1 unit = £10.50/week of benefit; minimum 5 units (£2,730/yr benefit,
  requires earnings ≥£4,550/yr); maximum initial 75 units (£40,950/yr, requires earnings
  ≥£68,250/yr) [S11].
- Optional surplus participation ("option to accumulate a capital sum"): fixed additional
  premium; bonuses accrue from the second contract anniversary; not guaranteed (depend on
  investment performance, costs, claims); paid tax-free at the natural end of the
  contract; early-termination penalty 10%/8%/6%/4%/2% at 5/4/3/2/1 years before the
  selected retirement date [S11]. Machinery in the Schedule: Member's Credit account;
  annual Surplus Allocation (rate per unit) and Bonus Allocation (rate on the Member's
  Credit balance) declared by the Board on the advice of the With-Profits Actuary;
  interim rates possible; a member may commute the sick-pay right into "Commuted Bonus"
  only (capped at 100% of premiums paid); discretionary annual Terminal Bonus [S12 Parts
  M/N]. After two years of premiums a member may drop the IP cover and continue
  capital-accumulation only [S11].
- Benefit paid fortnightly; no work of any kind (including unpaid/voluntary) permitted
  while claiming [S11][S12 D5.5].
- FSCS treatment quoted in the KFD: 100% of an existing claim with no upper limit; 90% of
  unused premiums refundable [S11].

### 20. Tax and state benefits

- Benefits from individual IP paid from taxed personal income are free of income tax and
  CGT under current law (LV= [S4]; The Exeter — no tax or NI deducted [S7]; Cirencester —
  benefit "currently free from tax", which motivates the 60% ceiling [S11]).
- Benefit payments can reduce Universal Credit entitlement (means-testing), except
  payments routed directly to a mortgage lender (LV= "Pay my mortgage" facility) [S3 B6]
  [S4][S5].

### 21. Actuarial modeling frame (for the reference implementation)

- **Experience basis**: CMI IP11 Series (individual IP, 2007–2016 data): claim inception
  rates by sex, deferred period (DP1/4/13/26/52) and occupation class (OC1–OC4);
  claim termination rates split by recovery and death, two-dimensional in age and
  sickness duration (recovery rates show "run-in" periods of increasing rates at early
  durations for DP4/13/26; claimant mortality is duration-dependent to 5 years, age-only
  beyond); rates graduated for ages 17–65 (M) / 17–60 (F) and extended to age 70; table
  naming IP11 {M/F} DP{d} OC{n} {Inc/Rec/Dth} [R1]. Known issue: inception exposure
  errors understate IP11 inception rates; CMI published indicative adjustments alongside
  WP136 (terminations unaffected) [R1][R2][R3].
- **Model structure**: the CMI graduations are built on the multiple-state
  (healthy–sick–dead) model of CMIR 12, first applied to the IPM 1991-98 male OC1
  graduations [R4]. A cash flow model therefore projects: active lives (premium income,
  claim inceptions after the deferred period) and claims in payment (benefit outgo run off
  with duration-dependent recovery and death intensities — a disabled-life annuity). The
  CMI IP Rate Table Tool produces exactly these quantities (decrement rates, continuance
  probabilities, claim annuity values) for subscribers [R5]. Predecessor bases: IP06
  inception rates (2003–2010) and IPM 1991-98 termination rates [R1]. The older
  Manchester Unity sickness-rate approach and the inception-annuity formulation are the
  historical alternatives to the multi-state model [unverified — no public IFoA document
  retrieved; CMIR 12 lineage itself verified via R4].
- **Valuation frame**: Solvency UK best-estimate liability = probability-weighted average
  of future cash flows discounted at the risk-free term structure [R7]; claims-in-payment
  IP elements are MA-eligible "eligible elements" where separately managed [R8]; RAO
  Class IV constrains contract design (≥5-year non-cancellable) [R6]; conduct under ICOBS
  [R9, cross-ref]; actuarial work governed by TAS 100/200 [R10, cross-ref].
- Product features a UK IP cash flow model must represent, from §§4–13: deferred periods
  (incl. dual and sick-pay-linked), banded earnings-replacement caps with minimum benefit
  guarantees and offsets (affecting amounts actually paid vs sums insured), full-term vs
  limited payment terms (12/24/60-month budget variants), escalation pre- and in-claim
  (RPI/CPI/CPIH capped ~10%, premium multipliers 1.2×/1.5×/RPI+step), proportionate/
  rehabilitation partial benefits, linked-claim windows (6–12 months / 52 weeks) that
  waive the deferred period, waiver of premium during claim, and guaranteed vs reviewable
  vs age-costed premium bases.

---

## Variations across insurers

- **Incapacity definition**: own occupation is now universal as the primary definition —
  none of the six sampled products uses suited or any-occupation as the primary basis for
  standard risks. Variation is in the fallback for non-workers: LV= homemaker
  (meal/housework) [S3], Vitality and Royal London ADL/task-based (3 of 6, 3 of 9)
  [S10][S5], The Exeter household-duties/going-outdoors tests [S7], Aviva a separate
  12-month "restricted benefit" [S1]. Cirencester still sells an Own/Own Suited hybrid
  and tapers own-occupation benefit by claim duration (100%/75%/50%) — the only
  duration-tapered benefit in the sample [S11].
- **Benefit formula**: the modern mainstream is a two-band percentage of pre-tax earnings:
  65%/45% (Aviva, Exeter Income First) or 65%/50% (Royal London) around a £60,000
  breakpoint; Vitality is 60%/50% around £60,000/yr equivalent; LV= and Cirencester use a
  flat 60%. Absolute caps range from £120,000/yr (Exeter) to £250,000/yr (Royal London,
  LV=).
- **Deferred periods**: 4/8/13/26/52 weeks is the common core; Day 1 / 1-week short
  deferreds are the friendly-society and specialist niche (Exeter, Cirencester, Vitality
  7-day for self-employed); Aviva adds 104 weeks and Vitality 24/60 months at the long
  end; dual deferred periods (Aviva, Vitality) and public-sector sick-pay-linked deferreds
  (all except Cirencester) are established features.
- **Limited payment terms**: 24 months is the standard budget variant (Aviva, LV= Budget
  24; LV= also 12); Royal London and The Exeter offer 1/2/5-year and 2/5-year variants;
  Vitality 12/24/60 months. All pair the limit with a 6-month back-at-work requirement
  before a same-cause re-claim (26 weeks at Royal London).
- **Premium bases**: guaranteed level premiums dominate the mainstream; reviewable
  premiums follow a common pattern (fixed 5 years, then reviewable with no cap);
  age-costed guaranteed premium scales are the friendly-society hallmark (The Exeter,
  Cirencester). Vitality is unique in linking premiums to measured health engagement
  (Optimiser: −0/+2.5% p.a. by Vitality Status).
- **Minimum benefit guarantees**: £1,500/month is the market convention (Aviva, LV=,
  Vitality, Cirencester), Royal London £1,750; doctors/surgeons get doubled floors
  (£3,000 LV=/Vitality, £3,500 RL).
- **Representative design** for the reference implementation: a full-term, own-occupation,
  guaranteed-premium monthly-benefit IP on the Aviva/Royal London pattern — deferred
  periods 4–52 weeks, benefit = min(chosen amount, 65% of first £60,000 + ~50% above,
  ~£20,000/month), £1,500–1,750 minimum benefit guarantee with continuing-income offsets,
  RPI-linked escalation option (capped 10%, premium multiplier 1.5×, escalating in
  claim), proportionate/rehabilitation benefit on the (A−B)/A×C formula, linked-claims
  window waiving the deferred period, waiver of premium during claim, expiry at 50–70
  with a 24-month limited payment term as the budget variant. The Holloway unit-based
  contract with capital account (Cirencester) and Vitality's status-linked pricing are
  structural variations worth documenting but not the representative chassis.

---

## Gaps and caveats

- **Premium rates are not public.** All sampled products are individually quoted; no
  insurer publishes IP rate tables. Only structure is public (guaranteed/reviewable/
  age-costed, minimum £5/month at LV= and Royal London, LV= £3/month admin charge).
  Reviewable-premium review formulas are discretionary and undisclosed.
- **CMI tables are access-restricted.** The IP11 rate files, WP131/136/149/203 and the IP
  Rate Table Tool are for CMI Authorised Users/subscribers only; the public record used
  here is the briefing note [R1] and IFoA landing pages [R2–R5]. Actual IP11 rate values
  are therefore not reproduced in these notes. CMIR 12 itself was not retrieved.
- **Edition mismatches within insurers** (flagged where used):
  - LV=: KFD [S4] is the 05/19 edition naming Liverpool Victoria Friendly Society Ltd;
    policy conditions [S3] are 01/24 naming Liverpool Victoria Financial Services Ltd.
    The out-of-work own-occupation window differs (12 months in [S4] vs 30 days in [S3])
    — S3 (newer, contractual) is authoritative.
  - Cirencester: KFD V7 (May 2026) [S11] describes the own-occupation 75%/50% taper and a
    10%-per-event GIO; Schedule 5 V3a (Jul 2024) [S12] shows level-rate own-occupation
    sick pay and a 20%-of-sick-pay event limit. The registered rules on the site lag the
    KFD; treated as an edition difference, KFD figures reported with their source.
  - The Exeter: [S9] (2019) documents the Income One Plus / Pure Protection Plus adviser
    generation (60%/40% of £100,000 formula), while [S7]/[S8] (March 2026) are the
    current member documents for Income First (65%/45% of £60,000). The Exeter's current
    new-business product lineup was not separately verified.
- **Vitality gaps**: IP entry-age limits, expiry-age limits and any guaranteed
  insurability option are not in the plan provisions sections read; they sit in adviser
  literature not fetched. The Vitality Programme/Optimiser interaction with premiums was
  verified only at the level quoted.
- **FCA ICOBS and FRC TAS texts** were not fetched in this pass (JS-rendered site /
  redundant with the shared library): entries R9 and R10 carry fetched_ok = false and
  rely on the shared library [regulatory-actuarial.md R11, R33, R34] verified in the same
  session.
- **Manchester Unity / inception-annuity history** is [unverified] general knowledge; the
  multi-state lineage via CMIR 12 → IPM 1991-98 → IP11 is verified only at landing-page
  level [R4].
- **State Pension age linkage**: only Cirencester references state retirement age in the
  sampled documents ([S11]); none of the other five products' documents link expiry to
  SPA — the task-brief expectation of SPA-linked expiry ages is not borne out by these
  particular documents.
- **Mirror-hosted documents**: [S4] and [S9] were retrieved from intermediary mirrors
  (lifequote.co.uk) because the insurer originals are bot-blocked or superseded; document
  codes are recorded so they can be re-verified against insurer-hosted copies.
- Two sampled "current" documents ([S5] July 2026, [S7] March 2026, [S11] May 2026) are
  dated after the compilation date's product generations discussed in older adviser
  materials; where numbers conflict across generations the newest contractual document is
  preferred.
