# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/rente_viagere/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the *terme échu* instalment, the rule that the
> *arrérage* of the month of death is due in full [S6] [S1 Art. C17.2] [S7 Art. 7.3], the
> *réversion* at δ of the *rente atteinte* from the 1st day of the month or quarter
> following death and its definitive coefficient [S2] [S3] [S6 Art. 5.4.3], the *annuités garanties* as an
> annuity-certain floor and their exclusivity with the *réversion* [S2] [S3] [S4], the four
> *paliers* schemes [S2 pt 10.e] [S3 pt 11.d], the 31 December revalorisation date with its
> first-year pro-rating and its zero floor [S2 pt 10.f] [S3], the *frais d'arrérages* per
> *quittance* [S5] [S7 Art. 17.3], the *frais sur encours de rentes* biting on the
> *provision mathématique* rather than on the instalment [S1 Art. C9] [S2], the absence of
> any surrender value [R8], and the €110 commutation threshold [R10 art. A. 160-2](#frlib-rente_viagere-r10). Every
> **rate** is a **[std]** standardization. TGH05/TGF05 are homologated by the arrêté du
> 1er août 2006 [R1] [REG-R21] and annexed to the Code des assurances [R12], and this
> library does not redistribute them, so the mortality basis shipped here is an
> INSEE-shaped **generational proxy** [REG-R24] anchored so that the tariff annuity factor
> reproduces the notes' placeholder *taux de rente* exactly. No French insurer publishes an
> annuity rate card [S4 §7.3.2.3], so ρ is a model point input.

## Run it

```bash
python products/rente_viagere/run.py         # the worked-example scenario
python products/rente_viagere/run.py 2       # the same contract, expected basis
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/rente_viagere/Rente_FR_S")
model.Projection[1].result_cf()
```

## The month index is 0-based

`t` counts months from the effective date and the frame is `range(proj_len())`: `t = 0` is
the first projected month — the first whole civil month of service, at the end of which the
first *arrérage* falls due — and the last index is `proj_len() - 1`. `proj_len()` is
therefore the **number** of months projected and `result_cf()` has exactly that many rows:
708 on the worked anchor, `12 × (120 − 61)`, indexed `t = 0 … 707`. Month `t` runs from
time `t` to time `t + 1`, and `duration(t) = duration_mth(t) // 12 = t // 12`,
`policy_year(t) = t // 12 + 1`, `age(t, life) = x(0) + t // 12`.

One cells keeps a different clock, deliberately. `lives_if(t, life)` is a **time-point**
quantity — the probability that a life is alive at *time* `t`, with `t = 0` at the
effective date — so month `t` opens at `lives_if(t)` and closes at `lives_if(t + 1)`, and
`payment_surv_mth(t)` selects between them: `t + 1` in arrears, `t` in advance. That is
what makes the *réversion* gate `1 − l_a(t)` and the *arrérage* of the month of death fall
where it does, and it is why nothing in this model is ever indexed before time 0.
`tariff_lives` is the same kind of object on the pricing clock. `result_pols()` publishes
the **closing** survival, `lives_if(t + 1, life)`, in its `lives_if_1` and `lives_if_2`
columns, because its rows are months and not time points.

## Mortality is the model

After conversion the contract has **no premiums, no surrender value at any duration, no
account value and no policyholder option of any kind** [R8, verbatim](#frlib-rente_viagere-r8) [S1 Art. C3] [S2]
[S3]. The only decrements are deaths. The model therefore has **no `lapse_rate` of any
kind**, no `av_pp_at`, no `cv_pp`, no surrender-charge scale and no dynamic behaviour
formulas, and a test asserts each of those names is absent rather than leaving it to
inspection.

The one election that survives conversion is not a cash flow but an **admission test**:
below €110 a month, multiplied by the number of months in the payment period, the insurer
may pay a capital instead, with the annuitant's agreement [R9] [R10 art. A. 160-2](#frlib-rente_viagere-r10) [S2]
[S3] [S5] — so there is no annuity to project. `check_commutation_floor()` rejects such a
model point rather than projecting it and reporting a small answer.

## Shared chassis with `PA_UK_S` and `SPIA_US_S`, and where France parts

The UK counterpart is
[`PA_UK_S`](../../../uklib/products/pension_annuity/model.md) and the U.S. one
[`SPIA_US_S`](../../../uslib/products/immediate_annuity/model.md), and the payout chassis
is deliberately the same: a life-contingent instalment stream, a certain-period **floor**
rather than a second stream, survival measured at the *payment point* rather than at the
end of the month, and a second life gated on the first one's death. Shared names carry
shared meanings — `annual_income`, `lives_if`, `lives_death`, `certain_floor`,
`payment_factor`, `payment_surv_mth`, `cum_annuity_pp`, `annuity_pp`, `annuity_payments`,
`pols_if`, `liability_cf`.

Where France parts:

| | `PA_UK_S` | `Rente_FR_S` |
|---|---|---|
| Mortality basis | ONS **period** table plus a separate improvement scale and a rated-age multiplier | **generational** table keyed on `(sex, birth_year, age)`; no improvement scale, no rating |
| Tariff vs best estimate | one basis; income is a quote | **two** bases — a unisex tariff on the prudent table [R3], a sex-dependent best estimate, and the gap is profit-shared [R17] [REG-R16] |
| Second life | dependant's stream at δ with an **overlap** rule against the guarantee | *réversion* at δ of the *rente atteinte*, gated on `1 - l_a(t)` — the annuitant's survival to the start of month t — never overlapping the guarantee because the options are exclusive |
| Escalation | four bases including a path-dependent RPI ratchet | **revalorisation** — a discretionary calendar-year uplift, floored at zero, pro-rated in the first partial year — plus the four *paliers* schemes, which are steps and not escalation |
| Death benefit | value protection, a refund measured against instalments already paid | ***prorata d'arrérages*** only: the month of death is paid in full; the design is *capital aliéné*, with no death capital |
| Charges | priced into the annuity rate | ***frais d'arrérages*** retained out of **every** payment, so a genuine cash flow |

### How far "shared" goes, counted

"Shared chassis" is not "the same names". Of this model's **82** `Projection` cells, **40**
— 49% — are also in `PA_UK_S` *and* `SPIA_US_S`; **38** have no counterpart in either,
which is where the French product actually is: `taux_rente_tariff`, `taux_rente_own_table`,
`unisex_gap`, `revalo_factor`, `palier_factor`, `prorata_pp`, `prorata_factor`,
`arrerage_charges`, `certain_excess_years`, `guarantee_coeff`, `reversion_coeff`,
`cal_year_index` and the rest. The overlap is the payout chassis; the remainder is France.

The annuity amount itself is now `annual_income`, the twins' name, so all three libraries
call the thing being paid the same thing. Five names that **both** twins carry are still
absent here, for two different reasons:

| Twin name | Absent because | Detail |
|---|---|---|
| `is_joint` | **spelled differently** | The FR model reads `reversion_pct() > 0` inline wherever the twins call `is_joint()`. A *réversion* is elected at liquidation *with* its rate δ, so "no second life" and δ = 0 are one state and a separate boolean would be a second spelling of the same fact |
| `mort_rate_base` | **spelled differently** | In the twins it is the table lookup before the rating multiplier. Here the lookup is `mort_rate_at_age(table_sex, gen, x)` — three arguments, because the table is generational — and `mort_rate(t, life)` is that lookup and nothing else. There is no intermediate quantity left to name |
| `rating_factor` | **feature absent** | No retrieved French source rates an annuity for health, postcode or condition. Art. A. 132-18 confines the tariff to a homologated table or an actuary-certified experience table [R3], and every medical selection any retrieved document describes sits on the *dépendance* rider [S5] [S6], not on the annuity. The UK enhanced/impaired market has no French counterpart in the sources |
| `lives_if_last` | **feature absent** | The twins' last-survivor probability `l_a + l_d − l_a l_d` exists because a benefit turns on the last death. The French obligation is `max(γ(t), l_a(t+1)) + 1{δ>0}(1 − l_a(t)) l_r(t+1)` — the reversionary is served *only* if the annuitant died first — which is not a last-survivor probability, so `pols_if()` composes it inline rather than borrowing a name that would mean something else |
| `lives_death_last` | **feature absent** | It is the last-death density that triggers UK value protection. A *capital aliéné* annuity has no death capital at all [R8]; the *prorata d'arrérages* is triggered by `d_a` and `d_r` separately |

## The table is generational, so there is no improvement scale

`mort_rate(t, life)` is a **pure table lookup**:

```
q(t, life) = mort_rate_at_age(sex(life), birth_year(life), age(t, life))
```

with nothing applied on top of it and no calendar-year argument. TGH05/TGF05 are
prospective generation tables: `q(sex, generation, age)` already gives the rate the life
will experience at that age [R1] [R19] [R25, secondary](#frlib-rente_viagere-r25). The trend is inside the table. An
improvement scale on top of it — which the UK sibling needs, because its base table is a
*period* table — double-counts the trend, so **`Rente_FR_S` has no `improve_factor` and no
`improve_rate` cells and must not acquire one**.

The *millésime* is a model point attribute and is **never derived from the projection
year**. A period-table implementation reads the rate for age 66 in calendar year 2027 and
walks diagonally across generations; a generational one reads `(g = 1961, x = 66)` whatever
the projection year. Model points 2 and 10 are two annuitants aged 65 at entry with
*millésimes* 1961 and 1963, and their rates at the same attained age differ by exactly two
years of the table's own improvement.

## The tariff table and the best-estimate table are different objects

Art. A. 132-18 requires the single homologated table applied to all lives to be "la table
appropriée conduisant au tarif le plus prudent" [R3, verbatim](#frlib-rente_viagere-r3) [REG-R23], which for an
annuity is TGF05. `tariff_table_sex` is therefore `"F"` and the tariff is unisex. The
projection meanwhile decrements each life on its **own** table, or on a **[std]** portfolio
blend at `portfolio_male_share = 0.45` where the model point carries `mix`.

```
taux_rente_tariff()    = 1 / (annuity_factor("F") x (1 + rate_loading))
taux_rente_own_table() = 1 / (annuity_factor(sex(1)) x (1 + rate_loading))
unisex_gap()           = taux_rente_own_table() / rho - 1
```

On the worked anchor `unisex_gap()` is **13.03%**: a male 65 born 1961 priced on his own
table would receive €472.47 a month instead of €418.00. That difference is the systematic
technical surplus the ministry says must in substantial part return to policyholders within
eight years [R17] [REG-R16] — which in this model it does, through ν. Collapsing the
two tables destroys both halves of the mechanic: price him on TGF05 *and* project him on
TGF05 and there is no surplus, hence no source for the revalorisation the contract shares
[S3] [R7]; project him on TGH05 without crediting the surplus back and the model shows a
permanent retained profit the eight-year rule does not allow.

`annuity_factor` is also the **only** place the *taux technique* enters the model, through
`v = (1 + i)^(-1/12)`. It prices the annuity and reaches the projection only through ρ. It
is not a discount rate: the best estimate discounts at the risk-free term structure
[REG-R4] [REG-R5] — the rule is carried on EIOPA's authority, neither Solvency II text
[REG-R1] [REG-R2] having been retrievable — and a test asserts that no cash flow cells mentions
`technical_rate` at all.

## Two mortality bases: table and scenario

The notes' worked example is a **scenario** — "the annuitant dies in month 25, the 26th
month of service; the reversionary survives throughout" — while the rest of the notes projects on an expected
basis. Both readings ship, as a model point column, which is the same device `PA_UK_S` and
`SPIA_US_S` use:

| `mort_basis` | `lives_if` | Model points |
|---|---|---|
| `table` | the monthly recursion off the shipped generational table | 2, 4, 5, 7, 8, 9, 10, 11 |
| `scenario` **[std]** | the step function `1{t <= death_mth(life)}` on the survival-to-time-t clock, a blank or negative `death_mth` meaning the life survives | 1, 3, 6 |

Point 2 is the worked configuration on the `table` basis and is the run to read for a
realistic cash flow shape; point 1 is the same contract as a scenario and reproduces the
notes row by row. The switch is a **[std]** modelling device, not a product feature, and it
never reaches the pricing side: `tariff_lives` and `annuity_factor` always run off the
table, because a scenario is a statement about one realisation and pricing is not.

## Revalorisation is a calendar event, and it is pro-rated once

`revalo_factor` steps at each **31 December** [S2 pt 10.f], never on a policy anniversary,
and the uplift reaches instalments payable from the following 1 January **[std]**. The
first step is pro-rated `ν × (13 − M0)/12` for the part-year of service [S3], which
degenerates to the full ν for a 1 January effective date — model point 5 is that case. On
the worked configuration, M0 = 4:

```
k(t) = 0 for t <= 8,  1 for 9 <= t <= 20,  2 for 21 <= t <= 32, ...
R(t) = 1,  1.011250,  1.026419,  1.041815, ...
```

Both halves are notes' pitfalls. An anniversary convention holds the annuity at its initial
level for twelve months instead of nine and shifts every later step by three months.
Dropping the first-year pro-rata scales every later month by
`(1 + ν)/(1 + ν(13 − M0)/12)` for the whole of the annuity's remaining life, because `R` is
a running product. `check_revalo_roll_fwd()` rebuilds the index from its closed form and
`check_calendar_index()` rebuilds `k(t)` from the calendar the model carries independently,
so either mistake fails a check rather than merely a golden value.

ν is floored at zero — the only contractual bound any retrieved document states [S1 Art.
C11] [S2] [S3] — so `R` is non-decreasing and `check_revalo_floor()` asserts it. The *frais
sur encours de rentes* appear in **no** recursion: they bite on the *provision
mathématique* and reduce the profit-sharing base, hence ν, and never an instalment [S1 Art.
C9] [S2] [S5] [S6] [S7].

## The options, and their coefficients

The technical notes carry κ as a model point attribute. It is **derived** here, because
both of its values are derivable and a derived coefficient cannot drift out of step with
the table that implies it:

| Option | Cells | How |
|---|---|---|
| *Réversion* | `reversion_coeff()` | the published [S6 Art. 5.4.3] table, shipped as `reversion_coeff_table.csv` and keyed on the *taux de réversion* and the *millésime* difference |
| *Annuités garanties* | `guarantee_coeff()` | `a / (a + certain_excess_years())` off the tariff table — the construction assumption (iv) describes |
| Neither | `option_coeff()` returns 1.0 | |

κ reduces the annuitant's own annuity **once, permanently, at conversion**. It does not
also scale the reversion stream — the survivor receives δ of the *already reduced* annuity
reached at death [S2] — and it is not released if the reversionary predeceases the
annuitant: "une réduction définitive, même si le bénéficiaire de la réversion vient à
décéder antérieurement" [S6 Art. 5.4.3, verbatim].

The two options are **not cumulative** [S2] [S3]. `check_options_xor()` asserts no model
point carries both, and `option_coeff()` raises rather than compounding two definitive
reductions of the same annuity.

`guarantee_coeff()` is **derived, not carried**. No retrieved document publishes the cost
of *annuités garanties*, so an implementation has to choose between a flat model point
attribute and a figure recomputed from the mortality basis; this one recomputes. The
certain-period annuity factor exceeds the life factor by the sum over the guaranteed
months of (1 − survival), which on the shipped basis is `certain_excess_years()` = 0.5431
against a factor of 29.63 — hence **0.982002** at 15 years, and, the property a single
figure cannot express, 0.9986 at 5 years and 0.9267 at 25. Assumption (iv) of the
technical notes carries the same 0.9820 and the same 0.54-against-29.63 derivation, so the
model and the notes agree; the coefficient moves with the table, which is why substituting
a licensed basis moves it too.

The *réversion* gate is `(1 − l_a(t))`, the annuitant's survival to the **start** of month
t, and **not** `(1 − l_a(t + 1))`, its survival to the end: the survivor's first
instalment falls in the month *after* the month of death, immediately after the *prorata
d'arrérages* has settled it. Gating on the end of the month pays the reversion and the
*prorata* in the same month, so the month of death is paid `1 + δ` times. [S6] states the reversion start as the
1st day of the "month **or quarter**" following death, so a one-month gate at every
frequency is a **[std]** reading of its monthly limb; it is exact at m = 12 and opens a
quarterly reversion up to a quarter early. No shipped model point combines a *réversion*
with m < 12, so nothing in the worked example turns on it. The verbatim
"à compter du premier jour du mois qui suit le décès" [S6] belongs to the *cessation* of
the annuitant's own instalments, which is where the technical notes quote it.

The *paliers* are steps, not escalation: `palier_factor(t)` is a step function of duration
and nothing compounds. The four published schemes are `inc1` 100→200%, `inc2`
100→125→150%, `dec1` 100→50% and `dec2` 100→75→50%, with the second step "d'une durée
égale" to the first [S2] [S3], which is why one number parameterizes both.

## The month of death is paid in full

```
h(t)             = t mod (12/m)
prorata_pp(t)    = ((h(t) + 1)/(12/m)) x A(t)/m
prorata_factor(t)= d_a(t)(1 - gamma(t)) + delta (1 - l_a(t)) d_r(t)
```

At m = 12 that is exactly **one full instalment** — instalments "cessent d'être dus à
compter du premier jour du mois qui suit le décès" [S6], and the accrued arrears belong to
the heirs [S1 Art. C17.2] [S7 Art. 7.3]. Losing it, which is the UK sibling's default for
the final partial period, understates the worked configuration's outgo by €429.04. At m = 4
a death in the first month of a quarter settles one third of the quarterly instalment and
in the second month two thirds; model point 6 is that case.

The `(1 − γ(t))` gate suppresses the *prorata* while the *annuités garanties* run, the full
instalment being payable there already — paying both double-pays the month of death. There
is no "with or without proportion" election in France: the *prorata* is the rule. On the
unobserved `advance` variant nothing has accrued unpaid at death, so `prorata_pp` is zero
**[std]**.

`pols_if(t)`, the expense weight, has a **one-month gap** in the month of an annuitant's
death: the annuitant leg is already 0 and the reversion leg has not yet opened, so no
maintenance expense is accrued in the month the *prorata* is settled. The notes' formula is
implemented as written rather than smoothed; the gap is one month of a €30-a-year expense
and it is flagged in the `pols_if` docstring so a reader meeting it in `result_cf()` knows
it is intended.

## Inputs are external files

**Three** CSVs, in this directory beside `run.py` — not inside the model folder:

```
products/rente_viagere/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  reversion_coeff_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Rente_FR_S/                  <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file is
read once per model rather than once per model point; a test counts the reads. That matters
more here than in the sibling payout models, because a generational table is two orders of
magnitude larger than a period one.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `reversion_coeff_file` | `reversion_coeff_table()` | `reversion_coeff_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eleven model points. **Point 1 is the worked configuration as a scenario** (€200,000, effective 1 April 2026, M65 born 1961 with a *réversion* at 60% to F61 born 1965, monthly *terme échu*, ρ = 3.30%, f = 3%, annuitant dies month 25, the 26th month of service); point 2 is the same on the expected basis; 3 and 4 are the *annuités garanties* variant at 15 years on either basis; 5 is a 1 January effective date with a `dec2` *palier* and no *frais d'arrérages*; 6 is quarterly, to exercise the *prorata* fraction; 7 and 8 carry `inc2` and `dec1` *paliers*; 9 is a `mix`-basis annuitant with a 100% *réversion* to an older reversionary; 10 is the *millésime* twin of point 2 with an `inc1` *palier*; 11 is the unobserved *terme à échoir* variant at a 1.00% *taux technique* | anchor **[std]**, technical notes' worked example |
| `mort_table.csv` | Annual mortality by sex, *millésime* 1940–1980 and age 50–120, capped at 1 at the limiting age, with a `provenance` column | **[std]** proxy with the *shape* of a French generation table — a rate keyed on `(sex, birth_year, age)` and on nothing else. **Not** TGH05/TGF05 [R1] [R12], which this library does not redistribute. Makeham–Gompertz in age with a 1.0% per *millésime* improvement, solved so that `annuity_factor("F")` at (1961, 65) is 29.630420 and `annuity_factor("M")` is 26.214580 — the factors that reproduce ρ = 3.30% and the male-table 3.73% of spec footnotes 6 and 7 at `rate_loading` |
| `reversion_coeff_table.csv` | The 11 age-difference bands × 3 published *taux de réversion*, with a `provenance` column | [S6 Art. 5.4.3], the only option-cost table any retrieved French source publishes; its adoption as a euro-annuity coefficient is **[std]** (spec footnote 15) |

**Time-like columns.** No input file is keyed on `t`. In `model_point_table.csv`,
`death_mth_1` and `death_mth_2` are points on the frame's own time axis — the month a life
dies on the `scenario` basis — so they moved with it: the worked example's `26` became
**25**, and the explicit "this life is named in the scenario and does not die" sentinel `0`
became **−1**, month 0 now being a real month that cannot double as a sentinel (a blank
cell means the same thing and is read as −1). Nothing else in the file is an index into the
frame and nothing else changed: `effective_year` and `effective_month` are a calendar
anchor, `guarantee_years` and `palier_step_years` are contractual term *lengths*, and
`annuitant_age`, `reversion_age` and the two *millésimes* are ages and calendar years.
`mort_table.csv` is keyed on `(sex, birth_year, age)` — an attained age, not a duration —
and `reversion_coeff_table.csv` on a *millésime* difference, so neither carries a time
index at all and both are untouched.

**Substituting a licensed basis** means replacing `mort_table.csv` with a same-schema file
keyed on exactly the same `(sex, birth_year, age)`. **No formula changes**, and in
particular no improvement scale to switch off — which is the whole point of the generational
shape. Note that it also moves `guarantee_coeff()` and `taux_rente_tariff()`, because both
are derived from the tariff table; `check_taux_rente()` will then fail until the model
points' ρ are restruck on the new basis, which is the intended behaviour rather than a
nuisance.

## Sign convention

The notes define `CF(t)` as total gross liability **outgo**, which is `liability_cf`;
`net_cf` is its negative, the library-wide income-positive convention. Both are published
as `result_cf()` columns rather than one being made to stand for the other — the same
arrangement `PA_UK_S`, `SPIA_US_S` and the other frlib models use. There is no premium
income in the projection at all: the *capital constitutif* is a pricing input at the
effective date, before the first projected month.

One column runs the other way. `arrerage_charges` is money the insurer **retains** out of
each *quittance*, so it is published positive and **subtracted**:

```
liability_cf = annuity_payments + claims_prorata - arrerage_charges + expenses
```

## Naming

Cells follow lifelib, `PA_UK_S` and `SPIA_US_S`. The full symbol mapping lives in the
`Projection` Space docstring. Five cases needed care:

| Notes | Cells | Why |
|---|---|---|
| κ (a model point attribute) | `option_coeff()`, `reversion_coeff()`, `guarantee_coeff()` | One symbol for two coefficients with two different derivations, both derivable — so both are derived rather than carried, and `option_coeff` is the one conversion applies |
| `q` | `mort_rate_at_age(table_sex, gen, x)` / `mort_rate(t, life)` | The tariff rate and the best-estimate rate are different objects; collapsing them destroys the unisex mechanic |
| `l` | `lives_if(t, life)` / `tariff_lives(t, table_sex)` | The projection path of a covered life, and the annuitant's survival on a pricing table, which ignores the scenario switch |
| `G(t)` | `cum_annuity_pp(t, kind)` | `"ANNUITANT"` is the deterministic as-if-alive schedule; `"ALL"` is the expected total paid across both streams including the *prorata*, which is the notes' printed figure |
| `IF(t)` | `pols_if` | Not a policy count but the probability *any* payment obligation remains — kept because it is what the rest of the library calls the expense weight |

## Standardizations used

Everything in this list is **[std]**: the whole mortality basis — the INSEE-shaped
generational proxy, its Makeham–Gompertz shape, its 1.0% per *millésime* improvement and
its anchoring; `rate_loading = 2.27%`, the margin between the pure annuity factor and the
quoted ρ, chosen so that the derivation reproduces spec footnote 6's factor of about 29.63
and its 3.30%; the limiting age of 120; the uniform force of mortality within a year of age
that turns the annual table into `mort_rate_mth`; the portfolio male share θ = 0.45 and the
`mix` blend it drives; the independence of the two lives, which ignores broken-heart
dependence and shared lifestyle and so modestly overstates the *réversion* stream; the
revalorisation rate ν = 1.50% and the convention that a 31 December credit reaches
instalments payable from the following 1 January; the expense inflation π = 1.50% and the
maintenance expense of €30 a year; the guarantee coefficient's derivation; the adoption of
the Préfon coefficient table as a euro-annuity coefficient; the scenario mortality switch;
the zero *prorata* on the unobserved `advance` timing; the one-month *réversion* gate
applied at every payment frequency, where [S6] says "month **or** quarter"; and the
age-based stopping rule.

Deliberately excluded, per the notes: the *frais sur encours de rentes*, which reduce the
profit-sharing base and never an instalment; proof-of-life suspension, which shifts timing
and not amount [S1 Art. C13] [S2] [S3]; the change-of-spouse recalculation [S2] [S3], which
a single-policy model point cannot carry; the *rente dépendance* doubling [S5] [S6]; the
€15 de-minimis on the *prorata* [S1 Art. C17.2]; the *majorations légales* [R22]; and
policyholder taxation [R13] [R14] [R15], which does not enter the insurer's liability cash
flows at all.

## Tests

`tests/test_rente_viagere_fr.py` asserts every row of the notes' worked example to the cent
— the €418.00 instalment and its €12.54 charge, the 1.125% pro-rated first uplift reaching
the month-9 instalment at €422.70, the second uplift at €429.04 from month 21, the whole
instalment settled as a *prorata* on the month-25 death, the *réversion* opening at €257.43
in month 26, `cum_annuity_pp(25, "ALL") = €10,979.65` with €329.39 retained, and
`liability_cf` of €412.56 and €252.28 — on the 0-based month index the notes' table now
carries, with `result_cf()` asserted to run `t = 0 … proj_len() - 1`. Then one test per
known modelling pitfall: the
absence of any improvement scale, the *millésime* rather than the projection year as the
table key, the separation of the tariff and best-estimate tables, the 31 December
revalorisation date, the first-year pro-rata, the *arrérage* of the month of death, the
`l_a(t)` reversion gate, the *prorata* gate and the `max` inside `payment_factor`, the
definitive reversion coefficient, the absence of any surrender machinery, the *frais sur
encours* never touching an instalment, the *frais d'arrérages* being charged per
*quittance*, the *taux technique* reaching no cash flow, and the *palier* never touching the
reversion stream.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-rente_viagere-r1
[R12]: #frlib-rente_viagere-r12
[R13]: #frlib-rente_viagere-r13
[R14]: #frlib-rente_viagere-r14
[R15]: #frlib-rente_viagere-r15
[R17]: #frlib-rente_viagere-r17
[R19]: #frlib-rente_viagere-r19
[R22]: #frlib-rente_viagere-r22
[R3]: #frlib-rente_viagere-r3
[R7]: #frlib-rente_viagere-r7
[R8]: #frlib-rente_viagere-r8
[R9]: #frlib-rente_viagere-r9
[REG-R1]: #frlib-reg-r1
[REG-R16]: #frlib-reg-r16
[REG-R2]: #frlib-reg-r2
[REG-R21]: #frlib-reg-r21
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R4]: #frlib-reg-r4
[REG-R5]: #frlib-reg-r5
[std]: #frlib-std
<!-- END generated citation links -->
