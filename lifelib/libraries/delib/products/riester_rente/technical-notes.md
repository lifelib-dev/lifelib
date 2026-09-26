# Technical Notes

**Status:** Draft, 2026-08-29 (access date for every citation below).

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`Riester_DE_S`**, **monthly** grid over an annual contract — for the standardized composite German **klassische
Riester-Rentenversicherung** defined in `product-spec.md` (same directory). This is not any single
insurer's product; **no carrier level was established at any house for any year** — three retrieved
wordings now fix the *shapes* [S2] [S4] [S6], but one tariff is not a market — so every carrier
parameter below is **[std]** and every statutory one is cited. **These notes were drafted with no
retrieval and no search available and have since been re-verified against the primary documents**:
every statutory citation below was checked against the canonical XML, and twenty-six of the
forty-two entries in `sources.md` now record `Retrieved: yes`. [S#]/[R#] tags refer to that source
list (numbering carried from `_research/riester_rente.md`; frozen); [REG-R#] tags refer to the
cross-product reference library `references/regulatory-and-actuarial-references.md` (its own frozen
R1–R56 numbering). [unverified] now marks a claim this re-verification did **not** reach — a carrier
level, a market figure, a behavioural rate, a historic vintage. Parameter values are identical to
those in
`product-spec.md`. Cells names, model-point columns and CSV headers are English `lower_snake_case`;
German terms of art keep their German form in prose.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — the saver's
  *Eigenbeitrag*, the state *Zulage*, death, surrender, transfer, lump-sum, commutation and annuity
  benefits, expenses and commission — for a single-policy model point on an expected
  (probability-weighted) basis, together with the two state variables that make the product what it
  is: the account (*Deckungskapital* plus *Überschussguthaben*) and the **Beitragsgarantie
  accumulator**. Discounting, the *Deckungsrückstellung*, the *Zinszusatzreserve*, Solvency II
  technical provisions, the risk margin and capital are **out of scope** and are referenced rather
  than specified (see *Valuation and reserve pointers*).
- **Projection grid: monthly, over a contract that is annual.** The model runs on **two clocks**
  and the argument of a cells says which. `t` counts **projection months** from the valuation date
  and is **0-based**: `t = 0 … proj_len() − 1` with `proj_len() = 12 × proj_len_y()`.
  `k = proj_year(t) = t // 12` counts **projection years** and is the annual-step model's own `t`.
  The contractual contract year is `duration_y(k) + 1 = duration_init + k + 1`, which is `k + 1`
  only on a point projected from its own inception (`duration_init = 0`). The
  valuation date is **1 January 2027** [std] — the first day on which the product is closed to new
  business [REG-R44] — so `calendar_year_y(k) = 2027 + k` and the calendar year steps on the
  anniversary. The contract is annual in every
  respect the annual clock carries: the Zulage is an annual entitlement determined on a calendar
  year and paid once by the ZfA [R9] [R10] [R11], the *Überschuss* is declared annually, the two
  charges and the interest credit fall once a year, and the *Beitragsgarantie* is tested once. The
  *Eigenbeitrag* keeps it too, because the *Ratenzuschlag* prices a fractionated payment mode by
  loading the **amount** rather than by moving the contribution year.
- **What the monthly clock is for.** The in force, the three decrements, the claims, the expenses,
  the commission and the *Rente* instalments. The decrements carry the library's two speeds —
  `mort_rate`, `lapse_rate` and `transfer_rate` are the **annual** rates of the year the month falls
  in, `mort_rate_mth`, `lapse_rate_mth` and `transfer_rate_mth` the geometric twelfths the
  recursion applies — so twelve months compound back to each annual rate exactly and `pols_if(12k)`
  is the annual-step model's `pols_if(k)` to the last bit. The whole accumulation is therefore
  unchanged, and what the grid buys is the **monthly** *Leibrente* the AltZertG requires, together
  with a dated split of the three accumulation exits; both are quantified below.
- **`proj_len()` is the number of projected periods**, the exclusive end of the frame, per the
  library ruling asserted in `tests/test_model_conventions_de.py`:
  `result_cf().index[-1] == proj_len() − 1` and `len(result_cf()) == proj_len()`.
  `proj_len_y() = omega_age − age(0) + 1`, with `age(0) = issue_age + duration_init` and
  `omega_age = 110` **[std]**. The frame is contiguous `0 … proj_len() − 1` on every model point,
  including a point that commutes at *Rentenbeginn* and therefore carries zeros to the end — a
  uniform frame is what lets two model points be read side by side, and truncating a commuted point
  is a numbered pitfall.
- **Two phases in one projection.** `k_conv() = rentenbeginn_age − age(0)` is the **conversion
  year** and `t_conv() = 12 · k_conv()` the conversion month. `is_accum(t)` holds for
  `t < t_conv()`, `is_payout(t)` for `t ≥ t_conv()`, with `is_accum_y(k)` and `is_payout_y(k)` the
  annual readings. The
  accumulation recursions stop at `k_conv()`; the annuity liability runs from `t_conv()` to
  `proj_len() − 1`. A model that stops at *Rentenbeginn* has not modelled a lifelong annuity, which
  is the benefit the AltZertG requires [R1] [REG-R43].
- **Timing conventions [std].** The *Eigenbeitrag* and any unsubsidised contribution are received
  in the **first month** of the projection year; the *Zulage* earned in year `k − 1` is credited in
  that same month of year `k`, alongside that year's own contribution; charges are deducted from the
  contribution there; interest is credited at the **end** of the year on the account plus the
  year's *Sparbeitrag*; decrements act at the **end of each month**, and death, surrender and
  transfer benefits are struck on `av_total_pp(k + 1)` — the **annual** end-of-year account value,
  which is where the account is struck, so an exiting policy still takes the full year's interest
  and a contract year's exits release exactly what the annual-step model released. Conversion
  happens at `t_conv()`, after the final
  Zulage has been credited and before any payout-phase mortality. Annuity instalments are paid
  **monthly in advance**.
- **The monthly *Leibrente*, which is why the grid is monthly.** The contract pays a monthly
  *Leibrente* in advance [R1] and the *Rentenfaktor* is quoted in euro a month. The annual-step
  model these notes were first written for paid **twelve instalments as one annual amount at the
  start of the payout year**, to those alive at the start: for a life dying during the year it paid
  a full year where the contract pays only the instalments falling due, an overstatement of roughly
  `½ · q(x) · 12R` a year, about 0,7 % of the annuity at attained age 70 on the shipped proxy. That
  approximation is gone — `annuity_month_pp()` is paid to whoever `pols_annuity_pay(t)` says is paid
  that month — and it is worth 361,74 € of the anchor's payout phase and 573,50 € of model point
  12's, which carries no *Rentengarantiezeit*. Inside a guarantee window the two grids agree **to
  the cent**, the count being fixed there. The *level* of the annuity was always right, the
  conversion factor carrying the Woolhouse `−11/24` correction.
- **Age basis.** Age last birthday, `age_y(k) = issue_age + duration_init + k`, stepping on the
  anniversary so the twelve months of a projection year share one rate. Riester tariffs
  are **unisex** from a 2006 vintage [R23] [REG-R34], so `sex` is carried for reporting only and
  must not enter any rate.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** — contributions
  and Zulagen positive, benefits and expenses negative — with the outgo-positive orientation
  published as `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash
  flows to the cent, `pols_if` to six decimals **[std]**.
- **Out of scope, and said so rather than left to be discovered.** No unit-linked funds and no
  rebalancing algorithm (that chassis is `fondsgebundene_rentenversicherung`); no *Auszahlungsplan
  mit Restverrentung*; no Wohn-Riester in either limb — no *Eigenheimbetrag* withdrawal decrement,
  no certified *Darlehen*, no *Wohnförderkonto* [R13] [R19]; no *Berufsunfähigkeits-*
  *Zusatzversicherung* liability (only the guarantee carve-out its premium creates); no
  *Versorgungsausgleich*; no surplus in payment; no *Günstigerprüfung* and no policyholder tax of
  any kind; and no apportionment of investment return between the two contribution pools, which a
  real *Leistungsmitteilung* must perform [R12].

---

## Model inputs

Inputs are **external CSVs beside `run.py`**, in the `annuallife/TradLife_A` layout: the model folder
holds `__init__.py`, `_system.json` and the two Space directories and nothing else. `Data` holds
`input_dir()`, one reader cells per file and one `*_file` string Reference per file, takes no
parameters, and is therefore read **once per model** rather than once per model point; `Projection`
reaches it through a `data` Reference and holds no `*_file` Reference and no `input_dir`.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the twenty-six attributes tabulated below |
| `mort_table_accum.csv` | `age` (16–110) | `qx`, `provenance` |
| `annuity_mort_table.csv` | `age` (55–110) | `qx_base`, `improvement`, `provenance` |
| `lapse_table.csv` | `duration` (1–60) | `lapse_rate`, `transfer_rate`, `provenance` |
| `zulage_schedule.csv` | `zulage_id`, `t` | `unmittelbar`, `n_kinder_pre2008`, `n_kinder_post2008`, `bonus`, `provenance` |
| `income_schedule.csv` | `income_id`, `t` | `income`, `provenance` |
| `surplus_scenario.csv` | `scenario_id`, `t` | `decl_rate`, `provenance` |
| `freq_loading.csv` | `prem_freq` | `load`, `provenance` |

**Every file except `model_point_table.csv` carries a per-row `provenance` column**, delib's second
ruling: a model point is a configuration, every other row is an assumption and says where its number
came from. The two decrement tables are **[std] proxies** for proprietary DAV tables that this
library does not ship [REG-R47] [REG-R48] [REG-R49], anchored so that the worked example reproduces
exactly; what a replacement must preserve is stated in assumption class (c) and in `sources.md`.

### Cells vocabulary

`Data` publishes `input_dir`, `model_point_table`, `mort_table_accum`, `annuity_mort_table`,
`lapse_table`, `zulage_schedule`, `income_schedule`, `surplus_scenario` and `freq_loading`.

`Projection` publishes the library's shared names — **`model_point`, `proj_len`, `age`, `pols_if`,
`mort_rate`, `claims`, `expenses`, `net_cf`, `result_cf`** — plus, in the same lifelib spelling:
`pols_if_init`, `pols_if_at`, `pols_death`, `pols_lapse`, `pols_transfer`, `pols_conv`,
`pols_annuity_pay`; `mort_rate_at_age`, `annuity_mort_rate`, `lapse_rate`, `transfer_rate`;
`duration`, `duration_y`, `duration_mth`, `contract_year`, `calendar_year`, `calendar_year_y`,
`proj_len_y`, `proj_year`, `is_anniv`, `prem_due`, `k_conv`, `t_conv`, `is_accum`, `is_accum_y`,
`is_payout`, `is_payout_y`; `mort_rate_mth`, `lapse_rate_mth`, `transfer_rate_mth`; `income_ref`,
`zulage_entitlement_pp`, `zulage_granted_pp`, `zulage_pp`, `zulage_cum_pp`,
`mindesteigenbeitrag_pp`, `eigenbeitrag_pp`, `eigenbeitrag_paid_pp`, `contrib_total_pp`;
`acq_charge_pp`, `admin_charge_pp`, `prem_to_av_pp`; `dk_pp`, `surplus_acct_pp`, `av_total_pp`,
`av_total_pp_at`, `av_total_at`, `int_guar_pp`, `int_surplus_pp`, `int_credited_pp`, `decl_rate`;
`guar_pp`, `guar_carve_out_pp`, `garantieluecke_pp`, `pool_gefoerdert_pp`, `pool_ungefoerdert_pp`;
`slueb_pp`, `bewres_pp`, `account_conv_pp`, `capital_conv_pp`, `garantieluecke_conv_pp`,
`ann_factor`, `rentenfaktor_curr`, `rentenfaktor_applied`, `annuity_month_pp`, `is_kleinbetrag`,
`teilkapital_pp`, `annuity_capital_pp`, `commutation_pp`, `annuity_pp`; `db_pp`, `cv_pp`,
`transfer_value_pp`, `exit_charge_pp`; `premiums`, `zulagen`, `int_credited`, `commissions`,
`liability_cf`, `result_cf_annual`; and the six `check_*` cells with their `check_*_resid`
companions — four of which take a projection **year**, because the account, the guarantee
accumulator, the conversion and the ZfA lag move once a year. `claims(t, kind)`
takes an uppercase `kind` in `{DEATH, LAPSE, TRANSFER, LUMPSUM, COMMUTATION, ANNUITY}` and produces
the `claims_<lowercase kind>` columns. **No retired name is used**: there is no `lapse_rate_ann`, no
`prem_net_pp`, no `mort_ae_factor`, no `check_pols_if`, no `claims_wd` and no bare `claims` column.

---

## Model point attributes

`model_point_table.csv` is indexed by `point_id` and carries the columns below. It is the one input
file exempt from the provenance rule, because a model point is a **configuration** rather than an
assumption. The right-hand column names the points that exercise each attribute away from its base
value; the thirteen points are described under *Worked example*.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Row key; `Projection` is parameterized by it | all |
| `sex` | enum {M, F} | Reporting only. Pricing, the conversion and every rate are **unisex** [R23] | all |
| `issue_age` | int | Attained age at conclusion of the contract | all |
| `duration_init` | int | Completed contract years at the valuation date; 0 for a point projected from issue | 2, 6, 13 at 0 or 1 |
| `pols_if_init` | float | Policies represented; `result_cf()`'s first `pols_if` equals it exactly | all |
| `rentenbeginn_age` | int | Attained age at which the payout phase starts; bounded below by 62 for a contract concluded from 2012 [R1] | 13 (at the statutory floor, 62) |
| `rechnungszins` | float | The tariff's guaranteed rate, at or below the *Höchstrechnungszins* of the vintage [R22] [REG-R15] | 3 (0,90 %), others 0,25 % |
| `beitragssumme` | EUR | The *Beitragssumme* fixed at conclusion; the acquisition-charge and initial-commission base | all |
| `contrib_form` | enum {mindest, fixed} | `mindest` recomputes the § 86 amount every year; `fixed` is a level contractual contribution | 5, 8 |
| `contrib_fixed_pp` | EUR p.a. | The level contribution under `fixed`; 0 under `mindest` | 5 (60,00), 8 |
| `contrib_ratio` | float | Fraction of the *Mindesteigenbeitrag* actually paid; drives the proportional Kürzung [R10] | 7 (0.50) |
| `contrib_extra_pp` | EUR p.a. | Unsubsidised contribution above the § 10a ceiling; enters the account **and** the guarantee, draws no Zulage [R12] | 8 (900,00) |
| `rider_prem_pp` | EUR p.a. | Contribution applied to a biometric rider. **Not a cash flow of this model**; it appears only in the guarantee carve-out, capped at 20 % of total contributions [REG-R43] | 9 (400,00) |
| `income_id` | str | Key into `income_schedule.csv` | all |
| `income_init` | EUR | Contribution-liable earnings in the calendar year **before** the projection starts; the reference income for `t = 0` | all |
| `zulage_id` | str | Key into `zulage_schedule.csv` | all |
| `zulage_init_pp` | EUR | The Zulage credited at `t = 0`, earned in the year before it | 6 (375,00, including the bonus) |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | Payment frequency; keys `freq_loading.csv` | 3, 4, 6, 7, 10, 13 |
| `bfs_year` | int | The 0-based period index `t` from which contributions stop (*Beitragsfreistellung*); **−1 = never**, because `0` is now the first projected period | 10 (`t = 3`) |
| `dk_pp_init` | EUR | *Deckungskapital* at the valuation date | all |
| `surplus_pp_init` | EUR | *Überschussguthaben* at the valuation date | all |
| `guar_pp_init` | EUR | *Beitragsgarantie* accumulator at the valuation date | all |
| `teilkapital_share` | float | Elected *Teilkapitalauszahlung*, 0 to the statutory 0.30 [R1] | 12 (0.00) |
| `rentenfaktor_guar` | float | Guaranteed *Rentenfaktor*, € of monthly annuity per 10 000 € of capital, struck at inception | all |
| `rentengarantie_years` | int | *Rentengarantiezeit*; payments continue to beneficiaries for this many years from *Rentenbeginn* | 12 (0) |
| `scenario_id` | str | Key into `surplus_scenario.csv`; names the `decl_rate` path | 11 (`low`) |

Three of these are the ones a reader from another market is most likely to mis-set. `zulage_init_pp`
exists **only** because the Zulage arrives a year late [R11], so an in-force point opens owing one;
`rider_prem_pp` is a contribution the model deliberately does **not** see as cash; and
`contrib_ratio` is not a lapse or a premium holiday but the § 86 proportional Kürzung, which reduces
the **subsidy** and not only the contribution.

### The thirteen model points

Between them they exercise both contribution forms, all four payment frequencies, every option the
contract carries, an at-issue point beside the in-force ones, and four boundary cases.

| # | Cell | What it exercises |
|---|---|---|
| **1** | **Anchor** — F, issue age 47 in 2024, in force at duration 3, attained 50, *Rentenbeginn* 67, 0,25 %, one child born 2010, annual | The worked example. A live acquisition-charge window, a falling Zulage step, the 2 100 € ceiling binding from `t = 12`, a 30 % lump sum, a 10-year *Rentengarantiezeit*, and an account opening **below** the guarantee |
| **2** | The same contract **at its own inception** — `duration_init = 0`, 2024 | Acquisition charge from contract year 1, the acquisition expense and initial commission cash at issue, and the **reconciliation of point 1's opening balances** |
| **3** | Family with children born **2006 and 2010** — M, issue age 38 in 2018, 0,90 %, monthly | Both *Kinderzulage* rates running **simultaneously** (660,00 € entitlement); an older *Rechnungszins* vintage; the monthly frequency loading |
| **4** | **§ 86 case D** — income 20 000 €, two post-2008 children, quarterly | The *Sockelbeitrag* **floor** binding (boundary); a 12,92× subsidy multiple; and a *Kleinbetragsrente* **commutation** at *Rentenbeginn* |
| **5** | ***Mittelbar* eligible spouse** — `contrib_form = fixed`, 60,00 € a year, *Grundzulage* only | The `fixed` contribution form; the economically extreme corner of the book; a second commutation |
| **6** | **Berufseinsteiger** — M, issue age 23 in 2026, attained 24, monthly | The once-in-a-lifetime **200 € bonus** inside `zulage_init_pp`; the longest projection in the table |
| **7** | **Under-payer** — `contrib_ratio = 0.50`, half-yearly | The § 86 **proportional Kürzung**: half the contribution, half the Zulagen |
| **8** | **Two pools** — `contrib_form = fixed` at the ceiling plus `contrib_extra_pp = 900,00 €` | `pool_ungefoerdert_pp`; unsubsidised money entering the **guarantee** while drawing no Zulage |
| **9** | **Rider carve-out at the cap** — `rider_prem_pp = 400,00 €` on a 1 200,00 € contribution | The **20 % cap** on the biometric carve-out binding (boundary) |
| **10** | ***Beitragsfreistellung*** — `bfs_year = 3`, monthly | The book's dominant exit as a state change: guarantee frozen, Zulagen stopped, account rolling, acquisition charge still biting |
| **11** | **Low declared rate on a short deferral** — F, issue age 57 in 2024, in force at duration 3, attained 60, *Rentenbeginn* 67, income 60 000 € so the 2 100 € ceiling binds, `scenario_id = low` (0,50 %) | A **positive *Garantielücke*** at *Rentenbeginn* — the product's signature output. The deferral is seven years rather than seventeen because on the anchor's own term 0,50 % still does not open a gap; that result is reported under *Worked example* as the sensitivity it is |
| **12** | **No lump sum, no guarantee period** — `teilkapital_share = 0`, `rentengarantie_years = 0` | The pure lifelong annuity, and the invariance of `annuity_pp` to the guarantee period |
| **13** | **Late entrant at the statutory floor** — issue age 60 in 2026, *Rentenbeginn* **62**, monthly | The earliest certifiable payout age for a post-2012 contract (boundary); the shortest accumulation and the least guarantee headroom |

**Model point 1 is the worked example's anchor cell** and is `Projection[1]`.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len_y()` | Number of projected **years**, `omega_age − age(0) + 1` | once per model point |
| `proj_len()` | Number of projected **months**, `12 × proj_len_y()`; the frame is `0 … proj_len() − 1` | once per model point |
| `proj_year(t)`, `is_anniv(t)`, `prem_due(t)` | The projection year of month `t`, `t // 12`; its last month; and the month the year's contribution falls due | within year |
| `k_conv()`, `t_conv()` | The conversion **year**, `rentenbeginn_age − age(0)`, and the conversion **month**, `12 · k_conv()` | once |
| `age_y(k)`, `duration_y(k)`, `calendar_year_y(k)` | Attained age, completed contract years at the **start** of projection year `k` (0-based; the contract-year band is the 1-based `duration_y(k) + 1`), and the calendar year of year `k`; `age(t)`, `duration(t)` and `calendar_year(t)` read the same three from a month | annual, stepping on the anniversary |
| `pols_if(t)` | Policies in force at the **start** of month `t`; `pols_if(0) = pols_if_init()` | monthly recursion |
| `pols_if_at(t, timing)` | `"BEF_DECR"` = `pols_if(t)`, `"AFT_DECR"` = `pols_if(t+1)` | within month |
| `pols_death(t)`, `pols_lapse(t)`, `pols_transfer(t)` | Expected deaths, surrenders and *Anbieterwechsel* exits in **month** `t`, at the geometric twelfths `q_mth`, `w_mth` and `θ_mth` of the year's annual rates; in the annual model they ran in sequence at one year end, here they compete month by month | monthly |
| `pols_conv()`, `pols_annuity_pay(t)` | Policies reaching *Rentenbeginn*; policies on which an annuity instalment is actually paid, which during the *Rentengarantiezeit* is `pols_conv()` rather than `pols_if(t)` | annual |
| `income_ref(k)` | The **previous** calendar year's contribution-liable earnings driving year `t`'s entitlement | annual (lag 1) |
| `zulage_entitlement_pp(k)`, `zulage_granted_pp(k)`, `zulage_pp(k)` | Full § 84/85 entitlement; entitlement after the § 86 proportional Kürzung; the amount actually **credited** in year `t`, which is the previous year's grant | annual (lag 1) |
| `mindesteigenbeitrag_pp(k)`, `eigenbeitrag_pp(k)`, `eigenbeitrag_paid_pp(k)` | The § 86 minimum; the contribution before the frequency loading; the amount actually collected | annual |
| `prem_to_av_pp(k)` | The *Sparbeitrag* — the part of the contribution credited to the account, after charges. **May be negative** in a *beitragsfrei* year | annual |
| `dk_pp(k)`, `surplus_acct_pp(k)`, `av_total_pp(k)` | *Deckungskapital*, *Überschussguthaben*, and their sum at the start of year `t` | annual recursion |
| `av_total_pp_at(k, timing)`, `av_total_at(k, timing)` | `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_INT"`; the second form is the first times `pols_if(12k)` | within year |
| `int_guar_pp(k)`, `int_surplus_pp(k)`, `int_credited_pp(k)` | Guaranteed interest at the *Rechnungszins*, declared surplus above it, and their sum | annual |
| `guar_pp(k)`, `guar_carve_out_pp(k)`, `garantieluecke_pp(k)` | The *Beitragsgarantie* accumulator; the biometric carve-out capped at 20 %; the running shortfall `max(0, guar_pp(t) − av_total_pp(t))`, a **diagnostic**, since the guarantee is tested only at *Rentenbeginn* | annual |
| `pool_gefoerdert_pp(k)`, `pool_ungefoerdert_pp(k)` | Cumulative subsidised and unsubsidised contributions credited. **Contributions only** — the model does not apportion investment return between the pools and says so | annual |
| `zulage_cum_pp(k)` | Cumulative Zulagen credited: the ZfA-reclaimable limb of the *Rückzahlungsbetrag*. A diagnostic, never netted from a benefit | annual |
| `capital_conv_pp()`, `garantieluecke_conv_pp()` | Conversion capital and the *Garantielücke* the insurer funds at *Rentenbeginn* — the product's signature output | once, at `t_conv()` |
| `ann_factor()`, `rentenfaktor_curr()`, `rentenfaktor_applied()` | `ä⁽¹²⁾` on the **first-order** annuity basis; the current factor derived from it; the higher of it and `rentenfaktor_guar` | once |
| `is_kleinbetrag()`, `teilkapital_pp()`, `annuity_capital_pp()`, `annuity_pp(k)`, `annuity_month_pp()` | The commutation test and its consequences | once |
| `db_pp(k)`, `cv_pp(k)`, `transfer_value_pp(k)`, `exit_charge_pp(t)` | Death benefit, *Rückkaufswert*, *Anbieterwechsel* transfer value, and the *Stornoabzug* plus transfer charge the insurer retains | annual |

---

## Assumption inputs

Three classes, and the split is not cosmetic: class (a) is what the contract or the statute obliges,
class (b) is what the insurer decides afresh each year, class (c) is the modeller's view. On this
product class (a) is unusually large — most of the product is statute — and class (b) is unusually
consequential, because the declared rate is what decides whether the guarantee costs anything.

### (a) Contractual and guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| *Grundzulage* | **175.00** per year — § 84 Satz 1 EStG, "ab dem Beitragsjahr 2018 jährlich 175 Euro" | [R9] [REG-R42] |
| *Kinderzulage* | **185.00** for a child born before 1 Jan 2008; **300.00** for one born on or after — § 85 Abs. 1 Sätze 1 and 2, keyed to *Kindergeld* being *festgesetzt* | [R9] [R19] [REG-R42] |
| *Berufseinsteiger-Bonus* | **200.00**, "einmalig", 25th year not completed at the start of the contribution year, first year a Zulage is claimed — § 84 Sätze 2 and 3 | [R9] [REG-R42] |
| *Mindesteigenbeitrag* rate, ceiling, floor | **4 %** of the previous year's contribution-liable earnings, capped at the § 10a Abs. 1 Satz 1 *Höchstbetrag* of **2 100.00**, less the entitlement, floored at the **60.00** *Sockelbeitrag* — § 86 Abs. 1 Sätze 2, 4 and 5 | [R10] [REG-R42] |
| Proportional Kürzung | The Zulage is reduced in the ratio of the contribution paid to the *Mindesteigenbeitrag* — never lost outright | [R10] [REG-R42] |
| Zulage cash lag | Contribution year `t` is credited by the ZfA in `t + 1`; AltvPIBV § 9 Abs. 3 prescribes **15 May of `t + 1`** for every disclosure calculation | [R5] [R11] [REG-R42]; the annual-grid compression **[std]** (1) |
| *Beitragsgarantie* | At *Rentenbeginn*, at least "die bis dahin gezahlten Beiträge und die uns zugeflossenen staatlichen Zulagen" must be available for the agreed benefits — statutory as to the test, **contractual as to the Zulagen** | [R1] [REG-R43] for the test; [S2] § 1 Abs. 10, [S4] § 1 Abs. 2, [S6] for the Zulagen limb |
| Guarantee carve-out | Biometric-rider contributions excluded, "bis zu **20 Prozent** der Gesamtbeiträge" — AltZertG § 1 Abs. 1 Satz 1 Nr. 3, drafted at [S2] § 1 Abs. 10 | [R1] [REG-R43] [S2] |
| Earliest *Rentenbeginn* | Completed **62nd** year — § 1 Abs. 1 Satz 1 Nr. 2. The **60th** for contracts concluded before 1 Jan 2012 is the transitional rule of **§ 14 Abs. 2**, not § 1 | [R1] [REG-R43] |
| *Teilkapitalauszahlung* cap | **30 %** of "des zu Beginn der Auszahlungsphase zur Verfügung stehenden Kapitals" — § 1 Abs. 1 Satz 1 Nr. 4 Buchst. a | [R1] [REG-R43] |
| Acquisition-cost spreading | "gleichmäßig mindestens auf die ersten **fünf Vertragsjahre** …, soweit sie nicht als Prozentsatz von den Altersvorsorgebeiträgen abgezogen werden" — § 1 Abs. 1 Satz 1 Nr. 8. The qualifier is why the charge on a Zulage is taken once at inflow in every retrieved wording | [R1] [REG-R43] [S2] [S4] [S6]; *Höchstzillmersatz* 25 ‰, DeckRV § 4 Abs. 1 [REG-R16] |
| *Kleinbetragsrente* threshold | **The statutory rate is 1,5 %**, not 1 %: § 93 Abs. 3 Satz 2 Nr. 1 EStG, aggregated across the saver's contracts at that provider (Satz 3). On the 3 955.00 monthly *Bezugsgröße* used here that is **59.33**. `kleinbetrag_threshold_mth` is **39.55** and is therefore **too low**; the model is unchanged | [R15] [REG-R42] [REG-R46]; the *Bezugsgröße* `[unverified]`; see (2) |
| *Rückkaufswert* floor | "mindestens der Betrag des Deckungskapitals, das sich bei gleichmäßiger Verteilung der angesetzten Abschluss- und Vertriebskosten auf die ersten fünf Vertragsjahre ergibt" — § 169 Abs. 3 VVG; satisfied by construction here, and both retrieved wordings compute it that way | [REG-R28] [S2] [S4] |
| Annuity form | Lifelong, monthly, "gleich bleiben oder steigen" over the whole payout phase; up to twelve monthly payments may be combined into one | [R1] [REG-R43] |
| Unisex | "eine lebenslange und **unabhängig vom Geschlecht berechnete** Altersversorgung" — § 1 Abs. 1 Satz 1 Nr. 2, and in the wordings at [S2] § 1 Abs. 1, [S4] § 1 Abs. 1 and a "geschlechtsunabhängige Sterbetafel" at [S6]. The **dates** — 1 Jan 2006 for Riester, 21 Dec 2012 for the general market — are `[unverified]` | [R1] [R23] [REG-R34] |

1. **Gap 6 is closed and this footnote's premise no longer holds.** § 90 Abs. 2 EStG has the ZfA pay
   the **provider**, who "hat die erhaltenen Zulagen unverzüglich den begünstigten Verträgen
   gutzuschreiben"; § 89 Abs. 1 and Abs. 3 put the application and the provider's data transmission
   in the year after the contribution year at the earliest; and **AltvPIBV § 9 Abs. 3 fixes the
   crediting date for every disclosure calculation at 15 May of that year** [R5]. Reversals are
   settled **quarterly** — § 90 Abs. 3, remittance "bis zum zehnten Tag des dem Kalendervierteljahr
   folgenden Monats" — within a two-year recognition window. What remains **[std]** is only the
   compression of a mid-May credit onto the first month of the projection year; the *frequency* of
   reversals is
   established, their *rate* is experience data and is not (gap 16).
2. **The statute settles it, and against the model.** § 93 Abs. 3 Satz 2 Nr. 1 EStG defines a
   *Kleinbetragsrente* as one that "**1,5 Prozent** der monatlichen Bezugsgröße nach § 18 des Vierten
   Buches Sozialgesetzbuch nicht übersteigt" [R15]. On the *Bezugsgröße* this file uses the threshold
   is **59,33 €**, and `kleinbetrag_threshold_mth = 39.55` is a third of the way below it. Raising it
   would make **more** contracts commute and shorten the liability, so the direction of the error is
   toward a longer tail. **This is a model change and has not been made** (see the note under
   *Model-relevant contradictions* below). Two further points stand unchanged: the threshold is held
   **flat in nominal terms** while the *Bezugsgröße* is reset annually, which understates the
   commutation rate on a long deferral (sensitivity 7); and the test is applied **after** the elected
   lump sum, which the GDV model wording forbids [S2] — also a model change, also deferred. What is
   now settled in the model's favour is that commutation is the **provider's option** [S2] [S4].

### (b) Insurer-discretionary current elements (snapshot; revisable annually)

| Input | Value | Basis |
|---|---|---|
| *Rechnungszins* | **0,25 %** on the anchor, a 2024-vintage tariff; 0,90 % on one older point | cap [R22] [REG-R14] [REG-R15]. **Two carrier choices are now established** — 1,25 % on a 01.15 tariff [S4], **0,9 %** on a 01.01.2025 tariff [S6] — but neither is the anchor's vintage, so the level stays **[std]** (3) |
| *Laufende Verzinsung* `decl_rate(t)` | Scenario path in `surplus_scenario.csv`: `base` **2,30 %** level, `low` **0,50 %** level | **[std]** (4) |
| Surplus system in accumulation | *Verzinsliche Ansammlung*: declared surplus accrues in a **second account** beside the *Deckungskapital* and bears the declared rate | market practice; level **[std]** (4) |
| *Risikoüberschuss* and *Kostenüberschuss* | **Zero** in the base run | **[std]** (5) |
| *Schlussüberschussanteil* | **2,0 %** of contributions credited, declared at *Rentenbeginn*, and **counted toward the guarantee** | **[std]** (6), gap 9 |
| *Bewertungsreserven* share | **1,0 %** of the account at *Rentenbeginn*, the *hälftige* participation of § 153 Abs. 3 VVG | [REG-R24]; level **[std]** (6) |
| Acquisition charge | **2,5 %** of `beitragssumme`, in five equal instalments in contract years 1 to 5, **whether or not contributions are paid** | [R1] [REG-R16]; level **[std]** (7) — against **1,0 % of the *Eigenbeiträge*** at the one carrier now in hand [S4] |
| Administration charge | **4,0 %** of each contribution credited, Zulagen **included**, plus a fixed **12,00** per year | Charging the Zulagen is **confirmed** [S2] [S4] [S6] [S9], gap 14 closed; the **rate** is contradicted — 2,1 % on contributions against **6,0 % on Zulagen** at [S4] — and the levels stay **[std]** (7) |
| Frequency loading | 1.0000 / 1.0100 / 1.0200 / 1.0300 for annual / half-yearly / quarterly / monthly, treated as a **charge** and never credited to the account | **[std]** (7). One scale is now observed and has a different **mechanic**: +1,0 / +2,0 / +3,0 percentage points on the administration **rate** for half-yearly / quarterly / monthly [S4] |
| *Risikobeitrag* | **Zero** — the death benefit is the account value, so there is no sum at risk | design consequence **[std]** |
| *Stornoabzug*; transfer charge | **2,0 %** of the account on surrender; **50,00** flat on an *Anbieterwechsel*, with **no** *Stornoabzug* | § 169 Abs. 5 VVG requires a deduction to be "vereinbart, **beziffert** und angemessen" [REG-R28]. **The transfer-charge ceiling is 150,00 and gap 8 closes** — AltZertG § 1 Abs. 1 Satz 3 [R1]; 50,00 is what one fund provider charges [S9] and one insurer charges nothing [S4]. Levels **[std]** (7) |
| *Rentenfaktor* margin | **30 %** off the actuarially fair factor, carrying the *Sicherheitsabschlag* and the whole payout-phase loading | **[std]** (8). The construction — per 10 000 €, monthly, higher of guaranteed and current — is now established in a Riester wording [S6]; the **margin** is not |
| Annuitisation interest basis | **1,00 %**, the *Höchstrechnungszins* in force from 1 January 2025 | [REG-R15]; use of the cap **[std]** (8) |

3. The *Höchstzinssatz* caps the rate at which the **Deckungsrückstellung** is computed, not the rate
   a policy guarantees [R22] [REG-R14]; a tariff may guarantee less, and DeckRV § 2 Abs. 2 fixes
   whatever rate was used at conclusion "für die gesamte Laufzeit des Vertrages", which is why
   `rechnungszins` is a model point attribute. **A retrieved wording now proves the "may guarantee
   less" limb**: Debeka's 1 January 2025 Riester tariff uses **0,9 %** where the cap of that vintage
   is 1,00 % [S6]. Using the cap of the vintage remains the highest defensible value and so makes the
   guarantee **cheapest**; a lower tariff rate widens the *Garantielücke*.
4. **No declared rate was established for any Riester tariff at any carrier** (gap 12). 2,30 % is a
   round number in the region German life insurers declared in the mid-2020s [REG-R53]
   `[unverified]`, and 0,50 % is a stress, not a forecast. This is the single most consequential
   **[std]** in the file, because — as the product spec argues — **the guarantee's realised cost is
   a declared-rate question, not a *Rechnungszins* question**, and model point 11 exists to make
   that visible.
5. The accumulation-phase risk result is nil by construction here (no sum at risk), and no cost
   result was established. Setting both to zero keeps the surplus mechanic to the one component the
   corpus does establish, the *Zinsüberschuss*, and states the omission rather than burying it.
6. **Which surplus components may close a guarantee shortfall is still not established** (gap 9),
   and this pass can now say precisely why rather than merely that. AltZertG § 1 Abs. 5 does define
   the *gebildetes Kapital* for an insurance contract as the *Deckungskapital* "zuzüglich bereits
   zugeteilter Überschussanteile, des übertragungsfähigen Werts aus Schlussüberschussanteilen sowie
   der nach § 153 Abs. 1 und 3 des Versicherungsvertragsgesetzes zuzuteilenden Bewertungsreserven"
   [R1] — but that definition governs the **transfer** value, and the guarantee of § 1 Abs. 1 Satz 1
   Nr. 3 speaks only of what must "für die Leistungserbringung zur Verfügung stehen". The GDV model
   wording repeats the guarantee without naming components [S2] § 1 Abs. 10, and uses the § 1 Abs. 5
   list only for the transfer value at its own § 11 Abs. 2. So the retrieved documents are **silent
   on the point** rather than absent, which is a different and more useful kind of gap. The model
   counts all of them, the provider-favourable reading; counting only the vested *Deckungskapital*
   and *Überschussguthaben* raises the projected guarantee cost, and that variant is sensitivity 4.
7. **Charge figures now exist, and this footnote's premise is withdrawn.** One complete tariff basis
   is in hand — CosmosDirekt LA 1005 A § 11 [S4]: acquisition **1,0 % of the *Eigenbeiträge*** spread
   over at least five years; administration **2,1 %** of each *Eigenbeitrag*, **2,1 %** of capital
   transferred in and **6,0 % of each Zulage**; a sub-annual loading of +3,0 / +2,0 / +1,0 percentage
   points; **0,13 %** of the accumulated *Beitragssumme* taken monthly pro rata from the
   *Deckungskapital*, also when paid up; **1,5 %** of the annual annuity in payment; and **nil**
   *Stornoabzug* and **nil** transfer charge. Two disclosed totals are in hand too — *Effektivkosten*
   of **1,45** and **1,33 Prozentpunkte** at a fund house [S9]. Every level in this table nonetheless
   stays **[std]**, for a changed reason: **one tariff is not a range**, and the one observation
   differs from the composite in level, in base and in mechanic. It is recorded here so that the next
   calibration starts from a document rather than from a round number.
8. German market *Rentenfaktoren* sit materially below the actuarially fair factor — a proposition
   the 0,1 % interest basis behind Debeka's guaranteed factor makes concrete [S6]. Rather than deduct
   a percentage from each annuity payment **and** apply a conservative factor, which double-counts,
   the whole loading sits in the factor, and the insurer's real payout-phase administration is a
   per-policy expense cash flow — **which is not what the market does**: AltZertG § 2a Satz 1 Nr. 1
   Buchst. f permits a charge as a percentage of the benefit paid and one carrier levies 1,5 % of the
   annual annuity [S4]. The consequence to check is unchanged: `rentenfaktor_curr()` and the annuity
   table are **consistent by construction** while `rentenfaktor_guar` is an independent contract
   term, and the **higher** applies when they disagree. **That rule is no longer [std] by default** —
   Debeka drafts it in terms, "Die höhere Rente wird ausgezahlt (Günstigerprüfung)" [S6] — but the
   **level** of both factors is, and the design is not universal: neither the GDV model wording nor
   the CosmosDirekt wording uses a *Rentenfaktor* at all [S2] [S4] (gap 9).

### Model-relevant contradictions found in the 2026-08-30 provenance pass

**Three retrieved documents contradict rules this model implements. None of them has been applied,
because each is a model change: it moves the worked example below and the golden tests with it.**
They are set out here so that a reader of the anchor's numbers knows which of them rest on a rule the
documents now show to be wrong.

| What the model does | What the retrieved document says | Direction of the error |
|---|---|---|
| `kleinbetrag_threshold_mth = 39.55`, being **1 %** of the monthly *Bezugsgröße* | § 93 Abs. 3 Satz 2 Nr. 1 EStG: "eine monatliche Rente …, die **1,5 Prozent** der monatlichen Bezugsgröße nach § 18 des Vierten Buches Sozialgesetzbuch nicht übersteigt" [R15]. On the 3 955,00 € used here, **59,33 €** | The threshold is **a third too low**, so **too few** model points commute and the projected liability is **too long-tailed**. Model points 4, 5, 10 and 13 already commute; on a 59,33 € threshold others would join them |
| `is_kleinbetrag()` tests the annuity payable **after** the elected *Teilkapitalauszahlung* | [S2] § 1 Abs. 3: "**Eine Abfindung erfolgt nicht, wenn die Leistung nur aufgrund einer Teilkapitalauszahlung gemäß Absatz 4 auf eine Kleinbetragsrente sinkt.**" The test belongs on the annuity the whole conversion capital would buy | The test trips **less often** than the wording allows, in the same direction as the threshold error and compounding it on any point that elects the 30 % lump sum |
| Administration charge of **4,0 %** applied to the *Eigenbeitrag* and the Zulage **at the same rate** | [S4] § 11 Abs. 2: **2,1 %** of each *Eigenbeitrag* and **6,0 %** of each Zulage — the Zulagen charged at nearly three times the rate | The composite **undercharges** the Zulagen relative to the one tariff observed, which matters most on the low-income cells where the Zulagen are the majority of the contribution |

Two further differences are **not** contradictions but are worth recording beside them: the model's
frequency loading is a multiplicative factor on the contribution where the observed one is an
addition to a charge rate [S4]; and the model's flat 2,0 % *Stornoabzug* cannot express the
interest-linked market-value adjustment one carrier uses [S6]. Both are **[std]** choices whose
mechanic, not only whose level, now has an observed alternative.

### (c) Behavioural and experience assumptions (the modeller's view)

**Every input in this class is [std]. No behavioural rate was established for any German Riester
book, for any year** — no *Stornoquote*, no *Beitragsfreistellung* rate, no transfer-out rate, no
commutation take-up (gap 16). Each rationale below is an argument from the statutory consequences,
not from data.

| Input | Value | Rationale |
|---|---|---|
| Accumulation mortality `mort_table_accum.csv` | **[std]** proxy standing in for **DAV 2008 T** [REG-R48], applied with `mort_be_factor = 0.80` | The DAV tables are proprietary and **not redistributed** [REG-R47]. A death-benefit basis carries **no** improvement projection, because for death cover improvement favours the insurer |
| Annuity mortality `annuity_mort_table.csv` | **[std]** **generational** proxy standing in for **DAV 2004 R** [REG-R49]: `q(x, τ) = qx_base(x) · (1 − improvement(x))^(τ − 2027)`, applied with `annuity_mort_be_factor = 1.15` | The one structural property that is **not optional** is that the basis is two-dimensional in age and calendar year; a period-table proxy understates a twenty-year-deferred annuitisation by a margin that dwarfs every other assumption [REG-R49] |
| Why two factors, in opposite directions | 0.80 on the death basis, 1.15 on the annuity basis | The direction of prudence **forks by product** [REG-R47]: a first-order death table assumes mortality **higher** than expected, a first-order annuity table **lower**. The best estimate therefore sits below the one and above the other |
| Surrender `lapse_rate(t)` | **0,8 %** p.a. at contract durations 1–5, **0,6 %** at 6–10, **0,4 %** from 11 | Materially **below** a Schicht-3 rate, because a *Kündigung* repays all Zulagen and all § 10a relief (§ 93 Abs. 1 Satz 1) and taxes the growth (§ 22 Nr. 5 Satz 3) [R14] [REG-R42], and because EStG § 97 makes the subsidised capital non-transferable and ZPO § 851 Abs. 1 therefore unattachable [R16] [REG-R40] |
| Transfer out `transfer_rate(t)` | **1,2 %** p.a. at durations 1–5, **0,9 %** at 6–10, **0,6 %** from 11 | Set **above** surrender, because the *Wechselrecht* is free of subsidy consequences (§ 93 Abs. 2 Satz 1 EStG) [R1] [R14] and is therefore the rational exit; the ceding provider may charge at most 150,00 € for it and one retrieved insurer charges nothing [S4]. A model carrying only a lapse rate has mis-specified the book |
| *Beitragsfreistellung* | A **model-point switch** (`bfs_year`), not a decrement | (9) |
| Income growth | **2,0 %** p.a. on the anchor's `income_schedule` path | A round real-plus-inflation number; it decides when the 2 100 € ceiling binds and so the shape of the contribution stream |
| Commutation take-up | **Computed, not assumed** — the model tests the annuity against the threshold | The one behavioural quantity here that does not need a rate |
| *Teilkapitalauszahlung* take-up | **30 %** on the anchor, 0 % on model point 12 | German commentary reports the lump sum as usual `[unverified]`; **gap 10 records that this rests on nothing** |
| Expenses `expense_maint`, `expense_annuity`, `expense_claim`, `expense_acq` | **30.00** p.a. per in-force policy inflating at **2,0 %**; **24.00** p.a. per annuitant; **80.00** per claim; **150.00 + 2,0 %** of `beitragssumme` at issue | No German insurer publishes a unit cost. The per-policy maintenance figure carries the Zulage administration — the *Dauerzulageantrag* (§ 89 Abs. 1a), the annual data transmission (§ 89 Abs. 3), the quarterly reclaim remittance (§ 90 Abs. 3), the *Leistungsmitteilung* (§ 22 Nr. 5 Satz 7, due on first receipt and on change rather than annually) and the separate annual information duty of AltZertG § 7a [R4] [R11] [R12] — which is a real and product-specific cost |
| Commission | **2,5 %** of `beitragssumme` at issue, **1,5 %** of contributions thereafter | The initial rate is set at the *Höchstzillmersatz* [REG-R16] [REG-R20]. **The cash leaves at issue while the charge is recovered over five years** [R1]; that gap is the new-business strain and it is carried by the insurer |

9. ***Beitragsfreistellung* is the German Riester book's dominant exit** [R25], and the model
   represents it as a **switch on the model point** rather than as a decrement. The reason is
   structural, not laziness: a paid-up policy and a premium-paying one have **different account
   values and different guarantee accumulators** from the moment they diverge, so a
   *Beitragsfreistellung* **rate** would require the projection to carry two account values and two
   guarantee accumulators per model point, and then four, and so on. A scalar single-model-point
   projection cannot do that without doubling every recursion. The honest representation is a
   dedicated model point (10) that goes paid-up at `t = 3`, plus this statement that a real book
   needs a paid-up cohort split. It is listed again under *Key sensitivities*.

---

## Cash flow components and recursions

### Notation, defined once and used throughout

| Symbol | Cells | Meaning |
|---|---|---|
| `t` | — | Projection **month**, **0-based**: `t = 0 … 12n − 1`, `12n = proj_len()` |
| `k`, `n` | `proj_year(t)`, `proj_len_y()` | Projection **year**, `t // 12`, **0-based**: `k = 0 … n − 1`; the contractual contract year is `d(k) + 1 = duration_init + k + 1`, which is `k + 1` only on a point projected from its own inception (`duration_init = 0`) |
| `T` | `k_conv()` | The conversion year; `12T = t_conv()` is the conversion month |
| `x(k)`, `τ(k)`, `d(k)` | `age_y`, `calendar_year_y`, `duration_y` | Attained age, calendar year, completed contract years at the **start** of projection year `k`, all stepping on the anniversary (so `d` is 0-based; the contract-year band is `d(k) + 1`). `age(t)`, `calendar_year(t)` and `duration(t)` read the same three from a month |
| `l(t)` | `pols_if(t)` | Policies in force at the **start** of month `t`; `l(0) = pols_if_init()` |
| `q(t)`, `w(t)`, `θ(t)` | `mort_rate`, `lapse_rate`, `transfer_rate` | **Annual** decrement rates of the year month `t` falls in |
| `q_mth`, `w_mth`, `θ_mth` | `mort_rate_mth`, `lapse_rate_mth`, `transfer_rate_mth` | Their geometric twelfths — **the rates the recursion applies** |
| `Y(k)`, `E(k)` | `income_ref(k)`, `eigenbeitrag_pp(k)` | Reference income; the *Eigenbeitrag* before the frequency loading |
| `M(k)` | `mindesteigenbeitrag_pp(k)` | The § 86 minimum own contribution |
| `Z*(t)`, `Ẑ(t)`, `Z(t)` | `zulage_entitlement_pp`, `zulage_granted_pp`, `zulage_pp` | Full entitlement; entitlement after the Kürzung; the amount **credited** in year `t` |
| `φ` | `prem_freq_load` | Frequency loading, a **charge** and not a credit |
| `C(k)` | `contrib_total_pp(k)` | `E(k) + Z(k) + contrib_extra_pp` while in accumulation |
| `K_a(k)`, `K_v(k)` | `acq_charge_pp`, `admin_charge_pp` | Acquisition and administration charges |
| `S(k)` | `prem_to_av_pp(k)` | The *Sparbeitrag*, `C(k) − K_a(k) − K_v(k)`; **may be negative** |
| `D(k)`, `U(k)`, `A(k)` | `dk_pp`, `surplus_acct_pp`, `av_total_pp` | *Deckungskapital*, *Überschussguthaben*, and `A = D + U` |
| `i`, `j(k)` | `rechnungszins`, `decl_rate(k)` | Guaranteed rate; declared *laufende Verzinsung*, with `j ≥ i` |
| `G(k)`, `κ(k)` | `guar_pp`, `guar_carve_out_pp` | The *Beitragsgarantie* accumulator; the biometric carve-out |
| `Λ` | `garantieluecke_conv_pp()` | The *Garantielücke* funded at *Rentenbeginn* |
| `V` | `capital_conv_pp()` | The conversion capital |
| `ä` | `ann_factor()` | `ä⁽¹²⁾(x(T), τ(T))` on the **first-order** annuity basis at `annuity_rechnungszins` |
| `R`, `R_g`, `R_c` | `rentenfaktor_applied`, `rentenfaktor_guar`, `rentenfaktor_curr` | Applied, guaranteed and current *Rentenfaktor* |
| `a(k)` | `annuity_pp(k)` | The **annual** annuity, a reporting figure: twelve monthly instalments |
| `a(k)/12` | `annuity_month_pp()` | The monthly instalment, which is what is paid |

### The subsidy chain

The whole chain is **annual** and takes `k`: the entitlement is determined per contribution year
and the ZfA pays the provider once, in the following one.

    Y(k)   = income_init                       for k = 0
           = income(k − 1) from income_schedule for k ≥ 1

    Z*(k)  = 175·unmittelbar(k) + 185·n_pre(k) + 300·n_post(k) + 200·bonus(k)
    M(k)   = max( 60 , min( 0.04 · Y(k) , 2 100 ) − Z*(k) )
    E(k)   = contrib_ratio · M(k)        (contrib_form = mindest)
           = contrib_fixed_pp            (contrib_form = fixed)
           = 0                           (k ≥ bfs_year ≥ 0, or k ≥ T)
    Ẑ(k)   = Z*(k) · min( 1 , E(k) / M(k) )
    Z(k)   = zulage_init_pp   for k = 0;   Ẑ(k − 1)   for 1 ≤ k ≤ T;   0 for k > T

On the monthly frame both the *Eigenbeitrag* and the Zulage fall in the **first month** of the
projection year — `prem_due(t)`, `t % 12 == 0` — and in no other: the *Ratenzuschlag* prices a
fractionated payment mode by loading the amount rather than by moving the contribution year, and
the ZfA does not fractionate at all.

**Two lags, and they are different lags.** `Y(k)` looks back one calendar year because the statute
says the base is the previous year's earnings [R10]; `Z(k)` looks back one projection year because
the ZfA pays in arrear [R11]. Collapsing them into one is pitfall 1. Note also that `Z(T)` is
**non-zero** — the final contribution year's Zulage lands in the conversion year and must be
credited, guaranteed and converted before the guarantee is tested (pitfall 2).

### Contributions, charges and the *Sparbeitrag*

All of it is **annual** and takes `k`: one contribution, two charges, one *Sparbeitrag* a year.

    B(k)   = E(k) + Z(k) + contrib_extra_pp · 1{is_accum_y(k)}      charge base, unloaded
    C(k)   = E(k)·φ + Z(k) + contrib_extra_pp · 1{is_accum_y(k)}    cash actually received
    K_a(k) = acq_charge_rate · beitragssumme / 5      if d(k) < 5 and k ≤ T, else 0
    K_v(k) = admin_charge_prem_rate · B(k) + admin_charge_fixed + E(k)·(φ − 1)
    S(k)   = C(k) − K_a(k) − K_v(k)
           = B(k) − K_a(k) − admin_charge_prem_rate · B(k) − admin_charge_fixed

`E(k)·(φ − 1)` is the frequency loading: the saver pays `E(k)·φ` and only `E(k)` reaches the
*Sparbeitrag* base, so the loading is a charge and never enlarges the account or the guarantee
(pitfall 11). **`C(k)` is the cash received and therefore carries the loading, which `K_v(k)`
then takes straight back out; the administration charge's percentage base `B(k)` is the
unloaded contribution.** The second line above is the algebraic consequence: `S(k)` is
independent of `φ`, which is what pitfall 11 asserts — and it is why the contribution keeps the
annual grid on a monthly frame, φ pricing a fractionated mode by loading the amount rather than
by moving the contribution year. An earlier draft of these notes wrote
`S = C − K_a − K_v` with an **unloaded** `C` and a `K_v` that already carried `E(φ − 1)`, and so
deducted the loading twice; see *Changes the model stage made to these notes*. `K_a` continues for its five contract years **whether or not contributions are paid**,
so on a *beitragsfrei* contract `S(k)` is negative and the *Deckungskapital* falls — which is the
mechanic model point 10 exists to show. The administration charge falls on the **Zulagen as well as
the *Eigenbeitrag***, and **gap 14 is closed**: German tariffs do charge them. The GDV model wording
permits a charge on "jeder Zulage und Zuzahlung" and takes the acquisition-cost element "einmalig zum
Zeitpunkt des Zuflusses" [S2]; Debeka drafts the same [S6]; Union Investment discloses acquisition
cost as a percentage "der eingezahlten Beiträge (inkl. Zulagen)" [S9]; and CosmosDirekt puts a number
on it, **6,0 %** of each Zulage against **2,1 %** of each *Eigenbeitrag* [S4]. **The model charges
both at the same rate, which that one observation contradicts** — see *Model-relevant contradictions*
above. It is material for the reason the note always gave: in the low-income cases the Zulagen are
the majority of `C(k)`. The model's **[std]** is now a level, not a structural guess.

### The account: two balances, one credited rate

Both balances are **annual**, credited once a *Versicherungsjahr*, and take `k`.

    D(0) = dk_pp_init,  U(0) = surplus_pp_init,  A(k) = D(k) + U(k)

    int_guar_pp(k)    = i · ( D(k) + S(k) )
    int_surplus_pp(k) = ( j(k) − i ) · ( D(k) + S(k) )  +  j(k) · U(k)
    int_credited_pp(k)= int_guar_pp(k) + int_surplus_pp(k)

    D(k + 1) = ( D(k) + S(k) ) · ( 1 + i )
    U(k + 1) = U(k) + int_surplus_pp(k)
    A(k + 1) = A(k) + S(k) + int_credited_pp(k)

The split is **guarantee accounting, not two investment strategies**: the whole account grows at
`j(k)`, and `D` is carved out of it as the part the *Rechnungszins* guarantees. The German
arithmetic error this prevents is adding the declared *laufende Verzinsung* **to** the
*Rechnungszins*: `j` already **includes** `i`, and `j − i` is the *laufende
Zinsüberschussbeteiligung* [REG-R53] (pitfall 10). Within-year points are
`av_total_pp_at(k, "BEF_PREM") = A(k)`, `av_total_pp_at(k, "AFT_PREM") = A(k) + S(k)` and
`av_total_pp_at(k, "AFT_INT") = A(k + 1)`, with
`av_total_at(k, timing) = av_total_pp_at(k, timing) · l(12k)` — the count at the **start of the
year**, which is where the contribution is credited.

### The *Beitragsgarantie* accumulator

Annual, like the contributions it counts, and never accruing: the guarantee is nominal.

    κ(k) = min( rider_prem_pp , 0.20 · ( E(k) + Z(k) + contrib_extra_pp + rider_prem_pp ) )
    G(0) = guar_pp_init
    G(k + 1) = G(k) + E(k) + Z(k) + contrib_extra_pp·1{is_accum_y(k)} − κ(k)   for k ≤ T
             = G(T + 1)                                                        for k > T

    garantieluecke_pp(k) = max( 0 , G(k) − A(k) )      diagnostic only

Three things this encodes and a test asserts. The accumulator counts **Zulagen credited**, in the
year they are credited, not entitlements in the year they are earned [R1]. It counts
**unsubsidised** contributions too, because the guarantee is on the *Altersvorsorgebeiträge* paid in
and does not distinguish the pools [R1] (pitfall 9). And the biometric carve-out is **capped at
20 % of total contributions** [REG-R43], so raising `rider_prem_pp` beyond the cap does **not**
shrink the guarantee further (pitfall 8). `garantieluecke_pp(k)` is published because it is
positive in the early durations of any charged contract and closes later — a fact about the product
that a reader should see — but it is a diagnostic: **the guarantee is tested once, at `T`**.

### Conversion at *Rentenbeginn*

    account_conv_pp() = D(T) + S(T) + U(T) + slueb_pp() + bewres_pp()
    slueb_pp()        = slueb_rate · ( G(T + 1) − guar_pp_init + contributions credited before t = 0 )
    bewres_pp()       = bewres_rate · ( D(T) + S(T) + U(T) )
    V                 = max( account_conv_pp() , G(T + 1) )
    Λ                 = max( 0 , G(T + 1) − account_conv_pp() )

    ä    = Σ_{k ≥ 0} v^k · k p( x(T), τ(T) )  −  11/24,     v = 1 / (1 + annuity_rechnungszins)
    R_c  = ( 1 − rentenfaktor_margin ) · 10 000 / ( 12 · ä )
    R    = max( R_g , R_c )

    monthly test annuity  = ( 1 − teilkapital_share ) · V / 10 000 · R
    is_kleinbetrag()      = monthly test annuity ≤ kleinbetrag_threshold_mth

    if is_kleinbetrag():  teilkapital_pp() = 0 ; annuity_capital_pp() = 0 ; commutation_pp() = V
    else:                 teilkapital_pp() = teilkapital_share · V ;
                          annuity_capital_pp() = V − teilkapital_pp() ; commutation_pp() = 0

    annuity_month_pp() = annuity_capital_pp() / 10 000 · R       the instalment, paid monthly
    a(k)               = 12 · annuity_month_pp()   for is_payout_y(k) and not commuted

`k p(x, τ)` is survivorship on the **first-order** annuity basis — the same basis the market's
*Rentenfaktor* is struck on — while the projection's own survivorship uses the **second-order**
basis, `annuity_mort_rate(x, τ) · annuity_mort_be_factor`. The wedge between them is the
*Risikoüberschuss* in payment [REG-R47], which this model does not distribute (assumption class (b),
footnote 5). The commutation test is applied to the annuity **actually payable after the elected
lump sum**. The statute does not settle the point, but **the GDV model wording does, and against this
reading**: "Eine Abfindung erfolgt nicht, wenn die Leistung nur aufgrund einer Teilkapitalauszahlung
gemäß Absatz 4 auf eine Kleinbetragsrente sinkt" [S2] § 1 Abs. 3. The alternative — testing the
annuity the whole capital would buy — is therefore the drafted rule rather than merely a variant, and
it remains sensitivity 6 because changing it is a model change (gap 7). If the contract commutes there is **no** *Teilkapitalauszahlung*: the whole capital is one
payment. `a(k)` is a reporting figure and nobody's payment: the *Rentenfaktor* is quoted in euro a
**month**, and what the contract pays — and the model books — is `annuity_month_pp()`, one
instalment at a time.

### Decrements

The ledger is **monthly** and the rates it applies are the geometric twelfths of the year's annual
ones, `q_mth = 1 − (1 − q)^(1/12)` and likewise for `w` and `θ`:

    Accumulation (t < 12T):
      pols_death(t)    = l(t) · q_mth(t)
      pols_lapse(t)    = l(t) · ( 1 − q_mth(t) ) · w_mth(t)
      pols_transfer(t) = l(t) · ( 1 − q_mth(t) ) · ( 1 − w_mth(t) ) · θ_mth(t)
      l(t + 1)         = l(t) − pols_death(t) − pols_lapse(t) − pols_transfer(t)

    Payout (t ≥ 12T):
      pols_death(t)    = l(t) · q_mth(t) ;  pols_lapse(t) = pols_transfer(t) = 0
      l(t + 1)         = l(t) − pols_death(t)          and 0 at t = 12T if commuted

    pols_conv()          = l(12T)
    pols_annuity_pay(t)  = pols_conv()   if 0 ≤ t − 12T < 12 · rentengarantie_years
                         = l(t)          otherwise

with `q(t) = mort_rate_at_age(x(t)) · mort_be_factor` in accumulation and
`annuity_mort_rate(x(t), τ(t)) · annuity_mort_be_factor` in payout, and `q(t) = 1` at `x = omega_age`
so the closure identity closes exactly — the certainty falling in the terminal year's **last month**.
Twelve geometric twelfths compound back to each annual rate exactly, so `l(12k)` is the annual-step
model's `l(k)` to the last bit; `q(t)/12` would close nothing.

The lapse and transfer decrements are applied **in that
order to the survivors of mortality**, a stated **[std]** ordering — now within each **month**
rather than once at a year end. That is the one thing the finer grid changes about the exits: in the
annual model mortality took the whole cohort as its base and the transfer took what two decrements
had already thinned, while month by month the three **compete**. The survivorship at every
anniversary is unchanged and only the split moves — 5,62 € off the anchor's death outgo and 2,64 €
off its surrender outgo onto 8,30 € of transfers.

`pols_annuity_pay` is the whole
of the *Rentengarantiezeit*, now measured in ``12m`` **instalments**: the guarantee period changes
**who is paid**, never **how much** (pitfall 17).

### Benefits, expenses and the cash flow statement

The per-policy benefit amounts are **annual**, struck at the end of the contract year where the
account is struck; the cash flows that pay them are **monthly**, with `k = proj_year(t)`.

    db_pp(k)            = A(k + 1)                                    death, gross
    cv_pp(k)            = A(k + 1) · ( 1 − stornoabzug_rate )         surrender, gross
    transfer_value_pp(k)= max( 0 , A(k + 1) − transfer_charge )       Anbieterwechsel
    exit_charge_pp(t)   = stornoabzug_rate · A(k + 1) · pols_lapse(t)
                          + min( transfer_charge, A(k + 1) ) · pols_transfer(t)

    claims(t, "DEATH")       = db_pp(k) · pols_death(t)
    claims(t, "LAPSE")       = cv_pp(k) · pols_lapse(t)
    claims(t, "TRANSFER")    = transfer_value_pp(k) · pols_transfer(t)
    claims(t, "LUMPSUM")     = teilkapital_pp() · pols_conv()        at t = 12T only
    claims(t, "COMMUTATION") = commutation_pp() · pols_conv()        at t = 12T only
    claims(t, "ANNUITY")     = annuity_month_pp() · pols_annuity_pay(t)

    premiums(t)   = ( E(k)·φ + contrib_extra_pp·1{is_accum_y(k)} ) · l(t)   if prem_due(t), else 0
    zulagen(t)    = Z(k) · l(t)                                             if prem_due(t), else 0
    expenses(t)   = expense_acq · 1{t = 0 and duration_init = 0}
                    + expense_maint / 12 · (1 + expense_infl)^d(t) · l(t) · 1{is_accum(t)}
                    + expense_annuity / 12 · pols_annuity_pay(t)
                    + expense_claim · ( pols_death(t) + pols_lapse(t) + pols_transfer(t) )
    commissions(t)= comm_rate_init · beitragssumme · l(0) · 1{t = 0 and duration_init = 0}
                    + comm_rate_renew · ( E(k) + Z(k) ) · l(t)   in the month the contribution falls

    net_cf(t)     = premiums(t) + zulagen(t)
                    − claims_death(t) − claims_lapse(t) − claims_transfer(t)
                    − claims_lumpsum(t) − claims_commutation(t) − claims_annuity(t)
                    − expenses(t) − commissions(t)
    liability_cf(t) = − net_cf(t)

**Death and surrender benefits are published gross of the *Rückzahlungsbetrag***: the provider
withholds all Zulagen and all § 10a relief and remits them to the ZfA [R14], but that is a **tax
collection, not a reduction in the insurer's obligation**, and netting it would understate the outgo
(pitfall 18). `zulage_cum_pp(k)` publishes the reclaimable Zulage limb as a diagnostic; the § 10a
limb depends on the saver's marginal rate and cannot be computed from contract data at all.

A per-**event** cost such as `expense_claim` falls whole in the month of the event; a per-**year**
cost is a twelfth in each month, so a policy exiting in the fourth month of a contract year bears
four twelfths of that year's maintenance rather than all of it.

**`result_cf()` returns a `DataFrame` indexed by the projection month `t`
(`df.index.name == "t"`), contiguous, `0 … proj_len() − 1`, so it carries `proj_len()` rows, with
these columns in this order:**

    pols_if, pols_annuity_pay, premiums, zulagen,
    claims_death, claims_lapse, claims_transfer, claims_lumpsum, claims_commutation,
    claims_annuity, expenses, commissions, net_cf, liability_cf

`int_credited` is a **state movement, reported and not summed into `net_cf`** — money moving inside
the account, not across the insurer's boundary — and on the monthly grid it is not a column of this
frame at all: it moves once a *Versicherungsjahr*, like the two balances it moves between, so it
lives in `result_acct()` with them. `result_cf_annual()` sums the frame into projection years and is
the view this worked example prints. The separation of `zulagen` from `premiums` is the
single most important reporting decision in this model: **the Zulage is a contribution with a
different payer** [R8], and a statement that folds it into `premiums` cannot answer the one question
the product is about.

### The check identities the model publishes

**The residual's argument follows its cells' clock.** Two take a **month** and four a projection
**year**, because the account, the guarantee accumulator, the conversion and the ZfA lag move once a
*Versicherungsjahr* and have nothing to say about a month.

| Check | Clock | Identity |
|---|---|---|
| **`check_net_cf()`** (delib ruling 1) | month | On `result_cf()` row `t`: `net_cf` equals `premiums + zulagen` less the six `claims_*` less `expenses` less `commissions`, every term read from the **published frame** rather than from the cells behind it, for every `t`; residual at `check_net_cf_resid(t)`. `int_credited` is outside the identity and is not even a column of the frame |
| `check_pols_roll_fwd()` | month | The decrement recursion closes each **month**, at the monthly rates, and `Σ(pols_death + pols_lapse + pols_transfer) + pols_conv()·1{is_kleinbetrag()} + pols_if(proj_len()) = pols_if_init()`, the last term being the one index beyond the frame. The commuted cohort is a fourth exit: a *Kleinbetragsrenten-Abfindung* discharges the contract, so `pols_if(t_conv()+1) = 0` without any decrement having removed the population |
| `check_av_roll_fwd()` | year | `av_total_at(k+1, "BEF_PREM") = av_total_at(k, "BEF_PREM") + prem_to_av_pp(k)·l(12k) + int_credited(k) − Σ_months (claims_death + claims_lapse + claims_transfer + exit_charge)` for `k < k_conv()`, and `av_total_pp(k) = 0` for `k > k_conv()`. It closes **whatever the split** of the year's exits between the three decrements, all three releasing the same annual end-of-year account value |
| `check_guar_roll_fwd()` | year | `guar_pp(k+1) = guar_pp(k) + eigenbeitrag_pp(k) + zulage_pp(k) + contrib_extra_pp − guar_carve_out_pp(k)` while `k ≤ k_conv()`, frozen thereafter, and `guar_carve_out_pp(k) ≤ 0.20 ×` total contributions |
| `check_conversion()` | year | `capital_conv_pp() = max(account_conv_pp(), guar_pp(k_conv()+1))`; `capital_conv_pp() = teilkapital_pp() + annuity_capital_pp() + commutation_pp()`; `rentenfaktor_curr() · 12 · ann_factor() = (1 − rentenfaktor_margin) · 10 000`, the identity that ties the current factor to the annuity basis whether or not it is the factor applied; and `12 · annuity_month_pp() = annuity_pp(k)`, so an annual amount cannot reach a monthly frame by accident |
| `check_zulage_lag()` | year | `zulage_pp(0) = zulage_init_pp`, `zulage_pp(k) = zulage_granted_pp(k−1)` for `1 ≤ k ≤ k_conv()`, and `zulage_pp(k) = 0` thereafter |

Each returns a **`bool`** over the whole projection and has a `check_*_resid` companion, and the
conventions suite calls all six on **every** model point.

---

## Processing order

The order is stated per *Versicherungsjahr*, because that is the order the **contract** happens in;
the months sit inside it. For `k = 0 … proj_len_y() − 1`, and within each year for
`t = 12k … 12k + 11`, in this order. The order is a **[std]** decision — no source in this
corpus fixes the ordering of premium credit, charge deduction and interest accrual inside a period —
and it is stated here so that an implementation can be compared against it line by line.

1. Set `x(k)`, `d(k)`, `τ(k)`. Decide `is_accum_y(k)` / `is_payout_y(k)` from `k_conv()`, take the
   year's annual rates `q(12k)`, `w(12k)` and `θ(12k)`, and form their geometric twelfths.
2. **Accumulation only.** Read `Y(k)` — `income_init` at `k = 0`, otherwise the schedule's
   `income(k − 1)`. Compute the entitlement `Z*(k)` from the Zulage schedule and the statutory
   rates, then `M(k)`, then `E(k)` from the contribution form, `bfs_year` and `contrib_ratio`, then
   the granted entitlement `Ẑ(k)`.
3. **Credit the Zulage earned last year**: `Z(k) = zulage_init_pp` at `k = 0`, else `Ẑ(k − 1)`. This
   happens **before** anything else touches the account, and it happens in the conversion year too.
4. Form `C(k)`, deduct `K_a(k)` and `K_v(k)`, and credit the *Sparbeitrag* `S(k)` to the account:
   `av_total_pp_at(k, "AFT_PREM") = A(k) + S(k)`. Collect `premiums(t)` and `zulagen(t)` on `l(t)`
   in the year's **first month**, `t = 12k`, and in no other: a fractionated payment mode is priced
   by loading the amount, and the ZfA pays once a year.
5. Roll the guarantee accumulator: `G(k + 1) = G(k) + E(k) + Z(k) + contrib_extra_pp − κ(k)`, and
   the two contribution pools alongside it.
6. Charge the insurer's own expenses and commission: the acquisition expense and initial commission
   at `t = 0` on a point issued at the valuation date, the renewal commission in the month the
   contribution falls, and a **twelfth** of the annual per-policy maintenance in each month.
7. **If `k = k_conv()`**: strike `account_conv_pp()`, `V`, `Λ`; compute `ä`, `R_c`, `R`; apply the
   *Kleinbetragsrente* test; pay `claims_lumpsum` or `claims_commutation` on `pols_conv()` at
   `t = t_conv()`; and fix the instalment `annuity_month_pp()`. The account is extinguished —
   `av_total_pp(k) = 0` for `k > k_conv()`. **Nothing in steps 8 and 9 applies to the account after
   this point.**
8. **Accumulation only, end of year.** Credit interest: `int_guar_pp(k)` at `i` and
   `int_surplus_pp(k)` at `j(k) − i` on `D(k) + S(k)`, plus `j(k)` on `U(k)`;
   `av_total_pp_at(k, "AFT_INT") = A(k + 1)`. A policy that exited during the year has been credited
   the whole of it, which is the annual-step convention preserved.
9. **Accumulation, end of each month.** Apply the decrements to `l(t)`: mortality first, then
   surrender on the survivors, then transfer on the survivors of both, all three at the monthly
   rates. Strike `claims_death`, `claims_lapse` and `claims_transfer` on the **annual** `A(k + 1)`,
   and retain `exit_charge_pp(t)`.
10. **Payout, each month.** Pay `claims_annuity(t) = annuity_month_pp() · pols_annuity_pay(t)` in
    advance, charge a twelfth of `expense_annuity` on the same count, then apply annuitant mortality
    at the end of the month: `l(t + 1) = l(t) · (1 − q_mth(t))`.
11. Assemble `expenses(t)`, `commissions(t)`, `net_cf(t)` and `liability_cf(t)`, in every month.

At `t = proj_len() − 1` the projection ends: `q` is 1 in the terminal year and `q_mth` places that
certainty in its last month, so `l(proj_len()) = 0` — the one index beyond the frame — and the
closure identity is exact.

---

## Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is wrong. Each one
becomes a test in `tests/test_riester_rente_de.py`.

1. **Collapsing the two subsidy lags into one.** The entitlement looks back one **calendar** year
   for income [R10]; the cash arrives one **projection** year late [R11]. Assert
   `income_ref(0) = income_init`, `income_ref(k) = income_schedule[k − 1]`, and
   `zulage_pp(k) = zulage_granted_pp(k − 1)` — two distinct offsets, not one applied twice. Both are
   **annual** and the monthly grid gives the payment a month, not a different lag.
2. **Dropping the final contribution year's Zulage.** Contributions stop at `k_conv() − 1`; the
   Zulage they earned is credited at `k_conv()`. Assert `zulage_pp(k_conv()) > 0` on the anchor,
   that it enters `guar_pp(k_conv() + 1)`, and that it is inside `account_conv_pp()`. Stopping the
   Zulage with the contribution silently removes a full year's subsidy from both.
3. **Treating the *Mindesteigenbeitrag* as a cliff.** § 86 reduces the Zulage **in proportion** to
   the shortfall [R10] [REG-R42]. Assert on model point 7 that `contrib_ratio = 0.50` gives exactly
   `0.50 × zulage_entitlement_pp(k)` — not zero, and not the full amount.
4. **Treating the Zulage as a benefit, or netting it against the contribution.** It is a
   **contribution paid by the ZfA to the provider** [R8] [R11]. Assert `zulagen(t) > 0` as a
   separate positive column, that it never appears with a negative sign, and that
   `premiums(t)` excludes it.
5. **Modelling the *Günstigerprüfung* top-up as a contract cash flow.** Only the Zulage reaches the
   policy; the § 10a advantage is a personal tax refund [R6] [REG-R42]. Assert that no cells and no
   column corresponds to it.
6. **Using a single *Kinderzulage* rate.** The 185 € / 300 € split is a permanent **birth-cohort**
   rule, not a transition [R9] [R19]. Assert on model point 3 that both rates run **simultaneously**
   at `k = 0` and `k = 1`, giving `zulage_entitlement_pp = 175 + 185 + 300 = 660,00 €`.
7. **Testing the *Beitragsgarantie* anywhere but at *Rentenbeginn*.** It is tested **once** [R1].
   Assert that `db_pp(k)`, `cv_pp(k)` and `transfer_value_pp(k)` are **not** floored at `guar_pp`,
   and that the anchor has `garantieluecke_pp(0) > 0` — an account below the contributions paid —
   without that affecting any benefit.
8. **Enlarging the guarantee with a rider premium, or forgetting the 20 % cap.** Assert on model
   point 9 that `guar_carve_out_pp(k) = 0.20 × (E + Z + extra + rider)` and is **strictly less
   than** `rider_prem_pp = 400,00 €`, and that raising `rider_prem_pp` further does not reduce
   `guar_pp` further.
9. **Excluding unsubsidised contributions from the guarantee.** The guarantee is on the
   *Altersvorsorgebeiträge* paid in and does not distinguish the pools [R1]. Assert on model
   point 8 that `guar_pp(t + 1) − guar_pp(t)` includes `contrib_extra_pp`, while
   `zulage_entitlement_pp(t)` is unaffected by it.
10. **Adding the declared rate to the guaranteed rate.** `decl_rate` **includes** the
    *Rechnungszins* [REG-R53]. Assert `int_credited_pp(k) = j(k) · (D(k) + S(k)) + j(k) · U(k)`
    exactly, and that setting `j = i` makes `int_surplus_pp(k)` zero on the *Deckungskapital* leg.
11. **Crediting the frequency loading to the account.** The *Ratenzuschlag* is a charge. Assert that
    on model point 3 (monthly) `premiums(t)` exceeds the annual-mode amount by exactly
    `E(k) · 0.03` while `prem_to_av_pp(k)`, `guar_pp(k)` and every benefit are **unchanged**. It is
    also why the **contribution keeps the annual grid** on a monthly frame: φ prices the mode by
    loading the amount, so `prem_due(t)` puts the whole year's contribution in one month and a model
    that also split the cash into instalments would charge for the deferral twice.
12. **Charging acquisition costs in one year, or stopping them on *Beitragsfreistellung*.** The
    AltZertG requires spreading over at least five years [R1]. Assert `acq_charge_pp(t)` is equal in
    contract years 1 to 5 and zero afterwards, and on model point 10 that it **continues** after
    `bfs_year`, driving `prem_to_av_pp(k)` negative.
13. **Collapsing *Anbieterwechsel* into surrender.** A transfer is a full-value exit with **no**
    *Stornoabzug* [R1]. Assert `transfer_value_pp(k) = A(k + 1) − 50,00 €` while
    `cv_pp(k) = 0.98 · A(k + 1)`, and that the two decrements are separate columns. Both are struck
    on the **annual** end-of-year account value, so the month of the exit decides when it is paid
    and not how much.
14. **Treating *Beitragsfreistellung* as a termination.** It is a state change [R14] [REG-R28].
    Assert on model point 10 that `pols_if(t)` is **continuous** across `bfs_year`, that `guar_pp`
    freezes, that `zulage_pp` goes to zero, and that `av_total_pp` keeps rolling.
15. **Using one mortality table for both phases, or a period table for the annuity.** The direction
    of prudence forks by product [REG-R47], and DAV 2004 R is generational [REG-R49]. Assert that
    `mort_rate(t)` switches basis at `t_conv()`, that `annuity_mort_rate(x, τ)` depends on **both**
    arguments, and that `annuity_mort_rate(x, τ + 1) < annuity_mort_rate(x, τ)`. Assert too that
    `mort_rate_mth` is the **geometric** twelfth of the year's annual rate, so
    `(1 − q_mth)^12 = 1 − q` exactly and the annual survivorship is reproduced; `q/12` closes
    nothing.
16. **Testing the *Kleinbetragsrente* on the wrong annuity, or hiding the flat threshold.** The test
    is applied after the elected lump sum **[std]**, and the threshold is held flat in nominal terms
    **[std]**. Assert both explicitly, assert that model points 4 and 5 commute while the anchor does
    not, and that a commuted point pays `claims_commutation` and **no** `claims_lumpsum` and **no**
    `claims_annuity`.
17. **Applying the *Rentengarantiezeit* to the annuity amount, or paying a year of it at once.** The
    guarantee period changes the **payment count**, never the payment. Assert
    `pols_annuity_pay(t) = pols_conv()` for `t − t_conv() < 12 · rentengarantie_years` — the window
    is `12m` **instalments** — and `= pols_if(t)` afterwards, and that `annuity_month_pp()` is
    invariant to `rentengarantie_years`: model point 12, at zero, must pay the **same instalment**
    to a falling count. Assert also that the instalment is monthly —
    `claims_annuity(t) = annuity_month_pp() · pols_annuity_pay(t)` and
    `12 · annuity_month_pp() = annuity_pp(k)` — because booking a year at the start of the payout
    year on that year's opening count pays a life that dies in its first month for the whole of it.
18. **Netting the *Rückzahlungsbetrag* out of a benefit.** It is a tax collection the provider
    withholds and remits [R14]. Assert `claims_death(t) = A(k + 1) · pols_death(t)` gross, that
    `zulage_cum_pp(t)` is published and never subtracted from a claim, and that no cells attempts a
    § 10a repayment, which contract data cannot support.

---

## Policyholder behaviour modelling

Every formula here is **[std]**; there is no German Riester calibration evidence for any of them
(gap 16), and each rests on an argument from the statutory consequences.

- **Surrender is deliberately small and flat-ish.** 0,8 % / 0,6 % / 0,4 % by duration band. A
  *Kündigung* repays **all** Zulagen and **all** § 10a relief and taxes the accumulated growth on
  the subsidised part [R14] [REG-R42], against a surrender value that is already below the
  contributions paid in the early years. The German market's own description is that a Riester
  contract is effectively unsurrenderable in economic terms, and the assumption says so numerically.
- **Transfer out is set above surrender.** 1,2 % / 0,9 % / 0,6 %. The *Wechselrecht* is free of
  subsidy consequences [R1], so it dominates surrender for any saver who wants out but not out of
  the system. **A model carrying only a lapse rate has mis-specified this book**, and the ordering
  `transfer_rate > lapse_rate` at every duration is itself an assertion worth making.
- **No dynamic behaviour is modelled, and the omission is deliberate.** There is no rate-driven
  surrender function, because there is nothing to arbitrage into: the subsidy, not the credited
  rate, is what holds the contract. There is no *Teilkapitalauszahlung* take-up model, because the
  decision is a tax comparison the model does not perform — the lump sum is taxed **in full in its
  year with no *Fünftelregelung*** [R12] [R15] — and a fixed take-up rate standing in for a tax
  calculation should be labelled as such rather than dressed up.
- **What is computed rather than assumed.** The *Kleinbetragsrente* commutation. The model tests the
  annuity it has actually produced against the statutory threshold, so the commutation rate on a
  book is an **output**, not an input. Given how much of the German Riester book runs at the
  *Sockelbeitrag*, that is the right way round.
- **What a real book needs and this model does not have.** A *Beitragsfreistellung* **decrement**
  moving policies from a premium-paying to a paid-up cohort, each with its own account value and
  guarantee accumulator (assumption class (c), footnote 9). Model point 10 shows the mechanic on one
  policy; a book-level projection needs the split.

---

## Worked example

**Configuration.** Model point 1, the anchor: an in-force *klassische Riester-Rentenversicherung* at
the **1 January 2027** valuation date. `point_id = 1`; `sex = F` (reporting only — the tariff and the
conversion are unisex [R23]); `issue_age = 47`, the contract having been concluded on 1 January
**2024**; `duration_init = 3`, so `age(0) = 50`, `duration(0) = 3` — contract year 4 — and
`calendar_year(0) = 2027`;
`pols_if_init = 1.0`; `rentenbeginn_age = 67`; `rechnungszins = 0.0025`, the *Höchstrechnungszins* of
the 2024 vintage [R22] [REG-R15]; `beitragssumme = 33,600.00`; `contrib_form = mindest` with
`contrib_fixed_pp = 0.00`; `contrib_ratio = 1.00`, the full *Mindesteigenbeitrag* paid;
`contrib_extra_pp = 0.00`, so the two contribution pools coincide; `rider_prem_pp = 0.00`, so the
guarantee carries no carve-out; `income_id = grow2` and `income_init = 42,000.00`;
`zulage_id = k1_2010`, a household with **one child born in 2010** drawing *Kindergeld* to 2028, so
the entitlement is 475,00 € in contribution years 2027 and 2028 and 175,00 € thereafter;
`zulage_init_pp = 475.00`, the Zulage earned in 2026 and credited at `t = 0`;
`prem_freq = annual`, so `prem_freq_load = 1.0000`; `bfs_year = −1` (never); `dk_pp_init = 3,860.50`;
`surplus_pp_init = 150.48`, so `av_total_pp(0) = 4,010.98`; `guar_pp_init = 4,369.92` — three
*Eigenbeiträge* on the same income path plus the two Zulagen of 475,00 € credited in 2025 and 2026 —
which is **above** the account, so the anchor opens with a positive `garantieluecke_pp(0)` of
358,94 €;
`teilkapital_share = 0.30`, the statutory maximum lump sum; `rentenfaktor_guar = 29.00`;
`rentengarantie_years = 10`; and `scenario_id = base`. Hence `t_conv() = 67 − 50 = 17`, so
accumulation runs `t = 0 … 16` (attained ages 50 to 66, calendar 2027 to 2043), conversion falls at
`t = 17` (age 67, calendar 2044), the payout phase runs `t = 17 … 60`, and
`proj_len() = 110 − 50 + 1 = 61` periods. The opening balances are **[std]** seeds produced by the
same charge basis over contract years 2024 to 2026. **Model point 2 is this contract projected from
its own inception. It reconciles the two account seeds to the cent — `dk_pp_init` to 3 860,499285 €
and `surplus_pp_init` to 150,483132 € — and from its own `t = 3` onward reproduces every
per-policy quantity of the anchor's `t = 0` onward exactly; it does *not* reconcile
`guar_pp_init`, because the two seeds were struck on different income paths.** The discrepancy is
195,08 € and is set out in full under *Changes the model stage made to these notes*.

**Assumptions, each tagged.** *Grundzulage* **175,00 €**, *Kinderzulage* **300,00 €** for the child
born in 2010, no *Berufseinsteiger-Bonus* — all [R9] [REG-R42] `[unverified]`. *Mindesteigenbeitrag*
**4 %** of the previous calendar year's contribution-liable earnings, capped at **2 100,00 €**, less
the entitlement, floored at the **60,00 €** *Sockelbeitrag*, with the Kürzung proportional — [R10]
[REG-R42] `[unverified]`. Zulage cash lag **one year** [R11] [REG-R42], the one-year convention
**[std]**. Income path **2,0 %** p.a. from `income_init = 42 000,00 €` **[std]**, so the 2 100 €
ceiling first binds at `t = 12`. *Rechnungszins* **0,25 %** [R22] [REG-R15], the carrier's
own choice **[std]**. *Laufende Verzinsung* **2,30 %** level on the `base` scenario **[std]**, so
`int_surplus_pp` runs at **2,05 %** above the guaranteed leg. Acquisition charge **2,5 %** of the
33 600,00 € *Beitragssumme* — 840,00 €, in five equal instalments of **168,00 €** in contract years
1 to 5, so `t = 0` and `t = 1` carry it and `t = 2` onward do not — [R1] [REG-R16], level
**[std]**. Administration charge **4,0 %** of each contribution credited, Zulagen **included**
`[std]` — charging them is now established [S2] [S4] [S6] [S9] and only the rate is standardized —
plus a fixed **12,00 €** a year **[std]**. Frequency loading **1.0000** (annual)
**[std]**. *Risikobeitrag* **zero**, the death benefit being the account value. *Schlussüberschuss*
**2,0 %** of contributions credited and *Bewertungsreserven* share **1,0 %** of the account, both at
*Rentenbeginn*, both counted toward the guarantee — [REG-R24], levels and the counting convention
**[std]** (gap 9). Accumulation mortality: the shipped **[std]** proxy for **DAV 2008 T** [REG-R48]
at `mort_be_factor = 0.80`. Annuity mortality: the shipped **[std]** **generational** proxy for
**DAV 2004 R** [REG-R49], `q(x, τ) = qx_base(x) · (1 − improvement(x))^(τ − 2027)`, at
`annuity_mort_be_factor = 1.15` for the projection and at **1.00** — the first-order basis — inside
`ann_factor()`. Annuitisation interest **1,00 %** [REG-R15] **[std]**, with the Woolhouse
`−11/24` correction **[std]**; *Rentenfaktor* margin **30 %** **[std]**; guaranteed *Rentenfaktor*
**29,00 €** per 10 000 € per month **[std]** (gap 9). *Kleinbetragsrente* threshold **39,55 €** per
month **[std]** [REG-R42] [REG-R46] — **below the 59,33 € the statute implies** [R15], a discrepancy
recorded under *Model-relevant contradictions* and deliberately not fixed here. Surrender
**0,8 % / 0,6 % / 0,4 %** and transfer out **1,2 % / 0,9 % / 0,6 %** by duration band, both
**[std]**; *Stornoabzug* **2,0 %** [REG-R28] **[std]**; transfer charge **50,00 €** **[std]**,
now known to sit inside a statutory ceiling of **150,00 €** [R1] and to be the figure one fund
provider actually charges [S9] (gap 8 closed). Expenses **[std]**: maintenance 30,00 € per in-force policy per year inflating at **2,0 %**,
annuity administration 24,00 € per annuitant per year, claim expense 80,00 € per death, surrender or
transfer; no acquisition expense and no initial commission, because `duration_init = 3` puts them in
the past. Renewal commission **1,5 %** of the contributions credited **[std]**. `omega_age = 110`
**[std]**, with `q = 1` at that age so the decrements close exactly.

All amounts in euros; `pols_if` and `pols_annuity_pay` to six decimals, cash flows to the cent.
Totals are summed at **full precision and then rounded**, not summed from rounded cells.

### The cash flow statement — `Projection[1].result_cf()`, accumulation and conversion

Transcribed from the model's own output. `claims_commutation` is **0.00** at every `t` on this
cell — the anchor's annuity clears the *Kleinbetragsrente* threshold — and is omitted for space;
it is a required column of `result_cf()`. `liability_cf` is omitted for the same reason: it is
`−net_cf` exactly. `pols_annuity_pay` is zero throughout the accumulation and is carried in the
payout table below.

| k | pols_if | premiums | zulagen | int_credited | claims_death | claims_lapse | claims_transfer | claims_lumpsum | claims_annuity | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 1,205.00 | 475.00 | 125.21 | 6.62 | 43.39 | 65.90 | 0.00 | 0.00 | 33.21 | 25.20 | 1,505.67 |
| 1 | 0.978920 | 1,212.49 | 464.99 | 158.37 | 9.21 | 54.88 | 83.52 | 0.00 | 0.00 | 33.14 | 25.16 | 1,471.56 |
| 2 | 0.958169 | 1,507.08 | 455.13 | 201.64 | 12.93 | 52.48 | 79.96 | 0.00 | 0.00 | 32.75 | 29.43 | 1,754.65 |
| 3 | 0.942478 | 1,515.34 | 164.93 | 239.74 | 16.91 | 62.39 | 95.15 | 0.00 | 0.00 | 32.85 | 25.20 | 1,447.77 |
| 4 | 0.926909 | 1,523.36 | 162.21 | 278.17 | 21.59 | 72.38 | 110.47 | 0.00 | 0.00 | 32.93 | 25.28 | 1,422.92 |
| 5 | 0.911451 | 1,531.11 | 159.50 | 316.90 | 27.05 | 82.45 | 125.90 | 0.00 | 0.00 | 33.02 | 25.36 | 1,396.83 |
| 6 | 0.896093 | 1,538.55 | 156.82 | 355.91 | 33.42 | 92.59 | 141.44 | 0.00 | 0.00 | 33.10 | 25.43 | 1,369.38 |
| 7 | 0.880824 | 1,545.66 | 154.14 | 395.18 | 40.91 | 68.62 | 104.84 | 0.00 | 0.00 | 32.90 | 25.50 | 1,427.04 |
| 8 | 0.869997 | 1,560.24 | 152.25 | 436.87 | 49.75 | 75.86 | 115.91 | 0.00 | 0.00 | 33.14 | 25.69 | 1,412.15 |
| 9 | 0.859103 | 1,574.53 | 150.34 | 479.17 | 60.03 | 83.19 | 127.15 | 0.00 | 0.00 | 33.37 | 25.87 | 1,395.26 |
| 10 | 0.848126 | 1,588.46 | 148.42 | 522.04 | 71.94 | 90.62 | 138.53 | 0.00 | 0.00 | 33.60 | 26.05 | 1,376.14 |
| 11 | 0.837051 | 1,602.01 | 146.48 | 565.45 | 85.71 | 98.14 | 150.05 | 0.00 | 0.00 | 33.83 | 26.23 | 1,354.54 |
| 12 | 0.825864 | 1,589.79 | 144.53 | 608.79 | 101.51 | 105.64 | 161.54 | 0.00 | 0.00 | 34.04 | 26.01 | 1,305.57 |
| 13 | 0.814546 | 1,568.00 | 142.55 | 651.80 | 119.55 | 113.08 | 172.94 | 0.00 | 0.00 | 34.25 | 25.66 | 1,245.07 |
| 14 | 0.803079 | 1,545.93 | 140.54 | 694.42 | 140.11 | 120.45 | 184.22 | 0.00 | 0.00 | 34.44 | 25.30 | 1,181.95 |
| 15 | 0.791444 | 1,523.53 | 138.50 | 736.58 | 163.47 | 127.73 | 195.38 | 0.00 | 0.00 | 34.62 | 24.93 | 1,115.90 |
| 16 | 0.779621 | 1,500.77 | 136.43 | 778.20 | 189.98 | 134.91 | 206.38 | 0.00 | 0.00 | 34.79 | 24.56 | 1,046.59 |
| 17 | 0.767588 | 0.00 | 134.33 | 0.00 | 0.00 | 0.00 | 0.00 | 10,536.61 | 855.57 | 18.81 | 0.00 | −11,276.67 |
| **Total, k = 0 … 60** | | **25,631.84** | **3,627.10** | **7,544.45** | **1,150.72** | **1,478.78** | **2,259.27** | **10,536.61** | **19,793.08** | **1,057.57** | **436.87** | **−7,453.96** |

The table is `result_cf_annual()` — the monthly frame summed into projection years — with
`int_credited` read from `result_acct()`, which is where the annual state lives. **Its accumulation
rows are the annual-step model's to the last bit** on the contribution, the Zulage, the commission
and both balances; what moved when the grid did is the split of the exits between the three
decrements, the annuity, and the expenses.

**The Total row covers all sixty-one years, not only the eighteen displayed**, and is summed
**at full precision and then rounded**. Ten of its eleven columns differ from the sum of the
already-rounded cells: `premiums` 25 631,84 € against 25 631,85 €, `zulagen` 3 627,10 € against
3 627,09 €, `int_credited` 7 544,45 € against 7 544,44 €, `claims_death` 1 150,72 € against
1 150,69 €, `claims_lapse` 1 478,78 € against 1 478,80 €, `claims_transfer` 2 259,27 € against
2 259,28 €, `claims_annuity` 19 793,08 € against 19 793,06 €, `expenses` 1 057,57 € against
1 057,53 €, `commissions` 436,87 € against 436,86 €,
and `net_cf` −7 453,96 € against −7 453,97 €. Only `claims_lumpsum` agrees. **Assert the
full-precision totals.**

**What the monthly grid moved, against the annual-step model this replaced.** The contribution
(25 631,84 €), the Zulage (3 627,10 €), the interest credited (7 544,45 €), the commission
(436,87 €) and the lump sum (10 536,61 €) are unchanged, as are both balances, the guarantee
accumulator, the capital at *Rentenbeginn* and the *Kleinbetragsrente* verdict. The annuity falls
from 20 154,82 € to 19 793,08 €, because the instalment now stops with the month of death rather
than being paid for the whole year of it; the expenses fall from 1 069,29 € to 1 057,57 €, because a
mid-year exit bears only the months it was there; and the exits redistribute — 1 156,35 € to
1 150,72 € of death, 1 481,42 € to 1 478,78 € of surrender, 2 250,97 € to 2 259,27 € of transfer —
because the three decrements now compete month by month instead of running in sequence at a year
end. `net_cf` moves from −7 827,39 € to −7 453,96 €.

Four things to read off before the checks. **`zulagen` steps down between `k = 2` and `k = 3`**,
455,13 € to 164,93 €, while `premiums` *rises*: *Kindergeld* for the child born in 2010 stops
after the 2028 contribution year, so the entitlement falls at `k = 2` and the credit follows one
year later at `k = 3`, while the *Eigenbeitrag* jumps at `k = 2` because the § 86 minimum is 4 %
of income **less the entitlement** — a Zulage that stops is a contribution the saver must make
good. Two lags, two offsets, one table: pitfall 1. **The acquisition charge stops after `k = 1`**,
contract year 5; it never appears in the frame, being a deduction before the account, but
168,00 € of the 488,90 € rise in the *Sparbeitrag* between `k = 1` and `k = 2` is the charge
ending rather than the contribution rising, and it is why `garantieluecke_pp(k)` peaks at
**567,69 €** at `k = 2` and reaches zero at `k = 6`. **`claims_transfer` exceeds `claims_lapse`
at every `k` by about half again**, because the *Anbieterwechsel* rate is set above the surrender
rate at every duration and a transfer pays the full account less a flat 50,00 € against a
surrender's 98 %; both fall at `k = 7`, where contract duration passes 10 and the bands step
down. And **`net_cf` is positive in every accumulation year** before −11 276,67 € in the
conversion year: an in-force Riester cell is a positive cash flow to the insurer for as long as
it accumulates, and the whole liability is the conversion year and the annuity tail.

On the **monthly** frame the same year is a saw-tooth: the whole year's contribution and Zulage land
in its first month and nothing else does, so month 0 nets +1 642,25 € while each of the other eleven
carries a twelfth of the maintenance expense and that month's exits and nets about −12,50 €.

### The payout phase — selected rows, `k = 17 … 60`

`premiums`, `int_credited`, `claims_death`, `claims_lapse` and `claims_transfer` are **0.00 at
every `k` from 17 onward**: the account is extinguished at conversion, so there is no interest to
credit and a death pays nothing outside the *Rentengarantiezeit*. `zulagen` is 134,33 € at
`k = 17` — the final contribution year's subsidy, landing in the conversion year — and zero
thereafter. The counts are read at the **start** of the year; the instalments inside it are paid
monthly.

| k | age | pols_if | pols_annuity_pay | claims_annuity | expenses | net_cf |
|---|---|---|---|---|---|---|
| 17 | 67 | 0.767588 | 0.767588 | 855.57 | 18.81 | −11,276.67 |
| 18 | 68 | 0.762677 | 0.767588 | 855.57 | 18.85 | −874.43 |
| 26 | 76 | 0.701403 | 0.767588 | 855.57 | 19.33 | −874.91 |
| 27 | 77 | 0.690013 | 0.690013 | 762.71 | 17.42 | −780.13 |
| 28 | 78 | 0.677530 | 0.677530 | 748.18 | 17.20 | −765.39 |
| 34 | 84 | 0.574463 | 0.574463 | 628.63 | 15.35 | −643.98 |
| 44 | 94 | 0.273819 | 0.273819 | 286.52 | 9.02 | −295.54 |
| 54 | 104 | 0.016013 | 0.016013 | 13.95 | 0.85 | −14.81 |
| 60 | 110 | 0.000079 | 0.000079 | 0.09 | 0.01 | −0.10 |
| **Subtotal, k = 18 … 60** | | **17.024474** | **17.314559** | **18,937.51** | **468.77** | **−19,406.28** |

The *Rentengarantiezeit* is the whole of the difference between the two count columns. From
`k = 17` to `k = 26` — **120 instalments** from *Rentenbeginn*, `t = 204 … 323` —
`pols_annuity_pay` is frozen at
`pols_conv() = 0.767588` while `pols_if` decays to 0.701403, so `claims_annuity` is **exactly
855,57 € in each of those ten years** although a tenth of the annuitants have died. Those ten years
are also the annual-step model's **to the cent**: inside a guarantee window the count is fixed, and
120 monthly instalments on a fixed count are ten annual payments on it,
`120 × 92,885458 × 0,767588 = 8 555,73 €`. From `k = 27`
the columns join and the outgo falls with the survivors — and there the two grids part, 762,71 €
against the annual model's 769,11 €, because the instalment now stops with the month of death
rather than being paid for the whole year of it. Over the payout phase that is 361,74 €.

What is paid is `annuity_month_pp() = 92,885458 €`, one instalment a month, level for life;
`annuity_pp(k) = 1 114,625493 €` is the annual figure the twelve sum to, and it is the same in
**every** payout year, guarantee period or not — the guarantee changes who is paid, never how much
(pitfall 17). The subtotals say the same in aggregate: 17.314559 instalment-years paid against
17.024474 policy-years in force.

### Independent checks

*The first projected **month**, `t = 0`, rebuilt from the statute up, in one pass.* The reference
income is the previous calendar year's, so `Y(0) = income_init = 42 000,00 €`. The entitlement is
the *Grundzulage* plus one post-2008 *Kinderzulage*, `Z*(0) = 175,00 + 300,00 = 475,00 €`. The § 86
minimum is `max(60, min(0,04 × 42 000, 2 100) − 475) = max(60, 1 680 − 475) = 1 205,00 €`, and
`contrib_ratio = 1.00` pays it in full, so `E(0) = 1 205,00 €`; the frequency is annual, so
`φ = 1` and — the contribution being an annual event that falls in the year's first month —
`premiums(0) = 1 205,00 €`. The Zulage **credited** in year 0 is the one earned in
2026, `zulage_init_pp = 475,00 €`, so `zulagen(0) = 475,00 €`. Charges:
`K_a = 0,025 × 33 600 / 5 = 168,00 €` (contract year 4, inside the five-year window),
`K_v = 0,04 × 1 680,00 + 12,00 = 79,20 €`, so `S(0) = 1 680,00 − 168,00 − 79,20 = 1 432,80 €`.
Interest at the declared 2,30 % on the *Deckungskapital* plus the *Sparbeitrag* plus the
*Überschussguthaben*: `0,023 × (3 860,50 + 1 432,80 + 150,48) = 0,023 × 5 443,78 = 125,206940 €`,
the table's 125,21 €, and `A(1) = 5 568,986940 €`. All of that is annual and falls on the year's
clock.

The decrements are monthly. At attained age 50, contract
year 4 (`d(0) = 3`, the band read at `d(0) + 1 = 4`), the **annual** rates are
`q = 0,001500 × 1,10⁰ × 0,80 = 0,001200`, `w = 0,008` and `θ = 0,012`; their geometric twelfths are
`q_mth = 1 − (1 − 0,001200)^(1/12) = 0,000100055`, `w_mth = 0,000669124` and
`θ_mth = 0,001005543`, applied in that order within the month, so
`pols_death(0) = 0,000100055`, `pols_lapse(0) = (1 − q_mth) × 0,000669124 = 0,000669057` and
`pols_transfer(0) = (1 − q_mth)(1 − w_mth) × 0,001005543 = 0,001004769`. Benefits struck on the
**annual** `A(1)`, the end-of-year account every exit of that contract year takes:
`claims_death(0) = 5 568,986940 × 0,000100055 = 0,557205 €`;
`claims_lapse(0) = 0,98 × 5 568,986940 × 0,000669057 = 3,651449 €`;
`claims_transfer(0) = (5 568,986940 − 50,00) × 0,001004769 = 5,545308 €`. Expenses: a **twelfth**
of `30,00 × 1,02³ = 31,836240 €` of maintenance, inflated on **contract** duration and not on
projection year, plus `80,00 × (0,000100055 + 0,000669057 + 0,001004769) = 0,141911 €` of claim
expense, which is a per-**event** cost and falls whole — 2,794930 €. Commission
`0,015 × (1 205,00 + 475,00) = 25,20 €`, in the month the contribution falls. And
`1 680,00 − 0,557205 − 3,651449 − 5,545308 − 2,794930 − 25,200000 = 1 642,251108 €`, the frame's
`net_cf(0) = 1 642,25 €`. The other eleven months of the year carry no contribution and net about
−12,50 € each; the year sums to the annual table's 1 505,67 €.

*And the year's exits are the annual rates, compounded.* Over the twelve months the cohort loses
`0,001189015` to death, `0,007950812` to surrender and `0,011940288` to transfer. The annual-step
model's sequential split at one year end was `0,001200`, `0,007990` and `0,011890`: the total is the
same to the last bit — `1 − (1 − q)(1 − w)(1 − θ)` either way, which is why `pols_if(12)` is
`0,9789198848` on both — and only the **split** moves, from the decrement applied first toward the
one applied last.

*The conversion year rebuilt a different way.* At `k = 17` the *Deckungskapital* is
36 172,815098 €, the *Überschussguthaben* 8 224,490372 €, and the *Sparbeitrag* is the last
Zulage net of its charge, `175,00 − (0,04 × 175,00 + 12,00) = 156,00 €` — the acquisition charge
is long over. The raw account is therefore **44 553,305470 €**. On top of it the
*Schlussüberschussanteil* is 2 % of the contributions credited over the life of the contract,
which is exactly the guarantee accumulator: `0,02 × 37 877,2308 = 757,544616 €`; and the
*Bewertungsreserven* share is 1 % of the raw account, 445,533055 €. So
`account_conv_pp() = 45 756,383140 €`. The guarantee itself can be rebuilt without the recursion:
`guar_pp_init + pool_gefoerdert_pp(17) = 4 369,92 + 33 507,3108 = 37 877,2308 €`, which is
**7 879,15 € below** the account, so `capital_conv_pp() = 45 756,383140 €` and the
*Garantielücke* is zero on the `base` scenario. **Every one of those figures is the annual-step
model's to the last bit**, the account being an annual construction. The annuity factor at age 67 in
calendar 2044 on the first-order generational basis is `ä = 20,8722287915`, so the current
*Rentenfaktor* is
`0,70 × 10 000 / (12 × 20,8722287915) = 7 000 / 250,466746 = 27,947822`, **below** the
guaranteed 29,00, and the guaranteed factor applies. The lump sum is
`0,30 × 45 756,383140 = 13 726,914942 €`, leaving 32 029,468198 € to annuitise; the monthly
instalment is `32 029,468198 / 10 000 × 29,00 = 92,885458 €`, comfortably above the 39,55 €
*Kleinbetragsrente* threshold the model uses — and above the 59,33 € the statute implies, so this
cell is unaffected by that error — so the contract annuitises. That instalment is paid **monthly**,
in advance, from `t = t_conv() = 204`; `annuity_pp(17) = 12 × 92,885458 = 1 114,625493 €` is the
annual figure it sums to. Weighted on `pols_conv() = 0,7675876849`, that is
`claims_lumpsum(204) = 10 536,61 €` and, over the conversion year's twelve months — all inside the
guarantee window, so all on the same frozen count — `claims_annuity` of 855,57 €: the table's
row 17.

*The aggregate account rolls forward, and the charge the insurer keeps is what closes it.* The
account at the start of year 1 is `A(1) × l(12) = 5 568,986940 × 0,9789198848 = 5 451,592054 €`.
Rebuilt from year 0's own published parts: the opening account 4 010,98 €, plus the *Sparbeitrag*
1 432,80 €, plus the interest 125,206940 €, less the year's three exit benefits — 6,621611 €,
43,392406 € and 65,898295 €, each the sum of its twelve months — less the **exit charge the
insurer retains**, 1,482574 € of *Stornoabzug* and transfer charge over the same twelve months,
gives `5 568,986940 − 117,394886 = 5 451,592054 €`. The two agree to the last printed digit, **and
they agree whatever the split of the year's exits between the three decrements**, because all three
release the same annual end-of-year account value — which is what lets the monthly grid move the
split without touching the account. Dropping
the exit charge — which looks like income rather than like account released — leaves a residual
of 1,48 € at `k = 0`, and is the usual way this identity fails.

*Closure: the decrements sum to one.* Over the whole 732-month projection, expected deaths
in accumulation are **0,04110900**, deaths in payout **0,76758768**, surrenders **0,07648390**
and transfers out **0,11481942**. They sum to **1,00000000** exactly, and `pols_if(732) = 0`
because `mort_rate` is forced to 1 at `omega_age = 110` and `mort_rate_mth` places that certainty
in the terminal year's last month. Nothing is left in force and no exit is
counted twice. Note what the split says about the product: **23,24 % of the cohort leaves before
*Rentenbeginn*, and of those, 49,4 % leave by *Anbieterwechsel* against 32,9 % by *Kündigung*
and 17,7 % by death** — half again as many transfers as surrenders, at every duration and in
aggregate. A book modelled with a lapse rate alone would have mis-specified where the money goes
as well as how much of it goes.

*Closure: the statement reconciles.* On the Total row,
`25 631,84 + 3 627,10 − 35 218,47 − 1 057,57 − 436,87 = −7 453,96 €`, where 35 218,47 € is the
sum of all six `claims_*` columns. `int_credited` of 7 544,45 € is **not** in that sum: it moves
money inside the account rather than across the insurer's boundary — and on the monthly grid it is
not a column of the cash flow frame at all — and adding it would report
the cell's undiscounted deficit as 90,49 € instead of 7 453,96 €. This is `check_net_cf()`,
delib's first ruling, evaluated on the totals rather than month by month.

### Variant 1 — the `low` scenario and a binding *Beitragsgarantie* (model point 11)

`scenario_id = low` declares 0,50 % a year instead of 2,30 %. Model point 11 is a **shorter
deferral** than the anchor and that is deliberate: on a seventeen-year accumulation even 0,50 %
does not open a *Garantielücke*, and the reason is worth stating rather than hiding. Model
point 11 is `F`, `issue_age = 57`, `duration_init = 3`, so `age(0) = 60` and
`k_conv() = 7`; `income_id = grow2_60k` with `income_init = 60 000,00`, so the 2 100 € ceiling
binds from `k = 0` and `E(k) = 2 100 − Z*(k)`; `zulage_id = k1_2010` and
`zulage_init_pp = 475,00` as on the anchor; `beitragssumme = 17 500,00`; `prem_freq = annual`;
opening balances `dk_pp_init = 4 900,00`, `surplus_pp_init = 200,00`, `guar_pp_init = 5 825,00`,
so the cell opens 725,00 € under water; `teilkapital_share = 0.30`,
`rentenfaktor_guar = 29,00`, `rentengarantie_years = 10`; `proj_len_y() = 51` years and
`proj_len() = 612` months.

| k | pols_if | premiums | zulagen | int_credited | claims_death | claims_lapse | claims_transfer | claims_lumpsum | claims_annuity | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 1,625.00 | 475.00 | 35.08 | 21.75 | 54.89 | 83.51 | 0.00 | 0.00 | 33.34 | 31.50 | 1,875.01 |
| 1 | 0.977045 | 1,587.70 | 464.10 | 43.81 | 29.87 | 68.53 | 104.44 | 0.00 | 0.00 | 33.21 | 30.78 | 1,784.97 |
| 2 | 0.954320 | 1,837.07 | 453.30 | 53.94 | 40.55 | 63.36 | 96.64 | 0.00 | 0.00 | 32.76 | 34.36 | 2,022.69 |
| 3 | 0.936516 | 1,802.79 | 163.89 | 62.58 | 51.76 | 73.50 | 112.18 | 0.00 | 0.00 | 32.79 | 29.50 | 1,666.97 |
| 4 | 0.918697 | 1,768.49 | 160.77 | 70.91 | 64.50 | 83.25 | 127.13 | 0.00 | 0.00 | 32.80 | 28.94 | 1,592.64 |
| 5 | 0.900842 | 1,734.12 | 157.65 | 78.90 | 78.95 | 92.62 | 141.48 | 0.00 | 0.00 | 32.81 | 28.38 | 1,517.53 |
| 6 | 0.882930 | 1,699.64 | 154.51 | 86.57 | 95.28 | 101.59 | 155.23 | 0.00 | 0.00 | 32.80 | 27.81 | 1,441.44 |
| 7 | 0.864938 | 0.00 | 151.36 | 0.00 | 0.00 | 0.00 | 0.00 | 5,449.11 | 442.47 | 21.28 | 0.00 | −5,761.50 |
| 8 | 0.858363 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 442.47 | 21.33 | 0.00 | −463.80 |
| 19 | 0.731563 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 369.87 | 18.84 | 0.00 | −388.71 |
| 50 | 0.000061 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.03 | 0.01 | 0.00 | −0.04 |
| **Total, k = 0 … 50** | | **12,054.81** | **2,180.59** | **431.80** | **382.67** | **537.73** | **820.61** | **5,449.11** | **9,937.96** | **765.94** | **211.26** | **−3,869.89** |

Again the Total is summed at full precision and then rounded; the two differ on `zulagen`,
`claims_death`, `claims_lapse`, `claims_annuity`, `int_credited`, `expenses`, `commissions` and
`net_cf`. Every accumulation figure here is the annual-step model's; the annuity falls from
10 121,79 € to 9 937,96 € for the reason the anchor's does, and the exits redistribute the same
way.

**The guarantee binds, and this is the number the product exists to produce.** At `k = 7` the
raw account is 19 863,088636 €; the *Schlussüberschussanteil* adds 420,00 € and the
*Bewertungsreserven* share 198,630886 €, giving `account_conv_pp() = 20 481,719523 €`. The
guarantee accumulator is `guar_pp(8) = 21 000,000000 €` — the ceiling binds in every contribution
year, so the contributions credited are a round 2 100,00 € a year and the accumulator lands on a
round number. So `capital_conv_pp() = 21 000,000000 €` and
**`garantieluecke_conv_pp() = 518,280477 €`**: the insurer funds 518,28 € per policy out of its
own resources, 2,5 % of the capital, so that the saver receives at least what was paid in. The
annuity is then struck on the guaranteed capital rather than on the account —
`teilkapital_pp() = 6 300,00 €`, `annuity_capital_pp() = 14 700,00 €`, monthly instalment
`14 700 / 10 000 × 29,00 = 42,63 €` paid monthly, 511,56 € a year — and
`claims_lumpsum(t_conv()) = 6 300,00 × 0,8649383502 = 5 449,11 €`.

Two sensitivities follow, both reproducible by flipping `scenario_id` in
`model_point_table.csv`. On `base` this same cell's account reaches 22 271,80 € against the same
21 000,00 € guarantee, so the *Garantielücke* is **zero**: 1,80 percentage points of declared
interest over seven years is the whole difference between a guarantee that costs nothing and one
that binds — sensitivity 1, made arithmetic. And on the **anchor's** seventeen-year deferral the
`low` scenario still does not bind, but only just: the raw account at conversion is 37 370,67 €
against a guarantee of 37 877,23 €, a **raw shortfall of 506,56 €** closed only by the
*Schlussüberschussanteil* of 757,54 € and the *Bewertungsreserven* share of 373,71 €. Counting
those two toward the *Beitragserhaltungszusage* is the provider-favourable reading of an
unsettled question (gap 9); on the conservative reading the anchor's own low-rate *Garantielücke*
is 506,56 € rather than zero. That is sensitivity 4, and on this cell it is the larger of the
two.

### Variant 2 — the `fixed` contribution form (model point 5, the *mittelbar* spouse)

The second contribution form, at the economically extreme corner of the book: `contrib_form =
fixed` with `contrib_fixed_pp = 60,00`, the *Sockelbeitrag*, and `income_id = zero` because a
*mittelbar zulageberechtigt* spouse has no contribution-liable earnings of their own — so
`M(k) = max(60, min(0, 2 100) − 175) = 60,00 €`, the floor binds by construction, `E(k) = M(k)`
and the full *Grundzulage* is granted. `F`, `issue_age = 50`, `duration_init = 6`, so
`age(0) = 56` and `k_conv() = 11`; `beitragssumme = 1 020,00`; opening balances 1 150,00 €,
60,00 € and 1 400,00 €; `proj_len_y() = 55` years and `proj_len() = 660` months.
`claims_lumpsum` and `claims_annuity` are 0.00
throughout and `claims_commutation` replaces them.

| k | pols_if | premiums | zulagen | int_credited | claims_death | claims_lapse | claims_transfer | claims_commutation | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 60.00 | 175.00 | 32.74 | 3.07 | 8.52 | 12.60 | 0.00 | 34.88 | 3.52 | 172.40 |
| 1 | 0.982960 | 58.98 | 172.02 | 37.75 | 3.90 | 9.82 | 14.60 | 0.00 | 34.96 | 3.46 | 164.24 |
| 10 | 0.856985 | 51.42 | 149.97 | 81.96 | 20.01 | 14.21 | 21.50 | 0.00 | 36.10 | 3.02 | 106.55 |
| 11 | 0.843758 | 0.00 | 147.66 | 0.00 | 0.00 | 0.00 | 0.00 | 3,828.31 | 0.00 | 0.00 | −3,680.65 |
| 12 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| 54 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| **Total, k = 0 … 54** | | **609.80** | **1,926.26** | **631.80** | **108.18** | **123.53** | **185.58** | **3,828.31** | **388.54** | **35.83** | **−2,133.91** |

The saver pays 609,80 € over the whole projection and the state pays 1 926,26 € — **the Zulage
is 76 % of the contribution**, which is why a statement that folded `zulagen` into `premiums`
would be describing a different product. The contract never produces an annuity: at `k = 11` the
capital is 4 537,217342 €, and the annuity after the elected 30 % lump sum would be
`0,70 × 4 537,217342 / 10 000 × 29,00 = 9,21 €` a month against the model's 39,55 € threshold — and
it would fail the statutory 59,33 € threshold too, so this cell is likewise unaffected — so the
*Kleinbetragsrente* test commutes it and the whole capital is paid as an *Abfindung*,
`3 828,31 € = 4 537,217342 × 0,84375772`. There is **no** *Teilkapitalauszahlung* beside it,
`pols_if` is zero from `t_conv() + 1` because the *Abfindung* discharges the contract outright — an
exit `check_pols_roll_fwd()` counts as a commuted cohort rather than as a decrement — and the
frame carries zeros to `t = 659` rather than being truncated. Every figure of this cell's
accumulation, and the *Abfindung* itself, is the annual-step model's: a commuted contract pays no
annuity, so the one thing the monthly grid buys does not arise here, and only the split of the
exits and the expenses move.

### Changes the model stage made to these notes

Six, each because the model and the notes as drafted disagreed and the model was right.

1. **The frequency loading was deducted twice.** The drafted `S = C − K_a − K_v` had an
   *unloaded* `C` and a `K_v` already carrying `E(t)(φ − 1)`, so `prem_to_av_pp` **fell** with
   the payment frequency, contradicting pitfall 11. `C(t)` is now the cash **received** and the
   administration charge's percentage base is the unloaded `B(t)`; model point 3 (monthly) now
   has `premiums` larger by exactly `E(k) × 0,03` and an identical `prem_to_av_pp`, `guar_pp`
   and benefit set.
2. **`check_conversion()`'s third identity was inconsistent with the *Rentenfaktor* margin.**
   `12 · annuity_month_pp() · ann_factor() = annuity_capital_pp()` cannot hold when the factor
   carries a 30 % loading — it is short by exactly that margin. It is replaced by
   `rentenfaktor_curr() · 12 · ann_factor() = (1 − rentenfaktor_margin) · 10 000`, which says the
   same thing about the annuity basis, holds on every model point rather than only where the
   current factor applies, and still catches a Woolhouse correction applied twice.
3. **`check_pols_roll_fwd()` did not account for a commuted cohort.** An *Abfindung* discharges
   the contract, so `pols_if(t_conv() + 1) = 0` with no decrement having removed the population.
   The identity now carries `pols_conv()` as a fourth exit in the conversion **month** of a
   commuted contract; without it the check is false on model points 4, 5, 10 and 13.
4. **The guarantee accumulator's unsubsidised limb is gated on `is_accum_y(k)`**, matching
   `premiums(t)`. As drafted it added `contrib_extra_pp` in the conversion year, in which no
   contribution is paid.
5. **Model point 11 is a shorter-deferral cell than first drafted**, and its row in the model
   point table has been rewritten. Specified as the anchor with `scenario_id = low`, it did not
   bind: on that cell seventeen years of 0,50 % interest plus the two terminal surplus
   components exceed the charges by 624,69 €. The anchor-at-`low` figures are reported in
   Variant 1 as the sensitivity they are, because the 506,56 € raw shortfall they show is the
   more interesting of the two results.
6. **Model point 2 reconciles the anchor's account seeds and not its guarantee seed.** Projected
   from its own inception on the contract-clock income path `grow2_pre`, it reproduces
   `dk_pp_init` as 3 860,499285 € against 3 860,50 €, `surplus_pp_init` as 150,483132 € against
   150,48 € and `av_total_pp(0)` as 4 010,982418 € against 4 010,98 €, and from its `k = 3` onward every
   per-policy quantity coincides with the anchor's from `k = 0`. Its guarantee accumulator at the
   same point is **4 565,00 €** against the seed's 4 369,92 €. The two seeds were struck on
   different income paths — the account seed on earnings level at 42 000 € over the three
   pre-valuation contribution years, which reproduces 3 860,50 € to the cent, and the guarantee
   seed on a 2 %-declining back-path, which reproduces 4 369,92 € to the cent — and they cannot
   both be right. The seeds are kept as specified, because they are **[std]** opening balances of
   an in-force cell rather than derived quantities and because `garantieluecke_pp(0) = 358,94 €`
   depends on the pair; the 195,08 € discrepancy is recorded rather than papered over, and a
   calibration pass should restrike both on one path.

A seventh was settled later, when the model moved from an annual step to a monthly one.

7. **The grid is monthly and the contract is not.** `t` counts months and `k = t // 12` projection
   years, and a cells' argument says which clock it is on. The whole subsidy chain, both charges,
   both account balances, the guarantee accumulator and the conversion stay annual — they are
   annual terms of the statute and the contract, and the *Ratenzuschlag* is how a fractionated
   payment mode is priced without moving the contribution year — so the accumulation is
   bit-identical to the annual-step model's on all thirteen model points, the *Garantielücke* and
   the *Kleinbetragsrente* verdict included. What the finer grid was adopted for is the **monthly**
   *Leibrente* the AltZertG requires: pitfall 17's compression is gone, the *Rentengarantiezeit* is
   `12m` instalments, and the anchor's payout phase falls 361,74 €. It also dates the three
   accumulation exits, which now compete month by month instead of running in sequence at a year
   end, moving 5,62 € off the anchor's death outgo and 2,64 € off its surrender outgo onto 8,30 €
   of transfers.

---

## Valuation and reserve pointers

This library projects gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are **cited, never reproduced**.

- **The German statutory *Deckungsrückstellung*.** Prospective, computed on the
  *Rechnungsgrundlagen erster Ordnung* of the premium calculation — the tariff's own *Rechnungszins*
  and its first-order biometric basis — under § 341f HGB and the DeckRV [REG-R14] [REG-R54]. It is
  **not** the Solvency II best estimate, and the whole German picture depends on keeping the two
  apart: an insurer carries **two liability measures**, and the *Überschussbeteiligung*, the
  *Zinszusatzreserve* and the *Bewertungsreserven* test all run on the **HGB** side. `dk_pp(t) ×
  pols_if(t)` is this model's contribution to the first of them; the second-order path above is what
  feeds the Solvency II side.
- **The *Zinszusatzreserve*.** Where the § 5 Abs. 3 DeckRV *Referenzzins* falls below a contract's
  tariff rate, an additional HGB reserve arises [REG-R17]. On a **0,25 %** tariff it is small or nil;
  on the 1,75 % and 2,25 % vintages that dominate the older Riester book it is not, which is one
  reason a model of this product should carry `rechnungszins` as a **model-point** attribute rather
  than a library constant.
- **The guarantee is an option, and this projection prices none of it.** The *Beitragsgarantie* is a
  written put on the accumulation, struck at the contributions paid and exercisable once. The
  deterministic path above reports the *Garantielücke* on **one** declared-rate scenario;
  a time-value-of-options-and-guarantees calculation re-evaluates the crediting rule and the
  guarantee test per stochastic scenario, and the two scenarios shipped (`base`, `low`) are a
  sensitivity, not a distribution.
- **Solvabilität II.** Best estimate plus risk margin under the Directive as transposed by
  §§ 74–110 VAG [REG-R5] [REG-R6], with EIOPA publishing the curves. `BEL = Σ_t v(t) ·
  liability_cf(t)` over the recursion above. The **6 % cost-of-capital rate** is now read from the
  instrument — Art. 39 of the Delegierte Verordnung (EU) 2015/35, one sentence, retrieved and quoted
  in full in the cross-product reference library — but **no risk-free curve value, volatility
  adjustment or
  standard-formula shock in this library was read from a retrieved instrument**, so every such figure
  would still be **[std]**.
- **Contract boundary.** A Riester contract's future contributions are not unilaterally variable by
  the insurer, and the *Wechselrecht* is the policyholder's [R1] — but whether the Solvency II
  boundary extends to the whole future contribution stream **is still not determined** here. The
  Delegated Regulation itself was retrieved in the re-verification pass, but only its risk-margin
  articles were read; its contract-boundary articles were not, and no delib document states a figure
  from them. The model's posture is to project
  the full stream and publish it; a boundary-truncated view is obtained by truncating `result_cf()`.
- **The surplus regulations.** The MindZV puts an arithmetic floor under the transfer to the
  *Rückstellung für Beitragsrückerstattung* [REG-R18] [REG-R19] and § 153 VVG gives the individual
  entitlement and the *hälftige* participation in the *Bewertungsreserven* [REG-R24]. This model
  takes `decl_rate` as an **exogenous management action** and does not derive it from a
  distributable surplus; `frlib/products/assurance_vie_euro/` derives its credited rate from a
  statutory account, and the difference between the two treatments is a real difference between the
  two jurisdictions' surplus law, not a modelling shortcut.
- **IFRS 17.** A participating contract of this kind would be measured under the variable fee
  approach [REG-R55]; the same expected-cash-flow engine feeds it, and grouping, the CSM and the risk
  adjustment are out of scope.

---

## Key sensitivities and model risks

In rough order of leverage on a German Riester block.

1. **The declared *laufende Verzinsung*.** It is the largest single lever in the model and the least
   supported: it sets the account's growth, hence whether the *Garantielücke* is positive at all,
   hence the whole cost of the product's defining feature. Moving the `base` scenario from 2,30 % to
   the `low` scenario's 0,50 % is the difference between a guarantee that costs nothing and one that
   binds — model point 11 exists to show it. **No declared rate at any carrier was established**
   (gap 12).
2. **The charge basis, and the rate the Zulagen are charged at.** Every charge **level** is still
   **[std]**, but the question has narrowed. **Gap 14 is closed**: the Zulagen are charged, in the
   GDV model wording and at three carriers [S2] [S4] [S6] [S9]. What is now in doubt is the *rate*,
   and the one tariff in hand charges the Zulagen at **6,0 %** against **2,1 %** on the *Eigenbeitrag*
   [S4] where the model charges both at 4,0 %. On the low-income model points the Zulagen are the
   majority of the contribution, so the gap between 4,0 % and 6,0 % moves the account value on
   exactly the cells the product was designed for — and the gap between the composite's 2,5 %
   acquisition charge on a Zulagen-inclusive *Beitragssumme* and the observed 1,0 % on *Eigenbeiträge*
   alone moves it further. A calibration against [S4] is the highest-value next step in this file.
3. **The annuity basis and its generational structure.** A twenty-year deferral means the conversion
   happens on `τ = 2044` mortality. The improvement function, not the base table's level, is what
   decides the annuity factor, and it is entirely **[std]** [REG-R49]. The `rentenfaktor_margin` of
   30 % compounds the same uncertainty in the opposite direction.
4. **Which surplus components close the guarantee.** Counting the *Schlussüberschussanteil* and the
   *Bewertungsreserven* share toward the *Beitragsgarantie* is the provider-favourable reading and
   is unestablished (gap 9). Excluding them raises `garantieluecke_conv_pp()` by their whole amount
   on any cell where the guarantee binds.
5. **The absence of a *Beitragsfreistellung* decrement.** The dominant exit in the real book is
   represented as a per-model-point switch. A book projection built from these model points will
   therefore over-state future contributions and Zulagen unless the point weights carry the paid-up
   share — and **there is no official statistic for that share at all** (gap 2).
6. **The *Kleinbetragsrente* test — now a known error rather than an open question.** The threshold
   is **1,5 %** of the monthly *Bezugsgröße*, § 93 Abs. 3 Satz 2 Nr. 1 EStG [R15], and the model uses
   a 1 % figure; and the test belongs on the annuity **before** the elected lump sum, the GDV model
   wording excluding a commutation caused only by the *Teilkapitalauszahlung* [S2]. **Both of the
   model's choices push toward fewer commutations and a longer-tailed liability, and both are
   wrong in that direction.** Neither has been changed here — see *Model-relevant contradictions* —
   so this remains the largest single correction outstanding against the model.
7. **Holding the *Kleinbetragsrente* threshold flat in nominal terms.** The *Bezugsgröße* is reset
   annually; on a seventeen-year deferral a flat threshold **understates** the commutation rate, and
   the direction of the error is stated rather than hidden.
8. **This risk is retired: the *Leibrente* is paid monthly.** The annual grid paid a full year to a
   life that died in the payout year, overstating the annuity outgo by roughly `½ · q(x) · 12R` a
   year — small at 67 and growing with attained age. The monthly step pays one instalment at a time
   to whoever is alive that month, which removes it: 361,74 € of the anchor's payout phase and
   573,50 € of model point 12's. What remains **[std]** is *vorschüssig* against *nachschüssig*,
   worth about one month's interest on the annuity.
9. **This risk is retired. Gap 4 is closed.** Every statutory paragraph number in this file was
   checked against the canonical XML on 2026-08-30, with the instrument's *Stand* recorded at each
   entry in `sources.md`, and the two most consequential figures in the whole subsidy — the
   175 € / 185 € / 300 € Zulagen and the 4 % / 2 100 € / 60 € arithmetic — are read verbatim in
   §§ 84, 85, 86 and 10a EStG rather than corroborated at one remove [R6] [R9] [R10]. Three citations
   were **wrong** and are corrected: the 60th-year *Rentenbeginn* is AltZertG § 14 Abs. 2 and not
   § 1; the *Pfändungsschutz* is ZPO § 851 Abs. 1 and not EStG § 97; the *Effektivkosten* are
   AltvPIBV § 8 Nr. 3 and not the AltZertG, which never uses the word. What still requires a
   calibration pass before quantitative use is the **carrier** half: the charge levels, the declared
   rate and the *Rentenfaktor*, for which one tariff [S4] and one disclosed cost total [S9] now exist
   where none did.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-riester_rente-r1
[R10]: #delib-riester_rente-r10
[R11]: #delib-riester_rente-r11
[R12]: #delib-riester_rente-r12
[R13]: #delib-riester_rente-r13
[R14]: #delib-riester_rente-r14
[R15]: #delib-riester_rente-r15
[R16]: #delib-riester_rente-r16
[R19]: #delib-riester_rente-r19
[R22]: #delib-riester_rente-r22
[R23]: #delib-riester_rente-r23
[R25]: #delib-riester_rente-r25
[R4]: #delib-riester_rente-r4
[R5]: #delib-riester_rente-r5
[R6]: #delib-riester_rente-r6
[R8]: #delib-riester_rente-r8
[R9]: #delib-riester_rente-r9
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R20]: #delib-reg-r20
[REG-R24]: #delib-reg-r24
[REG-R28]: #delib-reg-r28
[REG-R34]: #delib-reg-r34
[REG-R40]: #delib-reg-r40
[REG-R42]: #delib-reg-r42
[REG-R43]: #delib-reg-r43
[REG-R44]: #delib-reg-r44
[REG-R46]: #delib-reg-r46
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R5]: #delib-reg-r5
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
