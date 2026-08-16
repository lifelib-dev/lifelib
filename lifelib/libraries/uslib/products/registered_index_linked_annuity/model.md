# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/registered_index_linked_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the 10% buffer, the 1/3/6 year term menu, the guaranteed minimum
> Cap/Step/Edge rates, the 7-7-6-5-4-3-0 withdrawal charge above a 10% free amount, the
> return-of-premium death benefit, the Maturity Date rule and the AG 54 interim value
> algebra — are sourced from the composite specimen. **Every declared rate and every piece
> of market data is a snapshot**: no current rate sheet was retrievable (both insurer rate
> pages returned HTTP 403), and the risk-free rate, dividend yield and implied volatility
> are flat scalars. Every behavioural and expense assumption is a **[std]**
> standardization, and the shipped mortality table is illustrative, *not* the prescribed
> 2012 IAM Basic basis. Replace them with company data and a real market-data interface
> before drawing any conclusion from the numbers.

This model is built on the **deferred annuity base chassis**,
[`MYGA_US_S`](../fixed_deferred_annuity/model.md), and shares its cells
names for every concept the two have in common. Where the RILA notes restate a recursion
with product-specific parameters, this model follows the RILA notes rather than the
chassis — and in three places that means the chassis mechanic is **absent**, not merely
different. See *What this model does not inherit from the chassis* below.

## Run it

```bash
python products/registered_index_linked_annuity/run.py
python products/registered_index_linked_annuity/run.py 2      # Scenario B, with the withdrawal
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/registered_index_linked_annuity/RILA_US_S")
model.Projection[1].result_iv()
```

`Projection` takes a `point_id`; `Projection[1]` and `Projection[2]` are the worked
example's anchor cell on the notes' Scenario A and Scenario B. `result_iv()` is **the
notes' own table**, one row per month: index level, index performance, `tau`, the fixed
income asset proxy, one column per replicating-portfolio leg, the derivative asset proxy,
the trading cost, the interim value and the Investment Amount. `result_cf()` returns the
cash flow statement indexed by policy month, `result_av()` the account values and
benefits, and `result_pols()` the in-force movements.

The model and both of its Spaces carry docstrings. `model.doc` describes the product and
the projection basis, `model.Projection.doc` holds the full mapping between the technical
notes' symbols and the cells names, and `model.Data.doc` the input arrangement.

## An option pricer is a precondition, not a refinement

A conforming RILA model **requires an option-pricing routine and a market-data
interface**. Actuarial Guideline LIV makes the Interim Value — the value at which *every*
mid-term withdrawal, surrender, death benefit, annuitization, transfer and fee deduction
settles — the market value of a hypothetical replicating portfolio of European options
plus a fixed income proxy [R2], and the source prospectuses implement exactly that with
Black-Scholes [S2] [S6]. No other product in this library has a contractual value that
cannot be computed without a derivatives pricer.

The three components the notes insist on separating are separate here too:

| Component | Cells |
|---|---|
| Crediting engine | `credit_rate_at`, `credit_rate_term`, `credit_rate_accrued` |
| Interim-value engine | `opt_component`, `opt_portfolio`, `iv_factor`, `iv_ratio` |
| Market-data provider | `Data.market_scenario()`, `index_level`, `mvr`, `risk_free`, `div_yield`, `impl_vol` |

Black-Scholes lives in `norm_cdf`, `bs_d1`, `bs_d2`, `bs_call`, `bs_put` and
`bs_binary_call`, written against the standard library's `math.erf` — no `scipy`. The
rate arguments are **annual effective** and are converted to continuous compounding inside
the pricer, so the 4.00% and 2.00% market inputs enter as `ln 1.04 = 3.9221%` and
`ln 1.02 = 1.9803%` exactly as the notes state.

## Monthly, and `t` is a month **end**

`t` counts policy months and denotes month ends, with `t = 0` the Issue Date. The
contractual interim value is a *daily* quantity; the model evaluates it at each month end
**[std]**, which resolves every contractual boundary because terms are whole years, the
withdrawal-charge schedule runs by complete contract years and the free-withdrawal limit
resets annually. A daily sub-grid is needed only for a path-dependent Performance Lock
election module, which is not implemented.

**`duration(t) = t // 12`, not `ceil(t/12) - 1`.** That is the notes' own `cy(t) =
floor(t/12)`, and it differs by one step from `MYGA_US_S`. The reason is the
timing convention: the MYGA chassis takes elective transactions at the *beginning* of the
month, so month 12 belongs to the contract year that is opening; here `t` is a month
*end*, so month 12 **is** the first anniversary and one complete contract year has
elapsed. The withdrawal charge steps and the free-withdrawal allowance resets on the
anniversary itself. The two conventions agree in every month except the anniversaries.

### A month-end index needs both readings, and the model carries both

`duration(t)` is read **at** the instant `t`, and that is right for anything settled
there: the withdrawal charge a transaction bears (`surr_charge_rate`), the
free-withdrawal base snapshotted at the anniversary (`free_wd_base`), and — because it
must move in the same month as the charge it responds to — the charge-expiry lapse shock
(`lapse_rate_sc_mult`, keyed on `policy_year(t) = duration(t) + 1`).

It is the wrong reading for a rate applied **across** month `t`. The monthly mortality
rate `q_m(t) = 1 - (1 - q_x)^(1/12)` is an exposure rate for the whole interval
`(t-1, t]`, and the maintenance expense is incurred over the same interval; both belong to
the contract year that interval lies inside, which is `ceil(t/12)`. So `age(t)` and
`inflation_factor(t)` are keyed on a second cells, **`duration_bom(t) = ceil(t/12) - 1`**
— the complete contract years at the *start* of month `t`, and the same reading
`MYGA_US_S` uses for its own `duration(t)`.

The difference is one month and it appears only in anniversary months, but it is not
cosmetic: on `duration(t)` the attained age would step at month 12, leaving eleven months
of contract year 1 at `q_x` and charging the twelfth at `q_(x+1)` (0.005495 against
0.006065 on the anchor cell), and the expense inflation step would land a month early
against the notes' `60/12 x 1.025^(y-1)`. At the Maturity Date the consequence is visible
in the other direction: `age(proj_len())` is 89, the age *during* the last month, and the
owner attains 90 at its end — which is the Maturity Date the contract's own rule names.

`proj_len()` is contractual rather than chosen: the Maturity Date is the later of the
anniversary after the oldest owner's 90th birthday and ten years from issue [S2], so
`policy_term() = max(90 − age_at_entry(), 10)` years — 360 months on the anchor cell.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `RILA_US_S/` holds nothing but formulas:

```
products/registered_index_linked_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  market_scenario.csv
  surr_charge_table.csv
  guar_min_rate_table.csv
  lapse_table.csv
  withdrawal_table.csv
  run.py
  README.md
  RILA_US_S/    <- formulas only
    __init__.py                         (model docstring)
    _system.json
    Data/__init__.py                    (reads the CSVs, once per model)
    Projection/__init__.py              (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for every
model point. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data` — so each file is read once per model no matter how many contracts are
projected, and `Projection[1].data is Projection[2].data`.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read,
so it works wherever the repository is checked out. Each table has a filename Reference and
a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `market_scenario_file` | `market_scenario()` | `market_scenario.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |
| `guar_min_rate_file` | `guar_min_rate_table()` | `guar_min_rate_table.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `withdrawal_file` | `withdrawal_table()` | `withdrawal_table.csv` |

**The trade-off:** the model is not portable on its own. Copy
`RILA_US_S/` without the CSVs and it will read fine, then fail on
first evaluation. What you gain is that a diff of the model shows logic changes only, and
an input can be edited or swapped in place — point `Data.mort_table_file` at another
same-schema file and the projection follows, with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Fifteen contracts. **Points 1 and 2 are the worked example's anchor cell** — M60 / $100,000 / one 6-year Cap option / 10% buffer / 100% cap — on Scenario A and Scenario B, point 2 carrying the illustrative $8,000 withdrawal. Point 3 runs the notes' base *behavioural* withdrawal rule. Points 4–14 carry Step, Edge and Floor crediting, interim value families (b) and (c), the pre-AG 54 engine, the updated-time-to-expiry amortization, a 110% participation rate on a 20% buffer, an uncapped option at issue age 81, the NGE cap-solve, and a charged excess withdrawal. **Point 15 is the notes' second labelled verification**, the [S2] withdrawal-charge example — see below | contract terms sourced [S1] [S2] [S4] [S5]; declared rates and every behavioural switch **[std]** |
| `mort_table.csv` | Annual mortality by attained age 40–120 and sex, with a `provenance` column | **[std]** illustrative annuitant curve. **Not a published table.** The prescribed basis is 2012 IAM **Basic** with generational Projection Scale G2 [REG-R59], which may not be redistributed here — swap it in by repointing `Data.mort_table_file` |
| `market_scenario.csv` | Four deterministic scenarios keyed by `(scenario_id, t)`, read as step functions: `up` (index 100 → 120 at month 36 → 140 at month 72, the Market Value Rate rising 100 bp at the term midpoint), `down` (100 → 80 → 75, same rate rise), `legacy` (500 → 600 at month 6, the pre-AG 54 source example) and `charge_ex` (100 → 71.66666667 at month 60, the level that lands the Account Value on exactly $80,000 for the [S2] withdrawal-charge example). The index path is therefore piecewise constant between the notes' own anchor months, and flat after the last of them | worked example [std]; the flat 4.00% / 2.00% / 20.00% market state is **[std]** |
| `surr_charge_table.csv` | The withdrawal charge by **complete** contract year: 7, 7, 6, 5, 4, 3, 0 per cent | sourced [S1] [S2] |
| `guar_min_rate_table.csv` | Guaranteed minimum Cap / Step / Edge rates by term: 2% / 6% / 8% Cap at 1 / 3 / 6 years, 2% Step and Edge | sourced [S1] [S2] |
| `lapse_table.csv` | The un-shocked annual surrender rate by contract year. The charge-expiry shock is **not** in this file: its size is the `lapse_shock_mult` Reference and the year it lands in is derived from `surr_charge_table.csv` by `lapse_shock_year()`, so the shock cannot drift away from the charge whose expiry causes it | **[std]** reference shape; the RILA-specific tables in [REG-R64] sit behind a paid data package |
| `withdrawal_table.csv` | Three scheduled programmes keyed by `(wd_schedule_id, t)`: none, the worked example's $8,000 at month 36, and a charged $20,000 at month 24 | worked example [S2]; the variant **[std]** |

Every model point projects to completion, and a test asserts it. Between them they exercise
**all four crediting types, all four interim-value families, both amortization conventions,
the uncapped branch, the participation-rate branch, the NGE cap-solve, both death benefit
bands and both readings of the withdrawal divergence** — so no branch of the notes'
parameter set is dead code.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`, and this
library's `MYGA_US_S`, wherever those have an analogue: `pols_*` for policy
counts, `av_*` for account values, plural nouns for cash flows, `*_rate` for rates, `*_pp`
for per-contract amounts, `*_at(t, timing)` for a quantity read at a point inside the
month, plus `model_point`, `age_at_entry`, `sex`, `policy_term`, `proj_len`,
`duration_mth`, `duration`, `age`, `net_cf`, `result_cf`, `check_av_roll_fwd`.

Four library-wide conventions are worth stating because each of them settles a name this
model once spelled its own way:

- **`pols_if(t)` is the count at the *start* of month `t`**, and is the weight applied to
  that same row's cash flows — so `premiums(t) / premium_pp()`,
  `withdrawals(t) / wd_payment_pp(t)` and `expenses(t)` over the per-contract maintenance
  charge all return the `pols_if` column of `result_cf()`. `pols_if(1) = pols_if_init()`,
  exactly as in `Term_US_A`. The notes' own **end**-of-month `l(t)` is not lost: it is
  `pols_if_at(t, "AFT_DECR")`, the last point of the decrement chain, and it is what
  `result_pols()` prints as `pols_if_aft_decr`.
- **`lapse_rate(t)` is annual and `lapse_rate_mth(t)` is monthly**, matching the
  `mort_rate` / `mort_rate_mth` pair. The decrement chain reads the monthly one; the
  notes' `w_annual(y,t)` is `lapse_rate` and their `w_m(t)` is `lapse_rate_mth`.
- **`lapse_rate_sc_mult(t)` is the charge-expiry shock multiplier** — the name the four
  universal-life models use for the notes' `M_sc` — and `lapse_shock_mult` is the scalar
  Reference carrying its **[std]** size of 3.0.
- **Every `check_*` takes no argument and returns a bool** over all projected `t`, as
  `CashValue_SE.check_av_roll_fwd()` does, so one test can call the same check across the
  library. The signed per-month residual is still there under `check_*_resid(t)`, which is
  what a failing check needs.

The technical notes use compact actuarial symbols instead; the full mapping lives in the
`Projection` Space docstring. Six cases needed care, and every one is a collision the notes
themselves carry — this product speaks three vocabularies at once (contract mechanics,
Black-Scholes, and the deferred annuity chassis):

| Notes | Cells | Why |
|---|---|---|
| `T` term length | `term_years` | `T` is in **years** while `t` is the policy **month**; `tau` is likewise in years |
| `P` | `premium_pp` / `bs_put` | The single purchase payment and the Black-Scholes put share a letter |
| `C` | `bs_call` / `mvr_at_term_start` / `surr_charge_pp` | The call, the [S2] fixed-leg symbol for the term-start Market Value Rate, and the chassis's surrender charge |
| `B` vs `b` | `budget_amort_pp` / `buffer` | The amortized option budget and the buffer differ only by case |
| `R` vs `r` | `index_perf` / `mvr` | Index performance and the Market Value Rate differ only by case |
| `M_sc`, `M_iv` vs `M(t)` | `lapse_rate_sc_mult`, `lapse_iv_mult` / *(absent)* | On the chassis `M(t)` is a **contract** market value adjustment; here the `M`s are lapse multipliers and there is no contract MVA at all |

One shared name takes a different argument from the chassis, deliberately.
`MYGA_US_S` keys `free_wd_base(y)` and `free_wd_allow(y)` on the contract
**year**; here they take the policy **month**, because the free-withdrawal base is
snapshotted from the Account Value at the most recent anniversary *before* that month's
transaction — `av_pp_at(12 * duration(t), "BEF_WD")` — and keying on `t` keeps one index
type through the whole file. The concept and the name are the same; only the argument
differs, and the `Projection` docstring's symbol table shows it.

## What this model does not inherit from the chassis

Three chassis mechanics are deliberately **absent**, and their absence is the modelling
statement:

- **No contract market value adjustment.** The only MVA-like term in the prospectus is the
  `[(1+C)/(1+D)]^E` factor *inside* the interim value [S2], which is why it is
  `mva_factor` — a factor, in the interim value — and there is no `mva_pp`, no `mva_rate`
  and no `mva_cap_rule` anywhere in this model. AG 54's project history explains why
  carriers diverge here: specific MVA requirements were deliberately removed from the
  guideline because consensus was unreachable [R2].
- **No Model #805 minimum guaranteed surrender value.** AG 54 displaces Model #805 outright
  when it is satisfied [R2] [REG-R42] [REG-R44], and the nonforfeiture value **is** the
  interim value. There is no `mgsv_pp`. (Were #805 to apply, note that the indexed
  nonforfeiture rate is floored at **15 basis points**, not 1% [REG-R42] — the same trap
  the chassis documents.)
- **No book value.** Between term start and term end the contract has no account value in
  the ordinary sense: `av_pp(t)` is a derivative price, and it is depressed exactly when
  the return-of-premium guarantee is in the money.

The chassis mechanics that *are* inherited — the composition of a surrender benefit, the
free-withdrawal base and its non-cumulative annual reset, the withdrawal-charge schedule
keyed on complete contract years, the decrement ordering and the `pols_maturity`
bookkeeping — keep the chassis's names.

## `tau = 0` belongs to the expiring option

The single most load-bearing convention in the file. At a Term End Date two options exist
in the same month: the one that is closing and the one that is opening. `term_elapsed_mth`,
`tau`, `index_at_term_start`, `mvr_at_term_start` and every option leg refer to the
**expiring** one, so `tau(72) = 0` rather than `6`.

That is what makes the notes' verification identity fall out of the algebra instead of
having to be imposed. At `tau = 0` the Black-Scholes functions return intrinsic value, the
amortized budget is zero, the trading cost is switched off and the MVA factor is 1, so

```
Pi(I, 0) = max(R,0) − max(R−c,0) − max(−b−R,0) = g       and       V = IA(1 + g)
```

for the Cap design, and the corresponding identity holds for Step, Edge and Floor. A test
asserts `check_term_end_identity()` and, term end by term end,
`check_term_end_identity_resid(t) == 0` for every crediting type. The
same convention makes the Transfer Period rule automatic: `iv_ratio` is exactly 1 there, so
the interim value equals the Investment Amount [S2] with no special case.

Homogeneity is imposed in one place, `budget_amort_factor`: `B` is defined against the
*current* `IA`, so every term of the interim value scales with the notional. That is why a
withdrawal reduces the interim value by exactly the cash removed — a test checks each
component scales by one factor and that `V` falls by precisely $8,000.

## The worked example and the base withdrawal rule contradict each other

The notes give a base behavioural withdrawal rule — "0% in contract year 1; thereafter 2%
of Account Value per year, taken at contract anniversaries and capped at the Free
Withdrawal Amount" — and a worked example whose Investment Amount is **exactly $100,000**
at the term midpoint, with the illustrative $8,000 as the only withdrawal. Both cannot
hold: 2% taken at months 12 and 24 would leave less than $100,000 of notional at month 36,
and the whole worked example is built on that figure.

Rather than pick one, the model ships both, the way `Term_US_A` ships its `M(1)`
divergence. `wd_rate_ann` is a **model point column**, not a Reference: points 1 and 2 set
it to 0 and reproduce the worked example to the cent; point 3 is otherwise identical to
point 1 and runs the behavioural rule at 2%. A test pins the gap open in both directions.
Neither is "correct" — the worked example is an illustration of the interim-value
mechanics and the 2% rule is a **[std]** behavioural assumption.

## The [S2] withdrawal-charge example needs a model point of its own

The notes carry a second explicitly labelled verification beside the interim-value table:
*"$100,000 payment, $80,000 Account Value at the start of contract year 6, full withdrawal
→ `FW = $8,000`, chargeable `$72,000`, `wc(5) = 3%`, charge `$2,160`, cash value
`$77,840`."* It is not reproducible on the anchor cell, whose Account Value at month 60 is
whatever Black-Scholes makes it, and re-deriving `AV − wc × (AV − FW)` from the model's own
cells asserts nothing: that composition *is* `surr_value_pp`.

So **model point 15 exists to put an Account Value of exactly $80,000 on the table at
month 60**. It runs the pre-AG 54 engine — the only interim-value family whose value is a
closed-form function of the index level — on a scenario whose index sits at
`71.66666667` from month 60, the level at which the accrued crediting rate is exactly
`min(0, −28.3333% + 10% × 5/6) = −20%`. Everything else then falls out of the contract:
the free amount is 10% of the anniversary Account Value, so `$8,000`; `wc(cy(60)) =
wc(5) = 3%`; the charge is `$2,160` and the cash surrender value `$77,840`, to a rounding
error of three millionths of a dollar. The crediting engine is a device here and nothing
more — the example is about the charge, which is engine-independent.

## The notes print the MVA factor as 0.971690

A display slip worth recording, because a reader checking the arithmetic by hand will hit
it. The notes state the interest-rate adjustment as `(1.04/1.05)^3 = 0.971690`. The actual
value is **0.9716998**, and every dollar figure in the table requires it: `94,968.40 ×
0.9716998 = 92,280.78`, while `94,968.40 × 0.971690 = 92,279.85`, nearly a dollar adrift.
The model computes the factor and reproduces the dollars; the test asserts
`mva_factor(36) == (1.04/1.05)**3` and pins 0.9716998 with a comment saying why.

## `result_cf()` starts at `t = 0`, not `t = 1`

The notes' cash flow ledger indexes the single premium and the acquisition expense at
`t = 0`, and `inv_amt_pp(0)`, `rop_pp(0)` and `pols_if(0)` are the initial branches of the
recursions. So `result_cf()` runs `t = 0 … proj_len()` and `net_cf(0) = +93,800` on the
anchor cell. This matches `MYGA_US_S` and differs from `Term_US_A`, which
starts at 1 because its premium falls at the beginning of policy year 1.

## There is no `commissions` cells

The notes' cash flow ledger has one acquisition line — `0.06 × premium + 200` **[std]** —
and no separate commission. Distribution cost sits inside that 6%, which is a plausible
RILA commission level, but the notes call it an acquisition expense and this model does not
invent a line item the specification does not carry. `expenses(t)` holds both the
acquisition charge at `t = 0` and the inflating $60-a-year maintenance expense.
`premium_taxes(t)` **is** present, because the notes do quantify premium tax — at 0%
[S2] — and the parameter is exposed rather than removed.

## `pols_maturity` and the Maturity Date

Unlike the deferred annuity chassis, whose horizon the notes leave open, this product's
horizon is contractual: at the Maturity Date the contract force-annuitizes at the Account
Value [S2]. `pols_maturity(t)` is zero in every month but the last and carries the
survivors out, so that

```
pols_if(t) − pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

closes for every `t`, including the last — `pols_if(t)` opens month `t` and `pols_if(t+1)`
opens the next, which at the Maturity Date is zero. Without it the block would appear to lose
lives with no cause. The name follows `BasicTerm_S.pols_maturity` and the construction
follows `Term_US_A`. The payout stream bought at that date is **not** derived here: it is
the immediate-annuity chassis, restricted to the two forms this contract offers, and with
no refund forms at all [S2].

## The 80 / 15 / 5 roll split is a split of value

The notes' term-end roll behaviour — 80% renew into the same option, 5% into a different
index-linked option (modelled as renewal at the same parameters) and 15% transfer to the
Fixed Account — is stated as a split of *contracts*, applied after the `phi` surrender. On
a probability-weighted single-contract model point it is equivalently a split of **value**
between the buckets, which is how `roll_share` implements it: the option keeps 85% of the
credited Investment Amount and the Fixed Account receives 15%, per contract, independently
of the surrender fraction. `inv_amt_pp_at(t, "BEF_ROLL")` is the credited amount before the
split — that is the column the worked example prints — and `"BEF_WD"` is after it.

The Holding Account is carried with a zero share: it receives maturing amounts only when
the option **and** the Fixed Account are both unavailable [S2], which never happens on the
base run, but `AV = Σ V_k + FA + HA` is then complete rather than approximate.

## What is not implemented

Named here so the gaps cannot be mistaken for oversights; the model docstring carries the
same list.

- **Performance Lock.** The notes give the election rule (`V/IA ≥ 1 + θ`, θ = 0.15, once
  per term) and the dollar-for-dollar withdrawal consequence, but **not the rate at which a
  locked bucket accrues to term end**. The module is incomplete in the specification, so it
  is left out rather than guessed.
- **Tiered participation rate.** The notes give its replicating portfolio but no crediting
  formula `g`.
- **Dual-direction and absolute-return segments, Annual Lock segments, rainbow segments,
  Secure Lock+, optional GMDB riders and living-benefit riders.** Listed out of scope by the
  product spec, with no formula.
- **RMD-driven withdrawals.** Named as a behavioural input; no amount formula.
- **Multi-option contracts.** The notes define a model point as one contract holding one
  option, with the multi-option case a vector sharing one contract-level decrement and
  guarantee base. This model carries the single-option case; the pro-rata-to-interim-value
  allocation rule is implemented over the option, the Fixed Account and the Holding Account
  rather than over several options.
- **The payout phase.** The Maturity Date benefit is emitted as an outgo at the Account
  Value; converting it to a payment stream is the immediate-annuity chassis.
- **A volatility surface.** The notes call the flat-surface approximation the largest single
  simplification in the model, and this implementation makes it. Supplying a surface is a
  change to `market_scenario.csv` plus a strike-and-maturity lookup, not to any formula.
- **Stochastic scenarios.** The index path, the CMT curve, the volatility and the dividend
  yield are read from a deterministic scenario table. The Academy's regression grid [R6] and
  the Lincoln and Prudential interim-value grids would be run by supplying more scenarios.
- **The contractual minimum-account-value rule.** A request that would leave less than
  $2,000 is treated as a full withdrawal [S1] [S2]; `wd_pp` merely caps the request at the
  Account Value **[std]**.
- **`check_margin()`.** On this chassis the cap *is* the fee — no charge is deducted from
  index-linked value, and the margin appears as the spread between the earned rate and the
  option budget implied by the declared cap. There is no charge-versus-cost decomposition to
  check. `check_av_roll_fwd()` and `check_pols_roll_fwd()` are implemented and both close to
  floating point, as does `check_term_end_identity()`; each takes no argument and returns a
  bool over every projected month, with `check_av_roll_fwd_resid(t)`,
  `check_pols_roll_fwd_resid(t)` and `check_term_end_identity_resid(t)` giving the signed
  residual when one fails.

## Standardizations used

Everything in this list is **[std]**: the monthly grid and the within-month processing
order; the decrement order death → surrender → term-end concentration; the declared Cap /
Step / Edge rates of 100% / 8% / 6% and the 3.00% Fixed Account rate (**no current rate
sheet was retrievable**); the whole market-data block — 4.00% risk-free, 2.00% dividend
yield, 20.00% flat implied volatility, a flat 4.00% Market Value Rate rising 100 bp at the
term midpoint; the 0.10% trading cost factor and its assessment on the sum of **absolute**
leg values; both free parameters of interim-value family (b) — the investment-grade
discount spread `iv_credit_spread` at 1.00%, which no source quantifies ([S4] says only
that the rate is above swap rates), and the Cap Calculation Factor's expense rate
`iv_expense_rate` at 0.10% of notional, which [S4] gives only as a dollar illustration;
the choice of interim-value family (a) and straight-line amortization; the
1.7834% / 2.22% NGE spread and the cap-solve target; the 80/15/5 roll split; the base
surrender shape 2% / 2% / 6%, the 3.0 charge-expiry shock multiplier, the `M_iv` moneyness
suppression, the 50% annual surrender cap and the 10% / 3% term-end concentration `phi`;
the 2% behavioural withdrawal rule; the 100% mortality A/E and the illustrative mortality
table; the 6% + $200 acquisition expense, the $60-a-year maintenance expense inflating at
2.5%, and the 0% premium tax; the ANB reading of the Maturity Date rule; and the extension
of the pro-rata-to-interim-value withdrawal allocation to the general-account buckets.

The **[std]** 100% mortality A/E deserves a specific warning, because the notes give one:
it is a placeholder, not a measurement. The payout chassis calibrates the same experience
study to 108.4% of 2012 IAM Basic, but that factor is payout-annuitant-select and is
deliberately **not** imported here; public deferred-period annuitant mortality is thin
[REG-R65] [unverified]. And do not run best-estimate mortality off the 2012 IAM *Period*
table: it carries the valuation margin built in at construction [REG-R60].

## Tests

`tests/test_registered_index_linked_annuity_us.py` asserts every cell of the notes'
six-row, thirteen-column worked example table, on both scenarios and on both sides of the
$8,000 withdrawal; the trace beneath it (`beta = 10.0632%`, the $10,063.19 budget, the
$89,936.81 opening fixed leg, the 1.7834% accretion yield and 2.22% implied spread, the
$5,031.60 midterm amortization, the $2,687.62 cost of the rate rise, the $119,171.01 and
$87,490.73 counterfactuals, the 9.4336% withdrawal ratio and the $1,433.62 excess of
notional lost over cash received); AG 54's term-start boundary `F + D = 100,000.00`
exactly; and the term-end identity `V = IA(1 + g)` for Cap, Step, Edge, Floor,
participation-rate and uncapped designs alike.

The notes' **second** labelled verification, the [S2] withdrawal-charge example, is
asserted on model point 15 end to end: `$80,000` Account Value at month 60, `$8,000` free,
`$72,000` chargeable, `wc(5) = 3%`, a `$2,160` charge and a `$77,840` cash surrender
value, every figure read out of the model's own cells.

Beyond the goldens there is one test per entry in the notes' "Known modeling pitfalls"
list — price return versus total return, the cap applying to the whole-term return,
homogeneity, the term-end identity, the discount-rate reference, the amortization
convention, the un-floored interim value, the un-smoothed Step and Edge discontinuities,
era mixing (the pre-AG 54 engine reproducing its own $52,500 worked example), and the
trading cost as a free parameter on a stated base — plus both roll-forwards at every month,
the result-table shapes, the two death benefit bands, the withdrawal-charge schedule and
its non-gross-up, the Transfer Period, the roll split, and the fact that every model point
projects.

Two tests pin the start-of-period in-force convention rather than the arithmetic:
`pols_if(1) == pols_if_init()` with `pols_if_at(t, "AFT_DECR") == pols_if(t+1)`, and the
reconciliation the convention buys — `premiums(t) / premium_pp()`,
`withdrawals(t) / wd_payment_pp(t)` and `expenses(t)` over the per-contract maintenance
charge all returning the `pols_if` column of the row they sit on.

Three tests guard the documentation rather than the arithmetic, because on this product
the documentation is half the deliverable: that the two readings of the contract year land
where they should (twelve months at each attained age, the expense step after the
anniversary, the charge schedule still on `duration(t)`); that every timing literal the
`Projection` docstring prints is one the cells actually accepts, and that its symbol table
names only cells that exist and covers every notes symbol the model implements; and that
the two invented family (b) parameters are marked **[std]** in the cells docstring, the
model docstring and this README's list above.

```bash
python -m pytest tests/test_registered_index_linked_annuity_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_registered_index_linked_annuity_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_registered_index_linked_annuity_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-registered_index_linked_annuity-r2
[R6]: #uslib-registered_index_linked_annuity-r6
[REG-R42]: #uslib-reg-r42
[REG-R44]: #uslib-reg-r44
[REG-R59]: #uslib-reg-r59
[REG-R60]: #uslib-reg-r60
[REG-R64]: #uslib-reg-r64
[REG-R65]: #uslib-reg-r65
[S1]: #uslib-registered_index_linked_annuity-s1
[S2]: #uslib-registered_index_linked_annuity-s2
[S4]: #uslib-registered_index_linked_annuity-s4
[S5]: #uslib-registered_index_linked_annuity-s5
[S6]: #uslib-registered_index_linked_annuity-s6
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
