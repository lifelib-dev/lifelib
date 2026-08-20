# Whole of Life Assurance (underwritten guaranteed, and over-50s guaranteed acceptance) — research notes (UK)

Research basis for reference implementations of liability cash flow projection models (lifelib/modelx style).
Access date for all citations: 2026-08-03. Currency: GBP. Terminology: UK (assurance, sum assured, cash-in value).

Two product cells are covered:

- **Cell A — Over-50s guaranteed acceptance whole of life** (no underwriting; fixed cash sum; first-year moratorium; premium cessation age; no surrender value). Sources: SunLife (Phoenix Life), Legal & General, Aviva, Royal London.
- **Cell B — Underwritten guaranteed whole of life** (medically underwritten; guaranteed premiums and sum assured for life; terminal illness benefit). Sources: Zurich, Royal London (adviser menu), Vitality (existence/positioning).
- Plus a **legacy variation**: unit-linked flexible/reviewable whole of life (maximum vs balanced cover) documented from a ReAssure closed-book factsheet.

---

## Primary sources

### S1 — SunLife, "Guaranteed Over 50 Plan — Terms and Conditions including the Policy Summary" (PDF)
- Publisher: SunLife (distributor SunLife Limited); insurer **Phoenix Life Limited** trading as SunLife
- Doc type: policy conditions + policy summary (combined booklet), doc code S-G050T12.25.V3 (Nov 2025 version)
- URL: https://www.sunlife.co.uk/siteassets/documents/2025-11-guaranteed-over-50-plan-terms-and-conditions.pdf
- Fetched: YES (full 8-page text extracted)
- Key facts: whole of life insurance paying a fixed cash sum on death after year 1. Eligibility age **49–85** at start, UK resident (England, NI, Scotland, Wales; excl. Channel Islands / Isle of Man). Minimum cover **£500**. Premiums cease at the policy anniversary on or after the **95th birthday**; cover continues for life. Year 1: non-accidental death → return of all premiums paid; accidental death (death within 90 days of accidental bodily injury from a sudden and unexpected event) → full cash sum. Accidental Death Benefit exclusions: criminal act, flying (except fare-paying passenger), hazardous pursuits, self-inflicted injury, war/hostilities, alcohol/drug abuse, natural causes/illness/disease. Aggregation limits: total guaranteed-acceptance SunLife-branded cover with Phoenix Life ≤ **£18,000** and total monthly premiums ≤ **£100**. **No cash-in value at any time**; stop paying → plan cancelled, nothing back (arrears process: 30 days + 14 days reminder; reinstatement possible within 6 months of first unpaid premium by paying arrears). One-off irreversible premium/cash-sum reduction option. Premium fixed, based on age at outset, smoking status and cash sum; monthly Direct Debit only. Documented consumer warnings: "Depending on how long you live you could pay more in premiums than the cash sum paid out"; inflation reduces the value of the fixed cash sum. Claim interest added from date of death to payment at Bank of England Base Rate − 0.5%, floor 0.5% p.a. 30-day cooling-off with premium refund. IHT: sum forms part of estate unless in trust. FSCS: 100% protection. Law of England and Wales. Phoenix Life Limited FCA/PRA reg. no. 110418; SunLife Limited (intermediary) reg. no. 769427, paid by commission as a percentage of total annual premium.

### S2 — SunLife, "Over 50s Life Insurance" product page
- Publisher: SunLife
- Doc type: product page (marketing + parameters)
- URL: https://www.sunlife.co.uk/over-50-life-insurance/
- Fetched: YES
- Key facts: premiums **£4–£100 per month**; guaranteed acceptance ages 49–85, no medical questions; premiums never increase; premium cessation at policy anniversary after 95th birthday; example quote: £20/month, age 50 non-smoker → cash sum **£5,694**; max £18,000 across all SunLife plans; no joint policies; free health & wellbeing support service (RedArc); welcome gift (£130 gift card after 6 monthly payments) [marketing incentive]; warnings repeated: fixed cash sum eroded by inflation, "you may pay in more than you get out", no cash-in value.

### S3 — SunLife, "Funeral Benefit Option" page
- Publisher: SunLife
- Doc type: product page (option description)
- URL: https://www.sunlife.co.uk/over-50-life-insurance/funeral-benefit-option/
- Fetched: YES
- Key facts: optional, free to add. Named funeral provider: **Co-op Funeralcare** (800+ funeral homes). On death, the plan's cash sum is paid **directly to the Co-op funeral director** and put towards the funeral; the family receives a **10% discount** on eligible Co-op Funeralcare services (excludes third-party costs, e.g. minister fees, flowers, memorials). Only valid with Co-op Funeralcare; incompatible with holding another funeral plan/benefit option; lapses if the underlying plan is cancelled; shortfall vs funeral cost is payable by the family.

### S4 — Legal & General, "Over 50's Life Insurance — Policy Terms and Conditions" (PDF)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy conditions, doc code QGI11740 06/26
- URL: https://www.legalandgeneral.com/landg-assets/personal/life-cover/_resources/over-50s/documents/terms-and-conditions.pdf
- Fetched: YES (full 6-page text extracted)
- Key facts: guaranteed acceptance, no medical questions, ages **50–80**, UK resident (≥183 days in UK in last tax year). Multiple policies allowed subject to total cash sum ≤ **£10,000** (policies pre-25 Nov 2017 per their own docs). Two variants: **Over 50s Fixed Life Insurance** (fixed cash sum and premiums) and **Over 50s Increasing Life Insurance** (cash sum reviewed annually in line with **RPI**, floor 0%, cap **10%** p.a.; premiums increase by **RPI × 1.5**, cap **15%** p.a.; declining an increase once freezes cash sum and premium permanently; cash-sum indexation continues after premiums cease at 90). Premiums payable monthly from start date up to and including the **90th birthday**; cover continues for life thereafter. Year 1: death from accident (bodily injury from "external, violent and visible means", death within 90 days) → full cash sum; any other cause → refund of premiums. Treated as non-accidental (refund only): suicide/intentional serious self-injury, hazardous sport/pastime, aerial flight other than fare-paying passenger on licensed airline, criminal act/assault, war/riot/civil commotion, alcohol or non-prescribed drugs. Missed premiums: cancellation right if unpaid 60 days after due date; no refund. Premium reduction option after year 1 (once per policy, floor at minimum premium; cash sum reduces). No explicit cash-in value (policy "pays out … if you die after one year"; policy summary S5 states no cash value). Trust option described. Cancellation: 30-day cooling-off with refund; after that no refund. Smoking status: non-smoker = no tobacco/e-cigarettes/nicotine replacement in last 12 months. Misrepresentation remedies (deliberate/reckless vs careless). Governed by English law; FCA/PRA reg. no. 117659.

### S5 — Legal & General, "Over 50s Fixed Life Insurance — Policy Summary" (PDF)
- Publisher: Legal & General Assurance Society Limited
- Doc type: policy summary (IPID-style), doc code QGI12836 11/2025
- URL: https://www.legalandgeneral.com/landg-assets/personal/life-cover/_resources/over-50s/documents/fixed-policy-summary.pdf
- Fetched: YES (full 4-page text extracted)
- Key facts: pays cash sum on death after one year; whole of life while premiums maintained; guaranteed acceptance 50–80, UK resident (183-day test); **maximum cash sum £10,000** across all L&G Over 50s policies; **no cash value unless a valid claim is made**; "not designed to meet the full cost of a funeral, and does not guarantee to do so"; stop premiums at **age 90**; year-1 accidental death → full cover, else premium refund; premium reduction after 1 year (min premium applies); explicit warning "total premiums paid may be greater than the cash sum we pay on death"; 30-day cooling-off.

### S6 — Legal & General, "Over 50s Life Insurance" product page
- Publisher: Legal & General
- Doc type: product page
- URL: https://www.legalandgeneral.com/insurance/over-50-life-insurance/
- Fetched: YES
- Key facts: monthly premium range **£5–£75**; premiums fixed for life; illustrative cash sums for £25/month non-smoker: age 50 → **£7,643**; age 60 → **£6,046**; age 70 → **£3,701**; age 80 → **£1,893** (shows steep age gradient of rates); cash sum cap £10,000 across policies; premiums stop at 90, cover continues.

### S7 — Aviva, "Guaranteed Lifelong Protection — Plan Conditions" (PDF)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: policy conditions, doc code LD01052 11/2016 (version currently posted under aviva.co.uk over-50s path)
- URL: https://static.aviva.io/content/dam/aviva-public/gb/pdfs/personal/insurance/life/over-50s/insurance-life-over-50s-guaranteed-lifelong-protection-plan-conditions.pdf
- Fetched: YES (via direct download; WebFetch returned 403; full 6-page text extracted)
- Key facts: benefit structure distinctive among over-50s plans: **before first anniversary** — death by "fatal accident" → Life Insurance Amount; other death → return of premiums paid. **On/after first anniversary** — death by fatal accident → **2 × Life Insurance Amount**; other death → 1 × Life Insurance Amount. "Fatal accident" = bodily injury caused directly by accidental, external, violent and visible means, not as a direct result of sickness/disease/physical disorder. Accidental-death enhancement not payable if death occurs while living outside Europe, USA, Canada, Australia or NZ, or caused by: criminal act, alcohol/drug abuse (incl. overdose, non-prescribed controlled drugs), flying (except passenger on commercially licensed aircraft), hazardous pursuits (motor sports, roped mountaineering, potholing, scuba), self-inflicted injury, war/riot/civil commotion. **No cash-in value at any time.** Premiums monthly by Direct Debit; **30 days grace**; unpaid at end of grace → plan cancelled, nothing payable. Premium cap: total **£100/month** per life insured across plans issued on/after 25/01/2010. Alteration powers, age-misstatement rule (outside age limits at true age → cancel and refund premiums without interest). Aviva Life & Pensions UK Ltd, FRN 185896; law of England.

### S8 — Aviva, "Key Features of Guaranteed Lifelong Protection" (PDF)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: key features document, doc code LD06001 11/2016
- URL: https://static.aviva.io/content/dam/aviva-public/gb/pdfs/personal/insurance/life/over-50s/insurance-life-over-50s-guaranteed-lifelong-protection-key-features.pdf
- Fetched: YES (via direct download; full 5-page text extracted)
- Key facts: single life only, plan holder aged **50–80** at start. Premium chosen by customer: **minimum £7, maximum £50 a month** (per plan; £100/month across plans); life insurance amount determined by premium and age. Premium term: **"You'll either pay for 30 years, or until the plan anniversary after your 90th birthday, whichever comes first"** — cover continues after premiums cease. Premiums never increase. Plan is deliberately inflexible ("You can't alter it once it's started"); no additional benefits. No cash-in value; documented risk that "the amount paid out on your death may be less than the total amount you have paid in premiums"; fixed cash sum eroded by inflation. 30-day cancellation with refund. FSCS 100%.

### S9 — Royal London, "Terms & Conditions — Over 50 Life Insurance" (PDF)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions, doc code D2COFTC
- URL: https://www.royallondon.com/siteassets/site-docs/insurance/life-insurance/over-50s-direct-terms-conditions.pdf
- Fetched: YES (full 9-page text extracted)
- Key facts: ages **50–80**, UK resident; payout ("Payout") up to **£10,000** across all RL Over 50 policies; monthly payments capped at **£100** across policies. Premiums payable monthly by Direct Debit until the policy anniversary on/after the **90th birthday** ("Final Payment Date") or earlier death. Year 1: accidental death (event causing physical injury that "could not have been predicted and was not intentional") → full Payout; suicide in year 1 explicitly not accidental → refund of payments; non-accidental death → refund of all monthly payments. Missed payment: 60 days to make good; death within the 60 days → claim reduced by unpaid amounts (worked example £3,050 − £10 = £3,040). **Payout Promise** (paid-up value feature, unusual for the market): if ≥ half of expected payments (start to Final Payment Date) have been made and payments stop, the policy stays entitled to a reduced Payout = full Payout × payments made ÷ total expected monthly payments (worked example: policy at 70, 240 expected payments, £3,500 payout, stops after 180 payments → 0.75 × £3,500 = **£2,625**). If < half paid → cancelled with nothing back. Premium reduction to as little as **£3.95/month** (Payout reduces); no increases allowed (take additional policies instead, subject to caps). **Payment holidays**: after year 1, up to 2 holidays, each up to 6 months, at least 12 months apart; missed amounts repaid or Payout reduced by missed payments (worked example £3,850 − £120 = £3,730). **Funeral Benefit Option**: payout sent directly to the funeral provider who arranges the funeral (provider agreement separate from RL; welcome pack from provider); year-1 death → Payout to estate; option removable (irreversibly); incompatible with trust or assignment; "Funeral Benefit Option is not regulated by the Financial Conduct Authority". Claims interest if payment delayed > 2 months: BoE base − 0.5%, floor 0.5%, daily. 30-day cooling-off refund; later cancellation: nothing back unless Payout Promise qualified. Trust and assignment supported. FSCS protected; law of England and Wales; FCA/PRA reg. no. 117672. (Named funeral provider not stated in the T&C; Co-op Funeralcare is used by SunLife [S3]; RL's current provider not verified.)

### S10 — Zurich, "Zurich Whole of Life — Terms and conditions" (PDF)
- Publisher: Zurich Assurance Ltd
- Doc type: policy conditions, doc code PW720491009 (08/25)
- URL: https://www.zurichintermediary.co.uk/-/media/zurich-intermediary/documents/terms-and-conditions/720491.pdf
- Fetched: YES (via direct download; full 20-page text extracted)
- Key facts: underwritten whole of life; pays **sum assured on death or diagnosis of terminal illness** (definite diagnosis, no known cure or beyond cure, death expected within 12 months, confirmed by attending consultant); pays once then ends. Lives: single, joint life first event, joint life second event. Entry ages: **18–83 single life; 18–69 joint first event; 18–83 joint second event** (age x = before (x+1)th birthday); no maximum cover-end age (whole of life). UK residency + registered with UK doctor for 6 months before applying. Exclusion: suicide or intentional self-inflicted injury within **12 months** of start (or of a requested/milestone increase) → refund of premiums for that cover. **Premiums guaranteed** unless cover changed / Increasing Cover chosen / disclosure corrections; minimum premium **£8/month or £80/year** (as at 1 Jan 2025); monthly or annual Direct Debit. Non-payment: cover ends if unpaid 2 months after due date; **no reinstatement** (new application needed). **Level or Increasing Cover** (chosen at outset only): increases each policy year by **3%, 5% or RPI (capped 10%)**; premiums rise **2% for each 1%** cover increase; opt out of an increase 3 times → option removed permanently; increases stop if sum assured would exceed **£40m**. **Milestone benefit** (guaranteed insurability): increase sum assured without further underwriting within 90 days of life events (mortgage increase/house move, marriage/civil partnership, divorce/dissolution/separation, birth/adoption, ≥10% salary rise on promotion/job change, increase in IHT liability incl. legislative change); cap = lower of original sum assured or **£200,000** across all Zurich policies; age limit 54 (69 for IHT events); premium for the increase based on original underwriting but current age. Requested increases re-underwritten ("personal circumstances"). Reduction of cover any time (floor: minimum premium). **Waiver of Premium** optional at extra cost (add at outset only): 6-month deferred period, own-occupation definition, entry 18–54, terminates at 70; monthly premiums required. Smoker-status review possible after 12 months nicotine-free. **No cash-in value at any time.** Trust registration (TRS) notes for claims. FSCS 100% (continuity first). Zurich Assurance Ltd, FRN 147672; law of England.

### S11 — Zurich, "Zurich Whole of Life — Key features" (PDF)
- Publisher: Zurich Assurance Ltd
- Doc type: key features document, doc code PW720505007 (02/25)
- URL: https://www.zurichintermediary.co.uk/-/media/zurich-intermediary/documents/key-features/720505.pdf
- Fetched: YES (via direct download; full 12-page text extracted)
- Key facts: confirms S10 (ages table identical; level vs increasing mechanics; premiums guaranteed; milestone benefit; WoP 18–54 entry, ends day before 70th birthday; suicide/self-inflicted 12-month exclusion; no cash-in value; 30-day cooling-off with refund). Free cover possible while underwriting is in progress. Sold with adviser involvement ("Your adviser will help you decide"). Cost depends on age, health, occupation, nicotine use, amount/type of cover and optional benefits.

### S12 — Zurich for advisers, "Whole of Life" product page
- Publisher: Zurich (zurichintermediary.co.uk)
- Doc type: adviser product page with document links
- URL: https://www.zurichintermediary.co.uk/whole-of-life
- Fetched: YES
- Key facts: document set (key features 720505, T&C 720491, target market statement 721465, IHT protection free cover 721123, WoL premium calculator). Minimum premium £8/month or £80/year; **free life cover during underwriting up to £1,500,000**; no upper age limit at claim; terminal illness = expected death within 12 months; milestone benefit cap lower of original sum assured or £200,000, usable to age 54 (69 for IHT).

### S13 — Royal London for advisers, "Life Cover — Product details" page (Personal Menu Plan)
- Publisher: Royal London (adviser.royallondon.com)
- Doc type: adviser product specification page
- URL: https://adviser.royallondon.com/protection/personal-protection/life-or-critical-illness-cover/detail/ (life cover detail page: https://adviser.royallondon.com/protection/personal-protection/life-cover/detail/)
- Fetched: YES (life cover detail page)
- Key facts (menu Life Cover, of which whole of life is the no-end-date form): minimum entry age **18**, maximum entry age **88** (attained); maximum cover end age 89 for term (whole of life = no end date). Sum assured: **unlimited**, or capped at **£5 million** when increasing (indexed) cover is selected. Guaranteed premiums offered. Increasing cover: fixed-rate increases **2%–5%**, or RPI-linked increases applied between **2% and 10%**. Terminal illness benefit included (definition per plan details). Payout as lump sum or income (income not available for joint life second death or decreasing cover).

### S14 — Royal London, "Personal Menu Plan — Life Cover — Plan details" (PDF, December 2024)
- Publisher: The Royal London Mutual Insurance Society Limited
- Doc type: policy conditions booklet (menu plan life cover, incl. whole of life), doc code PCP8P10004
- URL: https://adviser.royallondon.com/globalassets/docs/protection/pcp8p10004-plan-details-for-the-personal-menu-plan-life-cover.pdf
- Fetched: YES (44 pages downloaded; introductory sections and structure read — claims, premiums, cover-change options (Cover Increase Options, Renewable Option, Joint Life Separation/Reinstatement/Conversion, Gifting option), cash-in value section, mis-statement of age)
- Key facts used here: contract = application + terms + cover summary + endorsements; 30-day cooling-off with premium refund; UK/Jersey/Guernsey/Isle of Man residency notification requirements; menu structure with per-cover terms. (Detailed WoL parameters cited from S13; deeper clause-level extraction of this 44-page booklet not performed.)

### S15 — ReAssure, "Keeping your reviewable whole-of-life policy on track" (PDF factsheet)
- Publisher: ReAssure Ltd (closed-book consolidator; FRN 110495)
- Doc type: customer factsheet on legacy unit-linked reviewable whole of life
- URL: https://www.reassure.co.uk/uploads/2015/12/Keeping-your-whole-of-life-policy-on-track.pdf
- Fetched: YES (full 4-page text extracted)
- Key facts (legacy unit-linked flexible whole of life): premiums are invested into unit-linked funds; a portion of the fund is deducted monthly to pay for life cover; initial premium and cover guaranteed **to the first policy review**; reviews "usually start after 10 years", then typically **5-yearly**, reducing to **annual** past a certain age; failed review → increase premium to keep cover, or keep premium and reduce cover (default if customer lost contact: reduce cover). Two bases: **Maximum cover** (nearly all premium buys current cover; minimal reserve; premium jumps at reviews; illustrative initial premium ~**£8/month per £100,000** sum assured) vs **Standard/balanced cover** (higher initial premium builds an investment reserve to subsidise later cost of cover; illustrative ~**£50/month per £100,000**; premiums still reviewable, particularly after age 65 or when the fund is exhausted). Life cover costs "rise sharply from age 65". Surrender value = value of investment units (if any). Reinstatement after lapse needs a declaration of health. Optional accelerated critical illness / permanent disability benefits typically expiring at e.g. 65.

### S16 — Vitality, "Whole of life insurance" product page
- Publisher: Vitality (VitalityLife)
- Doc type: product page
- URL: https://www.vitality.co.uk/life-insurance/life-cover/whole-life/
- Fetched: YES (via direct download; WebFetch returned 403)
- Key facts: Vitality currently markets whole of life insurance — "guarantees your loved ones get a payout when you pass away"; ends only on death or premium cessation; positioned for funeral costs, legacy and inheritance-tax planning (in trust); life insurance from **£5 a month**; paid 99.4% of life cover claims in 2025 (their claims report); integrated with the Vitality Programme (healthy-living premium discounts/rewards). Detailed WoL plan provisions (ages, optimiser mechanics) not extracted — see Gaps.

---

## Regulatory and actuarial references

### R1 — FCA, "MS24/1: Pure Protection Market Study" (study landing page)
- Publisher: Financial Conduct Authority
- URL: https://www.fca.org.uk/publications/market-studies/ms24-1-1-market-distribution-pure-protection
- Fetched: YES
- Key facts: market study into distribution of pure protection to retail consumers. Timeline: terms of reference announced **August 2024**; study launched with final ToR **March 2025**; **interim report January 2026**; stakeholder workshops spring 2026; **final report expected Q3 2026**. Findings flagged: 58% of adults lack pure protection; disparities in claims ratios across products; intermediary incentives driving unnecessary switching. Linked docs: interim report, consumer research report (Jan 2026), Annex 1, Annex 2, ToR (ms24-1-2.pdf).

### R2 — FCA, "MS24/1 Annex 2: Value of pure protection products" (PDF)
- Publisher: Financial Conduct Authority
- URL: https://www.fca.org.uk/publication/market-studies/ms24-1-annex-2.pdf
- Fetched: YES (full text extracted; Chapter 3 is "Guaranteed acceptance over 50s")
- Key facts (directly relevant to modelling this product):
  - ToR premise: some guaranteed-acceptance over-50s (GO50) customers "receive low average payouts compared to overall premiums paid"; underwritten whole of life may offer better value for some (¶3.1, 3.18).
  - **Tipping point** (crossover): firms model ex ante the point at which cumulative premiums exceed sum assured, by cohort (age, smoker status). Stylised representative example: **£30/month premium, £5,000 sum assured → tipping point after 13 years 11 months** (¶3.10–3.11, Figure 3).
  - **Premium age caps**: "Typically, age caps on premiums apply from age 90, although we see some insurers applying this from age 95"; one insurer additionally caps premiums after **30 years or at age 90** to limit over-payment (¶3.15–3.16). FCA has not seen evidence that a significant proportion of customers reach the cap (¶3.17).
  - Entrants at **79–80** are most likely to receive payout < premiums paid (lower sum assured per premium at high ages, shorter time to tipping point); but "the majority of guaranteed acceptance over 50s policies pay out more than the value of premiums paid in" (¶3.13).
  - **Price comparison**: GO50 customers pay on average **£71.73 in premiums per £1,000 sum assured** vs **£8.10** for underwritten whole of life (¶3.19) — reflecting guaranteed acceptance anti-selection, older entry and shorter durations.
  - **Lapse-supported economics**: for products like GO50, "individual customers who keep paying beyond a point may pay more than is ultimately paid out. Their contributions help sustain the pool for others. Without this dynamic, insurers would need to rely on lapses to remain profitable … particularly where there is no surrender value" (¶3.9) — regulatory articulation of the cross-subsidy/lapse-support issue.
  - Differential smoker/non-smoker pricing implemented across the GO50 market (fn 4). One insurer restricts new fully-underwritten policies at age 77, making GO50 the only accessible cover at high ages (¶3.4). Claims acceptance is consistently higher for GO50 than other pure protection; one firm reported zero claim rejections (¶3.5).
  - ABI 2024 claims-accepted rates (Figure 2): term assurance 96%, critical illness 91%, **whole of life 100%** (combined GO50 + underwritten), income protection 86%, all protection 98%.
  - Consumer Duty framing: firms must assess fair value by cohort within Fair Value Assessments (FVAs), including tipping-point analysis; communications must enable informed choice about the over-payment risk (¶3.6, 3.9–3.14).

### R3 — PRA Rulebook, "Technical Provisions" Part (Solvency UK)
- Publisher: Prudential Regulation Authority (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Fetched: YES (via direct download; WebFetch returned 403; rule text extracted; site viewed "in the present on 03/08/2026")
- Key facts: technical provisions must be established for all insurance obligations (2.1); value = amount payable to transfer obligations immediately to another UK Solvency II firm (2.2); calculation must be market-consistent, prudent, reliable, objective (2.3); **value of TP = best estimate + risk margin** (2.4), valued separately unless cash flows can be replicated (2.5). Risk margin: cost-of-capital method with **cost-of-capital rate 4%** as specified in regulation 7B(b) of the IRPR Regulations (definition in 1.2, effective 31/12/2024 version) — the reduced Solvency UK rate. Volatility adjustment now by PRA permission under FSMA s.138BA. Related policy: PS2/15, PS10/24 (matching adjustment reform), **PS15/24 (restatement of assimilated law)**; supervisory statements incl. SS7/18 (matching adjustment).

### R4 — PRA, "PS15/24 – Review of Solvency II: Restatement of assimilated law"
- Publisher: Bank of England / PRA
- URL: https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/review-of-solvency-ii-restatement-of-assimilated-law-policy-statement
- Fetched: YES (via direct download; WebFetch returned 403)
- Key facts: final policy statement implementing the Solvency II Review ("Solvency UK"): Solvency II assimilated law **revoked by HMG on 31 December 2024** under FSMA 2023, replaced by PRA rules, SS/SoP and reporting templates **effective 31 December 2024**; confirms near-final rules from PS2/24 (adapting to the UK insurance market), PS3/24 (reporting/disclosure) and PS10/24 (matching adjustment reform); includes mapping tables from assimilated law to PRA material. Confirms the current prudential frame for UK whole of life liabilities is the restated PRA Rulebook (BEL + risk margin per R3), not EU Solvency II text.

### R5 — Financial Services and Markets Act 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Fetched: YES
- Key facts: Schedule 1 Part II lists 9 classes of contracts of long-term insurance. **Class I "Life and annuity"**: "Contracts of insurance on human life or contracts to pay annuities on human life, but excluding (in each case) contracts within paragraph III" (Class III = "Linked long term"). Conventional whole of life assurance (both cells here) is Class I long-term business; legacy unit-linked whole of life is Class III.

### R6 — CMI / IFoA, "'00' series tables" page
- Publisher: Institute and Faculty of Actuaries (Continuous Mortality Investigation)
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/00-series-tables
- Fetched: YES
- Key facts: the assured-lives **permanent assurances** ("00" series, graduated on UK life office experience 1999–2002 per CMI WP21 [series context; experience period not restated on this page]) tables relevant to whole of life: **AMC00** (males combined), **AMS00** (males smokers), **AMN00** (males non-smokers), **AFC00/AFS00/AFN00** (female equivalents); parallel temporary assurances tables (TM.../TF...) exist for term. Final mortality-rate values downloadable from the page; contact info@cmilimited.co.uk.

### R7 — IFoA blog, "CMI: New '16' Series term assurance mortality and accelerated critical illness tables"
- Publisher: Institute and Faculty of Actuaries (blog.actuaries.org.uk)
- URL: https://blog.actuaries.org.uk/cmi-new-16-series-term-assurance-mortality-and-accelerated-critical-illness-tables/
- Fetched: YES
- Key facts: the "16" Series tables (experience **2015–2018**, with indicative 2020 analysis) cover **term assurance mortality (incl. terminal illness) and accelerated CI only**; issued **to CMI Subscribers** (access restriction). Notably: "The Committee has now turned its attention to reporting on the mortality experience of **underwritten and non-underwritten whole of life assurances**" — i.e. modern WoL-specific assured-lives tables were pending as of that post; the "00" series permanent assurances tables (R6) remain the latest published assured-lives whole-of-life base tables. Non-underwritten (guaranteed acceptance) experience is being analysed separately from underwritten — direct CMI recognition of the anti-selection distinction.

### R8 — FRC, "General Technical Actuarial Standards (TAS 100)" page
- Publisher: Financial Reporting Council
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- Fetched: YES
- Key facts: **TAS 100 v2.0** published 3 March 2023, **effective 1 July 2023**; applies to all technical actuarial work in UK geographic scope; mandatory for IFoA members; principles-based (5 principles incl. Models); supporting Technical Actuarial Guidance: Models (Oct 2024), Proportionality (Oct 2025), Technical Actuarial Work and Geographic Scope (Mar 2023). (TAS 200: Insurance applies additionally to insurance technical actuarial work — TAS 200 itself not fetched; see Gaps.)

### R9 — CMI Limited website
- Publisher: CMI Limited (cmilimited.co.uk)
- URL: https://www.cmilimited.co.uk/
- Fetched: **NO** — connection reset on both WebFetch and direct download (site appears to refuse this client). Known reference only: CMI Limited is the IFoA subsidiary producing mortality/morbidity tables and the CMI Mortality Projections Model; full outputs restricted to Authorised Users/Subscribers [consistent with R7's "issued to CMI Subscribers"; details unverified from this site].

### R10 — FCA, "MS24/1 Terms of Reference" (PDF)
- Publisher: Financial Conduct Authority
- URL: https://www.fca.org.uk/publication/market-studies/ms24-1-2.pdf
- Fetched: **NO** (not attempted directly; linked from R1). Known reference: sets out the GO50 value concern quoted in R2 ¶3.1.

---

## Extracted specifications

### 1. Product taxonomy and regulatory classification
- Whole of life assurance = contract of insurance on human life with no fixed end date; RAO Schedule 1 Part II **Class I (Life and annuity)** long-term business; unit-linked variants fall in Class III (Linked long term) [R5].
- Both cells are "pure protection" products within the scope of FCA market study MS24/1 (whole of life including guaranteed acceptance over 50s) [R1][R2].
- Prudential valuation: Solvency UK (PRA Rulebook) — technical provisions = best estimate liabilities + risk margin, market-consistent transfer value; risk margin cost-of-capital rate 4% (from 31 Dec 2024) [R3][R4].
- Conduct: Consumer Duty fair-value assessment by customer cohort is the operative conduct control on over-50s plans, including ex-ante tipping-point modelling [R2]. (The applicable conduct sourcebook for pure protection sales is ICOBS rather than COBS [unverified — handbook chapter not successfully fetched].)

### 2. Cell A — Over-50s guaranteed acceptance plans

#### 2.1 Providers and legal entities (all fetched documents)
| Plan | Insurer | Reg no. | Doc |
|---|---|---|---|
| SunLife Guaranteed Over 50 Plan | Phoenix Life Ltd (t/a SunLife; distributor SunLife Ltd) | 110418 / 769427 | [S1] |
| L&G Over 50s (Fixed / Increasing) Life Insurance | Legal & General Assurance Society Ltd | 117659 | [S4] |
| Aviva Guaranteed Lifelong Protection | Aviva Life & Pensions UK Ltd | 185896 | [S7] |
| Royal London Over 50 Life Insurance | The Royal London Mutual Insurance Society Ltd | 117672 | [S9] |

#### 2.2 Eligibility / acceptance
- Guaranteed acceptance, **no medical questions** in all four plans [S1][S4][S7 via S8][S9]. Rating factors: age at entry and smoker status only (SunLife: "age at outset, your smoking status and the cash sum" [S1]; L&G asks date of birth and recent smoking habits, non-smoker = no tobacco/e-cigs/nicotine replacement in previous 12 months [S4]). FCA confirms smoker/non-smoker differential pricing across the market [R2].
- Entry age windows: SunLife **49–85** [S1]; L&G **50–80** [S4]; Aviva **50–80** [S8]; Royal London **50–80** [S9]. UK residency required in all; L&G uses a 183-days-in-last-tax-year test [S4]; SunLife excludes Channel Islands/Isle of Man [S1].
- Single life only (SunLife explicitly no joint policies [S2]; Aviva "Only one person can be covered" [S8]).

#### 2.3 Benefit structure and first-year moratorium
- Core benefit: fixed cash sum on death, payable in full only after the plan has been in force **one year** [S1][S4][S8][S9].
- Death in year 1 from non-accidental causes → **return of premiums paid** (no interest) [S1][S4][S7][S9]. Royal London gives the worked example: 6 payments of £20 → £120 refund [S9].
- Death in year 1 by **accident** → full cash sum from day 1 [S1][S4][S7][S9]. Accident definitions vary:
  - SunLife/L&G: death within **90 days** of accidental bodily injury; L&G: injury by "external, violent and visible means" excluding sickness/disease/degeneration [S1][S4].
  - Aviva: "fatal accident" = bodily injury by accidental, external, violent and visible means [S7].
  - Royal London: an unpredicted, unintentional event causing physical injury; suicide in year 1 explicitly non-accidental [S9].
- Accidental-death exclusions (common list): criminal act; flying other than fare-paying passenger; hazardous pursuits; self-inflicted injury; war/riot/civil commotion; alcohol/drug abuse; natural causes/illness [S1][S4][S7].
- **Aviva variation**: after year 1, accidental death pays **2 × sum assured** (double accidental death benefit for life); and the accidental enhancement is void if death occurs while living outside Europe/USA/Canada/Australia/NZ [S7][S8].

#### 2.4 Premiums, cessation ages and caps
- Level guaranteed premiums for life of the plan, monthly Direct Debit only [S1][S4][S7][S9].
- **Premium cessation** (cover continues to death):
  - SunLife: policy anniversary on/after **95th birthday** [S1].
  - L&G: up to and including **90th birthday** [S4][S5].
  - Aviva: **30 years or plan anniversary after 90th birthday, whichever first** [S8] — matches the "additional 30-year cap" design the FCA singles out as limiting over-payment [R2 ¶3.16].
  - Royal London: policy anniversary on/after **90th birthday** ("Final Payment Date") [S9].
  - FCA: caps "typically … from age 90, although we see some insurers applying this from age 95" [R2].
- Premium ranges per plan: SunLife **£4–£100/month** [S2]; L&G **£5–£75/month** [S6]; Aviva **£7–£50/month** [S8]; Royal London floor after reduction **£3.95/month** [S9].
- Per-life aggregation caps across same-insurer plans: SunLife total cover ≤ **£18,000** and premiums ≤ **£100/month** [S1]; L&G total cash sum ≤ **£10,000** [S4][S5]; Aviva premiums ≤ **£100/month** (plans since 25/01/2010) [S7]; Royal London payout ≤ **£10,000** and payments ≤ **£100/month** [S9].
- Sum assured examples (rate feel): £20/month at 50 (non-smoker) → £5,694 SunLife [S2]; £25/month non-smoker → £7,643 (50), £6,046 (60), £3,701 (70), £1,893 (80) L&G [S6]. Minimum cover: SunLife £500 [S1].

#### 2.5 Crossover ("tipping point") warning — documented consumer risk
- All four insurers carry the mandated-style warning that total premiums may exceed the cash sum: SunLife "Depending on how long you live, the total premiums paid may be greater than the cash sum payable on death" [S1]; L&G [S4][S5]; Aviva "the amount paid out on your death may be less than the total amount you have paid in premiums" [S8]; Royal London "it's possible you could end up paying more in total for your policy than it pays out" [S9].
- FCA quantification: representative modelling — £30/month for £5,000 sum assured crosses at **13 years 11 months**; entrants at 79–80 most exposed; majority of policies still pay out more than premiums paid [R2].
- Average price: **£71.73 per £1,000 sum assured** (GO50) vs £8.10 (underwritten WoL) [R2].

#### 2.6 Surrender / paid-up / lapse
- **No cash-in value at any time** in all four plans [S1][S4-S5][S7][S9]; cancellation after the 30-day cooling-off returns nothing [S1][S4][S9][S8].
- Lapse: SunLife 30 + 14 days arrears then cancellation, reinstatable within 6 months by paying arrears [S1]; L&G cancellation right after 60 days unpaid [S4]; Aviva 30 days grace then cancellation [S7]; Royal London 60 days, claim within window reduced by unpaid premiums [S9].
- **Royal London exception — "Payout Promise"** (paid-up benefit): if ≥ half of the expected payments (start → Final Payment Date) have been made, cover continues after premiums stop at a reduced payout = full payout × (payments made ÷ expected payments); e.g. 180/240 × £3,500 = £2,625 [S9]. This materially changes lapse behaviour/economics vs the other three plans (which forfeit everything on lapse) — model as a paid-up option with pro-rata sum assured.
- FCA on the economics: without the premium cross-subsidy from long-lived continuers, "insurers would need to rely on lapses to remain profitable", especially with no surrender value [R2 ¶3.9] — lapse-supported design is thus acknowledged in the regulatory record rather than only analyst commentary.

#### 2.7 Options and riders
- **Funeral Benefit Option** (payout redirected to a funeral provider): SunLife — Co-op Funeralcare, cash sum paid direct to the funeral director + 10% discount on eligible services, free to add [S3]. Royal London — payout sent direct to the (unnamed in T&C) funeral provider who arranges the funeral; year-1 death → estate instead; removal irreversible; incompatible with trust/assignment; the option itself is not FCA-regulated [S9]. L&G historically offered a Funeral Benefit Option with Dignity adding a £250 contribution [unverified — third-party broker snippets only; the current official L&G funeral-benefit page shows no such option].
- **Indexation**: only L&G among the four offers an increasing variant — cash sum indexed to RPI (0% floor, 10% cap), premiums increase at RPI × 1.5 (15% cap), premiums stop at 90 while indexation of the cash sum continues; declining one increase freezes the policy permanently [S4]. SunLife, Aviva, Royal London plans are fixed-sum only [S1][S8][S9].
- **Premium reduction**: SunLife once, irreversible [S1]; L&G once after year 1, min premium floor [S4]; Royal London reducible to £3.95/month [S9].
- **Payment holidays**: Royal London only — up to 2 holidays of up to 6 months, ≥ 12 months apart, after year 1; missed amounts repaid or netted off the payout [S9].
- Claims interest: SunLife and Royal London both add interest (BoE base − 0.5%, floor 0.5% p.a.) between death (RL: where payment delayed > 2 months) and payment [S1][S9].

#### 2.8 Tax and protection
- Cash sum normally part of the estate → potential IHT unless written in trust; free of income tax and CGT [S1][S4][S8][S9 (income/CGT explicitly in S9/S8)].
- FSCS: 100% of claim protected; continuity of cover is FSCS's first objective for life policies [S1][S8][S10].

### 3. Cell B — Underwritten guaranteed whole of life

#### 3.1 Current market (verified sellers)
- **Zurich Assurance Ltd** — "Zurich Whole of Life", adviser-distributed [S10][S11][S12].
- **Royal London** — whole of life as Life Cover with no end date under the Personal Menu Plan, adviser-distributed [S13][S14].
- **Vitality** — whole of life insurance currently marketed [S16].
- FCA treats "underwritten whole of life" as a live product category with distinct target market (wealthier, younger-entry, higher sums assured; Mintel research cited) [R2 ¶3.19–3.21]. One (unnamed) insurer restricts new underwritten policies at age 77 [R2 ¶3.4]. Other historical/possible sellers (AIG Life UK — acquired by Aviva in 2024; L&G whole-of-life protection) [unverified].

#### 3.2 Core design (Zurich as representative, cross-checked to Royal London)
- Benefit: **sum assured paid once, on death or earlier diagnosis of terminal illness** (life expectancy < 12 months, confirmed by attending consultant), then policy ends [S10][S12]; RL likewise includes terminal illness [S13].
- Lives assured: single; joint life first event; joint life second event [S10]. RL adds payout-as-income option (not on JL second death) [S13].
- Entry ages: Zurich **18–83** single and JL 2nd event, **18–69** JL 1st event [S10][S11]; Royal London **18–88** [S13]. No maximum cover age — cover is for life [S10][S12].
- Residency/underwriting: UK resident, registered with a UK doctor ≥ 6 months before application; full disclosure duty; insurer may access medical records up to 6 months post-issue (Zurich routine checks) [S10][S11]. Fully medically underwritten (health, occupation, family history, lifestyle) [S10 glossary "personal circumstances"][R2 ¶3.19].
- Sums assured: no stated maximum for level cover (Zurich increases stop only at **£40m** [S10]; Royal London "unlimited", **£5m cap** when increasing cover selected [S13]). Minimum premium Zurich **£8/month or £80/year** (as at 1 Jan 2025) [S10][S12].
- **Premiums guaranteed for life** — change only on customer-initiated cover changes, Increasing Cover escalation, or application-disclosure corrections [S10][S11]; RL offers guaranteed premiums [S13]. Monthly or annual Direct Debit (monthly compulsory with Waiver of Premium) [S10].
- Exclusion: suicide / intentional self-inflicted injury within **12 months** of start or of any increase → premiums refunded instead of sum assured (only stated exclusion on the core benefit) [S10][S11].
- **No cash-in value**; lapse after 2 months' unpaid premiums terminates cover with no reinstatement (new underwriting required) [S10].

#### 3.3 Indexation and options
- **Increasing Cover** (outset choice only): sum assured +3%, +5% or RPI (10% cap) annually; **premium +2% per 1% of cover increase** (premium escalation steeper than benefit escalation — key cash flow feature); 3 declined increases → permanently level [S10][S11]. Royal London: fixed 2–5% or RPI-linked 2–10% increases [S13].
- **Milestone benefit** (guaranteed insurability): sum assured increases without underwriting within 90 days of life events (house purchase/mortgage increase, marriage/civil partnership, divorce/separation, birth/adoption, ≥10% promotion salary rise, IHT-liability increases); cap = lower of original sum assured or **£200,000** aggregated across Zurich policies; max age 54 (69 for IHT events) [S10][S12].
- **Waiver of Premium** (optional, extra cost, outset only): 6-month deferred period, own occupation, entry 18–54, expires at 70 [S10][S11].
- Free cover during underwriting up to **£1,500,000** (Zurich) [S12].
- Smoker-status premium review after ≥ 12 months nicotine-free [S10].
- Non-smoker definition (Zurich, for rating): no tobacco/nicotine products for > 5 years = non-smoker; 12 months–5 years = previous smoker; < 12 months = smoker [S10 glossary].

#### 3.4 Tax positioning
- Marketed for IHT planning (write in trust so the sum assured sits outside the estate; cover the IHT liability itself) [S11 tax section][S16]; trust registration (TRS) requirements on claims [S10].

### 4. Legacy variation — unit-linked flexible/reviewable whole of life [note]
- Historic design (large closed books now with consolidators such as ReAssure/Phoenix): premiums buy units in investment funds; monthly deductions from the fund pay for life cover; **premium/cover guaranteed only to the first review** [S15].
- **Reviews**: usually first at 10 years, then 5-yearly, then annually beyond a certain age; failed review → raise premium or cut sum assured (default on lost contact: cut cover) [S15].
- **Maximum cover** basis: minimal investment content, cheapest initial premium (~£8/month per £100k illustrative), steep premium increases at reviews as mortality cost rises ("rise sharply from age 65"). **Standard/balanced cover** basis: higher initial premium (~£50/month per £100k illustrative) builds a unit reserve that subsidises later mortality charges, aiming (not guaranteeing) a level premium [S15].
- Surrender value = unit fund value (if any) — unlike the modern protection-only products, these can have a positive surrender value [S15].
- Optional accelerated CI / permanent disability riders typically expiring at a pre-set age such as 65 [S15].
- This is the design whose review shocks generated historic conduct issues; modern UK WoL (Cell B) is deliberately non-reviewable ("guaranteed") in response [unverified inference — the causal history is not stated in the fetched documents].

### 5. Actuarial modelling references
- **Mortality**: assured-lives base tables for permanent assurances = CMI "00" series **AMC00/AMS00/AMN00, AFC00/AFS00/AFN00** (publicly downloadable) [R6]. Newer "16" series (2015–2018 experience) covers term assurance/ACI only and is CMI-Subscriber-restricted; CMI has stated it is turning to **underwritten and non-underwritten whole of life** experience next — i.e. the guaranteed-acceptance (non-underwritten) cohort is analysed separately, reflecting anti-selection vs underwritten lives [R7]. For guaranteed acceptance business, population-adjacent mortality with select effects reversed (worse-than-assured lives) is the pricing reality implied by the £71.73 vs £8.10 per-£1,000 differential [R2] — table choice itself [unverified: no public GO50 basis is disclosed by insurers].
- **Projections**: CMI Mortality Projections Model (CMI_20xx series) is the standard improvement basis; access restricted to Authorised Users/Subscribers [R9 fetched_ok=false; restriction consistent with R7] [unverified detail].
- **Lapses**: no surrender value in either modern cell → lapse = pure profit release (Cell A caveat: Royal London Payout Promise creates a paid-up liability instead of forfeiture [S9]); FCA articulates the dependence ("rely on lapses to remain profitable") [R2].
- **Solvency UK BEL**: TP = BEL + risk margin (CoC 4%), market-consistent transfer value, per PRA Rulebook Technical Provisions Part as restated on 31 Dec 2024 [R3][R4].
- **Standards**: TAS 100 v2.0 (effective 1 July 2023) applies to all UK technical actuarial work incl. modelling of these liabilities [R8]; TAS 200: Insurance applies additionally [unverified — not fetched].
- Model-relevant cash flow features checklist per product cell:
  - Cell A: level premiums to cessation age (90/95, Aviva min(30 yrs, 90)); fixed sum assured deferred 1 year (ROP year 1, ADB full sum year 1, Aviva 2× ADB for life); no surrender value; RL pro-rata paid-up; aggregation caps immaterial to per-policy models; claims interest BoE−0.5% floor 0.5% between death and payment [S1][S4][S7][S8][S9][R2].
  - Cell B: guaranteed level (or 2-for-1 escalating) premiums for life; sum assured accelerated by terminal illness; suicide 12-month ROP; milestone-benefit jump options; WoP disability rider to 70; no surrender value [S10][S11][S12][S13].

---

## Variations across insurers

| Feature | SunLife (Phoenix) [S1-S3] | L&G [S4-S6] | Aviva [S7-S8] | Royal London O50 [S9] | Zurich WoL [S10-S12] | RL menu WoL [S13-S14] |
|---|---|---|---|---|---|---|
| Cell | A | A | A | A | B | B |
| Entry ages | 49–85 | 50–80 | 50–80 | 50–80 | 18–83 (single) | 18–88 |
| Underwriting | none | none | none | none | full medical | full medical |
| Moratorium | 1 yr ROP; ADB full sum (90-day rule) | 1 yr ROP; ADB full sum (90-day rule) | 1 yr ROP; ADB full sum; **2× ADB after yr 1** | 1 yr ROP; ADB full sum | none (suicide 12m ROP) | none (suicide clause n/a — not read) |
| Premium cessation | anniv ≥ 95th bday | 90th bday | min(30 yrs, anniv after 90) | anniv ≥ 90th bday | payable for life | payable for life |
| Max sum | £18,000 (aggregate) | £10,000 (aggregate) | premium-cap-driven (£100/mo) | £10,000 (aggregate) | effectively uncapped (£40m escalation stop) | unlimited / £5m if increasing |
| Premium range | £4–£100/mo | £5–£75/mo | £7–£50/mo per plan | to £100/mo cap; floor £3.95 | min £8/mo | n/a (quote) |
| Indexation | none | RPI cap 10% (prem RPI×1.5 cap 15%) | none | none | 3%/5%/RPI cap 10% (prem 2:1) | 2–5% fixed / RPI 2–10% |
| Surrender/paid-up | none | none | none | **Payout Promise pro-rata paid-up if ≥50% paid** | none | none stated |
| Terminal illness | no | no | no | no | yes (12-month) | yes |
| Funeral option | Co-op Funeralcare, 10% discount | Dignity +£250 [unverified] | not stated | yes (provider unnamed, payout redirected) | n/a | n/a |
| Other | one-off premium reduction | premium reduction after yr 1 | inflexible by design | payment holidays ×2 | milestone benefit, WoP, free cover £1.5m | menu options (gifting, joint-life splits) |

**Representative designs.** For Cell A, the market-standard design is: guaranteed acceptance 50–80(85), fixed cash sum ≤ £10k–£18k, level premiums ceasing at 90 (some 95; Aviva min(30y, 90)), 12-month return-of-premium moratorium with full payout for accidental death from day 1, no surrender value, funeral-benefit redirection option — L&G/Royal London/SunLife are near-identical on this chassis; take **L&G Over 50s Fixed** [S4][S5] or **SunLife** [S1] as the base, with the Aviva 2× accidental multiplier, L&G RPI-linked variant and RL Payout Promise as documented alternatives. For Cell B, **Zurich Whole of Life** [S10] is the cleanest representative: guaranteed level premiums for life, sum assured on death or terminal illness, suicide-only 12-month exclusion, optional escalation at 2% premium per 1% benefit, guaranteed insurability, no cash value. The legacy unit-linked reviewable design [S15] should be modelled only as a [note] variation (maximum vs balanced cover, decennial-then-quinquennial-then-annual reviews, unit-fund surrender value).

---

## Gaps and caveats

1. **Aviva document vintage.** The GLP plan conditions (LD01052) and KFD (LD06001) fetched from Aviva's live over-50s pages are dated 11/2016. They are the versions Aviva currently publishes at the product URLs, but a newer edition may exist behind the quote journey; premium min/max (£7–£50) and the 30-year premium cap should be treated as of that document date. Aviva's current consumer page itself was not separately captured.
2. **L&G Funeral Benefit Option.** Dignity partnership and the £250 contribution appear only in third-party broker material in this research; the official funeral-benefit URL now returns generic funeral-cost content. Tagged [unverified]; verify against the L&G T&C funeral annex or by phone before relying on it.
3. **Royal London menu WoL clause detail.** The 44-page Personal Menu Plan Life Cover plan-details PDF [S14] was downloaded and structurally read, but clause-level extraction (terminal illness definition, suicide clause, WoL-specific age table inside the booklet) was not completed; WoL parameters were taken from the adviser product page [S13]. 
4. **Vitality WoL provisions.** Only the consumer page was captured [S16]; the Vitality Plan Provisions PDF (with optimiser/premium-step mechanics, LifestyleCare conversion etc.) was not verified in this session. Vitality's WoL has non-standard mechanics (Vitality Programme premium adjustments) that would need their Plan Provisions before modelling.
5. **CMI access.** cmilimited.co.uk actively refused connections (fetched_ok=false), so CMI table/model access terms are recorded from IFoA-hosted pages only [R6][R7]. Full "16"-series tables and the CMI Projections Model are subscriber-restricted; the publicly downloadable assured-lives base tables are the "00" series. No public insurer disclosure of the mortality basis actually used for guaranteed-acceptance pricing was found (expected — proprietary).
6. **Conduct sourcebook detail.** ICOBS chapter-level rules (and PROD 4 product-governance text) were not successfully fetched (FCA handbook pages render as navigation shells); Consumer Duty / fair value facts are sourced from MS24/1 Annex 2 [R2] instead. The statement that over-50s plans are sold under ICOBS (not COBS) is [unverified].
7. **Market shares / "market leader" claims.** SunLife's position as the largest over-50s provider is widely asserted in broker material but was not verified from an official source — [unverified].
8. **AIG Life / Corebridge.** AIG Life UK's whole-of-life products and the 2024 Aviva acquisition were not verified from primary sources — [unverified]; Corebridge does not operate in the UK protection market [unverified].
9. **Tax detail.** Qualifying-policy rules, and any premium-tax nuances, were not researched; only the IHT/income-tax/CGT statements in the product documents are sourced.
10. **Rate tables.** Full premium rate tables per age/smoker cell are not published by the insurers; only the example quotes recorded in S2/S6 are available publicly. A pricing model will need to infer rates from these anchors plus mortality assumptions, or use the FCA per-£1,000 averages [R2] as calibration checks.
