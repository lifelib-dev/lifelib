# Unit-Linked Investment Bond (onshore single-premium life assurance bond) — research notes (UK)

Research for a reference liability cash-flow projection model (lifelib/modelx style). All facts are tagged
[S#] (primary product documents) or [R#] (regulatory/actuarial references) pointing at documents actually
fetched and read. Statements from general knowledge that could not be verified against a retrieved document
are tagged [unverified]. access date: 2026-08-03.

---

## Primary sources

### S1 — Prudential (M&G plc): "Key Features of the Prudential Investment Plan"
- Publisher: The Prudential Assurance Company Limited ("Pru, part of M&G plc"), reg. no. 15454, FCA ref 139793
- Doc type: Key Features Document (KFD). Doc code PIPK10011 10/2025_WEB
- URL: https://www.mandg.com/dam/pru/shared/documents/en/pipk10011.pdf
- Retrieved: YES (full PDF read, 16 pp)
- Currently marketed single-premium onshore investment bond. Detailed facts extracted below.

### S2 — Prudential (M&G plc): "Policy Provisions — Prudential Investment Plan"
- Publisher: The Prudential Assurance Company Limited
- Doc type: Policy conditions (full contract terms). Doc code INVM11630 11/2025_WEB
- URL: https://www.mandg.com/dam/pru/shared/documents/en/invm11630.pdf
- Retrieved: YES (full PDF read, 40 pp — definitions, unit pricing, charges, withdrawals, death benefit,
  PruFund smoothing, adviser charging, guarantee mechanics)

### S3 — Aviva: "Investment and Trustee Bond Plan Booklet — The details of your Investment Bond"
- Publisher: Aviva Life & Pensions UK Limited, reg. no. 3253947, FCA firm ref 185896
- Doc type: Policy conditions / plan booklet (full plan terms; covers Investment Bond and Trustee Bond).
  Doc code AIBPO HL59005 05/2023
- URL: https://static.aviva.io/content/dam/document-library/adviser/ecm/hl59005c.pdf
- Retrieved: YES (full PDF read, 15 pp). Note: static.aviva.io returns HTTP 403 to plain fetchers; retrieved
  with a browser user-agent. This booklet documents the pre-platform Aviva bond (with legacy features:
  bid-offer "One-Off Charge", Early Cash-in Charges, Establishment Charge, with-profits funds, MVR).

### S4 — Aviva: "Onshore Bond Key Features" (Aviva Wealth platform)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: Key Features Document. Doc code LF20017 06/2026 (companion T&Cs are LF30029)
- URL: https://static.aviva.io/content/dam/document-library/adviser/general/lf20017c.pdf
- Retrieved: YES (full PDF read, 8 pp). This is Aviva's current adviser-platform onshore bond — the modern
  "clean" open-architecture design.

### S5 — Quilter: "Key Features of the Collective Investment Bond"
- Publisher: Quilter Life & Pensions Limited, reg. no. 04163431, PRA/FCA ref 207977
- Doc type: Key Features Document. Doc code QIP 18193/205/14009, approved May 2026
- URL: https://www.quilter.com/siteassets/documents/platform/kfd/18193_cib_kfd.pdf
- Retrieved: YES (full PDF read, 16 pp). Current platform onshore bond (open architecture, ~3,000 funds).

### S6 — Quilter: "Terms and Conditions for the Collective Investment Bond"
- Publisher: Quilter Life & Pensions Limited
- Doc type: Policy conditions
- URL: https://www.quilter.com/siteassets/documents/platform/terms/19093_cib-cb1-2-terms.pdf
- Retrieved: PARTIAL — PDF downloaded successfully (valid PDF) but its content was NOT parsed/read in this
  session. No facts below are cited from it. Listed as a confirmed-existing companion document to S5.

### S7 — Canada Life: "Canada Life announces closure of onshore bond and personal pension to focus investment on offshore bonds"
- Publisher: Canada Life UK (canadalife.co.uk)
- Doc type: Other (news announcement; market-context evidence)
- URL: https://www.canadalife.co.uk/news/canada-life-announces-closure-of-onshore-bond-and-personal-pension-to-focus-investment-on-offshore-bonds/
- Retrieved: YES. The Select Account (onshore bond) closed to new business with immediate effect on
  23 January 2024; no change for existing customers ("all product features currently available continuing");
  the closed products represented less than 1% of the customer base; Canada Life is concentrating on the
  offshore bond market via its Isle of Man and Dublin operations.

### S8 — Aviva: "Key features of the Aviva Investment Bond" (legacy)
- Publisher: Aviva Life & Pensions UK Limited
- Doc type: Key Features Document (companion to S3). Doc code HL59015
- URL: https://static.aviva.io/content/dam/document-library/adviser/ecm/hl59015c.pdf
- Retrieved: PARTIAL — PDF downloaded (valid file) but NOT read in this session; no facts cited from it.

---

## Regulatory and actuarial references

### R1 — ITTOIA 2005, Part 4 Chapter 9: "Gains from contracts for life insurance etc."
- Publisher: legislation.gov.uk (UK statute)
- URL: https://www.legislation.gov.uk/ukpga/2005/5/part/4/chapter/9
- Retrieved: YES (chapter structure and key sections). The chargeable-event regime governing bond taxation:
  - s461 et seq. charge to income tax on gains; s465 person liable (UK-resident individuals), s466 personal
    representatives, s467 UK-resident trustees.
  - s484 "When chargeable events occur" — surrender of all rights, assignment for consideration, death
    (giving rise to benefits), maturity, and part surrender/part assignment excess events via s509/s514.
  - s491 "Calculating gains: general rules" — gain = TB (total benefit value) − (TD total allowable
    deductions + PG previous gains); s492 total benefit value; s494 total allowable deductions.
  - s498 requirement for periodic calculations for part surrenders/assignments (end of insurance year);
    s500 events treated as part surrenders; s507 method for periodic calculations (the "5% rule" machinery).
  - s535–s537 top-slicing relief; s539 deficiency relief.

### R2 — HMRC Insurance Policyholder Taxation Manual IPTM3560
- Publisher: GOV.UK (HMRC internal manual)
- Title: "IPTM3560 — Calculating gains: part surrenders and part assignments: 'periodic calculations' and
  'excess events': calculation method"
- URL: https://www.gov.uk/hmrc-internal-manuals/insurance-policyholder-taxation-manual/iptm3560
- Retrieved: YES. Mechanics: at each insurance year end a periodic calculation compares the net total value
  of rights surrendered/assigned with the net total allowable payments. Allowable element of each premium =
  premium × y/20, where y = number of insurance years (capped at 20) from payment year to calculation year —
  i.e. 5% of premium per insurance year, cumulative, with the full premium allowable after 20 years. A gain
  ("excess event") arises only when cumulative withdrawals exceed the cumulative allowable element.

### R3 — FCA Handbook COBS 21.3: "Further rules for firms engaged in linked long-term insurance business"
- Publisher: FCA (handbook.fca.org.uk)
- URL: https://www.handbook.fca.org.uk/handbook/COBS/21/3.html
- Retrieved: YES (rendered via browser; the site is JavaScript-only). Key rules:
  - COBS 21.3.-1R: the section applies to linked long-term contracts where the investment risk is borne by a
    policyholder who is a natural person.
  - COBS 21.3.1R: an insurer must not contract to provide benefits determined by reference to an index other
    than an approved index, or by reference to property other than the permitted-links list: (a) approved
    securities; (b) listed securities; (c) permitted unlisted securities; (d) permitted land and property;
    (e) permitted loans; (f) permitted deposits; (g) permitted scheme interests; (h) approved money market
    instruments (COBS 21.3.6R–21.3.8G); (i) cash; (j) permitted units; (k) permitted stock lending;
    (l) permitted derivatives contracts; (m) conditional permitted links.
  - COBS 21.3.1AR: classify property by economic behaviour ahead of legal form.
  - COBS 21.3.2G: CPI and RPI are approved indices; notional tax loss allowance permitted in fair pricing.
  - COBS 21.3.9R–21.3.12R stock lending conditions (collateral adequacy etc.); 21.3.13R–21.3.14G permitted
    derivatives (regulated market or off-market with approved counterparty; adequately covered).
  - COBS 21.3.15R–21.3.16R conditional permitted links (incl. conditional permitted long-term asset funds,
    illiquids for qualifying-scheme default arrangements) with policyholder-access conditions.

### R4 — FSMA 2000 (Regulated Activities) Order 2001 (SI 2001/544), Schedule 1 Part II
- Publisher: legislation.gov.uk
- URL: https://www.legislation.gov.uk/uksi/2001/544/schedule/1
- Retrieved: YES. Contracts of long-term insurance classes. Class I "Life and annuity": contracts of
  insurance on human life ... excluding contracts within paragraph III. Class III "Linked long-term":
  "Contracts of insurance on human life or contracts to pay annuities on human life where the benefits are
  wholly or partly to be determined by reference to the value of, or the income from, property of any
  description (whether or not specified in the contracts) or by reference to fluctuations in, or in an index
  of, the value of property of any description (whether or not so specified)." The unit-linked bond is a
  Class III contract; the Prudential provisions confirm the plan is a "contract of long-term insurance"
  within the meaning of the RAO [S2 provision 18.5].

### R5 — PRA Rulebook (Solvency II firms): Technical Provisions Part
- Publisher: Bank of England / PRA (prarulebook.co.uk)
- URL: https://www.prarulebook.co.uk/pra-rules/technical-provisions
- Retrieved: YES (page HTML downloaded and text-extracted; viewed as at 03/08/2026). Key rules (post-reform
  "Solvency UK" state):
  - TP 2.1: firms must establish adequate technical provisions for all insurance obligations.
  - TP 2.2: value = current transfer amount to another UK Solvency II firm.
  - TP 2.3: market-consistent, prudent, reliable, objective.
  - TP 2.4: technical provisions = best estimate + risk margin; TP 2.5 valued separately unless cash flows
    can be replicated by financial instruments.
  - TP 3.1: best estimate = probability-weighted average of future cash flows, discounted at the relevant
    risk-free interest rate term structure, gross of reinsurance; TP 3.2: cash-flow projection must take
    into account ALL cash in- and out-flows required to settle the obligations over their lifetime.
  - TP 4A.1 (Solvency UK reformed risk margin): RM = CoC · Σ_{t≥0} SCR(t)·max(λ^t, λ_floor)/(1+r(t+1))^{t+1}
    with cost-of-capital rate CoC = 4% (per regulation 7B(b) of the IRPR Regulations, defined in TP 1.2),
    risk-tapering factor λ = 0.9 for long-term insurance obligations (1.0 for general), floor λ_floor = 0.25.
    (This is the reformed, post-2023/24 UK risk margin — reduced from the EU 6% CoC design; related policy
    statements PS10/24 and PS15/24 "Review of Solvency II" are linked from the Part.)

### R6 — HMRC Life Assurance Manual LAM01160 (I-E / BLAGAB)
- Publisher: GOV.UK (HMRC internal manual)
- Title: "LAM01160 — ... key concepts: simplified example of the I-E calculation"
- URL: https://www.gov.uk/hmrc-internal-manuals/life-assurance/lam01160
- Retrieved: YES. BLAGAB (basic life assurance and general annuity business — the category containing
  onshore bonds) is taxed so that the company pays tax on both shareholder profit and policyholder
  investment return. The I-E base = investment income and chargeable gains allocated to BLAGAB minus
  expenses. Two rates apply: the normal corporation tax rate on the slice equal to adjusted BLAGAB trade
  profit, and the policyholder rate (basic rate of income tax, 20% in the example) on the remainder;
  policyholders receive returns net of basic-rate credit. A minimum profits test ensures I-E profit is at
  least the BLAGAB trade profit. This is why onshore bond gains carry a basic-rate tax credit in the
  policyholder chargeable-event computation [R6; consistent with S4, S5 product statements].

### R7 — FRC: TAS 100 "General Technical Actuarial Standards"
- Publisher: Financial Reporting Council (frc.org.uk)
- URL: https://www.frc.org.uk/library/standards-codes-policy/actuarial/tas-100/
- Retrieved: YES. TAS 100 version 2.0, published 3 March 2023, effective 1 July 2023; applies to all
  technical actuarial work in geographic scope and must be applied by all IFoA members. Principle 5 covers
  Models; supporting Technical Actuarial Guidance: Models (Oct 2024), Proportionality (Oct 2025),
  Technical Actuarial Work and Geographic Scope (Mar 2023). (TAS 200: Insurance was not verified from a
  fetched document in this session — see Gaps.)

### R8 — IFoA: Continuous Mortality Investigation page
- Publisher: Institute and Faculty of Actuaries (actuaries.org.uk)
- URL: https://www.actuaries.org.uk/learn-and-develop/continuous-mortality-investigation
- Retrieved: YES. The CMI carries out research into mortality and morbidity experience and produces
  practical tools widely used by actuaries; investigations cover annuitant mortality, critical illness /
  assurance mortality, income protection and self-administered pension scheme mortality; it produces
  mortality/morbidity tables, mortality projections, working papers. The CMI is funded by subscriptions and
  subscribers have access to all outputs (i.e., full tables/data are restricted to authorised users);
  historical publications are freely available; contact info@cmilimited.co.uk (CMI Limited operates on
  behalf of the IFoA). Specific table series names were not stated on the fetched page — see Gaps.

### R9 — IFoA historical sessional papers on unit-linked reserving
- Publisher: Institute and Faculty of Actuaries (actuaries.org.uk document archive)
- Example URLs: https://www.actuaries.org.uk/documents/category-b-unit-linked-policies (A. F. Wilson,
  "Category B unit-linked policies"); https://www.actuaries.org.uk/system/files/documents/pdf/0311-0367.pdf
- Retrieved: NO (fetched_ok = false). The archive PDFs are scanned images; text could not be extracted.
  Listed as known references for the unit vs non-unit ("sterling") reserve decomposition. The decomposition
  itself is therefore tagged [unverified] where used below.

---

## Extracted specifications

### 1. Product architecture and legal form
- Single-premium ("lump sum") unit-linked whole-of-life assurance bond; no fixed term or maturity date;
  designed to be held 5–10 years or more [S1 "About the Prudential Investment Plan", "Cashing in your plan";
  S5 "Keeping in touch" — hold at least six years; S4 "Your commitment" — five years or longer].
- The contract is a "contract of long-term insurance" within the meaning of the FSMA 2000 (Regulated
  Activities) Order 2001 [S2 §18.5]; the linked benefit design places it in RAO Class III "Linked
  long-term" [R4].
- Units are purely notional records of benefit entitlement: "You do not 'own' the Units: they are just a
  record of the benefits due to You" [S2 §3.1.5]; "Units in the Fund are used by us purely to work out what
  benefits should be paid to you. You will not own or have an interest in the Assets of a Fund" [S3 Part D];
  Quilter "remains the legal and beneficial owner of your chosen funds" [S5 Q1].
- Insurer's liability is capped at the value derived from the assets underpinning each fund — no
  make-whole if an external fund manager defaults [S2 §3.1.9; S4 Compensation; S1 "Other information"].
- Governing law: England (and Wales) in all four product sets [S1, S2 §18.4, S3 Part A, S4 Law, S5].

### 2. Eligibility and issue ages
- Prudential Investment Plan: plan owner must be over 18 and UK resident; lives assured min age 3 months,
  max age at outset 85 next birthday; owner can be the life assured or assure another's life; single or
  joint life; trusts possible [S1 "Is the PIP right for me?"]. Top-ups blocked if no longer UK-resident
  (crown servant exception) [S1 "What happens if I move abroad?"].
- Aviva Investment Bond (legacy): extra payments allowed while younger life assured is not over 84
  (Investment Bond); Trustee Bond: 79 (Five Year Plus) / 74 (Ten Year Plus options) [S3 "Extra payment
  option"].
- Aviva Onshore Bond (platform): up to 10 lives assured; max age of a life assured 89; no minimum age
  [S4 "What is the Onshore Bond?"].
- Quilter CIB: investor must be UK-resident individual aged 18–90 attained, or a company or trust; Capital
  Protected Death Benefit option not available if any life assured is over 90 at outset [S5 Q3, Aims].

### 3. Premiums (single premium with top-ups)
- Prudential: minimum initial £10,000 after any adviser set-up charge; each additional investment min
  £10,000; general maximum £5 million (more by referral); overall aggregate plan limit and per-fund
  min/max limits reserved; separate aggregate cap on with-profits investment [S1 "How much can I pay in?";
  S2 §2.2, §2.3].
- Aviva platform Onshore Bond: minimum £10,000 initial; additional payments min £1,000 at any time; no
  overall maximum except £1m normal limit into Smooth Managed funds [S4 "How do I invest?"].
- Quilter CIB: minimum initial £10,000; additional payments any time [S5 Your commitment, Q6].
- Aviva legacy bond: extra payment option at any time subject to terms/age limits [S3 "Extra payment option"].
- "Premium" = payment minus any set-up adviser charge; withdrawal limits and the 5% tax-deferred allowance
  are based on premiums so defined [S1 "Set up adviser charge"; S2 §1 "Premium", §12.2].

### 4. Lives assured structure and death benefit
- Single life or joint lives; the plan/bond ends on death of the (sole) life assured or the LAST survivor of
  joint/multiple lives ("last death" basis) [S1 "What happens ... if the person covered dies?"; S2 §9.2;
  S3 "Event (death)"; S4 "What happens when the lives assured die?"; S5 Q1, Q17]. Aviva platform allows up
  to 10 lives assured [S4].
- Life-of-another permitted (owner need not be a life assured); if an owner who is not a life assured dies,
  the plan continues and ownership passes to the estate / surviving joint owner [S1; S5 Q17].
- Death benefit (the "small amount of life cover"):
  - Prudential: Sum Assured = 100.1% of the bid value of units; units valued on the working day notice of
    death is received (12:00 cut-off), but the NUMBER of units cancelled is the number in credit at the
    date of death adjusted for post-death transactions; adviser charges paid between death and processing
    are reclaimed and included in the claim [S1; S2 "Sum Assured" definition, §4.2.7, §9].
  - Aviva legacy Investment Bond: 100.1% of plan value (101% for plans started before 3 August 2006);
    Trustee Bond: greater of (net invested premiums less withdrawals) and 101% of bond value (capital
    guarantee) [S3 "Benefit payable on death"].
  - Aviva legacy Accidental Death Benefit: 110% of bond value if death within 90 days of an accident
    (plans started on/after 12 Dec 2005); exclusions: (A) self-inflicted injury / drugs / alcohol /
    criminal act, (B) war, riot and civil commotion, (C) aviation other than as fare-paying passenger on a
    licensed commercial airline [S3 "Accidental Death Benefit"].
  - Aviva platform Onshore Bond: 101% of bond value [S4].
  - Quilter CIB: 100.1% of surrender value (101% prior to 25 November 2024) [S5 Aims, Q17].
- Return-of-premium guarantee riders (optional, chosen at outset only, cancellable but not restartable):
  - Prudential "Guaranteed Minimum Death Benefit" (a.k.a. Return of Premium Death Benefit Option): pays
    max(Sum Assured, GMDB) where GMDB = total premiums (net of set-up adviser charges) − partial/regular
    withdrawals − ongoing/ad hoc adviser charges. Charge assessed monthly = (GMDB − Sum Assured, if
    positive) × mortality factor depending on age at the last policy anniversary; levied by unit
    cancellation pro-rata across premiums/funds; zero when the option is out of the money [S1 "Are there
    any guarantees?", "Return of Premium Death Benefit option"; S2 §5.2, §10].
  - Quilter "Capital Protected Death Benefit": pays greater of (total premiums per policy − withdrawals,
    incl. DIM/adviser fees other than initial) and 100.1% of value; additional monthly charge; the charge
    may exceed growth [S5 Aims, Q5, Q17, Risks].
- On payment of the death benefit the plan is cancelled; no further benefits [S2 §9.5, §10.5].

### 5. Policy segmentation (mini-policies)
- Prudential: bond set up as a group of 20 identical segments by default; up to 999 segments on request
  (min £1,000 per segment when >20); premiums and units divided equally between policies; individual
  policies can be assigned or fully cashed in separately [S1 "What about tax?"; S2 §2.4].
- Aviva legacy: plan = 100 individual policies ("Your Plan is made up of 100 individual policies";
  definition: "a group of policies (maximum of 100)") [S3 Part A, Part C].
- Aviva platform: bond initially made up of 1,000 individual and identical policies [S4 "When can I access
  my money?"].
- Quilter: structured as 1,000 life assurance policies initially [S5 Q1, Q12].
- Purpose in every case is tax flexibility: full surrender of individual segments vs part surrender across
  all segments produce different chargeable-event outcomes [S1; S4; S5 Q12; R1 s484/s498; R2].

### 6. Charges — modern "clean" structures
- Prudential Annual Management Charge (AMC): each fund has its own AMC; for unit-linked funds 1/365 of the
  AMC is deducted daily from fund value (reflected in bid price); for PruFund funds the AMC is deducted
  monthly in arrears by unit cancellation at the Monthly Transaction Date [S2 §5.1.1–5.1.2].
- Prudential "Fund Size Discount" on the AMC by value band: <£24,999: 0.30%; £25,000–£49,999: 0.35%;
  £50,000–£99,999: 0.40%; £100,000–£249,999: 0.45%; £250,000–£499,999: 0.475%; £500,000–£999,999: 0.50%;
  £1,000,000–£1,749,999: 0.525%; £1,750,000–£2,999,999: 0.55%; £3,000,000+: 0.575% [S1 "What are the
  charges and costs?"]. The adjustment is computed at each Monthly Transaction Date on Assets Under
  Management per premium, applied as a single adjustment at the same percentage across funds [S2 §5.1.4].
- Fund-level "further costs" (transaction/underlying costs) borne within funds [S1; S2 §3.1.7].
- PruFund Protected Fund guarantee charge: fixed percentage set at outset, monthly in arrears by unit
  cancellation, ceases at Guarantee Date or on exit; non-refundable [S2 §5.3].
- Aviva platform: "Aviva charge" — annual management charge on the value of investments, deducted in
  monthly instalments (from no earlier than 17 Aug 2026 not applied to Transactional Cash); fund manager
  charges additional; Discretionary Investment Model charge where applicable; disinvestment mechanics for
  charge collection: +10% buffer over the charge due, £10 minimum disinvestment (or 6× the value, min £60,
  with Cash Management enabled) [S4 "What are the charges?"].
- Quilter: charges disclosed via personalised Key Features Illustration / Costs and Charges Statement /
  Charge Information Document (tiered platform-style charging; exact rates not printed in the KFD)
  [S5 Q7]. No current switch charge [S5 Q11].
- Both platform products levy an explicit "charge in respect of tax" (life-fund corporation tax passed to
  the policy) — see §13 below [S4; S5 Q15].

### 7. Charges — legacy structures (Aviva plan booklet)
- One-Off Charge: an initial charge on investing in or switching into specified funds, implemented as an
  Offer Price higher than the Bid Price (bid-offer spread mechanics); otherwise offer = bid (single priced)
  [S3 Part C definitions, Part D "Fund pricing"].
- Early Cash-in Charges: apply only if stated in the Schedule; a percentage of the value of units cashed in
  before the end of the Schedule period, per payment, on full or partial cash-in; NOT applied on death;
  regular withdrawals up to the "regular withdrawal percentage" are exempt [S3 Part D].
- Establishment Charge (if applicable): accrues daily during the early years, collected monthly by
  cancelling units, computed as a percentage of unit value, pro-rated across funds [S3 Part D].
- Yearly Management Charge: accrues daily, varies by fund, collected by reducing unit value and/or
  cancelling units; increase provisions tied to cost/tax/regulatory changes [S3 Part D].
- Switch Charge: administrative charge reserved but currently free [S3 Section three].
- With-profits funds within the bond: regular bonus at least monthly via unit price, discretionary final
  bonus, Market Value Reduction (MVR) on cash-in/switch-out if asset returns lag unit value; MVR never
  applied on death or on regular withdrawals ≤ 7.5% of plan value p.a. [S3 Part D, Section two].
- Other legacy features noted for regular-premium unit-linked endowment cousins (initial/capital units,
  allocation rates below 100%) were not present in any retrieved document — [unverified], flag as legacy
  variation only.

### 8. Funds, allocation and switching
- Fund count limits: Prudential max 10 funds at a time (Distribution Cash Fund and PruFund holding
  Accounts count within the 10) [S1; S2 §3.1.4]; Aviva legacy max 30 funds [S3 Part D]; platform products
  effectively unlimited menu (Quilter ~3,000 unit trusts/OEICs from 180+ managers [S5 About/Q8]; Aviva
  platform: authorised unit trusts, OEICs, SICAVs and Insured Funds, plus model portfolios and DIM
  [S4 "What can I invest in?"]).
- Switching: free at any time (right to introduce charges reserved) [S1; S2 §6.3.1.2; S3; S5 Q11].
- PruFund switching restrictions: once per quarter between PruFund Quarter Dates (25 Feb / 25 May / 25 Aug /
  25 Nov); 28-day waiting period on switches/withdrawals out of PruFund funds (unit price of the 28th day
  used); switches INTO PruFund route via holding Accounts growing at the Expected Growth Rate until the next
  Quarter Date; no switching into PruFund Protected funds [S1 "Can I change my investments?"; S2 §3.3.9,
  §4.2.1 ii), §6.3.3].
- Aviva platform Smooth Managed funds: one switch per calendar quarter [S4 "How do I change my investments?"].
- Automatic rebalancing: Prudential annual rebalancing to chosen proportions among unit-linked funds,
  cancelled by inconsistent instructions [S2 §6.4]; Quilter quarterly rebalancing within model portfolios
  [S5 Q8]; Aviva platform adviser-driven rebalancing [S4].
- Anti-market-timing: insurer may refuse/limit/charge switches on suspicion of market timing or excessive
  trading [S3 Section three; S5 Q10].
- Fund closure/merger/renaming powers with notice and default re-direction to nearest-objective fund or
  cash fund [S2 §3.1.3; S3 "Closing Funds"].

### 9. Unit pricing and valuation mechanics (modelling-relevant)
- Prudential internally-managed funds: at least monthly, maximum value (lowest buying price of assets) and
  minimum value (highest selling price) are computed, net of taxes/duties/reserves and the AMC; fund value
  is set between the two, driven mainly by net creation vs cancellation of units (purchase valuation basis
  if expanding, sale valuation basis if contracting — a swinging basis; a basis change "will reduce the
  Unit Price"); bid price ≥ minimum value / units in issue, rounded to nearest 0.1p [S2 §3.2.1–3.2.4].
- Externally-linked funds priced from the external manager's prices; insurer chooses between min/max bases
  by the same expansion/contraction logic [S2 §3.2.3, §3.2.5].
- Dilution levy possible to cover dealing costs, collected through unit pricing [S2 §3.2.6].
- Aviva legacy: funds valued every business day; Purchase Valuation vs Sale Valuation bases with the same
  expansion/contraction driver; deductions from benefits for expenses/losses on large cash-ins [S3 Part E].
- Forward pricing on platform products: deals placed before the cut-off receive the next dealing point's
  price; exact price unknowable in advance [S5 Q9].
- Transaction timing at Prudential: unit credit/cancellation same working day for correctly completed forms
  received by 12:00 midday, else next working day; up to 2 working days' delay allowed where the
  transaction is large relative to the fund [S2 §4.1.1, §4.2, §4.4].
- Deferral in exceptional circumstances: expected max 6 months for property/land funds, 1 month for others
  (Prudential and, in similar terms, Aviva); deferred transactions execute at end-of-period prices; the
  number of units to cancel is fixed at the start of the waiting period; deferral does NOT apply to death
  benefit payment [S1; S2 §8; S3 "Delay in dealing with Units in a Fund"].
- PruFund smoothing (for completeness — the smoothed with-profits fund range inside this unit-linked
  wrapper): unit price grows daily at the published Expected Growth Rate (EGR, never negative); at each
  Quarter Date if |NAV per unit − unit price| ≥ Quarterly Smoothing Limit the gap is halved (repeatedly);
  daily test against a Daily Smoothing Limit using the 5-working-day average NAV per unit, adjusting to a
  specified Gap After Adjustment; discretionary unit price reset to NAV; smoothing suspension (price = NAV
  per unit; review at least every 30 days, normally suspended min 30 days) [S2 §3.3.7–3.3.10]. PruFund
  Protected Fund Guarantee: on the chosen Guarantee Date units are added if value < Guaranteed Minimum Fund
  Value (initial protected premium, reduced proportionately for every unit cancellation for withdrawals /
  adviser charges / switches) [S2 §11].

### 10. Withdrawals (regular and partial) and surrender
- Three withdrawal mechanisms everywhere: regular withdrawals; one-off partial withdrawal (part surrender
  across policies); full surrender of one or more individual policies (segment surrender) [S2 §2.4.5, §7;
  S4 "When can I access my money?"; S5 Q12].
- Prudential regular withdrawals: frequencies monthly / 3-monthly / 4-monthly / 6-monthly / annual (4- and
  12-monthly not available with Distribution Income "natural income"); amount as fixed £, % of premiums, or
  % of unit value; each payment min £50; must leave ≥ £500 in a fund not fully encashed; maximum regular
  withdrawals in any 12 months = greater of 7.5% of plan value and 7.5% of total paid in, with ongoing
  adviser charges aggregated within the cap (e.g. 0.5% OAC ⇒ max 7% withdrawals); minimum 10 working days'
  lead time [S1 "How do I take money out?"; S2 §7.1].
- Prudential partial/full withdrawals: any time; possible 28-day settlement (unit price on the 28th day)
  for PruFund holdings and, at the insurer's protective discretion, generally [S1; S2 §4.2.2, §7.2, §7.3];
  requests are irrevocable once received [S2 §7].
- Aviva legacy: regular withdrawals monthly / 3-monthly / 6-monthly / yearly; up to the "regular withdrawal
  percentage" free of Early Cash-in Charges; distribution-fund natural-income options (half-yearly
  distributions, monthly payment variants smoothing 1/6 or 1/3 instalments) [S3 Section three].
- Aviva platform: withdrawals any time without penalty; regular withdrawals taken across all 1,000
  policies; single withdrawals by full policy surrender or part surrender across policies; minimum
  remaining balance applies [S4].
- Quilter: one-off part surrender max 95% of bond/fund value; £1,000 minimum must remain; regular
  withdrawals min £25, any date 1st–28th, chosen months; proceeds within ~10 working days of instruction
  [S5 Q12, Q13, Q16].
- Cancellation (cooling-off): 30 days from receiving plan documents, applies to top-ups too (Quilter:
  no cancellation rights on top-ups); refund reduced by any fall in value; adviser fees not refunded
  [S1 "What if the plan isn't right for me?"; S4 "Can I change my mind?"; S5 Q19].
- No paid-up mechanism exists (single premium product; no premium obligation) — structural observation
  [unverified as an explicit statement; consistent with all of S1–S5].

### 11. Adviser charging (post-RDR facilitation)
- Three adviser charge types (Prudential; materially identical at Aviva/Quilter): Set-up Adviser Charge
  (deducted from the payment before investment; the remainder is the Premium), Ongoing Adviser Charge
  (monthly/3-/6-/12-monthly; £ amount, % of premiums, or % of unit value; deducted by unit cancellation
  spread evenly across policies), Ad hoc Adviser Charge (one-off) [S2 §12.1–12.4; S1 "What are the charges
  and costs?"; S4 "How much will the advice cost?"].
- Ongoing and ad hoc adviser charges are treated as withdrawals for tax purposes (count within the 5%
  allowance) and count toward the 7.5% regular-withdrawal cap (Prudential) [S2 §12.1.1; S1; S4 Income Tax;
  S5 Q15 (DIM and adviser fees other than initial fees)].
- Maximum Limit Test caps total ongoing + ad hoc adviser charges per policy year; re-tested on partial
  withdrawals and instruction changes; charges cease on death notification, full surrender, assignment, or
  adviser deauthorisation [S2 §12.3.2, §12.7].
- Quilter/Aviva platform: DIM (discretionary manager) fees facilitated from the bond are likewise part
  surrenders with tax consequences [S5 Q11, Q15; S4].

### 12. Policyholder taxation (the wrapper the product promises)
- No personal CGT on the bond; gains do not use PSA / Dividend Allowance / CGT AEA [S1 "What about tax?";
  S4; S5 Q15; R1].
- Chargeable events: death of the (last) life assured giving rise to benefits, full surrender (of the bond
  or an individual policy/segment), part surrender above the allowance, assignment for consideration,
  maturity (n/a for whole-life bonds) [R1 s484; S1; S5 Q15].
- 5% tax-deferred allowance: cumulative 5% of each premium per insurance year (statutorily: allowable
  element = premium × y/20, y capped at 20 — i.e. total withdrawals up to 100% of premiums over 20 years
  with no immediate charge); unused allowance carries forward; excess over the cumulative allowance is an
  "excess event" gain at insurance-year end [R2; R1 s498/s507; S1; S4; S5 Q15 all state the 5%/20-year
  operation and that adviser/DIM fees consume the allowance].
- Gain on full surrender/death: TB − (TD + PG) per s491 (proceeds + prior withdrawals − premiums − prior
  excess gains) [R1 s491–s494]. On death the bond is treated as fully cashed in immediately before death
  [S5 Q15; R1 s484].
- Onshore credit: gains are treated as having borne basic-rate tax (because the insurer pays corporation
  tax on the fund — see §13); only higher/additional-rate taxpayers (or those pushed into those bands) pay
  the marginal difference [S4 Income Tax; S5 Q15; R6].
- Top-slicing relief (s535–s537) and deficiency relief (s539) exist in the statute [R1]; detailed mechanics
  not extracted — [unverified] beyond section references.
- Liability: individuals beneficially entitled; personal representatives; UK-resident trustees for
  trust-held bonds [R1 s465–s467; S5 "Tax under trust"].
- Chargeable Event Certificates are issued by the insurer when a gain arises [S5 Q15].
- Gains can affect personal allowances and means-tested benefits [S1; S5 Q15].

### 13. Life-office taxation reflected in product cash flows (I-E / BLAGAB)
- The insurer is liable to corporation tax on income and capital gains on the assets backing the bond
  (BLAGAB); under I-E the policyholder investment return is taxed at the policyholder rate (basic rate)
  with a minimum-profits test protecting the shareholder-profit slice [R6].
- Product pass-through mechanisms observed:
  - Insured funds: tax allowed for inside the daily unit price (Prudential unit pricing deducts reserves
    for taxes; Aviva insured funds' daily price includes the estimated tax charge) [S2 §3.2.1; S4 "Charge
    in respect of tax"; S3 Part E "paying tax on income from investments and capital gains"].
  - Platform/open-architecture holdings: explicit periodic tax charges to the policy — on income
    distributions and rebates as received (or at the monthly bond charge date for accumulation units), on
    realised gains at the next bond charge date after a sale/switch, on full surrender from proceeds, and
    an annual year-end deemed-disposal charge (Quilter financial year 1 Jan–31 Dec, charged in the first
    days of the new year) [S5 Q15 "Tax on funds"; S4 "Charge in respect of tax" — calculated annually, on
    sales and on income].

### 14. Prudential-regulatory frame for the projection model (Solvency UK)
- Technical provisions = best estimate + risk margin; BE = probability-weighted PV of ALL cash in/outflows
  needed to settle obligations, discounted on the risk-free term structure [R5 TP 2.4, 3.1, 3.2].
- Risk margin per reformed UK formula: 4% cost of capital, λ = 0.9 taper (floor 0.25) for long-term
  business [R5 TP 1.2, 4A.1].
- For unit-linked business UK practice decomposes the liability into the UNIT reserve (value of units,
  matched by the linked assets) and the NON-UNIT ("sterling") reserve — the BE of non-unit cash flows:
  charges (AMC less fund expenses), expenses, mortality cost of the death-benefit excess (e.g. the 0.1% or
  1% uplift and any GMDB rider), guarantee charges/claims; non-unit BE is commonly negative (future
  charges exceed costs), recognised as an asset-like offset under Solvency II-style valuation.
  [unverified — standard UK actuarial practice; the IFoA archive papers confirming the "sterling reserve"
  terminology could not be text-extracted (R9). The rule-level anchor is R5 TP 3.2 ("all the cash in- and
  out-flows") plus the product cash flows in S1–S5.]
- Conduct-side constraint on what benefits may be linked to: FCA permitted-links regime restricts linked
  benefits for natural-person policyholders to the COBS 21.3.1R asset list (and conditional permitted
  links with liquidity/access conditions) [R3]. This is why every product reserves fund deferral powers
  aligned to illiquid assets (6-month property deferral, S1/S2/S3).
- Mortality basis: CMI investigations (assurances mortality among them) are the standard industry source;
  full tables restricted to CMI subscribers [R8]. Specific table names for assured lives (e.g. the "00"
  and "16" Series, AMC00/AFC00, TMC16/TFC16) — [unverified; not confirmable from the fetched page].
  For a reference model the mortality assumption is a plug-in; the death-strain at risk is only
  (death benefit − unit value), i.e. 0.1%–1% of unit value plus any GMDB in-the-money amount [S1; S2 §5.2;
  S4; S5].
- Actuarial work standards: TAS 100 v2.0 (effective 1 July 2023) applies to the modelling work itself
  [R7]; TAS 200 (Insurance) applies to insurance technical actuarial work — [unverified; not fetched].

---

## Variations across insurers

| Feature | Prudential Investment Plan [S1,S2] | Aviva legacy Investment/Trustee Bond [S3] | Aviva platform Onshore Bond [S4] | Quilter CIB [S5] |
|---|---|---|---|---|
| Status | open | closed-book style booklet (05/2023) | open (adviser platform) | open (adviser platform) |
| Death benefit | 100.1% of units; optional ROP GMDB | 100.1% (101% pre-8/2006); Trustee Bond capital guarantee; ADB 110% | 101% | 100.1% (101% pre-25/11/2024); optional Capital Protected DB |
| Lives assured | 1 or 2 (joint), last death | 1+, last death | up to 10, last death | single/joint, last death |
| Max issue age (life assured) | 85 next birthday | top-ups to 84 | 89 | owner 18–90; CPDB rider <90 |
| Segments | 20 default, up to 999 (£1k min/segment) | 100 | 1,000 | 1,000 |
| Min initial / top-up | £10,000 / £10,000 | n/s in booklet | £10,000 / £1,000 | £10,000 / n/s |
| Max investment | £5m general | n/s | none (£1m Smooth Managed) | none stated |
| Fund menu | ~10 internal+mirror funds max held; PruFund smoothed range | insurer funds incl. with-profits, distribution funds; max 30 | open architecture (UT/OEIC/SICAV/insured) + DIM | ~3,000 UT/OEICs, MPS/DIM |
| Charge shape | fund AMC daily + tiered discount; adviser charges | YMC daily + legacy One-Off (bid/offer), Early Cash-in, Establishment charges | Aviva charge monthly + fund charges + explicit tax charge | platform tiered charging + explicit tax charge |
| Regular withdrawal cap | 7.5% p.a. (incl. OAC) | regular withdrawal % free of ECC; 7.5% MVR-free (WP) | none stated (5% tax allowance guidance) | min £25; £1,000 must remain |
| Smoothed fund option | PruFund (EGR + smoothing limits, 28-day waits, quarter dates) | with-profits fund with MVR | Smooth Managed funds (quarterly switch limit) | none |
| Settlement frictions | 28-day PruFund wait; 2-day large-deal delay; 6m property | property/external fund suspension | fund suspension/deferment | forward pricing, ~10 working days payout |

Representative design for a reference model: a modern "clean-charge" onshore bond — single premium
(min £10,000) with top-ups; single/joint life last-death; whole of life; death benefit 100.1% of unit
value (0.1% death uplift), optional return-of-premium GMDB with monthly mortality-factor charge on the
in-the-money excess; 100–1,000 identical segments; daily-priced single-priced units; fund-level AMC
accrued daily (optionally with a value-tier discount); regular/partial/segment withdrawals with the 5%/20-year
cumulative tax-deferred allowance and a 7.5% p.a. product cap; post-RDR adviser charges as unit-cancelling
outflows counted as withdrawals. The Prudential document pair (S1+S2) is the most completely specified
public source and is the recommended primary template; Quilter/Aviva-platform (S4, S5) show the explicit
life-fund tax charge variant; Aviva legacy (S3) supplies the legacy-charge layer (bid-offer One-Off
Charge, Early Cash-in Charge scale, Establishment Charge) for back-book variations.

Market context: Canada Life closed its Select Account onshore bond to new business on 23 January 2024,
retaining features for existing customers — evidence that the onshore bond market is consolidating around
platform providers (Quilter, Aviva, M&G/Pru, Standard Life etc.) [S7].

---

## Gaps and caveats

1. Quilter CIB Terms and Conditions (S6) and Aviva legacy KFD (S8) were downloaded but not parsed; all
   Quilter/Aviva facts above come from S5/S3/S4 only. The Quilter terms would pin down segment-level
   mechanics (e.g. per-policy rounding, bond charge date definition).
2. Canada Life Select Account product documents (KFD/policy provisions) were not retrieved — only the
   closure announcement (S7). Canada Life's key-features PDFs did not surface with stable URLs in search.
3. Standard Life/abrdn and Scottish Widows onshore bond documents were not fetched in this session; the
   3-insurer minimum is met by Prudential, Aviva and Quilter.
4. Legacy structures — allocation rates below/above 100%, capital/initial units with higher management
   charges on early premiums, establishment-charge scales — are only partially evidenced: S3 confirms
   One-Off (bid-offer) Charges, Early Cash-in Charge scales (values live in each policy Schedule, not the
   public booklet) and an Establishment Charge; initial/capital-unit mechanics remain [unverified].
5. Actual AMC percentages per fund are published in Fund Guides / Investment Option Documents (per-fund,
   frequently updated); only the Prudential AMC discount tier table is captured here. A rate-card snapshot
   would need a separate fetch of the PIP Fund Guide (mandg.com invb11013.pdf, located but not read).
6. FCA COBS 21.3 was captured (R3), but COBS 21.2 (prudent-management/discretion duties) was not extracted
   — the handbook site requires JavaScript rendering per page.
7. The unit vs non-unit ("sterling") reserve decomposition is standard UK practice but is tagged
   [unverified]: the IFoA archive papers evidencing the terminology are scanned images (R9). The PRA rule
   anchor (R5 TP 3.2, all-cash-flows BE) plus product cash flows are sufficient to build the model; a
   citable IFoA educational source (e.g. SP2 core reading) is subscription-restricted.
8. CMI assured-lives table names (e.g. "00" Series AMC00/AFC00, "16" Series) could not be confirmed from
   the fetched CMI page (R8) — full CMI outputs are subscriber-only; treat the mortality basis as
   [unverified] plug-in assumptions.
9. TAS 200 (Insurance), the IFoA APS standards, and specific IFoA working-party papers on unit-linked
   matters were not fetched; only TAS 100 v2.0 is verified (R7).
10. Chargeable-event fine detail (top-slicing s535–s537 computation, deficiency relief s539, personal
    portfolio bond rules, s500 loan-as-part-surrender) was identified by section number (R1) but the
    mechanics were not extracted beyond the 5% rule (R2).
11. Prudential PruFund smoothing parameters (Expected Growth Rates, Quarterly/Daily Smoothing Limits, Gap
    After Adjustment) are published separately at pru.co.uk (WPGB0031) and change over time; only the
    mechanism (not current values) is captured [S2 §3.3.10].
12. Solvency UK: the Technical Provisions Part was read as at 03/08/2026 (R5); contract-boundary rules and
    the detailed BE assumptions requirements (former Delegated Regulation, restated via PS15/24) were not
    separately extracted.
