# Implementation Notes

**Status:** Draft, 2026-08-26. Built from
[`products/assurance_vie_uc/technical-notes.md`](technical-notes.md);
the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The
> contractual mechanics are sourced — the unit **count** as the only thing guaranteed
> [R2], the death benefit as the account value plus the `capital sous risque` [S1] [S3]
> [S4], the 300,000 € cap with the excess reducing the floor [S1] [S3] [S4], cessation at
> attained age 75 [S1] [S3] [S4] [S7], the charge levied on the net amount at risk by
> attained age under the published formula `Pr = K × (PA/10 000) × 1/52` [S4 Annexe I],
> the levy taken from the euro support first [S1] [S3] [S4], the pro-rata split of a
> partial surrender [S10 ART 13.A], the surrender value as the account value with no exit
> charge [S1] [S3] [S4] [S7] [S10] [S11] [S13], charges applied by cancelling units [S7]
> [S13 art. 32.4], and `prélèvements sociaux` of 17.2% falling on the UC leg only at
> `dénouement` [R8 II, 3°, c)](#frlib-assurance_vie_uc-r8) [S4 Annexe II]. The Spirica tariff itself is sourced and is
> shipped verbatim [S4 Annexe I]. Every **rate** is a **[std]** standardization. No
> insurer publishes the mortality table, the age definition, the loading or the margin
> behind a plancher tariff [S1] [S3] [S4] [S7]; art. A. 335-1 permits only homologated or
> certified tables, so TH 00-02 / TF 00-02 are cited and **not shipped** [REG-R23]
> [REG-R24]; no French persistency or arbitrage study was retrieved; and no unit-return
> assumption is published beyond the ±10% disclosure conventions. So the mortality basis,
> the surrender table, the charge levels and the return scenarios are placeholders.

## Run it

```bash
python products/assurance_vie_uc/run.py         # the worked-example anchor cell
python products/assurance_vie_uc/run.py 2       # the base run, 360 months
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/assurance_vie_uc/UC_FR_S")
model.Projection[1].result_cf()
```

`result_av()` gives the account value recursion column for column as the notes' worked
example prints it; `result_cf()` gives the cash flows.

## The unit / non-unit decomposition is the model

French practice splits this contract exactly as UK practice splits a unit-linked bond —
`products/unit_linked_bond/` in `uklib` is the same recursion — and so does this
implementation:

**The unit leg** — a **count** of units valued at an exogenous liquidation value. Art.
A. 132-5 requires the information document to state that the insurer "ne s'engage que sur
le nombre d'unités de compte, mais pas sur leur valeur" [R2], and every retrieved contract
reproduces it [S1] [S3] [S4 art. 17.1.1] [S7] [S10 ART 9.A] [S13 art. 32.5]. The
consequence is mechanical and total: the state variable is `units(t)`, every charge is a
cancellation, and the account value is `units × unit_price`.

**The non-unit cash flow** — what accrues to the insurer: the `frais sur versement`, the
UC management charge, the `frais d'arbitrage` and the plancher premium, less expenses and
the plancher **death strain**.

### 1. Every benefit is funded from the policyholder's own account

Death, surrender and partial surrender all come out of the two legs, so a naive gross
presentation counts the same money twice. `net_cf` here is therefore the **non-unit**
stream:

```
net_cf(t) = frais sur versement + mgmt_fee_uc + arbitrage_fee + plancher_charge
            − expenses − plancher_strain
```

The gross flows are still published — `claims_death`, `claims_lapse`, `withdrawals` and
`av_releases` are `result_cf()` columns — and `check_benefit_funding()` asserts they net
exactly:

```
claims(t) − av_releases(t) − plancher_strain(t) = 0
```

### 2. The death strain is the `capital sous risque`, exactly

```
death benefit = max(plancher_amount, account value) = account value + capital sous risque
```

so the insurer's cost per death is `nar(t)` and nothing else. At `t = 11` on the anchor
cell — its twelfth and last month — the benefit per death is **93,972.82 €** and the strain
is **16,642.74 €**.

One centime-level subtlety is worth stating: the benefit is the floor **less that month's
premium**, because the levy is in arrears against a `capital sous risque` observed before
it. `94,000.00 − 27.18 = 93,972.82`. That half-month timing difference is the **[std]**
discretization of a design that observes weekly and levies monthly [S1] [S3] [S4]
(spec footnote 16).

### 3. Three amounts that move on this contract are not insurer cash flow

| Amount | Insurer income? | Why |
|---|---|---|
| `Frais sur versement` | **yes** | deducted from the premium before allocation |
| UC management charge | **yes** | the charge for managing the contract |
| `Frais d'arbitrage` | **yes** | the price of the switch |
| Plancher premium | **yes** | the price of the guarantee |
| `Prélèvements sociaux` | no | withheld from the policyholder and remitted [R8] |
| Fund-level recurring costs | no | inside `unit_price`, paid on to the fund manager [R13] |
| Euro credited interest | no | a policyholder credit; the euro margin is `Euro_FR_S`'s |

`social_levy_uc` is published as its own `result_cf()` column precisely so its *exclusion*
from `net_cf` is visible rather than merely asserted. The fund-level costs are not a
column at all, because they never leave the unit price — but adding the market-average
1.60% p.a. [R13] to the anchor cell's year 1 would put **1,136.76 €** against a true
`net_cf` of **1,262.66 €**, which is the measure of how badly counting them would mislead.
Both figures are survivorship-weighted at the start-of-month `pols_if(t)`, which is the only
way the two are comparable; the **unweighted** per-policy sum is 1,152.86 €, and setting
that against a weighted `net_cf` overstates the distortion by about 16 €.

## The garantie plancher is the modelling heart

The whole of the rider is one expression:

```
nar(t) = min(cap, max(0, plancher_amount(t) − av_pp_at(t, "BEF_LEVY")))
plancher_charge_pp(t) = nar(t) × plancher_rate(t) / 12
```

and four listed pitfalls live inside it.

**The charge base is the risk, not the account value** [S4 Annexe I]. At `t = 11` on the
anchor cell the correct charge is `16,642.74 × 0.0196/12 = 27.18 €`; on the account value
it would be `77,357.26 × 0.0196/12 = 126.35 €`, a factor of 4.6. Out of the money the
charge is **exactly zero** [S3 art. 21] [S4 art. 17.1.2] — model point 11 runs a rising
path for thirty years and pays nothing at all.

**The net amount at risk is floored at zero.** Without the `max(0, ·)` the rider pays a
negative premium in every rising month and the death strain becomes negative, which books
the gain on the policyholder's units as insurance profit. `check_nar_bounds()` asserts it
on every model point and every month.

**The cap is on the risk, not the benefit** [S1] [S3] [S4]. Model point 10 runs it: the
shortfall exceeds 300,000 € and `nar` sits exactly on the cap, so the beneficiary still
receives `account value + 300,000` rather than a benefit truncated at 300,000.

**An arbitrage never moves the floor.** `cum_prem_net` changes on premiums and surrenders
only [S1] [S4] [S7] [S10] [S13]; the 10,000 € switch at `t = 2` leaves
`plancher_amount = 99,000.00`. `check_floor_base()` rebuilds the floor base from the
withdrawal series by a second accumulation, so a model that let the switch move it shows a
10,000 € residual.

### The three floor bases, on one path

| Basis | `plancher_amount(11)` | `nar(11)` | Year-1 premium |
|---|---:|---:|---:|
| `simple` | 94,000.00 | 16,642.74 | 82.80 |
| `indexee`, 3.50% p.a. [S1] [S3] | 97,378.25 | 20,041.15 | 108.39 |
| `cliquet`, 12-month ratchet **[std]** | 94,216.29 | 16,860.46 | 84.57 |
| `cliquet`, 1-month ratchet **[std]** | 98,476.25 | 21,155.09 | 126.04 |

`cliquet` is reduced by a partial surrender **proportionally** and `simple` **nominally**,
which is the only reason the two differ in a year whose ratchet date locks in nothing:
`99,000 × (1 − 5,000/103,476.25) = 94,216.29` against `99,000 − 5,000 = 94,000.00`. A
ratchet is a value level, not a premium tally. **No retrieved document offers a ratchet**
at all [unverified], so `cliquet` is carried as a standardization (spec footnote 15).

### The levy source decides whether the rider touches the units

Under `euro_first` the premium comes off the euro support and the unit count is untouched
[S1] [S3] [S4]: `units(11)` is **745.036125** against **744.044774** under `uc_units` on
the same path. If the two agree, the levy is not being applied at all. `av_uc_pp(11)` is
58,136.28 € in all four `plancher_basis` variants for the same reason.

Where the euro balance cannot cover the premium the remainder cancels units whatever the
election, and the count then becomes path-dependent. Model point 10 is 100% UC and runs
that branch from the first month, `t = 0`; it is the mechanism by which a lower euro
credited rate reaches the UC leg.

### The cover stops, and so does the tariff

`nar(t)` is zero from attained age 75 [S1] [S3] [S4] and the shipped tariff stops at 74,
because the cover does. `plancher_rate()` **raises** on an attained age inside the cover
but outside the table rather than extrapolating: extending the cessation age to 80 [S12]
[S13] needs a tariff the sources do not contain, and an implementation that extended the
curve would silently invent a price. Model point 9 is issued at 73 and exercises the
cessation; a test pushes `plancher_end_age` to 85 and asserts the raise.

## The month, in the order it happens

Per policy, within month `t`:

```
p(t)  = p(t−1)(1 + r_uc(t))                     the liquidation value moves
V     = V(t−1)(1 + i_e)^(1/12)                  the euro leg accrues
n     = n(t−1) − n(t−1)·c_m                     the charge cancels units
V    -= A(t) ;  n += A(t)(1 − φ)/p(t)           the arbitrage settles
W(t) split pro rata ; n -= W_uc/p(t) ; V -= W_eur
F(t), K(t) observed on U + V                    the floor and the risk
plancher premium levied, euro first
decrements at end of month, deaths before surrenders
```

`p(t−1)`, `n(t−1)` and `V(t−1)` are the **opening** balances of month `t`, which in the
first month, `t = 0`, are the balances at issue. The model reads them through
`unit_price_open(t)`, `units_open(t)` and `av_euro_open_pp(t)` — cells that return the
`*_init` value at `t = 0` and the previous month's close thereafter — so no formula ever
indexes a month `t = −1`.

Two points in that order are load-bearing.

**The management charge is taken on the opening unit count** [S7] [S13 art. 32.4]. In a
month with an arbitrage the opening and closing counts differ by the arbitrage's units:
52.28 € against 59.54 € at `t = 2`. Immaterial monthly, systematic over decades, and a
common source of a persistent reconciliation break against an admin system.

**The monthly rate is `c/12` and not `1 − (1 − c)^(1/12)`.** The insurers compound the
*periodic* rate: 0.25% a quarter gives an annual factor of `(1 − 0.0025)^4 = 0.99003744`,
not `1 − 1.00%` [S1] [S2]. The same recursion at 0.1875% a quarter reproduces Bourso Vie's
printed eight-year table digit for digit — 99.2521, 98.5098, 97.7731, 97.0418, 96.3161,
95.5957, 94.8808, 94.1711 [S3 art. 21] — and the tests assert it.

`av_pp_at(t, timing)` exposes `"OPENING"`, `"BEF_FEE"`, `"BEF_WD"`, `"BEF_LEVY"` and
`"BEF_DECR"` so the ordering is inspectable rather than buried in one expression, and
`check_av_roll_fwd()` asserts the identity every month — starting from
`av_pp_at(t, "OPENING")` — against a UC return built from the opening unit count and a euro
credit built from the opening balance.

## Prélèvements sociaux: the asymmetry is statutory

Art. L. 136-7 II, 3°, a) levies the contribution on the euro component **annually**, as
interest is credited; II, 3°, c) levies it on the unit-linked component only at
`dénouement` [R8] [S4 Annexe II]. So the UC levy is contingent on a **gain**:

```
gain(X) = X × (1 − uc_cost_basis / av_uc)      social_levy = 17.2% × max(0, gain)
```

At `t = 5` on the anchor cell the surrender's gain component is `4,033.25 × (1 −
79,250.00/83,469.22) = 203.87 €` and **35.07 €** is withheld. At `t = 11` the UC leg is
**17,284.34 € under water**, so a death withholds nothing — and any excess already levied
year by year on the euro leg is restituted at final liquidation under art. L. 136-7
III bis [R8]. Accruing the UC levy annually is a listed pitfall: it would understate the
account value throughout and shrink the base the management charge is levied on. The euro
leg's annual component belongs to `Euro_FR_S`, which runs on the same monthly grid and
lands the whole of the year's levy in the anniversary month, beside the interest it is
struck on. Whether the plancher top-up above the
account value sits inside the levy base is stated in **no retrieved document**; the model
puts it outside and flags the treatment [unverified] (spec footnote 21).

## Behaviour, and why the anchor cell runs the table alone

Two multipliers sit on the base surrender table, both **[std]** and both elected per model
point through `lapse_dynamic`:

| Overlay | Formula | On the anchor |
|---|---|---|
| Performance | `M_perf = min(2, 1 + 2·max(0, g_ref − R_12m))` | 1 — it reads a **completed** trailing year, so it cannot bite before `t = 12` |
| Plancher moneyness | `M_pl = 0.5` while `nar(t) > 0` | not applied: `lapse_dynamic = "none"` |

`lapse_dynamic` is a **[std]** election introduced here and not in the technical notes.
The notes' worked example states a flat `lapse_rate` of 2.00% a year and asserts
`l(12) = [(1 − q_m)(1 − w_m)]^12 = (1 − 0.012)(1 − 0.020) = 0.968240` exactly — twelve
months of decrements, so the cells is `pols_if_at(11, "AFT_DECR")`, see Sign convention
below — which is the check that the monthly rates were derived geometrically rather than by
dividing by twelve — and the moneyness multiplier would break it from `t = 7`, where the
floor starts
to bite. The election keeps both: the anchor cell reproduces the notes, and model points 2,
9 and 10 run the dynamics. It is the right shape for the assumption anyway. `M_pl` is a
pure invention with no evidence behind it and it moves the rider's result in **both**
directions at once — hold the in-the-money policies and the strain rises, but so does the
premium income — so it should be the first thing a user replaces, and a user replacing it
needs to see the base run underneath.

The duration-8 spike in `lapse_table.csv` is the one shape that is not arbitrary: art.
125-0 A CGI makes the eighth anniversary the point at which the withholding falls to 7.5%
and the 4,600 € / 9,200 € annual `abattement` opens [REG-R40] [S4 Annexe II], and eight
years is the recommended holding period in both retrieved DICs [S5] [S12]. There is no
paid-up state — the contract is single premium — and the 30-day `renonciation` [REG-R29]
is carried inside the year-1 rate rather than as a separate decrement.

## Inputs are external files

The five input CSVs live **in this directory**, beside `run.py` — not inside the model
folder. `UC_FR_S/` holds nothing but formulas:

```
products/assurance_vie_uc/
  model_point_table.csv        <- inputs live here
  mort_table.csv
  lapse_table.csv
  plancher_rate_table.csv
  uc_scenario_table.csv
  run.py
  model.md
  product-spec.md              <- the documents this model implements
  technical-notes.md
  sources.md
  UC_FR_S/                     <- formulas only
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
| `lapse_table_file` | `lapse_table()` | `lapse_table.csv` |
| `plancher_rate_table_file` | `plancher_rate_table()` | `plancher_rate_table.csv` |
| `uc_scenario_table_file` | `uc_scenario_table()` | `uc_scenario_table.csv` |

Note what is **not** an input file. The charge rates and every attribute of the rider
except its tariff are **model point columns**, because they are per-policy contractual and
discretionary parameters rather than experience assumptions: art. A. 132-8 requires charge
*maxima* to be disclosed and not capped [REG-R30], and the retrieved contracts span 0.475%
to 1.50% on the management charge alone [S1] [S11], so a single shipped rate card would
assert a market fact that does not exist.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Eleven model points. **Point 1 is the worked-example anchor** (M65, 100,000 €, 70/30, `simple` floor, `euro_first`, one-off arbitrage and surrender, `stress_yr1`, 12 months); 2 is the base run over 360 months with programmed withdrawals, progressive arbitrage and the dynamics on; 3, 4 and 5 are the `indexee` and the two `cliquet` variants; 6 switches the levy to `uc_units`; 7 declines the rider on a path where the floor is 25,280 € in the money; 8 puts the floor on gross premiums; 9 is issued at 73 and runs through the cessation age; 10 is a 2,000,000 € 100%-UC cell that binds the cap and levies on units; 11 is a female 45 on `gestion pilotée` charges and a rising path | anchor cell **[std]**, technical notes' worked example |
| `mort_table.csv` | Base annual mortality by sex and age 12–120, capped at 1 | **[std]** proxy shaped like the INSEE national series [REG-R24], anchored so the 0.8 best-estimate factor gives the notes' `q(M,65) = 1.20%` placeholder exactly — *not* a homologated or certified table [REG-R23] |
| `lapse_table.csv` | Annual total-surrender rates by policy year: 2 / 4 / 6 / **12** / 6 % | **[std]**; no public French persistency study was retrieved. The year-8 spike is art. 125-0 A CGI made behavioural [REG-R40] |
| `plancher_rate_table.csv` | Annual premium per 10,000 € of `capital sous risque`, ages 12–74 | **Sourced**: Spirica's published tariff [S4 Annexe I], carried verbatim from `_research/assurance-vie-uc.md` §7. The only sourced quantitative table this model ships |
| `uc_scenario_table.csv` | Three UC return paths as month segments, the months 0-based like the frame: `stress_yr1`, `base_490` (4.90% p.a. [R13]), `bear_5pct` | **[std]**; the path is exogenous and no stochastic generator is specified |

## Sign convention

`net_cf` is **income-positive**, as everywhere in this library: charges collected less
expenses and the death strain. The technical notes present the same stream income-positive,
so there is no `liability_cf` companion on this product.

Balances are read at the **end** of month `t` after that month's levy, so each row's
`av_euro_pp` is the next row's opening euro balance — which is how the notes' table prints
it, and why the check on row `t = 8`, `94,000.00 − (87,098.23 + 11.25) = 6,890.52`, closes
on itself. `pols_if(t)`, by contrast, is read the other way round: it is the in-force
probability at the **start** of month `t`, so `pols_if(0) = pols_if_init() = 1` and the
`result_cf()` frame opens on it. That is the library's settled ruling — the exposure column
on a row is the weight actually carried by the flows on that same row, so dividing a flow by
it returns the per-policy amount. The end-of-month count has its own name,
`pols_if_at(t, "AFT_DECR")` — the notes' `l(t+1)` — and it is what the account-value
**stock** `av_at(t, timing)` is weighted by:
`av_at(11,"BEF_DECR") = 77,330.08 × 0.968240 = 74,874.07`.

This model shipped once with the end-of-month count published under the `pols_if` name
while every flow beside it was weighted at the start-of-month one. Nothing raised and
nothing went NaN — the column was simply the right series one month stale — which is why
`test_pols_if_is_the_weight_on_its_own_row` asserts it now. The rename moved **only** the
`pols_if` column: every other column of `result_cf()` is unchanged on all eleven model
points.

## The time index

`t` is the policy month and is **0-based**, as everywhere in this library and in lifelib:
`t = 0` is the issue month, month `t` runs from time `t` to time `t + 1`, and the frame is
`t = 0 … proj_len() − 1`, so `result_cf()` and `result_av()` each have exactly `proj_len()`
rows on every model point — twelve, `t = 0 … 11`, on the anchor cell. `proj_len()` is a
**count of months**, the exclusive end of the frame, not the last index. The contractual
policy year is the 1-based derived label `policy_year(t) = duration(t) + 1` with
`duration(t) = t // 12`, and `age(t) = issue_age() + duration(t)`.

The issue instant is **not a row**. The balances at issue are the `*_init` cells —
`unit_price_init`, `units_init`, `av_euro_init_pp`, `cum_prem_net_init`,
`uc_cost_basis_init`, and `prem_to_av_pp` for the total — and month 0 opens on them through
four opening cells: `unit_price_open(t)`, `units_open(t)`, `av_euro_open_pp(t)` and
`av_pp_at(t, "OPENING")`. Each returns the `*_init` value at `t = 0` and the previous
month's close for `t ≥ 1`, which is what keeps every recursion off a month `t = −1` and
keeps the first row's opening and closing balances distinct. The `frais sur versement` and
the 400 € acquisition expense are therefore beginning-of-period flows of month `t = 0`:
`prem_charge(0) = 1,000.00`, `expenses(0) = 403.33` (400 acquisition + 40/12 maintenance)
and `net_cf(0) = 647.99`, weighted at `pols_if(0) = 1`.

Two clocks follow from the index and are worth stating, because both are places an
off-by-one hides. The `cliquet` ratchet date is the **end** of month `t`, which is `t + 1`
months from issue, so an `n`-month ratchet fires where `(t + 1) % n == 0` and the first
annual ratchet is the end of `t = 11`. And `return_12m(t)` reads the twelve **completed**
months ending at the start of month `t`, so it is undefined — and `perf_factor` exactly 1 —
for `t < 12`.

### What the input CSVs are keyed on

| File | Column | 0-based? | Decision |
|---|---|---|---|
| `lapse_table.csv` | `policy_year` | no | A **contractual 1-based label**, 1 … 40. The file is unchanged; `lapse_rate_base(t)` maps through `policy_year(t) = t // 12 + 1` |
| `uc_scenario_table.csv` | `from_month`, `to_month` | **yes** | Segment bounds compared directly against the frame's `t` (`from_month ≤ t ≤ to_month`), so they are the model's own months under another name and were **shifted by −1**: `stress_yr1` is now 0–5 and 6–11, the two long scenarios 0–599 |
| `model_point_table.csv` | `wd_month`, `arb_month` | **yes** | Points on the frame's time axis, compared with `t ==`, so they **shifted by −1**: the anchor's surrender moves 6 → 5 and its arbitrage 3 → 2. The `0` in rows whose pattern is `none`, `programmed` or `progressive` is an unused placeholder the formula never reads, and it stays `0` |
| `model_point_table.csv` | `proj_len` | n/a | A **count** of months, unchanged: 12, 120, 240, 360 |
| `mort_table.csv`, `plancher_rate_table.csv` | `age` | n/a | Keyed by attained age, not by time; unchanged |

## Naming

Cells follow lifelib's `savings/CashValue_SE` and the account-value vocabulary this
library settled on. The full symbol mapping lives in the `Projection` Space docstring.
Five cases needed care:

| Notes | Cells | Why |
|---|---|---|
| `mgmt_fee_uc(t)` | `mgmt_fee_uc_pp` / `mgmt_fee_uc` | The notes' quantity is per policy; the library reserves the unsuffixed name for the in-force-weighted flow. Same split for `plancher_charge_pp` and `arb_fee_pp`. It is why the notes' table sums to 630.20 and the extraction to 621.33 |
| `l(t)`, `l(t+1)` | `pols_if(t)`, `pols_if_at(t, "AFT_DECR")` | The library's settled ruling: `pols_if(t)` is the **start**-of-month count and the weight on its own `result_cf` row, so the end-of-month count takes the `CashValue_SE` timing name instead. The old spelling — the end-of-month count published as `pols_if` — failed silently, which is why a test asserts the new one |
| `X_init` | `unit_price_init`, `units_init`, `av_euro_init_pp`, `cum_prem_net_init`, `uc_cost_basis_init` | The balances at issue, which are not a row of the 0-based frame. Month 0 opens on them through `unit_price_open`, `units_open`, `av_euro_open_pp` and `av_pp_at(t, "OPENING")` |
| `U(t)`, `V(t)` | `av_uc_pp` / `av_euro_pp` | The library calls a policyholder-owned fund `av_*_pp`; `av_pp_at(t, timing)` is the total |
| `net_cf(t)` | `net_cf` | The **non-unit** stream of the UC leg and the rider, not a gross total and not the contract's margin. Still income-positive |
| `W(t)` | `withdrawals` / `wd_amount_pp` | A partial surrender is an owner election, not a claim, so it is never a `claims` kind |

## Standardizations used

Everything in this list is **[std]**: the `frais sur versement` of 1.00%, the UC
management charge of 0.88% p.a. and the `frais d'arbitrage` of 0.50%; the `c/12` monthly
accrual and the `(1 + i_e)^(1/12)` euro accrual; the euro credited rate of 2.50% net, which
is a pointer to `Euro_FR_S` and not a model; the whole mortality basis and the 0.8
best-estimate factor; the surrender table and its duration-8 spike; the `cliquet` basis,
which no retrieved document offers at all; the `1/12` monthly step replacing the published
`1/52` weekly one, and the once-a-month observation of the `capital sous risque`; the three
return scenarios; the `lapse_dynamic` election and both multipliers behind it; acquisition
expense 400 € and maintenance 40 € a year, level; death-before-surrender as the processing
order; age last birthday; the pro-rata cost method behind the UC `prélèvements sociaux`
base; and the treatment of the plancher top-up as outside that base [unverified].

Deliberately excluded, per the notes and the specification: settlement frictions (J+3 value
dating [S10 ART 12.B], next-working-day arbitrage dating [S7], six-month deferral powers
[S7], the HCSF's surrender and arbitrage restrictions [REG-R13]); the 15–20 € monthly levy
thresholds and the unpaid-premium recovery procedure [S1] [S3] [S4]; the rider's
exclusions; trigger-based automatic arbitrage options (`sécurisation des plus-values`,
`limitation des moins-values`), which matter because they move value **out** of UC after a
rise and shrink the charge base and the plancher exposure together; support-level rules —
the 60% real-estate cap [S13 art. 32.6], reinvested distributions [S13 art. 32.3], bid/offer
spreads [S4] [S7], redemption gating [R7]; Afer's per-support PRUM floor [S11 Annexe 3],
which is a strip of per-support puts rather than one contract-level put; joint lives;
`avances` and `nantissement`; annuity conversion; and the `eurocroissance` leg, which
belongs to [`products/eurocroissance`](../eurocroissance/model.md).

**The euro leg is not implemented here.** `euro_credit_rate` is a single annual rate net of
the euro management charge, so the euro leg produces no margin line at all. `Taux minimum
garanti`, `participation aux bénéfices`, the `provision pour participation aux bénéfices`
and the `effet cliquet` are
[`products/assurance_vie_euro`](../assurance_vie_euro/model.md)'s. Reading `net_cf` as the
contract's total margin is a listed pitfall.

## Tests

`tests/test_assurance_vie_uc_fr.py` asserts the notes' worked example to the centime and
the unit count to the fourth decimal — the twelve-row table at `t = 0 … 11`, the issue
balances and the derived monthly factors, the year-1 per-policy totals and the
survivorship-weighted insurer-side extraction, the settlement arithmetic of the arbitrage
and the partial surrender, the death benefit at `t = 11`, and the four `plancher_basis`
variants on the same path — plus one
test for each pitfall the notes list: the charge base, the zero floor on the net amount at
risk, the cap on the risk, the arbitrage that does not move the floor, the proportional
`cliquet` adjustment, the opening unit count, the `c/12` convention, the levy source, the
UC social levy at `dénouement` only, the three pass-throughs, `net_cf` as the UC leg and
the rider alone, the cessation age with its refusal to extrapolate the tariff, and the
in-force frame — that the frame is `t = 0 … proj_len() − 1`, that `pols_if(t)` is the
start-of-month count, that each row's flows divide by their own row's `pols_if`, and that
the end-of-month count is `pols_if_at(t, "AFT_DECR")`. Two
independent reproductions sit alongside them: Bourso Vie's published eight-year unit table
[S3 art. 21] and Himalia's [S2], both digit for digit from the same recursion.

```bash
python -m pytest tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R13]: #frlib-assurance_vie_uc-r13
[R2]: #frlib-assurance_vie_uc-r2
[R7]: #frlib-assurance_vie_uc-r7
[R8]: #frlib-assurance_vie_uc-r8
[REG-R13]: #frlib-reg-r13
[REG-R23]: #frlib-reg-r23
[REG-R24]: #frlib-reg-r24
[REG-R29]: #frlib-reg-r29
[REG-R30]: #frlib-reg-r30
[REG-R40]: #frlib-reg-r40
[std]: #frlib-std
[unverified]: #frlib-unverified
<!-- END generated citation links -->
