# In-Force Implementation Notes

**Status:** Draft, 2026-11-10. `IUL_US_SEC` is [`IUL_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there, in any month of their policy year and with up to twelve index segments live,
and policies to be written in the ten years after it, as lifelib's `basiclife/BasicTerm_SE`
extends `basiclife/BasicTerm_S`. The product is the one
[`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `IUL_US_S` on another time axis, and it reads `IUL_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced: the 10.00% current
> and 2.00% guaranteed caps, the 100% participation and the 0% floor of the Benchmark
> Index Account [S2] [R1], the 4.50% current and 1.00% guaranteed fixed-account rates
> [S2], the monthly ladder of 1-year S&P 500 point-to-point segments, up to twelve live at
> once [S2] [S3] [S4], the $10 policy fee [S3] [S5], the $25 withdrawal fee [S3], the
> cumulative-MNLP no-lapse test [S3] [S4], the 10-year surrender charge period
> [S1] [S5] [S7] and the IRC 7702(d) corridor factors [R4]. Every behavioural and expense
> assumption, the whole COI scale, the surrender charge dollars, the per-unit charge and
> **the 6.40% level index return** are **[std]** standardizations introduced for the
> reference implementation. Replace them with company data before drawing any conclusion
> from the numbers.

## Run it

```bash
python products/indexed_ul/run_sec.py            # point 1: S point 1, issued now
python products/indexed_ul/run_sec.py 7          # point 7: S point 4 in force 65 months
python products/indexed_ul/run_sec.py --block    # every model point, summed row by row
python products/indexed_ul/run_sec.py 7 --cython # point 7 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about three
minutes, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer
than the build, and says so on stderr. `--build DIR` runs a build made elsewhere instead
(*The compiled model*, below). Nothing a build leaves is committed, and `.gitignore`
covers it.

The first prints, as rows `t = 0 … 11`, the cash flows, the account value roll-forward,
the segment ladder and the counts behind them for point 1, `IUL_US_S`'s baseline cell
issued at the valuation date: its cash flows, its account values and its segment ladder
are the numbers `run.py` prints for `IUL_US_S`'s point 1 in the same months. The second
prints point 7, `IUL_US_S`'s monthly payer restated 65 months after its issue. It brings
in all twelve of its live segments, and one of them matures in each of its first twelve
rows: the one in slot 12 at `t = 0`, credited 233.73 a policy, 6.40% of its 3,652.04.
Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/indexed_ul/IUL_US_SEC")
model.Projection[6].result_seg()     # point 7, the table's seventh row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[6]` is point 7, and its `point_id()` says so. Its four result tables are
indexed by `t`, with one row per month from the valuation date, `t = 0 … proj_len() − 1`:

| Cells | What it shows |
|---|---|
| `result_cf()` | `IUL_US_S`'s columns — `pols_if`, `premiums`, `claims_death`, `claims_lapse`, `withdrawals`, `expenses`, `premium_taxes`, `net_loan_cf` and `net_cf` — income-positive, so the flow columns net to `net_cf` |
| `result_av()` | `IUL_US_S`'s per-policy account value roll-forward, in the notes' processing order, then the surrender charge, the net cash surrender value and the loan, with zeros before issue |
| `result_seg()` | `IUL_US_S`'s segment ladder, per policy: the index level, the fixed account, the month's sweep into a new segment, the live segments' total and count, the credit of the segment maturing in the month and the return behind it, and the loan collateral; the index level is on the valuation clock (*Two clocks*, below) |
| `result_pols()` | The counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then the month's deaths and lapses, death first, and its maturities, which are always zero; then `IUL_US_S`'s two monthly decrement rates, written 0 outside cover |

`IUL_US_S`'s four self-checks, `check_av_components()`, `check_av_roll_fwd()`,
`check_seg_ladder()` and `check_margin()`, run over the same frame and hold on every
committed point, `IUL_US_S`'s point 5 and the three rows restated from it included, where
`IUL_US_S`'s own `check_margin()` fails from policy month 383 (*Departures*, below).

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read, so the run holds the cells of one point at
a time. Deleting it, `del model.Projection[idx]`, is not enough: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees, so the runner collects after
each release. It freezes everything alive (`gc.freeze()`) once the model and its table are
read, and again once it has asked every point for its frame, so that each collection scans
only what the block has made since. It prints where each point stands at the valuation
date — its months in force, policy year, attained age and count; its account value and
the three parts of it, the fixed account, the live segments and the loan collateral; its
loan, face in force, premiums paid, no-lapse accumulator and MEC status — then the block's
first twelve rows and the block summed into projection years, `pols_if` the count
entering each. It keeps the block's sum as it goes, compensated as pandas sums a
`groupby`, so that wherever every frame is finite the block is, bit for bit, the frames
concatenated and summed by `t`, as below. The committed block opens with 7.67 policies,
44,514.67 of premiums and a net cash flow of 41,034.86. A label not in the table, or not a
number, stops the runner with the table's labels and no traceback.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of the projection, the first month at attained age 121.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' own month index from issue, and the
  contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1` and `age(t) = age_at_entry() + duration(t)`, as in
  `IUL_US_S`. `BasicTerm_SE` reaches the same numbers by adding one a month, a recursion
  as long as the frame; the closed form needs no such chain of calls.

`IUL_US_S` already counts its months from the start of its own projection, and opens a
point whose `duration_mth` is above 0 there, from its account value and its loan. But it
ships no such point, and its entry loses what a policy's past has left it: it puts the
whole account value less the loan in the fixed account, opens the loan collateral at the
loan, the face at issue and both premium accumulators at 0, and has no index segment
before its first month. Re-opened that way at its month 60, `IUL_US_S`'s point 4 closes
its month 71, eleven months on, with 50,921.66 of account value where its own projection
holds 53,730.24, about 5% short, and reads its no-lapse guarantee as failed where its own
projection holds it in effect. What the valuation clock adds is that `t = 0` is one instant
for every point, that a point may be issued after it, and that a point in force brings in
its whole state, its live index segments among it (*The opening state*, below).

Point 7 is `IUL_US_S`'s point 4, the monthly payer, restated at its month 65. At `t = 0`
it is five months into policy year 6, at attained age 50, with all twelve segments live,
and its frame has 847 rows, `t = 0 … 846`. Its anniversaries fall at `t = 7, 19, …`, where
the attained age steps to 51 and the premium persistency from 0.98⁵ to 0.98⁶. Point 12 is
`IUL_US_S`'s point 4 to be issued 25 months after the valuation date:
`duration_mth(0) = −25`, it is on the books from `t_entry() = 25`, rows 0 to 24 are zeros,
its first monthly premium, $833.33, falls at `t = 25`, and its frame has 937 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the anniversary premium, `duration_mth(t) % 12 == 0`, and the premium persistency, 0.98 to the policy years completed; withdrawals from policy year 2 and loans at each anniversary from policy year 21; a segment's creation, in the month of the sweep that makes it, and its maturity twelve policy months later, before which the trailing credited rate is the fixed-account rate; the surrender charge by policy month and the lapse spike in the policy year after it; the COI scale, the base lapse rate, the per-unit charge and the collateral's credited rate by policy year; the mortality rate and the corridor factor at the attained age; the no-lapse period, its test against the minimum premium counted from issue, and the shock at its expiry; the GPT limit and the 7-pay test's seven years; premiums, withdrawals and charges ceasing at `charges_cease_age`, and the projection ending at `maturity_age`, both 121 | the index path, `index_level(t)`, from `index_level_init` at the valuation date; the cap in force, `index_cap_at(t)`, and the fixed-account rate, `fixed_rate_ann(t)`, each level as shipped; expense inflation, `inflation_factor(t) = (1 + inflation_rate)^(t // 12)`, 0 as shipped |

**The index path.** `IUL_US_S` grows the index at its level return along its own months,
`index_level(t) = index_level_init × (1 + index_return_ann)^(duration_mth(t) / 12)`: a
path of each point's own from its issue, which is one path for every point it ships, all
issued at its `t = 0`. Here the path runs on the valuation clock,
`index_level_init × (1 + index_return_ann)^(t / 12)`, one path for every point of a block,
as a historical or simulated path would be: `index_level_init`, 4,500.00 as shipped, is its
level at the valuation date. A segment's credit is a ratio of two levels, its level at
maturity over its level at its creation, so the path's clock moves no credit as long as
both levels are on the same path. A segment created in the frame, at month `t − 12`,
starts from `index_level(t − 12)`; one created before the valuation date carries its start
level in its ladder row, on this model's path: `IUL_US_S`'s level at the segment's
creation, times `index_level_init` over `IUL_US_S`'s level at the valuation date. On
point 7 the segment maturing at `t = 0` started from 4,229.32, where `IUL_US_S`'s started
from 5,918.41 and matures at 6,297.18: its return is 6.40% either way. What moves is the
level itself: on a point in force `d` months, `index_level(t)` is `IUL_US_S`'s level at its
month `t + d` divided by `(1 + index_return_ann)^(d / 12)`, 1.399374 on point 7, and so is
the `index_level` column of `result_seg()`. Each credit agrees with `IUL_US_S`'s on a
restated row to the rounding of a ratio of two other levels, a few parts in 10¹⁵, and
every other value of the four reports to within 4e-12 relative on the committed rows, but
the credit of a segment drawn to a rounding about zero (*The segment ladder*, below).
`index_level` is the single point of substitution: override it with a path keyed by the
months from the valuation date, and every segment created in the frame follows it, while
one created before the valuation date reads its start level from its ladder row, which
must then be on the same path.

The cap in force and the fixed-account rate are economic inputs too, read at `t`: a
re-declared rate applies to every point from the month it is declared, and a re-declared
cap to every segment created from that month on, since a segment keeps the cap declared at
its creation (`seg_index_cap(t)`, the ladder's `seg_index_cap_init` for a segment created
before the valuation date). As shipped both are level, 10.00% and 4.50%, so their clock
shows in no number. Expense inflation keeps `IUL_US_S`'s step by year and moves it onto
`t`, so that the maintenance expense would be in valuation-date dollars, for every point
alike; it ships at 0, as in `IUL_US_S`, and moves no number either. Switched on, a point in
force bears `IUL_US_S`'s maintenance expense times
`(1 + inflation_rate)^(t // 12 − (y − 1))`, `y` its policy year in the month, both models
stepping on their own anniversaries. Acquisition, $150 a policy in the issue month, is
charged per policy issued and not inflated, as in `basiclife/BasicTerm_SE`: `IUL_US_S`
charges it on the policies in force in the issue month, which are the policies issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in range(len(model.Data.point_id()))]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`IUL_US_S` computes, whatever the point's count. On `IUL_US_S`'s five points, all new
business, every cash flow and every count agrees, and so does every other cell the two
models share, at every argument `IUL_US_S`'s own sweep evaluates, bit for bit, but four
whose meaning changed: `pols_if_init()`, now the count already in force at the valuation
date, 0 for new business; `model_point()`, a row of another table; `result_pols()`, which
gains `pols_new_biz`; and `check_margin()`, whose identity this model states with the debt
a surrender recovers (*Departures*, below), and which holds on point 5, where
`IUL_US_S`'s fails.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `IUL_US_S`'s columns,
`pols_if_init` renamed `policy_count`, and ten of its columns are the in-force interface:
`basiclife/BasicTerm_SE`'s two, and eight that open an in-force policy's state, two of
them `IUL_US_S`'s own. The live index segments are a companion table,
`inforce_segments_sec.csv`, one row a segment (below). Every amount is per policy.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, in any month of its policy year, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `av_pp_init` | dollars, of either sign | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | the account value: the fixed account, the live segments and the loan collateral |
| `loan_bal_init` | dollars, 0 or more | the start of month 0 | the policy loan outstanding, the interest accrued to then included |
| `fa_pp_init` | dollars, of either sign | the start of month 0 | the fixed (holding) account, which an exhausted policy runs below 0 |
| `lca_pp_init` | dollars, 0 or more, above 0 exactly where the loan is | the start of month 0 | the loan collateral account, part of the account value, as the debt is not |
| `sum_assured_init` | dollars of face, 0 to `sum_assured` | the start of month 0: after policy month `duration_mth − 1`'s withdrawal cut | the face in force, after every Option A withdrawal cut to date |
| `cum_prem_init` | dollars, of either sign | the start of month 0 | the gross premiums paid from issue to policy month `duration_mth − 1`, less every withdrawal, which the GPT test, the 7-pay test and the TARGET premium cap read |
| `cum_prem_net_init` | dollars, of either sign, at most `cum_prem_init` | the start of month 0 | the same less every loan drawn: the no-lapse guarantee's accumulator |
| `is_mec_init` | an int code: 0, not a MEC; 1, a MEC | the start of month 0: the latch after policy month `duration_mth − 1`'s 7-pay test | whether the policy has failed the 7-pay test, and so is a modified endowment contract for good |

The eight state columns are 0 on a point issued at or after the valuation date: it is
issued at the face `sum_assured`, with no account value, no loan, nothing paid and no MEC
status, and with no segment. `av_pp_init` and `loan_bal_init` are `IUL_US_S`'s own columns:
they already measure the account value and the loan entering `IUL_US_S`'s first month, so
they keep their names. Each new column is named for the cell it opens, with `_init` added:
`fa_pp_init` for `fa_pp_at`, `lca_pp_init` for `lca_pp_at`, `sum_assured_init` for
`sum_assured_at`, `cum_prem_init` for `cum_prem_pp`, as in `UL_US_SEC`,
`cum_prem_net_init` for `cum_prem_net_pp` and `is_mec_init` for `is_mec`. No quantity of
the product is read at the last anniversary, so none needs a column at a second instant:
at a mid-year valuation the year's anniversary premium and loan draw are already inside the
two accumulators and the loan.

**The segment ladder.** `inforce_segments_sec.csv` holds, for each point in force, one row
for each of its last `min(12, duration_mth)` policy months, a month whose sweep made a
segment of nothing, or whose segment has since been drawn to nothing, included:

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `point_id` | a label, a point of the table | — | the point the segment belongs to; nothing else in the file names one |
| `slot` | whole months, 1 to 12 | the valuation date | the months since the segment's creation: slot `k` was created in policy month `duration_mth − k`, and slot 12 matures at `t = 0` |
| `seg_bal_pp_init` | dollars, `−1e-8` or more | the start of month 0 | the segment's balance |
| `seg_ded_cum_pp_init` | dollars, `−1e-8` or more | the start of month 0 | the monthly deductions charged to it since its creation |
| `seg_wd_cum_pp_init` | dollars, `−1e-8` or more | the start of month 0 | the withdrawals and loan transfers drawn from it since its creation |
| `seg_index_start_init` | index points, above 0 | the segment's creation | the index level it started from, on this model's path, whose level at the valuation date is `index_level_init` |
| `seg_index_cap_init` | a rate, 0 or more | the segment's creation | the cap declared then, at which its credit at maturity is capped |

A point not yet in force holds no row. A segment's balance, deductions and draws are its
credit base, and its creation balance takes no column: nothing may enter or leave a
segment but a deduction, a withdrawal or a loan transfer, since segments earn no interim
interest, so it is the three summed, the closure `IUL_US_S`'s own ladder check asserts
(*The segment ladder*, below). The ladder is long, a row a segment, rather than sixty
columns of the model point table, and it is read by a `Data` reader of its own,
`inforce_segments()`, which no reader of `IUL_US_S`'s could serve.

| `IUL_US_S` | `IUL_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_mth` (0 on every shipped point, at the first projected month) | `duration_mth` | The same column, now at the valuation date, and negative for a policy to be issued after it |
| `av_pp_init`, `loan_bal_init` | the same | `IUL_US_S` already opens an in-force point from them |
| — | `fa_pp_init` | `IUL_US_S` opens the fixed account at the account value less the loan |
| — | `lca_pp_init` | `IUL_US_S` opens the loan collateral at the loan |
| — | `sum_assured_init` | `IUL_US_S` opens every point at the face at issue, `sum_assured` |
| — | `cum_prem_init`, `cum_prem_net_init` | `IUL_US_S` opens both accumulators at 0 at its `t = 0` |
| — | `is_mec_init` | `IUL_US_S`'s flag is the 7-pay test of the month alone, and does not latch |
| — | `inforce_segments_sec.csv` | No segment of `IUL_US_S`'s can predate its `t = 0` |

On the twins the six new columns take what `IUL_US_S` itself assumes on new business, 0,
and `IUL_US_S`'s two are as its table has them, 0 on every shipped point, so each twin
opens as its S row does, and holds no ladder row.

The columns carried over are read as `IUL_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the plans for premiums, withdrawals and loans
and the allocation excepted, which hold over the frame:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class` | codes, as in `IUL_US_S`'s table | issue |
| `sum_assured` | dollars of face | issue: the face a policy is issued at, and the surrender charge's base, whatever withdrawals cut the face to |
| `db_option` | `A` or `B` | the option in force over the frame |
| `qual_test` | `GPT`, the only test modelled | issue |
| `premium_type` | `LEVEL`, `SINGLE` or `TARGET` | the pattern over the frame; a single premium falls in the issue month alone |
| `premium_mode` | `ANNUAL` or `MONTHLY` | the mode over the frame; an annual premium falls on the policy anniversary |
| `premium_pp_ann` | dollars a year, the planned premium, or the single premium on `SINGLE` | the plan over the frame, before the premium persistency |
| `load_prem_rate` | a fraction of each premium | the current load over the frame |
| `index_alloc_rate` | a fraction of the fixed account | the share each month's sweep moves into a new segment |
| `wd_pp`, `wd_first_year` | dollars a month; a policy year | the withdrawal taken in every month from that policy year on, gross of its $25 fee; 0 on every shipped point but 5 |
| `loan_new_pp_ann`, `loan_first_year` | dollars a year; a policy year | the standard loan drawn at each anniversary from that policy year on; 0 on every shipped point but 5 |
| `has_surr_charge`, `surr_charge_id` | a flag and a schedule ID, a row of `surr_charge_table.csv` | issue |
| `mnlp_rate` | dollars a year per $1,000 of face | issue: the minimum no-lapse premium rate |
| `gsp`, `glp`, `seven_pay_prem` | dollars, the compliance inputs | issue |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once, by
twenty rules in turn. The first that fails raises `ValueError`, naming the missing column
or every point that fails it:

- the in-force columns are present, and so is every column of `IUL_US_S`'s own that the
  projection reads as a number or a flag: `age_at_entry`, `wd_first_year`,
  `loan_first_year`, `sum_assured`, `premium_pp_ann`, `wd_pp`, `loan_new_pp_ann`,
  `mnlp_rate`, `gsp`, `glp`, `seven_pay_prem`, `load_prem_rate`, `index_alloc_rate` and
  `has_surr_charge`;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months, and −120 or more: "model_point_table_sec.csv:
  duration_mth must be -120 or more, a policy issued at most 120 months after the
  valuation date; it is not at point_id [12]". Future new business is written over a
  horizon, `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer
  than the projection from issue plus ten years: 1,572 months at issue age 0, the youngest
  the product issues, and 1,032 at 45, the only issue age the shipped COI scale carries.
  Set to 0, the Reference refuses future new business altogether, and a negative horizon
  is itself refused;
- `age_at_entry` is a whole number of years, 0 or more, and `wd_first_year` and
  `loan_first_year` each a whole number of policy years, 1 or more: `IUL_US_S` takes the
  `int()` of each, so a fraction would move an age or a first year without a word;
- `sum_assured`, the face at issue, is a number above 0, and `premium_pp_ann`, `wd_pp`,
  `loan_new_pp_ann`, `mnlp_rate`, `gsp`, `glp` and `seven_pay_prem` are each a number, zero
  or more: the guideline limit's `max` and the single premium's `min` read `gsp` and
  `glp`, and would lose a blank one;
- `load_prem_rate` and `index_alloc_rate`, the share of each premium the load takes and
  the share of the fixed account each month's sweep moves into a segment, are numbers from
  0 to 1;
- `has_surr_charge` is `True` or `False`, as pandas reads those words, in any case. A
  blank, a number or any other text is refused: one such value turns the whole column into
  text, where `"False"` is a true string, so that every point would read as carrying a
  surrender charge;
- `av_pp_init` and `fa_pp_init` are each a number, of either sign (*The opening state*,
  below); `lca_pp_init`, `loan_bal_init` and `sum_assured_init` each a number, zero or
  more, a face of 0 in force among them; and `cum_prem_init` and `cum_prem_net_init` each a
  number, of either sign: each is a tax or guarantee measure, not a balance, and
  withdrawals and loans can exceed the premiums paid;
- `is_mec_init` is 0 or 1, an int code; written as 1.0 it reads as `True`;
- a policy not yet in force, `duration_mth` 0 or less, has an opening state of zeros:
  "model_point_table_sec.csv: cum_prem_init must be 0 on a policy not yet in force,
  duration_mth 0 or less; it is not at point_id [12]";
- `sum_assured_init` is at most `sum_assured` on a policy in force, since face increases
  are not modelled. A face below it is accepted, whether withdrawals cut it or an elective
  decrease the model does not implement, and it is projected from the value given;
- `lca_pp_init` is above 0 exactly where `loan_bal_init` is: a standard loan moves value
  into the collateral account on the day it is taken, and the model takes no repayment, so
  the two are held together from the loan's first day, each at its own rate;
- `cum_prem_net_init` is at most `cum_prem_init`, to a cent and a half, half a cent for
  each of the two and half a cent more, since loans only lower it;
- `is_mec_init` is 1 wherever the 7-pay test has already failed in the month before the
  valuation date: `cum_prem_init` above `seven_pay_prem` times the policy years to then,
  in the first seven. A failure the premiums to date no longer show, after withdrawals, or
  one on a policy valued after its seventh year, where the test no longer applies, is the
  column's to record, and either value is accepted.

`Data.inforce_segments()` checks the ladder as it reads it, by nine rules in turn, each
naming the lines or the points it fails on:

- the seven columns are present;
- `point_id` and `slot` are each a whole number, read by value, below `2**53` in size;
- each `point_id` is a point of the table: "inforce_segments_sec.csv: point_id [99] on
  line [68] is no point of model_point_table_sec.csv";
- no `point_id` and `slot` appear together twice;
- `slot` is from 1 to its point's `duration_mth`: no segment predates issue, and a point
  not yet in force holds none;
- each balance, deductions and draws are a number, `−1e-8` or more: a draw or a deduction
  that took a segment's whole balance can leave a rounding about zero of either sign,
  which `IUL_US_S` closes on (*The segment ladder*, below) and an extract carried to the
  cent writes as 0; `check_seg_ladder()` holds every live balance to the same `−1e-8`,
  `IUL_US_S`'s tolerance, so a balance `Data` admits is one the check passes;
- each start level is a number above 0, the level the segment's return divides by;
- each cap is a number, zero or more: the credited rate's `min` reads the cap first, and
  would read a blank cap as a credit at the floor, without a word;
- each point's `av_pp_init` is its `fa_pp_init` plus its `lca_pp_init` plus the balances
  of its segments, to half a cent an amount and half a cent more:
  "model_point_table_sec.csv:
  av_pp_init must be fa_pp_init plus lca_pp_init plus the point's segments in
  inforce_segments_sec.csv, to half a cent an amount and half a cent more; it is not at
  point_id [7]". `check_av_components()` holds that identity in every month, and the
  opening state is the close of the month before. The projection opens the account value
  from its parts, the fixed account, the collateral and the ladder's balances, summed slot
  by slot as `seg_bal_active_pp()` sums, not from this column, so an extract carried to
  the cent, whose rounded parts need not sum to its rounded account value, opens one
  account, and the check holds on it, as it does on every committed point carried to the
  cent. The cent slack also covers an exhausted account: at its worst, on S point 5's
  month 906, the account value is −9.81e9 and its parts differ from it by 3.8e-6.

Six kinds of point read, but `proj_len()` refuses each, naming the point, because each is
a rule of the product, read from `Projection`'s References, not the table's. It checks them
in this order:

- a point to be issued at or past attained age 121, `maturity_age`, which would never be in
  cover: "point_id 12: age_at_entry 121 is at or past maturity_age, 121: a policy issued
  there would never be in cover". The age is checked first, so that such a point is
  refused by its age whenever it is to be issued: one to be issued later would otherwise
  have a frame of months, every one of them before its issue. A point to be issued at
  attained age 120 is a policy, with a year of cover;
- a point at or past the end of the projection at the valuation date,
  `duration_mth ≥ 12 × (121 − age_at_entry)`: "point_id 11: duration_mth 912 is at or past
  the end of the projection, policy month 912, attained age 121";
- a point whose planned withdrawal is above 0 and below the withdrawal fee,
  `0 < wd_pp < wd_fee`: "point_id 5: wd_pp 24.99 is above 0 and below wd_fee, 25.0: a
  withdrawal pays its fee out of itself, so it must be at least the fee". Such a withdrawal
  would debit the account less than the fee the insurer books and pay the policyholder
  nothing: `IUL_US_S` projects it, and its own account value roll-forward and margin
  identity fail on it, as they do on its point 5 withdrawing $20 a month;
- a point in force whose ladder does not hold exactly one row for each of its last
  `min(seg_term_mth, duration_mth)` months, slots 1 to that: "point_id 6:
  inforce_segments_sec.csv holds 11 segments, its last in slot 12, where a policy in force
  60 months holds one a month for its last 12, slots 1 to 12". The count is
  `seg_term_mth`'s, a Reference of `Projection`, which `Data` does not read. `Data`'s slot
  rule accepts twelve rows on the wrong slots, 2 to 13 at month 60, and so this rule
  refuses them, naming the last slot. Each of the five readers of the ladder,
  `seg_bal_pp_init()` to `seg_index_cap_init()`, asks `proj_len()` before it reads a row,
  so that a ladder missing a slot is refused by name, never read as pandas' `KeyError`;
- a point issued below `issue_age_min`, 0, or above `issue_age_max`, 85, the issue ages
  [`product-spec.md`](product-spec.md) admits: "point_id 4: issue age 86 is above
  issue_age_max, 85". `IUL_US_S` projects any age its tables serve, but the compiled
  model's caches are sized from the youngest issue age (*The compiled model*, below), so a
  younger point, whose frame and policy years run longer, would read past them. `Data`
  refuses a negative age first, so at the shipped 0 the lower rule binds only once the
  Reference is raised. The two rules come after the four above, which running in force
  set, so that every message those gave a point they still give.

So a loop over the block meets such a row only when it reaches it, after projecting the
points before it. `run_sec.py --block` asks every point for its frame before it projects
any, and stops before it prints anything.

The assumption tables are checked too, each once, in the `Data` cell its reader in
`Projection` takes its extent or its count from. The tables read at an attained age or a
policy year take their extents from `corridor_age_first()` and `corridor_age_last()`,
`mort_age_first()` and `mort_age_last()`, `lapse_last_year()` and `coi_rate_last_years()`,
the last policy year of each scale of `coi_rates.csv`, one for each sex, class and issue
age, beyond which each reads its nearest row. The key column is read by value, so a year
written `5.0` is 5, and a key that is blank, text or not a whole number is refused, naming
the file, the column and the lines it is on. So are keys that do not run one row an age or a
year, without a gap or a repeat, policy years from 1, the message naming each key that
repeats, with its lines, and each that is missing. So is a blank sex or class in the COI
scale, and a value that is blank, text or infinite. A lapse or mortality rate is a
probability, held to 0 to 1, since past 1 the monthly rate `1 − (1 − q)^(1/12)` has no real
value. A class factor, a guaranteed COI rate and a surrender charge are held to 0 or more,
since below it each projects, with every check passing, negative deaths, a credit for the
insurance or a surrender charge that rises once its schedule has run off. A COI rate is a
charge per $1,000 of net amount at risk a month, not a decrement: the current rate passes 1
from attained age 69, as it should, and nothing caps it. A corridor factor is held to 0 or
more too. `IUL_US_S`'s death benefit is the `max` of the face and the corridor factor times
the account value, with no floor on the account value, so on an exhausted account a factor
below 0 would pay far above the face: at −0.5 from attained age 95, `IUL_US_S`'s point 5
pays 58,155,653.50 on a face of 92,200 at its month 800, every account check passing.
`class_count()` and `surr_charge_count()` check the class factors and the surrender-charge
schedules, for the per-point joins that read them, the same way, and `surr_charge_count()`
also refuses a run-off that is not a whole number of years, 1 or more, which the projection
divides the charge by, where `IUL_US_S` divides by zero at 0. A class, or on a point with a
charge a schedule, the table has no row for is refused when `Data` joins it to the points,
naming every such point, and a COI cell when the point's first COI rate is read, naming it,
where `IUL_US_S` raises pandas' `KeyError`.

Each reader asks for its extent or its count before it reads a value, so a projection meets
the checks first. `IUL_US_S` takes each extent from the key column as pandas reads it, where
a blank key is a missing value the extent skips: the table is cut short, and every later
year or age reads the last good row, without a word. A blank value is a missing value to it
too, which shows in its flows or is lost in a `min` or a `max`: a blank lapse rate reaches
the lapse cap's `min`, whose bound is written first, and is read as the cap, 1.0, so that
every policy lapses; a blank corridor factor reads as no corridor at all, and a blank
surrender charge as none. Here the cap on the mortality rate, `min(q, 1.0)`, keeps a blank
base rate or class factor missing, as `IUL_US_S`'s own does, and each of them is refused
before any rate is read.

## The model points

No row of `model_point_table_sec.csv` or of `inforce_segments_sec.csv` is typed by hand.
Every one is generated from `IUL_US_S` and its table by `tests/sec_support.py`, from the
`IUL_US_SEC` entry in its `SEC_SPECS`, and the tests regenerate both files and compare, so
an edit to an `IUL_US_S` row reaches them or fails the suite. In the source repository,
`python tools/gen_sec_points.py IUL_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–5 | twin | S points 1–5 | issued at `t = 0`: `IUL_US_S`'s baseline cell, paying $10,000 a year; the same on Option B; the same with no indexed allocation, the control run the ladder is read against; the same paying monthly, the one point that builds the full ladder of twelve segments; and an underfunded policy paying $6,000 a year, withdrawing $200 a month from policy year 2 and borrowing $6,000 a year from policy year 21 |
| 6 | derived | S point 1 at S month 60 | on its fifth anniversary, at attained age 50, with 48,039.60 of premiums paid: its 43,877.35 of account value is all in the segment created at its fourth anniversary, which matures at `t = 0` with a credit of 2,808.15 as the year's premium of 9,039.21 falls |
| 7 | derived | S point 4 at S month 65 | five months into policy year 6, paying monthly, all twelve segments live, 47,950.61 in all, one maturing each month from `t = 0`; its surrender charge and its no-lapse guarantee in force |
| 8 | derived | S point 5 at S month 6 | six months into its first year: its ladder six months deep, the one segment swept at issue holding 4,998.62 and maturing at `t = 6`; its no-lapse guarantee in effect on its one premium of 6,000.00, failing for good at `t = 43`, policy month 49 |
| 9 | derived | S point 5 at S month 384 | in policy year 33, at attained age 77: its fixed account −112.50 entering the month, its segments empty, and its loan of 87,706.74 above its account value of 87,594.24, so above its cash value; its face cut to 175,600 by its withdrawals |
| 10 | derived | S point 5 at S month 605 | in policy year 51, at attained age 95: its account value −241.18, the fixed account −303,975.15 against a collateral of 303,733.97; its face at 131,400 |
| 11 | derived | S point 1 at S month 888 | two years before the end of its projection, at attained age 119, where the mortality rate is 1.0, with 1.042e-10 of a policy: every survivor dies at `t = 0`, and the frame's 23 later rows of cash flows are zeros |
| 12 | future | S point 4, 25 months on | to be issued at `t = 25` |

A derived row's `policy_count` is the count `IUL_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `IUL_US_S` carries into it, each column read
as `IUL_US_S`'s own formulas read it: the account value, the fixed account and the
collateral as their `BEF_PREM` timings at `d`; the loan, the face and the two
accumulators as the close of month `d − 1`, `loan_bal_pp(d − 1)`, `sum_assured_at(d − 1)`,
`cum_prem_pp(d − 1)` and `cum_prem_net_pp(d − 1)`; and the MEC latch as whether
`IUL_US_S`'s 7-pay test failed in any month before `d`, since its flag does not latch. Its
ladder row in slot `k` is the segment `IUL_US_S` created at its month `d − k`: its balance,
deductions and draws at the close of month `d − 1`, `seg_bal_pp(d − 1, d − k)` and the two
running totals beside it; the cap `index_cap_at(d − k)`; and the start level
`index_level(d − k)` rebased onto this model's path, times `index_level_init` over
`index_level(d)`. So the row continues the S projection from there, per policy: point 9
opens with 0.175064 policies, and point 11 with 1.042e-10. A derived row's `policy_id` is
the S row's with the month appended, `IUL-000005-M384`, and a future row's carries the
months to issue, `IUL-000004-F25`. Row `t` of a generated point is month `t + source_mth`
of its S point. All twelve are on the notes' anchor configuration, M45 / NT / $250,000 /
GPT, because the illustrative COI scale covers that cell alone, so a point on any other
issue age, sex or class needs `coi_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has the
three timings that `IUL_US_S` already names:

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements;
- `BEF_MAT`, the count before any maturity, `IUL_US_S`'s meaning: the `BEF_DECR`
  count, since nothing matures in the frame and no event of the month separates the two.

Any other timing raises. `IUL_US_S`'s cell of the name returns `pols_if(t)` for every
timing, and nothing calls it. `BEF_NB` is the one timing this model gives a meaning of
its own, `basiclife/BasicTerm_SE`'s, and the two models differ in it alone, in the issue
month: there `IUL_US_S` counts the issued policies, and this model counts them as new
business, not yet in. As in `UL_US_SEC`, `VUL_US_SEC` and `ULSG_US_SEC`,
`basiclife/BasicTerm_SE`'s `BEF_MAT`, the count at the start of the month before its new
business, is not adopted: the name keeps its S model's meaning.

The month's decrements are `IUL_US_S`'s, in its order, both at the end of the month:
deaths, then surrenders out of the survivors. No policy is terminated for insufficiency, as
in `IUL_US_S`, whose notes leave the account value in grace and the cash flow of a cure
undetermined: a policy whose account value is exhausted goes on being charged (*The opening
state*, below).

Every chain of calls from month `t` back to `t_entry()` is one cell a month. `BEF_NB`
forms the survivors of month `t − 1` itself, as its own value at `t − 1` plus that month's
new business, less that month's deaths and lapses, death applied first, as `pols_death`
and `pols_lapse` take them. Each account's opening balance forms the previous month's close
the same way, the same operations in the same order as the closing cell `IUL_US_S` calls
for: `av_pp_at(t, BEF_PREM)` from its own value at `t − 1` and month `t − 1`'s net
premium, index credit, withdrawal, deduction and interest, where `IUL_US_S`'s account
value ran through five cells a month; `fa_pp_at(t, BEF_PREM)` from its own and month
`t − 1`'s net premium, matured segment, draw, deduction, sweep and interest, where
`IUL_US_S`'s fixed account ran through six; and `lca_pp_at(t, BEF_PREM)` from its own,
month `t − 1`'s new loan and the collateral's interest, where `IUL_US_S`'s collateral ran
through two. The loan, the face, the two premium accumulators, the MEC latch, and each
segment's balance and its two running totals call themselves at `t − 1`.

On a model just read, a cold `net_cf` in the last month of point 1's 912-month frame runs
930 cells deep, against 3,974 for `IUL_US_S`'s point 1: 19 cells above the chain back to
`t_entry()`. The other committed points run 17 to 19 above theirs, point 12 19 above its
chain of 911 months from its issue. Each chain's head called alone, on a read of its own
with every chain cold, on the twin of point 4, which pays monthly and keeps twelve segments
live, runs at most 14 cells above its chain: the account value's 8, the fixed account's 12,
the collateral's 3, the loan's 4, the face's 5, each accumulator's 4, the latch's 5 and the
count's 14. At the longest cover the contract allows, issue age 0 and 1,452 months, a cold
`net_cf` in the last month runs 1,470 deep, 19 above its chain, both issued at the valuation
date and issued 120 months after it, since every chain stops at the issue month: compiled
with gcc, it runs on 352 KiB of C stack and not on 320 (*The compiled model*, below). Each
report evaluates its columns in ascending `t`, and on a model just read the committed
points' four reports and four checks run that way under a recursion limit of 18 to 28, and
`IUL_US_S`'s points 1 to 4 under 24 to 26. Two rows are the exception, twin 5 and point 8,
the rows of `IUL_US_S`'s point 5 on the books before its no-lapse guarantee expires: each
needs 217. Their guarantee fails for good at policy month 49, from which the count reads the
account value in no month until the expiry's shock, at policy month 240, reads the cash
value and runs the account value's chain cold back to month 49, 192 months, one cell a
month. `IUL_US_S`'s point 5, whose chain is five cells a month, does not run that way under
400.

The model exported by modelx 0.33 runs as plain Python, each cell a function call, and
needs more: Python's recursion limit, set after the import, must be at least 1,886 for a
cold `net_cf` in the last month on twin 1 and on point 12, issued 25 months on, 1,756 on
point 7 and 1,114 on point 9, and 2,966 at the longest cover, issue age 0, issued now or
120 months on; the ascending sweep of the four reports and four checks needs 64 on twin 1,
on point 7 and at the longest cover, 60 on point 9 and 438 on twin 5, the expiry's read
after a lapsed guarantee. So the export, and the sample and the runner, need a limit above
2,966, and `sample_sec.py` sets 12,000 (*The compiled model*, below).

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `IUL_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB) = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, the last month included, and `pols_if(t + 1)` adds
`pols_new_biz(t + 1)` to the count on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × (maturity_age − age_at_entry)` is `IUL_US_S`'s frame from issue, the
first month at attained age 121. Outside it, before issue and from `t = proj_len()` on,
every count, balance, segment, premium, withdrawal, loan draw, charge, credit, decrement
rate, decrement, claim and cash flow is zero and every flag false, `seg_count` the int 0;
only the two clocks, the inputs read on the valuation clock, the level policy fee and the
neutral 1.0 of the two lapse multipliers hold values there, and the month after the frame
holds two exceptions more, below. No count evaluates a decrement rate there, and no table
is read at a policy year or an attained age the policy does not have: `prem_persistency`,
`premium_pp`, `wd_pp`, `loan_new_pp`, `face_reduction_pp`, `sum_assured_at`,
`corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `expense_unit_mth_at`,
`maint_fee_pp`, `loan_credit_rate_ann`, `surr_charge_rate`, the segment cells, the
opening timings of the three accounts, `loan_bal_pp`, `cum_prem_pp`, `cum_prem_net_pp`,
`cum_mnlp_pp`, `gpt_limit`, `seven_pay_limit`, `cred_rate_ann`, `mort_rate`,
`lapse_rate_base`, `lapse_rate`, `pols_death`, `pols_lapse` and `expenses` are zero, and
`nlg_test_ok`, `nlg_in_effect`, `nlg_expiry_shock`, `is_shortfall`, `gpt_ok` and `is_mec`
false, before any table or rate is read, and every other value is zero through them.
`lapse_rate_sc_mult` and `lapse_rate_dyn_mult` are 1.0 there. The first is 1.0 before it
compares the policy year with the shock year: a point with no surrender charge has the
shock year 0, and before issue the valuation clock reaches policy year 0. Each table read at
a policy year or an attained age has one reader keyed by it, called inside cover only, so
on point 12, whose policy year is −2 at `t = 0`, no reader is asked for a policy year below
1 or an attained age below 45.

**The end of the projection.** The frame ends at `maturity_mth()`, the first month at
attained age 121, the notes' [unverified] maturity inference (spec F5), and not at an event
of the contract, which is described as continuing in force there with no further charges.
Premiums, withdrawals and charges cease at `charges_cease_age`, a Reference of its own, 121
too as shipped; set below `maturity_age`, the projection runs on past the cessation, the
account value earning its interest and the segments their credits with nothing deducted.
Lives can survive the last month, and `IUL_US_S`'s roll-forwards read them:
`check_av_roll_fwd()` and `av_change()` read the account value in force entering month
`t + 1`, which in the last month is `t = proj_len()`. So the two opening values read there,
the count carried in (`pols_if_at(t, BEF_NB)`, and through it `pols_if(t)`) and the
account value carried in (`av_pp_at(t, BEF_PREM)`), are defined for
`0 ≤ duration_mth(t) ≤ maturity_mth()`: in the month after the frame they are the survivors
of the last month and the account value they carry, `IUL_US_S`'s own values there.
Everything else is zero or false there, the expenses included, which would otherwise fall
on the carried count, and nothing reads past it: `av_change()` and the checks' residual
cells, which read `t + 1` or are read beside cells that do, are zero outside cover before
they read it. At the shipped assumptions the survivors at `proj_len()` are exactly 0.0 on
every committed point: the mortality table reaches 1.0 at attained age 119, and on the
anchor class, whose factor is 1.0, at an A/E of 1.0, every life has died by the end of the
first month at that age, as point 11 shows. At an A/E of 0.56, which leaves the rate below
1, they are 3.276e-6 of a policy on the twins of points 1 to 3, 3.414e-6 on point 4's and
3.485e-6 on point 5's, `IUL_US_S`'s own counts there, and every check closes.

**Rates stay rates.** The annual mortality rate is capped at 1.0, as in `IUL_US_S`,
`min(q, 1.0)` with its bound second, so that a missing input stays missing. On no committed
point does the product pass 1, since all are on NT, whose factor is 1.0: the cap binds on
the classes whose factor is above 1, first on Tob at attained age 113, 1.75 × 0.625687, and
on PTob at 115, at an A/E of 1.0. The annual lapse rate keeps `IUL_US_S`'s cap,
`min(lapse_rate_cap, rate)`, its bound written first. The cap is 1.0, inert as shipped:
these notes give none, and on the committed points the rate before it is at most 8%, the
4% of policy year 11 doubled by the surrender charge's expiry. The no-lapse guarantee's
expiry shock, `nlg_shock_lapse`, 25%, is returned before the cap, as in `IUL_US_S`: set
past 1 it is a rate past 1, whose monthly rate has no real value, and the account value's
and the margin's checks then raise through their residuals, as `IUL_US_S`'s
`math.isclose` raises. It falls only on a policy with no net cash value in the year after
its no-lapse period, and no committed point takes it. The dynamic lapse multiplier is 1 in
every month, `comp_rate_ann` being `cred_rate_ann`, so neither its floor of 0.5 nor its
cap of 2.0 binds on a committed point.

## The opening state

`IUL_US_S` opens a point whose `duration_mth` is above 0 from two columns, the account
value and the loan entering its first month, and takes the rest from them or as they stand
at issue: the fixed account as the account value less the loan, the collateral as the
loan, no live segment, the face at issue, both premium accumulators at 0, and a MEC flag
from the month's own 7-pay test alone. A policy valued in any month of its life needs all
eight columns and its ladder, each what `IUL_US_S` carries into that month. The committed
points show what most of them change, each compared with the same row read with the column
as `IUL_US_S` would open it:

- **The ladder and `fa_pp_init`.** Point 7 holds its 47,950.61 in twelve live segments and
  nothing in its fixed account, and one segment matures each month, its credit 233.73 at
  `t = 0` and 286.48 at `t = 11`. Read as `IUL_US_S` would open it, all of it in the fixed
  account and no segment live, it would earn no credit until `t = 12`, when the segment
  its first month's sweep makes of the whole account value matures: it would close month 6
  with 52,091.99 of account value where `IUL_US_S`'s own projection, and this model's,
  hold 53,730.24, and month 11 with 54,965.36 where they hold 58,038.13. Point 6 holds its
  43,877.35 in the segment created at its fourth anniversary, which matures at `t = 0` with
  a credit of 2,808.15; read with it in the fixed account, the credit would be lost and the
  account value would close month 0 at 52,341.01 in place of 55,149.71.
- **`sum_assured_init`.** Point 9 has withdrawn $200 a month for 31 years under Option A,
  each withdrawal cutting the face, which stands at 175,600.00 entering month 0, so its
  death benefit at `t = 0` is 175,400.00, after the month's cut. Read at the face at issue,
  as `IUL_US_S` would open it, the death benefit would be 249,800.00, the net amount at
  risk 159,212.58 in place of 84,874.24 and the cost of insurance 331.71 a policy in place
  of 176.83. The surrender charge is quoted on the face at issue either way, and has run
  off.
- **`cum_prem_net_init`.** Point 8, six months after its issue, has paid one annual
  premium of $6,000.00, which keeps its no-lapse test, premiums less withdrawals and loans
  against the minimum no-lapse premium counted from issue, 3,033.33 through month 0,
  passing: its guarantee is in effect, and with no cash value its lapse rate is 0. Read at
  0, as `IUL_US_S` opens the accumulator, the test would fail at once: the guarantee would
  be off, the lapse rate 6%, and 0.993983 policies would be in force at `t = 1` in place of
  0.999121.
- **`loan_bal_init` and `lca_pp_init`.** On the committed points the two are equal:
  `IUL_US_S`'s point 5 borrows only from policy year 21, when the collateral's credited
  rate has stepped up to the loan's 3.00%, so that points 9 and 10 carry 87,706.74 and
  303,733.97 of each. They part on a loan taken in the first ten policy years, when the
  collateral is credited 2.00% against the loan's 3.00%: on a variant of `IUL_US_S`'s
  point 5 borrowing from policy year 6, restated at its month 83, the collateral is
  12,342.02 where the loan is 12,514.54, two balances that have accrued apart since the
  first loan, and that `IUL_US_S`'s entry would merge into one.

The other two columns show nothing on the committed points: none fails the 7-pay test,
and none pays a TARGET premium. Each shows on a variant of an S point, in a copy of S's
table that is never committed, read with the column as above:

- **`cum_prem_init`.** `IUL_US_S`'s point 1 paying a TARGET premium of $30,000 a year,
  restated on its third anniversary, at its month 36, has paid 88,212.00, which leaves
  6,788.00 of room under the guideline premium limit, its guideline single premium of
  95,000: it collects 6,788.00 at `t = 0` and nothing after. With the column at 0 it would
  collect its whole premium for the year, 28,235.76, at once.
- **`is_mec_init`.** `IUL_US_S`'s point 4 paying $36,000 a year, monthly, fails the 7-pay
  test at its policy month 7. Restated at its month 85, in policy year 8, where the in-year
  test no longer applies, `is_mec(0)` is true from the latch alone; with the column at 0
  it would be false, as `IUL_US_S`'s own flag is there, which turns itself off in policy
  year 8, exactly when the failure becomes permanent.

The in-year test runs before the latch looks back, in the valuation month as in every
other, so a policy that fails the test at `t = 0` is a MEC from then on, whatever
`is_mec_init` says: the same variant restated at its month 7 has paid 21,000.00, inside the
first year's limit of 21,000.00, so its `is_mec_init` is 0, and month 0's premium of
3,000.00 takes it to 24,000.00: `is_mec(0)` is true. With `cum_prem_init` at 0 it would be
false.

**An exhausted account, in force.** `IUL_US_S` lapses no policy for insufficiency: a
policy whose account value is exhausted goes on being charged, its fixed account carrying
every deduction and draw the segments cannot, and the cost of insurance then compounds,
since the net amount at risk rises as the account value falls. Its point 5's fixed account
closes below 0 from policy month 383 and its account value from month 604, by design, and
its own tests pin both months; by the end of its frame the account value is about
−1.3 × 10¹⁰. So this model accepts such an opening state: `fa_pp_init` and `av_pp_init`
may be of either sign, held to each other by the account value's identity with the
collateral and the segments. Points 9 and 10 are those states, at 384 and 605, and each
continues `IUL_US_S`'s projection from there, its four checks holding. A face of 0 in force
is accepted too: Option A withdrawals cut the face dollar for dollar, never below 0, while
the policy stays in force. This is where the model departs from `UL_US_SEC` and
`ULSG_US_SEC`, which refuse an account value below 0 and ask for a point to be restated no
later than its last month at 0 or more: `IUL_US_S` carries an exhausted account on by
design, on a shipped point, and a row restated past it is a state its projection
continues. The cash flows stay finite and bounded there, the death claim being the
face less the loan, floored at 0, and the surrender value floored at 0; the account value
is not a meaningful number, as `IUL_US_S`'s [implementation notes](model.md) say.

## The segment ladder

A segment is created at every monthiversary by the sweep, and matures twelve policy months
later, so up to twelve are live at once [S4]. `IUL_US_S` keys each segment by the month of
its creation on its own clock, `seg_bal_pp(t, m)`. This model keys a segment in month `t`
by its **slot**, its months since creation, `k = duration_mth(t) − m`, where `m` is the
policy month of its creation, `duration_mth` of the month whose sweep made it: 0 in its
creation month and 11 in the last month it is live. The six cells of a segment in a month,
`seg_share`, `seg_wd_pp`, `seg_ded_pp`, `seg_bal_pp`, `seg_ded_cum_pp` and
`seg_wd_cum_pp`, take `(t, k)`, and each reads its own value of the month before at
`(t − 1, k − 1)`, the same segment a month younger. Keyed by `(t, m)`, a compiled cache
would hold every creation month of the frame in every month, 1,452 of them at the longest
cover, where twelve slots hold the live ones (*The compiled model*, below). A segment's
creation balance, `seg_new_pp(m)`, keeps its creation month, one value a segment, which
`seg_bal_pp` reads in slot 0 and the credit reads at maturity. A parameter that holds a
policy month is named `m`, never `t`, so that what moves with the valuation clock is `t`
alone. The twin comparison maps `IUL_US_S`'s `(t, m)` to `(t, t − m)` on its points, all
issued at its `t = 0`, where the policy month is its month. The ladder's `slot` is the slot
of month 0, `k = duration_mth_init() − m`, which is what an extract of a policy's live
segments knows: slot `k` at the valuation date is the segment born in policy month
`duration_mth_init() − k`, and slot 12 the one maturing at `t = 0`.

Each segment cell opens a segment born before the valuation date from its ladder row, at
`t_entry()`: `seg_bal_pp`, `seg_ded_cum_pp` and `seg_wd_cum_pp` from the slot's balance,
deductions and draws, `seg_share` and the pool, `seg_bal_active_pp`, from its balance, and
`index_credit_pp`, `seg_roll_pp` and the closure's residual, at `t = 0`, from slot 12's.
Its creation balance, `seg_new_pp(m)`, is its row's three amounts summed, so the closure
`check_seg_ladder()` asserts holds by construction on the segment maturing at `t = 0`, and
the credit, under either credit base convention, depends on the three amounts alone. A
segment born in the frame is the sweep of its month, as in `IUL_US_S`.

The start level and the cap of the segment maturing in month `t`, `seg_index_start(t)` and
`seg_index_cap(t)`, are `index_level(t − 12)` and `index_cap_at(t − 12)` for a segment born
in the frame, and its ladder row's `seg_index_start_init` and `seg_index_cap_init` for one
born before the valuation date. `IUL_US_S` credits a segment through its crediting engine,
five cells of float arguments, `index_change`, `index_credit_rate`, `seg_credit_base`,
`index_credit` and `seg_matured_value`. Here the projection computes the same credit in
cells keyed by the month, `seg_return(t)`, the segment's return, `seg_credit_rate(t)`, its
credited rate at the cap declared at its creation, and `index_credit_pp(t)`, the rate times
the credit base under `seg_credit_base_conv`, each in `IUL_US_S`'s order of operations and
of bounds, the cap first and then the floor. The five engine cells are kept as `IUL_US_S`
has them, `None` defaults included, for its worked example and for the comparison with
`IUL_US_S`, and no projection cell calls them. Every month the ladder runs reads a start
level and a cap, a month whose segment holds nothing included: the trailing credited rate,
`cred_rate_ann(t)`, which drives the dynamic lapse multiplier, is the credited rate of the
segment maturing in the month whether or not it holds a balance, from policy month 12 on.
So every one of the last twelve months holds a ladder row, empty or not, and `proj_len()`
refuses a point in force that lacks one.

**Rounding about zero.** A draw or a deduction that takes a segment's whole balance can
leave it a rounding about zero, a balance of the order of 10⁻¹⁶ of either sign, and
`IUL_US_S` closes on such states. `seg_share` reads the pool by `IUL_US_S`'s test,
`pool <= 0`, and `seg_count` counts a segment where its balance is above 0, so that on
such a state the two models branch alike; `Data` accepts a segment's balance, deductions
and draws down to `−1e-8` for the same reason, the tolerance `check_seg_ladder()` holds
each live balance to. The credit of a segment drawn to a
rounding about zero is a rounding itself: point 9's slot 12 holds nothing, and its credit
at `t = 0` is −1.455e-14 a policy, as `IUL_US_S`'s is at its month 384, well inside
`check_seg_ladder()`'s tolerance of `1e-8`. On a row restated earlier, every return is a
ratio of two levels on another path, which differs from `IUL_US_S`'s in its last bits, and
so can such a rounding: on point 8 the same credit, at its `t = 378`, is −2.910e-14.

The pool, `seg_bal_active_pp(t)`, and the total, `seg_bal_tot_pp(t)`, sum the segments in
an explicit loop that compensates as Python's `sum()` of floats does from Python 3.12,
Neumaier's improvement of Kahan's summation, so that each is `IUL_US_S`'s `sum()` bit for
bit there, a pool of 10⁻¹⁶ included. `IUL_US_S` sums a generator, which a rewritten cell
does not hold, so that it compiles; `seg_count` counts in a loop for the same reason. Python
3.11's `sum()` is a plain fold, which can put such a pool on the other side of zero, so the
states `IUL_US_S` closes on a rounding about zero depend on the interpreter it runs on.

## Departures from IUL_US_S

Each formula that opened at `t = 0` now opens at `t_entry()`, from the opening state and the
ladder on a point in force, and each cell that turns `t` into a policy year or an attained
age answers for the months outside cover. Of `IUL_US_S`'s 156 cells in `Projection`, 58 are
unchanged, 32 have a new docstring only, most of them to say what `t` now counts, and 66 are
rewritten. None is removed or renamed, and 42 cells are new, 198 in all. Compiling then
changed how each cell reads its inputs and spells its codes, and no number: it replaced one
cell, `coi_rate_scale`, by a schedule number, `coi_schedule`, and added four more,
`point_id`, `claims_death`, `claims_lapse` and `seg_credit_rate`, 202 in all (*The compiled
model*, below). Of `IUL_US_S`'s cells it changed the signature of one, `claims`, and the
second parameter of the six segment cells, a slot for a creation month. The twin identity
exempts `coi_rate_scale`, with its reason, compares `IUL_US_S`'s `claims(t, None)` with the
total `claims(t)`, and reads a segment cell's `(t, m)` at the slot `(t, t − m)`: a cell of
`IUL_US_S`'s that this model lacked, or took other arguments, would fail it otherwise.
`IUL_US_S`'s Reference `math`, which only its checks' `math.isclose` read, is dropped.
Running in force added none, and every other Reference of `Projection` is `IUL_US_S`'s,
value for value, but two that compiling turned into codes: `basis` and
`seg_credit_base_conv`, which hold `CURRENT` and `REMAINING`, 0, where `IUL_US_S` holds the
text. Compiling replaced `point_id` by `idx` and added the 18 codes and the contract's two
issue ages, `issue_age_min` and `issue_age_max`. Of `Data`'s eight cells, running in force
rewrote `model_point_table` to check the table as it reads it, and added eleven, nineteen in
all: the ladder's reader, `inforce_segments`, and its two summaries, `inforce_segment_count`
and `inforce_segment_last`; the six extents of the four tables read at a policy year or an
attained age, each of which checks its table's keys and values; and `class_count` and
`surr_charge_count`, which check the class factors and the surrender-charge schedules.
`Data` gains two References, `inforce_segments_file` and `future_horizon_mth`, 120, and
`model_point_file` names `model_point_table_sec.csv`. Compiling added 49 cells to `Data`, 68
in all, and its Reference `np`, and widened the checks of the model point table and of the
two age tables. Some departures come from compiling rather than from the clock: `proj_len`'s
two issue-age refusals and the last three rows below. The cap on mortality, `min(q, 1.0)`,
is `IUL_US_S`'s own and no departure, and so are the lapse rate's cap in `IUL_US_S`'s order,
its bound written first, and the shock lapse returned before it.

| Cells | `IUL_US_S` | `IUL_US_SEC` | Why |
|---|---|---|---|
| `proj_len`, `maturity_mth` | `12 × (maturity_age − x) − duration_mth_init()`, the months from the first projected month | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises, in this order, for a point to be issued at or past attained age 121, one at or past the end of the projection, one withdrawing above 0 and below the fee, one in force whose ladder lacks a row of its last `min(12, duration_mth)` months or holds another, and one issued below `issue_age_min`, 0, or above `issue_age_max`, 85 | `maturity_mth()` is new and is `IUL_US_S`'s frame from issue, on the policy clock, which `is_active` reads; a point with no month left, or none in cover, has no frame; a withdrawal below its fee breaks `IUL_US_S`'s own roll-forward; a ladder without its rows misstates the credits and the trailing rate; the compiled caches hold the frames of the contract's issue ages alone |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0`; `pols_if_at` returns `pols_if(t)` for every timing | `pols_if_at(t, BEF_DECR)`, from `t_entry()`; `BEF_NB` the count before the month's new business, formed from the month before in the cell itself, and `BEF_MAT` the `BEF_DECR` count, as in `IUL_US_S`; `pols_if_init()` is 0 unless in force; the decrements zero outside cover | Policies in force at the valuation date open the count; new business joins it in its issue month; the chain is one cell a month |
| `av_pp_at`, `fa_pp_at`, `lca_pp_at`, `loan_bal_pp` | `av_pp_init()`, `av_pp_init() − loan_bal_init()`, `loan_bal_init()` and `loan_bal_init()` at `t = 0`, then the previous month's closing cell: chains of five, six and two cells a month | at `t_entry()`, the account value's parts summed on a point in force, `av_pp_init()` on any other, and `fa_pp_init()`, `lca_pp_init()` and `loan_bal_init()`, then the previous month's close formed in the cell itself, `IUL_US_S`'s arithmetic in its order; zero outside cover but the account value's opening, carried into `t = proj_len()` | The fixed account and the collateral are not the account value less the loan and the loan once a policy has segments or interest has accrued; every chain one cell a month, since a compiled model runs it on the C stack |
| `seg_bal_pp`, `seg_ded_cum_pp`, `seg_wd_cum_pp`, `seg_share`, `seg_bal_active_pp`, `seg_bal_tot_pp`, `seg_count`, `seg_new_pp`, `seg_roll_pp`, `index_credit_pp` | keyed by the month of creation on `IUL_US_S`'s own clock; no segment before `t = 0`; the pool and the total summed by `sum()` over a generator | the six cells of a segment in a month keyed by its slot, `(t, k)`, `k = duration_mth(t) − m`, and `seg_new_pp` by the policy month of creation; a segment born before the valuation date opened from the ladder at `t_entry()`, its creation balance its row's three amounts summed, and its share there read only for a slot the ladder holds, 0 for any other, as `IUL_US_S`'s read outside a segment's life gives; the pool and the total summed in a compensated loop, the live segments counted in a loop | A policy in force holds live segments; twelve slots a month make a compiled cache of 12 where creation months would make one of 1,452; the loops are `IUL_US_S`'s `sum()` bit for bit from Python 3.12, and compile |
| `index_level`, `seg_return`, `index_credit_pp`, `cred_rate_ann` | the index at `duration_mth(t)`; a segment's start level `index_level(t − 12)` and its cap the engine's default, the cap in force at `t = 0`; the trailing rate's first-segment test `t < 12` | the index at `t`; the start level and the cap from `seg_index_start(t)` and `seg_index_cap(t)`, the frame's or the ladder's; the engine inlined into `seg_return(t)`, `seg_credit_rate(t)` and `index_credit_pp(t)`, in its order of operations and of bounds, and the five engine cells kept as they are, called by no projection cell; the first-segment test `duration_mth(t) < 12` | One index path for every point, on the valuation clock; each credit stays `IUL_US_S`'s, a ratio of two levels on that path; a compiled cell keyed by floats keeps a dictionary for a cache; the ladder runs from the policy's own twelfth month |
| `sum_assured_at`, `face_reduction_pp`, `cum_prem_pp`, `cum_prem_net_pp`, `premium_pp` | opened at `t = 0` at the face at issue, 0 and 0, and the TARGET cap's premiums to date at 0 | opened at `t_entry()` from `sum_assured_init()`, `cum_prem_init()` and `cum_prem_net_init()` on a point in force, and from the issue values on any other | A policy in force brings in its face, its premiums and its no-lapse accumulator |
| `is_mec` | the 7-pay test of the month alone, `policy_year(t) <= 7` and the premiums to date above the limit | the same test, then the latch: month `t − 1`'s flag, or `is_mec_init()` at `t_entry()` | A contract that fails the test is a modified endowment contract for good [R5]; `UL_US_S` latches it, and so does this model |
| `premium_pp`, `db_pp`, `face_reduction_pp`, `corridor_factor` | branches on the text of `premium_type()`, `premium_mode()`, `db_option()` and `qual_test()` | branches on eight decodes, each read from a 0/1 vector `Data` decodes from the column: `is_level_premium`, `is_single_premium`, `is_target_premium`, `is_annual_premium`, `is_monthly_premium`, `is_db_option_a`, `is_db_option_b` and `is_gpt` | No monthly cell compares text, and no projection cell calls a label accessor. The label accessors stay, for reporting, and a value no decode knows still raises `IUL_US_S`'s message |
| `class_factor`, `coi_rate_scale`, `surr_charge_rate`, `lapse_shock_year` | joined on the label accessors, the surrender-charge schedule's row read in each | the same joins, made in `Data` once for the table: the class factor, once `data.class_count()` has checked its table, a vector by point; the COI scale a schedule number, `coi_schedule()` (below); and the schedule's two columns, `surr_charge_rate_max()` and `surr_charge_runoff_years()`, vectors by point once `data.surr_charge_count()` has checked the table; a class, or on a point with a charge a schedule, the table lacks refused by `Data`, naming every such point; a point without a charge reads its schedule where the table holds its id, as at stage E, and its two accessors raise `ValueError`, naming the point, where it does not | A blank factor, a missing value to `IUL_US_S`, would reach the cap on `mort_rate`, which keeps it missing, and a blank charge `surr_charge_rate`'s `max`, which reads it as none; `IUL_US_S` raises pandas' `KeyError` on a missing key |
| `corridor_factor`, `mort_rate`, `coi_rate_guar`, `lapse_rate_base` | the table read in the monthly cell, at `age(t)` or `policy_year(t)`, clamped to the extent of the key column as pandas reads it | one reader keyed by the age or the year — `corridor_factor_at`, `mort_rate_base_at`, `coi_rate_guar_py` and `lapse_rate_base_py` — with `IUL_US_S`'s clamp, to the extents `Data` reads from each key column once it has checked the keys and the values, called inside cover only | No table is read at an age or a year the policy does not have, each is read once an age or a year, and a malformed key or value is refused by name, where `IUL_US_S`'s extent skips a blank key and cuts the table short, and a blank value is a missing value |
| `prem_persistency`, `premium_pp`, `wd_pp`, `loan_new_pp`, `face_reduction_pp`, `sum_assured_at`, `corridor_factor`, `db_pp`, `coi_rate_guar`, `coi_pp`, `expense_unit_mth_at`, `maint_fee_pp`, `loan_credit_rate_ann`, `sweep_pp`, `seg_index_start`, `seg_index_cap`, `seg_return`, `surr_charge_rate`, `cum_mnlp_pp`, `nlg_test_ok`, `nlg_in_effect`, `nlg_expiry_shock`, `is_shortfall`, `gpt_limit`, `gpt_ok`, `seven_pay_limit`, `is_mec`, `mort_rate`, `lapse_rate_base`, `lapse_rate_sc_mult`, `cred_rate_ann`, `lapse_rate_dyn_mult`, `lapse_rate` | unguarded: no `IUL_US_S` frame has a month before issue | zero or false outside cover, `is_active(t)`, before any table or rate is read; the two lapse multipliers 1.0, `lapse_rate_sc_mult` before it compares the policy year with the shock year | A future point's months before issue have `t ≥ 0` and policy years down to −9 at the horizon, and policy year 0 is the shock year of a point with no surrender charge. At `t = proj_len()` nothing is charged, paid, credited or withdrawn |
| `av_change`, `expenses` | `av_change` reads `t + 1`; maintenance on `pols_if(t)` | zero outside cover | At `t = proj_len()` the carried count would bear an expense, and `av_change` would read a month past the frame |
| `inflation_factor` | `(1 + inflation_rate)^(policy_year(t) − 1)`, stepping on the policy anniversaries | `(1 + inflation_rate)^(t // 12)`, stepping on the valuation anniversaries | Unit costs in valuation-date dollars; 0 as shipped |
| `wd_pp`, `loan_new_pp` | the model point's `wd_pp` and `loan_new_pp_ann` columns read in the monthly cell | read once a point, by `wd_pp_mth()` and `loan_new_pp_ann()` | A monthly cell on the accounts' chains reads no model point column in its own formula |
| `check_av_components`, `check_av_roll_fwd`, `check_seg_ladder`, `check_margin` | `math.isclose` with `rel_tol=1e-9` and `abs_tol=1e-8`, and the ladder's tests, month by month | the same conditions on residual cells, one a month: `check_av_components_resid(t)`, `check_av_roll_fwd_resid(t)` and `check_margin_resid(t)`, each a `float` over the larger side and 10, and the ladder's four, `check_seg_count_resid(t)`, `check_seg_credit_resid(t)`, `check_seg_bal_resid(t)` and `check_seg_closure_resid(t)`; a residual that is not a number fails, and one that is not real raises, as `IUL_US_S`'s check does | A residual a compiled model can type, and a failure that can be found by month |
| `check_margin` | the loan term `loan_bal_pp(t) × pols_lapse(t)`, the whole loan | `min(loan_bal_pp(t), csv_pp(t)) × pols_lapse(t)`, the debt a surrender recovers | The surrender claim is the net cash value floored at 0, so once a loan exceeds the cash value `IUL_US_S`'s identity is off by `(csv_pp(t) − loan_bal_pp(t)) × pols_lapse(t)` and its check fails on a projection that is right, as on its point 5 from policy month 383: −2.09 on point 9 at `t = 0`. This model states the identity as `UL_US_SEC`, `VUL_US_SEC` and `ULSG_US_SEC` do, and the two agree wherever the loan is within the cash value |
| `result_pols` | `pols_if`, the three outflows and the two rates | `pols_new_biz` second; the rates 0 outside cover | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `result_seg` | the return written 0 where `t < 12` | the return `seg_return(t)`, 0 in a policy's first twelve policy months | The ladder runs from the policy's own twelfth month |
| `claims` | `claims(t, kind=None)`: one kind's claims, or with `None` the two summed by Python's `sum` | `claims_death(t)` and `claims_lapse(t)`, the `result_cf` columns, and `claims(t)` their total, `0.0 + death + lapse` | A compiled cell takes C numbers, and `None` is none. Python's `sum` of two floats is their sum, rounded once, from its `0.0` start, which this computes, so the total is `IUL_US_S`'s float in every month, the sign of a zero included |
| `coi_rate_scale`, `coi_rate_last_year`, `coi_rate_guar_py` | the point's scale, a Series, sliced from the table by its sex, class and issue age, and its last policy year read from it | `coi_schedule()`, the number of the point's scale, a row of `Data`'s table of the scales by policy year, and the last year a `Data` vector by schedule; a point whose scale the table lacks is schedule 0, refused, naming it and its issue age, where a rate is read | No compiled cell returns a Series. `IUL_US_S` raised `KeyError` where it read the missing scale, and projects a point that never reads one, valued or issued at or past `charges_cease_age`, so the refusal waits for the read |
| `Data` and the cells that read a table | a malformed value or key met, if at all, only when a projection reaches it, a missing class or schedule as `KeyError`, and an age table read at its nearest row whatever its ages | refused by name at the first read of the array, over the whole table: an issue age, a `duration_mth`, a first year of the withdrawal or the loan, or a `point_id`, past `2**53`, a class the class factors lack, a schedule the surrender charges lack or a run-off of `2**53` years or more on a point with a charge, and a negative age in the corridor or mortality table | A compiled model holds numbers, not text, and holds each age table from age 0 (*What it refuses*, below) |

The other new cells are `policy_count`, `t_entry`, `is_active`, `pols_new_biz`, the six
new opening-state accessors, `fa_pp_init`, `lca_pp_init`, `sum_assured_init`,
`cum_prem_init`, `cum_prem_net_init` and `is_mec_init`, the ladder's five slot accessors,
`seg_bal_pp_init(k)`, `seg_ded_cum_pp_init(k)`, `seg_wd_cum_pp_init(k)`,
`seg_index_start_init(k)` and `seg_index_cap_init(k)`, and `coi_rate_last_year`, the extent
of a point's COI scale, all of running in force; those of compiling are listed under *What
compiling changed, and why*, below.

Of the cash flows, the change of clock moves none at the shipped assumptions: inflation
ships at 0, and the index path's clock moves the level and no credit. On a point restated
in force, every cash flow, count and per-policy value is `IUL_US_S`'s from its month on, to
rounding, and so is every column of `result_seg()` but the index level. On point 12, every
one is `IUL_US_S`'s point 4's, 25 months on.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, on the points of the splice
grid, which take the branches they do not, on the guaranteed basis and the adjusted
beginning credit base, and where a NaN index return reaches the credited rate's bounds.
The compile tests hold it so on x86-64, and to 1e-12 relative elsewhere, where no run has
shown it yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py indexed_ul                   # in place, beside the model
python tools/build_sec_cy.py indexed_ul --out /tmp/iul    # elsewhere, with the CSVs
```

The tool exports the model to `IUL_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `IUL_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/indexed_ul")  # the directory holding the build
from IUL_US_SEC_nomx_cy import mx_model as model
model.Projection[6].result_seg()           # point 7, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 6` after `Projection.result_cf()` leaves point
1's 912-row frame cached, while `point_id()`, not yet computed, reads point 7's label, and
`Projection.inflation_rate` set to 0.025 once `Projection[6]` has computed point 7's
`expenses(12)` leaves it at 4.3259, where modelx recomputes 4.4340, as an
ItemSpace made after it does. Set every Reference on a model just imported, before
anything is computed, where modelx would recompute.

A build takes about three minutes with gcc, 197 s here under load, and needs a C
compiler, which is why `requirements.txt` leaves modelx-cython out:
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
compiled 171 of its 198 `Projection` cells to C throughout, but 13 kept a dictionary for a
cache: the eight that took a timing or a kind as text, or `claims`'s `None`, and the five
cells of the crediting engine, keyed by floats. The six segment cells, keyed by the month
of a segment's creation, cached a C array of every month of the frame by every creation
month, which made a `Projection` ItemSpace a struct of 62.7 MB; and it ran only 1.4 times
its own export, 0.94 to 0.98 s against 1.31 to 1.36 s for `net_cf` over every frame of the
committed points. The bodies of the typed cells still called pandas and Python: a
`model_point()` lookup for each attribute a formula read, a `.loc` on a table for each
policy year's lapse and COI rate, each attained age's corridor factor and mortality, each
point's class factor and surrender-charge schedule, and each segment of the ladder, the
point's COI scale sliced into a Series by its sex, class and issue age, text compared in
every formula that branched on the death benefit option, the qualification test, the
premium pattern or mode, the basis or the credit base convention, and generators summed
in `claims`. So each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[6]` is point 7, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once: the death benefit option
  into `is_db_option_a` and `is_db_option_b`, the qualification test into `is_gpt`, the
  premium pattern into `is_level_premium`, `is_single_premium` and `is_target_premium`,
  the premium mode into `is_annual_premium` and `is_monthly_premium`, and
  `has_surr_charge` into a flag of its own. Each decodes as `IUL_US_S` compares the
  column, exactly, so a value none of the flags names, `"level"` or `"GPT "` among them,
  is no flag, and the cell that branches on it raises `IUL_US_S`'s message, as `IUL_US_S`
  does.
- **Tables indexed by integers.** The lapse table is held by policy year, and the corridor
  and mortality tables by attained age, padded from 0 so that the year or the age is the
  index. The COI scales, keyed by sex, class and issue age, are numbered from 1 in the
  order of those keys, each point carrying the number of its own, `coi_schedule()`, and
  held by schedule and policy year in `coi_rate_array`, with the last policy year of each
  schedule beside it, `coi_rate_last_years`. That departs from the plan's R7 as
  `UL_US_SEC` does: there is no first-key vector, since the table's check requires every
  scale to start at policy year 1. The padding holds NaN, and nothing reads it: each
  table's one reader refuses a policy year below 1, naming the point, and reads an age
  outside the table at its nearest row, as `IUL_US_S` does. The class factor and the
  surrender-charge schedule are one number a point, and each is joined to the points in
  `Data`. Every point reads its class factor in its first month in cover, and a point
  with a charge its schedule in every month of it, so `Data` refuses a class or, on a
  point with a charge, a schedule the table lacks, naming every such point, where
  `IUL_US_S` raised `KeyError` as the point projected. A point without a charge is never
  refused a projection for its schedule, which `IUL_US_S` never reads; it reads its
  schedule's two columns where the table holds its id, as at stage E, and where the table
  does not, `has_surr_charge_schedule()` is 0 and both accessors raise `ValueError`,
  naming the point, as at stage E. A point whose COI scale the table lacks reads the scale
  only while charges run, and a point valued or issued at or past `charges_cease_age`
  never does, so `IUL_US_S` projects it: it is schedule 0, with a last year of 0, and
  `coi_rate_last_year` refuses it, naming it and its issue age, where a rate is read.
- **The ladder by slot.** `Data` holds the segment ladder as five tables by the point's
  position and the slot, `seg_bal_pp_init()` to `seg_index_cap_init()`, as wide as the
  most rows one point holds, plus one, so that the slot is the column; a point's count and
  last slot are vectors, `inforce_segment_count()` and `inforce_segment_last()`, which
  `proj_len()` holds to the slots a policy in force holds. Each of the five readers of the
  ladder refuses a slot below 1 or past the point's last, naming the point and the slot,
  where stage E's `.loc` raised pandas' `KeyError`, so no read meets the padding, and a
  row in a far slot, which `proj_len()` refuses, widens nothing.
- **Segments by slot.** `IUL_US_S`'s six cells of a segment in a month take `(t, m)`, `m`
  the policy month of the segment's creation, and a compiled cache of them would hold
  every creation month of the frame in every month: 1,452 at the longest cover, issue age
  0. Here they take `(t, k)`, `k = duration_mth(t) − m` the segment's slot, 0 to 11, and
  read the same segment a month younger at `(t − 1, k − 1)` (*The segment ladder*, above),
  so that each caches twelve values a month. `seg_new_pp(m)`, one value a segment, keeps
  its creation month. The loops that read the segments, the pool, the total, the count and
  the least balance, run over the creation months in `IUL_US_S`'s order and read each at
  its slot, so that each sums, counts or compares in the order `IUL_US_S` does.
- **The crediting engine, inlined.** `IUL_US_S` credits a maturing segment through five
  cells of float arguments, `index_change`, `index_credit_rate`, `seg_credit_base`,
  `index_credit` and `seg_matured_value`, three of them with `None` defaults. A compiled
  cell keyed by floats keeps a dictionary for a cache, and a `None` default is a Python
  object. So the projection computes the credit in cells keyed by the month:
  `seg_return(t)`, the return of the segment maturing in month `t`; `seg_credit_rate(t)`,
  new, its credited rate, `max(index_floor, min(cap, index_par × r))` at the cap declared
  at its creation, the bounds in `IUL_US_S`'s order, the cap first and then the floor; and
  `index_credit_pp(t)`, the rate times the credit base under `seg_credit_base_conv`, the
  rate first, then the base, as `index_credit` multiplies them. Each computes what the
  engine computes, in its order, so the credit is `IUL_US_S`'s bit for bit. The five
  engine cells are kept as they are, for `IUL_US_S`'s worked example, which prices one
  segment's credit at the current and the guaranteed cap through them, and for the
  comparison with `IUL_US_S`; no projection cell calls them, and `tests/us_registry.py`
  admits them by name, `"engine"`, as Python cells with a dictionary for a cache.
- **Codes.** A timing, a kind, the basis or the credit base convention, which `IUL_US_S`
  spells as text, is an int Reference named as the text: the count's timings
  `BEF_NB = 0`, `BEF_DECR = 1` and `BEF_MAT = 2`, the accounts' `BEF_PREM = 3`,
  `BEF_CREDIT = 4`, `BEF_WD = 5`, `BEF_FEE = 6`, `BEF_SWEEP = 7`, `BEF_INV = 8` and
  `EOM = 9`; the kinds `DEATH = 0`, `LAPSE = 1`, `MATURITY = 2` and `WITHDRAWAL = 3`; the
  bases `CURRENT = 0` and `GUARANTEED = 1`; and the conventions `REMAINING = 0` and
  `ADJ_BEGIN = 1`. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`,
  `av_pp_at(t, BEF_FEE)`, `claim_pp(t, DEATH)`, and a run on the guaranteed basis sets
  `basis = GUARANTEED`. A string argument or a string value would give the cell a
  dictionary for a cache, where a code indexes a C array, so codes are numbered from 0
  without a gap. The model has two families of timing, the count's and the accounts',
  passed to different cells, and they are numbered as one, `BEF_NB` and `BEF_DECR` first,
  as in every SEC model, then the count's third, then the accounts' in the order of their
  instants within the month, `EOM` last. So no two timings share a code, and a code of one
  family passed to the other's cell, `av_pp_at(t, BEF_NB)`, is refused as `invalid
  timing` in both engines, where two families numbered from 0 would read it as
  `BEF_PREM` without a word. Each cell compares its code with `==` alone, so a text set on
  `basis` or `seg_credit_base_conv` meets the cell's own refusal in modelx, `invalid basis`
  or `invalid credit base`, and is refused at assignment compiled (*What it refuses*,
  below). The `Projection` docstring's *Codes* lists all 18.
- **The claims, split.** `IUL_US_S`'s `claims(t, kind=None)` is one kind's claims or, with
  `None`, the two summed by a generator: neither a C parameter nor a C loop. Here the kinds
  are two cells, `claims_death` and `claims_lapse`, the `result_cf` columns, and
  `claims(t)` is their total, `0.0 + death + lapse` (*Departures from IUL_US_S*, above).
  With two kinds the sum is rounded once, so no compensation is needed, where
  `ULSG_US_SEC`'s three kinds need `sum`'s loop written out.
- **Three compensated loops.** The pool, `seg_bal_active_pp`, the total,
  `seg_bal_tot_pp`, and the account value a point in force opens with, `av_pp_at` at
  `t_entry()`, its parts summed, sum floats as Python's `sum()` does from Python 3.12,
  Neumaier's way: each addition's rounding error carried in a variable of its own and
  added back once at the end, where it is finite and not zero,
  `abs(c) <= 1.7976931348623157e308`, the largest double, a test no compiler folds away,
  as `ULSG_US_SEC` writes it. Each is a C loop on doubles, and is `IUL_US_S`'s `sum()` bit
  for bit, a pool of 10⁻¹⁶ included, where no compiler reassociates the additions or folds
  `(s − u) + x` away (*Two compiler directives*, below).
- **No Python call kept.** No formula outside the reporting and engine cells calls a
  Python builtin outside its refusals but `int`, `float`, `bool`, `abs`, `min`, `max` and
  `range`, which Cython turns into C, all but one `int`: `lapse_shock_year`'s `int` of the
  run-off, a float, is a Python int converted to a C `long long`, exact below `2**63`, and
  `Data` holds a charged point's run-off below `2**53` years. So `tests/us_registry.py`
  admits none, as it admits `WholeLife_US_SEC`'s and `ULSG_US_SEC`'s `round`.
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `rate_class()`, `db_option()`, `qual_test()`, `premium_type()`, `premium_mode()` and
  `surr_charge_id()`, and the four reports return a table row, text and DataFrames, for a
  reader, for `run_sec.py` and for the comparison with `IUL_US_S`. No other cell calls
  them, so they cost the projection nothing. A label accessor returns its column as read,
  and `Data` accepts a label that is not text: a blank `surr_charge_id` on a point without
  a charge, which reads as NaN and projects, and any other blank or numeric label, which
  the point's first projection refuses. So each accessor compiles to a Python object, as
  the sample traces it (below), and returns what modelx returns. The four checks are
  reporting cells too, but they return a verdict, which compiles to a C `bint`.

The `Data` docstring lists its vectors and arrays, each with the column or file it comes
from: 20 vectors of int64, among them the point labels, the decodes, the COI schedule of
each point, the last year of each schedule and the ladder's count and last slot by point;
21 vectors of float64 by point, among them the three joins, and three by policy year or
attained age; six tables of float64, the COI scales by schedule and policy year and the
ladder's five columns by point and slot; and nine int counts and extents, each a table's
check, `coi_schedules`, the COI table's, and `inforce_segment_max`, the ladder's, among
them. The nine readers stay Python, returning DataFrames and a path, and no `Projection`
cell but `model_point()` reads them. Every other cell of `Projection` but the five engine
cells, 185 of its 202, returns a C `bint`, `long long` or `double`, and caches a single
value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,574 by `t`, of `double`, `long long` or `bint` | the 116 cells of `t` alone: every count, rate, factor, charge, premium, withdrawal, loan draw, balance, credit, claim and cash flow; the policy clock, its years and the attained ages; the segment maturing in each month, its start level, cap, return and credited rate; the segment count; the flags `is_active`, the guarantee's three, `is_shortfall`, `gpt_ok` and `is_mec`; and the checks' monthly residuals |
| a C array of 1,574 by 12 | `pols_if_at`, `fa_pp_at`, `lca_pp_at`, `av_pp_at` and `av_at`, by `(t, timing)`; `claim_pp` and `claims_from_av`, by `(t, kind)`; and the six segment cells, by `(t, k)` |
| a C array of 14 by `k` | the five readers of the ladder, by its slot at the valuation date |
| a C array of 1,453 by `m` | `seg_new_pp`, by the policy month of a segment's creation |
| a C array of 123 by `y` | `lapse_rate_base_py` and `coi_rate_guar_py`, by policy year |
| a C array of 122 by `a` | `corridor_factor_at` and `mort_rate_base_at`, by attained age |
| one `long long`, `double` or `bint` | the 46 cells without a parameter but the reporting ones: the point's label, numbers, decodes and opening state, its class factor, COI schedule and the scale's last year, its surrender charge, run-off and shock year, the ends of its frame, the basis, the monthly guaranteed and loan rates and the NAAR factor, the no-lapse period and premium, and the four checks |
| a Python object | `model_point()`, the seven label accessors and the four reports |
| a Python dictionary, by its float arguments | the five engine cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary but the engine
cells'.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the four reports
and the four checks on every committed point, which reach 176 of the 202 cells, and
then the 26 they do not and the codes no report passes: `model_point()` and the
seven label accessors, which only a reader asks for; `point_id()`, which only a refusal
names; `is_target_premium()`, which a level premium never asks for; the guideline premium
and 7-pay tests, the MEC latch and the shortfall trigger, which no report reads, with what
only they read, the three tax inputs, the two limits, the premiums to date and their two
opening-state columns; the five engine cells; and, in cells the reports reach, `pols_if_at`
at `BEF_MAT`, `av_at` at every timing but `BEF_PREM`, and `claims_from_av` at `MATURITY`.
It calls the monthly ones in every month of the frame and the month after it. Each engine
cell it calls with every defaulted parameter both at its `None` default and at a value:
traced at a value alone, mx2cy types the parameter as a C `double` or `long long` and keeps
its `None` default, which Cython refuses, and the build fails; traced both ways, it types
as a Python object, as the cell's dictionary keeps it. It projects the committed points
alone: the export it runs reads the CSVs of the directory the build is made in, and the
trace it needs is the committed points', which are what the tests project. The seven
label accessors it calls once more, on a copy of the table's first point with every label
blank, which it writes to a temporary directory and reads by a second instance of the
export, given the file's absolute path as `model_point_file`. That types them as Python
objects, so that a blank or numeric label returns what modelx returns rather than raising
`TypeError`. The committed points leave branches untaken: a TARGET or SINGLE premium,
Option B's corridor on an exhausted account, the guaranteed basis, the adjusted beginning
credit base, a point without a surrender charge and a lapse shock year in frame. That
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
| `t` | 1,574 | 1,572. The longest frame is a policy issued at the youngest issue age, 0, to the end of the projection at attained age 121, 121 policy years, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 121 + 120 = 1,572 months, `t = 0 … 1,571`, and the month after, 1,572, which the count and the account value's opening timing are carried into. `av_change` and the three relative residuals read `t + 1` in cover alone, so nothing reads 1,573 |
| `t`, `timing` | 1,574 by 12 | `t` as above, by the ten timings of the one numbering and two columns more, so a timing 10 or 11 is inside the cache, where the cell refuses it as modelx does, and one from 12 raises |
| `t`, `kind` | 1,574 by 12 | `t` as above, by the four kinds and eight columns more; a kind from 4 to 11 is refused by the cell, and one from 12 raises |
| `t`, `k` | 1,574 by 12 | `t` as above, by the slots 0 to `seg_term_mth` − 1, 0 to 11: the width every 2-D cache shares. Cython's generated unpickle code converts a space's 2-D caches with one function, written for one width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*) |
| `k` | 14 | 13: the ladder's slots at the valuation date, 1 to `seg_term_mth`, 12, and one more, so that slot 13 meets the reader's own refusal compiled |
| `m` | 1,453 | 1,451, the last covered policy month at issue age 0, the latest a segment is created in |
| `y` | 123 | 121, the policy year of the last covered month at issue age 0, read by the two readers by policy year inside cover alone |
| `a` | 122 | 120, the last attained age in cover, read by the two readers by age inside cover alone, from the youngest issue age, 0 |

`proj_len()` refuses a point issued below `issue_age_min`, 0, and `Data` one below 0, and
the projection ends at attained age 121, `maturity_age`, so no report on a point the model
projects runs past these caches. `issue_age_min`, `maturity_age`, `seg_term_mth` and
`Data.future_horizon_mth` are the contract the sizes are derived from; `issue_age_max`,
85, is the contract's too, and sizes nothing. Lower the minimum, or raise `maturity_age`
or the horizon, and a report runs past the caches in the compiled model alone: a frame of
more than 1,573 months, a creation month past 1,452, a policy year past 122 or an age past
121 raises `IndexError`, naming nothing, where modelx projects. Raise `seg_term_mth` past
12 and a slot from 12 does the same. Each needs the sizes derived again, as `spec_sec.py`
derives them, and a rebuild: `t` raised to 12 × (`maturity_age` − `issue_age_min`) + the
horizon + 2, `m` to 12 × (`maturity_age` − `issue_age_min`) + 1, `y` to `maturity_age` −
`issue_age_min` + 2, `a` to `maturity_age` + 1, the width to `seg_term_mth`, and `k` to
`seg_term_mth` + 2. The tests' splice that moves the segment term to 24 months runs in
modelx alone for that reason. The shipped COI scale carries the anchor cell alone, issue
age 45, so a point at any other is refused by its first COI rate, naming it; an issue
age of 0 is the contract's, which an extended scale reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it was
measured to change there. Here `cpow` reaches nine powers: the monthly rates of both
decrements, `1 − (1 − q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`, the monthly
fixed-account, guaranteed, loan and collateral rates, `(1 + i)^(1/12) − 1` in
`inv_return_mth`, `guar_rate_mth`, `loan_rate_mth` and `loan_credit_rate_mth`, the index
path, `(1 + r)^(t / 12)` in `index_level`, the premium persistency, `0.98^(y − 1)` in
`prem_persistency`, and expense inflation, `(1 + r)^(t // 12)` in `inflation_factor`.
Without `cpow` a compiler with C99's complex numbers, gcc among them, computes a power of
two doubles as a complex power, which can differ from Python's float power in its last
bits. `-ffp-contract=off` keeps gcc from fusing a multiplication and an addition into one
instruction rounded once, which would move the last bit of a product summed, and the
compensated loops rest on more: on the additions being done as written, which no
optimization level reassociates without `-ffast-math`, which nothing sets. With both
directives and the flag every compiled value agrees with modelx's bit for bit, and the
compile tests hold each, by the module's first line, by the compiler's command lines and,
on x86-64, by the comparison itself. On the same platforms the tool adds
`-Werror=incompatible-pointer-types`, so that gcc before 14, which only warns of a pointer
of the wrong type, fails the build as gcc 14 does: the error two cache widths give (*The
sample and the spec*, above).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of
4,986,976 bytes, about 5.0 MB, the type's basic size, which holds every cell's cache: 116
arrays of 1,574 months and 13 of 1,574 by 12, each beside a flag array of its shape that
marks what is computed, make nearly all of it, the 13 2-D caches' values 1.96 MB of it.
That is 1.8 times `ULSG_US_SEC`'s, for frames of 1,574 months against 1,358, and 2-D
caches 12 wide against 10, 13 of them against seven. As it stood after running in force,
with the segment cells keyed by creation month, the struct was 62.7 MB, and the slots
alone, not the codes, take it from that to this. Deleting it, `del model.Projection[idx]`,
frees nothing by itself: an ItemSpace sits in reference cycles, and only Python's cyclic
collector frees it. That is why `run_sec.py --block` collects after each release, in its
frame pass and in its projections (*Run it*, above), and a compile test holds a compiled
block run to one point's ItemSpace at a time. Allocating and zeroing the struct is paid
once a point: the frame pass, which makes each point's ItemSpace, asks its `proj_len()`
and releases it, took about 0.2 ms a point (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised. What it needs is stack. The deepest call the contract allows, a cold
`net_cf` in the last month of the longest cover, issue age 0, issued now or 120 months on,
runs the account value's chain back to `t_entry()`, 1,470 cells deep in modelx (*Counts
and timings*, above), and compiled with gcc it runs on a thread of 352 KiB of
stack and not of 320, 223 to 245 bytes a level. A test runs it in a thread of
1 MiB, the stack Windows gives a program's main thread unless the program is linked for
more, and again on the main thread, which is where `run_sec.py --cython` runs. MSVC's
frames may be larger than gcc's, and the `cython` CI job, which runs the test on Windows
too, is the check on them: the test first runs the call at seven stacks, from 256 KiB to
2 MiB, and reports the smallest it ran on, so a first run there measures MSVC's need. Until
then it is an estimate: at `WholeLife_US_SEC`'s 325 to 433 bytes a level it would be about
466 to 621 KiB, inside 1 MiB by more than 1.6 times, and `VUL_US_SEC`'s 1,484 levels,
as deep, ran on the 1 MiB main thread on the Windows leg. A stack below the need kills its
child on an overflow, by design (with gcc, 320 KiB does); on Windows the child
ends with `STATUS_STACK_OVERFLOW`, and should Windows Error Reporting hold it instead, the
test waits a bounded time for each child rather than the job's hour. The export recurses
in Python instead: the same call needs a recursion limit of 2,966 there, and the four
reports and the four checks, which run in ascending `t`, need 438 on the twin of
`IUL_US_S`'s point 5 and on point 8, where the expiry's shock reads the account value
cold back to policy month 49, and 60 to 64 on the other committed points once the package
is imported. So `sample_sec.py` sets 12,000, four times the first rounded up to the
thousand, and a test holds it to that derivation.

**On Windows**, which no run here has reached, the `cython` CI job's Windows leg is the
check, and five things are particular to it. The stack, above, is MSVC's to measure. The
three compensated loops are exact only where the compiler neither reassociates their
additions nor folds `(s − u) + x` away nor fuses an addition with a multiplication: MSVC's
default, `/fp:precise`, keeps all three, on x86-64, whose SSE2 arithmetic has no fused
multiply-add, and nothing sets `/arch:AVX2`; the exact comparison on the Windows leg's
core grid, which holds every pool and every segment share that reads it, is the check.
The powers call the C runtime's `pow`, which modelx's float power calls too, on the same
platform, so the compile tests' exact comparison holds there too, and a difference would
be a finding. MSVC accepts the unpickle code's mismatched 2-D cache shapes that gcc 14
refuses, so the one inner width is held by the Linux leg and by the test of the spec's
sizes. And the cost of allocating and zeroing the 5.0 MB struct a point has been measured
on Linux alone.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot decode, join or hold, when the array is first read, naming every
  point at fault, or the table and its lines: a `point_id` that is not a whole number,
  when the labels are first read, by `point_id()` or a refusal; a `rate_class` the class
  factors lack; and, on a point that `has_surr_charge`, a `surr_charge_id` the schedules
  lack. `IUL_US_S` fails every projection of a point of the first kind with a `KeyError`,
  and of the second its cash flows, which read the schedule in every month; compiled, that
  refusal is the table's, so every point is refused with it, as `Term_US_SEC`'s refusals at
  the first read are. No projection of a point without a charge reads its schedule, so
  none is refused for it; on such a point whose id the table lacks
  `surr_charge_rate_max()` and `surr_charge_runoff_years()` raise `ValueError`,
  `point_id 1: surr_charge_table.csv has no row for its surr_charge_id`, compiled as in
  modelx. Every decode and join compares the text exactly, as `IUL_US_S` does, so
  `"NT "`, with a space, is no class, `"m"` no sex of the COI scale and `"iul10"` no
  schedule, each refused in both engines. And, before it is cast to int64, a number of
  `2**53` or more in size, which numpy would cast to the least int64 without a word: a
  `point_id`, an issue age, a `duration_mth`, the first year of the withdrawal or the loan,
  and, on a point with a charge, a run-off, which `IUL_US_S` projects as a charge that
  never runs off.
- A negative age in `corridor_factors.csv` or `mort_table.csv`, by the table's check,
  which every reader of the table asks first: each is held from age 0, so that the age is
  the index. A refusal `IUL_US_S` lacks.
- A key beyond a table, by the one cell that reads it, naming the point, where
  `IUL_US_S`'s lookup raised `KeyError`: a policy year below 1, `point_id 1:
  lapse_table.csv has no rate for policy year 0`, from `lapse_rate_base_py`, and the same
  from `coi_rate_guar_py`, neither of which a projection calls outside cover; a point whose
  COI scale the table lacks, from `coi_rate_last_year`, when its first rate is read; and a
  slot of the ladder below 1 or past the point's last, `point_id 7:
  inforce_segments_sec.csv holds no segment in slot 13`, from each of the five readers.
- By `proj_len()`, the six kinds of point *The in-force interface* above lists, in that
  order.
- A timing or a kind a cell does not take, `ValueError("invalid timing")` and
  `ValueError("invalid kind")`, where the code is inside the cell's cache: a code of the
  other family, `av_pp_at(0, BEF_NB)`, `pols_if_at(0, BEF_PREM)`, `av_at(0, BEF_MAT)`, a
  timing of the family the cell lacks, `av_pp_at(0, BEF_SWEEP)`, `lca_pp_at(0, BEF_WD)`,
  `fa_pp_at(0, EOM)`, a kind the cell lacks, `claim_pp(0, MATURITY)`,
  `claims_from_av(0, WITHDRAWAL)`, and a code up to 11, `claims_from_av(0, 11)`.
- A basis or a credit base convention neither of its codes names, `ValueError("invalid
  basis")` and `ValueError("invalid credit base")`, set as an int; set as text, compiled
  refuses it at once, with `TypeError`, below.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1574)`, which modelx answers with 0, the month being outside cover;
`pols_if_at(0, 12)` and `claim_pp(0, 12)`, which modelx refuses as `invalid timing` and
`invalid kind`; `seg_bal_pp(0, 12)` and `seg_new_pp(1453)`, which modelx answers with 0;
`seg_bal_pp_init(14)`, which modelx refuses, naming the point and the slot;
`lapse_rate_base_py(123)` and `coi_rate_guar_py(123)`, which modelx reads at the table's
last year, 0.04 and 83.333333; and `corridor_factor_at(122)` and `corridor_factor_at(-1)`,
which modelx reads at the table's nearest row, 1.0 and 2.5. An `idx` past the last row is
refused in both, with an `IndexError` at the first read of a vector, and `Projection[-1]`
reads every vector at its last element in both, so it is the table's last point, under
that point's own `point_id()`.

A Reference is a C variable of its value's type: `issue_age_min`, `issue_age_max`,
`maturity_age`, `omega_age`, `charges_cease_age`, `seg_term_mth`, the two step years, the
codes, `basis`, `seg_credit_base_conv` and `idx` a `long long`, as
`Data.future_horizon_mth` is, and the rates, amounts and index levels a `double`. Set past
that type, it is converted when it is set, where modelx keeps the value as given. A float
set on an int Reference is truncated toward zero without a word, `maturity_age = 120.7`
reading 120, where modelx computes with the float: `maturity_mth()` is then
908.4000000000001 there. A text, a NaN or an
int beyond 64 bits is refused at once, with `TypeError`, `ValueError` or `OverflowError`:
`basis = "GUARANTEED"`, `IUL_US_S`'s spelling, is a `TypeError` compiled, where modelx
takes it and `is_guaranteed_basis()` then raises `invalid basis`. An int set on a
`double` Reference reads as a float compiled, where modelx returns the int:
`lapse_shock_mult = 2` gives `lapse_rate_sc_mult` 2 in modelx and 2.0 compiled in the
shock year. Each shipped Reference is a value of its C type, so no shipped number differs.
And a Reference set past its domain computes as C computes, where modelx raises: an
`inflation_rate` of `1e300` makes `inflation_factor(24)` infinite compiled, where modelx's
power raises `OverflowError`.

A rate past its domain is computed, not refused, as in `IUL_US_S`. The annual mortality rate
is capped at 1, `min(q, 1.0)`, in both, so its monthly rate stays real. The lapse rate is
capped at `lapse_rate_cap`, and the no-lapse expiry's shock, `nlg_shock_lapse`, is returned
before the cap: with either set past 1 the annual rate passes 1 and the monthly rate, `1 −
(1 − w)^(1/12)`, has no real value. It is complex in modelx, whose account value and margin
checks then raise, a residual that is not real raising, and NaN compiled, whose same two
checks then fail, a residual that is not a number failing. On point 1 with the cap at 5 and
the spike at 30 times, the shock year's rate is 1.2, and there `check_av_roll_fwd()` and
`check_margin()` raise in modelx and are false compiled, while `check_av_components()` and
`check_seg_ladder()` hold in both. A NaN stays NaN through the cap on mortality, in both,
and through each other bound the compiled model computes as a comparison that keeps the
value unless the bound is smaller, or larger. The credited rate keeps `IUL_US_S`'s order of
bounds, `max(index_floor, min(cap, index_par × r))`, so a return that is not a number is
lost to the cap, since `min` keeps its first argument unless a later one compares below it:
an `index_return_ann` of NaN credits every maturing segment at the cap, 10%, in both engines
alike, and a cap that is not a number credits the floor. `Data`'s refusals of a value
outside its range keep any NaN from reaching them through the inputs.

The index path and the competitor rate are inputs a user may want to replace: a
historical or simulated path in `index_level`, and a market rate in `comp_rate_ann`,
which switches dynamic lapse on. In modelx each is a formula override, made before the
model computes anything, as the docstrings say. Compiled, a formula is C, and there is no
override: a path is a formula edit and a rebuild, or a Reference the formula reads.

### Speed

`python tools/bench_sec_cy.py indexed_ul` builds the model into a temporary directory, or
takes a build with `--build`, and times one block run on three engines: modelx, the export
and the compiled model. Each engine runs the committed table repeated, in a process of its
own, as `run_sec.py --block` runs a block, each point projected and then released. The
table's companion, the segment ladder, is repeated with it, each copy of a row naming the
copy of its point, as the tool repeats every companion keyed by `point_id`. `net_cf` is
`net_cf(t)` summed over the frame, the projection alone, as `basiclife/BasicTerm_SC` is
timed on its `pv_net_cf()`; `result_cf` is the report `run_sec.py` prints, which builds a
DataFrame for each point. Each time is the fastest of three runs, with their spread in
seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,000 | 4.01 ms (24.06–24.42) | 4.75 ms (28.52–29.13) | 90 MB |
| export | 600 | 69.4 ms (41.62–41.82) | 65.0 ms (39.02–41.54) | 90 MB |
| modelx | 120 | 2,060 ms (247.7–256.2) | 2,140 ms (257.0–266.2) | 295 MB |

The blocks are the committed table repeated, 500 times compiled, 50 exported and ten in
modelx. On `net_cf` the compiled model runs 17.3 times its export, and on `result_cf`, where
building the DataFrame takes part of its time, 13.7 times; it runs 515 and 451 times modelx.
A second run of the compiled model and the export straight after, under a 1-minute load
between 3.0 and 3.2, gave the compiled model 4.12 and 4.63 ms and the export 69.2 and 64.7
ms, 16.8 and 14.0 times. That is more times its export than `UL_US_SEC`, 12.0, and
`ULSG_US_SEC`, 12.2, or `WholeLife_US_SEC`, 13.9, `Term_US_SEC`, 9.5, and `BasicTerm_SC` on
its own measure, 8.7. A point takes longer than `ULSG_US_SEC`'s, 1.42 ms, for 202 cells
against 165, frames of up to 937 months on the committed points, a ladder of twelve segments
a month, and a struct 1.8 times the size. As it stood after running in force, compiled the
same way, the model ran 1.4 times its export, the twelve committed points' `net_cf` taking
0.94 to 0.98 s (*What compiling changed, and why*, above), where a copy of them takes about
0.05 s here, some 20 times less: the representation, not the compiler, is the gain. The
release keeps a block flat: the compiled model's peak grew by less than 0.1 MB over its
6,000 points, and without the collection after each release (`--no-collect`), 504 compiled
points peaked at 2,326 MB, about 4.6 MB a point. Reading the eight files and building every
`Data` vector and array for those points took 0.155 s, and asking every point for its frame,
the runner's first pass, which makes, reads and releases each point's ItemSpace, 1.25 s,
about 0.2 ms a point, the struct's allocation and zeroing among it.

Measured on 2026-11-13 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 1.9 and 3.8 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Under load the spread is wide, and the fastest run is the
one to compare.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 5, issued at
  the valuation date, every cell of `IUL_US_S`'s agrees at every argument `IUL_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point`, `result_pols` and
  `check_margin`, whose meaning changed, and `coi_rate_scale`, the point's COI scale as a
  Series, which this model replaced by a schedule number, and whose rates the identity
  compares in `coi_rate_guar` in every month; `IUL_US_S`'s `claims(t, None)` is compared
  with the total `claims(t)`, its kinds through the `result_cf` columns `claims_death` and
  `claims_lapse`, and a segment cell's value at `(t, m)` with this model's at the slot
  `(t, t − m)`. A cell this model lacked would fail it. So the
  goldens `tests/test_indexed_ul_us.py` asserts on those points — the worked example's
  credits through the engine cells, the anchor's account value rows and its month-0
  trace, the ladder's first segment and its eleven deductions, the pitfalls, point 5's
  overloan from month 383 and its account value turning negative at month 604 — hold here,
  with no number restated. The identity holds on any count, since `IUL_US_S` already
  charges acquisition on the policies issued. The same suite holds the model to the
  conventions every `_SEC` model meets: every frame starts at `t = 0`, `pols_if` is the
  `BEF_DECR` count, new business enters once at its `policy_count`, nothing happens
  before issue, and the in-force columns are present.
- **The splice**, in `tests/test_indexed_ul_us_sec.py`: each `IUL_US_S` point restated in
  force at a month either side of its events, opened with `IUL_US_S`'s own count, state and
  segments there, continues the S projection from there, in its four reports, column by
  column, and in every other cell the two share, to 1e-9 relative with no absolute floor,
  since its counts and its deepest ladder values fall far below 1e-7. A value both models
  give below 1e-9 a policy, a rounding about zero, is held to that floor instead, and
  `seg_count` and `seg_share` are left out of a month where a live segment or the pool is
  such a rounding in either model: off the valuation date each such state is reached
  through other arithmetic than `IUL_US_S`'s, the creation balance of a segment carried in
  summed from its row and each return a ratio of two levels on another path. The
  comparison leaves out those cells the twin identity
  skips, `IUL_US_S`'s own opening accessors and frame, the index level, whose path is on
  another clock, and the MEC flag, which latches here and which a test of its own compares
  with `IUL_US_S`'s flag accumulated. The months straddle the product's events: a
  segment's creation and its maturity, the first anniversaries, a full ladder of twelve
  segments carried in mid-year, the surrender charge's last month, the lapse shock year,
  the no-lapse guarantee failing, passing again and expiring, with its lapse shock on a
  policy with no cash value, the 7-pay test's seventh year and the latch it leaves, the
  guideline cap on a TARGET premium, a loan whose collateral is credited apart from it,
  charges ceasing in cover, a face withdrawn to nothing, a segment and the pool closing on
  a rounding about zero, `IUL_US_S`'s point 5's fixed account and then its account value
  entering the month below 0, and the last covered month, whose `t = 1` is the month the
  survivors are carried into. So are variants of S's points, in a copy of S's table that
  is never committed, each changing S's columns only and each with input rows of its own,
  for branches S's own points do not reach: between them they carry every class and both
  sexes, both death benefit options, the single and the TARGET premium, each premium mode,
  a second surrender-charge schedule and none, issue ages 50 and 65, loans from policy year
  6, a split allocation, a premium over the 7-pay limit, withdrawals that cut the face to
  nothing, withdrawals from the issue month (variant 19, on a row issued 13 months on),
  and underfunded payers whose accounts are exhausted. A row restated at a variant's month
  98 holds a loan its collateral would not fail the shortfall test on, where the loan
  does. The twin of each variant
  issued at the valuation date is compared with its S point cell by cell. The References
  are set in both models to reach what the shipped values leave unreached: the mortality
  A/E at 0.56, which leaves survivors at the end of every frame; charges ceasing at
  attained age 100, inside every frame; the lapse cap at 35% and the lapse spike at 10
  times, so that the cap binds; and the per-unit charge after policy year 10, which ships
  at 0, switched on. Each also sets apart a Reference from another it ships equal to. A
  second fixture, on References of its own, binds the bounds `IUL_US_S` ships idle that
  one pair of models can bind, the guaranteed cap on the credits and the dynamic lapse
  multiplier's floor, and a path of the index overridden alike in both models binds the
  index floor and the multiplier's cap. Splices of their own move the segment term to 6
  months, and to 24 on the full grid, so that every segment cell, the ladder's count and
  the comparison's cut-off read `seg_term_mth`, not the twelve it ships at; and set a
  premium persistency above 1, under which a variant fails the 7-pay test first in policy
  year 7, the window's last, which its twin latches and its row restated there fails at
  `t = 0` with no latch carried in. On a variant's twin the tests of 0 that `seg_count`
  and `seg_share` keep are asserted at a segment and a pool of 5.6e-17, which a threshold
  of `1e-9` would read otherwise; `check_seg_bal_resid` is held to the least balance of
  the segments live in each month.
- **The core grid and the full one.** By default the splice and the future business run a
  core of 40 of their cases, which between them reach every line of the model the full
  grid reaches, every opening-state column, every kind of valuation month and every premium
  pattern and mode, and every floor and cap the grid binds, each checked by the raw value it
  bounds, and a test asserts that they do. The other cases carry the `sec_full` marker and
  show as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set, and so do the
  every-state test under the main splice's References, the cold calls at the longest cover
  and the runner's test on the committed table. One leg of the CI matrix sets it, so every
  CI run runs the full grid too. Even so the default run is long: 1,045 to 1,078 seconds
  over two runs under load without the compiled tests, as the `sec` CI job runs it, the
  longest of the product modules.
  Each splice's S is swept one point at a time, as its cases ask, and its rows are
  generated one S point at a time, and every test that reads models of its own runs
  before the committed model and `IUL_US_S`, swept once for the module, are read, so that
  none adds its models to theirs: the default run, without the compiled tests, peaks at
  4.36 GB, about 2.6 GB inside the 7 GB of the smallest CI runner, macOS's. Run after the
  committed models were read, the compile step's modelx tests took it to 5.19 GB.
- **Future new business**: issued 1, 6, 13 and 25 months after the valuation date, S's
  points and variants are the S projection moved on, cell by cell, but the count before new
  business in the issue month, which `IUL_US_S`'s cell counts as in force, the index level
  and the MEC flag, as on a restated row; with zeros before issue in every report and no
  decrement rate evaluated there. A point with no surrender charge, issued 6 months on,
  shows the guard on the lapse spike: before its issue its policy year is 0, the shock year
  such a point has.
- **How it computes**: on every row the splice and the future business compare, no cell
  has been called at a negative month, none evaluated from `t_entry()` on has read a month
  before it, and none evaluated at month `t` has read a month later than `t + 1`. Every
  monthly cell holds its value outside cover and reads no table there, before issue and at
  `proj_len()`. On a fresh read of the committed model the policy clock is a closed form,
  every point's reports run under a lowered recursion limit, raised by a stated allowance
  on the two rows whose expiry shock reads the account value cold, which a recursion
  backward over the frame would exceed, and no projection cell has read a label accessor.
  And every chain is called cold, each call on a read of its own, `net_cf` in the last
  month and each chain's head, on the committed points and at the longest cover, issue age
  0, issued now and 120 months on, modelx's stack trace counting no more than one cell a
  month back to `t_entry()` and a fixed overhead, which a chain of two cells a month would
  exceed.
- **Counts, validation and regeneration**: the roll-forward closes, the last month included,
  `BEF_MAT` is the `BEF_DECR` count, and `pols_if_at` refuses a timing it does not have;
  `result_pols()` is `IUL_US_S`'s, column for column, with `pols_new_biz` beside it;
  multiplying `policy_count` by 2.5, with every assumption that ships at zero switched on,
  scales every counted cell and moves no per-policy value; each malformed row of the table
  and of the ladder is refused naming its point or its line, by its own rule, and so is a
  projection of it; each assumption table with a malformed key or value is refused naming
  its file, its column and its lines, a corridor factor below 0 among them, while the bounds
  of each range are read; a `db_option`, `qual_test`, `premium_type` or `premium_mode` no
  decode knows raises `IUL_US_S`'s message, and a class, a COI cell or a schedule the tables
  lack is refused naming the point, each value a decode or a join knows written in another
  case or with a space among them; a key of the ladder of `2**53` or more in size is refused
  before numpy can cast it; the horizon is a Reference, which at 0 refuses any future
  business, saying so; a point to be issued at or past attained age 121, one at or past the
  end of the projection, one withdrawing below its fee and one whose ladder lacks a row or
  holds another are refused by `proj_len()`, in that order, each rule on its Reference, read
  at it, just past it and with it moved, and each pair of neighbouring rules broken together
  refused by the first; a ladder of twelve rows on the wrong slots is refused by name, and
  so is a projection that reads a sparse ladder before asking for its frame; every state
  `IUL_US_S` reaches, under the shipped References, the main splice's and the second
  splice's, each run of the test, restated in force by the generator and read through `Data`
  and `proj_len()`, is accepted, the exhausted accounts, a face of 0 and the roundings about
  zero among them, and the test asserts that it met them; each flag reads the same in every
  spelling `Data` accepts, and the edges of the interface are accepted, the tables' keys
  written as floats among them; the committed table and ladder with every amount carried to
  the cent are read, and each point holds its four checks and projects within a cent a
  policy of its committed row; the committed table and ladder are what `IUL_US_S` generates;
  and each committed derived and future row opens with `IUL_US_S`'s own count and state at
  its month and continues its S point per policy, frame by frame, at the shipped
  assumptions.
- **The opening state and the rest**: each opening column, and the ladder, read as
  `IUL_US_S` would open it, gives the numbers above; the MEC flag latches where
  `IUL_US_S`'s turns itself off; the index path runs on the valuation clock, overridden
  alike in both models; the cap and the fixed-account rate, overridden on this model alone
  by paths that step 30 months from the valuation date, since `IUL_US_S` reads one cap for
  every segment, are read at month `t`, a segment keeping the cap of its creation month
  and one carried in its ladder row's; and expense inflation, switched on, steps on the
  valuation anniversaries; a check whose residual is not a number fails, the NaN sent
  through a Reference before the model computes anything; a shock lapse past 1 makes the
  account value's and the margin's checks raise in both models; on point 5 the margin
  identity holds where `IUL_US_S`'s fails; acquisition falls on new business alone; a
  tobacco point whose mortality passes 1 is `IUL_US_S`'s in every cell, the capped months
  included, the rate there the float 1.0 in both models; a NaN that reaches the cap stays
  NaN; each clamp of a table shorter than the cover binds with an effect; the engine cells
  give the worked example's credits; the docstrings describe this model and not `IUL_US_S`,
  their tables read into the right cells, and they parse under docutils with nothing
  rendered wrongly; both models read the one copy of each assumption table, and every
  Reference of `Projection` is `IUL_US_S`'s, value for value, each pair that ships equal set
  apart somewhere; the points of a block sum row by row; an extract without the generator's
  three columns, relabelled, projects the same numbers; `run_sec.py` prints the model's
  numbers; and the benchmark's block, `tools/bench_sec_cy.py`'s, repeats the ladder with
  the table, each row naming its point's copy, and refuses a row naming no point.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py IUL_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their
  call syntax changed: a point's position for its label, the codes for the text of a
  timing, a kind, a basis or a convention, the two claims cells for `claims(t, kind)`, and
  a segment's slot for its creation month. Beyond call syntax, the test of a point issued
  at attained age 120 raises `issue_age_max` to 120, and the cases that refuse a point
  issued past attained age 121, and project it once `maturity_age` is moved past it, move
  `issue_age_max` with it.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting and engine ones refers to pandas, numpy or another module,
  reads a table with `.loc` or the like, calls a reporting or engine cell, holds text but
  in its docstring and its refusals, or holds a generator, a comprehension or a nested
  function; none calls anything but a cell, a `Data` vector and the builtins of *No
  Python call kept*, and the registry admits no other for this model; every `Data` vector
  a formula reads is an int64 or float64 array, read by element; no cell is uncached; each
  label accessor returns its point's column of the same name; and only the five engine
  cells, named in `tests/us_registry.py`, take a parameter no spec size names.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting and engine ones a
  C `bint`, `long long` or `double` and a C-array cache of exactly the spec's size, and
  every new `Data` cell but a reader a typed memoryview or a C scalar, and the generated C
  keeps no Python object among a projection cell's locals, calls no Python builtin there,
  and builds no container, under both directives (C3); on the committed points, every cell
  at every argument a full modelx sweep caches is what modelx computes, bit for bit on
  x86-64, and so is every raise and every `Data` array (C4); and `run_sec.py --block`, run
  compiled, holds one point's ItemSpace at a time. In `tests/test_indexed_ul_us_sec.py`:
  the same comparison on the splice grid, the core by default and the full grid with
  `USLIB_SEC_FULL=1`, variants included, a few rows at a time, with every slot, code and
  engine call no report asks for added; the account value a point in force opens with is
  its parts summed compensated, as stage `E` summed them, bit for bit in both engines on
  inputs `Data` accepts where a plain sum differs: `1.0` from `−1e16`, `1.0` and `1e16`,
  where a plain fold gives 0.0, and `−0.0` from three negative zeros, the loop starting at
  its first part; the compiled model refuses what modelx refuses,
  with modelx's message, and an argument past a cache raises `IndexError`; the deepest
  call the contract allows runs cold on a 1 MiB stack and on the main thread, and the test
  reports the smallest of seven stacks it ran on; and `run_sec.py --cython` prints what
  `run_sec.py` prints. They are marked `cython`, and they skip without the toolchain, but
  in the `cython` CI job, which installs it on Linux and on Windows, one leg a product, a
  skip fails, whatever made it.

```bash
python -m pytest tests/test_indexed_ul_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_indexed_ul_us_sec.py -q     # the full grid
python -m pytest tests/test_model_conventions.py -q -k "[IUL_US_SEC]"
python -m pytest tests/test_compiled_conventions.py -q -k "[IUL_US_SEC]"
python -m pytest tests/test_indexed_ul_us_sec.py -q -m cython  # the compiled tests
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-indexed_ul-r1
[R4]: #uslib-indexed_ul-r4
[R5]: #uslib-indexed_ul-r5
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
