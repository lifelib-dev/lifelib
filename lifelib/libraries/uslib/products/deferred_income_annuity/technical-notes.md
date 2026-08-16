# Technical Notes

**Status:** Draft, 2026-08-04 (all cited sources accessed 2026-08-04).

**Scope note.** A reference liability cash-flow projection model for the standardized composite product
defined in `product-spec.md` (same directory); not any single insurer's product. [S#]/[R#] refer to
`_research/deferred-income-annuity.md`; [REG-R#] refers to
`references/regulatory-and-actuarial-references.md`, whose shared numbering now runs **R1–R157** as one
space, with most of the **R73–R149** block unused (R1–R34 of life origin, provenance
`_research/regulatory-actuarial.md`; R35–R72 annuity-specific, provenance
`_research/regulatory-actuarial-annuities.md`;
**R150–R157 the AP&P Manual appendix and actuarial-guideline prints read on 2026-08-06**).
**[std]** marks standardizations introduced for
the reference implementation; [unverified] marks claims not confirmed against a retrieved document. Parameter
values are identical to those in `product-spec.md`.

**Two structural facts govern the whole design.**

1. **There is no account value.** No credited rate, no index crediting, no M&E or rider charge, no surrender
   charge, no free-withdrawal corridor, no market value adjustment, no benefit base, no interim value
   [S1 fn.1](#uslib-deferred_income_annuity-s1) [S2] [S4] [R13]. Consequently there is **no lapse decrement** — VM-22's standard-projection lapse
   section is expressly "not applicable" to contracts with no account value or surrender benefit [R9] — and
   no annuitization decrement (prescribed at 0% [R9]). The full list is in `product-spec.md`, "Parameters
   that do not exist for this product". Do not synthesize any of them.
2. **The income phase is the immediate-annuity payout chassis.** Payout forms, refund and certain-period
   guarantees, survivor reduction and its interaction with a guarantee period, COLA escalation and
   payment-survivorship weighting are specified in `products/immediate_annuity/technical-notes.md` and are
   **not restated** here. These notes cover the **deferral phase**, the **transition**, the **in-force
   options** and the **QLAC overlay**, and define only the payout-phase quantities the DIA changes — chiefly
   the refund base, which is cumulative premiums rather than a single premium.

---

## Model scope and conventions

- **Purpose.** Project gross expected liability cash flows — premiums in; deferral death benefits, income
  payments, refund benefits, acceleration and commutation payments, maintenance expenses out — for a
  single-contract model point. Reserves are not computed (see "Valuation and reserve pointers").
- **Projection frequency.** Monthly, indexed `t = 0, 1, 2, …` from issue **[std]**. Monthly is natural
  because the modal payment frequency is monthly [S1] [S2] [S3] [S4] and because the 13-month minimum deferral
  and the 13-month premium cut-off are expressed in months [S2] [S4] [R9].
- **Timing conventions [std].** Premiums are received at the **start** of month `t`. Income is paid in
  **arrears** at the **end** of each payment period, matching `products/immediate_annuity/product-spec.md`;
  the model exposes `pay_timing ∈ {advance, arrears}` because no retrieved DIA document states the
  convention. Deferral death benefits are paid at the **end of the month of death**. `T` is a month index and
  the income start date is the **start of month `T`** (exactly `T/12` years after issue); under arrears the
  first payment falls one payment period later, `12/m` months after `T` — at `m = 12`, at the end of month
  index `T`, i.e. `T + 1` months from issue. Consequently deaths in months `t < T` are deferral-phase deaths
  and deaths in months `t ≥ T` are payout-phase deaths.
- **Age basis.** Age nearest birthday (ANB) **[std]**: MassMutual states contract issue age on an ANB basis
  [S2]; prescribed VM-22 payout mortality is ANB with a conversion formula supplied for age-last-birthday
  companies [R9]; the 2012 IAM Basic and Period tables were developed ANB [R15] [REG-R59].
- **Model points.** Single-contract model points on an expected (probability-weighted) basis: the in-force
  factor `l(t)` multiplies every per-contract cash flow. Joint cells carry two lives and a joint status. No
  aggregation logic is specified here.
- **Decrement set.** Mortality only; `l(t)` never decrements for lapse or surrender [R9].
- **Rounding.** Full precision internally, cash flows to cents **[std]**. Generational mortality rates follow
  the Valuation Manual rule — three decimal places per 1,000, computed **from the 2012 period rate each time,
  never by compounding an already-rounded prior-year rate** [R9] [REG-R59]. **A-821 ¶14 prints the same rule and
  the same worked counter-example**, so this is now sourced twice over rather than once [REG-R153].

---

## Model point attributes

| Attribute | Type | Example (anchor cell **[std]**) |
|---|---|---|
| `issue_age`, `sex` | int (ANB); enum {M, F} | 60; F |
| `joint`, `joint_age`, `joint_sex` | bool; int; enum | false |
| `survivor_pct`, `reduction_trigger` | enum {0.50, 0.6667, 0.75, 1.00}; enum {either, primary} | n/a |
| `convertible_joint` | bool | false |
| `market_type` | enum {NQ, TradIRA, RothIRA, QLAC} | NQ |
| `income_form` `f` | enum {LO, LO_ROP, CR, IR, PC(n)} + joint variants | CR |
| `certain_period` `n` | years, 10–30 (PC forms only) | n/a |
| `income_start_month` `T` | int months from issue; `13 ≤ T ≤ 360` and start age ≤ 85 | 240 |
| `premium_schedule` | list of (month, amount) | [(0, 100000), (60, 50000)] |
| `db_form` | enum {ROP, NONE} | ROP |
| `cola_rate` `c` | 0.00, or 0.01–0.04 | 0.00 |
| `pay_frequency` `m`, `pay_timing` | enum {12, 4, 2, 1}; enum {arrears, advance} | 12; arrears **[std]** |
| `adjust_right`, `adjust_uses` | bool; int | true; 1 |
| `accel_uses`, `accel_months` | int 0–5; int {3, 6} | 2; 6 |
| `commutation_allowed` | bool (extended case only) | false |
| `guaranteed_future_rates` | bool — whether purchase rates for future premiums are guaranteed [R13 §1.B(1)(h)](#uslib-deferred_income_annuity-r13) | false **[std]** |
| `qlac_premium_room` | currency (QLAC only) | n/a |

Anchor cell **[std]**: Female 60 ANB, nonqualified, $100,000 at issue plus $50,000 at the start of policy
year 6, income start at attained age 80, Life with Cash Refund, monthly in arrears, return-of-premium death
benefit in deferral, no COLA. Used identically in `product-spec.md` and in the worked example.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `B(t)` | Guaranteed **annual** income purchased to date, before COLA | on each premium; on adjustment exercise |
| `CP(t)` | Cumulative premiums paid — the deferral death benefit base and the refund base | on each premium |
| `l(t)` | In-force (survival) probability at the **start** of month `t`; `l(0) = 1` | monthly |
| `phase(t)` | {deferral, payout, terminated} | at `t = T`; on death; on exhaustion of a non-life-contingent form |
| `T(t)` | Current income start month (mutable once) | on adjustment exercise |
| `RG(t)` | Remaining refund balance `= max(0, CP(T) − income scheduled through the end of month t−1)`; the `t−1` is the arrears convention (an instalment due at the end of the death month has not been paid) | monthly in payout, refund forms |
| `n_g` | Derived guarantee period in years | fixed at `T`; re-derived if `B` changes |
| `adjust_used`, `accel_used` | bool; int | on exercise |
| `accel_blackout(t)` | months of suspended payments remaining | monthly |
| `commuted(t)`, `resume_month` | extended case: guaranteed payments commuted; month the life-contingent tail resumes | on exercise |
| `sel_mult(t)` | mortality selection multiplier applied after an adjustment exercise | on exercise |
| `qlac_room(t)` | Indexed QLAC limit less premiums paid to this and any other intended QLAC | on each premium |

---

## Assumption inputs

Class (a) is contractual and fixed at issue; class (b) is the only insurer-declared element in the product;
class (c) is the modeler's view of experience.

### (a) Contractual / guaranteed elements

| Input | Value | Basis |
|---|---|---|
| Guaranteed income per slice | Fully guaranteed at the time each premium is paid | [R13 §3.H(1)](#uslib-deferred_income_annuity-r13) |
| Deferral death benefit | 100% of cumulative premiums, no interest, lump sum | [S1] [S2] [S3] [S4] [R13 §3.I(1)(a)](#uslib-deferred_income_annuity-r13) |
| Permitted DB calculation methods | % of premiums; % of premiums plus interest; flat dollar; combination | [R13 §3.I(1)](#uslib-deferred_income_annuity-r13) |
| Forms with **no** deferral DB | Life Only, Joint Life Only; and Single Life — No Death Benefit (deferral ≥ 10 yrs, start date locked) | [S1] [S2] [S3] [S4] |
| Minimum / maximum deferral; max start age | 13 months / 30 years; attained age 85 | [S2] [S4] [R9]; choices **[std]** |
| Premium cut-off | No premium within 13 months of the income start date | [S2] [S4] |
| Income start date adjustment | One-time ±5 years; new date ≥ 13 months after the last premium; option, day of month and frequency locked | [S1] [S2] [S3] [S4] |
| Adjustment repricing inputs | Originally scheduled payment; new date; Moody's Seasoned Baa Corporate Bond Yield at the request date; Annuity 2012 Mortality Table; contractual interest-rate-change adjustment | [S2] (A2000 in the NYL formulation [S1]) |
| COLA | Fixed compound 1%–4% on each income-start anniversary; elected at issue, irrevocable | [S2] [S3] [S4]; menu **[std]** |
| Payment acceleration | 6 monthly payments in one sum then 5 months without; 2 uses; age 59½; nonqualified | [S1] [S4]; count **[std]** |
| Commutation (extended) | ≤100% of the PV of remaining **guaranteed** payments; interest-rate adjustment applies; life-contingent tail resumes | [S4] [S5] [R13 §3.F](#uslib-deferred_income_annuity-r13) |
| Loans, surrender, withdrawals in deferral | None; prohibited | [S1] [S2] [R13 §3.P](#uslib-deferred_income_annuity-r13) |
| Explicit charges | None disclosed in any source | [S1] [S2] [S3] [S4] |
| Minimum monthly income | $100 | [S2] |
| Small-benefit termination right | Company may terminate for present value after 2 years without considerations if the paid-up benefit is under $20 monthly | [R10 §3.B](#uslib-deferred_income_annuity-r10); not modeled **[std]** |

### (b) Insurer-declared current elements

There is exactly one: the **annuity purchase rate** applied to each premium, set "at the time each purchase
payment is made" [S3] on "the attained age of the annuitant, the specified income commencement date and
specified income option, and the company's then current annuity purchase rates" [R13 §3.B(1)(b)](#uslib-deferred_income_annuity-r13), floored at
the income a new contract of the same class would buy [R13 §3.B(1)(c)](#uslib-deferred_income_annuity-r13).

**No purchase-rate table was obtained, and none is published.** The Compact expressly relieves the insurer of
disclosing the deferral-period basis: "Since the premium and income benefit are fully defined in the
contract, the mortality table and interest rate used in the deferral period and for determining the
contractually specified income payable do not need to be disclosed in the contract or the Actuarial
Memorandum" [R13 §1.B(1)(a)](#uslib-deferred_income_annuity-r13). The purchase-rate function below is therefore an explicit **[std]**
construction, not a sourced parameter. An in-force model that reads `B` from an administration extract does
not need it; it is required only for new business, subsequent premiums and the start-date adjustment.

| Input | Value | Basis |
|---|---|---|
| Pricing interest rate `i_p` | 4.75% annual effective | **[std]** (a) |
| Expense and profit load `L` | 6.0% of gross premium | **[std]** (b) |
| Pricing mortality | 2012 IAM Basic × Scale G2 generational, ANB, × 100% | **[std]** (c) |
| Interest-rate-change adjustment spread `s_adj` | 100 bp deducted from the Baa yield | **[std]** (d) |
| Commutation interest-rate adjustment margin `m_c` | 50 bp | **[std]**/[unverified] (e) |

(a) A pure modeling assumption; no DIA source discloses a pricing rate. Read it as a long-duration
general-account portfolio yield net of default costs; the prescribed VM-V portfolio credit-quality
distribution (5% Treasuries / 15% Aa / 40% A / 40% Baa [R9]) is a reasonable calibration frame.
(b) Reconciliation so the load is not arbitrary: on the anchor cell `L × 100,000 = $6,000` against roughly
$900 of present-valued maintenance expense (item in class (c), survivorship-weighted at `i_p`, computed on
the worked example's illustrative survival anchors extended past age 85 — the figure is sensitive to that
extension), a few thousand of first-year distribution cost, and the balance as profit margin. Sensitivity-test it before
relying on any absolute income level.
(c) VM-22 prescribes `q_x^(2012+n) = q_x^(2012) · (1 − G2_x)^n · F_x` on the 2012 IAM Basic table with `F_x`
from Table 6.8 for the standard projection [R9]; the pricing basis uses the same table and scale without the
prescribed `F_x` loading, at a **[std]** A/E of 100%.
(d) The contract's "interest rate change adjustment" is named but never quantified in any retrieved source
[S1] [S2]; 100 bp is a placeholder that keeps the repriced income directionally correct [S4] [S5].
(e) **The Pacific Life interest-rate adjustment charge formula was not found** in the fact sheet [S4] or the
client guide [S5]; it would appear only in the contract or the actuarial memorandum. Equation (13) implements
only the Compact's stated principle [R13 §3.F(7)](#uslib-deferred_income_annuity-r13) and is [unverified].

### (c) Behavioral and experience assumptions

| Input | Recommended public basis | Tags |
|---|---|---|
| Payout-phase mortality | 2012 IAR / 2012 IAM Basic with Scale G2, generational, ANB, per Model #821 and VM-M §1.J; the appendix print says the same — **A-821 ¶11** prescribes the 2012 IAR table for any individual annuity or pure endowment contract issued on or after January 1, 2015, and A-820 ¶6 makes A-821 the mortality leg of the CARVM triple by direct cross-reference | [R9] [R14] [REG-R59] [REG-R60] [REG-R153 ¶6](#uslib-reg-r153) |
| Payout-phase A/E | 2020–2024 Individual Payout Annuity Mortality Experience Study — 23 parent groups / 26 companies, >80% of industry sales, 3.1m contract-years, 143,190 deaths, shown against the 2012 IAM table; **the study explicitly includes deferred income annuities** | [R15] [REG-R61] |
| Deferral-phase mortality | **The weakest link.** The only public sources are a 2011–2015 deferred annuity mortality study and a 2006 analysis of mortality during the deferred period, both identified via the SOA index, neither fetched | [REG-R65]; A/E **[std]** = 1.00 |
| Mortality improvement | Scale G2 only (generational); none additional in the base run | **[std]** |
| Lapse / surrender | **None.** "For contracts in which there is no account value or surrender benefit, such as some contracts within the Payout Annuity Reserving Category …, this section is not applicable" | [R9] |
| Annuitization | Not applicable; prescribed at 0% for the standard projection | [R9] |
| Maintenance expense | $50 per contract per year escalated 2.5% (VM-22 prescribes $50 for individual Payout Annuity Reserving Category contracts, escalated by `[1.025]^(valuation year − 2015)` in year one and 2.5% thereafter, plus 7 bp on a present-value base for contracts without an account value) | [R9]; adoption as best estimate **[std]** |
| Premium persistency | Deterministic schedule, factor 1.00 | **[std]** (f) |
| Start-date adjustment take-up | 1.5% p.a. of exposure, one exercise, 60% defer / 40% advance, with rate and selection overlays | **[std]** |
| Payment acceleration take-up | 2% p.a. of exposure among eligible contracts | **[std]** |
| Commutation take-up (extended) | 1.5% p.a. of exposure, rate-insensitive in the base | **[std]** |

(f) DIA subsequent premiums are wholly discretionary and no source publishes a distribution of them. The base
model projects the model point's stated schedule with no attrition and exposes `pp(y)`. **Dump-in risk
differs structurally from a fixed deferred annuity's:** because a DIA prices each premium at *then-current*
rates there is no rate guarantee to select against — unless the contract guarantees paid-up annuity rates for
future premiums, which the Compact requires to be described where offered [R13 §1.B(1)(h)](#uslib-deferred_income_annuity-r13). VM-22 requires
"additional premium dump-ins under high guarantees in low-rate environments" to be reflected [REG-R36]; that
risk is switched on by `guaranteed_future_rates` and is off in the base **[std]**.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t`, `y` | policy month index `t = 0, 1, 2, …`; elapsed years `t/12`; policy year `y = floor(t/12) + 1` |
| `m` | payments per year (12 in the base) |
| `x`, `x(t)` | issue age ANB; attained age `x + floor(t/12)` |
| `T` | income start month (`13 ≤ T`; `x + T/12 ≤ 85`) |
| `k`, `P_k`, `t_k`, `d_k` | premium index, amount, payment month; `d_k = (T − t_k)/12` = deferral of slice `k` in years |
| `f` | income form elected at issue (immutable [S1] [S2] [S4]) |
| `B(t)`, `CP(t)`, `c` | guaranteed **annual** income before COLA; cumulative premiums; COLA rate |
| `l(t)`, `q(t)` | in-force probability at the start of month `t`, `l(0) = 1`; probability of death during month `t` |
| `i_p`, `v` | pricing interest rate; `v = (1 + i_p)^(−1)` |
| `L` | expense and profit load, fraction of gross premium |
| `_s p_x` | probability a life aged `x` survives `s` years on the pricing basis |
| `a^{(m)}_y(f; i)` | APV at age `y` of $1 **per annum** of income in form `f`, payable `m`-thly in arrears |
| `a_def(x, d, f; i)` | APV at the premium date of $1 per annum of income in form `f` beginning `d` years hence |
| `A_rop(x, d; i)` | APV at the premium date of $1 payable at the end of the month of death within a `d`-year deferral |
| `pr(x, d, f)` | purchase rate: annual income per $1 of premium |
| `n_g`, `e`, `g` | derived guarantee period in years; annual maintenance expense per contract; its escalation rate |
| `i_e(t)`, `i_c(t)` | repricing rate for a start-date change; discount rate for a commutation |

**Dimensional check.** `a_def` and `a^{(m)}` are APVs *per unit of annual income*, so they carry units of
years; `A_rop` and `L` are dimensionless (per $1 of premium). Hence `pr = (dimensionless)/(years) = 1/year`,
`P_k × pr` is currency per year, and dividing by `m` gives the currency amount of one payment.

### Pricing kernel: the purchase rate

    a_def(x, d, f; i)  =  v^d  ·  _d p_x  ·  a^{(m)}_{x+d}(f; i)                                       (1)

`a^{(m)}_y(f; i)` is the APV of the payout form, built from the payment factor `Φ(t) = max(C(t), L(t))`
defined in `products/immediate_annuity/technical-notes.md` (certain floor `C`, life-contingent factor `L`,
survivor percentage and reduction trigger included); for a certain-and-life form with guarantee period `n_g`,

    a^{(m)}_y(f; i)  =  Σ_{j=1..m·n_g} (1/m)·v^{j/m}  +  Σ_{j>m·n_g} (1/m)·v^{j/m}·_{j/m} p_y          (2)

APV of the return-of-premium death benefit over the deferral, benefit paid at the end of the month of death
**[std]**, with `q^[j]_x` the probability of death in the `j`-th month:

    A_rop(x, d; i)  =  Σ_{j=1..m·d}  v^{j/m} · _{(j−1)/m} p_x · q^[j]_x                                (3)

The purchase rate follows from the equivalence principle applied **per premium**:

    P·(1 − L)  =  B_slice · a_def(x, d, f; i_p)  +  1{db_form = ROP} · P · A_rop(x, d; i_p)

    ⇒  pr(x, d, f)  =  [ (1 − L) − 1{ROP} · A_rop(x, d; i_p) ] / a_def(x, d, f; i_p)                   (4)

**[std]**, for the reasons in assumption class (b). Equation (4) makes the central design fork quantitative:
setting `1{ROP} = 0` raises the numerator from `(1 − L) − A_rop` to `(1 − L)`, so the no-death-benefit form
buys strictly more income for the same premium, by the factor `(1 − L)/((1 − L) − A_rop)`. That is the
mortality-gain economics behind MassMutual's separately-conditioned Single Life — No Death Benefit option
[S2] and behind the silent removal of the return of premium when Life Only is elected [S1] [S3] [S4].

**Refund forms and the circularity they create.** The Compact treats income payments made before a
return-of-premium death benefit as period certain income [R13 definitions](#uslib-deferred_income_annuity-r13), which licenses the closed form.
For **installment refund**, payments "continue in the same amount and frequency until they equal the purchase
payments" [S2], so the form is exactly a certain-and-life annuity with

    n_g  =  CP(T) / B                                                                                  (5)

For **cash refund** the benefit is instead a lump-sum shortfall paid at death [S1] [S2], so (2) is an
approximation; the exact factor adds a decreasing term benefit

    a^{(m)}_y(CR)  =  a^{(m)}_y(life only)
                    + (1/B) · Σ_j v^{j/m} · _{(j−1)/m} p_y · q^[j]_y · max(0, CP(T) − (j−1)·B/m)        (6)

Both (5) and (6) put `B` on both sides. Resolve by fixed-point iteration on `B` (three iterations from a
life-only start are ample), or use the (5) approximation for both refund forms **[std]** with (6) as a check.
Under arrears, a death between `T` and `T + 1/m` yields a cash refund of the full `CP(T)`, no payment having
been made.

### Deferral-phase recursions

    CP(t)  =  CP(t−1)  +  Σ_{k : t_k = t} P_k,                                        CP(−1) = 0        (7)
    B(t)   =  B(t−1)   +  Σ_{k : t_k = t} P_k · pr( x(t_k), (T − t_k)/12, f ),        B(−1)  = 0        (8)
    l(t+1) =  l(t) · (1 − q(t)),                                                      l(0)   = 1        (9)

Equation (8) is the core of the product: **income is additive across slices**, each priced at the annuitant's
attained age and the remaining deferral **at its own payment date** [R13 §3.B(1)(b)](#uslib-deferred_income_annuity-r13) [S3]. Nothing
accumulates; there is no balance to roll forward. Admissibility tested at each premium: `P_k ≥ 10,000` (first)
or `≥ 500` (subsequent) [S1] [S2] [S3] [S6]; `CP(t) ≤ 1,500,000` without approval **[std]**; `t_k ≤ T − 13`
[S2] [S4]; and, on a QLAC, `CP(t) ≤ qlac_room`.

### Monthly processing order

At month `t`, with `l(t)` the in-force probability at the **start** of the month:

1. Roll attained age and policy year; look up `q(t)`, applying `sel_mult(t)` if a start-date adjustment has
   been exercised.
2. **Premium** (deferral only): if a scheduled premium falls at `t`, test admissibility, compute `pr` by (4),
   update `CP` and `B` by (7)–(8). Cash flow in: `P_k · l(t)`.
3. **Option exercises** (start of month): start-date adjustment (deferral, once); payment acceleration or
   commutation (payout only). Any of these may reset `B`, `T`, `accel_blackout` or `commuted`.
4. **Income payment** (`t ≥ T`, arrears — at the end of the month): pay
   `B(t)/m · (1+c)^{floor((t − T)/12)}` weighted by the form's payment survivorship, unless suppressed by an
   acceleration blackout or a commutation.
5. **Death benefits**: deaths during month `t` at rate `q(t)`; if `t < T` pay the ROP benefit (or nothing
   under a no-death-benefit form); if `t ≥ T` pay the form's refund benefit.
6. **Expenses**: `(e/12)·(1+g)^{y−1} · l(t)`.
7. **Decrement**: apply (9).

Order note **[std]**: contractual transactions precede the decrement, and the end-of-month income payment is
contingent on survival to that point — which is what the arrears convention means.

### Expected cash flows (per contract, month `t`)

| Cash flow | Formula | Sign |
|---|---|---|
| Premium income | `l(t) · Σ_{k: t_k = t} P_k` | + |
| Deferral death benefit | `1{t < T} · 1{ROP} · CP(t) · l(t) · q(t)` | − |
| Income payments | `1{t ≥ T} · (B(t)/m) · (1+c)^{floor((t−T)/12)} · L_pay(t)` | − |
| Refund / certain-period benefits | per form; cash refund `= l(t)·q(t)·RG(t)` — under arrears the instalment due at the end of the death month has not been paid, which is why `RG` is measured through month `t−1` (same convention as the immediate-annuity notes) | − |
| Payment acceleration | `accel_months · B(t)/m · l(t) · h_acc(t)` at exercise, offset by suppressed payments in the blackout | − |
| Commutation (extended) | `CV(t) · l(t) · h_com(t)` at exercise, offset by suppressed guaranteed payments | − |
| Maintenance expense | `(e/12)·(1+g)^{y−1} · l(t)` | − |

`L_pay(t)` is the form-specific payment-survivorship weight defined in the immediate-annuity notes: `l(t)`
for a life-only payment, certain inside a guarantee period, and the survivor-percentage-weighted joint status
for joint forms. **The DIA-specific change is only the base of the guarantee: `CP(T)`, the sum of all
premiums, not a single premium** [S2] [S4]. There is **no surrender cash flow row**, and none should be added.

### Income start date adjustment

Exercised once at month `t_e` in deferral, moving `T → T′` with `|T′ − T| ≤ 60` months, `T′ ≥ (last premium
month) + 13`, and `T′` inside the maximum deferral and maximum income-start age [S1] [S2] [S3] [S4]. The
disclosed recalculation keys on the originally scheduled payment, the new date, the Moody's Seasoned Baa
Corporate Bond Yield at the request date, a published annuity mortality table, and a contractual
interest-rate-change adjustment [S1] [S2]. Implemented as actuarial equivalence at `t_e` **[std]**:

    i_e(t_e)  =  Baa(t_e) − s_adj                                                                     (10)
    B′        =  B(t_e) · a_def( x(t_e), (T − t_e)/12, f; i_e ) / a_def( x(t_e), (T′ − t_e)/12, f; i_e )  (11)

Direction check: `a_def` decreases in `d`, so `T′ > T ⇒ B′ > B` and `T′ < T ⇒ B′ < B`, matching Pacific
Life's statement that advancing reduces and deferring increases the payment [S4] [S5]. Two refinements the
disclosed recipe does not mention and the reference model therefore does **not** apply: the ROP exposure
changes with deferral length (the `A_rop` term in (4)), and `CP` is unchanged so the derived guarantee period
(5) shifts. Both are flagged rather than modeled **[std]**. Not available on Life Only or Joint Life Only
[S1] [S3] [S4], nor on the Single Life — No Death Benefit option, whose annuity date cannot be changed [S2].

### Payment acceleration

At exercise month `t_a` (payout phase, attained age ≥ 59½, nonqualified, monthly frequency,
`accel_used < 2`) [S1] [S2] [S3] [S4] the contract pays `n_a = 6` monthly payments in one sum and suspends
payments for the following `n_a − 1` months [S1]. Accelerated payments are made **unconditionally**, so the
insurer forgoes the survivorship and interest discount on payments 2 through `n_a`:

    Cost(t_a)  =  (B/m) · Σ_{j=1..n_a−1} [ 1 − v^{j/m} · _{j/m} p_{x(t_a)} ]                          (12)

Small but real, and the reason the feature is capped in uses and gated at 59½ [S1] [S2] [S4]; the 59½ gate
itself is driven by the IRC §72(q) 10% additional tax [R8] [REG-R55]. Not available on a QLAC [S4].

### Commutation (extended case only)

    i_c(t)   =  i_p  +  max(0, r_ref(t) − r_ref(0))  +  m_c                                           (13)
    CV(t_c)  =  Σ_{j ∈ J_g(t_c)} (B/m) · (1 + i_c(t_c))^{−(j − t_c)/12}                               (14)

`J_g(t_c)` is the set of remaining **guaranteed** (non-life-contingent) payment months and `r_ref` a
reference market rate. Equation (13) is one-sided — it rises with rates and does not fall — implementing the
Compact's stated intent that the adjustment "reduce interest risk in the event of rising interest rate after
issue" and its required disclosure that "the higher the interest rate the lower the commuted value"
[R13 §3.F(7)](#uslib-deferred_income_annuity-r13). **The actual contractual formula is not published anywhere** [S4] [S5], so (13) is
**[std]**/[unverified]. After a 100% commutation the payments in `J_g` are suppressed; if the annuitant is
alive at `resume_month` (the end of the would-be guaranteed period) income **resumes until death** — the
life-contingent tail is not commuted [S4], and only Period Certain is fully extinguished. Unavailable on the
Life Only family [S4]; prohibited on a QLAC after the required beginning date other than a rescission period
not exceeding 90 days [R1 (q)(1)(iv)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(4)](#uslib-deferred_income_annuity-r2); interlocked with acceleration and the start-date
adjustment by six-month waiting periods in both directions [S4].

### Convertible versus non-convertible joint life

The most model-relevant pricing subtlety in the family, and the only place a joint DIA differs structurally
from a joint SPIA. With lives aged `x₁, x₂` and survivor percentage `s`:

**Non-convertible** — priced on "a single payout assumption that both annuitants will be alive on the annuity
date" [S2], and if one annuitant dies in deferral the contract continues on the option chosen at issue [S2]:

    P(1−L) − P·A_rop  =  B_J · [ a_def^{(both)} + s · Σ_{i=1,2} a_def^{(only i)} ]                    (15)

**Convertible** — priced on "two different payout assumptions": the joint payout if both are alive at the
annuity date, and the corresponding single life payout for each annuitant if only one is alive and the
contract converts [S2]:

    P(1−L) − P·A_rop  =  B_J^c · a_def^{(both)}  +  Σ_{i=1,2} B_S^{(i)} · a_def^{(only i)}            (16)

    a_def^{(both)}    =  v^d · _d p_{x₁x₂}(both alive) · a^{(m)}_joint(f)
    a_def^{(only i)}  =  v^d · ( _d p_{x_i} − _d p_{x₁x₂} ) · a^{(m)}_{x_i + d}(single f)

Because `B_S^{(i)}` (a full single-life payout) exceeds `s·B_J` (the reduced survivor amount), the right-hand
side of (16) carries more value per unit of `B_J`, so `B_J^c < B_J` — reproducing MassMutual's statement
exactly: "In general, if both annuitants are alive on the annuity date, the joint life payout will be
**lower** with a convertible joint life annuity option" [S2]. The convertible variant also caps the period
certain at 10 years and is unavailable with the inflation protector [S2]. Base model: non-convertible
**[std]**; `convertible_joint` switches to (16).

### QLAC overlay

A validation-and-restriction layer over the same recursions. It generates **no cash flows of its own** — it
caps premiums, restricts forms, constrains `T`, disables features and raises compliance flags. Loss of QLAC
status changes the owner's RMD position, not the insurer's liability cash flows.

| Rule | Implementation | Basis |
|---|---|---|
| Premium limit | `qlac_room(t) = Limit(year) − CP(t) − (premiums paid to any other contract intended to be a QLAC under any 401(a), 403(a), 403(b), 408 or governmental 457(b) arrangement)`; a breaching premium is rejected | [R1 (q)(2)(ii)](#uslib-deferred_income_annuity-r1) [REG-R57] |
| Limit level and indexing | $200,000 as enacted; indexed like §415(d) limits with base period the calendar quarter beginning **July 1, 2022**, increments rounded to the **next lowest multiple of $10,000**; **$210,000 for 2026** | [R1 (q)(4)(ii)(A)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(2)](#uslib-deferred_income_annuity-r2) [R3] [S4] |
| Percentage-of-account-balance limit | **None.** SECURE 2.0 § 202(a)(1) directed its elimination and the codified text has no percentage test. Do not implement a 25% test | [R2] [R1] [REG-R58] |
| Latest income start | `T` — the **annuity starting date**, not the date the first payment lands — no later than the first day of the month next following the 85th anniversary of birth | [R1 (q)(1)(ii)](#uslib-deferred_income_annuity-r1) [S1] [S2] [S3] [S4] |
| Earliest income start | A *product* rule, not a QLAC rule: after April 1 of the year following the year the owner attains the applicable RMD age | [S1] [S2] |
| Permitted death benefits | Exhaustive: (i) life annuity to a sole-beneficiary surviving spouse ≤100% of the employee's payment, commencing no later than the employee's annuity would have; (ii) life annuity to another beneficiary ≤ the applicable percentage, commencing by the last day of the year following the year of death; or (v) **return of premiums** up to premiums paid less payments already made, payable by the end of the year following the year of death | [R1 (q)(3)](#uslib-deferred_income_annuity-r1) |
| Applicable percentage | MDIB table where there is no pre-annuity-starting-date non-spousal death benefit; Table 6 (≤2 yrs → 100% … 25+ yrs → 20%) where the non-spousal beneficiary is irrevocably set; **0 where the contract provides a return of premium** | [R1 (q)(3)(iii)](#uslib-deferred_income_annuity-r1) |
| Model consequence | A QLAC carries **either** the ROP death benefit **or** a beneficiary life annuity — never both, since the applicable percentage is 0 when ROP is present | [R1 (q)(3)(iii)(C)](#uslib-deferred_income_annuity-r1) |
| Liquidity | `commutation_allowed = false`, `accel_uses = 0`, `cola_rate = 0` | [R1 (q)(1)(iv)](#uslib-deferred_income_annuity-r1) [S4]; the COLA restriction is a market choice, not a regulatory one (a) |
| Permitted forms | Restrict `income_form` to {Single Life No Refund, Single Life Cash Refund, Single Life No Death Benefit, Joint & Survivor Cash Refund}; Installment Refund and Period Certain unavailable | [S2] [S4] |
| RMD exclusion | The contract's value is excluded from the RMD account balance; **not** for a Roth IRA | [R4] [R5 (h)(4)](#uslib-deferred_income_annuity-r5) |
| Failure flags | Excess premium ends QLAC status on the date paid unless returned by the end of the following calendar year; any other failure voids status **retroactively to purchase** | [R1 (q)(4)(i)(B), (q)(4)(iii)(A)](#uslib-deferred_income_annuity-r1) |
| Rescission | A rescission right not exceeding 90 days from purchase does not violate the no-commutation rule | [R1 (q)(1)(iv)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(4)](#uslib-deferred_income_annuity-r2) |
| Divorce | A joint-and-survivor QLAC survives a post-purchase, pre-commencement divorce under QDRO conditions, retroactive to contracts purchased on or after July 2, 2014 | [R1 (q)(3)(vii)](#uslib-deferred_income_annuity-r1) [R2 §202(a)(3), §202(c)(1)(B)](#uslib-deferred_income_annuity-r2) |

(a) **Research finding worth carrying into the model as a comment:** the regulation expressly permits a QLAC
to provide a cost-of-living adjustment described in paragraph (o)(2) [R1 (q)(4)(iv)](#uslib-deferred_income_annuity-r1), yet NYL, Guardian and
Pacific Life all exclude COLA from their QLAC offering [S1] [S3] [S4] and MassMutual limits it on qualified
contracts [S2]. The market is more restrictive than the law; follow the market by default and expose the
switch.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]** reference constructions. No DIA behavioral experience study exists in any
retrieved source, and VM-22's standard projection prescribes 0% annuitization and no lapse assumption for
this reserving category [R9], so these are genuinely modeler's choices rather than calibrations.

**Lapse and surrender: exactly zero, at all durations.** Not conservatism — there is no surrender benefit to
elect [R9] [R13]. A nonzero lapse assumption in a DIA model is a defect, not a margin.

**Income start date adjustment.** One-time, deferral only, excluded on Life Only and Joint Life Only
[S1] [S3] [S4]:

    h_adj(t) = h_0 · M_dir(t),   h_0 = 1.5% p.a. of exposure; window policy year 3 to (T/12 − 2)   **[std]**
    direction split: 60% defer / 40% advance                                                       **[std]**
    M_def(t) = min( 3.0, 1 + 3 · max(0, i_e(t) − i_p − 0.01) )                                     **[std]**
    M_adv(t) = min( 3.0, 1 + 3 · max(0, i_p − i_e(t) − 0.01) )                                     **[std]**

Rationale: the option's value is driven by the spread between the pricing rate locked at issue and the Baa
yield at exercise, which is why the right is one-time and why the forms with the strongest health-driven
selection are excluded [S1] [S2] [S3] [S4]. In a higher-rate environment deferring buys proportionally more
income (equation (11) with a larger `i_e`), so `M_def` rises with rates and `M_adv` rises when rates fall.

**Selection on health.** `sel_mult = 0.90` for contracts exercising to **defer** and `1.10` for those
**advancing**, applied to `q(t)` from the exercise month **[std]**. Rationale: insurers exclude the Life Only
forms from the adjustment right precisely because that is where anti-selection on health bites hardest
[S1] [S3] [S4] — the exclusion is evidence the effect is believed real — and 10% is a deliberately modest
reference magnitude with no experience behind it.

**Payment acceleration.** `h_acc(t) = 2%` p.a. of exposure among contracts that are nonqualified, on monthly
frequency, at attained age ≥ 59½, in the payout phase, with uses remaining, and outside both a blackout and
the six-month interlocks **[std]** [S1] [S2] [S3] [S4]. Modeled as pure timing plus the cost in (12).

**Commutation (extended case).** `h_com(t) = 1.5%` p.a. of exposure among eligible contracts,
**rate-insensitive in the base run** **[std]**: the interest-rate adjustment in (13) is designed to
neutralize rate-driven anti-selection [R13 §3.F(7)](#uslib-deferred_income_annuity-r13), so a rate multiplier would double-count the protection.
Expose `M_com(t) = min(3.0, 1 + 4·max(0, r_ref(t) − r_ref(0)))` for sensitivity testing only.

**Spousal continuation on death in deferral.** Where the surviving spouse is joint annuitant and sole primary
beneficiary the contract may continue instead of paying the death benefit [S1] [S2] [S4]. Base **[std]**: 100%
election of the death benefit. The continuation branch is a switch; under non-convertible continuation no
further premiums are allowed [S2].

**Premium behavior.** Per assumption note (f): deterministic schedule, no dump-in dynamics unless
`guaranteed_future_rates` is set **[std]**.

---

## Worked example

Anchor cell **[std]**: Female 60 ANB, nonqualified, Life with Cash Refund, monthly in arrears, ROP death
benefit in deferral, no COLA. Premiums $100,000 at issue (age 60, 20-year deferral) and $50,000 at the start
of policy year 6 (age 65, 15-year deferral). Income start at attained age 80 (`T = 240`). Pricing basis
`i_p = 4.75%`, `L = 6.0%` **[std]**.

**Illustrative factors [std].** The 2012 IAM Basic / Scale G2 numerical tables were **not** retrieved — they
live at `mort.soa.org` [R16] — so the factors below are mutually consistent illustrative values, **not**
table lookups; a production implementation must substitute table values [R9] [REG-R59]. Anchors:
`_5p_60 = 0.975000`, `_10p_60 = 0.920000`, `_15p_60 = 0.838000`, `_20p_60 = 0.715000`, `_5p_80 = 0.780000`,
with geometric interpolation inside each five-year band, hence `_15p_65 = 0.715000/0.975000 = 0.733333`.
Payout factor `a^{(12)}_80(cash refund, female; 4.75%) = 8.60`; discount factors `v^20 = 0.395293`,
`v^15 = 0.498528`. `A_rop` is computed from the same survival anchors with a mid-band death-timing
approximation: `A_rop(60, 20) = 0.157900`, `A_rop(65, 15) = 0.180200`.

**Slice pricing, equation (4).** Slice 1 (age 60, `d = 20`): `a_def = 0.395293 × 0.715000 × 8.60 = 2.430657`;
`pr₁ = (0.940000 − 0.157900)/2.430657 = 0.321765`; `B₁ = 100,000 × 0.321765 = $32,176.50` per year. Slice 2
(age 65, `d = 15`): `a_def = 0.498528 × 0.733333 × 8.60 = 3.144050`;
`pr₂ = (0.940000 − 0.180200)/3.144050 = 0.241663`; `B₂ = 50,000 × 0.241663 = $12,083.15` per year. Total from
`T`: **`B = $44,259.65` per year = $3,688.30 per month**. Derived guarantee period (5):
`n_g = 150,000/44,259.65 = 3.3891` years, so the cash-refund guarantee is exhausted during the fourth payment
year, at attained age ≈ 83.4.

**The death-benefit fork, same premiums.** Setting `1{ROP} = 0` in (4): `pr₁ = 0.940000/2.430657 = 0.386727`
and `pr₂ = 0.940000/3.144050 = 0.298977`, so `B = 38,672.70 + 14,948.85 = $53,621.55` per year — **21.2% more
income** for the same $150,000. That difference is the price of the return-of-premium guarantee, and it is
mortality gain in the insurer's hands if the annuitant dies in deferral: at the year-10 death below, the ROP
form pays $150,000 and the no-death-benefit form pays nothing while releasing the entire reserve.

**Projection (annual display grid; the model runs monthly).** `E[DB]` is the expected deferral death benefit
paid in policy year `t`, `= (l(t−1) − l(t)) × CP(t)`; `E[income]` is the expected income paid at the end of
policy year `t` on an annual-payment display approximation.

| Policy year `t` | Age at start of year (ANB) | Premium at start | `CP(t)` | `B(t)` (annual) | `l(t)` | `E[DB]` in year `t` | `E[income]` at `t` |
|---|---|---|---|---|---|---|---|
| 1 | 60 | 100,000 | 100,000 | 32,176.50 | 0.994949 | 505.08 | — |
| 5 | 64 | — | 100,000 | 32,176.50 | 0.975000 | 494.95 | — |
| 6 | 65 | 50,000 | 150,000 | 44,259.65 | 0.963743 | 1,688.54 | — |
| 10 | 69 | — | 150,000 | 44,259.65 | 0.920000 | 1,611.90 | — |
| 15 | 74 | — | 150,000 | 44,259.65 | 0.838000 | 2,369.01 | — |
| 19 | 78 | — | 150,000 | 44,259.65 | 0.738063 | 3,571.09 | — |
| 20 | 79 | — | 150,000 | 44,259.65 | 0.715000 | 3,459.50 | — |
| 21 | 80 | — | 150,000 | 44,259.65 | 0.680338 | — | 30,111.54 |
| 25 | 84 | — | 150,000 | 44,259.65 | 0.557700 | — | 24,683.61 |

Trace, policy year 6: the $50,000 premium arrives at the start of the year while the annuitant is alive, so
expected premium income is `50,000 × l(5) = $48,750.00`; it buys slice 2 at the age-65 / 15-year purchase
rate, taking `B` from $32,176.50 to $44,259.65 by (8) and `CP` to $150,000 by (7). Deaths during year 6
(`l(5) − l(6) = 0.0112569`) now attract the larger benefit `CP(6) = 150,000`, giving `E[DB] = $1,688.54`.
Nothing accumulates and nothing is credited: between premiums the only state change is the survivorship in
(9). The income start date is the start of month index `T = 240` (20 years from issue); under arrears the
first payment falls one month later, 241 months from issue — which is why policy year 20 (months 228–239)
still shows a deferral death benefit and policy year 21 (months 240–251) carries the first twelve payments.

---

## Valuation and reserve pointers

This library projects **gross liability cash flows**; reserve layers consume them and are cited, not
reproduced.

- **Statutory — principle-based.** VM-22, "PBR for Non-Variable Annuities", constitutes CARVM for contracts
  in scope and names **Deferred Income Annuity contracts explicitly** in the Payout Annuity Reserving
  Category [R9 §3.F.1.a](#uslib-deferred_income_annuity-r9) [REG-R36]. Effective for valuation dates on or after **January 1, 2026**, with an
  elective three-year transition on VM-A/VM-C/VM-M/VM-V for newly issued business and mandatory prospective
  application three years after the effective date [R9] [REG-R36]. Aggregate reserve = **SR** (stochastic,
  **CTE70**) + **DR** for contracts passing the Single Scenario Test + formulaic reserves for excluded
  contracts; the Additional Standard Projection Amount is a VM-31 **disclosure** item [R9] [REG-R36]. Payout
  and Accumulation categories may be aggregated only under an integrated risk management process and a single
  portfolio or portfolios with the same ALM strategy [R9].
- **Statutory — formulaic fallback.** For contracts not passing the Stochastic Exclusion Test, **VM-V Section
  1 "Income Annuities"** — not VM-22 — sets the statutory maximum valuation interest rate, its scope
  expressly including "deferred income annuity contracts issued after Dec. 31, 2017" [R9] [REG-R37]. The rate
  is a function of the **Valuation Rate Bucket** (A–D by reference period and initial age; a DIA issued below
  age 70 with a long reference period lands in **Bucket D**), the **premium determination date** — for a DIA
  the "date consideration is determined and committed to by contract holder", with an immateriality tolerance
  of a change under 10% in present value and under $1 million — and jumbo versus non-jumbo status; rates are
  published daily (jumbo) and quarterly (non-jumbo) by the NAIC [R9]. VM-V §1 supersedes the interest-rate
  guidance in AG IX-B and the interest references in AG IX-C [REG-R37]; the incorporated guideline family is
  indexed at [REG-R41]. **VM-21 does not apply** — it is the variable-annuity standard [REG-R35] [REG-R36].
- **Statutory — the formulaic chain itself.** CARVM is A-820 ¶¶14–15 (method), ¶¶7–10 (interest) and
  Appendix A-821 (mortality) [REG-R153 ¶6](#uslib-reg-r153), as interpreted for contracts with elective benefits by **AG 33**
  [REG-R151]. Both were read from the AP&P Manual print on 2026-08-06. The DIA-specific consequences — which
  mandatory stream families are empty, why the ±5-year adjustment re-rates the annuitization portion, why a
  commutation right bars *Text* 4(B), and why the 7% expense-allowance floor has no base here — follow from
  those two prints [REG-R151] [REG-R153].
- **Prescribed standard-projection assumptions** reusable directly: mortality
  `q_x^(2012+n) = q_x^(2012) · (1 − G2_x)^n · F_x` on the 2012 IAM Basic table with `F_x` from Table 6.8
  (ANB) [R9]; **lapse: not applicable**; **annuitization: 0% at all projection intervals**; maintenance
  expense **$50** per individual Payout Annuity Reserving Category contract per year escalated at 2.5%, plus
  **7 basis points** applied, for contracts without an account value, to a present-value base [R9] (the exact
  base was truncated at a page break in the research extract [R9]).
- **Nonforfeiture.** Model #805 applies during deferral but the cash-surrender requirement is conditional and
  untriggered; the paid-up annuity requirement is satisfied by construction [R10] [R13 §3.H(1)](#uslib-deferred_income_annuity-r13). For Compact
  filings a comparative-adequacy certification replaces the demonstration [R13 §1.B(1)(g)](#uslib-deferred_income_annuity-r13). Corrected
  parameter: the Model #805 indexed nonforfeiture rate is floored at **15 basis points**, not 1% [REG-R42] —
  see `product-spec.md`, Regulatory context.
- **Tax.** IRC §807: the tax reserve is the greater of net surrender value (zero here) and 92.81% of the
  NAIC-prescribed method — CARVM — capped at the statutory reserve [REG-R16]. Contract-holder taxation runs
  through IRC §72's exclusion ratio and the §72(q) penalty [R8] [REG-R55].
- **U.S. GAAP.** Under LDTI a payout annuity carries a liability for future policy benefits with annually
  reviewed assumptions and **no market risk benefit** — there is no account value for an MRB to attach to
  [REG-R34] [REG-R71].
- **Standards for the modeling work.** ASOP 7 (cash flow analysis) [REG-R27]; ASOP 22 (asset adequacy)
  [REG-R29]; ASOP 54 (pricing) [REG-R70]; ASOP 56 (modeling) [REG-R32]. There is **no ASOP for
  principle-based reserves for annuities** — ASOP 52 is scoped to VM-20 life products [REG-R31] [REG-R70
  context](#uslib-reg-r70).

---

## Key sensitivities and model risks

1. **Longevity, levels and improvement.** With no lapse decrement nothing offsets a mortality miss; the
   liability runs to the last survivor. The valuation table is the 2012 IAR/IAM family with Scale G2
   [R9] [REG-R59] [REG-R60] while the experience under it has moved — the 2020–2024 payout study measures
   directly against the 2012 IAM basis and is the right place to look for drift [R15] [REG-R61]. Test the A/E
   factor and an improvement scale stronger than G2 first.
2. **Deferral-phase mortality, especially on no-death-benefit forms.** Equation (4) puts the whole ROP cost
   in the numerator: on the anchor cell, removing the ROP moves income by 21.2%. Deferred-period annuitant
   mortality is served publicly by only two dated sources [REG-R65] and is the least-evidenced assumption in
   the model. It is also asymmetric — a *higher* assumed deferral mortality lets the insurer offer *more*
   income — so an error here is not conservative in either direction by default.
3. **The pricing rate `i_p` and the load `L`.** They set the income level directly through (4). If the model
   reads `B` from an administration extract these drop out of the in-force projection entirely, which is the
   recommended configuration for valuation work and removes the largest [std] exposure.
4. **Start-date adjustment take-up.** A one-time, ±5-year, rate-sensitive option granted without an explicit
   charge in every retrieved product [S1] [S2] [S3] [S4]. Take-up, direction split and selection multiplier are
   all **[std]** with no experience behind them.
5. **Commutation in the extended case.** The interest-rate adjustment formula is unpublished [S4] [S5];
   equation (13) is a construction. Because commutation removes guaranteed payments and leaves the
   life-contingent tail [S4], a wrong adjustment changes the shape of the residual liability, not just its
   timing.
6. **Timing conventions.** Arrears versus advance moves the whole payout stream by one payment period;
   end-of-month versus mid-month death benefit timing moves deferral claims by half a month. Both are
   **[std]** and must be documented when reconciling to an administration system.

Known pitfalls specific to this product:

- **Building a lapse module.** There is nothing to lapse to [R9]. A "prudent" 2% lapse assumption is wrong
  here and understates the liability.
- **Building an account-value roll-forward.** The liability is a schedule of income slices keyed on (premium,
  purchase date, income start date, income option), not a balance [derived from S1–S4, R13]. Any credited
  rate, charge or interim value invented to fill a template is fictitious.
- **Using life-insurance mortality tables.** 2017 CSO and 2015 VBT are for insured lives; annuitant longevity
  must use the 2012 IAM/IAR family and the payout experience studies [REG-R59] [REG-R61].
- **Chaining rounded generational rates.** `q_x^(2012+n)` must be computed from the 2012 period rate each
  time; the Valuation Manual explicitly flags `q^2014 = q^2013(rounded) × 0.99` as incorrect [R9] [REG-R59],
  and **A-821 ¶14 prints the identical prohibition and the identical counter-example** [REG-R153].
- **Feeding the behavioral take-up rates into a CARVM run.** `h_adj`, `h_acc` and `h_com` are projection
  assumptions. AG 33 **prohibits** experience-based elective incidence and makes the elective path a decision
  variable maximised over, so importing them into a formulaic reserve is a defect, not a refinement
  [REG-R151].
- **Single-premium refund bases.** For a flexible-premium DIA the cash-refund and installment-refund bases are
  **cumulative premiums** `CP(T)`, not the initial premium [S2] [S4].
- **Circularity in refund forms.** (5) and (6) put `B` on both sides; failing to iterate leaves a systematic
  bias in the derived guarantee period and hence in the income.
- **Double-counting the deferral death benefit.** Its cost belongs in the purchase rate (4) *and* in the
  projected cash flows; it must not additionally be loaded into `a_def`.
- **Modeling payment acceleration as a withdrawal.** It is a timing shift expressly labelled "not a liquidity
  feature" [S2]; the only economic cost is (12).
- **QLAC arithmetic from stale documents.** A 25%-of-account-balance test, a $125,000 or $130,000 cap, or an
  RMD age of 70½ are all superseded [R1] [R2] [R3], though pre-2023 insurer guides still print them [S2] [S3].
  Cite § 1.401(a)(9)-6(**q**), not "A-17" [R1] [R6].
- **Treating the COLA as index-linked.** Every observed option is a fixed compound escalator elected at issue,
  not a CPI adjustment [S1] [S2] [S3] [S4].

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-deferred_income_annuity-r1
[R10]: #uslib-deferred_income_annuity-r10
[R13]: #uslib-deferred_income_annuity-r13
[R14]: #uslib-deferred_income_annuity-r14
[R15]: #uslib-deferred_income_annuity-r15
[R16]: #uslib-deferred_income_annuity-r16
[R2]: #uslib-deferred_income_annuity-r2
[R3]: #uslib-deferred_income_annuity-r3
[R4]: #uslib-deferred_income_annuity-r4
[R6]: #uslib-deferred_income_annuity-r6
[R8]: #uslib-deferred_income_annuity-r8
[R9]: #uslib-deferred_income_annuity-r9
[REG-R151]: #uslib-reg-r151
[REG-R153]: #uslib-reg-r153
[REG-R16]: #uslib-reg-r16
[REG-R27]: #uslib-reg-r27
[REG-R29]: #uslib-reg-r29
[REG-R31]: #uslib-reg-r31
[REG-R32]: #uslib-reg-r32
[REG-R34]: #uslib-reg-r34
[REG-R35]: #uslib-reg-r35
[REG-R36]: #uslib-reg-r36
[REG-R37]: #uslib-reg-r37
[REG-R41]: #uslib-reg-r41
[REG-R42]: #uslib-reg-r42
[REG-R55]: #uslib-reg-r55
[REG-R57]: #uslib-reg-r57
[REG-R58]: #uslib-reg-r58
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R61]: #uslib-reg-r61
[REG-R65]: #uslib-reg-r65
[REG-R70]: #uslib-reg-r70
[REG-R71]: #uslib-reg-r71
[S1]: #uslib-deferred_income_annuity-s1
[S2]: #uslib-deferred_income_annuity-s2
[S3]: #uslib-deferred_income_annuity-s3
[S4]: #uslib-deferred_income_annuity-s4
[S5]: #uslib-deferred_income_annuity-s5
[S6]: #uslib-deferred_income_annuity-s6
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
