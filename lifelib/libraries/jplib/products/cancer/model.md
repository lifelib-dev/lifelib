# Implementation Notes

**Status:** Draft, 2026-08-20. Built from
[`products/cancer/technical-notes.md`](technical-notes.md); the product it
implements is specified in [`product-spec.md`](product-spec.md). Both state their
**deltas against the third-sector chassis**, medical insurance (*iryō hoken*, 医療保険):
its [product specification](../medical/product-spec.md), its
[technical notes](../medical/technical-notes.md), and the model that implements them,
[`Medical_JP_S`](../medical/model.md). This model carries that model's names for every
shared concept.

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced: the 90-day waiting period as a hard zero, the
> two-year repeat cycle measured from the previous payment trigger, 上皮内新生物
> (*jōhinai shinseibutsu*, carcinoma in situ) as a separate once-only tier that does
> not trigger the premium waiver, the absence of any day limit and of any surrender
> value, and the waiver on the first invasive diagnosis. The **incidence basis is
> sourced too**, which makes this product an exception in `jplib`: 全国がん登録
> (*zenkoku gan tōroku*, the national cancer registry) publishes incidence rates
> (*rikanritsu*, 罹患率) by five-year age band, freely [R5] [REG-R29]. Everything else is
> **[std]** — the sex split of that basis, the post-diagnosis survival model, the
> relapse hazard, the care frequencies, the expense scale and the premium itself. No
> carrier publishes a rate table for a cancer main contract, the statement of the
> method of calculating premiums and reserves (*sanshutsu hōhō-sho*, 算出方法書) is not
> published [REG-R2], and third-sector (*dai-san-bun'ya*, 第三分野) business has no standard
> incidence table and no reference pure premium to fall back on [R3]. Replace the
> assumption tables with company data before drawing any conclusion from the numbers.

## Run it

```bash
python products/cancer/run.py            # the anchor cell
python products/cancer/run.py 4          # another model point
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/cancer/Cancer_JP_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a `DataFrame` indexed by policy month `t` with one column per
cash flow line, and `result_pols()` the policy counts, rates and ledgers. `model.doc`
describes the product and the projection basis; `model.Projection.doc` holds the full
mapping from the technical notes' symbols to the cells names.

## Three states, not one — the structural contrast with the chassis

[`Medical_JP_S`](../medical/model.md) projects a single in-force population and reads a
hospitalization incidence off it. A cancer model cannot. The diagnosis benefit repeats on a two-year
cycle, the inpatient benefit has no day limit, and the treatment benefit pays by the
month — so all three run on **how long the insured lives after diagnosis**.
`Cancer_JP_S` therefore carries `pols_healthy` (never diagnosed), `pols_locked`
(diagnosed, inside the cycle) and `pols_open` (diagnosed, eligible again), and needs a
post-diagnosis survival basis as well as an incidence basis. `check_cancer_roll_fwd()`
asserts that the two diagnosed recursions collapse to the single line
`pols_cancer(t+1) = (pols_cancer(t) + diag_first(t)) × sc(t)`, which is where an
off-by-one in the delay shows up and nowhere else in the in-force figures.

Four things the third-sector chassis has are **absent here, as product facts**:

- **no `L1` and no `LA`** — no per-hospitalization day ledger and no lifetime aggregate
  (*tsūsan*, 通算) day ledger [S1] [S3] [R11]. What replaces them is a **60-month
  ledger on the treatment benefit**, a ledger on *months*, not days;
- **no benefit-driven termination** — paying the diagnosis lump sum neither terminates
  nor exhausts the contract [S1], so the in-force roll-forward has two ways out;
- **no `cv_pp` and no 自動振替貸付** (*jidō furikae kashitsuke*, automatic premium loan) —
  the composite is 無解約払戻金型 at every duration under 終身払 [S7] [S10] [S11], so there is
  nothing to lend against and a missed premium really does lapse the policy;
- **no `claims_death`** — the composite carries no death benefit [S1], so mortality is
  a pure liability-releasing decrement.

## The cycle is a delay on the trigger history, not a rate

A life that has just been paid cannot be paid again for `C` = 24 months; after that it
can, on a fresh relapse (*saihatsu*, 再発), metastasis (*ten'i*, 転移) or new primary,
without limit [S5] [S7] [S10]. That clock is keyed to an **event** — the previous
payment trigger — so `unlock(t)` is the trigger cohort of month `t − C` carried forward
on diagnosed decrements alone, and not a release rate applied to a stock. Two
consequences are easy to get wrong and both are pinned by tests. `unlock` reads `trig`,
which is first diagnoses **and** repeats: reading it off `diag_first` would let every
repeat payment escape the lock. And the clock is emphatically **not** the medical
chassis's 180-day one-hospitalization memory — different length, different trigger (a
payment, not a discharge), different consequence (eligibility, not grouping) [S5] [S1].
`check_cycle_ledger()` rebuilds `pols_locked` straight off the trigger vector with no
reference to the `unlock` recursion.

## 上皮内新生物 is a second benefit tier, not a discount on the first

`insitu_ev` attaches to `pols_healthy` alone and carries its own once-only ledger,
`insitu_avail`. It does not move the life into the diagnosed state, does not start the
cycle and does not trigger the waiver [S6] [S11] [S7] [S10]. Implementing it as
`insitu_pct × claims_diag` inside the main diagnosis benefit gets the amount right and
the cap, the cycle and the waiver all wrong. The three sourced treatments of in-situ
disease — full rate, half rate and 10% — are one model-point parameter, `insitu_pct`.

An in-situ diagnosis pays the reduced lump sum and the surgery benefit in full, and
**nothing continuing** **[std]**. The rationale is a data fact rather than a
convenience: the sourced estimated patient counts (*suikei kanjasū*, 推計患者数) and
mean length of stay (*heikin zaiin nissū*, 平均在院日数) are for malignant neoplasm
(*akusei shinseibutsu*, 悪性新生物) and do not measure in-situ exposure [R7], so
attaching the invasive frequencies to in-situ lives would credit them with an exposure
no retrieved statistic observes. The direction of the error is stated: it understates
the in-situ tier. `check_insitu_ledger()` asserts that benefit paid plus availability
remaining is one, reading the paid side off the published claim line rather than off the
recursion, so the identity cannot close by construction.

## Two ledgers that are per diagnosed life, not per block

`treat_months` counts against the 60-month cap and `adv_paid` against the ¥20,000,000
advanced medicine (*senshin iryō*, 先進医療) cap, and both measure what an **individual**
has consumed. Diagnosed lives enter at different times, so each is carried as a cohort
average diluted by new entrants — and only by `diag_first`, because a repeat trigger is
an already-diagnosed life whose ledger continues. Weighting either by `pols_cancer`
would measure the block's consumption and defer the cap forever; diluting with
`diag_rep` would reset a ledger that should keep running.

The direction of the approximation is stated rather than discovered:
`E[min(Σ, K)] ≠ min(E[Σ], K)`, so a deterministic average understates the cap's bite.
That matters more here than on the medical chassis, because the 60-month cap is reached
by a real minority rather than never — `treat_prob` and the diagnosed-state duration
give an expected 12.98 qualifying months against it [S5] [S11]. The ledgers read small
at the anchor cell (`M(12)` = 0.4002 months, `V(12)` = ¥2,401.31) and are not therefore
deletable: model point 4 carries a twelve-month cap that binds for more than four
hundred months of its projection.

## Monthly, and monthly by construction

Three mechanics are monthly by construction rather than by approximation: the 90-day
waiting period is three months of the grid, the treatment benefit's unit of payment
**is** the calendar month [S5] [S10] [S11], and the premium mode is monthly (*getsubarai*,
月払) throughout the composite [S1] [S6] [S11] [S12]. `t` is the policy month, and
`proj_len() = 12 × (omega_age − x + 1)` — 924 months on the anchor cell, running to the
terminal age of 第三分野標準生命表2018, 116 male and 118 female [REG-R18] [REG-R20]. A
diagnosis arising in month `t` pays its lump sum in month `t` and the life enters the
diagnosed state at the **end** of that month, so the four continuing benefits begin at
`t + 1` **[std]**.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Cancer_JP_S/` holds nothing but formulas:

```
products/cancer/
  model_point_table.csv        <- inputs live here
  mort_table.csv               incidence_table.csv
  sex_factor_table.csv         survival_table.csv
  lapse_table.csv              hosp_stay_table.csv
  run.py
  model.md  product-spec.md  technical-notes.md  sources.md
  Cancer_JP_S/                 <- formulas only
    __init__.py  _system.json
    Data/__init__.py           (reads the CSVs, once per model)
    Projection/__init__.py     (the by-policy projection)
```

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eight points. **Point 1 is the worked-example anchor cell**; 2–8 exercise the female limb and the 118 terminal age, the 定期 flag with conditioned repeats, a cap that binds with no 先進医療 rider, both ends of the 20–75 issue-age range, 65歳払済, a no-waiver design, and the がん退院一時金 rider | **[std]** throughout — every premium in it is a modelling value, because no rate table for this product is public [REG-R2] [R3] |
| `mort_table.csv` | 第三分野標準生命表2018 proxy by sex, male ages 20–116 and female 20–118 | **[std]** library-wide construction: the quoted rates — 男 q(40) = 0.00076 among them — graduated log-linearly between anchors [R1] [REG-R18] [REG-R19] [REG-R20]; **not a copy** [REG-R21] |
| `incidence_table.csv` | 罹患率 per 100,000 by five-year age band, both sexes, all sites C00–C96, 2023 | Sourced and reproduced verbatim with its attribution [R5] [REG-R29] |
| `sex_factor_table.csv` | The two sourced male / both-sexes ratios, at band midpoints 37.5 and 72.5 | Sourced [R5]; the *interpolation between them* is **[std]** |
| `survival_table.csv` | Five-year relative survival (*go-nen sōtai seizonritsu*, 5年相対生存率) by sex, 2018 diagnoses | Sourced [R6] [REG-R28] |
| `lapse_table.csv` | Annual lapse by policy year, 9% grading to a 3% ultimate | **[std]**, shared unchanged with the medical chassis; anchored to the sourced 5.6% 解約・失効率 [REG-R31] |
| `hosp_stay_table.csv` | Mean stay for 悪性新生物 discharges: all-ages, and the four-band age gradient | Both sourced [R7] [REG-R27]; which basis is read is a switch |

Every row of every assumption table carries a `provenance` column saying which of these
it is. The readers live on the `Data` Space, which takes no parameters, so each file is
read **once per model** rather than once per model point, and `Data.input_dir()`
resolves the directory from `_model.path.parent` at run time. The trade-off is that the
model is not portable on its own: copy `Cancer_JP_S/` without the CSVs and it reads
fine, then fails on first evaluation. What that buys is a diff that shows logic changes
only, and an input that can be swapped in place.

### The mortality table is a construction, not a copy

This is the one place where the library's position has to be stated exactly.
第三分野標準生命表2018 is published by 日本アクチュアリー会 at a stable public URL, free and in full
[R1] [REG-R18] [REG-R19] — anyone can retrieve it and check a rate, a real contrast
with `uklib`, where the CMI tables cannot be read at all without a subscription. **But
the publisher's site terms prohibit reproduction, alteration and transmission to third
parties without written consent** [REG-R21], so `jplib` must not ship a copy.

What is shipped instead is **one [std] table for the whole library**, built on the union
of the individual rates `jplib`'s products quote and attribute: 22 anchor rows across the
two sexes — 男 q(40) = 0.00076 among them, and the terminal rows 男 q(116) = 1.00000 and
女 q(118) = 1.00000 [REG-R18] [REG-R19] [REG-R20] — **graduated log-linearly
(geometrically)** between adjacent anchors, `q(x) = q(a) × (q(b)/q(a))^((x−a)/(b−a))`.

The graduation was chosen over the curve fits the products previously shipped
independently for two reasons. It reproduces **every** anchor exactly, so nothing sourced
is disturbed — which is the property the three incumbent fits all failed, and it is why
nine products could publish the same sourced cell at values up to 34% apart. And it is
locally the Gompertz family, which is the family the publisher itself uses at the older
ages. The model therefore reproduces the quoted rates exactly and asserts nothing else
about the published table; no conclusion about Japanese third-sector mortality follows
from it beyond the anchored rates. The copy in this directory is cut to the ages this
model can reach, **male 20–116 and female 20–118**: the composite's 20–75 issue-age range
run out to each sex's terminal age. Drop a licensed extract in over the same schema —
`sex`, `age`, `mort_rate` — and no formula changes.

`incidence_table.csv` is the opposite case, and the contrast is the point: the
age-banded 罹患率 of 全国がん登録 are reproduced here verbatim with the attribution the dataset
requires [R5] [REG-R29].

## Modules that are off in the base run

Eight of the notes' optional constructions are implemented and held at an inert base
value, so that the base run reproduces the worked example while the machinery stays
visible and testable. `lapse_canc_factor` is the one whose base is inert rather than off.

| Switch | Base | What it does |
|---|---|---|
| `void_adjust` | `False` | Scales `pols_if_init()` by `1 − void_prob()`, de-recognising the 0.037% of policies diagnosed inside the 90-day window — a **de-recognition, not a decrement**, so the premium already collected comes back with the future benefit. The acquisition expense and initial commission are deliberately *not* scaled: they were incurred [S1] [S5] [S10] |
| `sel_lapse_lambda` | `0.0` | Anti-selective lapse on the **incidence** basis, `1 + lam × max(0, w_cum − w_ref)`. Amplified here by the waiver: the healthiest lives are also the only ones still paying. No Japanese evidence was retrieved |
| `repeat_conditioned` | `False` (model point) | Multiplies the relapse hazard by `treat_prob`. Two of the three sourced two-year designs condition the repeat on being under treatment [S7] [S10], so the designs differ by an order of magnitude, not a rounding. True on point 3 |
| `hosp_age_gradient` | `False` | Reads the sourced 35–64 / 65+ / 75+ mean-stay gradient instead of the all-ages 14.4 days [R7] [REG-R27]. The base run takes the all-ages figure because the gradient has four broad bands and the incidence twenty-one narrow ones |
| `mort_age_offset` | `0.0` | Reads the mortality table at `age(t) + 0.5`, interpolating between rows: the table is built for a nearest-birthday age (*hoken-nenrei hōshiki*, 保険年齢方式) basis, so reading it at attained age with the fraction discarded (*man-nenrei*, 満年齢) understates the valuation age by about half a year [R2] [REG-R20] |
| `net_of_cancer` | `False` | Nets the never-diagnosed baseline of `cancer_death_share` = **0.28 [std]**, so cancer mortality inside the table's own rates is not carried twice against the diagnosed excess hazard. 0.28 is a round placeholder with **no observed range**: no document in this product's source set gives 悪性新生物's share of all-cause Japanese mortality — [REG-R28] publishes the cancer death count and no all-cause denominator — so the switch shows the capability, not a calibration |
| `renew_reprice_rate` | `0.0` | Steps the premium at each ten-year renewal on the 定期 chassis flag [S5] [S7]. Point 3 carries the flag with the rate at zero |
| `lapse_canc_factor` | `1.0` | Scales the diagnosed lapse rate off the healthy one. Inert wherever the waiver fires — a waived life has no premium to miss and no surrender value to take — so it reaches a cash flow only on the `waiver_trigger = "none"` and `"disability"` designs [S7] [S10] [S11]. Live on point 7 |

The 定期 flag deserves one further sentence, because what it does *not* do is the
surprise: it projects to the same horizon as 終身, since the renewal is automatic and
neither document states a maximum renewal age. What it changes is the premium — which
would ordinarily close the contract boundary at each renewal. `jplib` records that
tension rather than resolving it, exactly as the medical chassis does.

Two constructions the notes name are deliberately **not** implemented, and the absence
is stated rather than left to inference. A **duration-banded excess hazard** needs
cohort tracking by time since diagnosis that a three-state model does not carry; the
flat hazard overstates late-duration mortality and therefore understates the
long-survivor benefits, and a cure-fraction basis moves the liability one way only — up.
And reinstatement (*fukkatsu*, **復活**) enters as a new model point rather than as a
negative lapse, because the waiting period **re-runs from the 復活日** [S1] [S6]: a
reinstated policy has 90 days of no cover in front of it, and a negative lapse would
hand back cover the contract does not restore and delete an anti-selection control.

## One divergence from the technical notes

`technical-notes.md` carries `disch_rider` in its model point attribute table, but its
cash-flow section defines seven claim lines and none of them is the cancer discharge
lump sum (*gan taiin ichijikin*, がん退院一時金). `product-spec.md` does specify the benefit
— ¥100,000 on discharge from a covered stay of ten or more consecutive days, unlimited
count, with a 30-day re-payment bar [S1] [S2] — and puts it in scope. The model
therefore supplies a **[std]** formula:

    claims_discharge(t) = disch_mult × A × disch_qual_share × h × pols_cancer(t)

with `disch_mult` = 10 from the specification and `disch_qual_share` = 0.60 **[std]**,
the share of cancer admissions whose stay reaches ten days. The 30-day re-payment bar is
not modelled **[std scope]**: at 0.0208 admissions per diagnosed life-month the overlap
is second-order. The rider is off on every model point but 8, so the worked example and
the base run are untouched by it. This is the only cash flow in the model the notes do
not define.

## Sign convention

The notes' `net_cf(t)` is already **income positive** — premiums less claims, less
`expenses` (acquisition and maintenance), less `claim_expenses` deducted explicitly, less
commission — which is the library-wide sign, so there is no outgo-positive `liability_cf`
companion to publish: one stream, one sign, one name.

The asymmetry that defines this product's cash-flow signature sits inside that one line:
**premiums are weighted by `pols_healthy` and claims by `pols_cancer`**, and the two are
disjoint, because the waiver fires on the same first invasive diagnosis that starts
every benefit [S10] [S11]. Weighting the premium by `pols_if` is the single largest
arithmetic error available here — it overstates lifetime income by 6.1% at the anchor
cell — and it is invisible in the first three months, because there the two are equal.
`pols_payer()` is where the choice is made, and it is a *product* choice rather than a
constant: on the `waiver_trigger = "none"` and `"disability"` designs the diagnosed keep
paying and can lapse, which is why `lapse_rate_canc_mth()` is not simply zero either.
Model point 7 runs both reversals.

## Naming

Cells names follow lifelib's `basiclife/BasicTerm_S` wherever it has an analogue —
`pols_*` for policy counts, plural nouns for cash flows, `*_rate` for annual rates and
`*_rate_mth` for their monthly counterparts, `claims(t, kind)` with an uppercase `kind`
string. The full notes-symbol-to-cells mapping lives in the `Projection` docstring,
headed `Notes symbol`. Five cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `pols_open(t)` | `pols_open` | The population **eligible** for a repeat payment, not the population in payment; a fresh relapse is what converts eligibility into a payment |
| `insitu_ev(t)`, `Z(t)` | `insitu_ev` / `insitu_avail` / `insitu_used` | A second benefit tier with its own once-only ledger, on `pols_healthy` alone. `insitu_used` accumulates off the published claim line, not off the recursion, so `check_insitu_ledger` cannot close by construction |
| `M(t)`, `V(t)` | `treat_months` / `adv_paid` | Ledgers **per diagnosed life**, diluted only by `diag_first`. The names say months and yen, which is the dimensional check the treatment benefit needs |
| `w(t)` vs `w_cum(t)` | `lapse_rate_mth` / `lapse_cum` | `lapse_cum` is a proportion of the original cohort, not a running total of the rate, and the loading it feeds moves **incidence**, not lapse |
| *(no symbol)* | `claims(t, "LAPSE")` | Exists and returns zero: there is no surrender value at any duration under 終身払, so a lapse pays nothing. A column of zeros states the product fact where a missing column would hide it. There is no `claims_death` at all |

Ten further names are fixed **across all nine `jplib` products**, so that one concept has
one spelling in the library. This model carries them as follows:

| Name | Means | Note |
|---|---|---|
| `pols_if_at(t, timing)` | The in-force count at `BEF_DECR` / `BEF_LAPSE` / `AFT_DECR` | `BEF_LAPSE` is the sum over the **two states**, each decremented on its own mortality basis, so a blended rate on `pols_if` does not reproduce it. What the vocabulary cannot show here is the movement that defines the product: the three timings are *decrement* timings and a first diagnosis is not a decrement, so `diag_first` changes which benefits and which premium a life carries while leaving `pols_if` identical at all three points. Read `pols_healthy`, `pols_cancer` and `diag_first` for the state movement — `pols_if_at` answers only how many lives are left, never which state they are in |
| `check_net_cf()` / `check_net_cf_resid(t)` | The check that the **published statement** adds up | Rebuilt from the columns of `result_cf` rather than from `net_cf`, so a column wired to the wrong cells shows up in the very table a reader is looking at. The benefit side is swept as every column beginning `claims_` — which it can be, because there is no subtotal column among them |
| `inc_band_at_age(a)` | The five-year 全国がん登録 band containing an **age** | The `*_at_age` suffix marks a lookup keyed by an age, as `mort_rate_at_age` does. `Medical_JP_S` has an `inc_band` keyed by a projection period, and one spelling must not carry two argument meanings across the library |
| `claims(t)`, and **no `claims` column** | The benefit total as a cells, never as a column | `result_cf` publishes the nine `claims_*` splits and no subtotal beside them, so its columns add to `net_cf` as they stand. A statement carrying its own subtotal among its parts stops being additive unless the reader knows which column to skip |
| `expenses(t)` | Acquisition **plus maintenance only** | The claim-handling cost is `claim_expenses(t)`, a cells of its own, deducted explicitly in `net_cf()` and published as its own `claim_expenses` column. The notes' month-by-month traces narrate the two in one arithmetic line; the worked-example table and the policy-year-1 aggregate carry them as two |
| `claim_expenses(t)` | ¥5,000 per diagnosis trigger, ¥3,000 per admission | On the diagnosis and admission counts, where `expenses` is on `pols_if` — different weights, so publishing one column would hide a real movement |
| `prem_period_type()` | The premium-paying period as a **category**, `whole_life` or `to_65` | `prem_period` is reserved for a duration in the model's own grid unit. The model point *column* keeps the name `prem_period` |
| `premium_mth_pp()` | The **monthly** office premium per policy | `premium_pp` is an annual per-policy premium elsewhere in the library; this grid's step is the payment interval |
| `mort_rate_at_age(a)` | The shipped table rate keyed by **age**, which may be fractional | `mort_rate_base(t)` is the name for a table rate in period `t`, which this model does not need: `mort_rate(t)` reads `mort_rate_at_age(age(t) + mort_age_offset)` directly |
| `mort_be_factor` | The multiplier turning the shipped valuation table into the projection basis | 1.25 here. Named for what it does — a best-estimate factor — and not to be confused with an actual-to-expected ratio, which is a different quantity |

## Standardizations used

Everything in this list is **[std]**, and each is marked so at its definition in the
notes and in the model: the whole post-diagnosis survival model — `mu_ex = −ln(S5)/5`
from a sourced 5年相対生存率 [R6] [REG-R28], held flat for the diagnosed lifetime, and
added to the baseline rather than replacing it; the relapse hazard `rel_rate` = 0.06
p.a., which gives 1.485593 diagnosis payments per diagnosed life and has no source and
no observed range; the sex split of the incidence basis, a two-point interpolation
between two sourced ratios [R5] read at the band midpoint and clamped; `treat_prob` =
0.10 and the cohort-average ledger behind the 60-month cap; `hosp_rate` = 0.25
admissions per diagnosed life-year, derived from two sourced counts [R7] [R5] on a
construction in which the population cancels — 38.98 inpatient days per diagnosed person
over a cancer lifetime, the single most useful number for sanity-checking an
implementation; `surg_per_hosp` = 0.35 payable cancer surgeries per admission, carried from
the medical chassis so the two products do not disagree about the same statistic, and
`surg_per_insitu` = 0.80 recognised in an in-situ diagnosis month; `outp_days` = 1.10,
resting on an unsourced 250 outpatient operating
days and an unsourced 25% qualifying share, a factor-of-four uncertainty between them;
`adv_freq` = 0.012 at `adv_sev` = ¥600,000; `mort_be_factor` = 1.25, the reciprocal of 0.80, a
round value inside the sourced 70–85% risk-theory band [R2] [REG-R20]; the whole expense and
commission scale, carried from the medical chassis because no Japanese cancer expense or
commission scale is public; the ¥3,000 premium; and mortality-before-lapse as the
processing order. The first three are the levers: the survival basis is the assumption a
medical model does not have at all, and three of the eight benefit streams are integrals
over it.

### The clamp on the sex factor

`sex_factor(a)` is clamped to `[0, 2]` **[std]**, and the clamp is not decoration. The
linear form reaches 2 at age 98.87, and above that the female limb `2 − f_male` goes
**negative** — at the 100+ band midpoint of 102.5 it would give −0.086 × the band rate,
on a female projection that runs to 118. The admissible domain of a construction whose
two limbs must sum to twice the band rate and must both be non-negative is exactly
`f_male` in `[0, 2]`, so that is where it is clamped; it binds on the 100+ band alone,
where it takes female incidence to exactly zero and caps male incidence at twice the
band rate. That is a discontinuity, and it is the construction's own behaviour made
admissible rather than a new approximation: the construction is already 6% below the
sourced female rate at 70–74. Replacing `sex_factor_table.csv` and the interpolation
with the by-sex age-band grid from the same workbook removes both the clamp and the
error, and it is the first thing a serious user should do.

## Tests

`tests/test_model_conventions_jp.py` asserts the house style over the whole registry.
`tests/test_cancer_jp.py` asserts this product:

- the notes' six-row worked example and its four month-by-month traces, hard-coded, to
  the precision the notes display — money to ¥0.01, `pols_if` and the healthy split to
  six decimals, the diagnosed state to eight, the ledgers to four — plus the
  policy-year-1 aggregates, the ¥16,035.00 of benefit per diagnosed life-month and its
  five components, and the relapse hazard's stated calibration target;
- every pitfall the notes list, one test each and named after it, because every one of
  them is a way an implementation can look right and be wrong;
- the shipped mortality table: **all twenty** sourced rates inside the age range this
  model reads, pinned to the digits the publisher shows, plus the log-linear graduation
  between them and the exact age span of the file. A quoted rate that the shipped table
  cannot reproduce is a library defect, not a rounding, so it is asserted rate by rate;
- the expense split — `expenses` is acquisition plus maintenance, `claim_expenses` is a
  line of its own, and `net_cf` deducts both;
- the seven `check_*` roll-forward and ledger identities, on every one of the eight
  model points;
- each optional module in **both** positions, off and switched on;
- and the structural product facts — the whole-of-life horizon set by the mortality
  table's terminal age, the three states partitioning the in-force, the crossing sex
  curves and the clamp, 65歳払済, the no-waiver design, and the treatment cap that binds.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #jplib-cancer-r1
[R11]: #jplib-cancer-r11
[R2]: #jplib-cancer-r2
[R3]: #jplib-cancer-r3
[R5]: #jplib-cancer-r5
[R6]: #jplib-cancer-r6
[R7]: #jplib-cancer-r7
[REG-R18]: #jplib-reg-r18
[REG-R19]: #jplib-reg-r19
[REG-R2]: #jplib-reg-r2
[REG-R20]: #jplib-reg-r20
[REG-R21]: #jplib-reg-r21
[REG-R27]: #jplib-reg-r27
[REG-R28]: #jplib-reg-r28
[REG-R29]: #jplib-reg-r29
[REG-R31]: #jplib-reg-r31
[std]: #jplib-std
<!-- END generated citation links -->
