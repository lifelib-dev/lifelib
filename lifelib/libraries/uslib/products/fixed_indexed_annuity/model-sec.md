# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `FIA_US_SEC` is [`FIA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of their contract year, in deferral, in income or with their
account value exhausted, and contracts to be written in the ten years after it, as
lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is the one
[`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `FIA_US_S` on another time axis, and it reads `FIA_US_S`'s assumption tables in place,
> every assumption unchanged; its rate scenarios are `FIA_US_S`'s, moved onto the
> valuation clock. The contractual elements are sourced, the 7% premium bonus, its vesting
> and the surrender charge schedule [S5], the 5.25% cap and the 5.00%/2.00% rollup [S2]
> and the 0.95% rider charge on the benefit base [S9] among them. Every behavioural and
> expense assumption is a **[std]** standardization, the index paths included, and the
> shipped mortality table is illustrative, *not* a published basis. Replace them with
> company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/fixed_indexed_annuity/run_sec.py          # point 1, in force 84 months
python products/fixed_indexed_annuity/run_sec.py 14       # the anchor, depleted
python products/fixed_indexed_annuity/run_sec.py --block  # every point, row by row
python products/fixed_indexed_annuity/run_sec.py 14 --cython  # point 14, compiled
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about three and
a half minutes, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and
`.gitignore` covers it.

The first prints point 1, the worked example's anchor cell, in force at the valuation date
on its seventh anniversary, policy month 84, on the balances the notes state there. Its
rows `t = 0 … 11` are `FIA_US_S`'s months 84 to 95, the worked example's contract year 8,
and its row `t = 11`, the anniversary closing that year, is the worked example's month 95
number for number: an index credit of 6,720.00, the 5.25% cap on a 9.00% return on
128,000.00; the rider charge of 1,710.00 on the opening benefit base; the first lifetime
withdrawal, 10,144.16; an account value of 122,865.84; the Model #805 floor at 84,605.80;
and a benefit base of 195,080.00. Every column of its `result_cf()`, `result_pols()`,
`result_av()` and `result_glwb()` agrees with `FIA_US_S`'s months 84 to 707 but
`expenses`, which are in valuation-date dollars here, 6.67 in the first month where
`FIA_US_S` has 7.92, and `net_cf` with them. The second prints point 14, the anchor cell
issued at age 62 and valued 240 months on, in contract year 21, its account value
exhausted at the anniversary closing contract year 19: it is `DEPLETED`, with 0.468859
contracts in force, each paid 7,741.20 by the rider at the anniversary closing each
contract year, the first at `t = 11`. Three lines to the same thing for point 14:

```python
import modelx as mx
model = mx.read_model("products/fixed_indexed_annuity/FIA_US_SEC")
model.Projection[13].result_cf()     # point 14, the table's fourteenth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[13]` is point 14, and its `point_id()` says so. `result_cf()` has
`FIA_US_S`'s thirteen columns — `pols_if`, `premiums`, `withdrawals`, `wd_guar`,
`wd_excess`, `income_payments`, `claims_death`, `claims_lapse`, `claims_maturity`,
`commissions`, `expenses`, `premium_taxes` and `net_cf` — with one row per month from the
valuation date, `t = 0 … proj_len() − 1`. `withdrawals` is the total and the three columns
after it partition it, so summing every column of the frame double-counts the withdrawal, as
in `FIA_US_S`. `result_av()` has `FIA_US_S`'s values per contract on the same rows, the
account value's steps and the surrender trace, and `result_glwb()` the rider's state, with
zeros before issue; its `phase` column holds each month's phase by its label, `FIA_US_S`'s
four and `PRE_ISSUE` before issue. `result_pols()` sets out the counts behind `result_cf()`:
`pols_if`, `pols_new_biz`, the annual and monthly decrement rates, the month's deaths,
surrenders and deemed maturities, and `pols_if_aft_decr`, as in `FIA_US_S` with
`pols_new_biz` added. `result_cf_annual()` sums `result_cf()` into contract years over the
months in cover.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[idx]` and a
collection), so the run holds the cells of one point at a time: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees. It freezes everything alive
before each pass, so that each collection scans only what the pass has made since, and it
keeps the block's sum as it goes, compensated as pandas sums a `groupby`, so that the block
is, bit for bit, the frames concatenated and summed by `t`, as below. It prints the block's
first twelve rows, then the block summed into projection years.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the contract, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of cover, the close of the contract year entered at attained age 120.
- **`duration_mth(t)`, the policy clock**, counts the months the contract has been in
  force at time `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is `FIA_US_S`'s `t`, the technical
  notes' month index, and the contract runs on it, as in `FIA_US_S`: the completed
  contract years `duration(t) = duration_mth(t) // 12`, the contract year
  `policy_year(t) = duration(t) + 1`, the attained age opening that year
  `age(t) = age_at_entry() + duration(t)`, the covered age at the anniversary closing it,
  `exercise_age(t)`, and the anniversary month, where every contractual event lands, the
  one with `duration_mth(t) % 12 = 11`. `BasicTerm_SE` reaches the same numbers by adding
  one a month, a recursion as long as the frame; the closed form needs no such chain of
  calls.

The months a formula names for the anniversaries of month `t`'s contract year are months
of the frame, on the valuation clock: `anniv_mth(t) = t + 11 − duration_mth(t) % 12`
closes the year, and `year_open_mth(t) = t − 1 − duration_mth(t) % 12` is the month whose
close opened it. In `FIA_US_S` they are `12 × duration(t) + 11` and `12 × duration(t) − 1`,
policy months, which were its `t` too.

Point 1 is the anchor cell in force 84 months. At `t = 0` it opens contract year 8 at
attained age 69; the anniversary closing that year, policy month 95, is `t = 11`, where it
takes its first lifetime withdrawal at exercise age 70; its account value runs out at
`t = 143`, the anniversary closing contract year 19, and its frame has 624 rows,
`t = 0 … 623`. Point 11 is the same contract valued at policy month 95: month 0 is itself
the anniversary month, `anniv_mth(0) = 0`, and the year it closes opened at
`year_open_mth(0) = −12`, before the valuation date, so the year's opening values come
from the row. Point 12, the joint-life point valued at policy month 150, is mid-year in
contract year 13: its anniversary falls at `t = 5`, and its year opened at `t = −7`. Point
18 is the anchor cell to be issued 15 months after the valuation date:
`duration_mth(0) = −15` and `policy_year(0) = −1`, it is on the books from
`t_entry() = 15`, rows 0 to 14 are zeros, its premium of 100,000 falls at `t = 15`, and
its frame has 723 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the surrender charge and the bonus vesting, by contract year; the rollup schedule, by contract year, and the twenty-year growth window; the MVA term, in months to the end of the ten-year charge period; the step-up, the first exercise and every other annual event, in the anniversary month; the withdrawal programme, whose `t` in `withdrawal_table.csv` counts elapsed contract years; the payout bands, at the exercise age; mortality, at the attained age; the base lapse and the shock-lapse year; the end of cover, at the close of the contract year entered at age 120 | the rate scenario, the index level and the MVA reference yield, whose `t` in `rate_scenario_sec.csv` is a valuation month; expense inflation, `inflation_factor(t) = 1.025^(t/12)` |

The rate scenario is a path in calendar time, shared by every contract of a block, so it
moves to `t`. `FIA_US_S` keys its scenarios' levels by anniversary number from issue, the
`t` of `rate_scenario.csv`, so each of its contracts reads the path from its own issue. Here
a contract reads anniversary `y`'s level at the valuation month that anniversary falls in,
`m = 12y − duration_mth_init()`, the last row of its scenario at or before `m`, through
`scenario_value(y, name)`. `FIA_US_S`'s `worked` scenario steps from 5,000 to 5,450 at
anniversary 8, and `FIA_US_S` gives each contract the step at its own anniversary 8: for
point 2, issued at the valuation date, that is `t = 96`, and for point 1, in force at policy
month 84, `t = 12`, so no one path keyed by valuation month reproduces both. So
`rate_scenario_sec.csv`, which the generator writes from `FIA_US_S`'s scenarios, holds each
of them under its own id at `t = 12y`, which the points issued at the valuation date read,
and, for every row valued in force or issued later, a copy of its scenario under an id of
its own: `worked-M84` for points 1, 3 and 7, `growth-M60` for point 10 and so on, and
`worked-F15` for point 18, 91 rows in twelve scenarios. In the copy for a row valued at
policy month `d` the levels `FIA_US_S` set before `d` collapse to the one in force at `d`,
at `t = 0`, and the later rows move `d` months earlier; the copy for a row issued `k` months
on moves `k` months later and sets no level before its issue month. So every row reads each
anniversary's level at the month its own anniversary falls in, and the model reproduces
`FIA_US_S` at every anniversary. The copies are what reproduce `FIA_US_S`'s contracts, each
on the path from its own issue; the contracts of a block valued at one date would read one
path, the index as it moves from the valuation date, each at its own anniversaries.

`FIA_US_S` reads an anniversary before its scenario's first row at the first row's level.
Here no cell asks for one before the point's first month on the books: the level at the
anniversary that opened the year under way, where that anniversary precedes the valuation
date, is history, which a path read from the valuation date on cannot give, and it is the
model point's `index_level_prev_anniv_init` (below). A point whose scenario sets no level by
its first month on the books, `t = 0` or its issue month if later, is refused as the table
is read, and `scenario_value` raises, naming the point, behind that refusal.

Expense inflation keeps `FIA_US_S`'s formula, `1.025^(t/12)`, on `t`, so the maintenance
expense, $80 a contract a year, is in valuation-date dollars for every point alike: 6.67 a
month at `t = 0`. `FIA_US_S` inflates from issue, so its in-force points, entered at policy
month 84, carry `1.025^7`, 7.92 a month at entry. Acquisition, 6.0% of the premium, is
charged per contract issued, in the issue month and not inflated, as in
`basiclife/BasicTerm_SE`, and so are the commission and the premium tax, both 0 as shipped,
on the premium of the contracts issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf()
          for i in range(len(model.Data.model_point_table()))]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`FIA_US_S` computes, whatever the point's count: `FIA_US_S` already takes the premium and
charges acquisition on the contracts in force at its `t = 0`, which on new business are the
contracts issued. On `FIA_US_S`'s six new-business points every cash flow, every count and
every value per contract agrees, and so does every other cell the two models share, the
phases compared as their codes, but those whose meaning changed: `pols_if_init()`, now the
count already in force at the valuation date, 0 for new business; `model_point()`, a row of
another table; `av_pp_init()`, `av_fixed_pp_init()`, `benefit_base_pp_init()`,
`rollup_base_pp_init()` and `mgsv_pp_init()`, now the opening state of a contract in force,
0 on new business, whose issue values are credited in the issue month instead; and
`result_pols()`, which gains `pols_new_biz`. `FIA_US_S`'s `entry_year()`, `entry_mth()`,
`phase_init()` and `payout_rate_init()` are gone. `FIA_US_S`'s three in-force points,
1, 3 and 7, continue `FIA_US_S`'s projection from policy month 84, every count, cash flow
and value per contract `FIA_US_S`'s but the maintenance expense, and `net_cf` with it, so
the worked example's goldens, which all sit on point 1 at policy month 95, hold here at
`t = 11`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `FIA_US_S`'s columns,
`entry_year` apart and eight of them renamed, and fourteen of its columns are the in-force
interface: `basiclife/BasicTerm_SE`'s two, and twelve that open an in-force contract's
state. Each of the fourteen is a number, and every amount is per contract.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the contract's age in months: positive in force, in any month of its contract year, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value, the fixed account included; 0 in `DEPLETED` |
| `av_fixed_pp_init` | dollars | the start of month 0 | the fixed account, the part of the account value outside the index segment |
| `benefit_base_pp_init` | dollars | the start of month 0, which for a base flat between anniversaries is also the anniversary on or before the valuation date | the GLWB benefit base [S9], notional; 0 without the rider |
| `rollup_base_pp_init` | dollars | likewise | the base the guaranteed simple rollup is computed on [S2]; 0 without the rider |
| `lw_pp_init` | dollars | likewise | the lifetime withdrawal amount, the income in force; 0 before the first exercise |
| `mgsv_pp_init` | dollars | the start of month 0 | the Model #805 floor [R2], the notes' `MGV` |
| `wd_cum_pp_init` | dollars | the start of month 0 | the gross withdrawals taken from issue to the valuation date |
| `av_pp_prev_anniv_init` | dollars | the anniversary on or before the valuation date, the one that opened the contract year under way: the close of policy month `12 × duration(0) − 1` | the account value there, the notes' `AV(0)` of the year: the base of the year's free withdrawal and, through its indexed part, of its index credit |
| `av_fixed_pp_prev_anniv_init` | dollars | that anniversary | the fixed account there, `F(0)` of the year: the base of the year's annual fixed interest, which the stack reads, and the part of `AV(0)` outside the year's index segment |
| `phase_prev_anniv_init` | an int code | that anniversary | the phase the year opened in: 1 `ACCUM`, 2 `INCOME` or 3 `DEPLETED` on a contract in force, 0 on one not yet in force |
| `payout_rate_locked_prev_anniv_init` | a fraction of the benefit base | that anniversary | the lifetime withdrawal percentage of the age bands [S3], locked at the first exercise **[std]**, 0 before it |
| `index_level_prev_anniv_init` | index points | that anniversary | the index level at which the year's point-to-point segment started, the base of its return |

On a point issued at or after the valuation date every one of the twelve is 0, the phase
code included: such a contract opens with nothing, and its issue values arrive in its issue
month. In the first contract year, `duration_mth` 1 to 11, the year opened at issue, so the
anniversary's account value is the issue value, `premium × (1 + bonus_rate)`, its fixed
account `(1 − alloc_indexed)` of that, the benefit and rollup bases the premium under the
rider, the phase `ACCUM` and the withdrawals to date 0. On a point valued on an anniversary,
`duration_mth` a positive multiple of 12, the anniversary that opened the year is the
valuation date itself: the account value and the fixed account there are those entering
month 0, and the index level there is the one the scenario sets at `t = 0`, which the model
reads instead. `prev_anniv` is the anniversary that **opened** the contract year: an extract
that fills the anniversary columns from the anniversary after the valuation date is a year
out.

The phase is an int code, named by a `Projection` Reference of its label, so that every
comparison of a phase is a comparison of numbers. `result_glwb()` reports the label:

| Code | Reference and label | The phase |
|---|---|---|
| 0 | `PRE_ISSUE` | before issue, `duration_mth(t) < 0`; the column's code on a contract not yet in force |
| 1 | `ACCUM` | deferral, before the first lifetime withdrawal |
| 2 | `INCOME` | from the first lifetime withdrawal, while an account value remains |
| 3 | `DEPLETED` | the account value exhausted by guaranteed withdrawals and rider charges, the rider paying `LW` for life |
| 4 | `TERMINATED` | the account value exhausted by an excess withdrawal, a charge or a negative MVA, or in `ACCUM`, or the benefit base taken to 0: a deemed surrender of every contract, so never the phase of a contract in force |
| 5 | `MATURED` | from the end of cover, `t ≥ proj_len()`, outside every frame |

Each column is read where the contract needs it, and only there:

- `av_pp_init`, `av_fixed_pp_init`, `mgsv_pp_init` and `wd_cum_pp_init` open the account
  value's, the fixed account's, the floor's and the withdrawals' monthly chains at
  `t_entry()`, on a point in force.
- `benefit_base_pp_init`, `rollup_base_pp_init` and `lw_pp_init` open the contract year
  under way where it opened before the valuation date: the base the year's rollup and stack
  build on and its rider charge is taken on, the base its rollup is computed on, and the
  amount carried to the next anniversary, the floor of that anniversary's ratchet.
- `av_pp_prev_anniv_init` and `av_fixed_pp_prev_anniv_init` are the year under way's
  `AV(0)` and `F(0)` where it opened before the valuation date, read by `av_pp_year_open`
  and `av_fixed_pp_year_open`: the free withdrawal is 10% of the first, the index credit
  is on their difference and the stack's annual fixed interest on the second.
- `phase_prev_anniv_init` is the phase the year under way's annual steps are processed
  under, read by `phase_year_open`, unless the year is the exercise year, when the phase is
  `INCOME`; it decides the exercise and the growth window too.
- `payout_rate_locked_prev_anniv_init` is the percentage `payout_rate_locked` carries
  through the year under way, unless it is the exercise year.
- `index_level_prev_anniv_init` is the level `index_level` returns for the anniversary that
  opened the year under way on a contract valued mid-year. On an anniversary the scenario
  gives that level at `t = 0`, and the column is carried unread.

Everything else the projection uses is fixed at issue, in `FIA_US_S`'s columns, or follows
from the policy clock. The rider's status needs no column: a contract in force with the
rider elected has the rider alive (below).

| `FIA_US_S` | `FIA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `entry_year`, whole years: 7 on points 1, 3 and 7 | `duration_mth`, months: 84 | `FIA_US_S` enters a contract in force on an anniversary only, after `entry_year` completed contract years, opening its frame there; months reach any month of the year, and 0 or less is new business |
| `av_initial` | `av_pp_init` | Renamed after the cell it opens. Where the column is blank, `FIA_US_S`'s `av_pp_init()` computes the issue value `P (1 + b)` [S5]; the rule is kept, crediting the issue month (`prem_to_av_pp`), and the cell reads the account value in force |
| — | `av_fixed_pp_init` | `FIA_US_S` splits the account value at entry by the allocation at issue, `alloc_fixed × AV`, which holds at issue only (below) |
| `bb_initial` | `benefit_base_pp_init` | Renamed; the issue value, `P` under the rider [S9], opens the first contract year in `benefit_base_pp_at` |
| `rb_initial` | `rollup_base_pp_init` | Renamed; the issue value, `P` under the rider, opens the first contract year in the new `rollup_base_pp_year_open` |
| `mgv_initial` | `mgsv_pp_init` | Renamed after the chassis name of the floor, which the model uses throughout; its issue value, 87.5% of the premium, the bonus excluded [S10] [R2], is credited in the issue month (the new `prem_to_mgsv_pp`) |
| `lw_initial` | `lw_pp_init` | Renamed |
| `phase_initial`, text | `phase_prev_anniv_init`, an int code | The phase as a code (above), named for the instant it holds at: a phase changes only at an anniversary |
| `payout_rate_initial` | `payout_rate_locked_prev_anniv_init` | Renamed after `payout_rate_locked`, at the anniversary, where a lock happens |
| — | `av_pp_prev_anniv_init`, `av_fixed_pp_prev_anniv_init` | `FIA_US_S` values a contract in force on an anniversary only, where the year opens on the values entering its first month |
| — | `index_level_prev_anniv_init` | `FIA_US_S` reads every anniversary's level from its scenario, keyed from issue |
| — | `wd_cum_pp_init` | `FIA_US_S` counts the withdrawals to date from the month it enters a contract, from 0 |

A column measured entering month 0 is the cell it opens with `_init` added; a value at the
anniversary on or before the valuation date adds `_prev_anniv_init` instead. The benefit
base, the rollup base and the lifetime withdrawal are flat between anniversaries, so the
value entering month 0 is the one at that anniversary, and one column each serves; the
phase and the locked percentage change only at an anniversary, and their one column is
named for it.

On twins 2, 4, 5, 6, 8 and 9 the twelve are 0, the state of a contract entering its issue
month, and each takes its issue values in month 0, as its `FIA_US_S` row does. Twins 1, 3
and 7 are `FIA_US_S`'s in-force points, and they carry `FIA_US_S`'s columns, with what
`FIA_US_S` itself assumes for the columns it has none for: the fixed account
`alloc_fixed × AV`, 0 on all three, which are wholly indexed; the anniversary values equal
to the entering ones, since `FIA_US_S` enters them on anniversary 7; no withdrawals to date;
and the index level of anniversary 7, 5,000.

The columns carried over are read as `FIA_US_S` reads them. For a contract in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry`, `joint_age` | years, age nearest birthday; `joint_age` blank on a single life | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `tax_status` | codes, as in `FIA_US_S`'s table | issue |
| `premium` | dollars, the single premium | issue |
| `bonus_rate`, `alloc_indexed` | fractions: of the premium, credited to the account value; of the account value, allocated to the indexed account | issue |
| `glwb_elected` | a flag, `True` or `False` | issue |
| `glwb_basis`, `credit_method`, `rollup_id` | codes and a key into `rollup_table.csv`, as in `FIA_US_S`'s table | issue: the contract's provisions |
| `cap_rate`, `stack_factor`, `av_int_factor` | a rate a year; multiples of the credit | issue: the declared cap, held level **[std]**, the stacking factor on the benefit base and the share of the index credit reaching the account value |
| `mva_ref_yield_at_issue` | a rate a year | issue: the MVA's `i0` |
| `income_start_age`, `utilization_intensity` | an attained age; a fraction of `LW` | assumptions of the base run: the age at which it exercises, and how much of `LW` it takes |
| `scenario_id`, `wd_schedule_id` | keys into `rate_scenario_sec.csv` and `withdrawal_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `FIA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the fourteen in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `age_at_entry` and `income_start_age` are whole numbers of years, and `joint_age` is
  blank or a whole number of years, 0 or more: `FIA_US_S` reads each by `int()`, which
  would truncate a fraction without a word;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than cover
  from issue plus ten years: 1,092 months at issue age 40, the youngest the product issues
  and the shipped mortality table carries. Set to 0, the Reference refuses future new
  business altogether, and says so; a negative horizon is itself refused;
- `glwb_elected` is `True` or `False`, read by value: one cell written as text turns the
  column to text as pandas reads it, and that cell alone is refused, where `FIA_US_S`'s
  `bool()` would read every cell of such a column as elected, `"False"` among them;
- the premium, the bonus rate, the utilization, the cap, the stacking factor and the share
  of the index credit reaching the account value are each a finite number, zero or more;
  `alloc_indexed` is a number from 0 to 1; and `mva_ref_yield_at_issue` is a finite number
  above −1, the base of the MVA's power;
- the nine amounts of the opening state are each a finite number, zero or more; the locked
  percentage is a number from 0 to 1; the index level is a finite number, zero or more; and
  the phase code is a whole number;
- a contract not yet in force, `duration_mth` 0 or less, has an opening state of zeros,
  the phase code included;
- a contract in force is in phase 1, 2 or 3: `TERMINATED` is a deemed surrender of every
  contract, so none is in force in it;
- its index level is above 0, since the year's return divides by it;
- it is in `INCOME` or `DEPLETED` only under the rider: income starts only there;
- without the rider, its benefit base, rollup base, lifetime withdrawal and locked
  percentage are 0;
- under the rider, its benefit base is above 0: an anniversary that takes the base to 0
  terminates the contract;
- in `ACCUM` its lifetime withdrawal and locked percentage are 0, and in `INCOME` or
  `DEPLETED` its lifetime withdrawal is 0 exactly where its locked percentage is: the
  withdrawal is the locked percentage of a benefit base above 0, and a reduction that took
  it to 0 would have taken the base with it. A percentage of 0 is what a contract locks
  that exercised below the first age band, as it can where `min_income_age` is below the
  band's first age, both 50 as shipped, or in a band at 0%, which `payout_rate_table.csv`
  may hold. Its withdrawal is then 0 for life, in `INCOME` and, once the account value is
  exhausted, in `DEPLETED`, so `INCOME` or `DEPLETED` with both at 0 is read;
- in `DEPLETED` the account value and the fixed account, entering month 0 and at the
  anniversary, are 0, and in `ACCUM` or `INCOME` the account value at the anniversary is
  above 0: the anniversary that exhausts the account value leaves both phases;
- the fixed account does not exceed the account value it is part of, at either instant, by
  more than a cent;
- in the first contract year the values at the anniversary are the issue values, to a
  cent: the account value `premium × (1 + bonus_rate)`, the fixed account
  `(1 − alloc_indexed)` of it, the benefit and rollup bases the premium under the rider and
  0 without it, and the withdrawals to date 0; and the phase is `ACCUM`;
- on a point valued on an anniversary, the account value and the fixed account at the
  anniversary equal those entering month 0, exactly: the two instants are one;
- off an anniversary, the indexed account, `av_pp_init − av_fixed_pp_init`, equals its
  value at the anniversary to three cents, since it moves only at an anniversary, and the
  fixed account entering month 0 is not below its value at the anniversary by more than a
  cent, since between anniversaries it only accrues;
- last, each point's keys into the tables it is joined with: its `scenario_id` is a
  scenario of `rate_scenario_sec.csv` that sets its levels by the first month the point is
  on the books, `t = 0` or its issue month if later; on a point valued on an anniversary,
  the index level at the anniversary is the one its scenario sets at `t = 0`, exactly,
  since the model reads the scenario there and not the column; its `rollup_id` is a
  schedule of `rollup_table.csv`; its `wd_schedule_id` is a programme of
  `withdrawal_table.csv`; and `mort_table.csv` gives a rate at its `sex` and its attained
  age in that first month. So reading the model point table reads those four tables,
  checked. `FIA_US_S` meets a key its table lacks only as it projects: a missing scenario,
  rollup schedule, sex or age raises Python's own `KeyError`, naming no file, and a missing
  withdrawal programme takes no withdrawal, without a word.

Amounts of money are compared to a cent, so that an extract may carry each to the cent, as
an administration system holds it: each amount so carried is within half a cent of its
exact value. The indexed account is compared to three cents, being the difference of two
such amounts at each of two instants, and so missing by up to two cents: one 2.9 cents off
is read, one 3.1 cents off refused. Two columns that hold one amount at instants that
coincide, on an anniversary, are compared exactly. The generated rows carry `FIA_US_S`'s
own values, unrounded.

The checks tie the phase to the balances. A lifetime withdrawal or a locked percentage above
0 makes it `INCOME`, with an account value at the anniversary, or `DEPLETED`, without one.
Both at 0 make it `ACCUM` or `INCOME` with an account value at the anniversary, and
`DEPLETED` without one; in either income phase the contract locked 0, below the first age
band or in a band at 0%. So the column can be wrong alone only between `ACCUM` and `INCOME`
with both at 0, which the opening state does not tell apart.

Accepted, because a contract can be in each state: an account value of 0 in `DEPLETED`,
where the rider pays on; a lifetime withdrawal and a locked percentage of 0 in `INCOME` or
`DEPLETED`, where the contract exercised below the first age band or in a band at 0%; a
blank `joint_age` on the joint basis, which reads the annuitant's own age; and a
`duration_mth`, an age or a phase code written as a float, read as the whole number it
holds.

Left to the projection, because it needs `maturity_age`, a `Projection` Reference, which
`Data` cannot read: whether a point is still in cover. `proj_len()` refuses a point at or
past maturity at the valuation date, `duration_mth ≥ 12 × (121 − age_at_entry)` at the
shipped `maturity_age`, naming it, and a point whose cover from issue is empty, issued past
`maturity_age`, which would otherwise project a frame of zeros. On the shipped tables the
mortality check refuses an attained age past 120 first, the table's last. So a loop over
the block meets such a row only when it reaches it, after projecting the points before it,
and `run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything. The index level at an anniversary before the valuation date is
history, which nothing here can check beyond its being above 0.

Five of the six assumption tables are `FIA_US_S`'s files, read in place, and the sixth is
the generated `rate_scenario_sec.csv`. All six are read by `FIA_US_S`'s readers, and their
keys and values are checked as well. Beside each reader a `Data` cell reads the
table's keys by value, once, checks them and the table's values, and returns the table
indexed by the checked keys, and the projection reads the table there and nowhere else:
`mort_rates`, `surr_charge_scale`, `rollup_steps`, `payout_rates`, which expands the
payout bands to one row an age, `rate_scenario_steps` and `wd_schedules`. The surrender
table's last year and the payout bands' first and last ages, which bound the reads, are int
cells taken from the same checked keys. A key written `1.0` is 1, as `FIA_US_S`'s lookups
match it. A key that is not a whole number, text and a blank among them, a blank text key,
a value that is not a number in its range, blank, text and infinite values among them, a
repeated key, and, where the projection reads every year or age between a table's first and
last, keys that leave a gap, payout bands that overlap among them, are refused, naming the
file and the lines, before a projection reads a value from the table: the message names
each repeated key with its lines, each key or span of keys missing and each payout band
that ends below its start, every fault in one message. A rollup schedule is
a step function, so its years need not run one a year, and a scenario may start after
`t = 0`, for business issued later, so the month it must start by is the point's, which the
model point table's checks hold. `FIA_US_S` takes the keys as pandas reads them: one written
as text turns its whole column to text, so that every withdrawal is then zero without a
word, and every other lookup on the column raises Python's own `TypeError`, `KeyError` or
`ValueError`, naming no file; and an age in a gap between two payout bands reads 0. Every
value a cap, a `min` or a `max` reads is refused blank, as text or infinite, since `min`
and `max` lose a NaN in a later argument without a word.

## The model points

No row of `model_point_table_sec.csv` or `rate_scenario_sec.csv` is typed by hand. Every
one is generated from `FIA_US_S` and its inputs by `tests/sec_support.py`, from the
`FIA_US_SEC` entry in its `SEC_SPECS`, and the tests regenerate both files and compare, so
an edit to a `FIA_US_S` row or scenario reaches them or fails the suite. In the source
repository, `python tools/gen_sec_points.py FIA_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 3, 7 | twin | S points 1, 3 and 7, in force at S month 84 | `FIA_US_S`'s three in-force contracts, on their seventh anniversary, on the balances the notes state there: the worked example; the notes' "Where the step-up binds" block, on the 3% simple rollup; and the anchor overdrawing at 105% of the maximum |
| 2, 4, 5, 6, 8, 9 | twin | S points 2, 4, 5, 6, 8 and 9 | issued at `t = 0`: the anchor; pure stacking, with the only fixed allocation, 20%, credited at a participation rate under a cap; joint life; no rider; a $60,000 withdrawal at anniversary 3, before exercise; and income deferred to attained age 85 |
| 10 | derived | S point 4 at S month 60 | pure stacking in `ACCUM` on its fifth anniversary, its fixed account 18,075.55 of an account value of 112,735.43 |
| 11 | derived | S point 1 at S month 95 | the anchor valued in the last month of contract year 8, the month of the anniversary that takes its first lifetime withdrawal: its row `t = 0` is the worked example's anniversary 8 again, on the year's opening values from its row |
| 12 | derived | S point 5 at S month 150 | joint life in `INCOME`, mid-year in contract year 13: the phase, the locked 4.70% and the index level of 2,015.71 that opened the year come from its row |
| 13 | derived | S point 7 at S month 216 | the overdrawing anchor in contract year 19, its account value down to 2,132.92: at `t = 11` its excess withdrawal exhausts it, and the contract terminates |
| 14 | derived | S point 2 at S month 240 | the anchor in contract year 21, `DEPLETED`: an account value of 0 and income of 7,741.20 a year paid by the rider |
| 15 | derived | S point 8 at S month 6 | the pre-exercise point in its first policy year, the year's opening values its issue values |
| 16 | derived | S point 6 at S month 696 | the no-rider point in its last policy year, entered at attained age 120, where mortality is 1: a 12-row frame |
| 17 | derived | S point 4 at S month 100 | pure stacking in `INCOME`, mid-year in contract year 9, its fixed account accrued since the anniversary, 13,668.09 against 13,564.88 there |
| 18 | future | S point 2, 15 months on | to be issued at `t = 15` |

A derived row's `policy_count` is the count `FIA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `FIA_US_S` carries into it, each column read as
`FIA_US_S`'s own formulas read it: the account value, the fixed account, the benefit base,
the rollup base, the lifetime withdrawal, the floor and the withdrawals to date at the
close of S month `d − 1`; the account value and the fixed account opening the contract year
of `d`, S's `av_pp_year_open(d)` and `av_fixed_pp_year_open(d)`; the phase and the locked
percentage closing S month `12 × duration(d) − 1`, the anniversary that opened that year,
or S's own at issue in the first year; and the index level there, S's
`index_level(duration(d))`. So the row continues the S projection from there: point 10
opens with 0.861548 contracts, point 11 with 0.964118, point 12 with 0.618921, point 14
with 0.468859 and point 16 with 4.554486e−13. Its `policy_id` is the S row's with the
month appended, `FIA-000004-M60`, and so is its scenario's id, `growth-M60`; a future
row's ids carry the months to issue, `FIA-000002-F15` and `worked-F15`. Row `t` of a
generated point is month `t + source_mth` of its S point.
Unlike `MYGA_US_SEC`'s, the table holds no row in a last covered month: at the shipped
mortality, 1.0 at age 120, `FIA_US_S`'s count is 0 from the second month of the contract
year entered at 120, so such a row would project zeros. Point 16, in that year's first
month, is the row that shows the year, and the tests reach its last month on a copy of the
mortality table cut below 1 at 120. All eighteen are the anchor configuration's male 62,
non-qualified, $100,000 single-premium contract with the 7% bonus, as every `FIA_US_S`
point is; the shipped mortality table starts at attained age 40, the youngest issue age
the product allows.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order, each an int code named as `FIA_US_S`'s text
(*The compiled model*, below):

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_MORT`, the same count, this product having no annuitization decrement;
- `BEF_LAPSE`, after the month's deaths;
- `AFT_DECR`, after its surrenders, the count at the end of the month.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `FIA_US_S`'s, unchanged
but for their guard outside cover. `BEF_DECR` already meant in `FIA_US_S` what it means in
`BasicTerm_SE`, so no name clashes, and `BEF_NB` is the one timing running in force adds.
Any other timing raises. `BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a month
before its maturities, is not adopted: the contracts here leave at the end of the last
covered month, as `pols_maturity`, where `FIA_US_S`'s goldens put the horizon.

The survivors carried into month `t` are those of month `t − 1`'s `BEF_DECR` count, which
`BEF_NB` forms itself, as its own value at `t − 1` plus that month's new business, through
the month's deaths and surrenders in the order `AFT_DECR` takes them. So
`pols_if_at(t, AFT_DECR)` is `pols_if_at(t + 1, BEF_NB)` in every month but the last
covered one, where the deemed maturity empties the block. Both decrements are monthly
rates converted from the annual ones, `1 − (1 − q)^(1/12)`, so that every anniversary count
is the annual grid's; the deemed full surrender on termination falls whole in its
anniversary month, as in `FIA_US_S`.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `FIA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `FIA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing account value, `av_at(t, EOY)`, is weighted
by `pols_if_at(t + 1, BEF_NB)`. Both roll-forward checks are loops over the frame that
scale their tolerance with `policy_count`, since a residual is rounding on that many
contracts: `FIA_US_S`'s 1e-6 for the account value and 1e-12 for the count, on a point
counting one contract. Each fails at the first month whose residual is not within its
tolerance, so a residual that is not a number fails, as `FIA_US_S`'s `math.isclose` fails
it. The count's residual is 0 outside cover before it reads `t + 1`, so that at
`t = proj_len()` nothing reads a month past the frame.

The premium, the premium bonus, the commission, acquisition and the premium tax fall on
`pols_new_biz(t)`, in the issue month: `t = 0` on the twins issued at the valuation date,
`t = 15` on point 18, and never on a point already in force, which paid its premium before
the valuation date. `FIA_US_S` puts them at `t = 0` on `pols_if_init()`, the contracts
issued, so on a twin they are the same at any count.

Every chain runs one cell a month back to `t_entry()`: the count, through `BEF_NB`; the
account value, `av_pp`, and the fixed account, `av_fixed_pp`, each with its opening written
inline, where `FIA_US_S`'s each ran through two cells a month, the balance and its `_at`
cell; the floor, `mgsv_pp`; and the withdrawals to date, `wd_cum_pp`. The values of the year
— the benefit base, the rollup base, the lifetime withdrawal, the phase, the locked
percentage and the rider's state — step once a year, each reading its value at the
anniversary that opened the year, `year_open_mth(t)`, in the frame. A cold `net_cf` in the
last month runs one cell a month back to `t_entry()` and at most 10 more on the committed
points: 715 cells deep on a 708-month frame, against 1,420 in `FIA_US_S`, and 631 on point
1's 624 months, against 1,252. At issue age 40, the contract's longest cover from issue, 972
months, it runs 979 deep, and a point issued 120 months on runs no deeper, because its
chains stop at its issue month. A cold count alone, `pols_if`, runs up to 25 more than its
months: its first month's lapse rate reads the phase closing that contract year, up to 11
months on (below), which opens the account value's chain beneath it; 997 at issue age 40.
Each report evaluates its columns in ascending `t`, and a sweep of the committed points that
way reaches a depth of 370 cells, on point 9, as `FIA_US_S`'s sweep of its point 9 does:
the floor is first read deep in the frame, at the anniversary the account value
runs out, policy month 359, whose depletion test reads the withdrawal's MVA, and the MVA's
collar reads the floor, whose chain then runs back to the books' first month. So the tests
sweep the committed points under a recursion limit of 400, which a recursion backward over
the frame would exceed.

One read reaches ahead of its month, and only one kind. The annual surrender rate is a
property of the contract year, evaluated on the state closing it: `lapse_rate(t)` reads the
phase opening and closing the year at `anniv_mth(t)`, and `lapse_moneyness_factor(t)` the
account value and the benefit base there, up to 11 months after `t`. That anniversary lies
inside the frame, since cover ends at the close of a contract year, and the state read there
depends on no count and on nothing after it, so the read opens no chain past it. Every
other read goes no further than `t + 1`: the block's closing account value, weighted by
the next month's count, and the count's roll-forward, which reads that count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()` is `FIA_US_S`'s frame from issue, the close of the
contract year entered at `maturity_age`, 120: 708 months at issue age 62. Outside it, before
issue and from the end of cover on, every count is zero, and so every cash flow and every
value per contract; every flag is `False`; the phase is `PRE_ISSUE` before issue and
`MATURED` after cover; and the moneyness factor is 1.0, no adjustment. No count evaluates a
decrement rate there, and no table is read at a contract year or an attained age the
contract does not have: the index return, the credit rate, the surrender charge and the
vesting, the rollup rate, the step-up, the scheduled withdrawal, the MVA term, mortality,
the shock and base lapse and the moneyness factor, which `FIA_US_S` leaves unguarded, are
zero, false or, for the moneyness factor, 1.0 outside cover, before any table or rate is
read.

## The opening state

`FIA_US_S` projects its new-business points from issue, on the premium and the issue rules
the notes state, and enters its in-force points on an anniversary, on the balances the
notes state there. A contract valued in any month of its life needs all twelve state
columns, each what `FIA_US_S` carries into that month. Each shows on a committed row:

- **`av_pp_init`** opens the account value. Point 1 carries the 128,000.00 the notes state
  at anniversary 7, and so does `av_pp_prev_anniv_init`, `Data` holding the two equal on an
  anniversary. With both halved to 64,000.00, the index credit at `t = 11` is 3,360.00
  rather than 6,720.00, the stack 5,040.00 rather than 10,080.00, the first lifetime
  withdrawal 9,882.08 rather than 10,144.16, and the account value runs out at `t = 71`
  rather than `t = 143`.
- **`av_fixed_pp_init`** opens the fixed account. Point 10, the pure-stacking point with
  20% in the fixed account at issue, carries 18,075.55 of its account value of 112,735.43
  at its fifth anniversary: the fixed account takes the rider charge first, so after issue
  it falls behind its 20%. `FIA_US_S` enters a contract in force with `alloc_fixed × AV`,
  which here would be 22,547.09. With that in both fixed-account columns the year's fixed
  interest at `t = 11` is 518.58 rather than 415.74, the stack 1,296.46 rather than
  1,039.34, and the first lifetime withdrawal, at `t = 35`, 9,432.20 rather than 9,459.58;
  no later withdrawal is further apart.
- **`av_pp_prev_anniv_init`** and **`av_fixed_pp_prev_anniv_init`** are the year under way's
  opening account value and fixed account, where it opened before the valuation date.
  Point 17, valued four months into contract year 9, carries 105,550.67 and 13,564.88 at
  the anniversary that opened it, against 105,653.88 and 13,668.09 entering month 0: the
  fixed account has accrued 103.21 since, and the indexed account, 91,985.79, has not
  moved. The year's free withdrawal is 10% of the first, 10,555.07; its index credit, at
  `t = 7`, is 6%, the cap, on their difference, 5,519.15, of which the account value takes
  half; and its fixed interest for the year is 2.30% of the second, 311.99.
- **`benefit_base_pp_init`** is what five years of 250% stacking made of point 10's
  premium: 151,125.86, on which its rider charge at `t = 11` is 1,435.70. Its first
  lifetime withdrawal, at `t = 35`, is 5.20% of the base then, 181,914.98: 9,459.58.
  Carried at the premium, 100,000.00, the charge would be 950.00 and the withdrawal
  7,385.52.
- **`rollup_base_pp_init`** is the base the simple rollup is computed on, not the benefit
  base: point 1 carries 100,000.00 against a benefit base of 180,000.00, and the rollup at
  `t = 11` is 5% of it, 5,000.00, which with the stack takes the base to 195,080.00 and the
  first lifetime withdrawal to 10,144.16. Carried at the benefit base, the rollup would be
  9,000.00, the base 199,080.00 and the withdrawal 10,352.16.
- **`lw_pp_init`** is the income in force, which the next anniversary ratchets from in
  `INCOME`. In `DEPLETED` there is no base to recompute it from: point 14 pays its
  7,741.20 at every anniversary for life, and carried at 7,000.00 it would pay 7,000.00.
- **`mgsv_pp_init`** opens the floor. Point 1 carries the notes' 93,811.84 and closes
  contract year 8 at 84,605.80, `93,811.84 × 1.01 − 10,144.16`, which is also what the
  MVA's collar on a surrender at `t = 11` reads: its limit is
  `122,865.84 − 3,606.30 − 2,359.26 − 84,605.80 = 32,294.48`, the notes' figure. The floor
  binds where the surrender value falls below it, as it does on point 2, the anchor issued
  at the valuation date, in 85 months between `t = 83` and `t = 226`: at `t = 83` the
  surrender value is 93,387.87 and the surrender benefit the floor, 93,811.84.
- **`phase_prev_anniv_init`** is the phase the year under way's annual steps are processed
  under. Point 10's year opened in `ACCUM`, so at `t = 11` it takes its stack of 1,039.34;
  point 12's opened in `INCOME`, so at `t = 5` it takes its withdrawal of 9,929.10 and no
  rollup or stack, the growth window having closed at the first withdrawal; point 14's
  opened in `DEPLETED`, so it takes no index credit and no rider charge, cannot lapse, and
  is paid its income by the rider. The checks tie the phase to the balances (above).
- **`payout_rate_locked_prev_anniv_init`** is carried, not re-read. Point 13 locked 5.20%
  at its exercise age of 70, and its lifetime withdrawal at `t = 11` is 5.20% of its
  benefit base there, 143,893.99: 7,482.49, of which it asks 105%, 7,856.61. Re-read at
  the age the year closes at, 81, the band from 80 up would give 5.70%, 8,201.96.
- **`index_level_prev_anniv_init`** is where the year's point-to-point segment started.
  Point 12 carries 2,015.71, anniversary 12's level, and the year's return at `t = 5` is
  `2,297.91 / 2,015.71 − 1 = 14.00%`, credited at the 5.25% cap: 5,906.72 on its account
  value of 112,508.93. Carried at 2,200.00, as it would be had the index stood there at
  the anniversary, the return would be 4.45%, below the cap, and the credit 5,007.16. The
  generated scenarios change level only at `FIA_US_S`'s anniversaries, so on every
  committed row the scenario's level at `t = 0` is the column's too; a path that moves
  between anniversaries is where only the column holds the year's starting level.
- **`wd_cum_pp_init`** opens the running total of gross withdrawals, which reports and
  drives no cash flow: point 12 has taken 29,787.31 by the valuation date, three years of
  9,929.10, and its `wd_cum_pp` is 39,716.42 after the anniversary at `t = 5`.

The issue values `FIA_US_S` computes from the premium stay rules, and move into the issue
month: `prem_to_av_pp(t)` credits `P (1 + b)`, 107,000.00 on the anchor, its fixed share
`alloc_fixed() × P (1 + b)`, 21,400.00 on point 4, and the new `prem_to_mgsv_pp(t)` the
floor's 87.5% of the premium, the bonus excluded, 87,500.00, each in the month with
`duration_mth(t) = 0`; the benefit base and the rollup base open the first contract year
at the premium under the rider. The cells that bear the notes' names for the opening
values, `av_pp_init()`, `av_fixed_pp_init()`, `benefit_base_pp_init()`,
`rollup_base_pp_init()` and `mgsv_pp_init()`, read the opening state instead, 0 on new
business, as `pols_if_init()` does for the count.

A value of the contract year is read at the anniversary that opened the year three ways,
the same for each: from the frame, where that anniversary is at or after `t_entry()`;
from the model point's `_prev_anniv_init` or `_init` column, where the year opened before
the valuation date on a contract in force; and by the issue rule, in the first year of a
contract issued at or after the valuation date. Point 2's first year opens on 107,000.00 by
the rule, and its second on the close of `t = 11`, 106,050.00, from the frame, where a year
of no index credit against the rider charge leaves the account value above the base of
105,000.00 and the step-up binds; point 17's year opens on its column's 105,550.67; and
point 18's first year opens on 107,000.00 at `t = 15`. `phase_year_open(t)` and
`rollup_base_pp_year_open(t)` are cells of their own; `FIA_US_S` wrote each read inline in
every cell that made it.

The model point carries no rider status. In `FIA_US_S` a contract with the rider elected
loses it on the phase `TERMINATED` or a benefit base of 0, and the phase turns a base of 0
into `TERMINATED` at the anniversary; `Data` refuses both on a contract in force. So a
contract in force with the rider elected has the rider alive, and `rider_in_force_open(t)`
reads `glwb_elected()` for the year under way, as it does for a new contract's first year.

## Departures from FIA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock or of the opening state,
and every recursion begins at `t_entry()`. Where `FIA_US_S`'s test would have stayed correct
on the valuation clock, it moved anyway, so that cover has one definition. Of `FIA_US_S`'s
168 cells, 62 are unchanged, 12 have a new docstring only and 90 are rewritten; four are
removed, `entry_year`, `entry_mth`, `phase_init` and `payout_rate_init`, and 34 cells are
new, 198 in all. Compiling then changed how each cell reads its inputs and spells its
codes, and no number: it took away three of `FIA_US_S`'s cells, `bonus_clawback_on`,
`mva_pp_on` and `wd_reduction_rate_on`, each written inline in the cells that call it, and
added five, `point_id`, now a cell where it was the Space's parameter, and the four join
numbers `mort_schedule`, `rollup_number`, `scenario_number` and `wd_schedule_number`, 200
in all (*The compiled model*, below); of `FIA_US_S`'s cells it changed the signature of
two, `claims` and `claims_over_av`, whose total is the code `ALL`. The twin identity would
fail on a cell of `FIA_US_S`'s that this model lacked, so it exempts the seven by name, each
with its reason, compares `FIA_US_S`'s `(t, None)` with `(t, ALL)`, and reads every timing,
kind and scenario column at its code.

| Cells | `FIA_US_S` | `FIA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, and through it `duration`, `policy_year` and `age` | `duration_mth(t) = t` | `duration_mth_init() + t` | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth`, `entry_year`, `entry_mth` | `12 × policy_term()`, the months from issue; the frame from `entry_mth() = 12 × entry_year()` | `maturity_mth() − duration_mth_init()`, the months from the valuation date, refusing a point at or past maturity or with no cover from issue; `entry_year` and `entry_mth` removed | Every frame starts at the valuation date. `maturity_mth()` is new and keeps `FIA_US_S`'s formula |
| `anniv_mth`, `year_open_mth` | `12 × duration(t) + 11` and `12 × duration(t) − 1` | `t + 11 − duration_mth(t) % 12` and `t − 1 − duration_mth(t) % 12` | On the valuation clock a policy month is not a month of the frame |
| `pols_if`, `pols_if_init`, `pols_if_at` | `pols_if(t) = pols_if_at(t − 1, "AFT_DECR")`, from `pols_if_init()`, the column's 1.0, at `entry_mth()`, two cells a month | `pols_if_at(t, BEF_DECR)`, from `t_entry()`, one cell a month, with `BEF_NB` added; `pols_if_init()` is 0 unless in force | Contracts in force at the valuation date open the count; new business joins it in its issue month |
| `av_pp`, `av_pp_at`, `av_fixed_pp`, `av_fixed_pp_at` | `av_pp(t)` is `av_pp_at(t, "EOY")`, which reads `av_pp(t − 1)`: two cells a month, from `av_pp_init()` at `entry_mth()`; likewise the fixed account | each timing built from the month's opening in one formula, the opening `av_pp(t − 1)`, or the column at `t_entry()`, plus the premium credited in the issue month; `av_pp` and `av_fixed_pp` write it inline | One cell a month. The values are `FIA_US_S`'s bit for bit |
| `av_pp_init`, `av_fixed_pp_init`, `benefit_base_pp_init`, `rollup_base_pp_init`, `mgsv_pp_init`, `lw_pp_init` | read the columns, or, where one is blank, compute the issue value, `P (1 + b)`, `P` under the rider, `0.875 P` or 0; `av_fixed_pp_init` is `alloc_fixed × AV`, always | read the in-force columns, 0 on new business | The issue values stay rules, credited in the issue month (`prem_to_av_pp`, `prem_to_mgsv_pp`, the first year's opening of the bases), and a fixed account in force is a column of its own |
| `phase_init`, `payout_rate_init` | the phase, as text, and the locked percentage at entry | removed: `phase_prev_anniv_init()`, an int code, and `payout_rate_locked_prev_anniv_init()`, read by `phase_year_open` and `payout_rate_locked` | The phase is a code, and both are values at the anniversary |
| `premiums`, `prem_to_av_pp`, `prem_to_av` | at `t = 0` where `entry_mth() = 0`, on `pols_if_init()` | in the month with `duration_mth(t) = 0`, on `pols_new_biz(t)` | A point in force paid its premium before the valuation date, and one issued later pays it in its issue month |
| `av_pp_year_open`, `av_fixed_pp_year_open`, `benefit_base_pp_at`, `rollup_pp`, `rollup_base_pp`, `lw_pp_at`, `payout_rate_locked`, `phase_open`, `is_exercise`, `in_growth_period`, `rider_in_force_open` | the value at the anniversary opening the year from the frame, or from the entry columns where the year opened before `entry_mth()` | three ways: from the frame where the year opened at or after `t_entry()`, from the `_prev_anniv_init` or `_init` column where it opened before the valuation date, by the issue rule on new business; the new `phase_year_open` and `rollup_base_pp_year_open` read the phase and the rollup base so | A contract valued mid-year needs the year's opening values, which `FIA_US_S` cannot express |
| `index_level`, `scenario_value` | the scenario's level at anniversary `y`, keyed from issue; before its first row, the first row's level | the level at the valuation month anniversary `y` falls in, `12y − duration_mth_init()`, from the checked companion, by an explicit loop, raising where no level is set by then; for the anniversary opening the year under way, before the valuation date, `index_level_prev_anniv_init()` | The scenario runs on the valuation clock, and the year's starting level is history |
| `wd_cum_pp`, `mgsv_pp` | from 0 and from `mgsv_pp_init()` at `entry_mth()` | from `wd_cum_pp_init()` and `mgsv_pp_init()` at `t_entry()`, the floor adding `prem_to_mgsv_pp` in the issue month | Every recursion begins on the books, from the opening state |
| `mva_term` | `surr_charge_period − (t + 1)/12` | `surr_charge_period − (duration_mth(t) + 1)/12` | A policy month passed as `t` |
| `pols_maturity` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `check_pols_roll_fwd_resid`, `av_at` | `pols_if(t + 1)`, the next month's count; the residual 0 before `entry_mth()` | `pols_if_at(t + 1, BEF_NB)`; the residual 0 outside cover, before `t + 1` is read | Next month's new business is no part of month `t`'s movement, and no month past the frame is read |
| `check_av_roll_fwd`, `check_pols_roll_fwd` | `all(math.isclose(...))` over `entry_mth() … proj_len() − 1`, the tolerance fixed | a loop over `t = 0 … proj_len() − 1`, the tolerance scaled by `max(policy_count(), 1)`, failing at the first residual not within it, `not abs(r) <= tol`, so that one that is not a number fails, as `math.isclose` fails it | A residual is rounding on that many contracts |
| `phase`, `phase_open` and every cell that compares a phase | return and compare the phase strings, some by tuple membership | return and compare int codes, `PRE_ISSUE` 0 to `MATURED` 5; `result_glwb()` reports the labels | A projection cell branches on numbers; the conventions' phase check reads the labels |
| `covered_age`, `credit_rate`, `step_up_applies`, `rollup_base_pp`, `mva_pp_on` | branch on the text of `glwb_basis()` and `credit_method()` and of the References `step_up_mode`, `rb_wd_convention` and `mva_collar_basis`; `credit_rate` calls `credit_rate_on(r, method)` | branch on the new `is_*` cells, one bool for each value `FIA_US_S` tests, decoded once a point; `credit_rate` computes the engine inline, in `FIA_US_S`'s order; a value `FIA_US_S` does not know is answered as there | No projection cell compares a model point column's or a switch's text or calls a label accessor, which are left to reporting; compiling moved the column decodes into `Data` and made the switches codes |
| `mort_rate`, `surr_charge_rate`, `vest_rate`, `rollup_rate`, `payout_rate_locked`, `wd_scheduled_pp`, `scenario_value` | read `FIA_US_S`'s readers' tables per `t`, the payout bands walked row by row and the last surrender year taken by `int()` of the raw keys | read `Data`'s checked tables, each through one cell keyed by an age, a year or a year count: `mort_rate_base_at(a)`, `surr_charge_rate_py(y)`, `vest_rate_py(y)`, `rollup_rate_py(y)`, `payout_rate_at(a)`, `wd_scheduled_at(k)`, and `scenario_value(y, name)` | A key the table cannot be read by is refused by name before a value is read, and every table is read through one cell |
| every guarded cell | `t < entry_mth()` falls back to the `_init` cells; a dozen cells unguarded | outside cover, zero, `False`, `PRE_ISSUE` or `MATURED`, or 1.0 for `lapse_moneyness_factor`, before any table or rate is read | No month outside cover is the contract's (above) |
| `expenses`, `inflation_factor` | acquisition at `t = 0` on `pols_if_init()`; zero where `t < entry_mth()` or `t ≥ proj_len()`; inflation from issue | acquisition on the premium of the contracts issued, in the issue month and not inflated; zero outside cover; `inflation_factor` unchanged in code, on `t` | Acquisition per contract issued, as in `basiclife/BasicTerm_SE`, and unit costs in valuation-date dollars |
| `result_cf`, `result_pols`, `result_av`, `result_glwb`, `result_cf_annual` | over `entry_mth() … proj_len() − 1`; `result_cf_annual` by `duration(t) + 1` | over `t = 0 … proj_len() − 1`, zeros before issue; `result_pols` with `pols_new_biz` second; `result_glwb`'s phase decoded; `result_cf_annual` over the months in cover, by `policy_year(t)` | The frame starts at the valuation date |
| `lapse_moneyness_factor` | no guard: outside its frame it reads a month past the frame | 1.0 outside cover | A month outside cover has no moneyness |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_new_biz`, the six new opening-state accessors and the thirteen `is_*` decodes: two of
`glwb_basis`, five of `credit_method` and two each of the three string References. The
docstring-only changes rewrite the time-axis prose, say which cells are labels for
reporting, which engines `FIA_US_S`'s tests call and no projection cell does
(`credit_rate_on` and `payout_rate`), and that `use_guaranteed_scale` is set before the
model computes anything, and correct "this cells" in `activation_rate`. In `Data`,
`model_point_table` reads `model_point_table_sec.csv` and checks it, `rate_scenario_file`
names `rate_scenario_sec.csv`, `future_horizon_mth` is new, `rate_scenario`'s and
`withdrawal_table`'s docstrings name the clock their `t` is on, and nine cells are new: the
six checked tables and the three int extents, `surr_charge_last_year`,
`payout_rate_first_age` and `payout_rate_last_age`. `FIA_US_S`'s six readers are unchanged
in code.

The four joins on text keys are `FIA_US_S`'s, each read by the one cell that reads its
table: mortality on the model point's `sex`, in `mort_rate_base_at`; the rollup schedule on
its `rollup_id`, in `rollup_rate_py`; the withdrawal programme on its `wd_schedule_id`, in
`wd_scheduled_at`; and the scenario on its `scenario_id`, in `scenario_value`. Running in
force kept them on the text, as `FIA_US_S` joins; compiling moved each join into `Data`,
which numbers the keys once, and the cell reads its table at the point's number; it
moved the seven decodes of the model point's columns there too, and turned the three
switches and the timing and kind strings into int codes (*The compiled model*, below), so
that no projection cell compares text. `Data` checks
each key before a projection reads by it.

The cap on mortality is no departure: `mort_rate` caps the annual rate at 1, as
`FIA_US_S` does, and writes the cap `min(q, 1.0)`, the bound second, so that a blank rate
that reached it would stay NaN rather than read as certain death; `Data` refuses a blank,
text or infinite rate in any case. At the shipped A/E factor of 100% the cap binds at age
120 alone, where the table's rate is 1.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, so point 1's
`expenses(t)` is `FIA_US_S`'s `expenses(84 + t)` divided by `1.025^7`, and point 10's,
valued five years on, `FIA_US_S`'s divided by `1.025^5`. Their other cash flows, their
counts and every value per contract are `FIA_US_S`'s from the month they are valued at on.
Point 18 is `FIA_US_S`'s point 2 fifteen months on in those columns too. Its maintenance
expense is `1.025^(15/12)` times S's, inflated from the valuation date rather than from
its issue, and its acquisition, uninflated in both, is S's.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, and the compile tests hold it
so on x86-64 on the splice grid and at the contract's extremes too, which take the
branches the committed points do not. `FIA_US_SEC` compiles on the chassis
`MYGA_US_SEC` compiled first, and takes from it what `MYGA_US_SEC`'s *What the deferred
annuities inherit* sets out; where it departs, this section says so.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py fixed_indexed_annuity                   # in place
python tools/build_sec_cy.py fixed_indexed_annuity --out /tmp/fia    # elsewhere
```

The tool exports the model to `FIA_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `FIA_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/fixed_indexed_annuity")    # the directory holding the build
from FIA_US_SEC_nomx_cy import mx_model as model
model.Projection[13].result_cf()                         # point 14, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 13` after `Projection.result_cf()` leaves point
1's frame cached, `proj_len()` 624, while `point_id()`, not yet computed, reads point 14's
label, and `Projection.expense_maint` set to 60 once `Projection[1]` has computed point
2's `expenses(0)` leaves it at 6,006.67, where modelx, and an ItemSpace made after,
compute 6,005.00. Set every Reference on a model just imported, before anything is
computed, where modelx would recompute; a test holds the compiled model to this.

A build takes about three and a half minutes with gcc, 204 s here under load, and needs a
C compiler, which is why `requirements.txt` leaves modelx-cython out:
`pip install -r requirements-cython.txt`. `run_sec.py --cython` builds in place when it
finds no build, or one older than the model, the sample, the spec or the tool, and
`--build DIR` runs a build made with `--out DIR`. Nothing a build writes is committed. All
of it derives from committed files, and an extension module is built for one operating
system, processor and Python (`_mx_classes.cpython-313-x86_64-linux-gnu.so` here); in
place, `.gitignore` covers all of it. A `lifelib.create()` copy of the library carries no
`tools/`, so it cannot build, and `run_sec.py --cython` says so.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so. Compiled by
the same tool, with a sample of its own, as it stood after running in force, the model typed
163 of its 198 `Projection` cells as C numbers. Fourteen returned a row, text or a
DataFrame; sixteen took a timing, a kind, a scenario column or a crediting method or basis
as text, and five took a float, and those 21 kept a dictionary for a cache. It ran 1.5 times
as fast as its own export, 22.4 ms a point on `net_cf` against 33.5, over the committed
points. The bodies of the typed cells still called pandas and Python: a
`model_point()` lookup for each attribute a formula reads, the text of a column or a
switch compared in each of the thirteen decodes, a `.loc` on a table for each attained
age's mortality, each contract year's surrender charge, vesting and rollup, each year's
scheduled withdrawal and each anniversary's scenario level, a total over the kinds for
`kind=None`, and `pd.isna` for a blank joint age. So
each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[13]` is point 14, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The vectors are the checked columns
  `Data.model_point_table()` returns, read as `FIA_US_S` reads them, by `float()` and
  `int()`: unlike `MYGA_US_SEC`, the model reads no separate copy of the numeric columns,
  since the table's checks, from stage `E`, already refuse every numeric column a formula
  reads where it is blank, text or out of its range, naming the column and the points.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once, the seven `is_*` vectors:
  `glwb_basis` into `is_single_basis` and `is_joint_basis`, and `credit_method` into one
  flag for each of its five methods, and a blank `joint_age` into the issue age. Each
  compares the text exactly, as `FIA_US_S` compares it, so a value written in another case
  or with a space, `Cap` or ` cap`, is no flag, and the cell that branches on it answers as
  `FIA_US_S` does, raising its message, `invalid credit_method`, or reading the basis as
  single where `FIA_US_S`'s `covered_age` does. The rider election is a 0/1 vector read by
  value, `"False"` written as text among them, as stage `E`'s check reads it.
- **The switches, as codes.** `step_up_mode`, `rb_wd_convention` and `mva_collar_basis`,
  text References in `FIA_US_S`, hold an int code, `ANNUAL`, `PRO_RATA` and `GROSS` as
  shipped, `AT_EXERCISE`, `DOLLAR` and `SURRENDER_VALUE` the alternatives, each read by its
  two decodes, which stay `Projection` cells. A code neither decode names, 2 or −1, raises
  `FIA_US_S`'s message, `invalid step_up_mode`, in both engines. A text set on one is no
  code: modelx then raises the same message, and the compiled model refuses the text at
  once, as it refuses any text set on an int Reference (*What it refuses*, below).
- **Tables indexed by integers.** Each assumption table is an array, or a set of arrays, a
  cell reads by element. The mortality table's sexes, the rollup schedules, the scenarios
  and the withdrawal programmes are numbered from 1 in the sorted order of their keys, each
  point carrying its own, `mort_schedule()`, `rollup_number()`, `scenario_number()` and
  `wd_schedule_number()`. The mortality is held by sex and attained age, with each sex's
  first and last age beside it; the surrender charge and the vesting by contract year; the
  rollup schedules by schedule and contract year, step-filled, 0.0 before a schedule's
  first row, where `FIA_US_S`'s step function finds none; the payout bands by exercise age,
  one row an age, single-life and joint-life side by side; the scenarios by scenario and
  valuation month, step-filled from a scenario's first row, with each scenario's first
  month beside them; and the programmes by programme and elapsed contract years, 0.0 where
  a programme has no row, which is no withdrawal, as in `FIA_US_S`. Each is read through
  one cell keyed by the age, the year or the count, `mort_rate_base_at(a)`,
  `surr_charge_rate_py(y)`, `vest_rate_py(y)`, `rollup_rate_py(y)`, `payout_rate_at(a)`,
  `wd_scheduled_at(k)` and `scenario_value(y, name)`, each of them a reader running in
  force had already added, and the padding, NaN, is read by none of them.
- **Arrays held to the last read.** Every array ends at the last month or age a read
  reaches, whatever the table's keys, as `MYGA_US_SEC`'s scenario and withdrawal arrays end
  at `Data.read_last_mth`: the scenarios run to `read_last_mth`, 1,093, the last `t` of the
  cache, `12 × (maturity_age − issue_age_min + 1) + future_horizon_mth + 1`; the rollups to
  the contract year a month to it falls in, 92, and the programmes to the count of years it
  falls in, 91; and the mortality and the payout bands to `Data.read_last_age`, 122, the
  last `a` of the cache, `maturity_age + 2`. `spec_sec.py` derives both References, and a
  test holds each to the spec. A schedule's, a band's or a scenario's last row holds to the
  end, as the step function and the last band hold it, so a key far past any read, a
  scenario level or a withdrawal at 1e10, which `FIA_US_S` holds and never reaches, neither
  makes an array gigabytes wide nor refuses a point `FIA_US_S` projects. Unlike
  `MYGA_US_SEC`'s, which end at their tables' last keys where those come first, the
  scenario, rollup and withdrawal arrays always run to the bound, 1,094 months a scenario,
  about 18 KB for its two columns, so that each reader can refuse a read past the bound,
  naming the point, rather than hold the last level there: no projection reads one, and the
  refusal keeps the array's end and the cache's in step.
- **Ages from the table's first.** The payout array starts at the first band's age and
  the mortality at the table's first age, or at 0 where that is lower, rather than at age
  0, so that the age less the array's first is the index. So no age a table holds is
  refused, a negative one among them, which `FIA_US_S` holds beside the ages it reads, and
  none far below the others widens an array. Where `MYGA_US_SEC` pads its age tables from
  0 and refuses a negative age, this model reads the table `FIA_US_S` reads.
- **Codes.** A timing, a kind or a scenario column, which `FIA_US_S` spells as text, is an
  int Reference named as the text: the count's timings `BEF_NB = 0`, `BEF_DECR = 1`,
  `BEF_MORT = 2`, `BEF_LAPSE = 3` and `AFT_DECR = 4`; the account value's `BEF_PREM = 5`,
  `BEF_INV = 6`, `BEF_FEE = 7`, `BEF_WD = 8` and `EOY = 9`; the benefit base's own
  `BEF_ROLLUP = 10` and `BEF_STEP_UP = 11`; the kinds `DEATH = 0`, `LAPSE = 1` and
  `MATURITY = 2`, in `result_cf`'s order, and `ALL = 3`; and the columns
  `INDEX_LEVEL = 0` and `MVA_REF_YIELD = 1`. A call reads as before, less the quotes:
  `pols_if_at(t, BEF_DECR)`, `av_pp_at(t, BEF_WD)`, `claims(t, DEATH)`. A string argument
  would give the cell a dictionary for a cache, where a code indexes a C array, so codes are
  numbered from 0 without a gap. The three families of timing, passed to different cells,
  are numbered as one, `BEF_NB` and `BEF_DECR` first, as in every SEC model, then the
  count's others, the account value's and the benefit base's own, each family in the order
  of its instants. The benefit base and the lifetime withdrawal share `BEF_WD` and `EOY`
  with the account value, where `FIA_US_S` spells them alike, so each is one Reference,
  and `BEF_MORT` keeps a code of its own, though the count reads it at `BEF_DECR`'s
  instant, so that each string is one code. So a code of one family passed to another's
  cell, `av_pp_at(t, BEF_NB)`, is refused as `invalid timing` in both engines, rather than
  read as a timing of the cell's own. The `Projection` docstring's *Codes* lists all
  twenty-four, the switches' six among them.
- **The totals, by `ALL`.** `FIA_US_S`'s `claims(t, kind=None)` and
  `claims_over_av(t, kind=None)` are one kind's amount or, with `None`, the three kinds
  added: `None` is no C parameter. Here the total is the code `ALL`, and `net_cf` calls
  `claims(t, ALL)`. `FIA_US_S` writes the total as a chain of `+`, death, lapse, maturity,
  and the chain is kept, so the total is `FIA_US_S`'s float bit for bit, the sign of a
  zero included. The twin identity compares `FIA_US_S`'s `(t, None)` with `(t, ALL)`.
  `ALL` passed to a cell of one kind is refused as `invalid kind`: by `pols_decr`,
  `claim_from_av_pp` and `claims_from_av` in every month, and by `claim_pp` outside a
  `DEPLETED` month, where `claim_pp`, as `FIA_US_S`'s, answers 0.0 before it reads the
  kind.
- **No float parameter on the projection's path.** A cell keyed by a float compiles with
  a Python dictionary for a cache. `FIA_US_S`'s bonus clawback,
  `bonus_clawback_on`, its collared MVA, `mva_pp_on`, and its proportional reduction,
  `wd_reduction_rate_on`, which the projection calls on a currency base, are each written
  inline in their callers: the clawback in `wd_clawback_pp` and `surr_clawback_pp`, the MVA
  with the clawback inside it in `wd_mva_pp` and `mva_pp`, and the reduction in
  `wd_reduction_rate`, each the same expression in the same order, so the numbers are
  `FIA_US_S`'s bit for bit. The twin identity exempts the three, whose values it compares
  through their callers in every month. `credit_rate` and `payout_rate_locked` already
  computed the crediting engine inline, on the decodes, and read the payout bands through
  `payout_rate_at`, from stage `E`.
- **Four cells kept as `FIA_US_S` wrote them.** `credit_rate_on(r, method)`,
  `payout_rate(a, basis)`, `mgsv_rate_statutory(cmt5, option_cost)` and
  `mgsv_rate_is_compliant(cmt5, option_cost)` take a float or text, and no projection cell
  calls them. They are `FIA_US_S`'s formulas, `math.floor` and the walk of the payout bands
  included, kept for a reader, for `FIA_US_S`'s own tests and for the comparison with
  `FIA_US_S`, which calls them at the arguments `FIA_US_S`'s tests use.
  `mgsv_rate_statutory` tests its step for zero before it divides (*What it refuses*,
  below). `tests/us_registry.py` names the four, under `"engine"`, and the compile tests
  admit them, and no other cell, to a dictionary cache, a float or text parameter and the
  `math` module; no compiled cell may call them. Compiled, `method` and `basis` are typed
  `str`, so a value that is not text raises `TypeError` there, where modelx raises `invalid
  credit_method` or `invalid glwb_basis`.
- **No Python call kept.** No formula outside the reporting and engine cells calls a Python
  builtin outside its refusals but `int`, `float`, `bool`, `min` and `max`, which Cython
  turns into C, so `tests/us_registry.py` admits none. No such cell is uncached, and none
  takes a float.
- **Operands in `FIA_US_S`'s order.** Compiled, a two-argument `max` or `min` evaluates
  its arguments right to left, so a point that reaches two refusals would raise the
  second's message. Each that takes two operands from cells, `wd_guar_pp`,
  `wd_unfunded_pp`, `wd_free_pp`, `surr_benefit_pp` and `claim_pp` for `DEATH` and for
  `MATURITY`, binds them to locals first, in `FIA_US_S`'s order. No number moves: only the
  order the caches fill.
- **Reporting cells stay Python.** `model_point()`, the eight label accessors
  `policy_id()`, `sex()`, `tax_status()`, `glwb_basis()`, `credit_method()`, `rollup_id()`,
  `scenario_id()` and `wd_schedule_id()`, and the five reports return a table row, text
  and DataFrames, for a reader, for `run_sec.py` and for the comparison with `FIA_US_S`.
  No other cell calls them, so they cost the projection nothing. A label accessor returns
  its column as read, and `Data` accepts a label that is not text: a blank or numeric
  `policy_id` or `tax_status`, which no cell reads, a `glwb_basis` or `credit_method`
  none of its decodes names, which the projection meets as `FIA_US_S` does, and a numeric
  `sex`, `rollup_id`, `scenario_id` or `wd_schedule_id` where its table's keys are
  numbers. So each accessor compiles to a Python object, as the sample traces it (below),
  and returns what modelx returns. The two checks are reporting cells too, but they return
  a verdict, which compiles to a C `bint`.

Of `Projection`'s cells, compiling took away three, `bonus_clawback_on`, `mva_pp_on` and
`wd_reduction_rate_on`, and added five: `point_id`, `mort_schedule`, `rollup_number`,
`scenario_number` and `wd_schedule_number`, 200 in all. The Reference `idx`, 0, takes the
place of `point_id`, and `issue_age_min`, 40, `issue_age_max`, 80, and the 24 codes of the
timings, the kinds, the columns and the switches' alternatives are new References, the three
switches holding codes. `Data` has 76 cells, 17 at stage `E`, and its docstring lists its
vectors, arrays and counts, each with the column or file it comes from: 21 vectors of int64,
by point, scenario or sex, and 22 of float64, by point or year; six tables of float64, the
mortality, the rollups, the payout bands, the two scenario columns and the programmes; and
thirteen int counts and extents, each read from a checked table. Its seven readers, its six
checked tables and `input_dir()` stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 182 of
its 200, the two checks among them, returns a C `bint`, `long long` or `double`, and caches
a single value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,094 by `t`, of `double`, `long long` or `bint` | the 104 cells of `t` alone: every count, rate, factor, charge, credit, withdrawal, value, claim and cash flow; the policy clock, its years and its anniversaries, the attained, covered and exercise ages; the phases and the flags `is_active`, `is_anniv`, `is_exercise`, `depletion_cause`, the rider's two, `in_growth_period`, `step_up_applies` and `mva_in_force`; and the checks' monthly residuals |
| a C array of 1,094 by 12 | the 13 cells of `t` and one code: `pols_if_at`, `av_pp_at`, `av_fixed_pp_at`, `av_indexed_pp_at`, `benefit_base_pp_at`, `lw_pp_at` and `av_at`, by `(t, timing)`; and `pols_decr`, `claim_pp`, `claim_from_av_pp`, `claims`, `claims_from_av` and `claims_over_av`, by `(t, kind)` |
| a C array of 83 by 12 | `scenario_value`, by `(y, name)` |
| a C array of 83 by `y` | `index_level` and `mva_ref_yield`, by anniversary, and `surr_charge_rate_py`, `vest_rate_py` and `rollup_rate_py`, by contract year |
| a C array of 123 by `a` | `mort_rate_base_at`, `payout_rate_at` and `activation_rate`, by age |
| a C array of 82 by `k` | `wd_scheduled_at`, by elapsed contract years |
| one `long long`, `double` or `bint` | the 55 cells without a parameter: the point's label, numbers, decodes, join numbers and flag, its opening state, the six switch decodes, the ends of its frame, its cap and fixed rate in force, its clawback factor, and the two checks |
| a Python object | the reporting cells but the checks, fourteen |
| a Python dictionary, behind a C signature | the four engine cells, their bodies Python |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary but the engine
cells'.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the five reports
and the two checks on every committed point, which reach every cell but these:
`model_point()` and the eight label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; the four engine cells, which no projection cell calls;
`bonus_factor` and `activation_rate`, which only a reader asks for; the withdrawals to
date, `wd_cum_pp` with `wd_cum_pp_init`, the indexed account, `av_indexed_pp`, and
`claims_over_av`, which no report reads; and the five decodes no committed point and no
shipped Reference asks, `is_credit_spread`, `is_credit_trigger`,
`is_step_up_at_exercise`, `is_rb_dollar` and `is_collar_surrender_value`, each asked only
where the decodes before it in its cell answer False. Nor do they reach every code: no
report reads the fixed or the indexed account at each timing, the account value before the
fee or the count before its lapses. The sample calls those too, the monthly ones in every
month of the frame and the month after it, each timed cell at every code of its family and
each kinded cell at its three kinds, `claims_over_av` at `ALL`, and the engine cells at the
arguments `FIA_US_S`'s own tests use. It projects the committed points alone: the export
it runs reads the CSVs of the directory the build is made in, and the trace it needs is
the committed points', which are what the tests project. The eight label accessors it
calls once more, on a copy of the table's first point with its four free labels blank and
its four keys, `sex`, `rollup_id`, `scenario_id` and `wd_schedule_id`, the number 1,
beside one-key copies of the mortality, rollup, scenario and withdrawal tables keyed by 1,
which it writes to a temporary directory and reads by a second instance of the export,
given the files' absolute paths. That types them as Python objects, so that a blank or
numeric label returns what modelx returns rather than raising `TypeError` (*What compiling
changed, and why*). The committed points leave branches untaken: the female mortality, the
spread and trigger methods, the at-exercise step-up, the dollar rollup base, the
surrender-value collar, a joint income below the first band, a withdrawal programme past
its first years, the youngest and oldest issue ages. That still types every cell, because
every branch of a cell returns the one type its others return, a rate a float in every
branch and a phase an int in every branch, and on points that take those branches the
compiled model computes modelx's numbers (above). A code a cell refuses is not called: a
raise types nothing. The sample also raises the recursion limit, which modelx raises and
its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forwards read and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and one of headroom:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,094 | 1,092. The longest frame is a contract issued at the youngest issue age, 40, covered through the contract year entered at 120, 972 months, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: `t = 0 … 1,091`, and the month after, 1,092. Every cell that reads `t + 1`, the count's roll-forward residual and `av_at(t, EOY)` among them, answers 0 outside cover before it reads it, and the surrender rate's read of the anniversary closing its year stays in the frame, so nothing reads 1,093, which is the headroom |
| `t`, and `timing` or `kind` | 1,094 by 12 | the twelve timings of the one numbering, `BEF_NB` 0 to `BEF_STEP_UP` 11, and the three kinds and `ALL`. Every 2-D cache has this one width. Cython's generated unpickle code converts a space's 2-D caches with one function for each inner width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A kind from 4 to 11 or a timing a cell does not take is then inside the cache, where the cell refuses it as modelx does, and a code from 12 raises |
| `y`, and `name` | 83 by 12 | the anniversary 82, below, and the two columns, a column from 2 to 11 refused inside the cache as above |
| `y` | 83 | 81, `maturity_age − issue_age_min + 1`: the contract year of the last covered month at issue age 40, read by the three year readers, and the anniversary closing it, read by `index_level`, `mva_ref_yield` and `scenario_value`, each in cover alone; plus one, and one of headroom |
| `a` | 123 | 121, `maturity_age + 1`: the exercise age closing the contract year entered at 120, read by `payout_rate_at`, past the last attained age `mort_rate_base_at` reads, 120; `activation_rate` shares the size. It rests on `issue_age_min` only through its being 0 or more; plus one, and one of headroom |
| `k` | 82 | 80, the elapsed contract years of the last covered year at issue age 40, read by `wd_scheduled_at` in cover alone; plus one, and one of headroom |

`proj_len()` refuses a point issued below 40, `issue_age_min`, or above 80,
`issue_age_max`, the issue ages `product-spec.md` admits, one with no cover from issue, one
at or past maturity, and one whose sex's mortality stops below 120, `maturity_age`, in
modelx as compiled, and cover ends with the contract year entered at `maturity_age`, so no
report on a point the model projects runs past these caches. `issue_age_min`,
`maturity_age` and `Data.future_horizon_mth` are the contract the sizes are derived from;
`issue_age_max` sizes nothing, since every size rests on the youngest issue age, and set
higher it projects the older issue ages `FIA_US_S` projects. Lower the minimum, or raise
`maturity_age` or the horizon, and a report runs past the caches in the compiled model
alone: a frame of more than 1,092 months, an anniversary past 82 or an age past 122 raises
`IndexError`, naming nothing, where modelx projects. Each needs the sizes derived again, as
`spec_sec.py` derives them, `Data.read_last_mth` and `Data.read_last_age` with them, and a
rebuild. The shipped mortality table starts at attained age 40, the youngest issue age, so
a point younger than 40 in its first month on the books is refused by `Data` first, naming
it.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it was
measured to change there. Here `cpow` reaches six powers in six cells: the monthly rates of
both decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`; the fixed
account's and the floor's monthly accruals, `(1 + i)^(1/12)` in `fixed_interest_pp` and
`mgsv_pp`; the MVA, `[(1 + i0)/(1 + it)]^(n/12)` in `mva_rate`; and expense inflation,
`(1 + r)^(t/12)` in `inflation_factor`. Without `cpow` a compiler with C99's complex
numbers, gcc among them, computes a power of two doubles as a complex power, which can
differ from Python's float power in its last bits. With both directives and the flag every
compiled value agrees with modelx's bit for bit, and the compile tests hold each, by the
module's first line, by the compiler's command lines and, on x86-64, by the comparison
itself. On the same platforms the tool adds `-Werror=incompatible-pointer-types`, so that
gcc before 14, which only warns of a pointer of the wrong type, fails the build as gcc 14
does: the error two cache widths give (*The sample and the spec*, above).

A power of a negative base is where the two engines would part: Python gives a complex
number, or raises, and `cpow`'s C power NaN. The base of each power is held at 0 or more:
the decrements' by `Data`, which refuses a mortality rate outside 0 to 1, and by the cap
and clamp on each annual rate; the MVA's by `Data`, which refuses a reference yield, at
issue or in a scenario, at −1 or below; and the fixed rate in force, `mgsv_rate` and
`inflation_rate`, Projection References `Data` cannot read, by the cell that takes the
power, which refuses a rate below −1, naming the point, in both engines (*What it
refuses*, below). At exactly −1 the base is 0, and the power is 0 in both.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 3,398,096
bytes, about 3.4 MB, the type's basic size, which holds every cell's cache, each beside a
flag array of its shape that marks what is computed. The thirteen 2-D caches, 1,094 by
12, are about 2.05 MB of it with their flags, three fifths, and the 104 arrays by `t`
about 1.33 MB, nearly all the rest. That is 1.35 times `MYGA_US_SEC`'s, for frames of
1,094 months against 1,322 and thirteen 2-D caches 12 wide against ten 8 wide. Making one
and releasing it, nothing computed, took 0.14 ms here, the collection included. Deleting
it, `del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a compile test holds a compiled block run to one point's ItemSpace at a time. Without
it, 504 compiled points peaked at 1,601 MB (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no limit
raised. What it needs is stack. The deepest calls the contract allows, cold in the last
month of the longest cover, issue age 40, issued now or 120 months on, run the count's and
the account value's chains back to `t_entry()`, 979 cells deep in modelx on `net_cf` and 998
on the count's roll-forward residual, `check_pols_roll_fwd_resid`, and on `expenses` and
`pols_lapse`, which read the count: one cell a month and 7 to 26 more, the count's first
month reading the account value's chain at the anniversary closing it. Compiled with gcc,
`net_cf` runs on a thread of 236 KiB of stack and not of 234, and the residual on 238 KiB
and not 236, 242 to 247 bytes a level. A test runs `net_cf`, the residual and `pols_lapse`
cold, at the valuation date and 120 months on, in a thread of 1 MiB, the stack Windows gives
a program's main thread unless the program is linked for more, and again on the main thread,
which is where `run_sec.py --cython` runs. MSVC's frames may be larger than gcc's, and the
`cython` CI job, which runs the test on Windows too, is the check on them: the test first
runs the call at seven stacks, from 256 KiB to 2 MiB, and reports the smallest it ran on, so
a first run there measures MSVC's need. Until it has, the need is an estimate: at the 325 to
433 bytes a level MSVC took on `WholeLife_US_SEC`'s chain, 998 levels need about 317 to 422
KiB, inside 1 MiB by more than twice. A stack below the need kills its child on an overflow,
by design; on Windows the child ends with `STATUS_STACK_OVERFLOW`, and should Windows Error
Reporting hold it instead, the test waits a bounded time for each child rather than the
job's hour. The export recurses in Python instead: the same calls need a recursion limit of
2,001 there, on the residual, `expenses` and `pols_lapse` alike, and 1,976 on `net_cf`, and
the five reports and the two checks, which run in ascending `t`, need 742 with the package's
import, as the sample runs them, so `sample_sec.py` sets 9,000, four times the first rounded
up to the thousand, and a test holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode or hold, when the vector is first read, naming every point at
  fault, or the table and its lines: a `point_id` that is not a whole number,
  `model_point_table_sec.csv: point_id must be a whole number; ['7x'] is not`, read by
  `point_id()` and every refusal. And, before it is cast to int64, a number of `2**53` or
  more in size, which numpy would cast to the least int64 once past int64: a model point's
  `duration_mth`, issue age, `income_start_age` or `joint_age`,
  `model_point_table_sec.csv: joint_age must be below 2**53 in size; it is not at point_id
  [3]`, a refusal `FIA_US_S` lacks on the last two, which it projects at `1e20`; a
  `point_id`; and, by the table's check, which every reader of the table asks first, an
  assumption table's key, `rate_scenario_sec.csv: t must be below 2**53 in size; it is not
  on line [5]`. A key written as a float, an age `61.0`, is read by its value, as
  `FIA_US_S`'s lookups match it, and a key that is not whole is refused by the table's
  check, as at stage `E`. A key far past any read, short of `2**53`, is held nowhere and
  refuses nothing (*What compiling changed, and why*).
- A key beyond a table, by the one cell that reads it, naming the point, where
  `FIA_US_S`'s lookup raised `KeyError`: an attained age outside the point's sex's,
  `point_id 1: the mortality table gives no rate at attained age 39`, from
  `mort_rate_base_at`; a contract year below 1, `point_id 1: the surrender charge table
  gives no rate at contract year 0`, from `surr_charge_rate_py` and `vest_rate_py`; and a
  month before the point's scenario's first, `point_id 1: scenario sets no level by month
  -84`, from `scenario_value`. No projection reaches any of them: `Data` refuses a point
  whose first month on the books its tables do not cover, and `proj_len()` one its
  mortality stops short for. Each reader likewise refuses a read past the month or age its
  array is held to, `Data.read_last_mth` or `Data.read_last_age`, which no projection
  makes; inside the caches the arrays reach those bounds, so compiled, a read past them
  meets the cache's end first (below). A contract year before a rollup schedule's first
  row, and a count a programme has no row at, are no rollup and no withdrawal, as in
  `FIA_US_S`.
- By `proj_len()`, in this order: a point issued below `issue_age_min` or above
  `issue_age_max`, `point_id 2: issue age 81 is above issue_age_max, 80`; one whose cover
  from issue is empty; one at or past maturity at the valuation date; and one whose sex the
  mortality table rates only below `maturity_age`, `point_id 2: the mortality table gives
  no rate at attained age 120, the age the last contract year is entered at`.
- A rate whose power would take a negative base, by the cell that takes the power, naming
  the point: a fixed rate in force below −1, `fixed_rate` or, under the guaranteed scale,
  `fixed_rate_min`, `point_id 4: the fixed rate in force, fixed_rate_min or fixed_rate,
  must be -1 or more, not -1.5`, in `fixed_interest_pp`; a `mgsv_rate` below −1, in
  `mgsv_pp`; and an `inflation_rate` below −1, in `inflation_factor`. Where `FIA_US_S`
  projects a complex number, or raises `TypeError` at the next `max`, both engines refuse,
  so that neither computes what the other cannot: a refusal `FIA_US_S` lacks.
- A divisor of zero, with Python's `ZeroDivisionError: float division by zero`, which the
  cell tests before it divides, since compiled division words it `float division`: a
  `mgsv_stat_step` of zero, in the engine cell `mgsv_rate_statutory`, where `FIA_US_S`
  raises the same. Every other division divides by a constant, 12 or 12.0, by `1 + b` or
  `1 + i`, which `Data` holds above 0, or by an index level, an account value or a
  remainder the cell tests first, answering 0, the floor of the moneyness factor or a full
  reduction where it is 0 or less, as `FIA_US_S` does.
- A timing, a kind or a column a cell does not take, `ValueError("invalid timing")`,
  `("invalid kind")` and `("invalid name")`, where the code is inside the cell's cache: a
  code of another family, `pols_if_at(0, BEF_WD)`, `av_pp_at(0, BEF_NB)`, a kind a cell
  lacks, `claim_from_av_pp(0, ALL)`, or `claim_pp(0, ALL)` outside a `DEPLETED` month, a
  code up to 11, `claims(0, 5)`, and a column past the two, `scenario_value(7, 2)`; and a
  switch's code that neither decode names, `invalid step_up_mode`, `invalid
  rb_wd_convention` and `invalid mva_collar_basis`.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1094)` and `net_cf(-1)`, which modelx answers, the second, on point 1, in force,
with a month before the valuation date; `pols_if_at(0, 12)`, `claims(0, 12)` and
`scenario_value(0, 12)`, which modelx refuses as `invalid timing`, `invalid kind` and, on
point 1, a month before its scenario's first; `scenario_value(83, INDEX_LEVEL)`,
`index_level(-1)`, `surr_charge_rate_py(83)`, `vest_rate_py(83)`, `rollup_rate_py(83)` and
`rollup_rate_py(-1)`, `payout_rate_at(-1)`, `wd_scheduled_at(82)` and `wd_scheduled_at(-1)`,
`activation_rate(123)` and `activation_rate(-1)`, and `mva_ref_yield(83)`, which modelx
answers with a number; and
`scenario_value(-1, INDEX_LEVEL)`, `surr_charge_rate_py(-1)`, `payout_rate_at(123)`,
`mort_rate_base_at(123)` and `mort_rate_base_at(-1)`, which modelx refuses, naming the
point and the key. An `idx` past the last row is refused in both, with an `IndexError` at
the first read of a vector, and `Projection[-1]` reads every vector at its last element in
both, so it is the table's last point, under that point's own `point_id()`, 18.

A Reference is a C variable of its value's type: `issue_age_min`, `issue_age_max`,
`maturity_age`, the codes, the switches and `idx` a `long long`, as
`Data.future_horizon_mth` is, the two flags `use_guaranteed_scale` and
`rider_charge_from_mgsv` a `bint`, and the rates and amounts a `double`. Set past that
type, it is converted when it is set, where modelx keeps the value as given. A float set
on an int Reference is truncated toward zero without a word, `maturity_age = 120.7`
reading 120, so that point 2's `proj_len()` is 708, where modelx computes with the float
and refuses the point, the mortality giving no rate at attained age 120.7. A text, a NaN,
an infinity or an int beyond 64 bits is refused at once, with `TypeError`, `ValueError` or
`OverflowError`, the switches' text, `step_up_mode = "annual"`, among them, which modelx
takes and then refuses as `invalid step_up_mode` at the first cell that decodes it. An
int set on a `double` Reference reads as a float compiled, where modelx returns the int:
`fixed_rate = 2` gives `fixed_rate_in_force()` 2 in modelx and 2.0 compiled. Each shipped
Reference is a value of its C type, so no shipped number differs. And a Reference set past
its domain computes as C computes, where modelx raises: an `inflation_rate` of `1e300`
makes `inflation_factor(24)` infinite compiled, where modelx's power raises
`OverflowError`.

Mortality is capped at 1, as in `FIA_US_S`, by `min(q, 1.0)`, the bound second, the rider
charge rate at `rider_charge_rate_max` the same way, and the annual surrender rate at
`lapse_rate_max`, 35%, by `min(lapse_rate_max, …)`, the bound first, as `FIA_US_S` writes
each; the compiled model computes each as comparisons in the same order. So a NaN sent
through a Reference, `mort_ae_factor` or `rider_charge_rate`, stays NaN at the first two
caps in both engines, and the roll-forward check it reaches fails, in both, while one that
reaches the surrender rate's cap, through a base rate, gives the cap, 35%, in both, as in
`FIA_US_S`.

### Speed

`python tools/bench_sec_cy.py fixed_indexed_annuity` builds the model into a temporary
directory, or takes a build with `--build`, and times one block run on three engines:
modelx, the export and the compiled model. Each engine runs the committed table repeated,
in a process of its own, as `run_sec.py --block` runs a block, each point projected and
then released. `net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,012 | 1.32 ms (7.96–8.11) | 2.26 ms (13.60–14.91) | 92 MB |
| export | 612 | 14.6 ms (8.95–9.36) | 15.8 ms (9.65–9.98) | 92 MB |
| modelx | 126 | 489 ms (61.65–62.67) | 579 ms (72.99–81.09) | 170 MB |

On `net_cf` the compiled model runs 11.1 times its export, and on `result_cf`, where
building the DataFrame takes much of its time, 7.0 times; it runs 370 and 256 times modelx.
A second run of the compiled model and the export straight after, under a 1-minute load
between 3.2 and 3.7, gave the compiled model 1.19 and 2.28 ms and the export 14.5 and 15.7
ms, 12.2 and 6.9 times. The compiled model takes about `MYGA_US_SEC`'s time a point, 1.19
ms, for an ItemSpace 1.35 times the size; of it, making and releasing the ItemSpace takes
about 0.14 ms. It runs about as many times its export as `MYGA_US_SEC`, 12.6, and
`UL_US_SEC`, 12.0, more than `Term_US_SEC`, 9.5, or `BasicTerm_SC` on its own measure, 8.7,
and fewer than `VUL_US_SEC`, 13.8. As it stood after running in force, compiled the same
way, the model ran 1.5 times as fast as its export (*What compiling changed, and why*,
above), and the compiled model runs about 19 times that build on the same measure, 1.19 ms a
point over the committed points against 22.4: the representation, not the compiler, is the
gain, and the export gained from it too, 13.9 ms a point against 33.5. The release keeps a
block flat: the compiled model's peak grew by less than 0.1 MB over its 6,012 points, and
without the collection after each release (`--no-collect`), 504 compiled points peaked at
1,601 MB. Reading the seven files and building every `Data` vector and array for those
points took 0.12 s, and asking every point for its frame, the runner's first pass, 0.86 s,
most of it making and releasing an ItemSpace a point.

Measured on 2026-11-13 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 3.1 and 5.1 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Each time is the fastest of three runs; under load the spread
is wide, and the fastest run is the one to compare. The comparisons over the committed
points, with the build as it stood after running in force, are the fastest of two runs of
three rounds each, in one process an engine, and so is the cost of an ItemSpace, the
fastest of five rounds of 1,000.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 2, 4, 5, 6, 8 and
  9, issued at the valuation date, every cell of `FIA_US_S`'s agrees at every argument
  `FIA_US_S` evaluates in its own sweep, the phases compared as their codes, but for
  `pols_if_init`, `model_point`, the five `_init` cells whose issue values the issue month
  credits instead, the four cells removed and `result_pols`, whose meaning changed. So the
  goldens `tests/test_fixed_indexed_annuity_us.py` asserts on those points hold here with no
  number restated, and those on its in-force points 1, 3 and 7, the worked example's among
  them, hold through the splice (below). The identity holds on any count, since `FIA_US_S`
  already takes the premium and charges acquisition on the contracts issued. The same suite
  holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, the in-force columns are present, and every
  month in cover sits in one of the four phases, `PRE_ISSUE` before it.
- **The splice**, in `tests/test_fixed_indexed_annuity_us_sec.py`: each `FIA_US_S` point
  restated in force at a month either side of its events continues the S projection, in
  `result_cf` and `result_pols`, column by column, and in every other cell the two share, to
  1e-9 relative with no absolute floor, the roll-forward residuals apart, which keep a floor
  of 1e-9, but those the twin identity skips and those a restated row changes by design:
  `proj_len`, a frame on the valuation clock; `anniv_mth` and `year_open_mth`, months on the
  valuation clock; `scenario_id`, which names the row's own scenario; `lw_pp_init`, the
  income the row carries where S's is its own column; and `result_cf_annual`, whose first
  row on a row restated mid-year is part of a contract year, its months each compared in
  `result_cf`. So do `FIA_US_S`'s own in-force points, 1, 3 and 7, opened at their month 84,
  so that the worked example's goldens, at `FIA_US_S`'s month 95, hold at `t = 11`. The
  anchor is restated at 60, 84, 95, the last month of contract year 8, 96, 144, 216 and 240,
  and `FIA_US_S`'s in-force points later in their lives, the anchor at 95, the simple rollup
  at 96 and the overdraw at 216. The other points are restated either side of their own
  events: the fixed account on its anniversary, in its year's last month and in income;
  joint life before its exercise, in the month of it and in income; the shock-lapse year,
  with the rider and without; the end of the growth window; the first policy year and the
  year of the pre-exercise withdrawal; and the last policy year, entered at 120, to its last
  covered month. Eight variants of S's points, in a copy of S's table that is never
  committed, carry what S's own points do not: the participation, spread and trigger
  crediting methods, the female table, a contract without the rider whose withdrawal empties
  it in accumulation and a withdrawal past the free amount but inside the account value, the
  programmes with input rows of their own; and the anchor exercising at 69, 79 and 80, so
  that with its own 70 and point 9's 85 a projection reads both sides of the 69/70 and 79/80
  payout band boundaries. Each spliced row runs on its own copy of its S scenario, re-based
  to its month, the scenarios stepped so that a level read at the wrong month or on the
  wrong clock reads another number; on a row valued mid-year the copy's level at `t = 0` is
  then moved off the year's opening level the row carries, so that a model reading the
  scenario there instead of the column parts from S. The mortality at age 120 is cut
  below 1, so that the last covered month has survivors to mature. Inflation, on the
  valuation clock, is set to 0 in both models; the assumptions that ship at zero, the index
  cost, the rider charge taken from the floor, the floor's $50 annual charge, the commission
  and the premium tax, are switched on in both; and the floor's rate is raised, so that it
  overtakes the surrender value. A second set of References, read into a pair of models of
  its own, switches what ships idle: the step-up at exercise only, the dollar rollup-base
  convention, the surrender-value collar, a no-rider shock lapse above the lapse cap, a
  rider charge above its cap, a fixed rate below its guaranteed minimum, a cap below its
  guaranteed minimum on a ninth variant, a credit floor raised to 0.1%, apart from the cap's
  floor, and a minimum exercise age above the income start age, each binding where it acts;
  and it puts the index cost back to its shipped 0, so that a trigger contract meets a flat
  index year at a net return of exactly 0, where it credits.
  An anniversary before the splice month is history on the restated row, which reads the
  level of the one that opened its year from its column, so the scenario's levels at earlier
  anniversaries are not compared.
- **The core grid and the full one.** By default the splice runs 12 of its 44 cases, the
  future business 5 of its 15 and the switched References 5 of their 9, which between them
  reach every branch, every opening-state column, every phase at the valuation date, every
  kind of valuation month and every switch the full grid reaches, and a test asserts that
  they do; line coverage of the two grids showed the default rows executing every line of
  `Projection`'s formulas that the full grid's rows execute. The other cases carry the
  `sec_full` marker and show as skipped, with the reason,
  unless `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so every CI run runs
  the full grid too.
- **Future new business**: four of S's points issued at the valuation date and the eight
  variants, each issued a month after it, and the anchor, the joint point and the
  pre-exercise programme, issued 15, 13 and 15 months after it, are each the S projection
  moved on, with zeros before issue in every report and every decrement rate the float 0.0
  there, and no table read at an age, a contract year or an anniversary the contract does
  not have. A point issued more than a year on reads contract year −1 before issue, which is
  what shows a missing guard.
- **How it computes**: on every row the splice and the future business compare, under both
  sets of References, after every report, no cell has been called at a negative month, none
  evaluated from `t_entry()` on has read a month before it, and none evaluated at month `t`
  has read a month later than `t + 1`, directly or through a cell keyed by a year or an age,
  but the surrender rate's reads at `anniv_mth(t)`, each admitted by reader, cell and month,
  inside the frame, with what it reads walked for a count, a decrement or a later month; no
  index level has been read at an anniversary before the year under way on the books, and no
  scenario level or reference yield at one before the books. On a fresh read of the
  committed model `duration_mth` is a closed form, and every point is swept under a
  recursion limit lowered to 400, which a recursion backward over the frame would exceed on
  every committed frame but the last policy year's. And a cold last-month call runs one cell
  a month back to `t_entry()` and at most 16 more, the count alone at most 11 more again, on
  the committed points and at issue age 40, at the valuation date and 120 months on.
- **Counts, validation and regeneration**: the roll-forward closes, `AFT_DECR` is the next
  month's `BEF_NB`, and `pols_if_at` refuses a timing it does not have; `result_pols()` is
  `FIA_US_S`'s, column for column, with `pols_new_biz` beside it; scaling `policy_count` by
  2.5, with the zero-shipped assumptions switched on, scales every cash flow and every
  counted cell and moves no per-contract value, and at a million contracts both roll-forward
  checks close on their scaled tolerance; each of 118 malformed model point tables is
  refused naming its column or its point, by the one check it is built for, as the table is
  read and through a projection, a key that the table it joins lacks among them, and a fault
  that breaks two checks by its nature by the earlier, which pins their order, every column
  of a check that reads its columns in turn refused at that column by a case of its own;
  each of 41 assumption tables whose keys or values cannot be read is refused naming the
  file and the lines, each repeated key and each missing key or span, by `Data` and by a
  projection that reads it; a crediting method, a rider basis, a step-up mode, a
  rollup-base convention and a collar basis that no decode knows each raise `FIA_US_S`'s
  own message, in both models; a scenario that starts after the first month a point on it
  is on the books is refused for that point, and read for a point issued no earlier; keys
  and integer columns written as floats are read by value; the horizon is a Reference,
  which refuses a point issued past it, at 0 any future business, saying so, and below 0
  itself; a point past its cover, or with none at all, is refused by `proj_len()`, while one
  in its last covered month, or issued at 101 under the shipped `maturity_age`, projects,
  and `run_sec.py --block` refuses such a point before printing anything; the edges of the
  interface, the first policy year's months 1 and 11 and the second year's first, amounts a
  part of a cent inside their tolerance, the indexed account 2.9 cents off, a blank joint
  age, a count of 0, and a lifetime withdrawal and a locked percentage of 0 in `INCOME` and
  in `DEPLETED`, each paying nothing at its next anniversary, are accepted; and the
  committed tables are what `FIA_US_S` generates, their text `FIA_US_S`'s or composed from
  its keys.
- **The opening state and the rest**: each derived row's opening state is what `FIA_US_S`
  carries into its month, and at the shipped assumptions each row in force, the twins of S's
  in-force points among them, is S's from that month on, in every cell but those expense
  inflation moves, so that the worked example's anniversary 8 is the anchor twin's `t = 11`
  cell for cell; each state column, changed, moves its committed row; the year under way
  reads its opening state; the phase is a code and the report keeps its labels; the rate
  scenario runs on the valuation clock and the withdrawals on the policy clock; expense
  inflation runs on the valuation clock at the shipped 2.5%, which only this test sees,
  since the splice sets the rate to 0; the premium, the commission, the premium tax and
  acquisition fall on new business alone, per contract issued, asserted at 2.5 contracts a
  point; the lapse rate reads the anniversary closing its year; a depleted row projects its
  whole frame at a zero account value; where `mort_ae_factor` takes the annual mortality
  past 1 both models cap it at `(float, 1.0)` and every contract in force dies, on new
  business, on a row restated the month before the cap and on one inside the capped year,
  and a NaN rate that reaches the cap stays NaN, as a NaN rider charge rate does at the
  rider charge's own cap, `FIA_US_S`'s `min(rider_charge_rate, rider_charge_rate_max)`,
  where a residual that is not a number fails its roll-forward check; under the guaranteed
  scale the twins of
  points 2, 4 and 9 are `FIA_US_S` cell by cell; each keyed reader returns `FIA_US_S`'s own
  lookup at every key the contract can ask for; every guarded cell holds its value outside
  cover and reads no rate there, and every monthly cell answers there; the points of a block
  sum row by row; an extract without the generator's three columns, labelled apart from its
  positions, projects the same numbers; the docstrings describe the valuation clock, the
  symbol map names every cell running in force adds, no row of a docstring's table runs into
  a column gap, and, where docutils is installed, every docstring parses without a warning;
  the model reads `FIA_US_S`'s tables in
  place, but for its model point table and its scenario companion; and `run_sec.py` prints
  the model's numbers, for the anchor in force, depleted and issued later, the block and a
  relabelled table, and writes "1 month" for a point a month either side of the valuation
  date.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py FIA_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their call
  syntax changed: a point's position for its label, the codes for the text of a timing, a
  kind, a scenario column or a switch, and `ALL` for `None`. Each point is named by its
  label, in `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: the two `ALL` totals are `FIA_US_S`'s `(t, None)` bit for
  bit, sign of a zero and type included, and with every kind set to −0.0 each total is
  −0.0, as `FIA_US_S`'s chain gives; every parameterless cell but the reporting ones
  returns a Python `int`, `float` or `bool`, not a numpy scalar (R11); a point issued below
  `issue_age_min` or above `issue_age_max`, and one whose sex the mortality table rates
  only below `maturity_age`, are refused by `proj_len()`, naming the point, and each
  projects once its bound is moved past it; a fixed rate in force, a `mgsv_rate` and an
  `inflation_rate` below −1 are refused by the cell that takes the power, naming the
  point, where `FIA_US_S` projects a complex number or raises `TypeError`, and at −1 both
  models project; each sex is read at its own ages, a rollup schedule that starts late
  rolls up nothing before it, and an age table with a band or an age below 0, or a
  mortality age far past any read, projects as `FIA_US_S` does; each value a decode names,
  written in another case or with a space beside it, is answered as `FIA_US_S` answers it,
  and a table without a decoded column is refused where `FIA_US_S` reads it; the `Data`
  vectors are int64 or float64 arrays and every extent an int; each array holds NaN where
  nothing is read; each size in `spec_sec.py` is the one its comment derives from the
  model's References, `Data.read_last_mth` and `Data.read_last_age` with them, and the
  sample's recursion limit the one its comment derives; the spec's `twin_arg_map` maps
  `FIA_US_S`'s totals and scenario columns onto the codes; and `run_sec.py` sums the block
  as `groupby` does, bit for bit, and outside the repository, beside a copy of the model or
  at a path too shallow to hold one, `run_sec.py --cython` says it cannot build, and in
  place it rebuilds exactly when no build is there or a source is newer than the build, and
  in place and from `--build DIR` it refuses a package whose `Projection` imports from
  `_mx_classes.py`, its extension module missing, on a fake product whose times are set
  and whose import is stubbed, building nothing.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting and engine ones refers to pandas, numpy, `math` or another
  module, reads a table with `.loc` or the like, calls a reporting or an engine cell,
  holds text but in its docstring and its refusals, or holds a generator, a comprehension,
  a tuple or a nested function; none calls anything but a cell, a `Data` vector and the
  builtins of *No Python call kept*, and the registry admits no other for this model;
  every `Data` vector a formula reads is an int64 or float64 array, read by element; no
  cell is uncached; and each label accessor returns its point's column of the same name.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting and engine ones a
  C `bint`, `long long` or `double` and a C-array cache of exactly the spec's size, and
  every new `Data` cell but a reader a typed memoryview or a C scalar, and the generated C
  keeps no Python object among a projection cell's locals, calls no Python builtin there,
  and builds no container, under both directives (C3); on the committed points, every cell
  at every argument a full modelx sweep caches is what modelx computes, bit for bit on
  x86-64, and so are every raise and every `Data` array (C4); and `run_sec.py --block`, run
  compiled, holds one point's ItemSpace at a time. In
  `tests/test_fixed_indexed_annuity_us_sec.py`: the same comparison, with the codes,
  readers and engine calls no report reaches, on the splice grid and under the switched
  References, the core by default and the full grid with `USLIB_SEC_FULL=1`; at the
  contract's extremes; where the caps bind; on labels that are not text and keys that are
  numbers; on tables written out of key order with their keys as floats; on keys far past
  any read; and on NaN sent through a Reference; the compiled model refuses what modelx
  refuses, with modelx's message, a divisor of zero and a negative power base among them,
  and an argument past a cache raises `IndexError`; the deepest calls the contract allows
  run cold on a 1 MiB stack and on the main thread, and the test reports the smallest of
  seven stacks, 256 KiB to 2 MiB, they ran on, waiting a bounded time for each; a Reference
  set after the model has computed changes no value it has cached; and `run_sec.py --cython`
  prints what `run_sec.py` prints, and refuses a `--build` directory that holds no build.
  Every case of more than four points, the committed points' among them, is compared four
  points at a time (`C4_CHUNK`), each its own case, so that a run holds one chunk's sweep.
  They are marked `cython`, and they skip without the toolchain, but in the `cython` CI job,
  which installs it on Linux and on Windows, one leg a product, a skip fails, whatever made
  it.

Measured here under load, the module's default run takes about 8 minutes without the
compile tests, and the compile tests on their own, the build included, as the `cython`
job's leg for this product runs them, about 18 minutes, of which the build and C3 take
3½.

```bash
python -m pytest tests/test_fixed_indexed_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_fixed_indexed_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k FIA_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k FIA_US_SEC
python -m pytest tests/test_fixed_indexed_annuity_us_sec.py -q -m cython  # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-fixed_indexed_annuity-r2
[std]: #uslib-std
<!-- END generated citation links -->
