# In-Force Implementation Notes

**Status:** Draft, 2026-11-03. `RILA_US_SEC` is [`RILA_US_S`](model.md) taught to project
from a valuation date. Besides contracts issued at that date, it takes contracts already
in force there, in any month of any term, and contracts to be written in the ten years
after it, as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The
product is the one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `RILA_US_S` on another time axis, and it reads `RILA_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements are sourced: the 10% buffer, the
> 1, 3 and 6 year terms and their guaranteed minimum rates, the 7-7-6-5-4-3-0 withdrawal
> charge above a 10% free amount, the return-of-premium death benefit for issue ages 80
> and under, the Maturity Date rule and the interim value algebra [S1] [S2] [S4] [S5] [S6]
> [R2]. The declared rates and the market data are a **[std]** snapshot, every behavioural
> and expense assumption is a **[std]** standardization, and the shipped mortality table
> is illustrative, *not* a published basis. Replace them with company data before drawing
> any conclusion from the numbers.

## Run it

```bash
python products/registered_index_linked_annuity/run_sec.py          # point 1, at t = 0
python products/registered_index_linked_annuity/run_sec.py 16       # in force 71 months
python products/registered_index_linked_annuity/run_sec.py --block  # every point, summed
python products/registered_index_linked_annuity/run_sec.py 16 --cython  # point 16, compiled
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about a minute
and a half, and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is
newer than the build, and says so on stderr. `--build DIR` runs a build made elsewhere
instead (*The compiled model*, below). Nothing a build leaves is committed, and
`.gitignore` covers it.

The first prints what `run.py` prints for `RILA_US_S`'s point 1, the worked example's
anchor cell, issued here at the valuation date: the option budget of 10.0632%, 10,063.19
of the 100,000 purchase payment, the fixed leg opening at 89,936.81 and accreting at
1.7834%, a 2.22% spread; the interim value decomposition at `t = 0`, 11, 35, 71 and 143;
and the cash flows of rows `t = 0 … 11`, every number the same. Above them it says where
the point stands at the valuation date and where the term under way started.

The second prints point 16, the same contract in force 71 months. Its row `t = 0` is the
worked example's month 71, the Term End Date at +40%: the index at 140 against the
`I_s` of 100 that the term started from, which the row carries, credits 40% on the
Investment Amount of 100,000, so the interim value is 140,000.00. The roll split then
leaves 119,000.00 in the option and moves 21,000.00 to the Fixed Account, 21,051.79 after
the month's interest, and the term-end surrender concentration of a charge-free year, 10%,
takes 12,454.89 of surrender value. Every column agrees with `RILA_US_S`'s months 71 to
359 but `expenses`, which are in valuation-date dollars here, 4.25 at `t = 0` where
`RILA_US_S` has 4.81, and `net_cf` with them. Its decomposition prints `t = 0`, the
second term's midpoint, `t = 36`, and that term's end, `t = 72`, where the index, still at
140, credits nothing. Three lines to the same thing for point 16:

```python
import modelx as mx
model = mx.read_model("products/registered_index_linked_annuity/RILA_US_SEC")
model.Projection[15].result_cf()     # point 16, the table's sixteenth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[15]` is point 16, and its `point_id()` says so. `result_cf()` has
`RILA_US_S`'s nine
columns — `pols_if`, `premiums`, `withdrawals`, `claims_death`, `claims_lapse`,
`claims_maturity`, `expenses`, `premium_taxes` and `net_cf` — with one row per month from
the valuation date, `t = 0 … proj_len() − 1`. `result_av()` has `RILA_US_S`'s eleven
values per contract on the same rows, `result_iv()` the interim value decomposition, one
column per leg of the replicating portfolio, and both are zeros before issue.
`result_pols()` sets out the counts behind `result_cf()`: `pols_if`, `pols_new_biz`, then
the month's deaths, surrenders, the term-end part of those surrenders and the forced
annuitizations at the Maturity Date, then `pols_if_aft_decr`, the notes' end-of-month
`l(t+1)`, as in `RILA_US_S`.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read (`del model.Projection[idx]`, then a
collection), so the run holds the cells of one point at a time: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees. It freezes what is alive
once the model and its table are read (`gc.freeze()`), and again before the projections,
so that each collection scans only what the run has made since. It keeps the block's sum
as it goes, compensated as pandas sums a `groupby`, so that the block is, bit for bit, the
frames concatenated and summed by `t`, as below. It prints a line per point
on where it stands at the valuation date, then the block's first twelve rows and the block
summed into projection years, `t // 12 + 1`. Each derived row runs on its own copy of its
scenario (*The market scenario*, below), so the shipped table is a set of test cases rather
than a block valued on one market, and the block shows how the frames add, and nothing
more.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however long the contract has been in force,
  month `t` runs from time `t` to time `t + 1`, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the Maturity Date.
- **`duration_mth(t)`, the policy clock**, counts the months elapsed from issue at the
  start of month `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is `RILA_US_S`'s `t`, and the
  contract runs on it. `RILA_US_S`'s two readings of the contract year are kept, each on
  this clock: the interval reading `duration(t) = duration_mth(t) // 12`, which sets the
  attained age `age(t) = age_at_entry() + duration(t)`, and the month-end reading
  `duration_eom(t) = (duration_mth(t) + 1) // 12`, which sets the withdrawal charge and
  `policy_year(t) = duration_eom(t) + 1`. The term in force is
  `term_elapsed_mth(t) = duration_mth(t) % (12 T) + 1` months old at the month end, and
  `is_term_end(t)` is true where that reaches `12 T`. `BasicTerm_SE` reaches the policy
  clock by adding one a month, a recursion as long as the frame; the closed form needs no
  such chain of calls.

Every within-month quantity is still evaluated at the month **end**, time `t + 1`, as in
`RILA_US_S`: the market state, the interim value, the Account Value and the benefits on
row `t` are the values there, while `pols_if(t)` is the count entering the month at time
`t`. So the month that closes on an anniversary or a Term End Date is the last month of
its contract year or of its term, policy month `12 cy − 1` or `12 T k − 1`.

Point 16 is the anchor cell in force 71 months. At `t = 0` it is in policy month 71, the
last month of contract year 6, at attained age 65: the month that closes on its sixth
anniversary and on the end of its first term. Its first renewal term opens at `t = 1` and
ends at `t = 72`, policy month 143, its next at `t = 144`, and the Maturity Date closes
policy month 359, at `t = 288`, so its frame has 289 rows. Point 20 is a Step Rate option
on a one-year term in force 30 months: the term under way began at policy month 24, six
months before the valuation date, from the `I_s` of 100 that its row carries, and ends at
`t = 5`, policy month 35, crediting the 8% step on the index's 120. Point 24 is the
anchor cell to be issued 13 months after the valuation date: `duration_mth(0) = −13`, it is
on the books from `t_entry() = 13`, rows 0 to 12 are zeros, its first anniversary closes
`t = 24`, its first term ends at `t = 84`, and its frame has 373 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the terms, their Term Start and End Dates and the Transfer Period at each Term End Date; the cap re-solved at each renewal under `nge_reset`; the time to expiry `tau` of the option in force; the Contract Anniversaries, the free-withdrawal base snapshotted at each and the reset of the Free Withdrawal Amount; the behavioural withdrawal at each anniversary; the withdrawal programme, whose `month_end` in `withdrawal_table.csv` is a policy month end; the withdrawal charge by complete contract years and the charge-expiry shock year; the base surrender rate by contract year and the term-end surrender concentration; mortality at the attained age; the return-of-premium band, by issue age; the Maturity Date | the market scenario, `market_state(t, name)`, whose `month_end` in `market_scenario_sec.csv` is a time on the valuation clock: the index level, the Market Value Rate, the risk-free rate, the dividend yield and the implied volatility at month `t`'s end, `t + 1`, and on the Term Start Date of a term that starts at or after the valuation month; expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

The market scenario is a path in calendar time, shared by every contract of a block, so it
moves to `t`. What a term fixed when it started is a fact of the contract instead: the
index level `I_s`, the Market Value Rate `r_0` and the risk-free rate, dividend yield and
volatility the option budget is priced at, and, at a renewal under `nge_reset`, the cap
solved from them. A Term Start Date at or after the valuation month is read from the
scenario at the time it falls at, and one before it from the opening state (*The opening
state*, below). `term_start_month(t)` still returns a policy month, and each of the five
cells that read a term's start, `index_at_term_start`, `mvr_at_term_start`,
`risk_free_at_term_start`, `div_yield_at_term_start` and `impl_vol_at_term_start`, and
`cap_rate`, turns it into a month from the valuation date once, by subtracting
`duration_mth_init()`. Point 19, valued at its renewal at policy month 72, takes its `I_s`
of 140 and its re-solved cap from its scenario at `t = 0`; point 18, eight months later,
takes both from its row.

Expense inflation keeps `RILA_US_S`'s annual step, which `RILA_US_S` takes on the contract's
anniversaries as `1.025^duration(t)`, but takes it every twelve months from the valuation
date, `1.025^(t // 12)`, so the maintenance charge, $60 a contract a year, is in
valuation-date dollars for every point alike. Acquisition, 6% of the purchase payment plus
$200 a contract issued, is charged in the issue month and not inflated, and so is the
premium tax, 0% as shipped, on the purchase payments of the contracts issued.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf() for i in model.Data.model_point_table().index]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`RILA_US_S` computes, whatever the point's count: `RILA_US_S` already takes the purchase
payment and charges acquisition on the contracts in force at its `t = 0`, which on new
business are the contracts issued, and on a contract issued at the valuation date this
model's market is `RILA_US_S`'s own scenario. On `RILA_US_S`'s fifteen points every cash
flow, every count and every value per contract agrees bit for bit, and so does every
other cell the two models share but three whose meaning changed: `pols_if_init()`, now the
count already in force at the valuation date, 0 for such a point; `model_point()`, a row
of another table; and `result_pols()`, which gains `pols_new_biz`.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `RILA_US_S`'s columns,
and fifteen of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s two, and
thirteen that open an in-force contract's state. Each of the fifteen is a number, and
every amount is per contract. The market scenario the table's rows run on is in a second
file, `market_scenario_sec.csv` (*The market scenario*, below).

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the contracts in force at the valuation date, for a point already in force; the contracts issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy months elapsed from issue: positive in force, in any month of any term, 0 for a contract issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |
| `inv_amt_pp_init` | dollars, 0 or more | the start of month 0, before any month-0 event: the close of policy month `duration_mth − 1` | `IA`, the Investment Amount (AG 54's Index Strategy Base [R2]): the notional the month's crediting and interim value apply to, after every term-end credit, roll split and proportional withdrawal reduction before it. It is also the crediting basis |
| `fixed_acct_pp_init` | dollars, 0 or more | the start of month 0 | `FA`, the Fixed Account |
| `holding_acct_pp_init` | dollars, 0 or more | the start of month 0 | `HA`, the Holding Account |
| `av_pp_init` | dollars, of either sign | the start of month 0: after policy month `duration_mth − 1`'s withdrawal | `AV`, the Account Value, the interim value plus the two accounts |
| `av_pp_prev_anniv_init` | dollars, of either sign | the Contract Anniversary on or before the valuation date, before the withdrawal of the month that closes on it, policy month `12 × (duration_mth // 12) − 1` | `AV_anniv(y)`, the base of the contract year's Free Withdrawal Amount; the purchase payment in the first contract year, which opened at issue |
| `free_wd_remain_init` | dollars, 0 or more | the start of month 0 | the Free Withdrawal Amount still unused in the contract year |
| `rop_pp_init` | dollars, 0 to the purchase payment | the start of month 0 | the return-of-premium death benefit base: the purchase payment, reduced in proportion by each withdrawal |
| `index_at_term_start_init` | an index level, above 0; blank where not read | the Term Start Date of the term under way, where it precedes the valuation month | `I_s`, the index level the term's performance is measured from |
| `mvr_at_term_start_init` | a rate a year, effective, above −1; blank where not read | the same | `r_0`, the Market Value Rate then, which the interim value's rate adjustment reads [S2] |
| `risk_free_at_term_start_init`, `div_yield_at_term_start_init` | rates a year, effective, above −1; blank where not read | the same | the risk-free rate and the dividend yield the term's option budget is priced at |
| `impl_vol_at_term_start_init` | a volatility a year, above 0; blank where not read | the same | the implied volatility the term's option budget is priced at |
| `cap_rate_init` | a rate, at least the term's guaranteed minimum cap; blank where not read | the Term Start Date of the term under way, where it is a renewal under `nge_reset` before the valuation month | `c`, the Cap Rate re-solved at that renewal and floored at the guaranteed minimum |

On a point issued at or after the valuation date every amount is 0 and every term-start
value blank: such a contract opens with nothing, its purchase payment arriving in its issue
month, and its first term reads its start from the scenario. In the first contract year,
`duration_mth` 1 to 11, no free amount is available, so `free_wd_remain_init` is 0, and the
year opened at issue, so `av_pp_prev_anniv_init` is the purchase payment. Before the first
Term End Date, `duration_mth` 1 to `12 T − 1`, nothing has been transferred to either
account, so both are 0. On a point valued at a renewal, `duration_mth` a positive multiple
of `12 T`, the month before closed a term, where the interim value is the Investment Amount
itself, so `av_pp_init` is the Investment Amount plus the two accounts. On a point valued
on an anniversary, `duration_mth` a positive multiple of 12, the anniversary that opened
the year is the valuation date itself, and `av_pp_prev_anniv_init` is the Account Value
before that month's withdrawal and `av_pp_init` the value after it: they differ by the
withdrawal, as on point 17, by its $8,000. `prev_anniv` is the anniversary that **opened**
the contract year: an extract that fills the column from the anniversary after the
valuation date is a year out.

**The term-start values are given only where the term began before the valuation month**,
`duration_mth` positive and not a multiple of `12 T`, and blank everywhere else. They are
facts frozen at a past date, as `DIA_US_SEC`'s cohort weights are: no scenario re-based to
the valuation date holds a level before it, and a sensitivity run that moves the market at
the valuation date must not move them. Where the Term Start Date is at or after the
valuation month the scenario holds it: a renewal at the valuation month reads the
scenario at `t = 0`, and a future row's first term reads its copy at its issue month. So
a blank is the honest value there, and `Data` holds every given index above 0, the level
`index_perf` divides by, with no exception for a row that does not read it. A table
written the other way, with the value entering month 0 on every row, is refused.
`cap_rate_init` is narrower still: it is given only where that term began at a renewal
under `nge_reset`, `duration_mth` above `12 T`. Off `nge_reset`, and under it in the
initial term, the cap is the model point's declared cap floored at the guaranteed
minimum, which no column needs to restate. At a renewal under `nge_reset`, `RILA_US_S`
re-solves the cap from that date's market and the References `earned_rate`, `nge_spread`,
`nge_solve_iter` and `nge_cap_search_max`, a contractual fact fixed then.

**The Account Value may be of either sign.** It is the interim value plus the two
accounts, and the interim value can be negative even when the index has risen [S2]:
flooring it is not implementing the contract. `RILA_US_S` carries a contract through a
negative interim value, so `Data` accepts any finite `av_pp_init` and
`av_pp_prev_anniv_init`. The four balances a contract holds, the Investment Amount, the
two accounts and the return-of-premium base, are zero or more, and a contract in force
that holds none of the first three is refused instead: only a full withdrawal leaves a
contract nothing, and such a contract is no longer in force.

**There is no Performance Lock.** `RILA_US_S` does not implement it: the notes give the
election rule and the dollar-for-dollar withdrawal consequence, but not the rate at which
a locked bucket accrues to term end (*What is not implemented* in [`model.md`](model.md)).
This model is `RILA_US_S` run in force and adds none, so the notes' `lock_flag` and
`lock_value` are not columns, and an in-force contract carries no locked value. Nor is
there a column for the Term Start Date: terms start at issue and renew every `12 T` policy
months, so the date follows from `duration_mth` and `term_years`.

| `RILA_US_S` | `RILA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under `BasicTerm_SE`'s name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| — | `duration_mth` | The policy clock, in months. Every `RILA_US_S` point is new business, opening its frame at issue |
| — | `inv_amt_pp_init` | `RILA_US_S` opens the Investment Amount with the purchase payment at `t = 0` |
| — | `fixed_acct_pp_init`, `holding_acct_pp_init` | `RILA_US_S` opens both accounts empty |
| — | `av_pp_init` | `RILA_US_S` opens the month's investment return from the purchase payment, and the block's Account Value from 0, at `t = 0` |
| — | `av_pp_prev_anniv_init` | `RILA_US_S` reads every anniversary's base from its frame, which starts at issue |
| — | `free_wd_remain_init` | `RILA_US_S` opens the remainder at 0 in contract year 1, which has no free amount |
| — | `rop_pp_init` | `RILA_US_S` opens the base at the purchase payment |
| — | the five `*_at_term_start_init` | `RILA_US_S` reads every term's start from its scenario, at the Term Start Date's policy month passed as a time from issue |
| — | `cap_rate_init` | `RILA_US_S` re-solves every renewal's cap under `nge_reset` from its scenario |

A column measured entering month 0 is the cell it opens with `_init` added; the base
measured at the anniversary adds `_prev_anniv_init`, and the five fixings and the cap name
the cell they stand in for before the valuation month, with `_init`.
`free_wd_remain_init` takes no `_ytd`: it is not an accumulator restarting each year but
the remainder of an annual allowance, which each anniversary resets.

The columns carried over are read as `RILA_US_S` reads them. For a contract in force, the
facts they record are still those at issue, the option's terms included: a renewal keeps
its option, at the declared or the re-solved cap.

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex` | `M` or `F` | — |
| `premium` | dollars, the single purchase payment | issue |
| `term_years`, `buffer`, `crediting_type` | years, 1, 3 or 6; a fraction; `CAP`, `STEP`, `EDGE` or `FLOOR` | issue: the option, renewed at each Term End Date |
| `declared_cap`, `declared_step`, `declared_edge`, `participation`, `floor_rate` | rates; `declared_cap` blank for an uncapped option | issue: the declared rates of the initial term, and of every renewal off `nge_reset` |
| `iv_family`, `amort_rule` | `portfolio`, `notional`, `delta` or `legacy`; `straight_line` or `updated_expiry` | issue: the interim value algebra |
| `nge_reset` | a flag, `True` or `False` | issue: whether the cap is re-solved at each renewal **[std]** |
| `wd_rate_ann` | a fraction of the Account Value a year | the behavioural withdrawal rule **[std]** |
| `scenario_id`, `wd_schedule_id` | keys into `market_scenario_sec.csv` and `withdrawal_table.csv` | assumptions, not facts about the contract |
| `provenance` | text: `RILA_US_S`'s on a twin, the generator's on any other row | — |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it. First the table's own shape:

- the fifteen in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months, read by value, so that `12.0` is 12;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than
  cover from issue plus ten years: 1,200 months at issue age 0, the youngest the product
  issues [S1] [S2], and 720 at 40, the youngest the shipped mortality table rates. Set to
  0, the Reference refuses future new business altogether, and a negative horizon is
  itself refused.

Then the contract's terms, `term_years` before every check that reads the term clock:

- `age_at_entry` is a whole number of years, 0 or more, and `term_years` a whole number of
  years, 1 or more, each read by value: `RILA_US_S` reads both by `int()`, which truncates
  a fraction without a word, and the term clock counts months modulo `12 T`;
- `premium` is a number above 0;
- `buffer` and `floor_rate` are fractions, 0 or more and below 1, each the strike
  `I_s (1 − x)` of a put, and `participation` is a number above 0, by which the cap's
  strike divides;
- `declared_cap` is blank, for an uncapped option, or a number, zero or more, and
  `declared_step`, `declared_edge` and `wd_rate_ann` are numbers, zero or more: each
  reaches a `max` or a `min` that would lose a blank;
- `nge_reset` is a flag, read by value: `True` or `False`, as pandas reads either, or 1 or
  0, where `RILA_US_S`'s `bool()` reads any text, a blank among them, as `True`;
- `nge_reset` is set only on a capped Cap Rate option, `crediting_type` `CAP` with
  `declared_cap` given. `RILA_US_S`'s solver prices the at-the-money call, the call at the
  cap and the buffer's put: on a Floor option it would solve the wrong portfolio, and on a
  Step, an Edge or an uncapped option the flag does nothing, and `RILA_US_S` projects
  either without a word.

Then the opening state:

- the Investment Amount, the two accounts, the remainder and the return-of-premium base
  are numbers, zero or more, and the Account Value and its base at the anniversary are
  finite numbers of either sign;
- each term-start value, where given, is a number in its range: the index level and the
  volatility above 0, the Market Value Rate, the risk-free rate and the dividend yield
  above −1, each added to 1 under a division or a logarithm, and the cap a finite number;
- a contract not yet in force, `duration_mth` 0 or less, holds nothing yet: its seven
  amounts are 0;
- the five term-start values are given exactly where the term under way began before the
  valuation month, and `cap_rate_init` exactly where, besides, that term began at a
  renewal under `nge_reset`;
- a contract in force holds an Investment Amount or an account balance;
- `rop_pp_init` is at most the purchase payment;
- in the first contract year the remainder is 0 and the base at the anniversary is the
  purchase payment;
- before the first Term End Date both accounts are 0;
- on a renewal valuation `av_pp_init` is the Investment Amount plus the two accounts;
- on an anniversary valuation `av_pp_prev_anniv_init` is at least `av_pp_init`, the
  anniversary month's withdrawal lying between them.

Last, each point's keys into the tables it is joined with, each table's count cell asked
first, so that a malformed table is refused by its own message (below): its `scenario_id`
is a scenario of `market_scenario_sec.csv` that sets its levels by the first month the
point is on the books, `t = 0` or its issue month if later; its `wd_schedule_id` is a
programme of `withdrawal_table.csv`; its `term_years` is a term of
`guar_min_rate_table.csv`; `mort_table.csv` gives a rate at its `sex` and its attained age
in that first month; and `cap_rate_init`, where given, is at least the guaranteed minimum
cap of its term, which `cap_rate` floors every re-solved cap at. `RILA_US_S` meets a key
its table lacks only as it projects: a missing scenario, sex or age raises Python's own
error, naming no file, and a missing withdrawal programme takes no withdrawal, without a
word.

An extract may carry each amount of money to the cent, as an administration system holds it,
each within half a cent of its exact value, and every rule between amounts allows for that
without a tie falling to floating point: a cent where a rule compares one amount with
another or with 0, as `MYGA_US_SEC`'s do, and two and a half cents in the renewal rule,
whose identity ties four amounts and so can miss by two cents, half a cent from each.
`RILA_US_S`'s Edge option restated at its renewal at 36, every amount carried to the cent,
misses its identity by a cent, which floating point reads as 0.010000000009, and is read;
point 19's Account Value 0.024 above its Investment Amount and Fixed Account is read, and
0.03 above is refused. The generated rows carry `RILA_US_S`'s own values, unrounded. The
table is returned with the columns those checks read by value as the numbers they were
checked as: `duration_mth`, `age_at_entry` and `term_years` int64, or float64 where a value
of the column is `2**53` or more in size, which an int64 cannot be trusted to hold, so that
the value reaches `Data`'s vectors uncast (*What it refuses*, below), `policy_count`,
`premium`, the rates and the thirteen opening-state columns float64, blank as NaN, and
`nge_reset` the flags it was checked as. A text column outside its categories passes `Data`
and is refused, with `RILA_US_S`'s message, by the cell that branches on it, wherever the
model first reads it (`invalid crediting_type`, `invalid iv_family`, `invalid amort_rule`).

Accepted, because a contract can be in each state: an Account Value below 0, at the
valuation date or at the anniversary; a zero count; and a `duration_mth`, an
`age_at_entry` or a `term_years` written as a float, read as the whole number it holds.

Two rules are the product's rather than the table's, because they need `Projection`
References, which `Data` cannot read, and `proj_len()` checks them, each raising
`ValueError` naming the point, after the bounds the compiled model's caches are sized
from and before the mortality table's cover (*What it refuses*, below). A point at or past
its Maturity Date at the valuation date,
`duration_mth ≥ maturity_mth()`, which needs `maturity_age` and `maturity_min_years`, has
no frame and is refused rather than projecting nothing. And from the second contract
year, `duration_mth` 12 or more, the remainder is at most the year's Free Withdrawal
Amount, `free_wd_rate × av_pp_prev_anniv_init`, to a cent: the year's withdrawals only
ever reduce it. That rule holds where the base is 0 or more, and is not applied below 0.
On a negative base `RILA_US_S`'s allowance is negative too, and its behavioural rule,
`min(wd_rate_ann × AV, allowance)`, takes the more negative of two negative amounts, a
withdrawal below 0, which the cap at the Account Value passes through; at a behavioural
rate above `free_wd_rate` that leaves a positive remainder no allowance bounds. This model,
`RILA_US_S` run in force, computes the same, and no shipped point's Account Value falls
below 0. A loop over the block meets a refused row only when it reaches it, after
projecting the points before it, so `run_sec.py --block` asks every point for its frame
before it projects any, and stops before it prints anything.

An attained age past the mortality table's last before the Maturity Date is refused by
`proj_len()` too, naming the point and the last age the table rates the point's sex at,
where `RILA_US_S` raises pandas' `KeyError` at the first month that reads it, because the
maturity age is a `Projection` Reference; the shipped table runs to 120, past every
committed contract's cover. Nothing can check that a term-start value is the one the
point's own history ran on, because no scenario holds a path before `t = 0`.

The five assumption tables are `RILA_US_S`'s, read in place by `RILA_US_S`'s readers, and
the scenario companion through `RILA_US_S`'s reader too. Beside each reader a `Data` cell
checks the table once and returns its rows, an int, which every `Data` array and number
made from the table asks for before it reads a value, so that the one `Projection` cell
that reads the table meets the check first: `market_scenario_count`,
`mort_table_count`, `surr_charge_count`, `guar_min_rate_count`, `lapse_table_count` and
`withdrawal_count`. Each reads its table's keys by value, once, as the join matches them,
so that a month written `36.0` is 36, and refuses, naming the file, the column and the
lines at fault: a key that is blank, text or not a whole number, or below its least value;
a key on two rows; a sex other than `M` or `F`; a gap in a sex's ages; a surrender charge
table whose contract years do not run from 0, one row a year, which `RILA_US_S` would read
as no charge in the missing year; and a lapse table whose first year is not 1, under which
the years before it would have no rate. It refuses a value that is blank, text, infinite
or outside its range: a mortality rate below 0, a surrender charge or base surrender rate
outside 0 to 1, a guaranteed minimum rate or a withdrawal below 0, an index level or a
volatility not above 0, a Market Value Rate, risk-free rate or dividend yield not above
−1. A mortality rate above 1 is accepted, and capped. `RILA_US_S` takes the keys as pandas
reads them: one written as text turns its column to text, every lookup on it misses, and
a surrender charge or a withdrawal is then zero without a word, or a lookup raises an
error that names no file.

## The market scenario

`RILA_US_S` keys its market by the month end from issue, `market_scenario.csv`'s
`month_end`, which is the valuation clock of a contract issued at the valuation date and of
no other. Its scenarios step: Scenario A's index is 100 from issue, 120 from month end 36
and 140 from month end 72, Scenario B's 100, 80 and 75. A contract restated in force at
month `d` reads month `d + t` of its path at its own `t`, which one table on the valuation
clock cannot hold for contracts restated at different months.

So `RILA_US_SEC` reads its own, `market_scenario_sec.csv`, through `RILA_US_S`'s reader,
`Data.market_scenario()`, whose Reference `Data.market_scenario_file` names it. It has
`RILA_US_S`'s columns — `scenario_id`, `month_end`, `index_level`, `mvr`, `risk_free`,
`div_yield`, `impl_vol` and `provenance` — and `month_end` is a time in months from the
valuation date. It holds 27 rows:

- `RILA_US_S`'s ten rows as they stand, `up`, `down`, `legacy` and `charge_ex`, for the
  twins, so that a twin reads `RILA_US_S`'s own market;
- for each row restated at month `d`, a copy of its S point's path re-based to that month,
  `{id}-M{d}`: each `month_end` less `d`, the level in force at `d` moved to 0, and the
  levels before it dropped. `up-M71` holds 120 at 0, S's level from month end 36, and 140
  at 1, S's month end 72;
- for each row issued `k` months on, a copy moved `k` months later, `{id}-F{k}`: `up-F13`
  holds Scenario A's three levels at 13, 49 and 85, and none before the issue month.

No row is typed by hand: the file is generated with the table, by the same spec (*The model
points*, below), from `RILA_US_S`'s scenarios as `RILA_US_S`'s reader reads them, each
copied row keeping `RILA_US_S`'s `provenance`, and the tests regenerate it and compare.
`Projection.market_state(t, name)` reads the state that holds at time `t` on the model
point's scenario, as `RILA_US_S`'s step search finds it, from `Data`'s arrays, which hold
each column step-filled by valuation month (*The compiled model*, below); the month's state
is the one at its month end, `t + 1`. A real block shares one scenario on the valuation
clock, and then needs no copies: the shipped table is a set of test cases, each derived row
valued on its own market.

`Data.market_scenario_count()` checks the file as `Data` checks the assumption tables
(above), and `Data` refuses a point whose scenario sets no level by its first month on the
books. A scenario may start after `t = 0`, for business issued later, so the month it must
start by is the point's: a future row's copy holds no level before its issue month, and no
cell reads one there.

## The model points

No row of `model_point_table_sec.csv` or `market_scenario_sec.csv` is typed by hand. Every
one is generated from `RILA_US_S`, its table and its scenarios by `tests/sec_support.py`,
from the `RILA_US_SEC` entry in its `SEC_SPECS`, and the tests regenerate both files and
compare, so an edit to a `RILA_US_S` row reaches them or fails the suite. In the source
repository, `python tools/gen_sec_points.py RILA_US_SEC` writes them.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–15 | twin | S points 1–15 | issued at `t = 0`: `RILA_US_S`'s fifteen contracts — the worked example's anchor cell on Scenarios A and B, the second with its $8,000 withdrawal at the term midpoint, the behavioural withdrawal rule, Step, Edge and Floor crediting, interim value families (b) and (c), the pre-AG 54 engine, the updated-time-to-expiry amortization, a participation rate above 100% on a 20% buffer, an uncapped option at issue age 81, the cap re-solved at each renewal, an excess withdrawal that bears the charge, and the [S2] withdrawal charge example |
| 16 | derived | S point 1 at S month 71 | the anchor in the last month of its first term: the Term End Date at +40% at `t = 0`, from the row's `I_s` of 100, with 0.850607 contracts in force and an Account Value of 119,890.17 entering the month |
| 17 | derived | S point 2 at S month 36 | Scenario B's anchor on its third anniversary, after the $8,000 withdrawal of the month that closed on it: 84,803.11 before it, 76,803.11 after, 480.31 of the year's 8,480.31 free amount left, and the return-of-premium base at 90,566.38, above the Account Value |
| 18 | derived | S point 13 at S month 80 | the reset point mid-term after its first renewal, at policy month 72: the cap re-solved there, 99.7038%, and its `I_s` of 140 from the row, and 19,019.70 in the Fixed Account from the first term's end |
| 19 | derived | S point 13 at S month 72 | the same contract valued at that renewal: no term-start column, its `I_s` of 140 and its cap re-solved from its scenario at `t = 0` |
| 20 | derived | S point 4 at S month 30 | the Step Rate option on a one-year term, mid-term, with 30,835.04 in the Fixed Account from two term ends |
| 21 | derived | S point 15 at S month 59 | the pre-AG 54 engine in the month that closes on its fifth anniversary, an Account Value of 100,000.00 entering it and 80,000.00 at its end: the [S2] withdrawal charge example at `t = 0` |
| 22 | derived | S point 12 at S month 40 | the uncapped option at issue age 81, mid-term on Scenario B, with its `r_0` of 4.00% from the row against a current Market Value Rate of 5.00% |
| 23 | derived | S point 7 at S month 119 | interim value family (b) in its last covered month, a one-row frame ending on the Maturity Date: 0.332808 contracts in force, its renewal term's `I_s` of 75 from the row |
| 24 | future | S point 1, 13 months on | to be issued at `t = 13`, on its own copy of Scenario A, `up-F13` |

A derived row's `policy_count` is the count `RILA_US_S` carries into that month, its
`pols_if(d)`, and its opening state is what `RILA_US_S` carries into it, each column read as
`RILA_US_S`'s own formulas read it: the Investment Amount, the two accounts, the Account
Value, the remainder and the return-of-premium base at the close of S month `d − 1`; the
Account Value before withdrawals at the anniversary that opened the contract year of `d`,
S's `av_pp_at(12 × (d // 12) − 1, "BEF_WD")`, or the purchase payment in the first year;
where the term under way began before `d`, S's market at its Term Start Date,
`market_state(term_start_month(d), name)`; and, on a renewal under `nge_reset`, S's
`cap_rate(d)`. So the row continues the S projection from there, in every cell but those
expense inflation moves, to the last bit, or to a few parts in 10^16 where pandas reads a
value of the table back an ulp off. Its `policy_id` is the S row's with the month appended,
`RILA-000001-M71`, and a future row's carries the months to issue, `RILA-000001-F13`. Row
`t` of a generated point is month `t + source_mth` of its S point. All 24 are at
`RILA_US_S`'s issue ages, 60, 75, 80 and 81; the product issues from age 0 [S1] [S2], but
the shipped mortality table starts at attained age 40, so a point issued younger needs it
extended first, and `Data` refuses such a point until it is.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has
five timings, in processing order:

- `BEF_NB`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, before month `t`'s decrements, the
  notes' `l(t)`;
- `BEF_LAPSE`, after its deaths;
- `BEF_TERM_SURR`, after its background surrenders;
- `AFT_DECR`, after the term-end surrender concentration `phi`, the notes' end-of-month
  `l(t+1)`.

The first two are `basiclife/BasicTerm_SE`'s, and the other three `RILA_US_S`'s, unchanged
but for their guard outside cover. `BEF_DECR` already meant in `RILA_US_S` what it means
in `BasicTerm_SE`, so no name clashes, and `BEF_NB` is the one timing running in force
adds. Any other timing raises. `BasicTerm_SE`'s `"BEF_MAT"`, the count at the start of a
month before its maturities, is not adopted: the contracts here mature at the end of the
last covered month, as `pols_maturity`, where `RILA_US_S` puts the Maturity Date.

The survivors carried into month `t` are those of month `t − 1`'s `BEF_DECR` count, which
`BEF_NB` forms itself, as its own value at `t − 1` plus that month's new business,
through the month's deaths, background surrenders and term-end surrenders in the order
`AFT_DECR` takes them. So `pols_if_at(t, AFT_DECR)` is `pols_if_at(t + 1, BEF_NB)`,
bit for bit, in every month but the last covered one, where the Maturity Date empties the
block, and it is `pols_if(t + 1)` except where month `t + 1` is an issue month, whose new
business joins `pols_if`.

The chain of calls from month `t` back to `t_entry()` is one cell a month, where
`RILA_US_S`'s count ran through two, `pols_if` and `pols_if_at`, and so are the Investment
Amount's, which ran through three, and the two accounts' and the free-withdrawal carry's,
which ran through two; the return-of-premium base's was one already. A cold `net_cf` in
the last month of the anchor's 360-month frame, point 1, runs 380 cells deep, counted as
modelx's stack trace counts it, against 1,095 in `RILA_US_S`: 359 Investment Amounts, one
a month back to month 0, and 21 cells above and below them, from the net cash flow down
through the behavioural withdrawal to the opening notional of the last month, and down
from month 0's interim value, which prices the term's option budget at its Term Start
Date's market, to the `Data` vectors its accessors read. Every committed point runs one
cell a month back to `t_entry()` and 14 to 21 more, the most on point 19, valued at a
renewal under `nge_reset`, whose month 0 re-solves the cap under the option budget; point
24, issued 13 months on, runs as deep as point 1, because its chains stop at its issue
month. At the longest cover the product allows, issue age 0, 1,080 months from issue, on a
copy whose mortality is extended below the table's age 40, it runs 1,100 deep, as new
business at the valuation date and issued 120 months on alike. Each report evaluates its
columns in ascending `t`, and a sweep of the committed points that way, every report and
check, runs at most 19 cells deep, on point 19, where the month after a renewal reads,
under its surrender rate, the interim value whose option budget re-solves the cap.
`RILA_US_S`'s own sweep runs at most 18 deep, on the reset point, point 13, as this
model's does on its twin, and up to three levels less than this model's on its other
twins, where this model's accessors read a `Data` vector a level further down.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `RILA_US_S`'s `pols_if`. It is not `BasicTerm_SE`'s
`pols_if`, the count before maturity. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left. This is `check_pols_roll_fwd_resid(t)`, which in `RILA_US_S` subtracts
`pols_if(t + 1)`: here that would count the next month's new business as a gain of month
`t`. For the same reason the block's closing Account Value, `av_at(t, AFT_WD)`, is
weighted by `pols_if_at(t + 1, BEF_NB)`. Both roll-forward checks scale their tolerance
with `policy_count`, `max(policy_count(), 1)` times `RILA_US_S`'s, since a residual is
rounding on that many contracts, and keep `RILA_US_S`'s `all(...)`, so that a residual that
is not a number fails the check. The term-end identity is per contract and keeps
`RILA_US_S`'s tolerance.

The purchase payment, its premium tax and acquisition fall on `pols_new_biz(t)`, in the
issue month: `t = 0` on the twins, `t = 13` on point 24, and never on a point already in
force, which paid its purchase payment before the valuation date. `RILA_US_S` puts them at
`t = 0` on `pols_if(0)`, the contracts issued, so on a twin they are the same at any count.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < maturity_mth()`, where
`maturity_mth() = 12 × policy_term()` is `RILA_US_S`'s frame from issue: 360 policy months
at issue age 60, 120 at 80 or above. Outside it, before issue and from the Maturity Date
on, every count is zero, and so every cash flow and every value per contract. No count
evaluates a decrement rate there, no table is read at a contract year or an attained age
the contract does not have, and no market path is read: every rate, factor and amount is
0.0 and every flag false, but the two surrender multipliers, `lapse_rate_sc_mult` and
`lapse_iv_mult`, which are 1.0, their neutral value. The market readers, `market_state`
and the five cells of the month's market, are read in cover only: a future row's copy
holds no level before its issue month, and `result_iv()` writes the index level as 0.0
there. The clock's own arithmetic, `duration`, `duration_eom`, `policy_year`, `age` and
the term clock, is defined in every month but means nothing outside cover, and no cell
calls it there; `duration_mth` and `inflation_factor` are defined in every month.

## The opening state

`RILA_US_S` projects new business only, so its frame always opens at issue, from the
purchase payment allocated wholly to the option. Read cell by cell, its recursions carry
the Investment Amount, the Fixed and Holding Accounts, the Account Value's movement, the
Free Withdrawal Amount's carry, the return-of-premium base and the count, and its cells
read the market at each Term Start Date and the Account Value at each anniversary, which a
contract valued in force may have reached before the valuation date. The interim value
has no state of its own: it is the Investment Amount times a factor priced from the
month's market and the term's start. So the opening state is thirteen columns, and the
technical notes' model point attributes and state variables map onto them:

| Notes attribute or state | Column |
|---|---|
| `investment_amount`, `IA_k(t)` | `inv_amt_pp_init` |
| `fixed_account_value`, `holding_account_value`, `FA(t)`, `HA(t)` | `fixed_acct_pp_init`, `holding_acct_pp_init` |
| `AV(t)` | `av_pp_init` |
| `AV_anniv(y)` | `av_pp_prev_anniv_init` |
| `FW_used(y)`, as its complement | `free_wd_remain_init` |
| `rop_base`, `ROP(t)` | `rop_pp_init` |
| `term_start_index`, `I_s` | `index_at_term_start_init` |
| `term_start_mvr`, `r_0` | `mvr_at_term_start_init` |
| the market on the Term Start Date, `(r, q, sigma)` | `risk_free_at_term_start_init`, `div_yield_at_term_start_init`, `impl_vol_at_term_start_init` |
| `declared_cap`, `c`, as re-solved at a renewal | `cap_rate_init` |
| `lock_flag`, `lock_value` | none: no Performance Lock |

The Investment Amount's basis is the Investment Amount itself, the notional the month's
crediting and interim value multiply, after the withdrawals and the roll split before the
valuation month, so no second basis column is needed. The term-start market is carried in
full, not the option budget alone, which straight-line amortization would need: the
`updated_expiry` rule re-prices the term-start portfolio at every month's time to expiry,
and one form serves both rules and every crediting type.

Each column is read where the contract needs it, and only there:

- the Investment Amount, the two accounts and the return-of-premium base at `t_entry()`
  on every row in force, each opening its recursion;
- `free_wd_remain_init` at `t_entry()`, unless the valuation month is the last of its
  contract year, `duration_mth % 12` being 11, where the anniversary resets the allowance:
  on points 16, 21 and 23 it is carried unread;
- the five term-start values wherever the term under way began before the valuation
  month, and `cap_rate_init` wherever that term began at a renewal under `nge_reset`;
- `av_pp_prev_anniv_init` by `free_wd_base(t)` and `free_wd_allow(t)` in the months of
  the year under way before the month that closes on its next anniversary. No cash flow
  reads it: the allowance is read only in a month that closes on an anniversary, whose
  base is then in the frame, so the column holds the base of the year under way, by which
  `proj_len()` bounds the remainder;
- `av_pp_init` by month 0's investment return, `inv_income_pp(0)`, and the block's
  movement, `av_change(0)`, where the two cancel in the Account Value's roll-forward. No
  report reads it either: the Account Value of the month is the Investment Amount priced
  at the month's market plus the two accounts. So `Data` checks it rather than the model
  reading it: against the two accounts and the Investment Amount on a renewal valuation,
  and against the base at the anniversary on an anniversary valuation.

The rows show each, with what it gives when the column is wrong:

- **`index_at_term_start_init`.** Point 16's term began at issue from `I_s` = 100, and its
  row carries it: at `t = 0`, the Term End Date, the index at 140 credits
  `140 / 100 − 1` = 40%, under the cap of 100%, and the interim value is 140,000.00, the
  worked example's. Its copy of Scenario A, re-based to month 71, holds 120 at `t = 0`,
  S's level from month end 36: a term begun before the valuation month cannot read its
  start from the scenario. With the column at 80 the credit would be 75% and the interim
  value 175,000.00.
- **`mvr_at_term_start_init`.** Point 22, mid-term on Scenario B, carries `r_0` = 4.00%,
  against a current rate of 5.00%: its interim value's rate adjustment at `t = 0` is
  `(1.04 / 1.05)^(31/12)` = 0.975582, 31 months being left in the term at the month end,
  and its interim value 78,979.80. With `r_0` at the current 5.00% there would be no
  adjustment, and the interim value would be 81,145.33.
- **`risk_free_at_term_start_init`, `div_yield_at_term_start_init`,
  `impl_vol_at_term_start_init`.** They price the term's option budget, 13.4077% on point
  22, which the straight-line rule amortizes over the term, and with which the cap solve
  and the `updated_expiry` rule price. A volatility of 25% would make it 13.8162% and the
  interim value at `t = 0` 78,818.33; a risk-free rate of 5.00%, 17.2706% and 77,452.64; a
  dividend yield of 3.00%, 8.7345% and 80,827.31.
- **`cap_rate_init`.** Point 18 carries the cap re-solved at its renewal at policy month 72
  from that date's market, 99.7038%, against the declared 100% of its initial term, and
  reads it in every month of its 40-month frame: the next renewal, at policy month 144,
  falls after its Maturity Date. With a cap of 20% the short call at the cap would be
  worth −14,233.12 at `t = 0` rather than −2,688.05, and the interim value 105,653.72
  rather than 106,565.25. Point 19, the same contract valued at that renewal, re-solves
  the cap from its scenario at `t = 0` and reaches `RILA_US_S`'s `cap_rate(72)` and option
  budget, 10.0450%, bit for bit.
- **`inv_amt_pp_init`.** Point 22's 94,119.20 is the purchase payment less the
  proportional reductions of its behavioural withdrawals at policy months 11, 23 and 35.
  The interim value is homogeneous of degree one in it: halved, the Account Value at
  `t = 0` would halve too, from 78,979.80 to 39,489.90, the accounts being empty.
- **`fixed_acct_pp_init`, `holding_acct_pp_init`.** Point 20's Fixed Account holds 30,835.04
  from its two term ends, at policy months 11 and 23, each moving 15% of the credited
  Investment Amount into it, with interest at 3.00% and less the account's share of the
  anniversary withdrawals. Point 18's, 19,019.70, halved would take its Account Value at
  `t = 0` from 125,631.86 to 116,098.56. The Holding Account is 0 on every shipped row,
  its share of the roll split being 0 as shipped.
- **`free_wd_remain_init`.** Point 17 has 480.31 left of the year's 8,480.31: the $8,000 at
  its third anniversary used the rest. So a surrender at the end of `t = 0` is charged 5%
  of its Account Value of 76,889.71 less the 480.31, 3,820.47. Had the year's allowance
  been left whole, it would shelter 8,480.31, and the charge would be 3,420.47. The
  remainder carries through `t = 10`, and at `t = 11`, the month that closes on the fourth
  anniversary, the allowance resets to 7,784.76, 10% of the frame's own Account Value
  there, 77,847.64.
- **`av_pp_prev_anniv_init`.** Point 17's base is its Account Value at the third
  anniversary before the $8,000, 84,803.11: `free_wd_base(t)` and `free_wd_allow(t)` are
  84,803.11 and 8,480.31 for `t = 0` to 10, and `proj_len()` holds the remainder, 480.31,
  to that allowance. At 90,000 they would be 90,000 and 9,000, and nothing else would
  move. On point 16, valued in the last month of contract year 6, the base of every year
  it reads is in the frame, and the column is carried unread.
- **`rop_pp_init`.** Point 17's base is the purchase payment reduced by the $8,000 in
  proportion to the Account Value before it, `100,000 × (1 − 8,000 / 84,803.11)` =
  90,566.38, above its Account Value, so its death benefit at `t = 0` is the base. Had the
  withdrawal been left out of it, the death claims at `t = 0` would be 57.20 rather than
  51.80. Point 22, issued at 81, has no return-of-premium guarantee, and its death benefit
  is the Account Value, 78,979.80, below its base of 94,119.20.
- **`av_pp_init`.** Point 21 enters its valuation month with 100,000.00 and closes it at
  80,000.00, the pre-AG 54 interim value at an accrued rate of −20% on the fifth
  anniversary: the [S2] example then falls at `t = 0`, 8,000 free, 72,000 charged at 3%,
  2,160.00, and a surrender value of 77,840.00, none of which reads the column. Point 22's
  column at 70,000 rather than 78,855.68 would move month 0's investment return from 124.11
  to 8,979.80 and the block's movement with it, and no report and no check.

## Departures from RILA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read at a policy month passed as `t` is a read on the policy clock, on the valuation clock
or of the opening state, and every recursion begins at `t_entry()`. Where `RILA_US_S`'s test
would have stayed correct on the valuation clock, it moved anyway, so that cover has one
definition. Of `RILA_US_S`'s 156 `Projection` cells, running in force left 63 unchanged,
gave 21 new text only and rewrote 72; it renamed and removed none, and added 36, 192 in all.
The 21 were eighteen new docstrings, two docstrings and one code line, `bs_d1`'s, rewrapped
to 92 characters, its syntax unchanged. The `Projection` References were `RILA_US_S`'s
`point_id`, its 28 constants, `data`, `math` and `pd`, every value unchanged. Compiling then
changed how each cell reads its inputs and spells its codes, and no number: it removed one
of `RILA_US_S`'s cells, `opt_legs`, a tuple of leg names, and added eleven, `point_id`, now
a cell where it was the Space's parameter, the join numbers `mort_schedule`,
`scenario_number` and `wd_schedule_number`, the leg cells `opt_leg_count` and `opt_leg`, and
the int-keyed forms of the pricing engine, `opt_component_at`, `opt_portfolio_at`,
`opt_portfolio_abs_at`, `credit_rate_by` and `cap_solved_at_start`, 202 in all (*The
compiled model*, below). Of `RILA_US_S`'s cells it changed the signature of eight: `claims`
and `claims_over_av`, whose total is the code `ALL` where `RILA_US_S`'s kind defaults to
`None`; the five cells of the interim value's decomposition, `opt_component_pp`,
`fixed_proxy_pp`, `budget_amort_pp`, `deriv_proxy_pp` and `trading_cost_pp`, whose timing
`RILA_US_S` defaults to `"BEF_ROLL"` and every caller here passes; and `mort_rate_base_at`,
whose age is `a` where `RILA_US_S` names it `x`. The Reference `idx`, 0, took the place of
`point_id`, and `issue_age_min`, 0, `issue_age_max`, 111, and 36 codes are new References.
The twin identity would fail on a cell of `RILA_US_S`'s that this model lacked, so it
exempts `opt_legs` by name, with its reason, compares `RILA_US_S`'s `claims(t, None)` and
`claims_over_av(t, None)` with the calls at `ALL`, and reads every timing, kind, bucket,
leg, market and column at its code.

| Cells | `RILA_US_S` | `RILA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration`, `duration_eom`, `is_anniv` | `t`, `t // 12`, `(t + 1) // 12`, `(t + 1) % 12 == 0` | `duration_mth_init() + t`, and the others the same of `duration_mth(t)`; `is_anniv` false outside cover | The policy clock, opened from the model point |
| `proj_len`, `maturity_mth` | `12 × policy_term()`, the months from issue | `maturity_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the Maturity Date, for a mortality table that stops short of the cover, and for a remainder above the year's Free Withdrawal Amount; first, for an issue age outside `issue_age_min` to `issue_age_max` | The frame starts at the valuation date. `maturity_mth()` is new and keeps `RILA_US_S`'s formula; the rules need `Projection` References, and the issue ages bound the compiled model's caches |
| `term_elapsed_mth`, `term_start_month`, `tau`, `is_term_end` | arithmetic of `t` | the same of `duration_mth(t)`, `term_start_month` still a policy month; `tau` 0.0 and `is_term_end` false outside cover | Terms align with issue, on the policy clock |
| `market_state` | `market_state(k, name)`, `k` a month from issue, on the scenario `scenario_id()` names | `market_state(t, name)`, `t` a time from the valuation date, on the scenario the model point's `scenario_id` names, read from `Data`'s arrays by its number, step-filled as `RILA_US_S`'s step search finds the state | The market is a path in calendar time. The parameter is a time on the valuation clock, so it takes `t`'s name, and every caller passes it by position |
| `index_at_term_start`, `mvr_at_term_start` | `market_state(term_start_month(t), …)`, a policy month passed as a time | the scenario at `term_start_month(t) − duration_mth_init()` where that is `t_entry()` or later; the model point's `*_at_term_start_init` before it | A Term Start Date before the valuation month is a fact of the contract, which no scenario re-based to the valuation date holds |
| `opt_component`, `opt_budget_at_cap` | the Term Start Date's market read from the scenario at `term_start_month(t)` in place | through the new `risk_free_at_term_start`, `div_yield_at_term_start` and `impl_vol_at_term_start`, each read as the index is | The same |
| `cap_rate` | re-solved under `nge_reset` at every renewal | the same at a renewal at or after the valuation month; `cap_rate_init()` for a renewal before it | A cap re-solved before the valuation date is a fact of the contract, which a change to the market or a Reference at the valuation date must not move |
| `index_perf`, `step_rate`, `edge_rate`, `opt_budget_at_cap`, `declared_cap_solved`, `opt_component`, `opt_budget`, `fixed_leg_yield`, `nge_spread_implied`, `credit_rate_at`, `budget_amort_factor`, `mva_factor`, `fixed_proxy_factor`, `deriv_proxy_factor`, `trading_cost_factor`, `cap_calc_factor`, `iv_factor`, `opt_component_pp` | unguarded: no `RILA_US_S` frame has a month outside cover | 0.0 outside cover, before any market or table is read | No market path is read outside cover: a future row's copy holds no level before issue |
| `opt_legs`, `opt_component`, `credit_rate_at`, `budget_amort_factor`, `fixed_proxy_factor`, `deriv_proxy_factor`, `trading_cost_factor`, `cap_calc_factor`, `iv_factor` | branch on the text of `crediting_type()`, `iv_family()` and `amort_rule()` | branch on ten `is_*` cells, one bool for each value `RILA_US_S` tests, decoded from the model point's column; a value `RILA_US_S` does not know raises its message where `RILA_US_S` raises it | No projection cell compares a model point column's text or calls a label accessor, which are left to reporting; compiling moved the decodes into `Data` |
| `inv_amt_basis_pp`, `inv_amt_pp`, `fixed_acct_pp_at`, `fixed_acct_pp`, `holding_acct_pp_at`, `holding_acct_pp`, `rop_pp`, `inv_income_pp` | open at `t = 0` from the purchase payment, or from 0; `inv_amt_pp` through `inv_amt_pp_at` and `inv_amt_basis_pp`, the accounts through their `_at` cells | open at `t_entry()` from the opening state, or from the purchase payment in the issue month, the opening written inline, one cell a month; the arithmetic `RILA_US_S`'s | Every recursion begins on the books, from the opening state |
| `free_wd_avail` | reset where `t` closes on an anniversary; carried as `free_wd_remain(t − 1)`, two cells a month; 0 at `t = 0` | reset on the policy clock; carried as `free_wd_avail(t − 1) − wd_free_pp(t − 1)`, one cell a month, from `free_wd_remain_init()` at `t_entry()` | The contract year is on the policy clock, and the remainder carried into the valuation month is opening state |
| `free_wd_base` | `av_pp_at(12 cy − 1, "BEF_WD")`, a policy month passed as `t` | the same month on the valuation clock, `12 cy − 1 − duration_mth_init()`, or `av_pp_prev_anniv_init()` where it precedes `t_entry()` | On the valuation clock month `12 cy − 1` is not the month that closes the anniversary |
| `wd_scheduled_pp` | the withdrawal table at `(wd_schedule_id(), t + 1)` | `wd_amount_pm(duration_mth(t) + 1)`, the new reader keyed by policy month end | The withdrawal programme stays on the policy clock |
| `mort_rate`, `surr_charge_rate`, `lapse_rate_base`, `guar_min_rate`, `lapse_shock_year` | read their tables in place; `lapse_rate_base` and `lapse_shock_year` take the `max` and the `min` of a list of the table's keys | read through one reader per table, `mort_rate_base_at(a)`, `surr_charge_rate_at(cy)` and `lapse_rate_base_py(y)`, each reading `Data`'s array of the table, which asks the table's count first, and `guar_min_rate` the point's term's row, joined in `Data`; loops for the lists | A key the table cannot be read by is refused by name before a value is read, and every table is read through one cell |
| `free_wd_base`, `free_wd_allow`, `wd_pp`, `surr_charge_rate`, `mort_rate`, `lapse_rate_base`, `lapse_rate`, `lapse_rate_sc_mult`, `lapse_iv_mult`, `pols_death`, `pols_lapse`, `pols_lapse_term`, `expenses` | unguarded, but `expenses`, zero where `t < 0` or `t ≥ proj_len()` | zero outside cover, `lapse_rate_sc_mult` and `lapse_iv_mult` 1.0, before any table or rate is read | A contract year or an attained age the contract does not have is never looked up, and nothing is charged or decremented there |
| `pols_if`, `pols_if_init`, `pols_if_at`, `pols_maturity` | `pols_if(t)` from the column's 1.0 at `t ≤ 0`, through `pols_if_at(t − 1, "AFT_DECR")`, two cells a month; the maturity at `t == proj_len() − 1` | `pols_if_at(t, BEF_DECR)`, from `t_entry()`, one cell a month, with `BEF_NB` added; `pols_if_init()` 0 unless in force; the maturity at `duration_mth(t) == maturity_mth() − 1` | Contracts in force open the count, and new business joins it in its issue month; one definition of cover |
| `premiums`, `prem_to_av_pp`, `prem_to_av`, `expenses` | the purchase payment and acquisition at `t == 0`, the block's on `pols_if(0)` | in the month with `duration_mth(t) == 0`, the block's on `pols_new_biz(t)` | A point in force paid its purchase payment before the valuation date, and one issued later pays it in its issue month |
| `inflation_factor` | `1.025^duration(t)`, stepping on the contract's anniversaries | `1.025^(t // 12)`, stepping every twelve months from the valuation date | Unit costs in valuation-date dollars |
| `check_pols_roll_fwd_resid`, `av_at`, `av_change` | `pols_if(t + 1)`, the next month's count; the block's Account Value opening from 0 at `t = 0` | `pols_if_at(t + 1, BEF_NB)`; from `av_pp_init() × pols_if_init()` at `t_entry()` | Next month's new business is no part of month `t`'s movement, and a point in force opens with its Account Value |
| `check_av_roll_fwd`, `check_pols_roll_fwd` | `all(...)` over the frame, the tolerance fixed | the same `all(...)`, the tolerance times `max(policy_count(), 1)` | A residual is rounding on that many contracts, and `all` fails a residual that is not a number |
| `result_pols` | `pols_if`, the four movement columns and `pols_if_aft_decr` | `pols_new_biz` after `pols_if` | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |
| `result_iv` | `index_level(t)` in every row | 0.0 outside cover | A future row's copy holds no level before issue |

The other new cells are `policy_count`, `duration_mth_init`, `t_entry`, `is_active`,
`pols_new_biz` and the thirteen opening-state accessors. Mortality caps as `RILA_US_S`
does, `min(q × mort_ae_factor, 1.0)`, the bound second, so that a missing input stays NaN:
`RILA_US_S`'s cell, guarded, and no departure.

In `Data`, `model_point_table` reads `model_point_table_sec.csv` and checks it, and
`market_scenario` reads `market_scenario_sec.csv`, through the Reference
`market_scenario_file`; `future_horizon_mth` is new. Four readers' docstrings changed,
`market_scenario`'s and `withdrawal_table`'s to name the clock their `month_end` is on, and
`surr_charge_table`'s and `guar_min_rate_table`'s to name the count that checks them; six
count cells are new, one beside each reader of the assumption tables and the scenarios.
`input_dir`, `mort_table` and `lapse_table` are unchanged. Compiling added 67 cells to
`Data`, its vectors, arrays and counts, 81 in all (*The compiled model*, below), and three
References, `read_last_mth`, `read_last_age` and `np`.

`Data` also refuses, naming the point, what `RILA_US_S` projects without a word: `nge_reset`
written as any text, which `RILA_US_S`'s `bool()` reads as `True`; `nge_reset` off a capped
Cap Rate option, where `RILA_US_S`'s solver prices the wrong portfolio or does nothing; an
issue age or a term that is not a whole number, which `RILA_US_S` truncates; a term of 0, on
which the term clock divides by zero; a blank or text rate that a `max` or a `min` reads;
and assumption tables whose keys or values cannot be read (above). Each is a recorded
departure: `RILA_US_S` projects such a point. So are the refusals compiling added, which
*What it refuses* (below) sets out beside `RILA_US_S`'s own outcome: a point issued above
`issue_age_max`, or whose cover needs an age past `Data.read_last_age`, which `RILA_US_S`
projects only on a mortality table extended past 120; a `term_years` of `2**53` or more in
size, which a floors row can match; and a power whose base an input or a moved Reference
takes below 0, where `RILA_US_S` returns a complex number, or past the largest float.

No read goes further ahead than the month after its own: the month's market is read at its
month end, `t + 1`, and the block's closing Account Value and the in-force roll-forward read
the count carried into month `t + 1`.

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, and its steps fall
on the valuation date's anniversaries rather than the contract's, so point 16's
`expenses(t)` is `RILA_US_S`'s `expenses(71 + t)` divided by `1.025^6`, or by `1.025^5` at
`t = 0, 12, 24, …`, where the valuation clock has stepped and the contract's anniversary is
a month away. Its other cash flows, its counts and every value per contract are
`RILA_US_S`'s from its month 71 on. Point 24 is `RILA_US_S`'s point 1 thirteen months on in
those columns too, its purchase payment and acquisition included. Its maintenance expense is
1.025 times `RILA_US_S`'s, since the valuation clock stepped at `t = 12`, before the point's
issue, and `1.025^2` times in the last month of each of its contract years, between the
valuation clock's next step and the point's own anniversary.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell reads
its inputs and spells its codes, and no number: what the model computed on each committed
point was frozen before the change, and it still computes it (*Tests*, below). Cell by cell,
at every argument a full modelx sweep evaluates, the compiled model computes what modelx
computes, bit for bit, on the committed points, and the compile tests hold it so on x86-64
on the splice grid and at the contract's extremes too, which take the branches the committed
points do not. `RILA_US_SEC` compiles on the chassis `MYGA_US_SEC` compiled first, and takes
from it what `MYGA_US_SEC`'s *What the deferred annuities inherit* sets out, with the index
crediting `FIA_US_SEC` compiled; where it departs, this section says so. What is its own is
the Black–Scholes engine, which `RILA_US_S` calls at float arguments, with Python's `math`,
to price the option budget, the interim value and the cap solve.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py registered_index_linked_annuity               # in place
python tools/build_sec_cy.py registered_index_linked_annuity --out /tmp/rila  # elsewhere
```

The tool exports the model to `RILA_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `RILA_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
# the directory holding the build
sys.path.insert(0, "products/registered_index_linked_annuity")
from RILA_US_SEC_nomx_cy import mx_model as model
model.Projection[15].result_cf()     # point 16, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made, and
keeps the values it computes until it is deleted; the base `Projection` and `Data` keep
theirs for good. So `Projection.idx = 15` after `Projection.result_cf()` leaves point 1's
360-row frame cached, `proj_len()` 360, while `point_id()`, not yet computed, reads point
16's label, and `Projection.expense_maint` set to 120 once `Projection[1]` has computed
point 2's `expenses(1)` leaves it at 4.99, where an ItemSpace made after, `Projection[2]`,
computes 9.98 for point 3's. Set every Reference on a model just imported, before anything
is computed, where modelx would recompute; a test holds the compiled model to this.

A build took 75 s and 80 s here, in two runs, with MSVC, and needs a C compiler, which is
why `requirements.txt` leaves modelx-cython out: `pip install -r requirements-cython.txt`.
`run_sec.py --cython` builds in place when it finds no build, or one older than the model,
the sample, the spec or the tool, and `--build DIR` runs a build made with `--out DIR`.
Nothing a build writes is committed. All of it derives from committed files, and an
extension module is built for one operating system, processor and Python
(`_mx_classes.cp313-win_amd64.pyd` here); in place, `.gitignore` covers all of it. A
`lifelib.create()` copy of the library carries no `tools/`, so it cannot build, and
`run_sec.py --cython` says so.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so. Compiled by
the same tool, with a sample of its own, as it stood after running in force, the model gave
179 of its 192 `Projection` cells a C number to return. Seven returned text and six a row, a
tuple or a DataFrame; 28 took a timing, a kind, a bucket, a leg, a market or a scenario
column as text, or a float, and those 28 and the eight other cells of float parameters kept
a dictionary for a cache, 36 in all. It ran 1.01 times as fast as its own export, 132.2 ms a
point on `net_cf` against 134.0, over the committed points. The bodies of the typed cells
still called pandas and Python: a `model_point()` lookup for each attribute a formula reads;
the text of a column compared in each of the ten decodes, and `pd.isna` for an uncapped
option; a `.loc` on a table for each attained age's mortality, each contract year's
surrender charge and each programme's withdrawal; a list of the scenario's months built and
searched on every read of the market; the Black–Scholes engine on Python floats, at every
leg, month and basis; and the cap solve, eighty bisections of three prices each, in every
month of every renewal term under `nge_reset`. So each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from 0,
  as `BasicTerm_SC` is: `Projection[15]` is point 16, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, named as the column, and a cell reads its point's
  element: `buffer()` is `float(data.buffer()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory. The vectors are the checked columns
  `Data.model_point_table()` returns, read as `RILA_US_S` reads them, by `float()`, `int()`
  and `bool()`, since the table's checks, from stage `E`, already refuse every numeric
  column a formula reads where it is blank, text or out of its range, naming the column and
  the points. Where a point's int can be one an int64 cannot hold, a 0/1 vector beside it,
  `term_years_ok()`, `age_at_entry_ok()` and `duration_mth_ok()`, says whether it is, and
  the accessor refuses the point where it reads the element (*What it refuses*, below).
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once: `crediting_type` into
  `is_cap_crediting`, `is_step_crediting`, `is_edge_crediting` and `is_floor_crediting`,
  `iv_family` into `is_iv_portfolio`, `is_iv_notional`, `is_iv_delta` and `is_iv_legacy`,
  and `amort_rule` into `is_straight_line` and `is_updated_expiry`; the `nge_reset` flag as
  `Data` checked it; and a blank `declared_cap`, an uncapped option, into `is_uncapped`,
  where `RILA_US_S` asks `pd.isna` of the model point. Each compares the text exactly, as
  `RILA_US_S` compares it, so a value written in another case or with a space, `Cap`, or
  `CAP` after a space, is no flag, and the cell that branches on it answers as `RILA_US_S`
  does, raising its message, `invalid crediting_type`.
- **Tables indexed by integers.** Each assumption table is an array, or a set of arrays, a
  cell reads by element. The scenarios, the mortality table's sexes and the withdrawal
  programmes are numbered from 1 in the sorted order of their keys, each point carrying its
  own, `scenario_number()`, `mort_schedule()` and `wd_schedule_number()`. The market is held
  as five arrays, one a column, by scenario and valuation month, step-filled from each
  scenario's first row as `RILA_US_S`'s step search reads it, NaN before the first and in
  row 0, with each scenario's first month beside them, and `market_state(t, name)` reads the
  point's row at `t`, where `RILA_US_S` builds and searches a list of the scenario's months
  on every call. The mortality is held by sex and attained age, from age 0, with each sex's
  first and last age beside it; the surrender charge by complete contract year; the
  programmes by programme and policy month end, 0.0 where a programme has no row, which is
  no withdrawal, as in `RILA_US_S`; and the guaranteed minimum rates joined to each point's
  term once, three vectors by point. Each is read through one cell keyed by the month, the
  age or the year, `market_state(t, name)`, `mort_rate_base_at(a)`,
  `surr_charge_rate_at(cy)` and `wd_amount_pm(m)`, and the padding, NaN, is read by none of
  them. The lapse table, a step function keyed by contract years no contract bounds, stays
  two row vectors, years and rates, which `lapse_rate_base_py(y)` scans for the last year at
  or before `y`, comparing each as the table holds it, where `RILA_US_S` takes the `max` of
  a list.
- **Arrays held to the last read.** Every array by month or age ends at the last month or
  age a read reaches, whatever the table's keys: the scenarios and the programmes at
  `Data.read_last_mth`, 1,202, the last `t` of the cache, and the mortality at
  `Data.read_last_age`, 121, the last age of its cache. `spec_sec.py` derives both
  References, and a test holds each to the spec. A scenario's last row holds to the end, as
  the step function holds it, so a key far past any read, a scenario month or a programme's
  month end of `1e20` or `2**60`, which `RILA_US_S` holds and never reaches, neither widens
  an array nor refuses a point `RILA_US_S` projects: it is dropped before it is cast,
  whatever its size. That is a departure from `MYGA_US_SEC` and `FIA_US_SEC`, which refuse a
  table key of `2**53` or more as they load the table: here such a key refuses nothing
  `RILA_US_S` projects, and a key `2**53` or more in a model point's int column still is
  refused (*What it refuses*, below). A sex's first and last ages are held as the table
  gives them, clamped to −1 and `read_last_age + 1`, so that `proj_len()` tells a table that
  rates past what the array holds from one that stops short of the cover.
- **Codes.** A timing, a kind, a bucket, a leg, a market, a scenario column or a crediting
  rule, which `RILA_US_S` spells as text, is an int Reference named as the text, the
  scenario's columns upper-cased: 36 in eight families, which the `Projection` docstring's
  *Codes* lists. A call reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`,
  `av_pp_at(t, BEF_WD)`, `claims(t, DEATH)`, `market_state(t + 1, RISK_FREE)`. A string
  argument would give the cell a dictionary for a cache, where a code indexes a C array, so
  the codes of each family are numbered from 0 without a gap. The two families of timing,
  the count's and the values', are numbered as one, `BEF_NB` 0 and `BEF_DECR` 1 first, as in
  every SEC model, then the count's others and the values' `BEF_CREDIT` 5 to `AFT_WD` 8,
  each in the order of its instants, so that a timing of one family passed to the other's
  cell, `av_pp_at(t, BEF_NB)`, is refused as `invalid timing` in both engines, rather than
  read as one of its own. The claim kinds `DEATH`, `LAPSE` and `MATURITY` are 0 to 2, in
  `result_cf`'s order, and `ALL` 3; the three rate kinds of `guar_min_rate(kind)`, `CAP`,
  `STEP` and `EDGE`, are 4 to 6, after them, so that a claim kind passed there is refused as
  `invalid kind`, and so is a rate kind passed to a claim cell. The engine's `mkt` and the
  projection's pricing basis share `CURRENT` 0 and `TERM_START` 1, which `RILA_US_S` spells
  alike; `UPDATED_EXPIRY` 2 is a basis alone.
- **The totals, by `ALL`.** `RILA_US_S`'s `claims(t, kind=None)` and `claims_over_av(t,
  kind=None)` are one kind's amount or, with `None`, the three kinds added: `None` is no C
  parameter. Here the total is the code `ALL`, and `net_cf` calls `claims(t, ALL)`.
  `RILA_US_S` writes the total as a chain of `+`, death, lapse, maturity, and the chain is
  kept, so the total is `RILA_US_S`'s float bit for bit, the sign of a zero included. `ALL`
  passed to a cell of one kind, `pols_decr`, `claim_pp`, `claim_from_av_pp` or
  `claims_from_av`, is refused as `invalid kind`.
- **The pricing engine, keyed by integers.** `RILA_US_S` prices each leg of the replicating
  portfolio with `opt_component(t, leg, spot, tau, mkt)`, which takes the index level and
  the time to expiry as floats, sums the legs in `opt_portfolio` and `opt_portfolio_abs` at
  the same floats, credits through `credit_rate_at(t, accrual)` and solves the cap through
  `opt_budget_at_cap(t, cap)`: each would compile with a dictionary for a cache and a Python
  body. But the projection calls them at three sets of floats only, each a function of `t`,
  so each is an int-keyed cell here. `opt_component_at(t, leg, basis)` is the leg at the
  current market and `tau(t)`, `CURRENT`, at the term-start market and the term `T`,
  `TERM_START`, the option budget's, or at the term-start market and `tau(t)`,
  `UPDATED_EXPIRY`, the `updated_expiry` amortization's, a C array of seven legs by nine
  codes a month. It writes `RILA_US_S`'s Black–Scholes price inline, `bs_d1`, `bs_d2`,
  `norm_cdf` and the call, the put or the binary call, the same operations in the same
  order, with `RILA_US_S`'s sign and scale per leg. `opt_portfolio_at(t, basis)` and
  `opt_portfolio_abs_at(t, basis)` add the legs `opt_leg(i)` names, and `credit_rate_by(t,
  rule)` is `credit_rate_at` at the accrual 1, `TERM_END`, or `1 − tau(t)/T`, `PRORATED`,
  the pre-AG 54 rule. `cap_solved_at_start(t)` is the cap solve, `RILA_US_S`'s bisection
  inline, keyed by the term's first month on the books, its Term Start Date as a month from
  the valuation date or `t_entry()` for the term under way there, which every month of the
  term passes: so one solve a term, of one price a trial, where `RILA_US_S` solves in every
  month of a renewal term, three prices a trial, at the same term-start market each time.
  The at-the-money call and the buffer's put do not depend on the trial cap, so they are
  priced once, where `RILA_US_S`'s cache returns the same doubles each trial. Each int-keyed
  cell is `RILA_US_S`'s float to the last bit, which a module test holds against the engine
  cell, on every committed point and month, and on two points under `nge_reset` that solve
  a one-year cap fifty times on a market that steps each year, where a comparison in the
  bisection regrouped, `atm - (otm + otp)`, moves solves that the committed points' few
  leave alone.
- **Python's `sum`, compensated.** `RILA_US_S` adds the legs, their absolute values and the
  three buckets of a withdrawal's allocation with Python's `sum`, which CPython 3.12 and
  later compensates on floats, Neumaier's way. A running sum in C would differ from it in
  the last bit, and a `sum` over a generator compiles to calls into Python. So
  `opt_portfolio_at`, `opt_portfolio_abs_at` and `wd_alloc_pp` write Neumaier's loop out,
  from `0.0 +` the first term, adding the compensation once at the end where it is finite,
  as CPython does: `RILA_US_S`'s double, three legs or four, and three buckets once the
  Holding Account holds anything.
- **`opt_legs()`, as codes.** `RILA_US_S`'s `opt_legs()` returns the crediting type's legs
  as a tuple of their names, which no C type holds. It is dropped for `opt_leg_count()`, 3,
  2, 2 or 4 by the crediting type, and `opt_leg(i)`, the code of leg `i` in `RILA_US_S`'s
  order. The twin identity exempts `opt_legs`, and a module test maps the codes back onto
  `RILA_US_S`'s tuple on every twin, the four crediting types among them.
- **`math`, admitted in two cells.** The two pricing cells, `opt_component_at` and
  `cap_solved_at_start`, call `math.log`, `math.exp`, `math.sqrt` and `math.erf`. Compiled,
  each is a call into Python's own function, through the module the export holds as an
  attribute: Cython turns none into C. `tests/us_registry.py` admits them in those two cells
  alone, by their dotted names, `"python_calls": {"opt_component_at": ("math.erf",
  "math.exp", "math.log", "math.sqrt"), ...}`, and the compile tests refuse a module call
  any cell makes that its entry does not admit, or that is not the sole argument of a
  `float(...)`: wrapped so, the result is a C double at once, and every local of the cell
  stays C, which the generated code is checked for. So a compiled price is modelx's on every
  platform, by construction, and a `math` raise, `exp`'s `OverflowError` among them, is
  Python's own in both engines. C's own `erf`, `log`, `exp` and `sqrt`, from `libc.math`,
  were measured as the alternative on a prototype of this model, which is not shipped: equal
  to Python's bit for bit over 22 million arguments under MSVC, both calling the Windows C
  runtime, and 0.39 ms, or 19%, faster a point compiled. They are not taken: the model's
  formulas cannot spell a C call, so the build would have to rewrite the generated code, and
  C's functions return NaN or an infinity where `math` raises, at the edges of their
  domains. Five more cells admit `math.log` alone, `opt_budget_target`, `fixed_leg_yield`,
  `mva_factor`, `fixed_proxy_factor` and `inflation_factor`, in the bound they check before
  a power (*Two compiler directives*, below). No other compiled cell calls `math`: the
  uncapped cap, `math.inf` in `RILA_US_S`, is `Data.cap_uncapped()`, a C double, and
  `RILA_US_S`'s `math.isinf(cap)` is `is_uncapped()`.
- **Operands in `RILA_US_S`'s order.** Compiled, a two-argument `max` or `min` evaluates its
  arguments right to left, so a point that reaches two refusals would raise the second's
  message. Each that takes two operands from cells, `cap_rate`, `step_rate`, `edge_rate`,
  `death_ben_pp`, `wd_behavioral_pp` and `wd_free_pp`, binds them to locals first, in
  `RILA_US_S`'s order; the inline prices keep the order of `RILA_US_S`'s raising calls too,
  the binary's discount before its `d1`, and `credit_rate_by` forms its accrual before its
  cover test, as `RILA_US_S` forms the argument before the call. No number moves: only the
  order the caches fill.
- **Reporting cells stay Python.** `model_point()`, the seven label accessors `policy_id()`,
  `sex()`, `crediting_type()`, `iv_family()`, `amort_rule()`, `scenario_id()` and
  `wd_schedule_id()`, and the four reports return a table row, text and DataFrames, for a
  reader, for `run_sec.py` and for the comparison with `RILA_US_S`. No other cell calls
  them, so they cost the projection nothing. A label accessor returns its column as read,
  and `Data` accepts a label that is not text: a blank or numeric `policy_id`, which no cell
  reads, a `crediting_type`, `iv_family` or `amort_rule` none of its decodes names, which
  the projection meets as `RILA_US_S` does, and a numeric `scenario_id` or `wd_schedule_id`
  where its table's keys are numbers. So each of those six compiles to a Python object, as
  the sample traces it (below), and returns what modelx returns; `sex()` compiles to `str`,
  since the mortality table's check admits no sex but `M` and `F`, and `sex()` refuses any
  other value itself, naming the point, so that it returns text or raises in either engine,
  which the typing guard asks of a label compiled to `str` (precised at M26). The three
  checks are reporting cells too, but they return a verdict, which compiles to a C `bint`.
- **Engine cells stay Python too.** The eleven cells of float parameters, `norm_cdf`,
  `bs_d1`, `bs_d2`, `bs_call`, `bs_put`, `bs_binary_call`, `opt_component`, `opt_portfolio`,
  `opt_portfolio_abs`, `credit_rate_at` and `opt_budget_at_cap`, are `RILA_US_S`'s formulas
  with its strings coded, kept for a reader, for `RILA_US_S`'s own tests, which call four of
  them, and for the twin identity, which compares the keys `RILA_US_S` caches in them, 5,170
  on point 1. `tests/us_registry.py` names them under `"engine"`, and the compile
  tests admit them, and no other cell, to a dictionary cache, a float parameter and the
  `math` module; no compiled cell may call one. `bs_d1` tests the volatility before it
  squares it (*What it refuses*, below), a change to `RILA_US_S`'s formula that moves no
  number.

Of `Projection`'s cells, compiling took away `opt_legs` and added eleven: `point_id`,
`mort_schedule`, `scenario_number`, `wd_schedule_number`, `opt_leg_count`, `opt_leg`,
`opt_component_at`, `opt_portfolio_at`, `opt_portfolio_abs_at`, `credit_rate_by` and
`cap_solved_at_start`, 202 in all. The Reference `idx`, 0, takes the place of `point_id`,
and `issue_age_min`, 0, `issue_age_max`, 111, and the 36 codes are new References. `Data`
has 81 cells, 14 at stage `E`, and its docstring lists its vectors, arrays and counts, each
with the column or file it comes from: 25 vectors of int64, by point, scenario or sex, and
28 of float64, by point, year or row; seven tables of float64, the five scenario columns,
the mortality and the programmes; and twelve int counts and extents and one double, the
uncapped cap, each read from a checked table. Its seven readers, `model_point_table()` among
them, and `input_dir()` stay Python, returning DataFrames and a path, and no `Projection`
cell but `model_point()` reads them. Every other cell of `Projection`, 190 of its 202, the
three checks among them, returns a C `bint`, `long long` or `double`, and all but the eleven
engine cells cache a single value, or a C array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,203 by `t`, of `double`, `long long` or `bint` | the 91 cells of `t` alone: every count, rate, factor, value, charge, claim and cash flow; the policy clock, its years, the attained age and the term clock; the flags `is_active`, `is_anniv` and `is_term_end`; the market at month `t`'s end and at its term's start; the cap solved once a term; and the checks' monthly residuals |
| a C array of 1,203 by 9 | the 25 cells of `t` and one code: `pols_if_at`, `inv_amt_pp_at`, `interim_value_pp_at`, `iv_notional_pp`, `fixed_proxy_pp`, `budget_amort_pp`, `deriv_proxy_pp`, `trading_cost_pp`, `fixed_acct_pp_at`, `holding_acct_pp_at`, `av_pp_at` and `av_at`, by `(t, timing)`; `pols_decr`, `claim_pp`, `claim_from_av_pp`, `claims`, `claims_from_av` and `claims_over_av`, by `(t, kind)`; `roll_to_acct_pp`, `wd_bucket_value_pp` and `wd_alloc_pp`, by `(t, bucket)`; `market_state`, by `(t, name)`; `opt_portfolio_at` and `opt_portfolio_abs_at`, by `(t, basis)`; and `credit_rate_by`, by `(t, rule)` |
| a C array of 1,203 by 7 by 9 | `opt_component_at`, by `(t, leg, basis)`, and `opt_component_pp`, by `(t, leg, timing)` |
| a C array of 1,082 by `m`, 122 by `a`, 93 by `y` or 92 by `cy` | `wd_amount_pm`, `mort_rate_base_at`, `lapse_rate_base_py` and `surr_charge_rate_at`, each its table's one reader |
| a C array of 9, 8 or 5 | `roll_share`, by bucket; `guar_min_rate`, by rate kind; and `opt_leg`, by leg number |
| one `long long`, `double` or `bint` | the 54 cells without a parameter: the point's label, numbers, decodes and join numbers, its opening state, its frame's ends and its term, its leg count, the shock year, the budget target, and the three checks |
| a C `double` with a dictionary for a cache | the eleven engine cells |
| a Python object | the twelve reporting cells, `sex()` a `str` |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and the eleven dictionaries among `Projection`'s caches there are the engine
cells'.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell the
run never calls compiles as a Python object. So `sample_sec.py` runs the four reports and
the three checks on every committed point, which reach every cell but these: `model_point()`
and the seven label accessors, which only a reader asks for; `point_id()`, which only a
refusal names; the eleven engine cells, which no projection cell calls;
`lapse_shock_year()`, `guar_min_rate` at a rate kind the point's crediting type does not
read, `roll_share` at each bucket, `opt_leg_count()` and `opt_leg`; and the cells and codes
no report reads: the fixed leg's yield and the implied spread, the free-withdrawal base and
allowance away from an anniversary, the pre-AG 54 rate on a priced family, the cap solve off
`nge_reset`, the option-pricing market at each month end, each leg on each basis, the
decomposition and each leg after the withdrawal, the opening notional, the balances after
the withdrawal, the block's Account Value before it, and the claims released from and paid
above the Account Value at every kind and `ALL`. The sample calls those too, the monthly
ones in every month of the frame and the month after it, each timed cell at every code of
its family, each kinded cell at its three kinds, each bucketed one at its three buckets, the
market at every name to the instant after that month, and the engine cells at the arguments
`RILA_US_S`'s own tests use. It projects the committed points alone: the export it runs
reads the CSVs of the directory the build is made in, and the trace it needs is the
committed points', which are what the tests project. The six free label accessors it calls
once more, on a copy of the table's first point with its four free labels blank and its two
keys, `scenario_id` and `wd_schedule_id`, the number 1, beside one-key copies of the
scenario and withdrawal tables keyed by 1, which it writes to a temporary directory and
reads by a second instance of the export, given the files' absolute paths. That types them
as Python objects, so that a blank or numeric label returns what modelx returns rather than
raising `TypeError` (*What compiling changed, and why*). The committed points leave branches
untaken: a Floor option at a one-year renewal under every family, a negative base under a
power, a power past the largest float, a market read before a scenario's first month. That
still types every cell, because every branch of a cell returns the one type its others
return, a rate a float in every branch and a code an int in every branch, and on points that
take those branches the compiled model computes modelx's numbers (above). A code a cell
refuses is not called: a raise types nothing. The sample also raises the recursion limit,
which modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and in
the month after it, `t = proj_len()`, which the roll-forwards read and the compile tests'
full sweep evaluates every monthly cell at; plus one because the index starts at 0, and one
of headroom:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,203 | 1,201. The longest frame is a contract issued at the youngest issue age, 0, covered to the Maturity Date, `max(maturity_age − issue_age_min, maturity_min_years)` = 90 years, 1,080 months, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: `t = 0 … 1,199`, and the month after, 1,200. The count's roll-forward residual and `av_at(t, AFT_WD)` answer 0.0 outside cover before they read `t + 1`, but the month's market is read at its end, so the five unguarded readers, `index_level` and the four beside it, read `market_state` at 1,201 when called at 1,200. `Data.read_last_mth` is the last `t`, 1,202, the headroom |
| `t`, and `timing`, `kind`, `bucket`, `name`, `basis` or `rule` | 1,203 by 9 | the nine timings of the one numbering, `BEF_NB` 0 to `AFT_WD` 8; inside them the kinds 0 to 3, the buckets 0 to 2, the columns 0 to 4, the bases 0 to 2 and the rules 0 and 1. Every 2-D cache has this one width. Cython's generated unpickle code converts a space's 2-D caches with one function for each inner width, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*). A code below 9 a cell does not take is then inside the cache, where the cell refuses it as modelx does, and a code from 9 raises `IndexError`, compiled alone |
| `t`, `leg`, and `timing` or `basis` | 1,203 by 7 by 9 | the seven legs, `ATM_CALL` 0 to `EDGE_BINARY` 6, by the width 9, one inner shape for both 3-D caches, for the same reason. A leg from 7 raises `IndexError`, compiled alone |
| `kind`, alone | 8 | `guar_min_rate`'s rate kinds, `CAP` 4 to `EDGE` 6, numbered after the claim kinds: 7 values from 0, and one of headroom |
| `bucket`, alone | 9 | `roll_share`'s buckets, 0 to 2, sized 9 all the same, the width of the 2-D bucket caches, since `roll_to_acct_pp` passes it every bucket its own cache holds: so a bucket 3 to 8 reaches `roll_share`'s refusal, `invalid bucket`, in both engines |
| `i` | 5 | `opt_leg`'s leg number, 0 to 3 on a Floor option, the widest, and one of headroom |
| `a` | 122 | 120, the attained age the last covered year is entered at, `max(maturity_age, issue_age_max + maturity_min_years) − 1`, read from age 0 by `mort_rate_base_at` in cover alone; plus one, and one of headroom. `Data.read_last_age` is the last `a`, 121 |
| `cy` | 92 | 90, the complete contract years at the month end of the last covered month on the longest cover, `max(maturity_age − issue_age_min, maturity_min_years)`, read by `surr_charge_rate_at` in cover alone; plus one, and one of headroom |
| `y` | 93 | 91, the contract year at that month end, read by `lapse_rate_base_py` in cover alone; plus one, and one of headroom |
| `m` | 1,082 | 1,080, the policy month end of the last covered month on the longest cover, read by `wd_amount_pm` in cover alone; plus one, and one of headroom |

`proj_len()` refuses a point issued below `issue_age_min`, 0, or above `issue_age_max`, 111,
one at or past maturity, and one whose sex the mortality table rates short of its cover or
past `Data.read_last_age`, in modelx as compiled, and cover ends at the Maturity Date, so no
report on a point the model projects runs past these caches. The bounds are `RILA_US_S`'s,
not the product's: `product-spec.md` issues from 0 to 85, but `RILA_US_S` projects any issue
age its mortality table rates for the cover, and refusing one would refuse a point stage `E`
projected (D2). On the shipped table, whose last age is 120, that is up to 111, whose
ten-year minimum cover is entered at 120 in its last year, so `issue_age_max` is 111, and it
sizes the age cache through `read_last_age`. 112 is refused, as `RILA_US_S` refuses it, with
a `KeyError` at attained age 121. `issue_age_min`, `issue_age_max`, `maturity_age`,
`maturity_min_years` and `Data.future_horizon_mth` are the contract the sizes are derived
from. Lower the minimum, or raise any of the others, and a report runs past the caches in
the compiled model alone: a frame of more than 1,200 months, an age past 121, a contract
year past 92 or a policy month end past 1,081 raises `IndexError`, naming nothing, where
modelx projects. Each needs the sizes derived again, as `spec_sec.py` derives them,
`Data.read_last_mth` and `Data.read_last_age` with them, and a rebuild. The shipped
mortality table starts at attained age 40, so a point younger than 40 in its first month on
the books is refused by `Data` first, naming it; the ages from 0 are the contract's, which
an extended table reaches.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it was
measured to change there. Here `cpow` reaches the powers of fifteen cells: the square of the
volatility in `opt_component_at`, `cap_solved_at_start` and the engine's `bs_d1`; the
moneyness factor's square in `lapse_iv_mult`; the monthly rates of both decrements, `1 − (1
− q)^(1/12)` in `mort_rate_mth` and `lapse_rate_mth`; the accounts' monthly accrual, `(1 +
i)^(1/12)` in `fixed_acct_pp_at`, `fixed_acct_pp`, `holding_acct_pp_at` and
`holding_acct_pp`; the budget target's discount, `(1 + y_e − spread)^(−T)` in
`opt_budget_target`; the fixed leg's yield, `(1 − beta)^(−1/T)` in `fixed_leg_yield`; the
interim value's rate adjustment, `[(1 + r_0)/(1 + r(t))]^tau` in `mva_factor`; the family
(c) discount, `(1 + r + spread)^(−tau)` in `fixed_proxy_factor`; and expense inflation,
`1.025^(t // 12)` in `inflation_factor`. Without `cpow` a compiler with C99's complex
numbers, gcc among them, computes a power of two doubles as a complex power, which can
differ from Python's float power in its last bits. With both directives and the flag every
compiled value agrees with modelx's bit for bit, and the compile tests hold each, by the
module's first line, by the compiler's command lines and, on x86-64, by the comparison
itself. On Windows MSVC compiles without the flag, since it emits no fused multiply-add for
x64 without `/arch:AVX2`, which setuptools does not pass, and the comparison is exact there
too: the inline Black–Scholes price holds many a product added to a third, each rounded
apart. On the same platforms as the flag the tool adds `-Werror=incompatible-pointer-types`,
so that gcc before 14, which only warns of a pointer of the wrong type, fails the build as
gcc 14 does: the error two cache widths give (*The sample and the spec*, above). MSVC
accepts two widths without a word, so on Windows the one width, and the one 3-D shape, rest
on a test that holds every 2-D and 3-D size in `spec_sec.py` to them (*Tests*, below).

A `**` is where the two engines would part. Python's `**` raises where it has no float to
give, and C's `pow` raises nowhere: a base of 0 under a negative power gives an infinity in
C, where Python raises `ZeroDivisionError`; a base below 0 under a power that is not a whole
number NaN, where Python returns a complex number; and a result past the largest float an
infinity, where Python raises `OverflowError`. So each power an input `Data` accepts, or a
moved Reference, can take there is guarded before it is taken, the same in both engines, and
refuses nothing `RILA_US_S` projects to a real number (*What it refuses*, below). The guards
are tests on C doubles, and `math.log`, admitted in the five cells that use it, only where
the base or the power is large: the bound is `y·log|x|` against `709.7827128933845`, `log`
of the largest float and a margin of `5e-13` above the error of the product, and a square's
base against `1.3407807929942596e154`, the largest float whose square is a float. Mortality
and the surrender rate need no guard: `Data` holds a mortality rate at 0 or more and the
cell caps it at 1, and `lapse_rate` is capped at `lapse_rate_max`, 0.5 as shipped, below 1,
which a Reference set above 1 passes and the monthly rate then refuses.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 6,385,368
bytes, about 6.4 MB, the type's basic size, which holds every cell's cache, each beside a
flag array of its shape that marks what is computed. The 25 2-D caches, 1,203 by 9, are 3.25
MB of it with their flags, half; the two 3-D caches, 1,203 by 7 by 9, 1.82 MB; and the 91
arrays by `t` 1.30 MB, nearly all the rest. Of the library's products only `VUL_US_SEC`'s,
7.8 MB, is larger: this is 1.9 times `FIA_US_SEC`'s, for nine timings, whose width every 2-D
cache takes, and the leg caches by basis and timing. As it stood after running in force the
model compiled to a struct of 1,301,576 bytes, its 36 caches by a string or a float
dictionaries. Making one costs time as well as memory: Python zeroes the struct when it
makes the ItemSpace, and making and releasing one, nothing computed, the runner's collection
included, took 1.17 ms here, of the 2.00 ms a compiled point takes (*Speed*, below).
Deleting it, `del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in
reference cycles, and only Python's cyclic collector frees it. That is why `run_sec.py
--block` collects after each release, in its frame pass and in its projections (*Run it*,
above), and a compile test holds a compiled block run to one point's ItemSpace at a time.
Without it, 504 compiled points peaked at 2,713 MB (*Speed*, below). A smaller struct would
need fewer timed caches, which would change `RILA_US_S`'s cells' call syntax, or per-basis
copies of the leg pricing; the struct is accepted, and reported here.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no limit
raised. What it needs is stack. The deepest call the contract allows, a cold `net_cf` in the
last month of the longest cover, issue age 0, 1,080 months from issue, issued now or 120
months on, runs the Investment Amount's chain back to `t_entry()`, 1,100 cells deep in
modelx, and 1,096 on the count's roll-forward residual, on `expenses` and on `pols_lapse`
(*Counts and timings*, above). Compiled with MSVC 14.37, on this machine, it runs on a
thread of 384 KiB of stack and dies on one of 320, issued now and 120 months on alike.
Windows rounds a thread's reservation up to 64 KiB, so the bytes a level were read from the
longest chain that runs at fixed reservations, a cold `net_cf(t)` on the point issued now,
found to five months: 327 months at 128 KiB, 555 at 192, 779 at 256 and 1,011 at 320, about
228 months more for each 64 KiB, 287 bytes a level, and about 31 KiB besides, so about 340
KiB at 1,100 levels. These are MSVC's figures. A test runs the call in a thread of 1 MiB,
the stack Windows gives a program's main thread unless the program is linked for more, and
again on the main thread, which is where `run_sec.py --cython` runs: three times the need.
gcc's frames are another compiler's, and its figures come from the `cython` CI job's Linux
leg, which runs the test there: the test first runs the call at a range of stacks, from 256
KiB to 2 MiB, and its warning reports the smallest it ran on. On `SPIA_US_SEC`'s chain that
leg took about twice the bytes a level MSVC took on this machine; at that ratio this chain
would need about 680 KiB on gcc, 1.5 times under 1 MiB: an estimate, until the Linux leg
records this one. A stack below the need kills its child on an overflow, by design; on
Windows the child ends with `STATUS_STACK_OVERFLOW`, and should Windows Error Reporting hold
it instead, the test waits a bounded time for each child rather than the job's hour. The
export recurses in Python instead: the same call needs a recursion limit of 2,213 there,
issued now and 120 months on alike, and the residual and `expenses` 2,205, and the four
reports and the three checks, which run in ascending `t`, need 154 on the committed points
with the export's import among the frames they run under, as the sample runs them, and 49
once it is imported, so `sample_sec.py` sets 9,000, four times the first rounded up to the
thousand, and a test holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot read for the whole table, when the array is first read, naming the
  table and its points or lines: what `model_point_table()` and the six count cells refuse,
  as at stage `E` (*The in-force interface*, above), their messages unchanged; and a label
  of the model point table that is not a whole number below `2**53` in size, from
  `Data.point_id`, when a label is first read, `model_point_table_sec.csv: point_id must be
  a whole number; [7.5] is not`.
- What a point's projection cannot use, by the accessor that reads it, naming the point, and
  no other point for it: a `term_years`, an `age_at_entry` or a `duration_mth` of `2**53` or
  more in size, which an int64 cannot be trusted to hold, `point_id 2: term_years must be
  below 2**53 in size; it is not`, on a term of `2**60` the floors table has a row for,
  while point 1 beside it projects. Stage `E`'s checks refuse every value that is not whole,
  out of its range, blank or text, as they did, so what reaches the accessors is the size
  alone, and only where the tables join it: a term the floors table has a row for, which
  `RILA_US_S` projects on Python's exact ints, a refusal it lacks; an age or a duration only
  at an attained age a one-row mortality table rates.
- A key beyond a table, by the one cell that reads it, naming the point, where `RILA_US_S`'s
  lookup raised: an attained age outside the point's sex's, or past `Data.read_last_age`,
  `point_id 1: the mortality table holds no rate at age 121`, from `mort_rate_base_at`,
  where `RILA_US_S`'s `.loc` raised `KeyError`; a month before the point's scenario's first,
  or past `Data.read_last_mth`, `point_id 24: its market scenario holds no level at month
  0`, on the row issued 13 months on, from `market_state`, where `RILA_US_S`'s `max()` of an
  empty list raised; a contract year below the lapse table's first, from
  `lapse_rate_base_py`; and a policy month end below 0 or past `read_last_mth`, from
  `wd_amount_pm`. No projection reaches any of them: `Data` refuses a point whose first
  month on the books its tables do not cover, and `proj_len()` one its mortality stops short
  for. A contract year past the charge schedule, and a month end a programme has no row at,
  are no charge and no withdrawal, as in `RILA_US_S`; and a table key far past any read, a
  scenario month of `2**60` among them, is held nowhere and refuses nothing (*What compiling
  changed, and why*), and a scenario row at month `2**60` beside point 1's leaves its
  projection as it was.
- By `proj_len()`, in this order: a point issued below `issue_age_min` or above
  `issue_age_max`, `point_id 12: age_at_entry 81 is above issue_age_max, 80, the oldest
  issue age the compiled model holds`, with the Reference lowered to 80; one at or past
  maturity at the valuation date; one whose sex the mortality table rates short of the age
  its last covered year is entered at, `point_id 12: the mortality table rates its sex to
  age 89, short of age 90, at which its last covered year is entered`, on a copy of the
  table ending at 89, where `RILA_US_S` raises pandas' `KeyError` at the first month that
  reads the age; one whose cover needs an age past `Data.read_last_age`, `point_id 12: its
  last covered year is entered at age 90, past read_last_age, 89, the oldest age the
  compiled model holds`, with `Data.read_last_age` lowered to 89, which only a mortality
  table extended past 121 and a raised `issue_age_max` reach; and, from the second contract
  year, a remainder above the year's Free Withdrawal Amount, as at stage `E`.
- A power its base takes off Python's real numbers, by the cell that takes it, in both
  engines, where `RILA_US_S`'s `**` raises or returns a complex number (*Two compiler
  directives*, above). A base of 0 under a negative power raises Python's own
  `ZeroDivisionError("0.0 cannot be raised to a negative power")`, in `opt_budget_target`,
  `fixed_leg_yield` and `fixed_proxy_factor`, never where `tau` is 0. A base below 0 under a
  power that is not a whole number raises `ValueError`, naming the point and what took the
  base there: in `fixed_leg_yield`, an option budget of 1 or more on a term longer than a
  year, which a declared rate and a market `Data` accepts can price; in
  `fixed_proxy_factor`, `iv_credit_spread` below `−1 − risk_free`; in the four account
  cells, `declared_acct_rate` and `guar_min_acct_rate` both below −1, `point_id 20:
  fixed_acct_pp(0): 1 + acct_rate, -0.5, is below 0, and its power 1 / 12 is no real number`
  at −1.5 each, where `RILA_US_S` raises `TypeError` comparing a complex number; and in
  `lapse_rate_mth`, `lapse_rate_max` above 1, `point_id 1: lapse_rate_mth(72): 1 -
  lapse_rate, -1.0, is below 0, lapse_rate_max being above 1, and its power 1 / 12 is no
  real number`, at `lapse_rate_max` 2 and a charge-expiry shock of 100 times, where
  `RILA_US_S` returns a frame of complex numbers. Under a whole-number power a negative base
  computes as in `RILA_US_S`, and so do `-0.0` and a power of 0. A power past the largest
  float raises `OverflowError`, naming the point, before it is taken: `point_id 1:
  inflation_factor(24): 1e+300 ** 2 is past the largest float`, at an `inflation_rate` of
  `1e300`, where `RILA_US_S`'s `OverflowError` carries the platform's message. Infinite and
  NaN operands are not checked, since Python's `**` answers them without a raise.
- A timing, a kind, a bucket, a leg, a basis, a column or a rule a cell does not take,
  `ValueError("invalid timing")`, `("invalid kind")`, `("invalid bucket")`, `("invalid
  leg")`, `("invalid basis")`, `("invalid name")` and `("invalid rule")`, where the code is
  inside the cell's cache: a code of another family, `pols_if_at(0, BEF_WD)`, `av_pp_at(0,
  BEF_NB)`, a claim kind passed for a rate kind, `guar_min_rate(DEATH)`, `ALL` passed to a
  cell of one kind, `claim_pp(0, ALL)`, a bucket 3 to 8, `roll_share(4)`, and a code up to
  8, `claims(0, 5)` or `market_state(1, 5)`; and a leg number past the crediting type's,
  `ValueError("invalid leg index")`, `opt_leg(3)` on a Cap option.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1203)` and `net_cf(-1)`, which modelx answers with 0.0, the month being outside
cover; `pols_if_at(0, 9)`, `claims(0, 9)`, `market_state(1, 9)`, `opt_component_at(0, 7,
CURRENT)`, `opt_component_pp(0, 7, BEF_ROLL)`, `opt_leg(5)`, `guar_min_rate(8)` and
`roll_share(9)`, which modelx refuses as an invalid code; `surr_charge_rate_at(92)`,
`surr_charge_rate_at(-1)`, `lapse_rate_base_py(93)` and `wd_amount_pm(1082)`, which modelx
answers with a number; and `mort_rate_base_at(122)`, `mort_rate_base_at(-1)`,
`lapse_rate_base_py(-1)`, `wd_amount_pm(-1)`, `market_state(1203, INDEX_LEVEL)`,
`market_state(-1, INDEX_LEVEL)` and `index_level(1202)`, which reads the market at 1,203,
which modelx refuses, naming the point and the key. No projection makes those calls. An
`idx` past the last row is refused in both, with an `IndexError` at the first read of a
vector, and `Projection[-1]` reads every vector at its last element in both, so it is the
table's last point, under that point's own `point_id()`, 24.

A Reference is a C variable of its value's type: `issue_age_min`, `issue_age_max`,
`maturity_age`, `maturity_min_years`, `nge_solve_iter`, `db_rop_max_issue_age`, the codes
and `idx` a `long long`, as `Data.future_horizon_mth`, `Data.read_last_mth` and
`Data.read_last_age` are, and the rates and amounts a `double`. Set past that type, it is
converted when it is set, where modelx keeps the value as given. A float set on an int
Reference is truncated toward zero without a word, `maturity_age = 120.7` reading 120, so
that point 2's `proj_len()` is 720, where modelx computes with the float, 728.4. A text, a
NaN or an int beyond 64 bits is refused at once, with `TypeError`, `ValueError` or
`OverflowError`: `ALL = "x"` a `TypeError`, where modelx refuses `claims(0, ALL)` as
`invalid kind`; `issue_age_max = float("nan")` a `ValueError`, where modelx projects point
1, every comparison with NaN false; and `issue_age_max = 2**70` an `OverflowError`. An int
set on a `double` Reference reads as a float compiled, `declared_acct_rate = 2` giving
`acct_rate()` 2 in modelx and 2.0 compiled. Each shipped Reference is a value of its C type,
so no shipped number differs. A Reference set past its domain meets the guards above, the
same in both engines; the one place they part is a power whose result lies within about
`1e-12` relative above the largest float, which the logarithm's bound lets through: there
modelx's `**` raises Python's `OverflowError`, with the platform's message, and the compiled
model raises this model's, after the power, its result an infinity, so that neither returns
one. No input reaches it but by construction.

Mortality is capped at 1, as in `RILA_US_S`, by `min(q × mort_ae_factor, 1.0)`, the bound
second, and the annual surrender rate at `lapse_rate_max`, as `RILA_US_S` writes it; the
compiled model computes each as comparisons in the same order. So a NaN sent through a
Reference, `mort_ae_factor`, stays NaN at the cap in both engines, and the roll-forward
check it reaches fails, in both.

### Speed

`python tools/bench_sec_cy.py registered_index_linked_annuity` builds the model into a
temporary directory, or takes a build with `--build`, and times one block run on three
engines: modelx, the export and the compiled model. Each engine runs the committed table
repeated, in a process of its own, as `run_sec.py --block` runs a block, each point
projected and then released. The scenarios are keyed by scenario, not by point, so every
copy of a point reads its own row's scenario. `net_cf` is `net_cf(t)` summed over the frame,
the projection alone, as `basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf`
is the report `run_sec.py` prints, which builds a DataFrame for each point. Each time is the
fastest of six runs, two benchmarks of three, with the spread of all six in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,000 | 2.00 ms (12.02–13.41) | 2.36 ms (14.16–17.28) | 93 MB |
| export | 600 | 8.33 ms (5.00–5.15) | 8.20 ms (4.92–5.50) | 82 MB |
| modelx | 120 | 167 ms (19.98–25.71) | 164 ms (19.67–23.46) | 148 MB |

The benchmark was run twice, straight after each other on the same build, three runs of each
engine and loop each time; the table gives the fastest of the six, and the spread of all
six. On `net_cf` the compiled model runs 4.2 times its export, and on `result_cf`, where
building the DataFrame takes part of its time, 3.5 times; it runs 83 and 69 times modelx.
Each run alone gave the compiled model 2.00 ms on `net_cf` and the export 8.33 and 8.35 ms.
That is the lowest ratio to the export of the library's products, against 9.5 for
`Term_US_SEC` and `SPIA_US_SEC`, 11.1 for `FIA_US_SEC` and 17.3 for `IUL_US_SEC`, and the
struct is why: of the compiled model's 2.00 ms a point, making and releasing the ItemSpace,
which Python zeroes, takes 1.17 ms (*What a compiled run needs*, above), where the export's
ItemSpace holds dictionaries that start empty. Of the rest, the `math` calls the two pricing
cells make into Python take about 0.4 ms: on a prototype of this model, not shipped, C's
`libm` in their place ran 1.65 ms a point against 2.04, over the committed points repeated
25 times (*What compiling changed, and why*). As it stood after running in force, compiled
the same way, the model ran 1.01 times its export (above, measured on a build not shipped,
so not reproducible from the repository), and the compiled model runs 68 times that build on
the same measure, 1.94 ms a point over the committed points repeated five times against
132.2: the representation, not the compiler, is the gain, and the export gained from it too,
8.23 ms a point against 134.0. The release keeps a block flat: the compiled model's peak
grew by 2.2 MB at most over its 6,000 points, and without the collection after each release
(`--no-collect`), 504 compiled points peaked at 2,713 MB. Reading the seven files and
building every `Data` vector and array for those points took 0.047 s, and asking every point
for its frame, the runner's first pass, 6.7 s, nearly all of it making and releasing an
ItemSpace a point. Every engine, loop and run summed `net_cf` over a copy of the table to
−1,057,592.027.

Measured on 2026-11-14 on a desktop shared with other work: 12 cores and 20 threads (an
Intel Core i7-12700KF), 64 GB, Windows 11; Python 3.13.18, its extensions compiled by MSVC
14.37 (Visual Studio 2022), with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1, numpy
2.5.4 and pandas 3.1.1. Windows reports no load average: sampled every 10 seconds over both
runs, the processors were 6 to 39% busy, half the time 10% or less, of which the benchmark's
own process, one thread, is 5 points; another session's build and tests of this model ran
beside it. Each time is the fastest of its runs; the fastest run is the one to compare. The
comparisons over the committed points, with the build as it stood after running in force and
with the prototype, are the fastest of two runs of three loops each, in a process an engine
and run, the processors 2 to 22% busy, and so is the cost of an ItemSpace, the fastest of
five rounds of 1,000.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 15, issued at
  the valuation date, every cell of `RILA_US_S`'s agrees at every argument `RILA_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`,
  whose meaning changed. So the goldens `tests/test_registered_index_linked_annuity_us.py`
  asserts on cells that sweep reaches — the notes' interim value table to the cent, the
  option budget and the fixed leg's yield, the term-end identity for every crediting type,
  the pre-AG 54 worked example and the [S2] withdrawal charge example among them — hold
  here with no number restated. The identity holds on any count, since `RILA_US_S` already
  takes the purchase payment and charges acquisition on the contracts issued. The same
  suite holds the model to the conventions every `_SEC` model meets: every frame starts at
  `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The splice**, in `tests/test_registered_index_linked_annuity_us_sec.py`: each
  `RILA_US_S` point restated in force at months either side of its events continues the S
  projection, in its four reports, frame by frame, and in every other cell the two share, at
  every argument S evaluates from that month on, to 1e-9 relative with no absolute floor,
  the roll-forward residuals apart, which are rounding around 0 and keep a floor of 1e-9; it
  skips the cells the twin identity skips, `proj_len`, a frame on the valuation clock, and
  `scenario_id`, which names the row's own copy. The months are those the product's events
  need: either side of each Term End Date and renewal, 11 and 12 and 23 and 24 on a one-year
  term, 35 and 36, 59 and 60, 71 and 72; months mid-term; the anniversaries, with the year's
  base read from the opening state or from the frame; the months around each withdrawal; a
  month after a renewal under `nge_reset`; and the last covered months. So do ten variants
  of S's points, in a copy of S's table that is never committed, for what S's own points do
  not reach: a three-year term; a one-year term under `nge_reset`, re-solving its cap every
  year; a behavioural rate above the free rate, which the allowance binds; a Floor option
  whose cap binds; a crash path, whose interim value falls below 0, and on it a behavioural
  rate above the free rate and a positive request on a negative Account Value; a withdrawal
  above the Account Value, which leaves nothing held; an Edge term ending exactly at its
  buffer, where the Edge rate is credited; and a withdrawal at a negative interim value on a
  positive Account Value, which the accounts alone pay, the option's share floored at 0.
  Each spliced row runs on its own copy of its scenario, re-based to its month, and S's
  paths are replaced in both models by paths that step in every field, the index, the Market
  Value Rate, the risk-free rate, the dividend yield and the volatility, so that a term's
  start read from the current market reads another number; and a row valued mid-term runs on
  a copy whose state at `t = 0`, which month 0, valued at `t = 1`, never reads, is moved off
  the row's term-start columns, so that a term's start read from the scenario at the
  valuation date does too. Inflation, on the valuation clock, is set to 0 in both models;
  the assumptions that ship at zero, the Holding Account's share of the roll split and the
  premium tax, are switched on in both, References that ship equal are set apart, and bounds
  that bind nowhere as shipped are made to bind, so that a term read in the wrong place
  reads another number.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every opening-state column, every kind of
  valuation month and every binding floor, cap, clamp and branch a test lists, and which run
  every line of the model the full grid runs, as measured at M10. The other cases carry the
  `sec_full` marker and show as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set.
  One leg of the CI matrix sets it, so every CI run runs the full grid too.
- **Future new business**: issued 13 months after the valuation date, more than a year on,
  seven of S's points and seven of the variants are each the S projection moved on, with
  zeros before issue in every report, its own copy of its scenario, which holds no level
  before issue, and no decrement rate evaluated nor table read before issue; and so are the
  anchor issued a month on and at the horizon, 120 months on.
- **How it computes**: on every row the splice and the future business compare, no cell has
  been called at a negative month, none evaluated from `t_entry()` on has read a month
  before it, and none evaluated at month `t` has read a month later than `t + 1`, directly
  or through a cell keyed by no month; and no table reader has been reached from a month
  outside cover. On a fresh read of the committed model the policy clock is a closed form,
  every point is swept under a lowered recursion limit, which a recursion backward over the
  frame would exceed, and a cold last-month call runs at most one cell a month back to
  `t_entry()`, plus a fixed overhead, on six of the committed points, two twins, three rows
  in force, point 19, the deepest, among them, and the row issued later, and at issue age 0.
- **Counts, validation and regeneration**: the count rolls forward through new business and
  decrements, and `pols_if_at` refuses a timing it does not have; `result_pols()` is
  `RILA_US_S`'s, column for column, with `pols_new_biz` beside it; multiplying
  `policy_count` by 2.5, a count that is not whole, multiplies every counted cell and moves
  no per-contract value, and at 10^8 contracts both roll-forward checks close on their
  scaled tolerance, each residual above the fixed tolerance it would have had. Each
  malformed row is refused naming its point, by the one rule under test, on a model read for
  it and again through a projection; so is each assumption table whose keys or values cannot
  be read, naming the file and the lines, and each point at or past its Maturity Date or
  carrying a remainder above the year's allowance, by `proj_len()`, each rule refused at the
  first month it reads; an unknown crediting type, interim value family or amortization rule
  is refused where the model first reads it; the edges of each rule are accepted, a renewal
  valuation with every amount carried to the cent and `nge_reset` written 1 or 0, or 1.0 or
  0.0, among them, and so is every state `RILA_US_S` reaches on the splice's inputs,
  restated at its anniversaries, its renewals and its years' last months among others, but a
  contract a full withdrawal has emptied; keys written as floats are read by value; the
  horizon is a Reference, which at 0 refuses any future business, saying so; and the
  committed table and scenarios are what `RILA_US_S` generates, and each derived and future
  row in them, projected at the shipped assumptions, is its `RILA_US_S` point from its month
  on, frame by frame and cell by cell, but for what expense inflation moves.
- **The opening state and the rest**: each derived row's opening state is what `RILA_US_S`
  carries into its month, and each column, changed, moves a committed row where it is read;
  a term begun before the valuation date reads its start from the row, a renewal at the
  valuation date reads its start and its cap from the scenario, and a re-solved cap is read
  until the next renewal; the year under way reads its free-withdrawal state; withdrawals
  stay on the policy clock and the market runs on the valuation clock; expense inflation
  runs on the valuation clock at the shipped 2.5%, which only this test sees, since the
  splice sets the rate to 0; acquisition and the purchase payment fall on new business
  alone; where the cap on mortality binds, both models' annual and monthly rates are the
  float 1.0, the count is 0.0 after, every cell agrees with S, and a NaN A/E factor stays
  NaN; each check fails a residual that is not a number, sent through a Reference set
  before the model computes anything; every guarded cell holds its value outside cover;
  the points of a block sum row by row; an extract without the generator's three columns,
  relabelled, projects the same numbers; `run_sec.py` prints the model's numbers; and the
  docstrings describe the valuation clock.

- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest absolute value and its values at five months,
  and the model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py RILA_US_SEC
  --check` makes the same comparison. The tests above held through the compile step with
  their call syntax changed: a point's position for its label, the codes for the text of a
  timing, a kind, a bucket, a leg, a market or a column, and `ALL` for `RILA_US_S`'s `None`.
  Each point is named by its label, in `point_id()`, in a refusal and in `run_sec.py`'s
  output.
- **What compiling changed**, held in modelx in every run: each int a point's projection
  reads of `2**53` or more in size, a `term_years`, an `age_at_entry` or a `duration_mth`,
  is refused by the point's own accessor, naming the point, while every other point projects
  the committed numbers; a point issued below `issue_age_min` or above `issue_age_max`, one
  whose sex's mortality stops short of its cover and one whose cover needs an age past
  `Data.read_last_age` are refused by `proj_len()`, in that order, naming the point, and
  each projects once its bound is moved back; each power off its domain is refused in both
  engines, beside `RILA_US_S`'s own outcome, a complex number, a `TypeError` or Python's
  `ZeroDivisionError`, and each computes on the other side of its bound; the int-keyed
  pricing cells are the engine cells' floats by `float.hex` on every committed point and
  month, and on two points under `nge_reset` that solve a one-year cap fifty times on a
  market that steps each year, `opt_component_at` at each leg and basis, the two portfolios,
  `credit_rate_by` at both rules and `cap_solved_at_start` against a loop over
  `opt_budget_at_cap`, and `sqrt 2` is the double `math.sqrt(2.0)` returns; the cap is
  solved once a term, keyed by the term's first month on the books, and is `RILA_US_S`'s in
  every month of the term; `opt_leg` names `RILA_US_S`'s `opt_legs()` on every twin;
  `claims(t, ALL)` and `claims_over_av(t, ALL)` are `RILA_US_S`'s by `float.hex`, at three
  negative zeros too; with the Holding Account's share of the roll split at 5%, where
  Neumaier's sum and a running one part, every cell is `RILA_US_S`'s; the scenario,
  programme and sex numberings follow the keys on files written out of key order, read
  twice; each decode compares the text exactly, as `RILA_US_S` does, a value in another case
  or beside a space being no flag; the arrays are NaN where no read reaches, and each array
  is as wide as its last month or age and one more; every `Data` cell but the readers is the
  int64 or float64 array, or the int, or the double `cap_uncapped`, that the `Data`
  docstring's table states; every parameterless projection cell returns a Python number;
  each size in `spec_sec.py` is the one its comment derives from the model's References,
  every 2-D cache one inner width and both 3-D caches one inner shape, and
  `Data.read_last_mth` and `Data.read_last_age` the spec's last `t` and `a`; the sample's
  recursion limit is the one its comment derives, the sample calls the six free labels on a
  second instance, and it calls each of the eleven engine cells; `run_sec.py`'s running sum
  of a block is `groupby`'s, bit for bit; `run_sec.py --cython` rebuilds in place exactly
  when a source is newer than the build; and outside the repository, beside a copy of the
  model, it says it cannot build.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting and engine ones refers to pandas, numpy or another module, reads
  a table with `.loc` or the like, calls a reporting cell, holds text but in its docstring
  and its refusals, or holds a generator, a comprehension or a nested function; none calls
  anything but a cell, a `Data` vector and the builtins of *What compiling changed, and
  why*, and the registry admits `math.erf`, `math.exp`, `math.log` and `math.sqrt` in the
  two pricing cells and `math.log` in five more, each by its dotted name, each call the sole
  argument of a `float(...)`, and each admission taken; every cell the registry names an
  engine cell takes a parameter no spec size names, and no compiled cell calls one; every
  `Data` vector a formula reads is an int64 or float64 array, read by element; no cell is
  uncached; and each label accessor returns its point's column on every point.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting and engine ones a C
  `bint`, `long long` or `double` and a C-array cache of exactly the spec's size, and every
  new `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps
  no Python object among a projection cell's locals, calls no Python builtin there, and
  builds no container, under both directives (C3); on the committed points, every cell at
  every argument a full modelx sweep caches is what modelx computes, bit for bit on x86-64,
  and so is every raise and every `Data` array (C4); and `run_sec.py --block`, run compiled,
  holds one point's ItemSpace at a time. In
  `tests/test_registered_index_linked_annuity_us_sec.py`: the same comparison on the splice
  grid, the core by default and the full grid with `USLIB_SEC_FULL=1`, a chunk of rows at a
  time; at the contract's extremes, issue age 0 issued now and 120 months on, on mortality
  extended below 40, issue age 111, a one-row frame, a Floor option at a one-year renewal
  under each interim value family, the uncapped option, the pre-AG 54 engine and
  `updated_expiry`; where the cap on mortality binds, and under NaN References; at the Step
  and the Edge exactly at their boundaries at a term end; with the Holding Account's share
  at 5%; on blank and numeric labels; on keys written as floats, in reverse order, and on
  table keys far past any read, which are held, not refused; and on each power off its
  domain. The total of three negative zeros keeps `RILA_US_S`'s sign, compiled. The compiled
  model refuses what modelx refuses, with modelx's message, on an extract labelled otherwise
  than by position, every refusal of the module among them, and an argument past a cache,
  either side, raises `IndexError`; the deepest call the contract allows runs cold on a 1
  MiB stack and on the main thread, and the test reports the smallest stack it ran on,
  waiting a bounded time for each; a Reference set after the model has computed changes no
  value it has cached; and `run_sec.py --cython` prints what `run_sec.py` prints, for a
  point and for the block, and refuses a directory that holds no build. They are marked
  `cython`, and they skip without the toolchain, but in the `cython` CI job, which installs
  it on Linux and on Windows, one leg a product, a skip fails, whatever made it.

```bash
python -m pytest tests/test_registered_index_linked_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_registered_index_linked_annuity_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k RILA_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k RILA_US_SEC
python -m pytest tests/test_registered_index_linked_annuity_us_sec.py -q -m cython
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-registered_index_linked_annuity-r2
[std]: #uslib-std
<!-- END generated citation links -->
