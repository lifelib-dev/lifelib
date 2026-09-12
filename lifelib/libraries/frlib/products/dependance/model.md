# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/dependance/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the two-state trigger and its AVQ and AGGIR grids
> [S1 §2.2] [R1] [R3], the *rente partielle* at half the *rente totale* [S1] [S2] [S7]
> [S8], the *capital d'équipement* paid once per membership [S1 §4.3.2.1] [S5 art. 17], the
> 0 / 12 / 36-month *carence* by cause with termination and full refund of premiums
> [S1 §1.1.4.2c] [S3] [S5 art. 7] [S7 §3.2], the three-month *franchise* from recognition
> [S1 §4.3.1.2] [S7 §4.2.1], premium *exonération* from recognition [S1 §1.2.4]
> [S6 art. 18], the eight-year *mise en réduction* and the CNP *barème* behind it
> [S1 §1.3] [S5 annexe 2] [S7 §4.6], no surrender value [S1 §7.3] [S11], and the two
> separate indexations [S1 §1.2.3, §4.3.1.3] [S5 arts. 15, 21] [S7 §3.4].
> **Every rate is a standardization.** No French LTC incidence or continuance table is
> public: [R12 §3.1.3](#frlib-dependance-r12) specifies the structure of the laws a model needs and states that
> its numerical bases are the insurer's own undisclosed experience tables, and no
> BCAC-style published reference table for *dépendance* was located [REG-R28]. The
> prevalence curve is a **[std]** logistic fitted to two *sourced* DREES APA rates per
> sex [R7]; the severity shares that turn public GIR prevalence into insured prevalence
> are **[std]**; the two state-mortality multiples are **[std]**, one of them calibrated
> against a CCSF duration [R9 §2](#frlib-dependance-r9) and one against nothing; the mortality proxy is a
> Gompertz shaped like a French population table and is **not** TH 00-02 / TF 00-02
> [REG-R22] or TGH05 / TGF05 [REG-R21]; and the lapse table has one indirect anchor
> [R10 §2.3](#frlib-dependance-r10). The premium is the CCSF's 2013 indicative price [R8 §2.2](#frlib-dependance-r8), not a rate.
> Replace the basis with portfolio experience before drawing any conclusion.

## Run it

```bash
python products/dependance/run.py       # the worked example's anchor cell
python products/dependance/run.py 9     # a partielle claim already 18 months old
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/dependance/Dep_FR_S")
model.Projection[1].result_cf()
```

## The time index, and what the input keys are

`t` is the policy month and it is **0-based**, the library-wide convention: `t = 0` is the
first projected month and it is a full month, not an issue instant — the premium, the
maintenance and acquisition expense, the *carence* refund, the *capital* and the month's
decrements all sit on that one row.

`proj_len()` is the **number of projected months**, the exclusive end of the frame:
`proj_len() = 12 × (terminal_age - age_at_entry())`, 480 on the base cell, the projection
is `range(proj_len())`, and `result_cf()` and `result_states()` have `proj_len()` rows
indexed `t = 0 … proj_len() - 1`. The last projected month on the base cell is therefore
`t = 479`, at attained age 109. This is lifelib's `for t in range(proj_len())`.

Two other clocks run beside `t` and neither is the frame's index:

- `policy_year(t) = t // 12 + 1` is the **contractual, 1-based label** derived from `t`.
  Policy year 1 is `t = 0…11`, the anniversary is the start of months 12, 24, …, and
  `duration(t) = t // 12` is the same thing as a 0-based count of completed years.
- `z` is the months since **first recognition** of a covered state. It is a cohort label
  running from 1 — cohort 1 is a state recognised at the end of the previous month — and
  it is stored as element `z - 1` of the `dep_cohorts(t)` vectors. It is independent of
  `t` and the conversion did not touch it.

**No input CSV is keyed by the model's `t`,** so no input file changed:

| File | Time-like column | Decision |
|---|---|---|
| `lapse_table.csv` | `policy_year` (1 … 11) | Contractual 1-based label; values unchanged. Read as `lapse_rate_base(t)` through `policy_year(t) = t // 12 + 1`, capped at the last row |
| `revision_table.csv` | `policy_year` (1 … 6) | The same; values unchanged. Also read at the synthetic month `12 (y - 1)` by `premium_factor(y)` |
| `reduction_table.csv` | `years_paid` (5 … 30) | An **elapsed count** of completed premium years, not a point on the frame; already 0-based in lifelib's sense and unchanged. Read as `reduction_coeff(n)` with `n = years_premiums_paid(t) = (t + 1) // 12` |
| `mort_table.csv` | `age` (40 … 110) | An attained age, not a time index; unchanged. Read at `age(t) = age_at_entry() + t // 12` |
| `model_point_table.csv` | `claim_duration_months`, `years_paid`, `carence_*_months`, `franchise_months` | All **elapsed counts or contractual lengths in months**, not points on the frame; unchanged. None of them offsets the frame — an in-force cell still opens at `t = 0` and restarts its policy-year clock at the valuation date |
| `prevalence_table.csv`, `severity_share_table.csv`, `cause_mix_table.csv` | none | Keyed by sex, trigger grid and cause |

## Five ledgers, and why the model needs all of them

The health chain is *autonome* → *dépendance partielle* / *dépendance totale* → *décès*,
with lapse as a further exit from autonomy, and a fifth in-force but **paid-up** ledger,
*réduite*, reached only by lapse from eight full years of premiums:

```
                     +------------- i_T -----------------+
                     |                                   v
    autonome ---- i_P + ---> partielle ---- i_A ---> totale ----> deces
       |                         |                     |
       |                         v                     v
       |                       deces                 deces
       |
       +-- lapse before 8 years --> nothing at all
       |
       +-- lapse from 8 years ----> reduite --- i_T ---> totale (reduced rente)
```

Three absences are **product facts, not gaps**. There is no account value and no
surrender value [S1 §7.3] [S11], so no `cv_pp` exists and a lapse before eight years
carries no cash flow at all. There is no death benefit on this composite — the optional
*Capital décès* is out of scope [S1 §1.1.4.1] — so `claims_death` does not exist. And
there is no maturity: the cover is *viagère* [S1 §1.1.5] [S5 art. 8], so what ends the
projection is a **[std]** terminal age of 110 rather than the contract.

The *partielle* → *totale* transition is modelled, which is a **departure from the only
actuarial reference retrieved**: [R12 §3.1.2](#frlib-dependance-r12) sets it to zero for want of a transition law
and prices two separate guarantees instead. The contracts do provide for deterioration
[S1 §4.3.1.2] [S5 art. 13], so this implementation carries it, and `aggravation_rate`
therefore has no external anchor at all.

Recovery out of a covered state is a **named input held at zero**, not an omission:
`recovery_rate` is wired into the ledger roll and into `pols_recovery()`, and the base run
sets it to zero, as [R12 §3.1.1](#frlib-dependance-r12) does. The direction of error is one-sided — claims are
overstated — and no retrieved source quantifies it. A test switches it on and asserts all
three roll-forward checks still close.

### The reduced ledger is the one a naive model omits

`pols_red(t)` is fed by `pols_reduction(t)` — the lapses of month `t` on a membership with
eight full years of premiums behind it — and drained by mortality and by entry into
*totale*. It never lapses, because there is no premium left to miss. Treating that lapse
as an exit **understates lifetime claims by 4.57%** and drops a ledger that peaks at
**8.27% of the original policy at month 194**, attained age 86 — the largest state in the
model after `pols_auto` at that duration.

The amount is carried as a **value** rather than per cohort: reductions happen in every
month from the qualifying period and each freezes `G(y) × c(n)` at its own date, so the
ledger holds a distribution of amounts. `red_rente_value(t)` tracks the
probability-weighted total and `red_rente_pp(t)` the mean, which is **exact in
expectation** because incidence does not depend on the amount.

## The two dependent ledgers are two-dimensional

A cohort is indexed by `z`, the months since **first recognition**, for two reasons that
have nothing to do with each other:

- the **franchise** drops the first three instalments, so a cohort is paid only from
  `z >= franchise_months() + 1` [S1 §4.3.1.2] [S7 §4.2.1];
- the ***rente* in payment** is the guarantee of the policy year in which the cohort was
  recognised, indexed forward at `reval_rente` — a different rate from the one that
  indexes the guarantee before claim — so the amount depends on the cohort's vintage,
  which is what `z` records.

`dep_cohorts(t)` holds all four vectors for one month and is the model's only list-valued
cells: four two-argument recursions would be `4 × proj_len() × max_dur()` separate
cells, nearly a million on the base cell, where this is `proj_len()` cells with a loop
inside.
`pols_part_dur(t, z)` and its siblings read elements out of it, so the notes'
two-dimensional objects are still addressable by name. The fourth vector is a
**population × amount** ledger for the reduced-*rente* claims, whose amounts are frozen
individually and cannot be recovered from the policy year.

**The duration index runs from first recognition.** A cohort that aggravates keeps its `z`,
so it does not serve a second *franchise* **[std]** — no retrieved document states that it
does, and [S1 §4.3.1.2] makes the higher amount effective from the first day of the
following month without mentioning a new *franchise*. Restarting `z` on aggravation would
drop three instalments per aggravated life.

## Prevalence is not incidence, and the identity that converts it

Every public French number about dependence measures **receipt of the *allocation
personnalisée d'autonomie*** — granted on the AGGIR grid to GIR 1–4 [R2 arts. R. 232-1,
R. 232-4](#frlib-dependance-r2) [R3]. It is a **prevalence**, not an incidence, and a **public** classification
rather than the insurer's, which the *notice* says in terms [S5 art. 13] [S6 art. 21.1].
Two explicit **[std]** steps stand between it and a claim frequency, and both are in the
model rather than in a spreadsheet behind it.

**Step one, `severity_share(kind)`.** The fractions of APA prevalence read as insured
*partielle* and *totale*, keyed by the contract's trigger grid. Two sourced anchors bound
the base row and neither pins it: the GIR 1–2 share of APA beneficiaries at end 2023,
**34.9%** [R7], and the market's own count — 44,200 *rentes* in payment against about
1.39 million people covered, an insured prevalence of about **3.2%** against an APA
prevalence of 7.2%, a ratio of about **0.44** [R10 §2.3](#frlib-dependance-r10) [R13 p6](#frlib-dependance-r13) [REG-R28]. The shipped
`s_T + s_P` is 0.45.

**Step two, the prevalence-to-incidence identity.** Differentiating the state proportions
along the age axis gives entry forces in terms of the prevalence slope, the aggravation
force and all three mortality forces. Three properties an implementation must respect, and
`inc_rate_partial()` and `inc_rate_total()` do:

- **the mortality terms are not refinements** — a rising prevalence understates incidence
  because the dependent population is simultaneously being drained by its own excess
  mortality, and dropping `mu_T · pi_T` understates `i_T` by more than a third at age 85;
- **`aggravation_rate` and `inc_rate_total` are not independent inputs** — the stock of
  *totale* lives is pinned by the assumed prevalence, so consistently varying the
  aggravation force from 0 to 0.20 to 0.40 moves lifetime claims by only
  **+0.54% / 0 / −0.52%**, while adding it *without* re-deriving the incidence raises them
  **0.84%** and puts the lives in the wrong state, which matters more than the total
  because *partielle* pays half;
- **`inc_rate_partial` can go negative at extreme ages** — both rates are floored at zero
  **[std]**. On the female base basis the floor never binds below the terminal age; on the
  male basis it binds at attained age 109, which
  `test_the_identity_carries_its_mortality_terms_and_floors_both_rates` asserts on model
  point 10.

The gradient from attained age 70 to 90 is a factor of 28 for `i_P` and **81** for `i_T`,
and `i_T` overtakes `i_P` between 80 and 85 — the severity mix worsening with age, arriving
through the mortality terms rather than through the constant shares, which cannot produce
it.

## State-dependent mortality is the largest lever on this product

`mort_rate_partial()` and `mort_rate_total()` apply proportional hazards **on the force**,
so the annual rates at attained age 85 are 0.06179 healthy, 0.10562 in *partielle* and
0.23841 in *totale*. Applying healthy-life mortality to dependent lives while leaving the
incidence basis unchanged raises lifetime claims by **159.7%**. No impaired-life table for
either French dependence state exists in any retrieved source [R12 §3.1.3](#frlib-dependance-r12), which is
exactly why the multiple is easy to leave at 1 and catastrophic to leave at 1.

`mort_total_mult` is **calibrated, not guessed**. `sojourn_total(84)` returns **2.9989
years** at 4.27, against the mean duration of about three years the CCSF reports for heavy
dependents at a mean age at onset of 84 for women [R9 §2](#frlib-dependance-r9); at 2.75 it gives 4.19 years and
at 3.50, 3.50. `mort_partial_mult` has **no such anchor**: it must exceed 1 and sit well
below `mort_total_mult`, and at 1.75 `sojourn_partial(82)` gives 3.14 years, the same order
as the 29.2-month mean duration of APA receipt across all GIRs [R7].

Both sojourn cells are **calibration companions**, not part of the projection: they run on
a continuously advancing exact age, where `age(t)` steps once a policy year.
`mort_force_at(x)` interpolates the force log-linearly between the table's integer ages,
which reproduces the shipped Gompertz exactly.

## The carence and the franchise are different things

| | *Carence* | *Franchise* |
|---|---|---|
| Runs from | inception | recognition |
| Length | 0 / 12 / 36 months **by cause** | 3 months, absolute |
| Effect | blocks the benefit **and terminates the membership**, refunding every premium | delays payment by three instalments |
| Cells | `carence_factor(t)`, `pols_carence_exit(t)`, `refunds_carence(t)` | `franchise_months()`, the `z >= fr + 1` test in `claims` |
| Cost of removing it | **+3.99%** of lifetime claims | **+7.09%** |
| Sources | [S1 §1.1.5, §1.1.4.2c] [S3] [S5 art. 7] [S7 §3.2] | [S1 §4.3.1.2] [S7 §4.2.1] [S8] |

Model points 6 and 7 are model point 1 with one of the two switched off, so the two are
separable in the tests rather than confounded.

**A *carence* claim is a decrement with a cash flow, not a suppressed claim.** Note what
`carence_factor` does *not* touch: `pols_auto(t+1)` does not depend on it at all, because a
*carence* claim ends the membership rather than deferring it. The blocked lives leave the
in-force ledger exactly as the covered ones do and take `refunds_carence(t)` with them —
**in policy year 1 that refund is 0.6141 €, three quarters of the year's *rente* and
*capital* claims combined (0.8071 €)**. Modelling the *carence* as a multiplier on
incidence alone [R12 §3.2.1](#frlib-dependance-r12) leaves the membership in force and omits the refund.

**The *franchise* is not a premium holiday.** *Exonération* runs from recognition
[S1 §1.2.4] [S4] [S5 art. 21] [S6 art. 18], so a life inside the three months pays no
premium and receives no *rente*. Carrying it the way an income-protection deferred period
is carried — premium-paying, benefit-free — overstates premium income.

## Premium income rides on pols_auto, never on pols_if

`pols_prem(t)` is the premium-paying population and it is `pols_auto(t)` on every model
point except a `total_only` one. Lives in a recognised state are exonerated [S1 §1.2.4] and
reduced lives are paid up [S1 §1.3], so both bands pay nothing: at attained age 90 they are
**44.6%** of the in-force block. `result_cf()` publishes all five ledgers beside `pols_if`
for exactly this reason. Lapse applies to `pols_auto` alone, for the same fact seen twice:
neither band has a premium to miss, and with no surrender value there is nothing to
surrender for [S1 §7.3].

## What cover_type does, and the one thing it standardizes

`total_and_partial` is the composite the notes specify and the basis of the worked example.
`total_only` buys the *rente totale* alone, and the model reads that as: *partielle* is
**not a recognised state**, so it pays no *rente*, carries no *capital*, does not exonerate
the premium — and the *carence* and the *franchise* both attach at entry into *totale*,
whether direct or by aggravation, since that is then the first recognition. **The health
chain is untouched**, which is what keeps the prevalence identity intact.

One consequence is a **[std]** departure worth naming: on a `total_only` cell an
aggravating life starts a **fresh** duration cohort and therefore serves a *franchise*,
where on a `total_and_partial` cell the duration index runs from first recognition and
deterioration does not restart it. Both follow from the same principle — the clock runs
from first recognition of a *covered* state — and no retrieved document addresses either.
Lapse still applies to `pols_auto` alone there, so an unrecognised *partielle* life pays
premium but cannot lapse: a **[std]** simplification that overstates premium income.

## The capital d'équipement is paid once per membership

It rides on `pols_capital_claims(t)` — `pols_recognition(t)` less the entrants out of the
reduced ledger, which have lost the option [R12 §1.2.1](#frlib-dependance-r12). A life that takes it on entering
*partielle* takes nothing further on aggravating [S1 §4.3.2.1] [S2] [S5 art. 17], so an
aggravation appears there only on a `total_only` cell, where it is the first recognition.
Paying it again would inflate capital claims by the whole aggravation flow. It is paid with
**no *franchise*** **[std]**, which only [S10] states in terms.

## Two indexations, two ledgers

`reval_guarantee` (1.0% **[std]**) moves the guarantee and the premium in the same
proportion [S1 §1.2.3] [S5 art. 21] [S7 §3.4]. `reval_rente` (1.5% **[std]**) moves every
*rente* in payment, whatever its vintage [S1 §4.3.1.3] [S5 art. 15] [S7 §4.2.3]. The
reduced guarantee moves with **neither** [S7 §4.6]. Collapsing the two rates into one
happens to work only when they are equal, and the base configuration deliberately sets them
different so that a test can tell.

The consequence a reader should expect: a cohort recognised earlier ends up on a **larger**
amount than one recognised later on the same policy, because *rentes* in payment index
faster than guarantees do. `test_the_rente_in_payment_moves_at_a_different_rate_from_the_
guarantee` asserts exactly that.

The tariff revision `revision_rate(t)` multiplies on top of `reval_guarantee` and is a
**scheduled rate index by policy year**, not an assumption: a real revision is a management
action, and the shipped path — nil for five years then 1.5% — is arbitrary inside the
0–10% band [S7 §4.4]. `revision_lapse_factor(t)` is the premium-shock lapse module, off in
the base run and 1.24 at the 10% cap [S1 §1.2.3].

## Inputs are external files

The eight input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Dep_FR_S/` holds nothing but formulas:

```
products/dependance/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  prevalence_table.csv
  severity_share_table.csv
  lapse_table.csv
  cause_mix_table.csv
  reduction_table.csv
  revision_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Dep_FR_S/                    <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file is
read once per model rather than once per model point.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `prevalence_file` | `prevalence_table()` | `prevalence_table.csv` |
| `severity_share_file` | `severity_share_table()` | `severity_share_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `cause_mix_file` | `cause_mix_table()` | `cause_mix_table.csv` |
| `reduction_file` | `reduction_table()` | `reduction_table.csv` |
| `revision_file` | `revision_table()` | `revision_table.csv` |

The decrement basis is four files and not one because nothing in this product's assumption
set comes from a single publication: keeping them apart keeps their provenances apart.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eleven model points: **point 1 is the worked example** (F70, *totale et partielle*, AVQ-5, 1,000 € + 500 €/month, 3,500 € *capital*, 75 €/month, 0/12/36 *carence*, 3-month *franchise*, reduction from 8 years); a male 65 `total_only` AVQ-6 cell; a female 60 AGGIR cell with no *capital* option; a male 75 cell on a 5-year reduction period paying quarterly; a female 55 cell inside the couple discount and below every prevalence anchor; point 1 with the *carence* removed; point 1 with the *franchise* removed; point 1 paying annually; a *partielle* claim 18 months old; a *totale* claim 6 months old; and a paid-up cell with twelve years of premiums | anchor cell **[std]**, technical notes; the *rente*/premium pair [R8 §2.2](#frlib-dependance-r8) |
| `mort_table.csv` | Healthy-life annual mortality by sex and age 40–110, with age 110 forced to 1 | **[std]** Gompertz proxy `1 - exp(-B c^x)`, `B = 5.2321459244e-06`, `c = 1.11704543`, fitted to the **[std]** anchors `mort_rate(60) = 0.00400` and `mort_rate(90) = 0.10500`; male rows are the same force × **1.60 [std]**, a sex multiple introduced here because `technical-notes.md` specifies a female basis only. **Not** TH 00-02 / TF 00-02 [REG-R22] or TGH05 / TGF05 [REG-R21]; population-table-shaped, and **no INSEE value is read** — [REG-R24] names the series a production fit would use, not a number used here |
| `prevalence_table.csv` | `prev_ceil`, `prev_beta`, `prev_x_mid` per sex | the two slope parameters are pinned to **sourced** DREES rates at end 2023 — 20% of women and 13% of men aged 80–89 read at 84.5, 54% and 40% from age 90 read at 93, from [R7] alone ([REG-R26] carries the 60+ APA rate and the GIR mix, no rate split by age band and sex); `prev_ceil = 0.90` is **[std]** and unidentified by a two-anchor fit |
| `severity_share_table.csv` | `share_partial` and `share_total` by trigger grid | all three rows **[std]**; the `avq5` row is bounded by the sourced GIR 1–2 share of 34.9% [R7] and the market ratio of about 0.44 [R10 §2.3](#frlib-dependance-r10) [R13 p6](#frlib-dependance-r13) [REG-R28]; the `avq6` (×0.85) and `aggir` (×1.25) rows have **no anchor whatever** and say so |
| `lapse_table.csv` | Annual lapse by policy year, 8 / 6 / 5 / 4 / 3 % | **[std]**; no French LTC persistency study is public, and the only anchor is a book that shrank 9.9% in 2024 on 28,400 new subscribers [R10 §2.3](#frlib-dependance-r10) [REG-R28] |
| `cause_mix_table.csv` | accident 10% / illness 55% / neurological or psychiatric 35% | **[std]** (spec footnote 8); the three-way *structure* is near-universal across the retrieved contracts, the **weights** are stated by none of them |
| `reduction_table.csv` | *Barème* coefficient by completed years of premiums, 16% at 5 rising to 70% from 30 | the **only published French LTC reduction scale** retrieved, CNP Banque de France annexe 2 in force 1 January 2012 [S5 annexe 2]; re-based to an 8-year qualifying period **[std]** (spec footnote 13) |
| `revision_table.csv` | Tariff revision by policy year, nil for five years then 1.5% | **[std]** (spec footnote 10); the only sourced constraint is the 10% annual cap [S7 §4.4] |

Every file carries a `provenance` column whose words say which kind of claim each row is,
and a test asserts they are all present and that the two unanchored severity rows say so.

## Sign convention

`net_cf(t)` is **income positive** — `premiums - claims - refunds_carence - expenses -
claim_expenses` — which is the notes' own sign and the library-wide one, so there is no
outgo-positive `liability_cf` companion. `refunds_carence` is **not** a claim: it is a
return of premium and it has its own column, because it is the only cash flow on this
product that runs backwards through the *carence*.

Nothing is discounted. A market-consistent valuation applies EIOPA's monthly risk-free term
structure [REG-R5] to exactly this stream, and that is a layer above this model.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
population counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth`
for monthly ones, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase `kind`
string. The full symbol mapping lives in the `Projection` Space docstring. Five cases
needed care:

| Notes | Cells | Why |
|---|---|---|
| `q_H` / `q_P` / `q_T` | `mort_rate` / `mort_rate_partial` / `mort_rate_total` | `mort_rate` means the **healthy-life** rate in every model in this library. Reading a dependent's mortality out of it is this product's largest available error, and the naming is there to prevent it |
| `t` vs `z` | the two arguments | Different clocks, never mixed: the *carence* takes `t` and the *franchise* takes `z` |
| `red` and its frozen `G(y) c(n)` | `pols_red` / `red_rente_pp` | The ledger holds a **distribution** of frozen amounts, so the model carries a probability-weighted value and its mean — exact in expectation, and what the notes license |
| `carence_exit(t)` | `pols_carence_exit` / `refunds_carence` | The count is a `pols_*`; the cash flow keeps the notes' own name because it is a refund of premiums and not a claim |
| `rente_total_monthly`, `premium_monthly` | `rente_total_mth`, `premium_mth` | The library spells a monthly amount `*_mth` |
| `P(y)` | `premium_mth_pp` — with `premium_pp` for `12 P(y)` | Library-wide `premium_pp` is the **annual** premium per policy, which is how `PER_FR_S` reads it — that model is projected monthly too, and its annual *versement* falls whole in the month that opens each plan year. This contract's premium is genuinely monthly, so every recursion here uses `premium_mth_pp`; `premium_pp` is published alongside it so the two periodicities cannot be confused |

## Standardizations used

Everything in this list is **[std]**: the entire experience basis — the Gompertz mortality
proxy and its two anchors, the 1.60 sex multiple on the force, the two state-mortality
multiples, the aggravation force, the prevalence ceiling, the two severity-share factors
for the non-base trigger grids, the cause mix and the lapse table; the terminal age of 110
and the age basis `entry_age + floor(t/12)`; the monthly reading of the three-month
*franchise* and the duration clock that does not restart on aggravation; the *capital*
paid with no *franchise*; the reduction composite (*totale* only, no *capital*, no further
*revalorisation*) and the re-basing of the CNP *barème* to eight years; the two
*revalorisation* rates and the tariff-revision path; the *revalorisation* falling on the
policy anniversary rather than a calendar date; the premium-shock lapse multiplier and its
threshold; the absence of any fractional-payment loading; acquisition 150 €, maintenance
3.00 €/month, assistance 1.20 €/month and expense inflation 1.5% a year, with claim
adjudication 250 € per recognition and *rente* handling 10 € per instalment held **flat**;
the order out of the autonomous ledger — mortality, then lapse, then incidence among the
survivors; the floor of both entry forces at zero; the restart of the policy-year clock at
the valuation date on an in-force cell; and, on a `total_only` cell, the fresh duration
cohort on aggravation and the continued exposure of the unrecognised *partielle* ledger to
premium but not to lapse.

**There is no observed range for any expense level on this product.** No retrieved
document discloses an expense assumption, a loading or a commission rate, and [R12 §3.2.1](#frlib-dependance-r12)
parameterises the loadings symbolically without values. Only two structural facts are
sourced and both are respected: assistance ends on *mise en réduction* [S1 §1.3]
[S5 art. 24.2], so its base excludes `pols_red`; and claim adjudication is a medically
supervised process with a 45-working-day deadline and an arbitration route
[S5 arts. 19–20] [S6 arts. 23–24], so it carries a per-claim cost an order of magnitude
above the per-instalment one.

## Tests

`tests/test_dependance_fr.py` asserts the notes' sixteen-month worked example to the
displayed precision, the policy-year-1 aggregates, the lifetime totals, the derived monthly
rates at ages 70 and 71, and the three month-by-month derivations the notes give — month 0
end to end, month 4 as the first instalment after the *franchise*, and the four-factor
decomposition of the month-12 *carence* step. Beyond that there is one test per named
modelling pitfall: flat state mortality, dropping the reduced ledger, confusing the
*carence* with the *franchise*, treating the *franchise* as a premium holiday, bolting an
aggravation rate onto an identity derived without one, charging premium to the whole
in-force block, paying the *capital* twice, collapsing the two indexations, and restarting
the duration clock. Several replace a **formula** rather than a Reference, because setting
a Reference would move the incidence identity as well — and the point of the identity is
that the two must move together or not at all.

The four `check_*()` cells — the in-force roll-forward, the five-ledger population
identity, and the two dependent ledgers against their aggregate recursions — are asserted
on every model point, as is `check_model_point()`, which validates the input.

The frame itself is pinned twice: `test_worked_example_lifetime_totals_and_counts` asserts
`len(result_cf()) == proj_len() == 480` with `index[-1] == 479`, and
`tests/test_model_conventions_fr.py` asserts library-wide that the index is contiguous,
starts at or above zero and ends at `proj_len() - 1`.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-dependance-r1
[R3]: #frlib-dependance-r3
[R7]: #frlib-dependance-r7
[REG-R21]: #frlib-reg-r21
[REG-R22]: #frlib-reg-r22
[REG-R24]: #frlib-reg-r24
[REG-R26]: #frlib-reg-r26
[REG-R28]: #frlib-reg-r28
[REG-R5]: #frlib-reg-r5
[std]: #frlib-std
<!-- END generated citation links -->
