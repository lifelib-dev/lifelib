# Whole Life Insurance (participating and non-participating) — research notes (U.S.)

Research date / access date for all citations: 2026-08-03.
Purpose: source library for a reference implementation of a liability cash-flow projection model
(lifelib/modelx style) for U.S. whole life (WL) insurance — participating (par) and
non-participating (non-par, incl. simplified-issue final expense).

Citation discipline: every fact below is tagged [S#] (primary product document) or [R#]
(regulatory/actuarial reference) pointing at a document actually fetched and read on the access
date. Statements from general knowledge are tagged [unverified].

---

## Primary sources

### S1 — Guardian: Core Whole Life and Limited Pay Whole Life (2019 Series) Product Guide
- Publisher: The Guardian Life Insurance Company of America (doc 2019-85695; "For Internal and Producer Use Only")
- Doc type: producer guide (PDF, 23 pp.)
- URL: https://centurionagencyltd.com/guardian_whole_life_product_agent_guide_12-2019.pdf (agency file share hosting a genuine Guardian document)
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S1]):
  - Product suite (2019 series): level-pay Whole Life Paid-Up at 95 (L95, form 18-L95), Paid-Up at 99 (L99, 18-L99), Paid-Up at 121 (L121, 18-L121); limited-pay 10 Pay WL (19-L10), 15 Pay WL (19-L15), 20 Pay WL (19-L20), Life Paid-Up at 65 (L65, 19-L65).
  - All products participating; dividends declared annually by the Board; no dividend in policy year 1.
  - Maturity date = anniversary nearest attained age 121; guaranteed death benefit to age 121. At age 100 the base-policy cash value equals base face amount; CV of dividend additions equals their face; CV of PUAs equals their face.
  - Issue ages: L95/L99 0–80 (Preferred classes 18–80); L121 0–90; 10 Pay & 15 Pay 0–75; 20 Pay 0–70; L65 0–45. Rated non-smoker from age 10 (10 Pay/15 Pay) or 15 (20 Pay/L65), classes 1–3 only for ages 10–14.
  - Underwriting classes: Preferred Plus NT, Preferred NT, Non-smoker, Standard (Smoker), Rated NT, Rated Smoker; premiums identical for the best two classes (Preferred Plus and Preferred).
  - Minimum face amounts: $250,000 Preferred Plus NT; $100,000 Preferred NT; $25,000 all other classes ($100,000 all-other for L121; L121 has no $25,000 tier).
  - Premiums: guaranteed, level; payable to 95/99/121, for 10/15/20 years, or to age 65 by product. Modal factors: annual 1.000000, semi-annual 0.515000, quarterly 0.262650, monthly "Guard-O-Matic" 0.085833.
  - Policy fee: none — "continuous banding replicates a $100 policy fee."
  - Substandard: table extras up to class 16, assessed for greater of 20 years or to age 65 but not beyond premium period; rate × face/1,000; flat extras temporary or permanent (permanent = greater of 20 yrs or to 65; not allowed on 10/15 Pay); dividends permanently impacted by ratings.
  - Dividend banding: L95/L99/L121 pay higher dividend rates for base face ≥ $1,000,000; no banding on limited-pay plans.
  - Death benefit = face + rider insurance + additions + dividends left at interest + dividends credited at death + unwaived premium beyond month of death − outstanding loans and loan interest − premium due − accelerated benefits taken.
  - Lapse: 31-day grace; lapses into non-forfeiture provision elected at issue; Automatic Premium Loan available.
  - Reinstatement: within 5 years of default with evidence of insurability; overdue premiums with 6% interest compounded yearly.
  - Free look 10 days (state variations); refund of premiums.
  - MEC: 7-pay test per IRC 7702A; 7-pay premium rates based on the 2017 CSO composite table; deemed-cash-value and material-change mechanics.
  - Loans: allowed anytime (incl. year 1) up to CV of base + adds, less loans/interest to next anniversary; unpaid interest capitalized on anniversary; initial fixed loan rate 6% (5.66038% payable in advance) WITH direct recognition; fixed rate drops 6% → 4% at the later of the 20th anniversary or anniversary nearest 65 (L95/99/121), later of the 10th/15th/20th anniversary (per product) or age 60 (limited pay), or age 65 (L65); with direct recognition, loans at the 4% rate get lower dividends than at 6%.
  - Variable loan rate (VLR) option: electable at 10th anniversary; irrevocable; NO direct recognition under VLR; max VLR = greater of Moody's Corporate Bond Yield Average — Monthly Average Corporates (quarterly lookup by anniversary month: Oct/Jan/Apr/Jul) or 4.5%; if prior declared rate is within 0.5% of the maximum, the maximum stays at the prior declared rate.
  - Guaranteed cash values: based on 4.0% interest and the 2017 CSO Composite Sex-Distinct table; same guaranteed CV for rated and unrated. First policy year with guaranteed CV: L95 yr 1; L99 yr 3; L121 yr 3; 10 Pay yr 1; 15 Pay yr 1; 20 Pay yr 2; L65 yr 2. Guaranteed CV = face at age 100 (all products except L121, where at 121).
  - Riders: Paid-Up Additions (18-PUA), Index Participation Feature (15-IPR), Waiver of Premium, Waiver of Specified Amount, Applicant's WP, DuoGuard (level-pay only), Enhanced Accelerated Benefit, LTC Services rider, GIO/GIOPlus, Accidental Death Benefit, Exchange of Insureds, Lifetime Protection Builder (level-pay only), Select Security, 10-Year Renewable Term (RTR-10, 16-15DTR).
  - Conversions/exchanges: term conversions permitted to all products; conversion credits on all but 10/15 Pay; 1035 exchanges permitted (no loan carry-over).
  - Gender-distinct pricing except Montana (unisex).
  - Backdating up to 6 months where permitted.

### S2 — Guardian: Dividend Manual, Whole Life (2017 edition)
- Publisher: The Guardian Life Insurance Company of America (doc 2019-81397; producer use only)
- Doc type: producer dividend manual (PDF, 5 pp.)
- URL: https://www.centurionagencyltd.com/guardian_life_dividend_options_12-2019.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S2]):
  - Guardian is a mutual insurer; dividends paid to participating policyholders every year since 1868; not guaranteed; declared annually by the Board.
  - Dividend options: A Cash; B Reduce Premium (excess reduces loan interest); C Dividend Accumulation (interest rate announced with each year's dividend scale, changes annually); D Paid-Up Additions (default on permanent plans; option C default on par term); F OYT up to policy cash value, balance to dividend additions; G OYT up to CV, balance to reduce premium; I LTC Additions (only at issue, only with LTC rider); L OYT up to 2× face, balance to paid-up additions; P OYT up to 2× face, balance to reduce premium; Q OYT with Target Face Amount; R Increasing Q; S Premium Offset; U Dividends repay loan principal (interest billed separately).
  - Option Q: OYT + dividend additions + PUA-rider additions sum to a Target Face Amount fixed at issue; term portion guaranteed only first 2 years; if dividend insufficient, non-loaned additions surrendered to pay term cost; Target max = 9× base face; Target min = $25,000; minimum PUA rider purchase required.
  - Option R (Increasing Q): target increases annually for 20 years starting year 3 — constant increases up to 10% of initial total death benefit, or compound up to 6% of prior-year total DB; initial target max = base face (50/50 blend); min $25,000; if dividend+additions insufficient, policyowner billed for the difference.
  - Option S (Premium Offset): annual dividend pays annual premium, shortfall covered by surrendering non-loaned paid-up (rider) additions; electable at issue with sufficiently large initial PUA rider payment, or later when additions suffice; if values insufficient the dividend buys PUAs and full premium is due.
  - Options Q/R: once switched away, cannot switch back. Option changes effective on next anniversary.
  - Dividends paid in cash / used to repay loans above cost basis may be ordinary income.

### S3 — MassMutual: Whole Life Series Product Reference Guide
- Publisher: Massachusetts Mutual Life Insurance Company (LI10804e-mmsd 522; "For financial professionals")
- Doc type: producer product reference guide (PDF, 8 sections)
- URL: https://www.aimcorfileshare.com/download.php?idFile=4417 (distributor file share hosting a genuine MassMutual document)
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S3]):
  - Portfolio: Whole Life 100 (premiums to age 100, lowest premium), Whole Life 65 (paid up at 65), Whole Life 10/12/15/20 Pay, Whole Life High Early Cash Value (HECV, premiums to age 85, COLI/executive-benefit oriented). All level-premium participating policies; guaranteed level face; guaranteed CV = face at age 100.
  - Policy forms: Whole Life Legacy series MMWL-2018 / ICC18-MMWL (and MMWLA-2018 / ICC18-MMWLA); digital platform WL-2018 / ICC18WL.
  - Issue ages (non-qualified): WL100 0–90; WL65 0–60; 10/12/15/20 Pay 0–75; HECV 0–75. Qualified market from age 17. Gender-distinct except Montana (unisex); qualified policies unisex.
  - Minimum face: $25,000 generally; $100,000 for 10 Pay and 12 Pay and HECV; $10,000 qualified WL100; $1,000 conversion/GIR-exercise segments.
  - Policy fee: $50 annually (WL100, WL65, HECV); none on 10/12/15/20 Pay.
  - Policy size bands (drive premiums and dividends): e.g. WL100 Band 1 $1,000–$24,999 … Band 5 $1M+; 10/12/15/20 Pay Band 1 $25,000–$99,999, Band 2 $100,000–$999,999(–$249,999/$999,999 tiering), Band 4 $1M+; band resets on face changes.
  - Guaranteed cash value interest rates: WL100 3.75% to age 100 (0% thereafter); WL65 3%; HECV 3%; 10 Pay 2%; 12 Pay 3%; 15 Pay 2.5%; 20 Pay 3% — all with CV = face at age 100. (Note the guaranteed interest basis varies BY PRODUCT within one insurer.)
  - Modal factors: semi-annual 0.5117; quarterly 0.2589; monthly 0.0870.
  - Risk classes: Ultra Preferred NT, Select Preferred NT, Non-Tobacco, Select Preferred Tobacco, Tobacco; below $50,000 face only NT/Tobacco; juveniles (0–16) NT only; table ratings A,B,C,D,E,F,H,J,L,P and flat extras; permanent ratings payable to 65 or 20 years if longer (not beyond premium period); preferred classes unavailable with table ratings/medical flat extras.
  - Premiums: basic annual premium varies by issue age, gender, class, band; no minimum annual premium; annual premium = basic + substandard + rider premiums.
  - Dividends: vary by gender, risk class, face band, issue age, duration, tax-qualified status; not guaranteed; first-year dividend paid (not contingent on 2nd-year premium); dividends may vary if fixed loan rate elected and loan outstanding (= direct recognition on the fixed-rate regime).
  - Dividend options: Cash (CS); Reduce Premiums — excess to cash (RPC) or to PUAs (RPD); Paid-Up Additions (PD); Accumulation (DA); LISR/Flex (FLX); One-Year Term with excess to cash/PUA/reduce-premium (TCS/TPD/TRP — via Yearly Term Purchase rider, OYT amount = guaranteed CV); Reduce Loan (RN); Reduce Loan Interest (RI). Options are non-contractual (currently available).
  - Loans: anytime; either adjustable loan rate (ALR — default, no direct recognition) or fixed 6% with direct recognition; choice at issue, cannot change; ALR max = Moody's composite yield on seasoned corporate bonds (monthly average) or guaranteed rate + 1% if higher; LISR requires ALR.
  - Non-forfeiture options: cash, extended term insurance, reduced paid-up.
  - Reinstatement: within 31 days of grace-period end without evidence; within 5 years with evidence; back premiums + 6% interest.
  - Payment options: lump sum or lifetime monthly income per Life Income Payment Option Rates; Alternate Life Income allows SPIA-rate-based payout.
  - Face amount increases (WL100/65/HECV only): new coverage segments with own issue age/class/premium/dividends; min increase $25,000; increase ages capped (to insured age 90/60/75 by product); one policy fee.
  - Alternate Payment Option (APO): dividends + surrender of PUA cash value pay premiums (full or partial APO; annual mode for full APO).
  - Riders: Waiver of Premium (issue 0–59, 6-month wait, own-occ 60 months, terminates at 65; face limits $6M/$4M for 10/12/15-Pay, $8M/$5M others); Additional Life Insurance Rider ALIR (PUA rider; scheduled + unscheduled catch-up payments; expense charge 7.5% of each payment on 10/15 Pay, 10% on others, guaranteed max same; min initial scheduled payment $300/yr; +10%/yr increases without evidence up to 100% cumulative; purchases PUAs); PALIR (flexible-timing ALIR variant, same charges, issue-only); Life Insurance Supplement Rider LISR (term+PUA blend to a Target Face Amount with crossover; expense charge current 8% capped 10% on 10/15 Pay, current 10% capped 12% others; TFA 300% of base max, $50,000 min; requires FLX dividend option; term rates current & guaranteed); LTCAccess rider (accelerates up to 90% of face; residual ≥ $25,000; monthly benefit = pool / benefit period of 2,3,4,5,6,10 yrs; MMB min $3,000 max $30,000 at issue; optional 4% simple annual MMB increases; benefit payments create liens on DB and CV); Renewable Term Rider RTR (annually renewable to age 95; current premiums level 10 yrs then annually increasing, guaranteed max; min $100,000; max 20× base face; convertible ≤ 10 yrs/age 65); Guaranteed Insurability Rider GIR (issue 0–40; option ages 25,28,31,34,37,40,43,46; option amount min $25,000, max lesser of 2× base or $125,000; substitute options for marriage/birth/adoption; terminates at 46); Yearly Term Purchase (YTP — auto-attached under OYT dividend option; OYT amount = year-end guaranteed CV); Transfer of Insured; Accelerated Death Benefit for terminal illness (12 months).
  - MEC: limited-pay (10/12/15/20 Pay) products' premiums approach 7-pay limits, so face decreases can retroactively create MECs; MEC distributions taxed gain-first + 10% penalty pre-59½.
  - 1035 exchanges accepted incl. with loans (loan carried as ALIR payment; min net 1035 cash $10,000).

### S4 — Northwestern Mutual: "Dividend paying whole life insurance" (product/dividend page)
- Publisher: The Northwestern Mutual Life Insurance Company
- Doc type: consumer product page (HTML)
- URL: https://www.northwesternmutual.com/life-insurance/whole-life-insurance/dividend-paying-whole-life-insurance/
- Retrieved: YES (WebFetch)
- Facts extracted (all [S4]):
  - 2026 dividend interest rate: 5.75% "for most policies."
  - Published dividend mechanics (three-factor formula): annual dividend = (beginning guaranteed accumulated value + gross annual premium − mortality & expense charge based on actual company results, credited with the current dividend interest rate) − ending guaranteed accumulated value. I.e., dividend = actual-experience accumulated value − guaranteed accumulated value.
  - Dividend options shown: increase policy values (paid-up additions), offset premiums, cash.
  - Dividends not guaranteed; dividend scale reviewed annually by Board of Trustees; paid every year since 1872.
  - Whole life policies in the company's General Account are dividend-eligible.
  - Illustrative example: $2,100 annual dividend in policy year 10 (specific example case).

### S5 — Northwestern Mutual: 2026 dividend announcement (press release, Oct 28, 2025)
- Publisher: Northwestern Mutual (newsroom)
- Doc type: press release (HTML)
- URL: https://news.northwesternmutual.com/2025-10-28-Northwestern-Mutual-Announces-Historic-9-2-Billion-Dividend-Payout-in-2026-A-Powerful-Demonstration-of-Companys-Enduring-Commitment-to-Policyowners
- Retrieved: YES (WebFetch)
- Facts extracted (all [S5]):
  - Total expected 2026 dividend payout $9.2 billion, of which ≈ $7.9 billion to whole life policyowners; 155 consecutive years of dividends; ≈ $170 billion cumulative.
  - Most policyowners elect paid-up additional insurance, which increases accumulated value and death benefit.

### S6 — Mutual of Omaha (United of Omaha): Living Promise Whole Life — consumer brochure (128136_0323)
- Publisher: United of Omaha Life Insurance Company (Mutual of Omaha company)
- Doc type: consumer brochure (PDF, 2023)
- URL: https://choicemutual.com/wp-content/uploads/2023/08/2023MutualofOmahabrochure.pdf (agency hosting of genuine brochure)
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S6]):
  - Final-expense simplified-issue whole life; no medical exams, health-question underwriting; premiums guaranteed never to increase.
  - Level Benefit Plan: issue ages 45–85; face $2,000–$50,000 ($5,000–$50,000 in WA); includes Accelerated DB for terminal illness (12-month prognosis) or 90-day nursing home confinement (ICC12L084R); optional Accidental Death Benefit rider ICC12L082R (additional DB = face).
  - Graded Benefit Plan: issue ages 45–80; face $2,000–$20,000; death from natural causes in first 2 years pays return of premium + 10%; full benefit for accidental death from day 1; not available AR/MT/NC.
  - Policy forms: Level ICC12L080P (FL D354LFL12P); Graded ICC12L081P (FL D355LFL12P).

### S7 — United of Omaha: Living Promise Product and Underwriting Guide (California)
- Publisher: United of Omaha Life Insurance Company (form 142658, producer use only)
- Doc type: producer product & underwriting guide with rate tables (PDF)
- URL: https://www.datocms-assets.com/13639/1563367329-moo-livingpromise-uw-guide.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S7]):
  - CA version: Level plan issue ages 45–85, face $2,000–$40,000, classes Standard Tobacco/Nontobacco; Graded 45–80, $2,000–$20,000, single Standard class (no tobacco split).
  - Underwriting: MIB, prescription-database check, random phone interviews; knock-out application questions Part 1 (decline) / Part 2 (graded only); point-of-sale tele-underwriting (Apptical).
  - FULL annual premium rate tables per $1,000 by age/sex/tobacco, e.g. Level male NT age 45 $24.99, age 65 $59.05, age 85 $202.19; female NT age 65 $42.48; Graded male age 65 $103.00, female age 65 $69.50. Annual policy fee $36 added to all.
  - Modal factors: annual 1.00, semi-annual 0.52, quarterly 0.275, monthly BSP 0.089.
  - Suicide exclusion 2 years (1 year ND) — return of premium less loans.
  - Build chart (height/weight limits per plan); aggregate limits: ≤ $40,000 Living Promise Level, ≤ $50,000 all simplified-issue with United of Omaha; ≤ $20,000 Graded, ≤ $25,000 all graded coverage.

### S8 — Mutual of Omaha: Living Promise plan highlights sheet (615060)
- Publisher: United of Omaha Life Insurance Company
- Doc type: consumer highlight sheet (PDF)
- URL: https://producer.mutualofomaha.com/enterprise/wcm/connect/producer.mutualofomaha.com-9968/efbe83e0-01d4-4275-b956-7d393e577666/45107_living-promise-client-highlight-sheet.pdf?MOD=AJPERES&CVID=nz81aeV
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S8]):
  - Maturity age 100 (120 in FL): face amount paid at maturity less outstanding loans and loan interest.
  - Builds cash value that may be borrowed against; benefits never decrease; premiums never increase; cannot be cancelled while premiums paid.
  - Level plan face range restated as $2,000–$50,000 (WA $5,000–$50,000).

### S9 — New York Life: Secure Wealth Plus product page
- Publisher: New York Life Insurance Company
- Doc type: consumer product page with FAQ (HTML)
- URL: https://www.newyorklife.com/products/insurance/life-insurance/accumulation-focused-life/secure-wealth-plus
- Retrieved: YES (direct HTTP download; WebFetch was blocked with 403)
- Facts extracted (all [S9]):
  - Secure Wealth Plus = permanent participating whole life optimized for early cash value accumulation (lower initial DB per premium dollar than protection-focused WL).
  - Policy form ICC18217-50P (4/18); issued by New York Life Insurance Company (NY, NY).
  - Cash value guaranteed to grow each year for life; dividend-eligible; NYL has paid dividends every year since 1854 ("168 years" in FAQ).
  - Loans: borrow up to maximum loan value at a VARIABLE loan interest rate; loan balance + accrued interest reduces CSV and death benefit; surrenders = surrender of paid-up additional insurance.
  - Expedited underwriting (24–48 hrs, no labs) for annual premiums ≤ $150,000 (adults) / ≤ $100,000 (ages 0–17); larger premiums require full underwriting.
  - MEC framework explained (7-pay, material change, gain-first taxation, 10% penalty pre-59½; withdrawal-with-DB-reduction rule within first 15 years).

### S10 — New York Life: "New York Life Launches Wealth Plus" press release (Sept 26, 2022)
- Publisher: New York Life Insurance Company
- Doc type: press release (HTML)
- URL: https://www.newyorklife.com/newsroom/2022/new-york-life-launches-wealth-plus
- Retrieved: YES (direct HTTP download)
- Facts extracted (all [S10]):
  - Secure Wealth Plus: 10-year premium-paying whole life, issue ages 0–60, minimum annual premium $10,000.
  - Positioned with Market Wealth Plus (VUL, form ICC22-322-32P, NYLIAC) as accumulation-oriented "Wealth Plus" series; dividends not guaranteed.

### S11 — Penn Mutual: Guaranteed Whole Life II — Features and Options (Coverage Riders), T4522
- Publisher: The Penn Mutual Life Insurance Company
- Doc type: consumer rider/feature supplement to the product brochure (PDF, 9 pp.)
- URL: https://gateway.pennmutual.com/static-assets/files/products/riders/t4522.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S11]):
  - Base policy form ICC18-TL (Guaranteed Whole Life II); participating (dividends referenced throughout; not guaranteed); not offered in NY.
  - Accelerated Death Benefit Rider (terminal illness, 12-month prognosis): auto-included, issue ages 0–85; acceleration ≥ $10,000 and ≤ min($250,000, 50% of face).
  - Chronic Illness Accelerated Benefit Rider: auto-included, issue 20–85, 2-of-6 ADLs or severe cognitive impairment, 90-day condition, no charge until exercised.
  - Accelerated Permanent Paid-Up Additions Rider (issue 0–85): PUA purchases up to an Annual Payment Limit set at application; min payment $25/monthly anniversary; requires PUA dividend option; replaces Flexible Protection Rider term faster.
  - Enhanced Permanent Paid-Up Additions Rider (issue 0–85): PUA purchases up to Annual Payment Limit and duration set at issue; min $25; dividend option must be PUAs or premium reduction.
  - Flexible Protection Rider (issue 0–85, issue-only, payment periods ≥ 10 yrs): term + PUA blend; dividends must buy PUAs; term gradually replaced by paid-up insurance.
  - Disability Waiver of Premium (issue 5–55; 6-month wait; 2-yr own-occ then any-occ; terminates at 65; unavailable if waiver-covered face across policies > $5,000,000; payment periods ≥ 10 yrs) and Enhanced version (6-yr own-occ).
  - Accidental Death Benefit (issue 0–60; min $5,000; max lesser of 2× face or $50,000 ages 0–25 / $250,000 ages 26–60; ends at 70).
  - Children's Term Insurance Rider (issue 0–17; $5,000 increments to $25,000; converts up to 5× at child age 23 without evidence).
  - Guaranteed Purchase Option Rider (issue 0–40; option ages 22,25,28,31,34,37,40,43,46 via new WL policy; alternates for marriage/birth/adoption).
  - Overloan Protection Benefit Rider: if loan > 99% of CV, converts to reduced paid-up with loan; insured ≥ 75 and policy in force ≥ 15 years.
  - Business riders: Supplemental Exchange (substitute insured), Surrender Value Enhancement (return of premiums less COI if surrendered within first 5 years; business policies, annual mode, PUA dividend option).

### S12 — Penn Mutual: Protection Whole Life II brochure (PM9135)
- Publisher: The Penn Mutual Life Insurance Company
- Doc type: consumer brochure (PDF, 6 pp., March 2025)
- URL: https://www.pennmutual.com/static-assets/v1/item/4bdcd58e-0743-a0e0-35cc-332143082ed9/attachments/Protection%20Whole%20Life%20II.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [S12]):
  - Protection Whole Life II, form ICC22-TLP; not offered in NY.
  - Death benefit guaranteed to age 121; premiums guaranteed never to increase, paid to age 100; guaranteed cash value growth.
  - Participating: eligible for annual dividends; dividend options: grow cash value/death benefit (PUAs), reduce premiums, cash; dividends paid every year since 1847.
  - Chronic and terminal illness acceleration built in; optional riders: EPPUA, Children's Term, ADB, Disability WP / Enhanced WP, Guaranteed Purchase Option.
  - Accelerated Client Experience (ACE): fully underwritten issuance in hours, often without exams/labs.

### S13 — Penn Mutual: "New Accumulation Whole Life" press release (Sept 2024)
- Publisher: The Penn Mutual Life Insurance Company
- Doc type: press release (HTML)
- URL: https://www.pennmutual.com/about-us/news/press-releases/2024/09/new-accumulation-whole-life
- Retrieved: YES (WebFetch)
- Facts extracted (all [S13]):
  - Accumulation Whole Life: premium payment periods from 5 years to age 100 (max-funded and short-pay designs); 13 riders incl. Overloan Protection and two PUA riders; annual dividends (never guaranteed); dividends paid 175+ years; not available in NY.

### S14 — IULvsWholeLife.com: "2026 Whole Life Dividend Rates: Five Mutual Carriers Verified"
- Publisher: IULvsWholeLife.com (independent aggregator — SECONDARY source; use with care)
- Doc type: dividend-scale comparison article (HTML)
- URL: https://iulvswholelife.com/dividend-rates/
- Retrieved: YES (WebFetch)
- Facts extracted (all [S14], secondary):
  - 2026 declared dividend interest rates (2025 in parens): MassMutual 6.60% (6.40%), Northwestern Mutual 5.75% (5.50%), New York Life 6.40% (6.20%), Guardian 6.25% (6.10%), Penn Mutual 6.00% (6.00%).
  - 2026 payouts: MassMutual $2.9B; Northwestern Mutual $9.2B; New York Life $2.78B; Guardian $1.7B; Penn Mutual $300M. (NM figures corroborated by [S5]; MassMutual figures corroborated by a WebSearch snippet of the company announcement, not directly fetched.)
  - DIR is not a policy yield: expense/mortality experience also drives the dividend; PUAs themselves earn dividends (compounding).

---

## Regulatory and actuarial references

### R1 — NAIC Model 808: Standard Nonforfeiture Law for Life Insurance
- Publisher: National Association of Insurance Commissioners (Jan 2014 printing)
- URL: https://content.naic.org/sites/default/files/model-law-808.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [R1]):
  - Cash surrender value on default ≥ PV(future guaranteed benefits incl. existing paid-up additions) − PV(future adjusted premiums) − policy indebtedness (Sec. 3).
  - Paid-up nonforfeiture benefit: PV at default ≥ the cash surrender value (Sec. 4) — basis of reduced paid-up and extended term options.
  - Adjusted premium (Sec. 5c, nonforfeiture net level premium method, post-1989 policies): uniform percentage of gross premiums (excluding rating extras and any stated policy fee) such that PV(adjusted premiums) at issue = PV(future guaranteed benefits) + 1% of the amount of insurance (or of the average amount in first 10 years) + 125% of the nonforfeiture net level premium (NNLP capped at 4% of amount of insurance) — the statutory acquisition-expense allowance.
  - Older Sec. 5 method (pre-5c): expense allowance components 2% of amount + 40% of first-year adjusted premium (+ additional 25% component); 1941/1958/1980 CSO by era.
  - Nonforfeiture interest rate (pre-Valuation-Manual issues): 125% of the calendar-year statutory valuation interest rate rounded to nearer ¼%, floor 4.00%; for policies issued on/after the VM operative date, the rate is provided by the Valuation Manual (Sec. 5c I).
  - Mortality: 1980 CSO (with optional 10-year select factors) for the 1980-era regime; smoker/nonsmoker and unisex variants permitted; substandard may use modified tables.
  - Refiling of nonforfeiture bases for interest/mortality changes does not require refiling other policy provisions.
  - Consistency-of-progression requirements for CV schedules; indeterminate-premium plans handled by commissioner rules (Sec. 6).

### R2 — NAIC Model 582: Life Insurance Illustrations Model Regulation
- Publisher: NAIC (April 2001 printing)
- URL: https://content.naic.org/sites/default/files/model-law-582.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [R2]):
  - Key definitions verified: "currently payable scale" (in effect or declared within 95 days); "disciplined current scale" (DCS — reasonably based on actual recent historical experience, certified annually by the illustration actuary; no projected improvement; expenses ≥ minimum assumed expenses); "illustrated scale" = not more favorable than the lesser of DCS and currently payable scale.
  - Guaranteed elements vs non-guaranteed elements defined; illustrations must be basic / supplemental / in-force types.
  - Self-supporting illustration test: using DCS experience assumptions, at all illustrated points from the 15th anniversary (20th for second-to-die), accumulated value of policy cash flows ≥ total policyowner value available (CSV + other elective benefits).
  - Lapse-supported illustration: fails self-support when persistency = DCS persistency for 5 years then 100% thereafter. Insurers may not illustrate scales that are lapse-supported or not self-supporting.
  - Dividend accumulation/interest credits in illustrations cannot exceed the earned interest rate underlying the DCS.
  - Illustration actuary: annual certification to board and commissioner; separate annual officer certification; error notification duties.
  - Minimum assumed expenses: fully allocated, marginal (only if > GRET), or an approved generally recognized expense table (GRET).

### R3 — NAIC Valuation Manual, 2025 edition (VM-02, VM-20, VM-M and framework sections)
- Publisher: NAIC
- URL: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (4.4 MB PDF downloaded; 457 pp.; full text extracted)
- Facts extracted (all [R3]):
  - VM-02 (Minimum Nonforfeiture Mortality and Interest): ordinary life issued 2017–2019 uses 2001 CSO for minimum nonforfeiture; 2017 CSO permitted from Jan 1, 2017 and MANDATORY for issues on/after Jan 1, 2020 (per Model 808 Sec. 5cH(6)); preferred-structure tables NOT allowed for nonforfeiture; smoker/nonsmoker or composite; ultimate or select & ultimate at company option; gender-blended tables for unisex pricing; preneed uses 1980 CSO; industrial uses 1961 CSI; ~4.5-year transition pattern recommended for future CSO adoptions.
  - VM-20 (PBR for Life Products): minimum reserve = f(net premium reserve NPR, deterministic reserve DR, stochastic reserve SR) with exclusion tests. NPR computed seriatim (Sec. 3); NPR mortality = 2001 CSO for pre-2020 issues (with election of 2017 CSO from 2017), 2017 CSO REQUIRED for ordinary life issued on/after Jan 1, 2020; composite vs smoker-distinct rules mirror nonforfeiture; 2017 CSO Preferred Class Structure tables may substitute for reserves (not nonforfeiture) with annual actuarial certification vs the corresponding VBT.
  - Exclusion tests: Stochastic Exclusion Test (ratio test ≤ threshold, demonstration, or certification — annually); Deterministic Exclusion Test (DET) passes if sum of valuation net premiums ≤ sum of guaranteed gross premiums (typical for traditional par WL with substantial gross premiums), so many WL blocks hold NPR only.
  - Life PBR Exemption: companies with < $300M individual life "exemption premiums" (group < $600M combined) may file annual exemption; exempt business is valued under VM-A / VM-C (essentially pre-PBR CRVM/net-premium requirements: "reserve requirements for … companies exempt pursuant to the life PBR exemption … are provided by VM-A and VM-C").
  - YRT-assumed coverage NPR = ½ year's cost of insurance on reinsured NAR.
  - VM-M definitions: 2017 CSO developed by the CSO Subgroup of the Joint American Academy of Actuaries Life Experience Committee and SOA Preferred Mortality Oversight Group from the 2015 VBT; adopted by NAIC April 2016; includes ultimate and select&ultimate forms, smoker/nonsmoker and composite, M/F, ANB/ALB; separate 2017 CSO Preferred Class Structure tables (super-preferred NS, preferred NS, residual NS, preferred SM, residual SM).
  - Actuarial Guidelines are carried in VM-C as part of minimum reserve requirements for applicable business [R3].

### R4 — IRC §7702 (Cornell LII text)
- Publisher: Legal Information Institute, Cornell Law School (26 U.S.C. §7702)
- URL: https://www.law.cornell.edu/uscode/text/26/7702
- Retrieved: YES (WebFetch)
- Facts extracted (all [R4]):
  - Federal definition of life insurance: must satisfy either the cash value accumulation test (CSV ≤ net single premium for future benefits at all times) or the guideline premium test + cash value corridor.
  - Corridor: DB ≥ specified percentage of CSV, grading from 250% (ages ≤ 40) down to 100% (ages 90–95).
  - Interest assumptions: pre-2021 fixed 4% (CVAT/GLP) and 6% (GSP); for contracts issued after 2020 the rates are the §7702 "applicable rates" (insurance interest rate tied to the lesser of the §7702 valuation interest rate and applicable federal rates; 2% transitional rate for 2021 issues). Whole life gross premium levels and CVAT compliance are directly affected by this 2021 change.

### R5 — IRC §7702A (Cornell LII text)
- Publisher: Legal Information Institute, Cornell Law School (26 U.S.C. §7702A)
- URL: https://www.law.cornell.edu/uscode/text/26/7702A
- Retrieved: YES (WebFetch)
- Facts extracted (all [R5]):
  - Modified endowment contract = contract meeting §7702 but failing the 7-pay test (cumulative premiums in first 7 contract years > net level premiums for a policy paid-up after 7 annual payments); applies to contracts entered into on/after June 21, 1988.
  - Material change restarts 7-pay testing (DB increases, added qualified benefits), with exceptions for benefits funded by necessary premiums and interest crediting.
  - Distributions in the 2 years before failing the test are treated as made in anticipation of failure; MEC distributions taxed under §72 (gain-first) — relevant to loans/withdrawals modeling on limited-pay WL.
  - Small-contract rule: for death benefits ≤ $10,000, each 7-pay premium is increased by $75.

### R6 — ASOP No. 15: Dividends for Individual Participating Life Insurance, Annuities, and Disability Insurance
- Publisher: Actuarial Standards Board (revised edition adopted March 2006; deviation language updated May 2011; Doc. No. 134)
- URL: https://www.actuarialstandardsboard.org/wp-content/uploads/2014/06/asop015_134.pdf
- Retrieved: YES (PDF downloaded, full text extracted)
- Facts extracted (all [R6]):
  - Definitions: contribution principle (aggregate divisible surplus allocated to policies in proportion to their contribution to surplus); dividend framework (structure by which insurer allocates divisible surplus); divisible surplus (aggregate amount available for distribution as dividends); dividend determination (allocation of divisible surplus incl. dividend factors); experience factors.
  - The actuary should use the contribution principle in determining dividends and may apply it annually or over an extended period; dividend factors should be developed to produce an estimated aggregate payout equal to divisible surplus.
  - Required actuarial report/disclosures: description of process and dividend framework, whether the contribution principle was followed, material changes since prior determination.
  - Historical basis: 1980/1985 Academy Recommendations on dividend principles/practices.

### R7 — ASOP No. 2: Nonguaranteed Elements for Life Insurance and Annuity Products (ASB standard page)
- Publisher: Actuarial Standards Board
- URL: https://www.actuarialstandardsboard.org/asops/asop-no-2-nonguaranteed-elements-for-life-insurance-and-annuity-products/
- Retrieved: YES (WebFetch)
- Facts extracted (all [R7]):
  - Adopted September 2021; effective June 1, 2022. Governs NGE determination (premiums/charges/credits changeable at insurer discretion), e.g. indeterminate-premium non-par life; explicitly EXCLUDES policyholder dividends, which remain under ASOP 15.
  - Requires understanding of insurer's NGE framework: determination policy, policy classes, profitability objectives; NGE scales based on reasonable expectations of future experience; no recouping of past losses.

### R8 — SOA: 2017 CSO Tables (table repository page)
- Publisher: Society of Actuaries
- URL: https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- Retrieved: YES (WebFetch)
- Facts extracted (all [R8]):
  - Official repository of 2017 CSO table set: male/female, smoker/nonsmoker, composite, gender-blended, preferred class structure, loaded and unloaded, ANB and ALB, select&ultimate and ultimate variants (machine-readable downloads).

### R9 — SOA/ILEC: 2019 Individual Life Insurance Mortality Experience Report (2012–2019)
- Publisher: Society of Actuaries Research Institute, Individual Life Experience Committee (Oct 2024)
- URL: https://www.soa.org/resources/research-reports/2024/ilec-mort-2012-19 (report PDF: https://www.soa.org/globalassets/assets/files/resources/research-report/2024/ilec-mort-main.pdf)
- Retrieved: YES (landing page fetched; PDF not separately parsed)
- Facts extracted (all [R9]):
  - Observation years 2012–2019; industry mortality experience relative to standard tables (2015 VBT basis) with trends by key policy characteristics (product type incl. whole life/perm, face band, duration).
  - Data collection transition: MIB was statistical agent for 2012–2017 data; NAIC is the statistical agent from 2018 on.
  - Use for the model: source of realistic experience-mortality assumptions relative to 2015 VBT for par WL dividend/experience modeling.

### R10 — ASOP No. 24: Compliance with the NAIC Life Insurance Illustrations Model Regulation
- Publisher: Actuarial Standards Board (September 2024 revision, Doc. No. 217)
- URL: https://www.actuarialstandardsboard.org/wp-content/uploads/2024/09/asop024_217.pdf
- Retrieved: NO (identified via search; not fetched/parsed — listed as a known reference)
- Notes: governs illustration-actuary work under Model 582 (DCS certification, self-support/lapse-support testing). [unverified beyond title/publisher/URL]

### R11 — NAIC Model 820: Standard Valuation Law
- Publisher: NAIC
- URL: https://content.naic.org/sites/default/files/inline-files/MDL-820.pdf
- Retrieved: NO (download blocked — bot challenge HTML returned; listed as a known reference)
- Notes: statutory home of CRVM, calendar-year valuation interest rates, and the Valuation Manual's authority; the operative-date and valuation-rate cross-references appear inside Model 808 [R1] and the Valuation Manual [R3]. [unverified beyond title/publisher/URL]

---

## Extracted specifications

All facts tagged. "Par WL" = participating whole life (Guardian/MassMutual/NYL/Penn Mutual/Northwestern Mutual designs); "FE WL" = final-expense simplified-issue WL (United of Omaha Living Promise).

### 1. Product structure and premium patterns
- Canonical par WL chassis: level guaranteed premiums, level guaranteed face, guaranteed cash value schedule reaching the face amount at age 100 (endowment-at-100 design), with maturity/coverage continuing to age 121 [S1][S3].
- Premium-paying variants observed:
  - Level pay to age 95 / 99 / 121 (Guardian L95/L99/L121) [S1]; to age 100 (MassMutual WL100 [S3]; Penn Mutual Protection WL II premiums to age 100 [S12]).
  - Limited pay: 10/15/20 pay + paid-up-at-65 (Guardian) [S1]; 10/12/15/20 pay + WL65 + pay-to-85 HECV (MassMutual) [S3]; 10-year pay (NYL Secure Wealth Plus) [S10]; payment periods 5 years to age 100 (Penn Mutual Accumulation WL) [S13].
  - FE WL: continuous premiums to maturity at age 100 (120 in FL) [S8].
- Issue-age ranges: broad 0–80/0–90 for level pay [S1][S3]; shortened for limited pay consistent with the premium period (e.g. L65 issue 0–45 [S1]; WL65 0–60 [S3]; Secure Wealth Plus 0–60 [S10]); FE WL 45–85 level / 45–80 graded [S6][S7].
- Face bands/minimums: par WL minimum faces $25,000–$250,000 varying by class [S1], $25,000–$100,000 by product [S3]; premium/dividend rates vary by face band [S1][S3]; NYL uses a premium minimum instead ($10,000/yr) [S10]; FE WL face $2,000–$50,000 [S6][S8].
- Policy fee: Guardian none — banding replicates a $100 fee [S1]; MassMutual $50/yr (waived on limited pay) [S3]; United of Omaha $36/yr added to rated premium [S7].
- Modal factors (annualized premium loads): Guardian SA 0.515 / Q 0.26265 / M 0.085833 [S1]; MassMutual SA 0.5117 / Q 0.2589 / M 0.0870 [S3]; United of Omaha SA 0.52 / Q 0.275 / M 0.089 [S7].
- Actual FE premium rates per $1,000 (CA): e.g. Level male NT: 45→$24.99, 65→$59.05, 85→$202.19; Level female NT: 65→$42.48; Graded male 65→$103.00; +$36 policy fee [S7].

### 2. Guaranteed cash values / nonforfeiture
- Statutory basis: CSV ≥ PV(guaranteed benefits) − PV(adjusted premiums) − debt, with the adjusted-premium expense allowance = 1% of amount + 125% of NNLP (NNLP capped at 4% of amount) [R1]; paid-up NFB actuarially equivalent to CSV [R1]; nonforfeiture interest = 125% of statutory valuation rate (min 4.00%) pre-VM, VM-prescribed after [R1][R3].
- Nonforfeiture mortality: 2017 CSO mandatory for issues ≥ 2020-01-01 (2001 CSO for 2017–2019 issues unless elected); composite or smoker-distinct; ultimate or S&U; preferred-structure tables prohibited for nonforfeiture [R3].
- Observed contractual guarantees: Guardian: 4% interest, 2017 CSO composite sex-distinct; CV=face at 100 (121 for L121); first guaranteed CV in year 1–3 depending on product [S1]. MassMutual: guaranteed interest varies by product — 3.75% (WL100), 3% (WL65/HECV/12&20 Pay), 2.5% (15 Pay), 2% (10 Pay), 0% after age 100; CV=face at 100 [S3].
- Nonforfeiture options in force: cash, reduced paid-up, extended term (MassMutual explicit [S3]); Guardian: lapse into "non-forfeiture provision elected at issue," APL available [S1]; Penn Mutual overloan rider forces reduced paid-up on 99% loan utilization [S11].

### 3. Dividends (participating mechanics)
- Legal/professional frame: contribution principle, divisible surplus, annual Board declaration [R6]; illustrated dividends limited by DCS/currently-payable scale and self-support/lapse-support tests [R2]; ASOP 2 excludes dividends (covers non-par NGEs) [R7].
- Published dividend formula (Northwestern Mutual): dividend = (guaranteed accumulated value + gross premium − experience-based mortality&expense charge, accumulated at the dividend interest rate) − ending guaranteed accumulated value — i.e. classic three-factor contribution formula [S4].
- 2026 dividend interest rates: NM 5.75% [S4]; aggregate table MassMutual 6.60%, NYL 6.40%, Guardian 6.25%, Penn Mutual 6.00% [S14, secondary].
- 2026 payouts: NM $9.2B total / $7.9B WL [S5]; MassMutual $2.9B, NYL $2.78B, Guardian $1.7B, PM $0.3B [S14, secondary].
- Dividend timing: Guardian pays no first-year dividend [S1]; MassMutual pays first-year dividends [S3] — a real cross-insurer design difference.
- Dividend rate structure: varies by gender, class, band, issue age, duration, tax-qualified status [S3]; banding by face ($1M+) on Guardian level-pay [S1].
- Dividend options (union across carriers): cash; reduce premium (excess to cash or PUAs); accumulate at interest (rate declared annually); paid-up additions (default at Guardian [S1][S2]; "most commonly elected"/vast majority at NM [S4][S5]); one-year term options (up to CV, up to 2× face, or to a Target Face Amount with PUA balance — Guardian F/G/L/P/Q/R [S2]; MassMutual OYT=guaranteed CV via YTP rider [S3]); premium offset [S2][S3 as APO]; repay loan principal / loan interest [S2][S3]; LTC additions (Guardian I) [S2]; LISR/Flex feed (MassMutual) [S3].
- Term-blend riders funded by dividends+rider premiums with target face and crossover: Guardian option Q/R (target ≤ 9× base; increasing-target version) [S2]; MassMutual LISR (TFA ≤ 300% base; crossover ≤ age 100; FLX option required) [S3]; Penn Mutual Flexible Protection Rider (+APPUA/EPPUA) [S11].

### 4. Policy loans
- Two loan regimes market-wide: fixed rate WITH direct recognition vs variable/adjustable rate WITHOUT direct recognition:
  - Guardian: fixed 6% (5.66038% in advance), direct recognition; steps down to 4% late in life (product-specific triggers); one-time irrevocable option at 10th anniversary to switch to VLR (max = greater of Moody's monthly corporate average or 4.5%, 50 bp corridor), no direct recognition under VLR [S1].
  - MassMutual: choice fixed at issue — adjustable loan rate (default; max = Moody's seasoned corporate composite or guaranteed rate + 1%) with no direct recognition, or fixed 6% with direct recognition [S3].
  - NYL Secure Wealth Plus: variable loan rate [S9].
- Loan mechanics: max loan ≈ CV less accrued items to next anniversary; unpaid interest capitalizes on anniversary; loans reduce death proceeds and CSV [S1][S3][S9].
- Loans interact with dividends only under direct recognition [S1][S3]; loan utilization > 99% CV triggers overloan protection (Penn Mutual rider: age ≥ 75, duration ≥ 15) [S11].

### 5. Death benefit and policy termination
- DB = face + rider amounts + PUA face + dividend accumulations + terminal dividend items − loans/interest − due premium − accelerated benefits (Guardian's full formula) [S1].
- Grace 31 days; reinstatement within 5 years with evidence and 6% interest on arrears (Guardian, MassMutual) [S1][S3].
- Suicide exclusion 2 years (FE WL: return of premium less loans; 1 year in ND) [S7]; contestability restarts on reinstatement [S7].
- Graded death benefit (FE WL Graded): natural-cause death in first 2 policy years pays premiums paid + 10%; accidental death pays full face from day 1 [S6][S7].
- Maturity: FE WL endows at 100 (120 in FL) for face less loans [S8]; par WL policies mature at 121 with CV=face at 100 [S1][S3].

### 6. Riders (typical set for a reference model)
- Paid-up additions rider (single/flexible premium PUA purchases; expense charge 7.5–10% of PUA premium at MassMutual, guaranteed caps [S3]; payment limits set at issue [S11]).
- Term riders on the insured (annually renewable to 95, 10-yr level current scale, ≤ 20× base face [S3]; 10-yr RT at Guardian [S1]).
- Waiver of premium on disability (6-month wait; own-occ definition 2–6 yrs; terminates ~65) [S1][S3][S11].
- Guaranteed insurability / purchase options (option ages ~22–46, amount caps e.g. min $25k / max lesser of 2× base or $125k at MassMutual) [S3][S11].
- Accelerated death benefits: terminal illness (12-month prognosis) near-universal [S6][S11][S12]; chronic illness (2 of 6 ADLs) [S11]; LTC riders with monthly-benefit pools, 90-day elimination, lien mechanics (MassMutual LTCAccess: accelerate ≤ 90% of face, residual ≥ $25k, MMB $3k–$30k, periods 2–10 yrs, 4% MMB increase option) [S3].
- Accidental death benefit (FE: additional DB = face [S6]; Penn Mutual caps $50k/$250k by age [S11]).
- Children's term, exchange-of-insured, overloan protection, surrender-value enhancement (business) [S11][S3].

### 7. Tax qualification constraints on design
- §7702 life-insurance definition: CVAT or GPT+corridor; post-2020 issues use the lower "applicable" (insurance) interest rates — 2% transitional in 2021 — which raised permissible premium levels for WL funding [R4].
- §7702A MEC 7-pay test; limited-pay WL premiums sit close to 7-pay limits, so 10-pay designs and PUA riders are the main MEC risk; material changes (face decreases, added benefits) retest [R5][S3][S1].
- Carriers embed 7-pay administration: Guardian computes 7-pay on 2017 CSO composite and tracks deemed cash value [S1]; NYL flags the 15-year withdrawal-with-DB-reduction rule [S9].

### 8. Statutory valuation (for the liability model's reserve module)
- Issues on/after 2020-01-01: VM-20 applies to ordinary life — NPR (seriatim, 2017 CSO, VM-prescribed interest) plus DR/SR unless exclusion tests passed; traditional WL typically passes the DET when valuation net premiums ≤ guaranteed gross premiums [R3].
- Small companies: Life PBR Exemption (< $300M/$600M premiums) → VM-A/VM-C (pre-PBR CRVM framework) [R3].
- Pre-2017/2020 in-force: CRVM under the Standard Valuation Law with 2001 CSO/1980 CSO cohorts [R1][R3][R11-unfetched].
- Experience assumptions for dividends/PBR: ILEC 2012–2019 industry mortality vs 2015 VBT [R9]; 2017 CSO table set downloadable from SOA [R8].

### 9. Underwriting structures observed
- Fully underwritten par WL: 4–6 classes (2 preferred NT tiers, standard NT, preferred/standard tobacco), juvenile unismoke, table ratings to class 16 / table P + flat extras [S1][S3].
- Accelerated/expedited UW paths on WL: NYL 24–48 hr no-lab issue below premium thresholds [S9]; Penn Mutual ACE [S12].
- Simplified issue FE WL: knock-out health questions, Rx/MIB checks, tele-interview; standard-only classes (tobacco split on level plan only); build chart [S7].

---

## Variations across insurers

1. Premium period menus differ but converge on: level-pay-to-~100/121 + {10, 15/12, 20}-pay + paid-up-at-65; every carrier surveyed offers a 10-pay [S1][S3][S10][S13].
2. Guaranteed interest in the CV schedule: single rate for all products at Guardian (4%) vs product-specific rates 2–3.75% at MassMutual — a modeling knob that must be per-product, not per-company [S1][S3].
3. First-year dividend: paid by MassMutual [S3], not paid by Guardian [S1].
4. Loan regimes: Guardian = fixed-with-DR default, VLR electable at year 10; MassMutual = ALR default (no DR), fixed-with-DR electable at issue; NYL SWP = variable [S1][S3][S9]. Direct recognition is always paired with the fixed rate.
5. Dividend banding: by face amount at Guardian (level-pay only, $1M+) and MassMutual (all products, multiple bands) [S1][S3].
6. Term-blend mechanisms are universal but named differently (Guardian Q/R options; MassMutual LISR; Penn Mutual Flexible Protection Rider) [S2][S3][S11].
7. FE WL (United of Omaha) differs structurally: tiny faces ($2k–$50k), age-45+ issue, simplified issue, graded DB tier, explicit $36 policy fee, endowment at 100 — and its materials never mention dividends (see gap below) [S6][S7][S8].
8. Accumulation-oriented WL is a distinct sub-species: NYL Secure Wealth Plus (10-pay, $10k min premium, early-CV optimized, expedited UW) [S9][S10] and Penn Mutual Accumulation WL (5-pay to pay-to-100 menu) [S13].
9. Representative design for a reference model: a participating, level-premium, endow-at-100/mature-at-121 WL on 2017 CSO / 4% nonforfeiture basis with PUA-default dividends (three-factor contribution formula à la [S4]), optional 10/20-pay and pay-to-65 variants, PUA + term riders, fixed 6% loan with direct recognition — this matches the Guardian/MassMutual mainstream and NAIC minimum standards [S1][S2][S3][S4][R1][R3]. A secondary non-par simplified-issue FE variant (level + graded) parameterized from [S6][S7][S8] covers the non-par case with real premium rates.

---

## Gaps and caveats

- Living Promise participation status: none of the retrieved documents states whether the policy pays dividends; final-expense WL from United of Omaha is generally non-participating [unverified]. Model it as non-par, but confirm from a specimen policy.
- Guardian guide is the 2019 series (2017 CSO repricing); current-year rate books/dividend scales are producer-portal-only. The 2019 documents remain the best public description of the mechanics.
- MassMutual guide (S3) is the 2022 producer reference (LI10804e 522); the Legacy-series forms are 2018. Current "MassMutual Whole Life" digital-platform variants may differ in detail.
- Full specimen policy forms (contract wording with the actual CV tables) were not publicly obtainable for the par carriers; guaranteed-CV *schedules* per unit were only obtained as basis descriptions (interest + mortality + endow-at-100), not as printed tables. A carrier illustration PDF (massmutual.com) was blocked (Akamai 403 / timeout).
- New York Life product pages block server-side fetchers (403); content was retrieved by direct HTTP download with a browser user-agent. NYL Custom Whole Life parameters (face $50k–$1M, issue 0–70) appeared only in search-result snippets — [unverified].
- SEC EDGAR was not used: traditional par/non-par WL is not SEC-registered (no statutory prospectuses exist for these products; variable products are out of scope) [unverified as a general statement].
- Northwestern Mutual product-level specs (issue ages, bands, loan rate) are not published on public pages retrieved; only dividend mechanics and payout were captured [S4][S5].
- 2026 DIR figures for MassMutual/NYL/Guardian/Penn Mutual come from a fetched secondary aggregator [S14]; carrier press releases were not directly fetchable (Yahoo mirror 404, massmutual.com blocked). NM's 5.75% is confirmed on the carrier's own page [S4].
- ASOP 24 (R10) and NAIC Model 820 (R11) are listed but were not fetched; do not rely on characterizations of their contents beyond titles.
- Older CSO regimes (1941/1958/1980) matter for in-force blocks; this note captures the current-issue (2017 CSO) basis in detail and Model 808's historical sections only in outline [R1].
- Rate tables extracted (S7) are the California edition; state variations (WA face minimums, FL forms/maturity 120, ND suicide 1 yr) are real and noted where seen [S6][S7][S8].
