# Single Premium Immediate Annuity (SPIA) — research notes (U.S.)

Access date for all citations: 2026-08-04.

Purpose: source library and extracted specifications to drive a reference
liability cash-flow projection model (lifelib/modelx style) for U.S. individual
single premium immediate annuities (fixed, immediate payout annuities).

Citation discipline: every fact below is tagged with the source document it was
extracted from ([S#] primary product documents, [R#] regulatory/actuarial
references). Facts stated from general knowledge and not verified against a
retrieved document are tagged [unverified]. The [R#] numbers in this file are
**product-local** and are independent of the cross-product numbering used in
`_research/regulatory-actuarial.md`.

---

## Primary sources

### S1. Massachusetts Mutual Life Insurance Company — "MassMutual RetireEase — A Single Premium Immediate Annuity" (AN1500 526 / MM202905-316012)
- Publisher: Massachusetts Mutual Life Insurance Company (official document
  served from MassMutual's own `compass.massmutual.com` asset service)
- Doc type: consumer product brochure with a formal "Product Highlights" spec
  section (8 pages, © 2026)
- URL fetched: https://compass.massmutual.com/api/public/assets/file/bltd6a32711c1c02d16
- Retrieved: YES (full PDF, text layer extracted; surrender-charge chart
  re-extracted with text-position coordinates to confirm the year→rate mapping)
- Product: MassMutual RetireEase, contract form **#SPIA05; SPIA05 (NC)**, "a
  single premium immediate fixed annuity contract."
- Facts extracted:
  - **Market types**: Nonqualified; Qualified (Traditional IRA, SEP IRA,
    Custodial IRA, Roth IRA, Beneficiary/Inherited IRA).
  - **Issue age (annuitant)**: lifetime annuity options ages **18–90**; period
    certain only options **maximum age 100**. Issue age is defined **age
    nearest** birthday ("if the annuitant is 74 years, six months, and one day
    old, his or her contract age is 75").
  - **Single purchase payment**: minimum **$10,000**; minimum scheduled annuity
    income payment must be at least **$100**; maximum without further MassMutual
    approval **$1.5 million**.
  - **Annuity date**: must be within **12 months** of contract issue.
  - **Payment frequency**: monthly, quarterly, semi-annually, annually.
  - **Single life annuity options**: No Refund; Cash Refund; Installment Refund;
    Period Certain.
  - **Joint & survivor life annuity options** — three families:
    - No-refund: No Refund; *Reduction at Death of Annuitant — No Refund*;
      *Reduction at Death of Either Annuitant — No Refund*.
    - Refund: Cash Refund; Installment Refund; *Reduction at Death of
      Annuitant — Installment Refund*; *Reduction at Death of Either Annuitant —
      Installment Refund*.
    - Period certain: Period Certain; *Reduction at Death of Annuitant — Period
      Certain*; *Reduction at Death of Either Annuitant — Period Certain*.
  - **Survivor reduction percentages**: "Reductions of 1/2, 2/3, or 3/4 are
    available." The brochure body states the owner **chooses whether the
    reduction happens upon the primary annuitant's death or the first death**
    (annuitant or joint annuitant), and that payments continue at a reduced
    amount for as long as the surviving annuitant lives.
  - **Period certain only**: Period Certain **5–30 years**; length may be
    lengthened or shortened after the first contract year, subject to contract
    limits.
  - **MassMutual Inflation Protector** (optional COLA): automatically increases
    annuity payments by **1%, 2%, 3%, or 4%** on each anniversary of the annuity
    date; must be elected at contract issue; may not be cancelled or changed;
    reduces the initial payment; **not available with the Life with Installment
    Refund** option; "may be limited or not available at all due to RMD rules."
  - **Withdrawal provisions** (available **only** with options that include a
    period certain):
    - *Period Certain Only*: one full **or** partial withdrawal each year after
      the first contract year; a partial withdrawal reduces future period
      certain annuity payment amounts.
    - *Single or Joint Life with Period Certain*: one **partial** withdrawal per
      year after the first contract year; the withdrawal reduces future period
      certain payment amounts but **does not reduce the lifetime payments after
      the end of the period certain**.
    - Withdrawals are **not allowed for contracts issued in Oregon**.
  - **Withdrawal limits**: minimum **$5,000**; maximum = **the present value of
    all remaining period certain payments, less any surrender charges**; partial
    withdrawals limited so each remaining guaranteed payment is at least $100.
  - **Surrender charges** (percentage of amount withdrawn; applies only to
    options that include a period certain), by contract year:
    | Contract year | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10+ |
    |---|---|---|---|---|---|---|---|---|---|
    | Charge | 8% | 7% | 6% | 5% | 4% | 3% | 2% | 1% | 0% |
  - **No fees / no cash value**: "there are zero fees and no market performance
    to worry about. In addition, there is no accumulation or cash value — and,
    therefore, limited liquidity."
  - **Ownership**: individual or non-natural entity (e.g., a trust); joint
    ownership allowed between two individuals; contract cannot be jointly owned
    by an individual and a non-natural entity. Collateral assignment: NY
    nonqualified contracts unrestricted; all other states limited to Period
    Certain Only options and requires MassMutual approval.
  - **Qualified death rule**: for qualified contracts, on the owner's death
    (annuitant if Custodial IRA) MassMutual "may shorten the remaining payment
    period" to keep payments within the **10-year post-death distribution period
    under IRC §401(a)(9)**, or within the beneficiary's life/life expectancy for
    eligible designated beneficiaries (spouse, or an individual not more than
    10 years younger than the decedent).
  - Product is explicitly **not** a Medicaid-friendly immediate annuity.

### S2. Pacific Life Insurance Company — "Pacific Income Provider — A Single-Premium, Immediate Fixed Annuity" fact sheet (FAC0719-00 11/25, item 25-555)
- Publisher: Pacific Life Insurance Company (official; `annuities.pacificlife.com`)
- Doc type: product fact sheet / spec sheet (4 pages)
- URL fetched: https://www.annuities.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/fact-sheets/pacific-income-provider-fact-sheet.pdf
- Retrieved: YES (full PDF read)
- Product: **Pacific Income Provider**. Contract form series **ICC10:30-1181,
  30-1181OR**; endorsements ICC14:15-1181-1, 15-1181OR-1, ICC14:15-1181-2A,
  15-1181OR-2A, ICC14:15-1181-3, ICC14:15-1181-4.
- Facts extracted:
  - **Purchase payment**: single premium; all cash purchase payments submitted
    with the application; 1035 exchange/transfer funds must be received within
    **60 days (90 days in New York)**.
  - **Minimum**: **$25,000** (nonqualified and qualified). **Maximum**:
    aggregate purchase payments over **$2 million for ages 0–85**, or over
    **$1 million for ages 86+**, require Pacific Life approval.
  - **Maximum issue age: 90.**
  - Payments must begin **within one year** of purchase; the income option is
    set at contract issue and **cannot be changed**; frequency monthly,
    quarterly, semiannually, or annually; only one option per contract.
  - **Period Certain option**: up to **30 years**.
  - **Single Life options**: Life Only; Life with Period Certain (up to 30
    years); Life with Cash Refund; Life with Installment Refund.
  - **Joint Life options** — "Income payments can be reduced to **50%, 67%, or
    75%** of the current income payment **upon the death of either annuitant**":
    Joint Life Only; Joint Life with Period Certain; Joint Life with Cash Refund;
    Joint Life with Installment Refund.
  - **Joint and Survivor Life options** — "Income payments can be reduced to
    **50%, 67%, or 75%** of the current income payment **upon the death of the
    primary annuitant**": Joint and Survivor Life Only; …with Period Certain;
    …with Cash Refund; …with Installment Refund.
    *(This is the cleanest published statement of the "reduce on either death"
    vs "reduce only on primary death" distinction found in this research.)*
  - **Qualified restrictions**: for qualified contracts, Period Certain length
    may not exceed **10 years (nine years for an inherited IRA)** where needed to
    comply with SECURE Act RMD regulations. **Installment Refund is not
    available with qualified contracts.** For IRA/Roth IRA/SEP-IRA contracts,
    joint annuitants limited to a spouse, or an individual older than or **no
    more than 10 years younger** than the primary annuitant.
  - **Optional features** (only one may be added; elected at purchase; not
    changeable afterward):
    - **Future Adjustment Option** — a one-time increase or decrease in income
      payments on a date selected at issue. Increase by **up to three times** the
      initial income payment, or decrease by **up to one-half** of the initial
      income payment. Not available with Joint income options when a reduced
      benefit has been elected. An **increasing** future adjustment is **not
      available for qualified contracts**. May not satisfy IRC §72(t)/§72(q)
      substantially-equal-periodic-payment requirements.
    - **Inflation Protection Option** — annual increase of **2%, 3%, or 4%**,
      selected at issue.
  - **Income Payment Acceleration** (liquidity): after age **59½**, and after
    receiving monthly annuity payments for **at least five years**, the owner may
    take a lump sum equal to **three or six times** the normal monthly payment;
    normal payments resume in the **fourth or seventh month** respectively;
    available with **all** income options; exercisable a **maximum of two
    times**; at least one normal monthly payment must be received between uses.
    For qualified contracts the entire acceleration period must fall in the same
    tax year.
  - **Withdrawal of Guaranteed Income Payments** (commutation): for
    **nonqualified** contracts only, a lump-sum withdrawal of **up to 100% of the
    present value of remaining guaranteed income payments**. **Not available in
    Oregon.** Available with all options **except** Life Only, Joint Life Only,
    Joint and Survivor Life Only. **An interest-rate adjustment will apply.**
    Owner(s) must be **59½ or older**. A withdrawal lowers or may stop remaining
    guaranteed payments; **except for the Period Certain option, if the owner is
    still living at the end of the period when guaranteed payments would have
    stopped, Pacific Life will resume income payments until death.**
  - **Six-month waiting period** in each direction between Income Payment
    Acceleration and a withdrawal.
  - **Death benefit**: return of premium is paid if an owner or annuitant dies,
    **or is diagnosed with a terminal illness with life expectancy of 12 months
    or fewer, before the first payment date**.

### S3. Pacific Life Insurance Company — "Pacific Income Provider — A Single-Premium, Immediate Fixed Annuity" client guide (FAC0718-0224)
- Publisher: Pacific Life Insurance Company (official; `pacificlife.com`)
- Doc type: consumer client guide (16 pages, Feb 2024 version)
- URL fetched: https://www.pacificlife.com/content/dam/paclife/rsd/annuities/public/pdfs/guide/pacific-income-provider-client-guide.pdf
- Retrieved: YES (full PDF read)
- Facts extracted (supplements S2):
  - Narrative confirmation of the joint-life distinction: "Payments can be
    reduced upon either person's death (**Joint Life option**) or upon the death
    of the **primary annuitant** (**Joint and Survivor Life option**)."
  - Cash Refund definition: "The remaining purchase payment amount equals your
    original purchase payment minus the total income payments received."
  - "Usually, the longer the payout period, the lower the income payment
    amount." After issue, income option and frequency **cannot change**.
  - Withdrawal eligibility restated: nonqualified contract, age ≥ 59½, and one
    of Period Certain / Life with Period Certain / Life with Cash Refund / Life
    with Installment Refund (or the Joint version). "There is **no limit to the
    number of withdrawals** you can make."
  - **Hypothetical income illustrations** (explicitly "For illustrative purposes
    only. Your payments may differ") — usable only as loose rate anchors for the
    Feb-2024 rate environment:
    - John and Mary, **both age 65**, **Joint Life Only**: premium **$230,856**
      buys **$1,200/month** ⇒ **$519.8/month per $100,000**, i.e. ≈ **6.24%**
      annualized payout rate.
    - Virginia, **age 69**, IRA, **Life with 10 Year Period Certain**: premium
      **$281,379** buys **$20,000/year** ⇒ ≈ **7.11%** annualized payout rate.
    - Inflation Protection chart: **male age 65**, purchase payment **$204,736**,
      Single Life with **3% Inflation Protection**: monthly income begins at
      about **$900** and reaches about **$1,600** after 20 years ("increased more
      than 70% after 20 years") ⇒ ≈ **5.28%** initial annualized payout rate with
      3% compounding. (Chart values are rounded to the nearest $100 in the
      source.)
  - Income Payment Acceleration worked example: normal monthly payment $1,000;
    a three-month acceleration requested after the April payment produces
    **$3,000** in addition to the April $1,000 (total $4,000), then **no payments
    for May, June, July**, and normal payments resume in **August**.

### S4. Integrity Life Insurance Company / National Integrity Life Insurance Company (Western & Southern Financial Group) — "IncomeSource® Series Product Summary" (CF-51-0075-2406)
- Publisher: Western & Southern Financial Group (official; `westernsouthern.com`)
- Doc type: distributor/producer product summary (2 pages)
- URL fetched: https://www.westernsouthern.com/-/media/files/distributors/toolkits/incomesource-product-summary.pdf
- Retrieved: YES (full PDF read)
- Product: **IncomeSource** SPIA. Contract series **ICC16 ENT-01 1701** and
  **ENT-01 1701 NY**. Deceased Commutation Rider series **ICC09 ER.02 0901**;
  Living Commutation Rider series **ICC09 ER.01 0901**.
- Facts extracted:
  - **Availability**: all states and D.C.
  - **Issue ages**: **0–95**, depending on income payout option. Individual
    payout options **0–85** (0–95 for certain-period payouts). Joint payout
    options **0–85** (one annuitant may be as old as **90**).
  - **Minimum contract size**: **$10,000**, or the premium required to purchase a
    periodic income payout of **$100**, whichever is higher.
  - **Maximum contract size**: **$2 million** without prior company approval,
    with exceptions: Single Life only & Temporary Life — **$1 million** through
    issue age 75, **$500,000** for issue ages 76–85; Joint Life only —
    **$500,000** for issue ages 76–85.
  - **Tax status**: both qualified and nonqualified funds accepted.
  - **Payout frequencies**: monthly, quarterly, semiannually, annually.
  - **Income payout options**: life or two lives; life or two lives with period
    certain; life or two lives with cash refund; life or two lives with
    installment refund; **period certain (5–30 years)**; **temporary life
    payouts (5–30 years)** — "Income will continue for a period of time…
    specified by the owner, **only while the annuitant is alive**. Temporary life
    payouts provide **no benefit on or after death** of annuitant."
  - **Increasing Payout Option (IPO)**: annually **compounded** guaranteed
    increase of **1%, 2%, 3%, 4% or 5%**; electing it reduces the initial payout;
    "if annuitant dies prior to life expectancy, a payee may receive less total
    income with an IPO than without one."
  - **Commutation Benefits** (the most explicit commutation provision found):
    - *Living annuitant commutation*: **10%–90% of the present value** of all
      remaining payouts, **available after the first contract year**.
    - *Deceased annuitant commutation (death benefit commutation)*: beneficiary
      may cash out the remaining **certain** payouts on the death of the
      annuitant (single life) or the last-to-die joint annuitant (joint and
      survivor).
    - Restrictions: **currently unavailable in NY**; not available with **life
      only** payouts, **temporary life** payouts, or **certain period payouts of
      less than 10 years**. (An accompanying W&S description also lists Oregon as
      excluded — see Gaps.) Available for both qualified and nonqualified.
  - **Core contract nature**: "An immediate annuity is permanent. The owner has
    no access to the premium… There is **no cash value, no death benefit** and
    the annuity **can't be surrendered**. The contract terms, such as payment
    amount and frequency, **cannot be changed, unless commutation is available
    and elected**."

### S5. New York Life Insurance and Annuity Corporation (NYLIAC) — "Just the facts about the New York Life Guaranteed Lifetime Income Annuity II" (1222A.1125 / ML25-006013 / SMRU5817113, exp. 06.27.2028)
- Publisher: New York Life (official; `nylannuities.com`)
- Doc type: client fact sheet / spec sheet (5 pages)
- URL fetched: https://www.nylannuities.com/connectedassets/final-assets/marketing-materials/fact-sheet-products/TPD_Client_FactSheet_GLI_II_Generic.pdf
- Retrieved: YES via direct HTTP with a browser user-agent. (Note: the same URL
  returned **HTTP 403** through the WebFetch tool; recorded here as a
  tool-specific failure, not a dead link.)
- Product: **New York Life Guaranteed Lifetime Income Annuity II**, issued by
  NYLIAC. Policy form **ICC11-P103** (may be **211-P103**); state variations
  apply. "The contract is **irrevocable and has no cash surrender value**."
- Facts extracted:
  - **Issue ages** (availability of payment options varies by age):
    - Nonqualified **0–95**
    - Qualified **18–89** (joint annuitants 0–89)
    - Inherited nonqualified **0–95** (no joint owner/annuitants)
    - Inherited qualified **0–89** (no joint annuitants)
    - Roth **59½–89** (Roth IRA in place ≥ 5 calendar years before the year
      income starts; joint annuitants must be spouses and must independently
      satisfy the 5-year and 59½ tests)
    - Inherited Roth IRA **0–89** (no joint annuitants)
  - **Single premium**: minimum **$10,000** (may vary by state or payment
    option); premium over **$2 million** requires a large-case questionnaire and
    prior NYLIAC approval (aggregating premiums from multiple policies).
  - **Income payment modes**: monthly, quarterly, semi-annually, annually.
    Payments must begin **within 12 months** of purchase.
  - **Payment options**:
    - **Life Only** (and Joint Life Only — on the joint version, if one annuitant
      dies payments continue **in full** to the survivor; payments stop at the
      death of both).
    - **Life with Period Certain** — guaranteed period **5 to 30 years**.
    - **Life with Cash Refund** — lump sum to beneficiaries equal to premium less
      all payments made. For **Joint Life** policies this option is available
      **only if the survivor's income is 100%** of the income while both are
      alive.
    - **Life with Installment Refund** — beneficiaries continue receiving
      scheduled payments until the premium is fully recovered.
    - **Life with Percent of Premium Death Benefit** — death benefit equal to
      **25% or 50% of the original premium**, chosen at issue. Not available on
      qualified policies; not available in New York.
  - **Guaranteed period definition for refund options**: "The guaranteed payment
    period for the Life with Cash Refund and Life with Installment Refund payment
    options is determined by **dividing the premium paid for the policy by the
    annualized income benefit amount**." (Directly implementable.)
  - **Reduction of Income for Joint Life Policies**: survivor may receive
    **40%–99%** of the original income amount. Percentage chosen at purchase.
    "For Life with Period Certain policies, if the first annuitant dies during
    the guaranteed payment period, the payments to the second annuitant **will
    not be reduced until the end of that period**." For **qualified** policies
    with a **spouse** joint annuitant, the owner may elect reduction on the death
    of the **primary annuitant** or on the death of **either** annuitant; for
    qualified policies with a **non-spouse** joint annuitant, reduction may occur
    **only after the death of the primary annuitant**, and if the secondary
    annuitant dies first, **100%** of payments continue while the primary lives.
    Not available on Joint Life with Cash Refund or Installment Refund, or with
    the Changing Needs Option / Income Enhancement Option.
  - **Annual Increase Option** (COLA): payments increase each year by **1% to
    4%**; must be elected at purchase; increase begins **one year after the first
    income payment**; owner must be at least **59½** at the first payment;
    available on qualified and nonqualified; not available with Changing Needs
    Option or Income Enhancement Option.
  - **Changing Needs Option**: one-time **increase of 1% to 400%** (up to five
    times the original income payment) **or** one-time **decrease of 1% to 50%**
    (down to one-half of the original payment); may begin on or any time after
    the **third anniversary** of the income start date; date and percentage fixed
    at purchase; owner ≥ 59½ at first payment; annuitant (younger annuitant if
    joint) must be **age 80 or younger at purchase** and the adjustment must
    occur before the annuitant's **91st birthday**; nonqualified only.
  - **Income Enhancement Option**: a **one-time** increase in income after the
    **fifth policy anniversary** if the **10-Year CMT Index** in the third full
    week of the month immediately preceding the fifth anniversary is **at least
    two percentage points (2%) higher** than the 10-Year CMT in the third full
    week of the month immediately preceding the policy date. The increase amount
    is **fixed at issue**. Nonqualified only; annuitant (younger annuitant if
    joint) **75 or younger** at issue; owner ≥ 59½ at first payment.
  - **Withdrawal / commutation features**:
    - **Up to 100% Cash Withdrawal (guaranteed periods only)**: after age 59½,
      withdraw up to **100% of the discounted value of the remaining guaranteed
      payments** at any time within the guaranteed payment period. Future income
      payments through the end of the guaranteed period are reduced **by the
      withdrawal percentage elected**; if the annuitant is alive at the end of
      the guaranteed period, **full annuity payments resume for the life of the
      policy**. Exercisable **once**. Nonqualified only, and only with Life with
      Cash Refund / Life with Installment Refund / Life with Period Certain.
    - **30% Cash Withdrawal (based on life expectancy)**: after age 59½,
      withdraw **30% of the discounted value of the remaining payments expected
      to be paid, based on the annuitant's life expectancy when the policy was
      purchased**. Exercisable on the **5th, 10th, or 15th anniversary** of the
      first income payment, or on proof of a significant nonmedical financial
      loss. Once exercised, **future income payments are reduced by 30% for the
      life of the policy**. Exercisable once; **not available after the
      annuitant's life expectancy**. Available on nonqualified policies with Life
      Only or Life with Percent of Premium Death Benefit; on qualified policies
      with Life Only, Life with Cash Refund, Life with Installment Refund, or
      Life with 5–30-year options; and on Roth IRA Life Only policies.
    - The two cash-withdrawal features are **mutually exclusive**.
    - **Interest Rate Change Adjustment**: "The cash withdrawal amount is subject
      to an Interest Rate Change Adjustment that will **increase or decrease the
      withdrawal amount based on the change in interest rates, as measured by the
      10-Year Constant Maturity Treasury (CMT) Index**, between the time you
      purchase your policy and the time you elect to receive the cash
      withdrawal." (This is the SPIA analogue of an MVA; the actual formula is
      not published in this document.)
  - **Payment Acceleration** (nonqualified, monthly payments): after 59½, receive
    the next scheduled monthly payment plus **five subsequent payments** — six
    months of income at once; no payments for the next five months; usable
    **two times** during the life of the policy.
  - **Death-of-annuitant commutation**: "Upon death of the annuitant (or both
    annuitants for a Joint Life Policy), remaining guaranteed payments **can be
    commuted into a lump sum** if the policy owner selected this option before
    death. The commuted value will always be less than the sum of the remaining
    payments."
  - **Roth RMD interaction**: if at the owner's death the remaining guaranteed
    period under a Life with Period Certain option is longer than the
    beneficiary's life expectancy (IRS Single Life Table), **NYLIAC will commute
    all future guaranteed payments**.
  - **Tax caveats stated by the issuer**: withdrawals under Payment Acceleration
    and Cash Withdrawal are reported **as fully taxable**; the federal income tax
    treatment of an immediate annuity containing a withdrawal feature is
    described by NYLIAC as **uncertain**; if a policy with a withdrawal feature
    is purchased before 59½ and the feature is exercised within five years of the
    first annuity payment, a **10% additional tax (plus interest) may be imposed
    retroactively** on annuity payments received before 59½.
  - **Payout-option pricing note**: "there are limited situations (primarily
    younger annuitants) where the **same or essentially the same income payment**
    is available for longer guarantee periods or cash refund options."

### S6. Nationwide Life Insurance Company — "INCOME Promise® — A Single-premium Immediate Fixed Annuity" (NFS-0133-C (05/04))
- Publisher: Nationwide Life Insurance Company (PDF hosted on Nationwide's
  retirement-plans site `nrsforu.com`)
- Doc type: consumer brochure with a spec page (8 pages)
- URL fetched: https://www.nrsforu.com/BOA/media/pdf/NFS-0133.pdf
- Retrieved: YES (full PDF read). **Caveat: this is a 2004-vintage document**
  (contracts APO-4834, APO-4834-37, APO-4834-43; Oklahoma APO-4834-36) — retained
  because it documents an older but very typical SPIA option set and terminology.
- Facts extracted:
  - **Maximum issue age**: annuitants through **85**; owners any age.
  - **Minimum/maximum single premium**: **$10,000 / $2,000,000** ("higher amounts
    may be available on certain options").
  - **Payments**: monthly, quarterly, semiannual, annual. **Minimum payment
    amount $100**; if any payment would be less than $100, Nationwide "has the
    right to **reduce the frequency of payments**" to meet the minimum.
  - **Payment options**: Single life; Single life with term certain (**five, 10,
    15 or 20 years**); Single life with installment refund; **Joint and 50% last
    survivor**; **Joint and 100% last survivor**; Term certain (**five to 20
    years**).
  - **Scheduled payment increase** (COLA): elect **1%, 2% or 3%** annually; on
    each contract anniversary the fixed payment level for the following year is
    increased by the chosen annual increase factor; election is **irrevocable**.
  - **Death during a term-certain period**: the beneficiary may choose to receive
    the remaining term-certain payments **or a lump sum equal to the present
    value of those payments**.
  - Premium is reduced by "applicable state premium taxes" in determining income.

### S7. TIAA-CREF Life Insurance Company — "Single Premium Immediate Annuities" prospectus (Rule 497(c) filing, Registration No. 333-46414, dated May 1, 2008)
- Publisher: TIAA-CREF Life Insurance Company, filed with the SEC
- Doc type: **registered product prospectus** (SEC EDGAR)
- URL fetched: https://www.sec.gov/Archives/edgar/data/1067490/000119312508102441/d497.htm
- Retrieved: YES (full HTML, 256 KB of text). **Caveat: 2008 filing** — used for
  its contractual precision on immediate-annuity mechanics, not as a
  currently-sold product spec. Note also that these are single premium immediate
  **variable** annuity contracts with a fixed-account option, not a pure fixed
  SPIA.
- Facts extracted:
  - Three contracts: **One-Life Annuity** (income as long as the annuitant lives
    or until the end of an optional specified guaranteed period, whichever is
    longer); **Two-Life Annuity**; **Fixed-Period Annuity** (income for a fixed
    period of **between 5 and 30 years**).
  - **Two-Life income options** (contractual names): *Two-Life Annuity with Full
    Benefit While Either Annuitant Survives*; *Two-Life Annuity with **Two-Thirds
    Benefit** While Either Annuitant Survives*; *Two-Life Annuity with **One-Half
    Benefit** While Second Annuitant Survives First Annuitant*.
    (Note the asymmetry: the two-thirds form reduces on **either** death; the
    one-half form reduces only on the **first annuitant's** death.)
  - **Assumed Investment Return = 4%** — "the assumed annual rate of return used
    in calculating the amount of each variable annuity payment."
  - **Commuted Value** definition (verbatim mechanics): "the amount we will pay
    under certain circumstances in a lump sum instead of the remaining series of
    annuity payments. It's less than the total of the future payments, because
    the future interest we've assumed in computing the series of payments will
    not be earned if payment is made in one sum. **For the fixed account, the
    commuted value is the sum of payments less the interest that would have been
    earned from the effective date of the commuted value calculation to the date
    each payment would have been made.** For any variable investment account, the
    commuted value is based on interest at an effective annual rate of **4%**…"
  - **Current Value** definition: "the present value of the future annuity
    payments, which for variable payments is computed using the assumption that
    the relevant investment account has an effective annual rate of 4%. In the
    case of the One-Life and Two-Life Annuities, the present value is determined
    based on **the age of the annuitant(s), if alive; the remaining guaranteed
    period, if any; the frequency of payment; and the mortality tables used to
    determine the initial amount of annuity payments**." Used for free-look
    refunds.
  - **Liquidity limits**: a lump-sum commuted value is available (i) from a
    One-Life or Two-Life Annuity **only if the annuitant(s) dies during the
    guaranteed period**, or (ii) under a Fixed-Period Annuity from the variable
    investment accounts. "**Under the One-Life and Two-Life Annuities, no lump
    sum payment is available during the lifetime of annuitant(s)**, or if the
    annuitant dies after the end of the guaranteed period."
  - **Separate-account charges** (variable payout only): annual contract fee
    **None**; **mortality and expense risk charge — maximum contractual 1.00%**,
    fee waiver 0.60%, **current 0.40%**; **administrative expense charge —
    maximum 0.20%, current 0.20%**; total separate account annual charges
    **maximum 1.20%, current 0.60%** (of average account value). At least three
    months' notice before raising above 0.60%.
  - **Statutory valuation basis disclosed in the financial statements**: "For
    deferred annuities in the pay out stage, **Single Premium Immediate Annuities
    ('SPIA')** and supplementary contracts, **the path of future guaranteed
    benefits with the highest present value is used to set policy reserves**. For
    most fixed period annuity contracts…, this present value is calculated using
    the **maximum statutory valuation interest rate for SPIA**. **Life annuity
    contracts are valued based on the Annuity 2000 table**, and the maximum
    valuation interest rates on an **issue year basis**." (2007 valuation date.)
  - Premium tax: "If TIAA-CREF Life is required to pay this premium tax, it may
    deduct the amount of the premium tax paid from any premium payment."

### S8. Mutual of Omaha / United of Omaha Life Insurance Company — producer product overview (form 135880, updated 9-17)
- Publisher: Mutual of Omaha Insurance Company (official producer site)
- Doc type: producer portfolio overview (16 pages); **for producer use only**
- URL fetched: https://producer.mutualofomaha.com/enterprise/wcm/connect/14033a75-36a8-4542-b987-a96fa72cc5b3/135880.pdf?MOD=AJPERES&ContentCache=NONE
- Retrieved: YES (full PDF read). **Caveat: dated 9-2017.**
- Facts extracted (income annuities; annuities underwritten by **United of Omaha
  Life Insurance Company**, and Companion Life in New York):
  - **Ultra-Income** (SPIA): **issue ages 0–85**; multiple payout options;
    payments must begin **within 13 months** following the purchase date; choice
    of payment frequency **monthly, quarterly, semiannually or annually**.
    Optional features: **age rating available** (i.e., substandard/impaired-life
    rating that raises income); **up to 6 percent Cost-of-Living Allowance
    (COLA)**.
  - **Income Annuity with Premium Return** (SPIA): issue ages **59–85**; life
    only or joint life income payouts; payments must begin within 13 months;
    **return of premium upon death**.
  - **Income Access** (SPIA): issue ages **0–85**; "offers various optional
    features that provide additional income"; payments must begin within
    13 months; return of premium features. Optional features listed alongside:
    **10 percent or 20 percent payment increase based on health condition**;
    **3 percent inflation protection**; **50 percent payment increase for nursing
    home confinement**; **survivor continuation option**.

### S9. LifeAnnuities.us — "Best SPIA Rates — July 2026: Top Payouts by Age"
- Publisher: LifeAnnuities.us (**commercial annuity-quote / lead-generation
  site — NOT an insurer, regulator, or actuarial body**)
- Doc type: rate-survey web page
- URL fetched: https://lifeannuities.us/rates/best-spia-rates/
- Retrieved: YES (HTML)
- **Reliability: LOW.** Recorded solely as a rate anchor of last resort because
  no insurer- or regulator-published payout-rate table could be retrieved (see
  Gaps). Numbers below should be treated as indicative order-of-magnitude only
  and must not be used as authoritative pricing.
- Facts extracted (stated methodology: highest quote among 8 A-rated carriers
  surveyed as of **July 2026**, per **$100,000** single premium, **life-only**
  payout; joint figures assume a 100% survivor benefit):
  | Age | Male | Female | Joint |
  |---|---|---|---|
  | 55 | $575/mo | $558/mo | $511/mo |
  | 60 | $618/mo | $597/mo | $546/mo |
  | 65 | $664/mo | $635/mo | $583/mo |
  | 70 | $754/mo | $704/mo | $659/mo |
  | 75 | $882/mo | $805/mo | $765/mo |
  | 80 | $1,059/mo | $975/mo | $905/mo |
  - Carriers named as surveyed: New York Life, MassMutual, Western & Southern,
    Pacific Life, Prudential, Nationwide, Lincoln Financial, Mutual of Omaha.
  - Male 65 life-only $664/month per $100,000 ⇒ **7.97% annualized payout rate**.
  - Site's own carrier table for male 65 life only: New York Life $664,
    Western & Southern $659, Pacific Life $653, Mutual of Omaha $648,
    MassMutual $642, Nationwide $637, Prudential $632, Lincoln Financial $627 —
    i.e., a **best-to-worst spread of about 5–6%**.
  - Site's claim on option pricing: "A 10-year period certain costs only ~3% of
    income."

### S10. New York Life — "Annuity rates" page (weekly payout-rate publication)
- Publisher: New York Life (official; `nylannuities.com`)
- Doc type: rates web page
- URL fetched: https://www.nylannuities.com/resources/rates
- Retrieved: PARTIAL — page HTML retrieved successfully, but the rate tables are
  loaded client-side via JavaScript and rendered as "Loading…" in the static
  HTML, so **no numeric rates could be extracted**.
- Facts extracted (methodology text, which is itself useful):
  - New York Life publishes **weekly** payout rates for the Guaranteed Lifetime
    Income Annuity II, quoted as "the **annualized payout as percent of total
    premium**", "**Based on the life with cash refund option for a policy
    purchased by a male annuitant with $100,000**", broken out by **Age × Single
    Life × Joint Life**. "These payout rates … include both interest and return
    of principal."
  - "Payout amounts for female applicants, who have longer life expectancies, are
    lower. **In the state of MT, payout amounts do not differentiate male and
    female life expectancies.**"
  - There is an "Income Annuity Quote-Lock Procedures" process (details not on
    this page).

### S11. The Guardian Life Insurance Company of America — "Single Premium Immediate Annuity (SPIA)" educational page (last updated January 29, 2026)
- Publisher: Guardian Life (official; `guardianlife.com`)
- Doc type: consumer education page (not a product spec sheet)
- URL fetched: https://www.guardianlife.com/annuities/income/single-premium-immediate-spia
- Retrieved: YES (HTML). Low specification content; used only for the general
  points below.
- Facts extracted:
  - Market size datapoint: "More than **$3.6 billion** in single premium
    immediate annuities (SPIAs) were sold in the **first quarter of 2024**."
  - "Immediate annuities start making annuity payments 'immediately': typically
    within a month (and **never more than one year out**)."
  - "In some states, your premium payment may be subject to an **annuity tax**.
    This tax may be deducted from your premium by the insurer prior to scheduling
    payments." (i.e., state premium tax reduces the amount annuitized.)
  - "Immediate annuity payments typically aren't subject to the 10% federal
    income tax penalty."
  - Notes that some immediate annuities "offer non-guaranteed **dividend
    payments** in addition to the guaranteed income" (participating SPIA design).

### Failed / unusable fetches (recorded for completeness; contents NOT used)
- `https://www.immediateannuities.com/annuity-brochures/massmutual-retireease.pdf` — **HTTP 403**.
- `https://www.immediateannuities.com/annuity-rates/by-age.html` — **HTTP 403** (both WebFetch and direct HTTP).
- `https://legacy.mutualofomaha.com/documents/annuities/lc3146.pdf` (Ultra-Income brochure) — **HTTP 404**.
- `https://webprod3.mutualofomaha.com/annuities/plan-details/ultra-income.php` — **DNS resolution failure**.
- `https://communications.fidelity.com/fili/spia/nyl/docs/new_york_life_lifetime_spia_factsheet.pdf` — HTTP 200 but the PDF has **no extractable text layer** (image-only); no facts taken.
- `https://communications.fidelity.com/fili/docs/ws-spia-factsheet.pdf` — returned a **230-byte stub**, not the document.
- `https://www.nylannuities.com/connectedassets/.../TPD_Client_FactSheet_GLI_II_Generic.pdf` via **WebFetch** — HTTP 403 (succeeded via direct HTTP; see S5).

---

## Regulatory and actuarial references

### R1. NAIC — *Valuation Manual*, **Jan. 1, 2026 Edition**, **VM-V: Statutory Maximum Valuation Interest Rates for Formulaic Reserves**, Section 1 "Income Annuities"
- Publisher: National Association of Insurance Commissioners
- URL fetched: https://content.naic.org/sites/default/files/pbr_data_valuation_manual_current_edition.pdf
- Retrieved: YES (457-page PDF; VM-V Section 1 at PDF pages 447–457)
- **Status finding (answers the VM-22 scope question):** in the current
  Valuation Manual the *statutory maximum valuation interest rate machinery for
  income annuities that was historically labelled VM-22 now sits in **VM-V***.
  **VM-22 has been redefined** as "Requirements for Principle-Based Reserves for
  **Non-Variable Annuities**" (see R2).
- Purpose and scope (VM-V §1.A): "These requirements define **for single premium
  immediate annuity contracts and other similar contracts, certificates and
  contract features the statutory maximum valuation interest rate** that complies
  with Model #820. These are the maximum interest rate assumption requirements to
  be used in the **CARVM** and for some contracts, **CRVM**."
- In scope (§1.A.2), whether group or individual, life-contingent **and**
  term-certain-only, direct or assumed:
  a. **Immediate annuity contracts issued after Dec. 31, 2017**;
  b. Deferred income annuity contracts issued after Dec. 31, 2017;
  c. Structured settlements in payout or deferred status issued after Dec. 31, 2017;
  d./e. Fixed payout annuities arising from settlement options or annuitizations
  of host contracts (2017/2018 transition rules);
  f. Supplementary contracts (excluding contracts with no scheduled payments such
  as retained asset accounts and settlements at interest);
  g./h. Fixed income payment streams from CDAs and from guaranteed living
  benefits once contract funds are exhausted;
  i. Certificates with premium determination dates after Dec. 31, 2017 emanating
  from non-variable group annuity contracts under Model #820 §5.C.2.
- These requirements **supersede** VM-A/VM-C for in-scope business and expressly
  supersede **AG 9-B** (Clarification of Methods Under SVL for Individual SPIAs…)
  and the valuation-interest-rate references in **AG 9-C** (Use of Substandard
  Annuity Mortality Tables in Valuing Impaired Lives Under Individual SPIAs).
- **Rate-setting mechanics** (VM-V §1.B–§1.C), which are directly implementable:
  - **Reference period (RP)** — for life-contingent contracts with substantially
    similar payments: the time, **rounded to the nearest year**, from the
    **premium determination date** to the earlier of (i) the date of the last
    **non-life-contingent** payment and (ii) the date of the **first
    life-contingent** payment. For non-life-contingent contracts: to the date of
    the last non-life-contingent payment. Where payments are not substantially
    similar, select the bucket whose Macaulay duration best fits.
    *Guidance note*: "Contracts with **installment refunds** or similar features
    should consider the length of the installment period calculated from the
    premium determination date as the non-life contingent period."
  - **Initial age** — annuitant's **age last birthday** at the premium
    determination date; for joint contracts, the **younger** annuitant; rated age
    if valued as impaired/substandard.
  - **Jumbo contract** — initial consideration **≥ $250 million** (considerations
    for contracts issued to the same contract holder within 90 days combined).
  - **Valuation Rate Buckets A–D.** No life contingencies (Table 1.C-1):
    RP ≤ 5Y → A; 5Y < RP ≤ 10Y → B; 10Y < RP ≤ 15Y → C; RP > 15Y → D.
    With life contingencies (Table 1.C-2):
    | Initial age | RP ≤ 5Y | 5Y<RP≤10Y | 10Y<RP≤15Y | RP>15Y |
    |---|---|---|---|---|
    | 90+ | A | B | C | D |
    | 80–89 | B | B | C | D |
    | 70–79 | C | C | C | D |
    | < 70 | D | D | D | D |
  - **Premium determination date** for an immediate annuity (Table 1.C-3): "Date
    consideration is determined and committed to by contract holder."
    Immaterial-change rule: a change in consideration of **less than 10% in
    present value and less than $1 million** retains the original date.
  - **Quarterly valuation rate**: **`Iq = R + S − D − E`** where R = reference
    rate for the bucket, S = spread rate, D = default cost rate, and
    **E = spread deduction = 0.25%**. For **non-jumbo** contracts the quarterly
    statutory maximum valuation interest rate is `Iq` **rounded to the nearest
    1/4 of 1%**, published quarterly by the NAIC by the third business day of the
    quarter.
  - **Daily valuation rate** (jumbo contracts): **`Id = Iq + C(d−1) − Cq`**,
    where `Iq` is the quarterly rate for the calendar quarter preceding the
    business day immediately preceding the premium determination date, `C(d−1)`
    is the daily corporate rate for the business day immediately preceding the
    premium determination date, and `Cq` is the average daily corporate rate for
    the same period used to develop `Iq`. Rounded to the nearest **1/100 of 1%**;
    published **daily** by the NAIC.
  - **Reference rate R**: weighted average of the **quarterly Treasury rates**
    (average of daily Treasury rates over the prior calendar quarter, downloaded
    from `fred.stlouisfed.org`, rounded to 2 decimals) for **2-, 5-, 10- and
    30-year** U.S. Treasuries, using **Weight Table 1**.
  - **Spread S**: weighted average of "Table X spreads" (NAIC-published current
    market benchmark spreads for the prior quarter, built like VM-20 Appendix 2.D
    Table F but averaging JP Morgan and Bank of America spreads over the quarter)
    for **WAL 2, 5, 10 and 30**, using **Weight Table 2** (Table 2 is identical to
    Table 1).
  - **Default cost D**: weighted average of **VM-20 Table A** prescribed annual
    default costs for **WAL 2, 5 and 10** using **Weight Table 3** (same
    underlying weights as Table 1, with the 10-year and 30-year columns combined
    because VM-20 default rates only go to 10 years). Table A is updated annually
    in Q2 and used from Q3.
  - **Prescribed portfolio credit quality distribution** (used to weight spreads
    and defaults): **5% Treasuries; 15% Aa (5% each Aa1/Aa2/Aa3); 40% A (13.33%
    each A1/A2/A3); 40% Baa (13.33% each Baa1/Baa2/Baa3)** — "40%/3 is used
    unrounded in the calculations."
  - **Daily corporate rate C**: weighted average of Bank of America Merrill Lynch
    U.S. corporate effective yields from FRED using **Weight Table 4**, series
    **BAMLC1A0C13YEY** (1–3Y), **BAMLC2A0C35YEY** (3–5Y), **BAMLC3A0C57YEY**
    (5–7Y), **BAMLC4A0C710YEY** (7–10Y), **BAMLC7A0C1015YEY** (10–15Y),
    **BAMLC8A0C15PYEY** (15Y+).
  - **How the weight tables are built** (useful because it defines the NAIC's own
    representative SPIA cell set): representative annuity forms per bucket —
    **Bucket A**: single life age 91 with 0 and 5-year certain, plus 5-year
    certain only. **Bucket B**: single life ages 80 and 85 with 0, 5- and 10-year
    certain, plus 10-year certain only. **Bucket C**: single life age 70 with 0
    and 15-year certain; single life age 75 with 0, 10- and 15-year certain; plus
    15-year certain only. **Bucket D**: single life ages 55, 60 and 65 with 0 and
    15-year certain, plus 25-year certain only. Annual cash flows are projected
    **assuming annuity payments are made at the end of each year**, averaged
    across forms using **the statutory valuation mortality table in effect for
    the following calendar year for individual annuities for males (ANB)**,
    summed into groups **years 1–3, 4–7, 8–15, 16–30** (PV of cash flows beyond
    year 30 discounted back to end of year 30 at the **lower of 3% and the
    30-year Treasury rate**), present-valued at Treasury rates for the group
    midpoints, and duration-weighted.
  - Weight tables are updated in **Q4** each year for the following calendar
    year; each bucket's weights sum to exactly 100%.
  - Group annuity certificates: rate determined **separately for each
    certificate**; if the payout form has not been elected, use the normal form of
    payout (or, if undeterminable, the form producing the most conservative
    rate). "The statutory maximum valuation interest rate **will not change when
    the form of payout is elected**."

### R2. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-22: Requirements for Principle-Based Reserves for Non-Variable Annuities**, and Section II "Reserve Requirements" Subsection 2
- Publisher: NAIC. Same URL as R1 (PDF pages 5, 16–21, 227–318).
- Retrieved: YES
- **Status of the broader non-variable annuity PBR framework (verified):**
  - VM-22 (PBR) is **effective for valuation dates on or after January 1, 2026**
    (VM-22 §2.B). Minimum reserve requirements for **non-variable annuity
    contracts issued 1/1/2026 and later** are those in VM-22, **except** Preneed
    Annuities, GICs, Synthetic GICs, Funding Agreements and other Stable Value
    Contracts, which follow VM-A, VM-C and VM-V.
  - **Three-year transition**: a company may elect to reserve business otherwise
    subject to VM-22 under VM-A/VM-C/VM-M/VM-V for business issued during the
    first three years after the effective date; once VM-22 PBR is applied to a
    block it must continue; all applicable blocks must be on VM-22 PBR
    prospectively starting three years after the effective date.
  - **Annuity PBR Exemption** (VM Section II, Subsection 2.D): available if the
    company has **less than $1.0 billion of "Exemption Reserves"** and (if part of
    an NAIC group with other life insurers) the **group has combined exempted
    prior-year reserves of less than $2 billion**; or if the only new in-scope
    contracts arise from election of benefits from existing VM-A/VM-C contracts
    and the company was exempt in the prior year. Statement of exemption filed
    with the domiciliary commissioner before July 1 and included with the Q2 NAIC
    filing; the commissioner may reject it before Sept. 1. Exemption reserves are
    built from the *Analysis of Increase in Reserves During the Year* exhibits,
    including **Column 6 "Life Contingent Payout (Immediate and
    Annuitizations)", line 15** for both individual and group annuities, gross of
    reinsurance. **Contracts with guaranteed living benefits (GMIBs, GMABs,
    GLWBs) are excluded from the exemption.** Exempt business follows VM-A/VM-C
    with VM-M mortality and **VM-V** valuation rates.
- **Reserve methodology relevant to SPIA:**
  - Aggregate reserve = **SR** (stochastic reserve) + **DR** for contracts that
    pass the Single Scenario Test + reserves for contracts valued under
    VM-A/VM-C/VM-M/VM-V (i.e., those passing the exclusion test and electing not
    to model). **SR = CTE70** of the scenario reserves.
  - **Reserving Categories** (aggregation is not permitted across categories
    except as specified). The **"Payout Annuity Reserving Category"** expressly
    includes: **(i) Single Premium Immediate Annuity contracts**; (ii) Deferred
    Income Annuity contracts; (iii) Structured Settlement Contracts in payout or
    deferred status; (iv) fixed income payment streams from settlement options or
    annuitizations of host contracts; (v) supplementary contracts (excluding
    contracts with no scheduled payments); (vi) certificates from non-variable
    group annuity contracts under Model #820 §5.C.2; (vii) **Pension Risk
    Transfer Annuities**. Other categories: **Longevity Reinsurance** and
    **Accumulation**.
  - Payout and Accumulation categories may be aggregated **only** if the company
    manages both in an integrated risk-management process **and** the contracts
    are managed within a single portfolio or portfolios with the same ALM
    strategy.
  - **Additional Standard Projection Amount (ASPA)** is required **for disclosure
    purposes only** under VM-31 (with a LATF referral pending to add attribution
    analysis for the 1/1/2027 manual; "the SPA is not a safe harbor").
  - **Prescribed behavior assumptions relevant to payout annuities**: the
    **annuitization rate shall be 0%** at all projection intervals; and the
    prescribed lapse table "is not applicable" "For contracts in which there is
    **no account value or surrender benefit**, such as some contracts within the
    Payout Annuity Reserving Category."
- **Prescribed mortality for the Standard Projection Amount** (VM-22 §6.C.8),
  which also serves as the "little or no data" floor under §11.B.3:
  - For **Individual Annuity contracts within the Payout Annuity Reserving
    Category other than Structured Settlement Contracts**:
    **`q_x^(2012+n) = q_x^2012 · (1 − G2_x)^n · F_x`**
    where `q_x` is from the **2012 IAM Basic Mortality Table** (VM-M §2.C), `G2_x`
    is **Projection Scale G2** (VM-M §1.J.1.c), and `F_x` is from **Table 6.8**.
  - **Table 6.8 — F_x for Individual Annuities in the Payout Annuity Reserving
    Category** (age nearest birthday):
    | Attained age x | Female | Male |
    |---|---|---|
    | ≤50–57 | 125.0% | 100.0% |
    | 58 | 120.6% | 99.0% |
    | 59 | 116.2% | 98.0% |
    | 60 | 111.8% | 97.0% |
    | 61 | 107.4% | 96.0% |
    | 62 | 103.0% | 95.0% |
    | 63 | 101.0% | 95.4% |
    | 64 | 99.0% | 95.8% |
    | 65 | 97.0% | 96.2% |
    | 66 | 95.0% | 96.6% |
    | 67 | 93.0% | 97.0% |
    | 68 | 94.4% | 98.6% |
    | 69 | 95.8% | 100.2% |
    | 70 | 97.2% | 101.8% |
    | 71 | 98.6% | 103.4% |
    | 72 | 100.0% | 105.0% |
    | 73 | 101.6% | 107.0% |
    | 74 | 103.2% | 109.0% |
    | 75 | 104.8% | 111.0% |
    | 76 | 106.4% | 113.0% |
    | 77 | 108.0% | 115.0% |
    | 78 | 108.0% | 116.0% |
    | 79 | 108.0% | 117.0% |
    | 80 | 108.0% | 118.0% |
    | 81 | 108.0% | 119.0% |
    | 82–87 | 108.0% | 120.0% |
    | 88 | 109.0% | 119.0% |
    | 89 | 110.0% | 118.0% |
    | 90 | 111.0% | 117.0% |
    | 91 | 112.0% | 116.0% |
    | 92–97 | 113.0% | 115.0% |
    | 98 | 111.4% | 113.0% |
    | 99 | 109.8% | 111.0% |
    | 100 | 108.2% | 109.0% |
    | 101 | 106.6% | 107.0% |
    | 102 | 105.0% | 105.0% |
    | 103 | 103.3% | 103.3% |
    | 104 | 101.7% | 101.7% |
    | ≥105 | 100.0% | 100.0% |
  - **Age-basis conversion** (guidance note): rates are age **nearest** birthday;
    to convert to age last birthday after applying the factor,
    **`q(x)_ALB = [q(x)_ANB + (1 − q(x)_ANB) · q(x+1)_ANB] / (2 − q(x)_ANB)`**.
  - **Structured settlements, standard lives** use a different base:
    **`q_x^(2011+n) = q_x^2011 · (1 − G2_x)^n · F_x`** with `q_x` from the
    **1983 IAM Table "a"** (VM-M §1.M) and `F_x` from **Table 6.9**, which is
    strongly graded by contract-year band (contract years 1–5, 6–10, ≥11) and runs
    at very high multiples at young ages (e.g., **300%–375%** at attained age ≤2).
  - The "with guaranteed living benefits / without guaranteed living benefits"
    **Table 6.7** factors apply to the **Accumulation** category, not to payout
    annuities.
- **Prudent estimate mortality (VM-22 §11)**: expected mortality curves are built
  from direct company experience where available, then from similar-segment data
  with margins, and finally from the §11.B.3 industry table if there is no data;
  credibility blending must return **100% of the industry table at zero
  credibility**; business segments must at minimum separate **payout annuities**
  from deferred annuities with GLBs and from deferred annuities with no
  guaranteed benefits or only GMDBs, and should separate impaired-life segments
  such as **structured settlements**. Segments where mortality must be
  **decreased** to add conservatism are called **longevity segments** — and for
  longevity segments (which is what a SPIA block is) the industry table and the
  credibility-adjusted table **must** be adjusted for mortality improvement to
  the valuation date, and future mortality improvement beyond the valuation date
  **must** be reflected if it increases the reserve (permitted but not required
  if it reduces it), based on current relevant data with a margin for
  uncertainty.

### R3. NAIC — *Valuation Manual*, Jan. 1, 2026 Edition, **VM-M Appendix M — Mortality Tables**, §1.J (2012 IAR) and §2.C (2012 IAM Basic)
- Publisher: NAIC. Same URL as R1 (PDF pages 445–446).
- Retrieved: YES
- **2012 IAR Table** (§1.J.1.a): "that **generational** mortality table developed
  by the Joint Academy/SOA **Payout Annuity Table Team** and containing rates,
  `q_x^(2012+n)`, derived from a combination of the **2012 IAM Period Table** and
  **Projection Scale G2**, using the methodology stated in the 'Application of
  the 2012 IAR Mortality Table' paragraph of **Appendix A-821** of the AP&P
  Manual."
- **2012 IAM Period Table** (§1.J.1.b): the Period Table containing **loaded**
  mortality rates for calendar year 2012, rates `q_x^2012`, shown in Appendices
  1–2 of Appendix A-821.
- **Projection Scale G2** (§1.J.1.c): "a table of **annual rates, G2_x, of
  mortality improvement by age** for projecting future mortality rates beyond
  calendar year 2012," shown in Appendices 3–4 of Appendix A-821.
- **Application formula** (§1.J.2): **`q_x^(2012+n) = q_x^2012 · (1 − G2_x)^n`**.
  "The resulting `q_x^(2012+n)` shall be **rounded to three decimal places per
  1,000**… the rounding shall occur according to the formula above, **starting at
  the 2012 period table rate**." Worked example: male age 30, `q^2012 = 0.741`;
  `q^2013 = 0.741 × (1 − 0.010)^1 = 0.73359 → 0.734`;
  `q^2014 = 0.741 × (1 − 0.010)^2 = 0.7262541 → 0.726`. **It is incorrect** to
  compute `q^2014` as `0.734 × 0.99 = 0.727` (chaining rounded rates).
- **2012 IAM Basic Table** (§2.C): "the **unloaded** mortality table underlying
  the 2012 IAM Period Table. This was developed from the **2002 experience
  table**, projected with improvement factors to 2012. The **2000-2004 Payout
  Annuity Mortality Experience Study** includes experience for immediate
  annuities, annuitizations and life settlement options of individual life
  insurance and annuity death claims. The experience analyzed **excluded
  substandard annuities, structured settlement annuities and variable payout
  annuities**. The experience represented **16 companies** over the exposure
  period."
- Also recognized in VM-M: **Annuity 2000 Mortality Table** (§1.I); **1983 Table
  "a"** (§1.M); **1994 GAR** (§1.L); **GAM-94 Basic** (§2.D).

### R4. NAIC — **Model #821**, *Model Rule (Regulation) for Recognizing a New Annuity Mortality Table for Use in Determining Reserve Liabilities for Annuities* (January 2013 publication; recommended effective date 1/1/2014)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-821.pdf
- Retrieved: YES (5 pages)
- Purpose (§2): recognizes the **1983 Table "a"**, the **1983 GAM Table**, the
  **Annuity 2000 Mortality Table**, the **2012 Individual Annuity Reserving
  (2012 IAR) Mortality Table**, and the **1994 GAR Table** for minimum standard
  of valuation for annuity and pure endowment contracts.
- §4.D: "the **2012 IAR Mortality Table shall be used** for determining the
  minimum standard of valuation for any individual annuity or pure endowment
  contract issued on or after [effective date of this amended regulation]."
- §4.E (**structured settlement carve-out**): "The **1983 Table 'a' without
  projection** is to be used… solely when the contract is based on life
  contingencies and is issued to fund periodic benefits arising from:
  (1) settlements of various forms of claims pertaining to court settlements or
  out of court settlements from **tort actions**; (2) settlements involving
  similar actions such as **worker's compensation** claims; or (3) settlements of
  **long term disability claims** where a temporary or life annuity has been used
  in lieu of continuing disability payments."
- §5 restates the generational formula `q_x^(2012+n) = q_x^2012 (1 − G2_x)^n` with
  the same rounding rule and worked example as R3.
- §3.E–§3.F define "**Period table**" (rates applicable to a given calendar year)
  and "**Generational mortality table**" (rates that decrease for a given age from
  one year to the next, based on a Period table plus a projection scale of
  mortality improvement).
- §7: 1994 GAR uses `q_x^(1994+n) = q_x^1994 (1 − AA_x)^n`.

### R5. NAIC — **Model #805**, *Standard Nonforfeiture Law for Individual Deferred Annuities* (Fall 2020 publication)
- Publisher: NAIC
- URL fetched: https://content.naic.org/sites/default/files/model-law-805.pdf
- Retrieved: YES (5 pages)
- **VERIFIED — immediate annuities are exempt.** §2.A: "This Act **shall not
  apply** to any reinsurance, group annuity purchased under a retirement plan or
  plan of deferred compensation…, premium deposit fund, variable annuity,
  investment annuity, **immediate annuity**, **any deferred annuity contract
  after annuity payments have commenced**, or reversionary annuity, nor to any
  contract which shall be delivered outside this state through an agent…"
- §2.B: Sections 3–8 do not apply to contingent deferred annuities.
- Practical consequence for modelling: a SPIA has **no nonforfeiture minimum, no
  minimum guaranteed cash value, and no statutory minimum paid-up annuity
  benefit**. This is consistent with the issuers' own statements that the
  contract is irrevocable with no cash surrender value [S4][S5][S1].

### R6. **26 U.S.C. § 72** — Annuities; certain proceeds of endowment and life insurance contracts
- Publisher: Legal Information Institute, Cornell Law School (mirror of the
  U.S. Code)
- URL fetched: https://www.law.cornell.edu/uscode/text/26/72
- Retrieved: YES (via WebFetch)
- **§72(a)** general rule: "Gross income includes any amount received as an
  annuity (whether for a period certain or during one or more lives) under an
  annuity, endowment, or life insurance contract."
- **§72(b)(1) exclusion ratio**: "Gross income does not include that part of any
  amount received as an annuity… which bears the same ratio to such amount as the
  **investment in the contract** … bears to the **expected return** under the
  contract." I.e. **exclusion ratio = investment in the contract ÷ expected
  return**.
- **§72(b)(2)** cap: "The portion… excluded from gross income… **shall not exceed
  the unrecovered investment in the contract immediately before the receipt of
  such amount**." (So the tax-free portion stops once basis is fully recovered —
  a hard switch in the projection.)
- **§72(b)(3)**: if the annuitant dies after the annuity starting date with
  unrecovered investment remaining, that unrecovered investment "shall be allowed
  as a **deduction** to the annuitant for his last taxable year."
- **§72(c)** definitions: **investment in the contract** = aggregate premiums or
  other consideration paid, minus amounts received before the annuity starting
  date to the extent excludable from gross income. **Expected return** is
  computed using **actuarial tables prescribed by the Secretary** where dependent
  on life expectancy, and as the aggregate of amounts receivable for
  fixed-installment payments.
- **§72(q)** 10% additional tax on premature distributions from non-qualified
  annuities, with exceptions including **age 59½ or older**, death, disability,
  **substantially equal periodic payments** over life/life expectancy, and
  distributions **under an immediate annuity contract**. (The immediate-annuity
  exception is why a nonqualified SPIA can be bought before 59½ without penalty —
  but see [S5], where the issuer warns that adding a *withdrawal feature* can
  retroactively trigger the 10% tax plus interest.)

### R7. IRS — **Publication 939, *General Rule for Pensions and Annuities*** (Rev. 12-2025)
- Publisher: Internal Revenue Service
- URL fetched: https://www.irs.gov/pub/irs-pdf/p939.pdf
- Retrieved: YES (85 pages)
- **Computation under the General Rule** (6 steps): (1) investment in the
  contract, including adjustments for the refund feature and the death benefit
  exclusion; (2) expected return; (3) **divide Step 1 by Step 2 and round to
  three decimal places** → exclusion percentage; (4) multiply the exclusion
  percentage by the **first regular periodic payment** → tax-free part of each
  payment; (5) × number of payments in the year; (6) remainder is taxable.
  "**The tax-free part remains the same even if the total payment increases due
  to variation in the annuity amount such as cost of living increases, or you
  outlive the life expectancy factor used.**" For annuity starting dates after
  1986 the cumulative tax-free amount **cannot exceed net cost**.
- **Age convention**: "A person's age, for purposes of figuring the expected
  return, is the age at the **birthday nearest** to the annuity starting date."
- **Expected return by payout form**:
  - **Fixed period annuity**: number of months (not less than 13) × payment.
  - **Single-life annuity**: annual payment × multiple from **Table I / Table V**.
  - **Annuity for the shorter of life or a specified period (temporary life)**:
    annual payment × multiple from **Table IV / Table VIII**.
  - **Joint and survivor annuity, identical survivor income**: annual payment ×
    multiple from **Table II / Table VI**.
  - **Joint and survivor with a reduced survivor income**: combined multiple
    (Table VI) minus the primary annuitant's own multiple (Table V) gives the
    survivor-only multiple; expected return = (primary annual payment ×
    Table V multiple) + (survivor annual payment × difference).
  - Quarterly/semiannual/annual frequency requires an adjustment to the Table
    I/II/V/VI/VIA multiples (e.g., a quarterly payout with the first payment one
    full month after the annuity starting date adjusts a 19.2 multiple by
    **+0.1** to 19.3).
- **Refund feature adjustment** (directly relevant to cash-refund and
  installment-refund SPIAs): the investment in the contract is **reduced** by the
  value of the refund feature = applicable percentage from **Table III /
  Table VII** (indexed by age and number of years guaranteed) × the **smaller of**
  net cost or total guaranteed return.
  - Worked example: at **age 65**, $21,053 buys **$100/month for life** with a
    refund feature guaranteeing return of the full $21,053. Years guaranteed =
    $21,053 ÷ $1,200 = **17.54 → 18** (rounded to nearest whole year); **Table VII
    percentage for age 65 with 18 years guaranteed = 15%**; value of the refund
    feature = 15% × $21,053 = **$3,158**; **investment in the contract adjusted =
    $17,895**. If instead only 17 years of $100/month were guaranteed, the total
    guaranteed return is $20,400, the percentage is **14%**, the refund value is
    **$2,856**, and the adjusted investment is **$18,197**.
- **Exclusion-ratio illustration (single life)**: investment in the contract
  **$10,800**, **$100/month for life**, age 65, Table V multiple **20.0** ⇒
  expected return **$24,000** (20 × 12 × $100); exclusion percentage
  **$10,800 ÷ $24,000 = 45.0%**; each year until net cost is recovered
  **$540** of $1,200 is tax-free and **$660** is included in income. With only six
  payments in a year the exclusion is **$270**.
- **Exclusion-ratio illustration (joint and survivor with reduced survivor
  income)**: investment $62,712, expected return $121,200 ⇒ exclusion percentage
  **51.7%**; on $6,000/year, **$3,102** is tax-free and **$2,898** taxable; after
  the primary's death the survivor receiving $4,200/year applies the **same
  51.7%** ⇒ **$2,171.40** tax-free, **$2,028.60** taxable.
- **Expected return example, single life**: $500/month at age nearest 66,
  Table V multiple 19.2 ⇒ expected return **$115,200**.
- **Temporary life example**: $200/month for 5 years or until death, age 65,
  Table VIII multiple **4.9** ⇒ expected return **$11,760**.
- **Disqualifying form of payment**: if the annuity starting date is after
  June 30, 1986 and the contract provides a disqualifying form of settlement,
  **such as an option to receive a lump sum in full discharge of the obligation**,
  the entire investment is treated as post-June 1986 investment (Regs. §1.72-6(d)(3)).
  *(Directly relevant to SPIAs with 100% commutation features.)*

### R8. **Treas. Reg. § 1.401(a)(9)-6** — Required minimum distributions for defined benefit plans and annuity contracts
- Publisher: Legal Information Institute, Cornell Law School (mirror of 26 CFR)
- URL fetched: https://www.law.cornell.edu/cfr/text/26/1.401%28a%29%289%29-6
- Retrieved: YES (via WebFetch)
- Distributions must be "paid in the form of **periodic annuity payments** for the
  employee's life (or the joint lives of the employee and beneficiary) or over a
  **period certain**", with **payment intervals not exceeding one year**, and
  under §1.401(a)(9)-6(a)(1) all payments **must be nonincreasing** except as
  specifically permitted.
- **Permitted increases** (§1.401(a)(9)-6(o)): annual increases not exceeding the
  percentage increase in an **eligible cost-of-living index** (§(o)(2)); "**an
  increase by a constant percentage, applied not less frequently than annually,
  at a rate that is less than 5 percent per year**" (§(o)(1)(iii)); increases from
  plan amendments (§(o)(1)(v)); for insurance contracts, increases from
  **dividends or other actuarial gains** (§(o)(3)).
  *(This is the direct constraint that keeps qualified SPIA COLA options at 1–4%
  rather than 5%+ — see [S1][S2][S5], whose COLA menus top out at 4%; [S4]'s 5%
  IPO and [S8]'s 6% COLA sit at or above the boundary and would be
  qualified-restricted.)*
- **Period certain limits** (§1.401(a)(9)-6(c)(1)): the period certain cannot
  exceed "the applicable denominator for the calendar year that includes the
  annuity starting date" from the uniform lifetime table used under
  §1.401(a)(9)-5(c); for non-spouse beneficiaries the period certain is further
  restricted based on the age difference.
- **MDIB survivor-percentage limits**: §1.401(a)(9)-6(b)(2)(ii) permits a
  **spouse** beneficiary to receive **100%** of the employee's payment
  "regardless of the difference in the ages"; §1.401(a)(9)-6(b)(2)(iii) restricts
  **non-spouse** survivor percentages by a table keyed to the age difference, with
  applicable percentages **ranging from 52% (40+ year difference) to 100% (10
  years or less)**.
- Payments must commence on or before the **required beginning date**
  (§1.401(a)(9)-6(a)(3)(i)).

### R9. SOA Research Institute & LIMRA — **2020-2024 Individual Payout Annuity Mortality Experience Study** (study highlights, © 2026)
- Publisher: Society of Actuaries Research Institute (Individual Annuity
  Experience Committee) with LIMRA
- URL fetched: https://www.soa.org/globalassets/assets/files/resources/research-report/2026/2020-24-payout-annuity-exp-study.pdf
- Retrieved: YES (5-page public "Study Highlights"; the detailed report and
  dashboards are behind the paid Experience Studies Pro package)
- Scope: **23 parent company groups / 26 individual companies**, "just over
  **80% of the industry** based on recent sales." Current study: **3,109,309
  contract-years exposed**, **$33.7 billion annual income-years exposed**,
  **143,190 deaths** over five years. Prior (2014–2019) study: 4,323,432
  contract-years, $33.6 billion income-years, 236,331 deaths. Average annual
  income rose from **$7,800 to $11,000**.
- **Headline A/E ratios (amount basis):**
  - vs. **2012 IAM Basic Table**: **99.6%** overall (down from **104.7%** in the
    prior study); **100.1% female**, **99.1% male**.
  - vs. **2012 IAM Basic projected with improvement Scale G2**: **108.4%**
    overall (prior study 108.7%); **107.5% female**, **109.4% male**.
  - i.e. **actual mortality is running about 8% heavier than 2012 IAM Basic with
    full G2 improvement** — G2 has over-projected improvement over the period.
  - By attained age group with ≥65% credibility, all groups except 65–74 had
    2012 IAM Basic G2 A/E **above 100%**; ages **65–69 = 80%** and **70–74 = 92%**.
  - By annual income band, A/E generally **decreases as income increases**:
    under 2012 IAM Basic G2, from **126%** for annual income below $2,500 to
    **91.5%** for annual income of $50,000 or more. (Classic amount-based
    antiselection/socioeconomic gradient — relevant to any SPIA model that
    segments by policy size.)
- Method: expected deaths = attained-age rate × exposure; 2012 IAM rates improved
  from **July 1, 2012 to July 1** of the applicable calendar year; tables
  developed **age nearest birthday** on **amount-weighted** experience.
- Coverage: includes immediate annuities, deferred income annuities, settlement
  options, and annuitizations of life insurance and annuity death claims;
  **certain-period-only non-life-contingent annuities are excluded**;
  **substandard annuities excluded**; **structured settlement annuities excluded**
  ("a report on structured settlement mortality experience was published in
  January 2020 covering 2005 through 2017").
- For joint lives, "no recognition is given to the secondary annuitant if alive
  while the primary annuitant is alive," because of concerns about under-reporting
  of secondary-annuitant deaths.
- Contributors include Integrity Life (Western & Southern), Massachusetts Mutual,
  Guardian Life, Brighthouse, American National, Ameriprise/RiverSource, CNO,
  EquiTrust, F&G, Midland National, and others.
- Earlier studies in the same series (not fetched): 2014–2019, 2009–2013.

### R10. **26 U.S.C. § 130** — Certain personal injury liability assignments (structured settlements)
- Publisher: Legal Information Institute, Cornell Law School
- URL fetched: https://www.law.cornell.edu/uscode/text/26/130
- Retrieved: YES (via WebFetch)
- **§130(a)**: "Any amount received for agreeing to a **qualified assignment**
  shall not be included in gross income to the extent that such amount does not
  exceed the aggregate cost of any **qualified funding assets**."
- **§130(c)** qualified assignment: any assignment of a liability to make
  **periodic payments as damages** (by suit or agreement) or as workmen's
  compensation, on account of personal injury or sickness, where the assignee
  assumes the liability from a party to the suit/agreement, and:
  - "such periodic payments are **fixed and determinable** as to amount and time
    of payment";
  - "such periodic payments **cannot be accelerated, deferred, increased, or
    decreased by the recipient**";
  - the assignee's obligation is no greater than the assignor's; and
  - the payments are excludable from the recipient's gross income under
    §104(a)(1) or (2).
- **§130(d)** qualified funding asset: "**any annuity contract issued by a
  company licensed to do business as an insurance company** under the laws of any
  State, or any obligation of the United States," which is used to fund the
  periodic payments, whose payment periods are **reasonably related** to the
  periodic payments under the assignment, which is designated as such, and which
  is **purchased not more than 60 days before and not later than 60 days after**
  the date of the qualified assignment.
- **Modelling consequence**: a structured settlement annuity is contractually a
  SPIA-like payment stream but with (a) **no commutation or acceleration
  permitted at all** (a statutory requirement, not merely a product choice), and
  (b) a **different prescribed valuation mortality basis** — 1983 Table "a"
  without projection under Model #821 §4.E [R4], and the separate Table 6.9 F_x
  structure under VM-22 §6.C.8 [R2].

### R11. Wisconsin Office of the Commissioner of Insurance — **PI-214, *Consumer's Guide to Understanding Annuities*** (R 09/2025)
- Publisher: State of Wisconsin OCI
- URL fetched: https://oci.wi.gov/Documents/Consumers/PI-214.pdf
- Retrieved: YES
- Used only for the regulator's plain-language framing: "**Immediate annuities,
  usually purchased with a single premium, provide income payments starting no
  later than one year after you pay the premium.**" "During the payout period, the
  amount of each income payment to you is generally set when the payments start
  and will not change."
- The guide's charge taxonomy (percentage-of-premium load, contract fee, market
  value adjustment, transaction fee) is written for **deferred** annuities; it
  offers no SPIA-specific charge schedule.

---

## Extracted specifications

Every line is tagged with the source it came from. Where sources disagree the
disagreement is shown explicitly.

### 1. Product identity and contract nature

- A SPIA is bought with a **single premium** and converts it immediately into a
  payment stream; income must begin within a short window: **12 months**
  [S1][S5], **one year** [S2][S3], **13 months** [S8], "no later than one year"
  [R11], "typically within a month (and never more than one year out)" [S11].
- Once issued the contract is **irrevocable**, has **no account value, no cash
  surrender value, and cannot be surrendered** [S4][S5]; "there is no
  accumulation or cash value — and, therefore, limited liquidity" [S1].
- The income option, payment frequency and all optional features are **fixed at
  issue and cannot be changed afterwards** [S2][S3][S5]. The one general exception
  is the *period certain only* option, whose certain period MassMutual permits
  the owner to lengthen or shorten after the first contract year [S1].
- Because the contract is an immediate annuity it is **outside the Standard
  Nonforfeiture Law** [R5] — there is no nonforfeiture floor, no minimum cash
  value, and no minimum paid-up benefit to model.
- Premium is reduced by **state premium tax** where applicable before income is
  determined [S6][S7][S11].
- Form numbers observed: **SPIA05 / SPIA05 (NC)** (MassMutual) [S1];
  **ICC10:30-1181, 30-1181OR** plus six endorsements (Pacific Life) [S2][S3];
  **ICC16 ENT-01 1701 / ENT-01 1701 NY** with commutation riders **ICC09 ER.01
  0901** (living) and **ICC09 ER.02 0901** (deceased) (Integrity/National
  Integrity) [S4]; **ICC11-P103 / 211-P103** (NYLIAC) [S5];
  **APO-4834 / -37 / -43 / -36 (OK)** (Nationwide, 2004) [S6].

### 2. Issue ages

| Source | Lifetime options | Period-certain-only | Notes |
|---|---|---|---|
| MassMutual RetireEase [S1] | **18–90** | max age **100** | age **nearest** birthday |
| Pacific Income Provider [S2] | max issue age **90** | — | |
| Integrity IncomeSource [S4] | individual **0–85**; joint **0–85** (one annuitant up to **90**) | **0–95** | overall stated range 0–95 |
| NYL GLI II [S5] | nonqualified **0–95**; qualified **18–89**; inherited NQ **0–95**; inherited Q **0–89**; Roth **59½–89**; inherited Roth **0–89** | — | joint annuitants 0–89 on qualified |
| Nationwide INCOME Promise [S6] | annuitants through **85**; **owners any age** | — | 2004 doc |
| Mutual of Omaha Ultra-Income [S8] | **0–85** | — | 2017 doc |
| Mutual of Omaha Income Annuity w/ Premium Return [S8] | **59–85** | — | 2017 doc |

- VM-V's own representative-cell set for the weight tables uses single-life ages
  **55, 60, 65, 70, 75, 80, 85, 91** [R1] — a reasonable default age grid for a
  reference model.

### 3. Premium limits

- Minimum: **$10,000** [S1][S4][S5][S6]; **$25,000** [S2]. Integrity adds "or the
  premium required to purchase a periodic income payout of **$100**, whichever is
  higher" [S4]. NYL notes minimums "may vary by state or payment option" [S5].
- Maximum without further underwriting/approval: **$1.5 million** [S1];
  **$2 million** for ages 0–85 and **$1 million** for ages 86+ [S2];
  **$2 million** with sub-limits (single-life-only and temporary life:
  **$1 million** to issue age 75, **$500,000** ages 76–85; joint-life-only:
  **$500,000** ages 76–85) [S4]; **$2 million** requires a large-case
  questionnaire and prior approval, aggregating multiple policies [S5];
  **$2,000,000** [S6].
- Minimum periodic payment: **$100** [S1][S4][S6]. Nationwide reserves the right
  to **reduce the payment frequency** if a payment would fall below $100 [S6].

### 4. Payout (annuity income) options — full inventory

**Single-life forms**

| Form | MassMutual [S1] | Pacific Life [S2] | Integrity [S4] | NYL [S5] | Nationwide [S6] | TIAA-CREF Life [S7] |
|---|---|---|---|---|---|---|
| Life only ("no refund") | yes | yes | yes | yes | yes | One-Life, 0 guaranteed period |
| Life with period certain | yes | up to **30 yr** | yes | **5–30 yr** | **5, 10, 15, 20 yr** | One-Life with optional guaranteed period |
| Life with cash refund | yes | yes | yes | yes | — | — |
| Life with installment refund | yes | yes (NQ only) | yes | yes | yes | — |
| Life with % of premium death benefit | — | — | — | **25% or 50%** | — | — |
| Temporary life | — | — | **5–30 yr** | — | — | — |

**Period-certain-only forms**

- **5–30 years** [S1][S4]; up to **30 years** [S2]; **5 to 20 years** [S6];
  **5 to 30 years** ("Fixed-Period Annuity") [S7].
- Qualified restriction: for qualified contracts, Pacific Life caps period certain
  at **10 years (9 years for an inherited IRA)** where needed for SECURE Act RMD
  compliance [S2]; the general regulatory constraint is §1.401(a)(9)-6(c)(1) [R8].
- MassMutual permits the certain period to be **increased or decreased after the
  first contract year**, within contract limits [S1].

**Joint forms and survivor reduction — the key design distinction**

- Pacific Life draws the cleanest line [S2][S3]:
  - **"Joint Life" options** — income reduces to **50%, 67%, or 75%** upon the
    death of **either** annuitant.
  - **"Joint and Survivor Life" options** — income reduces to **50%, 67%, or
    75%** upon the death of the **primary** annuitant only.
  - Both families are offered in Only / with Period Certain / with Cash Refund /
    with Installment Refund variants.
- MassMutual offers the same choice, named per option [S1]:
  *Reduction at Death of Annuitant* vs *Reduction at Death of Either Annuitant*,
  crossed with No Refund / Installment Refund / Period Certain, with reductions of
  **1/2, 2/3, or 3/4**.
- NYL uses a **continuous** survivor percentage: the survivor may receive
  **40%–99%** of the original income [S5]. Election rules:
  - Qualified with a **spouse** joint annuitant: reduction may be on the death of
    the **primary** annuitant **or** on the death of **either** annuitant.
  - Qualified with a **non-spouse** joint annuitant: reduction **only** on the
    death of the **primary** annuitant; if the secondary dies first, **100%**
    continues while the primary lives.
  - **Not available** on Joint Life with Cash Refund or Installment Refund, nor
    with the Changing Needs Option or Income Enhancement Option.
  - **Interaction with a certain period**: "if the first annuitant dies during the
    guaranteed payment period, the payments to the second annuitant **will not be
    reduced until the end of that period**." Restated in the footnotes as: the
    reduction takes place at "the first annuitant's death **or the end of the
    guaranteed payment period, whichever is later**."
- Nationwide (2004) offers only the two classic discrete forms: **Joint and 50%
  last survivor** and **Joint and 100% last survivor** [S6].
- TIAA-CREF Life's Two-Life contract names the asymmetry explicitly [S7]:
  *Full Benefit While Either Annuitant Survives*; ***Two-Thirds** Benefit While
  **Either** Annuitant Survives*; ***One-Half** Benefit While **Second Annuitant
  Survives First Annuitant***.
- Integrity offers "payouts for … two lives" in every family plus the same
  commutation riders, but the product summary does not publish the survivor
  percentage menu [S4].
- Joint-annuitant eligibility for IRAs: spouse, or an individual **older than or
  no more than 10 years younger** than the primary annuitant [S2].
- Refund options often force a 100% survivor benefit: NYL's Joint **Life with Cash
  Refund** is available "only if the survivor's income is **100%** of the income
  benefit while both annuitants are alive" [S5].
- Regulatory ceiling on survivor percentages for qualified money: MDIB table in
  §1.401(a)(9)-6(b)(2)(iii), **52% (40+ year age gap) to 100% (≤10 years)** for a
  non-spouse beneficiary; **100% always allowed for a spouse** [R8].

### 5. Refund-option mechanics (implementable definitions)

- **Cash refund**: on death, beneficiaries receive a **lump sum equal to premium
  less the sum of payments already made** [S1][S5]; Pacific Life states it as
  "your original purchase payment **minus** the total income payments received"
  [S3]. If total payments already equal or exceed the premium, nothing further is
  paid [S5].
- **Installment refund**: the same shortfall is paid out **as scheduled annuity
  payments** rather than a lump sum, until the premium is fully recovered
  [S1][S4][S5][S6].
- **Guaranteed period implied by a refund option** — NYL gives the exact rule
  [S5]: **guaranteed payment period = premium paid ÷ annualized income benefit
  amount**. This makes a cash-refund/installment-refund SPIA modellable as a
  life annuity with a derived certain period.
- **Percent-of-premium death benefit** (NYL only): a fixed **25% or 50% of the
  original premium** paid on death, chosen at issue; not available on qualified
  policies or in New York [S5].
- **Return of premium before the first payment**: Pacific Life pays return of
  premium if an owner or annuitant dies — **or is diagnosed with a terminal
  illness with a life expectancy of 12 months or fewer** — before the first
  payment date [S2].
- **Death within a certain period** — the beneficiary may generally elect
  remaining scheduled payments **or** a lump-sum present value [S1][S5][S6][S7].

### 6. Payment frequency and timing

- **Monthly, quarterly, semiannually, annually** — universal across
  [S1][S2][S3][S4][S5][S6][S8].
- Frequency is fixed at issue and cannot be changed [S2][S3].
- First payment: within **12 months** of issue [S1][S5]; within **one year**
  [S2][S3]; within **13 months** [S8].
- IRS expected-return multiples require a frequency adjustment for
  quarterly/semiannual/annual payouts [R7].
- VM-V's own weight-table cash-flow model assumes **annuity payments are made at
  the end of each year** [R1] — i.e., an annuity-immediate convention for the
  prescribed rate machinery.

### 7. Cost-of-living / annual increase options

| Insurer | Menu | Mechanics |
|---|---|---|
| MassMutual "Inflation Protector" [S1] | **1%, 2%, 3%, 4%** | automatic increase on each **anniversary of the annuity date**; elect at issue; **not cancellable or changeable**; **not available with Life with Installment Refund**; "may be limited or not available at all due to RMD rules" |
| Pacific Life "Inflation Protection Option" [S2][S3] | **2%, 3%, 4%** | annual increase, selected at issue; lower initial payment; only one optional feature per contract |
| Integrity "Increasing Payout Option (IPO)" [S4] | **1%, 2%, 3%, 4%, 5%** | **annually compounded** guaranteed increase |
| NYL "Annual Increase Option" [S5] | **1% to 4%** | begins **one year after the first income payment**; owner must be ≥ **59½** at first payment; not available with Changing Needs or Income Enhancement Option; available qualified and nonqualified |
| Nationwide [S6] | **1%, 2%, 3%** | applied to the fixed payment level on each contract anniversary; **irrevocable** election |
| Mutual of Omaha Ultra-Income [S8] | **up to 6%** COLA | 2017 document |
| Mutual of Omaha Income Access [S8] | **3%** inflation protection | 2017 document |

- **No CPI-linked COLA was found in any retrieved product document.** All observed
  COLA options are **fixed-percentage compound increases**. CPI-linked increases
  are permitted for qualified money by §1.401(a)(9)-6(o)(2) [R8], but no retrieved
  insurer document offers one. [unverified] Some carriers historically offered
  CPI-U-linked SPIA riders; not confirmed by any source retrieved here.
- The **5%** constant-percentage ceiling in §1.401(a)(9)-6(o)(1)(iii) [R8]
  explains why the qualified-eligible menus stop at 4% [S1][S2][S5], while
  Integrity's 5% [S4] and Mutual of Omaha's 6% [S8] sit at/above the boundary.
- Tax note: the tax-free portion of each payment is **fixed in dollars at the
  first payment** and does **not** increase with COLA increases [R7] — so a COLA
  SPIA's taxable proportion rises over time.

### 8. Other payment-shaping options

- **Pacific Life Future Adjustment Option** [S2][S3]: one-time scheduled change in
  the income level, amount and effective date chosen at issue. **Increase by up to
  3× the initial income payment**, or **decrease by up to ½ of the initial
  income payment**. Not available with Joint income options where a reduced
  benefit has been elected. **Increasing adjustment not available on qualified
  contracts.**
- **NYL Changing Needs Option** [S5]: one-time **increase of 1%–400%** (up to 5×
  the original payment) or **decrease of 1%–50%**, on or after the **3rd
  anniversary** of the income start date; date and percentage fixed at purchase;
  annuitant (younger annuitant if joint) must be **≤ 80 at purchase** and the
  adjustment must occur before the **91st birthday**; nonqualified only.
- **NYL Income Enhancement Option** [S5]: a one-time, **index-triggered** income
  increase after the **5th policy anniversary**, triggered if the **10-Year CMT**
  in the third full week of the month before the 5th anniversary is **≥ 2
  percentage points higher** than the 10-Year CMT in the third full week of the
  month before the policy date. **The increase amount is fixed at issue.** If the
  trigger is not met, the original payment simply continues. Nonqualified only;
  annuitant **≤ 75** at issue.
- **Mutual of Omaha Income Access** optional features [S8]: **10% or 20% payment
  increase based on health condition**; **50% payment increase for nursing home
  confinement**; **survivor continuation option**.
- **Mutual of Omaha Ultra-Income**: "**age rating available**" [S8] — impaired-risk
  / medically underwritten SPIA, i.e. a rated (older) age is used to increase
  income for the same premium. AG 9-C governs the valuation of such contracts and
  its valuation-rate references are superseded by VM-V [R1]; VM-V handles this by
  defining "initial age" as the **rated age** (or an equivalent rated age on a
  substandard basis) [R1].

### 9. Liquidity: commutation, withdrawals and acceleration

This is the single most variable area of SPIA design.

**No liquidity at all**
- Integrity's base contract: "There is **no cash value, no death benefit** and the
  annuity **can't be surrendered**… contract terms cannot be changed, **unless
  commutation is available and elected**" [S4].
- TIAA-CREF Life One-Life / Two-Life: "**no lump sum payment is available during
  the lifetime of annuitant(s)**, or if the annuitant dies after the end of the
  guaranteed period" [S7].

**Partial commutation of the certain portion (most common design)**
- MassMutual [S1]: withdrawals only on options that include a period certain.
  *Period Certain Only* → one **full or partial** withdrawal per year after
  year 1. *Single or Joint Life with Period Certain* → one **partial** withdrawal
  per year after year 1, which **reduces the period certain payments but not the
  lifetime payments after the certain period ends**. Minimum withdrawal
  **$5,000**; maximum = **PV of all remaining period certain payments less
  surrender charges**; remaining payments must stay ≥ $100. **Surrender charge
  8/7/6/5/4/3/2/1/0% in contract years 2–10+.** Not permitted in **Oregon**.
- Integrity [S4]: **Living Commutation Rider** — lump sum of **10%–90% of the
  present value** of all remaining payouts, available **after the first contract
  year**. **Deceased Commutation Rider** — beneficiary cashes out remaining
  **certain** payouts on the death of the annuitant (or last-to-die joint
  annuitant). Excluded from: **life only**, **temporary life**, and **certain
  periods shorter than 10 years**; currently unavailable in **NY** (an
  accompanying W&S description also cites **Oregon**).
- Pacific Life [S2][S3]: **Withdrawal of Guaranteed Income Payments** — up to
  **100% of the PV of remaining guaranteed income payments**, nonqualified only,
  owner ≥ **59½**, **not in Oregon**, **not available with Life Only / Joint Life
  Only / Joint and Survivor Life Only**, **no limit on the number of
  withdrawals**, and — critically — **"with the exception of the Period Certain
  option, if you are still living at the end of the period when your guaranteed
  income payments would have stopped, Pacific Life will resume income payments
  until your death."** An **interest-rate adjustment applies**.
- NYL [S5]: **Up to 100% Cash Withdrawal** of the discounted value of remaining
  guaranteed payments (nonqualified; Life with Cash Refund / Installment Refund /
  Period Certain; age ≥ 59½; **once** per policy). Future payments through the end
  of the guaranteed period are reduced **by the withdrawal percentage elected**;
  **full payments resume for life** if the annuitant is alive at the end of the
  guaranteed period.

**Commutation against life expectancy (rare)**
- NYL **30% Cash Withdrawal** [S5]: **30% of the discounted value of the remaining
  payments expected to be paid, based on the annuitant's life expectancy at
  purchase**. Exercisable on the **5th, 10th or 15th anniversary** of the first
  income payment, or on proof of a significant nonmedical financial loss. Once
  exercised, **all future income payments drop by 30% permanently**. **Not
  available after the annuitant's life expectancy.** Works on **Life Only** and
  **Life with Percent of Premium Death Benefit** (nonqualified), and on qualified
  Life Only / Cash Refund / Installment Refund / 5–30-year options. Mutually
  exclusive with the 100% Cash Withdrawal feature.

**Payment acceleration (borrowing forward from the schedule, no PV discount)**
- Pacific Life [S2][S3]: after **age 59½** and **≥ 5 years** of monthly payments,
  take **3× or 6×** the normal monthly payment as a lump sum; payments resume in
  the **4th** or **7th** month; **max 2 uses**; at least one normal payment
  between uses; available with **all** income options. Six-month waiting period in
  each direction versus the withdrawal feature.
- NYL Payment Acceleration [S5]: nonqualified, monthly payments, after 59½ —
  receive the next payment plus **five** subsequent payments at once, then no
  payments for five months; usable **two times**.

**Commuted-value formulas actually published**
- TIAA-CREF Life gives an explicit fixed-account formula [S7]: "**For the fixed
  account, the commuted value is the sum of payments less the interest that would
  have been earned from the effective date of the commuted value calculation to
  the date each payment would have been made.**" For variable accounts the
  commuted value uses an effective annual rate of **4%** (the AIR). The related
  "Current Value" (free-look refund) is "the present value of the future annuity
  payments … based on **the age of the annuitant(s), if alive; the remaining
  guaranteed period, if any; the frequency of payment; and the mortality tables
  used to determine the initial amount of annuity payments**."
- NYL discloses only the driver, not the formula [S5]: an **Interest Rate Change
  Adjustment** that "will increase or decrease the withdrawal amount based on the
  change in interest rates, as measured by the **10-Year Constant Maturity
  Treasury (CMT) Index**, between the time you purchase your policy and the time
  you elect to receive the cash withdrawal."
- Pacific Life discloses only that "**an interest-rate adjustment will apply**"
  [S2].
- MassMutual's cap is "**the present value of all remaining period certain
  payments, less any surrender charges**", with the surrender charge grade shown
  in §1 above [S1].
- **No insurer document retrieved publishes the actual discount-rate formula** —
  see Gaps.

**Tax friction on commutation**
- Withdrawals under acceleration/cash-withdrawal features are reported **as fully
  taxable** [S5].
- A contract that provides "an option to receive a lump sum in full discharge of
  the obligation" is a **disqualifying form of payment or settlement** under
  Regs. §1.72-6(d)(3), pushing the entire investment into post-June-1986
  treatment [R7].
- If a policy with a withdrawal feature is bought before 59½ and the feature is
  exercised within five years of the first annuity payment, a **10% additional tax
  plus interest may be imposed retroactively** on payments received before 59½
  [S5]; the §72(q) immediate-annuity exception is what is at risk [R6].

### 10. Charges and fees

- **MassMutual: "there are zero fees"** on RetireEase; the only charge is the
  **surrender charge on withdrawals from period-certain options** (8/7/6/5/4/3/2/1%
  in contract years 2–9, 0% from year 10) [S1].
- No explicit charge schedule is published by Pacific Life [S2][S3], Integrity
  [S4], NYL [S5] or Nationwide [S6]. In a fixed SPIA, expenses and profit are
  loaded implicitly into the **payout rate**, not disclosed as separate charges.
  [unverified] This is the general market convention for fixed SPIAs.
- The **only** explicit asset-based charges found are on the **variable** immediate
  annuity [S7]: M&E **max 1.00% / current 0.40%**, administrative expense
  **0.20%**, total separate account **max 1.20% / current 0.60%**, no annual
  contract fee.
- **State premium tax** may be deducted from the premium before income is
  determined [S6][S7][S11].
- Interest-rate adjustments on commutation [S2][S5] are a charge-like mechanism
  but are not quantified in any retrieved document.

### 11. Payout-rate anchors

Treat all of these as weak. No insurer- or regulator-published payout-rate table
was successfully retrieved with numbers in it.

- **New York Life** publishes **weekly** payout rates as the "**annualized payout
  as percent of total premium**", "**based on the life with cash refund option for
  a policy purchased by a male annuitant with $100,000**", by **Age × Single Life
  × Joint Life**, with the note that the rates "include both interest and return
  of principal" and that female payouts are lower except in **Montana**, where
  rates are unisex. The table itself is JavaScript-rendered and could not be
  captured [S10].
- **Pacific Life hypothetical illustrations** (Feb 2024 client guide, explicitly
  illustrative) [S3]:
  - Joint Life Only, both age 65: $230,856 → $1,200/month ⇒ **≈ 6.24%** annualized.
  - Life with 10-Year Period Certain, age 69: $281,379 → $20,000/year ⇒ **≈ 7.11%**.
  - Single Life with 3% Inflation Protection, male 65: $204,736 → ≈ $900/month
    initially, ≈ $1,600/month after 20 years ⇒ **≈ 5.28%** initial.
- **Broker aggregator survey, July 2026** [S9] — **low reliability**: best quote
  per $100,000, life only — male 65 **$664/mo (7.97% annualized)**, female 65
  **$635/mo**, joint 65 **$583/mo**; male 55 $575, 60 $618, 70 $754, 75 $882,
  80 $1,059. Carrier spread best-to-worst **≈ 5–6%**; the site claims a 10-year
  period certain costs "**~3% of income**".
- Structural regularities visible across all anchors and consistent with theory:
  payout rate rises with age; female < male at the same age; joint < single;
  adding a certain period or refund guarantee reduces income; adding a COLA
  materially reduces the initial payment. [S3][S9][S10] and, qualitatively,
  [S1][S2][S4][S5].
- NYL warns of a genuine non-monotonicity to watch for in a pricing model: "there
  are limited situations (**primarily younger annuitants**) where the **same or
  essentially the same income payment** is available for longer guarantee periods
  or cash refund options" [S5] — i.e., for young annuitants the life-contingent
  and certain streams nearly coincide.

### 12. Valuation basis (statutory)

- **Reserve method**: CARVM — "the path of future guaranteed benefits with the
  highest present value is used to set policy reserves" for SPIAs, deferred
  annuities in payout and supplementary contracts [S7]; VM-V §1.A.1 confirms the
  maximum rate applies "**in the CARVM and for some contracts, CRVM**" [R1].
- **Maximum valuation interest rate** for immediate annuities issued after
  Dec 31, 2017: **VM-V §1**, `Iq = R + S − D − E` with **E = 0.25%**, bucketed
  A–D by reference period and initial age, rounded to the nearest **¼%** quarterly
  for non-jumbo contracts and to **1/100%** daily for **jumbo** contracts
  (initial consideration ≥ **$250 million**) [R1]. See R1 for the full input
  definitions, the prescribed **5/15/40/40 Treasury/Aa/A/Baa** credit-quality mix,
  and the FRED series names.
- **Valuation mortality**: **2012 IAR** generational table for individual annuity
  contracts, `q_x^(2012+n) = q_x^2012 (1 − G2_x)^n`, rounded to three decimals per
  1,000 starting from the 2012 Period rate [R3][R4]; **Annuity 2000** for older
  issues [R4][S7]; **1983 Table "a" without projection** for structured
  settlements and similar tort/workers'-comp/LTD-commutation annuities [R4].
- **PBR**: **VM-22** applies to non-variable annuities for **valuation dates on or
  after 1/1/2026**, with a **three-year transition** election and a
  **$1.0 billion / $2.0 billion** small-company exemption [R2]. SPIAs sit in the
  **Payout Annuity Reserving Category**, alongside DIAs, structured settlements,
  supplementary contracts and pension risk transfer annuities; **SR = CTE70**;
  **annuitization rate is prescribed at 0%**; the prescribed lapse table does not
  apply to contracts with no account value or surrender benefit [R2].
- **Prescribed mortality for the Standard Projection Amount / "no data" floor**:
  **2012 IAM Basic × Scale G2 × F_x** with the payout-annuity F_x table
  reproduced in full at R2 (Table 6.8); structured settlements use **1983 IAM
  Table "a" × G2 × F_x** with Table 6.9 [R2].
- **Longevity-segment improvement requirement**: for a SPIA block (a "longevity
  segment"), the industry table and the credibility-adjusted table **must** be
  brought forward for mortality improvement to the valuation date, and future
  improvement beyond the valuation date **must** be reflected if it increases the
  reserve [R2].
- **Experience calibration**: the industry is running about **99.6% of 2012 IAM
  Basic** but **108.4% of 2012 IAM Basic projected with G2** on an amount basis
  over 2020–2024 — i.e., G2 has over-projected improvement — with strong
  gradients by attained age (65–69 at 80%, 70–74 at 92%) and by policy size
  (126% below $2,500 annual income down to 91.5% at $50,000+) [R9].

### 13. Taxation

**Nonqualified SPIA**
- Each payment splits into an excludable return of investment and a taxable
  interest element, at **exclusion ratio = investment in the contract ÷ expected
  return** [R6][R7], mirrored in insurer language: "a portion of each annuity
  payment will be tax-free, until the total amount of non-taxable income you've
  received equals the amount of your single purchase payment" [S1]; "your tax
  liability will be limited to the earned interest portion" [S3].
- **Expected return** is computed with **IRS actuarial tables** (Tables I–VIII,
  age nearest birthday), by payout form: fixed period = months × payment; single
  life = annual payment × Table I/V multiple; temporary life = annual payment ×
  Table IV/VIII multiple; joint & survivor identical = Table II/VI multiple;
  joint & survivor reduced = (primary payment × Table V) + (survivor payment ×
  [Table VI − Table V]); with a frequency adjustment for non-monthly payouts [R7].
- **Refund feature adjustment**: investment in the contract is reduced by
  **Table III/VII percentage × min(net cost, total guaranteed return)** — worked
  example at age 65 with 18 guaranteed years gives a **15%** factor, reducing a
  $21,053 investment to **$17,895** [R7]. **This is the tax adjustment that must
  be applied to cash-refund and installment-refund SPIAs.**
- The **tax-free amount per payment is fixed at the first payment** and does not
  change with COLA increases or with living past life expectancy [R7]; the
  exclusion **stops** once unrecovered investment reaches zero [R6 §72(b)(2)];
  any unrecovered investment at death is a **deduction on the final return**
  [R6 §72(b)(3)].
- **§72(q) 10% penalty** does not apply to distributions "under an immediate
  annuity contract" or after 59½ [R6]; insurers restate this [S11], but NYL warns
  that **adding a withdrawal feature can retroactively expose pre-59½ payments to
  the 10% tax plus interest** [S5].
- A **full-commutation option** is a "disqualifying form of payment or settlement"
  under Regs. §1.72-6(d)(3) [R7].
- Nonqualified contracts may also attract the **3.8% net investment income tax**
  [S2].

**Qualified SPIA**
- Payments are generally fully taxable as ordinary income; the SPIA is the
  distribution vehicle rather than a tax shelter — "There is no additional tax
  deferral benefit provided when an annuity contract is used to fund a
  tax-qualified retirement plan or an IRA" [S1].
- Annuity payments **satisfy the RMD** for the annuitized amount but **cannot be
  aggregated** with other IRA assets for RMD purposes [S2].
- Payments must be **periodic, at intervals ≤ 1 year, and nonincreasing** except
  for the permitted increases; **constant-percentage increases must be < 5% per
  year**; COLA increases must track an eligible cost-of-living index; insurance
  contracts may increase from dividends/actuarial gains [R8].
- **Period certain length** is capped by the uniform lifetime table denominator at
  the annuity starting date [R8], operationalized by Pacific Life as **≤ 10 years
  (9 for inherited IRAs)** on qualified contracts [S2].
- **Survivor percentage** for a non-spouse beneficiary is capped by the MDIB table
  (**52% at a 40+ year age gap** up to **100% at ≤ 10 years**); a spouse may
  always take 100% [R8]. Insurers implement this as the non-spouse
  reduce-only-on-primary-death restriction [S5] and the "no more than 10 years
  younger" joint-annuitant rule [S2].
- On the owner's death, remaining payments may be **shortened to fit the 10-year
  post-death distribution period** under §401(a)(9) or the eligible designated
  beneficiary's life expectancy [S1]; NYLIAC will **commute** all future
  guaranteed payments if the remaining certain period exceeds the beneficiary's
  Single Life Table expectancy [S5].
- **Installment refund is not available on qualified contracts** at Pacific Life
  [S2]; the **Percent of Premium Death Benefit** and the **Changing Needs /
  Income Enhancement** options are nonqualified-only at NYL [S5]; an **increasing**
  Future Adjustment is nonqualified-only at Pacific Life [S2].

### 14. Structured settlement annuities (related product family)

- Contractually a SPIA-shaped payment stream, but under **IRC §130** the periodic
  payments must be "**fixed and determinable as to amount and time of payment**"
  and "**cannot be accelerated, deferred, increased, or decreased by the
  recipient**" — so **no commutation or acceleration of any kind is permissible**,
  unlike a retail SPIA [R10].
- The funding asset must be an **annuity contract issued by a state-licensed
  insurance company** (or a U.S. obligation), with payment periods reasonably
  related to the assignment, purchased within **60 days before or after** the
  qualified assignment [R10].
- **Valuation mortality is different**: **1983 Table "a" without projection** for
  tort settlements, workers'-compensation settlements and LTD-claim commutations
  [R4 §4.E]; under VM-22 the prescribed Standard-Projection basis is **1983 IAM
  Table "a" × Scale G2 × F_x** with a **contract-year-banded** F_x table running
  at very high multiples at young ages (e.g. 300%–375% at attained age ≤ 2) [R2].
- Structured settlements sit in the **same VM-22 Payout Annuity Reserving
  Category** as SPIAs [R2] and in the **same VM-V scope** for maximum valuation
  interest rate [R1], but are **excluded from the SOA payout annuity experience
  study** and studied separately (a structured settlement mortality report
  covering 2005–2017 was published in January 2020) [R9]. They were also excluded
  from the experience underlying the **2012 IAM Basic** table [R3].
- VM-22 §11 explicitly names structured settlements as an example of an
  impaired-lives segment requiring its own mortality assumption [R2].

---

## Variations across insurers

1. **Survivor-reduction trigger is the sharpest structural variation.** Three
   patterns exist:
   - Explicit two-family design where the trigger is part of the option name —
     Pacific Life's *Joint Life* (reduce on **either** death) vs *Joint and
     Survivor Life* (reduce on the **primary** death) [S2][S3], and MassMutual's
     *Reduction at Death of Annuitant* vs *Reduction at Death of Either
     Annuitant* [S1].
   - Continuous survivor percentage with tax-driven trigger rules — NYL's
     **40%–99%**, where a **spouse** joint annuitant on a qualified policy may use
     either trigger but a **non-spouse** may use only the primary-death trigger
     [S5].
   - Legacy discrete forms with only "last survivor" semantics — Nationwide's
     Joint and 50% / 100% last survivor [S6].
   For a reference model, **Pacific Life's design is the most representative and
   the cleanest to implement**: two triggers × three percentages (50/67/75) ×
   four guarantee variants.

2. **Survivor percentage menus.** 50%/67%/75% [S2]; 1/2, 2/3, 3/4 [S1]; 2/3 or
   1/2 by contract form [S7]; 50%/100% [S6]; continuous **40%–99%** [S5]. The
   50 / 66⅔ / 75 / 100 set covers essentially the whole market.

3. **Certain-period range.** 5–30 years is now standard [S1][S2][S4][S5][S7];
   the older Nationwide product caps at 20 [S6]. Qualified money is separately
   capped near 10 years by RMD rules [S2][R8].

4. **COLA menus.** 1–4% is the modal design [S1][S5]; 2–4% [S2]; 1–3% [S6];
   1–5% compound [S4]; up to 6% [S8]. **No CPI-linked option was found.** The
   **1–4% fixed compound** menu is the representative design because it works for
   both qualified and nonqualified money under the <5% constant-percentage rule
   [R8].

5. **Liquidity is where designs diverge most.**
   - *None*: Integrity's base contract [S4]; TIAA-CREF Life's life-contingent
     contracts during the annuitant's lifetime [S7].
   - *Certain-period-only, charge-bearing*: MassMutual — one withdrawal a year,
     $5,000 minimum, capped at the PV of remaining certain payments, with an
     **8%-to-1% nine-year surrender charge** [S1]. This is the only published
     SPIA surrender-charge schedule found.
   - *Percentage-band commutation rider*: Integrity — **10%–90% of PV**, after
     year 1, excluded on life-only/temporary-life/short certain periods [S4].
   - *Full PV commutation with income resumption*: Pacific Life — up to **100% of
     PV**, unlimited number of withdrawals, and (except on pure Period Certain)
     **income resumes for life at the end of the original guaranteed period**
     [S2][S3]. NYL's 100% Cash Withdrawal behaves the same way [S5].
   - *Commutation against life expectancy on a life-only contract*: **only NYL**,
     via the **30% Cash Withdrawal**, with a permanent 30% haircut to all future
     income [S5]. This is the most unusual feature found in the survey.
   - *Payment acceleration (no PV discount)*: Pacific Life (3× or 6×, twice)
     [S2]; NYL (6 months at once, twice) [S5].
   - **Oregon** is repeatedly carved out of withdrawal features [S1][S2]; **New
     York** is carved out of the Integrity commutation riders [S4] and of NYL's
     Percent of Premium Death Benefit [S5].

6. **Death benefits before income starts.** Only Pacific Life publishes a
   pre-first-payment return-of-premium death benefit, and extends it to a
   **terminal-illness diagnosis with ≤ 12 months' life expectancy** [S2].
   NYL uniquely offers an explicit **25%/50% of premium** death benefit as a
   payout option [S5]; Mutual of Omaha markets a whole product ("Income Annuity
   with Premium Return") around return of premium on death [S8].

7. **Temporary life** (income only while alive, for a fixed term, with **no** death
   benefit) was found at only one insurer — **Integrity IncomeSource**, 5–30 years
   [S4]. It is tax-recognized (IRS Tables IV/VIII exist precisely for it [R7]) but
   is rare in the retail market.

8. **Impaired-risk / medically underwritten SPIAs.** Only Mutual of Omaha's
   Ultra-Income advertises "**age rating available**" [S8], plus Income Access's
   **10%/20% payment increase based on health condition** and **50% increase for
   nursing home confinement** [S8]. AG 9-C and VM-V's "rated age" definition
   confirm this is a recognized statutory category [R1].

9. **Index-linked income features.** Only NYL's **Income Enhancement Option** ties
   income to a market index (10-Year CMT, ≥ 200 bp rise, one-time, amount fixed at
   issue) [S5]. No retrieved SPIA had caps, participation rates, spreads, buffers
   or floors — those belong to indexed/RILA designs, not to SPIAs.

10. **Minimum premium** clusters at **$10,000** [S1][S4][S5][S6]; Pacific Life is
    the outlier at **$25,000** [S2]. **Maximum without approval** clusters at
    **$2 million** [S2][S4][S5][S6], with MassMutual at **$1.5 million** [S1].

**Most representative design for a reference model.** Take MassMutual RetireEase
[S1] and Pacific Income Provider [S2] as the joint template:
issue ages 18–90 (age nearest); minimum premium $10,000–$25,000, maximum
$1.5–2 million; monthly/quarterly/semiannual/annual payments beginning within
12 months; option set = {life only, life with period certain 5–30, life with cash
refund, life with installment refund, period certain only 5–30} × {single, joint
reduce-on-either-death, joint reduce-on-primary-death} with survivor percentages
{50%, 66⅔%, 75%, 100%}; optional fixed compound COLA of 1–4%; no explicit charges;
liquidity limited to commutation of the certain portion at the PV of remaining
certain payments, subject to a declining surrender charge and an interest-rate
adjustment; no cash value and no nonforfeiture floor.

---

## Gaps and caveats

1. **No specimen contract was retrieved.** Every primary source is a fact sheet,
   brochure, product summary or prospectus. The most contractually precise
   documents obtained are the Integrity product summary [S4], the NYL fact sheet
   [S5] and the TIAA-CREF Life prospectus [S7]. A true SPIA policy form (with the
   settlement-option tables, the guaranteed purchase-rate basis, and the
   commuted-value definition) was **not** located on any insurer or SEC domain
   during this research.

2. **No published payout-factor tables or guaranteed annuity purchase rates.**
   None of the retrieved documents disclose the mortality table, interest rate, or
   expense loading used to convert premium into income. Fixed SPIA pricing is
   entirely embedded in the quoted payout rate. The best available proxies are
   the Feb-2024 hypothetical illustrations in [S3] and the low-reliability broker
   survey in [S9]. NYL's rate table [S10] would have been the ideal anchor but is
   JavaScript-rendered.

3. **No commutation / interest-rate-adjustment formula is published by any fixed
   SPIA issuer.** Pacific Life says only "an interest-rate adjustment will apply"
   [S2]; NYL identifies the **10-Year CMT** as the driver but gives no formula
   [S5]; MassMutual caps the withdrawal at "the present value of all remaining
   period certain payments" without stating the discount rate [S1]. The only
   explicit formula found anywhere is TIAA-CREF Life's (simple-interest discount
   on the fixed account; 4% AIR on variable accounts) [S7], and that is a 2008
   variable contract. **A reference model will have to assume a commutation
   discount basis** — flagging it as [unverified] is appropriate.

4. **Exclusion-ratio illustration** — the only worked examples in this file come
   from **IRS Publication 939** [R7], not from an insurer illustration. No
   insurer document retrieved contained a numeric exclusion-ratio illustration;
   several describe the concept qualitatively [S1][S3][S6].

5. **Mutual of Omaha Ultra-Income specifics are from a 2017 producer overview**
   [S8]; the current brochure (`lc3146.pdf`) 404s and the product page's host
   (`webprod3.mutualofomaha.com`) does not resolve. The 6% COLA and "age rating"
   facts should be re-verified before being relied on.

6. **Nationwide INCOME Promise [S6] is a 2004 document** and TIAA-CREF Life's
   prospectus [S7] is a **2008** filing. Neither should be treated as a
   currently-sold product spec; they are included for design vocabulary and
   contractual precision respectively.

7. **Integrity commutation state exclusions**: the retrieved product summary [S4]
   names **NY** only; a Western & Southern web description surfaced in search also
   named **Oregon**, but that description was read only through a search-result
   snippet and the underlying page was **not** independently fetched — treat the
   Oregon exclusion as [unverified].

8. **VM-22 is in its first year of effectiveness** (valuation dates on or after
   1/1/2026) with a three-year transition and a pending LATF directive on
   Standard Projection Amount attribution analysis targeted at the 1/1/2027
   manual [R2]. Numbers and structure should be re-checked against the current
   edition each January.

9. **NAIC-published rate inputs are not reproduced here.** VM-V's Weight Tables
   1–4, the Table X spreads, the VM-20 Table A default costs, and the actual
   published quarterly/daily maximum valuation interest rates all live on the
   **Industry tab of the NAIC website** and were not retrieved [R1]. Only the
   algorithm and its inputs' definitions are captured.

10. **2012 IAM Period / 2012 IAM Basic rate tables and Scale G2 rates were not
    retrieved.** They live in **Appendices 1–4 of Appendix A-821 of the AP&P
    Manual** [R3][R4]; only the generational application formula and its rounding
    rule are captured here. The single verified numeric datapoint is the worked
    example: male age 30, `q^2012 = 0.741` per 1,000, `G2_30 = 0.010` [R3][R4].

11. **VM-22 Table 6.9 (structured settlement F_x) is only partially reproduced**
    here (attained ages ≤ 2 through 26 of a much longer table) [R2].

12. **SOA payout annuity study detail is paywalled** — only the free 5-page
    highlights were retrieved [R9]. A/E ratios by contract type, refund feature,
    benefit class, annuitant status and contract-year group exist in the paid
    Experience Studies Pro package and were not obtained.

13. **State premium tax rates were not researched.** Several sources note premium
    tax may be deducted [S6][S7][S11] but none quantify it.

14. **Participating / dividend-paying SPIAs** are mentioned once [S11] but no
    such product's mechanics were located.

15. **Sources noted but not fetched**, listed so a follow-up pass can target them:
    NAIC **Model #820** (Standard Valuation Law), **AG 9-B** and **AG 9-C** in
    VM-C, **AP&P Manual Appendix A-821** (the actual 2012 IAM/G2 rate tables),
    the SOA **2014–2019** and **2009–2013** payout annuity studies, the SOA
    **structured settlement mortality report (Jan 2020, 2005–2017)**, and the
    American Academy of Actuaries **"VM-22 In Brief"** issue brief at
    `actuary.org/wp-content/uploads/2021/04/VM-22_In-Brief.pdf`.
