# Implementation Notes

**Status:** Draft, 2026-08-29. Built from
[`technical-notes.md`](technical-notes.md); the product it implements is specified in
[`product-spec.md`](product-spec.md).

> **This is a mechanics demonstration, not a pricing or reserving result.** The *mechanics*
> are the established German ones and each carries the instrument it must be checked
> against — the *Berufsunfähigkeit* definition, its 50 % degree and its *Sechs-Monats-Fiktion*
> [S1] [S12] [R1], the *Anerkenntnis* and *Nachprüfung* frame with its three-month run-off
> [R2] [R3], the *Beitragsbefreiung* as core cover rather than an option [S1] [S2], the
> *Brutto* / *Zahlbeitrag* pair and the *Beitragsverrechnung* behind it [R10] [R14] [S6] [S12],
> the unisex rule [REG-R34], and the absence of any death, maturity or surrender cash flow
> [S1] [R8] [R9]. The six months is the *Fiktion*'s period, not the *Prognosezeitraum*'s: the
> latter is set by each carrier and the GDV model conditions leave it blank. **Every level is a standardization.** The DAV 1997 family and DAV 2008 T
> are the property of the Deutsche Aktuarvereinigung, are not public and are **not
> redistributed here** [R16] [R17] [REG-R50] [REG-R48]; no *Produktinformationsblatt* was
> obtained, so no carrier's BU charge structure is on the record here — the disclosure
> itself exists, VVG-InfoV § 2 requiring it in euro, and it is only the *Effektivkosten*
> figure that a pure risk contract does not carry [R12] [S14]; and **no German BU rate card
> of any kind was obtained**, so the *Bruttobeitrag* is an output of a stated first-order
> basis rather than a table lookup. Replace the decrement, charge and premium bases with
> company data before drawing any conclusion from the numbers. **On provenance:** delib was
> drafted under a policy that blocked all egress, on the authoring model's own knowledge
> disciplined by **[std]** and `[unverified]` tags, and its citations have **since been
> re-verified against the primary documents**; `sources.md` records per entry what was
> opened and what was not, 26 of this product's 43 entries carrying `Retrieved: yes` and 17
> still `Retrieved: no`.

## Run it

```bash
python products/berufsunfaehigkeit/run.py
python products/berufsunfaehigkeit/run.py 4      # the Beitragsdynamik variant
python products/berufsunfaehigkeit/run.py 7      # an in-force policy already in claim
```

```python
import modelx as mx
model = mx.read_model("products/berufsunfaehigkeit/BU_DE_S")
model.Projection[1].result_cf()
```

`Projection` takes a `point_id`; `Projection[1]` is the worked-example anchor cell.
`result_cf()` returns a tidy `DataFrame` indexed by **policy month** `t` carrying the three
state ledgers, the premium-paying count and one column per cash flow line, and
`result_states()` publishes the transitions, rates and per-policy amounts beside it.
`model.Projection.doc` holds the full mapping from the notes' symbols to the cells names, and
`model.Data.doc` says what a replacement for each biometric table must preserve.

The grid is **monthly** and `t` is **0-based**: `t = 0` is the first projected month — the
month of inception for a new-business point, the valuation month for an in-force one — and
`proj_len()` is the **number** of projected months, the **exclusive end** of the frame, so
the frame is `range(proj_len())`: `t = 0 … proj_len() − 1`, and `result_cf().index[-1] ==
proj_len() − 1`. On the anchor cell `proj_len() = 12 × (67 − 30) = 444`, i.e. 444 rows
(`t = 0 … 443`) in about a second. The contractual, 1-based *policy year* is derived, not
indexed by: `policy_year(t) = duration_mth(t) // 12 + 1`.

**Time-like CSV columns.** No input file is keyed by the projection month `t`, so no CSV
value moved with this frame change. `lapse_table.csv` is keyed by `policy_year` 1–5 with row
6 the ultimate — a contractual 1-based label read through `policy_year(t)`, so the file is
left alone. `claim_duration_table.csv` is keyed by `dur_year` 1–10 with row 11 the ultimate,
the **claim** year since onset, on the 1-based claim-duration clock `z` and independent of
`t`; unchanged. `inception_table.csv` and `mortality_table.csv` are keyed by attained `age`,
reached through `age(t)`; unchanged. In `model_point_table.csv`, `duration_init_months` and
`claim_duration_init` are **elapsed counts**, already 0-based by nature, and neither is a
point on the frame's axis — the frame always opens at `t = 0` and carries the elapsed
duration as an offset inside `duration_mth(t)` — so both are unchanged.

## Four ledgers, one return arc, and § 174 in arithmetic

This is what a reader arriving from `RLV_DE_S` or `BasicTerm_S` will get wrong, and it is why
the product is worth modelling. A BU contract is a **multi-state model with a return arc**,
not a decrement model:

```
aktiv  --inception-->  leistungspflichtig  --Nachprüfung-->  run-off (3 months)  --> aktiv
  |                          |                                    |
 death, lapse              death                                death
```

`pols_actv`, `pols_dis` and `pols_runoff` are the three ledgers and `pols_if` is their total.
**Death and lapse are the only exits**, so `pols_if(t+1) = pols_if(t) − pols_death(t) −
pols_lapse(t)`, and inception, recovery and reactivation are **internal transfers** that must
not appear in that identity — putting them there is how a multi-state model silently loses
mass, invisibly in the cash flows.

The run-off ledger is § 174 VVG in arithmetic [R3] [REG-R29]: where the insurer establishes that
its liability has ceased it remains obliged to pay **to the end of the third month after the
notice reaches the policyholder**, so a recovery does not stop the annuity in the month it
happens. `pols_recovery(t)` feeds run-off slot 1, the slots roll at **active-lives** mortality —
these lives have recovered and are no longer impaired — and only the slot-3 survivors rejoin
`pols_actv` as `pols_reactivation(t)`. On the anchor cell the tail is 206,41 € of the 13 151,35 €
of *BU-Rente*, **1,6 % of all benefit**: small in aggregate, structural in kind. A model
returning a recovery straight to the active ledger loses three monthly *Renten* per recovery and
fails `check_runoff_roll_fwd()` immediately.

The run-off carries **amounts as well as counts**: `runoff_val(t, k)` is the slot population
times the *BU-Rente* it is still being paid, because the cohorts terminating in one month came
in on different *Renten* and have crossed different numbers of onset anniversaries. A cohort
keeps the *BU-Rente* it was on at the *Nachprüfung* date and receives no further
*Leistungsdynamik* **[std]** — three months is inside one onset anniversary in every realistic
case — which removes a second duration dimension at no measurable cost. The disabled ledger
carries a value vector for the same reason: the month's benefit is one sum over a slice.

`dis_cohorts(t)` and `runoff_cohorts(t)` are **list-valued cells**, a cost decision: a
two-argument recursion over `(t, z)` would be nearly two hundred thousand separate cells on the
anchor cell where this is one per month with a loop inside, and the notes' two-dimensional
objects stay addressable as `pols_dis_dur(t, z)`, `pols_runoff_slot(t, k)` and `runoff_val(t, k)`.

Two things this deliberately does **not** do. It does not separate recovery from *konkrete
Verweisung* — both end the benefit through the same *Nachprüfung* with the same run-off and no
public data separates them [R3] [R29], so `recov_rate(z)` is exactly one
claim-termination-other-than-death rate — and it carries **no age-at-disablement dimension** on
reactivation, which DAV 1997 RI does [R16].

## The premium is two numbers, and both are published

A German BU tariff is quoted as a pair, and no other product in this repository is [R10] [S13]
[S16]. The ***Bruttobeitrag*** is the contractually guaranteed **maximum**; the ***Zahlbeitrag***
actually billed is `beitragsverrechnung` times it — the anticipated *Überschuss* credited in
advance under § 153 VVG through § 176, with the MindZV risk-result minimum behind it [R14]
[REG-R18] [REG-R24].

`result_cf()` publishes **both**: `premiums(t)` is the gross stream and `surplus_credit(t)` the
credit returned out of it, so the cash collected is the difference and the
*Überschussbeteiligung* is a visible line rather than a netting hidden inside the premium. A
model carrying only the *Zahlbeitrag* silently assumes the credit is permanent; one carrying only
the *Bruttobeitrag* overstates collected premium by `1/0,70 − 1 = 42,86 %`. Over the anchor
cell's 444 months `Σ premiums / Σ (premiums − surplus_credit) = 24,771.0596 / 17,339.7417 =
1.428571428571429`, which is `1 / 0.70` to fifteen figures — necessarily so, because `freq_load`
scales *Bruttobeitrag* and *Beitragsverrechnung* **together** and cancels out of the ratio.

There is **no surplus account, no RfB and no declaration mechanic**, which is correct for BU
rather than a simplification: *Beitragsverrechnung* applies the surplus immediately instead of
accumulating it. Holding the ratio constant is the model's largest discretionary assumption and
the one the product's own consumer literature warns about [S13] [S16].

## The *Bruttobeitrag* is derived, not read

The `*_first` cells are a **second projection**, not a variant of the first: the same
four-ledger chain on *Rechnungsgrundlagen erster Ordnung* — inception × 1,30, reactivation
× 0,70, disabled-lives mortality × 0,80, active-lives mortality × 0,80, **no lapse** — run
over the contract's **original** term from `entry_age` and indexed by `s` rather than `t`.
Prudence for a disability product means a claim that starts more often, ends less often and
lasts longer; it also means fewer premium-paying lives lost, because here an active death and
a lapse both *release* a liability and a prudent basis does not anticipate a favourable event.

The equivalence is linear in `P`, because both the acquisition and the proportional
administration loadings are proportional to it:

```
P = (PV_rente + PV_wgh + PV_cost + PV_admin)
    / ( PV_prem x (1 - admin_prem_rate) - acq_rate x BS_unit )

  = (24,452.4895291302 + 531.1897520089 + 335.6805156244 + 544.5174674852)
    / (29.0716529817 x 0.91 - 0.025 x 37)
  = 25,863.8772130176 / 25.5302042134  =  1,013.0697368527 EUR p.a.
```

so the monthly instalment is `P × 1,05 / 12 = 88,6436` € and the *Zahlbeitrag* `0,70 ×` that
`= 62,0505` €. **The recursion is acyclic**: no decrement depends on the premium, so nothing
in the `pv_*` cells depends on `P`. The equivalence is struck **before** the *Risikozuschlag*
and **without lapse**, deliberately on both counts, and `PV_prem` is struck on `P / 12` in
every month — so `freq_load` is a genuine loading on the tariff premium rather than a
re-expression of it. Running the shadow from inception rather than from the valuation date is
what gives an in-force point the premium its contract was struck at: **model point 6 is model
point 1 fifteen years on, and the two price identically at 1 013,0697 € p.a.** Model point 13
supplies `gross_prem_ann = 2 400,00 €` instead, so the override branch ships too.

## The *Beitragsbefreiung* is the absence of a premium, not a benefit

While the *BU-Rente* is in payment the premium is waived — core cover in every German BU
contract [S1] [S2] — and in a multi-state model that is not a cash flow at all but the
*absence* of one. It falls out only if the premium is weighted by the right count:

```
pols_prem(t) = pols_actv(t) + Σ_{z ≤ karenz_months} pols_dis_dur(t, z)
premiums(t)  = prem_gross_pp(t) x pols_prem(t)
```

Weighting by `pols_if(t)` instead charges premium to lives in claim and silently deletes the
waiver. It is the classic German BU implementation error, it leaves every total looking
plausible, and it is why `check_net_cf()` rebuilds the premium leg from
`prem_zahl_pp(t) × pols_prem(t)` rather than from `premiums(t) − surplus_credit(t)`.

A life inside the *Karenzzeit* is *berufsunfähig*, is **not** yet paid, and **still pays
premium** **[std]** — the waiver runs with the benefit. On the anchor `karenz_months = 0`, so
`pols_prem(t) == pols_actv(t)` everywhere; on model point 5 (`K = 6`) they differ at 323 of 324
months. The *Karenzzeit* is **not** the *Prognosezeitraum* and **not** the *Sechs-Monats-Fiktion*;
both of those are part of the *definition* of BU, and the *Karenzzeit* defers the pension alone —
"Die Karenzzeit gilt nur für die Rente" [S4]. With `K = 0` the first *BU-Rente* falls in the month
**after** an onset — `claims(1, "BU_RENTE") = 0,11 €`.

## Two escalations, two clocks

| | escalates | steps on | cells |
|---|---|---|---|
| *Beitragsdynamik* `g_B` | the **insured** *BU-Rente* **and** the annual *Bruttobeitrag*, before any claim | the **policy** anniversary | `dyn_factor(t)` → `bu_rente_pp(t)`, `prem_gross_ann_pp(t)` |
| *Leistungsdynamik* `g_L` | the *BU-Rente* **in payment** | the anniversary of the **onset** | `leistungsdyn_factor(z)` → `rente_pay_pp(t, z)` |

`rente_pay_pp(t, z) = bu_rente_pp(t − z) × (1 + g_L)^((z − 1) // 12)`: the insured amount at
the moment of onset, which for a cohort at duration `z` in month `t` is month `t − z`,
escalated on each anniversary of that onset. Cohorts `z = 1 … 12` are paid what they came in
on and `z = 13` opens the first escalated year. Escalating the amount in payment on the
**policy** anniversary is the wrong clock and is a numbered pitfall.

The `dynamik` form is model point 4, and it carries a departure from market practice recorded
rather than corrected: German insurers price each increment at the attained age reached, so a
given increase buys **less** than proportional cover. This model escalates premium and insured
*BU-Rente* by the same `g_B` and prices the whole stream by **one** equivalence at inception —
internally consistent, acyclic, and understating what the market would charge.

## Two rating multipliers, and only one of them touches a claim

- **`occ_factor`** (κ) loads the **inception rate**: `inc_rate(t) = inc_rate_base(t) ×
  occ_factor() × accept_factor × au_uplift()`, and those are the **only three** multipliers on
  it. So it moves every claim and every decrement and reaches the premium only through the
  equivalence. Model point 3 is the anchor at BG4: `inc_rate` scales by exactly 3,00 while
  the premium scales by **2,932141**, slightly *below* it, because the flat administration
  and assessment charges do not scale with the risk.
- **`risk_factor`** (ρ) loads the ***Bruttobeitrag* alone**. Model point 11 carries 1,50: its
  premium and surplus credit scale by exactly 1,50 while every decrement, claim and claim
  expense is bit-for-bit what it would be at 1,00. A *Risikozuschlag* prices an individually
  assessed impairment the base table does not carry and this model does not carry either, so
  a loaded contract is projected **above** its own modelled cost. The direction is stated,
  not corrected.

`accept_factor = 0,80` is the *Anerkennungsquote* and multiplies the **inception rate**, not
the benefit: a declined claim generates no annuity at all rather than a smaller one. The
shipped table is **gross of declinature**, so a user substituting one already net of it must
set the factor to 1,00 or the effect is counted twice [REG-R53].

`sex` is a model-point attribute for reporting only and **must not price**: sex-differentiated
premiums and benefits have been unlawful in Germany for contracts written from 21 December 2012
[R15] [REG-R34]. Model points 1 and 2 differ in `sex` alone, and their frames are identical.

## The *Leistungsendalter* stops the benefit and holds the mass

`cover_end_age` and `benefit_end_age` are separate contractual terms, not synonyms. Model point 9
carries cover to 67 and benefit to 63: from attained age 63 the *BU-Rente* and the
claim-maintenance cost are exactly zero while the premium runs on for four more years, collecting
a further 2 244,03 €.

What is easy to get wrong is the population. **The mass is held, not deleted**: the ledgers
keep rolling past `benefit_end_age`, so `check_states()` and `check_pols_roll_fwd()` still close
across the boundary and `pols_if(t)` is continuous through it, where deleting the disabled
cohorts breaks both identities at once. Those lives do **not** resume paying premium **[std]** —
they are still *berufsunfähig*, and the *Beitragsbefreiung* is read as keyed to the **state**
rather than to the payment. The alternative reading is defensible and is named.

## Four absences are product facts

- **No death benefit.** An SBU pays nothing on death, before or during a claim [S1], so
  `pols_death(t)` is a decrement and never a cash flow, and there is no `claims_death` column.
- **No maturity benefit.** Survival to the *Endalter* pays nothing; a claim still in payment at
  the horizon simply stops. That is true of the GDV model conditions and of the modelled product;
  it is **not** universal — one retrieved carrier's AVB grants a surplus-financed *Schlusszahlung*
  at expiry where no BU arose [S12]. That is a surplus application, not a guarantee, and this model
  carries no surplus account to fund one.
- **No cash value.** § 169 VVG through § 176 gives this contract a *Rückkaufswert* — the AVB pay it
  "entsprechend § 169 des Versicherungsvertragsgesetzes (VVG)" [S1] — and § 165 a *beitragsfreie
  BU-Rente* [R8] [R9] [R5] [REG-R28]; both are the release of a reserve this model deliberately does
  not compute, and both are **small**, the conditions themselves warning that the premium parts
  available to build it are "sehr gering" against premiums paid [S6]. `claims(t, "LAPSE")` therefore exists, returns zero
  at every `t` and is published as a zero column; there is no `av_pp_at`, no surrender cells and
  no paid-up state. The zero states the scope; a missing column would hide it.
- **No acknowledged state.** § 173's once-only *befristetes Anerkenntnis* would justify one
  [R2], but this model pays from **onset** and does not model the *Leistungsprüfung* delay, so
  acknowledgement is a timing event with no cash-flow consequence — right in amount, early.

## Inputs are external files

The seven input CSVs live **in this directory**, beside `run.py`, and `BU_DE_S/` holds nothing
but formulas — `__init__.py`, `_system.json`, `Data/__init__.py` and `Projection/__init__.py`, no
`_data/`, no IOSpec, no embedded values. This follows lifelib's `annuallife/TradLife_A`, which
keeps its inputs beside the model; it is the opposite of `basiclife/BasicTerm_S`, which stores
its inputs inside the model.

### Read once, in `Data`

`Projection` is parameterized by `point_id`, so every `Projection[N]` is a separate ItemSpace
with its own cells cache; readers placed there would re-read every file for every policy. They
live instead in an unparameterized **`Data`** Space that `Projection` reaches through a `data`
Reference, so each file is read once per model however many policies are projected, and a test
counts the reads against a registered file set. `Data.input_dir()` resolves the location from
`_model.path.parent` when the model is read, so it works from any checkout.

**The trade-off:** the model is not portable on its own — copy `BU_DE_S/` without the CSVs and
it reads fine, then fails on first evaluation. What you gain is that a diff of the model shows
logic changes only, and an input can be swapped in place: point `Data.mortality_file` at
another same-schema file and the projection follows, with no formula change.

| Reference | Cells | File | Contents and provenance |
|---|---|---|---|
| `model_point_file` | `model_point_table()` | `model_point_table.csv` | Thirteen model points. **Point 1 is the worked-example anchor cell** (aktiv / F30 / BG1 / 1 500 € a month / cover and benefit to 67 / no *Karenzzeit* / monthly). Points 2–13 exercise the unisex twin, the occupational factor, the `dynamik` form, a *Karenzzeit*, an in-force active policy, an in-force claim, an *Endalter* of 60, a *Leistungsendalter* below the *Versicherungsdauer*, the *AU-Klausel*, a *Risikozuschlag*, both escalations off, and a premium override. **The one file with no `provenance` column** — a model point is a configuration, not an assumption, and it is the only exemption from delib's second ruling |
| `inception_file` | `inception_table()` | `inception_table.csv` | Annual *Invalidisierungswahrscheinlichkeit* by attained age 18–66. **[std]** two-slope Gompertz proxy `0.00110 × 1.06^(min(x,45)−30) × 1.13^(max(x,45)−45)`, unisex and **gross of declinature**; DAV 1997 I is DAV property and is **not shipped** [R16]. **The anchor a replacement must preserve is `inc_rate(30) = 0.001100`**, with the age shape and a declaration of whether it is gross or net of declinature |
| `claim_duration_file` | `claim_duration_table()` | `claim_duration_table.csv` | `recov_rate` and `mort_dis_sel_factor` by claim year 1–10, row 11 the ultimate. **[std]**; DAV 1997 RI and DAV 1997 TI are not shipped [R16]. **What must be preserved is the duration shape** — reactivation 0,250 in claim year 1 falling to 0,006 and near zero after about five years, disabled mortality select at 3,0 falling to 1,2. A flat reactivation rate is worth roughly a factor of two on projected benefit |
| `mortality_file` | `mortality_table()` | `mortality_table.csv` | `mort_rate_actv` and `mort_rate_dis` by attained age 18–70. **[std]** Gompertz proxies, active `0.00035 × 1.095^(age−30)` and disabled **exactly 4,00×** it; DAV 2008 T [R17] and DAV 1997 TI [R16] are not shipped. Anchored at `mort_rate_actv(30) = 0.000350`. **What must be preserved is the excess of disabled over active mortality** — never one rate for both states |
| `occupation_file` | `occupation_table()` | `occupation_table.csv` | The five *Berufsgruppen* with loadings and labels: BG1 1,00, BG2 1,40, BG3 2,10, BG4 3,00, BG5 4,50. **[std]**, anchored at 1,00 for office and 3,00 for the reference manual class inside the recalled 2×–4× band [S6]. Carrier classifications are **not comparable with one another** |
| `lapse_file` | `lapse_table()` | `lapse_table.csv` | Annual *Stornoquote* by policy year 1–5, row 6 the ultimate: 4,0 / 4,0 / 3,5 / 3,0 / 2,5 / 2,0 %. **[std]**, and **low by the standards of every other delib product** — a product fact, not a modelling choice, because cover cannot be replaced once health has changed [S16]. The 30-day *Widerruf* sits inside year 1 [REG-R23] |
| `freq_loading_file` | `freq_loading_table()` | `freq_loading_table.csv` | `prem_mode_months` (12 / 6 / 3 / 1) and the *Ratenzahlungszuschlag* `freq_load` (1,00 / 1,02 / 1,03 / 1,05). **[std]**: the ladder is the recalled German market convention and no retrieved document confirms it |

Every file but the model point table carries a **`provenance` column**, one tag per row —
delib's second ruling, and it is machine-checked.

## The published identities

Seven `check_*()` cells, each a no-argument `bool` over all `t` with a per-`t` residual.

**`check_net_cf` — delib ruling 1, in one line:**
`net_cf(t) = prem_zahl_pp(t) × pols_prem(t) − claims(t,"BU_RENTE") − claims(t,"REINTEGRATION") − claims(t,"LAPSE") − expenses(t) − claim_expenses(t)`.

The premium leg is deliberately rebuilt from the *Zahlbeitrag* **actually billed** times the
premium-paying count rather than from `premiums(t) − surplus_credit(t)`, which makes it a real
reconciliation instead of a restatement of `net_cf`'s own formula: it crosses the *Brutto* /
*Zahl* split and fails if the premium is weighted by `pols_if` instead of `pols_prem`.

| Check | Identity |
|---|---|
| `check_states` | `pols_if(t) = pols_actv(t) + pols_dis(t) + pols_runoff(t)` |
| `check_pols_roll_fwd` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t)` |
| `check_dis_roll_fwd` | `pols_dis(t+1) = pols_dis(t) − pols_death_dis(t) − pols_recovery(t) + pols_inception(t)` |
| `check_runoff_roll_fwd` | `pols_runoff(t+1) = pols_runoff(t) − pols_death_runoff(t) − pols_reactivation(t) + pols_recovery(t)` |
| `check_prem_split` | `premiums(t) − surplus_credit(t) = prem_zahl_pp(t) × pols_prem(t)` |
| `check_cover_end` | `claims(t,"BU_RENTE") = 0` wherever `age(t) ≥ benefit_end_age()`, and `premiums(t) = 0` wherever `age(t) ≥ cover_end_age()` |

`check_pols_roll_fwd` is **trivially zero by construction** — `pols_if` is defined by exactly
that recursion — and is published because it is the notes' own identity. `check_states` is the
one that is **not** trivial: `pols_if` is built off the two exits rather than as the sum of the
three ledgers, so comparing it against them catches a life that leaves one ledger without
arriving in another, or arrives in two. The first fixes the definition, the second tests it.

## Modules that are off in the base run

| Module | Switch | Off value | What it does |
|---|---|---|---|
| *AU-Klausel* | `au_uplift`, gated by `au_klausel` | `1.00` | Multiplies the inception rate. Model point 10 has the clause **on** with the uplift at 1,00, so the switch is demonstrably inert. The **clause** is documented — six months of continuous certified *Arbeitsunfähigkeit*, or four plus a specialist prognosis; the AU pension equal to the *BU-Rente*; a cap of 24 months per contract at one carrier and up to 36 at another; set off against a later BU award [S4] [S6] [S8] [S12]. What no retrieved source quantifies is the **loading** it puts on incidence, so shipping a number would still be an invention |
| *Beitragsdynamik* | `beitragsdyn_rate`, gated by `premium_form` | `0.00` on the `level` form | Escalates the insured *BU-Rente* and the annual *Bruttobeitrag* together on each policy anniversary; 3 % on model point 4 |
| *Wiedereingliederungshilfe* | `wiedereingliederung_months` | `6`, and `0` on model point 12 | Monthly *Renten* paid on each **completed** run-off |
| *Leistungsdynamik* | `leistungsdyn_rate` | `0.02`, and `0.00` on model point 12 | In-claim escalation on each onset anniversary |
| *Risikozuschlag* | `risk_factor` | `1.00` | A multiplier on the *Bruttobeitrag* alone |
| Premium override | `gross_prem_ann` | `0.0` = derive by equivalence | Model point 13 supplies 2 400,00 € p.a. instead |

Model point 12 is the anchor with both escalations off: its equivalence gives 865,95 € against
the anchor's 1 013,07 €, so the *Leistungsdynamik* and the *Wiedereingliederungshilfe* together
are worth **147,12 € p.a.**, 14,5 % of the *Bruttobeitrag* — not additively, because both are
paid out of the same claim population.

Three constructions the notes describe are **not implemented**, each because doing so would
stack an unsourced assumption on an already-**[std]** basis: **lapse selection** (strongly
selective in BU, so a non-selective rate understates the surviving book's inception rate —
direction known, size not); **premium-shock lapse** (take-up of the *Beitragsdynamik* increases
is folded into the **effective** `beitragsdyn_rate` instead, which keeps the equivalence
acyclic); and the ***Nachversicherungsgarantie***, needing both a take-up assumption and an
anti-selection loading on the incremental cover.

## Sign convention

`net_cf` is **income positive** — the *Bruttobeitrag* in, the *Beitragsverrechnung*, claims and
expenses out — which is the notes' own orientation and the library-wide sign. `liability_cf`
publishes the same stream outgo-positive, `liability_cf(t) = −net_cf(t)` exactly, and both are
columns of `result_cf()` so the identity is verifiable in the frame rather than only in prose. A
Solvency II best estimate is `Σ v(t) × liability_cf(t)` over the relevant risk-free term
structure, plus a risk margin [REG-R1] [REG-R2] [REG-R4]; **nothing in this library discounts**,
and `rechnungszins` appears only inside the equivalence.

The shape to expect is a large first-month strain — the whole acquisition charge falls in month
0, 937,09 € of the 946,57 € of expense against an 88,64 € instalment, so `net_cf(0) = −884,58
€` — then thin positive margins that decay, cross zero between months 264 and 265 at attained
age 52, and reach −76,85 € in the last month. That crossing is the *Deckungsrückstellung* this
model does not compute being built and run down.

`expenses` is administration only — acquisition, the proportional loading and the flat charge.
The *Leistungsbearbeitungskosten* are `claim_expenses`, separate because they scale with
**claims** rather than policies; commission is not a line at all, sitting inside `acq_rate`.

## Naming

Cells follow lifelib's `basiclife/BasicTerm_S` and `savings/CashValue_SE` wherever those models
have an analogue: `pols_*` for policy counts, plural nouns for cash flows, `*_rate` for **annual**
rates with `*_rate_mth` for their monthly equivalents, `*_pp` for per-policy amounts,
`claims(t, kind)` with an uppercase `kind` string, `pols_if_at(t, timing)` for the end-of-month
read, and `check_*()` / `check_*_resid(t)` for the identities. The full symbol mapping lives in
the `Projection` Space docstring.

The **monthly cohort-vector chassis** is shared with frlib's `Dep_FR_S` (*assurance
dépendance*): `dis_cohorts` ↔ `dep_cohorts`, `pols_dis_dur(t, z)` ↔ `pols_part_dur` /
`pols_tot_dur`, `seed_claim_dur` ↔ `seed_dur`, and `cohort_len`, `rente_pay_pp(t, z)`,
`pols_prem` and `pols_recovery` mean the same thing on both. `pols_runoff_slot` is this
model's counterpart of `Dep_FR_S`'s `pols_red` — a small holding ledger a naive
implementation omits, which is a first-order error in both. Inside this library,
`Pflege_DE_S` is the other monthly multi-state model and shares the **vocabulary** —
`pols_prem`, `pols_if_at`, `check_states`, `check_pols_roll_fwd` — but not the cohort
vectors: its ledgers (`pols_karenz(t, g, z)`, `pols_grad(t, g)`, `pols_pg(t, g)`,
`pols_reactiv`) are indexed by *Pflegegrad* rather than by claim duration.

Five names needed care:

| Notes | Cells | Why |
|---|---|---|
| `κ` vs `ρ` | `occ_factor` / `risk_factor` | One loads the inception rate and moves every claim; the other loads the *Bruttobeitrag* and moves nothing else |
| `R(t)` vs `R_p(t, z)` | `bu_rente_pp` / `rente_pay_pp` | The **insured** *BU-Rente* on the policy clock against the amount **in payment** on the onset clock |
| `L(t)` vs `L_p(t)` | `pols_if` / `pols_prem` | In force against premium-paying: the difference *is* the *Beitragsbefreiung* |
| `i(x)` vs the composed rate | `inc_rate_base` / `inc_rate` | The table rate and the rate after κ, α and υ, published separately so a substituted table already net of declinature is visible |
| `l_r(t,k)` vs `V_r(t,k)` | `pols_runoff_slot` / `runoff_val` | A count and a value: the run-off carries frozen *BU-Renten*, so both are needed |

`status`, `sex`, `au_klausel` and `claim_duration_init` drive little or nothing in the base
parameterization and are exposed as documented cells rather than dropped: a silently missing
column is worse than an inert one.

## Standardizations used

Everything in this table is **[std]**. The product is unusually **[std]**-heavy and that is the
correct outcome, not a defect: the *mechanics* are well established and cited above, and it is
only the *levels* that no retrievable document supplies.

| Standardization | Value | Rationale |
|---|---|---|
| Inception table | `0.00110 × 1.06^(min(x,45)−30) × 1.13^(max(x,45)−45)`, anchored at `i(30) = 0.001100` | DAV 1997 I is not public and is not shipped [R16]. The **shape** is what the research establishes — flat to 30, moderate through the forties, sharply accelerating after — and the level is anchored so the worked example reproduces exactly |
| Occupational loadings | BG1 1,00 … BG5 4,50 | One base table with occupational loadings is how German BU pricing works; the 1,00 / 3,00 anchors sit inside the recalled 2×–4× manual/office band, the rest interpolated geometrically. **No retrieved document supports the classification**: the NÜRNBERGER AVB was read in full for the 2026-08-30 pass and never uses the word *Berufsgruppe*, and no *Berufsgruppenverzeichnis* is published at a public address [S6] |
| Reactivation table | 0,250 → 0,006 by claim year | DAV 1997 RI is not shipped [R16]. Front-loading is the established shape; the levels are construction, and there is **no age-at-disablement dimension**, which the real table has |
| Active-lives mortality | `0.00035 × 1.095^(age−30)` | DAV 2008 T is not shipped [R17]. An insured-lives *Todesfall*-character shape, not a population table |
| Disabled-lives mortality | exactly **4,00 ×** the active column, times select factors 3,0 / 2,0 / 1,6 / 1,4 / 1,3 / 1,2 | DAV 1997 TI is not shipped [R16]. Defining the column *from* the active one rather than rounding its own formula independently makes `mort_rate_dis(t,z) / mort_rate(t)` exactly 12,0 at claim duration 1 and 4,8 ultimately at every age, so "never one rate for both states" is an exact identity instead of a tolerance |
| `accept_factor` | **0,80** | The *Anerkennungsquote*, recalled at 75–80 % [R21] [R20] `[unverified]`. Applied to the **inception rate**, on a table that is gross of declinature |
| `au_uplift` | **1,00** everywhere | No source quantifies the *AU-Klausel*'s effect on incidence. An inert switch is honest; an invented loading is not |
| Lapse table | 4,0 % falling to 2,0 % | No German insurer publishes a BU *Stornoquote*. The level is low, which is a product fact [S16]; **lapse selection is not modelled**, and the direction of that error is one-sided |
| Monthly conversion | `p_m = 1 − (1 − p)^(1/12)` on every annual rate | One convention applied uniformly to `i`, `r`, `q^a`, `q^i` and `w` |
| Processing order | mortality → lapse → inception; then disabled deaths → terminations; then the run-off | Taking incidence first gives `0.000073362928` against `0.000073111651` in month 0 — 0,34 %, compounding over 444 months |
| First-order loads | 1,30 / 0,70 / 0,80 / 0,80, **no lapse** | Prudence for a disability product forks: higher incidence, lower reactivation, lower disabled and active mortality, and no anticipation of a favourable decrement |
| `rechnungszins` | **1,00 % p.a.** | The *Höchstrechnungszins*. **The figure is sourced**: DeckRV § 2 Abs. 1 fixes it "auf 1 Prozent", and § 2 Abs. 2 makes the rate used at conclusion apply for the whole term [R13]. **The 1 January 2025 commencement is not in the consolidated text and stays `[unverified]`** [REG-R15]. Used only in the equivalence |
| `acq_rate` | **2,5 % of the *Beitragssumme***, once at issue | Sits **at** the § 4 DeckRV *Höchstzillmersatz*: "Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten" [R13] [REG-R16], restated by both retrieved AVB as 2,5 % of the premiums payable over the term [S1] [S6]. The ceiling is the only sourced number in the charge structure, and the level is a choice to sit at it |
| `admin_prem_rate` | **9 % of the *Bruttobeitrag*** | A construction, and **not** because the disclosure does not exist: VVG-InfoV § 2 Abs. 1 Nr. 1 with Abs. 2 and Abs. 4 requires a German BU insurer to state the calculated acquisition costs and the administration costs in euro, and one AVB points the customer to the *Produktinformationsblatt* for them [R12] [S6]. **No PIB was obtained** [S13], so the level here is a choice. A pure risk contract does separately lack an *Effektivkosten* figure, § 2 Abs. 1 Nr. 9 confining that to contracts whose obligation is certain [S14] |
| `admin_flat_ann` | **18,00 € p.a.**, charged 1/12 monthly, **uninflated** | A German *Verwaltungskostenzuschlag* is fixed in the tariff at conclusion |
| `claim_assess_cost` / `claim_maint_cost_mth` | **800,00 €** per inception / **12,00 €** per month in payment | The BU-specific charge a modeller from a term-life background forgets. Flat euro amounts, which is why a heavier class carries a premium below the ratio of its inception rates |
| `freq_load` | 1,00 / 1,02 / 1,03 / 1,05 | The recalled German *Ratenzahlungszuschlag* ladder `[unverified]` — the retrieved AVB name the frequencies (single, monthly, quarterly, half-yearly, annual) but no loading [S1]; it scales *Brutto* and *Beitragsverrechnung* together |
| `beitragsverrechnung` | **0,70**, held constant | Midpoint of the recalled 0,60–0,75 common range inside a 0,50–0,80 band `[unverified]` — **no retrieved document gives a ratio**, though two now state the mechanic in their own words [S6] [S12]. **The largest single parameter uncertainty in the model**, and holding it constant its largest discretionary assumption |
| `leistungsdyn_rate` | **2 % p.a.** | Midpoint of the recalled 1–3 % menu. A BU model without in-claim escalation misses the product's dominant long-duration sensitivity |
| `wiedereingliederung_months` | **6**, paid on the **completed** run-off | Recalled range 3–12 monthly *Renten*. Paying it on every recovery instead overstates it by exactly the run-off's own mortality — 418,79 € against 409,61 € on the anchor cell |
| Run-off values not escalated | no *Leistungsdynamik* inside the three months | Three months is inside one onset anniversary in every realistic case, and it removes a second duration dimension |
| *Karenzzeit* premium | still payable inside it | The *Beitragsbefreiung* runs with the **benefit**, so a life not yet paid still pays |
| *Leistungsendalter* premium | **not** resumed after it | The waiver is read as keyed to the **state**. The alternative reading is defensible and is named |
| Age basis | age last birthday advancing at the **policy anniversary** | The model carries no dates; a date-based implementation carries a fractional offset of at most one year |
| `dynamik` pricing | one equivalence at inception on the whole escalating stream | Internally consistent, acyclic, and **not** the market's annual-repricing practice — recorded rather than corrected |
| The thirteen model points | — | Configuration rather than observation: no rate card, no commercial envelope and no *Berufsgruppenverzeichnis* was obtained. One envelope datum did arrive: a retrieved AVB caps total BU, EU and *Grundfähigkeit* entitlement at 60 % of regular annual gross income [S9], which the anchor's 1 500 €/month is well inside |

The only quantities in the model that are **not** standardizations are the structural rules: the
three-month run-off [R3], the *Beitragsbefreiung* while the *BU-Rente* is in payment [S1] [S2],
the *Brutto* / *Zahlbeitrag* pair and its immediate credit [R10] [R14], the unisex rule [R15],
the zero lapse benefit and the absence of a death and a maturity benefit [S1] [R8] [R9], and the
§ 4 DeckRV ceiling the acquisition charge sits at [R13] [REG-R16]. Each of those is now backed by a
document that was read: the statutes as canonical XML, the contractual rules in the GDV model
conditions and four carrier AVB — see `sources.md`.

## Tests

`tests/test_berufsunfaehigkeit_de.py` asserts the frame itself — `list(result_cf().index) ==
list(range(proj_len()))`, so 444 rows `t = 0 … 443` on the anchor cell, ending at the last
index `proj_len() − 1` — then all eighteen printed rows of the notes' worked
example to the cent and the state ledgers to six decimals, the full-precision totals against
the sum-of-rounded-cells the notes also print, the derived *Bruttobeitrag* of 1 013,0697 € p.a.
reached two independent ways, month 0 rebuilt term by term with a calculator, the first
inception and the first *BU-Rente* from the annual rates, the § 174 run-off traced through one
cohort, the four-way decrement closure, the *Brutto* / *Zahl* ratio surviving aggregation, the
*Beitragsdynamik* variant's twelve printed rows and totals, the seven `check_*` identities with
their residuals, and **one test per numbered modeling pitfall** — eighteen of them. The
whole-model-point-table sweep is **not** here: `tests/test_model_conventions_de.py` owns the
library's single sweep, because a model point's first evaluation is the most expensive thing in
the run.

```bash
python -m pytest lifelib/libraries/delib/tests/test_berufsunfaehigkeit_de.py -q
python -m pytest lifelib/libraries/delib/tests/test_model_conventions_de.py -q -k BU_DE_S
```

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-berufsunfaehigkeit-r1
[R10]: #delib-berufsunfaehigkeit-r10
[R12]: #delib-berufsunfaehigkeit-r12
[R13]: #delib-berufsunfaehigkeit-r13
[R14]: #delib-berufsunfaehigkeit-r14
[R15]: #delib-berufsunfaehigkeit-r15
[R16]: #delib-berufsunfaehigkeit-r16
[R17]: #delib-berufsunfaehigkeit-r17
[R2]: #delib-berufsunfaehigkeit-r2
[R20]: #delib-berufsunfaehigkeit-r20
[R21]: #delib-berufsunfaehigkeit-r21
[R29]: #delib-berufsunfaehigkeit-r29
[R3]: #delib-berufsunfaehigkeit-r3
[R5]: #delib-berufsunfaehigkeit-r5
[R8]: #delib-berufsunfaehigkeit-r8
[R9]: #delib-berufsunfaehigkeit-r9
[REG-R1]: #delib-reg-r1
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R29]: #delib-reg-r29
[REG-R34]: #delib-reg-r34
[REG-R4]: #delib-reg-r4
[REG-R48]: #delib-reg-r48
[REG-R50]: #delib-reg-r50
[REG-R53]: #delib-reg-r53
[std]: #delib-std
<!-- END generated citation links -->
