# Product Specification

**Status:** Draft, 2026-08-04 (cited sources accessed 2026-08-04, except the AP&P Manual
appendix items **R151–R157**, accessed 2026-08-06 — see `sources.md`).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/registered-index-linked-annuity.md` — were
extracted from the cited document. [REG-R#] tags resolve against the **shared
cross-product numbering space, which now runs R1–R157** with most of the
**R73–R149** block unused, curated at
`references/regulatory-and-actuarial-references.md`: R1–R34 are the life-origin
entries (research provenance `_research/regulatory-actuarial.md`), R35–R72 the
annuity-specific entries (`_research/regulatory-actuarial-annuities.md`). It is one
numbering space, not two. Values marked **[std]** are standardizations introduced for
the reference implementation; each [std] table row carries a footnote giving the
rationale and the observed range across insurers. Facts the research file could not
verify are flagged [unverified].

The implementation anchor for mechanics is the **Brighthouse Shield Level II 6-Year
Annuity** Rule 424(b)(3) prospectus, whose Appendix F carries the complete AG 54-era
interim value algebra and the worked proportional-withdrawal example [S2].

---

## Product overview and market role

A RILA (the NAIC prefers **ILVA**, "index-linked variable annuity", precisely to signal
that a compliant design is a variable annuity first [R2] [REG-R44]) is a deferred annuity under
which purchase payments are allocated to index-linked options whose returns "(both gains
and losses) are based at least in part on the performance of an index or other benchmark
… over a set period of time ('crediting period')" [R1]. Upside is limited by **cap rates**
and/or **participation rates** ("limits on gains"); downside by **buffers** or **floors**
("limits on losses") [R1]. A buffer absorbs the first *b* percentage points of index loss
and passes the excess through to the contract holder; a floor caps the holder's loss at
*f* and leaves the insurer with the tail [R1].

The index-linked options sit in a **non-unitized separate account** [S4] [R2]. Of the ILVA
separate accounts the American Academy of Actuaries surveyed, none are SEC-registered, all
are non-unitized, and they may be insulated or non-insulated; statutory accounting is
separate account, U.S. GAAP is general account, and RBC splits C0–C1 general account /
C3–C4 separate account [R6]. RILAs are themselves SEC-registered securities — unlike fixed
indexed annuities, which returned to state regulation after Rule 151A was vacated and
Dodd-Frank §989J enacted [REG-R53]. The SEC recorded RILA sales of **$47.4 billion in
2023**, 15% above the prior year and more than five times the 2017 level ($9.2 billion),
with Q4 2023 the first quarter in which RILA sales surpassed variable annuity sales
[R1, citing LIMRA](#uslib-registered_index_linked_annuity-r1).

The distinguishing modeling fact: between term start and term end the contract has **no
account value in the ordinary sense**. Every transaction — withdrawal, surrender, death
claim, annuitization, transfer, fee deduction — settles at an **Interim Value**, a daily
mark of a hypothetical replicating portfolio priced with an option-pricing model
[R2] [S2] [S4] [S6]. That is contractual, not a modeling refinement (see
`technical-notes.md`).

---

## Representative specification

### Contract identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Individual single-premium deferred index-linked separate account annuity | [S1] [S2] |
| Chassis | Brighthouse Shield Level II 6-Year design | [S2]; selection **[std]** (1) |
| Account structure | Non-unitized separate account for index-linked options; general account for Fixed Account and Holding Account | [S2] [S4] [R2] [R6] |
| Premium structure | Single premium; no subsequent purchase payments | [S1] [S2]; scope **[std]** (2) |
| Owner / annuitant issue ages | 0–85 | [S1] [S2] |
| Minimum purchase payment | $25,000 (prior approval below $25,000 or at/above $1,000,000) | [S1] [S2] |
| Minimum account value | $2,000 (below this a withdrawal request is treated as a full withdrawal) | [S1] [S2] |
| Minimum allocation to one index-linked option | $500 | [S1] |
| Minimum partial withdrawal | $500 | [S1] |
| Maturity Date (forced annuitization) | Contract anniversary after the oldest Owner's 90th birthday, or 10 years from issue, whichever is later | [S2] |
| Free look | 10 days after receipt (longer in some states) | [S1] [S2] |
| Anchor model point | Male 60, single premium $100,000, 100% allocated to one 6-year option, S&P 500 price return, 10% buffer, Cap crediting | **[std]** (3) |

Footnotes to [std] rows:

1. The research file's own conclusion: the best single reference target is a
   single-premium, 6-year-chassis buffered RILA with 1/3/6-year terms, Cap / Step / Edge
   crediting, a 7-7-6-5-4-3-0 withdrawal charge above a 10% free amount, a
   return-of-premium GMDB, no explicit asset charge and an AG 54 interim value —
   "essentially the Brighthouse Shield Level II design" [S2], matching AG 54's literal
   definitions [R2] and the Academy's worked example structure [R6].
2. Observed: single premium [S1] [S2]; flexible premium with a contribution cut-off at owner
   age 86 and $500/$50 minimum additional contributions [S4]; flexible-premium combination
   contract with variable subaccounts [S3]. Single premium removes premium-persistency
   modeling from a product whose difficulty lies entirely in the interim value.
3. Pure modeling choice. Age 60 sits inside the band receiving the return-of-premium death
   benefit (owners 80 or younger [S2]) and inside the standard issue-age range [S1] [S2].
   S&P 500 price return appears in the index menu of every source product whose menu was
   captured in the research file [S1] [S2] [S3] [S4].

### Index-linked option menu

| Parameter | Representative value | Basis |
|---|---|---|
| Term lengths offered | 1, 3, 6 years (point-to-point) | [S1] [S2] [S3] [S4] [S5]; 2-year dropped **[std]** (4) |
| Buffers ("Shield Rates") offered | 10%, 15%, 25% | [S1] [S2] |
| Representative buffer | 10% | universal across insurers [S1]–[S6] [R1]; pick **[std]** (5) |
| Indices | S&P 500, Russell 2000, MSCI EAFE, Nasdaq-100 — all **price return** | [S2] |
| Rate crediting types | Cap Rate; Step Rate; Step Rate Edge | [S2] |
| Floor strategies | Not offered on this chassis (documented as a variation) | [S1] [S2]; contrast [S5] |
| Reallocation | Only during the Transfer Period — the 5 calendar days following the Contract Anniversary coinciding with a Term End Date | [S1] [S2] |
| Default at Term End | Automatic renewal into the same option at the new declared rate unless the owner elects otherwise; 30 days' advance notice | [S1] [S2] |

4. Observed term menus: 1/3/6 [S1] [S3] [S4] [S5]; **1/2/3/6** [S2]; **1 and 6 only** [S6];
   the Academy survey reports one, two, three or six years [R6]. The 2-year term is unique
   to [S2] among the retrieved sources and is dropped to hold the menu at the industry mode.
5. Observed buffer menus: 10/15/25 [S1] [S2]; 5/10/15/20/**100** [S3]; 10/15/20/40 [S4];
   10/20/30 plus a −10% floor [S5]; protection levels 10/15/20/25 [S6]. **The 10% buffer is
   the one value present in every menu**, and Equitable commits that "we will always offer a
   Segment Option with a Segment Buffer that protects the first 10% of loss" [S4].

### Declared (non-guaranteed) crediting parameters — snapshot

| Parameter | Representative value | Basis |
|---|---|---|
| 6-year Cap Rate (10% buffer) | 100% | **[std]** (6) |
| 3-year Cap Rate (10% buffer) | 55% | **[std]** (6) |
| 1-year Cap Rate (10% buffer) | 12% | **[std]** (6) |
| 1-year Step Rate (10% buffer) | 8% | **[std]** (7) |
| 1-year Edge Rate (10% buffer) | 6% | **[std]** (7) |
| Participation Rate | 100% | [S4]; adoption **[std]** (7) |
| Declared Fixed Account rate | 3.00% | **[std]** (8) |

6. **No currently-declared rate sheet was retrievable** — the Brighthouse Shield rates page
   and the Equitable performance cap rate page both returned HTTP 403 / WAF rejections
   (research gap 1) — so every rate here is a modeling snapshot. Observed *illustrative*
   prospectus values: 10% cap, 1-year [S1]; 75% cap, 3-year at a 10% buffer [S3]; 12% cap
   1-year and 100% cap 6-year [S6]; 60% cap with 110% participation on a 6-year 20%-buffer
   segment and 9% cap on a 1-year Step Up [S4]. The chosen 12% / 55% / 100% triple brackets
   those and sits well above the contractual minima below.
7. Observed illustrative step/trigger values: 8% Step [S1]; 5% Step with 90% participation
   [S3]; 12.5% trigger and 6% dual trigger, 1-year [S6]. No *Edge* value appears in any
   retrieved document; 6% is a modeling choice set below the 8% Step, the correct economic
   ordering because the Edge design pays down to −*b* rather than to 0 and so buys a lower
   rate. Participation Rate 100% is what Equitable guarantees for the life of every current
   segment type [S4].
8. No declared fixed-account rate appears in any retrieved document; only the 1% contractual
   minimum is public [S1] [S2]. 3.00% is a snapshot consistent with the **[std]** 4.00%
   risk-free assumption in `technical-notes.md`.

### Guaranteed minimum crediting parameters (contractual floors on the declared rates)

| Parameter | Representative value | Basis |
|---|---|---|
| Minimum guaranteed Cap Rate | 2% (1-year), 6% (3-year), 8% (6-year) | [S1] [S2] |
| Minimum guaranteed Step Rate | 2% | [S2] |
| Minimum guaranteed Edge Rate | 2% | [S2] |
| Minimum guaranteed interest rate, Fixed Account and Holding Account | 1% | [S1] [S2] |
| Buffer (Shield Rate) | Guaranteed for the life of each term; not redeterminable mid-term | [S1] [S2] |

These are **guaranteed elements** in ASOP No. 2 terms — it lists "minimum index parameters"
as a guaranteed element and "index parameters used to determine credited interest" as a
non-guaranteed element [R5] [REG-R26]. A projection model must floor every renewal-rate
assumption at this table.

### Charges

| Parameter | Representative value | Basis |
|---|---|---|
| Explicit asset-based charge (M&E, administration) on index-linked value | **None** | [S2] [S3] [S4] [S6] [R6] |
| Contract maintenance fee | None | [S2] |
| Withdrawal charge (% of the amount withdrawn in excess of the free amount) | 7%, 7%, 6%, 5%, 4%, 3%, 0% by complete contract years since the Issue Date | [S1] [S2] |
| Withdrawal charge gross-up | None — the charge is deducted from the amount withdrawn, not added to it | [S1] [S2]; contrast [S4] |
| Free withdrawal amount | Zero in contract year 1; thereafter 10% of Account Value as of the prior Contract Anniversary, less amounts already withdrawn in the current contract year; non-cumulative | [S1] [S2] |
| Premium tax | 0% (state pass-through, modeled as zero) | [S2]; value **[std]** (9) |
| Trading cost provision inside the interim value | 0.10% of the sum of the absolute market values of the replicating options | **[std]** (10) |

9. Brighthouse lists the complete charge inventory as "(i) Withdrawal Charges; and (ii)
   Premium Tax and other taxes" [S2]. Premium tax is state-specific and is not quantified
   in any retrieved document; zero is the modeling default with the parameter exposed.
10. AG 54 requires consistency with the hypothetical portfolio "less a provision for the
    cost attributable to reasonably expected or actual Trading Costs" [R2], and [S2], [S4]
    and [S6] all say the derivative valuation reflects "the estimated cost of exiting" the
    options — **without a number** (research gap 8). The Academy example shows trading costs
    of $0.01–$0.04 per $100 of base against **net** derivative values of $12.94–$38.46 [R6],
    i.e. of order ten basis points of *net* option value. The [std] factor here is assessed
    on the **sum of absolute** option component values — a wider base than the Academy's net
    figure (at their t = 0 the gross base is $31.14 against a net $12.94), so 0.10% on this
    base is a deliberately conservative reading of the same order of magnitude. It must be
    treated as a free parameter, and the assessment base must be stated whenever it is
    recalibrated.

### Death benefit

| Parameter | Representative value | Basis |
|---|---|---|
| Standard death benefit, owners 80 or younger at issue | **Return of Premium**: greater of Account Value and Purchase Payment | [S2] |
| Standard death benefit, owners 81+ at issue | Account Value | [S2] |
| Adjustment for withdrawals | The Purchase Payment component is reduced *proportionately* by the percentage reduction in Account Value for each partial withdrawal, including any applicable withdrawal charge | [S1] [S2] |
| Value used mid-term | **Interim Value** of each open index-linked option | [S1] [S2] [S4] [S6] |
| Determination date | End of the business day on which due proof of death and an acceptable payment election are received | [S1] |
| Optional GMDB riders | Out of scope | scope **[std]** (see Riders) |

The guarantee therefore sits on top of a value that can itself be depressed by a negative
interim value: "we will pay the Interim Value, which may be less than if you held the
Contract until all of your Shield Option(s) reach their Term End Date" [S1]. The GMDB is
genuinely in the money in equity stress — it is not a nominal guarantee.

### Annuitization

| Parameter | Representative value | Basis |
|---|---|---|
| Income options | Life Annuity with 10 Years of Annuity Payments Guaranteed; Joint and Last Survivor Annuity with 10 Years Guaranteed | [S2] |
| Value applied | Interim Value if annuitized before a Term End Date | [S1] |
| Annuity purchase rates | Not located in any retrieved document — modeled from a public basis | research gap; **[std]** (11) |

11. Option *names* are documented [S1] [S2] but the mortality basis, assumed interest rate,
    factor tables and the **survivor continuance percentage** on the joint form are not;
    they live in the contract specimen or SAI, neither of which was located (research
    gap 2). The reference model computes payout factors from the 2012 IAM Period Table —
    the *loaded* table, correct for a **guaranteed** purchase-rate basis — with Projection
    Scale G2 per Model #821 / VM-M [REG-R59] at a **[std]** 2.50% assumed interest rate,
    and assumes **100% last-survivor continuance [std] [unverified]**. The payout-phase
    mechanics themselves are not restated here: they are the chassis in
    `products/immediate_annuity/product-spec.md` and
    `products/immediate_annuity/technical-notes.md`, restricted to the two forms above —
    this contract offers no cash-refund or installment-refund form [S2], so those branches
    of that chassis are unused.

### Interim value (the defining mechanic)

| Parameter | Representative value | Basis |
|---|---|---|
| Methodology | AG 54 Hypothetical Portfolio = Fixed Income Asset Proxy + Derivative Asset Proxy, less Trading Costs | [R2] [S2] |
| Algebraic family | `(A − B) x [(1+C)/(1+D)]^E` for the fixed leg, plus the current market value of the replicating options | [S2]; selection **[std]** (12) |
| Option-budget amortization | Straight-line to the end of the term | [S2]; selection **[std]** (13) |
| Discount rate ("Market Value Rate") | Constant Maturity Treasury yield at the term's maturity, linearly interpolated between adjacent CMT maturities | [S2] |
| Option pricing model | Black-Scholes, European options | [S2] [R2] |
| Transactions settled at interim value | Partial withdrawal, surrender, death benefit, annuitization, transfer, deduction of any fee, free-look cancellation | [S1] [S2] [S4] [S6] |
| Value during the Transfer Period | Interim Value equals the Investment Amount at the Term End Date (no option adjustment) | [S2] |

12. Three algebraic families appear across the retrieved prospectuses (see *Variations*).
    Family (a) — fixed leg net of the initial option budget with an explicit
    interest-rate adjustment factor — is chosen because it is the closest literal
    implementation of AG 54's Fixed Income Asset Proxy definition [R2] and is used by two
    of the five insurers [S2] [S3].
13. Observed: straight-line amortization nationally [S2]; **updated time to expiry**
    nationally but straight-line **in Pennsylvania** [S3]; linear amortization of the
    beginning proxy value [S5]. Straight-line is chosen with the alternative retained as
    a configuration switch (`technical-notes.md`).

---

## Contractual mechanics

Notation: `R` = index performance over the term = `I(T)/I(0) − 1`; `b` buffer (positive,
e.g. 0.10); `c` cap; `s` step; `e` edge; `PR` participation; `f` floor (positive).

### Term-end crediting [S1] [S2]

    Buffer + Cap    g = min(R, c)   if R >= 0 ;   g = min(0, R + b)   if R <  0
    Buffer + Step   g = s           if R >= 0 ;   g = min(0, R + b)   if R <  0
    Buffer + Edge   g = e           if R >= -b;   g = R + b           if R <  -b

[S1] states the buffer branch verbatim as "the lesser of: zero or the Index Performance
increased by the Shield Rate" (worked: −15% index performance under Shield 10 → a −5%
Performance Rate) together with the governing rule that "The Performance Rate can never be
greater than zero if the Index Performance is negative" [S1]. Cap-versus-Step contrast
from [S1]: at +15% index performance a 10% Cap pays 10% and an 8% Step pays 8%; at 0%
index performance the Cap pays 0% and the Step pays 8%. The Edge design moves the trigger
threshold from 0 to −*b* — it pays "the rate credited at the Term End Date if the Index
Performance is equal to or greater than the Shield Rate" [S2]. Roll-forward [S1] [S2]
(worked in [S1] as $50,000 + $4,000 = $54,000):

    InvestmentAmount(term end) = InvestmentAmount(term start, adjusted for withdrawals) x (1 + g)

### Interim value

For any business day strictly inside a term, `InterimValue` = market value of the Fixed
Income Asset Proxy + current market value of the Derivative Asset Proxy, the fixed leg
being [S2]:

    (A - B) x [ (1 + C) / (1 + D) ] ^ E
       A    = Investment Amount on the day the Interim Value is calculated
       B    = market value of the Derivative Asset Proxy under INITIAL market conditions,
              with straight-line amortization to the end of the Term
       C, D = Market Value Rate on the Term Start Date / on the calculation day
       E    = total days remaining in the Term / 365

The `[(1+C)/(1+D)]^E` factor is "a Market Value Adjustment to address any changes in
interest rates from the Term Start Date to the day the Interim Value is calculated" [S2].
The Derivative Asset Proxy is valued with Black-Scholes and "reflects the impact of the
Cap Rate, Step Rate, Edge Rate, and Shield Rate at the end of the Term as well as the
estimated cost of exiting the replicating options prior to the Term End Date" [S2].
Replicating portfolios [S2] — ATMC/OTMC at-/out-of-the-money call, OTMP out-of-the-money
put, ATMBC/ITMBC at-/in-the-money binary call:

    Cap Rate option:  ATMC - OTMC - OTMP        Step Rate option: (Step Rate x ATMBC) - OTMP
    Step Rate Edge option:  (Edge Rate x ITMBC) - OTMP

"For purposes of the Interim Value formula, the value of the out-of-the-money call will be
zero if a Cap Rate Shield Option is uncapped" [S2]. Two economic warnings a model must
reproduce: "the out-of-the-money put will almost always reduce the Interim Value, even when
the current Index Value on a Business Day is higher than the Index Value on the Term Start
Date"; and "you could have negative Interim Value, even if the Index Value has increased at
the time of the calculation" [S2]. Worked in [S2] (index 500 → 600, six months remaining,
Market Value Rate 3%): $49,452.40 + $4,062.37 = **$53,514.77**.

### Withdrawals — the proportional rule

A mid-term withdrawal reduces the index-linked notional **in the same proportion that the
withdrawal reduced the Interim Value**, not dollar-for-dollar [S2] [S3] [S4] [S6]:

    InvestmentAmount_after = InvestmentAmount_before x ( 1 - GrossWithdrawal / InterimValue )

Worked in [S2]: `$50,000 x (1 − $20,000 / $53,514.77) = $31,313.57`; the reduced amount
becomes the notional for the rest of the term [S2]. Prudential states the identical rule
and works it at a 71.429% ratio [S3]. The prospectus states the asymmetry: "a withdrawal
when Interim Value is less than the Investment Amount will cause a greater percentage
reduction in the Investment Amount that remains in your Shield Option relative to the
percentage reduction for the same withdrawal amount when Interim Value is greater than the
Investment Amount" [S2]. **The reduction in notional can exceed the cash the owner
receives** — numeric illustration in `technical-notes.md`.

### Withdrawal charge and surrender

The charge is a percentage of the amount withdrawn **in excess of the Free Withdrawal
Amount**, by complete contract years since the Issue Date, and is not grossed up [S1] [S2].
Worked in [S2]: $100,000 purchase payment, $80,000 Account Value at the start of contract
year 6, full withdrawal → free amount $8,000 (10%), charge 3% x $72,000 = $2,160, cash
value $77,840. The Free Withdrawal Amount is zero in contract year 1, thereafter 10% of
the Account Value at the prior Contract Anniversary, reduced by amounts already withdrawn
in the same contract year, with no carry-over [S1] [S2].

### Fixed Account, Holding Account, transfers, renewal, Performance Lock

A **Fixed Account** (general account) is available with a term of not less than one year
and a minimum guaranteed interest rate not less than 1% [S1] [S2]; a **Holding Account**
(also general account, minimum 1%) receives maturing amounts when both the same option and
the Fixed Account are unavailable and holds them to the next Contract Anniversary [S2].
Transfers among index-linked options are permitted only during the Transfer Period — the
five calendar days following the Contract Anniversary coinciding with the Term End Date —
and partial transfers outside it are not permitted [S1] [S2]. There is **no separate
fixed-account MVA formula** in the prospectus; the only MVA language in it is the
`[(1+C)/(1+D)]^E` factor inside the interim value appendix [S2]. Once per term the owner
may **lock** an option's Interim Value; the lock is irrevocable for the rest of the term,
after which withdrawals reduce the Performance Lock Value **dollar-for-dollar** and
transfers become permissible on any Contract Anniversary [S2] — economically the option
leg vanishes and the bucket becomes a fixed accrual to term end.

---

## Riders and options

**In scope (modeled).** The built-in **return-of-premium GMDB** (no explicit charge, owners
80 or younger at issue, proportional reduction for withdrawals) [S2]; the **Fixed Account**
and **Holding Account** as general-account destinations at term end and for unallocated
amounts [S1] [S2]; **automatic renewal** into the same option at the new declared rate at
each Term End Date with a Transfer Period election window [S1] [S2]; and **Performance
Lock** as an optional module [S2].

**Out of scope (listed, not modeled):**

- Optional GMDB riders for a charge: Highest Anniversary Value Death Benefit [S4]; Maximum
  Anniversary Value Death Benefit at 0.20% of a Charge Base [S5].
- Guaranteed lifetime income riders — Allianz's Select Income variant bundles one inside a
  1.95% base contract fee on a Charge Base, the only explicit asset-based charge in the
  sample, and its figures are provisional ("[To be updated by amendment]" markers in an
  initial N-4) [S5].
- **Dual-direction / absolute-return** segments paying `|R|` for losses inside the buffer
  [S4], the trigger rate for the same [S5], or a Dual Performance Trigger Rate / Dual Rate
  [S6]; **floor** strategies (Allianz Index Guard, −10% floor) [S5]; **100% buffer**
  full-protection strategies [S3].
- **Annual Lock** segments, which compound yearly Standard-rule rates and whose interim
  value needs "a single extended exotic option that periodically settles and resets in
  strike price" [S4] [S6]; **tiered participation rate** strategies [S3]; **Optimal Mix /
  rainbow** segments blending 3 or 4 component indices [S4].
- **Secure Lock+** (a lock that also *resets* the Performance Cap, minimum Reset Rate
  3.50%) [S6]; variable investment subaccounts on a combination chassis [S3]; dollar cap
  averaging accounts [S4]; systematic withdrawal and RMD programs; transfer and
  special-service fees ($35 / $55 / up to $90, currently waived) [S4].

---

## Variations across insurers

1. **Interim value algebra — three families.** (a) *Fixed leg net of the option budget,
   with an explicit interest-rate adjustment factor*: `(A − B) x [(1+C)/(1+D)]^E`
   [S2] [S3]. (b) *Full notional discounted at a single current rate plus a separate,
   always-positive expense rebate*: Equitable's `SegmentInvestment / (1 + rate)^(time to
   maturity)` plus a **Cap Calculation Factor** [S4]; Lincoln's
   `C x [1/(1+E)^D x (1+E)^D/(1+F)^D]`, which collapses algebraically to `C / (1+F)^D`
   [S6]. (c) *A delta applied to the notional rather than a value*: Allianz's
   `Daily Adjustment = [Δ Proxy Value + proxy interest] x Index Option Base`, with **no
   interest-rate adjustment term at all** [S5]. **Chosen: family (a)** — it is the closest
   literal reading of AG 54's Fixed Income Asset Proxy definition [R2] and it is the
   chassis anchor [S2].
2. **Option-budget amortization convention.** Straight-line to term end [S2]; updated time
   to expiry [S3] — except in Pennsylvania, where the same insurer switches to
   straight-line [S3]; linear amortization of the beginning proxy value [S5]. **Chosen:
   straight-line**, matching the chassis; the alternative is a configuration switch
   because a single insurer needs both.
3. **Discount rate reference.** CMT at the term's maturity, linearly interpolated [S2]; CMT
   plus a market-observable investment-grade corporate spread [S6]; the Bloomberg Barclays
   U.S. Intermediate Credit Index at a set duration that "may not match the actual length
   of the Index Strategy" [S3]; an investment-grade rate built as risk-free plus a spread,
   which Equitable notes is above swap rates and therefore "will result in a lower value
   for that component" [S4]. AG 54's project history explains the dispersion: MVA
   requirements were deliberately **removed** because consensus was unreachable, leaving
   the "equity" principle to state review [R2]. **Chosen: CMT**, per the chassis.
4. **Buffer versus floor.** Buffers dominate. **Only one insurer in the retrieved sample
   offers an explicit floor** — Allianz's Index Guard Strategy at a −10% Floor — and it
   needs a **four-option** replicating portfolio (ATM call − OTM call − ATM put + OTM put)
   rather than the three-option buffer portfolio [S5]. Prudential's **100% buffer** is full
   protection achieved inside the buffer framework, not a floor [S3]. The Academy confirms
   both species exist [R6] and the SEC treats buffers and floors as the two kinds of
   "limits on losses" [R1]. **Chosen: buffer only**, with the floor payoff and its
   replicating portfolio in `technical-notes.md` so the module can be switched on.
5. **Buffer depth and term length.** Buffers 10/15/25 [S1] [S2]; 5/10/15/20/100 [S3];
   10/15/20/40 [S4]; 10/20/30 [S5]; 10/15/20/25 [S6] — **10% is universal** and Equitable
   commits to always offering it [S4]. Terms 1/3/6 are near-universal, [S2] adds 2 years,
   [S6] offers only 1 and 6, and the Academy reports one/two/three/six [R6]. **Chosen: 10%
   buffer on a 1/3/6 menu**, full buffer menu retained.
6. **Dual-direction and absolute-return designs.** Equitable's Dual Direction pays `|R|`
   for losses within the buffer, the participation rate applying only to positive index
   performance [S4]; Allianz's Index Dual Precision pays the trigger rate for the same
   region [S5]; Lincoln's Dual Performance Trigger and Dual Rate accounts likewise [S6];
   Brighthouse's Step Rate Edge triggers at −*b* rather than 0 [S2]. **Chosen: Edge only**
   — the minimal member of the family, needing one binary option rather than a re-strike of
   the whole portfolio.
7. **Withdrawal accounting is uniform** and is the single most important behavioral rule:
   all insurers reduce the notional proportionally to the reduction in interim value
   [S2] [S3] [S4] [S6], and all warn the proportional reduction can exceed the dollar
   withdrawal when the interim value is below the notional [S2] [S3] [S6]. The one exception
   is a **locked** bucket, reduced dollar-for-dollar [S2]. **Chosen: proportional**, with
   the locked-bucket exception in the Performance Lock module.
8. **Charge structure.** [S1]–[S4] and [S6] carry **no explicit asset-based charge** on
   index-linked value; the cap *is* the fee — "While no fees or charges are deducted from
   the amounts held in the Index Strategies, the available Cap Rates, Participation Rates,
   Tier Levels, and Step Rates reflect the expenses related to the Index Strategies" [S3],
   and [S4] and [S6] both call the cap an "implicit ongoing fee". The Academy confirms
   "Most contracts do not have explicit fees other than for optional benefits" [R6]. The
   outlier is Allianz's rider-bundled 1.95% [S5]. **Chosen: no explicit charge.**
   [unverified] whether any RILA applies an explicit M&E charge to index-linked account
   value — none of the retrieved documents does.
9. **Fee-series structure.** One chassis often sells three ways: Series B (8%-grading-to-0
   withdrawal charge over 6 years), Select (no charge, lower caps) and Advisory (no charge)
   [S4]; B-Share and Advisory [S6]. A model must parameterize the withdrawal-charge
   schedule and the cap level **jointly**, since they trade off. **Chosen: the
   commission-paying B-equivalent** (7-7-6-5-4-3-0 [S1] [S2]).
10. **Pre- versus post-AG 54 interim value.** The older Shield Level Select design used no
    option pricing at all — a **time-prorated accrual** in which the Shield, Cap and Step
    Rates each accrue linearly over the term and the term-end rules are applied to the
    accrued rates (worked in [S1]: 10% cap x 183/365 = 5% accrued cap, giving a $52,500
    interim value on a $50,000 investment amount) [S1]. It predates AG 54's July 1, 2024
    effective date [R2] and would not satisfy the Hypothetical Portfolio requirement without
    a material-consistency demonstration. Retained in `technical-notes.md` as a tractable
    first implementation target and regression contrast, **not** as the representative
    design.

---

## Regulatory context

**Actuarial Guideline LIV (AG 54) — definitional.** AG 54 specifies "the conditions under
which an Index-Linked Variable Annuity (ILVA) is consistent with the definition of a
variable annuity and exempt from Model 805 and specify nonforfeiture requirements
consistent with variable annuities" [R2] [REG-R44]. Because an ILVA account is not
unitized, it requires **Interim Values materially consistent with a Hypothetical Portfolio
= Fixed Income Asset Proxy + Derivative Asset Proxy, less a provision for Trading Costs**;
the Index Strategy Base must equal the Strategy Value at term start; the fixed proxy is a
hypothetical bond starting at (Base − Derivative Asset Proxy value) and, at unchanged
yield, accreting to the Base at term end; derivative assumptions must track observable
market prices wherever possible, valued by "the standard Black-Scholes method, Monte-Carlo
Simulation techniques, and other market consistent option valuation techniques"; and
non-hypothetical-portfolio methods need a material-consistency demonstration "under a
reasonable number of realistic economic scenarios that include index changes that test
crediting constraints and recognize initial option pricing market conditions" [R2]. An
actuarial memorandum with certifications is required with each ILVA filing [R2]. Effective
for all contracts, riders, endorsements and amendments issued **on or after July 1, 2024**;
an ILVA that fails "is not considered a variable annuity and therefore is subject to Model
805" [R2]. Whether an MVA is included, and any formula, was deliberately left to the states
under the equity principle [R2]. The retrieved document's adoption trail stops at the Life
Insurance and Annuities (A) Committee (2/24/2023); NAIC Executive/Plenary adoption is
[unverified].

**NAIC Model #250 and the model-number correction.** AG 54 requires ILVA nonforfeiture
benefits to comply with **Section 7 of Model #250, *not including* Section 7.B**, with net
investment return consistent with the interim value requirements [R2] [REG-R43] — §7.B being
the provision that would otherwise push non-varying benefits back to the deferred-annuity
nonforfeiture law [R4]. **Correction carried from the research:** #250 is the **Variable
Annuity** Model Regulation; the **Annuity Disclosure Model Regulation is #245**, not #250
[REG-R43] [REG-R45], as AG 54's own citation confirms [REG-R44]. RILAs are largely exempt
from #245 via its §3.D registered-product carve-out but still owe the Buyer's Guide
[REG-R45].

**NAIC Model #805 and the 15-basis-point correction.** Model #805 **does not apply to a
RILA if and only if AG 54 is satisfied** [R2] [REG-R42] [REG-R44]. Where a model must
nevertheless evaluate the #805 floor (a non-compliant design, or a fixed account tested
under Model #250 §7.B), the indexed nonforfeiture rate is the lesser of 3% and the
five-year CMT rate (rounded to the nearest 1/20 of one percent, from a date no more than 15
months before issue or redetermination) **reduced by 125 basis points and subject to a
floor of 15 basis points (0.15%)** — **not** the 1% floor commonly asserted [REG-R42]. The
minimum nonforfeiture amount accumulates net considerations of 87.5% of gross, less prior
withdrawals, a $50 annual contract charge, premium tax paid and indebtedness [REG-R42].

**SEC registration — the 2024 move to Form N-4.** Release Nos. 33-11294; 34-100450;
IC-35273; File No. S7-16-23; RIN 3235-AN30 amended 17 CFR Parts 230, 232, 239 and 274 to
require RILAs and registered MVA annuities to register on **Form N-4** rather than Forms
S-1/S-3, driven by the **Registration for Index-Linked Annuities Act**, Division AA, Title I
of the Consolidated Appropriations Act, 2023, Pub. L. 117-328; 136 Stat. 4459 (Dec. 29,
2022) [R1] [REG-R49]. **Effective September 23, 2024** (verified twice [REG-R49] [REG-R49b]);
**compliance date May 1, 2026**, by which RILA issuers must file a Rule 485(a)
post-effective amendment on final Form N-4 [R1] — that date carries **[unverified]** in the
cross-product bibliography, which reports it from filing-agent and law-firm summaries
without reading section II.J of the release [REG-R49] [unverified]. The rule requires
tailored disclosure of cap rates, participation rates, buffers and floors, contract
adjustments and surrender charges; a prescribed **Key Information Table**; optional summary
prospectuses under Rule 498A, whose title now expressly extends to "registered non-variable
annuity contracts" [REG-R51]; and Rule 156 compliance for sales literature [REG-R49]. It
also names the three early-withdrawal costs — surrender charges, **interim value
adjustments** ("the IVA will adjust the contract value based, generally, on a complex
formula where the IVA may change daily and can be positive or negative"), and a positive or
negative MVA — collectively "contract adjustments" [R1]. Form N-4 itself was not
retrievable (sec.gov HTTP 403) and is described only through the adopting releases
[REG-R52].

**Valuation — VM-21 and its scope test.** VM-21 constitutes CARVM in its scope, aggregate
reserve = stochastic reserve (CTE70) + additional standard projection amount [REG-R35].
**Applicability is frequently mis-stated.** §2.A.1 brings in variable deferred annuities and
"any other policy or contract which contains guarantees similar in nature to GMDBs or
VAGLBs … where there is no other explicit reserve requirement", but **§2.A.3 excludes
"Separate account contracts that guarantee an index and do not offer GMDBs or VAGLBs"**
[R3]. So a bare accumulation RILA is **outside** VM-21, while the representative design
here — carrying a return-of-premium GMDB — is **in** scope [R3] [S2]; §2.A.2 disapplies VM-21
to contracts falling under VM-A item **A-255** while extending it to subaccounts with
MVA-like features [R3]. That A-255 limb is no longer a blind cross-reference: A-255 has been
read, and the test is its ¶1 definition — a deferred annuity, individual or group, whose
underlying assets are held in a separate account, whose values are guaranteed if held for
specified periods, whose nonforfeiture values rest on a market-value-adjustment formula if
held for shorter periods, and whose assets "must be in a separate account during the period
or periods when the contract holder can surrender the contract" [REG-R157]. **Whether the
representative design meets that test is not resolved here** — the exclusion is VM-21's text,
not A-255's [REG-R157] [REG-R35] [unverified]. AG 43 is not simply superseded: through
reference in AG 43, VM-21 also reaches pre-2017 contracts outside its own scope, and the
two populations may be reserved as one aggregated group [REG-R35] [REG-R38].

**Valuation — the formulaic CARVM floor, and what now sources it.** A contract outside VM-21
falls back to formulaic CARVM: SVL §5a, printed word for word at A-820 ¶15
[REG-R1] [REG-R153 ¶15](#uslib-reg-r153). Its interpretive layer has been read at first hand. **AG 33 reaches
this contract** — it applies "to all annuity contracts subject to CARVM, where any elective
benefits … are available", with no product list, no separate-account exception and no
threshold, and this chassis offers its three named elective benefits (full surrenders,
partial withdrawals, full and partial annuitizations) [REG-R151] [S1] [S2]. **AG 35 was
retrieved and does not address this design** — it defines no term "equity indexed annuity"
and says nothing about separate accounts, registered products, buffers, floors or AG 54;
record it as neither including nor excluding RILA [REG-R152]. **A-250 and A-255, long called
this product's "closest formulaic items", turn out not to be reserve methods at all** — one
printed page each, each delegating the reserve to A-820, and between them containing no
formula, symbol, factor, table, elective-path rule, interim-value rule or the word CARVM
[REG-R156] [REG-R157]. What remains unsourced is narrower than before and still real: **no
retrieved document says how an Interim Value — a market-consistent derivative price — becomes
"the future guaranteed benefit" of §5a**, AG 54 governing the *nonforfeiture* value and not
the reserve [R2] [REG-R44].

**Capital.** C-3 Phase II sets the Total Asset Requirement at CTE 90 and RBC as the excess
of TAR over statutory reserves, subject to a Standard Scenario floor [REG-R47]; VM-21
§§4.A–4.E and the RBC requirements are identical except for the elective tax treatment
[REG-R35], so one projection serves both. Reform background (hedging penalties, Standard
Scenario misalignment) is in the Oliver Wyman QIS II reports [REG-R48]. The Academy places
ILVA RBC as "C0–C1: General Account, C3–C4: Separate Account" [R6].

**Non-guaranteed elements.** Cap, Step, Edge and Participation Rates reset at each Term
Start Date are NGEs under ASOP No. 2, which lists "index parameters used to determine
credited interest" as an NGE and "minimum index parameters" as guaranteed elements, and
whose scope covers fixed, variable and **indexed** deferred annuities [R5] [REG-R26]. It
requires a determination policy, an NGE framework, NGE scales, policy classes and periodic
review of in-force NGEs [R5]. The prospectuses confirm the discretion: "Trigger Rates,
Caps, and Participation Rates may be adjusted on the next Term Start Date and may vary
significantly from Term to Term" [S5].

**Federal tax.** IRC §72: LIFO income-first on pre-annuity-starting-date distributions from
deferred annuities; §72(q)'s 10% additional tax on the includible portion of non-qualified
distributions; §72(s)'s at-least-as-rapidly and five-year death distribution rules; and
aggregation of all annuity contracts issued by one company to one policyholder in a
calendar year [REG-R55]. §1035 permits annuity-to-annuity and annuity-to-qualified-LTC
exchanges but **not** annuity-to-life [REG-R56]. §817(h) requires adequate diversification
of the segregated asset account [REG-R15]. §807 sets the tax reserve at the greater of net
surrender value and 92.81% of the NAIC-prescribed method (CARVM), capped at statutory
[REG-R16].

**Distribution conduct.** Model #275 (2020 best-interest revision) requires producers to act
in the consumer's best interest and insurers to supervise recommendations [REG-R46]; FINRA
Rule 2330 governs recommended purchases and exchanges of deferred variable annuities, with
principal review within seven business days and disclosure of the surrender period and the
pre-59½ tax penalty [REG-R54] — [unverified] whether FINRA applies it to RILAs
specifically, since the rule text says "deferred variable annuities". Both bite the model
indirectly, through exchange velocity and hence surrender assumptions.

**Interstate Insurance Compact.** The Compact's ILVA standard (IIPRC-03-I-ILVA) is
**narrower than AG 54**: it "requires the use of the Hypothetical Portfolio methodology and
does not allow for materially consistent approaches" [R6]. Quoted second-hand through the
Academy paper; the Compact standard was not retrieved [R6] [unverified].

**U.S. GAAP.** RILA index credits and annuity guarantee riders are the paradigm **market
risk benefits** at fair value through earnings under LDTI [REG-R34], with ASOP No. 10 (Doc.
No. 207) the professional-standards counterpart; the MRB-versus-insurance-liability
classification determines the measurement model [REG-R71].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-registered_index_linked_annuity-r1
[R2]: #uslib-registered_index_linked_annuity-r2
[R3]: #uslib-registered_index_linked_annuity-r3
[R4]: #uslib-registered_index_linked_annuity-r4
[R5]: #uslib-registered_index_linked_annuity-r5
[R6]: #uslib-registered_index_linked_annuity-r6
[REG-R1]: #uslib-reg-r1
[REG-R15]: #uslib-reg-r15
[REG-R151]: #uslib-reg-r151
[REG-R152]: #uslib-reg-r152
[REG-R156]: #uslib-reg-r156
[REG-R157]: #uslib-reg-r157
[REG-R16]: #uslib-reg-r16
[REG-R26]: #uslib-reg-r26
[REG-R34]: #uslib-reg-r34
[REG-R35]: #uslib-reg-r35
[REG-R38]: #uslib-reg-r38
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R44]: #uslib-reg-r44
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R47]: #uslib-reg-r47
[REG-R48]: #uslib-reg-r48
[REG-R49]: #uslib-reg-r49
[REG-R49b]: #uslib-reg-r49
[REG-R51]: #uslib-reg-r51
[REG-R52]: #uslib-reg-r52
[REG-R53]: #uslib-reg-r53
[REG-R54]: #uslib-reg-r54
[REG-R55]: #uslib-reg-r55
[REG-R56]: #uslib-reg-r56
[REG-R59]: #uslib-reg-r59
[REG-R71]: #uslib-reg-r71
[S1]: #uslib-registered_index_linked_annuity-s1
[S2]: #uslib-registered_index_linked_annuity-s2
[S3]: #uslib-registered_index_linked_annuity-s3
[S4]: #uslib-registered_index_linked_annuity-s4
[S5]: #uslib-registered_index_linked_annuity-s5
[S6]: #uslib-registered_index_linked_annuity-s6
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
