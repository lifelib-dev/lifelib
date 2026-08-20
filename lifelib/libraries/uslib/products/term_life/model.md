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
model = mx.read_model("products/term_life/Term_US_A")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy year `t` with one column per
cash flow line.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## Annual, not monthly

Policy year `t` runs 1 … `proj_len()` = `95 − age_at_entry()`. **Note the contrast with
lifelib's `BasicTerm_S`, where `t` counts months** — here it counts years, because every
decrement in this product is on an annual cycle and there is no account value requiring
monthiversary processing. The technical notes describe an optional monthly mode; it is
not implemented, and the `premium_mode` column in the model point table is currently
inert.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Term_US_A/` holds nothing but formulas:

```
products/term_life/
  model_point_table.csv        <- inputs live here
  premium_rates.csv
  mort_table.csv
  class_factor_table.csv
  shock_lapse_table.csv
  run.py
  README.md
  Term_US_A/                  <- formulas only
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

**The trade-off:** the model is not portable on its own. Copy `Term_US_A/` without the
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

The notes give the roll-forward as `l(t+1) = l(t)(1−q)(1−cv)(1−w)` and, separately, the
rule "l(t) = 0 for x+t−1 ≥ 95". Those two do not reconcile in the final policy year: the
survivors of year 60 do not lapse, die or convert — their coverage simply runs out — so
the roll-forward appears to lose lives with no cause.

`pols_maturity(t)` names that quantity (zero in every year but the last), which makes the
identity close exactly:

```
pols_if(t) − pols_if(t+1) = pols_death(t) + pols_lapse(t) + pols_conv(t) + pols_maturity(t)
```

This is bookkeeping, not a new assumption — the value is fully determined by the notes'
own rules. It surfaced because the test asserting the identity failed at t = 60. The name
follows `BasicTerm_S.pols_maturity`.

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
premium tax 2%; maintenance $30 inflating at 2%; acquisition $300; the mortality
extension beyond age 46; and the interpolated ART premium years. Conversion is switched
**off** by default (`conv_rate_base = 0`) so the base run reproduces the worked example,
which sets it aside to keep one decrement narrative.

## Tests

`tests/test_term_life_us.py` asserts the full 12-row worked example to the cent, the
in-force column to six decimals, the roll-forward identity, expiry behaviour, the M(1)
divergence, the BasicTerm_S name set, that both docstrings survive serialization, that
the model folder contains no data of any kind, that an input can be swapped by
repointing a Reference, and a read → write → re-read round trip carrying the inputs
along.

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
