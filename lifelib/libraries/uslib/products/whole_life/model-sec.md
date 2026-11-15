# In-Force Implementation Notes

**Status:** Draft, 2026-11-01. `WholeLife_US_SEC` is [`WholeLife_US_S`](model.md) taught
to project from a valuation date. Besides policies issued at that date, it takes policies
already in force there, in any month of their policy year, and policies to be written in
the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes, and how the model compiles. The suffix adds lifelib's letters to
`S`: `E` for in force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `WholeLife_US_S` on another time axis, and it reads `WholeLife_US_S`'s assumption tables
> in place, every assumption unchanged. The contractual skeleton is sourced, the
> final-expense rate card [S7] among it, and everything else is a **[std]**
> standardization, **including all four guarantee-basis tables**: illustrative curves
> calibrated to the worked example's anchors, *not* the 2017 CSO / 4% tables the notes
> name, and not even one basis between them, as
> [`model.md` sets out](#uslib-whole_life-guarantee-basis-tables). Replace them with
> company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/whole_life/run_sec.py            # point 1: the anchor cell, in force
python products/whole_life/run_sec.py 19         # point 19: the loan variant, mid-year
python products/whole_life/run_sec.py --block    # every model point, summed row by row
python products/whole_life/run_sec.py 19 --cython # point 19 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about a minute
and a quarter, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and
`.gitignore` covers it.

The first prints, as rows `t = 0 … 11`, the twelve months `run.py` prints for
`WholeLife_US_S`'s point 1, the worked example's policy year 10, with the counts and rates
behind them. Every column agrees with `run.py`'s but `expenses`, which are in
valuation-date dollars here, 5.00 in the first month where `run.py` prints 5.98, and
`net_cf` and `liability_cf` with them. Three lines to the same thing for point 19:

```python
import modelx as mx
model = mx.read_model("products/whole_life/WholeLife_US_SEC")
model.Projection[18].result_cf()     # point 19, the table's nineteenth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[18]` is point 19, and its `point_id()` says so. `result_cf()` has
`WholeLife_US_S`'s twelve columns — `pols_if`, `premiums`, `rider_premiums`, `expenses`,
`premium_taxes`, `claims_death`, `claims_lapse`, `claims_maturity`, `div_cash_paid`,
`loan_draws`, and the net flow under both signs, `net_cf` and `liability_cf` — with one
row per month from the valuation date, `t = 0 … proj_len() − 1`. `result_pols()` sets out
the counts behind it on the same rows: `pols_if`, `pols_new_biz`, then the month's deaths
and surrenders in processing order and the maturities of the last covered month, then
`WholeLife_US_S`'s four decrement rates, annual and monthly, written 0 outside cover.
`result_cv()` has `WholeLife_US_S`'s values per policy, each month's closing balances and
its two benefit amounts, with zeros before issue. `result_cf_annual()` sums `result_cf()`
into policy years, as in `WholeLife_US_S`, and leaves out the months before issue.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read, so the run holds the cells of one point at
a time. Deleting it, `del model.Projection[idx]`, is not enough: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees, so the runner collects after
each release. It freezes everything alive (`gc.freeze()`) once the model and its table are
read, and again once it has asked every point for its frame, so that each collection scans
only what the block has made since. It keeps the block's sum as it goes, compensated as
pandas sums a `groupby`, so that the block is, bit for bit, the frames concatenated and
summed by `t`, as below.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to maturity at attained age 100.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month index, and the contract runs on
  it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1` and
  `age(t) = age_at_entry() + duration(t)`, as in `WholeLife_US_S`, and `is_anniv(t)` is
  true in the last month of each policy year in cover. `BasicTerm_SE` reaches the same
  numbers by adding one a month, a recursion as long as the frame; the closed form needs
  no such chain of calls.

`anniv_mth(t)`, the month of the anniversary that ends the policy year containing `t`, is
on the valuation clock: `t + 11 − duration_mth(t) % 12`, where `WholeLife_US_S` returns the
policy month `12 × duration(t) + 11`. The two are the same number only where the clocks
coincide.

Point 1 is the worked example's anchor cell, in force 108 months. At `t = 0` it is on the
anniversary that opens policy year 10, at attained age 54. Its tenth anniversary, where
the year's dividend is credited and buys paid-up additions, falls at `t = 11`,
`WholeLife_US_S`'s month 119, and its frame has 552 rows, `t = 0 … 551`. Point 19 is the
loan variant in force 114 months, six months into policy year 10: its tenth anniversary
falls at `t = 5`, its next premium, policy year 11's $1,800, at `t = 6`, and its frame has
546 rows. Point 22 is point 2 to be issued three months after the valuation date:
`duration_mth(0) = −3`, it is on the books from `t_entry() = 3`, rows 0 to 2 are zeros,
and its frame has 663 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the premium-paying period and the months instalments fall due, the guaranteed cash value schedule and its interpolation, the net single premiums and theirs, guaranteed mortality at the attained age and the scale and best-estimate rates built on it, the lapse schedule and its final-year zero, the dividend declaration and its first year, loan-interest capitalization, the purchases of the PUA rider and the REDUCE_PREM excess, the graded death benefit's policy years 1–2, maturity at attained age 100 | expense inflation, `inflation_factor(t) = 1.02^(t/12)` |

The interest-sensitive lapse overlay reads a constant, `competitor_rate`, so it is on
neither clock, and the product has no scenario table. Expense inflation alone runs on `t`,
so the maintenance charge is in valuation-date dollars, for every point alike.
Acquisition, 90% of the first year's annual premium plus $250, is charged per policy
issued, in the issue month, and not inflated, as in `basiclife/BasicTerm_SE`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
n = len(model.Data.model_point_table())
frames = [model.Projection[i].result_cf() for i in range(n)]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`WholeLife_US_S` computes, whatever the point's count: `WholeLife_US_S` already charges
acquisition on the policies in force at its `t = 0`, which on new business are the
policies issued. On `WholeLife_US_S`'s fourteen new-business points every cash flow and
every count agrees, and so does every other cell the two models share but three whose
meaning changed: `pols_if_init()`, now the count already in force at the valuation date,
0 for new business; `model_point()`, a row of another table; and `result_pols()`, which
gains `pols_new_biz`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `WholeLife_US_S`'s
columns, and nine of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s
two, and seven that open an in-force policy's state. Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `pua_face_init` | dollars of paid-up face | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the paid-up additions in force |
| `loan_bal_init` | dollars | the start of month 0 | the policy loan outstanding, capitalized interest included |
| `div_accum_init` | dollars | the start of month 0 | the dividend accumulation balance, interest and dividends to date included; 0 unless the option is ACCUM |
| `pua_face_prev_anniv_init` | dollars of paid-up face | the anniversary that opened the policy year under way, on or before the valuation date: the close of policy month `12 × duration(0) − 1` | the paid-up additions entering the policy year, which its PUA-block dividend and its term-blend gap read |
| `loan_bal_prev_anniv_init` | dollars | that anniversary | the loan entering the policy year, on which the year's interest capitalizes and which the dividend's interest margin credits at the loan rate |
| `div_prev_anniv_init` | dollars | that anniversary | the dividend credited there, which `div_prev_anniv` returns through the year under way, and so the year's premium offset and its REDUCE_PREM excess read |
| `prem_cum_init` | dollars | the start of month 0 | the gross premium, before any dividend offset, of every instalment due from issue to policy month `duration_mth − 1`, which the graded final-expense death benefit reads |

The seven state columns are 0 on a point issued at or after the valuation date, the
values at issue. In the first policy year, `duration_mth` 1 to 11, the three anniversary
columns hold their issue values, 0, because that year opened at issue, and
`div_accum_init` is 0 too, because no dividend has been credited yet. On a point valued
on an anniversary, `duration_mth` a multiple of 12, the two `_prev_anniv_init` columns
are the same instant as `pua_face_init` and `loan_bal_init`, and must equal them.
`prev_anniv` is `WholeLife_US_S`'s word, as in its `div_prev_anniv`: the anniversary that
**opened** the policy year, where `anniv` alone, as in `is_anniv` and `anniv_mth`, is the
one that ends it. An extract that fills the three anniversary columns from the
anniversary after the valuation date is a year out.

Everything else the projection uses is fixed at issue, in `WholeLife_US_S`'s columns, or
follows from the policy clock: the cash value is read from the guaranteed schedule by
policy year, the net single premiums and the mortality by attained age, and the premium
from the model point or, on final expense, from the rate table.

| `WholeLife_US_S` | `WholeLife_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_inforce` (whole policy years) | `duration_mth` | The policy clock, in months, so that a policy can be valued in any month of its year; the S column is dropped |
| `puaf_inforce` | `pua_face_init` | Renamed in place, so that the seven state columns share one vocabulary: a column measured entering month 0 is the cell it opens with `_init` added, and so is `div_prev_anniv_init`, `div_prev_anniv`'s value through the year under way; a balance measured at the anniversary adds `_prev_anniv_init` |
| `loan_inforce` | `loan_bal_init` | The same |
| — | `pua_face_prev_anniv_init` | `WholeLife_US_S` opens its in-force frame on an anniversary, where this is `puaf_inforce` |
| — | `loan_bal_prev_anniv_init` | The same, with `loan_inforce` |
| — | `div_accum_init` | `WholeLife_US_S` opens the accumulation balance at 0, the notes' `DA = 0` |
| — | `div_prev_anniv_init` | `WholeLife_US_S` takes last year's dividend as 0, an anniversary before its frame |
| — | `prem_cum_init` | `WholeLife_US_S` sums the premiums paid from issue, whatever its frame |

On the twins the five new columns take what `WholeLife_US_S` itself assumes, so each twin
opens as its S row does: on point 1 the paid-up additions at the anniversary are its
4,100, the loan 0, the accumulation balance and last year's dividend 0, and the premiums
paid 16,200, nine years at $1,800.

The columns carried over are read as `WholeLife_US_S` reads them. For a policy in force,
the facts they record are still those at issue, the dividend option and the premium mode
excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `product`, `premium_period`, `sex`, `risk_class` | codes, as in `WholeLife_US_S`'s table | issue |
| `issue_age` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `face_amount` | dollars, level for the life of the policy | issue |
| `annual_premium` | dollars a year, the participating design's `G`; blank on final expense, whose premium comes from `premium_rates.csv` | issue |
| `dividend_option` | `PUA`, `CASH`, `ACCUM`, `REDUCE_PREM`, or `NONE` on final expense | the option in force over the frame |
| `premium_mode` | `A`, `SA`, `Q` or `M` | the mode billed over the frame; its instalments fall on the policy clock |
| `pua_rider_premium` | dollars a year, level while premiums are payable | issue |
| `term_blend_target` | dollars of target face, 0 for no blend | issue |
| `loan_utilization` | a fraction of the guaranteed cash value | an assumption, not a fact about the policy |
| `provenance` | text: `WholeLife_US_S`'s on a twin, the generator's on any other row | — |

The loan is not carried forward as a balance. `WholeLife_US_S` holds it at
`loan_utilization × CV_t` in every month of its frame, and this model does the same from
month 0 on, whatever `loan_bal_init` says. That column is what month 0's advance,
`loan_draw(0)`, is measured from, and what the death benefit of month 0 deducts, so the
advance closes any gap between the extract's loan and the fraction: point 19 owes
2,070.00 entering month 0 and 2,098.33 at its end, an advance of 28.33.

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the nine in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is below `2**53` months, which an int64 and a float both hold exactly,
  so that numpy never casts it to the least int64, a policy issued `2**63` months on;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,320 months at issue age 0, the youngest the product
  issues, and 780 at 45, the youngest the shipped tables carry. Set to 0, the Reference
  refuses future new business altogether, and a negative horizon is itself refused;
- each opening-state column is a number, zero or more;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros;
- the non-participating final-expense design has no paid-up additions,
  `pua_face_init` and `pua_face_prev_anniv_init`, and no dividend, `div_prev_anniv_init`;
- only the ACCUM option has an accumulation balance, which on any other the projection
  would drop from every benefit;
- on a point valued on an anniversary the two `_prev_anniv_init` columns equal
  `pua_face_init` and `loan_bal_init`;
- in the first policy year, which opened at issue and has credited no dividend yet, the
  three anniversary columns and `div_accum_init` are 0.

A row whose paid-up additions at the anniversary exceed those entering month 0 is
accepted. The model never shrinks the block, so such a row records a partial surrender
of additions, which the model does not implement, and it is projected from the values it
gives.

A point whose cover had ended by the valuation date,
`duration_mth ≥ 12 × (100 − issue_age)`, reads, but `proj_len()` refuses it, naming the
point: the end of cover is the product's rule, not the table's. So a loop over the block
meets such a row only when it reaches it, after projecting the points before it.
`run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`WholeLife_US_S` and its table by `tests/sec_support.py`, from the `WholeLife_US_SEC`
entry in its `SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a
`WholeLife_US_S` row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py WholeLife_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1 | twin | S point 1 | the anchor cell in force 108 months, on the anniversary opening policy year 10, with its 4,100 of paid-up additions: the worked example's year |
| 2–15 | twin | S points 2–15 | issued at `t = 0`: `WholeLife_US_S`'s new business, under each dividend option, with a loan, the PUA rider, the term blend funded and unfunded, limited pay, the female cell, final expense level and graded, and monthly mode |
| 16 | derived | S point 5 at S month 108 | REDUCE_PREM on the anniversary opening policy year 10, last year's dividend 288.66 |
| 17 | derived | S point 4 at S month 108 | ACCUM on the same anniversary, with 1,766.74 accumulated |
| 18 | derived | S point 8 at S month 78 | the funded term blend six months into policy year 7, before its crossover: 106,074.52 of paid-up additions, 93,241.47 at the anniversary |
| 19 | derived | S point 6 at S month 114 | the loan variant six months into policy year 10: a loan of 2,070.00, 1,900.00 at the anniversary |
| 20 | derived | S point 12 at S month 18 | the graded final-expense plan inside its graded years, with 3,162.00 of premiums paid |
| 21 | derived | S point 5 at S month 659 | REDUCE_PREM in its last month of cover: a one-row frame |
| 22 | future | S point 2, 3 months on | to be issued at `t = 3` |

A derived row's `policy_count` is the count `WholeLife_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `WholeLife_US_S` carries into it, each column
read as `WholeLife_US_S`'s own formulas read it: the paid-up additions, the loan and the
accumulation balance at the close of S month `d − 1`; the paid-up additions and the loan
at the close of S month `anniv_mth(d) − 12`, the anniversary that opened the policy year
of `d`; S's `div_prev_anniv(d)`; and S's `prem_cum(d − 1)`. So the row continues the S
projection from there: points 16 and 17 open with 0.704576 policies, and point 21 with
0.041820. Its `policy_id` is the S row's with the month appended, `WLPAR-000005-M108`,
and a future row's carries the months to issue, `WLPAR-000002-F3`. Row `t` of a
generated point is month `t + source_mth` of its S point. All 22 are at issue age 45 on
the participating design or 65 on final expense, the only issue ages `cv_table.csv`
carries, so a point at any other needs the schedules extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order, each an int Reference named as the string
`basiclife/BasicTerm_SE` or `WholeLife_US_S` passes, so that a timing, like every
argument, is a C number when the model compiles:

- `BEF_NB = 0`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR = 1`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_SURR = 2`, after the month's deaths;
- `BEF_MAT = 3`, after its surrenders;
- `AFT_DECR = 4`, after the maturities of the last covered month, the notes' `l_{t+1}`.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `WholeLife_US_S`'s,
unchanged but for their guard outside cover and, in `AFT_DECR`, the last covered month
read on the policy clock. Any other timing raises. One name means two instants in the two
references: `BasicTerm_SE`'s `"BEF_MAT"` counts the policies at the **start** of a month,
before that month's maturities, where `WholeLife_US_S`'s counts them at its **end**, after
the month's surrenders. The policies here mature at the end of the last covered month, as
in `WholeLife_US_S`, so the name keeps the S meaning, and `BasicTerm_SE`'s timing is not
adopted.

The survivors carried into month `t` are those of month `t − 1`'s `BEF_DECR` count,
which `BEF_NB` forms itself, as its own value at `t − 1` plus that month's new business,
through the month's deaths and surrenders in the order `BEF_MAT` takes them. So
`pols_if_at(t, AFT_DECR)` is `pols_if_at(t + 1, BEF_NB)` at every `t` of every frame,
and it is `pols_if(t + 1)` except where month `t + 1` is an issue month, whose new business
joins `pols_if`. The chain of calls from month `t` back to `t_entry()` is one cell a month,
where `WholeLife_US_S`'s ran through five: on a model just read, a cold `net_cf` in the
last month of a 660-month frame runs 671 cells deep, against 3,304 in `WholeLife_US_S`, so
modelx needs a recursion limit of 670 for it. On the longest frame the shipped tables
allow, 780 months for point 2 issued 120 months on, it runs 671 deep too, because the
chain stops at the issue month, and on the longest cover the contract allows, from issue
age 0, issued now or 120 months on, 1,211 deep (*The compiled model*, below). Each report
evaluates its columns in ascending `t`, and a sweep of the committed points that way runs
under a recursion limit of 28.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `WholeLife_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `WholeLife_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × (100 − issue_age)` is `WholeLife_US_S`'s frame from issue. Outside
it, before issue and from maturity on, every count is zero, and so every cash flow, every
value state and every dividend. No count evaluates a decrement rate there, and no table is
read at a policy year or an attained age the policy does not have: `is_anniv` and
`prem_due` are false, and `premium_pp_ann`, `rider_premium_pp_ann`, `prem_cum`, `cv_pp`,
`nsp_mth`, `mort_rate_guar`, `div_prev_anniv`, `div_credited`, `oyt_face`, `div_to_pua`,
`div_accum`, `pua_face_offset`, `pua_face`, `pua_cv`, `loan_bal`, `loan_draw` and the
death benefit are zero before any table is read. Every other value is zero through them.

## The opening state

`WholeLife_US_S` opens an in-force point on an anniversary, from three columns,
`duration_inforce`, `puaf_inforce` and `loan_inforce`, and assumes the rest: no
accumulation balance, no dividend at the anniversary before its frame, and premiums
summed from issue. That is all the worked example's policy year 10 needs. A policy valued
at any month of its life needs all seven state columns, each what `WholeLife_US_S` carries
into that month, and each shows on a derived row:

- **`div_prev_anniv_init`.** Point 16, on REDUCE_PREM, is valued on the anniversary opening
  policy year 10. It pays 1,800.00 less last year's dividend of 288.66 at `t = 0`, so
  1,511.34 a policy, as `WholeLife_US_S` collects at its month 108. With the column at 0
  it would pay 1,800.00.
- **`div_accum_init`.** Point 17, on ACCUM, is valued on the same anniversary with
  1,766.74 accumulated, which earns its monthly interest from `t = 0` and reaches the
  death, surrender and maturity benefits. With the column at 0 the balance would be lost
  from every benefit, and the maturity claims of its last month alone would be 1,060.82
  lower.
- **`prem_cum_init`.** Point 20, the graded final-expense plan valued six months into
  policy year 2, has paid two annual premiums of $1,581, 3,162.00. To the end of the
  graded years, `t = 5`, its death benefit is
  `0.97 × 1.1 × 3,162.00 + 0.03 × 15,000 = 3,823.85`, and from `t = 6`, policy year 3, the
  face. With the column at 0 it would be 450.00.

A valuation off an anniversary needs the year's opening values as well, because the
annual quantities of a policy year read the balances entering it, and inside the year
those have moved on:

- **`pua_face_prev_anniv_init`.** Point 18 is the funded term blend six months into policy
  year 7. The year's rider instalment, paid at its start, has bought 12,833.05 of
  additions since the anniversary, so the point holds 106,074.52 entering month 0 against
  93,241.47 at the anniversary. The one-year-term layer of the year is sized on the
  second: `200,000 − 100,000 − 93,241.47 = 6,758.53`, which the year's dividend funds in
  full, so the death benefit of month 0 is `100,000 + 106,074.52 + 6,758.53 = 212,833.05`,
  `WholeLife_US_S`'s at its month 78. On the current additions there would be no gap at
  all.
- **`loan_bal_prev_anniv_init`.** Point 19, the loan variant six months into policy year
  10, owes 2,070.00 entering month 0 against 1,900.00 at the anniversary. At its tenth
  anniversary, `t = 5`, the year's interest capitalizes on the second, 6% of 1,900.00,
  114.00. The dividend's interest margin reads the same 1,900.00, though at the shipped
  rates, 6.00% on the loan and on the dividend alike, the loan cancels out of it.

On a point valued on an anniversary each pair is one instant, and `Data` refuses a row
where they differ. Off an anniversary they differ wherever the year has moved the balance
since it opened: by the rider's purchases, by the REDUCE_PREM excess, which buys additions
in the year's first month, and, for the loan, every month with the cash value. Point 21,
REDUCE_PREM in its last month, holds 4,823.37 of additions against 4,544.40 at its
anniversary.

`WholeLife_US_S`'s goldens on its point 1 read four values from the month before its
frame: `pua_face(107)`, `loan_bal(107)`, `cv_pp(107)` and `pua_cv(107)`. On the twin no
month comes before the frame, and each is opening state at `t = 0`: `pua_face_init()` is
the 4,100, `loan_bal_init()` 0, `cv_pp_anniv(9)` 9,500, the guaranteed cash value entering
policy year 10, and `pua_face_prev_anniv_init() × nsp(54)` 1,648.93, each `WholeLife_US_S`'s
value. The worked example's year then runs as in `WholeLife_US_S`: the dividend of 326.25
credited at `t = 11` brings the paid-up additions to 4,876.79, `WholeLife_US_S`'s
`pua_face(119)`.

## Departures from WholeLife_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock or of the opening
state, and every recursion begins at `t_entry()`. Where `WholeLife_US_S`'s test would have
stayed correct on the valuation clock, it moved anyway, so that cover has one definition.
Running in force left 40 of `WholeLife_US_S`'s 97 cells unchanged, one of them,
`dyn_lapse_factor`, with a line re-wrapped, gave 9 a new docstring only and rewrote 44; it
renamed two and removed two, and added 11 cells, 106 in all. Compiling then changed how
each cell reads its inputs and spells its codes, and no number, and added 12 cells, 118 in
all (*The compiled model*, below); of `WholeLife_US_S`'s cells it changed the signature of
one, `claims`. The twin identity names each of the five, with its reason: a cell of
`WholeLife_US_S`'s that this model lacked, or took other arguments, would fail it
otherwise. Some departures come from compiling rather than from the clock: `proj_len`'s
second refusal and the last three rows below.

| Cells | `WholeLife_US_S` | `WholeLife_US_SEC` | Why |
|---|---|---|---|
| `duration_mth` | `t` | `duration_mth_init() + t` | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth` | `12 × (100 − x)`, the months from issue | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises at or past maturity, and on a point issued below `issue_age_min`, 0 | The frame starts at the valuation date. `maturity_mth()` is new and keeps `WholeLife_US_S`'s formula, and the compiled caches hold the contract's frames alone |
| `proj_start`, `duration_inforce` | an in-force frame opens at `12 × duration_inforce()`, the elapsed policy years | removed: every report and check runs over `range(proj_len())` | Every frame opens at `t = 0`, and `duration_mth_init()` replaces the elapsed years |
| `puaf_inforce`, `loan_inforce` | the in-force point's opening paid-up additions and loan | renamed `pua_face_init` and `loan_bal_init` | One vocabulary for the seven state columns |
| `pols_if`, `pols_if_init`, `pols_if_at` | a recursion from `pols_if_init()`, the column's 1.0, at `proj_start()`, five cells a month | `pols_if_at(t, BEF_DECR)`, from `t_entry()`, one cell a month; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `pua_face`, `div_accum`, `loan_draw`, `claim_pp(·, DEATH)`, `check_pua_roll_fwd_resid` | open at `proj_start()` from `puaf_inforce()`, 0 and `loan_inforce()` | open at `t_entry()` from `pua_face_init()`, `div_accum_init()` and `loan_bal_init()` | Every recursion begins on the books, from the opening state |
| `prem_cum` | a recursion back to issue | opens at `t_entry()` from `prem_cum_init()` | No cell asks for a month before the valuation date |
| `div_prev_anniv` | `div_credited(12 × duration(t) − 1)`, a policy month passed as `t`; 0 before the frame | `div_credited(anniv_mth(t) − 12)`, or `div_prev_anniv_init()` where that month is before `t_entry()` | On the valuation clock month `12 × duration(t) − 1` is not the anniversary |
| `anniv_mth` | `12 × duration(t) + 11`, a policy month | `t + 11 − duration_mth(t) % 12`, a valuation month | The same |
| `div_int` | the cash value `cv_pp(t − 12)`, in any month | `cv_pp_anniv(duration(t))`, and the loan from `loan_bal_prev_anniv_init()` where `t − 12` is before `t_entry()`; zero but at an anniversary | `cv_pp(t − 12)` is a month before the valuation date in a point's first projected year. At an anniversary, the one month its dividend reads it, the two cash values agree to within an ulp. In any other month nothing reads it, and before issue it would read the schedule at a negative policy year |
| `div_pua`, `oyt_face`, `loan_int` | the balance twelve months back, or `puaf_inforce()` and `loan_inforce()` before the frame | the same, or `pua_face_prev_anniv_init()` and `loan_bal_prev_anniv_init()` where that month is before `t_entry()` | A policy year under way at the valuation date opened before it |
| `pua_face_rider` | a mid-year instalment priced at `nsp_mth(t − 1)` | the same straight line, written at the start of month `t` | At `t = 0` on a valuation off an anniversary, `t − 1` is before the valuation date. The arithmetic is the same |
| `lapse_rate`, `cv_pp_anniv` | the years to maturity as `proj_len() // 12` | `maturity_mth() // 12` | `proj_len()` now counts from the valuation date |
| `expenses` | acquisition, `0.9 G + 250` at `t = 0`, on the policies in force there | `(0.9 G + 250) × pols_new_biz(t)` | A point already in force bears none, and one issued later bears it in its issue month, per policy issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `inflation_factor` | `1.02^(t/12)`, `t` the policy month | the same formula, `t` the valuation month | Unit costs in valuation-date dollars |
| `check_pols_roll_fwd_resid`, `check_pols_roll_fwd` | `pols_if(t) − pols_if(t + 1) − …`, the tolerance scaled by `pols_if_init()` | `pols_if(t) − pols_if_at(t + 1, BEF_NB) − …`, scaled by `policy_count()` | Next month's new business is no part of month `t`'s movement, and `pols_if_init()` is 0 on new business |
| `div_to_pua`, `claim_pp(·, MATURITY)`, `pols_maturity`, `pols_if_at(·, AFT_DECR)` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `is_anniv`, `prem_due`, `premium_pp_ann`, `rider_premium_pp_ann`, `cv_pp`, `pua_cv`, `nsp_mth`, `mort_rate_guar`, the dividends and the counts | unguarded, or guarded by `t` against 0, `proj_start()` or `proj_len()` | false or zero outside cover, `is_active(t)`, before any table or rate is read | A future point's months before issue have `t ≥ 0`, and policy month −1 is no anniversary |
| `result_cf`, `result_cv`, `check_pua_roll_fwd` | `range(proj_start(), proj_len())` | `range(proj_len())` | Every frame opens at `t = 0` |
| `result_cf_annual` | whole policy years | the policy years in the frame, the months before issue left out | An in-force point's first row holds the rest of its current policy year, and its `pols_if` is the count at the valuation date |
| `result_pols` | `pols_if`, the three outflows and four rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()`, and no rate read before issue |
| `claims` | `claims(t, kind=None)`: one kind's claims, or with `None` the three summed by Python's `sum` | `claims_death(t)`, `claims_lapse(t)` and `claims_maturity(t)`, the `result_cf` columns, and `claims(t)` their total, `0.0 + death + lapse + maturity` | A compiled cell takes C numbers, and `None` is none. Python's `sum` of floats is compensated, so a total written out is its float only where at most two kinds are non-zero, and that holds in every month: maturities fall in the last covered month alone, where `lapse_rate` is 0. A test holds the total to `WholeLife_US_S`'s bit for bit |
| `div_base`, `div_round_digits` | `None` turns the rounding off | an int, 2 as shipped, and a count below −400, −1,000 say, turns the rounding off | `None` is no C number. Every other count rounds as `WholeLife_US_S` rounds, a negative one to tens, hundreds and so on, and 0 to the dollar. The two part only below −400, where `WholeLife_US_S`'s `round` gives 0.0 for every float, as it does from −309 digits down, and here the dividend is unrounded |
| `Data` and the cells that read a table | a malformed value or key met, if at all, only when a projection reaches it, and a key beyond a table as `KeyError` | refused by name at the first read of the array, over the whole table, and a key beyond a table refused by the cell that reads it, naming the point | A compiled model holds numbers, not text, and computes a NaN as silently as modelx (*What it refuses*, below) |

The other new cells of running in force are `policy_count`, `duration_mth_init`,
`t_entry`, `is_active`, `pols_new_biz` and the five new opening-state accessors; those of
compiling are listed under *What compiling changed, and why*, below.

One read goes further ahead than the month after its own, and it is kept.
`oyt_face(t)` sizes the term-blend layer of the policy year containing `t` on the dividend
credited at the anniversary that ends it, `div_credited(anniv_mth(t))`, up to eleven
months ahead, because the one-year term in force through the year is bought with that
dividend. It opens no chain forward: the dividend depends on the balances entering the
year and on the schedules alone, never on the layer or on a later month, and the frame
ends on an anniversary, so the read never leaves it.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
and `liability_cf` with it. A point in force carries that expense in valuation-date
dollars, so point 1's `expenses(t)` is `WholeLife_US_S`'s `expenses(108 + t)` divided by
`1.02^9`, about 1.195. Its other cash flows and its counts are `WholeLife_US_S`'s from
month 108 on. Point 22 is `WholeLife_US_S`'s point 2 three months on in those columns too;
its maintenance expense is `1.02^(3/12)` above S's, and its acquisition, 1,870.00, is
S's exactly.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, on the points of the splice
grid, which take the branches they do not, on the contract's longest frames, and on
points where the cap on mortality binds. The compile tests hold it so on x86-64, and to
1e-12 relative elsewhere, where no run has shown it yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py whole_life                   # in place, beside the model
python tools/build_sec_cy.py whole_life --out /tmp/wl     # elsewhere, with the CSVs
```

The tool exports the model to `WholeLife_US_SEC_nomx/`, the Python package modelx's
`export` writes, which runs without modelx. It copies the CSVs beside the export when it
builds anywhere but here, because the package reads the CSVs of the directory that holds
it. It then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `WholeLife_US_SEC_nomx_cy/`, whose spaces are C
extension types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/whole_life")     # the directory holding the build
from WholeLife_US_SEC_nomx_cy import mx_model as model
model.Projection[18].result_cf()              # point 19, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 18` after `Projection.result_cf()` returns
point 1's frame under point 19's `point_id()`, and `Projection.div_round_digits` set to
−1,000 once `Projection[0]` has credited point 1's tenth dividend leaves it rounded there,
326.25, where an ItemSpace made after computes 326.248. Set every Reference on a model
just imported, before anything is computed, where modelx would recompute; a test holds
the compiled model to this.

A build takes about a minute and a quarter with gcc, 80 s here, and needs a C compiler,
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
typed 95 of its 106 `Projection` cells as C numbers, but three of them still took a
timing or a kind as text, and so kept a dictionary for a cache, and it ran only 1.4 times
its own export, 18.5 ms a point on `net_cf` against 25.9, over the committed points. The
bodies of the typed cells still called pandas and Python: a `model_point()` lookup for
each attribute, a `.loc` on a table for each policy year's cash value, each attained
age's mortality and net single premium and each point's final-expense rate and net level
premium, text compared in every formula that branched on the product, the premium
period, the premium mode or the dividend option, and a generator summed in `claims`. So
each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[18]` is point 19, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.issue_age()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column into
  the number it selects, for every point at once: the product into two flags, `is_par`
  and `is_graded`; the premium period and the dividend option into their codes; and the
  premium mode into the months between instalments, `prem_cycle`, by which
  `modal_factor` selects the mode's factor. Each decodes as `WholeLife_US_S` reads the
  column: a dividend option that is none of the four is `NONE`, as `WholeLife_US_S`
  applies such a dividend to nothing, and what cannot be decoded is refused (below).
- **Tables indexed by integers.** The cash value schedules, keyed by premium period, sex
  and issue age, are numbered, each point carrying the number of its own, `cv_schedule`,
  and held by schedule and policy year in `cv_array`. The guaranteed mortality and the net
  single premiums, keyed by sex and attained age, are numbered by sex the same way and held
  by schedule and age in `mort_table_array` and `nsp_array`, padded from age 0 so that the
  index is the attained age. The padding holds NaN, and nothing reads it: the one cell that
  reads each table checks its key against the schedule's extent first. The final-expense
  rates and the net level premiums are one number a point, and read by one design alone,
  so each is joined to the points in `Data`, with a 0/1 flag beside it, and the one cell
  that reads it, `premium_rate` or `np_guar`, refuses a point the table has no key for,
  where `WholeLife_US_S`'s `.loc` raised `KeyError`. `Data` refuses neither, because
  `WholeLife_US_S` projects a participating point with no final-expense rate.
- **Codes.** A timing, a kind, a premium period or a dividend option, which
  `WholeLife_US_S` spells as text, is an int Reference named as the text: `BEF_NB = 0`
  to `AFT_DECR = 4`, `DEATH = 0`, `LAPSE = 1` and `MATURITY = 2`, `TO_100 = 0` to
  `TO_65 = 3`, and `PUA = 0` to `NONE = 4`. A call reads as before, less the quotes:
  `pols_if_at(t, BEF_DECR)`, `claim_pp(t, DEATH)`. A string argument or a string value
  would give the cell a dictionary for a cache, where a code indexes a C array, so codes
  are numbered from 0 without a gap, the timings in the order of their instants within
  the month and the kinds in the order the month settles them. The `Projection`
  docstring's *Codes* lists all seventeen.
- **The claims, split.** `WholeLife_US_S`'s `claims(t, kind=None)` is one kind's claims or,
  with `None`, the three summed by a generator: neither a C parameter nor a C loop. Here
  the kinds are three cells, `claims_death`, `claims_lapse` and `claims_maturity`, the
  `result_cf` columns, and `claims(t)` is their total (*Departures from WholeLife_US_S*,
  above).
- **One Python call kept.** `div_base` rounds the dividend to `div_round_digits` places
  with Python's `round`, which cannot be computed ahead, since the amount is projected.
  Compiled it is the same call, so the dividend is the same float, and
  `tests/us_registry.py` admits it, by its key `"python_calls"`, in that cell alone. The
  digits are an int, and a count below −400 turns the rounding off, where
  `WholeLife_US_S` takes `None`; every other count rounds as `WholeLife_US_S` rounds.
- **Reporting cells stay Python.** `model_point()`, the label accessors `product()`,
  `premium_period()`, `sex()`, `risk_class()`, `dividend_option()` and `premium_mode()`,
  and the four reports return a table row, text and DataFrames, for a reader, for
  `run_sec.py` and for the comparison with `WholeLife_US_S`. No other cell calls them, so
  they cost the projection nothing. A label accessor returns its column as read, and
  `Data` accepts a label that is blank, which pandas reads as NaN, or a number, on a point
  that carries no paid-up additions, dividends or rider premium, and the point's first
  projection refuses it. So each of the six compiles to a Python object, as the sample
  traces it (below), and returns what modelx returns (precised at M26). The two checks are
  reporting cells too, but they return a verdict, which compiles to a C `bint`.

The `Data` docstring lists its 42 vectors, arrays, extents and counts, each with the column
or file it comes from: 19 vectors of int64, 15 of float64, three tables of float64 and five
counts. The seven readers stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 107 of
its 118, returns a C `bint`, `long long` or `double`, and caches a single value, or a C
array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,322 by `t`, of `double`, `long long` or `bint` | the 66 cells of `t` alone: every count, rate, factor, premium, value, dividend, claim and cash flow; the policy clock, its years, the attained ages and the anniversary month; the flags `is_active`, `is_anniv` and `prem_due`; and the checks' monthly residuals |
| a C array of 1,322 by 5 | `pols_if_at(t, timing)`, and `claim_pp(t, kind)`, whose three kinds leave two columns unused (*The sample and the spec*, below) |
| a C array of 102 by `y` | `cv_pp_anniv(y)`, by policy year, and `nsp(y)` and `mort_rate_guar_at(y)`, by attained age |
| one `long long`, `double` or `bint` | the 36 cells without a parameter: the point's numbers, codes, schedules and flags, its opening state, the ends of its frame, its premium rate, modal factor and net level premium, and the two checks |
| a Python object | the eleven reporting cells but the checks |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell the
run never calls compiles as a Python object. So `sample_sec.py` runs the four reports and
the two checks on every committed point, and then the eleven cells no report reaches, and
the one timing: `model_point()` and the six label accessors, which only a reader asks for;
`point_id()`, which only a refusal names; `mec_flag()` and `policy_year(t)`, which no cell
reads; `dyn_lapse_factor(t)`, which the lapse rate reads only with its overlay switched on,
and it ships off; and `pols_if_at`, a cell the reports reach, at `AFT_DECR`, the one timing
no formula asks for, in every month of the frame and the month after it, with the count
`pols_if_at` carries into that month. It runs the committed points alone: the export it runs
reads the CSVs of the directory the build is made in, which in place is the product
directory, so points of its own would have to be written there. The committed points leave
branches untaken: the semi-annual and quarterly cycles, the twenty-year and to-65 premium
periods, the three overlays and the dividend on the paid-up additions, all shipped off,
rounding switched off, the cap on mortality. That still types every cell, because every
branch of a cell returns the one type its others return, a count a float in every branch,
and on points that take those branches the compiled model computes modelx's numbers (above).
The label accessors are typed from more than the committed points: the sample also calls
the six on a copy of the first point with every label blank and its paid-up additions,
dividends and rider premium 0, written to a temporary directory and read by a second
instance of the export, so that each compiles to a Python object (M26). The sample also
raises the recursion limit, which modelx raises and its export does not (*What a compiled
run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forward reads and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and one of headroom where that leaves room:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,322 | 1,321. The longest frame is a policy issued at the youngest issue age, 0, covered to 100 for 100 policy years, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 100 + 120 = 1,320 months, `t = 0 … 1,319`, and the month after, 1,320. The count roll-forward's residual there reads the count carried into the month after that, 1,321. No headroom |
| `t`, `timing` | 1,322 by 5 | `t` as above, by the five timings, so a code past `AFT_DECR` raises |
| `t`, `kind` | 1,322 by 5 | `t` as above, by the three kinds and two columns more, so that both 2-D caches have timing's width. Cython's generated unpickle code converts a space's 2-D caches with one function, written for one width, and given 1,322 by 3 beside 1,322 by 5 it passed the narrower where the wider was expected, which gcc 14 refuses and which would write past its end. A kind of 3 or 4 is then inside the cache, where `claim_pp` refuses it as modelx does, and one from 5 raises |
| `y` | 102 | 100, shared by three cells: the policy year `cv_pp_anniv` reads, up to 100 at issue age 0, and the attained age `nsp` and `mort_rate_guar_at` read, up to `maturity_age`, 100. Each is read inside cover alone, so none in the month after the frame |

`proj_len()` refuses a point issued below 0, `issue_age_min`, in modelx as compiled, and
cover ends at `maturity_age`, 100, so no report on a point the model projects runs past
these caches. Those two References and `Data.future_horizon_mth` are the contract the sizes
are derived from. Lower the minimum, or raise `maturity_age` or the horizon past 120 months,
and a report runs past the caches in the compiled model alone: a frame longer than 1,320
months, or a policy year or an age past 101, raises `IndexError`, naming nothing, where
modelx projects. Each needs the sizes derived again, as `spec_sec.py` derives them, and a
rebuild: `t` raised to 12 × (`maturity_age` − `issue_age_min`) + the horizon + 2, and `y`,
which holds a policy year and an attained age, to the larger of their two derivations,
max(`maturity_age` − `issue_age_min`, `maturity_age`) + 2. The shipped tables carry
mortality and net single premiums from attained age 18 and cash values at issue ages 45 and
65 alone, so a point issued below 18 is refused today by the first table it reads, naming
it; an issue age of 0 is the contract's, which an extended table reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it
was measured to change there. Here `cpow` reaches four powers of two doubles: the monthly
rates of both decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`,
the monthly growth of the accumulated dividends, `(1 + i)^(1/12)` in `div_accum`, and
expense inflation, `(1 + r)^(t/12)` in `inflation_factor`. Without `cpow` a compiler with
C99's complex numbers, gcc among them, computes each as a complex power, which can differ
from Python's float power in its last bits. With both directives and the flag every
compiled value agrees with modelx's bit for bit, and the compile tests hold each, by the
module's first line, by the compiler's command lines and, on x86-64, by the comparison
itself. On the same platforms the tool adds `-Werror=incompatible-pointer-types`, so that
gcc before 14, which only warns of a pointer of the wrong type, fails the build as gcc 14
does: the error two cache widths gave (*The sample and the spec*, above).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 1,194,688
bytes, about 1.2 MB, the type's basic size, which holds every cell's cache: 66 arrays of
1,322 months and two of 1,322 by 5 make most of it. Deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a compile test holds a compiled block run to one point's ItemSpace at a time. Without
it, 506 compiled points peaked at 596 MB (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised. What it needs is stack. The deepest call the contract allows, a cold
`net_cf` in the last month of the longest cover, issue age 0, issued now or 120 months on,
runs the count chain back to `t_entry()`, 1,211 cells deep in modelx, one cell a month
and 12 more, and compiled with gcc it needs 288 KiB of thread stack. A test runs it in a
thread of 1 MiB, the stack Windows gives a program's main thread unless the program is
linked for more, and again on the main thread, which is where `run_sec.py --cython`
runs. MSVC's frames may be larger than gcc's, and the `cython` CI job, which runs the test
on Windows too, is the check on them: the test first runs the call at seven stacks, from
256 KiB to 2 MiB, and reports the smallest it ran on, so a first run there measures MSVC's
need. A stack below the need kills its child on an overflow, by design (with gcc, 256 KiB
does); on Windows the child ends with `STATUS_STACK_OVERFLOW`, and should Windows Error
Reporting hold it instead, the test waits two minutes for each bracketing child, and five
for the two it asserts, rather than the job's hour. The export recurses in Python instead:
the same call needs a recursion limit of about 2,450 there, and the four reports and the
two checks, which run in ascending `t`, need 128, so `sample_sec.py` sets 10,000, four
times the first rounded up to the thousand, and a test holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates.

- What `Data` cannot decode or hold, when the array is first read, naming every point at
  fault, or the schedule or the table: a `point_id` that is not a whole number, a premium
  period other than `TO_100`, `PAY_10`, `PAY_20` or `TO_65`, a premium mode other than
  `A`, `SA`, `Q` or `M`,
  `model_point_table_sec.csv: premium_mode must be A, SA, Q or M; it is not at point_id
  [2, 5]`; a cash value schedule whose policy years are not whole, leave a gap, repeat or
  start below 1, `cv_table.csv: the schedule of premium_period TO_100, sex M, issue_age 45
  must run in whole policy years from 1 or more, without a gap or a repeat`; a mortality
  or net single premium schedule with an age that is not whole, a gap, a repeated or
  negative age; an issue-age key of the cash values, the net level premiums or the rates
  that is not whole; a key of the net level premiums or the rates that appears twice.
  `WholeLife_US_S` met each only when a projection reached it. And, before it is cast to
  int64, a number of `2**53` or more in size, which numpy would cast to the least int64
  past int64: a model point's issue age, `model_point_table_sec.csv: issue_age must be
  below 2**53 in size; it is not at point_id [3]`, and a `duration_mth`, a policy issued
  `2**63` months on. A fractional issue age is not refused: it truncates toward zero, as
  `WholeLife_US_S`'s `int` truncates it, so 45.5 projects as 45, and −0.5 as 0, which
  is then issued, as in `WholeLife_US_S`. A key written as a float, a policy year `9.0`,
  is read by its value, as `WholeLife_US_S`'s lookups match it, and
  so are the keys each extent and join is taken from; a key written as text is not whole,
  and the table's check refuses it.
- A value a cap, a `min` or a `max` reads that is not a number in its range, when its
  array is first read, naming the file, the column and every line, key or point at
  fault, over the whole table, so that a value no point reads is refused as one that it
  reads is: through the dividend and the paid-up additions those bounds reach every
  amount and rate the projection reads. The face, the premium of the participating
  design, the rider premium and the blend target, a cash value, a net level premium and a
  final-expense rate must each be a number, zero or more; the loan share a number from 0
  to 1, `model_point_table_sec.csv: loan_utilization must be a number from 0 to 1; it is
  not at point_id [2, 5]`; a guaranteed mortality rate a number from 0 to 1,
  `mort_table.csv: mort_rate must be a number from 0 to 1; it is not at sex M, age
  [21]`; and a net single premium, which the purchases divide by, a number above 0.
- A key beyond a table, by the one cell that reads it, naming the point, where
  `WholeLife_US_S`'s `.loc` raised `KeyError`: `point_id 2: cv_table.csv has no cash
  value for policy year 1`, from `cv_pp_anniv`, on a participating point issued at 46;
  `point_id 2: mort_table.csv has no rate at attained age 45`, from `mort_rate_guar_at`,
  on a sex the table lacks; and `point_id 11: premium_rates.csv has no rate_per_1000 for
  its product, sex, risk_class and issue_age`, from `premium_rate`.
- By `proj_len()`, a point past its cover, `point_id 2: duration_mth 660 is at or past
  maturity, policy month 660`, and a point the contract does not issue,
  `point_id 2: issue age -1 is below issue_age_min, 0`.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1322)`, which modelx answers with 0, the month being outside cover;
`pols_if_at(0, 5)` and `claim_pp(0, 5)`, which modelx refuses as `invalid timing` and
`invalid kind`; and `cv_pp_anniv(-1)`, which modelx answers with 0. A kind of 3 or 4 is
inside `claim_pp`'s cache, and both engines refuse it as `invalid kind`. An `idx` past
the last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's
last point, under that point's own `point_id()`.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
best-estimate rate at 1, `min(q, 1.0)`, as `WholeLife_US_S` does. Uncapped, the monthly
rate, `1 − (1 − q)^(1/12)`, would be complex in modelx and NaN compiled, silently. Capped,
both compute 1. A NaN rate would stay NaN through the cap, in both, as through the
dividend's floor and the other bounds, each of which the compiled model computes as a
comparison that keeps the value unless the bound is smaller, or larger; `Data`'s
refusals of a value outside its range keep any NaN from reaching them.

### Speed

`python tools/bench_sec_cy.py whole_life` builds the model into a temporary directory, or
takes a build with `--build`, and times one block run on three engines: modelx, the export
and the compiled model. Each engine runs the committed table repeated, in a process of its
own, as `run_sec.py --block` runs a block, each point projected and then released.
`net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,006 | 0.53 ms (3.19–3.47) | 1.22 ms (7.32–7.60) | 88 MB |
| export | 616 | 7.4 ms (4.56–4.99) | 7.7 ms (4.76–5.09) | 88 MB |
| modelx | 132 | 274 ms (36.1–39.6) | 271 ms (35.8–41.8) | 137 MB |

On `net_cf` the compiled model runs 13.9 times its export, and on `result_cf`, where
building the DataFrame takes most of its time, 6.3 times; it runs 515 and 223 times
modelx. A second run straight after, under a 1-minute load between 1.2 and 2.8, gave the
compiled model 0.54 and 1.18 ms and the export 7.6 ms on both, 14.1 and 6.4 times, and
modelx 254 and 262 ms. As it stood after running in force, compiled the same way, the
model ran 1.4 times its export (*What compiling changed, and why*, above): the
representation, not the compiler, is the gain, as it was for `Term_US_SEC`, whose compiled
model runs 9.5 times its export on the same measure, with a C struct of about a third of
this one's, its frames shorter and its cells fewer. The release keeps a block flat: the
compiled model's peak grew by less than 0.1 MB over its 6,006 points, and without the
collection after each release (`--no-collect`), 506 compiled points peaked at 596 MB.
Reading the six files and building every `Data` vector and array for those points took
0.05 s, and asking every point for its frame, the runner's first pass, 0.13 s.

Measured on 2026-11-12 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.30 GHz), a 1-minute load average between 0.7 and 4.1 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Under load the spread is wide, and the fastest run is the
one to compare.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 2 to 15, issued
  at the valuation date, every cell of `WholeLife_US_S`'s agrees at every argument
  `WholeLife_US_S` evaluates in its own sweep, but for `pols_if_init`, `model_point` and
  `result_pols`, whose meaning changed, the four cells this model renamed or removed, and
  `claims`, whose arguments changed: each of its kinds is a column of `result_cf`, which
  the identity compares, and the module holds the total to `WholeLife_US_S`'s.
  So the goldens `tests/test_whole_life_us.py` asserts on those points — every dividend
  option, the loan, the rider, the term blend funded and unfunded, limited pay, the
  female cell, final expense and monthly mode — hold here with no number restated. Unlike
  `Term_US_SEC`'s, the identity holds on any count, since `WholeLife_US_S` already charges
  acquisition on the policies issued. The same suite holds the model to the conventions
  every `_SEC` model meets: every frame starts at `t = 0`, `pols_if` is the `BEF_DECR`
  count, new business enters once at its `policy_count`, nothing happens before issue,
  and the in-force columns are present.
- **The splice**, in `tests/test_whole_life_us_sec.py`: each `WholeLife_US_S` point
  restated in force at a month either side of its events continues the S projection, in
  `result_cf`, in `result_pols`, column by column, and in every other cell the two share,
  to 1e-9, but those the twin identity skips, `pols_if_init` and `model_point`, and those
  whose value is a month or a frame on the valuation clock, `proj_len`, `anniv_mth` and
  `result_cf_annual`. The participating points are restated at months 12, 108, 115, 119,
  120 and 600,
  the final-expense points at 12, 18, 23, 24, 115 and 400: inside the graded years, in
  their last month, in the first after them, and later. The funded blend is restated at
  78 and 83 too, before its crossover, and ACCUM, REDUCE_PREM and final expense level in
  their last covered month.
  So does the anchor cell's twin from S's month 108, and S's point 1 restated later in its
  life. So do three variants of S's points, in a copy of S's table that is never
  committed, for branches S's own points do not reach: the PUA rider paid monthly,
  REDUCE_PREM paid semi-annually, and the graded plan paid quarterly. Inflation, the one
  input on the valuation clock, is set to 0 in both models. Three switches that ship off
  are turned on in both, the PUA-block dividend, the premium-offset overlay and the
  interest-sensitive lapse overlay, and the loan rate is set apart from the dividend rate,
  because at the shipped settings parts of the opening state show in one place alone: the
  additions at the anniversary in the term blend, last year's dividend under REDUCE_PREM,
  and the loan at the anniversary in its interest.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch above, every opening-state
  column, every kind of valuation month and every premium mode, and a test asserts that
  they do. The other cases carry the `sec_full` marker and show as skipped, with the
  reason, unless `USLIB_SEC_FULL=1` is set. The `sec` CI job's Linux leg sets it, so every
  CI run runs the full grid too.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point
  is the S projection moved on, with zeros before issue in `result_cf`, `result_pols` and
  `result_cv` and no decrement rate evaluated there, and so is each variant issued a month
  on.
- **How it computes**: on every row the splice and the future business compare, the core
  by default and the full grid with `USLIB_SEC_FULL=1`, after every report, no cell has
  been called at a negative month, none evaluated from `t_entry()` on has read a month
  before it, and none evaluated at month `t` has read a month later than `t + 1` but
  `oyt_face`, which reads the year's dividend at `anniv_mth(t)` and nowhere else. On a
  fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, because the policy clock is a closed form, and every point is swept
  under modelx's recursion limit lowered to 60, which a recursion backward over the frame
  would exceed.
- **Counts, validation and regeneration**: the roll-forward closes, `AFT_DECR` is the next
  month's `BEF_NB`, and `pols_if_at` refuses a timing it does not have; `result_pols()`
  is `WholeLife_US_S`'s, column for column, with `pols_new_biz` beside it; doubling
  `policy_count` doubles every cash flow and moves no per-policy value; each malformed row
  is refused naming its point, a missing, negative or misplaced opening state among them,
  at either end of the first policy year and on the first anniversary; the horizon is a
  Reference, which at 0 refuses any future business, saying so; a point past its cover is
  refused by `proj_len()`, and `run_sec.py --block` refuses it before printing anything; a
  zero count, durations written as floats, balances written as whole numbers, a policy
  issued 120 months on, rows valued on the first anniversary and the month after, and a
  row whose additions at the anniversary exceed those entering month 0 are accepted; and
  the committed table is what `WholeLife_US_S` generates.
- **The opening state and the rest**: the twin of the worked example's point opens with
  the four values `WholeLife_US_S`'s goldens read before its frame, and at the shipped
  assumptions it is S's point from month 108 on, in every cell but those expense inflation
  moves, which carries the walk through policy year 10 over; the derived rows carry the
  dividend, the accumulation balance, the premiums paid and the anniversary values as
  above, and with the first three zeroed they give the 1,800.00, the shortfall of 1,060.82
  and the 450.00 above; expense inflation runs on the valuation clock at the shipped 2%,
  which only this test sees, since the splice sets the rate to 0; acquisition falls on new
  business alone; on `WholeLife_US_S`'s point 2 at an A/E of 5.0, where the product
  passes 1 at attained age 97, the rate is the float 1.0 in both models on four rows,
  three of them `WholeLife_US_S`'s in every cell, the capped months included, every policy
  in force dies in the first capped month and none is in force after it, and a NaN sent
  to the cap stays NaN; every guarded cell holds its value outside cover and reads no rate
  there, on the committed points and on the splice's future rows, which carry the rider,
  the blend and each dividend option before issue; the points of a block sum row by row;
  an extract without the generator's three columns projects the same numbers; and
  `run_sec.py` prints the model's numbers, for a point in force, a point restated, a point
  to be issued and the block, line by line, and sums the block as `groupby` does, bit for
  bit; and outside the repository, beside a copy of the model or at a path too shallow to
  hold one, `run_sec.py --cython` says it cannot build.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py WholeLife_US_SEC
  --check` makes the same comparison. The tests above held through the compile step with
  their call syntax changed: a point's position for its label, the codes for the text of
  a timing or a kind, and the three claims cells for `claims(t, kind)`. The extract is
  labelled 122 down to 101 rather than by position, and each point is named by its label,
  in `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: the claims total is `WholeLife_US_S`'s `claims(t)` bit for
  bit, sign of a zero and type included, and each kind its `claims(t, kind)`, on the
  fourteen new-business twins in every month, and in a month whose three kinds are all
  −0.0, set in both models, it is 0.0, as `WholeLife_US_S`'s `sum` gives; each premium
  period, on S point 9 at issue ages 30 and 50, decodes to `WholeLife_US_S`'s
  premium-paying years and MEC flag; a dividend option written `PAU` is `NONE` and the
  point is `WholeLife_US_S`'s in every cell; `div_round_digits` at −1,000 and at −401 is
  `WholeLife_US_S`'s `None`, and at −400, −2, −1 and 0 its own −400, −2, −1 and 0, on the
  anchor cell's twin from S's month 108; and a point issued below `issue_age_min` is
  refused by `proj_len()`, naming it, issue age −1 at the shipped bound and the anchor
  cell's twin, at 45, under a bound raised to 46, which projects at the shipped 0.
- **Decoding**: what cannot be decoded, a premium period or a mode, a `point_id` that is not
  whole, a table with a gap, a repeat, a key that is not whole or is written as text, a
  model point's issue age past int64, is refused naming the points, the schedule or the
  table, by the `Data` cell that reads it and by a projection; a table whose keys are
  written as floats projects exactly the committed numbers, as it does in `WholeLife_US_S`,
  and a model point's issue age of 45.5 projects as `WholeLife_US_S`'s point at 45, bit for
  bit, and −0.5 reads 0 and is issued; a key beyond a table, an age either side of the
  mortality and the net single premiums, a policy year past a schedule, an issue age, a sex
  and a final-expense key the tables lack, is refused by the one cell that reads it, naming
  the point; and the padding beyond each table's extent is NaN.
- **Values a bound reads**: each amount, share, probability and price above written
  blank, as text, as an infinity or outside its range, one at a time and two in one
  column, a value of a key no point carries among them, is refused naming the file, the
  column and every line, key or point at fault, by the `Data` cell that first reads it
  and by a projection; no other rule refuses the copy; and each edge of each range is
  accepted and projects.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting ones refers to pandas, numpy or another module, reads a table
  with `.loc` or the like, calls a reporting cell, holds text but in its docstring and its
  refusals, or holds a generator, a comprehension or a nested function; none calls
  anything but a cell, a `Data` vector and the builtins Cython turns into C, but for
  `div_base`'s `round`, which the registry admits by its cell, and a test holds every such
  admission to a builtin its cell does call; every `Data` vector a formula reads is an
  int64 or float64 array, read by element; no cell is uncached; and each label accessor
  returns its point's column of the same name.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting ones a C `bint`,
  `long long` or `double` and a C-array cache of exactly the spec's size, and every new
  `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps no
  Python object among a projection cell's locals, calls no Python builtin there but the one
  admitted, and builds no container, under both directives (C3); on the committed points,
  every cell at every argument a full modelx sweep caches is what modelx computes, bit for
  bit on x86-64, and so is every raise and every `Data` array (C4); and
  `run_sec.py --block`, run compiled, holds one point's ItemSpace at a time. In
  `tests/test_whole_life_us_sec.py`: the same comparison on the splice grid, the core by
  default and the full grid with `USLIB_SEC_FULL=1`, variants included, twenty rows at a
  time; on the contract's seven extremes, the five frames from issue age 0 and the oldest
  final-expense issue ages, with rounding off; and where the cap binds, and where a NaN
  reaches it; the compiled model refuses what modelx refuses, with modelx's message, on the
  relabelled extract too, every value it cannot decode, every value a bound reads outside
  its range and every `duration_mth` and issue age of `2**53` or more, and an argument past
  a cache raises `IndexError`; the deepest call the contract allows runs cold on a 1 MiB
  stack and on the main thread, and the test reports the smallest of seven stacks, 256 KiB
  to 2 MiB, it ran on, waiting a bounded time for each; a Reference set after the model has
  computed changes no value it has cached; and `run_sec.py --cython` prints what
  `run_sec.py` prints, and refuses a directory that holds no build. They are marked
  `cython`, and they skip without the toolchain, but in the `cython` CI job, which installs
  it on Linux and on Windows and runs the core grid, a skip fails, whatever made it.

```bash
python -m pytest tests/test_whole_life_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_whole_life_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k WholeLife_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k WholeLife_US_SEC
python -m pytest tests/test_whole_life_us_sec.py -q -m cython   # the compiled tests alone
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
