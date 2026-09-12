# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/temporaire_deces/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the attained-age revision rule and the published
> *tarif de base annuel* [S3], PTIA as an acceleration whose payment ends the contract
> [S1] [S2] [S3] [S6], PTIA cessation earlier than death cessation [S3], premium
> cessation on death and on PTIA [S3] [S7], the first-year suicide void [R1], the
> absence of any surrender or reduced-paid-up value [R3], and the fractionation loadings
> with their *frais d'échéance* [S1]. Every behavioural and experience assumption is a
> **[std]** standardization: no French insurer publishes a mortality table, a PTIA
> incidence rate, an expense loading, a commission scale or a lapse rate for this
> product [S1] [S2] [S3] [S6] [S7] [S8] [S9] [S12], and the homologated TH 00-02 /
> TF 00-02 tables are annexed to an *arrêté* and are cited by name rather than
> redistributed here [R6] [REG-R22] [REG-R23]. Replace the decrement and expense tables
> with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/temporaire_deces/run.py
python products/temporaire_deces/run.py 2      # the level-premium variant
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/temporaire_deces/TD_FR_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` with one row per **month** and one column per cash
flow line; `result_cf_annual()` is the same frame summed into policy years, which is the view
the technical notes' worked example is stated on and the one to lay beside an annual-step
model; and `result_pols()` is the decrement side beside them, with each annual rate published
next to the monthly rate derived from it.

**The time index.** `t` is **0-based** and counts **policy months**, the clock lifelib's
`basiclife/BasicTerm_S` and the other monthly models of this library run on: `t = 0` is the
first policy month and month `t` runs from time `t` to time `t + 1`. `proj_len()` is the
**number** of projected months — the exclusive end of the frame — so `result_cf()` runs
`t = 0 … proj_len() - 1`, has `proj_len()` rows and is built with lifelib's
`for t in range(proj_len())`. On the anchor cell `proj_len_y() = 75 - 58 = 17` policy years and
`proj_len() = 12 × 17 = 204` months.

Because every contractual schedule here is annual, the policy year is derived and used as a
lookup key: `duration_mth(t) = t` is the completed policy months, `duration(t) = t // 12` the
completed policy years, `policy_year(t) = duration(t) + 1` the contractual 1-based label, and
`age(t) = issue_age + duration(t)` the attained age — which steps at the **anniversary**, not
monthly. Only the two policy-year-keyed CSVs read `policy_year(t)`, and nothing is indexed by
it; see *Inputs are external files* below.

Every model point here is new business at issue, so every frame starts at `t = 0`; there is no
in-force offset. `pols_if(0) = pols_if_init()`, and `pols_if(proj_len())` is the expiring
cohort, defined for the closure identity and a weight on nothing.

The model and both its Spaces carry docstrings — `model.doc` describes the product and
the projection basis, `model.Projection.doc` holds the full mapping between the
technical notes' symbols and the cells names, and `model.Data.doc` says what each input
file is and, for the mortality table, what it is *not*.

## The cotisation rises with attained age — the French delta

This is the one thing about the product that a reader arriving from `Term_UK_S` or
`Term_US_S` will get wrong, and it is visible in the cash flows rather than buried in a
parameter. The French default premium form is `revisable`: the cotisation is recomputed
at **every annual renewal** from the tariff rate at the new attained age
[S1] [S2] [S3] [S4] [S6] [S7] [S9] [S10]. So `prem_pp(t)` moves every year — and **only** at
the anniversary: the tariff is re-read in the first month of each policy year and is flat across
that year's twelve months, so a 204-month frame carries seventeen distinct cotisations and not
204.

| policy year | 1 | 2 | 3 | … | 17 |
|---|---|---|---|---|---|
| months `t` | 0–11 | 12–23 | 24–35 | … | 192–203 |
| attained age | 58 | 59 | 60 | … | 74 |
| `prem_rate(t)` [S3] | 1,05 % | 1,13 % | 1,56 % | … | 4,86 % |
| `prem_pp(t)` | 1 575,00 | 1 695,00 | 2 340,00 | … | 7 290,00 |

What is actually *collected* in a month is `prem_inst_pp(t)`, the instalment the elected
*fractionnement* makes due: the whole cotisation in the first month of the policy year on the
annual mode, a twelfth of it every month on the monthly one.

`prem_pp(24) / prem_pp(12) = 1,56 / 1,13 = 1,380531` — a 38 % step from age 59 to 60
against a trend of about 8 % a year. That step is in the published grid, and a fitted
curve smooths it away, so `prem_rate` is a **table lookup and nothing else**. Over the
whole cover the cotisation multiplies by 4,6286, which is exactly `r(74)/r(58)` and does
not depend on the capital at all — a one-line test of the entire premium engine.

The level alternative, `constante`, is a model point column and a **[std]**
construction: no French standalone contract in the corpus writes a level cotisation
[S1] [S2] [S3] [S6] [S7] [S9] [S10]. With `level_premium = 0` it is derived by actuarial
equivalence with the revisable stream over the whole cover period, on **tariff
survivorship** — insured decrements only, no lapse — at `tech_rate = 0,5 %` **[std]**:

```
P_lev = tariff_prem_pv() / tariff_annuity() = 60 476,2476 / 15,449728 = 3 914,3891 €
```

`prem_level_pp()` takes `level_premium` directly where the model point supplies one
(model point 3) and derives it where it does not (model point 2), so both branches ship.

The two forms do **not** collect the same projected premium total, and a test asserting
that they do is testing the wrong identity. The equivalence ignores lapse; once lapses
truncate the expensive late years the `constante` projection collects 36 367,46 €
against the revisable 31 999,13 €. The identity that does hold is the discounted one on
tariff survivorship, `P_lev × 15,449728 = 60 476,25 €`. Switching form moves projected
premium income by +13,7 % and `net_cf` by +18,4 % with no change to a single claim,
which makes it the largest structural lever in the model [R11] [R13].

`prem_rate` also carries `tariff_drift`, an experience re-rating of the class, at
**0 % p.a.** in the base run. Two of the eight carriers reserve an express right to
reprice for class experience [S1] [S6] and the same carrier's current page implies a level above
its own retrieved grid [S3] [S4]; freezing the card at its retrieved vintage is what
keeps the base run reproducible from cited data alone. A drift assumption is a
premium-income assumption, not a mortality one.

## PTIA is an acceleration, not an addition

*Perte totale et irréversible d'autonomie* pays the **same** capital, early, to the
insured, and its payment ends the contract [S1] [S2] [S3] [S6] [S8]. Arithmetically that
is one two-decrement table, not two covers: `mort_rate` and `ptia_rate` are **dependent**
rates and therefore *additive*,

```
pols_if(t+1) = pols_if(t) × (1 − mort_rate_mth(t) − ptia_rate_mth(t)) × (1 − lapse_rate_mth(t))
```

so a life that leaves through the PTIA decrement is gone from `pols_if` and can never generate a
death claim. An implementation using independent rates, `1 − (1−q_d)(1−q_p)`, gets
0.00479680 against 0.00480000 at `t = 0` — immaterial there, material at older ages, and
either way a convention that has to be declared.

**The additivity is also why the two rates are converted to the month together.** `mort_rate`
and `ptia_rate` stay the **annual** rates the technical notes tabulate. What the monthly
recursion applies is their sum converted at constant force, `decr_rate_mth(t) = 1 − (1 − q_d −
q_p)^(1/12)`, split back into `mort_rate_mth` and `ptia_rate_mth` in the ratio `q_d : q_p`.
Converting each rate apart and adding the results is the tempting reading and it is wrong here
for exactly the reason above: it is the *sum* the annual recursion applies, so it is the sum
that has to compound back. The naive form gives a twelve-month insured survival of 0,9952029339
against 0,9952000000 — 2,6 × 10⁻⁶ of error in `pols_if` at the first anniversary and
1,0 × 10⁻⁵ by month 204 — and loses the exact `ptia_rate_mth / mort_rate_mth = ptia_ratio` that
the acceleration ratio rests on.

`check_decrement_closure()` asserts the consequence at every `t`: claim events plus
lapses plus survivors equal the original policy. It is built by direct summation over the
exit cells with no reference to the recursion, so a PTIA life left in force or counted
twice fails there rather than hiding inside a plausible-looking total.

PTIA cover also **stops earlier than death cover**, at `ptia_end_age`, in five of the
eight retrieved carriers [S2] [S3] [S6] [S7] [S8]. The switch is a hard gate on the
attained age rather than a taper: `ptia_rate(t)` is exactly zero from the first `t` with
`age(t) ≥ ptia_end_age()`. Because the attained age steps on the anniversary, the gate closes
on an anniversary too: on the worked configuration that is `t = 84 … 203`, the whole of the
policy year at attained age 65 onwards. Model point 11 enters at exactly `ptia_end_age`, so its
PTIA cover never attaches at all.
`check_ptia_gate()` recomputes the gate independently of `ptia_rate` and asserts both.

The suicide exclusion never touches PTIA. Art. L. 132-7 voids the **death** cover for
suicide in the first **year** [R1] — "au cours de la première année du contrat", so the
exclusion covers months `t = 0 … 11` in full and a monthly grid does not shrink it to month 0 —
and PTIA is not death, so `suicide_factor` multiplies `benefit_death_pp` alone. Nor does the model carry the art. R. 132-5
immediate-cover ceiling of 120 000 €: that alinéa is confined to principal-residence loan
cover [R1] [R2].

## No cash value, anywhere

Art. L. 132-23 forbids both *rachat* and *réduction* on a temporaire décès [R3]. There is
no account value, no surrender value, no reduced-paid-up state and no maturity value at
any duration [S3] [S5] [S7] [S9] [S11], so a lapse is a pure decrement: it moves
`pols_if` and pays nothing.

`claims(t, "LAPSE")` exists, returns zero, and appears in `result_cf()` as a zero column,
because a non-zero lapse row is the pitfall a reader arriving from a US model with cash
surrender values will import. A column of zeros states the product fact; a missing column
would only hide it. `check_no_cash_value()` is trivially zero by construction and is
published anyway — the failure it guards against is not an arithmetic slip but an edit,
and a named check that must stay at zero makes that edit fail loudly.

The same statutory fact is why the whole of the exit machinery is lapse. The 30-day
*renonciation* window [REG-R29] [S1] [S2] [S3] sits inside the year-1 lapse rate
**[std]**; there is no surrender charge, no dynamic surrender behaviour and no paid-up
election to model.

## The last projected year has no lapse

The notes' processing order puts lapses at the **end** of the month, after both insured
decrements. At the end of the final projected policy year the cover expires, and a lapse and an
expiry are then the same event paying the same nothing. So `lapse_rate(t)` is zero through the
**whole** of that policy year — months `proj_len() - 12 … proj_len() - 1`, 192 to 203 on the
anchor cell — and the whole surviving population leaves as an expiry. The zero covers the year
and not just its last month because the notes state the convention of a policy year:
`w(n − 1) = 0` **[std]**, under *Lapse* and in step 9 of the processing order. Zeroing only the
final month would leave eleven months of 6 % lapse inside the final year and move the survivor
figure away from the notes' own. Read over the whole year it reproduces their split of the
closure identity:

| | deaths | PTIA | lapses | survivors | total |
|---|---|---|---|---|---|
| worked configuration | 0,06737020 | 0,00516859 | 0,64859269 | 0,27886852 | **1,00000000** |

The **survivor term is exactly what the annual-step model this replaced carried**, being a pure
anniversary quantity; the three exit terms are not, and the reallocation is the expected effect
of the finer grid — a decrementing block reaches the claim decrements later in the year, so
fewer lives leave through them and correspondingly more leave as a lapse. (The annual grid read
0,06939268 / 0,00536169 / 0,64637711 against the same 0,27886852.)

`pols_if(proj_len())` is that survivor figure. It is read by
`check_decrement_closure()` and by nothing else — never a weight on a cash flow — and
`result_cf()` stops at `t = proj_len() - 1`. There is no `pols_expiry` cells, because the
notes put `l(12n)` in the identity directly rather than naming the expiry as a decrement.
Nothing in the cash flows moves either way.

## The *délai d'attente*

A *délai d'attente* delays the start of cover: 12 months for illness-caused death and
PTIA where the adhesion carried no medical formality, with the cotisations collected
returned to the heirs on a death inside the window [S6]; 3 months at another carrier,
waived for accidental death [S9]. Five of the eight retrieved carriers have none
[S1] [S2] [S3] [S7] [S8], and the composite runs with `waiting_period_y = 0` [S3].

Model point 9 switches it on for one year. The mechanics are cited, the arithmetic is
**[std]**: inside the window a death claim pays `prem_refund_pp(t)`, the cotisations actually
**collected** up to and including the **month** of claim, in place of the capital, and a PTIA
claim pays nothing. On a fractionated point that is now strictly less than the annual cotisation
of the year of claim, which is both the literal reading of "les cotisations collectées" and the
only one that stays a cash quantity; model point 9 pays annually, so its 296,00 € is unchanged.
The window itself is counted in months, `duration_mth(t) < 12 × waiting_period_y()` — the unit
the sources actually state it in (12 months at one carrier, 3 months at another), and exactly
the old window for a whole number of years. The monthly grid makes a **sub-annual** window
expressible for the first time; no shipped model point uses one, so no `waiting_period_m` column
is introduced. The refund accumulates at nil interest **[std]** — no source gives a rate. The accidental capital is *not* suppressed inside the
window, which is the [S9] waiver. The decrements are untouched throughout: the window
changes what a claim pays, never who leaves.

## Inputs are external files

The six input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `TD_FR_S/` holds nothing but formulas:

```
products/temporaire_deces/
  model_point_table.csv        <- inputs live here
  premium_rate_table.csv
  mort_table.csv
  lapse_table.csv
  freq_loading_table.csv
  benefit_schedule.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  TD_FR_S/                     <- formulas only
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
| `premium_rate_file` | `premium_rate_table()` | `premium_rate_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `freq_loading_file` | `freq_loading_table()` | `freq_loading_table.csv` |
| `benefit_schedule_file` | `benefit_schedule()` | `benefit_schedule.csv` |

**The trade-off:** the model is not portable on its own. Copy `TD_FR_S/` without the
CSVs and it will read fine, then fail on first evaluation. What you gain is that a diff
of the model shows logic changes only, and an input can be swapped in place — point
`Data.mort_table_file` at another same-schema file and the projection follows, with no
formula change. Tests cover both halves of that bargain.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Twelve model points. **Point 1 is the worked-example anchor cell** (revisable / M58 / non-smoker / 150 000 € / cover to 75 / PTIA to 65 / annual). Points 2–12 exercise the level premium derived and given, all four fractionation frequencies, a *surprime*, the accidental option, PTIA running to the death-cover limit, a cell entering at `ptia_end_age`, a one-year *délai d'attente*, a 35-year run from age 30, and a 20 000 € capital | anchor cell **[std]**, the technical notes' worked example |
| `premium_rate_table.csv` | The *tarif de base annuel* by attained age 18–74 under `rate_id = maif_2019`, as a decimal fraction of the capital, with a `provenance` column marking ages 66–74 as in-force rates only | **[S3]**, a real published grid — the only complete French standalone temporaire décès rate card in the corpus. A 2019–2021 vintage: use it for shape, not for level [S3] [S4] [S10] |
| `mort_table.csv` | Annual death rates by attained age 18–74, with each row tagged in a `provenance` column | **[std]** Gompertz-form proxy `0.00400 × 1.09^(age − 58)`. *Not* a published or homologated table: TH 00-02 / TF 00-02 are annexed to an *arrêté* and are cited, never shipped [R6] [REG-R22] [REG-R23]. The 9 % slope is calibrated on the published grid's own gradient and sits at the top of it — the grid compounds at 7,7 % a year over ages 42–58 and 8,98 % over the rated span 35 → 74 [S3] — and a tariff gradient is not a mortality gradient. **The anchor a replacement must preserve is `mort_rate` at age 58 = 0.00400** |
| `lapse_table.csv` | Annual lapse by policy year, 12 / 10 / 8 / 6 % | **[std]**, and **no observed range exists** — not one of the eight retrieved carriers publishes a lapse rate [S1] [S2] [S3] [S6] [S7] [S8] [S9]. Elevated for three years to absorb the *renonciation* window [REG-R29], then flat |
| `freq_loading_table.csv` | The fractionation multiplier and the fixed annual *frais d'échéance* by payment frequency | **[S1]** — with the 1,30 € association subscription and the 3 % annuity conversion charge, the only disclosed charge figures in the whole corpus |
| `benefit_schedule.csv` | Benefit factors by schedule id and policy year; one schedule, `constant`, factor 1.0 in every year | [S1] [S2] [S3] [S6] [S7] [S8] [S9] — the capital of a French standalone temporaire décès does not amortize. The table exists so a decreasing shape can be dropped in; no source gives one, so none ships |

### How the time-like input columns are keyed

The model's `t` is 0-based; the shipped inputs are not all keyed by it, and each column was
decided by meaning rather than by name:

| File | Column | Decision |
|---|---|---|
| `lapse_table.csv` | `policy_year` (1 … 4) | **Contractual 1-based label — file unchanged.** The rates stay **annual**; `lapse_rate_base(t)` reads them at `policy_year(t) = duration(t) + 1`, so months `t = 0 … 11` take the 12 % of policy year 1 and the last row is clamped to from policy year 4 on. `lapse_rate_mth(t)` does the spreading |
| `benefit_schedule.csv` | `policy_year` (1 … 57) | **Contractual 1-based label — file unchanged.** `benefit_factor(t)` reads it at `policy_year(t) = duration(t) + 1`, clamped to the last row |
| `freq_loading_table.csv` | `instalments` | **Not time-like.** The number of cotisation instalments per policy year — 1 / 2 / 4 / 12 — which drives `prem_cycle()` and `prem_inst_pp(t)`. The column shipped with the file all along; the monthly grid is what gave it something to drive |
| `model_point_table.csv` | `waiting_period_y` | **An elapsed count, in contractual policy years — unchanged.** A `1` is a one-year window, which is months `t = 0 … 11`: `in_waiting(t)` is `duration_mth(t) < 12 * waiting_period_y()` |
| `model_point_table.csv` | `issue_age`, `cover_end_age`, `ptia_end_age` | Attained ages, not points on the time axis — unchanged |
| `model_point_table.csv` | `issue_date` | Carried for identification, read by no formula — unchanged |
| `premium_rate_table.csv`, `mort_table.csv` | `age` | Attained age, read through `age(t) = issue_age + t` — unchanged |
| `freq_loading_table.csv` | `prem_freq` | Not time-like — unchanged |

No CSV holds the model's `t` under any name, so **no input file's values were shifted** by the
move to the 0-based index. What moved is the two lookups, which now go through
`policy_year(t)` instead of passing `t` raw.

## Modules that are off in the base run

Four constructions are implemented and switched off, so the base run reproduces the
worked example while the machinery stays visible and testable.

| Module | Switch | Off value | What it does |
|---|---|---|---|
| Tariff drift | `tariff_drift` | `0.0` | Multiplies the rate card by `(1 + drift)^duration(t)`, an experience re-rating of the class [S1] [S6] [S7]. The exponent is completed policy **years**, because a re-rating is an annual act |
| Premium-shock lapse | `shock_lapse_beta` | `0.0` | `M_shock = 1 + β·max(0, P(t)/P(t−12) − 1 − g0)` with `g0 = 0.10` — the ratio is between consecutive **renewals**, so the previous cotisation is read twelve months back. The revisable form hands the policyholder a rising bill, and the grid's own +38 % step at age 60 [S3] is exactly where an affordability response would show; switched on it bites through the whole of policy year 3, months 24–35, and nowhere else |
| Selective lapsation | `sel_lapse_lambda` | `0.0` | Loads persisters' mortality by `1 + λ·max(0, w_cum − w_ref)` once cumulative lapse passes `w_ref = 30 %`, with `w_cum` read **at the anniversary** so the loaded `mort_rate` stays one annual rate for its policy year. Larger here than on a UK level-premium term policy, because cumulative lapse reaches 64,9 % over seventeen years |
| Accidental capital | `acc_share` | `0.0` | An *additional* capital `(accident_multiplier − 1) × acc_share × B(t)` on the **accidental share** of claims [S1] [S2] [S6] [S7] [S9] [S12], not a uniform uplift. No retrieved source gives an accidental share of deaths |

The selective-lapsation cells short-circuits when `sel_lapse_lambda` is zero, and that is
load-bearing rather than an optimization: the loaded death rate depends on the lapse
path, the lapse path depends on the premium under the shock module, and on the
`constante` form the premium depends on the survivorship the loaded rate would feed. The
equivalence is therefore struck on `mort_rate_base` and `ptia_rate_base` — the tariff
rates — which is both the actuarially right basis and what keeps the derivation acyclic.

Indexation on the PASS or an insurer rate [S1] [S2] [S6] [S7] is described in the sources
and is **not** implemented: it reprices capital and cotisation together on an exogenous
index, and refusal is definitive at three carriers [S2] [S6] [S7], so modelling it would
add an absorbing state driven entirely by an assumption with no source.

## Sign convention

`net_cf` is **income positive** — cotisations in, claims and expenses out — which is the
notes' own orientation and the library-wide sign. `liability_cf` publishes the same
stream outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are columns of
`result_cf()` so the identity is verifiable in the frame rather than only in prose. A
Solvabilité II best estimate is `Σ v(t) × liability_cf(t)` over the relevant risk-free
term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R4] [REG-R5]; nothing in this
library discounts.

`expenses` is the notes' **total** and includes `commissions`, which is published beside
it because the notes' worked-example table prints both. The commission is a *part* of the
expense column, not a further line: `net_cf` subtracts `expenses` once and never
`commissions` as well. The worked example fixes the reading —
`expenses(0) = 250 + 2,08 + 0,06 + 630 = 882,14 €` in the first **month**, the maintenance term
being one twelfth of the 25 € annual charge, and the last of those four is the 40 % initial
commission on the whole annual cotisation collected in that month. The twelve months of policy
year 1 total 904,22 €.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` wherever that model has an analogue:
`pols_*` for policy counts, plural nouns for cash flows, `*_rate` for **annual** rates and
`*_rate_mth` for the monthly ones derived from them, `*_pp` for per-policy amounts,
`claims(t, kind)` with an uppercase `kind` string, and `pols_if_at(t, timing)` for the
within-month in-force reads. The technical notes use compact actuarial symbols; the full mapping
lives in the `Projection` Space docstring. Seven cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `P_tar(t)`, `P_lev`, `P(t)` | `prem_tariff_pp` / `prem_level_pp` / `prem_pp` | Three different amounts, one per cells: the tariff cotisation `SA·r·f·φ`, the level cotisation struck by equivalence on that same amount, and what is actually charged — either of those **plus the fixed *frais d'échéance* `F` once**. `P(t)` is the one that feeds `premiums` and the commission base; the equivalence is struck on `P_tar` |
| `q_d(t)`, `q_p(t)` | `mort_rate_base` / `mort_rate`, `ptia_rate_base` / `ptia_rate` | The table rate and the rate applied after the selective-lapsation loading are different numbers; and the `constante` equivalence is struck on the *tariff* pair, which is what keeps it acyclic |
| `B(t)` | `benefit_pp` / `benefit_death_pp` / `benefit_ptia_pp` | `B(t)` is the contractual capital. What a claim actually pays differs inside a *délai d'attente*, where a death pays back cotisations and PTIA pays nothing |
| `w(t)` vs `w_cum(t)` | `lapse_rate` / `lapse_cum` | `lapse_cum` is a proportion of the original cohort, not a running total of `lapse_rate`, and the loading it feeds moves *claims* |
| `expenses(t)` | `expenses` / `commissions` / `claim_expenses` | `expenses` is the notes' total and contains the other two; they are named because the worked example rebuilds a month from them line by line |
| `P(t)` vs `P_inst(t)` | `prem_pp` / `prem_inst_pp` | Library-wide `prem_pp` is the **annual** cotisation per policy, which is what the notes' `P(t)` means and what the tariff produces; `prem_inst_pp` is the instalment the elected *fractionnement* actually collects in a month. Twelve monthly instalments sum to exactly one `prem_pp`, fee included |
| `q_d(t)` vs `q_dm(t)` | `mort_rate` / `mort_rate_mth`, `ptia_rate` / `ptia_rate_mth`, `lapse_rate` / `lapse_rate_mth` | The unsuffixed cells keeps the **annual** meaning the technical notes give it — the rate of the policy year containing month `t` — and the `*_mth` companion is the rate actually applied in the month. `lapse_rate_ann` is a retired name for exactly this reason |

Two further names exist only because of the time index. **`policy_year(t) = duration(t) + 1`**
is the contractual 1-based label, and it is what the two policy-year-keyed CSVs are read at;
keeping it as a named cells rather than an inline expression is what stops the 0-based `t` from
being passed raw into a table whose first row is policy year 1. And `duration_mth` / `duration`
/ `policy_year` is the same triple `Obseques_FR_S` and `ADE_FR_S` already carry, so the three
models on this chassis read alike.

The model point carries `issue_date` and `benefit_shape`, and neither drives a formula:
on the *différence de millésime* basis a projection on policy years needs `issue_age` and
nothing else, and only the `constant` benefit shape has a shipped schedule. Both are
exposed as documented cells rather than dropped, because the notes' model point attribute
table lists them and a silently missing column is worse than an inert one.

## Standardizations used

Everything in this list is **[std]**: the whole mortality table and its 9 % Gompertz
slope; `ptia_ratio = 0.20`, which has **no source at all** and is the assumption in the
model most in need of one; the lapse duration table, for which **no observed range
exists**; the suicide factor 0.98 and its restriction to year 1 and to death claims;
acquisition expense 250 €; maintenance 25 € inflating at 2 %; claim expense 150 € per
death or PTIA claim; initial commission 40 % of the first-year cotisation and renewal 5 %
from year 2; the technical rate 0,5 % used only for the `constante` equivalence and never
to discount a published cash flow; the whole `constante` form, since no French standalone
contract in the corpus writes one; the additive dependent-rate convention and the
death-and-PTIA-before-lapse processing order; **the constant-force conversion of every annual
rate to the month, taken on the combined insured decrement and split in the rates' own
proportion**, since no retrieved French source states a conversion convention for any decrement;
**the collection of the cotisation in `prem_instalments` equal instalments on the mode's own
cycle, fee included**; the expense inflation stepping by policy year rather than compounding
continuously; the zero lapse rate in the final policy
year; the *délai d'attente* arithmetic and its nil-interest refund; `acc_share = 0`,
`tariff_drift = 0`, `shock_lapse_beta = 0` and `sel_lapse_lambda = 0`; and the model
points themselves.

The only quantities in the model that are **not** standardizations are the tariff grid
[S3], the fractionation loadings and *frais d'échéance* [S1], the constant benefit factor
[S1] [S2] [S3] [S6] [S7] [S8] [S9], the zero lapse benefit [R3], and the structural rules
— attained-age revision, PTIA acceleration and cessation, premium cessation, the
first-year suicide void, and expiry with nothing payable.

## Tests

`tests/test_temporaire_deces_fr.py` asserts the twelve months of the notes' first policy year
and every one of the seventeen rows of their policy-year table, read off `result_cf_annual()`,
to the cent and `pols_if` to six decimals; the totals at full precision; the level-premium
variant's five printed years and its `P_lev = 3 914,3891 €` reached two independent ways and
unmoved by the conversion; the closure identity's four-way split; that twelve monthly rates
compound back to exactly the annual ones and that the in-force at every anniversary is what the
annual recursion gives; that `result_cf_annual()` is the monthly frame regrouped and not a
second projection; that each annual contract term lands on the policy year rather than inside
it; and one test per listed modeling pitfall — the revisable cotisation moving with attained age, PTIA never paid twice, PTIA
cover stopping first, the additive dependent-rate convention, the absence of any surrender
value, the *différence de millésime* age basis, the tariff grid's unsmoothed +38 % step,
the suicide factor applying only to death and only in the first year, the premium-cessation rule
applied once, expiry with no tail state, the two premium forms *not* collecting the same
total, `rating_factor` never reaching the capital, the fractionation loading and fee not
being double-charged, and the accidental option having no effect at `acc_share = 0`.

Its month-level golden dictionary is keyed by the 0-based `t` (`t = 0 … 11`) and its
policy-year one by the contractual 1-based label (1 … 17), and it pins the frame directly:
`list(df.index) == list(range(204))` with `proj_len() == 204` and `proj_len_y() == 17`, and
`len(result_cf_annual()) == 17`. `tests/test_model_conventions_fr.py` asserts the same library-wide frame
rule for every model point of every model — index name `t`, `index[0] >= 0`, contiguous, and
`index[-1] == proj_len() - 1`.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-temporaire_deces-r1
[R11]: #frlib-temporaire_deces-r11
[R13]: #frlib-temporaire_deces-r13
[R2]: #frlib-temporaire_deces-r2
[R3]: #frlib-temporaire_deces-r3
[R6]: #frlib-temporaire_deces-r6
[REG-R1]: #frlib-reg-r1
[REG-R2]: #frlib-reg-r2
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R29]: #frlib-reg-r29
[REG-R4]: #frlib-reg-r4
[REG-R5]: #frlib-reg-r5
[std]: #frlib-std
<!-- END generated citation links -->
