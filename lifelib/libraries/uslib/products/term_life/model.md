# Implementation Notes

**Status:** Draft, 2026-08-06. Built from
[`products/term_life/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the guaranteed premium schedule, the policy fee, expiry at
> attained age 95 — are sourced from a specimen policy. Every behavioural and expense
> assumption is a **[std]** standardization introduced for the reference implementation,
> because no public source carries it. Replace them with company data before drawing
> any conclusion from the numbers.

## Run it

```bash
python products/term_life/run.py
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/term_life/Term_US_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by the 0-based period `t` — one row per
**policy month**, `t = 0 … proj_len() − 1` — with one column per cash flow line, and
`result_cf_annual()` sums the same frame into policy years.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## Monthly, 0-based, as in lifelib

The time index `t` is 0-based and counts **policy months**, the clock
`basiclife/BasicTerm_S` runs on: `t = 0` is the issue month, period `t` runs from time `t`
to time `t + 1`, and the frame is `t = 0 … proj_len() − 1` with
`proj_len() = 12 × (95 − age_at_entry())` the number of policy months projected (720 rows
for the anchor cell, issue age 35). So `pols_if(0) == pols_if_init()`, the acquisition
expense and the first premium fall at `t = 0`, the shock lapse at `t = 12 × policy_term() − 1`,
and the first ART premium at `t = 12 × policy_term()`.

Everything *contractual* about the product is nevertheless annual, so the policy year is
derived and used as a lookup key: `duration(t) = t // 12` is the completed policy years,
`policy_year(t) = duration(t) + 1` the contractual 1-based label, and
`age(t) = age_at_entry() + duration(t)` — age changes on the anniversary, not the birthday.
Every model point in the table is new business (`duration_inforce = 0`), so `t` counts
from inception and from the projection start alike.

### Two speeds, and why the grids reconcile

Every assumption this product has is published annually — the mortality table by age, the
lapse vector by policy year, the conversion rate per year — so the model keeps them at
that speed and derives what it applies: `mort_rate(t)` and `lapse_rate(t)` are the
**annual** rates of the policy year containing month `t`, and `mort_rate_mth(t)` and
`lapse_rate_mth(t)` are `1 − (1 − q)^(1/12)`. That naming is the library's convention and
`tests/test_model_conventions.py` asserts it.

The shock lapse is the one exception the notes make explicitly, and the model follows it:
it is **not spread**. The final level-period policy year's annual rate *is* the shock, so
`lapse_rate_mth` returns zero in eleven of that year's months and the shock in full at
`t = 12n − 1`, immediately before the first ART premium falls due.

Between them those two rules make the grids reconcile exactly where they should: because
the ordinary rates compound back to the annual ones and the shock sits on a year boundary,
`pols_if(12k)` here equals the annual-step model's `pols_if(k)`, to floating point. A test
asserts it at every anniversary of the frame. Nothing else agrees — claims now fall at the
end of the month of death, maintenance expense accrues monthly at `1.02^(t/12)`, and a
modal premium is collected when it is contractually due — and nothing else should:

| Policy year 11 (the first ART year) | Annual grid | Monthly grid |
|---|---|---|
| In force at the start | 0.129955 | 0.129955 |
| Premium | 99.29 | 99.29 |
| Death claims | 81.87 | 69.90 |
| Maintenance expense | 4.75 | 4.08 |

Premium, commission and premium tax are identical because an annual-mode premium is
collected on the anniversary and weighted by the anniversary in force under either grid.
Claims and expenses are lower on the monthly grid because a block losing 30% of its lives
over the year is exposed for less of it than an anniversary weighting assumes. That gap is
the reason the model was converted.

### Premium mode

`premium_mode` in the model point table is no longer inert. `premium_pp_ann(t)` is the
notes' `AP` — the annualized guaranteed premium of the policy year — and `premium_pp(t)`
is the instalment actually collected in month `t`: `modal_factor() × AP` in a payment
month, zero otherwise, on the specimen's own scale of A 1.0 / SA 0.52 / Q 0.27 / M 0.08333
[S6], with the modal load inside the factor. Three quantities deliberately stay on `AP` so
that they do not move with the mode: the jump ratio (the shock buckets are calibrated on
annualized premiums) and the conversion credit (contractually one annual premium). The
acquisition expense does not move with the mode either, but for a different reason — it is
a flat $300 per policy, not a fraction of premium. Commission and premium tax *are* charged
on the instalment, so a modal payer pays them in instalments too. Both shipped model points
are annual mode, which is the anchor cell's mode.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Term_US_S/` holds nothing but formulas:

```
products/term_life/
  model_point_table.csv        <- inputs live here
  premium_rates.csv
  mort_table.csv
  class_factor_table.csv
  shock_lapse_table.csv
  run.py
  README.md
  Term_US_S/                  <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the
model and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which
stores its inputs *inside* the model through modelx's IOSpec machinery — hence no
`_data/` directory and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every policy. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many policies are projected, and `Projection[1].data is Projection[2].data`. A test
counts the reads.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is
read, so it works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `premium_rates_file` | `premium_rates()` | `premium_rates.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `class_factor_file` | `class_factor_table()` | `class_factor_table.csv` |
| `shock_lapse_file` | `shock_lapse_table()` | `shock_lapse_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `Term_US_S/` without the
CSVs and it will read fine, then fail on first evaluation. What you gain is that a diff
of the model shows logic changes only, and an input can be edited or swapped in place —
point `Data.mort_table_file` at another same-schema file and the projection follows,
with no formula change. Tests cover both halves of that bargain.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Two model points, both on the anchor configuration. **Point 1 is the worked-example anchor cell** (M35 / StdNT / $100k / T10 / annual); point 2 is identical but leaves the M(1) override blank, exercising the formula path | anchor cell from the specimen [S6] |
| `premium_rates.csv` | Guaranteed premium schedule by policy year, with a `provenance` column marking each row. **Covers the anchor configuration T10 / M / StdNT / band 1 only** — a model point on any other plan, sex, class or band needs this table extended first, and a test enforces that every model point is projectable | sourced anchors [S6]; intermediate ART years geometrically interpolated **[std]** |
| `mort_table.csv` | Base mortality by age, with a `provenance` column | ages 35–46 are the worked example's illustrative vector; ages 47+ are a geometric extension **[std]**, *not* a published table |
| `class_factor_table.csv` | Rate-class factors 0.80 / 0.90 / 1.00 / 1.75 | **[std]**, technical notes footnote A |
| `shock_lapse_table.csv` | Shock lapse by jump-ratio bucket | **[std]**, technical notes |

### Time-like columns in the CSVs

None of the input files is keyed by the model's `t`, and the move to a monthly frame
re-keyed none of them: the inputs are annual because the *contract* is annual, and it is
the model that derives the policy year from `t` rather than the tables that follow it.

| File | Column | Decision |
|---|---|---|
| `premium_rates.csv` | `policy_year` (1 … 60) | A contractual, 1-based label — the specimen schedule is printed by policy year — left as is. `premium_pp_ann(t)` looks it up at `policy_year(t) = duration(t) + 1`; `jump_ratio()` reads rows `policy_term()` and `policy_term() + 1` through `premium_pp_ann(12n − 1)` and `premium_pp_ann(12n)`. |
| `mort_table.csv` | `age` (35 … 94) | Attained age, read at `age(t) = age_at_entry() + duration(t)`; unchanged. Age 94 is the last row and `age(proj_len() − 1) = 94` for issue age 35, so the frame must end at `proj_len() − 1`. |
| `model_point_table.csv` | `duration_inforce` (0, 0) | An elapsed count in policy years, 0-based by nature (0 = new business); unchanged. No formula reads it today. |
| `model_point_table.csv` | `premium_mode` (A, A) | The contractual billing mode. Read by `modal_factor()` and `prem_due(t)` — see *Premium mode* above; it was inert on the annual grid. |
| `class_factor_table.csv`, `shock_lapse_table.csv` | — | No time-like column. |

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue:
`pols_*` for policy counts, plural nouns for cash flows, `*_rate` for rates, `*_pp` for
per-policy amounts, plus `model_point`, `age_at_entry`, `sum_assured`, `policy_term`,
`proj_len`, `age`, `net_cf` and `result_cf`. A test asserts that shared set is present,
so the two models cannot drift apart silently.

The technical notes use compact actuarial symbols instead; the full mapping lives in the
`Projection` Space docstring. Three cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `d(t)` deaths | `pols_death` | `d` is *also* the PLT duration index in `M(d)` |
| `x(t)` lapses vs `X(t)` premium tax | `pols_lapse` / `premium_taxes` | The notes' two symbols differ only by case |
| *(no symbol)* | `pols_maturity` | See below |

## `pols_maturity` — the one cells the notes do not define

The notes give the roll-forward as `l(t+1) = l(t)(1−q_m)(1−cv_m)(1−w_m)` and, separately,
the rule "l(t) = 0 for x + dur(t) ≥ 95". Those two do not reconcile in the final period of
the frame, `t = proj_len() − 1` (t = 719, the last month of policy year 60, for the anchor
cell): its survivors do not lapse, die or convert — their coverage simply runs out — so the
roll-forward appears to lose lives with no cause.

`pols_maturity(t)` names that quantity (zero in every period but the last), which makes the
identity close exactly:

```
pols_if(t) − pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_conv(t) + pols_maturity(t)
```

This is bookkeeping, not a new assumption — the value is fully determined by the notes'
own rules. It surfaced because the test asserting the identity failed in the last period.
The name follows `BasicTerm_S.pols_maturity`.

## The M(1) divergence is shipped, not resolved

The notes give the rule `M(1) = min(8.0, 1 + 0.55·(J−1))`, which for the anchor cell's
`jump_ratio = 5.4571` returns **3.4514** — but the worked-example table is computed with
**3.50**. The notes acknowledge this ("M(1) = 3.45 ≈ 3.50 (the worked example uses 3.50)").

Rather than pick one, the model ships both. `plt_mort_factor_init_formula()` computes the
rule; the model point carries a `plt_mort_factor_override` column, set to 3.50 on point 1
only, and `plt_mort_factor_init()` uses the override when present and the formula
otherwise. Point 2 is identical to point 1 except that it leaves the override blank, so
the divergence is exercised by a test rather than buried. Neither value is "right" — the
rule is a standardization and so is the pin.

## Standardizations used

Everything in this list is **[std]**: rate-class factors; the level-period lapse vector
(6%, 5%, 4%, 6% anticipatory) and the PLT run-off (30%, 15%, 10%); the shock-lapse
buckets; the M(1)/M(d) deterioration rule and the 3.50 pin; commission 80% / 5% / 2%;
premium tax 2%; maintenance $30 a year accruing at a twelfth a month and inflating at
`1.02^(t/12)`; acquisition $300; the mortality extension beyond age 46; the interpolated
ART premium years; and the constant-force conversion of every annual rate to its monthly
counterpart, with the shock lapse exempted from it. Conversion is switched
**off** by default (`conv_rate_base = 0`) so the base run reproduces the worked example,
which sets it aside to keep one decrement narrative.

## Tests

`tests/test_term_life_us.py` asserts both tables of the worked example — the twelve months
of policy year 1 (rows `t = 0 … 11`) and the policy-year aggregation of years 1–12 — to the
cent, the in-force column to six decimals, the roll-forward identity over
`range(proj_len())`, the annual-equivalence invariant (`pols_if(12k)` against the annual
recursion at every anniversary of the frame), that the shock falls in one month and the
other eleven carry no ordinary lapse, that the monthly rates compound back to the annual
ones, expiry behaviour (`age(719) == 94`, `pols_if(720) == 0`, the frame is
`range(proj_len())` with `proj_len()` rows), that `policy_year(t) = duration(t) + 1` is the
premium schedule's key, the modal-factor machinery, the M(1) divergence, the BasicTerm_S
name set, that both docstrings survive serialization, that the model folder contains no
data of any kind, that an input can be swapped by repointing a Reference, and a
read → write → re-read round trip carrying the inputs along.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_term_life_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_term_life_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[std]: #uslib-std
<!-- END generated citation links -->
