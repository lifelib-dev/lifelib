# Fixed Deferred Annuity (multi-year guaranteed annuity / book-value fixed annuity) — research notes (U.S.)

Access date for all citations: 2026-08-04.

Purpose: source library and extracted specifications to drive a reference liability
cash-flow projection model (lifelib/modelx style) for U.S. individual fixed deferred
annuities of the multi-year guaranteed (MYGA) / book-value type, including the
market-value-adjusted (MVA) variants.

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). Facts stated from general knowledge and not verified against a
retrieved document are tagged [unverified]. The S#/R# numbering in this file is
local to this product and is independent of the cross-product library numbering
used in `regulatory-actuarial.md`.

Note on failed fetches: several aggregator-hosted brochures (immediateannuities.com)
returned HTTP 403 and one insurer host (media.american-equity.com) failed DNS
resolution. Those are listed with `retrieved: NO` and nothing is asserted from them.

---

## Primary sources

### S1. Athene Annuity & Life Assurance Company — "ATHENE MaxRate® Multi-Year Guarantee Annuity (MYGA) CA Version", producer fact sheet AN1007-CA (10/14)
- Publisher: Athene Annuity & Life Assurance Company (Wilmington, DE; main
  administrative office Greenville, SC). PDF hosted on iPipeline's forms
  repository, which distributes carrier-authored producer material.
- Doc type: producer product fact sheet (2 pages), "FOR PRODUCER USE ONLY".
- URL fetched: https://files.ipipeline.com/AALAC/AN1007CA.pdf
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Product is "a modified single premium deferred annuity contract that offers
    clients asset growth they can rely on with guaranteed interest rates."
  - Issue ages 0–80 (actual age), qualified and non-qualified.
  - Initial premium $5,000 minimum, $1,000,000 maximum; larger amounts with
    company approval.
  - Additional premium: minimum $500; up to 5 additional deposits allowed in the
    first 6 months.
  - Renewal mechanics: company declares a new rate for each subsequent guarantee
    period; "The rate will never be less than 1%."
  - 30-day window at the end of each guarantee period: owner may take a partial
    withdrawal, full surrender, or elect an income option with no withdrawal
    charges; if no instruction is received the contract automatically begins a new
    guarantee period of the same duration at a new guaranteed rate.
  - Initial guarantee period withdrawal charges, contract years 1–7:
    9%, 8%, 7%, 6%, 5%, 4%, 3%.
  - Subsequent (renewal) guarantee period withdrawal charges, contract years 1–7:
    5%, 5%, 5%, 5%, 5%, 4%, 3%.
  - Maximum subsequent-guarantee-period withdrawal charge by attained age (age on
    last contract anniversary): 94 → 4%; 95 → 3%; 96 → 2%; 97 → 1%; 98–100 → 0%.
  - "Free Out": during the last 30 days of each guarantee period the owner
    receives the accumulation value on withdrawal/surrender/income election.
  - Death benefit: beneficiary is paid the full accumulation value as of the date
    of death (state variations may apply).
  - Income options: available after the first contract year; based on the **cash
    surrender value** except during the 30-day window, when the full accumulation
    value applies. Options: fixed period; life income; life income with certain
    periods of 10 or 20 years.
  - RMDs are treated as any other withdrawal and are subject to withdrawal charges
    unless taken during the 30-day free-out window.
  - This CA version has **no** market value adjustment provision (MVA is not
    mentioned anywhere in the document).

### S2. Athene Annuity & Life Assurance Company of New York — "ATHENE MaxRate® Multi-Year Guarantee Annuity (MYG)", producer fact sheet AN1007-NY (06/16)
- Publisher: Athene Annuity & Life Assurance Company of New York (Nyack, NY).
- Doc type: producer product fact sheet (4 pages), New York only.
- URL fetched: https://files.ipipeline.com/AALAC/AN1007NY.pdf
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Two variants: base MaxRate and "MaxRate with Enhanced Liquidity".
  - Issue ages 0–80 (actual age), Q and NQ. Initial premium $10,000 min,
    $1,000,000 max. Additional premium min $500, up to 5 deposits in first 6 months.
  - Guarantee periods: 5-year and 7-year contracts. Guaranteed rate "will never be
    less than 1%"; company declares a new rate for each subsequent guarantee period.
  - Withdrawal charges: 5-year contract 7, 6, 5, 4, 3 (%); 7-year contract
    7, 6, 5, 4, 3, 2, 1 (%). Renewal (subsequent 5-year guarantee period) schedule
    for both: 5, 4, 3, 2, 1 (%).
  - Maximum subsequent-guarantee-period withdrawal charge by attained age: 94 → 4;
    95 → 3; 96 → 2; 97 → 1; 98–100 → 0.
  - Subsequent premium payments do not trigger a separate withdrawal charge
    schedule; the whole accumulation value renews on the base policy's schedule.
  - MVA (verbatim substance): "An adjustment is made to the accumulation value when
    withdrawal charges are assessed. The MVA reflects the change in interest rates
    from the time the guarantee period began to the time the withdrawal is made.
    The MVA may increase or decrease the accumulation value. The amount of MVA,
    positive or negative, will not be greater than the amount of the Withdrawal
    Charge." → two-sided MVA, **symmetrically capped at the withdrawal charge**.
  - 30-day free-out window: no MVA and no withdrawal charges; owner receives the
    accumulation value.
  - Death benefit: full accumulation value (no MVA, no withdrawal charge).
  - Income options: available after first contract year; based on the **full
    accumulation value**; fixed period, life income, life income with 10- or
    20-year certain.
  - RMDs subject to withdrawal charge and MVA on the base product; waived on the
    Enhanced Liquidity version.
  - Enhanced Liquidity waivers (highest single applicable waiver applies, not the
    sum):
    - 10% Free Waiver: after the first contract year, up to 10% of the accumulation
      value as of the last contract anniversary, no withdrawal charge or MVA. No
      benefit in the first contract year. Minimum partial withdrawal $500; minimum
      systematic withdrawal $100.
    - Substantially Equal Periodic Payments (SEPP) waiver: annual, must continue at
      least five years or to age 59½.
    - Confinement waiver: after the first contract year; owner or joint owner
      confined to a long-term care facility or hospital due to injury or sickness;
      confinement began while the contract was in force and has lasted 90
      consecutive days.
    - Terminal illness waiver: in any contract year after the first; physician
      certifies life expectancy ≤ 12 months and the owner was expected to live more
      than 12 months as of the contract date.
    - RMD waiver.

### S3. Voya Retirement Insurance and Annuity Company — "Voya Multi-Rate Annuity (Voya MRA)" prospectus, Form 424B3, dated May 1, 2021
- Publisher: Voya Retirement Insurance and Annuity Company (Windsor, CT), filed
  with the SEC.
- Doc type: statutory prospectus for a **single purchase payment, modified
  guaranteed deferred annuity contract** (39 pages, incl. Appendix I on the MVA).
  Product is closed to new sales as of this prospectus.
- URL fetched: https://www.sec.gov/Archives/edgar/data/837010/000010300521000017/definitivemultirateannuity.pdf
- Retrieved: YES (full text extracted, pages 1–17 and 37–39)
- Facts extracted:
  - Guaranteed Terms offered "for various lengths of time ranging up to and
    including ten years"; each has its own guaranteed interest rate, stated as an
    effective annual rate.
  - Minimum single purchase payment $10,000; minimum $1,000 into any single
    Guaranteed Term; payments over $1,000,000 only with consent; no additional
    purchase payments to an existing contract.
  - More than one guaranteed interest rate may apply within a Guaranteed Term
    greater than one year (e.g. one rate for years 1, another for 2–3, another for
    4–5). Not permitted in New York.
  - Guaranteed interest rates "will never be less than the minimum guaranteed
    interest rate stated in the contract"; Voya "observes no specific formula" and
    considers regulatory/tax requirements, sales commissions, administrative
    expenses, general economic trends and competitive factors.
  - Maturity handling: notice at least 18 days before term end; election form due
    at least 5 days prior; absent an election, automatic reinvestment into a term
    of equal duration, else next shortest, else next longest.
  - Early Withdrawal Charge schedule, by **years since the purchase payment was
    credited** (not years since the current term began):
    | Years since credited | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    |---|---|---|---|---|---|---|---|---|
    | Charge % of payment withdrawn | 7% | 7% | 6% | 6% | 5% | 4% | 2% | 0% |
    Once it declines to 0% it never reapplies, regardless of reinvestment. The
    charge applies only to withdrawals of the purchase payment, and withdrawals are
    assumed to come from purchase payment first (not earnings) for this purpose.
  - Special (free) withdrawal: after 12 months from the contract effective date,
    one withdrawal per calendar year of up to 10% of account value, no early
    withdrawal charge. Applies only to the first withdrawal each calendar year;
    all subsequent withdrawals that year are charged even if the full 10% was not
    used; excess over 10% on the first withdrawal is charged. **An MVA still
    applies to free amounts withdrawn before maturity.**
  - Early withdrawal charge waived for: withdrawal at the end of a Guaranteed Term
    (with ≥5 days' written notice); full surrender when account value ≤ $2,500 and
    no withdrawal in the prior 12 months; systematic distribution option (SWO/ECO)
    payments; involuntary termination (account value < $2,500).
  - Nursing home waiver (where approved): >1 account year elapsed since the
    purchase payment was credited; annuitant has spent ≥45 consecutive days in a
    licensed nursing facility; request within 3 years of admission (no 3-year limit
    in Oregon; non-licensed facility permitted in New Hampshire). Not waived if the
    annuitant was already in a facility at purchase.
  - Annual maintenance fee: none currently charged, but the contract permits one.
    Premium taxes 0%–4% depending on jurisdiction.
  - **MVA formula (Appendix I), exactly as stated:**
    ```
    MVA = [ (1 + i) / (1 + j) ] ^ (x / 365)
    ```
    where
    - `i` = the **deposit period yield**: identify the U.S. Treasury Notes maturing
      in the **last three months of the Guaranteed Term**; take their
      yield-to-maturity for the last business day of each week in the deposit
      period; average those percentages.
    - `j` = the **current yield**: the same Treasury Notes, yield-to-maturity for
      the **last business day of the week preceding the withdrawal**, averaged.
    - `x` = the number of days remaining in the Guaranteed Term, computed from the
      **Wednesday of the week of withdrawal**.
    The MVA is a **multiplicative factor** applied to the amount withdrawn from the
    Guaranteed Term. Factor > 1 → owner gains; factor < 1 → owner loses. No cap or
    collar on the factor is stated. It is fully two-sided.
  - Worked examples given in the prospectus (x = 927 days in all four):
    i = 4%, j = 6% → 0.9528; i = 5%, j = 6% → 0.9762; i = 6%, j = 4% → 1.0496;
    i = 5%, j = 4% → 1.0246. A $2,000 check request with factor 0.9528 requires a
    $2,099.08 withdrawal from the Guaranteed Term (i.e. gross-up for a negative MVA).
  - MVA applies on: withdrawal before term end; annuitization before term end (only
    a **positive** MVA is applied to amounts used to start a **lifetime** payment
    option); involuntary termination (< $2,500); contract cancellation; death
    benefit paid more than six months after the annuitant's death; death benefit on
    the death of a person other than the annuitant.
  - MVA does **not** apply to: SWO/ECO systematic distribution payments; death
    benefit paid within six months of the annuitant's death; amounts withdrawn at
    the end of a Guaranteed Term with ≥5 days' notice.
  - Death benefit: account value if paid within six months of the annuitant's
    death; account value adjusted by MVA if later or if the owner ≠ annuitant; may
    also be subject to an early withdrawal charge if owner ≠ annuitant.
  - Income phase: may start after the first contract year; default start is the
    later of the annuitant's 85th birthday or the 10th anniversary of the purchase
    payment. Minimum first payment $50 or total yearly payments $250. No early
    withdrawal charge on annuitization (MVA may apply). Age plus guaranteed-payment
    years must not exceed 95 at commencement for lifetime options with guarantees.
  - Free look / right to cancel: 10 days; refund equals the purchase payment.

### S4. Nationwide Life Insurance Company — "BOA Platinum Edge", Form S-1 registration statement / prospectus dated May 1, 2023, "Flexible Purchase Payment Modified Guaranteed Annuity Contracts Supporting Guaranteed Periods"
- Publisher: Nationwide Life Insurance Company (Columbus, OH), filed with the SEC
  (filed 2023-04-07).
- Doc type: registration statement containing the full prospectus, including
  Appendix A with MVA worked examples and a sensitivity table.
- URL fetched: https://www.sec.gov/Archives/edgar/data/1127203/000119312523095286/d490814ds1.htm
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Guaranteed Period Options (GPOs) of 3, 4, 5, 6, 7, 8, 9 and 10 years. A
    "Transition Account" holds unallocated money at a monthly-declared rate and is
    free of both MVA and CDSC.
  - The Specified Interest Rate is credited **daily**, producing an annual
    effective yield, and is guaranteed for the whole Guaranteed Period. New
    Specified Interest Rates are generally declared **weekly**. Nationwide
    "observes no specific method"; rates are influenced by fixed-income yields with
    compatible duration and by competitive considerations, administrative costs and
    general economic trends. Notably: **"there is no minimum Specified Interest
    Rate for any of the Guaranteed Period Options."**
  - Guaranteed Periods always end on a Maturity Date that is the last day of a
    calendar quarter, so an allocation not made on a quarter-end produces a term up
    to three months longer than the nominal N years.
  - Maturity notice at least 90 days prior, including the projected value at
    maturity. At maturity the owner may surrender in whole/part, transfer wholly or
    partially to other GPOs, or take no action (amounts move to the Transition
    Account) — all without MVA or CDSC.
  - Minimum purchase payments (initial/subsequent) vary by contract type; e.g. Tax
    Sheltered Annuity $10,000 / $1,000; SEP IRA and Simple IRA $2,000 / $1,000.
    Minimum $1,000 per Guaranteed Period Option elected.
  - Contingent Deferred Sales Charge (CDSC): "will not exceed 5% of the amount
    withdrawn"; no front-end sales charge. Measured by **completed years in the
    GPO from the date of the purchase payment**:
    - 10-year GPO: 5%, 5%, 4%, 4%, 3%, 3%, 2%, 2%, 1%, 1%, 0% for completed years
      0 through 10.
    - 5-year GPO: 5%, 5%, 4%, 4%, 3%, 0% for completed years 0 through 5 (the CDSC
      is simply not assessed once the GPO reaches its Maturity Date).
    Surrenders are taken first from the Transition Account, then pro rata across
    GPOs, unless the owner specifies otherwise.
  - Free withdrawal: each Contract Year the owner may withdraw without CDSC the
    **greater of** 10% of the Contract Value **or** any amount withdrawn to meet
    IRC minimum distribution requirements. **Non-cumulative** (unused free amounts
    do not carry forward). **An MVA still applies to free amounts withdrawn before
    the Maturity Date.**
  - CDSC also not deducted: on annuitization of contracts in force at least two
    years; on Transition Account amounts; on pre-maturity transfers between GPOs
    within the contract (though a new CDSC schedule then applies to the transferred
    amount); on death benefit paid before the Annuitization Date; on values held
    for the full Guaranteed Period.
  - Long-term-care waiver of CDSC: confinement to a long-term-care facility or
    hospital for a continuous 180-day period commencing while the contract is in
    force; either joint owner qualifies; request during confinement or within 90
    days after it ends.
  - **MVA formula, exactly as stated:**
    ```
    MVA Factor = [ (1 + a) / (1 + b + 0.0025) ] ^ t
    ```
    where
    - `a` = the Interest Rate Swap rate for a period equivalent to the Guaranteed
      Period, at the time of deposit into the GPO (rate published two days prior to
      the allocation date);
    - `b` = the Interest Rate Swap rate at the time of distribution for a period
      equivalent to the **time remaining** in the Guaranteed Period; in determining
      years to maturity, **any partial year is counted as a full year**, unless
      that would cause the number of years to exceed the Guaranteed Period (rate
      published two days prior to the withdrawal/transfer/distribution);
    - `t` = the number of days until the Maturity Date **divided by 365.25**.
    - The `+0.0025` (25 bp) is explicitly stated to account "for some of the
      administrative and processing expenses incurred when fixed-interest
      investments are liquidated." It makes the MVA structurally biased slightly
      against the owner.
    - Swap quotes are published for 1, 2, 3, 4, 5, 7 and 10 years; unpublished
      maturities (6, 8, 9) are interpolated from the relationship of the published
      rates (worked example: 5-year 6.00% and 7-year 6.50% → 6-year 6.25%).
    - The MVA Factor equals 1 during the Investment Period.
    - If Interest Rate Swaps cease to be published, Nationwide uses "appropriate
      rates based on the U.S. Treasury Bond yields."
    - The factor multiplies the Specified Value (allocation + accrued interest at
      the Specified Interest Rate − prior distributions), or the portion withdrawn.
    - No cap or collar on the factor is stated. Fully two-sided.
  - Appendix A worked examples (5-year GPO, $10,000 allocation, Specified Interest
    Rate 8.5%, 5-year swap at deposit 8%, surrender 985 days from maturity,
    Specified Value $12,067.96):
    - 3-year swap at surrender 7% → factor = [(1.08)/(1.07+0.0025)]^(985/365.25)
      = 1.01897 → surrender value $12,296.89.
    - 3-year swap at surrender 9% → factor = [(1.08)/(1.09+0.0025)]^(985/365.25)
      = 0.96944 → surrender value $11,699.17.
    (Note 985/365.25 = 2.69 which is stated to "round up to 3" for selecting `b`'s
    maturity, while `t` itself uses the exact day count.)
  - Appendix A sensitivity table for a 10-year GPO with `a` = 8%, showing the MVA
    percentage by current swap yield and time remaining. Selected values:
    | Current yield `b` | 9 yrs left | 7 yrs | 5 yrs | 2 yrs | 180 days |
    |---|---|---|---|---|---|
    | 12% | −29.35% | −23.68% | −17.56% | −7.43% | −1.88% |
    | 10% | −16.94% | −13.44% | −9.80% | −4.04% | −1.01% |
    | 9%  | −9.84%  | −7.74%  | −5.59% | −2.28% | −0.57% |
    | 8%  | −2.06%  | −1.61%  | −1.15% | −0.46% | −0.11% |
    | 7%  | +6.47%  | +5.00%  | +3.55% | +1.40% | +0.34% |
    | 6%  | +15.84% | +12.11% | +8.51% | +3.32% | +0.81% |
    | 4%  | +37.45% | +28.07% | +19.33%| +7.32% | +1.76% |
    The −2.06% at `b` = `a` = 8% is the pure effect of the 25 bp expense adder.
  - MVA is **not** applied to the death benefit. It **is** applied on annuitization
    before the Maturity Date.
  - Annuitization: Annuitization Date must be at least two years after issue (TSA
    exception with approval). Fixed payment annuity options: (1) Life Annuity;
    (2) Joint and Survivor Annuity; (3) Life Annuity with 120 or 240 Monthly
    Payments Guaranteed. Default if no election: fixed payment life annuity with a
    240-month guaranteed period. Default Annuity Commencement Date: age 70½
    (qualified/IRA/TSA) or age 90 (non-qualified). Payments below $50 trigger a
    frequency change; amounts below $5,000 may be paid as a lump sum.
  - Free look: 10 days; refund equals Contract Value **including any applicable
    MVA** (i.e. the free-look refund is market-value-adjusted, not premium).

### S5. Midland National Life Insurance Company — "Oak ADVantage® multi-year guarantee annuity", consumer brochure 34158Y REV 6-26
- Publisher: Midland National Life Insurance Company (West Des Moines, IA), a
  Sammons Financial Group member. Official insurer domain.
- Doc type: consumer product brochure (8 pages).
- URL fetched: https://www.midlandnational.com/documents/35453/349595425/34158Y+-+Oak+ADVantage+brochure.pdf/57b2f6a9-d3fc-65d4-c613-83f262f42fab?t=1724168079212
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Contract form ICC21-AS204A/AS204A; riders/endorsements ICC20-AR380A/AR380A and
    ICC19-AR360A/AR360A.
  - Guarantee periods: 3, 5 or 7 years. Issue ages "up to 90".
  - Minimum premium $50,000 (qualified and non-qualified). **Additional premium is
    not allowed.** No front-end charges and no annual fees; 100% of premium is
    credited.
  - "The declared fixed rate is an annual effective rate. Interest is credited
    daily."
  - Renewal: 30-day window at the end of the guarantee period to (a) take the value
    free of penalties, (b) renew into another 3-, 5- or 7-year period, or (c)
    annuitize. Default is automatic renewal into the same guarantee period, subject
    to not extending beyond the maturity date.
  - Early withdrawal (surrender) charge: **level 3%** in every contract year of the
    3-, 5- or 7-year surrender charge period (state variations possible).
  - Free withdrawal: after the first contract anniversary, an amount equal to the
    **interest earned in the prior contract year** (an interest-only design, not a
    10%-of-AV design). By current company practice, first-year interest is also
    available, and systematic interest withdrawals (monthly/quarterly/semi-annual/
    annual, minimum $50 each) are penalty-free.
  - By current company practice, RMDs based solely on this contract that exceed the
    available penalty-free amount may be withdrawn without surrender charge or MVA.
    ("Current company practice" is explicitly stated **not** to be a contractual
    guarantee and can be removed or changed at any time.)
  - Nursing home confinement waiver (not in all states): after the first contract
    year, up to 100% of contract value without surrender charge or MVA; cannot be
    confined at issue; included by rider at no charge.
  - Advisory fees: owner may authorize up to 1.50% of contract value annually to be
    paid to a financial advisor; treated as partial surrenders subject to surrender
    charge and MVA to the extent they exceed the free amount.
  - Death benefit: beneficiaries receive **the greater of the contract value or the
    minimum surrender value**, as a lump sum or installments.
  - Annuitization: payments based on the annuity's **surrender value**; by current
    company practice payments may be based on the accumulation value if (1) after
    the first contract year for a Life income option, or (2) the annuity has been
    in force at least five years and payments are taken over at least five years.
    Options (all states but Florida, 5–20 years for non-life options): income for a
    specified period; income for a specified amount; life income with period
    certain; life income; joint and survivor life income. Florida: options based on
    accumulation value after the first contract year — life income; life income
    with 10- or 20-year period certain; joint and survivor; joint and survivor with
    10- or 20-year period certain.
  - MVA: "may decrease or increase the annuity's surrender value depending on the
    change in the MVA external index rate"; inverse relationship to the index rate.

### S6. Midland National Life Insurance Company — "Oak ADVantage℠ multi-year guarantee annuity" highlight sheet 34199Y REV 11-24
- URL fetched: https://www.midlandnational.com/documents/35453/65313/34199Y+-+Oak+ADVantage+highlight+sheet.pdf/efeb0d27-884d-e0f2-535d-6430a37a58ac?t=1635796256861
- Doc type: 2-page product highlight sheet. Retrieved: YES.
- Facts extracted (in addition to / confirming S5):
  - "Surrender charges are a level 3.0% in each contract year" over a 3-, 5- or
    7-year surrender charge period.
  - "Beginning in year two, an amount up to the prior year's interest credited may
    be withdrawn without penalty."
  - "IRS-required minimum distributions (RMDs) are not subject to surrender charges
    or market value adjustments."
  - Advisory fee limit stated as up to **1.0%** on this (older, 11-24) version vs.
    1.50% on the 6-26 brochure [S5] — a documented change over time.
  - Death benefit: greater of accumulation value or minimum surrender value.
  - "The MVA, and the specific limits on your policy, are determined by your state."

### S7. Midland National Life Insurance Company — "Oak ADVantage® and Oak ADVantage® Care" rate sheet 32400Y REV 7-23-26 (interest rates effective July 23, 2026)
- URL fetched: https://www.midlandnational.com/documents/35453/349595419/32400Y+-+Oak+ADVantage+rate+sheet.pdf/fa83c185-49b5-ef49-afc7-fdf4da62b245?t=1726160212636
- Doc type: 1-page producer rate sheet. Retrieved: YES.
- Facts extracted:
  - Minimum premium $50,000 non-qualified and qualified.
  - Guarantee periods 3-year, 5-year, 7-year.
  - Declared rates shown on the sheet (rates effective July 23, 2026): 5.45%,
    5.60%, 5.50%, with a highlighted "5.60% guaranteed five-year". **Caveat:** the
    PDF lays the rates out in a graphic table and the text-extraction order does
    not unambiguously bind each rate to its guarantee period; the safest reading is
    3-year 5.45%, 5-year 5.60%, 7-year 5.50%, but treat the period-to-rate mapping
    as [unverified].
  - New business rate-lock rules: rate is based on the application signed date if
    (1) the application reaches the home office within 10 calendar days of signing
    and (2) the premium is received within 60 calendar days of signing.
  - Footnote: "A surrender during the surrender charge period could result in a loss
    of premium. The surrender charge and market value adjustment may reset with
    renewal."
  - Oak ADVantage Care contract form ICC25-AS504A/AS504A (a variant with care
    benefits).

### S8. Midland National Life Insurance Company — "Understanding the market value adjustment", 32340Y-2 REV 7-25 (Midland National Capital Income® fixed index annuity)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32340Y+-+Understanding+the+MVA/7446bfd5-4e75-8e71-db85-e055f63ea9de
- Doc type: 2-page consumer MVA explainer. Retrieved: YES.
- **Caveat:** this piece is written for the Capital Income *fixed index* annuity,
  not for Oak ADVantage. It is used here because it states the Sammons/Midland MVA
  formula and its caps explicitly, and Oak ADVantage uses the same MVA family
  [S5][S6]; do not attribute the numeric example to a MYGA.
- Facts extracted:
  - **MVA formula, exactly as stated:**
    ```
    MVA = (i0 − it) × T
    ```
    applied by multiplying "the portion of any full or partial surrender that
    exceeds any available penalty-free withdrawal amount, before the reduction for
    any surrender charge" by the formula result, where
    - `i0` = the index value of the MVA external index on the **issue date**;
    - `it` = the index value of the MVA external index at the time of the partial or
      full surrender;
    - `T` = time in years = (days from the surrender date to the end of the current
      contract year ÷ 365) + whole number of years remaining in the MVA period.
    - **MVA External Index = Barclay's US Credit Index.** (Formula varies by state.)
    This is a **linear duration × rate-change** MVA (a first-order approximation of
    the geometric forms in [S3][S4]), driven by a **corporate credit index yield**
    rather than Treasuries or swaps.
  - **Caps:** "The amount of MVA may be limited based on the interest credited
    and/or surrender charge." The worked example applies the cap as: MVA, positive
    or negative, limited to the surrender charge amount **or** the interest credited
    amount. Surrender value after surrender charge and MVA is guaranteed not to be
    less than the state-law minimum.
  - MVA applies only while the policy is within the MVA period (equal to the
    surrender charge period) and only on withdrawals exceeding the penalty-free
    amount, including full surrender.
  - "The MVA is not applied to the death benefit and may not apply upon
    annuitization. The MVA does not apply after the MVA period."
  - Worked example (Capital Income, 7-year SC/MVA period, $100,000 premium, 3%
    credited every year, 10% penalty-free allowance, surrender at end of contract
    year 5, SC 3%): accumulation value $115,927; free amount $11,593; surrender
    charge $3,130; interest credited $15,927; MVA reference rate 3.00% at issue.
    - Reference rate falls to 2.00%: MVA rate = (3.00% − 2.00%) × 2 = +2.00%;
      MVA = ($115,927 − $11,593) × 2.00% = +$2,086.69; surrender value $114,884.
    - Reference rate rises to 4.00%: MVA rate = (3.00% − 4.00%) × 2 = −2.00%;
      MVA = −$2,086.69; surrender value $110,711.
    (T = 2 here: 2 whole years remaining in a 7-year MVA period at the end of
    year 5.)
  - Surrender-charge schedule shown in the same example (Capital Income): year 1
    6%, year 2 6%, year 3 5%, year 4 4%, year 5 3%.

### S9. Midland National Life Insurance Company — "Midland National Capital Income® Fixed index annuity — Annuity disclosure statement", 32372Y-5 (8-24)
- URL fetched: https://www.midlandnational.com/documents/35453/9032621/32372Y+-+Capital+Income+disclosure+for+most+states/f334edb5-4545-608e-3e7b-f8558ed021b8
- Doc type: signed annuity disclosure statement (12 pages). Retrieved: YES.
- **Caveat:** FIA, not a MYGA. Cited here for (a) the contractually-precise MVA
  wording, (b) the nonforfeiture floor wording, and (c) the disclosure-statement
  structure that Model 245 [R4] drives.
- Facts extracted:
  - **Minimum surrender value / nonforfeiture floor, verbatim substance:** "The
    surrender value will never be less than the minimum requirements set forth by
    state law, at the time of issue, in the state where the Annuity Contract is
    delivered or issued for delivery. The minimum surrender value will never be less
    than **87.5% of all premiums less any surrenders (after MVA or reduction for
    surrender charges) accumulated at a rate not less than the rate required or
    otherwise directed by your Annuity Contract.**"
  - Surrender value = accumulation value, subject to MVA, less applicable surrender
    charges and applicable state premium taxes.
  - Surrender charge schedule (all states): year 1 6.0%, 2 6.0%, 3 5.0%, 4 4.0%,
    5 3.0%, 6 3.0%, 7 2.0%, 8 0.0%.
  - MVA text: applies only to withdrawals above the penalty-free amount; depends on
    changes in the MVA external index rate (Barclay's US Credit Index); "generally
    decreases the surrender amount when rates rise and increases the surrender
    amount when rates fall"; "An MVA will not reduce the amount surrendered below
    the minimum surrender value." Formula reproduced as MVA = (i0 − it) × T with the
    same definitions as [S8].
  - Penalty-free withdrawal: up to 10% of beginning-of-year accumulation value in
    any contract year; advisory fees are in addition to the penalty-free allowance.
  - Guaranteed rate floors for this FIA: minimum guaranteed fixed rate 0.25%;
    minimum index cap 0.50%; minimum participation rate 5.00%; maximum annual index
    margin 15.00%.
  - Annuitization: outside Florida, payout during the surrender charge period is
    based on the **surrender value** rather than the accumulation value; Florida
    payouts are based on accumulation value after the first contract year.
  - Free look 30 days (refund of premium less withdrawals).

### S10. MassMutual Ascend Life Insurance Company — "SecureGain 5 Annuity — A fixed annuity with a market value adjustment", consumer brochure B1088822NW 4/23
- Publisher: MassMutual Ascend Life Insurance Company (Cincinnati, OH), a wholly
  owned subsidiary of Massachusetts Mutual Life Insurance Company. (Formerly Great
  American Life.)
- Doc type: consumer brochure (12 pages) with a product-features specification table.
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/b1088822nw.pdf?sfvrsn=845c2fde_3
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Contract form P1088011NW / P1088011ID / P1088011OR; rider forms R6032310NW,
    R6032310OR, R6032410NW, R6032410OR.
  - Issue ages: qualified 0–89; non-qualified 0–89; Inherited IRA 0–75; Inherited
    non-qualified 0–75.
  - Single purchase payment of $10,000 or more. No upfront charges, no fees.
  - Initial term: five years.
  - Crediting design (distinctive): a **base interest rate** is set at issue; the
    first term year receives a **+0.25% bonus**; the base rate then **increases by
    0.10% each year** during the initial five-year term. Hypothetical illustrated in
    the brochure: 3.00% base → 3.25% (yr 1, base+bonus), 3.10%, 3.20%, 3.30%,
    3.40% (yrs 2–5).
  - After the initial term the rate is set at the company's discretion but never
    below the contract's guaranteed minimum interest rate, which "will be 1% or
    higher" per the brochure. (The 2025 rate flier [S11] states a **Minimum Interest
    Rate of 0.25%** for the current ICC24 form — a change over time.)
  - Penalty-free withdrawals: 10% of purchase payments during the first contract
    year; thereafter 10% of the account value on the most recent contract anniversary.
  - Early withdrawal charge (initial term): year 1 9%, 2 8%, 3 7%, 4 6%, 5 5%,
    6+ 0%.
  - MVA applies on surrender during the first five years and on withdrawals in
    excess of the 10% penalty-free allowance during the initial five-year term.
    Described as "comparing the interest rate environment when you purchase your
    contract to the environment when you choose to surrender."
  - Income payout options: fixed period; life or life with a minimum fixed period;
    joint and one-half survivor (survivor receives 50% for life).
  - Included waiver riders (both after the first contract year; not available in
    Massachusetts):
    - Extended care waiver rider: confinement to a nursing home or long-term care
      facility for at least **90 consecutive days** → withdraw up to 100% of account
      value with no early withdrawal charge.
    - Terminal illness waiver rider: physician diagnosis of terminal illness,
      defined as prognosis of survival of **12 months or less** (or longer if state
      law requires) → withdraw up to 100% of account value with no early withdrawal
      charge.
    - In California the Extended Care rider is replaced by a broader "Waiver of
      Early Withdrawal Charges for Facility Care or Home Care or Community-Based
      Services Rider".
  - Death benefit paid directly to beneficiaries, avoiding probate.

### S11. MassMutual Ascend Life Insurance Company — "SecureGain 5" client rate flier F1089525NW-1 (rates effective 09/22/25)
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/f1089525nw-1.pdf?sfvrsn=7b719de_1
- Doc type: 2-page rate flier with the disclosure footnotes. Retrieved: YES.
- **This is the single best retrieved statement of the nonforfeiture floor in a
  real product.** Facts extracted:
  - Contract form ICC24-P1172524NW. Not applicable in New York.
  - Declared initial rate for the 5-year term, effective 09/22/25: **4.45%** for
    purchase payments $100,000 and over; **4.10%** for purchase payments under
    $100,000. Rates apply to the initial purchase payment and are guaranteed until
    the fifth contract anniversary.
  - "Interest rates will never be lower than the annuity's **Minimum Interest Rate
    of 0.25%**."
  - **Guaranteed minimum surrender value (GMSV), verbatim substance:** "The
    guaranteed minimum surrender value (GMSV) equals **87.5% of purchase payments
    minus all prior withdrawals (not including early withdrawal charges or negative
    market value adjustments) plus interest credited daily at the GMSV rate of
    2.80%**. The GMSV will not be less than the minimum values required by the NAIC
    Standard Nonforfeiture Law for Individual Deferred Annuities, model #805, and
    the GMSV rate will not be less than the minimum rate required by each state."
    → an actual, current, product-specific GMSV rate of **2.80%** (below the 3% cap
    in Model 805 §4.B [R1]).
  - Early withdrawal charges and MVA "apply if you surrender your annuity or take
    withdrawals from it during each initial term **or any renewal terms**"; they do
    not apply to amounts covered by the 10% free withdrawal allowance.
  - For additional purchase payments, each term year ends on a contract anniversary,
    so the first contract year for an additional payment may be shorter than a year.
  - After the annuity payout initiation date the owner cannot surrender or withdraw.
  - 10% federal penalty tax on the taxable amount of payments received before 59½.

### S12. MassMutual Ascend Life Insurance Company — "How a market value adjustment works", S6075424NW 8/24
- URL fetched: https://mybusiness.massmutualascend.com/docs/default-source/default-document-library/forms/marketing-materials/s6075424nw.pdf?sfvrsn=d91920de_2
- Doc type: 2-page consumer MVA explainer. Retrieved: YES.
- Facts extracted:
  - **MVA reference indices:** "The interest rates used in the calculation are the
    **5-Year Treasury Constant Maturity Series published by the Federal Reserve
    and/or the BofA Merrill Lynch 5-10 Year US Corporate Bond Index.**" (A blended
    Treasury + corporate-credit reference.)
  - **Asymmetric cap:** "A **positive adjustment will never be greater than the
    early withdrawal charge** that applies to the withdrawal or surrender." and
    "A **negative adjustment will never reduce your surrender value to less than
    the minimum permitted under the standard non-forfeiture law of your state.**"
    The positive side is capped at the surrender charge; the negative side is
    floored by the SNFL minimum, not by the surrender charge.
  - "The potential MVA is based on the NAIC Standard Nonforfeiture Law for
    Individual Deferred Annuities model regulation, and as such the MVA minimums
    could vary by state."
  - Hypothetical (7-year early withdrawal charge period, $100,000 purchase payment,
    2.50% annual interest, full surrender at end of year 6): surrender value with
    no MVA $111,783; maximum positive MVA → $115,969; maximum negative MVA →
    $111,488. (Note the maximum negative MVA outcome here is above premium because
    the SNFL floor binds.)

### S13. New York Life Insurance and Annuity Corporation (NYLIAC) — "Secure Term MVA Fixed Annuity II — Just the facts", client fact sheet ML25-007661 / SMRU5821693 (Exp. 03.20.2028)
- Publisher: New York Life Insurance and Annuity Corporation (a Delaware
  corporation), wholly owned subsidiary of New York Life Insurance Company.
  Official insurer domain (nylannuities.com).
- Doc type: 4-page client fact sheet with full feature table and footnotes.
- URL fetched: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_ST_MVA_II_Generic.pdf
- Retrieved: YES (full text extracted). (An earlier WebFetch of the same URL and of
  an immediateannuities.com copy returned HTTP 403; the direct Python fetch
  succeeded.)
- Facts extracted:
  - Policy form ICC24D-P04 in most jurisdictions (NC24D-P04 in some states).
  - "Single premium fixed deferred annuity with several interest rate
    guarantee/surrender periods to choose from."
  - Issue ages: non-tax-qualified 0–85; tax-qualified 18–85; Inherited IRA /
    Inherited Roth IRA / Inherited non-tax-qualified 0–85. Single or joint
    annuitants (joint not available in NY).
  - Additional premiums not permitted. Minimum initial premium $5,000; premiums
    above $2,000,000 require NYLIAC approval.
  - Interest crediting bands (rate varies by premium size): $5,000–24,999;
    $25,000–49,999; $50,000–99,999; $100,000–1,499,999; $1,500,000 and over.
  - Initial interest rate guarantee periods of **3, 4, 5, 6 or 7 years**, each with
    a **matching surrender charge schedule**.
  - Rate-lock rules: to get the higher of the rate on the application-signed date or
    the premium-received date, the application and premium must be received within
    30 days of signing (60 days for funds coming via a NYLIAC-initiated 1035
    exchange/rollover/transfer, with the application within 30 days).
  - **Renewal mechanics:** "At the end of the initial interest rate guarantee period,
    the policy will receive a new renewal rate **each anniversary** that is based on
    the accumulation value. That rate will not be less than the guaranteed minimum
    interest rate (GMIR) stated in your policy." For policies issued in New York,
    the GMIR is **redetermined on each policy anniversary** after the initial
    guarantee period and will not be lower than **1.00%**. (i.e. the product does
    **not** roll into a new multi-year guarantee; it becomes an annually-declared
    contract.)
  - No annual policy maintenance or administration fee.
  - Withdrawals: minimum $100; accumulation value may not fall below $2,000 after a
    partial withdrawal.
  - **Free withdrawal amount each policy year — the greatest of:**
    (a) 10% of the accumulation value as of the last policy anniversary;
    (b) 10% of the current accumulation value;
    (c) 100% of the gain earned in the policy (only for policies with premium
        ≥ $100,000; not available in New York);
    plus RMDs as calculated by New York Life under the RMD Automated option.
  - Surrender charge schedules (most jurisdictions), by policy year, truncated at
    the length of the guarantee period selected:
    | Guarantee period | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
    |---|---|---|---|---|---|---|---|
    | 3 yr | 7% | 7% | 7% | | | | |
    | 4 yr | 7% | 7% | 7% | 6% | | | |
    | 5 yr | 7% | 7% | 7% | 6% | 5% | | |
    | 6 yr | 7% | 7% | 7% | 6% | 5% | 4% | |
    | 7 yr | 7% | 7% | 7% | 6% | 5% | 4% | 3% |
    New York schedules are the classic declining form: 3 yr 7/6/5; 4 yr 7/6/5/4;
    5 yr 7/6/5/4/3; 6 yr 7/6/5/4/3/2; 7 yr 7/6/5/4/3/2/1.
  - **MVA:** applies to surrenders and to withdrawals in excess of the
    surrender-charge-free amount **during the surrender charge period**. "The dollar
    amount of this adjustment is calculated by a formula that takes into account
    **the number of months left in the surrender charge period** and **the change in
    the yield to maturity value of a reference index** from the date that the policy
    was issued to the date of surrender or withdrawal." Increase in reference-index
    YTM → money deducted; decrease → money added. Policies issued in New York use a
    **different MVA formula** that "measures the change in U.S. Treasury Constant
    Maturity yield(s) and applicable corporate bond index(es) from policy issue date
    to the date of surrender or excess withdrawal."
  - **MVA floor:** "The MVA cannot decrease the surrender value of the policy below
    the premiums paid (less prior withdrawals and applicable charges and taxes)
    accumulated at the guaranteed minimum interest rate as stated in the policy."
    However, the surrender charge itself can still take the owner below premium.
  - MVA does **not** apply to death benefit payments, to RMDs as calculated by
    NYLIAC, or to withdrawals under the Living Needs Benefit/Unemployment Rider.
  - Death benefit: full accumulation value prior to annuitization.
  - Living Needs Benefit / Unemployment Rider (included, no charge, issue ages ≤85,
    minimum cash value $5,000, policy in force ≥1 year, qualifying event on/after
    the policy date). Qualifying events: enrolled and living in a health care
    facility for **60 consecutive days**; diagnosed life expectancy of **12 months
    or less**; total and permanent disability preventing any work for pay for at
    least **12 consecutive months**; qualifying for and receiving **state
    unemployment benefits for 60 consecutive days**. Full or partial waiver of
    surrender charges. Disability benefit not available for withdrawals/surrenders
    on or after the 66th birthday (charges and MVA then apply). Rider form ICC09-R100
    (209 100 in some states).
  - Optional Enhanced Beneficiary Benefit (EBB) Rider (form 201-306; not on IRA/Roth/
    inherited/SIMPLE/SEP policies; not in NY): pays a percentage of policy earnings
    at death. For issue age 70 or younger: **40% of earnings**, maximum benefit
    **100% of adjusted premium payments**, **rider charge 0.30% annual**, deducted
    as **0.075% of accumulation value each policy quarter**, locked at purchase,
    never to exceed 1% annually, and **discontinued after the 25th policy
    anniversary**. Cannot be cancelled once elected.
  - Optional Enhanced Spousal Continuance Rider (form 201-305), auto-included with
    EBB; sole-primary-beneficiary spouse may continue the policy including the EBB
    amount; exercisable once.

### S14. Symetra Life Insurance Company — "Form of Section 457 Contract Data Page", Exhibit 99.4(i) to Form 485BPOS for Symetra Separate Account C (filed 2009)
- Publisher: Symetra Life Insurance Company (Bellevue, WA), filed with the SEC.
- Doc type: **specimen contract data page** (bracketed values), for the Spinnaker
  Advisor Variable Annuity. Cited here only for the MVA on its **Guaranteed
  Interest Period Fixed Account Option**, which is a book-value fixed deferred
  annuity option with a classic "declared-rate differential" MVA. **Caveat:** this
  is a VA chassis, not a standalone MYGA, and the values are bracketed specimen
  values.
- URL fetched: https://www.sec.gov/Archives/edgar/data/0000912869/000119312509093761/dex994i.htm
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Maximum issue age for an annuitant [85]; maximum annuitization age [90].
  - Minimum initial purchase payment [$10,000]; minimum subsequent [$30]; minimum
    allocation $1,000 per selected Guaranteed Period.
  - Minimum guaranteed interest rate [1.50%].
  - **MVA formula, exactly as stated:**
    ```
    MVA = W × (Ic − In) × Fs
    ```
    where
    - `W` = the amount withdrawn, transferred, or annuitized from a Guaranteed
      Period under the Guaranteed Interest Period Fixed Account Option;
    - `Ic` = the interest rate, in decimal form, **credited** on the money
      withdrawn/transferred/annuitized;
    - `In` = the interest rate, in decimal form, that **would be credited on new
      money** allocated to a Guaranteed Period of the same duration as the one being
      taken from (i.e. the company's own current declared new-money rate, not an
      external index);
    - `Fs` = the adjustment factor, varying by the length of time remaining in the
      Guaranteed Period and by `Ic`;
    - `s` = number of whole years remaining; partial years are **interpolated**
      between whole-year adjustment factors.
  - **Adjustment factor (Fs) table, as printed:**
    | Years remaining | Fs where Ic < 6% | Fs where Ic ≥ 6% |
    |---|---|---|
    | 0 | 0.00 | 0.00 |
    | 1 | 0.90 | 0.90 |
    | 2 | 1.80 | 1.75 |
    | 3 | 2.60 | 2.50 |
    | 4 | 3.40 | 3.15 |
    | 5 | 4.10 | 3.80 |
    | 6 | 4.80 | 4.35 |
    | 7 | 5.40 | 4.85 |
    | 8 | 6.00 | 5.35 |
    | 9 | 6.50 | 5.75 |
    | 10 | 7.00 | 6.15 |
    These are effectively **modified-duration factors** (Fs ≈ annuity-immediate
    present-value factor for the remaining term), which is why the higher-rate column
    is uniformly lower. This is the cleanest closed-form MVA in the retrieved set
    for modelling: a first-order Macaulay/modified-duration approximation with the
    duration table hard-coded in the contract.
  - Transfer charge: 12 free transfers per certificate year; $10 or 2% of the amount
    transferred, whichever is less, thereafter. Premium tax deduction reserved.

### S15. Forethought Life Insurance Company (Global Atlantic) — "SecureFore II Fixed Annuities" product page
- Publisher: Global Atlantic / Forethought Life Insurance Company (Indianapolis, IN).
- Doc type: insurer web page (not a disclosure document).
- URL fetched: https://www.globalatlantic.com/retirement-annuities/fixed-annuities/securefore-ii
- Retrieved: YES (web page)
- Facts extracted:
  - SecureFore II is a MYGA with an MVA, offered in **3-, 5- or 7-year withdrawal
    charge periods**. Rates are "locked in and guaranteed not to change for the full
    Interest Guarantee Term", set at company discretion.
  - Free withdrawal: up to **10% of beginning-of-year Contract Value** (10% of the
    initial annuity deposit in the first year), plus any IRS-mandated RMD **even if
    it exceeds** the standard free withdrawal amount. State variations apply.
  - MVA applies during the withdrawal charge period on withdrawals exceeding the
    free withdrawal amount.
  - Included waivers: Nursing Home Waiver (in Florida requires 60 consecutive days
    of confinement and is unavailable until the first contract anniversary),
    Terminal Illness Waiver, and a **Chronic and Critical Illness Waiver** requiring
    the covered individual to be **age 65 or younger at contract issue**.
  - Contract/rider forms listed: FA1101SPDA-01, ICC17-FA1101SPDA-01, FA4012-02,
    ICC17-FA4012-02, FA4052-03, ICC20-FANC-01, FANHW-01, FATIW-01, ICC20-FATI-01,
    ICC20-FA4120-02, FA4120-03, ICC25-RA26-CCIW-01, RA26-CCIW-01.
  - Withdrawal charge percentages, issue ages, premium minima, death benefit and
    annuitization details were **not** stated on the page.

### S16. Oceanview Life and Annuity Company — "Harbourview Multi-Year Guaranteed Annuity — Product Disclosure", OVLAC-MYGA-DISC Rev. 01/20
- Publisher: Oceanview Life and Annuity Company. (A smaller MYGA specialist, not a
  "major" carrier — included because it is a genuine signed **MYGA product
  disclosure** in the Model 245 format, which the majors do not post publicly.)
- Doc type: 2-page signed product disclosure with owner/producer signature block.
- URL fetched: https://oceanviewlife.com/wp-content/uploads/2020/05/OVLAC-MYGA-DISC.pdf
- Retrieved: YES (full text extracted)
- Facts extracted:
  - Policy form ICC19 OLA SPDA-*; single premium deferred annuity; minimum premium
    $10,000.
  - "Interest is credited at the initial interest rate guaranteed for the first
    Guarantee Period. At the end of the Guarantee Period, and each subsequent
    Guarantee Period thereafter, a new rate will be declared... can never be less
    than the contract's minimum guaranteed rate at the time of your purchase. Your
    interest is credited and **compounded daily** to yield our declared annual rate."
  - No front-end sales charges or annual administrative fees.
  - Contract Value = 100% of all premiums and earned interest. Cash Surrender Value
    = Contract Value less cash withdrawals and applicable surrender charges and MVA.
  - Free withdrawal: after the first contract year, up to **10% of the Contract Value
    as of the prior Contract Anniversary**; multiple partial withdrawals permitted up
    to that amount with no surrender charge or MVA.
  - MVA applies only during the surrender charge period, only on surrender or on
    withdrawals exceeding the free amount. **"The Market Value Adjustment does not
    apply upon death of the owner(s) or the annuitant when the owner is a
    non-natural person, upon annuitization or after the surrender charge period."**
  - "Surrender charges and MVA are waived in the event of the Owner's death."
  - Payout options: life only; life with 10 years certain; fixed period; customized
    options available.
  - Premium tax deduction: "The Premium tax rate varies by state or municipality and
    currently ranges from 0 – 3.5%", deducted when the company pays the tax, on
    withdrawal, at income commencement, or at death benefit payment.
  - Surrender charges may be waived for some RMDs.

### S17. New York Life Secure Term MVA Fixed Annuity IV fact sheet (Fidelity-hosted copy)
- URL attempted: https://communications.fidelity.com/fili/docs/new-york-life-IV-factsheet.pdf
- Retrieved: **NO** — the server returned an HTML interstitial rather than the PDF
  (1,245 bytes, `<!DOC...`). Nothing is asserted from this document.

### S18. American Equity Investment Life — "GuaranteeShield℠ Single Premium Deferred Annuity" brochure 01SB1169
- URL attempted: https://media.american-equity.com/Documents/01SB1169.pdf
- Retrieved: **NO** — DNS resolution failure (`getaddrinfo ENOTFOUND
  media.american-equity.com`) on both WebFetch and direct HTTP. Search-engine
  summaries described a 3-/5-year MYGA with a 9/8/7/6/5 surrender charge schedule,
  a Market Value Adjustment Rider that does not apply to free withdrawals, death
  benefits, or post-surrender-charge-period distributions, and a 10%-of-prior-year-
  end free withdrawal from year 2 — but **none of that is verified** and is not
  relied upon below.

### S19. Aggregator-hosted brochures (immediateannuities.com)
- URLs attempted (all HTTP 403, Retrieved: **NO**):
  - https://www.immediateannuities.com/annuity-brochures/new-york-life-secure-term-mva-fixed-annuity-ii.pdf
  - https://www.immediateannuities.com/annuity-brochures/midland-national-guarantee-ultimate.pdf
  - https://www.immediateannuities.com/annuity-brochures/symetra-custom-7.pdf
- The New York Life content was obtained instead from the insurer's own domain [S13].
  Midland National Guarantee Ultimate and Symetra Custom 7 remain unverified.

---

## Regulatory and actuarial references

### R1. NAIC — Model #805, "Standard Nonforfeiture Law for Individual Deferred Annuities" (NAIC Model Laws, Regulations, Guidelines and Other Resources — Fall 2020)
- Publisher: National Association of Insurance Commissioners.
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (all 5 pages)
- Content extracted:
  - **§2 Applicability.** Does not apply to reinsurance, group annuities purchased
    under an employer/employee-organization retirement or deferred compensation plan
    (other than plans providing IRAs/individual retirement annuities under IRC §408),
    premium deposit funds, variable annuities, investment annuities, **immediate
    annuities**, any deferred annuity contract **after annuity payments have
    commenced**, reversionary annuities, or contracts delivered outside the state.
    §§3–8 do not apply to contingent deferred annuities.
  - **§3 Nonforfeiture requirements.** Contract must provide (1) a paid-up annuity
    benefit on cessation of considerations or on written request; (2) if a lump sum
    settlement is provided, a **cash surrender benefit** on surrender at or prior to
    commencement of annuity payments (payment may be deferred up to six months with
    the commissioner's written approval); (3) a statement of the mortality table (if
    any) and interest rates used; (4) a statement that benefits are not less than
    statutory minima. §3.B permits termination by cash payment if no considerations
    for two full years and the paid-up annuity at maturity from prior considerations
    would be under $20/month.
  - **§4.A Minimum nonforfeiture amount.** Equals an accumulation, at the §4.B
    rates, of the **net considerations** paid, **decreased by**:
    (a) prior withdrawals/partial surrenders accumulated at the §4.B rates;
    (b) **an annual contract charge of $50** accumulated at the §4.B rates;
    (c) any premium tax paid by the company, accumulated at the §4.B rates (only if
        actually paid and not later credited back); and
    (d) indebtedness including accrued interest.
  - **§4.A(2).** "The net considerations for a given contract year ... shall be an
    amount equal to **eighty-seven and one-half percent (87.5%)** of the gross
    considerations credited to the contract during that contract year."
  - **§4.B Interest rate — indexed nonforfeiture rate.** "The interest rate used in
    determining minimum nonforfeiture amounts shall be an annual rate of interest
    determined as **the lesser of three percent (3%) per annum** and the following,
    which shall be specified in the contract if the interest rate will be reset:
    (1) **The five-year Constant Maturity Treasury Rate** reported by the Federal
    Reserve as of a date, or average over a period, **rounded to the nearest 1/20th
    of one percent**, specified in the contract **no longer than fifteen (15) months
    prior** to the contract issue date or redetermination date; (2) **reduced by 125
    basis points**; (3) where the resulting interest rate is **not less than 15 basis
    points (0.15%)**; and (4) the interest rate shall apply for an initial period and
    may be redetermined for additional periods, with the redetermination date, basis
    and period stated in the contract."
    → **Important correction to the common description:** in the retrieved Fall 2020
    edition the floor is **0.15%, not 1%**. The corridor is therefore
    **0.15% ≤ i ≤ 3.00%**, with i = round(5-yr CMT, 1/20%) − 1.25%.
    [unverified] The original 2003 amendment set the floor at 1%; a subsequent NAIC
    amendment lowered it to 15 bp. The 1% floor is not in the retrieved text.
  - **§4.C Equity-indexed benefits.** During the period a contract provides
    substantive participation in an equity-indexed benefit, the 125 bp reduction may
    be **increased by up to an additional 100 basis points** to reflect the value of
    the equity index benefit, provided the present value of the additional reduction
    does not exceed the market value of the benefit.
  - **§5 Present value.** The paid-up annuity benefit's present value at the annuity
    commencement date must be at least the minimum nonforfeiture amount at that date,
    computed on the contract's stated mortality table and interest rates.
  - **§6 Cash surrender value.** Must not be less than the present value, as of the
    surrender date, of that portion of the maturity value of the paid-up annuity
    benefit arising from considerations paid before surrender, reduced appropriately
    for prior withdrawals/partial surrenders, **calculated at an interest rate not
    more than one percent (1%) higher than the contract's accumulation rate**, less
    indebtedness, plus additional amounts credited. "**In no event shall any cash
    surrender benefit be less than the minimum nonforfeiture amount at that time.
    The death benefit under such contracts shall be at least equal to the cash
    surrender benefit.**"
  - **§8 Maturity date.** For §§6–7 purposes, when optional maturity dates are
    permitted, the maturity date is deemed the latest permitted date, **but not later
    than the contract anniversary next following the annuitant's 70th birthday or the
    10th contract anniversary, whichever is later**.
  - **§9.** Contracts without cash surrender benefits or without death benefits at
    least equal to the minimum nonforfeiture amount must say so prominently.
  - **§13 Effective date.** Operative for contracts issued after the second
    anniversary of enactment, with optional earlier election on a form-by-form basis.

### R2. NAIC — Valuation Manual, Jan. 1, 2026 edition; **VM-22: Requirements for Principle-Based Reserves For Non-Variable Annuities**
- Publisher: NAIC (© 2025 NAIC). 457-page PDF; VM-22 begins at PDF page 227
  (manual page 22-1).
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (downloaded and text-extracted; VM-22 sections read directly)
- Content extracted:
  - **Title and status.** "VM-22: Requirements for Principle-Based Reserves For
    Non-Variable Annuities." §1.A: "For all contracts encompassed by the Scope,
    these requirements constitute the **Commissioners Annuity Reserve Valuation
    Method (CARVM)** and, for some contracts and certificates, the Commissioners
    Reserve Valuation Method (CRVM)." → VM-22 PBR **replaces** formulaic CARVM for
    in-scope non-variable annuities.
  - **§2.A Scope.** "Applicable non-variable annuity contracts specified in VM
    Section II, Subsection 2 'Annuity Products', Paragraphs C and D and applicable
    contracts in VM Section II, Subsection 3 'Deposit-Type Contracts' are subject to
    VM-22 requirements." (MYGAs / fixed deferred annuities fall in the Accumulation
    Reserving Category — see below.)
  - **§2.B Effective Date & Transition — verbatim:** "These requirements apply for
    **valuation dates on or after January 1, 2026**." Transition: a company may elect
    to reserve under VM-A/VM-C/VM-M/VM-V for business otherwise subject to VM-22 PBR
    and issued during the **first three years** following the effective date; once
    VM-22 PBR is elected for a block it must continue; and "a company shall apply
    VM-22 PBR requirements to all applicable blocks of business on a prospective
    basis **starting three years after the effective date**" (i.e. 2029).
  - **§3.A Aggregate reserve** = Stochastic Reserve (SR) + Deterministic Reserve (DR)
    for contracts passing the Single Scenario Test + reserves for contracts valued
    under VM-A/VM-C/VM-M/VM-V (those passing the exclusion test and electing not to
    model). §3.B: determined both pre- and post-reinsurance-ceded. §3.C: the
    **additional standard projection amount is required for disclosure purposes only**
    pursuant to VM-31, with a LATF guidance note (April 3, 2025 referral) directing
    attribution analysis and reiterating "the SPA is not a safe harbor."
  - **Reserving categories** (§4): "Payout", "Longevity Reinsurance", and
    "**Accumulation Reserving Category**" — "all annuities within scope of VM-22 that
    are not in the 'Payout Reserving Category' or 'Longevity Reinsurance Reserving
    Category'". Fixed deferred annuities / MYGAs sit here.
  - **§6.B.5 Full Surrenders — prescribed standard-projection lapse formula,
    verbatim:**
    ```
    Total Lapse = (Base Lapse × GMIR Factor + Rate Factor × MVA Factor) × ITM Factor
    ```
    with
    - ITM Factor = (0.75 ÷ ITM)² if ITM < 0.75 and AV ≠ 0; = 1 if 0.75 ≤ ITM ≤ 1.25
      and AV ≠ 0; = (1.25 ÷ ITM)² if ITM > 1.25 and AV ≠ 0; = 0 if AV = 0.
      ITM = GAPV ÷ Account Value. **Guidance note: "ITM = 1 for contracts in the
      Accumulation Reserving Category with no guaranteed living benefits or
      guaranteed death benefits."** → for a plain MYGA the ITM Factor is 1.
    - Rate Factor = Market Factor × Max(0, 1 − 5 × (1 − CSV/AV)).
      (The `1 − CSV/AV` term is essentially the surrender-charge + MVA haircut;
      the dynamic component switches off entirely once the haircut reaches 20%.)
    - **MVA Factor = 0 when MVA is in effect; 1 when MVA is not in effect.**
      → Under the prescribed assumption an in-force MVA **completely suppresses** the
      interest-rate-driven dynamic lapse component.
    - GMIR Factor: indexed annuities 1.00. **Fixed annuities: 1.25 if GMIR ≤ 1.0%;
      1.00 if 1.0% < GMIR ≤ 2.5%; 0.70 if GMIR > 2.5%.**
    - Market Factor = −1.25 × (CR − MR)^X if CR ≥ MR; = 0 if MR > CR ≥ (MR − BF);
      = 1.25 × (MR − BF − CR)^X if CR < (MR − BF). **X = 2.0 during the Surrender
      Charge Period, 2.5 at Shock, and 2.5 thereafter.**
    - **Minimum Lapse = 0.5%; Maximum Lapse = 90%** (not applicable if AV = 0).
    - CR = the crediting rate at the time of the projection (for indexed annuities,
      the options budget).
    - MR = market competitor rate. For **fixed annuities with Interest Guarantee
      Period ≥ 2 years:** MR = **N-year Treasury rate plus a 50% A / 50% AA spread
      minus Pricing Spread**, with **N = 5-year for 2 ≤ IGP < 5; N = 7-year for
      5 ≤ IGP < 7; N = 10-year for IGP ≥ 7**. For indexed annuities and fixed
      annuities with IGP < 2 years: MR = Max(3-month Treasury, 5-year Treasury plus
      50% A / 50% AA spread) minus Pricing Spread. **Pricing Spread = 0%.**
    - BF (Buffer Factor) = **50 bps**, the band in which no dynamic lapse occurs.
  - **§6 Table 6.5: Base Lapse Rates for Fixed Annuities with no Guaranteed Living
    Benefits** — the single most directly usable table for a MYGA model:
    | Years before/after surrender charge (SC) expiration | IGP ≤ 1 yr* | IGP > 1 yr, not in year of IGP expiry | In year of an IGP expiry after IGP > 1 yr |
    |---|---|---|---|
    | 3 yrs or more after expiry | 3.0% | 2.0% | 55.0% |
    | 2 yrs after expiry | 7.5% | 2.0% | 65.0% |
    | 1 yr after expiry | 10.0% | 2.0% | 75.0% |
    | Upon expiry | 25.0% | 6.0% | 75.0% |
    | 1 yr to expiry | 2.5% | 1.0% | 70.0% |
    | 2 yrs to expiry | 2.5% | 1.0% | 70.0% |
    | 3 yrs or more to expiry | 2.5% | 1.0% | 70.0% |
    (*includes floating rate structures.)
    Guidance-note worked examples, verbatim:
    - Example 1: initial 3-year IGP and 3-year SC period, then renewing into 1-year
      IGPs with no SC → base lapse rates in contract years 1–7 of
      **1%, 1%, 1%, 75%, 10%, 7.5%, 3%**.
    - Example 2: initial 3-year IGP and 3-year SC period, then renewing into another
      3-year IGP with 3-year SC period → contract years 1–7 of
      **1%, 1%, 1%, 75%, 1%, 1%, 75%**.
    - Example 3: initial 1-year IGP and 3-year SC period, then renewing into a 2-year
      IGP with no SC → contract years 1–6 of **2.5%, 2.5%, 2.5%, 25%, 1%, 65%**.
  - **§6 Table 6.4** (indexed annuities, no GLB) and **Table 6.6** (indexed and fixed
    annuities **with** GLBs) give attained-age-banded base lapse rates. Table 6.4's
    shock-year (upon expiry) rates are 33.5% / 41.5% / 37.0% / 23.5% for attained ages
    before 60 / 60–69 / 70–79 / 80+. Table 6.6's shock-year rates are
    18.5% / 14.0% / 11.0% / 8.5%.
  - **§6 Partial Withdrawals, Table 6.2 (Accumulation Reserving Category, Qualified):**
    attained age 59 and under 1.65% (no GLB) / 0.95% (with GLB, prior to exercising);
    60–64 2.10% / 1.15%; 65–69 2.35% / 1.40%; 70–74 3.95% / 2.70%; 75–79 4.80% / 4.30%;
    80 and over — value not fully captured in extraction (begins "6…").
  - **§6.B.6 Annuitizations: "The annuitization rate for contracts shall be 0% at all
    projection intervals."** (A material modelling simplification for MYGAs.)
  - **§6.B.7:** no index transfers and **no future deposits** are assumed unless
    required by the contract.
  - **§6.B.8 Mortality — prescribed formula, verbatim:**
    ```
    q_x^(2012+n) = q_x^(2012) × (1 − G2_x)^n × F_x
    ```
    "where q_x denotes mortality from the **2012 IAM Basic Mortality Table**, as
    defined in **VM-M Section 2.C**, multiplied by the appropriate factor (F_x) from
    Table 6.7 and G2_x denotes mortality improvement from **Projection Scale G2**, as
    defined in **VM-M Section 1.J.1.c**." The F_x factors "reflect emerging
    experience, including the impact of how historical mortality improvement has
    differed from the G2 scale. The G2 scale for use in projecting mortality
    improvement on a going forward basis has not changed."
  - **Table 6.7 F_x for Individual Annuities in the Accumulation Reserving Category**
    (selected rows; "without GLB" / "with GLB", Female / Male):
    | Attained age | F/no-GLB | M/no-GLB | F/GLB | M/GLB |
    |---|---|---|---|---|
    | ≤52 | 150.0% | 120.0% | 125.0% | 105.0% |
    | 60 | 132.0% | 101.0% | 107.0% | 82.0% |
    | 65 | 112.8% | 101.0% | 92.0% | 84.0% |
    | 70 | 114.0% | 106.8% | 97.8% | 91.0% |
    | 75 | 122.2% | 108.0% | 107.2% | 96.0% |
    | 80 | 120.8% | 108.0% | 110.0% | 101.0% |
    | 85 | 113.2% | 109.2% | 110.0% | 107.2% |
    | 87+ | 110.0% | 110.0% | 110.0% | 110.0% |
    | 100 | 104.6% | 107.0% | 104.6% | 107.0% |
    | 104 | 101.0% | 101.7% | 101.0% | 101.7% |
    Age-nearest-birthday basis; an ALB conversion formula is given:
    `q(x)_ALB = [q(x)_ANB + (1 − q(x)_ANB) × q(x+1)_ANB] / (2 − q(x)_ANB)`.
  - **§6.B.3** prescribes a per-contract expense of **$35 × 1.025^(valuation-year
    offset)** for contracts the company does not administer (e.g. assumed
    rider-only reinsurance).
  - Discounting/CTE machinery: SR based on CTE70 of the greatest present value of
    accumulated deficiency across stochastic scenarios; DR based on a single
    deterministic scenario ("scenario 12 found in Appendix 1 of VM-20").

### R3. NAIC — "Valuation Manual (VM)-22 (A) Subgroup" committee page
- URL fetched: https://content.naic.org/committees/a/valuation-manual-22-sg
- Retrieved: YES (web page)
- Content: the subgroup's charge is to "Address topics designated as post-launch
  activities following the implementation of the VM-22 principle-based reserving
  (PBR) framework", monitor the fixed annuities reserve framework, and "Develop and
  recommend appropriate changes, including those that improve the accuracy and
  clarity of the VM-22 reserve requirements." An exposure draft "VM-22 Retrospective
  Application" is open for a 90-day public comment period through **June 22, 2026**.
  The page does **not** state adoption/effective dates, and does **not** describe the
  pre-2026 VM-22 (statutory maximum valuation interest rates for income annuities).
  [unverified] Prior to the 1/1/2026 edition, VM-22 was titled "Statutory Maximum
  Valuation Interest Rates for Income Annuities"; this was **not** confirmed from a
  retrieved primary document.

### R4. NAIC — Model #245, "Annuity Disclosure Model Regulation" (NAIC Model Laws — Summer 2021)
- URL fetched: https://content.naic.org/sites/default/files/model-law-245.pdf
- Retrieved: YES (40 pages; §§1–6 read)
- **Note on numbering:** the NAIC Annuity Disclosure Model Regulation is **#245**,
  not #250. (#250 is a different model.)
- Content extracted:
  - §1 Purpose: minimum disclosure standards for annuity contracts, the method of
    disclosure, and the use and content of illustrations.
  - §3 Scope: all group and individual annuity contracts and certificates except
    employer-sponsored plan funding vehicles, non-registered VAs sold to accredited
    investors/qualified purchasers, registered products complying with SEC/FINRA
    disclosure rules (but §5 compliance required after January 1, 2014 absent an SEC
    summary prospectus rule; and the **Buyer's Guide must still be delivered** for
    variable annuities), structured settlement annuities, and (bracketed) charitable
    gift annuities and funding agreements.
  - **§4.I definition of MVA, verbatim:** "'Market Value Adjustment' or 'MVA'
    feature is a positive or negative adjustment that may be applied to the account
    value and/or cash value of the annuity upon withdrawal, surrender, contract
    annuitization or death benefit payment based on **either the movement of an
    external index or on the company's current guaranteed interest rate being offered
    on new premiums or new rates for renewal periods**, if that withdrawal, surrender,
    contract annuitization or death benefit payment occurs at a time other than on a
    specified guaranteed benefit date." → the regulation itself recognises both the
    **external-index** design [S8][S12][S13] and the **declared-new-money-rate**
    design [S14].
  - §4.D "Determinable elements", §4.G "Guaranteed elements", §4.J "Non-guaranteed
    elements" — the three-way taxonomy that governs what may be illustrated.
  - §5.A Delivery: face-to-face — disclosure document and Buyer's Guide at or before
    application; otherwise within 5 business days of receipt of the completed
    application (with mail/Internet safe harbours). **If not provided at or before
    application, a free look period of no less than 15 days must be provided**,
    running concurrently with any other free look.
  - §6 Illustrations: must be labelled as an illustration; must be accompanied by the
    disclosure document; costs and fees individually noted; guaranteed death benefits
    and surrender values shown and labelled guaranteed; non-guaranteed elements may
    be no more favourable than current elements with no assumed future improvement,
    and must reflect planned changes including those after an initial guaranteed or
    bonus period. For fixed indexed annuities, three index scenarios are required
    (most recent 10 calendar years; the lowest-growth and highest-growth continuous
    10-year periods out of the last 20).

### R5. NAIC — Model #275, "Suitability in Annuity Transactions Model Regulation" (NAIC Model Laws — Spring 2020; the best-interest revision)
- URL fetched: https://content.naic.org/sites/default/files/model-law-275.pdf
- Retrieved: YES (20 pages; §§1–6 read)
- Content extracted:
  - §1.A Purpose: "to require producers ... to **act in the best interest of the
    consumer** when making a recommendation of an annuity and to require insurers to
    establish and maintain a system to supervise recommendations." §1.B: creates no
    private cause of action and does not subject a producer to fiduciary standards.
    Drafting note confirms this is "a successor regulation that exceeds the
    requirements of the **2010** model regulation" and references Dodd-Frank §989J.
  - §4 Exemptions: direct response solicitations with no recommendation; ERISA plans;
    IRC §401(a)/401(k)/403(b)/408(k)/408(p) employer plans; §414 government/church
    plans and §457 deferred compensation; non-qualified deferred compensation
    arrangements; personal-injury settlements; formal prepaid funeral contracts.
  - §5.C "Consumer profile information" — 14 enumerated items: age; annual income;
    financial situation and needs including debts; financial experience; insurance
    needs; financial objectives; intended use of the annuity; financial time horizon;
    existing assets or financial products; **liquidity needs**; liquid net worth; risk
    tolerance including willingness to accept non-guaranteed elements; financial
    resources used to fund the annuity; tax status.
  - §6.A(1) **Care Obligation**: reasonable diligence, care and skill to know the
    consumer's situation, understand available options, have a reasonable basis to
    believe the recommendation effectively addresses the consumer's situation **over
    the life of the product**, and communicate the basis of the recommendation.
    Explicitly: no fiduciary obligation is created; the lowest-compensation product
    need not be recommended; no ongoing monitoring obligation is imposed.
  - §6.A(1)(j) **Exchange/replacement analysis** — the producer must consider whether
    the consumer will **incur a surrender charge, be subject to the commencement of a
    new surrender period**, lose existing benefits, or face increased fees; whether
    the replacing product substantially benefits the consumer over the life of the
    product; and whether the consumer has had another exchange or replacement **within
    the preceding 60 months**. (Directly relevant to MYGA-to-MYGA rollover behaviour
    at surrender-charge expiry.)
  - §6.A(2) **Disclosure Obligation**: prior to recommendation, disclose on a form
    substantially similar to Appendix A the scope and terms of the relationship, and
    whether the producer is licensed and authorised to sell fixed annuities, fixed
    indexed annuities, [variable annuities, life insurance, mutual funds, stocks and
    bonds, certificates of deposit].

### R6. 26 U.S. Code § 72 — "Annuities; certain proceeds of endowment and life insurance contracts" (Cornell Legal Information Institute)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (full section text)
- Content extracted:
  - **§72(b)(1) Exclusion ratio, verbatim:** "Gross income does not include that part
    of any amount received as an annuity ... which bears the same ratio to such amount
    as **the investment in the contract (as of the annuity starting date)** bears to
    **the expected return under the contract (as of such date)**."
  - §72(b)(2): the excluded portion may not exceed the **unrecovered investment**
    immediately before receipt. §72(b)(4): unrecovered investment = investment in the
    contract at the annuity starting date less the aggregate previously-excluded
    amounts received on or after that date.
  - §72(b)(3): if payments cease by reason of death with unrecovered investment
    remaining, the unrecovered investment is allowed as a deduction in the annuitant's
    last taxable year.
  - **§72(c)(1) Investment in the contract** = aggregate premiums or other
    consideration paid, minus aggregate amounts previously received that were
    excludable from gross income.
  - **§72(e) Amounts not received as annuities** (i.e. pre-annuitization withdrawals
    and surrenders): §72(e)(2)(B) — amounts received **before** the annuity starting
    date are included in gross income **to the extent allocable to income on the
    contract** and excluded to the extent allocable to investment in the contract
    (income-first / LIFO). §72(e)(3)(A): the amount allocable to income is the excess
    of "**the cash value of the contract (determined without regard to any surrender
    charge)** immediately before the amount is received" over the investment in the
    contract at that time. → For a MYGA, the taxable-income measure is the
    **account value gross of surrender charge**, not the surrender value.
    §72(e)(4)(A): loans and pledges are treated as amounts received.
  - **§72(q) 10-percent penalty for premature distributions from annuity contracts**:
    tax increased by 10% of the includible portion. Exceptions in §72(q)(2) include:
    (A) on or after age 59½; (B) on or after the death of the holder (or primary
    annuitant if the holder is not an individual); (C) attributable to becoming
    disabled within §72(m)(7); (D) part of a series of **substantially equal periodic
    payments** for life/life expectancy (SEPP) made at least annually; (E) from a
    plan/contract described in §72(e)(5)(D); (F) allocable to investment before
    August 14, 1982; (G) under a qualified funding asset; (H) to which §72(t) applies;
    (I) under an **immediate annuity contract** (§72(u)(4)); (J) purchased by an
    employer on plan termination.
  - §72(q)(3) **Recapture on modification of a SEPP series**: if the series is
    modified (other than by death or disability) before the later of the close of the
    5-year period beginning with the first payment and age 59½, the tax that would
    have applied is imposed **plus interest for the deferral period**. §72(q)(3)(B):
    a §1035 exchange does not itself constitute a modification if the aggregate
    distributions continue to satisfy the SEPP requirements.

### R7. IRS — Rev. Rul. 2002-6, 2002-1 C.B. (Section 807 — Rules for Certain Reserves) — used here to establish AG 33's identity and effective date
- URL fetched: https://www.irs.gov/pub/irs-drop/rr-02-6.pdf
- Retrieved: YES (3 pages)
- Content extracted:
  - "The National Association of Insurance Commissioners (NAIC) adopted **Actuarial
    Guideline XXXIII, Determining Minimum Commissioners Annuities Reserve Valuation
    Method (CARVM) Reserves for Individual Annuity Contracts (AG 33), effective on
    December 31, 1995, for all contracts issued on or after January 1, 1981.**"
  - IRC §807(d)(1): the tax life insurance reserve for a contract is the greater of
    the net surrender value and the §807(d)(2) reserve, capped at statutory reserves.
    §807(d)(2)/(d)(3)(B)(ii): the tax reserve method for annuity contracts is **the
    CARVM prescribed by the NAIC and in effect on the date of issuance**.
  - AG 33 itself contains the statement that the guideline "does not constitute a
    change of method or basis from any previously used method", but the ruling holds
    that adopting AG 33's factors **is** a change in basis for tax purposes under
    §807(f) (spread over 10 years).
- **The full text of AG 33 was not retrieved.** It is published in the NAIC
  Accounting Practices and Procedures Manual, Appendix C, which is not freely
  accessible. See Gaps.

### R8. Society of Actuaries Research Institute & LIMRA — "2023-2024 Fixed-Rate Deferred Annuity Surrender Study" (public report), February 2026
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2023-24-frda-public-report.pdf
- Retrieved: YES (7 pages — the public highlights report; detailed results are behind
  the Experience Studies Pro subscription)
- Content extracted:
  - Joint SOA Individual Annuity Experience Committee / LIMRA study of **fixed-rate
    deferred annuity** surrender experience for calendar years 2023 and 2024; updates
    the prior 2015–2022 study.
  - **24 contributing companies, ~65% of industry new sales by premium; ~4.8 million
    contracts of surrender exposure by count; $612 billion of surrender exposure by
    contract value; over 567,000 surrenders.**
  - Scope: single- and flexible-premium products, with or without a GLB (only ~2% of
    exposure had a GLB); **excludes fixed indexed annuities, variable annuities, and
    annuities sold in employer-sponsored plans**; U.S. and territories only.
  - Business mix: 59.1% non-qualified by contract count; females 52–57% of contracts
    by count in every market type (the reverse on a contract-value basis for
    Traditional IRA and non-qualified).
  - Key behavioural findings (qualitative; the underlying numbers are in the
    subscriber package):
    - Surrender rates **peaked in the year the surrender charge expired** and
      "remained elevated" in the following years because no surrender charge applied.
    - Surrender rates **decreased as the guaranteed minimum interest rate (GMIR)
      group increased** — most evident after the surrender charge period.
    - Surrender rates **decreased as the current credited rate increased**.
    - Surrender rates increased with the excess of market rate over credited rate,
      and this relationship was "well defined in the years after surrender charge
      expiry"; during the surrender charge period the underlying level was low but
      "there was still a notable increase between the surrender rate when the
      difference between the market rate and credited rate was 3% relative to when
      the difference was 0%."
    - **"In the year the surrender charge expired, high 'shock' surrender rates were
      observed that were not necessarily impacted or driven by market interest rate
      sensitivity."** Between 1% and 3% spreads there was no clear further increase.
    - Surrender rates rose slightly with attained age from the 60–64 group through
      75–79, but the pattern varied with the presence of a surrender charge.
  - Contributors named: American National, Athene Annuity & Life, Brighthouse
    Financial, CNO (Bankers Life & Casualty), Columbus Life (W&S), Fidelity & Guaranty
    Life, Global Atlantic, Guardian, Integrity Life (W&S), MassMutual, National
    Integrity Life (W&S), New York Life, OneAmerica, Pacific Life, Protective,
    Prudential, Riversource/Ameriprise, Sammons, Securian, The Standard, Symetra,
    Thrivent Financial, USAA, Western & Southern Life Assurance.
  - Methodology: age-nearest-birthday, calendar-year exposure with an annual exposure
    assumption and a **Balducci adjustment**; the contract year of a surrender is
    based on the actual surrender date.

### R9. Society of Actuaries — 2012 Individual Annuity Reserving Report & Table; and the 2012 IAM Basic Table on mort.soa.org
- URLs fetched:
  - https://www.soa.org/resources/experience-studies/2011/2012-ind-annuity-reserving-rpt/ (Retrieved: YES, web page)
  - https://mort.soa.org/ViewTable.aspx?TableIdentity=2581 (Retrieved: YES, table page)
- Content extracted:
  - The SOA Payout Annuity Table Team, working with the NAIC's Life Actuarial (A)
    Task Force, created "a new annuity valuation mortality table, including the
    **projection scales and margins** necessary to make the table suitable for
    standard valuation purposes for individual annuities." Available downloads on the
    SOA page: the report (hosted on the Academy's site), a Q&A implementation
    document, and the tables via mort.soa.org.
  - **mort.soa.org Table Identity 2581 = "2012 IAM Basic Table – Male, ANB"**:
    "2012 Individual Annuity Mortality Basic Table – Male. Basis: Age Nearest
    Birthday", ages 0–120; developed from **2000–2004 payout annuity experience data
    covering 16 companies**; P-spline smoothing; ages below 50 graded from a projected
    1994 GAM table; ages 96+ extrapolated by the Kannisto method; **projected to 2012
    using Projection Scale G2**; maximum q capped at **0.400** at the oldest ages.
    Sample q_x: age 0 = 0.001783; age 30 = 0.000824; age 50 = 0.002285;
    age 75 = 0.020905; age 100 = 0.298452; age 105+ = 0.400 (flat). Certified
    January 2013. (Female table is Table Identity 2582.)
  - The statutory hooks for these tables are VM-M §2.C (2012 IAM Basic) and
    VM-M §1.J.1.c (Projection Scale G2), per VM-22 §6.B.8 [R2].

### R10. SOA — "2015-2022 Fixed Rate Deferred Surrender Experience Study"
- URL attempted: https://www.soa.org/49c0c1/globalassets/assets/files/resources/experience-studies/2024/15-22-frds.pdf
- Retrieved: **NO** — HTTP 404 on two attempts. Search-engine summaries reported
  shock surrender rates in contract years 4, 6, 8 and 11 (matching 3-, 5-, 7- and
  10-year surrender charge periods), with a peak in contract year 6 of 33.4% by
  contract count and 40.3% by contract value for calendar years 2018–2022 versus
  10.2% / 10.6% for 2015–2017 — **not verified**, do not rely on these numbers.

---

## Extracted specifications

Every line below is tagged with the document it came from. Where designs differ
across carriers, all variants are shown.

### 1. Product chassis

| Item | Value | Source |
|---|---|---|
| Legal form | Single-premium or **modified** single-premium deferred annuity (SPDA/MSPDA); "modified guaranteed annuity" when MVA'd and SEC-registered | [S1][S3][S4][S16] |
| Premium pattern | Single premium, no additional premium (Oak ADVantage, NYL, MassMutual Ascend brochure, Voya) | [S5][S13][S10][S3] |
| Premium pattern (variant) | Modified single premium: up to **5 additional deposits in the first 6 months**, minimum $500 each | [S1][S2] |
| Premium pattern (variant) | Flexible purchase payment with per-payment guaranteed period options | [S4] |
| Account value | 100% of premium at issue; no front-end load; interest credited daily or annually at the declared effective annual rate | [S5][S9][S16][S4] |
| Interest crediting frequency | Credited **daily**, quoted as an annual effective rate | [S4][S5][S16] |
| Fee load | No annual maintenance/administration fee (Oak ADVantage, NYL, MassMutual Ascend, Oceanview). Voya reserves the right to charge one but currently does not. Nationwide charges none. | [S5][S13][S10][S16][S3][S4] |

### 2. Issue ages and premium limits

| Carrier / product | Issue ages | Min premium | Max premium | Source |
|---|---|---|---|---|
| Athene MaxRate (CA) | 0–80 (actual age), Q and NQ | $5,000 | $1,000,000 (more w/ approval) | [S1] |
| Athene MaxRate (NY) | 0–80 | $10,000 | $1,000,000 (more w/ approval) | [S2] |
| Voya MRA | not stated in the retrieved text | $10,000 ($1,000 per guaranteed term) | >$1,000,000 with consent | [S3] |
| Nationwide BOA Platinum Edge | not stated | varies by contract type; e.g. TSA $10,000, SEP/Simple IRA $2,000; $1,000 per GPO | not stated | [S4] |
| Midland Oak ADVantage | up to 90 | $50,000 (Q and NQ) | not stated | [S5][S6][S7] |
| MassMutual Ascend SecureGain 5 | Q 0–89, NQ 0–89, inherited 0–75 | $10,000 | not stated | [S10] |
| NYL Secure Term MVA II | NQ 0–85, TQ 18–85, inherited 0–85 | $5,000 | >$2,000,000 needs approval | [S13] |
| Oceanview Harbourview | not stated | $10,000 | not stated | [S16] |

### 3. Guarantee periods offered

- 3 / 5 / 7 years: Midland Oak ADVantage [S5][S6][S7]; Global Atlantic SecureFore II
  (as withdrawal charge periods) [S15].
- 3 / 4 / 5 / 6 / 7 years, each with a matching surrender charge schedule: NYL Secure
  Term MVA Fixed Annuity II [S13].
- 5 / 7 years: Athene MaxRate NY [S2]. (Athene MaxRate CA shows a 7-year initial
  withdrawal charge schedule with auto-renewal into a period of the same duration
  [S1].)
- 5 years only: MassMutual Ascend SecureGain 5 [S10][S11].
- Up to and including 10 years, at the company's discretion: Voya MRA [S3].
- 3, 4, 5, 6, 7, 8, 9, 10 years: Nationwide BOA Platinum Edge [S4].

### 4. Declared rate and renewal-rate mechanics

- Initial rate guaranteed for the whole initial guarantee period; a new rate is
  declared for each subsequent guarantee period [S1][S2][S5][S16].
- Rate varies by **premium band**: NYL uses five bands ($5,000–24,999 / 25,000–49,999
  / 50,000–99,999 / 100,000–1,499,999 / 1,500,000+) [S13]; MassMutual Ascend uses two
  ($100,000+ vs under $100,000) [S11].
- **Renewal floor mechanisms observed (three distinct designs):**
  1. **Explicit renewal-rate floor stated in the marketing document**: Athene — "the
     rate will never be less than 1%" [S1][S2].
  2. **Contract GMIR, fixed at issue**: MassMutual Ascend SecureGain 5 minimum
     interest rate **0.25%** on the current ICC24 form [S11] (the older 4/23 brochure
     said the GMIR "will be 1% or higher" [S10] — a documented tightening over time);
     Oceanview "never less than the contract's minimum guaranteed rate at the time of
     your purchase" [S16]; Midland Capital Income minimum guaranteed fixed rate 0.25%
     [S9]; Symetra specimen minimum guaranteed interest rate [1.50%] [S14].
  3. **No minimum at all** — Nationwide's registered MGA states plainly: "there is no
     minimum Specified Interest Rate for any of the Guaranteed Period Options" [S4].
- **Renewal structure differs materially:**
  - Roll into a **new multi-year guarantee period** of the same (or elected) duration,
    with a **new, usually shorter, surrender charge schedule**: Athene [S1][S2];
    Midland Oak ADVantage [S5][S6]; MassMutual Ascend (EWC and MVA apply "during each
    initial term **or any renewal terms**") [S11].
  - Roll into **annually redetermined rates with no new surrender charge**: NYL
    Secure Term MVA II — "the policy will receive a new renewal rate each anniversary
    that is based on the accumulation value", not less than the GMIR; in NY the GMIR
    itself is redetermined each anniversary and will not be lower than 1.00% [S13].
  - Roll into the **Transition Account** (short-term liquid account, monthly declared
    rate, no MVA/CDSC) if no election is made: Nationwide [S4].
  - Automatic reinvestment into an equal-duration term, else next shortest, else next
    longest: Voya [S3].
- Renewal surrender charge schedules are typically **lower than the initial schedule**:
  Athene CA initial 9/8/7/6/5/4/3 vs renewal 5/5/5/5/5/4/3 [S1]; Athene NY initial
  7/6/5/4/3 (5-yr) or 7/6/5/4/3/2/1 (7-yr) vs renewal 5/4/3/2/1 [S2].
- Attained-age caps on renewal charges: Athene maximum subsequent-period withdrawal
  charge 4% at 94, 3% at 95, 2% at 96, 1% at 97, 0% at 98–100 [S1][S2].
- Rate-lock rules at new business: Midland — application within 10 calendar days of
  signing and premium within 60 calendar days [S7]; NYL — application and premium
  within 30 days of signing (60 days for NYLIAC-initiated transfers) [S13].
- **No "bailout rate" provision was found in any retrieved document.** The bailout
  feature (a stated renewal rate below which the owner may surrender without charge)
  is a real MYGA/FIA feature [unverified] but is not evidenced by any source here.
  The functional analogue in the retrieved products is the **30-day free-out window**
  at each guarantee-period end [S1][S2][S5][S6].

### 5. Declared rates actually observed

| Product | Rate | As of | Source |
|---|---|---|---|
| Midland Oak ADVantage, 3/5/7-year (mapping [unverified]) | 5.45% / 5.60% / 5.50% | eff. July 23, 2026 | [S7] |
| MassMutual Ascend SecureGain 5, premium $100,000+ | 4.45% | eff. 09/22/25 | [S11] |
| MassMutual Ascend SecureGain 5, premium <$100,000 | 4.10% | eff. 09/22/25 | [S11] |
| MassMutual Ascend SecureGain 5, GMSV accumulation rate | 2.80% | 09/22/25 | [S11] |
| MassMutual Ascend SecureGain 5, contract minimum interest rate | 0.25% | 09/22/25 | [S11] |

MassMutual Ascend SecureGain 5 rate **shape** within the initial term (distinctive):
base rate + 0.25% bonus in term year 1, then base + 0.10% per year cumulatively for
term years 2–5. Illustrated example on a 3.00% base: 3.25%, 3.10%, 3.20%, 3.30%,
3.40% [S10].

### 6. Surrender / withdrawal charge schedules

| Product | Schedule (contract year 1 →) | Source |
|---|---|---|
| Athene MaxRate CA, initial period | 9, 8, 7, 6, 5, 4, 3 | [S1] |
| Athene MaxRate CA, renewal period | 5, 5, 5, 5, 5, 4, 3 | [S1] |
| Athene MaxRate NY, 5-year | 7, 6, 5, 4, 3 | [S2] |
| Athene MaxRate NY, 7-year | 7, 6, 5, 4, 3, 2, 1 | [S2] |
| Athene MaxRate NY, renewal (5-yr) | 5, 4, 3, 2, 1 | [S2] |
| Voya MRA (by years since payment credited, 0→7) | 7, 7, 6, 6, 5, 4, 2, 0 | [S3] |
| Nationwide BOA Platinum Edge, 10-yr GPO (completed years 0→10) | 5, 5, 4, 4, 3, 3, 2, 2, 1, 1, 0 | [S4] |
| Nationwide BOA Platinum Edge, 5-yr GPO (completed years 0→5) | 5, 5, 4, 4, 3, 0 | [S4] |
| Midland Oak ADVantage (3/5/7-yr period) | **level 3.0% every year** | [S5][S6] |
| Midland Capital Income (FIA, 7-yr) | 6, 6, 5, 4, 3, 3, 2, 0 | [S9] |
| MassMutual Ascend SecureGain 5 | 9, 8, 7, 6, 5, 0 | [S10] |
| NYL Secure Term MVA II, non-NY, 7-yr | 7, 7, 7, 6, 5, 4, 3 (truncated to the elected period) | [S13] |
| NYL Secure Term MVA II, New York, 7-yr | 7, 6, 5, 4, 3, 2, 1 | [S13] |

Notes:
- Voya and Nationwide measure the charge from the **original purchase payment date**,
  not from the start of the current guarantee period, so reinvestment does not
  restart the clock (Voya) or does restart it only for transferred amounts
  (Nationwide) [S3][S4].
- Nationwide's CDSC is contractually capped: "will not exceed 5% of the amount
  withdrawn" [S4].
- Surrender charge ordering: Nationwide takes surrenders first from the Transition
  Account, then pro rata across GPOs [S4]; Voya assumes withdrawals come from the
  purchase payment first (not earnings) for charge purposes, an assumption explicitly
  **not** made for tax purposes [S3].

### 7. Free / penalty-free withdrawal provisions

Four distinct designs are evidenced:

1. **10% of account value, annually, from year 2** — Athene Enhanced Liquidity (10%
   of AV as of the last contract anniversary, no benefit in year 1) [S2]; Oceanview
   (10% of Contract Value as of the prior anniversary, after the first contract year,
   taken in any number of partial withdrawals) [S16]; Midland Capital Income (10% of
   beginning-of-year AV in any contract year) [S9].
2. **10% including the first year** — MassMutual Ascend SecureGain 5: 10% of purchase
   payments in year 1, then 10% of AV at the most recent anniversary [S10]; Global
   Atlantic SecureFore II: 10% of beginning-of-year Contract Value, 10% of the initial
   deposit in year 1 [S15]; Nationwide: greater of 10% of Contract Value or the RMD,
   each Contract Year, non-cumulative [S4].
3. **Interest-only** — Midland Oak ADVantage: after the first contract anniversary,
   an amount equal to the **interest earned in the prior contract year**; systematic
   monthly/quarterly/semi-annual/annual interest withdrawals of at least $50 each;
   first-year interest available only by current company practice [S5][S6].
4. **Greatest-of formula** — NYL Secure Term MVA II: the greatest of (a) 10% of AV at
   the last anniversary, (b) 10% of current AV, (c) 100% of the gain in the policy
   (premium ≥ $100,000 only, not in NY) [S13].

Additional mechanics:
- Voya's "special withdrawal": one withdrawal per calendar year of up to 10% of
  account value after 12 months, **first withdrawal only**, non-cumulative within the
  year, and **the MVA still applies** [S3].
- Nationwide's free amount is non-cumulative and **the MVA still applies to free
  amounts withdrawn before maturity** [S4].
- Minimum withdrawal amounts: Athene $500 partial / $100 systematic [S2]; NYL $100
  with an AV floor of $2,000 after a partial withdrawal [S13]; Midland systematic
  interest payments at least $50 [S5].
- Advisory-fee withdrawals (RIA-distributed products): Midland Oak ADVantage permits
  up to **1.50%** of contract value annually (1.0% on the older sheet), treated as
  partial surrenders subject to surrender charge and MVA above the free amount
  [S5][S6]; Midland Capital Income permits up to 1.5% **not** subject to surrender
  charges or MVA [S9].

### 8. Market value adjustment — formulas, exactly as written

Five distinct MVA designs were retrieved. All are stated verbatim in the S-entries
above; collected here for modelling.

**(a) Geometric, Treasury-based, uncapped, two-sided — Voya MRA [S3]:**
```
MVA = [ (1 + i) / (1 + j) ] ^ (x / 365)
```
`i` = deposit-period yield (average YTM of the Treasury Notes maturing in the last
three months of the guaranteed term, taken on the last business day of each week of
the deposit period); `j` = current yield (same notes, last business day of the week
preceding the withdrawal); `x` = days remaining, measured from the Wednesday of the
week of withdrawal. Multiplicative factor on the amount withdrawn. No cap.

**(b) Geometric, swap-based, with a 25 bp expense adder, uncapped, two-sided —
Nationwide BOA Platinum Edge [S4]:**
```
MVA Factor = [ (1 + a) / (1 + b + 0.0025) ] ^ t
```
`a` = interest rate swap for a term equal to the Guaranteed Period, at deposit
(published rate 2 days before allocation); `b` = interest rate swap at distribution
for a term equal to the **remaining** period, with **partial years rounded up to a
full year** (capped at the Guaranteed Period), published 2 days before; `t` = days
until the Maturity Date ÷ **365.25**. The `0.0025` covers liquidation
administrative/processing expenses. Factor = 1 during the Investment Period. Falls
back to U.S. Treasury Bond yields if swaps are unpublished. No cap or collar.

**(c) Linear, corporate-credit-index-based, capped both ways — Midland National /
Sammons [S8][S9]:**
```
MVA = (i0 − it) × T
```
applied to the portion of the surrender exceeding the free amount, **before** the
surrender charge. `i0` = MVA external index value at issue; `it` = index value at
surrender; `T` = (days from surrender to the end of the current contract year ÷ 365)
+ whole years remaining in the MVA period. **MVA external index = Barclay's US Credit
Index.** The MVA, positive or negative, is **limited to the surrender charge amount
and/or to the interest credited to the accumulation value**, and the resulting
surrender value cannot fall below the state minimum. Formula varies by state.

**(d) Linear, declared-new-money-rate-based, with a contractual duration factor table
— Symetra specimen [S14]:**
```
MVA = W × (Ic − In) × Fs
```
`W` = amount withdrawn/transferred/annuitized; `Ic` = rate credited on that money;
`In` = rate that would be credited on **new money** for a Guaranteed Period of the
same duration; `Fs` = contractual adjustment factor by whole years remaining `s` and
by whether `Ic` is below or at/above 6% (table in S14); partial years interpolated.
This is a hard-coded modified-duration MVA driven by the insurer's own renewal rate
rather than a public index — the second branch of the NAIC Model 245 §4.I definition
[R4].

**(e) "Months remaining × change in reference-index YTM", floored at the GMIR
accumulation — New York Life [S13]:**
The formula "takes into account the number of months left in the surrender charge
period and the change in the yield to maturity value of a reference index from the
date that the policy was issued to the date of surrender or withdrawal." New York
policies use a different formula "that measures the change in U.S. Treasury Constant
Maturity yield(s) and applicable corporate bond index(es)". **Floor: the MVA cannot
reduce the surrender value below premiums paid (less prior withdrawals and applicable
charges and taxes) accumulated at the policy's GMIR.** The exact algebra is not in the
fact sheet (it points to a separate "Examples and Explanation" flyer).

**Cap / collar designs observed (this is the main cross-carrier variation):**
| Design | Effect | Source |
|---|---|---|
| Symmetric cap at the withdrawal charge | \|MVA\| ≤ withdrawal charge, both directions | Athene NY [S2] |
| Cap at min(surrender charge, interest credited), both directions | \|MVA\| ≤ min(SC, interest credited) | Midland [S8][S9] |
| Asymmetric: positive capped at the EWC, negative floored by SNFL minimum | upside limited, downside limited only by nonforfeiture | MassMutual Ascend [S12] |
| Floored at premium accumulated at the GMIR | MVA alone cannot breach that floor (surrender charge still can) | NYL [S13] |
| No cap stated | pure market factor | Voya [S3], Nationwide [S4] |

**MVA reference rates observed:**
| Reference | Source |
|---|---|
| U.S. Treasury Notes maturing in the last quarter of the term (YTM) | Voya [S3] |
| Interest rate swaps + 25 bp | Nationwide [S4] |
| Barclay's US Credit Index | Midland [S8][S9] |
| 5-Year Treasury CMT and/or BofA Merrill Lynch 5-10 Year US Corporate Bond Index | MassMutual Ascend [S12] |
| Company's own new-money declared rate | Symetra [S14] |
| Reference index YTM; in NY, U.S. Treasury CMT + corporate bond indexes | NYL [S13] |

**When the MVA does and does not apply (composite):**
- Applies: full surrender and withdrawals above the free amount during the
  surrender-charge / MVA period [S2][S8][S9][S10][S13][S15][S16]; and on annuitization
  before maturity [S3][S4].
- Applies even to free-amount withdrawals: Voya [S3] and Nationwide [S4] — a real
  design difference from the retail MYGAs, where the free amount is MVA-free.
- Does **not** apply: to the death benefit [S2][S4][S8][S13][S16]; after the MVA
  period ends [S8][S16][S13]; during the 30-day free-out window at a guarantee-period
  end [S2]; to RMDs (Athene Enhanced Liquidity [S2]; Midland by current company
  practice [S5]; NYL for NYLIAC-calculated RMDs [S13]); under waiver riders (Midland
  nursing home [S5][S6]; Athene confinement/terminal illness/SEPP [S2]; NYL Living
  Needs Benefit/Unemployment [S13]); on annuitization (Oceanview [S16], "may not
  apply" Midland [S8]); to systematic distribution options (Voya SWO/ECO [S3]).
- Voya applies **only a positive MVA** to amounts used to start a **lifetime** payout
  option (a one-way protection for the owner) [S3].
- Nationwide's 10-day free-look refund is Contract Value **including any applicable
  MVA**, not premium [S4]; Voya's free-look refund equals the purchase payment [S3].

### 9. Death benefit

| Design | Source |
|---|---|
| Full accumulation value at date of death; no surrender charge, no MVA | Athene CA and NY [S1][S2]; NYL [S13] |
| **Greater of** accumulation value and the minimum surrender value | Midland Oak ADVantage [S5][S6] |
| Surrender charges and MVA waived on the owner's death | Oceanview [S16] |
| Account value if paid within 6 months of the annuitant's death; account value **adjusted by MVA** if later, or if the owner ≠ annuitant (and possibly a CDSC if owner ≠ annuitant) | Voya [S3] |
| Contract Value with no CDSC and no MVA before the Annuitization Date | Nationwide [S4] |
| Paid directly to beneficiaries, avoiding probate | MassMutual Ascend [S10]; Midland [S5] |
| Optional enhanced death benefit: 40% of policy earnings (issue age ≤70), max 100% of adjusted premium, charge 0.30%/yr taken as 0.075% of AV quarterly, ends after the 25th anniversary, never >1%/yr | NYL Enhanced Beneficiary Benefit Rider [S13] |

Statutory floor: Model 805 §6 — "The death benefit under such contracts shall be at
least equal to the cash surrender benefit" [R1].

### 10. Minimum guaranteed surrender value / nonforfeiture floor

- **Statutory rule** [R1]: minimum nonforfeiture amount = accumulation of **87.5% of
  gross considerations** at the §4.B indexed rate, less prior withdrawals accumulated
  at the same rate, less an **annual $50 contract charge** accumulated at the same
  rate, less premium taxes paid, less indebtedness. Indexed rate =
  **min(3%, round(5-yr CMT, nearest 1/20 of 1%) − 1.25%)**, floored at **0.15%**;
  determinable from a date or average specified in the contract no more than 15 months
  before issue or redetermination; may be reset if the contract says so. An extra
  reduction of up to 100 bp is allowed while an equity-index benefit is substantively
  provided (§4.C).
- **Product implementations retrieved:**
  - MassMutual Ascend SecureGain 5: "GMSV equals **87.5% of purchase payments minus
    all prior withdrawals (not including early withdrawal charges or negative market
    value adjustments) plus interest credited daily at the GMSV rate of 2.80%**",
    explicitly tied to "the NAIC Standard Nonforfeiture Law for Individual Deferred
    Annuities, model #805" [S11]. Note the deduction base **excludes** the surrender
    charges and negative MVAs previously assessed — i.e. the floor is computed on the
    gross withdrawal, not the net proceeds.
  - Midland National: "The minimum surrender value will never be less than **87.5% of
    all premiums less any surrenders (after MVA or reduction for surrender charges)
    accumulated at a rate not less than the rate required or otherwise directed by
    your Annuity Contract**" [S9]. Note this wording measures surrenders **after** the
    MVA/surrender-charge reduction — the opposite convention from [S11]. Both are in
    the market; the model should make the convention a switch.
  - NYL: the MVA floor is premiums paid (less prior withdrawals and applicable charges
    and taxes) accumulated at the **GMIR** — a contract-level floor distinct from the
    statutory 87.5% floor [S13].
  - MassMutual Ascend's MVA explainer: "A negative adjustment will never reduce your
    surrender value to less than the minimum permitted under the standard
    non-forfeiture law of your state" [S12].
  - Midland: "Surrender value after surrender charge and MVA is guaranteed to not be
    less than the minimum required by the laws of the state in which the contract is
    delivered" [S8].
- **Cash surrender value rule** [R1 §6]: CSV ≥ PV of the portion of the maturity value
  of the paid-up annuity benefit arising from prior considerations, discounted at a
  rate **not more than 1% higher** than the contract's accumulation rate, reduced for
  prior withdrawals and indebtedness, increased by additional credited amounts — and
  never below the minimum nonforfeiture amount.
- **Deemed maturity date** [R1 §8]: the later of the contract anniversary next
  following the annuitant's 70th birthday and the 10th contract anniversary.

### 11. Waivers of surrender charge / MVA

| Waiver | Trigger detail | Source |
|---|---|---|
| Nursing home / confinement | LTC facility or hospital, confinement began in force, **90 consecutive days**, after year 1 | Athene [S2] |
| Nursing home / confinement | Qualified nursing care center, after year 1, up to 100% of contract value, not confined at issue, rider included at no charge | Midland [S5][S6] |
| Nursing home | Annuitant ≥ **45 consecutive days** in a licensed nursing facility, >1 account year elapsed, request within 3 years of admission (no limit in OR; non-licensed facility permitted in NH); not available if already confined at purchase | Voya [S3] |
| LTC / hospital | Continuous **180-day** confinement commencing in force; either joint owner; request during confinement or within 90 days after | Nationwide (CDSC only) [S4] |
| Extended care | Nursing home / LTC facility ≥ **90 consecutive days**, after year 1, up to 100% of account value | MassMutual Ascend [S10] |
| Health care facility | Enrolled and living in a health care facility **60 consecutive days** | NYL Living Needs Benefit [S13] |
| Nursing home | FL: **60 consecutive days**, unavailable until the first anniversary in FL | Global Atlantic [S15] |
| Terminal illness | Physician certifies life expectancy ≤ **12 months**; owner expected to live >12 months at contract date; after year 1 | Athene [S2] |
| Terminal illness | Prognosis of survival **12 months or less** (or longer per state law), after year 1, up to 100% of AV | MassMutual Ascend [S10] |
| Terminal illness | Diagnosed life expectancy **12 months or less** | NYL [S13]; Global Atlantic [S15] |
| Disability | Total and permanent disability preventing any work for pay for ≥ **12 consecutive months**; **not available for withdrawals on/after the 66th birthday** | NYL [S13] |
| Unemployment | Qualifying for and receiving **state unemployment benefits for 60 consecutive days** | NYL [S13] |
| Chronic and critical illness | Covered individual **age 65 or younger at issue** | Global Atlantic [S15] |
| SEPP | Annual withdrawals, must continue ≥5 years or to age 59½ | Athene [S2] |
| RMD | Waived on partial withdrawals of RMDs | Athene Enhanced Liquidity [S2]; Midland (current company practice) [S5][S6]; NYL (NYLIAC-calculated) [S13]; Global Atlantic (even above the free amount) [S15] |
| Small-balance / involuntary | Full surrender when account value ≤ $2,500 with no withdrawal in the prior 12 months; involuntary termination < $2,500 | Voya [S3] |

Common structure: waivers are typically available only **after the first contract
year**, and the waiver rider is **included at no charge** [S2][S5][S10][S13][S15].
Where multiple waivers apply, Athene uses the **single highest** free-withdrawal
amount, not the sum [S2].

### 12. Annuitization / income options

| Product | Basis of payout | Options | Source |
|---|---|---|---|
| Athene MaxRate CA | **Cash surrender value**, except during the 30-day window (full AV); after year 1 | fixed period; life income; life income with 10- or 20-year certain | [S1] |
| Athene MaxRate NY | **Full accumulation value**; after year 1 | same | [S2] |
| Midland Oak ADVantage | **Surrender value** (accumulation value in FL); by current company practice, accumulation value if (a) life option after year 1 or (b) in force ≥5 years and payments over ≥5 years | income for specified period; income for specified amount; life with period certain; life; joint and survivor. Non-life options 5–20 years (all states but FL) | [S5] |
| Midland Capital Income (FIA) | surrender value if elected during the surrender charge period; FL accumulation value after year 1 | life; life with period certain; joint and survivor; specified period; specified amount | [S9] |
| MassMutual Ascend SecureGain 5 | not stated | fixed period; life or life with a minimum fixed period; joint and one-half survivor (survivor 50% for life) | [S10] |
| Voya MRA | Contract Value; MVA applies if before term end (only a **positive** MVA for lifetime options); no early withdrawal charge on annuitization | payments for a specified period or for life; monthly/quarterly/semi-annual/annual; options with a death benefit. Min first payment $50 or $250/yr. Start any time after year 1; default start = later of annuitant's 85th birthday or the 10th anniversary; age + guaranteed years ≤ 95 | [S3] |
| Nationwide BOA Platinum Edge | Contract Value less premium taxes, applied to the fixed payment annuity table; MVA applies if before maturity; no CDSC if in force ≥2 years | (1) Life Annuity; (2) Joint and Survivor Annuity; (3) Life Annuity with 120 or 240 Monthly Payments Guaranteed. Default = life with 240 months guaranteed. Default commencement age 70½ (qualified) / 90 (NQ). Annuitization Date ≥2 years after issue. Payments <$50 → change frequency; <$5,000 → lump sum | [S4] |
| Oceanview Harbourview | not stated; MVA does not apply on annuitization | life only; life with 10 years certain; fixed period; customized | [S16] |

- **No annuitization bonus was found in any retrieved document.** Some carriers grant
  accumulation-value (rather than surrender-value) payouts under conditions — Midland's
  "current company practice" concession [S5] and Athene's 30-day-window full-AV
  treatment [S1][S2] are the closest analogues.
- VM-22 prescribes an **annuitization rate of 0% at all projection intervals** for the
  standard projection [R2] — statutorily, the annuitization option is assumed never
  exercised.

### 13. RMD friendliness

- Best treatment: RMD withdrawals are **exempt from surrender charge and MVA even
  above the free amount** — Global Atlantic SecureFore II [S15]; Midland (by current
  company practice) [S5][S6]; NYL (RMDs as calculated by NYLIAC under the RMD
  Automated option) [S13]; Athene Enhanced Liquidity [S2]; Nationwide (free amount =
  greater of 10% of Contract Value or the RMD, though the MVA still applies) [S4].
- Worst treatment: Athene MaxRate base product — "RMDs will be treated as any other
  withdrawal and subject to Withdrawal Charges" unless taken in the 30-day free-out
  window [S1][S2].
- Structural note: Oak ADVantage's **interest-only** free withdrawal [S5] makes the
  separate RMD concession essential, because an RMD can easily exceed a year's
  interest at older ages.
- IRS applicable age for RMDs is 73 for owners who attain age 72 after 2022 (72 for
  those who attained 70½ after 2019; 70½ if born before July 1, 1949); the excise tax
  for a missed RMD is 25%, reduced to 10% if corrected within the correction window
  [S4].

### 14. Taxation (for cash-flow modelling of policyholder behaviour)

- Pre-annuitization withdrawals are **income-first (LIFO)**: the taxable portion is
  the excess of the **cash value determined without regard to any surrender charge**
  over the investment in the contract [R6 §72(e)(3)(A)]. → Model the taxable base off
  the **account value**, not the surrender value.
- Annuity payments use the **exclusion ratio** = investment in the contract at the
  annuity starting date ÷ expected return at that date [R6 §72(b)(1)], capped at the
  unrecovered investment [R6 §72(b)(2)], with a terminal deduction if payments cease
  on death with unrecovered investment [R6 §72(b)(3)].
- 10% penalty under §72(q) on the includible portion of premature distributions, with
  exceptions for age 59½, death, disability, SEPP, immediate annuities, and others
  [R6]. SEPP modification within 5 years / before 59½ triggers recapture **plus
  interest**; a §1035 exchange is not a modification if the combined distributions
  continue to satisfy SEPP [R6 §72(q)(3)].
- Loans and pledges are treated as amounts received [R6 §72(e)(4)(A)].
- Premium taxes: 0%–4% depending on jurisdiction [S3]; 0%–3.5% [S16]; may be deducted
  from the accumulation value or death benefit if required by the state of residence
  [S5][S9].

### 15. Statutory valuation (for reserve modelling)

- **VM-22 PBR applies for valuation dates on or after January 1, 2026**, with a
  three-year elective transition and mandatory prospective application to all
  applicable blocks starting three years after the effective date [R2 §2.B]. For
  in-scope contracts, VM-22 **constitutes CARVM** [R2 §1.A].
- Aggregate reserve = SR + DR (contracts passing the Single Scenario Test) + reserves
  for contracts excluded from modelling and valued under VM-A/VM-C/VM-M/VM-V
  [R2 §3.A]. The additional standard projection amount is **disclosure-only** under
  VM-31 [R2 §3.C].
- MYGAs sit in the **Accumulation Reserving Category** [R2].
- Prescribed standard-projection assumptions of most relevance to a MYGA model
  (all [R2]): the dynamic full-surrender formula and its components; base lapse
  Table 6.5 for fixed annuities with no GLB (including the **75% shock in the year of
  an IGP expiry** and the 1%/2% base rates inside a multi-year IGP); annuitization
  rate 0%; no future deposits; mortality
  `q_x^(2012+n) = q_x^(2012) × (1 − G2_x)^n × F_x` off the 2012 IAM Basic table with
  Projection Scale G2 and Table 6.7 F_x factors.
- Note the interaction that matters most for MVA'd MYGAs: **MVA Factor = 0 when the
  MVA is in effect**, which zeroes the entire `Rate Factor × MVA Factor` dynamic term,
  leaving only `Base Lapse × GMIR Factor` (times ITM Factor = 1) [R2 §6.B.5]. The
  regulator's prescribed view is that an in-force MVA fully neutralises
  interest-rate-driven disintermediation.
- Pre-2026 statutory reserving for these contracts was formulaic CARVM as clarified by
  **AG 33** ("Determining Minimum Commissioners Annuities Reserve Valuation Method
  (CARVM) Reserves for Individual Annuity Contracts", NAIC-adopted, **effective
  December 31, 1995 for all contracts issued on or after January 1, 1981**) [R7]. For
  tax purposes, IRC §807(d)(2)/(d)(3)(B)(ii) makes CARVM as prescribed by the NAIC and
  in effect at issue the tax reserve method for annuity contracts, with the tax reserve
  equal to the greater of the net surrender value and the §807(d)(2) reserve, capped at
  statutory [R7].

### 16. Lapse / surrender behaviour evidence

- **Regulatory prescribed rates** [R2 Table 6.5]: for a fixed annuity with no GLB and
  an IGP > 1 year, base lapse is **1.0%** in years running up to expiry, **75.0%** in
  the year of an IGP expiry, and **2.0%** in years after surrender charge expiry when
  not in an IGP-expiry year. The worked examples make the pattern explicit — e.g. a
  3-year IGP / 3-year SC product renewing into another 3-year IGP / 3-year SC gives
  contract-year base lapses of **1%, 1%, 1%, 75%, 1%, 1%, 75%** [R2].
- **Industry experience** [R8]: surrender rates peak in the year the surrender charge
  expires and remain elevated afterwards; decrease as the GMIR increases; decrease as
  the credited rate increases; increase with the excess of market rate over credited
  rate, with the relationship well defined **after** surrender-charge expiry but muted
  during the surrender charge period; and the shock-year rate is high **regardless of
  the interest-rate environment**.
- The regulatory dynamic-lapse shape mirrors this: `X = 2.0` during the surrender
  charge period and `2.5` at and after shock, with a 50 bp no-response buffer and a
  `Max(0, 1 − 5 × (1 − CSV/AV))` term that switches the dynamic component off once the
  surrender-charge + MVA haircut reaches 20% of account value [R2].
- **Distribution-side friction on the shock lapse.** Model #275 §6.A(1)(j) requires
  the producer, on any exchange or replacement, to consider whether the consumer will
  incur a surrender charge or start a new surrender period, whether the replacing
  product substantially benefits the consumer over the life of the product, and whether
  the consumer has had another exchange or replacement **within the preceding 60
  months** [R5]. That 60-month look-back is a real behavioural constraint on MYGA-to-
  MYGA churn at surrender-charge expiry and is worth reflecting qualitatively when
  calibrating shock-lapse assumptions. Model #275 §5.C also makes **liquidity needs**
  and **risk tolerance including willingness to accept non-guaranteed elements**
  mandatory profile items, which bears on who buys a 7-year MVA'd contract [R5].

### 17. Disclosure and illustration constraints on the modelled contract

- The disclosure document and Buyer's Guide must be delivered at or before application
  in a face-to-face sale, or within five business days otherwise; failing that, a free
  look of **not less than 15 days** must be provided [R4 §5.A].
- Illustrated non-guaranteed elements may be **no more favourable than current**
  elements, may assume **no future improvement**, and must reflect planned changes
  including changes after an initial guaranteed or bonus period [R4 §6.F(8)]. This
  directly constrains how a MYGA's post-initial-term renewal rate may be shown, and is
  the reason MassMutual Ascend's escalating-rate design [S10] must be disclosed as a
  guaranteed element rather than an illustrated projection.
- Guaranteed death benefits and surrender values must be shown and clearly labelled
  guaranteed [R4 §6.F(7)]; costs and fees must be individually noted [R4 §6.E].

---

## Variations across insurers

1. **MVA formula family.** Three algebraic families appear. (i) **Geometric
   discount-factor** forms, `[(1+a)/(1+b)]^t`, used by the SEC-registered modified
   guaranteed annuities — Voya on Treasury note yields with no spread [S3], Nationwide
   on interest rate swaps with a 25 bp expense adder [S4]. (ii) **Linear
   duration × rate-change** forms, `(i0 − it) × T`, used by the retail MYGAs — Midland
   on the Barclay's US Credit Index [S8][S9]. (iii) **Linear
   declared-rate-differential × contractual duration factor**, `W × (Ic − In) × Fs`,
   using the insurer's own new-money rate [S14]. NAIC Model 245 §4.I explicitly
   recognises both the external-index and the company-declared-rate branches [R4].
   For a reference model, family (i) is the cleanest and the best documented
   (Nationwide's is fully specified including day-count, rounding and worked examples);
   family (ii) is the most common in current retail MYGAs.

2. **MVA caps.** The biggest single divergence. Athene NY caps the MVA symmetrically
   at the withdrawal charge [S2]. Midland caps it at min(surrender charge, interest
   credited) both ways [S8][S9]. MassMutual Ascend caps only the **positive** side at
   the early withdrawal charge and floors the negative side at the SNFL minimum [S12].
   New York Life floors the MVA at premium accumulated at the GMIR [S13]. The two
   registered products impose **no cap at all** [S3][S4] — which is exactly why they
   are registered securities. A model must treat the cap as a first-class parameter,
   not an afterthought.

3. **Free-withdrawal design.** 10% of account value is the market convention
   [S2][S4][S9][S10][S15][S16], but Midland's Oak ADVantage uses an **interest-only**
   allowance [S5][S6] and New York Life uses a **greatest-of** formula that can reach
   100% of the gain for large premiums [S13]. Whether the MVA applies **inside** the
   free amount also differs: it does for Voya [S3] and Nationwide [S4], and does not
   for the retail MYGAs [S2][S9][S10][S15][S16].

4. **Renewal architecture.** Two clean camps. Camp A rolls into a **new multi-year
   guarantee period with a fresh (lower) surrender charge schedule** — Athene
   [S1][S2], Midland [S5][S6], MassMutual Ascend [S11]. Camp B drops to **annually
   declared rates with no new surrender charge** — New York Life [S13]. Camp A creates
   a repeating shock-lapse pattern at each renewal boundary; Camp B creates a single
   shock at the end of the initial term followed by ordinary interest-sensitive lapse.
   VM-22's Table 6.5 worked examples are explicitly built around this distinction [R2].

5. **Surrender charge shape.** Classic declining schedules from 7%–9% (Athene CA
   9/8/7/6/5/4/3 [S1]; MassMutual Ascend 9/8/7/6/5 [S10]; NYL NY 7/6/5/4/3/2/1 [S13])
   dominate the commission-paid retail market. NYL's non-NY schedule holds 7% flat for
   three years before declining [S13]. Nationwide's registered contract caps the charge
   at 5% and steps it down in pairs [S4]. Midland's RIA-distributed Oak ADVantage uses
   a **level 3%** in every year [S5][S6] — a distinctly fee-based-channel design that
   pairs a low, flat charge with an interest-only free withdrawal.

6. **Guarantee-period-end handling.** Athene's **30-day free-out window** (no
   withdrawal charge, no MVA, full accumulation value, income option available)
   [S1][S2] and Midland's equivalent 30-day window [S5][S6] are the retail norm.
   Nationwide gives 90 days' advance notice and defaults unelected money into a liquid
   Transition Account [S4]; Voya gives 18 days' notice with a 5-day election deadline
   and defaults to auto-reinvestment [S3].

7. **Guaranteed minimum interest rate.** Ranges from an explicit 1% renewal floor
   [S1][S2], to a contract GMIR of 0.25% [S11][S9] or 1.50% [S14], to **none at all**
   on the registered Nationwide contract [S4]. This matters directly because VM-22's
   GMIR Factor steps the base lapse by 1.25 / 1.00 / 0.70 across the ≤1.0% /
   1.0–2.5% / >2.5% GMIR bands [R2].

8. **Most representative design for a reference model.** A single-premium,
   non-flexible MYGA with: a 5-year guarantee period; a declining surrender charge of
   9/8/7/6/5; a 10%-of-account-value annual free withdrawal; a two-sided MVA of the
   linear `(i0 − it) × T` form referenced to a corporate credit index and capped at the
   surrender charge; death benefit = full account value with no charge and no MVA;
   a GMSV of 87.5% of premium less withdrawals accumulated at a contract GMSV rate
   inside the 0.15%–3% Model 805 corridor; nursing-home and terminal-illness waivers
   after year 1; RMD exemption from charges and MVA; and roll-over into a new
   guarantee period at a redeclared rate with a shorter surrender charge schedule.
   That composite is closest to **MassMutual Ascend SecureGain 5** [S10][S11][S12] on
   charges and nonforfeiture, and to **Midland Oak ADVantage / Capital Income**
   [S5][S8][S9] on MVA algebra. For anyone wanting a fully-specified MVA with worked
   arithmetic to unit-test against, use **Nationwide BOA Platinum Edge** [S4].

---

## Gaps and caveats

1. **AG 33 full text was not retrieved.** Actuarial Guideline XXXIII is published in
   the NAIC Accounting Practices and Procedures Manual, Appendix C, which is not
   freely available. Its official title, adoption and effective date are sourced from
   IRS Rev. Rul. 2002-6 [R7]. Its substantive requirements (separate valuation interest
   rates for elective vs non-elective benefits, integrated benefit streams, the
   greatest-present-value construction) are **not** verified here.
2. **Model 805 nonforfeiture floor.** The retrieved Fall 2020 edition sets the floor at
   **15 basis points**, not 1% [R1]. The commonly cited "1%–3% corridor" reflects the
   2003 amendment as originally adopted; the change to 0.15% is not documented by any
   retrieved source beyond the Fall 2020 text itself. Treat "1% floor" as [unverified].
3. **NAIC model numbering.** The Annuity Disclosure Model Regulation is **#245**
   [R4], not #250.
4. **Pre-2026 VM-22.** That VM-22 previously carried statutory maximum valuation
   interest rates for income annuities is [unverified] — the NAIC subgroup page [R3]
   does not say so, and the 2026 edition of the manual contains only the PBR text
   [R2]. Similarly, the current maximum valuation interest rates for non-PBR annuity
   business (VM-A / VM-C / Appendix A-820) were **not** extracted.
5. **VM-22 Table 6.2 (partial withdrawals), attained age 80+.** The value was
   truncated in text extraction; only ages ≤59 through 75–79 are recorded [R2].
6. **Bailout rate provisions.** No retrieved document contains one. Bailout provisions
   are a genuine MYGA/FIA feature [unverified], but nothing here evidences one, and the
   30-day free-out window is the mechanism actually documented [S1][S2][S5][S6].
7. **Annuitization bonus.** None found in any retrieved document.
8. **Annuity payout factors.** No retrieved document contains an actual annuity rate
   table or payout factors. Nationwide refers to "the fixed payment annuity table" in
   the contract without reproducing it [S4]. Payout factor construction will have to
   come from the 2012 IAR / 2012 IAM Basic + Scale G2 machinery [R9][R2] plus a chosen
   valuation interest rate, not from a product document.
9. **Exact MVA algebra for New York Life** is not in the retrieved fact sheet — it
   points to a separate "Examples and Explanation" flyer that was not retrieved [S13].
10. **Midland Oak ADVantage rate-to-period mapping** on the July 2026 rate sheet is
    ambiguous in text extraction; the 5.45% / 5.60% / 5.50% values are certain, the
    assignment to 3 / 5 / 7 years is [unverified] [S7].
11. **Failed fetches**: American Equity GuaranteeShield brochure (DNS failure) [S18];
    New York Life Secure Term MVA IV fact sheet via Fidelity (HTML interstitial) [S17];
    three immediateannuities.com brochures (HTTP 403) [S19]; SOA 2015-2022 Fixed Rate
    Deferred Surrender study (HTTP 404) [R10]. Nothing is asserted from any of these.
    Consequently **Midland National Guarantee Ultimate, Symetra Custom 7, American
    Equity GuaranteeShield, Pacific Life and Global Atlantic SecureFore withdrawal
    charge schedules remain undocumented** here.
12. **No contract specimen for a pure MYGA was retrieved.** The closest are the
    Nationwide S-1 prospectus [S4] and the Symetra specimen contract data page [S14].
    Actual contract forms (e.g. Midland ICC21-AS204A, MassMutual Ascend
    ICC24-P1172524NW, NYLIAC ICC24D-P04) are named in the retrieved documents but the
    forms themselves are not publicly posted.
13. **Index-crediting parameters** (caps, participation rates, spreads, buffers,
    floors) are out of scope for a book-value MYGA. The only such values recorded here
    come from Midland Capital Income, a fixed **index** annuity [S9], and are included
    solely because that document also carries the MVA and nonforfeiture wording.
14. **Interim value formulas** in the RILA/index-linked sense do not exist on these
    products; the MVA plus surrender charge **is** the interim value adjustment.
15. Several sources are marketing or producer documents rather than contracts, and say
    so ("See annuity contract for full details" [S1][S2]; "This brochure is for
    solicitation purposes only" [S5]). Where a document flags a feature as offered "by
    current company practice", that feature is explicitly **not** a contractual
    guarantee and can be withdrawn at any time [S5][S6].
