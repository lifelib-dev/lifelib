# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/universal_life/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics — the guaranteed maximum COI scale, the $7.50 per-policy and
> $0.26/$0.156 per-unit charges, the GPT corridor factors, the specimen's
> net-amount-at-risk convention, the monthly surrender-charge amortization, the 0.75%
> loan spread, cessation of charges at attained age 121 — are sourced from a specimen
> policy [S3]. The two assumptions that drive this product hardest, the **current
> credited rate** and the **current COI scale**, are both **[std]**: insurers do not
> publish them, and the one rates page the research attempted returned HTTP 403 [S5].
> So are the mortality table, the lapse vector, the premium persistency scale and every
> expense. Replace them with company data before drawing any conclusion from the
> numbers.

## Run it

```bash
python products/universal_life/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/universal_life/UL_US_S")
model.Projection[1].result_av()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
There are three result tables, all `DataFrame`s indexed by policy month `t`:

| Cells | What it shows |
|---|---|
| `result_av()` | The per-policy account value roll-forward, **in the columns and order of the worked example in the technical notes** — `AV(t-1)`, `NP`, `AV'`, `DB`, `NAAR`, `COI`, `MD`, `AV'-MD`, interest, `AV(t)`, then the surrender and loan values |
| `result_cf()` | The liability cash flows: `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes`, `net_cf` — income-positive, so the flow columns sum to `net_cf` |
| `result_pols()` | The decrements: in force, deaths, lapses, maturities, and the monthly rates behind them |

The model and both Spaces carry docstrings — `model.doc` describes the product, the
projection basis and everything deliberately left out, and `model.Projection.doc` holds
the full mapping between the technical notes' symbols and the cells names.

## Monthly, not annual

Policy month `t` runs 1 … `proj_len()`. `t = 1` is the **issue month** of a
new-business model point; for an in-force point it is the first projected month,
sitting `duration_mth_init()` completed months after issue. This is the grid the
technical notes specify, and it is not a stylistic choice: universal life is defined by
a monthiversary deduction and a monthly interest credit, and the order of those two
inside the month changes the answer. Compare `Term_US_A`, where `t` counts **years**,
because every decrement in that product is on an annual cycle and there is no account
value requiring monthiversary processing.

The processing order inside month `t` is the notes' own:

1. amortize the surrender charge (`surr_charge_rate`);
2. gross premium and its load, net premium to the account value (`premium_pp`,
   `prem_to_av_pp`);
3. withdrawal, withdrawal fee, and under Option A the face reduction they force
   (`wd_pp`, `wd_fee_pp`, `sum_assured_at`) — after which the account value is the
   notes' `AV'(t)`, `av_pp_at(t, "BEF_FEE")`;
4. death benefit and the GPT corridor test (`db_pp`);
5. net amount at risk (`net_amt_at_risk`);
6. the monthly deduction (`mth_deduction_pp`);
7. the shortfall test (`is_shortfall`);
8. **end of month**: one month's interest on the post-deduction balance
   (`inv_income_pp`), loan interest accrual (`loan_bal_pp`);
9. **end of month**: decrements, death before lapse (`pols_death`, `pols_lapse`).

Cash flows are **undiscounted**. Premiums, expenses and premium taxes fall at the
beginning of the month and are weighted by `pols_if(t)`; death claims by
`pols_if(t) × mort_rate_mth(t)`; surrender payments by
`pols_if(t) × (1 − mort_rate_mth(t)) × lapse_rate_mth(t)`. Reserves and discounting are
a separate layer that consumes these flows.

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `UL_US_S/` holds nothing but formulas:

```
products/universal_life/
  model_point_table.csv        <- inputs live here
  coi_rates.csv
  corridor_factors.csv
  mort_table.csv
  class_factor_table.csv
  lapse_table.csv
  prem_persistency.csv
  surr_charge_table.csv
  run.py
  README.md
  UL_US_S/             <- formulas only
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
many policies are projected.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is
read, so it works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `coi_rates_file` | `coi_rates()` | `coi_rates.csv` |
| `corridor_file` | `corridor_factors()` | `corridor_factors.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `class_factor_file` | `class_factor_table()` | `class_factor_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `prem_persistency_file` | `prem_persistency_table()` | `prem_persistency.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `UL_US_S/`
without the CSVs and it will read fine, then fail on first evaluation. What you gain is
that a diff of the model shows logic changes only, and an input can be edited or swapped
in place — point `Data.mort_table_file` at another same-schema file and the projection
follows, with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Three model points, all on the anchor configuration M35 / StdNT / $100,000. **Point 1 is the worked-example anchor cell** (Option A, GPT, $1,800 planned annual premium, no opening account value, no loan); point 2 switches to Option B, and is also the point that runs into permanent shortfall from policy year 57 (see below); point 3 is an in-force cell at 120 completed months with $15,000 of account value and a $2,000 loan | anchor cell from the specimen [S3]; the planned premium, and points 2 and 3, **[std]** |
| `coi_rates.csv` | Guaranteed maximum monthly COI per $1,000 NAAR, policy years 1–87, with a `provenance` column marking each row. **Covers the specimen anchor cell M / StdNT / issue age 35 only** — a model point on any other cell needs this table extended first, and a test enforces that every model point is projectable | printed anchor years sourced [S3]; intermediate years log-linearly interpolated **[std]** |
| `corridor_factors.csv` | GPT corridor factors by attained age, 250% to age 40 grading to 101% above 93 | specimen table [S3] [R2] |
| `mort_table.csv` | Best-estimate annual mortality by age 18–120, `q(120) = 1.0` | **illustrative [std]**, a Gompertz–Makeham curve — *not* a published table. The notes recommend 2015 VBT; that family is licensed and may not be reproduced here |
| `class_factor_table.csv` | Rate-class factors for the spec's six classes | **[std]**, matching `Term_US_A` where the classes overlap |
| `lapse_table.csv` | Base annual lapse 6% / 5% / 4% / 3% by policy year | **[std]**; shape informed qualitatively by [R7] [REG-R20], whose tables are behind a paid package |
| `prem_persistency.csv` | Paid/planned factors, 100% falling 2pp a year to a 70% floor | **[std]**; shape from [R7] |
| `surr_charge_table.csv` | The surrender charge schedule as `(initial per $1,000, runoff years)` | 9-year runoff and monthly amortization sourced [S1] [S2] [S3]; the $9.00 level **[std]** |

The surrender charge is stored as two parameters rather than a 108-row rate vector so
that the run-off length is a *number the model can read*: `lapse_shock_year()` derives
the surrender-charge-expiry lapse shock from it instead of hard-coding "year 10", and a
different schedule moves the shock with it.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those
models have an analogue: `pols_*` for policy counts, `av_*` for account values, plural
nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts, `timing` and
`kind` string arguments that raise `ValueError` on anything unknown. The technical notes
use compact actuarial symbols instead; the full mapping lives in the `Projection` Space
docstring, and it covers **every** symbol the notes define — the model point attributes
table, the state variables table and the notation list. Three of those have no cells at
all and are carried in the mapping as `(not modelled)` so the absence is recorded rather
than silent: `grace_flag(t)` (the grace cascade is a diagnostic here), `premium_mode`
(every premium in this model is monthly **[std]**) and `earned_rate(t)` (the input the
optional NGE revision rule would need). Eight cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `risk_class` | `rate_class` | The name comes from `Term_US_A`/`BasicTerm_S`, which this library follows ahead of the notes where the two collide; it also avoids reading as Python's `class`. The six classes themselves are the product spec's, unchanged |
| `l(t)` | `pols_if(t)` | The notes' `l(t)` is in force at the **end** of month `t`; `BasicTerm_S`'s `pols_if(t)` is in force at the **start**. So `pols_if(t) = l(t−1)`, and the notes' own "weight premiums by `l(t−1)`" becomes "weight by `pols_if(t)`" |
| `MD(t)` | `mth_deduction_pp` / `maint_fee_pp` | `CashValue_SE` calls the non-COI part of an account-value deduction `maint_fee`; that name is kept, and `mth_deduction_pp` is the notes' `MD(t)` in full |
| *(none)* | `maint_fee` vs `expenses` | See below — they are opposite signs and easy to confuse |
| `t` in `SC(t)` | `duration_mth(t) + 1` | See below — the notes' `t` counts the current month |
| `q_coi` | `coi_rate` | Per $1,000 of **NAAR per month**, not per unit of account value as in `CashValue_SE`. It is divided by 1,000 in `coi_pp` |
| `AV'(t)` | `av_pp_at(t, "BEF_FEE")` **and** `av_pp_db_basis(t)` | The notes write one symbol and use it for two things: the balance the deduction comes out of (signed) and the balance the death benefit is measured on (floored at zero). See the section on the death benefit floor above |
| "Withdrawal outgo" | `withdrawals(t)` | The notes list it beside death claims and surrender outgo, but a withdrawal is a payment the owner *elects*, not a claim on a contingency. It is its own cells and its own `result_cf()` column, and `"WITHDRAWAL"` is not a `kind` of `claims` — see below |

## `maint_fee` is income; `expenses` is outgo

The one naming trap in this model. `maint_fee_pp(t)` is the non-COI part of the monthly
deduction — the $7.50 per-policy charge plus the per-unit coverage charge — taken *out
of the policyholder's account value and kept by the insurer*. `expenses(t)` is the
insurer's own **[std]** maintenance cost of $75 per policy per year, inflating at 2.5%,
paid *out*. They differ in sign, in size and in whose money they are. `margin_expense()`
has both, with the right signs; if the two ever get swapped, `check_margin()` fails.

The same distinction explains why there is no acquisition expense: the notes specify
none for this product, because the higher per-unit charge in policy years 1–10 *is* the
contractual acquisition-cost recovery, and that is income. `expense_acq` is carried at
zero only so products built on this chassis can switch it on.

## A withdrawal is not a claim

The notes' cash flow table lists "Withdrawal outgo" in the same block as death claims
and surrender outgo, and it is tempting to fold it in as a third `kind` of `claims`.
This model does not: a partial withdrawal is a payment made on the **owner's election**,
not on a contingency, and the annuity models in this library already treat it that way.
So

- `withdrawals(t) = W(t) × pols_if(t)` is a cells of its own, weighted by the in force
  at the beginning of the month because that is when a withdrawal is taken — not by a
  decrement, as death and surrender payments are;
- the `result_cf()` column is `withdrawals`;
- `"WITHDRAWAL"` is **not** a `kind` accepted by `claims(t, kind)` or `claim_pp(t, kind)`,
  and is not in the `kind is None` total, so nothing double-counts it.

The consequence to hold on to when reading a formula: `claims(t)` with no `kind` is the
death and surrender total *only*, so `net_cf` subtracts `withdrawals(t)` as a separate
term, and so does `check_av_roll_fwd()`. The per-policy amount is still `wd_pp(t)`, the
notes' `W(t)`; the $25 fee is retained by the insurer, so it is `wd_fees(t)` inside
`margin_expense()` and never part of the payment.

The surrender column is named to match the `kind` that produces it: `claims(t, "LAPSE")`
lands in `claims_lapse`.

## The NAAR convention is the specimen's, and it is not the obvious one

`NAAR(t) = DB(t) / (1 + i_gm) − AV'(t)`. Two choices in that line are the specimen's,
and the notes list both among the modelling pitfalls:

- the death benefit is discounted one month at the **guaranteed** rate, never at the
  credited rate — 1.0016516 at the composite 2% guarantee, where the specimen itself
  prints 1.0024663 = 1.03^(1/12) at its own 3% guarantee [S3];
- the account value is measured **before** the monthly deduction, not after. Measuring
  it after makes the COI charge depend on itself and forces an iteration, and produces
  small but systematic COI errors.

`test_pitfall_naar_uses_guaranteed_rate_and_pre_deduction_av` asserts the formula and
then asserts that each of the two wrong readings moves the answer by more than a dollar
in month 1, so neither can creep back in unnoticed.

Measuring the account value before the deduction is also what removes the Option B
circularity the notes warn about: under Option B the death benefit depends on the
account value and the net amount at risk depends on the death benefit, but with this BOM
ordering neither depends on the deduction, so nothing is simultaneous. Model point 2
exercises it.

## The notes' `t` and `duration_mth(t)` differ by one

The surrender charge amortizes as `SC(t) = max(0, (9.00 − t/12) × U)`, and the notes'
`t` there **counts the current month**: in the issue month it is 1, giving $8.916667 per
$1,000, not $9.00. `duration_mth(t)` in this model is *completed* months, following
`CashValue_SE`, so it is 0 in the issue month. `surr_charge_rate` therefore uses
`duration_mth(t) + 1`, and says so in its docstring. Reading the notes' `t` as
`duration_mth(t)` shifts the entire nine-year run-off by a month; the test pins the
first month, the twelfth, the last non-zero month and the first zero month.

## `surr_charge_pp` is the schedule; `surr_charge` is what is collected

The notes write `CSV(t) = AV(t) − SC(t)` with no floor. Taken literally that is negative
for the first eight policy years of the anchor cell — the scheduled charge is $891.67 in
the issue month against an account value of $101.80 — and a negative cash surrender
value would be a payment *from* the surrendering policyholder. `csv_pp` and `ncsv_pp`
are floored at zero **[std]**, so:

- `surr_charge_pp(t)` is the charge the schedule *says*;
- `surr_charge(t)` is the charge actually *collected*, `(AV(t) − CSV(t)) × pols_lapse(t)`,
  capped by the account value.

Early surrenders therefore forfeit the whole fund and pay nothing, which is what the
contract means, and `check_margin()` still closes because the collected figure is the one
in the margin.

## The grace cascade is shipped as diagnostics, not as a decrement

This is the one module the technical notes describe and do not specify completely enough
to project, and it is worth being explicit rather than quietly approximating.

What *is* complete, and is implemented: the trigger, `AV'(t) − L(t−1) < MD(t)`
(`is_shortfall`), and the required cure payment, three times the monthly deduction
grossed up for the premium load (`cure_premium_pp`).

What is not: during the 61-day grace, "deductions accrue as due-and-unpaid" — the notes
do not say what happens to the account value meanwhile, and death in grace pays
`DB − L − overdue deductions`, which needs a state the notes do not define. The cure
test, "planned-premium payers are assumed to cure if `pp(y) × planned >= cure`", compares
an *annual* planned premium with a cure derived from a *monthly* deduction; the
dimensions do not line up, and guessing which side to rescale would be inventing the
answer.

So no policy is terminated for insufficiency in this model. That is a real limitation
for an underfunded model point, and it is named in the model docstring as well as here.

**It is not inert.** Two of the three shipped model points never trigger it, and one
does:

| Model point | Months projected | Months in shortfall | First trigger |
|---|---|---|---|
| 1 — anchor, Option A | 1,032 | 0 | — |
| 2 — Option B | 1,032 | **356** | month 677, policy year 57, attained age 91 |
| 3 — in force, Option A | 912 | 0 | — |

The anchor cell's $150 a month comfortably covers a $39.54 deduction and the account
value grows from there, and point 3 opens with $15,000 already in the fund. Point 2 is
different: under Option B the death benefit is face *plus* account value, so the net
amount at risk never runs down the way it does under Option A, and by attained age 91
the monthly deduction is $1,096.87 against an account value of $407.74. From that month
on the policy is in permanent shortfall — and because nothing terminates it, deductions
keep coming out of a fund that is empty. Its account value ends the projection about
**$1.84 m overdrawn**.

**Treat cash flows for a model point in shortfall as not meaningful past the trigger
month.** `test_shortfall_trigger_is_live_on_point_2_and_inert_on_1_and_3` pins exactly
that table, over the whole projection rather than the first ten years, so the claim and
the assertion cannot drift apart again.

## The death benefit is floored at the face amount, because the account value is not

A negative account value has one consequence that must not be allowed through. The notes
set the Option B death benefit to `F + AV'(t)` (processing order, step 4) and measure the
net amount at risk against the same `AV'(t)` (step 5), both on the premise that `AV'` is
a real account balance. For point 2 past month 677 it is not one, and taken literally
that formula gives a death benefit *below* the face amount, then a negative one:
`db_pp(747)` was −$1,643.45 and `db_pp(800)` was −$131,817.63 — death claims paid **by**
the beneficiary. Before this was fixed, 263 rows of `result_cf()` carried negative
`claims_death`, which netted $2,944.78 off the death claims and inflated `net_cf` by the
same amount.

So the account value that the death benefit and the net amount at risk are measured
against is a cells of its own, `av_pp_db_basis(t) = max(0, AV'(t))`, floored at zero
**[std]** — the same floor `csv_pp` already carries, for the same reason: a negative
account balance is an artifact of the missing termination, not a contract state.
`av_pp_at(t, "BEF_FEE")` stays signed, because that is the balance the deduction really
comes out of and the roll-forward has to close against it.

Two things follow. The Option B death benefit is never below the face amount, so no
death claim is ever negative. And the net amount at risk stops growing with the
shortfall, so the model does not charge an ever-larger COI on a fund that is not there.
Wherever `AV'(t) ≥ 0` — every month of points 1 and 3, and the first 677 of point 2's
1,032 months — the floored and unfloored values are identical, so the worked example is
untouched and `check_av_roll_fwd()` and `check_margin()` still close on all three points.

## `check_margin` needs three more terms here than in `CashValue_SE`

`CashValue_SE.net_cf` is a profit measure: it already nets the change in account value
and the investment income, so its margin identity is just
`net_cf = margin_expense + margin_mortality`. This library projects **gross liability
cash flows**, so `net_cf` here is
`premiums − claims − withdrawals − expenses − premium_taxes` and the
identity becomes

```
net_cf(t) = margin_expense(t) + margin_mortality(t)
            + av_change(t) − inv_income(t)
            + loan_bal_pp(t) × pols_lapse(t)
```

The last term is the policy debt extinguished against the account value when a policy
carrying a loan surrenders; it is zero for the two new-business model points and live
for point 3. `check_margin()` verifies this month by month, and together with
`check_av_roll_fwd()` it is the strongest single guard in the model: it fails if a charge
is double-counted, if a weighting uses the wrong in-force basis, or if the
deduction/interest order is reversed.

## Where the projection stops when the contract never matures

Universal life has no maturity date. At attained age 121 monthly deductions cease,
premiums are no longer accepted, and coverage continues for life [S2] [S3]. So there is
no contractual event to project to, and `pols_maturity(t)` is identically zero — the
cells is kept only so the in-force roll-forward has the same shape as in the term and
annuity models of this library, where it is not zero.

What ends the projection instead is mortality. `omega_age` is 120, the last age of
`mort_table.csv`, where the annual rate is 1.0, and
`proj_len() = 12 × (omega_age − age_at_entry() + 1) − duration_mth_init()` — 1,032
policy months for the anchor cell. The charge-cessation rule at age 121 is implemented
anyway (`premium_pp`, `coi_pp` and `maint_fee_pp` all return zero from there) so that a
longer mortality table does not silently keep charging.

## The free withdrawal allowance is annual, and that needs state

The notes' step 3 says "apply free-amount rule (10% of AV per policy year **[std]**)",
and their state variables table carries `wd_used_year`, "free-withdrawal usage in current
policy year, updated on withdrawal". The **per policy year** is the whole content of the
rule: grant the 10% afresh every month and a policyholder withdrawing 10% of the account
value monthly consumes twelve full annual allowances in a policy year, so
`face_reduction_pp` never fires and an Option A face amount never moves — which is not a
simplification of the rule, it is its deletion.

So `wd_used_year(t)` is a cells: zero on each policy anniversary, and increased month by
month by the free part of each withdrawal taken since, `min(W(t−1), wd_free_pp(t−1))`.
`wd_free_pp(t)` is then what is *left* of the allowance, `max(0, 10% × AV −
wd_used_year(t))`. In the first withdrawal month of a policy year nothing is used yet and
it is the full 10%; a second 10% withdrawal in the same policy year is fully chargeable
and cuts the face. `test_free_withdrawal_allowance_is_annual_not_monthly` drives a model
point at 10% a month and asserts exactly that, including the reset at the anniversary.

## Standardizations used

Everything in this list is **[std]**: the 2.00% guaranteed and 4.00% current credited
rates; the 60% current-to-guaranteed COI factor; the 6% current premium load; the $9.00
per $1,000 initial surrender charge; the log-linear interpolation between the specimen's
printed COI anchor years; the illustrative mortality table and the 100% A/E factor with
no improvement; the rate-class factors; the base lapse vector and its 35% cap; the 2.0×
surrender-charge-expiry shock; the dynamic-lapse formula (neutral in the base run,
because `comp_rate_ann` returns the credited rate exactly as the notes prescribe); the
premium persistency scale; $75 per policy per year of maintenance expense inflating at
2.5%; the 2.5% percent-of-premium expense; monthly rather than daily compounding; the
floor at zero on `csv_pp` and `ncsv_pp`; taking "cumulative premiums less **a portion**
of withdrawals" as the whole withdrawal; the free-withdrawal base of 10% of account
value (the specimen's own carve-out is 10% of *net cash surrender value*, capped at
$10,000, first withdrawal of each of the first 15 policy years [S3] — the notes
standardize it away and this model follows the notes); and the floor at zero on the
account value the death benefit is measured against.

Withdrawals and loans are otherwise **off by data, not by code**: the mechanics are
implemented, and every shipped model point carries `wd_pp = 0`, while only point 3
carries a loan balance. Rider charges are the notes' placeholder term, zero.

Not implemented at all, and named in the model docstring for the same reason: the grace
cascade (above), reinstatement, NGE revision, new loans and repayments, face increases
and decreases, option changes and surrender-charge layering, and CVAT.

## Tests

`tests/test_universal_life_us.py` asserts all three rows of the worked example column by
column to the cent, the full-precision trace printed under it (`i_m`, the NAAR factor,
the discounted death benefit, the guaranteed and current COI rates, the COI charge, the
monthly deduction, the non-binding corridor minimum), the contractual policy-date rule
`AV = net premium − first monthly deduction`, **one test per entry in the notes' "Known
modeling pitfalls" list**, the account value and in-force roll-forwards, the margin
identity, the surrender-charge month index, the year-10 lapse shock, the per-unit
step-down after year 10, the loan roll-forward, the in-force model point's duration
offset, the cash-surrender floor, that withdrawals are wired but off, the result table
shapes, that unknown `timing` and `kind` strings raise, and that every model point in
the table projects.

Three tests pin the library-wide cash flow conventions: `test_a_withdrawal_is_not_a_claim`
(on the withdrawing model point, where the amounts are non-zero, so a double count would
show), `test_the_cash_flow_columns_sum_to_net_cf` (income-positive `net_cf`, all three
model points) and `test_pols_if_is_the_start_of_month_weight`
(`premiums(t) / premium_pp(t) == pols_if(t)`, so the in-force column of `result_cf()`
reconciles with the row it sits on).

Four more tests exist because a review found the model wrong:

| Test | What it pins |
|---|---|
| `test_death_benefit_never_falls_below_the_face_amount` | `db_pp(t) >= sum_assured_at(t)`, `claim_pp(t, "DEATH") >= 0` and `claims(t, "DEATH") >= 0` for **every** month of **every** model point. Point 2 used to produce a death benefit below the face amount in 355 of its 1,032 months, and negative death claims in 263 rows of `result_cf()` |
| `test_shortfall_trigger_is_live_on_point_2_and_inert_on_1_and_3` | The shortfall table above, over the whole projection: 0 months for points 1 and 3, 356 contiguous months for point 2 starting at month 677. The old test looked at point 1 only, and only at its first 120 months, while this README claimed the trigger was inert everywhere |
| `test_free_withdrawal_allowance_is_annual_not_monthly` | A 10%-of-account-value monthly withdrawal exhausts the policy year's allowance in its first month, cuts the face in every month after that, and gets a fresh allowance at the anniversary. The allowance used to be granted afresh every month, so the face never moved |
| `test_mec_flag_latches_once_the_seven_pay_test_fails` | `is_mec` stays `True` from the month the 7-pay test fails to the end of the projection. It used to revert to `False` in policy year 8, when the in-year test stops applying — the moment the failure becomes permanent under 7702A |

```bash
python -m pytest tests/test_universal_life_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_universal_life_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_universal_life_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-universal_life-r2
[R7]: #uslib-universal_life-r7
[REG-R20]: #uslib-reg-r20
[S1]: #uslib-universal_life-s1
[S2]: #uslib-universal_life-s2
[S3]: #uslib-universal_life-s3
[S5]: #uslib-universal_life-s5
[std]: #uslib-std
<!-- END generated citation links -->
