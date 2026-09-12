# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/with_profits/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> mechanics are sourced — the asset share item list and its regulatory codification,
> bonus hardening, the unit-price floor, the guarantee-date and death MVR exemptions,
> the MVR's contractual bound, the 80–120% target range, the smoothing cap, the lifetime
> guarantee-charge cap and the 90:10 split. Every **rate** is a **[std]**
> standardization: bonus declarations are not published in firms' principles and
> practices documents, no MVR scale is public, the CMI's tables are restricted to
> Authorised Users, and no UK with-profits lapse experience was retrieved.

## Run it

```bash
python products/with_profits/run.py           # scenario A, the up market
python products/with_profits/run.py 2         # scenario B, the down market
python products/with_profits/run.py 5         # the conventional endowment
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/with_profits/WP_UK_S")
model.Projection[1].result_cf()
```

`result_payout()` gives the payout machinery — asset share against guaranteed benefit
against smoothed payout, and the final bonus or MVR the gap between them produces.
`result_cf()` gives the cash flows.

## Monthly steps, an annual declaration

The grid is **monthly** and the bonus declaration is not, and that pairing is the whole
of what this model had to get right.

The declaration is the governing act of discretion on a with-profits policy: firms
declare once a year, and a declaration hardens the guarantee permanently. It was the
notes' stated reason for an annual grid, and it is a fact about the product rather than
about the grid, so it survives: `is_declaration_month(t)` is true in the twelfth month
of each policy year and nowhere else, and that is where `unit_price`, `guar_benefit_pp`,
`cost_of_bonus_pp` and `shareholder_transfer_pp` move. `Q` and `FV` (or `G`) are step
functions — flat for eleven months, stepping in the twelfth — and the cost of bonus and
the transfer are nil in those eleven.

Everything continuous runs monthly around it: the fund return, the annual management and
guarantee charges, the mortality charge, both decrements, the smoothed payout, the final
bonus and the MVR. Annual rates convert with the effective forms — `fund_return_mth()`,
`amc_rate_mth()`, `guar_charge_rate_mth()`, `mort_rate_mth()`, `surr_rate_mth()` — so
twelve months compound back to the annual figure exactly and the assumption basis does
not move with the grid. A bare `*_rate` is the annual rate, as everywhere in the
library; only `*_rate_mth` is monthly.

`check_declaration_is_annual()` asserts the cycle directly, because this is the way the
conversion goes wrong quietly. Compounding the annual `b` twelve times a year gives a
model that still runs, whose roll-forwards all still close, and whose guarantee is an
order of magnitude too large a decade later. The check tests the quantity a declaration
actually moves — the unit *price* on the bond chassis, since a withdrawal cancels units
between declarations, and the guaranteed benefit on the endowment.

What the monthly grid buys, beyond matching the rest of the library, is the **guarantee
date**. It is a date: an exit in month `12k − 1` is MVR-free and an exit in the other
eleven months of that policy year is not, which `mvr_applied_pp()` can now say. The
anti-selective encashment that follows is then a dated exercise rather than a year-long
elevation of the surrender rate — see *Behaviour* below, where that change is the one
assumption whose shape moved rather than its frequency.

## The time index and the frame

`t` is the library's **0-based** policy month index. `t = 0` is the issue month, month
`t` runs from time `t` to time `t + 1`, the contractual policy year containing it is the
1-based label `policy_year(t) = t // 12 + 1`, `duration(t) = t // 12` is the completed
policy years and `duration_mth(t) = t` the elapsed months.
`age(t) = age_at_entry() + duration(t)`, advancing on the anniversary.

`t` counts from **issue**, not from the projection start, so an in-force cell opens its
frame at its elapsed months: `proj_start() = 12 × duration_inforce()`. The model point
keeps `duration_inforce` in **years**, the unit a contract speaks in, and the conversion
is `proj_start()`'s job. The worked example's bond is in force at duration 5, so it is
projected from `t = 60`, the first month of its sixth policy year — the year the notes
work through. Because the conversion is a whole number of years the frame always opens
on an anniversary, which keeps the declaration months aligned with the contract.

`proj_len()` is the **number of policy months from issue**, i.e. the exclusive end of
the frame: `result_cf()` and `result_payout()` are indexed by
`range(proj_start(), proj_len())`, the last row is `proj_len() - 1`, and the row count
is `proj_len() - proj_start()`. On the shipped points that is 720 rows for the bond
cells (`t = 60 … 779`, `proj_len() = 12 × (120 - 55)`), 343 for the withdrawing cell
whose fund exhausts (`t = 60 … 402`, `proj_len() = 403`), 300 for the new-business
endowment (`t = 0 … 299`, `proj_len() = 12 × 25`) and 60 for the same endowment in force
at duration 20 (`t = 240 … 299`).

**Carried-in state is an opening balance, not a row below the frame.** `asset_share`,
`unit_price`, `units`, `guar_benefit_pp` and `smoothed_payout` are all *closing*
balances — the value at the end of month `t` — so the state an in-force cell brings in
is the value the first projected month **opens** with, and it is read through
`asset_share_at(t, "BEF_PREM")`, `guar_benefit_open(t)`, `smoothed_payout_open(t)` and
`policy_value_open(t)`. Nothing is ever indexed at a negative `t`, which is what those
accessors are for: on a new-business cell `proj_start()` is 0, and "the month before
the first" does not exist.

Two contractual schedules are keyed by the **policy year**, not by `t`, and the model
maps rather than re-keys them: the lapse table's `policy_year` column
(`surr_rate_base()` reads row `policy_year(t)`, and returns the annual rate) and the
model point's `guarantee_dates` anniversaries (`is_guarantee_date(t)` is true when `t`
is a declaration month whose `policy_year(t)` is one of them, so the 10th anniversary
ends month `t = 119`).

## The asset share is a state variable, not a cash flow

That sentence is the model.

```
AS(t) = [AS(t−1) + P(t) − W_AS(t)]·(1 + r_m)·(1 − c_amc,m − c_g,m) − ST(t) − MC(t) + M(t)
```

Every item in that recursion is a recorded deduction from or addition to a
**retrospective accumulation**. None of them is a policy cash flow. The policy's actual
flows are premiums, claims, withdrawals, expenses and the shareholder transfer; the
asset share reaches them only through the bonus, smoothing and MVR rules, and the
difference between what is paid and what the asset share says is **absorbed by the
estate**. `asset_share` is published as a `result_cf()` column beside the flows precisely
so that it is visible *and* visibly not part of `net_cf`.

This is the one product in the library with **no account value in the library's sense**.
There is no `av_pp_at` here. The asset share is not a policyholder fund — nobody owns it
and nobody is paid it — and the guaranteed benefit is not a fund either. Both are
modelled, under their own names, and the gap between them is where the whole product
lives. Naming either of them `av_pp_at` would assert something false about the contract.

`asset_share_at(t, timing)` exposes the recursion one step at a time — `"BEF_PREM"`,
`"BEF_RETURN"`, `"AFT_RETURN"`, `"AFT_CHARGE"`, `"AFT_ST"`, `"AFT_MC"` — because the
order is
**contractual discipline** rather than arithmetic convenience: the shareholder transfer
is charged to asset shares *after* the charges and *before* the mortality charge, and the
mortality charge's sum at risk is measured on the balance after the transfer.
`check_asset_share_roll_fwd()` rebuilds the whole recursion in one expression and asserts
it closes, so a mis-ordered step shows up rather than quietly shifting the answer. It
rebuilds it with the *monthly* rates, which is the other thing it pins down: an annual
rate left in the recursion fails there rather than quietly overcharging the asset share
twelvefold.

## The bonus hardens, and that is what makes guarantees expensive

A declared regular bonus increases the guaranteed benefit **permanently**. The unit price
therefore never falls — `b ≥ 0` is a contractual floor, not a modelling choice — and
every declaration converts non-guaranteed final bonus into guaranteed benefit *without
changing the target payout*. That is the whole tension the discretion manages.

| | Bond chassis (UWP) | Endowment chassis (CWP) |
|---|---|---|
| Guaranteed benefit | `FV(t) = U(t)·Q(t)`, unit face value | `G(t) = SA + attaching bonuses` |
| Rolls forward by | `Q(t) = Q(t−1)(1 + b(t))` | `G(t) = G(t−1)(1 + b_rev(t))` |
| Cost of bonus | `b(t)·FV(t−1)` | `ΔG(t)·v_sv^(n−(t+1))` |
| Death benefit | `1.01 × (FV + FB)` | `G + TB` |
| Surrender | `FV + FB − MVR` | smoothed payout, capped at `G + TB` |
| Maturity | none — whole of life | `G(n−1) + TB(n−1)` |

Both are **one cells**, `guar_benefit_pp`. Every rule that consumes them — the bonus
cost, the mortality charge's sum at risk, the final bonus, the MVR — treats them
identically, so keeping two names would have duplicated five rules to no purpose.

The base projection holds the model point's snapshot rate level, as the notes specify.
`bonus_supportable()` and the smoothed setting rule are implemented and switched off
behind `bonus_rule_on`, so the revision module is available for scenario work without
disturbing the reproduction of the worked example.

## Smoothing: the cap, then the corridor

```
S_raw = AS(t)
S_cap = clamp(S_raw, (1−σ)^(1/12)·S(t−1), (1+σ)^(1/12)·S(t−1))       σ = 10% p.a.
S(t)  = clamp(S_cap, 0.80·AS(t), 1.20·AS(t))
```

**The cap is the notes' year-on-year discipline, taken to its twelfth root.** That is
the conversion that keeps the rule's meaning: twelve capped months move the payout by
exactly ±σ over the policy year, where a flat ±σ per month would be twelve times as
loose and a ±σ applied only at anniversaries would leave the eleven intervening payouts
— on which real claims are paid — unsmoothed. `smooth_cap_dn_mth()` and
`smooth_cap_up_mth()` carry the two bounds.

**The order matters.** The cap is what stops a market shock reaching payouts in one step;
the corridor is what stops the cap holding a payout indefinitely away from the asset
share. In the notes' down scenario the cap binds in eleven of the twelve months and the
corridor never does — exactly the pattern the two rules are designed to produce. (Not the
twelfth: the asset share was still above the floor after one month at −1.345%, so the
year's fall lands at −9.0% rather than the −10.0% an annual step would report. That is
the smoothing responding sooner, not the cap failing.)

Two things the cap cannot say, both visible in the shipped cells:

- It is **skipped in the first projected month of a new-business cell**, where the
  opening payout `smoothed_payout_open(t)` is nil and the cap would otherwise clamp the
  payout to nil with it.
- On a **premium-paying** policy it is only loosely meaningful. A firm's ±10% discipline
  is a *like-for-like* comparison between successive maturity cohorts — this year's payout
  on a 25-year endowment against last year's — not a comparison of one policy's own payout
  across its own durations. A regular-premium asset share grows far faster than 10% a year
  early on because premiums, not investment return, dominate it, so the cap's upper bound
  binds and the **corridor floor** is what actually sets the payout: exactly 80% of the
  asset share from `t = 1` through `t = 154` on the shipped endowment cell — `t = 0` is
  the one month where the cap is skipped, so the payout there is the asset share itself.
  After that the corridor floor no longer binds and the capped path alone carries the
  payout up, reaching 100.0% of the asset share at maturity as the asset share outgrows
  the premium. The single-premium bond the worked
  example uses has no such problem, which is why the notes can state the cap plainly.

The corridor implements the 80–120% target range deterministically at model-point level.
The regulatory test is a **portfolio** property — a proportion of policies within the
range — which a single-policy model cannot express, so the corridor is a **[std]** reading
of it. `check_payout_corridor()` asserts it holds every month.

## Final bonus and MVR are never simultaneous

`FB > 0` requires `S > FV` and `MVR > 0` requires `S < FV`, so the two cannot both be
positive. `check_fb_mvr_exclusive()` asserts it, because an implementation that computed
them independently could produce both — and would then pay a final bonus and deduct a
market value reduction on the same exit.

The MVR also carries a **contractual bound**: it may not exceed the excess of the unit
value over the underlying asset value, `max(0, FV − AS)`. `check_mvr_bound()` asserts that
too. In the notes' down scenario the bound is £2,693.46 at the end of the year and the
MVR actually applied is £1,031.08 — comfortably inside it, which is the point of checking
rather than assuming.

`mvr_pp` is the **scale** and `mvr_applied_pp` is what an exit actually bears, which is
zero in a guarantee-date **month** and zero on death. The month, not the year: an exit in
any of the other eleven months of a guarantee-date policy year bears the reduction like
any other, which is a distinction the monthly grid can draw and an annual one cannot.
Both are needed, because the behavioural deterrent keys off the scale being positive
while the payout keys off what is applied.

**The MVR is unitised only.** It is an adjustment to a *unit* value, and the notes define
it for the unitised chassis alone; a conventional endowment has no units to reduce.
Applying the same arithmetic there would be arithmetically harmless — it happens to
collapse the surrender payout onto the asset share — but it would report a £19,575
"market value reduction" in the first policy year of a 25-year endowment, which is not a thing
that exists. The endowment's surrender value is set on a surrender basis instead: the
smoothed payout, capped at the prospective value `G + TB`.

## Behaviour is where the anti-selection lives

Three behavioural adjustments sit on the base surrender rate, all **[std]** and all
rationalized from the incentive structure rather than measured:

| Overlay | Size | Applied to | When |
|---|---|---|---|
| MVR deterrent | ×0.6 | the annual rate | while an MVR would be applied — an active MVR penalizes exit |
| Guarantee-imminent | ×0.8 | the annual rate | in the twelve months before a guarantee date |
| Guarantee-date encashment | 7.5% of survivors | that month alone | in the guarantee-date month, **only when `GB > AS`** |

**The gate on the third is the point.** MVR-free encashment is worth exercising precisely
when the guaranteed benefit exceeds the asset share and worth nothing otherwise, so
exercising unconditionally would invent anti-selection where there is none.
Anti-selective exit when guarantees are in the money is the dominant behavioural risk on
with-profits business, and dynamic assumptions of this kind are a regulatory expectation
for the best estimate rather than an optional refinement.

**It is also the one assumption whose shape the monthly grid changed, not just its
frequency.** On an annual grid the exercise could only be a `×2.5` multiplier on the
whole guarantee-date *year*'s surrender rate, which spreads MVR-free exits across eleven
months in which the window is shut. `guarantee_exercise()` puts it in the month the
option is open, at a rate set so that the guarantee-date year still sheds roughly what
the annual multiplier shed. The first two overlays are diffuse tilts and stay as
multipliers on the annual rate, where `surr_rate_mth()` converts them; the encashment
enters there instead, as
`w_m = 1 − (1 − w_ordinary,m)(1 − ε)`. Neither 2.5 nor 7.5% is measured — no public UK
with-profits lapse experience was retrieved.

## A withdrawal election is not unconditional

The MVR-free allowance is 5% of the original premium a year, and the withdrawing cell
(model point 4) takes the whole of it — a twelfth each month. Against a fund whose growth
is only the declared bonus, that **exhausts the fund**: the cell cancels its last unit at
`t = 403`, in its thirty-fourth policy year, so `fund_exhaust_mth()` is 403. `wd_pp()`
caps the withdrawal at the unit fund it comes out of, and `proj_len()` stops the
projection at the month before exhaustion (`proj_len() = 403`, last row `t = 402`), where
`is_forced_encashment()` marks the ending
as a real contractual event and the survivors are paid `FV + FB` — the residual final
bonus included — rather than nothing. A projection that ends at the *limiting age* pays
nothing there, because that ending is a modelling truncation.

`check_fund_nonneg()` asserts the result, because the failure mode is silent: an uncapped
election turns the unit holding negative, the guaranteed benefit negative with it, and
every number downstream stays plausible enough to read past.

The asset share is floored at zero for the same class of reason. The charges and the
mortality charge do not stop when the balance runs out, so a sustained adverse scenario
drives the raw recursion negative — and a negative asset share would make the payout
*target* negative and invert the corridor, whose bounds are `0.80·AS` and `1.20·AS`. What
a nil asset share means is that the fund backing the policy is exhausted and the guarantee
is being met entirely by the estate, which is what `smoothing_account` then records.

## What a deterministic run cannot do

This is a deterministic single-scenario projection, and it **materially understates the
cost of guarantees**, because guarantee cost is convex in the fund return: the average of
the cost over scenarios exceeds the cost at the average scenario. The `c_g` charge in the
asset share recursion is a *charging* proxy — a deduction firms make — and **not a
valuation of anything**.

What this model produces is exactly the per-scenario cash flow vector a market-consistent
stochastic valuation consumes. The stochastic layer is out of scope, and the notes list a
deterministic base run as the central model risk for precisely this reason.

Read the down cell's tail for what it is, too. A single year at −15% is a market shock;
sixty consecutive years at −15% is not a scenario anyone would value against, and the cell
duly exhausts its asset share and leaves the guarantee entirely estate-funded. That end of
the projection is a demonstration of the machinery under stress, not a result.

## Inputs are external files

The three input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `WP_UK_S/` holds nothing but formulas:

```
products/with_profits/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  WP_UK_S/                    <- formulas only
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
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Six model points. **Points 1 and 2 are the worked example's two scenarios** — a UWP bond in force at duration 5 with AS £30,000, FV £27,602.02, S £29,500, at +7% and −15%; point 3 is the same cell on a 5% base return; point 4 adds the 5% withdrawal election; point 5 is CWP new business (M35, £720 p.a., SA £20,000, 25 years); point 6 is the same policy in force at duration 20 on a gross pension basis | anchor cells **[std]**, technical notes' worked example |
| `mort_table.csv` | Base annual mortality by sex and age 18–120, capped at 1 | **[std]** proxy shaped like the ONS national life tables, anchored so that the 60% best-estimate factor gives the notes' `q(60) = 0.5%` placeholder exactly — *not* a CMI table |
| `lapse_table.csv` | Annual surrender rates by chassis and policy year: bond flat 5%, endowment 5 / 4 / 3 / 2%+ | **[std]**; no public UK with-profits lapse experience was retrieved |

**No input file is keyed by the model's `t`,** so the move to the 0-based index left
every CSV byte-for-byte unchanged. Column by column:

| File | Column | Decision | Why |
|---|---|---|---|
| `lapse_table.csv` | `policy_year` (1 … 4) | unchanged | a contractual 1-based policy-year label; `surr_rate_base()` reads row `policy_year(t) = t // 12 + 1` and caps at the table's last row, returning the **annual** rate |
| `model_point_table.csv` | `duration_inforce` (0, 5, 20) | unchanged | an elapsed count in **years**, 0-based by nature; `proj_start()` is `12 ×` it |
| `model_point_table.csv` | `policy_term` (0, 25) | unchanged | a term *length* in years, not a point on the time axis; `proj_len()` is `12 ×` it on the endowment chassis, whose last month is `12 × policy_term() - 1` |
| `model_point_table.csv` | `guarantee_dates` (10) | unchanged | contractual anniversaries; anniversary `k` ends month `12k − 1`, and `is_guarantee_date()` maps through `policy_year(t)` and `is_declaration_month(t)` |
| `mort_table.csv` | `age` (18 … 120) | unchanged | an attained age, not a time index; read at `age(t) = age_at_entry() + t // 12` |

Nothing was re-keyed to months. A table quoted per policy year stays quoted per policy
year, and the grid conversion lives in the formulas.

Note how little is in a file. **The discretionary scale that actually drives this product
is not in a rate table** — the bonus rates, the smoothing cap, the target corridor, the
guarantee-fill target, the charge levels all live in model point columns and `Projection`
References. That is not an oversight: none of it is published. Firms' principles and
practices documents describe the discretion and withhold the numbers, so every one of
those values is a standardization, and putting them where a reader trips over them is
better than filing them in a table that looks like data.

## The worked example, both scenarios

`tests/test_with_profits_uk.py` asserts every line of this to the penny. It covers the
sixth policy year of a cell in force at duration 5 — months `t = 60 … 71`, with
`AS = 30,000.00`, `S = 29,500.00` and `FV = 27,602.02` as its opening balances — and the
closing rows are month `t = 71`, the declaration month:

| Step | A (r = +7% p.a.) | B (r = −15% p.a.) |
|---|---|---|
| AMC taken over the twelve months | 311.10 | 274.93 |
| Guarantee charge over the twelve months | 30.98 | 27.38 |
| Mortality charge over the twelve months | 0.00 | 4.60 |
| Asset share after return and charges, month 71 | 31,747.19 | 25,216.50 |
| Declared bonus `b` for the policy year | 2.00% | 1.00% |
| Unit price `Q(71)`; face value `FV(71)` | 1.126163; 28,154.07 | 1.115122; 27,878.05 |
| Cost of bonus `CB = b·FV(70)` | 552.04 | 276.02 |
| Shareholder transfer `ST = CB/9` | 61.34 | 30.67 |
| Asset share after `ST` | 31,685.86 | 25,185.83 |
| Mortality charge `MC`, month 71 | 0.00 | 1.24 |
| **Asset share `AS(71)`** | **31,685.86** | **25,184.59** |
| After the smoothing cap `S_cap` | 31,685.86 | 26,846.96 *(floor binds)* |
| Smoothed payout `S(71)` | 31,685.86 | 26,846.96 |
| Final bonus `FB` | 3,531.79 | 0.00 |
| `MVR` (bound) | 0.00 | 1,031.08 *(bound 2,693.46)* |
| Guarantee-date payout | 31,685.86 | 27,878.05 |
| Surrender payout | 31,685.86 | 26,846.96 |
| Death payout | 32,002.72 | 28,156.83 |
| Smoothing cost, guarantee / surrender | 0.00 / 0.00 | 2,693.46 / 1,662.37 |

Scenario B is the one to read. The smoothing cap binds in eleven of the twelve months and
holds the surrender payout to a 9.0% fall over the policy year while the asset share
falls 16.1%; the guarantee bites, so a guarantee-date exit pays £27,878.05 against an
asset share of £25,184.59 and the estate absorbs the £2,693.46 difference; and the MVR
that makes an ordinary surrender pay the smoothed target sits well inside its regulatory
bound. Both scenarios' surrenders land inside the 80–120% corridor — 100.0% and 106.6% of
the asset share.

The payouts, the final bonus and the MVR exist in **every** month of that year, not only
its last. A claim in month 65 is paid on month 65's smoothed payout, which is the
substantive thing the monthly grid adds here: an annual grid can only pay every claim of
a year at the year-end payout.

The endowment chassis has its own check line: twenty-five declarations, one at the end of
each policy year, give `G = 20,000 × 1.015^25 = £29,018.91` at the last projected month
`t = 299`, which the new-business cell reaches exactly — twenty-five, not three hundred,
which is the arithmetic a monthly implementation gets wrong if it compounds `b` monthly.
Against an asset share of £28,339.99 the guarantee bites by £678.91 at maturity on the
base return.

## What is out of scope, and why

The **smoothed-fund (PruFund-style) chassis is not implemented.** Its mechanics are daily
and quarterly — a 5% daily and 10% quarterly smoothing limit with a 2.5% gap trigger — and
a monthly grid still smooths away the limits that define the design — a daily limit needs
a daily step, and a trigger that fires and unwinds between two monthly points is invisible
to this projection, so moving from an annual grid to a monthly one narrows that gap
without closing it. Implementing it here
would produce something that ran and meant nothing, so `chassis()` accepts the two chassis
this grid can carry and rejects the third by name.

Also out of scope, per the notes: paid-up conversion on the endowment chassis; the
guaranteed annuity option module on legacy pension cells (long interest-rate optionality
that needs the stochastic layer to mean anything); estate reattributions and special
bonuses; and the fund-level excess of actual expenses over capped charges, which a
single-policy model cannot see.

## Standardizations used

Everything in this list is **[std]**: the bonus declarations (2.00% UWP / 1.50% CWP) and
holding them level; the AMC of 1.00%, the guarantee and smoothing charge of 0.10% and its
2% lifetime cap; the 60% best-estimate mortality factor and the whole mortality table; the
lapse table and all three dynamic multipliers; the 10% smoothing cap and the 80–120%
corridor at model-point level; the guarantee-fill target θ = 80%, the bonus speed κ = 0.5
and the ±1% change cap; the 101% death uplift and the 4% surrender-basis discount rate;
maintenance expense £30 a policy a year inflating at 3%; death-before-surrender as the
processing order; charging only the *guaranteed* element in the mortality charge's sum at
risk; omitting the survivorship discount from the CWP cost of bonus; and nil estate
distributions in the base run.

## Tests

`tests/test_with_profits_uk.py` asserts both scenarios of the worked example step by step
to the penny — the asset share recursion and its step ordering, the bonus cost and
shareholder transfer, the mortality charge and its sum at risk, the smoothing cap and
corridor, the final bonus, the MVR and its regulatory bound, and all three payout bases —
plus the endowment chassis end to end, the bonus-hardening floor, the three behavioural
overlays in isolation, the withdrawal cap and forced encashment, the guarantee-charge
lifetime cap, the out-of-scope chassis, and all seven invariant checks on every model
point.

The monthly grid adds its own: that the declaration is annual — the unit price and the
guaranteed benefit move in declaration months and nowhere else, and the cost of bonus and
the shareholder transfer are nil in the other eleven — that twelve months of each
converted rate compound back to the annual assumption, and that the MVR-free window is
the guarantee-date month rather than its policy year.

It also pins the frame: `result_cf()` is indexed by
`range(proj_start(), proj_len())`, it opens at `12 × duration_inforce()` and ends at
`proj_len() - 1`, and the new-business endowment opens at `t = 0`. The library-wide
conventions module (`tests/test_model_conventions_uk.py`) asserts the same rule on every
model point of every model.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uklib-std
<!-- END generated citation links -->
