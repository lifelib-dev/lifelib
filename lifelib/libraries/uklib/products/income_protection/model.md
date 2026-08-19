# Implementation Notes

**Status:** Draft, 2026-08-15. Built from
[`products/income_protection/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the deferred period menu, the two-band
> maximum-benefit formula, escalation capped at 10% with a ×1.5 premium multiplier
> continuing in claim, waiver of premium from benefit start, linked claims within 52
> weeks, expiry without value. Every **rate** is a **[std]** standardization: the CMI
> IP11 Series is restricted to CMI Authorised Users [R1] [R2] [R5] [REG-R22], so the
> inception, recovery and in-claim mortality rates shipped here are proxies **shaped
> like** IP11 that carry no CMI authority, and the premium is a placeholder. Replace
> them with a licensed basis first.

## Run it

```bash
python products/income_protection/run.py       # the active-lives anchor cell
python products/income_protection/run.py 2     # the claims-in-payment worked example
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/income_protection/IP_UK_S")
model.Projection[1].result_cf()
```

## The only multiple-state model in the library

Every other model here runs a single in-force probability down through decrements. This
one carries a **three-state** population:

```
        inception ι                recovery ρ
   H ─────────────────────────▶ S ─────────────────────────▶ H     (return_to_h basis)
   │                            │
   │ mortality q_H              │ mortality q_S
   │ lapse w                    │
   ▼                            ▼
   D / lapsed                   D
```

That structure is not decoration: it is the structure the CMI's own graduations use, and
it is why income protection has **two** experience bases rather than one — claim
*inception* rates out of H, and claim *termination* rates out of S, the latter split into
recovery and death. Lapse is a further exit from H; **lives in claim never lapse**
**[std]**, since their premiums are waived and the benefit in payment is the most
valuable thing they own.

### The in-claim population is two-dimensional

Termination rates depend on how long the claim has already run — 40% a year at duration
one falling to 5% from duration five in the shipped basis — so the model tracks
`l_S(t, z)` cohort by cohort. **Collapsing that to a single bucket with a
duration-independent termination rate materially misstates claim run-off**, and is the
notes' first-listed pitfall: the duration gradient *is* the defining feature of income
protection terminations.

`sick_cohorts(t)` holds the whole vector for one month and is the model's only
list-valued cells. The alternative — a two-argument `pols_sick_dur(t, z)` recursion —
would be `proj_len() × max_dur()` separate cells, 130,000 of them on the anchor cell,
each with its own cache entry. Keeping the vector in one cells per month makes it
`proj_len()` cells with a loop inside; `pols_sick_dur(t, z)` reads an element out of it,
so the notes' two-dimensional object is still addressable by name. `claim_rate_vectors()`
is the same trick for the three per-duration rate vectors, and takes the anchor cell from
about sixteen seconds to five.

**The shipped termination basis suppresses the age dimension** **[std]**. IP11 is
two-dimensional in age and duration, with claimant mortality duration-dependent to five
years and age-only beyond, and it also has a "run-in" of *increasing* recovery rates over
the first weeks of claim for the shorter deferred periods, which annual duration-year
granularity smooths away. A licensee restoring both dimensions changes
`termination_table.csv` and two lookups, and nothing else.

## The deferred period is in the inception basis, not a fourth state

`ι` is a claim *payment* inception rate specific to the policy's deferred period —
exactly the quantity the CMI publishes per deferred period [R1] — so:

- a sickness spell that recovers inside the deferred period never leaves H;
- a life sick but not yet in payment stays in H and **keeps paying premiums**, which is
  what the contract's waiver-from-payment-start convention says.

No separate "sick, not yet in payment" state is needed and the lag between onset and
payment is absorbed into the calibration of `ι`. Dual deferred periods and sick-pay-linked
NHS/teacher deferreds would need spell-level modelling and are out of scope.

## Two kinds of model point, and where recoveries go

The notes give two calculations. The model point's `recovery_basis` column says which one
a cell runs, and `status` says which state the population starts in:

| `recovery_basis` | Recovered lives | What it is | Model points |
|---|---|---|---|
| `return_to_h` | re-enter H, resume paying premiums, are again exposed to inception | the **active-lives** projection, the notes' processing order step 5 | 1, 3, 4, 6, 7 |
| `exit` | leave the model | the **disabled-life annuity** of the claims-in-payment valuation, and the basis the worked example is computed on | 2, 5 |

Keeping it a column rather than deriving it from `status` matters, because the choice is
a valuation question and not a property of the cell: a claims-in-payment reserve is the
disabled-life annuity, but a full contract-boundary best estimate for the same policy
would carry the post-recovery active phase as well. Model point 7 is point 2 on
`return_to_h`, and its benefit PV is about 2% higher, because recovered lives can and do
claim again.

**Linked claims limitation.** Contractually a same-cause recurrence within 52 weeks
restarts payment with **no new deferred period**, and returning recovered lives to the
standard inception basis ignores that — it understates re-inception at short horizons.
The refinement is a post-recovery flag carrying a loaded inception rate for twelve
months; it is not implemented, and the notes name the same gap.

## Premiums come from H alone

`premiums(t)` is carried on `pols_active(t)` and **never** on `pols_if(t)`. Premiums are
waived from the start of benefit payment [S5] [S7] [S10] [S11], so projecting income from
lives in claim overstates it by the whole in-claim population — the notes' second-listed
pitfall. `result_cf()` publishes `pols_active` beside `pols_if` for exactly this reason:
the difference between the two columns is the population whose premiums are waived.

Note the asymmetry escalation creates: the benefit escalates in claim and the premium
that would have paid for it does not, which is why the escalation option is
inflation-sensitive on precisely the claims that are longest. The 10% cap is an embedded
inflation option the insurer has written.

## Benefit in arrears, and the month a claim starts

A claim incepting at the end of month `t` seeds cohort `z = 1` and receives its first
payment at the end of month `t + 1`. So the benefit is paid on `pols_sick_surv(t)` — the
cohorts already in payment at the start of the month that survived it — and not on
`pols_sick(t)` plus new inceptions. Paying the new inceptions would hand over a full
month's benefit at the instant payment starts and break the equivalence with the
inception-annuity decomposition of the same projection.

The contractual daily pro-rating of partial claim months is replaced by whole-month
payment **[std]**: a life recovering mid-month receives nothing for that month here, and
a pro-rated amount in reality.

## Expiry truncates everything

All cover and any claim in payment terminate at the policy end date with no value.
`pols_maturity(t)` is that termination, non-zero only in the last month, and it is what
makes the in-force roll-forward close. **An untruncated disabled-life annuity materially
overstates the liability for claims incepting near expiry** — model point 5 is a claim at
duration 30 months on a policy with 15 years to run, and its benefit stream stops dead at
`proj_len()`.

## Amount payable is not the chosen benefit

Offsets against other income, the £1,500 minimum benefit guarantee and proportionate
benefits on a partial return to work all move the amount actually paid away from the
benefit the policyholder chose. The base run sets `AP = B` through `ap_ratio = 1` and
`claim_severity = 1` **[std]**, which **overstates** outgo wherever the maximum-benefit
formula bites and understates nothing, since `AP ≤ B` always. A portfolio calibration
sets one or both below 1 from claims experience.

`benefit_max_pp()` implements the contractual two-band maximum — 65% of earnings to the
£60,000 breakpoint, 50% above it, capped at £20,000 a month and floored at the £1,500
guarantee — and `check_benefit_max()` asserts every model point's chosen benefit is
inside it, with the 90% tolerance that stops a small fall in earnings cutting an in-force
benefit. Unlike the other two checks that one is a **validation of the model point**
rather than an identity of the projection: a benefit above the maximum is a policy that
could not have been written, and the underwriting record is on the model point precisely
so that it can be checked.

## Discounting, which the rest of the library does not do

Every other model in this library projects **undiscounted** gross liability cash flows
and leaves discounting to the layer that consumes them. This one also carries
`disc_factor(t)`, `pv_benefits()` and `annuity_dis()`, because the notes' worked example
is a present value and because the disabled-life annuity is the object a claims-in-payment
reserve is quoted as.

They are a **companion**, not part of the projection: no line of `result_cf()` is
discounted, and `disc_rate` is the worked example's flat 3% **[std]**, not a valuation
basis. A Solvency UK best estimate discounts these same cash flows on the PRA risk-free
term structure [R7] [REG-R1]; the claims-in-payment element is matching-adjustment
eligible where it is organised and managed separately [R8] [REG-R2], which is precisely
the `exit`-basis disabled-life annuity above.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `IP_UK_S/` holds nothing but formulas:

```
products/income_protection/
  model_point_table.csv        <- inputs live here
  inception_table.csv
  termination_table.csv
  mort_table.csv
  lapse_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  IP_UK_S/                    <- formulas only
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
| `inception_file` | `inception_table()` | `inception_table.csv` |
| `termination_file` | `termination_table()` | `termination_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |

The two experience bases are separate files because they are separate CMI publications
and are parameterized differently — inception by sex, occupation class, deferred period
and age, exactly as the IP11 Series names its tables; terminations by claim duration.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Seven model points: the active-lives anchor cell (M35 / OC1 / DP26 / £2,000 a month to age 65, RPI-escalating), **point 2 is the claims-in-payment worked example** (the same cell, level cover, in claim at duration 0, `exit` basis), a level-cover active cell, a female OC3 DP13 cell, a claim at duration 30 months with 15 years to expiry, a heavier OC2 DP52 cell whose earnings cross the two-band breakpoint, and point 2 again on the `return_to_h` basis | anchor cell **[std]**, technical notes |
| `inception_table.csv` | Annual claim inception rates at pivot ages 30–64, by sex × occupation class × deferred period, with a `provenance` column | the M / OC1 / DP26 pivots are the notes' **[std]** proxy table verbatim; every other cell is those pivots times flat **[std]** factors (deferred period 2.60/1.80/1.45/1.00/0.60 for 4/8/13/26/52 weeks, occupation 1.00/1.35/1.90/2.60, female 1.25) — *not* IP11 values |
| `termination_table.csv` | Annual recovery and in-claim mortality by claim duration year, 40/25/15/10/5% and a flat 3% | the notes' **[std]** proxy table verbatim |
| `mort_table.csv` | Active-life mortality by sex and age 16–75 | **[std]** proxy shaped like the ONS national life tables — *not* ONS values |
| `lapse_table.csv` | Annual lapse by policy year, 10 / 8 / 6 / 6 / 6 / 4 % | **[std]**; no public UK IP lapse study was retrieved, so this table has no anchor at all |

Inception rates are interpolated **linearly** between pivot ages and extrapolated linearly
beyond them (floored at zero), which is what the notes specify — note the contrast with
`CI_UK_S`, whose notes specify *log*-linear interpolation of its pivot table. Two products,
two rules, and each model follows its own notes.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
population counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth`
for monthly ones, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase
`kind` string. The full symbol mapping lives in the `Projection` Space docstring. Three
cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `q_H` vs `q_S` | `mort_rate` / `mort_rate_sick` | `mort_rate` means the active-life rate in every model in this library; reading a claimant rate out of it is the mistake the naming prevents |
| `BEN(t)` | `claims(t, "BENEFIT")` | An income stream rather than a lump sum, but reached through the library's one benefit-outgo cells. The other two kinds are zero and say so: **no death benefit** on this composite, and **no surrender value** at any time |
| `t` vs `z` | the two arguments | Different clocks, never mixed: rates out of S take `z`, rates out of H take `t` |

## Standardizations used

Everything in this list is **[std]**: the entire experience basis — inception, recovery,
in-claim mortality, active-life mortality and lapse — and the factors that spread the
inception pivots across sex, occupation class and deferred period; the linear pivot
interpolation and its extrapolation; the age-suppression of the termination basis; the
premium; maintenance £60 a year and claim management £300 a year, both inflating at 3%;
the flat 3% RPI snapshot and the ×1.5 premium multiplier; the premium-shock lapse
multiplier `M_esc`; the economic-cycle overlay `M_cycle` (held at 1, a scenario axis
rather than a calibrated assumption); `AP = B` and `k = 1`; whole-month benefit payment
in place of daily pro-rating; the annual-to-monthly conversions; death-then-lapse-then-
inception as the order out of H and recovery-then-death out of S; and, on an `in_claim`
cell, treating the valuation date as a policy anniversary so the escalation clock
restarts there.

## Tests

`tests/test_income_protection_uk.py` asserts the notes' three-month claims-in-payment
worked example to the penny including its present values, the month-one active-lives
figures beside it, the duration gradient and what collapsing it would cost, that premiums
come from H alone, the in-arrears payment timing, expiry truncation, the two recovery
bases against each other, the three-state population identity, the two-band benefit
maximum, and that death and lapse pay nothing.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #uklib-income_protection-r1
[R2]: #uklib-income_protection-r2
[R5]: #uklib-income_protection-r5
[R7]: #uklib-income_protection-r7
[R8]: #uklib-income_protection-r8
[REG-R1]: #uklib-reg-r1
[REG-R2]: #uklib-reg-r2
[REG-R22]: #uklib-reg-r22
[std]: #uklib-std
<!-- END generated citation links -->
