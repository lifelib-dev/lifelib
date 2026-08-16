# Variable Annuity with living and death benefit guarantees — research notes (U.S.)

Access date for all citations: 2026-08-04.

Purpose: source library and extracted specifications to drive a reference liability
cash-flow projection model (lifelib/modelx style) for U.S. individual deferred
variable annuities (VAs) carrying guaranteed minimum death benefits (GMDBs) and
guaranteed living benefits (GLWB/GMWB, GMIB, GMAB).

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). These S#/R# numbers are **local to this file** and independent of the
cross-product library numbering. Facts stated from general knowledge and not
verified against a retrieved document are tagged [unverified].

Retrieval note: `sec.gov` and `efts.sec.gov` return HTTP 403 to a plain fetch. All
SEC documents below were retrieved with an explicit declared User-Agent (SEC's
stated requirement for programmatic access) and read in full as text. Every
document marked "Retrieved: YES" was actually downloaded and read.

---

## Primary sources

### S1. Jackson National Life Insurance Company — Perspective II® Flexible Premium Variable and Fixed Deferred Annuity — statutory prospectus dated April 28, 2025
- Publisher: Jackson National Life Insurance Company, through Jackson National
  Separate Account – I (CIK 0000927730)
- Doc type: SEC Form N-4 statutory prospectus, filed as Form 485BPOS
  (accession 0000927730-25-000086), ~4.9 MB HTML
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773025000086/ck0000927730-20250422.htm
- Retrieved: YES (converted to ~1.28 MB plain text and read in relevant part)
- Product: Perspective II, contracts offered for sale on and after June 24, 2019.
  Flexible premium variable **and fixed** deferred annuity. Separate Account plus a
  general-account Fixed Account with multiple duration "Fixed Account Options"
  subject to a market value adjustment.
- Why it matters: this is the most contractually detailed GLWB/GMDB disclosure in
  the set — it gives full benefit-base algebra (GWB, GAWA, bonus/Bonus Base,
  step-up, GWB adjustment, excess-withdrawal proportional reduction), plus
  ten years of historical rate tables in Appendices F–J.

### S2. Jackson National Life Insurance Company — Perspective II® Initial Summary Prospectus (Summary Prospectus for New Investors), April 28, 2025
- Publisher: same as S1; filed as exhibit EX-99.(o)(1) to the S1 registration statement
- Doc type: Rule 498A Initial Summary Prospectus (~16 pages)
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773025000086/jnlpiiafter6-24x19initials.htm
- Retrieved: YES (full text read)
- Why it matters: compact Key Information Table + fee tables + "Benefits Available
  Under the Contract" table; the cleanest single view of the charge structure.

### S3. Jackson National Life Insurance Company — Rate Sheet Prospectus Supplement dated April 27, 2026 (Perspective II)
- Publisher: same as S1; SEC Form 497 (accession 0000927730-26-000157)
- Doc type: rate sheet prospectus supplement (6 pages) — the document that carries
  the *currently offered* rider charges, GAWA percentages, bonus percentages, GWB
  adjustment percentages and GMDB roll-up percentages
- URL fetched: https://www.sec.gov/Archives/edgar/data/927730/000092773026000157/jnlpiiafter6-24x19rateshee.htm
- Retrieved: YES (full text read)
- Why it matters: this is the *current* (April 27, 2026) parameter set. Rate-sheet
  filings are how modern VA writers reset GLWB payout rates without a prospectus
  amendment — a structural fact any model of this product must accommodate.

### S4. American General Life Insurance Company (Corebridge Financial) — Polaris Advisory Variable Annuity — prospectus dated May 1, 2026
- Publisher: American General Life Insurance Company, Variable Separate Account
  (CIK 0000729522); SEC Form 485BPOS, accession 0001193125-26-186414
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526186414/d79162d485bpos.htm
- Retrieved: YES (~732 KB plain text; fee table, living-benefit and death-benefit
  sections, Appendix C fee formula and Appendix H examples read)
- Product: fee-based (advisory) share class; no withdrawal charge. Living benefits:
  Polaris Income Max and Polaris Income Plus Daily Flex. Death benefits: Contract
  Value, Return of Purchase Payment, Maximum Anniversary Value.
- Why it matters: contains (a) a **VIX-linked non-discretionary rider fee formula**
  written out algebraically, and (b) the "Secure Value Account" mandatory
  general-account allocation as an investment-requirement risk control.

### S5. American General Life Insurance Company (Corebridge) — Rate Sheet Prospectus Supplement dated May 1, 2026 (Polaris Advisory)
- Doc type: SEC Form 497, accession 0001193125-26-164551 (3 pages)
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526164551/d113668d497.htm
- Retrieved: YES (full text read)
- Why it matters: full current Maximum Annual Withdrawal Percentage / Protected
  Income Payment Percentage grid by age band × 1-vs-2 covered persons ×
  three Income Options, plus Income Credit and Minimum Income Base percentages.

### S6. American General Life Insurance Company (Corebridge) — Polaris Choice IV — prospectus dated May 1, 2026
- Doc type: SEC Form 485BPOS, accession 0001193125-26-173379
- URL fetched: https://www.sec.gov/Archives/edgar/data/729522/000119312526173379/d97533d485bpos.htm
- Retrieved: YES (~503 KB plain text; fee table, penalty-free withdrawal, nursing
  home waiver, purchase-payment and issue-age rules read)
- Product: commission-based ("B-share"-style) Polaris with a 4-year withdrawal
  charge schedule. Note: "This contract is no longer available for purchase by new
  contract Owners." [S6] — it is a recently-sold, currently-in-force design.
- Why it matters: supplies the withdrawal-charge schedule, M&E-equivalent "Base
  Contract Expense" and contract maintenance fee that the advisory class (S4) lacks.

### S7. Equitable Financial Life Insurance Company / Equitable Financial Life Insurance Company of America — Retirement Cornerstone® Series — prospectus dated May 1, 2026
- Publisher: Separate Account No. 70 (CIK 0001537470) and Equitable America
  Variable Account No. 70A; SEC Form 485BPOS, accession 0001193125-26-169230
- URL fetched: https://www.sec.gov/Archives/edgar/data/1537470/000119312526169230/d120089d485bpos.htm
- Retrieved: YES (~1.45 MB plain text; definitions, benefits, GIB mechanics,
  charges and expenses sections read)
- Product: "combination variable and fixed individual and group flexible premium
  deferred annuity contract" with a **two-account architecture**: an *Investment
  Performance account* (no guarantees) and a *Protection with Investment
  Performance account* (funds the guarantees). Guaranteed income benefit (GIB) is
  an annuitization-style GMIB; GMDBs are Return of Principal, Highest Anniversary
  Value, and "Greater of".
- Why it matters: the only design in the set with (a) a **formula-driven roll-up
  rate tied to 10-year Treasuries**, (b) a bifurcated account structure that
  restricts which money earns guarantees, and (c) an explicit deferral-bonus
  roll-up that terminates permanently on the first withdrawal.

### S8. The Lincoln National Life Insurance Company — Lincoln ChoicePlus℠ product suite / Lincoln ChoicePlus Assurance℠ — Form N-4 post-effective amendment filed April 23, 2026 (prospectuses and rate sheets dated May 1, 2026)
- Publisher: Lincoln Life Variable Annuity Account N (CIK 0001048606); SEC Form
  485BPOS, accession 0001104659-26-047599 (~20 MB HTML bundling several rate-sheet
  supplements and prospectuses)
- URL fetched: https://www.sec.gov/Archives/edgar/data/1048606/000110465926047599/tm265235d1_485bpos.htm
- Retrieved: YES (~2.68 MB plain text; the three Lincoln ProtectedPay®/4LATER®/
  i4LIFE® rate sheets, the Key Information and Fee Tables, the ProtectedPay
  Enhancement/Account Value Step-up mechanics, and Appendix C discontinued-rider
  charges were read)
- Products: Lincoln ProtectedPay® Select Core / Select Plus / Select Max (GLWB
  suite), 4LATER® Select Advantage (deferral rider), i4LIFE® Advantage with
  Guaranteed Income Benefit (a *variable annuitization payout rider* with a
  guaranteed floor), plus legacy Lincoln Lifetime Income℠ Advantage 2.0 and
  Lincoln Max 6 Select℠ Advantage.
- Why it matters: unique **two-table GLWB payout structure** (Table A while
  contract value > 0; Table B, materially lower, once contract value hits zero) and
  a payout-phase guarantee (i4LIFE) rather than a withdrawal-phase guarantee.

---

## Regulatory and actuarial references

### R1. NAIC — Valuation Manual, Jan. 1, 2026 Edition — **VM-21: Requirements for Principle-Based Reserves for Variable Annuities**
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457-page PDF downloaded; VM-21 occupies PDF pages 142–226,
  manual pages 21-1 through 21-76; Sections 1, 2, 3, 4, 6, 7, 10 read)

### R2. NAIC / Oliver Wyman — "Variable Annuity Statutory Reserve and Capital Reform — QIS II Executive Summary", February 12, 2018
- Publisher: NAIC Variable Annuities Issues (E) Working Group (report by Oliver Wyman)
- URL fetched: https://content.naic.org/sites/default/files/committee_related_documents/cmte_e_va_issues_wg_related_qis_ii_executive_summary.pdf
- Retrieved: YES (13-page PDF; background and QIS I/QIS II overview read)

### R3. NAIC — Life Risk-Based Capital instructions, **LR027 Interest Rate Risk and Market Risk** (C-3 Phase II for VAs)
- Publisher: NAIC Capital Adequacy (E) Task Force
- URL fetched: https://content.naic.org/sites/default/files/inline-files/LR027%20mod%20for%20vol%20res%202020.pdf
- Retrieved: YES (5-page PDF; full 7-step process, CTE(98) definition, RBC formula,
  phase-in and smoothing read)

### R4. American Academy of Actuaries — "Implementation of Requirements for Principle-Based Reserves for Variable Annuities – 2022 Edition of VM-21" (Practice Note Supplement), February 2022
- Publisher: Variable Annuity Reserves & Capital Work Group, Life Practice Council, AAA
- URL fetched: https://actuary.org/wp-content/uploads/2022/02/VA_PN_Supplement_Final.pdf
- Retrieved: YES (34-page PDF; introduction, acronym list, background, C-3 Phase 2
  Q&A and disclosures Q&A read)

### R5. American Academy of Actuaries — "Utilization Assumptions of Guaranteed Living Benefits for Deferred Annuities: A Resource and Discussion Guide", May 2024
- Publisher: Life Experience Committee, AAA (Donna Claire, chair)
- URL fetched: https://actuary.org/sites/default/files/2024-05/life-paper-GLBs.pdf
  (note: `www.actuary.org` 301-redirects to `actuary.org`; the redirect target was
  fetched directly)
- Retrieved: YES (18-page PDF, read in full including both sample utilization tables)

### R6. U.S. Securities and Exchange Commission — **Form N-4** (reference copy, version effective September 23, 2024)
- URL fetched: https://www.sec.gov/files/formn-4.pdf
- Retrieved: YES (65-page PDF; general instructions and item index read)

### R7. SEC Rule 498A, 17 CFR 230.498A — summary prospectuses for variable annuity and variable life contracts
- URL fetched: https://www.law.cornell.edu/cfr/text/17/230.498A
- Retrieved: YES

### R8. FINRA Rule 2330 — Members' Responsibilities Regarding Deferred Variable Annuities
- URL fetched: https://www.finra.org/rules-guidance/rulebooks/finra-rules/2330
- Retrieved: YES

### R9. Internal Revenue Code § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES

### R10. Treas. Reg. § 1.817-5 — Diversification requirements for variable annuity, endowment, and life insurance contracts
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.817-5
- Retrieved: YES

### R11. Actuarial Standards Board — ASOP No. 52, "Principle-Based Reserves for Life Products under the NAIC Valuation Manual"
- URL fetched: http://www.actuarialstandardsboard.org/asops/principle-based-reserves-life-products-naic-valuation-manual/
- Retrieved: YES

### R12. Actuarial Standards Board — Standards of Practice index (titles and effective dates for ASOP Nos. 22, 52, 56)
- URL fetched: http://www.actuarialstandardsboard.org/standards-of-practice/
- Retrieved: YES

### R13. Society of Actuaries Research Institute & LIMRA — "2022–2024 Variable Annuity Guaranteed Living Benefit / Contract Holder Behavior Study"
- URL fetched: https://www.soa.org/resources/experience-studies/2025/2022-24-va-livingbenefit/
- Retrieved: YES (landing page only — the detailed report is a paid data package)

---

## Extracted specifications

### 1. Contract architecture and phases

- Two phases universally: accumulation phase and income phase (annuitization).
  Once annuitized, withdrawals/surrender cease and (with the exception of certain
  riders) death benefits and living benefits terminate [S2][S4][S6][S7][S8].
- Separate account divided into subaccounts ("Investment Divisions" [S1][S2];
  "Variable Portfolios" [S4][S6]; "variable investment options" [S7];
  "Subaccounts" [S8]), each investing in one underlying fund.
- General-account options coexist with the separate account:
  - Jackson: "Fixed Account Options" of stated duration with a declared base
    interest rate; a market value adjustment applies on early withdrawal,
    transfer or annuitization [S1].
  - Corebridge: "Fixed Accounts", "DCA Fixed Accounts" and — only with a living
    benefit — the mandatory **Secure Value Account** [S4].
  - Equitable: "guaranteed interest option" plus "account for special dollar cost
    averaging" [S7].
  - Lincoln: fixed account with Guaranteed Periods; an **Interest Adjustment**
    (MVA) applies to withdrawal/surrender/transfer before the end of a Guaranteed
    Period [S8].
- Latest annuitization date:
  - Jackson: "Latest Income Date" = the Contract Anniversary on which the Owner is
    **95** [S2].
  - Corebridge: "Latest Annuity Date" = first NYSE business day of the month
    following the owner's **95th birthday**; annuitization generally permitted any
    time after the 2nd contract anniversary [S4].
  - Equitable: maturity date = contract date anniversary following the annuitant's
    **95th birthday** [S7].
  - Lincoln: i4LIFE® Advantage may be elected up to **age 95** (younger of owner or
    Secondary Life) [S8].

### 2. Issue ages, premium limits

| Item | Value | Source |
|---|---|---|
| Jackson max issue age | "We will not issue a Contract to someone older than age 85." | [S1] |
| Jackson min initial premium | $10,000 non-qualified (under most circumstances); $5,000 qualified | [S2] |
| Jackson min subsequent premium | $500 ($50 under auto payment plan) | [S2] |
| Jackson max total premiums | $1,000,000 without prior approval | [S2] |
| Jackson GMWB (Flex) eligible ages | Designated Lives **35 to 80**; 35 to 75 if Flex DB elected | [S1] |
| Jackson add-on GMDB eligibility | Roll-up, HQAV and Combination GMDBs available if age **79 or younger** at issue | [S1] |
| Corebridge max issue age | "We will not issue a contract to anyone age 86 or older on the contract issue date." Qualified contracts generally not issued at 72+ absent RMD evidence | [S6] |
| Corebridge min initial purchase payment | $25,000 qualified and non-qualified; min subsequent $500; min automatic subsequent $100 | [S6] |
| Corebridge purchase payment limit | $2,000,000 for contracts issued on/after Sept 5, 2023 ($1,000,000 before) | [S4] |
| Corebridge subsequent payments | not accepted from owners age 86+; not accepted on/after the 1st contract anniversary if a living benefit is elected | [S6] |
| Equitable GMDB election ages | age **0–75** at issue (0–70 for Series CP®) | [S7] |
| Equitable Inherited IRA continuation contract | not available for owners over age 70 | [S7] |
| Lincoln ProtectedPay PAI age bands | begin at **59** (59–64 / 65–69 / 70–74 / 75–79 / 80+) | [S8] |
| Lincoln Account Value Step-up age limit | owner/annuitant (and Secondary Life if joint) must be **under age 86** | [S8] |

### 3. Base contract charges (the "M&E + admin" layer)

**Jackson Perspective II** [S2]:
- Single blended "**Core Contract Charge**" of **1.30% maximum**, assessed daily as
  a percentage of average daily account value of the Investment Divisions.
  Reduced to **1.15%** if Contract Value on the later of the Issue Date or the most
  recent Contract Quarterly Anniversary is ≥ $1 million.
- Annual Contract Maintenance Charge **$35 maximum**, waived on Contract Value of
  $50,000 or more; deducted proportionally on the Contract Anniversary or on total
  withdrawal.
- Key Information Table shows base contract annual fee **1.31% minimum = 1.31%
  maximum** (the 1.30% asset charge plus the amortized contract fee) [S2].
- Fund fees and expenses: **0.52% minimum / 2.28% maximum** of average fund net
  assets (as of December 31, 2021 per the table footnote) [S2].
- Transfer charge: $25 per transfer after 25 transfers in a Contract Year (reserved
  right) [S2].
- Premium taxes: 0.0%–3.5%, varying by state [S2].
- Expedited delivery $10 (Mon–Fri) / $22.50 (Sat); wire fee $20 domestic / $25
  international [S2].

**Corebridge Polaris Choice IV** (commission share) [S6]:
- **Base Contract Expense 1.65%** of average daily ending net asset value allocated
  to the Variable Portfolios.
- **Contract Maintenance Fee $50** annually, waived if contract value ≥ $75,000.
- Transfer fee $25 per transfer after the first 15 in a contract year ($10 in PA and TX).
- Fund expenses 0.46% – 1.85%.
- Beneficiary "Extended Legacy Program" base contract expense also 1.15% [S6].

**Corebridge Polaris Advisory** (fee-based share) [S4]:
- **Base Contract Expenses 0.40%** of average daily ending net asset value in the
  Variable Portfolios; **no contract maintenance fee and no withdrawal charge**.
- Transfer fee $25 after 15 transfers per contract year ($10 in PA and TX).
- Fund expenses 0.21% – 1.60%.
- Advisory fees withdrawn from contract value are capped at an annualized 1.5% of
  contract value and are **treated as withdrawals** for benefit purposes [S4].
- Premium tax 0% – 3.5%, deducted only at annuitization if advanced [S4].

**Equitable Retirement Cornerstone** — charges are unbundled into three daily
separate-account charges [S7]:

| Series | Operations charge | Administration charge | Distribution charge | Total daily |
|---|---|---|---|---|
| B | 0.80% | 0.30% | 0.20% | 1.30% |
| CP® | 0.95% | 0.35% | 0.25% | 1.55% |
| L | 1.10% | 0.30% | 0.25% | 1.65% |
| C | 1.10% | 0.25% | 0.35% | 1.70% |
| ADV | 0.35% | 0.20% | 0.10% | 0.65% |

(Totals computed from the three component rows; the components are quoted
individually in the prospectus.) [S7]
- Annual administrative charge: deducted on each contract date anniversary **only
  if Total account value < $50,000**. Contract years 1–2: $30 or, if less, 2% of
  Total account value. Contract years 3+: $30 [S7].
- Transfer charge: currently $0; reserved right to charge for transfers in excess of
  12 per contract year, never to exceed $35 [S7].
- Special service charges: wire transfer $90; express mail $35; duplicate contract $35 [S7].
- Note: for Protection with Investment Performance variable investment options, a
  portion of the operations charge is stated to compensate for the (free) Return of
  Principal death benefit [S7].

**Lincoln ChoicePlus** [S8] — base contract expense varies with the elected death
benefit (i.e., GMDB cost is embedded in the M&E rather than charged separately):

| Death benefit elected | Base contract expense (% of average Contract Value) |
|---|---|
| Guarantee of Principal Death Benefit | 1.55% |
| Enhanced Guaranteed Minimum Death Benefit (EGMDB) | 1.65% |
| 5% Step-up Death Benefit | 1.80% |
| Estate Enhancement Benefit (EEB) without 5% Step-up | 1.85% |
| EEB in combination with 5% Step-up | 1.90% |

- Administrative Expense (**Annual Account Fee**) **$35** [S8].
- Key Information Table: base contract 1.57%–1.92% depending on death benefit
  (includes an amount attributable to the Annual Account Fee); fund fees and
  expenses **0.27% – 3.48%**; optional benefits **0.40% – 2.75%** as an annualized
  percentage of the Protected Income Base [S8].
- Lowest annual cost $2,116 / highest annual cost $7,939 on a $100,000 investment
  with 5% appreciation [S8].
- In the prospectus section retrieved, the Transaction Expenses table lists **only**
  an Interest Adjustment on the fixed account — i.e., that particular class carries
  no withdrawal charge. See "Gaps and caveats". [S8]

### 4. Withdrawal (surrender / contingent deferred sales) charge schedules

**Jackson Perspective II — Base Schedule** (as a percentage of *Remaining Premium*
withdrawn, by **Completed Years since receipt of that premium**, not contract year) [S2]:

| Completed Years since premium receipt | 0–1 | 1–2 | 2–3 | 3–4 | 4–5 | 5–6 | 6–7 | 7+ |
|---|---|---|---|---|---|---|---|---|
| Charge | 8.5% | 7.5% | 6.5% | 5.5% | 5.0% | 4.0% | 2.0% | 0.0% |

- A **Four Year Withdrawal Charge Schedule** option existed for an additional
  0.40% charge; elected before August 28, 2023 [S1].
- "Remaining Premium" = total premium paid, reduced by withdrawals of premium
  (including withdrawal charges) before adjustment for MVA or charges [S2].
- **Free withdrawal**: "The free withdrawal is equal to **10% of Remaining Premium**
  during each Contract Year that would otherwise incur a withdrawal charge, minus
  earnings." Earnings (excess of Contract Value over Remaining Premium) come out
  free first; premium that has aged past the schedule also comes out free. RMD
  withdrawals reduce the free-withdrawal allowance [S1].
- **Terminal Illness / Extended Care Benefit** (free, all contracts): increases the
  amount withdrawable without a withdrawal charge on (i) 12-month terminal
  prognosis or (ii) 90 consecutive days' nursing home/hospital confinement.
  Maximum free withdrawal $250,000 of Contract Value; exercisable once; MVA still
  applies [S2].

**Corebridge Polaris Choice IV** — withdrawal charge as a percentage of each
Purchase Payment withdrawn, by years since receipt [S6]:

| Years since receipt | 1 | 2 | 3 | 4 | 5+ |
|---|---|---|---|---|---|
| Charge | 8% | 7% | 6% | 5% | 0% |

- Penalty-free withdrawal amount = **10% of remaining Purchase Payments not yet
  withdrawn** each contract year and still subject to withdrawal charges. It does
  not reduce the basis for future penalty-free amounts. Purchase payments no longer
  subject to a withdrawal charge may also be withdrawn penalty-free [S6].
- **Nursing Home Waiver**: withdrawal charges may be waived on withdrawals made
  while confined for ≥ 60 days, or within 90 days after leaving; not usable in the
  first 90 contract days; confinement must begin after purchase [S6].

**Corebridge Polaris Advisory**: no withdrawal charge at all [S4].

**Equitable Retirement Cornerstone** — withdrawal charge as % of the contribution
withdrawn, by contract year following receipt of that contribution (contributions
invested longest are treated as withdrawn first) [S7]:

| Series | Yr 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| B | 7% | 7% | 6% | 6% | 5% | 3% | 1% | 0% | — | — |
| L | 8% | 7% | 6% | 5% | 0% | — | — | — | — | — |
| CP® | 8% | 8% | 7% | 6% | 5% | 4% | 3% | 2% | 1% | 0% |
| C | none | | | | | | | | | |
| ADV | none | | | | | | | | | |

- The charge applies (1) on withdrawals in a contract year exceeding the free
  withdrawal amount, (2) on surrender, and (3) on annuitization into a **non-life-
  contingent** annuity option [S7].
- Series CP® pays a **credit** of 4% or 5% of each contribution based on total
  first-year contributions; credits are not treated as contributions for withdrawal
  charge purposes and are forfeited on free-look cancellation [S7].

**Lincoln**: no withdrawal charge in the class whose fee table was read; an
**Interest Adjustment** applies to fixed-account amounts withdrawn, surrendered or
transferred before the end of a Guaranteed Period. The Interest Adjustment does
**not** apply to dollar cost averaging, cross-reinvestment, withdrawals up to the
Maximum Annual Withdrawal amount under Lincoln SmartSecurity® Advantage, or Regular
Income Payments under i4LIFE® Advantage [S8].

### 5. Market value adjustment (fixed-account MVA)

Jackson describes the MVA **mechanically and by rate relationship** rather than
publishing a closed-form exponent [S1]:

- Definition: "an adjustment to the Contract Value allocated to the Fixed Account
  that is withdrawn, transferred, or annuitized before the end of the period" [S2].
- Reference rates:
  - *base interest rate* = the rate declared when the allocation to a Fixed Account
    Option was made.
  - *current new business interest rate* = **0.25% per annum greater than** the base
    interest rate currently offered on new allocations to Fixed Account Options of
    the same duration. If that duration is not offered, it is estimated from the
    closest durations offered [S1].
- Direction: if the new-business rate exceeds the original base rate → downward
  (negative) adjustment; if lower → upward (positive) adjustment; equal → none [S1].
- **Dead band**: "If the current new business interest rate is greater than the base
  interest rate … there will be no Market Value Adjustment if the difference between
  the two is less than 0.25%." This offsets the +0.25% loading built into the
  new-business rate [S1].
- **Floor**: "In no event will the amount of a total withdrawal, transfer or
  annuitization from the Fixed Account Options be less than the Fixed Account
  Minimum Value." Worked example in the prospectus: $10,000 initial premium at a
  3% declared rate → $10,265 after one year; with a 1% Fixed Account minimum
  interest rate the Fixed Account Minimum Value is $8,787.50, so an MVA cannot
  reduce the withdrawal by more than $1,477.50. A $1,500 negative MVA is truncated
  to leave exactly $8,787.50 [S1].
- **MVA exemptions**: amounts taken from the one-year Fixed Account Option; death
  benefit payments; payments under a life-contingent income option or an income
  option spread over ≥ 5 years; amounts withdrawn for contract charges; free
  withdrawals; amounts removed on the Latest Income Date; amounts removed in the
  30-day window following the end of a Fixed Account Option period [S1].
- The Fixed Account minimum interest rate is **reset periodically according to a
  formula**, and a credited rate may move up or down to the new minimum but never
  below the base interest rate [S1]. (The formula's inputs were not extracted —
  see Gaps.)

Modelling note: the explicit algebraic MVA factor of the form
`((1+i_old)/(1+i_new))^n − 1` was **not** found in any of the four prospectuses read
[unverified as a contract term for these products]. Jackson's disclosure is a
rate-differential description with a 0.25% dead band and a nonforfeiture floor;
Lincoln calls the same thing an "Interest Adjustment" without publishing a formula
in the section read [S8].

### 6. Guaranteed living benefits — benefit-base mechanics

#### 6.1 Jackson "Flex GMWB" / "Flex Net GMWB" family (single and joint) [S1][S3]

Core state variables: **GWB** (Guaranteed Withdrawal Balance — the benefit base),
**GAWA** (Guaranteed Annual Withdrawal Amount), **Bonus Base**, and a separate
**GWB adjustment** amount.

*Initialisation* [S1]:
- Added at issue → GWB = initial Premium net of applicable premium taxes.
- Added on a later Contract Anniversary → GWB = Contract Value on that date.
- GAWA = GAWA% × GWB immediately prior to the first partial withdrawal. The GAWA%
  is fixed by the Designated Life's **attained age at the time of the first
  withdrawal** and by the elected benefit option's Income Stream Level.
- GWB and Bonus Base are each capped at **$10 million** [S1].
- Available at Designated Life ages **35–80** (35–75 with Flex DB) [S1].

*Premium payments* [S1]:
- GWB increases by the premium net of premium taxes.
- If the premium is received after the first withdrawal, GAWA increases by
  `GAWA% × premium (net of tax)`, or by `GAWA% × increase in GWB` if the $10m cap
  binds.
- Bonus Base increases by the premium net of premium taxes.

*Withdrawals* — the prospectus states the algebra explicitly [S1]:
- Let `W` = current partial withdrawal, `ΣW` = cumulative withdrawals this Contract
  Year, `L` = max(GAWA, RMD if a qualified contract).
- **Excess Withdrawal** = min( W , ΣW − L ), i.e. only the portion of the current
  withdrawal that pushes cumulative withdrawals past the limit.
- If `ΣW ≤ L`: `GWB_new = max(GWB_old − W, 0)`; **GAWA unchanged**.
- If `ΣW > L`:
  `GWB_new = max( (GWB_old − non-excess portion of W) × (1 − ExcessW / CV_before_excess) , 0 )`
  — i.e. dollar-for-dollar for the non-excess portion, then **proportional to the
  contract-value reduction caused by the excess portion**;
  `GAWA_new = min( GAWA_old × (1 − ExcessW / CV_before_excess) , GWB_new )`.
- If the For Life Guarantee is not in effect and GWB < GAWA at the end of a Contract
  Year, GAWA is set equal to GWB.
- "For purposes of all of these calculations, all partial withdrawals are assumed to
  be the total amount withdrawn, including any withdrawal charges, asset allocation
  fees, Market Value Adjustments and other charges and adjustments." [S1]
- **All** withdrawals count toward the annual limit, including automatic
  withdrawals, RMDs, advisory-fee withdrawals, partial 1035 exchanges and free
  withdrawals [S1].
- If cumulative withdrawals ≤ L, **no withdrawal charge applies** to them [S1].
- IRC §72(t)/72(q) withdrawals are **not** treated as RMDs for guarantee-preservation
  purposes [S1].

*Step-up* [S1]:
- On each Contract Anniversary, if Contract Value > GWB, GWB resets to Contract
  Value under one of two methods fixed at election:
  - **Contract Anniversary Value** — the Contract Value on that anniversary; or
  - **Highest Quarterly Contract Value** — the highest of the *quarterly adjusted*
    Contract Values over the four most recent Contract Quarterly Anniversaries
    (including the anniversary itself). "Quarterly adjusted Contract Value" =
    Contract Value at that quarterly anniversary, **plus** premiums paid since (net
    of tax), **adjusted** for withdrawals since (dollar-for-dollar for non-excess,
    proportional for excess — same rule as for GWB).
- On step-up after the first withdrawal: `GAWA_new = max( GAWA% × GWB_new , GAWA_old )`.
- Bonus Base is set to `max(GWB_after_stepup, Bonus_Base_before)`.
- After a step-up the applicable GMWB charge rate may change (see §9).

*Bonus (roll-up)* [S1]:
- A bonus equal to `Bonus% × Bonus Base` is credited **to the GWB at the end of each
  Contract Year in the Bonus Period in which no withdrawals were taken**. Any
  withdrawal in a Contract Year, including automatic withdrawals and RMDs, kills the
  bonus for that year.
- Bonus Base adjustments: initial = GWB; on an excess withdrawal, Bonus Base is set
  to `min(GWB_after, Bonus_Base_before)`; otherwise no withdrawal adjustment; on
  premium, increases by net premium; on step-up, `max(GWB_after, Bonus_Base_before)`.
  Capped at $10 million.
- **Bonus Period**: begins on the endorsement effective date and **restarts** each
  time the Bonus Base increases due to a step-up, provided the step-up occurs on or
  before the Contract Anniversary immediately following the Designated Life's 80th
  birthday. It ends on the earlier of (i) the 10th Contract Anniversary following
  the endorsement effective date or the most recent Bonus-Base-increasing step-up,
  or (ii) the date Contract Value reaches zero.
- If the bonus is applied after the first withdrawal,
  `GAWA_new = max( GAWA% × GWB_new , GAWA_before_bonus )`.
- Applying the bonus does **not** change the Bonus Base or the GWB adjustment.

*GWB Adjustment* (a one-shot deferral reward) [S1]:
- **GWB Adjustment Date** = later of (i) the Contract Anniversary on or immediately
  following the Designated Life's 70th birthday, and (ii) the 12th Contract
  Anniversary following the endorsement effective date.
- Initial GWB adjustment = `GWB Adjustment % × GWB` at endorsement, capped at $10m.
- Premiums received before the 1st Contract Anniversary after the endorsement date
  increase it by `GWB Adjustment % × net premium`; later premiums increase it by
  the net premium itself.
- If **no** partial withdrawal has been taken on or before the GWB Adjustment Date,
  `GWB = max(GWB, GWB adjustment)` on that date and the provision terminates.
  Any withdrawal on or before that date voids it without value. Bonus Base is not
  adjusted.

*For Life Guarantee* [S1]:
- Effective at issue of the endorsement if the Designated Life is **59½ or older**;
  otherwise it turns on later.
- If not yet in effect, withdrawals that drive Contract Value to zero **void it
  permanently**.
- Voided on the death of the Designated Life (or first joint owner); a spousal
  beneficiary may continue the GMWB but **without** the For Life Guarantee, in which
  case the GWB is payable only until depleted, and the GWB adjustment provision is
  void.

*Contract Value = 0* [S1]:
- With For Life Guarantee in effect: annual payments of GAWA continue for the life
  of the Designated Life while the contract remains in the accumulation phase.
- Without it: payments of GAWA continue until the earlier of death or GWB depletion;
  the last payment cannot exceed remaining GWB.
- If the GAWA% has not yet been fixed, it is set at the percentage for the
  Designated Life's attained age when Contract Value hits zero.
- All other contract rights cease; no further premiums; all other endorsements
  terminate without value; no death benefit on subsequent death.

*Annuitization options created by the rider* [S1]:
- **Life Income of GAWA** — on the Latest Income Date with the For Life Guarantee in
  effect, fixed payments equal to the GAWA for life, with no death benefit.
- **Specified Period Income of the GAWA** — where the For Life Guarantee is not in
  effect (spousal continuation), number of years = GWB ÷ GAWA, GWB reduced by each
  payment, final payment truncated to the remaining GWB.
- **AutoGuard Fixed Payment Income Option** — same construction (years = GWB/GAWA)
  for the AutoGuard non-lifetime GMWB [S1].

*Charge increase / opt-out mechanic* [S1]:
- On **each fifth Contract Anniversary** the GMWB charge may be increased. The owner
  may opt out, but doing so forfeits the GWB bonus provision, the automatic step-up,
  the GWB adjustment and any other increases to GWB/GAWA; **no future premiums are
  allowed**; and the GAWA% is fixed with no future recalculation. The election is
  irrevocable. Increases can occur only every five years.

#### 6.2 Jackson current (April 27, 2026) rider parameters [S3]

Current annual charges when elected at issue (charge basis in the right column):

| Add-on benefit | Current annual charge | Charge basis |
|---|---|---|
| AutoGuard | 0.85% | GWB |
| Flex GMWB (Single) | Plus 1.70% / Core 1.25% / Value 0.30% | GWB |
| Flex GMWB (Joint) | Plus 2.00% / Core 1.55% / Value 0.60% | GWB |
| Flex Net GMWB (Single) | Core 1.40% / Value 0.45% | GWB |
| Flex Net GMWB (Joint) | Core 1.70% / Value 0.75% | GWB |
| Flex Strategic Income GMWB (Single) | 1.75% | GWB |
| Flex Strategic Income GMWB (Joint) | 1.85% | GWB |
| MarketGuard Stretch | 1.10% | GMWB Charge Base |
| Roll-up GMDB | 0.90% | GMDB Benefit Base |
| Highest Quarterly Anniversary Value GMDB | 0.30% | GMDB Benefit Base |
| Combination Roll-up + HQAV GMDB | 1.00% | GMDB Benefit Base |
| Flex DB (with Flex Value or Flex Core) | 0.80% | GMWB Death Benefit |

Flex GMWB (Single), current benefit-option parameters [S3]:

| Parameter | Value | Core | Plus |
|---|---|---|---|
| Bonus | 5% | 6% | 7% |
| Step-Up basis | Annual Contract Value | Annual Contract Value | Quarterly Contract Value |
| GWB Adjustment | 105% | 105% | 200% |
| GAWA% age 35–59 | 3.00% | 4.00% | 4.00% |
| GAWA% age 60–64 | 3.00% | 4.00% | 4.35% |
| GAWA% age 65–69 | 4.00% | 5.55% | 5.85% |
| GAWA% age 70–74 | 4.15% | 5.75% | 6.05% |
| GAWA% age 75–80 | 4.25% | 5.95% | 6.25% |
| GAWA% age 81+ | 4.50% | 6.20% | 6.50% |

Flex GMWB (Joint), current [S3]:

| Parameter | Value | Core | Plus |
|---|---|---|---|
| Bonus | 5% | 6% | 7% |
| Step-Up basis | Annual CV | Annual CV | Quarterly CV |
| GWB Adjustment | 105% | 105% | 200% |
| GAWA% 35–59 | 2.75% | 3.75% | 3.75% |
| GAWA% 60–64 | 2.75% | 3.75% | 4.10% |
| GAWA% 65–69 | 4.00% | 5.20% | 5.45% |
| GAWA% 70–74 | 4.15% | 5.40% | 5.65% |
| GAWA% 75–80 | 4.25% | 5.60% | 5.85% |
| GAWA% 81+ | 4.50% | 5.85% | 6.10% |

- Flex Net GMWB (Single/Joint) currently offers only Value and Core, with the same
  GAWA% grids as the corresponding Flex Value/Core columns, bonus 5%/6%, annual
  Contract Value step-up, GWB adjustment 105% [S3].
- **Flex Strategic Income GMWB** (an accelerated-then-standard payout design),
  bonus 5%, single life: Accelerated GAWA% 5.35% / 5.60% / 7.00% / 7.25% / 7.35% /
  7.60% and Standard GAWA% 3.00% / 3.00% / 4.00% / 4.00% / 4.00% / 4.00% for age
  bands 35–59, 60–64, 65–69, 70–74, 75–80, 81+. Joint life: Accelerated 5.00% /
  5.00% / 6.25% / 6.40% / 6.50% / 6.75%, Standard 2.75% / 2.75% / 4.00% × 4 [S3].
- **AutoGuard** (non-lifetime GMWB): GAWA% flat **5.00%** [S3].
- **MarketGuard Stretch** GAWA%: ages 0–54 4.50%, 55–59 5.00%, 60+ 5.50% [S3].
- **Flex DB** GMWB Death Benefit step-up percentage 100.00% [S3].
- **Roll-up GMDB** and **Combination Roll-up + HQAV GMDB** roll-up percentage:
  **6.00%** if age 69 or younger at election, **5.00%** if age 70 or older [S3].
- Riders elected **on a Contract Anniversary** (rather than at issue) get worse
  terms: Flex GMWB Core only, charge 1.45%, bonus 6%, annual CV step-up, GWB
  adjustment 105%, and lower GAWA% (single: 3.75/3.75/5.00/5.00/5.25/5.50;
  joint: 3.25/3.25/4.50/4.50/4.75/5.00) [S3].
- Aggregate: current minimum optional-benefit fee 0.30% (of GMDB Benefit Base) and
  maximum 2.00% (of GWB); lowest annual cost $1,701, highest $5,322 on $100,000 [S3].

#### 6.3 Jackson historical rate tables (useful for modelling in-force cohorts) [S1]

Appendix G, Flex GMWB (formerly LifeGuard Freedom Flex) GAWA percentages by
issue window — a compact illustration of GLWB rate de-risking and re-risking:

| Issue window | 35–64 (Max / Value) | 65–74 | 75–80 | 81+ |
|---|---|---|---|---|
| 2019-06-24 → 2020-12-13 | 4.00% / 3.00% | 5.00% / 4.00% | 5.50% / 4.50% | 6.00% / 5.00% |
| 2020-12-14 → 2021-02-28 | 3.75% / 3.00% | 4.75% / 4.00% | 5.25% / 4.50% | 5.75% / 5.00% |
| 2021-03-01 → 2022-03-06 | 3.50% / 3.00% | 4.75% / 4.00% | 5.00% / 4.50% | 5.25% / 5.00% |
| 2022-03-07 → 2023-08-27 | 3.75% / 3.25% | 5.00% / 4.25% | 5.25% / 4.75% | 5.50% / 5.25% |

From 2023-08-28 the age bands were re-cut to 35–59 / 60–64 / 65–69 / 70–74 / 75–80 /
81+ and the options renamed Value / Core / Plus; e.g. for Flex GMWBs issued
2024-11-11 → 2025-04-27 the Plus column is 4.00 / 4.25 / 5.50 / 5.60 / 5.80 / 6.00% [S1].

Appendix I (bonus percentages) [S1]:
- Flex GMWB bonus options were 5%/6%/7% (Bonus I/II/III) for 2019-06-24 → 2020-08-09,
  cut to 4%/5%/6% for 2020-08-10 → 2022-07-31, and restored to 5%/6%/7% from
  2022-08-01 → 2023-08-27.
- Flex Net GMWB bonus: 6% (2019-06-24 → 2020-08-09), 5% (2020-08-10 → 2022-07-31),
  6% (2022-08-01 → 2023-08-27).

Appendix H (GWB Adjustment percentages) [S1]:
- Flex GMWB: **200%** for 2019-06-24 → 2020-08-09; 170/180/190% by Bonus option for
  2020-08-10 → 2021-02-28; **105%** for 2021-03-01 → 2025-04-27.
- Flex Net GMWB: 200% then 180%, then discontinued.

Appendix F (historical charges) — illustrative of the charge/benefit-base link [S1]:
- LifeGuard Freedom Net GMWB issued before 2020-08-10: max 2.90% / current 1.45% /
  max single increase 0.25% with the Income Stream Max table; 1.60% / 0.80% / 0.15%
  with the Income Stream Value table. Charge basis **GWB**, charge frequency
  **quarterly**.
- Flex Net GMWB 2023-08-28 → 2024-11-10: Value max 1.70% current 0.60% (max single
  increase 0.15%); Core max 3.00% current 1.30% (max single increase 0.25%).
- Flex Net Joint 2023-08-28 → 2024-11-10: Joint Value max 2.30% current 0.90%
  (+0.20%); Joint Core max 3.00% current 1.60% (+0.25%).
- Flex Strategic Income Single 2023-08-28 → 2024-11-10: max 3.00% current 1.50%
  (+0.25%); Joint max 3.00% current 1.80% (+0.25%).
- LifeGuard Freedom Accelerator DB charge 0.70%; EarningsMax 0.35%; Four Year
  Withdrawal Charge Schedule 0.40%.
- Flex DB (pre-2021-11-08): max 1.60% / current 0.80% with the Max table; max 1.20% /
  current 0.60% with the Value table; charge basis **GMWB Death Benefit**, quarterly.

Appendix G also documents a **deferral-credit** design (LifeGuard Freedom
Accelerator GMWB, closed 2023-08-28): a starting GAWA% plus an annual **Deferral
Credit percentage** added to the GAWA% for each year of deferral — e.g. for issues
2022-03-07 → 2023-08-27, single life ages 45–49 3.50% starting GAWA with 0.10%
deferral credit, rising to ages 75–80 5.25% with 0.35% deferral credit [S1].

#### 6.4 Corebridge "Polaris Income Max" and "Polaris Income Plus Daily Flex" [S4][S5]

State variables: **Income Base**, **Income Credit Base** (Income Max only),
**Minimum Income Base** (Daily Flex only), **Maximum Annual Withdrawal Amount
(MAWA)**, **Protected Income Payment**, and an **Activation Date** chosen by the owner.

*Polaris Income Max* [S4]:
- Income Base initially = first Purchase Payment; increased by each subsequent
  Purchase Payment; reduced **proportionately** for any withdrawal before the
  Activation Date and for Excess Withdrawals after it.
- On each Benefit Year Anniversary **prior to the Activation Date**:
  `Income Base = max( Higher Anniversary Value , Income Base + Income Credit )`
  where Anniversary Value = contract value on that Benefit Year Anniversary and
  `Income Credit = Income Credit Percentage × Income Credit Base`.
- Income Credit Base = first Purchase Payment, increased by subsequent payments,
  reduced proportionately by pre-Activation withdrawals. **It is stepped up to a
  Higher Anniversary Value when the Income Base is, but it is not increased when an
  Income Credit is added** — so the roll-up is *simple on the ratchet base*, not
  compounding on prior credits [S4].
- The Income Credit is unavailable on and after the Activation Date [S4].
- Because Higher Anniversary Values are only determined on Benefit Year
  Anniversaries, intra-year highs are not captured [S4].

*Polaris Income Plus Daily Flex* [S4]:
- Income Base steps up **daily** before the Activation Date: "on any day that the
  contract value is greater than the Income Base on that day, the Income Base is
  stepped up to that value."
- A **Minimum Income Base** floor is applied on each Benefit Year Anniversary before
  Activation: `Minimum Income Base % × Purchase Payments` (payments proportionately
  reduced by any pre-Activation withdrawals). It stops growing at Activation.
- After Activation, the Income Base increases only on a Benefit Year Anniversary, by
  a **look-back** to the highest Step-up Value since the Activation Date (first
  look-back) or since the last Excess Withdrawal, and thereafter since the last
  Benefit Year Anniversary [S4].

*Withdrawals* [S4]:
- Before Activation: **any** withdrawal reduces the Income Base (and Income Credit
  Base) proportionately to the contract-value reduction.
- After Activation: `MAWA = Income Base × Maximum Annual Withdrawal Percentage`.
  Excess Withdrawal = amount exceeding MAWA in a Benefit Year; it reduces the Income
  Base in the same proportion the contract value is reduced by the Excess Withdrawal.
- RMD relief: for qualified contracts, if the RMD (computed on that contract using
  the Uniform Lifetime / Joint Life tables) exceeds MAWA, none of the RMD is treated
  as an Excess Withdrawal; favourable treatment is given to the greater of MAWA and
  RMD [S6].
- If contract value falls to zero after Activation while Income Base > 0, the
  **Protected Income Payment** = `Income Base at that moment × Protected Income
  Payment Percentage`, payable each Benefit Year until the death of the covered
  person(s) [S4].

*Investment requirements* — a hard risk control [S4]:
- Polaris Income Max: **20% Secure Value Account + 80% Variable Portfolios**
  (18 investment options).
- Polaris Income Plus Daily Flex: **10% Secure Value Account + 90%** either Asset
  Allocation Portfolios (37 options) or Build Your Own Allocation (76 options across
  12 asset classes).
- The Secure Value Account is a general-account fixed account with a one-year
  auto-renewing guarantee period, a contract-specified guaranteed minimum interest
  rate, and **no transfers out unless the living benefit is cancelled**. Withdrawals
  reduce it proportionately. The required SVA percentage never changes for the life
  of the contract [S4].
- Automatic quarterly rebalancing is mandatory (owners are auto-enrolled) [S4].

*Current rates, Polaris Income Max, effective May 1, 2026* [S5]:
- Initial annual fee rate **1.45%** for both one and two covered persons.
- **Income Credit Percentage 7.00%** (available only during the Income Credit Period).
- MAWA% / Protected Income Payment % (PIP%) by age on the Activation Date (for two
  covered persons, the **younger**):

| Covered persons / age band | Option 1 MAWA / PIP | Option 2 MAWA / PIP | Option 3 MAWA / PIP |
|---|---|---|---|
| One, 50–59 | 4.95% / 3.50%¹ | 5.05% / 3.50%¹ | 4.30% / 4.30% |
| One, 60–64 | 6.10% / 3.50%¹ | 6.10% / 3.50%¹ | 5.00% / 5.00% |
| One, 65–69 | 8.00% / 4.50% | 9.00% / 3.50% | 6.40% / 6.40% |
| One, 70–74 | 8.25% / 4.50% | 9.25% / 3.50% | 6.60% / 6.60% |
| One, 75+ | 8.35% / 4.50% | 9.35% / 3.50% | 6.80% / 6.80% |
| Two, 50–59 | 4.45% / 3.25%² | 4.55% / 3.25%² | 3.80% / 3.80% |
| Two, 60–64 | 5.60% / 3.25%² | 5.60% / 3.25%² | 4.50% / 4.50% |
| Two, 65–69 | 7.50% / 4.25% | 8.50% / 3.25% | 5.90% / 5.90% |
| Two, 70–74 | 7.75% / 4.25% | 8.75% / 3.25% | 6.10% / 6.10% |
| Two, 75+ | 7.85% / 4.25% | 8.85% / 3.25% | 6.30% / 6.30% |

¹ PIP% becomes 4.50% if income is activated before age 65 **and** the Income Base is
later increased to a new Higher Anniversary Value on/after the 65th birthday.
² Analogous, PIP% becomes 4.25%. [S5]

*Current rates, Polaris Income Plus Daily Flex, effective May 1, 2026* [S5]:
- Initial annual fee rate **1.45%** (one and two covered persons).
- **Minimum Income Base Percentage 6.00%** of each Purchase Payment, annually.
- MAWA% / PIP% (age bands start at 45 rather than 50):

| Covered persons / age band | Option 1 | Option 2 | Option 3 |
|---|---|---|---|
| One, 45–59 | 4.70% / 3.25%¹ | 4.80% / 3.25%¹ | 4.10% / 4.10% |
| One, 60–64 | 6.00% / 3.25%¹ | 6.00% / 3.25%¹ | 4.80% / 4.80% |
| One, 65–69 | 7.75% / 4.50% | 8.75% / 3.50% | 6.20% / 6.20% |
| One, 70–74 | 8.00% / 4.50% | 9.00% / 3.50% | 6.40% / 6.40% |
| One, 75+ | 8.10% / 4.50% | 9.15% / 3.50% | 6.60% / 6.60% |
| Two, 45–59 | 4.20% / 3.00%² | 4.30% / 3.00%² | 3.60% / 3.60% |
| Two, 60–64 | 5.50% / 3.00%² | 5.50% / 3.00%² | 4.30% / 4.30% |
| Two, 65–69 | 7.25% / 4.25% | 8.25% / 3.25% | 5.70% / 5.70% |
| Two, 70–74 | 7.50% / 4.25% | 8.50% / 3.25% | 5.90% / 5.90% |
| Two, 75+ | 7.60% / 4.25% | 8.65% / 3.25% | 6.10% / 6.10% |

*Living benefit fee — a genuine formula* [S4]:
- Fee is a percentage of the **Income Base**, deducted from contract value quarterly
  (first deduction at the end of the first quarter following election).
- Guaranteed maximum annual fee rate **2.50%**; minimum annual fee rate **0.60%**;
  the annualized rate may move by at most **±0.40% per Benefit Quarter** (i.e.
  0.10% per quarter) for Polaris Advisory contracts; **±0.25% per Benefit Quarter**
  (0.0625% per quarter) for Polaris Choice IV [S4][S6].
- The initial rate is guaranteed for the first Benefit Year; thereafter it resets
  quarterly by the **non-discretionary VIX formula**:

  ```
  Annual Fee Rate(quarter t)
      = Initial Annual Fee Rate + { 0.05% × [ QuarterlyAverage(Daily VIX²) / 33 − 10 ] }
  ```

  where `QuarterlyAverage(Daily VIX²)` is the average over the Benefit Quarter of
  the squared daily closing CBOE Volatility Index. The result is then (i) clipped to
  the ±0.40% (or ±0.25%) per-quarter movement band relative to the previous quarter's
  rate and (ii) clipped to the [0.60%, 2.50%] range. Quarterly fee rate = annual
  rate ÷ 4. [S4]
- Worked example from the prospectus (initial rate 1.45%): quarterly avg VIX² of
  204.42 → 1.45% + 0.05% × (204.42/33 − 10) = 1.45% + 0.05% × (−3.81) = **1.26%**;
  quarterly fee 0.3150%. A VIX² average of 602.30 gives an unclipped 1.86%, but the
  prior rate was 1.42%, so the +0.40% band caps it at **1.82%** [S4].
- A separate **Lifetime Income Option Change Fee** of up to 0.25% applies if the
  owner changes Income Option on the Activation Date; the sum of the living benefit
  fee and this fee cannot exceed the 2.50% maximum [S4].
- Legacy Polaris Choice IV riders (Polaris Income Plus / Income Builder / Income
  Plus Daily) carry maximum annual fee rates of **2.20%** (one covered person) and
  **2.70%** (two covered persons); the discontinued MarketLock For Life fee is a
  flat 0.70% (one) / 0.95% (two) [S6].
- Fee stops when contract value falls to zero [S4].

#### 6.5 Equitable "Guaranteed income benefit (GIB)" — a formula-rate GMIB [S7]

Architecture: only money allocated to the **Protection with Investment Performance
account** creates or increases the **GIB benefit base**. Money in the *Investment
Performance account*, the guaranteed interest option and non-designated Special DCA
does not [S7].

*Roll-up rates — tied to Treasuries* [S7]:
- **Annual Roll-up rate** — applies from the contract year of (and after) the first
  withdrawal from the Protection account. Variable, tied to the **Ten-Year
  Treasuries Formula Rate**:

  ```
  Ten-Year Treasuries Formula Rate (per calendar quarter)
      = average of daily 10-year U.S. Treasury note rates reported over the
        20 calendar days ending on the 15th day of the last month of the
        preceding calendar quarter
        + 1.00%,
        rounded to the nearest 0.10%
  ```
  Rates come from the Federal Reserve Board Constant Maturity Series. The Annual
  Roll-up rate is floored at **4%** and capped at **8%** in all contract years
  (Equitable reserves the right to declare above 8%).
- **Deferral bonus Roll-up rate** — applies in the contract years *before* the first
  withdrawal from the Protection account. Same formula but **+1.50%** instead of
  +1.00%, same 4%/8% floor and cap. Expected to run ~0.50% above the Annual
  Roll-up rate, though not guaranteed [S7].
- The deferral bonus **terminates permanently for the life of the contract** the
  first time a withdrawal is taken from the Protection account; the Annual Roll-up
  amount is credited instead from then on [S7].
- Prospectus examples: an unfloored Annual rate of 3.75% floors up to 4.00% while
  a Deferral bonus rate of 4.25% stays; an Annual rate of 7.75% stays while a
  Deferral bonus rate of 8.25% caps down to 8.00% [S7].
- **New business rates** apply for the first **two** contract years (one year for
  contracts issued before September 1, 2011); renewal rates apply from contract
  year 3. Renewal rates are never less than 4% or, if greater, the underlying
  formula rate [S7].
- **75-day rate lock-in**: if the initial contribution is received within 75 days of
  application signature, the initial rates are the **greater of** the rates in effect
  at application date and at issue date [S7].
- Contributions/transfers into the Protection account after the first day of a
  contract year receive the rates in effect as of the most recent contract date
  anniversary [S7].

*Annual Roll-up amount (credited on each contract date anniversary)* [S7]:
```
Annual Roll-up amount
  =  GIB/Roll-up benefit base at preceding anniversary × Annual Roll-up rate at start of year
   − withdrawals up to the Annual withdrawal amount           (dollar-for-dollar reduction)
   + pro-rated roll-up on contributions to the Protection VIOs during the year
   + pro-rated roll-up on transfers into the Protection VIOs during the year
   + pro-rated roll-up on Special DCA amounts designated for the Protection VIOs
```
Pro-rating is by days remaining in the contract year after the contribution/transfer.
On death, a pro-rated portion of the roll-up amount is added [S7].

The **Deferral bonus Roll-up amount** is the same formula with the Deferral bonus
rate and **without** the withdrawal deduction (since any withdrawal kills it) [S7].

*Annual withdrawal amount* [S7]:
```
Annual withdrawal amount = Annual Roll-up rate in effect on the first day of the
                           contract year × GIB benefit base as of the most recent
                           contract date anniversary
```
Withdrawals up to this amount do not reduce the GIB benefit base (they reduce the
roll-up amount dollar for dollar). Anything above it is an **Excess withdrawal**,
which reduces the GIB benefit base **pro rata** to the contract-value reduction.
A withdrawal from the Protection account in the first contract year in which it is
funded is automatically an Excess withdrawal [S7].

Worked example from the prospectus: with a GIB benefit base of $140,323, a $8,213
withdrawal against a $5,213 Annual withdrawal amount produces a $3,000 Excess; with
Protection account value of $100,000 that is 3%, so the base is reduced by
$140,323 × 3% = $4,209 to $136,114, and the $240 Annual Roll-up amount then brings
it to $136,354 on the next anniversary [S7].

*Lifetime GIB payments* [S7]:
- Begin at the **earliest** of (i) the contract year following the date the
  Protection account value falls to zero (other than by Excess withdrawal),
  (ii) the contract date anniversary following the owner's 95th birthday, and
  (iii) the contract's maturity date.
- Amount = **GIB benefit base × flat payout percentage**, where:

| Age (younger spouse if joint) | Single Life | Joint Life |
|---|---|---|
| Up to age 85 | 4% | 3.25% |
| Ages 86–94 | 5% | 4% |
| Age 95 | 6% | 4.50% |

- If the Protection account has **not** fallen to zero by maturity/age 95, the payment
  is the **greater of** (a) the Protection account value applied to the guaranteed or
  (if greater) current annuitization factors, and (b) GIB benefit base × the flat
  percentage above. Prospectus example: a male age 95 with a $100,000 GIB benefit
  base and $50,000 Protection account value receives the greater of $1,065/month
  (current annuitization factors on $50,000) and $500/month (6% × $100,000) → $1,065 [S7].
- **If the Protection account falls to zero because of an Excess withdrawal, the GIB
  is terminated with no payment and no supplementary contract, even if the GIB
  benefit base is greater than zero.** [S7]
- GIB annuity purchase factors are unisex, vary by age and payment frequency, and are
  "generally more conservative than the base contract annuity purchase factors" [S7].
- **Charge**: maximum **1.25%**, current **0.95%**, expressed as an annual percentage
  of the benefit base, deducted on each contract date anniversary [S7].

#### 6.6 Lincoln ProtectedPay® Select and i4LIFE® Advantage [S8]

State variables: **Protected Income Base**, **Enhancement Base**, **Enhancement
Value**, **Protected Annual Income (PAI)**, **Account Value Step-up**.

*Enhancement (roll-up)* [S8]:
- Current **Enhancement Rate 6%** (rate sheet dated May 1, 2026).
- **Enhancement Period**: a 10-year period beginning on the rider effective date.
  - Elections **before June 11, 2018** and **on/after November 28, 2022**: a single
    10-year Enhancement Period, no reset; Enhancements stop when it expires.
  - Elections **June 11, 2018 – November 27, 2022**: multiple Enhancement Periods,
    resetting immediately after an Account Value Step-up.
- An Enhancement and an Account Value Step-up **cannot both occur in the same year**;
  if the step-up is ≥ the Enhancement, the Enhancement is not applied.
- Additional Purchase Payments received within the **first 90 days** after the rider
  effective date are eligible for the Enhancement on the first Benefit Year
  anniversary; later payments are not eligible until the second anniversary.
  Prospectus example (5% Enhancement version): $100,000 initial + $15,000 on day 30
  → Protected Income Base ≥ $120,750 = $100,000 × 1.05 + $15,000 × 1.05 on the first
  anniversary; a further $10,000 on day 95 makes it ≥ $130,750 [S8].
- Neither Enhancement nor Step-up can raise the Protected Income Base above the
  **$10 million** maximum [S8].

*Account Value Step-up* (rider elections on/after November 28, 2022) [S8]:
The Protected Income Base increases to the highest Contract Value on each Benefit
Year anniversary if all of:
1. owner/annuitant (single) or owner/annuitant and Secondary Life (joint) are **under
   age 86**; and
2. the highest Contract Value on that anniversary — after deducting withdrawals
   (including the protected lifetime income fee and the account fee) and adding
   Purchase Payments made that day plus any Persistency Credits added that day — is
   greater than the Protected Income Base immediately prior to the anniversary; and
3. the Account Value Step-up exceeds the Enhancement Value for the same anniversary.

The step-up does not increase the Enhancement Base or Enhancement Value, and is
available even in years when a withdrawal occurred [S8]. (For elections **before**
November 28, 2022, the step-up increases *both* the Protected Income Base and the
Enhancement Base [S8].)

*Protected Annual Income rates (rate sheet, May 1, 2026)* [S8]:

Lincoln ProtectedPay Select Core® — one rate table:

| Age at first PAI withdrawal | Single Life | Joint Life |
|---|---|---|
| 59–64 | 4.40% | 4.15% |
| 65–69 | 6.05% | 5.50% |
| 70–74 | 6.25% | 5.70% |
| 75–79 | 6.45% | 5.90% |
| 80+ | 6.60% | 6.00% |

Lincoln ProtectedPay Select Plus® — **Table A applies while Contract Value > 0;
Table B applies once Contract Value reaches zero**, at which point the PAI amount is
immediately recalculated as `Protected Income Base × Table B rate`:

| Age | A Single | A Joint | B Single | B Joint |
|---|---|---|---|---|
| 59–64 | 5.60% | 5.10% | 3.00% | 3.00% |
| 65–69 | 7.55% | 7.00% | 4.50% | 4.25% |
| 70–74 | 7.80% | 7.30% | 4.50% | 4.25% |
| 75–79 | 7.90% | 7.40% | 4.50% | 4.25% |
| 80+ | 8.00% | 7.50% | 4.50% | 4.25% |

Lincoln ProtectedPay Select Max®:

| Age | A Single | A Joint | B Single | B Joint |
|---|---|---|---|---|
| 59–64 | 5.60% | 5.10% | 3.00% | 3.00% |
| 65–69 | 8.55% | 8.15% | 3.50% | 3.25% |
| 70–74 | 8.75% | 8.30% | 3.50% | 3.25% |
| 75–79 | 8.90% | 8.50% | 3.50% | 3.25% |
| 80+ | 9.00% | 8.60% | 3.50% | 3.25% |

The Table B rate is determined by the later of (a) the age when the first PAI
withdrawal occurred, or (b) the age as of the Valuation Date of the most recent
Account Value Step-up; if no withdrawals were taken before contract value reached
zero, current age (or the younger of the two lives) is used. The Core rate table
"thereafter may not change unless an Account Value Step-up occurs after reaching a
new age band." [S8]

*Charges* [S8]:
- ProtectedPay lifetime income suite: **guaranteed maximum annual charge 2.75%**
  (single and joint); **current initial annual charge 1.50% single / 1.60% joint**;
  fee is a percentage of the **Protected Income Base** (as increased for subsequent
  purchase payments, Account Value Step-ups and Enhancements, and decreased for
  Excess Withdrawals), deducted from Contract Value **quarterly**, first deduction on
  the three-month anniversary of the rider effective date.
- The fee **rate** may increase on every Account Value Step-up (owner may opt out of
  the step-up within 30 days of the Benefit Year anniversary; opting out reverses
  both the fee rate and the Protected Income Base to their pre-step-up levels,
  adjusted for purchase payments and Excess Withdrawals, for that year only).
- During the first ten Benefit Years an Enhancement increases the **dollar** fee but
  not the fee rate; after the tenth anniversary, if the Enhancement Period has
  renewed, the rate may increase with each Enhancement (opt-out available).
- The fee rate **also** increases, with **no opt-out**, once cumulative Purchase
  Payments after the first Benefit Year anniversary reach or exceed **$100,000**.
- Fee is prorated on rider termination (except death) and ceases when Contract Value
  reaches zero.
- Legacy guaranteed maximum annual charges: Lincoln Lifetime Income℠ Advantage 2.0
  (Managed Risk) elected on/after May 21, 2018 — 2.25% single / 2.45% joint; elected
  before that date — 2.00%/2.00% with current initial 1.25%/1.50%; Lincoln Market
  Select® Advantage and Lincoln Max 6 Select℠ Advantage — 2.25%/2.45%;
  4LATER® Select Advantage elected on/after November 28, 2022 — 2.75%/2.75% [S8].

*i4LIFE® Advantage with Guaranteed Income Benefit* — a payout-phase guarantee [S8]:
- i4LIFE® Advantage is a **variable annuity payout rider** giving variable, periodic
  "Regular Income Payments" for life, split into an **Access Period** (during which
  additional withdrawals and surrender remain possible) and a **Lifetime Income
  Period**. The optional Guaranteed Income Benefit provides a **minimum floor** under
  those Regular Income Payments.
- GIB amount = a specified percentage of Account Value or Protected Income Base,
  based on age at election:

| Age | Single Life GIB % | Joint Life GIB % |
|---|---|---|
| Under 40 | 2.25% | 2.00% |
| 40–54 | 3.00% | 2.50% |
| 55–58 | 3.25% | 2.75% |
| 59–64 | 4.00% | 3.50% |
| 65–69 | 5.00% | 4.50% |
| 70–79 | 5.25% | 4.75% |
| 80+ | 5.25% | 4.75% |

- Standalone i4LIFE® Advantage Select GIB current initial annual charge **1.55%
  single / 1.75% joint**, added to the base product charge (which already includes
  the M&E for the elected death benefit). For contract owners transitioning **from**
  ProtectedPay Select Core® or 4LATER® Select Advantage, the current initial annual
  charge is **1.50% single / 1.60% joint** [S8].
- On transition from a Prior Rider, the initial charge is a percentage of the
  **greater of** the carried-over Protected Income Base or the Account Value,
  deducted quarterly; on an automatic step-up of the GIB the dollar charge increases
  by (1) the same percentage as the GIB payment increase and (2) the percentage
  increase in the Prior Rider's current charge rate. If a withdrawal above the
  Regular Income Payment is taken, the dollar fee is reduced in proportion to the
  account-value reduction [S8].
- If Account Value is reduced to zero by additional withdrawals during the Access
  Period, i4LIFE® ends and the contract terminates [S8].

*4LATER® Advantage (discontinued, deferral-only design)* [S8]:
- Protected Income Base is automatically enhanced by **15% at the end of each 3-year
  Waiting Period** (adjusted for purchase payments and withdrawals) until i4LIFE® is
  elected, the rider terminates, or the Maximum Protected Income Base is reached.
- A "Future Protected Income Base" tracks what the base will become at the end of the
  Waiting Period: `115% × Protected Income Base`. Payments within 90 days of contract
  effective date get the full 15%; later payments get 15% **pro-rated for full years
  remaining** in the Waiting Period (prospectus example: `$100,000 × 115% +
  $10,000 × 100% + $10,000 × 15% × 1/3 = $125,500`).
- **Maximum Protected Income Base = 200% of the Protected Income Base on the rider
  effective date**, increased by 200% of any additional purchase payments, never
  exceeding $10 million across all Lincoln/affiliate contracts on the same life.
- Withdrawals reduce the Protected Income Base, Future Protected Income Base and
  Maximum Protected Income Base **proportionately** to the contract-value reduction.
- Resets to current contract value are permitted after each Waiting Period (annuitant
  must be under age 81); a reset restarts the Waiting Period and sets the Maximum
  Protected Income Base to 200% of the reset contract value [S8].

### 7. Guaranteed minimum death benefits

#### 7.1 Jackson [S1][S2][S3]

- **Basic Death Benefit** (included, no charge): greater of (i) Contract Value on the
  date all required documentation is received, and (ii) total Premiums paid since
  issue, reduced for prior withdrawals (including applicable charges and adjustments)
  **in the same proportion that the Contract Value was reduced** on the date of the
  withdrawal [S1][S2]. This is a *proportional* return-of-premium GMDB, not a
  dollar-for-dollar one.
- **Roll-up GMDB** — greatest of (a) Contract Value, (b) total Net Premiums, and
  (c) the GMDB Benefit Base, where the Benefit Base is:
  - premium paid net of premium taxes,
  - less withdrawal adjustments,
  - **compounded at an annual Roll-Up percentage from the Issue Date until the
    Contract Anniversary immediately preceding the oldest Covered Life's 81st
    birthday**.
  Withdrawal adjustment rule: withdrawals in a Contract Year up to `Roll-up% ×
  GMDB Benefit Base as of the previous Contract Anniversary (or Issue Date)` reduce
  the base **dollar-for-dollar**; the excess reduces it by
  `Benefit Base × (percentage reduction in Contract Value from the excess withdrawal)`
  — i.e. **dollar-for-dollar up to the roll-up rate, proportional above it**.
  All withdrawal adjustments are made **at the end of the Contract Year** and on
  receipt of due proof of death (after the GMDB charge is calculated). Premium
  adjustments occur at the time of payment, except premiums received in the first
  Contract Quarter which are treated as of the Issue Date [S1].
  Current Roll-Up percentage: **6.00%** if age 69 or younger at election, **5.00%**
  if age 70 or older [S3]. Charge: max 1.80%, current 0.90% of the GMDB Benefit Base
  [S2][S3]. Fixed Account Options are **not** available with this GMDB [S1].
- **Highest Quarterly Anniversary Value GMDB** — greater of Contract Value and the
  GMDB Benefit Base, the base being the greatest of the *adjusted quarterly Contract
  Values* at the endorsement effective date and each Contract Quarterly Anniversary
  **prior to the oldest Covered Life's 81st birthday**. Each adjusted quarterly value
  = Contract Value at that date, adjusted **proportionally** for subsequent
  withdrawals, plus subsequent premiums net of tax. Max charge 0.60%, current 0.30%
  [S1][S2][S3].
- **Combination Roll-up and HQAV GMDB** — greatest of Contract Value, total Net
  Premiums, and `max(Roll-up Component, HQAV Component)` with the two components
  defined exactly as above. Max charge 2.00%, current 1.00% [S1][S2][S3].
- **Flex DB** — a GMWB-linked death benefit equal to the Flex GMWB's GWB, **not
  reduced for allowed annual withdrawals**; charge assessed on the "GMWB Death
  Benefit". Max 1.60%, current 0.80%; step-up percentage 100.00%. Available only at
  issue with certain Flex GMWB benefit options, Designated Life 35–75 [S1][S2][S3].
- **All add-on death benefits**: the charge may be increased on **each fifth Contract
  Anniversary**; opting out of the increase permanently stops future roll-up / HQAV
  increases to the benefit base and prohibits future premium payments, while
  withdrawals continue to reduce the base [S1].
- Add-on death benefits **may provide value on or after the Income Date**: if the
  Income Date is the Latest Income Date, the death benefit becomes
  `GMDB Benefit Base on the Latest Income Date − Contract Value on that date`. If the
  Income Date is earlier, the endorsement terminates with no benefit [S1].
- **EarningsMax** (Earnings Protection Benefit; closed to new elections 2023-08-28):
  adds **40%** of contract earnings to the death benefit if issue age < 70, or **25%**
  if issue age 70–75 (electable at issue age ≤ 75). Earnings = Contract Value −
  Remaining Premium, and earnings are capped at **250% of remaining premiums**
  excluding premiums paid in the 12 months before death (other than the initial
  premium if death occurs in contract year 1). Historical charge 0.35% [S1].
- Ceiling ages: the Roll-up, HQAV and Combination GMDBs are available if the owner is
  **79 or younger** at issue; all roll-up/ratchet growth stops at the Contract
  Anniversary preceding the oldest Covered Life's **81st** birthday [S1].

#### 7.2 Corebridge [S4][S6]

- **Contract Value death benefit** (standard on the advisory contract) [S4].
- **Return of Purchase Payment** death benefit: greater of contract value and **Net
  Purchase Payments**, where Net Purchase Payments are reduced **in the same
  proportion by which the contract value is reduced** by each withdrawal. Charge
  **0.15%** of average daily ending net asset value in the Variable Portfolios [S4].
  Worked example: $250,000 Net Purchase Payments, contract value $300,000, $15,000
  withdrawal → 5% reduction → Net Purchase Payments $237,500; the same $23,000
  withdrawal on a $230,000 contract value is a 10% reduction and cuts Net Purchase
  Payments from $237,500 to $213,750 [S4].
- **Maximum Anniversary Value** death benefit: greatest of contract value, Net
  Purchase Payments, and the Maximum Anniversary Value (highest contract value locked
  in on any Benefit Year Anniversary), with both Net Purchase Payments and the
  Maximum Anniversary Value reduced proportionally by withdrawals. Charge **0.40%**
  on the advisory contract [S4]; **0.25%** on Polaris Choice IV [S6].
- Polaris Choice IV also offers a discontinued **Combination HV & Roll-Up Death
  Benefit** at **0.65%**; it is not available in Washington and cannot be combined
  with the Maximum Anniversary Value death benefit or a living benefit [S6].
- Spousal continuation: a **Continuation Contribution** equal to the excess of the
  death benefit over contract value is contributed to the contract [S4]. On
  continuation, the standard death benefit is `max(contract value, Continuation Net
  Purchase Payments)` if the continuing spouse is age 85 or younger, and contract
  value only if age 86 or older; the Maximum Anniversary Value death benefit is
  available if the continuing spouse is age 80 or younger, with anniversary ratchets
  only until the earlier of the continuing spouse's 83rd birthday or death [S6].

#### 7.3 Equitable [S7]

Three GMDBs, all applying **only to the Protection with Investment Performance
account**; the Investment Performance account pays its own account value:

- **Return of Principal** (standard, no charge): benefit base = contributions and
  transfers into the Protection variable investment options (directly or via a
  designated Special DCA), less a deduction for withdrawals from those options
  (including withdrawal charges).
- **Highest Anniversary Value** (0.25%): benefit base = the greater of contributions/
  transfers into the Protection VIOs, and the highest Protection account value on any
  contract date anniversary **up to the anniversary following the owner's (or older
  joint owner's) 85th birthday**, plus contributions/transfers since the most recent
  reset. Withdrawals reduce it **pro rata** (including applicable withdrawal charges).
- **"Greater of" death benefit** (max 1.10%, current 0.95% of benefit base): the
  greater of the **Roll-up to age 85 benefit base** and the Highest Anniversary Value
  benefit base. It can only be elected together with the GIB, and it is restricted by
  owner age.
  - The Roll-up to age 85 benefit base uses **exactly the same Annual Roll-up rate and
    Deferral bonus Roll-up rate as the GIB** (§6.5), and it and the GIB benefit base
    are **equal until age 85**.
  - It **automatically resets** to the Protection account value, if higher, on every
    contract date anniversary up to the anniversary following the owner's 85th
    birthday (or maturity, if earlier). Equitable reserves the right to raise the
    "Greater of" fee when a reset occurs; the owner may opt out of the reset (notice
    at least one business day before the anniversary) to avoid the fee increase, and
    may opt back in later.
  - On the contract date anniversary following age 85 the Roll-up to age 85 base
    (i) stops rolling up, (ii) stops resetting, and (iii) is reduced
    **dollar-for-dollar** by withdrawals up to the Annual withdrawal amount. By
    contrast the GIB benefit base keeps rolling up and resetting until age 95, so
    after 85 the two bases diverge.
  - Excess withdrawals reduce the Roll-up to age 85 base **pro rata**. A withdrawal
    from the Protection account in the first contract year it is funded is an Excess
    withdrawal. A withdrawal that drives the Protection account value to zero
    **terminates** the "Greater of" death benefit.
- Total contract death benefit = Investment Performance account value **plus** the
  greater of the Protection account value and the applicable GMDB benefit base [S7].

#### 7.4 Lincoln [S8]

- GMDB is priced **into the base contract expense**, not as a separate rider charge:
  Guarantee of Principal 1.55%, EGMDB 1.65%, 5% Step-up 1.80%, EEB without step-up
  1.85%, EEB with 5% step-up 1.90% (all as % of average Contract Value) [S8].
- **Estate Enhancement Benefit (EEB)** references Purchase Payments made into the
  contract prior to a withdrawal; it may not be terminated unless the contract is
  surrendered or is in the annuity payout period [S8].
- **Accumulated Benefit Enhancement (ABE℠)** (closed): a 1035-exchange enhancement.
  The ABE Enhancement Amount = excess of the prior contract's documented death
  benefit over the actual cash surrender value received, with the prior death benefit
  capped at the **lesser of 140% of the prior contract's cash value, or the prior
  contract's cash value plus $400,000**. If the surrender value received was less than
  95% of the documented cash value, the prior death benefit is reduced
  proportionately. If death occurs in the first Contract Year only **75%** of the
  Enhancement Amount is used. It goes to zero for owners added at age 76+ [S8].
- 4LATER® Select Advantage provides **no** death benefit on the Protected Income Base
  [S8].

### 8. Ancillary programs and account features

- **Dollar cost averaging**: Jackson offers standard DCA (from the one-year Fixed
  Account Option or any Investment Division) and **DCA+** (from a special DCA+ Fixed
  Account Option carrying enhanced declared rates), requiring $15,000 of Contract
  Value; both at no charge [S2]. Corebridge offers a DCA Program and DCA Fixed
  Accounts [S4]. Equitable offers "special DCA", "general DCA" and the "Investment
  Simplifier" (fixed-dollar or interest-sweep transfers out of the guaranteed
  interest option) [S7].
- **Rebalancing**: free at Jackson [S2]; **mandatory quarterly** at Corebridge when a
  living benefit is elected [S4]; Equitable offers Option I (among Investment
  Performance VIOs) and Option II (VIOs plus guaranteed interest option) at no charge,
  and the Protection account value **cannot** be rebalanced [S7].
- **Earnings Sweep** (Jackson, free): moves earnings from the one-year Fixed Account
  Option and the JNL/Dreyfus Government Money Market Investment Division; may only be
  added within 30 days of issue [S2].
- **Capital Protection Program** (Jackson, closed 2023-08-28): allocates enough
  premium to a selected Fixed Account Option so that the allocated amount equals total
  original premium at the end of the period — i.e. a self-funded GMAB-equivalent [S1].
- **Free look**: Jackson 10 days from delivery, refund of either the full amount paid
  with the application or premiums paid to the Fixed Account plus Separate Account
  Contract Value plus any non-asset-based fees deducted from premiums [S2]. Equitable
  10 days (longer where required by state law); some states require refund of the full
  contribution; IRA contracts returned within 7 days get a full contribution refund;
  Series CP® owners **forfeit the credit** on cancellation [S7].
- **Transfer limits**: Jackson 25 free transfers/Contract Year [S2]; Corebridge 15
  [S4][S6]; Equitable 12 (charge currently waived) [S7]; Lincoln "generally … no more
  than 12 transfers between investment options per Contract Year" [S8].
- **Minimum withdrawal amounts**: Jackson lesser of $500 or the entire Investment
  Division/Fixed Account Option balance; $50 under the Automatic Withdrawal Program
  [S2]. Equitable partial withdrawals must be at least $300 [S7].
- **Commutation**: Jackson income options with a specified period allow a beneficiary
  lump sum subject to a commutation fee, computed as the difference between (a) the
  present value of remaining guaranteed payments at the rate assumed in the initial
  payment and (b) their present value at a rate no more than **1.00% higher** [S1].

### 9. Charge-increase and rate-reset mechanics (a first-class model feature)

Three structurally different mechanisms appear across the four insurers, and a model
of this product must be able to represent at least one:

1. **Periodic discretionary reset with opt-out** (Jackson): rider charge may be raised
   on each fifth Contract Anniversary, subject to a stated maximum single increase
   (e.g. +0.25% for Core options, +0.15% for Value options) and an absolute maximum
   rate; opting out permanently forfeits step-ups, bonus and GWB adjustment and blocks
   further premiums [S1][S3].
2. **Step-up-triggered reset with opt-out** (Lincoln): the fee rate can change on every
   Account Value Step-up or (after year 10) Enhancement; opt-out reverses both the fee
   rate and the Protected Income Base to their pre-event levels for that year only;
   the rate also rises with no opt-out once cumulative purchase payments after year 1
   reach $100,000 [S8].
3. **Non-discretionary formula reset** (Corebridge): the VIX² formula in §6.4, floored
   at 0.60%, capped at 2.50%, with a ±0.40% (or ±0.25%) annualized band per quarter [S4][S6].
4. **Formula-driven benefit growth rate reset** (Equitable): the roll-up rate itself
   (not the fee) resets annually from the 3rd contract year off a 10-year Treasury
   formula, floored at 4% and capped at 8% [S7].

### 10. VM-21 — statutory reserve framework [R1]

**Scope** (VM-21 §2.A) [R1]:
- Variable deferred annuity contracts, whether or not they contain GMDBs or VAGLBs;
  variable immediate annuity contracts; any group annuity contract containing
  guarantees similar in nature to GMDBs/VAGLBs; and any other policy or contract with
  similar guarantees where there is no other explicit reserve requirement.
- Guidance note: "Current VAGLBs include GMABs, hybrid and traditional GMIBs, lifetime
  and non-lifetime GMWBs, and GPAFs."
- Excluded: contracts under VM-A-255 (Modified Guaranteed Annuities) — although VM-21
  **does** apply to in-scope contracts with subaccounts having MGA-like features
  (e.g. MVAs); and separate account contracts that guarantee an index and offer no
  GMDB or VAGLB.
- These requirements "constitute the Commissioners Annuity Reserve Valuation Method
  (CARVM) for all contracts encompassed by Section 2.A" [R1].
- **AG 43 relationship**: "Effectively, through reference in AG 43, the reserve
  requirements in VM-21 also apply to those contracts issued prior to Jan. 1, 2017,
  that would not otherwise be encompassed by the scope of VM-21." AG 43 and VM-21
  business may be aggregated into a single reserve calculation [R1].

**Effective date and phase-in** (§2.B) [R1]:
- Applies for valuation dates on or after **January 1, 2020**. Optional 36-month
  phase-in from that date (extendable to 7 years with domiciliary approval).
  `Reserve = D − (B − A) × C / B` where A = months elapsed since Dec 31, 2019,
  B = 36 (or the approved longer period), C = R1 − R2 (2020-basis reserve minus
  2019-basis reserve), D = the unadjusted reserve on the valuation date.
- §2.C adds a **separate 36-month economic scenario generator phase-in** starting
  January 1, 2026, using the same amortization formula with A measured from
  December 31, 2025 and B = 36 [R1].

**Aggregate reserve** (§3.A) [R1]:
```
Aggregate reserve = SR (Section 4)
                  + additional standard projection amount (Section 6)
                  + reserve for contracts using the Alternative Methodology (Section 7)
```
- The **SR** "for any group of contracts shall be determined as **CTE70** of the
  scenario reserves following the requirements of Section 4" (§3.D) [R1].
- All components are determined both **post-reinsurance-ceded and
  pre-reinsurance-ceded** (§3.B) [R1].
- **Alternative Methodology** (§3.E, §7) is available only for a group of variable
  deferred annuity contracts with **either no guaranteed benefits or only GMDBs** —
  i.e. never for a GLWB block [R1].

**Projection requirements** (§4.A) [R1]:
- Projection of accumulated deficiencies **ignores federal income tax** in both cash
  flows and discount rates.
- Must reflect insurance company expenses (including overhead and investment expense),
  fund expenses, contractual fees and charges, revenue-sharing income net of
  applicable expenses, and reinsurance/hedging cash flows.
- "Cash flows from any fixed account options also shall be included. **Any market
  value adjustment assessed on projected withdrawals or surrenders also shall be
  included** (whether or not the cash surrender value reflects market value
  adjustments)."
- Each variable subaccount must be mapped to an appropriately crafted **proxy fund**,
  normally a linear combination of recognized market indices, sub-indices or funds,
  reflecting efficient-frontier characteristics [R1].

**Additional standard projection amount — CTEPA method** (§6.A–6.B) [R1]:
```
Prescribed Projections Amount   = CTE70 (adjusted) computed with the Section 6.C
                                  prescribed assumptions substituted for company
                                  prudent estimates, with the scenario reserve for
                                  every scenario floored at aggregate CSV
Unbuffered ASPA                 = Prescribed Projections Amount − CTE70 (adjusted)
Buffer                          = Unfloored CTE70 (adjusted) − Unfloored CTE65 (adjusted)
                                  (Unfloored CTE65 averages the largest 35% instead of 30%)
Additional Standard Projection Amount = max( Unbuffered ASPA − Buffer , 0 )
```
[R1]

**Prescribed assumptions in the Standard Projection (§6.C)** [R1] — these are the
regulator's own view of policyholder behaviour and are the single most useful public
calibration anchor for a GLWB model:

*Maintenance expenses* (§6.C.2):
- If the company administers the contract: `$100 × 1.025^(valuation year − 2015)` per
  contract in the first projection year, inflating at 2.5% p.a., **plus** 7 bps of
  projected account value each year.
- If the company does not administer the contract:
  `$35 × 1.025^(valuation year − 2015)`, inflating at 2.5% p.a.

*Guarantee Actuarial Present Value (GAPV)* (§6.C.3) — the moneyness driver:
- Assume immediate/continued exercise if the benefit is currently exercisable;
  otherwise exercise at the earliest possible time.
- Once a GMWB is exercised, assume withdrawal of **100%** of the guaranteed maximum
  annual withdrawal amount each subsequent contract year.
- Account value growth is **0% net of all fees** chargeable to account value.
- Any market index is held constant.
- Mortality: **2012 IAM Basic Mortality Table, improved to Dec 31, 2017 using
  Projection Scale G2**, with no further improvement in the projection.
- Discount rate: the **10-year Treasury bond rate on the valuation date**.
- For hybrid GMIBs, two GAPVs are computed — an **Annuitization GAPV** (treating it as
  a traditional GMIB) and a **Withdrawal GAPV** (treating it as a lifetime GMWB).

*Partial withdrawals* (§6.C.4):
- Automatic withdrawals in excess of the GMWB guaranteed maximum annual withdrawal
  amount (or the GMIB dollar-for-dollar maximum) are cut back to that amount.
- Contracts with lifetime GMWBs / hybrid GMIBs that took a non-zero, non-excess
  withdrawal in the contract year preceding the valuation date: withdraw **90%** of
  the guaranteed annual withdrawal amount (or the GMIB dollar-for-dollar maximum)
  each year until account value hits zero.
- Other lifetime GMWB / hybrid GMIB contracts: no partial withdrawals until the
  initial withdrawal period given by the **Withdrawal Delay Cohort Method**, then 90%.
- Non-lifetime GMWBs: **70%** on the same pattern.
- Contracts with no minimum guaranteed benefits: **3.5% of account value** per year.

*Withdrawal Delay Cohort Method* (§6.C.5):
- Each contract is split into cohorts, each with a different initial withdrawal
  period, weighted by differences in a revised GAPV across candidate initial
  withdrawal ages. Contract account value, guarantee bases and other characteristics
  are allocated across cohorts by those weights.
- A **"never withdraw" cohort** is constructed with prescribed weight:
  **0.05** for tax-qualified GMWB contracts, **0.20** for non-qualified GMWB
  contracts, **0.15** for tax-qualified hybrid GMIB contracts and **0.40** for
  non-qualified hybrid GMIB contracts.
- For a contract whose attained age exceeds its issue age, cohorts with initial
  withdrawal ages below the attained age are discarded and the remaining weights
  re-scaled to sum to 1.

*In-the-moneyness (ITM) definition* (§6.C.6):
- GMDB: **75%** × (GMDB GAPV / account value).
- GMAB: **150%** × (GMAB GAPV / account value).
- Traditional GMIB and all GMWBs: **100%** × (GAPV / account value).
- Hybrid GMIB: 100% × (max(Annuitization GAPV, Withdrawal GAPV) / account value).

*Table 6.3 — Standard Table for Full Surrenders* (§6.C.6) [R1]:

| ITM | In surrender charge period (or policy years 1–3 if none) | First year after the surrender charge period | Subsequent years (or years 4+ if no surrender charge) |
|---|---|---|---|
| Under 50% | 4.0% | 25.0% | 15.0% |
| 50–75% | 3.0% | 18.0% | 10.0% |
| 75–100% | 2.5% | 12.0% | 7.0% |
| 100–125% | 2.5% | 8.0% | 4.5% |
| 125–150% | 2.5% | 6.0% | 3.0% |
| 150–175% | 2.0% | 5.0% | 2.0% |
| 175–200% | 2.0% | 4.5% | 1.5% |
| Over 200% | 2.0% | 4.0% | 1.0% |

Adjustments [R1]:
- Contracts with both a VAGLB and a GMDB use the **lower** of the two ITM-based rates.
- **For GMWB or hybrid GMIB contracts, in all contract years in which a withdrawal is
  projected, the table rate is multiplied by 60%.**
- The full surrender rate for a GMWB contract is **0% if the account value is zero**.
- GMAB contracts with no other living benefit: **50%** surrender in the contract year
  immediately following guarantee maturity.
- Contracts with no minimum guaranteed benefits: ITM = 0%, so the "<50%" row applies.
- Index-linked VA contracts with no guaranteed living benefits: 3% in the surrender
  charge period (or years 1–3), **60%** in the first year after it, 15% thereafter.
- Table 6.4 (simple 403(b) VA contracts) caps rates by attained age — e.g. 60–74:
  4.0% in the surrender charge period, 11.0% in the first year after, 8.0% thereafter.

*Annuitizations* (§6.C.7): the annuitization rate is **0% at all projection intervals
for contracts without a GMIB**; for GMIB contracts it is synonymous with the benefit
exercise rate and is 0% while the GMIB is not exercisable [R1].

**Alternative Methodology dynamic lapse formula** (§7.B.1) — the only closed-form
dynamic lapse formula in the Valuation Manual for VAs [R1]:
```
λ = MIN[ U , MAX[ L , 1 − M × ( GV/AV − D ) ] ],   with U = 1, L = 0.5, M = 1.25, D = 1.1
```
where GV is the GMDB and AV the account value on the valuation date; `λ` is a
**multiplier** on the prudent-estimate lapse rate. Present values are computed to
contract maturity at a **5.75%** discount rate [R1].

Prescribed net annualized fund returns for the CA and FE components (Table 7.1) [R1]:

| Asset class / fund | Net annualized return |
|---|---|
| Fixed Account | Guaranteed Rate |
| Money Market | 0% |
| Fixed Income (Bond) | 0% |
| Balanced | −1% |
| Diversified Equity | −2% |
| Diversified International Equity | −3% |
| Intermediate Risk Equity | −5% |
| Aggressive or Exotic Equity | −8% |

- Component **CA** = PV of the projected change in surrender charges plus an implied
  borrowing cost of **25 bps** at the beginning of each future period applied to the
  surrender charge at that time [R1].
- Component **FE** = PV of fixed dollar expenses less fixed dollar revenue through the
  earlier of maturity or 30 years, inflating from the current inflation rate (CIR,
  itself the greater of 3% and the rate in the company's most recent asset adequacy
  analysis) grading uniformly to an ultimate **3% p.a. in the 8th year** [R1].
- Component **GC** = `F × GV − G × AV × R`, with F, G and the linear coefficients
  β₁, β₂ for R being NAIC-published pre-calculated factors "reflecting a 65%
  confidence interval and ignoring federal income tax", interpolated over attained
  age, contract duration, ratio of account value to GMDB, and total asset-based
  charges; the margin ratio W is constrained to [0.2, 0.6] [R1].

**Contract holder behaviour principles** (§10.A) [R1]:
- "As the value of a product option increases, there is an increased likelihood that
  contract holders will behave in a manner that maximizes their financial interest
  (e.g., lower lapses, higher benefit utilization, etc.)."
- "Behavior formulas may have both rational and irrational components (irrational
  behavior is defined as situations where some contract holders may not always act in
  their best financial interest). The rational component should be dynamic."
- Living benefits are typically elective; death benefit options generally non-elective.

**Risks explicitly in scope** (§1.C) include separate-account fund performance, hedge
instrument basis/gap/price/parameter risk, "utilization risk associated with
guaranteed living benefits", annuitization risk, partial withdrawal and premium
payment risk, and disintermediation risk [R1].

### 11. C-3 Phase II risk-based capital [R3][R4]

Per NAIC Life RBC instruction **LR027** (Interest Rate Risk and Market Risk), a
7-step process applying to "all policies and contracts that have been valued
following the requirements of AG-43 or VM-21" [R3]:

1. Determine **CTE(98)** — "the numerical average of the **2 percent largest values**
   of the Scenario Reserves, as defined by Section 4 of VM-21", using the same process
   and methods as the reserve calculation.
2. Compute the C-3 RBC amount; floor at $0.
3. Compute C-3 RBC for Alternative Methodology business separately.
4. Sum, floor at zero. **Total Asset Requirement (TAR) = VM-21 reserve before any
   phase-in + C-3 RBC amount.**
5. Apply the reserve phase-in to C-3 RBC over the same period, if elected.
6. Apply smoothing if elected (regulator approval required to change the election or
   after a material change in the Clearly Defined Hedging Strategy).
7. Divide by `(1 − enacted maximum federal corporate income tax rate)` and split into
   interest-rate-risk (Line 35) and market-risk (Line 37) portions.

The RBC formula itself [R3]:
- Macro Tax Adjustment (MTA) basis:
  ```
  25% × ( (CTE(98) + Additional Standard Projection Amount − Statutory Reserve)
          × (1 − Federal Income Tax Rate)
        − (Statutory Reserve − Tax Reserve) × Federal Income Tax Rate )
  ```
  with the second term capped at the non-admitted deferred tax assets attributable to
  the same portfolio.
- Specific Tax Recognition (STR) basis:
  ```
  25% × ( CTE-After-Tax(98) + Additional Standard Projection Amount − Statutory Reserve )
  ```
- Under STR, a **Tax Adjustment** is added: approximately
  `corporate tax rate × f × (actual tax reserves − projected tax reserves at the start
  of the projection)`, where f = 1 minus the average, over the CTE(98) scenarios, of
  the ratio of contracts in force at the scenario's duration-to-worst to contracts in
  force at the start; **f is approximated as 0.5 under the Alternative Method** [R3].
- Phase-in: the excess of the 2019-restated C-3 RBC over the 2019 reported amount is
  amortized 2/3 at 12/31/2020 and 1/3 at 12/31/2021 for a 3-year phase-in [R3].

Context from the AAA practice note [R4]:
- "Variable annuity (VA) products have been subject to principle-based methodologies
  since **2005 for C-3 Phase 2 risk-based capital** and **2009 for reserves**."
- The 2020 revisions were targeted changes to "remove restrictions that limit the use
  of hedging in risk management" and "reduce non-economic reserve and capital
  requirements and volatility"; basic principles (company assumptions, margins,
  liability cash flow projection) were largely unchanged.
- The practice note records that the 2020 changes moved the C-3 Phase 2 stochastic
  measure to "**25% of CTE 98 instead of CTE 90** anytime stochastic projections
  apply" [R4].
- Acronym set relevant to modelling: CDHS, CSMP (Company-Specific Market Path), CTEPA,
  DIM (Direct Iteration Method), GAPV, GPVAD, MTA, NAER (Net Asset Earned Rate), SPA,
  STR [R4].
- The practice note explicitly does not cover state variations such as **New York
  Regulation 213** [R4].

### 12. The 2016–2020 NAIC VA framework reform [R2][R4]

- The NAIC "enacted its C3 Phase II initiative in **2006** to prescribe a set of
  standards for calculating Risk-Based Capital charges for market risk within VA
  products. C3 Phase II was followed in **2009** by Actuarial Guideline XLIII (AG 43),
  which established the reserving standards for VA products. The complex interplay of
  these standards challenged VA statutory capital management and, in part, motivated
  VA writers to seek capital management solutions via captive reinsurers." [R2]
- Oliver Wyman was engaged by the NAIC; a preliminary report was delivered September
  10, 2015; **QIS I** ran February–July 2016 with fifteen participating companies;
  **QIS II** (three cycles of testing, seventeen participants) reported to the
  Variable Annuities Issues Working Group with the executive summary dated
  February 12, 2018 [R2].
- Thematic findings driving the reform: (i) "presence of penalties for economic-based
  hedging" — companies hedging the full fair value of VA guarantees saw increases in
  both the level and the volatility of capital requirements because of misalignments
  between reserve and capital components; and (ii) "structural deficiencies in the
  Standard Scenario calculations" preventing alignment with the corresponding
  stochastic components [R2].
- Industry scale cited: "over $2 trillion in industry assets under management" [R2].
- The resulting framework became effective for valuation dates on or after
  January 1, 2020 (VM-21 §2.B) [R1].

### 13. Securities-law framework

**SEC Form N-4** [R6]:
- Reference copy version **effective September 23, 2024**, amended by Release
  No. IC-35273 (Registration for Index-Linked Annuities and Registered Market Value
  Adjustment Annuities; Amendments to Form N-4 …).
- Used by "all separate accounts organized as unit investment trusts and offering
  Contracts with Variable Options and all Insurance Companies that offer Contracts
  with Variable Options, Index-Linked Options, and/or Contract Adjustments."
- Part A item order (the source of the structure seen in every prospectus above):
  Item 1 Front and Back Cover Pages; **Item 2 Overview of the Contract**;
  **Item 3 Key Information**; **Item 4 Fee Table**; Item 5 Principal Risks of
  Investing in the Contract; Item 6 Description of Insurance Company, Registered
  Separate Account, and Investment Options; Item 7 Charges and Adjustments;
  Item 8 General Description of Contracts; … Parts B (SAI) and C.
- General Instruction C.3(a): Items 2, 3 and 4 must appear **in numerical order at the
  front of the prospectus**, preceded only by the cover page, a glossary, or a table
  of contents.
- An **Interactive Data File** (Inline XBRL) is required for information responsive to
  Items 2(b)(2), 2(d), 3, 4, 5, 6(a) instruction, 6(d), 6(e), 7(e), 10, 17, 26(c) or
  31A for contracts sold to new investors. (This is why the 2026 filings above carry
  XBRL member tags such as `PolarisIncomeMaxOneCoveredPersonMember`.)
- Plain-English requirements of Rule 421(d) apply to Part A.
- "A single prospectus may describe multiple Contracts that are essentially
  identical… a Contract that does not offer optional benefits would not be
  essentially identical to one that does for a charge."

**SEC Rule 498A, 17 CFR 230.498A** [R7]:
- Authorizes summary prospectuses for variable annuity contracts, variable life
  insurance contracts, RILAs and registered non-variable annuities; satisfies
  Securities Act §§ 5(b)(1) and 10(b) and Investment Company Act § 24(g).
- **Initial Summary Prospectus** (paragraph (b)) — for new purchases; may describe a
  single Contract (but more than one Class). Required headings, in order: "Important
  Information You Should Consider About the [Contract]"; "Overview of the [Contract]";
  "Benefits Available Under the [Contract]"; "Buying the [Contract]"; "Making
  Withdrawals: Accessing the Money in Your [Contract]"; "Additional Information About
  Fees"; and an appendix listing available investment options.
- **Updating Summary Prospectus** (paragraph (c)) — for existing owners and additional
  purchases; may describe one or more Contracts and Classes; must include "Updated
  Information About Your [Contract]" disclosing material changes since the prior
  prospectus.
- The retrieved text records an effective date of **July 24, 2024 (89 FR 60085)** for
  the current version [R7].
- S2 above is a live example of an Initial Summary Prospectus; the Jackson 497VPU
  filings observed in EDGAR are Updating Summary Prospectuses.

**FINRA Rule 2330 — Members' Responsibilities Regarding Deferred Variable
Annuities** [R8]:
- Governs recommended purchases and exchanges of deferred variable annuities and
  **initial subaccount allocations**; excludes reallocations after purchase and
  generally excludes tax-qualified employer-sponsored plans unless recommendations are
  made to individual participants.
- (b) Recommendation requirements: reasonable basis for suitability under Rule 2111;
  the customer must be reasonably informed of features including "surrender period and
  surrender charge; potential tax penalty if customers sell or redeem deferred
  variable annuities before reaching the age of **59½**"; the registered representative
  must document the suitability determination in writing.
- (c) Principal review: **"no later than seven business days after an office of
  supervisory jurisdiction of the member receives a complete and correct application
  package."**
- (d) Supervisory procedures: surveillance to identify inappropriate exchange rates;
  firms must monitor whether customers had exchanges "**within the preceding 36
  months**".
- (e) Training: documented programs for associated persons and supervisory principals.

### 14. Tax framework

**IRC § 72** [R9]:
- §72(b)(1) **exclusion ratio** — the portion of each annuity payment excluded from
  income is the ratio of "the investment in the contract (as of the annuity starting
  date)" to "the expected return under the contract (as of such date)".
- §72(c)(1) investment in the contract = premiums paid less prior tax-free
  distributions; §72(c)(2) requires subtracting the actuarial value of a refund
  feature.
- §72(e)(2)–(3) **income-first rule** for contracts purchased after **August 13, 1982**:
  pre-annuitization distributions are taxed to the extent of "income on the contract".
  §72(e)(4)(A) treats loans and pledges as taxable distributions; §72(e)(4)(C) taxes
  gain on transfers without adequate consideration.
- §72(q)(1) **10% additional tax** on the taxable portion of early distributions from
  a (non-qualified) annuity, with §72(q)(2) exceptions including age 59½, death,
  disability, substantially equal periodic payments, and amounts allocable to pre-1982
  investment.
- §72(s) **required distribution rules at death**: if the holder dies after annuity
  payments begin, remaining amounts must be distributed "at least as rapidly" as
  before; if before annuitization, generally within five years, with a §72(s)(2)
  exception permitting distribution over the beneficiary's lifetime if payments begin
  within one year of death.
- Direct product tie-ins: Jackson notes §72(t)/§72(q) withdrawals are **not** RMDs for
  GMWB guarantee-preservation purposes [S1]; and both Jackson and Corebridge apply
  special RMD treatment inside the GLWB [S1][S6].

**Treas. Reg. § 1.817-5 (§817(h) diversification)** [R10]:
- (b)(1) A segregated asset account is adequately diversified if no more than **55%**
  of the value of total assets is represented by any **one** investment, **70%** by any
  **two**, **80%** by any **three**, and **90%** by any **four**.
- (b)(2) Safe harbour: an account meeting the §851(b)(4) RIC diversification standards
  qualifies if "no more than 55% of the value of the total assets of the account is
  attributable to cash, cash items (including receivables), government securities, and
  securities of other regulated investment companies."
- (f) **Look-through**: a pro-rata portion of each asset of an underlying RIC,
  partnership or trust is treated as an asset of the segregated asset account — this
  is what makes the insurance-dedicated fund structure in every product above work.
- (c) Testing dates: the last day of each calendar quarter (March 31, June 30,
  September 30, December 31) **or within 30 days after** that day.

### 15. Actuarial standards of practice [R11][R12]

| ASOP | Full title | Effective date |
|---|---|---|
| No. 22 | Statements of Actuarial Opinion Based on Asset Adequacy Analysis for Life Insurance, Annuity, or Health Insurance Reserves and Other Liabilities | June 1, 2022 [R12] |
| No. 52 | Principle-Based Reserves for Life Products under the NAIC Valuation Manual | December 31, 2017 (adopted September 2017) [R11][R12] |
| No. 56 | Modeling | October 1, 2020 [R12] |

- ASOP No. 52's stated scope is actuaries calculating or reviewing reserves "for
  policies subject to **VM-20** requirements"; it references ASOP Nos. 7, 21, 22, 23,
  25 and 41 [R11]. **Note**: on the retrieved text, ASOP 52 is a VM-20 (life) standard,
  not a VM-21 (VA) standard — see Gaps.
- ASOP No. 56 (Modeling) is the governing standard for the projection model itself
  [R12].

### 16. Policyholder-behaviour experience sources [R5][R13]

**SOA Research Institute / LIMRA, 2022–2024 VA and RILA contract holder behavior
study** [R13]:
- Joint study of Variable Annuity and RILA behaviour for contracts with anniversaries
  in **2022, 2023 and 2024**.
- **Seventeen participating companies**, representing "approximately 48% of new
  premium for VAs and RILAs and 39% of general and separate account reserves."
- **11.5 million contracts exposed; $1.5 trillion in contract value exposed; over
  625,000 surrenders; four million contract withdrawals totalling $56.7 billion.**
- Deliverables include an in-depth analysis report and interactive data visualisation
  dashboards. The detailed report is a **paid data package** — the landing page alone
  was retrieved.

**American Academy of Actuaries, "Utilization Assumptions of Guaranteed Living
Benefits for Deferred Annuities", May 2024** [R5]:
- Prepared by the AAA **Life Experience Committee** (Donna Claire, chair); explicitly
  "not a promulgation of the Actuarial Standards Board … not an actuarial standard of
  practice … not binding upon any actuary."
- Key modelling framing: "Unlike other assumptions that are 'one-directional' …
  **GLB utilization can be inefficient … at both ends of the spectrum**", i.e.
  (a) delaying withdrawals or taking them too soon (before allowable, or before the end
  of a deferral period / bonus increase), and (b) taking less than the maximum allowed
  or taking excess withdrawals.
- On the never-utilize cohort: "Allowing companies to assume that there is a 'never
  utilize' cohort may **understate the reserves** required, especially when a company
  assumes its 'never utilize' cohort is a material proportion of its total business."
  Alternatives suggested: shift the never-utilize cohort into very-late-utilization
  cohorts (policy year 25 or 30, or age 95) rather than never.
- Empirical anchor cited: "the latest SOA Study found that **less than 5% of the FIA
  contractholders age 80 and above never utilized the GLB benefit**."
- The paper points modelers directly at **VM-21 Section 6.C.4 and 6.C.5** as the
  worked example of partial-withdrawal utilization modelling.
- Segmentation the paper recommends: contract provisions (GMDB-only vs VAGLB) and tax
  status (qualified vs non-qualified) — "contracts with VAGLBs and qualified contracts
  with or without VAGLBs have exhibited higher partial withdrawals utilization than
  other contracts."
- **Sample Utilization Table 1** (a non-qualified FIA with a 7%-for-10-years roll-up,
  payout as a percentage of account value by age at first withdrawal, age 95 the last
  election age):

| Age band | Yearly payment as % of account value at first withdrawal |
|---|---|
| 51–<56 | 5.00% |
| 56–<61 | 5.25% |
| 61–<66 | 5.50% |
| 66–<71 | 6.00% |
| 71–<76 | 6.50% |
| 76–<81 | 7.25% |
| 81–95 | 9.00% |
| 95 | 15.00% |

  with the simplifying assumption that all contractholders utilize when the payout
  rate increases and that **7% wait until age 95** [R5].
- **Sample Utilization Table 2** is a full age × years-waited matrix (rows = attained
  age 50 through 81+, columns = wait 0, 1, 2, …, 11 years, "Age 100", total 100).
  It embeds a **7% "wait until age 100"** tail at every age and large concentrations
  at the wait-10 column (e.g. 63% at age 50–53, 73% at age 55, 48% at 66–68, dropping
  to 0% at ages 78+). This is a directly reusable shape for a cohort-based GLWB
  utilization model [R5].

---

## Variations across insurers

1. **Where the guarantee sits — withdrawal phase vs payout phase vs a walled-off
   account.** Jackson [S1] and Corebridge [S4] use the mainstream design: one contract
   value, a shadow benefit base, guaranteed withdrawals while contract value > 0, and
   insurer-funded payments after it hits zero. Equitable [S7] instead bifurcates the
   contract into an *Investment Performance account* (no guarantees, no rider fee) and
   a *Protection with Investment Performance account* (funds the GIB and GMDB), and its
   living benefit is an **annuitization/supplementary-contract** guarantee rather than
   a withdrawal guarantee. Lincoln [S8] offers both: ProtectedPay® is a conventional
   GLWB, while i4LIFE® Advantage is a **variable annuitization payout rider with a
   guaranteed floor**, and 4LATER® is a pure deferral rider that must convert into
   i4LIFE® to pay anything.

2. **How the benefit base grows.** Four distinct roll-up mechanics appear:
   - *Bonus-with-Bonus-Base, restarting on step-up* (Jackson): 5–7% of a Bonus Base,
     only in years with no withdrawals, for a 10-year Bonus Period that **restarts on
     each Bonus-Base-increasing step-up** up to age 80, plus a one-shot GWB Adjustment
     of 105%–200% at the later of age 70 and duration 12 [S1][S3].
   - *Income Credit on a separate Income Credit Base* (Corebridge Income Max): 7.00% of
     an Income Credit Base that ratchets to Higher Anniversary Values but **is not
     increased by the credits themselves** — so credits are simple, not compound, on
     the ratcheted base [S4][S5].
   - *Formula-rate roll-up floored at 4% and capped at 8%* (Equitable): 10-year CMT
     +1.00% (or +1.50% before the first withdrawal), reset annually from contract
     year 3, with a 75-day rate lock at sale [S7].
   - *Flat enhancement with a 10-year window* (Lincoln): 6% Enhancement Rate, mutually
     exclusive with the Account Value Step-up in any year, over a 10-year Enhancement
     Period that does **not** reset for current (post-2022-11-28) elections [S8].

3. **Step-up frequency spans four orders of granularity**: annual anniversary
   (Jackson Value/Core, Lincoln, Corebridge Income Max), highest-of-four-quarters
   applied annually (Jackson Plus), and **daily** (Corebridge Polaris Income Plus
   Daily Flex) [S1][S3][S4][S8].

4. **Rider fee mechanics.** Fee bases are consistently the benefit base rather than
   account value (GWB [S3], Income Base [S4], GIB benefit base [S7], Protected Income
   Base [S8]), and all four assess **quarterly**. But the reset mechanism differs
   sharply: five-yearly discretionary with a forfeiting opt-out (Jackson [S1]),
   step-up-triggered with a reversing opt-out plus a no-opt-out $100,000-premium
   trigger (Lincoln [S8]), and a **non-discretionary VIX² formula** with a hard
   ±0.40%/quarter band and a [0.60%, 2.50%] corridor (Corebridge [S4]). The Corebridge
   design is the only one where the fee is a deterministic function of an observable
   market variable, which makes it the easiest to model faithfully and the most
   interesting to model at all.

5. **Investment-risk controls.** Corebridge imposes a mandatory general-account
   **Secure Value Account** allocation (20% with Income Max, 10% with Daily Flex) plus
   mandatory quarterly rebalancing [S4] — the strongest hard control in the set.
   Equitable achieves a similar effect by restricting which account funds guarantees
   and by "Custom Selection Rules" for the Protection account [S7]. Lincoln uses
   Investment Requirements (Appendix B) and managed-risk fund suites [S8]. Jackson
   restricts the Fixed Account rather than the funds: the Fixed Account Options are
   **unavailable** if the Roll-up GMDB, Combination GMDB, Flex DB or EarningsMax is
   elected [S1].

6. **Excess-withdrawal treatment is essentially universal**: dollar-for-dollar up to
   the guaranteed amount, then **pro-rata to the contract-value reduction** for the
   excess [S1][S4][S7][S8]. Jackson's disclosure is the most precise about ordering
   (non-excess portion dollar-for-dollar first, then proportional on the excess) and
   about the fact that withdrawal charges, MVAs and advisory fees all count toward the
   withdrawal for this purpose [S1].

7. **GMDB roll-up caps at 80/81/85**: Jackson stops all roll-up and ratchet growth at
   the Contract Anniversary preceding the oldest Covered Life's **81st** birthday
   [S1]; Equitable's Highest Anniversary Value ratchets to the anniversary following
   the **85th** birthday and the Roll-up to age 85 base stops there [S7]; Corebridge's
   Maximum Anniversary Value has no stated attained-age cutoff in the retrieved text
   but the spousal-continuation version stops at the continuing spouse's 83rd birthday
   [S6].

8. **Share-class structure.** Equitable is the clearest illustration of the classic
   B/L/C/bonus/advisory spectrum with the surrender-charge/M&E trade-off made explicit
   (Series B 1.30% total with a 7-year schedule; Series L 1.65% with a 4-year schedule;
   Series C 1.70% with no schedule; Series CP® 1.55% with a 4–5% credit and a 9-year
   schedule; Series ADV 0.65% with no schedule) [S7]. Corebridge shows the same trade
   across two separate registrations: Polaris Choice IV at 1.65% with a 4-year 8/7/6/5
   schedule [S6] versus Polaris Advisory at 0.40% with none [S4].

9. **Most representative design for a reference model.** The **Jackson Perspective II
   Flex GMWB with the Roll-up GMDB** is the best single chassis: it is the most
   contractually explicit, it exercises every mechanic a general VA model needs
   (proportional excess-withdrawal reduction, bonus with a restarting deferral window,
   both annual and highest-quarterly step-up bases, a benefit-base-assessed quarterly
   fee with a periodic reset and opt-out, contract-value-zero lifetime payments,
   rider-created annuitization options, a fixed-account MVA), and its ten years of
   published historical rate tables make in-force cohort modelling feasible. Use the
   **Corebridge VIX² fee formula** as the optional dynamic-fee variant and the
   **Equitable GIB** as the optional GMIB/annuitization variant.

---

## Gaps and caveats

- **No closed-form MVA factor was found.** None of the four prospectuses publishes an
  algebraic MVA/Interest Adjustment formula (e.g. `((1+i_o)/(1+i_n+spread))^(n/12) − 1`).
  Jackson describes the adjustment by rate relationship with a 0.25% dead band and a
  Fixed Account Minimum Value floor [S1]; Lincoln simply names the "Interest
  Adjustment" [S8]. The exact factor is normally in the **contract/specimen policy or
  the Statement of Additional Information**, neither of which was retrieved. Any
  formula written into a model would be [unverified].
- **Guaranteed annuity purchase rate tables were not obtained.** Equitable states GIB
  annuity purchase factors are unisex, age- and frequency-based, and "generally more
  conservative than the base contract annuity purchase factors" [S7], and gives one
  numeric data point (a male age 95 with $50,000 producing $1,065/month under *current*
  factors), but the guaranteed tables (mortality basis and interest rate) are in the
  contract, not the prospectus. Same for Jackson, Corebridge and Lincoln. Guaranteed
  purchase-rate bases such as "Annuity 2000 at 1.0%" are [unverified].
- **The Jackson Fixed Account minimum interest rate formula** is referenced ("reset
  according to the formula detailed above") but the formula's inputs (typically a
  5-year CMT-based nonforfeiture formula) were not extracted from the retrieved text.
  The Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805) was
  **not** retrieved, so the 1%–3% corridor and the 87.5%-of-premium minimum
  nonforfeiture amount are [unverified] here.
- **Lincoln share-class attribution is ambiguous.** Accession 0001104659-26-047599 is a
  ~20 MB bundle containing several rate sheets and several prospectuses. The fee table
  read (Annual Account Fee $35, base contract 1.55%–1.90%, transaction expenses
  consisting only of an Interest Adjustment) is internally consistent but cannot be
  attributed with certainty to a single named product among "Lincoln ChoicePlus
  Assurance (A-Share / B-Share / Bonus / C-Share / L-Share)". A surrender-charge
  schedule for the B-share Lincoln ChoicePlus Assurance was **not** located and is not
  stated anywhere above.
- **Corebridge Appendix I is mislabeled in the source.** In the retrieved 2026 Polaris
  Advisory prospectus, the section headed "APPENDIX I – LIVING BENEFIT RATES FOR
  CONTRACTS ISSUED ON OR AFTER MAY 1, 2023" repeats the Appendix C fee-formula
  examples rather than a rate table. Current rates were therefore taken from the
  separately filed Rate Sheet Supplement [S5], which is authoritative for new business.
- **SOA/LIMRA study detail is paywalled.** Only the landing page for the 2022–2024
  study was retrieved [R13]; no GLWB utilization rate by age/moneyness, and no
  empirical dynamic lapse curve, was obtained from a primary source. The only
  regulator-blessed numeric behaviour anchors in this file are the VM-21 §6.C
  prescribed tables [R1] and the AAA sample tables [R5], and the AAA tables are for a
  **non-qualified FIA**, not a VA — apply with care.
- **ASOP scope caution.** The ASB page retrieved for ASOP No. 52 states its scope as
  policies "subject to **VM-20** requirements" [R11]. VM-21 valuation work is therefore
  not obviously in ASOP 52's scope; the applicable standards for a VA principle-based
  valuation are more likely ASOP Nos. 7, 22, 23, 25, 41 and 56. No ASOP specific to
  VM-21 was located. Treat any claim that "ASOP 52 governs VM-21" as [unverified].
- **NAIC page 404.** `https://content.naic.org/cipr-topics/variable-annuities` returned
  the NAIC "we can't find what you're looking for" page (fetched_ok = false for the
  intended content). The VA framework narrative above therefore rests on the Oliver
  Wyman QIS II executive summary [R2] and the AAA practice note [R4] rather than an
  NAIC topic page.
- **efts.sec.gov and www.sec.gov reject plain fetches (HTTP 403).** All SEC content
  was retrieved with a declared User-Agent. This is a tooling caveat, not a data
  caveat — every SEC document listed as retrieved was read.
- **Rate sheets are volatile by design.** Every current-rate table in §6.2, §6.4 and
  §6.6 carries an explicit "can be superseded at any time" clause with a 10-day
  advance-filing commitment [S3][S5][S8]. Any model calibrated to these numbers should
  record the rate-sheet date (Jackson April 27, 2026; Corebridge May 1, 2026; Lincoln
  May 1, 2026) as a first-class assumption.
- **Fund expense ranges are as-of dates that lag.** Jackson's Annual Fund Expenses
  table in the April 2025 prospectus is stated "as of December 31, 2021" [S2]; treat
  the 0.52%–2.28% range as indicative rather than current.
- **Not covered here**: GMAB mechanics (no currently-sold GMAB was located in the four
  registrations read — Jackson's Capital Protection Program is the closest analogue and
  is closed [S1]); registered index-linked annuity (RILA) buffer/floor structures,
  which are in scope of VM-21 for surrender-rate purposes [R1] but are a separate
  product type; and New York Regulation 213 reserve variations [R4].
