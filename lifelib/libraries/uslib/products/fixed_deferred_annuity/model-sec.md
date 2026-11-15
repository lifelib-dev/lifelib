# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `MYGA_US_SEC` is [`MYGA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of their contract year, and contracts to be written in the
ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`.
The product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `MYGA_US_S` on another time axis, and it reads `MYGA_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced, the 4.45% declared
> rate, the 0.25% GMIR and the 2.80% GMSV rate from a rate sheet [S11] and the 9/8/7/6/5
> surrender charge and the 10% free withdrawal from a brochure [S10] among them. Every
> behavioural and expense assumption is a **[std]** standardization, the rate scenarios
> included, and the shipped mortality table is illustrative, *not* a published basis.
> Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/fixed_deferred_annuity/run_sec.py          # point 1, issued at t = 0
python products/fixed_deferred_annuity/run_sec.py 8        # the anchor, a year on
python products/fixed_deferred_annuity/run_sec.py --block  # every point, row by row
python products/fixed_deferred_annuity/run_sec.py 8 --cython  # point 8, compiled
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about two and a
half minutes, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and
`.gitignore` covers it.

The first prints, as rows `t = 0 … 11`, the twelve months `run.py` prints for
`MYGA_US_S`'s point 1, the worked example's first contract year, number for number. The
second prints point 8, the same contract valued on its first anniversary. Its row `t = 0`
is the worked example's month 12: the $4,000 free withdrawal taken from 104,450.00,
100,450.00 credited to 100,815.11, and the Model #805 floor at 86,148.02. Every column
agrees with `MYGA_US_S`'s months 12 to 23 but `expenses`, which are in valuation-date
dollars here, 4.09 in the first month where `MYGA_US_S` has 4.19, and `net_cf` with them.
Three lines to the same thing for point 8:

```python
import modelx as mx
model = mx.read_model("products/fixed_deferred_annuity/MYGA_US_SEC")
model.Projection[7].result_cf()     # point 8, the table's eighth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[7]` is point 8, and its `point_id()` says so. `result_cf()` has
`MYGA_US_S`'s eleven columns — `pols_if`, `premiums`, `withdrawals`, `claims_death`,
`claims_lapse`, `claims_annuitization`, `claims_maturity`, `commissions`, `expenses`,
`premium_taxes` and `net_cf` — with one row per month from the valuation date,
`t = 0 … proj_len() − 1`. `result_av()` has `MYGA_US_S`'s values per contract on the same
rows, the worked example's five columns and the surrender trace, with zeros before issue.
`result_pols()` sets out the counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then
the month's annuitizations, deaths and surrenders in processing order and the deemed
maturities of the last covered month, then `pols_if_aft_decr`, the notes' end-of-month
`l(t)`, as in `MYGA_US_S`.

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
  valuation month for every model point, however old the contract, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the deemed maturity at attained age 100.
- **`duration_mth(t)`, the policy clock**, counts the months the contract has been in
  force at time `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is the technical notes' month
  index, and the contract runs on it: `duration(t) = duration_mth(t) // 12`, the contract
  year `policy_year(t) = duration(t) + 1` and `age(t) = age_at_entry() + duration(t)`, as
  in `MYGA_US_S`, and the guarantee period containing month `t`,
  `gp_index(t) = duration_mth(t) // (12 n) + 1`. `BasicTerm_SE` reaches the same numbers
  by adding one a month, a recursion as long as the frame; the closed form needs no such
  chain of calls.

Point 8 is the anchor cell in force 12 months. At `t = 0` it is on its first anniversary,
opening contract year 2, at attained age 61, and the $4,000 withdrawal the contract takes
in policy month 12 falls there. Its shock-lapse year, contract year 6, opens at `t = 48`,
and its frame has 468 rows, `t = 0 … 467`. Point 12 is the stress trace in force 61
months, in contract year 6, the month after its first window: its renewal rate and its
MVA reference yield `i0`, fixed at policy month 60, the month before the valuation date,
come from its row, and its next window falls at `t = 59`. Point 14 is the anchor cell to
be issued 15 months after the valuation date: `duration_mth(0) = −15`, it is on the books
from `t_entry() = 15`, rows 0 to 14 are zeros, its $4,000 falls at `t = 27`, and its
frame has 495 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the initial term and each renewal period of `n` years, and the index, start and end of the guarantee period in force; the 30-day window in the first month of each renewal period, and the annuitization elected in it; the redeclaration months; the surrender charge schedules, their clock and the attained-age cap; the MVA term; the free-withdrawal years, the base each fixes and the reset at each anniversary; the scheduled withdrawals, whose `t` in `withdrawal_table.csv` is a policy month, and the free-withdrawal utilization in the first month of each contract year; the base lapse by contract year and the dynamic-lapse exponent; mortality at the attained age; the deemed maturity at attained age 100 | the rate scenario, the market rate `market_rate(t)` and the MVA reference yield `mva_ref_yield(t)`, whose `t` in `rate_scenario.csv` is a valuation month; expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

The rate scenario is a path in calendar time, shared by every contract of a block, so it
moves to `t`. A rate fixed in the past is a fact of the contract instead. The declared
rate of a renewal period is fixed at its redeclaration, the first month of each renewal
period under `rollover` and each anniversary after the initial term under
`annual_redeclare`, and `i0` at the start of each renewal period, which matters under
`rollover`, the one architecture with an MVA after the initial term. A rate fixed at or
after the valuation date is read from the scenario at the valuation month it is fixed in,
and one fixed before it from the opening state (below). Point 11, valued in its 30-day
window at policy month 60, takes its renewal rate, `max(GMIR, MR(0) − s_ren)` = 4.45%,
and its `i0`, 10.00%, from the stress scenario at `t = 0`; point 12, a month later, takes
both from its row. `redeclare_month(t)` and `gp_start_month(t)` still return policy
months, and `credit_rate` and `mva_ref_yield_locked`, the two cells that read them, turn
each into a valuation month once. Each shipped scenario is one row at `t = 0`, a flat
path, so no shipped number depends on the clock it is read on.

Expense inflation keeps `MYGA_US_S`'s annual step, `1.025^duration(t)`, but takes it every
twelve months from the valuation date rather than on the contract's anniversaries, so the
maintenance charge, $50 a contract a year, is in valuation-date dollars for every point
alike. Acquisition, `expense_acq` per contract issued and 0 as shipped, is charged in the
issue month and not inflated, as in `basiclife/BasicTerm_SE`, and so are the 2.00%
commission and the premium tax, on the premium of the contracts issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
n = len(model.Data.model_point_table())
frames = [model.Projection[i].result_cf() for i in range(n)]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`MYGA_US_S` computes, whatever the point's count: `MYGA_US_S` already takes the premium
and charges the commission and acquisition on the contracts in force at its `t = 0`,
which on new business are the contracts issued. On `MYGA_US_S`'s seven points every cash
flow, every count and every value per contract agrees, and so does every other cell the
two models share but five whose meaning changed: `pols_if_init()`, now the count already
in force at the valuation date, 0 for new business; `model_point()`, a row of another
table; `av_pp_init()` and `mgsv_pp_init()`, now the account value and the floor in force
entering month 0, 0 for new business, whose issue values are credited in the issue month
instead; and `result_pols()`, which gains `pols_new_biz`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `MYGA_US_S`'s columns,
and twelve of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s two, and
ten that open an in-force contract's state. Each of the twelve is a number, and every
amount is per contract.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the contract's age in months: positive in force, in any month of its contract year, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars, more than 0 in force | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value |
| `mgsv_pp_init` | dollars, possibly negative | the start of month 0 | the Model #805 floor [R1]: 87.5% of the premium, less each withdrawal as the contract's convention counts it and the monthly contract charge, accumulated at the GMSV rate |
| `prem_accum_gmir_pp_init` | dollars, possibly negative | the start of month 0 | `P_accum@GMIR`, the premium less prior withdrawals accumulated at the GMIR, which the `gmir_floor` MVA cap holds `AV + M` above [S13] |
| `interest_credited_pp_init` | dollars | the start of month 0 | the interest credited from issue, which the `min_sc_interest` MVA cap reads [S8] [S9] |
| `interest_credited_pp_prev_anniv_init` | dollars | the anniversary that opened the contract year under way, on or before the valuation date: the close of policy month `12 × duration(0) − 1` | the interest credited from issue to that anniversary, from which the interest-only allowance of the next contract year is measured [S5] [S6] |
| `free_wd_allow_init` | dollars | that anniversary | the free-withdrawal allowance of the contract year under way: `free_wd_rate`, 10% as shipped, of the account value at the anniversary under `pct_av` [S10]; the interest credited over the contract year before under `interest_only` |
| `free_wd_remain_init` | dollars | the start of month 0 | the part of that allowance the year's withdrawals have not used |
| `tax_basis_pp_init` | dollars | for a point in force, the start of month 0; for any other, issue | the IRC §72 investment in the contract [R6] |
| `credit_rate_init` | a rate a year, effective | the start of month 0: the rate credited in policy month `duration_mth − 1` | the declared rate in force |
| `mva_ref_yield_locked_init` | a rate a year | the start of month 0 | the MVA reference yield `i0` locked for the guarantee period in force |

On a point issued at or after the valuation date every one of the ten is 0 but
`tax_basis_pp_init`: such a contract opens with nothing, and its issue values arrive in
its issue month. `tax_basis_pp_init` is then the basis at issue, as `MYGA_US_S`'s
`tax_basis_initial` is, which varies with tax status: the premium on every shipped point,
all of them non-qualified, and 0 for a qualified contract. In the first contract year,
`duration_mth` 1 to 11, the year opened at issue, so `interest_credited_pp_prev_anniv_init`
is 0 and `free_wd_allow_init` is the issue allowance, `free_wd_rate` times the premium
under `pct_av` and 0 under `interest_only`. On a point valued on an anniversary,
`duration_mth` a positive multiple of 12, the anniversary that opened the year is the
valuation date itself: the interest to it is `interest_credited_pp_init`, and under
`pct_av` the year's allowance is `free_wd_rate` times `av_pp_init`. The remainder carried
into such a month is last year's, which lapses at the anniversary unread, the allowance
being non-cumulative [S4] [S16]. Entering any month of the initial term, `duration_mth` 1
to 12 `n`, the first renewal month included, the declared rate and `i0` are still the
issue values, `declared_rate_initial` and `mva_ref_yield_at_issue`. `prev_anniv` is the
anniversary that **opened** the contract year: an extract that fills the two anniversary
columns from the anniversary after the valuation date is a year out.

Each column is read where the contract needs it, and only there:

- `free_wd_allow_init` on a valuation on an anniversary, where month 0 opens the year and
  the allowance resets to it, as on points 8 and 11. Off an anniversary the remainder
  carries the year, and only `Data`'s check that the remainder does not exceed the year's
  allowance reads this column. Each later year's allowance is fixed in the frame.
- `free_wd_remain_init` off an anniversary, the remainder `free_wd_avail(0)` opens from.
- `interest_credited_pp_prev_anniv_init` under `interest_only` alone, by the allowance of
  the year after the one under way.
- `interest_credited_pp_init` under the `min_sc_interest` cap and the `interest_only`
  allowance, and `prem_accum_gmir_pp_init` under the `gmir_floor` cap.
- `credit_rate_init` wherever the declaration in force was made before the valuation date,
  and `mva_ref_yield_locked_init` wherever a linear-duration or geometric MVA applies in a
  renewal period that started before it. The declared-differential MVA reads no `i0`, and
  under `annual_redeclare` no MVA applies after the initial term, so there the column is
  carried unread.
- `tax_basis_pp_init` by `tax_basis_pp` and `taxable_wd_pp`, which are reported and drive
  no cash flow.

Everything else the projection uses is fixed at issue, in `MYGA_US_S`'s columns, or follows
from the policy clock. The guarantee-period position, the surrender-charge clock, the
window, the base lapse and the attained age all derive from `duration_mth` alone, because
every renewal period is `n` years, as in `MYGA_US_S`.

| `MYGA_US_S` | `MYGA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months. Every `MYGA_US_S` point is new business, opening its frame at issue |
| `tax_basis_initial` | `tax_basis_pp_init` | Renamed in place, after the cell that reads it, so that the ten state columns share one vocabulary; on new business it keeps its meaning, the basis at issue |
| `av_pp_init()` computes `P (1 − load)` | `av_pp_init` | The notes' `av_initial`: the issue value is still computed by its rule, now in the issue month (`prem_to_av_pp`), and the cell reads the account value in force |
| `mgsv_pp_init()` computes `0.875 P` | `mgsv_pp_init` | The notes' `mgsv_initial`, the same way (`prem_to_mgsv_pp`) |
| — | `prem_accum_gmir_pp_init` | `MYGA_US_S` opens `P_accum` with the premium at `t = 0` |
| — | `interest_credited_pp_init` | `MYGA_US_S` opens the interest credited at 0 |
| — | `interest_credited_pp_prev_anniv_init` | `MYGA_US_S` reads the interest at each anniversary from its frame, which starts at issue |
| — | `free_wd_allow_init` | `MYGA_US_S` fixes every year's allowance in its frame |
| — | `free_wd_remain_init` | `MYGA_US_S` resets the allowance at `t = 0`, its issue anniversary |
| — | `credit_rate_init` | `MYGA_US_S` reads every declared rate from the scenario, at its redeclaration month |
| — | `mva_ref_yield_locked_init` | `MYGA_US_S` reads every `i0` from the scenario, at the start of its period |

A column measured entering month 0 is the cell it opens with `_init` added, and so is
`free_wd_allow_init`, the value `free_wd_allow` returns for the contract year under way; a
balance measured at the anniversary adds `_prev_anniv_init`. `free_wd_remain_init` takes
no `_ytd`: it is not an accumulator restarting each year but the remainder of an annual
allowance, which each anniversary resets.

On the twins the nine columns other than `tax_basis_pp_init` are 0, the state of a
contract entering its issue month, and `tax_basis_pp_init` is the S row's
`tax_basis_initial`, so each twin takes its issue values in month 0, as its S row does.

The columns carried over are read as `MYGA_US_S` reads them. For a contract in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `tax_status` | codes, as in `MYGA_US_S`'s table | issue |
| `premium` | dollars, the single purchase payment | issue |
| `guar_period` | years, the initial term and each renewal period | issue |
| `declared_rate_initial`, `gmir`, `mgsv_rate` | rates a year, effective | issue: the initial term's rate, the guaranteed minimum and the GMSV accumulation rate |
| `mgsv_annual_charge` | dollars a year | issue |
| `mgsv_wd_convention`, `renewal_architecture`, `free_wd_rule`, `mva_family`, `mva_cap_rule` | codes, as in `MYGA_US_S`'s table | issue: the contract's provisions |
| `free_wd_mva_exempt` | a flag, `True` or `False` | issue |
| `free_wd_rate` | a fraction of the free-withdrawal base | issue |
| `mva_ref_yield_at_issue` | a rate a year | issue: `i0` for the initial term |
| `premium_tax_rate` | a fraction of the premium | issue |
| `scenario_id`, `wd_schedule_id` | keys into `rate_scenario.csv` and `withdrawal_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `MYGA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the twelve in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `age_at_entry` and `guar_period` are whole numbers of years: `MYGA_US_S` reads both by
  `int()`, which would truncate a fraction without a word, and the initial-term check
  below reads `guar_period` as written;
- `guar_period` is 1 year or more: at 0 the guarantee-period index divides by zero,
  naming no point, and below it the projection runs a period no contract has;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,320 months at issue age 0, the youngest the product
  issues, and 840 at 40, the youngest the shipped mortality table carries. Set to 0, the
  Reference refuses future new business altogether, and a negative horizon is itself
  refused;
- the account value, the two interest columns, the allowance, the remainder and the basis
  are each a finite number, zero or more;
- the floor, `P_accum`, the declared rate and `i0` are each a finite number;
- a contract not yet in force, `duration_mth` 0 or less, has an opening state of zeros,
  `tax_basis_pp_init` apart;
- a contract in force has an account value above 0: one fully withdrawn is no longer in
  force, and the dynamic lapse, which reads the surrender benefit as a share of the
  account value, has nothing to divide by;
- in the first contract year the interest at the anniversary is 0;
- in the first contract year the allowance is the issue allowance;
- on a point valued on an anniversary the interest at the anniversary equals the interest
  entering month 0;
- the interest at the anniversary does not exceed the interest entering month 0;
- under `interest_only`, from the second contract year on, the year's allowance, the
  interest credited over the year before, does not exceed the interest credited to the
  anniversary that opened the year, and in the second year it is that interest, the first
  year's;
- off an anniversary the remainder does not exceed the year's allowance;
- entering a month of the initial term, the first renewal month included, the declared rate
  and `i0` are `declared_rate_initial` and `mva_ref_yield_at_issue`;
- after it, the declared rate is the GMIR or more;
- on a point valued on an anniversary under `pct_av`, the year's allowance is
  `free_wd_rate × av_pp_init`;
- last, each point's keys into the tables it is joined with: its `scenario_id` is a
  scenario of `rate_scenario.csv` that sets its levels by the first month the point is on
  the books, `t = 0` or its issue month if later; its `wd_schedule_id` is a programme of
  `withdrawal_table.csv`; and `mort_table.csv` gives a rate at its `sex` and its attained
  age in that first month. So reading the model point table reads those three tables,
  checked. `MYGA_US_S` meets a key its table lacks only as it projects: a missing
  scenario, sex or age raises Python's own error, naming no file, and a missing
  withdrawal programme takes no withdrawal, without a word.

Amounts of money are compared to a cent, so an extract may carry each column to the cent,
as an administration system holds it. Each amount so carried is within half a cent of its
exact value, so a rule that holds between the exact amounts can miss by half a cent from
each: from the allowance, and from the account value or the premium it is a share of,
scaled by `free_wd_rate`, 0.0055 in all at the product's 10%. A cent holds every such pair
with room for the floating-point error of the comparison, where half a cent left the ties
to that error: point 11's allowance and account value, 12,432.034927 and 124,320.349270,
carried as 12,432.03 and 124,320.35, are 0.005 apart, and so is an issue allowance carried
as 864.18 or 864.19 at 7% of a premium of 12,345.50, which is 864.185. So are read an
allowance of 10,445.00 on an account value of 104,449.99, whose 10% is 10,444.999 in
floating point, and an issue allowance of 7,000.00 at a `free_wd_rate` of 7% of 100,000,
which in floating point is 7,000.000000000001. A stale allowance, last year's or a dollar
out, is still refused. The projection then starts from the allowance as carried. The
generated rows carry `MYGA_US_S`'s own values, unrounded.

Accepted, because a contract can be in each state: a negative floor or `P_accum`, since
every withdrawal is deducted from both and nothing floors either, in either model; any
basis at issue, zero or more, on a contract not yet in force, 0 for a qualified one; on a
point valued on an anniversary, a remainder above the year's allowance, last year's; and
a `duration_mth`, an `age_at_entry` or a `guar_period` written as a float, read as the
whole number it holds.

Left to the projection: a sex the mortality table rates only to an attained age below the
last covered month's, `maturity_age − 1`, because the maturity age is a `Projection`
Reference, which `Data` cannot read. `proj_len()` refuses such a point against the table's
last age for the sex, where `MYGA_US_S` raises a `KeyError` once the projection reaches the
age; the shipped table runs to 120, past every contract's cover. So is the issue age the
product admits, 0 to 85, `Projection.issue_age_min` and `issue_age_max` (*The compiled
model*, below).

The six assumption tables are `MYGA_US_S`'s, read in place by `MYGA_US_S`'s readers, and
their keys are checked as well. Beside each reader a `Data` cell reads the table's keys by
value, once, checks them and the table's values, and returns the table indexed by the
checked keys: `mort_rates`, `surr_charge_scales`, `surr_charge_age_caps`,
`rate_scenario_steps`, `wd_schedules` and `mva_factors`. Every array the projection reads
of the table is built from that cell and nowhere else (*The compiled model*, below), and
the extents that bound the reads, the age cap's first and last ages, the duration
factors' last year, each sex's ages and each scenario's months among them, are taken from
the same checked keys. A key written `1.0` is 1, as
`MYGA_US_S`'s lookups match it. A key that is not a whole number, text and a blank among
them, a blank text key, a rate or an amount that is not a number in its range, a repeated
key, and keys that leave a gap where the projection reads every year or age between a
table's first and last are refused, naming the file, the column and the lines, before a
projection reads a value from the table, and so is a surrender charge table without the
`initial` and the `renewal` schedules, the two `surr_charge_id` names, where `MYGA_US_S`
reads a schedule it cannot find as no charge, so that one spelt `Renewal` would leave
every renewal period free of charge. A scenario may start after `t = 0`, for business
issued later, so the month it must start by is the point's, which the model point table's
last checks hold. `MYGA_US_S` takes the keys as pandas reads them: one written as text
turns its column to text, every lookup on it misses, and a surrender charge or a
withdrawal is then zero without a word, the age cap vanishes, or a lookup raises an error
that names no file.

A point whose cover had ended by the valuation date,
`duration_mth ≥ 12 × (100 − age_at_entry)`, reads, but `proj_len()` refuses it, naming the
point: the end of cover is the product's rule, not the table's. So are the issue ages the
product admits, 0 to 85: `proj_len()` refuses a point issued below `issue_age_min` or above
`issue_age_max`, `point_id 3: issue age 86 is above issue_age_max, 85`. So a loop over the
block meets such a row only when it reaches it, after projecting the points before it.
`run_sec.py --block` asks every point for its frame before it projects any, and stops before
it prints anything.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`MYGA_US_S` and its table by `tests/sec_support.py`, from the `MYGA_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `MYGA_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py MYGA_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–7 | twin | S points 1–7 | issued at `t = 0`: `MYGA_US_S`'s seven contracts — the worked example's anchor cell, the stress trace, Camp B with the GMIR-floored MVA, the registered-contract conventions, the interest-only, net-of-charges point under the interest-credited cap with its $20,000 excess withdrawal at policy month 29, the asymmetric cap and the declared-differential MVA |
| 8 | derived | S point 1 at S month 12 | the anchor on its first anniversary, with year 2's allowance of 10,445.00, under which its $4,000 at `t = 0` is free |
| 9 | derived | S point 5 at S month 30 | the month after its excess withdrawal, which used up contract year 3's interest-only allowance of 4,648.02: an account value of 91,426.34, the floor net of charges at 75,862.37, 11,426.34 of interest to date and 9,098.02 to the anniversary, and a basis of 91,095.23 |
| 10 | derived | S point 3 at S month 30 | Camp B halfway through contract year 3 of its initial term, with a `P_accum` of 100,626.17, which its GMIR-floored MVA reads |
| 11 | derived | S point 4 at S month 60 | the registered-contract point in its 30-day window at `t = 0`: no surrender charge, no MVA, the annuitization election, and the rate redeclared and `i0` re-locked from the scenario at `t = 0` |
| 12 | derived | S point 2 at S month 61 | the stress trace in the month after its window, in its shock-lapse year, with the renewal rate of 4.45% and the `i0` of 10.00% fixed at policy month 60 |
| 13 | derived | S point 3 at S month 479 | Camp B in its last covered month, a one-row frame ending at the deemed maturity, with the rate declared at policy month 468 |
| 14 | future | S point 1, 15 months on | to be issued at `t = 15` |

A derived row's `policy_count` is the count `MYGA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `MYGA_US_S` carries into it, each column read
as `MYGA_US_S`'s own formulas read it: the account value, the floor, `P_accum`, the
interest credited, the remainder and the basis at the close of S month `d − 1`; the
declared rate and `i0` S credits and holds in that month; the interest at the close of S
month `12 × duration(d) − 1`, the anniversary that opened the contract year of `d`; and
S's allowance of that year, its `free_wd_allow(policy_year(d))`. So the row continues the
S projection from there: point 8 opens with 0.982074 contracts, points 9 and 10 with
0.954660, point 11 with 0.907698, point 12, a month into its 90% shock-lapse year, with
0.741165, and point 13 with 0.001064. Its `policy_id` is the S row's with the month
appended, `MYGA-000001-M12`, and a future row's carries the months to issue,
`MYGA-000001-F15`. Row `t` of a generated point is month `t + source_mth` of its S point.
All fourteen are the anchor cell's male 60, non-qualified, $100,000 contract with a
five-year guarantee period, as every `MYGA_US_S` point is; the shipped mortality table
starts at attained age 40, so a point issued younger needs it extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order:

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements, the
  notes' `l(t−1)`;
- `BEF_MORT`, after the month's annuitization elections;
- `BEF_LAPSE`, after its deaths;
- `AFT_DECR`, after its surrenders, the notes' end-of-month `l(t)`.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `MYGA_US_S`'s, unchanged
but for their guard outside cover. `BEF_DECR` already meant in `MYGA_US_S` what it means
in `BasicTerm_SE`, and `BEF_MORT` is "before mortality", not `BasicTerm_SE`'s
`"BEF_MAT"`, so no name clashes, and `BEF_NB` is the one timing running in force adds.
Any other timing raises.
`BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a month before its maturities, is
not adopted: the contracts here mature at the end of the last covered month, as
`pols_maturity`, where `MYGA_US_S`'s goldens put the deemed maturity.

The survivors carried into month `t` are those of month `t − 1`'s `BEF_DECR` count,
which `BEF_NB` forms itself, as its own value at `t − 1` plus that month's new business,
through the month's annuitizations, deaths and surrenders in the order `AFT_DECR` takes
them. So `pols_if_at(t, AFT_DECR)` is `pols_if_at(t + 1, BEF_NB)` in every month but
the last covered one, where the deemed maturity empties the block, and it is
`pols_if(t + 1)` except where month `t + 1` is an issue month, whose new business joins
`pols_if`. The chain of calls from month `t` back to `t_entry()` is one cell a month,
where `MYGA_US_S`'s count ran through two, and so are the account value's, which ran
through three, and the free-withdrawal carry's, which ran through two. A cold `net_cf` in
the last month of a 480-month frame runs 494 cells deep on a model just read, and 495 on
point 3, whose GMIR-floored MVA reads `P_accum`'s chain too, against 1,437 in
`MYGA_US_S`, so modelx needs a recursion limit of 493 for it, as `mx.set_recursion`
takes it, and 494 on point 3. At issue age 0, the contract's longest cover from issue,
1,200 months, on a copy whose mortality is extended below the table's age 40, it runs
1,214 to 1,215 deep, issued now or 120 months on, and a point issued later runs no deeper
than its cover, because its chain stops at its issue month. The deepest head there is the
account value's residual, `check_av_roll_fwd_resid`, cold in the last month, 1,216 deep on
an interest-only, GMIR-floored point, the cover and 16 more, the bound a test holds it
to.
Each report evaluates its columns in ascending `t`, and a sweep of the committed points
that way runs under a recursion limit of 15. The compiled model runs the same chains on
the C stack (*The compiled model*, below).

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `MYGA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_annuitization(t) + pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `MYGA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing account value, `av_at(t, EOM)`, is weighted
by `pols_if_at(t + 1, BEF_NB)`. Both roll-forward checks scale their tolerance with
`policy_count`, since a residual is rounding on that many contracts.

The premium, the commission, the premium tax and acquisition fall on `pols_new_biz(t)`,
in the issue month: `t = 0` on the twins, `t = 15` on point 14, and never on a point
already in force, which paid its premium before the valuation date. `MYGA_US_S` puts them
at `t = 0` on `pols_if_init()`, the contracts issued, so on a twin they are the same at
any count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × (100 − age_at_entry)` is `MYGA_US_S`'s frame from issue. Outside
it, before issue and from the deemed maturity on, every count is zero, and so every cash
flow and every value per contract. No count evaluates a decrement rate there, and no table
is read at a contract year or an attained age the contract does not have:
`in_gp_window` and `mva_in_force` are false, and the declared rate, `i0`, mortality, the
surrender charge and its age cap, the MVA term and duration factor, the base and dynamic
lapse terms, the floor's charge and the scheduled withdrawals are zero before any table or
rate is read. The dynamic-lapse ratio of the surrender benefit to the account value would
be 0/0 there, and the lapse rate's clamp would give its 0.5% floor.

## The opening state

`MYGA_US_S` projects new business only, so its frame always opens at issue, from the
premium and the two rules the notes state for the account value and the floor. A contract
valued in any month of its life needs all ten state columns, each what `MYGA_US_S` carries
into that month, and each shows on a derived row:

- **`free_wd_allow_init`.** Point 8, the anchor valued on its first anniversary, carries
  year 2's allowance, 10% of its account value there, 104,450.00: 10,445.00. Month 0
  resets the allowance to it, so the $4,000 withdrawal at `t = 0` is free of surrender
  charge and MVA and leaves 6,445.00 for the year, as in `MYGA_US_S`'s month 12. `Data`
  holds the column on such a row under `pct_av` to 10% of the account value, to a cent:
  an extract carrying year 1's allowance of 10,000.00, read before the anniversary, is
  refused, and one carrying 10,445.004 projects from 10,445.004, the column, not the
  product. The point's remainder, 10,000.00, is year 1's and lapses unread. On an
  interest-only contract valued on an anniversary the allowance is the interest credited
  over the year before, which no value at the anniversary gives: `MYGA_US_S`'s point 5 at
  its month 12 would carry its first year's interest, 4,450.00, which is also the interest
  to the anniversary, and `Data` holds the column to it in the second contract year. From
  the third year on the allowance is the interest of one year out of several, which no
  other column gives, and `Data` refuses only an allowance above the interest credited to
  the anniversary.
- **`interest_credited_pp_init`.** Point 9, under the interest-credited cap, is valued at
  month 30 with 11,426.34 credited since issue. The cap holds the MVA on a surrender to the
  lesser of the surrender charge and the interest credited to date: at `t = 0` the
  charge, 6,423.11, is the lesser, so the MVA is −6,423.11 and the surrender benefit
  78,912.44. With both interest columns at 0, and year 3's allowance at 0 with them, the
  interest to date would be month 0's alone, 332.31, and the surrender benefit 85,003.23.
- **`interest_credited_pp_prev_anniv_init`.** Point 9 credited 9,098.02 to its second
  anniversary. Its contract year 4, from `t = 6`, has the interest credited over year 3
  as its allowance: 13,438.44 credited by `t = 5` less those 9,098.02, so 4,340.41. With
  the column at 0, and year 3's allowance at 0 with it, since that allowance cannot
  exceed the interest to its anniversary, the allowance would be every dollar credited
  since issue, and the surrender charge on a lapse at `t = 6` would fall from 5,366.26 to
  4,820.38.
- **`free_wd_remain_init`.** Point 9 has nothing left of year 3's allowance of 4,648.02:
  the $20,000 at policy month 29 used it. So a surrender at the end of month 0 is charged
  on the whole account value, 7% of 91,758.65, or 6,423.11. Had the year's allowance been
  left whole, it would shelter 4,648.02, and the charge would be 6,097.74.
- **`prem_accum_gmir_pp_init`.** Point 10, Camp B under the GMIR-floored cap, carries
  100,626.17. The cap holds `AV + M` at or above `P_accum`: at `t = 0` it lifts the MVA
  from its raw −12,203.50 to `P_accum − AV`, −11,257.20, and the surrender value from
  92,631.19 to 93,577.50. With the column at 0 the cap would not bind. In months 0 to 2
  the Model #805 floor binds as well, so the surrender benefit is the floor, 93,970.22 at
  `t = 0`, either way.
- **`mgsv_pp_init`.** That floor opens from point 10's 93,754.22 entering month 0. With the
  column at 0 a lapse at `t = 0` would receive the surrender value of 93,577.50 rather
  than the floor. Point 9's floor, 75,862.37, is net of charges: the $20,000 reduced it by
  the 17,850.72 actually paid, its MVA and its charge deducted.
- **`av_pp_init`.** Every point in force opens its account value from it, at `t = 0`:
  point 9's 91,426.34 is what its $20,000 at policy month 29 left, with that month's
  interest. Halved, to 45,713.17, it closes month 0 at 45,879.33. A contract in force has
  an account value above 0, and `Data` refuses 0: one fully withdrawn is no longer in
  force.
- **`tax_basis_pp_init`.** Point 8's basis is the premium, 100,000.00, with nothing
  withdrawn before its first anniversary, so the $4,000 at `t = 0` is taxable in full,
  income first: the account value exceeds the basis by 4,450.00. With the basis at the
  account value it would be none. Point 9's 91,095.23 is the premium less the 8,904.77 of
  its $20,000 withdrawal that was not gain. The basis drives no cash flow.
- **`credit_rate_init`.** Point 12's renewal rate, 4.45%, was declared at policy month 60,
  the month before the valuation date, and `credit_rate` reads it from the row through
  `t = 58`, policy month 119; at `t = 59`, its next window, the rate is redeclared from
  the scenario. With the column at the GMIR, 0.25%, the least `Data` accepts there, the
  account value at `t = 58` would be 126,313.41 instead of 154,555.49. Point 13 reads its
  rate, declared at policy month 468, from its row too. Point 11, valued in its window,
  redeclares at `t = 0` from the scenario, and its column, the initial rate entering
  month 60, is unread.
- **`mva_ref_yield_locked_init`.** Point 12's `i0`, 10.00%, was locked at policy month 60
  at the stress scenario's yield. At the scenario's current 10.00% the MVA is zero; had `i0`
  been locked at 8%, a surrender at `t = 0` would carry an MVA of `(8% − 10%) × 4.83` years
  on the excess, −10,903.39, capped at the charge, −5,639.69. On point 11 the period starts
  at `t = 0` and `i0` is locked from the scenario, and on point 13, Camp B past its initial
  term, no MVA applies and the column is carried unread.

`MYGA_US_S`'s `av_pp_init()` and `mgsv_pp_init()` compute the issue values,
`P (1 − load_prem_rate)` and `0.875 P`, because, as [`model.md`](model.md) says, shipping
them as data would let a model point silently violate the statute [R1]. The rules are
kept, and moved: `prem_to_av_pp(t)` credits `P (1 − load_prem_rate)` and the new
`prem_to_mgsv_pp(t)` credits `net_consideration_ratio × P` in the month with
`duration_mth(t) = 0`, and `P_accum` takes the premium there too. The cells that bear the
notes' names for the opening values, `av_pp_init()` and `mgsv_pp_init()`, read the opening
state instead, 0 on new business, as `pols_if_init()` does for the count.

The allowance of the year under way is carried rather than the account value at the
anniversary it was fixed on, because the account value gives only the `pct_av` allowance.
The interest-only allowance is the interest credited over the year *before* the one under
way, on an anniversary valuation `I(d − 1) − I(d − 13)`, which needs the cumulative
interest two anniversaries back. Carrying the allowance covers both rules with one
column, and the account value at the anniversary is then needed by nothing.

## Departures from MYGA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock or of the opening
state, and every recursion begins at `t_entry()`. Where `MYGA_US_S`'s test would have
stayed correct on the valuation clock, it moved anyway, so that cover has one definition.
Of `MYGA_US_S`'s 127 cells, 53 are unchanged, 13 have a new docstring only and 61 are
rewritten; none is renamed or removed, and 30 cells are new, 157 in all. Compiling then
changed how each cell reads its inputs and spells its codes, and no number: it took away
two of `MYGA_US_S`'s cells, `mva_pp_on` and `mva_factor_geometric`, each written inline in
the cells that call it, and one of its own, `mva_factor_at`, and added six, 160 in all
(*The compiled model*, below); of `MYGA_US_S`'s cells it changed the signature of two,
`claims` and `claims_over_av`, whose total is the code `ALL`, and the value of one,
`surr_charge_id`, a code where `MYGA_US_S` returns the schedule's name. The twin identity
exempts the two cells taken away and `surr_charge_id`, each with its reason, compares
`MYGA_US_S`'s `(t, None)` with `(t, ALL)`, and reads every timing, kind and column at its
code: a cell of `MYGA_US_S`'s that this model lacked, or took other arguments, would fail
it otherwise.

| Cells | `MYGA_US_S` | `MYGA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration`, `policy_year` | `t`, `t // 12`, `t // 12 + 1` | `duration_mth_init() + t`, and the other two on `duration_mth(t)` | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth` | `12 × (100 − x)`, the months from issue | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises at or past maturity, on a point issued below `issue_age_min`, 0, or above `issue_age_max`, 85, and on one whose sex the mortality table rates only below `maturity_age − 1` | The frame starts at the valuation date. `maturity_mth()` is new and keeps `MYGA_US_S`'s formula. A point with no month left has no frame, nor one the product does not issue, and the compiled caches hold the contract's frames alone; the mortality's last age is a bound `Data` cannot check, `maturity_age` being a `Projection` Reference |
| `gp_index`, `gp_end`, `in_gp_window`, `redeclare_month`, `mva_term` | arithmetic and tests of `t` against `12n` | the same of `duration_mth(t)`; `redeclare_month` still returns a policy month | The guarantee periods, their windows and the redeclarations are on the policy clock |
| `pols_if`, `pols_if_init`, `pols_if_at` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`, two cells a month | `pols_if_at(t, BEF_DECR)`, from `t_entry()`, one cell a month, with `BEF_NB` added; `pols_if_init()` is 0 unless in force | Contracts in force at the valuation date open the count; new business joins it in its issue month |
| `av_pp`, `av_pp_at` | `av_pp(t)` through `av_pp_at` at `"BEF_INV"` and `"BEF_WD"`, three cells a month, from `av_pp_init()` at `t = 0` | the opening written in both, `av_pp(t − 1)`, or `av_pp_init()` at `t_entry()`, plus the premium credited in the issue month | One cell a month. The values are `MYGA_US_S`'s bit for bit |
| `av_pp_init`, `mgsv_pp_init` | compute the issue values, `P (1 − load)` and `0.875 P` | read the in-force columns, 0 on new business | The issue values stay rules, crediting the issue month (`prem_to_av_pp` and the new `prem_to_mgsv_pp`) |
| `prem_to_av_pp`, `mgsv_pp`, `prem_accum_gmir_pp` | the premium credited, the floor's 87.5% and `P_accum`'s premium at `t = 0` | in the month with `duration_mth(t) = 0`, on top of the opening state from `t_entry()` | A contract's issue values arrive in its issue month, whenever that is |
| `interest_credited_pp`, `tax_basis_pp`, `taxable_wd_pp` | open at `t = 0` from 0 and from `tax_basis_initial` | open at `t_entry()` from `interest_credited_pp_init()` and `tax_basis_pp_init()` | Every recursion begins on the books, from the opening state |
| `tax_basis_pp_init` | reads `tax_basis_initial` | reads the same column, renamed `tax_basis_pp_init` | One vocabulary for the opening state |
| `free_wd_avail` | reset where `t % 12 = 0`; carried as `free_wd_remain(t − 1)`, two cells a month | reset where `duration_mth(t) % 12 = 0`; carried as `free_wd_avail(t − 1) − wd_free_pp(t − 1)`, one cell a month, from `free_wd_remain_init()` at `t_entry()` | The contract year is on the policy clock, and the remainder carried into the valuation date is opening state |
| `free_wd_base` | `av_pp_at(12 (y − 1), "BEF_WD")`, a policy month passed as `t` | `av_pp_at(12 (y − 1) − duration_mth_init(), BEF_WD)`, asked only for a year that opens on the books | On the valuation clock month `12 (y − 1)` is not the anniversary that opens year `y` |
| `free_wd_allow` | the interest credited to the ends of months `12 (y − 1) − 1` and `12 (y − 2) − 1`, policy months passed as `t` | the same months as valuation months; the year under way from `free_wd_allow_init()`, and the interest at the anniversary that opened it from `interest_credited_pp_prev_anniv_init()` | The same, and a year that opened before the valuation date is opening state |
| `credit_rate` | `market_rate(redeclare_month(t))`, a policy month passed as `t`; the initial rate while `t < 12n` | `market_rate(m)`, `m = redeclare_month(t) − duration_mth_init()`, or `credit_rate_init()` where `m` is before `t_entry()`; the initial rate while `duration_mth(t) < 12n` | A rate declared before the valuation date is a fact of the past, and one declared after it is read on the valuation clock |
| `mva_ref_yield_locked` | `mva_ref_yield(gp_start_month(t))`, a policy month passed as `t` | `mva_ref_yield(m)`, `m = gp_start_month(t) − duration_mth_init()`, or `mva_ref_yield_locked_init()` where `m` is before `t_entry()` | The same, for the yield locked at the start of the period |
| `wd_scheduled_pp`, `wd_pp` | the withdrawal table at `(wd_schedule_id, t)`; the utilization where `t % 12 = 0` | at `(wd_schedule_id, duration_mth(t))`; the utilization where `duration_mth(t) % 12 = 0` | Withdrawals stay on the policy clock |
| `in_gp_window`, `redeclare_month`, `surr_charge_id`, `mva_term`, `lapse_rate_base`, `free_wd_allow`, `mva_rate`, `mva_pp_on`, `mgsv_wd_deduct_pp` | branch on the text of `renewal_architecture()`, `free_wd_rule()`, `mva_family()`, `mva_cap_rule()` and `mgsv_wd_convention()` | branch on the new `is_*` cells, one bool for each value `MYGA_US_S` tests, each read from a 0/1 vector `Data` decodes from the column; a value `MYGA_US_S` does not know is answered as there | No projection cell compares text or calls a label accessor, which are left to reporting. The timing and kind strings, and the schedule `surr_charge_id(t)` names, are codes (*The compiled model*, below) |
| `mort_rate`, `surr_charge_rate`, `surr_charge_age_cap_at`, `scenario_rate`, `wd_scheduled_pp`, `mva_duration_factor` | read `MYGA_US_S`'s readers' tables, and take the age cap's and the duration factors' extents by `int()` of the raw keys | read `Data`'s arrays, each built from a checked table, `mort_rates`, `surr_charge_scales`, `surr_charge_age_caps`, `rate_scenario_steps`, `wd_schedules` or `mva_factors`, and the extents from the same checked keys; the joins on text keys are rows `Data` numbers each point's key by; the mortality is read through the new `mort_rate_at(a)`, keyed by the attained age, and the duration factors at the whole years `mva_term_years(t)` computes; a month before the scenario's first, and an attained age outside the table's for the point's sex, are refused, naming the point | A key the table cannot be read by is refused by name before a value is read, every table is read through one cell, and a compiled cell reads no table but an array |
| `premiums`, `prem_to_av` | at `t = 0`, on `pols_if_init()` | on `pols_new_biz(t)` | A point in force paid its premium before the valuation date, and one issued later pays it in its issue month |
| `expenses` | acquisition at `t = 0` on `pols_if_init()`; zero where `t < 0` or `t ≥ proj_len()` | `expense_acq × pols_new_biz(t)`; zero outside cover | Acquisition per contract issued, in the issue month and not inflated, as in `basiclife/BasicTerm_SE` |
| `inflation_factor` | `1.025^duration(t)`, stepping on the contract's anniversaries | `1.025^(t // 12)`, stepping every twelve months from the valuation date | Unit costs in valuation-date dollars |
| `pols_maturity` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `check_pols_roll_fwd_resid`, `av_at`, `av_change` | `pols_if(t + 1)`, the next month's count; the block's account value opening from 0 at `t = 0` | `pols_if_at(t + 1, BEF_NB)`; from `av_pp_init() × pols_if_init()` at `t_entry()` | Next month's new business is no part of month `t`'s movement, and a point in force opens with its account value |
| `check_av_roll_fwd`, `check_pols_roll_fwd` | `all(...)` over the frame, the tolerance fixed | a loop over the frame, the tolerance scaled by `max(policy_count(), 1)` | A residual is rounding on that many contracts |
| `pols_annuitization`, `pols_death`, `pols_lapse`, `withdrawals`, `mort_rate`, `surr_charge_rate`, `surr_charge_age_cap`, `mva_in_force`, `mva_duration_factor`, `lapse_rate_base`, `lapse_dyn_exponent`, `lapse_dyn_market`, `lapse_dyn_rate`, `lapse_rate`, `mgsv_charge_pp` | unguarded: no `MYGA_US_S` frame has a month outside cover | zero or false outside cover, before any table or rate is read; `surr_charge_age_cap` calls the new `surr_charge_age_cap_at(age(t))`, the one reader of its table | A contract year or an attained age the contract does not have is never looked up, and nothing is charged or decremented there |
| `result_pols` | `pols_if`, the four outflows and `pols_if_aft_decr` | `pols_new_biz` second | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_new_biz`, the seven new opening-state accessors and the fourteen `is_*` decodes. The
docstring-only changes rewrite the time-axis prose, wrap three summaries to 92 characters,
correct "This cells" in `annuitization_pp`, and say that `result_av`'s `free_wd_avail`
column holds `free_wd_remain`. In `Data`, `model_point_table` reads
`model_point_table_sec.csv` and checks it, `future_horizon_mth` is new, four readers'
docstrings changed, `rate_scenario`'s and `withdrawal_table`'s to name the clock their `t`
is on, and nine cells are new: the six checked tables and the three extents,
`surr_charge_age_cap_first`, `surr_charge_age_cap_last` and `mva_factor_last_year`.
`MYGA_US_S`'s six readers are unchanged. Compiling added 58 `Data` cells, 75 in all, and the
Reference `np`: the vectors, arrays, counts and extents the projection reads, and
`model_point_numbers`, which reads the numeric columns as `MYGA_US_S` reads them; it
widened the checks of the model point table and of the two age tables (*The compiled
model*, below).

`MYGA_US_S`'s four joins on text keys are rows of `Data`'s arrays here, each read by the one
cell that reads its table: mortality at the row of the model point's `sex`, the scenario at
its `scenario_id`'s and the withdrawals at its `wd_schedule_id`'s, each numbered by `Data`
as `MYGA_US_S`'s `.loc` matches the key, and the surrender charge at the schedule code
`surr_charge_id(t)` returns, `NONE`, `INITIAL` or `RENEWAL`, where `MYGA_US_S` returns the
schedule's name, which `surr_charge_rate` tests for `none` and joins on. `Data` checks each
key before a projection joins on it: the model point table refuses a point whose scenario,
withdrawal programme, or sex and attained age the tables lack, and the surrender charge
table one without both schedules, where `MYGA_US_S` raises an error that names no file or
charges nothing.

No read goes further ahead than the month after its own: the block's closing account
value, weighted by the count carried into the next month, and the in-force roll-forward
read `t + 1`, and the two free-withdrawal cells read nothing later than the anniversary
that opens the year they are asked for.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, so point 8's
`expenses(t)` is `MYGA_US_S`'s `expenses(12 + t)` divided by 1.025, and point 11's,
valued five years on, by `1.025^5`. Their other cash flows, their counts and every value
per contract are `MYGA_US_S`'s from the month they are valued at on. Point 14 is
`MYGA_US_S`'s point 1 fifteen months on in those columns too. Its maintenance expense is
1.025 times S's, since the valuation clock stepped at `t = 12`, before the point's issue,
and `1.025^2` times S's in months 9 to 11 of each of its contract years, between the
valuation clock's next step and the point's own anniversary.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points and at the contract's
extremes, the longest frames from issue age 0 and the oldest issue age, 85, under the
attained-age cap. The compile tests hold it so on x86-64, on the splice grid too, which
takes the branches the committed points do not, and to 1e-12 relative elsewhere, where no
run has shown it yet. `MYGA_US_SEC` is the first annuity to compile, and the first of the
deferred annuities, whose chassis `FIA_US_SEC`, `VA_US_SEC` and `RILA_US_SEC` share: what
they take from it is set out last (*What the deferred annuities inherit*, below).

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py fixed_deferred_annuity                    # in place
python tools/build_sec_cy.py fixed_deferred_annuity --out /tmp/myga    # elsewhere
```

The tool exports the model to `MYGA_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `MYGA_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/fixed_deferred_annuity")    # the directory holding the build
from MYGA_US_SEC_nomx_cy import mx_model as model
model.Projection[7].result_cf()                          # point 8, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 7` after `Projection.result_cf()` leaves point
1's frame cached, `proj_len()` 480, while `point_id()`, not yet computed, reads point 8's
label, and `Projection.expense_maint` set to 60 once `Projection[7]` has computed point
8's `expenses(0)` leaves it at 4.0920, where modelx, and an ItemSpace made after, compute
4.9104. Set every Reference on a model just imported, before anything is computed, where
modelx would recompute; a test holds the compiled model to this.

A build takes about two and a half minutes with gcc, 153 s here, and needs a C compiler,
which is why `requirements.txt` leaves modelx-cython out:
`pip install -r requirements-cython.txt`. `run_sec.py --cython` builds in place when it
finds no build, or one older than the model, the sample, the spec or the tool, and
`--build DIR` runs a build made with `--out DIR`. Nothing a build writes is committed. All
of it derives from committed files, and an extension module is built for one operating
system, processor and Python (`_mx_classes.cpython-313-x86_64-linux-gnu.so` here); in place,
`.gitignore` covers all of it. A `lifelib.create()` copy of the library carries no `tools/`,
so it cannot build, and `run_sec.py --cython` says so.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so. Compiled by
the same tool, with a sample of its own, as it stood after running in force, the model typed
142 of its 157 `Projection` cells as C numbers. Ten took a timing, a kind or a scenario
column as text, `surr_charge_id` returned text, and five took a float, and those 16 kept a
dictionary for a cache; it ran no faster than its own export, 314 ms a point on `net_cf`
against 341, over the committed points. The bodies of the typed cells still called pandas
and Python: a `model_point()` lookup for each attribute a formula reads, the text of a
column compared in each of the fourteen decodes of the renewal architecture, the
free-withdrawal rule, the MVA family, its cap and the floor's withdrawal convention, a
`.loc` on a table for each attained age's mortality and age cap, each contract year's
surrender charge, each policy month's withdrawal and each year's MVA factor, a list of the
scenario's months built and its `max` taken for every month's rate, a total over the kinds
for `kind=None`, and an `int()` of a float for the MVA's whole years. So each input now
reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[7]` is point 8, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once, the fourteen `is_*` cells:
  the renewal architecture into `is_rollover` and `is_annual_redeclare`, the
  free-withdrawal rule into `is_pct_av` and `is_interest_only`, the MVA family into
  three, its cap into five and the floor's withdrawal convention into two. Each compares
  the text exactly, as `MYGA_US_S` compares it, so a value written in another case or with
  a space, `Pct_av` or ` pct_av`, is no flag, and the cell that branches on it answers as
  `MYGA_US_S` does, raising its message, `invalid free_wd_rule`, or taking its `else`
  branch. `free_wd_mva_exempt` is `MYGA_US_S`'s `bool()` of the value, kept: a blank, read
  as NaN, and any text, `False` in a column pandas reads as text among them, are true, as
  `MYGA_US_S` projects them.
- **Numbers, read as `MYGA_US_S` reads them.** `MYGA_US_S` reads the eight numeric columns
  of the contract and the ten of the opening state by `float()`, at the first month that
  asks. `Data.model_point_numbers()` reads every value so, element by element, once: a
  blank is NaN and projects NaN, as there, and text is refused, naming the column and every
  point it is on. The eighteen vectors read it, so text on one point refuses every point's
  projection at its first read of any of them, where `MYGA_US_S` refuses that point alone,
  at the month that reads the value.
- **Tables indexed by integers.** Each assumption table is an array, or a set of arrays, a
  cell reads by element. The scenarios, the withdrawal programmes and the mortality table's
  sexes are numbered from 1 in the sorted order of their keys, each point carrying its own,
  `scenario_number()`, `wd_schedule_number()` and `mort_schedule()`. The scenarios are
  step-filled by valuation month, one array a column, from the month of a scenario's first
  row to the table's last, with each scenario's first month beside them, so that
  `scenario_rate(t, name)` is one load at `min(t, last)`; the last row keyed at or before
  `t = 0` sets month 0. The programmes are held by policy month, 0.0 where a programme has
  no row, which is no withdrawal, as in `MYGA_US_S`, and so is a month past the table's
  last; a row keyed before policy month 0 is never read, and is left out. The surrender
  charges are held by schedule and contract year, the rows numbered as the schedule codes
  are, `INITIAL` 1 and `RENEWAL` 2, with each schedule's last year beside them. The age cap
  and the mortality are held by attained age, padded from 0 so that the age is the index,
  the mortality by sex, with each sex's first and last age beside it, and read through one
  cell keyed by the age each, `surr_charge_age_cap_at(a)` and the new `mort_rate_at(a)`. The
  duration factors are held by whole year remaining and column. The padding holds NaN, and
  nothing reads it: a mortality age outside the sex's and a month before the scenario's
  first are refused, naming the point, by the one cell that reads the table, and a contract
  year past a schedule's last is no charge, as in `MYGA_US_S`. The scenario and withdrawal
  arrays run to their tables' last months, and to `Data.read_last_mth` at the most, the
  last month any read reaches: 1,321, the last `t` of the cache, `12 × (maturity_age −
  issue_age_min) + future_horizon_mth + 1`, which `spec_sec.py` derives; a scenario is read
  at a valuation month of the frame or the month after it, a programme at a policy month in
  cover, 1,199 at the most. A row past it is held nowhere, since no read reaches it, and
  the last level before it holds to the end of the array, as the step function holds it.
  So a key far past any frame, a row at month 1e10, which `MYGA_US_S` looks up and never
  reaches, neither makes an array 373 GiB wide nor refuses a point `MYGA_US_S` projects. A
  change to one of the three bounds moves `read_last_mth` with the spec, and a test holds
  the two together.
- **Codes.** A timing, a kind, a scenario column or a surrender charge schedule, which
  `MYGA_US_S` spells as text, is an int Reference named as the text: the count's timings
  `BEF_NB = 0`, `BEF_DECR = 1`, `BEF_MORT = 2`, `BEF_LAPSE = 3` and `AFT_DECR = 4`, the
  account value's `BEF_WD = 5`, `BEF_INV = 6` and `EOM = 7`; the kinds `DEATH = 0`,
  `LAPSE = 1`, `ANNUITIZATION = 2` and `MATURITY = 3`, in `result_cf`'s order, and
  `ALL = 4`; the columns `MVA_REF_YIELD = 0` and `MARKET_RATE = 1`; and the schedules
  `NONE = 0`, `INITIAL = 1` and `RENEWAL = 2`, which `surr_charge_id(t)` returns. A call
  reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`, `av_pp_at(t, BEF_WD)`,
  `claims(t, DEATH)`. A string argument would give the cell a dictionary for a cache,
  where a code indexes a C array, so codes are numbered from 0 without a gap. The two
  families of timing, passed to different cells, are numbered as one, `BEF_NB` and
  `BEF_DECR` first, as in every SEC model, then each family in the order of its instants
  within the month. So no two timings share a code, and a code of one family passed to
  the other's cell, `av_pp_at(t, BEF_NB)`, is refused as `invalid timing` in both
  engines, where two families numbered from 0 would read it as `BEF_WD` without a word.
  The `Projection` docstring's *Codes* lists all eighteen.
- **The totals, by `ALL`.** `MYGA_US_S`'s `claims(t, kind=None)` and
  `claims_over_av(t, kind=None)` are one kind's amount or, with `None`, the four kinds
  added: `None` is no C parameter. Here the total is the code `ALL`, and `net_cf` calls
  `claims(t, ALL)`. `MYGA_US_S` writes the total as a chain of `+`, death, lapse,
  annuitization, maturity, not as `sum()`, and the chain is kept, so the total is
  `MYGA_US_S`'s float bit for bit however many of the kinds are non-zero, the sign of a
  zero included. The twin identity compares `MYGA_US_S`'s `(t, None)` with `(t, ALL)`.
  `ALL` passed to a cell of one kind, `claim_pp(t, ALL)`, is refused as `invalid kind`.
- **No float parameter on the projection's path.** A cell keyed by a float compiles with
  a Python dictionary for a cache. `MYGA_US_S`'s MVA cap on a currency base,
  `mva_pp_on(t, base)`, is written inline in its two callers, `mva_pp` and `wd_mva_pp`,
  each on its own base, and its geometric MVA factor, `mva_factor_geometric`, in
  `mva_rate`, each the same expression in the same order, so the numbers are
  `MYGA_US_S`'s bit for bit. Re-keying the cap's base to a code instead would have added a
  cache of 1,322 by 8 for nothing a reader needs. The twin identity exempts both of
  `MYGA_US_S`'s cells, whose values it compares through their callers in every month. And
  `mva_factor_at(k, column)`, the duration factors' reader by whole year that running in
  force had added, is gone: its year runs to the factor table's last row and the guarantee
  period, data no contract bound holds, so no cache could be sized for it, and
  `mva_duration_factor(t)` reads the array itself.
- **Whole years, by integer arithmetic.** `mva_duration_factor` took the whole years of
  the MVA term by `int()` of the float, which compiles to Python arithmetic on a Python
  object. The new `mva_term_years(t)` computes them as ints, `n k − y` from the guarantee
  period, its index and the contract year, the same int `MYGA_US_S` adds to the months in
  `mva_term`, and `mva_duration_factor` reads it.
- **Three cells kept as `MYGA_US_S` wrote them.** `mgsv_rate_statutory(cmt5)`,
  `mgsv_rate_is_compliant(cmt5)` and `mva_ref_term_years(tau)` take a float, and no
  projection cell calls them. They are `MYGA_US_S`'s formulas unchanged, `math.floor` and
  `math.ceil` included, kept for a user checking a contract's rate against Model #805 and
  for the comparison with `MYGA_US_S`. `tests/us_registry.py` names them, under
  `"engine"`, and the compile tests admit them, and no other cell, to a dictionary cache,
  a float parameter and the `math` module, the one module a formula outside the reports
  refers to; no compiled cell may call them.
- **No tuple built.** Two formulas assigned two locals at once, `lo, hi = ...` in
  `surr_charge_age_cap_at` and `cr, mr = ...` in `lapse_dyn_market`, and
  `claim_from_av_pp` tested a kind's membership in a tuple: each builds a Python tuple,
  and each is now plain assignments and comparisons.
- **No Python call kept.** No formula outside the reporting and engine cells calls a
  Python builtin outside its refusals but `int`, `float`, `bool`, `abs`, `min`, `max` and
  `range`, which Cython turns into C, so `tests/us_registry.py` admits none. No such cell
  is uncached, and none takes a float.
- **Operands in `MYGA_US_S`'s order.** Compiled, a two-argument `max` or `min` evaluates
  its arguments right to left, so a point that reaches two refusals would raise the
  second's message. Each of the six that take two operands from cells or tables,
  `surr_benefit_pp`, `claim_pp` for `DEATH` and `MATURITY`, `wd_free_pp`, `credit_rate`
  and `surr_charge_rate`, binds them to locals first, in `MYGA_US_S`'s order, and so do
  the two divisions whose divisor a cell tests (*What it refuses*, below). A point whose
  `mva_cap_rule` and `mgsv_wd_convention` are both blank reaches both refusals of
  `surr_benefit_pp`, and raises `invalid mva_cap_rule` in both engines. No number moves:
  only the order the caches fill.
- **Reporting cells stay Python.** `model_point()`, the ten label accessors `policy_id()`,
  `sex()`, `tax_status()`, `mgsv_wd_convention()`, `renewal_architecture()`,
  `free_wd_rule()`, `mva_family()`, `mva_cap_rule()`, `scenario_id()` and
  `wd_schedule_id()`, and the three reports return a table row, text and DataFrames, for a
  reader, for `run_sec.py` and for the comparison with `MYGA_US_S`. No other cell calls
  them, so they cost the projection nothing. A label accessor returns its column as read,
  and `Data` accepts a label that is not text: a blank or numeric `policy_id` or
  `tax_status`, which no cell reads, a value none of a column's flags names, which the
  projection meets as `MYGA_US_S` does, and a numeric `sex`, `scenario_id` or
  `wd_schedule_id` where its table's keys are numbers. So each accessor compiles to a
  Python object, as the sample traces it (below), and returns what modelx returns. The two
  checks are reporting cells too, but they return a verdict, which compiles to a C
  `bint`.

Of `Projection`'s cells, compiling took away three, `mva_pp_on`, `mva_factor_geometric` and
`mva_factor_at`, and added six: `point_id`, `scenario_number`, `wd_schedule_number`,
`mort_schedule`, `mort_rate_at` and `mva_term_years`, 160 in all. The Reference `idx`, 0,
takes the place of `point_id`, and `issue_age_min`, 0, `issue_age_max`, 85, and the eighteen
codes are new References. The `Data` docstring lists its vectors, arrays and counts, each
with the column or file it comes from: 22 vectors of int64 by point and 19 of float64; each
scenario's first month, each surrender schedule's last year and each sex's first and last
age, int64; the age cap by attained age, and the scenarios, the programmes, the surrender
charges, the mortality and the duration factors as tables, float64; and eight int counts and
extents, each a table's check. Its seven readers, its six checked tables,
`model_point_numbers()` and `input_dir()` stay Python, returning DataFrames and a path, and
no `Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 143
of its 160, the two checks among them, returns a C `bint`, `long long` or `double`, and
caches a single value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,322 by `t`, of `double`, `long long` or `bint` | the 79 cells of `t` alone: every count, rate, factor, charge, premium, withdrawal, value, claim and cash flow; the policy clock, its years, the guarantee period's index, start and end, and the attained ages; the flags `is_active`, `in_gp_window` and `mva_in_force`; the schedule code `surr_charge_id`; and the checks' monthly residuals |
| a C array of 1,322 by 8 | the 10 cells of `t` and one code: `pols_if_at`, `av_pp_at` and `av_at`, by `(t, timing)`; `pols_decr`, `claim_pp`, `claim_from_av_pp`, `claims`, `claims_from_av` and `claims_over_av`, by `(t, kind)`; and `scenario_rate`, by `(t, name)` |
| a C array of 102 by `y` | `free_wd_base` and `free_wd_allow`, by contract year |
| a C array of 101 by `a` | `surr_charge_age_cap_at` and `mort_rate_at`, by attained age |
| one `long long`, `double` or `bint` | the 50 cells without a parameter: the point's label, numbers, decodes and flag, its opening state, its scenario's, programme's and sex's rows, the ends of its frame, its GMIR factor, its monthly GMSV rate and its count in force, and the two checks |
| a Python object | the reporting cells but the checks, fourteen |
| a Python dictionary, behind a C signature | the three engine cells, their bodies Python |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary but the engine
cells'.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the three reports
and the two checks on every committed point, which reach every cell but twenty:
`model_point()` and the ten label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; the three engine cells, which no projection cell calls; the
investment in the contract, `tax_basis_pp`, with `taxable_wd_pp` and `tax_basis_pp_init`,
which only it reads, and no report; `gp_end`, the months left in the guarantee period;
and `claims_over_av`, the benefit paid above the account value, which no report reads.
And of the cells they reach they leave two codes uncalled: `av_pp_at`'s `EOM` and
`av_at`'s `BEF_WD`. The sample calls those too, the monthly ones in every month of the
frame and the month after it, `claims_over_av` at every kind and `ALL`, and the engine
cells at one argument each, the arguments `MYGA_US_S`'s own tests use. It projects the
committed points alone: the export it runs reads the CSVs of the directory the build is
made in, and the trace it needs is the committed points', which are what the tests
project. The ten label accessors it calls once more, on a copy of the table's first point
with its seven free labels blank and its three keys, `sex`, `scenario_id` and
`wd_schedule_id`, the number 1, beside one-key copies of the mortality, scenario and
withdrawal tables keyed by 1, which it writes to a temporary directory and reads by a
second instance of the export, given the files' absolute paths. That types them as Python
objects, so that a blank or numeric label returns what modelx returns rather than raising
`TypeError` (*What compiling changed, and why*). The committed points leave branches
untaken: the female mortality, the GMIR's other bands, a schedule that runs out, a
declared-differential term past the factor table's last year, the attained-age cap,
utilization withdrawals. That still types every cell, because every branch of a cell
returns the one type its others return, a rate a float in every branch and the whole
years of the MVA term an int in every branch, and on points that take those branches the
compiled model computes modelx's numbers (above). A code a cell refuses is not called: a
raise types nothing. The sample also raises the recursion limit, which modelx raises and
its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forwards read and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and one of headroom where that leaves room:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,322 | 1,321. The longest frame is a contract issued at the youngest issue age, 0, covered to 100, 1,200 months, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: `t = 0 … 1,319`, and the month after, 1,320, where `check_pols_roll_fwd_resid`, and `av_change` through `av_at(t, EOM)`, read `pols_if_at(t + 1, BEF_NB)`, 1,321. So no headroom |
| `t`, and `timing`, `kind` or `name` | 1,322 by 8 | the eight timings of the one numbering, `BEF_NB` 0 to `EOM` 7; the four kinds and `ALL`; and the two columns. Every 2-D cache has this one width. Cython's generated unpickle code converts a space's 2-D caches with one function for each inner width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A kind from 5 to 7, a column from 2 to 7, or a timing a cell does not take is then inside the cache, where the cell refuses it as modelx does, and a code from 8 raises |
| `y` | 102 | 100, the contract year of the last covered month at issue age 0, read by `free_wd_base` and `free_wd_allow` in cover alone, and one of headroom |
| `a` | 101 | 99, `maturity_age` − 1, the last attained age in cover, read by the two readers by age in cover alone, from the youngest issue age, 0, and one of headroom |

The duration factors have no cache of their own: `mva_duration_factor(t)` reads them at
`mva_term_years(t)`, keyed by `t` (*What compiling changed, and why*). `proj_len()` refuses
a point issued below 0, `issue_age_min`, or above 85, `issue_age_max`, the issue ages
`product-spec.md` admits, and one at or past maturity, in modelx as compiled, and cover ends
at attained age 100, `maturity_age`, so no report on a point the model projects runs past
these caches. `issue_age_min`, `maturity_age` and `Data.future_horizon_mth` are the contract
the sizes are derived from; `issue_age_max` sizes nothing, since every size rests on the
youngest issue age, and set higher it projects the older issue ages `MYGA_US_S` projects.
Lower the minimum, or raise `maturity_age` or the horizon, and a report runs past the caches
in the compiled model alone: a frame of more than 1,320 months, a contract year past 101 or
an age past 100 raises `IndexError`, naming nothing, where modelx projects. Each needs the
sizes derived again, as `spec_sec.py` derives them, and a rebuild: `t` raised to 12 ×
(`maturity_age` − `issue_age_min`) + the horizon + 2, `y` to `maturity_age` −
`issue_age_min` + 2 and `a` to `maturity_age` + 1. The shipped mortality table starts at
attained age 40, so a point younger than 40 in its first month on the books is refused today
by `Data`, naming it; an issue age of 0 is the contract's, which an extended table reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it was
measured to change there. Here `cpow` reaches nine powers in eight cells: the monthly
rates of both decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`;
the monthly credited, GMSV and GMIR rates, `(1 + i)^(1/12)` in `credit_rate_mth`,
`mgsv_rate_mth` and `prem_accum_gmir_pp`; the dynamic lapse's two power terms in
`lapse_dyn_market`; the geometric MVA factor, raised to the MVA term, in `mva_rate`; and
expense inflation, `(1 + r)^(t // 12)` in `inflation_factor`. Without `cpow` a compiler
with C99's complex numbers, gcc among them, computes a power of two doubles as a complex
power, which can differ from Python's float power in its last bits. With both directives
and the flag every compiled value agrees with modelx's bit for bit, and the compile tests
hold each, by the module's first line, by the compiler's command lines and, on x86-64, by
the comparison itself. On the same platforms the tool adds
`-Werror=incompatible-pointer-types`, so that gcc before 14, which only warns of a pointer
of the wrong type, fails the build as gcc 14 does: the error two cache widths give (*The
sample and the spec*, above).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 2,512,888
bytes, about 2.5 MB, the type's basic size, which holds every cell's cache, each beside a
flag array of its shape that marks what is computed. The ten 2-D caches, 1,322 by 8, are
about 1.27 MB of it with their flags, half, and the 79 arrays by `t` nearly all the rest.
That is 1.33 times `UL_US_SEC`'s, for frames of 1,322 months against 1,358 and ten 2-D
caches against five. Making one and releasing it, nothing computed, took 0.09 ms here, of
the 1.2 ms a compiled point takes (*Speed*, below). Deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference cycles,
and only Python's cyclic collector frees it. That is why `run_sec.py --block` collects after
each release, in its frame pass and in its projections (*Run it*, above), and a compile test
holds a compiled block run to one point's ItemSpace at a time. Without it, 504 compiled
points peaked at 1,207 MB (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no limit
raised. What it needs is stack. The deepest calls the contract allows, a cold `net_cf` and
a cold `check_av_roll_fwd_resid` in the last month of the longest cover, issue age 0,
issued now or 120 months on, run the count's and the account value's chains back to
`t_entry()`, 1,214 to 1,216 cells deep in modelx, one cell a month and 14 to 16 more; the
residual, on an interest-only, GMIR-floored point, is the deepest.
Compiled with gcc each runs on a thread of 320 KiB of stack and not of 288 or 304, 243 to
270 bytes a level. A test runs both in a thread of 1 MiB, the
stack Windows gives a program's main thread unless the program is linked for more, and again
on the main thread, which is where `run_sec.py --cython` runs. MSVC's frames may be larger
than gcc's, and the `cython` CI job, which runs the test on Windows too, is the check on
them: the test first runs the call at seven stacks, from 256 KiB to 2 MiB, and reports the
smallest it ran on, so a first run there measures MSVC's need. Until it has, the need is an
estimate: at the 325 to 433 bytes a level MSVC took on `WholeLife_US_SEC`'s chain, 1,216
levels need about 386 to 514 KiB, inside 1 MiB by about twice at the least. A stack below
the need kills its child on an overflow, by design (with gcc, 288 KiB does); on Windows the
child ends with `STATUS_STACK_OVERFLOW`, and should Windows Error Reporting hold it instead,
the test waits a bounded time for each child rather than the job's hour. The export recurses
in Python instead: the same call needs a recursion limit of 2,444 there, and the three
reports and the two checks, which run in ascending `t`, need 54 once the package is imported
and 128 with its import, as the sample runs them, so `sample_sec.py` sets 10,000, four times
the first rounded up to the thousand, and a test holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode or hold, when the vector is first read, naming every point at
  fault, or the table and its lines: a `point_id` that is not a whole number,
  `model_point_table_sec.csv: point_id must be a whole number; ['7x'] is not`, read by
  `point_id()` and every refusal; and text in one of the eighteen numeric columns,
  `model_point_table_sec.csv: premium must be a number; it is not at point_id [2]`, which
  refuses every point's projection (*What compiling changed, and why*). And, before it is
  cast to int64, a number of `2**53` or more in size, which numpy would cast to the least
  int64 once past int64: a `point_id`, a model point's issue age,
  `model_point_table_sec.csv: age_at_entry must be below 2**53 in size; it is not at
  point_id [3]`, a `duration_mth` and a `guar_period`; and, by the table's check, which
  every reader of the table asks first, an assumption table's key, `rate_scenario.csv: t
  must be below 2**53 in size; it is not on line [3]`, which would otherwise read as the
  least int64, a scenario's first level from month 0, where `MYGA_US_S` refuses the point.
  A key written as a float, an age `40.0`, is read by its value, as `MYGA_US_S`'s lookups
  match it; a key written as text is not whole, and the table's check refuses it, as at
  stage `E`.
- A negative age in `mort_table.csv` or `surr_charge_age_cap.csv`, `mort_table.csv: age
  must be 0 or more; it is not on line [164]`, by the table's check, which every reader of
  the table asks first: each is held from age 0, so that the age is the index. A refusal
  `MYGA_US_S` lacks, which projects a point on such a table, never reading the row.
- A key beyond a table, by the one cell that reads it, naming the point, where
  `MYGA_US_S`'s lookup raised: an attained age outside the point's sex's, `point_id 1: the
  mortality table gives no rate at attained age 39`, from `mort_rate_at`, and a month
  before the point's scenario's first, as on a scenario that starts in a later point's
  issue month, `point_id 14: the rate scenario sets no level of the point's scenario at
  t = 0`, from `scenario_rate`. No projection reaches either: `Data` refuses a point whose
  first month on the books its tables do not cover, and `proj_len()` one its mortality
  stops short for. A contract year past a schedule's last, and a policy month a programme
  has no row at, are no charge and no withdrawal, as in `MYGA_US_S`.
- A divisor of zero, with Python's `ZeroDivisionError: float division by zero`, which
  the cell tests before it divides, since compiled division words it `float division`: an
  account value of zero in cover, in `lapse_dyn_rate`, which every report reaches and a
  scheduled withdrawal of the whole account value brings about, where `MYGA_US_S` raises
  the same; a geometric MVA's `1 + it + s_adm` of zero, in `mva_rate`; and a
  `mgsv_stat_step` of zero, in the engine cell `mgsv_rate_statutory`. Every other division
  divides by a constant, 12 or 12.0, or by the guarantee period, which `Data` holds at 1
  year or more.
- By `proj_len()`, a point issued below `issue_age_min` or above `issue_age_max`, one at
  or past maturity, and one whose sex the mortality table rates only below `maturity_age −
  1`, in that order: `point_id 3: issue age 86 is above issue_age_max, 85`, and
  `point_id 1: the mortality table gives no rate at attained age 99, the last before the
  deemed maturity`.
- A timing, a kind or a column a cell does not take, `ValueError("invalid timing")`,
  `("invalid kind")` and `("invalid name")`, where the code is inside the cell's cache: a
  code of the other family, `pols_if_at(0, BEF_WD)`, `av_pp_at(0, BEF_NB)`, a kind a cell
  lacks, `claim_pp(0, ALL)`, a code up to 7, `claims(0, 5)`, and a column past the two,
  `scenario_rate(0, 2)`.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1322)` and `net_cf(-1)`, which modelx answers with 0.0, the month being outside
cover; `pols_if_at(0, 8)`, `claims(0, 8)` and `scenario_rate(0, 8)`, which modelx refuses
as `invalid timing`, `invalid kind` and `invalid name`; `free_wd_allow(102)`, which modelx
answers with 0.0, and `free_wd_allow(-1)`, which modelx answers with year 1's allowance;
`free_wd_base(y)` for a year that opened before the valuation date, `free_wd_base(2)` on
point 9, in force 30 months, which reads the account value at a month before `t = 0`, and
which modelx answers with the opening account value: `free_wd_allow`, its one caller,
takes such a year's allowance from the opening state, so no projection asks for it;
`surr_charge_age_cap_at(101)` and `surr_charge_age_cap_at(-1)`, which modelx reads as 0.0,
the table's last row, and 1.0, no cap; and `mort_rate_at(101)`, which modelx reads from the
table, 0.313569, and `mort_rate_at(-1)`, which modelx refuses, naming the age. An `idx`
past the last row is refused in both, with an `IndexError` at the first read of a vector,
and `Projection[-1]` reads every vector at its last element in both, so it is the table's
last point, under that point's own `point_id()`, 14.

A Reference is a C variable of its value's type: `issue_age_min`, `issue_age_max`,
`maturity_age`, the codes and `idx` a `long long`, as `Data.future_horizon_mth` is, and
the rates and amounts a `double`. Set past that type, it is converted when it is set,
where modelx keeps the value as given. A float set on an int Reference is truncated toward
zero without a word, `maturity_age = 100.7` reading 100 and `issue_age_min = 0.5`
reading 0, where modelx computes with the float: `maturity_age = 100.7` makes point 1's
`proj_len()` 488.4 there, and `result_cf()` then fails. A text, a NaN, an infinity or an
int beyond 64 bits is refused at once, with `TypeError`, `ValueError` or `OverflowError`.
An int set on a `double` Reference reads as a float compiled, where modelx returns the
int: `gmir_factor_low = 2` gives `gmir_factor()` 2 in modelx and 2.0 compiled, where the
cell returns the Reference as it is. Each shipped Reference is a value of its C type, so
no shipped number differs. And a Reference set past its domain computes as C computes,
where modelx raises: an `inflation_rate` of `1e300` makes `inflation_factor(24)` infinite
compiled, where modelx's power raises `OverflowError`.

Mortality is not capped, in `MYGA_US_S` or here: `Data` refuses a rate outside 0 to 1, as
at stage `E`, and the shipped rates in cover are 0.263 at most. The annual lapse rate is
clamped to `lapse_rate_min` and `lapse_rate_max`, 0.5% and 90%, as in `MYGA_US_S`, by
`min` and `max`, which the compiled model computes as comparisons in the same order. The
clamp binds in the shock year, where 93.75% is held to 90%, on every committed point that
reaches it, and the comparison there is bit for bit. A NaN that reaches the clamp, sent
through `gmir_factor_low`, a Reference, gives the floor, 0.5%, in both, and `net_cf(0)`
the same finite number in both, without a word, as in `MYGA_US_S`.

### What the deferred annuities inherit

`FIA_US_SEC`, `VA_US_SEC` and `RILA_US_SEC` run on the chassis this model runs on, an
account value rolled forward by month with a surrender charge, an MVA or its like, a
free-withdrawal allowance and an age cap, and their compile steps start from what this
one settled:

- **Scenario rates by month.** A scenario path keyed by valuation month is a step-filled
  array a column, `[scenario, t]`, from the scenario's first month to the table's last,
  NaN before the first and in row 0, read by one cell, `scenario_rate(t, name)`, which
  refuses a month before the scenario's first, naming the point, and holds the last level
  past the table's end, the column a code in the model's one inner width. The last row
  keyed at or before `t = 0` sets month 0. The array ends at the last month a read
  reaches, `Data.read_last_mth`, the cache's last `t`, so a key far past the frame neither
  widens it nor refuses a point the S model projects.
- **Withdrawal schedules.** A programme keyed by policy month is `[schedule, policy
  month]`, 0.0 where it has no row, a value rather than padding, so no read tests for
  NaN, and 0.0 past its last month; a row keyed before policy month 0 is left out, and so
  is one past `Data.read_last_mth`.
- **Surrender charges by year.** The schedule in force is a code that is also its row of
  the charges, `[3, year]`, with each schedule's last year beside them, and a year past
  the last is no charge, as `MYGA_US_S`'s lookup missed. `MYGA_US_S` names the schedule in
  lower case, so the twin identity exempts its `surr_charge_id` and compares the rate it
  selects.
- **The MVA.** A float-keyed helper on a currency base is written inline in each int-keyed
  caller, not re-keyed; a float engine on the projection's path likewise; whole years of a
  float term are an int cell computed by integer arithmetic, never `int()` of the float;
  and a table keyed by a quantity no contract bound holds is read in the `t`-keyed cell,
  not through a cache keyed by it.
- **The age cap and the mortality.** Tables by attained age are padded from age 0, which
  refuses a negative age, read through one cell keyed by the age each, sharing one size,
  `maturity_age + 1`; the mortality is `[schedule, age]` by sex, with each sex's first and
  last age, refused outside them, and its last age is checked against the last covered
  month's in `proj_len()`, where `maturity_age` can be read.
- **The free-withdrawal base.** The contract-year cells keep `MYGA_US_S`'s key, `y`,
  sized `maturity_age − issue_age_min + 2`, and read the state that opens a year in
  cover alone.
- **Cells kept as the S model wrote them.** A float-parameter cell no projection cell
  calls stays as written, its module included, under the registry's `"engine"`, which
  admits it by name and refuses it to every compiled caller.
- **Totals.** Where the S model adds its kinds by a chain of `+`, the chain stays, under an
  `ALL` code, bit for bit at any number of non-zero kinds; the spec's `twin_arg_map` maps
  the S model's `None` onto it and passes the SEC model's own codes through untouched,
  since the product's tests compare the SEC model with itself too.
- **Numbers read as the S model reads them.** One checked copy of the numeric columns, read
  by `float()` element by element, refusing text by column and point.
- **Labels and depth.** The label accessors are traced on the committed points and on a
  second instance whose labels are blank and whose join keys are numbers, read from
  one-key copies of the tables by absolute path; and the chains are one cell a month,
  1,214 to 1,216 levels at the longest cover, 320 KiB of gcc's stack, with the export's
  2,444 and the sample's 10,000.

### Speed

`python tools/bench_sec_cy.py fixed_deferred_annuity` builds the model into a temporary
directory, or takes a build with `--build`, and times one block run on three engines:
modelx, the export and the compiled model. Each engine runs the committed table repeated,
in a process of its own, as `run_sec.py --block` runs a block, each point projected and
then released. `net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,006 | 1.19 ms (7.15–8.17) | 2.11 ms (12.66–13.44) | 90 MB |
| export | 602 | 15.0 ms (9.02–10.06) | 15.4 ms (9.25–9.57) | 90 MB |
| modelx | 126 | 520 ms (65.56–70.81) | 517 ms (65.09–70.77) | 140 MB |

On `net_cf` the compiled model runs 12.6 times its export, and on `result_cf`, where
building the DataFrame takes much of its time, 7.3 times; it runs 437 and 245 times
modelx. A second run of the compiled model and the export straight after, under a 1-minute
load between 3.2 and 4.0, gave the compiled model 1.30 and 2.21 ms and the export 15.1 and
14.8 ms, 11.7 and 6.7 times. The modelx runs were made apart, to keep each run under ten
minutes. The compiled model takes about `UL_US_SEC`'s time a point, 1.21 ms, for an
ItemSpace 1.33 times the size; of its 1.19 ms, making and releasing the ItemSpace takes
about 0.09 ms. It runs about as many times its export as `UL_US_SEC`, 12.0, more than
`Term_US_SEC`, 9.5, or `BasicTerm_SC` on its own measure, 8.7, and fewer than
`VUL_US_SEC`, 13.8. As it stood after running in force, compiled the same way, the model
ran no faster than its export (*What compiling changed, and why*, above), and the compiled
model runs about 210 times that build on the same measure, 1.47 ms a point over the
committed points against 314: the representation, not the compiler, is the gain, and the
export gained from it too, 14.1 ms a point against 341. The release keeps a block flat: the
compiled model's peak grew by less than 0.1 MB over its 6,006 points, and without the
collection after each release (`--no-collect`), 504 compiled points peaked at 1,207 MB.
Reading the seven files and building every `Data` vector and array for those points took
0.08 s, and asking every point for its frame, the runner's first pass, 0.53 s, most of it
making and releasing an ItemSpace a point.

Measured on 2026-11-13 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 2.7 and 5.1 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Each time is the fastest of three runs; under load the spread
is wide, and the fastest run is the one to compare. The comparisons over the committed
points, with the build as it stood after running in force, are the fastest of two runs of
three rounds each, in one process an engine, and so is the cost of an ItemSpace, the
fastest of five rounds of 1,000.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 7, issued at
  the valuation date, every cell of `MYGA_US_S`'s agrees at every argument `MYGA_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point`, `av_pp_init`,
  `mgsv_pp_init` and `result_pols`, whose meaning changed, `mva_pp_on` and
  `mva_factor_geometric`, which this model writes inline in their callers, and
  `surr_charge_id`, which names the schedule where this model returns its code, each
  compared through the cells that read it in every month; `MYGA_US_S`'s timings, kinds
  and scenario columns are read at their codes, and its `claims(t, None)` and
  `claims_over_av(t, None)` at `ALL`. So the goldens
  `tests/test_fixed_deferred_annuity_us.py` asserts on cells that sweep reaches — the
  worked example's table to the cent, both surrender traces line by line and the
  roll-forwards among them — hold here with no number restated. The identity holds on any
  count, since `MYGA_US_S` already takes the premium and charges acquisition on the
  contracts issued. The same suite holds the model to the conventions every `_SEC` model
  meets: every frame starts at `t = 0`, `pols_if` is the `BEF_DECR` count, new business
  enters once at its `policy_count`, nothing happens before issue, and the in-force
  columns are present.
- **The splice**, in `tests/test_fixed_deferred_annuity_us_sec.py`: each `MYGA_US_S` point
  restated in force at a month either side of its events continues the S projection, in
  `result_cf`, in `result_pols`, column by column, and in every other cell the two share, to
  1e-9, but those the twin identity skips; `proj_len`, a frame on the valuation clock;
  `scenario_id`, which names the row's own scenario (below); and `tax_basis_pp_init`, the
  basis entering the row's valuation month where S's is the basis at issue, though
  `tax_basis_pp` and `taxable_wd_pp`, which open from it, are compared. The months are 11
  and 12, either side of the first anniversary; 30, after point 5's excess withdrawal; 59,
  60 and 61, the last month of the initial term, the window and the month after it; 89,
  inside the first renewal period, after point 3's redeclaration at 84; and 479, the last
  covered month. So do four variants of S's points, in a copy of S's table that is never
  committed, for what S's own points do not reach: a female contract at the GMIR's middle
  band, with the floor's annual charge and premium tax; a qualified contract at its high
  band, with no basis; a seven-year guarantee period; and issue at age 85, where the age cap
  binds. Each spliced row runs on its own copy of its S scenario, re-based to its month and
  stepped within the initial term and the renewal periods, so that a rate read at the wrong
  month or on the wrong clock reads another number, and the renewal surrender charges are
  set apart from the initial ones. Inflation, on the valuation clock, is set to 0 in both
  models, and four assumptions that ship at zero are switched on in both, the
  free-withdrawal utilization, a renewal spread, the acquisition expense and a premium load,
  because at the shipped zeros they hide parts of the state from any comparison. A contract
  year that closed before the splice month is no year of the restated row, and its allowance
  is not compared.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every branch, every opening-state column,
  every kind of valuation month and every product switch the full grid reaches, and a test
  asserts that they do. The other cases carry the `sec_full` marker and show as skipped,
  with the reason, unless `USLIB_SEC_FULL=1` is set. One leg of the CI matrix sets it, so
  every CI run runs the full grid too.
- **Future new business**: issued 1 and 15 months after the valuation date, each S point
  is the S projection moved on, with zeros before issue in `result_cf`, `result_pols` and
  `result_av` and no decrement rate evaluated there, and so is each variant issued a month
  on. A point issued 15 months on reads contract year −1 before issue, which is what shows
  a missing guard.
- **How it computes**: on every row the splice and the future business compare, after every
  report, no cell has been called at a negative month, none evaluated from `t_entry()` on
  has read a month before it, none evaluated at month `t` has read a month later than
  `t + 1`, directly or through a cell keyed by a contract year or an age, and no contract
  year that closed before the valuation date has been asked for. On a fresh read of the
  committed model `duration_mth` is a closed form, every point is swept under a lowered
  recursion limit, which a recursion backward over the frame would exceed, and a cold
  last-month call runs at most one cell a month back to `t_entry()`, plus a fixed overhead,
  on the committed points and at issue age 0.
- **Counts, validation and regeneration**: the roll-forward closes, `AFT_DECR` is the
  next month's `BEF_NB`, and `pols_if_at` refuses a timing it does not have;
  `result_pols()` is `MYGA_US_S`'s, column for column, with `pols_new_biz` beside it;
  doubling `policy_count` doubles every cash flow and moves no per-contract value, and at
  a million contracts both roll-forward checks close on their scaled tolerance; each
  malformed row is refused naming its point, a missing, negative, infinite or misplaced
  opening state among them, each state column on new business and on future business, a
  zero account value in force, an interest-only allowance above the interest at its
  anniversary, a stale allowance at either end of the first contract year and on an
  anniversary, an interest-only allowance apart from the first year's interest at either
  end of the second, and a scenario, a withdrawal programme, a sex or an attained age that
  the table it keys lacks; each assumption table whose keys cannot be read, a key written
  as text in each of the six, a blank, a fractional or a repeated key, a gap, a blank text
  key and a value out of its range, is refused naming the file and the lines, and the
  renewal schedule misspelt naming the file, by `Data` and by a projection that reads it;
  a scenario that starts after the first month a point on it is on the books is refused
  for that point, and read for a point issued no earlier; keys written as floats are read
  by value; the horizon is a Reference, which at 0 refuses any future business, saying so;
  a point past its cover is refused by `proj_len()`, and `run_sec.py --block` refuses it
  before printing anything; a zero count, durations written as floats, a negative floor
  and `P_accum`, a zero basis, a contract issued 120 months on, on an anniversary a
  remainder above the year's allowance, allowances carried to the cent, the ties at half a
  cent among them, and an interest-only contract on its second anniversary, which
  continues `MYGA_US_S`, are accepted; and the committed table is what `MYGA_US_S`
  generates.
- **The opening state and the rest**: each derived row's opening state is what `MYGA_US_S`
  carries into its month, and at the shipped assumptions the row is S's from that month
  on, in every cell but those expense inflation moves; each state column, changed, moves
  its committed row as above; the rate scenario runs on the valuation clock and the
  withdrawals on the policy clock; expense inflation runs on the valuation clock at the
  shipped 2.5%, which only this test sees, since the splice sets the rate to 0;
  acquisition falls on new business alone, per contract issued, asserted at 2.5 contracts
  a point; every guarded cell holds its value outside cover and reads no rate there, and
  every monthly cell answers there; the points of a block sum row by row; an extract
  without the generator's three columns, labelled apart from its positions, projects the
  same numbers; and `run_sec.py` prints the model's numbers, for a point issued at the
  valuation date, two points restated and the block, and writes "1 month" for a point a
  month either side of the valuation date.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py MYGA_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their call
  syntax changed: a point's position for its label, the codes for the text of a timing, a
  kind or a scenario column, and `ALL` for `None`. Each point is named by its label, in
  `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: the two `ALL` totals are `MYGA_US_S`'s `(t, None)` bit for
  bit, sign of a zero and type included, on its points' twins in every month, and with
  every kind set to −0.0 each total is −0.0, as `MYGA_US_S`'s chain gives; the schedule
  code is `MYGA_US_S`'s schedule in every month; the engine cells raise where
  `MYGA_US_S`'s raise; a divisor of zero raises `MYGA_US_S`'s `ZeroDivisionError`, with
  its message, on its own inputs, a withdrawal of the whole account value among them;
  every parameterless cell but the reporting ones returns a Python `int`, `float` or
  `bool`, not a numpy scalar (R11); a point issued below `issue_age_min` or above
  `issue_age_max`, and one whose sex the mortality table rates only below
  `maturity_age − 1`, are refused by `proj_len()`, naming the point, and each projects
  once its bound is moved past it; each value a decode names, written in another case or
  with a space beside it, is answered as `MYGA_US_S` answers it, raising its message or
  projecting its numbers; the `Data` vectors hold the table as `MYGA_US_S` reads it, by
  `float()`, `int()`, `bool()` and the decodes' exact comparison, and each join number the
  key's place in sorted order; each array holds its table at its keys, on copies written out
  of their keys' order with keys as floats, and holds NaN where nothing is read but 0.0
  where a programme has no row; scenario keys at or below 0 and withdrawals keyed before
  issue are read as `MYGA_US_S` reads them, and a scenario level and a withdrawal at month
  1e10 widen no array, and every point projects as without them; each size in `spec_sec.py`
  is the one its comment derives from the model's References, and the sample's recursion
  limit the one its comment derives; and
  `run_sec.py` sums the block as `groupby` does, bit for bit, and outside the repository,
  beside a copy of the model or at a path too shallow to hold one, `run_sec.py --cython`
  says it cannot build, and in place it rebuilds exactly when no build is there or a
  source is newer than the build, on a fake product whose times are set, building
  nothing.
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
  `tests/test_fixed_deferred_annuity_us_sec.py`: the same comparison, with the codes and
  engine calls no report reaches, on the splice grid, twenty rows at a time, the core by
  default and the full grid with `USLIB_SEC_FULL=1`, variants included; at the contract's
  extremes, the longest frames from issue age 0, a scenario that starts in a point's issue
  month 120 months on, a withdrawal programme to the last covered month, the oldest issue
  age through the attained-age cap, the last covered month, a declared-differential term
  past the factor table's last year and a schedule that runs out, again under the splice's
  References with `USLIB_SEC_FULL=1`; where the caps bind, the attained-age cap on the
  surrender charge and each of the four MVA cap rules; on labels that are not text, one
  blank decoded label a point, and keys that are numbers; and on every table written out
  of key order with keys as floats, scenario keys at and below 0 and a withdrawal before
  issue among them; the compiled model refuses what modelx refuses, with modelx's message,
  on the extract relabeled `100 + point_id` too, a point the contract does not issue, text
  in a number, a value at `2**53`, a negative age, each decoded value written otherwise, a
  code inside a cache it does not take among them, a point that reaches two refusals
  raises `MYGA_US_S`'s first, a divisor of zero raises Python's `ZeroDivisionError`
  message, and an argument past a cache raises `IndexError`; the deepest call the
  contract allows runs cold on a 1 MiB stack and on the main thread, and the test reports
  the smallest of seven stacks, 256 KiB to 2 MiB, it ran on, waiting a bounded time for
  each; a Reference set after the model has
  computed changes no value it has cached; and `run_sec.py --cython` prints what
  `run_sec.py` prints, and refuses a directory that holds no build. They are marked
  `cython`, and they skip without the toolchain, but in the `cython` CI job, which
  installs it on Linux and on Windows, one leg a product, a skip fails, whatever made it.

```bash
python -m pytest tests/test_fixed_deferred_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_fixed_deferred_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k MYGA_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k MYGA_US_SEC
python -m pytest tests/test_fixed_deferred_annuity_us_sec.py -q -m cython  # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-fixed_deferred_annuity-r1
[R6]: #uslib-fixed_deferred_annuity-r6
[std]: #uslib-std
<!-- END generated citation links -->
