# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/critical_illness/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The benefit
> structure is sourced — the accelerated design, the additional-payment benefit at
> `min(25% of SA, £25,000)` and children's cover at `min(50% of SA, £25,000)`, both
> non-depleting, the 14-day survival period, the absence of any surrender value, the
> 5-yearly review cycle. Every **rate** is a **[std]** standardization: the CMI's
> accelerated-CI diagnosis tables (AC04, the "16" Series) are restricted to subscribers
> [REG-R22] [REG-R26], and the £55 monthly premium is a placeholder — no UK insurer
> publishes CI rate cards. **Profitability conclusions drawn from the worked example are
> meaningless.**

## Run it

```bash
python products/critical_illness/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/critical_illness/CI_UK_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy month `t` with one column per
cash flow line.

## Monthly, on an annual chassis

This product sits on the [term assurance](../term_assurance/model.md) chassis, which is
an **annual** model — but these notes specify a **monthly** grid, so `CI_UK_S` carries
the `_S` tag and `Term_UK_A` the `_A`. Nothing in the contract needs monthiversary
processing; the notes choose monthly for parity with the rest of the library, and it is
what makes the 14-day survival period and the 5-yearly premium reviews expressible.

Policy month `t` runs 1 … `proj_len()` = `12 × term`. The notes index the in-force
probability `l(t)` at the **end** of month `t` with `l(0) = 1`; the library indexes
`pols_if(t)` at the **start**, so:

```
pols_if(t)                 == the notes' l(t−1)
pols_if_at(t, "AFT_DECR")  == the notes' l(t)
```

That is deliberate — `pols_if(t)` is then the weight on the same `result_cf()` row's
cash flows, which is what every model in this library means by the name.

## The combined decrement — why `q_d` and `i_ci` cannot be added

The insured event is *death or first CI diagnosis, whichever comes first*. Adding the
two rates double-counts lives that are both diagnosed and die in the same period: once
the CI claim has been paid, the subsequent death of that life is not a second claim, and
a death inside the survival period converts the CI claim into a death claim of the same
amount rather than adding one. So

```
q_claim(a) = i_ci(a)·(1 + τ)^(y−1) + q_d(a)·(1 − k)          [std]
```

where `k` is the proportion of deaths preceded by a claimable diagnosis. `k = 0.10` flat
is a standardization — the cause-of-claim splits that would calibrate it live in CMI
working papers whose datasets are subscriber-restricted [R8] [R9] — and it is a Reference
rather than a literal because the notes rate it the third-largest lever on the
liability. `k = 0` maximally double-counts; `k = 0.25` may understate.

On the **accelerated** contract nothing further is needed: however the overlap resolves,
`SA` is paid once. The 14-day survival period is cash-flow-neutral there and is not
modelled — applying the slippage `δ` to the accelerated main benefit is one of the notes'
listed pitfalls, because a death inside the period still pays `SA` as a death claim.

On the **standalone** contract death pays nothing and the decrement splits:

```
q_pay(a)  = i_ci(a)·(1 + τ)^(y−1)·(1 − δ)
q_exit(a) = q_d(a)·(1 − k) + i_ci(a)·(1 + τ)^(y−1)·δ
```

Same total, so the in-force run-off is identical; only the *paid* part generates outgo.
Note where `k` goes: onto the non-paying death exit, never onto the paid decrement.
Applying it to `q_pay` is the mirror-image pitfall and understates claims.

### One documented divergence from the notes

The notes convert annual rates to monthly with `1 − (1 − q)^(1/12)` and prescribe
`q_pay_m` for the standalone main benefit — but converting `q_pay` and `q_exit`
independently leaves their sum slightly *below* the `q_m` the same notes use for the
in-force run-off. Adding the annual parts and converting them geometrically cannot both
hold.

`claim_rate_paid_mth` follows the notes literally, and `claim_rate_exit_mth` is defined
as the **residual** `q_m − q_pay_m`, so the split is exact by construction and the
run-off is the notes'. `check_claim_split()` bounds the artefact rather than hiding it:
it asserts the residual really is the independently converted `q_exit` to within
`claim_split_tol` (1e-4). On the shipped standalone point the largest discrepancy across
300 months is about 1e-5 — four decimal places — and it grows with the level of the
rates, which is why the tolerance is a Reference the user can tighten or state.

## The non-terminating benefits

The additional-payment and children's-cover benefits are the notes' third and fourth
pitfalls, and they are one mistake in two directions. Both are:

- **non-depleting** — they do not reduce the sum assured; and
- **non-terminating** — they do not decrement the in-force.

Only the main benefit ends the policy. Modelling them as accelerations of `SA` is a
different product; terminating the policy on one is the same error with the opposite
sign. They are carried as frequency loadings on the in-force and appear in
`pols_if_at()` nowhere at all.

The monthly conversion for these two is `rate / 12`, **not** `1 − (1 − rate)^(1/12)`,
and that is deliberate: these are claim *frequencies* — expected repeatable events per
year — not probabilities of a terminating event, so there is no survival transform to
apply. The notes use the same approximation and say so.

The treatment ignores the contractual claim-count caps (one per additional-payment
condition [S11], two children's claims [S1], and the £50,000 per-child cross-policy
limit) because at the **[std]** frequencies shipped here the probability of reaching a
cap is second order. Respecting them exactly would need claim-count state variables.

## Inputs are external files

The three input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `CI_UK_S/` holds nothing but formulas:

```
products/critical_illness/
  model_point_table.csv        <- inputs live here
  ci_rate_table.csv
  lapse_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  CI_UK_S/                    <- formulas only
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
| `ci_rate_file` | `ci_rate_table()` | `ci_rate_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Seven model points. **Point 1 is the worked-example anchor cell** (M40 / non-smoker / accelerated / 25-year / £100,000 / £55.00 per month); points 2–7 are the standalone variant, the reviewable variant, an indexed policy, one without children's cover, a female smoker on a shorter term, and a joint first-event policy | anchor cell **[std]**, technical notes' worked example |
| `ci_rate_table.csv` | Annual `i_ci` and `q_d` at the **pivot ages 40, 45, 50, 55, 60, 65** by sex and smoker status, with a `provenance` column | the male non-smoker pivots are the notes' **[std]** proxy table verbatim; the other three sex/smoker cells are those pivots times flat factors (i_ci ×1.75 smoker, ×0.95 female; q_d ×2.00 smoker, ×0.70 female) — all **[std]**, and *not* CMI or ONS values |
| `lapse_table.csv` | Annual lapse by policy year, 10 / 8 / 6 / 6 / 6 / 4 % | **[std]** protection-book shape; UK CI lapse studies are proprietary |

### The rate basis is interpolated, not tabulated

`ci_rate_table.csv` holds **six pivot ages**, because that is the form the notes give the
basis in — together with the rule that intermediate ages are interpolated log-linearly.
So `pivot_interp()` does exactly that: geometric in the rate, linear in age,

```
r(x) = r₀ · (r₁/r₀)^((x − x₀)/(x₁ − x₀))
```

which is "log-linear" written without a logarithm. Outside the pivot range it continues
the nearest end segment's gradient — the same expression with the exponent outside
[0, 1] — and that is an **extrapolation**, flagged as one: a 25-year policy issued at 40
stays inside the pivots, but a younger or longer one does not.

Keeping the interpolation in the model rather than pre-expanding the file means swapping
in a licensed AC04 or "16" Series basis replaces a 24-row table, not a generated one.

**The sex and smoker cells are cruder than the pivots.** Real accelerated-CI experience
is not a flat female factor: breast cancer makes female incidence exceed male at the
younger ages. The flat factors shipped here are placeholders like everything else in the
file, and the `provenance` column marks which cells came from the notes.

## The reviewable variant

`premium_guarantee = reviewable` turns on a 5-yearly review from the fifth anniversary
[S3] [S4] — so the first bites in month 61. Premiums are constant between reviews and
multiplied by `1 + ρ_review` at each one; the snapshot is `ρ_review = 0`, so model point
3 runs identically to point 1 until the Reference moves. Two behavioural responses hang
off the same switch, both **[std]**:

| Response | Formula | Why |
|---|---|---|
| Review shock lapse | `min(0.30, w(y) + 2.0·max(0, ρ − 0.05))` for twelve months after a review raising premiums by more than 5% | One insurer's review changes are subject to **no stated limit** [S4], which makes review-driven shocks the dominant behavioural risk on reviewable business |
| Selective lapsation | `i_ci × (1 + η)`, `η = 0.10`, from the first such shock onward | Healthier lives lapse first when premiums rise |

The economics are the point of the variant rather than the cash flows: guaranteed
premiums mean morbidity deterioration and ABI definition drift fall entirely on the
insurer, and the reviewable design transfers that to policyholders at the cost of these
two responses. Do not model reviewable business with the guaranteed-premium constraint.

## What this product does not have

No account value, no asset share, no surrender or paid-up value, no bonus, no market
value reduction — and **no commission line**: the notes fold acquisition cost into the
£200 initial expense rather than carrying commission separately as the term assurance
chassis does. There is likewise no interest-sensitive dynamic lapse; with no cash value
and no credited rate there is nothing to arbitrage, so the machinery the accumulation
products in this library carry is deliberately absent.

`claims(t, "LAPSE")` exists, returns zero, and appears in `result_cf()` as a zero column,
so the absence of a surrender value is stated rather than inferred.

## Sign convention, and the worked example's Net CF column

`net_cf` is **income positive**, the notes' own sign and the library-wide one, so there
is no outgo-positive `liability_cf` companion here.

One caveat for a reader checking the worked example by eye: **the notes' Net CF column
excludes the initial expense.** At month 1 it shows 31.88, with the £200 noted separately
as taking the month to −168.12. `net_cf(1)` is the total, −168.12; the notes' column is
`net_cf(1) + 200`. Both readings are asserted in the tests.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
policy counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth`
for monthly ones, `*_pp` for per-policy amounts, `claims(t, kind)` and
`benefit_pp(t, kind)` with uppercase `kind` strings, `pols_if_at(t, timing)`. The full
symbol mapping lives in the `Projection` Space docstring. Three cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `a(x)` frequency vs `a` attained age | `ap_rate` / `age` | The notes use one letter for both in the same table; nothing here is called `a` |
| `q_d` | `mort_rate` | Kept as the library-wide name even though mortality never decrements on its own here — it enters only through `claim_rate`, net of the overlap |
| `SA` | `sum_assured` / `benefit_pp(t, "MAIN")` | A constant in the notes and a function of `t` here, because the indexation option moves it |

The additional-payment and children's caps are struck against the **indexed** sum assured
**[std]**: the notes state them against `SA` without saying which, and holding them to a
frozen outset value would let the ancillary benefits shrink in real terms while the main
one did not. At the anchor cell the cash cap binds either way.

## Standardizations used

Everything in this list is **[std]**: the whole diagnosis and mortality basis and its
sex/smoker factors; the log-linear interpolation and its extrapolation beyond the
pivots; the overlap factor `k = 0.10`; the survival-period slippage `δ = 0.03`; the CI
trend `τ = 0`; the additional-payment frequency `0.15 × i_ci` and the children's
frequency `0.0004` p.a.; the lapse table; the £55 monthly premium; initial expense £200,
maintenance £30 p.a. inflating at 3%, claim expense £250; the flat 3% RPI scenario and
the indexation caps; the review shock lapse and anti-selection constructions; the
exclusion of the £4,000 child funeral benefit; claim-before-lapse as the processing
order; and treating the joint first-event decrement as `1 − (1−q₁)(1−q₂)`.

Two scope limits are worth stating separately. Decreasing and family-income shapes exist
on the term chassis and are implemented in `Term_UK_A`, but these notes scope them out,
so `cover_basis` accepts `level` only. And a **standalone joint first-event** policy
raises rather than projecting: the notes write the standalone decrement split for one
life, and there is no published basis for splitting a joint first-event decrement into
paying and non-paying parts, so inventing one would be worse than refusing.

## Tests

`tests/test_critical_illness_uk.py` asserts the notes' three-month worked example to the
penny and the in-force column to six decimals, the combined-decrement arithmetic and
both overlap pitfalls, the standalone split and its bounded artefact, that the
non-terminating benefits neither deplete `SA` nor decrement the in-force, the pivot
interpolation against hand-computed values, the reviewable variant in both positions,
indexation, the joint decrement, and that a lapse pays nothing.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R8]: #uklib-critical_illness-r8
[R9]: #uklib-critical_illness-r9
[REG-R22]: #uklib-reg-r22
[REG-R26]: #uklib-reg-r26
[std]: #uklib-std
<!-- END generated citation links -->
