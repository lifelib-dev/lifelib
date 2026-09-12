# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/fixed_indexed_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the 0% index credit floor, the surrender charge and bonus vesting
> schedules, the `b/(1+b)` clawback, the ratio-form MVA, the 5.00%/2.00% guaranteed rollup,
> the 150% stacking factor, the 0.95% rider charge on the benefit base, the payout
> percentage bands and the Model #805 floor — are sourced from the composite specimen.
> Every behavioural and expense assumption is a **[std]** standardization introduced for
> the reference implementation, because the tables that would calibrate them sit behind
> paid subscriptions. Replace them with company data before drawing any conclusion from
> the numbers.

## Run it

```bash
python products/fixed_indexed_annuity/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/fixed_indexed_annuity/FIA_US_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by the 0-based **month** `t` with one column
per cash flow line, and `result_cf_annual()` sums it into contract years; `result_pols()`,
`result_av()` and `result_glwb()` carry the in-force movements, the account-value and surrender
trace, and the rider state.

Its columns are `pols_if`, `premiums`, `withdrawals`, `wd_guar`, `wd_excess`,
`income_payments`, `claims_death`, `claims_lapse`, `claims_maturity`, `commissions`,
`expenses`, `premium_taxes` and `net_cf`, with `net_cf` income-positive as everywhere in
this library. `withdrawals` is the library-wide total for partial withdrawal payments and
the three columns after it partition it into the notes' own ledger categories — they are
published **alongside** the total rather than instead of it, so summing every column of
the frame double-counts the withdrawal.

The model and both its Spaces carry docstrings — `model.doc` describes the product and the
projection basis, `model.Projection.doc` holds the full mapping between the technical
notes' symbols and the cells names, and `model.Data.doc` the input arrangement.

## Monthly grid, annual contract

`t` is the **month index and it is 0-based**: `duration(t) = t // 12` is the completed
contract years at the start of month `t`, `policy_year(t) = duration(t) + 1` is the
contractual label, and the frame is `t = entry_mth() … proj_len() − 1` with
`proj_len() = 12 × policy_term()`. So `len(result_cf()) == proj_len() − entry_mth()` — 624
rows for the anchor, which enters after seven completed years and runs to attained age 120 —
and `len(result_cf_annual()) == 52`, the contract years those months make up.

**A monthly grid is not a monthly product.** Every *contractual* mechanic here is annual, and
the model keeps all of them on the anniversary:

> **Projection frequency [std]: monthly**, on contract months — with the contract anniversary
> still the single event date. Every *contractual* mechanic of the composite is annual — annual
> point-to-point crediting, the rider charge at the end of each contract year, the benefit base
> update, and the lifetime withdrawal — and the model keeps all of them on the anniversary.

All eight of the notes' processing steps therefore land in the **anniversary month**,
`is_anniv(t)`, the last month of each contract year, `t = 12k + 11`; eleven rows in twelve
carry no contractual cash at all. What the finer grid resolves is everything that is *not* a
contractual event: mortality and surrender in the month they happen, the fixed account
accruing at `(1 + i_F)^(1/12) − 1` and the Model #805 floor at `(1 + i_nf)^(1/12)` so a
mid-year death or surrender is valued on the balance it actually has, and maintenance expense
falling where it is incurred. The variants the notes exclude stay excluded — monthly-sum
crediting, a monthly charge deduction, daily interim values and mid-year withdrawal crediting
— and the indexed account is deliberately **flat between anniversaries**, which is the sourced
rule "withdrawals are not credited with index interest in the year they are taken" carried to
mid-year exits.

Because the monthly decrement rates compound to the annual ones and every contractual step is
unmoved, **every anniversary value is what the annual step produced**: account value, benefit
base, rollup base, lifetime withdrawal, Model #805 floor, phase, and `pols_if` at `t = 12k`.
The cash differs, which is the point.

One contractual quantity is now *more* faithful to the notes than the annual grid could be.
The notes state the MVA's remaining term `n` in **months**, so `mva_term(t)` is
`surr_charge_period − (t + 1)/12`: at the worked example's anniversary 8, month `t = 95`, that
is the 24 months the source quotes, and a surrender six months earlier carries the 30 months it
actually has instead of being rounded to the anniversary.

Three vocabulary cells carry the split and the whole model is written in terms of them:
`duration(t)` for anything keyed by contract year, `is_anniv(t)` for anything that happens
once a year, and `year_open_mth(t)` for the month whose closing value opens the contract year
— because the previous *month* is not the previous *year*, and reaching for `t − 1` where a
year is meant is the mistake this vocabulary exists to prevent.

**There is no issue-instant row:** the single premium, the premium bonus and the acquisition
expense are beginning-of-month flows of month 0 on a new issue, sitting on the same row as
that month's own decrements.

`age(t) = age_at_entry() + duration(t)` is the attained age **opening the contract year** of
month `t`, exactly as in `Term_US_S` and the chassis — so `mort_rate(t)` reads `age(t)` itself
and returns that year's annual rate, which `mort_rate_mth(t)` converts for the month. Age
changes on the anniversary, not on the birthday and not monthly. The transactions of the
contract year fall at its closing anniversary and are one year older, and that age is
`exercise_age(t) = covered_age(t) + 1`: it is what reads the lifetime-withdrawal percentage
table and what clears the contractual minimum exercise age of 50. The anchor's first
withdrawal is in contract year 8, month `t = 95`, at `exercise_age(95) = 70`.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `FIA_US_S/` holds nothing but formulas:

```
products/fixed_indexed_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  surr_charge_table.csv
  rollup_table.csv
  payout_rate_table.csv
  rate_scenario.csv
  withdrawal_table.csv
  run.py
  README.md
  FIA_US_S/       <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for every
contract. They live instead in an unparameterized **`Data`** Space, which `Projection`
references as `data` — so each file is read once per model no matter how many contracts are
projected, and `Projection[1].data is Projection[2].data`.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is read,
so it works wherever the repository is checked out. Each table has a filename Reference and
a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |
| `rollup_file` | `rollup_table()` | `rollup_table.csv` |
| `payout_rate_file` | `payout_rate_table()` | `payout_rate_table.csv` |
| `rate_scenario_file` | `rate_scenario()` | `rate_scenario.csv` |
| `withdrawal_file` | `withdrawal_table()` | `withdrawal_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `FIA_US_S/`
without the CSVs and it will read fine, then fail on first evaluation. What you gain is that
a diff of the model shows logic changes only, and an input can be edited or swapped in place
— point `Data.mort_table_file` at another same-schema file and the projection follows, with
no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Nine contracts on the anchor configuration M62 / NQ / $100,000 / GLWB at issue. **Point 1 is the worked-example anchor**, entered in force at anniversary 7 | anchor cell **[std]**; contract parameters [S2] [S5] [S9] [S10] |
| `mort_table.csv` | Annual mortality by attained age and sex, ages 40–120 | **[std]** illustrative Makeham annuitant curve, *not* a published table; shared with `products/fixed_deferred_annuity` so the two annuity models sit on one basis |
| `surr_charge_table.csv` | The surrender charge percentage 9.1% → 0% and the bonus vesting percentage 0% → 100%, both by contract year | sourced [S5] |
| `rollup_table.csv` | Three guaranteed simple rollup schedules: blended 5.00%/2.00%/0%, a flat 3.00%, and none | sourced [S2] / [S9]; the `none` row is the pure-stacking configuration **[std]** |
| `payout_rate_table.csv` | Lifetime withdrawal percentages by attained-age band, single and joint | sourced [S3]; the 80+ band extends [S3]'s single "80" row **[std]**, supported by [S4] |
| `rate_scenario.csv` | Two scenarios of index level and MVA reference yield, keyed by **anniversary**. `worked` is the notes' own path — flat at 5,000 to anniversary 7, 5,450 at anniversary 8, flat after, so index credits are zero from anniversary 9 exactly as the notes assume | worked example; the `growth` path **[std]** |
| `withdrawal_table.csv` | Ad hoc gross withdrawals by schedule and **elapsed contract year** | **[std]** variants |

### What each time-like column is keyed by

Two files carry a column literally called `t`, and they do not mean the same thing:

| File | Column | Decision | Why |
|---|---|---|---|
| `rate_scenario.csv` | `t` | **anniversary number** | It keys a *time point*, and **not the frame's month index**: row `y` is the index level and MVA reference yield **at anniversary `y`**, `y = 0` at issue. Anniversary `y` opens contract year `y + 1`, so the values are already 0-based and are read at `duration(t)`. `index_return(t) = I(y+1)/I(y) − 1` differences the opening and closing levels of month `t`'s contract year, and `mva_rate(t)` reads `mva_ref_yield(duration(t) + 1)` at the transaction date. The `worked` rows at 0 and 8 produce `R = 9.00%` and `iₜ = 3.50%` for the golden month `t = 95` |
| `withdrawal_table.csv` | `t` | **elapsed contract years** | Also not the frame's month index: a row keyed `y` is the ad hoc withdrawal taken at the anniversary closing contract year `y + 1`, read at `duration(t)`. The `preexercise` schedule's $60,000 sits at `t = 2`, the withdrawal at the anniversary closing contract year 3 — month 35 on this grid. The `none` placeholder stays at `t = 0` |
| `surr_charge_table.csv` | `contract_year` | **unchanged** | A contractual 1-based label; the model maps through `policy_year(t) = duration(t) + 1` |
| `rollup_table.csv` | `contract_year` | **unchanged** | Same, and read as a step function of `policy_year(t)` |
| `model_point_table.csv` | `entry_year` | **unchanged** | An elapsed count — seven *completed* contract years — which the model turns into its first projected month, `entry_mth() = 12 × entry_year()` |
| `mort_table.csv`, `payout_rate_table.csv` | `age`, `age_lo`/`age_hi` | **unchanged** | Attained ages, not time indices |

**No shipped CSV changed when the grid did**, which is the useful consequence of never keying
an input by the frame's own index: both `t` columns count anniversaries or contract years, and
both were already 0-based. The `provenance` strings are left as they were, so three of them
quote a `(t)` that is now a contract-year rather than a month: `rate_scenario.csv`'s
"`R(8) = 5,450/5,000 − 1 = 9.00%`" is the model's `index_return(95)` (the file's own key
`t = 8` is an anniversary, correctly unshifted); and `model_point_table.csv`'s "`AV(0) =
107,000` against `BB(0) = 100,000`" (point 2) and "`BB(7) = 121,000`" (point 3) name *opening*
states of contract years 1 and 8 — the values the tests assert as `av_pp_year_open(11)`,
`benefit_base_pp_at(11, "BEF_ROLLUP")` and `benefit_base_pp_at(95, "BEF_ROLLUP")`. The figures
are unchanged and still correct; only the symbols are in the old notation.

Mortality is the one table worth a second look. The notes prescribe the 2012 IAM Basic /
2012 IAR generational family with Projection Scale G2, `q_x^(2012+n) = q_x^(2012) ×
(1 − G2_x)^n`, with rounding applied from the 2012 period rate each time and never by
compounding an already-rounded rate. That table may not be redistributed here, so the
shipped curve is illustrative and **generational projection is not implemented**. Swap the
real basis in by repointing `Data.mort_table_file`.

## Naming

Cells follow [`MYGA_US_S`](../fixed_deferred_annuity/model.md) — the deferred
annuity chassis this product sits on — and through it lifelib's `basiclife/BasicTerm_S` and
`savings/CashValue_SE`: `pols_*` for policy counts, `av_*` for account values, plural nouns
for cash flows, `*_rate` for rates, `*_pp` for per-contract amounts, `*_at(t, timing)` for a
quantity read at a point inside the anniversary. The technical notes use compact actuarial
symbols instead; the full mapping lives in the `Projection` Space docstring.

Six cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l(t)` | `pols_if(t)` | The library's start-of-period count; at `t = 12k` it is exactly the notes' `l(k)`, the probability in force at anniversary `k`. See below |
| `MGV(t)` | `mgsv_pp` | The chassis calls the same Model #805 floor `MGSV`. Both source files say in terms it is **one quantity under two labels**; the chassis name wins so the two annuity models share it. See below — the *recursion* is not shared |
| `E(t)` | `wd_excess_pp` | On the chassis `E(t)` is the charge base. Here it is the **excess withdrawal**, the part above the guaranteed amount. See below |
| `X(t)` | `wd_charge_base_pp` / `surr_charge_base_pp` | The chassis's `wd_excess_pp` / `surr_excess_pp`, renamed because `wd_excess_pp` is taken |
| `x + t` | `age(t)` | `age_at_entry() + duration(t)`, the age opening month `t`'s contract year, as in `Term_US_S` and the chassis; `exercise_age(t) = age(t) + 1` is the age at the closing anniversary, where the withdrawal falls |
| `M_shock(t)` | *(absorbed)* | The notes state the shock as three absolute rates, not as a multiplier; see below |
| `d`, `c` | `trigger_rate`, `cap_rate` | `d` is deaths in `Term_US_S` and the floor's withdrawal deduction on the chassis; `c` is the floor's contract charge there |

Three shared names are spelled the library's way rather than the notes': the
free-allowance portion of a withdrawal is `wd_free_pp`, the chassis name; the mortality
A/E deviation factor is `mort_ae_factor`; and the roll-forward self-checks are the
no-argument booleans `check_av_roll_fwd()` and `check_pols_roll_fwd()`, with the signed
per-month residual behind each kept as `check_av_roll_fwd_resid(t)` and
`check_pols_roll_fwd_resid(t)` for when one of them fails.

One name is reused deliberately: `credit_rate(t)` is the chassis's declared effective annual
rate `i_cr(t)` and here the index credit rate `cr(t) = max(f, min(c, R(t)))`. Different
formulas, same concept — the rate at which interest is credited for the contract year — so the
name is kept rather than split.

## `pols_if(t)` opens month `t`, and at `t = 12k` it *is* the notes' `l(k)`

The technical notes define `l(k)` as the in-force probability at the **end** of contract
year `k`. Across this library `pols_if(t)` is the number in force at the **start** of `t` —
`Term_US_S` has `pols_if(0) == pols_if_init()`, and lifelib's `savings/CashValue_SE` has
`pols_if(t)` equal to `pols_if_at(t, "BEF_MAT")`. The end of contract year `k` and the start
of month `12k` are the same instant, anniversary `k`, so the two coincide there and — because
the monthly decrement rates compound to the annual ones — the equality is exact, not
approximate:

| | Cells | Notes symbol |
|---|---|---|
| in force opening contract year `k + 1` | `pols_if(12k)` | `l(k)` |
| in force opening month `t` | `pols_if(t)` | — |
| in force leaving month `t` | `pols_if_at(t, "AFT_DECR")`, equivalently `pols_if(t + 1)` | — |

The reason this matters is not tidiness. Every cash flow of month `t` — the guaranteed
withdrawal, the excess, the post-depletion income, the maintenance expense — is weighted by
the count *entering* it, so with `pols_if` carrying the closing count the `pols_if`
column of `result_cf()` would not reconcile with the cash flows printed beside it. It does:
divide any cash flow on a row by its per-contract amount and the `pols_if` figure on that
same row comes back, which a test asserts on every model point.

**The finer grid changes one answer here rather than its resolution.** A withdrawal falls in
the anniversary month `12k + 11` and is therefore weighted by `pols_if(12k + 11)`, the
contracts that actually reach the anniversary — where the annual step could only weight it by
`l(k)`, the contracts that entered the year, and so paid a full year of guaranteed income to a
contract that died in month three. `result_cf_annual()` prints `l(k)` in its `pols_if` column
and the year's cash beside it, so the two conventions sit on the same row and the difference
is visible rather than buried.

The roll-forward identity reads
`pols_if(t) − pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)`, and
`result_pols()` prints `pols_if` as the first column and `pols_if_aft_decr` as the last, so
each row opens and closes on the page.

## `MGV` is `MGSV`, but the recursion is not the chassis's

Both `products/fixed_indexed_annuity/product-spec.md` and the chassis notes say the same
thing from opposite directions: the Model #805 floor is called **`MGV`** here after [S10]
and **`MGSV`** on the chassis after its own specimen, and it must not be modeled as two
quantities. The model therefore uses `mgsv_pp` throughout, and a test asserts the
`Projection` docstring explains the bridge.

**The arithmetic is genuinely different, and that is deliberate.** This product accretes and
*then* deducts; the chassis deducts and *then* accretes:

```
FIA      MGV(t)  = max(0, MGV(t−1) × (1 + i_nf)^(1/12) − G(t))
chassis  MGSV(t) = [MGSV(t−1) − d(t) − c(t)] × (1 + i_nf)^(1/12)
```

Both now step monthly, and they still differ: the FIA accretes and *then* deducts, the chassis
deducts and *then* accretes. `G(t)` is zero away from an anniversary, so over a contract year
the FIA form collapses to `max(0, MGV⁽⁰⁾ × (1 + i_nf) − G)` — the annual arithmetic the worked
example pins to the cent, `93,811.84 × 1.01 − 10,144.16 = 84,605.80`. What the monthly accrual
buys is a floor that means something at a mid-year death or surrender, which is where it most
often binds. The chassis notes explicitly warn against carrying their recursions across
unexamined. Same name, same concept, different arithmetic, on purpose.

## `wd_excess_pp` means something different here than on the chassis

On the chassis `E(t)` is the amount exposed to the surrender charge and the MVA, and is
named `wd_excess_pp` / `surr_excess_pp`. In these notes `E(t)` is the **excess withdrawal**
— the part of a gross withdrawal above the guaranteed lifetime amount. That is not a naming
nicety: it is the quantity that permanently reduces the guarantee pro rata and, if it
exhausts the account value, destroys the income stream entirely. It is the product's
headline concept and it keeps the name `wd_excess_pp`.

The chargeable amount, the notes' `X(t)`, is `wd_charge_base_pp` on the withdrawal path and
`surr_charge_base_pp` on the surrender path. Reading a chassis formula across without
renaming would silently charge a surrender charge on the wrong base — on the whole
guaranteed withdrawal rather than on the excess above the free amount — which is exactly
the error [S9] warns about when it says withdrawals up to the annual benefit amount carry no
charge "even if greater than the Free Withdrawal Amount".

## The worked example is an in-force cell, not a new issue

The notes' worked example opens contract year 8 at anniversary 7 on stated balances —
`AV⁽⁰⁾ = 128,000.00`, `BB⁽⁰⁾ = 180,000.00`, `RB⁽⁰⁾ = 100,000.00`, `MGV⁽⁰⁾ = 93,811.84` —
described as
"illustrative balances, broadly consistent with a seven-year deferral at these parameters
**[std]**". They are *not* derived from a projection, and no index path reproduces all four
simultaneously; contriving one would be retuning assumptions to force a match.

So model point 1 carries `entry_year = 7` — seven *completed* contract years, an elapsed count
the model turns into its first projected month, `entry_mth() = 84` — and those balances become
that contract year's opening timing: `av_pp_year_open(95)` (equivalently
`av_pp_at(84, "BEF_INV")`), `benefit_base_pp_at(95, "BEF_ROLLUP")`, `rollup_base_pp_init()`,
`mgsv_pp_init()`, `phase_init()`. `result_cf()` is indexed from `entry_mth()`, and an in-force
model point pays no premium and incurs no acquisition expense — both are behind it. Model
point 2 is the same cell issued at `t = 0`, which exercises the notes' Initialisation block
instead as the opening state of its first month: `AV⁽⁰⁾ = P × (1 + b) = 107,000`,
`BB⁽⁰⁾ = RB⁽⁰⁾ = P = 100,000` with the bonus excluded, `MGV⁽⁰⁾ = 0.875 × P = 87,500` with the
bonus excluded again. Rolling point 2's floor forward seven years reproduces the worked
example's `93,811.84` exactly — as `mgsv_pp(83)`, the value closing contract year 7 and opening
contract year 8, reached by eighty-four monthly accruals of `(1 + i_nf)^(1/12)` rather than
seven annual ones. That is the one place the two model points meet, and a test asserts it.

## The MVA collar on a partial withdrawal is shipped both ways

The notes limit the adjustment to `|MVA| ≤ max(0, G(t) − SC(t) − CB(t) − MGV(t))`, and
justify it as ensuring that "a negative MVA combined with charges never reduces **the
surrender value** below the guaranteed minimum value". Those two halves do not sit together
on a partial withdrawal: the limit is written on the *gross withdrawal* while its stated
purpose is a *surrender-value* test, and the worked example only ever exercises it at a full
surrender, where `G(t) = AV(t)` and the distinction vanishes.

Read literally, a partial withdrawal smaller than the nonforfeiture floor produces a
non-positive limit and therefore **no adjustment at all** — a $20,000 withdrawal against an
$84,605.80 floor gets an MVA of exactly zero. Read as a test on the contract, it gets the
adjustment its rate produces up to what the remaining floor allows.

Neither reading can be preferred on the evidence, so both ship behind `mva_collar_basis`:

| Value | Limit measured against | Effect |
|---|---|---|
| `"gross"` **[std] default** | `G(t)`, the notes' literal text | a small partial withdrawal carries no MVA |
| `"surrender_value"` | `AV(t)`, the notes' stated purpose | a small partial withdrawal carries its MVA |

**They agree on the surrender path**, so the worked example reproduces under either, and a
test pins the gap open rather than closing it in either direction. Model point 8's $60,000
withdrawal is deliberately large enough that the literal collar does not bind it to zero, so
the withdrawal-path MVA is live in the shipped default run.

## The net proceeds line is a cent-rounding artefact, and both readings are asserted

The surrender trace's components all reproduce exactly to the cent — `SC = 3,606.30`,
`CB = 2,359.26`, `MVA = −1,158.64`, limit `= 32,294.48` — but the notes' net proceeds of
`115,741.64` is the sum of those *displayed* figures. The clawback (2,359.26168) and the MVA
(−1,158.64384) each carry fractions of a cent, so carrying full precision — which the notes'
own convention asks for, "full precision internally, cents on reported cash flows **[std]**"
— gives `115,741.6345`, 0.55 cents lower. The model keeps full precision and the test pins
both figures rather than tuning either away.

## `M_shock` is absorbed into `lapse_rate_base`

The notes write `w(t) = min(0.35, w_base(t) × M_shock(t) × M_money(t))` but state the shock
as three *absolute* rates rather than as multipliers on the 6% ultimate:

```
w_shock = 0.33   no GLWB rider
w_shock = 0.10   GLWB in force but not activated
w_shock = 0.05   GLWB activated (phase = INCOME)
```

Carrying `M_shock` as a separate factor would require inventing a denominator, so
`lapse_rate_base(t)` returns `shock_lapse_rate(t)` in the year the surrender charge expires
and `lapse_rate(t)` multiplies only by `lapse_moneyness_factor(t)`. The name
`shock_lapse_rate` follows `Term_US_S`. Model points 1, 9 and 6 exercise the three rates
respectively, and the notes call this "the single most important behavioral fact in the
product".

**The timing does not follow `Term_US_S`, and the contrast is the point.** There the notes put
the shock "in full at the end of the final level-period month" — a contractual date, the month
before the first ART premium falls due — so the whole shock lands in that one month. Here the
notes state it as the surrender rate *of contract year 11*, a year that carries no surrender
charge in any of its months, so there is no date inside it for the decision to cluster on and
`lapse_rate_mth` spreads it like any other annual rate: twelve months of
`1 − (1 − 0.33)^(1/12)` compound back to exactly 33%. `lapse_moneyness_factor` is read on the
state *closing* the contract year for the same reason — one factor for the year, rather than a
number that drifts with the fixed-account accrual inside it.

## The four phases, and why the *cause* of depletion matters

`ACCUM` is deferral. `INCOME` starts at the first lifetime withdrawal. `DEPLETED` is what
the product is sold for: the account value is gone, the insurer pays `LW` from its own funds
for the rest of the covered life, no rider charge is deducted, no index credit is computed,
the surrender value and death benefit are zero, and **lapse is impossible**.

`TERMINATED` is the same exhaustion with the guarantee destroyed — reached when the account
value is driven to zero by an excess withdrawal, a surrender charge or a negative MVA rather
than by guaranteed withdrawals and rider charges. `depletion_cause(t)` carries the
attribution and is evaluated *before* the depletion test, exactly as the notes require. A
model testing only `AV ≤ 0` would either give the guarantee away after an excess withdrawal
or destroy it after a legitimate one. Model points 1 and 7 are the same cell withdrawing
100% and 105% of the maximum; they reach exhaustion in the same year and end in opposite
states.

### The attribution has to reach the cash, not just the phase label

At the anniversary of exhaustion — contract year 19, month `t = 227` — the withdrawal
requested is larger than the balance left to meet it, and the two branches fund that gap
differently:

| | point 1, `DEPLETED` at `t = 227` | point 7, `TERMINATED` at `t = 227` |
|---|---|---|
| account value after the rider charge | 1,038.38 | 765.92 |
| withdrawal requested `G(227)` | 10,144.16 | 7,856.61 |
| shortfall `av_depletion_pp(227)` | 9,105.78 | 7,090.69 |
| of which unpayable `wd_unfunded_pp(227)` | 0.00 | 7,090.69 |
| cash paid `wd_payment_pp(227)` | 10,144.16 | 765.92 |

On the left the insurer funds the whole shortfall from its own funds — that stream *is* the
product. On the right it funds none of it: the balance is gone and the rider that would have
covered the rest was destroyed by the very withdrawal being paid, [S5] treating the contract
"as well as the rider" as Surrendered at that point. Paying the request in full on both
branches would honour the guarantee in the year the excess withdrawal kills it, which is
precisely the failure the notes' attribution test exists to prevent — reached one step
further downstream than the phase label.

The cap is on the **payment**, not on the withdrawal. `wd_pp(t)` still carries the amount
requested, so the excess still sets `depletion_cause`, still drives `ρ` to 1 and still takes
the benefit base to zero; only `wd_payment_pp` and the three ledger lines are net of
`wd_unfunded_pp`. Within the payment the account value is consumed in the order the notes
compose the withdrawal — the first `LW` dollars are the guaranteed portion and the rest is
the excess [S9] — so the **excess goes unpaid first** and the guaranteed portion is eaten
into only after that **[std]**, the notes being silent on a withdrawal the account value
cannot fund. At `t = 227` — the anniversary closing contract year 19 — point 7 pays 765.92 of
guaranteed portion and none of the 374.12 excess.

One consequence had to be decided rather than read off: when the contract terminates, the
survivors leave as a **deemed full surrender** (`lapse_rate` returns 1.0 for that contract
year, paying `max(surrender value, MGV)` which is `MGV` once the account value is zero),
following the specimen wording "the contract as well as the rider will be considered
Surrendered" [S5]. Without it the block would sit in force forever holding a contract that
pays nothing, and the in-force roll-forward would not close. On the monthly grid this is the
one surrender rate that is **not** spread: it is a contractual event on a date, so
`lapse_rate_mth` puts the whole of it in the anniversary month and nothing in the eleven
before it. The behavioural shock at surrender-charge expiry is the opposite case and *is*
spread — see below.

An account value exhausted in `ACCUM` terminates rather than depletes **[std]**: the notes
define the depleted state only out of `INCOME`, and before exercise there is no `LW` to pay.

## The horizon

The notes state none, and the `DEPLETED` liability is a life annuity, so stopping early
would silently drop the tail the product exists for. `proj_len()` is the **number of projected
months**, `12 × policy_term()`, the exclusive end of the frame, so the last row is
`t = proj_len() − 1`: the final month of the contract year *entered* at attained age
`maturity_age` = 120, the terminal age of the shipped mortality table, where the annual rate
is 1.000000 — hence a monthly rate of 1.0 in the first month of that year, so the projection
closes itself rather than being truncated and `pols_maturity` is numerically zero. It is kept
anyway, because a substituted table with no terminal age would make it bite and because
without it the last month would appear to lose lives with no cause. The name follows
`BasicTerm_S.pols_maturity`.

## Standardizations used

Everything in this list is **[std]**: the anniversary-only event date, and with it the flat
indexed account between anniversaries — the sourced "no credit in the year of withdrawal"
rule [S1] extended to mid-year deaths and surrenders, the other three documented mid-segment
conventions being interim-value structures the notes exclude; the annual step-up (no retrieved document describes an automatic ratchet during deferral —
`step_up_mode = "at_exercise"` reduces the model to the documented designs); the 1.00% flat
nonforfeiture rate inside the 0.15%–3% corridor; the insurer-favourable reading under which
the guaranteed withdrawal consumes the free withdrawal amount; the pro-rata allocation of a
withdrawal across the fixed and indexed accounts, the notes giving a rule only for the
charge; the base surrender vector 2/3/4/5/6% and the three-way shock lapse 33%/10%/5%; the
rider moneyness multiplier; the locking of the payout percentage at first exercise; the
`ACCUM`-exhaustion-terminates rule; the deemed full surrender on termination; the excess
going unpaid before the guaranteed portion when the account value cannot fund the whole
withdrawal; the 6.0%-of-premium acquisition expense with no separate commission line; the
$80 per contract per year maintenance expense inflating at 2.5%; the 0% premium tax; the
illustrative mortality table with an A/E factor of 100%; and the attained age 120 horizon.

Two crediting parameters belong here rather than on the sourced list. The notes print the
index-margin and performance-trigger *forms* — `max(f, p × R − s)` [S8] [R1] and
`d × 1{R ≥ 0}` [R1] — but declare no level for either, in neither `technical-notes.md` nor
`product-spec.md`. So `spread_rate = 2.00%` **[std]** and `trigger_rate = 4.50%` **[std]**
are illustrative levels that exist only to exercise those branches, and must not be read as
parameters of the composite. The two crediting parameters that *are* sourced are the cap,
5.25% [S2], and the participation rate, 80% — the latter from [R1]'s worked
`min(80% × 10%, 6%) = 6%`, which a test asserts.

Switched **off** by default so the base run reproduces the worked example:
`index_cost_rate = 0` (the volatility-controlled-index haircut), `mgsv_annual_charge = 0`
(Model #805 permits $50), `rider_charge_from_mgsv = False` (one carrier deducts the rider
charge from the floor [S1] [S2]; another deducts its allocation charge there [S3] [S4]),
`use_guaranteed_scale = False` (the guaranteed minimum cap and fixed
rate), `rb_wd_convention = "pro_rata"` (the dollar-subtraction convention [S2] is the
alternative), and `comm_rate_acq = 0`.

## Not implemented

Named so the gaps cannot be mistaken for oversights: monthly-sum crediting (the grid is monthly
but the *index path* is not — `rate_scenario.csv` states index levels at anniversaries only, so
there are no monthly returns to sum, and its floor convention is itself flagged ambiguous);
interim values in either documented form [S10] [S11], both daily marks of the embedded option;
cap re-declaration against the option budget (the notes give the target but no
option-pricing function); stochastic GLWB activation on the `h(a)` table, which cannot be
applied to a single deterministic cell — `activation_rate()` reports it and the base run
activates at `income_start_age`; generational mortality with Scale G2; joint-life
survivorship (the notes give the joint *payout percentage* but no second-life mortality);
the income doubler, confinement and terminal illness waivers, and annuitization, all put out
of scope by the notes themselves; additional premium; and `check_margin()`, because the
notes define no margin decomposition and the model projects no asset side.

## Tests

`tests/test_fixed_indexed_annuity_us.py` asserts all sixteen rows of the notes' worked
example and every line of its surrender trace, the "Where the step-up binds" variant block,
the year-1 step-up on a new issue, the depletion arithmetic and the survival of the income
stream, the payment cap on the terminating exhaustion branch, the verbatim [S9]
excess-withdrawal reduction and the verbatim [S10] clawback, one test per pitfall the notes
state as a **model mechanic**, the crediting engine against [R1]'s worked case, the three
shock-lapse rates, the Model #805 §4B/§4C rate including the 15 bp floor, the in-force and
account-value roll-forwards — through the no-argument `check_pols_roll_fwd()` and
`check_av_roll_fwd()` and through the `check_*_resid(t)` residuals behind them — that the
`pols_if` column of `result_cf()` is the weight carried by the cash flows on its own row,
and that every model point projects. The worked example's golden values are pinned at month
`t = 95`, the anniversary that closes contract year 8, and its stated opening balances at that
contract year's opening timing; the frame assertions pin `t = entry_mth() … proj_len() − 1`,
the anchor's 624 monthly rows and the 52 rows of `result_cf_annual()`.

Nine tests are the monthly grid's own: that the monthly decrement rates compound back to the
annual ones and that the annual rates are properties of the contract year; that the fixed
account accrues at `(1 + i_F)^(1/12) − 1` and that twelve accruals are exactly
`fixed_interest_ann_pp`; that the Model #805 floor accretes monthly and deducts at the
anniversary, still reproducing `93,811.84 × 1.01 − 10,144.16`; that **no contractual cash moves
between anniversaries**, swept across every month of every model point; that the indexed
account is flat between them while the fixed account is not; that every annual state cells
steps once a year from the previous anniversary and carries its value in between; that the
shock lapse **is** spread over contract year 11 while the deemed full surrender at termination
is **not**; and that `result_cf_annual()` sums the months into contract years without losing a
dollar.

Three of the notes' thirteen "Known modeling pitfalls" entries carry no test, and cannot:
that the behavioural assumptions must not be reused in a CARVM valuation, that "efficient
policyholder selection" is not AG 33's language, and that the declared parameters are stale
and state-varying are statements about how the projection may be *used* rather than about
what it computes. A fourth, "Interim values and index costs", is half covered — the
interim-value structures it names are not implemented at all, while the index-cost haircut
it also names is, and
`test_pitfall_index_costs_are_deducted_before_the_cap_and_participation_rate` asserts that
`index_cost_rate` comes off `R(t)` ahead of both the cap and the participation rate. The
remaining nine each have their own test.

```bash
python -m pytest tests/test_fixed_indexed_annuity_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_fixed_indexed_annuity_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_fixed_indexed_annuity_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_indexed_annuity-r1
[std]: #uslib-std
<!-- END generated citation links -->
