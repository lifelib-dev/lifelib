# In-Force Implementation Notes

**Status:** Draft, 2026-11-02. `SPIA_US_SEC` is [`SPIA_US_S`](model.md) taught to project
from a valuation date. Besides annuities whose annuity date is that date, it takes
contracts already in payment there, and annuities commencing in the ten years after it,
as lifelib's `basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is the
one [`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `SPIA_US_S` on another time axis, and it reads `SPIA_US_S`'s assumption tables in place,
> every assumption unchanged. The contractual elements — the five payout forms, the two
> survivor-reduction triggers, the fixed compound COLA, the cash-refund and
> installment-refund definitions and the commutation surrender-charge scale — are sourced
> from the composite's product documents [S1] [S2] [S3] [S5]. Everything else is a
> **[std]** standardization, among them the mortality table and the improvement scale,
> which are illustrative stand-ins for the 2012 IAM Basic table and Projection Scale G2,
> the expense and commutation assumptions, and the initial income `B(1)`, which is an
> exogenous input because no insurer publishes payout factors. Replace them with company
> data and a real quote before drawing any conclusion from the numbers.

## Run it

```bash
python products/immediate_annuity/run_sec.py            # point 1: the anchor cell
python products/immediate_annuity/run_sec.py 16         # the anchor in payment 14 months
python products/immediate_annuity/run_sec.py --block    # every model point, summed
python products/immediate_annuity/run_sec.py 16 --cython  # point 16 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about a minute,
and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer than the
build, and says so on stderr. `--build DIR` runs a build made elsewhere instead (*The
compiled model*, below). Nothing a build leaves is committed, and `.gitignore` covers it.

The first prints the fifteen rows `run.py` prints for `SPIA_US_S`'s point 1, the worked
example's anchor cell commencing at the valuation date, every column the same, with the
counts, survival and payment factors behind them. The second prints the same cell in
payment 14 months, the month after its joint annuitant's death. It pays 343.33 a month from
`t = 0`, two thirds of the 515.00 the COLA has reached, as `SPIA_US_S` pays in its month
14, and 353.63 from `t = 10`, its second anniversary. Its expenses are in valuation-date
dollars, 5.00 a month where `SPIA_US_S`'s month 14 carries 5.125, a year's inflation more,
and `liability_cf` and `net_cf` move with them. Three lines to the same thing for point 16:

```python
import modelx as mx
model = mx.read_model("products/immediate_annuity/SPIA_US_SEC")
model.Projection[15].result_cf()     # point 16, the table's sixteenth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[15]` is point 16, and its `point_id()` says so. `result_cf()` has
`SPIA_US_S`'s seven columns — `pols_if`, `annuity_payments`, `claims`, `commutations`,
`expenses`, and the gross outgo under both signs, `liability_cf` and `net_cf` — with one row
per month from the valuation date, `t = 0 … proj_len() − 1`. `result_pols()` sets out what
lies behind it on the same rows: `pols_if` and `pols_new_biz`, the annuities commencing in
the month, then `SPIA_US_S`'s survival and payment-factor columns in `SPIA_US_S`'s order,
the survival read at the end of each month, and every column 0 before an annuity commences.

`--block` asks every point for its frame before it projects any, then projects each and
releases its ItemSpace once its frame is read, so the run holds the cells of one point at
a time. Deleting it, `del model.Projection[idx]`, is not enough: an ItemSpace sits in
reference cycles, which only Python's cyclic collector frees, so the runner collects after
each release. It freezes everything alive (`gc.freeze()`) once the model and its table are
read, and again once it has asked every point for its frame, so that each collection scans
only what the block has made since. It keeps the block's sum as it goes, compensated as
pandas sums a `groupby`, so that the block is, bit for bit, the frames concatenated and
summed by `t`, as below. The shipped table is a set of test cases standing at different
calendar dates (*Two clocks*, below), so the block shows how the frames add, and nothing
more.

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however long the contract has been in payment,
  month `t` runs from time `t` to time `t + 1`, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the stop rule. Survival is indexed by a **time point** on this clock:
  `lives_if(t, life)` and `lives_if_last(t)` are survival *at* time `t`, the start of
  month `t`, so the deaths of month `t` are `lives_if(t, life) − lives_if(t + 1, life)`
  and an arrears instalment is paid on survival to time `t + 1`, as in `SPIA_US_S`.
  `SPIA_US_S` calls that argument `k`, on its one clock; here it is `t`, because survival
  is carried forward from the valuation date.
- **`duration_mth(t)`, the policy clock**, counts the months elapsed from the annuity date
  at the start of month `t`: `duration_mth(t) = duration_mth_init() + t`, with
  `duration_mth_init()` read from the model point. It is the technical notes' month index,
  and the contract runs on it: `duration(t) = duration_mth(t) // 12`,
  `policy_year(t) = duration(t) + 1` and `age(t, life) = age_at_entry(life) + duration(t)`,
  as in `SPIA_US_S`, and through them the payment months, the COLA anniversaries, the
  certain period, the commutation months and the surrender-charge year. A cell keyed on
  this clock takes `k`, a policy month or the time point that opens it, or `y`, a policy
  year: `is_payment_pm(k)` and `annuity_pp_sched_pm(k)` are the payment schedule by
  policy month, `annual_income(y)` the income by policy year, and `cum_annuity_pp(k)`, the
  notes' `G(k)`, the instalments scheduled before the time `k` months after the annuity
  date, so the notes' `G(13)` reads as they write it. The two table readers,
  `mort_rate_base_at(x, life)` and `improvement_rate_at(x, life)`, take an attained age,
  `x`. `BasicTerm_SE` reaches the policy clock by adding one a month, a recursion as long
  as the frame; the closed form needs no such chain of calls.

The **stop rule** ends every frame where it ends `SPIA_US_S`'s. `stop_mth()` is
`SPIA_US_S`'s frame length from the annuity date, `max(horizon_mths(), certain_mths_eff())`:
the notes' age stop on the youngest covered life, or the end of the certain period if that
is later. A month is in the contract's frame when `0 ≤ duration_mth(t) < stop_mth()`,
which is `is_active(t)`, and the frame ends with the last such month,
`proj_len() = stop_mth() − duration_mth_init()`. A contract's own end, its last death or
its last certain instalment, is a probability or a floor reaching zero inside the frame,
which runs on with zeros, as `SPIA_US_S`'s does.

Point 16 is the worked example's anchor cell in payment 14 months. At `t = 0` it is in
policy year 2, at attained ages 66 and 63, and its joint annuitant has been dead since the
end of policy month 13, the worked example's month of death. Its next COLA anniversary,
policy month 24, falls at `t = 10`, and its frame has 682 rows, `t = 0 … 681`, to the
anchor's last month, policy month 695. Point 22 is the anchor cell on the table basis
commencing 13 months after the valuation date: `duration_mth(0) = −13`, it is on the books
from `t_entry() = 13`, rows 0 to 12 are zeros, `policy_year(0)` is −1, and its frame has
709 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the payment months and the instalment schedule, the COLA anniversaries, the certain period and an installment refund's derived period and final trim, the payments to date, the scenario's months of death, the attained ages that key the mortality table and the improvement scale, the calendar year that dates the improvement, the commutation months, the utilization and the surrender charge by contract year, the age stop rule | expense inflation, `inflation_factor(t) = 1.025^(t // 12)` |

Expense inflation alone runs on `t`. `SPIA_US_S`'s annual steps, `(1 + π)^(y(t) − 1)`, keep
their shape and move onto the valuation clock, so the maintenance charge is in
valuation-date dollars for every point alike and steps on each anniversary of the valuation
date. The commutation discount rate reads neither clock: it moves with the 10-year CMT's
change since the annuity date, on one path of the CMT that every point shares. For a
contract on the books at the valuation date that is the change to the valuation date, an
opening-state column, plus `cmt10_shift`, a change made at the valuation date; a contract
commencing later, bought after it, has seen none (*The opening state*, below). A path of
the 10-year CMT would be read on the valuation clock, each contract taking the change on it
from the later of its annuity date and the valuation date. There is no acquisition cost in
either model: the premium is single and the cost is priced in.

**Mortality improvement stays on the policy clock**, because it is already dated by the
calendar. Its exponent is `calendar_year(t) − mort_table_year`, and
`calendar_year(t) = annuity_year() + duration(t)` is the calendar year the contract
reaches, whatever the valuation date. So a contract in payment reads the improvement of its
own calendar years, and nothing is re-based: restated from `SPIA_US_S` at month `d`, its
month `t` is `SPIA_US_S`'s month `d + t` and the same calendar year, and point 20's
`mort_rate(t, life)` is `SPIA_US_S`'s point 9's at `24 + t` exactly. Moving it onto the
valuation clock would need a calendar valuation date, which the model point table does not
carry, and would step a generational basis on the valuation date's anniversaries rather
than the contract's.

That has a consequence for the shipped table. Every row keeps the annuity year of the
`SPIA_US_S` point it was taken from, 2026, so the rows are test cases standing at different
calendar dates at their common `t = 0`: the twins at their annuity date, point 16 fourteen
months later, point 22 thirteen months earlier. A real block carries each contract's actual
annuity year, and its points then share one valuation date.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf()
          for i in range(len(model.Data.model_point_table()))]
block = pd.concat(frames).groupby(level="t").sum()
```

On a point commencing at `t = 0` the two clocks coincide, and the model computes what
`SPIA_US_S` computes, whatever the point's count: neither model charges acquisition, and
every cash flow is the count times an amount per contract. On `SPIA_US_S`'s fifteen points
every cash flow and every count agrees, and so does every other cell the two models share
but three whose meaning changed: `pols_if_init()`, now the count already in payment at the
valuation date, 0 for such a point; `model_point()`, a row of another table; and
`result_pols()`, which gains `pols_new_biz` and sets `pols_if` first.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `SPIA_US_S`'s columns,
and six of its columns are the in-force interface: `basiclife/BasicTerm_SE`'s two, and
four that open a contract's state. Every amount is per contract.

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | contracts, not necessarily whole | for a point in payment, the start of month 0, before any month-0 event; for any other, the month its annuity commences | the contracts the point stands for: in payment at the valuation date, or commencing at or after it. A count of contracts on the books, never weighted by survival |
| `duration_mth` | whole months | the valuation date | the months elapsed from the annuity date: positive in payment, 0 for an annuity commencing at the valuation date, `−k` for one commencing `k` months later, with `k` at most 120 as shipped |
| `lives_if_init_1` | a probability, 0 to 1 | for a contract in payment, the valuation date, the start of month 0, before any month-0 death; for any other, the annuity date, where each covered life is 1 | the primary annuitant's survival: 1 or 0 on a real record |
| `lives_if_init_2` | a probability, 0 to 1 | the same | the joint annuitant's survival; 0 on a single-life contract |
| `commute_frac_cum_init` | a fraction, 0 or more and below 1 | the start of month 0, before any month-0 withdrawal | the cumulative fraction of the certain instalments the owner has commuted before the valuation date, the notes' `θ_cum`, as it applies to month 0's instalment |
| `cmt10_shift_init` | a change in a rate, as a decimal: 0.005 for a rise of 50 basis points | the valuation date | the 10-year CMT at the valuation date less the 10-year CMT at the annuity date, which moves the commutation discount rate one for one; 0 for a contract commencing at or after the valuation date |

At the annuity date each covered life is 1, the fraction 0 and the CMT's change 0, so a
point commencing at or after the valuation date carries those values, and the twins carry
`SPIA_US_S`'s own: 1 and 1 on a joint contract, 1 and 0 on a single-life one, no
commutation and no change. Where `WholeLife_US_SEC`'s opening state is 0 at issue, an
annuity's survival opens at 1.

The count is a count of contracts, not of lives. A joint contract whose two annuitants have
died inside its certain period is one contract on the books, with both its lives at 0, and
is still paying. Survival is carried by the two life columns alone: the lives are
independent, as in `SPIA_US_S`, so their two probabilities are the whole survival state,
which a count weighted by survival could not carry. On a real record each life is 1 or 0,
and a joint contract may carry one life already dead; a death that has happened but has
not reached the record carries 1, and the model then projects that life as alive, as the
record does. Restated from `SPIA_US_S` at month `d`, each is `SPIA_US_S`'s probability,
`lives_if(d, life)`. The commutation fraction is what the owner's withdrawals have taken
from every certain instalment still to come: each withdrawal `W` at a commuted value `CV`
raises it from `θ` to `θ + (1 − θ) W / CV`, as in `SPIA_US_S`, and during the certain
period month 0's instalment is the scheduled one times `1 − commute_frac_cum_init`, so a
record of the instalment now paid gives the column as one less the ratio of the two. The
CMT's change is a fact of the market, not of the contract's history: the 10-year CMT on the
valuation date less the 10-year CMT on the contract's annuity date, the same for every
contract bought on one date, from a published series.

| `SPIA_US_S` | `SPIA_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in payment at the valuation date, 0 for a point commencing at or after it |
| — | `duration_mth` | The policy clock, in months. `SPIA_US_S` projects every contract from its annuity date |
| — | `lives_if_init_1`, `lives_if_init_2` | `SPIA_US_S` opens every contract with each covered life alive, `lives_if(0, life) = 1` |
| — | `commute_frac_cum_init` | `SPIA_US_S` opens every contract with no commutation taken, `commute_frac_cum(0) = 0` |
| — | `cmt10_shift_init` | `SPIA_US_S` reads the CMT's change since the annuity date from one Reference, `cmt10_shift`, which every point shares because every one commences at its `t = 0`. Contracts in payment bought at different dates have seen different changes, which one Reference cannot hold |

Two things `SPIA_US_S` computes from the annuity date need no column. The payments to
date, which a cash refund nets and an installment refund counts against the premium, are a
deterministic schedule fixed at the annuity date, and the model sums them on the policy
clock (*The opening state*, below). The certain months left are
`certain_mths_eff() − duration_mth`, and none once `duration_mth` reaches the certain
period.

The columns carried over are read as `SPIA_US_S` reads them. For a contract in payment, the
facts they record are those of the annuity date:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `premium` | dollars, the single premium | the annuity date: a pricing input, which the projection reads only as the refund forms' guarantee |
| `premium_tax_rate` | a rate | the annuity date; reported in `premium_net_pp()`, which no cash flow reads |
| `annual_income` | dollars a year, `B(1)`, the unreduced income of policy year 1 | the annuity date: exogenous, and fixed then |
| `form`, `joint`, `survivor_pct`, `reduction_trigger` | the payout form and the survivor terms, as in `SPIA_US_S`'s table | the annuity date |
| `certain_months` | a count of months from the annuity date, 0 for none | the annuity date |
| `frequency`, `timing` | payments a year, 12, 4, 2 or 1; `arrears` or `advance` | the annuity date; the payment months fall on the policy clock |
| `cola_rate` | a rate a year, compound | the annuity date; the income steps on each anniversary of it |
| `primary_age`, `joint_age` | years, age nearest birthday | the annuity date, not the valuation date: `age(0, life)` is the attained age there |
| `primary_sex`, `joint_sex` | `M` or `F` | — |
| `commutation_enabled`, `issue_state_excludes_withdrawal`, `qualified` | flags; `qualified` is read by no formula | the annuity date |
| `rating_factor` | a multiplier of mortality, the substandard rating, 1.0 as shipped | the annuity date |
| `annuity_year` | a calendar year | the annuity date: the anchor of the generational improvement |
| `mort_basis` | `table` or `scenario`, the probability-weighted run or the worked example's deterministic one | a modelling switch **[std]**, not a fact about the contract |
| `death_mth_1`, `death_mth_2` | policy months, blank for a life that survives | the scenario's month of death, counted from the annuity date on the clock `duration_mth` counts |
| `provenance` | text: `SPIA_US_S`'s on a twin, the generator's on any other row | — |

A contract issued before its annuity date — the product allows up to twelve months'
deferral [S1] [S5] — is modelled as an annuity commencing later, a point whose
`duration_mth` is `−k`. `SPIA_US_S` collapses the annuity date onto the issue date, so the
short pre-income period between them, which carries a death benefit at one carrier only
[S2], is not modelled here either.

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- the six in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months, read by value, so that `12.0` is 12;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than the
  stop rule from the annuity date plus ten years: 816 months on the anchor's 65/62 pair,
  1,080 for a single life at 40, the youngest age the shipped tables carry, and 1,560 at
  0, the youngest issue age the model projects. Set to 0, the Reference refuses
  future new business altogether, and a negative horizon is itself refused;
- each life column is a probability, 0 to 1;
- `commute_frac_cum_init` is a number, 0 or more and below 1;
- `cmt10_shift_init` is a number, of either sign;
- a single-life contract has no second life: `lives_if_init_2` is 0;
- a contract not yet in payment, `duration_mth` 0 or less, holds its values at the annuity
  date: each covered life 1, no commutation and no change in the CMT;
- each month of death, `death_mth_1` and `death_mth_2`, is blank or a whole number of
  months, read by value, so that `13.0` is 13 and a fraction or text is refused, on either
  basis; the table is returned with the two columns as the numbers they were checked as,
  which is what the projection reads;
- on the scenario basis each life's opening status is its month of death's: 1 while the
  life survives to the valuation date, `death_mth` blank, negative or `duration_mth` or
  later, and 0 once it has died, so that the scenario's step, which survival follows after
  the valuation date, agrees with the opening value at it;
- a commutation fraction appears only where a commutation could have been taken before the
  valuation date: the contract holds the right, its issue state allows it, it has a certain
  period, an elected one or an installment refund's, and `duration_mth` is 13 or more, the
  first withdrawal being taken in policy month 12 and reducing the instalments from month
  13. That is a necessary condition only: the check cannot see an installment refund's
  derived period, which needs the projection, nor whether enough of a certain period was
  left to commute, and it does not ask whether the model's own utilization would have
  taken a withdrawal, since a real record's withdrawals do not depend on it.

The surrender-charge scale, which `SPIA_US_S` reads from the same file, is checked too, by
`Data.surr_charge_scale()`: its policy years are read by value, once, so that `2.0` is year
2, and a year that is not a whole number, text and a blank among them, a gap, a repeat, a
year below 1 or a blank rate is refused, naming the file. `surr_charge_rate(y)` takes the
scale's first and last years and its rates from there, where `SPIA_US_S` takes `int()` of
the raw years for its first and last, so that a year written `x` raises Python's own
message and one written `3a` turns the years to text.

A point at or past the stop rule, `duration_mth ≥ stop_mth()`, reads, but `proj_len()`
refuses it, naming the point. So does a contract that owes nothing after the valuation
date: in payment, its certain period over, and no life-contingent payment left, because
the form is `certain_only` or every covered life has died. Such a contract made its last
payment, or its refund, before the valuation date, and an in-force extract should not carry
it; it is `Term_US_SEC`'s point past its cover, for a product whose cover can end with a
death. The rule needs the certain period, which an installment refund derives from the
schedule, so it is the product's rule and not the table's, and each message says why
nothing is owed: a `certain_only` contract pays nothing after its certain period; every
covered life has died, and the certain period has ended; or every covered life has died,
on a form with no certain period. So a loop over the block meets such a row only when it
reaches it, after projecting the points before it. `run_sec.py --block` asks every point
for its frame before it projects any, and stops before it prints anything.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`SPIA_US_S` and its table by `tests/sec_support.py`, from the `SPIA_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `SPIA_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py SPIA_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1–15 | twin | S points 1–15 | commencing at `t = 0`: `SPIA_US_S`'s worked example under both triggers, its traces and its pitfall cases, each covered life 1 |
| 16 | derived | S point 1 at S month 14 | the anchor cell the month after its joint annuitant's death: lives 1 and 0, paying 343.33 from `t = 0` and 353.63 from `t = 10` |
| 17 | derived | S point 6 at S month 13 | the cash refund in its annuitant's month of death: the refund, 100,000 − `G(13)` = 93,485.00, at `t = 0`, and nothing after |
| 18 | derived | S point 5 at S month 120 | the 10-year certain period ending at the valuation date: the survivor reduction it deferred begins at `t = 0`, 447.97, two thirds of 671.96 |
| 19 | derived | S point 13 at S month 30 | both lives dead inside the certain period: lives 0 and 0, the floor paying the full instalment, 530.45 rising to 652.39 at `t = 89`, and nothing from `t = 90` |
| 20 | derived | S point 9 at S month 24 | the commuting point on the table basis, on its second anniversary: lives 0.986815 and 0.993436, and eligible to commute at `t = 0` |
| 21 | derived | S point 8 at S month 695 | the anchor cell on the table basis in its last month, a one-row frame: the primary dead, aged past the limiting age, the joint annuitant alive with probability 3.84e-06 |
| 22 | future | S point 8, 13 months on | commencing at `t = 13` |

A derived row's opening state is what `SPIA_US_S` carries into its month `d`, each column
read as `SPIA_US_S`'s own formulas read it: each life's survival to time `d`,
`lives_if(d, life)`, before month `d`'s deaths; the commutation fraction applying in month
`d`, `commute_frac_cum(d)`, before its withdrawal, which is 0 on every shipped row, because
commutation utilization ships at 0; and the CMT's change since the annuity date,
`SPIA_US_S`'s `cmt10_shift`, which it applies from month 0 on, so that a row restated at `d`
has seen all of it, 0 on every shipped row, as `cmt10_shift` ships. Its `policy_count` is
`SPIA_US_S`'s
`pols_if_init()`, the contracts the point stands for, and not `SPIA_US_S`'s `pols_if(d)`,
which is the closing obligation measure: the survival is in the life columns. So the row
continues the S projection from there. Its `policy_id` is the S row's with the month
appended, `IA-000001-M14`, and a future row's carries the months to the annuity date,
`IA-000008-F13`. Row `t` of a generated point is month `t + source_mth` of its S point.
All 22 are at issue ages 65 and, where joint, 62, as `SPIA_US_S`'s points are. The shipped
mortality table and improvement scale carry ages 40 to 120, so a point on the table basis
at a younger issue age needs both extended first.

## Counts and timings

`pols_if_init()` is the count in payment at the valuation date: `policy_count` for a point
already in payment, 0 for any other. `pols_new_biz(t)` is `policy_count` in the month the
annuity commences, the month with `duration_mth(t) = 0`, and 0 in every other: new business
in `basiclife/BasicTerm_SE`'s sense, a contract entering the books, with no premium,
because the single premium is a pricing input, as in `SPIA_US_S`. `pols_if_at(t, timing)`
has two timings, `basiclife/BasicTerm_SE`'s:

- `BEF_NB`, the contracts carried in from month `t − 1`, before month `t`'s annuities
  commence: `pols_if_init()` at `t_entry()`, the first month on the books, and the whole
  `policy_count` after it, to the stop rule;
- `BEF_DECR`, that count plus `pols_new_biz(t)`, which weights every cash flow of month
  `t`.

Any other timing raises. **The count is not decremented.** `SPIA_US_S` weights every flow
by its constant `pols_if_init()` and carries mortality in each life's `lives_if`, and this
model does the same on the count on the books: every cash flow is
`pols_if_at(t, BEF_DECR)` times an amount per contract weighted by survival. So
`BEF_NB` is a closed form, the same float that a recursion
`BEF_NB(t − 1) + pols_new_biz(t − 1)`, as `Term_US_SEC`'s, would give, with no chain of
calls behind it. The count leaves the books only at the stop rule:
`pols_if_at(t, BEF_DECR) − pols_if_at(t + 1, BEF_NB)` is 0 at every `t` of every
frame but the last, where it is the whole count, at the end of the last projected month.
`SPIA_US_S` has no maturity, and neither has this model.

`pols_if(t)` keeps `SPIA_US_S`'s definition, the notes' obligation measure `IF(t)`, on the
count on the books: `pols_if_at(t, BEF_DECR) × max(C(t), l_alive(t + 1))`, the contracts
with a payment obligation still open at the end of month `t`, with the life-contingent leg
dropped on `certain_only`, as in `SPIA_US_S`. It carries the maintenance expense. It is a
closing measure, not the count before decrements: on point 8, the anchor cell on the table
basis, `pols_if(0)` is 0.99999986 against a count of 1, as in `SPIA_US_S`; on point 17, the
cash refund in its month of death, it is 0; and on point 21, the anchor cell in its last
month, 3.41e-06, `SPIA_US_S`'s `pols_if(695)`. So the registry marks the model
`closing_pols_if`, and the convention every other `_SEC` model meets,
`pols_if(t) = pols_if_at(t, BEF_DECR)`, skips it. The count on the books is not a column
of `result_pols()`: it is the table's `policy_count`, from the annuity date to the stop
rule.

**`pols_new_biz`, and no lapse.** `SPIA_US_S`'s tests forbid `pols_new_biz` on a SPIA,
beside `pols_lapse`, `lapse_rate`, `surr_value`, `cash_value` and `av_pp`: the contract has
no account value and no surrender right, so there is no lapse decrement, a position VM-22
makes prescriptively for this reserving category [R2] [REG-R36]. Here `pols_new_biz`
exists, because an annuity commencing after the valuation date is a contract entering the
books, and it means only that. The model has none of the other five.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < stop_mth()`, and outside it, before the
annuity commences and from the stop rule on, every count is zero, and so every cash flow.
No count evaluates a rate there, and no cell reads a policy year or an attained age the
contract does not have: `is_payment_mth` and `commute_elig` are false, and the scheduled
and payable instalments, the certain floor, the payment factors, the mortality and
improvement rates, the commuted value, the commutation fraction, the refund, the
withdrawal and its surrender charge are zero before any table or schedule is read.
`lives_if` and `lives_if_last` are zero before the contract is on the books.

Three chains of calls run from month `t` back to `t_entry()`, each one cell a month, as in
`SPIA_US_S`: survival on the table basis, `lives_if`; the commutation fraction on every
point, `commute_frac_cum`, which recurses whether or not the contract can commute; and the
payments to date on a refund form, `cum_annuity_pp`, back to the valuation date's policy
month. The longest sets how deep a cold call runs, counted as modelx's stack trace counts
it; `mx.set_recursion` admits a call one level deeper than the limit it is given. A cold
`net_cf` in the last month of the anchor's 696-month frame on the table basis, point 8, runs
709 cells deep, 696 of them `lives_if`, a recursion limit of 708, against 705 cells in
`SPIA_US_S` and 706 before compiling, which added the reads of the tables' arrays at the
chain's foot; on the scenario basis, point 1, it runs 703 deep, 695
of them `commute_frac_cum`; on the cash refund in payment 13 months, point 17, 654 deep, 647
of them `cum_annuity_pp`; and on point 22, commencing 13 months on, 709 again, because its
chains stop at `t_entry()`. At the longest cover the contract allows, 1,440 months from
issue age 0, the youngest the model projects on any form, in a copy whose mortality table
and improvement scale are extended to age 0: a single-life cash refund on the table basis
runs 1,453 cells deep, a recursion limit of 1,452, at the valuation date and commencing 120
months on alike, and so does a joint life annuity certain issued at 0 and 0 with a certain
period of 1,440 months, the longest `proj_len()` admits, commencing 120 months on: the
deepest call the contract allows; a `certain_only` annuity issued at 0 runs 1,452 deep.
Each report evaluates its columns in ascending `t`, and a sweep of the committed points
that way, every report and check, runs 12 cells deep, a recursion limit of 11.

## The opening state

`SPIA_US_S` projects every contract from its annuity date, with each covered life alive,
no commutation taken and the CMT where it stood at purchase. A contract valued in payment
needs what those have become by the valuation date. Read cell by cell, `SPIA_US_S`'s
recursions carry two quantities along a path, survival per life and the commutation
fraction, which are three state columns, and two that follow from the contract's terms
alone, the payments to date and the income by policy year, which need none. One input is a
point-to-point quantity on a market path whose term began before `t = 0`, the CMT's change
since the annuity date, and its value at the valuation date is the fourth column.

**Survival per life.** Each life column opens `lives_if` at `t_entry()`; from there the
table basis decrements it month by month, and the scenario basis follows the months of
death on the policy clock, `lives_if(t, life) = 1{duration_mth(t) ≤ death_mth(life)}`,
which `Data` holds the opening status to. The derived rows show each case:

- Point 16, the anchor cell in payment 14 months, opens with lives 1 and 0, its joint
  annuitant having died in policy month 13. On the *either* trigger it pays two thirds of
  the instalment from `t = 0`, 343.33, `SPIA_US_S`'s month-14 figure, and the COLA
  continues on the unreduced income, to 353.63 from `t = 10`.
- Point 19, the certain-floor case, opens with both lives at 0 inside its 10-year certain
  period. The life-contingent factor is 0 and the floor 1, so it pays the full instalment,
  530.45 at `t = 0` rising with the COLA to 652.39 at `t = 89`, policy month 119, with
  `pols_if` at 1, and nothing from `t = 90`, where `pols_if` and the expense fall to 0
  together.
- Point 20 opens with two fractional lives, 0.986815 and 0.993436, `SPIA_US_S`'s survival
  of the anchor pair to month 24 on the table basis.
- Point 21 opens with the primary at 0, dead with certainty once past the limiting age,
  and the joint annuitant at 3.84e-06, in the last month of the frame.

**The commutation fraction.** `commute_frac_cum_init` is path-dependent, because it
records the withdrawals actually taken, so the contract's terms cannot re-derive it.
Commutation utilization ships at 0, so no shipped row has commuted, and the column is 0 on
all 22. Switch it on as the splice does, before either model computes anything:
`commute_util_base = 0.5` in both, and the CMT 50 basis points up since the annuity date,
`SPIA_US_S`'s `cmt10_shift` at 0.005, which a row restated in payment carries as
`cmt10_shift_init`, this model's `cmt10_shift` then being 0. `SPIA_US_S`'s point 9
withdraws 25,485.58, half its commuted value, at policy month 12, the first month a
withdrawal is allowed, and its certain instalments are halved from month 13. Restated in
payment 13 months, it opens with `commute_frac_cum_init` 0.5. It pays 257.50 at `t = 0`,
half the 515.00 scheduled, withdraws 11,735.74 at policy month 24 and receives 17,115.93 in
instalments over the rest of its certain period, each `SPIA_US_S`'s figure. With the column
at 0 it would pay 515.00 at `t = 0`, withdraw 23,471.48 at policy month 24 and 10,635.96
more at month 36, and receive 21,808.98: the figures of a contract that never commuted.
From policy month 120 both pay the life-contingent instalment in full, and alike, because
a commutation reduces certain instalments only.

**The CMT's change since the annuity date.** The commutation discount rate is
`j = j0 + [CMT10(t) − CMT10(0)]`, `0` the annuity date: the base rate, 4.00% **[std]**,
moved one for one with the 10-year CMT's change since purchase. `SPIA_US_S` reads the change
from one Reference, `cmt10_shift`, and every one of its points commences at its own `t = 0`,
so one value fits them all. Contracts in payment at a valuation date were bought at
different dates and have seen different changes, which no one value holds. So every contract
of a block reads the change on one path of the CMT, which every point shares, as it shares
every economic input, each from its own annuity date. A contract on the books at the
valuation date, in payment or commencing then, has seen `cmt10_shift_init` by that date, and
sees `cmt10_shift`, the change made at the valuation date, from month 0 on, as `SPIA_US_S`'s
contract sees its `cmt10_shift` from its annuity date: its rate is
`j0 + cmt10_shift_init() + cmt10_shift`, added in that order. A contract commencing later is
bought after that change and has seen none of it, so its rate is `j0`. The column ships at 0
on every row, as `cmt10_shift` does. Set to 0.005 on point 20, the commuting point in
payment 24 months, the CMT 50 basis points up since its annuity date, point 20 discounts at
4.5%, its commuted value at `t = 0` 46,942.96, `SPIA_US_S`'s point 9 at its month 24 with
its `cmt10_shift` at 0.005, while in the same read its twin, point 9, commencing at the
valuation date, discounts at 4.0%, its commuted value at policy month 12 52,062.79,
`SPIA_US_S`'s on the shipped 0, and so does the same contract commencing 13 months later, a
row the tests add, at its policy month 12. With `cmt10_shift` at 0.005 too, the CMT up 50
basis points more at the valuation date, point 20 discounts at 5.0% and point 9 at 4.5%,
while the contract commencing 13 months later, bought after the rise, still discounts at
4.0%, its commuted value unmoved. The rate is level: it reads neither clock. A path of the
10-year CMT would be another input table, read on the valuation clock, each contract taking
the change on it from the later of its annuity date and the valuation date.

**The certain months left** need no column. `certain_floor(t)` is
`1{duration_mth(t) < n_eff}` on the policy clock, and the effective certain period `n_eff`
is fixed at the annuity date: the elected one, or an installment refund's, which
`certain_mths_refund()` derives from the schedule. Point 18 is valued at policy month 120,
where its certain period ends, so the survivor reduction it deferred begins at `t = 0`:
447.97, two thirds of the 671.96 the COLA has reached, where `SPIA_US_S`'s point 5 paid the
full instalment through month 119.

**The payments to date** need no column either. `cum_annuity_pp(k)`, the notes' `G(k)`, is
the instalments scheduled before time `k`: a deterministic as-if-alive schedule, fixed by
`B(1)`, the COLA, the frequency and the timing, which a cash refund nets on death and an
installment refund searches for the premium. It stays on the policy clock, keyed as
`SPIA_US_S` keys it, and only its recursion's base moves: at the valuation date's policy
month, `duration_mth(t_entry())`, one loop sums the instalments scheduled before it, the
same additions in the same order as the recursion, so `G` is `SPIA_US_S`'s to the last bit,
and a later key recurses back to that one, a month at a time. Point 17, the cash refund in
payment 13 months, reads `G(13) = 12 × 500.00 + 515.00 = 6,515.00` and pays the refund of
93,485.00 at `t = 0`, as `SPIA_US_S`'s point 6 pays at its month 13; its `result_cf()` on a
fresh read evaluates `G` at keys 13 to 659 alone. Recursing from the annuity date, as
`SPIA_US_S`'s does, the first refund of a contract long in payment would recurse as deep as
the contract is old: a cash refund in payment 600 months reads `G(600)`, which in
`SPIA_US_S` runs 606 cells deep from cold, a recursion limit of 605, where this model's
whole `result_cf()` for it runs 9 deep, a limit of 8. The income by policy year,
`annual_income(y)`, is based the same way, at the valuation date's policy year, where in
`SPIA_US_S` the anchor cell's `annual_income(58)` recurses through 58 `annual_income`
cells, back to `B(1)`.

## Departures from SPIA_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, each
read of the schedule at a month is a read by policy month, and every recursion on the
valuation clock begins at `t_entry()`. Of `SPIA_US_S`'s 72 `Projection` cells, 22 are
unchanged, 14 have a new docstring only and 36 are rewritten, and 23 cells are new, 95 in
all. Of its five `Data` cells, three are unchanged, one has a new docstring and one, the
model point table's reader, is rewritten, and one is new, `surr_charge_scale`. None is
removed or renamed, which the twin identity asserts: a cell of `SPIA_US_S`'s that this
model lacked would fail it. Compiling then changed how each cell reads its inputs and
spells its codes, and no number: it added three cells to `Projection`, `point_id`,
`mort_schedule` and `improvement_schedule`, 98 in all, and 64 to `Data`, 70 in all (*The
compiled model*, below); of `SPIA_US_S`'s cells it changed the signature of one, `claims`,
now of `t` alone, which the twin identity compares with `SPIA_US_S`'s `claims(t, None)`
and `claims(t, "REFUND")`. `Projection`'s `point_id` Reference gave way to `idx`;
`commute_disc_convention`, which held text, holds an int code; and the codes,
`issue_age_min` are new References, as is `Data`'s `np`.

| Cells | `SPIA_US_S` | `SPIA_US_SEC` | Why |
|---|---|---|---|
| `duration_mth`, `duration` | `t`, `t // 12` | `duration_mth_init() + t`, `duration_mth(t) // 12` | The policy clock, opened from the model point |
| `proj_len`, `stop_mth` | `max(horizon_mths(), certain_mths_eff())`, the months from the annuity date | `stop_mth() − duration_mth_init()`, the months from the valuation date; raises at or past the stop rule, and for a contract owing nothing | The frame starts at the valuation date. `stop_mth()` is new and keeps `SPIA_US_S`'s formula |
| `pols_if_init` | the column's 1.0, the weight of every flow | `policy_count()` for a point in payment at the valuation date, 0 otherwise | Contracts in payment open the count; an annuity commencing joins it as new business in its month |
| `annuity_payments`, `claims`, `commutations`, `surr_charge`, `pols_if` | `pols_if_init()` times an amount per contract | `pols_if_at(t, BEF_DECR)` times the same amount | The count on the books weights every flow |
| `lives_if`, `lives_if_last`, `check_lives_roll_fwd_resid` | indexed by `k` from the annuity date: 1 at `k ≤ 0`, the scenario's step at `k > death_mth`, the check rebuilt from 1 | indexed by `t` from the valuation date: `lives_if_init(life)` at `t_entry()` and 0 before, the step at `duration_mth(t) > death_mth`, the check rebuilt from the opening state | Survival is carried forward from the valuation date, from the contract's state there |
| `commute_frac_cum` | 0 at `t ≤ 0` | `commute_frac_cum_init()` at `t_entry()` | A contract in payment may have commuted already |
| `cum_annuity_pp`, `annual_income` | recursions from the annuity date, `G(k − 1) + annuity_pp_sched(k − 1)`, a policy month passed as `t`, and `B(y − 1)(1 + g)` from the column's `B(1)` | still on the policy clock, `G` reading `annuity_pp_sched_pm(k − 1)` and `B(1)` read by `annual_income_first()`; each based at the valuation date's key by one loop, in the recursion's order | A contract valued late in life reads its payments to date and its income without recursing back to the annuity date, to the last bit the same |
| `is_payment_mth`, `annuity_pp_sched`, `annuity_pp`, `certain_floor`, `commute_elig`, `claim_pp` | `t` tested against the payment step, the trim month `n_R − 1`, the certain period and the commutation month `12(y − 1)`; the refund balance read at `G(t)`, or `G(t + 1)` in an advance payment month | the same tests on `duration_mth(t)`, the schedule through `is_payment_pm(k)` and `annuity_pp_sched_pm(k)`; the balance at `G(duration_mth(t))`, or one month on | On the valuation clock month `t` is not a policy month |
| `commuted_value`, `commute_amount` | the remaining certain instalments over months `t + 1 … n_eff − 1`, by a loop and two list comprehensions | the same over policy months, read from `annuity_pp_sched_pm`, by loops | The same reason, and no closure in a cell the commutation fraction's recursion runs through |
| `commute_disc_rate` | `j0 + cmt10_shift`, the CMT's change since the annuity date | on a contract on the books at the valuation date, `j0 + cmt10_shift_init() + cmt10_shift`: the change to that date, from the model point, then the change made at it; `j0` on a contract commencing later | Contracts in payment bought at different dates have seen different changes, which one Reference cannot hold; on the one path a block shares, a contract bought after the valuation date has seen none of a change made at it |
| `surr_charge_rate` | the scale's first and last years by `int()` of the raw table's years | the years, the first and last among them, and the rates from `Data.surr_charge_scale()`, which reads the years by value once and refuses a malformed scale by name | A year written as text raised Python's own message or turned every lookup into a miss |
| `certain_mths_eff`, `certain_mths_refund`, `is_payment_mth`, `payment_surv_mth`, `payment_factor_life`, `pols_if`, `annuity_pp`, `claim_pp`, `lives_if`, `check_lives_roll_fwd_resid`, `commuted_value` | branch on the text of `form()`, `payment_timing()`, `reduction_trigger()`, `mort_basis()` and the `commute_disc_convention` Reference | branch on eight flags, `is_period_certain`, `is_certain_only`, `is_cash_refund`, `is_installment_refund`, `is_arrears`, `is_trigger_either`, `is_scenario` and `is_disc_compound`, each validating its column or Reference as `SPIA_US_S`'s accessor does | No projection formula compares text or calls a label accessor, which are left to reporting, so that the compiled form can type every cell |
| `mort_rate_base`, `improvement_rate` | the table joined on age and sex in the monthly cell | the limiting-age test kept there, the table read through `mort_rate_base_at(x, life)` and `improvement_rate_at(x, life)` | One reader per table, keyed by attained age, called only at ages the table holds |
| `mort_rate`, `mort_rate_base`, `improvement_rate`, `lives_death`, `lives_death_last`, `certain_floor`, `payment_factor_life`, `annuity_pp_sched`, `annuity_pp`, `commute_elig`, `commuted_value`, `commute_frac_cum`, `surr_charge`, `commutations`, `claim_pp`, `pols_if` | unguarded: no `SPIA_US_S` frame has a month outside it | zero or false outside the frame, `is_active(t)`, before any table, rate or policy year is read | A month before the annuity date has `t ≥ 0`, a negative policy month and a policy year of 0 or less |
| `inflation_factor` | `(1 + π)^(policy_year(t) − 1)` | `(1 + π)^(t // 12)` | Unit costs in valuation-date dollars, stepping on the valuation date's anniversaries |
| `result_pols` | `SPIA_US_S`'s seven survival and payment-factor columns, then `pols_if` | `pols_if` first and `pols_new_biz` second, then the seven; zeros before the annuity commences | The counts first, after `basiclife/BasicTerm_SE`'s `result_pols()`, and no rate read before the annuity date |

The other new cells are `policy_count`, `duration_mth_init`, `lives_if_init`,
`commute_frac_cum_init`, `cmt10_shift_init`, `t_entry`, `is_active`, `pols_if_at` and
`pols_new_biz`. One
difference shows on invalid input alone: an invalid `commute_disc_convention` raises
wherever a certain month remains to discount, where `SPIA_US_S` raises at the first
instalment it discounts.

Of the cash flows, the change of clock moves the maintenance expense alone, and
`liability_cf` and `net_cf` with it. A contract in payment carries that expense in
valuation-date dollars. Point 18, valued on an anniversary, has `expenses(t)` equal to
`SPIA_US_S`'s `expenses(120 + t)` divided by `1.025^10`, about 1.280, at every `t`; off an
anniversary the steps fall on the valuation date's anniversaries rather than the
contract's, so point 16's are `SPIA_US_S`'s from month 14 on divided by 1.025 in some
months and by 1.025² in others. Their other cash flows and their counts are `SPIA_US_S`'s
from their months on. Point 22 is `SPIA_US_S`'s point 8 thirteen months on in those columns
too, and its maintenance expense is `SPIA_US_S`'s times 1.025 or 1.025².

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, on the points of the splice
grid, which take the branches they do not, on the contract's longest frames, where a
commutation's floors bind, on keys written as floats and on a sex that is not text, and
where the cap on mortality binds or a NaN reaches it. The compile tests hold it so on
x86-64, and to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py immediate_annuity                  # in place, beside the model
python tools/build_sec_cy.py immediate_annuity --out /tmp/spia  # elsewhere, with the CSVs
```

The tool exports the model to `SPIA_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `SPIA_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/immediate_annuity")   # the directory holding the build
from SPIA_US_SEC_nomx_cy import mx_model as model
model.Projection[15].result_cf()                   # point 16, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made, and
keeps the values it computes until it is deleted; the base `Projection` and `Data` keep
theirs for good. So `Projection.idx = 15` after `Projection.result_cf()` leaves point 1's
frame cached, while `point_id()`, not yet computed, reads point 16's label, and
`Projection.expense_maint` set to 90 once `Projection[0]` has computed point 1's
`expenses(0)` leaves it at 5.0, where an ItemSpace made after, `Projection[1]`, computes 7.5
for point 2's. Set every Reference on a model just imported, before anything is computed,
where modelx would recompute; a test holds the compiled model to this.

A build takes 35 to 40 s here, with MSVC, and needs a C compiler, which is why
`requirements.txt` leaves modelx-cython out: `pip install -r requirements-cython.txt`.
`run_sec.py --cython` builds in place when it finds no build, or one older than the model,
the sample, the spec or the tool, and `--build DIR` runs a build made with `--out DIR`.
Nothing a build writes is committed. All of it derives from committed files, and an
extension module is built for one operating system, processor and Python
(`_mx_classes.cp313-win_amd64.pyd` here); in place, `.gitignore` covers all of it. A
`lifelib.create()` copy of the library carries no `tools/`, so it cannot build, and
`run_sec.py --cython` says so.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so. Compiled by
the same tool, with a sample of its own, as it stood after running in force, the model typed
87 of its 95 `Projection` cells as C numbers. Three took a timing or a kind as text,
`pols_if_at`, `claim_pp` and `claims`, whose kind could be `None`, and those three and
`sex`, a label, kept a dictionary for a cache; the bodies of the typed cells still called
pandas and Python: a `model_point()` lookup for each attribute a formula reads, text
compared in each of the eight decodes, `pd.isna` on each month of death, a `.loc` on a table
for each attained age's mortality and improvement and each contract year's surrender charge,
a list built and its `min` taken for the age stop. It ran 2.0 times its own export, 7.57 ms
a point on `net_cf` against 14.9, over the committed points, measured once, on a build of
the stage-`E` model with a sample and a spec of its own, which are not shipped. So each
input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[15]` is point 16, and `point_id()` returns the
  label, which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point column a formula uses is a `Data` vector of
  int64 or float64, one element a point, named as the column, and a cell reads its point's
  element as `SPIA_US_S` reads the point's value: `premium_pp()` is
  `float(data.premium()[idx])`, an age is `int()` of its element and a flag `bool()` of
  its. Compiled, the vector is a typed memoryview, and the read is a load from memory.
  Where a point's value can be one its projection cannot use, a 0/1 vector beside it,
  `premium_ok()` and the like, says whether it is usable, and the accessor refuses the
  point where it reads the element (*What it refuses*, below).
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column a
  formula branches on into 0/1 flags, for every point at once: the form into
  `is_period_certain`, `is_certain_only`, `is_cash_refund` and `is_installment_refund`,
  the trigger into `is_trigger_either`, the timing into `is_arrears` and the basis into
  `is_scenario`; and beside each column a `has_*` flag, whether the value is one
  `SPIA_US_S` names. Each decodes as `SPIA_US_S` compares the column, exactly, case and
  whitespace included, so a value no flag names sets no `has_*` flag, and the decode that
  reads it raises `SPIA_US_S`'s message, `invalid form` and the like, where the projection
  first meets it, as at stage `E`. A flag column, `joint`, `commutation_enabled`,
  `issue_state_excludes_withdrawal` or `qualified`, is `bool()` of each element as pandas
  reads it, as `SPIA_US_S`'s `bool(model_point()[...])` is. A blank month of death, which
  `SPIA_US_S` reads as a survivor through `pd.isna`, is -1 in `death_mth_1` and
  `death_mth_2`.
- **Tables indexed by integers.** The mortality table and the improvement scale, keyed by
  age and sex, are each numbered by its own sexes, in sorted order, from 1, and held by
  schedule and attained age in `mort_table_array` and `improvement_array`, padded with
  NaN from age 0 so that the age is the index, with the first and last age of each
  schedule beside them. Each point carries the schedule of each life's sex in each table,
  read through `mort_schedule(life)` and `improvement_schedule(life)`, and each table's
  one reader, `mort_rate_base_at(x, life)` or `improvement_rate_at(x, life)`, checks the
  age against the schedule's extents before it reads, so nothing reads the padding. A sex
  a table lacks, a blank among them, is schedule 0 there, a row of padding whose first age
  is 1 and whose last is 0, which the reader refuses at the first age it reads, naming the
  point, the age and the life, where `SPIA_US_S`'s `.loc` raised `KeyError`: no point on the
  scenario basis reads it, nor any single-life point's second life, so neither is refused.
  The two tables are numbered apart, so a sex one holds and the other lacks shifts neither
  numbering. The surrender charges are a vector by contract year, padded from year 0,
  with the scale's first and last years beside it, and `surr_charge_rate(y)` reads it at
  `y` clamped to them, as `SPIA_US_S` reads the scale's first and last rows beyond them.
- **Codes.** A timing, the kind or the commutation discount convention, which `SPIA_US_S`
  spells as text, is an int Reference named as the text: the count's timings `BEF_NB = 0`
  and `BEF_DECR = 1`, the kind `REFUND = 0`, and the conventions `COMPOUND = 0` and
  `SIMPLE = 1`, which `commute_disc_convention` now holds, `COMPOUND` as shipped. A call
  reads as before, less the quotes: `pols_if_at(t, BEF_DECR)`, `claim_pp(t, REFUND)`. A
  string argument would give the cell a dictionary for a cache, where a code indexes a C
  array, so codes are numbered from 0 without a gap, the timings by instant, as in every SEC
  model. A cell compares a code with `==` or `!=` alone, so that a text passed where a code
  is taken meets the cell's own refusal in modelx too: `invalid timing`, `invalid kind` or
  `invalid commute_disc_convention`. The `Projection` docstring's *Codes* lists the five.
- **One kind, no total.** `SPIA_US_S`'s `claims(t, kind=None)` is one kind's claims or,
  with `None`, their total, and the cash refund is its only kind, so the total is that
  kind's claims and no sum. Here `claims(t)` takes `t` alone and is that kind's formula,
  the same product in the same order, with no `0.0 +` that would turn a `-0.0` into
  `0.0`; `claim_pp(t, kind)` keeps its kind, as the code. The twin identity compares
  `SPIA_US_S`'s `claims(t, None)` and `claims(t, "REFUND")` with `claims(t)` (*Tests*,
  below).
- **No list.** `horizon_mths()` finds the younger of the two issue ages by one comparison,
  where `SPIA_US_S` takes the `min` of a list; the commuted value and the withdrawal were
  loops over policy months already, since running in force. And the payments to date and
  the income by policy year are based at the policy month and year of the valuation date
  read from the model point, `max(duration_mth_init(), 0)` and that `// 12 + 1`, where at
  stage `E` they read them through the clock at `t_entry()`: the same keys, so no number
  moved.
- **No Python call kept.** No formula outside the reporting cells calls a Python builtin
  outside its refusals but `int`, `float`, `bool`, `min`, `max` and `range`, which Cython
  turns into C, so `tests/us_registry.py` admits none. `payment_freq()` compares the
  element with each of 12, 4, 2 and 1 rather than hold `int()` of it in a local, which
  would keep a Python object in the cell. No cell is uncached, and none takes a float.
- **Reporting cells stay Python.** `model_point()`, the label accessors `form()`,
  `reduction_trigger()`, `payment_timing()`, `mort_basis()` and `sex(life)`, and the two
  reports return a table row, text and DataFrames, for a reader, for `run_sec.py` and for
  the comparison with `SPIA_US_S`. No other cell calls them, so they cost the projection
  nothing. Each label returns its point's column: `form`, `reduction_trigger` and
  `mort_basis` the column of their own name, `payment_timing` the `timing` column and
  `sex(life)` the `primary_sex` or `joint_sex` column by life, which the registry entry
  declares in `"reporting_columns"`, so that the conventions hold each label to the column
  it returns. The first four validate their column, as `SPIA_US_S`'s do, so each returns
  text or raises, and compiles to a Python `str`. `sex(life)` returns its column as read,
  and `Data` accepts a sex that is not text: a single-life point's blank second life,
  which reads as NaN, or a number, which `SPIA_US_S` projects on the scenario basis, which
  never joins a table. So it compiles to a Python object, as the sample traces it
  (below), with the one dictionary for a cache in `Projection`, and returns what modelx
  returns. The two checks are reporting cells too, but they return a verdict, which
  compiles to a C `bint`.

The `Data` docstring lists its vectors, arrays and counts, each with the column or file it
comes from: 42 vectors of int64 by point and 11 of float64, the 14 `_ok` flags, the four
flag columns and the 11 flags decoded from text among the first; the mortality table and the
improvement scale, float64 by schedule and attained age, and their first and last ages,
int64 by schedule; the surrender charges, float64 by contract year; and four int counts and
extents, each a table's check, `mort_sexes` and `improvement_sexes` among them. The six
readers stay Python, returning DataFrames and a path, and no `Projection` cell but
`model_point()` reads them. Every other cell of `Projection`, 90 of its 98, returns a C
`bint`, `long long` or `double`, and caches a single value, or a C array the spec sizes from
the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,562 by `t`, of `double`, `long long` or `bint` | the 32 cells of `t` alone: every count, rate, factor, instalment, claim, commutation and cash flow; the policy clock, its years and the calendar year; the flags `is_active`, `is_payment_mth` and `commute_elig`; and the checks' monthly residuals |
| a C array of 1,562 by 3 | the nine cells of `t` and a life or a code: `age`, `lives_if`, `lives_death`, `mort_rate_base`, `improvement_rate`, `mort_rate` and `mort_rate_mth`, by `(t, life)`; `pols_if_at`, by `(t, timing)`; and `claim_pp`, by `(t, kind)` |
| a C array of 1,442 by `k` | `is_payment_pm`, `annuity_pp_sched_pm` and `cum_annuity_pp`, by policy month |
| a C array of 122 by `y` | `annual_income`, `commute_util_rate` and `surr_charge_rate`, by policy year |
| a C array of 121 by 3 | `mort_rate_base_at` and `improvement_rate_at`, by `(x, life)` |
| a C array of 3 | `age_at_entry`, `death_mth`, `lives_if_init`, `mort_schedule` and `improvement_schedule`, by `life` |
| one `long long`, `double` or `bint` | the 36 cells without a parameter: the point's label, numbers, decodes and flags, its opening state, its certain periods, the ends of its frame, the discount convention decoded, and the two checks |
| a Python object | the eight reporting cells but the checks |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and the one dictionary among `Projection`'s caches there is `sex`'s.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the two reports
and the two checks on every committed point, which reach every cell but these:
`model_point()` and the five label accessors, which only a reader asks for; `point_id()`,
which only a refusal names; `premium_tax_rate()`, `premium_net_pp()` and `qualified()`,
which the model reports and no flow reads; `lives_death`, each life's death density, which
the last-death density replaces in every flow; and `surr_charge`, the charge the insurer
keeps, which no column shows. The sample calls those too, the monthly ones in every month
of the frame and the month after it, `lives_death` for both lives. Every timing of
`pols_if_at` and the one kind of `claim_pp` are reached by the reports. It projects the
committed points alone: the export it runs reads the CSVs of the directory the build is
made in, and the trace it needs is the committed points', which are what the tests
project. It calls `sex(1)` and `sex(2)` once more, on a copy of the table's first point
with both sexes blank, which it writes to a temporary directory and reads by a second
instance of the export, given the file's absolute path as `model_point_file`. That types
`sex` as a Python object, so that a blank or numeric sex returns what modelx returns
rather than raising `TypeError` (*What compiling changed, and why*); the other four labels
validate their column, and a blank would make them raise, so the run calls them on the
committed points alone. The committed points leave branches untaken: quarterly,
semi-annual and annual payments in arrears, a withdrawal taken, the residual floor
binding, the simple discount, a rating that caps mortality, the age stop inside a certain
period, the installment refund's trim below monthly, a COLA on a refund form. That still
types every cell, because every branch of a cell returns the one type its others return,
a rate a float in every branch, and on points that take those branches the compiled model
computes modelx's numbers (*Tests*, below). The sample also raises the recursion limit,
which modelx raises and its export does not (*What a compiled run needs*, below).

`spec_sec.py` sizes each C-array cache, by the names of the cells' parameters, and a
compiled cache raises `IndexError` for an argument outside it. So each size covers the
largest argument a cell is called with on a point the contract allows, in its frame and
in the month after it, `t = proj_len()`, which `lives_if` reads and the compile tests' full
sweep evaluates every monthly cell at; plus one because the index starts at 0, and one of
headroom:

| Parameters | Size | The largest argument |
|---|---|---|
| `t` | 1,562 | 1,560. The longest frame is any form on a youngest life of issue age 0, the youngest `issue_age_min` admits, whose frame `SPIA_US_S` runs to the age stop, 12 × (120 − 0) = 1,440 months, commencing 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 1,560 months, `t = 0 … 1,559`, and the month after, 1,560. Nothing reads `t + 1` at `t = proj_len()` |
| `t`, and `life`, `timing` or `kind` | 1,562 by 3 | the lives 1 and 2, the timings `BEF_NB` 0 and `BEF_DECR` 1, and the kind `REFUND` 0. Every 2-D cache has this one width, the widest. Cython's generated unpickle code converts a space's caches of one depth with one function for each inner shape, and given two widths it passes the narrower where the wider is expected, which gcc 14 refuses and which would write past its end (`WholeLife_US_SEC`'s *The sample and the spec*); MSVC accepts it. A timing 2, a kind 1 or 2, or a life 0 is then inside the cache, where the cell refuses it as modelx does, and a code or a life of 3 raises `IndexError`, compiled alone |
| `k` | 1,442 | 1,440, 12 × (`omega_age` − `issue_age_min`), the stop rule's policy month on the longest frame: the schedule is read at every policy month of a frame, to 1,439 on a youngest life of 0 and on a certain period of 1,440 months, and the payments to date, `G(k)`, on a cash refund up to the stop rule's month itself, 1,440, in an advance payment month of the last month, and on an installment refund up to the age stop |
| `y` | 122 | 120, the policy year of policy month 1,439, read by the income by policy year at the schedule's months, by the utilization inside a certain period, and by the surrender charge in every month of the frame |
| `x` and `life` | 121 by 3 | 119, the last attained age below `omega_age`, read by the two age readers from the youngest issue age, 0: `claims` weights by the last-death density on every form, a `certain_only` annuity on the table basis among them. Beside it `life`, 3 wide, as every 2-D cache |
| `life` | 3 | 2, in `age_at_entry`, `death_mth`, `lives_if_init` and the two schedules |

`proj_len()` refuses, naming the point, a covered life whose issue age is below
`issue_age_min`, 0, on every form, the primary's and the joint annuitant's each asked, a
departure: `SPIA_US_S` projects an annuity whose primary or joint issue age is below 0,
which `SPIA_US_SEC` refuses, a negative age being outside every contract, as `Term_US_SEC`
refuses its contract's bounds in `proj_len()`; and an elected certain period above `12 *
(omega_age - issue_age_min)`, 1,440 months, the longest the caches hold. It asks before it
asks the stop rule, since the installment refund's period, which the stop rule reads,
searches the payments to date up to the age stop, past the `k` cache on a point issued
younger. `SPIA_US_S` projects every form at any issue age, its frame running to the age stop
on its youngest life, so the caches are sized for issue age 0 on every form, below the 18
`product-spec.md` issues a lifetime form at: refusing a lifetime form below 18 would refuse
a point `SPIA_US_S` projects, which stage `E` projected (D2). A `Projection` ItemSpace is
about 16% larger for it (*What a compiled run needs*, below). `issue_age_min`, `omega_age`
and `Data.future_horizon_mth` are the contract the sizes are derived from. Raise `omega_age`
or the horizon, and a report runs past the caches in the compiled model alone: a frame of
more than 1,561 months, a policy month past 1,441, a policy year past 121 or an age past 120
raises `IndexError`, naming nothing, where modelx projects. Each needs the sizes derived
again, as `spec_sec.py` derives them, and a rebuild: `t` raised to 12 × (`omega_age` −
`issue_age_min`) + the horizon + 2, `k` to 12 × (`omega_age` − `issue_age_min`) + 2, `y` to
`omega_age` − `issue_age_min` + 2, and `x` to `omega_age` + 1. The shipped tables start at
age 40, so a point on the table basis at a younger issue age is refused today by its first
rate, naming it; the ages from 0 are the contract's, which extended tables reach.

### Two compiler directives

`tools/build_sec_cy.py` marks the module mx2cy translates `# cython: infer_types=True,
cpow=True`, and compiles it with `-ffp-contract=off` on every platform but Windows, as
`Term_US_SEC`'s *Two compiler directives* sets out, with what each costs and what it was
measured to change there. Here `cpow` reaches four powers: the monthly mortality rate,
`1 − (1 − q)^(1/12)` in `mort_rate_mth`, the generational improvement,
`(1 − G2_x)^k` in `mort_rate`, the compound commutation discount, `(1 + j)^(−(s − m)/12)`
in `commuted_value`, and expense inflation, `(1 + π)^(t // 12)` in `inflation_factor`.
Without `cpow` a compiler with C99's complex numbers, gcc among them, computes a power of
two doubles as a complex power, which can differ from Python's float power in its last
bits. With both directives and the flag every compiled value agrees with modelx's bit for
bit, and the compile tests hold each, by the module's first line, by the compiler's
command lines and, on x86-64, by the comparison itself. On Windows MSVC compiles without
the flag, since it emits no fused multiply-add for x64 without `/arch:AVX2`, which
setuptools does not pass, and the comparison is exact there too. On the same platforms as
the flag the tool adds `-Werror=incompatible-pointer-types`, so that gcc before 14, which
only warns of a pointer of the wrong type, fails the build as gcc 14 does: the error two
cache widths give (*The sample and the spec*, above). MSVC accepts two widths without a
word, so on Windows the one width rests on a test that holds every 2-D size in
`spec_sec.py` to the one width (*Tests*, below).

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 1,147,464
bytes, about 1.1 MB, the type's basic size, which holds every cell's cache, each beside a
flag array of its shape that marks what is computed. Its 41 caches of 1,562 months, 32 by
`t` alone and nine 3 wide, are most of it. That is 2.7 times `Term_US_SEC`'s and about
`WholeLife_US_SEC`'s, for frames of 1,562 months, which any form at issue age 0 sizes: it is
about 16% larger than it would be sized from 18, the youngest age `product-spec.md` issues a
lifetime form at. Making one costs time as well as memory: Python zeroes the struct when it
makes the ItemSpace, and making and releasing one, nothing computed, the runner's collection
included, took 0.26 ms here, of the 0.81 ms a compiled point takes (*Speed*, below).
Deleting it, `del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in
reference cycles, and only Python's cyclic collector frees it. That is why `run_sec.py
--block` collects after each release, in its frame pass and in its projections (*Run it*,
above), and a compile test holds a compiled block run to one point's ItemSpace at a time.
Without it, 506 compiled points peaked at 540 MB (*Speed*, below).

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no limit
raised. What it needs is stack. The deepest call the contract allows, a cold `net_cf` in the
last month of the longest cover, 1,440 months, runs a chain of one cell a month back to
`t_entry()`, from issue age 0: 1,453 cells deep in modelx on a cash refund, commencing now
or 120 months on, and on a joint life annuity certain issued at 0 and 0 with 1,440 certain
months, commencing 120 months on, and 1,452 on a `certain_only` annuity. Compiled with MSVC
14.37, on this machine, each runs on a thread of 384 KiB of stack and dies on one of 320, as
does every other longest cover. Windows rounds a thread's reservation up to 64 KiB, so the
bytes a level were read from the longest chain that runs at fixed reservations, in steps of
40 months: 360 months at 128 KiB, 640 at 192 and 920 at 256, 280 months more for each 64
KiB, 234 bytes a level, and 37 to 46 KiB besides, so about 377 KiB at 1,453 levels; at 320
KiB, 1,200 months ran on one run and died on a second. A test runs the call in a thread of 1
MiB, the stack Windows gives a program's main thread unless the program is linked for more,
and again on the main thread, which is where `run_sec.py --cython` runs, and which reserved
2,031,616 bytes here: 2.7 and 5.2 times the need. gcc's frames are another compiler's, and
the `cython` CI job, which runs the test on Linux too, is the check on them: the test first
runs the call at nine stacks, from 256 KiB to 2 MiB, and reports the smallest it ran on. At
the 232 to 288 bytes a level gcc took on the chains of the models compiled before this one,
the chain alone at 1,453 levels needs about 330 to 410 KiB. A stack below the need kills its
child on an overflow, by design; on Windows the child ends with `STATUS_STACK_OVERFLOW`, and
should Windows Error Reporting hold it instead, the test waits a bounded time for each child
rather than the job's hour. The export recurses in Python instead: the same call needs a
recursion limit of 2,931 there, 2,929 on the `certain_only` annuity, and the two reports and
the two checks, which run in ascending `t`, need 154 with the package's import among the
frames they run under. So `sample_sec.py` sets 12,000, four times the first rounded up to
the thousand, and a test holds it to that derivation.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the error itself propagates.

- What `Data` cannot read for the whole table, when the array is first read, naming the
  table and its points or lines: what `model_point_table()` refuses, as at stage `E`
  (*The in-force interface*, above); a label that is not a whole number below `2**53` in
  size, `model_point_table_sec.csv: point_id must be a whole number; [3.5] is not`, from
  `Data.point_id`, when a label is first read; and in `mort_table.csv` or
  `improvement_scale.csv` an age that is not a whole number, `mort_table.csv: age must be
  a whole number; it is not on line [2]`, a blank sex, a rate that is not a finite number,
  or a sex whose ages do not run from its first to its last, or run below 0,
  `mort_table.csv: the ages of sex F must run from -1 to 120 without a gap or a repeat,
  none negative`, by the table's check, which every array, extent and schedule of the
  table reads first. `SPIA_US_S` raised `KeyError` only where a projection read a missing
  key, and read a blank rate as NaN. A key written as a float, an age `40.0`, is read by
  its value, as `SPIA_US_S`'s lookups match it.
- What a point's projection cannot use, by the cell that reads it, naming the point, and no
  other point for it: a value that is not a number, `point_id 1: premium_tax_rate must be
  a number or blank; it is not`; an age, a month count, a frequency or a year that `int()`
  cannot read, or of `2**53` or more in size, which an int64 cannot be trusted to hold,
  `point_id 3: primary_age must be a number int() reads, below 2**53 in size; it is not`;
  and a blank or infinite amount or rate on a point whose projection reads it through a
  `max`, a `min` or a search that would turn the missing value into a number: the premium on
  a cash or installment refund, `point_id 6: premium must be a number, and a finite one on a
  cash or installment refund, which reads it; it is not`, the first year's income and the
  COLA rate on every point, the survivor percentage on a joint contract with a life
  contingency and the rating on the table basis. That is `Term_US_SEC`'s rule for a value a
  cap, a `min` or a `max` reads (its *What it refuses*), applied by point where Term applies
  it over the whole table, so that the model refuses no point `SPIA_US_S` projects to a
  number, as at stage `E`. A blank premium on a life annuity is NaN, as in `SPIA_US_S`, and
  a single-life point's blank `joint_age`, a blank `certain_months` on a form without an
  elected period and a blank `annuity_year` on the scenario basis are read by no projection,
  and refused only by a direct call of the accessor. A fraction in an int column truncates,
  as `SPIA_US_S`'s `int()` does, so a frequency written `12.5` is monthly.
- A value of `form`, `reduction_trigger`, `timing` or `mort_basis` none of `SPIA_US_S`'s
  values names, compared exactly, case and whitespace included, by the decode that reads
  it, with `SPIA_US_S`'s message, `invalid form`, as at stage `E`; and a frequency other
  than 12, 4, 2 or 1, `invalid frequency`.
- An attained age a table lacks, by its reader, naming the point, the age and the life,
  where `SPIA_US_S`'s `.loc` raised `KeyError`: `point_id 8: mort_table.csv has no
  mort_rate at attained age 65 for the sex of life 1` on a point on the table basis whose
  sex the table lacks, which is schedule 0, and the same at 17 on a `certain_only` annuity
  issued at 17 on the shipped tables, which start at 40.
- By `proj_len()`, before the stop rule, a contract the caches do not hold and no contract
  is, each covered life's issue age asked, in this order: a covered life issued below
  `issue_age_min` on any form, `point_id 8: issue age -1 is below issue_age_min, 0`, and an
  elected certain period above 1,440 months, `point_id 5: certain_months 1441 is above 12 *
  (omega_age - issue_age_min), 1440, the longest certain period the caches are sized for`;
  then, as at stage `E`, a point at or past the stop rule and a contract owing nothing.
- A timing, a kind or a life a cell does not take, `ValueError("invalid timing")`,
  `ValueError("invalid kind")` and `ValueError("invalid life")`, where it is inside the
  cell's cache: `pols_if_at(0, 2)`, `claim_pp(0, 1)` and `claim_pp(0, 2)`, and a life of 0,
  `lives_if_init(0)`, `death_mth(0)`, `age_at_entry(0)` or `mort_schedule(0)`; and a
  `commute_disc_convention` that is neither code, 2 say, `invalid commute_disc_convention`,
  wherever a certain month remains to discount.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1562)` and `net_cf(-1)`, which modelx answers with 0, the month being outside
cover; `pols_if_at(0, 3)` and `claim_pp(0, 3)`, which modelx refuses as `invalid timing`
and `invalid kind`; `lives_if_init(3)` and `death_mth(3)`, which modelx refuses as
`invalid life`; `cum_annuity_pp(1442)`, `annual_income(122)` and `surr_charge_rate(122)`,
which modelx computes, `cum_annuity_pp(-1)` and `annual_income(-1)`, which modelx reads as
0 and as `B(1)`; and `mort_rate_base_at(121, 1)`, which modelx refuses, naming the age. No
projection makes those calls. An `idx` past the last row is refused in both, with an
`IndexError` at the first read of a vector, and `Projection[-1]` reads every vector at its
last element in both, so it is the table's last point, under that point's own
`point_id()`.

A Reference is a C variable of its value's type: `issue_age_min`, `omega_age`,
`mort_table_year`, the codes, `commute_disc_convention` and `idx` a `long long`, as
`Data.future_horizon_mth` is, and the rates and amounts a `double`. Set past that type, it
is converted when it is set, where modelx keeps the value as given. A float set on an int
Reference is truncated toward zero without a word, `omega_age = 120.7` reading 120, where
modelx computes with the float: `omega_age = 120.0` makes `proj_len()` 696.0 there, and
`result_cf()` then fails. A text, a NaN, an infinity or an int beyond 64 bits is refused at
once, with `TypeError`, `ValueError` or `OverflowError`: so `commute_disc_convention =
"simple"`, which modelx takes and `is_disc_compound()` refuses, cannot be set compiled at
all. An int set on a `double` Reference reads as a float compiled, where modelx returns the
int: `commute_util_base = 1` gives `commute_util_rate(2)` 1 in modelx and 1.0 compiled,
where the cell returns the Reference as it is. Each shipped Reference is a value of its C
type, so no shipped number differs. And a Reference set past its domain computes as C
computes, where modelx raises or turns complex: an `inflation_rate` of `1e300` makes
`inflation_factor(24)` infinite compiled, where modelx's power raises `OverflowError`, and a
`cmt10_shift` of −1.05, a discount rate below −100%, makes point 5's `commuted_value(0)` NaN
compiled and a complex number in modelx.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
best-estimate and the rated rates at 1, `min(q, 1.0)`, as `SPIA_US_S` does. Uncapped, the
monthly rate, `1 − (1 − q)^(1/12)`, would be complex in modelx and NaN compiled, silently.
Capped, both compute 1. A NaN rate would stay NaN through the cap, in both, as through
every other bound, each of which the compiled model computes as a comparison that keeps
the value unless the bound is smaller, or larger: a NaN `mort_ae_factor`, set as a
Reference, makes point 8's `mort_rate(0, 1)`, `lives_if(1, 1)` and `net_cf(0)` NaN in both.
But the payment factor's `max(C, L)` keeps its first argument when the second is NaN, in
both, so `annuity_payments(0)` is 0.0 there, a number: which is why `Data` refuses, on
each point whose projection reads one through such a `max`, a missing amount or rate.

### Speed

`python tools/bench_sec_cy.py immediate_annuity` builds the model into a temporary
directory, or takes a build with `--build`, and times one block run on three engines:
modelx, the export and the compiled model. Each engine runs the committed table repeated,
in a process of its own, as `run_sec.py --block` runs a block, each point projected and
then released. `net_cf` is `net_cf(t)` summed over the frame, the projection alone, as
`basiclife/BasicTerm_SC` is timed on its `pv_net_cf()`; `result_cf` is the report
`run_sec.py` prints, which builds a DataFrame for each point. Each time is the fastest of
three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,006 | 0.808 ms (4.85–5.13) | 1.25 ms (7.51–7.81) | 83 MB |
| export | 616 | 7.66 ms (4.72–4.84) | 8.05 ms (4.96–5.14) | 79 MB |
| modelx | 132 | 197 ms (26.02–26.74) | 200 ms (26.43–27.70) | 137 MB |

On `net_cf` the compiled model runs 9.5 times its export, and on `result_cf`, where building
the DataFrame takes much of its time, 6.4 times; it runs 244 and 160 times modelx. A second
run of the whole benchmark straight after, on a second build of the same files, gave the
compiled model 0.823 and 1.23 ms, the export 7.76 and 8.35 ms and modelx 194 and 203 ms, 9.4
and 6.8 times the export. The compiled model runs fewer times its export than `UL_US_SEC`,
12.0, or `VUL_US_SEC`, 13.8, about as many as `Term_US_SEC`, 9.5: of its 0.81 ms, making and
releasing the ItemSpace, which Python zeroes, takes about 0.26 ms. As it stood after running
in force, compiled the same way, the model ran 2.0 times its export (*What compiling
changed, and why*, above, measured once on a build not shipped, so not reproducible from the
repository), and the compiled model runs about 10 times that build on the same
measure, 0.76 ms a point over the committed points against 7.57: the representation, not the
compiler, is the gain, and the export gained from it too, 7.37 ms a point against 14.9. The
release keeps a block flat: the compiled model's peak grew by 2 MB over its 6,006 points,
and without the collection after each release (`--no-collect`), 506 compiled points peaked
at 540 MB. Reading the four files and building every `Data` vector and array for those
points took 0.04 s, and asking every point for its frame, the runner's first pass, 1.7 s,
most of it making and releasing an ItemSpace a point.

Measured on 2026-11-13 on a desktop shared with other work: 12 cores and 20 threads (an
Intel Core i7-12700KF), 64 GB, Windows 11; Python 3.13.18, its extensions compiled by MSVC
14.37 (Visual Studio 2022), with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.1, numpy
2.5.4 and pandas 3.1.1. Windows reports no load average: sampled every 10 seconds, the
processors were 7 to 24% busy during the runs, mostly 10 to 15%, of which the benchmark's
own process, one thread, is 5 points, and a probe of this page's ran beside the second run's
last modelx runs. Each time is the fastest of three runs; the fastest run is the one to
compare. The comparisons over the committed points, with the build as it stood after running
in force, are the fastest of three rounds each, in one process an engine, and so is the cost
of an ItemSpace, the fastest of five rounds of 1,000.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 to 15, commencing
  at the valuation date, every cell of `SPIA_US_S`'s agrees at every argument `SPIA_US_S`
  evaluates in its own sweep, but for `pols_if_init`, `model_point` and `result_pols`, whose
  meaning changed; `SPIA_US_S`'s `claims(t, None)` and `claims(t, "REFUND")` are compared
  with `claims(t)`, through the spec's `twin_arg_map`, and its timing and kind strings with
  the codes. A cell this model lacked would fail it. So the goldens
  `tests/test_immediate_annuity_us.py` asserts on those points — every row of the
  worked-example table under both triggers, the income levels behind it, the notes' five
  traces and the pitfall cases — hold here with no number restated. The identity holds on
  any count, since neither model charges acquisition. The same suite holds the model to the
  conventions every `_SEC` model meets: every frame starts at `t = 0`, new business joins
  the `BEF_NB` count and enters once at its `policy_count`, nothing happens before the
  annuity commences, and the in-force columns are present; and to `SPIA_US_S`'s product
  fact, that the gross outgo is never negative. The convention that `pols_if` is the
  `BEF_DECR` count is skipped, because `pols_if` is the closing measure (*Counts and
  timings*).
- **The splice**, in `tests/test_immediate_annuity_us_sec.py`: each `SPIA_US_S` point
  restated in payment at months either side of its events continues the S projection, in
  `result_cf`, in `result_pols`, column by column, and in every other cell the two share, to
  1e-9 relative with no absolute floor, which would hide the survival near the limiting age,
  but for the cells the twin identity skips and the two whose value is a frame length or a
  time point on the valuation clock, `proj_len` and `payment_surv_mth`. The months are those
  S's events need: the first anniversary and the months either side of it, the worked
  example's month of death and the month after, both lives dead, the second withdrawal and
  the month after the residual floor binds, the last month of each certain period and the
  first after it, the trim months of the installment refunds, the last month of a frame,
  either side of the limiting age inside a certain period, and months between quarterly or
  semi-annual instalments. So do eleven variants of S's points, in a copy of S's table that
  is never committed, for branches S's own points do not reach: every frequency on both
  timings, a cash refund on the table basis and one on a joint contract, an installment
  refund on a COLA path that commutes, one paid in advance, one that never repays its
  premium and one whose first instalment repays it, the primary trigger on the table basis,
  rated and commencing in 2020, commutation barred by the issue state, commutation on
  `certain_only`, and a certain period that outlasts the age stop, with premium tax and
  qualified money. Inflation, the one input on the valuation clock, is set to 0 in both
  models. Commutation, which ships at zero utilization, is switched on in both at 0.5, and
  the CMT is set 50 basis points up since `SPIA_US_S`'s annuity dates, its `cmt10_shift` at
  0.005, because at the shipped zeros neither the commutation fraction nor the CMT's change
  shows in any comparison. This model reads the splice's table once, as a block is read, on
  one path of the CMT: a point restated in payment has seen `SPIA_US_S`'s change by the
  valuation date, and carries it as `cmt10_shift_init`, and nothing changes after it, so
  this model's `cmt10_shift`, the change made at the valuation date, is 0; a point
  commencing later has seen no change and sees none, so it is compared with `SPIA_US_S` read
  again with its `cmt10_shift` at 0, the same contract on that path. In both copies the
  improvement scale is set apart by age and sex, because the shipped scale is the same for
  both sexes at every age and flat at 0.01 to age 85, where a join on the wrong sex or age
  would read the same number. Improvement itself is not neutralized: it is dated by the
  calendar on the policy clock.
- **The core grid and the full one.** By default the splice and the future business run a
  core of their cases, which between them reach every form, trigger, basis, timing and
  frequency, every opening-state column at every value it takes, every kind of valuation
  month and every branch the full grid reaches, and each frequency and timing other than
  monthly that a refund or commuting point carries is valued off its payment period by some
  core case; a test asserts all of it. The other cases carry the `sec_full` marker and show
  as skipped, with the reason, unless `USLIB_SEC_FULL=1` is set. One leg of the CI matrix
  sets it, so every CI run runs the full grid too.
- **Future new business**: commencing 13 months after the valuation date, more than a year
  on and off every payment step, each S point and each variant is the S projection moved
  on, with zeros before the annuity date in `result_cf` and `result_pols`, no decrement rate
  evaluated there and neither table read below an issue age; and so are the anchor cell on
  the table basis and the commuting point commencing 12 months on, and the worked
  example's anchor cell commencing a month on.
- **How it computes**: on every row the splice and the future business compare, the core
  by default and the full grid with `USLIB_SEC_FULL=1`, after every report, no cell has
  been called at a negative argument, none evaluated from `t_entry()` on has read a month
  before it, none evaluated at month `t` has read a month later than `t + 1`, and every
  policy-clock and age argument is one the contract has: the payments to date, the
  schedule, the income, the utilization and the surrender charge from the annuity date to
  the stop rule, and the two table readers from each life's issue age to its age in the
  last month, below the limiting age. On a fresh read of the committed model,
  `duration_mth(500)` evaluates `duration_mth` once, because the policy clock is a closed
  form, and every point is swept under modelx's recursion limit lowered to 40, which a
  recursion backward over the frame would exceed. And a cold `net_cf` in the last month
  runs no deeper than one cell a month back to `t_entry()`, plus a fixed overhead, on the
  anchor cell's twins on both bases, on the cash refund in payment 13 months and at the
  longest cover the product allows.
- **Counts, validation and regeneration**: the count is on the books from the annuity date
  to the stop rule, and `pols_if_at` refuses a timing it does not have; `pols_if` is the
  closing obligation measure on that count; `result_pols()` is `SPIA_US_S`'s, column for
  column, with `pols_new_biz` beside it; multiplying `policy_count` by 2.5, a count that is
  not whole, with commutation and the CMT's change switched on at the splice's values,
  multiplies every cash flow, the surrender charge and the counts at each timing, and moves
  no per-contract value. Each malformed row is refused naming its point, each on a model
  read for it and again through a projection, and each by the one rule under test: among
  them a count, a duration, a probability, a fraction or a CMT change that is not a number,
  a state other than the annuity date's on a contract not yet in payment, a second life on a
  single-life contract, a month of death written as text or as a fraction, on either basis,
  a scenario life whose status is not its month of death's, and a commutation fraction where
  none could have been taken, a certain period of 0 months among them. A malformed
  surrender-charge scale is refused naming the file, the same way, and one written as floats
  is read by value. Each kind of contract owing nothing, and a point at or past the stop
  rule, is refused by `proj_len()` with its message, and `run_sec.py --block` refuses such a
  table before printing anything; the horizon is a Reference, which at 0 refuses any future
  business, saying so; an unknown form, trigger, timing, basis, frequency or discount
  convention is refused where the projection meets it, and so are a third life, a claim kind
  and a timing neither model knows; a zero count, integer columns written as floats, an
  annuity commencing 120 months on, a month of death written as −1 on a living life, a
  commutation fraction from policy month 13, a fall in the CMT since the annuity date and a
  fraction past the residual floor are accepted; and the committed table is what `SPIA_US_S`
  generates.
- **The opening state and the rest**: the derived rows carry the worked example over at the
  valuation date, with the figures above; each life's survival opens at its column and runs
  on as `SPIA_US_S`'s does; the payments to date are `SPIA_US_S`'s at every key, read on a
  fresh model from the valuation date's policy month on; the commutation fraction carries
  over in force, and zeroed gives the figures above; at a utilization of 1 the residual
  floor caps a withdrawal in force, leaving the smallest certain instalment at $100, which
  the splice's 0.5 never does; the simple discount convention continues `SPIA_US_S` too;
  three contracts in one table, in payment, commencing at the valuation date and commencing
  later, read each the CMT's change since its own annuity date, on one path, with
  `cmt10_shift` at 0 and at 0.005, the last unmoved by it; improvement is dated by the
  calendar on the policy clock; where a cap on mortality binds, at the limiting age on the
  anchor's twin and on rows in payment, one of them rated past 1 at 117, the annual and
  monthly rates are the float 1.0, every life alive at the start of the month dies in it,
  and every report is float64 and finite; a NaN sent to either cap, through
  `mort_rate_base`'s or `rating_factor`'s formula replaced, stays NaN; expense inflation
  runs on the valuation clock at the shipped 2.5%, which only this test sees, since the
  splice sets the rate to 0; an annuity commencing later brings no premium and no
  acquisition cost; the model has `pols_new_biz` and no lapse; the stop rule ends every
  frame; every guarded cell holds its value outside the frame and reads no rate there; the
  points of a block sum row by row; an extract without the generator's three columns,
  relabelled and reversed, projects the same numbers; `run_sec.py` prints the model's
  numbers, for a point commencing at the valuation date, one in payment, one in its last
  month, a one-row frame its headings call one row, one commencing later and the block; the
  docstrings describe the valuation clock and map every cell running in force adds; and the
  model reads `SPIA_US_S`'s assumption tables in place.
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py SPIA_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their call
  syntax changed: a point's position for its label, the codes for the text of a timing, a
  kind or the discount convention, and `claims(t)` for `claims(t, kind)`. Each point is
  named by its label, in `point_id()`, in a refusal and in `run_sec.py`'s output.
- **What compiling changed**: each value a point's projection cannot use, text, a blank or
  infinite amount or rate where a `max`, a `min` or a search reads it, an int `int()` cannot
  read or of `2**53` or more in size, is refused by the point's own accessor, in a
  projection and by a direct call, naming the point, while the table reads and every other
  point projects the committed numbers exactly, a point holding the same value outside the
  accessor's scope among them; a fraction in an issue age, a certain period or an annuity
  year truncates, as `SPIA_US_S`'s `int()` does, and the point projects the committed
  numbers; a point issued below `issue_age_min`, 0, on a lifetime form or the `certain_only`
  form, a joint annuitant on each among them, and a certain period above 1,440 months are
  refused by `proj_len()`, naming the point, and each projects once its bound is moved; a
  `certain_only` annuity at issue age 0, the longest cover the caches hold, and at 17, a
  single life annuity at 17 and a joint life annuity whose joint annuitant is issued at 0,
  below the 18 `product-spec.md` issues lifetime forms at, project, and each but the second
  is `SPIA_US_S`'s in every cell; on an improvement scale holding a sex the mortality table
  lacks, both written out of their keys' order, each table is numbered by its own sexes,
  each life reads its own sex's row, and the points project the committed numbers; the
  padding beyond each table's extent is NaN, each reader refuses an age below its table's
  first, and a sex the table lacks is refused at the first age read, where a point on the
  scenario basis with the same sex projects; on tables whose sexes start at different ages,
  each reader reads within its own sex's ages and refuses an age below them, naming the
  point, the age and the life; every `Data` cell but the readers is the int64 or float64
  array, or the int, that the `Data` docstring's table states; each size in `spec_sec.py` is
  the one its comment derives from the model's References, every 2-D cache one inner width,
  and the codes dense from 0, the sample's recursion limit is the one its comment derives,
  and the sample calls `sex` on a second instance whose table's sexes are blank; and outside
  the repository, beside a copy of the model or at a path too shallow to hold one,
  `run_sec.py --cython` says it cannot build.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting ones refers to pandas, numpy or another module, reads a table
  with `.loc` or the like, calls a reporting cell, holds text but in its docstring and its
  refusals, or holds a generator, a comprehension or a nested function; none calls
  anything but a cell, a `Data` vector and the builtins of *No Python call kept*, and the
  registry admits no other for this model; every `Data` vector a formula reads is an int64
  or float64 array, read by element; no cell is uncached; and each label accessor returns
  its point's column on every point, of its own name or as the registry's
  `"reporting_columns"` names it, and each such entry is needed.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting ones a C `bint`,
  `long long` or `double` and a C-array cache of exactly the spec's size, and every new
  `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps no
  Python object among a projection cell's locals, calls no Python builtin there, and builds
  no container, under both directives (C3); on the committed points, every cell at every
  argument a full modelx sweep caches is what modelx computes, bit for bit on x86-64, and so
  is every raise and every `Data` array (C4); and `run_sec.py --block`, run compiled, holds
  one point's ItemSpace at a time. In `tests/test_immediate_annuity_us_sec.py`: the same
  comparison on the splice grid, the core by default and the full grid with
  `USLIB_SEC_FULL=1`, twenty rows at a time, each life's death density with every other
  cell; at the contract's extremes, the longest frames, the youngest and oldest issue ages
  and the longest certain period, on age tables extended to age 0 with a value of their own
  at every age and sex; where the residual floor binds, and its cap on the fraction
  commuted is reached, and under the simple discount, each set through References and
  first shown to bind in modelx; where the cap on mortality
  binds, and where a NaN A/E reaches it; on keys written as floats, where every `Data` array
  is first held to its dtype and values on the keys as written, in modelx, in seconds; and
  on a sex that is a number or blank, which `sex` returns as modelx does; the compiled model
  refuses what modelx refuses, with modelx's message, on the relabelled extract, every
  refusal of the module among them, and an argument past a cache, either side, raises
  `IndexError`; the deepest call the contract allows runs cold on a 1 MiB stack and on the
  main thread, and the test reports the smallest of nine stacks, 256 KiB to 2 MiB, it ran
  on, waiting a bounded time for each; a Reference set after the model has computed changes
  no value it has cached; and `run_sec.py --cython` prints what `run_sec.py` prints, and
  refuses a directory that holds no build. They are marked `cython`, and they skip without
  the toolchain, but in the `cython` CI job, which installs it on Linux and on Windows, one
  leg a product, a skip fails, whatever made it.

```bash
python -m pytest tests/test_immediate_annuity_us_sec.py -q
USLIB_SEC_FULL=1 python -m pytest tests/test_immediate_annuity_us_sec.py -q   # full grid
python -m pytest tests/test_model_conventions.py -q -k "[SPIA_US_SEC]"
python -m pytest tests/test_compiled_conventions.py -q -k "[SPIA_US_SEC]"
python -m pytest tests/test_immediate_annuity_us_sec.py -q -m cython  # the compiled tests
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R2]: #uslib-immediate_annuity-r2
[REG-R36]: #uslib-reg-r36
[std]: #uslib-std
<!-- END generated citation links -->
