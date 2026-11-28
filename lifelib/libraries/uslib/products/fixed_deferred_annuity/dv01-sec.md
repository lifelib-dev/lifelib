# Key-Rate DV01 and CS01 on MYGA_US_SEC

**Status:** Draft, 2026-11-25. `dv01_sec/` values a book of [`MYGA_US_SEC`](model-sec.md)
contracts on stochastic interest-rate paths, at a series of annual closes, on the base curve
and on twelve key-rate curves, and reports the interest-rate sensitivity of the book's
liability by tenor. The contracts, their formulas and their assumption tables are
MYGA_US_SEC's, unchanged; the market is the G2++ generator of
`economic/CashValue_ME_G2PP`. The same model runs in
live modelx and, compiled with modelx-cython, on several threads at once.

> **This is a mechanics demonstration, not a risk measurement.** Every behavioural and
> expense assumption is MYGA_US_SEC's **[std]** standardization (see
> [`product-spec.md`](product-spec.md)), and the G2++ parameters and the input curve are the
> economic library's examples. Replace them with company data before drawing any conclusion
> from the numbers.

## Run it

```bash
python products/fixed_deferred_annuity/run_dv01_sec.py                    # live modelx
python products/fixed_deferred_annuity/run_dv01_sec.py --compiled         # compiled, 1 and 4 workers
python products/fixed_deferred_annuity/run_dv01_sec.py --compiled --build DIR --workers 8
python products/fixed_deferred_annuity/run_dv01_sec.py --compiled --policies 1050
python products/fixed_deferred_annuity/run_dv01_sec.py --compiled --collect     # through collect
```

The first builds the model and prints the two reports of the shipped book, MYGA_US_SEC's
fourteen model points (`model_point_table_sec.csv`), on ESG path 1 for years 0, 1 and 2, with
their totals and the seconds taken: about five minutes and 1.2 GB. `--compiled` builds the
model with modelx-cython into `DIR`, or into a temporary directory, which takes about ten
minutes; a build already in `DIR` is reused when it was made from the same model, compiler,
modelx and interpreter (a stamp in `DIR` records them), and rebuilt otherwise. It then runs the report twice, each time in a
fresh process: on one worker thread, and on `--workers` threads. It prints each run's totals
and seconds and checks that the two reports are equal. `--policies N` replaces the shipped
book by N policies, MYGA_US_SEC's seven new-business points repeated; the timings below are
on that book. `--collect` computes the compiled report through `Valuation.collect` instead of
the pooled driver. `--paths` and `--years` widen the report, and `--json FILE` writes it out.

In Python:

```python
from lifelib.libraries.uslib.products.fixed_deferred_annuity.dv01_sec import build_model, report

model = build_model()
dv01, cs01 = report.live_report(model, num_scenarios=1, annual_steps=2)
model.close()
```

## What the report computes

For each ESG path `s` and year `y`, the close is month `c = 12y - 1`, the last month
completed before year `y` starts (`c = -1` at the valuation date, before any month has
closed). At that close every policy is valued in force:

* its state entering month `c + 1` (account value, Model #805 floor, accumulated premiums
  at the GMIR, interest credited, free-withdrawal allowance, tax basis, declared rate and
  locked MVA yield, and the count in force) is the state its **actual** projection on path
  `s` reached, month by month, on the rates that path's market quoted;
* from then on it is projected again on the **curve** observed on path `s` after close
  `c`: the base curve, or the curve with one key rate bumped. Renewal rates, competitor
  rates for the dynamic lapse, and MVA yields come from that curve's forwards, so a bump
  changes the cash flows as well as their discounting.

The liability is minus the present value of the policy's net cash flows (premiums less
benefits and expenses) after the close, each month's flow discounted to the close on the
same curve. The book's liability is the sum over its policies. For key `k`:

* **DV01** = base liability − liability valued on curve `k`, both projections run on their
  own curve. It is positive when the bump lowers the liability.
* **CS01** = base liability − the base projection's cash flows discounted on curve `k`.
  The cash flows are held at their base values, so CS01 is the discounting effect alone,
  and DV01 − CS01 is the effect of the bump on the cash flows.

Curve `k` adds 1 bp to the annual-effective zero rate at the `k`-th tenor of
`dv01_sec/shock_steps.csv` (12 to 120 months annually, then 180
and 240), falling linearly to zero at the neighbouring tenors and held flat beyond the first
and the last. The CSV may be edited: positive whole months, strictly increasing. Each report
has one row per path and year and one column per tenor.

On the shipped book the totals over the 36 cells are DV01 1,213.007886 and
CS01 1,532.723324.

## The model

`build_model()` assembles six Spaces:

| Space | What it holds |
| --- | --- |
| `Data` | MYGA_US_SEC's Data Space, copied, with `shock_key_months` and `book_projection_end` added. |
| `ESG` | The G2++ generator, copied, with `P_t_T_path(i, j, scen_id)`, one path's zero-coupon price, added. |
| `Market[as_of_month, scen_id, shock]` | One curve: observed after a close, on one path, with one key-rate bump (`-1` for none). Rates before the close are the fixings observed then. |
| `Actual[idx, scen_id]` | One policy on one path from the valuation date, its quotes from the market of each month (`actual.py`). |
| `Valuation[valuation_month, idx, scen_id, shock]` | The same policy restarted after the close, its opening state from `act`, its quotes from one `Market` (`valuation.py`). |
| `Outer` | The book's sums and the annual risk report (`outer.py`). |

Both projections carry every MYGA_US_SEC Projection formula but the three of its
deterministic rate scenario, which the market replaces (`contract.py`). `Valuation`'s
formula gives each item the Reference `act`, the `Actual` item of its policy and path, or on
the collect route (`collect_history`) the policy's record of `Actual.collect`: its eleven openings
at the months after the closes (`opening_months`); this is a dynamic Space Reference, and compiling it needs a modelx that exports such References.
`Market`, `Outer` and the ESG cell come from lifelib's MYGA DV01 example on `MYGA_US_S`.

## The compiled model

`dv01_sec/compiled.py` exports the model with `ESG`, `Market`, `Data` and `Actual` locked, writes a spec of
cache sizes (MYGA_US_SEC's own, from `spec_sec.py`, for both projections),
and compiles it with `dv01_sec/sample.py` as the trace, which runs the report of the shipped
book. Nothing is written into the library tree. The compiled report is computed by
`report.pooled_report`: one task per policy values the policy at every close on every curve,
releasing each item once read, and the results are summed in policy order as `Outer` sums
them, so the totals do not depend on the number of workers.

**Through collect.** `Valuation.collect(month, scen_id, key)` evaluates every policy at one
close and curve. Its `.sum` result holds the liability PV total and, on the base curve, the
cash-flow totals. The compiled collector accumulates supported numeric fields in C and
discards each private policy instance after copying its outputs. Worker subtotal order can
change floating-point rounding. The reports agree within the financial tolerance.

The report first calls `Actual.collect(scen_id)` once per path. Each Valuation reads its
policy's saved openings through `.individual[policy_id]`. It uses `Actual[policy_id, scen_id]`
through the same `act` Reference on the Direct route. The report makes 39 Valuation Collect
calls for the book below. The compiled export retains the locks on shared dependencies.

**The driver.** With more than one worker the main thread submits every task and then waits
once for all of them with `concurrent.futures.wait`, instead of waiting on each result in
turn as `list(pool.map(...))` does. On free-threaded CPython 3.14 a thread waiting on a lock
spins while attached to the interpreter, which holds back the reuse of the memory the workers
free, so with `pool.map` the four workers ran on fresh pages and scaled 1.3x where a single
wait scales 2.5x or more.

Requirements: free-threaded CPython 3.14 (`python3.14t`) for the parallel run, Cython 3.3,
a C compiler, modelx with the export of dynamic Space References and with `Space.set_collect`,
and modelx-cython with the compiled collect. Under a
GIL build the workers take turns and the reports are the same.

## Compiled report timing

The book repeats seven new-business policy points and uses ESG path 1 and years 0 to 2.
This gives 39 Valuations per policy and 40,950 Valuations in total. Times are medians and
ranges from five alternating fresh-process rounds on an eight-core Ryzen 7 5800H in WSL2
with free-threaded CPython 3.14.8 and the GIL off. The timer covers the full report after
loading the model and input tables. The Direct driver saves each base PV, base cash-flow
series and shocked PV before deleting the corresponding `Valuation` ItemSpace. It deletes
`Actual` after the last close for each policy and scenario. Deletion is part of the timing.

| Route | Policies | Workers | Wall s, median [min–max] | Median ms/policy |
| --- | ---: | ---: | ---: | ---: |
| Direct | 1,050 | 1 | 11.103 [10.798–11.961] | 10.574 |
| Collect | 1,050 | 1 | 9.849 [9.822–9.929] | 9.380 |
| Collect | 1,050 | 4 | 3.120 [3.096–3.157] | 2.971 |

Collect scales 3.16× from one to four workers. Each run checked all 36 DV01 and 36 CS01
entries against live modelx. At four workers the largest relative DV01 difference was
8.20e-8 and the largest absolute difference was 1.30e-6.

## Memory lifetime

The Collect report retains each path's opening records and the requested valuation sums.
Each policy's calculation state is released after its outputs have been collected. The
Direct report achieves its own bounded policy lifetime with the explicit deletions
described above. Interactive Direct access can keep a policy's ItemSpace available when
its individual Cell values are needed for inspection.

## Tests

`tests/test_fixed_deferred_annuity_us_sec_dv01.py` holds the model's shape, the live report
of the shipped book against stored values (rel 1e-10, abs 1e-7), and, where modelx-cython and
a C compiler are installed, the compiled report at 1 and 4 workers against the live one.
The Collect and pooled reports are checked against each other using the same financial tolerances.
