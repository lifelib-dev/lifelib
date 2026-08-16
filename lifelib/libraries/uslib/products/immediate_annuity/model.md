# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/immediate_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the five payout forms, the two survivor-reduction triggers, the
> fixed compound COLA, the cash-refund and installment-refund definitions, and the 8%-to-0%
> commutation surrender-charge scale — are sourced from the composite's product documents.
> Everything else is a **[std]** standardization introduced for the reference
> implementation. In particular **no insurer publishes payout factors or the pricing
> basis for a fixed SPIA**, so the initial annual income `B(1)` is an exogenous input, not
> a model output, and the $6,000-per-$100,000 level shipped here is a round arithmetic
> anchor that makes the worked example exact — deliberately generous against the
> COLA-adjusted illustrations, which imply nearer 4.5% for this cell. Replace it with a
> real quote, and the mortality tables with company data, before drawing any conclusion
> from the numbers.

## Run it

```bash
python products/immediate_annuity/run.py
python products/immediate_annuity/run.py 8      # the same cell, probability-weighted
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/immediate_annuity/SPIA_US_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy month `t` with one column per
cash flow line; `result_pols()` returns the survival probabilities and payment factors
behind it.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## Monthly, not annual

`t` counts **policy months from the annuity date**, 1-based, running
1 … `proj_len()`. The notes set the grid (`t = 1, 2, …` months from the annuity date) and
the product forces it: instalments fall monthly on the anchor cell, the COLA steps at
month 13, 25, …, and deaths are decremented at end of month, so a survivor reduction that
takes effect "from the instalment due at the end of the month of death" needs a monthly
grid to be expressible at all. The annuity date is collapsed onto the issue date, so
there is no deferral period; any nonzero deferral turns this product into the
deferred-income-annuity chassis.

**Note the contrast with lifelib's `CashValue_SE`, whose months are 0-based.** Here
`t = 0` is not a projected month: it is the base case of each recursion
(`lives_if(0, life) = 1`, `cum_annuity_pp(0) = 0`), matching the notes' own 1-based index.

`proj_len()` runs to the notes' age stop rule on the **youngest** covered life — 696
months on the anchor cell's 65/62 pair — or to the end of the effective certain period if
that is later. Stopping on the primary's age alone would truncate the joint annuitant's
tail; the notes say so explicitly, and a test pins it.

That rule stops the projection *one month before* any life attains ω = 120: `age(t, life)`
advances on policy anniversaries, so at `t = 696` the younger life is 119, and the `q = 1`
row of the mortality table is never reached inside the run. The notes' other stop test —
`IF(t) < 1e-6` — is therefore **not** subsumed by it, contrary to what an earlier draft of
this file and the model's own docstrings claimed: model point 8 ends at
`pols_if(696) = 3.41e-06`, 3.4 times the threshold. The age rule is the one
implemented, because it keeps `proj_len()` independent of the projection it bounds, and
the truncated tail — one further month, after which the attained age is 120, `q = 1` and
every flow is zero — is worth 3.41e-06 of a contract. A test pins the residual so the
claim cannot quietly become false again.

## Inputs are external files

The four input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `SPIA_US_S/` holds nothing but formulas:

```
products/immediate_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  improvement_scale.csv
  surr_charge_table.csv
  run.py
  README.md
  SPIA_US_S/          <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the
model and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which
stores its inputs *inside* the model through modelx's IOSpec machinery — hence no
`_data/` directory and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every contract. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many contracts are projected.

`Data.input_dir()` resolves the location from `_model.path.parent` when the model is
read, so it works wherever the repository is checked out. Each table has a filename
Reference and a reader Cells, both on `Data`:

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `improvement_scale_file` | `improvement_scale()` | `improvement_scale.csv` |
| `surr_charge_file` | `surr_charge_table()` | `surr_charge_table.csv` |

**The trade-off:** the model is not portable on its own. Copy `SPIA_US_S/`
without the CSVs and it will read fine, then fail on first evaluation. What you gain is
that a diff of the model shows logic changes only, and an input can be swapped in place —
point `Data.mort_table_file` at another same-schema file and the projection follows, with
no formula change. That is also how the notes' first sensitivity is run: scale
`improvement_scale.csv` to 50% or 150% of tabulated improvement and re-read.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Fifteen contracts on one anchor configuration, varying only what the worked example varies, plus two that hold open a case the notes under-specify (14: quarterly in advance; 15: `certain_only`). **Point 1 is the worked-example anchor cell** (trig = `either`); point 2 is the same cell on trig = `primary`, which is the table's second CF column | anchor cell **[std]**, technical notes "Worked example" |
| `mort_table.csv` | Base annuitant mortality `q_x` by age (40–120) and sex, with a `provenance` column | **[std]** illustrative Gompertz–Makeham curve — ***not*** the 2012 IAM Basic table, and not any published table |
| `improvement_scale.csv` | Generational improvement rates by age and sex | **[std]** illustrative G2-shaped scale — ***not*** Projection Scale G2 |
| `surr_charge_table.csv` | Commutation surrender charge by contract year, 8% in year 2 to 0% from year 10 | sourced [S1] — the only published SPIA surrender-charge schedule found |

**On the mortality tables.** The technical notes prescribe the **2012 IAM Basic** table
projected with **Projection Scale G2**, applied generationally, with a ×1.084 A/E factor
from the 2020–2024 SOA/LIMRA payout study. The notes also forbid embedding it: "The model
must load them; it cannot hard-code them", and the Basic table is in any case not printed
in any source this library holds — A-821 prints the *loaded* Period Table only. The two
files shipped here are illustrative stand-ins carrying the right shape and the right
schema, marked **[std]** in their `provenance` columns. Swap in a licensed basis by
replacing the files. Keep the two objects separate: the loaded Period Table is a
valuation object and the Basic table a best-estimate one, and they must not be
interchanged.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those
models have an analogue: `pols_*` for contract counts, plural nouns for cash flows,
`*_rate` for rates, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase
`kind`, `result_cf()`, plus `model_point`, `age_at_entry`, `sex`, `age`, `duration`,
`duration_mth`, `policy_year`, `proj_len`, `mort_rate`, `mort_rate_mth`, `expenses`,
`inflation_rate`, `surr_charge`, `surr_charge_rate` and `net_cf`. A test asserts that
shared set is present, so the models cannot drift apart silently.

Four names are the library-wide spelling rather than this product's own shorthand, so that
the twelve reference models can be read against each other:

- `mort_ae_factor` is the mortality A/E deviation factor — the notes' `AE`, 1.084 **[std]**.
- `omega_age` is the limiting age ω = 120.
- `check_lives_roll_fwd()` and `check_payment_factor()` take **no argument and return a
  bool** covering every projected month, which is what lets one test call the same check
  across every model. The signed per-month residual — the more useful object once a check
  fails — is `check_lives_roll_fwd_resid(t)` and `check_payment_factor_resid(t)`, and each
  bool is implemented in terms of its own residual.
- `net_cf` is income-positive in every model in the library, so `liability_cf` carries the
  notes' outgo-positive `CF(t)` verbatim and both are published as columns of
  `result_cf()` (below).

The technical notes use compact actuarial symbols instead; the full mapping lives in the
`Projection` Space docstring. Five cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l(t)` survival vs `L(t)` payment factor | `lives_if` / `payment_factor_life` | The notes' two symbols differ only by case |
| `G(t)` cumulative instalments vs `G2_x` | `cum_annuity_pp` / `improvement_rate` | Same letter, unrelated quantities |
| `θ` substandard vs `θ_cum` commutation | `rating_factor` / `commute_frac_cum` | Same letter, unrelated quantities |
| `d_term(t)` | `lives_death_last` | Not a separate quantity — see below |
| `CF(t)` | `liability_cf` / `annuity_payments` | The worked example's "CF" column is not the notes' `CF(t)` — see below |

`d_term(t)` is defined in the notes as `d₁` on a single-life contract and `d_last` on a
joint one. Because `lives_if_last(t)` returns `l₁` when the contract is single-life, the
two collapse: `lives_death_last` *is* `d_term` in both cases, and no second cells is
needed.

## The worked example is a scenario, not a table run — so the model ships both

The notes' verification anchor is not a probability-weighted projection. It is a
**scenario**: "the joint (secondary) annuitant dies during month 14; the primary survives
throughout", evaluated at `l₁ = 1`, `l₂ = 0`. But the same notes say model points are
"projected on an expected (probability-weighted) basis". Both readings are shipped, and
which one applies is a model point column, `mort_basis`:

- `mort_basis = "table"` runs the notes' generational recursion off `mort_table.csv` and
  `improvement_scale.csv`. Model points 7, 8, 9, 12 and 15.
- `mort_basis = "scenario"` **[std]** replaces `lives_if(t, life)` with the deterministic
  step function `1{t < death_mth(life)}`, a blank `death_mth` meaning the life survives
  the whole projection. Model points 1–6, 10, 11, 13 and 14 — the worked example's runs.

The scenario switch is a **[std]** modelling device, not a product feature. It exists
because retuning assumptions until a probability-weighted run happened to land on
500.00 / 515.00 / 343.33 would be dishonest, and because the notes' trace is only
meaningful as a scenario: it is checking the *payment factor algebra*, not the mortality
basis. Model point 8 is the anchor cell on the table basis and is what a reader should
look at for a realistic cash flow shape.

## The worked example's "CF" column is not the notes' `CF(t)`

The notes define `CF(t) = E[ANN(t)] + E[CR(t)] + E[COMM(t)] + E[EXP(t)]` and, separately,
a maintenance expense of $60 p.a. paid monthly. But the worked-example table's "CF" column
reads **500.00** at `t = 1`, not the **505.00** that definition gives once the $5.00
monthly expense is added. The column is the annuity instalment alone.

This is not resolvable from the notes, so the model names both and the tests assert both.
`annuity_payments(t)` is `E[ANN(t)]` and is what the worked-example rows are asserted
against; `liability_cf(t)` is the notes' `CF(t)`, outgo positive, and is asserted at
505.00. `net_cf(t) = −liability_cf(t)` keeps `Term_US_A`'s sign convention (income less
outgo) so the two models' cash flow statements read the same way, even though this product
has no projected income at all. **Both are columns of `result_cf()`** — the notes' stream
survives verbatim under the name the notes give it, and the library-wide income-positive
convention is available under the name every other model uses, so neither has to stand
for the other.

## `max(C, L)` — the certain period is a floor, not a second stream

`payment_factor(t) = max(certain_floor(t), payment_factor_life(t))` is the single most
important line in the model, and the notes' first-listed pitfall:

> During the certain period the instalment is certain — do not also weight it by survival.
> `max(C, L)` prevents paying `1 + L`; an additive construction silently doubles the
> guarantee.

Two consequences fall out for free, with no extra flag:

- Because the floor pays the **full, unreduced** instalment, a survivor reduction inside a
  certain period is automatically deferred to the end of that period — NYL's published
  rule [S5]. Model point 5 kills the joint annuitant in month 14 under a 10-year certain
  period and pays the full instalment until `t = 120`, dropping to δ only at `t = 121`.
- A commutation reduces certain-period instalments only, because `θ_cum` is multiplied by
  `C(t)`: at `t = 121` the life-contingent tail is paid in full. Applying `θ_cum` to that
  tail contradicts every retrieved contract, and model point 9 pins it.

Model point 13 is the harder case: **both** annuitants die inside the certain period, so
`L = 0` while `C = 1`. The full instalment continues, `pols_if` stays at 1 because a
payment obligation is still open, and everything — annuity, expense, in-force — goes to
zero together at `t = 121`.

## `certain_only` — where the notes' expense formula outlives the contract

The notes carry the maintenance expense on `IF(t) = max(C(t), l_alive(t))` and, in the
same assumption table, describe it as "$60 per contract p.a., paid monthly **while any
payment obligation remains**". On the four life-contingent forms the formula and the
prose say the same thing. On `certain_only` they do not, because the notes also set
`L(t) ≡ 0` there: the last instalment falls at `n_eff` and nothing whatever is owed
afterwards, but `l_alive` is a *survival probability*, not a payment factor, and stays
positive for the annuitant's whole remaining lifetime.

Taken literally the formula keeps billing a contract that ended years earlier. On model
point 15 — `certain_only`, 10-year certain, single male 65, table basis — that is
**1,539.83 of expense spread over the 540 months after the last payment**, still charging
5.63 in month 240 against a `pols_if` of 0.7046 on a contract whose final instalment was
paid ten policy years before.

`pols_if` follows the prose: the life-contingent leg is dropped on `certain_only`, the one
form that carries no life contingency at all, so `IF(t) = C(t)` there and
`IF(t) = max(C(t), l_alive(t))` on every other form. Nothing on any other form or model
point moves — no shipped point used `certain_only` before, which is exactly why the notes'
internal inconsistency went unnoticed. Model point 15 exists to hold the case open, and a
test asserts `pols_if(121) = 0` and zero expense from `t = 121` on.

## Two timing conventions, each worth one instalment

The notes flag both as pitfalls, and they are wired to the same model point switch,
`timing`:

- **Survival measurement.** An arrears instalment falling at the end of month `t` requires
  survival to the end of month `t`; an advance instalment falls at the *start* of month
  `t`, which is the end of month `t − 1`, so survival is measured at `t − 1` — at every
  frequency. Using end-of-period survival for advance payments understates the liability
  by about one period's mortality per payment. Model points 6 (arrears) and 10 (advance)
  are the same single life dying in month 14: the arrears run stops paying at `t = 14`,
  the advance run at `t = 15`.

  The notes write that advance point as `t − 12/m`, "one full payment period earlier".
  That is measured from the **arrears** month of the same instalment, which falls one
  payment period *later* than the advance month; `is_payment_mth` indexes an advance
  instalment by the month it actually falls in (`t = 1, 4, 7, …` at `m = 4`), so the two
  readings coincide only at `m = 12` — the only frequency the notes spell out, and the
  only one every other shipped model point uses. Taking `t − 12/m` literally at `m = 4`
  reads survival three months too early and pays the quarterly instalment due at the
  start of month 4 to a life the projection has already killed off in month 3. Model
  point 14 is that contract: quarterly in advance, single male 65, dying in month 3. It
  pays $1,500.00 in the first year, not $3,000.00, and a test asserts both the payment
  months `1, 4, 7, 10, 13` and the survival months `t − 1` behind them.
- **Refund balance.** The cash refund nets instalments *already paid*: `G(t−1)` on arrears,
  but `G(t)` in an advance payment month, because an instalment paid at the start of the
  month of death has been paid. Model point 6 pays $93,485.00 and model point 11 pays
  $92,970.00 — exactly one instalment apart, and using `G(t−1)` on advance would overstate
  the liability by that instalment.

## `n_R` is derived, never hard-coded

The installment-refund certain period is `n_R = min{t ∈ T : G(t) ≥ P}` — payments continue
until cumulative payments equal the premium, which is NYL's `premium ÷ annualized income`
rule rounded up to a payment date [S5]. On the anchor it lands on the notes' 200 months,
and the temptation is to write 200 down. `certain_mths_refund()` searches the schedule
instead, so it moves with `B(1)`: model point 12 is the same contract at $4,800 of annual
income and returns 250 months. The notes' "hard-coding it breaks every sensitivity run on
`B(1)`" is a test.

The final-instalment trim the notes prescribe — `P − G(n_R − 12/m)` **[std]** — is
implemented literally, and is a no-op wherever `P` is an exact multiple of the instalment,
which is the shipped case. One caveat the notes do not address: strictly the trim belongs
to the payment made *under the guarantee*, not to one made because the annuitant is alive.
The flat trim is what the notes specify and what is implemented.

## Standardizations used

Everything in this list is **[std]**: the monthly grid and the arrears default; the
`mort_basis` scenario switch; the shipped mortality table and improvement scale (neither
is a published table); the A/E factor of 1.084 on the *projected* basis; the monthly
mortality conversion `q_m = 1 − (1 − q)^(1/12)`; joint-life independence in
`l_last = l₁ + l₂ − l₁l₂`; the limiting age ω = 120 on the best-estimate side; the initial
income level `B(1) = $6,000`; premium tax τ = 0; maintenance expense $60 p.a. inflating at
2.5% and carried by `IF(t) = max(C, l_alive)`, with the `l_alive` leg dropped on
`certain_only` so the expense ends with the contract (above); the
anniversary-of-annuity-date COLA rule
(NYL's "one year after the first income payment" alternative is *not* implemented); the
installment-refund trim; and the whole commutation basis — the 4.00% base discount rate,
the compound convention and the flat `cmt10_shift` are **[std]** *and* **[unverified]**,
since no fixed SPIA issuer publishes a commutation discount formula.

Commutation utilization is switched **off** by default (`commute_util_base = 0`) so the
payment engine is exercised in isolation, which is what the notes' base run specifies. Two
warnings travel with it: any run with `commutation_enabled` inherits an unsupported
discount assumption, and a `u(y)` vector fed into a reserve calculation is **not** a
conservative approximation of CARVM — commutation is an elective benefit under AG 33,
whose incidence rates must be maximised over rather than assumed [REG-R151].

**Not implemented**, and named in the model docstring for the same reason: the
qualified-money overlay (the `qualified` column is inert); the rate-driven dynamic take-up
`u(y, t)`; a 10-year CMT path; the ALB/ANB conversion; the exclusion-ratio tax split,
which is a policyholder computation generating no insurer cash flow; and every valuation
layer — CARVM, VM-22 CTE70, and the 2012 IAR valuation table with its
no-compound-rounding rule.

## Tests

`tests/test_immediate_annuity_us.py` asserts every row and column of the worked-example
table to the cent on both trigger columns, the income levels behind it, and each of the
notes' five traces: the trigger split at `t = 14` with `L = 0.6667` against `L = 1`, the
reversed death on which the two triggers coincide at 343.33, the COLA continuing after the
reduction, the 10-year certain period deferring the reduction to `t = 121`, the
$93,485.00 cash refund, and the 200-month derived refund period. It then works through the
notes' "Known modeling pitfalls" list one test at a time — certain-period double counting,
the A/E factor on the wrong base, period versus generational, survival-measurement timing
at `m = 12` **and** at `m = 4` in advance, refund-balance timing, a hard-coded `n_R`,
joint-life independence, commutation applied to the wrong slice, and exclusion-ratio tax
modelled as a cash flow — plus the product invariants: no lapse decrement, no premium
income, no discounting, the stop rule on the younger life and the residual `IF` it leaves,
the `certain_only` expense stopping with the last payment, the in-force roll-forward,
`result_cf()` shape, and that every model point projects.

The roll-forward test is not the usual tautology. `check_lives_roll_fwd_resid` rebuilds
each life's survival from the monthly rates rather than telescoping `lives_death` — which
is *defined* as `l(t−1) − l(t)` and so closes for any `lives_if` whatever — and one test
proves the difference by replacing `lives_if` with a misindexed recursion in a throwaway
model instance and asserting the residual moves off zero and the no-argument
`check_lives_roll_fwd()` goes `False` with it.

```bash
python -m pytest tests/test_immediate_annuity_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_immediate_annuity_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_immediate_annuity_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[REG-R151]: #uslib-reg-r151
[S1]: #uslib-immediate_annuity-s1
[S5]: #uslib-immediate_annuity-s5
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
