# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/obseques/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the twelve-month *délai de carence* and its two
> benefits, the refund of premiums *collected* rather than accrued [S1] [S8] [S9], the
> 1.00 % guaranteed revalorisation of the capital and the first-anniversary eligibility
> for it [S14] [S1] [S9], the surrender value equal to the *provision mathématique*
> [S1] [S8] [S9] [S12], *réduction* to a paid-up capital on non-payment [R7], the
> surrender-value and *prime unique* scales [S5] [S14] [S15] [S2], and the premium of
> every model point. Every **rate** is a **[std]** standardization. TH 00-02 and
> TF 00-02 are the homologated regulatory tables for this product [REG-R22] [REG-R23];
> they are cited by name and **never redistributed**, so the mortality shipped here is an
> INSEE-derived proxy [REG-R24] anchored so that the anchor cell's best-estimate factor is
> the notes' own placeholder rate exactly. **No public French source gives any lapse,
> surrender or paid-up rate for this product**, so every behavioural assumption is a
> drafting construction.

## Run it

```bash
python products/obseques/run.py         # the RefOBS-VIA anchor cell
python products/obseques/run.py 3       # the prime unique cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/obseques/Obseques_FR_S")
model.Projection[1].result_cf()
```

## Three cells, one engine

The three cells are the same contract with **one model point column changed** —
`premium_form`, this product's signature. Nothing branches on `cell()`, which is a label
rather than a switch.

| | **RefOBS-VIA** | **RefOBS-TMP** | **RefOBS-UNI** |
|---|---|---|---|
| `premium_form` | `lifetime` | `temporary` | `single` |
| Premium, entry 50, 5000 € | 336.03 €/year for life [S14] | 651.26 €/year for 10 years [S14] | 4274.04 € once [S5] |
| Revalorisation | 1.00 % p.a. guaranteed [S14] | 1.00 % p.a. [S14] | 0.00 % **[std]** |
| Premium-stop decrement | to the end | to the end of the term | **none** |
| Crossover | `t` = 168 / 204 | `t` = 84, then it stops | never (`-1`) |
| Anchor | **model point 1** | model point 2 | model point 3 |

The *prime unique* cell takes a zero revalorisation rate because its rate card presents
its values *sans participation aux bénéfices* [S5], so a non-zero rate would be
inconsistent with that document's own surrender scale. The same reasoning gives zero to
the three other cells priced off tables published on that basis [S5] [S15] [S2].

Two structural features separate this product from
[`WOL_UK_S`](../../../uklib/products/whole_of_life/model.md), the UK guaranteed-acceptance
over-50s cell that is otherwise almost the same contract: **the capital is a state
variable**, and **lapse pays money**. Both are first-order, and both are asserted.

## The time index

`t` is the **0-based policy month**, the library-wide convention. `t = 0` is the first
projected month, month `t` runs from time `t` to time `t + 1`, and the frame is

```
t = 0, 1, ..., proj_len() - 1        len(result_cf()) == proj_len()
```

so `proj_len()` is the **number** of projected months — `12 × (omega_age − entry_age + 1)`,
756 on the anchor cell and 516 on the entry-70 one — and the last projected month is
`proj_len() - 1`. Every model point here is new business, so every frame starts at 0.

The **policy year** is the contractual, 1-based label derived from it,
`policy_year(t) = duration(t) + 1 = t // 12 + 1`, and it is what the premium, lapse and
select schedules are keyed by. `duration(t) = t // 12` is 0-based, as in lifelib, and
`duration_mth(t) = t` is the months elapsed at the **start** of month `t`; `t + 1` months
have elapsed by the end of it, which is where deaths, surrenders and *réductions* fall.

Three consequences worth naming, because each is a place an off-by-one hides:

- the twelve *carence* months are `t = 0 … 11`, so `in_carence(t)` is `t < carence_months`
  and the signature discontinuity falls between `t = 11` and `t = 12`;
- the counts line up with the notes with **no offset**: `pols_if(t)` is the notes' `l(t)`,
  the in-force at time `t` months from issue, and `pols_if(0) == pols_if_init()`;
- `crossover_mth` returns a month on this frame, so `0` is a real answer and the "never
  crosses" sentinel is **`-1`**.

## The délai de carence is two benefits, not one

For twelve months [S1] [S8] [S9] [S11] [S12] [S13]:

- a **non-accidental** death refunds the premiums **collected** — `refund_pp(t)`, which
  under an annual premium in advance is a **step function**, constant at 336.03 € through
  months `t` = 0 to 11, not a monthly accrual;
- an **accidental** death pays the **full guaranteed capital from day one** [S1] [S8]
  [S9] [S11] [S13].

From `t = 12` any death pays the capital. Expected death outgo steps by a factor of
**7.8080** between `t = 11` and `t = 12`, and the step decomposes exactly into three
independent moves — in-force 0.994191, monthly mortality 0.885251, benefit 8.871657.
That discontinuity is the reason the grid must be monthly.

Three ways to get it wrong, all of them large, all of them tested:

| Error | First month (`t` = 0) | Policy year 1 |
|---|---|---|
| Correct | 0.380884 | 4.4274 |
| Pay the **capital** inside the *carence* | 3.345618 (×8.78) | 38.8893 |
| Drop the **accident** leg | 0.224846 (−41 %) | 2.6136 |
| Accrue the refund base **monthly** | — | 3.2750 (−26 %) |

`benefit_pp(t, "ILL")` and `benefit_pp(t, "ACC")` carry the two legs and
`benefit_pp(t, "DEATH")` blends them by `acc_share`, 5 % **[std]**. That share is set
below any plausible external-cause share on purpose: the contractual definition of an
accident is **narrower than external-cause mortality**, because cerebral and
cardio-vascular events are never accidents whatever their origin, and the burden of proof
is on the claimant [S1] — with the market description adding myocardial infarction,
coronary conditions and emotional shock [R21], and the other contract that defines an
accident narrowing it a different way, by excluding acute and chronic illness and harm
from medical or surgical treatment [S8]. It matters only inside the waiting period — where
it is the whole of the difference between a refund and a capital.

**The accidental multiplier** doubles the accidental benefit, capped at 20000 € [S8], and
applies **past the waiting period only**. Inside it the accidental benefit is already the
full capital, so doubling it there — or applying the multiplier to all deaths —
overstates outgo. `accident_mult()` is used in exactly one place,
`benefit_pp(t, "ACC")`, past the *carence* only.

## The capital is a state variable

`capital_pp(t)` is `C_0 × (1 + r)^(y−1)`, uprated out of the *participation aux bénéfices*
[S1] [S2] [S15] [S16] [REG-R14] [REG-R15]. The uprating starts at the **first
anniversary**, not at issue, because PB is allocated to contracts in force at least a year
[S1] [S9] — so `capital_pp(t) == capital_0()` for `t < 12`, which `check_capital_reval()`
asserts. Uprating at issue would make it 5050.00 € in the first year and overstate the
year-1 accidental leg.

Two parameters are easy to confuse and are kept apart deliberately. `reval_rate` moves the
**capital**. `carence_refund_rate` credits interest on a **refund of premiums**, is zero
in every retrieved contract [S1] [S8] [S9], and reaches a different product in statute —
the legal-rate floor of the loi Sueur is drafted for the advance-*prestations* form [R6].
The illness benefit inside the waiting period is a refund, not a capital, and carries no
revalorisation.

`reval_prem_linked` is the fork that must never be hard-coded: five of the seven retrieved
insurers leave the premium alone [S5] [S6] [S7] [S14] [S16], one raises the **remaining**
premiums in the same proportion [S9] [S10] [S11]. `reval_simple` is the second reading of
"*1 % du capital souscrit*" — a simple uplift on the subscribed capital rather than
compounding on the current one. Which reading the wording intends is [unverified]; compound
is the reference **[std]** and the simple form is model point 11.

## Lapse pays money, and réduction is not termination

*Rachat* pays the *provision mathématique* [S1] [S8] [S9] [S12], because a whole-life contract
sits in art. L. 132-23 CA's residual *autres assurances sur la vie* class, where the insurer may
refuse neither *rachat* nor *réduction*. The article withholds them from a closed list only:
temporary death assurance and immediate or in-payment annuities may carry neither, and
survivorship capitals, pure endowments and deferred annuities without return of premium may
carry no *rachat* [R10]. So
`claims(t, "LAPSE")` is **non-zero from `t` = 0** and worth 1005.89 € over the anchor
cell's horizon. This is where the UK sibling's model is actively misleading: there a lapse
pays nothing, every lapse extinguishes a liability for free, and raising lapse always
lowers the liability. Here it does not.

| Anchor cell, undiscounted, before expenses | Net stream |
|---|---|
| As modelled | **+2236.92** |
| `claims_lapse` forced to zero, decrements unchanged | +3242.81 (+45 %) |
| Lapse **decrement** removed altogether | +3165.11 |

The two right-hand rows move in the same direction for opposite reasons, and the second is
the one that matters: the premiums a lapser stops paying are worth more than the reserve
handed back, so **zero lapse raises the liability**. Both are asserted.

**No premium-stop decrement where no premium is due.** After `prem_cease_age`, past the
end of a temporary term, on a *prime unique* cell and in the paid-up state there is
nothing left to stop paying, and a decrement there silently destroys liability.
`lapse_rate()` is zero in all four, and `check_lapse_gate()` re-states the gate through
`prem_due_pp` rather than through `in_paying_period`, so it does not merely repeat the
branch it is checking.

***Réduction* is a paid-up contract, not an exit.** Non-payment produces *réduction*
wherever the surrender value is sufficient [R7] [S1] [S8] [S9], so a share
`reduction_share` of premium-stops converts — a state change with no cash flow — and the
contract still owes those policies a reduced capital for the rest of the insured's life.
It is carried as a **second population strand**:

| Cells | What it holds |
|---|---|
| `pols_if(t)` | policies still paying premiums, measured at the **start** of month t — the notes' `l(t)`, since the notes carry `l` at time t months from issue and the start of month t is time t, and the column the worked example prints |
| `pols_paid_up(t)` | paid-up (*réduit*) policies at the start of month t — the notes' `l_r(t)`, same alignment |
| `capital_paid_up(t)` | the **aggregate paid-up capital** in force |
| `pols_all(t)` | the sum, which is what the maintenance expense is carried on |

Carrying the aggregate capital alongside the count removes the need for a per-conversion
cohort dimension: `reduced_capital_pp(t)` depends on *when* the policy converted, but every
paid-up policy thereafter rolls forward on the same survival factor, so the sum of their
capitals satisfies the same recursion as the count. Death outgo on the strand is then
`capital_paid_up(t) × q_m(t)`.

`reduction_share` is 0 in the base cell, 0.5 on model point 5 and 1.0 as the upper stress
**[std]**. No public source gives any split between voluntary surrender and paid-up
conversion, because none gives any decrement rate at all. It dominates the late-duration
liability and **must never be approximated by perturbing the lapse rate instead**.

## The overrun, and its two crossovers

Under *primes viagères* cumulative premiums grow without bound while the capital grows at
most at the revalorisation rate, so the insured can and often does pay more than the
capital — the KID says so in terms [S11]. `crossover_mth(basis)` finds the month, and it
finds **two**:

| Basis | Anchor cell | Notes |
|---|---|---|
| `"ISSUE"` | `t` = **168**, policy year 15 | against `capital_0`, 5040.45 € against 5000 € |
| `"CURRENT"` | `t` = **204**, policy year 18 | against the revalorised capital, 6048.54 € against 5921.52 € |

Three years apart, and publishing one without saying which is how a stated crossover moves
by years. The standardised tables add a second convention on top: they date their columns
by the age at the **end** of the year, so their "age 65" column is this model's attained
age 64 during policy year 15. Model point 7 reproduces the notes' subsidiary table exactly
on that reading — 2467.80 / 4113.00 / 5758.20 / 7403.40 € of cumulative premiums at the
tables' ages 65 / 75 / 85 / 95 [S5] — and crosses at `t` = 360, policy year 31, attained
age 80.

Letting lifetime premiums stop by accident removes the overrun and with it the product's
characteristic feature. `prem_cease_age` is 0 on the anchor **[std]**, so it is still
collecting 336.03 € a year at attained age 100; model point 10 is the documented
"*jusqu'à vos 80 ans*" form [S9] [S10] and stops at 30 premiums.

The overrun-aware lapse module — `lapse_rate` × `(1 + beta)` past the tipping point — is a
pure stress dial, and `lapse_overrun_beta` is 0 in the base run.

## The surrender value is an input, not a formula

`surr_value_pp(t)` reads a **published scale** rather than computing a prospective
*provision mathématique*, and that is a deliberate limitation. The contract makes the
surrender value the mathematical provision [S1] [S8] [S9] [S12]; a production model
computes it prospectively on the tariff basis; and **no French insurer publishes its
tariff basis** — the whole retrieved set contains one technical rate with a table (0.75 %
with TH 00-02 [S8]) and one rate alone (0 % [S1]).

What every insurer *does* publish, since 1 July 2025, is a standardised table of surrender
values by duration for a 5000 € capital [R13] [R15]. The model reads that, interpolates it
linearly in **elapsed months from issue** between the published quinquennial anchors
**[std]** and holds
it flat beyond the last one. Because a *rachat* resolves at the **end** of month `t`, the
lookup key is `duration_mth(t) + 1 = t + 1`: `surr_value_pp(0)` is the one-month value,
13.07 € on the anchor cell, and the published five-year anchor of 784.01 € is
`surr_scale_pp(59)`. The anchors already embed that insurer's own revalorisation,
which is why `surr_value_pp` is **not** additionally scaled by `capital_pp` — it is
pro-rated to the policy's own `capital_0` and netted of any penalty, and nothing else.

**Every published anchor is shipped, not a sample of them.** Each grid carries all nine
quinquennial values, at 60 to 540 months. Dropping the intermediate ones and letting the
interpolation stand in for them is not a rounding: on the Mutex *temporaire* 25 ans grid it
puts month 300 at about 4497 € against the published 5074 €, 11 % low, and erases the peak
the grid exists to show — a temporary-premium surrender value that tops out at the end of
the premium term and then declines under the 0.40 % p.a. charge on the capital [S1] [S2].
A test asserts all nine anchors on all six grids.

The other consequence is that **the premium, the revalorisation rate and the surrender scale
of a model point must come from one document**. Feeding one insurer's premium into another's
grid produces plausible-looking and wrong margins: the lifetime premium for the same capital
spans 2.0:1 across the retrieved set at entry age 50, 1.7:1 at 60 and 1.5:1 at 70. A test
asserts that every `surr_scale` value names a scale that exists.

`single_prem_rate(x)` is the second scale and serves twice: it is the tariff behind the
*prime unique* form, and it is what turns a mathematical provision into a *valeur de
réduction*, `reduced_capital_pp(t) = V(t) / u(x(t))` [S1] [S8].

## Différence de millésime

The age basis is the **calendar year of subscription less the calendar year of birth**
[S1] [S8] [S9] — not age last birthday and not age nearest birthday. The true basis
increments on 1 January; `age(t)` increments at the **policy anniversary** instead
**[std]**, which is exact for a January issue and off by up to one policy year of mortality
otherwise. `issue_month` is a model point column, 1 on every shipped point, so the
approximation is visible in the data rather than buried in a formula. The *décalage d'âge*
schedules annexed to art. A. 335-1 CA [REG-R23] apply on top of the basis where a
homologated table is used, and are not modelled because no homologated table is shipped.

## Inputs are external files

The six input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `Obseques_FR_S/` holds nothing but formulas:

```
products/obseques/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  select_table.csv
  lapse_table.csv
  surr_scale_table.csv
  single_prem_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  Obseques_FR_S/               <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file is
read once per model rather than once per model point; a test counts the reads.

**No CSV column is the model's `t`,** so none of them moved when the frame became 0-based:

| File | Time-like column | Decision |
|---|---|---|
| `lapse_table.csv` | `policy_year`, values 1–6 | **Unchanged.** A contractual, 1-based policy-year label; `lapse_rate_base` looks it up through `policy_year(t) = t // 12 + 1`, clamped to the last row |
| `select_table.csv` | `policy_year`, values 1–4 | **Unchanged**, same reason, through `select_uplift(t)` |
| `surr_scale_table.csv` | `month`, values 0, 60, 120 … 540 | **Unchanged.** An **elapsed count** from issue — the published quinquennial anniversaries, 0 meaning "at issue" — not the frame's index. `surr_scale_pp(t)` reads it at `duration_mth(t) + 1`, the months elapsed at the end of month `t` |
| `mort_table.csv` | `age` (with `sex`) | **Unchanged.** Attained age, reached through `mort_rate_base(age(t))`; not a time key |
| `single_prem_table.csv` | `age` | **Unchanged.** Attained age, through `single_prem_rate(age(t))` |
| `model_point_table.csv` | `prem_term_y`, `carence_months`, `surr_penalty_years` | **Unchanged.** Durations — counts of years or months, 0-based by nature. What changed is the comparison at the boundary: `t < 12 × prem_term_y`, `t < carence_months`, `t < 12 × surr_penalty_years`, each having been `<=` on the 1-based frame |
| `model_point_table.csv` | `prem_cease_age`, `entry_age` | **Unchanged.** Attained ages, compared against `age(t)` |
| `model_point_table.csv` | `issue_month` | **Unchanged.** A *calendar* month, 1–12, and not on the frame's axis at all — it flags the age-basis approximation and enters no formula |

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `select_table_file` | `select_table()` | `select_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `surr_scale_file` | `surr_scale_table()` | `surr_scale_table.csv` |
| `single_prem_file` | `single_prem_table()` | `single_prem_table.csv` |

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Twelve model points. **Point 1 is the worked-example anchor cell** (RefOBS-VIA / M50 / 5000 € / 336.03 €/year for life / 1.00 % revalorisation / *carence* 12 months); points 2 and 3 are the other two premium forms; points 4–6 are the premium-linked coupling, *réduction* at 50 %, and the doubled accidental benefit with a 5 % surrender penalty and an assistance-netted refund; points 7–9 are a second insurer's *viagère* rate card, an entry-70 female cell and a 25-year *temporaire*; points 10–12 are a cessation age of 80, simple revalorisation and monthly instalments | anchor cell **[std]**, technical notes' worked example; every premium and scale transcribed from [S14] [S5] [S15] [S2] |
| `mort_table.csv` | Annual base mortality by sex × attained age 18–112, capped at 1, with a `provenance` column | **[std]** throughout. An INSEE-shaped Gompertz proxy [REG-R24] anchored at `q(M, 50) = 0.0040` with 9 % p.a. age progression — the notes' walk-through basis *exactly*, so `q(M,50) × 1.25 × 1.60 = 0.008000` — and female rates a flat 0.60 factor on it. **Not** TH 00-02 / TF 00-02 [REG-R22] [REG-R23], which are cited and never shipped |
| `select_table.csv` | Select uplift by policy year: 1.60 / 1.30 / 1.15 / 1.00 | **[std]**; the *direction* is defensible on a guaranteed-issue book [S1] [S11] [S12] [S13] [R21], the magnitude has no public calibration of any kind |
| `lapse_table.csv` | Annual premium-stop rate by policy year: 6 / 5 / 3.5 / 3.5 / 3.5 / 2.5 % | **[std]**; no public French source gives any lapse, surrender or paid-up rate for this product. The declining shape follows from a surrender value worth a fraction of the premiums paid [S14] |
| `surr_scale_table.csv` | Six surrender-value grids in € per 5000 € of capital, by **elapsed months from issue**; each carries **all nine** published quinquennial anchors, at 60 to 540 months in steps of 60 | Transcribed anchors: AXA Serenova *viagère* and *temporaire* 10 ans at entry 50 [S14], CNP *viagère* and *prime unique* at 50 [S5], Sogecap *viagère* at 70 [S15], Mutex *temporaire* 25 ans at 50 [S2]. **This file is the source of truth for the provenance of every anchor** — its `provenance` column names the insurer, entry age, premium form and source id row by row. Month-0 anchors are **[std]**: zero on a periodic-premium form, a linear back-extrapolation on the single-premium one |
| `single_prem_table.csv` | u(x), the single premium per 1 € of whole-life capital, by attained age 18–112 | Anchored at 0.854808 / 0.909720 / 0.963912 at ages 50 / 60 / 70 [S5]; interpolated and extrapolated **[std]**, clipped to [0.30, 1.00] |

## Sign convention

The technical notes print the stream **outgo-positive**, so that orientation survives
verbatim as `liability_cf(t)` and `net_cf(t) = −liability_cf(t)` exactly — income-positive,
the library-wide sign.

```
liability_cf = claims_death + claims_death_paid_up + claims_lapse + expenses − premiums
net_cf       = −liability_cf
```

One caveat for a reader checking the worked example by eye: **the notes' table omits
expenses entirely**, "for clarity", and prints premium income, death outgo and surrender
outgo as separate positive columns. So neither `net_cf` nor `liability_cf` equals any
column of that table, and the tests assert `premiums(t)`, `claims(t, "DEATH")` and
`claims(t, "LAPSE")` against it directly. The notes' undiscounted totals — premiums
6184.01, death 2941.20, surrender 1005.89, net +2236.92 — are likewise before expenses,
which come to 704.33 over the same horizon.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
policy counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth` for
monthly ones, `*_pp` for per-policy amounts, `claims(t, kind)` and `benefit_pp(t, kind)`
with uppercase `kind` strings. The full symbol mapping lives in the `Projection` Space
docstring. Five cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `l(t)`, `l_r(t)` | `pols_if` / `pols_paid_up` / `pols_all` | Two population strands, because *réduction* keeps a liability rather than ending one; on every point where `reduction_share` is 0 the three coincide. **And no offset:** the notes measure `l` at time t months from issue, the library at the start of month t, which is the same instant, so `pols_if(t)` = `l(t)` — the worked example's column is headed `pols_if(t)` for exactly that reason |
| `C_red(t)` | `reduced_capital_pp` / `capital_paid_up` | The per-policy paid-up capital, and the **aggregate** in force — which is what removes the need for a per-conversion cohort dimension |
| `surr_scale(t)` | `surr_scale` / `surr_scale_pp` | The model point's **choice** of published grid, and the interpolated amount off it. Separate cells because mixing one insurer's premium with another's grid is the easiest wrong answer on this product |
| `claims_death` | `claims_death` + `claims_death_paid_up` | The notes' single column is the sum of the two strands; the library publishes one column per `kind` |
| `omega` | `omega_age` | `omega` is a retired name in this library |

## Standardizations used

Everything in this list is **[std]**: the mortality proxy and its 0.60 female factor; the
1.25 anti-selection loading and the 1.60 / 1.30 / 1.15 select uplift; the mortality
improvement dial (zero in base, a flat annual rate as the proxy, since France has no
publicly available insured-lives projection model comparable to the CMI's); the lapse
table; the 5 % accidental share of deaths; `reduction_share` at 0 in base with 0.5 and 1.0
as the variations; the monthly conversion `q_m = 1 − (1 − q)^(1/12)`; the limiting age
`omega_age = 112` and mortality forced to 1 there; the anniversary age step in place of the
1 January *millésime* step, with `issue_month = 1` on every shipped point so that the
approximation is exact where the data says it is; linear interpolation of both external
scales in elapsed months and the month-0 anchors; compounding rather than simple revalorisation; annual premiums in
advance with the instalment options carried as a 2.2 % loading [S11] rather than a
re-tariffing; acquisition 150 € at issue and maintenance 24 €/year inflating at 1.8 %;
death-before-premium-stop as the processing order; and the overrun lapse stress dial.

Deliberately excluded, per the notes: the **post-mortem revalorisation** between death and
payment [S1] [S8] [R8] [REG-R31] and the statutory payment clock of art. L. 132-23-1 CA —
settlement-lag refinements; **capital increases**, anti-selective on a guaranteed-issue
book and mitigated but not removed by the fresh waiting period on the increment [S1] [S8];
the 30-day ***renonciation*** with a full refund [S1] [S8] [REG-R29], modelled as
never-issued business outside the projection; the **40-day suspension** of cover during the
formal-notice window [S1], where ignoring it is the conservative choice; **aggregate
capital caps** per insured [S1] [S8] [S12], which bind across contracts rather than per
policy; and **claim handling costs**, folded into maintenance because no retrieved document
separates them from disclosed *charges*.

There is **no maturity kind and no account value**. The contract ends only on death, on
*rachat* or on lapse [S1] [S8] [S9] [S11]; maturity outgo is identically zero because there
is no maturity, and a test asserts that none of the account-value chassis exists here.

## Tests

`tests/test_obseques_fr.py` asserts all fifteen rows of the notes' worked example to the
cent and the in-force column to five decimals — re-keyed to the 0-based frame, values
unchanged — the undiscounted totals over the full 756-month horizon `t = 0 … 755`, the
`t = 11` / `t = 12` *carence* step and its three-factor decomposition, the
notes' own closed-form survivorship checks at the first two anniversaries, the capital and
the surrender value at `t = 204` two ways, and then one test for each of the twelve
modelling pitfalls the notes list — each named for the failure it catches. A further test
pins **all nine** published quinquennial anchors on **all six** shipped surrender grids,
against the model as well as against the CSV, because an anchor silently replaced by an
interpolant between its neighbours is a shipped input 11 % away from the figure the
documents claim to transcribe. Five `check_*`
cells run over every model point in the conventions suite: the in-force roll-forward across
both strands, the annual survivorship identity, the capital roll-forward, the premium-stop
gate and the truncation residual at the limiting age.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R10]: #frlib-obseques-r10
[R13]: #frlib-obseques-r13
[R15]: #frlib-obseques-r15
[R21]: #frlib-obseques-r21
[R6]: #frlib-obseques-r6
[R7]: #frlib-obseques-r7
[R8]: #frlib-obseques-r8
[REG-R14]: #frlib-reg-r14
[REG-R15]: #frlib-reg-r15
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R31]: #frlib-reg-r31
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
