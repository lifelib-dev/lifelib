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
model = mx.read_model("products/with_profits/WP_UK_A")
model.Projection[1].result_cf()
```

`result_payout()` gives the payout machinery — asset share against guaranteed benefit
against smoothed payout, and the final bonus or MVR the gap between them produces.
`result_cf()` gives the cash flows.

## The asset share is a state variable, not a cash flow

That sentence is the model.

```
AS(t) = [AS(t−1) + P(t) − W_AS(t)]·(1 + r(t))·(1 − c_amc − c_g) − ST(t) − MC(t) + M(t)
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

`asset_share_at(t, timing)` exposes the recursion one step at a time — `"BEF_RETURN"`,
`"AFT_RETURN"`, `"AFT_CHARGE"`, `"AFT_ST"`, `"AFT_MC"` — because the order is
**contractual discipline** rather than arithmetic convenience: the shareholder transfer
is charged to asset shares *after* the charges and *before* the mortality charge, and the
mortality charge's sum at risk is measured on the balance after the transfer.
`check_asset_share_roll_fwd()` rebuilds the whole recursion in one expression and asserts
it closes, so a mis-ordered step shows up rather than quietly shifting the answer.

## The bonus hardens, and that is what makes guarantees expensive

A declared regular bonus increases the guaranteed benefit **permanently**. The unit price
therefore never falls — `b(t) ≥ 0` is a contractual floor, not a modelling choice — and
every declaration converts non-guaranteed final bonus into guaranteed benefit *without
changing the target payout*. That is the whole tension the discretion manages.

| | Bond chassis (UWP) | Endowment chassis (CWP) |
|---|---|---|
| Guaranteed benefit | `FV(t) = U(t)·Q(t)`, unit face value | `G(t) = SA + attaching bonuses` |
| Rolls forward by | `Q(t) = Q(t−1)(1 + b(t))` | `G(t) = G(t−1)(1 + b_rev(t))` |
| Cost of bonus | `b(t)·FV(t−1)` | `ΔG(t)·v_sv^(n−t)` |
| Death benefit | `1.01 × (FV + FB)` | `G + TB` |
| Surrender | `FV + FB − MVR` | smoothed payout, capped at `G + TB` |
| Maturity | none — whole of life | `G(n) + TB(n)` |

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
S_cap = clamp(S_raw, (1−σ)·S(t−1), (1+σ)·S(t−1))       σ = 10%
S(t)  = clamp(S_cap, 0.80·AS(t), 1.20·AS(t))
```

**The order matters.** The year-on-year cap is what stops a market shock reaching payouts
in one step; the corridor is what stops the cap holding a payout indefinitely away from
the asset share. In the notes' down scenario the cap binds at −10% and the corridor then
does not — exactly the pattern the two rules are designed to produce.

Two things the cap cannot say, both visible in the shipped cells:

- It is **skipped in the first projected year of a new-business cell**, where `S(t−1) = 0`
  would otherwise clamp the payout to nil.
- On a **premium-paying** policy it is only loosely meaningful. A firm's ±10% discipline
  is a *like-for-like* comparison between successive maturity cohorts — this year's payout
  on a 25-year endowment against last year's — not a comparison of one policy's own payout
  across its own durations. A regular-premium asset share grows far faster than 10% a year
  early on because premiums, not investment return, dominate it, so the cap binds
  throughout and the **corridor floor** is what actually sets the payout: 80% of the asset
  share at duration 1 on the shipped endowment cell, rising to 100.0% at maturity as the
  asset share outgrows the premium. The single-premium bond the worked example uses has no
  such problem, which is why the notes can state the cap plainly.

The corridor implements the 80–120% target range deterministically at model-point level.
The regulatory test is a **portfolio** property — a proportion of policies within the
range — which a single-policy model cannot express, so the corridor is a **[std]** reading
of it. `check_payout_corridor()` asserts it holds every year.

## Final bonus and MVR are never simultaneous

`FB > 0` requires `S > FV` and `MVR > 0` requires `S < FV`, so the two cannot both be
positive. `check_fb_mvr_exclusive()` asserts it, because an implementation that computed
them independently could produce both — and would then pay a final bonus and deduct a
market value reduction on the same exit.

The MVR also carries a **contractual bound**: it may not exceed the excess of the unit
value over the underlying asset value, `max(0, FV − AS)`. `check_mvr_bound()` asserts that
too. In the notes' down scenario the bound is £2,704.05 and the MVR actually applied is
£1,328.04 — comfortably inside it, which is the point of checking rather than assuming.

`mvr_pp` is the **scale** and `mvr_applied_pp` is what an exit actually bears, which is
zero on a guarantee date and zero on death. Both are needed, because the behavioural
deterrent keys off the scale being positive while the payout keys off what is applied.

**The MVR is unitised only.** It is an adjustment to a *unit* value, and the notes define
it for the unitised chassis alone; a conventional endowment has no units to reduce.
Applying the same arithmetic there would be arithmetically harmless — it happens to
collapse the surrender payout onto the asset share — but it would report a £19,575
"market value reduction" in policy year 1 of a 25-year endowment, which is not a thing
that exists. The endowment's surrender value is set on a surrender basis instead: the
smoothed payout, capped at the prospective value `G + TB`.

## Behaviour is where the anti-selection lives

Three multipliers sit on the base surrender rate, all **[std]** and all rationalized from
the incentive structure rather than measured:

| Overlay | Factor | When |
|---|---|---|
| MVR deterrent | 0.6 | while an MVR would be applied — an active MVR penalizes exit |
| Guarantee-date spike | 2.5 | in a guarantee-date year, **only when `GB > AS`** |
| Guarantee-imminent | 0.8 | in the year before a guarantee date |

**The gate on the second is the point.** MVR-free encashment is worth exercising precisely
when the guaranteed benefit exceeds the asset share and worth nothing otherwise, so
applying the spike unconditionally would invent anti-selection where there is none.
Anti-selective exit when guarantees are in the money is the dominant behavioural risk on
with-profits business, and dynamic assumptions of this kind are a regulatory expectation
for the best estimate rather than an optional refinement.

## A withdrawal election is not unconditional

The MVR-free allowance is 5% of the original premium a year, and the withdrawing cell
(model point 4) takes the whole of it every year. Against a fund whose growth is only the
declared bonus, that **exhausts the fund**: the cell cancels its last unit in policy year
34. `wd_pp()` caps the withdrawal at the unit fund it comes out of, and `proj_len()` stops
the projection the year before exhaustion, where `is_forced_encashment()` marks the ending
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
folder. `WP_UK_A/` holds nothing but formulas:

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
  WP_UK_A/                    <- formulas only
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

Note how little is in a file. **The discretionary scale that actually drives this product
is not in a rate table** — the bonus rates, the smoothing cap, the target corridor, the
guarantee-fill target, the charge levels all live in model point columns and `Projection`
References. That is not an oversight: none of it is published. Firms' principles and
practices documents describe the discretion and withhold the numbers, so every one of
those values is a standardization, and putting them where a reader trips over them is
better than filing them in a table that looks like data.

## The worked example, both scenarios

`tests/test_with_profits_uk.py` asserts every line of this to the penny:

| Step | A (r = +7%) | B (r = −15%) |
|---|---|---|
| Asset share after fund return | 32,100.00 | 25,500.00 |
| After charges (× 0.989) | 31,746.90 | 25,219.50 |
| Declared bonus `b(6)` | 2.00% | 1.00% |
| Unit price `Q(6)`; face value `FV(6)` | 1.126162; 28,154.06 | 1.115122; 27,878.04 |
| Cost of bonus `CB = b·FV(5)` | 552.04 | 276.02 |
| Shareholder transfer `ST = CB/9` | 61.34 | 30.67 |
| Asset share after `ST` | 31,685.56 | 25,188.83 |
| Mortality charge `MC` | 0.00 | 14.84 |
| **Asset share `AS(6)`** | **31,685.56** | **25,173.99** |
| After the smoothing cap `S_cap` | 31,685.56 | 26,550.00 *(floor binds)* |
| Smoothed payout `S(6)` | 31,685.56 | 26,550.00 |
| Final bonus `FB` | 3,531.50 | 0.00 |
| `MVR` (bound) | 0.00 | 1,328.04 *(bound 2,704.05)* |
| Guarantee-date payout | 31,685.56 | 27,878.04 |
| Surrender payout | 31,685.56 | 26,550.00 |
| Death payout | 32,002.42 | 28,156.82 |
| Smoothing cost, guarantee / surrender | 0.00 / 0.00 | 2,704.05 / 1,376.01 |

Scenario B is the one to read. The smoothing cap holds the surrender payout at exactly
−10.0% year on year while the asset share falls 16.1%; the guarantee bites, so a
guarantee-date exit pays £27,878.04 against an asset share of £25,173.99 and the estate
absorbs the £2,704.05 difference; and the MVR that makes an ordinary surrender pay the
smoothed target sits well inside its regulatory bound. Both scenarios' surrenders land
inside the 80–120% corridor — 100.0% and 105.5% of the asset share.

The endowment chassis has its own check line: `G(25) = 20,000 × 1.015^25 = £29,018.91`,
which the new-business cell reaches exactly, against an asset share of £28,903.84 — so the
guarantee bites by £115 at maturity on the base return.

## What is out of scope, and why

The **smoothed-fund (PruFund-style) chassis is not implemented.** Its mechanics are daily
and quarterly — a 5% daily and 10% quarterly smoothing limit with a 2.5% gap trigger — and
an annual grid smooths away the very limits that define the design. Implementing it here
would produce something that ran and meant nothing, so `chassis()` accepts the two chassis
the annual grid can carry and rejects the third by name.

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
multipliers in isolation, the withdrawal cap and forced encashment, the guarantee-charge
lifetime cap, the out-of-scope chassis, and all six invariant checks on every model point.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uklib-std
<!-- END generated citation links -->
