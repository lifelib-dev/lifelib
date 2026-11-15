# In-Force Implementation Notes

**Status:** Draft, 2026-11-04. `VA_US_SEC` is [`VA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of their contract year, before or after their first
withdrawal and with their account value exhausted or not, and contracts to be written in
the ten years after it, as lifelib's `basiclife/BasicTerm_SE` extends
`basiclife/BasicTerm_S`. The product is the one [`product-spec.md`](product-spec.md)
specifies and [`technical-notes.md`](technical-notes.md) models; this page says what
running in force changes, and how the model compiles. The suffix adds lifelib's letters to
`S`: `E` for in force, as in `BasicTerm_SE`, and `C` for the compiled form, as in
`basiclife/BasicTerm_SC`: the same formulas compile under modelx-cython, from
`sample_sec.py` and `spec_sec.py` beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `VA_US_S` on another time axis. It reads `VA_US_S`'s assumption tables in place, every
> assumption unchanged, and its return and rate scenarios are `VA_US_S`'s, moved onto the
> valuation clock. The contractual elements are sourced: the 1.30% base contract asset
> charge, the $35 contract fee and the withdrawal charge scale on Remaining Premium [S2];
> the excess-withdrawal algebra and the GMDB withdrawal adjustment at Contract Year end
> [S1]; the rate-sheet parameters dated 2026-04-27, among them the 1.25% GLWB and 0.90%
> GMDB charges, the 6.00% bonus, the 6.00%/5.00% roll-up, the 105% GWB Adjustment and the
> GAWA% grid [S2] [S3]; the VIX-linked fee reset [S4] [S6] and the CMT-linked roll-up [S7].
> The dynamic lapse, the withdrawal-year factor and the maintenance expense are VM-21's
> [R1]; every other behavioural assumption is a **[std]** standardization, the return path
> is illustrative and the shipped mortality table is *not* a published basis. **Guarantee
> cost cannot be valued deterministically** [R1]: the model verifies the recursion, not the
> value of the guarantees. Replace the assumptions with company data before drawing any
> conclusion from the numbers.

## Run it

```bash
python products/variable_annuity/run_sec.py          # point 1, the anchor issued at t = 0
python products/variable_annuity/run_sec.py 2        # the worked example, in force
python products/variable_annuity/run_sec.py --block  # every point, row by row
python products/variable_annuity/run_sec.py 2 --cython  # point 2, compiled
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about four and a
half minutes, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and `.gitignore`
covers it.

The first prints point 1, the worked example's anchor cell, issued at the valuation date.
Its row `t = 26` is the worked example's month, the 27th policy month, at whose end the
ninth Contract Quarterly Anniversary falls, and the runner prints it step by step, per
contract: subaccounts of 66,000.00 and 44,000.00 at the beginning of the month, 66,666.82
and 43,796.74 after its growth, the two rider fees, 351.56 on the GWB and 252.81 on the
GMDB Benefit Base, 604.37 in all, and 66,302.07 and 43,557.12 at its end, 109,859.19; a
death benefit of 112,360.00, the Benefit Base, of which 2,500.81 is the guarantee claim;
and a GWB and a Bonus Base of 112,500.00. Its frame has 720 rows, `t = 0 … 719`: its
first withdrawal falls at `t = 120`, the start of contract year 11 at attained age 70, and
its account value runs out at `t = 228`, in contract year 20. The second prints point 2,
the notes' carried state entered as a contract in force 26 months: the same block at
`t = 0`, number for number, on a frame of 694 rows, its first withdrawal at `t = 94` and
its account value exhausted at `t = 202`. Every column of its `result_cf()`,
`result_pols()`, `result_av()` and `result_bases()` agrees with `VA_US_S`'s point 2 but
`expenses`, which are in valuation-date dollars here, 17.34 in the first month where
`VA_US_S` has 17.90, and `net_cf` with them. Three lines to the same thing for point 2:

```python
import modelx as mx
model = mx.read_model("products/variable_annuity/VA_US_SEC")
model.Projection[1].result_cf()     # point 2, the table's second row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[1]` is point 2, and its `point_id()` says so. `result_cf()` has
`VA_US_S`'s fifteen columns — `pols_if`, `premiums`, `asset_charges`, `fees_glwb`,
`fees_gmdb`, `maint_fees`, `withdrawals`, `glwb_payments`, `claims_death`, `claims_lapse`,
`claims_maturity`, `expenses`, `commissions`, `premium_taxes` and `net_cf` — with one row
per month from the valuation date, `t = 0 … proj_len() − 1`. `result_av()` has `VA_US_S`'s
values per contract on the same rows, each subaccount, the contract value before the
charges, the three charges collected by unit cancellation, the asset charge and the fund
expense, the contract value and the surrender proceeds, and `result_bases()` the guarantee
bases, the withdrawal, the death benefit and its guarantee claim, and the two moneyness
ratios, with zeros before issue. `result_pols()` sets out the counts behind `result_cf()`:
`pols_if`, `pols_new_biz`, the month's deaths, surrenders and survivors at the end of cover,
and `pols_if_aft_decr`, as in `VA_US_S` with `pols_new_biz` added. `VA_US_S` publishes no
annual report, and nor does this model: the runner sums `result_cf()` into projection years
itself, `t // 12 + 1`.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[idx]` and a
collection), so the run holds the cells of one point at a time: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees. It freezes everything alive
before each pass, so that each collection scans only what the pass has made since, and it
keeps the block's sum as it goes, compensated as pandas sums a `groupby`, so that the block
is, bit for bit, the frames concatenated and summed by `t`, as below. It lists the points,
each with where it stands at the valuation date and its frame, then prints the block's first
twelve rows and the block summed into projection years 1 to 12. The runner looks each point
up in `Projection` by its position, and passes each timing as the model's own code, so it
runs the compiled model unchanged.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the contract, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of cover, the last month before attained age 120.
- **`duration_mth(t)`, the policy clock**, counts the policy months elapsed at the start
  of month `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()`
  read from the model point's `duration_mth`. The contract runs on it, as in `VA_US_S`:
  the contract year `policy_year(t) = duration_mth(t) // 12 + 1`, the completed years
  `duration(t)`, the attained age `age(t) = age_at_entry() + duration(t)`, the contract
  quarter `contract_quarter(t) = duration_mth(t) // 3 + 1`, and the Contract Anniversaries
  and Contract Quarterly Anniversaries at the end of the months with 11, 23, 35, … and
  2, 5, 8, … policy months elapsed **[std]**. This page names a policy month by that
  count, 0 in the issue month: the notes' "27th policy month" is policy month 26.

`VA_US_S` already counts its `t` from the first month it projects and its policy months
by the same addition, and it enters its point 2 at `t = 0`, 26 months after issue. What it
lacks is a frame with edges: it opens every recursion at `t == 0`, takes the single premium
and charges acquisition there, and guards its cells with `t < 0` and `t ≥ proj_len()`.
Here a contract issued at or after the valuation date is on the books from its issue
month, `t_entry() = max(0, −duration_mth_init())`, where every recursion opens and the
premium falls; a contract in force opens at `t = 0` on the state its row carries; and cover
is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()` is `VA_US_S`'s frame from issue.

The months a formula names for the edges of month `t`'s contract year are months of the
frame, on the valuation clock: `anniv_mth(t) = t + 11 − duration_mth(t) % 12` closes the
year, and `year_open_mth(t) = t − 1 − duration_mth(t) % 12` is the month whose close opened
it. `t_of_month(m) = m − duration_mth_init()` is the month of the frame in which policy
month `m` falls, negative for one before the valuation date: the withdrawal year scans its
months from it, and the VIX-linked fee reads each quarter's VIX-squared average at the
quarter's last month.

Point 2 is the notes' carried state, in force 26 months. At `t = 0` it is in contract
year 3 at attained age 62; its third anniversary falls at the end of `t = 9`,
`anniv_mth(0) = 9`, and the year opened at the close of `t = −3`, before the valuation
date, so the year's opening values come from its row. Point 1 reaches the same month at
`t = 26`, where `anniv_mth(26) = 35` and `year_open_mth(26) = 23`, months of its own
frame. Point 12, the anchor valued at policy month 131, is in the last month of contract
year 11: `anniv_mth(0) = 0`, and the year opened at `t = −12`. Point 23 is the anchor to be
issued 15 months after the valuation date: `duration_mth(0) = −15` and
`policy_year(0) = −1`, it is on the books from `t_entry() = 15`, rows 0 to 14 are zeros,
its premium of 100,000 falls at `t = 15`, and its frame has 735 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the transaction programmes, whose `t` in `transaction_table.csv` is the elapsed policy month; the withdrawal charge scale, by completed years; the GAWA% grid, at the attained age of the first withdrawal; mortality, at the attained age; the base surrender rate and its shock year, by contract year; the start of withdrawals, in the first month of the contract year in which the attained age reaches `wd_start_age`, and of every year after it; the Bonus Period and the GWB Adjustment Date, by contract year, and the roll-up's growth cutoff and the Bonus Period's restart cutoff, by the attained age at the anniversary; the five-yearly fee increase, by completed years; the rider fees at each Contract Quarterly Anniversary, and the contract fee and the seven guarantee events at each Contract Anniversary; the end of cover, at attained age 120 | the gross fund returns, whose `t` in `return_scenario_sec.csv` is a valuation month; the quarterly VIX-squared averages and the 10-year CMT rate, whose `t` in `rate_scenario_sec.csv` is one too; expense inflation, `inflation_factor(t) = 1.025^(valuation_year − 2015 + t // 12)` |

The return and rate scenarios are paths in calendar time, shared by every contract of a
block, so they move to `t`. `VA_US_S` keys them by the elapsed policy month, the `t` of
`return_scenario.csv` and `rate_scenario.csv`, so each of its contracts reads the path from
its own issue. Its `base` path sets returns at policy months 0, 12, 24, 26 and 27,
reverse-engineered so that the anchor's contract value is 104,000.00 and 112,500.00 at
anniversaries 1 and 2, and 110,000.00, split 66,000 and 44,000, entering the 27th policy
month, whose returns are the worked example's +1.20% and −0.30%. Point 1, issued at the
valuation date, reads that month at `t = 26`, and point 2, in force 26 months, at `t = 0`,
so no one path keyed by valuation month reproduces both. So `return_scenario_sec.csv` and
`rate_scenario_sec.csv`, which the generator writes from `VA_US_S`'s scenarios, hold each
of them under its own id, which the points issued at the valuation date read, and, for
every row valued in force or issued later, a copy of its scenario under an id of its own,
named by the months it moves: `base-M26` for point 2, `decline-M144` for point 13,
`variant-M41` for point 17, `base-M40` for points 16 and 20 and so on, and `base-F15` for
point 23; 60 rows of returns and 18 of rates, in seventeen scenarios each. In the copy for
a row valued at policy month `m` the levels `VA_US_S` set before `m` collapse to the one in
force at `m`, at `t = 0`, and the later rows move `m` months earlier, each subaccount's
returns on rows of their own: `base-M26` holds +1.20% and −0.30% at `t = 0`, and 0.50% and
0.20% from `t = 1`. The copy for a row issued `k` months on moves `k` months later and sets
nothing before its issue month. So every row reads each policy month's return and rate at
the valuation month in which that policy month falls, and the model reproduces `VA_US_S`
there. The copies are what reproduce `VA_US_S`'s contracts, each on the path from its own
issue; the contracts of a block valued at one date would read one path, the market as it
moves from the valuation date.

The copy is moved by the row's own `duration_mth`, the policy months elapsed at the
valuation date, not by the S month it was taken from. `VA_US_S` projects its point 2 from
the valuation date, so a row restated from it at S month `d` is in force `26 + d` months:
point 20, `VA_US_S`'s point 2 at its month 14, is in force 40 months and reads `base-M40`,
the copy point 16, `VA_US_S`'s point 5 at its month 40, reads too.

`VA_US_S` reads a month before a contract's issue at its issue month,
`max(duration_mth(t), 0)`, which none of its points reaches. Here no cell reads a scenario
outside cover: `inv_return_mth(t, i)` and `scenario_rate(t, name)` take the last row of the
point's scenario at or before `t`, which `Data` holds step-filled by month, and raise,
naming the point, where there is none, behind `Data`'s refusal of a point whose scenario
sets nothing by its first month on the books. The VIX-squared average of contract quarter
`k` is the rate scenario's level at the valuation month of the quarter's last policy month,
`vix_sq(k) = scenario_rate(t_of_month(3k − 1), VIX_SQ)`, read only for quarters on the
books. A past VIX reaches the projection only through the rate of the quarter before the one
under way, the clip's prior, which is the model point's `phi_glwb_init` (below), so no
column holds a level the scenario also sets.

Expense inflation counts the years from the valuation date, `t // 12`, on top of the years
from VM-21's expense base year, 2015, to the valuation year, 2026 [R1], so the maintenance
expense, $100 a contract a year inflating at 2.5%, plus 7 basis points of the account
value, is in valuation-date dollars for every point alike: 10.93 a contract a month at
`t = 0` before the account-value part. `VA_US_S` counts the contract's own completed
years, `duration(t)`, which is `t // 12` on a contract issued at the valuation date and
mixes the two clocks on any other: on point 2 its factor is `1.025^2` higher in the first
ten months of each projection year and `1.025^3` in the last two, where the contract has
passed an anniversary and the projection year has not. Acquisition, 0 as shipped
**[std]**, is charged per contract issued, in the issue month and not inflated, as in
`basiclife/BasicTerm_SE`; `VA_US_S` charges it at `t = 0`, which on its point 2 is a month
in force. The commission and the premium tax, 0 as shipped, fall on every premium as in
`VA_US_S`: the single premium in the issue month and any premium a programme schedules
after it.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf()
          for i in range(len(model.Data.model_point_table()))]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`VA_US_S` computes, whatever the point's count: `VA_US_S` already weights its premium by
the contracts in force and charges acquisition at `t = 0`, which on new business is the
issue month. On `VA_US_S`'s eight new-business points every cash flow, every count and
every value per contract agrees, and so does every other cell the two models share, but
those whose meaning changed: `pols_if_init()`, now the count already in force at the
valuation date, 0 for new business; `model_point()`, a row of another table; and
`result_pols()`, which gains `pols_new_biz`. No cell of `VA_US_S`'s is removed.
`VA_US_S`'s point 2 continues `VA_US_S`'s projection from the valuation date, every count,
cash flow and value per contract `VA_US_S`'s but the maintenance expense, and `net_cf`
with it, so the worked example's goldens hold here on point 1 at `t = 26` and on point 2
at `t = 0`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `VA_US_S`'s columns,
`av_init` apart and nine of them renamed, and twenty-two of its columns are the in-force
interface: `basiclife/BasicTerm_SE`'s two, and twenty that open an in-force contract's
state. Each is a number or a flag, and every amount is per contract.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the contract's age in months: positive in force, in any month of its contract year, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `sa_pp_init_1`, `sa_pp_init_2` | dollars | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the value of each subaccount, one column for each subaccount a fund set of `fund_table.csv` holds, blank on a point whose set lacks it; their sum is the account value, 0 on a contract whose account value has run out, or the rounding of either sign about 0 that the depletion closed on |
| `gwb_pp_init` | dollars | the start of month 0 | the Guaranteed Withdrawal Balance [S1] |
| `bb_pp_init` | dollars | the start of month 0 | the Bonus Base, on which the bonus is credited [S1] |
| `gawa_pp_init` | dollars a year | the start of month 0 | the Guaranteed Annual Withdrawal Amount, 0 before the GAWA% is locked; on a contract whose account value has run out, what the GLWB pays at each contract year's start |
| `rb_pp_init` | dollars | the start of month 0 | the GMDB Benefit Base |
| `np_pp_init` | dollars | the start of month 0 | the cumulative Net Premiums, the floor under the death benefit that no withdrawal reduces |
| `rp_pp_init` | dollars | the start of month 0 | the Remaining Premium, on which the withdrawal charge is taken [S2] |
| `adj_pp_init` | dollars | the start of month 0 | the GWB Adjustment [S3], 0 once a withdrawal has voided it or its date has passed |
| `gawa_pct_init` | a fraction of the GWB | the start of month 0 | the GAWA% locked at the first withdrawal, or at the attained age at which the account value ran out where that came first [S1] [S3]; 0 before either |
| `bonus_end_init` | a contract year | the start of month 0 | the contract year in which the Bonus Period ends, ten years from issue or from the last step-up that restarted it [S1] |
| `has_wd_init` | a flag, `True` or `False` | the start of month 0 | whether a withdrawal has been taken since issue |
| `sum_wd_pp_ytd_init` | dollars | the start of month 0, in the contract year under way | the gross withdrawals taken in the year so far, the notes' `SumW_y` |
| `free_wd_used_cum_pp_ytd_init` | dollars | likewise | the part of the free-withdrawal allowance those withdrawals used |
| `gmdb_dfd_acc_pp_ytd_init` | dollars | likewise | the GMDB's dollar-for-dollar reduction accrued in the year so far, applied at the year's end [S1] |
| `gmdb_factor_acc_ytd_init` | a factor from 0 to 1 | likewise | the GMDB's proportional factor accrued in the year so far, applied at the year's end, 1 where no withdrawal has gone past the allowance **[std]** |
| `wd_this_year_init` | a flag | likewise | whether the year under way took a withdrawal before month 0 |
| `rb_pp_prev_anniv_init` | dollars | the anniversary on or before the valuation date, the one that opened the contract year under way: the close of policy month `12 × duration(0) − 1` | the GMDB Benefit Base there, the base of the year's dollar-for-dollar allowance [S1] |
| `stepup_base_pp_ytd_init` | dollars | the Contract Quarterly Anniversaries of the year under way before the valuation month | the largest account value at them, on any step-up basis, the history the highest-quarterly step-up base alone reads [S1]; 0 where none has passed |
| `phi_glwb_init` | a rate a year | the last contract quarter to end before the valuation month | on the VIX-linked fee, that quarter's GLWB charge rate, the prior the clip moves the first rate on the books from [S4]; 0 in the first quarter and on the other fee rules |

On a point issued at or after the valuation date every one of the twenty is 0, or `False`,
the factor included: such a contract opens with nothing, and its issue values arrive in its
issue month. On a point valued at a contract year's start, `duration_mth` a positive
multiple of 12, the year to date is empty, three sums of 0 and a factor of 1, the year's
flag `False`, and the Benefit Base at the anniversary is the one entering month 0, the two
instants being one. In the first contract year, `duration_mth` 1 to 11, the year opened at
issue, so the Benefit Base at the anniversary is the issue value, the premium credited at
issue. Before the year's first Contract Quarterly Anniversary, `duration_mth % 12` below 3,
no quarter of the year has ended, and the highest quarterly value is 0. `prev_anniv` is the
anniversary that **opened** the contract year: an extract that fills the column from the
anniversary after the valuation date is a year out.

Each column is read where the contract needs it, and only there:

- `sa_pp_init_1` and `sa_pp_init_2` open the subaccounts' monthly chains, `sa_pp(t, i)`,
  at `t_entry()`, through `Data.sa_pp_init_array()`, and their sum is the account value
  entering month 0, `av_pp_init()`.
- The seven bases, the GAWA% and the Bonus Period's end open their own chains at
  `t_entry()`, and `has_wd_init` opens the withdrawal status, `has_wd_by`, which the
  first-withdrawal test, the GAWA's increase on a later premium, the GWB Adjustment and the
  CMT-linked roll-up's spread read.
- The four `_ytd_init` columns open the year to date where the year under way opened before
  the valuation date: `sum_wd_pp`, which the excess test adds each withdrawal to;
  `free_wd_used_cum_pp` and `free_wd_avail`, the free allowance left for a withdrawal and
  for a surrender; and `gmdb_dfd_acc_pp`, `gmdb_wd_dfd_pp` and `gmdb_factor_acc`, the GMDB's
  adjustment, applied at the year's end.
- `wd_this_year_init` answers for the months of the year under way before `t = 0` in
  `is_wd_year`, which the bonus and the surrender rate's withdrawal-year factor read.
- `rb_pp_prev_anniv_init` is the year's opening Benefit Base where the year opened before
  the valuation date, read by `rb_prior_anniv_pp`, the base of the dollar-for-dollar
  allowance.
- `stepup_base_pp_ytd_init` joins the quarter ends on the books in the step-up base at the
  anniversary closing the year under way, and at no other, on the highest-quarterly basis
  alone.
- `phi_glwb_init` is the prior the clip moves the VIX-linked rate from in the quarter under
  way at the valuation date, read by `phi_glwb_vix`.

Everything else the projection uses is fixed at issue, in `VA_US_S`'s columns, or follows
from the policy clock. The depleted status needs no column: a contract in force enters
month 0 depleted exactly where its opening account value is at or below the threshold
(below).

| `VA_US_S` | `VA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1) | `policy_count` | The count, under `BasicTerm_SE`'s name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth_init`: 0, or 26 on point 2 | `duration_mth` | The policy months elapsed at the valuation date, under `BasicTerm_SE`'s name. `VA_US_S` takes a contract at issue or in force, never one to come; here 0 or less is new business |
| `av_init` | `sa_pp_init_1`, `sa_pp_init_2` | `VA_US_S` splits the account value it enters by the target allocation, `alloc(i) × AV`, which holds at the target only: the subaccounts grow apart (below) |
| `gwb_init`, `bb_init`, `gawa_init`, `rb_init`, `np_init`, `rp_init`, `adj_init` | `gwb_pp_init`, `bb_pp_init`, `gawa_pp_init`, `rb_pp_init`, `np_pp_init`, `rp_pp_init`, `adj_pp_init` | Renamed after the cell each opens |
| `gawa_pct_init`, `bonus_end_init` | `gawa_pct_init`, `bonus_end_init` | Kept |
| — | `has_wd_init` | `VA_US_S` infers a withdrawal from a GAWA% above 0, which a depletion without a withdrawal also locks (below) |
| — | `sum_wd_pp_ytd_init`, `free_wd_used_cum_pp_ytd_init`, `gmdb_dfd_acc_pp_ytd_init`, `gmdb_factor_acc_ytd_init` | `VA_US_S` restarts the year to date at `t = 0`, as though every valuation were a contract year's start |
| — | `wd_this_year_init` | `VA_US_S`'s `is_wd_year` scans the year from `t = 0` only |
| — | `rb_pp_prev_anniv_init` | `VA_US_S` takes the Benefit Base at `t = 0` before the withdrawal, `rb_pp_at(0, "BEF_WD")`, for an anniversary before its frame |
| — | `stepup_base_pp_ytd_init` | `VA_US_S` leaves out every quarter end before `t = 0` |
| — | `phi_glwb_init` | `VA_US_S` recurses the VIX-linked rate from the first contract quarter, through fixings before its frame |

A column measured entering month 0 is the cell it opens with `_init` added, `gwb_pp_init`
for `gwb_pp`; a value of the contract year to date adds `_ytd_init`, since the cells'
names do not say that they restart each year; and a value at the anniversary on or before
the valuation date adds `_prev_anniv_init` instead.

On twins 1 and 3 to 9 the twenty are 0, the state of a contract entering its issue month,
and each takes its issue values in month 0, as its `VA_US_S` row does. Twin 2 is
`VA_US_S`'s point in force, and it carries `VA_US_S`'s columns, with what `VA_US_S`
itself assumes for the columns it has none for: its account value of 110,000.00 split by
the 60/40 allocation, 66,000.00 and 44,000.00, which the notes' carried state holds; no
withdrawal, as its GAWA% of 0 says; an empty year to date; a Benefit Base at the
anniversary of 112,360.00, its entering one, which is `VA_US_S`'s fallback on a month with
no premium; and no quarterly history or VIX prior, `VA_US_S`'s frame holding no month
before its `t = 0`.

The columns carried over are read as `VA_US_S` reads them. For a contract in force, the
facts they record are still those at issue:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `designated_lives`, `tax_status` | codes, as in `VA_US_S`'s table; the last two reported, not modelled | issue |
| `premium` | dollars, the single purchase payment | issue |
| `premium_tax_rate` | a fraction of each premium | issue |
| `fund_set`, `glwb_option`, `cdsc_schedule` | keys into `fund_table.csv`, the subaccounts with their allocation and fund expenses; `gawa_pct_table.csv`, the GAWA% grid; and `cdsc_table.csv`, the withdrawal charge scale | issue: the contract's provisions |
| `glwb_stepup_basis`, `gmdb_option`, `fee_reset_rule`, `rollup_rule` | codes, as in `VA_US_S`'s table | issue: the contract's provisions |
| `wd_start_age`, `wd_intensity` | an attained age, 0 for never; a fraction of the annual limit | assumptions of the base run: when withdrawals begin, and how much of the limit they take |
| `scenario_id`, `txn_id` | keys into the two scenario companions and `transaction_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `VA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the in-force columns are present, the subaccount values apart, which are checked with the
  fund sets, below;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `age_at_entry`, `wd_start_age` and `bonus_end_init` are whole numbers, 0 or more:
  `VA_US_S` reads each by `int()`, which would truncate a fraction without a word;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,080 months at issue age 40, the youngest the shipped
  mortality table rates. Set to 0, the Reference refuses future new business altogether,
  and says so; a negative horizon is itself refused;
- `has_wd_init` and `wd_this_year_init` are `True` or `False`, read by value, as `True`,
  `False`, `1` or `0`: one cell written as text turns the column to text as pandas reads
  it, so `"True"` and `"False"` are read as the flags they name, and anything else, a blank
  among them, is refused;
- the premium and the withdrawal intensity are each a finite number, zero or more, and the
  premium tax rate a number from 0 to below 1;
- the twelve amounts of the opening state are each a finite number, zero or more, and the
  GAWA%, the GMDB's proportional factor and the VIX prior each a number from 0 to 1;
- a contract not yet in force, `duration_mth` 0 or less, has an opening state of zeros, the
  flags `False` and the factor 0;
- on a contract valued at a contract year's start the year to date is empty, exactly, the
  year's flag is `False`, and the Benefit Base at the anniversary equals the one entering
  month 0, exactly: the two instants are one;
- before the contract year's first quarterly anniversary, `duration_mth % 12` below 3, the
  highest quarterly value is 0;
- the VIX prior is 0 on a contract in force unless it is on the `vix` rule and past its
  first contract quarter, `duration_mth` 3 or more: before then, and off the rule, no
  quarter's rate is the clip's prior;
- in the first contract year the Benefit Base at the anniversary is the issue value, to a
  cent: the premium credited at issue,
  `(premium + the programme's month-0 premium) × (1 − premium_tax_rate)`;
- in force, the Bonus Period's end is a contract year, 1 or more;
- a contract that has withdrawn has no GWB Adjustment, any withdrawal voiding it;
- a GAWA above 0 has a GAWA% above 0, the GAWA being that percentage of a base;
- off a contract year's start, a withdrawal this year is a withdrawal, so the year's flag
  needs `has_wd_init`; withdrawals to date above 0 need the year's flag; the free allowance
  used and the dollar-for-dollar reduction are each part of the withdrawals to date, so
  neither exceeds them by more than a cent; and the proportional factor is below 1 only
  where the year has withdrawals;
- last, each point's keys into the tables it is joined with: its `fund_set` is a set of
  `fund_table.csv`, and each subaccount the set holds has its `sa_pp_init_<i>` column, a
  finite number, zero or more to within 1e-8, and 0 on a contract not yet in force; its
  `scenario_id` is a scenario of `return_scenario_sec.csv` that sets a return for each of
  those subaccounts by the first month the point is on the books, `t = 0` or its issue month
  if later, and, on a point the `vix` fee or the `cmt_linked` roll-up reads it for, one of
  `rate_scenario_sec.csv` that sets its levels by then; its `txn_id` is a programme of
  `transaction_table.csv`; its `glwb_option` is a grid of `gawa_pct_table.csv`, and, in
  force, `has_wd_init` needs a GAWA% above 0 unless that grid gave 0% at an attained age the
  contract reached before the valuation month, since the first withdrawal locks the
  percentage of the age it is taken at, and a GWB and a GAWA% above 0 need a GAWA above 0
  under the same proviso, since the withdrawal or the depletion that locked the percentage
  set the GAWA to it times the GWB, and nothing after takes the GAWA to 0 while a GWB is
  left (`Data.model_point_table` reads the grid at those ages); its `cdsc_schedule` is a
  schedule of `cdsc_table.csv`; and `mort_table.csv` gives a rate at its `sex` and its
  attained age in its first month on the books. So reading the model point table reads every
  assumption table, checked. `VA_US_S` meets a key its table lacks only as it projects: a
  missing fund set, scenario, grid, schedule, sex or age raises Python's own `KeyError`,
  naming no file, and a missing transaction programme schedules nothing, without a word.

The checks run in that order. The rules that hold at a contract year's start and those that
hold off it never apply to the same point, so that a value a year's start fixes is refused
by the rule that fixes it. Amounts of money are compared to a cent, so that an extract may
carry each to the cent, as an administration system holds it: each amount so carried is
within half a cent of its exact value. Two columns that hold one amount at instants that
coincide, at a year's start, are compared exactly. A subaccount value is held to 0 or more
to within 1e-8, not a cent, since a contract that opens depleted has its account released in
month 0 with no flow, and `check_av_roll_fwd`, at 1e-6 a contract, would miss by a cent
below 0 left there: `VA_US_S` runs an account down by scaling each subaccount by one less
the share of the account a charge or a withdrawal takes, so a depletion can close on a
rounding of either sign about 0, of the order of 1e-14, the one amount of the opening state
its arithmetic leaves below 0, the bases being held at 0 or more by its floors. On
`VA_US_S`'s shipped points and inputs every depletion closes on exactly 0. Under the
splice's References with no premium tax its never-withdrawing roll-up closes at policy month
524 on 5.7e-15, and its never-withdrawing return of premium at 659 on −2.3e-14; and under
the shipped References, untaxed too, that return of premium issued at 55 or 56 closes at 752
on −1.1e-13. The generated rows carry `VA_US_S`'s own values, unrounded, such a rounding
among them.

Accepted, because a contract can be in each state: an account value of 0 in force, where
the GLWB pays on and the projection reads the contract as depleted from month 0, or the
rounding about 0 a depletion closed on, above it or below it, which the same test reads as
depleted; a GAWA% above 0 with no withdrawal taken, where the account value ran out first;
free allowance
used and a dollar-for-dollar reduction above what the month allows at the valuation date,
since the allowance is recomputed every month from the earnings and the Remaining Premium;
`has_wd_init` with a GAWA% of 0, or a GWB with no GAWA, where the grid gave 0% at an age
the contract reached, as below a grid's first band; every value at each bound its rule
includes, an allocation, a fund expense, a GAWA%, a withdrawal charge or a mortality rate of
0 or 1, a return or a CMT just above −1, and a premium, a withdrawal intensity or a premium
tax of 0, among them; a `duration_mth`, an age or `bonus_end_init` written as a float, and
a flag written as 1 or 0, or as 1.0 or 0.0, read as the value each holds; and an extract
whose every amount is carried to the cent.

Left to the projection, because each needs a `Projection` Reference, which `Data` cannot
read, and refused by `proj_len()`, naming the point. It refuses a point at or past the end
of cover at the valuation date, `duration_mth ≥ 12 × (120 − age_at_entry)` at the shipped
`omega_age`, and a point issued at or past `omega_age`, whose cover from issue is empty and
which would otherwise project a frame of zeros; on the shipped tables the mortality check
refuses an attained age past 120 first, the table's last. And on a contract in force it
refuses, in this order, an opening state that a rule turning on depletion or on a rate
Reference forbids. A contract in force is depleted exactly where its opening account value
is at or below `av_depletion_threshold`, which the projection derives. So:

- a contract depleted at the valuation date carries an account value of 0, to within 1e-8:
  depletion releases the account in month 0 with no flow, so `check_av_roll_fwd` would miss
  by any more, and `VA_US_S`'s depletions close on roundings of the order of 1e-14;
- a contract that has neither withdrawn nor depleted has no GAWA% locked, the percentage
  locking at the first withdrawal or at depletion, and so no GAWA;
- one depleted without a withdrawal has a GAWA% above 0, the grid's at the age its account
  ran out at, unless its grid gave 0% at an age it reached before the valuation month,
  which `Data.gawa_pct_zero_by_point()` gives `proj_len()`, a vector built in `Data`, so
  that the projection reads no grid at an age before its books;
- on the highest-quarterly basis, one not depleted and three months or more into its
  contract year has a step-up history above the threshold: depletion is absorbing, so every
  quarter end of the year before the valuation month closed above it;
- on the `vix` fee rule, in the second contract quarter, `duration_mth` 3 to 5, the VIX
  prior is the first quarter's rate, `phi_glwb_curr`; and from the third quarter it is at
  most `vix_corridor_hi`, and at least `vix_corridor_lo` where `phi_glwb_curr` is, the
  corridor running upward, since the clip holds every rate after the first at most at the
  corridor's top, and from a first rate at or above its foot, at least at its foot.

So a loop over the block meets such a row only when it reaches it, after projecting the
points before it, and `run_sec.py --block` asks every point for its frame before it
projects any, and stops before it prints anything. The rest of the year to date, the
step-up history and the VIX prior are history, which nothing here can check beyond these
rules.

Five of the seven assumption tables are `VA_US_S`'s files, read in place, and the other two
are the generated `return_scenario_sec.csv` and `rate_scenario_sec.csv`. All seven are read
by `VA_US_S`'s readers, and their keys and values are checked as well. Beside each reader a
`Data` cell reads the table's keys by value, once, checks them and the table's values, and
returns the table indexed by the checked keys, and the projection reads the table there and
nowhere else: `mort_rates`, `fund_sets`, `return_scenario_steps`, `rate_scenario_steps`,
`gawa_pct_bands`, `cdsc_scale` and `transactions`. The mortality table's last age, at which
every older age is read, is an int cell, `mort_last_age()`, taken from the same checked
ages. A key written `1.0` is 1, as `VA_US_S`'s lookups match it. A key that is not a whole
number, text and a blank among them, a blank text key, a value that is not a number in its
range, blank, text and infinite values among them, a repeated key, a fund set whose
allocations do not sum to 1, and, where the projection reads every age or year between a
table's first and last, mortality ages or withdrawal charge years that leave a gap are
refused, naming the file and the lines, before a projection reads a value from the table;
for those two the message names each repeated key with its lines and each key or span of
keys missing, every fault in one message. The GAWA% grid is banded, so its ages need not run
one a year, and a scenario may start after `t = 0`, for business issued later, so the month
it must start by is the point's, which the model point table's checks hold. `VA_US_S` takes
the keys as pandas reads them: one written as text turns its whole column to text, so that
every scheduled premium and withdrawal is then zero without a word, and every other lookup
on the column raises Python's own `TypeError`, `KeyError` or `ValueError`, naming no file.
Every value a `min` or a `max` reads is refused blank, as text or infinite, since `min` and
`max` lose a NaN in a later argument without a word.

## The model points

No row of `model_point_table_sec.csv`, `return_scenario_sec.csv` or
`rate_scenario_sec.csv` is typed by hand. Every one is generated from `VA_US_S` and its
inputs by `tests/sec_support.py`, from the `VA_US_SEC` entry in its `SEC_SPECS`, and the
tests regenerate the three files and compare, so an edit to a `VA_US_S` row or scenario
reaches them or fails the suite. In the source repository,
`python tools/gen_sec_points.py VA_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 3 to 9 | twin | S points 1 and 3 to 9 | issued at `t = 0`: the anchor, projected from issue on the reverse-engineered `base` path; a sustained decline to exhaustion, on `decline`; the excess-withdrawal programme, 20,000 at policy month 60 and a further premium of 25,000 at 72; the highest-quarterly step-up basis with the annual-ratchet GMDB; the VIX-linked fee and the CMT-linked roll-up, on `variant`; a contract that never withdraws, on the return-of-premium death benefit with no withdrawal charge and the five-yearly fee increase; another on the Roll-up GMDB, whose account value the rider fees exhaust at `t = 554`; and the return of premium withdrawing from attained age 70 |
| 2 | twin | S point 2, in force at 26 | the notes' carried state at the beginning of the 27th policy month, on `VA_US_S`'s own columns: the worked example's month is its `t = 0`, on `base-M26` |
| 10 | derived | S point 1 at S month 6 | the anchor in its first contract year, the year's opening Benefit Base its issue value, 100,000.00, and two of the year's quarter ends, policy months 2 and 5, behind it |
| 11 | derived | S point 1 at S month 120 | the anchor at the start of contract year 11, attained age 70, taking its first withdrawal at `t = 0`: a GWB of 166,500.00, the Adjustment of 105,000.00 still in force, and subaccounts of 71,849.14 and 36,585.76 |
| 12 | derived | S point 1 at S month 131 | the same contract in that year's last month, after its first withdrawal: 9,573.75 withdrawn this year, all of it inside the GMDB's dollar-for-dollar allowance |
| 13 | derived | S point 3 at S month 144 | the declining point at the start of contract year 13, its account value exhausted, paid its GAWA of 9,200.00 at `t = 0` |
| 14 | derived | S point 4 at S month 60 | the excess programme at the start of contract year 6, taking its withdrawal of 20,000 at `t = 0`, in the 4% charge year |
| 15 | derived | S point 4 at S month 65 | the same contract five months on: 20,000.00 withdrawn this year, 10,262.37 of free allowance used, a dollar-for-dollar reduction of 8,029.35 and a proportional factor of 0.882908; its further premium at `t = 7` |
| 16 | derived | S point 5 at S month 40 | the highest-quarterly point mid-year in contract year 4, its account value at the year's first quarter end, 110,132.46, before the valuation month |
| 17 | derived | S point 6 at S month 41 | the VIX-fee point in the last month of contract quarter 14, the prior quarter's rate of 1.6626% from its row, and the CMT-linked roll-up before any withdrawal |
| 18 | derived | S point 8 at S month 560 | the never-withdrawing Roll-up point after its account value has run out without a withdrawal: `has_wd_init` `False`, with a GAWA% of 6.2% locked at depletion |
| 19 | derived | S point 7 at S month 719 | the never-withdrawing return of premium in its last policy month, at attained age 119: a one-row frame |
| 20 | derived | S point 2 at S month 14 | `VA_US_S`'s point in force restated 14 months on, in force 40 months: its scenario's copy moves by 40, not 14, and is the one point 16 reads, `base-M40` |
| 21 | derived | S point 9 at S month 125 | the withdrawing return of premium five months after its year's withdrawal of 9,744.58, its Benefit Base reduced in proportion to 91,983.20 |
| 22 | derived | S point 7 at S month 100 | the never-withdrawing return of premium before its GWB Adjustment Date, `t = 43`, the Adjustment of 105,000.00 carried |
| 23 | future | S point 1, 15 months on | to be issued at `t = 15` |

A derived row's `policy_count` is the count `VA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `VA_US_S` carries into it, each column read as
`VA_US_S`'s own formulas read it: the subaccount values, a column for each subaccount in the
fund table of the `VA_US_S` the generator reads, so that a fund table given a subaccount
gives the table its column, the seven bases, the GAWA%, the Bonus Period's end and the
withdrawal status at the close of S month `d − 1`; the year to date at that close in the
year under way, and empty at a year's start; whether the year has taken a withdrawal, from
the year's months of S's frame before `d`; the Benefit Base opening the year, S's own
`rb_prior_anniv_pp(d)`; the largest account value at the year's quarter ends before `d`;
and, on the VIX-linked fee, S's rate of the quarter before. So the row continues the S
projection from there: point 10 opens with 0.977100 contracts, point 11 with 0.495831, point
12 with 0.468807, point 13 with 0.527147, point 18 with 6.916464e−05 and point 19 with
2.039028e−13. Its `policy_id` is the S row's with the month appended, `VA-000001-M120`, and
its scenario's id is the S scenario's with the policy months elapsed at the valuation date,
`base-M120`; a future row's carry the months to issue, `VA-000001-F15` and `base-F15`. Row
`t` of a generated point is month `t + source_mth` of its S point. All twenty-three are
contracts on the anchor cell, a male life issued at 60 ANB, single life and non-qualified,
on a $100,000 premium allocated 60/40, as every `VA_US_S` point is, differing only in the
switches the notes make first-class parameters; the shipped mortality table starts at
attained age 40.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
four timings, in processing order, each an int code named as `VA_US_S`'s text (*The compiled
model*, below):

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_LAPSE`, after the month's deaths;
- `AFT_DECR`, after its surrenders, the notes' `l(t)`, the count at the end of the
  month.

The first two are `basiclife/BasicTerm_SE`'s, and the other two `VA_US_S`'s, unchanged
but for their guard outside cover. `BEF_DECR` already meant in `VA_US_S` what it means in
`BasicTerm_SE`, so no name clashes, and `BEF_NB` is the one timing running in force adds.
Any other timing raises. `BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a month
before its maturities, is not adopted: the contracts here leave at the end of the last
covered month, as `pols_maturity`, where `VA_US_S` puts its horizon.

The survivors carried into month `t` are those of month `t − 1`'s `BEF_DECR` count, which
`BEF_NB` forms itself, as its own value at `t − 1` plus that month's new business, through
the month's deaths and surrenders in the order `AFT_DECR` takes them, **death first, then
surrender** **[std]**. So `pols_if_at(t, AFT_DECR)` is `pols_if_at(t + 1, BEF_NB)` in
every month but the last covered one, where the survivors leave as `pols_maturity`. Both
decrements are monthly rates converted from the annual ones, `1 − (1 − q)^(1/12)`
**[std]**, so that every anniversary count is the annual grid's.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `VA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `VA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing account value, `av_at(t, EOM)`, is weighted
by `pols_if_at(t + 1, BEF_NB)`, the contracts left once the month's decrements have
gone, before the next month's new business, and every other timing of `av_at` by
`pols_if(t)`.

The single premium and acquisition fall in the issue month, the one with
`duration_mth(t) = 0`: `t = 0` on the twins issued at the valuation date, `t = 15` on
point 23, and never on a point already in force, which paid its premium before the
valuation date. The guarantee bases take their issue values from it there, by `VA_US_S`'s
own rules, and the Bonus Period's end opens at `bonus_period_years`. The contract is
flexible-premium, so a premium a programme schedules after issue falls on every contract
then in force, weighted by `pols_if(t)` as every cash flow is: `VA_US_S`'s point 4 pays its
further premium of 25,000 at policy month 72, on twin 4 at `t = 72`, on 0.772986
contracts, 19,324.64 in all, and on point 15 at `t = 7`. In the issue month `pols_if(t)` is
the count issued, so the purchase payment needs no case of its own.

The subaccount and account values are read at five instants of the month, `VA_US_S`'s
`sa_pp_at(t, i, timing)` and `av_pp_at(t, timing)`: `BEF_PREM`, the opening balance,
which at `t_entry()` is the model point's `sa_pp_init(i)` and `av_pp_init()`, 0 on new
business; `BEF_WD`, after the premium has bought units; `BEF_INV`, after the
withdrawal; `BEF_FEE`, after the month's growth; and `EOM`, after the charges,
`sa_pp(t, i)` and `av_pp(t)`. The guarantee bases, `gwb_pp_at`, `gawa_pp_at` and
`rb_pp_at`, take `BEF_PREM`, which opens on the base's `_init` column at `t_entry()`,
`BEF_WD` and `BEF_ANNIV`; their closing values, after the anniversary events, are
`gwb_pp`, `gawa_pp` and `rb_pp`.

The three checks are loops over the frame. The account value's and the count's scale their
tolerance with `policy_count`, since a residual is rounding on that many contracts: the
References `check_tol_av` and `check_tol_pols`, `VA_US_S`'s 1e-6 and 1e-12 on a point
counting one contract, times `max(policy_count(), 1)`. The charge split, an identity per
contract, keeps `check_tol_charge`, `VA_US_S`'s 1e-8. Each fails at the first month whose
residual is not strictly inside its bound, so a residual that is not a number fails, as it
fails `VA_US_S`'s strict bound. The count's residual and `av_at(t, EOM)` are 0.0 outside
cover before either reads `t + 1`, so that at `t = proj_len()` nothing reads a month past
the frame; `VA_US_S` guards both only below `t = 0`.

Every chain runs one cell a month back to `t_entry()`: the count, through `BEF_NB`; each
subaccount, `sa_pp(t, i)`, with the month's steps written inline, where `VA_US_S`'s ran
through two cells a month, `sa_pp` and `sa_pp_at`; the guarantee bases `gwb_pp`, `bb_pp`,
`gawa_pp`, `rb_pp`, `np_pp`, `rp_pp` and `adj_pp`, the last inline too, where `VA_US_S`'s
read `adj_pp_bef_anniv`; the statuses `has_wd_by`, `depleted_flag`, `gawa_pct_fixed` and
`bonus_end`; the year to date, `sum_wd_pp`, `free_wd_used_cum_pp`, `gmdb_dfd_acc_pp` and
`gmdb_factor_acc`; and the VIX-linked rate, `phi_glwb_vix(k)`, one cell a quarter from the
quarter under way at `t_entry()`. Each reads its previous month first, then the month's
steps, so a cold call walks the chain once. A cold `net_cf` in the last month runs one cell
a month back to `t_entry()` and at most 15 more on the committed points: 735 cells deep on
point 1's 720-month frame, against 1,447 in `VA_US_S`, and 708 on point 2's 694 months,
against 1,395. A chain head called cold alone runs at most 17 more, `bonus_end` and
`gmdb_factor_acc` on twin 4, whose first month opens the withdrawals', the bases' and the
account value's chains beneath them. A cold count alone, `pols_if`, runs up to 20 more than
its months: its first month's surrender rate reads that contract year's withdrawal year at
the anniversary closing it, up to 11 months on (below), which opens the withdrawals' chain
beneath it. At the contract's longest cover from issue, 1,020 months from issue age 35, the
youngest the GLWB is issued at, measured on a mortality table extended below its first age,
40, a cold `net_cf` runs 1,035 deep and a cold `pols_if` 1,040, and a point issued 120
months on runs no deeper, because its chains stop at its issue month. The compiled model
sizes its `t` cache from that contract issued 120 months on: its frame of 1,140 months and
the month after it, 1,141 values, and one of headroom (*The sample and the spec*, below).
Each report evaluates its columns in ascending `t`, and a sweep of the committed points that
way reaches a depth of 569 cells, on point 8, where `VA_US_S`'s sweep of its point 8 reaches
1,123: the contract never withdraws, its account value runs out at `t = 554`, and its GAWA,
locked there, is first read by the payment that opens contract year 48, at `t = 564`, whose
chain then runs back to the books' first month. So the tests sweep the committed points
under a recursion limit of 600, which a recursion backward over the frame would exceed.

One read reaches ahead of its month, and only one kind. The surrender rate's
withdrawal-year factor, 0.60 in a contract year that takes a withdrawal [R1], is a
property of the year: `lapse_wd_factor(t)` reads `is_wd_year` once, at `anniv_mth(t)`, the
month closing the year, up to 11 months after `t`, the same value as `VA_US_S`'s
`is_wd_year(t)`, which scans the whole year. That anniversary lies inside the frame, since
cover ends at the close of a contract year, and the year's answer there rests on no count,
no decrement and nothing after it, so the read opens no chain past it; `is_wd_year` itself
scans no month after its own, being read at a year's last month only, here and by the bonus
at the anniversary. Called at another month of the year, as the compile tests' full sweep
calls every cell at every month, it answers the same and scans the year's months after it,
inside the frame: a read past `t + 1` that no cell of the model makes. On point 1 the factor
is 1.00 to `t = 119` and 0.60 from `t = 120`, the month of the first withdrawal, to `t =
239`, the close of the contract year in which its account value runs out, each of those
years withdrawing in its first month. Every other read goes no further than `t + 1`: the
block's closing account value, weighted by the next month's count, and the count's
roll-forward, which reads that count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()`, the policy month of attained age `omega_age`, 120:
720 months at issue age 60. Outside it, before issue and from the end of cover on, every
count is zero, and so every cash flow, every balance, every charge and every rate, the
decrement rates included; every flag is `False`; the four factors that multiply a base or a
rate, `gmdb_wd_factor`, `gmdb_factor_acc`, `lapse_dyn_mult` and `lapse_wd_factor`, are 1.0,
no change; `bonus_end` is the int 0; and the phase is `PRE_ISSUE` before issue and
`EXPIRED` from the end of cover. The clocks and `inflation_factor` keep their values. No
count evaluates a decrement rate there, and no table is read at a policy month, a contract
year or an attained age the contract does not have: the surrender charge rate, the
scheduled premium and withdrawal, the GAWA%, mortality, the rider charge rates and the
roll-up rate are 0.0 outside cover before any table or rate is read, and the keyed readers
and the scenario readers are not reached there. `VA_US_S` leaves the moneyness multiplier
and the withdrawal-year factor unguarded: outside its frame the first reads the multiplier
of an empty account's moneyness, and the second scans a year that is not there.

The phase is `VA_US_S`'s: `ACCUM`, then `DEPLETED` once the account value has run out
with the GLWB alive, and `EXPIRED` from the end of cover, with `PRE_ISSUE` before issue
added. It is a leaf: no cell, report, check or runner reads it, the projection's state
being `depleted_flag`. `VA_US_S` returns the text; here each phase is an int code named as
the text, `PRE_ISSUE` 0 to `EXPIRED` 3 (*The compiled model*, below).

## The opening state

`VA_US_S` projects its new-business points from issue, on the premium and the issue rules
the notes state, and enters its point 2 at the notes' carried state, opening every
recursion at its `t = 0`. A contract valued in any month of its life needs all twenty state
columns, each what `VA_US_S` carries into that month. Each shows on a committed row:

- **`sa_pp_init_1`** and **`sa_pp_init_2`** open the subaccounts. Point 11, the anchor
  valued at policy month 120, carries 71,849.14 and 36,585.76, 66.3% and 33.7% of its
  account value of 108,434.90: since the worked example's month the first subaccount has
  grown at a gross 0.50% a month and the second at 0.20%. `VA_US_S` enters a contract in
  force with its account value split by the allocation, which here would give 65,060.94 and
  43,373.96. With that split the account value at `t = 11`, the anniversary closing contract
  year 11, is 97,688.70 rather than 97,893.67, and 86,816.22 rather than 87,207.58 a year
  later.
- **`gwb_pp_init`** opens the Guaranteed Withdrawal Balance, of which the first withdrawal
  locks the GAWA. Point 11 carries 166,500.00, ten years of bonuses and a step-up on its
  premium, and takes its first withdrawal at `t = 0`, at attained age 70: 5.75% of the
  GWB, 9,573.75. Carried at its value at anniversary 2, 112,500.00, the withdrawal would
  be 6,468.75, and the GLWB fee at the quarter's end 331.35 rather than 490.39.
- **`bb_pp_init`** is the base the bonus is credited on. Point 20, `VA_US_S`'s point 2
  valued at policy month 40, carries 112,500.00, which the step-up at anniversary 2 set,
  and its bonus at `t = 7`, the anniversary closing contract year 4, is 6% of it,
  6,750.00, taking the GWB to 126,000.00. Carried at the premium, 100,000.00, the bonus
  would be 6,000.00 and the GWB 125,250.00.
- **`gawa_pp_init`** is the GAWA in force, which a contract whose account value has run
  out is paid. Point 13, the declining point valued at the start of contract year 13, is
  paid its 9,200.00 at `t = 0` and at every contract year's start for life: 4,849.76 on
  its 0.527147 contracts at `t = 0`. Carried at 8,000.00, it would be paid 8,000.00 a
  year.
- **`gawa_pct_init`** is the percentage locked at the first withdrawal, at which a later
  premium raises the GAWA. Point 15, the excess programme valued five months after its
  withdrawal at policy month 60, locked 5.55% at attained age 65, and its premium of
  25,000 at `t = 7` raises the GAWA by 5.55% of it, from 6,463.10 to 7,850.60. Carried at
  5.75%, the GAWA would rise to 7,900.60.
- **`rb_pp_init`** opens the GMDB Benefit Base, which is charged quarterly and rolls up at
  each anniversary. Point 2 carries the notes' 112,360.00, on which its GMDB fee at
  `t = 0` is 252.81, and which rolls up 6% at `t = 9` to 119,101.60. Carried at
  100,000.00, the fee would be 225.00 and the roll-up 106,000.00.
- **`np_pp_init`** opens the cumulative Net Premiums, which no withdrawal reduces, a floor
  under the death benefit on the `rollup` and `ratchet` elections [S1]. Point 16, the
  highest-quarterly point on the annual-ratchet GMDB valued at policy month 40, carries
  100,000.00; its withdrawals, from `t = 80`, reduce the ratchet's base in proportion, and
  from `t = 92` the death benefit is the Net Premiums, 100,000.00, against a Benefit Base
  of 92,993.27 and an account value of 91,310.70.
- **`rp_pp_init`** opens the Remaining Premium, on which the withdrawal charge is taken
  [S2]. Point 2 carries 100,000.00: a surrender at `t = 0`, in its third contract year,
  pays the 6.5% charge on the Remaining Premium beyond the free amount, the larger of the
  earnings and 10% of the Remaining Premium, here 10,000.00: 6,490.85. Carried at
  90,000.00, the free amount would be the earnings, 19,859.19, and the charge 5,850.00.
- **`adj_pp_init`** carries the GWB Adjustment, which raises the GWB at the Adjustment
  Date, the later of the anniversary on or after attained age 70 and the 12th, where no
  withdrawal has ever been taken [S1] [S3]. Point 22, the never-withdrawing point valued at
  policy month 100, carries 105,000.00, and its Adjustment Date is `t = 43`, the 12th
  anniversary. There the GWB, 183,211.94 after the year's bonus, is already above it, as
  the bonus of each year without a withdrawal makes it on every shipped point, and the
  Adjustment ends without effect; carried at 205,000.00, it would raise the GWB to
  205,000.00 there.
- **`bonus_end_init`** is the contract year the Bonus Period ends, which a step-up
  restarts [S1]. Point 20 carries 12, the step-up at anniversary 2 having restarted the
  ten-year period, and is credited its bonus at each anniversary without a withdrawal:
  6,750.00 at `t = 19`, the anniversary closing contract year 5. Carried at 4, the bonus
  would stop after contract year 4, and the GWB at `t = 19` would be 126,000.00 rather
  than 132,750.00.
- **`has_wd_init`** opens the withdrawal status. Point 18, the never-withdrawing Roll-up
  point valued at policy month 560, its account value exhausted by the rider fees alone,
  carries `False` with a GAWA% of 6.2%, locked at depletion, where `VA_US_S`'s inference
  would read a withdrawal. The status is read by the first-withdrawal test, the GAWA's
  increase on a later premium, the GWB Adjustment and the CMT-linked roll-up's spread.
  Point 17, the CMT-linked point valued at policy month 41 before any withdrawal, rolls
  its Benefit Base up at `t = 6` by 4.50%, the 3.00% CMT rate plus the 1.50% spread before
  the first withdrawal, from 115,754.65 to 120,963.61. Carried as having withdrawn, its
  Adjustment voided and a GAWA% and a GAWA locked, as `Data` then requires, it would roll
  up at 4.00%, the floor, to 120,384.84. And the status says whether a withdrawal is the
  first, which locks the GAWA% of the age it is taken at: point 11, the anchor at its first
  withdrawal, on a grid that gives 0% from 60 to 64, where a contract may have withdrawn
  with no GAWA% locked, withdraws 5% of its GWB at `t = 0`, the grid's percentage at
  attained age 70, carried as not having withdrawn, and nothing, its GAWA being 0, carried
  as having withdrawn.
- **`sum_wd_pp_ytd_init`**, **`free_wd_used_cum_pp_ytd_init`**,
  **`gmdb_dfd_acc_pp_ytd_init`** and **`gmdb_factor_acc_ytd_init`** carry the contract year
  to date where the year under way opened before the valuation date. Point 15, five months
  after its withdrawal of 20,000 at policy month 60, carries 20,000.00 withdrawn this year,
  10,262.37 of free allowance used, a dollar-for-dollar reduction of 8,029.35, the whole of
  the year's allowance, and a proportional factor of 0.882908 for the excess above it. The
  GMDB's adjustment falls at the year's end, `t = 6`: the Benefit Base, 133,822.56, is
  reduced to `(133,822.56 − 8,029.35) × 0.882908` and rolled up 6%, to 117,727.68. With
  the year to date empty, as `VA_US_S` would restart it at `t = 0`, it would roll up whole,
  to 141,851.91. The free allowance used is netted off a surrender's free amount: a
  surrender at `t = 0` finds none left and pays a charge of 3,604.30, which with the
  allowance used carried at 0 would be 3,243.25. And the withdrawals to date are what the
  excess test adds a later withdrawal to: on point 21, the withdrawing return of premium
  valued five months after its year's withdrawal of 9,744.58, the year's whole limit, a
  further 500.00 the next month, added for a test, is excess, where with the year to date
  carried at 0 it would be inside the limit.
- **`wd_this_year_init`** answers for the months of the year under way before `t = 0`. On
  point 15 it is `True`, the excess withdrawal having fallen at policy month 60, so the
  year's surrender rate takes the withdrawal-year factor, 1.24% a year at `t = 0` rather
  than 2.07%, and the year earns no bonus at its anniversary, `t = 6`. Carried `False`,
  with an empty year to date, as `Data` then requires, the year would be read as one
  without a withdrawal, and its bonus of 6,599.35 would take the GWB to 116,588.55 rather
  than leave it at 109,989.20.
- **`rb_pp_prev_anniv_init`** is the Benefit Base at the anniversary that opened the year
  under way, the base of the year's dollar-for-dollar allowance, `rho × RB` [S1]: on point
  15, 6% of 133,822.56, 8,029.35, which the withdrawal at policy month 60 used whole, as
  the year to date records. In the first contract year it is the issue value: point 10,
  valued at policy month 6, carries the premium, 100,000.00.
- **`stepup_base_pp_ytd_init`** carries the highest-quarterly basis's history of the year
  under way. Point 16 carries 110,132.46, its account value at policy month 38, the year's
  first quarter end, and its step-up base at `t = 7`, the anniversary closing contract
  year 4, is the largest of that and the account values at the quarter ends on the books,
  `t = 1`, 4 and 7: 110,299.01, at `t = 7` itself. The GWB after the year's bonus,
  126,020.93, is above it, and no step-up fires; carried at 130,000.00, the step-up would
  take the GWB to 130,000.00.
- **`phi_glwb_init`** is the rate of the last contract quarter to end before the valuation
  month, on the VIX-linked fee: the prior from which the clip moves each quarter's rate by
  at most 0.40% [S4]. Point 17, valued in the last month of contract quarter 14, carries
  1.6626%, quarter 13's rate, and quarter 14's own, from the quarter's VIX-squared average
  of 602.30, is 1.6626% too, inside the band: its GLWB fee at `t = 0` is 490.46. Carried at
  1.00%, the clip would hold quarter 14 to 1.40% and the fee to 413.00.

The issue values `VA_US_S` computes from the premium stay rules, and move into the issue
month: the premium buys units at the allocation and raises the GWB, the Bonus Base, the Net
Premiums, the Remaining Premium and the Benefit Base, 105% of it the GWB Adjustment, and the
Bonus Period's end opens at `bonus_period_years`, each in the month with
`duration_mth(t) = 0`. The cells that bear the notes' names for the opening values,
`av_pp_init()`, `gwb_pp_init()` and the rest, read the opening state instead, 0 on new
business, as `pols_if_init()` does for the count.

Every recursion opens at `t_entry()` and reads its previous month first: the column there,
`X_init()`, and `X(t − 1)` after it. The year to date opens three ways: empty at a contract
year's start, the month before after `t_entry()`, and the `_ytd_init` column at
`t_entry()` where the year opened before it. The Benefit Base opening the year is read three
ways too: from the frame, `rb_pp(year_open_mth(t))`, where that anniversary is at or after
`t_entry()`; from `rb_pp_prev_anniv_init`, where the year opened before the valuation date
on a contract in force; and by `VA_US_S`'s issue rule, the base after the issue month's
premium, `rb_pp_at(t_entry(), BEF_WD)`, in the first year of a contract issued at or
after the valuation date. `VA_US_S` takes that last value wherever the anniversary precedes
its frame, which is wrong on a contract in force once a premium has been credited after the
anniversary and before the valuation month. The year's withdrawal flag answers from
`wd_this_year_init` where the year opened before `t_entry()`, and scans the year's months on
the books for the rest. The step-up base takes the quarter ends at or after `t_entry()`
from the frame, and the column at the anniversary closing the year under way at the
valuation date. And the VIX-linked rate's clip takes `phi_glwb_init` as its prior in the
quarter under way at `t_entry()`, so no quarter before it is read.

The depleted status takes no column. `depleted_flag` is absorbing, and from the month after
it is set every subaccount is held at 0, so at each month end the flag is set exactly where
the account value is at or below `av_depletion_threshold`, half a cent **[std]**. So a
contract in force enters month 0 depleted exactly where its opening account value, the sum
of its subaccount values, is at or below the threshold, and new business never does, the
rounding of either sign about 0 that a depletion can close on among them (above): the test
is the threshold's, never 0's, and the rules of `proj_len()` that turn on depletion read the
same test, the first of them holding the account of a contract that opens depleted to 0
within 1e-8. `depleted_open(t)` is that test at `t_entry()` and `depleted_flag(t − 1)` after
it, and every cell that `VA_US_S` writes with `depleted_flag(t − 1)` reads it, `VA_US_S`
reading below `t = 0` in its first month. Points 13 and 18 open depleted. Point 13, valued
at a contract year's start, is paid at `t = 0`, from the GAWA and the GWB its row carries,
where `VA_US_S` reads the month before its frame; point 18, valued mid-year, is first paid
at `t = 4`, the start of contract year 48: 11,160.00, 6.2% of its GWB of 180,000.00.

The withdrawal status is a column, not derived. `VA_US_S` infers it from a GAWA% above 0,
which holds until a contract's account value runs out before its first withdrawal: the
GAWA% locks at depletion too, at the attained age then, while `VA_US_S`'s own frame keeps
`has_wd_by` `False`. Once the account is exhausted no cash flow reads the status, but the
GWB Adjustment, which `result_bases()` reports, does, until its date: a withdrawal voids it,
and a depletion does not. So `has_wd_init` carries `VA_US_S`'s own `has_wd_by` entering the
month, and `Data` ties it to the Adjustment, the year's withdrawal flag and the GAWA%.

## Departures from VA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
issue event keyed on `t == 0` falls in the issue month, and every recursion begins at
`t_entry()`. Where `VA_US_S`'s test would have stayed correct on the valuation clock, it
moved anyway, so that cover has one definition. Running in force left, of `VA_US_S`'s 200
cells, 74 unchanged, 15 with a new docstring only and 111 rewritten; it removed none, and
added 31, 231 in all. Compiling then changed how each cell reads its inputs and spells its
codes, and no number: it removed no cell and added ten, `point_id`, now a cell where it was
the Space's parameter, `subaccount_count` and `subaccount_id(j)`, which walk a point's fund
set by position, and the seven join numbers `fund_set_number`, `return_scenario_number`,
`rate_scenario_number`, `txn_number`, `gawa_grid_number`, `cdsc_number` and
`mort_schedule`, 241 in all (*The compiled model*, below); of `VA_US_S`'s cells it changed
the signature of two, `claims` and `claims_over_av`, whose total is the code `ALL`, and the
parameter's name of one, `lapse_itm_mult(ratio)`, `VA_US_S`'s `lapse_itm_mult(m)`. The twin
identity compares `VA_US_S`'s `(t, None)` with `(t, ALL)`, reads every timing, kind, rate
column and phase at its code, and compares every cell by position, so it exempts no cell
for the compile step.

| Cells | `VA_US_S` | `VA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth_init`, `proj_len`, `maturity_mth`, `t_entry`, `is_active` | `duration_mth_init()` the column of the name, 0 or a month in force; `proj_len() = 12 × policy_term() − duration_mth_init()` | `duration_mth_init()` from `duration_mth`, negative for a contract issued later; `proj_len() = maturity_mth() − duration_mth_init()`, refusing a point at or past the end of cover or with no cover from issue, and on a contract in force an opening state that the depletion threshold, `phi_glwb_curr` or the VIX corridor forbids; `maturity_mth`, `t_entry` and `is_active` new | Every frame starts at the valuation date and knows where the contract's cover starts and ends, and a rule of the opening state that needs a `Projection` Reference runs where its frame is defined |
| `anniv_mth`, `year_open_mth` | — : the year's edges are policy months, `12(y − 1) − 1` and `12(y − 1)`, each converted by `t_of_month` where it is read | new: `t + 11 − duration_mth(t) % 12` and `t − 1 − duration_mth(t) % 12` | The edges of a contract year as months of the frame |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_new_biz`, `policy_count` | `pols_if(t) = pols_if_at(t − 1, "AFT_DECR")`, from `pols_if_init()`, the column's 1, at `t = 0`: two cells a month | `pols_if_at(t, BEF_DECR)`, from `t_entry()`, one cell a month, with `BEF_NB` added; `pols_if_init()` 0 unless in force; `pols_new_biz` and `policy_count` new | Contracts in force at the valuation date open the count; new business joins it in its issue month |
| `sa_pp`, `sa_pp_at`, `av_pp`, `av_pp_at`, `adj_pp` | `sa_pp(t, i)` is `sa_pp_at(t, i, "EOM")`, which reads `sa_pp(t − 1, i)`: two cells a month, from `alloc(i) × av_pp_init()` at `t = 0`; `adj_pp` reads `adj_pp_bef_anniv`, which reads `adj_pp(t − 1)`; the sums over subaccounts generators | each month's steps inline, one cell a month, from `sa_pp_init(i)` and `adj_pp_init()` at `t_entry()`; explicit loops over the set's subaccounts, by position, `subaccount_id(j)` | One cell a month, and the subaccounts as they stand. The values are `VA_US_S`'s bit for bit |
| `av_pp_init`, `sa_pp_init` and the seven bases' `_init` cells | `av_pp_init()` the column `av_init`, which `sa_pp_at` splits by `alloc(i)` at `t = 0`; the bases' columns | `av_pp_init()` the sum of the new `sa_pp_init(i)`, each read from the point's `sa_pp_init_<i>` column; the renamed columns | The account value as its subaccounts hold it |
| `has_wd_init` | `gawa_pct_init() > 0` | the column | The inference fails after a depletion without a withdrawal |
| `sum_wd_pp`, `free_wd_avail`, `free_wd_used_cum_pp`, `gmdb_wd_dfd_pp`, `gmdb_dfd_acc_pp`, `gmdb_factor_acc` | restart at `t == 0` as at a contract year's start | three ways: empty at a year's start, the month before after `t_entry()`, the new `_ytd_init` accessors at `t_entry()` | A contract valued mid-year carries its year to date |
| `is_wd_year` | `any` over the year's months from `t = 0` | the new `wd_this_year_init()` for the year's months before `t = 0`, and an explicit loop over its months on the books | The year's withdrawal before the valuation date is history |
| `rb_prior_anniv_pp` | `rb_pp` at the anniversary, or `rb_pp_at(0, "BEF_WD")` where the anniversary precedes the frame | three ways: from the frame at `year_open_mth(t)`, from the new `rb_pp_prev_anniv_init()` in force, by the issue rule on new business | A premium after the anniversary is not part of the year's allowance base |
| `stepup_base_pp` | the largest account value at `t − 3j` for `j = 0 … 3`, `t − 3j ≥ 0`, by a generator | the quarter ends at or after `t_entry()`, by an explicit loop, and the new `stepup_base_pp_ytd_init()` at the anniversary closing the year under way at the valuation date | The year's quarter ends before the valuation month are history |
| `phi_glwb_vix` | recurses from the first contract quarter | the new `phi_glwb_init()` as the clip's prior in the quarter under way at `t_entry()`, the quarter `max(duration_mth_init(), 0) // 3 + 1`, a key the model point fixes, not a clock read | The quarters before the books are history |
| `depleted_open`, `depleted_flag`, `glwb_payment_pp` and every cell that read `depleted_flag(t − 1)` | `depleted_flag(t − 1)`, below `t = 0` in the first month; `glwb_payment_pp` reads `gawa_pp(t − 1)` and `gwb_pp(t − 1)` | the new `depleted_open(t)`, derived from the opening account value at `t_entry()`; `glwb_payment_pp` reads `gawa_pp_init()` and `gwb_pp_init()` there | No month before the books is read, and a contract depleted at a year's start is paid at `t = 0` |
| `premium_pp`, `expenses` | the single premium and acquisition at `t == 0` | in the month with `duration_mth(t) = 0` | A point in force paid its premium before the valuation date, and one issued later pays it in its issue month |
| `pols_maturity` | the last month as `t = proj_len() − 1` | `duration_mth(t) = maturity_mth() − 1` | One definition of cover, on the policy clock |
| `inv_return_mth`, `scenario_rate` | `VA_US_S`'s readers' tables at `max(duration_mth(t), 0)`, by a list comprehension | the checked companions at `t`, as `Data` holds them, step-filled from each row to the next, raising where no level is set | The scenarios run on the valuation clock |
| `inflation_factor` | `1.025^(valuation_year − 2015 + duration(t))`, from issue | `1.025^(valuation_year − 2015 + t // 12)` | Unit costs in valuation-date dollars |
| `check_av_roll_fwd`, `check_pols_roll_fwd`, `check_charge_split`, their residuals, `av_at` | `all(abs(r) < tol)` over a generator, the tolerance fixed; `pols_if(t + 1)`, guarded below `t = 0` only | loops over `t = 0 … proj_len() − 1` that fail at the first residual not inside the bound, two of the tolerances scaled by `max(policy_count(), 1)`; `pols_if_at(t + 1, BEF_NB)`; 0.0 outside cover, before `t + 1` is read | A residual is rounding on that many contracts, next month's new business is no part of month `t`'s movement, and no month past the frame is read |
| `stepup_base_pp`, `rb_pp`, `rb_pp_at`, `gmdb_wd_dfd_pp`, `gmdb_wd_excess_pp`, `gmdb_guarantee_pp`, `phi_gmdb`, `phi_glwb`, `rollup_rate` | branch on the text of `stepup_basis()`, `gmdb_option()`, `fee_reset_rule()` and `rollup_rule()` | branch on the ten new `is_*` cells, one bool for each value `VA_US_S` tests, decoded once a point, in `VA_US_S`'s order; a value `VA_US_S` does not know raises `VA_US_S`'s message | No projection cell compares a model point column's text or calls a label accessor, which are left to reporting; compiling moved the decodes into `Data` |
| `sub_ids`, `alloc`, `fund_expense_rate`, `gawa_pct_at_age`, `surr_charge_rate`, `prem_scheduled_pp`, `wd_scheduled_pp`, `mort_rate` | read `VA_US_S`'s readers' tables per call, the GAWA% band by a list comprehension, the schedule's last year by `int()` of the raw keys and the mortality table's last age by a generator | read `Data`'s checked tables, through the new keyed readers `surr_charge_rate_at(k)`, `prem_scheduled_pm(m)`, `wd_scheduled_pm(m)` and `mort_rate_base_at(x)`, and `gawa_pct_at_age(a)`, each from `Data`'s arrays | A key the table cannot be read by is refused by name before a value is read, and each table is read through cells of its own, one a table but the fund table's three and the programme's two |
| every guarded cell | `t < 0` and `t ≥ proj_len()`, or `t >= 0`; `lapse_dyn_mult`, `lapse_wd_factor`, the bases' chains, mortality and the surrender charge rate unguarded | outside cover 0.0, `False`, 1.0 for the four factors, the int 0 for `bonus_end`, `PRE_ISSUE` or `EXPIRED` for the phase, before any table or rate is read | No month outside cover is the contract's (above) |
| `lapse_wd_factor` | `is_wd_year(t)`, a scan of the year up to 11 months on | `is_wd_year(anniv_mth(t))` | The one read ahead of the month, at the anniversary closing the year (above) |
| `phase` | `EXPIRED` from `proj_len()` | `PRE_ISSUE` before issue too | Nothing is active before issue |
| `result_pols` | five columns | `pols_new_biz` second | The count issued in the issue month |

The 31 new cells all appear above: the clock's five, `maturity_mth`, `t_entry`,
`is_active`, `anniv_mth` and `year_open_mth`; the count's two; the nine opening-state
accessors; `depleted_open`; the ten `is_*` decodes, two of `glwb_stepup_basis`, three of
`gmdb_option`, three of `fee_reset_rule` and two of `rollup_rule`; and the four keyed
readers. The docstring-only changes rewrite the time-axis prose, say which cells are labels
for reporting, called by no projection cell, and that a contract's single premium falls in
its issue month. Three References are new, `check_tol_av`, `check_tol_pols` and
`check_tol_charge`, `VA_US_S`'s three tolerances. In `Data`, `model_point_table` reads
`model_point_table_sec.csv` and checks it, `return_scenario_file` and `rate_scenario_file`
name the two companions, `future_horizon_mth` is new, the two scenario readers'
docstrings name the clock their `t` is on, and running in force added eleven cells: the
seven checked tables, `fund_values_init`, `mort_last_age`, and `gawa_pct_zero_band` with
`gawa_pct_zero_by_point`, which read the GAWA% grid at the ages a contract in force
reached before the valuation month, for the rules of the locked GAWA%. Compiling replaced
`fund_values_init`, a DataFrame, with `sa_pp_init_array`, and wrote `gawa_pct_zero_band`'s
loop out in the two cells that called it, so that `gawa_pct_zero_by_point` is a 0/1 vector
by position, and added the vectors, arrays and counts `Data`'s docstring lists, 90 cells in
all (*The compiled model*, below). `VA_US_S`'s seven readers of the assumption tables are
unchanged in code.

Seven joins on text keys are `VA_US_S`'s, each read by the cells that read its table: the
fund set on the model point's `fund_set`, in `sub_ids`, `alloc` and `fund_expense_rate`;
the two scenarios on its `scenario_id`, in `inv_return_mth` and `scenario_rate`; the
programme on its `txn_id`, in `prem_scheduled_pm` and `wd_scheduled_pm`; the GAWA% grid on
its `glwb_option`, in `gawa_pct_at_age`; the withdrawal charge scale on its
`cdsc_schedule`, in `surr_charge_rate_at`; and mortality on its `sex`, in
`mort_rate_base_at`. Running in force kept them on the text, as `VA_US_S` joins; compiling
moved each join into `Data`, which numbers the keys once, and the cell reads its table at
the point's number; it moved the ten decodes there too, and turned the timing, kind, rate
column and phase strings into int codes (*The compiled model*, below), so that no
projection cell compares or returns text. `Data` checks each key before a projection reads
by it.

The mortality rate is the table's, read at the attained age and sex, with no factor
applied, as in `VA_US_S`, so no rate past 1 can arise and none is capped, and there is no
cap to depart from; `Data` refuses a rate outside 0 to 1, blank or text. The shipped table
reaches 1.0 at age 120, past every frame: cover ends with attained age 119. The surrender
rate's bound of 1 is `VA_US_S`'s `min(1.0, ...)`, kept in its order.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
and `net_cf_ga` with it. A point in force carries that expense in valuation-date dollars,
so point 2's `expenses(t)` is `VA_US_S`'s with the per-contract term divided by `1.025^2`
in the first ten months of each projection year and by `1.025^3` in the last two. Its
other cash flows, its counts and every value per contract are `VA_US_S`'s from the
valuation date on. Point 23 is `VA_US_S`'s point 1 fifteen months on in those columns too.
Its maintenance expense is inflated from the valuation date rather than from its issue,
the per-contract term `1.025` times `VA_US_S`'s in the first nine months of each contract
year and `1.025^2` times it in the last three, and its acquisition, uninflated in both, is
`VA_US_S`'s. Acquisition, 0 as shipped, would also move on point 2, which `VA_US_S`
charges at its `t = 0`.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, and the compile tests hold it
so on x86-64 on the splice grid and at the contract's extremes too, which take the
branches the committed points do not. `VA_US_SEC` compiles on the chassis `MYGA_US_SEC`
compiled first, as `FIA_US_SEC` does, and takes from it what `MYGA_US_SEC`'s *What the
deferred annuities inherit* sets out, in `FIA_US_SEC`'s forms where `FIA_US_SEC` departs
from it; where this model departs from either, this section says so.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py variable_annuity                  # in place
python tools/build_sec_cy.py variable_annuity --out /tmp/va    # elsewhere
```

The tool exports the model to `VA_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `VA_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/variable_annuity")    # the directory holding the build
from VA_US_SEC_nomx_cy import mx_model as model
model.Projection[1].result_cf()                     # point 2, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 1` after `Projection.result_cf()` leaves point
1's frame cached, `proj_len()` 720, while `point_id()`, not yet computed, reads point 2's
label, and `Projection.expense_maint` set to 60 once `Projection[1]` has computed point
2's `expenses(0)` leaves it at 17.34, where modelx, and an ItemSpace made after, compute
12.97. Set every Reference on a model just imported, before anything is computed, where
modelx would recompute; a test holds the compiled model to this.

A build takes about four and a half minutes with gcc, 278 s here under load, and needs a
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
205 of its 231 `Projection` cells as C numbers. Twenty-six returned a Python object: a
row, text, the phase among it, a list or a DataFrame, and five cells the sample had called
where they raise. Fourteen took a timing, a kind or a rate column as text, and three a
float, and those seventeen, the phase and the five kept a dictionary for a cache, 23 in
all. It ran 1.1 times as fast as its own export, 127 ms a point on `net_cf` against 143,
over the committed points. The bodies of the typed cells still called pandas and Python: a
`model_point()` lookup for each attribute a formula reads, the text of a column compared in
each of the ten decodes, a `.loc` on a table for each subaccount's allocation, fund expense
and opening value, each attained age's mortality and GAWA%, each completed year's withdrawal
charge and each policy month's scheduled premium and withdrawal, a search of the scenario
for each month's return, VIX average and CMT rate, a list of the fund set's subaccount ids
for each sum over them, `math.floor` for the CMT-linked roll-up, and a total over the kinds
for `kind=None`. So each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[1]` is point 2, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The vectors are the checked columns
  `Data.model_point_table()` returns, read as `VA_US_S` reads them, by `float()` and
  `int()`, the two flags of the opening state by value, as stage `E`'s check reads them:
  as at `FIA_US_SEC`, and unlike `MYGA_US_SEC`, the model reads no separate copy of the
  numeric columns, since the table's checks, from stage `E`, already refuse every numeric
  column a formula reads where it is blank, text or out of its range, naming the column and
  the points. The subaccount values are one table by point and subaccount id,
  `Data.sa_pp_init_array()`, 0.0 where the point's set lacks the id, as stage `E` read a
  blank column.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each of the four switch
  columns a formula branches on into 0/1 flags, for every point at once, the ten `is_*`
  vectors: `glwb_stepup_basis` into two, `gmdb_option` into three, `fee_reset_rule` into
  three and `rollup_rule` into two. Each compares the text exactly, as `VA_US_S` compares
  it, so a value written in another case or with a space, `Annual_CV` or ` annual_CV`, is
  no flag, and the cell that branches on it raises `VA_US_S`'s message, `invalid
  stepup_basis`, in both engines.
- **Tables indexed by integers.** Each assumption table is an array, or a set of arrays, a
  cell reads by element. The fund sets, the two scenarios, the programmes, the GAWA% grids,
  the withdrawal charge schedules and the mortality table's sexes are numbered from 1, each
  point carrying its own, `fund_set_number()`, `return_scenario_number()`,
  `rate_scenario_number()`, `txn_number()`, `gawa_grid_number()`, `cdsc_number()` and
  `mort_schedule()`: each in the sorted order of its keys, the order its checked table holds
  them in, but the fund sets, numbered in the order `Data.fund_sets()` holds them, the
  file's, which it keeps unsorted, so that a table mixing text and numeric set keys reads
  as at stage `E`. The fund sets are held by set and subaccount id, their allocations and
  fund expenses, with each set's ids in the file's order, its count and its last id beside
  them; the returns by scenario, subaccount id and valuation month, step-filled from each
  subaccount's first row, with that first month beside them; the VIX averages and the CMT
  rates by scenario and valuation month, step-filled likewise; the programmes by programme
  and elapsed policy month, 0.0 where a programme has no row, which is no premium and no
  withdrawal, as in `VA_US_S`; the GAWA% by grid and attained age, each age the band it
  falls in, 0.0 below the grid's first band, `VA_US_S`'s 0%; the withdrawal charges by
  schedule and completed years, with each schedule's last year beside them, a year past it
  reading the last year's rate, as `VA_US_S`'s lookup caps it; and the mortality by sex and
  attained age, with each sex's first and last age beside it. Each is read through the
  cells running in force had already added, `alloc(i)`, `fund_expense_rate(i)`,
  `sa_pp_init(i)`, `inv_return_mth(t, i)`, `scenario_rate(t, name)`,
  `prem_scheduled_pm(m)`, `wd_scheduled_pm(m)`, `gawa_pct_at_age(a)`,
  `surr_charge_rate_at(k)` and `mort_rate_base_at(x)`, and the padding, NaN, is read by none
  of them.
- **The subaccount, by its id.** A subaccount is the argument of every subaccount cell by
  its id, `sa_pp(t, i)` with `i` 1 or 2 as shipped, as `VA_US_S` names it, from 1 to
  `subaccount_id_max`, 9, slot 0 of each cache unused. `VUL_US_SEC` makes its subaccounts
  positions, since its lineup is one table every point shares; here a point's fund set picks
  its own ids, keyed alike by the returns and the opening columns, so a position would name
  another subaccount on another fund set, and the twin identity could not map `VA_US_S`'s
  ids onto them. A sum over the subaccounts, `VA_US_S`'s sum over `sub_ids()`, loops over
  the positions of the point's set, `0 … subaccount_count() − 1`, taking each id from
  `subaccount_id(j)`, in the file's order, so each total is the same sum in the same order,
  bit for bit. `sub_ids()`, `VA_US_S`'s list, stays as an engine cell (below).
- **Arrays held to the last read.** Every array ends at the last month, age or subaccount
  id a read reaches, whatever the table's keys, as `FIA_US_SEC`'s do: the scenarios and the
  programmes run to `Data.read_last_mth`, 1,141, the last `t` of the cache,
  `12 × (omega_age − issue_age_min) + future_horizon_mth + 1`, and the withdrawal charges to
  the completed years a month to it can count, 95; the mortality and the GAWA% grids to
  `Data.read_last_age`, 120, the last `a` of the cache, `omega_age`; and the fund sets, the
  returns and the opening values to `Data.read_last_sub_id`, 9, the last `i` of the cache,
  `subaccount_id_max`. `spec_sec.py` derives the three References, and a test holds each to
  the spec. A scenario's last row holds to the end, as `VA_US_S`'s step function holds it,
  and a grid's last band, so a key far past any read, a return or a premium at month 1e10,
  which `VA_US_S` holds and never reaches, neither makes an array gigabytes wide nor refuses
  a point `VA_US_S` projects, and each reader refuses a read past its array's bound, naming
  the point, where no projection reads one. A fund set holding an id past
  `read_last_sub_id` keeps its other ids in the arrays, and its true count and last id, by
  which `proj_len()` refuses its points (*What it refuses*, below). The return arrays are
  1,142 months by ten ids a scenario, about 91 KB each, 1.6 MB for the eighteen rows the
  committed scenarios and the padding take, read once a block.
- **Ages from the table's first.** The mortality array starts at the table's first age, or
  at 0 where that is lower, as `FIA_US_SEC`'s does, so no age a table holds is refused, a
  negative one among them, and none far below the others widens an array.
  `mort_rate_base_at` caps the age at the table's last, `Data.mort_last_age()`, as
  `VA_US_S` does, the bound second, `min(x, top)`: a table that stops below cover reads its
  last rate on, as in `VA_US_S`, where `MYGA_US_SEC` and `FIA_US_SEC` refuse a point their
  mortality stops short for. The GAWA% array starts at age 0, since an age below a grid's
  first band is 0%, a value, not padding.
- **Codes.** A timing, a kind, a rate scenario's column or a phase, which `VA_US_S` spells
  as text, is an int Reference named as the text: the count's timings `BEF_NB = 0`,
  `BEF_DECR = 1`, `BEF_LAPSE = 2` and `AFT_DECR = 3`; the account value's `BEF_PREM = 4`,
  `BEF_WD = 5`, `BEF_INV = 6`, `BEF_FEE = 7` and `EOM = 8`; the bases' own
  `BEF_ANNIV = 9`; the kinds `DEATH = 0`, `LAPSE = 1` and `MATURITY = 2`, in `result_cf`'s
  order, and `ALL = 3`; the columns `VIX_SQ = 0` and `CMT10 = 1`, `VA_US_S`'s names
  upper-cased; and the phases `PRE_ISSUE = 0`, `ACCUM = 1`, `DEPLETED = 2` and
  `EXPIRED = 3`. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`,
  `av_pp_at(t, BEF_WD)`, `claims(t, DEATH)`. A string argument would give the cell a
  dictionary for a cache, where a code indexes a C array, so codes are numbered from 0
  without a gap. The three families of timing, passed to different cells, are numbered as
  one, `BEF_NB` and `BEF_DECR` first, as in every SEC model, then the count's others, the
  account value's and the bases' own, each family in the order of its instants. The bases
  share `BEF_PREM` and `BEF_WD` with the account value, where `VA_US_S` spells them alike,
  so each is one Reference. So a code of one family passed to another's cell,
  `av_pp_at(t, BEF_NB)`, is refused as `invalid timing` in both engines, rather than read as
  a timing of the cell's own. The `Projection` docstring's *Codes* lists all twenty.
- **The totals, by `ALL`.** `VA_US_S`'s `claims(t, kind=None)` and
  `claims_over_av(t, kind=None)` are one kind's amount or, with `None`, the three kinds
  added: `None` is no C parameter. Here the total is the code `ALL`, and `net_cf` calls
  `claims(t, ALL)`. `VA_US_S` writes the total as a chain of `+`, death, lapse, maturity,
  and the chain is kept, so the total is `VA_US_S`'s float bit for bit, the sign of a zero
  included. The twin identity compares `VA_US_S`'s `(t, None)` with `(t, ALL)`. `ALL`
  passed to a cell of one kind, `pols_decr`, `claim_pp`, `claim_from_av_pp` or
  `claims_from_av`, is refused as `invalid kind`, as `VA_US_S` refuses `None` there, and
  `claim_from_av_pp` tests its kind by a chain of `==` where `VA_US_S` tests membership of
  a tuple.
- **No float parameter on the projection's path.** A cell keyed by a float compiles with
  a Python dictionary for a cache. `VA_US_S`'s moneyness multiplier, `lapse_itm_mult`,
  and its VIX-linked fee formula and clip, `fee_rate_vix_raw` and `fee_rate_vix_clip`,
  which the projection calls on a moneyness ratio, a VIX average and a rate, are written
  inline in their callers: the multiplier, at each of the two moneyness ratios, in
  `lapse_dyn_mult`, and the formula and the clip in `phi_glwb_vix`, each the same
  expression in the same order, the prior before the average, so the numbers are
  `VA_US_S`'s bit for bit.
- **Four cells kept as `VA_US_S` wrote them.** The three float engines, and `sub_ids()`,
  `VA_US_S`'s list of the set's ids, which no compiled cell may build, are `VA_US_S`'s
  cells, kept for a reader, for the module's own tests and for the twin identity, which
  compares them at the arguments `VA_US_S`'s sweep evaluates; `sub_ids` loops over
  `subaccount_id(j)`, as the sums do. `tests/us_registry.py` names the four, under
  `"engine"`, and the compile tests admit them, and no other cell, to a dictionary cache,
  a float parameter or a Python object; no compiled cell may call them. `lapse_itm_mult`
  takes `ratio`, where `VA_US_S`'s takes `m`: `spec_sec.py` sizes `m`, the policy month,
  and an engine cell takes a parameter no size names, so the engine's parameter was
  renamed, and no other cell or call moved.
- **The CMT-linked roll-up's rounding.** `VA_US_S` rounds the CMT rate to its step by
  `math.floor(raw / step + 0.5) * step`. Here the floor is the float floor division by
  1.0, `v // 1.0`, which is `math.floor(v)` as a float for every finite `v` in both
  engines, exactly, so no number moves and no module is read; `VA_US_S`'s three refusals,
  a step of 0, a `v` that is NaN and one that is infinite, are written out in its order,
  each with Python's message.
- **No Python call kept.** No formula outside the reporting and engine cells calls a Python
  builtin outside its refusals but `int`, `float`, `bool`, `abs`, `min`, `max` and
  `range`, which Cython turns into C, so `tests/us_registry.py` admits none. No such cell is
  uncached, and none takes a float.
- **Operands in `VA_US_S`'s order.** Compiled, a two-argument `max` or `min` evaluates
  its arguments right to left, so a point that reaches two refusals would raise the
  second's message. Each that takes two operands from cells, in `wd_pp`, `wd_free_pp`,
  `wd_exempt_pp`, `surr_chargeable_pp`, `gwb_pp_aft_stepup`, `gawa_pp_at`,
  `gmdb_wd_dfd_pp`, `gmdb_guarantee_pp` and `db_pp`, binds them to locals first, in
  `VA_US_S`'s order, and so do the two inlined engines. No number moves: only the order the
  caches fill.
- **Reporting cells stay Python.** `model_point()`, the thirteen label accessors
  `policy_id()`, `sex()`, `designated_lives()`, `tax_status()`, `fund_set()`,
  `glwb_option()`, `stepup_basis()`, `gmdb_option()`, `cdsc_schedule()`,
  `fee_reset_rule()`, `rollup_rule()`, `scenario_id()` and `txn_id()`, and the four reports
  return a table row, text and DataFrames, for a reader, for `run_sec.py` and for the
  comparison with `VA_US_S`. No other cell calls them, so they cost the projection
  nothing. A label accessor returns its column as read, and `Data` accepts a label that is
  not text: a blank or numeric `policy_id`, `designated_lives` or `tax_status`, which no
  cell reads; a blank switch, which its decodes answer False to; and a numeric `sex`,
  `fund_set`, `glwb_option`, `cdsc_schedule`, `scenario_id` or `txn_id` where its table's
  keys are numbers. So each accessor compiles to a Python object, as the sample traces it
  (below), and returns what modelx returns. The three checks are reporting cells too, but
  they return a verdict, which compiles to a C `bint`.

Of `Projection`'s cells, compiling took away none and added ten: `point_id`,
`subaccount_count`, `subaccount_id`, and the seven join numbers, 241 in all. The Reference
`idx`, 0, takes the place of `point_id`, and `issue_age_min`, 35, `issue_age_max`, 85,
`glwb_issue_age_max`, 80, `gmdb_issue_age_max`, 79, `subaccount_id_max`, 9, and the twenty
codes are new References. `Data` has 90 cells, 20 at stage `E`, and its docstring lists
its vectors, arrays and counts, each with the column or file it comes from: 32 vectors of
int64, by point, set, scenario, grid, schedule or sex, and 19 of float64, by point; ten
tables of float64 and three of int64, the opening subaccount values, the fund sets, the
rates, the GAWA% grids, the withdrawal charges, the programmes, the mortality and the
returns' first months; the returns, a table of three dimensions; and nine int counts and
extents, each read from a checked table. Its seven readers, its seven checked tables,
`model_point_table()` and `input_dir()` stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 219 of
its 241, the three checks among them, returns a C `bint`, `long long` or `double`, and
caches a single value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,142 by `t`, of `double`, `long long` or `bint` | the 132 cells of `t` alone: every count, rate, factor, charge, fee, withdrawal, value, base, claim and cash flow; the policy clock, its years, quarters and anniversaries and the attained ages; the year's edges, `anniv_mth` and `year_open_mth`; the statuses, `depleted_flag`, `has_wd_by` and the year's flags; the phase; `cmt10`; and the checks' monthly residuals |
| a C array of 1,142 by 10 | the 17 cells of `t` and one code or id: `pols_if_at`, `av_pp_at`, `av_at`, `gwb_pp_at`, `gawa_pp_at` and `rb_pp_at`, by `(t, timing)`; `pols_decr`, `claim_pp`, `claim_from_av_pp`, `claims`, `claims_from_av` and `claims_over_av`, by `(t, kind)`; `scenario_rate`, by `(t, name)`; and `inv_return_mth`, `unit_growth`, `sa_pp` and `sa_weight`, by `(t, i)` |
| a C array of 1,142 by 10 by 10 | `sa_pp_at`, by `(t, i, timing)` |
| a C array of 1,021 by `m` | `t_of_month`, `prem_scheduled_pm` and `wd_scheduled_pm`, by policy month |
| a C array of 342 by `k` | `surr_charge_rate_at`, by completed years, and `vix_sq` and `phi_glwb_vix`, by contract quarter |
| a C array of 121 by `a` or `x` | `gawa_pct_at_age` and `mort_rate_base_at`, by attained age |
| a C array of 10 by `i` or `j` | `alloc`, `fund_expense_rate` and `sa_pp_init`, by subaccount id, and `subaccount_id`, by position |
| one `long long`, `double` or `bint` | the 57 cells without a parameter: the point's label, numbers, decodes, join numbers, flags and subaccount count, its opening state, the ends of its frame, its roll-up percentage and Adjustment year, and the three checks |
| a Python object | the reporting cells but the checks, eighteen, and `sub_ids` |
| a Python dictionary, behind a C signature | the three float engine cells, their bodies Python |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary but the engine
cells'.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. And a call that raises types its cell, and
every cell beneath it on the stack, as a Python object too: mx2cy's tracer logs a call
unwound by an exception as returning `None`, which merges with the type the cell returns
elsewhere into `object`, with a dictionary for a cache. Compiled as it stood after running
in force, with a sample that called the scenario readers before a point's first month on
the books and the quarter readers off them, five cells compiled so for that alone. So
`sample_sec.py` calls each cell only where the point computes it, and no call it makes
raises: no code a cell refuses, no key past an array's hold, no scenario read before its
first month, no quarter before the point's first on the books. It calls every `Data` cell
of no parameter first, bare, so that each vector and extent is typed whatever the
projections reach, `gawa_pct_zero_by_point`, which only a depleted point that has not
withdrawn asks for, among them. Then, on every committed point, it runs the four reports
and the three checks, which reach most cells, and calls the rest: every `Projection` cell
of no parameter, `model_point()`, `point_id()` and the thirteen label accessors among
them, and `sub_ids()`; every monthly cell from `t = 0` to the month after the frame,
`t = proj_len()`, each guarded outside cover, but the scenario readers, which it calls from
`t_entry()`; each timed cell at every code of its family, `sa_pp_at` and the subaccount
cells at every id the point's set holds, and each kinded cell at its three kinds,
`claims` and `claims_over_av` at `ALL` too, which no report reads, nor `charge_income_pp`,
`gmdb_claims`, `net_cf_ga`, `wd_charges`, `sa_weight` and `phase`; the rate scenario at
both columns; `vix_sq` and `phi_glwb_vix` at every quarter from the point's first on the
books to its last; the keyed readers at every policy month, completed year and attained
age of cover; the subaccount readers at every id the set holds, and `subaccount_id` at
every position; and the engine cells at the arguments the module's own tests use, which a
test holds equal to the module's. It projects the committed points alone: the export it
runs reads the CSVs of the directory the build is made in, and the trace it needs is the
committed points', which are what the tests project. The thirteen label accessors it calls
once more, on a copy of the table's first point with its three free labels and its four
switches blank and its six keys, `sex`, `fund_set`, `glwb_option`, `cdsc_schedule`,
`scenario_id` and `txn_id`, the number 1, beside one-key copies of the mortality, fund,
GAWA%, withdrawal charge, return, rate and programme tables keyed by 1, which it writes to a
temporary directory and reads by a second instance of the export, given the files'
absolute paths. That types them as Python objects, so that a blank or numeric label
returns what modelx returns rather than raising `TypeError` (*What compiling changed, and
why*). The committed points leave branches untaken: the female mortality, an issue age
other than 60, a three-subaccount set, a grid with a 0% band, a programme past its first
years, a contract depleted at a year's start without a withdrawal. That still types every
cell, because every branch of a cell returns the one type its others return, a rate a
float in every branch and a phase an int in every branch, and on points that take those
branches the compiled model computes modelx's numbers (above). The sample also raises the
recursion limit, which modelx raises and its export does not (*What a compiled run needs*,
below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which the roll-forwards read and the compile
tests' full sweep evaluates every monthly cell at; plus one because the index starts at
0, and one of headroom:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,142 | 1,140. The longest frame is a contract issued at the GLWB's youngest issue age, 35, covered to attained age `omega_age`, 120, 1,020 months, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: `t = 0 … 1,139`, and the month after, 1,140. Every cell that reads `t + 1`, the count's roll-forward residual and `av_at(t, EOM)` among them, answers 0 outside cover before it reads it, and the reads ahead of the month, the withdrawal year at the anniversary closing it, `is_wd_year`'s scan of its year and `phi_glwb`'s read of the VIX at its quarter's last month, stay in the frame, so nothing reads 1,141, which is the headroom |
| `t`, and `timing`, `kind`, `name` or `i` | 1,142 by 10 | the ten timings of the one numbering, `BEF_NB` 0 to `BEF_ANNIV` 9, the three kinds and `ALL`, the two columns, and the subaccount ids 1 to 9. Every 2-D cache has this one width. Cython's generated unpickle code converts a space's 2-D caches with one function for each inner width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A kind from 4 to 9, a column from 2 to 9 or a timing a cell does not take is then inside the cache, where the cell refuses it as modelx does, and a code from 10 raises |
| `t`, `i` and `timing` | 1,142 by 10 by 10 | `sa_pp_at`, the one 3-D cache, with one inner shape, for the same reason |
| `m` | 1,021 | 1,019, `12 × (omega_age − issue_age_min) − 1`: the last covered policy month at issue age 35, read by `t_of_month`, by the programme readers and by `vix_sq`, at the last month of quarter 340; plus one, and one of headroom |
| `k` | 342 | 340, `4 × (omega_age − issue_age_min)`: the last contract quarter at issue age 35, read by `vix_sq` and `phi_glwb_vix`, past the 84 completed years `surr_charge_rate_at` reads, which shares the name; plus one, and one of headroom |
| `a`, `x` | 121 | 119, the last attained age in cover, read by `gawa_pct_at_age` and `mort_rate_base_at`, from age 0: `omega_age + 1`. It rests on `issue_age_min` only through its being 0 or more |
| `i`, `j` | 10 | 9, `subaccount_id_max`: the last subaccount id, read by `alloc`, `fund_expense_rate` and `sa_pp_init`, slot 0 unused, and the last position of a set of nine, read by `subaccount_id`, with one of headroom. `i` takes no headroom, which would break the one width |

`proj_len()` refuses, first, a point issued below 35, `issue_age_min`, or above 85,
`issue_age_max`, 80, `glwb_issue_age_max`, or, on the `rollup` and `ratchet` GMDB, 79,
`gmdb_issue_age_max`, the issue ages `product-spec.md` admits, and one whose fund set holds
a subaccount id above 9, `subaccount_id_max`; then, as at stage `E`, one with no cover from
issue and one at or past the end of cover at the valuation date, in modelx as compiled, and
cover ends with the month before attained age `omega_age`, so no report on a point the model
projects runs past these caches. `issue_age_min`, `omega_age`, `subaccount_id_max` and
`Data.future_horizon_mth` are the contract the sizes are derived from; the three oldest
issue ages size nothing, since every size rests on the youngest, and set higher they
project the older issue ages `VA_US_S` projects. Lower the minimum, or raise `omega_age`,
the horizon or `subaccount_id_max`, and a report runs past the caches in the compiled model
alone: a frame of more than 1,140 months, a policy month past 1,020, a quarter past 341, an
age past 120 or an id past 9 raises `IndexError`, naming nothing, where modelx projects.
Each needs the sizes derived again, as `spec_sec.py` derives them, `Data.read_last_mth`,
`Data.read_last_age` and `Data.read_last_sub_id` with them, and a rebuild. The shipped
mortality table starts at attained age 40, so a point issued younger than 40 is refused by
`Data` first, naming it, until a table rates its age.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it was
measured to change there. Here `cpow` reaches three powers in three cells: the monthly
rates of both decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`,
and expense inflation, `(1 + r)^n` in `inflation_factor`, whose exponent `n`, the years
from the expense base year, is an int. Without `cpow` a compiler with C99's complex
numbers, gcc among them, computes a power of two doubles as a complex power, which can
differ from Python's float power in its last bits. With both directives and the flag every
compiled value agrees with modelx's bit for bit, and the compile tests hold each, by the
module's first line, by the compiler's command lines and, on x86-64, by the comparison
itself. On the same platforms the tool adds `-Werror=incompatible-pointer-types`, so that
gcc before 14, which only warns of a pointer of the wrong type, fails the build as gcc 14
does: the error two cache widths give (*The sample and the spec*, above).

A power of a negative base is where the two engines would part on a fractional exponent:
Python gives a complex number, or raises, and `cpow`'s C power NaN. The decrements' bases
are held at 0 or more: the mortality's by `Data`, which refuses a rate outside 0 to 1, and
the surrender rate's by its bound of 1. Expense inflation's exponent is an int, so a base
below 0, an `inflation_rate` below −1, gives the same real power in both engines, and,
unlike `FIA_US_SEC`, whose powers take fractional exponents, the model refuses no rate
there. Where Python's float power raises and C's `pow` does not, `inflation_factor` raises
Python's message itself: a base of 0 to a negative power, an `inflation_rate` of −1 with a
valuation year before the base year, `ZeroDivisionError: 0.0 cannot be raised to a negative
power`, where C's `pow` gives infinity; and a power past the largest float from a finite
base, an `inflation_rate` of `1e300`, where C's `pow` gives infinity, by calling Python's
own float power there, which raises `OverflowError` with the platform's message: `(34,
'Numerical result out of range')` on Linux and `(34, 'Result too large')` on Windows, as
`VA_US_S` does.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 5,503,984
bytes, about 5.5 MB, the type's basic size, which holds every cell's cache, each beside a
flag array of its shape that marks what is computed. The seventeen 2-D caches, 1,142 by
10, are about 2.33 MB of it with their flags, two fifths; the 3-D one, `sa_pp_at`'s, 1.37
MB, a quarter; and the 132 arrays by `t` about 1.75 MB, nearly all the rest. That is 1.62
times `FIA_US_SEC`'s, for frames of 1,142 months against 1,094, seventeen 2-D caches 10
wide against thirteen 12 wide, and the subaccounts at each timing, which `FIA_US_SEC` has
not; and three times the 1.81 MB the model compiled to as it stood after running in force,
whose caches the spec did not size but by `t`. Making one and releasing it, nothing
computed, took 0.24 ms here, the collection included. Deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, and only Python's cyclic collector frees it. That is why `run_sec.py --block`
collects after each release, in its frame pass and in its projections (*Run it*, above),
and a compile test holds a compiled block run to one point's ItemSpace at a time. Without
it, 506 compiled points peaked at 2,547 MB (*Speed*, below). Cython's
generated function that would unpickle an ItemSpace declares one C array a cache shape on
its stack, the 3-D shape's two, of `double` and `int`, 1.37 MB between them, past the
1 MiB Windows gives a thread; nothing pickles a compiled space, the tests pickling only what
the cells return, so no run reaches it, as no run reaches `VUL_US_SEC`'s.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no limit
raised. What it needs is stack. The deepest calls the contract allows, cold in the last
month of the longest cover, issue age 35, issued now or 120 months on, run the count's and
the account value's chains back to `t_entry()`, 1,042 cells deep in modelx on `pols_decr`
at `DEATH` or `LAPSE`, 1,041 on the count's roll-forward residual,
`check_pols_roll_fwd_resid`, and on `pols_lapse`, and 1,034 to 1,035 on `net_cf`: one cell
a month and 14 to 22 more, the count's first month reading the withdrawals' chain at the
anniversary closing its year. Compiled with gcc, with `Data` read first, `pols_decr`, the
residual and `pols_lapse` run on a thread of 234 KiB of stack and not of 232, about 230
bytes a level, and `net_cf` on 232 KiB and not 230; a thread that reads `Data` too, cold,
needs 246 KiB. A test runs `pols_decr`, the residual and `net_cf` cold, at the valuation
date and 120 months on, in a thread of 1 MiB, the stack Windows gives a program's main
thread unless the program is linked for more, and again on the main thread, which is where
`run_sec.py --cython` runs. MSVC's frames may be larger than gcc's, and the `cython` CI job,
which runs the test on Windows too, is the check on them: the test first runs the call at
seven stacks, from 256 KiB to 2 MiB, and reports the smallest it ran on, so a first run
there measures MSVC's need. Until it has, the need is an
estimate: at the 325 to 433 bytes a level MSVC took on `WholeLife_US_SEC`'s chain, 1,042
levels need about 331 to 441 KiB, inside 1 MiB by more than twice. A stack below the need
kills its child on an overflow, by design; on Windows the child ends with
`STATUS_STACK_OVERFLOW`, and should Windows Error Reporting hold it instead, the test
waits a bounded time for each child rather than the job's hour. The export recurses in
Python instead: the same calls need a recursion limit of 2,092 there on `pols_decr`, 2,090
on the residual and `pols_lapse`, and 2,079 on `net_cf`, and the four reports and the three
checks, which run in ascending `t`, need 1,149 with the package's import, on point 8, whose
GAWA is first read at policy month 563, as the sample runs them, so `sample_sec.py` sets
9,000, four times the first rounded up to the thousand, and a test holds it to that
derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode or hold, when the vector is first read, naming every point at
  fault, or the table and its lines: a `point_id` that is not a whole number,
  `model_point_table_sec.csv: point_id must be a whole number; ['7x'] is not`, read by
  `point_id()`, and so by every refusal and by `run_sec.py`, where `VA_US_S` and stage `E`
  take any label pandas reads, text among them; the projection, keyed by position, reads no
  label, so the table's other cells project. And, before it is cast to int64, a number of
  `2**53` or more in size, which numpy would cast to the least int64 once past int64: a
  model point's `duration_mth`, issue age, `wd_start_age` or `bonus_end_init`,
  `model_point_table_sec.csv: duration_mth must be below 2**53 in size; it is not at
  point_id [3]`, refusals `VA_US_S` lacks, which reads each by Python's `int()`; a
  `point_id`; and, by the table's check, which every reader of the table asks first, an
  assumption table's key, `rate_scenario_sec.csv: t must be below 2**53 in size; it is not
  on line [6]`. A key written as a float, an age `61.0`, is read by its value, as
  `VA_US_S`'s lookups match it, and a key that is not whole is refused by the table's check,
  as at stage `E`. A key far past any read, short of `2**53`, is held nowhere and refuses
  nothing (*What compiling changed, and why*).
- A key beyond a table, by the one cell that reads it, naming the point, where `VA_US_S`'s
  lookup raised `KeyError`: an attained age outside the point's sex's,
  `point_id 1: the mortality table gives no rate at attained age 39`, from
  `mort_rate_base_at`; a count of completed years below 0, `point_id 1: the withdrawal
  charge scale gives no rate at -1 completed years`, from `surr_charge_rate_at`; a
  subaccount the point's set does not hold, `point_id 1: the fund set holds no subaccount
  3`, from `alloc` and `fund_expense_rate`, and a position past the set's last,
  `point_id 1: the fund set holds no subaccount at position 2`, from `subaccount_id`; and a
  month before the scenario's first, `point_id 23: the return scenario sets no return for
  subaccount 1 by month 0`, from `inv_return_mth`, and `point_id 23: the rate scenario sets
  no level by month 0`, from `scenario_rate`. No projection reaches any of them: `Data`
  refuses a point whose first month on the books its tables do not cover, and the
  projection reads each table in cover alone. Each reader likewise refuses a read past the
  month, age or id its array is held to, `Data.read_last_mth`, `Data.read_last_age` or
  `Data.read_last_sub_id`, which no projection makes; inside the caches the arrays reach
  those bounds, so compiled, a read past them meets the cache's end first (below). A policy
  month a programme has no row at, one before policy month 0 among them, is no premium and
  no withdrawal, and an age below a grid's first band, a negative one among them, is 0%, as
  in `VA_US_S`.
- By `proj_len()`, in this order: a point issued below `issue_age_min`, above
  `issue_age_max` or `glwb_issue_age_max`, or, on an elected GMDB, above
  `gmdb_issue_age_max`, `point_id 1: issue age 81 is above glwb_issue_age_max, 80, the
  GLWB's oldest; raise glwb_issue_age_max to project it`; one whose fund set holds a
  subaccount id above `subaccount_id_max`, `point_id 1: its fund set holds subaccount 10,
  above subaccount_id_max, 9; raise subaccount_id_max and Data.read_last_sub_id, and
  rebuild a compiled model, whose caches it sizes, to project it`; then, as at stage `E`,
  one whose cover from issue is empty, one at or past the end of cover at the valuation
  date, and the five rules of the opening state that need a `Projection` Reference. The
  first five are refusals `VA_US_S` lacks, which projects each point given the tables to
  read it with: the product does not issue it, or the compiled model's caches cannot hold
  it. `Data` holds a set with an id past the hold, its other ids, its count and its last id
  kept, so that the refusal is `proj_len()`'s, naming the point and the Reference.
- A divisor of zero, with Python's message: a `vix_divisor` of zero, in `phi_glwb_vix`, and
  a `cmt_round_step` of zero, in `rollup_rate`, `ZeroDivisionError: float division by
  zero`, which each cell tests before it divides, since compiled division words it `float
  division`; and a `fee_reset_years` of zero, on the five-yearly fee increase, in
  `phi_glwb`, `ZeroDivisionError: integer division or modulo by zero`, which compiled
  integer division raises in Python's words, so no test is written. `VA_US_S` raises each
  of the three. Every other division divides by a constant, 4.0 or 12.0, or by an account
  value, a charge due or a base the cell tests first, answering 0 where it is 0 or less,
  as `VA_US_S` does.
- A CMT-linked roll-up whose rounded rate is not a number, `ValueError: cannot convert
  float NaN to integer`, or is infinite, `OverflowError: cannot convert float infinity to
  integer`, from `rollup_rate`, each `VA_US_S`'s `math.floor`'s message; and expense
  inflation's two powers Python refuses (*Two compiler directives*, above).
- A timing, a kind or a column a cell does not take, `ValueError("invalid timing")`,
  `("invalid kind")` and `("invalid name")`, where the code is inside the cell's cache: a
  code of another family, `pols_if_at(0, BEF_WD)`, `av_pp_at(0, BEF_NB)`,
  `gwb_pp_at(0, BEF_INV)`, a kind a cell lacks, `claim_pp(0, ALL)`, a code up to 9,
  `claims(0, 5)`, and a column past the two, `scenario_rate(0, 2)`; and a switch's value no
  decode names, `invalid stepup_basis`, `invalid gmdb_option`, `invalid fee_reset_rule` and
  `invalid rollup_rule`.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1142)` and `net_cf(-1)`, which modelx answers with 0.0; `pols_if_at(0, 10)`,
`claims(0, 10)`, `scenario_rate(0, 10)` and `sa_pp_at(0, 1, 10)`, which modelx refuses as
`invalid timing`, `invalid kind` and `invalid name`; `t_of_month(1021)` and
`t_of_month(-1)`, `prem_scheduled_pm(1021)` and `prem_scheduled_pm(-1)`,
`surr_charge_rate_at(342)`, `vix_sq(342)`, `phi_glwb_vix(-1)`, `gawa_pct_at_age(121)` and
`gawa_pct_at_age(-1)`, and `mort_rate_base_at(121)`, which modelx answers with a number;
and `prem_scheduled_pm(1142)`, `surr_charge_rate_at(-1)`, `mort_rate_base_at(-1)`,
`alloc(10)`, `subaccount_id(10)` and `subaccount_id(-1)`, `sa_pp(0, 10)` and
`inv_return_mth(0, 10)`, which modelx refuses, naming the point and the key. An `idx` past
the last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's last
point, under that point's own `point_id()`, 23.

A Reference is a C variable of its value's type: `issue_age_min` and the other bounds,
`omega_age`, `fee_reset_years`, `valuation_year`, the codes and `idx` a `long long`, as
`Data.future_horizon_mth` is, and the rates and amounts a `double`. Set past that type, it
is converted when it is set, where modelx keeps the value as given. A float set on an int
Reference is truncated toward zero without a word, `omega_age = 120.7` reading 120, so that
point 1's `proj_len()` is 720, where modelx computes with the float, a `proj_len()` of
728.4. A text, a NaN, an infinity or an int beyond 64 bits is refused at once, with
`TypeError`, `ValueError` or `OverflowError`, `omega_age = "120"` among them, which modelx
takes and then fails on at the first cell that computes with it. An int set on a `double`
Reference reads as a float compiled, where modelx returns the int: `rollup_pct_young = 1`
gives `rollup_pct()` 1 in modelx and 1.0 compiled. Each shipped Reference is a value of its
C type, so no shipped number differs.

Mortality takes no factor and no cap, as in `VA_US_S`, and `Data` refuses a rate that is
not a number, so no NaN reaches it through a Reference. The surrender rate's bound of 1 is
`VA_US_S`'s `min(1.0, …)`, the bound first, and the moneyness multiplier's two bounds,
`min(lapse_itm_upper, max(lapse_itm_lower, …))`, and the VIX clip's, `min(hi, max(lo,
raw))`, each of `lo` and `hi` a bound of the corridor against one of the band, are written
the same way, the inlined engines in `VA_US_S`'s order; the compiled model computes each as
comparisons in the same order. So a NaN sent through a Reference gives the bound it reaches
first, in both engines: a `lapse_rate_sc` of NaN a surrender rate of 1, every contract
surrendering in month 0; a `lapse_itm_threshold` of NaN the multiplier's lower bound, 0.5;
and a `vix_band` of NaN the corridor alone, the formula's rate unclipped by the band. One
sent into the account value, an `asset_charge_me` of NaN, fails the account value's
roll-forward check and the charge split's, in both.

### Speed

`python tools/bench_sec_cy.py variable_annuity` builds the model into a temporary
directory, or takes a build with `--build`, and times one block run on three engines:
modelx, the export and the compiled model. Each engine runs the committed table repeated,
in a process of its own, as `run_sec.py --block` runs a block, each point projected and
then released. `net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,003 | 1.70 ms (10.23–11.08) | 2.60 ms (15.61–16.59) | 94 MB |
| export | 621 | 22.2 ms (13.80–14.25) | 21.9 ms (13.59–14.36) | 94 MB |
| modelx | 138 | 815 ms (112.47–114.29) | 899 ms (124.06–125.41) | 204 MB |

On `net_cf` the compiled model runs 13.0 times its export, and on `result_cf`, where
building the DataFrame takes much of its time, 8.4 times; it runs 478 and 346 times modelx.
A second run of the compiled model and the export straight after, under a 1-minute load
between 1.7 and 3.0, gave the compiled model 1.72 and 2.67 ms and the export 22.2 and 22.2
ms, 12.9 and 8.3 times. The compiled model takes 1.4 times `FIA_US_SEC`'s time a point,
1.19 ms, for an ItemSpace 1.62 times the size; of it, making and releasing the ItemSpace
takes about 0.24 ms. It runs about as many times its export as `VUL_US_SEC`, 13.8,
`MYGA_US_SEC`, 12.6, and `FIA_US_SEC`, 12.2, and more than `UL_US_SEC`, 12.0,
`Term_US_SEC`, 9.5, or `BasicTerm_SC` on its own measure, 8.7. As it stood after running in
force, compiled the same way, the model ran 1.1 times as fast as its export (*What compiling
changed, and why*, above), and the compiled model runs about 75 times that build on the
same measure, 1.7 ms a point over the committed points against 127: the representation, not
the compiler, is the gain, and the export gained from it too, 20.3 ms a point against 143.
The release keeps a block flat: the compiled model's peak grew by less than 0.1 MB over its
6,003 points, and without the collection after each release (`--no-collect`), 506 compiled
points peaked at 2,547 MB. Reading the seven files and building every `Data` vector and
array for those 6,003 points took 2.27 s, a cost that grows with the points, the table's
checks and the vectors running over every row, and asking every point for its frame, the
runner's first pass, 1.50 s, most of it making and releasing an ItemSpace a point.

Measured on 2026-11-14 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 1.0 and 2.3 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Each time is the fastest of three runs; under load the spread
is wide, and the fastest run is the one to compare. The comparisons over the committed
points, with the build as it stood after running in force, are the fastest of two runs of
three rounds each, in one process an engine, under a load between 2.2 and 2.5, and so is
the cost of an ItemSpace, the fastest of five rounds of 1,000.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 and 3 to 9,
  issued at the valuation date, every cell of `VA_US_S`'s agrees at every argument
  `VA_US_S` evaluates in its own sweep, but for `pols_if_init`, `model_point` and
  `result_pols`, whose meaning changed. So the goldens `tests/test_variable_annuity_us.py`
  asserts on those points hold here with no number restated, and those on point 2 hold
  through the splice (below). The identity holds on any count, since `VA_US_S` already
  weights its premium by the contracts in force and charges acquisition in the issue month
  of its new business. The same suite holds the model to the conventions every `_SEC` model
  meets: every frame starts at `t = 0`, `pols_if` is the `BEF_DECR` count, new business
  enters once at its `policy_count`, nothing happens before issue, and the in-force columns
  are present; and to `VA_US_S`'s own fact on the valuation clock, both roll-forward
  residuals inside the model's own tolerances, scaled by the count, at `t = 0`, 60, 120 and
  299 wherever the frame has them.
- **The splice**, in `tests/test_variable_annuity_us_sec.py`: each `VA_US_S` point restated
  in force at a month either side of its events continues the S projection, in `result_cf`
  and `result_pols`, column by column, and in every other cell the two share, to 1e-9
  relative with no absolute floor, but those the twin identity skips and those a restated
  row changes by design: the opening-state cells, which read the row's columns; `proj_len`,
  a frame on the valuation clock; `duration_mth_init`, `is_inforce` and `t_of_month`, which
  read the months in force; `scenario_id`, which names the row's own scenario copy; and
  `policy_id`. The cells whose exact value can be 0 while the computed one is rounding about
  it keep a floor of 1e-9: the roll-forward residuals, and the GWB a contract not for life
  runs down to 0, with the payment a contract on it and its moneyness, where an opening
  state the CSV gives back an ulp off leaves the two models 1e-11 apart. The payments in
  force, a payment a contract times a count that falls to 1e-12 late in a long frame, fall
  to about 1e-8, where that floor would pass an error of several per cent, so they are
  compared with none, in the cell and in `result_cf`'s column, but at the months where both
  models pay less than the floor a contract, the GWB's rounding about 0. `VA_US_S`'s own
  point 2 continues it too, at offset 0, the cells its acquisition at `t = 0` moves compared
  from `t = 1`, and the worked example's goldens hold on it at `t = 0` and on point 1 at
  `t = 26`. The anchor is restated at the starts of contract years 2 and 3, in the Bonus
  Period; at the worked example's month; at policy months 40, 60 and 71; at 119 and 120,
  either side of the start of the year of its first withdrawal, and in that year's middle
  and last months; in the last month of contract year 12, where its GWB Adjustment Date
  falls; and at the month its account value runs out and twice after it, mid-year and at a
  year's start. `VA_US_S`'s point 2 is restated at four of its months, each copy of its
  scenarios moving by `26 + d`, and the other points either side of their own events: the
  decline's depletion, valued in the month it runs out, and the year's start after it, the
  excess withdrawal and the premium after it, valued in the premium's month, the
  highest-quarterly step-up, a quarter's last month on the VIX-linked fee, the Adjustment
  Date where the Adjustment binds, the depletion without a withdrawal, valued in its month,
  and the last policy month. Seventeen variants of S's points, in a copy of S's table that
  is never committed, carry what S's own points do not, each with input rows of their own: a
  programme that pays a premium of 10,000 at policy month 62 and withdraws 12,000 at 66,
  3,000 at 69 and 2,000 at 83, the last month of contract year 7, restated around each, so
  that the year's opening Benefit Base, the year to date and the withdrawal year read ahead
  are compared where they differ from what `VA_US_S` assumes before its frame; a path that
  exhausts a never-withdrawing account at 56, the Adjustment carried to its date; the female
  table; a second fund set and a second GAWA% grid; issue ages 55, restated at a contract
  year's start depleted not for life with its GWB below its GAWA, so that the first payment
  on the books is the GWB its row carries, and 72; a path whose quarter ends swing, so that
  the year's highest quarterly value falls before the valuation month and wins the step-up;
  two never-withdrawing points at issue ages 55 and 56, for the Bonus Period's restart age;
  issue ages 69 and 70, either side of the roll-up rate's split, the first with a premium of
  60,000 at policy month 100, the second on a GAWA% grid of 60%, a path that falls through
  its first contract year and gains 10% a month through its second, and withdrawals that
  take the GWB to its floor of 0 inside the limit and past it and the GAWA to the GWB; a CMT
  that falls mid-year below the year's dollar-for-dollar use; a contract not for life at 59,
  withdrawing 130% of its limit from 62, whose GWB runs down to rounding about 0; the
  never-withdrawing roll-up and return of premium with no premium tax, whose accounts run
  out at policy months 524 and 659 on a rounding of 5.7e-15 and of −2.3e-14, each restated
  the month after, depleted on what is left, the first of which only the threshold, not 0,
  reads as depleted; and the anchor on a fund set of three subaccounts, a third that the
  shipped fund table lacks, whose value column the generator takes from the fund table of
  the S model it reads. Each variant's twin, issued at the valuation date, is compared with
  its S point cell by cell, as a restated row is: on variant 16's, which withdraws in its
  first contract year on the roll-up death benefit, the year's opening Benefit Base comes by
  the issue rule at `t = 0`. 88 cases in all. Inflation, on the valuation clock, is set to 0
  in both models; the acquisition expense, the commission and the premium tax, which ship at
  zero, are switched on in both; and the GWB Adjustment is raised to 200%, at which it binds
  at policy month 143 on points 7 and 8. A second set of References, read into the same pair
  of models in turn, switches what ships idle, each where it binds with an effect: a current
  GLWB charge of 0.7%, so that the VIX-linked rate meets its corridor's floor and the
  step-ups it leaves the account value to make raise the Bonus Base at attained age 81, the
  restart age, which restarts the Bonus Period, at 82, which does not, and later; a GWB cap
  of 151,000, which a premium after issue also meets; and a shock-year surrender rate of
  125%, which the bound of 1 caps: 11 cases. The quarters before a row's books are history
  on the restated row, which reads the last one's rate from its column, so `VA_US_S`'s
  VIX-linked rates of those quarters are not compared.
- **The core grid and the full one.** By default the splice runs 26 of its 88 cases, the
  future business 8 of its 27 and the switched References 6 of their 11, which between
  them reach every branch, every opening-state column, every kind of valuation month and
  every category of input the full grids reach, and a test asserts that they do; line
  coverage of the grids showed the default rows executing every line of `Projection`'s
  formulas that the full grids' rows execute. Line coverage cannot tell `>=` from `>`, so
  each boundary of the step-up base's two reads, the frame's quarter ends and the year's
  column, and of the year-open Benefit Base's has a core row on each side of it, and so
  does each age boundary of the contract: the Bonus Period's restart age and the roll-up
  rate's split. The same test checks every bound by the values it bounds: each side of
  every `min` and `max` in `Projection` wins, the other below it, in some call the sweep or
  the comparison of a core row makes, but ten sides it names idle, each with its reason,
  two `VA_US_SEC`'s own tolerances scaled by a count above 1 and eight that cannot bind by
  a premise the cells hold, and two it names bound elsewhere, each by a test that compares
  its rows with `VA_US_S` and asserts the side wins there: the GWB above the GWB
  Adjustment on its date, at the shipped 105% on the committed rows, and the mortality's
  age clamp, on a table that stops below cover. The other cases carry the `sec_full`
  marker and show as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set. One leg of
  the CI matrix sets it, so every CI run runs the full grid too.
- **Future new business**: S's eight points issued at the valuation date and the seventeen
  variants, each issued a month after it, and the anchor and the VIX-fee point, issued 15
  and 13 months after it, are each the S projection moved on, with zeros before issue in
  every report, every decrement rate the float 0.0 there, and no table read at an age, a
  contract year, a quarter or a policy month the contract does not have; their scenario
  copies set nothing before issue, so a scenario read there would raise. A point issued
  more than a year on reads contract year −1 before issue, which is what shows a missing
  guard.
- **How it computes**: on every row the splice and the future business compare, under both
  sets of References, after every report, no cell has been called at a negative month, none
  evaluated from `t_entry()` on has read a month before it, and none evaluated at month `t`
  has read a month later than `t + 1`, directly or through a cell keyed by a year, an age, a
  quarter or a policy month, but the withdrawal-year factor's reads at `anniv_mth(t)`, each
  admitted by reader, cell and month, inside the frame, with what it reads walked for a
  count, a decrement or a later month; and no table is read at an age, a year, a quarter or
  a policy month before the books. On a fresh read of the committed model `duration_mth`,
  `anniv_mth` and `year_open_mth` are closed forms, and every point is swept under a
  recursion limit lowered to 600, which a recursion backward over the frame would exceed
  on every committed frame but nine short ones. And a cold last-month call runs one cell a
  month back to `t_entry()` and at most 20 more, the count alone at most 11 more again, on
  the committed points and at the longest cover, 1,020 months from issue age 35, at the
  valuation date and 120 months on.
- **Counts, validation and regeneration**: the roll-forward closes, `AFT_DECR` is the next
  month's `BEF_NB`, and `pols_if_at` refuses a timing it does not have; `result_pols()` is
  `VA_US_S`'s, column for column, with `pols_new_biz` beside it; scaling `policy_count` by
  2.5 on seven committed rows, with the zero-shipped assumptions switched on and the premium
  tax charged, scales every cash flow and every counted cell and moves no per-contract
  value, and at a million contracts on three rows the roll-forward checks close on their
  scaled tolerance, where the fixed one would fail; each of 118 malformed model point tables
  is refused naming its column or its point, by the one check it is built for, as the table
  is read and through a projection, a key that the table it joins lacks among them, a GWB
  with its GAWA zeroed where the GAWA% is locked, a subaccount value just past a cent below
  0, and a withdrawal status with no GAWA% locked at each end of the ages its grid is read
  at, issued at the shipped grid's first age and, on a grid paying 0% from 60, issued at 59
  and valued at 12 months, its month before the valuation month still at 59; each of 61
  assumption tables and companions whose keys or values cannot be read, a key written as
  text in each, is refused naming the file and the lines, by `Data` and by a projection that
  reads it; every refusal of `Data`'s eight checking cells, entry by entry, 138 entries, is
  the first refusal of some case; a step-up basis, a GMDB election, a fee rule and a roll-up
  rule that no decode knows each raise `VA_US_S`'s own message, in both models; a scenario
  that sets nothing by the first month a point on it is on the books is refused for that
  point; keys and integer columns written as floats are read by value, and the two flags
  written as 1 and 0, or as 1.0 and 0.0, as the flags they hold; the horizon is a Reference,
  which refuses a point issued past it, at 0 any future business, saying so, and below 0
  itself; a point issued at the age cover ends, or valued at the end of cover, is refused by
  `proj_len()`, while one issued a year before that age, or valued in its last covered
  month, projects, and `run_sec.py --block` refuses such a point before printing anything;
  so is each opening state a rule needing a `Projection` Reference forbids: a GAWA% locked
  with neither a withdrawal nor depletion, on an account value of 0.6 cents, just above the
  depletion threshold, too, none on a contract depleted without a withdrawal, no step-up
  history three and eleven months into the year, and one at the threshold itself, a VIX
  prior other than `phi_glwb_curr` in the second quarter's first month and its last, and one
  outside the corridor from the third, while the months either side of each window, two
  months into the year and the next year's first with no history, and the first quarter's
  last month with no prior and the third's first with a prior other than `phi_glwb_curr`,
  project; the edges of the interface are accepted: the first contract year at both ends and
  the second year's first month, amounts a part of a cent inside their tolerance, the
  step-up history and the VIX prior from their first months, the history just above the
  depletion threshold, the VIX prior at both ends of the corridor, a withdrawal status with
  no GAWA% locked where the grid gave 0%, below its first band or in a band at 0%, at both
  ends of the ages the grid is read at, issued a year below the shipped grid's first age
  and, on the grid paying 0% from 60, issued at 59 and valued at 13 months, its month before
  the valuation month its first at 60, a contract depleted without one there, and a GWB and
  a GAWA% above 0 with no GAWA there; an opening account value of exactly the depletion
  threshold, and of part of it, each read as depleted; a depleted contract marked as one
  that withdrew, a count of 0, and a rate scenario that no point reads left out; and, on a
  first quarter's rate of 0.1%, below the corridor's foot, a VIX prior below the foot in the
  third quarter, which the clip gives there; each value column holds the bounds of its
  range, an allocation, a fund expense, a GAWA%, a withdrawal charge and a mortality rate of
  0 and 1, a return and a CMT just above −1, a VIX average, a premium, a withdrawal
  intensity and a premium tax of 0, a locked GAWA% of 1 and a year's proportional factor of
  0, a subaccount value a cent below 0 on a depleted contract, and, on a first quarter's
  rate of 100%, a VIX prior of 1; the committed table with every amount of its opening state
  rounded to the cent, as an extract carries it, reads, and each point passes `proj_len()`
  and enters its first month depleted exactly where it did; a mortality table stopped at 110
  and a charge schedule stopped at three years on 5.5% are read past their ends as `VA_US_S`
  reads them; and the committed tables are what `VA_US_S` generates, their text `VA_US_S`'s
  or composed from its keys.
- **The opening state and the rest**: each derived row's opening state is what `VA_US_S`
  carries into its month, and at the shipped assumptions each row in force, point 2 among
  them, is S's from that month on, in every cell but those expense inflation moves;
  `policy_count` and each of the twenty state columns, changed on a copy of a committed row
  that reads it, against a baseline that differs from it in that column alone, changes what
  the row reports, and three controls change nothing; the year under way reads its opening
  state; depletion is derived from the opening account value, and point 18 carries
  `has_wd_init` `False` with a GAWA% locked; the scenarios run on the valuation clock and
  the programmes on the policy clock; expense inflation runs on the valuation clock at the
  shipped 2.5%, which only this test sees, since the splice sets the rate to 0; the single
  premium and acquisition fall in the issue month alone, per contract issued, never on a row
  in force, and the commission and the premium tax on each premium as it is paid; the
  surrender rate reads the withdrawal year at its anniversary; a depleted row projects its
  whole frame at a zero account value; a NaN mortality rate reaches the count and its
  residual as NaN, and a NaN asset charge the account value's and the charge split's
  residuals, and each check whose residual is not a number fails; each keyed reader returns
  `VA_US_S`'s own lookup at every key the contract can ask for; every guarded cell holds its
  value outside cover and reads no rate there; the points of a block sum row by row; an
  extract without the generator's three columns, labelled apart from its positions, projects
  the same numbers, and `run_sec.py` finds its points by label; the docstrings describe the
  valuation clock, the symbol map names every cell running in force adds and no row of it
  leaves a column blank, no row of a docstring's table runs into a column gap, and, where
  docutils is installed, every docstring parses without a warning; the model reads
  `VA_US_S`'s tables in place, but for its model point table and its two scenario
  companions, and every Reference of either Space is `VA_US_S`'s but the four it adds; each
  Reference a rewritten cell reads that ships equal to another, the M&E charge and the CMT
  spread, the charge years' surrender rate and the CMT floor, the bonus and the younger
  roll-up rate, the VIX formula's offset and the Bonus Period, and the GWB Adjustment's age
  and the roll-up rate's split, is read as itself: with each pair set apart, the twins of
  `VA_US_S`'s points are `VA_US_S`'s in every cell; and `run_sec.py` prints the model's
  numbers, for the anchor issued at the valuation date, the worked example in force, a
  depleted point and a point issued later, and the block, writes "1 month" for a point a
  month either side of the valuation date, and refuses a label the table lacks, a number or
  not, naming the labels it has.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py VA_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their call
  syntax changed: a point's position for its label, the codes for the text of a timing, a
  kind or a rate column, and `ALL` for `None`; and the cases that issue a point at the age
  cover ends, or a year before it, lower `issue_age_min` or raise the oldest issue ages to
  reach it, the bounds being References `proj_len()` checks first. Each point is named by
  its label, in `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: the two `ALL` totals are `VA_US_S`'s `(t, None)` bit for bit,
  sign of a zero and type included, and with every kind set to −0.0 each total is −0.0, as
  `VA_US_S`'s chain gives; every parameterless cell but the reporting ones returns a Python
  `int`, `float` or `bool`, not a numpy scalar (R11); a point issued below `issue_age_min`,
  above `issue_age_max` or `glwb_issue_age_max`, or above `gmdb_issue_age_max` on an elected
  GMDB, and one whose fund set holds an id above `subaccount_id_max`, are refused by
  `proj_len()`, naming the point, and each projects once its bound is moved past it; the
  inlined engines are `VA_US_S`'s engine cells bit for bit, under NaN too, and the
  CMT-linked roll-up's rounding is `VA_US_S`'s `math.floor`, bit for bit, at a tie for each
  CMT level of the VIX and CMT twin too, where the order of its operations shows, in modelx
  and compiled, its three refusals `VA_US_S`'s word for word; a number cast to int64 is
  refused at `2**53` itself, and at `2**53 − 1` passes the bound; each table is numbered as
  its docstring says, the fund sets in the file's order, and a set's ids stay in the file's
  order; each sex is read at its own ages; each value a decode names, written in another
  case or with a space beside it, raises `VA_US_S`'s message, as `VA_US_S` does; the `Data`
  vectors are int64 or float64 arrays of the shapes the `Data` docstring's table gives and
  every extent an int; each array holds NaN where nothing is read; each size in
  `spec_sec.py` is the one its comment derives from the model's References,
  `Data.read_last_mth`, `Data.read_last_age` and `Data.read_last_sub_id` with them, and the
  sample's recursion limit the one its comment derives; the sample calls the engine cells at
  the module's own arguments; the spec's `twin_arg_map` maps `VA_US_S`'s totals and rate
  columns onto the codes; and `run_sec.py` sums the block as `groupby` does, bit for bit,
  and outside the repository `run_sec.py --cython` says it cannot build, and in place it
  rebuilds exactly when no build is there or a source is newer than the build, and it
  refuses a package whose `Projection` imports from `_mx_classes.py`, its extension module
  missing.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting and engine ones refers to pandas, numpy, `math` or another
  module, reads a table with `.loc` or the like, calls a reporting or an engine cell,
  holds text but in its docstring and its refusals, or holds a generator, a comprehension,
  a tuple or a nested function; none calls anything but a cell, a `Data` vector and the
  builtins of *No Python call kept*, and the registry admits no other for this model;
  every `Data` vector a formula reads is an int64 or float64 array, read by element; no
  cell is uncached; and each label accessor returns its point's column, `stepup_basis` its
  `glwb_stepup_basis`.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting and engine ones a C
  `bint`, `long long` or `double` and a C-array cache of exactly the spec's size, and every
  new `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps
  no Python object among a projection cell's locals, calls no Python builtin there, and
  builds no container, under both directives (C3); on the committed points, every cell at
  every argument a full modelx sweep caches is what modelx computes, bit for bit on x86-64,
  and so are every raise and every `Data` array (C4); and `run_sec.py --block`, run
  compiled, holds one point's ItemSpace at a time. In
  `tests/test_variable_annuity_us_sec.py`: the same comparison, with the codes, readers and
  engine calls no report reaches, on the committed points, on the splice grid and under the
  switched References, the core by default and the full grid with `USLIB_SEC_FULL=1`; at the
  contract's extremes; where the caps bind; on each sex at its own ages; on labels that are
  not text and keys that are numbers; on tables written out of key order with their keys as
  floats; on keys far past any read, one model held at a time; and on NaN sent through a
  Reference and, by a Python subclass of the compiled `Data` set as `Projection.data`,
  through the mortality to the count; the compiled model refuses what modelx refuses, with
  modelx's message, on a relabeled table, the contract's bounds among them, and an argument
  past a cache raises `IndexError`; a divisor of zero, an integer one among them, and a
  power Python refuses raise `VA_US_S`'s error in both engines, word for word; the deepest
  calls the contract allows run cold on a 1 MiB stack and on the main thread, and the test
  reports the smallest of seven stacks, 256 KiB to 2 MiB, they ran on, waiting a bounded
  time for each; a Reference set after the model has computed changes no value it has
  cached; and `run_sec.py --cython` prints what `run_sec.py` prints, refuses a label the
  table lacks as `run_sec.py` does, and refuses a `--build` directory that holds no build.
  Every case of more than four points, the committed points' among them, is compared four
  points at a time (`C4_CHUNK`), each its own case, so that a run holds one chunk's sweep.
  They are marked `cython`, and they skip without the toolchain, but in the `cython` CI job,
  which installs it on Linux and on Windows, one leg a product, a skip fails, whatever made
  it.

The module's cost, measured at M22 on a 4-CPU Linux machine shared with other runs, one run
each (Python 3.13, modelx 0.33.0, modelx-cython 0.1.0, gcc 13.3): by default, the whole
module, the compile tests among them, ran 372 tests in 40 min 7 s, peaking at 9.6 GB, since
the compile tests follow the committed models the modelx part holds; its modelx part alone,
as the `sec` job runs it without modelx-cython, ran 343 in 14 min 42 s before the review's
roll-up and bound cases were added, peaking at 4.2 GB; and the `cython` job's leg,
`USLIB_CYTHON_SHARD=variable_annuity USLIB_REQUIRE_CYTHON=1 python -m pytest -m cython
tests`, ran its 20 tests in 26 min 27 s with the build, about 4.5 minutes of it, peaking at
6.0 GB, set by the splice grid's comparison, which holds the splice's two models beside a
chunk's sweep. The compiled cold calls at the longest cover need between 244 and 246 KiB of
thread stack with gcc.

```bash
python -m pytest tests/test_variable_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_variable_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k VA_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k VA_US_SEC
python -m pytest tests/test_variable_annuity_us_sec.py -q -m cython  # compiled
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-variable_annuity-r1
[std]: #uslib-std
<!-- END generated citation links -->
