# Fixed Indexed Annuity (FIA), including guaranteed lifetime withdrawal benefit riders — research notes (U.S.)

Access date for all citations: 2026-08-04.

Purpose: source library and extracted specifications to drive a reference liability
cash-flow projection model (lifelib/modelx style) for U.S. individual deferred fixed
indexed annuities (FIAs), including the guaranteed lifetime withdrawal benefit (GLWB)
/ guaranteed lifetime income benefit rider that is now attached to the majority of the
market.

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). Facts stated from general knowledge and not verified against a
retrieved document are tagged [unverified]. The S#/R# numbering in this file is
**local to this product** and independent of the cross-product library numbering used
in `_research/regulatory-actuarial.md`.

Note on retrieval method: several publishers serve product PDFs that the fetch tool
could not render to text. Those PDFs were downloaded and text-extracted locally with
`pypdf`; where that succeeded the document is marked Retrieved: YES. Where the fetch
itself failed (403 / DNS / password-protected viewer), the document is marked
Retrieved: NO and **no content from it is asserted anywhere in this file**.

---

## Primary sources

### S1. Athene Annuity and Life Company — "Athene Ascent<sup>SM</sup> Pro 10 — For income that lasts as long as your retirement." (consumer brochure, form 65178 (04/26/24))
- Publisher: Athene Annuity and Life Company, West Des Moines, IA (insurer's own
  consumer brochure; PDF mirrored by an authorized distributor site)
- Doc type: consumer product brochure (16 pages)
- URL fetched: https://annuityeducator.com/storage/59206/athene-ascent-pro-10.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Product: Athene Ascent Pro 10, single-premium deferred FIA with a **built-in**
  (automatically elected, charged) income rider — Athene Ascent Income Rider.
  Contract forms cited on back page: Ascent Pro GEN (09/15) NB, GEN10 (04/14);
  Ascent Income Rider IR1 (09/15), IR2 (09/15).
- Facts extracted:
  - Premium: minimum $10,000 ($5,000 in AK, AZ, CT, HI, ID, IL, LA, MN, MO, NH, NJ,
    OR, PA, TX, UT, WA); maximum $1,000,000 (larger with company approval).
  - Account structure: "Accumulated Value" = premium + interest − withdrawals −
    charges. Allocable to a **fixed strategy** (guaranteed annual rate declared each
    year, credited daily) and/or **indexed strategies**; "it's guaranteed that you
    will never earn less than 0% interest"; credits lock in and cannot be lost to
    later market declines. Reallocation permitted at the end of each interest
    crediting period. If a strategy is eliminated, its value is reallocated to the
    Fixed Strategy.
  - Death benefit: greater of Accumulated Value or Minimum Guaranteed Contract Value
    (MGCV).
  - Cash Surrender Value = greater of (i) Accumulated Value adjusted for applicable
    Withdrawal Charges and MVA, and (ii) the MGCV.
  - MGCV: "Ensures you will receive a minimum interest crediting rate on a percentage
    of your premium, adjusted for withdrawals, while the contract is in effect."
  - Free withdrawal: up to **10% of Accumulated Value each Contract Year, beginning
    in the first Contract Year**, free of Withdrawal Charge and MVA. RMDs count as
    part of the free withdrawal and are free of charge/MVA.
  - Minimum Interest Credit: at the end of the withdrawal charge period, if total
    interest credited to Accumulated Value is less than the Minimum Interest Credit,
    a one-time true-up credit equal to the difference is applied. The Minimum
    Interest Credit is a percentage of Initial Premium less withdrawals and charges.
  - Bailout: if Athene lowers the declared 1-Year Point-to-Point Annual Cap Rate
    below the contractual Bailout Cap Rate, the owner has full access to Accumulated
    Value free of any charges for up to 30 days after that Contract Anniversary.
  - Confinement Waiver: withdraw up to 100% of Accumulated Value, no Withdrawal
    Charge/MVA, if confined to a Qualified Care Facility ≥60 consecutive days after
    the first Contract Year; treated as an **Excess Withdrawal → terminates the
    income rider**.
  - Terminal Illness Waiver: up to 100% of Accumulated Value, no charge/MVA, if
    diagnosed with terminal illness expected to result in death within one year;
    available after the first Contract Anniversary; also an Excess Withdrawal that
    terminates the income rider.
  - MVA: applies to withdrawals in excess of the free amount and to full surrenders
    during the withdrawal charge period. "If interest rates have increased, stayed
    the same, or decreased by less than 0.25%, the MVA will be negative. If interest
    rates have decreased by more than 0.25%, the MVA will be positive." (i.e., a
    0.25% deadband is embedded in the MVA — see Extracted specifications.) MVA is not
    applicable in all states. Cross-reference given to Form 17653, "Understanding
    the MVA."
  - **Income rider (Ascent Income Rider)** — three phases: Growth (Accumulation),
    Income, Extended Income Guarantee.
    - Income Base = Initial Premium + Annual Simple Interest Credits + Interest
      Credits (if applicable) − Withdrawals. No cash/surrender value; cannot be
      taken as a lump sum.
    - Growth phase ends when income starts or **after 20 years, whichever is first**.
    - Two crediting options elected at issue and not changeable:
      (1) "Guaranteed Growth" — Income Base grows at a Guaranteed **Simple** Interest
      Rate only; (2) "Guaranteed Growth, Plus Interest Credits" — lower guaranteed
      simple rate **plus 100% of any Interest Credits added to the Accumulated
      Value** (a "stacking" design).
    - Withdrawals reduce the Income Base **proportionally** to the reduction in
      Accumulated Value (10% AV withdrawal → 10% Income Base reduction).
    - Lifetime Income Withdrawal = Income Base × Lifetime Income Withdrawal %.
    - Three payout options: Level Income; Earnings-Indexed Income (starts lower,
      increases by a percentage of interest credits); Inflation-Adjusted Income
      (starts lower, indexed to CPI-U, capped at 10% increase/yr, for up to 30 years
      or until AV = 0).
    - **Single-life guaranteed Lifetime Income Withdrawal Percentages** (S1 p.10):

      | Attained age | 50 | 55 | 60 | 65 | 66 | 67 | 68 | 69 | 70 | 75 | 80 | 85 | 90+ |
      |---|---|---|---|---|---|---|---|---|---|---|---|---|---|
      | Level | 5.70% | 6.00% | 6.55% | 7.25% | 7.35% | 7.45% | 7.55% | 7.70% | 8.05% | 8.90% | 9.65% | 10.55% | 12.15% |
      | Earnings-Indexed | 3.70% | 4.00% | 4.55% | 5.25% | 5.35% | 5.45% | 5.55% | 5.70% | 6.05% | 6.90% | 7.65% | 8.55% | 10.15% |
      | Inflation-Adjusted | 2.56% | 2.70% | 2.94% | 3.26% | 3.30% | 3.35% | 3.39% | 3.46% | 3.62% | 4.00% | 4.34% | 4.74% | 5.46% |

      Percentages grade by single year of age for ages 50–90.
    - **Joint life = single life percentage − 0.50%**, based on the attained age of
      the **younger** life.
    - Rider Charge: deducted **monthly** from Accumulated Value **and** from the MGCV
      (not deducted from MGCV in certain states); calculated as **a percentage of the
      Income Base**; initial annual rate declared in the contract.
    - Rider may be cancelled by the owner **on or after the 10th anniversary of the
      rider's effective date**.
    - Enhanced Income Benefit (income doubler): doubles the Lifetime Income
      Withdrawal for a maximum of **60 months** or until AV = 0, on confinement to a
      Qualified Care Facility for **180 out of 250 days** (90 out of 125 days in AK,
      AZ, CT, HI, ID, IL, LA, MN, MO, NH, NJ, OR, PA, UT, WA), after ≥1 year in
      force and while in the Income Phase. Not available in CA and MA. Ceases (and
      cannot start) once the Extended Income Guarantee Phase begins.
    - **AV exhaustion**: "If Lifetime Income Withdrawals (and not an Excess
      Withdrawal) reduce your Accumulated Value to zero, you'll continue to receive
      the Lifetime Income Withdrawal amount for the rest of your life" — the Extended
      Income Guarantee Phase. Level and Inflation-Adjusted options stay level in that
      phase; **Earnings-Indexed increases by 1% annually for the remainder of life**.
    - **Excess withdrawal / charge-driven exhaustion**: "If Excess Withdrawals,
      Withdrawal Charges or Market Value Adjustments (MVAs) reduce the contract's
      Accumulated Value to zero, your Lifetime Income Withdrawal Payments will stop
      and the rider will terminate."
    - RMDs exceeding the Lifetime Income Withdrawal are not Excess Withdrawals and
      do not reduce future Lifetime Income Withdrawals; before income starts an RMD
      reduces the Income Base pro rata.
    - Spousal continuation: in Accumulation Phase the rider continues; in Income or
      Extended Income Guarantee Phase the surviving spouse continues **only if the
      Joint Lifetime Income Withdrawal Option was selected**, otherwise the rider
      terminates. Non-spouse beneficiary → rider terminates on death.

### S2. Athene Annuity and Life Company — "Athene Ascent<sup>SM</sup> Pro 10 Bonus — Product Guide, Rates effective July 1, 2022" (form 65220 (07/01/22))
- Publisher: Athene Annuity and Life Company (insurer product guide / rate-and-spec
  sheet; PDF mirrored by a distributor site)
- Doc type: producer product guide + declared rate sheet (6 pages)
- URL fetched: https://iamsascend.com/wp-content/uploads/2023/01/Ascent-Pro-Fact-Sheet.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Facts extracted (rates are as of 07/01/2022 and are non-guaranteed):
  - **Declared index parameters, Ascent Pro 10 Bonus:**
    - BNP Paribas Multi Asset Diversified 5 Index (volatility-controlled): 2-Year
      No-Cap Point-to-Point participation rate **160%**; 1-Year No-Cap
      Point-to-Point participation rate **115%**.
    - Nasdaq FC Index (volatility-controlled, monthly performance cap embedded in
      index): 2-Year par **102%**; 1-Year par **67%**.
    - AI Powered US Equity Index (AiPEX, volatility-controlled): 2-Year par **130%**;
      1-Year par **97%**.
    - S&P 500 Daily Risk Control 5% Index TR: 1-Year No-Cap par **60%**.
    - S&P 500 (price index): 1-Year Point-to-Point **cap 5.25%**; **Bailout Cap Rate
      1.00%**.
    - Fixed Account with 1-Year Guarantee: **2.30%**.
  - Withdrawal Charge Duration: 10 years.
  - **Income Rider rates:** Annual Income Rider Charge Rate **1.00%**;
    Option 1 (Guaranteed Growth) Income Base simple interest **10.00% years 1–10,
    5.00% years 11–20**; Option 2 (Guaranteed Growth Plus Interest Credits) simple
    interest **5.00% years 1–10, 2.00% years 11–20**, plus a **200% Stacking
    Percentage** applied to interest credits.
  - **Income Base Bonus:** Option 1 = **25%**; Option 2 = **15%** (added to the
    Initial Income Base, i.e. Initial Income Base = Initial Premium × (1 + bonus)).
  - Ownership rules: IRA must be single ownership (joint payout available for
    spouses); nonqualified requires Owner = Annuitant, joint ownership only for
    spouses who are also joint annuitants; non-natural owner permitted.
  - Premium: single premium only; minimum $10,000 ($5,000 in AK, CT, HI, ID, MN, NJ,
    OR, PA, UT, WA); maximum $1,000,000.
  - **Premium Bonus 3%** (all three state groups) credited to Accumulated Value, with
    a **vesting schedule** that differs by state group:

      | Contract year | Group A (AL, AR, AZ, CO, DC, FL 35-64, GA, IA, IL, IN, KS, KY, LA, MA, MD, ME, MI, MO, MS, MT, NC, ND, NE, NH, NM, RI, SD, TN, VA, VT, WI, WV, WY) | Group B (AK, CT, DE, HI, ID, MN, NJ, NV, OH, OK, OR, PA, SC, TX, UT, WA) | Group C (FL ages 65-80) |
      |---|---|---|---|
      | 1 | 0% | 0% | 0% |
      | 2 | 0% | 10% | 0% |
      | 3 | 0% | 20% | 0% |
      | 4 | 0% | 30% | 0% |
      | 5 | 0% | 40% | 0% |
      | 6 | 0% | 50% | 0% |
      | 7 | 20% | 60% | 20% |
      | 8 | 40% | 70% | 40% |
      | 9 | 60% | 80% | 60% |
      | 10 | 80% | 90% | 80% |
      | 11+ | 100% | 100% | 100% |

      CA vesting: 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%.
  - **Withdrawal Charge schedules** (by the same state groups):

      | Contract year | Group A | Group B | Group C |
      |---|---|---|---|
      | 1 | 12% | 8.3% | 10% |
      | 2 | 12% | 8.0% | 10% |
      | 3 | 12% | 7.1% | 10% |
      | 4 | 11% | 6.2% | 10% |
      | 5 | 10% | 5.3% | 9% |
      | 6 | 9% | 4.4% | 8% |
      | 7 | 8% | 3.5% | 7% |
      | 8 | 7% | 2.6% | 6% |
      | 9 | 6% | 1.6% | 5% |
      | 10 | 4% | 0.9% | 4% |
      | 11+ | 0% | 0.0% | 0% |

      CA schedule: 8.2%, 7.7%, 6.6%, 5.6%, 4.5%, 3.4%, 2.3%, 1.2%, 0.1%, 0%.
  - Free withdrawal: 10% of Accumulated Value per year.
  - Death benefit: greater of (i) Accumulated Value or (ii) MGCV.
  - Income Base mechanics (contractual wording): "The Initial Income Base is equal to
    the Initial Premium plus Income Base bonus. On each Contract Anniversary, an
    interest credit will be calculated based on the **Premium minus Withdrawals**
    multiplied by an Income Base Guaranteed **Simple** Interest Rate." → the simple
    rollup base is premium net of withdrawals, not the rolled-up Income Base.
  - Rider charge base and deduction: "1.00% of the rider's Income Base and applies for
    the full contract term. The Rider Charge is deducted monthly from your annuity's
    Accumulated Value **and Minimum Guaranteed Contract Value**. Rider Charges are
    not deducted from the MGCV in certain states."
  - Minimum attained age for Lifetime Income Withdrawal Benefits: **50**.
  - Income Rider Termination Waiting Period: after the 10th Contract Year.
  - Issue ages: Ascent Pro 10 Bonus **35–80** (Group A/C states), **35–74** (Group B
    states); not available in some states.
  - MVA applies to the portion of a withdrawal/surrender exceeding the free amount
    during the Withdrawal Charge period; no MVA in MO.
  - Index disclosures: BNPP MAD 5 Index deducts a **servicing cost of 0.50% p.a.**
    calculated daily plus embedded rebalancing/replication costs; AiPEX deducts a
    **servicing cost of 0.50% p.a.** calculated daily; both apply volatility control
    that limits positive and negative index movement.

### S3. Allianz Life Insurance Company of North America — "Allianz Benefit Control® — Fixed Index Annuity" (consumer brochure, ABC-001 (R-11/2025))
- Publisher: Allianz Life Insurance Company of North America (official allianzlife.com URL)
- Doc type: consumer product brochure (16 pages)
- URL fetched: https://www.allianzlife.com/-/media/Files/Global/documents/2020/02/24/20/53/ABC-001.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Product: Allianz Benefit Control® FIA. MVA rider forms cited: C64237-MVA,
  R95581-MVA, ICC17C64237-MVA.
- Facts extracted:
  - Two-value architecture: **Accumulation Value (AV)** — lump-sum/surrender value,
    does **not** include any bonuses — and **Protected Income Value (PIV)** — the
    lifetime-withdrawal base, receives premium and interest bonuses, not available as
    a lump sum.
  - Issue age maximum **80**. Minimum purchase payment **$20,000**; maximum
    $1,000,000 without prior approval. Additional premium accepted for the **first 18
    contract months** in amounts between **$25 and $25,000** unless a larger amount
    is approved.
  - **Premium bonus: 25% of any premium paid in the first 18 months, credited to the
    PIV only** (0% to AV).
  - **Bonus Control benefit** — owner elects, each contract year, between two
    interest-allocation options:
    - Option 1 "Accelerated": **PIV interest bonus factor 250%**, **accumulation
      value interest factor 50%** (i.e. 4% index credit → 10% to PIV, 2% to AV).
    - Option 2 "Balanced": **PIV interest bonus factor 150%**, **accumulation value
      interest factor 100%** (4% → 6% to PIV, 4% to AV).
    - In AK, CT, HI, MD, NJ, OR, PA, UT, WA the complement of the AV interest factor
      is styled "Accumulation Value Interest Charge Percentage."
    - Once lifetime withdrawals begin, the contract **defaults to the Balanced (150%)
      option**.
  - Crediting: choice of fixed interest (declared at the beginning of each contract
    year, credited daily) and/or indexed allocations; **Index Lock** lets the owner
    lock an index value once per crediting period (or automatically via Auto Lock);
    Index Lock is not available on all allocation options.
  - **Allocation charge**: applies only to annual point-to-point and MY point-to-point
    allocations; deducted from the AV and in select states also from the guaranteed
    minimum value. Current 0%, **maximum 2.5%**, can change each crediting period.
  - Free/penalty-free withdrawals: in the contract year following the most recent
    premium payment, up to **10% of the contract's paid premium** per year, free of
    withdrawal charge and MVA. Free withdrawals reduce AV by the dollar amount and
    reduce PIV **by the same proportion** the AV was reduced. Index credit is still
    given on free withdrawals for the portion of the contract year the money remained
    in the index allocation.
  - **Surrender charge schedule** (start of contract year → percentage):
    1: 9.30%, 2: 9.30%, 3: 8.30%, 4: 7.30%, 5: 6.25%, 6: 5.25%, 7: 4.20%, 8: 3.15%,
    9: 2.10%, 10: 1.05%, thereafter 0%. Full AV available without penalty or MVA
    after 10 contract years.
  - MVA: may increase or decrease cash value; "can never cause your contract's cash
    value to be less than the guaranteed minimum value or more than the accumulation
    value." Direction table given: corporate bond yields at withdrawal **less than**
    at premium → CSV higher; **equal** → unaffected; **greater** → lower.
  - **Lifetime withdrawals** may begin any time after age **50**, on any monthly
    anniversary, even mid-year. The annual maximum is a percentage of PIV based on
    age at the most recent contract anniversary:

      | Age band | Single life % | Joint life % |
      |---|---|---|
      | 50–54 | 3.70% | 3.20% |
      | 55–59 | 4.20% | 3.70% |
      | 60–69 | 4.70% | 4.20% |
      | 70–79 | 5.20% | 4.70% |
      | 80 | 5.70% | 5.20% |

      Joint uses the age of the younger person.
  - **No explicit rider charge**: "since there is no additional charge for the PIV or
    AIM riders, there is no financial benefit to canceling them." (Cost is embedded
    in the AV interest factor / crediting parameters.)
  - **Cumulative withdrawal amount**: if the owner takes less than the annual maximum,
    the shortfall accumulates (without interest) and may be taken at any time. If the
    cumulative withdrawal amount ever equals or exceeds the AV, the Allianz Income
    Multiplier (AIM) rider terminates.
  - Income increases: every time an allocation earns interest, the lifetime withdrawal
    amount increases by the interest rate × the PIV interest bonus factor; increases
    are ratcheted (the amount can never decrease).
  - **Allianz Income Multiplier (AIM)** (income doubler): after **5 years** in force,
    withdraw up to **double** the annual maximum if unable to perform ≥2 of 6 ADLs
    (eating, bathing, dressing, toileting, transferring, continence) **or** confined
    to a qualified hospital / nursing / assisted-living facility for ≥**90 days in a
    consecutive 120-day period**. Doubling stops on depletion of AV, if cumulative
    withdrawal amount exceeds AV, or on recovery — but base lifetime income continues
    for life. Illustrated in the brochure as beginning on the **next contract
    anniversary** after qualification, and as reverting to half the doubled amount on
    recovery (the illustration shows base income continuing at the higher ratcheted
    level).
  - **AV exhaustion**: lifetime withdrawals "will continue even if you use up all the
    money you placed in the annuity"; the worked example shows AV fully distributed
    by age 75 with income continuing.
  - Annuitization: standard annuity options available after the 5th contract year;
    payments based on the **greater of AV or CSV — not the PIV**.
  - Death benefit: beneficiary chooses **either** the PIV taken over ≥5 years
    (limited to **250% of the accumulation value**; the PIV death benefit limit can
    vary by state) **or** a lump sum of the AV (or guaranteed minimum value or
    cumulative withdrawal amount, if greater).
  - RMDs from a qualified contract qualify as penalty-free withdrawals; PIV decreases
    by the same percentage as the AV.

### S4. Allianz Life Insurance Company of North America — "Allianz 222® Annuity — Guide to current rates as of 8/4/2026" (form M-7246 (R-8/2026))
- Publisher: Allianz Life Insurance Company of North America (official allianzlife.com URL)
- Doc type: declared-rate sheet (3 pages)
- URL fetched: https://www.allianzlife.com/what-we-offer/annuities/fixed-index-annuities/222/rates/-/media/Files/Allianz/PDFs/declared-rates/fixed-index-annuity/M-7246-Declared.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Facts extracted (rates current as of the access date, non-guaranteed):
  - Monthly sum with cap, S&P 500: **monthly cap 1.70%**.
  - Annual point-to-point with cap, S&P 500: **cap 4.50%**.
  - Annual point-to-point with participation rate: BlackRock iBLD Claria ER **100%**;
    Bloomberg US Dynamic Balance II ER **85%**; PIMCO Tactical Balanced ER **80%**.
  - 2-year MY point-to-point with participation rate (rate declared per year of the
    initial crediting period; the final-year rate is the one quoted for multi-year
    methods): Bloomberg US Dynamic Balance II ER 110% / 135%; PIMCO Tactical Balanced
    ER 105% / 130%; S&P 500 Futures Daily Risk Control 5% 120% / 145%.
  - 5-year MY point-to-point with participation rate (years 1–5): Bloomberg US
    Dynamic Balance II ER 145/165/185/205/**230%**; PIMCO Tactical Balanced ER
    145/165/185/205/**230%**; S&P 500 Futures Daily Risk Control 5%
    160/180/200/225/**250%**.
  - Fixed interest: **2.80%**.
  - **PIV bonus 45.00%**; **PIV interest bonus 150.00%**.
  - **PIV lifetime withdrawal percentages** (Allianz 222):

      | Age | Single | Joint |
      |---|---|---|
      | 60–69 | 5.00% | 4.50% |
      | 70–79 | 5.50% | 5.00% |
      | 80–100 | 6.00% | 5.50% |

  - **Guaranteed minimum (floor) index parameters** — these are the contractual
    guaranteed elements that bound the non-guaranteed scale:
    - minimum **monthly cap 0.50%** for monthly sum with cap;
    - minimum **annual cap 0.25%** for annual point-to-point with cap;
    - minimum **annual participation rate 5%** for annual point-to-point with a
      participation rate;
    - minimum **annual participation rate 5%** for MY 2-year and MY 5-year
      point-to-point with a participation rate;
    - minimum **fixed interest rate 0.10%**.
  - Caps, participation rates, interest rate and allocation charge are set at issue
    and guaranteed for the first crediting period; subsequent rates set on each
    contract anniversary.
  - **Allocation charge** (annual point-to-point, MY 2-year and MY 5-year
    point-to-point): deducted annually from the contract accumulation value **and the
    guaranteed minimum value (in most states)**; current 0%, **maximum 2.5%**. After
    issue it can only change when specified criteria are met — "the annual average
    U.S. 10-year Treasury rate for the calendar year, corporate bond downgrades for
    the calendar year, and investment-grade corporate bond defaults for the calendar
    year." Reference form M-7381.
  - PIV bonus, PIV interest bonus, lifetime withdrawal percentage table and maximum
    allocation charge are **set at issue and guaranteed for the life of the
    contract**.
  - Allianz 222 requires the contract be held **at least 10 contract years** before
    lifetime income withdrawals give access to the PIV including the bonuses.
  - 60-day rate lock on new/pending applications (higher of the rates available
    during the period). Participation rate on Allianz FIAs is 100% unless noted.
  - MVA rider forms: C54370-MVA, R95352-MVA, ICC16C54370-MVA.

### S5. American Equity Investment Life Insurance Company — "IncomeShield 10 with Optional Lifetime Income Benefit Rider" (consumer brochure, 01SB1164-10 10.16.19)
- Publisher: American Equity Investment Life Insurance Company (insurer brochure;
  the official media.american-equity.com URL failed DNS from this environment, so a
  distributor mirror of the same form number was used)
- Doc type: consumer product brochure (12 pages)
- URL fetched: https://www.annuityresources.com/assets/brochures/americanequityincomeshield10.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Product: IncomeShield 10 FIA with optional Lifetime Income Benefit Rider (LIBR).
  Forms: ICC17 BASE-IDX-B, ICC17 IDX-11-10, ICC19 E-MPTP, ICC19 E-PTPC, ICC19 E-PTPR,
  **ICC16 R-MVA**, ICC17 R-LIBR-FCP, ICC17 R-LIBR-FSP, ICC17 R-LIBR-W-FSP,
  ICC17 R-LIBR-W-FCP, ICC19 R-NCR, ICC19 R-TIR.
- Facts extracted:
  - **Premium Bonus 7%** on all premium received in the first contract year, applied
    to Contract Value on the date received and allocated the same way as the premium.
  - **Premium Bonus vesting schedule**: contract years 1–11+ = 0, 10, 20, 30, 40, 50,
    60, 70, 80, 90, 100%. Vested amount cannot be forfeited by a Free Withdrawal. On
    death, **100% of the Premium Bonus vests immediately**.
  - **Surrender Charge schedule (issue ages 18–80)**: years 1–11+ = 9.1, 9, 8, 7, 6,
    5, 4, 3, 2, 1, 0 %.
  - **Minimum Guaranteed Surrender Value (MGSV)**: "At no time will the Cash Surrender
    Value of the contract be less than **87.5% of premium received, less any
    withdrawals, accumulated at the minimum guaranteed interest rate**."
  - Free Withdrawal: after the first contract year, up to **10% of Contract Value**
    per year without expense.
  - Allocation rules: initial premium allocable in any combination to fixed interest
    or index strategies; **subsequent premiums automatically go to the fixed interest
    strategy**; reallocation on contract anniversary subject to a **$1,000 minimum
    per value** and a **minimum transfer of 10% of contract value** to select a new
    value.
  - MVA: the product contains an MVA rider; MVA may increase or decrease a withdrawal
    in excess of the Free Withdrawal amount or the surrender value; does **not** apply
    to Free Withdrawals, death benefit, MGSV, or distributions after the surrender
    charge period. "In general, as the MVA Index increases, Cash Surrender Values
    decrease."
  - Nursing Care Rider: automatic for owners **under age 75 at issue**; after the
    first contract year, a **one-time** withdrawal of up to 100% of contract value if
    confined to a qualified nursing care facility for a minimum of **90 days**;
    confinement must begin after issue; no withdrawal/surrender charges or MVA.
  - Terminal Illness Rider: automatic for owners under age 75 at issue; after the
    first contract year, one-time withdrawal up to 100% of contract value on terminal
    illness diagnosis occurring after issue; no charges or MVA.
  - Death Benefit: greater of Contract Value or MGSV; paid with no surrender charges
    plus 100% bonus vesting.
  - **LIBR** (optional rider, issue ages **50–80**): income measured by the **Income
    Account Value (IAV)**, credited at the **IAV Rate** until the earlier of income
    commencement or the end of the Accumulation Period. Five rider options:
    - Option 1: IAV Rate declared at issue, guaranteed **15 years**, **compound**
      interest, **no rider fee**.
    - Option 2: IAV Rate declared at issue, guaranteed **7 years**, **simple**
      interest.
    - Option 3: initial IAV Rate declared at issue, guaranteed **10 years**, then
      never below the Minimum Guaranteed IAV Rate for the rest of the Accumulation
      Period; **compound** interest.
    - Option 4: as Option 2 (7-year guarantee, simple) **plus the Wellbeing Benefit**.
    - Option 5: as Option 3 (10-year guarantee, compound) **plus the Wellbeing
      Benefit**.
    - Wellbeing Benefit: increases income by an income payment factor for **up to five
      years** if the owner (or spouse) cannot perform multiple ADLs; **not
      confinement-driven** (available to those receiving home care); **two-year
      waiting period**.
  - Rider Fee: "deducted from the **Contract Value** each year as long as the rider is
    attached" (the fee base is not stated in this brochure).
  - **Payout Factors table** (percentage of IAV; single life varies by **sex** and
    age, joint by age of the younger):

      | Age | Single F | Single M | Joint | Age | Single F | Single M | Joint |
      |---|---|---|---|---|---|---|---|
      | 50 | 2.90% | 3.08% | 2.64% | 65 | 4.30% | 4.48% | 3.78% |
      | 51 | 2.99% | 3.16% | 2.73% | 66 | 4.39% | 4.57% | 3.83% |
      | 52 | 3.08% | 3.25% | 2.83% | 67 | 4.47% | 4.66% | 3.88% |
      | 53 | 3.16% | 3.34% | 2.93% | 68 | 4.54% | 4.75% | 3.94% |
      | 54 | 3.25% | 3.43% | 3.02% | 69 | 4.62% | 4.84% | 3.99% |
      | 55 | 3.34% | 3.52% | 3.12% | 70 | 4.70% | 4.92% | 4.04% |
      | 56 | 3.44% | 3.61% | 3.22% | 71 | 4.77% | 5.00% | 4.09% |
      | 57 | 3.53% | 3.71% | 3.30% | 72 | 4.84% | 5.08% | 4.13% |
      | 58 | 3.63% | 3.81% | 3.38% | 73 | 4.90% | 5.16% | 4.17% |
      | 59 | 3.73% | 3.90% | 3.45% | 74 | 4.96% | 5.24% | 4.20% |
      | 60 | 3.82% | 4.00% | 3.52% | 75 | 5.02% | 5.32% | 4.24% |
      | 61 | 3.92% | 4.10% | 3.57% | 76 | 5.08% | 5.39% | 4.27% |
      | 62 | 4.02% | 4.19% | 3.62% | 77 | 5.14% | 5.46% | 4.31% |
      | 63 | 4.11% | 4.29% | 3.67% | 78 | 5.20% | 5.53% | 4.35% |
      | 64 | 4.21% | 4.39% | 3.73% | 79 | 5.27% | 5.60% | 4.40% |
      |   |   |   |   | 80 | 5.32% | 5.67% | 4.44% |

      Montana: gender-neutral, both sexes use female factors; joint factors unchanged.
  - **IAV step-up to Contract Value at income start**: "If, on the day before income
    payments are to begin, the Contract Value is greater than the IAV, American Equity
    will increase the IAV to equal the Contract Value."
  - Income may begin **30 days or one year after issue depending on the rider
    option**; joint life requires both spouses ≥50 and pays until the death of the
    survivor subject to spousal continuation.
  - Excess withdrawals after income has started reduce future income payments and the
    IAV **pro rata** (5% of Contract Value withdrawn → 5% reduction in future income).
  - **AV exhaustion by excess withdrawal**: "Should excess withdrawals reduce the
    Contract Value to zero, the IAV will also be reduced to zero, and the contract as
    well as the rider will be considered Surrendered. Any remaining income payments
    would also terminate."
  - LIBR terminates on the earliest of written request, contract termination,
    annuitization, or change of owner; cannot be reinstated.

### S6. Midland National Life Insurance Company — "IndexMax ADV® 5 Fixed index annuity — Annuity disclosure statement" (form 32908Y-1, 8-24)
- Publisher: Midland National Life Insurance Company (Sammons Financial) — official
  midlandnational.com document library URL
- Doc type: **signed annuity disclosure statement** (12-page form; the most
  contractually precise consumer-facing document short of the contract itself)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32908Y+IndexMax+ADV+5+disclosure/e1927985-0db5-24cb-257c-61b46011487e
- Retrieved: YES (full PDF text-extracted locally)
- Product: IndexMax ADV 5, single-premium deferred FIA (fee-based / RIA channel).
  Forms AS203A/ICC20-AS203A (contract); AR386A/ICC20-AR386A, AR387A/ICC20-AR387A,
  AR388A/ICC20-AR388A, AR360A/ICC19-AR360A (riders/endorsements).
- Facts extracted:
  - "The IndexMax ADV 5 is **not a registered security** and does not directly
    participate in stock or equity investments. Index returns do not include
    dividends." 30-day free look (refund of premium less withdrawals).
  - Single premium only; no additional premium after issue.
  - **Term structure**: a five-year initial term, then an automatic **five-year
    re-entry term** (unless the owner opts out within 30 days of the end of the
    initial term), then automatic **one-year terms**. The re-entry term carries a
    **new surrender charge period and new MVA period**, and resets starting index
    values and the Interest Credit Basis. 30-day window at the end of the initial
    term to surrender/partially surrender free of surrender charge and MVA.
  - Fixed account: rate declared at issue for the initial term, at term start for the
    re-entry term, then annually. **Minimum guaranteed fixed account interest rate
    0.25%.**
  - Crediting method: **"Term participation with annual performance credits"** —
    - **Annual performance credit (APC)**: applies on the anniversaries of the first
      four years of a five-year term and on each anniversary of a one-year term; APC
      rate set at term start; **minimum guaranteed APC rate 0.25%**. APC applies only
      if the index value at the end of the contract year exceeds the value at the
      beginning; otherwise zero. Credit = APC rate × Interest Credit Basis.
    - **Term performance credit (TPC)**: applies only at the end of a term longer than
      one year (i.e. year 5 of each five-year term); no APC that year. **Minimum
      participation rate for the re-entry term's TPC is 10%.** TPC applies only if the
      **average monthly index value in the final year of the term** exceeds the index
      value on the index start date; credit = participation rate × percentage change ×
      Interest Credit Basis.
    - **Interest Credit Basis** = Accumulation Value at the beginning of the term less
      withdrawals from that index account. Advisory fees taken pro rata out of index
      accounts do **not** reduce the Interest Credit Basis.
    - Worked example (S5 p.5): $20,000 premium, beginning index 1000, participation
      rate 100%, APC rate 1%. APC = 1% × $20,000 = $200 in each year the index rose.
      Year-5 monthly average 1365 → term monthly average index return
      (1365 − 1000)/1000 = 36.5%; TPC = 100% × 36.5% × $20,000 = $7,300.
  - Penalty-free withdrawal: **10% of beginning-of-year accumulation value**, in any
    contract year beginning in the **second** contract year.
  - RMDs: by current company practice, RMDs based solely on the accumulation value may
    be withdrawn without surrender charge or MVA even if they exceed the penalty-free
    amount ("current company practice" is explicitly **not a contractual guarantee**).
  - Advisory fee: owner may authorize up to **1.5% of accumulation value annually** to
    the RIA/IAR; treated as a partial surrender.
  - **Surrender charge schedule**:

      | Year | Initial term | Re-entry term | Re-entry (CA) | Re-entry (DE) |
      |---|---|---|---|---|
      | 1 | 6.0% | 3.0% | 3.0% | 3.0% |
      | 2 | 6.0% | 3.0% | 2.35% | 3.0% |
      | 3 | 5.0% | 2.5% | 1.4% | 2.5% |
      | 4 | 4.0% | 2.0% | 0.45% | 1.95% |
      | 5 | 3.0% | 1.5% | 0.44%* | 0.95% |

      *CA: the surrender charge percentage in the 10th contract year decreases 0.04%
      monthly until it reaches 0.00%.
  - **MVA formula (verbatim)**:
    `Market value adjustment = (i0 − it) × (T)`
    where `i0` = index value of the MVA external index on the **start date of the
    five-year term**; `it` = index value of the MVA external index at the time of the
    surrender (full or partial); `T` = "number of days from the date of the surrender
    to the end of the current Contract Year divided by 365, plus whole number of years
    remaining in the market value adjustment period". The MVA external index is
    **Barclay's US Credit Index**. The MVA is applied by multiplying the portion of
    the withdrawal exceeding the penalty-free amount, **before** reduction for any
    surrender charge, by that factor.
  - **MVA cap/collar (verbatim structure)**: when positive, the MVA is no greater than
    min(A, B); when negative, no less than −1 × min(A, B), where
    A = the surrender charge applicable at the time of the surrender; and
    B = in all states except California, (total interest credited to the accumulation
    value since issue) − (sum of all positive MVAs applied since issue) + (sum of all
    negative MVAs applied since issue); in California, **0.50% × accumulation value at
    the time of the withdrawal**.
  - Worked MVA example (p.7): AV $102,000, penalty-free $10,200, surrender charge 5%
    = $4,590, interest credited $2,000, MVA index 3.00% at issue. If index = 2.00% at
    surrender, factor = (3.00% − 2.00%) × 3 = 3.00%; raw MVA = ($102,000 − $10,200) ×
    3.00% = $2,754, **limited to $2,000**; surrender value $99,410. If index = 4.00%,
    factor = −3.00%, raw MVA = −$2,754, limited to −$2,000; surrender value $95,410.
  - **Minimum surrender value**: "never be less than **87.5% of all premiums less any
    surrenders (after MVA or reduction for surrender charges) accumulated at a rate
    not less than the rate required or otherwise directed by your Contract**."
  - Surrender value = accumulation value, subject to MVA, less applicable surrender
    charges and state premium taxes; never less than the state-law minimum at issue.
  - Death benefit: greater of (accumulation value **plus a death benefit interest rate
    from the term start date to the date of death**) or the minimum surrender value.
    Calculation varies by the index accounts held at death. Not available once an
    annuity payout option has been elected. Spousal continuation available.
  - Annuity payout options: life income; life income with period certain; joint and
    survivor life income; income for a specified period; income for a specified
    amount. If elected during the surrender charge period, the payout is based on the
    **surrender value** rather than the accumulation value (except Florida, where
    after the first contract year the payout is based on the accumulation value and
    options are life income, life income with 10- or 20-year certain, joint and
    survivor, and joint and survivor with 10- or 20-year certain).
  - Nursing Home Confinement Waiver: automatic, no charge; after the first contract
    anniversary, up to 100% of accumulation value without surrender charge or MVA;
    covered person cannot be confined at issue; applies to the first qualifying joint
    annuitant only.

### S7. Midland National Life Insurance Company — "Midland National Capital Income® fixed index annuity — Understanding the market value adjustment" (form 32340Y-CA, REV 10-24, for use in California only)
- Publisher: Midland National Life Insurance Company — official midlandnational.com URL
- Doc type: contract-feature explanatory disclosure (2 pages)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32340Y-04+-+Understanding+the+MVA+CA/e6de4768-02a1-cdef-4370-aa8c1896db2d
- Retrieved: YES (full PDF text-extracted locally)
- Facts extracted:
  - **MVA formula (verbatim): `(io − it) × (T)`**, applied by multiplying the portion
    of any full or partial surrender exceeding the available penalty-free withdrawal
    amount, **before reduction for any surrender charge**, by that factor. Where
    `io` = index value of the MVA external index on the **issue date**; `it` = index
    value at the time of partial/full surrender; `T` = days from the surrender to the
    end of the current contract year ÷ 365, plus whole years remaining in the MVA
    period. **MVA External Index = Barclay's US Credit Index.**
  - MVA period = the **7-year surrender charge period** for Capital Income; MVA
    applies only when the withdrawal exceeds the penalty-free amount (including full
    surrender). MVA is **not applied to the death benefit** and may not apply on
    annuitization; does not apply after the MVA period.
  - Capital Income surrender charge schedule shown in the CA example: years 1–5 = 6%,
    6%, 5%, 4%, 3%.
  - MVA limit in California: the MVA is limited, positive or negative, to the lesser
    of the applicable surrender charge and **0.50% of the accumulation value**.
    Worked example: AV $115,927, 10% penalty-free $11,593, surrender charge $3,130,
    MVA index 3% at issue → 2% at surrender gives (3.0% − 2.0%) × 2 = 2.0%; raw MVA
    ($115,927 − $11,593) × 2.00% = $2,087, **limited to 0.50% × AV = $579.64**;
    surrender value $113,377. With the index at 4%, MVA = −$579.64, surrender value
    $112,218.
  - Contract forms: AS202A04 (contract); AR362A, AR363A, AR364A, AR369A, AR378A,
    AR379A04, AR380A (riders/endorsements).
  - Explicit statement that deductions for optional benefit riders, strategy fees, or
    charges for enhanced crediting methods **can exceed interest credited**, "which
    would result in loss of premium" — i.e. the 0% floor applies to index credits,
    not to the account value net of charges.

### S8. Midland National Life Insurance Company — "MNL IncomeVantage® fixed index annuity — quick reference guide" (form 25665Y REV 1-20)
- Publisher: Midland National Life Insurance Company — official midlandnational.com URL
- Doc type: producer quick reference guide (1 page; "FOR FINANCIAL PROFESSIONAL ONLY")
- URL fetched: https://www.midlandnational.com/documents/35445/8312558/25665Y.pdf/dcf404b7-a1fd-037e-b188-60cfacb0c537
- Retrieved: YES (full PDF text-extracted locally)
- Product: MNL IncomeVantage 10 / 14, flexible-premium FIA with a **built-in GLWB at
  no additional cost**. Forms AC/AS139A/ICC16-AS145A.MVA/AS145A.
- Facts extracted:
  - Issue ages: IncomeVantage 10 **40–79**; IncomeVantage 14 **40–75** (40–54 in CA).
  - Minimum premium: **flexible premium**, $20,000 non-qualified and $20,000
    qualified.
  - **Surrender charge schedules**:
    - IncomeVantage 10 (years 1–11+): 10, 10, 10, 10, 10, 9, 8, 6, 4, 2, 0 %.
    - IncomeVantage 14 (years 1–15+): 10, 10, 10, 10, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1,
      0 %.
  - Penalty-free withdrawals: beginning in the **2nd** contract year, up to **5% of
    the accumulation value** each year (note: lower than the 10% typical of the
    accumulation-focused designs).
  - **Interest crediting methods offered**: Fixed; Annual Point-to-Point with Cap
    Rate; Annual Point-to-Point with **Index Margin** (spread); Annual Point-to-Point
    with Participation Rate; Annual Point-to-Point with **Threshold Participation
    Strategy**; **Two-Year** Point-to-Point with Index Margin; **Monthly**
    Point-to-Point with Cap Rate; **Daily Average** with Index Margin.
  - Built-in GLWB feature: **GLWB stacking roll-up credit of 2% of the GLWB value plus
    a stacking component of 150% of the dollar amount of interest credited to the
    accumulation value**; lifetime payment amount (LPA) feature; increasing or level
    LPA options; **2% GLWB value bonus**; RMDs penalty-free by current company
    practice.
  - Explicit disclosure that a product with a built-in GLWB "may offer lower credited
    interest rates, lower index cap rates, lower participation rates and/or greater
    index margins" — i.e. the GLWB is financed through the option budget rather than
    an explicit charge.

### S9. Nassau Life and Annuity Company — "Indexed Annuity Rider Disclosure Document — Amplified Income Plus" (form OL5370B, 8/25; rider forms 19GLWB3, ICC19GLWB3.1) — SAMPLE
- Publisher: Nassau Life and Annuity Company (Nassau Financial Group) — official
  assets.nfg.com document
- Doc type: **signed rider disclosure document (specimen)** — the most
  contractually precise GLWB description retrieved
- URL fetched: https://assets.nfg.com/documents/salesnet/NGARider-OL5370-sample.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Product: Amplified Income Plus, a **GLWB rider** offered with Nassau Growth Annuity®
  and Nassau Bonus Annuity®.
- Facts extracted:
  - Covered Person: one for the Single Life Option; two spouses (each other's
    designated beneficiary) for the Spousal Life Option; cannot be changed after issue
    and cannot be converted between options on marriage/divorce/death.
  - Income may not start before the youngest Covered Person turns **50**; payments
    begin on the monthly anniversary following the request.
  - **Annual Benefit Amount** = Annual Benefit Amount Percentage × **the greater of
    the Income Benefit Base and the Accumulation Value on the exercise date**.
    Percentage depends on rider option (Single/Spousal), **age at contract issue**,
    and **age of the youngest living Covered Person at exercise**. Withdrawals up to
    the Annual Benefit Amount incur no charges/adjustments even if greater than the
    contract's Free Withdrawal Amount. Unused Annual Benefit Amount **does not carry
    forward**.
  - **Income Benefit Base**: equals the premium payment at issue; has no cash value;
    cannot be withdrawn. Grows **on the first 15 Contract Anniversaries** (if the
    rider has not been exercised) by two additive components:
    - **GLWB Roll-Up Amount = GLWB Roll-Up Rate × Adjusted Initial Income Benefit
      Base** (the *initial* base adjusted for withdrawals) — i.e. an explicitly
      **simple-interest** rollup. Stated **GLWB Roll-Up Rate = 3%**.
    - **Echo Amount = 150% Echo Factor × [fixed interest paid over the Contract Year
      + index credit amounts − Strategy Fee Amounts]**, floored at zero — i.e. a
      stacking credit on realized interest, net of strategy fees.
    - Worked example: base $200,000; adjusted initial base $100,000; interest+index
      credits $12,000; strategy fee $2,000; roll-up 3%; echo 150% →
      roll-up $3,000 + echo max(0, ($12,000 − $2,000) × 150%) = $15,000 → new base
      $218,000. With $0 credits and a $2,000 strategy fee, echo = $0 and the base
      grows only by the $3,000 roll-up.
    - The 15-year guaranteed-value table confirms the roll-up is **flat $3,000/yr on
      a $100,000 adjusted initial base** (simple, not compound): $103,000 → $145,000
      over 15 years.
  - Withdrawals **before exercise** (including RMDs) reduce the Income Benefit Base,
    the Adjusted Initial Income Benefit Base, and future income **in the same
    proportion that the Accumulation Value is reduced**.
  - **Excess withdrawal after exercise** — verbatim mechanics with worked example:
    an Excess Withdrawal is any withdrawal (excluding RMDs) after exercise causing
    cumulative withdrawals in the Rider Year to exceed the Annual Benefit Amount. The
    reduction percentage is computed as
    `Excess Withdrawal ÷ (Accumulation Value − Annual Benefit Amount)`, and the Income
    Benefit Base is reduced by that percentage. Example: AV $100,000, base $200,000,
    ABA $10,000 (5%), withdrawal $28,000 → AV net of ABA $90,000; excess $18,000;
    reduction 20%; base $200,000 → $160,000; ABA → $8,000.
  - RMD treatment: after exercise, an RMD greater than the Annual Benefit Amount may
    be taken **without** reducing the Income Benefit Base or Annual Benefit Amount.
  - **AV exhaustion**: "Your guaranteed income payments will continue if your
    Accumulation Value is reduced to zero **as a result of rider fee deductions or
    guaranteed income payments**… Guaranteed income payments will stop and your rider
    will terminate if your Accumulation Value is reduced to zero **for any other
    reason (including an Excess Withdrawal)**."
  - **Rider fee**: deducted at the end of each Contract Year from the Accumulation
    Value; **fee = 0.95% × Income Benefit Base** (charge base is the benefit base, not
    the account value). Deducted from the Fixed Account first; if depleted, split
    proportionately among the Indexed Accounts. Deducted **after** index credits are
    added. The **Rider Fee Percentage may be changed after the 15th Contract Year but
    will never exceed 1.50%**. A **proportional** fee (by days elapsed) is deducted on
    surrender, on a withdrawal above the Free Withdrawal Amount, or on rider
    termination. Signature page acknowledges the fee "will continue even after the
    surrender charge period on my contract has ended."
  - Rider termination events (earliest of): death of the Covered Person (Single) or
    surviving Covered Person (Spousal); **Income Benefit Base reduced to zero**;
    termination of the base contract; assignment; owner's written cancellation on or
    after the Earliest Cancellation Date; change in any Covered Person. No refund of
    past fees.
  - At the Contract Maturity Date, if AV > 0 the owner may elect lifetime guaranteed
    income payments equal to **1/12 of the Annual Benefit Amount** in place of a base
    annuity option.
  - Explicit statement that the annuities are "**NOT securities and are not subject to
    registration with the Securities and Exchange Commission**."

### S10. Nassau Life and Annuity Company — "Indexed Annuity Disclosure Document — Nassau Athos Annuity<sup>SM</sup>, Single Premium Fixed Indexed Annuity (Bonus)" (form OL5719, 6/26; contract form 25FIA-XT) — SAMPLE
- Publisher: Nassau Life and Annuity Company — official assets.nfg.com document
- Doc type: **signed base-contract disclosure document (specimen)**, 34 pages
- URL fetched: https://assets.nfg.com/documents/salesnet/OL5719.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Facts extracted:
  - **Premium bonus by issue age of oldest owner: 16% (age ≤75), 14% (ages 76–80)**;
    credited to Accumulation Value at issue, allocated and earning interest the same
    way as the premium, and treated as gain for tax purposes.
  - **Vested Premium Bonus percentages** (contract years 1–11+):
    0, 0, 15, 20, 30, 40, 50, 60, 70, 85, 100 %.
  - **Non-Vested Premium Bonus recovery formula (verbatim):**
    `(1 − A) × [ B / (1 + B) ] × C`, where A = the Vested Premium Bonus percentage for
    the contract year, B = the Premium Bonus Percentage, C = the Gross Withdrawal less
    the Free Withdrawal Amount. Worked example: year 5, bonus 16%, gross $100,000,
    free $7,000 → 70% × 0.1379 × $93,000 = **$8,979**.
  - **Surrender charge schedule** (contract years 1–11+): 12, 12, 12, 11, 10, 9, 8, 7,
    6, 4, 0 %. **Surrender charge = (Gross Withdrawal − Free Withdrawal Amount) ×
    surrender charge %.** Surrender Charge Period = first 10 Contract Years.
  - **Free Withdrawal Amount = 7% of the Daily Accumulation Value as of the preceding
    Contract Anniversary**; **none in the first Contract Year**; not carried forward.
    RMDs on an IRA are treated as free withdrawals after January 1 of the first
    Contract Year.
  - **MVA formula (verbatim from the worked example):**
    `MVA multiplier = [(1 + i_0) / (1 + i_t)]^(n/12) − 1`
    where `i_0` = MVA Index at issue, `i_t` = MVA Index at surrender, `n` = months
    remaining to the end of the Surrender Charge Period. `MVA = (Maximum Gross
    Withdrawal − Free Withdrawal Amount) × MVA multiplier`. Worked example: 24 months
    remaining, index 3.00% → 4.00%: [(1.03)/(1.04)]^(24/12) − 1 = **−0.0191**; MVA =
    ($100,000 − $7,000) × −0.0191 = **−$1,776**.
  - **MVA limit (verbatim):** `MVA limit = (A − B − C)`, not less than zero, where
    A = Maximum Gross Withdrawal, B = charges and adjustments, C = TGV. "A negative
    MVA combined with charges and adjustments never reduces the Cash Surrender Value
    below TGV. The maximum positive MVA cannot exceed the maximum negative MVA."
  - **Total Guaranteed Value (TGV)** = the minimum value paid on death, annuitization
    or surrender. At issue **TGV = 87.5% of premium (excluding Premium Bonus)**, and
    consists of the sum of a Fixed Guaranteed Value and an Indexed Guaranteed Value
    accumulated at their respective rates, each adjusted for Net Withdrawals and
    reallocations. "The interest rates will range between **0.15% and 3%** and will
    never be less than the minimum permitted by the state."
  - Allocation options: one Fixed Account and three **Extendable Indexed Accounts** —
    Extendable S&P 500 Dynamic Intraday TCA Point-to-Point with Participation;
    Extendable Nasdaq-100 Volatility Control 15% Point-to-Point with Participation;
    Extendable S&P 500 Point-to-Point with Cap. Minimum allocation per account: 10% of
    premium or $2,000.
  - **Guaranteed minimum rates** (contractual floors on the non-guaranteed scale):
    Fixed Account (1-year duration) **1%**; Extendable S&P 500 Dynamic Intraday TCA
    PTP with Participation **5%**; Extendable Nasdaq-100 Volatility Control 15% PTP
    with Participation **5%**; Extendable S&P 500 PTP with Cap **0.50%**.
  - Crediting mechanics:
    - Participation-rate accounts: Account Return = percentage change in index ×
      Participation Rate, **never less than 0%**.
    - Cap-rate accounts: Current Year Return = lesser of the Annual Index Return and
      (Cap Rate × elapsed portion of the contract year); Account Return = cumulative
      compounding of Current Year Returns across the Segment, floored at zero. (The
      disclosure's example table shows the *Current Year Return* can be negative
      within a multi-year Segment: −5% for a −5% index year; the floor applies to the
      Segment's Account Return.)
    - Multi-year segments: Cumulative Index Return = Π(1 + annual index return) − 1
      over the Segment.
  - **Extendable account / interim-value machinery (the key modeling structure):**
    - **Account Value** — the basis for calculating Index Credits at the Contract
      Anniversary.
    - **Daily Account Value** — includes realized *and unrealized* Index Credits for
      the current Segment; used to calculate the death benefit and the Protected
      Account Value.
    - **Protected Account Value = max( Account Value, 90% Protection Level × the
      highest Daily Account Value on any Contract Anniversary during the Segment )**;
      it is the maximum amount available for full surrender before fees and charges.
    - **Protected Account Return** = max(0, (1 + Account Return) × 90% − 1).
    - **Reset vs. Extend**: at each anniversary (during the 15-day Reallocation
      Period, if Daily Account Value > Protected Account Value) the owner may Reset
      (end the Segment, credit the Index Credit, start a new 1-year Segment with a new
      rate) or Extend (defer the credit, extend the Segment one year, receive a
      modified rate). For **participation-rate** accounts the modified participation
      rate applies **retroactively to the whole Segment**; for **cap-rate** accounts
      the modified cap applies **only to the next Contract Year**.
    - **Protected Account Value Reset**: automatic Reset if the Protected Account Value
      ≥ the Daily Account Value on a Contract Anniversary; Account Value and Daily
      Account Value are set equal to the Protected Account Value and a new Segment
      begins.
    - Index Credit Amount = Account Value on the Segment Maturity Date × max(Account
      Return, Protected Account Return); zero on any other day.
  - **Index Credit Amount on Withdrawal (verbatim mechanics)**: partial index credit
    on a mid-Segment withdrawal =
    `Gross Withdrawal × Protected Account Return ÷ (1 + Protected Account Return)`.
    Worked example: AV $100,000, Protected Account Return 10%, $10,000 gross
    withdrawal → $10,000 × 10% = $1,000; ÷ 1.10 = **$909**; Account Value after
    withdrawal = $100,000 + $909 − $10,000 = $90,909.
  - **Maximum Gross Withdrawal** = sum over accounts of the Account Maximum Gross
    Withdrawal, where for Indexed Accounts that is the Daily Account Value **on a
    Contract Anniversary** and the Protected Account Value **on all other dates**, and
    for the Fixed Account it is the Account Value.
  - **Cash Surrender Value**: Standard CSV = Maximum Gross Withdrawal less Non-Vested
    Premium Bonus and Surrender Charges, adjusted by MVA, **never less than TGV**.
    During the **Window Period** (currently 15 days after the Contract Anniversary,
    never less than 5 days), CSV = greater of Standard CSV and the **Window Period CSV
    = max( A, B + C − D )** where A = TGV at surrender, B = Standard CSV on the prior
    Contract Anniversary, C = interest credited to the Fixed Account since that
    anniversary, D = Net Withdrawals since that anniversary.
  - **Death benefit** = greater of (1) the Cash Surrender Value and (2) the Fixed
    Account Value plus, for each Indexed Account, **max(Daily Account Value, Protected
    Account Value)**. No surrender charge, bonus recovery or MVA applies on death.
  - Annuity payment options: Life Annuity with Specified Period Certain; Non-Refund
    Life Annuity; Joint and Survivorship Life Annuity; Installment Refund Life
    Annuity; Joint and Survivorship Life Annuity with 10-Year Period Certain; Payments
    for a Specified Period Certain; Payments of a Specified Amount. Annuity payments
    are based on the **greater of the Cash Surrender Value and the Daily Accumulation
    Value** on the Contract Maturity Date.
  - Nursing Home Waiver: after the first Contract Anniversary, confinement to a
    Licensed Nursing Home Facility for ≥**90 consecutive days**; waives the Surrender
    Charge but **not** the Non-Vested Premium Bonus recovery or the MVA. Not available
    if confined in the year prior to and including the issue date.
  - Terminal Illness Waiver: after the first Contract Anniversary; terminal illness =
    expected to result in death within **six months**; same partial waiver (surrender
    charge only).
  - Free look refund excludes the Premium Bonus.
  - "The contract is not a security. The contract is not registered under the
    Securities Act of 1933 and is being offered and sold in reliance on an exemption
    therein."

### S11. Nationwide Life and Annuity Insurance Company — "Nationwide New Heights® fixed indexed annuities — Index and Strategy Growth Opportunities" (form FAM-0475AO.2 (1/17))
- Publisher: Nationwide Life and Annuity Insurance Company (Nationwide-operated
  marketing asset host `s3.amazonaws.com/nh3`)
- Doc type: consumer strategy brochure (6 pages)
- URL fetched: https://s3.amazonaws.com/nh3/FAM-0475AO.2_Strategy_Brochure.pdf
- Retrieved: YES (full PDF text-extracted locally)
- Note: this is a 2017-vintage document retained because it documents a **structurally
  different FIA design** (the Balanced Allocation Strategy) that is worth modeling as
  a variation. Current New Heights Select rates were not retrieved (see Gaps).
- Facts extracted:
  - Index options at that time: J.P. Morgan Mozaic II (multi-asset, monthly
    reallocation), MSCI EAFE, NYSE Zebra Edge, S&P 500 Composite Price Index.
  - **Balanced Allocation Strategy (BAS)** — each strategy option blends three
    components: an **index allocation** (a percentage multiplied by index
    performance), a **declared rate allocation** (a percentage multiplied by the
    declared annual fixed rate), and a **strategy spread** (an annual percentage
    deducted when calculating earnings, which "will never cause earnings to be less
    than zero for any strategy term").
  - Two strategy options per index: Strategy A (higher index allocation, higher
    returns in strongly rising markets); Strategy B (lower or no strategy spread,
    better in slow-growth markets).
  - **Strategy term**: a specified number of years used to measure strategy earnings;
    set at contract issue; at the end of each term the owner may select a new index
    and strategy.
  - **Balanced Allocation Value (BAV)** = the greater of (1) the contract value plus
    any strategy earnings not yet credited, or (2) the return-of-purchase-payment
    guarantee amount. The BAV is tracked **daily**; earnings are credited at the end
    of each strategy term.
  - Withdrawal crediting: "Full earnings to-date are credited on the free withdrawal
    amount; **pro-rata earnings** are credited on withdrawals above the amount."
    Earnings-to-date are also credited if a death benefit is payable.
  - **Optional one-time lock-in** of the index value, once per strategy term, plus an
    automatic end-of-term lock-in; the BAV "will never fall below its value at the
    beginning of the term."
  - Index allocation, declared rate allocation, declared rate and strategy spread are
    guaranteed for the first strategy term and subject to change at the beginning of
    each new strategy term.
  - Guaranteed lifetime income benefit and enhanced death benefit are **optional
    riders for additional cost**.

### S12. Athene Annuity and Life Company — Ascent Pro producer product page (athene.com)
- Publisher: Athene Annuity and Life Company
- Doc type: product landing page
- URL fetched: https://www.athene.com/producer/products/ascent-pro
- Retrieved: YES (HTML page; the linked PDFs are behind a Widen viewer, see failures)
- Facts extracted: product positioned as an FIA "focused on income" with a built-in
  income rider offering guaranteed Income Base growth; two income payment options
  (Level or Earnings-Indexed); free annual withdrawals up to 10% of accumulated value
  beginning year one; bailout feature; terminal illness and confinement waivers
  (state-dependent). Issued by Athene Annuity and Life Company (all states except NY)
  and Athene Annuity & Life Assurance Company of New York (NY).

### Documents attempted but NOT retrieved (no content asserted from these)
| ID | Document | URL | Failure |
|---|---|---|---|
| S-f1 | Athene Ascent Pro 10 "Rates and Availability" | https://athenecentral.widen.net/s/lhw7bjvvzz/65219 | Widen viewer / password-protected PDF; no text |
| S-f2 | Athene Ascent Series spec sheet (distributor mirror) | https://www.iamsinc.com/wp-content/uploads/2016/04/Ascent-Series-Spec-Sheet.pdf | HTTP 403 |
| S-f3 | American Equity IncomeShield 10 brochure (official) | https://media.american-equity.com/Documents/1164-SB-10.pdf | DNS resolution failure (`getaddrinfo ENOTFOUND`) from this environment; content obtained from the mirror at S5 instead |
| S-f4 | Nationwide New Heights Select 10 product brochure | https://nationwidefinancial.com/media/pdf/FAM-1606AO.pdf | HTTP 403 |

---

## Regulatory and actuarial references

> These product-local R# numbers are independent of the cross-product library
> numbering used elsewhere in this repository.

### R1. American Academy of Actuaries, Life Experience Committee — "Fixed Indexed Annuities—Product Mechanics and Risk Management" (February 2026)
- Publisher: American Academy of Actuaries
- URL fetched: https://actuary.org/wp-content/uploads/2026/02/life-FIA-policypaper.pdf
- Retrieved: YES (31-page PDF text-extracted locally)
- Status disclaimer in the document: not an ASOP, not binding, "a list of
  considerations and resources."
- Facts extracted:
  - Market context: 2023 U.S. FIA sales **$95.6 billion**, +20% year over year
    (citing LIMRA).
  - Crediting mechanisms defined: **Cap**, **Participation Rate**, **Spread**,
    **Floor**, **Performance Trigger**. Worked definition: "if an index returns 10%
    and the participation rate is 80% and the cap is 6%, the amount credited is
    min[80% × 10%; 6%] = 6%"; with a 2% spread and 12% index growth the credit is 10%
    (participation 100%, cap > 10%).
  - Monthly sum cap example: 2022 S&P 500 monthly returns with a **1% monthly cap and
    0% monthly floor** produced an annual credit of **5.0%** against a −7.6% raw sum
    (table of monthly returns reproduced in the paper).
  - Performance trigger example: 7% defined rate credited whenever the annual S&P 500
    return is positive/zero; 2018 (−4%) → 0%, 2019 (19%) → 7%, 2020 (15%) → 7%,
    2021 (22%) → 7%, 2022 (−10%) → 0%.
  - Custom / volatility-controlled indices: built-in volatility control, diversified
    multi-asset exposure, tactical allocation algorithms; index performance usually
    excludes dividends.
  - Surrender charges typically over the first **5 to 10 years**, decreasing to 0%;
    MVA may also apply during that period, subject to standard nonforfeiture limits.
  - Death benefit "usually the greater of the contract value or a guaranteed minimum
    amount (e.g., a percentage of total purchase payments adjusted for any withdrawals
    and accumulated at the contract's nonforfeiture rate)."
  - GLWB described as "one of the most popular optional features in FIAs today";
    guaranteed for life "even if their account balance is reduced to $0"; unlike
    annuitization the owner retains access to the account balance. Other riders: GMIB,
    GMDB, enhanced benefit riders, LTC riders.
  - **Policyholder behavior (industry experience observations):**
    - Dynamic lapse modelling is typical. Surrender rates start low, rise through the
      surrender charge period, spike in the **shock lapse** year when the charge
      expires, then fall back but remain above pre-shock levels.
    - Independent-agent business lapses more than bank/captive channels; qualified
      contracts lapse less than non-qualified; **contracts with GLWBs lapse less than
      those without**; **activated GLWBs lapse least**, with the lowest rates where
      the withdrawal is **95%–105% of the maximum available amount**.
    - Withdrawal rates rise with attained age; higher for qualified contracts,
      especially at ages 70+ (RMDs); higher where a GLWB has been paid for; among
      GLWB users the majority withdraw **95%–105% of the maximum**.
    - Most contracts are single- or first-year-premium only; subsequent deposits are
      higher on contracts **without** a GLWB.
    - Mortality: per a 2011–2015 SOA study, qualified annuities have lower A/E ratios
      than non-qualified; FIAs **without** GLWBs showed increasing A/E ratios by
      account-value band, contrary to the usual pattern.
  - **Hedging / option budget:** insurers invest most premium in fixed income with
    "the remaining portion allocated to an **option/hedge budget** to purchase
    hedges." Static hedging (buy-and-hold index options, rule-based cohorting by
    weighted-average guaranteed liability index credit levels) is used by "the
    majority of FIA programs." Instruments: vanilla European calls and call spreads on
    S&P 500 and customized volatility-controlled indices; **Cliquet options for
    monthly sum cap policies, Asian options for averaging policies, digital options
    for trigger policies**. Dynamic hedging (futures, swaps, exchange-traded options,
    Greeks-based rebalancing) used by some. Multi-year options and guaranteed
    participation/cap products can lack OTC liquidity. Hedge notional may be set on
    0% surrenders, best-estimate surrenders, or in between. Some companies net FIA
    index risk against IUL, RILA and GLB/VA exposures.
  - **Statutory reserves:** determined under **AG 33** (CARVM for annuity contracts
    with elective benefits) and **AG 35** (how to incorporate the index feature into
    the AG 33 calculation). AG 35 offers "Type 1" and "Type 2" methods, with quarterly
    filing certification requirements and constraints/notification on changing method.
    **AG 35 requires reserves for equity indexed annuities to be tested for asset
    adequacy** (not a standalone adequacy requirement).
  - **VM-22:** at publication the NAIC and industry were developing a principle-based
    reserve approach for fixed annuity reserves (VM-22), including FIAs, "targeted for
    Jan. 1, 2026, on an elective basis and Jan. 1, 2029, on a required basis."
  - **GAAP:** FIAs without GMDBs are FAS 97 investment contracts; with GMDBs they are
    universal life-type contracts. The **index feature is an embedded derivative**,
    fair-valued on expected current and future index credits (current index-period
    option valued with closed-form Black-Scholes). **GLBs and GMDBs are market risk
    benefits (MRBs)**, held at fair value with an adjustment for explicit fees; where
    there is no explicit MRB fee the MRB is valued option-like with a non-zero initial
    fair value and an offsetting host adjustment. Remaining cash flows form the host
    contract, discounted at a **host accrual rate** set so total liability at issue =
    initial premium. DAC, DSI and URL are the associated intangibles. Two-tier
    contracts (cash-value tier without index credits, annuitization tier with them)
    have **no embedded derivative**; the annuitization benefit is an MRB.
  - **Illustrations:** NAIC Model 245 (Annuity Disclosure Model Regulation) requires a
    disclosure and Buyer's Guide at or within five days of application; non-guaranteed
    elements shall be **no more favorable than current** and shall not assume
    improvements; **an index must have existed at least 10 years to be illustrated**;
    non-guaranteed illustrations must be shown for three scenarios (most recent 10
    calendar years; worst 10 continuous of the last 20; highest 10 consecutive of the
    last 20), using the geometric mean annual effective rate for each. Additional
    requirements apply for MVA upside/downside.
  - **Nonforfeiture:** the NAIC Standard Nonforfeiture Law for Individual Deferred
    Annuities applies to FIAs; FIAs "may use a nonforfeiture interest rate **up to
    100 basis points lower** than the rate applicable to other fixed deferred annuities
    to reflect the value of the index benefit," and the commissioner may require an
    actuarial certification that the value of the equity guarantee is at least
    equivalent to the interest-rate deduction.
  - **Suitability:** Model 275 requires producers to act in the consumer's best
    interest and insurers to supervise recommendations.
  - **Filing:** products may be filed through the Interstate Insurance Compact
    (IIPRC); "the IIPRC limits usually default to the most conservative state
    variations."
  - **Rate setting:** most companies review non-guaranteed elements (caps,
    participation rates, spreads, performance triggers) regularly (e.g. monthly),
    considering current investment yields, option costs, market volatility, premium
    volumes, competitive environment and profit objectives; "rate setting targets could
    be the priced product **option budget** for the index strategies, therefore
    maintaining the initial product profitability."
  - Source list includes AG 33, AG 35, NAIC 805-1, NAIC 245, NAIC 275, and the SOA
    FIA behavior studies for 2013-2015, 2016-2018 and 2019-2020, the SOA 2011-2015
    Deferred Annuity Mortality Study, and SOA payout annuity mortality studies.

### R2. NAIC — "Standard Nonforfeiture Law for Individual Deferred Annuities" (Model #805), NAIC Model Laws, Regulations, Guidelines and Other Resources — Fall 2020
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (5-page PDF text-extracted locally)
- Facts extracted:
  - Scope exclusions (Section 2A): reinsurance, employer/employee-organization group
    annuities under a retirement or deferred-compensation plan (other than IRA-type
    plans under IRC §408), premium deposit funds, **variable annuities**, investment
    annuities, immediate annuities, deferred annuities after annuity payments have
    commenced, and reversionary annuities. Sections 3–8 do not apply to contingent
    deferred annuities (Section 2B).
  - **Section 4A(1): minimum nonforfeiture amount** = accumulation, at the Section 4B
    rates, of the **net considerations** paid, **decreased by** (a) prior withdrawals
    or partial surrenders accumulated at the same rates, (b) **an annual contract
    charge of $50** accumulated at the same rates, (c) any premium tax paid by the
    company, accumulated, and (d) indebtedness including accrued interest.
  - **Section 4A(2): net considerations = 87.5% of the gross considerations credited
    to the contract during that contract year.**
  - **Section 4B: the nonforfeiture interest rate** = the lesser of **3% per annum**
    and: (1) the **five-year Constant Maturity Treasury Rate** reported by the Federal
    Reserve as of a date, or average over a period, rounded to the nearest 1/20th of
    one percent, specified in the contract, no longer than **15 months** prior to the
    contract issue date or redetermination date; (2) **reduced by 125 basis points**;
    (3) where the resulting rate is **not less than 15 basis points (0.15%)**; and
    (4) the rate applies for an initial period and may be redetermined for additional
    periods (redetermination date, basis and period stated in the contract).
  - **Section 4C (the FIA provision):** "During the period or term that a contract
    provides substantive participation in an equity indexed benefit, it may increase
    the reduction described in Subsection B(2) above by **up to an additional 100
    basis points** to reflect the value of the equity index benefit. The present value
    at the contract issue date, and at each redetermination date thereafter, of the
    additional reduction shall not exceed the market value of the benefit." The
    commissioner may require a demonstration and may disallow or limit the reduction.
  - Section 6 (cash surrender values): the cash surrender benefit prior to maturity
    must not be less than the present value, at the date of surrender, of the maturity
    value of the paid-up annuity benefit arising from prior considerations, reduced
    for prior withdrawals, computed at an interest rate **not more than 1% higher**
    than the contract's accumulation rate, less indebtedness and plus additional
    credited amounts. "In no event shall any cash surrender benefit be less than the
    minimum nonforfeiture amount at that time. **The death benefit under such contracts
    shall be at least equal to the cash surrender benefit.**"
  - Section 8 (maturity date for benefit calculation): the latest election date
    permitted by the contract, but not later than the anniversary next following the
    annuitant's **70th birthday** or the **tenth contract anniversary**, whichever is
    later.

### R3. NAIC — "Annuity Nonforfeiture Model Regulation" (Model #806), October 2007 edition
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-806.pdf
- Retrieved: YES (12-page PDF text-extracted locally)
- Facts extracted:
  - Purpose: implements Section 4 of Model #805.
  - "**Equity-indexed benefits**" defined as a benefit in an annuity contract in which
    the value of the benefit is determined using an interest crediting rate based on
    the performance of an equity-based index and contract parameters; excludes
    separate-account variable benefits and indexed guaranteed separate account
    contracts purchased by institutional buyers. "**Index term**" = each period until
    the next indexed interest crediting date.
  - Redetermination machinery: the "basis" may be a specified period producing the
    5-year CMT value, or a **change-triggered method** with a symmetrical range whose
    **maximum allowable range is ±50 basis points**; at the beginning of each modal
    period a potential nonforfeiture rate is computed without caps/floors and the
    current rate is updated only if the difference exceeds the range. A method that
    defines the nonforfeiture rate as the lowest rate in a specified period is
    **specifically excluded**. Changes to the initial method are allowed **once per
    calendar year**, applying only to new contracts.
  - **Multiple nonforfeiture rates within one contract (Section 6B):** a contract with
    equity-indexed benefits may have more than one nonforfeiture rate — the
    non-equity-indexed benefit uses the Model 805 §4B rate, and each equity-indexed
    benefit for which the additional reduction is elected uses a reduced rate. The
    contract's minimum nonforfeiture amount is the **sum** of the per-benefit
    nonforfeiture amounts (computed before any reduction for indebtedness), with
    indebtedness deducted afterwards.
  - **Transfers between benefits (Section 6B(4)):** on transfer *from* a benefit, that
    benefit's minimum nonforfeiture amount is reduced by its pre-transfer minimum
    nonforfeiture amount × the proportion of the benefit's contract value transferred;
    on transfer *to* a benefit, it is increased by the sum of those reductions × the
    proportion of total transferred contract value going to that benefit; contract
    value is first reduced by any transfer fees.
  - **Excess withdrawals (Section 6B(5)):** where a withdrawal from a benefit exceeds
    that benefit's nonforfeiture amount, the insurer must treat the excess at least as
    favorably as deducting it from the nonforfeiture amounts of other benefits **in
    order from lowest to highest nonforfeiture interest rate**.
  - Contract charges and premium taxes are allocated to each benefit's minimum
    nonforfeiture amount in proportion to that benefit's share of total contract value.
  - **Section 7 — the "substantive participation" test (the key quantitative rule):**
    1. Calculate the **annualized option cost** for the equity-indexed benefit in basis
       points for the entire Index Term as of the beginning of the Index Term, using
       the benefit's **guaranteed** product features (guaranteed participation rate,
       guaranteed caps, etc.), on a basis representative of the point in time at the
       beginning of the current index term (which cannot change during the term), with
       **no adjustments for persistency, death, utilization, etc.**, and calibrated to
       capital-markets-based option pricing.
    2. "If the annualized option cost for the equity-indexed benefit is **twenty-five
       (25) basis points or more**, then the equity-indexed benefit provides
       substantive participation… and the company may take a reduction equal to the
       **lesser of 100 basis points and the annual cost basis value**."
    3. An actuarial certification signed by a member of the American Academy of
       Actuaries is required at form filing (Appendix C) and **annually** thereafter
       with the annual statement (Appendix D).
    - If the commissioner determines the reduction was inappropriately taken, the
      commissioner may require recalculation of all values for all affected
      policyholders.

### R4. NAIC — "Suitability in Annuity Transactions Model Regulation" (Model #275), Spring 2020 edition
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-275.pdf
- Retrieved: YES (20-page PDF; sections 1–5 text-extracted locally)
- Facts extracted:
  - Purpose (Section 1A): require producers "to act in the best interest of the
    consumer when making a recommendation of an annuity" and require insurers to
    establish and maintain a supervision system. Section 1B expressly disclaims any
    private cause of action or fiduciary standard.
  - **Drafting note tying Model 275 to Dodd-Frank (verbatim):** "Section 989J of the
    Dodd-Frank Wall Street Reform and Consumer Protection Act of 2010 ('Dodd-Frank
    Act') specifically refers to this model regulation as the 'Suitability in Annuity
    Transactions Model Regulation' (#275). Section 989J of the Dodd-Frank Act confirmed
    this exemption of certain annuities from the Securities Act of 1933 and confirmed
    state regulatory authority. This regulation is a successor regulation that exceeds
    the requirements of the 2010 model regulation."
  - Scope: "any sale or recommendation of an annuity." Exemptions (Section 4): direct
    response solicitations without a recommendation; contracts funding ERISA plans,
    §401(a)/401(k)/403(b)/408(k)/408(p) plans established or maintained by an employer,
    §414 government/church plans, §457 deferred compensation, and non-qualified
    deferred compensation arrangements; structured settlements of personal injury
    litigation; formal prepaid funeral contracts.
  - "Consumer profile information" enumerated (14 items) including liquidity needs,
    liquid net worth, financial time horizon, and "**risk tolerance, including but not
    limited to, willingness to accept non-guaranteed elements in the annuity**."
  - **"Non-guaranteed elements" defined (verbatim):** "the premiums, credited interest
    rates (including any bonus), benefits, values, dividends, non-interest based
    credits, charges or elements of formulas used to determine any of these, that are
    subject to company discretion and are not guaranteed at issue. An element is
    considered non-guaranteed if any of the underlying non-guaranteed elements are used
    in its calculation."
  - "Material conflict of interest" defined as a financial interest of the producer in
    the sale that a reasonable person would expect to influence impartiality; expressly
    **excludes** cash and non-cash compensation.

### R5. NAIC — "Variable Annuity Model Regulation" (Model #250), October 2007 edition
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: YES (13-page PDF; sections 1–3 text-extracted locally)
- Facts extracted: Model #250 is the **Variable Annuity Model Regulation** — it applies
  to contracts "that provide for annuity benefits that vary according to the investment
  experience of a separate account or accounts maintained by the insurer." It governs
  company qualification, separate accounts, contract filing, required reports, and
  agent qualification.
- **Correction to a common misattribution:** Model #250 is **not** an FIA-specific
  model. FIAs are general-account, non-separate-account products [S5][S10] and are
  therefore outside its scope. The NAIC models that actually bear on FIAs are **#805**
  and **#806** (nonforfeiture) [R2][R3], **#245** (Annuity Disclosure / illustrations)
  [R1], and **#275** (Suitability / best interest) [R4].

### R6. Actuarial Standards Board — ASOP No. 2, "Nonguaranteed Elements for Life Insurance and Annuity Products" (Doc. No. 204)
- Publisher: Actuarial Standards Board
- URL fetched: http://www.actuarialstandardsboard.org/wp-content/uploads/2021/12/asop002_204-2.pdf
- Retrieved: YES (33-page PDF; front matter and sections 1–3.4 text-extracted locally)
- Facts extracted:
  - **Adopted September 2021; effective for actuarial services performed on or after
    June 1, 2022.**
  - Purpose (1.1): guidance for the determination of nonguaranteed elements (NGEs) for
    life insurance and annuity products, including riders.
  - Scope (1.2): individual policy forms where NGEs may vary at the discretion of the
    insurer, including in-force policies on the effective date; "determination"
    includes both the initial determination at issue and subsequent in-force
    determinations. "Examples of products within the scope of this standard include
    universal life, indeterminate premium life, and **deferred annuity products. Such
    products may be fixed, variable, or indexed.**" Excludes policyholder dividends
    (ASOP No. 15), reinsurance contract elements, and illustrations subject to ASOP
    No. 24.
  - Definitions:
    - **2.3 Guaranteed Element** — "a premium, value, charge, or benefit that limits an
      NGE… Examples of guaranteed elements include maximum premium charges, maximum
      expense charges, minimum credited interest rates, maximum cost of insurance
      charges, maximum gross premiums, **minimum index parameters**, maximum mortality
      and expense (M&E) risk charges, and maximum policy loan interest rates."
    - **2.4 Nonguaranteed Element (NGE)** — any premium, charge, or benefit that
      (1) affects policy costs or values, (2) is not guaranteed, and (3) can be changed
      at the insurer's discretion; "an NGE reflects expectations of **future**
      experience as opposed to… a dividend, which reflects participation in past
      experience." Examples explicitly include "credited interest, cost of insurance
      (COI) charges, **bonuses**, indeterminate premiums, **index parameters used to
      determine credited interest**, and expense charges."
    - **2.1 Anticipated Experience Factor**; **2.5 NGE Framework**; **2.6 NGE Scale**;
      **2.8 Policy Class**; **2.9 Profitability Metric**.
  - **Section 3.2 — the two governing principles for the determination policy
    (verbatim):**
    a. "NGE scales are determined with the expectation that they will be revised **only
       if anticipated experience factors have changed** since issue, or alternatively,
       since the previous revision."
    b. "NGE scales are determined based on reasonable expectations of future experience
       and are **not determined with the objective of recouping past losses or
       distributing past gains**."
  - Section 3.2.1: the actuary should consider, among other items, how anticipated
    experience factors reflect expectations of future experience; the variability and
    credibility of each factor; the insurer's reserve, profitability, capital, surplus
    and marketing objectives; reinsurance and taxes; and periodic review of in-force
    NGEs including the maximum time between successive reviews.
  - Section 3.2.2 (applying the policy) requires taking into account guaranteed
    elements, **policyholder options including the likelihood of antiselection**, other
    relevant policy provisions, reserve/profitability/capital/surplus/marketing
    impacts, reinsurance and taxation, applicable law, and available resources.
  - Section 3.3.1 (policy classes for future sales): classes should be consistent with
    ASOP No. 12, appropriate for each NGE (a policy may sit in different classes for
    credited interest and for COI), reflective of differences in anticipated experience
    factors, **refined appropriately to mitigate antiselection**, and not expected to
    be redefined after issue. Grouping methodologies may vary by duration (e.g. an
    investment-year interest crediting method using new-money in early durations and
    portfolio in later durations).
  - Section 3.3.2 (in-force): policies should remain in their classes unless new
    information material to anticipated experience factors supports reassignment.
  - Section 3.4 (determination process): take into account the appropriateness of
    models/methods/profitability metrics; how anticipated experience factors relate to
    NGE scales; **consistency of NGE scales with policy provisions**; **limits due to
    regulatory constraints**; **limits due to guaranteed elements**; and impacts on/from
    reserve, profitability, capital, surplus and marketing objectives. Approximation
    methods such as smoothing and interpolation are permitted.
  - Section 3.4.1 additionally requires considering how NGE scales are structured to
    cover costs under the product design and the profitability impact if policyholder
    behavior varies from expectations; constraints on the ability to revise NGE scales
    (guaranteed elements, contractual limitations, development and implementation cost,
    systems constraints); sensitivity analysis; and a recommended review frequency.
    "For example, changes in credited interest may be based on a previously established
    interest rate spread."
- **Application to FIAs:** this is the standard that governs renewal cap /
  participation-rate / spread / index-margin setting on in-force FIA contracts, and the
  guaranteed minimum caps and participation rates disclosed at [S4] and [S10] are the
  "minimum index parameters" that ASOP No. 2 §2.3 names as guaranteed elements bounding
  those NGE scales.

### R7. NAIC — Valuation Manual (VM)-22 (A) Subgroup
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/committees/a/valuation-manual-22-sg
- Retrieved: YES (HTML page)
- Facts extracted: the subgroup's 2026 charges are to address post-launch activities
  following implementation of the VM-22 principle-based reserving framework, to monitor
  the **non-variable (fixed) annuities** reserve framework and determine whether
  revisions are needed, and to develop and recommend changes improving the accuracy and
  clarity of VM-22 reserve requirements and reporting. Variable annuities are handled
  separately by the Variable Annuities Capital and Reserve (E/A) Subgroup.
- For the VM-22 effective dates (elective 1/1/2026, mandatory 1/1/2029 for new
  business) see [R1], which states them directly.

### R8. Society of Actuaries Research Institute / LIMRA — "2019-20 Fixed Indexed Annuity Contract Owner Behavior Study" (announcement page)
- Publisher: Society of Actuaries Research Institute (joint with LIMRA)
- URL fetched: https://www.soa.org/resources/announcements/press-releases/2023/fixed-indexed-annuity/
- Retrieved: YES (HTML page). The report PDF at
  https://www.soa.org/4a3268/globalassets/assets/files/resources/experience-studies/2023/19-20-fia-contract-owner.pdf
  returned **HTTP 404** and was not retrieved.
- Facts extracted:
  - Data from **20 companies representing just over 60% of the U.S. FIA market**;
    study years 2019–2020.
  - **Shock-lapse contrast: in the year the surrender charge expires, the surrender
    rate was 10% for contracts with a GLWB rider versus 33% for contracts without.**
  - Withdrawal incidence: **37%** of GLWB-rider contracts took withdrawals in 2019–2020
    versus **fewer than 30%** of contracts without a GLWB rider.
  - Subsequent premium deposits (contract years 2–10): **2.5%** of contracts overall;
    **3.3%** without a GLWB rider; **1.9%** with one.

### R9. Society of Actuaries Research Institute / LIMRA — "2023 Fixed Indexed Annuity Contract Owner Behavior Experience Study" (study landing page, 2025)
- Publisher: Society of Actuaries Research Institute
- URL fetched: https://www.soa.org/resources/experience-studies/2025/2023-fixed-index-annuity/
- Retrieved: YES (HTML page). The detailed results are behind a paid Experience Studies
  Pro subscription and were **not** retrieved; the report PDF is listed at
  https://www.soa.org/globalassets/assets/files/research/exp-study/2025/2023-fixed-indexed-anuity-study.pdf
  (not fetched).
- Facts extracted (scope only):
  - Observation year **2023**; **17 participating companies representing 57% of
    industry new sales and 58% of industry assets in force**.
  - Approximately **2.7 million** contracts of surrender exposure by count; **$328
    billion** of surrender exposure by contract value; over **208,000** surrenders;
    **$13.0 billion** of contract withdrawals.
  - Includes both single- and flexible-premium products, with and without GLWB riders.

### R10. SEC — Final Rule, "Indexed Annuities," Release No. 33-9152 (removal of Rule 151A)
- Publisher: U.S. Securities and Exchange Commission
- URLs attempted:
  - https://www.sec.gov/files/rules/final/2010/33-9152.pdf → **HTTP 403** (not retrieved)
  - https://www.federalregister.gov/documents/2010/10/20/2010-26347/indexed-annuities →
    **302 redirect to an interstitial host** (not retrieved)
- Retrieved: **NO**
- What can be said from retrieved sources: [R4] (NAIC Model #275, Spring 2020) states
  in its own drafting note that "Section 989J of the Dodd-Frank Act confirmed this
  exemption of certain annuities from the Securities Act of 1933 and confirmed state
  regulatory authority," and refers to Model #275 by name as the regulation Dodd-Frank
  §989J points to. Separately, two currently-sold FIA disclosure documents state
  plainly that the contracts are not securities: "The IndexMax ADV 5 is **not a
  registered security**" [S6]; "The contract is not a security. The contract is not
  registered under the Securities Act of 1933 and is being offered and sold in reliance
  on an exemption therein" [S10]; and "**NOT securities and are not subject to
  registration with the Securities and Exchange Commission ('SEC')**" [S9].
- [unverified] The D.C. Circuit vacated SEC Rule 151A in *American Equity Investment
  Life Insurance Co. v. SEC*, 613 F.3d 166 (D.C. Cir. 2010), and Dodd-Frank §989J (the
  "Harkin Amendment") set out conditions — non-separate-account value, compliance with
  the state standard nonforfeiture law (or Model #805 in its absence), state filing and
  approval, and state adoption of suitability rules that substantially meet or exceed
  Model #275 — under which such annuities are exempt securities. **These specifics were
  not confirmed against a retrieved primary document** and must be re-verified before
  being relied on.

### R11. NAIC Actuarial Guidelines XXXIII and XXXV (AG 33, AG 35)
- Retrieved: **NO** (the guidelines themselves live in the NAIC Accounting Practices &
  Procedures Manual, which is not freely served in text form; no primary copy was
  successfully fetched).
- Everything this file says about AG 33 / AG 35 comes from [R1] (the American Academy
  of Actuaries FIA paper), which is a secondary but authoritative professional source:
  AG 33 governs CARVM reserves for annuity contracts with elective benefits; AG 35
  governs incorporation of the index feature into the AG 33 calculation, offers "Type
  1" and "Type 2" methods with quarterly certification and change-notification
  requirements, and requires asset adequacy testing of equity-indexed annuity reserves
  [R1].
- [unverified] Type 1 is commonly described as the "hedged as required" method
  (requiring an ongoing demonstration of hedge effectiveness) and Type 2 as "not hedged
  as required" (requiring certification of the reasonableness of assumptions). Not
  confirmed against a retrieved primary document.

---

## Extracted specifications

### 1. Contract architecture and values

- An FIA is a general-account single- or flexible-premium **deferred** annuity. Premium
  buys an **Accumulation Value / Accumulated Value / Contract Value** (naming varies by
  insurer) allocated across a **fixed account** and one or more **indexed accounts**
  [S1][S5][S6][S10][R1].
- The three values that must be modeled separately:
  1. **Account value (AV)** — the working balance; grows with index/fixed credits,
     falls with withdrawals and charges [S1][S6][S10].
  2. **Minimum guaranteed / nonforfeiture value** — variously "Minimum Guaranteed
     Contract Value" (MGCV) [S1][S2], "Minimum Guaranteed Surrender Value" (MGSV) [S5],
     "minimum surrender value" [S6], "Total Guaranteed Value" (TGV) [S10]. It floors
     the cash surrender value and, in some designs, the death benefit.
  3. **Benefit base / Income Base / Protected Income Value / Income Account Value** —
     a notional GLWB base with no cash value [S1][S2][S3][S5][S9].
- Cash Surrender Value = max( AV adjusted for surrender charge and MVA (and, where
  applicable, bonus recovery), minimum guaranteed value ) [S1][S6][S10].
- Death benefit = max( AV, minimum guaranteed value ) in the plain designs [S1][S2][S5];
  Midland IndexMax adds a "death benefit interest rate" from the term start date to the
  date of death [S6]; Nassau Athos uses max( CSV, Fixed Account Value + Σ max(Daily
  Account Value, Protected Account Value) ) [S10]; Allianz Benefit Control offers a
  **PIV-based** death benefit if taken over ≥5 years, capped at **250% of the AV**, or
  an AV lump sum [S3].
- Model #805 §6 requires the death benefit under a contract providing cash surrender
  benefits to be **at least equal to the cash surrender benefit** [R2].

### 2. Index crediting formulas

Crediting methods encountered, with the parameters that must be modeled:

| Method | Formula (as documented) | Source |
|---|---|---|
| Annual point-to-point with cap | credit rate = max(0, min(index return, cap)) | [R1][S4][S10] |
| Annual point-to-point with participation rate | credit rate = max(0, par × index return) | [R1][S4][S10] |
| Annual point-to-point with spread / index margin | credit rate = max(0, par × index return − spread) | [R1][S8] |
| Combined cap + par | credit = min(par × index return, cap), floored at 0 — worked as min(80% × 10%, 6%) = 6% | [R1] |
| Monthly sum (annualized) with monthly cap | credit rate = max(0, Σ over 12 months of min(monthly return, monthly cap)); the monthly floor is 0 in the Academy example but negative monthly returns are summed in full in many designs | [R1] worked example uses a 0% monthly floor; [S4] declares a monthly cap of 1.70% with a **guaranteed minimum monthly cap of 0.50%** |
| Monthly / daily average | credit rate based on the average of monthly (or daily) index values over the term rather than the terminal value | [S6] (average monthly index value in the final year of the 5-year term), [S8] (Daily Average with Index Margin) |
| Performance trigger | a declared rate is credited whenever the index return ≥ threshold (0 in the example); otherwise 0 | [R1] |
| Threshold participation | listed as an available method; mechanics not documented in a retrieved source | [S8] |
| Multi-year (2-year, 5-year) point-to-point with participation rate | par applied to the cumulative index return over the term; par is declared for each year of the initial crediting period and the final-year rate is the one quoted | [S4][S2] |
| Term participation with annual performance credits | APC = APC rate × Interest Credit Basis in years 1–4 of a 5-year term (only if index up); TPC = par × (avg monthly index value in final year − start index)/start index × Interest Credit Basis at term end | [S6] |
| Balanced Allocation Strategy | earnings = index allocation × index performance + declared rate allocation × declared rate − strategy spread, floored at 0 for the term | [S11] |
| Extendable point-to-point (Nassau) | Account Return per §5 below | [S10] |

- **The 0% floor is on the index credit, not on the account value.** Midland National
  states explicitly that "deductions from the accumulation value for optional benefit
  riders or strategy fees or charges associated with allocations to enhanced crediting
  methods could exceed interest credited to the accumulation value, which would result
  in loss of premium" [S7].
- Index returns are computed on **price** indices in most cases and exclude dividends
  [S6][R1]; some products use total-return volatility-controlled indices (e.g. S&P 500
  Daily Risk Control 5% Index TR) [S2].
- **Proprietary volatility-controlled indices carry embedded costs** that reduce the
  credited return before any cap/par is applied: BNP Paribas MAD 5 deducts **0.50% p.a.
  servicing cost** calculated daily plus rebalancing/replication costs; AiPEX deducts
  **0.50% p.a.** servicing cost [S2]; the S&P 500 Dynamic Intraday TCA embeds a
  **2 bp × change-in-notional** transaction cost on rebalance plus an **annualized 12
  bp replication cost scaled by weight** [S10]; the Nasdaq-100 Volatility Control 15%
  Index deducts a daily financing charge equal to the Effective Federal Funds Rate ×
  exposure, with exposure ranging **0%–200%** and capped at a **±25 percentage point**
  daily change [S10].
- **Interest Credit Basis** (the amount the credit rate is applied to) is not always the
  current account value: Midland defines it as the Accumulation Value at the beginning
  of the term less withdrawals from that index account, and advisory fees taken pro rata
  from index accounts do **not** reduce it [S6]. Athene's Income Base simple-interest
  credit is on **Premium minus Withdrawals**, not on the rolled-up base [S2].

### 3. Guaranteed minimum index parameters (guaranteed elements)

| Product | Parameter | Guaranteed minimum |
|---|---|---|
| Allianz 222 [S4] | monthly cap (monthly sum) | 0.50% |
| Allianz 222 [S4] | annual cap (annual PTP) | 0.25% |
| Allianz 222 [S4] | annual participation rate (annual PTP and MY 2- and 5-year PTP) | 5% |
| Allianz 222 [S4] | fixed interest rate | 0.10% |
| Allianz Benefit Control [S3] | allocation charge | maximum 2.5% (current 0%) |
| Midland IndexMax ADV 5 [S6] | fixed account rate | 0.25% |
| Midland IndexMax ADV 5 [S6] | annual performance credit rate | 0.25% |
| Midland IndexMax ADV 5 [S6] | TPC participation rate (re-entry term) | 10% |
| Nassau Athos [S10] | fixed account rate (1-year) | 1% |
| Nassau Athos [S10] | participation rate (both PTP-with-participation accounts) | 5% |
| Nassau Athos [S10] | cap rate (S&P 500 PTP with cap) | 0.50% |
| Athene Ascent Pro [S1][S2] | bailout cap rate (contractual; 1.00% declared in 2022) | contract-specified |

Under ASOP No. 2 these are "guaranteed elements" that limit the NGE scale, and the
declared caps/par rates/spreads are NGEs to be reset only when anticipated experience
factors change, never to recoup past losses [R6].

### 4. Bonuses and vesting

| Product | Bonus | Credited to | Vesting |
|---|---|---|---|
| Athene Ascent Pro 10 Bonus [S2] | 3% premium bonus | Accumulated Value | 0/0/0/0/0/0/20/40/60/80/100% (Group A & C); 0/10/20/30/40/50/60/70/80/90/100% (Group B and CA) |
| Athene Ascent Pro 10 Bonus [S2] | Income Base bonus 25% (Option 1) / 15% (Option 2) | Income Base only | immediate (part of Initial Income Base) |
| Allianz Benefit Control [S3] | 25% premium bonus on premium paid in first 18 months | **PIV only** | requires lifetime withdrawals to realize; forfeited on full surrender; reduced proportionally on partial surrender |
| Allianz 222 [S4] | 45% PIV bonus | PIV only | requires ≥10 contract years then lifetime withdrawals |
| American Equity IncomeShield 10 [S5] | 7% premium bonus on first-year premium | Contract Value | 0/10/20/30/40/50/60/70/80/90/100%; **100% vested immediately on death** |
| Midland IncomeVantage [S8] | 2% GLWB value bonus | GLWB value only | not documented in the retrieved source |
| Nassau Athos [S10] | 16% (issue age ≤75) / 14% (76–80) | Accumulation Value | 0/0/15/20/30/40/50/60/70/85/100% |

- **Two distinct bonus mechanics must be modeled separately.** In the "AV bonus with
  vesting" design the bonus is in the account value from day one and a **non-vested
  portion is clawed back** on surrender or excess withdrawal. Nassau states the recovery
  formula explicitly: `(1 − vested%) × [bonus% / (1 + bonus%)] × (gross withdrawal −
  free withdrawal amount)` [S10] — note the `b/(1+b)` factor, which strips the bonus out
  of a bonus-inclusive account value rather than applying the bonus percentage directly.
  In the "benefit-base-only bonus" design (Allianz) the bonus never touches the AV, so
  there is nothing to claw back — it is simply forfeited if income is never taken [S3][S4].
- Bonus products carry an explicit disclosure that they "may include higher surrender
  charges, longer surrender charge periods, lower caps, higher spreads, or other
  restrictions" [S3], and Nassau adds that a premium bonus "should never be considered an
  'offset' to a penalty paid under the prior annuity, because it is repaid to the
  Company if you make certain withdrawals" [S10]. The free-look refund excludes the
  Premium Bonus [S10].

### 5. Interim values and mid-term crediting

The two most modelling-relevant interim-value designs retrieved:

**Nassau Athos "Extendable" accounts** [S10]:
- Account Value — basis for anniversary index credits.
- Daily Account Value — realized **plus unrealized** index credits for the current
  Segment; drives the death benefit and the Protected Account Value.
- **Protected Account Value = max( Account Value, 0.90 × max over prior Contract
  Anniversaries in the Segment of the Daily Account Value )**; it is the maximum amount
  available for full surrender before fees and charges.
- **Protected Account Return = max( 0, 0.90 × (1 + Account Return) − 1 )**.
- Cap accounts: Current Year Return = min( annual index return, cap × elapsed fraction
  of the contract year ) — so the cap accrues linearly through the year; Account Return
  compounds Current Year Returns across the Segment and is floored at zero.
- Participation accounts: on Extend, the modified participation rate applies
  **retroactively to the entire Segment**; on cap accounts the modified cap applies
  **only to the next contract year**.
- Index Credit Amount = Account Value at Segment Maturity × max( Account Return,
  Protected Account Return ); zero on all other days.
- **Index Credit Amount on Withdrawal** (mid-Segment partial credit) =
  `Gross Withdrawal × Protected Account Return / (1 + Protected Account Return)`.
- **Protected Account Value Reset**: automatic Reset (Account Value and Daily Account
  Value set to the Protected Account Value, new Segment starts) if the Protected Account
  Value ≥ the Daily Account Value on a Contract Anniversary.

**Nationwide New Heights "Balanced Allocation Value" (BAV)** [S11]:
- BAV = max( contract value + strategy earnings not yet credited, return-of-purchase-
  payment guarantee amount ); tracked daily; earnings credited at the end of each
  strategy term.
- Full earnings-to-date credited on the free withdrawal amount; **pro-rata** earnings on
  withdrawals above it; earnings-to-date credited on death.
- Optional one-time index-value lock-in per strategy term plus automatic end-of-term
  lock-in; BAV never falls below its start-of-term value.

Allianz's **Index Lock** is a different (simpler) form of the same idea: the owner locks
an index value once per crediting period, or via Auto Lock, guaranteeing a positive
index credit for that period regardless of subsequent index moves; not available on all
allocation options [S3].

### 6. Surrender charge schedules (as retrieved)

| Product | Yr1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15+ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Athene Ascent Pro 10 Bonus, Group A [S2] | 12 | 12 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 4 | 0 | | | | |
| Athene Ascent Pro 10 Bonus, Group B [S2] | 8.3 | 8.0 | 7.1 | 6.2 | 5.3 | 4.4 | 3.5 | 2.6 | 1.6 | 0.9 | 0 | | | | |
| Athene Ascent Pro 10 Bonus, Group C [S2] | 10 | 10 | 10 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 0 | | | | |
| Athene Ascent Pro 10 Bonus, CA [S2] | 8.2 | 7.7 | 6.6 | 5.6 | 4.5 | 3.4 | 2.3 | 1.2 | 0.1 | 0 | 0 | | | | |
| Allianz Benefit Control [S3] | 9.30 | 9.30 | 8.30 | 7.30 | 6.25 | 5.25 | 4.20 | 3.15 | 2.10 | 1.05 | 0 | | | | |
| American Equity IncomeShield 10 (ages 18–80) [S5] | 9.1 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 | | | | |
| Midland IndexMax ADV 5, initial term [S6] | 6.0 | 6.0 | 5.0 | 4.0 | 3.0 | — | | | | | | | | | |
| Midland IndexMax ADV 5, re-entry term [S6] | 3.0 | 3.0 | 2.5 | 2.0 | 1.5 | — | | | | | | | | | |
| Midland Capital Income (CA example) [S7] | 6 | 6 | 5 | 4 | 3 | | (7-yr period) | | | | | | | | |
| MNL IncomeVantage 10 [S8] | 10 | 10 | 10 | 10 | 10 | 9 | 8 | 6 | 4 | 2 | 0 | | | | |
| MNL IncomeVantage 14 [S8] | 10 | 10 | 10 | 10 | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
| Nassau Athos [S10] | 12 | 12 | 12 | 11 | 10 | 9 | 8 | 7 | 6 | 4 | 0 | | | | |

Charge base: Nassau states it as **(Gross Withdrawal − Free Withdrawal Amount) ×
charge %** [S10]; Midland applies the charge to "any amount above the available
penalty-free withdrawal amount" [S6]; Athene applies it to withdrawals exceeding the
free amount [S1].

### 7. Market value adjustment (MVA) formulas

Three distinct formula families were retrieved verbatim.

**(a) Ratio-of-yield-factors form (Nassau Athos)** [S10]:
```
MVA multiplier = [ (1 + i_0) / (1 + i_t) ] ^ (n / 12)  -  1
MVA            = ( Maximum Gross Withdrawal - Free Withdrawal Amount ) x MVA multiplier
```
`i_0` = MVA Index at issue; `i_t` = MVA Index at the time of withdrawal/surrender;
`n` = months remaining to the end of the Surrender Charge Period.
Worked: 24 months remaining, 3.00% → 4.00% gives [(1.03)/(1.04)]^2 − 1 = −0.0191, and
($100,000 − $7,000) × −0.0191 = −$1,776 [S10].
Limit: `MVA limit = max(0, Maximum Gross Withdrawal − charges and adjustments − TGV)`;
a negative MVA combined with charges never reduces CSV below TGV, and the maximum
positive MVA cannot exceed the maximum negative MVA [S10].

**(b) Linear rate-difference-times-duration form (Midland National)** [S6][S7]:
```
MVA = ( i_0 - i_t ) x T
```
applied to the portion of the withdrawal exceeding the penalty-free amount, **before**
reduction for any surrender charge. `i_0` = index value of the MVA external index on the
issue date [S7] or on the start date of the five-year term [S6]; `i_t` = index value at
the time of surrender; `T` = (days from the surrender to the end of the current contract
year ÷ 365) + whole years remaining in the MVA period. **MVA external index = Barclay's
US Credit Index** [S6][S7].
Collar: positive MVA ≤ min(A, B); negative MVA ≥ −min(A, B), where A = the applicable
surrender charge, and B = (all states except CA) total interest credited to the AV since
issue − sum of positive MVAs applied since issue + sum of negative MVAs applied since
issue; (CA) **0.50% × AV at withdrawal** [S6][S7].

**(c) Deadband/direction description (Athene Ascent Pro)** [S1]: "If interest rates have
increased, stayed the same, or decreased by **less than 0.25%**, the MVA will be
negative. If interest rates have decreased by **more than 0.25%**, the MVA will be
positive." The full formula is in Athene Form 17653 / the Certificate of Disclosure,
neither of which was retrieved. MVA is not applicable in all states (no MVA in MO) [S2].

**(d) Directional description only (Allianz)** [S3]: bond yields lower at withdrawal →
higher CSV; equal → unaffected; higher → lower CSV. Bounded so the CSV can never be
below the guaranteed minimum value or above the AV.

**(e) Directional description only (American Equity)** [S5]: as the MVA Index increases,
CSVs decrease. MVA does not apply to Free Withdrawals, death benefit, MGSV, or
distributions after the surrender charge period.

Common across all: MVA applies **only** to the portion above the free withdrawal amount
and **only** during the surrender charge / MVA period, is not applied to the death
benefit, and cannot push the surrender value below the nonforfeiture minimum
[S1][S5][S6][S7][S10][R1].

### 8. Free withdrawals and RMDs

| Product | Free withdrawal | First available |
|---|---|---|
| Athene Ascent Pro [S1][S2] | 10% of Accumulated Value | Contract Year 1 |
| Allianz Benefit Control [S3] | 10% of **paid premium** | contract year after the most recent premium |
| American Equity IncomeShield 10 [S5] | 10% of Contract Value | after year 1 |
| Midland IndexMax ADV 5 [S6] | 10% of beginning-of-year AV | year 2 |
| MNL IncomeVantage [S8] | **5%** of AV | year 2 |
| Nassau Athos [S10] | **7%** of the Daily Accumulation Value at the prior anniversary | year 2 (none in year 1) |

Unused free withdrawal does not carry forward [S9][S10]. RMDs are treated as free
withdrawals — contractually at Athene [S1] and Nassau [S10], and **by current company
practice** (explicitly non-guaranteed) at Midland [S6][S8]. Allianz treats RMDs as
penalty-free withdrawals that reduce the PIV proportionally [S3].

A subtle point that matters for cash-flow modeling: Allianz still credits index interest
on amounts taken as free withdrawals earlier in the contract year, prorated for the
portion of the year the money remained in the indexed allocation [S3]; Athene by
contrast states "Withdrawals are not credited with index interest in the year they are
taken" [S1]; Nassau credits a partial index credit on withdrawal using the formula in
§5 [S10]; Nationwide credits full earnings-to-date on the free withdrawal amount and
pro-rata earnings above it [S11].

### 9. Nonforfeiture minimum

- Minimum nonforfeiture amount = accumulation of **87.5% of gross considerations**, less
  accumulated withdrawals, less an accumulated **$50 annual contract charge**, less
  accumulated premium tax paid, less indebtedness [R2 §4A].
- Nonforfeiture interest rate = **min(3%, max(0.15%, 5-year CMT − 125 bp))**, with the
  CMT observed as of a date or averaged over a period specified in the contract, no more
  than 15 months before issue or redetermination, rounded to the nearest 1/20 of 1%
  [R2 §4B].
- **FIA-specific**: an additional reduction of **up to 100 bp** may be taken during any
  period in which the contract provides "substantive participation in an equity indexed
  benefit," provided the present value of the additional reduction does not exceed the
  market value of the benefit [R2 §4C]. Model #806 §7 makes this operational: compute
  the annualized option cost of the guaranteed index features over the Index Term; if it
  is **≥25 bp** the benefit provides substantive participation and the reduction is the
  **lesser of 100 bp and the annualized option cost**, certified by an Academy member at
  filing and annually thereafter [R3].
- Contracts with equity-indexed benefits may carry **more than one nonforfeiture rate**;
  the contract minimum is the sum of per-benefit minimums, with prescribed rules for
  transfers between benefits, for excess withdrawals (deduct from the benefit with the
  **lowest** nonforfeiture rate first), and for allocating contract charges and premium
  taxes pro rata by contract value [R3 §6B].
- As implemented in product documents: American Equity MGSV = **87.5% of premium
  received, less withdrawals, accumulated at the minimum guaranteed interest rate**
  [S5]; Midland minimum surrender value = **87.5% of all premiums less surrenders (after
  MVA or surrender charge reduction), accumulated at a rate not less than the rate
  required or directed by the contract** [S6]; Nassau TGV = **87.5% of premium excluding
  the Premium Bonus**, split into Fixed and Indexed Guaranteed Values accumulated at
  their respective rates ranging **0.15%–3%** [S10]. Note that the Nassau TGV
  excludes the bonus from the 87.5% base, and that the 0.15%–3% range is exactly the
  Model #805 §4B floor and ceiling [R2].
- Rider charges may be deducted from the guaranteed minimum value as well as the account
  value: Athene deducts the Rider Charge monthly from **both** the Accumulated Value and
  the MGCV (except in certain states) [S1][S2]; Allianz deducts the allocation charge
  from the accumulation value **and the guaranteed minimum value in most states**
  [S3][S4].

### 10. GLWB rider mechanics

**Benefit base rollup — three distinct forms observed:**

| Design | Rollup form | Rate | Period | Source |
|---|---|---|---|---|
| Athene Ascent Income Rider, Option 1 | **simple** interest on *premium less withdrawals* | 10.00% yrs 1–10, 5.00% yrs 11–20 | to income start or 20 yrs | [S1][S2] |
| Athene Ascent Income Rider, Option 2 | simple interest **+ stacking** of 200% of interest credits | 5.00% yrs 1–10, 2.00% yrs 11–20; 200% stacking | to income start or 20 yrs | [S2] |
| Allianz Benefit Control | **no fixed rollup**; PIV grows only by the interest bonus factor × index credits | 250% (Accelerated) or 150% (Balanced) of index credit | until income starts | [S3] |
| Allianz 222 | as above | 150% PIV interest bonus | ≥10 yrs before PIV accessible | [S4] |
| American Equity LIBR | **compound** (Options 1, 3, 5) or **simple** (Options 2, 4) at a declared IAV Rate | rate guaranteed 15 yrs (Opt 1), 7 yrs (Opt 2, 4), 10 yrs then ≥ minimum (Opt 3, 5) | to income start or end of Accumulation Period | [S5] |
| MNL IncomeVantage | **stacking roll-up**: 2% of the GLWB value **plus** 150% of the dollar interest credited to the AV | 2% + 150% stack | not documented | [S8] |
| Nassau Amplified Income Plus | **simple** roll-up on the *Adjusted Initial* Income Benefit Base **plus** an Echo of 150% of (fixed interest + index credits − strategy fees), floored at 0 | 3% roll-up; 150% Echo | first **15** contract anniversaries, if not exercised | [S9] |

- Distinguish carefully: Athene's simple rollup is on **premium less withdrawals** [S2];
  Nassau's is on the **Adjusted Initial Income Benefit Base** [S9] — both produce a flat
  dollar increment, not a percentage of the current (grown) base.
- The Athene, MNL and Nassau designs all "stack" a multiple of realized index credits on
  top of the guaranteed rollup. The Allianz design is pure stacking (no guaranteed
  rollup at all), with the trade-off that in the Accelerated option only **50% of index
  credits reach the AV** [S3].
- **Step-up / ratchet to account value:** American Equity ratchets the IAV to the
  Contract Value on the day before income begins if the Contract Value is higher [S5];
  Nassau computes the Annual Benefit Amount on **the greater of the Income Benefit Base
  and the Accumulation Value at exercise** [S9]. No retrieved document describes an
  annual automatic ratchet during deferral, although Allianz's income-phase design
  ratchets the *withdrawal amount* upward whenever interest is credited and locks the
  higher level in [S3].

**Withdrawal percentages by attained-age band:** see the tables at [S1] (Athene, single
year of age 50–90, three payout options, joint = single − 0.50%), [S3] (Allianz Benefit
Control, five bands 50–80, single and joint), [S4] (Allianz 222, three bands 60–100,
single and joint), and [S5] (American Equity, single year of age 50–80 **by sex**, plus a
joint column). American Equity's use of **sex-distinct** single-life factors is notable
— Montana requires gender-neutral issue using the female factors [S5].

**Rider charge and its base:**

| Product | Charge | Base | Deducted from | Continues after AV = 0? |
|---|---|---|---|---|
| Athene Ascent Income Rider [S1][S2] | 1.00% p.a., monthly | **Income Base** | Accumulated Value **and MGCV** (not MGCV in some states) | not documented in retrieved sources |
| Allianz Benefit Control / 222 [S3][S4] | none explicit (allocation charge 0%, max 2.5%, on the AV and in most states the guaranteed minimum value) | AV | AV and guaranteed minimum value | n/a |
| American Equity LIBR [S5] | fee varies by option; **Option 1 has no fee** | not stated in the retrieved brochure | **Contract Value**, annually | n/a — rider terminates when Contract Value hits 0 by excess withdrawal |
| MNL IncomeVantage [S8] | none explicit ("included at no additional cost") | n/a | n/a | n/a |
| Nassau Amplified Income Plus [S9] | **0.95%**, annually at end of contract year; may be changed after the 15th contract year but never above **1.50%** | **Income Benefit Base** | Accumulation Value (Fixed Account first, then pro rata across Indexed Accounts), **after** index credits are added; proportional fee on surrender / excess withdrawal / termination | fee ceases when the rider terminates; the rider survives AV = 0 caused by fees or income payments, so **income continues without further fee deduction** [S9] |

Nassau's signature page requires the owner to acknowledge that the fee "will continue
even after the surrender charge period on my contract has ended" [S9].

**What happens when the account value reaches zero (the load-bearing GLWB rule):**
- Athene: if **Lifetime Income Withdrawals** (not an Excess Withdrawal) drive AV to zero,
  income continues for life in the "Extended Income Guarantee Phase"; Level and
  Inflation-Adjusted stay level, **Earnings-Indexed increases 1% annually**. If **Excess
  Withdrawals, Withdrawal Charges or MVAs** drive AV to zero, payments stop and the rider
  terminates [S1].
- Nassau: income continues if AV is reduced to zero "as a result of **rider fee
  deductions or guaranteed income payments**"; it stops and the rider terminates if AV
  hits zero "for **any other reason (including an Excess Withdrawal)**" [S9].
- American Equity: "Should excess withdrawals reduce the Contract Value to zero, the IAV
  will also be reduced to zero, and the contract as well as the rider will be considered
  Surrendered. Any remaining income payments would also terminate" [S5].
- Allianz: "Your lifetime withdrawals will continue even if you use up all the money you
  placed in the annuity"; the worked example runs the AV to zero at age 75 with income
  continuing [S3].
- General: "It allows policyholders to take withdrawals… guaranteed for the remainder of
  their life… even if their account balance is reduced to $0. And unlike annuitization
  benefits, the owner has access to their account balance" [R1].

**Excess withdrawal treatment.** Two proportional-reduction conventions appear:
- **Simple pro-rata on the account value** (before income starts, and in most designs
  after): the benefit base falls by the same percentage as the account value
  [S1][S3][S5][S9].
- **Post-exercise excess convention (Nassau, stated with a worked example)**: reduction
  percentage = `Excess Withdrawal ÷ (Accumulation Value − Annual Benefit Amount)`, i.e.
  the denominator is the AV **after** the guaranteed payment has been taken [S9].
- RMDs above the guaranteed amount are generally **not** excess withdrawals once income
  has started [S1][S9], but do reduce the base pro rata before income starts [S1][S9].

**Income doubler / enhanced benefit triggers:**

| Product | Trigger | Waiting period | Multiplier | Duration | Exclusions |
|---|---|---|---|---|---|
| Athene Enhanced Income Benefit [S1][S2] | confinement to a Qualified Care Facility **180 of 250 days** (90 of 125 in AK, AZ, CT, HI, ID, IL, LA, MN, MO, NH, NJ, OR, PA, UT, WA) | 1 year in force; must be in Income Phase | **2×** | max **60 months** or until AV = 0 | not in CA, MA; unavailable once in the Extended Income Guarantee Phase |
| Allianz Income Multiplier (AIM) [S3] | unable to perform ≥**2 of 6 ADLs**, **or** confinement to a qualified hospital/nursing/assisted-living facility ≥**90 days in a consecutive 120-day period** | **5 years** in force | **2×** | until AV depleted, cumulative withdrawal amount exceeds AV, or recovery | — |
| American Equity Wellbeing Benefit (LIBR Options 4 & 5) [S5] | unable to perform multiple ADLs; **not confinement-driven** (home care qualifies) | **2 years** | an "income payment factor" (not quantified in the retrieved brochure) | up to **5 years** | only with Options 4 and 5 |

**Rider cancellation / termination:** Athene allows cancellation on or after the 10th
rider anniversary [S1][S2]; Allianz allows cancellation of the PIV and AIM riders at any
time (with forfeiture of the PIV) [S3]; Nassau prohibits cancellation before an
"Earliest Cancellation Date" and terminates the rider without value on the earliest of
death of the (surviving) Covered Person, the Income Benefit Base reaching zero, base
contract termination, assignment, elective cancellation after the Earliest Cancellation
Date, or a change of Covered Person, with **no refund of past fees** [S9].

**Spousal continuation:** Athene continues the rider in the Accumulation Phase, but in
the Income or Extended Income Guarantee Phase only if the Joint option was elected [S1];
Nassau's Spousal Life Option continues if the survivor elects Spousal Continuation as
Owner [S9]; American Equity requires the spouse to be sole primary beneficiary, elect
spousal continuation, and be at least age 50 [S5].

### 11. Waivers

| Product | Confinement / nursing home | Terminal illness |
|---|---|---|
| Athene Ascent Pro [S1][S2] | ≥60 consecutive days after year 1; up to 100% of AV; no withdrawal charge or MVA; **is an Excess Withdrawal → terminates the income rider**; not in MA (and no waivers in CA) | death expected within **1 year**; after the first anniversary, diagnosis at least 1 year after issue; up to 100% of AV, no charge/MVA; also an Excess Withdrawal → terminates the rider |
| American Equity [S5] | owners **under 75 at issue**; after year 1; ≥**90 days**; **one-time** withdrawal up to 100% of contract value; no charges or MVA | owners under 75 at issue; after year 1; one-time up to 100%; no charges or MVA |
| Midland IndexMax ADV 5 [S6] | after the first anniversary; up to 100% of AV without surrender charge or MVA; cannot be confined at issue; first qualifying joint annuitant only; automatic, no charge | not documented in the retrieved pages |
| Nassau Athos [S10] | after the first anniversary; ≥**90 consecutive days**; waives the **surrender charge only** — the Non-Vested Premium Bonus recovery and the MVA still apply | terminal illness = death expected within **six months**; after the first anniversary; surrender charge waived only |

The Nassau design is a materially different (less generous) waiver than the Athene /
American Equity / Midland designs, because bonus recovery and MVA survive the waiver
[S10].

### 12. Annuitization and payout options

- Midland IndexMax ADV 5: life income; life income with period certain; joint and
  survivor life income; income for a specified period; income for a specified amount.
  If elected during the surrender charge period the payout is based on the **surrender
  value**, not the accumulation value (Florida excepted: after the first contract year
  the payout is based on the accumulation value, with a restricted option list) [S6].
- Nassau Athos: Life Annuity with Specified Period Certain; Non-Refund Life Annuity;
  Joint and Survivorship Life Annuity; Installment Refund Life Annuity; Joint and
  Survivorship with 10-Year Period Certain; Payments for a Specified Period Certain;
  Payments of a Specified Amount. Payments based on the **greater of the Cash Surrender
  Value and the Daily Accumulation Value** on the Contract Maturity Date [S10].
- Allianz Benefit Control: standard annuity options available after the 5th contract
  year; payment based on the **greater of the AV or the CSV — not the PIV**; "in most
  cases, the PIV may provide you with an annual lifetime withdrawal amount that is
  greater than the amount you would receive based on your accumulation value" [S3].
- Nassau Amplified Income Plus: at the Contract Maturity Date, if AV > 0 the owner may
  elect lifetime payments of **1/12 of the Annual Benefit Amount** monthly in place of a
  base contract annuity option [S9].
- Model #805 §8 fixes the maturity date for minimum-value purposes at the later of the
  anniversary following the annuitant's 70th birthday and the 10th contract anniversary
  [R2].
- **Payout factors were not retrieved.** Athene publishes "Payout Factors" and "Payout
  Factors (Full Download)" documents for Ascent Pro 7 and 10 [S12], but they are served
  through a viewer that could not be fetched (see Gaps).

### 13. Issue ages, premium limits, and other issue-time parameters

| Product | Issue ages | Minimum premium | Maximum premium | Premium pattern |
|---|---|---|---|---|
| Athene Ascent Pro 10 Bonus [S2] | 35–80 (Group A/C); 35–74 (Group B) | $10,000 ($5,000 in AK, CT, HI, ID, MN, NJ, OR, PA, UT, WA) | $1,000,000 (more with approval) | single premium |
| Athene Ascent Pro 10 [S1] | not stated in the brochure | $10,000 ($5,000 in 16 named states) | $1,000,000 | single premium |
| Allianz Benefit Control [S3] | max issue age **80**; lifetime withdrawals from age 50 | **$20,000** | $1,000,000 without prior approval | additional premium for the first **18 contract months**, $25–$25,000 per payment |
| American Equity IncomeShield 10 [S5] | surrender schedule stated for ages **18–80**; LIBR issue ages **50–80**; Nursing Care / Terminal Illness riders for owners **under 75** | not stated in the retrieved brochure | not stated | initial premium allocable to any strategy; later premiums go to the fixed strategy |
| Midland IndexMax ADV 5 [S6] | not stated in the retrieved pages | not stated | not stated | **single premium only** |
| MNL IncomeVantage 10 / 14 [S8] | 40–79 / 40–75 (40–54 in CA) | $20,000 NQ and $20,000 Q | not stated | **flexible premium** |
| Nassau Athos [S10] | bonus tiers imply issue through age **80** (≤75 and 76–80); a section addresses "Applicants Nearing their 76th Birthday" | not stated in the retrieved pages | not stated | single premium |

Ownership rules (Athene): IRA must be single ownership with joint payout available for
spouses; nonqualified requires Owner = Annuitant, joint ownership only for spouses who
are also joint annuitants; non-natural owners permitted [S2].

### 14. Charges other than surrender charge and rider charge

- **Allocation charge** (Allianz): 0% current, **maximum 2.5%**, applies only to annual
  point-to-point and MY point-to-point allocations, deducted annually from the
  accumulation value and, in most states, the guaranteed minimum value. Post-issue it
  can only change when specified criteria are met — the annual average U.S. 10-year
  Treasury rate for the calendar year, corporate bond downgrades for the year, and
  investment-grade corporate bond defaults for the year [S3][S4].
- **Strategy fee / index margin** (Nassau, Midland): Nassau's Echo calculation nets
  "Strategy Fee Amounts" out of interest and index credits before applying the 150%
  factor [S9]; Midland offers crediting methods with an "Index Margin" (a spread) [S8].
- **Advisory fee** (fee-based FIAs): Midland IndexMax ADV 5 permits an authorized
  advisory fee of up to **1.5% of accumulation value annually**, treated as a partial
  surrender, subject to surrender charge and MVA if it exceeds the penalty-free amount —
  but pro-rata deductions from index accounts do **not** reduce the Interest Credit Basis
  [S6].
- **Model #805 annual contract charge**: the nonforfeiture minimum permits a **$50**
  annual contract charge to be deducted [R2]. No retrieved product document declares an
  actual annual policy fee.
- No M&E charge appears in any retrieved FIA document — M&E is a separate-account
  (variable annuity) construct and is absent from these general-account products
  [S1][S3][S5][S6][S10].

### 15. Reserves, capital and accounting (for model context)

- Statutory: **AG 33** (CARVM for annuities with elective benefits) + **AG 35** (index
  feature), Type 1 / Type 2 methods, quarterly certification, asset adequacy testing
  required for equity indexed annuity reserves [R1].
- **VM-22** principle-based reserving for non-variable annuities including FIAs:
  elective from 1/1/2026, mandatory for new business from 1/1/2029 [R1]; the VM-22 (A)
  Subgroup handles post-launch monitoring and revisions [R7].
- Nonforfeiture: Model #805 / #806 as in §9 above [R2][R3].
- GAAP: index feature = **embedded derivative** (Black-Scholes on the current index
  period plus future option budgets); GLBs/GMDBs = **market risk benefits** at fair value
  net of ascribed fees; remaining cash flows = host contract at a **host accrual rate**
  set so the total issue liability equals premium; DAC/DSI/URL are the intangibles [R1].
- Disclosure/illustration: NAIC Model #245 as in [R1] — three prescribed historical
  scenarios, 10-year index existence requirement, MVA-specific upside/downside
  illustration requirements.
- Suitability/best interest: NAIC Model #275 [R4], which is also the regulation named by
  Dodd-Frank §989J [R4].

### 16. Behavior assumptions to calibrate

- Dynamic lapse with a **shock lapse** in the year the surrender charge expires
  [R1][R8]. Quantitatively, in 2019–2020 the shock-year surrender rate was **10% with a
  GLWB rider versus 33% without** [R8].
- GLWB withdrawal utilization clusters at **95%–105% of the maximum available amount**;
  contracts in that band have the lowest surrender rates [R1].
- Withdrawal incidence 2019–2020: **37%** of GLWB contracts versus **<30%** of non-GLWB
  contracts [R8].
- Subsequent premium is rare on single-premium designs: **2.5%** of contracts in years
  2–10 made a deposit; **1.9%** with a GLWB, **3.3%** without [R8].
- Qualified contracts lapse less and withdraw more (especially 70+, RMD-driven);
  independent-agent business lapses more than bank or captive channels [R1].
- Deferred annuity mortality: qualified contracts have lower A/E than non-qualified per
  the SOA 2011–2015 study; FIAs without GLWBs showed an anomalous *increasing* A/E by
  account-value band [R1].
- 2023 study scope for a more current calibration: 17 companies, 57% of new sales, 2.7m
  contracts, $328bn exposure, 208,000 surrenders, $13.0bn withdrawals — detailed results
  behind a paid subscription [R9].

---

## Variations across insurers

1. **Where the bonus lands is the single biggest structural fork.**
   - *AV bonus with vesting and clawback* — Athene (3%) [S2], American Equity (7%) [S5],
     Nassau Athos (16%/14%) [S10]. The bonus is in the account value from day one, so it
     earns index credits, but a non-vested portion is recovered on surrender or excess
     withdrawal via a formula of the form `(1 − vested%) × [b/(1+b)] × (gross − free)`
     [S10].
   - *Benefit-base-only bonus* — Allianz Benefit Control (25% PIV bonus) [S3] and
     Allianz 222 (45% PIV bonus) [S4]. Nothing touches the AV; the bonus is realized only
     through lifetime withdrawals and is simply lost on surrender.
   These require genuinely different model code: the first needs a vesting vector and a
   clawback on the surrender path; the second needs a second value stream that never
   feeds the surrender benefit.

2. **Guaranteed rollup vs. pure stacking on the benefit base.** Athene (10% simple),
   American Equity (compound or simple declared IAV rate) and Nassau (3% simple) all
   guarantee a deferral rollup [S1][S2][S5][S9]. Allianz guarantees **none** — the PIV
   grows only when index credits are earned, multiplied by 150% or 250% [S3][S4]. Midland
   IncomeVantage sits between: 2% of the GLWB value **plus** 150% of dollar interest
   credited [S8]. The pure-stacking design shifts the deferral guarantee from the
   insurer to the market and is materially cheaper to hedge.

3. **Rider charge base and whether the rider is optional.**
   - Charged on the **benefit base**: Athene 1.00% of Income Base [S2], Nassau 0.95% of
     Income Benefit Base [S9]. This is the classic GLWB charge and grows as the base
     rolls up.
   - Charged on the **contract value**: American Equity LIBR [S5].
   - **No explicit charge at all**: Allianz [S3][S4] and MNL IncomeVantage [S8], which
     instead fund the guarantee through a lower AV interest factor (Allianz: 50% or 100%
     of index credits reach the AV) or lower caps/par rates (Midland's own disclosure
     says so explicitly [S8]).
   - **Built-in and mandatory** (Athene, Midland IncomeVantage) versus **optional**
     (American Equity, Nassau, Nationwide) [S1][S5][S8][S9][S11].

4. **Simple vs. compound rollup and the rollup base.** American Equity offers both
   simple (Options 2, 4) and compound (Options 1, 3, 5) with different guarantee
   durations and fee structures — a genuine within-insurer option menu [S5]. Athene and
   Nassau are simple, but on **different bases**: Athene rolls up on *premium less
   withdrawals* [S2], Nassau on the *Adjusted Initial Income Benefit Base* [S9]. Both
   yield a flat dollar increment; neither is "simple interest on the current base."

5. **Interim value sophistication.** Three tiers:
   - *No interim value* — account value only, with index credits granted at anniversary
     and no credit in the year of withdrawal (Athene: "Withdrawals are not credited with
     index interest in the year they are taken") [S1].
   - *Prorated / partial credit on withdrawal* — Allianz credits index interest on free
     withdrawals for the portion of the year the money was in the allocation [S3];
     Nassau credits `gross × PAR / (1 + PAR)` [S10].
   - *Full daily interim value* — Nassau Athos (Daily Account Value / Protected Account
     Value with a 90% Protection Level ratchet on anniversary highs) [S10] and Nationwide
     New Heights (Balanced Allocation Value tracked daily, with an optional one-time
     lock-in) [S11]. These are essentially a daily mark of the embedded option and are the
     hardest to model.

6. **Term structure.** Most products credit annually with annual reallocation
   [S1][S3][S5][S10]. Midland IndexMax ADV 5 is a **5-year term product with automatic
   re-entry into a second 5-year term carrying a fresh surrender charge and MVA period**
   [S6] — a design that requires modeling a restarting charge schedule. Multi-year
   participation-rate strategies (2- and 5-year) with year-by-year declared rates appear
   at Allianz [S4] and Athene [S2]. Nassau's "Extendable" accounts let the owner extend a
   Segment one year at a time, with participation-rate changes applying **retroactively
   to the whole Segment** and cap changes applying **prospectively only** [S10].

7. **MVA formula family.** Ratio-of-yield-factors `[(1+i0)/(1+it)]^(n/12) − 1` [S10]
   versus linear `(i0 − it) × T` [S6][S7]. The linear form is unbounded in principle and
   is therefore always collared — Midland collars it at the lesser of the surrender charge
   and cumulative net interest credited (or 0.50% of AV in California) [S6][S7]. The ratio
   form is naturally bounded but Nassau still limits it to `max(0, gross − charges − TGV)`
   [S10]. Athene's design embeds a **0.25% deadband** — rates must fall by more than
   0.25% for the MVA to turn positive [S1].

8. **Free withdrawal percentage tracks the income orientation of the product.** The
   accumulation-oriented and hybrid products give 10% [S1][S3][S5][S6]; Nassau Athos (a
   high-bonus product) gives 7% and none in year 1 [S10]; MNL IncomeVantage (income-
   focused, built-in GLWB) gives only 5% [S8].

9. **Income doubler trigger.** Confinement-only with a long look-back (Athene: 180 of
   250 days) [S1] versus ADL-or-confinement (Allianz: 2 of 6 ADLs *or* 90 of 120 days)
   [S3] versus ADL-only, home-care-eligible (American Equity Wellbeing) [S5]. Waiting
   periods run 1 year (Athene), 2 years (American Equity), 5 years (Allianz). Duration
   caps: 60 months (Athene), 5 years (American Equity), open-ended until recovery or AV
   depletion (Allianz).

10. **What "most common / representative" looks like.** For a reference implementation,
    the design that best represents the mainstream 2020s U.S. FIA-with-GLWB is:
    - single premium, 10-year surrender charge grading roughly 9–10% down to 0–1%
      [S3][S5][S10];
    - an AV-credited premium bonus of a few percent with a 10-year vesting schedule and
      clawback on excess withdrawal [S2][S5][S10];
    - fixed account plus S&P 500 annual point-to-point with cap plus one or two
      volatility-controlled proprietary indices on uncapped multi-year participation
      rates [S2][S4][S10];
    - 0% floor on index credits, MVA on withdrawals above 10% free, nonforfeiture floor
      at 87.5% of premium accumulated at 0.15%–3% [S5][S6][S10][R2];
    - GLWB with a benefit base rolling up at a guaranteed simple rate for a 10–20 year
      deferral window plus a stacking credit on realized index interest, a rider charge
      of ~0.95%–1.00% **of the benefit base** deducted from the account value, age-banded
      single-life withdrawal percentages around 4.5%–5.5% at age 65 stepping up with
      attained age, joint life 0.5% lower, a 2× income doubler on ADL/confinement, and
      lifetime income continuing after the account value is exhausted **unless** the
      exhaustion was caused by an excess withdrawal [S1][S2][S9].
    The Athene Ascent Pro / Ascent Income Rider [S1][S2] and the Nassau Growth/Bonus
    Annuity + Amplified Income Plus [S9][S10] pair are the two most completely documented
    instances of this shape in the retrieved sources, and the Nassau pair is the one with
    verbatim formulas for every moving part (MVA, bonus clawback, interim value, excess
    withdrawal, rider fee). **Nassau is the recommended chassis for a first reference
    implementation**, with Athene's income rider as the reference for a simple-rollup +
    stacking + income-doubler benefit base.

---

## Gaps and caveats

1. **No full contract specimen was retrieved for any FIA.** Everything here comes from
   brochures, producer guides, rate sheets, and **signed disclosure statements**. The
   disclosure statements [S6][S9][S10] are the closest to contractual language and are
   the ones formulas were taken from, but they all say the contract prevails in a
   conflict. Athene's "Certificate of Disclosure," which is the document its brochure
   repeatedly defers to for the MVA formula, the MGCV definition, the Minimum Interest
   Credit percentage, and the rider phase definitions, **was not located publicly**.
2. **Athene rate sheets and payout factors could not be fetched.** The "Rates and
   Availability" and "Payout Factors" PDFs on athene.com are served through a
   password-protected Widen viewer [S-f1]; the only Athene declared rates in this file
   are from a **July 2022** distributor-mirrored product guide [S2] and are stale.
   Athene's current caps, participation rates, income-base rollup rates and rider charge
   are unverified as of the access date.
3. **American Equity's official document host would not resolve from this environment**
   [S-f3]; the IncomeShield 10 content came from a distributor mirror of the same form
   number (01SB1164-10) and is a **2019** brochure. Current IAV rates, the rider fee
   percentage and its base, and the Minimum Guaranteed IAV Rate are all undocumented.
   Notably, the retrieved brochure states the LIBR fee is "deducted from the Contract
   Value" without stating whether the **fee base** is the Contract Value or the IAV —
   this is a material modeling parameter and remains unresolved.
4. **Nationwide New Heights is under-documented here.** The current Select-series
   brochure returned HTTP 403 [S-f4], so the only Nationwide source is a 2017 strategy
   brochure [S11] with no numbers — no strategy spreads, index/declared-rate
   allocations, surrender charges, or rider terms. The BAS/BAV design is described
   qualitatively only.
5. **AG 33 and AG 35 were not retrieved in primary form** [R11]. All statements about
   them derive from the American Academy of Actuaries paper [R1]. The Type 1 / Type 2
   naming ("hedged as required" / "not hedged as required") is tagged [unverified].
6. **SEC Release 33-9152 and the Federal Register text of the Rule 151A removal could
   not be fetched** (403 and a redirect wall respectively) [R10]. The *American Equity
   Investment Life Insurance Co. v. SEC* citation and the specific conditions of
   Dodd-Frank §989J are tagged [unverified]. What **is** verified: NAIC Model #275's own
   drafting note stating that §989J "confirmed this exemption of certain annuities from
   the Securities Act of 1933 and confirmed state regulatory authority" and names Model
   #275 [R4]; and three currently-sold FIA disclosure documents asserting the contracts
   are not securities and are not SEC-registered [S6][S9][S10].
7. **VM-22 itself was not retrieved.** Only the NAIC subgroup charge page [R7] and the
   Academy paper's summary of effective dates [R1]. The 2026 Valuation Manual PDF was
   identified but not fetched.
8. **NAIC Model #245 (Annuity Disclosure) was not retrieved directly**; its illustration
   requirements are reported via [R1].
9. **The task brief's reference to "NAIC Models #250 and #275" appears to be partly
   misdirected.** #250 was retrieved and is the **Variable Annuity Model Regulation**,
   which by its own definition covers only separate-account products and therefore does
   not reach FIAs [R5]. #275 is correct and directly relevant [R4]. The FIA-relevant
   models are #805, #806, #245 and #275.
10. **SOA FIA experience study detail is paywalled.** The 2019–20 summary numbers in [R8]
    come from the SOA announcement page; the full report PDF 404'd. The 2023 study's
    detailed surrender/utilization tables require an Experience Studies Pro subscription
    [R9]. No table of surrender rates by duration or GLWB utilization by attained age was
    obtained — these will need to be sourced separately or assumed.
11. **Athene's Minimum Interest Credit and MGCV percentages are qualitative only.** The
    brochure says the Minimum Interest Credit is "a percentage of your Initial Premium
    less withdrawals and charges" and the MGCV guarantees "a minimum interest crediting
    rate on a percentage of your premium" [S1] — neither percentage nor rate is given.
12. **Whether the Athene rider charge continues after account-value exhaustion is not
    documented.** The brochure says the charge is deducted from the Accumulated Value and
    MGCV [S1], but the Extended Income Guarantee Phase begins when the Accumulated Value
    is zero, so the charge presumably stops; this is **not stated** in any retrieved
    source. Nassau, by contrast, is explicit that the rider survives AV = 0 caused by
    fees or income payments [S9].
13. **Monthly-sum floor convention is ambiguous.** The Academy's worked example applies a
    **0% monthly floor** as well as a 1% monthly cap [R1], which is unusual — most
    monthly-sum designs cap the upside monthly but let negative months subtract in full.
    Allianz declares a 1.70% monthly cap with a 0.50% guaranteed minimum monthly cap
    [S4] but the retrieved rate sheet does not state the monthly floor. Verify against a
    contract before implementing.
14. **Several products' state variations are extensive** (Athene's three withdrawal-charge
    state groups plus a separate CA schedule [S2]; Midland's CA and DE re-entry
    schedules and CA-specific MVA collar [S6]; Allianz's state-specific naming of the
    accumulation value interest charge [S3]). A reference model should pick one state
    basis and say so.
15. All declared rates recorded here are **non-guaranteed elements** subject to change at
    the insurer's discretion within the contractual guaranteed minimums, and are captured
    only as of the dates stamped on the documents (Allianz 222: 8/4/2026 [S4]; Athene:
    7/1/2022 [S2]). They are illustrative of parameter levels, not durable product
    constants [R6].
