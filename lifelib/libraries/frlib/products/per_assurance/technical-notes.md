# Technical Notes

**Status:** Draft, 2026-08-26 (all cited sources accessed 2026-08-26).

**Scope note.** These notes specify a reference liability cash-flow projection model for
the standardized composite PER individuel assurantiel defined in `product-spec.md` (same
directory). This is not any single insurer's contract. [S#] / [R#] tags refer to the
source list in `sources.md` (numbering carried from `_research/per-assurance.md`);
[REG-R#] tags refer to the cross-product reference library
`references/regulatory-and-actuarial-references.md` (its own frozen R-numbering).
**[std]** marks standardizations introduced for the reference implementation;
[unverified] marks claims not confirmed against a retrieved document. Parameter values
are identical to those in `product-spec.md`. The model is **PER_FR_S**, on a **monthly**
grid; the annuity that a liquidating plan buys is projected by `Rente_FR_S` and is
specified in `products/rente_viagere/technical-notes.md`, not here.

---

## Model scope and conventions

- **Purpose.** Project gross best-estimate liability cash flows for single-policy PER
  model points in the **accumulation phase**: *versements* in; death, early-release,
  transfer-out and maturity benefits out; expenses. The account value and its two supports
  are state variables and the glide path drives their split. Reserves are not computed here
  (see *Valuation and reserve pointers*). In the last projected month, `t = proj_len − 1`,
  the account is settled — a capital payment, a conversion to a *rente viagère*, or both;
  the annuity's own cash flows belong to `Rente_FR_S`, and this model hands over an amount
  and records it.
- **Time index [std].** `t` is **0-based** and counts **plan months**, as in lifelib's
  `basiclife/BasicTerm_S` and the five frlib models that were monthly from the start:
  `t = 0` is the first projected month, month `t` runs from time `t` to time `t + 1`, and
  the frame is `t = 0, 1, …, proj_len − 1` with `proj_len = 12n` the *number* of projected
  months rather than the last index. `n = proj_years = retirement_age − age(0)` is the
  declared horizon, still in years, because the contract states it in years.
  Because every contractual schedule is annual, the plan year is **derived** and used as a
  lookup key: `dur(t) = duration_ifo + t // 12` are the completed *ancienneté* years at the
  start of month `t`, and the contractual, 1-based label the *ancienneté* schedules are
  written in is the plan's own year `y(t) = dur(t) + 1`, never `t` itself. Where these
  notes say "the plan year" as contract language, its months are the twelve
  `t = 12j … 12j + 11` of the projected plan year `j = y − 1 − duration_ifo`.
  Nothing is indexed by the plan year. An in-force cell opens the frame at `t = 0` like any
  other; its history is carried in `duration_ifo`, not in a frame offset.

  **Two months of each plan year carry its annual events, and they are not the same
  month.** The plan-year **start** is `t ≡ 0 (mod 12)`, where the *versement* arrives and
  the balance is rebalanced onto the glide path. The **anniversary** is the last month of
  the plan year, `t ≡ 11 (mod 12)`, where the management charge is levied and, at
  `t = 12n − 1`, where the plan is liquidated. The *garantie plancher* base moves at those
  two months and nowhere else.
- **Projection frequency [std]: monthly**, on plan months — with the plan-year start and
  the plan anniversary still the two event dates. **A monthly grid is not a monthly
  product.** Every *contractual* mechanic of this plan is annual — the *versement*, the
  glide-path rebalancing read off a grid keyed by whole years to the horizon, the
  management charge on the end-of-year balance [S3] [S7], the annual statement
  [R5 R. 224-2](#frlib-per_assurance-r5), the liquidation at the declared horizon — and
  the model keeps every one of them there. What the finer grid adds is everything that is
  *not* contractually annual: death, *déblocage anticipé* and transfer out falling in the
  month they happen and settled on the balance the plan actually holds **then**, the two
  supports accruing month by month so that a mid-year exit is not paid a year-end balance,
  and maintenance expense falling where it is incurred. An annual step remains a
  well-defined special case of the recursions below and reproduces every anniversary value
  exactly — see *Anniversary equivalence* — but it is not what the reference model runs.
  The sub-annual rebalancing the sample shows [S7] is now *expressible* and is still not
  modelled; that is a choice, argued in product-spec footnote 8, not a constraint.
- **Timing conventions [std].** Monthiversary (BOM) processing. *Versement* and
  glide-path rebalancing at the beginning of the month that **opens** a plan year;
  investment return credited over every month on the start-of-month balances; the
  management charge on the post-crediting balance in the **anniversary** month only (the
  [S3] convention); decrements and benefit payments at the end of every month (EOM), in
  the processing order below. State variables are stored at EOM; `l⁻(t)`, the in-force
  probability, is read at the **start** of month `t` so that it weights that month's cash
  flows.
- **Decrement conversion [std].** Every decrement and every credited return in this
  product is published, calibrated and tabulated **annually**, and the monthly rates the
  recursions apply are derived from them at the constant-force conversion, so that twelve
  months compound back to exactly the annual figure:

  ```
  q_m(t)    = 1 − (1 − q(t))^(1/12)              mortality
  w_e,m(t)  = 1 − (1 − w_e(t))^(1/12)            déblocage anticipé
  w_r,m(t)  = 1 − (1 − w_r(t))^(1/12)            transfer out
  r_eu,m    = (1 + r_eu)^(1/12) − 1              euro credit,  0,277395 % a month
  r_uc,m    = (1 + r_uc)^(1/12) − 1              UC credit,    0,407412 % a month
  ```

  Unsuffixed `q`, `w_e`, `w_r`, `r_eu`, `r_uc` stay the **annual** quantities these notes
  tabulate, which is the library register's rule. Dividing an annual rate by twelve is a
  different assumption and a wrong one: `12 q_m = 0,0050115` on the anchor cell against a
  stated `q = 0,00500`, so a twelfth would overstate the plan year's mortality by 0,23 %.
  **The management charge is the one annual quantity that is not converted**: it is a
  contractual event on a date, it lands whole in the anniversary month, and spreading it
  would move the *garantie plancher* base — see *Crediting and charges*.
- **Currency and basis.** EUR; single-policy model points projected on an expected
  basis, `pols_if` multiplying per-policy amounts. Account quantities are per policy
  (`av_pp`, `av_euro_pp`, …) and cash-flow outputs are aggregate — never multiply a claims
  column by `pols_if` twice.
- **Age basis.** Attained age at the valuation date, integer, incremented once per plan
  year **[std]** — the age steps at the plan anniversary, not on the birthday and not
  monthly, so `age(t) = age(0) + t // 12`. No retrieved French document fixes a model age
  basis; the regulatory non-annuity tables are applied with the annexed *décalage d'âge* age shifts [REG-R23],
  which the shipped proxy does not reproduce.
- **Tax is outside the projection.** The deductibility election changes the holder's exit
  taxation, not the insurer's gross benefit [R13] [R19] [R20] [R21]. `deduction_elected`
  is carried and never enters a cash flow.
- **Rounding.** Intermediate values at full precision; reported cash flows to the cent
  **[std]**.

---

## Model point attributes

| Attribute | Type | Example (worked configuration) |
|---|---|---|
| `point_id` | int | 1 |
| `sex` | enum {M, F} | M |
| `age` | int, attained age at the valuation date, `age(0)` | 52 |
| `retirement_age` | int, the declared *horizon* [R5 D. 224-3](#frlib-per_assurance-r5) | 64 |
| `duration_ifo` | int, completed years since the first *versement* | 2 |
| `compartment` | enum {c1, c2, c3} [R3 L. 224-2](#frlib-per_assurance-r3) | c1 |
| `allocation_profile` | enum {prudent, equilibre, dynamique, offensif} [R6] | equilibre |
| `premium` | currency p.a., paid in the first month of each plan year to the horizon | 3 000.00 |
| `av_euro_init` | currency, euro support carried into `t = 0` | 0.00 |
| `av_uc_init` | currency, UC bucket carried into `t = 0` | 16 600.00 |
| `death_floor_init` | currency, *garantie plancher* base carried into `t = 0` | 16 000.00 |
| `death_floor_flag` | bool, floor in force to the 70th birthday [S1] [S3] | True |
| `exit_form` | enum {capital_single, capital_staged, annuity, mixed} [R3 L. 224-5](#frlib-per_assurance-r3) | mixed |
| `annuity_share` | float in [0, 1], share of the balance converted to a *rente* | 0.30 |
| `capital_instalments` | int, annual instalments under `capital_staged` (the annuity's own frequency, not the projection step) | 1 |
| `deduction_elected` | bool — recorded, never used in a cash flow | True |

`compartment` earns its place because it changes two operative rules, not one: **c3**
rights may be delivered **only** as a life annuity [R3 L. 224-5](#frlib-per_assurance-r3) [S2], and they are
**excluded** from the main-residence early-release case [R3 L. 224-4 I 6°](#frlib-per_assurance-r3). A c3 model
point must therefore force `exit_form = annuity` and use a reduced early-release rate.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `av_euro_pp_at(t, timing)` | Per-policy euro-support balance, `timing` ∈ {BEF_REBAL, BOM, BEF_CHARGE, EOM} | carried in at BEF_REBAL; rebalanced and credited the *versement* at BOM in a plan-year start month; credited the month's return at BEF_CHARGE; charged at EOM in an anniversary month |
| `av_uc_pp_at(t, timing)` | Per-policy UC balance | same |
| `av_pp_at(t, timing)` | `av_euro_pp_at + av_uc_pp_at` | derived |
| `death_floor_pp(t)` | *Garantie plancher* base: *versements* net of loading, less all charges taken, less benefits paid — the [S1] drafting, **not** the [S3] one, which adds euro-fund interest | two months of twelve: up at the plan-year start, down at the anniversary, flat in between |
| `alloc_euro(t)` | Target euro (low-risk) share in month `t`, from the grid [R6] | steps at the anniversary, from `years_to_horizon` |
| `switch_pp(t)` | Gross amount switched between supports at the rebalancing; nil in every other month | plan-year start month |
| `arbitrage_charge_pp(t)` | `arb_rate × |switch_pp(t)|` [S1]; nil in every other month | plan-year start month |
| `mgmt_charge_pp(t)` | Management charge on the post-crediting balance; nil in every other month | anniversary month |
| `is_plan_boy(t)` | `t ≡ 0 (mod 12)`: the month that opens a plan year | — |
| `is_anniv(t)` | `t ≡ 11 (mod 12)`: the month that closes it | — |
| `years_to_horizon(t)` | `n − t // 12`, the whole years remaining to the horizon; constant inside a plan year | steps at the anniversary |
| `duration(t)` | `duration_ifo + t // 12`, completed years since the first *versement*; 0-based | steps at the anniversary |
| `plan_year(t)` | `duration(t) + 1`, the plan's own 1-based *ancienneté* year — the key into `exit_table.csv` and the indemnity window | steps at the anniversary |
| `q_m(t)`, `w_e,m(t)`, `w_r,m(t)` | The monthly rates actually applied, `1 − (1 − ·)^(1/12)` on the plan year's annual rate; `mort_rate_mth`, `early_release_rate_mth`, `transfer_out_rate_mth` | every month |
| `l(t)` | In-force probability at the **end** of month `t`; the projection opens at `l⁻(0) = pols_if(0) = 1`. The model publishes `l(t)` as `pols_if_at(t, "AFT_DECR")` and as the `pols_if_eoy` column of `result_state()` — **not** as `pols_if`, which is the start-of-month count `l⁻(t)`; see *The exposure convention* below | EOM decrements |

---

## Assumption inputs

Three classes are distinguished. Class (a) is contractual or statutory; class (b) is the
insurer's current discretionary scale; class (c) is the modeler's view of experience.

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Guaranteed technical rate on the euro support | **0,00 %** — the maximum a PER tariff may use | [R9 A. 142-1](#frlib-per_assurance-r9) [S1] [S7] |
| Euro-support capital floor | *Versements* net of loading, less charges levied, less benefits paid; **not** a floor at gross premiums. [S3] drafts the same floor **with** euro-fund interest net of charges added — see the *garantie plancher* recursion below | [S1] [S7] |
| UC guarantee | None; the number of units is guaranteed, not their value | [S1] [S2] |
| Glide-path minimum (équilibré) | euro share 0 % / 20 % / 50 % / 70 % by band; band edges **[std]** (product-spec footnote 7) | [R6 art. 1](#frlib-per_assurance-r6) [S2] [S7] |
| Right to release early | Only on the seven L. 224-4 cases, no surrender right otherwise; paid as a single payment of all or part of the eligible rights, no charge | [R3 L. 224-4](#frlib-per_assurance-r3) [R5 D. 224-4](#frlib-per_assurance-r5) [S2] [S3] [S4] [S7] |
| Transfer-out indemnity | 1 % of acquired rights while the plan is under five years old at the exit date, `y(t) < 5`, nil thereafter; plus an optional reduction of up to 15 % of euro-denominated rights, **off** in the base | [R3 L. 224-6](#frlib-per_assurance-r3) [R5 R. 224-6](#frlib-per_assurance-r5) [S1]–[S8] |
| Death closes the plan | Benefit = account value, floored by the *garantie plancher* to the 70th birthday, capped €762 245 | [R3 L. 224-4 II](#frlib-per_assurance-r3) [S1] [S3] |
| Exit menu | Capital in one payment or *fractionné*, annuity, or a mix; c3 annuity only | [R3 L. 224-5](#frlib-per_assurance-r3) |
| Annuity basis | Technical rate **0 %**; TGF05 / TGH05 or a certified experience table that may not be cheaper | [R9 A. 142-1](#frlib-per_assurance-r9) [R11] [R12] [REG-R21] [REG-R23] |
| Small-annuity commutation | Monthly *quittance* ≤ €110, scaled by the months in the payment period | [R10 A. 160-2](#frlib-per_assurance-r10) |

### (b) Insurer-discretionary current elements (snapshot; maxima disclosed, levels not capped [REG-R30])

| Input | Symbol | Value | Basis |
|---|---|---|---|
| Entry loading on each *versement* | `load` | 2,50 % | [S8] [S10]; adoption **[std]**, product-spec (10) |
| Euro management charge | `c_eu` | 0,70 % p.a. | [S8] [S9]; adoption **[std]** (11) |
| UC management charge | `c_uc` | 0,70 % p.a. | [S8] [S9]; adoption **[std]** (11) |
| Arbitrage charge on the rebalancing | `arb_rate` | 0,30 % of the amount switched | [S1]; adoption **[std]** (9) |
| *Frais d'arrérages* | `c_arr` | 1,50 % of each gross instalment | [S8]; adoption **[std]** (13) |
| Euro-fund gross asset return | `r_eu` | 3,38 % p.a. | [S9]; adoption **[std]**, product-spec (5) |
| UC gross return, net of fund-level charges | `r_uc` | 5,00 % p.a. | **[std]**, product-spec (5) |
| Annuity conversion factor, male 64, annual in arrears, no reversion | `a_x` | 22,0000 | **[std]**, product-spec (17) |
| PPB stock and release policy | — | not modelled | simplification **[std]** (1) |

1. The euro credit is set at the asset return and the charge taken on the post-crediting
   balance; no *provision pour participation aux bénéfices* stock is carried. The only
   retrieved gross-charge-net triple shows the served rate exceeding asset return less
   charge by 7 basis points [S9], i.e. a PPB release, and a PER's PPB horizon is fifteen
   years rather than eight because the commitments sit in a *comptabilité auxiliaire
   d'affectation* [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8). Modelling that stock is a scenario extension:
   four of the seven sampled contracts have **no** contractual PB clause at all
   [S4] [S5] [S6] [S7]. The machinery this replaces — the *compte de participation aux
   résultats*, the PPB dotation-and-release lever and its vintage clock — is specified in
   `products/assurance_vie_euro/technical-notes.md`; see *The euro leg is
   cross-referenced, not re-implemented* below for what to take from it and what not to.

### (c) Behavioral / experience assumptions (modeler's view)

The homologated tables are cited, never shipped: TH 00-02 / TF 00-02 for the death
benefit during accumulation and TGH05 / TGF05 for the annuity [REG-R21] [REG-R22]
[REG-R23].

| Input | Recommended basis | Basis tags |
|---|---|---|
| `mort_rate` | INSEE-derived proxy, sex-distinct; **0,00500 flat** in the worked example | **[std]** (2); source [REG-R24]; regulatory basis [REG-R22] [REG-R23] |
| `early_release_rate` | 1,60 % p.a., flat | **[std]** (3) |
| `transfer_out_rate` | 1,00 % p.a., flat | **[std]** (3) |
| `lapse_rate` | **does not exist** — there is no surrender right | [R3 L. 224-4](#frlib-per_assurance-r3) [S2] [S3] [S4] [S7] |
| Maintenance expense | €30 per plan p.a., inflating 1,80 % p.a. | **[std]** (4) |
| Annuity election at the horizon | `annuity_share = 0,30` | **[std]**, product-spec (16) |
| Profile-change and horizon-change behavior | not modelled | **[std]** (5) |

2. TH 00-02 / TF 00-02 are homologated and public but are not redistributed here
   [REG-R22] [REG-R23]; the shipped CSV is an INSEE-derived proxy [REG-R24] anchored so
   that the model reproduces the flat 0,00500 used in the worked example. Population
   mortality is heavier than insured experience, and the *décalage d'âge* age shifts the
   regulatory tables carry [REG-R23] are not reproduced. No observed range exists: no
   sampled contract publishes a mortality basis, and the one published rate card [S7] is
   a gross premium scale, not a set of decrement rates.
3. No public split of accumulation-phase exits exists [research §18]. The one citable
   anchor is aggregate: early releases and transfers together were €1 651 m against
   €63,0 bn of accumulation-phase provisions in 2024, i.e. **2,62 %** [R22], which the
   split 1,60 % / 1,00 % reproduces to 2,60 %. Two caveats travel with it: it is an
   *amount* ratio adopted as a *policy* decrement rate, which assumes exiting plans carry
   the average balance; and it is contaminated by the market's growth phase — the book was
   growing 18,7 % a year [R22] — so it is not a steady-state rate.
4. No insurer's unit cost is public; only the charge cap is [research §18] [REG-R30]. The
   €20 association fee [S8] is a one-off at adhesion, nil for in-force cells.
5. The declared retirement date may be changed at any time [R5 D. 224-3](#frlib-per_assurance-r5), re-allocating
   the whole balance immediately [S3] [S4]. The base model holds `retirement_age` fixed;
   a scenario overlay can shift it and re-read the grid.

**Why the exit decrements are not called lapses.** The house vocabulary reserves
`lapse_rate` and `claims_lapse` for a contractual surrender right, and this contract has
none — the accumulation phase carries **no surrender right except in the statutory cases**
[S2] [S3] [S4] [S7], the plan being blocked until the L. 224-1 maturity [R3 L. 224-1](#frlib-per_assurance-r3). The
two exit decrements are named for what they are.

- **`early_release_rate`** — *déblocage anticipé* under one of the seven L. 224-4 cases
  [R3]. Not a lapse in four respects: it requires a listed triggering event; it bears
  **no charge** [S2] [S3] [S7]; it may be **partial**, leaving the plan in force
  [R5 D. 224-4](#frlib-per_assurance-r5); and its main-residence limb is closed to compartment 3
  [R3 L. 224-4 I 6°](#frlib-per_assurance-r3). The base model treats it as a full exit paying the whole account
  value, the partial case being a documented extension.
- **`transfer_out_rate`** — a transfer of acquired rights to another PER [R3 L. 224-6](#frlib-per_assurance-r3).
  The plan ends for this insurer but the savings do not leave the regime: the blocage,
  the compartments and the exit conditions travel with the money. It pays a transfer
  value, not a surrender value, and its formula differs from the early-release one by the
  1 % indemnity in the first five years.

Using one decrement for both, or naming either `lapse_rate`, silently attaches the wrong
payment formula to half the exits.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | plan **month** index, **0-based**: `t = 0, 1, …, 12n − 1`, where `proj_len = 12n` is the *number* of projected months and `n = proj_years = retirement_age − age(0)` the declared horizon in years |
| `dur(t)` | completed *ancienneté* years at the start of month `t`: `duration_ifo + t // 12`; `duration(t)` |
| `y(t)` | the plan's own 1-based year, `y(t) = dur(t) + 1`; `plan_year(t)` |
| `k(t)` | whole years to the horizon in month `t`: `k(t) = n − t // 12`, so `k = n` through the first plan year and `k = 1` through the last; constant inside a plan year |
| `a(t)` | target euro (low-risk) share in month `t`, read from the grid at `k(t)` |
| `V` | *versement* received at the beginning of a plan-year start month, `t ≡ 0 (mod 12)`; nil in the other eleven; `V_net = V · (1 − load)` |
| `load`, `c_eu`, `c_uc`, `arb_rate`, `c_arr` | 2,50 %, 0,70 %, 0,70 %, 0,30 %, 1,50 % |
| `r_eu`, `r_uc` | euro and UC **annual** gross returns, 3,38 % and 5,00 % |
| `r_eu,m`, `r_uc,m` | the monthly rates actually credited, `(1 + r)^(1/12) − 1`: 0,277395 % and 0,407412 % |
| `E_eu(t)`, `E_uc(t)` | per-policy support balances after the BOM steps |
| `E_eu⁻(t)`, `E_uc⁻(t)` | the two support balances **carried into** month `t`: `av_euro_init` / `av_uc_init` at `t = 0`, last month's EOM balances afterwards; `av_euro_pp_at(t, "BEF_REBAL")` and `av_uc_pp_at(t, "BEF_REBAL")` |
| `A(t)` | per-policy total account value at EOM `t`, `= av_pp_at(t, "EOM") = av_pp(t)` |
| `A⁻(t)` | per-policy total carried into month `t`: the opening state at `t = 0`, `A(t−1)` afterwards; `av_pp_at(t, "BEF_REBAL")` |
| `m(t)` | gross amount switched at the rebalancing; nil outside a plan-year start month |
| `g(t)` | *garantie plancher* base, `death_floor_pp(t)` |
| `g⁻(t)` | the base carried into month `t`: `death_floor_init` at `t = 0`, `g(t−1)` afterwards |
| `q(t)` | `mort_rate`, the **annual** rate of the plan year containing month `t`, read on a table basis at `age(t) = age(0) + t // 12`, the age the plan year opens at |
| `w_e(t)`, `w_r(t)` | `early_release_rate`, `transfer_out_rate`, the **annual** rates of the plan year, read at `y(t)` |
| `q_m(t)`, `w_e,m(t)`, `w_r,m(t)` | the monthly rates actually applied, `1 − (1 − ·)^(1/12)`; `mort_rate_mth`, `early_release_rate_mth`, `transfer_out_rate_mth` |
| `ι(t)` | transfer indemnity rate: 1 % while `y(t) < 5` — the plan is under four completed *ancienneté* years at the month's EOM exit date, i.e. `12·duration_ifo + t < 48` — else 0 |
| `l(t)` | in force at the **end** of month `t`. In cells names `pols_if_at(t, "AFT_DECR")` |
| `l⁻(t)` | in force at the **start** of month `t`: `l⁻(0) = 1` and `l⁻(t) = l(t−1)` afterwards. In cells names `pols_if(t)` |
| `a_x` | annuity conversion factor at the horizon, 22,0000 **[std]**, product-spec (17); an undiscounted count of **annual** instalments |
| `θ` | `annuity_share`; `C_thr` = €110 monthly commutation threshold [R10] |
| `E(t)` | maintenance expense, `(30/12) · 1,018^(t/12)` **[std]**, assumption footnote (4) |

### The glide path

```
k(t)  = n - t // 12
a(t)  = grid[allocation_profile, k(t)]
```

with the *équilibré* grid `a = 0 %` for `k > 10`, `20 %` for `10 ≥ k > 5`, `50 %` for
`5 ≥ k > 2`, `70 %` for `k ≤ 2` [R6 art. 1](#frlib-per_assurance-r6) **[std]** band edges. The grid is an **input
table**, not a formula: the model reads `allocation_grid.csv`, keyed by
(`allocation_profile`, `years_to_horizon`) with columns `euro_share` and `uc_share`, so
that the other three profiles and any insurer ladder finer than the four regulatory bands
[S1] substitute without touching the code.

The grid's key is **whole years** to the horizon, so `a(t)` is constant through the twelve
months of a plan year and steps only at the anniversary. That is also the reason the
rebalancing stays annual on a grid that could now express any frequency: a sub-annual
rebalancing re-imposes the *same* target inside the year, correcting drift rather than
de-risking faster. See *Key sensitivities* for what it would cost.

### The plan-year rebalancing and the *versement*

At the month that **opens** a plan year, `t ≡ 0 (mod 12)`:

```
m(t)      = a(t) · A⁻(t) − E_eu⁻(t)
arb(t)    = arb_rate · |m(t)|
E_eu(t)   = E_eu⁻(t) + m(t)              + a(t) · V_net
E_uc(t)   = E_uc⁻(t) − m(t) − arb(t) + (1 − a(t)) · V_net      (m ≥ 0)
```

with the roles of the two supports exchanged when `m(t) < 0`. In the other eleven months
of the plan year `m(t) = 0`, `arb(t) = 0` and `V_net = 0`, so `E_eu(t) = E_eu⁻(t)` and
`E_uc(t) = E_uc⁻(t)`: nothing contractual happens at the beginning of an ordinary month.
A `⁻` marks the balance **carried into** the month — the model point's opening state in
the first projected month, `t = 0`, and the previous month's closing balance afterwards,
so that nothing is indexed at `t = −1`. Two conventions, both **[std]**: the arbitrage charge is taken from the
**source** support, so the destination receives the full switch and the post-rebalancing
euro share lands **at or just above** the regulatory minimum rather than just below it;
and the *versement* is allocated directly at the target mix and bears no arbitrage charge,
which is what "allocation of both contributions and existing balance" means in the one
contract publishing its ladder [S1]. Under a de-risking profile `a(t)` is non-decreasing,
so `m(t)` is normally positive (UC → euro); it can turn negative after a UC fall, and the
formula is symmetric.

### Crediting and charges

Crediting happens **every month**; the charge happens in the **anniversary month** alone:

```
av_euro_pp_at(t, "BEF_CHARGE") = E_eu(t) · (1 + r_eu,m)
av_uc_pp_at(t, "BEF_CHARGE")   = E_uc(t) · (1 + r_uc,m)

av_euro_pp_at(t, "EOM") = av_euro_pp_at(t, "BEF_CHARGE") · (1 − c_eu)   if t ≡ 11 (mod 12)
                        = av_euro_pp_at(t, "BEF_CHARGE")                otherwise
av_uc_pp_at(t, "EOM")   = av_uc_pp_at(t, "BEF_CHARGE")   · (1 − c_uc)   if t ≡ 11 (mod 12)
                        = av_uc_pp_at(t, "BEF_CHARGE")                  otherwise

A(t)                    = av_euro_pp_at(t, "EOM") + av_uc_pp_at(t, "EOM")
```

Twelve monthly credits and one anniversary charge reproduce the annual factor exactly,
`(1 + r_m)^12 (1 − c) = (1 + r)(1 − c)`, which is why every anniversary balance is the
annual-step model's.

**The credit is spread and the charge is not**, and both halves of that are decisions
**[std]**. The euro fund is contractually credited once a year with an *effet cliquet*
[S3] [S7], which argues for the anniversary; but every sampled contract that says what
happens to a **mid-year exit** revalues it *pro rata temporis* at the served rate [S7],
credits weekly and definitively acquires each Friday [S1], or compounds daily [S2].
Spreading geometrically is the monthly realisation of exactly that, and without it a
mid-year death, release or transfer would be paid on a balance carrying no return since
the last anniversary. The charge goes the other way: it is levied on the end-of-year
balance after crediting — the [S3] convention, "annually at 31 December on both", which
these notes and `product-spec.md` already adopt — and it stays whole in the anniversary
month. Spreading it would leave `A(t)` at the anniversary unchanged, because the monthly
factors still compound, but it would move the *garantie plancher* base, which accumulates
a **sum** of charges rather than a product of factors: measured on this model, a monthly
levy at `1 − (1 − c)^(1/12)` moves `g` at the anniversary by up to **71,95 €** on the
anchor cell, **88,13 €** on model point 3 and **531,57 €** on model point 12 — and the
worked example below prints `g = 47 267,36`. A monthly levy remains a documented variant
(product-spec footnote 12); it is a new assumption, not a finer grid.

**The price of that decision, stated:** a mid-year exit is valued **gross** of the plan
year's charge. On the anchor cell's last plan year the balance at month 142 is **0,387 %**
above the anniversary value the annual grid paid; at the anniversary month itself the exit
is valued post-charge and agrees exactly. The contractual position is genuinely split —
[S2] charges the euro fund *pro rata temporis* and [S7] accrues daily and levies annually —
and an implementation wanting the other answer would accrue monthly and true up at the
anniversary, which is this convention plus a true-up and breaks the floor identity's tie to
the annual figures.

The euro support rises in the base run, but it is **not monotone by construction**, and
the difference matters. A. 142-1 caps the *tariff's* technical rate at 0 % — "un taux
d'intérêt technique **au plus égal à** 0 %" [R9 A. 142-1](#frlib-per_assurance-r9) — which is a
maximum, not a floor on what is credited; a PER euro fund has **no guaranteed
accumulation rate at all**, only a capital floor gross of charges plus profit sharing
[S1] [S7] (product-spec, *Euro-fund crediting*). Since the charge is taken on the
post-crediting balance, `av_euro_pp` grows over a plan year only while
`r_eu > c_eu / (1 − c_eu)`, which is **0,7049 %** at `c_eu = 0,70 %`. The base run's
3,38 % clears that comfortably; at a credited 0 % the support would fall by the charge
each year. (Within a plan year the euro balance rises every month and then steps down once,
in the anniversary month, by the charge.) The effective euro rate net
of charge is `1,0338 × 0,9930 − 1 = 2,6563 %` — not `3,38 − 0,70 = 2,68 %`, and not the
`2,75 %` actually served in 2025, whose extra seven basis points came from a PPB release
[S9] the base model does not carry.

### The euro leg is cross-referenced, not re-implemented

`r_eu` above is a **flat credited rate**, and the *participation aux bénéfices* machinery
that would produce one is deliberately absent from this model. What it replaces is
specified, with the same citation discipline, in
`products/assurance_vie_euro/technical-notes.md` — sections *The `compte de participation
aux résultats`*, *The crediting rule, the TMG and the PPB lever* and *The PPB and its
eight-year clock*. In outline: the minimum PB is built each year on the two accounts of
art. A. 132-11 [REG-R14] [REG-R15] — 85 % of the financial account plus the technical
account less the insurer's share — and the rate actually served is then moved above or
below that statutory floor by dotations to and releases from the *provision pour
participation aux bénéfices*, with a *taux minimum garanti* as a hard floor underneath and
each PPB vintage due to be spent within eight years [REG-R16].

Three things a reader should take from those notes rather than from these.

- **The crediting rate is an output of a fund-level system, not an input.** Here it is an
  input, at a single observed figure carried flat, which is the (b)-table's
  "PPB stock and release policy — not modelled **[std]**" and assumption footnote (1).
  Nothing in this model produces `r_eu`, and no sensitivity run on it is a projection of
  what an insurer would credit.
- **The PPB is a two-way lever, and its clock is longer here.** The eight-year release
  deadline the euro-fund notes model is **fifteen** years for PER commitments, which sit
  in a *comptabilité auxiliaire d'affectation* [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8).
  A PPB layer lifted from `Euro_FR_S` onto this product has to have that clock changed.
- **A PER euro fund and an assurance vie euro fund are not the same contract.** Four of
  the seven sampled PER contracts have **no** contractual PB clause at all [S4] [S5] [S6]
  [S7], and the *garantie plancher* and glide path specified here have no counterpart in
  the euro-fund product. Take the crediting chassis from those notes; do not take the
  liability.

The one number in this model that a PPB would have changed is visible: [S9]'s triple is a
3,38 % asset return, a 0,70 % charge and a **2,75 %** rate served, and the seven basis
points between `2,6563 %` and `2,75 %` are the release this model does not carry.

### The garantie plancher base

```
g(t) = g⁻(t) + V_net(t) − arb(t) − charges taken in month t
```

where the charges taken are `E_eu(t)·(1+r_eu,m)·c_eu + E_uc(t)·(1+r_uc,m)·c_uc` in an
anniversary month and nil in every other.

**The formula is unchanged in form by the monthly grid**, and its three moving terms are
non-zero in only two months of the twelve: the base steps **up** by `V_net − arb` in the
month that opens a plan year and **down** by the charge in the anniversary month, and is
flat in between. A mid-year death is therefore floored on the base as it stood at the last
anniversary plus this year's *versement*, while the account value beside it has grown every
month — which is why the month at which the floor stops biting can now be located exactly
(model point 10 crosses at month 26; see *Known modeling pitfalls*).

**Two contractual draftings exist and this is [S1]'s, not [S3]'s.** [S1] guarantees a
death benefit "not less than premiums net of charges minus benefits already paid" — no
interest limb — and [S7] states expressly that its guarantee is **not** a floor at gross
premiums. [S3] drafts the same guarantee the other way: the settled amount "cannot be less
than contributions net of loading **plus euro-fund interest net of management charges**".
The recursion above is [S1]'s alone. **These notes are the source of truth for the
modelled quantity**, and `product-spec.md`'s *Death benefit during accumulation* table
carries the same drafting for that reason.

The difference is not cosmetic. Under [S1]'s drafting

```
A(t) − g(t) = [A⁻(0) − g⁻(0)] + Σ gross investment return credited to date
```

so the floor bites only where cumulative investment return is negative, which is what
`check_floor_identity()` asserts. Under [S3]'s drafting the euro leg of that return
accrues to the floor as well, so on an all-euro plan the floor would track the account
value and the identity above would fail by construction. Implementing [S3] means adding
the euro credit net of its charge to `g(t)` and dropping the identity, not adjusting a
parameter.

The cover ceases at the member's 70th birthday [S1] [S3] and is capped at €762 245 across
contracts [S3]. The cessation is tested on the **plan year**, `age(t) + 1 < 70`, so the
cover is off for the whole plan year that ends on the 70th birthday **[std]** — unchanged
from the annual grid. The month-exact alternative (cover in force until the birthday month)
was considered and declined: the age basis here is an integer attained age incremented once
per plan year, so there is no sub-annual age to test one against, and introducing one would
be a second modelling change beside the grid change. Measured, the two rules give identical
cash flows to the cent on model point 9, the only shipped cell that retires at 70.

### Decrements and benefits at EOM

```
d_death(t)    = l⁻(t) · q_m(t)
d_release(t)  = l⁻(t) · (1 − q_m(t)) · w_e,m(t)
d_transfer(t) = l⁻(t) · (1 − q_m(t)) · (1 − w_e,m(t)) · w_r,m(t)
l(t)          = l⁻(t) · (1 − q_m(t)) · (1 − w_e,m(t)) · (1 − w_r,m(t))
```

with `l⁻(0) = 1` and `l⁻(t) = l(t−1)` for `t > 0`.

An ordered dependent-decrement convention **[std]**, matching the library's house
treatment, and the whole chain is re-applied **every month** at the converted monthly
rates. Because `[(1 − q_m)(1 − w_e,m)(1 − w_r,m)]^12 = (1 − q)(1 − w_e)(1 − w_r)` exactly,
the in force at every anniversary is identical to the annual-step model's.

**The split between the three decrements moves, and the total does not.** Walking the
ordered chain twelve times with small steps dilutes the later decrements less than walking
it once with large ones. Over the anchor cell's first plan year deaths fall from 0,005000
to **0,004941** (−1,19 %), releases from 0,015920 to **0,015884** (−0,23 %) and transfers
rise from 0,009791 to **0,009886** (+0,98 %), while the three still sum to the same
0,030711 the annual grid removed. Reading a fall in `claims_death` as an error is the
mistake this paragraph exists to prevent; the total decrement, and so `l` at every
anniversary, is unchanged.

Per-policy benefit amounts, all measured on the **end-of-month** balance `A(t)` — the
balance the plan actually holds in the month of exit, which is what the finer grid buys:
`max(A(t), g(t))` on death while the floor is in force, else `A(t)`
[R3 L. 224-4 II](#frlib-per_assurance-r3) [S1] [S3]; the whole of `A(t)` on early release,
with no charge [R5 D. 224-4](#frlib-per_assurance-r5) [S2] [S3] [S7]; and `A(t) · (1 − ι(t))`
on transfer out [R3 L. 224-6](#frlib-per_assurance-r3).

### The exposure convention

These notes index the in-force probability at the **end** of the period, as `l(t)`. The
library indexes the published exposure at the **start** of the period, because that is the
weight the period's own cash flows carry. Both live in the model, under different names:

| Notes | Cells | Meaning |
|---|---|---|
| `l⁻(t)` | `pols_if(t)` | in force at the **start** of month `t`; `pols_if(0) = 1`, and `l⁻(t) = l(t−1)` afterwards. The weight on row `t` of `result_cf()`, and the exposure every decrement of month `t` is taken against |
| — | `pols_if_at(t, "BEF_RELEASE")`, `pols_if_at(t, "BEF_TRANSFER")` | the intra-month steps of the ordered decrement |
| `l(t)` | `pols_if_at(t, "AFT_DECR")` | in force at the **end** of month `t`; the `pols_if_eoy` column of `result_state()` and the column the worked-example table below prints, read there at the anniversary month |

The two series are one period apart, `pols_if_at(t, "AFT_DECR") = pols_if(t+1)`, and the
one rule worth carrying away is that **`result_cf()["pols_if"]` weights its own row**: a
cash flow divided by that row's `pols_if` is a per-policy amount for the same month. The
survivors who settle at the horizon are `l(12n−1) = pols_if_at(12n−1, "AFT_DECR")`, after
the final month's decrements, which is why `claims_maturity` does not carry the same weight
as `premiums` in the same row.

`result_cf_annual()` sums the monthly frame into plan years and publishes `pols_if` as the
count **entering** the plan year, `pols_if(12·t_year)` — which is exactly the column the
annual-step model carried on the same row — and `av_pp` as the balance **closing** it,
`av_pp(12·t_year + 11)`, which is what `av_pp(t)` meant on the annual grid. Everything else
in that frame is a sum of twelve months.

### Settlement at the horizon

In the last projected **month**, `t = 12n − 1` — the horizon anniversary — the survivors
`l(12n−1)` settle. The settlement is a contractual event on a contractual date and is
**not spread** over the final plan year **[std]**: the capital leg, the conversion and the
commutation test all fall whole in that month, on the survivors of that month. With
`θ = annuity_share` and `A = A(12n−1)`:

```
capital_leg   = (1 − θ) · A                           no exit charge  [S1][S2][S3][S7][S8]
annuity_cap   = θ · A
rente_gross   = annuity_cap / a_x                     0 % technical rate  [R9]
rente_net     = rente_gross · (1 − c_arr)             frais d'arrérages   [S8]
commute if      rente_net / 12 ≤ C_thr                                    [R10]
commuted      = rente_net · a_x
claims_maturity = capital_leg + ( commuted  if commuted else 0 )
annuity_conversion = 0 if commuted else annuity_cap
```

Two things follow from the 0 % technical rate. First, `a_x` is an **undiscounted**
expected-instalment count — the tariff table's curtate expectation of life at the annuity
age, not a discounted annuity factor — a count of **annual** instalments, which is what
fixes the annuity's own payment frequency; the projection grid does not, and paying
quarterly or monthly means replacing `annuity_factor.csv` rather than changing a step.
Second, commuting at the conversion basis returns
the converted capital less the *arrérage* charge exactly:
`rente_net · a_x = annuity_cap · (1 − c_arr)`. Commutation is therefore nearly
value-neutral, which is why it is common — €272 m of 2024 individual-PER benefits at an
average €16 200 [R22]. Where the annuity is not commuted, `annuity_conversion` is handed
to `Rente_FR_S`; the annuity reserve, the 0,80 % p.a. charge on annuity reserves [S7],
reversion, *annuités garanties* and revaluation through the profit-sharing account are
specified in `products/rente_viagere/technical-notes.md`.

### Monthly processing order [std]

The annual order with the month inserted, not a new order. Each step is tagged with where
it lands.

1. **Every month** — read `k(t)` and `a(t)` from the allocation grid. *Annual content:*
   both are keyed by whole years to the horizon and step only at the anniversary.
2. **Plan-year start month only (`t ≡ 0 mod 12`)** — receive `V`; deduct the entry
   loading; `V_net` is available to allocate. Nil in the other eleven months.
3. **Plan-year start month only** — rebalance the carried-in balance to `a(t)`: compute
   `m(t)`, take `arb(t)` from the source support, move `m(t)` to the destination.
   `m(t) = arb(t) = 0` in every other month.
4. **Plan-year start month only** — allocate `V_net` at the target mix, `a(t)` to euro and
   `1 − a(t)` to UC.
5. **Every month** — credit each support at `r_eu,m` / `r_uc,m` on its start-of-month
   balance. *Monthly.*
6. **Anniversary month only (`t ≡ 11 mod 12`)** — take the management charge on each
   post-crediting support balance. Nil in the other eleven months.
7. **Every month** — update `g(t)` with `V_net(t)`, less `arb(t)`, less the charges of
   step 6. The formula runs every month; its three terms are non-zero in two of them.
8. **EOM, every month** — decrements in the order death, early release, transfer out, at
   `q_m`, `w_e,m`, `w_r,m`; pay `claims_death`, `claims_early_release`, `claims_transfer`
   on the exiting probabilities, valued on `A(t)`, the balance held in the month of exit.
9. **EOM, every month** — maintenance expense `E(t) = (30/12)·1,018^(t/12)` on the
   in force at the start of the month. *Monthly.*
10. **`t = 12n − 1` only** — settle the survivors: capital leg, annuity conversion,
    commutation test. *Annual, on the horizon anniversary; not spread.*
11. Roll `l(t)`. `age`, `dur(t)`, `y(t)` and `k(t)` advance only where `t ≡ 11 → 0`.

### Anniversary equivalence

Because the three monthly decrement rates compound back to their annual values, the two
monthly credit factors compound back to theirs, and the charge sits at the year boundary,
the recursions above collapse over the twelve months of one plan year to the annual-step
recursions, term for term:

```
l(t + 12)  = l(t) · (1 − q) · (1 − w_e) · (1 − w_r)
E_eu(t+12) = [E_eu(t) + …] · (1 + r_eu) · (1 − c_eu)
g(t + 12)  = g(t) + V_net − arb − charge
```

**Every anniversary state and the entire settlement are therefore identical on the two
grids, to floating point** — verified against a pre-conversion snapshot of the annual-step
model across all twelve shipped model points: worst relative deviation **1,8 × 10⁻¹⁴** on
`av_euro_pp`, `av_uc_pp`, `A`, the death benefit and the management charge at
`t = 12y + 11`, **2,5 × 10⁻¹⁵** on `g`, **1,4 × 10⁻¹⁴** absolute on `l`, and the same on
every field of `result_settlement()` including `claims_maturity` of 47 987,47. So are the
plan-year totals of the credited return and of `premiums`, and every quantity that is one
value per plan year: `k`, `a`, `m`, `arb`, `q`, `w_e`, `w_r`, `ι`, `y` and the attained age.
A monthly run can be checked against an annual one on those columns alone.

**Nothing else agrees, and nothing else should.** Claims fall at the end of the month of
exit and are valued on the balance held then, so on the anchor cell `claims_death` falls
2,49 % (2 160,30 → 2 106,52), `claims_early_release` 1,54 % (6 878,40 → 6 772,42) and
`claims_transfer` 0,35 % (4 225,92 → 4 211,07); maintenance expense accrues monthly on a
decrementing block, so the aggregate falls 0,61 % (334,87 → 332,82) while the per-policy
total rises 0,82 % (397,87 → 401,14) on the monthly-compounded inflation factor; and the
split between the three decrements moves while their total does not. `liability_cf` and
`net_cf` follow. The cash flows are where the finer grid does its work.

### Known modeling pitfalls

These are the ways an implementation of *this* product looks right and is wrong. Each is
a test.

1. **Off-by-one on the glide-path band.** Bands are read on years *remaining*, and the
   boundary values 10, 5 and 2 belong to the tighter band **[std]**. Bands are read at
   `k(t) = n − t // 12`, so assert `a = 20 %` at `k = 10`, `50 %` at `k = 5`, `70 %` at
   `k = 2` **at the rebalancing months** — and assert that every month of a plan year reads
   the same band. The looser reading understates the euro share for a full year at each of
   three transitions.
2. **Charging arbitrage on the *versement*.** New money is allocated at the target mix and
   is not a switch. Assert `arbitrage_charge_pp(t) = 0` in a plan year whose account opens
   exactly on target, even though a *versement* was paid — and `= 0` in the eleven months
   of every plan year that are not its first, where there is no switch at all.
3. **Taking the arbitrage charge from the destination**, which leaves the post-rebalancing
   euro share **below** the regulatory minimum. The assertion has to be stated by
   direction, because the source-charging convention above and a share at or above the
   line cannot both hold on a reverse switch. Assert
   `av_euro_pp_at(t, "BOM") ≥ a(t) · av_pp_at(t, "BOM")` where `m(t) ≥ 0` — the ordinary
   de-risking switch, where the UC bucket is the source and the euro destination receives
   the switch in full — and
   `av_euro_pp_at(t, "BOM") ≥ a(t) · av_pp_at(t, "BOM") − (1 − a(t)) · arb(t)` where
   `m(t) < 0`, the euro support being the source and so bearing the charge out of the
   balance being measured. Both are measured **in a rebalancing month** (pitfall 4). `check_euro_share_min()` tests exactly that pair, against
   `euro_share_min_bound(t)`. **An unconditional `≥ a(t)` is wrong** and one shipped model
   point breaks it: point 2 opens 40 % euro against a 20 % minimum, sells euro down to the
   grid, and lands at `3 988 / 19 988 = 19,95 %`. That is the gap these notes leave open,
   not a defect in the model; a firm that resolves it by charging the UC side in both
   directions changes one branch of the rebalancing and nothing else.
4. **Testing the minimum at the wrong moment — the sharpest pitfall on the monthly grid.**
   The minimum binds at the rebalancing **date**, not continuously; between dates the mix
   drifts with relative performance, and on a monthly grid there are **eleven months** of
   that drift rather than an instant. In the worked example the euro share is 70,0006 %
   after the rebalancing that opens the last plan year, month 132, and falls monotonically
   to 69,67 % at the anniversary, month 143 — so the residual
   `av_euro_pp_at(t, "BOM") − a(t)·av_pp_at(t, "BOM")` is **negative by construction in
   eleven months of twelve**, and a `check_euro_share_min()` looping over the whole frame
   fails on every model point while nothing is wrong. Restrict it to the months where
   `t ≡ 0 (mod 12)`. Re-imposing the target every month would invent a rebalancing
   frequency the contract does not have; see *Key sensitivities* for what it would cost.
5. **Setting the capital floor at gross premiums.** The guarantee is *versements* net of
   loading and net of charges taken [S1] [S3] [S7]. Assert
   `av_pp(t) − death_floor_pp(t) = [A⁻(0) − g⁻(0)] + Σ` gross investment return — the
   opening gap being the state carried into `t = 0`, not a row of the frame — and that the
   floor stops at the 70th birthday and caps at €762 245 [S1] [S3]. The identity closes
   **month by month**, not merely at anniversaries, and the base is flat between the two
   months that move it.
6. **Calling either exit a lapse.** There is no surrender right [R3 L. 224-4](#frlib-per_assurance-r3), no surrender
   charge and no market value adjustment. Assert `claims_early_release(t)` is the **whole**
   account value and that no `lapse_rate` or `claims_lapse` exists.
7. **Getting the transfer indemnity window wrong.** It is measured from the **first
   *versement***, not from the projection start [R3 L. 224-6](#frlib-per_assurance-r3).
   Assert `claims_transfer(t) / (d_transfer(t) · av_pp(t))` equals 0,99 while
   `y(t) = duration_ifo + t // 12 + 1 < 5` and 1,00 afterwards. The window is measured in
   the plan's own 1-based year, not in the projection index, and on the monthly grid it is
   **exactly** a month test: `y(t) < 5` if and only if `12·duration_ifo + t < 48`, because
   `duration_ifo` is a whole number of years. Nothing about it changes with the grid.
8. **Double-counting exits.** Assert `d_death(t) + d_release(t) + d_transfer(t) + l(t) =
   l⁻(t)` exactly, every **month** — in cells names, `pols_if(t)` less the three decrements
   equals `pols_if_at(t, "AFT_DECR")`. Reading `pols_if` as the *end*-of-period count here
   is the second pitfall hiding inside the first: see *The exposure convention*. And note
   what the monthly grid does **not** break: the three decrements are re-split by the finer
   chain — deaths −1,19 %, releases −0,23 %, transfers +0,98 % over the anchor's first plan
   year — while their **total**, and so `l` at every anniversary, is unchanged. A test that
   pins a single decrement total to the annual grid's figure will fail, and correctly.
9. **Discounting the annuity conversion.** A PER tariff may not use a positive technical
   rate [R9 A. 142-1](#frlib-per_assurance-r9). Assert `a_x` equals the undiscounted sum of survival probabilities
   on the tariff table. A 2 % rate would shorten the factor from 22,0000 to
   `(1 − 1,02⁻²²) / 0,02 = 17,658` — a fall of **19,7 %** — and so inflate the annuity,
   which is `annuity_cap / a_x`, by `22 / 17,658 − 1 =` **24,6 %**. Quoting the fall in
   the factor as the rise in the annuity is itself the arithmetic slip; the two are not
   the same number.
10. **Commuting on a different basis from the conversion, or testing the threshold
    annually.** Assert `commuted = annuity_cap · (1 − c_arr)` exactly — commuting at a book
    value manufactures a gain out of nothing — and remember €110 is a **monthly**
    *quittance* scaled by the months in the payment period [R10], so an annual frequency
    tests against €1 320.
11. **Mixing per-policy and aggregate.** `av_pp` is per policy and already excludes
    decrements; multiplying a claims column by `pols_if` again understates every benefit by
    the square of the survival factor.
12. **Running the plan past the horizon, or putting tax in it.** The projection ends at
    the declared retirement age: the frame's last row is `t = proj_len − 1 = 12n − 1`,
    `k(t)` never goes negative and no *versement* arrives after settlement —
    `premium_pp(proj_len)` and `years_to_horizon(proj_len)`, one **month** past the frame,
    are both nil. Reading `proj_len` as the last index rather than the row count runs the
    plan one month past its own horizon. Note also that `premium_pp(proj_len − 1)` is now
    nil for an ordinary reason: the last *versement* falls in the month that **opens** the
    last plan year, `proj_len − 12`, not in the last month. And the deduction election, the
    age-graded fractions and the social levies change what the holder keeps, never what the
    insurer pays [R19] [R20] [R21].
13. **Dividing an annual rate by twelve.** Every decrement and every return in this product
    is published annually and must be converted at the constant force,
    `1 − (1 − q)^(1/12)` for a decrement and `(1 + r)^(1/12) − 1` for a return. A twelfth
    overstates the anchor cell's plan-year mortality by 0,23 % and its euro credit by
    3,4335 % against a stated 3,38 %, and it destroys the anniversary equivalence. Assert
    the conversion in the direction that is true — `1 − (1 − q_m)^12 = q` — and **never**
    `12·q_m = q`, which is a linearity the conversion does not have.
14. **Levying the management charge monthly.** The single most likely way to get this
    conversion wrong, because it *looks* harmless: the account value at every anniversary
    survives it untouched, since `(1 + r_m)^12 (1 − c_m)^12 = (1 + r)(1 − c)` when
    `c_m = 1 − (1 − c)^(1/12)`. What does not survive is the *garantie plancher* base,
    which accumulates a **sum** of charges rather than a product of factors: twelve monthly
    charges do not add to the annual one, and `g` at the anniversary moves by up to
    **71,95 €** on the anchor cell and **531,57 €** on model point 12. The charge is a
    contractual event on a date; it lands whole in the anniversary month.

---

## Policyholder behavior modeling

All dynamic formulas are **[std]**: no public French experience exists for PER lapse,
early-release, transfer or annuitisation rates by duration or age [research §18].

- **Base rates.** `early_release_rate` 1,60 % and `transfer_out_rate` 1,00 %, flat,
  anchored on the 2,62 % aggregate of [R22] — assumption footnote (3). These are **annual**
  rates and are spread over their twelve months at `w_e,m` and `w_r,m`, the constant-force
  conversion, so twelve months compound back to the calibrated annual figure exactly.
- **Transfer-out step at the five-year point.** The indemnity falls from 1 % to nil at the
  fifth anniversary [R3 L. 224-6](#frlib-per_assurance-r3) and a rational holder waits. A multiplier of **0,7**
  in the years before the anniversary and **1,3** in the anniversary year is the reference
  shape **[std]** — off in the base run so the worked example stays transparent. It is a
  multiplier on the **annual** rate, applied before the monthly conversion, so it grades
  once a plan year as the behaviour it models does and not once a month. The pair
  is chosen so that the two adjacent years average to exactly 1,00 and turning the shape
  on does not quietly move the flat 1,00 % calibration; note that it is mean-preserving
  over **those two years only**, and that a run with several pre-anniversary years at 0,7
  averages below 1 and would have to be rescaled.
- **Early release is event-driven, not price-driven.** Its causes are death of a spouse,
  invalidity, serious illness of a dependent child, over-indebtedness, exhaustion of
  unemployment rights, business liquidation and purchase of the main residence
  [R3 L. 224-4](#frlib-per_assurance-r3). Only the last is discretionary, and none responds to investment
  performance; a dynamic moneyness multiplier would be a category error here.
- **The horizon is the behavioral variable.** The holder may move the declared retirement
  date at any time [R5 D. 224-3](#frlib-per_assurance-r5), re-cutting the whole allocation immediately [S3] [S4].
  That is the largest behavioral lever on this product and it has no public calibration.
- **Annuity election.** `annuity_share = 0,30` **[std]**; the 2024 payment-phase amounts
  split 47 % annuity, 28 % capital, 25 % commuted small annuity [R22], the third being an
  annuity election that reverses at settlement. **Commutation** is the insurer's option
  exercised with the annuitant's agreement [R10 A. 160-2](#frlib-per_assurance-r10); the base model commutes
  deterministically whenever the test passes, and a `commutation_agreement_rate`
  **[std]** is the natural refinement.

---

## Worked example

Anchor cell (product-spec, *Anchor model cell*): male, `age` 52 at t = 0, retirement age
64, so `n = proj_years = 12`, `proj_len = 144` months, the frame is `t = 0 … 143` and
`k(0) = 12`; `duration_ifo = 2`, so the plan is already in its third year at `t = 0` and
`y(0) = 3`; compartment c1; *équilibré* profile; `av_euro_init = 0,00`,
`av_uc_init = 16 600,00` [R22], `death_floor_init = 16 000,00` **[std]**;
`premium = 3 000,00` paid in the **first month of each plan year** to the horizon —
months `t = 0, 12, …, 132` — `V_net = 2 925,00` after the 2,50 % loading [S8]. Assumptions:
`r_eu = 3,38 %` [S9] carried flat **[std]**, `c_eu = c_uc = 0,70 %` [S8] [S9],
`r_uc = 5,00 %` **[std]**, `arb_rate = 0,30 %`
[S1], `q = 0,00500` flat **[std]**, `w_e = 1,60 %` and `w_r = 1,00 %` **[std]**, transfer
indemnity 1 % while `y(t) < 5` [R3 L. 224-6](#frlib-per_assurance-r3). Account columns are **per policy**, in
euros, to the cent; `l(t)` to six decimals.

The four annual rates above are converted at the constant force to the rates the recursion
applies:

```
q_m    = 1 − (1 − 0,00500)^(1/12) = 0,00041762      12·q_m = 0,0050115, 0,23 % too much
w_e,m  = 1 − (1 − 0,01600)^(1/12) = 0,00134321
w_r,m  = 1 − (1 − 0,01000)^(1/12) = 0,00083718
r_eu,m = (1 + 0,0338)^(1/12) − 1   = 0,00277395
r_uc,m = (1 + 0,0500)^(1/12) − 1   = 0,00407412
```

and twelve of each compound back to 0,00500, 0,01600, 0,01000, 3,38 % and 5,00 % exactly.

### The twelve months of the first plan year (`t = 0 … 11`)

The table that makes the monthly grid legible, per policy. Three things to read off it:
the *versement* arrives **once**, in month 0; the management charge falls **once**, in
month 11, on the post-crediting balance, and it is the same 143,51 the annual grid levied;
and the *garantie plancher* base is **flat** in between, moving only when those two do.
`l⁻(t)` is the count each month opens with, which is `result_cf()`'s `pols_if` on the same
row.

| t | V_net | credited | charge | av_pp | g(t) | l⁻(t) |
|---|---|---|---|---|---|---|
| 0 | 2 925.00 | 79.55 | 0.00 | 19 604.55 | 18 925.00 | 1.000000 |
| 1 | 0.00 | 79.87 | 0.00 | 19 684.42 | 18 925.00 | 0.997404 |
| 5 | 0.00 | 81.18 | 0.00 | 20 007.17 | 18 925.00 | 0.987087 |
| 10 | 0.00 | 82.85 | 0.00 | 20 418.06 | 18 925.00 | 0.974341 |
| 11 | 0.00 | 83.19 | **143.51** | **20 357.74** | **18 781.49** | 0.971812 |

The month-0 decrement is the check on the rate conversion: `l⁻(1) = (1 − 0,00041762) ·
(1 − 0,00134321) · (1 − 0,00083718) = 0,997404` ✓, and twelve such months land on
`l(11) = 0,969289` — the annual model's `l(0)`, exactly. The last row is the annual grid's
first row: `av_pp = 20 357,74` and `g = 18 781,49`, to floating point.

### The same frame on the plan year (`y = 0 … 11`)

This is the table the annual-step model printed, **value for value**: every quantity in it
is a rebalancing or an anniversary quantity, and not one of them moved. What changed is the
*index* each is read at. Row `y` is months `t = 12y … 12y + 11`; `k`, `a(y)`, `V_net` and
`arb` are read at the **rebalancing month** `t = 12y`, and the three balances and `l` at
the **anniversary month** `t = 12y + 11`. `result_state_annual()` publishes exactly this.

The row labels are the 0-based projected plan year, so the first is `y = 0` and the last is
`y = 11`. The last column is `l`, the in force at the **end** of the plan year — the
`pols_if_eoy` column, not `result_cf()`'s `pols_if`, which on row `t` carries `l⁻(t)`. See
*The exposure convention*.

| y | months t | k | a(y) | V_net | arb | av_euro_pp | av_uc_pp | av_pp | l |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 0–11 | 12 | 0 % | 2 925.00 | 0.00 | 0.00 | 20 357.74 | 20 357.74 | 0.969289 |
| 1 | 12–23 | 11 | 0 % | 2 925.00 | 0.00 | 0.00 | 24 275.75 | 24 275.75 | 0.939522 |
| 2 | 24–35 | 10 | 20 % | 2 925.00 | 14.57 | 5 584.66 | 22 673.50 | 28 258.16 | 0.910668 |
| 3 | 36–47 | 9 | 20 % | 2 925.00 | 0.20 | 6 402.30 | 26 010.29 | 32 412.59 | 0.882701 |
| 4 | 48–59 | 8 | 20 % | 2 925.00 | 0.24 | 7 255.25 | 29 475.54 | 36 730.79 | 0.855592 |
| 5 | 60–71 | 7 | 20 % | 2 925.00 | 0.27 | 8 141.84 | 33 077.41 | 41 219.24 | 0.829316 |
| 6 | 72–83 | 6 | 20 % | 2 925.00 | 0.31 | 9 063.37 | 36 821.28 | 45 884.65 | 0.803847 |
| 7 | 84–95 | 5 | 50 % | 2 925.00 | 41.64 | 25 053.10 | 25 402.28 | 50 455.38 | 0.779161 |
| 8 | 96–107 | 4 | 50 % | 2 925.00 | 0.52 | 27 399.17 | 27 827.98 | 55 227.15 | 0.755232 |
| 9 | 108–119 | 3 | 50 % | 2 925.00 | 0.64 | 29 848.43 | 30 315.50 | 60 163.93 | 0.732038 |
| 10 | 120–131 | 2 | 70 % | 2 925.00 | 36.80 | 45 335.35 | 19 695.53 | 65 030.89 | 0.709557 |
| 11 | 132–143 | 1 | 70 % | 2 925.00 | 0.56 | 48 832.72 | 21 255.68 | 70 088.40 | 0.687766 |

### Settlement

Settlement of the survivors in the last projected month, `t = 143` — the horizon
anniversary — with `annuity_share = 0,30`, `a_x = 22,0000` **[std]** and `c_arr = 1,50 %`
[S8]. Every value below is the annual grid's, unchanged: the settlement is a contractual
event on a date the finer grid does not move.

| Quantity | Value |
|---|---|
| `av_pp(143)` | 70 088.40 |
| `capital_leg = 0,70 · av_pp(143)` | 49 061.88 |
| `annuity_cap = 0,30 · av_pp(143)` | 21 026.52 |
| `rente_gross = annuity_cap / 22` | 955.75 |
| `rente_net = rente_gross · 0,985` | 941.41 |
| monthly equivalent `rente_net / 12` | 78.45 |
| commutation test against €110 [R10] | 78.45 ≤ 110 → **commute** |
| `commuted = rente_net · 22` | 20 711.12 |
| `claims_maturity` per policy | 69 773.00 |
| `claims_maturity` aggregate, `× l(143) = 0,687766` | 47 987.47 |
| `death_floor_pp(143)` | 47 267.36 |

### What the finer grid moved

The three claim aggregates and the expense scale are the only figures in this example that
changed, and the annual grid's numbers are kept beside them as the comparison.

| Over the twelve plan years, per model point | Annual grid | Monthly grid |
|---|---|---|
| `claims_death` | 2 160.30 | **2 106.52** (−2,49 %) |
| `claims_early_release` | 6 878.40 | **6 772.42** (−1,54 %) |
| `claims_transfer` | 4 225.92 | **4 211.07** (−0,35 %) |
| `expenses`, aggregate | 334.87 | **332.82** (−0,61 %) |
| `expenses`, per policy before survivorship | 397.87 | **401.14** (+0,82 %) |
| `claims_maturity` | 47 987.47 | 47 987.47 (unchanged) |
| `premiums` | 30 500.77 | 30 500.77 (unchanged) |

Two effects, both of them the point of the exercise. A mid-year exit is now settled on the
balance it actually holds in the month of exit rather than at the year end, which takes all
three claim lines down; and the ordered decrement chain, walked twelve times with small
steps, re-splits the three decrements — deaths −1,19 %, releases −0,23 %, transfers
+0,98 % over the first plan year — while leaving their total, and `l` at every anniversary,
exactly where it was. The two expense figures move in **opposite directions** and both are
printed for that reason: per policy the total rises, because `1,018^(t/12)` compounds every
month instead of stepping once a year; in aggregate it falls, because the charge is now
borne by the in force of each month rather than of the plan-year start.

**Checks.** *(i) The floor identity.* `av_pp(143) − death_floor_pp(143) = 70 088.40 −
47 267.36 = 22 821.04`, and the opening gap `16 600.00 − 16 000.00 = 600.00` — the state
carried into `t = 0` — plus the gross investment return credited over the 144 months,
`22 221.04`, is the same number; the sum now runs over months and lands on the same total.
The *garantie plancher* is therefore 32,6 % below the account value and never bites in
this scenario [S1] [S3]. *(ii) The band crossing at month 84, re-derived.* That plan year
opens with `av_pp = 45 884.65` carried in and `k = 5`, so the target euro share steps from
20 % to 50 %: the target euro balance is `0,50 × 45 884.65 = 22 942.32` against `9 063.37`
held, a switch of `13 878.95`, an arbitrage charge of `0,003 × 13 878.95 = 41.64` taken
from the UC side, and a BOM euro balance of
`9 063.37 + 13 878.95 + 0,50 × 2 925.00 = 24 404.82` — every figure identical to the annual
grid's, because the rebalancing is an annual event on an annual balance. Twelve months of
crediting and the anniversary charge give
`24 404.82 × 1,0338 × 0,9930 = 25 053.09` at month 95, one cent below the table's
`25 053.10` because the model carries the carried-in balance unrounded — intermediates are
at full precision and only reported cash flows are rounded. The BOM euro share is
`24 404.82 / 48 768.01 = 50,0427 %`, at or just above the regulatory minimum as the
source-charging convention requires. Relative performance then moves it, and on the monthly
grid the drift is visible month by month rather than only at the year end: the last plan
year opens at `70,0006 %` at month 132 and closes at `48 832.72 / 70 088.40 = 69,67 %` at
month 143, eleven months of drift below the 70 % target that held at the rebalancing date.
*(iii) The commutation identity.* `941.414625 × 22 = 20 711.12`, which is also
`21 026.52 × 0,985` — commuting at the conversion basis returns the converted capital less
the *arrérage* charge, and the total maturity claim of 69 773.00 is `av_pp(143)` less
`0,015 × 21 026.52 = 315.40`. The anchor cell's annuity, at €78.45 a month, is a live
instance of the market pattern: the average PER annuity in payment is €1 300 a year, about
€108 a month, just under the €110 threshold [R22] [R10], and the cliff for this cell sits
at `annuity_share = 42,06 %` — at 50 % the annuity would be €1 569.02 a year, €130.75 a
month, above the threshold and paid as a *rente*.

Per-policy expenses run `E(t) = (30/12) · 1,018^(t/12)` **[std]**, so `E(0) = 2.50`,
`E(143) = 3.0922` and the undiscounted 144-month total before survivorship is `401.14`.

### Cash flow outputs (per plan month `t`)

`l⁻(t)` below is the count the **month** opens with, which is the `pols_if` column of
`result_cf()` on the same row; `l(12n−1)` is the count the final month closes with,
`pols_if_at(12n−1, "AFT_DECR")`. `V(t)` and `E(t)` are the monthly amounts: `V(t) = V` in
the month that opens a plan year and 0 otherwise, `E(t) = (30/12)·1,018^(t/12)` every
month. `result_cf_annual()` sums these rows into plan years.

| Output | Formula |
|---|---|
| `premiums` | `V(t) · l⁻(t)` |
| `claims_death` | `d_death(t) · max( A(t), g(t) )` |
| `claims_early_release` | `d_release(t) · A(t)` |
| `claims_transfer` | `d_transfer(t) · A(t) · (1 − ι(t))` |
| `claims_maturity` | `l(12n−1) · (capital_leg + commuted)` at `t = 12n − 1`, else 0 |
| `annuity_conversion` | `l(12n−1) · annuity_cap` at `t = 12n − 1` where not commuted, else 0 |
| `expenses` | `E(t) · l⁻(t)` |
| `liability_cf` | claims + `annuity_conversion` + expenses − premiums (outgo-positive) |
| `net_cf` | `− liability_cf` (income-positive, per the house sign convention) |

On the monthly frame only the twelve *versement* months are cash-positive; the statement
that a contributing plan is cash-positive in every plan year but the settlement one is read
off `result_cf_annual()`, where plan years 0–10 are positive and year 11 is −47 395.16
(annual grid: −47 412.01).

---

## Valuation and reserve pointers

This library projects gross best-estimate liability cash flows; valuation layers are
cited, not reproduced.

- **The French statutory provision.** The *provision mathématique* is the difference
  between the actuarial present values of the two parties' commitments, **including
  future management costs** [REG-R6] — not a net-premium reserve. For the annuity phase,
  one contract states it as "la valeur des engagements de rente, fonction de la table de
  mortalité et du taux d'intérêt technique à 0 %" [S3], which at a 0 % rate is a pure
  life-contingent instalment count with no interest offset.
- **Profit sharing.** The statutory minimum PB is determined globally, not contract by
  contract, from a *compte de participation aux résultats* credited with 85 % of the
  financial balance and the technical balance less the insurer's share [REG-R14]
  [REG-R15]; sums parked in the PPB must be released within eight years — **fifteen** for
  commitments under a *comptabilité auxiliaire d'affectation*, which is what a PER is
  [REG-R16] [R8 L. 142-4](#frlib-per_assurance-r8). UC commitments are outside that machinery [REG-R15]. The
  ring fence itself carries a policyholder priority claim and an ACPR-supervised recovery
  plan on under-coverage [R8 L. 142-4 to L. 142-6](#frlib-per_assurance-r8) [REG-R10] — a constraint a
  single-policy model cannot see and a fund-level projection must.
- **Solvency II and IFRS 17 — cited, not specified.** Technical provisions, SCR and risk
  margin [REG-R1] [REG-R2] and the risk-free term structure used to discount [REG-R5]
  were not researched for this product [unverified]; IFRS 17 measures fulfilment cash
  flows plus a contractual service margin from 2023 [REG-R45], its variable fee approach
  for direct participating contracts being [unverified] here. The engine is this same
  projection.
- **Tax, plainly.** Deductibility at entry under CGI art. 163 quatervicies [R13]
  [REG-R42] changes the taxation of the exit — pension regime with the 10 % abatement, or
  *rente viagère à titre onéreux* on an age-graded fraction, or the flat levy on gains
  [R19] [R20] [R21] — but **not the gross liability cash flows**. The insurer pays the same
  euro amount either way; the difference is withheld or assessed downstream. Tax therefore
  appears in no recursion above, and `deduction_elected` is carried solely so a downstream
  tax layer can find it. The same applies to the death-benefit levies, where the trigger
  is the **age at death**, not the age at which premiums were paid, and a PER pays
  inheritance duty on the **whole** benefit after 70 [R15] [REG-R41].
- **Professional standards.** NPA 1 and NPA 2 are *pratiques recommandées* of the Institut
  des actuaires; NPA 2 applies to any actuarial model under a proportionality principle
  [REG-R43] [REG-R44].

---

## Key sensitivities and model risks

1. **The glide path is the product's dominant financial lever.** Moving the *équilibré*
   grid to the *prudent* one raises the euro share from 0/20/50/70 to 30/60/80/90 [R6],
   replacing most of a 5,00 % UC return with a 3,38 % euro return over the anchor cell's
   twelve years. The grid is an input table for exactly this reason.

   **The rebalancing frequency is now a modelling choice, not a constraint.** On an annual
   projection step it was forced; on the monthly grid the model could rebalance as often as
   the sample does — quarterly to semi-annually [S1] [S3] [S7] — and it does not, because
   `allocation_grid.csv` is keyed by whole **years** to the horizon: a sub-annual
   rebalancing re-imposes the *same* target inside the year, so it corrects drift rather
   than de-risking faster, and turning it on is an assumption change rather than a finer
   grid. Measured on this model, moving the anchor cell to semi-annual, quarterly or
   monthly rebalancing changes its final balance by **−0,0095 %**, **−0,0142 %** and
   **−0,0175 %** and its twelve-year arbitrage charge from 95,75 to 96,06, 96,21 and 96,40;
   on the 32-year model point 12 the balance moves −0,0228 %, −0,0343 % and −0,0422 %.
   Small, but no longer unmeasurable — which is itself the argument for stating it.
2. **The declared horizon.** Changing `retirement_age` re-cuts the whole allocation
   instantly [R5 D. 224-3](#frlib-per_assurance-r5) [S3] [S4] and changes the number of years the plan compounds.
   No public data exists on how often holders move it [research §18].
3. **The two exit decrements dominate the run-off.** At 2,60 % a year combined they remove
   about a quarter of the book over twelve years — far more than mortality. Both rates are
   **[std]** on a single aggregate anchor [R22] contaminated by the market's growth phase.
4. **Charge levels, not charge structure, drive the outcome.** The sampled entry loading
   spans 0 % to 4,80 % and the euro management charge 0,50 % to 2,30 % [S1]–[S8]; the
   composite sits near the middle. The *encadré* discloses maxima and caps nothing
   [REG-R30], so a charge level is never a contractual constant.
5. **The annuity factor is a placeholder.** `a_x = 22,0000` is **[std]**; no sampled
   insurer publishes a rate card and TGH05 / TGF05 were not extracted [R12] [REG-R21].
   The commutation cliff at `annuity_share = 42,06 %` moves directly with `a_x`.
6. **Mortality is a proxy.** The shipped decrement CSV is an INSEE-derived **[std]** proxy
   [REG-R24]; the regulatory tables are cited, not shipped [REG-R22] [REG-R23]. The only
   published rate card in the sample is a *gross premium* scale on a no-underwriting death
   rider [S7] and must not be read as a mortality basis.
7. **No PPB stock.** The base model credits the asset return directly, so `r_eu` is an
   assumption rather than an output. Where an insurer smooths — and the one retrieved
   triple shows seven basis points of it [S9] — the crediting path and the PPB balance are
   one two-lever system, with a fifteen-year release horizon here against the general eight
   [REG-R16]. That system is specified in
   `products/assurance_vie_euro/technical-notes.md` and summarised above under *The euro
   leg is cross-referenced, not re-implemented*.
8. **Two options are outside the base run.** The 15 % transfer-value reduction dominates
   the 1 % indemnity by an order of magnitude in a rising-rate scenario [R5 R. 224-6](#frlib-per_assurance-r5)
   [S8], and one contract's annuity table frozen at adhesion for deductible C1 sums [S1]
   is a long-dated longevity option given away for nothing. Neither is visible in a base
   run; valuing either needs a stochastic layer.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-per_assurance-r10
[R11]: #frlib-per_assurance-r11
[R12]: #frlib-per_assurance-r12
[R13]: #frlib-per_assurance-r13
[R15]: #frlib-per_assurance-r15
[R19]: #frlib-per_assurance-r19
[R20]: #frlib-per_assurance-r20
[R21]: #frlib-per_assurance-r21
[R22]: #frlib-per_assurance-r22
[R3]: #frlib-per_assurance-r3
[R6]: #frlib-per_assurance-r6
[REG-R1]: #frlib-reg-r1
[REG-R10]: #frlib-reg-r10
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R16]: #frlib-reg-r16
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R30]: #frlib-reg-r30
[REG-R41]: #frlib-reg-r41
[REG-R42]: #frlib-reg-r42
[REG-R43]: #frlib-reg-r43
[REG-R44]: #frlib-reg-r44
[REG-R45]: #frlib-reg-r45
[REG-R5]: #frlib-reg-r5
[REG-R6]: #frlib-reg-r6
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
