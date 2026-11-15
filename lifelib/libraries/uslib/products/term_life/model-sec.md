# In-Force Implementation Notes

**Status:** Draft, 2026-11-01. `Term_US_SEC` is [`Term_US_S`](model.md) taught to project
from a valuation date. Besides policies issued at that date, it takes policies already in
force there and policies to be written in the ten years after it, as lifelib's
`basiclife/BasicTerm_SE` extends `basiclife/BasicTerm_S`. The product is the one
[`product-spec.md`](product-spec.md) specifies and
[`technical-notes.md`](technical-notes.md) models; this page says what running in force
changes, and how the model compiles. The suffix adds lifelib's letters to `S`: `E` for in
force, as in `BasicTerm_SE`, and `C` for the compiled form, as in `basiclife/BasicTerm_SC`:
the same formulas compile under modelx-cython, from `sample_sec.py` and `spec_sec.py`
beside the model.

> **This is a mechanics demonstration, not a pricing or reserving result.** The model is
> `Term_US_S` on another time axis, and it reads `Term_US_S`'s assumption tables in place,
> every assumption unchanged: the contractual elements are sourced from a specimen policy
> [S6], and every behavioural and expense assumption is a **[std]** standardization.
> Replace them with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/term_life/run_sec.py            # point 1: the anchor cell, issued at t = 0
python products/term_life/run_sec.py 4          # point 4: the anchor cell in force mid-ART
python products/term_life/run_sec.py --block    # every model point, summed row by row
python products/term_life/run_sec.py 4 --cython # point 4 on the compiled model
```

`--cython` runs the compiled model and prints the same lines. The runner builds it beside
the model with the repository's `tools/build_sec_cy.py` the first time, in about a minute,
and again whenever the model, `sample_sec.py`, `spec_sec.py` or the tool is newer than the
build, and says so on stderr. Nothing the build leaves there is committed, and
`.gitignore` covers it.

The first prints the twelve rows `run.py` prints for `Term_US_S`'s point 1, with the
policy counts behind them. Three lines to the same thing for point 4:

```python
import modelx as mx
model = mx.read_model("products/term_life/Term_US_SEC")
model.Projection[3].result_cf()      # point 4, the table's fourth row
```

`Projection` takes `idx`, the position of a point in the table, as `basiclife/BasicTerm_SC`
does: `Projection[3]` is point 4, and its `point_id()` says so. `result_cf()` has
`Term_US_S`'s columns — `pols_if`, `premiums`, `claims`, `commissions`, `expenses`,
`premium_taxes`, `conv_credits` and `net_cf` — with one row per month from the valuation
date, `t = 0 … proj_len() − 1`. `result_pols()` sets out the counts behind it on the same
rows: `pols_if`, `pols_new_biz`, then the month's deaths, conversions and lapses in
processing order, and the expiries of the last covered month. `result_cf_annual()` sums
`result_cf()` into policy years, as in `Term_US_S`, and leaves out the months before
issue.

`--block` projects every point and releases its ItemSpace once its frame is read, so the
run holds the cells of one point at a time. Deleting it, `del model.Projection[idx]`, is
not enough: an ItemSpace sits in reference cycles, which only Python's cyclic collector
frees, so the runner collects after each release. It freezes everything alive
(`gc.freeze()`) once the model and its table are read, and again once it has asked every
point for its frame, so that each collection scans only what the block has made since.
It keeps the block's sum as it goes, compensated as pandas sums a `groupby`, so that the
block is, bit for bit, the frames concatenated and summed by `t`, as below (*The compiled
model* has the measurements).

## Two clocks

The model runs on two clocks, and each formula reads the one its quantity belongs to.

- **`t`, the valuation clock**, counts months from the valuation date. `t = 0` is the
  valuation month for every model point, however old the policy, and the frame runs
  `t = 0 … proj_len() − 1`, where `proj_len()` is the number of months from the valuation
  date to the end of cover.
- **`duration_mth(t)`, the policy clock**, counts the months the policy has been in force
  at time `t`: `duration_mth(t) = duration_mth_init() + t`, with `duration_mth_init()` read
  from the model point. It is the technical notes' month index, and the contract runs on
  it: `duration(t) = duration_mth(t) // 12`, `policy_year(t) = duration(t) + 1` and
  `age(t) = age_at_entry() + duration(t)`, as in `Term_US_S`. `BasicTerm_SE` reaches the
  same numbers by adding one a month, a recursion as long as the frame; the closed form
  needs no such chain of calls.

Point 4 is the anchor cell in force 126 months. At `t = 0` it is in policy year 11, at
attained age 45, six months into its first ART year. Its next premium, policy year 12's
$830, falls due at `t = 6`, its eleventh anniversary, and its frame has 594 rows,
`t = 0 … 593`. Point 6 is the anchor cell to be issued three months after the valuation
date: `duration_mth(0) = −3`, it is on the books from `t_entry() = 3`, rows 0 to 2 are
zeros, and its frame has 723 rows.

| Read on the policy clock | Read on the valuation clock |
|---|---|
| the premium schedule and the months premiums fall due, the jump ratio, the shock lapse month, the lapse and commission scales, base mortality at the attained age, post-level-term mortality, the conversion window and credit, expiry at attained age 95 | expense inflation, `inflation_factor(t) = 1.02^(t/12)` |

Expense inflation alone runs on `t`, so the maintenance charge is in valuation-date dollars,
for every point alike. Acquisition is a flat $300 per policy issued, charged in the issue
month and not inflated, as in `basiclife/BasicTerm_SE`.

Because row `t` is the same month for every point, the frames of a block line up and sum
row by row, which is what `run_sec.py --block` prints:

```python
import pandas as pd
frames = [model.Projection[i].result_cf()
          for i in range(len(model.Data.model_point_table()))]
block = pd.concat(frames).groupby(level="t").sum()
```

`run_sec.py --block` keeps one frame at a time, and adds each to a running sum with the
compensation pandas' `groupby` sum carries, in the same order, so its block is this one's
to the last bit, on the committed points and on 155 more (a naive running sum differs
from it in 851 of the committed points' 5,784 values, by up to 3e-16 relative).

On a point issued at `t = 0` the two clocks coincide, and the model computes what
`Term_US_S` computes, with one difference by design: acquisition is charged per policy
issued, where `Term_US_S` charges it once per model point, whatever the count. On
`Term_US_S`'s own points, which count one policy each, every cash flow and every count
agrees, and so does every other cell the two models share but two whose meaning changed:
`pols_if_init()`, now the count already in force at the valuation date, 0 for new
business, and `model_point()`, a row of another table.

## The in-force interface

The model point table is `model_point_table_sec.csv`. It carries `Term_US_S`'s columns, two
of them restated as the in-force interface under `basiclife/BasicTerm_SE`'s names:

| Column | Unit | Measured at | Meaning |
|---|---|---|---|
| `policy_count` | policies, not necessarily whole | for a point in force, the start of month 0, before any month-0 event; for any other, its issue month | the policies in force at the valuation date, for a point already in force; the policies issued, for one issued at or after it |
| `duration_mth` | whole months | the valuation date | the policy's age in months: positive in force, 0 for a policy issued at the valuation date, `−k` for one to be issued `k` months later, with `k` at most 120 as shipped |

Term's only state variable is the in-force count, so these two columns are all it takes to
open a policy in force. Everything else the projection uses is fixed at issue, in
`Term_US_S`'s columns, or follows from the policy clock. The premium is read from the
guaranteed schedule by policy year, not solved, so no premium fixed at issue has to be
carried, and the jump ratio, the M(1) rule, the conversion window and the expiry month all
follow from columns fixed at issue.

| `Term_US_S` | `Term_US_SEC` | Why |
|---|---|---|
| `pols_if_init` (1.0) | `policy_count` | The count, under BasicTerm_SE's name. `pols_if_init()` now means the count in force at the valuation date, 0 for a point issued at or after it |
| `duration_inforce` (years, read by no formula) | `duration_mth` | The policy clock, in months; the S column is dropped |

The columns carried over are read as `Term_US_S` reads them. For a policy in force, the
facts they record are still those at issue, the premium mode excepted:

| Column | Unit | Measured at |
|---|---|---|
| `point_id`, `policy_id` | labels | — |
| `age_at_entry` | years, age nearest birthday | issue, not the valuation date: `age(0)` is the attained age there |
| `sex`, `rate_class`, `plan` | codes, as in `Term_US_S`'s table | issue |
| `sum_assured` | dollars, level for the life of the policy | issue |
| `premium_mode` | `A`, `SA`, `Q` or `M` | the mode billed over the frame; its instalments fall on the policy clock |
| `plt_mort_factor_override` | a multiplier, blank for the notes' rule | an assumption, not a fact about the policy |

Three more columns, `row_kind`, `source_policy_id` and `source_mth`, record where the
generator took each shipped row from (below). No formula reads them, and an in-force
extract need not carry them: without them the model projects the same numbers, and
`run_sec.py` runs.

`Data.model_point_table()` checks the table as it reads it, over all rows at once. The
first check that fails raises `ValueError`, naming the missing column or every point that
fails it:

- both in-force columns are present;
- no `point_id` appears twice;
- `policy_count` is a number, zero or more, so not blank, text or infinite;
- `duration_mth` is a whole number of months;
- `duration_mth` is −120 or more. Future new business is written over a horizon,
  `Data.future_horizon_mth`, 120 months as shipped, so that no frame runs longer than cover
  from issue plus ten years. Set to 0, the Reference refuses future new business
  altogether.

A point whose cover had ended by the valuation date,
`duration_mth ≥ 12 × (95 − age_at_entry)`, reads, but `proj_len()` refuses it, naming the
point: the end of cover is the product's rule, not the table's. So does a point the
contract does not issue, whose plan's level period is below ten years,
`Projection.policy_term_min`, the shortest plan's, as `T5`'s is, or whose issue age is
below 18, `Projection.issue_age_min`, the youngest every plan issues at
([`product-spec.md`](product-spec.md)). `Data` reads both as `Term_US_S` reads them, and
`Term_US_S` projects them as far as its tables go, but the compiled model's caches are
sized from the contract (*The compiled model*, below). A loop over the block meets such a
row only when it reaches it, after projecting the points before it, so
`run_sec.py --block` asks every point for its frame before it projects any, and stops
before it prints anything.

## The model points

No row of `model_point_table_sec.csv` is typed by hand. Every one is generated from
`Term_US_S` and its table by `tests/sec_support.py`, from the `Term_US_SEC` entry in its
`SEC_SPECS`, and the tests regenerate the table and compare, so an edit to a `Term_US_S`
row reaches it or fails the suite. In the source repository,
`python tools/gen_sec_points.py Term_US_SEC` writes it.

| Point | Kind | From | At the valuation date |
|---|---|---|---|
| 1, 2 | twin | S points 1 and 2 | issued at `t = 0`: `Term_US_S`'s worked example |
| 3 | derived | S point 2 at S month 12 | in force at its first anniversary, the shock lapse 107 months ahead |
| 4 | derived | S point 1 at S month 126 | midway through its first ART year |
| 5 | derived | S point 1 at S month 719 | in its last month of cover: a one-row frame |
| 6 | future | S point 1, 3 months on | to be issued at `t = 3` |

A derived row's `policy_count` is the count `Term_US_S` carries into that month, its
`pols_if(d)`, so the row continues the S projection from there: point 4 opens with 0.108385
policies. Its `policy_id` is the S row's with the month appended, `TL-000001-M126`, and a
future row's carries the months to issue, `TL-000001-F3`. Row `t` of a generated point is
month `t + source_mth` of its S point. All six are on the anchor configuration, T10 / M /
StdNT / band 1 / annual mode, because the specimen gives a guaranteed premium scale for
that cell alone [S6]; a point on any other plan, sex, class or band needs
`premium_rates.csv` extended first.

## Counts and timings

`pols_if_init()` is the count in force at the valuation date: `policy_count` for a point
already in force, 0 for any other. `pols_new_biz(t)` is `policy_count` in the issue month,
the month with `duration_mth(t) = 0`, and 0 in every other. `pols_if_at(t, timing)` has two
timings, `basiclife/BasicTerm_SE`'s, each an int Reference named as `BasicTerm_SE`'s
string, so that a timing, like every argument, is a C number when the model compiles:

- `BEF_NB = 0`, the count carried in from month `t − 1`, before month `t`'s new business:
  `pols_if_init()` at `t_entry()`, the first month on the books, and the survivors of
  month `t − 1` after it;
- `BEF_DECR = 1`, that count plus `pols_new_biz(t)`, before month `t`'s decrements.

Any other timing raises. The survivors carried into month `t` are those of month `t − 1`'s
`BEF_DECR` count, which `BEF_NB` forms itself, as its own value at `t − 1` plus that
month's new business, exactly the sum `BEF_DECR` returns. So the chain of calls from
month `t` back to `t_entry()` is one cell a month, as deep as `Term_US_S`'s `pols_if`
chain. On a model just read, a cold `net_cf` in the last month of a 720-month frame runs
728 cells deep, against 726 in `Term_US_S`, the two more being the two timings `pols_if`
passes through, and at the longest frame the contract allows, issue age 18 and issued 120
months on, it runs 932 deep.

`pols_if(t)` is `pols_if_at(t, BEF_DECR)`, the count that weights row `t`, and on a point
issued at `t = 0` it is exactly `Term_US_S`'s `pols_if`. `BasicTerm_SE`'s third timing,
`"BEF_MAT"`, is not adopted, nor is its `pols_if`, which is the count before maturity:
here the policies expire at the end of the last covered month, as `pols_maturity`, where
`Term_US_S`'s worked example puts expiry. The roll-forward closes as

```
pols_if(t) − pols_if_at(t + 1, BEF_NB)
    = pols_death(t) + pols_lapse(t) + pols_conv(t) + pols_maturity(t)
```

at every `t` of every frame, and `pols_if(t + 1)` adds `pols_new_biz(t + 1)` to the count
on the left.

Cover is `is_active(t)`, `0 ≤ duration_mth(t) < expiry_mth()`, and outside it, before
issue and from expiry on, every count is zero, and so every cash flow. No count evaluates a
decrement rate there, and no table is read at a policy year or an attained age the policy
does not have: `prem_due`, `premium_pp_ann`, `mort_rate_base`, `conv_elig` and the
commission scale `comm_rate` are zero or false outside cover.

## Departures from Term_US_S

Each formula that tested `t` against a contractual event now tests the policy clock, and
each read of a contractual schedule at a month is a read at a policy year. Where
`Term_US_S`'s test would have stayed correct on the valuation clock, it moved anyway, so
that cover has one definition. Ten cells are new for running in force, and two more for
compiling, `point_id` and `premium_schedule` (*The compiled model*, below). None of
`Term_US_S`'s 52 is removed, which the twin identity asserts: a cell of `Term_US_S`'s that
this model lacked would fail it. One departure comes from neither the clock nor running in
force: the notes' M(1) rule and the post-level-term grading write their bounds second, as
`mort_rate` writes its cap in both models, so that a NaN stays NaN; `Term_US_S` writes
them first (below).

| Cells | `Term_US_S` | `Term_US_SEC` | Why |
|---|---|---|---|
| `duration_mth` | `t` | `duration_mth_init() + t` | The policy clock, opened from the model point |
| `proj_len` | `12 × (95 − x)`, the months from issue | `expiry_mth() − duration_mth_init()`, the months from the valuation date; raises past cover, and on a point the contract does not issue | The frame starts at the valuation date. `expiry_mth()` keeps `Term_US_S`'s formula, and the compiled caches hold the contract's frames alone |
| `pols_if`, `pols_if_init` | a recursion from `pols_if_init()`, the column's 1.0, at `t = 0` | `pols_if_at(t, BEF_DECR)`, from `t_entry()`; `pols_if_init()` is 0 unless in force | Policies in force at the valuation date open the count; new business joins it in its issue month |
| `jump_ratio` | `AP(12n) / AP(12n − 1)`, policy months passed as `t` | `premium_pp_ann_py(n + 1) / premium_pp_ann_py(n)` | On the valuation clock, month `12n` is not policy year `n + 1` |
| `lapse_rate_mth` | the shock at `t = 12n − 1` | at `duration_mth(t) = 12n − 1` | The shock is a policy month |
| `conv_rate` | the final eligible year found by `conv_elig(t + 12)` | `conv_elig_py(policy_year(t) + 1)` | A question about the next policy year, asked by policy year rather than twelve months ahead |
| `expenses` | acquisition, $300 once at `t = 0`, whatever the count | `expense_acq × pols_new_biz(t)` | A point already in force bears none, and one issued later bears it in its issue month, per policy issued and not inflated, as in `basiclife/BasicTerm_SE` |
| `inflation_factor` | `1.02^(t/12)`, `t` the policy month | the same formula, `t` the valuation month | Unit costs in valuation-date dollars |
| `pols_maturity`, `phase` | expiry at `t = proj_len() − 1`, and `t ≥ proj_len()` | at `duration_mth(t) = expiry_mth() − 1`, and `≥ expiry_mth()` | One definition of cover, on the policy clock; `phase` gains `PRE_ISSUE` |
| `prem_due`, `premium_pp_ann`, `mort_rate_base`, `conv_elig`, `comm_rate` and the decrement counts | unguarded: no `Term_US_S` frame has a month outside cover | zero or false outside cover, before any table or rate is read | A policy year or an attained age the policy does not have is never looked up, and no scale reads a month before issue as a policy year |
| `plt_mort_factor_init_formula`, `plt_mort_factor` | `min(8.0, …)`, `max(2.0, …)` | `min(…, 8.0)`, `max(…, 2.0)` | A NaN stays NaN, as at the cap; the same float wherever the argument is a number (below) |
| `result_cf_annual` | whole policy years | the policy years in the frame, the months before issue left out | An in-force point's first row holds the rest of its current policy year, and its `pols_if` is the count at the valuation date |
| `result_pols` | — | new | The counts behind `result_cf()`, after `basiclife/BasicTerm_SE`'s `result_pols()` |

Of the cash flows, the change of clock moves the maintenance expense alone, and `net_cf`
with it. A point in force carries that expense in valuation-date dollars, so point 4's
`expenses(t)` is `Term_US_S`'s `expenses(126 + t)` divided by `1.02^(126/12)`, about 1.231.
Its `pols_if`, `premiums`, `claims`, `commissions`, `premium_taxes` and `conv_credits` are
`Term_US_S`'s from month 126 on. Point 6 is `Term_US_S`'s point 1 three months on in those
six columns too; its maintenance expense is `1.02^(3/12)` above S's, and its acquisition is
$300 exactly.

`mort_rate` caps the annual rate at 1, written `min(q, 1.0)`, the product first and the
bound second, as `Term_US_S` writes it (below). Past 1 the monthly rate,
`1 − (1 − q)^(1/12)`, has no real value. At 1 it is 1, so every policy in force at the
start of the first month the cap binds dies in that month, and none is in force after
it. On the shipped mortality and class tables the product passes 1 only after the level
period. At the issue ages [`product-spec.md`](product-spec.md) admits, it first does so,
at the lowest M(1), in the tobacco class on the twenty-year plan issued at 65, its oldest
tobacco issue age: at attained age 94, the tenth PLT year, once M(1) passes 5.9152, which
the notes' rule gives at a jump ratio past 9.9367. There a non-tobacco class needs an M(1)
above 8, the most the rule gives, so an override. The model does not refuse an older
issue age. Where the first PLT year falls at attained age 94, as on the ten-year plan
issued at 84, the product passes 1 there once M(1) passes 4.5652 in the tobacco class and
7.9891 in the standard non-tobacco class, the least M(1) that does so on any point the
model projects. At M(1) = 8 the anchor cell issued at 70 in the tobacco class passes 1 at
attained age 90, in policy year 21, as a test shows (*Tests*, below). No committed point
comes near it, nor any point of the splice grid.

The order of the cap's arguments matters. Python's `min` and the compiled cell alike keep
the first argument unless a later one compares smaller, and no comparison with NaN holds,
so `min(1.0, q)` is 1.0 where `q` is NaN: a blank class factor would read as certain death
in the first month, every count and cash flow finite. `min(q, 1.0)` is NaN there, in both
engines, and wherever `q` is a number it is the float `min(1.0, q)` is, 1.0 included, so
the order changes no number the model computes. The notes' M(1) rule,
`min(8.0, 1 + 0.55 × (J − 1))`, and the floor of the post-level-term grading,
`max(2.0, …)`, are written with their bounds second for the same reason, where
`Term_US_S` writes them with their bounds first, and are the same floats wherever their
arguments are numbers. An infinity is a number, though, and the cap reads an infinite
class factor as certain death in either order, so `Data` also refuses, by name, every
value a cap, a `min` or a `max` reads that is blank, text or infinite (*What it refuses*,
below): no NaN, and no infinity, reaches one.

## The compiled model

The model compiles under modelx-cython into C-typed code, as `basiclife/BasicTerm_SC` does,
and modelx reads and runs the same formulas as before. Compiling changed how each cell
reads its inputs and spells its codes, and no number: what the model computed on each
committed point was frozen before the change, and it still computes it (*Tests*, below).
Cell by cell, at every argument a full modelx sweep evaluates, the compiled model computes
what modelx computes, bit for bit, on the committed points, on the 55 points of the
splice grid, which take the branches they do not, on the contract's two longest frames,
and on points where the cap on mortality binds. The compile tests hold it so on x86-64,
and to 1e-12 relative elsewhere, where no run has shown it yet.

### Building it

In the source repository:

```bash
python tools/build_sec_cy.py term_life                    # in place, beside the model
python tools/build_sec_cy.py term_life --out /tmp/term    # elsewhere, with the CSVs
```

The tool exports the model to `Term_US_SEC_nomx/`, the Python package modelx's `export`
writes, which runs without modelx. It copies the CSVs beside the export when it builds
anywhere but here, because the package reads the CSVs of the directory that holds it. It
then runs mx2cy, modelx-cython's compiler, on the export, with `sample_sec.py` and
`spec_sec.py` (below). The result is `Term_US_SEC_nomx_cy/`, whose spaces are C extension
types, and it is imported as the export is:

```python
import sys
sys.path.insert(0, "products/term_life")      # the directory holding the build
from Term_US_SEC_nomx_cy import mx_model as model
model.Projection[3].result_cf()               # point 4, compiled
```

Compiled, no cache is ever cleared. An ItemSpace takes the References when it is made,
and keeps the values it computes until it is deleted; the base `Projection` and `Data`
keep theirs for good. So `Projection.idx = 3` after `Projection.result_cf()` returns
point 1's frame under point 4's `point_id()`, and `Data.future_horizon_mth` lowered after
the table was read refuses nothing. Set every Reference on a model just imported, before
anything is computed, where modelx would recompute; a test holds the compiled model to
this.

A build takes about a minute with gcc, 53 s here, and needs a C compiler, which is why
`requirements.txt` leaves modelx-cython out: `pip install -r requirements-cython.txt`.
`run_sec.py --cython` builds in place when it finds no build, or one older than the model,
the sample, the spec or the tool, and `--build DIR` runs a build made with `--out DIR`.
Nothing a build writes is committed. All of it derives from committed files, and an
extension module is built for one operating system, processor and Python
(`_mx_classes.cpython-313-x86_64-linux-gnu.so` here); in place, `.gitignore` covers all of
it. A `lifelib.create()` copy of the library carries no `tools/`, so it cannot build, and
`run_sec.py --cython` says so.

### What compiling changed, and why

A compiled cell is fast when its body is C, and types alone do not make it so. Compiled by
the same tool, with a sample of its own, as it stood after running in force, the model
typed 53 of its 62 cells as C numbers and ran only 1.4 times its own export, 21.2 ms a
point on `net_cf` against 29.0, because the bodies of the typed cells still called pandas:
a `model_point()` lookup for each attribute, and a `.loc` on a table for each policy
year's premium and each month's mortality. So each input now reaches a cell as a number:

- **`idx`.** `Projection` is parameterized by the position of a point in the table, from
  0, as `BasicTerm_SC` is: `Projection[3]` is point 4, and `point_id()` returns the label,
  which every refusal names. The position is what indexes the vectors below.
- **`Data`'s vectors.** Each model point attribute a formula uses is a `Data` vector of
  int64 or float64, one element a point, and a cell reads its point's element:
  `age_at_entry()` is `int(data.age_at_entry()[idx])`. Compiled, the vector is a typed
  memoryview, and the read is a load from memory.
- **Text, decoded once.** A C cell holds no text, so `Data` decodes each text column into
  the number it selects, for every point at once: the plan into the level period,
  `policy_term`; the premium mode into the months between instalments, `prem_cycle`, by
  which `modal_factor` selects the mode's factor; the class into its mortality factor,
  `class_factor`; the face amount into its `band`; and a blank M(1) override into a 0/1
  flag beside a value of 0.0, so that no formula tests for NaN. Each decodes as
  `Term_US_S` reads the column, and what it cannot decode it refuses (below).
- **Tables indexed by integers.** The premium schedules, keyed by plan, sex, class and
  band, are numbered, each point carrying the number of its own, `premium_schedule`, and
  held by schedule and policy year in `premium_rates_array`. Base mortality is
  `mort_table_array`, padded from age 0 so that the index is the attained age. The
  shock-lapse buckets are three vectors and a count, which `shock_lapse_rate` loops over.
  The padding holds NaN, and nothing reads it: the one cell that reads each table checks
  its key against the table's extent first.
- **Codes.** A timing or a phase, which `Term_US_S` spells as text, is an int Reference
  named as the text: `BEF_NB = 0` and `BEF_DECR = 1`, and `PRE_ISSUE = 0`, `LEVEL = 1`,
  `PLT = 2` and `EXPIRED = 3`. A call reads as before, less the quotes:
  `pols_if_at(t, BEF_DECR)`. A string argument or a string value would give the cell a
  dictionary for a cache, where a code indexes a C array, so codes are numbered from 0
  without a gap, the timings in the order of their instants within the month.
- **Reporting cells stay Python.** `model_point()`, the label accessors `sex()`,
  `rate_class()`, `plan()` and `premium_mode()`, and the three reports return a table row,
  text and DataFrames, for a reader, for `run_sec.py` and for the comparison with
  `Term_US_S`. No other cell calls them, so they cost the projection nothing. A label
  accessor returns its column as read, and `Data` accepts a label that is blank, which
  pandas reads as NaN, or a number, which the point's first projection refuses. So each of
  the four compiles to a Python object, as the sample traces it (below), and returns what
  modelx returns (precised at M26).

The `Data` docstring lists its 23 vectors, arrays, extents and counts, each with the column
or file it comes from. The six readers stay Python, returning DataFrames and a path, and no
`Projection` cell but `model_point()` reads them. Every other cell of `Projection`, 56 of
its 64, returns a C `bint`, `long long` or `double`, and caches a single value, or a C
array the spec sizes from the contract:

| Compiled to | Cells |
|---|---|
| a C array of 1,046 by `t`, of `double`, `long long` or `bint` | the 33 cells of `t` alone: every count, rate, factor, premium and cash flow; the policy clock, its years and the attained age; `phase`; and the flags `is_active`, `prem_due` and `conv_elig` |
| a C array of 1,046 by 2 | `pols_if_at(t, timing)` |
| a C array of 79 by policy year | `premium_pp_ann_py(y)` and `conv_elig_py(y)` |
| a C array of 69 by PLT duration | `plt_mort_factor(d)` |
| one `long long` or `double` | the 19 other cells without a parameter: the point's numbers, the ends of its frame, its factors, the jump ratio and the shock lapse rate |
| a Python object | the eight reporting cells |

The declarations the build generates, `_mx_classes.pxd` in the compiled package, are the
record of it, and none of `Projection`'s caches there is a dictionary.

### The sample and the spec

mx2cy types each cell from the values the sample run passes it and gets back, and a cell
the run never calls compiles as a Python object. So `sample_sec.py` runs the three reports
on every committed point, and then the eight cells no report reaches: `model_point()` and
the four label accessors, which only a reader asks for; `band()`, which no cell reads,
since `Data` bands the face itself; `point_id()`, which only a refusal names; and
`phase(t)`, before issue, in cover and from the month cover ends, with the count
`pols_if_at` carries into that month. It runs the committed points alone: the export it
runs reads the CSVs of the directory the build is made in, which in place is the product
directory, so points of its own would have to be written there. The committed points
leave branches untaken: the semi-annual, quarterly and monthly modes, a twenty-year level
period, the conversion window's age limit, cover that ends with the level period, the cap
on mortality. That still types every cell, because every branch of a cell returns the one
type its others return, a count a float in every branch, and on points that take those
branches the compiled model computes modelx's numbers (above). The label accessors are
typed from more than the committed points: the sample also calls the four on a copy of the
first point with every label blank, written to a temporary directory and read by a second
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
| `t` | 1,046 | 1,044. The longest frame is a policy issued at the youngest issue age, 18, covered to 95 for 77 policy years, and issued 120 months after the valuation date, the furthest ahead `Data.future_horizon_mth` admits as shipped: 12 × 77 + 120 = 1,044 months, `t = 0 … 1,043`, and the month after, 1,044 |
| `t`, `timing` | 1,046 by 2 | `t` as above, by the two timings, so a code that is neither raises |
| `y` | 79 | 77, the last policy year; no cell reads one outside cover. The year after month `t`'s is asked only inside the conversion window, at most year 31 |
| `d` | 69 | 68: PLT year 68, which `mort_rate` reads in the month after the longest ten-year frame, as it reads the PLT year in every month. No headroom |

`proj_len()` refuses a point issued below 18, `issue_age_min`, and one whose level period
is below ten years, `policy_term_min`, in modelx as compiled, and cover ends at
`expiry_age`, 95, so no report on a point the model projects runs past these caches.
Those three References and `Data.future_horizon_mth` are the contract the sizes are
derived from. Lower either minimum, or raise `expiry_age` or the horizon past 120 months,
and a report runs past the caches in the compiled model alone: a frame longer than 1,044
months, a policy year past 78 or a PLT year past 68 raises `IndexError`, naming nothing,
where modelx projects. Each needs the sizes derived again, as `spec_sec.py` derives them,
and a rebuild; a longer horizon, `t` raised to 12 × 77 + the horizon + 2.

### Two compiler directives

`tools/build_sec_cy.py` puts a line at the top of the module mx2cy translates, before it
compiles it: `# cython: infer_types=True, cpow=True`. Without `infer_types`, an integer
local such as `n = policy_term()` in `lapse_rate` stays a Python object, though the cell is
typed `double`, and so does the loop counter in `shock_lapse_rate`. Without `cpow`,
`x ** y` on two doubles is a complex power, which a compiler with C99's complex numbers,
gcc among them, computes with `cpow` rather than `pow`. So `1 - (1 - q) ** (1 / 12)`, the
monthly rate of every decrement here, can differ from Python's in its last bits: on the
splice grid's 55 points, 240 compiled values differed from modelx's without it, by up to
2.4e-15 relative, the first point 9's `mort_rate_mth(708)`, at q near 0.44. With both
directives, every value agrees bit for bit, and the compile tests hold each directive, by
the module's first line and, on x86-64, by C4 itself. What they cost is C's semantics,
which no formula here meets: a local assigned only from int literals is a C `long`, 32
bits on Windows, and an int raised to a negative int truncates. The tool's docstring has
the detail.

On Linux and macOS the tool also compiles with `-ffp-contract=off`, after any flags the
interpreter or `CFLAGS` give. gcc fuses `a * b + c` into one fused multiply-add wherever
the target has the instruction, and clang within an expression: one rounding where Python
rounds twice. The default x86-64 target has none, but `-march=native` gives one on a
processor with FMA: built so here without the flag, the compiled model fused three
operations, and `plt_mort_factor(10)` came out 2.15 where modelx computes
2.1500000000000004. With it, the same build is modelx's bit for bit. MSVC, on Windows,
emits no fused multiply-add for x64 without `/arch:AVX2`, which setuptools does not pass.

### What a compiled run needs

**Memory, and the release.** A compiled `Projection` ItemSpace is a C struct of 429,896
bytes, the type's basic size, which holds every cell's cache, and deleting it,
`del model.Projection[idx]`, frees nothing by itself: an ItemSpace sits in reference
cycles, the list of roots it keeps among them, and only Python's cyclic collector frees
it. That is why `run_sec.py --block` collects after each release, in its frame pass and
in its projections (*Run it*, above). On 600 compiled points, the committed table a
hundred times over, the runner as it is took 1.35 to 1.40 s, and after every release no
ItemSpace but the base was alive, counted among the objects the collector tracks, and
not frozen (`gc.get_objects()`); the process peaked at 71 MB. With the collection taken
out of the release, the frame pass left all 600 of its ItemSpaces alive, which the
runner's second freeze then kept for good, and the projections up to 71 at a time; the
process peaked at 349 MB. And with the first freeze moved after the frame pass, each of
the frame pass's collections scanned everything alive, pandas, numpy and the model, and
the run took 10.4 to 11.7 s, the same 71 MB. Two runs each, under load.

**Stack, not recursion limit.** A compiled chain of cells calls C to C, on the C stack,
which the interpreter's recursion limit does not count, so the compiled model needs no
limit raised: the deepest call the contract allows runs under a limit of 60. What it needs
is stack. That call, a cold `net_cf` in the last month of the longest frame, runs the count
chain back to `t_entry()`, 932 cells deep in modelx, one cell a month and 9 more, which a
test holds, and compiled with gcc it needs between 232 and 236 KiB. A test runs it in a
thread of 1 MiB, the stack Windows gives a program's main thread unless the program is
linked for more, and again on the main thread, which is where `run_sec.py --cython` runs.
MSVC's frames may be larger than gcc's, and the `cython` CI job, which runs the test on
Windows too, is the check on them. The export recurses in
Python instead: the same call needs a recursion limit of 1,881 there, and the three
reports, which run in ascending `t`, need 48, so `sample_sec.py` sets 10,000.

### What it refuses

The compiled model refuses what modelx refuses, with the same message. modelx raises its
`FormulaError`, which quotes the error; compiled, the `ValueError` itself propagates.

- What `Data` cannot decode or hold, when the vector is first read, naming every point at
  fault, or the schedule or the table: a `point_id` that is not a whole number, a plan
  whose years `int` cannot read, a premium mode other than `A`, `SA`, `Q` or `M`, a class
  `class_factor_table.csv` lacks; a premium schedule whose policy years are not whole,
  leave a gap, repeat or start below 1; a mortality table with an age that is not whole, a
  gap, a repeated or negative age; a shock-lapse table with no bucket. `Term_US_S` met
  each only when a projection reached it. A key written as a float, a policy year `1.0`,
  is read by its value, as `Term_US_S`'s `.loc` matches it, and so are the keys each
  table's extents are taken from: a key written as text is refused by the extents as by
  the array, so a projection, which reads an extent first, meets the table's own refusal.
- A value a cap, a `min` or a `max` reads that is not a finite number, blank, text or
  infinite, when its array is first read, naming the file, the column and every line or
  point at fault, over the whole table, so that a value no point reads is refused as one
  that it reads is: a factor of `class_factor_table.csv`, by class,
  `class_factor_table.csv: factor must be a finite number; it is not at rate_class
  ['PNT']`; a rate of `mort_table.csv`, by age; a premium of `premium_rates.csv`, which
  the jump ratio and so the M(1) rule read, by every schedule at fault and every policy
  year in it; an `age_at_entry`, whose attained age indexes the mortality table, and a
  `plt_mort_factor_override`, by `point_id`. A blank override is the notes' rule, and is
  read so. `Term_US_S` met each only when a projection reached it: it raised on text and on
  a blank or infinite age, read an infinite factor, base rate or M(1) override as certain
  death at its cap and a negative infinite M(1) override as its grading's floor, 2.0,
  without a word, and projected NaN or an infinity from the rest.
- A key beyond a table, by the one cell that reads it, where `Term_US_S`'s `.loc` raised
  `KeyError`: `point_id 2: mort_table.csv has no rate at attained age 30`, from
  `mort_rate_base`, and `point_id 2: premium_rates.csv has no premium for policy year 61`,
  from `premium_pp_ann_py`.
- By `proj_len()`, a point past its cover, `point_id 5: duration_mth 720 is at or past the
  end of cover, policy month 720`, and a point the contract does not issue:
  `point_id 2: the plan's level period, 5 years, is below policy_term_min, 10`, and
  `point_id 6: issue age 17 is below issue_age_min, 18`.

An argument outside a cache raises `IndexError` in the compiled model alone, as above:
`net_cf(1046)`, which modelx answers with 0, the month being outside cover. An `idx` past
the last row is refused in both, with an `IndexError` at the first read of a vector, and
`Projection[-1]` reads every vector at its last element in both, so it is the table's
last point, under that point's own `point_id()`.

An annual mortality above 1 is not refused but capped, in both: `mort_rate` caps the
product of the base rate, the class factor and M(d) at 1, as `Term_US_S` does
(*Departures from Term_US_S*, above). Uncapped, the monthly rate, `1 − (1 − q)^(1/12)`,
would be complex in modelx and NaN compiled, silently. Capped, both compute 1, and a
compile test holds the two equal on points where the cap binds, new business and in
force. A NaN product would stay NaN through the cap, in both, as it would through the
M(1) rule's `min` and the grading's `max`, each of which the compiled model computes as a
comparison that keeps the value unless the bound is smaller, or larger; `Data`'s refusals
of a value that is not a finite number keep any NaN from reaching them.

### Speed

`python tools/bench_sec_cy.py term_life` builds the model into a temporary directory and
times one block run on three engines: modelx, the export and the compiled model. Each
engine runs the committed table repeated, in a process of its own, as `run_sec.py --block`
runs a block, each point projected and then released. `net_cf` is `net_cf(t)` summed over
the frame, the projection alone, as `basiclife/BasicTerm_SC` is timed on its
`pv_net_cf()`; `result_cf` is the report `run_sec.py` prints, which builds a DataFrame for
each point. Each time is the fastest of three runs, with their spread in seconds:

| Engine | Points | `net_cf`, a point | `result_cf`, a point | Peak memory |
|---|---|---|---|---|
| compiled | 6,000 | 0.50 ms (2.98–3.20) | 1.26 ms (7.57–8.02) | 84 MB |
| export | 600 | 4.7 ms (2.84–3.32) | 5.9 ms (3.53–4.04) | 84 MB |
| modelx | 120 | 196 ms (23.5–26.0) | 223 ms (26.8–27.7) | 116 MB |

On `net_cf` the compiled model runs 9.5 times its export, and on `result_cf`, where
building the DataFrame takes most of its time, 4.7 times; it runs 394 and 177 times
modelx. A run earlier the same day, under a lighter load, between 0.9 and 1.4, gave the
compiled model 0.47 and 1.27 ms and the export 5.0 and 6.2 ms, 10.7 and 4.9 times.
`BasicTerm_SC`, timed on 2026-11-01 on its own measure, `pv_net_cf()` over 1,000 of its
points, ran 8.7 times its export. The release keeps a block flat: the compiled model's
peak grew by less than 0.1 MB over its 6,000 points. Reading the five files and building
every `Data` vector and array for those points took 0.03 s, and asking every point for
its frame, the runner's first pass, 0.08 s.

Measured on 2026-11-02 on a machine shared with other work, under load: 4 CPUs (an Intel
Xeon at 2.10 GHz), a 1-minute load average between 1.6 and 3.0 as the runs started; Linux,
Python 3.13.18 and gcc 13.3.0, with modelx 0.33.0, modelx-cython 0.1.0, Cython 3.3.0,
numpy 2.5.3 and pandas 3.0.5. Under load the spread is wide, and the fastest run is the
one to compare.

## Tests

- **The twin identity**, in `tests/test_model_conventions.py`: on points 1 and 2, every
  cell of `Term_US_S`'s agrees at every argument `Term_US_S` evaluates in its own sweep,
  but for `pols_if_init` and `model_point`, and a cell this model lacked would fail it.
  So `Term_US_S`'s worked example, which `tests/test_term_life_us.py` asserts, money to the
  cent and the in-force to six decimals, holds here with no number restated. It holds
  because each S point counts one policy: on any other count, acquisition per policy
  issued would part from `Term_US_S`'s once per point, and the module asserts the count.
  The same suite holds the model to the conventions every `_SEC` model meets: every frame
  starts at `t = 0`, `pols_if` is the `BEF_DECR` count, new business enters once at its
  `policy_count`, nothing happens before issue, and the in-force columns are present.
- **The splice**, in `tests/test_term_life_us_sec.py`: each `Term_US_S` point restated in
  force at months 1, 12, 119 (the shock), 120 (the first ART premium), 121 and 719 (the
  last) continues the S projection, in every cell the two share but `proj_len` and
  `result_cf_annual`, to 1e-9, `Term_US_S`'s text for a phase compared as the code of the
  same name. So do variants of S's points, in a copy of S's table that is never
  committed, each reaching what S's own points cannot:
  - the anchor cell issued at 65 and paying quarterly, restated at months 1, 47, 59 and
    60: its conversion window, policy years 1 to 5, is closed by attained age 70 rather
    than by the level period, and its premium falls due every third month;
  - point 2 issued at 45 on a twenty-year plan and paying semi-annually, restated at
    months 238 to 241, either side of the shock and the first ART premium: the level
    period's length, read by the shock month, the jump ratio and M(1). A copy of
    `premium_rates.csv` carries its T20 scale, T10's moved on ten years;
  - the anchor cell issued at 85 and paying monthly, restated at months 1, 118 and 119:
    cover ends with the level period, so the shock falls in the last covered month;
  - ten more, restated in their second month, each carrying a value the model decodes or
    joins its tables on that no shipped point carries: the female sex, each of the other
    three classes, and each side of every face-amount boundary, $249,999.99 and $250,000
    and so on to $1,000,000. Each key has a premium schedule of its own in the copies, the
    anchor cell's at a scale of its own, so that a point joined to the wrong schedule, or
    banded wrongly, reads another premium.

  The comparison runs over S's own frame. `Term_US_S`'s jump ratio reads policy year 11
  past the age-85 point's frame, where this model's cells answer that the month is outside
  cover, and such a read has no counterpart to compare. Inflation, the one input on the
  valuation clock, is set to 0 in both models, and conversion is switched on in both, at
  the notes' **[std]** 1% a year and 2% in the final eligible year, because at the shipped
  zeros the conversion window is invisible to any comparison.
- **Future new business**: issued 1 and 12 months after the valuation date, each S point
  is the S projection moved on, with zeros before issue and no decrement rate evaluated
  there, and so is each of the first three variants issued a month on.
- **How it computes**: on every row of the splice's grid, after every report, no cell has
  been called at a negative month, and none evaluated at month `t` has read a month later
  than `t + 1`. On a fresh read of the committed model, `duration_mth(500)` evaluates
  `duration_mth` once, because the policy clock is a closed form, and every point's three
  reports run under modelx's recursion limit lowered to 40, which a recursion backward
  over the frame, through `t + 1`, would exceed. And on a fresh read a cold `net_cf` in
  the last month runs one cell a month back to issue, and at most 16 more, by modelx's
  stack trace, on the committed twin and at the contract's two longest frames, 728 and
  932 cells, where a count chain of two cells a month, which gives the same numbers,
  would run twice as deep. No number shows any of the five, and the compiled model needs
  each (*The compiled model*, above).
- **Counts, validation and regeneration**: the roll-forward closes, and `pols_if_at`
  refuses a timing it does not have; doubling `policy_count` doubles every cash flow and
  moves no per-policy value; each malformed row is refused naming its point, a duration of
  −121 among them; the horizon is a Reference, which at 2 refuses the point issued 3 months
  on and at 0 refuses any future business, saying so; a point past its cover, and one the
  contract does not issue, on a level period below ten years or issued below 18, is
  refused by `proj_len()`, a five-year plan with a schedule of its own projecting only
  once `policy_term_min` is lowered, and `run_sec.py --block` refuses such a point before
  printing anything; a zero count, durations written as floats and a policy issued 120
  months on are accepted; and the committed table is what `Term_US_S` generates.
- **The clocks and the rest**: point 4 pays policy year 12's premium at `t = 6`; expense
  inflation runs on the valuation clock at the shipped 2%, which only this test sees,
  since the splice sets the rate to 0; acquisition falls on new business alone; every
  guarded cell holds its value outside cover and reads no rate there; the points of a
  block sum row by row; an extract without the generator's three columns projects the
  same numbers, and, labelled 106 down to 101 rather than by position, names each point
  by its label, in `point_id()`, in a refusal and in `run_sec.py`'s output;
  `run_sec.py` prints the model's numbers, for point 4 and for the block; and outside the
  repository, beside a copy of the model or at a path too shallow to hold one,
  `run_sec.py --cython` says it cannot build.
- **The cap**: on the anchor cell issued at 70 in the tobacco class, with M(1) at 8.0 and
  a tobacco schedule, in copies of the tables, under the splice's References, inflation
  at 0 and conversion on, the product of the base rate, the class factor and M(d) passes 1
  from policy year 21, at attained age 90, to the end of cover. In both models
  `mort_rate` and `mort_rate_mth` are the float 1.0 there; every policy in force at the
  start of that year's first month dies in it, and none is in force after it; the
  reports hold finite floats; and every cell the two models share agrees, to 1e-9
  relative with no absolute floor, at every argument `Term_US_S` evaluates, the capped
  months and the reports included. So does the point restated in force the month before
  the cap, opened with `Term_US_S`'s count and compared cell by cell as a splice row is.
  It loses every policy in the capped month, and the point in force five months into that
  year loses every policy in the first month it projects. And a NaN sent to the cap, to
  the M(1) rule's `min` or to the grading's `max`, through the formula of the cell that
  feeds it replaced by one returning NaN in a model read for the test, stays NaN at the
  bound and at each call after it that the test lists, the mortality and a count among
  them: `mort_rate` is NaN, not 1.0, where the class factor is NaN. (`shock_lapse_rate`
  reads the jump ratio through a comparison, which takes the last bucket for a NaN;
  `Data`'s refusals keep a NaN from it.)
- **The fingerprint** (C2): before the compile step changed anything, what the model
  computed on each committed point was frozen in the module, each column of `result_cf()`
  and `result_pols()`, its sum, its largest value and its values at five months, and the
  model reproduces it to 1e-12. `python tools/gen_sec_fingerprint.py Term_US_SEC --check`
  makes the same comparison. The tests above held through the compile step with their
  call syntax changed: a point's position for its label, and the codes for the text of a
  timing or a phase.
- **Decoding**: every value a decoded column can hold, each sex, class, plan and mode and
  each side of every face boundary, decodes as `Term_US_S`'s own cells read it; a table
  whose keys are written as floats, policy years `1.0` and ages `35.0`, projects exactly
  the committed numbers, as it does in `Term_US_S`; what cannot be decoded, a table with a
  gap, a blank policy year, a policy year or an age that is not whole, or a key written as
  text, and a key beyond a table, are each refused naming the point, the schedule or the
  table, a projection meeting the same refusal; and the padding beyond each table's
  extent is NaN.
- **Values a bound reads**: a class factor, a base rate, a premium and an issue age
  written blank, as text or as an infinity, and an M(1) override written as text or as
  either infinity, are each refused naming the file, the column and every line or point
  at fault, by the `Data` cell that first reads them and by a projection: one at a time,
  a factor of a class and a premium of a schedule no point carries among them, and two in
  one column, at two classes, two ages, two policy years, two schedules or two points; no
  other rule refuses the copy, every other `Data` cell reading or meeting the same
  refusal.
- **No pandas in `Projection`** (C5), in `tests/test_compiled_conventions.py`, which holds
  what every `_SEC` model meets once it compiles. Read from the formulas, with no compiler:
  no cell but the reporting ones refers to pandas, numpy or another module, reads a table
  with `.loc` or the like, calls a reporting cell, holds text but in its docstring and its
  refusals, or holds a generator, a comprehension or a nested function; none calls
  anything but a cell, a `Data` vector and the builtins Cython turns into C, `int`,
  `float`, `bool`, `abs`, `min`, `max` and `range`, or builds a list, a dict, a set or a
  tuple; every `Data` vector a formula reads is an int64 or float64 array, read by
  element; no cell is uncached, which modelx-cython would leave untyped; no cell shares
  its name with what a call with keywords calls anywhere in the model; and each label
  accessor returns its point's column of the same name.
- **Compiled**, where modelx-cython and a C compiler are installed, after compiling the
  model once into a temporary directory, never into the tree. In the same conventions
  module: the generated declarations give every cell but the reporting ones a C `bint`,
  `long long` or `double` and a C-array cache of exactly the spec's size, and every new
  `Data` cell but a reader a typed memoryview or a C scalar, and the generated C keeps no
  Python object among a projection cell's locals, calls no Python builtin there and
  builds no container, under both directives (C3); on the committed points, every cell
  at every argument a full modelx sweep caches is what modelx computes, bit for bit on
  x86-64, and so is every raise and every `Data` array (C4); and `run_sec.py --block`,
  run compiled, holds one point's ItemSpace at a time. In
  `tests/test_term_life_us_sec.py`: the same comparison on the splice grid, variants
  included, on the contract's two longest frames and on the points where the cap binds;
  the compiled model refuses what modelx refuses, with modelx's message, on the extract
  labelled otherwise than by position too, and every value a bound reads that is not a
  finite number; the deepest call the contract allows runs cold on a 1 MiB stack and on
  the main thread; a Reference set after the model has computed changes no value it has
  cached; and `run_sec.py --cython` prints what `run_sec.py` prints, and refuses a
  directory that holds no build. They are marked `cython`, and they skip without the
  toolchain, but in the `cython` CI job, which installs it on Linux and on Windows, a skip
  fails, whatever made it.

```bash
python -m pytest tests/test_term_life_us_sec.py -q
python -m pytest tests/test_model_conventions.py -q -k Term_US_SEC
python -m pytest tests/test_compiled_conventions.py -q -k Term_US_SEC
python -m pytest tests/test_term_life_us_sec.py -q -m cython      # the compiled tests alone
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
