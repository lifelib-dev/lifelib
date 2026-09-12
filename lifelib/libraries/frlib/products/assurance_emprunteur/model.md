# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/assurance_emprunteur/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the two premium bases [S9] [S11] [S13] against
> [S2] [S7] [S8] [S10], the two indemnity bases [S1] [S3] [S6] [S11] against [S10], the
> *franchise* menu [S9], the 1 095-day ITT cap [S1] [S11] [S12], the 66 % *barème croisé*
> IPT threshold [S1] [S5] [S9] [S10] [S11] [S12], the `crd × quotité` death and PTIA
> capital [S1] [S5] [S9] [S10] [S11], waiver of premium in claim [S5] [S11], the level
> *nivelé* premium [S13], *résiliation à tout moment* [R1] [R3] [REG-R35] and expiry
> without value [S1] [S9]. **Every rate is a **[std]** standardization.** No French
> decrement, incidence or termination table for this product was retrieved: insurer rate
> cards are proprietary, the CCSF publishes tariff levels only as chart series [R12], and
> the homologated TH 00-02 / TF 00-02 tables are cited by name but are not
> redistributable [REG-R22] [REG-R23]. The mortality, PTIA, ITT inception, ITT
> termination, IPT mortality, *résiliation* and CRD premium tables shipped here are
> proxies shaped from INSEE population data [REG-R24] and carry no authority. Replace
> them with a licensed basis first.

## Run it

```bash
python products/assurance_emprunteur/run.py        # the worked-example anchor cell
python products/assurance_emprunteur/run.py 2      # the capital restant du premium basis
python products/assurance_emprunteur/run.py 9      # a claim in payment, ITT at month 18
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/assurance_emprunteur/ADE_FR_S")
model.Projection[1].result_cf()
```

## Four states over an amortising loan

`ADE_FR_S` is the most intricate model in this library, and the reason is that four
mechanisms run at once: a deterministic loan, a four-state population, three guarantees
that end at three different ages, and a lapse decrement that is really a substitution
market. The state machine is `IP_UK_S`'s healthy/sick/dead chassis with a fourth state
and a duration-triggered forced transition:

```
        inception iota            recovery rho
   healthy ---------------> ITT ---------------> healthy
      |                      |  \  tau
      | mortality q_h        |   \
      | PTIA q_ptia          |    v
      | resiliation w        |   IPT ---- q_ipt ----> dead
      v                      |          (no recovery)
   dead / claimed / lapsed   +---- q_s ----> dead
```

**IPT has no recovery.** Once a life is assessed above the 66 % *barème croisé*
threshold the only exits are death and the guarantee's age limit, so the IPT annuity can
run to the end of the loan while the ITT one is capped at three years. That asymmetry is
why `ipt_share_at_cap` — the fraction of the capped ITT cohort that consolidates — is a
first-order assumption: it converts a bounded three-year claim into an annuity, and the
liability is roughly linear in it. Nothing public quantifies it.

### The time index, and the two clocks

`t` is the **0-based policy month**, the library-wide convention: `t = 0` is the
contract's first month, `result_cf()` runs `t = 0 … proj_len() − 1` — 240 rows on the
anchor cell, indexed 0 to 239 — and `proj_len() = loan_term_months` is the *number* of
months projected, the exclusive end of the frame, exactly lifelib's
`for t in range(proj_len())`. Month `t` runs from time `t` to time `t + 1`: the premium
falls at its beginning and the instalment, the transitions and every benefit at its end.
The contractual policy year is the 1-based label `policy_year(t) = duration(t) + 1` with
`duration(t) = t // 12`, and it is derived, never indexed by: it is what the *résiliation*
table and the expense inflation are read on.

Two quantities keep an index of their own, and neither is the month index:

* **`crd(k)` is a time point.** `k = 0` is adhesion, so `crd(0) = capital_initial` and
  `crd(T) = 0` at the last instalment. Month `t` opens on `crd(t)` and closes on
  `crd(t + 1)`. That index was already 0-based and does not move.
* **`z` is the claim duration**, 1 to `itt_max_months()` = 36, counted from the start of
  claim *payment*. `t` and `z` are different clocks and the model never mixes them: rates
  out of ITT take `z`, rates out of healthy take `t`.

The technical notes carry the state probabilities at a time point too — `l_h(k)`,
`l_itt(k, z)`, `l_ipt(k)`, with `l_h(0) = 1` — so `pols_healthy(t)` is the notes' `l_h(t)`
opening month `t` and `pols_healthy_close(t)` is `l_h(t + 1)` closing it.

### The loan spine is computed, not read

Nothing is read from an *échéancier*. `echeance()` is the level instalment from
`capital_initial`, `loan_rate_annual` and `loan_term_months`, and `crd(k)` is the
*capital restant dû* at time `k`, immediately **after** the `k`-th instalment. `crd` is the
only thing linking the loan to the insurance: the Décès and PTIA capital of month `t` is
`crd(t + 1) × quotité`, the balance at the end of that month, and the ITT/IPT benefit is
`echeance() × quotité`.

`check_crd()` asserts three things at once — `crd(0) = capital_initial`, `crd(T) = 0` at
the final instalment, and `crd(k) = crd(k−1)(1 + i) − ech` at every `k`. That is the
check a pasted schedule fails, and it also catches the wrong rate conversion: a French
loan quotes a *taux nominal annuel* whose monthly rate is **nominal ÷ 12**, not
`(1 + nominal)^(1/12) − 1`. `loan_rate_mth()` is the one place in the model where an
annual rate is not converted with `1 − (1 − r)^(1/12)`, and its docstring says so, because
that rule is for decrements and a loan is not a decrement.

The convention matters as much as the arithmetic. The balance opening month `t` and the one
closing it — `crd(t)` and `crd(t + 1)` — differ by the month's capital repayment,
EUR 609.20 over the first month on the anchor cell, and whichever is chosen must be used
everywhere. The model writes the benefit on the **closing** balance `crd(t + 1)`, the
instalment falling on the day of death being deemed due [S9]. Indexing `crd` on the month
rather than on the time point is how that choice gets made by accident.

### The in-claim population is two-dimensional, and the cap assesses it

ITT termination rates depend on how long the claim has run: recovery falls 0.55 → 0.15
across the three duration years while the IPT transition rises 0.02 → 0.12. So the model
tracks `l_itt(t, z)` cohort by cohort. `itt_cohorts(t)` holds the whole vector for one
month and is the model's only list-valued cells; `pols_itt_dur(t, z)` reads an element out
of it so the notes' two-dimensional object stays addressable by name without the model
carrying `proj_len() × itt_max_months()` separate cells. `itt_rate_vectors()` is the same
trick for the four per-duration rate vectors. The list is rebuilt rather than mutated on
each step, so a month already computed is never rewritten by a later one.

At `z = itt_max_months()` — 36 months, the 1 095-day cap [S1] [S11] [S12] — the surviving
cohort is **assessed, not advanced**: `pols_cap_to_ipt(t)` passes to IPT and
`pols_cap_return(t)` goes back to healthy. If cohort 36 simply advanced to cohort 37, ITT
claims would run for ever and IPT would never be fed from the cap. On the anchor cell that
is 0.198077 of every inception still in ITT at three years, of which 0.069327 consolidates
— and the IPT annuity it buys is EUR 1 293.18 of the cell's present value, against
EUR 1 932.71 for the whole of ITT.

## The guarantees end at different ages, and the premium does not

`cover_deces(t)`, `cover_ptia(t)` and `cover_itt(t)` are three separate indicators because
the three cover-end ages differ — 85, 70 and 70 on the anchor cell (Décès 85 and PTIA 70
[S9] [S11]; ITT/IPT 70 [S9], where MAIF stops at 67 [S11]), against a loan of 240 months.
**Collapsing Décès and PTIA into one decrement** is tempting,
since they pay the identical `crd(t + 1) × quotité`, and it is wrong: a collapsed decrement
either pays PTIA after 70 or stops paying death before 85.

At the first month where `cover_itt` is 0, any claim in payment is **moved** into healthy
at the beginning of the month and before any transition. `pols_itt_transfer(t)` and
`pols_ipt_transfer(t)` are that movement — 0.009266 and 0.013982 of a policy at `t = 216`
on the anchor cell, the month the insured turns 70. The mass is moved, not deleted: those
lives are alive, still death covered and still paying, and deleting them would break
`check_states()` and destroy cover they still hold.

**The premium does not fall when the cover shrinks.** The rate is *nivelé* [S13]. On the
anchor cell that is 24 months × EUR 140.00 = EUR 3 360.00 of nominal premium against death
cover alone, EUR 638.67 survivorship-weighted, while EUR 25 806.51 of capital is still
owed. A model that switches the premium off with the guarantee understates premium income
by exactly that; the mirror error is letting `claims(t, "ITT")` run past the age limit.
`check_cover_end()` asserts the second. It is zero by construction in this implementation
— every ITT and IPT quantity is computed off `itt_cohorts(t)` and `pols_ipt(t)`, which
return zero from the cover-end month — and it is published anyway because the
mis-implementation it names is invisible from anywhere else in the output.

Model point 8 is the extreme case: ITT/IPT cover off from `t = 84` on a loan of 264
months, so 180 months of the loan carry death cover only. The published French
claim-decline causes list "maximum cover age exceeded" among the commonest [R12], which is
this interaction seen from the claims register.

## Premiums come from healthy alone

`premiums(t)` is carried on `pols_healthy(t)` and **never** on `pols_if(t)`. Premiums are
waived in claim [S5] [S11], so projecting income from lives in ITT or IPT overstates it by
the whole in-claim population — and it is easy to write by accident in a model that also
tracks total lives in force. `result_cf()` publishes `pols_healthy` beside `pols_if` for
exactly this reason: the difference between the two columns is the population whose
premiums are waived.

Symmetrically, the *résiliation* decrement applies to healthy only. Lapsing a life in
claim silently cancels a claim in payment, and nothing else in the output would show it.

## Benefit in arrears, and the ITT to IPT move

A claim incepting at the end of month `t` seeds cohort `z = 1` and is first paid at the end
of month `t + 1`. So the ITT benefit is paid on `pols_itt_stay(t)` — the cohorts already in
payment at the start of the month that survived it — and the month's own inceptions are
excluded. On the anchor cell `claims(0, "ITT")` is exactly zero and `claims(1, "ITT")` is
EUR 0.93, which is `ech × s_itt(1) × n_itt(0)` — `s_itt` on the claim clock `z`, where the
first month in payment is `z = 1`.

A life in ITT throughout month `t` is paid for that month whether it then stays,
consolidates at the cap, or returns to healthy; and `claims(t, "IPT")` covers the IPT
survivors **plus the month's ITT → IPT transitions**, so the move creates neither an unpaid
month nor a doubled one. `check_benefit_split()` asserts it:

```
ben_itt + ben_ipt = ech x Q x IR x (l_itt(t+1) - n_itt(t) + l_ipt(t+1) + cap_return(t))
```

**The `cap_return` term is the one an implementation forgets.** Those lives were in ITT
throughout the month and are paid for it, but they end the month in healthy and so appear
in neither closing disabled state. The technical notes' first draft omitted it; the
identity was short by up to EUR 0.13 a month on the anchor cell, and the note was corrected
against the model rather than the model against the note.

The check is not an identity by construction: `pols_itt_close(t)` reads the *next* month's
un-transferred opening cohort vector out of the recursion, while the benefit sums the
survivals directly. A mis-indexed duration shift moves one and not the other.

## Two premium bases, two indemnity bases, two IPT benefit bases

All three are model point columns, not variants of the model.

| Column | Values | What changes |
|---|---|---|
| `premium_basis` | `capital_initial` [S9] [S11] [S13] / `capital_restant_du` [S2] [S7] [S8] [S10] | a level rate on the original capital, or a rate on the outstanding balance re-read at each anniversary with the attained age |
| `indemnity_basis` | `forfaitaire` [S1] [S3] [S6] [S11] / `indemnitaire` [S10] | whether the *échéance* is paid outright or capped at the actual income loss through `income_loss_ratio` |
| `ipt_benefit_basis` | `echeance` [S5] [S9] [S11] / `crd` [S1] [S2] [S7] | whether IPT is a state paying monthly, or a single payment of `crd(t + 1) × quotité` after which the life leaves the model |

**The "decreasing" premium does not decrease.** On the anchor cell's life the CRD basis
rises from EUR 125.33 in policy year 1 to a peak of EUR 164.03 in year 10 before falling to
EUR 31.65 in year 20, because the attained-age rate climbs faster than the CRD falls. A
monotonicity assertion on it fails, correctly, and `test_the_decreasing_premium_rises_first`
asserts the peak. Over the whole 240 months the two bases are PV-equivalent by
construction — EUR 12 602.19 against EUR 12 588.82, a ratio of 1.001062 — which is how the
CRD scale was calibrated and would not be true of a real tariff.

`indemnitaire` is the **same formula** with `indemnity_ratio()` below 1, never a second
benefit expression that could drift from the *forfaitaire* leg. At `income_loss_ratio = 1`
the two cells are identical, which is the honest base: modelling the cap properly needs a
distribution of employer sick pay and *prévoyance* cover across the book that nothing
retrieved supplies [S6] [S10].

`quotite` scales the benefit **and** the premium, once each. Applying it to the CRD and
again to the benefit is invisible at 1.00, so model point 3 carries 0.60 and the test
asserts every cash flow is exactly 0.60 of the anchor's.

## Model points

Twelve single-life cells, each projecting on a monthly grid to its own loan expiry:

| Point | Cell | What it exercises |
|---|---|---|
| 1 | M52, EUR 200 000 at 3.00 % over 240 months, *capital initial* 0.84 %, *forfaitaire*, *franchise* 90 | **the worked example** |
| 2 | point 1 on the `capital_restant_du` basis | the non-monotonic CRD premium, PV-equivalence |
| 3 | point 1 at `quotite` 0.60 | *quotité* applied once to each leg |
| 4 | point 1 *indemnitaire*, `income_loss_ratio` 0.55 | the indemnity lever |
| 5 | point 1 with `ipt_benefit_basis = crd` | IPT as a capital, not a state |
| 6 | F34, EUR 250 000 at 2.20 % over 300 months, `quotite` 0.50, *franchise* 30 | the female factors and the 1.60 *franchise* factor |
| 7 | M45, EUR 90 000 at 4.10 % over 180 months, CRD basis, *franchise* 180 | the 0.65 *franchise* factor at the long end |
| 8 | M58, EUR 120 000 at 3.60 % over 264 months, cover to 80 / 65 / 65 | 180 months of loan with death cover only |
| 9 | point 1 seeded `status = itt` at claim duration 18 months | a claim in payment, mid-cap |
| 10 | point 1 seeded `status = ipt` | the IPT annuity, and the cover-end transfer at scale |
| 11 | M62, EUR 40 000 at 5.20 % over 84 months, *franchise* 60 | a short loan on an older life |
| 12 | F40, EUR 180 000 at 3.00 % over 240 months, CRD basis, *indemnitaire* 0.80, *franchise* 120 | four levers at once |

Point 1's premium rate is the notes' 0.84 %, and its margin on premium — `1 −
pv_outgo/pv_premiums` at the flat 2.5 % — is 9.81 %. Points 2 to 5, 9 and 10 keep that same
rate, so that what moves the margin is the lever each of them turns and nothing else. The
four cells with a loan of their own — 6, 7, 8 and 11 — carry the level rate that would
reproduce the anchor's 9.81 %, **rounded to the four decimals `model_point_table.csv` ships**
**[std]**. That is how those rates were picked; it is not an invariant, because the rounding
bites hardest where the rate is smallest: 0.27390 % rounded to 0.2700 % costs point 6 1.3 pp
(margin 8.50 %), and 1.09572 % rounded to 1.1000 % gains point 8 0.35 pp (10.16 %), against
9.81 % on point 11 and 10.14 % on point 7. Point 12's 0.25 % is a round pick, not a
calibration — *indemnitaire* 0.80 on a *quotité* of 0.75 leaves it at 25.1 %. Only the
anchor's margin is asserted by a test.

## Discounting, which the rest of the library does not do

Every other model in this library projects **undiscounted** gross liability cash flows and
leaves discounting to the layer that consumes them. This one also carries `disc_factor(t)`,
`pv_premiums()`, `pv_claims(kind)`, `pv_expenses()` and `pv_outgo()`, because the notes'
Checks quote present values over the full 240 months and those are what the tests assert.

They are a **companion**, not part of the projection: no line of `result_cf()` is
discounted, and `disc_rate` is the notes' flat 2.5 % **[std]**, not a valuation basis. A
Solvabilité II best estimate discounts these same cash flows on the EIOPA risk-free term
structure [REG-R4] [REG-R5]; no numeric EIOPA curve value was extracted anywhere in this
library, which is why the reference rate here is a modeling convention.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `ADE_FR_S/` holds nothing but formulas:

```
products/assurance_emprunteur/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  itt_inception_table.csv
  itt_termination_table.csv
  franchise_table.csv
  lapse_table.csv
  crd_rate_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  ADE_FR_S/                    <- formulas only
    __init__.py                   (model docstring)
    _system.json
    Data/__init__.py              (reads the CSVs, once per model)
    Projection/__init__.py        (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`. `Projection` is parameterized by
`point_id`, so the CSV readers live in an unparameterized **`Data`** Space and each file is
read once per model rather than once per model point; a test counts the reads.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_table_file` | `mort_table()` | `mort_table.csv` |
| `itt_inception_file` | `itt_inception_table()` | `itt_inception_table.csv` |
| `itt_termination_file` | `itt_termination_table()` | `itt_termination_table.csv` |
| `franchise_file` | `franchise_table()` | `franchise_table.csv` |
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `crd_rate_file` | `crd_rate_table()` | `crd_rate_table.csv` |

**There is no loan schedule file**, and that is the point of `check_crd()`.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | The twelve cells above, with a `policy_id` column | anchor cell **[std]**, technical notes; the guarantee structure and age limits [S9] [S11] [S13] |
| `mort_table.csv` | Healthy-life annual mortality at pivot ages 30–85, by sex, with a `provenance` column | **[std]** proxy shaped from INSEE population data [REG-R24] — *not* TH 00-02 / TF 00-02 [REG-R22] [REG-R23], which are cited by name and not redistributable; female rows are 0.60 × male |
| `itt_inception_table.csv` | Annual ITT claim-payment inception rates at pivot ages 30–69, by sex | **[std]**; the male / 90-day column is the notes' proxy table verbatim, female rows are ×1.30 |
| `itt_termination_table.csv` | Annual recovery, ITT→IPT transition and death-in-claim rates by claim duration year: 0.55/0.30/0.15, 0.02/0.06/0.12, 0.02/0.03/0.04 | the notes' **[std]** proxy table verbatim; no French anchor |
| `franchise_table.csv` | The inception multiplier by *franchise*: 1.60/1.25/1.00/0.85/0.65 for 30/60/90/120/180 days | menu sourced [S9]; factors **[std]** |
| `lapse_table.csv` | Annual *résiliation* by policy year: 4 / 12 / 12 / 10 / 10 / 7 % | **[std]**; the published French series are counts of substitution *requests*, not lapse rates [R12] |
| `crd_rate_table.csv` | The CRD-basis annual premium rate at pivot ages 30–70, 0.14 % to 2.90 % | **[std]** tariff, calibrated to the anchor cell's level scale to 0.11 % |

**No input column is the model's `t`, so the move to the 0-based time index left every CSV
untouched.** The time-like columns, and why each stands:

| File | Column | Decision |
|---|---|---|
| `lapse_table.csv` | `policy_year` | a contractual **1-based label**, 1 … 6, read as `policy_year(t) = t // 12 + 1` with years past the table taking its last row. Values unchanged |
| `itt_termination_table.csv` | `claim_duration_year` | on the **claim clock** `z`, not on `t`: read as `claim_dur_year(z) = (z − 1) // 12 + 1`, 1-based because claim payment starts at `z = 1`. Values unchanged |
| `model_point_table.csv` | `loan_term_months` | a **count** of months and the value of `proj_len()`, the exclusive end of the frame. Unchanged: 240 months are still 240 months, now indexed 0 … 239 |
| `model_point_table.csv` | `claim_duration_months` | an **elapsed count** on the claim clock (`z0` = 18 on model point 9, which therefore opens in cohort `z = 19`). 0-based by nature, unchanged |
| `model_point_table.csv` | `itt_max_days` | a contractual duration in days, 1 095. Not a time index |

The remaining keys — `age` in `mort_table.csv`, `itt_inception_table.csv` and
`crd_rate_table.csv`, `franchise_days` in `franchise_table.csv`, `point_id` — are
attributes, not time. There is no column holding a point on the frame's time axis, because
every model point projects from adhesion: the in-claim cells carry their claim duration as
an attribute rather than starting the frame late.

Mortality, ITT inception and the CRD premium scale are interpolated **linearly** between
pivot ages and **held flat** outside them. The flat extrapolation is deliberate and is what
produces the CRD premium of EUR 31.65 in policy year 20, where the attained age of 71 is
past the last pivot: extrapolating the scale linearly instead would invent a rate no table
supports. Note the contrast with `IP_UK_S`, which extrapolates its inception pivots
linearly — two products, two rules, and each model follows its own notes.

## Sign convention

`net_cf(t)` is **income positive**, the library-wide convention. The technical notes print
the stream outgo-positive, and that orientation survives verbatim as `liability_cf(t)` =
`ben_deces + ben_ptia + ben_itt + ben_ipt + expenses − prem`, with
`net_cf(t) == -liability_cf(t)` exactly. Both are columns of `result_cf()`, so the notes
and the model can be compared line by line without a mental sign flip.

Death, PTIA, *résiliation* and expiry generate no payment beyond what `claims()` carries.
`claims(t, "LAPSE")` and `claims(t, "MATURITY")` are published and are zero: there is **no
surrender value** at any time and **no maturity benefit**, and those facts are stated rather
than inferred from a missing column.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE`: `pols_*` for
population counts, plural nouns for cash flows, `*_rate` for annual rates and `*_rate_mth`
for monthly ones, `*_pp` for per-policy amounts, `claims(t, kind)` with an uppercase `kind`
string. The full symbol mapping lives in the `Projection` Space docstring. Four cases
needed care:

| Notes | Cells | Why |
|---|---|---|
| `ben_deces`, `ben_ptia` | `claims(t, "DEATH")`, `claims(t, "PTIA")` | `claims` is the library's one benefit-outgo cells and `kind` names the column it produces, so the kinds are English. The French terms stay in the prose, where they are the name of the thing |
| `q_h` / `q_s(z)` / `q_ipt` | `mort_rate` / `itt_mort_rate` / `mort_rate_ipt` | three mortality rates on two clocks. `mort_rate` is the **healthy-life** rate, because that is what it means in every model in this library; reading a claimant rate out of it is the mistake the naming prevents |
| `l_h(t+1)` vs `l_h(t)` | `pols_healthy_close(t)` vs `pols_healthy(t)` | the library indexes states at the **start** of the month so every cash flow on a `result_cf()` row is weighted by a state count on the same row. The notes' own end-of-month quantities — the states at time `t + 1` — are published too, so the worked-example table reads off directly |
| `ι` and `i_rate` | `itt_inception_rate_mth(t)` and `pols_itt_inception(t)` | the cells is the pure basis rate; the guarantee indicator `I(t)` is applied where the decrement is taken, exactly as the notes write it |

`t` is the 0-based policy month and `z` the 1-based claim duration. They are different
clocks and the model never mixes them: rates out of ITT take `z`, rates out of healthy
take `t`.

## Standardizations used

Everything in this list is **[std]**: the entire experience basis — healthy-life mortality,
the PTIA-to-death ratio of 0.10, ITT inception, the three ITT termination rates, the 0.35
split at the 1 095-day cap, the ×3.0 IPT mortality factor and the *résiliation* table — and
the factors that spread the inception pivots across sex and *franchise*; the linear pivot
interpolation and its flat extrapolation; the CRD premium scale and the level rate on every
`capital_initial` cell; the annual-to-monthly conversion `1 − (1 − r)^(1/12)` for every
decrement; death-then-PTIA-then-*résiliation*-then-inception as the order out of healthy and
recovery-then-transition-then-death as the order out of ITT; whole-month benefit payment in
place of daily pro-rating; maintenance EUR 30 a year and claim management EUR 250 a year,
both inflating at 1.8 %; the flat 2.5 % discount rate used only for present values; the
dynamic substitution response (`lapse_beta` 3.0, `lapse_rate_max` 0.35,
`subst_acceptance` 0.88, `market_prem_ratio` 1.0, so the uplift is off in the base run); the
anti-selection lever `selection_load` at 0; the claim admission ratio `claim_admission` at
1.00, against observed declines of 7.7 %–16.3 % on incapacity claims [R12]; and holding the
amortisation schedule fixed, an early-repayment decrement being a documented extension
[S9] [S10].

Three things are deliberately **not** modelled and the notes say why: multi-head
aggregation, *perte d'emploi*, and IPP and every partial benefit below the 66 % threshold,
where the market's benefit shape is not agreed — a linear ramp at two insurers
[S1] [S11] against a flat 50 % at three others [S5] [S9] [S10].

## Tests

`tests/test_assurance_emprunteur_fr.py` asserts the notes' fifteen-month worked example to
the cent and its state probabilities to six decimals — keyed `t = 0 … 14`, since the
frame is 0-based, with the CRD column read as `crd(t + 1)` — the column sums, the derived
monthly rates, the loan spine both ways, the ITT cohort survival table through the
1 095-day cap, the present values over the full 240 months, and one test per modelling
pitfall the notes name — the CRD read from a table, the wrong rate conversion, Décès and
PTIA collapsed, the premium falling with the cover, the duration dimension collapsed or
the cap dropped, the ITT → IPT movers paid twice or not at all, premiums charged to lives
in claim, *quotité* applied twice, and the "decreasing" premium that rises.
`test_result_cf_shape` pins the frame itself at `list(range(240))`, and
`tests/test_model_conventions_fr.py` asserts library-wide that the index is contiguous,
starts at or after 0 and ends at `proj_len() - 1`.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #frlib-assurance_emprunteur-r1
[R12]: #frlib-assurance_emprunteur-r12
[R3]: #frlib-assurance_emprunteur-r3
[REG-R22]: #frlib-reg-r22
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R35]: #frlib-reg-r35
[REG-R4]: #frlib-reg-r4
[REG-R5]: #frlib-reg-r5
[std]: #frlib-std
<!-- END generated citation links -->
