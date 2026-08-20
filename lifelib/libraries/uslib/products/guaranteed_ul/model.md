# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/guaranteed_ul/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md). Those notes build on
the universal life chassis, and so does this model — see
[`products/universal_life/`](../universal_life/index.md) and its
[technical notes](../universal_life/technical-notes.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the 25% premium load and the $5.50 monthly per-policy charge,
> the 2.0% guaranteed credited rate, the 5.0%/3.0% loan rates, the 61-day grace period,
> the return-of-premium percentages and their 40%-of-face cap, the in-force test on the
> shadow account net of indebtedness, the cessation of charges at attained age 121 — are
> sourced from the retrieved carrier documents behind the product spec. **Every
> shadow-account parameter is a `[std]` standardization**: no carrier publishes them and
> no specimen policy form was retrievable. So are the mortality tables, the lapse
> tables, the dynamic-lapse formulas, the exercise rates and every expense. Replace them
> with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/guaranteed_ul/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/guaranteed_ul/ULSG_US_S")
model.Projection[1].result_av()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
There are four result tables, all `DataFrame`s indexed by policy month `t`:

| | |
|---|---|
| `result_av()` | the two account values, in the worked example's own column order |
| `result_guar()` | the guarantee diagnostics: net amounts at risk, `SG − L`, catch-up, grace |
| `result_cf()` | the liability cash flows |
| `result_pols()` | the decrements |

The model and both Spaces carry docstrings — `model.doc` describes the product and the
projection basis, `model.Projection.doc` holds the full mapping between the technical
notes' symbols and the cells names, and `model.Data.doc` explains the input arrangement.

## Monthly, and `t = 1` is not policy month 1

`t` counts **policy months** from the start of the projection, 1-based.
`proj_len() = 12 × (121 − age_at_entry()) − duration_mth_init()` — the notes' maximum
projection length, running to attained age 121 where premiums and all charges cease.

The technical notes index the same months by their **absolute** policy month number,
starting at `duration_months + 1`. Model point 1 is an in-force cell with
`duration_mth = 300`, so the worked example's months **301–305 are `t = 1 … 5`** here,
with `duration_mth(t) = 300 + t − 1`. Getting that offset wrong is the easiest way to
misread the golden table.

State variables the notes define at `t = 0` — `AV_0`, `SG_0`, `L_0`, `CumPrem_0`,
`l_0 = 1`, `g_0 = 0` — are the `t == 0` branch of the corresponding recursion.

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `ULSG_US_S/` holds nothing but formulas:

```
products/guaranteed_ul/
  model_point_table.csv        <- inputs live here
  coi_rates.csv
  corridor_factors.csv
  mort_table.csv
  class_factor_table.csv
  lapse_table.csv
  surr_charge_table.csv
  rop_table.csv
  run.py
  README.md
  ULSG_US_S/              <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its inputs beside the model
and reads them at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores
its inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/`
directory and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every policy. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many policies are projected.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is
read, so it works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `coi_rates_file` | `coi_rates()` | `coi_rates.csv` |
| `corridor_file` | `corridor_factors()` | `corridor_factors.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `class_factor_file` | `class_factor_table()` | `class_factor_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |
| `rop_file` | `rop_table()` | `rop_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `ULSG_US_S/` without
the CSVs and it will read fine, then fail on first evaluation. What you gain is that a
diff of the model shows logic changes only, and an input can be edited or swapped in
place — point `Data.mort_table_file` at another same-schema file and the projection
follows, with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Four points, all on the anchor cell M60 / StdNT / $500,000. **Point 1 is the worked-example cell** (in force at 300 months, AV $2,400, SG $118,000, level $10,800); point 2 is the same policy from issue on the notes' behavioural basis; point 3 funds the lifetime guarantee with one premium; point 4 elects a guarantee to age 90 and underfunds it | attributes from the notes' model point table; the opening cumulative premium and the extra points **[std]** |
| `coi_rates.csv` | Guaranteed **annual** maximum COI per $1,000 by attained age, M / StdNT only | **[std]** Perks curve, `c = 1.115`, fitted to the two figures the notes state — 8.615 per $1,000 per month at attained age 85 and a solved lifetime `P*` near $10,800. **Not** the 2017 CSO table |
| `corridor_factors.csv` | GPT corridor factors by attained age: the IRC 7702(d)(2) applicable percentages in full, 250% to age 40 down to 100% from age 95 | sourced [R4]; never binds on a thin-account design |
| `mort_table.csv` | Best-estimate annual mortality by attained age | **[std]** the same curve at 72% of the guaranteed basis, *not* the 2015 VBT the notes recommend |
| `class_factor_table.csv` | Rate-class factors for the four NT and two tobacco classes [S4] | **[std]** |
| `lapse_table.csv` | Base annual lapse by policy year: 4.0 / 3.0 / 2.5 / 2.0 / 1.5 / 1.0 / 0.75% | **[std]** shape anchored to [R7], [REG-R20], [REG-R21] |
| `surr_charge_table.csv` | 15-year linear schedule, $18 per $1,000 of initial face | **[std]** (spec note) |
| `rop_table.csv` | Refund windows at anniversaries 20 and 25 | ratios, anniversaries and the cap [S1]; exercise rates **[std]** |

Neither mortality table is a published one. The 2017 CSO and 2015 VBT families are
licensed and the notes forbid hard-coding them; both files here are illustrative and
swappable by repointing their Reference.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those
models have an analogue, and this library's own `UL_US_S` — the chassis this
product is built on — everywhere else: `pols_*` for policy counts, `av_*` for account
values, plural nouns for cash flows, `*_rate` for rates, `*_pp` for per-policy amounts,
`timing` and `kind` string arguments, `result_cf` / `result_pols` / `result_av`,
`check_av_roll_fwd` / `check_margin`. Names introduced here are the ones guaranteed UL
genuinely adds: the shadow account (`sg_*`), the guarantee tests, the grace counter, the
forgone deduction and the return-of-premium endorsement.

`result_cf()` follows the library-wide column set: lower snake case, indexed by `t`,
`pols_if` the start-of-month weight applied to that same row, and the cash flow columns
summing to `net_cf` income-positive. The surrender column is **`claims_lapse`**, named
for the `"LAPSE"` kind that produces it, and partial withdrawals are **`withdrawals`**,
a column of their own rather than a claim. Every `check_*` here takes no argument and
returns a `bool` over the whole projection, so one test can call the same check across
the library.

The full notes-symbol → cells-name table lives in the `Projection` Space docstring, and
it covers every symbol the notes define, model point attributes included. Nine cases
needed care:

| Notes | Cells | Why |
|---|---|---|
| `risk_class` | `rate_class` | The name `Term_US_A` and `UL_US_S` both use for the underwriting class, and the one the model point table column carries. The only model point attribute renamed on cross-model grounds rather than for a reason internal to this product |
| `l_t` | `pols_if(t)`, no offset | These notes define `l_t` at the **beginning** of month `t`; the universal life notes define theirs at the **end**, so the chassis has `pols_if(t) = l(t−1)` and this model does not |
| `AV'(t)` | `av_pp_at(t, "BEF_COI")` | Measured **after the expense charges**, one step later than the chassis' `"BEF_FEE"` — a deviation the notes flag deliberately |
| `CSV_t` | `ncsv_pp(t)` | The notes' `CSV_t` already nets indebtedness, so it is the chassis' *net* cash surrender value, not its `csv_pp` |
| `D_t` | `mth_deduction_forgone_pp(t)` | Split from `mth_deduction_taken_pp`, which is what the roll-forward uses |
| "guarantee active" | `is_guar_active` / `is_guar_supported` | The notes use the same words for two tests at different measurement points |
| `MD` non-COI part | `maint_fee_pp(t)` | A charge *against the account value*, i.e. income — not `expenses`, which is the insurer's own outgo |
| `W_t` (the cash flow) | `withdrawals(t)` | A withdrawal is a payment on the owner's election out of a policy that stays in force, not a claim, so it is its own cells and its own `result_cf()` column; `claims(t, "WITHDRAWAL")` raises |
| `phi_t` | `prem_persistency(t)` | See below |

## The forgone deduction is the product

`products/universal_life/technical-notes.md` warns against carrying its recursions
across unexamined, and the account-value recursion is exactly where guaranteed UL parts
company with it. On the universal life chassis a monthly deduction the account cannot
carry triggers a grace period and, in short order, a lapse. Here it usually does not:

```
AV''(t) = AV'(t) − COI(t)
if AV''(t) < 0 and SG''(t) − L(t−1) > 0:      # the guarantee is standing
    D(t) = −AV''(t);  AV''(t) = 0             # the insurer funds the shortfall
else:
    grace
```

`D(t)` — `mth_deduction_forgone_pp` — **is not a receivable.** It never accrues against
future premiums and it is never recovered out of an account-value recovery. The
worked-example anchor demonstrates both halves: month 304 takes $1,965.90 of a
$2,890.47 deduction and forgoes $924.57; months 305 onward forgo the whole $2,900.88;
and when the next annual premium arrives twelve months later the full $8,100 net premium
is credited to an account value of zero, with none of the ~$24,000 of forgone deductions
netted off. A test asserts precisely that.

From month 305 the net amount at risk is the entire discounted death benefit and the
cost of insurance charged on it is forgone. That is the "negative account economics"
regime the notes describe, and it is what dominates late-duration guaranteed UL
liability cash flows. `margin_mortality(t)` goes deeply negative there, which is the
model saying the same thing.

### The zero floor is unconditional here, and in the notes it is not

The notes' pitfall list says `AV` "floors at 0 only while the guarantee is active", and
their step 6 sets `AV''(t) = 0` in the guarantee branch alone — the grace branch gets no
account-value recursion at all. **This model floors the account value unconditionally**,
in the grace months and after a lapse as well. It is a deliberate `[std]` deviation, for
two reasons: a negative balance would break `check_av_roll_fwd()`, which closes on the
deduction actually *taken* and nothing is taken from an exhausted account; and the notes
give the grace branch nothing to implement.

No cash flow moves. Nothing is deducted either way, a policy in grace surrenders for
nothing by construction, and `pols_if(t)` is zero once it has lapsed, so every in-force
weighted figure is zero from there on. Two things do follow, and they are worth knowing
before reading a per-policy column:

- `mth_deduction_forgone_pp(t)` keeps reporting the shortfall in the grace months. On
  the anchor that is $5,007.40 a month at `t = 81` and `t = 82`, where the guarantee has
  already failed. It is the guarantee's running cost only while `is_guar_supported(t)`
  holds; in grace the same number is the notes' *required grace payment*, which is why
  `cure_premium_pp(t)` is built from it. `result_guar()` prints
  `mth_deduction_forgone` next to `is_guar_active` so the two are read together.
- The per-policy account value goes on projecting after the lapse. At `t = 85` the
  anchor's next annual premium credits $8,100 to `av_pp`, on a row whose `status(t)` is
  `LAPSED` and whose `pols_if(t)` is zero.

`test_the_zero_floor_is_unconditional_and_that_is_a_deviation` pins all of it, so the
deviation cannot be forgotten or quietly closed.

## The shadow account is never floored

`sg_pp(t)` has no zero floor anywhere. Its negative part **is** the catch-up
requirement: `catch_up_prem_pp(t) = max(0, −(SG_t − L_t)) / (1 − 8%)`. Flooring it at
zero would destroy the catch-up computation and misprice restoration, which the notes
list among the pitfalls. `check_sg_roll_fwd()` closes the shadow recursion arithmetic
month by month and would fail the moment a floor crept in; model point 4 drives the
balance negative so that the test has something to catch.

The two accounts also discount the death benefit at **different** rates —
`naar_factor() = 1 + j_g` on the real account, `sg_naar_factor() = 1 + j^g` on the
shadow — so their net amounts at risk differ even before their balances do.

## The order of tests

The notes are explicit that the guarantee test must run **after** the full monthly
deduction attempt, because testing before it lets a policy lapse a month early or late
at exactly the durations where the net amount at risk is the whole death benefit. The
model does that, and it uses two tests rather than one:

- `is_guar_supported(t)` — the step-6 test `SG''(t) − L(t−1) > 0`, before the interest
  credits, which decides whether a failed deduction is forgone or opens the grace;
- `is_guar_active(t)` — the step-9 in-force test `SG(t) − L(t) > 0`, after them.

The anchor's account value fails in month 4 of the projection and its guarantee holds
for another 77 months. The grace period opens in month 81 — the first month with
`SG − L ≤ 0` — runs the `[std]` two-month discretization of the 61-day grace, and the
policy lapses at the beginning of month 83 with no value. `pols_lapse_grace(t)` carries
those policies out of the in-force roll-forward: it is a contractual termination, not a
rate-based decrement, so it takes the whole remaining block at once and pays nothing.

## The COI-scale precision divergence is shipped, not resolved

The notes state a rule — the current COI scale is 65% and the shadow scale 55% of the
guaranteed maximum — and a worked example computed with `m = 5.60` and `m^g = 4.74` at
attained age 85. But 65% and 55% of the notes' own `m^max = 8.615` are **5.59975** and
**4.73825**. The worked example uses the rounded figures, which is how the notes quote
them; the difference is about $0.12 a month of base deduction and **$0.65** of shadow
deduction — an order of magnitude more than the cent-level rounding that explains the
rest of that table, and enough to move the golden numbers.

Rather than pick one, the model ships both. `coi_rate_dp()` reads a model point column
giving the number of decimal places the declared scales are quoted to per $1,000. Point
1 sets it to **2**, which reproduces the notes' table and is a perfectly ordinary way
for an admin system to carry a rate table; points 2–4 leave it blank and take the rule
at full precision. `test_coi_scale_precision_divergence_is_shipped_not_resolved` pins
both readings and the size of the gap, so it cannot be closed silently in either
direction. Neither value is "right" — the entire scale is a standardization.

## What is left of the worked example after that

With the 2-decimal scales in place the model reproduces every figure of the notes'
five-row table to within **6 cents**, and the residual is entirely the notes' own
display rounding. Two sources:

1. The notes' arithmetic line uses the net-amount-at-risk discount **rounded to the
   whole dollar** — `499,176` rather than 499,175.57 on the base account and `497,774`
   rather than 497,774.10 on the shadow. `test_notes_naar_constants_are_dollar_roundings`
   names both.
2. The notes cascade cent-rounded intermediates from row to row. Their shadow interest
   column runs a cent or so low in every row, and by month 305 the shadow balance has
   drifted 5.6 cents from a clean recomputation. That is the worst figure in the table;
   every base-account figure is within about a cent.

The notes anticipate this: *"Independent recomputation may differ by cents due to
rounding."* `test_worked_example_gap_is_only_the_notes_rounding` pins the bound at 6
cents and also asserts the gap is **not** zero, so neither side can drift.

## Premium persistency: applied once, and overridden on the anchor

The notes are not self-consistent about where the premium persistency probability
`phi` belongs. Their cash flow list writes premium income as `l_t · phi_t · P_t`, while
their step 2 credits `(1 − pi) · P_t` to the account value — which would hand the
account and the shadow account more than the insurer actually received. This model
applies `phi` **once**, to the premium received, so the account value, the shadow
account, the cumulative premium and the premium income all move together.

That leaves the worked example, which is explicitly a *contract-mechanics* view with
the behavioural assumptions suppressed. Premium persistency is a class (c) behavioural
assumption, so model point 1 carries `prem_persistency_override = 1.00`; points 2 and 4
take the notes' 98%.

The consequence is worth seeing, and worth stating exactly. Point 2 pays the notes'
`P* = $10,800`, which is $3.93 *under* this model's own solved $10,803.93 — so it is
marginally underfunded before persistency is applied at all, and its lifetime guarantee
was always going to fail. On the contractual path with persistency off,
`sg_pp_solve(t, 10800)` first turns non-positive at **`t = 632`, attained age 112**.
Apply the 98% and the same recursion at `10800 × 0.98` fails at **`t = 503`, attained
age 101** — which is exactly where the model's own `is_guar_active(t)` first goes False
on point 2. Two percent of premium moves the guarantee failure eleven years earlier.
That is the notes' own third sensitivity — *"a 98% vs. 100% payment probability
materially shifts guarantee failure times for exactly-funded level payers"* — reproduced
rather than described, and
`test_premium_persistency_shifts_the_guarantee_failure_time` asserts the eleven-year
shift itself, not merely that the paid premium is under `P*`.

## The anchor's opening shadow balance is not a funded lifetime guarantee

The notes' model point carries `sg_init = 118,000` at duration 300 together with a
level `P* = 10,800` and a lifetime guarantee. Those do not reconcile: under the notes'
own `[std]` shadow parametrization a policy funded at `P*` from issue would be carrying
roughly twice that at duration 300, and `no_lapse_premium()` on point 1 — the level
premium needed *from the projection start* given $118,000 — returns about **$31,000**.
So the anchor's guarantee fails at attained age 91 and the policy lapses shortly after.

Both figures are labelled illustrative in the notes, and the model ships them as given
rather than adjusting either. `test_in_force_anchor_is_not_a_fully_funded_lifetime_guarantee`
records the consequence. It is also what makes point 1 a useful cell: it is the only
shipped model point that walks the full cascade — funded, guarantee-supported, catch-up
territory, grace, lapse — inside a projection short enough to read.

## The funding-premium solve is implemented

The notes give the complete algorithm, so `no_lapse_premium()` implements it:
`guar_min_sg(prem)` replays the shadow recursion under a hypothetical premium with
decrements and premium persistency off — the solve is contractual, not behavioural —
and the bracket doubles then bisects to $0.01 of annual premium, targeting
`g(P) > 0` **strictly** (a `≥ 0` target on a monthly grid can leave the guarantee
failing on the final monthiversary). Payment months are the model point's own, so
single-pay and n-pay premiums solve over their own premium vectors.

It is a side calculation — nothing in the projection depends on it — and it is also the
calibration hook. The shipped guaranteed-maximum COI curve is fitted so that the
from-issue anchor cell solves to **$10,804**, against the notes' illustrative
`P* = $10,800`. Both the target and the curve are `[std]`.

## Not implemented

Named here and in the model docstring so their absence is not mistaken for an oversight:

- **the cumulative-premium-test guarantee design** (AG 38 8E Design #2) — the notes
  document the swap but give no required-premium schedule, so there is nothing to
  project;
- **catch-up premium payment** — `catch_up_prem_pp()` computes the requirement; the
  notes state expressly that catch-up behaviour is not modelled in the base run;
- **grace cure** — `cure_premium_pp()` computes the payment; the notes give no cure
  probability, so a policy in grace always lapses;
- **new policy loans, repayments and withdrawal utilisation** — the mechanics are all
  implemented, but the notes set utilisation to zero and give no pattern;
- **7702 / 7702A guideline and MEC testing** — flagged out of model by the notes; caps
  and flags, not cash flows, and no guideline inputs are given for this product;
- **terminal illness acceleration** (cash-flow-neutral by the notes),
  **selective-lapse mortality adjustment** (excluded expressly) and **NGE re-rating**;
- **reserves** — VM-20 ULSG, AG 38 and A-830 consume these cash flows and are cited,
  not reproduced.

## Standardizations used

Everything in this list is **[std]**: the entire shadow parameter set (8% load, 5.5%
credited, 55% COI factor, $0.05 per unit, no per-policy charge); the $0.20 base
per-unit charge; the 65% current COI factor and the 3.5% current credited rate; the
illustrative guaranteed-maximum COI curve and the best-estimate mortality table; the
rate-class factors; the base lapse vector and the lifetime multiplier's flat duration
shape; the premium-pattern and funding-status dynamic factors, the 0.3% floor and the
50% cap; the 1%-grading-to-0% mortality improvement and its 20-year limit; the 15-year
$18 per $1,000 surrender charge; the 5% and 10% return-of-premium exercise rates; the
98% premium persistency; the $300 plus 90%-of-first-year-premium acquisition expense,
the $75 inflating maintenance expense and the $300 claim expense; the two-month
discretization of the 61-day grace; the one-month return-of-premium exercise window;
the even split of a modal premium; the unconditional zero floor on the account value,
where the notes floor it only under a live guarantee; and the `coi_rate_dp` pin on
model point 1. The
percent-of-premium tax the universal life chassis carries is **zero** here, because the
guaranteed-UL notes' expense list has no such item — commission sits inside the
acquisition expense instead.

## Tests

`tests/test_guaranteed_ul_us.py` asserts all five rows and eleven columns of the notes'
worked example against hard-coded goldens; the notes' dollar-rounded NAAR constants and
the exact bound on the residual gap; the COI-scale precision divergence in both
directions; one test per entry in the notes' "Known modeling pitfalls" list — the NAAR
discount convention and its zero floor, the simple-twelfth COI conversion against the
compound experience conversion, the account-value floor **and the fact that this model
applies it unconditionally where the notes do not**, forgone deductions not being
receivables, the shadow account never being floored, the order of the guarantee tests,
and the ANB basis; the corridor table against the IRC 7702(d)(2) applicable percentages
at every statutory breakpoint; the eleven-year guarantee-failure shift a 98% premium
persistency produces; the in-force, account-value, shadow-account and margin roll-forwards
on all four model points; the return-of-premium windows and the 40%-of-face cap; the
three lapse multipliers; the surrender-charge run-off; the mortality-improvement grading
and its 20-year cap; the funding-premium solve against the notes' calibration; and that
every model point in the table projects.

It also pins the library-wide conventions this model shares: that the `result_cf()`
columns sum to `net_cf` income-positive, that `pols_if(t)` is the start-of-month count
weighting its own row, that a withdrawal is `withdrawals(t)` and `claims(t,
"WITHDRAWAL")` raises so the claims total cannot double-count it, and that every
`check_*` is a no-argument `bool`.

```bash
python -m pytest tests/test_guaranteed_ul_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_guaranteed_ul_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_guaranteed_ul_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R4]: #uslib-guaranteed_ul-r4
[R7]: #uslib-guaranteed_ul-r7
[REG-R20]: #uslib-reg-r20
[REG-R21]: #uslib-reg-r21
[std]: #uslib-std
<!-- END generated citation links -->
