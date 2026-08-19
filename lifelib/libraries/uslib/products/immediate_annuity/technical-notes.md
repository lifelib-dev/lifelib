# Technical Notes

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite product defined in `product-spec.md` (same directory). This is
not any single insurer's product. [S#]/[R#] tags refer to the source list in `sources.md`,
numbering carried verbatim from `_research/immediate-annuity.md`; [REG-R#] tags refer
to the cross-product reference library
`references/regulatory-and-actuarial-references.md`, one shared numbering space now
running **R1–R157** with most of the **R73–R149** block unused (R1–R34 from
`_research/regulatory-actuarial.md`, R35–R72 from
`_research/regulatory-actuarial-annuities.md`, and R150–R157
from the AP&P Manual appendix reading of **2026-08-06** — of which **R151** (AG 33)
and **R153** (A-820 with A-821 and A-822) are cited here). **[std]** marks standardizations
introduced for the reference implementation. Parameter values are identical to those in
`product-spec.md`; the mechanics anchors are one carrier's SPIA [S1] and a second
carrier's [S2] [S3].

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows (income instalments to the
  annuitant, joint annuitant and beneficiary; certain-period and refund payments; cash-refund
  lump sums; commutation payments; maintenance expenses) for a single SPIA in payment.
  Discounting and reserves are not computed (see Valuation and reserve pointers).
- **Mortality is the model.** No premium after outset, no account value, no cash surrender
  value, no policyholder option other than certain-portion commutation [S1] [S4] [S5]. The only
  decrement is death; the only stochastic driver is longevity. There is **no lapse
  decrement** — a point VM-22 makes prescriptively for this reserving category: the prescribed
  lapse table "is not applicable" for contracts with no account value or surrender benefit,
  and the prescribed annuitization rate is 0% [R2] [REG-R36].
- **Projection frequency.** Monthly grid, `t = 1, 2, …` months from the annuity date
  **[std]**. Payment dates fall on the grid per the frequency `m`; day-count and business-day
  conventions are not modeled **[std]**.
- **Timing conventions [std].** COLA increases apply at the start of the month containing the
  anniversary of the annuity date (first at `t = 13`) [S1]. **Arrears is the default**: an
  instalment due at the end of month `t` requires survival to the end of month `t`; on advance
  timing it is paid at the period start and requires survival to the start. The arrears
  default follows VM-V's own prescribed weight-table cash flow model, which assumes "annuity
  payments are made at the end of each year" [R1]. Deaths are decremented at end of month; a
  death during month `t` means the life does not receive an arrears instalment due at the end
  of month `t`, and a survivor reduction likewise takes effect **from the instalment due at
  the end of the month of death** — not from the following payment date **[std]**. Both
  follow from evaluating `L(t)` at end-of-month survival, `lᵢ(t)`, and both must be applied
  the same way or the two decrements disagree by one payment period.
- **Age basis.** **Age nearest birthday (ANB)** **[std]**: one carrier defines contract age as
  age nearest birthday [S1]; the 2012 IAM/IAR family is tabulated ANB [R2] [R9]; IRS
  Publication 939 uses "the age at the birthday nearest to the annuity starting date" [R7].
  One place prescribes a **different** basis: VM-V's "initial age" for valuation-rate bucket
  selection is the annuitant's **age last birthday** at the premium determination date (the
  *younger* annuitant on a joint contract, or the rated age if valued as impaired) [R1].
  VM-22 supplies the conversion [R2]:
  `q(x)_ALB = [q(x)_ANB + (1 − q(x)_ANB)·q(x+1)_ANB] / (2 − q(x)_ANB)`.
- **Limiting age.** ω = 120. **No longer [std] on the valuation side**: A-821's printed 2012
  IAM Period Table runs to **age 120** for both sexes and prints `1000·q₁₂₀ = 1000.000`
  there, so ω = 120 is the table's own terminal age and no extrapolation is required for the
  valuation basis [REG-R153]. The printed rates also confirm the ultimate cap the 2012 IAR
  development report describes — **400.000 per 1,000 = 0.40000** — and expose a
  terminal-age asymmetry a shared array will hide: **female** rates reach 400.000 at age
  **108**, **male** rates are 380.000 at **105** and 400.000 from **106** [REG-R153] [REG-R60].
  (The development report's account of how that cap arises — the 10% margin holds to age 100,
  then grades down 1% a year until the cap is invoked, where the margin is zero [REG-R60] —
  is a construction property, not a terminal age.) The **[std]** extrapolation rule stays for
  the **best-estimate** basis, which runs on the 2012 IAM **Basic** table: A-821 prints only
  the *loaded* Period Table, so the Basic table's own tabulation limit is not sourced here.
- **Model points.** USD; single-contract model points projected on an expected
  (probability-weighted) basis: survival probabilities multiply scheduled per-contract cash
  flows. No aggregation logic is specified here. **Joint-life independence [std]** — the
  SOA/LIMRA payout study is explicit that its data cannot inform this: "no recognition is
  given to the secondary annuitant if alive while the primary annuitant is alive", because of
  under-reporting of secondary-annuitant deaths [R9].

**Relation to `uk/products/pension-annuity/technical-notes.md`.** The survival-indexed
payment engine is the same object — a scheduled instalment multiplied by a payment factor
blending a certain floor with life-contingent survival. The U.S. differences are all
structural:

| Dimension | UK pension annuity | U.S. SPIA |
|---|---|---|
| Best-estimate mortality | CMI-restricted SAPS/PMA-PFA tables, proxied by an ONS population table × α **[std]** | **2012 IAM Basic × Projection Scale G2**, generational, × an A/E factor from a public experience study [R3] [R9] [REG-R59] [REG-R61] |
| Valuation mortality | Solvency UK best estimate + risk margin (no prescribed table) | **2012 IAR** generational table with an explicit no-compound-rounding rule [R3] [R4] [REG-R59] |
| Escalation | RPI 0-floor with catch-up ratchet, LPI-5, fixed | **Fixed compound only** (1–4%); no RPI/LPI analogue and **no CPI-linked option in any retrieved U.S. document** [S1] [S2] [S4] [S5] [S6] [S8] |
| Death benefit on a refund basis | Value protection (v × P − payments) | **Cash refund** (P − payments) and **installment refund** (payments continue until P is recovered) [S1] [S3] [S5] |
| Guaranteed term | Guarantee period | **Period certain** (5–30 yrs), plus a *derived* certain period on refund forms = premium ÷ annualized income [S5] |
| Survivor reduction | Dependant percentage δ on the annuitant's death; the dependant's pension is an **additive second stream** that may run alongside the guarantee | δ on **either** the primary's death or **any** annuitant's death — a switch, not a parameter [S1] [S2] [S3] [S7]; the reduction **rescales the single stream** and is suspended by the certain floor [S5] |
| Taxation | Income taxed in full as pension income | **Exclusion ratio** under IRC §72 / IRS Pub. 939 [R6] [R7] [REG-R55] |
| Liquidity | None after cancellation window | Commutation of the **certain portion only**, net of a declining surrender charge [S1] |

---

## Model point attributes

| Attribute | Type | Example (anchor cell) |
|---|---|---|
| `premium` P | currency | 100,000 **[std]** |
| `premium_tax_rate` τ | float | 0.00 **[std]** (mechanism [S6] [S7] [S11]) |
| `annual_income` B(1) | currency p.a. | 6,000 **[std]** (spec footnote 8) |
| `form` | enum {life_only, life_certain, cash_refund, installment_refund, certain_only} — the five forms of [S1] [S2] [S4] [S5] | life_only (joint) **[std]** |
| `joint` | bool | true **[std]** |
| `primary_age` x₁ / `primary_sex` | int (ANB [S1]) / enum {M, F} | 65 / M **[std]** (spec footnote 2) |
| `joint_age` x₂ / `joint_sex` | int (ANB [S1]) / enum {M, F} | 62 / F **[std]** (spec footnote 2) |
| `survivor_pct` δ | float ∈ {0.50, 2/3, 0.75, 1.00} [S1] [S2] [S5] [S6] [S7] | 2/3 **[std]** (spec footnote 10) |
| `reduction_trigger` | enum {either, primary} [S1] [S2] [S3] [S7] | switch — both runs shown |
| `certain_months` n | int, 0 or 60–360 [S1] [S2] [S4] [S5] | 0 (120 when `life_certain`) **[std]** |
| `frequency` m | enum {12, 4, 2, 1} [S1] [S2] | 12 **[std]** |
| `timing` | enum {advance, arrears} | arrears **[std]** |
| `cola_rate` g | float ∈ {0, .01, .02, .03, .04} [S1] [S5] | 0.03 **[std]** |
| `commutation_enabled` | bool (certain-bearing forms only [S1]) | false in base **[std]** |
| `issue_state_excludes_withdrawal` | bool (Oregon [S1] [S2]; NY for [S4] riders) | false |
| `qualified` | bool | false **[std]** (spec footnote 1) |

`B(1)` is a *pricing* input, not a modeled output: no insurer publishes payout factors or
the pricing basis, so it must be taken from a quote or calibrated (spec footnote 8). The
model does **not** derive `B(1)` from `P`.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `B(y)` | Annualized income in policy year y, unreduced ("as if all annuitants alive") | anniversaries |
| `l₁(t)`, `l₂(t)` | Survival probabilities of primary / joint annuitant to end of month t; l(0) = 1 | monthly |
| `d₁(t)`, `d₂(t)` | Death densities, `dᵢ(t) = lᵢ(t−1) − lᵢ(t)` | monthly |
| `l_last(t)` | Probability at least one annuitant alive = l₁ + l₂ − l₁·l₂ **[std independence]** | monthly |
| `d_last(t)` | Last-death density = l_last(t−1) − l_last(t) | monthly |
| `G(t)` | Cumulative gross instalments scheduled through month t | payment dates |
| `n_R` | Derived installment-refund certain period (months) | once, at t = 0 |
| `θ_cum(t)` | Cumulative commutation fraction applied to certain-period instalments | on withdrawal |
| `CV(t)` | Commuted value of the remaining certain instalments | on request |

`G(t)` is a **deterministic** schedule: instalments payable while any covered life is alive
follow the deterministic escalation path, so the refund balance needs no path simulation.

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Instalment | B(y)/m at each payment date | [S1] [S2] |
| COLA rule | B(y) = B(y−1)(1+g) on each anniversary of the annuity date; compound; irrevocable | [S1] [S4] [S6] |
| Survivor benefit | δ × the **current** income payment | [S2] |
| Reduction trigger | death of either annuitant, or of the primary annuitant only | [S1] [S2] [S3] [S7] |
| Certain period | n months of instalments payable regardless of survival | [S1] [S2] [S4] [S5] |
| Cash refund | lump sum at death = max(0, P − G(death)) | [S1] [S3] [S5] |
| Installment refund | instalments continue until cumulative payments equal P | [S1] [S4] [S5] [S6] |
| Refund-implied guaranteed period | premium ÷ annualized income benefit amount | [S5] |
| Withdrawal cap / minimum / residual floor | PV of remaining certain payments less surrender charges / $5,000 / $100 per remaining payment | [S1] |
| Surrender charge sc(y) | yr 2: 8%; 3: 7%; 4: 6%; 5: 5%; 6: 4%; 7: 3%; 8: 2%; 9: 1%; 10+: 0% (no withdrawal in yr 1) | [S1] |
| Effect of a withdrawal on post-certain lifetime payments | none | [S1] [S2] [S5] |
| Cash surrender value | none, at any time | [S1] [S4] [S5] |
| Nonforfeiture floor | none — immediate annuities excluded from Model #805 §2.A | [R5] [REG-R42] |
| Charges to the policyholder | none ("zero fees") | [S1] |

### (b) Insurer-declared current elements (snapshot)

For a fixed SPIA this class is nearly empty: no credited rate, no cap, no participation
rate, no declared rider terms. Two quantities remain, and neither is published.

| Input | Value | Basis |
|---|---|---|
| Initial annual income per unit premium (the payout factor) | 6.00% of premium p.a. (= $6,000 on $100,000) | **[std]**, spec footnote 8 (i) |
| Commutation discount rate `j(t)` | 4.00% + (10-yr CMT(t) − 10-yr CMT(0)), compound | **[std]** [unverified], spec footnote 14 (ii) |
| Commutation discount convention | `compound` (default **[std]**) or `simple` (per [S7]) | (ii) |
| State premium tax τ | 0.00% | mechanism [S6] [S7] [S11]; rate **[std]** (iii) |

(i) **No insurer publishes payout factors, guaranteed annuity purchase rates or the
pricing basis** for a fixed SPIA (research gap). The only insurer-sourced anchors are
illustrations labelled "for illustrative purposes only": Joint Life Only, both 65,
$230,856 → $1,200/month ⇒ **6.24%** annualized; Life with 10-Year Period Certain, age 69,
⇒ **≈7.11%**; single life male 65 with a 3% COLA ⇒ **≈5.28%** initial [S3].
A low-reliability broker survey gives male 65 life-only **7.97%** with a 5–6% carrier
spread [S9]; a carrier's weekly rate table could not be captured [S10]. **Consequence: no
pricing or annuity-rate test against public data is possible.** `B(1)` is exogenous.
Note that the 6.00% **[std]** level sits **above** what the COLA-adjusted anchors imply
for this cell (≈4.5%; spec footnote 8): it is a round arithmetic anchor that makes the
worked example exact, not a price, and must be re-set from a quote before any output is
read as one.

(ii) **No fixed SPIA issuer publishes a commutation discount formula.** One carrier gives
only the cap [S1], a second only "an interest-rate adjustment will apply" [S2], a third
only the 10-Year CMT as driver [S5]. The one explicit formula located is on a fourth's
2008 *variable* contract: fixed-account commuted value = "the sum of payments less the
interest that would have been earned from the effective date of the commuted value
calculation to the date each payment would have been made" (simple interest), with 4% on
variable accounts [S7]. The reference implementation therefore **assumes** a basis and
flags it **[std]** and **[unverified]**; any implementation must carry the same flag.

(iii) Premium tax is deducted before income is determined [S6] [S7] [S11], but no source
quantifies a rate and state rates were not researched (research gap).

### (c) Behavioral / experience assumptions (modeler's view)

| Input | Recommended public basis | Basis tags |
|---|---|---|
| Base annuitant mortality | **2012 IAM Basic Table** (unloaded table underlying the 2012 IAM Period Table, developed from the 2002 experience table projected to 2012) with **Projection Scale G2**, applied generationally | [R3] [R2] [REG-R59] |
| A/E adjustment to best estimate | × **1.084** **[std]**, from the 2020–2024 SOA/LIMRA payout study: amount-basis A/E versus 2012 IAM Basic projected with G2 is **108.4%** overall (107.5% F, 109.4% M) | [R9] [REG-R61]; adoption **[std]** (iv) |
| Mortality improvement | Scale G2 only, applied generationally; no additional improvement in the base run **[std]** | [R3] [R4]; see (iv) |
| Substandard / rated lives | `q_rated = min(1, θ·q_be)`, θ ≥ 1 (equivalently a rated-age offset); θ = 1 in base | existence [S8]; VM-V "rated age" [R1]; overlay **[std]** |
| Lapse / surrender | **None** — no cash value, no surrender right | [S1] [S4] [S5] [R5]; VM-22 declares the lapse table inapplicable here [R2] |
| Annuitization | Not applicable (already in payout); VM-22 prescribes 0% | [R2] |
| Commutation utilization | 0% in the base run **[std]** | (v) |
| Maintenance expense | $60 per contract p.a., paid monthly while any payment obligation remains, inflating 2.5% p.a. | **[std]** (vi) |

(iv) The study measured **99.6%** A/E against 2012 IAM Basic *unprojected* and **108.4%**
against 2012 IAM Basic *projected with Scale G2* over 2020–2024, on 3,109,309
contract-years and 143,190 deaths from 23 parent company groups representing just over 80% of
industry sales [R9] [REG-R61]. The reading: **G2 has over-projected improvement** — actual
mortality is running about 8% heavier than the fully projected basis. A flat 1.084 on the
projected basis reproduces the study average and is the least-assumption starting point, but
it is **[std]**, because the study documents gradients the flat factor ignores: by attained
age, all groups with ≥65% credibility except 65–74 had A/E above 100%, with **65–69 at 80%**
and **70–74 at 92%**; by annual income band, A/E generally decreases as income rises, from
**126%** below $2,500 of annual income to **91.5%** at $50,000 or more — the classic amount-based
socio-economic gradient, directly relevant to any block segmented by policy size [R9]. A
production basis must reflect both. VM-22 additionally *requires*, for a "longevity segment"
(which a SPIA block is), that the industry and credibility-adjusted tables be brought forward
for improvement to the valuation date and that future improvement be reflected if it
increases the reserve [R2] [REG-R36].

(v) No public data on SPIA commutation take-up was located; the base run holds utilization at
zero so the payment engine is exercised in isolation. (vi) No insurer publishes expense
assumptions; the "zero fees" statement [S1] refers to charges to the policyholder, not the
insurer's cost. $60 p.a. is a round placeholder for in-payment administration; acquisition
cost is out of scope (single premium, priced in).

**Mortality tables are not embedded — and the two that matter here are now in different
states.** The **2012 IAM Period Table and Projection Scale G2 have been retrieved**: the
AP&P Manual is a free download, not the paid publication recorded at [REG-R33], and A-821
prints both tables in full, both sexes, age nearest birthday, at its Appendices I–IV
[REG-R153]. They are transcribed in `_research/appp-a820-a821-a822.md`, so the *valuation*
basis (2012 IAR = 2012 IAM Period × Scale G2, generational) is sourceable end to end, and
the rounding worked example is now cross-checked against the printed tables rather than
standing alone: male age 30, `1000·q^2012 = 0.741`, `G2₃₀ = 0.010` [R3] [R4] [REG-R153]. The
**2012 IAM Basic table — the unloaded table this model's best estimate runs on — is still
not retrieved**: A-821 prints the *loaded* Period Table only, and the Basic table is defined
in VM-M §2.C [R3]. Machine-readable versions of either are conventionally obtained from the
SOA's mortality table repository [unverified — not a source in the research file]. **The
model must load them; it cannot hard-code them**, and the two tables must not be
interchanged — the loaded Period Table is a valuation object, the Basic table a
best-estimate one.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| t | month index from the annuity date, t = 1, 2, …; policy year y(t) = ⌈t/12⌉ |
| m | payments per year (12/4/2/1); payment months T = {12k/m : k = 1, 2, …} (arrears); on advance the k-th instalment falls one full payment period earlier, at the start of month 12(k−1)/m + 1 |
| P, τ | single premium; premium tax rate. P_net = P(1 − τ) |
| B(y) | unreduced annualized income in policy year y; `inst(t) = B(y(t))/m` for t ∈ T |
| g | fixed compound COLA rate (0.03 **[std]**, ∈ {1%…4%} [S1] [S5]) |
| δ | survivor percentage (2/3 **[std]**, ∈ {50%, 66⅔%, 75%, 100%}) |
| trig | reduction trigger ∈ {either, primary} [S1] [S2] [S3] |
| n, n_R, n_eff | elected certain months; derived installment-refund months; effective certain months by form |
| x₁, x₂ | issue ages (ANB) of primary and joint annuitant |
| l₁(t), l₂(t) | survival probabilities; dᵢ(t) = lᵢ(t−1) − lᵢ(t) |
| l_last(t), d_last(t) | at-least-one-alive probability and last-death density |
| L(t), C(t), Φ(t) | life-contingent payment factor; certain-floor indicator 1{t ≤ n_eff}; payment factor max(C, L) |
| G(t) | cumulative gross instalments scheduled through month t |
| CV(t), j(t), sc(y), θ | commuted value; commutation discount rate; surrender charge rate; withdrawal fraction |
| c_e, π | maintenance expense p.a. (60 **[std]**) and expense inflation (0.025 **[std]**) |

Dimensional check: `B` is currency per annum; `inst = B/m` currency per payment; `P`, `G`,
`CV` and refund lump sums currency; `Φ`, `L`, `C`, `δ`, `θ`, `l`, `d` dimensionless; `n`,
`n_eff`, `n_R` months; `g`, `π`, `j`, `sc` rates. Every cash flow below is currency/month.

### COLA update (start of month 12(y−1)+1, y ≥ 2) [S1] [S4]

    B(y) = B(y−1) × (1 + g)

Escalation applies to the **unreduced** income level and continues after a survivor
reduction, because the contract reduces payments to δ "of the **current** income payment"
[S2]. One carrier instead starts the first increase one year after the first income payment [S5] —
one payment period later than the anniversary-of-annuity-date rule adopted here; the
difference is one instalment's escalation and is a **[std]** convention choice.

### The payment factor — one formula, five forms, two triggers

**Life-contingent factor `L(t)`** (survival measured at the payment point: end of month t
on arrears, end of month t − 12/m on advance — one full payment period earlier, i.e.
t − 1 when m = 12 **[std]**):

    single life:            L(t) = l₁(t)
    joint, trig = either:   L(t) = l₁(t)·l₂(t) + δ · [ l₁(t) + l₂(t) − 2·l₁(t)·l₂(t) ]
    joint, trig = primary:  L(t) = l₁(t) + δ · [ 1 − l₁(t) ] · l₂(t)
    period certain only:    L(t) ≡ 0

The `either` form pays the full instalment while **both** are alive and δ × instalment
while **exactly one** is alive [S2] [S3] — the second bracket is exactly
`P(at least one alive) − P(both alive)`. The `primary` form pays the full instalment while
the **primary** is alive irrespective of the joint annuitant's status, and δ × instalment
only when the primary is dead and the joint annuitant alive [S2] [S3]; this is also the
mandatory structure for qualified contracts with a non-spouse joint annuitant, where "if
the secondary annuitant dies first, 100% of payments continue while the primary lives" [S5].

**Certain floor `C(t) = 1{t ≤ n_eff}`**, with

    n_eff = n     for life_certain and certain_only, single or joint  [S1] [S2] [S4] [S5]
    n_eff = n_R   for installment_refund                              [S1] [S5]
    n_eff = 0     for life_only and cash_refund                       [S1] [S2]

**Master payment factor and annuity outgo** (t ∈ T):

    Φ(t) = max( C(t), L(t) )
    E[ANN(t)] = inst(t) × Φ(t) × ( 1 − θ_cum(t)·C(t) )

The `max` makes the certain period an **annuity-certain floor** rather than an additional
stream: during the certain period the full instalment is paid regardless of survival, and
`max` prevents paying `1 + L` [S1] [S2] [S5]. Two consequences:

- Because the floor pays the **full, unreduced** instalment, the construction automatically
  reproduces the published rule that a survivor reduction "will not be reduced until the end of
  that period" when the first death falls inside a certain period [S5] — no separate flag
  is needed (spec footnote 11).
- The `(1 − θ_cum·C)` term applies a prior commutation to certain-period instalments only;
  life-contingent payments after the certain period are untouched [S1] [S2] [S5].

**Derived installment-refund period.** Payments continue until cumulative payments equal
the premium [S1] [S4] [S5] [S6]:

    n_R = min{ t ∈ T : G(t) ≥ P }
    final instalment at n_R is trimmed to  P − G(n_R − 12/m)          **[std]**

Under a level path (the relevant case — the anchor carrier does not offer the COLA with Life with
Installment Refund [S1]) this closes to `n_R = (12/m)·⌈ m·P / B(1) ⌉` months, which is the
published rule "guaranteed payment period = premium paid ÷ annualized income benefit
amount" [S5] rounded up to a payment date. Anchor check:
`P/B(1) = 100,000/6,000 = 16.667 years = 200 months`.

**Cash refund lump sum** (at the death that terminates the income stream):

    E[CR(t)] = d_term(t) × max( 0, P − G(t−1) )                        [S1] [S3] [S5]
    d_term = d₁       single-life contract
    d_term = d_last   joint contract (offered only with δ = 100% [S5])

Measuring the balance at `t−1` implements "instalments already paid" for a mid-month death
under arrears **[std]**; on advance timing an instalment paid at the *start* of the death
month **has** been paid, so use `G(t)` in advance payment months or the lump sum is
overstated by one instalment.

**Maintenance expense** (`l_alive = l₁` single-life, `l_last` joint):

    IF(t)     = max( C(t), l_alive(t) )                                **[std]**
    E[EXP(t)] = (c_e / 12) × (1 + π)^(y(t)−1) × IF(t)                  **[std]**

**Total gross liability cash flow:**

    CF(t) = E[ANN(t)] + E[CR(t)] + E[COMM(t)] + E[EXP(t)]

There is no premium income in the projection (the single premium at t = 0 is a pricing
input) and no surrender outgo [S1] [S4] [S5].

### Mortality construction

    q_base(x, 2012+k) = q_x^{2012 IAM Basic} × (1 − G2_x)^k               [R3] [R2]
    q_be(x, cal)      = min( 1, AE × q_base ),  AE = 1.084                **[std]** from [R9]
    q_rated(x, cal)   = min( 1, θ × q_be ),     θ = 1 in base             **[std]**
    q_m(t)            = 1 − (1 − q_rated)^(1/12)                          **[std]**
    lᵢ(t)             = lᵢ(t−1) × (1 − q_m^{(i)}(t)),  i = 1, 2

`k` is the number of calendar years from 2012 to the projection year, so the basis is
**generational**, not period: each attained age in each future calendar year uses its own
improved rate. The A/E factor is applied to the *projected* basis, matching the study's
measurement convention [R9]. The **valuation** basis is a different table with a different
rounding rule and must not be conflated with the best estimate (see Valuation pointers).

### Commutation module (optional; certain-bearing forms only [S1])

Eligibility per the composite: `commutation_enabled`, `n_eff > 0`, policy year ≥ 2, not
Oregon, one withdrawal per contract year [S1].

    CV(t) = Σ_{ s ∈ T,  t < s ≤ n_eff }  inst(s) · (1 − θ_cum(t)) · v(t, s)

    compound (default **[std]**):  v(t, s) = (1 + j(t))^(−(s − t)/12)
    simple   (per [S7]):           v(t, s) = max( 0, 1 − j(t)·(s − t)/12 )
    j(t) = j₀ + [ CMT10(t) − CMT10(0) ],  j₀ = 4.00%    **[std]** [unverified]

Requested gross withdrawal `W`, with `5,000 ≤ W ≤ CV(t)` and each remaining guaranteed
payment staying at or above $100 [S1]:

    surrender charge = sc(y) × W                                        [S1]
    E[COMM(t)]       = W × (1 − sc(y))            (paid to the owner)
    θ_cum(t⁺)        = θ_cum(t) + (1 − θ_cum(t)) × W / CV(t)            [S5 pro-rata rule]

The pro-rata reduction implements one carrier's published rule that future income payments
through the end of the guaranteed period are reduced "by the withdrawal percentage elected",
with full payments resuming for life at the end of that period if the annuitant is alive
[S5]; another carrier states the same resumption rule for every form except pure Period
Certain [S2]. On a `certain_only` contract there is nothing to resume, so a 100%
withdrawal ends the contract.

### Monthly processing order

1. If `t = 12(y−1)+1`, y ≥ 2: apply `B(y) = B(y−1)(1+g)` [S1].
2. Decrement mortality: update `l₁`, `l₂`, `d₁`, `d₂`, `l_last`, `d_last`.
3. If `t ∈ T`: set `inst(t) = B(y(t))/m`; compute `C(t)`, `L(t)`, `Φ(t)`; record
   `E[ANN(t)]`; update `G(t) = G(t−) + inst(t)` (deterministic as-if-alive schedule).
4. Refund: if the form carries a cash refund, accrue
   `E[CR(t)] = d_term(t) × max(0, P − G(t−1))`.
5. Commutation (if enabled and eligible this contract year): evaluate `CV(t)`, apply `W`,
   record `E[COMM(t)]`, update `θ_cum`.
6. Accrue `E[EXP(t)]`.
7. Stop when `IF(t) < 10⁻⁶`, or when every covered life has passed the limiting age
   (`t/12 + x₁ > ω` and, if joint, `t/12 + x₂ > ω`), ω = 120 **[std]** — stopping on the
   primary's age alone would truncate a younger joint annuitant's tail.

---

## Policyholder behavior modeling

**There is almost none, and that is a cited product property rather than an omission.** The
contract is irrevocable, the income option and frequency cannot be changed after issue,
there is no account value and no surrender right [S1] [S2] [S3] [S4] [S5]. The model therefore
carries **no lapse decrement and no dynamic lapse formula** — the position VM-22 prescribes
for this reserving category [R2] [REG-R36].

The one live option is **commutation of the certain portion**, and no public utilization data
exists. Reference constructions, both **[std]**: a **deterministic** per-contract-year
utilization vector `u(y)`, zero in the base (shape anchors only — the feature requires the
owner to be 59½ or older [S2] [S5], is capped at the PV of remaining certain payments [S1] and
is barred in Oregon [S1] [S2]); or a **rate-driven dynamic** take-up, since commutation is
worth more when rates have fallen since issue (the interest-rate adjustment raises the
payout):

    u(y, t) = min( u_max, u_base(y) × max(0, 1 + κ·[ CMT10(0) − CMT10(t) ]) )

with `u_max = 0.10`, `κ = 20` **[std]** — pure shape assumptions calibrated to nothing, whose
only justification is directional: one carrier names the 10-year CMT change as the driver of the
withdrawal amount [S5] and another confirms an interest-rate adjustment applies [S2].

**Both constructions are best-estimate objects and are barred from a CARVM run.** Commutation
is an *elective benefit* under AG 33, and for elective benefits "incidence rates should not be
based on tables reflecting past company experience, industry experience or other expectations"
— the guideline substitutes trial sets **maximised over**, theoretically all rates 0% to 100%,
with 0% or 100% the typical optimum [REG-R151 *Definitions* 2](#uslib-reg-r151). A `u(y)` or `u(y, t)` vector
fed into a reserve calculation is therefore not a conservative approximation of CARVM; it is a
different quantity. (Note also that AG 33 reaches this product **only** because the commutation
right exists — see "Valuation and reserve pointers" below.)

Excluded by scope: payment acceleration (borrowing forward with no PV discount) [S2] [S3] [S5];
the 30% cash withdrawal, which commutes against **life expectancy** on a life-only contract
and permanently cuts all future income by 30% [S5] — the only retrieved feature that commutes
a life-contingent stream. Anti-selection enters at **outset**, not through in-force behavior:
voluntary annuitants self-select for longevity, and impaired lives are diverted to age-rated
contracts [S8] whose valuation is governed by AG 9-C and VM-V's "rated age" definition
[R1] [REG-R41]. The reference model carries this through θ, not through behavior dynamics.

---

## Worked example

**Configuration (anchor cell; parameters identical to `product-spec.md`).** P = $100,000;
τ = 0; B(1) = $6,000 p.a. **[std]** ⇒ `inst` = $500.00/month; joint form, primary male ANB
65, joint annuitant female ANB 62 **[std]**; monthly (m = 12) in arrears **[std]**; fixed
compound COLA g = 3% **[std]**; survivor percentage δ = 66⅔% **[std]**; no certain period
(n = 0). **Scenario: the joint (secondary) annuitant dies during month 14**; the primary
survives throughout. The two trigger conventions run side by side — this is the death that
distinguishes them.

Income levels: year 1 (t = 1–12) B = 6,000.00 ⇒ 500.00/month; year 2 (from t = 13)
B = 6,000 × 1.03 = 6,180.00 ⇒ 515.00/month; year 3 (from t = 25) B = 6,180 × 1.03 =
6,365.40 ⇒ 530.45/month. Reduced amounts: 2/3 × 515.00 = 343.33 and 2/3 × 530.45 = 353.63.

| t | Event | Unreduced inst(t) | CF, trig = **either** | CF, trig = **primary** |
|---|---|---|---|---|
| 1 | first monthly instalment (arrears) | 500.00 | 500.00 | 500.00 |
| 12 | 12th instalment | 500.00 | 500.00 | 500.00 |
| 13 | anniversary: B ← 6,180.00; 13th instalment | 515.00 | 515.00 | 515.00 |
| 14 | **joint annuitant dies during the month**; the instalment due at month end is the first scheduled payment date after the death | 515.00 | **343.33** | **515.00** |
| 15 | 15th instalment | 515.00 | 343.33 | 515.00 |
| 24 | 24th instalment | 515.00 | 343.33 | 515.00 |
| 25 | anniversary: B ← 6,365.40 | 530.45 | **353.63** | **530.45** |

**Trace and checks.**

- t = 14, `trig = either`. The death is decremented at the end of month 14, so the scenario
  values at the payment point are l₁ = 1, l₂ = 0:
  `L = l₁l₂ + δ(l₁ + l₂ − 2l₁l₂) = 0 + (2/3)(1 + 0 − 0) = 0.6667`; `C = 0`, so
  `Φ = 0.6667` and `CF = 515.00 × 2/3 = 343.33`, and the same at every later payment
  date. ✔ (Note the timing convention bites here, not at t = 15: the instalment due at the
  end of the month of death is already the first scheduled payment date after the death.)
- t = 14, `trig = primary`, same values: `L = l₁ + δ(1 − l₁)l₂ = 1 + 0 = 1`, so
  `CF = 515.00`. ✔ The joint annuitant's death is invisible to the payment stream while
  the primary lives [S2] [S3] [S5].
- **Reverse the death** (primary dies in month 14, joint annuitant survives; l₁ = 0,
  l₂ = 1): `L_either = 0 + (2/3)(0 + 1 − 0) = 2/3` and `L_primary = 0 + (2/3)(1)(1) = 2/3`.
  Both conventions pay 343.33 from t = 14. **The two triggers coincide on the primary's
  death and differ only on the secondary's** — which is precisely why the trigger must be a
  model switch, not a footnote [S1] [S2] [S3] [S7].
- **COLA continues after the reduction**, because δ applies to the *current* income payment
  [S2]: 343.33 becomes 353.63 at t = 25, not a frozen 343.33.
- **With a 10-year certain period** (n = 120): `C(t) = 1` for t ≤ 120, so
  `Φ(t) = max(1, L(t)) = 1` and every instalment from t = 14 to t = 120 is the **full**
  515.00 / 530.45 / …, with the reduction to δ beginning only at t = 121 — reproducing
  the cited deferral rule with no extra logic [S5].
- **Single-life with cash refund**, death in month 14: lump sum =
  `max(0, 100,000 − G(13)) = 100,000 − (12 × 500.00 + 515.00) = 93,485.00` [S1] [S3] [S5]. On
  **installment refund** (level path, no COLA [S1]) the derived certain period is
  `12 × 100,000/6,000 = 200 months` [S5].

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**; valuation layers consume them and are
cited, not reproduced:

- **Reserve method.** CARVM — for SPIAs, deferred annuities in payout and supplementary
  contracts, "the path of future guaranteed benefits with the highest present value is used
  to set policy reserves" [S7]; enabling statute Model #820 [REG-R1], codified at **AP&P
  Appendix A-820 ¶15**, with the scope gate at ¶14 (qualified-plan group annuity business
  excepted and routed to a CRVM-consistent method by ¶13.b) and the method/interest/mortality
  triple at ¶6 [REG-R153 ¶¶6, 13.b, 14, 15](#uslib-reg-r153). **AG 33 does not reach the base composite** — its
  applicability requires that elective benefits be available, and its non-elective definition
  expressly covers immediate annuity benefits "where no benefit options are available"; a
  commutation right puts the contract inside it [REG-R151].
- **VM-22 (PBR), valuation dates on or after 1/1/2026.** SPIAs sit in the **Payout Annuity
  Reserving Category**; aggregate reserve = SR + DR for contracts passing the Single
  Scenario Test + reserves for contracts valued under VM-A/VM-C/VM-M/VM-V; **SR = CTE70**;
  the additional standard projection amount is **disclosure-only** under VM-31; a three-year
  transition election and a $1.0bn/$2.0bn Annuity PBR Exemption apply [R2] [REG-R36].
- **Prescribed mortality for the VM-22 Standard Projection Amount** (also the "little or no
  data" floor): `q_x^(2012+k) = q_x^{2012 IAM Basic}·(1 − G2_x)^k·F_x`, with `F_x` from
  **Table 6.8** (payout-annuity factors, age nearest birthday, reproduced in full at [R2])
  [R2] [REG-R36]. Note this is the **same base table and projection scale** as the
  best-estimate construction above, with a prescribed `F_x` overlay in place of the
  experience A/E factor.
- **Maximum valuation interest rate.** **VM-V §1**, not VM-22, for immediate annuities issued
  after 12/31/2017: `Iq = R + S − D − E` with `E = 0.25%`, bucketed A–D by reference period
  and initial age (age **last** birthday, younger annuitant on a joint contract), rounded to
  the nearest ¼% quarterly for non-jumbo contracts and to 1/100 of 1% daily for jumbo
  contracts (initial consideration ≥ $250 million) [R1] [REG-R37]. VM-V §1 supersedes AG 9-B
  and the interest references in AG 9-C [R1] [REG-R37] [REG-R41]. For the **older in-force
  layer** VM-V §1 does not reach, the A-820 formulaic rate is `I = .03 + W(R − .03)` with a
  **flat W = .80** for single premium immediate annuities — no Plan Type and no
  guarantee-duration lookup — and `R` the **12-month** average of the Moody's composite yield
  on seasoned corporate bonds ending June 30 of the calendar year **of** issue or purchase,
  rounded "to the nearer one-quarter of one percent (1/4 of 1%)" [REG-R153 ¶¶7.a.i(b), 8.b,
  9.b](#uslib-reg-r153). **A-820 prints no tie-break** for that rounding (the "ties down" convention is VM-20
  §3.C.2.a's, not A-820's), and its ¶7 trigger — "the effective date of the Codification" —
  is a date A-820 never prints; both stay unresolved in the primary text
  [REG-R153 ¶7](#uslib-reg-r153) [REG-R3].
- **Valuation mortality.** **2012 IAR** generational table:
  `q_x^(2012+k) = q_x^{2012 IAM Period}·(1 − G2_x)^k`, **rounded to three decimal places per
  1,000, with the rounding applied to the value computed from the 2012 period rate each time
  — never by compounding an already-rounded prior-year rate** [R3] [R4] [REG-R59]. Verified
  example: male 30, `q^2012 = 0.741` ⇒ `q^2014 = 0.741 × 0.99² = 0.7262541 → 0.726`, **not**
  `0.734 × 0.99 = 0.727`. Chaining rounded rates is wrong in a way a single-year unit test
  will not catch. **The table-by-issue-date rules are now sourced** from the codified
  appendix that A-820 ¶6 cross-references: **Annuity 2000** for individual issues **1/1/2001
  through 12/31/2014**, **2012 IAR** for issues **on or after 1/1/2015**, **1983 Table "a"
  without projection** for the structured-settlement carve-out (tort and out-of-court
  settlements, workers'-compensation-type claims, LTD claims where an annuity replaces
  continuing payments), and **1994 GAR** for group-purchased annuities, **with no effective
  date printed for the group rule** [REG-R153 ¶6, A-821 ¶¶10–12, 15](#uslib-reg-r153). **Still open:** A-821
  prints **no standard for an individual annuity issued before 1/1/2001**, and the 1994 GAR,
  Annuity 2000 and 1983 Table "a" are **named and not printed**, so A-821's 1994 GAR formula
  `q_x^(1994+n) = q_x^1994·(1 − AA_x)^n` is not computable from library sources [REG-R153].
- **Tax and GAAP.** IRC §807: tax reserve = greater of net surrender value (zero here) and
  92.81% of the NAIC-prescribed method — CARVM for annuities — capped at the statutory
  reserve [REG-R16]. Under LDTI, payout annuities carry a **liability for future policy
  benefits** with annually reviewed assumptions [REG-R34]; ASOP 10 governs that work
  [REG-R71].
- **Standards for the modeling work.** ASOP 7 (life cash flow analysis) [REG-R27]; ASOP 22
  (asset adequacy — a SPIA block is a classic cash-flow-testing exposure) [REG-R29]; ASOP 56
  (modeling: validation, documentation, model risk) [REG-R32]; ASOP 54 in pricing mode
  [REG-R70]. ASOP 52 is scoped to **VM-20 life products** [REG-R31]; the reference library
  catalogues no VM-21/VM-22 analogue, i.e. **no ASOP for principle-based reserves for
  annuities** [unverified as an absolute negative — inferred from the bibliography, not from
  an ASB statement].

**Policyholder taxation is not an insurer cash flow.** Under IRC §72 each payment splits at
**exclusion ratio = investment in the contract ÷ expected return**, capped at the unrecovered
investment [R6] [REG-R55], with expected return from the IRS actuarial tables by payout form
and a **refund feature adjustment** reducing the investment in the contract by
`Table III/VII percentage × min(net cost, total guaranteed return)` [R7]. Worked IRS example:
at age 65, $21,053 buying $100/month for life with a full refund feature gives years
guaranteed = 21,053/1,200 = 17.54 → 18, a Table VII percentage of **15%**, a refund value of
$3,158 and adjusted investment of **$17,895** [R7]. Critically for a COLA contract, "the
tax-free part remains the same even if the total payment increases due to variation in the
annuity amount such as cost of living increases" [R7] — the excluded dollar amount is fixed
at the first payment, so the taxable proportion of a 3%-escalating SPIA rises every year.
This is a **policyholder-side computation**: it changes no insurer liability cash flow and
belongs in an illustration or in-force tax module, not in `CF(t)`.

---

## Key sensitivities and model risks

Dominant assumptions, in order:

1. **Longevity level.** The liability is a life-contingent payment stream with **no
   offsetting decrement** — no lapse, no cash value. Lower mortality lengthens every stream
   with nothing to offset it. The **[std]** A/E factor of 1.084 is the weakest calibrated
   link: the study reports 99.6% against unprojected 2012 IAM Basic but 108.4% against the
   G2-projected basis [R9], so applying the factor to the wrong base misstates the mortality
   level by about 8%.
2. **Longevity trend.** Scale G2 is a fixed, dated improvement scale and the 2020–2024
   experience says it has **over-projected** [R9]. Sensitivity-test a scaled G2 (e.g. 50%
   and 150% of tabulated improvement) before anything else. VM-22 requires future improvement
   to be reflected for longevity segments where it increases the reserve [R2].
3. **The survivor-reduction trigger.** A *structural* sensitivity, not a parametric one: on
   the anchor cell the `primary` trigger pays 100% for the primary's whole lifetime whenever
   the joint annuitant dies first, while `either` drops to δ. Over a joint 65/62 cell this is
   a first-order liability movement, and it is invisible if the trigger is buried as a
   footnote rather than modeled as a switch [S1] [S2] [S3] [S7].
4. **Initial income level `B(1)`.** The largest source of model error is not an assumption at
   all: **no insurer publishes payout factors or the pricing basis**, so `B(1)` is exogenous
   and unverifiable (spec footnote 8; assumption note (i)). Every result is conditional on
   it, and no pricing test against public data is possible.
5. **COLA rate.** A 3% compound escalation roughly doubles the instalment over 24 years;
   liability duration and longevity sensitivity both rise with `g`. The menu is bounded at
   4% for qualified-eligible designs by the sub-5% constant-percentage rule [R8].
6. **Commutation basis.** Both the discount rate and its functional form are invented
   **[std] [unverified]** (assumption note (ii)). Latent while utilization is zero, but any
   run with `commutation_enabled` inherits an unsupported assumption — flag it in output.

Known modeling pitfalls:

- **Certain-period double-counting.** During the certain period the instalment is certain —
  do not also weight it by survival. `max(C, L)` prevents paying `1 + L`; an additive
  construction silently doubles the guarantee.
- **Rounding the valuation table by compounding.** `q^(2012+k)` must be rounded from the 2012
  period rate every time; chaining rounded rates gives 0.727 where the manual requires 0.726
  [R3] [R4] [REG-R59] [REG-R153 A-821 ¶14](#uslib-reg-r153).
- **Applying the A/E factor to the wrong base.** 1.084 belongs on 2012 IAM Basic **projected
  with G2**; on the unprojected table the study's own answer is 99.6% [R9].
- **Period versus generational.** The 2012 IAM Period Table is one calendar year's rates; the
  2012 IAR is that table plus Scale G2 applied generationally [R3] [R4]. Using the Period
  Table without projection understates longevity throughout.
- **Age-basis mismatch.** The tables are ANB; VM-V's initial age for rate bucketing is ALB
  [R1] [R2]. Mixing them shifts every lookup by up to a year (conversion in Model scope).
- **Survival-measurement timing.** Arrears instalments require survival at the payment date,
  advance instalments at the period start. Using end-of-period survival for advance payments
  understates the liability by about one period's mortality per payment — material at high
  ages. Symmetrically, **refund balance timing**: `G` must net instalments *paid before
  death* on arrears (`G(t−1)`), but an advance instalment paid at the **start** of the death
  month has been paid — use `G(t)` there or the cash refund is overstated by one instalment.
- **Refund-form certain period.** `n_R` is derived from `P/B(1)` and moves with the pricing
  input; hard-coding it (e.g. at 200 months) breaks every sensitivity run on `B(1)`.
- **Joint-life independence.** The `l₁·l₂` products assume independence **[std]**;
  broken-heart and shared-lifestyle dependence overstate the expected survivor stream
  modestly, and the payout experience study cannot inform the assumption because it gives no
  recognition to a living secondary annuitant [R9].
- **Commutation applied to the wrong slice.** A withdrawal reduces certain-period instalments
  only; applying `θ_cum` to the life-contingent tail contradicts every retrieved contract
  [S1] [S2] [S5].
- **Treating exclusion-ratio tax as a cash flow.** It is a policyholder computation and
  generates no insurer flow; modeling it as an outgo distorts the liability.
- **Vintage and scope drift.** VM-22 is in its first year of effectiveness with a three-year
  transition and a pending LATF directive targeted at the 1/1/2027 manual [R2]; VM-V weight
  tables, Table X spreads and the published quarterly rates live on the NAIC Industry tab and
  were not retrieved [R1]. Re-check both each January.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-immediate_annuity-r1
[R2]: #uslib-immediate_annuity-r2
[R3]: #uslib-immediate_annuity-r3
[R4]: #uslib-immediate_annuity-r4
[R5]: #uslib-immediate_annuity-r5
[R6]: #uslib-immediate_annuity-r6
[R7]: #uslib-immediate_annuity-r7
[R8]: #uslib-immediate_annuity-r8
[R9]: #uslib-immediate_annuity-r9
[REG-R1]: #uslib-reg-r1
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R3]: #uslib-reg-r3
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[REG-R33]: #uslib-reg-r33
[REG-R34]: #uslib-reg-r34
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R55]: #uslib-reg-r55
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R61]: #uslib-reg-r61
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
