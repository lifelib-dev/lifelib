# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/variable_ul/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md). Those notes build on the
universal-life chassis in
[`products/universal_life/technical-notes.md`](../universal_life/technical-notes.md),
and this model is the counterpart of [`UL_US_S`](../universal_life/model.md) on
the same chassis.

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the premium load ceiling, the $10.00 per-policy and $0.20 per
> $1,000 monthly charges, the M&E rate, the fixed-option floor, the loan rates, the GPT
> corridor factors at the quoted ages, the net amount at risk defined without a
> discount, the $83.34 COI cap, the age-121 rule — come from four registered
> prospectuses. Everything else is a **[std]** standardization: the current premium
> load, the two-subaccount lineup, the surrender charge scale, the corridor
> interpolation, the illustrative COI and mortality tables that stand in for the
> licensed 2017 CSO and 2015 VBT families, the lapse and persistency vectors, the
> expense placeholders, and — decisively for this product — **the separate-account
> return scenario**. Replace them with company data before drawing any conclusion from
> the numbers.

## Run it

```bash
python products/variable_ul/run.py          # the worked-example anchor, point 1
python products/variable_ul/run.py 4        # the in-force cell with a loan
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/variable_ul/VUL_US_S")
model.Projection[1].result_av()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
There are four result tables, all `DataFrame`s indexed by policy month `t`:

| Table | What it shows |
|---|---|
| `result_av()` | the per-policy account value roll-forward, in the worked example's own column order |
| `result_cf()` | the **gross (policyholder) view** liability cash flows — the primary projection |
| `result_net()` | the **net-of-account (general-account strain) view**, derived from the same run |
| `result_pols()` | the decrements |

and three self-checks: `check_av_roll_fwd()`, `check_margin()`, `check_net_view()`.

The model and both Spaces carry docstrings — `model.doc` describes the product and the
projection basis, and `model.Projection.doc` holds the full mapping between the
technical notes' symbols and the cells names.

## Monthly, on monthiversaries

Policy month `t` runs 1 … `proj_len()` = `12 × (121 − age_at_entry() + 1) −
duration_mth_init()`. For a new-business model point `t = 1` is the issue month; for an
in-force point it is the first projected month, sitting `duration_mth_init()` completed
months after issue. The contract has **no maturity date** — at attained age 121 premiums
and monthly deductions cease, the asset charges continue, and coverage runs to death or
surrender — so `pols_maturity(t)` is identically zero and the projection is truncated by
mortality, not by the policy.

Ending at attained age 121 rather than 120 is deliberate. It is the age at which the
regime switches, and the notes list *"missing the age-121 regime switch (charges stop;
asset drags continue)"* among the modeling pitfalls; running one policy year past 120
makes the switch live and testable.

Within each month the notes' order is: premium and load → withdrawal and its fee →
loan activity → death benefit and corridor → net amount at risk → monthly deduction,
allocated pro rata over the unloaned accounts → growth (separate-account unit-value
factor, fixed-option interest, loan interest, debt accrual) → end-of-month death benefit
and net amount at risk → decrements, **death before lapse**.

## Where this model leaves the universal-life chassis

`UL_US_S` is the same chassis, and this model follows it name for name. Where
the two differ, the difference is the variable-UL notes' own instruction — the chassis
file warns against carrying its recursions across unexamined, and each of these is a
place where doing so would be wrong. The table is the complete list of differences, and
the model docstring carries the same list in prose:

| | `UL_US_S` | `VUL_US_S` | Source of the difference |
|---|---|---|---|
| Net amount at risk | `DB / (1 + i_gm) − AV'`, one month discounted at the guaranteed rate | `max(0, DB − AV')`, **no discount** | The VUL prospectuses define NAAR as death benefit − account value [S2]. **Sourced.** |
| Investment return | one declared credited rate `i_cr` | per-subaccount `(1 + r)(1 − e_i/12)(1 − m/12)` on exogenous gross returns, plus a declared rate on the fixed option only | The account value is a separate-account vector |
| Charge base | per-unit charge on the **current** face, `units(t)` | $0.20 charge *and* surrender charge on **F₀**, `units()` — no `t` | "per $1,000 of F₀" [S2] |
| Surrender charge | amortized **monthly**, `max(0, 9.00 − t/12)` | steps by **policy year**, `18.00 × (15 − y)/14` | The worked example pins the step at 12/14 in policy year 3 |
| Maintenance expense | $75/year inflating at 2.5% | flat $75/year, `inflation_rate = 0.0` | The variable-UL notes give no inflation |
| Lapse shock | a whole shock **year** at surrender-charge expiry | a one-**month** spike, optional, magnitude an input | "spike multiplier on q^w in the month after SC_t reaches zero" |
| Total lapse cap | 35% **[std]** | none — the dynamic multiplier is already bounded at 2.0 | The variable-UL notes set no cap |
| GPT / 7-pay | tracked as compliance flags | not tracked | "not enforced in the baseline; premiums are assumed within limits" |

The last of the chassis's names that has no VUL analogue is `wd_free_pp`: the fixed-UL
specimen carves out a free withdrawal amount and cuts the face by the excess, where the
variable-UL notes cut the face **proportionately** with no free amount. `naar_factor` is
gone for the same reason — there is no discount to hold.

## Inputs are external files

The ten input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `VUL_US_S/` holds nothing but formulas:

```
products/variable_ul/
  model_point_table.csv        <- inputs live here
  subaccount_table.csv
  scenario_table.csv
  coi_rates.csv
  corridor_factors.csv
  mort_table.csv
  class_factor_table.csv
  lapse_table.csv
  prem_persistency.csv
  surr_charge_table.csv
  run.py
  README.md
  VUL_US_S/                <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the
model and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which
stores its inputs *inside* the model through modelx's IOSpec machinery — hence no
`_data/` directory and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every policy. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many policies are projected. `Data.input_dir()` resolves the location from
`_model.path.parent` when the model is read, so it works wherever the repository is
checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `subaccount_file` | `subaccount_table()` | `subaccount_table.csv` |
| `scenario_file` | `scenario_table()` | `scenario_table.csv` |
| `coi_rates_file` | `coi_rates()` | `coi_rates.csv` |
| `corridor_file` | `corridor_factors()` | `corridor_factors.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `class_factor_file` | `class_factor_table()` | `class_factor_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `prem_persistency_file` | `prem_persistency_table()` | `prem_persistency.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `VUL_US_S/` without
the CSVs and it will read fine, then fail on first evaluation. What you gain is that a
diff of the model shows logic changes only, and an input can be edited or swapped in
place — point `Data.mort_table_file` at another same-schema file and the projection
follows, with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Four points, all on the anchor configuration M45 / StdNT / $500,000. **Point 1 is the worked-example anchor cell** (Option A, 24 completed months, $30,000/$20,000 opening subaccounts, 60/40 allocation, no fixed balance, no debt, scenario `WE`); point 2 is identical with the two month-1 pins blank; point 3 is new business under Option B; point 4 is an in-force cell with a fixed-option balance and an $8,000 loan | anchor cell from the notes' worked example and model-point attribute table |
| `subaccount_table.csv` | Two subaccounts, equity 0.75% and bond 0.55% fund expense | **[std]** collapse of observed menus; ranges 0.29%–1.18% [S1], 0.55%–2.88% [S2], 0.46%–2.54% [S3], 0.08%–1.93% [S4] |
| `scenario_table.csv` | Monthly **gross** subaccount returns by `scenario_id`. `WE` is the worked example's month (+1.00% / −0.50%) then a level 6% a year path; `LEVEL6` is that path throughout | **[std]**; the worked example's month is the notes' own |
| `coi_rates.csv` | Guaranteed maximum monthly COI per $1,000 NAAR, M / StdNT / 45, policy years 1–77 | year 1 = $0.22 is the disclosed anchor [S4]; the rest is an **illustrative [std]** stand-in for the licensed 2017 CSO table, capped at $83.34 |
| `corridor_factors.csv` | GPT corridor factors, attained ages 18–121, grading to 100% at 95 | quoted ages and 100% from 95 sourced [S2] [R3]; ages 41–94 are **linear interpolation [std]** — see below |
| `mort_table.csv` | Best-estimate annual mortality by age, 18–121 | **illustrative [std]**, *not* the 2015 VBT the notes recommend — that family is licensed. Deliberately well below the COI basis |
| `class_factor_table.csv` | Rate-class factors 0.80 – 1.75 | **[std]** |
| `lapse_table.csv` | Base annual lapse by policy year: 6% / 5% / 4% / 3% | **[std]**, from the UL persistency studies [REG-R20] [REG-R21] applied to VUL by analogy — VUL is not broken out separately, which the notes flag |
| `prem_persistency.csv` | 1.00 in year 1 grading to 0.85 in year 5 and 0.80 after | **[std]** placeholder grading, base levels [REG-R21] |
| `surr_charge_table.csv` | `VUL14`: $18.00 per $1,000, linear to zero over 14 policy years | amount and shape **[std]** (spec footnote 10); 14-year period [S1] [S2] |

## Naming

Cells follow `UL_US_S` — and through it lifelib's `basiclife/BasicTerm_S` and
`savings/CashValue_SE` — wherever the concept is shared: `pols_*` for policy counts,
`av_*` for account values, plural nouns for cash flows, `*_rate` for rates, `*_pp` for
per-policy amounts, `timing` and `kind` string arguments that `raise ValueError` on
anything unknown. Names are added only where variable UL has something fixed universal
life does not: the subaccount vector (`sa_pp`, `alloc`, `fund_expense_ann`,
`gross_return_mth`), the fixed option (`fa_pp`, `fixed_return_mth`), the loan account
(`la_pp`, `loan_cr_rate_ann`, `loan_spread`), the M&E charge (`me_charge_pp`,
`me_rate_ann`), the two views (`claims_net`, `net_cf_ga`, `result_net`,
`check_net_view`) and the behavior module (`funding_ratio`, `av_pricing_pp`).

The technical notes use compact actuarial symbols; the full mapping lives in the
`Projection` Space docstring. Eight cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `AV_{t+1}`, `D_{t+1}` | `av_pp(t)`, `loan_bal_pp(t)` | The notes index end-of-month balances with `t+1`. Their death claim `DB_t^EOM − D_{t+1}` is two quantities of the *same* month |
| `CSV_t = AV − SC − D` | `ncsv_pp(t)` | The chassis calls the debt-net figure `ncsv_pp`; `csv_pp` is the `AV − SC` intermediate |
| `m` (M&E rate) and `m` (policy month) | `me_rate_ann` and the pricing path's `m` argument | The notes reuse the letter |
| `l_t` | `pols_if(t)` | Both are start-of-month, so they coincide — unlike `UL_US_S`, whose notes put `l(t)` at end of month |
| `c_t` per $1,000 NAAR/month | `coi_rate(t)` | Not comparable with `CashValue_SE.coi_rate`, a rate per unit of account value |
| `U` | `units()` — **no `t`** | Charges are on `F₀`, not the current face |
| `MD_t` non-COI part | `maint_fee_pp(t)` | Income. `expenses(t)` is the insurer's own outgo, and the two must never be confused |
| withdrawals (a gross outflow) | `withdrawals(t)`, column `withdrawals` | A payment on the owner's election, not a claim: `claims(t, kind)` takes `"DEATH"` and `"LAPSE"` only, and does not count withdrawals in its `kind is None` total. `claim_pp(t, "WITHDRAWAL")` still carries the per-policy amount |

The `result_cf()` columns are `pols_if`, `premiums`, `claims_death`, `claims_lapse`,
`withdrawals`, `expenses`, `premium_taxes`, `net_cf`. The surrender column is named for
the `"LAPSE"` kind that produces it, and the cash flow columns net to `net_cf`, which is
income-positive as in every model in this library.

## The worked example's two age lookups — shipped, not resolved

The notes' worked example sits in **policy year 3**, where the model point's attained
age is 47, but it looks up two age-dependent parameters at the **issue** age 45:

- the corridor factor, quoted as `κ(45) = 215%`, where the rule at age 47 gives 203%;
- the current COI rate, quoted as `c = $0.04`, which the notes themselves label the
  *year-1* disclosed anchor for male 45 standard non-tobacco [S4].

The notes' own state-variable table defines `κ_t` as "corridor factor at `x_t`", the
attained age, so the rule is unambiguous and the worked example diverges from it.
Rather than pick one, the model ships both. `corridor_factor_at(a)` and `coi_rate_at(y)`
are the rules; model point 1 carries `corridor_override_m1 = 2.15` and
`coi_rate_override_m1 = 0.04`, and model point 2 is the same cell with both blank.

**Both pins are confined to `t == 1`.** That is the single month the worked example
describes, and the pinned values are lookups performed at the wrong age, not parameters
of the contract. Holding an issue-age corridor factor across the seventy-seven years
this projection runs would misstate every later month, and holding one disclosed COI
rate flat would leave a policy paying $0.04 per $1,000 for its insurance at age 100.
Because the pin lifts at month 2, point 1's output *steps* between months 1 and 2 —
`run.py` prints a note saying so, and point 2 is the same cell without the step. Neither
value is "right"; the rule is a standardization and so is the pin, and
`test_the_two_age_lookups_are_shipped_both_ways` holds the gap open in both directions.

This is the pattern `Term_US_A` uses for its `M(1)` divergence.

A second, smaller gap sits in the same worked example and is pinned the same way. The
notes' table totals the two subaccounts by adding the **displayed** figures: 30,482.82 +
20,023.41 = 50,506.23, where the exact sum is 50,506.2245, which displays as 50,506.22.
The same half cent flows into the memo `EOM NAAR = 449,493.77`. It is a display
artifact, not a modelling difference — the recursion is identical — and
`test_worked_example_total_av_is_a_sum_of_rounded_parts` asserts both readings so it
cannot be quietly closed.

## The corridor tail grades to 100% at 95, not at 90

The two governing documents describe the tail of the GPT corridor table differently.
The technical notes' parameter table gives *"250% (≤40), 215% (45), 185% (50), 150%
(55), 130% (60), to 100% at 90–95; linear interpolation"*, which does not say which end
of that range reaches 100%. The product spec's footnote 11 does: *"The reference model
linearly interpolates between the quoted ages and grades to 100% at 95."*

`corridor_factors.csv` follows the spec — 130% at attained age 60 joined by a straight
line to 100% at 95, level at 100% from there — and marks every interpolated age, 41–94,
`linear interpolation [std]`. The column is carried to six decimals because the
thirty-five-year grade does not terminate in four: the annual step is 0.30/35 =
0.0085714…, so κ(90) = 1.042857, not 1.0000.

The choice is not cosmetic. Grading to 90 instead would put κ at exactly 1.0000 from
age 90 on, and a corridor of 1.0000 collapses the net amount at risk to zero on an
Option A policy funded above its face — which is what the anchor cell has become by
then. At policy month 517, attained age 90, its account value before the deduction is
$801,347.97 against a $500,000 face, so the corridor alone is holding the death benefit
up. With κ(90) = 1.042857 the death benefit is $835,691.34, the net amount at risk
$34,343.37 and the month's cost of insurance $154.73; with κ = 1.0000 the death benefit
would be the account value itself, the net amount at risk exactly zero and the cost of
insurance zero — for every month from age 90 to the end of the projection.
`test_corridor_grades_to_100_at_95` pins the endpoint, the interpolation and that
consequence together, so the tail cannot be quietly regraded back.

No sourced number moves either way. The two readings differ only over attained ages
61–94, and not one of those is a quoted age: 250% (≤40), 215% (45), 185% (50), 150%
(55) and 130% (60) are [S2] [R3] and identical under both, and so is 100% from age 95
on. What is at stake is which **[std]** line is drawn between the last quoted factor
and that 100%.

## `naar_factor` is gone — the one sourced deviation

The fixed-UL chassis discounts the death benefit one month at the *guaranteed* rate
before subtracting the account value, and its notes are emphatic that using the current
rate or the post-deduction account value produces systematic COI errors. **None of that
applies here.** The VUL prospectuses define the net amount at risk as death benefit less
account value with no discount [S2], and the variable-UL notes call this out as the one
sourced deviation from the base chassis.

So `net_amt_at_risk(t) = max(0, db_pp(t) − av_pp_at(t, "BEF_FEE"))`, there is no
`naar_factor` cells, and `test_naar_carries_no_one_month_discount` asserts both the
formula and the size of the error the chassis version would introduce — about $824 of
net amount at risk on the anchor cell, in every month.

What *is* kept from the chassis is where the account value is measured: **before** the
monthly deduction. That is what removes the circularity under Option B, where the death
benefit depends on the account value and the net amount at risk depends on the death
benefit.

## Two views of one run, and the claim that is not `DB − AV`

The notes carry an explicit warning headed *"a common specification error"*: the
insurer's death-claim cash flow is the **full death benefit** less policy debt. Seizing
the account value is the *funding* of part of that outflow; `DB − AV` is the net
general-account strain. Projecting only `DB − AV` understates gross benefit outgo and
breaks reconciliation with statutory exhibits, and projecting the full death benefit
*and* separately expensing the net amount at risk double counts.

The model projects the gross view — `claims(t, "DEATH") = (db_pp_eom(t) −
loan_bal_pp(t)) × pols_death(t)` — and derives the general-account view arithmetically
from the same run in `result_net()`, whose columns carry the notes' own names
(`load_income`, `md_income`, `me_income`, `loan_spread`, `claim_gross`, `claim_net`,
`surr_outgo`, `sc_income`, `sa_transfer`). `check_net_view()` pins the two together:

```
net_cf(t) == net_cf_ga(t)
             + av_change(t) − inv_income(t) + wd_fees(t)
             − me_charge(t) − loan_spread(t)
             + loan_bal_pp(t) × (pols_death(t) + pols_lapse(t))
```

`av_change − inv_income` is the net premium in and the account releases out;
`− me_charge` and `− loan_spread` remove the two margins the gross view never sees
because they are collected *inside* the accounts; the last term is the debt extinguished
against the account value. It closes to 1e-9 for every month of every shipped model
point.

## The default test fires at issue

The notes define default as `CSV_t = AV_t − SC_t − D_t ≤ 0`, and step 9 lapses the
policy at the next monthiversary "if not cured". Read literally that test is **true from
issue** on any front-loaded design: in policy year 1 the scheduled $18 per $1,000
surrender charge is $9,000 against an account value a first premium has barely started,
so `AV − SC` is deeply negative on a perfectly healthy new policy. Model point 3 shows
exactly this — `first_default_month() == 1`.

`is_default(t)` therefore reports the notes' test as written, and **`is_shortfall(t)` is
the companion diagnostic** that answers the question the default rule is really asking:
can the unloaned account value pay the monthly deduction? That is the fixed-UL chassis's
trigger, and on model point 3 it first fires at policy month 594 — policy year 50, where
a level $500 a month stops covering the cost of insurance on a $500,000 net amount at
risk.

Neither test terminates anything. The grace cascade is **not implemented**: the notes
give no cure test, no in-grace deduction accrual and no in-grace death benefit, so there
is nothing complete enough to project. `first_shortfall_month()` marks where the
projection stops describing a live contract; past it the arithmetic simply continues, as
it does on the fixed-UL chassis.

One consequence is worth naming. Once the unloaned account value passes through zero the
pro-rata deduction denominator does too, and the notes list *"pro-rata deduction
allocation breaking on zero unloaned balances (guard the denominator)"* among the
pitfalls. The guard here falls back to the **premium allocation shares** `α_i` rather
than to zero **[std]**: the shares still sum to one, so the full deduction is still
applied and the account value roll-forward stays exact on both sides of the crossing.
Returning zero instead would silently forgive the charge and break the identity — which
is what `test_pitfall_pro_rata_deduction_guards_the_denominator` was written to catch.

## The dynamic behavior module is built, and switched off

The notes' policyholder-behavior section is implemented in full — the funding ratio
`φ_t = AV_t / AV*_t`, dynamic lapse `λ_t = min(2.0, max(0.5, 1 + 0.5(1 − φ_t)))`,
premium persistency `ρ_t = ρ^base_t × min(1.3, max(0.7, φ_t^−0.25))`, and the
denominator `AV*`, which is a genuine second recursion: the account value projected from
issue under a level 6% gross return, current charges, planned premiums, no decrements,
no loans, starting from zero.

It is switched **off** by `Projection.dyn_behavior_on = False`, which makes `φ = 1`,
`λ = 1` and `ρ = 1`. That is what lets the base deterministic run pay the planned
premium in full, which is what the worked example does ("planned premium $500/month
paid"). `Term_US_A` switches conversion off for exactly the same reason. Switch it on
with one assignment:

```python
model.Projection.dyn_behavior_on = True
```

and the base persistency scale and both dynamic multipliers come alive together. All
three self-checks still close with it on; a test asserts that.

The surrender-charge cliff spike is separately optional, as the notes make it —
`lapse_shock_mult` ships at 1.0 (off), and the cliff month, policy month 169, is derived
from `surr_charge_table.csv` rather than hard-coded.

## Standardizations used

Everything in this list is **[std]**: the 4.0% current premium load; the two-subaccount
lineup and its 0.75% / 0.55% fund expense ratios; the monthly approximation of daily M&E
and fund-expense accrual; the $18.00 per $1,000 surrender charge and its linear
fourteen-year run-off; the linear interpolation of the corridor factors between the
quoted ages and the grading of their tail to 100% at attained age 95 rather than 90;
the illustrative guaranteed COI scale standing in for the 2017 CSO table
and the 50%-of-guaranteed current placeholder; the illustrative best-estimate mortality
table standing in for the 2015 VBT, and the 100% A/E factor with no improvement; the
rate-class factors; the base lapse vector and its monthly conversion; the
surrender-charge cliff spike; the dynamic lapse and premium persistency forms and the
6% pricing path behind them; the level 6% gross return scenario; the loan-collateral
opening balance taken equal to the opening debt; the pro-rata deduction allocation and
its allocation-share fallback; the floors on `csv_pp` and `ncsv_pp`; the $75 per policy
per year maintenance expense with no inflation and the 2% percent-of-premium expense;
and the truncation of the projection at attained age 121.

Not implemented, and named as such in the model docstring: the grace and default
cascade, the no-lapse guarantee and overloan protection riders, new loans and
repayments, guideline premium and 7-pay/MEC testing, face and option changes, CVAT, and
stochastic return sets (a data change, not a formula change). Withdrawals are
implemented and set to zero in every shipped model point, which is the notes' baseline.

## Tests

`tests/test_variable_ul_us.py` asserts every row and column of the worked example — the
opening balances, the premium and its load, the 60/40 net premium split, the corridor
product that loses to the face, the net amount at risk, the cost of insurance, the two
fixed charges, the monthly deduction and its pro-rata split, both unit-value growth
factors to six decimals, both end-of-month subaccount balances, the M&E collected in
each subaccount, the insurer margin for the month, the surrender charge, the cash
surrender value and the end-of-month death benefit and net amount at risk — plus one
test per entry on the notes' "Known modeling pitfalls" list, the in-force roll-forward,
all three self-checks on all four model points, the two-way age-lookup divergence, the
behavior module both off and on, the `withdrawals`/`claims` split and the `result_cf()`
columns netting to `net_cf`, the start-of-month `pols_if` weighting, and a read → write
→ re-read round trip carrying the inputs along.

```bash
python -m pytest tests/test_variable_ul_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_variable_ul_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_variable_ul_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R3]: #uslib-variable_ul-r3
[REG-R20]: #uslib-reg-r20
[REG-R21]: #uslib-reg-r21
[std]: #uslib-std
<!-- END generated citation links -->
