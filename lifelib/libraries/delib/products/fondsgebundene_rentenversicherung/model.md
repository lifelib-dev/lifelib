# Implementation Notes

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30.
Built from [`products/fondsgebundene_rentenversicherung/technical-notes.md`](technical-notes.md);
the product it implements is specified in [`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing, reserving or disclosure result.** The
> *mechanics* are common ground in German practice and several are cited: the
> *Beitragsverrechnung* order and the purchase of *Anteileinheiten* at the *Anteilspreis*
> [S1], the *Höchstzillmersatz* of 25 ‰ of the *Beitragssumme* [R12] [R13] [REG-R16] and the
> even spreading of the acquisition charge over the first five contract years [R1] [REG-R28],
> the *Beitragsrückgewähr* death benefit [S2], the *Zeitwert* *Rückkaufswert* and the
> conditions on a *Stornoabzug* [R1] [REG-R36], the survival of the fund-based charges into a
> *beitragsfrei* contract [R3], the `max(guaranteed, current)` *Rentenfaktor* rule [S4] [R22],
> and the unisex tariff [REG-R34]. delib was drafted with HTTP egress blocked and nothing
> retrieved; the citations have since been re-verified against the primary documents, and
> **eighteen of the forty-four entries in `sources.md` now record a document that was opened
> and read**, twenty-four record none. **That verifies mechanics of the kind cited above and
> none of the levels below.** The **levels** are almost entirely **[std]**: **no lapse rate
> and no expense or commission scale was established anywhere**, and outside the single
> carrier whose rates could be read [S2] [S15] **no charge rate and no *Rentenfaktor* was
> established at any carrier** — that one tariff is a comparator the *Standardizations* table
> below measures the shipped levels against, not their source. The DAV tables behind both
> mortality bases — DAV 2008 T for the *Risikobeitrag* [R17] [REG-R48], DAV 2004 R behind
> the *Rentenfaktor* [R16] [REG-R49] — are
> Deutsche Aktuarvereinigung property and are **cited by name, never shipped**. Replace the
> charge scale, the decrement tables and the fund path with a real tariff and company data
> before drawing any conclusion from a number. Nothing here is an *Effektivkostenquote* and
> nothing here may be compared with a PRIIPs performance scenario [R8] [R9] [REG-R32].

## Run it

```bash
python products/fondsgebundene_rentenversicherung/run.py
python products/fondsgebundene_rentenversicherung/run.py 7    # the beitragsfrei cell
```

Three lines to the same thing:

```python
import modelx as mx
model = mx.read_model("products/fondsgebundene_rentenversicherung/FRV_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id` and `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by policy month `t` with one column per cash
flow line, and `result_fund()` the per-policy unit side — the *Anteilspreis*, the unit count,
the four within-month *Fondsguthaben* balances, the *Beitragsrückgewähr* base, the net amount
at risk and the three decrement rates, which is roughly what a German *Standmitteilung*
reports [S17]. `model.doc` describes the product and the basis, `model.Projection.doc` maps
the notes' symbols onto the cells names, and `model.Data.doc` says what each input file is and
what a replacement must preserve.

## The time index and the frame

`t` is the **0-based** policy month counted from the contract's own inception: `t = 0` is
the inception month, period `t` runs from time `t` to time `t + 1`, and `t = 60` means the
same thing on every model point — the first month after the acquisition-charge instalment
ends. `proj_len() = 12 × (annuity_age − entry_age)` is the **number** of policy months and
so the frame's **exclusive** end, so `result_cf()` covers `range(proj_start(), proj_len())`
— the last row is `t = proj_len() − 1`, which is 359 on the anchor cell, and
`len(result_cf())` is `proj_len() − proj_start()`. That is lifelib's own convention
(`basiclife/BasicTerm_S`, `savings/CashValue_SE`: `for t in range(proj_len())`), and it is
what the conventions suite asserts for every model point.

`proj_start() = duration_init_m` — **0** for new business and **96** for the in-force cell.
`duration_init_m` is an elapsed count and is therefore already 0-based, so it is the first
projected index itself and needs no `+ 1`; an in-force model point simply opens partway
through a frame whose origin is still inception. `pols_if(proj_start()) == pols_if_init()`
exactly, and `pols_if(proj_len()) = 0`, one past the last row.

The **contractual policy year is the 1-based label** `policy_year(t) = t // 12 + 1`, derived
from `t` and never indexed by, and `age(t) = entry_age + policy_year(t) − 1 = entry_age +
t // 12`. Because a 0-based frame has no `t = −1`, the opening *Anteilspreis* is its own cells,
`unit_price_open(t)` — `unit_price_init` at `t = proj_start()` and `unit_price(t − 1)` after it
— which is what `av_pp` and `units_bought_pp` read; the ledgers `cum_prem_pp` and
`cum_charge_acq_pp` likewise seed inside the frame's first month rather than one before it.

### What the CSVs did and did not do

| File | Column | Decision |
|---|---|---|
| `model_point_table.csv` | `duration_init_m` | **Unchanged.** An elapsed count, 0-based by nature; 96 stays 96 and is now `proj_start()` itself |
| `model_point_table.csv` | `pup_month` | **Shifted −1**: a point on the frame's time axis. Model point 7 goes *beitragsfrei* at `t = 120` (was 121). `0` stays the "never" **sentinel**, not the inception month |
| `model_point_table.csv` | `topup_month` | **Shifted −1**: model point 9 tops up at `t = 120` (was 121). `0` stays the "none" sentinel |
| `model_point_table.csv` | `wd_month` | **Shifted −1**: model point 9 withdraws at `t = 240` (was 241). `0` stays the "none" sentinel |
| `model_point_table.csv` | `entry_age`, `annuity_age`, `prem_term_y`, `prem_mode_months` | **Unchanged.** Ages, a term in years and a frequency in months — none is a point on the frame |
| `lapse_table.csv` | `policy_year` | **Unchanged.** The contractual 1-based label; `lapse_rate_base(t)` maps through `policy_year(t) = t // 12 + 1` |
| `fund_scenario_table.csv` | `policy_year` | **Unchanged**, for the same reason |
| `charge_table.csv` | `alpha_spread_months` | **Unchanged.** A count of months, not an index |
| `mort_table.csv` | `age` | **Unchanged.** An attained age |
| `rentenfaktor_table.csv` | `annuity_age` | **Unchanged.** An age at *Rentenbeginn* |

No `provenance` column was touched, and no row order changed.

## The insurer guarantees the number of units, not their value

Everything else follows from that sentence, and it is what makes this a unit-linked model
rather than a translation of the general-account ones beside it. There is no *Rechnungszins*
in the accumulation phase, no *Deckungskapital*, no *Zinsüberschuss* — and, because § 125 VAG
makes the covering assets a segregated *Anlagestock* held in the very units the liability is
denominated in [R15] [REG-R7], **no investment-mismatch term anywhere in the model**. The
state variable is therefore the unit count, and euro are derived from it:

```
units_pp(t + 1) = units_pp(t) + units_bought_pp(t) − units_cancelled_pp(t)
av_pp(t)        = units_pp(t) × unit_price_open(t)
```

`check_units_roll_fwd()` asserts the first line and `check_av_roll_fwd()` the account identity
that carries the price. They look redundant and are not, which is why both ship: **the unit
identity has no price term in it at all**, so it fails when a charge is taken in euro without
the matching units being cancelled while every euro total still looks plausible; the account
identity fails when the return is applied at the wrong point in the order. An implementation
can pass either one alone. The fund's **TER** is a third category and is deliberately given no `charge_*` cells: borne
inside the *Anteilspreis*, it never appears in a policy ledger, so
`fund_return_net_ann(t) = gross − ter` nets it off the assumed return instead. Charging it
explicitly double-counts; ignoring it overstates the policyholder's return.

## `net_cf` is the non-unit stream

Every benefit paid before *Rentenbeginn* — the death benefit up to the fund, the
*Rückkaufswert*, the *Teilentnahme*, the capital released at *Rentenbeginn* — is funded by
cancelling the policyholder's **own** units, so a gross presentation counts the same money
twice. **delib's first ruling** requires every model to publish `check_net_cf()`; the identity
here is one line:

```
net_cf = charge_acq + charge_admin_prem + charge_admin_fund + charge_policy_fee
         + charge_risk + stornoabzug − expenses − commissions − death_strain
```

Charges in, the insurer's own expenses, its commission and the death strain out, and nothing
else. `expenses` **excludes** commission and `commissions` is its own cells and its own
`result_cf()` column — the delib convention, stated the same way on `KLV_DE_S`, `Basis_DE_S`,
`Riester_DE_S` and `RLV_DE_S`, and the opposite of the frlib chassis, where commission sits
inside the expense total. Taking both conventions at once double-counts the commission.
`check_net_cf_resid(t)` does not restate that formula: it rebuilds the first two terms **by a
different route**, as `premiums − prem_to_av`, which is what the *Beitragsverrechnung* leaves
behind — so the check crosses the unit / non-unit boundary rather than asserting the code
against itself. The gross flows are published beside it rather than dropped. `premiums`, `prem_to_av`,
`claims_death`, `claims_lapse`, `claims_maturity`, `withdrawals` and `av_releases` are
`result_cf()` columns, all **excluded** from `net_cf`, and `check_benefit_funding()` asserts
that they net exactly:

```
claims_death + claims_lapse + claims_maturity + withdrawals + stornoabzug
    = av_releases + death_strain
```

Booking the whole *Fondsguthaben* as an insurer outgo is this product's first-order failure
mode — every column still looks reasonable and the liability is overstated by the entire fund
— and publishing the excluded columns is what lets a reader see what was excluded. The scale
of it on the anchor: 64 869,36 € of benefits against 40 586,28 € of premiums, of which
**4,39 € is an insurer cost**. Seven `check_*()` cells travel with the model, each a `bool`
over all `t` with a `check_*_resid(t)` companion — `check_net_cf`, `check_prem_split`,
`check_units_roll_fwd`, `check_av_roll_fwd`, `check_benefit_funding`, `check_pols_roll_fwd`,
`check_acq_charge` — and all seven are `True` on all thirteen model points.

## Withheld from the premium, or cancelled out of the fund

This is the distinction the product turns on and the model's most easily-hidden error. The
*Beitragsverrechnung* withholds the acquisition instalment and the premium-based
administration charge **before** any unit exists:

```
prem_to_av_pp(t) = B(t) + Z(t) − charge_acq_pp(t) − beta_rate × B(t)
units_bought_pp(t) = prem_to_av_pp(t) / unit_price_open(t)
```

while the *kapitalbezogene Verwaltungskosten*, the *Stückkosten* and the *Risikobeitrag* are
levied **after** the month's return, by cancelling units that already exist.
`check_prem_split()` asserts that the premium splits exactly three ways, so a model that also
netted the *Stückkosten* or the fund-based charge out of the *Beitrag* fails there. What the
model avoids is the shortcut that looks identical while premiums are paid: netting
`gamma` out of the *Beitrag* is right until the premium stops and wrong from then on. Model
point 7 goes *beitragsfrei* at `t = 120` on a zero-return fund, and from there `premiums(t)`
is zero while `charge_admin_fund(t)`, `charge_policy_fee(t)` and `charge_risk(t)` continue
and the fund decays — the product fact § 165 VVG makes possible [R3] [REG-R28], not a
modelling artefact. A *Zuzahlung* pays its own *Zuzahlungskosten* and **no**
*beitragsbezogene* charge, being no regular *Beitrag*; it is booked in `charge_acq`, which is
why `charge_acq(120)` is non-zero on model point 9.

## The acquisition charge, its window, and the in-force cell

`charge_acq_total() = alpha_rate × beitragssumme()` — **2,50 % of the sum of premiums
payable, the *Höchstzillmersatz* itself** [R12] [REG-R16] — spread in equal instalments over
`acq_window_months() = min(alpha_spread_months, 12 × prem_term_y)` months at the policy's own
premium frequency [R1] [REG-R28]. The composite takes the cap rather than a guessed interior
point, so the reference implementation demonstrates the binding constraint. On the anchor
cell that is 1 800,00 € over 60 instalments of **30,00 €** — 15 % of each of the first sixty
premiums, `t = 0 … 59`, and **nothing from `t = 60`**, where the *Anlagebeitrag* steps from
162,00 € to 192,00 €. That cliff is the characteristic shape of a German unit-linked
contract's early values and it is why this model runs monthly: an annual grid cannot place
the sixtieth month.

The instalment **count** is the window divided by the frequency — 60 monthly, 20 quarterly, 10
half-yearly, 5 annual, and **24** on model point 12, whose premium term is two years; a
shortened term still spread over sixty months would understate every instalment.
`check_acq_charge()` closes the ledger against an expectation **counted rather than
accumulated** — instalment dates elapsed times the instalment, plus the *Zuzahlungskosten* on
any *Zuzahlung* received — so a window running one month too long fails there.

`beitragssumme()` is the sum of premiums **payable at the initial level** and is invariant:
it does not shrink on lapse or *Beitragsfreistellung* and does not grow with a
*Beitragsdynamik* increment or a *Zuzahlung*. A real tariff re-zillmers each accepted
increment over its own sixty months, and an increment cannot be assumed at inception; the
bias that leaves is stated rather than hidden. Letting `S` follow the premiums actually paid
would make the acquisition charge a function of the lapse assumption — wrong, and circular.
An **in-force** model point opens after the window has closed: model point 6 starts at
`t = 96`, so `charge_acq(t)` is zero at every projected month **and** `commissions(96)`
carries no *Abschlussprovision*, `comm_acq_pp` and `expense_acq_pp` both falling at `t = 0`
and only there. That is the whole of the difference between an in-force cell and a
new-business one on this chassis.

## The *Beitragsrückgewähr*, and two mortality bases at once

The composite death benefit is `max(Fondsguthaben, Summe der gezahlten Beiträge)` [S2], so
the net amount at risk is `max(cum_prem_pp(t) − F, 0)` — positive early, vanishing once the
fund overtakes the premiums paid (`t = 94` on the anchor cell), returning after a market
fall. That makes `cum_prem_pp` a genuine **state variable** rather than a reporting
convenience, and the risk charge a quantity recomputed every month. It is the premiums
**paid**, gross: `cum_prem_pp(59) = 12 000,00 €` against 9 720,00 € actually invested, so
reading the floor off the invested amount would understate the death benefit by 19 %.

The floor at zero in `nar_pp()` is load-bearing. Without it the contract would pay the
insurer a negative charge in every month the fund is above the floor and `death_strain` would
turn negative, silently booking the fund's growth as insurance profit. And
`db_pp(t) = av_pp_at(t, "BEF_DECR") + nar_pp(t)` rather than `max(floor, fund)`: writing it as
a sum keeps the two sides apart, the first term being the policyholder's money and the second
the insurer's.

**The *Risikobeitrag* is priced on a death table and the conversion guarantee on an annuity
table.** `mort_rate_tariff_at_age` reads `mort_table.csv`, a **[std]** first-order DAV 2008 T
proxy [R17] [REG-R48]; `rentenfaktor_guar` reads `rentenfaktor_table.csv`, standing in for
DAV 2004 R [R16] [REG-R49]. **No cells reads both files** — the arithmetic form of the
statement that a German fondsgebundene contract carries two mortality bases at once; a model
pricing the death charge on an annuitant table understates it. The projection then decrements
on a **third** rate, the second-order best estimate `mort_be_factor = 0.75` times the tariff
rate [REG-R47]. The wedge is the *Risikoergebnis*, and because the factor is flat it is
exactly 25 % of the *Risikobeitrag* collected — 5,849973 less 4,387480 = 1,462493 € on the
anchor — a closed form a reader can check with a calculator. One basis for both makes the
risk result identically zero.

The two monthly conversions are deliberately different. Mortality is split **linearly**,
`mort_rate_mth = mort_rate / 12`, because the tariff's *Risikobeitrag* is `q(x)/12` times the
*riskiertes Kapital* and charge and decrement must share the split, or the model manufactures a
risk result out of a rounding convention. Lapse is split **geometrically**,
`1 − (1 − lapse_rate)^(1/12)`, because nothing is priced off it and the annual rate is the
observable to reproduce; the fund return compounds geometrically for the same reason, while
`gamma_rate_mth()` is `gamma_rate_ann() / 12` because a German tariff quotes charge rates
nominally.

## The *Rückkaufswert* is the *Fondsguthaben*

§ 169 VVG sends a fondsgebundene contract to the *Zeitwert*, and on a pure unit-linked
contract with no insurer-given guarantee the *Zeitwert* **is** the fund [R1] [REG-R28]. There
is no discounting, no *Rechnungszins*, no mortality basis, no *Zillmerung* residue and no
second-basis *Mindestrückkaufswert* anywhere in this model — the cleanest surrender rule of
the ten delib products. The protection sits earlier, in the sixty-month spreading, which is
why the surrender value is positive from the first month. A *Stornoabzug* is permissible only if *vereinbart*, *beziffert* and *angemessen*, and
**never for unamortised acquisition costs** [R1] [REG-R36]. `stornoabzug_pp(t)` is therefore
a flat rate on the *Fondsguthaben* and deliberately **not** a function of
`charge_acq_total() − cum_charge_acq_pp(t)`: that prohibition is what stops an insurer
recovering through the deduction what the five-year spreading denies it. Only `std_high`
carries a rate and only model point 5 uses it.

*Beitragsfreistellung* is a **model point election**, `pup_month`, not a cohort decrement —
the one place the model reproduces a mechanic exactly on one cell rather than approximately on
all of them. A paid-up policy's fund and its *Beitragsrückgewähr* base both depend on the
month it went paid-up, so a cohort rate would need one sub-cohort per month: a
two-dimensional recursion over 360 months for a second-order effect. The **[std]** 1 % p.a.
rate is recorded and not implemented, and the omission biases charge income **upward**.
*Storno* and *Beitragsfreistellung* stay two different things: one an exit paying the
*Rückkaufswert*, the other a change of state paying nothing [R2] [R3].

## The last month, the age at *Rentenbeginn*, and the reduction in yield

`lapse_rate_mth(proj_len() − 1) = 0` **[std]**. The end of the last projected month is
*Rentenbeginn*, so a
surrender and an annuitisation are the same event releasing the same *Fondsguthaben*, and the
whole surviving cohort is booked as `pols_maturity`. No cash flow moves either way; the
convention decides only the split between the lapse total and the maturity count, and it is
what the closure identity reproduces — deaths 0,04377181 plus lapses 0,65322937 plus maturity
0,30299882 = 1,00000000. It is frlib's convention on `TD_FR_S` and delib adopts it.

`age(proj_len() − 1) = annuity_age − 1`, because the annuity begins at the **end** of that month,
and the *Rentenfaktor* is read at `annuity_age`: **25,00 at 67 on the anchor, not the 24,45 an
off-by-one fetches at 66**, a 2,2 % understatement of the pension. The rule applied is
`max(rentenfaktor_guar(), rentenfaktor_curr())` [S4] [R22] — a guarantee **with upside**, so a
model applying only the guaranteed factor understates the benefit whenever the current tariff
is richer. On `std_2026` the two are equal, so the `max()` is exercised without an unsourced
uplift; model point 13 carries `rich_current`, 12 % higher, where it visibly bites. Only the
**conversion terms** are guaranteed; the capital they multiply is the market's, so a
guaranteed *Rentenfaktor* is not a guaranteed pension.

`reduction_in_yield()` is the product's defining metric, because on a contract with no
*Rechnungszins* the charge stack **is** the economics. It is `gross_return_ref() − irr_ann()`,
computed on a **single persisting contract** — no survivorship, no lapse — because a reduction
in yield is a statement about one policy. On the anchor 5,0000 % less 3,6593 % =
**1,3407 % p.a.**, and across the four shipped charge scales it moves by a factor of five.
**It is a delib-defined measure and not the statutory *Effektivkostenquote***, which is aligned
to the total-cost-indicator method of the PRIIPs RTS over a specified recommended holding
period [R7] [R9] [REG-R31] [REG-R32]; this model implements neither.

## Inputs are external files

The six input CSVs live **in this directory**, beside `run.py` — not inside the model folder.
`FRV_DE_S/` holds nothing but formulas:

```
products/fondsgebundene_rentenversicherung/
  model_point_table.csv  mort_table.csv  lapse_table.csv     <- inputs live here
  charge_table.csv  fund_scenario_table.csv  rentenfaktor_table.csv
  run.py
  product-spec.md  technical-notes.md  model.md  sources.md  <- the documents
  FRV_DE_S/                                                  <- formulas only
    __init__.py  _system.json                                   (model docstring)
    Data/__init__.py                (reads the CSVs, once per model)
    Projection/__init__.py          (the by-policy projection)
```

This follows lifelib's `annuallife/TradLife_A`, which keeps its inputs beside the model and
reads them at run time. It is the opposite of `basiclife/BasicTerm_S`, which stores its
inputs *inside* the model through modelx's IOSpec machinery — hence no `_data/` directory and
no embedded values here at all.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache; readers placed there would re-read every file for every policy. They
live instead in an unparameterized **`Data`** Space, which `Projection` references as `data` —
so each file is read once per model however many policies are projected. The conventions suite
counts the reads over a full sweep and asserts the file set, not merely the count.
`Data.input_dir()` resolves the location from `_model.path.parent` at read time, so it works
wherever the repository is checked out.

| Reference | Cells | File |
|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` |
| `mort_file` | `mort_table()` | `mort_table.csv` |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` |
| `charge_file` | `charge_table()` | `charge_table.csv` |
| `fund_scenario_file` | `fund_scenario_table()` | `fund_scenario_table.csv` |
| `rentenfaktor_file` | `rentenfaktor_table()` | `rentenfaktor_table.csv` |

**The trade-off:** the model is not portable on its own — copy `FRV_DE_S/` without the CSVs and
it reads fine, then fails on first evaluation — but a diff of the model shows logic changes
only, and an input can be swapped in place. **Every file but
`model_point_table.csv` carries a `provenance` column**, one tag per row, asserted by the
conventions suite: delib's second ruling, the citation discipline reaching the data files
rather than stopping at the prose. The model point table is the one exemption, a model point
being a *configuration* and not an assumption.

| File | Contents | Provenance |
|---|---|---|
| `model_point_table.csv` | Thirteen model points. **Point 1 is the anchor cell** (M37 / monthly 200,00 € / 30 years / *Rentenbeginn* at 67 / *Beitragsrückgewähr* / `std_gross` / `base`). Points 2–13 exercise the *Einmalbeitrag*, all four frequencies, a `pct_fund` and a `sum_assured` death benefit, an in-force cell opening at duration 96, a *beitragsfrei* cell on a zero-return fund, a *Zuzahlung* and a *Teilentnahme*, a *Beitragsdynamik*, a *Nettotarif* on an ETF, a two-year premium term on a stress path, a non-zero *Stornoabzug*, and a *Rentenbeginn* at 70 where the `max()` bites | anchor cell **[std]**, the notes' worked example |
| `mort_table.csv` | First-order annual death rates, ages 18–100 | **[std]** Gompertz proxy `0.00080 × 1.10^(age − 37)`, **anchored at `q(37) = 0.00080`** — the value the worked example rests on. *Not* a DAV table; those are cited and never shipped [R17] [REG-R48]. It stands for whichever first-order death basis a tariff uses, which at the one carrier that could be read is 65 % of DAV 1994 T rather than DAV 2008 T [S2]. A replacement must preserve the anchor, an insured-lives gradient and a first-order margin **above** best estimate |
| `lapse_table.csv` | Annual lapse: 6 % in years 1–5, 3 % in 6–10, 2 % in 11–12, 3 % from 13 | **[std]** — **no German unit-linked *Stornoquote* was established anywhere**. The front-loading is inferred from the exit terms [R1] [R2] [REG-R45]; the ×2.5 tax step lives in `Projection`, not here, depending on age as well as duration |
| `charge_table.csv` | Four tariffs: `std_gross`, `std_netto`, `std_high`, `std_low` | **[std]** but for `alpha_rate` on `std_gross`, the 25 ‰ cap [R12] [R13] [REG-R16], and the 60-month spread [R1] [REG-R28]. **One carrier's levels are now known** — 2,50 % acquisition, 6,90 % of premium, 0,42 % p.a. of fund, 18 €/yr [S15] — and `std_gross` is lighter than that on every line but the policy fee; nine other named carriers still supply none. The `std_gross`-to-`std_netto` gap is the acquisition load [S18] |
| `fund_scenario_table.csv` | Gross return and TER by `(scenario_id, policy_year)`: `base`, `etf`, `zero`, `stress` | **[std]** deterministic paths. Not forecasts and **not PRIIPs scenarios** [R8] [R9] [REG-R32] — and note that on the profession's own standard a German Schicht-3 unit-linked annuity is a **PRIIP Kategorie 4** product whose scenarios come from a stochastic capital-market model, not from an underlying's own return history [R18] |
| `rentenfaktor_table.csv` | Guaranteed and current factors by `(factor_id, annuity_age)`, ages 60–75 | **[std] and derived, not observed**: `10 000 / (12 · T_eff(x))` with `T_eff(x) = 100/3 − 0.75 (x − 67)` at a 0 % *Rechnungszins* — confirmed for a fondsgebundene tariff on DAV 2004 R [S2] [S10] [R16] [R22] [REG-R49] — giving exactly **25,00 at 67**. **Observed guaranteed factors at *Rentenbeginn* 67 are 25,22 / 24,12 / 22,91 / 21,83 € at deferments of 12 / 20 / 30 / 40 years** [S15], so the shipped table is about 9 % generous at the anchor cell and, being flat in the deferment, cannot reproduce the generational gradient. `std_2026` sets the current factor equal to the guaranteed one; `rich_current` 12 % higher |

## Modules that are off in the base run

| Module | Switch | Off value | What it does |
|---|---|---|---|
| Dynamic lapse | `lapse_dyn_beta` | `0.0` | `lapse_dyn_add(t) = β · max(0, 1 − av_pp(t)/cum_prem_pp(t))` raises the lapse rate while the contract is under water against the premiums paid — unit-linked lapse is market-sensitive precisely because the exit is at fund value on short notice [R1] [R2]. 0.15 is the reference value; **no German calibration for a coefficient of any size exists in this corpus.** Switched on it bites hardest on model point 12, whose stress path leaves the fund far below premiums paid for years |
| *Ablaufmanagement* | `ablauf_flag` (model point) | `False` on twelve of thirteen | A linear ramp of the **gross** return from the scenario's rate to `mmkt_return_ann = 1.50 %` over the last `glide_months = 60` months. With one fund and a deterministic return a reallocation and a change of assumed return are the same thing, so this is the honest representation of what is known — and **nothing about a real *Ablaufmanagement* was established**: not whether it is opt-in, not the ramp length, not the destination. Model point 8 switches it on |
| *Überschussbeteiligung* | — | not implemented | A unit-linked contract's surplus arises from the risk and cost results only [R5] [R14] [REG-R9] [REG-R18]; the model computes the risk result and credits none of it back. The omission biases the projected *Fondsguthaben* **downward**, the honest direction for a charge demonstration |

Hybrid and guarantee designs — *statisches* and *dynamisches Hybrid*, *Zwei-* and
*Drei-Topf-Hybride*, i-CPPI, *Wertsicherungsfonds* — are described in the product
specification and **deliberately not implemented**: each is a rule for reallocating between a
guaranteed pot and a risky pot along a path, and a deterministic projection has one smooth
path, so the rule either never triggers or triggers on a hand-chosen shock. What would have to
be added is named instead — a multi-scenario asset model, a monthly reallocation rule, a
guaranteed pot accreting at a *Rechnungszins*, a *Wertsicherungsfonds* return model — and that
is a different model. `kapitalwahl` is a fourth switch and changes no cash flow by design:
both routes release the same *Fondsguthaben*, the annuity being published rather than
projected. It is carried because the two tax regimes genuinely differ [R19] [R20] [REG-R41]
[REG-R45] and because take-up is the largest behavioural unknown here; **no take-up rate was
established**, so the base run annuitises.

## Sign convention

`net_cf` is **income positive** — charges in, expenses, commission and the death strain
out — the notes' own orientation and the library-wide sign. `liability_cf` publishes the
same stream outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are
`result_cf()` columns so the identity is verifiable in the frame rather than only in prose.
A Solvency II best estimate of the non-unit liability is `Σ v(t) × liability_cf(t)` over the
relevant risk-free term structure, with the unit liability — the *Fondsguthaben* itself,
backed one-for-one by the *Anlagestock* — added at market value [R15] [REG-R6] [REG-R7].
Nothing here discounts.

`expenses` **excludes commission**: it is the issue expense at `t = 0`, the inflating monthly
maintenance expense, and the per-event expenses of a death, a surrender and an annuitisation.
The *Abschluss-* and *Bestandsprovision* are `commissions`, their own column, and `net_cf`
subtracts each once — the delib convention, and the opposite of the frlib chassis, where
commission sits inside the expense total; taking both at once charges the commission twice.
The worked example fixes the reading:
`expenses(0) = 200,00 + 4,00 + 0,0075 + 0,2571 = 204,26 €` and
`commissions(0) = 1 800,00 + 3,00 = 1 803,00 €`, together the 2 007,26 € of acquisition and
first-month cash. Expect on a new-business cell a large negative `net_cf` in the inception
month `t = 0` — −1 966,22 € on the anchor, commission and issue expense falling there while
the charge that funds them arrives over sixty months —
then a thin positive margin growing with the fund. On the *Einmalbeitrag* cell the sign
reverses: `t = 0` is **+1 060,45 €**, the 3 250,00 € withheld at inception more than covering
the acquisition cost with no recovery to wait for.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` where it has an analogue and
`savings/CashValue_SE` for the account-value vocabulary: `pols_*` for policy counts, `av_*` for
the account value, `*_pp` for per-policy amounts, `*_rate` for rates, `claims(t, kind)` with an
uppercase `kind` string, and `av_pp_at(t, timing)` / `pols_if_at(t, timing)` for the
within-month reads. The technical notes use compact actuarial symbols; the full mapping is in
the `Projection` Space docstring. The chassis is shared with
`frlib/products/assurance_vie_uc/UC_FR_S`, the French *unités de compte* contract, and the
*On `UC_FR_S`* column says where a shared name means the same thing there and where it does
not:

| Notes | Cells | On `UC_FR_S` | Why |
|---|---|---|---|
| `F(t)`, `F_τ(t)` | `av_pp` / `av_pp_at` / `av_at` | names shared, readings differ: there `av_pp(t)` is the **end**-of-month fund (`av_pp_at(t, "BEF_DECR")`), `av_pp_at` names **five** timings, and `av_at` weights by the after-decrement count | The fund at the **start** of the month, at four named points inside it, and weighted by `pols_if`. The timings are the processing order made addressable |
| `u(t)`, `Δu(t)` | `units_pp` / `units_bought_pp` / `units_cancelled_pp` | `units` / `fee_units` / `wd_units` | The state variable and its two movements; delib puts every cancellation in one cells because the identity checking them has no price term |
| `K(t)`, — | `nar_pp` / `death_strain` | `nar` / `plancher_strain` | The *riskiertes Kapital* / the French *garantie plancher* amount at risk, floored at zero in both, and the only part of a death benefit the insurer funds |
| `W(t)`, `A(t)` | `av_releases` / `withdrawals` / `prem_to_av_pp` | same | The unit-side total the benefit-funding identity reconciles against; an owner election, never `claims_wd`, a *Teilentnahme* being no claim; and the *Anlagebeitrag* that buys units |

Three German terms of art keep their German form in the cells names, each naming a quantity
with a statutory definition and no English equivalent that would not mislead:
`beitragssumme()`, the base of the *Höchstzillmersatz* and not "total premiums";
`stornoabzug(t)`, a deduction whose validity conditions are statutory and not a "surrender
charge" — the euro amount retained, with the fraction it is struck at as `stornoabzug_rate()`,
which is the spelling `RV_DE_S` and `Riester_DE_S` use for that rate too; and the three
`rentenfaktor_*()`, euro per 10 000 € and not an annuity factor. Five further cases needed
care:

| Notes | Cells | Why |
|---|---|---|
| `qᴵ(t)`, `q(t)` | `mort_rate_tariff` / `mort_rate`, and their `_mth` forms | Two rates: the first-order table prices the *Risikobeitrag*, the second-order one produces the claims, and their difference is the *Risikoergebnis*. `mort_rate` is the projection's own decrement, per the library's shared vocabulary |
| `w(t)` | `lapse_rate_base` / `lapse_tax_step` / `lapse_dyn_add` / `lapse_rate` / `lapse_rate_mth` | The library requires an annual `lapse_rate` beside the monthly one; the table rate, the tax multiplier and the dynamic addition are separate cells so each is testable alone |
| `α(t)` | `charge_acq_pp` / `cum_charge_acq_pp` / `charge_acq_total` | The instalment, the ledger and the total the ledger must reach — `check_acq_charge` needs all three |
| `D(t)` | `db_floor_pp` / `db_pp` | The guaranteed floor and what a death actually pays; keeping them apart makes `death_strain` exactly the net amount at risk |
| (expense / commission) | `expense_acq_pp` / `comm_acq_pp`, `expenses` / `commissions` | Two lines, not one. `expenses` is the insurer's own outgo **excluding** commission and `commissions` is the *Abschluss-* and *Bestandsprovision*, which is what those two names mean on every delib model that has a commission to publish |

`sex` and `kapitalwahl` drive no formula — the tariff is unisex from 21 December 2012
[REG-R34] and the capital option is a reporting split — but both are exposed as documented
cells rather than dropped, because the notes' model point attribute table lists them.

## Standardizations used

Every entry is **[std]**, and the rationale is what makes it honest.

| Standardization | Value | Rationale |
|---|---|---|
| Acquisition rate, composite, and the *Zuzahlungskosten* | 2.50 % of the *Beitragssumme*; 2.50 % of a *Zuzahlung* | The rate is the *Höchstzillmersatz* — *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"*, § 4 Abs. 1 Satz 2 DeckRV [R12] [REG-R16] — and taking **the cap** demonstrates the binding constraint instead of inventing a level. It turns out to be the level one real tariff charges: **2,50 % der kumulierten Anlage** [S15]. The *Zuzahlungskosten* is set equal to it, and on a single premium it is the whole acquisition charge, which is what a real wording does — *"Bei Verträgen gegen Einmalbeitrag und bei Zuzahlungen entnehmen wir alle Abschluss- und Vertriebskosten sofort"* [S2] |
| Premium-based admin `beta_rate` | 4.00 % | Middle of an argued 2 %–10 % range. **6,90 % of each premium observed at one carrier** [S15]; no other carrier level was established |
| Fund-based admin `gamma_rate_ann` | 0.30 % p.a., taken as `/12` | Middle of an argued 0.10 %–1.20 % range. **0,42 % p.a. of the fund observed at one carrier** [S15]. Divided, not compounded, because a German tariff quotes a nominal monthly charge |
| *Stückkosten* `policy_fee_mth` | 3.00 € per month | Middle of an argued 0–5 € range; **18 € per year — 1,50 €/month — observed at one carrier** [S15], so the composite is the dearer of the two. A euro amount, which is why it consumes a small paid-up fund — and why BaFin warns that a large absolute *Stückkosten* charge makes the *Effektivkosten* vary sharply with premium size [R10] |
| *Stornoabzug*, composite | 0.00 % | § 169 Abs. 5 VVG permits one only where it is *vereinbart*, *beziffert* and *angemessen* and voids any deduction for unamortised acquisition cost [R1] [REG-R36]; zero avoids an unsourced number on a contested clause. **A real one exists and is a flat 150 €, not a percentage** [S2], so both the level and the shape are standardizations. 2.00 % on `std_high` exercises the machinery |
| The three charge variants | `std_netto`, `std_high`, `std_low` | The ends of the argued range plus the commission-free tariff [S18]; the gap to `std_gross` **is** the acquisition load |
| Mortality proxy | `0.00080 × 1.10^(x − 37)`, ages 18–100 | DAV tables are not redistributed [R17] [REG-R48]. Anchored at `q(37) = 0.00080` so the worked example reproduces; the 10 % gradient is insured-lives. It stands for **whichever first-order death table the tariff uses** — DAV 2008 T is the modern one, and the one fondsgebundene tariff whose bases could be read prices its *Risikobeiträge* on a unisex order at **65 % of DAV 1994 T** instead [S2] |
| `mort_be_factor` | 0.75, flat | Crude, and said to be. It buys a *Risikoergebnis* that is exactly 25 % of the *Risikobeitrag* [REG-R47] |
| Monthly conversions | mortality `/12`; lapse and return geometric | Charge and decrement must share a split; the lapse and return annual rates are the observables to reproduce |
| Lapse table, the 40 % cap and the zero final month | 6 / 3 / 2 / 3 % by duration band; `lapse_cap = 40 %`; `lapse_rate_mth(n − 1) = 0` | **No German unit-linked *Stornoquote* exists in this corpus**; the front-loading is inferred from the exit terms [R1] [R2]. The cap stops a dynamic module producing an absurd rate; the zero final month is because a surrender and an annuitisation are then one event |
| Tax-threshold lapse step | ×2.5 for twelve months from `max(13, 62 − entry_age + 1)` | The 12/62 rule is statutory — EStG § 20 Abs. 1 Nr. 6 Satz 2, which names the 60th year of life, raised to the **62nd** by § 52 Abs. 28 *"für Vertragsabschlüsse nach dem 31. Dezember 2011"*, and applying on surrender as well as at maturity [R20] [REG-R45]. It is the strongest single driver of German surrender behaviour; keying it on duration alone fires fourteen years early on the anchor. The ×2.5 magnitude is **[std]** |
| Fund paths and TER | 5.00 % gross, 0.45 % TER on `base`; `etf`, `zero`, `stress` | Round, clearly-labelled assumptions. **Not forecasts, not PRIIPs scenarios** [R8] [R9] [REG-R32] |
| *Kickback* credited back, and the *Ausgabeaufschlag* | 0.00 % p.a.; fully waived | A passive fund pays no trail. **The two questions this once sidestepped are answered**: insurers do receive rebates out of the fund's *Verwaltungsvergütung* and must test them for *Fehlanreize* and consider passing them back [R10] [R15], and the market pays a weighted mean just over **0,30 % p.a. of the fund**, up to over **1,20 %**, on about a third of new business [R11] — so 0 % models the cheap end of a real flow. Only the PRIIPs treatment of a credited rebate is still open [R7] [R8]. **The *Ausgabeaufschlag* waiver is confirmed**: *"Ausgabeaufschläge und Depotkosten fallen nicht an"*, and units are bought at the *Rücknahmepreis* [S2] |
| Guaranteed *Rentenfaktor* | 25,00 € per 10 000 € at 67, from `10 000/(12 T_eff)` | **Derived arithmetic, not a market observation** — and now measurable against one. The 0 % *Rechnungszins* on DAV 2004 R is confirmed for a fondsgebundene tariff [S2] [S10] [R16]. **The level is not**: at this model's own anchor cell the observed guaranteed factor is **22,91 €** against the shipped 25,00 €, and the observed factor *falls with the deferment* — 25,22 / 24,12 / 22,91 / 21,83 € at 12 / 20 / 30 / 40 years to age 67 — where the shipped table is flat in it [S15]. **Not changed in this pass**: the table, the worked example and the golden tests move together |
| Current *Rentenfaktor* | equal to guaranteed (`std_2026`); +12 % (`rich_current`) | Exercises the `max()` without an unsourced uplift, and makes it visibly bite on one cell. Consumer sources describe real guaranteed factors at 50–70 % of the current one `[unverified]` [R22], so both settings are conservative |
| Expenses and commission (`expenses` excludes commission; `commissions` is its own column) | acquisition commission 2.50 % of `S` + 200,00 € issue; 4,00 €/month at 2 % inflation; renewal 1.5 %; 150 / 50 / 100 € per event | **No German commission scale was established.** The acquisition commission equals the acquisition charge, so the model shows the financing problem the *Höchstzillmersatz* and the five-year spread exist to regulate. `comm_acq_rate` is a flat scalar, so on `std_netto` and `std_low` the assumed commission exceeds the tariff's own charge and those cells carry a projected loss — the flat assumption showing, not a product fact |
| Timing, processing order and the negative-fund safeguards | premium in advance, return, fund charges, *Teilentnahme*, *Risikobeitrag*, deaths before lapses; `min(.., remaining)` on the *Stückkosten* and the *Risikobeitrag* | The *Bewertungsstichtag* lag disappears on a monthly grid; observing the amount at risk before the charge that prices it makes `death_strain` exactly the *riskiertes Kapital*. The floors are safeguards, not tariff terms, and **no shipped model point triggers one** |
| *Beitragsfreistellung* as an election | `pup_month`, no cohort paid-up rate | A cohort rate needs one sub-cohort per paid-up month for a second-order effect; the **[std]** 1 % p.a. is recorded, not implemented, and the omission biases charge income upward |
| Modules off in the base run | `lapse_dyn_beta = 0`, `ablauf_flag = False`, no *Überschuss* credit | Base-run values, so the worked example reproduces with the machinery still there |
| The thirteen model points | see the input table above | Configurations, not assumptions — which is why they are the one provenance-exempt file |

The quantities that are **not** standardizations are the acquisition-charge cap, § 4 Abs. 1
Satz 2 DeckRV [R12] [REG-R16], and the five-year spreading, § 169 Abs. 3 VVG — which reaches this
contract through Abs. 4's *"im Übrigen gilt Absatz 3"* and through tariff practice rather than
directly [R1] [R13] [REG-R28]; the *Beitragsverrechnung* order, read verbatim at [S2] § 14
Abs. 1 as well as [S1]; the *Beitragsrückgewähr* shape [S2] § 2 Abs. 7; the
`max(guaranteed, current)` factor rule [S2] § 2 Abs. 2, [S4] [R22]; the *Zeitwert*
*Rückkaufswert*, § 169 Abs. 4, and the conditions on a *Stornoabzug*, Abs. 5 [R1] [REG-R36]; the
survival of the fund-based charges into a *beitragsfrei* contract [R3] [S2] § 14 Abs. 2; the
unisex tariff [REG-R34], now visible in a real *Rechnungsgrundlage* [S2]; and the rule that the
insurer guarantees units and not their value, which VAG § 124 Abs. 2 Satz 2 Nr. 1 and § 125
Abs. 5 make structural [S1] [R15] [REG-R7].

**Three shapes this model implements differently from the one tariff that could be read**, none
of them changed in this pass and all of them recorded so a calibration pass knows where to look:
the acquisition charge falls to zero at `t = 60`, where a real tariff continues a slice of it for
the whole premium term as a percentage [S2] § 18 Abs. 2; the *Stornoabzug* is a percentage of the
fund, where a real one is a flat euro amount [S2] § 17 Abs. 4; and a *Teilentnahme* reduces the
fund but not the *Beitragsrückgewähr* floor, where a real clause reduces both [S2] § 2 Abs. 7.

## Tests

`tests/test_fondsgebundene_rentenversicherung_de.py` asserts the notes' worked example — all
seventeen printed rows of Panel A to the cent and `pols_if` to six decimals, its
`expenses` and `commissions` columns among them, Panel B's benefit
columns, Panel C's per-policy unit side, and every column total at full precision — the notes'
three independent rebuilds (`t = 0` from the tariff alone, `t = 60` at the cliff, the
reduction in yield as a savings account), the four closure identities, the *Einmalbeitrag*
variant's printed table, the four-tariff reduction-in-yield comparison, the seven `check_*()`
identities with their residuals, and **one test per listed modeling pitfall** — eighteen of
them, named for the pitfall they guard. The library-wide house style — layout, docstrings,
naming, the retired-name register, the `check_net_cf` ruling, the `provenance` ruling, the
model point sweep and the round trip — is asserted separately, once, in
`tests/test_model_conventions_de.py`, which owns the only whole-table sweep in the library.

```bash
python -m pytest lifelib/libraries/delib/tests -q
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-fondsgebundene_rentenversicherung-r1
[R10]: #delib-fondsgebundene_rentenversicherung-r10
[R11]: #delib-fondsgebundene_rentenversicherung-r11
[R12]: #delib-fondsgebundene_rentenversicherung-r12
[R13]: #delib-fondsgebundene_rentenversicherung-r13
[R14]: #delib-fondsgebundene_rentenversicherung-r14
[R15]: #delib-fondsgebundene_rentenversicherung-r15
[R16]: #delib-fondsgebundene_rentenversicherung-r16
[R17]: #delib-fondsgebundene_rentenversicherung-r17
[R18]: #delib-fondsgebundene_rentenversicherung-r18
[R19]: #delib-fondsgebundene_rentenversicherung-r19
[R2]: #delib-fondsgebundene_rentenversicherung-r2
[R20]: #delib-fondsgebundene_rentenversicherung-r20
[R22]: #delib-fondsgebundene_rentenversicherung-r22
[R3]: #delib-fondsgebundene_rentenversicherung-r3
[R5]: #delib-fondsgebundene_rentenversicherung-r5
[R7]: #delib-fondsgebundene_rentenversicherung-r7
[R8]: #delib-fondsgebundene_rentenversicherung-r8
[R9]: #delib-fondsgebundene_rentenversicherung-r9
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R28]: #delib-reg-r28
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R34]: #delib-reg-r34
[REG-R36]: #delib-reg-r36
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R6]: #delib-reg-r6
[REG-R7]: #delib-reg-r7
[REG-R9]: #delib-reg-r9
[std]: #delib-std
<!-- END generated citation links -->
