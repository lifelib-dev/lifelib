# Technical Notes

**Status:** Draft, 2026-08-29 (sources accessed 2026-08-29); citations re-verified against the
primary documents 2026-08-30.

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`RV_DE_S`**, **monthly** grid — for the standardized composite German *klassische aufgeschobene
private Rentenversicherung* defined in `product-spec.md` (same directory). This is not any single
insurer's contract. [S#]/[R#] tags refer to the source list in `sources.md` (numbering carried from
`_research/klassische_rentenversicherung.md`; frozen); [REG-R#] tags refer to the cross-product
reference library `references/regulatory-and-actuarial-references.md` (its own frozen numbering).
**[std]** marks standardizations introduced for the reference implementation; [unverified] marks
claims no retrieved document confirms. Parameter values are identical to those in `product-spec.md`.
Cells names, model-point columns and CSV headers are English `lower_snake_case`; German terms of art
keep their German form in prose.

**Retrieval conditions.** These notes were drafted with direct HTTP egress from the build
environment blocked, on `WebSearch` result summaries alone and a budget exhausted after eighteen
queries on this product; that policy has since been lifted and the citations were re-verified
against the primary documents on 2026-08-30. **Thirty-six of the forty-three entries in
`sources.md` now read `Retrieved: yes`** — including every VVG, EStG and DeckRV section these notes
rest on, read as canonical XML with its amendment *Stand* recorded, and the carrier wordings whose
§ numbers appear below. Four entries were reached only in part and three not at all, and each says
which it is: treat a citation here as sound where its entry says `Retrieved: yes`, and as a pointer
to the instrument rather than a certificate where it does not. The consequence for these notes is
unchanged, and still specific and large: **the corpus establishes this product's mechanics
thoroughly and its levels barely at all.** No charge parameter and no behavioural rate was
established at any German carrier for any year, and the *Rentenfaktor* range [R19] [R24] and the
declared rate [S15] the pass did establish are not the levels this model ships, so **every number
in assumption classes (b) and (c) below, and most of class (a)'s levels, is [std]**. What the
citations do establish is the shape of each recursion, and that is what this file is for.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — premiums in;
  death benefits, surrender values, the *Kapitalabfindung*, annuity instalments and insurer expenses
  out — for a single-policy model point on an expected (probability-weighted) basis, together with
  the two account balances that make the product what it is: the *Deckungskapital* and the
  *Ansammlungsguthaben*.
- **Out of scope, and said so rather than left to be discovered.** Discounting; the statutory
  *Deckungsrückstellung* [REG-R54]; the *Zinszusatzreserve* [REG-R17]; the RfB and the MindZV
  arithmetic [REG-R18] [REG-R19]; the *Sicherungsbedarf* test [REG-R20]; the Solvency II best
  estimate, risk margin, SCR and MCR [REG-R6]; IFRS 17 [REG-R55]; and **all taxation** — every cash
  flow is gross of *Kapitalertragsteuer*, *Solidaritätszuschlag* and *Kirchensteuer* [REG-R38]. Also
  not modeled, each for a stated reason: the *Bonusrente* surplus system [R24]; *Zuzahlung*, which no
  source names (gap 15); the survivor's-annuity and BU riders [S10] [S4]; § 163 VVG adjustment of the
  guaranteed *Rentenfaktor* [R3] [R17] [REG-R27]; and § 169 Abs. 6 [R1].
- **Projection frequency.** **Monthly grid over an annual product**, so the model runs on **two
  clocks**. The contract's own natural period is the *Versicherungsjahr*: the *Rechnungszins* is
  credited annually, the *Überschussbeteiligung* is declared annually and the
  *Ansammlungsguthaben*'s interest is credited at each policy year end and on termination [S4]
  § 3 Abs. 6, [S15], the § 165 paid-up value is "stated in the contract for each insurance year"
  [R2], and *Kündigung* and *Beitragsfreistellung* both take effect "for the end of the current
  insurance period" [R1] [R2]. **Every one of those constructions therefore keeps the policy year as
  its argument.** What the monthly step is *for* is the other half of the product: the **monthly
  annuity** [S13] [R24], which the annual grid could only compress and which these notes listed as a
  pitfall for that reason; the *Rentengarantiezeit*, which guarantees `12m` instalments rather than
  `m` lumps; and the decrements, which now fall in the month they happen.
- **What `t` counts.** `t` indexes the **policy month**, counted from inception, and is **0-based**:
  `t = 0` is the first policy month. `duration(t) = t // 12` is the **0-based policy year** `k`, and
  every annual construction in this file takes that `k`; `policy_year(t) = duration(t) + 1` is the
  contractual 1-based label the input files are keyed on. The attained age and the calendar year
  both step on the **anniversary** — `age(t) = issue_age + duration(t)`,
  `calendar_year(t) = issue_year + duration(t)` — so one generational mortality surface and one
  declared-rate path serve a book of mixed vintages, every policy year carrying its own attained age
  and calendar year [REG-R14] [REG-R49]. A new-business model point opens at `t = 0`. An
  **in-force** model point that has already run `duration_init` complete policy years opens at
  `t_start() = 12 × duration_init`, carrying its opening balances on the model point;
  `k_start() = duration_init` is the same instant on the annual clock. `is_anniv(t)` is
  `t % 12 == 11`, the month the annual machinery acts in.
- **`proj_len()`** is the **exclusive** end of the frame in **months**, per the library-wide ruling
  (`tests/test_model_conventions_de.py`), so the frame is `t = t_start() … proj_len() − 1` and
  `result_cf().index[-1] == proj_len() − 1`:

      proj_len_y() = omega_age − issue_age          the number of policy years
      proj_len()   = 12 × proj_len_y()              the frame, in months

  with `omega_age = 121` **[std]** the terminal age of the shipped mortality proxy, at which
  `mort_rate = 1`. The projection therefore ends when the annuitant cannot survive further, not at a
  fixed horizon: a life annuity has no term, and truncating one at, say, 40 years silently drops the
  tail the *Rentenfaktor* was priced for. For the anchor cell, `proj_len_y() = 121 − 50 = 71`, so
  the frame is `t = 0 … 851` and the last policy year ends at attained age 121.
- **The *Rentenbeginn* is the end of the deferment period of `n = aufschub_y` years**, which is the
  end of month `12n − 1` and the same instant as the start of month `12n`. Accumulation-phase months
  are `t < 12n`; payout-phase months are `t ≥ 12n`. The *Kapitalabfindung* is paid in month
  `12n − 1`; the first annuity instalment falls in month `12n`.
- **Two speeds on each decrement.** `mort_rate(t)` and `lapse_rate(t)` return the **annual** rate of
  the policy year `t` falls in — the vectors tabulated below, flat across the year's twelve months —
  and `mort_rate_mth(t)` and `lapse_rate_mth(t)`, each `1 − (1 − r)^(1/12)`, are what the recursion
  applies. The twelfth is **geometric and never `r / 12`**, so twelve compound back to the year's
  rate exactly and `pols_if` at every anniversary is what the annual grid gave. Two rates of 1 are
  certainties rather than rates — the terminal `q = 1` of the proxy, and the § 165 cash-out — and
  both are placed in the anniversary month instead of being twelfth-rooted, since spreading a
  certainty geometrically empties the cohort eleven months early.
- **Timing conventions [std].** The premium at the **start of the policy year**, which is what
  § 12 Abs. 1 VVG makes the *Versicherungsperiode* for this tariff, so `prem_due(t)` is true in the
  first month of each policy year and nowhere else; charges deducted immediately after; the
  *Rechnungszins* credited on the post-premium, post-charge balance at the **end of the year**; the
  declared surplus credited to the *Ansammlungsguthaben* at the end of the year; death and surrender
  at the **end of each month**, deaths before surrenders; the *Rentenbeginn* events after the
  decrements of month `12n − 1`; and annuity instalments at the **start of each payout month**,
  monthly in advance, which is what a *Rente* is. **The ordering of premium credit, charge deduction
  and interest accrual is not established by any source in this corpus** [S11] and is the single most
  consequential [std] in this file (processing order, and pitfall 2).
- **What a mid-year exit is paid.** The value struck at the **end of the current
  *Versicherungsperiode*** — § 169 Abs. 3 VVG's *zum Schluss der laufenden Versicherungsperiode*,
  and not the cancellation date [R1] — so a policy leaving in any month of policy year `k` is paid
  `cv_pp(k)` or `db_pp(k)`, the same amount the annual grid paid. It is the consistent reading: the
  *Beitrag* was payable in advance for the whole period, so the period's value is what the contract
  earned. What the monthly grid changes is **when** the claim falls and **how many policies are
  exposed** to it, not what it is worth.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  benefits and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to euro
  cents, `pols_if` to six decimals **[std]**.
- **Unisex pricing is a hard constraint, not a convention.** A model point carries `sex` for the
  **decrement** — the underlying DAV tables are sex-specific raw material [REG-R47] [REG-R49] — and
  `sex` must not enter the premium, the charge scale or the *Rentenfaktor*, sex-based differences
  being prohibited for contracts concluded from 21 December 2012 [REG-R34].

---

## Model point attributes

Thirty columns. `model_point_table.csv` is indexed by `point_id` and is the one input file exempt
from the `provenance` rule, because a model point is a *configuration* rather than an assumption.
The right-hand column names the points that exercise each attribute away from its base value.

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Key; `Projection` is parameterized by it | all |
| `policy_id` | str | Label, `DE-RV-nnnn` | all |
| `sex` | enum {M, F} | Decrement only; **never** priced [REG-R34] | 2, 4, 7, 9, 11, 13 are F |
| `issue_age` | int | Age last birthday at inception | all |
| `issue_year` | int | Calendar year of inception; drives the generational mortality index and fixes the guarantee vintage [REG-R14] [REG-R49] | 6 (2005), 14 (2017) |
| `duration_init` | int | Complete policy years already elapsed; 0 = new business. Already 0-based, so the frame opens at `t_start() = 12 × duration_init` | 6 (20), 14 (8) |
| `pols_if_init` | float | Policies represented; `pols_if(t_start())` | all (1.0) |
| `premium_form` | enum {laufend, einmal} | Recurring or single premium [S11] [REG-R53] | 2 (`einmal`) |
| `prem_gross_pp` | EUR p.a. | Annual *Bruttobeitrag* before the frequency loading | all but 2 |
| `premium_single_pp` | EUR | *Einmalbeitrag* | 2 |
| `prem_freq` | enum {annual, half_yearly, quarterly, monthly} | *Zahlweise*; keys `freq_load_table.csv` for the *Ratenzahlungszuschlag*. The **collection** is annual in advance whatever the elected frequency, § 12 Abs. 1 VVG making the *Versicherungsperiode* the year for this tariff | 3 (monthly), 4 (quarterly), 5 (half-yearly) |
| `prem_term_y` | int | Premium-paying **years** from inception, a count: premiums fall in policy years `k < prem_term_y` | 4 (20 of 22), 5 (25 of 27) |
| `aufschub_y` | int | Deferment in **years**, a count: *Rentenbeginn* at the end of month `t = 12 × aufschub_y − 1` | all |
| `int_rate_guar` | rate | The contract's *Rechnungszins* — **a model-point attribute, not a global assumption** [R7] [REG-R14] [REG-R15] | 6 (2,75 %), 14 (0,90 %) |
| `charge_id` | str | Key into `charge_table.csv`; `zillmer_25` or the pre-2015 `zillmer_40` [REG-R16] | 6 (`zillmer_40`) |
| `annuity_rate_guar` | EUR/month per 10 000 € | *garantierter Rentenfaktor*, fixed at inception [S8] [R24] | all (levels **[std]**) |
| `rf_scenario_id` | str | Key into `rentenfaktor_table.csv` for the *aktueller Rentenfaktor* | 5 (`high`), 13 (`low`) |
| `decl_scenario_id` | str | Key into `decl_rate_table.csv` for the declared *laufende Verzinsung* | 14 (`low`) |
| `guar_capital_pp` | EUR | Minimum guaranteed contract value at *Rentenbeginn* [S9]; 0 = not stated | 13 (60 000) |
| `death_benefit_form` | enum {prem_refund, deckungskapital, max} | The three documented designs [S1] [R24]; `max` **[std]** [S19] | 2, 12 (`deckungskapital`); 5, 13 (`max`) |
| `db_incl_surplus` | int 0/1 | Whether the *Ansammlungsguthaben* is added to the death benefit [R24] | 4, 12 |
| `rgz_years` | int | *Rentengarantiezeit* in years [R24] [S9] [S13]; the model pays `12 × rgz_years` guaranteed instalments | 9 (0), 11 (5), 3/14 (15), 5/10 (20) |
| `kapitalwahl_rate` | float | Fraction electing the *Kapitalwahlrecht* at *Rentenbeginn* [S12] [R6] [R21] | 9 (1.00), 2/10 (0.00), 5 (0.20) |
| `pup_year` | int | **Contractual policy year** of *Beitragsfreistellung*, 1-based; 0 = never [R2]. The contract is paid up from policy year `k = pup_year − 1` | 7 (10), 8 (3, trips the minimum) |
| `dynamik_rate` | rate | *Dynamik* annual premium increase [S4]; 0 = option off | 12 (5 %) |
| `payout_system` | enum {konstant, teildynamisch, volldynamisch} | *Überschussverwendung* in payment [R19] [R20] [R24] | 4, 11 (`teildynamisch`); 5, 10 (`volldynamisch`) |
| `av_pp_init` | EUR | Opening *Deckungskapital* | 6, 14 |
| `av_sur_pp_init` | EUR | Opening *Ansammlungsguthaben* | 6, 14 |
| `prem_cum_pp_init` | EUR | Premiums paid before the valuation date — the *Beitragsrückgewähr* base | 6, 14 |
| `alpha_amort_pp_init` | EUR | Acquisition charge already amortised before the valuation date | 6 (2 592), 14 (900) |

**The fourteen model points.** Point 1 is the worked example's anchor cell. Between them the points
carry both premium forms, all four payment frequencies, two in-force cells on two legacy guarantee
vintages, both charge sets, all three death-benefit forms with and without surplus, all three payout
systems, five *Rentengarantiezeit* durations including zero, *Kapitalwahlrecht* take-ups of 0 %,
20 %, 30 % and 100 %, the *Dynamik*, both *Beitragsfreistellung* branches, and four boundary cases:
the paid-up conversion that fails the *Mindestversicherungsleistung* and is cashed out (8), full
commutation at *Rentenbeginn* (9), the guaranteed *Rentenfaktor* binding over a lower current one
together with a binding `guar_capital_pp` (13), and a *Rentengarantiezeit* of zero (9).

**One constraint the table must satisfy and the model asserts.** `av_spread_pp` (below) is seeded
equal to `av_pp_init` on an in-force point, which is exact only once the acquisition charge is
amortised under both treatments, so every in-force point has `duration_init ≥ alpha_spread_years = 5`
**[std]**. Points 6 and 14 open at durations 20 and 8.

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len_y`, `proj_len` | `omega_age − issue_age` policy years, and `12 ×` that as the exclusive end of the frame in months | once per model point |
| `duration(t)`, `policy_year(t)`, `is_anniv(t)` | The bridge between the two clocks: the 0-based policy year of month `t`, its 1-based label, and whether `t` is the year's last month | derived |
| `age(t)` | Attained age in month `t` = `issue_age + duration(t)`; **steps on the anniversary** | annual step |
| `calendar_year(t)` | `issue_year + duration(t)`; the second index of the generational mortality surface, also stepping on the anniversary | annual step |
| `pols_if(t)` | Policies in force at the **start of month** `t`; `pols_if(t_start()) = pols_if_init()` | monthly recursion |
| `pols_annuity(t)` | The count the annuity instalment is **paid on** — the annuitised count inside the *Rentengarantiezeit*, survivors after it, zero before *Rentenbeginn* | monthly |
| `av_pp(k)` | *Deckungskapital* per policy at the start of policy year `k` | annual recursion |
| `av_pp_at(k, timing)` | `"BEF_PREM"`, `"AFT_PREM"`, `"AFT_INT"` | within policy year `k` |
| `av_sur_pp(k)`, `av_sur_pp_at(k, timing)` | *Ansammlungsguthaben* per policy, and its within-year points | annual recursion |
| `av_spread_pp(k)`, `av_spread_pp_at(k, timing)` | The parallel *Deckungskapital* in which the acquisition charge is spread evenly over the first five contract years — the § 169 Abs. 3 VVG floor [REG-R28] | annual recursion |
| `spread_diff_pp(k)` | `av_spread_pp(k) − av_pp(k)`; the only quantity by which the two accounts differ | annual recursion |
| `capital_conv_pp` | Conversion capital struck at *Rentenbeginn* | once |
| `annuity_rate_appl` | `max(annuity_rate_guar, annuity_rate_curr)` [S4] | once |
| `annuity_guar_mth_pp` | *garantierte Rente*, monthly, struck at *Rentenbeginn* | once |
| `annuity_sur_mth_pp(k)` | *Überschussrente*, monthly, by payout system; steps on the anniversary | annual |
| `annuity_pp(t)` | The instalment actually paid in month `t`: `G + U(duration(t))` | monthly |
| `mort_rate_guar(t)`, `mort_rate(t)` | First-order (tariff) and second-order (best-estimate) **annual** mortality, flat across a policy year | lookup |
| `mort_rate_mth(t)`, `lapse_rate_mth(t)` | The **monthly** rates the recursion applies, each `1 − (1 − r)^(1/12)` | derived |
| `lapse_rate(t)` | **Annual** surrender rate; **0** from *Rentenbeginn* | lookup |

There is **no** paid-up sub-population state: *Beitragsfreistellung* is a deterministic election at a
stated policy year rather than a continuous decrement, for the reason given under *Policyholder
behaviour modelling*. There is **no** *Bonusrente* ledger in the accumulation phase, and **no**
survivor's-annuity state.

---

## Assumption inputs

**The eight input files.** All inputs are **external CSVs beside `run.py`**, read once per model by
the unparameterized `Data` Space (the `annuallife/TradLife_A` layout). Every file but the model point
table carries a per-row `provenance` column, this library's second ruling.

| File | Index columns | Value columns |
|---|---|---|
| `model_point_table.csv` | `point_id` | the thirty model-point attributes above (**provenance-exempt**) |
| `mort_table.csv` | `sex`, `age` | `q_base`, `improve`, `provenance` |
| `decl_rate_table.csv` | `scenario_id`, `calendar_year` | `decl_rate`, `provenance` |
| `rentenfaktor_table.csv` | `rf_scenario_id`, `age` | `annuity_rate_curr`, `provenance` |
| `charge_table.csv` | `charge_id`, `item` | `value`, `provenance` |
| `lapse_table.csv` | `duration` | `lapse_rate`, `provenance` |
| `freq_load_table.csv` | `prem_freq` | `freq_load`, `n_instalments` (**recorded, not applied**), `provenance` |
| `param_table.csv` | `item` | `value`, `provenance` |

`param_table.csv` holds every scalar [std] assumption that is neither a charge nor a rate table:
`expense_acq_pp`, `expense_maint_pp`, `expense_annuity_pp`, `expense_claim_pp`, `expense_infl`,
`mort_be_factor`, `mort_base_year`, `omega_age`, `val_reserve_rate`, `sur_ann_rate`,
`sur_ann_growth`, `sur_ann_theta` and `roll_fwd_tol`. Keeping them in a file rather than in
`Projection` References is what gives each of them its own provenance tag.

### (a) Contractual and guaranteed elements (cited)

| Input | Value / rule | Basis |
|---|---|---|
| *Deckungskapital* recursion | The *Sparbeitrag* — the premium net of the tariff costs and the *Risikobeitrag* — accumulated at the *Rechnungszins*: *"indem wir die eingezahlten Beiträge abzüglich der tariflichen Kosten und Risikobeiträge mit dem tariflichen Garantiesatz von 0,90 Prozent p. a. verzinsen"* | [S8] § 1 Abs. 2; [S11] § 27 Abs. 1; ordering **[std]** |
| *Rechnungszins* | A model-point attribute; 1,00 % for 2026 issues, 2,75 % and 0,90 % on the two legacy points | [R7] [R11] [REG-R14] [REG-R15] |
| *Höchstzillmersatz* | **25 ‰** of the *Beitragssumme* from 1 January 2015 — § 4 Abs. 1 Satz 2 DeckRV, *"Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"* — **40 ‰** before, the rate at conclusion applying for the whole term (§ 4 Abs. 4) | [R7]; [REG-R16] [REG-R20]; restated by four carriers as "2,5 % der Beiträge" [S1] § 14, [S4] § 11, [S8] § 8, [S9] § 16 |
| § 169 Abs. 3 surrender floor | At least the *Deckungskapital* that results from spreading the charged acquisition and distribution costs **evenly over the first five contract years**, *"die aufsichtsrechtlichen Regelungen über Höchstzillmersätze bleiben unberührt"* | [R1] at article level; [REG-R28]; [S1] § 12 Abs. 3, [S4] § 10 Abs. 3, [S8] § 7 Abs. 3, [S9] § 16 Abs. 4, [S11] § 34 Abs. 2 |
| § 169 Abs. 5 *Stornoabzug* | Permitted only if **agreed, quantified and appropriate**; a deduction for unamortised acquisition costs is void | [R1] [REG-R28] |
| § 165 paid-up value | Computed on the premium calculation basis, **on the basis of the § 169 Abs. 3–5 surrender value**, and tabulated per insurance year | [R2] [REG-R28] |
| § 165 minimum benefit | Below the *Mindestversicherungsleistung* the contract is **cashed out at the surrender value including profit shares**, not made paid-up | [R2] |
| Death benefit before *Rentenbeginn* | *Beitragsrückgewähr* (premiums paid, *ohne Zinsen*), the accumulated *Deckungskapital*, or the larger of the two; optionally plus the attributable surplus; or **no benefit at all** where no extension is bought | [S8] § 1 Abs. 1; [S9] § 1 Abs. 3 for the `max` form; [S4] § 1 Abs. 2–3; [R24] |
| Conversion capital | Includes *Überschussbeteiligung* and *Bewertungsreserven*, subject to a minimum guaranteed contract value | [S9] |
| Conversion rule | `monthly annuity = capital / 10 000 × Rentenfaktor` — *"wie viel Rente wir Ihnen monatlich je 10.000 Euro … zahlen"* | [S11] § 52 Abs. 1; [S14] § 2 Abs. 5; [S18]; [R24] |
| *Rentenfaktor* applied | `max(garantierter, aktueller)` — the annuity on the bases current at *Rentenbeginn* against the *garantierte Mindestrente*, the higher paid, tested at NÜRNBERGER **at each monthly instalment** | [S9] § 1 Abs. 1; [S14] § 2 Abs. 3 and 6; [S18]; [R24] |
| *Bewertungsreserven* | *hälftige* participation under § 153 Abs. 3 Satz 2 VVG, **crystallised at the transition to annuity payment** — § 153 Abs. 4, *"Bei Rentenversicherungen ist die Beendigung der Ansparphase der nach Absatz 3 Satz 2 maßgebliche Zeitpunkt"* — and continuing in payment by contract | [R4] at article level; [S4] § 3 Abs. 2; [S15]; [REG-R24] |
| Annuity | Monthly **in advance**, for life, from *Rentenbeginn* — *"monatlich, jeweils zum Monatsersten"*; *garantierte Rente* plus *Überschussrente*, only the first guaranteed, the RfB-financed part promised *"jeweils nur für ein Versicherungsjahr"* | [S9] § 1 Abs. 1; [S4] § 3 Abs. 7; [R20] [R24] |
| *Rentengarantiezeit* | Payment continues until the agreed years expire, *"unabhängig davon, ob die versicherte Person diesen Termin erlebt"*; commutable to a present value at the payout-phase *Rechnungszins* | [S1] § 1 Abs. 4; [S4] § 1 Abs. 4 and § 10 Abs. 14; [S9] § 1 Abs. 5; [R17] [R24] |
| Surrender in payment | None | [REG-R28]; reading **[std]** |
| Mortality basis | **DAV 2004 R (Aggregattafel)**, a *Generationentafel*, first order carrying safety margins over second order; carriers derive their own tables from it (*NÜRNBERGER Tafel 2013R*, *Debeka 01/21 R*) | [S4] § 1 Abs. 6, [S5] [S6] [S7] [S16]; [S9] [S11] for the derived tables; [R12] [R13] [REG-R47] [REG-R49] |
| Unisex tariff | Sex may not enter premium or benefit for contracts from 21 December 2012 | [REG-R34] |

### (b) Insurer-discretionary current elements (snapshot; revisable annually)

Everything in this class is a **declaration**, not a promise: the GDV model wording says so in terms —
*"Die Höhe der Überschussbeteiligung hängt von vielen Einflüssen ab, die nicht vorhersehbar und von
uns nur begrenzt beeinflussbar sind. … Die Höhe der künftigen Überschussbeteiligung kann also nicht
garantiert werden. Sie kann auch Null Euro betragen."* [S1] § 2 Abs. 7. **One carrier's rates are now
established** (gap 4 closed): Bayern-Versicherung's *Überschussverteilung 2026* declares the annuity
*Zinsüberschussanteil* for tariff generations 2015–2025 as **3 % less the *Rechnungszins*** before the
*Rentenbeginn* and 3,35 % less it during the *Rentenbezug*, against 2,25 % and 2,5 % for 2025 [S15] —
so the total interest credited is 3,00 % for 2026. **The values below are unchanged and remain
[std]**; they are a scenario path, not that declaration, and `model.md` records the divergence.

| Input | Value | Basis |
|---|---|---|
| Declared *laufende Verzinsung* `decl_rate` | **2,55 % p.a.** level on the `base` path; **1,50 %** on the `low` path | **[std]** (i) |
| Surplus rate `bonus_rate(t)` | `max(0, decl_rate(t) − int_rate_guar)` — **1,55 %** on the 1,00 % vintage, **0 %** on the 2,75 % vintage | mechanic [R24] [REG-R53]; **[std]** level |
| Interest credited on the *Ansammlungsguthaben* | at `decl_rate(t)`, the full declared rate | mechanic [R24]; **[std]** (ii) |
| *Bewertungsreserven* rate at *Rentenbeginn* `val_reserve_rate` | **1,5 %** of the accumulated value | mechanic [S4] [R4]; level **[std]** (iii) |
| *aktueller Rentenfaktor* at *Rentenbeginn* | **32,00 €** per month per 10 000 € at age 67 on the `base` path; **25,50 €** `low`; **35,00 €** `high` | mechanic [S13] [R24]; level **[std]** (iv) |
| *Überschussrente* rate `sur_ann_rate` (`konstant`) | **12 %** of the *garantierte Rente*, level | mechanic [R20]; level **[std]** (v) |
| *Überschussrente* growth `sur_ann_growth` (`volldynamisch`) | **1,5 % p.a.** compound on the *garantierte Rente* | mechanic [R20] [R24]; level **[std]** (v) |
| `teildynamisch` split `sur_ann_theta` | **0,5** — half the constant increment plus half the growth rate | mechanic [R20] [R24]; **[std]** (v) |

(i) Anchored on the only public *market averages* the library has: the average *laufende Verzinsung*
for 2025 was **2,53 % Klassik / 2,58 % Neue Klassik**, and for 2026 the sources give 2,6–2,7 %, 2,87 %
and 2,54 % — three incompatible averages [REG-R53]. 2,55 % sits inside the 2025 pair and is a market
average, not a carrier's declaration. **A carrier's declaration is now available and is not this
number**: Bayern-Versicherung's *Überschussverteilung 2026* credits a total of **3,00 %** before the
*Rentenbeginn* (2025: 2,25 %) and **3,35 %** during the payout phase (2025: 2,5 %) on tariff
generations 2015–2025 [S15]. The shipped path stays at 2,55 % because it is a market-average scenario
rather than one carrier's book, and because changing it moves the worked example and the golden
tests; the divergence is recorded rather than absorbed. **The declared rate is the *Garantieverzinsung* plus the
*laufende Zinsüberschussbeteiligung*, never a surplus on top of the guarantee** [REG-R53]; that is
what the `max(0, ·)` in `bonus_rate` implements, and it is why the 2,75 % legacy point receives no
interest surplus at all — a real and important German result, not a modelling artefact.
(ii) The *Ansammlungsguthaben* mechanic is established in a carrier's own definition — the surpluses
are credited to an *Überschussguthaben* and accumulated with interest, the interest credited at each
policy year end, on termination, and for an annuity also at the start of annuity payment or on
commutation [S15]; [S4] § 3 Abs. 6 says the same and adds that the balance is paid out on death,
surrender or commutation. **Neither states the rate.** Crediting the full declared rate rather than the *Rechnungszins* is [std]; the
alternative is a documented variant and moves the anchor cell's final *Ansammlungsguthaben*
materially.
(iii) The mechanic is now statutory rather than restated: § 153 Abs. 3 Satz 2 VVG allots the amount
determined at termination *"zur Hälfte"*, and § 153 Abs. 4 makes the *Beendigung der Ansparphase* the
relevant moment for an annuity [R4]; [S4] § 3 Abs. 2 and [S15] apply it. **No amount, ratio or
reserve level is established** anywhere.
1,5 % of the accumulated value is a placeholder sized to be visible without dominating.
(iv) See product spec footnote 9. Chosen so that the anchor cell's `max()` resolves **upward** (the
current factor wins) and point 13's resolves **downward** (the guarantee binds), because a rule with
one branch never exercised is a rule no test covers.
(v) The three systems are established and their *directions* are established — the constant form is
set from a whole-period projection and **falls if the insurer earns less**, the fully dynamic form
adjusts annually to actual surplus development, and the partial form is a stated combination of the
two [R20] [R24] — and two carriers now name them in their own AVB: *Garantie-PLUS-Rente* /
*Bonus-PLUS-Rente* / *Bonusrente* [S4] § 3 Abs. 7, and *dynamische Überschussrente* /
*teildynamische Bonusrente* [S9] § 2 Abs. 5 c). The fully dynamic form is confirmed to ratchet —
*"Die jeweils erreichte Rentenhöhe kann nicht mehr sinken"* [S9] — while the level form is confirmed
not to be guaranteed, the RfB-financed part being promised *"jeweils nur für ein Versicherungsjahr"*
[S4]. **No level, rate or split is established for any of them.**

### (c) Behavioural and experience assumptions (the modeller's view)

**Every input in this class is [std] and none has any evidence behind it** (gap 20): no German lapse
rate, no *Beitragsfreistellung* rate, no *Kapitalwahlrecht* take-up rate and no market *Stornoquote*
was returned by any search for this product.

**Mortality.** The first-order basis is **DAV 2004 R**, a *Generationentafel* which is the property
of the Deutsche Aktuarvereinigung, is not public and is **not shipped** [S8] [R12] [R13] [REG-R49].
`mort_table.csv` is a **[std] proxy** with the structure the real table has and none of its values:
a sex-distinct base table `q_base(sex, x)` for base year **2005** — the year DAV 2004 R was intended
for new business [R13] — and an age-dependent annual improvement rate `improve(x)`, combined as

    mort_rate_guar(t) = q_base(sex, x(t)) × (1 − improve(x(t)))^( calendar_year(t) − 2005 )

which is the generational form the reference library requires of any annuity proxy, built the way it
recommends: a base table times a cumulative improvement factor, anchored to Destatis's own
*Generationensterbetafeln* as the free redistributable analogue [REG-R49] [REG-R52]. The proxy is
anchored so that **`q_base(M, 50) = 0.002000` exactly**, and that anchor is stated in the model's
`Data` docstring; a substitute table must preserve it if the worked example is still to close.
`improve(x)` is **1,5 % p.a. below age 60, grading linearly to 0,5 % at age 100 and to zero at 110**
**[std]** — a deliberate simplification of the *Starttrend* / *Zieltrend* structure the German
construction actually uses, and documented as one rather than presented as a replication [REG-R49].

The second-order (best-estimate) basis is the first-order one loaded:

    mort_rate(t) = mort_rate_guar(t) × mort_be_factor,    mort_be_factor = 1.15  [std]

**The factor is above one and that is the whole point.** For an annuity, prudence means assuming
mortality **lower** than expected, so the first-order table sits below best estimate, and the safety
margin runs in **two dimensions** — level and trend [REG-R47] [REG-R49]. The same table is used for
the accumulation-phase death benefit, which is the German peculiarity worth naming: an annuity table
prices a death benefit, so that benefit is systematically **under**-charged relative to a
death-business basis such as DAV 2008 T [REG-R48], and the *Beitragsrückgewähr* design exists partly
because it makes the mismatch immaterial — the benefit is the premiums, not a sum insured.

**Lapse (*Storno*).** `lapse_table.csv`, keyed by the **contractual policy year** (`duration`,
1-based, so the lookup goes through `policy_year(t) = duration(t) + 1` and the twelve months of a
policy year all read the same row), and **zero from *Rentenbeginn***:

| Duration | 1 | 2 | 3 | 4–7 | 8–11 | **12** | 13+ | payout |
|---|---|---|---|---|---|---|---|---|
| `lapse_rate` **[std]** | 6,0 % | 5,0 % | 4,5 % | 4,0 % | 3,5 % | **6,0 %** | 3,0 % | 0 % |

The **duration-12 step is the only shaped feature and it is the one with a reason**: § 20 Abs. 1
Nr. 6 EStG makes half the gain taxable only where the contract has run **at least twelve years** and
payment falls after completion of the **62nd year of life**, so German Schicht-3 surrenders are
suppressed approaching duration 12 and spike at it [R6] [REG-R45]. That is the German analogue of the
eight-year threshold that drives French *assurance vie* behaviour, and delib models it the same way
frlib does — as a duration-dependent shape with the threshold named and the level [std]. The level of
every cell is unsourced.

**Election rates.** `kapitalwahl_rate` is a **model-point attribute**, base **30 %** [std]. It is not
a behavioural formula, and the notes say why: the annuitise-or-commute decision is a **tax
comparison** — 18 % of each instalment at the marginal rate against half the *Unterschiedsbetrag*
taxed once [R5] [R6] [REG-R41] [REG-R45] — and this model computes no tax, so the rate stands in for
a calculation it does not perform. `pup_year` is likewise a deterministic election rather than a
rate.

**Expenses (all levels [std]; no German carrier publishes any of them, gap 14).**

| Input | Value | Note |
|---|---|---|
| Acquisition `expense_acq_pp` | **400,00 €** per policy at issue, new business only | **[std]** |
| Maintenance, accumulation `expense_maint_pp` | **45,00 €** per policy p.a., inflating; a twelfth a month | **[std]** |
| Administration, payout `expense_annuity_pp` | **30,00 €** per policy p.a., inflating; a twelfth a month | **[std]** |
| Settlement `expense_claim_pp` | **120,00 €** per death, surrender or commutation event | **[std]** |
| Inflation `expense_infl` | **2,0 % p.a.**, compounding in **policy years** and stepping on the anniversary | **[std]** |

**Charges — and the distinction from expenses is load-bearing.** A *charge* is a deduction the tariff
makes from the premium or the *Deckungskapital*; it moves money **inside** the contract and produces
**no cash flow**. An *expense* is the insurer's actual outgo and is a cash flow. Confusing them is
pitfall 6. `charge_table.csv` is keyed by `(charge_id, item)` so each number carries its own
`provenance` tag:

| Item | `zillmer_25` | `zillmer_40` | Basis |
|---|---|---|---|
| `alpha_rate` | 0,025 of the *Beitragssumme* | 0,040 | cap [REG-R16]; use of the cap **[std]** |
| `alpha_spread_years` | 5 | 5 | § 169 Abs. 3 [REG-R28] |
| `beta_rate` | 0,040 of each gross premium | 0,040 | **[std]** |
| `gamma_rate` | 0,0020 p.a. of the *Deckungskapital* | 0,0020 | **[std]** |
| `gamma_pup_rate` | 0,0030 p.a. while premium-free | 0,0030 | **[std]** |
| `stornoabzug_rate` | 0,020 of the pre-deduction value | 0,000 | conditions [R1] [REG-R28]; level and flat, duration-free shape **[std]** — observed forms are none [S8] [S9], a flat 250 EUR [S4], or percentages tapering to nil over the last ten years [S11] |
| `min_annuity_mth` | 30,00 € a month | 30,00 € | § 165 threshold [R2]; level **[std]**, against 25,00 € a month at two carriers [S4] [S9] |
| `annuity_admin_rate` | 0,015 of each instalment | 0,015 | **[std]**; **recorded, not applied** — see pitfall 12 |

`freq_load_table.csv` carries the *Ratenzahlungszuschlag* **[std]** (gap 14): annual 1,000 (1
instalment), half-yearly 1,020 (2), quarterly 1,030 (4), monthly 1,050 (12). No retrieved wording
publishes one; every carrier refers the amounts to the *Kostenausweis nach § 2 VVG-InfoV* or the
*Persönlicher Vorschlag* [S1] § 14 Abs. 1, [S4] § 11 Abs. 1, [S9] § 16 Abs. 1, which is why this gap
is structural.

**The loading is the whole of what the *Zahlweise* does here, and the `n_instalments` column stays
documentation even on a monthly grid.** § 12 Abs. 1 VVG makes the *Versicherungsperiode* the year
where premiums are not measured in shorter periods, the *Deckungskapital* this model turns on is
defined at anniversaries, and § 169 Abs. 3 pays a mid-period exit the value struck at the **end** of
that period — so the consistent reading is a premium payable in advance for the whole year and a
value earned for the whole year, and `prem_due(t)` is true in the first month of each policy year
only. Modelling the instalments would require an unearned-premium convention on mid-year exits that
no source in this corpus establishes. `KLV_DE_S` is the contrast and the reason this is a decision
rather than an omission: there the *echt* / *unecht* distinction turns on whether the
*Versicherungsperiode* is genuinely monthly, two model points differ in nothing else, and the
instalment stream is therefore in the frame.

---

## Cash flow components and recursions

### Notation, defined once and used throughout

| Symbol | Cells | Meaning |
|---|---|---|
| `t`, `t0`, `N` | — | the 0-based policy-**month** index, `t = t0 … N − 1`; `t0 = t_start() = 12 × duration_init`; `N = proj_len() = 12 × proj_len_y()` |
| `k`, `k0`, `N_y` | `duration`, `k_start`, `proj_len_y` | the 0-based policy-**year** index, `k = t // 12`; `k0 = duration_init`; `N_y = omega_age − issue_age`. Every annual construction below takes `k` |
| `x(t)`, `τ(t)` | `age`, `calendar_year` | attained age `issue_age + k(t)`; calendar year `issue_year + k(t)`; both step on the **anniversary**. The contractual policy year is `k + 1` |
| `n`, `m`, `κ` | `aufschub_y`, `rgz_years`, `kapitalwahl_rate` | deferment years; guarantee period; commutation take-up. `n` and `m` are **counts of years**, so the last accumulation month is `t = 12n − 1` and the guarantee window is `12n ≤ t < 12n + 12m` |
| `l(t)` | `pols_if` | policies in force at the start of **month** `t`; `l(t0) = pols_if_init()` |
| `a(t)` | `pols_annuity` | the count the annuity instalment is paid on, monthly |
| `V(k)` | `av_pp` | *Deckungskapital* per policy at the start of policy year `k` |
| `A(k)` | `av_sur_pp` | *Ansammlungsguthaben* per policy at the start of policy year `k` |
| `Ṽ(k)`, `Δ(k)` | `av_spread_pp`, `spread_diff_pp` | the five-year-spread parallel account, and `Ṽ(k) − V(k)` |
| `P(k)` | `prem_pp` | gross premium per policy for policy year `k`, after the frequency loading, payable in advance |
| `α(k)`, `α̃(k)` | `charge_acq_pp`, `charge_acq_spread_pp` | zillmered and evenly-spread acquisition charge |
| `β(k)`, `γ(k)`, `ρ(k)` | `charge_prem_pp`, `charge_admin_pp`, `charge_risk_pp` | premium, reserve-based and risk charges |
| `S(k)` | `prem_to_av_pp` | *Sparbeitrag* — the premium net of what the charges take from it |
| `C(k)` | `charge_from_av_pp` | the part of the charges the premium could not meet, taken from `V` |
| `i`, `d(k)`, `b(k)` | `int_rate_guar`, `decl_rate`, `bonus_rate` | *Rechnungszins*; declared rate; `max(0, d(k) − i)` |
| `D(k)`, `Ď(k)` | `db_pp`, `db_base_pp` | death benefit paid on a death in policy year `k`; its start-of-year measure, used only for `ρ` |
| `R(k)`, `R̄(k)`, `R̲(k)` | `cv_pp`, `cv_tariff_pp`, `cv_floor_pp` | surrender value; the tariff value net of the *Stornoabzug*; the § 169 Abs. 3 floor |
| `q*(t)`, `q(t)`, `w(t)` | `mort_rate_guar`, `mort_rate`, `lapse_rate` | first-order and best-estimate mortality, and the surrender rate — all three **annual**, flat across a policy year |
| `q^m(t)`, `w^m(t)` | `mort_rate_mth`, `lapse_rate_mth` | the **monthly** rates the recursion applies, each `1 − (1 − r)^(1/12)` |
| `K`, `f_g`, `f_c`, `f` | `capital_conv_pp`, `annuity_rate_guar`, `annuity_rate_curr`, `annuity_rate_appl` | conversion capital; the two *Rentenfaktoren* and the applied one |
| `G`, `U(k)` | `annuity_guar_mth_pp`, `annuity_sur_mth_pp` | *garantierte Rente* and *Überschussrente*, monthly amounts stepping once a year |

Rates are per annum and dimensionless; `V`, `A`, `P`, `D`, `R`, `K` are EUR per policy; every cash
flow in `result_cf()` is EUR for the model point as a whole.

### The premium and the *Beitragssumme*

    P(k) = 0                                                 if k ≥ n, or k ≥ prem_term_y,
                                                             or (pup_year > 0 and k ≥ pup_year − 1)
         = premium_single_pp                                 if premium_form = einmal and k = 0
         = prem_gross_pp × freq_load × (1 + dynamik_rate)^k   if premium_form = laufend

    prem_due(t) = ( t mod 12 == 0 )        the first month of each policy year, and no other
    premiums(t) = P(duration(t)) × l(t)    where prem_due(t), else 0

    beitragssumme_pp = Σ_{u=0..min(prem_term_y, n)−1} P_sched(u)
    alpha_total_pp   = alpha_rate × beitragssumme_pp

`P_sched` is the premium schedule **as written at inception**, ignoring any later
*Beitragsfreistellung*: § 4 DeckRV takes the *Zillmersatz* on the sum of all premiums payable under
the contract [REG-R16], and a later election does not retrospectively shrink that base. The
frequency loading is inside `P`, so it is inside the *Beitragssumme* too.

### The premium decomposition

    α(k)  = min( P(k), max(0, alpha_total_pp − alpha_cum_pp(k)) )        zillmered
    α̃(k)  = alpha_total_pp / alpha_spread_years   for k < 5, else 0      § 169 Abs. 3 [REG-R28]
    β(k)  = beta_rate × P(k)
    γ(k)  = (paid_up(k) ? gamma_pup_rate : gamma_rate) × V(k)
    Ď(k)  = prem_cum_pp(k) + P(k)                     if death_benefit_form = prem_refund
          = V(k)                                      if death_benefit_form = deckungskapital
          = max(of the two)                           if death_benefit_form = max
    ρ(k)  = q*(12k) × max(0, Ď(k) − V(k))             for k < n, else 0
    charge_due_pp(k)      = α(k) + β(k) + γ(k) + ρ(k)
    charge_from_prem_pp(k)= min( P(k), charge_due_pp(k) )
    C(k)                  = charge_due_pp(k) − charge_from_prem_pp(k)
    S(k)                  = P(k) − charge_from_prem_pp(k)

Two conventions are doing work here and both are [std]. First, **the risk charge is struck on
start-of-year quantities**, `Ď(k)` and `V(k)`, rather than on the post-premium balance — otherwise
`ρ` depends on `V` after `ρ`, and the recursion is circular. It reads the **annual** first-order rate
`q*(12k)`, the rate of the first month of policy year `k`, which is the year's rate: the
*Risikobeitrag* the tariff strikes is an annual charge and is not twelfth-rooted. Second, **charges
are met from the premium where there is one and from the *Deckungskapital* where there is not**:
[S11] describes premium-based deductions, but a premium-free contract still bears administration and
mortality cost, and `C(k)` is what makes *Beitragsfreistellung* cost something instead of being
free. Note that for
`death_benefit_form = deckungskapital` the net amount at risk is identically zero, so `ρ ≡ 0` — which
is correct, and is a good invariance test.

### The *Deckungskapital* and the *Ansammlungsguthaben*

    av_pp_at(k,"BEF_PREM") = V(k)
    av_pp_at(k,"AFT_PREM") = V(k) + S(k) − C(k)
    int_credited_pp(k)     = i × av_pp_at(k,"AFT_PREM")
    av_pp_at(k,"AFT_INT")  = av_pp_at(k,"AFT_PREM") + int_credited_pp(k)

    bonus_credited_pp(k)      = b(k) × av_pp_at(k,"AFT_PREM") + d(k) × A(k)
    av_sur_pp_at(k,"AFT_INT") = A(k) + bonus_credited_pp(k)

The *Ansammlungsguthaben* is a **second, parallel account** with its own credited rate, settling at
year end and at exit [R24]. Its interest-surplus credit is `b(k) = max(0, d(k) − i)` applied to the
same base the guarantee is applied to, so the two together deliver the declared *laufende Verzinsung*
`d(k)` and never more — the arithmetic the reference library names as the commonest error in
describing a German contract [REG-R53].

### The § 169 Abs. 3 floor, as a difference recursion

The two accounts differ **only** in the acquisition charge, so the model carries the difference
rather than a second full recursion:

    Δ(k0) = 0
    spread_diff_pp_at(k,"AFT_INT") = ( Δ(k) + α(k) − α̃(k) ) × (1 + i)
    Δ(k+1) = spread_diff_pp_at(k,"AFT_INT")
    av_spread_pp_at(k,"AFT_INT") = av_pp_at(k,"AFT_INT") + spread_diff_pp_at(k,"AFT_INT")

with `γ` and `ρ` deliberately taken at the same euro amount in both accounts **[std]**, which is what
makes the difference exact. Two consequences are worth stating because they are not obvious. The
difference is **large in the first five years** — on the anchor cell the whole 25 ‰ is taken in the
first year against one fifth of it — and it **never returns to zero**, because the spread account earns the
*Rechnungszins* on the amounts not yet deducted. So on a zillmered tariff with a positive
*Rechnungszins* the § 169 Abs. 3 floor is above the tariff *Deckungskapital* at **every** duration,
not only in the first five years.

### Surrender, and the *Beitragsfreistellung* election

    surr_charge_pp(k) = stornoabzug_rate × ( av_pp_at(k,"AFT_INT") + av_sur_pp_at(k,"AFT_INT") )
    R̄(k) = av_pp_at(k,"AFT_INT") + av_sur_pp_at(k,"AFT_INT") − surr_charge_pp(k)
    R̲(k) = av_spread_pp_at(k,"AFT_INT")
    R(k) = max( R̄(k), R̲(k) )

A surrender in **any** month of policy year `k` is paid `R(k)`: § 169 Abs. 3 VVG strikes the value
*zum Schluss der laufenden Versicherungsperiode* and not at the cancellation date [R1], and the
*Beitrag* was payable in advance for that same period.

The floor is the § 169 Abs. 3 *Deckungskapital* alone, because Abs. 3 speaks of the
*Deckungskapital*; profit shares sit **on top of** the statutory minimum rather than inside it, which
is the reading § 165 Abs. 2's "surrender value … including profit shares" [R2] supports. **The
alternative reading, in which the floor also carries the *Ansammlungsguthaben*, is not implemented
and would make the floor bind at every duration**; the chosen reading lets the floor bind early and
stop binding once the surplus account has outgrown the interest residual and the *Stornoabzug*, so
both branches of the `max()` are exercised on the anchor cell alone.

*Beitragsfreistellung* is a deterministic election in the **contractual policy year** `pup_year`,
which is policy year `k = pup_year − 1`, tested at the end of the preceding year:

    pup_value_pp = max( av_pp_at(pup_year−2,"AFT_INT"), av_spread_pp_at(pup_year−2,"AFT_INT") )
    pup_cashout  = ( pup_value_pp / 10 000 × f_g ) < min_annuity_mth

If `pup_cashout` is false the contract continues premium-free: `P(k) = 0` from `k = pup_year − 1`,
the *Deckungskapital* is **reset to `pup_value_pp`** — the § 165 rule that the paid-up benefit is
computed on the § 169 Abs. 3–5 value, on the premium basis [R2] [REG-R28] — the *Ansammlungsguthaben*
is untouched, `Δ` is set to zero because the two accounts have merged, and the reserve-based charge
switches to `gamma_pup_rate`. **The uplift is real money and it is published**, as
`pup_uplift(pup_year − 2) = ( pup_value_pp − av_pp_at(pup_year−2,"AFT_INT") ) × l(12(pup_year − 1))`,
so that the fund-level roll-forward still closes. It is booked in the **transition year**
`k = pup_year − 2`, because that is the year whose roll-forward needs it: the uplift is the step
between that year's zillmered end-of-year balance and the reset opening balance of policy year
`k = pup_year − 1`, and `check_av_roll_fwd()` closes in every policy year only if it is credited on
the earlier of the two. On the anchor cell it is identically zero; on point 7 it is 28,39 € at
`k = 8`.
If `pup_cashout` is true the contract is **cashed out instead**, the whole surviving cohort leaving
in the **last month** of policy year `k = pup_year − 2` through the surrender decrement at `R(k)`
[R2]. That is one of the two places `w(k)` is 1 rather than a rate, and `w^m` places the certainty
in the anniversary month rather than spreading it geometrically: § 165 makes the cash-out fall at
the end of the *Versicherungsperiode*, not a twelfth of the way into it. **No *Stornoabzug* is applied on the paid-up route [std]**: Abs. 5 is drafted for a payout on
*Kündigung*, and here the contract continues. The alternative is a documented variant.

### Decrements and the in-force recursion

**Monthly**, with deaths before surrenders **[std]** inside each month, which is the annual grid's
own order taken a twelfth at a time. Accumulation phase, `t < 12n`:

    q^m(t) = 1 − (1 − q(t))^(1/12)            the year's annual rate, geometrically twelfthed
    w^m(t) = 1 − (1 − w(t))^(1/12)
    pols_death(t) = l(t) × q^m(t)
    pols_lapse(t) = ( l(t) − pols_death(t) ) × w^m(t)
    D(k)          = ( prem_refund ? prem_cum_pp(k) + P(k)
                    : deckungskapital ? av_pp_at(k,"AFT_INT")
                    : max(of the two) )  + ( db_incl_surplus ? av_sur_pp_at(k,"AFT_INT") : 0 )
    claims(t,"DEATH") = D(duration(t)) × pols_death(t)
    claims(t,"LAPSE") = R(duration(t)) × pols_lapse(t)
    l(t+1)        = l(t) − pols_death(t) − pols_lapse(t) − pols_commutation(t)

Payout phase, `t ≥ 12n`: mortality only, no surrender, no premium, no death benefit.

    pols_death(t) = l(t) × q^m(t)
    pols_lapse(t) = 0
    l(t+1)        = l(t) − pols_death(t)

Because `(1 − q^m)^12 (1 − w^m)^12 = (1 − q)(1 − w)` exactly, `l(12k)` at every anniversary is the
annual grid's `l(k)` to the last bit. What the finer grid changes is the **split** of a year's exits
between the two decrements — competing monthly rather than in a fixed annual order — not their total,
and the shift is small: 16,87 € of claims from death to lapse over the anchor cell's whole run.

Note that `D(k)` uses **end-of-year** balances while `Ď(k)` in the risk charge uses start-of-year
ones; they are different quantities with deliberately similar names, and the model publishes both.
Both are **annual**: a death in any month of policy year `k` is paid `D(k)`.

### The *Rentenbeginn*

All of it happens at the end of the last accumulation **month** `t = 12n − 1` — which is the end of
policy year `k = n − 1` — on the survivors of that month's decrements:

    capital_gross_pp = av_pp_at(n−1,"AFT_INT") + av_sur_pp_at(n−1,"AFT_INT")
    val_reserve_pp   = val_reserve_rate × capital_gross_pp
    K                = max( guar_capital_pp, capital_gross_pp + val_reserve_pp )
    f                = max( f_g, f_c )
    G                = K / 10 000 × f

    pols_surv_rb              = l(12n−1) − pols_death(12n−1) − pols_lapse(12n−1)
    pols_commutation(12n−1)   = κ × pols_surv_rb
    pols_annuitization(12n−1) = (1 − κ) × pols_surv_rb
    claims(12n−1,"COMMUTATION") = K × pols_commutation(12n−1)
    l(12n)                    = pols_annuitization(12n−1)

`f_c` is read from `rentenfaktor_table.csv` at `(rf_scenario_id, issue_age + n)` — the annuitant's
attained age at *Rentenbeginn*. The commuting policyholders receive `K`, the same capital the
annuitants convert, *Bewertungsreserven* included [S9]: the corpus gives no basis for paying them
less, and inventing one would be a charge no source supports.

### The annuity in payment

    U(k) = sur_ann_rate × G                                                  konstant
         = G × ( (1 + sur_ann_growth)^(k − n) − 1 )                          volldynamisch
         = θ·sur_ann_rate·G + G × ( (1 + θ·sur_ann_growth)^(k−n) − 1 )       teildynamisch, θ = 0.5

    annuity_pp(t)   = G + U(duration(t))         one instalment, paid in advance
    a(t)            = 0                            for t < 12n
                    = pols_annuitization(12n−1)    for 12n ≤ t < 12n + 12m   the Rentengarantiezeit
                    = l(t)                         for t ≥ 12n + 12m
    annuity_payments(t) = annuity_pp(t) × a(t)

**The instalment is the product's own unit and the model now pays it as one.** The timing is
established — *"Wir zahlen die Rente monatlich, jeweils zum Monatsersten"* [S9] § 1 Abs. 1 — and the
annual grid these notes were first written for could only compress twelve of them into one
start-of-year payment, a **[std]** that is now gone. `U` steps once a year, on the anniversary,
because an *Überschussrente* is redeclared annually.

`a(t)` is the mechanic the *Rentengarantiezeit* consists of: inside the guarantee window the
instalment is due whether or not the annuitant is alive, so it is weighted by the **annuitised**
count and not by survivors [R17] [R24], and the window is `12m` **instalments**. Because
`l(t) ≤ pols_annuitization(12n−1)` throughout the payout phase,
`a(t) = max(l(t), 1{12n ≤ t < 12n+12m} × pols_annuitization(12n−1))`, which is how
`check_annuity_guarantee()` states it. Inside the window the annual and monthly grids give the same
money to the cent, the count being fixed; they part company after it, where twelve monthly
measurements of a falling count are not one annual one, and that difference is the whole −369,14 €
the conversion moved on the anchor cell.

### Expenses and the cash flow statement

    base(t)      = l(t)  for t < 12n,   a(t)  for t ≥ 12n
    expenses(t)  = expense_acq_pp × 1{t = t_start() and duration_init = 0}
                 + ( t < 12n ? expense_maint_pp : expense_annuity_pp ) / 12
                   × (1+expense_infl)^duration(t) × base(t)
                 + expense_claim_pp × ( pols_death(t) + pols_lapse(t) + pols_commutation(t) )

    net_cf(t)      = premiums(t) − claims_death(t) − claims_lapse(t) − claims_commutation(t)
                     − annuity_payments(t) − expenses(t)
    liability_cf(t) = − net_cf(t)

The administration expense is **a twelfth of the year's amount each month** rather than a monthly
level of its own, so a year of it on a closed cohort is exactly the annual grid's charge; the
inflation factor steps on the **anniversary**, because it compounds in policy years and a
twelfth-rooted inflation would be a different assumption wearing the same number. A policy leaving
mid-year now bears administration only for the months it was there, which is worth 23,00 € over the
anchor cell's run.

`result_cf()` returns a `DataFrame` indexed by the 0-based **month** `t` (`index.name == "t"`),
contiguous from `t_start()` to `proj_len() − 1`, with these columns **in this order**:

    pols_if, pols_annuity, premiums, claims_death, claims_lapse, claims_commutation,
    annuity_payments, expenses, liability_cf, net_cf

`result_cf_annual()` sums it into policy years, indexed by the 1-based `policy_year`, which is the
view the worked example above is stated on. The account movements `av`, `av_sur`, `prem_to_av`,
`int_credited` and `bonus_credited` are **state, not cash flows**, they move once a policy year, and
they live in `result_pols()` with the rest of the annual state: the *Sparbeitrag* and the two credits
move money inside the contract and never cross the boundary, and a cash flow statement whose columns
do not all sum to its bottom line is one a reader has to know which columns to skip. The six that do
cross the boundary are `premiums`, the three `claims_*`, `annuity_payments` and `expenses`, and those
six are exactly what `check_net_cf()` reconciles.

### The published identities

| Cells | Clock | Identity |
|---|---|---|
| `check_net_cf()` | month | `net_cf(t) = premiums − claims_death − claims_lapse − claims_commutation − annuity_payments − expenses`, and `liability_cf(t) = −net_cf(t)` |
| `check_pols_roll_fwd()` | month | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_commutation(t)`, and `pols_if(t) ≥ 0` |
| `check_decrement_closure()` | month | `Σ_t (pols_death + pols_lapse + pols_commutation) + pols_if(N) = pols_if_init()`, with `pols_if(N) = 0` — one past the last month — because `mort_rate` is 1 in the policy year at `omega_age − 1` |
| `check_av_roll_fwd()` | **year** | `av(k) + prem_to_av(k) − charge_from_av(k) + int_credited(k) + pup_uplift(k) − av_release(k) = av(k+1)` |
| `check_av_sur_roll_fwd()` | **year** | `av_sur(k) + bonus_credited(k) − av_sur_release(k) = av_sur(k+1)` |
| `check_prem_split()` | **year** | `prem_pp(k) = prem_to_av_pp(k) + charge_from_prem_pp(k)` and `charge_due_pp(k) = charge_from_prem_pp(k) + charge_from_av_pp(k)` |
| `check_cv_floor()` | **year** | `cv_pp(k) = max(cv_tariff_pp(k), cv_floor_pp(k))` and `cv_pp(k) ≥ cv_floor_pp(k)` [REG-R28] |
| `check_annuity_conv()` | scalar | `annuity_guar_mth_pp × 10 000 = capital_conv_pp × annuity_rate_appl()`, `annuity_rate_appl() = max(f_g, f_c) ≥ f_g`, and `capital_conv_pp ≥ guar_capital_pp` [S4] [S9] |
| `check_annuity_guarantee()` | month | `pols_annuity(t) = max(pols_if(t), 1{12n ≤ t < 12n+12m} × pols_annuitization(12n−1))` for `t ≥ 12n`, and `= 0` for `t < 12n` |

Each has a residual companion beside it, and **the residual's argument follows its cells' clock**:
`check_*_resid(t)` over months for the six monthly identities, `check_*_resid(k)` over policy years
for the four annual ones. A monthly residual for the *Deckungskapital* roll-forward would first have
had to invent a monthly reserve, which is the error the two-clock split exists to make impossible.
Each `check_*()` takes no argument and returns a `bool`. `check_net_cf()` is required of every delib
model by the library's first ruling and is asserted in `tests/test_model_conventions_de.py`.

---

## Processing order, on two clocks

**The annual block runs once per policy year `k`, at its start**, and is the whole of steps A1 to A6.
**The monthly block runs in every month `t` of that year**, and is steps M1 to M5. Steps A1 to A6 and
M3 run only in the accumulation phase; step A7 only at the boundary; step M4 only in the payout phase.

The annual block, for `k = k0 … N_y − 1`:

A1. **Open the year.** `age_y(k) = issue_age + k`, `calendar_year_y(k) = issue_year + k`. The opening
    state is `av_pp(k)`, `av_sur_pp(k)`, `spread_diff_pp(k)`, `alpha_cum_pp(k)` and `prem_cum_pp(k)`;
    the population is `pols_if(12k)`.
A2. **Test the phase and the elections.** Accumulation if `k < n`, payout if `k ≥ n`; `paid_up(k)` is
    true if `pup_year > 0 and k ≥ pup_year − 1`. If `k = pup_year − 1` and the contract is
    converting, `av_pp(k)` has already been reset to `pup_value_pp` by A1's recursion and
    `spread_diff_pp(k)` to zero; `pup_uplift(pup_year − 2)` — booked one year earlier, on the
    transition year — records the difference.
A3. **Premium in advance, decomposed.** `prem_pp(k)`, then `charge_acq_pp`, `charge_prem_pp`,
    `charge_admin_pp` and `charge_risk_pp` — the last two on **start-of-year** balances — then
    `charge_from_prem_pp`, `charge_from_av_pp` and the *Sparbeitrag* `prem_to_av_pp`.
A4. **Credit the *Deckungskapital* and accrue the guarantee.**
    `av_pp_at(k,"AFT_PREM") = av_pp(k) + prem_to_av_pp(k) − charge_from_av_pp(k)`, then
    `int_credited_pp(k) = int_rate_guar × av_pp_at(k,"AFT_PREM")` and `av_pp_at(k,"AFT_INT")`.
    **This is the [std] ordering** — premium, then charges, then interest on what is left. The
    retrieved wordings fix the *decomposition* ([S8] § 1 Abs. 2, [S11] § 27 Abs. 1) but none of them
    fixes the **within-year sequence**, which stays a standardization.
A5. **Credit the surplus.** `decl_rate(k)` from the declared-rate path,
    `bonus_rate(k) = max(0, decl_rate(k) − int_rate_guar)`, then `bonus_credited_pp(k)` to the
    *Ansammlungsguthaben*, at year end [R24].
A6. **Roll the spread account and strike the year's values.** `spread_diff_pp_at(k,"AFT_INT")`, hence
    `av_spread_pp_at(k,"AFT_INT")`, the surrender value `cv_pp(k)` and the death benefit `db_pp(k)`.
    These are what a claim in **any** month of the year is paid.
A7. **End of month `12n − 1` — the *Rentenbeginn*.** Strike `capital_gross_pp`, add `val_reserve_pp`,
    apply `max(guar_capital_pp, ·)` to get `K`; determine
    `f = max(annuity_rate_guar, annuity_rate_curr)`; split the survivors between
    `pols_commutation(12n−1)` and `pols_annuitization(12n−1)`; pay `claims(12n−1,"COMMUTATION")`;
    strike `G`. Both account balances go to zero.

The monthly block, for `t = t_start() … N − 1`:

M1. **Open the month.** `duration(t) = t // 12` selects the year's state; the population is
    `pols_if(t)`.
M2. **Look up the year's rates and twelfth them.** `mort_rate_guar(t)` from the generational surface
    at `(sex, age(t), calendar_year(t))`, `mort_rate(t) = mort_rate_guar(t) × mort_be_factor`,
    `lapse_rate(t)` from the duration table at `policy_year(t)` (zero if `duration(t) ≥ n`), then
    `mort_rate_mth(t)` and `lapse_rate_mth(t)`, each `1 − (1 − r)^(1/12)`.
M3. **Premium, where one is due.** `prem_due(t)` in the first month of the policy year;
    `premiums(t) = prem_pp(duration(t)) × pols_if(t)`.
M4. **Payout phase, start of the month.** `annuity_pp(t) = G + U(duration(t))` paid on
    `pols_annuity(t)`, which is the annuitised count inside the *Rentengarantiezeit* and survivors
    after it.
M5. **End of the month — decrements, expenses, publish.** Death at `mort_rate_mth(t)` paying
    `db_pp(duration(t))`; then surrender on the survivors at `lapse_rate_mth(t)` paying
    `cv_pp(duration(t))`. Where `duration(t) = pup_year − 2`, `pup_cashout` is true and `is_anniv(t)`,
    the **whole surviving cohort** leaves through the surrender decrement. Expenses: acquisition at
    `t = t_start()` for new business; a twelfth of the year's maintenance or annuity administration
    per policy on `base(t)`, inflated by policy year; settlement expense on the month's deaths,
    surrenders and commutations. Then `pols_if(t+1)`, and
    `net_cf(t) = premiums − claims_death − claims_lapse − claims_commutation − annuity_payments −
    expenses`, with `liability_cf(t) = −net_cf(t)`.

---

## Known modeling pitfalls

These are the specific ways an implementation of *this* product looks right and is wrong. Each one
becomes a test in `tests/test_klassische_rentenversicherung_de.py`.

1. **Adding the declared rate on top of the guarantee.** The *laufende Verzinsung* **is** the
   *Garantieverzinsung* plus the *laufende Zinsüberschussbeteiligung* [REG-R53]. Assert
   `int_credited_pp(k) + bonus_rate(k)·av_pp_at(k,"AFT_PREM") = decl_rate(k)·av_pp_at(k,"AFT_PREM")`
   whenever `decl_rate(k) ≥ int_rate_guar`, and that on model point 6 — a 2,75 % vintage against a
   2,55 % declaration — `bonus_rate(k) = 0` in every policy year while `int_credited_pp(k) > 0`. A model that
   credits 1,00 % **and** a further 2,55 % overstates the anchor cell's year-one
   crediting by 39 % (56,82 € against 40,82 €) and its accumulated value at *Rentenbeginn*
   by 8,5 % (63 768,69 € against 58 788,98 €), the whole of the error sitting in the
   *Ansammlungsguthaben* (12 698,26 € against 7 718,55 €).
2. **Getting the within-year order wrong.** Premium, then charges, then interest on the balance
   [std]. Crediting interest before the charges, or on the opening balance only, changes year-one
   interest by the whole of `i × (S(0) − C(0))`. Assert `int_credited_pp(k)` equals
   `int_rate_guar × av_pp_at(k,"AFT_PREM")` exactly, and that
   `av_pp_at(k,"AFT_INT") ≠ (av_pp(k))·(1+i) + S(k)` on the anchor cell.
3. **Applying only the guaranteed *Rentenfaktor*.** The rule is `max(guaranteed, current)` [S4]
   [R24]. Assert `annuity_rate_appl() = 32.00` on the anchor (the current factor wins) and
   `= annuity_rate_guar` on point 13 (the guarantee binds), and that
   `annuity_rate_appl() ≥ annuity_rate_guar` on every point. A model taking the guaranteed factor
   alone understates the anchor's annuity by 12,5 %.
4. **Weighting the guaranteed annuity by survivors.** Inside the *Rentengarantiezeit* the instalment
   is due whether the annuitant lives or not [R17] [R24]. Assert
   `pols_annuity(t) = pols_annuitization(12n−1)` for `12n ≤ t < 12n + 12m` and `= pols_if(t)` after,
   and that the two differ at `t = 12n + 12m − 1` on the anchor. Assert also that point 9, with
   `rgz_years = 0`, has `pols_annuity(t) = pols_if(t)` at every payout month. The window is `12m`
   **instalments**, which is what a *Rentengarantiezeit* guarantees.
5. **Treating *Beitragsfreistellung* as a lapse.** They are separate decrements with different
   consequences: the paid-up contract keeps its guarantee vintage and its guaranteed *Rentenfaktor*
   and pays a reduced benefit; the surrendered one is gone for cash [R1] [R2]. Assert that on point 7
   `pols_if` is unbroken through the paid-up year `k = pup_year − 1`, `prem_pp(k) = 0` from it,
   `int_rate_guar` is unchanged, and that the conversion itself moves **no** policy: `lapse_rate` in
   policy year `pup_year − 2` is the ordinary duration-9 table rate of 3,5 % and not 1, and
   `av_pp(pup_year − 1) = pup_value_pp > av_pp_at(pup_year − 2,"AFT_INT")`. What is **not** true is
   that surrender ceases: a *beitragsfrei* contract keeps its § 168 VVG *Kündigung* right, so
   `claims_lapse` stays positive from the paid-up year on — 764,60 € in policy year 10 on point 7 —
   and only the § 165 cash-out branch of point 8 empties the cohort, in the anniversary month of
   policy year `pup_year − 1`.
6. **Booking the *Kostenbeitrag* as an expense.** The charges are internal deductions that move money
   inside the contract; `expenses` is the insurer's best-estimate outgo. Assert
   `expenses(t) ≠ charge_due_pp(duration(t)) × pols_if(t)` and that `expenses(t)` is invariant to
   `beta_rate` and `gamma_rate`, while `av_pp(k+1)` is not. Double-counting them inflates outgo by
   the whole charge load and is the commonest way to make a German model look conservative.
7. **Computing the surrender value off the zillmered reserve.** § 169 Abs. 3 floors it at the reserve
   with acquisition costs spread evenly over the first five contract years [REG-R28]. Assert
   `cv_pp(k) = max(cv_tariff_pp(k), cv_floor_pp(k))`, that the floor **binds** in the anchor's early
   years and **stops binding** later, and that omitting it changes `claims_lapse` in the second
   policy year by the whole of `spread_diff_pp_at(1,"AFT_INT")`.
8. **Letting the *Stornoabzug* recover acquisition costs.** § 169 Abs. 5 permits a deduction only if
   agreed, quantified and appropriate, and voids one for unamortised acquisition costs [R1]
   [REG-R28]. Assert that `surr_charge_pp(k)` is a flat percentage of the pre-deduction value and
   carries **no** duration term, and that `cv_pp(k)` never falls below `cv_floor_pp(k)` however large
   `stornoabzug_rate` is set.
9. **Using one mortality basis where the product uses two.** The first-order basis fixes the risk
   charge and the guaranteed benefits; the second-order basis drives the projection [REG-R47].
   Assert `mort_rate(t) = mort_rate_guar(t) × mort_be_factor` with `mort_be_factor > 1`, that
   `charge_risk_pp` uses the **annual** `mort_rate_guar` while `pols_death` uses the **monthly**
   `mort_rate_mth` derived from `mort_rate`, and that swapping them changes `net_cf`. Assert also
   that `1 − (1 − mort_rate_mth(t))^12 = mort_rate(t)`: the twelfth is geometric, and dividing the
   annual rate by twelve instead would leave `pols_if` above the annual grid's at every anniversary.
10. **Using a period mortality table.** DAV 2004 R is a *Generationentafel*; a period-table proxy
    priced at an annuitisation decades ahead understates the liability by a margin that dwarfs every
    other assumption [REG-R49]. Assert `mort_rate_guar` depends on `calendar_year(t)` as well as
    `age(t)`: on the anchor, `mort_rate_guar` at attained age 67 in 2043 must be **strictly below**
    the same age's rate for a life reaching 67 in 2026.
11. **Charging the risk premium on a zero net amount at risk.** With
    `death_benefit_form = deckungskapital` the death benefit **is** the reserve, so there is nothing
    at risk. Assert `charge_risk_pp(k) = 0` in every policy year on points 2 and 12, and that
    `charge_risk_pp(k) > 0` in every accumulation year on the anchor, where the benefit is the
    premiums paid. On that cell the net amount at risk **rises** to a peak of 4 587,95 € at `k = 5`
    and then declines, ending the deferment at 3 204,24 € rather than at zero: with the whole 25 ‰
    zillmered out of year 1, a 4 % premium charge and a 1,00 % *Rechnungszins*, the
    *Deckungskapital* never overtakes the premiums paid inside seventeen years, which is precisely
    why *Beitragsrückgewähr* is real risk cover on this design and not a formality. The risk charge
    itself rises monotonically, from 4,37 € to 15,39 €, because first-order mortality more than
    triples over the deferment while the amount at risk moves by a third.
12. **Deducting the payout-phase administration charge from the annuity.** The *Rentenfaktor* is
    exogenous here and already carries the tariff's payout loading, so `annuity_admin_rate` is
    recorded in `charge_table.csv` and **not applied**. Assert
    `annuity_payments(t) = (G + U(duration(t))) × pols_annuity(t)` exactly, with no charge term, and
    that the model's payout-phase `expenses` are a twelfth of the inflated per-policy
    `expense_annuity_pp` on the exposed count plus the `expense_claim_pp` settlement cost of that
    month's deaths, and nothing else. The settlement line survives into the
    payout phase although the death pays no benefit, because stopping an annuity and running the
    *Rentengarantiezeit* succession is administration the insurer still performs.
13. **Paying a death benefit after *Rentenbeginn*.** The reference model pays none:
    `claims_death(t) = 0` for every `t ≥ 12n` on every model point, and the test asserts it. **This is
    now a modelling choice, not an absence of evidence.** [S4] § 1 Abs. 5 offers *Beitragsrückgewähr
    während der Rentenzahlungszeit* as an alternative to the *Rentengarantiezeit* — premiums paid
    less rider premiums less annuities already received at their inception-guaranteed level, the
    claim extinguishing once instalments exceed premiums — and § 3 Abs. 7 accumulates the surplus
    attributable to it with interest until it is paid or the claim lapses. Modelling it would add a
    second post-*Rentenbeginn* benefit path and move the worked example, so it is recorded here and
    **deliberately left out of this pass**. The other two documented mechanics are the
    *Rentengarantiezeit* [S1] [S4] [S9] and the survivor's-annuity rider, which begins only after any
    guarantee period expires [S10] § 1 Abs. 3.
14. **Letting the *Kapitalwahlrecht* leave the account behind.** Commuting policyholders receive
    `capital_conv_pp` — the same capital annuitants convert, *Bewertungsreserven* included [S9].
    Assert `claims_commutation(12n−1) = capital_conv_pp × kapitalwahl_rate × pols_surv_rb`, that
    both account balances are zero from `k = n`, and that on point 9 (`kapitalwahl_rate = 1.00`)
    `pols_if(t) = 0` and every cash flow is zero for `t ≥ 12n`.
15. **Forgetting that the guarantee vintage is a model-point attribute.** Existing contracts keep the
    *Rechnungszins* they were written on [R7] [REG-R14]. Assert that points 1, 6 and 14 credit
    1,00 %, 2,75 % and 0,90 % respectively, and that re-running point 6 on a single global 1,00 %
    rate moves its *Deckungskapital* at `Rentenbeginn` from 82 833,38 € to 76 439,87 €, −7,7 %,
    while its *Ansammlungsguthaben* goes the other way, 3 629,35 € to 9 292,76 €, +156 %. The
    conversion capital barely moves — 87 759,66 € against 87 018,62 €, −0,8 % — which is the point:
    a single global rate leaves the *total* looking almost right and puts the money in the wrong
    account, where it carries no guarantee.
16. **Letting `sex` reach the tariff.** Unisex has been compulsory since 21 December 2012
    [REG-R34]. Assert that two model points identical but for `sex` produce identical `prem_pp`,
    identical `charge_*` except through `mort_rate_guar`, and identical `annuity_rate_appl()`.
17. **Amortising the acquisition charge against a shrunken *Beitragssumme*.** The § 4 DeckRV base is
    the sum of all premiums payable under the contract as written [REG-R16], not the premiums a later
    *Beitragsfreistellung* leaves behind. Assert `alpha_total_pp` on point 7 is unchanged by
    `pup_year`, and that `alpha_cum_pp` never exceeds `alpha_total_pp`.
18. **Truncating the payout phase.** A life annuity has no term; `proj_len() = omega_age −
    issue_age`. Assert `result_cf().index[-1] == proj_len() − 1`, that `pols_if(proj_len()) = 0` —
    one past the last row — and that the decrement closure sums to `pols_if_init()` exactly. A 40-year horizon on the anchor cell
    would drop a real, if small, tail of annuity payments beyond attained age 90.

---

## Policyholder behaviour modelling

Every formula here is **[std]**; nothing in the corpus calibrates any of it (gap 20).

- **Base surrender.** The duration table above, with the **duration-12 step** at the § 20 Abs. 1
  Nr. 6 EStG twelve-year threshold [R6] [REG-R45]. The shape is the assumption; the levels are
  placeholders. A German Schicht-3 projection with a lapse rate flat in duration has ignored the
  strongest single driver of German surrender behaviour.
- **No dynamic surrender.** The obvious German dynamic term would key the surrender rate on the gap
  between a market rate and the declared *laufende Verzinsung*, as frlib's euro-fund model keys it on
  the Livret A gap. It is **not implemented here**, for a reason worth stating: on this product the
  policyholder who surrenders forfeits a *guaranteed Rentenfaktor* struck on bases decades old, and
  the value of that forfeited option is exactly what a rate-gap formula does not capture. A model
  that adds a naive rate-gap term to a book of 4,00 % vintages will lapse precisely the contracts a
  real policyholder would never surrender.
- ***Beitragsfreistellung* as an election, not a rate.** A scalar per-policy account cannot carry two
  sub-populations with different *Deckungskapital*, and splitting the account would double the
  accumulation-phase state for a mechanic whose rate no source establishes. The model therefore
  carries `pup_year` as a **deterministic election** on the model point, exercises both of its
  statutory branches (conversion, and cash-out below the *Mindestversicherungsleistung*) on points 7
  and 8, and says here that a portfolio model needs the sub-population split this one does not have.
- **The *Kapitalwahlrecht* as a take-up rate.** `kapitalwahl_rate` is a model-point attribute, base
  30 % [std]. The decision it stands for is a tax comparison — the *Ertragsanteil* at 18 % of each
  instalment against half the *Unterschiedsbetrag* once [R5] [R6] [REG-R41] [REG-R45] — and **this
  model computes no tax**, so the rate is a stand-in for a calculation it does not perform, not an
  estimate of one.
- **What is deliberately absent.** No *Widerruf* decrement (it sits inside the year-1 lapse rate,
  [REG-R23]); no premium-default path, although § 166 VVG makes German lapse a **three-way**
  decrement in reality [REG-R28] [REG-R30]; no *Wiederinkraftsetzung* [S11]; no selective-lapsation
  mortality loading; and no take-up modelling for the *Dynamik*, whose parameters are unestablished
  (gap 15).

---

## Worked example

**Configuration.** Model point 1, `point_id = 1`, `policy_id = DE-RV-0001`: `sex = M`;
`issue_age = 50`; `issue_year = 2026`; `duration_init = 0`, so the frame opens at `t = 0`;
`pols_if_init = 1.0`; `premium_form = laufend`; `prem_gross_pp = 3 000,00 €`;
`premium_single_pp = 0,00 €`; `prem_freq = annual`, hence `freq_load = 1,000`; `prem_term_y = 17`;
`aufschub_y = 17`, so the *Rentenbeginn* falls at the end of month `t = 203` — the end of the
seventeenth policy year — at attained age 67;
`int_rate_guar = 1,00 %`, the 2026 vintage [REG-R15]; `charge_id = zillmer_25`;
`annuity_rate_guar = 28,00 €` per month per 10 000 €; `rf_scenario_id = base`;
`decl_scenario_id = base`; `guar_capital_pp = 0,00 €`, so the guaranteed-contract-value floor is
inoperative on this cell; `death_benefit_form = prem_refund`; `db_incl_surplus = 0`;
`rgz_years = 10`; `kapitalwahl_rate = 0,30`; `pup_year = 0`; `dynamik_rate = 0,0000`;
`payout_system = konstant`; `av_pp_init = 0,00 €`; `av_sur_pp_init = 0,00 €`;
`prem_cum_pp_init = 0,00 €`; `alpha_amort_pp_init = 0,00 €`. Hence `proj_len_y() = 121 − 50 = 71`
and `proj_len() = 852`, so the frame is `t = 0 … 851`: the accumulation phase is `t = 0 … 203`, the
*Rentengarantiezeit* covers `t = 204 … 323` — a hundred and twenty guaranteed instalments — and the
survivor-weighted annuity runs from `t = 324` to `t = 851`.

**Assumptions, each tagged.** *Contractual and cited:* the *Rechnungszins* `i = 1,00 % p.a.`
[REG-R15]; the *Höchstzillmersatz* `alpha_rate = 25 ‰` of the *Beitragssumme* [REG-R16], giving
`beitragssumme_pp = 17 × 3 000,00 = 51 000,00 €` and `alpha_total_pp = 1 275,00 €`, zillmered — taken
in full from the first year's premium and nil thereafter; the § 169 Abs. 3 five-year spread,
`alpha_spread_years = 5`, giving `α̃(k) = 255,00 €` for `k = 0 … 4` [REG-R28]; the § 165
*Mindestversicherungsleistung* test, not triggered on this cell [R2]; the death benefit
*Beitragsrückgewähr*, the premiums paid to date, premiums only [S1] [R24]; the conversion rule
`monthly annuity = capital / 10 000 × Rentenfaktor` [R24]; and the applied factor
`max(garantiert, aktuell)` [S4] [R24]. *Insurer-discretionary current:* the declared *laufende
Verzinsung* `decl_rate = 2,55 % p.a.` level on the `base` path **[std]**, hence
`bonus_rate = max(0; 2,55 % − 1,00 %) = 1,55 % p.a.` **[std]**, with the *Ansammlungsguthaben*
itself credited at the full 2,55 % **[std]**; the *Bewertungsreserven* crystallisation
`val_reserve_rate = 1,5 %` of the accumulated value at *Rentenbeginn* **[std]** [S4] [R4]; the
*aktueller Rentenfaktor* at age 67 on the `base` path, `32,00 €` per month per 10 000 € **[std]**,
which exceeds the guaranteed `28,00 €` and therefore wins the `max()`; and the *Überschussrente*
under the `konstant` system, `sur_ann_rate = 12 %` of the *garantierte Rente*, level **[std]**.
*Charges (all levels [std]):* `beta_rate = 4,0 %` of each gross premium; `gamma_rate = 0,20 % p.a.`
of the *Deckungskapital*; the *Risikobeitrag* `ρ(k) = mort_rate_guar(12k) × max(0, prem_cum_pp(k) +
prem_pp(k) − av_pp(k))`; `stornoabzug_rate = 2,0 %` of the pre-deduction value, subject to the
§ 169 Abs. 3 floor [R1] [REG-R28]; `annuity_admin_rate = 1,5 %`, recorded and **not applied**
(pitfall 12). *Behavioural and experience (all [std]):* first-order mortality from the shipped
generational proxy, `mort_rate_guar(t) = q_base(M, x(t)) × (1 − improve(x(t)))^(τ(t) − 2005)`,
annual and flat across a policy year, with
the anchor `q_base(M, 50) = 0,002000` and `improve(x) = 1,5 %` below age 60 grading to 0,5 % at 100
and to zero at 110; best-estimate mortality `mort_rate(t) = mort_rate_guar(t) × 1,15`; surrender
6,0 % / 5,0 % / 4,5 % / 4,0 % (durations 4–7) / 3,5 % (8–11) / **6,0 % at duration 12** / 3,0 %
thereafter, and **zero from *Rentenbeginn***; the *Kapitalwahlrecht* take-up 30 %; and expenses of
400,00 € acquisition at issue, 45,00 € per policy p.a. in the accumulation phase and 30,00 € p.a. in
the payout phase, both inflating at 2,0 % p.a., plus 120,00 € per death, surrender or commutation
event. `omega_age = 121` **[std]**. No *Dynamik*, no *Beitragsfreistellung*, no
*guar_capital_pp* floor, no behavioural modules.

**The frame.** The model projects **months**; the table below is
`RV_DE_S.Projection[1].result_cf_annual()`, the monthly frame summed into policy years, which is the
only view on which a year's worth of arithmetic can be read at once. Money to the cent and `pols_if`
to six decimals. The index is written as the 0-based policy year `k = policy_year − 1`, so row `k`
covers months `12k … 12k + 11`. Rows 0–16 are the whole accumulation phase; rows 17, 26, 27, 39, 54
and 70 sample the payout at the first annuity year, the last guaranteed year, the first
survivor-weighted year and three points down the tail. `av` and `av_sur` are the two balances at the
**start** of the row's year, for the model point as a whole, taken from `result_pols()`; they are
state rather than cash flow and they move once a year, which is why they are not columns of
`result_cf()`.

| k | pols_if | av | av_sur | premiums | claims_death | claims_lapse | claims_commutation | annuity_payments | expenses | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 0.00 | 0.00 | 3,000.00 | 4.88 | 158.67 | 0.00 | 0.00 | 451.10 | 2,385.34 |
| 1 | 0.938426 | 1,517.10 | 23.28 | 2,815.28 | 9.89 | 249.12 | 0.00 | 0.00 | 47.87 | 2,508.41 |
| 2 | 0.889902 | 4,032.52 | 84.53 | 2,669.71 | 15.14 | 320.11 | 0.00 | 0.00 | 45.76 | 2,288.69 |
| 3 | 0.848216 | 6,335.16 | 179.84 | 2,544.65 | 20.70 | 362.97 | 0.00 | 0.00 | 43.99 | 2,116.98 |
| 4 | 0.812600 | 8,474.57 | 306.74 | 2,437.80 | 26.62 | 445.58 | 0.00 | 0.00 | 42.92 | 1,922.68 |
| 5 | 0.778360 | 10,439.40 | 461.52 | 2,335.08 | 32.85 | 526.51 | 0.00 | 0.00 | 41.87 | 1,733.85 |
| 6 | 0.745440 | 12,238.83 | 641.09 | 2,236.32 | 39.41 | 601.95 | 0.00 | 0.00 | 40.83 | 1,554.13 |
| 7 | 0.713787 | 13,881.56 | 842.56 | 2,141.36 | 46.41 | 588.10 | 0.00 | 0.00 | 39.48 | 1,467.37 |
| 8 | 0.686908 | 15,455.93 | 1,068.70 | 2,060.72 | 53.95 | 648.43 | 0.00 | 0.00 | 38.70 | 1,319.64 |
| 9 | 0.660906 | 16,904.27 | 1,313.89 | 1,982.72 | 61.92 | 705.09 | 0.00 | 0.00 | 37.94 | 1,177.77 |
| 10 | 0.635750 | 18,232.03 | 1,575.91 | 1,907.25 | 70.35 | 758.18 | 0.00 | 0.00 | 37.18 | 1,041.55 |
| 11 | 0.611408 | 19,444.42 | 1,852.62 | 1,834.22 | 78.94 | 1,384.79 | 0.00 | 0.00 | 37.86 | 332.64 |
| 12 | 0.572603 | 20,013.45 | 2,086.42 | 1,717.81 | 87.98 | 713.03 | 0.00 | 0.00 | 34.50 | 882.30 |
| 13 | 0.553206 | 21,091.10 | 2,390.82 | 1,659.62 | 99.18 | 752.73 | 0.00 | 0.00 | 33.97 | 773.74 |
| 14 | 0.534287 | 22,078.63 | 2,706.76 | 1,602.86 | 111.26 | 790.09 | 0.00 | 0.00 | 33.43 | 668.08 |
| 15 | 0.515827 | 22,978.50 | 3,032.52 | 1,547.48 | 124.27 | 825.12 | 0.00 | 0.00 | 32.90 | 565.19 |
| 16 | 0.497806 | 23,793.00 | 3,366.34 | 1,493.42 | 138.27 | 857.84 | 8,596.26 | 0.00 | 49.65 | −8,148.61 |
| 17 | 0.336143 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 862.65 | 14.36 | −877.01 |
| 26 | 0.311032 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 862.65 | 17.36 | −880.01 |
| 27 | 0.307034 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 782.87 | 16.14 | −799.01 |
| 39 | 0.229120 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 576.71 | 15.74 | −592.45 |
| 54 | 0.055062 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 128.34 | 5.64 | −133.99 |
| 70 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | −0.00 |
| **Total** | — | — | — | **35,986.30** | **1,022.04** | **10,688.30** | **8,596.26** | **23,115.89** | **1,646.77** | **−9,082.96** |

At the start of policy year 71 the surviving fraction is 2,15 × 10⁻⁷ and every cash flow rounds to
nil; the year is kept because `result_cf().index[-1] == proj_len() − 1` is a machine-checked property
of this library, and because `pols_if(852)` — one past the last month — is the exact zero the closure
identity below needs.

**The Total row is summed over all 852 months at full precision and then rounded**, not summed from
the rounded cells, and the two differ: summing the 71 rounded annual rows gives `net_cf` =
−9 082,97 € against −9 082,96 €. The largest single-column gap is `annuity_payments`, 23 115,83 €
against 23 115,89 €; `claims_death` and `expenses` each lose two cents likewise. No rounded quantity
is re-used anywhere: every row is computed at full precision and rounded once, at the point of
display.

The shape is a long positive accumulation phase, a −8 148,61 € spike in policy year 17 where the
*Kapitalabfindung* falls on 30 % of the survivors, and a negative annuity tail running another
fifty-four years. Undiscounted, the cell collects 35 986,30 € and pays out 45 069,26 €.

**What the monthly grid moved, against the annual-step model this replaced.** Premiums are
**identical** — 35 986,30 € — and so is every account balance, every surrender value and the
conversion capital: the whole annual layer is bit-identical, on all fourteen model points. Three
columns moved, each for a reason:

| Column | Annual grid | Monthly grid | Why |
|---|---|---|---|
| `annuity_payments` | 23 485,03 € | **23 115,89 €** | Twelve instalments paid through the year on a cohort that loses lives, instead of twelve paid at the start of it. Inside the *Rentengarantiezeit* the two agree to the cent — 862,65 € a year — because the count is fixed there; the whole −369,14 € is in the survivor-weighted tail |
| `claims_death` | 1 038,91 € | **1 022,04 €** | Deaths and surrenders now compete month by month rather than once a year |
| `claims_lapse` | 10 670,70 € | **10 688,30 €** | The other side of the same shift: total exits are unchanged at every anniversary, the split is not |
| `expenses` | 1 669,77 € | **1 646,77 €** | A policy leaving mid-year bears administration for the months it was there |

### Independent checks

These rebuild table cells a **different way** — from the tariff parameters rather than from the
recursion — in arithmetic a reader can follow with a calculator.

**Check 1 — the first policy year, `k = 0`, from the tariff parameters alone.** The account
arithmetic is annual and nothing here reads the model:

    Beitragssumme = 17 x 3,000.00                         = 51,000.00
    alpha_total   = 0.025 x 51,000.00                     =  1,275.00  (P(0) covers it: all in year 1)
    beta(0)       = 0.040 x 3,000.00                      =    120.00
    gamma(0)      = 0.0020 x 0.00                         =      0.00  (the account is empty)
    q*(0)         = 0.002000 x (1 - 0.015)^(2026-2005)
                  = 0.002000 x 0.72804940                 = 0.00145610
    rho(0)        = 0.00145610 x (0.00 + 3,000.00 - 0.00) =      4.3683
    charges due   = 1,275.00 + 120.00 + 0.00 + 4.3683     =  1,399.3683  (all met from the premium)
    S(0)          = 3,000.00 - 1,399.3683                 =  1,600.6317
    int_credited  = 0.0100 x 1,600.6317                   =     16.0063
    V at year end = 1,600.6317 + 16.0063                  =  1,616.6380
    Delta after 0 = (0.00 + 1,275.00 - 255.00) x 1.01     =  1,030.2000
    cv_floor(0)   = 1,616.6380 + 1,030.2000               =  2,646.8380
    cv_tariff(0)  = (1,616.6380 + 24.8098) x 0.98         =  1,608.6189  (the floor wins)

Every line of that is unchanged from the annual-step model, which is the point of the two-clock
split. The **decrements** are where the month enters, and the year's totals are a sum of twelve:

    q(0)          = 0.00145610 x 1.15                     = 0.00167451   annual
    q^m(0)        = 1 - (1 - 0.00167451)^(1/12)           = 0.00013965   monthly
    w(0)          = table duration 1                      = 0.06         annual
    w^m(0)        = 1 - (1 - 0.06)^(1/12)                 = 0.00514301   monthly
    deaths, mth 0 = 1.000000 x 0.00013965                 = 0.00013965
    lapses, mth 0 = (1.000000 - 0.00013965) x 0.00514301  = 0.00514229
    deaths, yr 0  = sum over the twelve months            = 0.00162796
    lapses, yr 0  = sum over the twelve months            = 0.05994608
    claims_death  = 3,000.00 x 0.00162796                 =      4.8839
    claims_lapse  = 2,646.8380 x 0.05994608               =    158.6676
    expenses(0)   = 400.00 + sum of twelve x 45.00/12 x l
                    + 120.00 x 0.06157405                 =    451.1043
    net_cf, yr 0  = 3,000.00 - 4.8839 - 158.6676 - 451.1043 = 2,385.3442

which is the table's first row to the cent. Two things to read off it. The twelve monthly deaths sum
to 0,001628 against the annual grid's 0,001675 and the twelve monthly lapses to 0,059946 against
0,059900 — the **competing-decrement shift**, and the survivors at the anniversary are the same
0,938426 either way, because `(1 − q^m)^12 (1 − w^m)^12 = (1 − q)(1 − w)` exactly. And the surrender
value the leavers are paid is `cv_pp(0)` in every month of the year, § 169 Abs. 3 VVG striking it at
the **end** of the *Versicherungsperiode*.

The load-bearing line of the annual block is the seventh: the acquisition charge takes 42,5 % of the
year-one premium, leaving a *Sparbeitrag* of 1 600,63 €, and the § 169 Abs. 3 floor then stands
1 030,20 € **above** the tariff *Deckungskapital* at the end of the first year. That gap is the whole
of *Zillmerung* in one line, and it is why the floor binds through policy year 4 and stops binding in
policy year 5.

**Check 2 — the declared rate contains the guarantee.** The two credits are struck on the same base
and must together be the declared rate, never the declared rate on top of the guarantee:

    guarantee  0.0100 x 1,600.6317 = 16.0063170368
    surplus    0.0155 x 1,600.6317 = 24.8097914070
    sum                             = 40.8161084438
    declared   0.0255 x 1,600.6317 = 40.8161084438     identical to ten decimals

A model crediting 1,00 % **and** a further 2,55 % puts 56,82 € into the first year instead of
40,82 €, 39 %
too much; rolled forward on the same premium and charge schedule that reaches 63 768,69 € of
accumulated value at *Rentenbeginn* against the correct 58 788,98 €, an 8,5 % overstatement sitting
entirely in the *Ansammlungsguthaben* (12 698,26 € against 7 718,55 €). The mirror image is model
point 6 below.

**Check 3 — the *Rentenbeginn*, rebuilt from the two balances.** At the end of month `t = 203` — the
end of the seventeenth and last accumulation year — the *Deckungskapital* stands at 51 070,4278 € per
policy and the *Ansammlungsguthaben* at 7 718,5532 €:

    capital_gross  = 51,070.4278 + 7,718.5532           = 58,788.9809
    val_reserve    = 0.015 x 58,788.9809                =    881.8347
    K              = max(0.00, 58,788.9809 + 881.8347)  = 59,670.8156
    f              = max(28.00, 32.00)                  =     32.00    (the current factor wins)
    G              = 59,670.8156 / 10,000 x 32.00       =    190.9466  EUR a month
    U              = 0.12 x 190.9466                    =     22.9136  EUR a month
    annuity_pp     = 190.9466 + 22.9136                 =    213.8602  EUR a month, in advance
    pols_surv_rb   = 0.481648 - 0.000222 - 0.001220     =   0.480205
    commutations   = 0.30 x 0.480205                    =   0.144061
    claims_commut. = 59,670.8156 x 0.144061             =  8,596.2645
    annuitisations = 0.70 x 0.480205                    =   0.336143   = pols_if(204)
    annuity_pay    = 213.8602 x 0.336143                =     71.8877  EUR a month
                     x 12 months of the guarantee       =    862.6523  EUR in policy year 18

matching the table at policy years 17 and 18. The instalment is the product's own unit, and the
annual figure is now a **sum of twelve of them** rather than a year's annuity paid at once; inside
the *Rentengarantiezeit* the count is fixed, so the year's total is the same 862,65 € the annual grid
gave and the two models agree to the cent. They part company from policy year 28, where the count is
survivors and twelve monthly measurements of it are not one annual one. Applying the guaranteed
28,00 € instead would give G = 167,0783 €, 87,5 % of the right answer and 12,5 % of the whole payout
phase lost, the annuity scaling linearly in `f`.

**Closure, twice.** The decrements account for the whole policy — summed over all 852 months at full
precision, deaths 0,371014 + surrenders 0,484924 + commutations 0,144061 + survivors at
`t = 852` — one past the last month — 0,000000 = 1,000000 exactly, against
`pols_if_init() = 1,000000`. The survivor term is exactly zero because `mort_rate` is 1 in the policy
year at attained age 120 = `omega_age() − 1`, which is what makes `proj_len_y() = omega_age() −
issue_age` the right horizon: a 40-year run would strand 0,219599 of a policy at attained age 90 and
silently drop most of the tail of the payout phase. And the account rolls forward — in policy year 0,
at fund level, `0.00 + 1,600.6317 − 0.00 + 16.0063 − 99.5429 = 1,517.0951 = av(1)`, where 99,5429 €
is the end-of-year balance of 1 616,6380 € carried out by the 0,061574 of a policy that died or
surrendered **at any point in the year**. The same identity closes in every policy year, including
across the *Rentenbeginn*, where `av_release(16)` is the **whole** balance. That is
`check_av_roll_fwd()`, and it is stated per policy **year**: the *Deckungskapital* is defined at
anniversaries, so a monthly residual for it would first have had to invent a monthly reserve.

**One thing the table does not show, and it is the point of the *Rentengarantiezeit*.** In policy
year 27, the last guaranteed year, `pols_annuity` is 0,336143 — the count that annuitised — in every
one of its twelve months, while `pols_if` has fallen to 0,307366 by the last of them. The instalment
is due either way, so the year's outgo is 862,65 € and not the roughly 800 € a survivor weighting
would give. From policy year 28 the two coincide. `check_annuity_guarantee()` asserts it in every
month of every model point.

#### Variant A — the *Einmalbeitrag* form (model point 2)

A 55-year-old woman paying a single 50 000,00 € premium for a twelve-year deferment to the same
attained age 67, with `death_benefit_form = deckungskapital` and `kapitalwahl_rate = 0.00`.

| k | pols_if | av | av_sur | premiums | claims_death | claims_lapse | annuity_payments | expenses | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 0.00 | 0.00 | 50,000.00 | 76.88 | 2,891.05 | 0.00 | 451.10 | 46,580.97 |
| 1 | 0.938426 | 44,310.12 | 680.01 | 0.00 | 78.45 | 2,267.01 | 0.00 | 47.87 | −2,393.33 |
| 11 | 0.611187 | 31,246.12 | 5,757.88 | 0.00 | 117.65 | 2,222.96 | 0.00 | 37.85 | −2,378.46 |
| 12 | 0.572308 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1,548.54 | 22.06 | −1,570.60 |
| 23 | 0.532497 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1,433.87 | 25.74 | −1,459.61 |
| 39 | 0.370668 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 982.17 | 25.57 | −1,007.74 |
| 65 | 0.000285 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.77 | 0.07 | −0.84 |
| **Total** | — | — | — | **50,000.00** | **1,128.88** | **21,374.96** | **46,844.86** | **1,908.71** | **−21,257.42** |

Totals again at full precision then rounded; the rounded-cell `net_cf` is −21 257,45 €. Three things
read off it. The *Beitragssumme* is the single premium, so `alpha_total_pp` is 1 250,00 € and the
first year's *Sparbeitrag* is 46 750,00 € — 93,5 % of the premium against the anchor's 53,4 %, which is
the whole economic difference between the two forms. The net amount at risk is **identically zero**
in every policy year, the benefit being the *Deckungskapital* itself, so the *Risikobeitrag* disappears from
the decomposition. And the conversion capital is 62 913,28 € against the anchor's 59 670,82 €, a
*garantierte Rente* of 201,32 € a month, on a contract that paid 50 000,00 € once rather than
51 000,00 € over seventeen years.

#### Variant B — the 2,75 % legacy vintage (model point 6)

An in-force contract written in 2005 on a 2,75 % *Rechnungszins* and the 40 ‰ *Höchstzillmersatz*,
twenty policy years elapsed, so the frame opens at `t_start() = 240` — policy year 21 — and the
*Rentenbeginn* falls at the end of month 299, the end of policy year 25.
Its opening balances are the balances this model's own recursion produces for the same contract run
from inception, so the cell is the continuation of a projectable contract rather than a guess.

| k | pols_if | av | av_sur | premiums | int_credited | bonus_credited | claims_death | claims_lapse | claims_commutation | annuity_payments | net_cf |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 20 | 1.000000 | 61,190.90 | 3,200.00 | 2,592.00 | 1,747.81 | 81.60 | 259.29 | 2,052.23 | 0.00 | 0.00 | 210.52 |
| 21 | 0.965315 | 63,039.53 | 3,167.78 | 2,502.10 | 1,796.18 | 80.78 | 283.18 | 2,104.86 | 0.00 | 0.00 | 45.22 |
| 22 | 0.931471 | 64,758.71 | 3,134.66 | 2,414.37 | 1,841.04 | 79.93 | 308.66 | 2,153.51 | 0.00 | 0.00 | −115.50 |
| 23 | 0.898434 | 66,348.31 | 3,100.58 | 2,328.74 | 1,882.41 | 79.06 | 335.83 | 2,198.15 | 0.00 | 0.00 | −271.80 |
| 24 | 0.866171 | 67,807.93 | 3,065.46 | 2,245.12 | 1,920.26 | 78.17 | 364.77 | 2,238.75 | 21,974.56 | 0.00 | −22,428.44 |
| 25 | 0.584254 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 2,343.02 | −2,372.27 |
| 49 | 0.342195 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 1,337.26 | −1,365.93 |
| 78 | 0.000000 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | −0.00 |
| **Total** | — | — | — | **12,082.32** | **9,187.70** | **399.55** | **1,551.74** | **10,747.50** | **21,974.56** | **60,594.20** | **−84,230.73** |

Two columns appear here that the anchor table omits, `int_credited` and `bonus_credited`, because
their **ratio** is the point. Over the five remaining accumulation years the contract is credited
9 187,70 € of guaranteed interest and 399,55 € of surplus — and every euro of that surplus is the
declared 2,55 % paid on the *Ansammlungsguthaben*'s **own** balance. Not one cent is interest surplus
on the *Deckungskapital*: `bonus_rate = max(0; 2,55 % − 2,75 %) = 0` in every policy year, because a contract
already guaranteed more than the insurer is declaring receives no interest surplus at all. A model
with one global *Rechnungszins* cannot produce that row; a model that adds the declared rate to the
guarantee produces its opposite. The same cell shows the other legacy asymmetry: a *garantierter
Rentenfaktor* of 34,00 € struck on 2005 bases **beats** the current 32,00 €, so the
`max(garantiert, aktuell)` resolves to the guarantee; and the 40 ‰ charge set carries no
*Stornoabzug*, so `cv_pp(20)` is the undeducted 68 586,25 € against a § 169 Abs. 3 floor of
65 304,65 €, inoperative twenty years in.

#### What changed in these notes, and why

Five statements written before the model existed did not survive contact with it, and were corrected
here rather than worked around in the model. (i) ***`pup_uplift` moved one row earlier***, to the
transition year `k = pup_year − 2`: the fund-level roll-forward needs it there, or
`check_av_roll_fwd()` fails by the whole uplift. The amount is unchanged. (ii) ***Pitfall 5 no
longer asserts that the surrender claim in the paid-up row is zero***: a *beitragsfrei* contract
keeps its § 168 VVG *Kündigung* right, so ordinary surrender continues after a
*Beitragsfreistellung* — 764,60 € in policy year 10 on point 7 — and what distinguishes the election from
a lapse is that the conversion itself moves no policy. (iii) ***Pitfall 1's and pitfall 11's magnitudes were wrong for this
parameterisation*** and now carry the model's own figures: the double-credit error is 8,5 % of the
accumulated value rather than "more than half" of the *Deckungskapital*, and the anchor's net amount
at risk **rises** to 4 587,95 € at `k = 5` and ends the deferment at 3 204,24 € rather than falling
towards zero. (iv) ***Pitfall 15's "more than a fifth" was wrong***, and wrong in an interesting
direction: re-running point 6 on a global 1,00 % rate moves its *Deckungskapital* at *Rentenbeginn*
by −7,7 % and its *Ansammlungsguthaben* by +156 %, while the conversion capital moves by −0,8 %.
The vintage error is a **misallocation between the two accounts**, not a hole in the total, which
is why it survives a reasonableness check on the headline figure. (v) ***Pitfall 12 overstated the
payout-phase expense***: `expenses(t)` there is the inflated `expense_annuity_pp` on the exposed
count **plus** the `expense_claim_pp` settlement cost of that month's deaths, which is a small
percentage of the line in the first payout year and grows with mortality down the tail.

---

## Valuation and reserve pointers

This library publishes gross best-estimate-style liability cash flows, undiscounted, on a declared
grid. The valuation layers consume them and are cited, never reproduced.

- **The German statutory *Deckungsrückstellung*.** The HGB reserve of § 341f HGB, computed
  prospectively **on the *Rechnungsgrundlagen* of the premium calculation** [REG-R54] and discounted
  at no more than the § 2 DeckRV rate applicable when the contract was concluded [REG-R14]. It is
  **not** the Solvency II best estimate: an insurer carries two liability measures, and the
  *Überschussbeteiligung*, the *Zinszusatzreserve* and the § 139 VAG *Bewertungsreserven* test all
  run on the **HGB** side [REG-R14] [REG-R54]. `av_pp(t) × pols_if(t)` is this model's contribution
  to that line, not the line itself — a statutory *Deckungskapital* is a prospective reserve on
  first-order bases while `av_pp` is a retrospective account roll-forward, and the two coincide only
  under assumptions this model does not impose.
- **The *Zinszusatzreserve*.** Arises where the § 5 Abs. 3 DeckRV *Referenzzins* falls below a
  contract's tariff rate, and the § 12 MindZV *Sicherungsbedarf* test compares a Bundesbank month-end
  swap rate with **the highest *Rechnungszins* applicable to the contract over the next fifteen
  years** — a window that bites hardest on annuity business [REG-R17] [REG-R18]. Model points 6 and
  14, on 2,75 % and 0,90 % vintages, are exactly the cells that would carry one. **Not computed.**
- **The surplus layer.** The MindZV's 90 / 90 / 50 minima are a minimum **transfer to the RfB**, not
  a minimum payout [REG-R18] [REG-R10] [REG-R19]. This model represents the **credited outcome** —
  `decl_rate` and the *Ansammlungsguthaben* — not the three result sources that fund it; a model of
  the surplus chassis itself belongs in delib's `kapitallebensversicherung`.
- **Solvency II.** Best estimate plus risk margin [REG-R6], `BEL = Σ_t v(t) × liability_cf(t)` over
  the stream this model publishes, with the future discretionary benefits — the surplus credit and
  the *Bewertungsreserven* crystallisation — the substance of the calculation. **No risk-free curve,
  cost-of-capital rate or contract-boundary rule in this library was read from a retrieved
  instrument** [REG-R2] [REG-R4], so every such figure would be [std]. And **the guarantees are
  options**: the `max(guaranteed, current) Rentenfaktor` [S4] is a written option on the insurer's
  own future annuity tariff and the *Rechnungszins* floor a written interest guarantee, neither of
  which the deterministic path prices. A stochastic-on-deterministic run — this recursion, the
  crediting rule and the conversion rule re-evaluated per scenario — is what a
  time-value-of-options-and-guarantees calculation consumes.
- **IFRS 17 and professional standards.** A profit-participating deferred annuity would be measured
  under the variable fee approach [REG-R55], on this same fulfilment-cash-flow engine; actuarial work
  sits under the DAV *Fachgrundsätze* and the § 141 VAG *Verantwortlicher Aktuar*, distinct from the
  MaGo's *versicherungsmathematische Funktion* [REG-R56] [REG-R11] [REG-R21].

---

## Key sensitivities and model risks

In rough order of leverage on a German deferred-annuity block.

1. **The *Rentenfaktor*, and the fact that it is not calibrated to the shipped mortality table.**
   The annuity amount is `K / 10 000 × f`, so the whole payout phase scales linearly with `f`, and
   `f` is **[std]**. Market anchors now exist and the shipped values sit above them: 2025 averages of
   24,33–27,18 guaranteed and 27,27–30,40 current by deferment term [R24], and a current-factor
   average of 25,97 for 2022 [R19], against a shipped `base` current factor of 32,00 at age 67.
   **A user recalibrating to market would lower it**, and the payout phase scales linearly with the
   change. The reference library warns that a
   model publishing a [std] *Rentenfaktor* **and** a [std] annuity table must say whether the two are
   consistent and which is authoritative [REG-R49]. **They are not calibrated to each other, and the
   *Rentenfaktor* is authoritative**: it fixes the benefit amount, while the mortality proxy fixes
   only how long that amount is paid. The model publishes `annuity_due_factor()` — the annuity-due
   present value on the shipped proxy at the guarantee interest basis — purely as a diagnostic, so
   the gap is visible rather than hidden. Anyone substituting a real DAV 2004 R must re-strike the
   *Rentenfaktoren* with it or accept an inconsistency the model will not flag.
2. **The declared rate and the guarantee vintage together.** `bonus_rate = max(0, decl_rate −
   int_rate_guar)` is a difference of two numbers of similar size, so a 25 bp move in `decl_rate`
   moves the *Ansammlungsguthaben*'s accrual by about 16 % on the 1,00 % vintage and by **all of it**
   on the 2,75 % vintage, where the rate is already clipped at zero. The declared path is a level
   [std] scenario, not a forecast; the market's own 2026 averages disagree with each other by 33 bp
   [REG-R53], and one carrier's actual 2026 declaration is 3,00 % [S15] — 45 bp above the shipped
   path, which on the 1,00 % vintage is a 29 % change in `bonus_rate`.
3. **Mortality, in two dimensions.** For a deferred annuity the improvement trend matters more than
   the level, because the conversion happens decades out: on the anchor cell the annuitant reaches 67
   in 2043, 38 improvement years after the proxy's 2005 base. Both `q_base` and `improve` are [std],
   and the trend is the more dangerous of the two — the German construction uses a *Starttrend*
   converging to a weaker *Zieltrend* and the proxy uses a single age-graded rate, which is a
   documented simplification and not a replication [REG-R49].
4. **The surrender assumption, and the option it ignores.** Cumulative surrender over the anchor's
   seventeen accumulation years is material, and every surrendering policy forfeits a guaranteed
   *Rentenfaktor* struck on bases that will look generous by 2043. The model's lapse rates are
   unconditional; a policyholder who valued the forfeited option would surrender less. The
   direction of the error is therefore known and one-sided.
5. **The *Kapitalwahlrecht* take-up rate.** At 30 % it removes nearly a third of the annuity block at
   `t = 16` and replaces it with a single payment. It is a pure [std] with no evidence (gap 20), and
   it substitutes for a tax comparison the model does not perform [R6] [REG-R45].
6. **The charge set, and the § 169 Abs. 3 floor it collides with.** `alpha_rate` at the statutory
   ceiling makes the year-one *Sparbeitrag* small and the early *Deckungskapital* correspondingly
   thin, but the floor then reverses most of that for surrender purposes [REG-R16] [REG-R28], so the
   two parameters must be moved together.
7. **The annuity's timing, now that the grid can carry it.** The model pays the instalment
   **monthly in advance**, which is what the *Rentenfaktor* quotes and what the wordings describe
   — *"Wir zahlen die Rente monatlich, jeweils im Voraus"*. Neither the exact payment date within
   the month nor the in-advance/in-arrears basis was established [S13] [R24] (gap 19), so the
   in-advance reading is still **[std]**; what is no longer a modelling artefact is the *frequency*.
   The annual grid this model ran on compressed the twelve instalments into one start-of-year
   payment, which was generous to the payout phase by roughly half a year's interest on one year's
   annuity and by a full year of survivorship on instalments a decedent did not live to collect:
   on the anchor cell that compression was worth 369,14 €, 1,6 % of the payout phase, and the
   whole of it sat outside the *Rentengarantiezeit*, where the count is fixed and the two grids
   agree to the cent.
8. **Everything the model does not do.** No *Bonusrente*, no *Zuzahlung*, no survivor's annuity, no
   § 163 VVG adjustment, no *Zinszusatzreserve*, no MindZV allocation, no *Sicherungsbedarf* test, no
   tax. Each is named where it belongs above; together they are the reason this is a mechanics
   demonstration and not a valuation.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-klassische_rentenversicherung-r1
[R11]: #delib-klassische_rentenversicherung-r11
[R12]: #delib-klassische_rentenversicherung-r12
[R13]: #delib-klassische_rentenversicherung-r13
[R17]: #delib-klassische_rentenversicherung-r17
[R19]: #delib-klassische_rentenversicherung-r19
[R2]: #delib-klassische_rentenversicherung-r2
[R20]: #delib-klassische_rentenversicherung-r20
[R21]: #delib-klassische_rentenversicherung-r21
[R24]: #delib-klassische_rentenversicherung-r24
[R3]: #delib-klassische_rentenversicherung-r3
[R4]: #delib-klassische_rentenversicherung-r4
[R5]: #delib-klassische_rentenversicherung-r5
[R6]: #delib-klassische_rentenversicherung-r6
[R7]: #delib-klassische_rentenversicherung-r7
[REG-R10]: #delib-reg-r10
[REG-R11]: #delib-reg-r11
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R21]: #delib-reg-r21
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R30]: #delib-reg-r30
[REG-R34]: #delib-reg-r34
[REG-R38]: #delib-reg-r38
[REG-R4]: #delib-reg-r4
[REG-R41]: #delib-reg-r41
[REG-R45]: #delib-reg-r45
[REG-R47]: #delib-reg-r47
[REG-R48]: #delib-reg-r48
[REG-R49]: #delib-reg-r49
[REG-R52]: #delib-reg-r52
[REG-R53]: #delib-reg-r53
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
