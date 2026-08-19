# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/unit_linked_bond/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the 100.1% death uplift, the surrender value as
> the bid value of units with no penalty, the 7.5% rolling withdrawal cap, charges
> accruing daily through the unit price, segmentation into 100 identical policies. Every
> **rate** is a **[std]** standardization: per-fund charge rate cards are not published
> (research gap), the CMI's assured-lives tables are restricted to Authorised Users
> [R8] [REG-R30], and no public UK bond persistency study was retrieved — so the charge
> levels, the mortality basis and the whole surrender table are placeholders.

## Run it

```bash
python products/unit_linked_bond/run.py         # the anchor cell
python products/unit_linked_bond/run.py 2       # the accumulation cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/unit_linked_bond/ULB_UK_S")
model.Projection[1].result_cf()
```

`result_uf()` gives the unit fund recursion column for column as the notes' worked
example prints it; `result_cf()` gives the cash flows.

## The unit / non-unit decomposition is the model

UK practice splits this product into two streams, and so does this implementation:

**The unit fund** — the bid value of units, matched by the linked assets. It grows with
the fund, bears the tax provision and the fund-based charges, and is drawn down by
withdrawals and adviser charges.

**The non-unit cash flow** — what actually accrues to the insurer: the annual management
charge and any rider charge, less expenses and the **death strain**.

Getting the split right is most of the work, and the notes list three separate ways to
get it wrong.

### 1. Every benefit is funded by cancelling units

Death, surrender and withdrawal all come out of the policyholder's own fund, so a naive
gross presentation counts the same money twice. `net_cf` here is therefore the
**non-unit** stream:

```
NUCF(t) = AMC + rider charge − expenses − death strain
```

The gross flows are still published — `claims_death`, `claims_surrender`, `withdrawals`
and `unit_releases` are `result_cf()` columns — and `check_unit_funding()` asserts they
net exactly:

```
claims(t) − unit_releases(t) − death_strain(t) = 0
```

### 2. The death strain is the uplift, not the death benefit

The sum assured is `u × UF`, of which `UF` is funded by cancelling units. The insurer's
cost per death is

```
DS(t) = (u − 1)·UF(t) + max(0, G(t) − u·UF(t))·1{gmdb}
```

— a tenth of a percent of the fund on the composite, plus any in-the-money guarantee. At
month 12 of the anchor cell the death benefit per death is £97,876.92 and the strain is
**£97.78**.

**The uplift is a parameter and never a literal.** 100.1% against 101% is a *tenfold*
difference in death strain, which the notes list as a pitfall; model point 5 is the
anchor cell at 101% and its strain is exactly ten times point 1's.

### 3. Two of the four amounts leaving the fund are not income

| Amount | Insurer income? | Why |
|---|---|---|
| AMC | **yes** | the charge for managing the contract |
| GMDB rider charge | **yes** | the price of the guarantee |
| Further costs | no | fund-borne expenses, paid on to the fund |
| Tax provision | no | collected in-price, paid on as corporation tax |
| Adviser charges | no | post-RDR pass-throughs facilitated by cancelling units |

Booking the pass-throughs as margin would overstate the year-one non-unit result **by
more than the AMC itself**: on the anchor cell the tax provision is £967.89 against an
AMC of £993.10 (about 97%) and the further costs another £99.31 (about 10%).
`further_costs` and `tax_provisions` are published as their own `result_cf()` columns
precisely so their *exclusion* from `net_cf` is visible rather than merely asserted.

## The charge ordering, and why all three points are exposed

Per policy, within month `t`:

```
UF_g(t) = UF(t−1) × (1 + g_m(1 − t_pf))        growth, net of the tax provision
UF'(t)  = UF_g(t) × (1 − c_m − f_m)            AMC and further costs
UF(t)   = UF'(t) − W(t) − AC(t) − GC(t)        unit cancellations at end of month
```

**The order matters and is a listed pitfall.** The AMC accrues daily through the unit
price, so it is levied on the **post-growth, pre-cancellation** fund. Charging it on
`UF(t−1)` instead, or after the withdrawal, moves the margin by about half a month's
growth or withdrawal — small in one month and systematic over decades.

`av_pp_at(t, timing)` exposes all three points — `"BEF_GROWTH"`, `"AFT_GROWTH"`,
`"AFT_CHARGE"`, `"AFT_WD"` — so the ordering is inspectable rather than buried in one
expression, and `check_av_roll_fwd()` asserts the identity every month.

## The fund runs out, and the projection ends there

A 5% withdrawal against a 5% gross return is **not sustainable** once the 20% tax
provision and the 1.1% of charges are taken. The anchor cell's fund drifts down from
£100,000 and is exhausted at **month 354** — policy year 30, when the policyholder is 94.
`wd_pp()` caps the withdrawal at what the fund can pay, so the fund is drawn to nothing
rather than through it, and `proj_len()` ends the projection there: a bond with no units
has no liability, no margin and nothing left to project.

That is a product fact worth seeing rather than an artefact to hide. Every margin the
insurer was counting on stops at month 354, and the accumulation cell (model point 2,
no withdrawals) runs the full 660 months to the limiting age instead.

## The 5% allowance is policyholder tax machinery, not a product feature

`allowance_cum_pp()` and `excess_gain_pp()` track the cumulative 5% tax-deferred
allowance and the excess-event gain it produces when exceeded [R1] [R2]. **Neither
generates an insurer cash flow.** Two things follow, and both are listed pitfalls:

- the allowance never caps what can be withdrawn — the **product** cap is the rolling
  7.5% of `wd_cap_pp()` [S2 §7.1], which is a different and larger number; and
- adviser charges consume the same allowance [S2 §12.1.1], which is why `wd_cum_pp()`
  adds them in.

It is carried because it drives *behaviour*: `allow_factor()` steps surrender up by half
from policy year 21, once twenty years of allowance have been drawn and further
withdrawals generate immediate excess gains.

## Behaviour is the whole valuation

Every margin line is proportional to the unit fund **and** to persistency, and a
surrender costs nothing at the point of exit — the surrender value is the bid value of
units, cancelled, with no penalty — while truncating the entire future AMC stream. Two
dynamic overlays sit on the base table, both **[std]** and both inert in the base run:

| Overlay | Formula | Off value |
|---|---|---|
| Performance | `M_perf = min(2, 1 + 2·max(0, g_ref − R_12m))` | `return_shock = 0`, so `R_12m = g_ref` and the multiplier is 1 |
| Allowance exhaustion | `M_allow = 1.5` from policy year 21 | not a switch — it fires on schedule |

`return_shock` is kept separate from `fund_return` deliberately: it moves the
*behavioural* driver without disturbing the fund path, which is what makes the
multiplier testable in isolation. There is no interest-sensitive dynamic lapse and no
paid-up state — the product is single premium, so there is no premium obligation to
stop.

## Inputs are external files

The three input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `ULB_UK_S/` holds nothing but formulas:

```
products/unit_linked_bond/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  surr_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  ULB_UK_S/                   <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file
is read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `surr_table_file` | `surr_table()` | `surr_table.csv` |

Note what is **not** an input file. The charge rates — AMC, further costs, tax provision,
death uplift — are **model point columns** rather than a rate table, because they are
per-policy contractual and discretionary parameters rather than experience assumptions,
and because per-fund rate cards are not published anyway. The fund return is a single
Reference, because the base run is deterministic.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Six model points. **Point 1 is the worked-example anchor cell** (M65, £100,000, 100 segments, AMC 1%, further costs 0.10%, tax 20%, uplift 1.001, 5% withdrawals); point 2 drops the withdrawals; point 3 adds a 0.5% ongoing adviser charge; point 4 elects the GMDB rider; point 5 is the anchor at a 101% uplift; point 6 is a younger female on a larger premium and a 3% custom withdrawal | anchor cell **[std]**, technical notes' worked example |
| `mort_table.csv` | Base annual mortality by sex and age 18–120, capped at 1 | **[std]** proxy shaped like the ONS national life tables, anchored so that the 80% best-estimate factor gives the notes' `q(65) = 1.0%` placeholder exactly — *not* an assured-lives table |
| `surr_table.csv` | Annual full-surrender rates by policy year, 2 / 3 / 5 / 8 / 10 % | **[std]**; low early, rising as the advised holding period completes. No public UK bond persistency study was fetched |

## The GMDB rider, and why it never bites in the base run

The return-of-premium rider guarantees `G(t) = premium − withdrawals − adviser charges`,
so the guarantee **erodes as the policyholder draws the fund down**. On the anchor
withdrawal pattern it reaches zero at month 240, well before the fund does — so on the
base assumptions the guarantee never bites and model point 4's cash flows differ from
point 1's only by the (zero) rider charge.

That is the honest outcome of the base assumptions rather than a defect, and the tests
demonstrate the machinery by driving `fund_return` negative, where the guarantee moves
firmly into the money and the death strain becomes market-contingent. The rider's real
charge scale is unpublished [S2 §5.2], so the cost-of-insurance form used here has the
right shape and no authority — enable it only with its own sensitivity set.

One implementation note. `gmdb_guarantee_pp(t)` is measured **before** the current
month's cancellations, at `wd_cum_pp(t − 1)`. That is the only reading that resolves: the
rider charge is itself a cancellation alongside the withdrawal, so a guarantee net of the
same month's withdrawal would make the charge depend on a withdrawal that depends on the
charge.

## Naming

Cells follow lifelib's `savings/CashValue_SE` and the account-value vocabulary the U.S.
models settled on. The full symbol mapping lives in the `Projection` Space docstring.
Four cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `UF` | `av_pp` / `av_pp_at` | The library calls a policyholder-owned fund `av_pp_at`, and one concept must not carry two names across the library. The docstrings and `result_uf()` keep the unit vocabulary the product is discussed in |
| `G$(t)` vs `G(t)` | `fund_growth_pp` / `gmdb_guarantee_pp` | The notes use `G` for both the gross fund return and the GMDB guaranteed amount |
| `NUCF(t)` | `net_cf` | Not a gross liability total — see the decomposition above. Still income-positive, as everywhere in the library |
| *(no analogue)* | `pols_maturity` | Borrowed from the term models; a bond has no maturity, so this is the population left when the projection ends, and it pays nothing |

## Standardizations used

Everything in this list is **[std]**: the AMC of 1.00%, further costs of 0.10% and the
20% tax provision; the 1/12 monthly accrual convention for both charge rates; the whole
mortality basis and the 80% best-estimate factor; the surrender table; the 5% withdrawal
pattern; the performance multiplier and its cap, and the allowance-exhaustion step; the
GMDB charge form; acquisition expense £300 and maintenance £60 a year inflating at 2.5%;
the deterministic 5% gross fund return; death-before-surrender as the processing order;
and the treatment of the tax provision as exactly offsetting tax payable, which ignores
the I-E timing and base differences that create real insurer-side tax strain or float.

Deliberately excluded, per the notes: top-ups (a top-up is a new model point with its own
premium and allowance clock), joint last-death bonds, segment-level granularity (bond
level is exact only while all 100 segments stay identical), settlement frictions, and
smoothed and with-profits funds — PruFund's EGR and smoothing limits and MVR-bearing
funds change the unit-price dynamics and add guarantee costs, and belong to
[`products/with_profits`](../with_profits/model.md), not to this recursion.

## Tests

`tests/test_unit_linked_bond_uk.py` asserts the notes' worked example to the penny — the
month-by-month unit fund recursion, the year-one totals and the reconciliation that
closes them — plus the per-policy insurer-side extraction beside it, the charge ordering,
that the pass-throughs stay out of `net_cf`, the death-strain arithmetic and the tenfold
uplift sensitivity, the withdrawal caps, the fund exhausting the projection, the
allowance tracker generating no cash flow, both behavioural overlays, and the GMDB rider
under a falling fund.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-unit_linked_bond-r1
[R2]: #uklib-unit_linked_bond-r2
[R8]: #uklib-unit_linked_bond-r8
[REG-R30]: #uklib-reg-r30
[std]: #uklib-std
<!-- END generated citation links -->
