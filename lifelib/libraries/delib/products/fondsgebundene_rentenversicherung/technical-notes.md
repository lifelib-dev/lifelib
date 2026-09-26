# Technical Notes

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30.

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`FRV_DE_S`**, **monthly** grid — for the standardized composite German *fondsgebundene
Rentenversicherung* defined in `product-spec.md` (same directory). This is not any single
insurer's product. [S#]/[R#] tags refer to the source list in `sources.md` (numbering carried
from `_research/fondsgebundene_rentenversicherung.md`; frozen); [REG-R#] tags refer to the
cross-product reference library `references/regulatory-and-actuarial-references.md` (its own
R-numbering). **[std]** marks a standardization introduced for the reference implementation;
[unverified] marks a claim no retrieved document or search result confirmed. Parameter values are
identical to those in `product-spec.md`. Cells names, model-point columns and CSV headers are
English `lower_snake_case`; German terms of art keep their German form in prose, and three of
them — *Rentenfaktor*, *Beitragssumme*, *Stornoabzug* — keep it in the cells names too, because
each names a quantity with a statutory definition and no English equivalent that would not
mislead.

**The retrieval condition, once, because it governs every number below.** delib was **drafted**
with all HTTP egress blocked and this product's search budget already spent, so nothing cited here
was retrieved and the first draft rested on the authoring model's own knowledge of German practice,
disciplined by [std] and [unverified]. The citations have since been **re-verified against the
primary documents**: **eighteen of the forty-four entries in `sources.md` now say `Retrieved: yes`**
— one carrier's complete *Bedingungswerk* and its *Basisinformationsblätter* [S2] [S15] and the
statutory core in canonical text among them — two say `partly`, and twenty-four still say `no`,
most of those because no address for the document was ever established. Treat a claim as sound
where its entry says `Retrieved: yes`, and as a pointer rather than a certificate — an instrument
named, not one anybody checked — where it does not. The **mechanics** are common ground in German
practice and several are now read in a real wording. The **levels** are almost entirely **[std]**:
no lapse rate was established anywhere, and outside the one carrier that could be read not one
charge rate and not one *Rentenfaktor* was established at any carrier.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted**, on a monthly
  grid, for a single-policy model point on an expected (probability-weighted) basis. Discounting,
  the *Deckungsrückstellung*, Solvency II technical provisions and capital are out of scope and
  are referenced, never computed (see *Valuation and reserve pointers*).
- **`net_cf` is the non-unit stream, and that is the single most important convention here.**
  Every benefit this contract pays before *Rentenbeginn* — the death benefit up to the fund, the
  *Rückkaufswert*, the *Teilentnahme*, the capital released at *Rentenbeginn* — is funded by
  cancelling the policyholder's own units, so a gross presentation would count the same money
  twice. `net_cf(t)` is therefore **charges collected, less insurer expenses, less commission,
  less the death strain**. `expenses` **excludes** commission, which is published as its own
  `commissions` cells and column — the delib convention, stated the same way on `KLV_DE_S`,
  `Basis_DE_S`, `Riester_DE_S` and `RLV_DE_S`, and the opposite of the frlib chassis. The
  gross flows are still published — `premiums`, `prem_to_av`, `claims_death`,
  `claims_lapse`, `claims_maturity`, `withdrawals` and `av_releases` are all `result_cf()`
  columns — and `check_benefit_funding()` asserts that they net exactly. This is the same
  decomposition `frlib/products/assurance_vie_uc` uses for a French *unités de compte* contract;
  what is German about it is that the *Anlagestock* rule makes the unit assets and the unit
  liability move together by law [R15] [REG-R7], so the model has **no investment-mismatch term**.
- **Projection frequency.** Monthly. Sourced in substance rather than chosen: the dominant premium
  frequency is monthly, the *Risikobeitrag* and the *kapitalbezogenen Verwaltungskosten* are
  levied monthly by unit cancellation, and the *Abschluss- und Vertriebskosten* instalment runs
  for exactly **60 months** [R1] [REG-R28]. An annual grid cannot place the month-60 cliff.
- **Projection horizon.** The ***Aufschubzeit* only.** `proj_len() = 12 × (annuity_age −
  entry_age)` is the **number of policy months** from inception and so the frame's **exclusive
  end**; the last projected month is `t = proj_len() − 1`, the month in which *Rentenbeginn*
  falls. At the end of it the units are cancelled, the *Fondsguthaben* is converted at the
  *Rentenfaktor* and the contract leaves this model. The payout phase — the *Überschussrente*, the
  *Rentengarantiezeit*, the *Rentenbezugskosten* — belongs to `products/sofortrente/`.
- **The frame is 0-based in policy months counted from inception, and an in-force model point
  opens partway through it.** `t` is the policy month index from the contract's own inception with
  **`t = 0` the inception month**, so `t = 60` means the same thing on every model point: the
  first month after the acquisition-charge instalment ends. Period `t` runs from time `t` to time
  `t + 1`. The frame is `range(proj_start(), proj_len())` — `t = proj_start() … proj_len() − 1` —
  with `proj_start() = duration_init_m`, which is `0` for new business and `96` for the in-force
  cell; `duration_init_m` is an elapsed count and is already 0-based, so it **is** the first
  projected index. That is what lets a single `charge_acq_pp(t)` rule serve both without a
  duration offset, and it is why the library's conventions suite asserts frame **contiguity** and
  the last index rather than the first. **The contractual policy year is the 1-based label
  `policy_year(t) = t // 12 + 1`**, derived from `t` and never indexed by; it is what the annual
  input tables are keyed on.
- **Timing conventions [std].** Premium in advance at the start of the month; units bought at the
  *Anteilspreis* at the start of the month; the month's investment return then accrues; the
  fund-based charges, the *Stückkosten*, any *Teilentnahme* and the *Risikobeitrag* are taken at
  the end of the month at the closing *Anteilspreis*; decrements act at the end of the month,
  deaths before lapses. The *Bewertungsstichtag* lag a real contract carries — how many dealing
  days after receipt units are bought — disappears on a monthly grid and is not modelled.
- **The net amount at risk is observed once a month, before the risk charge that prices it.** The
  death benefit is therefore the floor **as observed before that month's *Risikobeitrag***, so the
  insurer's non-unit cost per death is **exactly the *riskiertes Kapital*** and nothing else. That
  half-month discretization is **[std]** and is the same one `UC_FR_S` makes for the French
  *garantie plancher*.
- **Age basis.** Age last birthday at inception, stepping at each policy anniversary:
  `policy_year(t) = t // 12 + 1`, `age(t) = entry_age + policy_year(t) − 1 = entry_age + t // 12`.
  **At `t = proj_len() − 1` the attained age is `annuity_age − 1`**, because the annuity begins at
  the **end** of that month. The *Rentenfaktor* is read at `annuity_age`, not at
  `age(proj_len() − 1)`, and getting that wrong is a listed pitfall.
- **One fund.** The composite carries a single composite fund; with a deterministic return a
  multi-fund split is arithmetically identical to one fund at the weighted return. *Fondswechsel*
  and *Ablaufmanagement* are therefore represented as changes to the assumed return, not as
  reallocations, and the model cannot show dispersion between funds.
- **Currency and precision.** EUR throughout. Unit counts are carried at full precision and
  reported to six decimals, money to the cent **[std]**. `pols_if` to six decimals.
- **Out of scope, and said so rather than left to be discovered.** No *Überschussbeteiligung*
  credit (the omission understates the projected *Fondsguthaben*); no hybrid or guarantee
  mechanism of any kind; no *Widerruf* window; no stochastic asset model, so nothing here may be
  compared with a PRIIPs performance scenario [R8] [R9] [REG-R32]; no tax computation — the tax
  rules enter only through the lapse shape; and no payout-phase machinery beyond the annuity the
  *Rentenfaktor* buys.

---

## Model point attributes

Columns of `model_point_table.csv`, indexed by `point_id`. The last column names the model points
that exercise the attribute non-trivially, so a reader can find the row that tests it.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | index; **model point 1 is the worked example's anchor cell** | all |
| `policy_id` | str | label, e.g. `DE-FRV-0001` | all |
| `sex` | enum {M, F} | **reporting only.** German tariffs are unisex for contracts from 21 December 2012 [REG-R34], so this must not enter pricing | 1, 4, 9 |
| `entry_age` | int (ALB) | age at inception | all |
| `duration_init_m` | int | policy months already elapsed at the valuation date; 0 for new business. An **elapsed count**, already 0-based, so it is `proj_start()` itself | 6 |
| `pols_if_init` | float | policies the model point represents | all |
| `annuity_age` | int | age at *Rentenbeginn*; fixes `proj_len()` and the *Rentenfaktor* row | 13 (70), all others 67 |
| `prem_form` | enum {`laufend`, `einmal`} | recurring or single premium | 2 (`einmal`) |
| `prem_pp` | EUR | the **instalment the policy states**, or the *Einmalbeitrag*. Already contains whatever *Ratenzahlungszuschlag* the tariff applied | all |
| `prem_mode_months` | int {1, 3, 6, 12} | payment frequency in months | 3 (3), 4 (6), 5 (12) |
| `prem_term_y` | int | premium-paying term in years; 0 for `einmal` | 12 (2 years against a 12-year deferment) |
| `dynamik_rate` | float | *Beitragsdynamik*, annual premium increase at each anniversary; 0 = off | 10 (3 %) |
| `pup_month` | int | 0-based policy month from which the contract is *beitragsfrei*; 0 = never (the sentinel, not the inception month) | 7 (120) |
| `db_form` | enum {`fund`, `prem_return`, `pct_fund`, `sum_assured`} | *Todesfallleistung* shape | 2, 13 (`fund`); 4, 12 (`pct_fund`); 7 (`sum_assured`); rest `prem_return` |
| `db_pct` | float | multiple of the fund used by `pct_fund` | 4, 12 (1.10) |
| `sum_assured` | EUR | *garantierte Mindesttodesfallleistung* used by `sum_assured` | 7 (40,000) |
| `charge_id` | str | key into `charge_table.csv` | 5 (`std_high`), 11 (`std_netto`), 13 (`std_low`) |
| `scenario_id` | str | key into `fund_scenario_table.csv` | 7 (`zero`), 11 (`etf`), 12 (`stress`) |
| `rentenfaktor_id` | str | key into `rentenfaktor_table.csv` | 13 (`rich_current`) |
| `unit_price_init` | EUR | *Anteilspreis* at the projection's opening, i.e. `unit_price_open(proj_start())` | 6 (118.40); 100.00 elsewhere |
| `units_init` | float | units held at the projection's opening | 6 (190.0); 0 elsewhere |
| `cum_prem_init` | EUR | premiums paid before the valuation date — the *Beitragsrückgewähr* base | 6 (24,000.00) |
| `topup_month` | int | 0-based month of a *Zuzahlung*; 0 = none (the sentinel) | 9 (120) |
| `topup_amount` | EUR | the *Zuzahlung* | 9 (20,000.00) |
| `wd_month` | int | 0-based month of a *Teilentnahme*; 0 = none (the sentinel) | 9 (240) |
| `wd_amount` | EUR | the *Teilentnahme* | 9 (15,000.00) |
| `ablauf_flag` | bool | *Ablaufmanagement* return glide on | 8 |
| `kapitalwahl` | bool | *Kapitalwahlrecht* elected at *Rentenbeginn* — a **reporting** split, since both routes release the same *Fondsguthaben* from this model | 13 |

Two columns are assumptions in disguise and are tagged where they are used rather than in the
file, because `model_point_table.csv` is the library's one provenance-exempt input: `sum_assured`
and `db_pct` are **[std]** levels chosen to exercise the two death-benefit shapes with a positive
net amount at risk, and `dynamik_rate` is **[std]** at 3 % because no carrier's dynamic step was
established.

**The thirteen model points.** 1 anchor (new business, monthly, *Beitragsrückgewähr*); 2 single
premium with a fund-only death benefit, so `charge_risk` is structurally zero; 3 quarterly;
4 half-yearly with a 110 % death benefit; 5 annual on the top-of-range charge tariff, which is
also the only point with a non-zero *Stornoabzug*; 6 in-force at duration 96, past the
acquisition window; 7 *beitragsfrei* from `t = 120` with a fixed *Mindesttodesfallleistung* on a
zero-return fund — the decay case; 8 *Ablaufmanagement*; 9 *Zuzahlung* and *Teilentnahme*;
10 *Beitragsdynamik*; 11 *Nettotarif* on an ETF fund; 12 a two-year premium term inside a
twelve-year deferment on the stress path, which is the acquisition-spread boundary; 13 a
*Rentenbeginn* at 70 with a current *Rentenfaktor* above the guaranteed one, so the `max()` bites.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_start()` | first projected month, `duration_init_m` (0-based) | once |
| `proj_len()` | projected months from inception, `12 × (annuity_age − entry_age)`; the frame's **exclusive** end, so the last month is `proj_len() − 1` | once |
| `beitragssumme()` | sum of premiums **payable** over the premium term at the initial level — the acquisition-charge base [R12] [REG-R16] | once |
| `unit_price(t)` | *Anteilspreis* at the **end** of month `t`, `= unit_price_open(t) × (1 + i(t))` | monthly |
| `unit_price_open(t)` | *Anteilspreis* at the **start** of month `t`; `unit_price_init` at `t = proj_start()` and `unit_price(t − 1)` after it. A cells of its own because a 0-based frame has no `t = −1` to read | monthly |
| `units_pp(t)` | *Anteileinheiten* per policy at the **start** of month `t` | monthly recursion |
| `av_pp(t)` | *Fondsguthaben* per policy at the start of month `t`, `= units_pp(t) × unit_price_open(t)` | derived |
| `av_pp_at(t, timing)` | the within-month balances: `"BEF_CHARGE"`, `"AFT_CHARGE"`, `"AFT_WD"`, `"BEF_DECR"` | within month |
| `av_at(t, timing)` | `av_pp_at(t, timing) × pols_if(t)` — the in-force fund at that point | derived |
| `cum_prem_pp(t)` | cumulative **gross** premiums paid to and including month `t`, seeded at `cum_prem_init` | monthly |
| `cum_charge_acq_pp(t)` | cumulative acquisition charge withheld — the ledger `check_acq_charge()` closes | monthly |
| `db_floor_pp(t)` | guaranteed minimum death benefit under `db_form` | monthly |
| `nar_pp(t)` | *riskiertes Kapital*, `max(db_floor_pp(t) − av_pp_at(t, "AFT_WD"), 0)` | monthly |
| `pols_if(t)` | policies in force at the **start** of month `t`; `pols_if(proj_start()) = pols_if_init()` | monthly decrements |
| `pols_if_at(t, timing)` | `"BEF_DECR"`, `"AFT_DEATH"`, `"AFT_DECR"`; `"AFT_DECR"` is the end-of-month count | within month |
| `pols_death(t)`, `pols_lapse(t)`, `pols_maturity(t)` | the three exits; `pols_maturity` is non-zero only at `t = proj_len() − 1` | monthly |

There is **no** *Deckungskapital*, **no** guaranteed-value state and **no** paid-up-benefit
state. That is a statutory fact about the product, not a simplification: § 169 VVG sends a
fondsgebundene contract to the *Zeitwert* [R1] [REG-R28], and § 165 VVG's conversion to a
*prämienfreie Versicherung* recomputes nothing on this chassis [R3].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| What is guaranteed | The **number** of *Anteileinheiten*, never their value | [S1]; *Anlagestock* [R15] [REG-R7] |
| *Beitragsverrechnung* order | gross *Beitrag* → less the acquisition instalment → less the premium-based admin charge → the remainder is the *Anlagebeitrag* and buys units | [S1] |
| Acquisition-charge cap | **2.50 %** of the *Beitragssumme* — the *Höchstzillmersatz* of 25 ‰ | [R12] [R13] [REG-R16] [REG-R20] |
| Acquisition-charge spreading | Evenly over the first **five contract years**, i.e. `min(60, 12 × prem_term_y)` months | [R1] [REG-R28] |
| Death benefit (base) | `max(Fondsguthaben, Summe der gezahlten Beiträge)` — *Beitragsrückgewähr* | [S2] |
| *Risikobeitrag* base | `max(Todesfallleistung − Fondsguthaben, 0)`, recomputed monthly | [S1] |
| *Risikobeitrag* mortality basis | A **death** table — DAV 2008 T, first order — not the annuity table | [R17] [REG-R48] |
| *Rentenfaktor* rule | `max(garantierter, aktueller)` at *Rentenbeginn* | [S4] [R22] |
| *Rentenfaktor* conversion basis | DAV 2004 R, generational, at an underlying rate of currently 0 % p.a. | [S10] (classic tariff, transfer is an inference); [R16] [REG-R49] |
| *Rückkaufswert* | The ***Zeitwert***, which on a pure unit-linked contract **is the *Fondsguthaben*** | [R1] [REG-R28] |
| *Stornoabzug* | Only if *vereinbart*, *beziffert* and *angemessen*; never for untilgte acquisition costs | [R1] [REG-R28] [REG-R36] |
| *Kündigung* | At any time for the end of the current *Versicherungsperiode* | [R2] [REG-R28] |
| *Beitragsfreistellung* | Premium-based charges stop; fund-based charges, the *Stückkosten* and the *Risikobeitrag* continue by unit cancellation | [R3] [REG-R28] |
| Unisex | Sex may not enter the premium or the benefit | [REG-R34] |
| *Überschussbeteiligung* | Risk and cost results only; **not projected** | [R5] [R14] [REG-R9] [REG-R18] |

### (b) Insurer-discretionary current elements

Thin, and thinner than on the sibling general-account products, because the discretion on this
contract bites through the **charge scale** and the **current *Rentenfaktor***, not through a
declared rate.

| Input | Snapshot value | Basis |
|---|---|---|
| Charge scale (`charge_table.csv`) | `std_gross`: α 2.50 %, spread 60 months, β 4.00 %, γ 0.30 % p.a., *Stückkosten* 3.00 EUR/month, *Zuzahlungskosten* 2.50 %, *Stornoabzug* 0.00 % | levels **[std]** (1) |
| Charge variants | `std_netto` (α 0, β 1.00 %, γ 0.20 %, fee 2.00); `std_high` (β 10.00 %, γ 1.20 %, fee 5.00, *Stornoabzug* 2.00 %); `std_low` (α 1.00 %, β 2.00 %, γ 0.10 %, fee 0.00) | **[std]** (1) |
| *Kickback* credited back | **0.00 % p.a.** — the composite's fund is passive and pays no trail | **[std]** (2) |
| Current *Rentenfaktor* | `std_2026`: equal to the guaranteed factor, so the `max()` is exercised without injecting an unsourced uplift. `rich_current`: 12 % above it | **[std]** (3) |
| *Ablaufmanagement* | A linear glide of the **gross** return from the scenario's rate to `mmkt_return_ann` = 1.50 % p.a. over the last 60 months; off unless `ablauf_flag` | **[std]** (4) |
| *Überschuss* credit | **None.** Omitting it biases the projected *Fondsguthaben* **downward** | [R5] [R14]; omission **[std]** |

1. **Every level here is still [std], and it can now be calibrated against one real tariff and
   one market distribution.** The anchor is the 25 ‰ *Höchstzillmersatz* — *"Der Zillmersatz darf
   25 Promille der Summe aller Prämien nicht überschreiten"*, § 4 Abs. 1 Satz 2 DeckRV [R12]
   [REG-R16] — and the composite takes **the cap**. The observed comparators, from DEVK's
   *Basisinformationsblätter* for a 1 000 € annual premium [S15]: acquisition **2,50 % der
   kumulierten Anlage** (equal to `std_gross`'s α), *Verwaltungskosten* **6,90 % der jeweils
   eingezahlten Anlage** (against β = 4,00 %), **0,42 % des Werts Ihrer Anlage pro Jahr** (against
   γ = 0,30 %), and **18 EUR pro Jahr** (against a 3,00 €/month fee, i.e. 36 €/yr). **`std_gross`
   is therefore a cheap tariff, not an average one** — its implied reduction in yield of roughly
   1 % p.a. sits below the market's lower quartile of 1,30 % at exactly this model point, where
   the weighted mean is **1,90 %** and insurers above 4 % exist at every age-and-term combination
   [R11], and where the DEVK sheet reports **1,4 %–3,4 %** over 30 years [S15]. Every observed
   level falls inside the argued range that `std_high` and `std_low` bracket. Nine of the ten
   other named carriers still supply no level [S3]–[S14] [S16] [S18] [R23] [R24]. `std_netto` is
   the commission-free tariff [S18], and the difference between its reduction in yield and
   `std_gross`'s **is** the acquisition load; note that a *real* net tariff's published
   *Effektivkosten* excludes the client's separate adviser fee [R10], so the delib gap is cleaner
   than a market comparison would be.
2. **Both questions this footnote called unresolved now have answers, and the zero is a choice
   rather than an evasion.** BaFin establishes that insurers receive *Rückvergütungen* out of the
   fund's *Verwaltungsvergütung*, must test them for *Fehlanreize*, and must consider passing them
   back through reduced calculated costs, an RfB allocation above the MindZV minimum, a
   *Kostenüberschussanteil* or a dedicated *Überschussanteil* [R10] [R15] [REG-R33]; one carrier's
   AVB uses them *"zur Deckung etwaiger Verwaltungskostenverluste"* and puts the remainder into
   the RfB [S2]; and the market levels are known — rebates on about a third of new business at a
   weighted mean just over **0,30 % p.a. of the *Fondsguthaben***, up to over **1,20 %**, of which
   about 52 % is returned on average, with a further 19 % of business carrying rebates paid
   directly to the intermediary at about 0,50 % [R11]. So `0.00 %` models the cheap end of a real
   and material flow, and the composite's argued 0 %–0,50 % range understates the observed one.
   How a credited rebate enters the PRIIPs cost calculation is the one limb still open [R7] [R8]
   [REG-R32].
3. Setting the current factor equal to the guaranteed one keeps the base run reproducible from
   the derivation alone while still exercising the `max()`. The 12 % uplift on `rich_current` is a
   round figure chosen so the `max()` visibly bites; **it is not a market observation** — and the
   consumer literature suggests a much wider real spread, guaranteed factors of 50–70 % of the
   current one being described as common `[unverified]` [R22], so `std_2026` is the conservative
   end and `rich_current` is nowhere near the generous one.
4. **The *Ablaufmanagement* parameters are established at two carriers, and they disagree** —
   which is why the module is switchable. DEVK runs it as an **opt-out default**, over the **last
   five years**, in **monthly** tranches on an explicit 1/60, 1/59, 1/58 … schedule, into a
   low-risk target fund, free of charge and with fund switching suspended while it runs [S2];
   Allianz offers it as an **option** over the **last three years** [S3]. The composite's 60-month
   linear glide matches the observed default at one carrier in span and destination; the tranche
   schedule differs, since 1/60 of a shrinking balance is not a linear glide of the return.

### (c) Behavioral / experience assumptions (modeler's view)

**Every input in this class is [std].** No German unit-linked lapse rate, paid-up rate,
*Kapitalwahlrecht* take-up or expense loading was established anywhere in this corpus.

**Mortality — two bases, and the wedge between them is the product.** The tariff prices the
*Risikobeitrag* on a **first-order death table**; the projection decrements on the
**second-order** best estimate [REG-R47]. **That two-basis structure is confirmed in a real
tariff** — DEVK uses *"Sterbetafel DAV 2004 R"* for the annuity and a separate order for the
*Risikobeiträge* [S2] — **but the table this library names for the risk charge is not the one
that tariff uses.** DEVK prices the monthly *Risikobeiträge* on *"einer mit 65 Prozent gewichteten
geschlechtsunabhängigen Ausscheideordnung auf Basis der Sterbetafel DAV 1994 T"*, and keeps
DAV 2008 T [R17] [REG-R48] for its underwritten *Risiko-Zusatzversicherung*. On an unwritten
*Beitragsrückgewähr* cover, a first-order basis can be an old heavy table scaled **down** as
easily as a modern table loaded **up**; the shipped proxy stands for either. Both orders are
**unisex**, which is [REG-R34] showing in a real *Rechnungsgrundlage*. DAV tables are the property
of the Deutsche Aktuarvereinigung, are not public and are **not redistributed by this library**.
The shipped `mort_table.csv` is a **[std] Gompertz-form proxy** of the first-order table:

    mort_rate_tariff_at_age(x) = 0.00080 × 1.10^(x − 37),   ages 18–100

**anchored at `q(37) = 0.00080` exactly**, which is the number the worked example rests on and
which a substitute table must preserve if the example is to reproduce. The 10 % per year of age
is an insured-lives death gradient, not a population one — a German term insurer's book is
**selected**, and a proxy built on population mortality overstates claims at the working ages this
product lives at [REG-R48] [REG-R52]. The best estimate is a flat ratio:

    mort_be_factor = 0.75     mort_rate(t) = 0.75 × mort_rate_tariff(t)

A flat ratio is crude and is stated as such; what it buys is that the *Risikoergebnis* is exactly
`(1 − 0.75) = 25 %` of the *Risikobeitrag* collected, which is a closed-form check a reader can
verify with a calculator. What a replacement must preserve: a first-order margin **above** the
best estimate for a death cover, which is the opposite direction from the annuity table
[REG-R47].

**Monthly conversion, and the asymmetry between mortality and lapse [std].** Mortality is split
**linearly**, `mort_rate_mth(t) = mort_rate(t)/12`, because the tariff's own *Risikobeitrag* is
`q(x)/12 × riskiertes Kapital` and the charge and the decrement must rest on the same split or the
model manufactures a risk result out of a rounding convention. Lapse is split **geometrically**,
`lapse_rate_mth(t) = 1 − (1 − lapse_rate(t))^(1/12)`, because nothing is priced off it and the
annual rate is the observable that must be reproduced over twelve months. Both conventions are
stated, and mixing them across the two mortality bases is a listed pitfall.

**Lapse — and the tax threshold that shapes it.** No German unit-linked *Stornoquote* was
established (gap 18 of the research file). What is structurally true is that unit-linked lapse is
**front-loaded**, because the acquisition charge is being taken and the value is furthest below
premiums paid, and that the exit is near-frictionless: § 168 VVG permits termination for the end
of the current *Versicherungsperiode* and § 169 pays the fund [R1] [R2] [REG-R28]. On top of that
sits the German tax threshold, which the reference library names as **the strongest single driver
of German surrender behaviour** [REG-R45]: under § 20 Abs. 1 Nr. 6 EStG only half the
*Unterschiedsbetrag* is taxable where the contract has run **at least twelve years** and payment
falls after completion of the **62nd** year of life, so surrenders are suppressed as the threshold
approaches and spike when both limbs are met [R20] [REG-R45].

| Policy year | 1–5 | 6–10 | 11 | 12 | 13+ |
|---|---|---|---|---|---|
| `lapse_rate_base` **[std]** | 6.0 % | 3.0 % | 2.0 % | 2.0 % | 3.0 % |

    lapse_tax_step(t)  = 2.5  in the twelve months of the policy year in which
                              BOTH duration 12 is complete AND attained age 62 is reached;
                              1.0 otherwise                                        [std]
    # the 12/62 threshold itself is statutory: EStG § 20 Abs. 1 Nr. 6 Satz 2 with
    # § 52 Abs. 28 (62 for contracts concluded after 31 December 2011; 60 before).
    # Its magnitude, 2.5, is [std].
    lapse_rate(t)      = min( lapse_cap, lapse_rate_base(t) × lapse_tax_step(t) + lapse_dyn_add(t) )
    lapse_rate_mth(t)  = 1 − (1 − lapse_rate(t))^(1/12)
    lapse_rate_mth(proj_len() − 1) = 0                                             [std]

with `lapse_cap = 40 %` **[std]**. The step year is `max(13, 62 − entry_age + 1)` in policy years
— on the anchor cell that is policy year **26**, `t = 300 … 311`, where the base 3.0 % becomes
7.5 % and the monthly rate 0.253505 % becomes 0.647574 %. **Keying the spike on duration alone is
wrong** and is a listed pitfall: the anchor cell passes duration 12 at age 48, fourteen years
before the tax benefit exists. On model point 12 the step never fires at all, because the
projection ends at `t = 143` and the step year begins at `t = 144`.

**In the final month the lapse rate is zero.** The end of month `proj_len() − 1` is
*Rentenbeginn*, so a surrender and an annuitisation are the same event releasing the same
*Fondsguthaben*; the whole surviving cohort is booked as `pols_maturity`. No cash flow moves
either way, but the convention decides the split between `Σ pols_lapse` and
`pols_maturity(proj_len() − 1)` and it is what the closure identity below reproduces. It is
frlib's convention on `TD_FR_S` and delib adopts it.

**Fund return.** No document in this corpus supplies one, and PRIIPs deliberately does not: its
scenarios are derived from the underlying's own return history under the RTS, not chosen by the
insurer [R8] [R9] [REG-R32]. `fund_scenario_table.csv` therefore carries **[std]** paths by
`(scenario_id, policy_year)`:

The table's `policy_year` key is the contractual 1-based label, reached through
`policy_year(t) = t // 12 + 1`, so it is unaffected by the 0-based frame.

| `scenario_id` | Gross return p.a. | TER p.a. | Purpose |
|---|---|---|---|
| `base` | 5.00 % level | 0.45 % | the base run **[std]** |
| `etf` | 5.00 % level | 0.15 % | the low-cost fund, for the *Nettotarif* cell |
| `zero` | 0.00 % level | 0.45 % | isolates the charge stack: every movement is a charge |
| `stress` | −20.00 % in year 1, then 5.00 % | 0.45 % | a fall that puts the fund far below premiums paid |

    fund_return_net_ann(t) = gross_return_ann(t) − ter_ann(t)                      [std]
    fund_return_net_mth(t) = (1 + fund_return_net_ann(t))^(1/12) − 1
    unit_price(t)          = unit_price_open(t) × (1 + fund_return_net_mth(t))
    unit_price_open(t)     = unit_price_init            at t = t₀
                           = unit_price(t − 1)          for t > t₀

On the base path that is 4.55 % p.a. net of fund costs and **0.371482 % per month**. **The TER is
netted off the return and is never a policy charge**: it lives inside the unit price and never
appears in the ledger, so charging it explicitly double-counts and ignoring it overstates the
policyholder's return. The **return** is compounded geometrically because it is an effective
annual rate; the **charges** are divided by twelve because a German tariff quotes a nominal
monthly rate — an asymmetry that is deliberate and is a listed pitfall. This is a scenario, not a
forecast, and **nothing in delib produces a distribution, so nothing in delib may be compared
with a PRIIPs performance scenario**.

**Expenses and commission (all levels [std]; no German commission scale was established).**

| Input | Value | Basis |
|---|---|---|
| Acquisition commission `comm_acq_rate` | **2.50 % of the *Beitragssumme***, paid at `t = 0` | **[std]** (5) |
| Issue expense `expense_issue` | 200.00 EUR at `t = 0` | **[std]** (5) |
| Maintenance expense `expense_maint_mth` | 4.00 EUR per policy per month, inflating at `expense_infl` | **[std]** (5) |
| Expense inflation `expense_infl` | 2.0 % p.a., applied as `1.02^(t/12)` | **[std]** |
| Renewal commission `comm_renew_rate` | 1.5 % of each gross premium | **[std]** (5) |
| Claim expense `expense_claim` | 150.00 EUR per death claim | **[std]** |
| Surrender expense `expense_surr` | 50.00 EUR per surrender | **[std]** |
| Annuitisation expense `expense_annuitisation` | 100.00 EUR per policy converting at *Rentenbeginn* | **[std]** |
| Dynamic-lapse coefficient `lapse_dyn_beta` | **0** in the base run; 0.15 as the reference value | **[std]** (6) |

5. **The acquisition commission is set equal to the acquisition charge deliberately.** The insurer
   pays 2.50 % of the *Beitragssumme* at inception and recovers exactly that, undiscounted, over
   the following sixty months — so the model demonstrates in one number the financing problem the
   *Höchstzillmersatz* and the five-year spread exist to regulate, and `t = 0` of the worked
   example is a large negative `net_cf`. No German commission scale was established, so any other
   level would be an unsourced number pretending to be an observation.
6. The dynamic module is off in the base run and is specified under *Policyholder behavior
   modeling* below.

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | **0-based** policy month index from inception, `t = 0` at inception; `t = t₀ … n − 1` |
| `t₀`, `n` | `proj_start()`, `proj_len()` | `duration_init_m`; `12 × (annuity_age − entry_age)`, the month **count** and so the frame's exclusive end |
| `y(t)`, `x(t)` | `policy_year(t)`, `age(t)` | `t // 12 + 1` (the contractual 1-based label); `entry_age + y(t) − 1` |
| `p(t)`, `p_open(t)` | `unit_price(t)`, `unit_price_open(t)` | *Anteilspreis* at the **end** and at the **start** of month `t`; `p_open(t₀) = unit_price_init`, `p_open(t) = p(t−1)` for `t > t₀` |
| `i(t)` | `fund_return_net_mth(t)` | monthly return net of the fund's TER |
| `u(t)` | `units_pp(t)` | units per policy at the **start** of month `t` |
| `F(t)`, `F_τ(t)` | `av_pp(t)`, `av_pp_at(t, τ)` | *Fondsguthaben* per policy, `F(t) = u(t)·p_open(t)` |
| `B(t)`, `Z(t)` | `prem_pp(t)`, `topup_pp(t)` | gross *Beitrag* due; *Zuzahlung* |
| `A(t)` | `prem_to_av_pp(t)` | *Anlagebeitrag* — what actually buys units |
| `α(t)` | `charge_acq_pp(t)` | acquisition instalment, plus *Zuzahlungskosten* on any `Z(t)` |
| `β`, `γₘ`, `SK` | `beta_rate`, `gamma_rate_mth`, `policy_fee_mth` | premium-based rate; `gamma_rate_ann/12`; *Stückkosten* |
| `S` | `beitragssumme()` | sum of premiums payable at the initial level |
| `C(t)` | `cum_prem_pp(t)` | cumulative **gross** premiums paid to and including month `t` |
| `D(t)`, `K(t)` | `db_floor_pp(t)`, `nar_pp(t)` | guaranteed minimum death benefit; *riskiertes Kapital* |
| `qᴵ(t)`, `q(t)` | `mort_rate_tariff_mth(t)`, `mort_rate_mth(t)` | first-order (the price) and second-order (the decrement) monthly death rates |
| `f` | `mort_be_factor` | 0.75; `q(t) = f · qᴵ(t)` |
| `w(t)` | `lapse_rate_mth(t)` | monthly lapse rate; `w(n − 1) = 0` |
| `l(t)` | `pols_if(t)` | policies in force at the **start** of month `t` |
| `W(t)` | `withdrawals_pp(t)` | *Teilentnahme* |
| `σ` | `stornoabzug_rate` | *Stornoabzug* rate on the *Fondsguthaben* |
| `R_g`, `R_c`, `R` | `rentenfaktor_guar()`, `rentenfaktor_curr()`, `rentenfaktor_applied()` | euro of monthly annuity per 10 000 € |

### The *Beitragsverrechnung*

    B(t) = prem_pp_base · d(t)   if t < 12·prem_term_y, (pup_month > 0 ⇒ t < pup_month), (t − t₀) mod prem_mode_months = 0
         = 0                     otherwise
    d(t) = (1 + dynamik_rate)^(y(t) − 1)                        Beitragsdynamik, 1.0 when off

    S    = prem_pp_base × (12 / prem_mode_months) × prem_term_y      laufend
         = prem_pp_base                                              einmal

    N_α  = min(60, 12 × prem_term_y) / prem_mode_months          acquisition instalments
    α(t) = alpha_rate · S / N_α        on the first N_α premium dates      laufend
         = zuzahlung_rate · B(t₀)      at t = t₀, once                     einmal
         + zuzahlung_rate · Z(t)       whenever a Zuzahlung falls

    A(t) = B(t) + Z(t) − α(t) − β · B(t)

`S` is the sum of premiums **payable**, at the **initial** level. It does not shrink when a
contract lapses or goes *beitragsfrei*, and it does not grow with a *Beitragsdynamik* increment,
because a real tariff re-zillmers each accepted increment over its own sixty months and an
increment cannot be assumed at inception [R12] [REG-R16]. The bias — the acquisition charge on a
dynamic contract is understated — is stated rather than hidden. `β` is charged on the regular
*Beitrag* only; a *Zuzahlung* pays its own charge and no second one.

`pup_month`, `topup_month` and `wd_month` carry **0 as the never / none sentinel** and not as
the inception month — `t = 0` is a legal index on the 0-based frame, so the guard has to be
written out, as it is in `B(t)` above and in `W(t)` below.

### The unit fund

    Δu(t) = A(t) / p_open(t)                                   units bought, at the opening price
    p(t)  = p_open(t) · (1 + i(t))
    F_BEF_CHARGE(t) = ( u(t) + Δu(t) ) · p(t)

    charge_admin_fund_pp(t) = γₘ · F_BEF_CHARGE(t)
    charge_policy_fee_pp(t) = min( SK, F_BEF_CHARGE(t) − charge_admin_fund_pp(t) )
    F_AFT_CHARGE(t) = F_BEF_CHARGE(t) − charge_admin_fund_pp(t) − charge_policy_fee_pp(t)

    W(t)  = min( wd_amount, F_AFT_CHARGE(t) )   if wd_month > 0 and t = wd_month, else 0
    F_AFT_WD(t) = F_AFT_CHARGE(t) − W(t)

    K(t)  = max( D(t) − F_AFT_WD(t), 0 )
    charge_risk_pp(t) = min( qᴵ(t) · K(t), F_AFT_WD(t) )
    F_BEF_DECR(t) = F_AFT_WD(t) − charge_risk_pp(t)

    u(t + 1) = F_BEF_DECR(t) / p(t)

The `min(·, remaining)` floors are **[std] safeguards**, not tariff terms: they keep the
*Fondsguthaben* non-negative on a contract whose fixed charges outrun a decayed fund. **None of
the thirteen shipped model points triggers one**, and a model point that did would in practice
have its cover terminated; the safeguard exists so that a user's own model point cannot produce a
negative fund silently.

The death-benefit floor is the model point's `db_form`:

    fund          D(t) = 0                                     → K(t) ≡ 0, no Risikobeitrag
    prem_return   D(t) = C(t)                                   Beitragsrückgewähr        [S2]
    pct_fund      D(t) = db_pct × F_AFT_WD(t)
    sum_assured   D(t) = sum_assured

`prem_return` is the composite. The net amount at risk is then `max(C(t) − F_AFT_WD(t), 0)`,
positive early and after a market fall and vanishing once the fund overtakes the premiums paid,
which is why **`cum_prem_pp` is a state variable of this product** and why the charge has to be
recomputed every month. It is the premiums **paid**, gross — not the premiums invested.

### Decrements and the in-force recursion

    pols_death(t)    = l(t) · q(t)
    pols_lapse(t)    = l(t) · (1 − q(t)) · w(t)
    pols_maturity(t) = l(t) · (1 − q(t))                 at t = n − 1, where w(n − 1) = 0
                     = 0                                 for t < n − 1
    l(t + 1) = l(t) · (1 − q(t)) · (1 − w(t)),   l(t₀) = pols_if_init(),   l(n) = 0

Deaths act before lapses **[std]**. `pols_if_at(t, ·)` exposes `"BEF_DECR"` (= `l(t)`),
`"AFT_DEATH"` and `"AFT_DECR"` (= `l(t+1)` before the maturity sweep), so the ordering is
inspectable rather than buried in one expression. **Closure identity**, which
`check_pols_roll_fwd()` asserts every month and a test asserts in total:

    Σ_{t=t₀..n−1} [ pols_death(t) + pols_lapse(t) + pols_maturity(t) ] = pols_if_init()

### Benefits, funding and the non-unit cash flow

    claims(t, "DEATH")    = pols_death(t)    · ( F_BEF_DECR(t) + K(t) )
    claims(t, "LAPSE")    = pols_lapse(t)    · F_BEF_DECR(t) · (1 − σ)
    claims(t, "MATURITY") = pols_maturity(t) · F_BEF_DECR(t)
    stornoabzug(t)        = pols_lapse(t)    · F_BEF_DECR(t) · σ
    withdrawals(t)        = l(t) · W(t)
    death_strain(t)       = pols_death(t) · K(t)
    av_releases(t)        = ( pols_death(t) + pols_lapse(t) + pols_maturity(t) ) · F_BEF_DECR(t)
                            + l(t) · W(t)

The death benefit is the floor **as observed before that month's *Risikobeitrag***, so the
insurer's non-unit cost per death is **exactly `K(t)`**. The *Rückkaufswert* is the
*Fondsguthaben* less a *Stornoabzug* if one is validly agreed [R1] [REG-R28]; with `σ = 0` on the
composite it is the *Fondsguthaben* exactly, and `claims_lapse` is then the whole release.

    premiums(t)  = ( B(t) + Z(t) ) · l(t)
    prem_to_av(t)= A(t) · l(t)
    charge_*(t)  = charge_*_pp(t) · l(t)                       for the four unit-side charges
    expenses(t)  = expense_issue · l(t) · 1{t = 0}
                   + expense_maint_pp(t) · l(t)
                   + expense_claim · pols_death(t)
                   + expense_surr  · pols_lapse(t)
                   + expense_annuitisation · pols_maturity(t)
    commissions(t) = comm_acq_rate · S · l(t) · 1{t = 0}
                   + comm_renew_rate · B(t) · l(t)

    net_cf(t) = charge_acq(t) + charge_admin_prem(t) + charge_admin_fund(t)
                + charge_policy_fee(t) + charge_risk(t) + stornoabzug(t)
                − expenses(t) − commissions(t) − death_strain(t)

    liability_cf(t) = − net_cf(t)

`net_cf` is **income-positive**, as it is in every model in this library. `expenses` and
`commissions` are two lines and not one, each subtracted once, which is what `expenses` means on
every delib model that has a commission to publish. The acquisition commission and the issue
expense fall at `t = 0`, the inception month, and **only** there, so an in-force model point
whose frame opens at `t = 96` never incurs either — which is correct, and which is the same
reason its `charge_acq(t)` is zero at every projected month.

**Three amounts that move on this contract are not insurer cash flow.** The *Anlagebeitrag* and
every account-value benefit are the policyholder's money passing through the unit fund; the fund's
**TER** never leaves the unit price and accrues to the fund manager; and any *Überschuss* credit
would be a policyholder credit, which this model does not project. Publishing `premiums`,
`prem_to_av`, `claims_*` and `av_releases` as columns while excluding them from `net_cf` makes
that exclusion visible rather than merely asserted.

### *Rentenbeginn*

    R_g = rentenfaktor_guar(annuity_age)      read at annuity_age, not at age(n − 1)
    R_c = rentenfaktor_curr(annuity_age)
    R   = max( R_g, R_c )
    av_maturity_pp() = F_BEF_DECR(n − 1)
    annuity_mth_pp() = av_maturity_pp() / 10 000 × R

The shipped `rentenfaktor_table.csv` is **[std] and derived, not observed**. The 0 %
*Rechnungszins* it rests on is no longer an inference from a classic tariff: a fondsgebundene AVB
states it — *"bei der Kalkulation der zu Vertragsbeginn garantierten Rentenfaktoren … einen
Zinssatz von 0,0 Prozent"*, on DAV 2004 R [S2] [S10] [R16] [REG-R49]. At 0 % a monthly annuity of
`R` per 10 000 € for an expected `T` years has present value `12·T·R`, so `R = 10 000 / (12·T)`;
the table sets

    T_eff(x) = 33.3333 − 0.75 · (x − 67),     ages 60–75,
    rentenfaktor_guar(x) = 10 000 / (12 · T_eff(x))

which gives exactly **25.00** at age 67, 22.47 at 62 and 26.81 at 70.

**Observed values are now available, and the table does not reproduce them.** At the same
*Rentenbeginn* age of 67 and the same 0 % rate, one carrier's guaranteed factors are **25,22 /
24,12 / 22,91 / 21,83 €** for deferments of 12 / 20 / 30 / 40 years [S15]. Two consequences:

- **Level.** At delib's anchor cell — a 37-year-old with a 30-year deferment — the observed
  factor is **22,91** against the table's **25.00**, so the shipped table is about **9 %
  generous** there. It is close at short deferments (25,22 at twelve years) and generous at long
  ones.
- **Shape.** The observed factor **falls with the deferment at a fixed *Rentenbeginn* age**, which
  is the generational DAV 2004 R showing through: a later birth cohort lives longer at 67. The
  shipped table is a function of `annuity_age` **alone** and is flat in the deferment, so it
  cannot reproduce that gradient at all — the entry-age-60 and long-deferment model points are
  priced on the same factor when a real tariff would separate them.

**Neither is changed here.** `rentenfaktor_table.csv` feeds `annuity_mth_pp()`, the worked example
and the golden tests, and moving it moves all three; that is a deliberate decision, not a
provenance fix. Read the other way, 25.00 at a 0 % *Rechnungszins* prices the guarantee as though
the insurer holds the capital for 33⅓ years and earns nothing on it; the market's own answer at
the anchor cell is 36⅜ years — the *Sicherheitsabschlag* made concrete, and slightly deeper in
reality than in the model [R16] [R22] [REG-R49]. `rentenfaktor_curr` equals `rentenfaktor_guar` on
`std_2026` and is 12 % higher on `rich_current`; consumer sources describe real guaranteed factors
at 50–70 % of the current one `[unverified]` [R22], so both settings are conservative.
**This model stops here**: the annuity is published, not projected.

### Reduction in yield

The product's defining metric, and the reason the library publishes it: on a contract with no
*Rechnungszins*, the charge stack **is** the economics. `reduction_in_yield()` is a scalar:

    gross_return_ref() = ( Π_{t=t₀..n−1} (1 + fund_return_gross_ann(t))^(1/12) )^(12 / (n − t₀)) − 1

    irr_ann() solves, by bisection on k:
       Σ_t (B(t) + Z(t)) · (1 + k)^((n − t)/12)
       − Σ_t W(t) · (1 + k)^((n − 1 − t)/12)
       + F(t₀) · (1 + k)^((n − t₀)/12)                    =  av_maturity_pp()

with both sums over `t = t₀ … n − 1`.  A premium falls at the **start** of its month and is
accumulated to the end of month `n − 1`, which is `n − t` months; a *Teilentnahme* falls at that
month's **end**, one month later, hence `n − 1 − t`.

    reduction_in_yield() = gross_return_ref() − irr_ann()

on a **single persisting contract** — no survivorship, no lapse — because a reduction in yield is
a statement about one policy's own money. The `F(t₀)` term is the *Fondsguthaben* the projection
opens with: it is zero on every new-business cell and matters only on the in-force one, where
without it the measure would credit the charge stack with money the projection never received as
premium. **It is a delib-defined measure and it is not the
statutory *Effektivkostenquote***: the German figure is aligned to the total-cost-indicator method
of Annex VI to Delegated Regulation (EU) 2017/653 over a specified recommended holding period,
and this model implements neither [R7] [REG-R31] [REG-R32]. Any level it produces is arithmetic on
delib's own [std] stack and **must never be quoted as a market figure** [R10] [R23] [R24].

### `result_cf()` and the published identities

`result_cf()` returns a DataFrame indexed by `t` (`index.name == "t"`), contiguous over
`range(proj_start(), proj_len())` — so `index[-1] == proj_len() − 1` — with these columns in this
order:

    pols_if, premiums, prem_to_av, charge_acq, charge_admin_prem, charge_admin_fund,
    charge_policy_fee, charge_risk, stornoabzug, withdrawals, claims_death, claims_lapse,
    claims_maturity, av_releases, death_strain, expenses, commissions, net_cf, liability_cf

`pols_if` is first and `pols_if(proj_start()) == pols_if_init()` exactly. Every flow on row `t` is
weighted by that row's `pols_if`, so dividing a flow by it recovers the per-policy amount; the
end-of-month count is `pols_if_at(t, "AFT_DECR")`, and the closing fund of the surviving cohort is
`av_pp(t+1) × pols_if(t+1)`, not `av_at(t, ·)`.

Seven `check_*()` cells are published, each a `bool` over all `t` with a per-`t`
`check_*_resid(t)` companion:

| Check | Identity |
|---|---|
| `check_net_cf()` | **delib ruling 1.** `net_cf = charge_acq + charge_admin_prem + charge_admin_fund + charge_policy_fee + charge_risk + stornoabzug − expenses − commissions − death_strain` |
| `check_prem_split()` | `premiums = prem_to_av + charge_acq + charge_admin_prem` — the *Beitragsverrechnung* closes |
| `check_units_roll_fwd()` | `units_pp(t+1) = units_pp(t) + units_bought_pp(t) − units_cancelled_pp(t)` — no price term |
| `check_av_roll_fwd()` | `F_BEF_DECR(t) = (F(t) + A(t))·(1 + i(t)) − charges − W(t)` — the price term, once |
| `check_benefit_funding()` | `claims_death + claims_lapse + claims_maturity + withdrawals + stornoabzug = av_releases + death_strain` |
| `check_pols_roll_fwd()` | `pols_if(t) = pols_death + pols_lapse + pols_maturity + pols_if(t+1)` |
| `check_acq_charge()` | `cum_charge_acq_pp(t)` equals the instalments elapsed × the instalment, and the total equals `alpha_rate × beitragssumme()` exactly |

`check_units_roll_fwd()` and `check_av_roll_fwd()` look redundant and are not: the unit identity
has **no price term at all**, so it fails if a charge is taken in euro without cancelling the
matching units, while the account identity carries the return and fails if the price is applied
at the wrong point in the month. An implementation can pass either alone.

### Monthly processing order

For `t = t₀ … n − 1`, in this order:

1. Advance `y(t)`, `x(t)`; read the charge row, the scenario row, `qᴵ(t)`, `q(t)` and `w(t)`.
2. Open the month: `u(t)` units, `F(t) = u(t)·p_open(t)`.
3. **Premium in advance.** `B(t)` if a premium is due (not after `prem_term_y`, not from
   `pup_month`), plus any `Z(t)`. Update `C(t) = C(t−1) + B(t) + Z(t)`, seeded inside the
   frame's own first month as `C(t₀) = cum_prem_init + B(t₀) + Z(t₀)` — there is no `t₀ − 1`
   to read on a new-business cell, where `t₀ = 0`. `cum_charge_acq_pp` is seeded the same way.
4. **Withhold**, in order: the acquisition instalment `α(t)`, then `β·B(t)`. The remainder is
   `A(t)`.
5. **Buy units** at the opening price: `Δu(t) = A(t)/p_open(t)`.
6. **Investment return.** `p(t) = p_open(t)·(1 + i(t))`; unit count unchanged; strike
   `F_BEF_CHARGE(t)`.
7. **Cancel units for the fund-based admin charge** `γₘ · F_BEF_CHARGE(t)`.
8. **Cancel units for the *Stückkosten*** `SK`, floored at the remaining balance.
9. **Settle any *Teilentnahme*** `W(t)`, floored at the remaining balance.
10. **Observe** `D(t)` and `K(t) = max(D(t) − F_AFT_WD(t), 0)`.
11. **Cancel units for the *Risikobeitrag*** `qᴵ(t)·K(t)`, floored at the remaining balance.
12. **Decrements at the end of the month**, deaths before lapses; at `t = n − 1`,
    `w(n − 1) = 0` and the survivors are booked as `pols_maturity(n − 1)`.
13. **Book the benefits** at `F_BEF_DECR(t)` plus `K(t)` on a death, less `σ` on a lapse.
14. **Roll forward** `u(t+1)` and `l(t+1)`.
15. **Extract the non-unit row** and accumulate `net_cf(t)`.

At `t = n − 1` the units are cancelled, `av_maturity_pp()` is struck and `annuity_mth_pp()` is
published. There is no `t = n` row.

---

## Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each
one becomes a test.

1. **Netting the fund-based charge out of the premium instead of cancelling units.** A model that
   deducts `γ` from the *Beitrag* gives the right answer while premiums are paid and the wrong
   answer the moment they stop. Assert that on model point 7 `charge_admin_fund(t) > 0` and
   `charge_policy_fee(t) > 0` at every `t ≥ 120`, where `premiums(t) = 0`.
2. **Charging the fund's TER as a policy charge.** It is inside the unit price [R7] [REG-R32]:
   charging it explicitly double-counts, ignoring it overstates the return. Assert
   `unit_price(t)/unit_price_open(t) = (1 + gross − ter)^(1/12)` exactly on `base`, and that no
   `charge_*` column contains a TER term.
3. **Pricing the *Risikobeitrag* on the annuity table.** The death charge is priced on a **death**
   table, DAV 2008 T [R17] [REG-R48]; the conversion guarantee rests on DAV 2004 R [R16]
   [REG-R49]. Assert that `mort_rate_tariff_at_age` reads `mort_table.csv` and
   `rentenfaktor_guar` reads `rentenfaktor_table.csv`, and that no cells reads both.
4. **Using one mortality basis for the charge and for the decrement.** That makes the
   *Risikoergebnis* identically zero and deletes the mechanic. Assert
   `Σ charge_risk − Σ death_strain = (1 − mort_be_factor) · Σ charge_risk` **exactly**, and that
   it is strictly positive on the anchor.
5. **Mixing the monthly conversions.** `qᴵ` and `q` must use the same split, or the model
   manufactures a risk result out of a rounding convention: at `q = 0.00080`, `q/12 = 0.00006667`
   against `1 − (1−q)^(1/12) = 0.00006669`, a 0.04 % difference that lands entirely in the risk
   result and grows with `q`. Assert `mort_rate_mth(t) = mort_rate(t)/12` and
   `lapse_rate_mth(t) = 1 − (1 − lapse_rate(t))^(1/12)`, and that `lapse_rate_mth < lapse_rate`
   wherever the annual rate is positive.
6. **Forgetting to floor the net amount at risk at zero.** `max(D − F, 0)`, not `D − F`. Without
   the floor the contract pays the insurer a negative charge in every month the fund is above the
   floor, and the death strain turns negative — the model silently books the fund's growth as
   insurance profit. Assert `nar_pp(t) ≥ 0` at every `t`, and that on model points 2 and 13
   (`db_form = fund`) `charge_risk(t) = 0.00` at every `t`.
7. **Running the acquisition instalment past its window, or spreading it over sixty months when
   the premium term is shorter.** Assert that the **instalment** is zero for `t ≥ 60` on every
   model point, and that on model point 12 the instalment count is **24**, not 60. Two
   exceptions have to be stated rather than asserted away, and both follow from the `α(t)`
   definition above: `charge_acq(120)` is non-zero on model point 9, where the *Zuzahlung*
   pays 2.50 % *Zuzahlungskosten* — 500.00 per policy — which this model books in
   `charge_acq`; and `Σ charge_acq_pp = alpha_rate × beitragssumme()` holds on eleven points
   but not on point 6, where the in-force frame opens past the window (0.00 against 2,775.00,
   which is pitfall 8), nor on point 9, where the *Zuzahlungskosten* make it 3,380.00 against
   2,880.00.
8. **Charging an in-force model point again for acquisition.** Model point 6 opens at `t = 96`.
   Assert `charge_acq(t) = 0` at every projected `t` **and** that `commissions(96)` contains no
   *Abschlussprovision* and `expenses(96)` no issue expense — the whole of the difference
   between it and a new-business cell.
9. **Letting the *Beitragssumme* follow the premiums actually paid.** `S` is the sum of premiums
   **payable**, at the **initial** level; it does not shrink on lapse or *Beitragsfreistellung*
   and does not grow with a *Beitragsdynamik* increment [R12] [REG-R16]. Assert `beitragssumme()`
   is invariant to `pup_month`, to `lapse_rate` and to `dynamik_rate`.
10. **Conflating *Storno* with *Beitragsfreistellung*.** They are two different things: one is an
    exit paying the *Rückkaufswert*, the other a change of state paying nothing [R2] [R3]
    [REG-R28]. Assert that on model point 7 `pols_if` is continuous across `t = 120` while
    `premiums` steps to zero and the unit-side charges continue.
11. **Inventing a *Rückkaufswert* formula.** The *Zeitwert* of a pure unit-linked contract **is**
    the *Fondsguthaben*: no discounting, no *Rechnungszins*, no mortality basis, no *Zillmerung*
    residue, no second-basis *Mindestrückkaufswert* [R1] [REG-R28]. Assert
    `claims_lapse(t) = pols_lapse(t) × av_pp_at(t, "BEF_DECR")` exactly wherever `σ = 0`.
12. **Building the *Stornoabzug* out of unamortised acquisition costs.** § 169 Abs. 5 VVG makes
    exactly that deduction ineffective and puts the burden of proof on the insurer [R1] [REG-R28]
    [REG-R36]. Assert `stornoabzug(t) = σ × pols_lapse(t) × av_pp_at(t, "BEF_DECR")` and that it
    is **not** a function of `charge_acq_total() − cum_charge_acq_pp(t)`.
13. **Booking the whole *Fondsguthaben* as an insurer outgo.** `net_cf` is the non-unit stream;
    the fund is the policyholder's money passing through. Assert `check_benefit_funding()` and
    `check_net_cf()`, and that no account-value benefit appears inside `net_cf`.
14. **Getting the age at *Rentenbeginn* off by one.** `age(proj_len() − 1) = annuity_age − 1`,
    because the annuity begins at the **end** of that month. Assert exactly that, and that
    `rentenfaktor_guar()` is read at `annuity_age`: on the anchor 25.00 at 67, not 24.45 at 66.
15. **Applying only the guaranteed *Rentenfaktor*.** The rule is `max(guaranteed, current)`
    [S4] [R22]. Assert equality on the anchor and, on model point 13,
    `rentenfaktor_applied() = rentenfaktor_curr() = 1.12 × rentenfaktor_guar()`.
16. **Re-applying a *Ratenzahlungszuschlag*.** `prem_pp` is the instalment the policy states and
    already contains whatever loading the tariff applied. Assert `premiums(t) = prem_pp ×
    pols_if(t)` exactly in a premium month on model points 3, 4 and 5, and `0.00` in the
    intervening months.
17. **Letting the *Beitragsrückgewähr* base be the premiums invested rather than the premiums
    paid.** Assert `cum_prem_pp(59) = 12,000.00` on the anchor — 60 × 200.00 — against
    `Σ_{t<60} prem_to_av_pp(t)`, which is 9,720.00, a 19 % understatement of the death benefit.
18. **Letting a fixed charge drive the fund negative.** The *Stückkosten* and the *Risikobeitrag*
    are floored at the remaining balance **[std]**. Assert `av_pp_at(t, τ) ≥ 0` at every `t` and
    every timing on every model point, and that no shipped point actually triggers a floor.

---

## Policyholder behavior modeling

All formulas are **[std]** reference constructions. There is no German calibration evidence for
any of them, and the research file's gaps register records that as gaps 18 and 19.

- **Base lapse [std].** The duration table above: 6 % p.a. in years 1–5, 3 % thereafter, dipping
  to 2 % in years 11–12. The front-loading is a structural inference from the exit terms — the
  acquisition charge is being taken, the value is furthest below premiums paid, and § 168 VVG
  makes the exit near-frictionless [R1] [R2] [REG-R28] — not an observation.
- **The tax-threshold step [std].** A ×2.5 multiplier for twelve months from the later of duration
  12 and attained age 62 [R20] [REG-R45]. This is the one behavioural feature the cross-product
  reference library actively requires of every German Schicht-3 model, and the reason is that a
  lapse assumption flat in duration ignores the strongest single driver of German surrender
  behaviour. Keying it on duration alone is pitfall 5's twin: on the anchor cell duration 12
  arrives fourteen years before the tax benefit does.
- **Dynamic lapse [std], off in the base run.** Unit-linked lapse is market-sensitive, because
  the exit is at fund value on short notice. The reference module raises the rate when the
  contract is under water against the premiums paid:

      lapse_dyn_add(t) = lapse_dyn_beta × max( 0, 1 − av_pp(t) / cum_prem_pp(t) )

  with `lapse_dyn_beta = 0` in the base run and **0.15** as the reference value. Switched on, it
  bites hardest on model point 12, whose stress path leaves the fund far below premiums paid for
  years, and it introduces a feedback the deterministic run only samples once: a falling fund
  raises lapse, which removes the policies whose charges would have recovered the acquisition
  cost.
- ***Beitragsfreistellung* is a model-point election, not a cohort decrement, and that is a
  deliberate limitation.** A paid-up policy's fund and its *Beitragsrückgewähr* base both depend
  on the month it went paid-up, so a cohort-level paid-up rate would need one sub-cohort per
  month — a two-dimensional recursion over 360 months for a second-order effect. The model
  therefore carries `pup_month` on the model point and reproduces the mechanic exactly on one
  cell (point 7) rather than approximately on all of them. A **[std]** paid-up rate of **1 % p.a.**
  is what a cohort implementation would use; it is recorded and **not implemented**, and omitting
  it biases the projected charge income **upward**, because a paid-up contract stops paying the
  premium-based charges.
- **What the model deliberately does not do.** No *Kapitalwahlrecht* take-up rate: the base run
  annuitises, which is a modelling choice made so that the *Rentenfaktor* is the thing the worked
  example demonstrates, and **not** an estimate of behaviour — no take-up rate was established
  anywhere [R20]. No *Abrufphase*: the *Rentenbeginn* is fixed, and whether deferral restates the
  guaranteed factor was not established. No *Widerruf* decrement: the 30-day window sits inside
  the year-1 lapse rate [R6] [REG-R23]. No *Fondswechsel* behaviour beyond the
  *Ablaufmanagement* glide.

---

## Worked example

**Configuration.** Model point 1, the anchor cell of `model_point_table.csv`:
`policy_id = DE-FRV-0001`; `sex = M` (reporting only — the tariff is unisex [REG-R34]);
`entry_age = 37`; `duration_init_m = 0`, so `proj_start() = 0`; `pols_if_init = 1.0`;
`annuity_age = 67`, so `proj_len() = 12 × (67 − 37) = 360` months and the frame is
`t = 0 … 359`;
`prem_form = laufend`; `prem_pp = 200.00 EUR`; `prem_mode_months = 1`; `prem_term_y = 30`;
`dynamik_rate = 0.00`; `pup_month = 0`; `db_form = prem_return`, so `db_pct` and `sum_assured` are
unused; `charge_id = std_gross`; `scenario_id = base`; `rentenfaktor_id = std_2026`;
`unit_price_init = 100.00 EUR`; `units_init = 0.0`; `cum_prem_init = 0.00 EUR`;
`topup_month = 0`, `topup_amount = 0.00`; `wd_month = 0`, `wd_amount = 0.00`;
`ablauf_flag = False`; `kapitalwahl = False`. Hence `beitragssumme() = 200.00 × 12 × 30 =
72 000,00 €`, the acquisition charge at the cap is `0.025 × 72 000 = 1 800,00 €`, and the
instalment is `1 800,00 / 60 = 30,00 € per month` — **15 % of each of the first 60 premiums,
`t = 0 … 59`, and nothing from `t = 60`**.

**Assumptions, each tagged.** *Charges*, from row `std_gross` of `charge_table.csv`, every level
**[std]** except where noted: acquisition rate `alpha_rate = 2.50 %` of the *Beitragssumme*, which
is the *Höchstzillmersatz* [R12] [REG-R16] and, as it happens, the rate one real tariff charges
[S15], spread over `alpha_spread_months = 60` — the statutory five-year shape of § 169 Abs. 3 VVG
[R1] [REG-R28], which a real tariff applies to only *part* of its acquisition cost, taking the
rest as a percentage of every premium for the whole term [S2]; premium-based admin
`beta_rate = 4.00 %` of each gross *Beitrag*, against 6,90 % observed [S15]; fund-based admin
`gamma_rate_ann = 0.30 % p.a.`, taken monthly as `gamma_rate_mth = 0.30 %/12 = 0.025 %` of the
*Fondsguthaben*; *Stückkosten* `policy_fee_mth = 3.00 €` per month, taken by cancelling units;
*Zuzahlungskosten* `zuzahlung_charge_rate = 2.50 %` (not exercised on this cell);
*Stornoabzug* `stornoabzug_rate = 0.00 %` [R1] [REG-R28]. *Fund*, from row `base` of
`fund_scenario_table.csv`: gross return `5.00 % p.a.` **[std]**, fund `TER = 0.45 % p.a.`
**[std]**, so `fund_return_net_ann = 4.55 % p.a.` and `fund_return_net_mth = (1.0455)^(1/12) − 1
= 0.371482 % per month`; *Kickback* credited back `0.00 %` **[std]**; no *Ablaufmanagement* glide.
*Mortality*: the tariff basis is a **[std]** first-order death proxy `mort_rate_tariff_at_age(x) =
0.00080 × 1.10^(x − 37)`, anchored at `q(37) = 0.00080`. It stands for whichever first-order death
table a carrier uses — DAV 2008 T is the modern one [R17] [REG-R48]; the one fondsgebundene tariff
whose bases could be read prices its *Risikobeiträge* on 65 % of DAV 1994 T [S2] — so
`mort_rate_tariff(0) = 0.00080` and `mort_rate_tariff_mth(0) = 0.00080/12 = 0.00006667`; the
best-estimate decrement is `mort_be_factor = 0.75` **[std]** times it, so `mort_rate(0) = 0.00060`
and `mort_rate_mth(0) = 0.00005`. *Lapse*, all **[std]**: `lapse_rate_base` 6.0 % p.a. in policy
years 1–5, 3.0 % in 6–10, 2.0 % in 11–12 and 3.0 % from 13, converted as
`lapse_rate_mth = 1 − (1 − lapse_rate)^(1/12)` — 0.514301 % monthly at 6 % and 0.253505 % at 3 %;
the tax step `lapse_tax_step = 2.5` applies in policy year 26 (`t = 300 … 311`), the year in which
attained age 62 is reached and duration 12 is long past [R20] [REG-R45], giving 7.5 % p.a. and
0.647574 % monthly there; `lapse_cap = 40 %`; `lapse_dyn_beta = 0` (module off);
`lapse_rate_mth(359) = 0`, because the end of month `t = 359` is *Rentenbeginn*. *Expenses*, all
**[std]**: acquisition commission `comm_acq_rate = 2.50 %` of the *Beitragssumme* = 1 800,00 €
plus `expense_issue = 200,00 €`, both at `t = 0`; maintenance `expense_maint_mth = 4,00 €` per
month inflating at `expense_infl = 2.0 % p.a.` as `4.00 × 1.02^(t/12)`; renewal commission
`comm_renew_rate = 1.5 %` of each gross premium; `expense_claim = 150,00 €` per death;
`expense_surr = 50,00 €` per surrender; `expense_annuitisation = 100,00 €` at *Rentenbeginn*.
*Conversion*: `rentenfaktor_guar(67) = 25.00` and `rentenfaktor_curr(67) = 25.00` from row
`std_2026`, both **[std]** and derived from `T_eff(67) = 33.3333` at a 0 % *Rechnungszins*
[S10] [R16] [R22] [REG-R49], so `rentenfaktor_applied() = 25.00`. No *Überschussbeteiligung*, no
*Zuzahlung*, no *Teilentnahme*, no *Beitragsdynamik*, no behaviour modules.

360 months is far too long to print in full, so the table below shows a representative set
of months — the first six, `t = 0 … 5`, which are the *Beitragsverrechnung* in detail;
`t = 11`, `23` and `58–60`, which straddle the acquisition-charge cliff; `t = 119` and `239`;
`t = 299–300`, which straddle the tax-threshold lapse step; and `t = 358–359`, the last two —
together with the full-precision totals over all 360 months. Totals are summed at full precision and then rounded, not summed from
the rounded cells. Money is shown to the cent, `pols_if` and unit counts to six decimals.

### The table

Three panels of the same projection. **Every figure is the model's own output**, rounded
for printing only; the `Total` row is the sum over all 360 months **at full precision, then
rounded**. Panel A carries the full month list; Panels B and C carry a subset of it, the
intermediate months adding nothing to either.

**Panel A — the non-unit ledger.** `stornoabzug` and `withdrawals` are 0.00 in every month
of this cell — the composite tariff has no *Stornoabzug* and this model point takes no
*Teilentnahme* — and are omitted here, though still published as columns, because a zero
column states a product fact where a missing one would hide it.

| t | pols_if | premiums | prem_to_av | charge_acq | charge_admin_prem | charge_admin_fund | charge_policy_fee | charge_risk | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 200.00 | 162.00 | 30.00 | 8.00 | 0.04 | 3.00 | 0.00 | 204.26 | 1,803.00 | -1,966.22 |
| 1 | 0.994807 | 198.96 | 161.16 | 29.84 | 7.96 | 0.08 | 2.98 | 0.01 | 4.25 | 2.98 | 33.64 |
| 2 | 0.989641 | 197.93 | 160.32 | 29.69 | 7.92 | 0.12 | 2.97 | 0.01 | 4.23 | 2.97 | 33.49 |
| 3 | 0.984502 | 196.90 | 159.49 | 29.54 | 7.88 | 0.16 | 2.95 | 0.01 | 4.22 | 2.95 | 33.35 |
| 4 | 0.979390 | 195.88 | 158.66 | 29.38 | 7.84 | 0.20 | 2.94 | 0.01 | 4.20 | 2.94 | 33.21 |
| 5 | 0.974304 | 194.86 | 157.84 | 29.23 | 7.79 | 0.24 | 2.92 | 0.02 | 4.19 | 2.92 | 33.08 |
| 11 | 0.944340 | 188.87 | 152.98 | 28.33 | 7.55 | 0.46 | 2.83 | 0.03 | 4.10 | 2.83 | 32.26 |
| 23 | 0.887098 | 177.42 | 143.71 | 26.61 | 7.10 | 0.88 | 2.66 | 0.05 | 3.92 | 2.66 | 30.69 |
| 58 | 0.738908 | 147.78 | 119.70 | 22.17 | 5.91 | 1.93 | 2.22 | 0.10 | 3.45 | 2.22 | 26.58 |
| 59 | 0.735054 | 147.01 | 119.08 | 22.05 | 5.88 | 1.95 | 2.21 | 0.10 | 3.44 | 2.21 | 26.47 |
| 60 | 0.731221 | 146.24 | 140.39 | 0.00 | 5.85 | 1.98 | 2.19 | 0.11 | 3.33 | 2.19 | 4.53 |
| 119 | 0.625891 | 125.18 | 120.17 | 0.00 | 5.01 | 4.02 | 1.88 | 0.00 | 3.14 | 1.88 | 5.89 |
| 239 | 0.459656 | 91.93 | 88.25 | 0.00 | 3.68 | 7.71 | 1.38 | 0.00 | 2.81 | 1.38 | 8.58 |
| 299 | 0.385184 | 77.04 | 73.96 | 0.00 | 3.08 | 9.16 | 1.16 | 0.00 | 2.60 | 1.16 | 9.64 |
| 300 | 0.384018 | 76.80 | 73.73 | 0.00 | 3.07 | 9.19 | 1.15 | 0.00 | 2.68 | 1.15 | 9.58 |
| 358 | 0.304251 | 60.85 | 58.42 | 0.00 | 2.43 | 9.82 | 0.91 | 0.00 | 2.27 | 0.91 | 9.98 |
| 359 | 0.303239 | 60.65 | 58.22 | 0.00 | 2.43 | 9.84 | 0.91 | 0.00 | 32.53 | 0.91 | -20.27 |
| **Total** | **202.931416** | **40,586.28** | **37,413.08** | **1,549.75** | **1,623.45** | **2,033.18** | **608.79** | **5.85** | **1,319.97** | **2,408.79** | **2,087.87** |

**Panel B — the benefits, and what funds them.** All of these are paid by cancelling the
policyholder's own units, so none enters `net_cf`; only `death_strain` — the *riskiertes
Kapital* the insurer funds — crosses the unit / non-unit boundary. `liability_cf` is
`net_cf` outgo-positive.

| t | claims_death | claims_lapse | claims_maturity | av_releases | death_strain | liability_cf |
|---|---|---|---|---|---|---|
| 0 | 0.01 | 0.82 | 0.00 | 0.83 | 0.00 | 1,966.22 |
| 1 | 0.02 | 1.64 | 0.00 | 1.65 | 0.00 | -33.64 |
| 5 | 0.06 | 4.84 | 0.00 | 4.89 | 0.01 | -33.08 |
| 11 | 0.11 | 9.48 | 0.00 | 9.57 | 0.02 | -32.26 |
| 23 | 0.23 | 18.18 | 0.00 | 18.38 | 0.04 | -30.69 |
| 59 | 0.65 | 40.13 | 0.00 | 40.70 | 0.07 | -26.47 |
| 60 | 0.72 | 20.10 | 0.00 | 20.73 | 0.08 | -4.53 |
| 119 | 1.90 | 40.75 | 0.00 | 42.64 | 0.00 | -5.89 |
| 239 | 9.43 | 78.11 | 0.00 | 87.54 | 0.00 | -8.58 |
| 300 | 19.90 | 237.76 | 0.00 | 257.66 | 0.00 | -9.58 |
| 358 | 31.15 | 99.47 | 0.00 | 130.61 | 0.00 | -9.98 |
| 359 | 31.19 | 0.00 | 39,298.91 | 39,330.11 | 0.00 | 20.27 |
| **Total** | **3,047.80** | **22,522.64** | **39,298.91** | **64,864.97** | **4.39** | **-2,087.87** |

**Panel C — the *Fondsguthaben*, per policy.** The unit side, which Panel A weights by
`pols_if`. `av_pp_at(t, "AFT_WD")` equals `av_pp_at(t, "AFT_CHARGE")` throughout, there
being no *Teilentnahme*, and is omitted. `t = 93` and `94` are added to the list because
they straddle the month the fund overtakes the premiums paid and the *Risikobeitrag* falls
to zero for the rest of the contract. Balances have no total, being balances.

| t | unit_price | units_pp | av_pp | av BEF_CHARGE | av AFT_CHARGE | av BEF_DECR | cum_prem_pp | nar_pp | lapse_rate_mth | mort_rate_mth |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 100.371482 | 0.000000 | 0.00 | 162.60 | 159.56 | 159.56 | 200.00 | 40.44 | 0.00514301 | 0.00005000 |
| 1 | 100.744344 | 1.589679 | 159.56 | 322.75 | 319.67 | 319.67 | 400.00 | 80.33 | 0.00514301 | 0.00005000 |
| 5 | 102.249694 | 7.885561 | 803.31 | 968.90 | 965.66 | 965.64 | 1,200.00 | 234.34 | 0.00514301 | 0.00005000 |
| 59 | 124.916609 | 83.728674 | 10,420.39 | 10,621.70 | 10,616.05 | 10,615.91 | 12,000.00 | 1,383.95 | 0.00514301 | 0.00007321 |
| 60 | 125.380652 | 84.984001 | 10,615.91 | 10,848.06 | 10,842.35 | 10,842.20 | 12,200.00 | 1,357.65 | 0.00253505 | 0.00008053 |
| 93 | 141.700579 | 131.144920 | 18,514.53 | 18,776.02 | 18,768.33 | 18,768.33 | 18,800.00 | 31.67 | 0.00253505 | 0.00009744 |
| 94 | 142.226971 | 132.450597 | 18,768.33 | 19,030.76 | 19,023.00 | 19,023.00 | 19,000.00 | 0.00 | 0.00253505 | 0.00009744 |
| 239 | 243.489783 | 274.678167 | 66,633.79 | 67,074.04 | 67,054.27 | 67,054.27 | 48,000.00 | 0.00 | 0.00253505 | 0.00030580 |
| 358 | 378.539129 | 340.534729 | 128,428.63 | 129,098.43 | 129,063.16 | 129,063.16 | 71,800.00 | 0.00 | 0.00253505 | 0.00079315 |
| 359 | 379.945333 | 340.950641 | 129,063.16 | 129,735.32 | 129,699.88 | 129,699.88 | 72,000.00 | 0.00 | 0.00000000 | 0.00079315 |

**Where the totals differ from summing the rounded cells.** Rounding each of the 360 cells
to the cent and then adding changes fourteen of the nineteen column totals, by one to twelve
cents: `av_releases` 64,864.85 against 64,864.97, `charge_admin_prem` 1,623.35 against
1,623.45, `death_strain` 4.33 against 4.39, `net_cf` 2,087.84 against 2,087.87, `pols_if`
202.931410 against 202.931416. The gap is worst where the cells are smallest — `death_strain`
is a hundredth of a cent a month for most of the projection and rounds to zero 360 times —
which is why the rule is to sum first and round afterwards.

### Independent checks

Three rebuilds of cells in the table **a different way**, from the parameters rather than
from the recursion, and then the identities that close.

**1. The inception month `t = 0`, from the tariff alone.** *Beitragssumme* 200.00 x 12 x 30 = 72,000.00;
acquisition charge 2.50 % of it = 1,800.00; over 60 instalments = **30.00 a month**, which
is 15 % of each premium. Premium admin 4.00 % x 200.00 = **8.00**. The *Anlagebeitrag* is
200.00 - 30.00 - 8.00 = **162.00** and at the opening *Anteilspreis* of 100.00 buys
**1.620000 units**. The month's return is (1.0455)^(1/12) - 1 = 0.0037148195588312, so the
price closes at 100.371481956 and the fund at 1.62 x 100.371481956 = **162.601800769**.
*Gammakosten* 0.0030/12 x 162.601800769 = **0.040650450**; *Stückkosten* **3.000000000**;
fund **159.561150318**. The *Beitragsrückgewähr* floor is the premium paid, 200.00, so the
*riskiertes Kapital* is **40.438849682** and the *Risikobeitrag* 0.00080/12 x 40.438849682 =
**0.002695923**. The month closes at **159.558454395** — Panel C's `av BEF_DECR` at t = 0,
159.56 — and 159.558454395 / 100.371481956 = **1.589679 units**, Panel C's `units_pp` at
t = 1. Nine decimals are carried here because six do not close the chain: the *Gammakosten*
at 0.040650 would leave 159.561151.

**2. `t = 60` — the cliff, and the risk charge at a second age.** The acquisition instalment
has stopped, so the *Anlagebeitrag* is 200.00 - 8.00 = **192.00**, up from 162.00, and
`charge_acq` is 0.00. Opening fund 10,615.913263 plus 192.00, times 1.0037148195588312, is
**10,848.062710117**; less 0.00025 x that = 2.712015678 and 3.00 gives **10,842.350694440**.
The attained age is 37 + 5 = **42**, so the tariff rate is 0.00080 x 1.10^5 =
**0.001288408** and its twelfth 0.000107367333. Premiums paid are 61 x 200.00 = 12,200.00,
so the *riskiertes Kapital* is **1,357.649305560** and the *Risikobeitrag* **0.145767186**;
weighted by `pols_if(60) = 0.73122052` that is **0.10658796**, Panel A's 0.11. The same row
carries a second step: `claims_lapse` halves from 40.13 to 20.10, because `t = 60` opens
policy year 6 and the lapse rate drops from 6.0 % to 3.0 %, the monthly rate from
0.514301 % to 0.253505 %.

**3. The reduction in yield, as a savings account.** Accumulate 200.00 a month for 360
months at the model's own IRR of **3.6592629 % p.a.**, monthly factor
(1.036592629)^(1/12) - 1, and the balance at the end of `t = 359` is **129,699.8842** — `av_maturity_pp()`
to the cent. Do it at the scenario's **gross** 5.00 % and the balance is **163,739.57**. The
**34,039.69** between them is what the charge stack and the fund's own TER cost this
policyholder over thirty years, and 5.0000 % - 3.6593 % = **1.3407 % per annum** is that cost
as a yield. It is a delib measure on delib's own **[std]** stack and **is not** the statutory
*Effektivkostenquote*.

**The identities that close.** Four, each exact:

    decrements     deaths 0.04377181 + lapses 0.65322937 + maturity 0.30299882 = 1.00000000
    risk result    charge_risk 5.849973 - death_strain 4.387480 = 1.462493 = 0.25 x 5.849973
    acquisition    60 x 30.00 = 1,800.00 = 2.50 % x 72,000.00 = cum_charge_acq_pp(359)
    net_cf         charges 5,821.018511 - expenses 1,319.970596
                   - commissions 2,408.794247 - strain 4.387480    = 2,087.866187
    benefit funding  3,047.802205 + 22,522.641344 + 39,298.911744 = 64,869.355293
                     av_releases 64,864.967813 + strain 4.387480 = 64,869.355293

The decrement line is the closure the `lapse_rate_mth(359) = 0` convention produces: the last
month's survivors are `pols_maturity`, not lapses, and no cash flow depends on which. The
risk-result line is a quarter of the charge exactly, and only because `mort_be_factor` is
flat; a model decrementing on the tariff basis would print zero there and look healthy doing
it. The acquisition line closes on the *Höchstzillmersatz*, and the `charge_acq` **column**
totals 1,549.75 rather than 1,800.00 because it is weighted by `pols_if` — the sixty
instalments are collected on an average of 0.860971 of a policy, so roughly one in seven of
them is never collected at all, which is the insurer's acquisition-cost problem in one number:
it pays 1,800.00 at inception and collects 1,549.75. The shortfall is an average over the
sixty months and not the attrition at the end of them: by `t = 59` `pols_if` is 0.735054, so
about one policy in four has already gone. The last line is the one that matters most:
**64,869.36 of benefits against 40,586.28 of premiums, and only 4.39 of it an insurer cost** —
the rest is the policyholder's own units coming back.

**The annuity the contract exists for.** The *Fondsguthaben* at *Rentenbeginn* is
**129,699.88 EUR**. The *Rentenfaktor* is read at `annuity_age = 67`, not at `age(359) = 66`;
guaranteed and current are both 25.00, so `rentenfaktor_applied() = 25.00` and the monthly
annuity is 129,699.88 / 10,000 x 25.00 = **324.25 EUR**. The off-by-one would fetch 24.45 and
understate the pension by 2.2 %.

### The variant: the single-premium form

Model point 2 is the *Einmalbeitrag* the notes promise beside the recurring form: 50,000.00
EUR at age 50, *Rentenbeginn* at 67 so `proj_len() = 204` months and the frame is
`t = 0 … 203`, a `fund` death benefit — the
*Fondsguthaben* itself, so there is no net amount at risk and `charge_risk` is **0.00 at
every month** — and the same `std_gross` scale and `base` fund otherwise. There is no
*Beitragssumme* to zillmer against and no five-year spreading to obey, so the acquisition
charge is the *Zuzahlungskosten* levied **once on receipt**, 2.50 % x 50,000.00 =
**1,250.00**, beside a premium admin charge of 4.00 % x 50,000.00 = **2,000.00**, also once.

| t | pols_if | premiums | prem_to_av | charge_acq | charge_admin_prem | charge_admin_fund | charge_policy_fee | expenses | commissions | net_cf | av BEF_DECR |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 50,000.00 | 46,750.00 | 1,250.00 | 2,000.00 | 11.73 | 3.00 | 204.28 | 2,000.00 | 1,060.45 | 46,908.94 |
| 1 | 0.994685 | 0.00 | 0.00 | 0.00 | 0.00 | 11.71 | 2.98 | 4.27 | 0.00 | 10.43 | 47,068.42 |
| 2 | 0.989399 | 0.00 | 0.00 | 0.00 | 0.00 | 11.69 | 2.97 | 4.25 | 0.00 | 10.40 | 47,228.46 |
| 11 | 0.943067 | 0.00 | 0.00 | 0.00 | 0.00 | 11.48 | 2.83 | 4.11 | 0.00 | 10.20 | 48,694.00 |
| 59 | 0.728611 | 0.00 | 0.00 | 0.00 | 0.00 | 10.45 | 2.19 | 3.43 | 0.00 | 9.20 | 57,329.28 |
| 119 | 0.611558 | 0.00 | 0.00 | 0.00 | 0.00 | 10.76 | 1.83 | 3.09 | 0.00 | 9.50 | 70,347.78 |
| 203 | 0.457239 | 0.00 | 0.00 | 0.00 | 0.00 | 10.72 | 1.37 | 48.30 | 0.00 | -36.21 | 93,766.43 |
| **Total** | **136.171795** | **50,000.00** | **46,750.00** | **1,250.00** | **2,000.00** | **2,206.15** | **408.52** | **911.63** | **2,000.00** | **2,953.04** | — |

Read against the anchor, that is the whole of what the *Beitragsverrechnung* does. The
charges are taken **once, at the front**, so `t = 0` carries a `net_cf` of **+1,060.45**
where the anchor's is -1,966.22: the 3,250.00 withheld at inception more than covers the
2,204.28 of acquisition cost — 2,000.00 of `commissions` and 204.28 of `expenses`, and there is no sixty-month recovery to wait for. From `t = 1`
the ledger is nothing but the two fund-based charges running down a fund growing faster than
they take. The *Fondsguthaben* reaches **93,766.43 EUR** and buys **234.42 EUR** a month at
the same 25.00 *Rentenfaktor*; the reduction in yield is **1.2320 % p.a.**, a little below
the anchor's 1.3407 %, a single premium paying the acquisition charge once and on a smaller
base relative to the money invested.

**And the second variant the notes promise, the charge scale.** The reduction in yield is the
one number that puts four tariffs on one scale. All four levels are **[std]**:

| Model point | Tariff | Fund | Gross | Reduction in yield | *Fondsguthaben* at *Rentenbeginn* |
|---|---|---|---|---|---|
| 11 | `std_netto` | `etf` | 5.0000 % | **0.4484 % p.a.** | 255,658.29 EUR |
| 13 | `std_low` | `base` | 5.0000 % | **0.7799 % p.a.** | 158,606.04 EUR |
| 1 | `std_gross` (anchor) | `base` | 5.0000 % | **1.3407 % p.a.** | 129,699.88 EUR |
| 5 | `std_high` | `base` | 5.0000 % | **2.4073 % p.a.** | 229,128.42 EUR |

The four cells differ in premium and term as well as in tariff, so this is not a controlled
experiment and must not be read as one. What it shows is that the charge scale moves the
reduction in yield by **a factor of five** across the argued range — a spread the supervisor has
since quantified rather than merely called considerable: *"Die Effektivkosten der verschiedenen
Anbieter und Produkte unterscheiden sich erheblich"*, with a weighted mean of 1,90 % p.a. at
entry age 37 over 30 years, quartiles at 1,30 / 1,64 / 2,35 %, and insurers above 4 % at every
age-and-term combination [R10] [R11]. **The delib figures below are still delib's own**, computed
on delib's `[std]` stack and not on Annex VI, and must not be quoted as market figures; the point
of setting them beside the survey is to show that `std_gross` sits below the market's lower
quartile. Model point 11 is the *Nettotarif* and 1 the commission tariff; **the gap between their
reduction in yield is the acquisition load**, the parameter this library most needs and cannot
source at a carrier [S18] — and note that a real net tariff's published *Effektivkosten* excludes
the adviser fee the client pays separately [R10], so the delib gap is the cleaner comparison.

### What the model stage changed in these notes

Three places where the notes as drafted disagreed with the model that implements them, and
in each the model was right:

1. **`result_cf()` publishes `liability_cf` as a nineteenth column**, after `net_cf`. The
   column list above named seventeen while the recursion defined `liability_cf(t) =
   -net_cf(t)` beside them, and the cross-model naming review then split `commissions` out of
   `expenses` as an eighteenth; the conventions suite asserts that identity **on the frame**, so
   the cells has to be a column or the sign convention is unverifiable.
2. **Pitfall 7's two assertions were too broad.** `charge_acq(t) = 0` for `t ≥ 60` fails on
   model point 9, whose *Zuzahlung* at `t = 120` pays 500.00 of *Zuzahlungskosten* that the
   notes' own `alpha(t)` books there; and `sum charge_acq_pp = alpha_rate x beitragssumme()`
   fails on point 6 (0.00 against 2,775.00, the in-force frame opening past the window) and
   on point 9 (3,380.00 against 2,880.00). The pitfall now asserts the **instalment** and
   names both exceptions.
3. **The reduction-in-yield equation gained the opening *Fondsguthaben*.** Without it the
   measure credits the charge stack with money an in-force cell never received as premium.
   The term is zero on every new-business cell, so nothing above moves.

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are cited, not reproduced.

- **The German statutory *Deckungsrückstellung*.** For a fondsgebundene contract the reserve is
  in two parts that must not be confused: the **unit liability**, which is the *Fondsguthaben*
  itself, backed one-for-one by the *Anlagestock* [R15] [REG-R7], and a **non-unit reserve** for
  the future administration and risk cash flows the charges are supposed to cover. This model
  produces the second stream and does not discount it. The *Höchstrechnungszins* of the DeckRV
  does **not** bind the accumulation phase — § 2 Abs. 1 applies only *"[b]ei Versicherungsverträgen
  **mit Zinsgarantie**"*, and a pure unit-linked contract has none [R12] [REG-R14] [REG-R15]; the
  *Höchstzillmersatz* does, and it is a parameter of the model rather than of the valuation [R12]
  [REG-R16]. The *Zinszusatzreserve* has nothing to attach to on the unit side [REG-R17].
- **§ 169 VVG is a payment floor, not a reserve — and on this contract the floor is Abs. 4's
  *Zeitwert*, not Abs. 3's five-year rule.** Abs. 3 carries the five-year spreading as a minimum
  on the *Deckungskapital* branch and reaches a unit-linked contract only *"im Übrigen"*, that is
  to the extent a benefit is guaranteed; § 4 DeckRV governs what the insurer may **reserve** [R1] [R12]
  [REG-R16] [REG-R28]. On this design the two do not conflict, because the tariff takes the
  acquisition charge in exactly the sixty instalments the payment floor implies, so the
  *Rückkaufswert* is the *Fondsguthaben* at every duration and no `max()` against a floor is
  needed. **The statute now answers the question this bullet left open**: on a contract with no
  guaranteed benefit there is no Abs. 3 floor to reach, and the protection operates through the
  tariff's *Kostenverrechnung* clause instead — which is what a real wording does [S2] § 18
  Abs. 2. Both readings still give the same numbers here.
- **Solvency II.** Technical provisions are a best estimate — the probability-weighted average of
  future cash flows discounted at the relevant risk-free term structure — plus a risk margin
  [REG-R1] [REG-R2] [REG-R6], with EIOPA publishing the curves monthly [REG-R4].
  `BEL_non_unit = Σ_t v(t) × liability_cf(t)` over the recursion above, with the unit liability
  added at market value. **The contract boundary is an open question on this product and this
  library does not resolve it**: the *Beitragsdynamik* is optional at each anniversary and the
  insurer's charge scale is revisable in some tariffs, both of which bear on where the boundary
  falls, and **no boundary rule in this library rests on an article anybody read**: the Delegated
  Regulation was retrieved for the re-verification pass, but only Artt. 37–39, the risk-margin
  articles, were read from it, and the contract-boundary articles were not [REG-R2].
- **The *Rentenfaktor* is an option and this model does not value it.** A guaranteed conversion
  rate applied thirty years forward to an unknown capital is a written option on longevity and on
  interest rates, and a deterministic projection prices none of it. The `max(guaranteed, current)`
  rule makes it explicitly one-sided, and that rule is now read in a wording rather than inferred:
  *"Der tatsächliche Rentenfaktor ist der höhere Wert aus dem zu Rentenbeginn aktuellen
  Rentenfaktor und dem zu Vertragsbeginn garantierten Rentenfaktor"* [S2] [S4] [R22]. A stochastic
  run — the same recursion with a scenario-dependent unit price and a scenario-dependent current
  factor — is what a time-value-of-options-and-guarantees calculation consumes. The supervisor
  treats the conversion terms as a *Kundennutzen* parameter in their own right, the reference
  point being *"das Verhältnis zwischen dem am Ende der Ansparphase zur Verfügung stehenden
  Kapital und den vom Kunden voraussichtlich bezogenen Rentenleistungen"* [R10], so a valuation
  layer is not the only reason to care what the factor is.
- **IFRS 17 and professional standards.** A fondsgebundene contract is the archetypal
  direct-participating contract and would be measured under the **variable fee approach**; the VFA
  mechanics were not read and are `[unverified]` [REG-R55]. German statutory reporting runs under
  HGB §§ 341–341o and the *RechVersV*, which report unit-linked business separately [REG-R54].
  The DAV's *Fachgrundsätze* and the responsible actuary's certifications under §§ 141–143 VAG
  frame the professional obligations [REG-R11] [REG-R56].

---

## Key sensitivities and model risks

In rough order of leverage for a German unit-linked block:

1. **The assumed fund return.** It is the single largest number in the model and it has **no
   source at all** — PRIIPs deliberately supplies none, deriving its scenarios from the
   underlying's own history [R8] [R9] [REG-R32]. It drives the *Fondsguthaben*, the fund-based
   charge income, the net amount at risk (and so the risk charge), and the annuity the
   *Rentenfaktor* buys. The `zero` scenario is shipped precisely so a reader can see the charge
   stack with the return switched off, and the four scenarios together bracket what the assumption
   is worth.
2. **The charge stack, and the acquisition charge above all.** Every level is **[std]** and the
   whole first-order economics of the product is *return minus charges*. The `std_netto` variant
   on the same chassis isolates the acquisition load. **The stack can now be located in the
   market, and it sits low**: BaFin's survey puts the *Effektivkosten* of the most-sold
   fondsgebundene products at a weighted mean of **1,90 % p.a.** at entry age 37 over 30 years —
   this model's anchor cell — with quartiles at **1,30 / 1,64 / 2,35 %** and insurers above 4 % at
   every age-and-term combination [R11] [REG-R35], and one real tariff reports **1,4 %–3,4 %** over
   the same term [S15]. `std_gross`'s implied ~1 % p.a. is **below the observed lower quartile**.
   Any statement that starts "a German unit-linked contract costs…" and ends in a delib number is
   therefore describing a cheap tariff, not a typical one.
3. **The guaranteed *Rentenfaktor* — and this is the largest known error in the model.** 25.00 at
   age 67 is **derived arithmetic**, and at the anchor cell the observed value is **22,91**
   [S15], so the shipped table is about **9 % generous** there. It is linear in the annuity, so
   that is a 9 % overstatement of the pension the model reports. Worse, the shipped table is flat
   in the deferment where a real one falls with it — 25,22 / 24,12 / 22,91 / 21,83 at 12 / 20 /
   30 / 40 years to the same age 67 — so the error grows with the term and the model prices short
   and long deferments alike. **The table is not changed in this pass**, because
   `rentenfaktor_table.csv`, the worked example and the golden tests move together. A reader who
   needs a market level should take the observed values above rather than the shipped ones, or go
   to a current *Basisinformationsblatt* [S15] [R23].
4. **The lapse shape.** No German unit-linked *Stornoquote* was established. On this product the
   direction of the exposure is the opposite of a protection block's: lapses in the first five
   years remove policies **before** the insurer has recovered the commission it paid at inception,
   so early lapse destroys value while late lapse merely shortens a profitable tail. The
   tax-threshold step is the least arbitrary part of the table, because the threshold itself is
   statutory [R20] [REG-R45]; its magnitude is not.
5. **`mort_be_factor`, and the two mortality bases.** A flat 0.75 ratio makes the *Risikoergebnis*
   exactly 25 % of the *Risikobeitrag*, which is analytically convenient and biologically crude;
   the real wedge varies by age. Because the *Beitragsrückgewähr* net amount at risk vanishes once
   the fund overtakes the premiums paid, the whole of this exposure sits in the first decade of
   the anchor cell, and it is far larger on model point 7, where a fixed *Mindesttodesfallleistung*
   on a decaying fund makes the risk charge grow without limit.
6. **The one-fund simplification.** *Fondswechsel*, multi-fund splits and *Ablaufmanagement* all
   collapse into a single return path, so the model cannot show dispersion between funds and
   cannot represent a *Wertsicherungsfonds* at all. That is also why the hybrid designs are named
   and not implemented: their whole content is what they do on paths this projection does not
   generate.
7. **The unmodelled *Überschussbeteiligung*.** A unit-linked contract's surplus arises from the
   risk and cost results only, because MindZV § 3 Abs. 1 computes the creditable investment income
   *"ohne die der Lebensversicherung für Rechnung und Risiko der Versicherungsnehmer zuzuordnenden
   Erträge und Aufwendungen"*, and § 3 Abs. 5 of a real AVB confirms that *"[v]or Rentenbeginn …
   keine Bewertungsreserven"* arise [R5] [R14] [S2] [REG-R9] [REG-R18]. The statutory minima are
   **90 %** of the *Risikoergebnis* and **50 %** of the *übriges Ergebnis*. The model computes the
   risk result and credits none of it back, so the projected *Fondsguthaben* is biased
   **downward** — the honest direction for a charge demonstration, and the direction to keep in
   mind when comparing the reduction in yield with a published *Effektivkosten* figure. Two facts
   limit the size of the omission: a real pre-*Rentenbeginn* credit is a premium-based
   *Grundüberschussanteil* that a paid-up or single-premium contract does not receive at all [S2],
   and BaFin found in 2025 that more than half of German life insurers declare no
   *Risikoüberschussbeteiligung* even on adequately priced new products [R11].
8. **Provenance, restated after the pass of 2026-08-30.** The mechanics of this model are no
   longer uncited. Read verbatim in a German fondsgebundene AVB [S2]: the *Beitragsverrechnung*
   split, the *Beitragsrückgewähr* death benefit, the `max(guaranteed, current)` factor rule, the
   *Zeitwert* *Rückkaufswert*, the *Stückkosten* taken by unit cancellation, the decay of a
   paid-up contract, the *Rücknahmepreis* and waived *Ausgabeaufschlag*, and the 0 %
   *Rechnungszins* on DAV 2004 R behind the *Rentenfaktor*. Read in the canonical statutes: the
   25 ‰ cap (DeckRV § 4 Abs. 1), the *Zeitwert* branch (VVG § 169 Abs. 4), the *Stornoabzug*
   conditions (Abs. 5), the termination right (§ 168), the paid-up right (§ 165), the 12/62 rule
   and the 15 % *Teilfreistellung* (EStG § 20 Abs. 1 Nr. 6 with § 52 Abs. 28), and the MindZV
   percentages. **The levels remain [std]**, and two are now known to be wrong against the one
   tariff that could be read: the guaranteed *Rentenfaktor* (item 3) and the death table behind
   `q_tariff` [R17]. A calibration pass against a real *Produktinformationsblatt* — the document
   that carries a carrier's charge rates, and the one limb of [S16] still missing — remains
   required before any quantitative use of this model.

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
[R2]: #delib-fondsgebundene_rentenversicherung-r2
[R20]: #delib-fondsgebundene_rentenversicherung-r20
[R22]: #delib-fondsgebundene_rentenversicherung-r22
[R23]: #delib-fondsgebundene_rentenversicherung-r23
[R24]: #delib-fondsgebundene_rentenversicherung-r24
[R3]: #delib-fondsgebundene_rentenversicherung-r3
[R5]: #delib-fondsgebundene_rentenversicherung-r5
[R6]: #delib-fondsgebundene_rentenversicherung-r6
[R7]: #delib-fondsgebundene_rentenversicherung-r7
[R8]: #delib-fondsgebundene_rentenversicherung-r8
[R9]: #delib-fondsgebundene_rentenversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R28]: #delib-reg-r28
[REG-R31]: #delib-reg-r31
[REG-R32]: #delib-reg-r32
[REG-R33]: #delib-reg-r33
[REG-R34]: #delib-reg-r34
[REG-R35]: #delib-reg-r35
[REG-R36]: #delib-reg-r36
[REG-R4]: #delib-reg-r4
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R52]: #delib-reg-r52
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R7]: #delib-reg-r7
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
