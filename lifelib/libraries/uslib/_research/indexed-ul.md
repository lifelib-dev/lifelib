# Indexed Universal Life Insurance (IUL) — research notes (U.S.)

Research date / access date for all citations: 2026-08-03.
Compiled for reference implementations of liability cash-flow projection models (lifelib/modelx style).
Every fact below is tagged [S#]/[R#] (retrieved document) or [unverified] (general knowledge, not verified against a retrieved source in this session).

---

## Primary sources

Fetch method note: PDFs were downloaded via WebFetch and text-extracted locally with pypdf; facts were read from the extracted full text unless noted.

### S1. Pacific Life — "Pacific Horizon IUL 2 — Client Guide" (LFC3384-2401 4/24, 24-VER-25A)
- Publisher: Pacific Life Insurance Company (Omaha, NE)
- Doc type: consumer brochure / client guide
- URL: https://www.pacificlife.com/content/dam/paclife/lid/public/brochures/indexed-universal-life-/LFC3384_HorizonIUL2.pdf
- Retrieved: YES (PDF fetched, full text extracted, 4 pp.)
- Key facts: product identity (flexible premium indexed UL, form series P21IUL, S23HZN2-B/-E/-L varying by coverage design option and state); three coverage design options elected irrevocably at issue (Enhanced Early Surrender Value / Balanced / Long-Term Performance); charge taxonomy (Administrative Charge, Coverage Charge, Cost of Insurance Charge, rider and indexed account charges, premium load per premium, surrender charges within 10 years of each layer of Basic Coverage issue date); premium mechanics (net premium first to fixed account, monthly transfer date on the 15th, transfers create segments with 1-, 2- or 5-year terms); Age 90 No-Lapse Guarantee Rider (form R22NLG) automatically issued with DB options A or B for issue ages 79 and under; Flexible Duration No-Lapse Guarantee Rider (R17FNL) extends up to lifetime; Enhanced Performance Factor Rider (R18EPF) with three design options boosting interest crediting for a monthly charge; chronic illness (R22CHR), LTC (R15LTC) and living benefits (R18ADB) riders; licensed in all states except New York.

### S2. Pacific Life — "Pacific Horizon IUL 2 — Your Account Choices" (IUC3996-1124 11/24, 24-VER-80A)
- Publisher: Pacific Life Insurance Company
- Doc type: consumer brochure (indexed-account detail guide)
- URL: https://www.pacificlife.com/content/dam/paclife/lid/public/brochures/indexed-universal-life-/IUC3996_Horizon_IUL_Guide.pdf
- Retrieved: YES (PDF fetched, full text extracted, 6 pp.)
- Key facts: full menu of fixed and indexed accounts with current and guaranteed caps/participation rates/floors, segment mechanics, indexed-account asset charge, indexed loan account. Details in "Extracted specifications" below.

### S3. Transamerica — "Navigating the Features of the Transamerica Financial Foundation IUL" (agent guide, 23448_FFIULAG1017)
- Publisher: Transamerica Life Insurance Company
- Doc type: producer/agent guide (36 pp., incl. rate tables)
- URL: https://s3-us-west-2.amazonaws.com/prod-orbital-resources/harpercole/Carriers/Transamerica/Products/IUL+Plans/23448_FFIULAG1017_Agent_Guide_Brochure_FINAL_Digital.pdf (distributor mirror of the Transamerica document; official Transamerica form number 23448_FFIULAG1017)
- Retrieved: YES (PDF fetched, full text extracted, 36 pp.)
- Key facts: complete product specification — issue ages, bands, underwriting classes, DB options, no-lapse guarantee, loan/withdrawal provisions, account mechanics with the exact excess-index-interest formula, full charge schedule, riders, minimum-premium rate tables. Details below.

### S4. Transamerica — "A Guide to the Transamerica Financial Foundation IUL Life Insurance Policy" (consumer brochure 258820R5, 09/22)
- Publisher: Transamerica Life Insurance Company
- Doc type: consumer brochure
- URL: https://ani.transamerica.com/ani/Uploads/Pages/53905/258820R5_0922_FFIUL%20Consumer%20Brochure_D.pdf
- Retrieved: YES (PDF fetched, full text extracted, 20 pp.)
- Key facts: September 2022 current caps (Global Index Account 13.00%, S&P 500 Index Account 12.00% — lower than the caps in the earlier agent guide S3), 0.75% floors, Basic Interest Account 2.00% minimum, loan rate table (current and guaranteed, cost-basis vs gain split), segment mechanics (up to 12 monthly segments of 12 months each), no-lapse periods.

### S5. Nationwide — "Nationwide IUL Accumulator II 2020 — Product overview" (FLM-1490AO.14, 03/26)
- Publisher: Nationwide Life and Annuity Insurance Company (Columbus, OH)
- Doc type: producer-facing product overview / fee & rate disclosure
- URL: https://financial.nationwide.com/media/pdf/FLM-1490AO.pdf (the same path on nationwidefinancial.com returned HTTP 403; financial.nationwide.com succeeded)
- Retrieved: YES (PDF fetched, full text extracted, 4 pp.)
- Key facts: complete current rate card as of 3/15/2026 for 11 indexed interest strategies (caps, participation rates, spreads, strategy charges), fixed strategy rates, both loan types with current/guaranteed rates, charge structure, death benefit guarantee schedule, IUL Rewards Program (0.20% persistency credit). Details below.

### S6. Securian Financial — "Eclipse Accumulator II IUL — A top choice for accumulation IUL" (F108140-16, 3-2026)
- Publisher: Minnesota Life Insurance Company / Securian Financial
- Doc type: producer-facing competitive comparison flyer
- URL: https://www.securian.com/content/dam/doc/il/eclipse-accumulator-ii-iul-fixed-loans-5-percent_108140-16.pdf
- Retrieved: YES (PDF fetched, full text extracted, 6 pp.)
- Key facts: current illustrated rate for its S&P 500 account 6.59%; benchmarking tables (male/female 45, Preferred Best and Standard; $25,000 annual premium to 65; fixed loans; max distributions, sum of charges year 20, CSV at 65, target premiums) across 16 named competitor IUL products with each product's current illustrated rate (range 5.61%–7.38%); Securian charge taxonomy (Cost of Insurance, Cash Extra, Additional Agreements charges = "mortality charges"; Premium Charge, Monthly Policy Charge, Policy Issue Charge, Transaction Charge, Index Segment Charge, Surrender Charge = "expense charges"); fixed-rate loan triggers a 12-month lockout on fixed-to-indexed transfers.

### S7. Securian Financial — Eclipse Accumulator IUL product page (financial professionals)
- Publisher: Securian Financial (Minnesota Life)
- Doc type: producer product-specification web page (HTML)
- URL: https://www.securian.com/financial-professionals/products/individual-life-insurance/indexed-universal-life/eclipse-accumulator.html
- Retrieved: YES (HTML fetched; specifications extracted via WebFetch summarization — see caveat in "Gaps")
- Key facts (as extracted): issue ages 0–80 age nearest birthday; minimum face amount $100,000; DB options level or increasing; indexed accounts — Indexed Account A (S&P 500, 1-yr, cap 10.50%, par 100%, floor 0%), Indexed Account G (S&P 500 Low Volatility, 1-yr, no cap, par 65%), Indexed Account O (S&P PRISM, 1-yr, no cap, par 215%), Hindsight Indexed Account (S&P 500 / Nasdaq-100 / Russell 2000, 1-yr, cap 9.50%, par 100%), Performance Trigger (S&P 500, 1-yr); contract minimum interest guarantee expressed as "2% cumulative average upon death or termination"; loans — fixed: charge 4%, credit 3% yrs 1–10 / 4% yrs 11+; variable: charge varies, 3% minimum; indexed loans: charge 5%, credit linked to indexed loan account; short-term loans interest-free if repaid within 90 days; 10-year surrender charge period (also applies after face increases); 14 optional agreements.

### S8. Allianz Life — "The benefits of diversifying your fixed index universal life insurance policy — Allianz Life Pro+ Elite" (CSI-486)
- Publisher: Allianz Life Insurance Company of North America (Minneapolis, MN)
- Doc type: consumer flyer (policy form R-9/2018; companion pieces M-5913, M-6070, M-5640)
- URL: https://www.allianzlife.com/life-insurance/-/media/files/Allianz/PDFs/life/csi-486.pdf
- Retrieved: YES (PDF fetched, full text extracted, 2 pp.)
- Key facts: Allianz brands the product "fixed index universal life (FIUL)"; participation rate declared at issue and on each policy anniversary, guaranteed never less than 5%; cap subject to annual change, minimum guaranteed cap 0.25%; current bonused-allocation rates used in the example: Bloomberg US Dynamic Balance II ER Index 160% participation, blended index 16.00% cap, PIMCO Tactical Balanced ER Index 160% participation, all annual point-to-point with 0% floor; blended index = DJIA 35% / Bloomberg Barclays US Aggregate 35% / EURO STOXX 50 20% / Russell 2000 10%; hypothetical 2005–2017 issue-date study: frequency of 0% credits 12.55%–23.81% for single allocations vs 4.37% for an equal mix; "Bonus products may include higher surrender charges, longer surrender periods, lower caps, higher spreads, or other restrictions."

### Failed / not-retrieved product fetches
- Securian "Eclipse Accumulator IUL" spec sheet 93901-21 (https://www.securian.com/content/dam/doc/il/eclipse-accumulator-iul-fixed-loans-5-percent_93901-21.pdf): HTTP 404 — superseded by the II version (S6/S7).
- Nationwide FLM-1490AO at https://nationwidefinancial.com/media/pdf/FLM-1490AO.pdf: HTTP 403 (retrieved from financial.nationwide.com instead, S5).

---

## Regulatory and actuarial references

### R1. NAIC Actuarial Guideline XLIX-A (AG 49-A), incl. the 2023 revisions (commonly called "AG 49-B")
- Publisher: National Association of Insurance Commissioners
- Title: "Actuarial Guideline XLIX-A — The Application of the Life Illustrations Model Regulation to Policies with Index-Based Interest Sold (On or After December 14, 2020)"; adopted by Life Actuarial (A) Task Force 12/11/2022 and Life Insurance and Annuities (A) Committee 2/24/2023; includes project history of the 2023 revisions
- URL: https://content.naic.org/sites/default/files/committees-pending-action-actuarial-guideline-xlix-a-230224.pdf
- Retrieved: YES (PDF fetched, full text extracted, 6 pp.)
- Content: full guideline text — scope, definitions (Benchmark Index Account, Hedge Budget, Supplemental Hedge Budget, Annual Net Investment Earnings Rate, Indexed Credits), illustrated-scale limits, disciplined-current-scale limits, policy loan limit, additional disclosure standards. Details below.

### R2. NAIC Life Insurance Illustrations Model Regulation (Model #582)
- Publisher: NAIC (Model Laws, Regulations, Guidelines — April 2001 printing)
- URL: https://content.naic.org/sites/default/files/model-law-582.pdf
- Retrieved: YES (PDF fetched, full text extracted, 14 pp.)
- Content: scope (exempts policies "with no illustrated death benefits on any individual exceeding $10,000"), definitions of disciplined current scale, currently payable scale, illustrated scale, self-supporting and lapse-supported illustrations, illustration actuary certification duties. Details below.

### R3. NAIC Valuation Manual — Jan. 1, 2026 Edition (incl. VM-01, VM-20)
- Publisher: NAIC
- URL: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (PDF fetched, full text extracted, 457 pp.)
- Content: VM-01 definitions ("index credit", "index credit hedge margin", "index crediting strategies", "indexed universal life (IUL) insurance policy"); VM-20 principle-based reserve requirements for life products (IUL is reserved as a UL product under VM-20); VM-20 cash-flow modeling of assets used to hedge indexed credited amounts; CDHS ("clearly defined hedging strategy") requirements; VM-21/VM-22 index credit hedge margin rules (annuity-side analogues). Details below.

### R4. IRC §7702 — Life insurance contract defined
- Publisher: Legal Information Institute, Cornell Law School (U.S. Code)
- URL: https://www.law.cornell.edu/uscode/text/26/7702
- Retrieved: YES (HTML fetched and summarized)
- Content: cash value accumulation test; guideline premium requirements + cash value corridor; floating "insurance interest rate" replacing fixed 4%/6% rates for contracts issued after 12/31/2020 (Consolidated Appropriations Act, 2021); corridor percentages 250% (ages 0–40) grading to 100% (ages 90–95); income-on-the-contract taxation on failure.

### R5. IRC §7702A — Modified endowment contract defined
- Publisher: Legal Information Institute, Cornell Law School
- URL: https://www.law.cornell.edu/uscode/text/26/7702A
- Retrieved: YES (HTML fetched and summarized)
- Content: 7-pay test ("A contract fails to meet the 7-pay test if the accumulated amount paid under the contract at any time during the 1st 7 contract years exceeds the sum of the net level premiums which would have been paid on or before such time if the contract provided for paid-up future benefits after the payment of 7 level annual premiums"); MEC distributions taxed under §72; material-change re-start rules; benefit-reduction look-back within first 7 years.

### R6. SOA Product Matters! (June 2023) — B. Hoffer, "Actuarial Guideline XLIX (AG49): Past, Present and Future"
- Publisher: Society of Actuaries, Product Development Section
- URL: https://www.soa.org/sections/product-dev/product-dev-newsletter/2023/june/pm-2023-06-hoffer/
- Retrieved: YES (HTML fetched and summarized)
- Content: history of AG 49 (2015) / AG 49-A (2020) / 2023 "quick-fix" (effective for policies issued after May 1, 2023); worked example — a product with a 200% multiplier funded by a 5% account-value charge could show ~6.5% illustrated-rate benefit (1.5% net of charge) pre-AG 49-A but no leverage benefit after; the 2023 amendment caps illustrated leverage (option profit) at the Benchmark Index Account's leverage, targeting uncapped volatility-controlled index accounts paired with fixed bonuses; notes unresolved debate on the 145% earned-rate cap and the BIA lookback methodology.

### R7. SOA Product Matters! (Nov 2022) — P. OuYang, "The Impact of AG 49 and AG 49-A on Indexed Universal Life Insurance Illustrations: Results from a Survey of 28 Insurers"
- Publisher: Society of Actuaries
- URL: https://www.soa.org/sections/product-dev/product-dev-newsletter/2022/november/pm-2022-11-ouyang/
- Retrieved: NO (WebFetch returned HTTP 404 in this session although the page is indexed by search engines). Kept as a known reference; per search-result snippets it is a Milliman survey of 28 insurers on AG 49/AG 49-A impacts — do not treat its contents as verified.

### R8. American Academy of Actuaries — Life Illustrations Practice Note (September 2021 update)
- Publisher: American Academy of Actuaries, Life Illustrations Work Group
- URL: https://actuary.org/wp-content/uploads/2021/09/Life_Illustrations_Practice_Note_Update.pdf
- Retrieved: YES (PDF fetched and summarized)
- Content: Q&A-format practice note on complying with ASOP No. 24 and NAIC Model 582 — disciplined current scale determination, self-support and lapse-support testing, and treatment of index-based interest crediting under AG 49/49-A.

### R9. ASB — ASOP No. 24, "Compliance with the NAIC Life Insurance Illustrations Model Regulation"
- Publisher: Actuarial Standards Board
- URL: http://www.actuarialstandardsboard.org/asops/compliance-naic-life-insurance-illustrations-model-regulation/
- Retrieved: YES (HTML fetched)
- Content: page for the December 2016 revision (doc. no. 184, effective April 30, 2017), shown on the ASB site with status "Superseded" — i.e., a later revision exists; consult the ASB site for the current version.

### R10. NAIC Universal Life Insurance Model Regulation (Model #585)
- Publisher: NAIC (Model Laws — January 2001 printing)
- URL: https://content.naic.org/sites/default/files/model-law-585.pdf
- Retrieved: YES (PDF fetched, full text extracted, 14 pp.)
- Content: the base UL regulatory chassis (valuation, nonforfeiture, mandatory policy provisions, disclosure) plus Section 10 "Interest-Indexed Universal Life Insurance Policies": defines "interest-indexed universal life insurance policy," requires filings describing how the insurer will address the risk that the indexed interest rate may fall, the amount and type of assets held for interest-indexed policies, and an annual Statement of Actuarial Opinion for interest-indexed UL policies.

---

## Extracted specifications

All facts tagged. "Current" rates are non-guaranteed and as of each document's print date.

### 1. Product identity and chassis
- IUL is a flexible-premium universal life chassis in which cash value allocated to indexed accounts earns interest "based in part on the performance of market-based indexes"; the policy is not directly invested in the market [S1].
- The NAIC Valuation Manual defines an IUL policy as "any universal life (UL) insurance policy where the interest credits are linked to an external reference" [R3].
- Some carriers brand the same design "fixed index universal life (FIUL)" (Allianz) [S8].
- Coverage design options selected irrevocably at issue can trade early surrender value against long-term accumulation (Pacific Life: Enhanced Early Surrender Value / Balanced / Long-Term Performance) [S1].

### 2. Issue ages, face amounts, underwriting
- Transamerica FFIUL: issue ages 0–85 (age last birthday); face bands $25,000–$99,999 / $100,000–$249,999 / $250,000–$499,999 / $500,000+; policies issued only on the 1st–27th of a month; classes Preferred Elite/Preferred Plus/Preferred/Non-Tobacco/Preferred Tobacco/Tobacco/Juvenile (juvenile 0–17); preferred classes require ≥$100,000 [S3].
- Nationwide IUL Accumulator II 2020: minimum specified amount $100,000; target market ages 30–55 [S5].
- Securian Eclipse Accumulator II: issue ages 0–80 (age nearest birthday); minimum face $100,000 [S7].

### 3. Death benefit options
- Level (face amount); Increasing (face + policy value); Transamerica adds a Graded option (increasing to age 70, grading to level at 95); amounts increased where needed to meet IRS (§7702 corridor) requirements; option changes allowed after policy year 3, once per year, not after age 95 [S3].
- Nationwide offers Level, Increasing, and Return of Premium (ROP not available in NY) [S5].
- Securian: level or increasing [S7].
- Death benefit corridor: §7702(d) cash value corridor requires death benefit ≥ applicable percentage of cash surrender value, 250% at attained ages 0–40 grading to 100% at ages 90–95 [R4].

### 4. Premiums and no-lapse guarantees
- Premiums are flexible — may be increased, decreased, skipped, or stopped if the no-lapse guarantee is in effect or cash surrender value covers deductions [S3].
- Transamerica Minimum Monthly No Lapse Premium (MNLP): policy will not lapse during the no-lapse period if cumulative premiums (less loans/withdrawals) ≥ cumulative MNLP; no-lapse period by issue age — 0–45: 20 years; 46–60: to age 65; 61–85: 5 years; grace period 61 days [S3][S4].
- Nationwide initial base death benefit guarantee — issue ages 0–55: 20 years; 56–69: (75 − issue age) years; 70+: 5 years [S5].
- Pacific Life: Age 90 No-Lapse Guarantee Rider automatically issued (DB options A/B, issue ages ≤79) guaranteeing death benefit to attained age 90 if Age 90 NLG premiums are paid; optional Flexible Duration No-Lapse Guarantee Rider up to lifetime [S1].
- Reinstatement (Transamerica): within 3 years of lapse with evidence of insurability; lapsed time does not count toward the surrender-charge period [S3].

### 5. Account structure and segment mechanics
- Accounts: a declared-rate fixed account plus one or more indexed accounts. Pacific Life: each premium (net of premium load) goes first to the Fixed Account; on the 15th of each month the owner may transfer to indexed accounts; each transfer creates a "Segment"; interest credited at the end of the 1-, 2- or 5-year segment term; matured segment value can be reallocated or rolled into a new segment [S1][S2].
- Transamerica: net premiums/transfers allocated monthly to segments; up to 12 segments per account, each lasting 12 months, beginning on monthly policy dates; at segment end a new segment begins with the prior value; transfers out of an index account only at segment maturity; transfers into index accounts only on the first day of a policy month [S3][S4].
- During a segment, policy values (death benefit, CSV) reflect only the guaranteed minimum interest; excess index interest is credited only at segment maturity; amounts withdrawn/borrowed mid-segment forfeit excess index interest [S3].
- Automatic Transfer Rule (Transamerica): standing percentage instructions applied at segment renewal; dollar cost averaging alternative requires ≥$5,000 in the Basic Interest Account, minimum transfer $100 [S3].
- Nationwide requires a Minimum Required Fixed Interest Strategy Allocation (MRFISA): an estimate of the coming year's policy charges is held in the fixed strategy; only the excess can go to indexed strategies [S5].

### 6. Index crediting — methods and current/guaranteed parameters

Crediting formula (annual point-to-point, the dominant design): index change % = (index value at segment end − index value at segment start) / value at start, excluding dividends; credited rate = min(cap, max(floor, participation × index change)) [S3][S2]. Transamerica's exact excess-interest dollar formula: (adjusted index change %) × (segment's adjusted beginning value) − (interest already credited at the guaranteed minimum during the segment), where the adjusted beginning value subtracts withdrawals, loan transfers, and one-half of monthly deductions and index-account monthly charges taken during the segment [S3].

Pacific Life Pacific Horizon IUL 2 (current rates, 11/24 print) [S2]:
- Fixed Account: 4.5% current declared; 1% guaranteed minimum; first-year rate locked.
- 1-Year Indexed Account: S&P 500 excl. dividends, 1-yr PTP; current cap 10%, guaranteed minimum cap 2%; 100% guaranteed participation; 0% floor.
- 1-Year No Cap Dynamic Par: S&P 500 excl. dividends; no cap; declared participation (guaranteed minimum 5%; par may be redeclared as frequently as monthly; illustrations assume 50%); 0% floor.
- 1-Year Invesco QQQ Indexed Account: QQQ ETF performance (dividend-tracking ETF); current cap 10.5% (guaranteed minimum 1%); 100% par; 0% floor.
- 1-Year High Cap Indexed Account: S&P 500; current cap 12.0% (guaranteed 4%); 100% par; 0% floor; monthly asset charge 0.067% (0.80% annualized) of the account's accumulated value.
- 2-Year Indexed Account: S&P 500; current cap 24% over 2 years (guaranteed 6% over 2 years); 100% par; 0% floor.
- High Par 5-Year Indexed Account: S&P 500, point-to-last-year-average measurement; no current cap (guaranteed cap 10% over 5 years); current par 110% (guaranteed minimum 105%); 0% floor.
- 1-Year High Par Volatility Control: BlackRock iBLD Endura VC 5.5 ER Index; no cap; current par 200% (guaranteed minimum 25%); 0% floor.
- Loaned 1-Year Volatility Control (available only with the Fixed Charge Indexed Loan Rider R23FALR): current par 160% (guaranteed minimum 20%); 0% floor.
- All indexed accounts have a 0% guaranteed floor [S2].
- Carrier-published hypothetical average annual crediting rates (1988–2023 lookback at current parameters): 1-Year 6.40%, No Cap Dynamic Par 5.70%, High Cap 6.51%, 2-Year 6.89%, High Par 5-Year 7.16%, vs S&P 500 price index 6.18% [S2].

Transamerica FFIUL [S3][S4]:
- Basic Interest Account: declared rate, guaranteed minimum effective annual 2%.
- S&P 500 Index Account: 1-yr PTP on S&P 500 excl. dividends; cap 13.75% at the agent-guide print date [S3], 12.00% in the 09/2022 consumer brochure [S4]; guaranteed minimum interest ("floor") 0.75% effective annual credited during the segment [S3].
- Global Index Account: 1-yr PTP on a best-weighted blend — 50% × better of S&P 500/EURO STOXX 50, 30% × worse of those two, 20% × Hang Seng, dividends excluded; cap 15% at the agent-guide print date [S3], 13.00% in 09/2022 [S4]; 0.75% floor.
- Caps set at company discretion at each segment start; guaranteed never to be less than the current Basic Interest Account rate [S3][S4].
- Note the design difference: Transamerica's "floor" is a 0.75% guaranteed interest rate credited throughout the segment (excess index interest is measured net of it), rather than a 0% floor in the crediting formula [S3].

Nationwide IUL Accumulator II 2020 (current rates effective 3/15/2026; all strategies 0% floor) [S5]:
- Core: 1-Yr Multi-Index Monthly Average cap 14.00%, par 100%, no charge; 1-Yr S&P 500 PTP cap 10.25%, par 100%, no charge; 1-Yr Uncapped S&P 500 PTP — spread 5.75% instead of a cap.
- High-cap: 1-Yr High-Cap Multi-Index Monthly Average cap 25.00%, charge 0.65%; 1-Yr High-Cap S&P 500 PTP cap 13.25%, charge 1.0% (indexed strategy charge deducted from the amount applied at segment creation).
- Volatility-control: 1-Yr J.P. Morgan Mercury Plus par 190% + 0.60% Plus credit; 1-Yr BNPP Global H-Factor Plus par 240% + 0.60% Plus credit; Mercury High Par 215%; H-Factor High Par 270%; Mercury High Par Select 255% with 1.0% charge; H-Factor High Par Select 320% with 1.0% charge. The Plus strategy credit (0.60% current) is added at segment maturity and is not guaranteed.
- Multi-Index Monthly Average: tracks S&P 500, Nasdaq-100 and DJIA over the year, then weights 50% best / 30% second / 20% third performer, monthly-average method.
- Fixed interest strategy: current 4.25%, guaranteed 1%.
- Nationwide IUL Rewards Program: additional interest at 0.20% annualized from year 16 (earlier for issue ages 51+) if cumulative net premium test is met; credited monthly on accumulated value minus indebtedness into the fixed strategy; guaranteed if requirements met [S5].

Securian Eclipse Accumulator II [S6][S7]:
- Five indexed account options, all 0% floor [S6]: Indexed Account A — S&P 500 1-yr PTP, cap 10.50%, par 100%; G — S&P 500 Low Volatility, uncapped, par 65%; O — S&P PRISM, uncapped, par 215%; Hindsight — S&P 500/Nasdaq-100/Russell 2000 with retrospective 60/40/0 best-performer weighting, cap 9.50%, par 100%; Performance Trigger — S&P 500 [S7 for parameters; S6 confirms five accounts and 0% floors].
- Interest guarantee: 2% cumulative average tested at death or termination [S7] (a retrospective cumulative guarantee rather than an annual floor).
- Current illustrated rate for the S&P 500 account: 6.59% (3/2026) [S6].

Allianz Life Pro+ Elite [S8]:
- Participation rate declared at issue and each anniversary, guaranteed ≥5%; caps redeclared annually, guaranteed minimum cap 0.25%.
- Current bonused-allocation examples: Bloomberg US Dynamic Balance II ER 160% par; blended index (DJIA 35/US Agg 35/EURO STOXX 50 20/Russell 2000 10) 16.00% cap; PIMCO Tactical Balanced ER 160% par; annual PTP; 0% floor.

Cross-market illustrated rates: Securian's 3/2026 competitor benchmarking lists current illustrated rates for S&P 500-style accounts across 16 carriers ranging from 5.61% (North American Smart Builder IUL 3) to 7.38% (Allianz Life Accumulator IUL) [S6].

### 7. Charge structure
Generic IUL monthly deduction = premium load + per-policy fee + per-unit (per $1,000) charge + cost of insurance on net amount at risk + rider charges + (for some accounts) indexed-account asset charges; surrender charge on surrender/lapse during the surrender period [S1][S3][S5] (composite; each component evidenced below).

- Premium expense charge: Transamerica current 4% of every premium all years (6% Puerto Rico), guaranteed 6% (8% PR) [S3]. Nationwide current 8.00% year 1 and 6.00% years 2+, guaranteed maximum 10.00% all years [S5]. Pacific Life deducts a premium load from each premium (amount not stated in retrieved docs) [S1].
- Per-policy fee: Transamerica $10/month current, $12 guaranteed max [S3]. Nationwide $10/month current, $20 guaranteed max [S5].
- Per-unit (per-$1,000) charge: Transamerica — shown in policy data pages; currently applies for the first 10 policy years (and 10 years after each face increase), decreasing over the 10 years; guaranteed level for all years; varies by issue age, sex, band, tobacco [S3]. Nationwide — assessed currently for 10 years, guaranteed all years [S5]. Pacific Life labels this the "Coverage Charge" [S1].
- Cost of insurance: monthly COI depends on face amount, risk class, age, gender, duration, and the difference between policy value and death benefit (i.e., net amount at risk); rates changeable up to guaranteed maximums; changes must be based on expectations of future cost factors (mortality, interest, persistency, expenses, reinsurance, taxes) [S3].
- Indexed-account asset charges (charge-funded enhanced accounts): Transamerica Index Account Monthly Charge 0.06%/month (0.72%/yr) of index account value, current and guaranteed, through age 120 [S3]. Pacific Life 1-Year High Cap account 0.067%/month (0.80%/yr) of account value [S2]. Nationwide indexed strategy charges 0.65%–1.0% deducted up front at segment creation for High-Cap/Select strategies [S5].
- Surrender charges: Transamerica per $1,000 of initial face and of each increase, for 15 years (and 15 years from each increase), varying by issue age, gender, risk class [S3]. Nationwide 10-year schedule [S5]. Pacific Life 10 years per layer of Basic Coverage [S1]. Securian 10 years, also after face increases [S7].
- Withdrawal fee: Transamerica $25 per withdrawal, minimum withdrawal $500, CSV cannot fall below $500 [S3].
- Securian names an additional "Policy Issue Charge" and "Transaction Charge" and "Index Segment Charge" among expense charges [S6].
- Minimum premium rate tables (per $1,000 of face, annual): Transamerica agent guide includes full issue-age tables; e.g., male non-tobacco issue age 45, band 1: 20.80 per $1,000 [S3].

### 8. Policy loans
Two families of loan design are standard [S5][S3][S2]:
- Declared-rate ("standard"/"fixed") loans — loaned value moved to a loan reserve credited at a fixed rate with a fixed charged rate; often becomes a "wash" (0% net) or preferred loan in later years:
  - Transamerica: loan reserve credited 2%; charged 2.75% current in arrears / 3% guaranteed max; preferred loans (years 11+, on gains) charged 2% current / 2.25% max — net 0.75% current years 1–10, 0% years 11+ on basis, 0.25% guaranteed on gains [S3][S4]. Minimum loan $500; loans taken from Basic Interest Account first, then pro-rata across index accounts/segments [S3].
  - Nationwide declared rate loan: credited 3.00% current (1.00% guaranteed minimum); charged 3.90% years 1–10 and 3.00% years 11+ (net cost 0.0% from year 11); guaranteed max charge 3.90% [S5].
  - Securian fixed loans: charged 4%; credited 3% years 1–10, 4% years 11+ [S7]; taking a fixed loan starts a 12-month lockout on fixed-to-indexed transfers [S6].
- Indexed/participating ("alternative"/"variable") loans — the loaned portion stays exposed to (or credited like) indexed strategies while a loan rate is charged:
  - Nationwide Alternative Loan: credited at the indexed strategies' crediting rate; charged 5% current all years, 8% guaranteed max; may be mixed with, or switched to, declared-rate loans [S5].
  - Securian: variable rate loans (charge varies, 3% minimum, credit tied to indexed accounts) and indexed loans (charged 5%) [S7]; short-term loans interest-free if fully repaid within 90 days [S7].
  - Pacific Life: Fixed Charge Indexed Loan Rider with a dedicated "Loaned 1-Year Volatility Control Indexed Account" (current par 160%, guaranteed min 20%) backing loaned values [S2].
- Illustration constraint: the illustrated loan credited rate may not exceed the illustrated loan charged rate by more than 50 bps [R1].

### 9. Withdrawals, maturity, and other provisions
- Withdrawals allowed after free-look, pro-rata across unloaned accounts, $500 minimum, $25 fee (Transamerica) [S3].
- Face increases (after year 1, to age 85, min $25,000, underwritten, new charges/surrender layers) and decreases (after year 3, min $25,000, ≤20% p.a. before the later of age 65/end of surrender period, subject to §7702) [S3].
- Charges run to age 120 (Transamerica index account monthly charge) [S3]; BIR terminates at insured age 100; Additional Insured Rider terminates at base insured age 121 — indicating an age-121 maturity framework for the base policy [S3]. Explicit maturity-age and post-maturity provisions were not stated in the retrieved brochures — [unverified] that these products mature at attained age 121 with continued coverage; confirm in specimen policy forms.
- Death benefit settlement alternative: Transamerica Income Protection Option endorsement — initial lump sum, monthly income over 5–25 years, final lump sum; elected at issue, modifiable before death; no additional cost [S3].

### 10. Riders (typical menu, with concrete parameters where retrieved)
- No-lapse guarantee riders (Pacific Life Age 90 NLG; Flexible Duration NLG to lifetime) [S1].
- Performance/multiplier rider: Pacific Life Enhanced Performance Factor Rider — three design options that boost interest crediting in exchange for a monthly rider charge [S1].
- Term riders: Transamerica Base Insured Rider (level term at term rates; min $100,000; max 10× base face without LTC; with LTC, lesser of base face or $1.5M, $3M combined cap; terminates age 100) and Additional Insured Rider ($25,000–$1M, up to five riders, convertible to age 70) [S3].
- Children's Benefit Rider: $1,000–$99,000; $6.00 per $1,000 annually; conversion to 5× up to $50,000 [S3].
- Guaranteed Insurability (issue ages 0–37; option dates after ages 22–40 birthdays + life events) [S3].
- Disability: Waiver of Monthly Deductions (18–55; waives deductions but not the index account monthly charge) or Waiver of Premium (applies a stated benefit amount as premium) [S3].
- Accidental Death Benefit (15–55; max lesser of 2.5× base face or $200,000 for smaller faces; death within 90 days of injury; terminates at 70) [S3].
- Overloan Protection Rider: automatically on Guideline Premium Test non-MEC policies; on exercise converts to paid-up and prevents loan-induced lapse/taxation; one-time charge on exercise: 5% of policy value at ages 75–90 grading to 1% at 94–120 [S3].
- Accelerated death benefits: Terminal illness (12-month prognosis; up to lesser of 100% of DB or $1.5M; min $5,000); Critical illness (listed conditions; up to lesser of 90% or $500,000, up to 3 claims); Chronic illness (2-of-6 ADLs or severe cognitive impairment, 90 consecutive days; ≤24% of eligible DB per 12 months, lifetime lesser of 90% or $1.5M); $350 administrative charge per acceleration ($100 for chronic recertification payments); acceleration reduces face, policy value, loan balance and MNLP by the election percentage [S3].
- LTC riders: Transamerica LTC Rider (accelerates base face; min specified amount $100,000, max $2M; combined cap $3M with BIR) [S3]; Nationwide Long-Term Care Rider II with 2%, 3%, 4% monthly payout options and couples discount [S5]; Pacific Life Premier LTC Rider / Premier Chronic Illness Rider [S1].
- Nationwide additional riders: Accidental Death, Change of Insured, Overloan Lapse Protection II, Premium Waiver, Surrender Value Enhancement, Waiver of Monthly Deductions [S5].

### 11. Illustration regulation (critical for any IUL projection/illustration model)
- Model 582 framework: applies to policies with illustrated death benefits over $10,000; defines the disciplined current scale (limit on illustrated non-guaranteed elements, "reasonably based on actual recent historical experience," certified annually by an illustration actuary; no projected improvements in experience may be assumed); illustrations must be self-supporting (accumulated policy value under DCS assumptions covers illustrated values) and not lapse-supported (test uses persistency under DCS for 5 years and 100% persistency thereafter); illustrated credited rate may not exceed the earned interest rate underlying the DCS [R2].
- AG 49-A (policies sold on/after 12/14/2020, as amended 2023) [R1]:
  - Benchmark Index Account (BIA): S&P 500 (SPX) 1-year point-to-point, annual cap, 0% floor, 100% participation, credited annually, hedge budget ≤ Annual Net Investment Earnings Rate (NIER), no multipliers/bonuses/enhancements; exactly one BIA per policy.
  - Maximum illustrated rate for the BIA = min( arithmetic mean of 25-year geometric average annual credited rates computed daily over lookback windows starting 66 years prior; 145% of NIER ).
  - Other index accounts: illustrated rate ≤ BIA rate + that account's Supplemental Hedge Budget, and (policies sold on/after 5/1/2023) ≤ min(account hedge budget, BIA hedge budget) × BIA rate / BIA hedge budget + Supplemental Hedge Budget — i.e., illustrated option-leverage capped at the BIA's [R1].
  - "Indexed Credits" is defined to capture any multiplier, factor, bonus, or charge reduction linked to an index [R1].
  - Disciplined current scale earned-rate limit: NIER + 45% of min(hedge budget − floor cost, min(NIER, BIA hedge budget)); insurers without hedging programs limited to NIER [R1].
  - Loans: illustrated loan credited rate ≤ illustrated loan charged rate + 50 bps [R1].
  - Disclosures: Alternate Scale ledger side-by-side with equal prominence (Alternate Scale indexed rate = min(illustrated rate − 100 bps, fixed account rate)); table of min/max 25-year geometric averages; 20-year historical index change table per illustrated account [R1].
- History/economics: AG 49 (2015) first bounded the illustrated index-credit rate; AG 49-A (2020) removed illustrated leverage from charge-funded multipliers (e.g., 200% multiplier with 5% AV charge could no longer illustrate a net benefit); the 2023 amendment (a.k.a. AG 49-B) shut the volatility-controlled-index + fixed-bonus route by capping illustrated option profit at the BIA level [R6][R1].
- Practice guidance: AAA Life Illustrations Practice Note (2021) and ASOP No. 24 govern the illustration actuary's DCS certification and testing practice [R8][R9].

### 12. Valuation / reserving and tax
- IUL is valued under the NAIC Valuation Manual as a life product under VM-20 (net premium reserve + deterministic/stochastic reserves as applicable); VM-01 defines "index credit" as "any interest credit, multiplier, factor, bonus, charge reduction, or other enhancement to policy or contract values that is directly linked to one or more indices," including floor-driven amounts, and it "may be positive or negative" [R3].
- VM-20 cash-flow projections must include cash flows for "assets used in the hedging of credited amounts for indexed accounts"; hedge modeling relies on the "clearly defined hedging strategy" (CDHS) framework, with margin increases where documentation of a future hedging strategy is incomplete [R3].
- The annuity-side sections of the same manual (VM-21 §4.A.4, mirrored in VM-22) impose an explicit "index credit hedge margin" — reduce index-credit hedge payoffs by a justified margin of no less than 1.5% multiplicatively of the hedged portion, or at least 20% absent sufficient credible company experience — a useful quantified analogue when modeling hedge inefficiency, though stated for annuities rather than VM-20 life business [R3].
- Interest-indexed UL filing/opinion requirements: NAIC Model 585 Section 10 requires filings describing how the insurer addresses the risk of the indexed rate falling, the assets held for interest-indexed policies, notice of significant changes, and an annual Statement of Actuarial Opinion on interest-indexed UL [R10].
- Federal tax definition: §7702 CVAT or GPT+corridor with floating minimum rates for post-2020 issues (previously 4% CVAT/GLP and 6% GSP) [R4]; MEC status per §7702A 7-pay test, with §72 taxation (and 10% penalty pre-59½) of MEC distributions [R5]; Transamerica automatically includes its Overloan Protection Rider only on GPT non-MEC policies [S3]; withdrawals within the first 15 policy years associated with benefit reductions can be taxable under §7702(f)(7)(B) [S1].
- Product tax framing in brochures: death benefit income-tax-free under §101(a)(1); loans/withdrawals tax-free up to basis if not a MEC and the policy stays in force [S1][S3].

### 13. Option budget / hedging mechanics (background for model calibration)
- The AG 49-A "Hedge Budget" is defined as "the total annualized amount assumed to be used to generate the Indexed Credits of the account, expressed as a percent of the account value," required to be consistent with the company's actual hedging program [R1]. This is the regulatory encoding of the option-budget concept: the general-account NIER funds the purchase of index options; the cap/participation level is what that budget buys [R1][R6].
- Charge-funded accounts (multiplier accounts, high-cap accounts, "Select" strategies) add an explicit asset charge that funds a Supplemental Hedge Budget — e.g., Nationwide's 1.0% strategy charge buys a 13.25% cap vs 10.25% without, and Pacific Life's 0.80%/yr charge buys a 12.0% cap vs 10% [S5][S2][R1].
- Insurer marketing confirms dynamic hedging as the production mechanism ("thanks to our indexing experience – plus our dynamic hedging capabilities …") [S8].

---

## Variations across insurers

1. Floor design. Most carriers use a 0% annual floor in the crediting formula (Pacific Life, Nationwide, Securian's indexed accounts, Allianz) [S2][S5][S6][S8]. Transamerica instead credits a guaranteed 0.75% during the segment and nets it out of excess index interest (Basic Interest Account guarantees 2%) [S3]; Securian expresses its guarantee as a 2% cumulative average tested at death/termination [S7]. A representative model should implement the 0% annual floor and optionally a retrospective cumulative guarantee.
2. Index menu. Everyone offers a 1-year S&P 500 (price return, dividends excluded) annual point-to-point account with cap, 100% participation [S2][S3][S5][S6]; beyond that, carriers diverge — multi-index best-performer blends (Transamerica Global 50/30/20; Nationwide Multi-Index Monthly Average 50/30/20; Securian Hindsight) [S3][S5][S7], uncapped S&P 500 with spread (Nationwide) or with declared participation (Pacific Life Dynamic Par) [S5][S2], multi-year segments (Pacific Life 2-year and 5-year) [S2], and uncapped volatility-controlled proprietary indexes with high participation (Pacific Life/BlackRock Endura 200%, Nationwide/JPM Mercury up to 255% & BNPP H-Factor up to 320%, Securian/S&P PRISM 215%, Allianz Bloomberg/PIMCO 160%) [S2][S5][S7][S8].
3. Charge-funded enhancements. Two mechanically different implementations: an ongoing asset charge on the account value (Pacific Life 0.80%/yr; Transamerica 0.72%/yr on all index accounts) [S2][S3] vs an up-front charge deducted from the amount entering the segment (Nationwide 0.65%–1.0%) [S5]. Persistency bonuses also differ: Nationwide's 0.20% Rewards credit from year 16 [S5]; Allianz warns bonus products can carry higher surrender charges/lower caps [S8].
4. Guaranteed minimum crediting parameters vary widely: guaranteed minimum caps range from 0.25% (Allianz) [S8] through 2% (Pacific Life 1-year account) [S2] to 4% (Pacific Life High Cap) [S2]; guaranteed minimum participation from 5% (Allianz, Pacific Life Dynamic Par) [S8][S2] to 105% (Pacific Life 5-year) [S2]; Transamerica guarantees caps never below the current Basic Interest Account rate [S3].
5. Premium loads: level (Transamerica 4% current/6% guaranteed) [S3] vs front-loaded by year (Nationwide 8% yr 1 / 6% renewal, 10% guaranteed) [S5].
6. Surrender charge periods: 10 years (Pacific Life, Nationwide, Securian) [S1][S5][S7] vs 15 years (Transamerica) [S3]; all re-start on face increases [S3][S7].
7. Loans: all carriers offer a declared-rate loan trending to ~0% net cost after ~year 10 and an indexed/participating loan at a 5%-ish charged rate with index-linked crediting [S3][S4][S5][S7]; Pacific Life uniquely routes loaned value to a dedicated lower-par volatility-control account via rider [S2]; Securian imposes a 12-month fixed→indexed transfer lockout after fixed loans [S6].
8. Representative design for a reference model: a flexible-premium UL chassis with (a) fixed account (1% guaranteed floor), (b) 1-year S&P 500 PTP indexed account, 0% floor, 100% participation, current cap ~10–14% with a low guaranteed cap, monthly segment starts, (c) optional charge-funded high-cap/multiplier account, (d) charges = premium load (4–8%), $10/month policy fee, 10-year per-unit charge, COI on NAR, 10-year surrender charge, (e) declared-rate and participating loans, (f) age-based no-lapse guarantee. This matches the common core of [S2][S3][S5][S7] and the AG 49-A Benchmark Index Account definition [R1].

---

## Gaps and caveats

- COI rate tables, per-unit charge tables, and surrender charge tables (actual dollar amounts) are not published in the retrieved brochures — they live in policy data pages / illustration systems. The only numeric tables retrieved are Transamerica's minimum monthly no-lapse premium rates per $1,000 [S3]. A specimen IUL policy form with data pages was not obtained: Pacific Life posts a specimen for a non-indexed UL chassis (form P08VP1) but no IUL specimen was found publicly.
- IUL policies are generally not SEC-registered (no prospectuses on EDGAR); they are state-regulated fixed products, so EDGAR full-text search was not used for the product documents. [unverified] as a general proposition, but consistent with none of the five carriers referencing a prospectus in the retrieved materials.
- S7 (Securian product page) was extracted via WebFetch's summarization model rather than raw text; individual numbers (e.g., the 9.50% Hindsight cap, 65%/215% pars, loan rates) should be re-verified against the underlying page or the Securian product specification PDF before hard-coding.
- Transamerica caps differ between S3 (agent guide, older print: 15%/13.75%) and S4 (09/2022 brochure: 13.00%/12.00%) — caps are redeclared over time; treat any single value as a snapshot.
- Pacific Horizon IUL 2 premium load, admin charge, and coverage charge amounts; Transamerica surrender charge dollar scale; Securian charge amounts — names confirmed, values not public [S1][S3][S6].
- Maturity age / age-121 mechanics not explicitly stated in any retrieved document ([unverified] inference from age-120/121 references in S3).
- R7 (SOA OuYang AG 49 survey) could not be fetched (404 via the fetch tool) and its findings are not used as verified facts. The original AG 49 (2015) text itself was not separately fetched; its provisions are described only via R1's background section and R6.
- ASOP No. 24's December 2016 edition is marked "Superseded" on the ASB page [R9]; the current edition was not retrieved.
- The VM index-credit hedge margin quantification (≥1.5%/20%) sits in VM-21/VM-22 (annuities); VM-20 itself requires hedge cash-flow modeling under CDHS discipline but the retrieved text was not exhaustively searched for a life-side numeric margin [R3].
- All "current" rates are non-guaranteed carrier declarations as of each document's print date (ranging 2017–2026) and change frequently; use them as calibration snapshots, not fixed parameters.
