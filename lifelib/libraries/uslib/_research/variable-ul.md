# Variable Universal Life Insurance (VUL) — research notes (U.S.)

Access date for all citations: 2026-08-03.

Purpose: source library and extracted specifications to drive a reference liability
cash-flow projection model (lifelib/modelx style) for U.S. variable universal life
(VUL) insurance — flexible-premium variable life with account value invested in
registered separate-account subaccounts plus a general-account fixed option.

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). Facts stated from general knowledge and not verified against a
retrieved document are tagged [unverified].

---

## Primary sources

### S1. Pruco Life Insurance Company (Prudential) — "VUL Protector (2015)" statutory prospectus (Form N-6 / 485BPOS)
- Publisher: Pruco Life Insurance Company (Arizona stock company, subsidiary of
  The Prudential Insurance Company of America); registrant is the Pruco Life
  Variable Universal Account (separate account, CIK 0000851693, 1940 Act file
  811-05826).
- Doc type: statutory prospectus (SEC Form N-6, post-effective amendment 485BPOS
  filed 2025-04-15, accession 0000851693-25-000091, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/851693/000085169325000091/plvulpregtofile.htm
- Retrieved: YES (full ~3.0 MB HTML downloaded and text-extracted).
- Product: "VUL Protector (2015)" flexible-premium variable universal life
  contract (protection-oriented VUL with lapse-protection rider). Sold through
  Pruco Securities broker-dealers.
- Key facts extracted (details in "Extracted specifications" below): fee table
  (premium loads, surrender charge, COI, M&E, admin), Type A/Type B death
  benefits, Limited No-Lapse Guarantee + Rider To Provide Lapse Protection,
  Fixed Rate Option (1% floor), standard/preferred loans, persistency credit,
  issue ages/minimum face amounts, age-121 provisions, 7702 CVAT/GPT election.

### S2. Equitable Financial Life Insurance Company — "VUL Optimizer (Series 166)" statutory prospectus (Form N-6 / 485BPOS)
- Publisher: Equitable Financial Life Insurance Company; registrant Separate
  Account FP (CIK 0000771726).
- Doc type: statutory prospectus (485BPOS filed 2025-04-24, accession
  0001193125-25-093072, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/771726/000119312525093072/d925311d485bpos.htm
- Retrieved: YES (full ~2.5 MB HTML downloaded and text-extracted).
- Product: "VUL Optimizer" (Series 166) — accumulation-oriented flexible-premium
  VUL with variable investment options, a Guaranteed Interest Option (GIO), and
  the "Market Stabilizer Option II" (MSO II), an index-linked option covered by
  a separate prospectus.
- Key facts: 6% premium charge (current 4% after 2 target premiums), 10-year
  surrender charge, tiered M&E (1.00%/0.50%), COI on 2017 CSO, GIO 1.5% floor,
  15-year no-lapse guarantee rider, LTC and Cash Value Plus riders, GPT corridor
  factors and CVAT description, loan mechanics (Moody's-based rate, 1% max
  spread).

### S3. The Lincoln National Life Insurance Company — "Lincoln LifeGoals" VUL statutory prospectus (Form N-6 / 485BPOS)
- Publisher: The Lincoln National Life Insurance Company; registrant Lincoln
  Life Flexible Premium Variable Life Account M (CIK 0001048607, 1940 Act
  811-08557, 1933 Act 333-259297).
- Doc type: statutory prospectus (485BPOS filed 2025-04-10, accession
  0001104659-25-033688, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/1048607/000110465925033688/tm253642d1_485bpos.htm
- Retrieved: YES (full ~1.7 MB HTML downloaded and text-extracted).
- Product: "Lincoln LifeGoals", a flexible premium variable universal life
  policy. Notable as a modern low-load design: no premium load, no surrender
  charge. (Lincoln's flagship accumulation VUL "AssetEdge" is filed on the same
  Account M; EDGAR full-text hits for "AssetEdge" main documents pointed to
  annuity accounts for the searched window, so LifeGoals was used as the
  retrievable Lincoln VUL prospectus.)
- Key facts: zero-load structure, COI min/max, monthly M&E 0.6% cap, per-$1,000
  admin fee, no-lapse provision, "Target Age" and Death Benefit Option 2→1
  design, 0.25% net loan spread.

### S4. Pacific Life Insurance Company — "Pacific Select VUL 2" statutory prospectus (Form N-6 / 485BPOS)
- Publisher: Pacific Life Insurance Company; registrant Pacific Select Exec
  Separate Account (CIK 0000832908, 1940 Act 811-05563, 1933 Act 333-231309).
- Doc type: statutory prospectus (485BPOS filed 2025-04-18, accession
  0001104659-25-036303, prospectus dated May 1, 2025).
- URL fetched: https://www.sec.gov/Archives/edgar/data/832908/000110465925036303/tm255241d1_485bpos.htm
- Retrieved: YES (full ~3.4 MB HTML downloaded and text-extracted).
- Product: "Pacific Select VUL 2" variable universal life; coverage-layer
  architecture (Basic Life Coverage Layers plus term-rider layers), death
  benefit options A/B/C, two declared-rate fixed accounts plus indexed fixed
  options, Flexible Duration No-Lapse Guarantee Rider.
- Key facts: 6.50% max premium load, 15-year surrender charge per coverage
  layer, COI guaranteed max on 2017 CSO, $10/mo admin + coverage charge +
  asset charge (0.36% max/0.20% current), fixed account 2.00% floor, loan
  charge 2.25% vs credit 2.00%, FDNLG shadow-fund rider loads (5.5%/10%).

### S5. Prudential Financial — "VUL Protector Prospectus" product page (prudential.com)
- Publisher: Prudential Financial.
- Doc type: insurer web page linking current prospectus (consumer-facing).
- URL fetched: https://www.prudential.com/personal/life-insurance/variable-life-insurance-performance/vul-protector-prospectus
- Retrieved: YES.
- Facts: VUL Protector policy form numbers "VULNT-2009" (most states) and
  "VULNT-2009NY" (New York); issuers Pruco Life Insurance Company (all states
  except NY) and Pruco Life Insurance Company of New Jersey (NY); full
  prospectus served via connect.rightprospectus.com/Prudential?site=VULP.

### S6. Prudential — "VUL Protector Fast Facts" producer sheet (1005325-00009)
- Publisher: Prudential (advisor site).
- Doc type: producer/agent fast-facts sheet (PDF).
- URL attempted: https://www.prudential.com/content/dam/us/sites/advisors/life-insurance/Product-Solutions/living-needs-benefit-rider/1005325-00009_VUL%20Protector%20Fast%20Facts.pdf
- Retrieved: NO (server returned an HTML stub instead of the PDF; fetch failed).
  Listed as a known reference only; no facts cited from it.

---

## Regulatory and actuarial references

### R1. SEC — Form N-6 (registration form for variable life insurance separate accounts)
- Publisher: U.S. Securities and Exchange Commission.
- URL fetched: https://www.sec.gov/files/formn-6.pdf (47-page reference copy,
  SEC 2567, 1/22 version)
- Retrieved: YES (PDF downloaded, full text extracted).
- Facts: Form N-6 "is to be used by separate accounts that are unit investment
  trusts that offer variable life insurance contracts to register under the
  Investment Company Act of 1940 and to offer their securities under the
  Securities Act of 1933." Part A (prospectus) items: 1 Front/Back Cover;
  2 Key Information; 3 Overview of the Contract; 4 Fee Table; 5 Principal
  Risks; 6 General Description of Registrant, Depositor, and Portfolio
  Companies; 7 Charges; 8 General Description of Contracts; 9 Premiums;
  10 Standard Death Benefits; 11 Other Benefits Available Under the Contract;
  12 Surrenders and Withdrawals; 13 Loans; 14 Lapse and Reinstatement;
  15 Taxes; 16 Legal Proceedings; 17 Financial Statements; 18 Portfolio
  Companies Available Under the Contract. Part B (SAI) items 19-29 include
  Item 29 Illustrations; Part C item 30 Exhibits.

### R2. SEC — Release 33-10765: "Updated Disclosure Requirements and Summary Prospectus for Variable Annuity and Variable Life Insurance Contracts" (rule 498A)
- Publisher: U.S. Securities and Exchange Commission.
- URL fetched: https://www.sec.gov/newsroom/press-releases/2020-57 (press
  release; fetched via curl). Final rule text at
  https://www.sec.gov/files/rules/final/2020/33-10765.pdf and Federal Register
  2020-05526 (both blocked to the fetch tool; not retrieved).
- Retrieved: YES (press release page).
- Facts: adopted March 2020; new rule 498A permits satisfying prospectus
  delivery for variable annuity and variable life contracts by delivering a
  concise summary prospectus and making the statutory prospectus available
  online; layered disclosure framework; rule and form amendments effective
  July 1, 2020. Registration form amendments include Form N-6 (the source of
  the standardized "Key Information" and fee-table formats seen in S1-S4).

### R3. IRC §7702 — Definition of life insurance contract
- Publisher: Legal Information Institute (Cornell), U.S. Code.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702
- Retrieved: YES.
- Facts: a contract qualifies as life insurance if it meets either (1) the cash
  value accumulation test (CVAT) — cash surrender value may not exceed the net
  single premium funding future benefits — or (2) the guideline premium
  requirements plus the cash value corridor (death benefit at least specified
  percentages of cash surrender value, 250% for attained ages 0-40 declining
  to 100% at ages 90-95). For contracts issued after 2020, §7702(f)(11)
  defines the "insurance interest rate" as the lesser of the prescribed U.S.
  valuation interest rate (life insurance, >20-year durations) and a 60-month
  average of applicable federal mid-term rates, with a 2% transition rate for
  contracts issued in 2021 (replacing the historical 4% CVAT / 6% GSP rates).

### R4. IRC §7702A — Modified endowment contract (MEC)
- Publisher: Legal Information Institute (Cornell), U.S. Code.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/7702A
- Retrieved: YES.
- Facts: a contract is a MEC if entered into after June 21, 1988 and it fails
  the 7-pay test — cumulative premiums in the first 7 contract years exceed
  the sum of net level premiums that would fund paid-up benefits after 7 level
  annual payments. MEC status triggers less-favorable distribution taxation
  (per §72(e)(10), referenced) for the failure year and later years, and
  distributions within 2 years before failure are treated as anticipatory.
  Material changes (e.g., death benefit increases) restart 7-pay testing as a
  new contract with cash-value adjustment.

### R5. IRC §817(h) — Diversification requirements for variable contracts
- Publisher: Legal Information Institute (Cornell), U.S. Code.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/817
- Retrieved: YES.
- Facts: a variable contract based on a segregated asset account is not treated
  as life insurance for any period in which the account's investments are not
  adequately diversified; safe harbor if the account satisfies §851(b)(3)
  standards and no more than 55% of assets are in one issue; special rule
  deems accounts invested in U.S. Treasury securities adequately diversified
  for variable life; look-through treatment for insurance-dedicated funds.

### R6. Treas. Reg. §1.817-5 — Diversification requirements
- Publisher: Legal Information Institute (Cornell), 26 CFR.
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.817-5
- Retrieved: YES.
- Facts: adequate diversification requires no more than 55% of account value in
  any one investment, 70% in any two, 80% in any three, 90% in any four;
  testing on the last day of each calendar quarter (or within 30 days);
  look-through to underlying assets of insurance-dedicated RICs/partnerships/
  trusts; failure disqualifies life-insurance treatment for the affected
  quarters.

### R7. NAIC — Valuation Manual, Jan. 1, 2025 edition (incl. VM-01, VM-20, VM-A/VM-C appendices)
- Publisher: National Association of Insurance Commissioners.
- URL fetched: https://content.naic.org/sites/default/files/pbr-data-valuation-manual-2025-edition.pdf
  (356-page PDF downloaded, text extracted).
- Retrieved: YES.
- Facts:
  - VM-01 definition: "The term 'variable life insurance policy' means a policy
    that provides for life insurance, the amount or duration of which varies
    according to the investment experience of any separate account or accounts
    established and maintained by the insurer as to the policy."
  - VM-20 ("Requirements for Principle-Based Reserves for Life Products")
    establishes the minimum reserve valuation standard (CRVM) for individual
    life policies issued on or after the Valuation Manual operative date —
    this includes VUL. Sections: 1 Purpose, 2 Minimum Reserve, 3 Net Premium
    Reserve (NPR), 4 Deterministic Reserve (DR), 5 Stochastic Reserve (SR),
    6 Exclusion Tests, 7 Cash-Flow Models, 8 Reinsurance, 9 Assumptions,
    App. 1 Economic Scenarios, App. 2 Asset Default Costs/Spreads.
  - Minimum reserve structure: policies fall into three reserving categories
    (Term, ULSG, All Other); for each, minimum reserve = sum of policy minimum
    NPRs plus the excess, if any, of the greater of DR and SR over (aggregate
    NPR minus due/deferred premium asset); companies may exclude groups from
    SR/DR via the stochastic/deterministic exclusion tests (SET/DET). VUL
    without secondary guarantees typically falls in the "All Other" category;
    VUL with secondary guarantees is ULSG-category [the categorization of VUL
    products between these categories is by presence of secondary guarantee —
    VM-20 Section 2 as extracted; see also product coding below].
  - The VM's statutory product-coding tables list "Variable Life Plans (without
    Secondary Guarantees)" (code 080) and "Variable Life Plans with Secondary
    Guarantees" (code 090) as distinct valuation product groups.
  - SET certification method is available "for groups of policies other than
    variable life" — i.e., variable life must use the ratio-based stochastic
    exclusion test rather than certification (VM-20 Section 6 as extracted).
  - VM-21 scope guidance: for an individual variable life contract with a GMDB
    and a VAGLB-like benefit, VM-21-style requirements apply only to the
    VAGLB-type benefit "since there is an explicit reserve requirement that
    applies to the variable life contract and the GMDB."
  - VM-C (appendix of actuarial guidelines) includes AG XXIII "Guideline
    Concerning Variable Life Insurance Separate Account Investments" and AG
    XXXVII "Variable Life Insurance Reserves for Guaranteed Minimum Death
    Benefits"; VM-A includes A-270 "Variable Life Insurance" (the model
    regulation as valuation requirement).

### R8. NAIC — Variable Life Insurance Model Regulation (Model #270)
- Publisher: National Association of Insurance Commissioners (January 1996
  printing with comments).
- URL fetched: https://content.naic.org/sites/default/files/model-law-270.pdf
  (66-page PDF downloaded, text extracted).
- Retrieved: YES.
- Facts: sections — 1 Authority; 2 Definitions; 3 Qualification of Insurer to
  Issue Variable Life Insurance; 4 Insurance Policy Requirements; 5 Reserve
  Liabilities for Variable Life Insurance; 6 Separate Accounts; 7 Information
  Furnished to Applicants; 8 Applications; 9 Reports to Policyholders;
  10 Foreign Companies; 11 Agent Qualifications; 12 Separability. Policy
  requirements include grace periods: scheduled-premium policies must have a
  grace period of "not less than" a stated period with values unaffected if
  premium paid within it; flexible premium policies must have a grace period
  ending not less than 61 days (per extracted text "not less than sixty-...")
  after specified notice, with the death benefit during grace equal to the
  death benefit in effect. Reserve liabilities for variable benefits must be
  held in the separate account and determined "on a basis consistent with the
  Standard Valuation Law," applied "in a manner that is actuarially consistent
  with the variable nature of the benefits"; commentary notes minimum death
  benefit guarantee reserves historically referenced the then-current standard
  ("the 1958 CSO mortality table and a rate of interest not in excess of
  3.5%" in the 1996 commentary).

### R9. ASB — ASOP No. 52, "Principle-Based Reserves for Life Products under the NAIC Valuation Manual"
- Publisher: Actuarial Standards Board.
- URL fetched: http://actuarialstandardsboard.org/wp-content/uploads/2017/10/asop052_189.pdf
  (39-page PDF downloaded, text extracted).
- Retrieved: YES.
- Facts: adopted by the ASB September 2017; provides guidance to actuaries
  performing principle-based valuations consistent with VM-20; states that in
  a conflict between the Valuation Manual in effect and the ASOP, the
  Valuation Manual governs.

### R10. American Academy of Actuaries — practice note "Life Principle-Based Reserves (PBR) Under VM-20" (April 2020)
- Publisher: American Academy of Actuaries, Life Valuation Committee work group.
- URL fetched: https://actuary.org/wp-content/uploads/2020/04/VM-20_PN_2020_Version_0.pdf
  (115-page PDF downloaded; title/front matter verified, body used as Q&A
  reference).
- Retrieved: YES.
- Facts: public policy practice note in Q&A format on applying VM-20 (NPR, DR,
  SR, exclusion tests, assumptions including mortality credibility and lapse)
  for life products under PBR.

### R11. ASB — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products"
- Publisher: Actuarial Standards Board.
- URL fetched: https://www.actuarialstandardsboard.org/asops/asop-no-2-nonguaranteed-elements-for-life-insurance-and-annuity-products/
- Retrieved: YES (standard's landing page/summary).
- Facts: revision adopted September 2021, effective June 1, 2022; applies to
  actuarial services on the determination of nonguaranteed elements (NGEs) for
  life and annuity products including universal life (fixed, variable, or
  indexed); example NGEs include "credited interest, cost of insurance (COI)
  charges, bonuses, indeterminate premiums, index parameters used to determine
  credited interest, and expense charges"; requires a determination policy,
  policy classes reflecting anticipated experience, and NGE scales "based on
  reasonable expectations of future experience and ... not determined with the
  objective of recouping past losses or distributing past gains." Directly
  governs the current-vs-guaranteed charge structure seen in S1-S4.

### R12. Society of Actuaries — 2017 Commissioners Standard Ordinary (CSO) Tables
- Publisher: Society of Actuaries.
- URL fetched: https://www.soa.org/resources/experience-studies/2015/2017-cso-tables/
- Retrieved: YES.
- Facts: the 2017 CSO table family (composite, smoker-distinct, preferred
  structure, gender-blended, loaded/unloaded, ANB/ALB, ultimate variants) is
  published by the SOA and "widely used in US life insurance pricing and
  statutory reserving"; developed because ILEC industry experience studies
  showed significant mortality improvement versus the 2001 CSO basis and to
  reflect preferred underwriting. (Guaranteed maximum COI rates in S2/S4 cite
  2017 CSO; S1's older-generation product still uses 2001 CSO.)

### R13. FINRA — "Insurance" investor product page (variable life / VUL)
- Publisher: FINRA.
- URL fetched: https://www.finra.org/investors/investing/investment-products/insurance
- Retrieved: YES.
- Facts: variable life insurance is "a type of security"; cash value is
  invested in policyholder-selected portfolios; investment return is not
  guaranteed and cash value fluctuates; VUL "combines features of universal
  life insurance and variable life insurance" (flexible premiums + investment
  account); variable life/VUL require SEC registration and FINRA regulates the
  firms and professionals selling them; suitability framing (know the
  investor's situation, risk tolerance). Related FINRA Rule 2211
  ("Communications with the Public About Variable Life Insurance and Variable
  Annuities", https://www.finra.org/rules-guidance/rulebooks/finra-rules/2211)
  was identified via search but its text was not fetched (known reference
  only).

---

## Extracted specifications

### 1. Product architecture and registration
- A VUL policy is a flexible-premium individual life insurance contract whose
  account value ("Contract Fund" [S1], "policy account value" [S2],
  "Accumulation Value" [S3], "Accumulated Value" [S4]) is allocated among
  (a) variable investment options (subaccounts of a registered separate
  account, each investing in a corresponding registered fund) and (b) one or
  more general-account fixed options [S1][S2][S3][S4].
- The separate account is registered as a unit investment trust and the
  contract is registered on SEC Form N-6 [R1]; prospectuses follow the N-6
  item structure (Key Information table, standardized fee tables, Standard
  Death Benefits, Other Benefits, Loans, Lapse) [R1][S1][S2][S3][S4], with
  summary-prospectus delivery permitted under rule 498A since July 1, 2020
  [R2].
- Death benefits and account values reflect investment experience; obligations
  and any guarantees are backed by the insurer's general account claims-paying
  ability [S1][S4]. Variable life is defined for statutory purposes as life
  insurance whose amount or duration varies with separate-account investment
  experience [R7].
- Examples of issuers/registrants: Pruco Life Variable Universal Account
  (811-05826) [S1]; Equitable Separate Account FP [S2]; Lincoln Life Flexible
  Premium Variable Life Account M (811-08557) [S3]; Pacific Select Exec
  Separate Account (811-05563) [S4].

### 2. Issue ages, face amount bands, underwriting
- Prudential VUL Protector: issue through age 85; minimum Basic Insurance
  Amount $75,000 (issue ages 18-75), $50,000 (0-17), $100,000 (76-80),
  $250,000 (81+); $250,000 minimum with Enhanced Cash Value Rider, $100,000
  with BenefitAccess Rider [S1].
- Equitable VUL Optimizer: available for issue ages 0-85 [S2]; footnotes
  reference a possible $10,000 minimum face amount stated in the policy
  (waiving the $10 monthly admin fee case) [S2]; Cash Value Plus Rider
  requires minimum face $250,000 (1-2 lives of an insured group) or $100,000
  (3+ lives) [S2].
- Underwriting classes: Prudential "preferred best" through substandard with
  flat extras ($0.10-$2.08 per $1,000/month for health/occupation/avocation/
  aviation risks) [S1]; Equitable "preferred elite non-tobacco" representative
  class [S2]; Pacific Life offers guaranteed issue, simplified issue, and
  regular issue (COI rates generally higher for GI/SI) [S4]; representative
  insured conventions in fee tables (e.g., female 43 preferred best [S1]; male
  35 preferred elite non-tobacco [S2]; male 40 target 65 [S3]; male 45
  standard non-smoker [S4]).
- Contract backdating to lower issue age permitted up to 6 months (Prudential)
  [S1].

### 3. Premium structure
- Premiums are flexible after a required initial premium: Prudential's minimum
  initial premium equals 8.6% of the Limited No-Lapse Guarantee Premium
  (including rider extras); thereafter amounts/timing discretionary subject to
  $25 minimum [S1]. Insurers may refuse premiums that would increase the death
  benefit under §7702 by more than the premium increases the fund, or that
  would exceed the Guideline Premium Limit; excess premium creating MEC status
  must be removed timely [S1][R3][R4].
- Premium loads (deducted from each premium):
  - Prudential: sales charge max 6% (current 3% in years 1-5, 2.25% years
    6-10, 0 thereafter) plus premium-based administrative charge max 7.5%
    (current 3.75%; covers premium taxes and premium-based costs) [S1].
  - Equitable: premium charge 6% of each premium (maximum); currently reduced
    to 4% after two sales-load "target premiums" have been paid (target
    premium actuarially determined per policy) [S2].
  - Lincoln LifeGoals: no sales load on premiums; company does not assess a
    premium tax charge to the owner; no deferred sales charge [S3].
  - Pacific Life: maximum sales charge 6.50% of premium [S4].

### 4. Charge structure (monthly deductions and asset charges)
- Cost of insurance (COI): deducted monthly, rate per $1,000 of Net Amount At
  Risk (NAR = death benefit − account value [S2], same concept in all four):
  - Prudential: current COI $0.02-$83.34 per $1,000 NAR (highest = insured age
    120); guaranteed maximum rates based on 2001 CSO tables varying by sex,
    smoker class, attained age; rates vary by band (Basic Insurance Amount),
    duration, issue age, sex, underwriting class; two-tiered COI rate design
    with duration/class-dependent tier breakpoint; representative female 43
    preferred best $250k: $0.13 [S1].
  - Equitable: COI $0.01-$83.34 per $1,000 at-risk (rep male 35 elite: $0.08);
    guaranteed maximums on 2017 CSO — gender-neutral policies use an 80% male/
    20% female blended 2017 CSO ultimate ANB table; sex-distinct policies use
    male/female smoker/nonsmoker 2017 CSO ultimate ANB; composite tables under
    age 18 [S2].
  - Lincoln: COI maximum $83.33333, minimum $0.02667 per $1,000 NAR; rep
    (male, issue age 40, Target Age 65, year 1) maximum $0.17771 [S3].
  - Pacific Life: guaranteed COI $0.01-$83.34 per $1,000 NAR (rep male 45
    standard NT year 1: guaranteed $0.22, current $0.04); guaranteed rates
    calculated using 2017 Commissioners Standard Ordinary tables; COI rates
    uniform within a "Class" [S4].
  - Note the common $83.33-$83.34 cap = 1/12 of $1,000, i.e., the monthly rate
    that fully consumes the NAR at attained age 120/121 [S1][S2][S3][S4]
    (interpretation [unverified]).
- Mortality & expense risk (M&E) / asset-based charges on separate-account
  assets:
  - Prudential: 0.45% effective annual rate, deducted daily against variable
    investment options [S1].
  - Equitable: 1.00% annual in policy years 1-10, 0.50% in years 11+, deducted
    monthly on value in variable options and MSO II [S2].
  - Lincoln: maximum 0.6% effective annual as % of separate-account value,
    deducted monthly; guaranteed at 0.6% for policy years 1-20 [S3].
  - Pacific Life ("asset charge"): guaranteed maximum 0.36% annually (0.03%
    monthly), current 0.20% annually (0.0167% monthly), on unloaned
    Accumulated Value [S4].
- Per-policy and per-$1,000 administrative charges (monthly):
  - Prudential: $0.07-$8.21 per $1,000 of Basic Insurance Amount plus $9 flat
    (rep: $0.21 + $9); per-$1,000 portion varies by issue age/sex/class and is
    currently deducted only during the first 7 contract years [S1].
  - Equitable: $10 flat per month (all years) plus $0.15-$0.47 per $1,000 of
    initial base face and post-increase face (rep $0.20) [S2].
  - Lincoln: up to $0.31263 per $1,000 of Initial Life Insurance Amount
    (minimum $0.10290; rep $0.1262), varying by gender, Target Age, Issue Age
    [S3].
  - Pacific Life: administrative charge $10.00/month (guaranteed = current)
    plus "coverage charge" of $29.00-$40.00 per policy plus guaranteed
    $0.09-$11.39 per $1,000 of Basic Life Coverage Layer (current $0.00-$3.81;
    rep male 45: max $40 + $0.55, current $40 + $0.49); varies by age, sex,
    risk class and death benefit option; layer charge fixed at layer issue
    [S4].
- Fund (portfolio) operating expenses borne via unit values:
  - Prudential: 0.29%-1.18% [S1]; Equitable: 0.55%-2.88% gross / 0.54%-2.57%
    net of expense limitation; Equitable additionally credits an "Investment
    Expense Reduction" to daily unit values, at least 0.15%, computed from a
    3-tier formula based on the portfolio's net expense ratio (e.g., portfolio
    at 0.75% net → 0.35% reduction) [S2]; Lincoln: 0.46%-2.54% [S3]; Pacific
    Life: 0.08%-1.93% [S4].
- Charges are quoted as guaranteed maxima with lower current (nonguaranteed)
  rates that the insurer may raise up to the maximum; changes must be by class
  and cannot recoup prior losses or distribute prior gains [S1] — the NGE
  framework governed by ASOP No. 2 [R11].

### 5. Surrender charges and transaction fees
- Prudential: surrender charge during first 14 contract years on lapse, full
  surrender, or Basic Insurance Amount decrease (including via withdrawal or
  DB-type change); initial charge $5.31-$54.56 per $1,000 of BIA varying by
  issue age/sex/class (rep female 43: $17.55/1,000; max applies to male 65
  substandard); declines to zero by end of year 14; not deducted from death
  benefit [S1]. Transfer fee $25 per transfer beyond 12/year; withdrawal fee
  $25; BIA decrease fee $25 [S1].
- Equitable: surrender charge during first 10 policy years (and 10 years after
  each requested face increase, additive): $11.40-$48.50 per $1,000 of initial
  base face (rep male 35: $18.29); pro-rata charge on face decreases; Cash
  Value Plus Rider can waive/refund [S2]. Transfer charge $25 (waived for
  transfer of all variable amounts to GIO and automated programs); wire $90,
  express mail $35, returned payment $35 [S2].
- Lincoln LifeGoals: no surrender charge or deferred sales load; transfer fee
  $25 per transfer beyond 24 per policy year [S3].
- Pacific Life: maximum surrender charge $49.72 per $1,000 of Basic Face
  Amount, applying while any Basic Life Coverage Layer has been in force less
  than 15 policy years; per-layer charge based on age, risk class, face and
  death benefit option; reduces to $0 after 15 years per layer; withdrawal
  charge $25 and transfer fee $25 (>12/year) authorized but "currently do not
  impose"; $100 administrative charges on certain rider/face-increase
  transactions [S4].

### 6. Death benefit options and 7702 mechanics
- Two or three death benefit options:
  - Type A / Option A / Option 1: level — DB = face amount (Basic Insurance
    Amount); NAR shrinks as fund grows [S1][S2][S4] (Lincoln's "Option 1"
    equivalent; LifeGoals issues with Option 2 and permits change to Option 1
    at/after Target Age [S3]).
  - Type B / Option B / Option 2: variable — DB = face amount + account value;
    NAR roughly constant [S1][S2][S3][S4].
  - Option C (Pacific Life): DB = face amount + premiums paid − withdrawals,
    subject to an Option C DB limit [S4]. (Prudential/Equitable/Lincoln
    LifeGoals do not offer a return-of-premium option in these filings.)
- DB option changes permitted subject to approval; a change adjusts face so
  that total DB is unchanged at the change date [S1]; Lincoln allows Option 2
  → Option 1 change during a specified Change Period, increasing face by the
  account value then potentially decreasing face to produce a zero Guideline
  Level Premium [S3].
- 7702 qualification: owner elects Cash Value Accumulation Test or Guideline
  Premium Test at issue [S1]; corridor: minimum DB as percentage of account
  value under GPT, e.g., Equitable's representative factors 250% (ages ≤40),
  215% (45), 185% (50), 150% (55), 130% (60) [S2], consistent with the
  §7702(d) corridor [R3]. Under CVAT the alternate DB is account value times
  the reciprocal of the net single premium at 2% interest and 2017 CSO
  mortality (101% above age 99) [S2].
- Insurers reserve the right to increase DB automatically to preserve §7702
  qualification and to refuse premiums breaching guideline limits [S1][S2].
- Death benefit payable is reduced by outstanding policy debt and, during
  grace, amounts required to keep the policy in force [S3][S1].

### 7. No-lapse (secondary) guarantees
- Prudential VUL Protector: built-in at no extra charge — Limited No-Lapse
  Guarantee protects during the first 5 contract years (conditional on
  Accumulated Net Payments exceeding a No-Lapse Guarantee Value and no
  contract debt), plus a "Rider To Provide Lapse Protection" from year 6
  onward (premium-funded lapse protection); loans void the protection [S1].
- Equitable: No-Lapse Guarantee rider at no extra charge; guards against lapse
  for 15 years for issue ages 0-70, grading down to 5 years for issue ages 80+,
  subject to specified guarantee premiums; terminates if policy loans plus
  accrued interest exceed account value [S2].
- Lincoln LifeGoals: No-Lapse Provision at no charge: policy will not lapse if
  cumulative premiums (less withdrawals and debt) ≥ cumulative No-Lapse
  Premiums due since issue and 12 monthly No-Lapse Premiums were paid within
  the past 15 policy months; no-lapse period length depends on issue age and
  Target Age [S3].
- Pacific Life: optional Flexible Duration No-Lapse Guarantee Rider, charge
  $0.00-$0.15 per $1,000 NAR monthly (rep $0.05); rider benefit tracked via a
  shadow-fund mechanism using notional loads — a No-Lapse Premium Load of
  5.50% of premium and an Excess Premium Load of 10% (loads used only to
  determine rider benefits, not actual deductions), with Basic Fund/Excess
  Fund balances floored at zero [S4].
- Statutory note: VUL with secondary guarantees is a distinct valuation
  category ("Variable Life Plans with Secondary Guarantees", code 090) and is
  treated in the ULSG reserving category under VM-20; GMDB reserves for
  variable life are addressed by AG XXXVII [R7].

### 8. Fixed accounts and interest crediting
- Prudential Fixed Rate Option: general-account option credited daily at a
  declared effective annual rate, guaranteed minimum 1%; transfers out limited
  to greater of 25% of the option value or $2,000 per contract year (generally
  one transfer out per year) [S1].
- Equitable Guaranteed Interest Option (GIO): guaranteed minimum crediting
  1.5% annual; transfers into unloaned GIO limited (greater of $500 or 25% of
  variable option value) when the current rate equals the guaranteed minimum
  [S2]. Equitable also offers MSO II, an index-linked segment option with a
  1.65% annual Variable Index Segment Account Charge and an Early Distribution
  Adjustment of up to 90% of segment value on pre-maturity distributions
  (full detail in a separate MSO II prospectus) [S2].
- Lincoln LifeGoals: loan account is the general-account feature; credited at
  no less than 0.25% (product is otherwise fully variable in this filing)
  [S3].
- Pacific Life: two declared-rate fixed options — Fixed Account and Fixed LT
  Account — each credited daily (365-day year) with minimum annual interest
  2.00%; declared higher rates guaranteed to the next policy anniversary;
  aggregate fixed-option allocations may be limited to $1,000,000 per owner/
  payor; plus unregistered Indexed Fixed Options (e.g., one with guaranteed
  participation rate 140%, 2% guaranteed minimum growth cap, 1% guaranteed
  interest floor; another with 100% participation, 3% minimum growth cap, 1%
  floor) [S4].

### 9. Policy loans
- Prudential: loan value = 99% of cash value in variable options plus 100% of
  the remainder; standard loans charged 2% effective annual, loaned amount
  credited 1% → net 1% spread; on/after the 10th contract anniversary all
  loans become preferred: charged 1.05% vs credited 1% → net 0.05%; interest
  due each anniversary, capitalized if unpaid; loan/debt ≥ fund less surrender
  charge triggers default; loans prevent no-lapse guarantees from applying;
  no minimum loan amount [S1].
- Equitable: loan interest charged = greater of 2.5% or the Moody's Corporate
  Bond Yield Average (monthly average corporates, two-month lag); collateral
  credited rate guaranteed ≥1.5% and spread guaranteed ≤1%; current practice:
  spread 1% in years 1-10, 0% from year 11 [S2].
- Lincoln: net loan spread 0.25% annualized (loan account credited ≥0.25%);
  loaned amounts move from subaccounts to the general-account loan account
  [S3].
- Pacific Life: loan interest charge 2.25% of loan-account balance annually;
  loan account credited minimum 2.00% (net guaranteed spread ≤0.25%); annual
  true-up transfers between investment options and loan account [S4].
- Overloan protection riders prevent lapse from excess debt: Prudential
  one-time charge 3.5% of Contract Fund on exercise [S1]; Pacific Life
  Overloan Protection 3 exercise charge 1.12%-4.52% of Accumulated Value
  (rep male 85: 2.97%) [S4]. Equitable offers a Loan Extension Endorsement
  (DB option forced to A) [S2].

### 10. Withdrawals, surrender, lapse, reinstatement
- Withdrawals: Prudential minimum $500, $25 fee, cash surrender value after
  withdrawal must cover two months of deductions; Type A withdrawals reduce
  face and can trigger pro-rata surrender charge [S1]. Equitable: partial
  withdrawal reduces Option A face proportionately (monthly charges adjust)
  [S2]. Pacific Life: $25 authorized withdrawal charge currently waived;
  withdrawals may reduce Total Face Amount under Option A [S4].
- Lapse: contract is in default when fund less surrender charge less debt ≤ 0
  (or debt ≥ fund less surrender charge), unless a no-lapse guarantee applies;
  grace period with notice (Prudential: 61-day grace from notice for excess
  debt default; notice premium ≈ 3 months of deductions) [S1]; Model 270
  requires grace-period minimums and death benefit during grace [R8].
- Reinstatement/restoration: Equitable permits restoration within 3 years of
  termination with evidence of insurability and payment covering ~3 months of
  deductions plus premium charge [S2].
- Maturity/age 121: Prudential — from the anniversary at insured age 121, no
  further premiums accepted and no monthly deductions; M&E and fund expenses
  continue; contract continues to death or surrender; lapse only from excess
  debt [S1]. Equitable — monthly charges not applicable after insured reaches
  age 121 [S2]. Pacific Life — "Monthly Deduction End Date" is the policy
  anniversary when the insured attains age 121; no premiums accepted after
  [S4].

### 11. Riders (charge structures actually observed)
- Accelerated death benefit / chronic & terminal illness: Prudential
  BenefitAccess Rider (2% or 4% monthly benefit; current charge $0.0021-$14.74
  or $0.004-$22.11 per $1,000 rider NAR; $150 terminal-illness transaction
  charge); Living Needs Benefit $150 processing [S1]. Equitable Living
  Benefits Rider (terminal illness; $100 post-issue election, $250 exercise;
  $500,000 max) and Long-Term Care Services Rider ($0.23-$2.95 per $1,000
  at-risk depending on nonforfeiture option; rep $0.50-$0.53) [S2]. Pacific
  Life Premier LTC Rider (guaranteed $0.02-$1.87, current $0.01-$1.15 per
  $1,000 LTC NAR) and Terminal Illness Rider ($100 processing) [S4].
- Term riders layered on base: Pacific Life Annual Renewable Term Rider and
  Scheduled ART (COI $0.01-$83.34 per $1,000 NAR + coverage charge guaranteed
  $0.10-$11.96 per $1,000, current $0 for scheduled version), SVER corporate
  term rider [S4].
- Waiver riders: Prudential Enhanced Disability Benefit (7.08%-12.17% of
  monthly benefit; benefit = greater of 9% of no-lapse premium and total
  monthly deductions; to age 60) [S1]; Equitable Disability Deduction Waiver
  (7%-132% of other monthly charges; rep 12%; issue ages 0-59, coverage cap
  $3,000,000) and Disability Waiver of Premium/Monthly Deductions ($0.01-$0.60
  per $1,000) [S2].
- Children's term: Prudential $0.42 per $1,000/month [S1]; Equitable $0.50 per
  $1,000 [S2].
- Accidental death: Prudential $0.04-$0.28 per $1,000 to age 100 [S1].
- Guaranteed insurability: Equitable Option to Purchase Additional Insurance
  ($0.04-$0.17 per $1,000; option amounts $25,000-$100,000; issue ages 0-37)
  [S2].
- Enhanced early cash value: Prudential Enhanced Cash Value Rider (one-time
  $0.50 per $1,000 BIA) [S1]; Equitable Cash Value Plus Rider ($0.04 per
  $1,000 face monthly; waives/reduces surrender charge in first 8 years and
  refunds part of premium charges on surrender in first 3 years — not on
  1035 exchanges) [S2].
- No-charge riders: Equitable Charitable Legacy Rider [S2]; built-in no-lapse
  guarantees (see §7).

### 12. Credits back to the policy
- Prudential persistency credit: from the 9th contract anniversary, monthly
  credit at a current annual rate of 0.40% (0.03327% monthly) of Contract Fund
  net of loans, while in force [S1].
- Equitable Investment Expense Reduction: daily unit-value credit ≥0.15%,
  larger for high-expense portfolios per fixed 3-tier formula [S2].
- Equitable M&E step-down (1.00%→0.50% after year 10) and Prudential sales
  load step-downs act as duration credits [S2][S1].

### 13. Transfers and investment restrictions
- Transfer allowances before fees: Prudential 12 free transfers/year ($25
  each thereafter) [S1]; Lincoln 24/year [S3]; Pacific Life 12/year [S4];
  Equitable charges $25 per transfer subject to waivers [S2].
- Fixed-option transfer-out restrictions (anti-disintermediation): Prudential
  greater of 25%/$2,000 per year [S1]; Equitable GIO in/out limits tied to
  crediting at the minimum [S2]; Pacific Life notes multi-year transfer-out
  schedules possible [S4].
- Separate-account diversification must satisfy §817(h)/Treas. Reg. 1.817-5
  (55/70/80/90 quarterly tests, look-through for insurance-dedicated funds)
  for the contract to remain life insurance for tax purposes [R5][R6].

### 14. Statutory valuation and actuarial framework (model-relevant)
- VUL is individual life insurance subject to VM-20 principle-based reserves
  for policies issued on/after the Valuation Manual operative date: minimum
  reserve = NPR floor plus excess of max(Deterministic Reserve, Stochastic
  Reserve) over aggregate NPR (less due/deferred premium asset), with
  exclusion tests available (variable life cannot use the SET certification
  method) [R7]. VUL without secondary guarantees: "all other" category; with
  secondary guarantees: ULSG category [R7].
- GMDB reserves for variable life are governed by AG XXXVII; separate-account
  investment rules by AG XXIII; A-270 (Model 270) is the underlying variable
  life regulation, requiring separate-account reserves consistent with the
  Standard Valuation Law [R7][R8].
- Guaranteed COI maxima observed use 2001 CSO (older-generation S1) or 2017
  CSO (S2, S4) [S1][S2][S4]; the 2017 CSO family is published by the SOA and
  used for pricing/statutory reserving [R12].
- Federal tax: §7702 CVAT/GPT + corridor (post-2020 dynamic "insurance
  interest rate", 2% transition in 2021 — hence CVAT net single premiums at 2%
  in S2's CVAT description) [R3][S2]; §7702A 7-pay/MEC [R4]; §817(h)
  diversification [R5][R6].
- Nonguaranteed element management (current COI/loads/credits vs guarantees)
  falls under ASOP No. 2 [R11]; PBR work under ASOP No. 52 and the AAA VM-20
  practice note [R9][R10].
- Sales/disclosure: Form N-6 registration and 2020 summary prospectus
  framework [R1][R2]; FINRA regulates distribution; VUL is a security
  [R13].

---

## Variations across insurers

1. Load structure. Two clear archetypes: (a) front-loaded + back-loaded
   traditional VUL — premium loads of 6%-7.5% max (current 3%-4%) plus 10-15
   year surrender charge (Prudential [S1], Equitable [S2], Pacific Life [S4]);
   (b) low-load/no-load designs — Lincoln LifeGoals has no premium load and no
   surrender charge, compensating through asset-based and per-$1,000 charges
   [S3]. The (a) design remains the dominant retail pattern.
2. M&E / asset charge. Wide range: 0.20% current/0.36% max (Pacific Life,
   monthly, on unloaned AV) [S4]; 0.45% daily (Prudential) [S1]; 0.6% max
   (Lincoln, monthly, guaranteed 20 years) [S3]; 1.00%/0.50% tiered by
   duration (Equitable) [S2]. Deduction frequency differs (daily via unit
   value vs monthly deduction).
3. COI basis. All four quote per-$1,000-NAR monthly rates capped near
   $83.33-$83.34; guaranteed maxima moved from 2001 CSO (older product
   generations still sold, e.g., S1) to 2017 CSO (S2, S4). Prudential layers a
   two-tier COI rate structure; banding by face amount is explicit in S1.
4. Death benefit options. Options A (level) and B (increasing) universal;
   return-of-premium Option C appears only at Pacific Life among these four
   [S4]. Lincoln's design pivots on a "Target Age" with an expected Option 2 →
   Option 1 switch [S3].
5. Secondary guarantees. Everything from short built-in guarantees (5-year
   [S1]; formula-based, age-graded 15→5 years [S2]; premium-test no-lapse
   provision [S3]) to a priced flexible-duration shadow-fund rider ($0.00-
   $0.15 per $1,000 NAR with notional 5.5%/10% loads) [S4].
6. Fixed/indexed options. Guaranteed minimum crediting: 1% [S1], 1.5% [S2],
   2% [S4]. Pacific Life and Equitable bolt indexed accounts onto VUL chassis
   (Indexed Fixed Options [S4]; MSO II segment option with 1.65% charge and
   90% early-distribution adjustment [S2]) — a growing hybrid pattern.
7. Loans. Net spreads range from 0.05%-1% (duration-dependent preferred loans,
   Prudential [S1]; 1%→0% Equitable [S2]) to flat 0.25% (Lincoln [S3],
   Pacific Life [S4]). Equitable's charged rate is Moody's-linked variable;
   others are fixed.
8. Credits. Persistency credits (0.40% of fund from year 9, Prudential [S1]),
   unit-value expense reductions (Equitable [S2]), and duration step-downs of
   loads/M&E are insurer-specific NGE features.
9. Representative design. For a reference model, the most representative
   mainstream design is the S1/S2-style retail VUL: flexible premiums with a
   ~6% maximum premium load (current ~3-4%), 10-14 year per-$1,000 surrender
   charge schedule, monthly deductions = COI on NAR (current scale below a
   2017 CSO guaranteed maximum) + $10-ish per-policy fee + per-$1,000 face
   charge (often limited to early years) + asset-based M&E (0.25%-1.00% with
   possible duration step-down), death benefit options A/B with §7702
   corridor, general-account fixed option with 1%-2% floor, spread-based
   loans, and an age-graded no-lapse guarantee; monthly deductions cease at
   age 121.

---

## Gaps and caveats

- Full COI rate tables by age/sex/class/duration are not disclosed in
  prospectuses — only min/max/representative rates; actual scales live in
  policy data pages and actuarial memoranda, which are not public. A model
  needs a proxy (e.g., percentage of 2017 CSO) [unverified].
- Complete surrender charge schedules per $1,000 by issue age/class (S1, S2,
  S4) are shown in the contract data pages, not in the prospectus body; only
  ranges, representative values, and durations (10/14/15 years) were
  extractable.
- Current declared fixed-account crediting rates and current COI scales are
  nonguaranteed and not stated numerically in the filings beyond floors and
  representative examples.
- Nationwide (VUL Accumulator) could not be verified: EDGAR full-text search
  for "Nationwide VUL Accumulator" returned zero hits, suggesting different
  naming in filings; not pursued further. Lincoln "AssetEdge" main prospectus
  document was not isolated (FTS hits were fund exhibits on annuity accounts);
  Lincoln coverage relies on LifeGoals [S3]. John Hancock "Accumulation VUL"
  filings exist (seen in FTS results) but were not retrieved.
- The full SEC final rule text 33-10765 and the Federal Register version were
  blocked to the fetch tools (403/bot-block); facts cited from the SEC press
  release [R2] only. Form N-6 item detail beyond the item list was skimmed,
  not exhaustively extracted.
- NAIC Model 270 text retrieved is the January 1996 printing with commentary;
  state adoptions vary and some states apply successor rules; the 1958
  CSO/3.5% reference is historical commentary, not current requirements [R8].
- AG XXXVII and AG XXIII were confirmed as titles listed in the Valuation
  Manual appendix [R7]; their full texts were not separately retrieved.
- SOA VUL-specific policyholder-behavior/lapse experience studies were not
  retrieved (only the 2017 CSO landing page [R12]); premium persistency and
  dynamic lapse assumptions for VUL modeling remain unsourced [unverified].
- FINRA Rule 2211 (communications about variable life) identified but text not
  fetched; suitability treated only briefly per task scope [R13].
- MSO II (Equitable) and Indexed Fixed Options (Pacific Life) are covered by
  separate prospectuses/disclosures not retrieved here; only the charges and
  guarantees stated in S2/S4 fee tables are cited.
- Equitable prospectus HTML contains inline-XBRL artifacts; extraction was
  cross-checked against surrounding narrative, but table alignment (e.g.,
  which representative charge maps to which rider variant) carries minor
  transcription risk.
