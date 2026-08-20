# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/term_assurance/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the decreasing-shape amortization, the family
> income benefit as an annuity-certain, terminal illness as an acceleration rather than
> an extra benefit, the absence of any surrender value, the indexation caps. Every
> quantitative assumption is a **[std]** standardization: no UK insurer publishes
> premium rate tables (pricing is quote-driven, and only the £5/month minimum is
> public [S5]), and the current CMI "16" Series assured lives tables are
> subscriber-restricted [R11]. Replace them with company data and licensed tables
> before drawing any conclusion from the numbers.

## Run it

```bash
python products/term_assurance/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/term_assurance/Term_UK_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy year `t` with one column per
cash flow line.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## No tail states — the structural contrast with `Term_US_A`

Policy year `t` runs 1 … `proj_len()` = `policy_term()`, and **there is nothing after
it**. Cover ceases at the end of the term with no maturity value, no renewal and no
conversion [S1] [S2] [S6] [S8] [R8].

That is the one difference from this library's U.S. term model that changes the shape
of the liability rather than a parameter. `Term_US_A` runs a *post-level-term* phase:
premiums jump to ART rates at the end of the level period, a shock lapse takes 80% of
the block, the survivors are loaded for mortality deterioration, and coverage continues
to attained age 95. None of that exists here — no `phase`, no `jump_ratio`, no
`shock_lapse_rate`, no `plt_mort_factor`, no `conv_rate`. The notes list importing a
U.S.-style post-level-term tail as a modelling pitfall precisely because it materially
misstates UK term liabilities.

What has no U.S. analogue, in the other direction, is the **family income benefit**
ledger below.

## Annual, not monthly

The notes' base grid is annual, with a monthly variant described but not implemented,
so `premium_mode` is inert. Two annual-grid approximations are wired in and are, per
the notes, an offsetting pair:

- the decreasing shape's death benefit is the **mid-year** balance `B(12(t−1) + 6)`;
- premiums are **annual in advance**, with no allowance for premiums ceasing at a
  mid-year death or lapse, which slightly overstates income.

The notes are explicit that applying a further half-year premium adjustment on top of
the mid-year claim timing would double-count the correction. The monthly grid is the
arbiter of both.

## Inputs are external files

The four input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Term_UK_A/` holds nothing but formulas:

```
products/term_assurance/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  select_factor_table.csv
  lapse_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Term_UK_A/                  <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its input file beside the
model and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which
stores its inputs *inside* the model through modelx's IOSpec machinery — hence no
`_data/` directory and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every policy. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many policies are projected. A test counts the reads.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is
read, so it works wherever the repository is checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `select_factor_file` | `select_factor_table()` | `select_factor_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `Term_UK_A/` without the
CSVs and it will read fine, then fail on first evaluation. What you gain is that a diff
of the model shows logic changes only, and an input can be swapped in place — point
`Data.mort_table_file` at another same-schema file and the projection follows, with no
formula change. Tests cover both halves of that bargain.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eight model points. **Point 1 is the worked-example anchor cell** (M35 / non-smoker / level / 25-year / £150,000 / £12.00 per month); points 2–8 exercise the decreasing and FIB shapes, FIB commutation, indexation, joint first death, the select mortality basis with waiver of premium, and one policy already in force at duration 5 | anchor cell **[std]**, technical notes' worked example |
| `mort_table.csv` | Mortality including terminal illness by sex, smoker status and age 18–100, with a `provenance` column marking each row | M/N ages 35–37 are the notes' illustrative worked-example vector; every other cell is a 9% p.a. geometric extension in age with a 2.2 smoker and a 0.70 female factor — all **[std]**, *not* a published table |
| `select_factor_table.csv` | Select-duration factors, 0.55 grading to 1.00 over a 5-year select period | **[std]**; the select period is the TMNL16/TFNL16 structure [R12] |
| `lapse_table.csv` | Annual lapse by policy year, 10 / 8 / 7 / 5 / 6 / 4 % | **[std]**, anchored to the FCA 5% in-force average and the clawback-spike pattern [R9] |

## Two mortality bases, and why there are two

UK assured lives tables are **select** tables — TMNL16/TFNL16 have a 5-year select
period, AM92 a 2-year one [R12] — so the mortality interface has to accept a rate
depending on duration since entry as well as attained age. `mort_rate_base(t, life)`
and `select_factor(t)` provide it.

But the notes' worked example is quoted as three *applied* rates, `q(1) = 0.00055`,
`q(2) = 0.00060`, `q(3) = 0.00065`, described as illustrative values in the shape of a
non-smoker temporary assurance table and explicitly **not** taken from any CMI table.
Three numbers rising at 9% a year are not consistent with a graduated select structure,
where the wearing-off of selection alone moves the applied rate faster than that.
Forcing them onto one would mean either a back-solved ultimate curve that is nearly
flat at ages 35–37 or shipped cells that deviate from the notes.

So both readings ship, as a model point column — the same device `SPIA_US_S` uses for
its `table` / `scenario` split:

| `mort_basis` | What `mort_table.csv` is read as | Model points |
|---|---|---|
| `applied` **[std]** | the rate actually applied — no select factor, no proxy scaling | 1–6, 8 |
| `select` | an **ultimate** basis, multiplied by `select_factor(duration)` and by `mort_scale`, the notes' **[std]** 75% proxy for improvement from the public "00" Series era to the 16-Series era | 7 |

Neither is "correct" — both are standardizations, and the point of shipping both is
that the gap cannot be closed silently in either direction. A production run replaces
the two CSVs with licensed tables and uses the `select` basis; no formula changes.

## The family income benefit ledger

A death in month `k` on the `fib` shape triggers `N − k` monthly instalments of `I`, in
arrears, ending at month `N`. Those instalments are an **annuity-certain**: once the
claim is admitted they run to the end of the term regardless of any life [S6] [S8]. So
the in-payment stream is decremented by neither mortality nor lapse — only *new* claims
carry `l(t)`.

`fib_cum(t)` is the ledger: the expected streams already in payment at the start of
year `t`. With deaths at mid-year on the annual grid **[std]**,

```
claims(t, "FIB") = I × [6 × D(t) + 12 × FIBcum(t)]
```

and one death in year `s` generates `6 + 12(n − s)` instalments in total, which is
exactly `N − k` at `k = 12(s−1) + 6`. `check_fib_ledger()` rebuilds each year's
instalment count straight off the death vector, with no reference to the recursion, and
asserts the two agree; a ledger decremented by mortality — the notes' pitfall — or one
paying only the year-of-death instalments fails there.

The optional commutation module replaces a proportion of the streams with a lump sum,
the present value of the remaining instalments at the **[std]** snapshot rate
`r_c = 3%`. Contractually the insurer reduces the remaining instalments "fairly and
reasonably" [S6] [S8] and no insurer publishes the basis. Base take-up is zero; model
point 4 exercises the other extreme, and its total outgo is materially lower than point
3's because commuting at 3% is worth less than paying the instalments out undiscounted.

## Terminal illness is not an extra benefit

Terminal illness is a 100% **acceleration** of the death benefit under a two-limb
12-month definition [S1] [S6] [S8]: one decrement, one payment. There is no `ti_rate`
anywhere in the model, and `mort_rate(t)` is the combined death-and-terminal-illness
rate — the 16-Series tables the shipped table proxies are graduated on that basis
[R10]. Adding a separate terminal-illness decrement double-counts claims, which is the
notes' first-listed pitfall.

## `claims_lapse` is a column of zeros, deliberately

There is no surrender value and no paid-up value at any duration [S1] [S6] [S8] [R8], so a
lapse is a pure decrement: it moves `pols_if` and pays nothing. `claims(t, "LAPSE")`
exists, returns zero, and appears in `result_cf()` as a zero column, because the notes
list a non-zero lapse row as a pitfall imported from US models with cash surrender
values. A column of zeros states the product fact; a missing column would only hide it.

## `pols_maturity` — the one cells the notes do not define

The notes give the roll-forward as `l(t+1) = l(t)(1−q)(1−w)` and, separately, terminate
everything at `t = n`. Those two do not reconcile in the final policy year: its
survivors neither die nor lapse — their cover simply runs out — so the roll-forward
appears to lose lives with no cause. `pols_maturity(t)` names that quantity, zero in
every year but the last, which makes the identity close exactly:

```
pols_if(t) − pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_maturity(t)
```

This is bookkeeping, not a new assumption — the value is fully determined by the notes'
own rules — and it is *not* a maturity benefit: the amount paid is nil. The name follows
`BasicTerm_S.pols_maturity`, and `Term_US_A` carries the same cells for the same reason.

## Modules that are off in the base run

Four of the notes' optional constructions are implemented and switched off, so the base
run reproduces the worked example while the machinery stays visible and testable.

| Module | Switch | Off value | What it does |
|---|---|---|---|
| Selective lapsation | `sel_lapse_lambda` | `0.0` | Loads persisters' mortality by `1 + λ·max(0, w_cum − w_ref)` once cumulative lapse passes `w_ref = 20%`. Lapsers are healthier, so a block that has shed lives carries impaired mortality on the remainder |
| Rebroking | `premium_market_ratio` | `1.0` | Multiplies the lapse rate by `min(2, max(1, P_inforce/P_market))`. Guaranteed premiums rule out premium-shock lapse; falling market rates for the attained age are the driver instead |
| Commission clawback | `clawback_mths` | `0` | Recovers `(48 − months in force)/48` of initial commission on lapses inside the window. Set it to `48` for the notes' four-year rule; inside the window it reverses the sign of the early-lapse sensitivity |
| Waiver of premium | model point `wop` | `False` (point 7 excepted) | A two-state incidence/recovery chain on the premium-paying population, plus a premium loading. Both its incidence basis and its extra premium are **[std]** placeholders — no public UK incidence basis for the work-tasks definitions appears in the sources |

The waiver module makes two simplifications worth naming: incidence in year `t`
produces waiver from year `t + 1`, which is the annual grid's reading of the 26-week
deferred period [S1] **[std]**; and mortality and lapse are assumed independent of the
waiver state **[std]**, which is what lets the waived population be carried as a
fraction of the in-force rather than as its own decrement.

The indexation option is a model point flag rather than a module switch. Its base run is
deterministic and always accepts, as the notes specify, with a flat 3% RPI scenario
**[std]** — so cover grows at 3% a year and premium at 4.5%, the ×1.5 factor
[S1] [S2] [S6]. One consequence: with acceptance certain, the rule removing the option
after three consecutive declines [S1] [S6] (two at one insurer [S8]) is never reached and
is not implemented. Indexation is restricted to the level shape **[std scope]**, since
no fetched insurer offers indexed decreasing cover.

## Sign convention

The notes' `CF(t)` is already **income positive** — they write "+ = inflow" — which is
the library-wide sign of `net_cf`. So unlike `WholeLife_US_A`, `SPIA_US_S` and
`DIA_US_S`, whose notes print the stream outgo-positive and which therefore publish a
`liability_cf` companion column, there is one stream here under one name.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue:
`pols_*` for policy counts, plural nouns for cash flows, `*_rate` for rates, `*_pp` for
per-policy amounts, `claims(t, kind)` with an uppercase `kind` string, and
`pols_if_at(t, timing)` for the within-year in-force reads. The technical notes use
compact actuarial symbols; the full mapping lives in the `Projection` Space docstring.
Four cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `q(t)` | `mort_rate_life` / `mort_rate` | The notes use one symbol for the per-life table rate and for the decrement applied to the policy, which on a joint first-death policy is `1 − (1−q₁)(1−q₂)` |
| `w(t)` vs `w_cum(t)` | `lapse_rate` / `lapse_cum` | `lapse_cum` is a proportion of the original cohort, not a running total of `lapse_rate`, and the loading it feeds moves *claims* |
| `E0`, `e(t)`, `ec` | `expenses` / `claim_expenses` | The first two are inside `expenses`, the library-wide name; the claim expense stays out because the worked example prints them as separate columns |
| *(no symbol)* | `pols_maturity` | See above |

## Standardizations used

Everything in this list is **[std]**: the whole mortality table and its select factors;
the 75% proxy scaling; the lapse duration table; the premium itself (£12.00 per month);
acquisition expense £150; maintenance £30 inflating at 3%; claim expense £250; initial
commission 150% of annualized premium and renewal 2.5% from year 2; the clawback
formula; the FIB commutation rate of 3%; the decreasing shape's 6% schedule rate, its
`j_m = (1+j)^(1/12) − 1` monthly convention and its mid-year death benefit; the
selective-lapsation and rebroking constructions; the waiver incidence, recovery and
premium loading; the flat 3% RPI scenario; and death-before-lapse as the processing
order.

## Tests

`tests/test_term_assurance_uk.py` asserts the notes' three-row worked example to the
penny and the in-force column to six decimals, the `B(60) = £134,588` decreasing-schedule
anchor and the `j_m` convention behind it, the FIB ledger against an independent rebuild
and against the annuity-certain total, that the FIB stream is not decremented by
mortality, expiry with no tail states, the roll-forward identity, the joint first-death
decrement, indexation's ×1.5 premium factor, the two mortality bases, the four off-by-
default modules in both positions, and that a lapse pays nothing.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #uklib-term_assurance-r10
[R11]: #uklib-term_assurance-r11
[R12]: #uklib-term_assurance-r12
[R8]: #uklib-term_assurance-r8
[R9]: #uklib-term_assurance-r9
[std]: #uklib-std
<!-- END generated citation links -->
