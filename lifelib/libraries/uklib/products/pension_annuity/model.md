# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/pension_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the instalment formula, the four escalation bases
> and the RPI catch-up ratchet, the dependant's percentage and overlap rule, the
> guarantee period as an annuity-certain floor, value protection and its exclusivity
> with the guarantee, the `v + δ ≤ 1` bound, the absence of any surrender value. Every
> **rate** is a **[std]** standardization: the SAPS S3/S4 and PMA16/PFA16 annuitant
> tables are restricted to CMI Authorised Users [R10] [R11] [REG-R22] [REG-R27] and the CMI
> projections model software with them, so the mortality basis here is an ONS-shaped
> population proxy with a flat adjustment and a deterministic improvement scale. No
> insurer publishes an annuity rate card, so the starting income is a model point input.

## Run it

```bash
python products/pension_annuity/run.py         # the worked-example scenario
python products/pension_annuity/run.py 2       # the same contract, expected basis
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/pension_annuity/PA_UK_S")
model.Projection[1].result_cf()
```

## Mortality is the model

After outset the contract has **no premiums, no surrender value, no account value and no
policyholder options at all** [S1 p4] [S2 §1.1, §12] [S5 cl.14.7]. The only decrements are
deaths; the only stochastic drivers are longevity and, on the indexed options, inflation.

That is not an omission — it is the design property that makes the liability eligible for
the Solvency UK **matching adjustment**, whose conditions effectively require this shape
[R1]. The model therefore has **no `lapse_rate` of any kind**, and no dynamic behaviour
formulas. Behaviour enters only at outset, outside the projection, as basis-selection
effects: voluntary annuitants self-select for longevity since the 2015 pension freedoms
[R6], which is the *direction* of the `annuitant_adj` factor being below 1, and
whole-market enhanced quoting [R5] leaves standard-terms lives healthier on average,
which is carried through `rating_factor()` rather than through any dynamic.

## Shared chassis with `SPIA_US_S`, and where the two part

The U.S. counterpart is [`SPIA_US_S`](../../../uslib/products/immediate_annuity/model.md),
and the payout chassis is deliberately the same: a life-contingent instalment stream, a
certain-period **floor** rather than a second stream, a refund-style death benefit
measured against instalments already paid, and survival measured at the *payment point*
rather than at the end of the month. Shared names carry shared meanings — `lives_if`,
`lives_death`, `certain_floor`, `payment_factor`, `payment_surv_mth`, `cum_annuity_pp`,
`annuity_pp`, `annuity_payments`, `pols_if`, `liability_cf`.

Where they part is the UK-specific machinery:

| | `SPIA_US_S` | `PA_UK_S` |
|---|---|---|
| Second life | joint annuitant with a survivor percentage on either of two reduction triggers | **dependant's stream** at δ, gated by an **overlap** rule against the guarantee |
| Escalation | fixed compound COLA | **four bases**, including LPI capped at 5% and a path-dependent **RPI catch-up ratchet** |
| Refund | cash refund and installment refund forms | **value protection**, on a first-death or last-survivor basis, XOR the guarantee |
| Owner options | a certain-portion **commutation** right with surrender charges | **none** — no surrender value at any time |

## Two mortality bases: table and scenario

The notes' worked example is a **scenario** — "the annuitant dies in month 17; the
dependant survives throughout" — while the rest of the notes projects on an expected
basis. Both readings ship, as a model point column, which is the same device `SPIA_US_S`
uses for the same reason:

| `mort_basis` | `lives_if` | Model points |
|---|---|---|
| `table` | the generational recursion off the shipped table and improvement scale | 2, 5, 6, 7, 8 |
| `scenario` **[std]** | the step function `1{t < death_mth(life)}`, blank meaning the life survives | 1, 3, 4, 9, 10 |

Point 2 is the worked configuration on the `table` basis and is the run to read for a
realistic cash flow shape; point 1 is the same contract as a scenario and reproduces the
notes row by row. The switch is a **[std]** modelling device, not a product feature: it
exists because the verification anchor is a scenario, and retuning assumptions to force a
probability-weighted run onto it would be dishonest.

## The guarantee is a floor, not a second stream

```
payment_factor(t) = max(certain_floor(t), payment_factor_life(t))
```

is the notes' first-listed pitfall written as one line. During the guarantee period the
full instalment is payable regardless of survival, escalating as if the annuitant were
alive [S2 §§6.5–6.6] [S7 §4.2]; an additive construction would pay `1 + l_a` and silently
double the guarantee. `check_payment_factor()` asserts it every month.

The guarantee and value protection **never coexist** in the representative design
[S2 §§6.7, 7.6] — `check_guarantee_xor()` asserts no model point carries both. An engine
supporting the combinable variant would have to net guarantee payments off the
value-protection balance [S7 §4.3], or the death benefit is paid twice.

## The overlap gate

`overlap = False` is the representative default and means the dependant's stream starts
only at the **end of the guarantee period**, not at the annuitant's death
[S2 §§5.9–5.11]. Applying δ from the death date silently converts every without-overlap
policy into the more expensive with-overlap form.

Model points 3 and 4 are the same 10-year-guarantee contract on either side of that
switch, and the difference is exactly the dependant's stream from month 18 to month 120 —
about £27,600 of total outgo on the shipped scenario. `overlap_gate(t)` is spelled that
way, rather than as a rate, so that nothing in the model reads as a decrement that is not
one.

## Escalation, and the one path-dependent option

| Basis | Rule |
|---|---|
| `level` | `A(y) = A(1)` |
| `fixed` | `A(y) = A(y−1)(1 + g)`, `g ≤ 10%` [S2 §3.2] |
| `lpi5` | `A(y) = A(y−1)(1 + min(5%, max(0, RPI)))` |
| `rpi_catchup` | income indexed to the **running peak** of the RPI reference index [S2 defs] |

The catch-up is a **ratchet**: a fall in the index freezes income rather than reducing
it, and later rises bite only once the index passes its previous peak. `rpi_peak(k)`
carries that state across anniversaries. Resetting it each year turns the catch-up into a
plain zero floor and overstates indexed income after a deflation-recovery path.

Under the deterministic 3% RPI assumption **[std]** the index is monotone, so the ratchet
never binds and `rpi_catchup` degenerates to fixed 3% — model points 6 and 2 agree by
construction, and `lpi5` at 3% agrees with them too. **That is not an accident to be
tidied away.** The zero floor, the ratchet and the LPI cap are all **inflation options**,
and a deterministic path values them at intrinsic only: the floor and ratchet never bind
and the cap never pays off. A market-consistent value needs stochastic inflation, and the
tests assert the degeneracy so that the limitation is visible rather than implied.

Escalation applies on the **anniversary**, not on payment dates: the year-2 rate does not
reach the `t = 12` arrears instalment, which accrued in year 1 [S2 §3.3].

## Value protection, and where the balance is measured

`VP(t) = d(t) × max(0, v·P − G(t−1))` — the death benefit measured against instalments
**already paid** [S1 p11] [S2 §7]. Two timing rules matter and both are the notes'
pitfalls:

- on **arrears** timing the balance is `G(t−1)`, because the instalment due at the end of
  the death month is never paid;
- on **advance** timing an instalment paid at the *start* of the death month **has** been
  paid, so in an advance payment month the balance is `G(t)` — netting it, or the lump sum
  is overstated by one instalment.

### `G(t)` means two things in the notes, so it takes a `kind`

The notes' *state variable* table defines `G(t)` as cumulative gross instalments
**scheduled**, which is what the worked example's G column prints. The value-protection
section says it accumulates instalments "while the annuitant is alive" on the first-death
basis and "the dependant's instalments too" on the last-survivor one. Those are different
objects whenever the dependant's stream is running, so:

| `cum_annuity_pp(t, kind)` | What it accumulates | Used by |
|---|---|---|
| `"ANNUITANT"` | the **deterministic as-if-alive** annuitant schedule — which needs no path simulation precisely because it ignores survival | the `first_death` VP balance |
| `"ALL"` | the same plus the expected dependant instalments | the notes' printed G column, and the `last_survivor` VP balance |

On a probability-weighted run the `"ALL"` figure is an *expected* cumulative payment
rather than a path-specific one, so the last-survivor balance is an approximation. That is
stated rather than hidden: it is exact in a scenario run, which is the basis the shipped
`last_survivor` model point (10) uses.

The contractual bound `v + δ ≤ 1` on the first-death basis [S2 §7.3] is asserted by
`check_vp_bound()`; the worked configuration sits **exactly** on it, at 50% + 50%.

## The proportionate final payment

Arrears contracts may elect a proportionate final payment for the accrued part-period
[S2 §4]; the representative default does not, and nothing is paid for the final partial
period. With it,

```
PROP(t) = d_a(t) × (h(t) + 0.5)/(12/m) × inst(next(t))     [std half-month accrual]
```

On the worked configuration a death in month 17 with quarterly arrears payments at months
3, 6, … gives `h = 1` — one complete month since the month-15 instalment — and a stub of
`(1 + 0.5)/3 × 1,390.50 = 695.25`, which is the notes' own figure. Model point 9 is the
worked configuration with the option elected, and reproduces it.

## Inputs are external files

Only **two** CSVs, because this product has almost nothing to parameterize: no lapse
table, no charge scale, no bonus rates, no surrender-value schedule. They live **in this
directory**, beside `run.py` — not inside the model folder:

```
products/pension_annuity/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  PA_UK_S/                    <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file
is read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Ten model points. **Point 1 is the worked configuration as a scenario** (£100,000, M65 with F62 dependant at 50%, quarterly arrears, fixed 3%, VP 50% first-death, no guarantee, `A(1) = £5,400`, annuitant dies month 17); point 2 is the same on the expected basis; 3 and 4 are a 10-year guarantee without and with overlap; 5 is single-life level monthly in advance; 6 and 7 are the RPI-catch-up and LPI bases; 8 is an enhanced life at θ = 1.35; 9 elects the proportionate final payment; 10 puts value protection on the last-survivor basis | anchor **[std]**, technical notes' worked example |
| `mort_table.csv` | Base annual mortality by sex and age 50–115, capped at 1, with a `provenance` column | **[std]** proxy shaped like the ONS UK national life tables — *population* mortality, **not** an annuitant table. Anchored at `q(M, 65) = 0.0130` with 9.5% p.a. age progression and a 0.65 female factor |

**Substituting a licensed basis** means replacing `mort_table.csv` with a same-schema
file — SAPS S3/S4 or the PMA16/PFA16 family — and setting `Projection.annuitant_adj` to 1
so the population-proxy adjustment stops being applied on top of an annuitant table. No
formula changes.

## The mortality construction, and its three standardizations

```
q_base  = ONS-shaped table rate × α          α = 0.80    [std]
q_imp   = q_base × (1 − f(x))^(c − c₀)       f = 1.25% to age 90, tapering to 0 at 110  [std]
q_rated = min(1, θ × q_imp)                  θ = 1.0 standard, 1.35 on the enhanced point  [std]
q_m     = 1 − (1 − q_rated)^(1/12)
```

Every one of the three factors is a standardization, and the notes are explicit about how
weak each is:

- **α = 0.80** is a shape-level placeholder, not calibrated against any published
  annuitant-versus-population comparison. It is the weakest link in the reference basis.
- **The improvement scale** stands in for the CMI Mortality Projections Model — CMI_2024
  [R12], now CMI_2025 [REG-R30] — whose software is restricted. It **materially
  understates** the age–period–cohort structure of the real model and exists only so the
  reference implementation is runnable without CMI access. The choice of long-term
  improvement rate is the single most sensitive judgment in UK annuity valuation, and the
  CMI model carries no default recommendation for it.
- **θ** is the simplest overlay that reprices longevity without touching contract
  mechanics; insurers' real rating structures (postcode, condition-specific factors) are
  not public.

The liability is a life-contingent stream with **no offsetting decrements**, so the level
of this rate is the single largest lever on it. Treat all reference-basis results as
mechanics demonstrations.

## Sign convention

The notes define `CF(t)` as total gross liability **outgo**, which is `liability_cf`;
`net_cf` is its negative, the library-wide income-positive convention. Both are published
as `result_cf()` columns rather than one being made to stand for the other — the same
arrangement `SPIA_US_S`, `DIA_US_S` and `WholeLife_US_A` use. There is no premium income
in the projection at all: the purchase price is a pricing input at `t = 0`.

## Naming

Cells follow lifelib and `SPIA_US_S`. The full symbol mapping lives in the `Projection`
Space docstring. Four cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `G(t)` | `cum_annuity_pp(t, kind)` | The notes use one symbol for two accumulations — see above |
| `l` vs `L` | `lives_if` / `payment_factor_life` | They differ only by case in the notes, as in `SPIA_US_S` |
| `w(t)` | `overlap_gate` | Not a lapse rate; there is no lapse on this product at all |
| `IF(t)` | `pols_if` | Not a policy count but the probability *any* payment obligation remains — kept because it is what the rest of the library calls the expense weight |

## Standardizations used

Everything in this list is **[std]**: the whole mortality basis — table, α, improvement
scale and taper, θ; the limiting age of 115; the flat 3% RPI and expense inflation; the
starting income; maintenance expense of £30 a year; the half-month accrual in the
proportionate final payment; the scenario mortality switch; joint-life independence
(which ignores broken-heart dependence and so modestly overstates the expected dependant
stream); measuring the value-protection balance at `t − 1` on arrears; the age-based
stopping rule in place of the notes' `IF(t) < 1e-6` alternative; and reading the
dependant's contractual "percentage of the higher of income at death and at guarantee
end" as `δ × A(y(t))`, which is exact under a non-decreasing escalation path and would
need explicit treatment under a decreasing one.

Deliberately excluded, per the notes: exact-day payment mechanics and stub proportioning,
the 30-day cancellation window, GMP-bearing policies and their different escalation
dates, and RPI reform risk.

## Tests

`tests/test_pension_annuity_uk.py` asserts every row of the notes' worked example to the
penny — the instalment schedule, the anniversary step to £1,390.50, the £43,209.50
value-protection lump sum on the month-17 death, the G column including the dependant's
instalment from month 18, and the £695.25 proportionate stub — plus the guarantee floor,
the overlap gate on both settings, the four escalation bases and their degeneracy under a
deterministic RPI path, the advance-timing VP netting rule, the `v + δ ≤ 1` bound, the
guarantee/VP exclusivity, and that no lapse machinery exists anywhere in the model.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-pension_annuity-r1
[R10]: #uklib-pension_annuity-r10
[R11]: #uklib-pension_annuity-r11
[R12]: #uklib-pension_annuity-r12
[R5]: #uklib-pension_annuity-r5
[R6]: #uklib-pension_annuity-r6
[REG-R22]: #uklib-reg-r22
[REG-R27]: #uklib-reg-r27
[REG-R30]: #uklib-reg-r30
[std]: #uklib-std
<!-- END generated citation links -->
