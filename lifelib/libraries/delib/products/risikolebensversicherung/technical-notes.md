# Technical Notes

**Status:** Draft, 2026-08-29; citations re-verified against the primary documents 2026-08-30.

**Scope note.** These notes specify a reference liability cash-flow projection model — model name
**`RLV_DE_S`**, **monthly** grid — for the standardized composite German *Risikolebensversicherung*
defined in `product-spec.md` (same directory). This is not any single insurer's product. [S#]/[R#]
tags refer to the source list in `sources.md` (numbering carried from
`_research/risikolebensversicherung.md`; frozen); [REG-R#] tags refer to the cross-product reference
library `references/regulatory-and-actuarial-references.md` (its own R-numbering). **[std]** marks
standardizations introduced for the reference implementation; [unverified] marks claims no search
corroborated. Parameter values are identical to those in `product-spec.md`. Cells names,
model-point columns and CSV headers are English `lower_snake_case`; German terms of art keep their
German form in prose.

**Retrieval conditions.** These notes were **drafted** with direct HTTP egress from the build
environment blocked and the session's `WebSearch` budget already exhausted, so nothing cited in them
had been opened and the text rested on the authoring model's own knowledge of German insurance law
and practice, with **inherited corroboration** from sibling delib research files as its only
second-hand evidence. **The citations have since been re-verified against the primary documents
(2026-08-30): 22 of the 40 entries in `sources.md` now read `Retrieved: yes` and 18 still read
`no`** — the statutes as canonical XML carrying each law's `Stand`, three AVB and two premium
specimens as PDFs, against a carrier sweep and a secondary literature that stayed shut. Where an
entry says `no`, **a delib citation is still a pointer, not a certificate**; and **every price,
charge, margin and behavioural level below is still [std]**, one direct writer's published model
case [S2] being a check on them and not an input.

**One vocabulary decision, made once and used throughout.** Three unrelated things are called
"netto" in this product, and confusing them is the classic implementation error [mechanic 4]:

| Term as used | Means | Name used here |
|---|---|---|
| *Nettoprämie* / *Nettobeitrag* (**actuarial**) | The risk premium from the mortality and interest bases, **before** expense loadings | `prem_net_level_pp`, symbol `Gn` |
| *Nettobeitrag* / *Zahlbeitrag* (**consumer**) | The premium billed = *Bruttobeitrag* less the *Beitragsverrechnung*. **The market's dominant usage** | `prem_paid_pp`, symbol `P` |
| *Nettotarif* / *Honorartarif* (**distribution**) | A commission-free tariff sold through fee-based advice | not modelled |

**The bare word *Nettobeitrag* is never a parameter name in this library**, and `prem_net_pp` is on
the library's retired-names register.

---

## Model scope and conventions

- **Purpose.** Project **gross best-estimate liability cash flows, undiscounted** — the billed
  *Zahlbeitrag*, death claims, expenses and commission — for a single-policy model point on an
  expected (probability-weighted) basis. **Discounting, the *Deckungsrückstellung*, Solvency II
  technical provisions and the SCR are referenced, never specified** (see *Valuation and reserve
  pointers*). The one place a discount rate appears is inside the **pricing** equivalence that
  strikes the *Bruttobeitrag* and the *Beitragsverrechnungssatz*, and inside the first-order
  *Deckungskapital* published as a pricing diagnostic. **Neither discounts a published cash flow.**
- **Projection frequency.** **Monthly grid.** The *product* is annual — a level annual
  *Bruttobeitrag*, an annual *Überschussdeklaration*, an annual *Versicherungssumme* schedule
  [R5] [R6] — and every one of those stays on the anniversary; what the finer grid resolves is
  *timing*. It also removes the one approximation the annual grid had to declare: § 168 VVG makes
  the *Versicherungsperiode* follow the *Zahlweise*, so a monthly-paying contract is terminable
  monthly and its exits are **not** concentrated at anniversaries [R8] [REG-R28], and a fractionated
  *Zahlbeitrag* is collected in instalments rather than whole at the anniversary. Both are now
  expressed rather than booked at the anniversary and noted as a simplification.
- **The frame is 0-based, and `t` counts policy months from issue.** Month `t` runs from time `t` to
  time `t + 1`, and falls in the policy year at attained age `x(t) = issue_age + duration(t)`, where
  `duration_mth(t) = t` is the completed policy months and `duration(t) = t // 12` the completed
  policy years. **The first month is `t = 0`** and **the contractual policy year is
  `policy_year(t) = duration(t) + 1`** — the label the three schedule CSVs are keyed on, derived and
  never indexed by. A new-business model point opens at `t = 0`; **an in-force model point opens at
  `t = 12 · duration_y`**, `duration_y` being completed policy years and therefore already a 0-based
  elapsed count, so that everything keyed to duration — the § 161 three-year window, the lapse
  table, the *Zillmerung* run-off — reads off one clock and needs no second. That is why `duration_y`
  is a model-point column rather than a re-based issue age.
- **`proj_len()` is the number of projected policy months**, `12 · policy_term`, and it is the
  frame's **exclusive end**; `proj_len_y() = policy_term` is the *Versicherungsdauer* in whole years
  and is what every annual construction is written against. `result_cf()` is indexed by `t` from
  `12 · duration_y` to `proj_len() − 1` inclusive, contiguously, so the frame is
  `range(12·duration_y, proj_len())` and has `12·(policy_term − duration_y)` rows. This is lifelib's
  own convention, which delib adopts and asserts in `tests/test_model_conventions_de.py`.
  `result_cf_annual()` sums that frame into policy years and is the view the worked example below is
  stated on.
- **Two speeds, and which quantity runs at which.** `mort_rate(t)` and `lapse_rate(t)` are the
  **annual** rates of the policy year containing month `t` — the vectors this document tabulates —
  and `mort_rate_mth(t)` and `lapse_rate_mth(t)` are the monthly rates actually applied, each
  `1 − (1 − r)^(1/12)` **[std]**, so that twelve of them compound back to exactly the year's rate.
  That is what makes the in-force at every anniversary identical to the annual-step model's, and it
  is why the whole first-order equivalence — `G`, `Gn`, `v_d` and the *Deckungskapital* — is
  unchanged by the conversion.
- **Cover ends at attained age `issue_age + policy_term`**, and the last covered month is
  `t = proj_len() − 1`, the twelfth month of the policy year at attained age
  `issue_age + policy_term − 1`. `cover_end_age` is **derived**, not carried, so the two cannot
  disagree.
- **Timing conventions [std].** A *Zahlbeitrag* **instalment** on the *Zahlweise*'s own cycle at the
  **beginning** of month `t` — one month in twelve for a *jaehrlich* payer, every month for a
  *monatlich* one; acquisition cost and initial commission at issue, i.e. in month `t = 0` of a
  new-business point and **never** on an in-force point, where they are sunk; a twelfth of the
  sum-related admin charge, the collection cost on the instalment actually collected, and the
  renewal commission on it, at the beginning of the month on the opening in-force; **death claims
  and the claim expense at the end** of the month of claim; lapses at the end of the month,
  **after** the death decrement; expiry at the end of the last month `t = proj_len() − 1`.
- **Age basis.** *Alter am Jahrestag* — the attained age at the policy anniversary. The age steps at
  `t = 12, 24, …` and **not** monthly: the monthly grid does not make the age basis finer, and every
  rate read at that age is flat across the policy year's twelve months. Germany has no counterpart
  to the French *différence de millésime*, where the rating age steps on 1 January irrespective of
  birth month; on a real-date implementation the offset here is at most a few months **[std]**.
- **No cash value in the model — and, in the market, a cash value that is nil or nominal.** § 169
  Abs. 1 VVG confines the surrender-value **duty on *Kündigung*** to a policy insuring a risk "bei dem
  der Eintritt der Verpflichtung des Versicherers gewiss ist", which a term assurance's is not, and
  that wording is now read rather than inferred [R2] [REG-R28]. **But it does not follow that no
  wording pays one, and the retrieved wordings show that two of three do**: the GDV model conditions
  and the Hannoversche AVB convert the contract into a *beitragsfreie Versicherung* on *Kündigung*
  and pay a *Rückkaufswert* under § 169, less a *Stornoabzug*, where the paid-up sum fails a minimum
  [S1] § 13 Abs. 8, [S4] § 13; Cosmos pays nothing [S3] § 15 Abs. 10. What is uniform is the size:
  the *Kostenverrechnung* leaves "keine oder nur geringe Mittel" [S1] § 14 Abs. 4, [S3] § 16 Abs. 4.
  The model therefore has **no account value, no `av_pp_at`, no surrender cells and no paid-up
  state**, and `claims(t, "LAPSE")` and `claims(t, "MATURITY")` are **0.00 at every `t`** — asserted
  by a published `check_no_cash_value()` rather than left to prose. **Read that check as pinning a
  best-estimate approximation of a nil-or-nominal amount, not as a statement that German term
  assurance cannot carry a surrender value.** The cash flow is right either way: a *Beitragsfreistellung*
  pays nothing at the time in any wording — it converts.
- **What is deliberately not modelled**, each stated so a reader does not go looking for it: the
  *Kriegsklausel* and the ABC clause, which are catastrophe-scenario provisions rather than
  best-estimate ones; the § 162 VVG forfeitures; the mental-illness exception to § 161; selective
  lapse and premium-shock lapse, which ship as switchable modules that are **off** in the base run;
  the *Summenzuwachs*, *verzinsliche Ansammlung* and *Todesfallbonus* surplus forms; every rider
  (UZV, BUZ, *Beitragsbefreiung*, *vorgezogene Todesfallleistung*, *Verlängerungs-* and
  *Umtauschoption*, *vorläufiger Versicherungsschutz*); and all taxation, which is documented in
  `product-spec.md` and computed nowhere.
- **Currency, sign and rounding.** EUR throughout. `net_cf(t)` is **income-positive** (premiums +,
  claims and expenses −), with the outgo-positive orientation published as
  `liability_cf(t) = −net_cf(t)`. Intermediate values at full precision; displayed cash flows to
  euro cents and `pols_if` to six decimals **[std]**. Totals are summed **at full precision and then
  rounded**, never summed from rounded cells.

### External inputs

Inputs are **external CSVs in the model folder's parent** — the `annuallife/TradLife_A` layout, not
`basiclife/BasicTerm_S`'s embedded IOSpec — read by an unparameterized `Data` Space so each file is
read **once per model** rather than once per model point. **Every file but the model point table
carries a per-row `provenance` column**, which is delib's second ruling and is machine-checked.

| File | Index columns | Value columns | Provenance |
|---|---|---|---|
| `model_point_table.csv` | `point_id` | the 18 model-point attributes below | **exempt** — a model point is a configuration, not an assumption |
| `mort_table.csv` | `table_id`, `sex`, `smoker`, `age` | `mort_rate` (second-order annual death rate) | per row |
| `benefit_schedule.csv` | `schedule_id`, `policy_year` | `benefit_factor` | per row |
| `nvg_schedule.csv` | `nvg_id`, `policy_year` | `sum_uplift` (cumulative multiplier on the sum insured) | per row |
| `lapse_table.csv` | `policy_year` | `lapse_rate` | per row |
| `freq_loading_table.csv` | `prem_freq` | `instalments`, `prem_freq_load` | per row |

Six files, no orphans: the conventions suite asserts that every CSV beside the model backs a
filename Reference in `Data` and that the set read by a full sweep is exactly the set registered in
`tests/de_registry.py`. Scalar assumptions are **References on `Projection`**, not rows in a table,
following `TradLife_A`; their values and tags are the assumption tables below.

---

## Model point attributes

| Attribute | Type | Meaning | Exercised by |
|---|---|---|---|
| `point_id` | int | Row key; `Projection` is parameterized by it | all |
| `policy_id` | str | Human-readable policy reference | all |
| `issue_age` | int | *Eintrittsalter* of the first *versicherte Person* | all |
| `sex` | enum {M, F} | Sex of the first life. **Decrement only — must never enter pricing** [R13] [REG-R34] | 1 vs 2 |
| `smoker` | enum {N, R} | *Nichtraucher* / *Raucher* of the first life; the largest rating split after age | 1 vs 3 |
| `sum_assured` | float EUR | Initial *Versicherungssumme*, `S0` | all |
| `policy_term` | int | *Versicherungsdauer* in whole years; equals `proj_len_y()`, and `proj_len() = 12 × it` | all |
| `prem_term` | int | *Beitragszahlungsdauer* in whole years, `≤ policy_term` | 6 (12 < 20) |
| `premium_form` | enum {laufend, einmal} | Level *Bruttobeitrag* over `prem_term`, or a single *Einmalbeitrag* at issue | 7 |
| `prem_freq` | enum {jaehrlich, halbjaehrlich, vierteljaehrlich, monatlich} | *Zahlweise*; drives the *Ratenzahlungszuschlag* | 4, 5, 6, 10 |
| `benefit_schedule_id` | str | Key into `benefit_schedule.csv`: `konstant`, `linear_fallend`, `annuitaet_fallend_3pct` | 4, 5 |
| `nvg_schedule_id` | str | Key into `nvg_schedule.csv`: `keine`, `nvg_zwei_erhoehungen` | 9 |
| `surplus_form` | enum {beitragsverrechnung, keine} | Participating with *Beitragsverrechnung*, or the § 153-excluded non-participating tariff [R5] | 12 |
| `lives` | int {1, 2} | Single life, or *verbundene Leben* paying on the **first** death | 10 |
| `issue_age2` | int | *Eintrittsalter* of the second life; `0` where `lives = 1` | 10 |
| `smoker2` | enum {N, R, -} | Smoker status of the second life; `-` where `lives = 1` | 10 |
| `rating_factor` | float | *Risikozuschlag*: a multiplier on the **mortality basis**, both orders. 1.00 standard | 11 |
| `mort_table_id` | str | Key into `mort_table.csv`; one table shipped, `dav2008t_proxy` | all |
| `duration_y` | int | Completed policy years at the valuation date; `0` for new business | 8 |
| `issue_date` | date | Reporting only; the model runs on integer durations | none |

Three of these are worth a sentence each. **`sex` is carried and must not be priced on**: art. 5(2)
of the Gender Directive was struck down with effect from 21 December 2012 [R13] [REG-R34], while the
underlying DAV 2008 T tables remain sex-distinct [R12] [REG-R48]. The model resolves the tension the
only way § 138 VAG allows — **the tariff blends the two tables 50/50 and the projection uses the
policy's own sex** [R11] [REG-R8] — so the unisex cross-subsidy appears in the cash flows rather
than in the price. **`rating_factor` scales the mortality basis, not the price**: an impaired life
pays more *and* is expected to claim more, so the *Zahl/Brutto* ratio is nearly invariant to it; the
alternative reading, in which the loading is pure price and falls through to surplus, is pitfall 17.
**`duration_y` is the only thing that moves where the frame starts**, and it is what makes the § 161
window, the lapse table and the acquisition-cost switch all read off one clock.

### Model points shipped

Fourteen, covering both premium forms, all four payment frequencies, all three benefit schedules, an
in-force point, three options and three boundary cases. **Model point 1 is the worked example's
anchor cell.**

| # | Configuration | What it exercises |
|---|---|---|
| 1 | 35 M N, 300 000 € `konstant`, 25/25 y, `laufend`, `jaehrlich`, participating | **The anchor.** The representative composite |
| 2 | As 1 but `sex = F` | The unisex cross-subsidy: identical tariff, different projected claims |
| 3 | As 1 but `smoker = R` | The smoker split; the derived premium ratio against point 1 |
| 4 | 40 M N, 250 000 € `linear_fallend`, 20/20 y, `monatlich` | Falling sum; the 5 % *Ratenzahlungszuschlag* |
| 5 | 33 F N, 400 000 € `annuitaet_fallend_3pct`, 30/30 y, `vierteljaehrlich` | *Darlehensabsicherung* schedule; the 3 % loading |
| 6 | 45 M N, 200 000 € `konstant`, 20/**12** y, `halbjaehrlich` | *Abgekürzte Beitragszahlungsdauer*; the largest *Deckungskapital*; the 2 % loading |
| 7 | 50 M N, 100 000 € `konstant`, 10/**1** y, `einmal`, `jaehrlich` | The second premium form; the equivalence at its boundary |
| 8 | 30 F N, 150 000 € `konstant`, 30/30 y, `duration_y = 12` | **In force.** The frame opens at `t = 144`; past the § 161 window and the elevated lapse durations |
| 9 | 32 M N, 200 000 € `konstant`, 28/28 y, `nvg_zwei_erhoehungen` | *Nachversicherungsgarantie*; the § 161 clock restarting per increment |
| 10 | 38 M N + 36 F N, 300 000 € `konstant`, 22/22 y, `monatlich`, `lives = 2` | *Verbundene Leben*; the first-death rate |
| 11 | 42 M R, 250 000 € `konstant`, 18/18 y, `rating_factor = 1.75` | *Risikozuschlag* on an impaired smoker |
| 12 | 36 F N, 300 000 € `konstant`, 25/25 y, `surplus_form = keine` | The § 153-excluded tariff: `prem_rebate ≡ 0`, billed = guaranteed |
| 13 | 60 M N, 50 000 € `konstant`, 5/5 y | **Boundary.** Oldest entry, shortest term; the § 161 window covers three of five years |
| 14 | 18 M N, 100 000 € `konstant`, 40/40 y | **Boundary.** Youngest entry, longest term; cumulative lapse at its largest |

---

## State variables

| Variable | Description | Updated |
|---|---|---|
| `proj_len_y` | `policy_term`; the number of policy years, what every annual construction is written against | once per model point |
| `proj_len` | `12 × proj_len_y`; the number of projected months, the frame's exclusive end | once per model point |
| `duration_mth(t)`, `duration(t)`, `policy_year(t)` | completed months (`= t`), completed years (`= t // 12`), the contractual 1-based label | derived |
| `age(t)` | Attained age of the first life = `issue_age + duration(t)`; steps on the **anniversary** | anniversary |
| `age2(t)` | Attained age of the second life = `issue_age2 + duration(t)`; unused where `lives = 1` | anniversary |
| `pols_if(t)` | In-force count at the **start** of month `t`; `pols_if(12·duration_y) = pols_if_init() = 1` | monthly recursion |
| `benefit_pp(t)` | *Versicherungssumme* in force = `sum_assured × benefit_factor(t) × sum_uplift(t)`; flat across a policy year | schedule lookup |
| `benefit_paid_pp(t)` | The benefit actually payable on a death in month `t`, after the § 161 switch | anniversary |
| `mort_rate(t)` | **Second-order annual** death rate of the policy year: own sex, smoker, rated, first-death where `lives = 2` | lookup |
| `mort_rate_mth(t)` | The monthly rate applied, `1 − (1 − mort_rate(t))^(1/12)` **[std]** | monthly |
| `mort_rate_tar(t)` | **First-order annual** tariff rate: unisex 50/50 blend, `× (1 + m) × rating_factor` | lookup |
| `lapse_rate(t)` | **Annual** lapse rate of the policy year; **0** through the whole final policy year | lookup |
| `lapse_rate_mth(t)` | The monthly rate applied after the death decrement, `1 − (1 − lapse_rate(t))^(1/12)` **[std]** | monthly |
| `suicide_factor(t)` | § 161 benefit switch, `< 1` inside three years of issue and of each increment | anniversary |
| `prem_gross_pp(t)` | **Annual** *Bruttobeitrag* per in-force policy, loaded for frequency; **0** for `duration(t) ≥ prem_term` | anniversary |
| `prem_rebate_pp(t)` | **Annual** *Beitragsverrechnung* per in-force policy | anniversary |
| `prem_paid_pp(t)` | **Annual** *Zahlbeitrag* per in-force policy = `prem_gross_pp − prem_rebate_pp` | anniversary |
| `instalments()`, `prem_cycle()`, `prem_due(t)` | Instalments a year (1/2/4/12), months between them, whether one falls due this month | *Zahlweise* |
| `prem_gross_inst_pp(t)`, `prem_rebate_inst_pp(t)`, `prem_inst_pp(t)` | The three annual amounts divided into instalments, zero in a month none is due | monthly |
| `res_pp_at(y, timing)` | First-order **net** *Deckungskapital* per policy at **policy year** `y` — a **pricing diagnostic**, not a balance-sheet provision | prospective, annual |
| `res_zill_pp_at(y, timing)` | The same reserve less the unamortised Zillmer balance; **negative for much of the term** | prospective, annual |
| `pols_death(t)` | Expected deaths in month `t` = `pols_if(t) × mort_rate_mth(t)` | monthly |
| `pols_lapse(t)` | Expected lapses in month `t`, on survivors of the death decrement | monthly |
| `pols_maturity(t)` | Expiring survivors; **0** except at `t = proj_len() − 1` | monthly |
| `premiums(t)` | `prem_inst_pp(t) × pols_if(t)` — the billed stream, the one inside `net_cf` | monthly |
| `prem_gross(t)` | `prem_gross_inst_pp(t) × pols_if(t)` — the **guaranteed** stream, published beside it | monthly |
| `claims(t, kind)` | `kind ∈ {DEATH, LAPSE, MATURITY}`; the last two are structurally zero | monthly |
| `expenses(t)` | Acquisition + maintenance + collection + claim expense | monthly |
| `commissions(t)` | Initial *Abschlussprovision* + *Bestandspflegeprovision* | monthly |
| `net_cf(t)` | Net liability cash flow, income-positive | monthly |

There is **no** account-value state variable, **no** surrender-value state variable and **no**
paid-up state. That is a statutory fact about the product, not a modelling simplification
[R2] [R3] [R8] [REG-R28].

---

## Assumption inputs

### (a) Contractual / guaranteed elements (cited)

| Input | Value | Basis |
|---|---|---|
| Death benefit | `benefit_pp(t)`, from any cause, subject only to the § 161 window | [R1] [R2] [S5] [S15] |
| Survival benefit | **None.** Nothing is paid at expiry | [R1] [R2] [S5] [S15] |
| Surrender / paid-up value | **Nil or nominal, and modelled as nil.** No § 169 Abs. 1 duty attaches on *Kündigung* (the *gewiss* test, now read verbatim); § 165 carries no such limitation and its paid-up right is live on a constant sum insured — [S3] ends the contract only below a 300 € paid-up sum, [S4] below 2 500 €, and on a falling sum insured no *Deckungskapital* is built at all. Where a wording pays, it pays the *Deckungskapital* less a *Stornoabzug* — 60 % at [S4] | [R2] [R3] [R8] [S1] [S3] [S4] [REG-R28] |
| Premium form | A **level *Bruttobeitrag*** over the *Beitragszahlungsdauer*, guaranteed for the term as the maximum the policyholder can ever be required to pay | [R6] [R10] [REG-R27] |
| What is billed | The *Zahlbeitrag* = *Bruttobeitrag* less the declared *Beitragsverrechnung*. **Not guaranteed**; § 153 confers an entitlement to participate, not to a level | [R5] [R6] [R9] [S5] [REG-R24] |
| Minimum surplus allocation | **90 % of the *Risikoergebnis***, **MindZV § 7** — the section number the file previously refused to guess, now read (gap 4 closed). § 8 gives 50 % of the *übriges Ergebnis* and § 6 Abs. 1 gives 90 % of the *anzurechnende Kapitalerträge* "abzüglich der rechnungsmäßigen Zinsen"; each is floored at zero. Both carrier wordings state the same three [S3] § 3 Abs. 1 a, [S4] § 20 | [R9] [REG-R18] [S3] [S4] |
| Equal treatment | VAG § 138 Abs. 2, verbatim: "Bei gleichen Voraussetzungen dürfen Prämien und Leistungen nur nach gleichen Grundsätzen bemessen werden." The unit of "gleiche Voraussetzungen" is the ***Bestandsgruppe*** and, inside it, the ***Gewinnverband*** — [S1] § 2 Abs. 2–3, with [S3] naming *Bestandsgruppe 112* for its term book. One declared rate per *Gewinnverband*, and [S2] shows it holding across two product variants to three decimal places | [R11] [REG-R8] [S1] [S2] [S3] |
| *Selbsttötung* | Insurer *leistungsfrei* where the *versicherte Person* intentionally takes her own life "vor Ablauf von drei Jahren nach Abschluss des Versicherungsvertrags", unless in a state excluding free determination of the will; extendable by *Einzelvereinbarung* (Abs. 2); the substitute payment is the *Rückkaufswert* nach § 169 (Abs. 3), which here is nil or nominal. **The clock restarts for an increased or reinstated part** — not from § 161, which is silent, but from all three retrieved wordings | [R1] [REG-R26] [S1] [S3] [S4] |
| Premium cessation | On death, and at the end of the *Beitragszahlungsdauer* | mechanics 4, 17 |
| *Rechnungszins* | **1,00 %** — but that is the DeckRV ***Höchstzinssatz***, the ceiling, read at the amending regulation itself (Art. 1 V v. 19.7.2024). **A carrier need not price at it and one does not**: [S3]'s AVB states its *Rechnungsgrundlagen* as "einem Rechnungszins in Höhe von **0,25 Prozent**". The model uses the ceiling; see the pitfalls | [R10] [REG-R14] [REG-R15] [S3] |
| *Höchstzillmersatz* | **25 ‰**, DeckRV § 4 Abs. 1: "Der Zillmersatz darf 25 Promille der Summe aller Prämien nicht überschreiten"; cut from 40 ‰ with effect from 1 January 2015, and the rate at conclusion applies for the whole term (Abs. 4). **It caps the *zillmerbare* part only** — both wordings spread the remaining acquisition cost over the premium-paying period [S1] § 14 Abs. 3, [S3] § 16 Abs. 3 — and the GDV model carries the clause only "bei der Verwendung des Zillmerverfahrens", so it is optional on this line | [R10] [REG-R16] [REG-R20] [S1] [S3] |
| Unisex | Sex may not enter the premium for contracts concluded from 21 December 2012 | [R13] [REG-R34] |
| Mortality table family | DAV 2008 T, with *R* and *NR* variants, **suitable for premium calculation** but not without a *Gesundheitsprüfung*; **values proprietary, not redistributed** | [R12] [REG-R48]; inherited corroboration |
| Premium tax | **None** — VersStG 2021 § 4 Abs. 1 Nr. 5 Buchst. a exempts a contract creating claims "im Fall des Todes", so there is no premium-tax line | [R16] |

### (b) Insurer-discretionary current elements

Thin, but decisive — on this product the discretion **is** the customer's bill.

| Input | Snapshot value | Basis |
|---|---|---|
| Declaration scaling `decl_scale` | **1.00**, i.e. the insurer declares exactly the MindZV minimum | **[std]** (1) |
| Surplus share `surplus_share` | **0.90** of the tariff mortality margin | [R9] [REG-R18]; choice of the minimum **[std]** (1) |
| Resulting `v_decl` (*Beitragsverrechnungssatz*) | **Derived, not assumed** — see the recursion section. Lands at about 0.43 on the anchor, so `Zahl / Brutto ≈ 0.57` | derived; inputs **[std]** |
| Cap on the declared rate `v_max` | **0.95** — a rebate may not exceed the premium | **[std]** (2) |
| *Kostenüberschuss* | **Not returned.** The tariff's β is 5,0 % and the modelled collection cost 3,0 %, so a cost result emerges in `net_cf` and stays there | **[std]** (3) |
| *Summenzuwachs*, *verzinsliche Ansammlung*, *Todesfallbonus* | **Off.** Only *Beitragsverrechnung* is implemented | mechanic 6; **[std]** |
| § 163 premium adjustment | **Off.** The *Bruttobeitrag* is fixed for the term — [S3]: "bleibt Ihre Absicherung sowie der vereinbarte Bruttobeitrag über die gesamte Versicherungsdauer unverändert" | [R6] [REG-R27] [S3]; non-use in practice still [unverified] |

1. **Modelling the statutory minimum is the conservative choice for the *Zahlbeitrag***, and it is
   the only level any instrument fixes: no German carrier publishes a declaration for this product,
   and none was located (research gap 1). `decl_scale` is the stress lever — setting it to **0**
   raises the billed premium to the guaranteed one with no change to any claim, which is precisely
   the move § 163 does not govern [R6], and it is the model's representation of the product's single
   largest policyholder risk.
2. `v_max` binds nowhere in the shipped model points; it exists so that an extreme `m` cannot drive
   the billed premium negative, and so that `check_prem_split()` has a stated domain.
3. **The tariff loading and the modelled cost are deliberately different numbers, and the gap is the
   *Kostenüberschuss*.** Returning it would require splitting the *übriges Ergebnis* limb of the
   MindZV, whose minimum share is different and for which the research file gives no basis [R9]
   [REG-R18]. Not returning it is a **stated simplification** and pitfall 15, not an oversight.

### (c) Behavioural / experience assumptions (the modeller's view)

**Every input in this class is [std].** No German insurer publishes a mortality table, a
*Sicherheitszuschlag*, a best-estimate factor, a commission scale or a lapse rate for this product,
and none was retrieved [S3]–[S13] [R12]. Expense loadings are the one exception, and only per
contract: § 2 VVG-InfoV makes the insurer give the applicant its acquisition and administration
costs in euro [R17], and one carrier's published specimen prints them [S2] — a model case, not a
rate card, and not adopted here.

**Mortality.** The regulatory basis is **DAV 2008 T** with its *R* and *NR* variants [R12]
[REG-R48], which is **cited by name and never shipped** — the tables are the property of the
Deutsche Aktuarvereinigung, are not public, and are not redistributed here. `mort_table.csv` is a
**[std] Gompertz-form proxy** for a medically selected insured-lives population:

    mort_rate(sex, smoker, x) = base(sex) × smoker_mult(smoker) × 1.095^(x − 30),   ages 18–80

    base(M) = 0.00040      base(F) = 0.00020
    smoker_mult(N) = 1.00  smoker_mult(R) = 2.20

Three anchors a replacement table must preserve, so that the worked example still closes. **The
50/50 unisex non-smoker blend is `0.00030 × 1.095^(x − 30)`**, which is the [std] best-estimate
scale the research file constructed and froze; **the female-to-male ratio is 0.50** at every age,
the order of magnitude reported for insured lives at the ages this product is sold [unverified]; and
**the smoker multiplier is 2.20**, the mid-point of the two-to-three range reported for insured-lives
smoker mortality at working ages [unverified], which reproduces a *premium* ratio near 2 once
sum-related and per-policy expenses are added back — **2.007** between model points 3 and 1 on the
built model, against the research file's zero-interest construction of 2.04. The 9,5 % per year of age is the slope of the
research's construction; it is a fitted-in-spirit gradient with **no German source**, and on a
40-year run (model point 14) it is the single most exposed number in the file. **Population tables
are the wrong starting point for a replacement**: an RLV model built on a Destatis table without a
selection adjustment overstates claims by a wide margin at issue ages 25–45 [REG-R48] [REG-R52].

**The two-order split.** The first-order (tariff) rate is

    mort_rate_tar(t) = (1 + m) × [ ω·q_tab(M, smoker, x(t)) + (1 − ω)·q_tab(F, smoker, x(t)) ]
                       × rating_factor

with the *Sicherheitszuschlag* `m = 1.25` **[std]** and the unisex mix `ω = sex_mix_male = 0.50`
**[std]**. So `q1 = 2.25 × q2` **for the tariff's own unisex life**, and for a real policy the ratio
is `2.25 × (unisex blend / own-sex rate)`. On the shipped proxy the blend is `0.75 × q̃(M)`, so the
ratio is **1.6875 for a male and 3.375 for a female**. That asymmetry is the unisex cross-subsidy, and it is a product fact, not a modelling
artefact. `m` is the single parameter that sets the *Brutto*/*Zahlbeitrag* spread; **its level is not
public** — the DAV *Richtlinie* regulates the **procedure** for setting the *Sicherheitszuschläge*,
not the level [R12] — and the argued range is **1.0 to 1.5** (research gap 6).

**Lapse.** No *Risikoversicherung*-specific rate exists anywhere in the research file (gap 13). The
inherited whole-market *Stornoquote* — 2,72 % (2024) and 2,56 % (2023) on the main GDV measure, with
a second irreconcilable measure at 1,2 % (2024) [R18] — is a book average dominated by long-dated
savings contracts and is **deliberately not used**. The shipped table is argued from three structural
features instead: **there is nothing to lose by lapsing**, no surrender value and no accumulated
bonus, so the financial friction that suppresses savings-contract lapse is absent; **the contract is
terminable at the end of each *Versicherungsperiode***, monthly for a monthly payer [R8], so exit is
frictionless in time as well as in money; and **the need that motivated the purchase amortises**.

| Policy year (`t + 1`) | 1 | 2–3 | 4+ | `n` |
|---|---|---|---|---|
| `t` | 0 | 1–2 | 3+ | `n − 1` |
| `lapse_rate(t)` **[std]** | 6 % | 4 % | 3 % | **0** |

**In the final period the lapse rate is zero.** Lapses fall at the end of the period, and
the end of period `t = n − 1` is the moment cover expires — a lapse and an expiry are then the same
event paying the same nothing, so the whole surviving cohort is booked as `pols_maturity(n − 1)`.
**No cash flow moves either way**, but the convention decides the split between `Σ pols_lapse` and
`pols_maturity(n − 1)` and is load-bearing for the closure identity. The argued plausible range in the
early durations is **2 % to 8 %**, and **no German figure supports any of it**. Note the shape
argument the shipped table does *not* follow: because the need amortises, term-life lapse arguably
should **rise** in later durations rather than flatten, the opposite of a savings product's shape.
The research file ships the flat 3 % tail; that tension is recorded here and is a listed sensitivity
rather than a silent choice.

**Suicide share.** § 161 makes the insurer *leistungsfrei* for an intentional self-inflicted death
inside three years, substituting a *Rückkaufswert* that is nil here [R1] [R2]. The model applies

    suicide_factor(t) = 1 − suicide_share   for the first three periods of a cover tranche
                      = 1                   thereafter,           suicide_share = 0.03  **[std]**

to **death claims only**. No German cause-of-death share was retrieved, and none is asserted; 0,03
stands for "about three per cent of deaths at these ages are suicides", with an argued range of
**0,01 to 0,05** [unverified]. It carries **three times the weight of the French one-year factor**
[`frlib` R1] simply because the window is three times as long, which is why the parameter is stated
rather than buried.

**Expenses and commission (all levels [std]; the structures are cited where they exist).**

| Input | Value | Basis |
|---|---|---|
| Acquisition cost, total | `zillmer_rate × prem_term × G` = **25 ‰ of the *Beitragssumme***, at issue | ceiling [R10] [REG-R16]; level **[std]** (4) |
| — of which initial commission `comm_rate_init` | **20 ‰ of the *Beitragssumme*** | **[std]** (4) |
| — of which other acquisition cost | **5 ‰ of the *Beitragssumme*** | **[std]** (4) |
| Tariff premium loading `beta_tariff` | **5,0 %** of each *Bruttobeitrag*, inside the equivalence | **[std]** (4) |
| Modelled collection cost `maint_prem_pct` | **3,0 %** of each *Zahlbeitrag* | **[std]** (4) |
| Renewal commission `comm_rate_renew` | **1,0 %** of each *Zahlbeitrag* from policy year 2 | **[std]** (4) |
| Sum-related admin `gamma_rate` | **0,30 ‰** of `benefit_pp(t)` a year | **[std]** (4) |
| Expense inflation `expense_infl` | **2,0 %** a year, on the sum-related admin only; the tariff's γ is level | **[std]** (5) |
| Claim expense `claim_expense` | **250 €** per death claim | **[std]** (4) |
| Best-estimate mortality factor `mort_be_factor` | **1.00** | **[std]** (6) |
| *Ratenzahlungszuschlag* `prem_freq_load` | 1.000 annual · **1.02** half-yearly · **1.03** quarterly · **1.05** monthly | convention **[std]** (7) |

4. **German term-life charge levels are not published as a rate card — but they are disclosed**
   (research gap 8, corrected). There is no *Effektivkostenquote*, and § 2 Abs. 1 Nr. 9 VVG-InfoV
   gives the reason in terms, confining the duty to a contract "bei dem der Eintritt der Verpflichtung
   des Versicherers gewiss ist"; and no *Basisinformationsblatt*, the product not being a PRIIP [R17].
   **But § 2 Abs. 1 Nr. 1 with Abs. 2, and § 4 Abs. 2, require the acquisition and administration
   costs to be given to the applicant in euro**, and both retrieved wordings point him there [S1]
   § 14 Abs. 1, [S3] § 16 Abs. 1. One carrier's published specimen shows **α = 2,41 % of the
   *Tarifbeitragssumme***, other annual costs of 48,52 € of which 35,20 € administration [S2] — so the
   composite's assumption that a term tariff runs at the 25 ‰ ceiling is **close to right for that
   carrier**, though the ceiling is mis-typed: DeckRV § 4 caps only the *zillmerbare* part, the rest
   being spread over the premium term [S1] § 14 Abs. 3, [S3] § 16 Abs. 3. **The parameters are
   unchanged** — one model case is not a market [S3] [S12].
   This is the single [std] charge most likely to be overstated, and the notes say so rather than
   letting a reader discover it from a sensitivity.
5. Inflating the modelled γ while the tariff's γ is level means the cost result narrows over a long
   term and eventually reverses — a real feature of a 25-year contract, and the reason model point 14
   (40 years) is worth its place.
6. Set to 1.00 so that the shipped proxy *is* the best estimate and there is exactly one unsourced
   mortality level rather than two stacked on each other. A user with experience data should move
   this rather than editing the table.
7. **2 % / 3 % / 5 % is a market convention with no carrier attribution**, inherited from the sibling
   delib research (gap 21). Whether German carriers strike it on the *Bruttobeitrag* or the
   *Zahlbeitrag* was not established; the model loads the **billed** amount, so the split identity
   holds at every frequency (pitfall 10).

---

## Cash flow components and recursions

### Notation (defined once, used throughout)

| Symbol | Meaning |
|---|---|
| `t` | **month** index, **0-based**: `t = t0 … 12n − 1`, with `t0 = 12·duration_y` and `n = proj_len_y() = policy_term`, `proj_len() = 12n` |
| `y` | **policy year** index, 0-based: `y = duration(t) = t // 12`. The contractual policy year is `y + 1` |
| `x(t)`, `x₂(t)` | attained ages, `issue_age + duration(t)` and `issue_age2 + duration(t)`; both step on the anniversary |
| `k` | `prem_term`, the *Beitragszahlungsdauer* in years |
| `S0` | `sum_assured` |
| `f(t)` | `benefit_factor(t)` from `benefit_schedule.csv`, read at `policy_year(t)` |
| `u(y)` | `sum_uplift_y(y)` from `nvg_schedule.csv`, read at `policy_year = y + 1`; `u ≡ 1` for `nvg_schedule_id = keine`; defined on `y ≥ 0` only. `sum_uplift(t) = u(duration(t))` |
| `B(t)` | `benefit_pp(t) = S0 · f(t) · u(t)` |
| `q̃(x)` | `mort_rate_at_age(table_id, sex, smoker, x)`, the shipped second-order table rate |
| `ω` | `sex_mix_male` = 0.50, the tariff's unisex mix **[std]** |
| `m` | `sicherheitszuschlag_m` = 1.25 **[std]** |
| `rf` | `rating_factor` |
| `q₂(t)` | `mort_rate(t)`, the projected second-order **annual** rate of month `t`'s policy year |
| `q₂ᵐ(t)` | `mort_rate_mth(t) = 1 − (1 − q₂(t))^(1/12)` **[std]**, the rate actually applied |
| `q₁(t)` | `mort_rate_tar(t)`, the first-order **annual** tariff rate |
| `w(t)` | `lapse_rate(t)`, read at `policy_year(t)`; `w ≡ 0` through the whole final policy year **[std]** |
| `wᵐ(t)` | `lapse_rate_mth(t) = 1 − (1 − w(t))^(1/12)` **[std]**, the rate actually applied |
| `σ(t)` | `suicide_factor(t)`, the § 161 benefit switch |
| `l(t)` | `pols_if(t)`, in force at the **start** of month `t`; `l(t0) = pols_if_init() = 1` |
| `p₁(y)` | tariff survivorship over **policy years**, mortality only: `p₁(0) = 1`, `p₁(y+1) = p₁(y)·(1 − q₁(12y))` |
| `i`, `v` | `rechnungszins` = 1,00 %; `v = 1/(1 + i)` |
| `G`, `Gn` | `prem_gross_pp` before frequency loading; `prem_net_level_pp`, the actuarial *Nettoprämie* |
| `φ` | `prem_freq_load`, the *Ratenzahlungszuschlag* multiplier |
| `v_d` | `beitragsverrechnung_rate()`, the declared *Beitragsverrechnungssatz*, struck once at issue |
| `z`, `β`, `γ` | `zillmer_rate` = 0.025; `beta_tariff` = 0.05; `gamma_rate` = 0.00030 |
| `c₀`, `c_r` | `comm_rate_init` = 0.020 of the *Beitragssumme*; `comm_rate_renew` = 0.010 of the *Zahlbeitrag* |
| `a`, `π`, `ec` | `maint_prem_pct` = 0.03; `expense_infl` = 0.02; `claim_expense` = 250 |
| `r` | `instalments()` ∈ {1, 2, 4, 12}, the number of premium instalments a policy year |
| `P_inst(t)` | `prem_inst_pp(t)`, the *Zahlbeitrag* instalment collected in month `t`, or zero |

`q₁`, `q₂` and `w` are dimensionless **annual** probabilities and `q₂ᵐ`, `wᵐ` the monthly ones
derived from them; `S0`, `B`, `G`, `P` and every cash-flow component are EUR. `G`, `Gn` and `P` are
**annual** amounts; what is collected in a month is `P_inst`.

### The two mortality bases

    q₂(t) = mort_be_factor · rf · Q̃(t),        Q̃(t) = q̃(sex, smoker, x(t))                 lives = 1
    q₁(t) = (1 + m) · rf · [ ω·q̃(M, smoker, x(t)) + (1 − ω)·q̃(F, smoker, x(t)) ]

Both are **annual** rates, read at an attained age that steps on the anniversary, and both are
therefore flat across a policy year's twelve months. Only `q₂` is converted to the month, at
`q₂ᵐ(t) = 1 − (1 − q₂(t))^(1/12)` **[std]**; `q₁` is a pricing rate and the equivalence it enters is
annual, so it is never converted.

For `lives = 2` the two lives are combined **at table level, before any loading**, on an
independence assumption **[std]**:

    Q̃(t) = q̃_A(t) + q̃_B(t) − q̃_A(t)·q̃_B(t)

and the same combination is applied to the two unisex blends before `(1 + m)·rf`. Combining after
loading instead inflates the cross term and is pitfall 14. The independence assumption **understates**
the true first-death rate for a couple sharing a household, a vehicle and a lifestyle, and no German
figure bounds the understatement (research gap 15).

### The *Bruttobeitrag*, by first-order equivalence

Struck once, at issue, on first-order bases and tariff survivorship — never on the projection's own
lapse or best-estimate mortality, and therefore acyclic with respect to everything behavioural.
Write

    A  = Σ_{y=0..n−1} v^(y+1) · p₁(y) · q₁(12y) · B(12y)   APV of death benefits, paid at year end
    ä  = Σ_{y=0..k−1} v^y · p₁(y)                          premium annuity-due over the paying term
    Γ  = Σ_{y=0..n−1} v^y · p₁(y) · B(12y)                 sum-exposure annuity, for the γ loading

**Every sum here runs over policy years, not months, and that is a decision rather than an
inheritance.** A first-order equivalence is an annual construction: the *Höchstrechnungszins* is an
annual rate, the *Bruttobeitrag* it strikes is the annual amount the *Versicherungsschein* states,
and the end-of-year benefit timing inside `A` is the **tariff's** prudent convention and not the
projection's, which pays a death claim at the end of the month of death. Re-striking the equivalence
month by month would move `G`, `Gn`, `v_d` and every figure below while changing nothing about the
contract. On the monthly grid all four are **bit-identical** to the annual-step model's.

The equivalence, with the α loading a per-mille of the *Beitragssumme* `k·G` incurred at issue,

    G·ä  =  A  +  z·k·G  +  β·G·ä  +  γ·Γ

is linear in `G` and solves in closed form:

    G = ( A + γ·Γ ) / ( (1 − β)·ä − z·k )

For `premium_form = einmal`, `k = 1` and `ä = 1`, so the same expression returns the
*Einmalbeitrag* — the second premium form is the same engine at a boundary, not a second engine. The
actuarial *Nettoprämie* is `Gn = A / ä`, and it is what the reserve recursion below uses; it is
**not** a cash flow and never appears in `result_cf()`.

### The *Zahlbeitrag*, by the MindZV allocation

The tariff's own mortality margin in period `t`, per in-force policy, is the difference between
the first-order rate and the tariff's best estimate:

    margin_pp(t) = ( q₁(t) − q₁(t)/(1 + m) ) · B(t) = (m/(1+m)) · q₁(t) · B(t)

so its actuarial value at issue is exactly `(m/(1+m))·A`. The declared *Beitragsverrechnungssatz* is
struck once, at issue, to return `surplus_share` of it over the premium-paying term:

    v_d = min( v_max,  decl_scale · surplus_share · (m/(1+m)) · A / (G · ä) )

and is **0** where `surplus_form = keine`. Then, at every `t < k`,

    prem_gross_pp(t)  = G · φ
    prem_rebate_pp(t) = v_d · G · φ
    prem_paid_pp(t)   = (1 − v_d) · G · φ

and all three are **0** for `t ≥ k`. Substituting the equivalence into `v_d` gives the identity that
explains the whole German term-life spread in one line:

    v_d = decl_scale · surplus_share · (m/(1+m)) · [ 1 − β − ( γ·Γ + z·k·G ) / ( G·ä ) ]

— **the surplus share, times the margin fraction of the risk element, times the risk share of the
gross premium.** On the anchor's calibration the bracket is about 0.85, so
`v_d ≈ 1 × 0.90 × 0.5556 × 0.85 ≈ 0.43` and `Zahl / Brutto ≈ 0.57`, reproducing the research file's
frozen [std] ratio from the mechanic rather than assuming it. **Raising `m` raises `G` and `v_d`
together, which is why the *Bruttobeitrag* moves far more than the *Zahlbeitrag*** (product spec,
contractual mechanics).

### The § 161 benefit switch, and increments

The base cover's three-year window runs from issue, so it bites at `duration(t) < 3` — months 0 to
35, policy years 1 to 3. A *Nachversicherungsgarantie* increment granted at the anniversary opening
policy year `y_j` carries **its own** three-year window, `y_j ≤ duration(t) < y_j + 3` [R1] [S1] [S3] [S4] — **market practice, not a modelling choice** (research gap 9, closed): "Wenn unsere Leistungspflicht durch eine Änderung des Vertrages erweitert wird ..., beginnt die Dreijahresfrist bezüglich des geänderten ... Teils neu". With
`Δu(t) = u(t) − u(t − 1)` for `t > 0` and `Δu(0) = u(0)`, the effective benefit is

    benefit_paid_pp(t) = S0 · f(t) · Σ_{j : y_j ≤ duration(t)} Δu(y_j) · σ_j(t)
    σ_j(t) = 1 − suicide_share   if  duration(t) < y_j + 3,  else 1   (the base tranche has y_j = 0)

so `suicide_factor(t) = benefit_paid_pp(t) / benefit_pp(t)` is a **weighted average** across
tranches, strictly between `1 − suicide_share` and `1` in a policy year when one tranche is inside
its window and another is not. On an in-force model point with `duration_y ≥ 3` and no increments,
`σ ≡ 1` at every projected `t`. The switch **never** touches lapses or the expiry, both of which pay
nothing in any event.

Both clocks are annual and every boundary therefore falls on an anniversary, which is why the
monthly grid resolves the switch **exactly** rather than approximately: § 161's three years from
conclusion are months 0 to 35, and `duration(t) < 3` is the same statement as `t < 36`. The
comparison is written in years because that is the unit the statute and the *Bedingungen* use.

### Decrements and the in-force recursion

Two decrements, applied in the stated order at the end of the **month**, on the monthly rates:

    pols_death(t)    = l(t) · q₂ᵐ(t)
    pols_lapse(t)    = l(t) · (1 − q₂ᵐ(t)) · wᵐ(t)        with w ≡ 0 in the final policy year
    pols_maturity(t) = 0 for t < 12n−1;  l(12n−1)·(1 − q₂ᵐ(12n−1))  at t = 12n−1
    l(t+1)           = l(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t),    l(t0) = 1

so `l(12n) = 0` exactly: **every exit lands inside the frame**, which is what lets `result_cf()` end
at `proj_len() − 1` with nothing left over. **Closure identity**, which a test asserts:

    Σ_{t=t0..12n−1} [ pols_death(t) + pols_lapse(t) + pols_maturity(t) ] = pols_if_init() = 1

**This recursion collapses to the annual one at every anniversary.** Because `q₂ᵐ` and `wᵐ` each
compound back to their policy year's annual rate, twelve months of it give
`l(t+12) = l(t)·(1 − q₂(t))·(1 − w(t))` — the annual-step recursion, term for term — so the in-force
at every policy anniversary is the annual-step model's own figure. What the finer grid adds is the
eleven months between them, and one genuine change: deaths and lapses now **interleave**, each
eroding the exposure the other works on, so the *split* of the closure identity moves even though
its total does not.

### Benefits, expenses and net cash flow

    claims(t, "DEATH")    = benefit_paid_pp(t) · pols_death(t)
    claims(t, "LAPSE")    = 0                                        [R2] [R3] [R8]
    claims(t, "MATURITY") = 0                                        a term contract pays nothing at expiry
    claims(t)             = Σ_kind claims(t, kind)

    acq_pp   = z·k·G                                                  incurred once, at issue
    comm_pp  = c₀·k·G                                                 of which commission
    maint(t) = γ · B(t) · (1 + π)^duration(t) / 12  +  a · P_inst(t)

    expenses(t)    = (acq_pp − comm_pp)·1{t = 0 and duration_y = 0}
                     + maint(t)·l(t) + ec·pols_death(t)
    commissions(t) = comm_pp·1{t = 0 and duration_y = 0}
                     + c_r·P_inst(t)·l(t)·1{duration(t) ≥ 1}

    prem_due(t)            = 1{ duration_mth(t) mod (12/r) = 0 }
    prem_gross_inst_pp(t)  = prem_gross_pp(t)/r · prem_due(t)
    prem_rebate_inst_pp(t) = prem_rebate_pp(t)/r · prem_due(t)
    P_inst(t)              = prem_gross_inst_pp(t) − prem_rebate_inst_pp(t)

    premiums(t)    = P_inst(t)·l(t)
    prem_gross(t)  = prem_gross_inst_pp(t)·l(t)
    prem_rebate(t) = prem_rebate_inst_pp(t)·l(t)

    net_cf(t)      = premiums(t) − claims(t) − expenses(t) − commissions(t)
    liability_cf(t) = −net_cf(t)

**Acquisition cost is a month-0 outgo, not an annualised loading and not a twelfth of one.** The
tariff amortises it through the equivalence; the cash flow incurs it at issue, which is the economic
reason an early lapse hurts on a product with no surrender value to forfeit (mechanic 10). On an
**in-force** model point it is sunk and is not incurred at all — which is why the switch tests
`duration_y = 0` and not merely `t = 0`.

**The two halves of `maint` move differently on the monthly grid, and both moves are the point.**
The sum-related administration charge is an annual amount and accrues a twelfth a month, so a policy
that runs a full year carries the same charge as it did — but it is borne by the in-force of **each
month** rather than of the anniversary, which is what makes a decrementing block cost less. The
collection cost follows the *Zahlweise*: it is charged when a bill is actually collected, once a
year on a *jaehrlich* payer and twelve times on a *monatlich* one, which is what a collection cost
is and what the *Ratenzahlungszuschlag* was pricing all along.

**The *Zahlweise* is now a cash-flow fact rather than a loading with nothing behind it.** On the
annual grid the `instalments` column of `freq_loading_table.csv` could not be used for anything: the
whole loaded annual premium was collected at the anniversary whatever the mode. Here it sets the
cycle, so a fractionated payer's later instalments are collected on a block that has already lost
lives, and § 168 VVG's *Versicherungsperiode* is expressed rather than approximated. The instalments
of a policy year sum to exactly that year's annual amount, `φ` having multiplied the annual figure
once: loading an instalment again after dividing charges the surcharge twice (pitfall 10).

### The first-order *Deckungskapital* — a pricing diagnostic

Published because mechanic 11's central claim is checkable and a naive implementation fails it, and
labelled a pricing quantity because it is one: it is **not** a *Deckungsrückstellung*, it is not
*gezillmert*, it enters no cash flow, and nothing in this library discounts a published cash flow.

**Its argument is a policy year `y`, not a month**, like the equivalence it belongs to: a
first-order *Deckungskapital* is struck on the tariff's annual bases against an annual
*Rechnungszins*, and a monthly reserve would be a different quantity built on a rate this contract
does not have. `result_pols()` publishes it against the policy year of each month, so it is flat
across that year's twelve rows.

    res_pp_at(y,"BEF_PREM") = Σ_{u=y..n−1} v^(u−y+1)·(p₁(u)/p₁(y))·q₁(12u)·B(12u)
                              − Gn · Σ_{u=y..k−1} v^(u−y)·(p₁(u)/p₁(y))

with `res_pp_at(0,"BEF_PREM") = 0` by the equivalence, `res_pp_at(n,"BEF_PREM") = 0` by exhaustion,
and a strictly positive interior. `res_pp_at(y,"AFT_PREM") = res_pp_at(y,"BEF_PREM") + Gn·1{y < k}`.
The Thiele recursion the check asserts is

    ( res_pp_at(y,"BEF_PREM") + Gn·1{y < k} ) · (1 + i)
        = q₁(12y)·B(12y) + (1 − q₁(12y))·res_pp_at(y+1,"BEF_PREM")

The *gezillmert* companion subtracts the unamortised Zillmer balance,

    res_zill_pp_at(y, timing) = res_pp_at(y, timing) − z·k·G · [ Σ_{u=y..k−1} v^(u−y)(p₁(u)/p₁(y)) ] / ä

which is **`−z·k·G` at `y = 0`** — negative from the first day, exactly as mechanic 10 describes, and
back to zero at expiry. Whether a negative individual reserve must be floored at zero for
balance-sheet purposes — the *Nullstellung* question — was **not established** [R21] [REG-R54]
(research gap 11), and because the model publishes no balance-sheet reserve, the question does not
reach its cash flows.

### What `result_cf()` publishes

Indexed by the 0-based **month** `t`, contiguous from `12·duration_y` to `proj_len() − 1`, in this
order:

    pols_if, prem_gross, premiums, prem_rebate,
    claims_death, claims_lapse, claims_maturity,
    expenses, commissions, net_cf, liability_cf

The three premium columns are the amounts **collected in the month**, so on an annual *Zahlweise*
eleven rows in twelve carry zeros in them. `result_cf_annual()` sums the frame into policy years,
indexed by the contractual 1-based `policy_year`, with `pols_if` the count at the **start** of the
year — a **regrouping of the same numbers and never a second projection**, which is what lets the
annual worked example below stay annual and still be asserted cell by cell.

`prem_gross` is the **guaranteed** stream and does not enter `net_cf`; `premiums` is the **billed**
stream and does. Publishing both is required by the product — a model carrying one premium stream
cannot represent a German RLV [R6] — and `check_net_cf()` names exactly which columns enter the
identity, so there is no ambiguity about which to skip.

`liability_cf` is the eleventh column and is `−net_cf(t)` exactly: `net_cf` is income-positive, the
library-wide sign, and the outgo-positive orientation a valuation layer wants is published beside it
rather than left to a reader to flip. It was added to the list at the model stage, because the
conventions suite reads the identity **off the frame** — a model that publishes a `liability_cf`
cells and omits the column fails `test_net_cf_is_income_positive`. `expenses` **excludes**
`commissions` here, which is its own column, and `net_cf` subtracts the two separately.

### The published `check_*` identities

Five, each with a per-`t` residual companion `check_*_resid(t)`, each returning a `bool` over all
`t`, and all five called on **every** model point by the conventions suite.

| Check | Identity | Why it earns its place |
|---|---|---|
| `check_net_cf()` | On `result_cf()` row `t`: `net_cf = premiums − claims_death − claims_lapse − claims_maturity − expenses − commissions`, every term read from the published frame | delib's first ruling: the headline number is reconciled in code, not only in prose — and by a different route from `net_cf`'s own, which subtracts the kind-less `claims(t)` subtotal, so the check crosses both the cells-to-frame boundary and the `claims(t, kind)` dispatch |
| `check_pols_roll_fwd()` | `pols_if(t+1) = pols_if(t) − pols_death(t) − pols_lapse(t) − pols_maturity(t)`, and the three exits sum to `pols_if_init()` | The decrement roll-forward and its closure |
| `check_prem_split()` | On the instalments, `prem_gross_inst_pp(t) = prem_inst_pp(t) + prem_rebate_inst_pp(t)`, and on the annual amounts likewise, with `0 ≤ prem_rebate_inst_pp(t) < prem_gross_inst_pp(t)` in a month an instalment is due inside the paying term and all three zero in every other month | The product's signature identity, at every `t` and every *Zahlweise* — and, since the conversion, in every month rather than only at the anniversary |
| `check_res_roll_fwd()` | The Thiele recursion above, per **policy year**, plus `res_pp_at(0) = 0` and `res_pp_at(n) = 0` | The reserve mechanic 11 says a naive implementation gets wrong |
| `check_no_cash_value()` | `claims(t,"LAPSE") = 0` and `claims(t,"MATURITY") = 0` at every `t` | A statutory fact [R2] [R3] [R8], checked on every model point rather than asserted in prose |

Two further identities are **scalar rather than per-period** and are therefore asserted in
`tests/test_risikolebensversicherung_de.py` instead of published as `check_*` cells: the first-order
premium equivalence `G·ä = A + z·k·G + β·G·ä + γ·Γ`, and the surplus equivalence
`v_d·G·ä = decl_scale·surplus_share·(m/(1+m))·A`. Forcing a scalar identity into a per-`t` residual
would mean inventing a per-period decomposition the product does not have, which is worse than
putting it in the test module and saying so.

---

## Monthly processing order

For `t = t0 … 12n − 1`, in exactly this order. Steps 1 to 3 change only at an anniversary; the rest
run every month.

1. Set `duration(t) = t // 12`, `policy_year(t) = duration(t) + 1` and
   `x(t) = issue_age + duration(t)` (and `x₂(t)` where `lives = 2`). If `t ≥ 12n`, stop.
2. Read the schedules at `policy_year(t)`: `f(t)` from `benefit_schedule.csv`, `u(duration(t))` from
   `nvg_schedule.csv`; form `B(t) = S0·f(t)·u(duration(t))`. Both are flat across the policy year.
3. Read the table rates for each life at its own attained age; combine to a first-death rate where
   `lives = 2`, **before** any loading; form the **annual** `q₂(t)` on the policy's own sex and
   `q₁(t)` on the tariff's unisex blend, then the monthly `q₂ᵐ(t) = 1 − (1 − q₂(t))^(1/12)`.
4. **Beginning of month — premium instalment.** For `duration(t) < k`, set the annual
   `prem_gross_pp(t) = G·φ`, `prem_rebate_pp(t) = v_d·G·φ` and `prem_paid_pp(t)` as their
   difference; else all three zero. Where `prem_due(t)`, divide each by `r` to get the instalment;
   else all three instalments are zero. Take `premiums(t) = P_inst(t)·l(t)`.
5. **Beginning of month — expenses on the opening in-force.** Collection `a·P_inst(t)·l(t)` and a
   twelfth of the sum-related admin, `γ·B(t)·(1+π)^duration(t)/12·l(t)`; at `t = 0` **and only where
   `duration_y = 0`**, the acquisition cost and the initial commission; for `duration(t) ≥ 1`, the
   renewal commission on the instalment collected.
6. Apply the § 161 switch tranche by tranche to get `benefit_paid_pp(t)`.
7. **End of month — death.** `pols_death(t) = l(t)·q₂ᵐ(t)`;
   `claims(t,"DEATH") = benefit_paid_pp(t)·pols_death(t)`; claim expense on the deaths. Claimants
   have already paid whatever instalment fell due at step 4 — that is what "premium payment ceases
   at death" means on a grid with premiums in advance **[std]**, and applying a second `(1 − q₂ᵐ)`
   factor to `premiums(t)` charges the rule twice (pitfall 11).
8. **End of month — lapse.** `pols_lapse(t) = l(t)·(1 − q₂ᵐ(t))·wᵐ(t)`; `claims(t,"LAPSE") = 0`.
   Through the whole **final policy year**, `duration(t) ≥ n − 1`, `w` and hence `wᵐ` are 0 **[std]**.
9. **End of month — expiry.** At `t = 12n − 1` only,
   `pols_maturity(12n − 1) = l(12n − 1)·(1 − q₂ᵐ(12n − 1))`; `claims(12n − 1,"MATURITY") = 0`.
10. Roll forward `l(t+1)` and form `net_cf(t)`.

At `t = 12n − 1` the projection ends with no maturity payment, no tail state and `l(12n) = 0`.

---

## Known modeling pitfalls

These are the specific ways an implementation of **this** product looks right and is wrong. **Each
one becomes a test** in `tests/test_risikolebensversicherung_de.py`.

1. **Confusing the three "netto"s.** *Nettoprämie* (actuarial), *Nettobeitrag*/*Zahlbeitrag*
   (consumer) and *Nettotarif* (distribution) are unrelated [mechanic 4]. Assert the order the
   built model actually produces on the anchor —
   `prem_paid_pp(0)/φ < prem_net_level_pp() < prem_gross_pp(0)/φ`, i.e. 733,01 € < 1 084,80 € <
   1 275,41 € — and that no cells is named `prem_net_pp` or `nettobeitrag`. **The billed
   *Zahlbeitrag* sits *below* the actuarial *Nettoprämie***, because `Gn = A/ä` is struck on the
   loaded first-order rate and 90 % of that loading is handed straight back as
   *Beitragsverrechnung*. Asserting `Gn < P` instead would be asserting the absence of the
   product's central mechanic.
2. **Carrying only one premium stream.** A model with a single premium cannot represent this product
   [R6]. Assert `prem_gross_pp(t) > prem_paid_pp(t)` at every `t` on model point 1 and
   `prem_gross(t) > premiums(t)` in every month an instalment is actually collected, and
   `prem_gross(t) == premiums(t)` exactly on model point 12, where `surplus_form = keine`.
3. **Treating the *Zahlbeitrag* as guaranteed.** Only the *Bruttobeitrag* is [R6] [REG-R27]. Assert
   that setting `decl_scale = 0` raises `premiums` to `prem_gross` at every `t` and changes **no**
   claim, no decrement and no expense other than the collection cost that scales with the billed
   premium.
4. **Inventing a *Rückkaufswert* — and the narrower point that replaced it.** This model pays none,
   and asserts so: `claims(t,"LAPSE") == 0.0` and `claims(t,"MATURITY") == 0.0` at every `t` and
   every model point, `check_no_cash_value()` is `True`, and no `av_pp_at`, `surr_value` or paid-up
   cells exist in `Projection`. **What that check does *not* license is the sentence "a German term
   assurance has no surrender value".** No § 169 Abs. 1 duty attaches on *Kündigung* — the *gewiss*
   test, read verbatim [R2] — but the GDV model wording and the Hannoversche AVB both convert to a
   *beitragsfreie Versicherung* and pay a *Rückkaufswert* under § 169, less a *Stornoabzug*, where
   the paid-up sum fails a minimum [S1] [S4]; only Cosmos pays nothing [S3]. The amount is nil or
   nominal in all of them, which is why the model's zero is defensible — as an approximation of a
   small number, not as an identity [R2] [R3] [R8] [S1] [S3] [S4].
5. **Concluding there is no *Deckungskapital*.** A level premium against a rising death rate builds
   one (mechanic 11). Assert `res_pp_at(0,"BEF_PREM") == 0` and `res_pp_at(n,"BEF_PREM") == 0` to
   1e-9, that `res_pp_at(t,"BEF_PREM") > 0` at some interior `t` on the anchor, that
   `res_zill_pp_at(0,"BEF_PREM") == −z·k·G` to 1e-9 (the two are formed by different summations,
   so the tolerance is headroom, even though they agree exactly on the anchor), and that
   `check_res_roll_fwd()` is `True`.
6. **Letting `sex` into the price.** Unlawful in Germany for contracts concluded from 21 December
   2012 — AGG § 33 Abs. 5 confines the derogation to *Versicherungsverhältnisse* "die vor dem
   21. Dezember 2012 begründet werden", and § 20 Abs. 2 leaves no actuarial justification open for
   sex at all [R13] [REG-R34].
   Model points 1 and 2 differ **only** in `sex`: assert their `prem_gross_pp(t)`,
   `prem_paid_pp(t)` and `beitragsverrechnung_rate()` are identical to 1e-12, while their
   `claims_death` totals differ by a factor near two.
7. **Applying the *Sicherheitszuschlag* to the projection.** `q₁` prices, `q₂` projects. Assert that
   `claims_death` is invariant to `sicherheitszuschlag_m` while `prem_gross` is not, and that
   `mort_rate_tar(t) / mort_rate(t)` equals `2.25 × (unisex blend / own-sex rate)` — 1.6875 for a
   male, 3.375 for a female on the shipped proxy, the blend being `0.75 × q̃(M)` — rather than 2.25
   for both.
8. **Applying the § 161 switch beyond three years, or to the wrong things.** Assert
   `suicide_factor(t) == 1 − suicide_share` exactly for the **first thirty-six months** and `== 1`
   from month 36 on model point 1; that it is `1` at every projected `t` on the in-force point 8
   (`t0 = 144`); and that it touches neither `claims_lapse` nor `claims_maturity`, both of which are
   zero anyway. The window is thirty-six months and not three rows, and because the statute measures
   it in years its boundary falls on an anniversary either way.
9. **Forgetting that the clock restarts for a *Nachversicherungsgarantie* increment.** All three
   retrieved wordings restart it "bezüglich des geänderten oder wiederhergestellten Teils" [S1] [S3]
   [S4], so this is the market's rule and not a modelling convenience. On model
   point 9, in the policy year of and the two policy years after each increase, assert
   `1 − suicide_share < benefit_paid_pp(t)/benefit_pp(t) < 1` strictly — the base tranche out of its
   window and the increment inside it — and that each window opens and closes on an anniversary,
   months 60 to 95 for the first increment.
10. **Mishandling the *Ratenzahlungszuschlag*.** `φ` multiplies the **annual** billed amount, so
    both premium streams and the rebate carry it once, and the instalment is that loaded amount
    divided by `r`. Assert `check_prem_split()` on every model point; that `prem_gross_pp(0)` on
    model point 4 (*monatlich*) is exactly `1.05 ×` the same cell recomputed at `jaehrlich`; and
    that the twelve instalments of a policy year sum to exactly the year's annual amount — a single
    loading, not one applied to each stream separately and not one applied again to each instalment.
11. **Double-counting premium cessation at death.** Instalments are collected at the beginning of
    the month and claims fall at its end, so a claimant has already paid. Assert
    `premiums(t) == prem_inst_pp(t) * pols_if(t)` exactly, with no `(1 − q₂ᵐ)` factor anywhere. The
    finer grid narrows the error — 0,038 € in the first month against 0,46 € in the first year —
    without removing the trap: there are now twelve times as many chances to apply it.
12. **Running the premium past the *Beitragszahlungsdauer*.** On model point 6 (`k = 12` years,
    `n = 20`) assert `prem_gross_pp(t) == premiums(t) == prem_rebate_pp(t) == 0` for
    `t = 144…239`, while `claims_death(t) > 0` there and `res_pp_at(y,"BEF_PREM")` is falling. The
    boundary is an anniversary, the *Beitragszahlungsdauer* being stated in whole years; the last
    instalment of this *halbjaehrlich* cell falls in month 138.
13. **Hard-coding a constant sum insured.** Two of the three German shapes fall (mechanic 3). Assert
    `benefit_pp(t)` is flat on point 1; falls linearly to `S0/n` on point 4; and on point 5 falls
    **slowly then fast**, `benefit_pp(12) − benefit_pp(0) < benefit_pp(12(n−1)) − benefit_pp(12(n−2))`
    in absolute size — the property a linear schedule gets backwards. And assert that each shape
    steps on the **anniversary** and is flat across a policy year: a declining *Versicherungssumme*
    does not decline monthly because the grid does.
14. **Combining two lives after loading instead of before.** On model point 10 assert
    `Q̃ == q̃_A + q̃_B − q̃_A·q̃_B` exactly and `Q̃ < q̃_A + q̃_B` strictly, and that `q₁` is
    `(1+m)·rf` times the combined **blend**, not the combination of two separately loaded rates.
15. **Returning the *Kostenüberschuss* as well as the *Risikoüberschuss*.** The model returns only
    the mortality margin; the cost result emerges in `net_cf` and stays there. Assert that
    `prem_rebate` is invariant to `maint_prem_pct` and `comm_rate_renew`, while `net_cf` is not.
16. **Taking the whole-market *Stornoquote* as the term-life lapse rate.** Structurally wrong
    [R18] (research gap 13). Assert the **annual** `lapse_rate(t) == 0.06` through months 0–11,
    `== 0.04` through months 12–35 and `== 0.03` from month 36; that `lapse_rate(t) == 0` through
    the whole final policy year while the table's own row for policy year `n` still reads 0.03; and
    that twelve of `lapse_rate_mth` compound back to the year's rate exactly. Spreading the annual
    rate by dividing it by twelve instead would leave the in-force at every anniversary wrong.
17. **Letting `rating_factor` scale the benefit.** A *Risikozuschlag* is a mortality loading, not a
    benefit uplift (mechanic 9). On model point 11 assert `benefit_pp(t)` is invariant to
    `rating_factor` while `prem_gross_pp` and `claims_death` both scale with it, and that the ratio
    `prem_paid_pp(0)/prem_gross_pp(0)` moves by less than one percentage point when `rating_factor`
    goes from 1.00 to 1.75 — the invariance that follows from loading both bases.
18. **Treating the *Über-Kreuz-Versicherung* as a different product.** It is a contracting structure
    with identical cover and identical cash flows; only the *Erbschaftsteuer* outcome changes [R15]
    [REG-R46]. Assert that no model-point column, no cells and no CSV in this product refers to it,
    and that the notes say why.

---

## Policyholder behaviour modelling

All dynamic formulas are **[std]** reference constructions; **there is no German calibration
evidence for any of them** (research gap 13).

- **Base lapse [std].** The duration table above, 6 % / 4 % / 3 %, with `w(n − 1) = 0`. Its whole
  argument is structural: nothing is forfeited by lapsing, exit is frictionless in time as well as in
  money because the *Versicherungsperiode* follows the *Zahlweise* [R8], and the need amortises.
- **Premium-shock lapse [std] (optional module, off in the base run).** The product's distinctive
  behavioural risk is that the insurer can raise the bill without changing a guaranteed term, simply
  by cutting the declaration [R6]. The reference multiplier on `w(t)`:

      M_shock(t) = 1 + λ_s · max( 0, prem_paid_pp(t)/prem_paid_pp(t−12) − 1 )

  with `λ_s = 2.0` **[std]** and base run `λ_s = 0`, so `M_shock ≡ 1`. The ratio is between
  **consecutive renewals** and so reads the annual *Zahlbeitrag* twelve months back, not one: a
  comparison of consecutive instalments would fire on the *Zahlweise* rather than on the
  declaration, and on an annual payer it would divide by a zero bill in eleven months of twelve. It
  is 1 through the whole of policy year 1, which has no preceding bill. It is inert in the base run
  because `prem_paid_pp` is level there — it bites only when `decl_scale` is stressed, which is
  exactly when it should. **A model that raises the *Zahlbeitrag* toward the *Bruttobeitrag* in a
  stress and leaves the lapse assumption unchanged is understating the stress.**
- **Selective lapse [std] (optional module, off in the base run).** Healthy lives can re-underwrite
  into a cheaper contract; impaired lives cannot, so persisters' mortality drifts up:

      q₂_eff(t) = q₂(t) · [ 1 + λ · max(0, w_cum(t) − w_ref) ]

  with `w_ref = 0.25` and `λ = 0.30` **[std]**, base run `λ = 0`. **delib does not model selective
  lapse in the base run** — one basis for stayers and leavers — which is a known simplification and
  pitfall-adjacent rather than a pitfall: it is stated here so it is not discovered.
- **No dynamic surrender, no *Widerruf* decrement, no option take-up.** There is nothing to surrender
  [R2], so the whole of the exit machinery is lapse and a lapse pays nothing; the 30-day § 152
  *Widerrufsfrist* [R8] [REG-R23] sits inside the year-one lapse rate **[std]**; and
  *Nachversicherungsgarantie* and *Dynamik* take-up is **exogenous**, supplied as a schedule rather
  than modelled as a decision, because no event list, cap, window or age limit was established
  (research gap 7).

---

## Worked example

**Configuration.** Model point 1, the anchor cell, in full: `point_id = 1`,
`policy_id = RLV-000001`, `issue_age = 35`, `sex = M`, `smoker = N`,
`sum_assured = 300 000 €`, `policy_term = 25`, `prem_term = 25`,
`premium_form = laufend`, `prem_freq = jaehrlich` (`prem_freq_load = 1.000`,
`instalments = 1`), `benefit_schedule_id = konstant` (`benefit_factor = 1.0` at every `t`),
`nvg_schedule_id = keine` (`sum_uplift = 1.0` at every `t`),
`surplus_form = beitragsverrechnung`, `lives = 1`, `issue_age2 = 0`, `smoker2 = -`,
`rating_factor = 1.00`, `mort_table_id = dav2008t_proxy`, `duration_y = 0`,
`issue_date = 2026-01-01`. Hence `t0 = 0`, `proj_len_y() = 25` and `proj_len() = 300` so the frame
is `t = 0 … 299` **months**, cover to attained age 60, and the annual table below — the monthly
frame summed into policy years by `result_cf_annual()` — is the **entire** projection.

**Assumptions, each tagged.** *Mortality*: the shipped [std] proxy
`mort_rate(M, N, x) = 0.00040 × 1.095^(x − 30)` at attained ages 35 to 59, so
`mort_rate(0) = 0.00040 × 1.095^5` and `mort_rate(24) = 0.00040 × 1.095^29` **[std]**;
`mort_be_factor = 1.00` **[std]**. *Tariff mortality*: the unisex 50/50 blend
`0.00030 × 1.095^(x − 30)` **[std]** loaded by `1 + m` with `sicherheitszuschlag_m = 1.25`
**[std]**, and `sex_mix_male = 0.50` **[std]** [R13] [REG-R34]. *Interest*:
`rechnungszins = 1,00 %` — the DeckRV ***Höchstzinssatz***, a **ceiling the model adopts as the
rate**; a retrieved carrier prices its term tariff at 0,25 % instead **[R10] [REG-R14] [REG-R15]
[S3]** — used only in the premium equivalence and the first-order reserve and **never** to discount
a published cash flow. *Loadings*: `zillmer_rate = 0.025` of the *Beitragssumme* at the
*Höchstzillmersatz* ceiling **[R10] [REG-R16]**, which bounds the *zillmerbare* part rather than the
whole acquisition cost **[S1] [S3]**, level **[std]**; `comm_rate_init = 0.020` of the *Beitragssumme* **[std]**;
`beta_tariff = 0.05` of each *Bruttobeitrag* **[std]**; `gamma_rate = 0.00030` of the
*Versicherungssumme* a year **[std]**. *Surplus*: `surplus_share = 0.90`, the MindZV minimum
allocation from the *Risikoergebnis* **[R9] [REG-R18]** with the choice of the minimum **[std]**;
`decl_scale = 1.00` **[std]**; `v_max = 0.95` **[std]**; so `v_d` is derived, not assumed.
*Modelled expenses*: `maint_prem_pct = 0.03` of each *Zahlbeitrag* **[std]**;
`comm_rate_renew = 0.010` of each *Zahlbeitrag* instalment from policy year 2 **[std]**;
`expense_infl = 0.02` on the sum-related admin only **[std]**; `claim_expense = 250 €` per death
claim **[std]**. *Behaviour*: lapse 6 % in policy year 1, 4 % in policy years 2 and 3, 3 % from
policy year 4, with `lapse_rate ≡ 0` through the whole of policy year 25 because that year ends at
expiry **[std]**, and each annual rate spread to the month at `1 − (1 − w)^(1/12)` **[std]**;
`suicide_share = 0.03` applied to death claims in months 0 to 35, policy years 1 to 3, only **[std]** [R1]
[REG-R26]. *Modules*: premium-shock lapse `λ_s = 0` and selective lapse `λ = 0`, both **off**
**[std]**. No *Nachversicherungsgarantie*, no *Dynamik*, no rider, no premium tax [R16], no
discounting of any published cash flow.

`expenses` below is the total of acquisition, sum-related admin, collection and claim expense;
`commissions` is the initial *Abschlussprovision* plus the *Bestandspflegeprovision*. All amounts in
euros; `pols_if` to six decimals; cash flows to the cent. The **Total** row is summed at full
precision and then rounded, which can differ in the last cent from adding the displayed cells.

**The annual view**, `result_cf_annual()`, indexed by the contractual 1-based policy year, with
`pols_if` the count at the **start** of the year:

| policy year | age | pols_if | prem_gross | premiums | prem_rebate | claims_death | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 35 | 1.000000 | 1,275.41 | 733.01 | 542.40 | 178.15 | 269.04 | 637.71 | −351.88 |
| 2 | 36 | 0.939408 | 1,198.13 | 688.60 | 509.54 | 185.01 | 105.44 | 6.89 | 391.26 |
| 3 | 37 | 0.901210 | 1,149.41 | 660.60 | 488.82 | 194.35 | 102.78 | 6.61 | 356.86 |
| 4 | 38 | 0.864508 | 1,102.60 | 633.69 | 468.91 | 211.46 | 100.58 | 6.34 | 315.32 |
| 5 | 39 | 0.837880 | 1,068.64 | 614.18 | 454.47 | 224.41 | 99.08 | 6.14 | 284.55 |
| 6 | 40 | 0.812008 | 1,035.64 | 595.21 | 440.43 | 238.14 | 97.59 | 5.95 | 253.53 |
| 7 | 41 | 0.786867 | 1,003.58 | 576.78 | 426.80 | 252.69 | 96.13 | 5.77 | 222.20 |
| 8 | 42 | 0.762432 | 972.41 | 558.87 | 413.54 | 268.11 | 94.68 | 5.59 | 190.50 |
| 9 | 43 | 0.738680 | 942.12 | 541.46 | 400.66 | 284.43 | 93.25 | 5.41 | 158.36 |
| 10 | 44 | 0.715587 | 912.67 | 524.53 | 388.13 | 301.71 | 91.84 | 5.25 | 125.73 |
| 11 | 45 | 0.693130 | 884.03 | 508.07 | 375.95 | 320.01 | 90.45 | 5.08 | 92.53 |
| 12 | 46 | 0.671287 | 856.17 | 492.06 | 364.11 | 339.37 | 89.07 | 4.92 | 58.70 |
| 13 | 47 | 0.650036 | 829.06 | 476.48 | 352.58 | 359.84 | 87.70 | 4.76 | 24.17 |
| 14 | 48 | 0.629355 | 802.69 | 461.32 | 341.36 | 381.49 | 86.35 | 4.61 | −11.13 |
| 15 | 49 | 0.609224 | 777.01 | 446.57 | 330.44 | 404.37 | 85.01 | 4.47 | −47.28 |
| 16 | 50 | 0.589621 | 752.01 | 432.20 | 319.81 | 428.54 | 83.68 | 4.32 | −84.34 |
| 17 | 51 | 0.570527 | 727.66 | 418.20 | 309.45 | 454.06 | 82.35 | 4.18 | −122.39 |
| 18 | 52 | 0.551923 | 703.93 | 404.57 | 299.36 | 480.98 | 81.04 | 4.05 | −161.50 |
| 19 | 53 | 0.533788 | 680.80 | 391.27 | 289.53 | 509.37 | 79.73 | 3.91 | −201.74 |
| 20 | 54 | 0.516105 | 658.25 | 378.31 | 279.94 | 539.28 | 78.42 | 3.78 | −243.18 |
| 21 | 55 | 0.498853 | 636.24 | 365.67 | 270.58 | 570.78 | 77.12 | 3.66 | −285.89 |
| 22 | 56 | 0.482016 | 614.77 | 353.32 | 261.45 | 603.90 | 75.82 | 3.53 | −329.94 |
| 23 | 57 | 0.465576 | 593.80 | 341.27 | 252.53 | 638.72 | 74.52 | 3.41 | −375.38 |
| 24 | 58 | 0.449515 | 573.32 | 329.50 | 243.82 | 675.27 | 73.22 | 3.29 | −422.28 |
| 25 | 59 | 0.433815 | 553.29 | 317.99 | 235.30 | 723.59 | 72.78 | 3.18 | −481.56 |
| **Total** | | | **21,303.65** | **12,243.75** | **9,059.91** | **9,768.05** | **2,367.66** | **752.81** | **−644.78** |

`claims_lapse(t)` and `claims_maturity(t)` are 0.00 at every `t` and are omitted for width; both are
required columns of `result_cf()` and `check_no_cash_value()` asserts them. `liability_cf(t) =
−net_cf(t)` is omitted for the same reason — it is the last column with its sign turned over.

**The monthly view**, the twelve months of policy year 1 on `result_cf()` — the shape the annual
grid could not show. Month 0 collects the whole year's *Zahlbeitrag*, this cell being a *jaehrlich*
payer, and bears the acquisition cost and the initial commission; the other eleven collect nothing
and carry a death claim and a twelfth of the sum-related admin charge:

| t | pols_if | prem_gross | premiums | prem_rebate | claims_death | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|
| 0 | 1.000000 | 1,275.41 | 733.01 | 542.40 | 15.27 | 188.93 | 637.71 | −108.90 |
| 1 | 0.994805 | 0.00 | 0.00 | 0.00 | 15.20 | 7.47 | 0.00 | −22.67 |
| 2 | 0.989637 | 0.00 | 0.00 | 0.00 | 15.12 | 7.44 | 0.00 | −22.55 |
| 3 | 0.984495 | 0.00 | 0.00 | 0.00 | 15.04 | 7.40 | 0.00 | −22.43 |
| 4 | 0.979380 | 0.00 | 0.00 | 0.00 | 14.96 | 7.36 | 0.00 | −22.32 |
| 5 | 0.974292 | 0.00 | 0.00 | 0.00 | 14.88 | 7.32 | 0.00 | −22.20 |
| 6 | 0.969231 | 0.00 | 0.00 | 0.00 | 14.80 | 7.28 | 0.00 | −22.09 |
| 7 | 0.964195 | 0.00 | 0.00 | 0.00 | 14.73 | 7.24 | 0.00 | −21.97 |
| 8 | 0.959186 | 0.00 | 0.00 | 0.00 | 14.65 | 7.21 | 0.00 | −21.86 |
| 9 | 0.954203 | 0.00 | 0.00 | 0.00 | 14.57 | 7.17 | 0.00 | −21.74 |
| 10 | 0.949246 | 0.00 | 0.00 | 0.00 | 14.50 | 7.13 | 0.00 | −21.63 |
| 11 | 0.944314 | 0.00 | 0.00 | 0.00 | 14.42 | 7.09 | 0.00 | −21.52 |
| **Year 1** | 1.000000 | **1,275.41** | **733.01** | **542.40** | **178.15** | **269.04** | **637.71** | **−351.88** |

The **Total** row is summed **at full precision, then rounded**, which is not the same as adding the
twenty-five displayed annual cells: `prem_gross` 21 303,65 € against 21 303,64 €, `premiums`
12 243,75 € against 12 243,73 €, `claims_death` 9 768,05 € against 9 768,03 €, `expenses`
2 367,66 € against 2 367,67 €. Only `prem_rebate`, `commissions` and `net_cf` agree.
**Assert the full-precision totals**; a test that adds the rounded rows tests the rounding.

### What the monthly grid moved, and what it did not

The annual-step model's own figures are kept here as the cross-check rather than deleted.
**Unmoved**, because they are annual constructions the conversion never touched: `ä = 21,6374941`,
`A = 23 472,374330 €`, `Γ = 6 491 248,23 €`, `G = 1 275,411882 €`, `Gn = 1 084,800958 €`,
`v_d = 0,42527476`, the *Zahlbeitrag* 733,011403 €, the whole *Deckungskapital* including its
7 553,29 € peak, and `pols_if` at **every policy anniversary** — the column above is the annual
model's to the last displayed digit, and to 4e-15 across all fourteen model points.

**Moved**, and that is the reason for the finer grid:

| | annual grid | monthly grid |
|---|---|---|
| `claims_death` total | 9 899,20 € | **9 768,05 €** |
| `expenses` total | 2 396,51 € | **2 367,66 €** |
| `net_cf` total | −804,77 € | **−644,78 €** |
| policy year 1 `net_cf` | −359,51 € | **−351,88 €** |
| crossover to negative | policy year 14 | policy year 14 |
| deaths / lapses over the run | 0,03305608 / 0,53554078 | **0,03261764 / 0,53597922** |
| expiries | 0,43140314 | 0,43140314 |
| model point 4 (*monatlich*) `premiums` | 4 471,82 € | **4 400,26 €** |

Death claims fall because a claim now falls in the month of death rather than at the year end, so
it is borne by a block that has decremented for part of the year — except in the final policy year,
where lapse is zero under both grids and the year's deaths are therefore identical. Expense falls
because a twelfth of the admin charge accrues each month on that month's in-force. The premium
columns are unchanged on the ten annual-*Zahlweise* points and lower on the four fractionated ones,
where instalments after the first are collected on a block that has already lost lives: 0,95 % less
on the *halbjaehrlich* point 6, 1,67 % less on the *monatlich* point 10. And the closure identity's
**total** is unchanged at 1,00000000 while its **split** moves, deaths and lapses now interleaving
month by month instead of the whole year's lapses being taken after the whole year's mortality.

### Independent checks

Three cells rebuilt a different way, and three closure identities. Every figure below is arithmetic a
reader can follow with a calculator from the tagged assumptions above; none of it reads a cell of the
model.

***1. The premium engine, from the equivalence rather than the closed form.*** The equivalence is
`G·ä = A + z·k·G + β·G·ä + γ·Γ`, and at `G = 1 275,411882 €` its two sides are

    G·ä    = 1 275,411882 × 21,6374941 = 27 596,717080
    A                                  = 23 472,374330
    z·k·G  = 0,025 × 25 × 1 275,411882 =    797,132426
    β·G·ä  = 0,05 × 27 596,717080      =  1 379,835854
    γ·Γ    = 0,00030 × 6 491 248,23    =  1 947,374470   sum = 27 596,717080

The *Beitragsverrechnungssatz* then follows from the *Zahlbeitrag* section's one-line identity
**without forming `G` at all**: the risk share of the gross premium is
`1 − 0,05 − 2 744,506896/27 596,717080 = 0,85054952`, so
`v_d = 0,90 × (1,25/2,25) × 0,85054952 = 0,50 × 0,85054952 = 0,42527476`, the model's
`beitragsverrechnung_rate()` to eight decimals, and
`prem_paid_pp(0) = 0,57472524 × 1 275,411882 = 733,011403 €`. Two things follow. The surplus share
and the margin fraction multiply to exactly one half, so on this calibration the *Zahlbeitrag* is
"the *Bruttobeitrag* less half its risk element". And the derivation runs on `m`, `β`, `γ`, `z` and
`k` and never touches the mortality **level** — which is why moving the level moves both premiums
together and leaves the ratio nearly still.

***2. The first month `t = 0`, rebuilt from the table rate up.*** At attained age 35 the **annual**
rate is `q₂(0) = 0,00040 × 1,095⁵ = 0,00040 × 1,57423874 = 0,00062969550`, and the **monthly** rate
applied is `q₂ᵐ(0) = 1 − (1 − 0,00062969550)^(1/12) = 0,000052489776` — twelve of which compound
back to exactly `q₂(0)`, which is the whole reason the conversion leaves the in-force at every
anniversary alone. Policy year 1 is inside the § 161 window, so a claim pays
`0,97 × 300 000 = 291 000 €`, giving
`claims_death(0) = 291 000 × 1,000000 × 0,000052489776 = 15,274525` (table: 15.27). The expense
line is four numbers and only one of them is large:

    acquisition net of commission  (0,025 − 0,020) × 25 × 1 275,411882 = 159,426485
    sum-related admin, one twelfth 0,00030 × 300 000 × 1,02⁰ / 12      =   7,500000
    collection, on the instalment  0,03 × 733,011403                   =  21,990342
    claim expense                  250 × 0,000052489776                =   0,013122   = 188,929950

with `commissions(0) = 0,020 × 25 × 1 275,411882 = 637,705941 €` on its own line, and
`733,011403 − 15,274525 − 188,929950 − 637,705941 = −108,899012 €`. **The first month's strain is
the initial commission**: alone it is 87 % of the premium collected that month, which is why an
early lapse hurts on a contract that pays nothing on lapse. Summed over policy year 1 the twelve
months give `−351,883322 €`, the annual table's first row.

***3. The third policy year, rebuilt through two decrement steps***, reading nothing from the
recursion. Twelve months of `(1 − q₂ᵐ)(1 − wᵐ)` collapse to the annual `(1 − q₂)(1 − w)`, so
`l(12) = [(1 − 0,000052489776)(1 − 0,005143)]¹² = 1 × (1 − 0,00062969550) × (1 − 0,06) =
0,93940809`; with `q₂(12) = 0,00040 × 1,095⁶ = 0,00068951657` and `w = 0,04`,
`l(24) = 0,93940809 × (1 − 0,00068951657) × (1 − 0,04) = 0,90120993` — both the figures the
annual-step model printed. With `q₂(24) = 0,00040 × 1,095⁷ = 0,00075502064` spread over policy year
3's twelve months, the deaths of that year total `0,000667867276` and
`claims_death = 291 000 × 0,000667867276 = 194,349377` (table: 194.35). Using the contractual
300 000 € here gives 200,36 € — a 3 % overstatement that runs for three years and then disappears,
the kind of error a totals-only test misses.

***Closure 1 — the decrements account for the whole policy.*** Over the three hundred months:
deaths **0,03261764**, lapses **0,53597922**, expiries **0,43140314**, total **1,00000000** =
`pols_if_init()`, and `pols_if(300) = 0` exactly, which is what lets `result_cf()` stop at
`proj_len() − 1 = 299`. The expiring cohort is the annual-step model's own figure to the last digit,
lapse being zero through the final policy year under either grid. The split between deaths and
lapses is **not** — 0,03305608 and 0,53554078 on the annual grid — because the two decrements now
interleave month by month, each eroding the exposure the other works on. Keeping the table's own 3 %
in the final policy year instead would give 0,54895 and 0,41846, and **no cash flow moves either
way**.

***Closure 2 — the § 161 wedge is the only thing between claim events and claim amounts.*** Expected
claim events at the contractual sum are `300 000 × 0,03261764 = 9 785,291238 €` against claims paid
of `9 768,048760 €`. The difference is **17,242478 €**, which is exactly
`0,03 × 300 000 × 0,00191583088 = 9 000 × 0,00191583088 = 17,242478 €`, the deaths of the **first
thirty-six months** — policy years 1 to 3. So the *Selbsttötung* switch is the **only** thing
standing between events and amounts on this cell — no lapse pays, no expiry pays, the schedule is
flat. An implementation applying the switch to every month, or to a lapse, or over the wrong window
breaks this while leaving every total plausible.

***Closure 3 — the cash flow statement, which is `check_net_cf()`.*** At full precision,
`12 243,747304 − 9 768,048760 − 2 367,661171 − 752,813300 = −644,775928 €`. Note which columns are
**not** in it: `prem_gross` is the guaranteed stream and does not enter, and `prem_rebate` is the
difference between the two premium columns and must not be subtracted again. That ambiguity is why
delib requires `check_net_cf()` of every model.

***And the reserve mechanic 11 says a naive implementation gets wrong.*** On **policy-year**
arguments, the *Deckungskapital* being an annual construction:
`res_pp_at(0,"BEF_PREM") = 0` exactly, `res_pp_at(25,"BEF_PREM") = 0` exactly, and the interior peaks
at **7 553,29 €** in policy year 15 — **2,52 % of the sum insured**. The Thiele step at the peak:
`(7 553,290695 + 1 084,800958) × 1,01 = 8 724,472569` against
`0,00414558817 × 300 000 + (1 − 0,00414558817) × 7 511,937517 = 8 724,472569`. The *gezillmerte*
companion opens at `−797,132426 € = −z·k·G`: negative from the first day.

***What the sign of the total means, and what it does not.*** `net_cf` sums to **−644,78 €** here
and to **+4 252,82 €** on model point 2, the same cell with `sex = F`. Neither is a profit measure —
the stream is undiscounted, the tariff was struck at 1,00 % on no-lapse survivorship, and no reserve
is held against the later years — but the *difference* is the unisex cross-subsidy the law requires:
the tariff prices a 50/50 blend, the declaration returns 90 % of the margin measured against that
blend, and a male life then claims about a third more than the tariff's own best estimate while
paying, to the cent, the same premium as a female one. The book average is positive; the anchor
alone is not, and the model is meant to show that rather than hide it.

### Variant — the declaration withdrawn (`decl_scale = 0`)

The product's largest policyholder risk, and the one § 163 VVG does **not** govern. Selected rows of
model point 1 on the annual view, with the **Total** row covering all twenty-five years:

| policy year | age | pols_if | prem_gross | premiums | prem_rebate | claims_death | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 35 | 1.000000 | 1,275.41 | 1,275.41 | 0.00 | 178.15 | 285.31 | 637.71 | 174.25 |
| 2 | 36 | 0.939408 | 1,198.13 | 1,198.13 | 0.00 | 185.01 | 120.72 | 11.98 | 880.42 |
| 3 | 37 | 0.901210 | 1,149.41 | 1,149.41 | 0.00 | 194.35 | 117.45 | 11.49 | 826.12 |
| 13 | 47 | 0.650036 | 829.06 | 829.06 | 0.00 | 359.84 | 98.28 | 8.29 | 362.65 |
| 24 | 58 | 0.449515 | 573.32 | 573.32 | 0.00 | 675.27 | 80.53 | 5.73 | −188.22 |
| 25 | 59 | 0.433815 | 553.29 | 553.29 | 0.00 | 723.59 | 79.84 | 5.53 | −255.68 |
| **Total** | | | **21,303.65** | **21,303.65** | **0.00** | **9,768.05** | **2,639.46** | **837.99** | **8,058.16** |

`pols_if`, `claims_death` and `prem_gross` are **identical to the last bit** at every `t`. What moves
is `premiums`, 12 243,75 € → 21 303,65 €, a **74,0 % increase in the customer's bill for no change
whatever in cover**, and with it the two flows that scale with the billed premium: `expenses`
+271,80 € (collection at 3 %) and `commissions` +85,18 € (renewal at 1 %). `net_cf` goes from
−644,78 € to +8 058,16 €. **No § 163 procedure, no *Treuhänder*, no right of objection**, because no
guaranteed term has moved — and it is a one-Reference change. The stress runs with the
premium-shock lapse module **off**, so the table shows the mechanical effect alone; switching
`shock_lapse_lambda` on is what a stress of this shape should carry, and its omission is why the
base run's `λ_s = 0` is stated rather than assumed.

### Variant — the second premium form (`einmal`, model point 7)

The same engine at `k = 1`: 50 M N, 100 000 € `konstant`, ten years' cover, a single
*Einmalbeitrag*, annual mode, participating. With `ä = 1` exactly the equivalence collapses to
`G = (A + γ·Γ)/(1 − β − z) = (5 895,894609 + 280,265049)/0,925 = 6 676,929360 €`, and
`Gn = A/ä = A = 5 895,894609 €`; `v_d = 0,44151243`, so the customer pays 3 728,98 € once, in month
0 and nowhere else:

| policy year | age | pols_if | prem_gross | premiums | prem_rebate | claims_death | expenses | commissions | net_cf |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 50 | 1.000000 | 6,676.93 | 3,728.98 | 2,947.95 | 231.67 | 174.98 | 133.54 | 3,188.79 |
| 2 | 51 | 0.937691 | 0.00 | 0.00 | 0.00 | 240.16 | 28.75 | 0.00 | −268.91 |
| 3 | 52 | 0.897762 | 0.00 | 0.00 | 0.00 | 251.77 | 28.12 | 0.00 | −279.89 |
| 4 | 53 | 0.859312 | 0.00 | 0.00 | 0.00 | 273.33 | 27.62 | 0.00 | −300.96 |
| 5 | 54 | 0.830845 | 0.00 | 0.00 | 0.00 | 289.39 | 27.29 | 0.00 | −316.67 |
| 6 | 55 | 0.803073 | 0.00 | 0.00 | 0.00 | 306.29 | 26.95 | 0.00 | −333.24 |
| 7 | 56 | 0.775968 | 0.00 | 0.00 | 0.00 | 324.06 | 26.61 | 0.00 | −350.68 |
| 8 | 57 | 0.749502 | 0.00 | 0.00 | 0.00 | 342.75 | 26.27 | 0.00 | −369.02 |
| 9 | 58 | 0.723645 | 0.00 | 0.00 | 0.00 | 362.36 | 25.93 | 0.00 | −388.29 |
| 10 | 59 | 0.698372 | 0.00 | 0.00 | 0.00 | 388.29 | 25.95 | 0.00 | −414.24 |
| **Total** | | | **6,676.93** | **3,728.98** | **2,947.95** | **3,010.07** | **418.47** | **133.54** | **166.90** |

Only `net_cf` drifts against its rounded cells, by one cent (166,90 € against 166,89 €). Three things
this form shows that the level form does not. **The shape inverts** — one large inflow then nine
years of pure outgo, against a level-premium cell that is thin and positive early and thin and
negative late. **The renewal commission and the collection cost stop with the premium**, so
`commissions(t) = 0` from month 12 while `claims_death(t)` runs to expiry — the arrangement
`check_prem_split()` also guards on model point 6, where an *abgekürzte Beitragszahlungsdauer* pays
its last instalment in month 138 against twenty years of cover. **And `v_d` is higher, 0,44151243 against
0,42527476**, because with one premium instead of twenty-five the Zillmer charge is 25 ‰ of a much
smaller *Beitragssumme*, so the risk share of the gross premium is larger.

The form is a **[std]** construction and no German standalone RLV in the corpus is written on it (the
out-of-scope *Restschuldversicherung* is, and it is a different product sold a different way). It is
here because it exercises the premium engine at `k = 1`, **not** as evidence of a market form.

### What the conversion to a monthly step changed in these notes

The model was moved from an annual grid to a monthly one after these notes were written, and the
sentences that stopped being true were restated rather than left standing. What changed here:

1. **The frame.** `t` counts policy months, `proj_len() = 12 · policy_term`, and the worked example
   is now **two tables** — the twelve months of policy year 1 on `result_cf()`, and the whole run
   summed into policy years by `result_cf_annual()`, which is the view every figure the notes quote
   is stated on. The annual grid's own totals are kept beside them as the cross-check.
2. **The two speeds.** `mort_rate` and `lapse_rate` stay the **annual** rates this document
   tabulates; `mort_rate_mth` and `lapse_rate_mth` are what the recursion applies, each
   `1 − (1 − r)^(1/12)` **[std]**. That geometric form, rather than dividing by twelve, is what
   makes the in-force at every anniversary identical to the annual-step model's.
3. **Nothing annual moved.** The first-order equivalence and the *Deckungskapital* take policy-year
   arguments and are bit-identical; so do the *Versicherungssumme* schedule, the *Nachversicherungs-*
   *garantie* steps, the § 161 windows, the *Beitragszahlungsdauer* and the expense inflation, all of
   which step on the anniversary.
4. **The *Zahlweise* became real.** A modal *Zahlbeitrag* is collected in instalments on its own
   cycle instead of whole at the anniversary, so the four fractionated model points collect
   0,95 %–1,67 % less over the run. That is the premium-cessation rule biting where an annual grid
   could not express it, and § 168 VVG's *Versicherungsperiode* being modelled rather than
   approximated — the one approximation the annual grid had to declare, now gone.
5. **The totals the timing moved.** Death claims 9 899,20 € → 9 768,05 €, expenses 2 396,51 € →
   2 367,66 €, `net_cf` −804,77 € → −644,78 € on the anchor, and +4 158,46 € → +4 252,82 € on model
   point 2. The crossover to a negative policy year stays at policy year 14.
6. **The closure identity's split.** Deaths and lapses now interleave month by month, so the anchor
   reads 0,03261764 deaths and 0,53597922 lapses against 0,03305608 and 0,53554078; the expiring
   cohort 0,43140314 and the total 1,00000000 are unchanged.
7. **The premium-shock module reads twelve months back**, `prem_paid_pp(t)/prem_paid_pp(t−12)`,
   because the comparison is between consecutive renewals and not between consecutive instalments.

### What the model stage changed in these notes

Six corrections, each made because the built model disagreed with a sentence written before it
existed, and in each case the model was right. Nothing in the model was changed to fit a sentence.

1. **Pitfall 1's ordering was inverted.** It asked for `prem_net_level_pp() < prem_paid_pp(0)/φ`; the
   model gives 1 084,80 € against 733,01 €, the other way round, because `Gn` is struck on the
   **loaded** first-order rate and 90 % of that loading comes back as *Beitragsverrechnung*.
2. **`mort_rate_tar / mort_rate` is 1,6875 for a male and 3,375 for a female**, not 1,5 and 3,0: the
   unisex blend of a proxy whose female rate is half the male one is `0,75 × q̃(M)`. Corrected in
   *The two-order split* and in pitfall 7.
3. **`result_cf()` publishes eleven columns**, `liability_cf` added: the conventions suite reads
   `net_cf(t) = −liability_cf(t)` off the frame, so publishing the cells without the column fails.
4. **The `decl_scale = 0` uplift is 74,0 %**, not "roughly 75 %"; it is a ratio of premiums and the
   monthly grid leaves it where it was.
5. **The smoker premium ratio is 2,007** on the built model against the research file's 2,04, and the
   *Bruttobeitrag* 1 275,41 € against that scale's 1 316 € — both because the research construction
   used a zero *Rechnungszins* and the model uses the real 1,00 %. Both figures stand.
6. **Pitfall 5's `res_zill_pp_at(0,"BEF_PREM") == −z·k·G` is asserted to 1e-9**, as headroom: on
   the shipped calibration the two summations agree exactly.

The sensitivity the notes predicted before the model existed came out of it unaltered: moving `m`
from 1,0 to 1,5 moves the *Bruttobeitrag* 1 146,33 € → 1 404,05 €, **+22,5 %**, and the
*Zahlbeitrag* 711,63 € → 754,34 €, **+6,0 %** — mechanic 5's 23 % and 6 %, reproduced from the
mechanic rather than assumed.

---

## Valuation and reserve pointers

This library projects **gross best-estimate-style liability cash flows, undiscounted**, on a declared
grid. The valuation layers consume them and are **cited, never reproduced**.

- **The German statutory *Deckungsrückstellung*.** HGB § 341f requires it to be computed
  prospectively — HGB § 341f Abs. 1 requires the *Deckungsrückstellung* "in Höhe ihres
  versicherungsmathematisch errechneten Wertes ... und nach Abzug des versicherungsmathematisch
  ermittelten Barwerts der künftigen Beiträge (prospektive Methode)", and Abs. 2 adds the
  interest-guarantee test. **The rest of what this paragraph used to attribute to § 341f is not in
  it**: the requirement to use the premium bases with a prudent margin is DeckRV § 5 Abs. 1, whose
  terms are worth having — "Die Ableitung von Rechnungsgrundlagen auf der Basis eines besten
  Schätzwertes genügt nicht" — and the provision for future administration costs where the
  premium-paying period is shorter than the cover period, which is exactly model point 6's situation,
  belongs to the RechVersV, which was **not retrieved** and stays `[unverified]` [R21] [R10]
  [REG-R54]. [S4] gives the carrier-side chain: the reserve is computed "nach § 88 VAG und § 341e und
  § 341f HGB sowie den dazu erlassenen Rechtsverordnungen". The DeckRV caps the *Rechnungszins* at
  the ***Höchstzinssatz*** in force at conclusion (**1,00 %** from 1 January 2025) — a ceiling, not a
  rate: [S3] prices its term tariff at **0,25 %** — and the *Zillmersatz* at **25 ‰ of the *Summe
  aller Prämien***, the rate at conclusion applying for the whole term [R10] [REG-R14] [REG-R15]
  [REG-R16] [S3]. The model's
  `res_pp_at` is the **net, ungezillmert, first-order** reserve and is a **pricing diagnostic**: it is
  not floored, not *gezillmert* and not a statutory provision. The *Nullstellung* question — whether
  a negative individual reserve must be floored at zero — was **not established** (research gap 11),
  and because no reserve of any kind enters `result_cf()`, it does not reach these cash flows.
- **The *Zinszusatzreserve*.** DeckRV § 5 Abs. 3's *Referenzzins* and *Korridormethode* [REG-R17]
  reach this product only nominally: the reserve is small and short-lived, so a reader expecting the
  *Zinszusatzreserve* discussion that dominates `products/kapitallebensversicherung/` and
  `products/klassische_rentenversicherung/` will not find one here, and that is a product fact.
- **The *Überschuss* layer.** The MindZV's minimum allocation binds on the **HGB** accounts and is a
  transfer to the RfB, not a payout [R9] [REG-R18] [REG-R19]; § 139 VAG's *Bewertungsreserven*
  participation and its *Sicherungsbedarf* test are **economically empty** here, the attributable
  amount scaling with a *Deckungsrückstellung* that is nil or nominal [R11] [REG-R9] [unverified].
  The model's `prem_rebate` is the **contract-level** consequence of the allocation, not the
  allocation itself; a reader wanting the RfB mechanics should read
  `products/kapitallebensversicherung/technical-notes.md`.
- **Solvency II best estimate.** Probability-weighted future cash flows discounted at the relevant
  risk-free term structure, plus a risk margin [REG-R1] [REG-R2] [REG-R6], reaching German business
  **through the VAG** rather than directly. `BEL = Σ_t v(t) · liability_cf(t)` over the recursion
  above. **No cost-of-capital rate, contract-boundary rule or standard-formula shock in this library
  was read from a retrieved instrument**, so every such figure would be **[std]**, and none appears
  [R22]. Directive (EU) 2025/2 takes effect 30 January 2027 and nothing here implements a 2027 basis
  [REG-R3].
- **Contract boundary — and here the German product is easier than the French one.** The
  *Bruttobeitrag* is guaranteed for the whole term and the insurer's only unilateral lever is the
  declaration, which is not a repricing of a guaranteed term [R6] [REG-R27]. So there is none of the
  ambiguity `frlib`'s annually revisable *temporaire décès* faces, where the boundary may end at the
  next renewal. The model's posture is the same either way: project to expiry and publish the full
  stream; a boundary-truncated view is a truncation of `result_cf()`, never something baked into the
  projection.
- **IFRS 17.** Fulfilment cash flows plus a contractual service margin, applying to IFRS reporters
  from 1 January 2023 with no German carve-out [REG-R55]. The same expected-cash-flow engine feeds
  it; grouping, CSM and risk adjustment are out of scope. Professional standards sit with the DAV's
  *Fachgrundsätze* and its annual *Höchstrechnungszins* recommendation [REG-R56].

---

## Key sensitivities and model risks

In rough order of leverage for a German term-life block.

1. **The *Sicherheitszuschlag* `m`, and the reason it is not the lever it looks like.** `m` sets the
   *Bruttobeitrag* almost by itself, and its level is **not public** — the DAV *Richtlinie* regulates
   the procedure, not the level [R12] (research gap 6). But because 90 % of the extra margin is
   returned as *Beitragsverrechnung*, moving `m` across its argued range of 1.0 to 1.5 moves the
   *Bruttobeitrag* by about **23 %** and the *Zahlbeitrag* by about **6 %** (product spec,
   contractual mechanics). **So the parameter with the widest uncertainty has the narrowest effect on
   the cash flow that matters**, which is the most useful single result in this product and the
   reason the *Zahlbeitrag* is derived rather than assumed.
2. **`decl_scale` — the declaration, and the product's largest policyholder risk.** Setting it to 0
   raises `premiums` to `prem_gross` at every `t`, with **no § 163 procedure, no *Treuhänder* and no
   policyholder remedy** [R6] [REG-R27]. On the anchor that is a **74,0 % increase in the billed
   premium** — 21 303,65 € collected over the term against 12 243,75 € — with no change to any
   benefit and no change to any decrement. Nothing in the corpus bounds how far or how often
   a German carrier has actually moved a declaration on this product (research gap 1), and the
   premium-shock lapse module exists precisely because a stress that ignores the behavioural response
   understates itself.
3. **Mortality level and slope.** Both are **[std]** and unsourced. The level anchors on the research
   file's constructed unisex scale; the slope, 9,5 % per year of age, compounds — over model point
   14's 40 years it is worth a factor of about 36 between the first and last year's death rate, so a
   one-point error in the slope is worth far more than a one-point error in the level. The **DAV 2008
   T tables are the intended replacement and are not redistributable** [R12] [REG-R48]; a Destatis
   population table is **not** a substitute without a selection adjustment [REG-R52].
4. **The unisex mix `ω`.** It moves the tariff a great deal — female mortality at these ages is
   roughly half male [unverified] — and **no German carrier discloses its own mix**, which makes it
   one of the largest single sources of unexplained rate spread between carriers [R13] [REG-R34].
   Because the mix enters the tariff and not the projection, it is also the parameter that decides
   how large the cross-subsidy between model points 1 and 2 is.
5. **Lapse.** Nothing in the corpus supports any rate, and the whole-market *Stornoquote* is
   deliberately not used [R18] (gap 13). Cumulative lapse over the anchor's 25 years is large enough
   that the assumption governs how much of the profitable later term is ever reached — and note the
   direction: on a level-premium product the **early** years are the strained ones, so early lapse
   hurts, which inverts the intuition a reader arriving from the French annually-revisable product
   brings with him.
6. **Acquisition cost at the Zillmer ceiling.** The composite assumes a term tariff runs at 25 ‰ of
   the *Beitragssumme*, and a slim direct-channel cost would sit far below it [S3] [S12]. It is the
   single largest year-one cash flow after the premium, it is entirely **[std]**, and it decides
   whether small model points such as point 13 (50 000 €, five years) are viable at all.
7. **The suicide share, and the § 161 window's length.** Worth little in the totals and much in
   correctness: the German window is **three years** against France's one [R1] [`frlib` R1], so the
   parameter carries three times the weight, and an implementation that applies the switch to every
   year, or to a lapse, or that omits the restart on a *Nachversicherungsgarantie* increment, is
   wrong in a way the totals will not reveal.
8. **What the model deliberately cannot represent.** The *Kriegsklausel* is a catastrophe-scenario
   clause and is documented, not modelled; the § 161 mental-illness exception is the ground on which
   German suicide claims are actually litigated [R23] and cannot be a best-estimate switch; selective
   lapse is real and is off by default; and the *Kostenüberschuss* emerges in `net_cf` and is not
   returned, because the MindZV's *übriges Ergebnis* limb carries a different minimum share and the
   research file gives no basis on which to split a German term tariff's expense result [R9]
   [REG-R18]. Each is a stated choice, and each is stated here rather than left to be discovered from
   a number that looks wrong.

<!-- BEGIN generated citation links -- regenerate with tools/gen_citation_links.py -->
[R1]: #delib-risikolebensversicherung-r1
[R10]: #delib-risikolebensversicherung-r10
[R11]: #delib-risikolebensversicherung-r11
[R12]: #delib-risikolebensversicherung-r12
[R13]: #delib-risikolebensversicherung-r13
[R15]: #delib-risikolebensversicherung-r15
[R16]: #delib-risikolebensversicherung-r16
[R17]: #delib-risikolebensversicherung-r17
[R18]: #delib-risikolebensversicherung-r18
[R2]: #delib-risikolebensversicherung-r2
[R21]: #delib-risikolebensversicherung-r21
[R22]: #delib-risikolebensversicherung-r22
[R23]: #delib-risikolebensversicherung-r23
[R3]: #delib-risikolebensversicherung-r3
[R5]: #delib-risikolebensversicherung-r5
[R6]: #delib-risikolebensversicherung-r6
[R8]: #delib-risikolebensversicherung-r8
[R9]: #delib-risikolebensversicherung-r9
[REG-R1]: #delib-reg-r1
[REG-R14]: #delib-reg-r14
[REG-R15]: #delib-reg-r15
[REG-R16]: #delib-reg-r16
[REG-R17]: #delib-reg-r17
[REG-R18]: #delib-reg-r18
[REG-R19]: #delib-reg-r19
[REG-R2]: #delib-reg-r2
[REG-R20]: #delib-reg-r20
[REG-R23]: #delib-reg-r23
[REG-R24]: #delib-reg-r24
[REG-R26]: #delib-reg-r26
[REG-R27]: #delib-reg-r27
[REG-R28]: #delib-reg-r28
[REG-R3]: #delib-reg-r3
[REG-R34]: #delib-reg-r34
[REG-R46]: #delib-reg-r46
[REG-R48]: #delib-reg-r48
[REG-R52]: #delib-reg-r52
[REG-R54]: #delib-reg-r54
[REG-R55]: #delib-reg-r55
[REG-R56]: #delib-reg-r56
[REG-R6]: #delib-reg-r6
[REG-R8]: #delib-reg-r8
[REG-R9]: #delib-reg-r9
[std]: #delib-std
[unverified]: #delib-unverified
<!-- END generated citation links -->
