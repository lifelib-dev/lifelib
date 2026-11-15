# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `UL_US_SEC` is [`UL_US_S`](model.md) taught to project from
a valuation date. Besides policies issued at that date, it takes policies already in force
there, in any month of their policy year, and policies to be written in the ten years
after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The
product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `UL_US_S` on another time axis, and it reads `UL_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual mechanics are sourced from a specimen policy
> [S3]. The two assumptions that drive this product hardest, the **current credited rate**
> and the **current COI scale**, are both **[std]**, because insurers do not publish them,
> and so are the mortality table, the lapse vector, the premium persistency scale and every
> expense. Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/universal_life/run_sec.py            # point 1: the anchor cell, at t = 0
python products/universal_life/run_sec.py 6          # point 6: the in-force cell, mid-year
python products/universal_life/run_sec.py --block    # every model point, summed row by row
python products/universal_life/run_sec.py 6 --cython # point 6 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about a minute
and a half, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and
`.gitignore` covers it.

The first prints, as rows `t = 0 … 11`, the cash flows and the account value roll-forward
`run.py` prints for `UL_US_S`'s point 1, the worked example's three rows among them, each
table line for line the same, and then the counts and rates behind them. Three lines to
the same thing for point 6:

```python
import modelx as mx
model = mx.read_model("products/universal_life/UL_US_SEC")
model.Projection[5].result_cf()     # point 6, the table's sixth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[5]` is point 6, and its `point_id()` says so. Its three result tables are
indexed by `t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `UL_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes` and `net_cf` — income-positive, so the flow columns sum to `net_cf` |
| `result_av()` | `UL_US_S`'s per-policy account value roll-forward, in the columns and order of the technical notes' worked example, with zeros before issue |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths and lapses, death first, and its maturities, which are always zero; then `UL_US_S`'s two monthly decrement rates, written 0 outside cover |

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read, so the run holds the cells of one point at
a time. Deleting it, `del model.Projection[idx]`, is not enough: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees, so the runner collects after
each release. It freezes everything alive (`gc.freeze()`) once the model and its table are
read, and again once it has asked every point for its frame, so that each collection scans
only what the block has made since. It prints where each point stands at the valuation
date, then the block's first twelve rows and the block summed into projection years. It
keeps the block's sum as it goes, compensated as pandas sums a `groupby`, so that the block
is, bit for bit, the frames concatenated and summed by `t`, as below.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection, the last month at attained age 120.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month index `d(t)`, and the contract
  runs on it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1`
  and `age(t) = age_at_entry() + duration(t)`, as in `UL_US_S`. `BasicTerm_SE` reaches the
  same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

`UL_US_S` already runs this policy clock, from the first month of its own projection, and
opens its in-force point there. What the valuation clock adds is that `t = 0` is one
instant for every point, that a point may be issued after it, and that a point in force
brings in what its past has left it: the face its withdrawals have left, the free
allowance it has used in the policy year, the premiums it has paid and its MEC status.

Point 3 is `UL_US_S`'s in-force cell, in force 120 months. At `t = 0` it is on the
anniversary that opens policy year 11, at attained age 45, with its surrender charge run
off, and its frame has 912 rows, `t = 0 … 911`. Point 6 is the same policy six months on,
in force 126 months: policy year 12 begins at `t = 6`, where the premium persistency
steps from 80% to 78% and the attained age to 46, and its frame has 906 rows. Point 9 is
`UL_US_S`'s point 1 to be issued 25 months after the valuation date:
`duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0 to 24 are zeros,
its first premium of $150.00 falls at `t = 25`, and its frame has 1,057 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the surrender charge run-off and the lapse shock in the policy year after it, the guaranteed COI scale, the per-unit charge's step-down after policy year 10, the premium persistency and base lapse scales, the GPT and 7-pay limits, all by policy year; the corridor factor and the mortality rate at the attained age; withdrawals from the first anniversary; charges, premiums and withdrawals ceasing at attained age 121; the end of the projection at policy month `omega_mth()` | expense inflation, `inflation_factor(t) = 1.025^(t // 12)`; the declared credited rate `crediting_rate_ann(t)` and the competitor rate `comp_rate_ann(t)`, flat as shipped |

Expense inflation keeps `UL_US_S`'s step by year and moves it onto `t`, so the
maintenance expense steps on the valuation anniversaries, in valuation-date dollars, for
every point alike. The two declared rates are economic inputs: a declared-rate scenario
would be indexed by `t`, one path for every point of a block, however old the policy. As
shipped both are 4.00% in every month, so the clock shows in no number, and the dynamic
lapse multiplier is 1. Acquisition is charged per policy issued, in the issue month, and
not inflated, as in `basiclife/BasicTerm_SE`; it ships at zero, as in `UL_US_S`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
n = len(model.Data.model_point_table())
frames = [model.Projection[i].result_cf() for i in range(n)]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`UL_US_S` computes, whatever the point's count: `UL_US_S` charges acquisition on the
policies in force in the issue month, which on new business are the policies issued. On
`UL_US_S`'s two new-business points every cash flow and every count agrees, and so does
every other cell the two models share, at every argument `UL_US_S`'s own sweep evaluates,
but three whose meaning changed: `pols_if_init()`, now the count already in force at the
valuation date, 0 for new business; `model_point()`, a row of another table; and
`result_pols()`, which gains `pols_new_biz`. On point 3 the projection is `UL_US_S`'s,
month for month, its expenses apart, which are in valuation-date dollars.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `UL_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and eight of its columns are the in-force
interface: `basiclife/BasicTerm_SE`'s two, and six that open an in-force policy's state.
Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value, its loaned part included |
| `loan_bal_init` | dollars | the start of month 0 | the policy loan outstanding, the interest accrued to then included |
| `sum_assured_init` | dollars of face | the start of month 0: after policy month `duration_mth − 1`'s withdrawal cut | the face in force, after every Option A withdrawal cut to date; at most `sum_assured`, the face at issue |
| `wd_used_year_init` | dollars | the start of month 0 | the free withdrawal allowance already used in the policy year under way: the free part of every withdrawal since the anniversary on or before the valuation date, so 0 on a point valued on an anniversary |
| `cum_prem_init` | dollars, of either sign | the start of month 0 | the gross premiums paid from issue to policy month `duration_mth − 1`, less every withdrawal paid, which the GPT test, the 7-pay test and the TARGET premium cap read |
| `is_mec_init` | an int code: 0, not a MEC; 1, a MEC | the start of month 0: the latch after policy month `duration_mth − 1`'s 7-pay test | whether the policy has failed the 7-pay test, and so is a modified endowment contract for good |

The six state columns are 0 on a point issued at or after the valuation date: it is issued
at the face `sum_assured`, with no account value, no loan, and nothing used, paid or
failed. `av_pp_init` and `loan_bal_init` are `UL_US_S`'s own columns: they already measure
the account value and the loan entering `UL_US_S`'s first month, so they keep their names.
Each new column is named for the cell it opens: `sum_assured_init` for `sum_assured_at`,
`wd_used_year_init` for `wd_used_year`, whose name already says that it restarts each
policy year, `cum_prem_init` for `cum_prem_pp`, under `ULSG_US_S`'s name for the same
column, and `is_mec_init` for `is_mec`. No quantity of the product is read at the last
anniversary, so none needs a column at a second instant.

| `UL_US_S` | `UL_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 or more, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `av_pp_init`, `loan_bal_init` | the same | `UL_US_S` already opens its in-force point from them |
| — | `sum_assured_init` | `UL_US_S` opens every point at the face at issue, `sum_assured` |
| — | `wd_used_year_init` | `UL_US_S` takes none of the year's free allowance as used at its `t = 0` |
| — | `cum_prem_init` | `UL_US_S` restarts the premiums less withdrawals at 0 on its in-force point, though the TARGET premium cap reads them |
| — | `is_mec_init` | `UL_US_S`'s latch looks back from its `t > 0` only |

On the twins the four new columns take what `UL_US_S` itself assumes, so each twin opens
as its S row does: on point 3 the face at issue, 100,000, and nothing used, paid or failed.

The columns carried over are read as `UL_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the option, the premium, its load and the
withdrawal excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `UL_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the surrender-charge base, whatever later withdrawals cut the face to |
| `db_option` | `A` or `B` | the option in force over the frame |
| `qual_test` | `GPT`, the only test modelled | issue |
| `premium_type` | `LEVEL`, `SINGLE` or `TARGET` | the pattern over the frame; a single premium falls in the issue month alone |
| `premium_pp_ann` | dollars a year, the planned premium, or the single premium on `SINGLE` | the plan over the frame, paid monthly |
| `load_prem_rate` | a fraction of each premium | the current load over the frame |
| `wd_pp` | dollars a month | the withdrawal taken in every month of the frame from the first anniversary on |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `gsp`, `glp`, `seven_pay_prem` | dollars, the compliance inputs | issue |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the eight in-force columns are present, and so is every other column a projection
  reads, the fifteen of `UL_US_S`'s above but `point_id` and `policy_id`;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is below `2**53` months in size, which an int64 and a float both hold
  exactly, so that numpy never casts it to the least int64, a policy issued `2**63` months
  on;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than the
  projection from issue plus ten years: 1,356 months at issue age 18, the youngest the
  product issues, and 1,152 at 35, the only issue age the shipped COI scale carries. Set
  to 0, the Reference refuses future new business altogether, and a negative horizon is
  itself refused;
- `age_at_entry` is a finite number below `2**53` in size, for the same reason. A fraction
  is not refused: it truncates toward zero, as `UL_US_S`'s `int` does, so 35.5 projects as
  35, and an issue age the contract does not issue is `proj_len()`'s to refuse (below);
- the values of the contract, each of which a projection reads as a number, through a
  floor, a `max` or a `min` included, are each a number in the range the quantity can
  take: `sum_assured`, the face at issue, above 0; `premium_pp_ann`, `wd_pp`, `gsp`, `glp`
  and `seven_pay_prem` zero or more; and `load_prem_rate` from 0 to 1,
  `model_point_table_sec.csv: load_prem_rate must be a number from 0 to 1; it is not at
  point_id [2, 5]`. A blank, a text or an infinity is no such number;
- `has_surr_charge` is `True` or `False`, as pandas reads those words in any case. Any
  other value, a 1, a 0 or a blank among them, would make the column numbers or text, and
  `UL_US_S`'s `bool()` reads the text `"False"` as true;
- the account value, the loan, the face and the year's usage are each a number, zero or
  more. A balance is never negative in force. `UL_US_S` lets a point's account value fall
  below zero once it is in permanent shortfall, because it does not implement the grace
  cascade that would end such a policy, so the message for `av_pp_init` says what to do:
  restate a point in permanent shortfall no later than the last month its account value is
  still zero or more. Without a loan that is the month its shortfall begins, as point 7
  is; with one, the shortfall test, which nets the loan, fails months earlier;
- `cum_prem_init` is a number, of either sign. Premiums less withdrawals is a tax measure,
  not a balance, and since the notes' "less a portion of withdrawals" is taken as the whole
  withdrawal **[std]**, withdrawals can exceed the premiums paid;
- `is_mec_init` is 0 or 1, an int code; written as 1.0 it reads as `True`;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros;
- `sum_assured_init` is above 0 on a policy in force, which holds a face, so an extract
  that leaves the column at zero is refused, rather than projected on the corridor alone;
- `sum_assured_init` is at most `sum_assured`, since face increases are not modelled. A
  face below it is accepted, whether withdrawals cut it or an elective decrease the model
  does not implement, and it is projected from the value given;
- on a point valued on a policy anniversary, `duration_mth` a multiple of 12,
  `wd_used_year_init` is 0: the year's allowance restarts there before any usage is read,
  so any other value would be dropped without a word;
- `is_mec_init` is 1 wherever the 7-pay test has already failed in the month before the
  valuation date: `cum_prem_init` above `seven_pay_prem` times the policy years to then,
  in the first seven. A failure the cumulative premium no longer shows, after withdrawals,
  is the column's to record, and either value is accepted.

A point at or past the end of the projection at the valuation date,
`duration_mth ≥ 12 × (121 − age_at_entry)`, reads, but `proj_len()` refuses it, naming
the point: "point_id 5: duration_mth 1032 is at or past the end of the projection, policy
month 1032, attained age 121". Two more points have no frame the contract issues, and
`proj_len()` refuses each the same way, before the first: one issued above `omega_age`,
120, which would never be in cover, "point_id 9: age_at_entry 121 is above omega_age, 120:
a policy issued there would never be in cover", and, after it, one issued below
`issue_age_min`, 18, the youngest issue age the product spec admits, "point_id 1: issue
age 17 is below issue_age_min, 18", which the compiled model's caches are sized from (*The
compiled model*, below). `UL_US_S` projects both. These are the model's rules, not the
table's. So a loop over the block meets such a row only when it reaches it, after
projecting the points before it. `run_sec.py --block` asks every point for its frame
before it projects any, and stops before it prints anything.

The assumption tables read at a policy year or an attained age are checked too, each once,
in the `Data` cell its reader in `Projection` takes its extent from: the last policy year of
`prem_persistency.csv` and `lapse_table.csv`, the first and last ages of
`corridor_factors.csv` and `mort_table.csv`, beyond which each reads its nearest row, and,
in `coi_schedules()`, which every vector of the COI scale asks first, the policy years of
each issue-age cell of `coi_rates.csv`. The key column is read by
value, so a year written `16.0` is 16, and a key that is blank, text or not a whole number
is refused, naming the file, the column and the lines it is on: "prem_persistency.csv:
policy_year must be a whole number; it is not on line [17]". So is a negative age in the
two age tables, "corridor_factors.csv: age must be 0 or more; it is not on line [2]",
which `UL_US_S`, reading the nearest row, projects: the compiled model holds each table by
attained age from age 0 (*The compiled model*, below). So are keys that do not run one
row a year or an age, without a gap or a repeat, policy years from 1, the message naming
each key that repeats, with its lines, and each that is missing: "mort_table.csv: the ages
must run one row an age, without a gap or a repeat; age 26 is on line [10, 11]; no line
holds age 27". So is a blank sex or class in the COI scale, and a rate that is blank, text
or infinite: "mort_table.csv: mort_rate must be a number; it is not on line [44]".
`class_count()` and `surr_charge_count()` check the class factors and the surrender-charge
schedules the same way: a class or a schedule blank or on two rows, and a factor, a charge
or a run-off that is not a number. The reader asks for its extent, or the count, before it
reads a value, so a projection meets the checks first. `UL_US_S` takes each extent from the
key column as pandas reads it, where a blank is a missing value the extent skips: with the
last policy year of `prem_persistency.csv` blank, every year from 16 on reads year 15's 72%
in place of 70%, and nothing says so. A blank rate is a missing value to it too, which shows
in its flows or is lost in a `min` or a `max`: a blank lapse rate reads as the cap of 35%, a
blank corridor factor as no corridor and a blank surrender charge as none. Here the cap on
the mortality rate, `min(q, 1.0)`, keeps a blank base rate or class factor missing, as
`UL_US_S` does; written `min(1.0, q)` it would read one as 1.0, every policy dying in that
month. Each is refused.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`UL_US_S` and its table by `tests/sec_support.py`, from the `UL_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `UL_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py UL_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 2 | twin | S points 1 and 2 | issued at `t = 0`: `UL_US_S`'s worked example on Option A, and the same policy on Option B, which runs into permanent shortfall in policy year 57 |
| 3 | twin | S point 3 | `UL_US_S`'s in-force cell, in force 120 months, on the anniversary opening policy year 11, with 15,000.00 of account value and a 2,000.00 loan |
| 4 | derived | S point 1 at S month 12 | on its first anniversary, inside the surrender-charge period: 1,244.21 of account value and 1,800.00 of premiums paid |
| 5 | derived | S point 1 at S month 113 | in policy year 10, the lapse-shock year, its surrender charge run off: the shock runs to `t = 6`, and policy year 11 begins at `t = 7` |
| 6 | derived | S point 3 at S month 6 | the in-force cell six months on, in force 126 months, mid-year with its loan: 15,755.09 of account value and a loan of 2,027.31 |
| 7 | derived | S point 2 at S month 676 | Option B in the month its permanent shortfall begins, policy year 57, attained age 91, with 309.04 of account value |
| 8 | derived | S point 1 at S month 1,008 | the first month at attained age 119, where the mortality rate reaches 1.0: every survivor dies at `t = 0`, and the frame's 23 later rows are zeros |
| 9 | future | S point 1, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `UL_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `UL_US_S` carries into it, each column read as
`UL_US_S`'s own formulas read it: the account value as `av_pp_at(d, "BEF_PREM")`, the loan
as `loan_bal_pp_bom(d)`, the face as `sum_assured_at(d − 1)`, the year's usage as
`wd_used_year(d)`, the premiums less withdrawals as `cum_prem_pp(d − 1)` and the MEC latch
as `is_mec(d − 1)`. So the row continues the S projection from there: point 4 opens with
0.939317 policies, and point 8 with 1.765e-10. Point 6's premiums to date, 720.00, are the
six months' since `UL_US_S`'s first month, because `UL_US_S` counts its in-force point's
premiums from there; an extract carries every premium since issue. A derived row's
`policy_id` is the S row's with the month appended, `UL-000001-M12`, and a future row's
carries the months to issue, `UL-000001-F25`. Row `t` of a generated point is month
`t + source_mth` of its S point. All nine are on the anchor configuration M35 / StdNT /
$100,000, because the specimen gives a guaranteed COI scale for that cell alone [S3], so a
point on any other issue age, sex or class needs `coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
the three timings that `UL_US_S` already names, each an int Reference named as the string
`UL_US_S` passes, so that a timing, like every argument, is a C number when the model
compiles:

- `BEF_NB = 0`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR = 1`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_MAT = 2`, the count before any maturity, `UL_US_S`'s meaning: the `BEF_DECR` count,
  since the contract never matures and no event of the month separates the two.

Any other timing raises, the account value's five among them, which follow in the same
numbering, `BEF_PREM = 3` to `EOM = 7` (*The compiled model*, below). `UL_US_S`'s cell of
the name returns `pols_if(t)` for every timing, and nothing calls it. `BEF_NB` is the one
timing this model gives a meaning of its own, `basiclife/BasicTerm_SE`'s, and the two
models differ in it alone, in the issue month: there `UL_US_S` counts the issued policies,
and this model counts them as new business, not yet in. Each S model's `"BEF_MAT"` keeps
that model's meaning, and `basiclife/BasicTerm_SE`'s, the count at the start of the month
before its new business, is not adopted: `WholeLife_US_SEC`'s is the end of its month,
after the surrenders, and this model's the start of the month, after its new business.

The survivors carried into month `t` are those of month `t − 1`'s `BEF_DECR` count, which
`BEF_NB` forms itself, as its own value at `t − 1` plus that month's new business, less
that month's deaths and lapses in the order `pols_death` and `pols_lapse` take them. The
account value and the loan are carried the same way. `av_pp_at(t, BEF_PREM)` forms month
`t − 1`'s closing balance itself, from its own value at `t − 1` and month `t − 1`'s net
premium, withdrawal, fee, deduction and interest, the same sum in the same order as
`av_pp(t − 1)`, and `loan_bal_pp_bom(t)` accrues a month's loan interest on its own value at
`t − 1`, as `loan_bal_pp(t − 1)` does. The face, the year's usage and the premiums to date
each call themselves at `t − 1` before anything else, and the MEC latch does once its
in-year test, which reads the same month's premiums to date, has run. So every chain of
calls from month `t` back to `t_entry()` is one cell a month, where `UL_US_S`'s account
value ran through five cells a month and its loan through two. On a model just read, a
cold `net_cf` in the last month of point 1's 1,032-month frame runs 1,048 cells deep and
needs modelx's recursion limit at 1,047, against 5,166 for `UL_US_S`'s point 1, and point
3's 912-month frame needs 927: 17 cells above the chain back to `t_entry()`, the deepest
of them month 0's COI rate, the extent of its scale, `Data`'s vector of extents, the check
of the COI table below it and its read. At the longest cover the contract allows, issue
age 18 and 1,236 months, it runs 1,252 deep and needs 1,251, whether the policy is issued
at the valuation date or 120 months after it, because every chain stops at the issue
month (*What a compiled run needs*, below). Called alone, each chain's head runs at most 9
cells above its chain, the account value's. Each report evaluates its columns in ascending
`t`, and every committed point's reports and checks run that way under a limit of 16.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `UL_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < omega_mth()`, where
`omega_mth() = 12 × (121 − age_at_entry)` is `UL_US_S`'s frame from issue, the first month
at attained age 121. Outside it, before issue and from `t = proj_len()` on, every count,
premium, withdrawal, charge, decrement rate, claim and cash flow is zero and every flag
false; only the two clocks, the inputs read on the valuation clock and the lapse shock's
neutral 1.0 hold values there, and the month after the frame holds one exception more,
below. No count evaluates a decrement rate there, and no table is read at a policy year or
an attained age the policy does not have: `prem_persistency`, `premium_pp`, `wd_pp`,
`wd_used_year`, `sum_assured_at`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`,
`maint_fee_pp`, `loan_bal_pp_bom`, `surr_charge_rate`, `cum_prem_pp`, `gpt_limit`,
`seven_pay_limit`, `mort_rate`, `lapse_rate_base`, `pols_death`, `pols_lapse` and
`expenses` are zero, and `gpt_ok` and `is_mec` false, before any table or rate is read,
and every other value is zero through them. `lapse_rate_sc_mult` is 1.0 there, before it
compares the policy year with the shock year: a point with no surrender charge has the
shock year 0, and before issue the valuation clock reaches policy year 0. Each table read
at a policy year or an attained age has one reader keyed by it, called inside cover only,
so on point 9, whose policy year is −2 at `t = 0`, no reader holds a key below policy year
1 or attained age 35.

**The end of the projection.** The frame ends at `omega_mth()` because the mortality table
ends at attained age 120, not at an event of the contract, which never matures. With the
shipped table, whose annual rate is 1.0 at ages 119 and 120, and a class factor and an A/E
of 1 or more, every life has died by the end of the first month at attained age 119:
point 8, valued in that month, loses its last 1.765e-10 of a policy at `t = 0`. With a
preferred class, an A/E below 1 or a table that stays below 1, lives survive the last
month, and `UL_US_S`'s roll-forwards read them: `check_av_roll_fwd()` and `av_change()`
read the account value in force entering month `t + 1`, which in the last month is
`t = proj_len()`. So the two opening values read there, the count carried in
(`pols_if_at(t, BEF_NB)`, and through it `pols_if(t)`) and the account value carried in
(`av_pp_at(t, BEF_PREM)`), are defined for `0 ≤ duration_mth(t) ≤ omega_mth()`: in the
month after the frame they are the survivors of the last month and the account value they
carry, `UL_US_S`'s own values there. Everything else is zero or false there, the expenses
included, which would otherwise fall on the carried count, and nothing reads past it:
`av_change()` and the checks' two residual cells, which read `t + 1`, are zero outside
cover before they read it. At the shipped assumptions the survivors at `proj_len()` are
exactly 0.0 on every committed point. Under the splice's References, an A/E of 0.56 among
them, they are 4.02e-6 of a policy on the twins of points 1 and 2 and 9.27e-6 on the twin of
point 3, equal to `UL_US_S`'s, and both checks close.

## The opening state

`UL_US_S` opens its in-force point 3 from two columns, the account value and the loan
entering its first month, and takes the rest as they stand at issue: the face at issue,
none of the year's free allowance used, no premium paid, and the MEC latch off. Point 3
needs no more, since it withdraws nothing and pays inside every limit, and its twin opens
the same way. A policy valued in any month of its life needs all six columns, each what
`UL_US_S` carries into that month. The committed points show the first two: point 6, the
in-force cell six months on, opens with 15,755.09 of account value and a loan of 2,027.31,
where `UL_US_S`'s columns hold the 15,000.00 and 2,000.00 of six months before; month 0's
roll-forward, interest credit, shortfall test and death claim read them.

On the committed points the other four columns show nothing: they withdraw nothing and pay
level premiums inside every limit, so the face stays at issue, no allowance is used, the
latch stays off, and no level premium reads the premiums paid. Each shows instead on a
variant that the splice restates in force (tests below), `UL_US_S`'s point 1 with a few of
its columns changed, in a copy of the tables that gives the variant's class COI rows of its
own, beside the same row with the column as `UL_US_S` assumes it, zero, or the face at issue
for the face:

- **`cum_prem_init`.** The TARGET variant, `UL_US_S`'s point 1 planning $6,000 a year,
  restated at month 71, in policy year 6. Its premiums to date, 33,750.00, leave 388.15 of
  room under the GPT limit, the guideline single premium of 34,138.15, so it collects
  388.15 at `t = 0` and nothing more in the year. With the column at 0 it would collect its
  level 450.00 at once, and 5,290.00 over the twelve months.
- **`is_mec_init`.** The single-premium variant, $50,000 capped at the guideline single
  premium, restated at month 85, in policy year 8. It failed the 7-pay test in its issue
  month, and the in-year test no longer applies, so `is_mec(0)` is true from the latch
  alone. With the column at 0 it would be false.
- **`wd_used_year_init`.** The withdrawal variant, `UL_US_S`'s point 1 withdrawing $60 a
  month from its first anniversary, restated at month 13. The year's first withdrawal has
  used 60.00 of its free allowance, so month 0's free amount is 82.39 where 10% of the
  account value is 142.39, and at `t = 1` the year's third withdrawal exceeds what is
  left of it and cuts the face by 35.66, to 99,964.34. With the column at 0 the free amount
  would be 142.39, and the first cut would come a month later.
- **`sum_assured_init`.** The same variant restated at month 24, its second anniversary.
  A year of withdrawals has cut the face to 99,442.27, and that is the death benefit of
  month 0; read as the face at issue, it would be 100,000.00. The surrender charge is
  691.67 either way, because it is quoted on the face at issue.

The in-year test runs before the latch looks back, in the valuation month as in every
other, so a policy that fails the test at `t = 0` is a MEC from then on, whatever
`is_mec_init` says. The over-funded variant, planning $24,000 a year and restated at month
3, has paid 6,000.00, inside the first year's 7-pay limit of 6,702.10, so its
`is_mec_init` is 0, and month 0's 2,000.00 takes it to 8,000.00: `is_mec(0)` is true.

## Departures from UL_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state on a
point in force, and each cell that turns `t` into a policy year or an attained age answers
for the months outside cover. Running in force left 45 of `UL_US_S`'s 107 cells in
`Projection` unchanged, one of them, `lapse_rate_dyn_mult`, with a line re-wrapped, gave 26
a new docstring only, most of them to say what `t` now counts, and rewrote 36; it removed
and renamed none, and added 26 cells, 133 in all. Compiling then changed how each cell
reads its inputs and spells its codes, and no number: it replaced one cell,
`coi_rate_scale`, by a schedule number, and added four, 136 in all (*The compiled model*,
below); of `UL_US_S`'s cells it changed the signature of one, `claims`. The twin identity
exempts `coi_rate_scale`, with its reason, and compares `UL_US_S`'s `claims(t, None)` with
the total `claims(t)`: a cell of `UL_US_S`'s that this model lacked, or took other
arguments, would fail it otherwise. Of `Data`'s nine, running in force rewrote
`model_point_table` to check the table as it reads it, and added nine cells, eighteen in
all: the extents of the five tables read at a policy year or an attained age, each of
which checks its table's keys and rates, and `class_count` and `surr_charge_count`, which
check the class factors and the surrender-charge schedules. Compiling added 35, 53 in all,
and widened the checks of the model point table and of the two age tables. Some
departures come from compiling rather than from the clock: `proj_len`'s two new refusals
and the last four rows below.

| Cells | `UL_US_S` | `UL_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `omega_mth` | `12 × (omega_age − x + 1) − duration_mth_init()`, the months from the first projected month | `omega_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the end of the projection, and on a point issued above `omega_age`, 120, or below `issue_age_min`, 18 | `omega_mth()` is new and is `UL_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left has no frame, nor one that would never be in cover, and the compiled caches hold the contract's frames alone |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, BEF_DECR)`, from `t_entry()`; `BEF_NB` the count before the month's new business, and `BEF_MAT` the `BEF_DECR` count, as in `UL_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `av_pp_at` (`BEF_PREM`), `loan_bal_pp_bom` | `av_pp_init()` and `loan_bal_init()` at `t = 0`, then `av_pp(t − 1)` and `loan_bal_pp(t − 1)`: chains of five cells a month and of two | the same openings at `t_entry()`, then the previous month's close formed in the cell itself, `UL_US_S`'s arithmetic in its order | Every chain one cell a month, since a compiled model runs it on the C stack |
| `sum_assured_at`, `wd_used_year`, `cum_prem_pp`, `is_mec`, `premium_pp` | opened at `t = 0` at the face at issue, 0, 0 and `False`, and the TARGET cap's premiums to date at 0 | opened at `t_entry()` from `sum_assured_init()`, `wd_used_year_init()`, `cum_prem_init()` and `is_mec_init()` on a point in force, and from the issue values on any other | A policy in force brings in its face, the year's withdrawals, its premiums and its MEC status |
| `prem_persistency`, `coi_rate_guar`, `lapse_rate_base`, `corridor_factor`, `mort_rate` | the table read in the monthly cell, at `policy_year(t)` or `age(t)`, clamped to the extent of the key column as pandas reads it | one reader keyed by the year or the age — `prem_persistency_py`, `coi_rate_guar_py`, `lapse_rate_base_py`, `corridor_factor_at`, `mort_rate_base_at` — with `UL_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the rates, called inside cover only; a policy year below 1 refused, naming the point, where `UL_US_S`'s lookup raised `KeyError` | No table is read at a year or an age the policy does not have, each is read once a year or an age, and a blank, text or fractional key, keys that repeat or leave a gap and a rate that is not a number are refused by name, where `UL_US_S`'s extent skips a blank key and cuts the table short, and a blank rate is a missing value |
| `surr_charge_rate`, `lapse_shock_year` | the schedule's row read in each | `surr_charge_rate_max()` and `surr_charge_runoff_years()`, one accessor for each of the schedule's two columns, which `Data` joins to the points once `surr_charge_count()` has checked the table, on every point whose ID the table holds, with a charge or without; on a point without one whose ID the table lacks, a blank ID included, both accessors raise `KeyError`, naming the point, as their `.loc` did at stage E | The same numbers for any schedule, with no table read in a monthly cell; a blank charge, which `UL_US_S`'s `max` reads as no charge, is refused |
| `premium_pp`, `db_pp`, `face_reduction_pp`, `corridor_factor` | branches on the text of `premium_type()`, `db_option()` and `qual_test()` | branches on six decodes, `is_level_premium()`, `is_single_premium()`, `is_target_premium()`, `is_db_option_a()`, `is_db_option_b()` and `is_gpt()`, each read from a 0/1 vector `Data` decodes from the column | No projection cell reads text. The label accessors stay for reporting, and an unknown value still raises `UL_US_S`'s message |
| `class_factor` | the factor of the point's class, read from the table | the same, joined to the points in `Data` once `class_count()` has checked the table's classes and factors | A blank factor, a missing value to `UL_US_S`, would reach the cap on `mort_rate`, `min(q, 1.0)`, which keeps it missing |
| `prem_persistency`, `premium_pp`, `wd_pp`, `wd_used_year`, `sum_assured_at`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `maint_fee_pp`, `surr_charge_rate`, `cum_prem_pp`, `gpt_limit`, `gpt_ok`, `seven_pay_limit`, `is_mec`, `mort_rate`, `lapse_rate_base`, `lapse_rate_sc_mult` | unguarded: no `UL_US_S` frame has a month before issue | zero or false outside cover, `is_active(t)`, before any table or rate is read; `lapse_rate_sc_mult` 1.0 | A future point's months before issue have `t ≥ 0` and policy years down to −2, and policy year 0 is the shock year of a point with no surrender charge. At `t = proj_len()` nothing is charged, paid or withdrawn, whatever `omega_age` and `charges_cease_age` are set to |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `inflation_factor` | `1.025^(policy_year(t) − 1)`, stepping on the policy anniversaries | `1.025^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_margin` | `math.isclose` with both tolerances at `1e-9`, month by month | the same condition on one relative residual a month, `check_av_roll_fwd_resid(t)` and `check_margin_resid(t)`; a residual that is not a number fails | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin` | the loan term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the loan a surrender recovers | The lapse claim is the net cash value floored at 0, so once a loan exceeds the cash value `UL_US_S`'s identity is off by `(CSV(t) − L(t)) × pols_lapse(t)` and its check fails on a projection that is right; on every shipped point the cash value covers the loan, and the two agree |
| `wd_pp` | the model point's `wd_pp` column read in the monthly cell | read once a point, by `wd_pp_mth()` | A monthly cell the account value's chain reads reads no table |
| `result_pols` | `pols_if`, the three outflows and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `claims` | `claims(t, kind=None)`: one kind's claims, or with `None` the two summed by Python's `sum` | `claims_death(t)` and `claims_lapse(t)`, the `result_cf` columns, and `claims(t)` their total, `0.0 + death + lapse` | A compiled cell takes C numbers, and `None` is none. Python's `sum` of two floats is their sum, rounded once, from its `0.0` start, which this computes, so the total is `UL_US_S`'s float in every month, the sign of a zero included. A test holds it to `UL_US_S`'s bit for bit |
| `coi_rate_scale`, `coi_rate_last_year`, `coi_rate_guar_py` | the point's scale, a Series, sliced from the table by its sex, class and issue age, and its last policy year read from it | `coi_schedule()`, the number of the point's scale, a row of `Data`'s table of the scales by policy year, and the last year a `Data` vector by point; a point whose scale the table lacks is schedule 0, refused, naming it, where a rate is read | No compiled cell returns a Series. `UL_US_S` raised `KeyError` where it read the missing scale, and projects a point that never reads one, valued or issued at or past `charges_cease_age`, so the refusal waits for the read |
| `cure_premium_pp` | `3 × MD(t) / (1 − pl)`, which raises Python's `ZeroDivisionError` at a load of 1 | the same, with the divisor checked first and Python's error raised, `ZeroDivisionError: float division by zero` | Compiled C's division raises the same error with another message. `Data` admits a load of 1, which `UL_US_S` projects, since no report reads the cure payment |
| `Data` and the cells that read a table | a malformed value or key met, if at all, only when a projection reaches it, a missing class or schedule as `KeyError`, and an age table read at its nearest row whatever its ages | refused by name at the first read of the array, over the whole table: a model point value outside its range, an issue age, a `duration_mth` or a `point_id` past `2**53`, a class the class factors lack, a schedule the surrender charges lack or a run-off of 0 years or of `2**53` or more on a point with a charge, and a negative age in the corridor or mortality table | A compiled model holds numbers, not text, computes a NaN as silently as modelx, and holds each age table from age 0 (*What it refuses*, below) |

The other new cells of running in force are `policy_count`, `t_entry`, `is_active`,
`pols_new_biz`, the four new opening-state accessors, `coi_rate_last_year`, the extent of a
point's COI scale, and `wd_pp_mth`, the withdrawal column read once a point; those of
compiling are listed under *What compiling changed, and why*, below.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, so point 3's
`expenses(t)` is `UL_US_S`'s divided by `1.025^10`, about 1.280, at every `t`: both models
step on its anniversaries. Its other cash flows, its counts and its account value
roll-forward are `UL_US_S`'s from month 0 on. Point 9 is `UL_US_S`'s point 1 twenty-five
months on in those columns too. Its maintenance expense is `1.025^2` above `UL_US_S`'s,
and `1.025^3` in the last month of each policy year, where the valuation year has stepped
and the policy year has not.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, on the points of the splice
grid, which take the branches they do not, on the contract's longest frames, and where
the cap on mortality binds or a NaN reaches it. The compile tests hold it so on x86-64,
and to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py universal_life                   # in place, beside the model
python tools/build_sec_cy.py universal_life --out /tmp/ul     # elsewhere, with the CSVs
```

The tool exports the model to `UL_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `UL_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/universal_life")  # the directory holding the build
from UL_US_SEC_nomx_cy import mx_model as model
model.Projection[5].result_cf()                # point 6, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 5` after `Projection.result_cf()` leaves point
1's frame cached, while `point_id()`, not yet computed, reads point 6's label, and
`Projection.inflation_rate` set to 0 once `Projection[2]` has computed point 3's
`expenses(12)` leaves it at 6.2047, where an ItemSpace made after computes 6.0534. Set
every Reference on a model just imported, before anything is computed, where modelx would
recompute; a test holds the compiled model to this.

A build takes about a minute and a half with gcc, 98 s here, and needs a C compiler,
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
typed 122 of its 133 `Projection` cells as C numbers, but six of them still took a timing
or a kind as text, or `claims`'s `None`, and so kept a dictionary for a cache, and it ran
only 2.2 to 2.3 times its own export, 10.4 ms a point on `net_cf` against 23.6, over the
committed points. The bodies of the typed cells still called pandas and Python: a
`model_point()` lookup for each of the 23 attributes a formula reads, a `.loc` on a table
for each policy year's persistency, lapse and COI rate, each attained age's corridor
factor and mortality, each point's class factor and surrender-charge schedule, the point's
COI scale sliced into a Series by its sex, class and issue age, text compared in every
formula that branched on the death benefit option, the qualification test or the premium
pattern, and a generator summed in `claims`. So each input now reaches a cell as a
number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[5]` is point 6, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once: the death benefit option
  into `is_db_option_a` and `is_db_option_b`, the qualification test into `is_gpt`, the
  premium pattern into `is_level_premium`, `is_single_premium` and `is_target_premium`,
  and `has_surr_charge` into a flag of its own. Each decodes as `UL_US_S` compares the
  column, so a value none of the flags names is no flag, and the cell that branches on it
  raises `UL_US_S`'s message, as `UL_US_S` does.
- **Tables indexed by integers.** The persistency and lapse tables are held by policy
  year, and the corridor and mortality tables by attained age, padded from 0 so that the
  year or the age is the index. The COI scales, keyed by sex, class and issue age, are
  numbered from 1 in the order of those keys, each point carrying the number of its own,
  `coi_schedule()`, and held by schedule and policy year in `coi_rate_array`; the last
  policy year of each point's scale is a vector beside it, `coi_rate_last_years`. That
  departs from the plan's R7 and `Term_US_SEC`, whose tables keep a first-key and a
  last-key vector by schedule: here the last year is held by point, which is the same
  number, and there is no first-key vector, since the table's check requires every scale
  to start at policy year 1. The padding holds NaN, and
  nothing reads it: each table's one reader refuses a policy year below 1, naming the
  point, and reads an age outside the table at its nearest row, as `UL_US_S` does. The
  class factor and the surrender-charge schedule are one number a point, and each is
  joined to the points in `Data`, which refuses a key the table lacks, naming every such
  point, since `UL_US_S` reads both on every projection of the point: the class factor in
  every month on the books, and the schedule in every month of a point with a charge. A
  point without a charge is never refused for its schedule, which `UL_US_S` never reads;
  it reads its schedule's two columns where the table holds its ID, as at stage E, and
  where the table does not, `has_surr_charge_schedule()` is 0 and both accessors raise
  `KeyError`, naming the point, where their `.loc` raised it at stage E.
  A point whose COI scale the table lacks is another matter: it reads the scale only while
  charges run, and a point valued or issued at or past `charges_cease_age` never does, so
  `UL_US_S` projects it. So it is schedule 0, with a last year of 0, and
  `coi_rate_last_year` refuses it, naming it, where a rate is read.
- **Codes.** A timing or a kind, which `UL_US_S` spells as text, is an int Reference named
  as the text: the count's timings `BEF_NB = 0`, `BEF_DECR = 1` and `BEF_MAT = 2`, the
  account value's `BEF_PREM = 3`, `BEF_WD = 4`, `BEF_FEE = 5`, `BEF_INV = 6` and `EOM = 7`,
  and `DEATH = 0`, `LAPSE = 1` and `MATURITY = 2`. A call reads as before, less the
  quotes: `pols_if_at(t, BEF_DECR)`, `av_pp_at(t, BEF_FEE)`, `claim_pp(t, DEATH)`. A
  string argument or a string value would give the cell a dictionary for a cache, where a
  code indexes a C array, so codes are numbered from 0 without a gap. The model has two
  families of timing, the count's and the account value's, passed to different cells, and
  they are numbered as one, `BEF_NB` and `BEF_DECR` first, as in every SEC model, then the
  count's third, then the account value's in the order of their instants within the
  month, `EOM` last. So no two timings share a code, and a code of one family passed to
  the other's cell, `av_pp_at(t, BEF_NB)`, is refused as `invalid timing` in both engines,
  where two families numbered from 0 would read it as `BEF_PREM` without a word. The
  `Projection` docstring's *Codes* lists all eleven.
- **The claims, split.** `UL_US_S`'s `claims(t, kind=None)` is one kind's claims or, with
  `None`, the two summed by a generator: neither a C parameter nor a C loop. Here the kinds
  are two cells, `claims_death` and `claims_lapse`, the `result_cf` columns, and
  `claims(t)` is their total (*Departures from UL_US_S*, above).
- **No Python call kept.** No formula outside the reporting cells calls a Python builtin
  outside its refusals but `int`, `float`, `bool`, `abs`, `min`, `max` and `range`, which
  Cython turns into C, all but one `int`: `lapse_shock_year`'s `int` of the run-off, a
  float, is a Python int converted to a C `long long`, exact below `2**63` and raising
  `OverflowError` past it (*What it refuses*, below). So `tests/us_registry.py` admits none,
  as it admits `WholeLife_US_SEC`'s `round`. Two divisions whose divisor `UL_US_S`'s own
  inputs can make zero are guarded: `Data` refuses a surrender-charge run-off of 0 on a
  point with a charge, and `cure_premium_pp` raises Python's own `ZeroDivisionError: float
  division by zero` at a load of 1, where compiled C's division would raise the same error
  with another message (*What it refuses*, below).
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `rate_class()`, `db_option()`, `qual_test()`, `premium_type()` and `surr_charge_id()`, and
  the three reports return a table row, text and DataFrames, for a reader, for `run_sec.py`
  and for the comparison with `UL_US_S`. No other cell calls them, so they cost the
  projection nothing. A label accessor returns its column as read, and `Data` accepts a
  label that is not text: a blank `surr_charge_id` on a point without a charge, which reads
  as NaN, or a column of numbers, ints, which `UL_US_S` projects, and any other blank or
  numeric label, which the point's first projection refuses. So each accessor compiles to a
  Python object, as the sample traces it (below), and returns what modelx returns. The two
  checks are reporting cells too, but they return a verdict, which compiles to a C `bint`.

The `Data` docstring lists its vectors, arrays and counts, each with the column or file it
comes from: 13 vectors of int64 by point, among them `coi_rate_last_years`, which was the
COI table's check and is now a vector; 16 vectors of float64 by point; four float64 tables
by policy year or attained age, and the COI scales by schedule and policy year; and nine
int counts and extents, each a table's check, `coi_schedules`, the COI table's, among them.
The nine readers stay Python, returning DataFrames and a path, and no `Projection` cell
but `model_point()` reads them. Every other cell of `Projection`, 126 of its 136, returns
a C `bint`, `long long` or `double`, and caches a single value, or a C array the spec sizes
from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,358 by `t`, of `double`, `long long` or `bint` | the 77 cells of `t` alone: every count, rate, factor, charge, premium, withdrawal, value, claim and cash flow; the policy clock, its years and the attained ages; the flags `is_active`, `gpt_ok`, `is_mec` and `is_shortfall`; and the checks' monthly residuals |
| a C array of 1,358 by 8 | `pols_if_at`, `av_pp_at` and `av_at`, by `(t, timing)`, and `claim_pp` and `claims_from_av`, by `(t, kind)`, whose three kinds leave five columns unused (*The sample and the spec*, below) |
| a C array of 105 by `y` | `prem_persistency_py`, `lapse_rate_base_py` and `coi_rate_guar_py`, by policy year |
| a C array of 122 by `a` | `corridor_factor_at` and `mort_rate_base_at`, by attained age |
| one `long long`, `double` or `bint` | the 39 cells without a parameter: the point's label, numbers, decodes and flags, its opening state, its class factor, COI schedule and the scale's last year, its surrender charge, run-off and shock year, the ends of its frame, the monthly guaranteed and loan rates and the NAAR factor, and the two checks |
| a Python object | the ten reporting cells but the checks |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the three reports
and the two checks on every committed point, which reach 112 of the 136 cells, and then
the 24 they do not and the six codes no formula passes: `model_point()` and the six label
accessors, which only a reader asks for; `point_id()`, which only a refusal names;
`is_target_premium()`, which a level premium never asks for; the guideline premium and
7-pay tests, the MEC latch, the shortfall trigger, the cure payment and the free
withdrawal amount, which no report reads, with what only they read, the three tax inputs,
the two limits, the premiums to date, the year's withdrawal usage and its three
opening-state columns; and, in cells the reports reach, `pols_if_at` at `BEF_MAT`, `av_at`
at `BEF_WD`, `BEF_FEE`, `BEF_INV` and `EOM`, and `claims_from_av` at `MATURITY`. It calls
the monthly ones in every month of the frame and the month after it. It projects the
committed points alone: the export it runs reads the CSVs of the directory the build is
made in, and the trace it needs is the committed points', which are what the tests
project. The six label accessors it calls once more, on a copy of the table's first
point with every label blank, which it writes to a temporary directory and reads by a
second instance of the export, given the file's absolute path as `model_point_file`. That
types them as Python objects, so that a blank or numeric label returns what modelx
returns rather than raising `TypeError` (*What compiling changed, and why*). The committed
points leave branches untaken: withdrawals, Option B's corridor, the
single and target premium patterns, a second surrender-charge schedule, charges ceasing in
cover, the lapse rate's cap, the cap on mortality and a point without a COI scale. That
still types every cell, because every branch of a cell returns the one type its others
return, a rate a float in every branch, and on points that take those branches the
compiled model computes modelx's numbers (above). The sample also raises the recursion
limit, which modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forwards read and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and one of headroom:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,358 | 1,356. The longest frame is a policy issued at the youngest issue age, 18, to the end of the projection at attained age 121, 103 policy years, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 103 + 120 = 1,356 months, `t = 0 … 1,355`, and the month after, 1,356. The two residuals and `av_change` read `t + 1` in cover alone, so nothing reads 1,357 |
| `t`, `timing` | 1,358 by 8 | `t` as above, by the eight timings of the one numbering, so a code past `EOM` raises |
| `t`, `kind` | 1,358 by 8 | `t` as above, by the three kinds and five columns more, so that every 2-D cache has timing's width. Cython's generated unpickle code converts a space's 2-D caches with one function, written for one width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A kind from 3 to 7 is then inside the cache, where the cell refuses it as modelx does, and one from 8 raises |
| `y` | 105 | 103, the policy year of the last covered month at issue age 18, read by the three readers by policy year inside cover alone |
| `a` | 122 | 120, `omega_age`, the last attained age in cover, read by the two readers by age inside cover alone, from the youngest issue age, 18 |

`proj_len()` refuses a point issued below 18, `issue_age_min`, and one issued above
`omega_age`, 120, in modelx as compiled, and the projection ends at attained age 121, so no
report on a point the model projects runs past these caches. Those two References and
`Data.future_horizon_mth` are the contract the sizes are derived from. Lower the minimum,
or raise `omega_age` or the horizon past 120 months, and a report runs past the caches in
the compiled model alone: a frame of more than 1,357 months, a policy year past 104 or an
age past 121 raises `IndexError`, naming nothing, where modelx projects. Each needs the
sizes derived again, as `spec_sec.py` derives them, and a rebuild: `t` raised to
12 × (`omega_age` − `issue_age_min` + 1) + the horizon + 2, `y` to `omega_age` −
`issue_age_min` + 3, and `a` to `omega_age` + 2. The shipped COI scale carries the anchor
cell alone, issue age 35, so a point at any other is refused today by its first COI rate,
naming it; an issue age of 18 is the contract's, which an extended scale reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it
was measured to change there. Here `cpow` reaches six powers: the monthly rates of both
decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`, the monthly
credited, guaranteed and loan rates, `(1 + i)^(1/12) − 1` in `inv_return_mth`,
`guar_rate_mth` and `loan_rate_mth`, and expense inflation, `(1 + r)^(t // 12)` in
`inflation_factor`. Without `cpow` a compiler with C99's complex numbers, gcc among them,
computes a power of two doubles as a complex power, which can differ from Python's float
power in its last bits. With both directives and the flag every compiled value agrees
with modelx's bit for bit, and the compile tests hold each, by the module's first line, by
the compiler's command lines and, on x86-64, by the comparison itself. On the same
platforms the tool adds `-Werror=incompatible-pointer-types`, so that gcc before 14, which
only warns of a pointer of the wrong type, fails the build as gcc 14 does: the error two
cache widths give (*The sample and the spec*, above).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 1,892,736
bytes, about 1.9 MB, the type's basic size, which holds every cell's cache: 77 arrays of
1,358 months and five of 1,358 by 8, each beside a flag array of its shape that marks what
is computed, make most of it, the five 2-D caches about 652 KB of it. That is 1.6 times
`WholeLife_US_SEC`'s, for frames of 1,358 months against 1,322 and 2-D caches eight wide
against five. Deleting it, `del model.Projection[idx]`, frees nothing by itself: an
ItemSpace sits in reference cycles, and only Python's cyclic collector frees it. That is
why `run_sec.py --block` collects after each release, in its frame pass and in its
projections (*Run it*, above), and a compile test holds a compiled block run to one
point's ItemSpace at a time. Without it, 504 compiled points peaked at
929 MB (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised. What it needs is stack. The deepest call the contract allows, a cold
`net_cf` in the last month of the longest cover, issue age 18, issued now or 120 months
on, runs the account value's chain back to `t_entry()`, 1,252 cells deep in modelx, one
cell a month and 17 more, and compiled with gcc it runs on a thread of 352 KiB of stack and
not of 336, 275 to 288 bytes a level. A test runs it in a thread of 1 MiB, the stack
Windows gives a program's main thread unless the program is linked for more, and again on
the main thread, which is where `run_sec.py --cython` runs. MSVC's frames may be larger
than gcc's, and the `cython` CI job, which runs the test on Windows too, is the check on
them: the test first runs the call at seven stacks, from 256 KiB to 2 MiB, and reports the
smallest it ran on, so a first run there measures MSVC's need, which at
`WholeLife_US_SEC`'s 325 to 433 bytes a level would be about 400 to 530 KiB. A stack below
the need kills its child on an overflow, by design (with gcc, 256 KiB does); on Windows the
child ends with `STATUS_STACK_OVERFLOW`, and should Windows Error Reporting hold it
instead, the test waits two minutes for each bracketing child, and five for the two it
asserts, rather than the job's hour. The export recurses in Python instead: the same call
needs a recursion limit of 2,530 there, and the three reports and the two checks, which
run in ascending `t`, need 60 once the package is imported and 130 with its import, as the
sample runs them, so `sample_sec.py` sets 11,000, four times the first rounded up to the
thousand, and a test holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode, join or hold, when the array is first read, naming every
  point at fault, or the table and its lines: a `point_id` that is not a whole number; a
  `rate_class` the class factors lack, `class_factor_table.csv has no factor for the
  rate_class of point_id [2, 6]`; on a point that `has_surr_charge`, a `surr_charge_id` the
  schedules lack, `surr_charge_table.csv has no schedule for the surr_charge_id of point_id
  [4], each of which has_surr_charge`, and a run-off of 0 years, which the charge's run-off
  divides by. `UL_US_S` fails every projection of such a point, with a `KeyError` or a
  `ZeroDivisionError`, and no projection of a point without a charge reads its schedule, so
  none is refused for it; on such a point whose ID the table lacks,
  `surr_charge_rate_max()` and `surr_charge_runoff_years()` raise `KeyError`, `'point_id
  7: surr_charge_table.csv has no schedule for its surr_charge_id'`, compiled as in
  modelx. And, before it is cast to int64, a number of `2**53` or more in
  size, which numpy would cast to the least int64 past int64: a `point_id`, a model point's
  issue age, `model_point_table_sec.csv: age_at_entry must be below 2**53 in size; it is not
  at point_id [3]`, and a `duration_mth`, a policy issued `2**63` months on, and, on a point
  with a charge, a run-off of `2**53` years or more in size, which `UL_US_S` projects as a
  charge that never runs off. That one is not cast without a word: `lapse_shock_year`'s
  compiled `int` is exact below `2**63` and raises `OverflowError` past it, and the run-off
  is held to the bound every number read as an int is held to. A
  fractional issue age is not refused: it truncates toward zero, as `UL_US_S`'s `int`
  truncates it, so 35.5 projects as 35. A key written as a float, a policy year `9.0`, is
  read by its value, as `UL_US_S`'s lookups match it; a key written as text is not whole,
  and the table's check refuses it.
- A value a cap, a floor, a `min` or a `max` reads that is not a number in its range,
  when the model point table is first read, naming every point at fault, so that a value
  no projection reaches, the cure payment's load, is refused as one that it reads is: the
  face above 0; the premium, the withdrawal and the three tax inputs zero or more; the
  load from 0 to 1; and the surrender-charge flag `True` or `False` (*The in-force
  interface*, above, lists each with the opening state's).
- A negative age in `corridor_factors.csv` or `mort_table.csv`, `corridor_factors.csv: age
  must be 0 or more; it is not on line [2]`, by the table's check, which every reader of
  the table asks first: each is held from age 0, so that the age is the index. A refusal
  `UL_US_S` lacks, which reads every attained age below a table's first at that row,
  whatever the table's ages.
- A key beyond a table, by the one cell that reads it, naming the point, where
  `UL_US_S`'s lookup raised `KeyError`: a policy year below 1, `point_id 1:
  prem_persistency.csv has no factor for policy year 0`, from `prem_persistency_py`, and
  the same from `lapse_rate_base_py` and `coi_rate_guar_py`, none of which a projection
  calls outside cover; and a point whose COI scale the table lacks, `point_id 1:
  coi_rates.csv has no scale for the point's sex, rate_class and age_at_entry`, from
  `coi_rate_last_year`, when its first rate is read.
- By `proj_len()`, a point issued above `omega_age`, at or past the end of the
  projection, or below `issue_age_min`, as *The in-force interface* above quotes.
- A timing or a kind a cell does not take, `ValueError("invalid timing")` and
  `ValueError("invalid kind")`, where the code is inside the cell's cache: a code of the
  other family, `av_pp_at(0, BEF_NB)`, `pols_if_at(0, BEF_PREM)`, `av_at(0, BEF_MAT)`, a
  kind a cell lacks, `claim_pp(0, MATURITY)`, and a code up to 7, `claims_from_av(0, 7)`.
- At a load of 1, `cure_premium_pp`'s `ZeroDivisionError: float division by zero`, which
  `UL_US_S` raises there too. `Data` admits the load, as `UL_US_S` projects it, since no
  report reads the cure payment.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1358)`, which modelx answers with 0, the month being outside cover;
`pols_if_at(0, 8)` and `claim_pp(0, 8)`, which modelx refuses as `invalid timing` and
`invalid kind`; `prem_persistency_py(105)`, which modelx reads at the table's last year,
0.70, and `prem_persistency_py(-1)`, which modelx refuses, naming the year; and
`corridor_factor_at(122)` and `corridor_factor_at(-1)`, which modelx reads at the table's
nearest row, 1.01 and 2.50. An `idx` past the last row is refused in both, with an
`IndexError` at the first read of a vector, and `Projection[-1]` reads every vector at its
last element in both, so it is the table's last point, under that point's own
`point_id()`.

A Reference is a C variable of its value's type: `issue_age_min`, `omega_age`,
`charges_cease_age`, `expense_unit_step_year`, `wd_first_year`, the codes and `idx` a
`long long`, as `Data.future_horizon_mth` is, and the rates and amounts a `double`. Set
past that type, it is converted when it is set, where modelx keeps the value as given. A
float set on an int Reference is truncated toward zero without a word, `omega_age = 120.7`
reading 120 and `issue_age_min = 18.5` reading 18, where modelx computes with the float:
`omega_age = 120.0` makes `omega_mth()` a float there, and `result_cf()` then fails. A
text, a NaN, an infinity or an int beyond 64 bits is refused at once, with `TypeError`,
`ValueError` or `OverflowError`. An int set on a `double` Reference reads as a float
compiled, where modelx returns the int: `lapse_shock_mult = 2` gives `lapse_rate_sc_mult`
2 in modelx and 2.0 compiled in the shock year, and so do `crediting_rate_curr` in
`crediting_rate_ann` and `wd_fee` in `wd_fee_pp`, which return the Reference as it is.
Each shipped Reference is a value of its C type, so no shipped number differs. And a
Reference set past its domain computes as C computes, where modelx raises: an
`inflation_rate` of `1e300` makes `inflation_factor(24)` infinite compiled, where
modelx's power raises `OverflowError`.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
best-estimate rate at 1, `min(q, 1.0)`, as `UL_US_S` does. Uncapped, the monthly rate,
`1 − (1 − q)^(1/12)`, would be complex in modelx and NaN compiled, silently. Capped, both
compute 1. A NaN rate would stay NaN through the cap, in both, as through every other
bound, each of which the compiled model computes as a comparison that keeps the value
unless the bound is smaller, or larger: a NaN `mort_ae_factor`, set as a Reference, makes
`mort_rate(0)` and `net_cf(0)` NaN in both. `Data`'s refusals of a value outside its range
keep any NaN from reaching them through the inputs.

### Speed

`python tools/bench_sec_cy.py universal_life` builds the model into a temporary directory,
or takes a build with `--build`, and times one block run on three engines: modelx, the
export and the compiled model. Each engine runs the committed table repeated, in a process
of its own, as `run_sec.py --block` runs a block, each point projected and then released.
`net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,003 | 1.21 ms (7.26–7.71) | 1.86 ms (11.16–11.81) | 87 MB |
| export | 603 | 14.5 ms (8.72–9.78) | 14.7 ms (8.84–9.53) | 87 MB |
| modelx | 126 | 545 ms (68.7–71.3) | 573 ms (72.1–73.8) | 167 MB |

On `net_cf` the compiled model runs 12.0 times its export, and on `result_cf`, where
building the DataFrame takes much of its time, 7.9 times; it runs 451 and 308 times
modelx. A second run straight after, under a 1-minute load between 1.1 and 2.4, gave the
compiled model 1.25 and 1.89 ms and the export 15.3 and 14.6 ms, 12.2 and 7.7 times, and
modelx 572 and 605 ms. The compiled model takes more than twice `WholeLife_US_SEC`'s time a
point, for frames of 1,032 months on the shipped points against WholeLife's 660 and more
cells a month, and runs about as many times its export as `WholeLife_US_SEC`, 13.9, and
more than `Term_US_SEC`, 9.5, or `BasicTerm_SC` on its own measure, 8.7. As it stood after
running in force, compiled the same way, the model ran 2.2 to 2.3 times its export (*What
compiling changed, and why*, above), and the compiled model runs about nine times that
build on the same measure, 1.17 ms a point over the committed points against 10.4: the
representation, not the compiler, is the gain. The release keeps a block flat: the
compiled model's peak grew by less than 0.1 MB over its 6,003 points, and without the
collection after each release (`--no-collect`), 504 compiled points peaked at 929 MB.
Reading the eight files and building every `Data` vector and array for those points took
0.10 s, and asking every point for its frame, the runner's first pass, 0.28 s.

Measured on 2026-11-12 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 1.1 and 2.6 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Under load the spread is wide, and the fastest run is the
one to compare.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 and 2, issued
  at the valuation date, every cell of `UL_US_S`'s agrees at every argument `UL_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`,
  whose meaning changed, and `coi_rate_scale`, the point's COI scale as a Series, which
  this model replaced by a schedule number, and whose rates the identity compares in
  `coi_rate_guar` in every month; `UL_US_S`'s `claims(t, None)` is compared with the total
  `claims(t)`, and its kinds through the `result_cf` columns `claims_death` and
  `claims_lapse`. A cell this model lacked would fail it. So the goldens
  `tests/test_universal_life_us.py` asserts on those points — every cell of the worked
  example's three rows to the cent, the issue-month trace at full precision, the pitfalls,
  the shortfall table of point 2 — hold here with no number restated. The identity holds
  on any count, since `UL_US_S` already charges acquisition on the policies issued. The
  same suite holds the model to the conventions every `_SEC` model meets: every frame
  starts at `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The splice**, in `tests/test_universal_life_us_sec.py`: each `UL_US_S` point restated in
  force at a month either side of its events continues the S projection, in `result_cf`,
  `result_pols` and `result_av`, column by column, and in every other cell the two share, to
  1e-9, but those the twin identity skips, `pols_if_init` and `model_point`, the accessors
  of the S point's own opening, `duration_mth_init`, `av_pp_init` and `loan_bal_init`, whose
  values are `UL_US_S`'s at its first month, and `proj_len`, which counts from another first
  month. Points 1 and 2 are restated at months 1, 11, 12 and 13, around the first
  anniversary; at 107, the first month without a surrender charge, and 108, 113 and 119,
  inside the lapse-shock year; at 120, where the shock ends and the per-unit charge steps
  down; and at 125. Point 2 is restated at 676 too, where its shortfall begins, point 1 at
  1,031, its last covered month, whose `t = 1` is the month the survivors are carried into,
  and at 779 and 780, either side of the attained age at which the splice's charges cease,
  and point 3 at 1, 6 and 12, besides its own twin from `UL_US_S`'s month 0. So are variants
  of S's points, in a copy of S's table that is never committed, each with its own COI rows,
  for branches S's own points do not reach, each at the months its own events need:
  withdrawals on Option A and on Option B, a single premium with no surrender charge, a
  TARGET premium on a second surrender-charge schedule, an over-funded level premium,
  restated among others in the month it fails the 7-pay test, issue age 18, the longest
  cover, in its last month too, and a level premium of $24,000 a year on Option B, whose
  account value outgrows the face, restated either side of the months the corridor starts
  and stops binding. Between them they carry both sexes and every class. Inflation, the one
  input on the valuation clock that moves a number, is set to 0 in both models, and the
  rest is set in both to reach what the shipped values leave unreached: an acquisition
  expense of $250; the mortality A/E at 0.56, which leaves survivors at the end of every
  frame, so the count and the account value carried into `proj_len()` are compared on every
  row; charges ceasing at attained age 100, inside every frame, where the shipped 121 is
  past the table's last age; and the lapse shock at 10 times, so that the shock year's rate
  meets the lapse rate's cap of 35%.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch above, every opening-state
  column, every kind of valuation month and every premium type, the corridor on either
  option, the lapse rate's cap and charges ceasing in cover among them, and a test asserts
  that they do; the premium is monthly in every case, the only mode the model has. The other
  cases carry the `sec_full` marker and show as skipped, with the reason, unless
  `USLIB_SEC_FULL=1` is set. The `sec` CI job's Linux leg sets it, so every CI run runs
  the full grid too.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point
  is the S projection moved on, cell by cell, the count at each of its timings among them
  but the count before new business in the issue month, which `UL_US_S`'s cell counts as
  in force; with zeros before issue in `result_cf`, `result_pols` and `result_av` and no
  decrement rate evaluated there; and so is each variant issued 13 months on, whose months
  before issue reach policy year −1.
- **How it computes**: on every row the splice and the future business compare, after every
  report, no cell has been called at a negative month, none evaluated from `t_entry()` on
  has read a month before it, and none evaluated at month `t` has read a month later than
  `t + 1`. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, because the policy clock is a closed form, and every point's reports
  run under modelx's recursion limit lowered to 40, which a recursion backward over the
  frame would exceed. And every chain is called cold, on a fresh read, in the last month of
  the twins of points 1 and 3 and at the longest cover, issue age 18, issued now and 120
  months on: `net_cf` first, then each chain's head alone, the loan's, the face's, the
  premiums', the latch's and the count's among them, and modelx's stack trace counts no more
  than one cell a month back to `t_entry()` and a fixed overhead, which a chain of two cells
  a month would exceed.
- **Counts, validation and regeneration**: the roll-forward closes, the last month included,
  `BEF_MAT` is the `BEF_DECR` count, and `pols_if_at` refuses a timing it does not have;
  `result_pols()` is `UL_US_S`'s, column for column, with `pols_new_biz` beside it;
  multiplying `policy_count` by 2.5 multiplies every cash flow by 2.5 and moves no
  per-policy value; each malformed row
  is refused naming its point, a count blank, text, negative or infinite, a duration blank,
  text, fractional or beyond the horizon, an opening-state column missing, blank, text,
  negative, infinite or set on a policy not yet in force, a MEC latch that is no int code, a
  face of zero in force or above the face at issue, a year's usage on an anniversary and a
  latch missing after a failure among them; each assumption table read at a policy year or
  an age is refused naming its file and column, with the lines of a key that is blank, text
  or fractional, or with each key that repeats, its lines, and each that is missing, where
  the keys repeat, leave a gap, miss policy year 1 or have no row, and so is the first
  projection of a point that reads it; so is a rate of those tables, a class factor or a
  surrender-charge value that is blank, text or infinite, with its lines, and a class or a
  schedule blank or on two rows; a `db_option`, `qual_test` or `premium_type` no decode
  knows raises `UL_US_S`'s message; the horizon is a Reference, which at 0 refuses any
  future business, saying so; a point at or past the end of the projection is refused by
  `proj_len()`, and `run_sec.py --block` refuses it before printing anything; a zero count,
  durations and the MEC latch written as floats, the face, the usage and the premiums to
  date written as whole numbers, the keys of the five keyed tables written as floats, a
  policy issued 120 months on, rows either side of the first anniversary and of the seventh
  policy year, a reduced face and a negative `cum_prem_init` are accepted; the committed
  table is what `UL_US_S` generates, and each of its derived and future rows projects its S
  point's three reports from its month on, to 1e-9, which pins the committed counts more
  tightly than the table's own comparison, 1e-12 absolute.
- **The opening state and the rest**: the twin of point 3 is `UL_US_S`'s point 3 from month
  0 on, at the shipped assumptions, in every cell but those expense inflation moves, which
  carries `UL_US_S`'s goldens on it over; the variants carry the premiums paid, the latch,
  the year's usage and the face as above, and with the column as `UL_US_S` assumes it give
  the 450.00, the `False`, the 142.39 and the 100,000.00 above; expense inflation runs on
  the valuation clock at the shipped 2.5%, and the declared rates, overridden to move, are
  one number for every point in each month, which only these tests see, and on those paths
  the account value entering each month is the close of the month before, both checks hold,
  and the twins of S's points 1 and 3 project what `UL_US_S` projects on the same paths,
  the dynamic lapse multiplier above 1 throughout; a check whose residual is not a number
  fails; on S's in-force point withdrawing on Option B, whose loan comes to exceed its cash
  value, both checks hold where `UL_US_S`'s margin identity fails; acquisition falls on new
  business alone; a tobacco point at the shipped A/E, as new business and restated in force
  the month before the cap, is `UL_US_S`'s in every cell, the capped months included, to
  1e-9 with no absolute floor, and on those rows and one restated inside the capped year,
  from `t = 936` at issue, attained age 113, where the cap first binds, its rate is the
  float 1.0 in both models, every life in force dies in that month, nothing is in force
  after it, and its numbers are real and finite, with both checks closing; a NaN sent to
  the cap, through `class_factor`'s formula replaced, stays NaN; every monthly cell holds
  its value outside cover and reads no table there, before issue and at `proj_len()`; the
  points of a block sum row by row; an extract without the generator's three columns,
  relabelled, projects the same numbers; and `run_sec.py` prints the model's numbers, for
  a point issued at the valuation date, a point restated, a point to be issued and the
  block, line by line, and sums the block as `groupby` does, bit for bit; and outside the
  repository, beside a copy of the model or at a path too shallow to hold one,
  `run_sec.py --cython` says it cannot build.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py
  UL_US_SEC --check` makes the same comparison. The tests above held through the compile
  step with their call syntax changed: a point's position for its label, the codes for the
  text of a timing or a kind, and the two claims cells for `claims(t, kind)`. The extract
  is relabelled rather than numbered by position, and each point is named by its label, in
  `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: the claims total is `UL_US_S`'s `claims(t)` bit for bit,
  sign of a zero and type included, on the new-business twins in every month, and in a
  month whose two kinds are both −0.0, set in both models, it is 0.0, as `UL_US_S`'s `sum`
  gives; a fractional issue age projects as `UL_US_S`'s point at the age truncated, bit
  for bit; a point issued below `issue_age_min` is refused by `proj_len()`, naming it, and
  projects under a bound lowered to its age, and a point to be issued above `omega_age` is
  refused whenever it is to be issued; a read beyond a table is refused by the cell that
  reads it, naming the point, and a point without a COI scale projects where no COI rate is
  read, with charges ceasing before its age; the COI schedules are numbered by their keys
  whatever the file's order, on a copy written in reverse; a point at a load of 1 projects,
  and its cure payment raises `UL_US_S`'s own error; the surrender-charge flag written in
  any case reads as the flag it spells; a decrement rate past 1, which makes the count
  complex in modelx, makes each check raise; and the padding beyond each table's extent
  is NaN.
- **Decoding, joins and values a bound reads**: what `Data` cannot decode or join, a
  `point_id` that is not whole or past `2**53`, a class the class factors lack, a schedule
  the surrender charges lack or a run-off of 0 or past `2**53` on a point with a charge, a
  negative age in an age table, and each model point value a bound reads written blank, as
  text, as an infinity or outside its range, is refused naming the points, the table or
  its lines, by the `Data` cell that first reads it and by a projection; a point without a
  charge is not refused for its schedule, reads it where the table holds its ID, as at
  stage E, and raises `KeyError` where it does not; and each edge of each range is
  accepted and projects.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting ones refers to pandas, numpy or another module, reads a table
  with `.loc` or the like, calls a reporting cell, holds text but in its docstring and its
  refusals, or holds a generator, a comprehension or a nested function; none calls
  anything but a cell, a `Data` vector and the builtins of *No Python call kept*, and the
  registry admits no other for this model; every `Data` vector a formula reads is an int64
  or float64 array, read by element; no cell is uncached; and each label accessor returns
  its point's column of the same name.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting ones a C `bint`,
  `long long` or `double` and a C-array cache of exactly the spec's size, and every new
  `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps no
  Python object among a projection cell's locals, calls no Python builtin there, and
  builds no container, under both directives (C3); on the committed points, every cell at
  every argument a full modelx sweep caches is what modelx computes, bit for bit on
  x86-64, and so is every raise and every `Data` array (C4); and `run_sec.py --block`, run
  compiled, holds one point's ItemSpace at a time. In `tests/test_universal_life_us_sec.py`:
  the same comparison on the splice grid, the core by default and the full grid with
  `USLIB_SEC_FULL=1`, variants included, ten rows at a time; at the contract's extremes,
  the longest frames from issue age 18, the oldest issue ages and the bounds of its
  values, from a COI copy written out of its keys' order; and
  where the cap binds, and where a NaN reaches it; the compiled model refuses what modelx
  refuses, with modelx's message, on the relabelled extract too, and an argument past a
  cache raises `IndexError`; on points without a charge, the two schedule accessors read
  the stage E values, and raise `KeyError` on an ID the table lacks, as modelx does, and
  `Data`'s joins are modelx's arrays; the deepest call the contract allows runs cold on a
  1 MiB stack and on the main thread, and the test reports the smallest of seven stacks,
  256 KiB to 2 MiB, it ran on, waiting a bounded time for each; a Reference set after the
  model has computed changes no value it has cached; and `run_sec.py --cython` prints what
  `run_sec.py` prints, and refuses a directory that holds no build. They are marked
  `cython`, and they skip without the toolchain, but in the `cython` CI job, which installs
  it on Linux and on Windows, one leg a product, a skip fails, whatever made it.

```bash
python -m pytest tests/test_universal_life_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_universal_life_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k "[UL_US_SEC]"
python -m pytest tests/test_compiled_conventions.py -q -k "[UL_US_SEC]"
python -m pytest tests/test_universal_life_us_sec.py -q -m cython  # the compiled tests
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
