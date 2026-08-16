# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/indexed_ul/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md). The shared universal
life mechanics those notes defer to are in
[`products/universal_life/technical-notes.md`](../universal_life/technical-notes.md),
and their executable form is [`UL_US_S`](../universal_life/model.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the 10.00% cap and 2.00% guaranteed cap, 100% participation
> and 0% floor of the AG 49-A Benchmark Index Account, the 4.50%/1.00% fixed account,
> the monthly 12-month segment ladder, the $10 policy fee, the $25 withdrawal fee, the
> 61-day grace and cumulative-MNLP no-lapse test, the 10-year surrender charge period,
> the IRC 7702(d) corridor factors — are sourced. Every behavioural and expense
> assumption, the whole COI scale, the surrender charge dollars, the per-unit charge and
> **the 6.40% level index return** are **[std]** standardizations introduced for the
> reference implementation. Replace them with company data before drawing any conclusion
> from the numbers.

## Run it

```bash
python products/indexed_ul/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/indexed_ul/IUL_US_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the baseline cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy month `t` with one column per
cash flow line; `result_av()` is the account value roll-forward, `result_seg()` the
indexed segment ladder, and `result_pols()` the decrements.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## Monthly, not annual

Policy month `t` runs 1 … `proj_len()` = `12 × (121 − age_at_entry())`, so a policy
issued at 45 projects 912 months, ending as the insured attains 121. The notes fix the
grid: everything happens on the monthiversary, because that is where segments are
created and mature. `t = 1` is the issue month of a new-business point; the notes' own
month index (which starts at 0) is `duration_mth(t)`, and every `mod 12` test — the
anniversary premium, the segment maturity — is written against it.

Age 121 is an **[unverified]** inference (spec F5): no retrieved document states maturity
mechanics, and the spec reads charges ceasing at 120 with coverage continuing. The
horizon therefore truncates the run rather than terminating the contract, and
`pols_maturity(t)` is identically zero.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `IUL_US_S/` holds nothing but formulas:

```
products/indexed_ul/
  model_point_table.csv        <- inputs live here
  coi_rates.csv
  corridor_factors.csv
  mort_table.csv
  class_factor_table.csv
  lapse_table.csv
  surr_charge_table.csv
  run.py
  README.md
  IUL_US_S/                 <- formulas only
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
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `IUL_US_S/` without the
CSVs and it will read fine, then fail on first evaluation. What you gain is that a diff
of the model shows logic changes only, and an input can be edited or swapped in place —
point `Data.mort_table_file` at another same-schema file and the projection follows,
with no formula change.

Two things the universal life chassis reads from a file are **not** files here, because
these notes give them in closed form instead:

- **Premium persistency.** The chassis reads a 16-row schedule; these notes give
  `expected premium_y = planned × 0.98^(y−1)`, which is `prem_persistency(t)` with the
  rate in a Reference.
- **The index path.** `index_level(t)` generates it from a level annual return. It is the
  single point of substitution: override that one cells with a historical or simulated
  path and the whole ladder follows.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Five model points, all on the notes' anchor configuration M45 / NT / $250,000 / Option A / GPT / $10,000 planned annual premium | anchor cell from the notes' model point attribute table; the **[std]** example premium |
| `coi_rates.csv` | Guaranteed maximum monthly COI per $1,000 of net amount at risk, policy years 1–76 for M / NT / 45 | **illustrative [std]** — the notes set the guaranteed basis at 2017 CSO ANB ultimate [REG-R17], which is licensed and is *not* reproduced here |
| `corridor_factors.csv` | IRC 7702(d)(2) applicable percentages, attained ages 0–121 | sourced [R4] |
| `mort_table.csv` | Best-estimate annual mortality by age | **illustrative [std]**, *not* the 2015 VBT the notes recommend [REG-R18]; the same table `UL_US_S` ships, so the chassis and this model share a basis |
| `class_factor_table.csv` | Rate-class factors for the spec's seven classes | **[std]** |
| `lapse_table.csv` | Base annual lapse 6% years 1–10, 4% after | **[std]** placeholders; calibrate to [REG-R20] [REG-R21] |
| `surr_charge_table.csv` | $25.00 per $1,000 of initial face, 10-year linear run-off | period sourced [S1] [S5] [S7]; the dollar scale is **[std]** (spec F17) |

The model points and what each is for:

| Point | Configuration | What it exercises |
|---|---|---|
| 1 | baseline, Option A, 100% indexed | the notes' anchor; one segment a year |
| 2 | Option B | corridor and a net amount at risk that does not run off |
| 3 | indexed allocation 0% | the control run: no segment ever created, everything at the fixed rate |
| 4 | monthly premium mode | the full twelve-concurrent-segment ladder |
| 5 | $6,000/yr, $200/mo withdrawal from year 2, $6,000/yr loan from year 21 | fixed-account-first-then-pro-rata sourcing, the loan collateral account, the no-lapse test, and the overloan exposure. The $200 is deliberately below the sourced $500 withdrawal minimum, and the account value is not meaningful after month 605 — both explained below |

A model point on any other issue age, sex or class needs `coi_rates.csv` extended first;
a test asserts every model point in the table actually projects.

## Naming

Every concept shared with the universal life chassis carries **the chassis name**, and
through it lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
policy counts, `av_*` for account values, plural nouns for cash flows, `*_rate` for
rates, `*_pp` for per-policy amounts, `timing` and `kind` string arguments. A test
asserts that shared set is present, so the two models cannot drift apart silently.

The names that are new are the ones the indexed crediting engine needs — the fixed
(holding) account (`fa_pp`, `fa_pp_at`), the segment ladder (`seg_new_pp`, `seg_bal_pp`,
`seg_bal_tot_pp`, `seg_count`, `seg_return`, `sweep_pp`, `seg_roll_pp`), the crediting
formula (`index_level`, `index_change`, `index_credit_rate`, `seg_credit_base`,
`index_credit`, `seg_matured_value`), the loan collateral account (`lca_pp`) and the
no-lapse guarantee (`mnlp_rate`, `cum_mnlp_pp`, `nlg_test_ok`, `nlg_in_effect`).

The full notes-symbol → cells-name mapping lives in the `Projection` Space docstring.
Seven cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `t` (0-based) | `duration_mth(t)` | the model's `t` is 1-based; the notes' index is the completed-months count |
| `CSV_t` | `ncsv_pp` | the notes' cash surrender value already nets the loan; the chassis splits `csv_pp` (`AV − SC`) from `ncsv_pp` (`CSV − L`) |
| `W_t` "gross of $25 fee" | `wd_pp` / `wd_fee_pp` | the fee is **inside** `W_t` here, not on top of it — see below |
| `W_t − fee` (the payment) | `withdrawals(t)` | a withdrawal is a payment on the owner's election, not a claim — see below |
| `DB_t − L_t` | `claim_pp(t, "DEATH")` | these notes net the *end-of-month* loan, where the chassis nets the opening one |
| `CumP_t` vs the GPT base | `cum_prem_net_pp` / `cum_prem_pp` | one nets loans as well as withdrawals, the other does not |
| `MD_t` split | `maint_fee_pp` / `expenses` | `maint_fee` is a charge against the account value (income); `expenses` is the insurer's own outgo |

`result_cf()` returns, in order: `pols_if`, `premiums`, `claims_death`, `claims_lapse`,
`withdrawals`, `expenses`, `premium_taxes`, `net_loan_cf`, `net_cf`. `pols_if` is the
count in force at the **start** of month `t` and is the weight on that same row's cash
flows; the cash flow columns are income-positive and sum to `net_cf`. The surrender
column is `claims_lapse`, not `claims_surr`, so the column name matches the `"LAPSE"`
kind that produces it.

## The worked example is the crediting engine, not a projection

The notes' worked example prices **one segment year** with stipulated inputs: a segment
created with $12,000.00 from the sweep, "its pro-rata share of monthly deductions is
$15.00 in each of the 12 segment months **[std]** example values", index 4,500.00 →
5,040.00 (scenario A) or → 3,825.00 (scenario B). It is not output of the full monthly
projection, and the notes label the numbers as example values.

So it is asserted against the engine cells with exactly those inputs, and every row and
column reproduces to the cent — including the two variant credits the notes price in the
same paragraph: Transamerica's half-weighted adjusted beginning value
(10.00% × (12,000.00 − 90.00) = **1,191.00** [S3]) via `seg_credit_base(..., "ADJ_BEGIN")`,
and the guaranteed-cap-only credit (2.00% × 11,820.00 = **236.40** [S2]) via the `cap`
argument of `index_credit`.

### Twelve deductions in the example, eleven in the ladder

The one place the notes do not close on themselves. Their processing order puts segment
maturity at **step 2** of month `m + 12`, before that month's **step 5** deduction; and a
segment is created at **step 7** of month `m`, after that month's deduction. A segment in
the running projection therefore bears deductions in months `m+1 … m+11` — **eleven** of
them — while the worked example stipulates twelve.

Both readings are defensible and neither is retunable into the other without breaking
something the notes state explicitly: charging twelve would require maturity after the
deduction, contradicting the step order; charging eleven contradicts the example's prose.
Rather than silently pick one and let the discrepancy vanish:

- the **step order governs the projection**, because it is the notes' normative
  specification and the whole account value roll-forward depends on it;
- the **example governs the engine test**, because its balance at maturity (11,820.00) is
  a stipulated input, not something the ladder computes;
- `test_first_segment_credit_reproduces_from_its_own_ladder` pins the ladder's own count
  at eleven, and `check_seg_ladder()` asserts every segment accounts for its creation
  balance exactly, so the gap cannot be closed silently in either direction.

The money is not lost either way: at month `m + 12` the matured value rolls into the fixed
account and immediately pays that month's deduction from it. Across twelve months the same
twelve deductions are taken — only eleven of them are inside the credit base.

## The ladder is degenerate under the annual-premium baseline

The notes' baseline pays **annually**, at BOM of policy month 1 of each policy year, and
sweeps **100%** of the fixed account. Nothing therefore arrives in the fixed account in
months 2–12, nothing is swept, and the "up to 12 concurrent segments" of [S3] [S4] collapses
to one segment a year. That is a correct consequence of the baseline, not a modelling
shortcut — but it would leave the ladder machinery, and the notes' first pitfall about it,
untested.

Model point 4 pays monthly instead. A segment is created every month, twelve are live from
month 12 onward, each carries its own index start level `I(m)`, and twelve separate credits
are paid each year. Model point 3 is the other end: 0% indexed allocation, so no segment is
ever created and the balance compounds at the fixed-account rate. Read points 1, 3 and 4
together and the ladder's contribution is visible rather than assumed.

## The withdrawal fee is inside `W`, not on top of it

The universal life chassis debits the account value `W + 25` and pays the policyholder `W`.
These notes read the other way: `W_t` is "gross of $25 fee" and the "withdrawal outflow =
W_t − $25 fee". So `av_pp_at(t, "BEF_FEE")` here subtracts `wd_pp(t)` alone, and
`claim_pp(t, "WITHDRAWAL")` is `wd_pp(t) − wd_fee_pp(t)`. This is a deliberate divergence
from the chassis, made because these notes restate the rule with their own convention; the
`Projection` docstring says so at the point of divergence.

The same rule applies to the death claim: the chassis nets `L(t−1)`, these notes write
`DB_t − L_t`, and `claim_pp` follows these notes.

### …and a withdrawal is not a claim

The notes write the withdrawal outflow as its own term of `CF_t`, alongside the death and
surrender legs, and the library follows that. The payment is the standalone cells
`withdrawals(t)` — `claim_pp(t, "WITHDRAWAL") × pols_if(t)`, weighted by the in-force at
BOM because a withdrawal is taken on the owner's election, not by a decrement — and it
gets a `withdrawals` column of its own in `result_cf()`.

`claims(t, kind)` therefore takes `"DEATH"` and `"LAPSE"` only; `"WITHDRAWAL"` raises.
The per-policy rule stays in `claim_pp`, which is where the fee-inside-`W_t` convention
above is stated, and `withdrawals` is its only caller. Dropping the kind from `claims`
is what keeps the `kind is None` total from counting the withdrawal twice — once in
`claims(t)` and once in the standalone cells — now that `net_cf` names both.

What is *not* here is either of the two $500 limits from the same source. The product
spec's Table 3 reads "$25 per withdrawal; minimum withdrawal $500; CSV may not fall below
$500" [S3], and neither the minimum nor the floor is enforced. `wd_pp(t)` is whatever the
model point's column says, and model point 5 deliberately asks for $200 a month — below the
sourced minimum — because a compliant $500 a month against a $6,000 annual premium empties
the policy long before the year-21 loan module that point exists to exercise. `ncsv_pp(t)`
floors at zero, not at $500. Both are limits on what a policyholder may *request*, and the
notes give no behaviour for a refused request, so the mechanics are implemented and the
limits are left to the data. They are named in **Not implemented** below and pinned by
`test_the_two_five_hundred_dollar_withdrawal_limits_are_not_enforced`.

## One pool, two claims on it, in that order

Withdrawals, new loan collateral and the monthly deduction are all sourced *fixed account
first, then pro rata across live segments* [S3]. The withdrawal and the loan collateral go
at step 3 of the monthiversary; the deduction at step 6. Both draw on the same pool — the
segments born in the previous eleven months, valued at the end of month `t − 1`,
`seg_bal_active_pp(t)` — and the obvious implementation caps each of them at that pool.

That is wrong, and it was wrong here until this pass. Capping both against the *pre-draw*
pool lets the two together take more than the segments hold. On model point 5 at month 384
the pool was $265.29, the step-3 draw took $200.00, and the step-6 deduction was then
allowed $177.38 — $377.38 out of $265.29. The segment born at month 373 went to −$112.09,
and twelve months later it paid an index credit of `0.0640 × (−112.0873) = −$7.17`: a
*negative* index credit, on an account whose floor is contractually 0%
(`cr_k = max(f, min(c, p × r))`, floor 0% [S2] [R1]).

Nothing caught it. The accounting identity in `check_seg_ladder()` still closed, because a
negative balance accounts for its creation amount as faithfully as a positive one, and
`seg_count(t)` reported zero, because it counts only segments with a *positive* balance.

So `mth_deduction_from_seg_pp(t)` is capped at `seg_bal_active_pp(t) − draw_from_seg_pp(t)`
instead: the step-3 draw has the first claim on the pool and the step-6 deduction gets what
is left. Their sum can no longer exceed the pool, no segment balance can go negative, and
no segment can pay a negative credit. `check_seg_ladder()` now asserts the last two
directly — `seg_bal_pp(t, m) ≥ 0` and `index_credit_pp(t) ≥ 0` for every month of every
model point — so the floor is a tested bound rather than a hoped-for property of the
arithmetic.

Whatever the segments cannot cover stays with the fixed account, which goes negative rather
than the deduction being silently truncated. That is deliberate: the notes charge `MD_t` in
full and hand an uncovered deduction to the grace cascade, which is not implemented — see
the next section for where that ends up.

## `check_margin()` is allowed to open up once a loan overruns the cash value

Four self-checks run on every model point: `check_av_components()` (the account value still
equals fixed account + live segments + loan collateral), `check_av_roll_fwd()` (the notes'
processing order), `check_seg_ladder()` (every segment accounts for its creation balance,
and neither a balance nor a credit is ever negative), and `check_margin()` (`net_cf`
reconciles to the expense and mortality margins). The first three hold for all five model
points.

`check_margin()` holds for points 1–4 and **fails for point 5 from policy month 384
(policy year 32)**, which is where its $6,000-a-year loan overtakes the cash value:
`ncsv_pp` floors at zero, the identity opens up by the unrecoverable debt, and
`is_shortfall(t)` starts firing. That is the exposure the notes name as key sensitivity 6 —
"heavy late-life loans plus a 0%-credit sequence can force lapse absent overloan protection
[S3]" — and the Overloan Protection Rider that would prevent it is described in the product
spec and deliberately not modeled. The test suite asserts the identity for points 1–4 and
asserts the overloan for point 5, so the gap is pinned open rather than papered over.

### And then the account value itself runs away — point 5's `result_av()` is meaningless after month 605

The margin identity is not the only thing that gives way, and the earlier draft of this
README stopped one step too soon. **No policy is terminated for insufficiency in this
model** — the grace and lapse-for-insufficiency cascade is in the *Not implemented* list
below, because the notes leave the in-grace account value treatment and the cure-payment
cash flow undetermined. So a policy that has run out of money keeps being charged: the
monthly deduction is taken in full, whatever the segments cannot cover is carried by the
fixed account, and the account value goes negative. From there it compounds, because

```
NAAR_t = max(0, DB_t × v_g − AV'_t)
```

rises one-for-one as `AV'_t` falls, and `COI_t = coi_t × NAAR_t / 1000` is charged against
`AV'_t` again next month. On model point 5:

| Policy month | Policy year | What breaks |
|---|---|---|
| 384 | 32 | loan overtakes cash value; `ncsv_pp` floors at 0; `check_margin()` opens up |
| 605 | 51 | `av_pp(605) = −241.18` — the account value turns negative |
| 912 | 76 (horizon) | `av_pp ≈ −1.3 × 10^10`, `coi_pp ≈ 6.7 × 10^8` |

So `result_av()` for model point 5 — `av_pp`, `net_amt_at_risk`, `coi_pp`,
`mth_deduction_pp` — **is not a meaningful number from month 605 onward.** Points 1–4 never
get near it: point 1's account value never falls below $8,102.

`result_cf()` is a different matter and stays finite and bounded throughout. The death
benefit is the Option A face amount — $250,000 at issue, reduced dollar-for-dollar by the
withdrawals to $70,000 by the horizon, and never lifted by the corridor, because the
corridor multiplies a *negative* account value. The death claim `max(0, DB − L)` floors at
zero once the loan passes the face, and the surrender payment floors at zero as well. The
largest single month's `net_cf` over the whole 912 months is $5,692 and the total is
−$18,374: the runaway lives entirely inside the account value, not in the cash flows.

Two fixes were available and neither was taken silently. Flooring the account value at zero
would stop the compounding, but it is a rule the notes do not give, and it would break
`check_av_components()` and `check_av_roll_fwd()` — the two identities that make the
segment bookkeeping checkable. Implementing the cascade properly needs the in-grace
treatment the notes withhold. So the behaviour is disclosed instead, here and in the model
docstring, and `test_point_5_account_value_runs_away_after_month_605` pins the boundary
month, the sign either side of it, and the finiteness of `result_cf()`, so the number
cannot drift without a test failing.

## The guaranteed basis is a Reference away

The notes distinguish class (a) contractual guarantees from class (b) current
non-guaranteed scales and say guaranteed-basis projections use class (a) only. Setting
`Projection.basis = "GUARANTEED"` switches the cap to 2.00%, the fixed account to 1.00%,
the premium load to 8%, the policy fee to $15, the per-unit charge to $0.40 in *all* years
and the COI scale to its guaranteed maximum. Key sensitivity 1 in the notes is how far
apart the two runs are; a test asserts the divergence and its direction.

## Not implemented

Named here and in the model docstring so their absence is not mistaken for an oversight:
stochastic index scenarios (the notes give lognormal parameters but simulation is a driver
around the model — `index_level` is the substitution point); cap re-declaration from an
option budget (no option pricing model, no NIER path, no target spread in the notes); the
grace and lapse-for-insufficiency cascade (the trigger and no-lapse test *are* implemented,
and so is the notes' lapse suppression while the guarantee is in effect, but the in-grace
account value treatment and the cure-payment cash flow are undetermined — with the
consequence for model point 5's account value set out above); the two $500 withdrawal
limits of spec Table 3 (minimum withdrawal $500, and a cash surrender value that may not
fall below $500 [S3]), which constrain what a policyholder may request and are left to the
model point data; the funding-stop
state of the premium persistency section (a second account value path the notes do not say
how to blend); the guaranteed floor accumulation test (explicitly a variation — the 0%
annual floor needs no shadow account); charge-funded high-cap accounts, multi-index and
multi-year segments, participating loans, the Overloan Protection Rider, face increases
and decreases, option changes, reinstatement and riders (all excluded from the baseline by
the product spec); and MEC status, which is a flag because it changes policyholder
taxation, not insurer liability cash flows.

## Standardizations used

Everything in this list is **[std]**: the 6.40% level index return of the base
deterministic run and the level index path it generates; the 5% current / 8% guaranteed
premium load; the $0.30 per $1,000 per-unit charge and its ten-year window; the $15
guaranteed policy fee; the whole COI scale and the 65% current-to-guaranteed factor; the
$25 per $1,000 surrender charge scale; the best-estimate mortality table; the rate-class
factors; the base lapse vector and its year-11 surrender-charge-expiry spike; the dynamic
lapse formula and the "underfunded = non-positive cash surrender value" reading behind the
25% no-lapse-expiry shock; the 98% premium persistency; the 3.00% charged and 2.00%/3.00%
credited loan rates; the guideline single, guideline level and 7-pay placeholders; the
$75-a-year maintenance and $150 acquisition expenses (with **no inflation**, because these
notes give none, unlike the chassis); the 2.0% premium tax; the monthiversary sweep, the
100% roll of matured value, the pro-rata deduction sourcing and the remaining-balance
credit base; routing the matured value through the fixed account; the dollar-for-dollar
Option A face reduction; treating an in-force model point's opening balance as all fixed
account, because the notes give no opening segment ladder; and the projection horizon at
attained age 121, which is itself **[unverified]**.

## Tests

`tests/test_indexed_ul_us.py` asserts every row and column of the worked example in both
index scenarios plus both variant credit bases; the anchor account value roll-forward to
the cent and the month-1 trace at full precision; one test per entry in the notes' "Known
modeling pitfalls" list; the four roll-forward self-checks across all five model points;
the in-force roll-forward; the no-lapse suppression, the surrender-charge-expiry spike and
the neutral dynamic multiplier; the loan collateral mechanics and the overloan exposure;
the guaranteed-basis divergence; that the model carries no present values or discount
curve; that the chassis name set is present; and a read → write → re-read round trip
carrying the inputs along.

Three of them exist because of the sections above, and each fails against the behaviour it
replaced or the claim it corrects:

| Test | What it pins |
|---|---|
| `test_the_two_draws_on_the_segment_pool_cannot_together_overdraw_it` | the step-3 draw plus the step-6 deduction never exceed `seg_bal_active_pp(t)`; no segment balance and no index credit is negative on any model point — the 0% floor as a bound |
| `test_point_5_account_value_runs_away_after_month_605` | the disclosed boundary: `av_pp > 0` through month 604, negative from 605, enormous at the horizon, while `result_cf()` stays finite and bounded |
| `test_the_two_five_hundred_dollar_withdrawal_limits_are_not_enforced` | model point 5's $200 withdrawal is below the sourced $500 minimum, and `ncsv_pp` floors at zero rather than $500 — the gap named in **Not implemented** |

```bash
python -m pytest tests/test_indexed_ul_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_indexed_ul_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_indexed_ul_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-indexed_ul-r1
[R4]: #uslib-indexed_ul-r4
[REG-R17]: #uslib-reg-r17
[REG-R18]: #uslib-reg-r18
[REG-R20]: #uslib-reg-r20
[REG-R21]: #uslib-reg-r21
[S1]: #uslib-indexed_ul-s1
[S2]: #uslib-indexed_ul-s2
[S3]: #uslib-indexed_ul-s3
[S4]: #uslib-indexed_ul-s4
[S5]: #uslib-indexed_ul-s5
[S7]: #uslib-indexed_ul-s7
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
