# In-Force Implementation Notes

**Status:** Draft, 2026-11-04. `ULSG_US_SEC` is [`ULSG_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year and in their grace, and policies to be
written in the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes, and how the model compiles. The suffix adds lifelib's letters to
`S`: `E` for in force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `ULSG_US_S` on another time axis, and it reads `ULSG_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced from the retrieved
> carrier documents behind the product spec: the 25% premium load and the $5.50 monthly
> per-policy charge [S3] [S7], the 2.0% guaranteed credited rate [S3] [S5] [S7], the 5.0%
> and 3.0% loan rates [S4], the 61-day grace period [S7], the return-of-premium
> percentages, anniversaries and 40%-of-face cap [S1], the in-force test on the shadow
> account net of indebtedness [S4] [S2] [S9] and the cessation of charges at attained age
> 121 [S7]. **Every shadow-account parameter is a [std] standardization**: no carrier
> publishes them and no specimen policy form was retrievable. So are the guaranteed
> maximum COI curve, which is not the 2017 CSO table, the mortality table and its
> improvement, the lapse table, the dynamic-lapse formulas, the exercise rates and every
> expense. Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/guaranteed_ul/run_sec.py            # point 1: the worked example, in force
python products/guaranteed_ul/run_sec.py 5          # point 5: S point 1 at 81, in its grace
python products/guaranteed_ul/run_sec.py --block    # every model point, summed row by row
python products/guaranteed_ul/run_sec.py 5 --cython # point 5 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about two
minutes, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer
than the build, and says so on stderr. `--build DIR` runs a build made elsewhere instead
(*The compiled model*, below). Nothing a build leaves is committed, and `.gitignore` covers
it.

The first prints, as rows `t = 0 … 11`, the cash flows, the two account values, the
guarantee diagnostics and the counts behind them for point 1, the technical notes'
worked-example policy. It is in force 300 months at the valuation date, as it is at the
start of `ULSG_US_S`'s own projection, so its rows `t = 0 … 4` are the worked example's
five months, policy months 301 to 305, here as in `run.py`: the account value closes them
at 7,679.31, 4,834.68 and 1,965.91, is exhausted at `t = 3`, and the guarantee carries the
policy from there. Its account values and guarantee diagnostics are `run.py`'s line for
line. Of its cash flows only `expenses` differ, 8.24 in the first month where `run.py`
prints 13.57, because the maintenance expense is in valuation-date dollars here, and
`net_cf` with them, −12,383.41 against −12,388.75. Three lines to the same thing for point
5:

```python
import modelx as mx
model = mx.read_model("products/guaranteed_ul/ULSG_US_SEC")
model.Projection[4].result_guar()     # point 5, the table's fifth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does, where `ULSG_US_S` takes a `point_id`: `Projection[4]` is point 5, and its
`point_id()` says so. Its four result tables are indexed by `t`, with one row per month
from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `ULSG_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `claims_rop`, `withdrawals`, `expenses`, `premium_taxes` and `net_cf` — income-positive, so the flow columns net to `net_cf` |
| `result_av()` | `ULSG_US_S`'s two account values per policy, in the columns and order of the technical notes' worked example, then the forgone deduction and the status, with zeros before issue |
| `result_guar()` | `ULSG_US_S`'s guarantee diagnostics: the net amount at risk and the cost of insurance on each account, the deduction forgone across the policies in force, the shadow account net of debt, whether the guarantee is active, the catch-up premium that would restore it and the grace counter |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths, surrenders, refund exercises and terminations in grace, in that order, and its maturities, which are always zero; then `ULSG_US_S`'s two monthly decrement rates, written 0 outside cover |

`ULSG_US_S`'s three self-checks, `check_av_roll_fwd()`, `check_sg_roll_fwd()` and
`check_margin()`, run over the same frame, and hold on every committed point.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read, so the run holds the cells of one point at
a time. Deleting it, `del model.Projection[idx]`, is not enough: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees, so the runner collects after
each release. It freezes everything alive (`gc.freeze()`) once the model and its table are
read, and again once it has asked every point for its frame, so that each collection scans
only what the block has made since. It prints where each point stands at the valuation
date, then the block's first twelve rows and the block summed into projection years,
`pols_if` the count entering each. The committed block opens with 5.43 policies, 186,024.04
of premiums and a net cash flow of 723.45. It keeps the block's sum as it goes,
compensated as pandas sums a `groupby`, so that the block is, bit for bit, the frames
concatenated and summed by `t`, as below, wherever every frame is finite: pandas' `groupby`
sum skips a NaN, and the runner's does not, so on a frame holding a NaN or an infinity
the two can part, the runner's sum turning NaN. The runner names a point by its label, and
maps it to its position: a label not in the table, a number or not, stops it with the
table's labels and no traceback.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection, the first month at attained age 121, where premiums
  and charges cease.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' `duration_months + t`, and the contract
  runs on it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1`
  and `age(t) = age_at_entry() + duration(t)`, as in `ULSG_US_S`. `BasicTerm_SE` reaches
  the same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

`ULSG_US_S` already runs this policy clock, from the first month of its own projection, and
opens its in-force point there: point 1 at 300 months, with its account value, its shadow
account, its loan and its premiums to date. What the valuation clock adds is that `t = 0`
is one instant for every point, that a point may be issued after it, and that a point in
force brings in what its past has left it: one value more than `ULSG_US_S` reads, the
months it has already spent in its grace.

Point 1 is `ULSG_US_S`'s in-force point, in force 300 months. At `t = 0` it is on the
anniversary that opens policy year 26, at attained age 85, where its 25th anniversary's
return-of-premium window falls, and its frame has 432 rows, `t = 0 … 431`. Point 7 is
`ULSG_US_S`'s point 2 restated at its month 305, five months into policy year 26: its
policy anniversaries, and with them its annual premiums, fall at `t = 7, 19, …`, and its
frame has 427 rows. Point 9 is `ULSG_US_S`'s point 2 to be issued 25 months after the
valuation date: `duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0
to 24 are zeros, its first premium, the $10,800 at the 98% premium persistency, $10,584.00,
falls at `t = 25`, and its frame has 757 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the premium months of each mode, the single premium in the issue month and the ten-pay years; acquisition in the issue month and its load on the first year's premiums; withdrawals from policy year 2; the surrender charge by policy month; the return-of-premium windows at the 20th and 25th anniversaries; the guaranteed COI scale, the mortality rate and the corridor factor at the attained age, and the improvement rate graded by it; the base lapse rate by policy year; premiums and charges ceasing, and the projection ending, at attained age 121, policy month `charges_cease_mth()` | the declared credited rate, `crediting_rate_ann(t)` and `inv_return_mth(t)`, flat as shipped; expense inflation, `inflation_factor(t) = (1 + inflation_rate)^(t // 12)`, 2.5% as shipped; mortality improvement, `mort_improve_factor(t)`, a year of it at each anniversary of the valuation date for 20 years |

**Expense inflation** keeps `ULSG_US_S`'s step by year and moves it onto `t`, so the
maintenance expense steps on the valuation anniversaries, in valuation-date dollars, for
every point alike. `ULSG_US_S` steps it on the policy year, from the policy's issue, so on
a point in force it inflates the $75 a year from the issue year: point 1's maintenance
expense is `ULSG_US_S`'s divided by `1.025^25`, about 1.854, at every `t`, since both
models step on its anniversaries. Acquisition, $300 a policy in the issue month and 90% of
every first-year premium, is charged per policy issued and not inflated, as in
`basiclife/BasicTerm_SE`: `ULSG_US_S` charges it on the policies in force in the issue
month, which are the policies issued. The claim expense, $300 a death, is not inflated in
either model.

**Mortality improvement** runs from the start of `ULSG_US_S`'s own projection: the factor
is 1.0 in its first year and gains a year of improvement on each anniversary of that start,
for at most 20 years, each year's at the rate graded at the attained age a year before,
1.0% to attained age 85 and 0 from 95. This model keeps both cells' formulas, so
improvement runs from the valuation date, for every point of a block, which is what
`ULSG_US_S` already does for its own in-force point 1: the years accrue at `t = 12, 24, …`,
in the same months for every point, whatever its own anniversaries. Between them the factor
moves only where a graded rate it reads moves, at attained ages 85 to 95, and those step on
the policy's anniversaries: on point 7, valued mid-year at attained age 85, it moves at
`t = 12, 19, 24, 31, 36, …`. A point written `k` months after the valuation date takes the
improvement of the valuation years before its issue too, each graded at the age its cohort
had reached in that year: point 9 dies at 0.9801 of the table's rate in its issue month,
`t = 25`, where `ULSG_US_S`'s point 2, issued at its own `t = 0`, dies at the table's rate.

So a point restated at `ULSG_US_S`'s month `d`, or written later, continues its S point
per policy, but its counts part from S's by design: it improves from its own valuation
date, and S's point from S's `t = 0`. On the committed points the account value and the
shadow account per policy are `ULSG_US_S`'s exactly, while the count of point 6,
`ULSG_US_S`'s point 2 restated at 240, is up to 0.0271 of a policy apart and its `net_cf`
up to 342.78. The tests compare the counts with improvement and inflation set to 0 in both
models, and hold each of the two to the valuation clock, at its shipped value, in a test of
its own (*Tests*, below).
The declared credited rate is an economic input too, read at `t`, and ships flat at 3.50%,
so its clock shows in no number.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
n = len(model.Data.model_point_table())
frames = [model.Projection[i].result_cf() for i in range(n)]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`ULSG_US_S` computes, whatever the point's count. On `ULSG_US_S`'s three new-business
points every cash flow and every count agrees, and so does every other cell the two models
share, at every argument `ULSG_US_S`'s own sweep evaluates, but three whose meaning
changed: `pols_if_init()`, now the count already in force at the valuation date, 0 for new
business; `model_point()`, a row of another table; and `result_pols()`, which gains
`pols_new_biz`. The four cells of `ULSG_US_S`'s funding-premium solve are not in this model,
and compiling replaced `coi_rate_scale` by a schedule number, spelled `status` as a code and
split `claims` into its kinds (*Departures*, below). On point 1, `ULSG_US_S`'s in-force
point, which both models open at the valuation date, the projection is `ULSG_US_S`'s from `t
= 0` on, in every cell the two share but `inflation_factor` and the cells it reaches, the
expenses, the expense margin, `net_cf` and `result_cf()`; with inflation set to 0 in both,
every cell agrees.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `ULSG_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and seven of its columns are the in-force interface:
`basiclife/BasicTerm_SE`'s two, and five that open an in-force policy's state. Every amount
is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars, 0 or more | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value, its loaned part included |
| `sg_pp_init` | dollars, of either sign | the start of month 0 | the shadow account, which is never floored: below 0 it measures the catch-up shortfall |
| `loan_bal_init` | dollars | the start of month 0 | the policy loan outstanding, the interest accrued to then included |
| `cum_prem_init` | dollars | the start of month 0 | the premiums paid from issue to policy month `duration_mth − 1`, withdrawals not netted, which the return-of-premium refund reads |
| `grace_mth_init` | whole months, an int | the start of month 0: the counter after policy month `duration_mth − 1` | the months already spent in the grace period, 0 for a policy not in grace; at most `grace_months − 1`, 1 as shipped |

The five state columns are 0 on a point issued at or after the valuation date: it is issued
with no account value, no shadow account, no loan, nothing paid and no grace.
`av_pp_init`, `sg_pp_init`, `loan_bal_init` and `cum_prem_init` are `ULSG_US_S`'s own
columns, and the technical notes' `av_init`, `sg_init`, `loan_init` and `cumprem_init`:
they already measure the balances entering `ULSG_US_S`'s first month, so they keep their
names. `grace_mth_init` is named for the cell it opens, `grace_mth`, as they are for
theirs; the technical notes give the counter no model point attribute, and open it at 0.
The shadow account is state, carried in its own column like the account value: it is the
policy's own balance, not a path a model could recompute from issue.
`UL_US_SEC`'s other state columns would open no cell here. The face never moves, since a
withdrawal reduces the two accounts and not the face, and the product has neither a free
withdrawal allowance nor a 7-pay test, which the notes put out of the model: so there is no
`sum_assured_init`, `wd_used_year_init` or `is_mec_init`. Nor is there a loan account, as
in `VUL_US_SEC`: the loaned part of the account value is the debt itself. No quantity of
the product is read at the last anniversary, so none needs a column at a second instant.

| `ULSG_US_S` | `ULSG_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 or more, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `av_pp_init`, `sg_pp_init`, `loan_bal_init`, `cum_prem_init` | the same | `ULSG_US_S` already opens its in-force point from them |
| — | `grace_mth_init` | `ULSG_US_S` reads the grace counter of the month before its frame as 0 |

On the twins the new column takes what `ULSG_US_S` itself assumes, 0, so each twin opens as
its S row does: point 1 with the worked example's account value of 2,400.00, shadow account
of 118,000.00, no loan, 270,000.00 of premiums paid, 25 annual premiums of $10,800, and no
grace.

The columns carried over are read as `ULSG_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the mode and the withdrawal excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `ULSG_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the face, level for the life of the policy, on which the per-unit charges and the surrender charge are quoted |
| `guarantee_age` | an attained age, 90 to 121 | the guarantee elected at issue; 121, the lifetime election, sets the lifetime lapse multiplier |
| `premium_type` | `LEVEL`, `SINGLE` or `TEN_PAY` | the pattern over the frame: a single premium falls in the issue month alone, ten-pay's in the first ten policy years |
| `premium_pp_ann` | dollars a year, the scheduled premium, or the single premium on `SINGLE` | issue: the premium the policy was issued on, which a point in force goes on paying |
| `premium_mode` | `A`, `S`, `Q` or `M` | the mode over the frame; its instalments fall on the policy clock |
| `load_prem_rate` | a fraction of each premium | the base premium load, contractual |
| `prem_persistency_override` | a probability, or blank | a pin of the point, which holds in every month (below) |
| `coi_rate_dp` | decimal places, or blank | a pin of the point, which holds in every month (below) |
| `wd_pp` | dollars a month | the withdrawal taken in every month of cover from policy year 2; 0 on every shipped point |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `rop_elected` | a flag | whether the return-of-premium endorsement applies |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

**The premium is an input.** It is fixed at issue, and a policy in force goes on paying
the premium it was issued on, whatever its shadow account now stands at: so the model reads
it from `premium_pp_ann`, as `basiclife/BasicTerm_SE` reads its premium from a table.
`ULSG_US_S`'s funding-premium solve, which finds the level premium that keeps the guarantee
in force from issue, stays `ULSG_US_S`'s (*Departures*, below). On its point 2 it finds
10,803.93, where the column holds the technical notes' `P*`, 10,800.00.

**The two pins**, `prem_persistency_override` and `coi_rate_dp`, are rules of the point,
not state, and `ULSG_US_S` applies each in every month of its frame. So does this model,
and a point restated in force or written later keeps its S point's pins. Point 1 and point
5, the worked-example policy restated 81 months on, pin both: the premium persistency at
1.00 and the declared COI scales to 2 decimals per $1,000, which reconciles the notes'
worked example with their own factor rule. Every other committed point leaves both blank,
and takes the 98% persistency of a level payer and the scales at full precision.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the in-force columns are present, and so is every column of `ULSG_US_S`'s own that the
  projection reads as a number or a flag: `age_at_entry`, `sum_assured`, `guarantee_age`,
  `premium_pp_ann`, `wd_pp`, `load_prem_rate`, the two pins, `has_surr_charge` and
  `rop_elected`: "model_point_table_sec.csv has no grace_mth_init column";
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more: "model_point_table_sec.csv: duration_mth must be -120 or
  more, a policy issued at most 120 months after the valuation date; it is not at point_id
  [9]". Future new business is written over a horizon, `Data.future_horizon_mth`, 120
  months as shipped, so that no frame runs longer than the projection from issue plus ten
  years: 1,356 months at issue age 18, the youngest the product issues, and 1,032 at 45,
  the youngest the shipped COI scale serves. Set to 0, the Reference refuses future new
  business altogether, and a negative horizon is itself refused;
- `age_at_entry` and `guarantee_age` are each a whole number of years, 0 or more: the
  projection takes the `int()` of each, where `ULSG_US_S` would truncate a guarantee age of
  95.5 to 95;
- `sum_assured` is a number above 0, the face every policy holds, and each of
  `premium_pp_ann` and `wd_pp` a number, zero or more;
- `load_prem_rate`, the share of each premium the load takes, is a number from 0 to 1:
  "model_point_table_sec.csv: load_prem_rate must be a number from 0 to 1; it is not at
  point_id [3]". Past 1 the account would be credited a net premium below 0, which the
  account value's floor at zero absorbs: at a load of 1.5 `ULSG_US_S`'s account-value and
  margin checks fail on each of its points;
- `prem_persistency_override` is blank, where the point takes the rule, or a number from 0
  to 1, a probability, and `coi_rate_dp` is blank, where the point quotes its scales
  exact, or a whole number of decimal places, 0 or more, where `ULSG_US_S` would take the
  `int()` of 2.5;
- `has_surr_charge` and `rop_elected` are each `True` or `False`, as pandas reads those
  words, in any case, so that `TRUE`, `false` and `FaLsE` decode, and project, as `True`
  and `False` do. A blank, a number, 1, 0, 1.0 and 0.0 among them, or any other text is
  refused: one such value turns the whole column into text, where `"False"` and `"0"` are
  true strings, so that every point would read as carrying the flag;
- `av_pp_init` is a number, zero or more. A balance is never negative in force.
  `ULSG_US_S` lets the account value close a month below zero with a loan on an exhausted
  account, through the loaned part's lower credited rate, so the message says what to do:
  restate such a point no later than the last month its account value is still zero or
  more;
- `sg_pp_init` is a number, of either sign: the shadow account is never floored;
- `loan_bal_init` and `cum_prem_init` are each a number, zero or more;
- `grace_mth_init` is a whole number of months, 0 or more;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros:
  "model_point_table_sec.csv: grace_mth_init must be 0 on a policy not yet in force,
  duration_mth 0 or less; it is not at point_id [9]".

The text columns, `sex`, `rate_class`, `premium_type`, `premium_mode` and
`surr_charge_id`, are keys and codes, which the projection decodes or joins on at their
first read, as `ULSG_US_S` does: a pattern or a mode no decode knows raises `ULSG_US_S`'s
message, and a class or a schedule its table lacks raises at its first read. The grace
counter is not held to the account value: `ULSG_US_S` can carry a positive account value
in grace, once the loaned part earns more than the unloaned, so no such rule could be
right.

Three kinds of point read, but `proj_len()` refuses each, naming the point, because each
is a rule of the product, read from `Projection`'s References, not the table's. It checks
them in this order:

- a point to be issued at or past attained age 121, which would never be in cover: "point_id
  9: age_at_entry 121 is at or past charges_cease_age, 121: a policy issued there would
  never be in cover". The age is checked first, so that a point issued past it within a
  year, whose frame would also end before the valuation date, is refused by its age, not
  by a policy month below 0. A point to be issued at attained age 120 is a policy, with a
  year of cover;
- a point at or past the end of the projection at the valuation date,
  `duration_mth ≥ 12 × (121 − age_at_entry)`: "point_id 3: duration_mth 732 is at or past
  the end of the projection, policy month 732, attained age 121";
- a point whose grace expired before the valuation date, `grace_mth_init ≥ grace_months`:
  "point_id 5: grace_mth_init 2 is at or past grace_months, 2: the grace expired before the
  valuation date, so the policy lapsed then, with no value". A policy whose grace has
  expired lapsed at the start of the next month, with nothing to pay, and is not in force,
  and the in-force interface carries no lapse latch.

So a loop over the block meets such a row only when it reaches it, after projecting the
points before it. `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

The assumption tables are checked too, each once, in the `Data` cell its reader in
`Projection` takes its extent or its count from. The tables read at an attained age or a
policy year take their extents from `corridor_age_first()` and `corridor_age_last()`,
`mort_age_first()` and `mort_age_last()`, `lapse_last_year()` and, for `coi_rates.csv`,
whose sex and rate class cells are numbered as schedules, `coi_schedules()`, which checks
the table, and `coi_rate_last_ages()`, the last attained age of each schedule, beyond which
each reads its nearest row. The COI scale is clamped at its last age alone, as in
`ULSG_US_S`: an attained age below its cell's first raises at the first read. The key column
is read by
value, so a year written `5.0` is 5, and a key that is blank, text or not a whole number is
refused, naming the file, the column and the lines it is on. So are keys that do not run
one row an age or a year, without a gap or a repeat, policy years from 1, the message
naming each key that repeats, with its lines, and each that is missing: "lapse_table.csv:
the policy years must run from 1, one row a year, without a gap or a repeat; no line holds
policy_year 5", and, inside a cell of the COI scale, "coi_rates.csv: the ages of each sex
and rate_class must run one row an age, without a gap or a repeat; at ('M', 'StdNT'), no
line holds age 61". So is a blank sex or class in the COI scale, and a value that is blank,
text or infinite. A lapse or mortality rate is a probability, held to 0 to 1, since past 1
the monthly rate `1 − (1 − q)^(1/12)` has no real value: "mort_table.csv: mort_rate must be
a number from 0 to 1; it is not on line [44]". A class factor, a guaranteed COI rate and a
surrender charge are held to 0 or more, since below it each projects negative deaths, a
credit for the insurance or a surrender charge that rises once its schedule has run off.
A COI rate is a charge per $1,000 of net amount at risk a year, not a decrement: the
shipped scale is above 1 at every age it charges and 0 at 121, where charges cease, and the
current monthly rate passes 1 from attained age 69, as it should. A corridor factor is held
to 0 or more too, a multiple of the account value that the statute's applicable
percentages hold to 100% or more: one below 1 only makes the corridor bind later, and one
below 0 would leave `db_pp`'s floor on the account value the one thing between an account
below 0 and a death benefit above the face. `class_count()` and
`surr_charge_count()` check the class factors and the surrender-charge schedules, for the
per-point joins that read them, the same way: a class or a schedule blank or on two rows,
and a factor or a charge that is not a number, or is below 0. `surr_charge_count()` also
refuses a run-off that is not a whole number of years, 1 or more, which the projection
divides the charge by, where `ULSG_US_S` divides by zero at 0: "surr_charge_table.csv:
runoff_years must be a whole number of years, 1 or more; it is not on line [2]".
`rop_count()` checks the return-of-premium windows, which are read by membership of their
anniversaries: an anniversary that is blank, text, not a whole number of years, 1 or more,
or on two rows, is refused, and so is a refund ratio or an exercise rate outside 0 to 1.

Each reader asks for its extent or its count before it reads a value, so a projection meets
the checks first. `ULSG_US_S` takes each extent from the key column as pandas reads it,
where a blank key is a missing value the extent skips: the table is cut short, and every
later year or age reads the last good row, without a word. A blank value is a missing value
to it too, which shows in its flows or is lost in a `min` or a `max`: a blank lapse rate
reaches the lapse rate's floor and is read as it, 0.3%, a blank corridor factor reads as no
corridor, a blank surrender charge as none, and a blank COI rate reaches the account
value's floor at zero, which reads it as an exhausted account. Here the cap on the
mortality rate, `min(q, 1.0)`, keeps a blank base rate or class factor missing, as
`ULSG_US_S`'s own does, and each of them is refused before any rate is read.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`ULSG_US_S` and its table by `tests/sec_support.py`, from the `ULSG_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `ULSG_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py ULSG_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 | twin | S point 1 | the technical notes' worked-example policy, in force 300 months, on the anniversary opening policy year 26, at attained age 85, with 2,400.00 of account value, a shadow account of 118,000.00 and 270,000.00 of premiums paid: its `t = 0 … 4` are the worked example's policy months 301 to 305, and its 25th anniversary's window falls at `t = 0` |
| 2–4 | twin | S points 2–4 | issued at `t = 0`: `ULSG_US_S`'s new business, the same policy from issue on the notes' behavioural basis, the lifetime guarantee funded by one premium of $152,300, and a guarantee to attained age 90, underfunded at $6,000 a year, with no endorsement |
| 5 | derived | S point 1 at S month 81 | a month into its grace, in force 381 months, at attained age 91, with 0.428726 in force, no account value, a shadow account of −1,365.21 and a grace counter of 1: it lapses at `t = 1` |
| 6 | derived | S point 2 at S month 240 | on its 20th anniversary, whose 50% window falls at `t = 0`: 911.21 of account value and 211,680.00 of premiums paid |
| 7 | derived | S point 2 at S month 305 | five months into policy year 26, at attained age 85, its account value exhausted and the guarantee carrying it on a shadow account of 244,383.19: its anniversaries fall at `t = 7, 19, …` |
| 8 | derived | S point 3 at S month 731 | its last covered month, at attained age 120, with 4.012e-10 of a policy: a one-row frame, whose `t = 1` is the month its survivors are carried into |
| 9 | future | S point 2, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `ULSG_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `ULSG_US_S` carries into it, each column read as
`ULSG_US_S`'s own formulas read it: the account value as `av_pp_at(d, "BEF_PREM")`, the
shadow account as `sg_pp_at(d, "BEF_PREM")`, the loan as `loan_bal_pp_at(d, "BEF_INT")`, the
premiums to date as `cum_prem_pp(d − 1)` and the grace counter as `grace_mth(d − 1)`. So the
row continues the S projection from there, per policy: point 5 opens with 0.428726 policies,
and point 8 with 4.012e-10. A month by which `ULSG_US_S` has lapsed the policy cannot be
restated, since no policy is in force there to restate: the generator refuses it, naming
the point and the month (*The opening state*, below). Each pin is the S point's. A derived
row's `policy_id` is the S row's with the month appended, `GUL-000001-M81`, and a future
row's carries the months to issue, `GUL-000002-F25`. Row `t` of a generated point is month
`t + source_mth` of its S point. All nine are on the anchor cell M60 / StdNT / $500,000,
because the illustrative COI scale covers that cell alone, from attained age 45, so a point
on any other sex or class, or issued younger than 45, needs `coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
the three timings that `ULSG_US_S` already names, each an int Reference named as the string
`ULSG_US_S` passes, so that a timing, like every argument, is a C number when the model
compiles:

- `BEF_NB = 0`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it, or 0 once the policy has lapsed for insufficiency;
- `BEF_DECR = 1`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_MAT = 2`, the count before any maturity, `ULSG_US_S`'s meaning: the `BEF_DECR`
  count, since the contract never matures and no event of the month separates the two.

Any other timing raises, the accounts' six and the loan's one among them, which follow in
the same numbering, `BEF_PREM = 3` to `BEF_INT = 9` (*The compiled model*, below).
`ULSG_US_S`'s cell of the name returns `pols_if(t)` for every timing, and nothing calls it.
`BEF_NB` is the one timing this model gives a meaning of
its own, `basiclife/BasicTerm_SE`'s, and the two models differ in it alone, in the issue
month: there `ULSG_US_S` counts the issued policies, and this model counts them as new
business, not yet in. As in `UL_US_SEC` and `VUL_US_SEC`, `basiclife/BasicTerm_SE`'s
`"BEF_MAT"`, the count at the start of the month before its new business, is not adopted:
the name keeps its S model's meaning.

The month's decrements are `ULSG_US_S`'s, in its order, all at the end of the month: deaths,
then surrenders out of the survivors, then return-of-premium exercises out of those left,
and, in the month before a grace expires, every policy still left, `pols_lapse_grace(t)`,
which terminates with no value. The lapse latch, `is_lapsed(t)`, then shuts from the next
month, and the count is 0 from there.

Every chain of calls from month `t` back to `t_entry()` is one cell a month. `BEF_NB`
forms the survivors of month `t − 1` itself, as its own value at `t − 1` plus that month's
new business, less that month's four decrements in `ULSG_US_S`'s order. Each account's
opening balance forms the previous month's close the same way, the same operations in the
same order as the closing cell `ULSG_US_S` calls for: `av_pp_at(t, BEF_PREM)` from its own
value at `t − 1` and month `t − 1`'s net premium, withdrawal and fee, expense charges, cost
of insurance, zero floor and interest, where `ULSG_US_S`'s account value ran through six
cells a month; `sg_pp_at(t, BEF_PREM)` likewise, where `ULSG_US_S`'s shadow account ran
through six; and `loan_bal_pp_at(t, BEF_INT)`, a month's interest on its own value at
`t − 1`, where `ULSG_US_S`'s loan ran through two. The premiums to date call themselves at
`t − 1`, and the grace counter and its latch are one chain between them, as in
`ULSG_US_S`. The mortality improvement factor reads itself a year back, a chain of one cell
a year: past 20 years, from `t = 252` on, it is the factor of month 240, so it is at most 22
cells deep.

On a model just read, a cold `net_cf` in the last month of point 1's 432-month frame runs
447 cells deep, against 2,111 for `ULSG_US_S`'s point 1: 16 cells above the chain back to
`t_entry()`. The other committed points run 15 to 18 above theirs: 747 cells on points 2,
3, 4 and 9, each on the books for 732 months. At the longest cover the contract allows,
issue age 18 and 1,236 months, it runs 1,253 deep at the valuation date and 1,256 issued
120 months after it, 18 and 21 above the chain: every chain stops at the issue month, but in
its first month the mortality of a point issued later reads the improvement factor of the
valuation years before its issue. Compiled, that call runs on the C stack (*What a
compiled run needs*, below). Each chain's head called alone, on a read of its own with
every chain cold, the loan's, the premiums', the account value's, the shadow account's, the
grace counter's with its latch and the count's, runs at most 12 cells above its chain on
the committed points, the count's the deepest, which runs 14 above at the longest cover at
the valuation date and 17 issued 120 months on; the improvement factor asked alone runs at
most 27 levels, from `t = 252` on. Each report evaluates its columns in ascending `t`, and
on a model just read the committed points' four reports and three checks run that way
under a recursion limit of 17, and `ULSG_US_S`'s under 14. A point issued 120 months on
needs 19, since its first month reads the improvement factor of the ten years before it.
Exported by modelx, with the recursion limit set after the import, the cold `net_cf` of the
last month needs a limit of 918 on point 1, 1,518 on points 3 and 9, and 2,526 at the
longest cover, issued now or 120 months on, and the ascending sweep 58, against 3,929 to
5,977 and 52 for `ULSG_US_S`'s points.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `ULSG_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_rop(t) + pols_lapse_grace(t) + pols_maturity(t)
```

at every `t` of every frame, the month of a lapse and every month after it included, and
`pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < charges_cease_mth()`, where
`charges_cease_mth() = 12 × (charges_cease_age − age_at_entry)` is `ULSG_US_S`'s frame from
issue, the first month at attained age 121. Outside it, before issue and from
`t = proj_len()` on, every count, balance, premium, withdrawal, charge, decrement rate,
decrement, claim and cash flow is zero and every flag false, the grace counter and the
return-of-premium anniversary are the int 0, and `status` says why: `PRE_ISSUE` before
issue and `CEASED` from `t = proj_len()` on. Only the two clocks, the inputs read on the
valuation clock and the dynamic lapse multiplier's neutral 1.0 hold values there, and the
month after the frame holds three exceptions more, below. No count evaluates a decrement
rate there, and no table is read at a policy year, an attained age or an anniversary the
policy does not have: `sum_assured_at`, `prem_persistency`, `premium_pp`, `cum_prem_pp`,
`wd_pp`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `sg_coi_pp`, `maint_fee_pp`,
`sg_maint_fee_pp`, the timings of the two accounts and the loan, `surr_charge_rate`,
`mort_rate`, `lapse_rate_base`, `lapse_rate`, the four decrements and `expenses` are zero,
`is_premium_mth` false and `grace_mth` and `rop_anniversary` 0, before any table or rate is
read, and every other value is zero through them. `lapse_rate_dyn_mult` is 1.0 there,
before it reads the guarantee or the account value. Each table read at a policy year, an
attained age or an anniversary has one reader keyed by it, called inside cover only, so on
point 9, whose policy year is −2 at `t = 0`, no reader is asked for a policy year below 1
or an attained age below 60. The mortality improvement rate is the one cell read at an
attained age before issue, on a point written later, and it reads no table: it grades the
improvement of the valuation years before issue at the age the cohort has reached in each.

**The end of the projection.** The frame ends at `charges_cease_mth()` because premiums and
charges cease at attained age 121, not at an event of the contract, whose cover continues
there [S7]. The shipped mortality table reaches 1.0 at attained age 120, but improvement
takes the rate below it: on a point issued at or after the valuation date at attained age
60, 20 years of 1% leave the rate at attained age 120 at 0.817907, and on point 1, whose
years of improvement fall from attained age 85 on, at 0.946302. So lives can survive the
last month, and `ULSG_US_S`'s roll-forwards read them: `check_av_roll_fwd()` and
`av_change()` read the account value in force entering month `t + 1`, and
`pols_lapse_grace()` the lapse latch of month `t + 1`, which in the last month is
`t = proj_len()`. So the three opening values read there, the count carried in
(`pols_if_at(t, BEF_NB)`, and through it `pols_if(t)`), the account value carried in
(`av_pp_at(t, BEF_PREM)`) and the latch (`is_lapsed(t)`), are defined for
`0 ≤ duration_mth(t) ≤ charges_cease_mth()`: in the month after the frame they are the
survivors of the last month, the account value they carry and the latch the last month
leaves, `ULSG_US_S`'s own values there. Everything else is zero or false there, the shadow
account included, which no cell reads there, and the expenses, which would otherwise fall
on the carried count. Nothing reads past it: `av_change()`, `pols_lapse_grace()` and the
three checks' residual cells, which read `t + 1`, are zero outside cover before they read
it. At the shipped assumptions the survivors at `proj_len()` are 3.48e-10 of a policy on
the twin of point 3, `ULSG_US_S`'s own, and 0.0 on every other committed point: points 1,
2, 4, 5, 6, 7 and 9 lapse before the end, and point 8, whose improvement restarts at its
valuation date, dies in its one month at the table's 1.0.

**Rates stay rates.** The annual mortality rate is capped at 1.0, as in `ULSG_US_S`,
`min(q, 1.0)` with its bound second, so that a missing input stays missing. On no committed
point does the product pass 1, since all are on StdNT, whose factor is 1.0: the cap binds
on the tobacco classes, whose factors take the table past 1, first on StdTob at attained
age 107, 1.75 × 0.582849, at an A/E of 1.0 with improvement off.
The annual lapse rate keeps `ULSG_US_S`'s floor of 0.3% and cap of 50%, each bound written
first, `min(lapse_rate_cap, max(lapse_rate_floor, rate))`, and `Data` holds each base rate
to 0 to 1, so the rate stays a probability while `lapse_rate_cap` is at most 1. On the
committed points the rate before its bounds is at most 0.04, so the cap never binds there,
while the floor binds from policy year 21 on, where the base rate is 0.75% and the
multipliers take it below 0.3%.

## The opening state

`ULSG_US_S` opens its in-force point 1 from four columns, the account value, the shadow
account, the loan and the premiums to date entering its first month, and reads the grace
counter of the month before its frame as 0. The worked example's policy is not in grace at
its policy month 300, so point 1 needs no more, and its twin opens the same way. A policy
valued in any month of its life needs all five columns, each what `ULSG_US_S` carries into
that month. The committed points show what each changes, each compared with the same row
read with the column at what `ULSG_US_S` assumes or at 0, or, for the shadow account,
floored at zero as the account value is:

- **`grace_mth_init`.** Point 5 is `ULSG_US_S`'s point 1 a month into its grace, at its
  month 81. It carries a counter of 1, which its first month, whose deduction fails again,
  advances to 2: the grace has run its two months, every policy left at the end of month
  0, 0.423179 of them, terminates, and `pols_if(1)` is 0.0, as `ULSG_US_S`'s `pols_if(82)`
  is. Read with the counter at 0, as `ULSG_US_S` reads the month before its frame, the grace
  would open afresh at `t = 0` and the policy would lapse a month late, with 0.423179
  policies still in force at `t = 1`.
- **`sg_pp_init`.** The same row's shadow account is −1,365.21, below zero: the guarantee
  has failed, and the negative balance is the catch-up shortfall. Month 0's charges take
  it to −5,551.43, so the catch-up premium that would restore the guarantee is 6,034.16.
  Floored at zero, as the account value is, the shadow account would close month 0 at
  −4,180.11 and the catch-up premium would be 4,543.60.
- **`cum_prem_init`.** Point 1 has paid 25 annual premiums of $10,800, 270,000.00, and its
  25th anniversary's window falls at `t = 0`: the refund there is the premiums paid,
  month 0's included, 280,800.00, capped at 40% of the face, 200,000.00, so the 0.099303 of
  a policy that exercises is paid 19,860.68 and `net_cf(0)` is −12,383.41. With the column
  at 0 the refund would be month 0's premium alone, 10,800.00, the refunds 1,072.48 and
  `net_cf(0)` 6,404.80. Point 6, on its 20th anniversary, has paid 211,680.00, and its 50%
  window refunds 111,132.00 a policy at `t = 0`; with the column at 0 it would refund
  5,292.00.
- **`av_pp_init`.** Point 6 also holds 911.21 of account value entering month 0, so that
  the account closes the month at 7,098.16, the cash surrender value of a policy that
  surrenders then, where read as 0 it would close at 6,181.24.

`loan_bal_init` is 0 on every committed point, as on every point of `ULSG_US_S`'s. A loan is
read where `ULSG_US_S` reads it: the loaned part of the account value earns the loan credit
rate, both of the guarantee's tests net it, and every claim deducts it.

**A row in its grace, and none after a lapse.** At the shipped assumptions `ULSG_US_S`'s
point 1 exhausts its account at its month 3, the guarantee carries it through month 79,
its grace opens at 80, and it lapses at the start of 82, with no value:

| S month | `pols_if` | `grace_mth` | `is_lapsed` | `sg_pp_at(t, "BEF_PREM")` | `status` |
|---|---|---|---|---|---|
| 79 | 0.439333 | 0 | `False` | 6,871.71 | `IN FORCE - GUARANTEE` |
| 80 | 0.434093 | 1 | `False` | 2,779.48 | `GRACE` |
| 81 | 0.428726 | 2 | `False` | −1,365.21 | `GRACE` |
| 82 | 0.0 | 0 | `True` | −5,551.43 | `LAPSED` |
| 83 | 0.0 | 0 | `True` | −9,756.36 | `LAPSED` |

A row restated at 80 carries a counter of 0, and one at 81 the counter of 1 that point 5
carries, `ULSG_US_S`'s `grace_mth(80)`; each lapses where `ULSG_US_S` does, at `t = 2` and
`t = 1`. No row is restated at 82 or later. The policy has lapsed: `ULSG_US_S`'s count there
is 0 and its latch shut, and the in-force interface carries no latch, since a lapsed policy
is not in force. So the generator refuses every month by which `ULSG_US_S` has lapsed the
policy, naming the point and the month, and `proj_len()` refuses a hand-made row whose
counter is at or past `grace_months`, as a row at 82 would carry 2. A row at 83 would carry
a count of 0 and a counter of 0, since `ULSG_US_S`'s counter reads 0 once the policy has
lapsed, and the model's rules accept that as a point with no policy in force: so it is the
generator, which reads `ULSG_US_S`'s latch, that refuses it. Points 2 and 4 lapse at their
months 504 and 236, and the last months each can be restated at, in its grace with a
counter of 1, are 503 and 235.

A counter carried in resets where `ULSG_US_S`'s does, in the first month whose deduction no
longer fails: a grace can end without a lapse where a scheduled premium falls due and
carries the deduction. `ULSG_US_S`'s point 4 paying $6,150 a year, a variant the tests use,
enters its grace at its month 239, and the anniversary premium at 240 cures it. Restated at
240 with a counter of 1, it resets at `t = 0` and stays in force; restated at 243, where its
second grace is a month old, it lapses at `t = 1`. With improvement and inflation set to 0
in both models, each is `ULSG_US_S`'s projection from there, cell by cell.

## Departures from ULSG_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state on a
point in force, and each cell that turns `t` into a policy year, an attained age or an
anniversary answers for the months outside cover. Of `ULSG_US_S`'s 139 cells in
`Projection`, 55 are unchanged, 34 have a new docstring only, most of them to say what `t`
now counts, and 46 are rewritten; four, the funding-premium solve, are removed, none is
renamed, and 25 cells are new, 160 in all. A cell of `ULSG_US_S`'s that this model lacked
would fail the twin identity, which names each of the four with its reason. `ULSG_US_S`'s
References `solve_tol`, `solve_max_doublings` and `math`, which only the solve and the
checks' `math.isclose` read, are dropped. Of `Data`'s nine cells, `model_point_table` is
rewritten to check the table as it reads it, three readers have their `read_csv` call
wrapped and `mort_table` its docstring; nine cells are new, 18 in all, and so is the
Reference `future_horizon_mth`, 120. Compiling then changed how each cell reads its inputs
and spells its codes, and no number (*The compiled model*, below): in `Projection` it
replaced one cell, `coi_rate_scale`, by a schedule number, and added five more, 165 in all;
of `ULSG_US_S`'s cells it changed the signature of one, `claims`, and the type of one,
`status`, which returns a code. The twin identity exempts `coi_rate_scale` and `status`,
each with its reason, and compares `ULSG_US_S`'s `claims(t, None)` with the total
`claims(t)`. In `Data` it rewrote `coi_rate_last_ages`, a Series at stage E, as an array
checked by the new `coi_schedules()`, and added 38 cells, 56 in all, and widened the checks
of the model point table and of the three age tables. The cap on mortality, `min(..., 1.0)`,
is `ULSG_US_S`'s own and no departure, and so are the shadow account never floored, the
lapse rate's two bounds in `ULSG_US_S`'s order and improvement from the start of the
projection, which here is the valuation date.

| Cells | `ULSG_US_S` | `ULSG_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `charges_cease_mth` | `12 × (charges_cease_age − x) − duration_mth_init()`, the months from the first projected month | `charges_cease_mth() − duration_mth_init()`, the months from the valuation date; raises, in this order, for a point to be issued at or past attained age 121, one at or past the end of the projection, one whose grace has expired and one issued below `issue_age_min`, 18 | `charges_cease_mth()` is new and is `ULSG_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left, or none in cover, has no frame, a policy whose grace has expired lapsed before the valuation date, and the compiled caches hold the contract's frames alone |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse`, `pols_rop`, `pols_lapse_grace` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, BEF_DECR)`, from `t_entry()`; `BEF_NB` the count before the month's new business, formed from the month before in the cell itself, and `BEF_MAT` the `BEF_DECR` count, as in `ULSG_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month; the chain is one cell a month |
| `av_pp_at`, `sg_pp_at`, `loan_bal_pp_at` | `av_pp_init()`, `sg_pp_init()` and `loan_bal_init()` at `t = 0`, then the previous month's closing cell: chains of six cells a month, six and two | the same openings at `t_entry()`, then the previous month's close formed in the cell itself, `ULSG_US_S`'s arithmetic in its order, its floor written first; every timing zero outside cover but the account value's opening, carried into `t = proj_len()` | Every chain one cell a month, since a compiled model runs it on the C stack |
| `cum_prem_pp`, `grace_mth`, `is_lapsed` | opened at `t = 0` from `cum_prem_init()`, a counter of 0 and a latch that is false | opened at `t_entry()` from `cum_prem_init()` and `grace_mth_init()` on a point in force, and from the issue values on any other; the latch false at `t_entry()`, and carried into `t = proj_len()` | A policy in force brings in its premiums to date and the months it has spent in grace; a policy that has lapsed is not in force |
| `premium_freq`, `is_premium_mth`, `prem_persistency`, `premium_pp`, `lapse_rate_pattern_mult` | branches on the text of `premium_type()` and `premium_mode()` | branches on three decodes, `is_level_premium()`, `is_single_premium()` and `is_ten_pay_premium()`, each read from a 0/1 vector `Data` decodes from the column, and `premium_freq()` read from an int vector of payments a year, 0 for a mode no decode knows | No projection cell reads text, and none calls a label accessor. The label accessors stay, for reporting, and a value no decode knows still raises `ULSG_US_S`'s message where it is read, so that a SINGLE point, which never reads its mode, projects whatever it is |
| `prem_persistency`, `wd_pp` | the model point's `prem_persistency_override` and `wd_pp` columns read in the monthly cell, the pin through `pd.isna` | read once a point: the pin as a value and a flag, `prem_persistency_override()` and `has_prem_persistency_override()`, and the withdrawal by `wd_pp_mth()`; the pin read from a vector of floats, NaN where blank, and a vector of 0/1 flags | A monthly cell tests a flag rather than a missing value, and reads no model point column in its own formula. `coi_rate_dp`, already read once a point, is read from an int vector, −1 where blank, `ULSG_US_S`'s own "exact" |
| `class_factor`, `coi_rate_scale` | joined on the label accessors; the point's COI scale a Series, sliced from the table by its sex and class | the class factor joined to the points in `Data` once `class_count()` has checked its table; the scale replaced by `coi_schedule()`, the number of the point's scale, a row of `Data`'s table of the scales by attained age, with its first and last age, `coi_rate_first_age()` and `coi_rate_last_age()`, read by schedule; a class or a sex and class the tables lack refused at the first read of the array, naming every such point | A blank factor, a missing value to `ULSG_US_S`, would reach the cap on `mort_rate`, which keeps it missing, and is refused, as is one below 0; a blank COI rate would reach the account value's floor. No compiled cell returns a Series. Every point reads its class factor and its scale in its first month in cover, where `ULSG_US_S` raised `KeyError` |
| `corridor_factor`, `mort_rate`, `coi_rate_guar`, `lapse_rate_base` | the table read in the monthly cell, at `age(t)` or `policy_year(t)`, clamped to the extent of the key column as pandas reads it | one reader keyed by the age or the year — `corridor_factor_at`, `mort_rate_base_at`, `coi_rate_guar_at` and `lapse_rate_base_py` — with `ULSG_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the values, called inside cover only; each reads `Data`'s array of the table, padded from 0, so that the age or the year is the index; a policy year below 1 and an age below a COI scale's first refused, naming the point, where `ULSG_US_S`'s lookup raised `KeyError` | No table is read at an age or a year the policy does not have, each is read once an age or a year, and a blank, text or fractional key, keys that repeat or leave a gap, a value that is not a number, a lapse or mortality rate outside 0 to 1 and a corridor factor or a COI rate below 0 are refused by name, where `ULSG_US_S`'s extent skips a blank key and cuts the table short, and a blank value is a missing value |
| `surr_charge_rate` | the schedule's row read in the cell | `surr_charge_rate_max()` and `surr_charge_runoff_years()`, one accessor for each of the schedule's two columns, which `Data` joins to the points once `surr_charge_count()` has checked the table, on every point whose ID the table holds, with a charge or without; a point with a charge whose schedule the table lacks refused at the first read, naming every such point, and on a point without one both accessors raise `KeyError`, naming the point, as their `.loc` did at stage E | The same numbers on any schedule, with no table read in a monthly cell; a blank charge, which `ULSG_US_S`'s `max` reads as none, a charge below 0 and a run-off that is not a whole number of years, 1 or more, are refused |
| `rop_anniversary`, `rop_ratio`, `rop_rate` | the return-of-premium table read in each | three readers keyed by the anniversary, `is_rop_anniv(y)`, `rop_ratio_anniv(y)` and `rop_rate_anniv(y)`, each reading `Data`'s array by anniversary, a flag of membership or a value, once `data.rop_last_anniv()` has checked the table | No monthly cell reads a table; an anniversary that is not a whole number of years, 1 or more, or is on two rows, and a refund ratio or an exercise rate outside 0 to 1 are refused |
| `sum_assured_at`, `is_premium_mth`, `prem_persistency`, `premium_pp`, `cum_prem_pp`, `wd_pp`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `sg_coi_pp`, `maint_fee_pp`, `sg_maint_fee_pp`, `surr_charge_rate`, `grace_mth`, `rop_anniversary`, `mort_rate`, `lapse_rate_base`, `lapse_rate_dyn_mult`, `lapse_rate` | unguarded: no `ULSG_US_S` frame has a month before issue | zero, false or the int 0 outside cover, `is_active(t)`, before any table or rate is read; `lapse_rate_dyn_mult` 1.0 | A future point's months before issue have `t ≥ 0` and policy years down to −2. At `t = proj_len()` nothing is charged, paid or withdrawn. The six `age(t) >= charges_cease_age` branches stay `ULSG_US_S`'s, never taken in cover, since the frame ends where the charges do |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `status` | the text `"LAPSED"`, `"GRACE"`, `"IN FORCE - GUARANTEE"` or `"IN FORCE"` | a code: `LAPSED`, `GRACE`, `IN_FORCE_GUARANTEE` or `IN_FORCE`, and `PRE_ISSUE` before issue and `CEASED` from `t = proj_len()` on; `result_av()` writes `ULSG_US_S`'s label for each in its `status` column | Codes for the months outside cover, which `ULSG_US_S`'s frame never holds; and a code, not text, so that the cell compiles to a C number |
| `inflation_factor` | `(1 + inflation_rate)^(policy_year(t) − 1)`, stepping on the policy anniversaries | `(1 + inflation_rate)^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_sg_roll_fwd`, `check_margin` | `math.isclose` with both tolerances at `1e-9`, month by month | the same condition on one relative residual a month, `check_av_roll_fwd_resid(t)`, `check_sg_roll_fwd_resid(t)` and `check_margin_resid(t)`, each a `float` over the larger side and 1; a residual that is not a number fails, and one that is not real raises, as `ULSG_US_S`'s check does | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin` | the lapse term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the loan a surrender recovers | The surrender claim is the net cash value floored at 0, so once a loan exceeds the cash value `ULSG_US_S`'s identity is off by `(csv_pp(t) − loan_bal_pp(t)) × pols_lapse(t)` and its check fails on a projection that is right; on every shipped point no loan is outstanding, and the two agree |
| `result_pols` | `pols_if`, the four outflows, the maturities and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `solve_len`, `sg_pp_solve`, `guar_min_sg`, `no_lapse_premium` | the funding-premium solve, a bisection over the level premium of a replay of the shadow account | removed | The premium is an input fixed at issue (below) |
| `claims` | `claims(t, kind=None)`: one kind's claims, or with `None` its four kinds summed by Python's `sum` | `claims_death(t)`, `claims_lapse(t)` and `claims_refund(t)`, the `result_cf` columns, and `claims(t)` their total, Python's compensated `sum` written out | A compiled cell takes C numbers, and `None` is none. Three kinds pay in one month on a return-of-premium anniversary, where a sum written left to right differs from `ULSG_US_S`'s in the last bit; the fourth, `GRACE`, pays 0.0 in every month (*What compiling changed, and why*, below) |
| `cure_premium_pp` | `D_t / (1 − pi)`, which raises Python's `ZeroDivisionError` at a load of 1 | the same, with the divisor checked first and Python's error raised, `ZeroDivisionError: float division by zero` | Compiled C's division raises the same error with another message. `Data` admits a load of 1, which `ULSG_US_S` projects, since no report reads the cure payment |
| `Data` and the cells that read a table | a malformed value or key met, if at all, only when a projection reaches it, a missing class, scale or schedule as `KeyError` | refused by name at the first read of the array, over the whole table: a class, a sex and class or, on a point with a charge, a schedule the tables lack; an issue age, a guarantee age, a `duration_mth`, a grace counter, a COI precision or a `point_id` of `2**53` or more; and a negative age in the corridor, mortality or COI table | A compiled model holds numbers, not text, computes a NaN as silently as modelx, and holds each age table from age 0 (*What it refuses*, below) |

The other new cells are `policy_count`, `t_entry`, `is_active`, `pols_new_biz`,
`grace_mth_init`, the new opening-state accessor, and `coi_rate_last_age`, the extent of a
point's COI scale; those of compiling are listed under *What compiling changed, and why*,
below.

**The funding-premium solve is not in this model.** `ULSG_US_S` implements the technical
notes' complete algorithm, a bisection over the level annual premium of a replay of the
shadow account with decrements off, as a side calculation that nothing in its projection
reads, and its tests check it. It is an issue-time calculation: it finds the premium a
policy is issued on, and a point in force carries that premium from issue, in its
`premium_pp_ann`. So this model reads the premium from the column, and the solve stays
`ULSG_US_S`'s. Kept unchanged here, the solve would answer a question no point valued later
asks. It replays the shadow account from the frame's first month, not from the policy's
issue, so on a point in force it solves from the valuation date: 11,961.02 on point 6, which
was issued on 10,800.00 and is still paying it, and 31,033.42 on point 1, from its shadow
account of 118,000.00 at month 300, as `ULSG_US_S` finds on its own point 1. On a point
written later, whose months before issue enter its minimum at zero, it finds no premium at
all and raises. And its cells take the premium as a float argument, which a compiled model
could cache only in a Python dictionary. To solve a policy's premium from a later state,
give `ULSG_US_S` a point carrying that state, as its point 1 does: it solves from that
point's own start.

Of the cash flows, the change of clock moves the maintenance expense, and `net_cf` with it,
and on a point restated or written later, through mortality improvement, the counts and
every flow they weight. Point 1's `expenses(t)` less its claim expense is `ULSG_US_S`'s
divided by `1.025^25` at every `t`. Point 9's maintenance expense is `1.025^2` above
`ULSG_US_S`'s point 2's, month for month, and `1.025^3` in the last month of each policy
year, where the valuation year has stepped and the policy year has not; its acquisition,
9,825.60 a policy, is `ULSG_US_S`'s exactly.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points; the compile tests hold it so
on x86-64, and to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py guaranteed_ul                   # in place, beside the model
python tools/build_sec_cy.py guaranteed_ul --out /tmp/ulsg    # elsewhere, with the CSVs
```

The tool exports the model to `ULSG_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `ULSG_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/guaranteed_ul")  # the directory holding the build
from ULSG_US_SEC_nomx_cy import mx_model as model
model.Projection[4].result_guar()             # point 5, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 4` after `Projection.result_cf()` leaves point
1's 432-row frame cached, while `point_id()`, not yet computed, reads point 5's label, and
`Projection.inflation_rate` set to 0 once `Projection[5]` has computed point 6's
`expenses(12)` leaves it at 4.2441, where modelx recomputes 4.1580. Set every Reference on
a model just imported, before anything is computed, where modelx would recompute.

A build takes about two minutes with gcc, 129 s here under load, and needs a C compiler,
which is why `requirements.txt` leaves modelx-cython out:
`pip install -r requirements-cython.txt`. `run_sec.py --cython` builds in place when it
finds no build, or one older than the model, the sample, the spec or the tool, and
`--build DIR` runs a build made with `--out DIR`. Nothing a build writes is committed. All
of it derives from committed files, and an extension module is built for one operating
system, processor and Python (`_mx_classes.cpython-313-x86_64-linux-gnu.so` here); in
place, `.gitignore` covers all of it. A `lifelib.create()` copy of the library carries no
`tools/`, so it cannot build, and `run_sec.py --cython` says so.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so. Compiled by
the same tool, with a sample of its own, as it stood after running in force, the model
typed 148 of its 160 `Projection` cells as C numbers, but eight of them still took a timing
or a kind as text, or `claims`'s `None`, and so kept a dictionary for a cache, as did
`status`, which returned text; and it ran only 2.2 to 2.5 times its own export, 10.4 to
10.8 ms a point on `net_cf` against 23.7 to 27.2, over the committed points. The bodies of
the typed cells still called pandas and Python: a `model_point()` lookup for each of the 22
columns a formula read, a `.loc` on a table for each attained age's corridor factor,
mortality and COI rate, each policy year's lapse rate, each anniversary's refund ratio and
exercise rate and each point's class factor and surrender-charge schedule, the point's COI
scale sliced into a Series by its sex and class, `pd.isna` on the two pins, text compared
in every formula that branched on the premium pattern or the mode, and a generator summed
in `claims`. So each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[4]` is point 5, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on, for every point at once: the premium pattern into
  `is_level_premium`, `is_single_premium` and `is_ten_pay_premium`, the premium mode into
  `premium_freq`, its payments a year, and `has_surr_charge` and `rop_elected` into flags of
  their own. Each decodes as `ULSG_US_S` compares the column, exactly, so a value none of
  the flags names is no flag, and a mode none of the frequencies names is 0, and the cell
  that branches on it raises `ULSG_US_S`'s message, as `ULSG_US_S` does, where it is read:
  a SINGLE point, which never reads its mode, projects whatever it is. The two pins become
  numbers: the persistency pin a value, NaN where blank, and a flag of whether the point
  gives one, and the COI precision an int, −1 where blank, `ULSG_US_S`'s own "exact".
- **Tables indexed by integers.** The lapse table is held by policy year, and the corridor
  and mortality tables by attained age, padded from 0 so that the year or the age is the
  index. The return-of-premium windows are held by anniversary, from 0 to the last, a flag
  of membership and the two values, so that the anniversary is the index. The COI scales,
  keyed by sex and class, are numbered from 1 in the order of those keys, each point
  carrying the number of its own, `coi_schedule()`, and held by schedule and attained age in
  `coi_rate_array`, padded from age 0, with the first and last age of each schedule beside
  it, `coi_rate_first_ages` and `coi_rate_last_ages`: the plan's R7, as `Term_US_SEC`'s
  tables are held. The padding holds NaN, and nothing reads it: each table's one reader
  refuses a policy year below 1 or an age below a COI scale's first, naming the point, reads
  an age outside the corridor or mortality table at its nearest row, as `ULSG_US_S` does,
  and answers an anniversary outside the windows' range as in none. The class factor and the
  surrender-charge schedule are one number a point, and each is joined to the points in
  `Data`. Every point reads its class factor and its COI scale in its first month in cover,
  and a point with a charge its schedule in every month of it, so `Data` refuses a class, a
  sex and class or, on a point with a charge, a schedule the table lacks, naming every such
  point, where `ULSG_US_S` raised `KeyError` as the point projected: every projection for
  the first two, and for a missing schedule the point's cash flows and margin check, which
  read it (its counts, accounts and guarantee report do not). Compiled, that refusal is the
  table's, so every point with a charge is refused those two reports with it, as
  `Term_US_SEC`'s refusals at the first read are. A point without a charge is never refused
  a projection for its schedule, which `ULSG_US_S` never reads; it reads its schedule's two
  columns where the table holds its ID, as at stage E, and where the table does not,
  `has_surr_charge_schedule()` is 0 and both accessors raise `KeyError`, naming the point,
  where their `.loc` raised it at stage E.
- **Codes.** A timing, a kind or a status, which `ULSG_US_S` spells as text, is an int
  Reference named as the text: the count's timings `BEF_NB = 0`, `BEF_DECR = 1` and
  `BEF_MAT = 2`, the accounts' `BEF_PREM = 3`, `BEF_WD = 4`, `BEF_FEE = 5`, `BEF_COI = 6`,
  `BEF_INV = 7` and `EOM = 8`, and the loan's `BEF_INT = 9`; the kinds `DEATH = 0`,
  `LAPSE = 1`, `REFUND = 2`, `GRACE = 3`, `WITHDRAWAL = 4` and `MATURITY = 5`; and the
  statuses `PRE_ISSUE = 0`, `IN_FORCE = 1`, `IN_FORCE_GUARANTEE = 2`, `GRACE = 3`,
  `LAPSED = 4` and `CEASED = 5`. A call reads as before, less the quotes:
  `pols_if_at(t, BEF_DECR)`, `av_pp_at(t, BEF_COI)`, `loan_bal_pp_at(t, BEF_INT)`,
  `claim_pp(t, DEATH)`. A string argument or a string value would give the cell a
  dictionary for a cache, where a code indexes a C array, so codes are numbered from 0
  without a gap. The model has three families of timing, the count's, the two accounts'
  and the loan's, passed to different cells, and they are numbered as one, `BEF_NB` and
  `BEF_DECR` first, as in every SEC model, then the count's third, then the accounts' in
  the order of their instants within the month, `EOM` last, then the loan's. So no two
  timings share a code, and a code of one family passed to another's cell,
  `av_pp_at(t, BEF_NB)` or `loan_bal_pp_at(t, BEF_PREM)`, is refused as `invalid timing`
  in both engines, where families numbered each from 0 would read it as a timing of the
  cell's own without a word. `ULSG_US_S` spells a kind and a status alike, `"GRACE"`, and
  the two families are numbered so that it is 3 in both, one Reference. Two of its
  statuses are not names, `"IN FORCE"` and `"IN FORCE - GUARANTEE"`: their codes join the
  words with underscores, the hyphen dropped, and `result_av()` writes `ULSG_US_S`'s label
  for each code in its `status` column, so the report reads as `ULSG_US_S`'s. The
  `Projection` docstring's *Codes* lists all 21.
- **The claims, split, and their total compensated.** `ULSG_US_S`'s `claims(t, kind=None)`
  is one kind's claims or, with `None`, its four kinds summed by a generator: neither a C
  parameter nor a C loop. Here the three kinds that pay are cells, `claims_death`,
  `claims_lapse` and `claims_refund`, the `result_cf` columns, and `claims(t)` is their
  total; the fourth, `GRACE`, is 0.0 in every month, a policy terminating in grace
  terminating without value, and has no cell. Python's `sum` of floats is compensated,
  since Python 3.12: it carries the rounding error of each addition, Neumaier's way, and
  adds it back once at the end. On a return-of-premium anniversary deaths, surrenders and
  refunds all pay in one month, and there a total written left to right,
  `0.0 + d + l + r`, differs from `ULSG_US_S`'s in the last bit in 3 of the 8 such months
  of the committed points. So `claims(t)` is `sum`'s loop written out, each addition and its
  carried error in explicit statements, which compile to C, and its last test, that the
  carried error is finite, written `abs(c) <= 1.7976931348623157e308`, the largest
  double, which no compiler folds away. The total is `ULSG_US_S`'s float in every month.
- **One Python call kept.** No formula outside the reporting cells calls a Python builtin
  outside its refusals but `int`, `float`, `bool`, `abs`, `min`, `max` and `range`, which
  Cython turns into C, and `round`. `coi_rate` and `sg_coi_rate` hold the declared COI
  scales to the point's precision with `round(r, dp)`, as `ULSG_US_S` does, where `r` is a
  `Projection` Reference, `coi_curr_factor` or `coi_sg_factor`, times the guaranteed rate.
  `Data` cannot read a `Projection` Reference, so the rounding cannot be done there ahead
  of the projection, as the plan's R16 would have it, without moving the two factors out
  of `Projection` or freezing them. So the call stays, a call into the interpreter on the
  same double in both engines, made only on a point that pins its precision, points 1 and
  5 of the committed table, and `tests/us_registry.py` admits it in those two cells alone,
  as it admits `WholeLife_US_SEC`'s `round`. The one division whose divisor `ULSG_US_S`'s
  own inputs can make zero, `cure_premium_pp`'s at a load of 1, is guarded, and raises
  Python's own `ZeroDivisionError: float division by zero`, where compiled C's division
  would raise the same error with another message (*What it refuses*, below).
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `rate_class()`, `premium_type()`, `premium_mode()` and `surr_charge_id()`, and the four
  reports return a table row, text and DataFrames, for a reader, for `run_sec.py` and for
  the comparison with `ULSG_US_S`. No other cell calls them, so they cost the projection
  nothing. A label accessor returns its column as read, and `Data` accepts a label that is
  not text: a blank `surr_charge_id` on a point without a charge, which reads as NaN, or a
  blank `premium_mode` on a SINGLE point, which never reads its mode, and a column of
  numbers, ints. So each accessor compiles to a Python object, as the sample traces it
  (below), and returns what modelx returns. The three checks are reporting cells too, but
  they return a verdict, which compiles to a C `bint`.

The `Data` docstring lists its vectors and arrays, each with the column or file it comes
from: 17 vectors of int64, among them the point labels, the decodes, the COI schedule of
each point and the first and last age of each schedule; 18 vectors of float64, among
them the joins and the five arrays of the tables by age, year or anniversary; the COI
scales by
schedule and age; and ten int counts and extents, each a table's check, `coi_schedules`,
the COI table's, which at stage E returned a Series of last ages, among them. The nine
readers stay Python, returning DataFrames and a path, and no `Projection` cell but
`model_point()` reads them. Every other cell of `Projection`, 155 of its 165, returns a C
`bint`, `long long` or `double`, and caches a single value, or a C array the spec sizes
from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,358 by `t`, of `double`, `long long` or `bint` | the 97 cells of `t` alone: every count, rate, factor, charge, premium, withdrawal, balance, claim and cash flow; the policy clock, its years and the attained ages; the grace counter, the status and the return-of-premium anniversary; the flags `is_active`, `is_premium_mth`, the guarantee's two tests, `is_shortfall` and `is_lapsed`; and the checks' monthly residuals |
| a C array of 1,358 by 10 | `pols_if_at`, `av_pp_at`, `sg_pp_at`, `av_at` and `loan_bal_pp_at`, by `(t, timing)`, and `claim_pp` and `claims_from_av`, by `(t, kind)`, whose six kinds leave four columns unused (*The sample and the spec*, below) |
| a C array of 105 by `y` | `lapse_rate_base_py`, by policy year, and `is_rop_anniv`, `rop_ratio_anniv` and `rop_rate_anniv`, by anniversary |
| a C array of 122 by `a` | `corridor_factor_at`, `mort_rate_base_at` and `coi_rate_guar_at`, by attained age |
| one `long long`, `double` or `bint` | the 44 cells without a parameter but the reporting ones: the point's label, numbers, decodes and pins, its opening state, its class factor, COI schedule and the scale's first and last age, its surrender charge and run-off, the ends of its frame, the monthly guaranteed, shadow and loan rates and the two NAAR factors, the lapse rate's guarantee and pattern factors, and the three checks |
| a Python object | `model_point()`, the five label accessors and the four reports |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the four reports
and the three checks on every committed point, which reach 157 of the 165 cells, and then
the eight they do not and the eight codes no formula passes: `model_point()` and the five
label accessors, which only a reader asks for; `point_id()`, which only a refusal names;
`cure_premium_pp`, the payment that would cure a grace, which no report reads; and, in
cells the reports reach, `pols_if_at` at `BEF_MAT`, `av_at` at `BEF_WD`, `BEF_FEE`,
`BEF_COI`, `BEF_INV` and `EOM`, `claim_pp` at `GRACE`, and `claims_from_av` at
`WITHDRAWAL` and `MATURITY`. It calls the monthly ones in every month of the frame and the
month after it. It projects the committed points alone: the export it runs reads the CSVs
of the directory the build is made in, and the trace it needs is the committed points',
which are what the tests project. The five label accessors it calls once more, on a copy
of the table's first point with every label blank, which it writes to a temporary
directory and reads by a second instance of the export, given the file's absolute path as
`model_point_file`. That types them as Python objects, so that a blank or numeric label
returns what modelx returns rather than raising `TypeError` (*What compiling changed, and
why*). The committed points leave branches untaken: withdrawals, the TEN_PAY pattern, the
non-annual modes, a single premium's lapse factor, the corridor binding, the lapse rate's
cap, the cap on mortality and a loan. That still types every cell, because every branch of
a cell returns the one type its others return, a rate a float in every branch. The two
`round` calls are reached on points 1 and 5, which pin the precision. The sample also
raises the recursion limit, which modelx raises and its export does not (*What a compiled
run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forwards read and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and one of headroom:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,358 | 1,356. The longest frame is a policy issued at the youngest issue age, 18, to the end of the projection at attained age 121, 103 policy years, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 103 + 120 = 1,356 months, `t = 0 … 1,355`, and the month after, 1,356, which the count, the account value's opening timing and the lapse latch are carried into. `pols_lapse_grace`, `av_change` and the three residuals read `t + 1` in cover alone, so nothing reads 1,357 |
| `t`, `timing` | 1,358 by 10 | `t` as above, by the ten timings of the one numbering, so a code past `BEF_INT` raises |
| `t`, `kind` | 1,358 by 10 | `t` as above, by the six kinds and four columns more, so that every 2-D cache has timing's width. Cython's generated unpickle code converts a space's 2-D caches with one function, written for one width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A kind from 6 to 9 is then inside the cache, where the cell refuses it as modelx does, and one from 10 raises |
| `y` | 105 | 103, the policy year of the last covered month at issue age 18, read by `lapse_rate_base_py`, and the anniversaries 0 to 102, read by the three readers by anniversary, all inside cover alone |
| `a` | 122 | 120, the last attained age in cover, read by the three readers by age inside cover alone, from the youngest issue age, 18 |

`proj_len()` refuses a point issued below 18, `issue_age_min`, and one issued at or past
`charges_cease_age`, 121, in modelx as compiled, and the projection ends at attained age
121, so no report on a point the model projects runs past these caches. Those two
References and `Data.future_horizon_mth` are the contract the sizes are derived from.
Lower the minimum, or raise `charges_cease_age` or the horizon, and a report runs past the
caches in the compiled model alone: a frame of more than 1,357 months, a policy year or an
anniversary past 104 or an age past 121 raises `IndexError`, naming nothing, where modelx
projects. Each needs the sizes derived again, as `spec_sec.py` derives them, and a
rebuild: `t` raised to 12 × (`charges_cease_age` − `issue_age_min`) + the horizon + 2, `y`
to `charges_cease_age` − `issue_age_min` + 2, and `a` to `charges_cease_age` + 1. The
shipped COI scale carries the anchor cell alone, from attained age 45, so a point at any
other cell is refused by `Data`, and one issued below 45 by its first COI rate, naming it;
an issue age of 18 is the contract's, which an extended scale reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it
was measured to change there. Here `cpow` reaches eight powers: the monthly rates of both
decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`, the monthly
credited, guaranteed, shadow, loan and loan-credit rates, `(1 + i)^(1/12) − 1` in
`inv_return_mth`, `guar_rate_mth`, `sg_rate_mth`, `loan_rate_mth` and `loan_cr_rate_mth`,
and expense inflation, `(1 + r)^(t // 12)` in `inflation_factor`. Without `cpow` a
compiler with C99's complex numbers, gcc among them, computes a power of two doubles as a
complex power, which can differ from Python's float power in its last bits. With both
directives and the flag every compiled value agrees with modelx's bit for bit, and the
compile tests hold each, by the module's first line, by the compiler's command lines and,
on x86-64, by the comparison itself. On the same platforms the tool adds
`-Werror=incompatible-pointer-types`, so that gcc before 14, which only warns of a pointer
of the wrong type, fails the build as gcc 14 does: the error two cache widths give (*The
sample and the spec*, above).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 2,699,256
bytes, about 2.7 MB, the type's basic size, which holds every cell's cache: 97 arrays of
1,358 months and seven of 1,358 by 10, each beside a flag array of its shape that marks
what is computed, make most of it, the seven 2-D caches' values 760 KB of it. That is 1.4
times `UL_US_SEC`'s, for 2-D caches ten wide against eight, seven of them against five,
and more cells a month. Deleting it, `del model.Projection[idx]`, frees nothing by itself:
an ItemSpace sits in reference cycles, and only Python's cyclic collector frees it. That
is why `run_sec.py --block` collects after each release, in its frame pass and in its
projections (*Run it*, above), and a compile test holds a compiled block run to one
point's ItemSpace at a time. Without it, 504 compiled points peaked at
1,298 MB (*Speed*, below). Allocating and zeroing the struct is paid once a point:
the frame pass, which makes each point's ItemSpace, asks its `proj_len()` and releases it,
took about 0.1 ms a point (*Speed*).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised. What it needs is stack. The deepest call the contract allows, a cold
`net_cf` in the last month of the longest cover, issue age 18, issued now or 120 months
on, runs the account value's chain back to `t_entry()`, 1,253 and 1,256 cells deep in
modelx (*Counts and timings*, above), and compiled with gcc it runs on a thread of 320 KiB
of stack and not of 288, 235 to 262 bytes a level. A test runs it in a thread of 1 MiB,
the stack Windows gives a program's main thread unless the program is linked for more,
and again on the main thread, which is where `run_sec.py --cython` runs. MSVC's frames may
be larger than gcc's, and the `cython` CI job, which runs the test on Windows too, is the
check on them: the test first runs the call at seven stacks, from 256 KiB to 2 MiB, and
reports the smallest it ran on, so a first run there measures MSVC's need. Until then it
is an estimate: at `WholeLife_US_SEC`'s 325 to 433 bytes a level it would be about 400 to
530 KiB, inside 1 MiB by about twice. A stack below the need kills its child on an
overflow, by design (with gcc, 288 KiB does); on Windows the child ends with
`STATUS_STACK_OVERFLOW`, and should Windows Error Reporting hold it instead, the test
waits a bounded time for each child rather than the job's hour. The export recurses in
Python instead: the same call needs a recursion limit of 2,526 there, and the four
reports and the three checks, which run in ascending `t`, need 58 once the package is
imported and 128 with its import, as the sample runs them, so `sample_sec.py` sets 11,000,
four times the first rounded up to the thousand, and a test holds it to that derivation.

**On Windows**, which no run here has reached, the `cython` CI job's Windows leg is the
check, and five things are particular to it. The stack, above, is MSVC's to measure. The
claims total is exact only where the compiler neither folds `0.0 + x` away nor fuses an
addition with a multiplication: gcc is held to that by `-ffp-contract=off`, and MSVC's
default, `/fp:precise`, keeps both, on x86-64, whose SSE2 arithmetic has no fused
multiply-add; the finiteness test, `abs(c) <= 1.7976931348623157e308`, is one no compiler
folds. The powers call the C runtime's `pow`, which modelx's float power calls too, on
the same platform, and `round` is the same Python call in both engines, so the compile
tests' exact comparison holds there too, and a difference would be a finding. MSVC
accepts the unpickle code's mismatched 2-D cache shapes that gcc 14 refuses, so the one
inner width is held by the Linux leg and by the test of the spec's sizes. And the cost
of allocating and zeroing the 2.7 MB struct a point has been measured on Linux alone.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode, join or hold, when the array is first read, naming every point
  at fault, or the table and its lines: a `point_id` that is not a whole number,
  `model_point_table_sec.csv: point_id must be a whole number; [1.5] is not`, when the
  labels are first read, by `point_id()` or a refusal; a `rate_class` the class factors
  lack, `class_factor_table.csv has no factor for the rate_class of point_id [2]`; a sex and
  rate class the COI scale lacks, `coi_rates.csv has no scale for the sex and rate_class of
  point_id [2, 6]`; and, on a point that `has_surr_charge`, a `surr_charge_id` the schedules
  lack, `surr_charge_table.csv has no schedule for the surr_charge_id of point_id [4], each
  of which has_surr_charge`. `ULSG_US_S` fails every projection of a point of the first two
  kinds with a `KeyError`, and of the third its cash flows and margin check, which read the
  schedule (its counts, accounts and guarantee report do not); compiled, the third refusal
  is the table's, so every point with a charge is refused those two reports with it, as
  `Term_US_SEC`'s refusals at the first read are. No projection of a point without a charge
  reads its schedule, so none is refused for it; on such a point `surr_charge_rate_max()`
  and `surr_charge_runoff_years()` raise `KeyError`, `'point_id 2: surr_charge_table.csv has
  no schedule for its surr_charge_id'`, compiled as in modelx. Every decode and join
  compares the text exactly, as `ULSG_US_S` does, so `"StdNT "`, with a space, is no class.
  And, before it is cast to int64, a number of `2**53` or more in size, which numpy would
  cast to the least int64 without a word: a `point_id`, an issue age,
  `model_point_table_sec.csv: age_at_entry must be below 2**53 in size, where an int64 holds
  it; it is not at point_id [3]`, a guarantee age, a `duration_mth`, a policy issued `2**63`
  months on, a grace counter and a COI precision, which `ULSG_US_S` projects as exact. The
  five columns are the model point table's rule 19, checked after its other 18, so that each
  of those keeps its message, and a fractional issue age is refused by the earlier rule that
  it be a whole number of years; the `point_id` is refused when the labels are first read.
- A negative age in `corridor_factors.csv`, `mort_table.csv` or `coi_rates.csv`,
  `corridor_factors.csv: age must be 0 or more; it is not on line [2]`, by the table's
  check, which every reader of the table asks first: each is held from age 0, so that the
  age is the index. A refusal `ULSG_US_S` lacks, checked after the table's other rules, so
  that a table whose ages leave a gap keeps that message.
- A key beyond a table, by the one cell that reads it, naming the point, where
  `ULSG_US_S`'s lookup raised `KeyError`: a policy year below 1, `point_id 2:
  lapse_table.csv has no rate for policy year 0`, from `lapse_rate_base_py`; an attained
  age below the point's COI scale, `point_id 2: coi_rates.csv has no rate for the point's
  sex and rate_class at attained age 40`, from `coi_rate_guar_at`, which a point issued at
  40 meets in its first month in cover; and an anniversary without a window, `point_id 2:
  rop_table.csv has no anniversary 3`, from `rop_ratio_anniv` and `rop_rate_anniv`, none
  of which a projection calls outside cover or off a window.
- By `proj_len()`, a point to be issued at or past attained age 121, at or past the end of
  the projection, whose grace has expired, or issued below `issue_age_min`, in that order,
  the last `point_id 2: issue age 17 is below issue_age_min, 18` (*The in-force interface*,
  above, quotes the others).
- A timing or a kind a cell does not take, `ValueError("invalid timing")` and
  `ValueError("invalid kind")`, where the code is inside the cell's cache: a code of
  another family, `av_pp_at(0, BEF_NB)`, `loan_bal_pp_at(0, BEF_PREM)`,
  `pols_if_at(0, BEF_PREM)`, `av_at(0, BEF_MAT)`, `sg_pp_at(0, BEF_INT)`, a timing of the
  family a cell lacks, `av_pp_at(0, EOM)`, a kind a cell lacks, `claim_pp(0, MATURITY)`,
  and a code up to 9, `claims_from_av(0, 9)`.
- A mode or a pattern no decode knows, `ValueError("invalid premium mode")` and
  `ValueError("invalid premium type")`, where the point reads it, as in `ULSG_US_S`.
- At a load of 1, `cure_premium_pp`'s `ZeroDivisionError: float division by zero`, which
  `ULSG_US_S` raises there too. `Data` admits the load, as `ULSG_US_S` projects it, since
  no report reads the cure payment.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1358)`, which modelx answers with 0, the month being outside cover;
`pols_if_at(0, 10)` and `claim_pp(0, 10)`, which modelx refuses as `invalid timing` and
`invalid kind`; `lapse_rate_base_py(105)`, which modelx reads at the table's last year,
0.0075, and `lapse_rate_base_py(-1)`, which modelx refuses, naming the year;
`corridor_factor_at(122)` and `corridor_factor_at(-1)`, which modelx reads at the table's
nearest row, 1.00 and 2.50; `coi_rate_guar_at(122)`, which modelx reads at the scale's
last age, 0.0; and `is_rop_anniv(105)` and `is_rop_anniv(-1)`, which modelx answers
`False`. An `idx` past the last row is refused in both, with an `IndexError` at the first
read of a vector, and `Projection[-1]` reads every vector at its last element in both, so
it is the table's last point, under that point's own `point_id()`.

A Reference is a C variable of its value's type: `issue_age_min`, `charges_cease_age`,
`lifetime_guarantee_age`, `wd_first_year`, `ten_pay_years`, `grace_months`, the
improvement's ages and years, the codes and `idx` a `long long`, as
`Data.future_horizon_mth` is, and the rates and amounts a `double`. Set past that type, it
is converted when it is set, where modelx keeps the value as given. A float set on an int
Reference is truncated toward zero without a word, `charges_cease_age = 121.7` reading 121
and `issue_age_min = 18.5` reading 18, where modelx computes with the float:
`charges_cease_age = 121.0` makes `charges_cease_mth()` a float there, and `result_cf()`
then fails. A text, a NaN or an int beyond 64 bits is refused at once, with `TypeError`,
`ValueError` or `OverflowError`. An int set on a `double` Reference reads as a float
compiled, where modelx returns the int: `crediting_rate_curr = 0` gives
`crediting_rate_ann(0)` 0 in modelx and 0.0 compiled, and so does `wd_fee` in `wd_fee_pp`,
which returns the Reference as it is. Each shipped Reference is a value of its C type, so
no shipped number differs. And a Reference set past its domain computes as C computes,
where modelx raises: an `inflation_rate` of `1e300` makes `inflation_factor(24)` infinite
compiled, where modelx's power raises `OverflowError`; and `load_prem_rate_sg` set to 1,
which `catch_up_prem_pp` divides by `1 − load_prem_rate_sg`, raises `ZeroDivisionError`
in both, with `float division by zero` in modelx and Cython's shorter `float division`
compiled. That divisor is a Reference, which a user sets on purpose, not a model point
value, and it is not guarded.

A rate past its domain is computed, not refused, as in `ULSG_US_S`. The annual mortality
rate is capped at 1, `min(q, 1.0)`, in both, so its monthly rate stays real. The lapse
rate is held between `lapse_rate_floor` and `lapse_rate_cap`, and with a bound set past 1
the annual rate passes 1 and the monthly rate, `1 − (1 − w)^(1/12)`, has no real value: it
is complex in modelx, whose account value and margin checks then raise `TypeError`, and
NaN compiled, whose same two checks then fail, a residual that is not a number failing,
while the shadow account's, which no decrement reads, holds in both. A NaN rate stays NaN
through the cap on mortality, in both, as through every other bound, each of which the
compiled model computes as a comparison that keeps the value unless the bound is smaller,
or larger: a NaN `mort_ae_factor`, set as a Reference, makes `mort_rate(0)` NaN in both.
`Data`'s refusals of a value outside its range keep any NaN from reaching them through
the inputs.

A withdrawal or a loan on a policy whose account the guarantee holds at 0 is accepted and
projected, as `ULSG_US_S` projects it, and fails two checks in both models, whatever its
size: on point 7, valued with its account exhausted, a withdrawal of $1 a month or a loan
of $1,000 makes `check_av_roll_fwd()` and `check_margin()` false, compiled as in modelx,
while `check_sg_roll_fwd()` holds. `ULSG_US_S` pays a withdrawal whatever the account can
fund, and accrues a loan the account cannot carry, and compiling moves no number, so
neither model changes; it is an item for `ULSG_US_S` (USLIB-SEC-PLAN.md §7.5).

### Speed

`python tools/bench_sec_cy.py guaranteed_ul` builds the model into a temporary directory,
or takes a build with `--build`, and times one block run on three engines: modelx, the
export and the compiled model. Each engine runs the committed table repeated, in a process
of its own, as `run_sec.py --block` runs a block, each point projected and then released.
`net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,003 | 1.42 ms (8.55–9.10) | 2.13 ms (12.80–13.58) | 87 MB |
| export | 603 | 17.4 ms (10.47–11.15) | 16.8 ms (10.12–11.97) | 87 MB |
| modelx | 126 | 539 ms (67.9–70.1) | 551 ms (69.4–72.3) | 181 MB |

The blocks are the committed table repeated, 667 times compiled, 67 exported and 14 in
modelx. On `net_cf` the compiled model runs 12.2 times its export, and on `result_cf`, where
building the DataFrame takes much of its time, 7.9 times; it runs 380 and 259 times modelx.
A second run of the compiled model and the export straight after, under a 1-minute load
between 2.5 and 3.0, gave the compiled model 1.43 and 2.13 ms and the export 16.8 and 16.8
ms, 11.8 and 7.9 times. That is about as many times its export as `UL_US_SEC`, 12.0, and
`WholeLife_US_SEC`, 13.9, and more than `Term_US_SEC`, 9.5, or `BasicTerm_SC` on its own
measure, 8.7. A point takes longer than `UL_US_SEC`'s, 1.21 ms, for 165 cells against 136
and a struct 1.4 times the size. As it stood after running in force, compiled the same way,
the model ran 2.2 to 2.5 times its export (*What compiling changed, and why*, above), and
the compiled model runs about seven times that build on the same measure, 1.43 to 1.68 ms a
point over the committed points against 10.41 to 10.84: the representation, not the
compiler, is the gain. The release keeps a block flat: the compiled model's peak grew by
less than 0.1 MB over its 6,003 points, and without the collection after each release
(`--no-collect`), 504 compiled points peaked at 1,298 MB. Reading the eight files and
building every `Data` vector and array for those points took 0.073 s, and asking every point
for its frame, the runner's first pass, which makes, reads and releases each point's
ItemSpace, 0.58 s, about 0.1 ms a point.

Measured on 2026-11-13 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 2.3 and 3.1 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Under load the spread is wide, and the fastest run is the
one to compare.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 2, 3 and 4, issued
  at the valuation date, every cell of `ULSG_US_S`'s agrees at every argument `ULSG_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`, whose
  meaning changed, the four cells of the funding-premium solve, which this model does not
  have, `coi_rate_scale`, the point's COI scale as a Series, which this model replaced by a
  schedule number, and whose rates the identity compares in `coi_rate_guar` in every
  month, and `status`, a code here, whose labels it compares in `result_av`'s `status`
  column; `ULSG_US_S`'s `claims(t, None)` is compared with the total `claims(t)`, and its
  kinds through the `result_cf` columns. A cell this model lacked, or that took other
  arguments, would fail it otherwise. The identity holds on any
  count, since `ULSG_US_S` already charges acquisition on the policies issued. The same
  suite holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The in-force twin**, in `tests/test_guaranteed_ul_us_sec.py`: point 1 opens with
  `ULSG_US_S`'s own opening balances and no grace, and with expense inflation set to 0 in
  both models it is `ULSG_US_S`'s projection from `t = 0`, in every cell and every report,
  to 1e-9 relative with no absolute floor; at the shipped assumptions the two part in the
  maintenance expense alone, in the inflation factor, the expenses, the expense margin and
  the net cash flow, and in no other cell. So the goldens `tests/test_guaranteed_ul_us.py`
  asserts on point 1 — every cell of the worked example's five rows, the notes' NAAR
  constants, the account value's exhaustion at `t = 3` and the guarantee carrying the
  policy from `t = 4` — hold here, with no number restated.
- **The splice**: each `ULSG_US_S` point restated in force at a month either side of its
  events continues the S projection from there, in its four reports, column by column, and
  in every other cell the two share, the two accounts at every timing, the loan, the grace
  counter, the latch and the checks' verdicts among them, to 1e-9 relative with no absolute
  floor, since its counts fall far below 1e-7. It leaves out those the twin identity skips
  and `ULSG_US_S`'s own opening values and frame. The months straddle the product's events:
  the first anniversaries; the surrender charge's last month; the account's exhaustion under
  the guarantee; a grace that opens in the valuation month, and a counter carried into it,
  which lapses the policy a month on; the 20th and 25th anniversaries' windows, at `t = 0`
  and, on a row valued mid-year, at `t = 1`; the month the shadow account's net amount at
  risk is floored; and the last covered month, whose `t = 1` is the month the survivors are
  carried into. So are variants of S's points, in a copy of S's table that is never
  committed, each changing S's columns only and each with input rows of its own, for
  branches S's own points do not reach: ten-pay premiums, quarterly; withdrawals that outrun
  an exhausted account, semi-annually; a loan under a funded account, in force at 300; a
  loan of $10,000 on S point 1's exhausted account, in force at 300, which takes the account
  entering 65 of its months below 0 and decides the guarantee's test in two, so that its
  twin and its row restated at 3, the last month its account is still 0 or more, compare
  `ULSG_US_S` where the loan's credit and the guarantee's test both read the debt; a single
  premium large enough for the corridor to bind, on a COI scale that stops short of its
  cover, so that its later ages are read at its last; a guarantee to 99, monthly, with
  neither a surrender charge nor the endorsement; each pin alone; issue age 40, below the
  mortality table's first age, on a second surrender-charge schedule; S point 4 paying
  $6,150 a year, whose anniversary premium cures its grace; S point 2 paying $100 a year,
  too little for its first month's deductions, issued 13 months on, the one row in grace
  from its issue month, which reads the grace counter's base there; and S point 2 with a
  guarantee to 100, the lifetime guarantee's age the splice sets, met exactly, where the
  guarantee to 99 meets it a year short. Between them they carry both sexes and every class.
  The twin of each variant issued at the valuation date is compared with its S point cell by
  cell, as a row issued there is, so that an issue rule only a variant takes at `t = 0` is
  reached; the two variants of point 1, in force 300 months, are splice cases from `t = 0`,
  as point 1 is. The References are set in both models: expense inflation and mortality
  improvement at 0, the two inputs on the valuation clock that move a number; the mortality
  A/E at 0.56, which leaves survivors at the end of every frame that does not lapse; a
  premium tax of 2%, the one assumption the product ships at zero; and the lifetime
  guarantee's age at 100 and the single premium's lapse factor at 0.65, each set apart from
  the Reference it ships equal to, `charges_cease_age`'s 121 and the dynamic lapse
  multiplier's 0.6, so that a cell reading the one for the other shows. A second fixture, on
  References of its own, binds the two bounds `ULSG_US_S` ships idle, the lapse rate's cap,
  lowered to 1.25%, and the credited rate's floor, under a declared rate of 1.5%. Charges
  cannot cease in cover, since the frame ends where they do.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every line of the model the full grid
  reaches, every opening-state column, every kind of valuation month, every premium pattern
  and mode, and every floor and cap the grid binds, each checked by the raw value it bounds,
  and a test asserts that they do. It also records each side of every `min` and `max` the
  core's rows bind, by the values each call compares, and asserts that every side binds
  there but the seven bound by tests of their own: the two bounds `ULSG_US_S` ships idle, on
  the second fixture; the cap on mortality; the three clamps of the tables shorter than the
  cover; and the shadow account residual's floor of 1, where its sides are small. The other
  cases carry the `sec_full` marker and show as skipped, with the reason, unless
  `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI run runs the full
  grid too.
- **Future new business**: issued 1, 12, 13 and 25 months after the valuation date, S point
  2 is the S projection moved on, cell by cell, and so are S points 3 and 4 and each
  new-business variant issued 13 months on, whose months before issue reach policy year
  −1; with zeros before issue in every report and no decrement rate evaluated there.
- **How it computes**: each row the splice and the future business compare is first run on
  the books and scanned: no cell has been called at a negative month, none evaluated from
  `t_entry()` on has read a month before it but the mortality improvement factor, which on
  a point written later reads the valuation years before its issue, by design, and none
  evaluated at month `t` has read a month later than `t + 1`. Every monthly cell holds its
  value outside cover and reads no table there, before issue and at `proj_len()`, on the
  committed points and on the splice. On a fresh read of the committed model the policy
  clock is a closed form, every point's reports run under a lowered recursion limit, which
  a recursion backward over the frame would exceed, no projection cell has read a label
  accessor, and the solve's cells are absent. And every chain is called cold, each call on
  a read of its own: `net_cf` in the last month on the committed points, and each chain's
  head on the twin of point 3, and both on the two rows of the longest cover, one issued
  now and one 120 months on, whose frames are asserted first, modelx's stack trace
  counting no more than one cell a month back to `t_entry()` and a fixed overhead, which a
  chain of two cells a month would exceed, while the improvement factor stays within a
  bound of its own; the ascending sweep at the longest cover belongs to the full grid.
- **Counts, validation and regeneration**: the roll-forward closes, the month of a lapse and
  the last month included, `BEF_MAT` is the `BEF_DECR` count, and `pols_if_at` refuses a
  timing it does not have; `result_pols()` is `ULSG_US_S`'s, column for column, with
  `pols_new_biz` beside it; multiplying `policy_count` by 2.5, with every assumption that
  ships at zero switched on, scales every counted cell and moves no per-policy value; each
  malformed row is refused naming its point, by its own rule, and so is a projection of it,
  a flag written 1, 0, 1.0 or 0.0 among them; a flag written `True` or `False` in any case
  decodes, and projects, as written; each assumption table with a malformed key, a policy
  year below 1 among them, or a value that is not a number, is refused naming its file,
  its column and its lines, and so is one with a value outside its range, a corridor
  factor below 0 among them, while the bounds of each range are read; a `premium_type` or
  `premium_mode` no decode knows raises `ULSG_US_S`'s message; the horizon is a Reference,
  which at 0 refuses any future business, saying so; a point to be issued at or past
  attained age 121, one at or past the end of the projection and one whose grace has
  expired are refused by `proj_len()`, in that order, a counter at `grace_months` and one
  past it among them, and with `grace_months` moved to 3 a counter of 3 is refused and one
  of 2 projects, and a point issued at attained age 120 has a year of cover; every state
  `ULSG_US_S` reaches on either splice's inputs,
  restated in force by the generator at the edges of its windows, or with
  `USLIB_SEC_FULL=1` at every month before its lapse, is read by `Data` and has a frame,
  but the one it refuses by name, an account value below 0 under a loan on an exhausted
  account, which also fails `ULSG_US_S`'s own checks; the edges of the interface are
  accepted, the keys of every keyed table and the integer columns written as floats among
  them; the committed table is what `ULSG_US_S` generates, and the generator refuses a
  month after a lapse; and each committed derived and future row opens with `ULSG_US_S`'s
  own count and state at its month and continues its S point per policy, frame by frame,
  at the shipped assumptions.
- **The opening state and the rest**: point 5 opens from its own grace counter and shadow
  account, and the twin of point 1 from its own premiums to date, and read as `ULSG_US_S`
  would open them they give the numbers above; mortality improvement, expense inflation and
  the declared rate run on the valuation clock, the improvement 0.9801 in point 9's issue
  month; a check whose residual is not a number fails, the NaN sent through a Reference the
  counts read, the improvement rate, and through two that reach a residual without them, the
  declared rate and the shadow account's rate, and each check decides as `ULSG_US_S`'s
  `math.isclose` does where its sides fall below 1; a lapse rate past 1, under a cap raised
  past it, makes the account value's and the margin's checks raise in both models, the
  residuals being floats; on a point whose loan comes to exceed its cash value the margin
  identity holds where `ULSG_US_S`'s fails; acquisition falls on new business alone, per
  policy issued and not inflated; a StdTob point at an A/E of 1.0 with improvement off,
  whose product first passes 1 at attained age 107, is `ULSG_US_S`'s in every cell, the
  capped months included, as new business and restated in force, the rate there is the float
  1.0 in both models, every life in force dies in that month and nothing is in force after
  it; a NaN that reaches the cap stays NaN, sent through the A/E or the improvement rate,
  each a Reference, and so does one that reaches a bound written second; a corridor table
  cut to ages 61 to 94 and a mortality table ended at 110, each read past its ends at its
  nearest row, leave two variants `ULSG_US_S`'s points in every cell, each clamp binding
  with an effect; each pin holds in every month and alone; the premium is the column's, and
  the solve is `ULSG_US_S`'s; the docstrings describe this model and not `ULSG_US_S`, their
  tables read into the right cells, and they parse under docutils with nothing rendered
  wrongly; both models read the one copy of each assumption table, and every other Reference
  of either Space is `ULSG_US_S`'s, value for value, but the horizon this model adds and the
  solve's tolerance, its limit of doublings and the `math` module, which it leaves out with
  the solve; the grace's length, which ships equal to the failed guarantee's lapse
  multiplier, 2, is set apart from it at three months, and the twins of `ULSG_US_S`'s points
  1, 2 and 4 are its points then, each through its lapse, a month later; the points of a
  block sum row by row; an extract without the generator's three columns, relabelled,
  projects the same numbers; and `run_sec.py` prints the model's numbers.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of its reports,
  its sum, its largest value and its values at five months, and the model reproduces it to
  1e-12. `python tools/gen_sec_fingerprint.py ULSG_US_SEC --check` makes the same
  comparison. The tests above held through the compile step with their call syntax
  changed: a point's position for its label, the codes for the text of a timing, a kind or
  a status, and the three claims cells for `claims(t, kind)`. The extract is relabelled
  rather than numbered by position, and each point is named by its label, in
  `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: the claims total is `ULSG_US_S`'s `claims(t)` bit for bit,
  sign of a zero and type included, on every month of the committed points, the months
  where three kinds pay among them, and on totals set in both models where a sum written
  left to right would differ; each code is the Reference the *Codes* table names, the
  three timing families numbered as one, `GRACE` 3 as a kind and as a status, and `status`
  holds `ULSG_US_S`'s labels through `result_av`; the spec's sizes are those derived from
  the contract, and the sample's recursion limit the one derived from the export's need;
  the padding beyond each table's extent is NaN, and the persistency pin NaN exactly where
  the column is blank; a point issued below `issue_age_min` is refused by `proj_len()`,
  naming it, and the longest frame, issue age 18 issued 120 months on, is 1,356 months;
  each number read into an int64 at `2**53` or more, and a negative age in an age table,
  is refused, and the class and COI joins and the charged schedule refuse a key their
  table lacks, naming every point, while a point without a charge is not refused for its
  schedule, reads it where the table holds its ID, as at stage E, and raises `KeyError`
  where it does not; a mode or a pattern no decode knows raises `ULSG_US_S`'s message
  where it is read, and a SINGLE point projects whatever its mode; and `run_sec.py
  --cython` prints what `run_sec.py` prints, and outside the repository says it cannot
  build. Each is a test of `tests/test_guaranteed_ul_us_sec.py`'s *Stage EC* section, run
  in modelx with no compiler: `test_the_claims_total_is_s_sum_bit_for_bit`, on the twins'
  every month and on the eight committed months where all three kinds pay, three of which
  a total written left to right gets wrong, and
  `test_the_claims_total_sums_any_parts_as_s_sum_does`, on three negative zeros and on
  `1e16, 1.0, -1e16`; `test_the_codes_are_dense_and_grace_is_one_code` and
  `test_status_is_a_code_and_the_report_keeps_s_labels`;
  `test_the_spec_sizes_each_cache_as_its_comment_derives` and
  `test_the_sample_raises_the_recursion_limit_its_comment_derives`;
  `test_every_padded_array_holds_nan_and_no_reader_reads_it`, eight refusals below a table
  on an extract labelled otherwise than by position;
  `test_the_coi_schedules_are_numbered_by_key_whatever_the_file_order`, six scales written
  in reverse key order; `test_what_data_cannot_number_or_join_is_refused_naming_it`, seven
  cases; `test_a_value_no_decode_knows_is_refused_as_in_ulsg_us_s`, eighteen, each value a
  decode or a join names in another case and with a space beside it;
  `test_a_point_without_a_charge_reads_its_schedule_as_at_stage_e`, on SC7, a second
  schedule, on `GUL15` and on an ID no table has, each pinned to the value the model read
  at stage E; `test_a_point_issued_below_issue_age_min_is_refused_by_proj_len`; five cases
  of the int64 bound among the malformed rows and three negative ages among the malformed
  keys; and the two runner tests. Beside the pins' test,
  `test_the_precision_pin_at_0_and_blank_is_s_pin_cell_by_cell` compares the twins of
  `ULSG_US_S`'s point 2 at 0 places and blank with `ULSG_US_S`, cell by cell, and holds
  `coi_rate_dp()` to `ULSG_US_S`'s int, so that 0 read as exact, or the accessor's `int()`
  dropped, fails there.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting ones refers to pandas, numpy or another module, reads a table
  with `.loc` or the like, calls a reporting cell, holds text but in its docstring and its
  refusals, or holds a generator, a comprehension or a nested function; none calls
  anything but a cell, a `Data` vector and the builtins of *One Python call kept*, and the
  registry admits `round` in `coi_rate` and `sg_coi_rate` alone; every `Data` vector a
  formula reads is an int64 or float64 array, read by element; no cell is uncached; and
  each label accessor returns its point's column of the same name.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting ones a C `bint`,
  `long long` or `double` and a C-array cache of exactly the spec's size, and every new
  `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps no
  Python object among a projection cell's locals, calls no Python builtin there but the
  admitted `round`, and builds no container, under both directives (C3); on the committed
  points, every cell at every argument a full modelx sweep caches is what modelx computes,
  bit for bit on x86-64, and so is every raise and every `Data` array (C4); and
  `run_sec.py --block`, run compiled, holds one point's ItemSpace at a time. In
  `tests/test_guaranteed_ul_us_sec.py`, eleven compiled tests after the fingerprint: the
  same comparison on the splice grid, the core by default and the full grid with
  `USLIB_SEC_FULL=1`, variants included, ten rows at a time, with the timings and kinds no
  sweep reaches called too, and every compiled `claims(t)` held to the `sum` of its
  compiled kinds by `float.hex`, the sign of a zero included, which the comparison by
  value cannot see; at the contract's extremes, seven points, the longest frame, 1,356
  months from issue age 18 issued 120 months on, ten-pay quarterly with withdrawals,
  StdTob at 85 where the cap binds, a one-row frame, issue age 120 and a load of 1, on a
  COI copy written in reverse key order and a return-of-premium table with anniversaries 1
  and 102; four cases of labels that are not text, blank or numeric; the keys of every
  table written as floats; where the cap binds, and under five References at NaN; the
  compiled model refuses what modelx refuses, with modelx's message, in 243 cases on their
  own inputs, the compiled `Data` cell beside the projection, and thirteen arguments past
  a cache raise `IndexError`; on points without a charge, the two schedule accessors read
  the stage E values, and raise `KeyError` on an ID the table lacks, as modelx does, and
  `Data`'s joins are modelx's arrays; the deepest call the contract allows runs cold on a
  1 MiB stack and on the main thread, and the test reports the smallest of seven stacks it
  ran on, 384 KiB with gcc; past a lapse rate of 1 the compiled checks fail where modelx's
  raise; a Reference set after the model has computed changes no value it has cached; and
  `run_sec.py --cython` prints what `run_sec.py` prints, and refuses a directory with no
  build. Under load, with the build reused, the grid took 74 s on the core grid, the
  refusals 140 s, the cap's 29 s, the labels' 21 s and the extremes' 14 s. They are marked
  `cython`, and they skip without the toolchain, but in the `cython` CI job, which
  installs it on Linux and on Windows, one leg a product, a skip fails, whatever made it.

```bash
python -m pytest tests/test_guaranteed_ul_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_guaranteed_ul_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k ULSG_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k ULSG_US_SEC
python -m pytest tests/test_guaranteed_ul_us_sec.py -q -m cython  # the compiled tests
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
