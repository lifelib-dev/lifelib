# In-Force Implementation Notes

**Status:** Draft, 2026-11-03. `VUL_US_SEC` is [`VUL_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year, and policies to be written in the ten
years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`.
The product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `VUL_US_S` on another time axis, and it reads `VUL_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements come from four registered
> prospectuses [S1] [S2] [S3] [S4]. The separate-account return scenario, the dominant
> assumption for this product, is **[std]** in full, and so are the current COI scale,
> the mortality table, the lapse vector and every expense. Replace them with company data
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/variable_ul/run_sec.py            # point 1: the anchor cell, in force
python products/variable_ul/run_sec.py 6          # point 6: the loan cell, six months on
python products/variable_ul/run_sec.py --block    # every model point, summed row by row
python products/variable_ul/run_sec.py 6 --cython # point 6 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about three
minutes, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and
`.gitignore` covers it.

The first prints, as rows `t = 0 … 11`, the account value roll-forward and the cash flows
`run.py` prints for `VUL_US_S`'s point 1, the worked example's month at `t = 0` among
them, each table line for line the same, and then the counts and rates behind them. Point
1 is in force 24 months at the valuation date, as it is at the start of `VUL_US_S`'s own
projection, so its row `t = 0` is the worked example's month here as there. Three lines to
the same thing for point 6:

```python
import modelx as mx
model = mx.read_model("products/variable_ul/VUL_US_SEC")
model.Projection[5].result_cf()     # point 6, the table's sixth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[5]` is point 6, and its `point_id()` says so. Its four result tables are
indexed by `t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `VUL_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes` and `net_cf` — the **gross (policyholder) view**, income-positive, so the flow columns net to `net_cf` |
| `result_av()` | `VUL_US_S`'s per-policy account value roll-forward, in the columns and order of the technical notes' worked example, with zeros before issue |
| `result_net()` | `VUL_US_S`'s **net-of-account (general-account strain) view**, derived from the same run, under the notes' own column names |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths and lapses, death first, and its maturities, which are always zero; then `VUL_US_S`'s two monthly decrement rates, written 0 outside cover |

`VUL_US_S`'s three self-checks, `check_av_roll_fwd()`, `check_margin()` and
`check_net_view()`, run over the same frame.

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
  date to the end of the projection, the last month at attained age 121.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month from issue,
  `duration_inforce + t`, and the contract runs on it:
  `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1` and
  `age(t) = age_at_entry() + duration(t)`, as in `VUL_US_S`. `BasicTerm_SE` reaches the
  same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

`VUL_US_S` already runs this policy clock, from the first month of its own projection, and
opens its in-force points there: points 1 and 2 at 24 months and point 4 at 120, with
their subaccounts, their fixed option and their loan. What the valuation clock adds is
that `t = 0` is one instant for every point, that a point may be issued after it, and that
a point in force brings in what its past has left it: the loan account, which has grown
apart from the debt since the loan was taken, and the face its withdrawals have left.

Point 4 is `VUL_US_S`'s in-force cell with a loan, in force 120 months. At `t = 0` it is
on the anniversary that opens policy year 11, at attained age 55, with a fixed-option
balance and an $8,000 loan at the preferred loan rate, and its frame has 804 rows,
`t = 0 … 803`. Point 6 is the same policy six months on, in force 126 months: policy year
12 begins at `t = 6`, where the attained age steps to 56, and its frame has 798 rows.
Point 9 is `VUL_US_S`'s point 3 to be issued 25 months after the valuation date:
`duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0 to 24 are zeros,
its first premium of $500.00 falls at `t = 25`, and its frame has 949 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the surrender charge by policy year and the lapse spike at its cliff, policy month `12 × runoff_years`; the loan's preferred rate from policy year 10; the guaranteed COI scale, the base lapse rates and the premium persistency scale by policy year; the corridor factor and the mortality rate at the attained age; the single premium and acquisition in the issue month; premiums, withdrawals and monthly deductions ceasing at attained age 121; the end of the projection at policy month `omega_mth()`; the at-issue pricing path behind the funding ratio, keyed by the policy month from issue | the separate-account return scenario, `gross_return_mth(t, i)`; the declared fixed rate, `crediting_rate_ann(t)`, flat as shipped; expense inflation, `inflation_factor(t) = (1 + inflation_rate)^(t // 12)`, 0 as shipped; the two first-month pins, which apply at `t = 0`, the valuation month |

**The return scenario** is an economic input. `VUL_US_S` keys `scenario_table.csv` by its
projected month `t` already, so the table is on the valuation clock as it stands: a
scenario is a path of the economy from the valuation date, the same month for every point
of a block, however old the policy. On `VUL_US_S`'s own in-force points the two models
read the same months, because `VUL_US_S` opens them at its own `t = 0`. A point restated
at a later month reads the path from its own valuation date instead. `VUL_US_S`'s point 1
restated in force at its month 12 reads month 0 of `WE` as shipped, the worked example's
month, +1.00% on its first subaccount, where `VUL_US_S` in its month 12 reads the level
path, 0.4868% a month. Its first subaccount closes month 0 at 34,396.04 against
`VUL_US_S`'s 34,221.25, 174.79 above, its account value 46.71 below, and its `net_cf` is
0.152 above in month 0 and 0.129 above in month 100. On a copy of `WE` re-based to month
12 the row is `VUL_US_S`'s projection exactly. That is the clock at work, not a fault: a
restated row continues the S projection only on a scenario re-based to its own valuation
date, so the tests give every restated or future row a re-based copy of its own
(*Tests*, below). The committed derived rows all read the flat `LEVEL6`, on which the
month makes no difference.

**Expense inflation** keeps `VUL_US_S`'s step by year and moves it onto `t`, so the
maintenance expense steps on the valuation anniversaries, in valuation-date dollars, for
every point alike. It ships at 0, as in `VUL_US_S`, since the variable-UL notes give the
$75 a year no inflation, so the clock shows in no number. The declared fixed rate is an
economic input too, read at `t`, and ships flat at 1.0%. Acquisition is charged per policy
issued, in the issue month, and not inflated, as in `basiclife/BasicTerm_SE`; it ships at
zero, as in `VUL_US_S`.

**The two first-month pins**, `corridor_override_m1` and `coi_rate_override_m1`, apply at
`t == 0`, as in `VUL_US_S`, and here `t = 0` is the valuation month. Point 1, the worked
example's anchor cell, is in force there, so its `corridor_factor(0)` is the pinned 2.15
and its `coi_rate(0)` the pinned 0.04, where the rule, which takes over at `t = 1`, gives
2.03 and 0.1297335 in policy year 3; point 2, the same cell with both pins blank, takes
the rule from `t = 0`. `Data` refuses a pin on a point issued after the valuation date,
where `t = 0` falls before issue and the pin would never apply, and the generator leaves
the pins blank on every row it restates at a later month.

**The pricing path** behind the funding ratio, the notes' `AV*`, is a projection made at
issue: the account value under the level 6% pricing return, current charges and planned
premiums, with no decrements, loans or withdrawals, from zero at issue. It is keyed by the
policy month from issue, `m = duration_mth(t)`, so it is on the policy clock, and it reads
no state: a point in force reads it from issue, with no opening value. Beyond its chain of
calls, one cell a month here (*Counts and timings*, below), it parts from `VUL_US_S`'s in
two places. `funding_ratio(t)` is 1.0 outside cover before it computes `m`: before issue
`m` is negative, and the path, based at `m = 0`, would recurse without end. And the path
credits its fixed option at `pricing_fixed_return_mth()`, one rate for
every policy month, the declared rate's level, which is
`(1 + max(guar_rate_ann, crediting_rate_curr))^(1/12) − 1`, where `VUL_US_S` credits it at
`fixed_return_mth(m)`, the projection's rate read at a policy month as though it were a
month of the projection. As shipped the two are one float. Under a declared rate that
moves with `t` they part: `VUL_US_S`'s pricing path moves with it, a different rate for
each point, and this model's does not, since no declaration after issue moves a projection
made at issue. The behaviour module ships off, `dyn_behavior_on = False`, so no shipped run
reads the path at all.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
n = len(model.Data.model_point_table())
frames = [model.Projection[i].result_cf() for i in range(n)]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`VUL_US_S` computes, whatever the point's count: `VUL_US_S` charges acquisition on the
policies in force in the issue month, which on new business are the policies issued. On
point 3, the twin of `VUL_US_S`'s one new-business point, every cash flow and every count
agrees, and so does every other cell the two models share, at every argument `VUL_US_S`'s
own sweep evaluates, but three whose meaning changed: `pols_if_init()`, now the count
already in force at the valuation date, 0 for new business; `model_point()`, a row of
another table; and `result_pols()`, which gains `pols_new_biz`. On points 1, 2 and 4,
`VUL_US_S`'s in-force points, which both models open at the valuation date, the projection
is `VUL_US_S`'s from `t = 0` on, in every report and every cell the two share but
`model_point()`, the expenses included, since inflation ships at 0.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `VUL_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and ten of its columns are the in-force interface,
with the shipped lineup of two subaccounts: `basiclife/BasicTerm_SE`'s two, six that open
an in-force policy's state, one of them for each subaccount, and `VUL_US_S`'s two
first-month pins, which apply in the valuation month. Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `sa_pp_init_<i>`, one for each subaccount of `subaccount_table.csv` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | subaccount `i`'s value, the policy's own, never the premium allocation times the account value |
| `fa_pp_init` | dollars | the start of month 0 | the fixed option's value |
| `la_pp_init` | dollars | the start of month 0 | the loan account: the collateral a loan has moved out of the investment options, part of the account value |
| `loan_bal_init` | dollars | the start of month 0 | the policy debt, the interest accrued to then included |
| `sum_assured_init` | dollars of face | the start of month 0: after policy month `duration_mth − 1`'s withdrawal cut | the face in force, after every Option A withdrawal cut to date; at most `sum_assured`, the face at issue |
| `corridor_override_m1`, `coi_rate_override_m1` | a corridor factor, and a current COI rate per $1,000 a month, or blank | the valuation month, `t = 0` | the worked example's two pins, which apply at `t = 0` alone; blank where a point pins nothing, and on a point issued after the valuation date |

The six state columns are 0 on a point issued at or after the valuation date: it is issued
with no account value and no loan, at the face `sum_assured`. `sa_pp_init_<i>`,
`fa_pp_init` and `loan_bal_init` are `VUL_US_S`'s own columns: they already measure the
accounts and the debt entering `VUL_US_S`'s first month, so they keep their names. Each new
column is named for the cell it opens, on `VUL_US_S`'s stem: `la_pp_init` for the loan
account, `la_pp_at`, beside `VUL_US_S`'s `sa_pp_init` and `fa_pp_init`, and
`sum_assured_init` for `sum_assured_at`, under `UL_US_SEC`'s name for the face in force.
`UL_US_SEC`'s other three state columns would open no cell here. The product tracks no free
withdrawal allowance, since the variable-UL notes cut the face proportionately with no free
amount, and neither the premiums paid nor a MEC latch, since the notes do not enforce the
guideline premium or 7-pay limits in the baseline: so there is no `wd_used_year_init`,
`cum_prem_init` or `is_mec_init`. No quantity of the product is read at the last
anniversary, so none needs a column at a second instant.

| `VUL_US_S` | `VUL_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 or more, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `sa_pp_init_<i>`, `fa_pp_init`, `loan_bal_init` | the same | `VUL_US_S` already opens its in-force points from them |
| — | `la_pp_init` | `VUL_US_S` opens the loan account at the debt, `loan_bal_init` **[std]**, which holds on the loan's first day only |
| — | `sum_assured_init` | `VUL_US_S` opens every point at the face at issue, `sum_assured` |
| `corridor_override_m1`, `coi_rate_override_m1` | the same | Applied at `t == 0` in both, which here is the valuation month |

On the twins the two new columns take what `VUL_US_S` itself assumes, so each twin opens as
its S row does: on point 4 a collateral equal to its debt, 8,000.00, and on points 1, 2
and 4 the face at issue, 500,000.

The columns carried over are read as `VUL_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the option, the premium, its load, the
allocation, the withdrawal and the scenario excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `VUL_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the base of the $0.20 per $1,000 charge and of the surrender charge, whatever later withdrawals cut the face to |
| `db_option` | `A` or `B` | the option in force over the frame |
| `qual_test` | `GPT`, the only test modelled | issue |
| `premium_type` | `LEVEL` or `SINGLE` | the pattern over the frame; a single premium falls in the issue month alone |
| `premium_pp_ann` | dollars a year, the planned premium, or the single premium on `SINGLE` | the plan over the frame, paid monthly on `LEVEL`, once in the issue month on `SINGLE` |
| `load_prem_rate` | a fraction of each premium | the current load over the frame |
| `alloc_<i>`, `alloc_fixed` | fractions of each net premium | the allocation over the frame |
| `wd_pp` | dollars a month | the withdrawal taken in every month of cover until attained age 121; 0 on every shipped point |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `scenario_id` | a scenario ID, rows of `scenario_table.csv` | the path read from the valuation date on |
| `provenance` | text: `VUL_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the in-force columns are present, `sa_pp_init_<i>` for each subaccount
  `Data.subaccounts()` lists, and so are `age_at_entry`, `has_surr_charge`, every amount
  the projection reads as a number, `sum_assured`, `premium_pp_ann` and `wd_pp`, and every
  share it reads, `load_prem_rate`, each `alloc_<i>` and `alloc_fixed`;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more: "model_point_table_sec.csv: duration_mth must be -120 or
  more, a policy issued at most 120 months after the valuation date; it is not at point_id
  [9]". Future new business is written over a horizon, `Data.future_horizon_mth`, 120
  months as shipped, so that no frame runs longer than the projection from issue plus ten
  years: 1,584 months at issue age 0, the youngest the product issues, and 1,044 at 45,
  the only issue age the shipped COI scale carries. Set to 0, the Reference refuses future
  new business altogether, and a negative horizon is itself refused;
- `age_at_entry` is a whole number of years, 0 or more: the projection takes its `int()`
  and counts its frame and every attained age on it;
- `sum_assured` is a number above 0, the face every policy holds at issue, and each of
  `premium_pp_ann` and `wd_pp` is a number, zero or more. Each reaches the account value,
  the face or the death benefit, where `VUL_US_S` reads a blank as a missing value;
- `load_prem_rate`, each `alloc_<i>` and `alloc_fixed`, the share of each premium the load
  takes and the shares of each net premium the accounts take, is a number from 0 to 1:
  "model_point_table_sec.csv: load_prem_rate must be a number from 0 to 1; it is not at
  point_id [3]". A load past 1 would credit the accounts a net premium below 0, every
  check passing: at 1.5, point 3's accounts would take −250.00 of its 500.00 premium in
  month 0. Allocations past 1 would credit them more than the net premium;
- `has_surr_charge` is `True` or `False`, as pandas reads those words. A blank, a number or
  any other text is refused, naming only the points at fault: one text value turns the
  whole column into text, where `"False"` is a true string, so that every point would read
  as carrying a surrender charge;
- each subaccount, the fixed option, the loan account, the debt and the face in force is a
  number, zero or more. A balance is never negative in force. `VUL_US_S` lets a subaccount
  fall below zero once the point is in permanent shortfall, because it does not implement
  the grace cascade that would end such a policy, so the message for the accounts says what
  to do: restate a point in permanent shortfall no later than the last month its account
  value is still zero or more, as point 7 is;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros;
- `sum_assured_init` is above 0 on a policy in force, which holds a face, so an extract
  that leaves the column at zero is refused, rather than projected on the corridor alone;
- `sum_assured_init` is at most `sum_assured`, since face increases are not modelled. A
  face below it is accepted, whether withdrawals cut it or an elective decrease the model
  does not implement, and it is projected from the value given;
- the loan account is above 0 exactly where the debt is: "model_point_table_sec.csv:
  la_pp_init must be above 0 where loan_bal_init is, and 0 where it is 0: the loan account
  holds a loan's collateral while the loan is outstanding; it is not at point_id [1]". A
  loan moves value out of the investment options into the loan account, and the model
  takes no new loan and no repayment, so the two are held together from the loan's first
  day, each growing at its own rate;
- each pin is blank, or a number, zero or more;
- each pin is blank on a policy issued after the valuation date: a pin applies in the
  valuation month, `t = 0`, before such a policy is issued, so it would never apply.

A point at or past the end of the projection at the valuation date,
`duration_mth ≥ 12 × (122 − age_at_entry)`, reads, but `proj_len()` refuses it, naming the
point: "point_id 4: duration_mth 924 is at or past the end of the projection, policy month
924, attained age 122". The end of the projection is the model's rule, not the table's. So
a loop over the block meets such a row only when it reaches it, after projecting the
points before it. `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

The assumption tables are checked too, each once, in the `Data` cell its reader in
`Projection` takes its extent, its count or its lineup from. The tables read at a policy
year or an attained age take their extents from `prem_persistency_last_year()`,
`lapse_last_year()`, `corridor_age_first()` and `corridor_age_last()`, and
`mort_age_first()` and `mort_age_last()`, beyond which each reads its nearest row, and from
`coi_schedules()`, which checks `coi_rates.csv` and numbers its issue-age cells, each with
its last policy year. The key column is read by value, so a year written `5.0` is 5, and a
key that is blank, text or not a whole number is refused, naming the file, the column and
the lines it is on. So are keys that do not run one row a year or an age, without a gap or a
repeat, policy years from 1, the message naming each key that repeats, with its lines, and
each that is missing: "lapse_table.csv: the policy years must run from 1, one row a year,
without a gap or a repeat; no line holds policy_year 5". So is a blank sex or class in the
COI scale, and a rate that is blank, text or infinite. A lapse or mortality rate is a
probability, held to 0 to 1, since past 1 the monthly rate `1 − (1 − q)^(1/12)` has no real
value: "lapse_table.csv: lapse_rate_ann must be a number from 0 to 1; it is not on line
[6]". A class factor, a guaranteed COI rate, a fund expense, a premium persistency factor
and a corridor factor are held to 0 or more, since below it each projects negative deaths, a
credit, a negative premium or a death benefit past the option's amount, every check passing.
A COI rate is a charge per $1,000 of net amount at risk, not a decrement, and the current
scale passes 1 from attained age 72, as it should. `class_count()` and `surr_charge_count()`
check the class factors and the surrender-charge schedules, for the per-point joins that
read them, the same way: a class or a schedule blank or on two rows, and a factor or a
charge that is not a number, or is below 0. A charge below 0 is none to `VUL_US_S`'s `max`
through the schedule's years, and after them a charge that rises each policy year: written
at −18.00, the shipped schedule charges $1.29 per $1,000 in policy year 16, every check
passing. `surr_charge_count()` also refuses a run-off that is not a whole number of years, 1
or more: "surr_charge_table.csv: runoff_years must be a whole number of years, 1 or more; it
is not on line [2]". The projection divides the charge by the run-off and counts policy
years on it, where `VUL_US_S` truncates a fraction with `int()` and divides by zero at 0.

Two tables are checked in cells of their own, because their keys do more than find a row.
`subaccount_count()` checks the subaccount lineup, read by value, and `subaccounts()` holds
its ids in the file's order, the one copy of them, whose positions `Projection` reads a
subaccount's inputs at. Its ids name the
model point table's columns, `sa_pp_init_<i>` and `alloc_<i>`, so an id written `1.0` must
still name `sa_pp_init_1`: here it does, and `VUL_US_S`, which names the column from the
id as pandas reads it, asks for `sa_pp_init_1.0` and raises `KeyError`. An id that is
blank, text or not whole, a lineup with no subaccount, an id on two rows and a fund
expense that is not a number, or is below 0, are refused. `scenario_count()` checks the
return scenario, which `scenario_rows()` reads once, in the file's order, so that a
refusal can name lines, and `scenario_last_mths()` gives the last month of each scenario
and subaccount. A blank
`scenario_id`, a `subaccount_id` or `t` that is not whole and a return that is not a
number are refused, and so are months that do not run one row a month, from 0 or later,
without a gap or a repeat, each clause naming its scenario and subaccount:
"scenario_table.csv: the months of each scenario_id and subaccount_id must run one row a
month, from 0 or later, without a gap or a repeat; at ('WE', 1), no line holds t 2". A
path may start after month 0: one re-based to a policy issued after the valuation date
holds nothing before its issue month, and a read there raises.

Each reader asks for its extent, the count or the lineup before it reads a value, so a
projection meets the checks first. `VUL_US_S` takes each extent from the key column as
pandas reads it, where a blank key is a missing value the extent skips: the table is cut
short, and every later year reads the last good row, without a word. A blank value is a
missing value to it too, which shows in its flows or is lost in a `min` or a `max`: a
blank corridor factor reads as no corridor and a blank surrender charge as none. Here the
cap on the mortality rate, `min(q, 1.0)`, keeps a blank base rate or class factor missing,
as `VUL_US_S`'s own does, and each of them is refused before any rate is read.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`VUL_US_S` and its table by `tests/sec_support.py`, from the `VUL_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `VUL_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py VUL_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 2 | twin | S points 1 and 2 | in force 24 months, in policy year 3 at attained age 47, with 30,000.00 and 20,000.00 in the two subaccounts on the `WE` scenario: the worked example's anchor cell, point 1 with the worked example's two first-month pins and point 2 with both blank |
| 3 | twin | S point 3 | issued at `t = 0`: new business on Option B, `VUL_US_S`'s one new-business point |
| 4 | twin | S point 4 | `VUL_US_S`'s in-force cell with a loan, in force 120 months, on the anniversary opening policy year 11, with 40,000.00 and 25,000.00 in the subaccounts, 10,000.00 in the fixed option and an 8,000.00 loan |
| 5 | derived | S point 3 at S month 12 | on its first anniversary, inside the surrender-charge period: 3,877.96 of account value |
| 6 | derived | S point 4 at S month 6 | the in-force cell six months on, in force 126 months, mid-year: 86,248.90 of account value, its collateral 8,039.90 and its debt 8,041.89 |
| 7 | derived | S point 3 at S month 593 | Option B in the month its permanent shortfall begins, policy year 50, attained age 94, with 26.59 of account value |
| 8 | derived | S point 4 at S month 768 | the first month at attained age 119, where the mortality rate reaches 1.0: every survivor dies at `t = 0`, and `result_cf()`'s 35 later rows are zeros |
| 9 | future | S point 3, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `VUL_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `VUL_US_S` carries into it, each column read as
`VUL_US_S`'s own formulas read it: each subaccount as `sa_pp_at(d, i, "BEF_PREM")`, the
fixed option as `fa_pp_at(d, "BEF_PREM")`, the collateral as `la_pp_at(d, "BEF_PREM")`, the
debt as `loan_bal_pp_at(d, "BEF_PREM")` and the face as `sum_assured_at(d − 1)`. So the row
continues the S projection from there: point 5 opens with 0.938584 policies, and point 8
with 4.006e-10. Its two pins are blank, since `VUL_US_S` applies a pin at its own `t = 0`
only, before month `d`, and so are a future row's, copied from its S point's, which are
blank. A derived row's `policy_id` is the S row's with the month appended,
`VUL-000003-M12`, and a future row's carries the months to issue, `VUL-000003-F25`. Row `t`
of a generated point is month `t + source_mth` of its S point. The derived rows restate S
points 3 and 4, which read the flat `LEVEL6`, so they need no scenario of their own. All
nine are on the anchor configuration M45 / StdNT / $500,000, because the notes disclose a
COI anchor for that cell alone [S4], so a point on any other issue age, sex or class needs
`coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
the three timings that `VUL_US_S` already names, each an int Reference named as the string
`VUL_US_S` passes, so that a timing, like every argument, is a C number when the model
compiles:

- `BEF_NB = 0`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR = 1`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_MAT = 2`, the count before any maturity, `VUL_US_S`'s meaning: the `BEF_DECR`
  count, since the contract never matures and no event of the month separates the two.

Any other timing raises, the account value's six among them, which follow in the same
numbering, `BEF_PREM = 3` to `EOM = 8` (*The compiled model*, below). `VUL_US_S`'s cell of
the name returns `pols_if(t)` for every timing, and nothing calls it. `BEF_NB` is the one
timing this model gives a meaning of its own, `basiclife/BasicTerm_SE`'s, and the two models
differ in it alone, in the issue month: there `VUL_US_S` counts the issued policies, and
this model counts them as new business, not yet in. As in `UL_US_SEC`,
`basiclife/BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of the month before its new
business, is not adopted: the name keeps its S model's meaning.

The account value keeps `VUL_US_S`'s timings, codes too, which name the points of the
month in the notes' processing order: `BEF_PREM`, the opening balance; `BEF_WD`, after the
net premium; `BEF_FEE`, after the withdrawal and its fee, the post-premium value the death
benefit and the net amount at risk are measured on; `BEF_INV`, after the monthly
deduction; and `BEF_ME`, after the gross return and the fund expense, before the M&E
charge. `av_at` adds `EOM`, the closing balance before the decrements.

Every chain of calls from month `t` back to `t_entry()` is one cell a month. `BEF_NB`
forms the survivors of month `t − 1` itself, as its own value at `t − 1` plus that month's
new business, less that month's deaths and lapses in the order `pols_death` and
`pols_lapse` take them. Each account's opening balance forms the previous month's close the
same way, the same products in the same order as the closing cell `VUL_US_S` calls for:
`sa_pp_at(t, i, BEF_PREM)` from its own value at `t − 1` and month `t − 1`'s net premium
share, withdrawal share, deduction share and unit-value growth, where `VUL_US_S`'s
subaccount ran through six cells a month; `fa_pp_at(t, BEF_PREM)` likewise, where
`VUL_US_S`'s fixed option ran through five; and the loan account's and the debt's,
`la_pp_at` and `loan_bal_pp_at`, a month's credited or charged interest on their own value
at `t − 1`, where `VUL_US_S`'s ran through two. The subaccounts and the fixed option share
each month's withdrawal and deduction pro rata, so whichever is called first runs the
others alongside it, a month at a time. The face, `sum_assured_at`, calls itself at
`t − 1` before anything else. The account value's opening balance,
`av_pp_at(t, BEF_PREM)`, is not a chain of its own: it is `av_pp(t − 1)`, which sums its
parts' closes.

On a model just read, a cold `net_cf` in the last month of point 1's 900-month frame runs
920 cells deep, against 5,411 for `VUL_US_S`'s point 1: 21 cells above the chain back to
`t_entry()`. Point 3's and point 4's run 21 above theirs too, 944 and 824 cells. At the
longest cover the contract allows, issue age 0 and 1,464 months, it runs 1,484 deep,
whether the policy is issued at the valuation date or 120 months after it, because every
chain stops at the issue month: compiled, about 350 KiB of C stack with gcc (*What a
compiled run needs*, below). Each
chain's head called alone, the loan's, the collateral's, the face's, a subaccount's and the
count's, runs at most 10 cells above its chain. Each report evaluates its columns in
ascending `t`, and on a model just read the committed points' four reports and three
checks run that way under a recursion limit of 17, and `VUL_US_S`'s under 16. That is
with the behaviour module off, as shipped.

With the behaviour module on, the funding ratio reads the pricing path at the policy month
from issue, and the path is a chain of its own, one cell a month, based at issue: each
opening balance of the path forms the previous month's close itself, where `VUL_US_S`'s ran
through four cells a month. So a cold `net_cf` on a point in force runs back to issue, not
to the valuation date: 939 cells on points 1 and 4, the 923 months of the frame's last
month from issue and 16 more. At the longest cover it runs 1,484 deep, module on or off.
The path stays based at issue. Its state is its own balances, the subaccounts' and the
fixed option's, which the pro-rata deduction couples month by month, so a form based at the
valuation date would have to carry them all through one loop in one cell.

So with the module on, the first month's funding ratio of a point in force at policy month
`d` reads the pricing path cold, back to issue, however the months after it are evaluated,
and an ascending sweep runs `d + 16` cells deep: 40 on point 1, 136 on point 4, 904 on
point 8, and 1,478 on a point in force in its last covered month at issue age 0, against
18 on every committed point, and 15 on that one, with the module off. It needs a modelx
recursion limit of `d + 15`, 39 on point 1 and 135 on point 4. A point issued at or
after the valuation date, whose path starts in its issue month, sweeps 22 deep under a
limit of 21. The cold call's bound is unchanged, 1,484 cells at the longest cover, so the
deepest stack is the same; only the depth of a typical point in force grows with its
duration.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `VUL_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < omega_mth()`, where
`omega_mth() = 12 × (omega_age − age_at_entry + 1)` is `VUL_US_S`'s frame from issue, the
first month at attained age 122. Outside it, before issue and from `t = proj_len()` on,
every count, premium, withdrawal, charge, decrement rate, decrement, claim and cash flow is
zero and every flag false; only the two clocks, the inputs read on the valuation clock, the
loan account's level credited rate, and the neutral 1.0 of the two lapse multipliers and
the funding ratio hold values there, and the month after the frame holds one exception
more, below. No count evaluates a decrement rate there, and no table is read at a policy
year or an attained age the policy does not have: `prem_persistency`,
`prem_persistency_base`, `premium_pp`, `wd_pp`, `sum_assured_at`, `corridor_factor`,
`db_pp`, `db_pp_eom`, `coi_rate_guar`, `coi_rate`, `coi_pp`, `maint_fee_pp`,
`loan_rate_ann`, `surr_charge_rate`, `mort_rate`, `lapse_rate_base`, `pols_death`,
`pols_lapse` and `expenses` are zero, and `is_default` false, before any table or rate is
read, and every other value is zero through them. `lapse_rate_sc_mult` is 1.0 there,
before it compares the policy month with the cliff, since a run-off of `n` years puts the
spike at policy month `12 n`, which can be the month after the frame; and `funding_ratio`
is 1.0 before it computes the policy month the pricing path is read at. The scenario's two
readers, `gross_return_mth` and `inv_return_mth`, take no guard, since an economic input
is one path for every point, and no formula reads them outside cover. Each table read at a
policy year or an attained age has one reader keyed by it, called inside cover only, so on
point 9, whose policy year is −2 at `t = 0`, no reader is asked for a policy year below 1
or an attained age below 45.

**The end of the projection.** The frame ends at `omega_mth()` because the mortality table
ends at attained age 121, not at an event of the contract, which never matures. With the
shipped table, whose annual rate is 1.0 from attained age 119, and a class factor and an
A/E of 1 or more, every life has died by the end of the first month at attained age 119:
point 8, valued in that month, loses its last 4.006e-10 of a policy at `t = 0`. With a
preferred class, an A/E below 1 or a table that stays below 1, lives survive the last
month, and `VUL_US_S`'s roll-forwards read them: `check_av_roll_fwd()` and `av_change()`
read the account value in force entering month `t + 1`, which in the last month is
`t = proj_len()`. So the two opening values read there, the count carried in
(`pols_if_at(t, BEF_NB)`, and through it `pols_if(t)`) and the account value carried in
(`av_pp_at(t, BEF_PREM)`), are defined for `0 ≤ duration_mth(t) ≤ omega_mth()`: in the
month after the frame they are the survivors of the last month and the account value they
carry, `VUL_US_S`'s own values there. Everything else is zero or false there, each
account's opening balance included, since a loan account carried into the month would earn
a month's credit past the frame's end, and the expenses, which would otherwise fall on the
carried count. Nothing reads past it: `av_change()` and the three checks' residual cells,
which read `t + 1`, are zero outside cover before they read it. At the shipped assumptions
the survivors at `proj_len()` are exactly 0.0 on every committed point. At an A/E of 0.56,
the rest as shipped, they are 3.88e-6 of a policy on the twin of point 1, 3.46e-6 on the
twin of point 3 and 5.44e-6 on the twin of point 4, each equal to `VUL_US_S`'s, and the
three checks close.

**A lapse rate past 1.** `VUL_US_S`'s annual lapse rate, the base rate times the cliff's
spike times the dynamic multiplier, has no cap, and this model keeps it so. `Data` holds
each base rate to 0 to 1, but the spike, `lapse_shock_mult`, and the multiplier's bound,
`lapse_dyn_cap`, are References. With both at 0 or more, the annual lapse rate is at most
`max(1, lapse_shock_mult)` × (`lapse_dyn_cap` with the behaviour module on, 1 with it off)
× the largest base rate, since the spike is 1 outside its month and the multiplier 1 with
the module off. It stays at most 1 while that product is at most 1: 0.06 as shipped, 0.12
with the module on and 0.36 under the tests' splice. Past 1 the monthly rate
`1 − (1 − q)^(1/12)` is complex, and so is every count after it, in both models: with a
spike of 40, point 3's rate is 1.2 in its cliff month, policy month 168. `VUL_US_S`'s
checks raise `TypeError` there, and so do this model's, whose residuals are `float`s, so
that a complex residual, whose magnitude would pass, cannot. Compiled, the power is NaN
instead, and the checks fail rather than raise.

## The opening state

`VUL_US_S` opens its in-force points from three kinds of column, each subaccount, the fixed
option and the debt entering its first month, and takes the rest as they stand at the start
of a loan and at issue: the loan account equal to the debt **[std]**, and the face at issue.
Its points 1, 2 and 4 need no more, and their twins open the same way. A policy valued in
any month of its life needs all six state columns, each what `VUL_US_S` carries into that
month. Point 6, `VUL_US_S`'s in-force cell six months on, shows two of them, and each is
compared below with the same row read as `VUL_US_S` would open it:

- **`la_pp_init`.** In six months the collateral has grown at the 1.0% credited to the
  loan account and the debt at the 1.05% charged in policy year 11, so point 6 holds
  8,039.90 of collateral against a debt of 8,041.89. Read as the debt, as `VUL_US_S` opens
  its loan account, the account value entering month 0 would be 86,250.89 for 86,248.90,
  1.99 high, and `net_cf` 0.00496 lower in month 0 and 0.00487 lower in month 11.
- **`sa_pp_init_<i>` and `fa_pp_init`.** The two subaccounts and the fixed option hold
  41,701.23, 26,052.83 and 10,454.95, each what its own returns have made of it: the
  subaccounts grow at the scenario's return less their fund expenses and the M&E charge,
  the fixed option at the declared rate. Spread by the allocation, 50/30/20, the unloaned
  78,209.01 would be 39,104.50, 23,462.70 and 15,641.80, the same total, and the account
  value would close month 0 16.12 lower and month 11 196.05 lower, `net_cf` 0.040 and
  0.473 higher.

No committed point withdraws, so none shows the face in force. It shows on
`VUL_US_S`'s point 3 changed to Option A and a withdrawal of $100 a month, at the shipped
assumptions. `VUL_US_S` takes the withdrawal in every month from issue and, on Option A,
cuts the face in proportion to it, as the variable-UL notes say: in the issue month $100
out of the 480.00 of account value the first net premium buys cuts the 500,000 by
104,166.67, and the withdrawals of months 0 to 12 leave a face of 174,445.82 entering
month 13:

- **`sum_assured_init`.** Restated at month 13, the point opens with that face. Month 0's
  withdrawal cuts it by 5,137.44 more, to 169,308.38, the death benefit of month 0, on
  which the cost of insurance is 19.83. Read as the face at issue, as `VUL_US_S` opens
  every point, month 0's cut would be 14,725.03 and the death benefit 485,274.97, with a
  cost of insurance of 57.58. The surrender charge is 8,357.14 either way, since it is
  quoted on the face at issue.

The two pins are not state: they are the worked example's two lookups, applied in the one
month it describes, and the generator leaves them blank on every row it restates.

## Departures from VUL_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state on a
point in force, and each cell that turns `t` into a policy year or an attained age answers
for the months outside cover. Of `VUL_US_S`'s 148 cells in `Projection`, 60 are unchanged,
36 have a new docstring only, most of them to say what `t` now counts, and 52 are
rewritten. None is removed or renamed, and 28 cells are new, 176 in all. Compiling then
changed how each cell reads its inputs and spells its codes, and no number: it replaced two
cells, `subaccount_ids` and `coi_rate_scale`, by the lineup's size and a schedule number,
and added seven, 181 in all (*The compiled model*, below); of `VUL_US_S`'s cells it
changed the signature of two, `claims` and `me_charge_pp`, each now a total. The twin
identity exempts `subaccount_ids` and `coi_rate_scale`, each with its reason, compares
`VUL_US_S`'s `claims(t, None)` and `me_charge_pp(t, None)` with the totals, and reads each
of `VUL_US_S`'s subaccount ids at its position in the lineup: a cell of `VUL_US_S`'s that
this model lacked, or took other arguments, would fail it otherwise. `VUL_US_S`'s `math`
Reference is dropped. Of `Data`'s eleven, `model_point_table` is rewritten to check the
table as it reads it, `scenario_table` is formed from `scenario_rows()`, the scenario's one
read, the same frame as `VUL_US_S`'s, and five readers have their `read_csv` call wrapped;
running in force added twelve cells, 23 in all, and the Reference `future_horizon_mth`,
120. Compiling added 42 cells, 65 in all, and the References `np` and
`return_horizon_mth`, 1,585, the last month the array of returns holds; it made three of
the checks ints, and widened the checks of the model point table and of the two age
tables. The cap on mortality,
`min(q, 1.0)`, is `VUL_US_S`'s own, and no departure. Some departures come from compiling
rather than from the clock: `proj_len`'s new refusals, `gross_return_mth`'s past the
horizon and the last four rows below.

| Cells | `VUL_US_S` | `VUL_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `omega_mth` | `12 × (omega_age − x + 1) − duration_mth_init()`, the months from the first projected month | `omega_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the end of the projection, on a point issued above `omega_age`, 121, below `issue_age_min`, 0, or above `issue_age_max`, 85, and on a lineup of more than `subaccount_max`, 9, subaccounts | `omega_mth()` is new and is `VUL_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left has no frame, nor one that would never be in cover, and the compiled caches hold the contract's frames and lineups alone |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, BEF_DECR)`, from `t_entry()`; `BEF_NB` the count before the month's new business, and `BEF_MAT` the `BEF_DECR` count, as in `VUL_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `sa_pp_at`, `fa_pp_at`, `la_pp_at`, `loan_bal_pp_at` | `sa_pp_init(i)`, `fa_pp_init()`, and `loan_bal_init()` for the loan account and the debt alike, at `t = 0`, then the previous month's closing cell: chains of six cells a month, five, two and two | the openings at `t_entry()`, the loan account from `la_pp_init()`, then the previous month's close formed in the cell itself, `VUL_US_S`'s arithmetic in its order; every timing zero outside cover | Every chain one cell a month, since a compiled model runs it on the C stack; the loan account and the debt part once interest accrues |
| `av_pp_init`, `av_pp_at` | `sum(SA_i(0)) + FA(0) + D(0)`, the debt standing in for the loan account, opened at `t = 0` | `sum(SA_i(0)) + FA(0) + LA(0)`, the subaccounts summed in a loop, opened at `t_entry()` and carried into `t = proj_len()` | The loan account is part of the account value, the debt is not |
| `sum_assured_at`, `face_reduction_pp` | the face at issue at `t = 0`, then the previous month's | `sum_assured_init()` at `t_entry()` on a point in force, the face at issue on any other, then the previous month's | A policy in force brings in the face its withdrawals have left |
| `funding_ratio`, `sa_pricing_pp_at`, `fa_pricing_pp_at`, `fa_pricing_pp` | the pricing path read at `duration_mth(t)` in any month; its fixed option credited at `fixed_return_mth(m)`; each opening balance the previous month's closing cell, four cells a month | 1.0 outside cover, before the policy month is computed; the fixed option credited at `pricing_fixed_return_mth()`; the previous month's close formed in the cell itself | Before issue the policy month is negative, and the path, based at issue, would recurse without end. `fixed_return_mth(m)` reads the projection's declared rate at a policy month: a rate path on the valuation clock would credit each point's pricing path with rates declared after the valuation date |
| `prem_persistency_base`, `coi_rate_guar_at`, `lapse_rate_base`, `corridor_factor_at`, `mort_rate` | the table read in the cell, clamped to the extent of the key column as pandas reads it | one reader keyed by the year or the age — `prem_persistency_py`, `coi_rate_guar_at`, `lapse_rate_base_py`, `corridor_factor_at`, `mort_rate_base_at` — with `VUL_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the rates, called inside cover only | No table is read at a year or an age the policy does not have, each is read once a year or an age, and a blank, text or fractional key, keys that repeat or leave a gap, a rate that is not a number, a lapse or mortality rate outside 0 to 1 and a premium persistency factor or a COI rate below 0 are refused by name, where `VUL_US_S`'s extent skips a blank key and cuts the table short, a blank rate is a missing value, and a rate or a factor out of range projects a count, a premium or a charge no policy can have |
| `surr_charge_rate`, `lapse_shock_month` | the schedule's row read in each | `surr_charge_rate_max()` and `surr_charge_runoff_years()`, one accessor for each of the schedule's two columns, which `Data` joins to the points once `surr_charge_count()` has checked the table, on every point whose ID the table holds, with a charge or without; on a point without one whose ID the table lacks, a blank ID included, both accessors raise `KeyError`, naming the point, as their `.loc` did at stage `E`; `lapse_shock_month` takes the `int()` of the run-off where `VUL_US_S` takes it, and `surr_charge_rate` divides by the run-off as the whole float it is | The same numbers on any schedule, with no table read in a monthly cell; a blank charge, which `VUL_US_S`'s `max` reads as none, a charge below 0, which it reads as none and then as a charge rising once the schedule has run off, and a run-off that is not a whole number of years, 1 or more, are refused |
| `subaccount_ids`, `alloc`, `fund_expense_ann`, `sa_pp_init`, `gross_return_mth` | the lineup, a list of ids, and the scenario as pandas reads them; a subaccount named by its id, its columns `alloc_<id>` and `sa_pp_init_<id>`; the scenario's extent taken from its rows in each month, and each return joined on the scenario's text keys | `subaccount_count()`, the lineup's size, `Data` having checked the lineup and read its ids by value, and a subaccount its position in the lineup, from 0, each cell refusing a position outside it; the scenario's number by point, `scenario_index()`, and its returns, its first months and its last, `scenario_last_mth(i)`, read from `Data`'s arrays, which `scenario_count()` checks; a month before a scenario's first refused, naming the point; and a month past `Data.return_horizon_mth`, 1,585, refused, naming the point and the scenario by its number, `scenario_index()`, where `VUL_US_S` reads the scenario's month, or its last, as stage `E` read it; so is every month of a scenario that starts past the horizon, which `Data` holds nothing of | An id written `1.0` still names `alloc_1`; a fund expense below 0, and a gap, a repeat or a blank in the scenario, are refused by name; a compiled cell takes and returns C numbers, so no list, text key or column name reaches one (*The compiled model*, below). `Data` holds the returns to the horizon alone, the last month a frame the contract allows reads, so a month past it, which no frame reads, would take the horizon's return, where `VUL_US_S` reads its own, or, on a scenario that starts past it, the padding: the read is refused rather than answered otherwise, and nothing `VUL_US_S` projects is refused |
| `premium_pp`, `prem_pricing_pp`, `db_pp`, `db_pp_eom`, `db_pricing_pp`, `face_reduction_pp`, `corridor_factor` | branches on the text of `premium_type()`, `db_option()` and `qual_test()` | branches on five decodes, `is_level_premium()`, `is_single_premium()`, `is_db_option_a()`, `is_db_option_b()` and `is_gpt()`, each read from a 0/1 vector `Data` decodes from the column | No monthly cell compares text, and no projection cell calls a label accessor. The label accessors stay, for reporting, and a value no decode knows still raises `VUL_US_S`'s message |
| `class_factor`, `coi_rate_scale`, `coi_rate_last_year` | the class factor and the COI scale, joined on the label accessors, the scale a Series sliced from the table by the point's sex, class and issue age | the class factor joined to the points in `Data` once `class_count()` has checked its table; `coi_schedule()`, the number of the point's scale, a row of `Data`'s table of the scales by policy year, whose last year is a `Data` vector by schedule; a point whose scale the table lacks is schedule 0, refused, naming it, where a rate is read | A blank factor, a missing value to `VUL_US_S`, would reach the cap on `mort_rate`, which keeps it missing, and is refused, as is one below 0; a blank COI rate would reach the account value. No compiled cell returns a Series, and `VUL_US_S` projects a point that never reads its scale, valued or issued at or past `charges_cease_age`, so the refusal waits for the read |
| `corridor_factor`, `coi_rate` | the pin read from the model point in the cell, applied at `t == 0` | the pin read once a point as a value and a flag, `corridor_override_m1()` and `has_corridor_override_m1()`, `coi_rate_override_m1()` and `has_coi_rate_override_m1()`, each a `Data` vector, the value NaN where the pin is blank, applied at `t == 0`, the valuation month | A monthly cell tests a flag rather than a missing value, and reads no model point column in its own formula |
| `prem_persistency`, `premium_pp`, `wd_pp`, `sum_assured_at`, `corridor_factor`, `db_pp`, `db_pp_eom`, `coi_rate_guar`, `coi_rate`, `coi_pp`, `maint_fee_pp`, `loan_rate_ann`, `surr_charge_rate`, `is_default`, `mort_rate`, `lapse_rate_base`, `lapse_rate_sc_mult` | unguarded: no `VUL_US_S` frame has a month before issue | zero or false outside cover, `is_active(t)`, before any table or rate is read; `lapse_rate_sc_mult` 1.0 | A future point's months before issue have `t ≥ 0` and policy years down to −2. At `t = proj_len()` nothing is charged, paid or withdrawn, whatever `omega_age` and `charges_cease_age` are set to |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `wd_pp` | the model point's `wd_pp` column read in the monthly cell | read once a point, by `wd_pp_mth()` | A monthly cell the accounts' chains read reads no table |
| `inflation_factor` | `(1 + inflation_rate)^(policy_year(t) − 1)`, stepping on the policy anniversaries | `(1 + inflation_rate)^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_margin`, `check_net_view` | `math.isclose` with both tolerances at `1e-9`, month by month | the same condition on one relative residual a month, `check_av_roll_fwd_resid(t)`, `check_margin_resid(t)` and `check_net_view_resid(t)`, each a `float`; a residual that is not a number fails, and one that is not real raises, as `VUL_US_S`'s check does | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin`, `check_net_view` | the lapse term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the loan a surrender recovers; the death term keeps the whole loan | The surrender claim is the net cash value floored at 0, so once a loan exceeds the cash value `VUL_US_S`'s identities are off by `(csv_pp(t) − loan_bal_pp(t)) × pols_lapse(t)` and its checks fail on a projection that is right; the death claim has no floor. On every shipped point the cash value covers the loan, and the two agree |
| `result_pols` | `pols_if`, the three outflows and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `claims` | `claims(t, kind=None)`: one kind's claims, or with `None` the two summed by Python's `sum` | `claims_death(t)` and `claims_lapse(t)`, the `result_cf` columns, and `claims(t)` their total, `0.0 + death + lapse` | A compiled cell takes C numbers, and `None` is none. Python's `sum` of two floats is their sum, rounded once, from its `0.0` start, which this computes, so the total is `VUL_US_S`'s float in every month, the sign of a zero included |
| `me_charge_pp` | `me_charge_pp(t, i=None)`: one subaccount's M&E charge, or with `None` the lineup's summed by Python's `sum` | `me_charge_sa_pp(t, i)`, a subaccount's, and `me_charge_pp(t)` the lineup's total, a loop from `0.0` | As for `claims`; and a subaccount's share of an amount is `<amount>_sa_pp(t, i)`, as `wd_sa_pp` and `mth_deduction_sa_pp` already were. On the shipped lineup of two the loop is `VUL_US_S`'s `sum` bit for bit; on three or more it can differ from it in the last bit (*The compiled model*, below) |
| `unloaned_av_pp_at`, `av_pp`, `av_pricing_pp_at`, `av_pricing_pp`, `inv_income_pp`, `sa_transfer` | Python's `sum` of a generator over the lineup | a loop over `range(subaccount_count())` from `0.0`, the terms in `VUL_US_S`'s order | A compiled cell holds no generator. The same float as `VUL_US_S`'s on two subaccounts |
| `Data` and the cells that read a table | a malformed value or key met, if at all, only when a projection reaches it, a missing class, scenario or schedule as `KeyError`, and an age table read at its nearest row whatever its ages | refused by name at the first read of the array, over the whole table: an issue age, a `duration_mth` or a `point_id` past `2**53`, a class the class factors lack, a scenario the return scenario lacks or holds no row of a lineup subaccount for, a schedule the surrender charges lack or a run-off of `2**53` or more on a point with a charge, a negative age in the corridor or mortality table, and a corridor factor below 0 | A compiled model holds numbers, not text, computes a NaN as silently as modelx, and holds each age table from age 0 (*What it refuses*, below) |

The other new cells of running in force are `policy_count`, `t_entry`, `is_active`,
`pols_new_biz`, the two new opening-state accessors, `la_pp_init` and `sum_assured_init`,
`coi_rate_last_year`, the extent of a point's COI scale, and `wd_pp_mth`, the withdrawal
column read once a point; those of compiling are listed under *What compiling changed, and
why*, below.
Of the cells with a new docstring only, `first_default_month` and `first_shortfall_month`
keep `VUL_US_S`'s loops and return a month counted from the valuation date: point 7,
restated in the month its shortfall begins, is in shortfall from `t = 0`.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it, and only once inflation is switched on: it ships at 0. At 2.5% a year, point 4's
`expenses(t)` is `VUL_US_S`'s divided by `1.025^10`, about 1.280, at every `t`, and point
1's by `1.025^2`: both models step on their anniversaries. Point 6's is `VUL_US_S`'s point
4's divided by `1.025^10` for `t = 0 … 5` and by `1.025^11` for `t = 6 … 11`, where its
policy year has stepped and the valuation year has not. Point 9 is `VUL_US_S`'s point 3
twenty-five months on in its other cash flows, its counts and its account value. Its
maintenance expense is `1.025^2` above `VUL_US_S`'s, and `1.025^3` in the last month of
each policy year, where the valuation year has stepped and the policy year has not.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, on the points of the splice
grid, which take the branches they do not, on the contract's longest frames and a lineup
of nine subaccounts, and where the cap on mortality binds or a NaN reaches it. The compile
tests hold it so on x86-64, and to 1e-12 relative elsewhere, where no run has shown it
yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py variable_ul                   # in place, beside the model
python tools/build_sec_cy.py variable_ul --out /tmp/vul    # elsewhere, with the CSVs
```

The tool exports the model to `VUL_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `VUL_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/variable_ul")    # the directory holding the build
from VUL_US_SEC_nomx_cy import mx_model as model
model.Projection[5].result_cf()               # point 6, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 5` after `Projection.result_cf()` leaves point
1's frame cached, while `point_id()`, not yet computed, reads point 6's label, and
`Projection.expense_maint` set to 90 once `Projection[3]` has computed point 4's
`expenses(12)` leaves it at 6.0417, where an ItemSpace made after computes 7.2500. Set
every Reference on a model just imported, before anything is computed, where modelx would
recompute; a test holds the compiled model to this.

A build takes about three minutes with gcc, 170 s here, and needs a C compiler,
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
typed 144 of its 176 `Projection` cells as C numbers. Fifteen more took a timing or a
kind as text, or `None` for a kind or a subaccount, three were never called by the
reports and compiled as Python objects, and those 18 kept a dictionary for a cache; it
ran no faster than its own export, 279 ms a point on `net_cf` against 279, over the
committed points. The bodies of the typed cells still called pandas and Python: a
`model_point()` lookup for each attribute a formula reads, a `.loc` on a table for each
policy year's persistency, lapse and COI rate, each attained age's corridor factor and
mortality, each point's class factor and surrender-charge schedule, a join on the
scenario's text keys for each month's return, a column named `"alloc_" + str(i)` for each
subaccount, the point's COI scale sliced into a Series, `pd.isna` on the two pins, text
compared in every formula that branched on the death benefit option, the qualification
test or the premium pattern, a generator summed over the kinds in `claims`, and seven
summed over the lineup. So each input
now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[5]` is point 6, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Subaccounts by position.** `VUL_US_S` names a subaccount by its id, lists the lineup's
  ids in `subaccount_ids()` and reads a point's allocation and opening value from the
  columns `alloc_<id>` and `sa_pp_init_<id>`. Here a subaccount is its position in the
  lineup, `i`, from 0, in the order of `subaccount_table.csv`: `subaccount_count()` is the
  lineup's size, which replaces `subaccount_ids()`, and `Data` holds the allocations and
  the opening values as tables by point and position, `alloc()` and `sa_pp_init()`, and
  the fund expenses as a vector by position, `fund_expense_ann()`. The ids are kept in
  `Data.subaccounts()`, for the reports, so `result_av()` names its columns `sa1_bef_prem`
  and so on, as `VUL_US_S` does. A position outside the lineup is refused, naming the
  point, by each of the four cells that read a subaccount's input, `alloc`,
  `fund_expense_ann`, `sa_pp_init` and `scenario_last_mth`, so that no cell reads another
  point's element or a column past the lineup.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once: the death benefit option
  into `is_db_option_a` and `is_db_option_b`, the qualification test into `is_gpt`, the
  premium pattern into `is_level_premium` and `is_single_premium`, and `has_surr_charge`
  into a flag of its own. Each decodes as `VUL_US_S` compares the column, so a value none
  of the flags names is no flag, and the cell that branches on it raises `VUL_US_S`'s
  message, as `VUL_US_S` does. Each first-month pin is a float64 vector beside a 0/1 flag
  of whether the point gives one: the value is NaN where the pin is blank, as `VUL_US_S`
  reads it and as the accessor returned at stage `E`, and the flag, never the value,
  decides, so no NaN reaches a formula.
- **Tables indexed by integers.** The persistency and lapse tables are held by policy
  year, and the corridor and mortality tables by attained age, padded from 0 so that the
  year or the age is the index. The COI scales, keyed by sex, class and issue age, are
  numbered from 1 in the order of those keys, each point carrying the number of its own,
  `coi_schedule()`, and held by schedule and policy year in `coi_rate_array`, with the
  last policy year of each schedule beside it, `coi_rate_last_years`, read at the point's
  schedule. The return scenarios, keyed by their id, are numbered the same way, each point
  carrying its own, `scenario_index()`, and held by scenario, subaccount position and month
  in `gross_return_array`, sized to the months a frame reads, with the first and last month
  of each scenario and subaccount beside it, so that `gross_return_mth(t, i)` is one load
  at `min(t, last)`. The padding holds NaN, and nothing reads it: each table's one reader
  refuses a policy year below 1, or a month before a scenario's first or past
  `return_horizon_mth`, naming the point, and reads an age outside the table at its
  nearest row, as `VUL_US_S` does. The class
  factor and the surrender-charge schedule are one number a point, and each is joined to
  the points in `Data`, which refuses a key the table lacks, naming every such point, since
  `VUL_US_S` reads both on every projection of the point: the class factor in every month
  on the books, and the schedule in every month of a point with a charge. So is the return
  scenario, which every projection reads, at every subaccount, in its first month on the
  books. A point without a charge is never refused for its schedule, which `VUL_US_S`
  never reads; it reads its schedule's two columns where the table holds its ID, as at
  stage `E`, and where the table does not, `has_surr_charge_schedule()` is 0 and both
  accessors raise `KeyError`, naming the point, where their `.loc` raised it at stage
  `E`. A point whose COI scale the table lacks is another matter: it reads the
  scale only while charges run, and a point valued or issued at or past
  `charges_cease_age` never does, so `VUL_US_S` projects it. So it is schedule 0, with a
  last year of 0, and `coi_rate_last_year` refuses it, naming it, where a rate is read.
- **Codes.** A timing or a kind, which `VUL_US_S` spells as text, is an int Reference named
  as the text: the count's timings `BEF_NB = 0`, `BEF_DECR = 1` and `BEF_MAT = 2`, the
  account value's `BEF_PREM = 3`, `BEF_WD = 4`, `BEF_FEE = 5`, `BEF_INV = 6`,
  `BEF_ME = 7` and `EOM = 8`, and `DEATH = 0`, `LAPSE = 1`, `MATURITY = 2` and
  `WITHDRAWAL = 3`. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`,
  `sa_pp_at(t, i, BEF_FEE)`, `claim_pp(t, DEATH)`. A string argument would give the cell a
  dictionary for a cache, where a code indexes a C array, so codes are numbered from 0
  without a gap. The two families of timing, the count's and the account value's, passed
  to different cells, are numbered as one, `BEF_NB` and `BEF_DECR` first, as in every SEC
  model, then the count's third, then the account value's in the order of their instants
  within the month, `EOM` last, as `UL_US_SEC` numbers them, with `BEF_ME`, the one instant
  variable UL adds, in its place. So no two timings share a code, and a code of one family
  passed to the other's cell, `av_pp_at(t, BEF_NB)`, is refused as `invalid timing` in both
  engines, where two families numbered from 0 would read it as `BEF_PREM` without a word.
  A cell compares a code with `==` alone, so that a text passed where a code is taken
  meets the cell's own refusal in modelx too. The `Projection` docstring's *Codes* lists
  all thirteen.
- **The two totals, split.** `VUL_US_S`'s `claims(t, kind=None)` is one kind's claims or,
  with `None`, the two summed by a generator, and its `me_charge_pp(t, i=None)` one
  subaccount's M&E charge or, with `None`, the lineup's summed: neither a C parameter nor a
  C loop. Here the kinds are two cells, `claims_death` and `claims_lapse`, the `result_cf`
  columns, and `claims(t)` is their total, `0.0 + death + lapse`; and a subaccount's M&E
  charge is `me_charge_sa_pp(t, i)`, the name the family gives a subaccount's share, and
  `me_charge_pp(t)` the lineup's total, a loop from `0.0` (*Departures from VUL_US_S*,
  above).
- **Loops for generators.** `VUL_US_S` sums over the lineup with `sum()` of a generator in
  eight cells: the unloaned and the total account value, `unloaned_av_pp_at` and `av_pp`,
  the pricing path's two, `av_pricing_pp_at` and `av_pricing_pp`, the M&E total, the
  investment income, `inv_income_pp`, the transfer to the general account, `sa_transfer`,
  and the account value at issue, `av_pp_init`, a loop since running in force. Each is a
  loop over `range(subaccount_count())` from `0.0`, the terms in `VUL_US_S`'s order. On the
  shipped lineup of two it computes `VUL_US_S`'s float bit for bit: Python's `sum()` of
  floats is compensated since 3.12, and the compensated sum of two terms, rounded, is their
  sum rounded once, which the loop computes. On a lineup of three or more the two can
  differ in the last bit: on 100,000 random lineups of three balances they differed 19,064
  times. The fingerprint and the comparison of the compiled model with modelx compare this
  model with itself, so neither is affected, and the twin identity's tolerance is far
  above a last bit; `VUL_US_S` ships two subaccounts, so no committed number moves.
- **Two cells dropped.** `subaccount_ids()`, a list, and `coi_rate_scale()`, the point's
  COI scale as a Series, are gone, `subaccount_count()` and `coi_schedule()` in their
  place. The twin identity exempts both, with the reason, and compares the COI rates in
  `coi_rate_guar` in every month and the lineup's subaccounts at their positions.
- **No Python call kept.** No formula outside the reporting cells calls a Python builtin
  outside its refusals but `int`, `float`, `bool`, `abs`, `min`, `max` and `range`, which
  Cython turns into C, all but one `int`: `lapse_shock_month`'s `int` of the run-off, a
  float, is a Python int converted to a C `long long`, exact below `2**63` and raising
  `OverflowError` past it, and `Data` holds the run-off below `2**53` (*What it refuses*,
  below). So `tests/us_registry.py` admits none. `surr_charge_rate` divides by the run-off
  as the float it is, where `VUL_US_S` divides by its `int()`: `Data` holds it to a whole
  number of years, which the float is exactly, so the quotient is the same float, and an
  `int()` there, held in a local, would keep a Python object in the cell. No cell is
  uncached, and none takes a float.
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `rate_class()`, `db_option()`, `qual_test()`, `premium_type()`, `surr_charge_id()` and
  `scenario_id()`, and the four reports return a table row, text and DataFrames, for a
  reader, for `run_sec.py` and for the comparison with `VUL_US_S`. No other cell calls
  them, so they cost the projection nothing. A label accessor returns its column as read,
  and `Data` accepts a label that is not text: a blank `surr_charge_id` on a point without
  a charge, which reads as NaN, or a column of numbers, ints, which `VUL_US_S` projects, a
  numeric `scenario_id`, `sex` or `rate_class` written so in both files, which joins as
  text does, and any other blank or numeric label, which the point's first projection
  refuses. So each accessor compiles to a Python object, as the sample traces it (below),
  and returns what modelx returns. The three checks are reporting cells too, but they
  return a verdict, which compiles to a C `bint`.

The `Data` docstring lists its vectors, arrays and counts, each with the column or file it
comes from: 13 vectors of int64 by point and 15 of float64; the allocations and the opening
values of the subaccounts, float64 by point and position; the lineup's ids, int64, and
fund expenses, float64, by position; four float64 tables by policy year or attained age;
the COI scales by schedule and policy year, and their last years by schedule; the first
and last months of each scenario and subaccount, int64, and the returns by scenario,
subaccount and month, float64; and eleven int counts and extents, each a table's check,
among them `subaccount_count`, the lineup's, `scenario_count`, the return scenario's, and
`coi_schedules`, the COI scale's, which at stage `E` were a DataFrame and two Series. The
twelve readers stay Python, returning DataFrames and a path, and no `Projection` cell but
`model_point()` reads them. Every other cell of `Projection`, 169 of its 181, returns a C
`bint`, `long long` or `double`, and caches a single value, or a C array the spec sizes
from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,586 by `t`, of `double`, `long long` or `bint` | the 87 cells of `t` alone: every count, rate, factor, charge, premium, withdrawal, value, claim and cash flow; the policy clock, its years and the attained ages; the flags `is_active`, `is_default` and `is_shortfall`; and the checks' monthly residuals |
| a C array of 1,586 by 9 | the 15 cells of `t` and one code or position: `pols_if_at`, `av_pp_at`, `av_at`, `unloaned_av_pp_at`, `fa_pp_at`, `la_pp_at` and `loan_bal_pp_at`, by `(t, timing)`; `claim_pp` and `claims_from_av`, by `(t, kind)`; and `sa_pp`, `gross_return_mth`, `inv_return_mth`, `wd_sa_pp`, `mth_deduction_sa_pp` and `me_charge_sa_pp`, by `(t, i)` |
| a C array of 1,586 by 9 by 9 | `sa_pp_at`, by `(t, i, timing)` |
| a C array of 1,465 by `m`, and of 1,465 by 9 and by 9 by 9 | the pricing path, by the policy month from issue: eight cells of `m` alone, `fa_pricing_pp_at` and `av_pricing_pp_at` by `(m, timing)`, `sa_pricing_pp` by `(m, i)`, and `sa_pricing_pp_at` by `(m, i, timing)` |
| a C array of 124 by `y` | `prem_persistency_py`, `lapse_rate_base_py`, `coi_rate_guar_at` and `coi_rate_at`, by policy year |
| a C array of 123 by `a` | `corridor_factor_at` and `mort_rate_base_at`, by attained age |
| a C array of 9 by `i` | `alloc`, `fund_expense_ann`, `sa_pp_init` and `scenario_last_mth`, by position |
| one `long long`, `double` or `bint` | the 44 cells without a parameter: the point's label, numbers, decodes and flags, its opening state, its pins and their flags, its class factor, COI schedule and the scale's last year, its scenario's number, its surrender charge, run-off and cliff, the lineup's size, the ends of its frame, the pricing rates, the first default and shortfall months, and the three checks |
| a Python object | the twelve reporting cells but the checks |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` first switches the
behaviour module on, `dyn_behavior_on`, which ships off: off, no report reaches the
pricing path behind the funding ratio, the premium persistency scale or its reader. With
it on, it runs the four reports and the three checks on every committed point, which reach
every cell but these: `model_point()` and the seven label accessors, which only a reader
asks for; `point_id()`, which only a refusal names; `inv_return_mth`, the unit-value
factor the account chain forms inline; the default and shortfall tests and their searches;
and the pricing path's three closes, `sa_pricing_pp`, `fa_pricing_pp` and `av_pricing_pp`,
which each opening timing forms itself. And of the cells they reach they leave some codes
uncalled: `pols_if_at`'s `BEF_MAT`, `claims_from_av`'s `MATURITY`, and the account cells'
timings no formula passes them. The sample calls those too, the monthly ones in every
month of the frame and the month after it, every account cell at every timing it takes,
and the pricing path at every policy month a point reads, from issue to its last month in
cover. It projects the committed points alone: the export it runs reads the CSVs of the
directory the build is made in, and the trace it needs is the committed points', which are
what the tests project. The seven label accessors it calls once more, on a copy of the
table's first point with every label blank, which it writes to a temporary directory and
reads by a second instance of the export, given the file's absolute path as
`model_point_file`. That types them as Python objects, so that a blank or numeric label
returns what modelx returns rather than raising `TypeError` (*What compiling changed, and
why*). The committed points leave branches untaken: a withdrawal, a single premium, a
point without a surrender charge, the COI rate's cap and the guaranteed bound binding,
mortality capped at 1, a first-month pin on a point issued at the valuation date, the
corridor pin alone. That still types every cell, because every branch of a cell returns
the one type its others return, a rate a float in every branch, and on points that take
those branches the compiled model computes modelx's numbers (above). The sample also
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
| `t` | 1,586 | 1,584. The longest frame is a policy issued at the youngest issue age, 0, to the end of the projection at attained age 122, 122 policy years, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 122 + 120 = 1,584 months, `t = 0 … 1,583`, and the month after, 1,584. `av_change` and the three residuals read `t + 1` in cover alone, so nothing reads 1,585 |
| `m` | 1,465 | 1,463, the policy month from issue of the last covered month at issue age 0, wherever the valuation date falls: the funding ratio reads the pricing path at `duration_mth(t)` in cover alone |
| `t` or `m`, and `timing`, `kind` or `i` | 1,586 or 1,465, by 9 | the nine timings of the one numbering, `BEF_NB` 0 to `EOM` 8; the four kinds and five columns more; and the subaccount positions, 0 to `subaccount_max` − 1, 8. Every 2-D cache has this one width. Cython's generated unpickle code converts a space's caches of one depth with one function for each inner shape, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A kind from 4 to 8, a position past the lineup, or a timing a cell does not take is then inside the cache, where the cell refuses it as modelx does, and a code or a position from 9 raises |
| `t` or `m`, `i` and `timing` | 1,586 or 1,465, by 9 by 9 | the subaccounts' positions by the timings, in `sa_pp_at` and `sa_pricing_pp_at`. The converters are named by the inner shape, so 3-D caches of 9 by 9 build beside 2-D caches of 9, and every 3-D cache has this one inner shape |
| `i` | 9 | 8, the last position `subaccount_max` admits |
| `y` | 124 | 122, the policy year of the last covered month at issue age 0, read by the four readers by policy year inside cover alone, the pricing path's among them |
| `a` | 123 | 121, `omega_age`, the last attained age in cover, read by the two readers by age inside cover alone, from the youngest issue age, 0. Ages 0 to 17 read the tables at their first age, 18 as shipped |

`proj_len()` refuses a point issued below 0, `issue_age_min`, or above 85, `issue_age_max`,
the issue ages `product-spec.md` admits, one issued above `omega_age`, 121, and a lineup of
more than `subaccount_max`, 9, subaccounts, in modelx as compiled, and the projection ends
at attained age 122, so no report on a point the model projects runs past these caches.
`issue_age_min`, `omega_age`, `subaccount_max` and `Data.future_horizon_mth` are the
contract the sizes are derived from; `issue_age_max` sizes nothing, since every size rests
on the youngest issue age. Lower the minimum, or raise `omega_age`, the horizon or
`subaccount_max`, and a report runs past the caches in the compiled model alone: a frame of
more than 1,585 months, a pricing month past 1,464, a policy year past 123, an age past 122
or a tenth subaccount raises `IndexError`, naming nothing, where modelx projects. Each needs
the sizes derived again, as `spec_sec.py` derives them, and a rebuild: `t` raised to 12 ×
(`omega_age` − `issue_age_min` + 1) + the horizon + 2, `m` to 12 × (`omega_age` −
`issue_age_min` + 1) + 1, `y` to `omega_age` − `issue_age_min` + 3, `a` to `omega_age` + 2,
and the width and `i` to `subaccount_max`. `Data.return_horizon_mth`, 1,585, the last month
`Data`'s array of returns holds, is `t`'s last index, so that the array is no larger than
the months a frame reads, and it is raised with `t`. The shipped COI scale carries the
anchor cell alone, issue age 45, so a point at any other is refused today by its first COI
rate, naming it; an issue age of 0 is the contract's, which an extended scale reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it
was measured to change there. Here `cpow` reaches nine powers: the monthly rates of both
decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`, the monthly
fixed-option, pricing and loan rates, `(1 + i)^(1/12) − 1` in `fixed_return_mth`,
`pricing_return_mth`, `pricing_fixed_return_mth`, `loan_rate_mth` and `loan_cr_rate_mth`,
the premium persistency's `φ^(−δ)` in `prem_persistency`, and expense inflation,
`(1 + r)^(t // 12)` in `inflation_factor`. Without `cpow` a
compiler with C99's complex numbers, gcc among them, computes a power of two doubles as a
complex power, which can differ from Python's float power in its last bits. With both
directives and the flag every compiled value agrees with modelx's bit for bit, and the
compile tests hold each, by the module's first line, by the compiler's command lines and,
on x86-64, by the comparison itself. On the same platforms the tool adds
`-Werror=incompatible-pointer-types`, so that gcc before 14, which only warns of a pointer
of the wrong type, fails the build as gcc 14 does: the error two cache widths give (*The
sample and the spec*, above).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 7,797,640
bytes, about 7.8 MB, the type's basic size, which holds every cell's cache, each beside a
flag array of its shape that marks what is computed. The two 3-D caches, `sa_pp_at`'s 1,586
by 9 by 9 and `sa_pricing_pp_at`'s 1,465 by 9 by 9, are about 1.5 and 1.4 MB of it with
their flags, and the 18 2-D caches about 3.0 MB more. That is 4.1 times `UL_US_SEC`'s, for
frames of 1,586 months against 1,358, nine subaccounts by nine timings where UL has none,
and the pricing path, which UL lacks. Making one costs time as well as memory: Python zeroes
the struct when it makes the ItemSpace, and making and releasing one, nothing computed, took
0.36 to 0.40 ms here, of the 2.5 ms a compiled point takes (*Speed*, below). Deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference cycles,
and only Python's cyclic collector frees it. That is why `run_sec.py --block` collects after
each release, in its frame pass and in its projections (*Run it*, above), and a compile test
holds a compiled block run to one point's ItemSpace at a time. Without it, 504 compiled
points peaked at 3,610 MB (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no limit
raised. What it needs is stack. The deepest call the contract allows, a cold `net_cf` in the
last month of the longest cover, issue age 0, issued now or 120 months on, runs the account
value's chain back to `t_entry()`, and with the behaviour module on the pricing path's back
to issue, 1,484 cells deep in modelx, one cell a month and 21 more. Compiled with gcc, with
the module on, it runs on a thread of 352 KiB of stack and not of 344, and with it off on
344 and not 336, 232 to 243 bytes a level. A test runs it in a thread of 1 MiB, the stack
Windows gives a program's main thread unless the program is linked for more, and again on
the main thread, which is where `run_sec.py --cython` runs. MSVC's frames may be larger than
gcc's, and the `cython` CI job, which runs the test on Windows too, is the check on them:
the test first runs the call at seven stacks, from 256 KiB to 2 MiB, and reports the
smallest it ran on, so a first run there measures MSVC's need. Until it has, the need is an
estimate: at the 325 to 433 bytes a level MSVC took on `WholeLife_US_SEC`'s chain, 1,484
levels need about 471 to 628 KiB, and at 1.3 to 2.0 times gcc's frames, its ratio there, 450
to 705 KiB, inside 1 MiB by 1.45 times at the least, the thinnest margin of any model so
far. A stack below the need kills its child on an overflow, by design (with gcc, 256 KiB
does); on Windows the child ends with `STATUS_STACK_OVERFLOW`, and should Windows Error
Reporting hold it instead, the test waits a bounded time for each child rather than the
job's hour. The export recurses in Python instead: the same call needs a recursion limit of
2,994 there with the module off and 2,984 with it on, and the four reports and the three
checks, which run in ascending `t` with the module on, need 1,834, the package's import
among the frames they run under or not: a point in force reads the pricing path cold back to
issue in its first month, point 8, in force at policy month 888, the deepest. So
`sample_sec.py` sets 12,000, four times the first rounded up to the thousand, and a test
holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode, join or hold, when the array is first read, naming every
  point at fault, or the table and its lines: a `point_id` that is not a whole number; a
  `rate_class` the class factors lack, `class_factor_table.csv has no factor for the
  rate_class of point_id [2, 6]`; a `scenario_id` the return scenario lacks, or one
  without a row for a subaccount of the lineup, `scenario_table.csv has no returns for
  every subaccount of the lineup on the scenario_id of point_id [3]`; and on a point that
  `has_surr_charge`, a `surr_charge_id` the schedules lack, `surr_charge_table.csv has no
  schedule for the surr_charge_id of point_id [4], each of which has_surr_charge`.
  `VUL_US_S` fails every projection of such a point with a `KeyError`, and no projection of
  a point without a charge reads its schedule, so none is refused for it; on such a point
  whose ID the table lacks, `surr_charge_rate_max()` and `surr_charge_runoff_years()` raise
  `KeyError`, `'point_id 7: surr_charge_table.csv has no schedule for its surr_charge_id'`,
  compiled as in modelx. And, before it is cast to int64, a number of `2**53` or more in
  size, which numpy would cast to the least int64 past int64: a `point_id`, a model point's
  issue age, `model_point_table_sec.csv: age_at_entry must be below 2**53 in size; it is not
  at point_id [3]`, and a `duration_mth`, a policy issued `2**63` months on, and, on a point
  with a charge, a run-off of `2**53` years or more in size, which `VUL_US_S` projects as a
  charge that never runs off. That one is not cast without a word: `lapse_shock_month`'s
  compiled `int` is exact below `2**63` and raises `OverflowError` past it, and the run-off
  is held to the bound every number read as an int is held to. A fractional issue age stays
  refused, as at stage `E` (*The in-force interface*, above), where `UL_US_SEC`'s truncates.
  A key written as a float, a policy year `9.0`, is read by its value, as `VUL_US_S`'s
  lookups match it; a key written as text is not whole, and the table's check refuses it.
- A negative age in `corridor_factors.csv` or `mort_table.csv`, `corridor_factors.csv: age
  must be 0 or more; it is not on line [2]`, by the table's check, which every reader of
  the table asks first: each is held from age 0, so that the age is the index. A refusal
  `VUL_US_S` lacks, which reads every attained age below a table's first at that row,
  whatever the table's ages. And a corridor factor below 0, `corridor_factors.csv:
  corridor_factor must be a number, zero or more; it is not on line [2]`, as the corridor
  pin is held: one takes the death benefit past the option's amount on an account value
  below 0, every check passing.
- A key beyond a table, by the one cell that reads it, naming the point, where
  `VUL_US_S`'s lookup raised `KeyError`: a policy year below 1, `point_id 1:
  prem_persistency.csv has no factor for policy year 0`, from `prem_persistency_py`, and
  the same from `lapse_rate_base_py` and `coi_rate_guar_at`, none of which a projection
  calls outside cover; a month before a scenario's first, as on a path re-based to begin in
  a later point's issue month, `point_id 9: scenario_table.csv has no return for
  subaccount_id 1 at t 0`, from `gross_return_mth`, and a month past the horizon,
  `point_id 1: scenario_table.csv is read to return_horizon_mth, 1585, so its scenario 2,
  in the order of the ids, has no return for subaccount_id 1 at t 1586`, from the same
  cell, a call no frame makes, as on every month of a scenario that starts past it; the
  scenario is named by its number, since no projection cell reads the label
  `scenario_id()`, even to refuse; a position outside
  the lineup, `point_id 1: no subaccount at position 2 of the lineup of 2`, from `alloc`,
  `fund_expense_ann`, `sa_pp_init` and `scenario_last_mth`; and a point whose COI scale the
  table lacks, `point_id 1: coi_rates.csv has no scale for the point's sex, rate_class and
  age_at_entry`, from `coi_rate_last_year`, when its first rate is read.
- By `proj_len()`, a point issued above `omega_age`, at or past the end of the
  projection, below `issue_age_min` or above `issue_age_max`, and a lineup of more than
  `subaccount_max` subaccounts, in that order: `point_id 3: issue age 86 is above
  issue_age_max, 85`.
- A timing or a kind a cell does not take, `ValueError("invalid timing")` and
  `ValueError("invalid kind")`, where the code is inside the cell's cache: a code of the
  other family, `av_pp_at(0, BEF_NB)`, `pols_if_at(0, BEF_PREM)`, `av_at(0, BEF_MAT)`, a
  timing the pricing path lacks, `sa_pricing_pp_at(0, 0, BEF_WD)`, a kind a cell lacks,
  `claim_pp(0, MATURITY)`, `claims_from_av(0, WITHDRAWAL)`, and a code up to 8,
  `claims_from_av(0, 8)`.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1586)`, which modelx answers with 0, the month being outside cover;
`pols_if_at(0, 9)` and `claim_pp(0, 9)`, which modelx refuses as `invalid timing` and
`invalid kind`; `alloc(9)` and `sa_pp_at(0, 9, BEF_PREM)`, which modelx refuses by the
subaccount's guard; `prem_persistency_py(124)`, which modelx reads at the table's last
year, 0.80, and `prem_persistency_py(-1)`, which modelx refuses, naming the year; and
`corridor_factor_at(123)` and `corridor_factor_at(-1)`, which modelx reads at the table's
nearest row, 1.00 and 2.50; and `sa_pp(0, -1)`, a position below the lineup, which modelx
refuses by the subaccount's guard. An `idx` past the last row is refused in
both, with an `IndexError` at the first read of a vector, and `Projection[-1]` reads every
vector at its last element in both, so it is the table's last point, under that point's
own `point_id()`.

A Reference is a C variable of its value's type: `issue_age_min`, `issue_age_max`,
`subaccount_max`, `omega_age`, `charges_cease_age`, `loan_pref_year`, the codes and `idx`
a `long long`, as `Data.future_horizon_mth` is, `dyn_behavior_on` a `bint`, and the rates
and amounts a `double`. Set past that type, it is converted when it is set, where modelx
keeps the value as given. A float set on an int Reference is truncated toward zero without
a word, `omega_age = 121.7` reading 121 and `issue_age_min = 0.5` reading 0, where modelx
computes with the float: `omega_age = 121.0` makes `omega_mth()` a float there, and
`result_cf()` then fails. A text, a NaN, an infinity or an int beyond 64 bits is refused at
once, with `TypeError`, `ValueError` or `OverflowError`. An int set on a `double`
Reference reads as a float compiled, where modelx returns the int: `lapse_shock_mult = 2`
gives `lapse_rate_sc_mult` 2 in modelx and 2.0 compiled in the cliff month, where the cell
returns the Reference as it is. Each shipped Reference is a
value of its C type, so no shipped number differs. And a Reference set past its domain
computes as C computes, where modelx raises: an `inflation_rate` of `1e300` makes
`inflation_factor(24)` infinite compiled, where modelx's power raises `OverflowError`.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
best-estimate rate at 1, `min(q, 1.0)`, as `VUL_US_S` does. Uncapped, the monthly rate,
`1 − (1 − q)^(1/12)`, would be complex in modelx and NaN compiled, silently. Capped, both
compute 1. A NaN rate would stay NaN through the cap, in both, as through every other
bound, each of which the compiled model computes as a comparison that keeps the value
unless the bound is smaller, or larger: a NaN `mort_ae_factor`, set as a Reference, makes
`mort_rate(0)` and `net_cf(0)` NaN in both. `Data`'s refusals of a value outside its range
keep any NaN from reaching them through the inputs. The annual lapse rate has no cap, in
`VUL_US_S` or here (*Counts and timings*, above): past 1, the monthly rate is complex in
modelx, and the three checks raise `TypeError`; compiled it is NaN, so are the counts after
it, and the three checks return `False`. With a spike of 40, point 3's
`lapse_rate_mth(168)` is NaN compiled. No comparison of the two engines crosses that
domain.

### Speed

`python tools/bench_sec_cy.py variable_ul` builds the model into a temporary directory,
or takes a build with `--build`, and times one block run on three engines: modelx, the
export and the compiled model. Each engine runs the committed table repeated, in a process
of its own, as `run_sec.py --block` runs a block, each point projected and then released.
`net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,003 | 2.53 ms (15.21–17.02) | 3.15 ms (18.93–20.82) | 89 MB |
| export | 603 | 34.9 ms (21.02–23.26) | 32.8 ms (19.75–22.60) | 89 MB |
| modelx | 126 | 964 ms (121.5–126.6) | 1,021 ms (128.7–131.3) | 189 MB |

On `net_cf` the compiled model runs 13.8 times its export, and on `result_cf`, where
building the DataFrame takes much of its time, 10.4 times; it runs 381 and 324 times
modelx. A second run of the compiled model and the export straight after, under a 1-minute
load between 1.7 and 2.7, gave the compiled model 2.53 and 3.14 ms and the export 36.4
and 33.2 ms, 14.4 and 10.6 times. The modelx runs were made apart, one loop at a time, to
keep each under ten minutes. The compiled model takes about twice `UL_US_SEC`'s time a
point, 1.21 ms, for an ItemSpace four times the size, two subaccounts and the pricing path;
of its 2.53 ms, making and releasing the ItemSpace, which Python zeroes, takes about 0.4
ms. It runs more times its export than `UL_US_SEC`, 12.0, `Term_US_SEC`, 9.5, or
`BasicTerm_SC` on its own measure, 8.7. As it stood after running in force,
compiled the same way, the model ran no faster than its export (*What compiling changed,
and why*, above), and the compiled model runs about 110 times that build on the same
measure, 2.51 ms a point over the committed points against 279: the representation, not
the compiler, is the gain, and the export gained from it too, 35 ms a point against 279.
The release keeps a block flat: the compiled model's peak grew by less than 0.1 MB over its
6,003 points, and without the collection after each release (`--no-collect`), 504 compiled
points peaked at 3,610 MB. Reading the ten files and building every `Data` vector and
array for those points took 0.12 s, and asking every point for its frame, the runner's
first pass, 1.9 s, most of it making and releasing an ItemSpace a point.

Measured on 2026-11-13 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 0.7 and 2.7 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Each time is the fastest of three runs; under load the spread
is wide, and the fastest run is the one to compare. The comparisons over the committed
points, with the build as it stood after running in force, are the fastest of three
rounds each, in one process an engine, and so is the cost of an ItemSpace, the fastest of
five rounds of 1,000.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on point 3, issued at the
  valuation date, every cell of `VUL_US_S`'s agrees at every argument `VUL_US_S` evaluates
  in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`, whose meaning
  changed, and `subaccount_ids` and `coi_rate_scale`, a list and a Series, which this model
  replaced by the lineup's size and a schedule number, and whose values the identity
  compares through the cells that read them in every month; `VUL_US_S`'s `claims(t, None)`
  and `me_charge_pp(t, None)` are compared with the totals `claims(t)` and
  `me_charge_pp(t)`, its kinds through the `result_cf` columns `claims_death` and
  `claims_lapse`, and each of its subaccount ids at its position in the lineup. A cell this
  model lacked would fail it. The identity holds on any count,
  since `VUL_US_S` already charges acquisition on the policies issued. The same suite
  holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The in-force twins**, in `tests/test_variable_ul_us_sec.py`: points 1, 2 and 4 open
  with `VUL_US_S`'s own opening balances, the collateral at the debt and the face at
  issue, and each is `VUL_US_S`'s projection from `t = 0`, in every report and every cell
  the two share, to 1e-9 relative with no absolute floor. So the goldens
  `tests/test_variable_ul_us.py` asserts on point 1 — every row and column of the worked
  example's month, from the opening balances to the end-of-month death benefit and net
  amount at risk, to the cent — hold here at `t = 0`, the valuation month, with no number
  restated.
- **The splice**: each `VUL_US_S` point restated in force at a month either side of its
  events continues the S projection from there, in its four reports, column by column, and
  in every other cell the two share, the subaccounts, the fixed option, the loan account,
  the debt and the face at every timing among them, and the pricing path at `VUL_US_S`'s
  own policy months, to 1e-9 relative with no absolute floor. It leaves out those the twin
  identity skips, `VUL_US_S`'s own opening values and frame, and the scenario's id, since
  each row reads a copy of its own; the first default and shortfall months are asserted
  instead as the first `VUL_US_S` finds at or after the row's month, less that month. The
  months straddle the product's events: the first anniversaries, the loan's preferred
  rate, the lapse table's last year, the surrender charge's cliff and its one-month lapse
  spike, the month a shortfall begins, the attained age at which the splice's charges
  cease, the corridor's first binding and the last covered month, whose `t = 1` is the
  month the survivors are carried into. So are nine variants of S's points, in a copy of
  S's table that is never committed, each changing S's columns only and each with input
  rows of its own, for branches S's own points do not reach: withdrawals on either option,
  a single premium with no surrender charge, an Option B point funded past its face, a
  point on a second surrender-charge schedule with a loan, an issue age below the
  mortality and corridor tables' first age, each first-month pin alone, so that neither's
  flag stands in for the other's, the COI pin set above the guaranteed rate that bounds
  it, and a withdrawal larger than the account value its first premium buys, whose cut
  takes the face past 0, where it is floored. Between them they carry both sexes and every
  class, and one COI scale stops short of its cover, so that its later years are read at
  its last. `VUL_US_S`'s in-force points 1, 2 and 4, and the variants in force 24 and 60
  months, are splice cases too, at their own month 0. The References are set in both
  models to reach what the shipped values leave unreached: the behaviour module on, so
  that the pricing path, the funding ratio and the premium persistency scale are compared;
  the lapse spike at 3 times; an acquisition expense of $250; the mortality A/E at 0.56,
  which leaves survivors at the end of every frame; charges ceasing at attained age 100,
  inside every frame; and the declared rate at 2.5%, apart from the guaranteed 1.0%. The
  return scenario is a path that moves every month, and each restated or future row reads
  its own copy, re-based to its month.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch above, every opening-state
  column and every kind of valuation month, and a test asserts that they do. The other
  cases carry the `sec_full` marker and show as skipped, with the reason, unless
  `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI run runs the
  full grid too. The tests that read the splice are one class, first in the module, whose
  models are closed before the committed model and `VUL_US_S` are first read, so the
  module never holds both, and each splice row is released once it has been compared.
- **Future new business**: issued later than the valuation date, S point 3 and each
  new-business variant is the S projection moved on, cell by cell, the count at each of
  its timings among them but the count before new business in the issue month, which
  `VUL_US_S`'s cell counts as in force; with zeros before issue in every report, no
  decrement rate evaluated there, and no scenario month read before issue.
- **How it computes**: each row the splice and the future business compare is first run on
  the books, its reports, its checks and then every monthly cell at every month from
  `t_entry()` to `proj_len() − 1`, at every subaccount, timing and kind, as Phase 2's
  sweep will run it, and is then scanned, before the comparison evaluates its cells at
  `VUL_US_S`'s keys: no cell has been called at a negative month, none evaluated from
  `t_entry()` on has read a month before it, none evaluated at month `t` has read a month
  later than `t + 1`, and no cell without a month but the loops over the frame has read
  one keyed by a month. The sweep is what reaches the account value's opening balance in a
  later point's issue month, which no report reads, since the funding ratio returns there
  first. The pricing path, a projection made at issue and based there, is the one
  look-back allowed, and is held to the rest at its own policy months. On a fresh read of
  the committed model the policy clock is a closed form, every point's reports run under a
  lowered recursion limit, which a recursion backward over the frame would exceed, and no
  projection cell has read a label accessor. And every chain is called cold, on a fresh
  read, at the shipped References, with the behaviour module on and at the longest cover:
  modelx's stack trace counts no more than one cell a month back to `t_entry()`, or back
  to issue through the pricing path, and a fixed overhead, which a chain of two cells a
  month would exceed. With the module on, the twins of points 1 and 4 sweep in ascending
  `t` under a recursion limit of their policy month at the valuation date and that
  overhead, and the twin of point 3 and the row issued 25 months on under the module
  off's.
- **Counts, validation and regeneration**: the roll-forward closes, the last month
  included, `BEF_MAT` is the `BEF_DECR` count, and `pols_if_at` refuses a timing it
  does not have; `result_pols()` is `VUL_US_S`'s, column for column, with `pols_new_biz`
  beside it; multiplying `policy_count` by 2.5, with every assumption that ships at zero
  switched on, multiplies every cash flow and moves no per-policy value; each malformed
  row is refused naming its point, by its own rule, and so is a projection of it; each
  assumption table with a malformed key, a policy year below 1 among them, or a value that
  is not a number, is refused naming its file, its column and its lines, and so is one
  with a lapse or mortality rate outside 0 to 1, or a class factor, a COI rate, a fund
  expense, a premium persistency factor or a surrender charge below 0, while the bounds of
  each range are read; a `db_option`, `qual_test` or `premium_type` no decode knows raises
  `VUL_US_S`'s message; the horizon is a Reference, which at 0 refuses any future business,
  saying so, and refuses itself below 0, as the return scenario's horizon does; a point at
  or past the end of the projection is refused by `proj_len()`; the edges of the interface
  are accepted, the keys of every keyed table written as floats among them; the committed
  table is what `VUL_US_S` generates, and each of its derived and future rows projects its S
  point's reports from its month on; and the generator reads one opening column for each
  subaccount of the lineup, and every S point it issues later has both pins blank.
- **The opening state and the rest**: point 6 opens from its own collateral and its own
  subaccounts, and read as `VUL_US_S` would open it gives the numbers above; the face in
  force opens from its column; a row restated on `WE` as shipped reads the worked
  example's month at `t = 0`, and on a copy re-based to its month is `VUL_US_S`'s; expense
  inflation runs on the valuation clock, the fund returns and the declared rate are one
  number for every point in each month, each subaccount's path repeating its own last
  month, the two ending apart, and a declared rate that moves leaves the pricing path
  where it was; with a current COI scale above the guaranteed one and a declared rate
  below the guaranteed 1.0%, point 4 is `VUL_US_S`'s in every cell, every current rate the
  guaranteed one and the fixed option and the pricing path credited at the floor; a check
  whose residual is not a number fails, the NaN sent through the M&E rate, a Reference; a
  lapse rate past 1 makes every check raise, in both models; each check decides as
  `VUL_US_S`'s `math.isclose` does where its sides fall below 1, a miss inside the
  absolute tolerance passing and one outside it failing; on a point whose loan comes to
  exceed its cash value the three checks hold where `VUL_US_S`'s margin and net-view
  identities fail; acquisition falls on new business alone, per policy issued and not
  inflated; a StdTob point at an A/E of 1.0, whose product first passes 1 at attained age
  113, 1.09495, is `VUL_US_S`'s in every cell, the capped months included, as new business
  and restated in force the month before the cap, the rate there is the float 1.0 in both
  models, every life in force dies in that month and nothing is in force after it; a NaN
  that reaches the cap stays NaN, sent through the class factor's formula or the A/E, a
  Reference, and so does one that reaches a bound on the COI rate written second, the
  scale's cap, the guaranteed rate over the current one and the pin's; every monthly cell
  holds its value outside cover and reads no table there; the points of a block sum row by
  row; an extract without the generator's three columns, relabelled, projects the same
  numbers; and `run_sec.py` prints the model's numbers, for a point in force, a point
  restated, a point to be issued and the block, line by line, and sums the block as
  `groupby` does, bit for bit; and outside the repository, beside a copy of the model or
  at a path too shallow to hold one, `run_sec.py --cython` says it cannot build.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py VUL_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their call
  syntax changed: a point's position for its label, the codes for the text of a timing or
  a kind, a subaccount's position for its id, and the split cells for `claims(t, kind)`
  and `me_charge_pp(t, i)`. Each point is named by its label, in `point_id()`, in a
  refusal and in `run_sec.py`'s output.
- **What compiling changed**: the two totals are `VUL_US_S`'s bit for bit, sign of a zero
  and type included, `claims(t)` its `claims(t)` and `me_charge_pp(t)` its
  `me_charge_pp(t)`, on its points' twins in every month, and so are the kinds and each
  subaccount's charge, and with both kinds, or both subaccounts' charges, set to −0.0 in
  both models each total is 0.0, as `VUL_US_S`'s `sum` gives; a point issued below
  `issue_age_min` or above `issue_age_max`, one to be issued above `omega_age` and a
  lineup of more than `subaccount_max` subaccounts are refused by `proj_len()`, naming the
  point, and the point issued at 86, one refused under an `issue_age_min` raised to 46 and
  the lineup of ten each project once the bound is moved past it; a read beyond a table and
  a position past the lineup are refused by the cell that reads it, naming the point, and a
  point without a COI scale where its first rate is read, which projects where no rate is
  read, with charges ceasing at its issue age; the scenarios are numbered by their ids
  whatever the file's order; on a COI file of seven scales written out of their keys'
  order, each scale's lines reversed, each scale's row of the array and its last year are
  the file's, found by key, and S's four points, given four of the scales, are
  `VUL_US_S`'s in every cell; a scenario month far past every frame adds nothing to the
  array of returns, which holds the months a frame reads, and a path run past them is held
  to them, a month past the horizon refused, naming the point and the scenario's number,
  as is every month of a path that starts past it; the padding beyond each table's extent
  is NaN; each size in `spec_sec.py` is the one its comment derives from the model's
  References, and the sample's recursion limit the one its comment derives.
- **Decoding, joins and values a bound reads**: what `Data` cannot decode or join, a
  `point_id` that is not whole or past `2**53`, an issue age or a `duration_mth` past
  `2**53`, a class the class factors lack, a scenario the return scenario lacks or holds no
  row of a lineup subaccount for, a schedule the surrender charges lack or a run-off past
  `2**53` on a point with a charge, a negative age in an age table and a corridor factor
  below 0, is refused naming the points, the table or its lines, by the `Data` cell that
  first reads it and by a projection, the message naming every point at fault and no
  other; a point without a charge is not refused for its schedule, reads it where the
  table holds its ID, as at stage `E`, and raises `KeyError` where it does not; each value
  a decode or a join names, written in another case or with a space beside it, is refused
  with `VUL_US_S`'s message or the join's, as `VUL_US_S` compares it exactly; and each edge
  of each range is accepted and projects.
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
  Python object among a projection cell's locals, calls no Python builtin there, and builds
  no container, under both directives (C3); on the committed points, every cell at every
  argument a full modelx sweep caches is what modelx computes, bit for bit on x86-64, and so
  is every raise and every `Data` array (C4); and `run_sec.py --block`, run compiled, holds
  one point's ItemSpace at a time. In `tests/test_variable_ul_us_sec.py`: the same
  comparison on the splice grid, the core by default and the full grid with
  `USLIB_SEC_FULL=1`, variants included, four rows at a time; at the contract's extremes,
  the longest frames from issue age 0, the oldest issue age and the bounds of its values,
  from a COI copy written out of its keys' order, and on a lineup of nine subaccounts
  written out of their ids' order; on labels that are not text and on keys written as
  floats, where every `Data` array is first held to the dtype it has on the keys as written,
  in modelx, in seconds; and where the cap binds, and where a NaN reaches it; the compiled
  model refuses what modelx refuses, with modelx's message, on the relabelled extract too,
  and an argument past a cache raises `IndexError`; on points without a charge, the two
  schedule accessors read the stage `E` values, and raise `KeyError` on an ID the table
  lacks, as modelx does, and `Data`'s joins are modelx's arrays; past a lapse rate of 1 its
  checks return `False`; the deepest call the contract allows runs cold on a 1 MiB stack and
  on the main thread, and the test reports the smallest of seven stacks, 256 KiB to 2 MiB,
  it ran on, waiting a bounded time for each; a Reference set after the model has computed
  changes no value it has cached; and `run_sec.py --cython` prints what `run_sec.py` prints,
  and refuses a directory that holds no build. They are marked `cython`, and they skip
  without the toolchain, but in the `cython` CI job, which installs it on Linux and on
  Windows, one leg a product, a skip fails, whatever made it.

```bash
python -m pytest tests/test_variable_ul_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_variable_ul_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k "[VUL_US_SEC]"
python -m pytest tests/test_compiled_conventions.py -q -k "[VUL_US_SEC]"
python -m pytest tests/test_variable_ul_us_sec.py -q -m cython  # the compiled tests
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
