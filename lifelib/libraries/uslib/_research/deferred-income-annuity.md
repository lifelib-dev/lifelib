# Deferred Income Annuity (DIA), including Qualified Longevity Annuity Contracts (QLAC) — research notes (U.S.)

Access date for all citations: 2026-08-04.

Purpose: source library and extracted specifications to drive a reference liability
cash-flow projection model (lifelib/modelx style) for U.S. individual deferred
income annuities (DIAs), including the QLAC variant.

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). Facts stated from general knowledge and not verified against a
retrieved document are tagged [unverified]. The S#/R# numbering here is
**product-local** and independent of the cross-product library numbering used in
`_research/regulatory-actuarial.md`.

Scope note: a DIA is a **paid-up deferred annuity**. Each premium immediately and
irrevocably purchases a fixed dollar income benefit commencing on a stated future
date. There is **no account value, no cash surrender value and no interest
crediting rate** during the deferral period [S1][S2][S4][R13]. Consequently many
of the product parameters that dominate fixed/indexed deferred annuity models
(credited rates, caps, participation rates, spreads, buffers, surrender-charge
schedules, MVA formulas, benefit-base rollups, interim values) **do not exist**
for this product. Where the brief asked for them, that is recorded explicitly in
"Gaps and caveats" rather than invented.

---

## Primary sources

### S1. New York Life Insurance and Annuity Corporation (NYLIAC) — "New York Life Guaranteed Future Income Annuity II — Product Overview"
- Publisher: NYLIAC (a Delaware corporation), subsidiary of New York Life
  Insurance Company, 51 Madison Avenue, New York, NY 10010. Document distributed
  by Fidelity Insurance Agency, Inc. (authorized distributor); item numbers
  `969689.8.0`, `NYL-DIA-0626`, `49695-20`; © 2026 FMR LLC.
- Doc type: consumer product overview / fact sheet (4 pages). Current vintage
  (June 2026 revision code).
- URL fetched: https://communications.fidelity.com/fili/dia/nyl/docs/new_york_life_dfia_factsheet.pdf
- Retrieved: YES (full 4-page PDF text extracted)
- Policy form: `ICC11–P101` in most jurisdictions; `211-P101` in some states;
  state variations apply.
- Facts extracted:
  - Investment amount: initial minimum **$10,000**; additional investment minimum
    **$100**; maximum cumulative **$2 million or more requires home office
    approval**.
  - Issue ages: Qualified **18–73**; QLAC **35–80**; Nonqualified **0–80**;
    Roth IRA **20–80**. For Joint Life on qualified, joint annuitant may be
    **18–80** but must be a spouse. For nonqualified joint life, both annuitants
    must be **80 or younger** and must be spouses. Roth requires the Roth IRA to
    have been in place at least five calendar years before the year income starts.
  - Issue-age constraint: "Issue age can be no later than **2 years before** the
    client's RMD age as defined by the IRS. Clients born after 1960 may purchase
    the annuity as late as age 73."
  - Deferral period minimum: **24 full months from date of contract issue**
    (applies to all annuity income options).
  - Deferral period maximum: **40 years** for lifetime income; **20 years** for
    period-certain-only.
  - Latest income start: **age 85** for nonqualified and Roth IRA; for qualified,
    by **April 1 of the year following** the year the owner turns **73** (owners
    born before 1960) or **75** (owners born in 1960 or later). For QLACs, income
    must begin **after** April 1 of the year after the owner turns 73/75 and
    **before the first day of the month after turning age 85**.
  - Annuity income options: Life Annuity with **Cash Refund**; Life Annuity with
    **Guarantee Period 10–30 years**; **Life Only** without guarantee period;
    **Period Certain Only, 5 to 30 years**.
  - Joint life continuance: available for Life with Cash Refund, Life with
    Guaranteed Period, and Life Only. With Cash Refund the **only** continuance
    option is **100%**. With Guaranteed Period or Life Only the choices are
    **100%, 66⅔%, or 50%**. Continuance percentage must be chosen at purchase.
    Not available for Joint Life Annuity with Cash Refund contracts. For Joint
    Life with Period Certain, if the first annuitant dies during the guaranteed
    period, payments to the second annuitant are **not reduced until the end of
    that period**.
  - **Income Start Date Adjustment Option** (one-time change, before the Income
    Start Date): may **accelerate up to five years** (but no sooner than
    **13 months after the latest investment**); may **defer up to five years**
    from the original Income Start Date (subject to the maximum deferral limits).
    Income payments are **recalculated**. The annuity income option and the day
    of month of payment cannot be changed. **Not available on Life Only policies.**
  - Recalculation basis on Income Start Date change: "adjusted based on the
    **Moody's Seasoned Baa Corporate Bond Yield (DBAA)** rates, **A2000 mortality
    tables**, and an **interest rate change adjustment**." (Footnote 8.)
  - **Return of Investment (deferral-phase death benefit)**: during the deferral
    period, **all annuity options except Single Life Only and Joint Life Only**
    include a **return of the premium payments** if the owner dies (or the
    annuitant if the owner is an entity such as a trust). If the surviving spouse
    is joint annuitant and sole primary beneficiary, the policy continues on the
    owner's death. Death on/after the Income Start Date is governed by the elected
    income option.
  - Explicit no-liquidity language: "This contract is **irrevocable, it has no
    cash surrender value, and no withdrawals are permitted prior to the Income
    Start Date**. … Contracts in which a Life Only payout option is selected do
    not provide a death benefit either prior to or after the chosen Income Start
    Date." (Footnote 1.)
  - **Payment Acceleration** (post-income-start liquidity): receive the next
    scheduled monthly payment plus five subsequent payments — **six months of
    income in one sum**; no payments for the next five months. Owner must be at
    least **age 59½**; may be exercised **two times** over the life of the policy;
    **nonqualified policies only**.
  - **Annual Increase Option** (COLA): income increases annually by **1%, 2%, or
    3%**. Must be elected at purchase; owner must be at least **59½ at the time of
    the first income payment**; initial payments are smaller. **Not available for
    QLAC** (footnote 5).
  - Payment frequency: monthly, quarterly, semiannually, annually; selected on the
    application and **cannot be changed**.
  - Tax note: exercising Payment Acceleration before 59½ can retroactively trigger
    the 10% penalty tax plus interest on annuity payments received before 59½.

### S2. Massachusetts Mutual Life Insurance Company — "MassMutual RetireEase Choice — A Flexible Premium Deferred Income Annuity" (client guide)
- Publisher: Massachusetts Mutual Life Insurance Company, Springfield, MA.
  Document code `AN4325 219  CRN202011-221296`; © 2019 MassMutual. PDF hosted on a
  third-party content CDN (`static.contentres.com`), but the document itself is
  MassMutual's own 32-page client guide.
- Doc type: detailed client/product guide (32 pages) — the most contractually
  granular DIA document retrieved.
- URL fetched: https://s3.amazonaws.com/static.contentres.com/media/documents/cda42ab0-617b-4977-94dc-221106c82e4f.pdf
- Retrieved: YES (all 32 pages text extracted)
- Contract forms: `FPDIA12` and `ICC12-FPDIA12` (in certain states, including
  North Carolina).
- **VINTAGE CAVEAT**: this guide is from 2019 and predates SECURE 1.0/2.0. Its
  QLAC figures ($130,000 limit, 25%-of-balance limit, RMD age 70½) are
  **superseded** — see [R1][R2][R3]. Its *product mechanics* remain the most
  detailed DIA description retrieved and are cited as such.
- Facts extracted:
  - Market types: Nonqualified; Qualified — Traditional IRA, Roth IRA, SEP IRA,
    Custodial IRA, QLAC IRA, Custodial QLAC IRA.
  - Issue ages ("age nearest birthday"): minimum annuitant **22** (non-QLAC),
    **41** (QLAC IRA / Custodial QLAC IRA); minimum joint annuitant **22**.
    Maximum annuitant: **88** (nonqualified and Roth IRA), **69** (Traditional,
    Custodial and SEP IRAs, due to RMD rules), **83** (QLAC). Maximum joint
    annuitant **88** in all market types.
  - Purchase payments: minimum initial **$10,000** (qualified and nonqualified);
    minimum subsequent **$500 per payment**; maximum cumulative **$1.5 million
    without further approval** (aggregated across all MassMutual-group DIAs with
    the same owner or annuitant). Minimum monthly annuity payment **$100**
    (may drop below $100 at a joint-and-survivor reduction or on remaining
    installment refund payments).
  - "Each time you make a purchase payment, you will know the exact amount of
    future income you are buying." Multiple payments are combined into a **single
    income stream**. MassMutual sends a confirmation of each subsequent payment
    and the additional income purchased; the owner may request a **refund within
    10 calendar days of receiving the confirmation**.
  - **No purchase payments accepted within 13 months of the annuity date.**
  - No cash value, no liquidity: "There is also **no accumulation or cash value**
    with RetireEase Choice and, therefore, **no liquidity**. The only time that
    distributions are made … are when annuity payments begin or when a death
    benefit is paid." Product highlights: **Withdrawal Provisions: None**.
  - **Annuity date (earliest)**: any day between the 1st and 28th of the month;
    **no earlier than 13 months after the contract issue date**; for a QLAC, no
    earlier than April 2 of the calendar year following the year the owner attains
    age 70½ **[superseded — see R1/R2]**.
  - **Annuity date (latest)**: the earlier of **30 years after contract issue**;
    or when **any annuitant attains age 90**; or (qualified other than Roth and
    QLAC) April 1 of the year after the owner attains 70½ **[superseded]**; or
    (QLAC) the **first day of the month following the owner's 85th birthday**.
  - **Annuity Date Adjustment Rider**: accelerate or defer within a **10-year
    window — up to five years before or after** the annuity date chosen at issue;
    **once only** during the life of the contract; new date is irrevocable.
    Requirements: new annuity date at least **13 full months after the last
    purchase payment**; same contract restrictions as the original; cannot be
    changed after payments begin; cannot be changed if a death benefit has been
    triggered (except for convertible joint options); the annuity **option** cannot
    be changed; the **day of month** cannot change (the month can); **payment
    frequency cannot change**; resulting annuity payment must be **at least $100**;
    no change permitted that breaks RMD requirements.
  - **Annuity date change recalculation basis**: "Your originally scheduled annuity
    payment; the new annuity date; **Moody's Seasoned Baa Corporate Bond Yield
    rate** at the time we receive the annuity date change request; the **Annuity
    2012 Mortality Table**; an **interest rate change adjustment set forth in the
    contract**."
  - Florida override: Florida requires deferred annuity contracts to permit
    annuitization at any time after 13 months from issue; for Florida contracts
    the annuity date can be accelerated for **all** annuity options (including the
    No-Refund options) to as early as 13 months after issue, not limited to five
    years prior.
  - Annuity options (non-QLAC). **Single Life**: Life — No Death Benefit; Life —
    No Refund; Life — Cash Refund; Life — Installment Refund; Life — Period
    Certain (**10 to 30 years**). **Joint and Survivor Life (non-convertible)**:
    No Refund; Cash Refund; Installment Refund; Period Certain (10–30 yrs);
    Reduction at Death of Either Annuitant — No Refund (**½, ⅔, ¾**); Reduction at
    Death of Either Annuitant — Period Certain (**½, ⅔, ¾**). **Joint and Survivor
    Life (convertible)**: No Refund / Cash Refund / Installment Refund / Period
    Certain (**period certain limited to 10 years** for the convertible variant),
    each convertible to the corresponding single life option.
  - **Deferral-phase death benefit**: "the death benefit prior to the annuity date
    is a **return of purchase payments** for most options (except for the Single
    Life — No Death Benefit annuity option)." The **Single Life — No Death Benefit**
    option provides **no death benefit either before or after** the annuity date;
    it **requires a deferral period of 10 years or longer**, the annuity date
    **cannot be changed**, and it is **not available in Connecticut, Florida or
    New York** (the guide states CT/FL in the product-highlights footnote and
    CT/NY in the body — an internal inconsistency in the document).
  - Post-annuity-date guarantees:
    - **Cash Refund Guarantee**: on death of the last surviving annuitant, if total
      annuity payments made < purchase payments made, the beneficiary receives the
      **difference in a lump sum**; otherwise the contract terminates.
    - **Installment Refund Guarantee**: payments **continue in the same amount and
      frequency until they equal the purchase payments**; beneficiary may instead
      elect the **present value of remaining payments in a lump sum**.
    - **Period Certain Guarantee**: payments continue to the beneficiary in the
      same amount and frequency **until the end of the period certain**;
      beneficiary may elect the **present value of remaining payments** instead.
    - Installment Refund and Period Certain guarantees are **not available with a
      QLAC**.
  - **QLAC-permitted options only**: Single Life — No Refund; Single Life — Cash
    Refund; Single Life — No Death Benefit; Joint and Survivor Life — Cash Refund.
  - Convertible vs. non-convertible joint pricing (directly relevant to modelling):
    "**Non-convertible** joint life annuity options guarantee income based on a
    **single payout assumption that both annuitants will be alive on the annuity
    date**. **Convertible** joint life annuity options guarantee income based on
    **two different payout assumptions**: as a joint life payout (if both alive on
    the annuity date) and as the corresponding single life annuity payout for each
    annuitant (if only one is alive and the contract converts). … In general, if
    both annuitants are alive on the annuity date, the joint life payout will be
    **lower** with a convertible joint life annuity option."
  - **Annuity payment acceleration**: nonqualified contracts with monthly payout
    frequency only; lump sum equal to **three or six** regularly scheduled
    payments; regular payments resume after the three- or six-month period;
    **maximum five times** over the life of the contract; at least one regular
    payment must be received before requesting again. Explicitly labelled "**not a
    liquidity feature**."
  - **MassMutual Inflation Protector**: automatically increases each payment by
    **1%, 2%, 3% or 4%** on each annuity-date anniversary. Must be elected at issue;
    **cannot be canceled or changed**. Not available with convertible joint options;
    may be limited or unavailable on qualified contracts due to RMD rules.
  - Payees: up to **10 payees** per contract; allocations must total 100%.
  - Annuitant cannot be changed once the contract is issued; there may be **up to
    two annuitants**.
  - Deferral-phase death mechanics (non-QLAC): if an **owner** dies (surviving
    owner or not), the beneficiary receives a death benefit equal to the **purchase
    payments applied to the contract**. If a non-owner **annuitant** dies and a
    surviving annuitant exists: **non-convertible** → contract continues with the
    option chosen at issue; **convertible** → the option converts to the
    corresponding single life option.
  - QLAC deferral-phase death benefits: Single Life — No Death Benefit → contract
    terminates; Single Life — No Refund and Single Life — Cash Refund → **purchase
    payments are returned to the beneficiary**; Joint and Survivor — Cash Refund →
    if married on date of death, return of purchase payments **or** continue as a
    beneficiary IRA. **Spousal continuances are not allowed on QLAC IRAs**; a
    spouse beneficiary electing to keep the QLAC in force holds it as a **spousal
    beneficiary IRA**, payments start on the originally elected annuity date, and
    **no new purchase payments are allowed**.
  - Divorce interaction on QLAC Joint and Survivor — Cash Refund: if the annuitants
    are divorced at the time of the owner's death and the divorce occurred before
    the annuity date, **only a return of purchase payments less annuity payments
    previously distributed** is paid; continued payments to a non-spouse
    beneficiary are not offered.
  - Product positioning: guide states the target client is "between the ages of
    **50 and 65** and ready to retire in **five to 10 years**", generally with
    "**$250,000 and $1.5 million** in investable assets".
  - Medicaid: "MassMutual RetireEase Choice is **not a Medicaid-friendly deferred
    annuity**. The use of … in conjunction with Medicaid planning is prohibited."

### S3. The Guardian Insurance & Annuity Company, Inc. (GIAC) — "Guardian SecureFuture Income Annuity® — A flexible premium deferred income annuity"
- Publisher: The Guardian Insurance & Annuity Company, Inc. (GIAC), a Delaware
  corporation, 7 Hanover Square, New York, NY 10004; wholly owned subsidiary of
  The Guardian Life Insurance Company of America. Document codes
  `641695.4.0 GSFIA-DIA-0118`, `1/15/2018`, `1.956733.103` (Fidelity-distributed
  version). PDF retrieved from a third-party mirror (`qlacs.net`) after the
  Fidelity-hosted copy failed.
- Doc type: consumer fact sheet / brochure (4 pages).
- URL fetched: https://www.qlacs.net/assets/guardian_dia_factsheet.pdf
- Retrieved: YES (all 4 pages text extracted)
- **VINTAGE CAVEAT**: January 2018 document; references "the required minimum
  distribution (RMD) age of **70½**" throughout — superseded by SECURE 1.0/2.0.
  Product mechanics still cited; age references flagged.
- Facts extracted:
  - Minimum initial premium **$10,000** (qualified and nonqualified); minimum
    subsequent premium **$100 each** (subsequent premiums **not available for
    QLAC**). Initial premium or sum of all premiums exceeding **$1 million**
    requires GIAC approval.
  - "Each payment purchases a specific amount of guaranteed lifetime income, based
    on **annuity purchase rates that are in effect at the time each purchase
    payment is made**. Multiple premium payments … will be combined into a single
    guaranteed income stream that begins on the Income Start Date you selected at
    issue."
  - Deferral period minimum: **24 full months** from contract issue.
  - Deferral period maximum: the earlier of **40 years from the issue date** or
    **until any annuitant reaches age 85**. **For Life Only options with issue age
    71–75, the maximum deferral period is 5 years.** For traditional IRA contracts,
    not past the calendar year the owner/annuitant attains 70½ [superseded], or
    **age 85 for a QLAC**.
  - Issue ages: Traditional IRA **18–68**; QLAC **31–82**; Nonqualified and Roth
    IRA **0–80** (maximum age for Single Life Only without guarantee period is
    **75**; for Joint Life Only without guarantee period, both annuitants must be
    **75 or younger**).
  - Annuity income options: Single Life — Life Only without Guarantee Period; Life
    with Guarantee Period (**5–30 years**, not available for QLAC); Life with Cash
    Refund. Joint and Survivor Life Only without Guarantee Period; Joint and
    Survivor Life with Guarantee Period (5–30 years); Joint and Survivor Life with
    Cash Refund.
  - **Return of premium payments (deferral phase)**: "During the deferral period,
    **all annuity options, except Single and Joint Life Only, include a return of
    the premium payment(s)** if the owner (or the annuitant, if the owner is an
    entity, such as a trust) dies."
  - **Income Start Date adjustment**: accelerate by **five years** (no sooner than
    **13 months after the latest premium payment**); defer up to **five years**
    from the original date (within maximum deferral limits). Payments are
    recalculated; the annuity option cannot be changed; **not available if Single
    or Joint Life Only is chosen**. Footnote: "If you defer the Income Start Date,
    there is a **one-time option to accelerate** the Income Start Date to a date no
    earlier than the original Income Start Date."
  - **Withdrawal Feature** (post-income-start): owners of Life with Guarantee
    Period or Life with Cash Refund contracts with **monthly** payout frequency and
    **at least six months remaining** in the guarantee or cash refund period may
    accelerate **up to five** regularly scheduled payments paid in a lump sum along
    with the regularly scheduled payment. Nonqualified and Roth IRA only; owner's
    **actual age 59½ or later**; regular payments resume after the six-month period;
    **exercisable once** over the life of the contract.
  - **Cost-of-Living Adjustment**: optional; automatically increases annuity
    payments by a specified percentage on each contract anniversary after the
    Income Start Date; elected at issue; cannot be changed or canceled; **not
    available for QLAC**; may be limited/unavailable on qualified contracts due to
    RMD rules. (Percentage range **1%–5%** per the cross-insurer comparison [S6];
    the fact sheet itself does not state the range.)
  - Payment frequency: monthly, quarterly, semiannually, annually — **frequency can
    be changed** (differs from NYL and MassMutual, which fix it at issue).
  - Post-income-start death mechanics: within a guarantee period, under a single
    life contract the remaining payments continue to the owner until the end of the
    guarantee period **or the owner can elect a lower, present-day-value lump sum**;
    under Cash Refund the owner may continue remaining payments or take a **lump
    sum equal to their combined total**. Under a joint life contract the survivor
    percentage is **not applied until the guarantee period ends**. After the
    guarantee period, a single life contract simply ends at the annuitant's death.

### S4. Pacific Life Insurance Company / Pacific Life & Annuity Company — "PACIFIC SECURE INCOME® — A Fixed, Deferred Income Annuity" (fact sheet)
- Publisher: Pacific Life Insurance Company (all states except New York) and
  Pacific Life & Annuity Company (all states). Document codes `24-299C`,
  `FAC0560-01`, `2/26 E1127`. Official Pacific Life domain.
- Doc type: producer/consumer fact sheet (6 pages). **Current vintage (Feb 2026)** —
  the most up-to-date primary source retrieved.
- URL fetched: https://www.annuities.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/fact-sheets/pacific-secure-income-fact-sheet.pdf
- Retrieved: YES (all 6 pages text extracted)
- Facts extracted:
  - **Minimum premium $15,000** (highest minimum among sources retrieved);
    **maximum $2 million** without Pacific Life home-office approval; **minimum
    subsequent purchase payment $500**.
  - **"The maximum Qualified Longevity Annuity Contract (QLAC) aggregate purchase
    payment limit in 2026 is $210,000 (indexed in future years for inflation)."**
    (Independently corroborates [R3].)
  - Flexible premium; multiple purchase payments permitted **only with the lifetime
    annuity income options**. Subsequent purchase payments **not permitted within
    13 months of the Annuity Payment Start Date**; 1035 exchange/transfer requests
    not accepted within **16 months** of that date. For the Period Certain option,
    multiple purchase payments or 1035 exchanges are permitted **with the
    application only**, funds must be received within **60 days of contract issue
    (90 days in New York)**, and no subsequent payments are permitted.
  - Payee receives **one** income payment per period regardless of the number of
    purchase payments.
  - Issue ages: **minimum 22**; maximum **85** (nonqualified and Roth IRA),
    **71** (traditional IRA), **82** (QLAC).
  - Ownership: an owner must also be an annuitant unless the owner is a non-natural
    person; joint owners and joint annuitants must be spouses; joint annuitants not
    permitted with the Period Certain option or with non-natural owners; joint
    owners not permitted with the Period Certain option or any Single Life option.
  - **Annuity Payment Start Date**: set at contract issue; **no sooner than 13
    months after contract issue**, **no later than 30 years after contract issue**.
    Maximum start-date age: **90** (nonqualified and Roth IRA); **73** for
    traditional IRA (payments required to begin by April 1 of the calendar year
    following the year the client turns 73); **QLAC — by no later than the first day
    of the following month after attaining age 85**.
  - **Annuity Payment Start Date Adjustment Feature**: one-time opportunity to
    advance or defer **up to five years in either direction**. Adjusted date must be
    at least **13 months from the most recent purchase payment** and **no later than
    30 years from issue**; must respect the maximum start-date ages (73 traditional
    IRA / 85 QLAC / 90 nonqualified and Roth). Advancing **reduces** the income
    payment; deferring **increases** it. Available with all options **except Life
    Only, Joint Life Only, Joint and Survivor Life Only, or Period Certain**.
    **Not available in Connecticut or New York.**
  - Annuity income options. **Period Certain** up to 30 years (no subsequent
    purchase payments if selected; not available with QLAC). **Single Life**: Life
    Only; Life Only with **100% Return of Purchase Payments Death Benefit**; Life
    with Period Certain (up to 30 years); Life with Cash Refund; Life with
    Installment Refund (not on qualified contracts, not with QLAC). **Joint Life**
    and **Joint and Survivor Life** variants of each, with survivor reduction to
    **50%, 67% or 75%** — reduction on the death of *either* annuitant (Joint Life)
    versus on the death of the *primary* annuitant (Joint and Survivor Life). All
    joint options require the joint annuitant to be a spouse. Income option is set
    at issue and **cannot be changed**.
  - Note on the "Life Only with 100% Return of Purchase Payments Death Benefit"
    option: this is a distinctive design — a **pure life annuity after income start
    but with a deferral-phase return-of-premium death benefit**, sitting between
    Life Only (no DB at all) and Cash Refund (DB both phases).
  - **Inflation Protection Option**: annual increase of **2%, 3% or 4%**; available
    with all annuity income options; begins after the Annuity Payment Start Date;
    must be selected at purchase and cannot be changed. **Not available with QLAC
    or with traditional IRA contracts.**
  - **Income Payment Acceleration**: after age 59½ and with monthly payments, take a
    lump sum equal to **three or six times** the normal monthly payment; normal
    payments resume in the fourth or seventh month; available with all income
    options; **maximum two times**; at least one normal payment must be received
    before reuse. **Not available with a QLAC.** For qualified contracts, the
    acceleration period must be in the same tax year.
  - **Withdrawal of Guaranteed Income Payments** (the most liquid feature found in
    any DIA source): for **nonqualified** contracts, a lump-sum withdrawal of **up
    to 100% of the present value of the remaining guaranteed income payments**.
    Available with all options **except** the Life Only / Joint Life Only / Joint
    and Survivor Life Only options (with or without the return-of-purchase-payments
    death benefit). **An interest-rate adjustment charge will apply.** Owner must be
    **59½ or older**. Making a withdrawal lowers or may stop remaining guaranteed
    payments; **except for the Period Certain option, if the annuitant is still
    living at the end of the period when guaranteed payments would have stopped,
    Pacific Life will resume income payments until death**. Not available in
    Missouri. Six-month waiting periods interlock the acceleration, withdrawal and
    start-date-adjustment features in both directions.
  - **Death benefit before annuity income payments begin**: a **return of purchase
    payments** death benefit applies. Non-natural owner → payable at the annuitant's
    death. Single Life options or Period Certain → contract terminates at the death
    of the first owner or annuitant and ROP is paid (**except for the Life Only
    option**). Joint Life / Joint and Survivor Life → contract terminates at the
    death of the first owner or the last annuitant and ROP is paid (**except Joint
    Life Only and Joint and Survivor Life Only**); a surviving spouse who is an
    annuitant and joint owner may continue the contract instead. Death benefit is
    paid as a **lump sum**. **Terminal illness acceleration**: if an owner or
    annuitant is diagnosed with a terminal illness with life expectancy of **12
    months or fewer** on or after the issue date, a death benefit will be paid
    (except for the Life Only variants).
  - Death on or after the Annuity Payment Start Date: governed by the elected income
    option; **no death benefits with any Life Only option**.
  - QLAC restrictions summarised on p.6: "there are restrictions on annuity payout
    options that can be elected under a QLAC contract, and the **commutation,
    payment acceleration, and inflation protection features are not available**.
    Changes to marital status may require a change to the annuity payout option
    and/or payments in order to maintain the QLAC status."
  - State availability: **Pacific Secure Income is not available in California,
    Illinois, North Carolina, Oregon, Pennsylvania, or Texas.**

### S5. Pacific Life — "Pacific Secure Income — Client Guide"
- Publisher: Pacific Life. Document codes `24-300A`, `FAC0555-2401`, `11/24 E1127`.
- Doc type: client guide (16 pages).
- URL fetched: https://www.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/guide/pacific-secure-income-client-guide.pdf
- Retrieved: YES (16 pages text extracted)
- Facts extracted (beyond S4):
  - Start-date adjustment restated: "cannot be advanced any sooner than **13 months
    after contract issue or the date of the last purchase payment**, and may not be
    deferred any later than **30 years after contract issue**." Graphic labels the
    two directions "Income Payments **Decrease**" (advance) / "Income Payments
    **Increase**" (defer).
  - Withdrawal feature: "**There is no limit to the number of withdrawals you can
    make**", subject to the eligibility conditions (nonqualified; 59½; Period
    Certain, Life with Period Certain, Life with Cash Refund, or Life with
    Installment Refund option, or their Joint Life versions).
  - Worked acceleration example: normal monthly payment $1,000; a three-month
    acceleration request after an April payment yields **$3,000** alongside the
    April $1,000 (total $4,000), no payments in May/June/July, normal payments
    resume in August.
  - The guide does **not** disclose the interest-rate-adjustment charge formula
    used for withdrawals (see "Gaps and caveats").

### S6. Fidelity Investments — "Compare Deferred Income Annuities" (cross-insurer comparison table)
- Publisher: Fidelity Brokerage Services / Fidelity Insurance Agency (distributor
  comparison of third-party insurer products).
- Doc type: web comparison table (secondary/aggregator, but sourced from the
  insurers' filed product parameters and useful as a cross-check).
- URL fetched: https://www.fidelity.com/annuities/deferred-fixed-income-annuities/compare
- Retrieved: YES
- Facts extracted (all five products show **minimum investment $10,000**):

  | Product | Issuer | Max issue age (qual / QLAC / nonqual) | Deferral period | Income start deadline (nonqual / qual / QLAC) | Period certain | Life w/ guarantee periods | Annual increase |
  |---|---|---|---|---|---|---|---|
  | Guardian SecureFuture Income Annuity | The Guardian Insurance & Annuity Company, Inc. | 73 / 82 / 80 | 13 months–40 years | 85 / RMD age / 85 | 5–10 yrs | 5–30 yrs | 1%–5% |
  | MassMutual RetireEase Choice | Massachusetts Mutual Life Insurance Company | 71 / 83 / 88 | 13 months–30 years | 90 / 72 / 85 | 5–30 yrs | 10–30 yrs | 1%–4% |
  | New York Life Guaranteed Future Income Annuity II | New York Life Insurance and Annuity Corporation | 73 / 80 / 80 | 2–40 years | 85 / RMD age / 85 | 10–30 yrs | 10–30 yrs | 1%–3% |
  | USAA Life Protected Deferred Income Annuity | USAA Life Insurance Company / USAA Life of New York | 71 / 83 / 83 | 2–30 years | 85 / 73 / 85 | 5–30 yrs | 5–30 yrs | 1%–3% |
  | Western & Southern IncomeSource Select | Western-Southern Life Assurance Company / National Integrity Life | 73 / 83 / 83 | 13 months–40 years | 85 / RMD age / 85 | n/s | 5–30 yrs | 1%–5% |

  - Western & Southern is flagged as allowing **up to two changes to the income
    start date**, versus one for the competitors — the only multi-change design
    identified.
  - Note: this table's Guardian max qualified issue age (73) and MassMutual
    qualified income-start deadline (72) reflect post-SECURE updates relative to
    the older insurer PDFs [S2][S3]; NYL's "2–40 years" deferral matches the
    24-month minimum in [S1].

### S7. New York Life — official GFI II client fact sheet on nylannuities.com (FAILED FETCH)
- URL attempted: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_GFI_II_Generic.pdf
- Retrieved: **NO** — HTTP 403 Forbidden. The NYLIAC content was obtained instead
  from the distributor-hosted copy [S1], which carries NYL's own policy form
  numbers and NYLIAC issuer statement.

### S8. MassMutual — official RetireEase Choice guide on compass.massmutual.com (FAILED FETCH)
- URL attempted: https://compass.massmutual.com/api/public/assets/file/bltd738363f5d003651
- Retrieved: **NO** — request timed out (60s). A current-vintage MassMutual DIA
  guide was therefore **not** obtained; [S2] is the 2019 edition.

### S9. Fidelity communications-hosted insurer fact sheets (PARTIAL FAILURE)
- URLs attempted: https://communications.fidelity.com/fili/docs/guardian-dia-factsheet.pdf
  and https://communications.fidelity.com/fili/docs/usaa-dia-factsheet.pdf
- Retrieved: **NO** — both returned an HTML interstitial rather than PDF bytes when
  fetched directly. Guardian content was obtained from a mirror [S3]; **no USAA Life
  primary document was retrieved** (USAA parameters below come only from [S6]).

### S10. Brighthouse Financial — "Single Premium Deferred Annuities / Income Annuities — Guaranteed Income Builder QLAC client brochure" (FAILED FETCH)
- URL attempted: https://www.brighthousefinancial.com/content/dam/brighthouse-financial/public/pdfs/gib/GIB-QLAC-Client-Brochure.pdf
- Retrieved: **NO** — HTTP 403 Forbidden. No Brighthouse facts are asserted below.

### S11. Guardian brochure on immediateannuities.com (FAILED FETCH)
- URL attempted: https://www.immediateannuities.com/annuity-brochures/guardian-securefuture-income-annuity.pdf
- Retrieved: **NO** — HTTP 403 Forbidden.

---

## Regulatory and actuarial references

### R1. 26 CFR § 1.401(a)(9)-6(q) — Qualifying longevity annuity contract (current text)
- Publisher: U.S. Government (eCFR, current edition), Treasury/IRS.
- Doc type: codified Treasury Regulation.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.401(a)(9)-6
  (renders 26 CFR 1.401(a)(9)-6; human-readable equivalent
  https://www.ecfr.gov/current/title-26/section-1.401(a)(9)-6)
- Retrieved: YES (full section text extracted)
- Source credit line in the regulation: `[T.D. 9130, 69 FR 33293, June 15, 2004; …
  T.D. 9673, 79 FR 37639, July 2, 2014; … T.D. 10001, 89 FR 58907, July 19, 2024]`
  — i.e., the paragraph (q) QLAC rules were **restructured from the old "A-17"
  Q&A format into paragraph (q) by the July 2024 final regulations** [R6].
- Facts extracted:
  - **(q)(1) Definition — a QLAC must satisfy all seven of:**
    (i) premiums satisfy the (q)(2) limitation;
    (ii) "distributions under the contract must commence not later than a specified
    annuity starting date that is **no later than the first day of the month next
    following the 85th anniversary of the employee's birth**";
    (iii) after distributions commence they satisfy § 1.401(a)(9)-6 (other than the
    (a)(3) requirement that payments commence by the required beginning date);
    (iv) "After the required beginning date, the contract does **not make available
    any commutation benefit, cash surrender right, or other similar feature (other
    than a right to rescind the contract within a period not exceeding 90 days from
    the date of purchase)**";
    (v) no death benefits other than those in (q)(3);
    (vi) the contract (or rider/endorsement) **states that it is intended to be a
    QLAC**, when issued (or December 31, 2016, if later);
    (vii) the contract is **not a variable contract under section 817, an indexed
    contract, or a similar contract**, except as the Commissioner provides.
  - **(q)(2)(ii) Dollar limitation** — "The dollar limitation as of a premium payment
    date is an amount by which **$200,000** (as adjusted under paragraph
    (q)(4)(ii)(A)) exceeds the sum of — (A) the premiums paid before that date with
    respect to the contract, and (B) the premiums paid on or before that date with
    respect to **any other contract that is intended to be a QLAC** … purchased for
    the employee under the plan, or any other plan, annuity, or account described in
    **section 401(a), 403(a), 403(b), or 408 or eligible governmental plan under
    section 457(b)**."
  - **There is no percentage-of-account-balance limitation in the current text.**
    The former 25% limit has been removed (see [R2] for the statutory command).
  - **(q)(2)(iii) Exchange**: if an insurance contract is exchanged for a QLAC, the
    **fair market value** of the exchanged contract is treated as a premium paid. If
    a contract is surrendered for cash and the cash used to buy a QLAC, **only the
    cash** is treated as premium.
  - **(q)(4)(ii)(A) Indexing**: "The **$200,000** amount … will be adjusted at the
    same time and in the same manner as the limits are adjusted under section
    415(d), except that — (1) The **base period is the calendar quarter beginning
    July 1, 2022**; and (2) the amount of any increment to the limit that is not a
    multiple of **$10,000 will be rounded to the next lowest multiple of $10,000**."
  - **(q)(4)(ii)(B) Age limitation** may be adjusted for mortality changes by
    published Commissioner guidance. **(q)(4)(ii)(C)** adjustments apply
    prospectively only.
  - **(q)(3) Permitted death benefits** — this is the exhaustive list:
    - **(i) Surviving spouse sole beneficiary**: the only benefit permitted is a
      **life annuity payable to the surviving spouse** whose periodic payment does
      **not exceed 100%** of the payment that was (or would have been) payable to
      the employee. If death is before the annuity starting date, the spouse's
      annuity must commence **no later than the date the employee's annuity would
      have commenced**.
    - **(ii) Surviving spouse not sole beneficiary**: the only benefit permitted is a
      **life annuity to the designated beneficiary** not exceeding the **applicable
      percentage** of the employee's payment. If death is before the annuity starting
      date, the beneficiary's annuity must commence **by the last day of the calendar
      year following the calendar year of the employee's death**.
    - **(iii) Applicable percentage** — three cases:
      (A) contracts with **no pre-annuity-starting-date non-spousal death benefit** →
      the percentage from the MDIB table in paragraph (b)(3);
      (B) contracts with a **set (irrevocable) non-spousal beneficiary designation** →
      Table 6 to (q)(3)(iii)(D);
      (C) contracts providing a **return of premium** → the applicable percentage is
      **0**.
    - **Table 6 to (q)(3)(iii)(D) — applicable percentage by adjusted
      employee/beneficiary age difference** (verbatim):
      ≤2 yrs → 100; 3 → 88; 4 → 78; 5 → 70; 6 → 63; 7 → 57; 8 → 52; 9 → 48;
      10 → 44; 11 → 41; 12 → 38; 13 → 36; 14 → 34; 15 → 32; 16 → 30; 17 → 28;
      18 → 27; 19 → 26; 20 → 25; 21 → 24; 22 → 23; 23 → 22; 24 → 21;
      **25 and greater → 20**.
    - **(v) Return of premiums** — "In lieu of a life annuity payable to a designated
      beneficiary …, a QLAC **may provide for a benefit to be paid to a beneficiary
      after the death of the employee up to the amount by which the premium payments
      made with respect to the QLAC exceed the payments already made under the
      QLAC**." It may also be provided after the death of both the employee and a
      surviving spouse receiving a life annuity. **Timing**: the ROP payment must be
      paid **no later than the end of the calendar year following the calendar year
      in which the employee (or surviving spouse) dies**; if death is after the
      required beginning date, the ROP payment is **treated as an RMD for the year
      paid and is not eligible for rollover**.
    - **(vii) Former spouses**: survivor benefits to a former spouse do not disqualify
      the contract where a QDRO (or divorce/separation instrument) issued in
      connection with the divorce provides that the former spouse is entitled to the
      survivor benefits / is treated as a surviving spouse / does not modify the
      former spouse's treatment as beneficiary or measuring life.
  - **(q)(4)(i)(B) Excess premiums and correction**: a contract that fails solely
    because a premium exceeds the (q)(2) limit ceases to be a QLAC **on the date the
    premium is paid**, and its value may no longer be disregarded under
    § 1.401(a)(9)-5(b)(4) — **unless the excess premium is returned to the non-QLAC
    portion of the account by the end of the calendar year following the calendar
    year in which it was paid**, in which case the contract is treated as never
    having exceeded the limit. Returning an excess premium is **not** treated as a
    prohibited commutation benefit.
  - **(q)(4)(iii)(A) Structural deficiency**: if a contract fails to be a QLAC for
    any reason other than excess premium, it is **retroactively, as of the date of
    purchase**, not a QLAC and not a contract "intended to be a QLAC".
  - **(q)(4)(iii)(B) Roth IRAs**: a contract purchased under a Roth IRA is **not
    treated as intended to be a QLAC** for the dollar-limit rule; a QLAC later rolled
    over or converted to a Roth IRA stops being treated as intended to be a QLAC.
  - **(q)(4)(iv) Permitted features**: a QLAC does not fail (q)(1)(vii) merely
    because it is a **participating annuity paying dividends** described in (n)(3)(iii),
    or because it provides a **cost-of-living adjustment as described in paragraph
    (o)(2)**.
  - **(q)(4)(v)**: for group annuity contracts, the "intended to be a QLAC" statement
    is satisfied by a **certificate** so stating.

### R2. SECURE 2.0 Act of 2022, § 202 ("Qualifying Longevity Annuity Contracts") — Division T of Pub. L. 117-328
- Publisher: U.S. Government Publishing Office (govinfo), enrolled text of Public
  Law 117-328 (Consolidated Appropriations Act, 2023), Division T = SECURE 2.0 Act
  of 2022. Statutory note codified at 26 U.S.C. 401 note; text at 136 Stat.
  5331–5332.
- Doc type: enacted federal statute.
- URL fetched: https://www.govinfo.gov/content/pkg/PLAW-117publ328/html/PLAW-117publ328.htm
- Retrieved: YES (full text downloaded; § 202 located and read)
- **Section number verified: SEC. 202, titled "QUALIFYING LONGEVITY ANNUITY
  CONTRACTS."** Facts extracted verbatim/near-verbatim:
  - **(a) In general**: "Not later than the date which is **18 months after the date
    of the enactment of this Act**, the Secretary of the Treasury … shall amend the
    regulation … relating to 'Longevity Annuity Contracts' (**79 Fed. Reg. 37633
    (July 2, 2014)**), as follows:"
  - **(a)(1) Repeal 25-percent premium limit**: amend "**Q&A-17(b)(3) of Treas. Reg.
    section 1.401(a)(9)-6 and Q&A-12(b)(3) of Treas. Reg. section 1.408-8** to
    **eliminate the requirement that premiums for qualifying longevity annuity
    contracts be limited to 25 percent of an individual's account balance**".
    → **Confirms the 25%-of-account-balance limit was removed by SECURE 2.0 § 202.**
  - **(a)(2)(A) Increase dollar limitation**: amend Q&A-17(b)(2)(i) "to increase the
    dollar limitation on premiums for qualifying longevity annuity contracts **from
    $125,000 to $200,000**".
  - **(a)(2)(B) Adjustments for inflation**: for "calendar years beginning on or
    after **January 1 of the second year following the year of enactment**", the
    $200,000 limit is adjusted in the same manner as section 415(d) limits, "except
    that the **base period shall be the calendar quarter beginning July 1 of the year
    of enactment**, and any increase … which is not a multiple of $10,000 will be
    **rounded to the next lowest multiple of $10,000**." (Enactment year 2022 →
    base period Q3 2022, first indexed year 2024 — matching R1's codified text.)
  - **(a)(3) Facilitate joint and survivor benefits**: a QLAC purchased with joint
    and survivor benefits permissible at purchase is not affected by a **divorce
    occurring after the original purchase and before annuity payments commence**,
    provided a QDRO (or divorce/separation instrument) meets stated conditions.
  - **(a)(4) Permit short free look period**: amend Q&A-17(a)(4) to ensure it "does
    not preclude a contract from including a provision under which an employee may
    **rescind the purchase of the contract within a period not exceeding 90 days from
    the date of purchase**."
  - **(c)(1) Effective dates**:
    - **(A) Paragraphs (a)(1) and (a)(2) [the 25% repeal and the $200,000 limit] are
      effective with respect to contracts purchased or received in an exchange **on
      or after the date of the enactment of this Act**"** (i.e., **December 29, 2022**
      [unverified — the enactment date itself was not separately verified from a
      retrieved source]).
    - **(B) Paragraphs (a)(3) and (a)(4) [divorce and free look] are effective with
      respect to contracts purchased or received in an exchange **on or after July 2,
      2014**"** — i.e., retroactive to the original QLAC regulation.
  - **(c)(2) Enforcement and interpretations**: before final regulations, the
    Secretary must administer the law per subsection (a) and the effective dates,
    and "**taxpayers may rely upon their reasonable good faith interpretations**".

### R3. IRS Notice 2025-67 — "2026 Amounts Relating to Retirement Plans and IRAs, as Adjusted for Changes in Cost-of-Living"
- Publisher: Internal Revenue Service (irs.gov); published in Internal Revenue
  Bulletin 2025-49.
- Doc type: IRS notice (annual COLA).
- URL fetched: https://www.irs.gov/pub/irs-drop/n-25-67.pdf
- Retrieved: YES
- Fact extracted (verbatim): "**The limitation on premiums paid for a qualifying
  longevity annuity contract under § 1.401(a)(9)-6(q)(2)(ii) remains $210,000.**"
  → **QLAC dollar limit for 2026 = $210,000**, unchanged from 2025. Corroborated
  independently by Pacific Life's Feb-2026 fact sheet [S4].

### R4. 26 CFR § 1.401(a)(9)-5(b)(4) — Exclusion of QLAC value from the account balance
- Publisher: eCFR (current edition), Treasury/IRS.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.401(a)(9)-5
- Retrieved: YES
- Fact extracted (verbatim): "**(4) Exclusion for QLAC. The account balance does not
  include the value of any qualifying longevity annuity contract (QLAC), defined in
  § 1.401(a)(9)-6(q), that is held under the plan.**"
  → This is the operative provision that **removes QLAC value from the RMD
  denominator**.
- Credit line: `[… T.D. 9673, 79 FR 37639, July 2, 2014; T.D. 9930, 85 FR 72477,
  Nov. 12, 2020; T.D. 10001, 89 FR 58907, July 19, 2024]`.

### R5. 26 CFR § 1.408-8(h) — QLACs in the IRA context
- Publisher: eCFR (current edition), Treasury/IRS.
- URL fetched: https://www.ecfr.gov/api/renderer/v1/content/enhanced/current/title-26?chapter=I&subchapter=A&part=1&section=1.408-8
- Retrieved: YES
- Facts extracted:
  - **(h)(1)**: "The special rule in § 1.401(a)(9)-5(b)(4) for a QLAC … **applies to
    an IRA**, subject to the modifications set forth in this paragraph (h)."
  - **(h)(2) Reliance on representations**: unless it has actual knowledge to the
    contrary, the IRA trustee/custodian/issuer may rely on the **IRA owner's written
    representation** of the amount of QLAC premiums not paid under that IRA.
  - **(h)(3)**: for a contract rolled from a plan to an IRA before the plan's required
    beginning date, the irrevocable non-spouse beneficiary selection deadline is
    satisfied if the contract requires selection **by the end of the year following
    the year of the rollover**.
  - **(h)(4) Roth IRAs**: "The rule in § 1.401(a)(9)-5(b)(4) **does not apply to a
    Roth IRA**." A contract purchased under a Roth IRA is not treated as intended to
    be a QLAC for the dollar limit; a QLAC rolled over/converted to a Roth IRA stops
    being so treated.
  - **(j) Applicability date**: "This section applies for purposes of determining
    required minimum distributions **for calendar years beginning on or after January
    1, 2025**." For earlier years the April 1, 2023 edition applies.
- Credit line: `[… T.D. 9673, 79 FR 37642, July 2, 2014; T.D. 10001, 89 FR 58948,
  July 19, 2024]`.

### R6. T.D. 10001 — "Required Minimum Distributions", final regulations (Federal Register)
- Publisher: Treasury Department / Internal Revenue Service.
- Doc type: final rule.
- URL fetched (metadata via Federal Register API):
  https://www.federalregister.gov/documents/2024/07/19/2024-14542/required-minimum-distributions
- Retrieved: YES (metadata; full preamble not read — see "Gaps and caveats")
- Facts extracted: title "**Required Minimum Distributions**"; document number
  **2024-14542**; **citation 89 FR 58886**; publication date **July 19, 2024**;
  action "**Final regulations**"; **effective September 17, 2024**.
- Relationship to QLACs: this is the T.D. that produced the current
  § 1.401(a)(9)-6(q), § 1.401(a)(9)-5(b)(4) and § 1.408-8(h) text cited above —
  the eCFR credit lines name **T.D. 10001, 89 FR 58907 / 58948, July 19, 2024**
  [R1][R4][R5]. It **restructured the QLAC rules out of the "A-17" Q&A format into
  paragraph (q)** and implemented SECURE 2.0 § 202 [R2]. Companion **proposed**
  regulations of the same date are at 89 FR 58644 (document 2024-14543, "Notice of
  proposed rulemaking and notice of public hearing").

### R7. T.D. 9673 — "Longevity Annuity Contracts", final regulations (the original 2014 QLAC rule)
- Publisher: Treasury Department / Internal Revenue Service.
- URL fetched (metadata via Federal Register API):
  https://www.federalregister.gov/documents/2014/07/02/2014-15524/longevity-annuity-contracts
- Retrieved: YES (metadata)
- Facts extracted: title "**Longevity Annuity Contracts**"; document number
  **2014-15524**; **citation 79 FR 37633**; publication date **July 2, 2014**.
  Abstract: final regulations "relating to the use of longevity annuity contracts in
  tax-qualified defined contribution plans under section 401(a) …, section 403(b)
  plans, individual retirement annuities and accounts (IRAs) under section 408, and
  eligible governmental plans under section 457(b)". This is the rule SECURE 2.0
  § 202 directs Treasury to amend [R2], and is the origin of the QLAC concept.

### R8. Internal Revenue Code § 72 — Annuities; certain proceeds of endowment and life insurance contracts
- Publisher: Cornell Legal Information Institute (LII) rendering of 26 U.S.C. § 72.
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (key subsections read; full section is long)
- Facts extracted:
  - **§ 72(b) Exclusion ratio**: the excludable part of any amount received as an
    annuity "bears the same ratio to such amount as the **investment in the
    contract** … bears to the **expected return under the contract**". The exclusion
    may not exceed "the **unrecovered investment in the contract** immediately before
    the receipt of such amount". If payments cease by reason of death with an
    unrecovered investment remaining, that amount "shall be allowed as a **deduction
    to the annuitant for his last taxable year**".
  - **§ 72(c) Definitions**: **investment in the contract** = aggregate premiums or
    other consideration paid, minus aggregate amounts previously received to the
    extent excludable from gross income. **Expected return**, where it depends on
    life expectancy, is computed "with reference to **actuarial tables prescribed by
    the Secretary**"; otherwise it is the aggregate of amounts receivable as an
    annuity.
  - **§ 72(q)**: 10% additional tax on premature distributions from annuity
    contracts, with exceptions including distributions on or after age **59½**,
    disability, death, and distributions that are "part of a **series of
    substantially equal periodic payments** … made for the life (or life expectancy)
    … of the taxpayer".
  - **§ 72(s)**: required distributions on the holder's death — if death is **after**
    annuity payments begin, the remaining interest must be distributed "**at least as
    rapidly as under the method of distributions being used as of the date of his
    death**"; if death is **before** the annuity starting date, distribution must be
    made "**within 5 years after the death**" (subject to the statutory exceptions).
- Modelling relevance: for a nonqualified DIA the exclusion ratio determines the
  taxable share of each income payment; the pre-59½ 10% penalty is why insurers
  gate acceleration/withdrawal features at 59½ [S1][S3][S4].

### R9. NAIC — Valuation Manual, January 1, 2026 edition
- Publisher: National Association of Insurance Commissioners.
- Doc type: statutory valuation manual (457 pages).
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (full 457-page text extracted and searched directly)
- Facts extracted:
  - **VM-01 definition (statutory definition of the product)**: "The term
    '**deferred income annuity**' (DIA) means an annuity contract that guarantees a
    periodic payment for the life of the annuitant or a term certain and **payments
    begin 13 months or later from the issue date** if the contract holder and/or
    annuitant survives to a predetermined future age."
  - **VM-22 title**: "Requirements for Principle-Based Reserves for Non-Variable
    Annuities."
  - **VM-22 Section 2.B Effective Date**: "These requirements apply for **valuation
    dates on or after January 1, 2026**." **Transition**: a company may elect to keep
    using VM-A / VM-C / VM-M / VM-V for business otherwise subject to VM-22 PBR and
    issued during the **first three years** following the effective date; once VM-22
    PBR is elected for a block it must continue; **all applicable blocks must be on
    VM-22 PBR prospectively three years after the effective date**.
  - **VM-22 Section 3.F.1.a — Reserving Categories**: the "**Payout Annuity Reserving
    Category**" expressly includes "**ii. Deferred Income Annuity contracts**",
    alongside SPIAs, structured settlements in payout or deferred status, fixed
    income payment streams from settlement options/annuitizations, supplementary
    contracts with scheduled payments, certain group-annuity certificates, and
    Pension Risk Transfer annuities. Other categories: "Longevity Reinsurance
    Reserving Category" and "Accumulation Reserving Category". Payout and
    Accumulation categories may be aggregated only if the company manages both in an
    **integrated risk management process** and within a **single portfolio or
    portfolios with the same ALM strategy**.
  - **VM-22 Section 3.A**: aggregate reserve = **SR** (stochastic reserve, Section 4)
    + **DR** (deterministic reserve) for contracts passing the Single Scenario Test +
    reserves for contracts valued under VM-A/VM-C/VM-M/VM-V. The **Additional
    Standard Projection Amount** is required for **disclosure purposes** pursuant to
    VM-31.
  - **VM-22 standard projection — prescribed maintenance expense (Table 6.1)**:
    Payout Annuity Reserving Category individual contracts/certificates **$50** per
    contract per year; Fixed Indexed Annuities and other Accumulation-category
    contracts **with** guaranteed living benefits **$100**; all other individual
    contracts **$75**. Escalated by **[1.025]^(valuation year − 2015)** in the first
    projection year and by an assumed **2.5%** annual inflation thereafter. Plus
    **seven basis points** of projected account value; **for contracts without an
    account value (such as Payout Annuity Reserving Category), the seven basis points
    are applied to the present value** of (the projected benefits — text truncated at
    the page break in the extract).
  - **VM-22 standard projection — lapse**: "For contracts in which there is **no
    account value or surrender benefit**, such as some contracts within the Payout
    Annuity Reserving Category …, **this section is not applicable**." (i.e., **no
    lapse assumption** for a DIA.)
  - **VM-22 standard projection — annuitization**: "The annuitization rate for
    contracts shall be **0% at all projection intervals**."
  - **VM-22 Section 6 standard projection mortality for the Payout Annuity Reserving
    Category** (other than structured settlements) — the prescribed generational
    formula:
    ```
    q_x^(2012+n) = q_x^(2012) * (1 - G2_x)^n * F_x
    ```
    where `q_x` is from the **2012 IAM Basic Mortality Table** (VM-M Section 2.C),
    `G2_x` is **Projection Scale G2** (VM-M Section 1.J.1.c), and `F_x` is the factor
    from **Table 6.8** (Payout Annuity Reserving Category). Guidance note: the rates
    are **age nearest birthday**; a company using age last birthday should convert
    with
    ```
    q(x)_ALB = [ q(x)_ANB + (1 - q(x)_ANB) * q(x+1)_ANB ] / (2 - q(x)_ANB)
    ```
    The Fx factors "represent adjustments to the 2012 IAM Basic Mortality Table
    brought up to the current period using Projection Scale G2 … Such adjustments
    reflect emerging experience, including the impact of how historical mortality
    improvement has differed from the G2 scale. The G2 scale for use in projecting
    mortality improvement on a going forward basis has not changed."
  - **Table 6.8 — Fx for Individual Annuities in Payout Annuity Reserving Category**
    (attained age → Female / Male), as extracted:
    ≤50–57: 125.0% / 100.0%; 58: 120.6% / 99.0%; 59: 116.2% / 98.0%;
    60: 111.8% / 97.0%; 61: 107.4% / 96.0%; 62: 103.0% / 95.0%; 63: 101.0% / 95.4%;
    64: 99.0% / 95.8%; 65: 97.0% / 96.2%; 66: 95.0% / 96.6%; 67: 93.0% / 97.0%;
    68: 94.4% / 98.6%; 69: 95.8% / 100.2%; 70: 97.2% / 101.8%; 71: 98.6% / 103.4%;
    72: 100.0% / 105.0%; 73: 101.6% / 107.0%; 74: 103.2% / 109.0%;
    75: 104.8% / 111.0%; 76: 106.4% / 113.0%; 77: 108.0% / 115.0%;
    78: 108.0% / 116.0%; 79: 108.0% / 117.0%. (Table continues beyond age 79 in the
    Valuation Manual; only ages ≤79 were captured in this extract.)
    For contrast, **Table 6.7** (Accumulation Reserving Category) starts at
    150.0% / 120.0% (female/male) for ages ≤52 without guaranteed living benefits.
  - **VM-M Section 1.J — 2012 Individual Annuity Reserve Valuation Table**:
    - "**2012 IAR Table**" = the generational mortality table developed by the Joint
      Academy/SOA Payout Annuity Table Team containing rates `q_x^(2012+n)` derived
      from a combination of the **2012 IAM Period Table** and **Projection Scale G2**,
      per Appendix A-821 of the AP&P Manual.
    - "**2012 IAM Period Table**" = the period table containing **loaded** mortality
      rates for calendar year 2012 (`q_x^2012`).
    - "**Projection Scale G2**" = annual rates `G2_x` of mortality improvement by age
      for projecting future mortality beyond calendar year 2012.
    - "**2012 IAM Basic Table**" = the **unloaded** mortality table.
    - **Application formula (verbatim)**:
      ```
      q_x^(2012+n) = q_x^(2012) * (1 - G2_x)^n
      ```
      "The resulting `q_x^(2012+n)` shall be **rounded to three decimal places per
      1,000**, e.g., 0.741 deaths per 1,000. Also, the **rounding shall occur
      according to the formula above, starting at the 2012 period table rate**."
      Worked example given: male age 30, `q_x^2012 = 0.741`;
      `q_x^2013 = 0.741 × (1 − 0.010)^1 = 0.73359 → 0.734`;
      `q_x^2014 = 0.741 × (1 − 0.010)^2 = 0.7262541 → 0.726`. The manual explicitly
      warns that computing `q_x^2014` as `0.734 × 0.99 = 0.727` (chaining the rounded
      rate) is **incorrect**.
  - **VM-V ("Statutory Maximum Valuation Interest Rates for Formulaic Reserves"),
    Section 1 Income Annuities** — scope explicitly includes "**b. Deferred income
    annuity contracts issued after Dec. 31, 2017**" (alongside immediate annuities,
    structured settlements, settlement-option payouts, supplementary contracts, CDA
    and GLB payment streams once funds are exhausted, and certain group-annuity
    certificates), for contracts **not passing the Stochastic Exclusion Test** under
    VM-22 Sections 1–13.
  - **VM-V Section 1.C.1 — Valuation Rate Buckets** (A–D):
    - Table 1.C-1 (no life contingencies, by reference period RP):
      RP ≤ 5Y → **A**; 5Y < RP ≤ 10Y → **B**; 10Y < RP ≤ 15Y → **C**; RP > 15Y → **D**.
    - Table 1.C-2 (with life contingencies, by RP and **initial age**):
      initial age **90+**: A / B / C / D across the four RP bands;
      **80–89**: B / B / C / D; **70–79**: C / C / C / D;
      **<70**: D / D / D / D.
      (A DIA sold at ages 50–70 with a long deferral therefore lands in **Bucket D**.)
  - **VM-V Section 1.C.2 — Premium determination date**: for a **deferred income
    annuity** it is the "**Date consideration is determined and committed to by
    contract holder**" (same rule as for immediate annuities). Guidance note: the
    company should interpret this consistently with its standard practices; "For some
    products, that interpretation may be the **issue date or the date the premium is
    paid**." **Immaterial change**: if the consideration changes by less than **10% in
    present value and less than $1 million**, the original premium determination date
    is retained.
  - **VM-V Section 1.C.3 — Rate determination**: the statutory maximum valuation
    interest rate depends on the **Valuation Rate Bucket**, the **Premium
    Determination Date**, and whether the contract is a **jumbo** or **non-jumbo**
    contract. Jumbo rates are **published daily by the NAIC**; non-jumbo rates
    **quarterly**, both on the Industry tab of the NAIC website.
  - **VM-V prescribed portfolio credit quality distribution** (used to weight the
    expected default costs / spreads): **5% Treasuries; 15% Aa bonds (5% Aa1, 5% Aa2,
    5% Aa3); 40% A bonds (13.33% A1, A2, A3); 40% Baa bonds (13.33% Baa1, Baa2,
    Baa3)** — with "40%/3 used unrounded in the calculations".
  - **VM Section II** treatment: contracts subject to VM-22 are the applicable
    non-variable annuity contracts specified in VM Section II Subsection 2 "Annuity
    Products" paragraphs C and D and applicable Deposit-Type Contracts.

### R10. NAIC — Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805), Fall 2020 edition
- Publisher: National Association of Insurance Commissioners.
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (all 5 pages)
- **Directly answers the brief's nonforfeiture question.** Facts extracted:
  - **Section 2 Applicability** — the Act "shall **not** apply to any reinsurance,
    group annuity purchased under a retirement plan … (other than a plan providing
    individual retirement accounts or individual retirement annuities under Section
    408 …), premium deposit fund, variable annuity, investment annuity, **immediate
    annuity**, **any deferred annuity contract after annuity payments have
    commenced**, or reversionary annuity …". **A DIA in its deferral phase is a
    deferred annuity and is NOT within any of these exclusions — Model #805 applies
    to it.** (Sections 3–8 additionally do not apply to contingent deferred
    annuities.)
  - **Section 3.A(1)**: on cessation of payment of considerations, or on written
    request, the company shall grant a **paid-up annuity benefit** on a plan
    stipulated in the contract, of value specified in Sections 5–8 and 10.
  - **Section 3.A(2)**: the cash-surrender-benefit requirement applies only "**If a
    contract provides for a lump sum settlement at maturity, or at any other time**"
    — i.e., **a contract that never offers a lump sum is not required to provide a
    cash surrender benefit.** This is the mechanism by which a zero-cash-value DIA
    complies.
  - **Section 3.A(3)–(4)**: the contract must state the mortality table (if any) and
    interest rates used in computing minimum paid-up annuity, cash surrender or death
    benefits, with sufficient information to determine the amounts, and must state
    that such benefits are not less than the statutory minimums.
  - **Section 3.B**: if no considerations have been received for **two full years**
    and the portion of the paid-up annuity benefit at maturity arising from prior
    considerations would be **less than $20 monthly**, the company may terminate the
    contract by paying the then present value of that portion.
  - **Section 4.A(1) Minimum nonforfeiture amount**: an accumulation of the **net
    considerations** paid at the Subsection B interest rates, decreased by prior
    withdrawals/partial surrenders accumulated at those rates, an **annual contract
    charge of $50** accumulated at those rates, and further items (c)–(d) [the
    remainder of Section 4.A(1) and the Subsection B nonforfeiture interest rate
    definition were not captured in the extracted pages — see "Gaps and caveats"].
  - **Section 5 Computation of Present Value**: "Any paid-up annuity benefit
    available under a contract shall be such that its **present value on the date
    annuity payments are to commence is at least equal to the minimum nonforfeiture
    amount on that date**. Present value shall be computed using the mortality table,
    if any, and the interest rates **specified in the contract**."
  - **Section 7 Calculation of Paid-up Annuity Benefits** — the provision that
    governs a no-cash-value DIA: "**For contracts that do not provide cash surrender
    benefits**, the present value of any paid-up annuity benefit available as a
    nonforfeiture option at any time prior to maturity shall not be less than the
    present value of that portion of the maturity value of the paid-up annuity
    benefit provided under the contract arising from considerations paid prior to the
    time the contract is surrendered in exchange for, or changed to, a deferred
    paid-up annuity … **For contracts that do not provide any death benefits prior to
    the commencement of any annuity payments, present values shall be calculated on
    the basis of such interest rate and the mortality table specified in the contract
    for determining the maturity value of the paid-up annuity benefit.** However, in
    no event shall the present value of a paid-up annuity benefit be less than the
    minimum nonforfeiture amount at that time."
  - **Section 8 Maturity Date**: where optional maturity dates may be elected, the
    maturity date is deemed the **latest date permitted by the contract**, but not
    later than the contract anniversary next following the annuitant's **70th
    birthday** or the **tenth contract anniversary**, whichever is later.
  - **Section 9 Disclosure of Limited Death Benefits**: "A contract that does **not
    provide cash surrender benefits** or does not provide death benefits at least
    equal to the minimum nonforfeiture amount prior to the commencement of any
    annuity payments **shall include a statement in a prominent place in the contract
    that such benefits are not provided**." → This is the model-law basis for the
    prominent cover-page warnings the Compact standard requires [R13] and that appear
    in DIA marketing [S1][S2].
  - Chronological summary: adopted 1977; amended 2003, 2017 (3rd quarter), Fall 2020.

### R11. NAIC — Annuity Disclosure Model Regulation (Model #245)
- Publisher: National Association of Insurance Commissioners (© 2015 edition of the
  model text within the Fall compendium).
- URL fetched: https://content.naic.org/sites/default/files/model-law-245.pdf
- Retrieved: YES (40 pages)
- Facts extracted:
  - Table of contents includes Section 3 "Applicability and Scope", Section 4
    "Definitions", Section 5 "Standards for the Disclosure Document and Buyer's
    Guide".
  - **Section 3 Applicability and Scope** — "This regulation applies to all group and
    individual annuity contracts and certificates **except: A. Immediate and deferred
    annuities that contain no non-guaranteed elements**; …" plus exclusions for
    ERISA/401(a)/401(k)/403(b)/457/church-plan-funding annuities, non-registered
    variable annuities sold to accredited investors/qualified purchasers, and
    (subject to a drafting note about NSMIA preemption) transactions involving
    variable annuities and other registered products complying with SEC/FINRA
    disclosure and illustration rules.
  - **Modelling/compliance relevance**: a **non-participating DIA has no
    non-guaranteed elements** — every income benefit is guaranteed at the time each
    premium is paid [R13] — so such a contract falls squarely within the
    **Section 3.A exemption** from Model #245. A **participating** DIA paying
    dividends [R13 § 3.T] would have a non-guaranteed element and would not be
    exempt on that ground. [The Section 3.A characterisation is a direct reading of
    the retrieved text; whether individual states apply it the same way to DIAs was
    not verified — see "Gaps and caveats".]

### R12. NAIC — Variable Annuity Model Regulation (Model #250) — **identifies a mis-numbering in the brief**
- Publisher: National Association of Insurance Commissioners (October 2007 edition).
- URL fetched: https://content.naic.org/sites/default/files/model-law-250.pdf
- Retrieved: YES
- Fact extracted: **NAIC Model #250 is the "VARIABLE ANNUITY MODEL REGULATION"**, not
  an annuity disclosure regulation. Its sections are: Authority; Definitions;
  Qualifications of Insurance Companies to Issue Variable Annuities; Separate
  Account; Filing of Contracts; Variable Annuity Contracts; Nonforfeiture Benefits;
  Required Reports; Foreign Companies; Qualities of Agents. Section 2.B defines
  "variable annuity" as a contract providing "annuity benefits that vary according to
  the investment experience of a separate account or accounts maintained by the
  insurer".
- Consequence: **Model #250 is not applicable to a DIA**, which is a non-variable
  general-account contract [R13]. The disclosure model the brief intended is
  **Model #245** [R11].

### R13. IIPRC — "Individual Deferred Paid-Up Non-Variable Annuity Contract Standards (Commonly Marketed as Deferred Income Annuities or Longevity Annuities)", IIPRC-A02-I-LONG
- Publisher: Interstate Insurance Product Regulation Commission (Insurance Compact).
- Doc type: adopted uniform product standard (26 pages). **This is the single most
  contractually precise DIA reference retrieved.**
- URL fetched: https://www.insurancecompact.org/sites/default/files/2022-12/171120_ind_def_pu_non_var_ann_long_stds.pdf
  (record page: https://www.insurancecompact.org/standards/record-adopted-standards/individual-deferred-paid-non-variable-annuity-contract-standards)
- Retrieved: YES (all 26 pages)
- Dates: **Adopted August 5, 2017; Effective November 20, 2017**; this rule amends the
  standards originally adopted **October 17, 2010**; amendments apply only to new
  filings received after the effective date.
- Facts extracted:
  - **Scope (verbatim)**: "These standards apply to an individual deferred paid-up
    non-variable annuity contract **with no cash surrender values prior to the
    commencement of annuity payments** that provides for a **single premium or
    flexible premiums over the deferral period** of the contract or for a shorter
    limited payment period, and that provides for **specified income payments
    beginning on a specified income commencement date for each premium paid**. Income
    payable on the commencement date is payable for **the annuitant's lifetime (with
    or without a guarantee period), or for a stipulated period certain**. A commuted
    value of some payments **may** be provided **after the annuity payments have
    commenced**. The standards require **all funds to be held in the general
    account**."
  - **Definition**: "'**Period certain annuity**' means an annuity where the annuitant
    is guaranteed a specific payment amount for a set period of time. If the annuitant
    dies before the end of the period, the annuitant's beneficiary or estate receives
    the remaining payments for the guaranteed period. **For policies that offer a
    return of premium death benefit (e.g., cash refund or installment refund options),
    the income benefit payments made prior to the death benefit shall be considered
    period certain income.**"
  - **§ 1.B(1)(g) — the nonforfeiture treatment (the key regulatory answer)**: "**In
    lieu of a nonforfeiture demonstration**, certification that the **income benefit
    provided under this contract is greater than that guaranteed at issue for the same
    premium under any non-variable deferred annuity contract offered by the company
    that provides cash surrender values during the deferral period or on the income
    commencement date.** A sample format for such certification is shown in
    Appendix A." → i.e., the Compact substitutes a **comparative-adequacy
    certification** for the usual Model #805 minimum-nonforfeiture-value
    demonstration.
  - **§ 1.B(1)(a)**: "Since the premium and income benefit are **fully defined in the
    contract**, the **mortality table and interest rate used in the deferral period
    and for determining the contractually specified income payable do not need to be
    disclosed** in the contract or the Actuarial Memorandum." → confirms there is no
    disclosed pricing basis for a DIA; the contract states dollars of income, not
    rates.
  - **§ 1.B(1)(c)–(d)**: the actuarial memorandum must disclose the interest and
    mortality basis used for income payable on any **alternative income commencement
    date or alternative income option**, including the basis for any tabular values in
    the contract, and the basis for any **specific charge** for the right to elect an
    alternative date/option.
  - **§ 1.B(1)(e)**: must describe "the **asset allocation approach** for the product,
    any **hedging policy** used in support of the product, and the **liquidity risks**
    associated with any hedging activities".
  - **§ 1.B(1)(f)**: sample death benefit calculations for representative issue ages
    **including issue age 60** if within the range.
  - **§ 1.B(1)(h)**: if supplemental premiums are permitted, a description of what
    guarantees, if any, are offered on the **paid-up annuity rates for future premium
    payments**.
  - **§ 1.B(1)(i)–(k)**: sample calculations of the commutation methodology and
    formulas; description of the methodology for the **interest rate and/or net
    investment return** used in commuted values; description of the **mortality
    assumption** used for life-contingent commuted values ("Any reasonable mortality
    assumption, consistent with applicable Actuarial Standards of Practice, may be
    used"). Drafting note: "The **commuted value must be calculated as an actuarial
    present value**. A reasonable mortality assumption would be based on credible
    data, with margins appropriate for the intended purpose."
  - **§ 2.A(8) — cover-page warning when there is no deferral-phase death benefit**
    (verbatim): "**The contract does not provide access to funds prior to the income
    commencement date. No death benefit is available to a beneficiary if the annuitant
    dies prior to the income commencement date.**"
  - **§ 2.A(9) — cover-page warning when there is one**: "**The contract does not
    provide access to funds prior to the income commencement date other than payment
    of the death benefit.**"
  - **§ 2.B Specifications page** must include: the single or initial premium; the
    date, schedule and mode of premiums; any limitations on premium amounts/timeframes;
    **all charges used in determination of the death benefit**; the **income
    commencement date** and, if it can be changed, the **minimum/maximum income
    commencement dates, minimum/maximum age, or minimum/maximum deferral period**; and
    "the **specified monthly income payment for the initial premium for the default
    income type at the income commencement date**". Participating contracts must state
    dividends are not guaranteed.
  - **§ 3.B — Annuity purchase rates for premiums paid after issue** (the core
    flexible-premium mechanic):
    - (a) "Each additional premium payment will **generate a paid up annuity** with
      guaranteed income payments beginning on a specified income commencement date and
      based on a specified income option"; if none is specified at payment, the
      contract must provide **default options**.
    - (b) "The annuity purchase rates used for such additional income benefits will be
      based on the **attained age of the annuitant, the specified income commencement
      date and specified income option, and the company's then current annuity
      purchase rates**, subject to any guarantees provided in the contract."
    - (c) "**Current annuity purchase rates**" requires the income purchased by
      additional premiums to be **not less than that in a new contract subject to
      these standards** for the same class of annuitants (dividend-paying and
      non-dividend-paying classes are separate), attained age and income commencement
      date, if the company still offers such a contract; otherwise the rates must be
      "**based on reasonable actuarial assumptions**".
    - (d) Within **30 days** of receiving an additional premium the company must send
      written confirmation of the premium amount, the **additional income benefit
      purchased**, the income option and the income commencement date; and if the
      company no longer offers a new DIA, a comparison against the guaranteed income
      under a cash-value deferred annuity it does offer. The confirmation must offer
      the option to **cancel the additional income by returning the confirmation within
      10 days** for a refund of the premium. (This matches the 10-day refund right in
      [S2] and [S3].)
  - **§ 3.H Contract values and guarantees**:
    - (1) "**All income benefits, based on the specified income commencement date and
      specified income option associated with each premium paid, shall be
      guaranteed.**" If the date or option can be changed, the contract must state any
      specific charge and must **either** (a) indicate the **mortality and interest
      assumption used in determining the actuarial equivalent value of the alternative
      income benefit**, **or** (b) contain a **table showing the alternative income
      benefit available** at various alternative commencement dates/ages and under
      various alternative income options.
    - (2) "**No commutation of income benefit stream is permitted, except for**:
      (a) lump sum payment of the **death benefit before the income commencement
      date**; (b) lump sum payment of the balance owed after an annuitant's death for
      an income option with a **period certain, installment refund or cash refund**
      feature; (c) a **lump sum value of a specified portion of the life contingent or
      non-life contingent annuity payments after the annuity payments have
      commenced**, excluding future dividend payments."
    - (3) Income payable at the commencement date must be for the annuitant's lifetime
      (with or without a guarantee period) **or** "a stipulated period certain for a
      **minimum of five (5) years with a maximum deferral period of twenty (20)
      years**".
  - **§ 3.F Commutation of annuity payments** (post-income-start liquidity, where
    offered):
    - The commuted value "shall be payable in a **lump sum only**"; non-commuted future
      benefits must be **unaffected** by the commutation.
    - **Replacement ratio disclosure**: unless the interest rate(s) and mortality table
      used to determine the commuted value are in the contract at issue, the contract
      must define the **replacement ratio** as **(i)/(ii)** where **(i)** is "the
      actual commuted value to be paid" and **(ii)** is "the commuted value calculated
      on the basis of the **current pricing assumptions** used in the determination of
      prices for the same type of income being commuted and for new contracts of the
      same class of contracts" (or, if none are currently issued, on current
      assumptions for new annuitizations of the same type of income).
    - If the rate(s) and table are in the contract at issue, the contract must include:
      "**The commuted value of any remaining annuity payments is always less than the
      sum of those benefit payments and the higher the interest rate the lower the
      commuted value.**"
    - Payment timing: if commutation information has already been provided, pay within
      **15 days** of the request; otherwise provide the information within 15 days,
      then pay within 15 days of the owner's acceptance. The commuted amount is
      determined **as of the designated date of payment**.
    - Commutation may be **limited by time, age, duration or triggering event** (shown
      on the specifications page) and **limited to a portion** of the benefits.
    - "(7) The **interest rate used to calculate commuted values can be adjusted for
      changes in interest rates, if any, between the issue date and the commutation
      date.**" Drafting note: "The intent of this section is to **reduce interest risk
      in the event of rising interest rate after issue**." → This is the regulatory
      basis for Pacific Life's "interest-rate adjustment charge" on withdrawals [S4]
      and is the DIA analogue of a market value adjustment.
  - **§ 3.I Death benefit** — **the death benefit formula is restricted to a closed
    list**: "If a death benefit is provided prior to the income commencement date, the
    contract shall describe the method of calculation, which shall be **limited to one
    of the following methodologies**: (a) **a percentage of premiums paid**;
    (b) **a percentage of premiums paid plus interest**; (c) **a flat dollar amount**;
    or (d) **any combination of (a), (b), and (c)**." Also: "(2) If a death benefit is
    provided prior to the income commencement date, it must be provided **with respect
    to both the initial premium and any additional supplemental premiums**."
  - **§ 3.J Deferral of payments**: the company **may not** reserve the right to defer
    payment of income payments or of any death benefit; it **may** reserve the right to
    defer payment of amounts payable **on commutation for up to six (6) months** (with
    prior written approval of the domiciliary regulator per § 1.A(8)).
  - **§ 3.M Income commencement date and income option**: the contract **may** provide
    that these cannot be changed. If a change right is granted, the contract must
    disclose the alternative income options, **any limitations on when a change can be
    made** (drafting example given: "change in income commencement date must be made at
    least two years before the new income commencement date"), **how often** such a
    change can be made, and **any explicit charge** for the change.
  - **§ 3.P Loans**: "The contract shall **not** include a loan provision; however, a
    company may state that the contract **does not have loan values**."
  - **§ 3.Q**: the contract shall state the **dollar amount of any minimum or maximum
    contract premium** requirements.
  - **§ 3.R Misstatement of age or sex**: the amount payable shall be "such as the
    premium payments to the company **would have purchased at the correct age** or the
    correct age and sex"; over/underpayments are charged or credited against current or
    next succeeding payments **with interest at a rate specified in the contract but
    not exceeding 6%**. With more than one annuitant, the adjustment may reflect
    misstatement of any annuitant.
  - **§ 3.N Incontestability**: contestable period **no greater than two years** from
    issue during the lifetime of the person(s) whose application statements are
    required; contests may not be based on **age and sex**; a separate two-year period
    may apply after any change requiring underwriting.
  - **§ 3.T Participating contract**: dividends used to purchase additional guaranteed
    income payments must be determined using **either** "current annuity purchase
    rates" as defined in § 3.B(1)(c), **or** "the same interest and mortality rates
    used to determine guaranteed income payments at the time of the premium payment to
    which the dividend is related was paid, and the attained age(s) of the
    annuitant(s) at the time the dividend is [applied]".
  - **§ 2.A(6)**: form numbers must carry an **`ICCxx`** prefix (xx = filing year) —
    which is why DIA form numbers appear as e.g. `ICC11–P101` [S1] and
    `ICC12-FPDIA12` [S2].
  - Self-certification is **not** available for these standards; Mix and Match with
    state product components **is** available.

### R14. American Academy of Actuaries / SOA Payout Annuity Table Team — "Payout Annuity Report" (September 28, 2011)
- Publisher: American Academy of Actuaries (report prepared by the Joint
  Academy/SOA Payout Annuity Table Team at the request of the NAIC Life Actuarial
  (A) Task Force).
- URL fetched: https://www.actuary.org/wp-content/uploads/2017/11/Payout_Annuity_Report_09-28-11.pdf
- Retrieved: YES (36 pages)
- Facts extracted:
  - The Team's charge from LATF was "to produce a new annuity valuation mortality
    table, including projection scales and margins necessary to" make it suitable for
    standard valuation. The Team developed "a basic table (**2012 IAM Table**),
    projection scale (**Scale G2**)" and explored "various approaches and levels of
    margin which were discussed and ultimately recommended by LATF. The IAR Table is
    comprised of these three [components]."
  - **Margin (verbatim)**: "the resulting margin recommended by LATF is **10% for all
    ages up to and including 100**. The margin then **grades down 1% per year for ages
    100** until the **ultimate mortality cap of 0.40000** is invoked. This results in
    a margin of zero [at that point]."
  - "The **2012 IAM Period Table is the 2012 IAM Basic Table with the margins** as
    determined by LATF, but **without future projection**."
  - The Team reviewed the approach used for the a2000 Table margins and "did not see a
    compelling reason to vary"; LATF agreed no changes in approach or level of margin
    were required.
  - Historical improvement: the Team "projected the rates from **2006-2012 (six
    years)** using Scale G2" after finding population improvement rates from 2006 to
    2009 were not inconsistent with Scale G2. For future projection the Team "decided
    to use **Scale G2, without further modification**." Scale G2 is shown in Table 11
    of the report; Table 12 compares annualized improvement in Scale G2 with U.S. Life
    Tables (sample row extracted: **1.5% / 1.5% / 1.3% / 0.6% / 1.3% / 1.3% / 1.2% /
    0.5%** across the compared age/sex bands).
  - Scale G2 "replaces **Scale G** as the scale used for individual annuity valuation."

### R15. SOA Research Institute & LIMRA — "2020-24 Payout Annuity Experience Study" (Study Highlights), © 2026
- Publisher: Society of Actuaries Research Institute (with LIMRA).
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2020-24-payout-annuity-exp-study.pdf
- Retrieved: YES (5-page Study Highlights document; the full results are behind the
  SOA "Experience Studies Pro" subscription)
- Facts extracted:
  - **"The study includes immediate annuities, deferred income annuities, settlement
    options, and annuitizations of life insurance and annuity death claims."** → the
    current SOA payout-annuity mortality basis **explicitly covers DIAs**.
  - Expected bases used for A/E ratios include the **2012 IAM Basic G2 Table**, the
    **2012 IAM Period G2 Table**, and the **2019 SSA Table** (2019 death probabilities
    from the 2022 OASDI Trustees Report; **no improvement** applied for the SSA-based
    A/E ratios). For the 2012 IAM bases, expected rates were improved (or disimproved)
    **from July 1, 2012 to July 1 of the applicable calendar year**.
  - "The 2012 IAM Basic and Period Tables were developed on an **age nearest birthday**
    basis using **amount-weighted** experience. Actual study experience was determined
    on an **age-nearest birthday** basis."
  - Data restricted to "annuitants whose payments are **life contingent now or will be
    sometime in the future**"; certain period-only non-life-contingent annuities are
    excluded; **substandard annuities excluded** due to paucity of data. **Structured
    settlement annuities are excluded** (studied separately; a structured settlement
    mortality report was published January 2020 covering 2005–2017).
  - Joint-life exposure: "no recognition is given to the secondary annuitant if alive
    while the primary annuitant is alive", because of concerns about **under-reporting
    of deaths on secondary annuitants**.
  - Results are broken out by "sex, attained age group, contract type, annual income,
    benefit class, annuitant status, **refund feature**, and contract year group",
    with and without Scale G2.
  - **26 contributing companies**, including (among those captured in the extract)
    American National, Ameriprise/RiverSource, Brighthouse Financial, CNO (Bankers
    Life & Casualty), EquiTrust, F&G Annuities & Life, and Guardian Life.
  - Prior study for comparison: **2014-19 Payout Annuity Mortality** study
    (https://www.soa.org/resources/experience-studies/2022/14-19-payout-annuity-mortality/).

### R16. SOA — "2012 Individual Annuity Reserving Report & Table" (resource page)
- Publisher: Society of Actuaries.
- URL fetched: https://www.soa.org/resources/experience-studies/2011/2012-ind-annuity-reserving-rpt/
- Retrieved: YES (page content; no date stated on the page for the report itself)
- Facts extracted: the page hosts the **Payout Annuity Report** produced by the SOA's
  Payout Annuity Table Team "as requested by the NAIC's Life Actuarial Task Force
  (LATF)", which "produced a new annuity valuation mortality table, including the
  projection scales and margins necessary to make the table suitable for standard
  valuation purposes for individual annuities". Downloadable items listed:
  - "Q&A Document for Implementation of 2012 Individual Annuity Reserve Table"
    (`/globalassets/assets/files/research/exp-study/2012-ind-annuity-reserving-q-a.docx`)
  - "Payout Annuity Report" (hosted at actuary.org — retrieved as [R14])
  - "Accompanying Tables" at **http://mort.soa.org/** (the SOA Mortality &
    Other Rate Tables repository — the machine-readable source for the 2012 IAM
    Period, 2012 IAM Basic and Scale G2 tables). [The mort.soa.org tables themselves
    were **not** downloaded — see "Gaps and caveats".]

### R17. IRS Private Letter Ruling 201515001 (RETRIEVED, NOT RELEVANT)
- URL fetched: https://www.irs.gov/pub/irs-wd/201515001.pdf
- Retrieved: YES (25 pages), but on reading, the ruling concerns a **variable
  deferred annuity with GLWB-style "Income Benefit Payments"** triggered by depletion
  of a contractual account value — **not** a deferred income annuity. Listed here so
  the fetch is on the record; **no facts from it are used below**.

---

## Extracted specifications

Every line below is tagged with the source it came from. Items marked
**[unverified]** are stated from general knowledge and were **not** confirmed
against any retrieved document.

### 1. Product definition and core mechanics

- Statutory definition: a DIA "guarantees a periodic payment for the life of the
  annuitant or a term certain and payments **begin 13 months or later from the issue
  date** if the contract holder and/or annuitant survives to a predetermined future
  age" [R9, VM-01].
- Regulatory product architecture: an individual **deferred paid-up non-variable
  annuity** with **no cash surrender values prior to the commencement of annuity
  payments**, single or flexible premiums, **specified income payments beginning on a
  specified income commencement date for each premium paid**, all funds in the
  **general account** [R13, Scope].
- Each premium purchases a **separate paid-up annuity**; "All income benefits, based
  on the specified income commencement date and specified income option associated
  with each premium paid, shall be **guaranteed**" [R13 § 3.H(1)]. Insurers combine
  the resulting slices into a single payment stream at the income start date
  [S1][S2][S3][S4].
- There is **no account value, no credited interest rate, no cash value, no loan**
  during deferral [S1 fn.1][S2 p.3, product highlights][R13 § 3.P]. The contract
  states **dollars of income**, not rates: "Since the premium and income benefit are
  fully defined in the contract, the **mortality table and interest rate used in the
  deferral period … do not need to be disclosed** in the contract or the Actuarial
  Memorandum" [R13 § 1.B(1)(a)].
- **Modelling consequence**: the DIA liability is a *deferred annuity-certain-and-life
  cash-flow schedule* keyed off (premium slice, purchase date, income start date,
  income option), not an account-value roll-forward. The state variables are the
  guaranteed income amount, the survival/decrement status of one or two lives, and
  (before income start) the cumulative premium for the return-of-premium death
  benefit. [derived from S1–S4, R13]

### 2. Premium structure

| Parameter | NYL GFI II [S1] | MassMutual RetireEase Choice [S2] | Guardian SecureFuture [S3] | Pacific Secure Income [S4] |
|---|---|---|---|---|
| Minimum initial premium | $10,000 | $10,000 | $10,000 | **$15,000** |
| Minimum subsequent premium | $100 | $500 | $100 (not for QLAC) | $500 |
| Maximum cumulative (without approval) | $2,000,000 | $1,500,000 | $1,000,000 | $2,000,000 |
| Minimum monthly income | not stated | $100 | not stated | not stated |
| Cut-off for additional premiums | 13 months before income start (implied by the 13-month rule on start-date changes) | **13 months** before annuity date | (13-month rule applies to start-date changes) | **13 months** before start date; 1035 exchanges **16 months** |

- Fidelity's cross-insurer table shows **$10,000 minimum for all five** of Guardian,
  MassMutual, NYL, USAA and Western & Southern [S6].
- MassMutual's cumulative limit aggregates "all deferred income annuity contracts
  issued by MassMutual and its subsidiaries that are owned by the same contract owner
  … or that have the same annuitant" [S2].
- Pacific Life restricts multiple purchase payments to the **lifetime** income options
  only; with Period Certain, all money must arrive with the application and within
  **60 days of issue (90 days in New York)** [S4].
- **Pricing of additional premiums** (the mechanic a model must implement): purchase
  rates are based on "the **attained age of the annuitant, the specified income
  commencement date and specified income option, and the company's then current
  annuity purchase rates**, subject to any guarantees provided in the contract"
  [R13 § 3.B(1)(b)]; the income purchased must be **not less than that in a new
  contract** of the same class, attained age and commencement date [R13 § 3.B(1)(c)].
  Guardian states this directly: "Each payment purchases a specific amount of
  guaranteed lifetime income, based on **annuity purchase rates that are in effect at
  the time each purchase payment is made**" [S3].
- **10-day free-look on each additional premium**: MassMutual [S2] and Guardian [S3]
  both grant a refund right within **10 calendar days of receiving the confirmation**;
  the Compact standard requires the confirmation to carry that option and to be sent
  **within 30 days** of receipt of the premium [R13 § 3.B(1)(d)].
- **QLAC 90-day rescission**: SECURE 2.0 § 202(a)(4) directed that the regulation not
  preclude "a provision under which an employee may **rescind the purchase of the
  contract within a period not exceeding 90 days from the date of purchase**"
  [R2]; the current regulation carries this as the sole carve-out from the
  no-commutation rule [R1 (q)(1)(iv)].

### 3. Issue ages

| Market | NYL [S1] | MassMutual [S2] | Guardian [S3] | Pacific Life [S4] |
|---|---|---|---|---|
| Minimum issue age | 0 (nonqualified) / 18 (qualified) / 20 (Roth) / **35 (QLAC)** | **22** (non-QLAC) / **41** (QLAC) | 0 (nonqual & Roth) / 18 (trad. IRA) / **31 (QLAC)** | **22** (all) |
| Max — nonqualified | 80 | 88 | 80 | **85** |
| Max — Roth IRA | 80 | 88 | 80 | 85 |
| Max — traditional/qualified | 73 | 69 *(pre-SECURE vintage)* | 68 *(pre-SECURE vintage)* | 71 |
| Max — **QLAC** | 80 | 83 | 82 | 82 |
| Max — joint annuitant | 80 (nonqual, both ≤80) / 80 (qual, spouse) | 88 (all markets) | 80 (75 for Life-Only) | spouse only |

- NYL adds a general rule: "Issue age can be **no later than 2 years before** the
  client's RMD age" [S1].
- Guardian adds an option-specific cap: maximum age for **Single Life Only without
  Guarantee Period is 75**; for **Joint Life Only**, both annuitants must be ≤75 [S3].
- MassMutual uses **age nearest birthday** ("if John is 74 years, six months, and one
  day old, his contract issue age will be **75**") [S2]. Prescribed VM-22 mortality is
  also age-nearest-birthday, with a conversion formula supplied for age-last-birthday
  companies [R9].
- Fidelity's cross-insurer table gives max issue ages (qualified / QLAC / nonqualified)
  of 73/82/80 Guardian, 71/83/88 MassMutual, 73/80/80 NYL, 71/83/83 USAA, 73/83/83
  Western & Southern [S6].

### 4. Deferral period and income start date

- **Minimum deferral** — three different conventions in the market:
  - **13 months** from contract issue: MassMutual [S2], Pacific Life [S4], and the
    VM-01 statutory definition [R9]. Fidelity lists Guardian and Western & Southern at
    "13 months" as well [S6].
  - **24 full months** from contract issue: NYL [S1] and Guardian's own fact sheet
    [S3] (Fidelity renders NYL and USAA as "2 years") [S6].
- **Maximum deferral**:
  - NYL: **40 years** for lifetime income; **20 years** period-certain-only [S1].
  - Guardian: earlier of **40 years** from issue or any annuitant reaching **age 85**;
    **5 years max** for Life Only options at issue ages 71–75 [S3].
  - MassMutual: **30 years** from issue [S2]; Pacific Life: **30 years** from issue
    [S4]. USAA 30 years, Western & Southern 40 years [S6].
- **Latest income start (non-QLAC)**:
  - **Age 85** — NYL nonqualified/Roth [S1]; Guardian and Western & Southern [S6];
    USAA [S6].
  - **Age 90** — MassMutual ("when any annuitant attains age 90") [S2] and Pacific
    Life (nonqualified and Roth) [S4].
  - Qualified (non-QLAC, non-Roth): by **April 1 of the year following** the year the
    owner attains the applicable RMD age — NYL states **73** (born before 1960) or
    **75** (born 1960 or later) [S1]; Pacific Life states **73** [S4]; MassMutual's
    2019 guide states **70½** [S2 — superseded].
- **Period certain durations**: NYL 5–30 years for Period-Certain-Only and 10–30 years
  for Life-with-Guarantee [S1]; MassMutual 10–30 years (10 years only for the
  convertible joint variants) [S2]; Guardian 5–30 years [S3]; Pacific Life up to 30
  years [S4]. Compact floor: "a stipulated period certain for a **minimum of five (5)
  years with a maximum deferral period of twenty (20) years**" [R13 § 3.H(3)(b)].

### 5. Income start date adjustment (accelerate / defer after issue)

This is the DIA's principal in-force optionality and the main thing a projection model
must handle beyond the base annuity.

| Feature | NYL [S1] | MassMutual [S2] | Guardian [S3] | Pacific Life [S4][S5] |
|---|---|---|---|---|
| Direction / magnitude | accelerate ≤5 yrs, defer ≤5 yrs | ±5 yrs (10-yr window) | accelerate 5 yrs, defer ≤5 yrs | ±5 yrs |
| Number of changes | one-time | **once only**, irrevocable | one-time; if deferred, a one-time option to accelerate back to no earlier than the original date | one-time |
| Floor on the new date | ≥13 months after the **latest investment** | ≥13 full months after the **last purchase payment** | ≥13 months after the **latest premium payment** | ≥13 months after the **most recent purchase payment**; ≤30 yrs from issue |
| Excluded options | **Life Only** | contracts where the DB has been triggered (except convertible joint); the No-Refund options outside Florida | **Single and Joint Life Only** | **Life Only, Joint Life Only, Joint and Survivor Life Only, Period Certain** |
| Other locks | income option and **day of month** cannot change | option, day of month and **payment frequency** cannot change; new payment must be ≥$100 | annuity option cannot change | — |
| State variations | — | **Florida**: acceleration allowed for *all* options to as early as 13 months after issue | — | **not available in Connecticut or New York** |
| Direction of income impact | recalculated | recalculated | recalculated | advance → **decrease**; defer → **increase** |
| Recalculation basis | **Moody's Seasoned Baa Corporate Bond Yield (DBAA)**, **A2000 mortality tables**, and an **interest rate change adjustment** | originally scheduled payment, new annuity date, **Moody's Seasoned Baa Corporate Bond Yield** at request date, **Annuity 2012 Mortality Table**, and an **interest rate change adjustment set forth in the contract** | not disclosed | not disclosed |

- Western & Southern is the outlier: **up to two changes** to the income start date
  [S6].
- Regulatory frame: if a change right is granted, the contract must disclose the
  alternatives, **any limitation on when a change can be made**, **how often**, and
  **any explicit charge**; and must **either** state the mortality and interest
  assumption used for actuarial equivalence **or** contain a **table of alternative
  income benefits** by alternative date/age and option [R13 §§ 3.M, 3.H(1)].
- **Modelling note**: the NYL and MassMutual disclosures give the actual repricing
  recipe — an actuarial-equivalence recalculation on (Moody's Baa yield at the change
  date, a stated annuity mortality table, plus a contractual interest-rate-change
  adjustment). This is an in-force option whose value is driven by the **spread
  between the pricing rate locked at issue and the Baa yield at exercise**, which is
  why the option is one-time and why Life Only (where anti-selection on health is
  strongest) is excluded [S1][S2][S3][S4].

### 6. Death benefit during the DEFERRAL phase — the key design fork

- **Regulatory constraint on the formula**: if a deferral-phase death benefit is
  provided, "the method of calculation … **shall be limited to one of the following
  methodologies**: (a) a **percentage of premiums paid**; (b) a **percentage of
  premiums paid plus interest**; (c) a **flat dollar amount**; or (d) any combination"
  [R13 § 3.I(1)]. It must apply to **both the initial premium and any additional
  supplemental premiums** [R13 § 3.I(2)].
- **In practice the market uses (a) at 100%** — a plain **return of premium** with no
  interest:
  - NYL: "all annuity options, **except Single Life and Joint Life Only**, include a
    **return of the premium payments**" if the owner dies [S1].
  - MassMutual: "the death benefit prior to the annuity date is a **return of purchase
    payments** for most options (except for the Single Life — No Death Benefit annuity
    option)"; the beneficiary "receives a death benefit equal to the **purchase
    payments applied to the contract**" [S2].
  - Guardian: "all annuity options, **except Single and Joint Life Only**, include a
    **return of the premium payment(s)**" [S3].
  - Pacific Life: "a **return of purchase payments** death benefit applies", except for
    the Life Only / Joint Life Only / Joint and Survivor Life Only options [S4]. Paid
    as a **lump sum** [S4].
- **The "no death benefit at all" fork** is a real, separately-priced option:
  - Pure form: MassMutual's **Single Life — No Death Benefit** option provides no
    death benefit **either before or after** the annuity date; it **requires a deferral
    period of 10 years or longer**; the **annuity date cannot be changed**; and it is
    restricted by state (the guide names Connecticut and Florida in one place and
    Connecticut and New York in another) [S2].
  - Implicit form: the **Life Only** options at NYL, Guardian and Pacific Life carry no
    deferral-phase ROP — "Contracts in which a **Life Only** payout option is selected
    do **not** provide a death benefit either prior to or after the chosen Income Start
    Date" [S1]; same at Guardian [S3] and Pacific Life [S4].
  - Intermediate form (Pacific Life only among sources retrieved): **"Life Only with
    100% Return of Purchase Payments Death Benefit"** — ROP in the deferral phase, pure
    life annuity thereafter [S4].
- **Disclosure obligations flowing from the fork**: a contract with no deferral-phase
  death benefit must carry on the **cover page**, in prominent print, "The contract
  does not provide access to funds prior to the income commencement date. **No death
  benefit is available to a beneficiary if the annuitant dies prior to the income
  commencement date.**"; one with a death benefit must say "The contract does not
  provide access to funds prior to the income commencement date **other than payment
  of the death benefit**." [R13 §§ 2.A(8)–(9)]. Model #805 § 9 is the underlying
  requirement [R10].
- **Modelling consequence**: this fork changes the liability from
  `PV(deferred annuity) ` to `PV(deferred annuity) + PV(ROP on death in deferral)`, and
  it changes the *sign of mortality risk during deferral* — with ROP, deferral-phase
  mortality is nearly neutral (premium is returned); without it, deferral-phase deaths
  are pure profit to the insurer and the pricing mortality assumption during deferral
  materially raises the income [derived from S1–S4, R13].
- Continuation election: where the surviving spouse is joint annuitant and sole primary
  beneficiary, the contract may **continue** rather than pay the death benefit
  [S1][S2][S4]. MassMutual details the choice: elect the death benefit, or continue the
  contract (nonconvertible), or convert to the corresponding single life option
  (convertible) — with "**If the contract is continued, additional purchase payments
  will not be allowed**" for the nonconvertible spousal continuation [S2].

### 7. Death benefit AFTER income start

- Governed entirely by the elected income option [S1][S2][S3][S4]; the option is set at
  issue and (universally in the sources) **cannot be changed** [S1][S2][S4].
- **Cash Refund**: on the death of the last surviving annuitant, if total annuity
  payments made are less than purchase payments made, the beneficiary receives the
  **difference in a lump sum**; otherwise the contract terminates [S2]. NYL phrases the
  same benefit as "a lump-sum payment of the difference between the investment amount
  and total income payments paid" [S1].
- **Installment Refund**: payments **continue in the same amount and at the same
  frequency until they equal the purchase payments**; the beneficiary may instead elect
  the **present value of the remaining payments in a lump sum** [S2].
- **Period Certain / Life with Guarantee Period**: payments continue to the beneficiary
  in the same amount and frequency **to the end of the certain period**; the
  beneficiary may elect the **present value of remaining payments** instead [S2][S1].
  Guardian offers the same election, phrased as "a lower, **present-day-value lump-sum
  payment**" [S3].
- **Life Only**: no death benefit; the contract simply ends [S1][S3][S4].
- Joint interaction with a guarantee period: "if the first annuitant dies during the
  guaranteed payment period, the payments to the second annuitant will **not be reduced
  until the end of that period**" [S1]; Guardian states the same [S3].
- Compact framing: any refund-style guarantee is treated as **period certain income**
  for standards purposes — "For policies that offer a return of premium death benefit
  (e.g., cash refund or installment refund options), the income benefit payments made
  prior to the death benefit shall be considered period certain income" [R13,
  definitions].

### 8. Single vs joint life

- Joint annuitants: **maximum two annuitants**; the annuitant(s) **cannot be changed
  once the contract is issued** [S2].
- Spouse requirement: joint annuitant must be a spouse for qualified contracts at NYL
  [S1]; must be a spouse for all Joint Life options at Pacific Life [S4]; must be the
  spouse and sole primary beneficiary for convertible joint options at MassMutual [S2];
  must be the spouse of the annuitant at contract issue for a **QLAC** at MassMutual
  [S2].
- **Survivor continuance percentages**:
  - NYL: **100%, 66⅔%, or 50%** for Life with Guaranteed Period or Life Only; **100%
    only** with Cash Refund [S1].
  - MassMutual: **½, ⅔, ¾** for the "Reduction at Death of Either Annuitant" variants;
    also offers ¾, ⅔, ½ survivor benefits for non-spouse joint annuitants more than 10
    years younger, on a sliding scale, with requests below ½ subject to further
    approval [S2].
  - Pacific Life: **50%, 67%, 75%** [S4].
- **Reduction trigger** — two distinct designs, both offered by Pacific Life:
  - "**Joint Life**" options reduce on the death of **either** annuitant [S4];
    MassMutual's "Reduction at Death of Either Annuitant" is the same design [S2].
  - "**Joint and Survivor Life**" options reduce on the death of the **primary**
    annuitant only [S4]. NYL offers both: "upon the death of a **specified annuitant**
    or upon the death of **either one** of the annuitants" [S1].
- **Convertible vs non-convertible joint options** (MassMutual, the most explicit
  treatment; directly relevant to pricing/reserving):
  - Non-convertible options "guarantee income based on a **single payout assumption
    that both annuitants will be alive on the annuity date**" [S2].
  - Convertible options guarantee **two** payout amounts: the joint life payout if both
    are alive on the annuity date, and the corresponding **single life payout** for
    each annuitant if only one is alive and the contract converts [S2].
  - "In general, if both annuitants are alive on the annuity date, the joint life
    payout will be **lower** with a convertible joint life annuity option than … with a
    nonconvertible" [S2] — i.e., the conversion right is paid for out of the joint
    payout.
  - Conversion is available **only if an annuitant dies during the deferral period**
    [S2]. If a non-owner annuitant dies, the option "automatically converts to the
    corresponding single life annuity option for the owner" [S2].
- RMD interaction: for a traditional or SEP IRA, "joint and survivor annuity options
  with **no reduction in benefit to the survivor** are only available … if the joint
  annuitant is either the spouse **or less than 10 years younger** than the annuitant
  on the annuity date" [S2] — the MDIB rule surfacing as a product restriction.

### 9. Cost-of-living / annual increase options

| Insurer | Available increases | Elected at | Changeable? | QLAC? |
|---|---|---|---|---|
| NYL "Annual Increase Option" [S1] | **1%, 2%, 3%** | purchase | no | **not available for QLAC** |
| MassMutual "Inflation Protector" [S2] | **1%, 2%, 3%, 4%** | issue | "cannot be canceled or changed" | limited/unavailable on qualified due to RMD rules |
| Guardian "Cost-of-Living Adjustment" [S3] | percentage set at issue (**1%–5%** per [S6]) | contract issue | no | **not available for QLAC** |
| Pacific Life "Inflation Protection Option" [S4] | **2%, 3%, 4%** | purchase | no | **not available with QLAC or traditional IRA** |
| USAA [S6] | 1%–3% | — | — | — |
| Western & Southern [S6] | 1%–5% | — | — | — |

- Increase applies **annually on the anniversary of the annuity date / income start
  date** [S2][S3][S4] — i.e., a simple compound escalation of the payment, not an
  index-linked adjustment.
- NYL additionally requires the policyowner to be **at least age 59½ at the time of the
  first income payment** to elect the Annual Increase Option [S1].
- Universal trade-off statement: "Income payments for the same premium amount will
  initially be **smaller** than policies without this feature, and will increase each
  year at the percentage chosen" [S1]; MassMutual and Pacific Life say the same
  [S2][S4].
- **QLAC compatibility is a regulatory, not marketing, matter**: a QLAC "does not fail
  to satisfy [the not-variable/not-indexed requirement] merely because it provides for
  a **cost-of-living adjustment as described in paragraph (o)(2)**" [R1 (q)(4)(iv)(B)].
  Yet NYL, Guardian and Pacific Life all **exclude** COLA from their QLAC offering
  [S1][S3][S4] and MassMutual limits it on qualified contracts [S2]. → The market is
  more restrictive than the regulation requires.

### 10. Liquidity features (the DIA's substitute for surrender value)

There is **no surrender charge schedule, no free-withdrawal corridor and no market
value adjustment** in the ordinary sense, because there is nothing to surrender
[S1][S2][S4][R13]. The liquidity features that exist are:

- **Payment acceleration** (take future scheduled payments early, then go without):
  - NYL: next payment **plus five** = **six months** in one sum; then no payments for
    five months. Age **59½**+, **two** times over the life of the policy,
    **nonqualified only** [S1].
  - MassMutual: **three or six** payments in a lump sum; monthly frequency and
    **nonqualified only**; **maximum five** times; must receive at least one regular
    payment between uses; "**not a liquidity feature**" [S2].
  - Guardian: up to **five** scheduled payments accelerated with the regular payment
    (six months total); requires **Life with Guarantee Period or Life with Cash Refund**
    with **at least six months remaining** in the guarantee/refund period; monthly
    frequency; nonqualified and Roth IRA; actual age **59½**+; **once** over the life
    of the contract [S3].
  - Pacific Life: **three or six** times the normal monthly payment; age 59½+; all
    income options; **maximum two** times; for qualified contracts the acceleration
    period must be **in the same tax year**; **not available with a QLAC** [S4].
- **Commutation / withdrawal of the present value of remaining guaranteed payments**:
  - Pacific Life is the only source with a true commutation feature: **up to 100% of
    the present value of remaining guaranteed income payments**, nonqualified only, age
    59½+, only on Period Certain / Life with Period Certain / Life with Cash Refund /
    Life with Installment Refund (and their Joint versions), **no limit on the number
    of withdrawals**, **not available in Missouri**, and "**an interest-rate adjustment
    charge will apply**" [S4][S5]. Distinctively, "except for the Period Certain
    option, if you are still living at the end of the period when your guaranteed
    income payments would have stopped, **Pacific Life will resume income payments
    until your death**" — i.e., the life-contingent tail is preserved [S4].
  - Six-month interlocks: acceleration ⇄ withdrawal ⇄ start-date-adjustment each impose
    a six-month waiting period on the others [S4].
- **The commuted-value rules a model should implement** [R13 § 3.F]:
  - Payable in a **lump sum only**; non-commuted benefits **unaffected**.
  - Must be an **actuarial present value** (drafting note).
  - "The **interest rate used to calculate commuted values can be adjusted for changes
    in interest rates** … between the issue date and the commutation date", with the
    stated intent "to **reduce interest risk in the event of rising interest rate after
    issue**" — the DIA analogue of an MVA.
  - Contractual disclosure if rates/table are in the contract at issue: "The commuted
    value of any remaining annuity payments is always less than the sum of those
    benefit payments and **the higher the interest rate the lower the commuted
    value**."
  - Otherwise a **replacement ratio = (actual commuted value to be paid) / (commuted
    value on current pricing assumptions for the same type of income and class)** must
    be defined in the contract and disclosed on request.
  - Payment within **15 days**; the company may reserve the right to defer commutation
    payment **up to six months** (with domiciliary-regulator approval), but **may not**
    defer income payments or death benefits at all [R13 §§ 3.F(4)(d), 3.J, 1.A(8)].
- **QLAC bar**: "After the required beginning date, the contract does **not make
  available any commutation benefit, cash surrender right, or other similar feature**"
  other than the ≤90-day rescission [R1 (q)(1)(iv)] — which is why Pacific Life's
  commutation, payment acceleration and inflation protection are all off for QLACs
  [S4].
- **Loans are prohibited outright** [R13 § 3.P].

### 11. Nonforfeiture treatment — resolving the brief's question

The brief asked whether the Standard Nonforfeiture Law for Individual Deferred
Annuities (Model #805) applies to DIAs given that they have no cash value. The answer
from the retrieved primary law is:

1. **Model #805 does apply.** Its Section 2 exclusion list covers "immediate annuity"
   and "**any deferred annuity contract after annuity payments have commenced**" — but
   a DIA **before** the income commencement date is precisely a deferred annuity
   contract before payments commence, and is in none of the listed exclusions [R10].
2. **The cash-surrender requirement is conditional and therefore not triggered.**
   Section 3.A(2) requires a cash surrender benefit only "**If a contract provides for
   a lump sum settlement at maturity, or at any other time**" [R10]. A DIA that never
   offers a lump sum never triggers it.
3. **The requirement that is triggered is the paid-up annuity benefit, and a DIA
   satisfies it by construction.** Section 3.A(1) requires a **paid-up annuity benefit**
   on cessation of considerations [R10] — and every DIA premium has *already*
   purchased a fully guaranteed paid-up annuity [R13 § 3.H(1)]. Section 7 governs
   valuation "**for contracts that do not provide cash surrender benefits**", requiring
   the present value of the paid-up annuity to be at least the present value of the
   portion of the maturity value arising from considerations already paid, discounted
   at the contract's stated interest rate, and (for contracts with **no** deferral-phase
   death benefit) on the contract's stated interest rate **and mortality table** [R10].
4. **Section 9 forces the disclosure**: a contract with no cash surrender benefit, or
   with death benefits below the minimum nonforfeiture amount before annuity payments
   commence, "shall include a statement in a prominent place in the contract that such
   benefits are not provided" [R10] — realised as the Compact's mandated cover-page
   language [R13 §§ 2.A(8)–(9)].
5. **For Compact filings the demonstration itself is replaced.** The IIPRC standard
   accepts, "**in lieu of a nonforfeiture demonstration**", a certification "that the
   income benefit provided under this contract is **greater than that guaranteed at
   issue for the same premium** under any non-variable deferred annuity contract offered
   by the company that provides cash surrender values during the deferral period or on
   the income commencement date" [R13 § 1.B(1)(g)]. This is a **comparative adequacy
   test against the company's own cash-value product**, not a minimum-value formula.
- Related Model #805 numbers captured: the minimum nonforfeiture amount accumulates net
  considerations at the Subsection B rates less prior withdrawals and an **annual
  contract charge of $50** [R10 § 4.A(1)]; a contract may be terminated for a paid-up
  benefit **under $20 monthly** after **two years** without considerations
  [R10 § 3.B]; the deemed **maturity date** for Sections 6/7 is the later of the
  anniversary following age **70** and the **tenth** contract anniversary
  [R10 § 8].

### 12. QLAC specifications

- **Premium limit**: **$200,000** as enacted, indexed [R1 (q)(2)(ii)][R2 § 202(a)(2)(A)];
  **$210,000 for 2026** (and unchanged from 2025) [R3], independently confirmed by
  Pacific Life: "The maximum … aggregate purchase payment limit in **2026 is $210,000**
  (indexed in future years for inflation)" [S4].
- **Indexing mechanics**: adjusted like section 415(d) limits, with **base period the
  calendar quarter beginning July 1, 2022**, and increments **rounded to the next
  lowest multiple of $10,000** [R1 (q)(4)(ii)(A)][R2 § 202(a)(2)(B)].
- **The 25%-of-account-balance limit was removed.** SECURE 2.0 § 202(a)(1) directed
  Treasury to "**eliminate the requirement that premiums … be limited to 25 percent of
  an individual's account balance**" [R2]; the current codified text at
  § 1.401(a)(9)-6(q)(2) contains **only a dollar limitation and no percentage test**
  [R1]. Effective **for contracts purchased or received in an exchange on or after the
  date of enactment** of SECURE 2.0 [R2 § 202(c)(1)(A)].
- **Aggregation**: the dollar limit is reduced by premiums previously paid to the
  contract **and by premiums paid to any other contract intended to be a QLAC** under
  the plan or any other 401(a), 403(a), 403(b), 408, or governmental 457(b) arrangement
  [R1 (q)(2)(ii)(B)]. Trustees/issuers may rely on the owner's **written
  representation** as to premiums not paid under that IRA [R5 (h)(2)][R1 (q)(4)(i)(A)].
- **Latest income start**: "no later than the **first day of the month next following
  the 85th anniversary of the employee's birth**" [R1 (q)(1)(ii)]. Every insurer
  restates this: NYL [S1], MassMutual ("the first day of the month following the
  contract owner's 85th birthday") [S2], Guardian [S3], Pacific Life ("no later than the
  first day of the following month after attaining age 85") [S4]. The maximum age may be
  adjusted for mortality by published Commissioner guidance [R1 (q)(4)(ii)(B)].
- **Earliest income start** is a *product* rule, not a QLAC rule: NYL requires income to
  begin **after** April 1 of the year following the year the owner turns 73/75 [S1];
  MassMutual required April 2 of the year after age 70½ [S2 — pre-SECURE vintage], with
  a footnote explaining the rationale: "Choosing an earlier annuity date would result in
  a **more restrictive QLAC without providing any of the tax advantages** that a QLAC
  offers" [S2].
- **Permitted death benefit forms** — the exhaustive list [R1 (q)(3)]:
  - Surviving spouse sole beneficiary → a **life annuity** to the spouse not exceeding
    **100%** of the employee's payment, commencing no later than when the employee's
    annuity would have commenced [R1 (q)(3)(i)].
  - Non-spouse (or spouse not sole) beneficiary → a **life annuity** not exceeding the
    **applicable percentage** of the employee's payment, commencing by the last day of
    the calendar year following the year of death [R1 (q)(3)(ii)].
  - Applicable percentage = MDIB table percentage if the contract has **no
    pre-annuity-starting-date non-spousal death benefit**; Table 6 percentage if the
    contract requires an **irrevocably set non-spousal beneficiary**; and **0** if the
    contract provides a **return of premium** [R1 (q)(3)(iii)(A)–(C)].
  - **Return of premium** in lieu of a life annuity, "**up to the amount by which the
    premium payments made … exceed the payments already made**", payable after the
    employee's death (and optionally after the death of both employee and spouse); must
    be paid **by the end of the calendar year following the year of death**; treated as
    an **RMD for the year paid, not eligible for rollover**, if death is after the
    required beginning date [R1 (q)(3)(v)].
  - Table 6 applicable percentages by adjusted age difference are reproduced verbatim
    in [R1] above (≤2 yrs → 100% … 25+ yrs → 20%).
- **Market implementation of those forms**: MassMutual permits only **Single Life — No
  Refund, Single Life — Cash Refund, Single Life — No Death Benefit, and Joint and
  Survivor Life — Cash Refund** on a QLAC; **Installment Refund and Period Certain
  guarantees are not available with a QLAC** [S2]. Pacific Life likewise excludes Period
  Certain and Installment Refund from QLACs [S4]. Guardian excludes guarantee periods
  and subsequent premiums from QLACs [S3].
- **Exclusion from RMD calculations**: "**The account balance does not include the value
  of any qualifying longevity annuity contract (QLAC)**, defined in
  § 1.401(a)(9)-6(q), that is held under the plan" [R4 § 1.401(a)(9)-5(b)(4)]; this rule
  "**applies to an IRA**" subject to the § 1.408-8(h) modifications [R5]. MassMutual
  states the consumer version: "The assets in a QLAC are **not included in RMD
  calculations until they are received as income**" [S2].
- **Roth carve-out**: § 1.401(a)(9)-5(b)(4) **does not apply to a Roth IRA**; a contract
  purchased under a Roth IRA is not treated as intended to be a QLAC for the dollar
  limit, and a QLAC rolled over or converted to a Roth IRA ceases to be so treated
  [R5 (h)(4)][R1 (q)(4)(iii)(B)].
- **Excess-premium correction**: the contract stops being a QLAC on the date the excess
  premium is paid, unless the excess is returned to the non-QLAC portion of the account
  **by the end of the calendar year following** the year it was paid, in which case the
  contract is treated as never having exceeded the limit; returning it is **not** a
  prohibited commutation [R1 (q)(4)(i)(B)]. MassMutual's guide describes the same
  correction window and the consequences of missing it — loss of QLAC status **as of the
  date the excess payment was made**, potential additional RMDs for prior years, and
  **no ability to restore QLAC status** [S2].
- **Structural failure** (any reason other than excess premium) voids QLAC status
  **retroactively to the date of purchase** [R1 (q)(4)(iii)(A)].
- **Prohibited features**: no commutation benefit, cash surrender right or similar
  feature after the required beginning date (other than the ≤90-day rescission)
  [R1 (q)(1)(iv)]; the contract must **not be variable under section 817, indexed, or
  similar** [R1 (q)(1)(vii)].
- **Permitted features**: **participating** contracts paying dividends, and contracts
  with a **cost-of-living adjustment** under paragraph (o)(2), do not violate
  (q)(1)(vii) [R1 (q)(4)(iv)].
- **Contract must state its intent**: the contract, rider or endorsement must state it
  is **intended to be a QLAC** when issued [R1 (q)(1)(vi)]; for group contracts, a
  certificate so stating suffices [R1 (q)(4)(v)].
- **Divorce**: survivor benefits to a former spouse are preserved where a QDRO or
  divorce/separation instrument entitles the former spouse to the survivor benefits,
  treats them as a surviving spouse, or does not modify their treatment as beneficiary
  or measuring life [R1 (q)(3)(vii)][R2 § 202(a)(3)] — **effective retroactively to
  contracts purchased on or after July 2, 2014** [R2 § 202(c)(1)(B)]. MassMutual's
  pre-SECURE-2.0 guide shows the old, harsher treatment (only a return of purchase
  payments on divorce before the annuity date, no continued payments to a non-spouse
  beneficiary) [S2] — a concrete illustration of what § 202(a)(3) changed.
- **QLAC issue-age and market implementation**: minimum issue ages 31–41 across insurers
  (Guardian 31, NYL 35, MassMutual 41) and maximum 80–83 (NYL 80, Pacific Life 82,
  Guardian 82, MassMutual 83, USAA 83, Western & Southern 83) [S1][S2][S3][S4][S6].
- **QLAC contract types offered**: MassMutual issues both **QLAC IRA** and **Custodial
  QLAC IRA**; for the custodial form the **payee and beneficiary must be the custodian**
  and the custodial agreement must state that the beneficiary is the spouse; **spousal
  continuances are not allowed** on either form [S2].

### 13. Taxation (nonqualified contracts)

- **Exclusion ratio**: the excludable portion of each annuity payment is
  `investment in the contract / expected return under the contract`, capped at the
  **unrecovered investment**; on death with an unrecovered investment remaining, that
  amount is a **deduction for the annuitant's last taxable year** [R8 § 72(b)].
- **Investment in the contract** = aggregate premiums paid minus aggregate amounts
  previously received to the extent excludable [R8 § 72(c)]. For a flexible-premium DIA,
  this is the sum of all purchase payments [derived from R8 with S2/S3].
- **Expected return**, where life-contingent, is computed by reference to **actuarial
  tables prescribed by the Secretary** [R8 § 72(c)].
- **10% penalty** on premature distributions with exceptions for age 59½, death,
  disability and a **series of substantially equal periodic payments** [R8 § 72(q)] —
  this is why every acceleration/withdrawal feature is gated at 59½
  [S1][S3][S4]. NYL warns that exercising Payment Acceleration within five years of the
  first annuity payment, on a policy purchased before 59½, can trigger the 10% penalty
  **retroactively, plus interest**, on payments received before 59½ [S1].
- **§ 72(s)** death-distribution rules: after the annuity starting date, the remaining
  interest must be distributed "at least as rapidly as under the method of distributions
  being used as of the date of death"; before it, within **5 years** [R8].
- MassMutual flags residual uncertainty on the acceleration feature: "Because deferred
  income annuities are relatively new to the market, **the IRS has not yet ruled on this
  tax treatment**" [S2].
- A 3.8% net investment income tax may apply to nonqualified contracts, and a 10%
  additional federal income tax may apply to annuity payments/withdrawals before 59½
  [S4].

### 14. Valuation and reserving basis (statutory)

- A DIA sits in the **VM-22 "Payout Annuity Reserving Category"** [R9], with VM-22 PBR
  effective for **valuation dates on or after January 1, 2026** and a **three-year
  transition** during which VM-A/VM-C/VM-M/VM-V may still be used for newly issued
  business [R9].
- Aggregate reserve = **SR + DR** (for contracts passing the Single Scenario Test) +
  formulaic reserves for excluded contracts; the **Additional Standard Projection
  Amount** is a **VM-31 disclosure** item, not an additive reserve floor by default
  [R9].
- Prescribed standard-projection assumptions that are directly implementable:
  - **Mortality**: `q_x^(2012+n) = q_x^(2012) · (1 − G2_x)^n · F_x`, with `q_x` from the
    **2012 IAM Basic** table, `G2_x` from **Scale G2**, and `F_x` from **Table 6.8**
    (Payout Annuity Reserving Category), age nearest birthday [R9]. Female Fx runs
    125% at ages ≤57 declining to ~93% at 67 then rising to 108% by 77–79; male Fx runs
    100% at ≤57, dipping to ~95% at 62–66 then rising to 117% by 79 [R9].
  - **Lapse**: not applicable — "For contracts in which there is **no account value or
    surrender benefit**, such as some contracts within the Payout Annuity Reserving
    Category …, this section is **not applicable**" [R9].
  - **Annuitization**: "The annuitization rate for contracts shall be **0% at all
    projection intervals**" [R9].
  - **Maintenance expense**: **$50** per individual contract per year for the Payout
    Annuity Reserving Category, escalated by `[1.025]^(valuation year − 2015)` in the
    first projection year and **2.5% p.a.** thereafter; plus **7 bp** applied — for
    contracts without an account value — to a present value basis [R9].
- Formulaic (non-PBR) route: **VM-V Section 1** covers "**Deferred income annuity
  contracts issued after Dec. 31, 2017**" for contracts not passing the Stochastic
  Exclusion Test [R9]. The maximum valuation interest rate is a function of the
  **Valuation Rate Bucket** (A–D by reference period and initial age — a typical DIA at
  issue age <70 falls in **Bucket D**), the **Premium Determination Date** ("date
  consideration is determined and committed to by contract holder"), and jumbo vs
  non-jumbo status; rates are published **daily** (jumbo) and **quarterly** (non-jumbo)
  by the NAIC [R9]. Underlying spread/default calculations use a prescribed portfolio of
  **5% Treasuries / 15% Aa / 40% A / 40% Baa** [R9].
- The **2012 IAR generational table** (for formulaic CARVM) is
  `q_x^(2012+n) = q_x^(2012) · (1 − G2_x)^n`, rounded to **three decimal places per
  1,000**, with rounding applied **from the 2012 period rate each time** (never chained
  off a previously rounded rate) [R9]. The **2012 IAM Period Table** = 2012 IAM Basic
  Table + LATF margin of **10% for ages ≤100**, grading down 1% per year thereafter
  until the ultimate mortality cap of **0.40000** [R14].
- Contract-level repricing on an income-start-date change is disclosed as using the
  **Annuity 2012 Mortality Table** [S2] or the **A2000 mortality tables** [S1] — i.e.,
  the *pricing/adjustment* basis is a published annuity table, distinct from the
  statutory valuation basis.

### 15. Charges

- There are **no explicit product charges** on a DIA in any source retrieved: MassMutual
  states plainly "There are **no fees** and no market performance to worry about" [S2],
  and neither NYL [S1], Guardian [S3] nor Pacific Life [S4][S5] discloses an M&E charge,
  administrative charge, contract fee, rider charge or surrender charge. Pricing margins
  are embedded in the annuity purchase rate [derived from S1–S4 with R13 § 1.B(1)(a)].
- The only charges the standards contemplate are: any **specific charge for the right to
  elect an alternative income commencement date or income option** [R13 §§ 1.B(1)(d),
  3.M(2)(c), 3.H(1)] and any **charges used in determination of the death benefit**,
  which must be disclosed on the specifications page [R13 § 2.B(2)].
- The only quantified "charge" found is Pacific Life's **interest-rate adjustment
  charge** on withdrawals of the present value of remaining guaranteed payments — named
  but not formulated in the retrieved documents [S4].
- Misstatement-of-age/sex adjustments carry interest "**at a rate specified in the
  contract but not exceeding 6%**" [R13 § 3.R(2)].

### 16. Payment frequency and administrative items

- Frequencies offered: **monthly, quarterly, semiannually, annually** at all four
  insurers [S1][S2][S3][S4].
- Frequency is **fixed at issue and cannot be changed** at NYL [S1] and MassMutual (it
  cannot be changed even on an annuity-date adjustment) [S2]; Guardian states frequency
  **can be changed at any time** [S3].
- MassMutual: annuity date "can fall on **any date except the 29th, 30th, or 31st**"; if
  it falls on a non-business day the payment processes on the next business day [S2].
  The Compact requires the date to be between the **1st and 28th** in effect via the
  specifications page [S2 restates this as a contract rule].
- Payees: up to **10** per contract at MassMutual, changeable at any time in writing,
  allocations totalling 100% [S2].
- **Evidence of survival**: the form may require proof the annuitant is living on the
  income commencement date or any income payment date [R13 § 3.L].
- **Incontestability**: two years from issue, with age and sex **not** contestable
  grounds [R13 § 3.N].
- The company **may not reserve any right to defer** income payments or death benefits
  [R13 § 3.J(1)].

---

## Variations across insurers

1. **Minimum deferral period: 13 months vs 24 months.** MassMutual [S2] and Pacific Life
   [S4] use **13 months**, matching the VM-01 statutory floor [R9] and the Florida
   annuitization rule [S2]. NYL [S1] and Guardian [S3] impose **24 full months**. The
   13-month convention is the regulatory minimum and is the more common design; the
   24-month version buys the insurer a longer guaranteed lock-in. **A model should
   parameterise this, defaulting to 13 months.**

2. **Maximum deferral: 30 vs 40 years.** MassMutual, Pacific Life and USAA cap at
   **30 years**; NYL, Guardian and Western & Southern at **40 years**
   [S1][S2][S3][S4][S6]. In practice the binding constraint is usually the **maximum
   income-start age** (85 or 90), not the year cap.

3. **Maximum income-start age: 85 vs 90 (nonqualified).** NYL, Guardian, USAA and
   Western & Southern stop at **85**; MassMutual and Pacific Life allow **90**
   [S1][S2][S3][S4][S6]. For QLACs the ceiling is uniformly **85** because the
   regulation fixes it [R1].

4. **Deferral-phase death benefit — the central design fork.** All four insurers default
   to a **100% return of premium** with no interest [S1][S2][S3][S4], consistent with the
   Compact's permitted method (a) [R13 § 3.I]. The variation is in how the
   *no-death-benefit* option is packaged:
   - **Implicit** (NYL, Guardian, Pacific Life): choosing **Life Only** silently removes
     the ROP [S1][S3][S4].
   - **Explicit and separately conditioned** (MassMutual): a distinct **Single Life —
     No Death Benefit** option requiring a **10+ year deferral**, with the annuity date
     locked and state restrictions [S2].
   - **Unbundled** (Pacific Life alone): **"Life Only with 100% Return of Purchase
     Payments Death Benefit"** separates the deferral-phase ROP from the post-income
     refund guarantee [S4]. This is the cleanest design for modelling because it makes
     the two mortality exposures independent parameters.
   No source offered a "percentage of premiums **plus interest**" deferral death benefit,
   even though the Compact permits it [R13 § 3.I(1)(b)].

5. **Income start date adjustment: uniform ±5 years, one time — with two exceptions.**
   All four insurers offer ±5 years, once [S1][S2][S3][S4]. Guardian adds a
   **one-time right to accelerate back** after a deferral [S3]; **Western & Southern
   allows two changes** [S6]. Florida law forces MassMutual to allow acceleration on
   *all* options to as early as 13 months [S2]. Pacific Life cannot offer the feature at
   all in **Connecticut or New York** [S4]. Only NYL and MassMutual disclose the
   **repricing basis** (Moody's Baa + a stated annuity mortality table + a contractual
   interest-rate-change adjustment) [S1][S2].

6. **COLA range: 1%–5%.** Narrowest is NYL at **1–3%** [S1]; MassMutual **1–4%** [S2];
   Guardian and Western & Southern **1–5%** [S6]; Pacific Life offers **2%, 3%, 4%**
   only [S4]. All are **fixed simple-compound escalators elected at issue and
   irrevocable**; none is CPI-linked in the sources retrieved. All four insurers
   restrict or exclude COLA on QLACs even though the regulation permits it
   [S1][S2][S3][S4] vs [R1 (q)(4)(iv)(B)].

7. **Post-income liquidity: acceleration everywhere, commutation only at Pacific Life.**
   Payment acceleration exists at all four, but with materially different limits — NYL
   **2 uses / 6 months** [S1]; MassMutual **5 uses / 3 or 6 months** [S2]; Guardian
   **1 use / up to 5 payments, and only with a guarantee or cash refund period with ≥6
   months left** [S3]; Pacific Life **2 uses / 3 or 6 months** [S4]. Only **Pacific Life**
   offers true commutation — up to **100% of the present value** of remaining guaranteed
   payments, unlimited in number, with an **interest-rate adjustment charge**, and with
   the life-contingent tail preserved [S4][S5]. This is the single largest liability-
   modelling difference across the four products.

8. **Joint-life reduction trigger and pricing convention.** Two designs coexist:
   reduction on the death of **either** annuitant vs on the death of the **primary**
   annuitant — Pacific Life offers both as separate option families [S4], NYL offers
   both as a choice [S1], MassMutual offers "Reduction at Death of Either Annuitant" as
   a named variant [S2]. Separately, MassMutual is the only source that exposes the
   **convertible vs non-convertible** distinction and states its pricing consequence
   (convertible joint payouts are lower because they also guarantee a single-life payout
   if one annuitant dies during deferral) [S2] — this is the most model-relevant pricing
   subtlety found.

9. **Minimum premium.** Four of five products cluster at **$10,000**
   [S1][S2][S3][S6]; **Pacific Life alone requires $15,000** [S4]. Minimum subsequent
   premiums split $100 (NYL, Guardian) vs $500 (MassMutual, Pacific Life)
   [S1][S2][S3][S4].

10. **Which design is representative.** For a reference implementation, the
    **MassMutual RetireEase Choice / Guardian SecureFuture archetype** is the best
    representative base case, and **Pacific Secure Income** the best "extended" case:
    - Base case: **flexible-premium DIA**, minimum initial premium **$10,000** and
      subsequent **$500**, minimum deferral **13 months**, maximum deferral **30 years**
      or income-start age **85**, income options **Life Only / Life with Cash Refund /
      Life with Installment Refund / Life with Period Certain 10–30 yrs** plus joint
      variants with **50/67/75%** survivor reduction, **100% return of premium** death
      benefit in deferral on every option except Life Only, **one-time ±5-year** income
      start date adjustment repriced on Moody's Baa + Annuity 2012 mortality + an
      interest-rate-change adjustment, optional **1–4% annual increase** elected at
      issue, **no charges, no cash value, no lapse**, and payment acceleration as the
      only in-force liquidity.
    - Extended case adds Pacific Life's **commutation of up to 100% of the present value
      of remaining guaranteed payments with an interest-rate adjustment**, which is the
      only feature in the product family requiring an MVA-like discount mechanic
      [S4][R13 § 3.F(7)].
    - QLAC overlay on the base case: restrict to **Life Only / Cash Refund / No Death
      Benefit / Joint & Survivor Cash Refund**, cap aggregate premium at the indexed
      dollar limit (**$210,000** in 2026), force income start **after the RMD age and by
      the first of the month after age 85**, and disable COLA, acceleration and
      commutation [S1][S2][S3][S4][R1][R3].

---

## Gaps and caveats

**Product-parameter gaps (things that genuinely do not exist for this product):**

- **Credited/declared interest rates, index crediting parameters (caps, participation
  rates, spreads, buffers, floors), M&E charges, admin charges, contract fees, rider
  charges, surrender charge schedules, free-withdrawal corridors, market value
  adjustment formulas, benefit-base rollups, step-ups, withdrawal percentages by
  attained-age band, and interim-value formulas** — **none of these exist** in a DIA.
  The product has no account value, no cash surrender value and no non-guaranteed
  crediting mechanic [S1][S2][S4][R13]. This is a structural feature of the product, not
  a research failure. The nearest analogues found are (a) Pacific Life's unnamed
  **interest-rate adjustment charge** on commutation [S4] and (b) the Compact's rule that
  the commuted-value interest rate "**can be adjusted for changes in interest rates …
  between the issue date and the commutation date**" [R13 § 3.F(7)].
- **No annuity purchase rate tables or income factors were obtained.** Insurers do not
  publish DIA purchase rates; the Compact standard expressly relieves them of disclosing
  the mortality table and interest rate used to determine the contractual income
  [R13 § 1.B(1)(a)]. A model must therefore either (i) supply its own pricing basis, or
  (ii) take the guaranteed income as an input. **No income-per-$100,000 figures are
  asserted anywhere in these notes.**
- **The Pacific Life interest-rate-adjustment charge formula was not found** in either
  the fact sheet [S4] or the client guide [S5]. It would appear only in the contract or
  the actuarial memorandum. Not modelled here.
- **No DIA specimen/sample contract was located.** Searches on insurer domains and SEC
  EDGAR full-text produced no DIA specimen contract; DIAs are non-registered
  general-account products, so they do not appear in SEC filings the way VAs and RILAs
  do. The IIPRC standard [R13] is the closest substitute and is used as the
  contractual-language authority throughout.

**Source-vintage caveats:**

- **MassMutual [S2] is a 2019 document** (© 2019; `CRN202011-221296`). Its QLAC figures
  ($130,000 limit, 25%-of-balance limit) and RMD-age references (70½) are **superseded**
  by [R1][R2][R3] and are flagged inline wherever quoted. Its product mechanics are
  presented as of that vintage. The current official MassMutual guide could **not** be
  retrieved [S8].
- **Guardian [S3] is a January 2018 document** and likewise references RMD age 70½.
  Fidelity's current comparison shows Guardian's qualified max issue age as 73 [S6],
  indicating the product has been updated since.
- **No USAA Life or Western & Southern primary document was retrieved.** All parameters
  for those two insurers come solely from Fidelity's comparison table [S6], which is a
  distributor aggregation rather than an insurer document. Treat those rows as
  lower-confidence.
- **No Brighthouse, Symetra, Principal or Mutual of Omaha primary document was
  retrieved.** The Brighthouse QLAC brochure returned 403 [S10]; the Symetra income
  annuity page returned 403; no Principal DIA client guide was located on
  principal.com. A third-party search result described a Symetra "Freedom Income" DIA
  with up to 45-year deferral and annual increases up to 6.5%, but **no Symetra document
  was retrieved and that claim is not asserted here.**

**Regulatory caveats and corrections:**

- **The brief's reference to "NAIC Model #250 disclosure" is a mis-numbering.**
  **Model #250 is the Variable Annuity Model Regulation** [R12] and does not apply to a
  non-variable DIA. The **Annuity Disclosure Model Regulation is Model #245** [R11].
- **Model #245 probably does not apply to a plain DIA either.** Its Section 3.A exempts
  "**Immediate and deferred annuities that contain no non-guaranteed elements**" [R11],
  and every income benefit in a non-participating DIA is guaranteed [R13 § 3.H(1)]. This
  is a direct reading of the retrieved model text; **whether individual states apply the
  exemption to DIAs in practice was not verified** and no state bulletin or filing
  guidance on the point was retrieved.
- **The brief's reference to "A-17" of Treas. Reg. 1.401(a)(9)-6 is now historical.**
  The QLAC rules were **restructured out of the Q&A "A-17" format into paragraph (q)** by
  T.D. 10001 (July 19, 2024) [R1 credit line][R6]. SECURE 2.0 § 202 still speaks in
  Q&A-17 terms because it was enacted in 2022 [R2]. Cite **§ 1.401(a)(9)-6(q)** for
  current law.
- **Model #805 Section 4.B (the nonforfeiture interest rate definition) and the balance
  of Section 4.A(1)(c)–(d) were not captured** in the extracted pages [R10]. The
  well-known "5-year CMT minus 125 bp, floored at 1% and capped at 3%" formulation is
  **[unverified]** here and is deliberately not stated as a sourced fact. It is in any
  case of limited relevance because a DIA has no cash value and the Compact substitutes
  a comparative certification for the demonstration [R13 § 1.B(1)(g)].
- **T.D. 10001's preamble was not read** — only the Federal Register metadata (title,
  89 FR 58886, July 19, 2024, effective September 17, 2024) and the codified result
  [R6][R1][R4][R5]. Any statement about *why* Treasury drafted a particular QLAC
  provision would be unsupported.
- **VM-22 Table 6.8 was captured only through attained age 79**; the table continues to
  higher ages in the Valuation Manual [R9]. VM-22 Table 6.7 (Accumulation category) was
  captured only through age 69 and is included only for contrast.
- **The VM-22 seven-basis-point expense provision was truncated at a page break** in the
  extract; the exact present-value base for contracts without an account value is not
  quoted [R9].
- **The 2012 IAM Period / 2012 IAM Basic / Scale G2 numerical tables were not
  downloaded.** They live at **mort.soa.org** [R16]; only the *application formulas* and
  the margin construction are sourced here [R9][R14]. Two `q_x` values appear (male age
  30, `q_x^2012 = 0.741`, `G2_30 = 0.010`) purely as the Valuation Manual's worked
  rounding example [R9].
- **The full SOA 2020-24 Payout Annuity Experience Study results are subscription-gated**
  ("Experience Studies Pro"); only the 5-page Study Highlights were retrieved [R15]. No
  A/E ratios or DIA-specific mortality results are quoted.
- **No SOA research specific to DIA or QLAC *pricing*** was located — the DIA-relevant
  SOA material found is mortality-experience research [R15][R16][R14] plus passing
  QLAC mentions in retirement-income papers that were not fetched.
- **SECURE 2.0's enactment date (December 29, 2022) is [unverified]** — the statutory
  text says only "the date of the enactment of this Act" [R2], and the Public Law's
  approval date was not separately confirmed from the retrieved text. The derived
  base-period quarter (July 1, 2022) *is* confirmed directly by the codified regulation
  [R1 (q)(4)(ii)(A)(1)].
- **MassMutual internal inconsistency, unresolved**: the Single Life — No Death Benefit
  option is said to be unavailable "in Connecticut or New York" in the body text and "in
  Connecticut or Florida" in two footnotes and the product highlights [S2]. Both
  variants are recorded above; neither is asserted as correct.
- **Fidelity's comparison table [S6] is a distributor aggregation.** Where it conflicts
  with an insurer's own document, the insurer document governs; where it is the only
  source (USAA, Western & Southern), it is flagged as such.
- **Unresolved conflict on Guardian's minimum deferral period.** Guardian's own 2018
  fact sheet states "Minimum: **24 full months** from the date of contract issue" [S3],
  while Fidelity's current comparison lists Guardian's deferral period as "**13 months**
  to 40 years" [S6]. This may be a product change since 2018 or an aggregation error;
  it was **not resolved**, because no current Guardian primary document could be
  retrieved [S9][S11]. Both figures are recorded above; neither is asserted as the
  current value.
- **State-by-state variation was not researched.** Only the state carve-outs the
  insurers themselves disclose are recorded (Florida's 13-month annuitization mandate
  [S2]; Pacific Life unavailable in CA/IL/NC/OR/PA/TX and its start-date adjustment
  unavailable in CT/NY, withdrawals unavailable in MO [S4]; MassMutual's CT/FL/NY
  restrictions [S2]).
