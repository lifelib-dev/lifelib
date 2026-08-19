# Product Specification

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** This is a *standardized composite specification* assembled for reference
liability cash-flow modeling. It does not describe any single insurer's product. Facts
carrying a source tag — [S#] (primary product documents) and [R#] (regulatory/actuarial
references), both numbered per `_research/immediate-annuity.md`, and [REG-R#] (the
cross-product reference library `references/regulatory-and-actuarial-references.md`,
one shared numbering space now running **R1–R157** with most of the **R73–R149** block
unused: R1–R34 from `_research/regulatory-actuarial.md`,
R35–R72 from `_research/regulatory-actuarial-annuities.md`, and
R150–R157 from the AP&P Manual appendix reading of **2026-08-06**, of which **R151** (AG 33)
and **R153** (A-820 with A-821 and A-822) are cited here) — were extracted from the
cited document. Values marked **[std]** are standardizations introduced for the reference
implementation; each [std] table row carries a footnote giving the rationale and the
observed range across insurers. Facts the research file could not verify are flagged
[unverified].

The design anchor is one carrier's single premium immediate fixed annuity [S1] combined
with a second carrier's SPIA [S2] [S3]. The second supplies the cleanest published
statement of the two joint-life reduction triggers; the first supplies the only published
SPIA surrender-charge schedule and the 1–4% compound COLA menu.

---

## Product overview and market role

A SPIA converts a single premium immediately into a payment stream. Income must begin
within a short window: **12 months** [S1] [S5], **one year** [S2] [S3], **13 months** [S8]; a
state regulator frames it as income "starting no later than one year after you pay the
premium" [R11], a carrier as "typically within a month (and never more than one year out)"
[S11]. Once issued the contract is **irrevocable**, has **no account value, no cash
surrender value, and cannot be surrendered** [S4] [S5]; one carrier: "there is no accumulation
or cash value — and, therefore, limited liquidity" [S1]. Income option, frequency and every
optional feature are **fixed at issue** [S2] [S3] [S5]; the one general exception is the
*period certain only* form, whose certain period may be lengthened or shortened after the
first contract year [S1]. Both qualified (Traditional / SEP / Custodial / Roth / inherited
IRA) and nonqualified money is accepted [S1] [S2] [S4] [S5]. More than **$3.6 billion** of
SPIAs were sold in Q1 2024 [S11].

**Position in this library.** This is the **payout chassis** for the U.S. annuity family:
the same survival-indexed payment engine serves deferred income annuities (which prepend a
deferral period), annuitizations of deferred-annuity account values, supplementary contracts
and pension risk transfer — VM-22 places all of them with SPIAs in a single **"Payout
Annuity Reserving Category"** [R2] [REG-R36]. Structured settlement annuities are SPIA-shaped
but statutorily distinct: under IRC §130 payments must be fixed and determinable and "cannot
be accelerated, deferred, increased, or decreased by the recipient", so no commutation of
any kind is permissible, and their valuation mortality basis differs [R10] [R4]. Out of scope.

A closely parallel model exists at `uk/products/pension-annuity/technical-notes.md`; the
payment engine is shared and the U.S. differences are tabulated in `technical-notes.md`
(Model scope). In summary: 2012 IAM Basic with Projection Scale G2 for best estimate and the
2012 IAR generational table for valuation [R2] [R3] [R4] versus the UK's CMI-restricted
proxies; **fixed compound COLA only** — no RPI/LPI escalation and **no CPI-linked option in
any retrieved U.S. document** [S1] [S2] [S4] [S5] [S6] [S8]; **cash refund and installment
refund** [S1] [S2] [S5] versus UK value protection; **period certain** [S1] [S2] [S4] [S5] versus
UK guarantee period; and exclusion-ratio taxation under IRC §72 [R6] [R7] [REG-R55].

---

## Representative specification

### Product identity and issue rules

| Parameter | Representative value | Basis |
|---|---|---|
| Design type | Single premium immediate **fixed** annuity; irrevocable; non-participating; no account value | [S1] [S2] [S4] [S5] |
| Contract nature | "The owner has no access to the premium… no cash value, no death benefit and the annuity can't be surrendered" (base form, before refund/certain options) | [S4] |
| Market types | Nonqualified and qualified (Traditional / SEP / Custodial / Roth / Beneficiary IRA) | [S1] [S2] [S4] [S5] |
| Market type in base model | Nonqualified | scope **[std]** (1) |
| Issue ages — lifetime forms | 18–90 | [S1]; [S2] max 90; band **[std]** (2) |
| Issue ages — period-certain-only form | to attained age 100 | [S1] |
| Age basis | **Age nearest birthday** ("74 years, six months and one day old ⇒ contract age 75") | [S1] |
| Annuity date (first payment date) | Within 12 months of issue; base model sets annuity date = issue date | [S1] [S5]; simplification **[std]** (3) |
| Changes after issue | None; exception: certain period on the *period-certain-only* form may be altered after year 1 | [S2] [S3] [S5]; exception [S1] |
| Anchor model point (used in both documents) | Premium $100,000; joint form; primary male ANB 65, joint annuitant female ANB 62; monthly in arrears; survivor percentage 66⅔%; 3% compound COLA; no certain period | **[std]** (2)(5)(6)(8)(10)(13) |

### Premium and income

| Parameter | Representative value | Basis |
|---|---|---|
| Single premium — minimum | $10,000 | [S1] [S4] [S5] [S6]; [S2] $25,000; choice **[std]** (4) |
| Single premium — maximum without insurer approval | $2,000,000 | [S2] [S4] [S5] [S6]; [S1] $1.5M; choice **[std]** (4) |
| Minimum scheduled periodic payment | $100 | [S1] [S4] [S6] |
| Payment frequency menu | Monthly, quarterly, semiannual, annual | [S1] [S2] [S4] [S5] [S6] [S8] |
| Payment frequency — base model | Monthly | choice **[std]** (5) |
| Payment timing — base model | **Arrears** | **[std]** (6) |
| State premium tax deducted from premium | 0.00% | mechanism [S6] [S7] [S11]; rate **[std]** (7) |
| Initial annual income — anchor cell | **$6,000 per $100,000 premium** = $500.00/month | **[std]** (8) |
| Explicit policyholder charges | None — "there are zero fees" | [S1] |

### Payout forms

| Parameter | Representative value | Basis |
|---|---|---|
| Single-life forms | Life only; life with period certain; life with cash refund; life with installment refund | [S1] [S2] [S4] [S5] |
| Non-life-contingent form | Period certain only | [S1] [S2] [S4] [S7] (not offered on [S5]'s lifetime-income form) |
| Period certain range / base default | 5–30 years / **10 years** | range [S1] [S2] [S4] [S5] [S7]; default **[std]** (9) |
| Joint reduction trigger | **Switch** — reduce on death of **EITHER** annuitant, or on death of the **PRIMARY** annuitant only | [S1] [S2] [S3] [S7] |
| Survivor percentage menu | 50%, 66⅔%, 75%, 100% | [S1] [S2] [S5] [S6] [S7]; set **[std]** (10) |
| Joint × guarantee combinations | Each trigger available as Only / with Period Certain / with Cash Refund / with Installment Refund | [S2]; [S1] crosses the two triggers with No Refund / Installment Refund / Period Certain only |
| Cash refund benefit | Lump sum at death = max(0, premium − cumulative income payments received) | [S1] [S3] [S5] |
| Installment refund benefit | Scheduled payments continue until cumulative payments equal the premium | [S1] [S4] [S5] [S6] |
| Guaranteed period implied by a refund form | premium ÷ annualized income benefit amount | [S5] |
| Survivor reduction during a certain period | Full unreduced instalment continues to the end of the certain period; reduction takes effect at the later of the triggering death and the certain-period end | [S5]; adoption **[std]** (11) |
| Temporary life; % -of-premium death benefit; pre-first-payment return of premium | Out of scope | [S4] [S5] [S2]; scope **[std]** (12) |

### Cost-of-living adjustment (COLA)

| Parameter | Representative value | Basis |
|---|---|---|
| COLA menu / base model | 1%, 2%, 3%, 4% **compound** / **3.00%** | [S1] [S5]; [S2] 2–4%, [S4] 1–5%, [S6] 1–3%, [S8] up to 6%; choice **[std]** (13) |
| Application | Automatic increase on each anniversary of the annuity date; elected at issue; not cancellable or changeable; annually compounded | [S1] [S4] [S6] |
| Reduction base | δ applies to the **current** income payment, so the survivor's payment escalates too | [S2] |
| Index-linked (CPI/RPI) escalation | **None offered** — no CPI-linked COLA found in any retrieved U.S. product document | survey of [S1] [S2] [S4] [S5] [S6] [S8]; permitted for qualified money by [R8] |
| Not available with | Life with Installment Refund | [S1] |
| Qualified-money ceiling on constant-percentage increases | Strictly **less than 5% per year** | [R8] |

### Liquidity: commutation and surrender charges

| Parameter | Representative value | Basis |
|---|---|---|
| Eligibility | Forms including a period certain only; after the first contract year; one withdrawal per contract year; not for contracts issued in Oregon | [S1] |
| Withdrawal minimum / residual constraint | $5,000 / each remaining guaranteed payment ≥ $100 | [S1] |
| Withdrawal maximum | **PV of all remaining period certain payments, less surrender charges** | [S1] |
| Surrender charge (% of amount withdrawn) by contract year | yr 2: 8%; 3: 7%; 4: 6%; 5: 5%; 6: 4%; 7: 3%; 8: 2%; 9: 1%; 10+: 0% | [S1] |
| Effect on life-contingent payments after the certain period | None | [S1] [S2] [S5] |
| Commutation discount basis | Compound annual j(t) = 4.00% + (10-yr CMT(t) − 10-yr CMT(0)) | **[std]** [unverified] (14) |
| Cash surrender value | None | [S1] [S4] [S5] |
| Nonforfeiture minimum | **None** — immediate annuities are expressly outside Model #805 | [R5] [REG-R42] |
| Payment acceleration features | Out of scope | [S2] [S5]; scope **[std]** (15) |

### Footnotes to [std] rows

1. Nonqualified keeps the projection free of the RMD overlay. Qualified adds: period certain
   capped near 10 years (9 for an inherited IRA) [S2] [R8]; installment refund unavailable
   [S2]; non-spouse survivor percentage capped by the MDIB table, 52% at a 40+ year age gap
   up to 100% at ≤ 10 years [R8]; constant-percentage COLA < 5% [R8]; and shortening of
   remaining payments to the 10-year post-death distribution period [S1] [S5].
2. Observed lifetime-form issue ages: 18–90 [S1]; max 90 [S2]; 0–85 individual with one joint
   annuitant to 90 [S4]; 0–95 nonqualified / 18–89 qualified [S5]; through 85 [S6]; 0–85
   [S8]. 18–90 is the intersection of the two anchors. VM-V's own representative cell set
   uses single-life ages 55, 60, 65, 70, 75, 80, 85, 91 [R1] — a good default age grid, and
   the source of the anchor cell's primary age 65. The joint annuitant's age 62 is a plain
   **[std]** three-year gap, chosen to stay inside the qualified "no more than 10 years
   younger" joint-annuitant rule [S2] so the same cell can be re-run as qualified.
3. Up to 12 months' deferral is permitted [S1] [S5]. Collapsing the annuity date onto the issue
   date removes a short pre-income period carrying a death benefit at one insurer only
   (that insurer pays return of premium on death, or on terminal illness with life expectancy
   ≤ 12 months, before the first payment date [S2]). Any nonzero deferral turns this product
   into the deferred-income-annuity chassis.
4. Minimum premium clusters at $10,000 [S1] [S4] [S5] [S6], one carrier the outlier at $25,000
   [S2]. Maximum without approval clusters at $2 million [S2] [S4] [S5] [S6], one carrier at $1.5
   million [S1]; the modal value is adopted. Sub-limits not carried into the composite: $1M to
   issue age 75 and $500K for ages 76–85 on single-life-only and temporary life [S4]; $1M for
   ages 86+ [S2].
5. All six product sources offer the same four-frequency menu; monthly is the frequency in
   which the published illustrations and rate anchors are predominantly quoted (the one
   exception is [S3]'s age-69 cell, quoted annually) [S3] [S9] [S10]. One carrier's
   right to *reduce* frequency if a payment would fall below $100 [S6] is not modeled.
6. No product document states advance versus arrears. VM-V's prescribed weight-table cash flow
   model assumes "annuity payments are made at the end of each year" [R1] — an
   annuity-immediate convention — so arrears is the default. The model exposes the choice
   because it moves the liability by about one payment period's mortality and interest.
7. Premium tax is deducted before income is determined at three sources [S6] [S7] [S11], but
   **no source quantifies a rate** and state rates were not researched (research gap). τ = 0
   in the base, exposed as a parameter.
8. **No insurer publishes payout factors, guaranteed annuity purchase rates, or the pricing
   basis** for a fixed SPIA; pricing is embedded entirely in the quoted payout rate
   (research gap). 6.00% p.a. of premium is a **round arithmetic anchor** ($500.00 a month
   on $100,000), chosen so every figure in the worked example is exact — **not** a priced
   rate. The nearest insurer illustration is a hypothetical Joint Life Only for two
   65-year-olds, $230,856 buying $1,200/month = **6.24%** annualized (February 2024, "for
   illustrative purposes only") [S3], but that cell carries **no** COLA, and a COLA
   materially reduces the initial payment [S1] [S2] [S3] [S4]: the same source's single
   male 65 with a 3% COLA runs at ≈**5.28%** against ≈**7.97%** for an un-escalated
   male 65 in the broker survey [S3] [S9] — a reduction of about a third.
   Scaling the 6.24% joint anchor by that ratio (≈4.1%) and allowing an uplift for the
   66⅔% survivor percentage against the illustration's implied 100% puts a 3%-COLA joint
   65/62 cell nearer **4.5%**. **The 6.00% level is therefore deliberately generous
   relative to the COLA-adjusted anchors and must be replaced by a real quote before any
   output is read as a price**; `B(1)` is an exogenous input, not a model output. Weaker
   anchors, context only:
   Life with 10-Year Period Certain at 69 ≈**7.11%**, single life male 65 with a 3% COLA
   ≈**5.28%** initial rising from ≈$900 to ≈$1,600/month over 20 years [S3]; a
   low-reliability broker survey (July 2026, best of 8 carriers per $100,000, life only)
   giving male 65 $664/month = **7.97%**, female 65 $635, joint 65 $583, carrier spread
   about 5–6% [S9]; a carrier's weekly "annualized payout as percent of total premium" table,
   life-with-cash-refund basis, male with $100,000, which is JavaScript-rendered and could
   not be captured [S10]. **Consequence: no pricing or annuity-rate test against public
   data is possible for this product.**
9. Certain-period ranges observed: 5–30 years [S1] [S4] [S5] [S7], up to 30 [S2], 5–20 [S6]. Ten
   years is the modal illustrated length [S3] [S9], sits inside the qualified cap [S2] [R8],
   and clears one carrier's 10-year floor for commutation eligibility [S4].
10. Observed survivor menus: 50/67/75 [S2]; 1/2, 2/3, 3/4 [S1]; two-thirds or one-half by
    contract form [S7]; 50/100 [S6]; continuous 40–99 [S5]. The discrete set {50, 66⅔, 75,
    100} covers essentially the whole market; 100% is included because refund forms
    frequently *require* it (one carrier's Joint Life with Cash Refund is available only if the
    survivor's income is 100% [S5]) and because the legacy "joint and 100% last survivor"
    form is still in the market [S6].
11. Only one carrier addresses the interaction: "if the first annuitant dies during the guaranteed
    payment period, the payments to the second annuitant will not be reduced until the end of
    that period", restated as the later of first death and the guaranteed-period end [S5].
    Neither anchor states a rule, so this one is adopted. It costs nothing to implement: because
    the certain floor pays the **full, unreduced** instalment, the `max(certain floor,
    life-contingent factor)` construction in `technical-notes.md` reproduces the deferral
    automatically. The alternative reading — a certain floor set at the *reduced* level — is
    supported by no retrieved document and is not implemented.
12. Each was found at a single insurer: temporary life payouts (5–30 years, income only while
    the annuitant lives, no benefit on or after death), at one carrier [S4]; Life with Percent
    of Premium Death Benefit (25% or 50% of premium), at a second [S5]; the pre-first-payment
    return-of-premium death benefit, at a third [S2].
13. The 1–4% compound menu is modal [S1] [S5] and the only menu that works for both qualified
    and nonqualified money under the sub-5% constant-percentage rule [R8]. Three percent is
    the upper-middle rung of that menu, the rate common to every observed menu
    [S1] [S2] [S4] [S5] [S6] [S8], and the rate in the only retrieved COLA illustration [S3].
14. **No fixed SPIA issuer publishes a commutation discount formula** (research gap).
    One carrier caps the withdrawal at "the present value of all remaining period certain
    payments, less any surrender charges" without stating a rate [S1]; a second
    discloses only that "an interest-rate adjustment will apply" [S2]; a third names the change
    in the **10-Year Constant Maturity Treasury (CMT) Index** between purchase and election
    as the driver but gives no formula [S5]. The only explicit formula found anywhere is
    a fourth's, on a 2008 *variable* contract: for the fixed account "the commuted
    value is the sum of payments less the interest that would have been earned from the
    effective date of the commuted value calculation to the date each payment would have
    been made" — a simple-interest discount — with 4% (the assumed investment return) on
    variable accounts [S7]. The composite therefore *assumes* a compound discount at a base
    4.00% [S7] moved one-for-one with the 10-year CMT change [S5]. Both level and functional
    form are a modeling invention: **[std]** and **[unverified]**. A simple-interest variant
    per [S7] is offered as a switch in `technical-notes.md`.
15. Excluded to keep the payment engine schedule-driven: one carrier's income payment
    acceleration (3× or 6× the monthly payment as a lump sum after 59½ and five years of
    payments, then no payments for three or six months, max two uses) [S2] [S3]; another's
    payment acceleration (six months of income at once, then five months of nothing, twice)
    [S5]. Both borrow forward from the schedule with no PV discount.

---

## Contractual mechanics

### Premium and income determination

A single premium `P` is paid at issue; where a state levies premium tax it is deducted
before income is determined [S6] [S7] [S11], so the amount annuitized is `P_net = P × (1 − τ)`.
The insurer converts `P_net` into a level annualized income `B(1)` using an unpublished
payout factor depending on form, annuitant age(s) and sex, certain period and COLA election.
No retrieved document discloses the mortality table, interest rate or expense loading behind
that factor [S1]–[S6] [S10]; one carrier states only that its published payout rates "include both
interest and return of principal" [S10]. Structural regularities across every anchor: payout
rate rises with age, female below male at the same age, joint below single, certain periods
and refund guarantees reduce income, and a COLA materially reduces the initial payment
[S3] [S9] [S10]. One carrier flags one genuine non-monotonicity: "there are limited situations
(primarily younger annuitants) where the same or essentially the same income payment is
available for longer guarantee periods or cash refund options" [S5].

### The five payout forms

With `inst` the scheduled instalment (annualized income ÷ frequency) and `G(t)` cumulative
income payments made through `t`:

1. **Life only** — instalment at each payment date while the annuitant lives; nothing on
   or after death [S1] [S2] [S4] [S5].
2. **Life with period certain** — instalment at every payment date in the certain period
   **regardless of survival**, and thereafter while the annuitant lives: an
   annuity-certain floor under a life annuity [S1] [S2] [S5]. On death within the certain
   period the beneficiary may generally elect the remaining scheduled payments **or** a
   lump-sum present value [S1] [S5] [S6] [S7].
3. **Life with cash refund** — life-only payments plus a lump sum at death of
   `max(0, P − G(death))`, "your original purchase payment minus the total income payments
   received" [S3]; nothing further once payments equal or exceed the premium [S5].
4. **Life with installment refund** — the same shortfall paid as *continuing scheduled
   payments* until cumulative payments equal the premium [S1] [S4] [S5] [S6]. One carrier gives
   the implementable equivalence: guaranteed payment period = **premium ÷ annualized income
   benefit amount** [S5], so this form is a life annuity with a derived certain period.
5. **Period certain only** — payments for a chosen 5–30 year term, no life contingency
   [S1] [S2] [S4] [S7]. (One carrier's lifetime-income form does not offer it; its option list is
   life-contingent throughout [S5].)

### Joint-life structure — the two reduction triggers

The sharpest structural variation in the U.S. market, modeled as a **switch, not a
footnote**. One carrier draws the line in the option names themselves: **"Joint Life"
options** — "Income payments can be reduced to 50%, 67%, or 75% of the current income
payment **upon the death of either annuitant**" [S2], restated as "Payments can be reduced
upon either person's death (Joint Life option)" [S3]; **"Joint and Survivor Life"
options** — "…reduced to 50%, 67%, or 75% of the current income payment **upon the death
of the primary annuitant**" [S2], so the secondary annuitant's death changes nothing while
the primary lives. A second carrier offers the same choice under per-option names — *Reduction
at Death of Annuitant* versus *Reduction at Death of Either Annuitant*, each crossed with
No Refund / Installment Refund / Period Certain, reductions of 1/2, 2/3 or 3/4 [S1] — and
a third carrier's contract names encode the identical asymmetry: *Two-Thirds Benefit While
**Either** Annuitant Survives* versus *One-Half Benefit While **Second** Annuitant
Survives First Annuitant* [S7]. Two consequences: the reduction applies to the **current**
income payment [S2], so a COLA keeps escalating the underlying level and the survivor's
payment with it; and under the primary-death trigger, if the secondary dies first **100%**
continues while the primary lives — a fourth carrier makes this mandatory for qualified
contracts with a non-spouse joint annuitant [S5].

### Cost-of-living adjustment

    B(y) = B(y−1) × (1 + g),   y ≥ 2,   g ∈ {1%, 2%, 3%, 4%}

Applied automatically on each anniversary of the annuity date [S1], "annually compounded"
[S4]; elected at issue, not cancellable or changeable, and it reduces the initial payment
[S1] [S2] [S4]. One carrier instead starts the increase "one year after the first income payment"
and requires the owner to be at least 59½ at the first payment [S5]; another applies it
to "the fixed payment level for the following year" on each contract anniversary and makes
the election irrevocable [S6]. A third warns that a payee may receive less total income
with an escalating payout than without one if the annuitant dies before life
expectancy [S4].

### Commutation and withdrawals

Withdrawals exist **only** on options that include a period certain [S1]. On the composite
design: one full or partial withdrawal each contract year after the first on *Period
Certain Only*; one **partial** withdrawal per year on *Single or Joint Life with
Period Certain*, reducing the period-certain payments but **not the lifetime payments
after the end of the period certain**; minimum $5,000; maximum the present value of all
remaining period certain payments less surrender charges; each remaining guaranteed
payment at least $100; not permitted in Oregon; surrender charge grading 8% in contract
year 2 to 1% in year 9 and 0% from year 10 [S1]. The insurer-side present value is not
disclosed by any fixed SPIA issuer (footnote 14). Three published behaviors a model must
reproduce:

- One carrier reduces payments through the end of the guaranteed period **by the
  withdrawal percentage elected**, and if the annuitant is alive at the end of that period
  full payments resume for life [S5]; another carrier states the same resumption rule for
  every form except pure Period Certain [S2].
- An **interest-rate adjustment** applies [S2], driven by the change in the 10-year CMT
  between purchase and election [S5] — the SPIA analogue of an MVA.
- On death within a certain period the beneficiary may take the remaining scheduled
  payments or their lump-sum present value [S1] [S5] [S6] [S7]; one carrier sells this as a
  death-triggered commutation rider, alongside a living commutation rider paying 10%–90%
  of the PV of all remaining payouts after year 1 [S4].

### No cash value, no nonforfeiture floor

There is no account value, no cash surrender value and no minimum paid-up benefit
[S1] [S4] [S5]. This is not a design choice: **immediate annuities are expressly excluded from
the scope of the Standard Nonforfeiture Law for Individual Deferred Annuities (Model #805)
§2.A**, alongside variable annuities, investment annuities, deferred annuities after
payments have commenced, and reversionary annuities [R5] [REG-R42]; the Variable Annuity
Model Regulation (#250) §7.A carves out the same list [REG-R43]. The modeling consequence is
that there is **no nonforfeiture minimum to track alongside the payment stream** — the
single most important difference from the deferred products in this library, whose minimum
nonforfeiture amount is a live state variable.

---

## Riders and options

**In scope (modeled):** the COLA escalation [S1] [S2] [S4] [S5] [S6]; the period-certain and
refund guarantee structures, which are payout forms rather than riders [S1] [S2] [S5]; and
certain-portion commutation with its surrender charge [S1].

**Described but out of scope:**

- **A future adjustment option at one carrier** — one-time scheduled income change, amount and
  date chosen at issue: increase up to **3×** the initial payment or decrease up to **½**;
  unavailable with joint options carrying a reduced benefit; an increasing adjustment is
  unavailable on qualified contracts [S2] [S3]. **A changing-needs option at a second** — one-time
  increase of 1%–400% (up to 5×) or decrease of 1%–50%, on or after the third anniversary
  of the income start date, fixed at purchase, nonqualified only [S5].
- **An income enhancement option** — one-time, index-triggered increase after the fifth
  anniversary if the **10-Year CMT** in the third full week of the preceding month is at
  least 2 percentage points above its level before the policy date; amount fixed at issue
  [S5]. The only index-linked income feature in any retrieved SPIA; no retrieved SPIA had
  caps, participation rates, spreads, buffers or floors.
- **Payment acceleration** [S2] [S3] [S5] (footnote 15). **A 30% cash withdrawal** —
  commutation against **life expectancy** on a life-only contract, 30% of the discounted
  value of remaining expected payments based on life expectancy at purchase, exercisable
  on the 5th, 10th or 15th anniversary, permanently cutting all future income by 30% [S5];
  the only retrieved feature that commutes a life-contingent stream.
- **Impaired-risk features** — one carrier's "age rating available" on one payout product,
  plus 10%/20% payment increases for health condition, a 50% increase for nursing home
  confinement and a survivor continuation option on a second product of the same carrier
  [S8]. From a 2017 producer document whose successor brochure 404s; re-verify before
  relying on it. AG 9-C governs valuation of substandard contracts and VM-V's "initial
  age" accommodates a **rated age** [R1] [REG-R41].
- **Temporary life payouts** (5–30 years, income only while alive, no death benefit),
  at one carrier only [S4] — tax-recognized (IRS Tables IV/VIII exist for it [R7]) but rare;
  **percent-of-premium death benefit** (25% or 50%, barred on qualified policies and in New
  York), at a second carrier only [S5]; **participating / dividend-paying SPIAs**, mentioned
  once [S11] with no mechanics located.

**How these excluded features would sort under AG 33, if any were added back.** The guideline's
two-category test turns on whether a benefit is *freely elected*, not on its label
[REG-R151 *Definitions* 1](#uslib-reg-r151). **Elective**, and therefore enough on their own to pull the contract
into AG 33's scope: **payment acceleration**, the **30% cash withdrawal** above, and the
certain-portion **commutation** already in the composite. **Non-elective**, and therefore not:
the **nursing-home confinement increase** and the **health-condition payment increases** on
the impaired-risk designs above [S8] — AG 33's non-elective list names "nursing home
benefits" expressly, and a benefit payable on a contingent event independent of an owner's
election stays non-elective however large the payment step. This is the correction that matters
most for reading older library notes, which had placed nursing-home waivers among the elective
set [REG-R151].

---

## Variations across insurers

1. **Survivor-reduction trigger — the sharpest structural variation.** Three patterns:
   (a) explicit two-family designs naming the trigger (*Joint Life* versus
   *Joint and Survivor Life* [S2] [S3]; *Reduction at Death of Either
   Annuitant* versus *Reduction at Death of Annuitant* [S1]; the
   two-thirds-either versus one-half-second-survives forms [S7]); (b) a continuous
   survivor percentage with tax-driven trigger rules (40%–99% at one carrier, where a spouse joint
   annuitant on a qualified policy may use either trigger but a non-spouse only the
   primary-death trigger [S5]); (c) legacy discrete last-survivor forms (a
   Joint and 50% / 100% last survivor pair [S6]).
   **Chosen: pattern (a) in its *Joint Life* / *Joint and Survivor Life* form** [S2] [S3] —
   two triggers × three percentages × four guarantee variants — the cleanest published
   statement, and it maps directly onto a boolean switch in the payment engine.
2. **Survivor percentage menus.** 50/67/75 [S2]; 1/2, 2/3, 3/4 [S1]; 2/3 or 1/2 by form
   [S7]; 50/100 [S6]; continuous 40–99 [S5]. Chosen: {50, 66⅔, 75, 100} (footnote 10).
3. **Certain-period range.** 5–30 years is standard [S1] [S2] [S4] [S5] [S7]; the older
   product in the survey caps at 20 [S6]; qualified money is capped near 10 years by RMD rules
   [S2] [R8]. Chosen: 5–30 with a 10-year default.
4. **COLA menus.** 1–4% modal [S1] [S5]; 2–4% [S2]; 1–3% [S6]; 1–5% compound [S4]; up to 6%
   [S8]. **No CPI-linked option was found anywhere.** Chosen: 1–4% fixed compound — the only
   menu working for both qualified and nonqualified money under the sub-5% rule [R8].
5. **Liquidity — where designs diverge most.** *None*: a first carrier's base contract
   [S4]; a second carrier's life-contingent contracts, where "no lump sum payment is
   available during the lifetime of annuitant(s)" [S7]. *Certain-period-only,
   charge-bearing*: a third carrier — one withdrawal a year, $5,000 minimum, capped at the
   PV of remaining certain payments, with the 8%-to-1% nine-year surrender charge, the only
   published SPIA surrender-charge schedule found [S1]. *Percentage-band rider*: the first
   carrier's commutation rider — 10%–90% of PV after year 1, excluded on life-only,
   temporary life and certain periods under 10 years [S4]. *Full PV commutation with income
   resumption*: a fourth carrier — up to 100% of PV, unlimited withdrawals [S2] [S3]; and a
   fifth carrier's once-only withdrawal of up to 100% of PV [S5]. *Against life
   expectancy*: the fifth carrier only [S5]. **Oregon** is repeatedly carved out of
   withdrawal features [S1] [S2]; **New York** out of the first carrier's commutation
   riders [S4] and the fifth's percent-of-premium death benefit [S5].
   **Chosen: the certain-period design** [S1] — the only one with a published charge
   schedule, and confining commutation to the certain (non-life-contingent) portion keeps
   the mortality and liquidity models separable.
6. **Minimum premium** ($10,000 cluster [S1] [S4] [S5] [S6] versus $25,000 [S2]; chosen
   $10,000) and **death benefits before income starts** (only one carrier publishes a
   pre-first-payment return-of-premium benefit, extended to terminal illness with ≤ 12
   months' life expectancy [S2]; excluded with the deferral window, footnote 3).
7. **Vintage caveat.** The consumer brochure [S6] is a 2004 document; the
   prospectus [S7] a 2008 SEC filing and a *variable* immediate annuity with a fixed-account
   option, not a pure fixed SPIA; the producer overview [S8] a 2017
   document. None is a currently-sold product spec; they supply design vocabulary and
   contractual precision. Composite parameter *levels* follow the current-era anchors
   [S1] [S2] [S3]; only *mechanics* come from the older documents.

---

## Regulatory context

**Standard Valuation Law (Model #820) and CARVM.** Model #820 is the enabling statute for
the Commissioners Annuity Reserve Valuation Method and makes the Valuation Manual
operative for annuity contracts [REG-R1] [REG-R3]. The codified text is **AP&P Appendix
A-820**, read at first hand on 2026-08-06 [REG-R153] — the manual turned out to be a **free
download**, not the paid publication the library had recorded [REG-R33], so the CARVM
construction no longer rests on the Model #820 print alone. Three A-820 paragraphs bear
directly on this product. **¶15** states CARVM as "the greatest of the respective excesses
of the present values, at the date of valuation, of the future guaranteed benefits,
including guaranteed nonforfeiture benefits" at the end of each contract year, less the
present value of future *valuation considerations* payable before that year end, with the
guaranteed benefits projected on the **contractual** mortality (if any) and interest basis
and the valuation basis entering through the discounting [REG-R153 ¶15](#uslib-reg-r153). **¶14** is the
scope gate: ¶15 reaches all annuity and pure endowment contracts **other than** group
annuity and pure endowment contracts purchased under an employer or employee-organization
retirement or deferred compensation plan (IRA/§408 plans excepted), which ¶13.b routes to a
**CRVM-consistent** method instead — an individual retail SPIA is squarely inside ¶15
[REG-R153 ¶¶13.b, 14](#uslib-reg-r153). **¶6** fixes the triple: for individual annuity and pure endowment
contracts the minimum standard is the **method of ¶¶14–15**, the **valuation interest rates
of ¶¶7–10**, and **the tables defined in Appendix A-821** [REG-R153 ¶6](#uslib-reg-r153). One carrier
states the application to this product directly: "For deferred annuities in the pay out
stage, Single Premium Immediate Annuities ('SPIA') and supplementary contracts, the path of
future guaranteed benefits with the highest present value is used to set policy reserves"
[S7].

**AG 33 does not reach a no-option SPIA.** Actuarial Guideline XXXIII — printed title
*"Determining CARVM Reserves for Annuity Contracts With Elective Benefits"* — has now been
read in full [REG-R151], and the finding for this product is a **negative** one. Its
applicability sentence reads: "This Actuarial Guideline shall apply to all annuity contracts
subject to CARVM, **where any elective benefits (as defined below) are available** to the
contract owner under the terms of the contract"; and its *Definitions* block classes as
**non-elective** "benefits payable under either a deferred or immediate annuity contract
(with or without life contingencies), **where no benefit options are available** under the
terms of the contract" [REG-R151 *Purpose*, *Definitions* 1](#uslib-reg-r151). A `life_only`, `cash_refund`
or `life_certain` contract of the composite design with **no commutation right** — the base
configuration here, `commutation_enabled = false` — is therefore **inside CARVM and outside
AG 33**. Add the commutation of the certain portion that two carriers offer [S1] [S5]
and the contract is inside both, because commutation is a benefit option "freely elected
under the terms of the contract"; the mechanics of that case are worked in
`technical-notes.md`, "Reserve basis". Two corrections to statements the library had carried
second-hand, recorded here because both were repeated wherever AG 33 was cited by title only.
**One, the effective date.** The guideline's own printed **Effective Date** block reads "This guideline shall be effective on **December 31, 1998**, affecting all contracts
issued on or after January 1, 1981", against the **December 31, 1995** date the library
carries from the Revenue Ruling for a differently-titled instrument — the 1 January 1981
issue-date reach is common to both, the effective date is not, and the extracted pages carry
**no amendment history**, so the natural reconciliation (a later revision) is an inference
this library does not assert. **Two, the elective/non-elective split.** **Nursing home
benefits are non-elective**, not elective — they are named in the *Definitions* non-elective
list — so any earlier library note placing nursing-home waivers among the elective set is
wrong [REG-R151]. AG 33's grade-in ran to 100% by December 31, 2000
and has **no live effect on any current valuation** [REG-R151 *Effective Date*](#uslib-reg-r151).

**VM-22 (PBR for non-variable annuities).** Effective for valuation dates on or after
**January 1, 2026**, VM-22 constitutes CARVM for non-variable annuities, with a three-year
elective transition under VM-A/VM-C/VM-M/VM-V and a small-company Annuity PBR Exemption
keyed to $1.0 billion of exemption reserves ($2 billion at group level) [R2] [REG-R36].
SPIAs sit in the **Payout Annuity Reserving Category** with DIAs, structured settlements,
annuitizations of host contracts, supplementary contracts and pension risk transfer
annuities; the stochastic reserve is **CTE70**; the prescribed **annuitization rate is
0%**; and the prescribed lapse table "is not applicable" for contracts with no account
value or surrender benefit — exactly this product [R2] [REG-R36]. **Correction to a common
citation error:** in the January 1, 2026 Valuation Manual, VM-22 is *entirely* the PBR
framework; the maximum valuation interest rate machinery for income annuities that VM-22
historically carried now sits in **VM-V Section 1** [R1] [R2] [REG-R36] [REG-R37]. A model
citing "VM-22 income annuity interest rates" against a current Valuation Manual is citing
the wrong section.

**VM-V Section 1 (maximum valuation interest rates for income annuities), and the AG IX
family.** For immediate annuities issued after December 31, 2017, VM-V §1 defines the
statutory maximum valuation interest rate complying with Model #820, "to be used in the CARVM
and for some contracts, CRVM" [R1] [REG-R37]. The quarterly rate is `Iq = R + S − D − E` with
spread deduction `E = 0.25%`, rounded to the nearest ¼% for non-jumbo contracts; jumbo
contracts (initial consideration ≥ $250 million) use a daily `Id = Iq + C(d−1) − Cq` rounded
to 1/100 of 1% [R1]. The bucket A–D follows from the **reference period** (premium
determination date to the earlier of the last non-life-contingent payment and the first
life-contingent payment, rounded to the nearest year) and the **initial age** (age **last**
birthday at that date, the *younger* annuitant on a joint contract, the rated age if valued
as impaired) [R1]. Of the annuity/CARVM guidelines indexed in VM-C, four touch this product —
**AG IX** (form classification of individual SPIAs), **AG IX-A** and **AG IX-C** (substandard
annuity mortality for impaired lives, structured settlements and SPIAs respectively) and
**AG IX-B** (methods under the SVL for individual SPIAs) [REG-R41] — and VM-V §1 expressly
**supersedes** AG 9-B and the valuation-interest-rate references in AG 9-C
[R1] [REG-R37] [REG-R41].

**The formulaic rate A-820 prints, for the issues VM-V §1 does not reach.** For a single
premium immediate annuity the A-820 dynamic formula is `I = .03 + W(R − .03)` with a **flat
weighting factor W = .80** — no Plan Type and no guarantee-duration lookup enters, those
being reserved to "other annuities" — and `R` is the **12-month average** of the Moody's
composite yield on seasoned corporate bonds ending June 30 of the calendar year **of** issue
or purchase, the result "rounded to the nearer one-quarter of one percent (1/4 of 1%)"
[REG-R153 ¶¶7.a.i(b), 8.b, 9.b](#uslib-reg-r153). Two limits are recorded rather than papered over: A-820
**prints no tie-break** for that rounding — the "ties down" convention belongs to VM-20
§3.C.2.a and must not be read off A-820 [REG-R153 ¶7.a.i](#uslib-reg-r153) [REG-R3] — and the whole ¶7
machinery is triggered "for policies issued on or after **the effective date of the
Codification**", a threshold date A-820 never prints [REG-R153 ¶7](#uslib-reg-r153). For immediate annuities
issued after 12/31/2017 this formula is superseded for maximum-rate purposes by **VM-V §1**
above [R1] [REG-R37]; it governs the older in-force layer.

**Valuation mortality (Model #821 and VM-M).** The **2012 Individual Annuity Reserving
(2012 IAR) Mortality Table** is the minimum valuation standard for individual annuity
contracts [R4], and it is **generational**:
`q_x^(2012+n) = q_x^2012 × (1 − G2_x)^n`, with `q_x^2012` from the 2012 IAM Period Table and
`G2_x` from Projection Scale G2 [R3] [R4] [REG-R59]. The result "shall be rounded to three
decimal places per 1,000… the rounding shall occur according to the formula above,
**starting at the 2012 period table rate**" — chaining already-rounded rates is explicitly
incorrect (male 30, `q^2012 = 0.741`; `q^2014 = 0.741 × 0.99² = 0.7262541 → 0.726`, **not**
`0.734 × 0.99 = 0.727`) [R3] [R4] [REG-R59]. Structured settlements funding tort,
workers'-compensation or LTD claims instead use **1983 Table "a" without projection** [R4].

**The effective dates, now read from the codified appendix rather than inferred.** A-820 ¶6
makes **Appendix A-821** the mortality leg by direct cross-reference, and A-821 prints the
table-by-issue-date rules the library previously did not carry [REG-R153 ¶6, A-821
¶¶10–12, 15](#uslib-reg-r153): the **Annuity 2000 Mortality Table** for any individual annuity or pure
endowment contract issued **1 January 2001 through 31 December 2014**; the **2012 IAR
Mortality Table** for issues **on or after 1 January 2015**; **1983 Table "a" without
projection** "solely when the contract is based on life contingencies and is issued to fund
periodic benefits arising from" tort or out-of-court settlements, workers'-compensation-type
claims, or long-term-disability claims where an annuity replaces continuing disability
payments; and the **1994 GAR Table** for annuities purchased under a group annuity or pure
endowment contract, **for which no effective date is printed**. A-821 also **prints the 2012
IAM Period Table and Projection Scale G2 in full**, both sexes, age nearest birthday, at its
Appendices I–IV; the male-30 anchor above (`1000·q = 0.741`, `G2 = 0.010`) is confirmed
against the printed tables [REG-R153]. **Two limits stay open.** A-821 prints **no standard
for an individual annuity issued before 1 January 2001**, so the valuation table for the
oldest in-force layer is not sourced here; and the **1994 GAR**, **Annuity 2000** and **1983
Table "a"** are **named and not printed**, so A-821's 1994 GAR projection formula
`q_x^(1994+n) = q_x^1994 · (1 − AA_x)^n` is not computable from library sources
[REG-R153].

**Nonforfeiture — expressly inapplicable.** Model #805 §2.A excludes **immediate
annuities** (and deferred annuities after payments commence) from the Standard
Nonforfeiture Law [R5] [REG-R42]. **Correction to a common misstatement:** Model #805's
indexed nonforfeiture rate is the lesser of 3% and the five-year CMT (rounded to the
nearest 1/20th of 1%) reduced by 125 basis points, **subject to a floor of 15 basis points
(0.15%) — not 1%** [REG-R42]. That floor governs the deferred products in this library and
is stated here only so it is not mis-applied to a SPIA, which has no nonforfeiture floor
at all.

**Disclosure and suitability.** **Correction to a common citation error:** the **Annuity
Disclosure Model Regulation is Model #245**, not #250 — #250 is the *Variable Annuity Model
Regulation* [REG-R45] [REG-R43]. Model #245 §3.A excludes "immediate and deferred annuities
containing no non-guaranteed elements" from scope [REG-R45], so a plain fixed SPIA of the
composite design falls outside the annuity disclosure and illustration rules entirely; a
participating SPIA paying dividends [S11] would not. Model #275 (2020 best-interest
revision) applies to the recommendation and bears on distribution cost and replacement
behavior, not on contract cash flows [REG-R46].

**SEC registration.** A fixed SPIA of this design is a state-regulated insurance contract
and is not SEC-registered [unverified — no retrieved document states this as a legal
conclusion]. The verified contrast: the single premium immediate **variable** annuity is
registered and sold by prospectus, and the only SEC-filed document in this research is
exactly that — a Rule 497(c) prospectus [S7] — carrying separate-account charges a fixed
SPIA does not have (M&E maximum 1.00% / current 0.40%; administrative expense 0.20%; total
separate account maximum 1.20% / current 0.60%; no annual contract fee) [S7].

**IRC §72 — exclusion ratio.** For a nonqualified SPIA each payment splits into an
excludable return of investment and a taxable interest element, at **exclusion ratio =
investment in the contract ÷ expected return** [R6] [R7] [REG-R55]; the exclusion "shall not
exceed the unrecovered investment in the contract immediately before the receipt of such
amount" [R6], and unrecovered investment remaining at death is deductible on the annuitant's
final return [R6]. Expected return uses the IRS actuarial tables by payout form, with a
**refund feature adjustment** *reducing* the investment in the contract by the Table III/VII
percentage × min(net cost, total guaranteed return) — the adjustment that must be applied to
cash-refund and installment-refund SPIAs [R7]. **The tax-free amount per payment is fixed in
dollars at the first payment and does not increase with COLA increases** [R7], so a COLA
SPIA's taxable proportion rises over time. The §72(q) 10% penalty does not apply to
distributions "under an immediate annuity contract" [R6] [S11], but one carrier warns that adding a
withdrawal feature can retroactively expose pre-59½ payments to the 10% tax plus interest
[S5], and a contract offering "an option to receive a lump sum in full discharge of the
obligation" is a *disqualifying form of payment or settlement* under Regs. §1.72-6(d)(3)
[R7]. Immediate annuities are also valid §1035 exchange destinations [REG-R56]. Taxation is
a policyholder-side computation generating no insurer cash flow.

**IRC §401(a)(9) — qualified contracts.** Payments must be periodic, at intervals not
exceeding one year, and **nonincreasing** except as permitted; a **constant percentage
increase applied at least annually at a rate less than 5% per year** is permitted, as are
increases tracking an eligible cost-of-living index [R8] [REG-R57]. The period certain is
capped by the uniform lifetime table denominator at the annuity starting date [R8],
operationalized by one carrier as ≤ 10 years (9 for an inherited IRA) [S2]. Non-spouse
survivor percentages are capped by the MDIB table, 52% at a 40+ year age gap up to 100% at
≤ 10 years; a spouse may always take 100% [R8]. The 2024 RMD final regulations (T.D. 10001,
applicable for calendar years beginning January 1, 2025) finalize this framework and add
the QLAC and partial-annuitization rules that matter to the DIA chassis [REG-R58].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-immediate_annuity-r1
[R10]: #uslib-immediate_annuity-r10
[R11]: #uslib-immediate_annuity-r11
[R2]: #uslib-immediate_annuity-r2
[R3]: #uslib-immediate_annuity-r3
[R4]: #uslib-immediate_annuity-r4
[R5]: #uslib-immediate_annuity-r5
[R6]: #uslib-immediate_annuity-r6
[R7]: #uslib-immediate_annuity-r7
[R8]: #uslib-immediate_annuity-r8
[REG-R1]: #uslib-reg-r1
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R3]: #uslib-reg-r3
[REG-R33]: #uslib-reg-r33
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R43]: #uslib-reg-r43
[REG-R45]: #uslib-reg-r45
[REG-R46]: #uslib-reg-r46
[REG-R55]: #uslib-reg-r55
[REG-R56]: #uslib-reg-r56
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R59]: #uslib-reg-r59
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
