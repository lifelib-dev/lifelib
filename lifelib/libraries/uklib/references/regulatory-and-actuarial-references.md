# Regulatory and Actuarial References — UK Life Insurance

**Status:** Draft, 2026-08-03.

Curated reference library for the UK section of the reference-product library. It
covers the prudential (PRA / Solvency UK), conduct (FCA), legislation-and-tax,
mortality/morbidity (CMI and ONS), professional-standards, and accounting sources that
the reference cash-flow-model implementations (term-assurance / critical-illness /
income-protection / whole-of-life / with-profits / unit-linked-bond / pension-annuity)
rely on. Product folders cite entries on this page as **[REG-R#]** (e.g., `[REG-R1]`);
the R1–R38 numbering below is **frozen** — do not renumber or reuse numbers, as
product documentation cites against it. Within this page, plain `[R#]` refers to the
same entries. Facts drawn from a document that was actually retrieved carry its
number; claims from general knowledge or search-result summaries are tagged
**[unverified]**; failed or unfetched links are disclosed per entry — no URL on this
page is fabricated. All URLs accessed **2026-08-03** unless noted otherwise.

**Regulatory architecture in one line:** the PRA (Bank of England) sets prudential
requirements under the post-Brexit "Solvency UK" regime (Solvency II as onshored,
then reformed in 2023–24 and restated into the PRA Rulebook at end-2024); the FCA
regulates conduct through its Handbook (COBS/ICOBS/PRIN); both act under FSMA 2000.

**Scope note on capital:** the SCR (and MCR) exist under Solvency UK — PS15/24 [R6]
restates the standard formula into the PRA Rulebook — but this library treats the
capital layer as **cited-not-specified**: reference cash flow models produce
best-estimate liability cash flows; SCR aggregation is referenced, never specified.

---

## Product-relevance matrix

`x` = load-bearing per the source bibliography's cross-reference table; `(x)` =
qualified, conditional, or background relevance (a qualification carried from that
table, or a product named only in the entry's own product annotation); blank = not
indicated by the source. Column key: TA = term-assurance, CI = critical-illness,
IP = income-protection, WOL = whole-of-life, WP = with-profits, ULB =
unit-linked-bond, PA = pension-annuity.

| R# | Reference (short name) | term-assurance | critical-illness | income-protection | whole-of-life | with-profits | unit-linked-bond | pension-annuity |
|----|------------------------|----------------|------------------|-------------------|---------------|--------------|------------------|-----------------|
| R1 | PRA Rulebook: Technical Provisions | x | x | x | x | x | x | x |
| R2 | PRA Rulebook: Matching Adjustment | | | (x) | | (x) | | x |
| R3 | PRA Rulebook: TMTP | | | | x | x | | x |
| R4 | Risk Margin Regulations 2023 (SI 2023/1346) | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R5 | PS10/24 — MA reform | | | (x) | | x | | x |
| R6 | PS15/24 — assimilated-law restatement | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R7 | PS2/24 — TMTP simplification | | | | (x) | (x) | | x |
| R8 | SS7/18 — matching adjustment | | | (x) | | (x) | | x |
| R9 | FCA COBS 20 — with-profits | | | | (x) | x | | |
| R10 | FCA COBS 21.3 — permitted links | | | | | | x | |
| R11 | FCA ICOBS | x | x | x | | | | |
| R12 | FCA PRIN 2A — Consumer Duty | x | x | (x) | (x) | x | x | (x) |
| R13 | FSMA 2000 | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R14 | RAO 2001, Sch 1 Pt II (long-term classes) | x | x | x | x | x | x | x |
| R15 | ITTOIA 2005 Pt 4 Ch 9 (chargeable events) | | | | x | x | x | |
| R16 | HMRC IPTM | | | | x | x | x | |
| R17 | Finance Act 2012 Pt 2 (BLAGAB / I-E) | x | x | x | x | x | x | x |
| R18 | HMRC LAM | (x) | (x) | (x) | (x) | x | x | (x) |
| R19 | Insurance Act 2015 | x | (x) | (x) | | | | |
| R20 | CIDRA 2012 | x | x | x | (x) | | | |
| R21 | Taxation of Pensions Act 2014 | | | | | | | x |
| R22 | CMI — role and access model | x | x | x | x | x | x | x |
| R23 | CMI Guide for Authorised Users | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R24 | CMI "92" Series tables | x | | | x | (x) | | (x) |
| R25 | CMI "00" Series tables | x | | | x | | | (x) |
| R26 | CMI "16" Series TA / accelerated CI | x | x | | x | | | |
| R27 | CMI "16" Series PMA16/PFA16 | | | | | | | x |
| R28 | CMI SAPS investigation | | | | | | | x |
| R29 | CMI WP185 — S4 Series | | | | | | | x |
| R30 | CMI_2025 projections model | x | (x) | (x) | x | x | | x |
| R31 | CMI Income Protection investigation | | x | x | | | | |
| R32 | ONS national life tables | x | (x) | (x) | x | (x) | x | x |
| R33 | FRC TAS 100 | x | x | x | x | x | x | x |
| R34 | FRC TAS 200 | x | x | x | x | x | x | x |
| R35 | IFoA APS L1 | (x) | (x) | (x) | (x) | x | (x) | (x) |
| R36 | Proxy modelling validation (BAJ 2024) | (x) | (x) | (x) | (x) | (x) | (x) | x |
| R37 | Model risk: illuminating the black box (BAJ) | (x) | (x) | (x) | (x) | (x) | (x) | (x) |
| R38 | UKEB adoption of IFRS 17 | (x) | (x) | (x) | (x) | (x) | (x) | (x) |

---

## 1. Prudential — PRA / Solvency UK

(uklib-reg-r1)=

### R1. PRA Rulebook — Technical Provisions Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/technical-provisions
- **Accessed:** 2026-08-03
- **Fetched:** yes (read via browser; prarulebook.co.uk blocks plain fetch with HTTP 403)
- **Annotation:** The operative UK rules for valuing insurance liabilities: technical
  provisions equal a best estimate plus a risk margin (rule 2.4); the best estimate is
  the probability-weighted average of future cash flows discounted at the relevant
  risk-free interest rate term structure, on realistic assumptions, gross of
  reinsurance (rule 3.1); the calculation must be market-consistent (rule 2.3), with
  TP set to market value where cash flows are reliably replicable with market
  instruments (rule 2.5) [R1]. The definitions chapter (as amended 31/12/2024) fixes
  the risk-margin cost-of-capital rate at 4% per regulation 7B(b) of the IRPR
  Regulations (R4) and defines the reference-undertaking basis for the notional SCR
  used in the risk margin [R1]. The single most load-bearing prudential source for
  all seven products: it defines exactly what a "best estimate liability" projection
  must produce.

(uklib-reg-r2)=

### R2. PRA Rulebook — Matching Adjustment Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/matching-adjustment
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** New Part created by PS10/24 (R5), effective 30 June 2024 (verified
  from rule date-stamps): a firm may not apply an MA to the risk-free curve for the
  best estimate without an MA permission (rule 2.1) [R2]. Verified definitions
  include the MA attestation ("attestation reference date"), "highly predictable"
  cash flows (MA 5.3), and "eligible element" — which now lets the guaranteed element
  of a with-profits immediate/deferred annuity and the in-payment element of an
  income protection policy into an MA portfolio even when the whole contract does not
  qualify [R2]. Definitions added 27/10/2025 implement the Matching Adjustment
  Investment Accelerator (MAIA permission, per PS17/25 [unverified — PS17/25 itself
  not fetched; its existence confirmed on the SS7/18 page, R8]). For a
  pension-annuity model this Part governs which liabilities may be discounted at
  risk-free + MA.

(uklib-reg-r3)=

### R3. PRA Rulebook — Transitional Measure on Technical Provisions Part
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.prarulebook.co.uk/pra-rules/transitional-measure-on-technical-provisions/31-12-2024
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser, as-at 31/12/2024 view)
- **Annotation:** The streamlined TMTP regime effective 31 December 2024, with
  verified definitions of "base TMTP" and a "dynamic portion" of designated
  obligations (the simplified calculation replaces the legacy Solvency-I-comparison
  approach [unverified as a characterization of the old method]), referencing back to
  INSPRU 7 as at end-2015 for legacy quantities [R3]. Relevant only to legacy WOL /
  WP / PA back-books written before 2016: a reference model needs to know TMTP exists
  (it adjusts technical provisions, not projected cash flows) but does not need to
  implement it. TMTP runs off fully by 2032 [unverified — per search summaries of
  PS2/24, R7].

(uklib-reg-r4)=

### R4. The Insurance and Reinsurance Undertakings (Prudential Requirements) (Risk Margin) Regulations 2023 (SI 2023/1346)
- **Publisher:** legislation.gov.uk (HM Treasury statutory instrument)
- **URL:** https://www.legislation.gov.uk/uksi/2023/1346/made
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The instrument that delivered the Solvency UK risk-margin cut:
  made 7 December 2023, in force 31 December 2023, it changes the cost-of-capital
  rate from 6% to 4% and introduces a risk-tapering factor lambda of 0.9 for life
  business (1.0 for non-life) with a floor of 0.25 [R4]. This pins the risk-margin
  parameters a UK implementation should carry: cost-of-capital method on the
  reference undertaking's notional SCR, 4% CoC, lambda-tapering of projected SCRs for
  life business. Applies to all products, with the largest proportional effect on
  long-duration business (PA, WOL, IP); the risk-margin projection itself requires an
  SCR runoff — cited-not-specified in this library.

(uklib-reg-r5)=

### R5. PS10/24 — Review of Solvency II: Reform of the Matching Adjustment
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/june/review-of-solvency-ii-reform-of-the-matching-adjustment-policy-statement
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; site 403s plain fetch)
- **Annotation:** The instrument of the mid-2024 MA reforms, published 6 June 2024
  (verified): a new Matching Adjustment Part of the Rulebook (R2); amendments to the
  Technical Provisions, Conditions Governing Business and Glossary Parts; updated
  SS7/18 (R8), SS8/18 (internal-model MA modelling), SS3/17, SS1/20, SS11/16; a new
  Statement of Policy on MA permissions; and reporting changes (MA asset & liability
  information return) [R5]. Reform themes verified from the contents: investment
  flexibility (assets with "highly predictable" cash flows), liability-eligibility
  expansion, credit-rating notching, and the new MA attestation regime [R5].
  Implementation 30 June 2024 with some requirements from 31 December 2024
  [unverified — per search summaries]. PA-dominant; WP and IP at the margins via
  liability eligibility.

(uklib-reg-r6)=

### R6. PS15/24 — Review of Solvency II: Restatement of assimilated law
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/november/review-of-solvency-ii-restatement-of-assimilated-law-policy-statement
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** Completes Solvency UK: published 15 November 2024 (verified), it
  restates the revoked Solvency II assimilated law (including the Delegated
  Regulation layer) into PRA rules effective 31 December 2024, with verified chapters
  covering Technical Provisions: Risk Margin; Technical Provisions: Further
  requirements; Own funds; Standard Formula restatement; ring-fenced funds;
  governance; disclosure; and groups [R6]. A 20 December 2024 correction fixed the
  mass-lapse life underwriting risk rule (SCR-SF 3B6.6(1)) (verified note on page).
  For implementers: after 31/12/2024 the place to look for detailed TP requirements
  (contract boundaries, expense treatment, homogeneous risk groups) is the PRA
  Rulebook, not EU delegated regulation [the specific location of contract-boundary
  rules within the restated Parts: unverified].

(uklib-reg-r7)=

### R7. PS2/24 — Review of Solvency II: Adapting to the UK insurance market
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2024/february/review-of-solvency-ii-adapting-to-the-uk-insurance-market-policy-statement
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved this session)
- **Annotation:** Published February 2024 [unverified — date per search summaries];
  finalized the TMTP simplification implemented in R3, internal-model streamlining,
  and third-country branch changes, with an accompanying Statement of Policy
  "Permissions for transitional measures on technical provisions and risk-free
  interest rates" effective 31 December 2024 [unverified]. Cited here as the
  provenance of the R3 regime — the operative rules themselves are in R3. Relevant
  to legacy back-books (WOL, WP, PA).

(uklib-reg-r8)=

### R8. SS7/18 — Solvency II: Matching adjustment (supervisory statement)
- **Publisher:** Prudential Regulation Authority (Bank of England)
- **URL:** https://www.bankofengland.co.uk/prudential-regulation/publication/2018/solvency-2-matching-adjustment-ss
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** The load-bearing supervisory statement on MA practice: first
  published 13 July 2018; current version published 23 October 2025, effective
  27 October 2025, updated for the MAIA following PS17/25 (verified from the page)
  [R8]. Verified scope: asset and liability eligibility assessment, demonstrating
  compliance with the matching conditions (the PRA matching tests appear as
  Appendix 1 [unverified — appendix title seen only in search results]), calculation
  of the MA benefit, ongoing portfolio management and compliance, and MA/MAIA
  applications [R8]. For an annuity cash flow model this is where the PRA's
  expectations on cash-flow matching tests live — it directly shapes how asset and
  liability cash flows are projected and compared; WP/IP via eligible elements.

---

## 2. Conduct — FCA

(uklib-reg-r9)=

### R9. FCA Handbook COBS 20 — With-profits
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/COBS/20/3.html (PPFM section; chapter at /handbook/COBS/20/)
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; COBS 20.2 and 20.3 read directly)
- **Annotation:** The conduct backbone of UK with-profits business. Verified from
  COBS 20.3: a firm must establish and maintain a PPFM (per fund where appropriate),
  retain five years of versions, distinguish enduring "principles" from shorter-term
  "practices", and — per the COBS 20.3.6 table — cover the methods for determining
  amounts payable, the bonus-setting approach, and smoothing of maturity/surrender
  payments; verified from COBS 20.2: fair-treatment rules address
  shareholder-vs-policyholder conflicts and require fair pay-outs on individual
  policies [R9]. A WP cash flow model's bonus/smoothing/estate logic should be
  parameterized the way a PPFM describes these mechanisms. COBS 20.5 covers
  with-profits governance (WP committees) [unverified — section seen only in search
  results].

(uklib-reg-r10)=

### R10. FCA Handbook COBS 21.3 — Further rules for firms engaged in linked long-term insurance business (permitted links)
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/COBS/21/3.html
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser)
- **Annotation:** Verified: applies to linked long-term contracts where the
  investment risk is borne by a natural-person policyholder (COBS 21.3.-1); an
  insurer may only link benefits to an approved index or to the listed categories of
  permitted property — approved/listed securities, permitted unlisted securities,
  permitted land and property, loans, deposits, scheme interests, money-market
  instruments, cash, permitted units, stock lending, derivatives, and conditional
  permitted links (COBS 21.3.1R) — classified by economic substance over legal form
  (21.3.1A) [R10]. For a unit-linked-bond model this constrains the fund universe
  and legitimizes unit-price linkage mechanics. PS20/4 (March 2020) widened the
  regime for illiquid assets [unverified — from search results;
  https://www.fca.org.uk/publication/policy/ps20-04.pdf].

(uklib-reg-r11)=

### R11. FCA Handbook ICOBS — Insurance: Conduct of Business sourcebook
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/ICOBS/1/1.html
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; ICOBS 1.1 read)
- **Annotation:** Verified: ICOBS applies to distribution, effecting and carrying out
  of **non-investment insurance contracts** (ICOBS 1.1.1R) [R11]. Practical split
  for this library: pure protection business (term assurance, standalone CI, IP) is
  conducted under ICOBS, while investment life business (unit-linked bonds,
  with-profits, pensions) falls under COBS; the glossary definition of "pure
  protection contract" and the firm option to apply COBS to protection sales are
  [unverified] details. Modeling impact is indirect (disclosure/cancellation conduct
  rather than cash flows), so one entry suffices.

(uklib-reg-r12)=

### R12. FCA Handbook PRIN 2A — The Consumer Duty
- **Publisher:** Financial Conduct Authority
- **URL:** https://handbook.fca.org.uk/handbook/PRIN/2A/1.html
- **Accessed:** 2026-08-03
- **Fetched:** yes (browser; PRIN 2A.1 read)
- **Annotation:** Verified: the Consumer Duty applies to a firm's retail market
  business, and where it applies, Principles 6 and 7 are disapplied (PRIN 2A.1.3G);
  "product" includes services and "retail customer" includes prospective customers
  [R12]. For modeling, the Duty's price-and-value outcome drives the product-level
  value assessments that actuarial cash flow models increasingly support (e.g.,
  charge levels on ULB, premiums on protection) [the price-and-value outcome
  location PRIN 2A.4: unverified]. Effective for open products from 31 July 2023
  [unverified].

---

## 3. Legislation and tax

(uklib-reg-r13)=

### R13. Financial Services and Markets Act 2000 (c. 8)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2000/8/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The framework statute. Verified: s.19 general prohibition (no
  regulated activity without authorisation or exemption) and Part 4A permissions
  (s.55A ff.); Part 1A establishes the FCA and PRA and their rule-making powers —
  the statutory hook for every Handbook and Rulebook entry above, including the
  s.138BA permissions used for MA/VA (seen in R1/R2 definitions) [R13]. Cite-only
  for modeling purposes.

(uklib-reg-r14)=

### R14. FSMA 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1 Part II
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The legal taxonomy of UK long-term insurance. Verified classes:
  I Life and annuity; II Marriage and birth; III Linked long term; IV Permanent
  health; V Tontines; VI Capital redemption; VII Pension fund management;
  VIII Collective insurance; IX Social insurance [R14]. Maps this library's product
  set onto the legal classes: TA/WOL/WP → Class I (or III if linked), ULB →
  Class III, IP (and long-duration CI riders) → Class IV, PA → Class I annuities.
  Useful for scoping which contracts are "long-term insurance business" for both
  regulatory permissions and tax.

(uklib-reg-r15)=

### R15. Income Tax (Trading and Other Income) Act 2005, Part 4 Chapter 9 — Gains from contracts for life insurance etc.
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2005/5/part/4/chapter/9
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The chargeable-event-gains regime for policyholder taxation.
  Verified: the chapter covers gains on life policies, annuities and capital
  redemption policies; s.498 requires periodic calculations on part
  surrender/assignment and s.507 sets the calculation method; s.500 treats certain
  loans/payments as part surrenders; top-slicing relief sits at ss.535–538 (presence
  confirmed; full text not read) [R15]. Mechanics [brief, unverified as to exact
  statutory expression]: part surrenders within a cumulative 5%-of-premium annual
  allowance are not immediately taxable — excesses over the allowance and gains on
  full surrender/death/maturity are chargeable event gains taxed as savings income,
  with top-slicing spreading relief. Load-bearing for ULB models (also WOL/WP bonds;
  not qualifying protection policies): the 5% withdrawal pattern is a standard
  policyholder-behavior assumption for UK bonds.

(uklib-reg-r16)=

### R16. HMRC Insurance Policyholder Taxation Manual (IPTM)
- **Publisher:** HM Revenue & Customs (GOV.UK)
- **URL:** https://www.gov.uk/hmrc-internal-manuals/insurance-policyholder-taxation-manual
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing/contents)
- **Annotation:** HMRC's working interpretation of R15. Verified: IPTM3000 is the
  chargeable-events section; the manual is the practical reference for the 5%
  allowance arithmetic, insurance years, and top-slicing worked examples [specific
  subsection numbers, e.g. IPTM3500s for part surrenders: unverified]. Secondary
  source — use for mechanics, cite R15 for law.

(uklib-reg-r17)=

### R17. Finance Act 2012, Part 2 — Insurance companies carrying on long-term business
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2012/14/part/2
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The company-level life tax regime. Verified: s.57 defines BLAGAB
  (life assurance business excluding pension business, ISA/CTF business, immediate
  needs annuities, overseas life assurance business, protection business, certain
  reinsurance); s.68 charges corporation tax on the "I-E profit" of BLAGAB (per the
  six-step method in s.73, by reference to amounts credited/debited in the accounts
  per s.70); non-BLAGAB long-term business — notably pension business and post-2012
  protection — is instead taxed on trade profits [R17]. Modeling consequence: for
  BLAGAB products (bonds, WP) policyholder-level tax is effectively borne inside the
  fund, whereas pension and protection business is gross — so a UK cash flow model
  needs a per-product tax-basis flag more than a full tax engine. Basis map:
  ULB/WP/WOL → BLAGAB (I-E); PA and pensions → non-BLAGAB; TA/CI/IP written
  post-2012 → protection business, trade basis.

(uklib-reg-r18)=

### R18. HMRC Life Assurance Manual (LAM)
- **Publisher:** HM Revenue & Customs (GOV.UK)
- **URL:** https://www.gov.uk/hmrc-internal-manuals/life-assurance
- **Accessed:** 2026-08-03
- **Fetched:** yes (landing/contents)
- **Annotation:** HMRC's manual on the FA 2012 regime. Verified structure: LAM01000
  introduction; LAM02000–LAM06000 the I-E calculation components; later sections
  cover reinsurance, cross-border and friendly societies; the I-E basis as enacted
  applies from 1 January 2013 [R18]. Secondary source — use for how HMRC applies
  BLAGAB/I-E, cite R17 for law. Product relevance as R17.

(uklib-reg-r19)=

### R19. Insurance Act 2015 (c. 4)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2015/4/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes (contents)
- **Annotation:** Verified coverage: duty of fair presentation for non-consumer
  insurance (Part 2) with proportionate remedies in Schedule 1 (deliberate/reckless
  vs other breaches), warranties and terms not relevant to actual loss (Part 3),
  remedies for fraudulent claims including group insurance (Part 4), late payment
  (Part 4A), and contracting-out limits [R19]. Commencement August 2016
  [unverified]. Modeling relevance is via claim outcomes — avoidance/proportionate
  reduction affects claim-severity assumptions on group protection (TA/CI/IP group
  schemes) and non-consumer business — background, not a cash flow driver.

(uklib-reg-r20)=

### R20. Consumer Insurance (Disclosure and Representations) Act 2012 (c. 6)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2012/6/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes (contents)
- **Annotation:** Verified: replaces the consumer duty of disclosure with a duty to
  take reasonable care not to make a misrepresentation; Schedule 1 sets graduated
  insurer remedies for qualifying misrepresentations (deliberate/reckless vs
  careless), with specific provisions for group policies and life insurance [R20].
  Underpins underwriting/claims assumptions for consumer protection products
  (declinature and avoidance rates) — TA, CI, IP, and WOL consumer sales.

(uklib-reg-r21)=

### R21. Taxation of Pensions Act 2014 (c. 30)
- **Publisher:** legislation.gov.uk
- **URL:** https://www.legislation.gov.uk/ukpga/2014/30/contents
- **Accessed:** 2026-08-03
- **Fetched:** yes (contents)
- **Annotation:** The "pension freedoms" Act, effective 6 April 2015 (verified).
  Verified changes: flexi-access drawdown, uncrystallised funds pension lump sums
  (UFPLS), relaxed annuity design restrictions, reformed death-benefit taxation, and
  the money-purchase annual allowance mechanics [R21]. Modeling relevance: it
  reshaped the UK annuity market (annuitization is now optional), which drives
  take-up, anti-selection and mortality-basis assumptions for pension-annuity models
  and lapse/transfer behavior in the pension wrappers feeding them.

---

## 4. Mortality and morbidity — CMI and ONS

(uklib-reg-r22)=

### R22. Continuous Mortality Investigation — main page (role and access model)
- **Publisher:** Institute and Faculty of Actuaries / CMI Ltd
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: the CMI researches mortality and morbidity experience
  from data supplied by UK life offices and consultancies and runs five
  investigations — annuities, assurances (mortality and critical illness), income
  protection, SAPS (pension scheme) mortality, and mortality projections [R22].
  Access model, stated honestly: the CMI is funded by subscriptions; current tables
  and the Projections Model are restricted to Authorised Users (subscribers, plus
  academics/researchers for non-commercial use), while older publications and
  working-paper texts are freely available [R22]. A reference implementation
  therefore documents table *names and structure* from public sources but cannot
  redistribute current qx values — model mortality bases should be [std]
  placeholders shaped like the named tables.

(uklib-reg-r23)=

### R23. CMI Guide for Authorised Users (2026)
- **Publisher:** Institute and Faculty of Actuaries / CMI Ltd
- **URL:** https://www.actuaries.org.uk/system/files/field/document/CMI%20Guide%20for%20Authorised%20Users%202026_0.pdf
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved)
- **Annotation:** The CMI's own guide to who counts as an Authorised User and how
  outputs are accessed [unverified beyond title/existence]. Cited as the canonical
  statement of the access regime summarized in R22.

(uklib-reg-r24)=

### R24. CMI "92" Series tables (AM92/AF92 family)
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/92-series-tables
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified table names: assured lives AM92 (males) and AF92
  (females); immediate annuitants IML92/IMA92, IFL92/IFA92; retirement annuitants
  RMV92/RFV92; pensioners PML92/PMA92, PFL92/PFA92; complete set published 30 June
  1999 [R24]. Base experience 1991–94 [unverified]. AM92/AF92 remain the canonical
  *teaching* assured-lives tables (IFoA Formulae and Tables) and the natural
  public-domain-adjacent shape for [std] protection-mortality placeholders, though
  modern pricing uses the "16" Series (R26); the annuitant tables are historical
  context for PA.

(uklib-reg-r25)=

### R25. CMI "00" Series tables
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-mortality-and-morbidity-tables/00-series-tables
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified families: permanent assurances AMC00/AMS00/AMN00 and
  AFC00/AFS00/AFN00 (combined/smoker/non-smoker); temporary assurances
  TMC00/TMS00/TMN00, TFC00/TFS00/TFN00; annuitants IML00/IFL00 (immediate),
  RMD00/RMV00/RMC00 and female equivalents (retirement), PPMD00/PPMV00 etc.
  (personal pensioners); pensioners PNMA00/PNFA00 (normal), PEMA00 etc. (early),
  PCMA00/PCFA00 (combined), widows WA00/WL00 [R25]. Base experience 1999–2002
  [unverified]. Shows the naming grammar (product/sex/smoker/select) a UK model's
  mortality-basis interface should mirror; the smoker/non-smoker split first matters
  here for protection pricing.

(uklib-reg-r26)=

### R26. CMI "16" Series term assurance mortality and accelerated critical illness tables (IFoA blog announcement)
- **Publisher:** Institute and Faculty of Actuaries (blog; tables by CMI Assurances Committee)
- **URL:** https://blog.actuaries.org.uk/cmi-new-16-series-term-assurance-mortality-and-accelerated-critical-illness-tables/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: the "16" Series covers term-assurance mortality
  (including terminal illness) and accelerated critical illness, based on 2015–2018
  experience; proposed with Working Paper 150, finalized with Working Paper 154
  (August 2021); WP151 analyzed CI claims by cause and WP152 covered 2019/2020
  experience; the CMI cautions against mechanical application (sum-assured
  differentials, COVID-19) [R26]. Table names in the family include TMNL16/TFNL16
  [unverified — from search summaries, not the fetched blog]. This is the current
  protection base-table family: a UK term/CI reference model should name-check the
  16 Series and use [std] placeholder rates in its shape (smoker status, select
  period); WOL indirectly.

(uklib-reg-r27)=

### R27. CMI briefing note — final "16" Series pension annuity in payment mortality tables
- **Publisher:** Institute and Faculty of Actuaries / CMI Annuities Committee
- **URL:** https://www.actuaries.org.uk/documents/final-16-series-pension-annuitant-mortality-tables-briefing-note-v01-2020-07-10
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: the "16" Series pension annuity in payment tables
  (PMA16/PFA16) are based on 2015–2018 experience of insured pension annuities — the
  current annuitant base-table family, superseding the "00" and "08" Series lineages
  [the "08" Series interim datasets (e.g. WP101, 2011–2014 data): unverified, from
  search summaries]. A pension-annuity model's base mortality should be expressed
  as a percentage of a named PMA/PFA-style table with a projection overlay (R30).

(uklib-reg-r28)=

### R28. CMI Self-Administered Pension Schemes (SAPS) mortality investigation
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/self-administered-pension-scheme-saps-mortality-investigation
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified series history: S1 (October 2008), S2 (February 2014),
  S3 (December 2018), and the current S4 Series released February 2024 alongside
  Working Paper 185; the latest experience analysis (WP209) covers 2017–2024 on data
  to September 2025 [R28]. S4 tables have an effective date of 1 January 2017 and
  are graduated on 2014–2019 data, deliberately excluding pandemic years
  [unverified — per search summaries of WP181]. SAPS tables are the pension-scheme
  (bulk annuity / DB) counterpart to the insured-annuitant PMA/PFA families and
  include amounts-based and socio-economic variants [unverified]; most relevant to
  bulk purchase annuities / buy-ins.

(uklib-reg-r29)=

### R29. CMI Working Paper 185 — final "S4" Series mortality tables
- **Publisher:** Institute and Faculty of Actuaries / CMI SAPS Committee
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-working-papers/self-administered-pension-scheme-mortality/cmi-working-paper-185
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved)
- **Annotation:** The release document for the S4 Series (February 2024), read
  together with consultation WP181 [unverified beyond existence/dates from R28 and
  search results]. Cited as the primary anchor for S4; the tables themselves are
  Authorised-User-restricted (R22).

(uklib-reg-r30)=

### R30. CMI Mortality Projections Model CMI_2025 (announcement, with Working Paper 211)
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://actuaries.org.uk/news-and-media-releases/news-articles/2026/mar/10-mar-26-cmi-model-shows-further-rise-in-cohort-life-expectancy/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: CMI_2025, the current version of the Mortality
  Projections Model, was published in March 2026 with Working Paper 211, calibrated
  to England & Wales population mortality data to 31 December 2025; methodology
  carried over from the restructured CMI_2024 (published June 2025 with WP201, which
  added age/period terms); cohort life expectancy at 65 rose ~8 weeks (M) /
  ~6 weeks (F) vs CMI_2024, and 2025 all-age mortality was a record low, about 2%
  below 2024 [R30]. The model is subscriber-restricted; users are expected to
  adjust core parameters (e.g. the long-term rate, which has no default
  recommendation [unverified]) to their portfolio. Any UK projection basis in this
  library should be expressed as "CMI_20xx with long-term rate p% [std]" — PA
  dominant, also WOL/WP and TA/CI/IP improvement bases.

(uklib-reg-r31)=

### R31. CMI Income Protection investigation
- **Publisher:** Institute and Faculty of Actuaries / CMI
- **URL:** https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation/cmi-investigations/income-protection-investigation
- **Accessed:** 2026-08-03
- **Fetched:** no (URL from search results; not retrieved)
- **Annotation:** The CMI's morbidity investigation for individual income
  protection: experience is analyzed as claim inceptions and claim terminations
  (recoveries and deaths) — the structure a multi-state IP cash flow model must
  mirror; current methodology per WP59, with recent experience in WP193 (2017–2020)
  and WP203 (2021–2023) [all unverified — from search-result summaries]. The
  critical-illness counterpart lives in the assurances investigation (R26). Historic
  standard bases (e.g. CMIR12 sickness rates) remain the public teaching reference
  [unverified].

(uklib-reg-r32)=

### R32. ONS National life tables (UK series)
- **Publisher:** Office for National Statistics
- **URL:** https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/lifeexpectancies/bulletins/nationallifetablesunitedkingdom/2021to2023
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** The fully public mortality reference. Verified from the fetched
  bulletin: period life tables on three consecutive years of data (2021–2023 release
  published 23 October 2024 covering England & Wales, with UK-level figures
  following — the UK 2021–2023 tables were published 18 March 2025 [unverified, from
  search results]); life expectancy at birth 83.0 (F) / 79.1 (M); datasets
  (including qx by single year of age and sex) are freely downloadable under the
  Open Government Licence [R32]. Because CMI tables are restricted (R22), ONS
  tables are the only redistributable UK mortality source — suitable for [std]
  placeholder bases in reference models, with the caveat that population mortality
  is heavier than insured/annuitant experience.

---

## 5. Professional standards

(uklib-reg-r33)=

### R33. FRC Technical Actuarial Standard TAS 100: General Actuarial Standards, v2.0
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- **Accessed:** 2026-08-03
- **Fetched:** yes (standard's FRC page; PDF not read)
- **Annotation:** Verified: v2.0 published 3 March 2023, effective 1 July 2023;
  contains the requirements applying to *all* technical actuarial work, with
  supporting guidance including on Principle 5 (Models) and proportionate
  application [R33]. For this library, TAS 100 is the quality bar a reference cash
  flow model's documentation should meet: justified assumptions, data limitations
  stated, models fit for purpose and communicated with their limitations
  [principle-level detail beyond Principle 5: unverified].

(uklib-reg-r34)=

### R34. FRC Technical Actuarial Standard TAS 200: Insurance, v2.0
- **Publisher:** Financial Reporting Council
- **URL:** https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-200/
- **Accessed:** 2026-08-03
- **Fetched:** yes (standard's FRC page; PDF not read)
- **Annotation:** Verified: v2.0 published 20 September 2024, effective 1 January
  2025; contains the requirements for technical actuarial work in insurance [R34].
  The 2024 revision reflects Consumer Duty implications, insurance transformations,
  audit and assumption-setting, and removes provisions now covered by TAS 100
  [unverified — from FRC/IFoA announcement summaries]. Directly in scope for anyone
  using these reference models for actual reserving or capital work in the UK.

(uklib-reg-r35)=

### R35. IFoA APS L1: Duties and Responsibilities of Life Assurance Actuaries, v4.0
- **Publisher:** Institute and Faculty of Actuaries
- **URL:** https://actuaries.org.uk/media/04ujhlcm/aps-l1-version-4-0.pdf
- **Accessed:** 2026-08-03
- **Fetched:** yes (PDF downloaded and read)
- **Annotation:** Verified from the document: version 4.0, effective 2 April 2024;
  sets requirements for Members acting as Chief Actuary (long-term business,
  Solvency II firms), Small Insurer Chief Actuary, With-Profits Actuary, and
  Appropriate Actuary (non-Solvency II firms), including predecessor-discussion and
  standpoint-disclosure obligations and the duty to disclose departures from
  generally accepted actuarial practice [R35]. Explains *who* professionally owns
  the with-profits discretion (R9) and the actuarial-function outputs a cash flow
  model feeds — all products, WP especially.

(uklib-reg-r36)=

### R36. Proxy Modelling Working Party — "Consideration of the proxy modelling validation framework"
- **Publisher:** British Actuarial Journal (Cambridge University Press), Vol. 29, 2024
- **URL:** https://www.cambridge.org/core/journals/british-actuarial-journal/article/consideration-of-the-proxy-modelling-validation-framework/B499011B84ACEC53C627C15765D33F4B
- **Accessed:** 2026-08-03
- **Fetched:** yes (abstract/landing)
- **Annotation:** Verified: Wollam, Kuona, Thomson, Liu, Paton and the IFoA Proxy
  Model Working Group; BAJ vol. 29 (2024). Covers calibration (OLS, automated
  selection, penalized regression), scenario selection, eleven validation tests and
  roll-forward practice for the proxy models UK life insurers fit to their "heavy"
  cash flow models, informed by the PRA's 2019 thematic review, with an
  annuity-portfolio case study [R36]. Directly load-bearing here: it defines the
  relationship between a full liability cash flow model (what this library
  specifies) and the proxy layer built on top of it — and thus what outputs the
  heavy model must expose.

(uklib-reg-r37)=

### R37. Model Risk Working Party — "Model risk: illuminating the black box"
- **Publisher:** British Actuarial Journal (Cambridge University Press), Vol. 23, 2017/18
- **URL:** https://www.cambridge.org/core/journals/british-actuarial-journal/article/model-risk-illuminating-the-black-box/FD2FD9F9DD86CCB611B4ECEF1421A7AA
- **Accessed:** 2026-08-03
- **Fetched:** yes (abstract/landing)
- **Annotation:** Verified: Black, Tsanakas, Smith et al. (IFoA Model Risk Working
  Party), BAJ vol. 23 (published online 2017). A practical model-risk-management
  framework — governance, model inventory and materiality filtering, risk appetite,
  mitigation and communication — with case studies [R37]. The professional frame
  for documenting model limitations and validating liability cash flow models
  (complements TAS 100 Principle 5, R33).

---

## 6. Accounting frames — why one cash flow model serves several bases

(uklib-reg-r38)=

### R38. UK Endorsement Board — IFRS 17 Insurance Contracts (UK adoption)
- **Publisher:** UK Endorsement Board
- **URL:** https://www.endorsement-board.uk/projects/ifrs-17-insurance-contracts/
- **Accessed:** 2026-08-03
- **Fetched:** yes
- **Annotation:** Verified: IFRS 17 (as issued May 2017 and amended June 2020 and
  December 2021) was adopted for UK use on 16 May 2022, effective 1 January 2023,
  replacing IFRS 4; the UKEB committed to a post-implementation review reporting by
  1 January 2028 [R38]. UK-listed and other IFRS-reporting life insurers therefore
  account for all the products in this library under UK-adopted IFRS 17.

### The three measurement bases one projection feeds

**IFRS 17 (UK-adopted).** IFRS 17 measures insurance contracts as fulfilment cash
flows (probability-weighted expected cash flows, discounted, plus an explicit risk
adjustment) plus a contractual service margin releasing profit over coverage, with
the variable fee approach for direct-participation business such as unit-linked and
with-profits [mechanics: unverified — general knowledge; standard text not fetched;
adoption facts per R38]. The expected-cash-flow engine is the same projection a
Solvency UK best estimate needs — differences are in discount rates, risk adjustment
vs risk margin, aggregation (groups/cohorts) and the CSM layer, not in the
underlying per-policy cash flows.

**Solvency UK.** The regulatory balance sheet values liabilities as best estimate
[R1] plus risk margin [R4], discounted at PRA-published risk-free curves, with MA
[R2] for eligible annuity-style business — again the same projected premiums,
claims, expenses and options/guarantees cash flows, with regime-specific
discounting and margins. SCR/MCR capital layers consume the same projections but
are cited-not-specified in this library [R6].

**Tax.** The tax result is computed from statutory accounts with the FA 2012
overlay [R17]: I-E for BLAGAB, trade profit for pension and protection business,
plus policyholder-level chargeable event effects [R15] that shape lapse/withdrawal
behavior. A tax projection is therefore a *consumer* of the same cash flow model
output (income, gains, expenses by fund/business line) rather than a separate
model — which is why the reference implementations keep product cash flows
basis-agnostic and apply basis layers (discounting, margins, tax) as configuration.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-reg-r1
[R10]: #uklib-reg-r10
[R11]: #uklib-reg-r11
[R12]: #uklib-reg-r12
[R13]: #uklib-reg-r13
[R14]: #uklib-reg-r14
[R15]: #uklib-reg-r15
[R17]: #uklib-reg-r17
[R18]: #uklib-reg-r18
[R19]: #uklib-reg-r19
[R2]: #uklib-reg-r2
[R20]: #uklib-reg-r20
[R21]: #uklib-reg-r21
[R22]: #uklib-reg-r22
[R24]: #uklib-reg-r24
[R25]: #uklib-reg-r25
[R26]: #uklib-reg-r26
[R28]: #uklib-reg-r28
[R3]: #uklib-reg-r3
[R30]: #uklib-reg-r30
[R32]: #uklib-reg-r32
[R33]: #uklib-reg-r33
[R34]: #uklib-reg-r34
[R35]: #uklib-reg-r35
[R36]: #uklib-reg-r36
[R37]: #uklib-reg-r37
[R38]: #uklib-reg-r38
[R4]: #uklib-reg-r4
[R5]: #uklib-reg-r5
[R6]: #uklib-reg-r6
[R8]: #uklib-reg-r8
[R9]: #uklib-reg-r9
[std]: #uklib-std
[unverified]: #uklib-unverified
<!-- END generated citation links -->
