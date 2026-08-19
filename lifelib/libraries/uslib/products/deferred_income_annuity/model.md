# Implementation Notes

**Status:** Draft, 2026-08-14. Built from
[`products/deferred_income_annuity/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md). The income
phase is the payout chassis of
[`products/immediate_annuity/technical-notes.md`](../immediate_annuity/technical-notes.md),
implemented in [`SPIA_US_S`](../immediate_annuity/model.md) — this model carries that
model's names for every shared concept.

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual elements — the paid-up income slice each premium buys at then-current
> rates, the 100% return-of-premium deferral death benefit, the one-time ±5-year income
> start date adjustment, six months of payment acceleration, commutation with the
> life-contingent tail preserved, the QLAC restriction set and its $210,000 2026 premium
> limit, the $50 maintenance expense escalated at 2.5%, and the absence of any lapse or
> annuitization decrement — are sourced. **The entire pricing kernel is not.** No
> purchase-rate table exists: the Insurance Compact expressly relieves the insurer of
> disclosing the deferral-period mortality and interest basis [R13 §1.B(1)(a)](#uslib-deferred_income_annuity-r13), so the
> 4.75% pricing rate, the 6.0% expense and profit load, the mortality table, the
> illustrative payout and return-of-premium factors, the 100 bp repricing spread and the
> 50 bp commutation margin are all **[std]** constructions. Replace them with company
> data before drawing any conclusion from the numbers.

## Run it

```bash
python products/deferred_income_annuity/run.py
python products/deferred_income_annuity/run.py 5      # life with installment refund
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/deferred_income_annuity/DIA_US_S")
model.Projection[1].result_annual()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell —
Female 60 ANB, nonqualified, Life with Cash Refund, $100,000 at issue plus $50,000 at
the start of policy year 6, income start at attained age 80. `result_cf()` returns a
`DataFrame` of monthly cash flows indexed by `t`; `result_pols()` the survival
probabilities and payment factors behind it; and `result_annual()` the technical notes'
own annual display grid, which is what the worked example prints.

The model and its `Projection` Space both carry docstrings — `model.doc` describes the
product and the projection basis, and `model.Projection.doc` holds the full mapping
between the technical notes' symbols and the cells names.

## Monthly, and `t` is 0-based

`t` counts **policy months from issue**, running `0, 1, 2, … proj_len()`. Monthly is
what the notes set ("Projection frequency. Monthly, indexed `t = 0, 1, 2, …` from
issue") and what the product forces: the modal payment frequency is monthly, and both
the 13-month minimum deferral and the 13-month premium cut-off are expressed in months.

**The 0-based index is a deliberate departure from `Term_US_A` and
`SPIA_US_S`, which are 1-based.** The reason is that in these notes `T` is a
month *index*, not a count: the anchor cell's income start month is `T = 240` and its
premiums fall at months 0 and 60. Renumber to a 1-based grid and `T = 240` silently
becomes the 241st month, moving every option window, premium date and payment date by
one. Month 0 is a real projected month here — the first premium arrives at its start,
deaths occur during it, the maintenance expense accrues in it — not a recursion base
case.

Two consequences worth holding on to:

| | `SPIA_US_S` (1-based) | `DIA_US_S` (0-based) |
|---|---|---|
| `lives_if(t, life)` | survival over `t` elapsed months | **the same** — survival over `t` elapsed months, i.e. alive at the *start* of month `t` |
| `lives_death(t, life)` | `l(t−1) − l(t)` | `l(t) − l(t+1)` |

The survival cells means exactly the same thing in both models; only the death density
shifts, because month `t` spans elapsed `[t−1, t)` there and `[t, t+1)` here.

`proj_len()` runs to the limiting age ω = 120 of the **youngest** covered life — the
Reference `omega_age`, 719 months on the anchor cell's age 60 — or to the end of the
guarantee period if that is later.

## Inputs are external files

The six input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `DIA_US_S/` holds nothing but formulas:

```
products/deferred_income_annuity/
  model_point_table.csv        <- inputs live here
  premium_schedule.csv
  mort_table.csv
  improvement_scale.csv
  payout_factor_table.csv
  rop_factor_table.csv
  run.py
  README.md
  DIA_US_S/     <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-contract projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps `input.xlsx` beside the model
and reads it at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory
and no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate
ItemSpace with its own cells cache. Readers placed there would re-read every file for
every contract. They live instead in an unparameterized **`Data`** Space, which
`Projection` references as `data` — so each file is read once per model no matter how
many contracts are projected. `Data.input_dir()` resolves the location from
`_model.path.parent` when the model is read, so it works wherever the repository is
checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `premium_schedule_file` | `premium_schedule_table()` | `premium_schedule.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `improvement_scale_file` | `improvement_scale()` | `improvement_scale.csv` |
| `payout_factor_file` | `payout_factor_table()` | `payout_factor_table.csv` |
| `rop_factor_file` | `rop_factor_table()` | `rop_factor_table.csv` |

**The trade-off:** the model is not portable on its own. Copy
`DIA_US_S/` without the CSVs and it will read fine, then fail on first
evaluation. What you gain is that a diff of the model shows logic changes only, and an
input can be edited or swapped in place — point `Data.mort_table_file` at another
same-schema file and the projection follows, with no formula change.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Seventeen contracts. **Point 1 is the worked-example anchor cell**; points 2 and 3 are the two readings the notes leave open; point 4 is the death-benefit fork; 5–10 walk the payout forms, joint triggers and COLA; 11–12 a compliant and a breaching QLAC; 13–15 the three in-force options; 16 generational mortality; 17 advance timing | anchor cell **[std]**, technical notes "Worked example" |
| `premium_schedule.csv` | One row per premium slice, keyed by `point_id`. A separate table because a flexible-premium DIA takes an unbounded number of slices | anchor schedule **[std]** |
| `mort_table.csv` | Annuitant mortality by age and sex. Ages 60–84 female are **band-constant rates that reproduce the notes' five-year survival anchors exactly**; everything else is a geometric continuation, and male rates are the female curve set forward three years | **[std]**, *not* the 2012 IAM Basic table — see below |
| `improvement_scale.csv` | Generational improvement by age and sex, 1% grading to 0 at age 105 | **[std]** illustrative, *not* Projection Scale G2 |
| `payout_factor_table.csv` | `a^(m)` at the income start age by `(age, sex, payout_form)`. The `(80, F, CR)` row is the notes' own **8.60** | worked example **[std]**; the other rows computed from `mort_table.csv` by equation (2) |
| `rop_factor_table.csv` | `A_rop` by `(issue_age, sex, deferral_years)`. The `(60, F, 20)` and `(65, F, 15)` rows are the notes' **0.157900** and **0.180200** | worked example **[std]**; the other rows the mid-band approximation of equation (3) |

The mortality table deserves a sentence of its own. The notes forbid embedding licensed
tables and prescribe the 2012 IAM Basic table with Projection Scale G2 — which is in any
case printed in no source this library holds, A-821 printing the *loaded* Period Table
only [REG-R153]. What is shipped instead is an illustrative curve chosen so that the
model reproduces the notes' worked example: over ages 60–84 its rates are the constant
annual rates implied by the notes' five-year survival anchors (0.975, 0.920, 0.838,
0.715 from age 60, and 0.780 over 80–85), so `_5p_60`, `_20p_60`, `_15p_65` and every
monthly value between them come out exactly. Past age 85 the notes give nothing, so the
curve continues geometrically at a rate **calibrated so that equation (2) at the income
start age returns 8.600** — the notes' own illustrative payout factor. That is what the
notes mean by calling their factors "mutually consistent"; a test pins it.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` where those
have an analogue, and — for the whole income phase — they follow `SPIA_US_S`
exactly, because a DIA in payment *is* a SPIA. `payment_factor`, `payment_factor_life`,
`certain_floor`, `certain_mths_eff`, `certain_mths_refund`, `annuity_pp_sched`,
`annuity_pp`, `annuity_pp_paid`, `cum_annuity_pp`, `lives_if`, `lives_death`,
`lives_if_last`, `lives_death_last`, `payment_surv_mth`, `commute_frac_cum`,
`commuted_value`, `commutations`, `claim_pp(t, kind)`, `claims(t, kind=None)`,
`result_cf`, `result_pols` are all the chassis' names with the chassis' meanings.

The technical notes use compact actuarial symbols; the full mapping lives in the
`Projection` Space docstring. Eight cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l` vs `L` | `lives_if` / `payment_factor_life` | Survival probability and payment factor differ only by case |
| `L` again | `expense_load` | `L` is *also* the expense and profit load in equation (4) |
| `B(y)` in the chassis | `annual_income(t)` | Indexed by **month**, not policy year: a DIA's income changes when a *premium* is paid |
| `n_g` | `guarantee_mths_pricing()` / `guarantee_yrs()` / `certain_mths_eff()` | Three different quantities the notes all call `n_g` — see below |
| `theta_cum` | `commute_frac_cum` | Inherited from the *immediate-annuity* notes: `theta` appears nowhere in the DIA notes, which write equations (13) and (14) with no symbol for the fraction at all |
| *(no symbol)* | `surv_to_payout()` | The weight the chassis has no need for — see below |
| *(no symbol)* | `commute_weight()` | Its mirror image at the commutation date — see below |
| `annuity_year` in the chassis | `issue_year` | A SPIA's annuity date is its issue date; here they are twenty years apart, so the generational anchor is named for the one that matters |

Three names are the library's rather than this model's, and are spelled its way here:
the mortality A/E deviation factor is **`mort_ae_factor`**, the limiting age of the
mortality table is **`omega_age`**, and every self-check is a **no-argument cells
returning a bool** over all projected `t` — `check_lives_roll_fwd()`,
`check_income_roll_fwd()`, `check_payment_factor()`, `check_commutation_value()` — each
with a `check_*_resid(t)` companion returning the signed float residual at one `t`. The
bool is what a cross-model test calls; the residual is what a debugging session reads
after it fails, and the bool is defined in terms of it so the two cannot disagree. There
is no `check_av_roll_fwd()` here, because there is no account value to roll forward.

## `surv_to_payout` and `commute_weight` — the chassis formulas that do not carry across

`SPIA_US_S` writes the payment factor as `Φ(t) = max(C(t), L(t))` with `C(t)` a
bare 0/1 indicator, and the DIA notes inherit that wording without adjusting: "`L_pay(t)`
is the form-specific payment-survivorship weight defined in the immediate-annuity notes:
`l(t)` for a life-only payment, **certain inside a guarantee period**, …".

A SPIA is already in payment, so its guarantee is certain full stop. **A DIA's is not.**
The guarantee period only begins if the contract reaches the income start date; an
annuitant who dies during the deferral takes the return-of-premium benefit and no
instalment is ever paid. On an expected basis the certain instalments therefore carry
`l_last(T)`, and this model writes

```
payment_factor(t) = max(certain_floor(t) * surv_to_payout(), payment_factor_life(t))
```

On the anchor configuration `l_last(240) = 0.715`, so copying the chassis formula across
unchanged would put the payment factor at 1.000 instead of 0.715 on every guaranteed
instalment of a period-certain or installment-refund contract — **a 39.9% overstatement
of the guaranteed leg**. It is the same weight equation (1) applies to
the pricing side through `_d p_x`, and the immediate-annuity notes' own warning is not to
carry their recursions across unexamined. A test pins `Φ = 0.715` inside the guarantee on
both such model points.

This does not touch the anchor cell, whose cash-refund form has no certain floor at all.

**`commute_weight` is the same idea one date later.** A commutation is exercised by an
owner who is *alive* at `t_c` [S4], so it can only extinguish the guaranteed instalments
of the `l_last(t_c)` sub-cohort — while the guarantee itself belongs to the whole
`l_last(T)` cohort that reached the income phase. On point 15 those weights are
**0.680338** and **0.715000**. Suppressing the guarantee with the second and paying the
commuted value with the first cancels 4.85% more guaranteed liability than the commuted
value buys — 6,898.37 of present value at `i_c` on that cell — so the model splits the
cohort explicitly:

```
E[income](t) = pols * [ inst(t) * (Φ(t) − w_c(t))      not commuted
                      + inst_paid(t) * w_c(t) ]        commuted
```

The economics is concrete: a contract whose annuitant died between `T` and `t_c` is
paying its period-certain guarantee to a beneficiary and could not have commuted at all.
`check_commutation_value()` asserts the exchange closes — the present value at `i_c` of
the instalments suppressed equals the commutation paid — and a test pins it.

## The joint deferral death benefit is priced on the curve it is paid on

Equation (3) writes `A_rop` on a single life `x`, and the notes never restate it for a
joint contract even though equations (15) and (16) both carry a `P·A_rop` term. This
model resolves that gap by pricing the benefit it actually projects.

On a joint contract the return of premium attaches to the **last** death — "if one
annuitant dies in deferral the contract continues on the option chosen at issue" [S2], so
the benefit falls due only when the contract ends, and `claims(t, "DEATH")` is weighted by
`lives_death_last(t)`. `rop_factor_calc` therefore runs the mid-band approximation over
`lives_if_last`, not over the primary life's curve. On point 8 (F60 + M63) the two
differ by a factor of two and a half:

| Exposure | 20-year probability | `A_rop(0)` | Joint income `B` |
|---|---|---|---|
| primary life dies | 0.285000 | 0.161605 | 42,358.20 |
| **last death** (what is projected) | 0.128767 | **0.064820** | **47,711.31** |

Pricing the primary life's density while projecting the last death's would charge for
two and a half times the exposure and understate the joint income by 11.2% — which is
the notes' own listed pitfall ("its cost belongs in the purchase rate (4) *and* in the
projected cash flows") read strictly, as requiring the *same* benefit in both places. A
test reconciles the present value of the projected death claims against
`Σₖ Pₖ·v^tₖ·l_last(tₖ)·A_rop(tₖ)`, to the accuracy of the five-year mid-band
approximation. **On a single-life contract `l_last` is the primary curve, so nothing in
the worked example moves.**

The alternative reading — pay the deferral death benefit on the *first* death and price
it there — is available in the notes through the spousal-continuation switch, and is not
taken: the base is 100% election of the death benefit on a contract that [S2] says
continues. Both the pricing and the projection are **[std]** on this point.

## Cash refund prices as certain-and-life and projects as life-contingent

`n_g` is three different things in the notes and conflating them double-counts the
guarantee:

- **`guarantee_mths_pricing()`** — the guarantee fed into the *pricing kernel* by
  equation (5), `n_g = CP(T)/B`. It puts `B` on both sides, so it is resolved by
  fixed-point iteration from a life-only start, the notes' own prescription and their
  listed pitfall ("failing to iterate leaves a systematic bias"). 40.669 months on the
  anchor cell.
- **`guarantee_yrs()`** — the same quantity once `B` is known, the **3.3891 years** the
  worked example quotes, exhausting the cash-refund guarantee at attained age ≈ 83.4.
- **`certain_mths_eff()`** — the *projection's* certain floor, which is **zero on a cash
  refund**. A cash refund is a lump-sum shortfall paid at death, not a stream of
  guaranteed payments. Equation (5) treats it as certain-and-life for *pricing* only —
  the notes say so outright, offering equation (6) as the exact alternative — and
  carrying that into the projection would pay the guarantee twice.

Installment refund is the form that really does pay a certain stream, and there
`certain_mths_eff()` is `certain_mths_refund()`, searched from the instalment schedule:
41 months on this cell, because 40 instalments fall short of the 150,000 of cumulative
premiums and 41 overshoot it. **[std]** — the monthly grid rounds the guarantee *up* to a whole
instalment rather than trimming the last one, which is what the notes' "exactly a
certain-and-life annuity with `n_g = CP(T)/B`" framing implies. `SPIA_US_S`
trims instead; that is a divergence between the two notes files, not a bug in either
model.

## The `A_rop(60, 20)` divergence is shipped, not resolved

The notes state that their illustrative return-of-premium factors were "computed from
the same survival anchors with a mid-band death-timing approximation", and print
`A_rop(60, 20) = 0.157900` and `A_rop(65, 15) = 0.180200`. Run that recipe on those
anchors and:

| Slice | Notes print | Recipe gives | Agreement |
|---|---|---|---|
| age 65, 15-year deferral | 0.180200 | **0.180241** | to four decimals |
| age 60, 20-year deferral | 0.157900 | **0.161605** | not to two |

One of the two is arithmetically consistent with the stated recipe and the other is not.
Rather than choose, the model ships both: `rop_factor_table.csv` carries the printed
factors and model point 1 reads them, reproducing the worked example; model point 3 is
identical except that `factor_basis = "formula"` computes them, and its income comes out
at 44,106.53 against the worked example's 44,259.65. A test pins the gap open in both
directions. Neither value is "right" — both are **[std]**.

Note what this isolates. The payout factor agrees on both bases: the shipped mortality
curve is calibrated so that equation (2) returns the notes' 8.60, exactly as the notes'
claim of mutual consistency requires. `A_rop(60, 20)` is the one place left over.

## The purchase-rate rounding is worth 3.6 cents

The worked example computes `B₁ = 100,000 × 0.321765 = $32,176.50` from a purchase rate
printed to six decimals. At full precision `pr₁ = 0.3217647` and the same premium buys
`$32,176.47`; over both slices the difference is **3.6 cents** on a `$44,259.65` income —
enough to fail a cent-level assertion on the two `E[income]` rows.

The model point column `purchase_rate_dp` carries the convention: 6 on point 1, blank
(full precision) on point 2. Point 1 reproduces the notes to the cent, point 2 shows what
the rounding is worth, and a test asserts both. Purchase rates really are administered to
a finite precision, so neither reading is unreasonable — but the choice is a **[std]**
convention and should not be invisible.

## What the in-force options implement, and what they do not

All three options are implemented as **deterministic single exercises** named on the
model point and off by default:

- **Income start date adjustment** — equations (10) and (11), actuarial equivalence at
  the exercise month on `i_e = Baa − 100 bp`. Point 13 defers the start by five years at
  month 120 and the income rises by a factor of 1.880. The two refinements the disclosed
  recipe does not mention — that the ROP exposure changes with the deferral length and
  that `CP` is unchanged so the derived guarantee period shifts — are **flagged rather
  than modeled**, as the notes require.
- **Payment acceleration** — six monthly payments in one sum, then five months without,
  with equation (12)'s cost reported by `accel_cost()`. It is a timing shift, expressly
  "not a liquidity feature"; modelling it as a withdrawal is a listed pitfall. The six
  instalments are all carried at **one** payment factor — the lump sum's own date, so
  the five pulled forward are unconditional on surviving to their scheduled dates, which
  is exactly the mortality element equation (12) prices. The test asserts the lifetime
  invariant rather than the block: point 14 is point 3 with the acceleration and nothing
  else, and their whole-of-payout income outgo differs by **153.52** on a 372,585 base —
  `inst × Σⱼ [l(t_a+1) − l(t_a+1+j)]` exactly. Equation (12)'s interest element does not
  appear because the projection is undiscounted, which is why 153.52 sits below
  `accel_cost() = 435.11` rather than on top of it. Paying those five instalments to the
  whole *initial* cohort would put 6,079.84 there — fourteen times (12)'s cost, and a
  withdrawal in all but name.
- **Commutation (extended case)** — equations (13) and (14), one-sided in rates per the
  Compact's stated intent. After a 100% commutation the guaranteed payments of the
  commuting cohort stop and, if the annuitant is alive when the would-be guarantee period
  ends, **income resumes until death**: point 15's income drops from 1,640.68 to 79.54 a
  month over months 252–359 and returns to 919.16 at month 360. The 79.54 is not a
  rounding residue — it is the guarantee still running to the beneficiaries of contracts
  whose annuitant died between `T` and `t_c`, the cohort that could not have commuted.

**What is not implemented is the incidence and selection layer** — the notes' 1.5% p.a.
adjustment take-up `h_adj` with its 60/40 direction split and `M_def`/`M_adv` rate
multipliers, the 0.90/1.10 health-selection multiplier `sel_mult`, the 2% p.a.
acceleration take-up `h_acc` and the 1.5% p.a. commutation take-up `h_com`. Each of them
splits the model point into an exercised and an unexercised cohort, which needs cohort
tracking this model does not carry. They are also, per the notes, the assumptions with
no experience behind them at all — and AG 33 **prohibits** experience-based elective
incidence in a CARVM run, so feeding them into a reserve is a defect rather than a
refinement. The model docstring lists them, along with equation (6)'s exact cash-refund
factor, equation (16)'s convertible-joint pricing, spousal continuation, premium
admissibility limits and every valuation layer.

## The QLAC overlay generates no cash flows

It caps premiums, restricts forms, constrains `T`, disables features and raises
compliance flags — nothing more. `qlac_room(t)` is the 2026 limit of **$210,000** less
cumulative premiums less premiums paid to any other intended QLAC, and `qlac_flags()`
returns the conditions the contract fails. There is **no percentage-of-account-balance
test**: SECURE 2.0 § 202(a)(1) directed its elimination and the codified text has no
percentage rule, so a 25% test, a $125,000 or $130,000 cap and an RMD age of 70½ are all
superseded arithmetic that pre-2023 insurer guides still print. Point 11 sits exactly on
the limit and flags nothing; point 12 pays $250,000 and flags the breach — and projects
identically apart from the premium itself, which is the point.

## Standardizations used

Everything in this list is **[std]**: the pricing rate `i_p = 4.75%` and the expense and
profit load `L = 6.0%`; the mortality table and its post-age-85 continuation, the
improvement scale, and the A/E factor `mort_ae_factor` of 1.00; the illustrative payout and
return-of-premium factors and the choice to round the purchase rate to six decimals; the
equation (5) approximation for both refund forms; arrears timing and the end-of-month
death benefit; the deferral death benefit attaching to the **last** death on a joint
contract **and `A_rop` priced on that same last-death curve**, equation (3) being written
on a single life and never restated for a joint contract; the acceleration lump sum
carrying the payment factor of its own date on all six instalments, and the commutation
extinguishing only the `l_last(t_c)` cohort's guarantee; the 100 bp repricing spread and
the assumption of no Baa movement since issue;
the 50 bp commutation margin (also **[unverified]**); six accelerated payments; the
maintenance expense weighted by `l(t)` rather than by the chassis' `max(C, l_alive)`;
rounding the installment-refund guarantee up to a whole instalment; and the anchor cell
itself. Sourced, by contrast: the income-slice mechanic and its purchase-rate rule
[R13 §3.B(1)(b)](#uslib-deferred_income_annuity-r13) [S3], the 100% return-of-premium deferral death benefit [R13 §3.I(1)(a)](#uslib-deferred_income_annuity-r13),
the ±5-year adjustment and its disclosed repricing inputs [S1] [S2], the six-month
acceleration [S1] [S4], commutation with the tail preserved [S4] [S5], the whole QLAC
restriction set [R1] [R2] [R3], the $50 maintenance expense escalated at 2.5% [R9], and the
absence of lapse and annuitization decrements [R9].

**There is no lapse decrement, and adding one is a defect.** "Not conservatism — there is
no surrender benefit to elect. A nonzero lapse assumption in a DIA model is a defect, not
a margin." There is no `lapse_rate`, no `pols_lapse`, no surrender cash flow row, no
account value and no credited rate anywhere in this model, and a test asserts that no
cells or Reference name even looks like one.

## Tests

`tests/test_deferred_income_annuity_us.py` asserts all nine rows and every column of the
notes' projection table, the slice pricing of equation (4) against each printed
intermediate factor, the derived guarantee period, the 21.2% death-benefit fork, the
policy-year-6 trace, the survival anchors, both shipped divergences, the arrears payment
timing and the full-`CP(T)` refund in the first payment month, the certain floor's
conditioning on reaching the income phase, the installment-refund derived period, the
joint triggers, the joint `A_rop` reconciliation against the projected death claims, the
COLA, all three in-force options — including acceleration's lifetime-outgo invariant and
the commutation exchange identity — the QLAC overlay, the generational construction, the
in-force and income roll-forwards, that the cross-model names (`mort_ae_factor`,
`omega_age`, the no-argument `check_*()` bools and their `check_*_resid(t)` companions)
are the library's canonical ones, and that every model point projects.

```bash
python -m pytest tests/test_deferred_income_annuity_us.py -q
```

<!-- BEGIN generated: tools/gen_scaffolding.py -->
## Verifying this copy

`tests/test_deferred_income_annuity_us.py` asserts this model against the worked example in
[technical-notes.md](technical-notes.md), and it ships **inside this library** — so it runs
against the copy you are holding, including any changes you have made to it:

```bash
python -m pytest tests/test_deferred_income_annuity_us.py -q
```

The whole suite, all twelve models and the shared conventions, is `python -m pytest tests -q`.
If you change an assumption and a test goes red, the worked example in the notes and the
model have parted company — which is the question this library exists to let you ask.
<!-- END generated -->

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uslib-deferred_income_annuity-r1
[R2]: #uslib-deferred_income_annuity-r2
[R3]: #uslib-deferred_income_annuity-r3
[R9]: #uslib-deferred_income_annuity-r9
[REG-R153]: #uslib-reg-r153
[std]: #uslib-std
[unverified]: #uslib-unverified
<!-- END generated citation links -->
